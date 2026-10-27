#!/usr/bin/env python3
# ! Alteração de IA - Revisar: script novo (01/10/2026, Pré-Fase 4) que gera, SÓ a partir da trilha bruta (trilha.py), o
# relatório para humanos de cada diagnóstico (um Markdown por caso, com o passo a passo em três camadas: o que o
# programa fez, o que o modelo declarou e o que o código conferiu), o índice de uma corrida e os indicadores somados
# (indicadores_raciocinio.json e .md, com --check e --colar).
# ! Motivo: o Eric pediu (01/10/2026) um relatório estruturado para humanos que siga a linha de raciocínio da IA a
# partir do arquivo bruto, para achar alucinação, erro de lógica e uso errado da documentação. O relatório não chama
# modelo nenhum: um segundo modelo resumindo o primeiro poderia inventar por cima, e a regra do projeto é script antes
# de modelo. Ele também não mistura camadas: a alegação do modelo aparece como alegação, com o trecho literal da
# resposta, e cada conferência diz se confere, se não confere ou se não dá para conferir por código. O gabarito
# aparece numa seção só, a de avaliação, porque na Fase 4 o agente não terá gabarito: tudo o que vem antes dela é o
# que ele poderá mostrar a quem desenvolve. Quando o modelo não escreve raciocínio (é o caso do qwen2.5:7b em todas
# as respostas oficiais), o relatório diz isso em vez de preencher o vazio.
"""Uso (em Programacao/AgenteCore/experimentos):
  RESULTADOS_DIR=resultados_alvo python gerar_relatorio_raciocinio.py --corrida fase3 --modelo qwen2.5:7b --versao 1 --caso lex-1
  RESULTADOS_DIR=resultados_alvo python gerar_relatorio_raciocinio.py --vitrine [--check] [--colar]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

import analisar_fase3b as a3b
import avaliar
import caminhos
import executar_fase3
import pre_fase4 as pf
import trilha as tr

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass

NOME = "indicadores_raciocinio"
PREFIXO = "tb_rac_"
# A vitrine: os relatórios que ficam versionados (o resto sai sob demanda, com --caso). Os 72 casos que nenhuma
# biblioteca viu, lidos pelo modelo decidido com a L1 dele, e a troca cruzada do Coder 3B, que é onde a
# documentação alheia mais atrapalhou (achado 4.42).
VITRINE = [("fase3", "qwen2.5:7b", 1, "avaliacao"), ("fase3b_ineditos", "qwen2.5:7b", 1, None),
           ("fase3b_cruzada_qwen", "qwen2.5-coder:3b", 1, None)]

ROTULO_DA_REGRA = {
    "quatro_linhas_presentes": "A resposta tem as quatro linhas pedidas",
    "rotulo_no_conjunto": "A causa está entre as permitidas",
    "fonte_existe_na_biblioteca": "O verbete citado existe na biblioteca",
    "fonte_estava_no_contexto": "O verbete citado estava no contexto entregue ao modelo",
    "campo_existe_no_caso": "O campo apontado aparece no caso",
    "rotulo_sustentado_por_verbete_do_contexto": "Algum verbete do contexto trata da causa respondida",
    "notas_nos_verbetes_citados": "Notas escritas pelo modelo nos verbetes citados",
    "impacto": "Frase de impacto",
    "causa_correta": "A causa respondida é a esperada",
    "campo_correto": "O campo respondido é o esperado",
    "verbete_de_ouro_no_contexto": "O verbete da causa esperada estava no contexto",
    "validador_da_biblioteca": "Decisão do validador em código",
    "revisao_humana_da_edicao": "Revisão humana da edição",
}
# Como dizer, numa frase, que uma conferência não conferiu (resumo do topo e índice da corrida).
FRASE_DA_FALHA = {
    "quatro_linhas_presentes": "faltam linhas pedidas na resposta",
    "rotulo_no_conjunto": "causa fora das permitidas",
    "fonte_existe_na_biblioteca": "verbete citado que não existe na biblioteca",
    "fonte_estava_no_contexto": "verbete citado que não estava no contexto",
    "campo_existe_no_caso": "campo apontado que não aparece no caso",
    "rotulo_sustentado_por_verbete_do_contexto": "nenhum verbete do contexto trata da causa respondida",
}
ROTULO_DO_RESULTADO = {"confere": "confere", "nao_confere": "**não confere**", "nao_se_aplica": "não se aplica",
                       "nao_verificavel": "não dá para conferir por código", "informativo": "informativo",
                       "aceita": "aceita", "rejeitada": "**rejeitada**"}
ROTULO_DA_PROVA = {"prompt_inteiro": "o prompt inteiro (documentação e texto do caso)",
                   "contexto": "a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada",
                   "nao_comprovado": "**não comprovado**: o prompt remontado difere do que a corrida gravou"}
NOME_DO_CAMPO = {"causa_raiz": "CAUSA_RAIZ", "campo": "CAMPO", "impacto": "IMPACTO", "fonte": "FONTE"}


def _cel(texto) -> str:
    """Texto seguro para célula de tabela Markdown."""
    return " ".join(str("" if texto is None else texto).split()).replace("|", "\\|")


def _num(v, casas: int = 1) -> str:
    if v is None:
        return "não registrado"
    return f"{float(v):.{casas}f}".replace(".", ",") if isinstance(v, float) else str(v)


def _tabela(cab: list[str], linhas: list[list[str]]) -> str:
    return "\n".join(["| " + " | ".join(cab) + " |", "|" + "---|" * len(cab)] + ["| " + " | ".join(l) + " |" for l in linhas])


def _bloco(texto: str) -> str:
    cerca = "````" if "```" in texto else "```"
    return f"{cerca}text\n{texto}\n{cerca}"


def hash_da_trilha(eventos: list[dict], tid: str) -> str:
    """Hash dos eventos de uma trilha, na forma em que estão no arquivo: qualquer evento alterado muda o hash."""
    linhas = [json.dumps(e, ensure_ascii=False, sort_keys=True) for e in eventos if e["trilha"] == tid]
    return hashlib.sha256("\n".join(linhas).encode("utf-8")).hexdigest()[:16]


def _evidencia(v: dict) -> str:
    e = v.get("evidencia")
    if v["regra"] == "notas_nos_verbetes_citados" and isinstance(e, dict):
        partes = []
        for item in e.get("verbetes") or []:
            notas = item["notas"]
            if not notas:
                partes.append(f"`{item['verbete']}`: sem notas do modelo")
                continue
            julgadas = Counter(n["veredito_humano"] or "sem revisão humana" for n in notas)
            partes.append(f"`{item['verbete']}`: {len(notas)} nota(s) do modelo (" + ", ".join(f"{k}: {n}" for k, n in sorted(julgadas.items())) + ")")
        return _cel("; ".join(partes) + ". " + e.get("limite", "")) if partes else _cel(e.get("limite", ""))
    if isinstance(e, dict):
        if "ausentes" in e:
            return "todas presentes" if not e["ausentes"] else "faltam: " + ", ".join(e["ausentes"])
        if "contexto" in e:
            return "contexto: " + ", ".join(f"`{i}`" for i in e["contexto"])
        if "verbetes" in e:
            return ("verbetes: " + ", ".join(f"`{i}`" for i in e["verbetes"])) if e["verbetes"] else "nenhum verbete do contexto trata dessa causa"
        if "codigo" in e:
            return _cel(f"código {e['codigo']}: {e.get('detalhe')}" if e.get("codigo") else e.get("detalhe"))
        return _cel(json.dumps(e, ensure_ascii=False))
    return _cel(e)


def relatorio_do_caso(eventos: list[dict], tid: str, outras: list[dict] | None = None, arquivo: str | None = None) -> str:
    """O relatório de um diagnóstico, montado só com os eventos da trilha `tid` (e os textos guardados nos blobs).
    `outras` é a lista opcional do mesmo caso nas outras versões da biblioteca (versão, causa respondida)."""
    blobs = tr.blobs_de(eventos)
    seq = [e for e in eventos if e["trilha"] == tid]
    if not seq:
        raise KeyError(f"trilha {tid!r} não está no arquivo")
    corrida = next((e["dados"] for e in eventos if e["tipo"] == "corrida"), {})
    por_tipo: dict[str, list[dict]] = {}
    for e in seq:
        por_tipo.setdefault(e["tipo"], []).append(e)
    entrada = por_tipo["entrada"][0]["dados"]
    cand = por_tipo["candidatos"][0]["dados"]
    prompts = {e["dados"].get("etapa"): e["dados"] for e in por_tipo["prompt"]}
    infs = {e["dados"].get("etapa"): e["dados"] for e in por_tipo["inferencia"]}
    prompt, inf = prompts["diagnostico"], infs["diagnostico"]
    decl = [e["dados"] for e in por_tipo.get("declaracao", [])]
    ver = [e["dados"] for e in por_tipo.get("verificacao", [])]
    campos = {d["campo"]: d for d in decl if d["campo"] in NOME_DO_CAMPO}
    raciocinio = next(d for d in decl if d["campo"] == "raciocinio")
    citadas = [d for d in decl if d["campo"] == "fonte_citada"]
    propostas = [d for d in decl if d["campo"] == "proposta"]
    sem_gabarito = [v for v in ver if not v["usa_gabarito"] and v["regra"] not in ("validador_da_biblioteca", "revisao_humana_da_edicao")]
    com_gabarito = [v for v in ver if v["usa_gabarito"]]
    escolhidos = [i for i in cand["itens"] if i["escolhido"]]
    conferem = sum(v["resultado"] == "confere" for v in sem_gabarito)
    nao_conferem = [v for v in sem_gabarito if v["resultado"] == "nao_confere"]
    julgaveis = [v for v in sem_gabarito if v["resultado"] in ("confere", "nao_confere")]
    resposta = blobs[inf["resposta"]]
    causa = campos.get("causa_raiz", {})
    modelo = corrida.get("modelo", "modelo")

    resumo = _tabela(["Camada", "Resumo"], [
        ["O que o programa fez",
         f"buscou entre {len(cand['itens'])} verbetes e entregou {len(escolhidos)} ({', '.join('`' + i['id'] + '`' for i in escolhidos)}); prompt de "
         f"{_num(inf.get('tokens_entrada'))} tokens; resposta de {_num(inf.get('tokens_saida'))} tokens em {_num(inf.get('segundos'))} s"],
        ["O que o modelo declarou",
         (f"causa `{causa.get('lido')}`" if causa.get("lido") else "nenhuma causa no formato pedido")
         + f"; {len(citadas)} verbete(s) citado(s); "
         + ("não escreveu raciocínio antes das quatro linhas" if raciocinio["vazio"] else "escreveu raciocínio antes das quatro linhas")],
        ["O que o código conferiu",
         f"{conferem} de {len(julgaveis)} conferências conferem"
         + ("; o que não confere: " + "; ".join(FRASE_DA_FALHA.get(v["regra"], v["regra"]) + (f" (`{v['alvo']}`)" if v.get("alvo") else "") for v in nao_conferem) if nao_conferem else "")],
    ])

    linhas_cand = [[str(i["posicao"]), f"`{i['id']}`", _num(i["pontuacao"], 3), _num(i["bm25"], 3), _num(i["reforco_endpoint"]), _num(i["reforco_entidade"]),
                    _num(i["reforco_status"]), "entregue ao modelo" if i["escolhido"] else "descartado"] for i in cand["itens"][:max(6, cand["k"] + 3)]]
    c = cand["consulta"]
    verbetes_txt = "\n\n".join(f"**`{p['id']}`**\n\n{_bloco(blobs[p['sha']])}" for p in prompt["partes"] if p["papel"] == "verbete")
    fixos = "\n\n".join(f"<details><summary>{'Instrução dada ao modelo' if p['papel'] == 'instrucao' else 'Formato pedido para a resposta'} "
                        f"({len(blobs[p['sha']])} caracteres)</summary>\n\n{_bloco(blobs[p['sha']])}\n\n</details>"
                        for p in prompt["partes"] if p["papel"] in ("instrucao", "formato"))
    provas = prompt["provas"]
    linhas_prova = [["O snapshot da biblioteca lido agora é o da corrida", "sim" if provas["biblioteca"] else "**não**"],
                    ["Os verbetes entregues, o tamanho e o hash da documentação batem com o registro", "sim" if provas["contexto"] else "**não**"],
                    ["O prompt de proposta gravado começa por este prompt e por esta resposta",
                     "não há proposta gravada para este caso" if provas["prompt_de_proposta"] is None else ("sim" if provas["prompt_de_proposta"] else "**não**")],
                    ["O hash do prompt enviado ao Ollama é o deste prompt",
                     "a corrida não guardou esse hash" if provas["hash_do_prompt_enviado"] is None else ("sim" if provas["hash_do_prompt_enviado"] else "**não**")]]

    linhas_decl = []
    for chave, nome in NOME_DO_CAMPO.items():
        d = campos.get(chave)
        if d is None or d.get("ausente"):
            linhas_decl.append([nome, "**a linha não está na resposta**", ""])
        else:
            linhas_decl.append([nome, f"`{_cel(d['valor'])}`", f"caracteres {d['ini']} a {d['fim']} da resposta"])
    if raciocinio["vazio"]:
        texto_rac = f"O `{modelo}` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas."
    else:
        texto_rac = "Texto escrito antes das quatro linhas, como veio (alegação do modelo, não conferida por si só):\n\n" + _bloco(raciocinio["valor"])

    def linha_ver(v: dict) -> list[str]:
        alvo = v.get("alvo")
        sobre = ", ".join(f"`{_cel(a)}`" for a in alvo) if isinstance(alvo, list) else (f"`{_cel(alvo)}`" if alvo not in (None, "resposta") else "")
        return [ROTULO_DA_REGRA.get(v["regra"], v["regra"]), sobre,
                ROTULO_DO_RESULTADO.get(v["resultado"], v["resultado"]), _evidencia(v)]

    def linha_avaliacao(v: dict) -> list[str]:
        esperado = (v.get("evidencia") or {}).get("gabarito")
        return [ROTULO_DA_REGRA[v["regra"]], f"`{_cel(v['alvo'])}`" if v.get("alvo") else "nada", f"`{_cel(esperado)}`" if esperado else "",
                ROTULO_DO_RESULTADO[v["resultado"]]]

    partes = [
        "<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.",
        "     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->",
        f"# Diagnóstico do caso `{entrada['caso']}` pelo `{modelo}` com a biblioteca L{corrida.get('biblioteca_epoca')}",
        "",
        f"Trilha `{tid}`. Corrida `{corrida.get('corrida')}`, Ollama {', '.join(corrida.get('versoes_do_ollama') or [])}; classe {entrada['classe']}, nível {entrada['nivel']}; "
        f"texto dos casos: {corrida.get('texto_dos_casos')}. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; "
        "o que o código conferiu é o que se pôde checar da alegação.",
        "", resumo, "",
        "## O que o programa fez", "",
        "### Entrada", "", "O caso como foi posto no prompt:", "", _bloco(blobs[entrada["texto"]]), "",
        "### Busca na biblioteca", "",
        f"Consulta montada em código: endpoint `{c['endpoint']}`, entidade `{c['entidade']}`, status `{c['status']}`, {c['termos']} termos. "
        f"A busca pontuou os {len(cand['itens'])} verbetes e entregou os {cand['k']} primeiros; abaixo, os mais bem pontuados.", "",
        _tabela(["Posição", "Verbete", "Pontuação", "BM25", "Reforço por endpoint", "Reforço por entidade", "Reforço por status", "Destino"], linhas_cand), "",
        "### Documentação entregue ao modelo", "", verbetes_txt, "",
        "### Prompt", "",
        f"{prompt['chars']} caracteres em {len(prompt['partes'])} partes (hash `{prompt['sha']}`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do "
        f"executor, e está provado até: {ROTULO_DA_PROVA[prompt['nivel']]}.", "",
        _tabela(["Prova", "Resultado"], linhas_prova), "", fixos, "",
        "### Inferência", "",
        f"Entrada de {_num(inf.get('tokens_entrada'))} tokens, saída de {_num(inf.get('tokens_saida'))} (teto de {_num(inf.get('teto_tokens'))}); {_num(inf.get('segundos'))} s no total "
        f"({_num(inf.get('prefill_ms'))} ms lendo o prompt, {_num(inf.get('geracao_ms'))} ms gerando)."
        + (f" A probabilidade de cada token está em `{inf['logprobs']['arquivo']}`." if inf.get("logprobs") else " A corrida não gravou a probabilidade dos tokens."),
        "", "Resposta, como veio:", "", _bloco(resposta), "",
        "## O que o modelo declarou", "", texto_rac, "",
        _tabela(["Linha", "Valor (trecho literal da resposta)", "Onde está"], linhas_decl), "",
        "## O que o código conferiu", "",
        "Conferências que não dependem de saber a resposta certa:", "",
        _tabela(["Conferência", "Sobre", "Resultado", "Evidência"], [linha_ver(v) for v in sem_gabarito]), "",
        "## Avaliação contra o gabarito", "",
        "Esta é a única seção que usa o gabarito do caso; nada acima depende dele.", "",
        _tabela(["Pergunta", "Respondido", "Esperado", "Resultado"], [linha_avaliacao(v) for v in com_gabarito]), "",
    ]
    if propostas or "proposta" in prompts:
        ip = infs.get("proposta", {})
        partes += ["## Proposta de edição da biblioteca", "",
                   f"Caso de aprendizado: depois do diagnóstico o modelo recebeu a correção e pôde propor edições na documentação ({_num(ip.get('tokens_saida'))} tokens em "
                   f"{_num(ip.get('segundos'))} s). Cada proposta passou pelo validador em código." if propostas else
                   "Caso de aprendizado: o modelo recebeu a correção e não propôs edição nenhuma.", ""]
        por_pai: dict[int, list[dict]] = {}
        for e in por_tipo.get("verificacao", []) + por_tipo.get("acao", []):
            if e.get("pai") is not None:
                por_pai.setdefault(e["pai"], []).append(e)
        linhas_p = []
        for e in [x for x in por_tipo.get("declaracao", []) if x["dados"]["campo"] == "proposta"]:
            d = e["dados"]
            filhos = por_pai.get(e["seq"], [])
            validador = next((f["dados"] for f in filhos if f["tipo"] == "verificacao"), None)
            acao = next((f for f in filhos if f["tipo"] == "acao"), None)
            humano = next((f["dados"]["resultado"] for f in por_pai.get(acao["seq"], []) if f["tipo"] == "verificacao"), None) if acao else None
            linhas_p.append([str(d.get("numero")), _cel(d.get("operacao")), f"`{_cel(d.get('verbete'))}`", _cel(d.get("valor")),
                             (ROTULO_DO_RESULTADO.get(validador["resultado"], validador["resultado"]) + (": " + _evidencia(validador) if validador.get("evidencia") else "")) if validador else "",
                             "aplicada" if acao else "não aplicada", humano or ("sem revisão humana" if acao else "")])
        if linhas_p:
            partes += [_tabela(["#", "Operação", "Verbete", "Texto proposto (alegação do modelo)", "Validador em código", "Biblioteca", "Revisão humana"], linhas_p), ""]
    if outras:
        partes += ["## O mesmo caso com as outras versões da biblioteca", "",
                   _tabela(["Versão", "Causa respondida", "Verbetes entregues"], [[f"L{o['versao']}", f"`{_cel(o['causa'])}`", ", ".join(f"`{i}`" for i in o["verbetes"])] for o in outras]), ""]
    partes += ["## Rastro", "",
               f"Gerado dos eventos {seq[0]['seq']} a {seq[-1]['seq']} da trilha" + (f" `{arquivo}`" if arquivo else "") + f"; hash dos eventos deste caso: `{hash_da_trilha(eventos, tid)}`. "
               "Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).", ""]
    return "\n".join(partes)


# ------------------------------------------------------------------ versão 2: molde de justificativa e relatório em ordem fixa

# ! Alteração de IA - Revisar: (26/10/2026, Fase 4, pacote P1) a justificativa humanizada por molde (especificação, seção 7),
# o contraste com a segunda causa (4.2) e o relatório por caso da versão 2 em ordem fixa (seção 11). Tudo em código, a
# partir dos campos do nó de decisão e dos eventos da trilha; nenhuma chamada a modelo. O molde só cita verbetes que a
# evidência do nó traz, e abaixo do selo "baixo" a frase de incerteza é obrigatória.
# ! Motivo: explicação fluente sem base aumenta a dependência excessiva (risco 8 da especificação); o texto que o
# desenvolvedor lê precisa dizer só o que o código mediu, e o relatório precisa ser conferível em segundos (veredito,
# evidência, contraste, FONTE, ação, árvore), com o gabarito por último e à parte, porque na Fase 4 ele não existe.
MARCA_DO_MOLDE = "gerada por molde"
PAPEIS_COM_VERBETE = ("verbete_entregue", "verbete_citado")


def _prob(v) -> str:
    return "não registrada" if v is None else _num(float(v), 2)


def _ids_da_evidencia(no: dict) -> list[str]:
    """Só os verbetes que a evidência do nó aponta pelo id: é tudo o que o molde pode citar."""
    return [e["id"] for e in no.get("evidencia") or [] if e.get("id") and e.get("papel") in PAPEIS_COM_VERBETE]


def _segunda(no: dict) -> dict | None:
    outras = [a for a in no.get("alternativas") or [] if a.get("opcao") != no.get("escolha")]
    if not outras:
        return None
    return sorted(outras, key=lambda a: -(a.get("escore") if isinstance(a.get("escore"), (int, float)) else -1))[0]


def _escore_da_escolha(no: dict):
    for a in no.get("alternativas") or []:
        if a.get("opcao") == no.get("escolha") and isinstance(a.get("escore"), (int, float)):
            return a["escore"]
    return (no.get("confianca") or {}).get("p_rotulo")


def contraste_por_molde(no: dict) -> str:
    """"Por que esta e não a segunda", só com os campos do nó: escolha, segunda alternativa, probabilidades e os
    verbetes da evidência."""
    segunda = _segunda(no)
    if segunda is None:
        return f"{no['escolha']} sem alternativa registrada no nó"
    ids = _ids_da_evidencia(no)
    texto = (f"{no['escolha']} e não {segunda['opcao']}: a escolha tem probabilidade {_prob(_escore_da_escolha(no))} "
             f"contra {_prob(segunda.get('escore'))}")
    return texto + (f"; verbete(s) na evidência: {', '.join(ids)}" if ids else "; nenhum verbete entregue na evidência")


def _campo_e_sinal(no: dict, por_seq: dict[int, dict]) -> tuple[str | None, str | None]:
    """O campo e o sinal em código que a evidência aponta (evento de poda com o diff contra o contrato, ou o campo
    declarado na trilha); sem eventos, só o que o nó trouxer em `campo`."""
    campo, sinal = no.get("campo"), None
    tid = None
    for e in no.get("evidencia") or []:
        ev = por_seq.get(e["seq"])
        if ev is None:
            continue
        tid = tid or ev.get("trilha")
        if ev["tipo"] == "poda" and ev["dados"].get("diff"):
            d = ev["dados"]["diff"][0]
            campo = campo or d.get("campo")
            sinal = sinal or f"{d.get('campo')}: esperado {d.get('esperado')}, recebido {d.get('recebido')}"
        elif e.get("papel") == "sinal_em_codigo" and ev["dados"].get("sinal"):
            sinal = sinal or str(ev["dados"]["sinal"])
    if campo is None and tid is not None:
        for ev in por_seq.values():
            if ev.get("trilha") == tid and ev["tipo"] == "declaracao" and ev["dados"].get("campo") == "campo" and ev["dados"].get("lido"):
                campo = ev["dados"]["lido"]
                break
    return campo, sinal


def frase_de_incerteza(no: dict, campo: str | None) -> str | None:
    c = no.get("confianca") or {}
    if c.get("selo") != "baixo":
        return None
    onde = f" e confira o campo {campo} antes de agir" if campo else " e confira o caso antes de agir"
    return f"O agente não está seguro desta causa (probabilidade {_prob(c.get('p_rotulo'))}); trate como hipótese{onde}."


def justificativa_por_molde(no: dict, eventos: list[dict] | None = None, verificacoes=(), intervencoes=()) -> str:
    """A frase que o desenvolvedor lê, em três partes fixas (especificação, seção 7): o que foi decidido e com base em
    quê; por que não a alternativa; o que o código conferiu e o que não dá para conferir. Cita só o que está nos campos
    do nó, nos eventos apontados pela evidência, nas conferências e nas intervenções recebidas."""
    por_seq = {e["seq"]: e for e in (eventos or [])}
    escolha = no["escolha"]
    campo, sinal = _campo_e_sinal(no, por_seq)
    ids = _ids_da_evidencia(no)
    partes = []
    base = f"O agente respondeu {escolha}" + (f" no campo {campo}" if campo else "")
    motivos = []
    if sinal:
        motivos.append(f"o sinal {sinal} está presente na resposta HTTP")
    if ids:
        motivos.append(f"o verbete {ids[0]} estava entre os entregues ao modelo" if len(ids) == 1
                       else f"os verbetes {', '.join(ids)} estavam entre os entregues ao modelo")
    partes.append(base + (" porque " + " e ".join(motivos) if motivos else ", com a evidência registrada nos eventos do nó") + ".")
    segunda = _segunda(no)
    if segunda is not None:
        frase = f"A segunda causa, {segunda['opcao']}, ficou com probabilidade {_prob(segunda.get('escore'))}"
        if segunda.get("sustentada_por") == []:
            frase += " e nenhum verbete entregue a sustenta"
        partes.append(frase + ".")
    fontes = [v for v in verificacoes if v.get("regra") == "fonte_estava_no_contexto" and v.get("alvo")]
    if fontes:
        fora = [v["alvo"] for v in fontes if v.get("resultado") == "nao_confere"]
        partes.append(f"A FONTE cita {len(fontes)} verbete(s), " + ("todos presentes no contexto." if not fora
                      else f"{len(fora)} fora do contexto entregue ({', '.join(fora)})."))
    for i in intervencoes:
        v = i.get("verbete")
        if i.get("mudou_rotulo"):
            partes.append(f"A remoção do verbete {v} mudou a resposta (de {i.get('rotulo_antes')} para {i.get('rotulo_depois')}), "
                          "então ele pesou na decisão.")
        else:
            partes.append(f"A remoção do verbete {v} não mudou a resposta: sem efeito medido do contexto.")
    if any(v.get("regra") == "impacto" and v.get("resultado") == "nao_verificavel" for v in verificacoes):
        partes.append("O que não dá para conferir por código: a frase de impacto.")
    d = no.get("divergencia") or {}
    if d.get("ha"):
        partes.append("O que o modelo declarou diverge do que o código mediu"
                      + (f" (entre {' e '.join(d['entre'])})" if d.get("entre") else "") + (f": {d['detalhe']}." if d.get("detalhe") else "."))
    if no.get("falha"):
        partes.append(f"Este nó está marcado com a falha {no['falha']} (origem: {tr.origem_da_falha(no['falha'])}).")
    incerteza = frase_de_incerteza(no, campo)
    if incerteza:
        partes.append(incerteza)
    return " ".join(partes)


def _resumo_do_evento(e: dict, blobs: dict) -> str:
    d = e["dados"]
    tipo = e["tipo"]
    if tipo == "decisao":
        return f"{d.get('decisao')}: escolha {d.get('escolha')}; divergência {'sim' if (d.get('divergencia') or {}).get('ha') else 'não'}"
    if tipo == "declaracao":
        return f"{d.get('campo')}: " + ("ausente" if d.get("ausente") else f"`{_cel(d.get('valor'))}`")
    if tipo == "verificacao":
        return f"{d.get('regra')}: {d.get('resultado')}" + (" (só na avaliação, ao fim desta seção)" if d.get("usa_gabarito") else "")
    if tipo == "interceptacao":
        return f"{d.get('metodo')} {d.get('caminho')} {d.get('status')}"
    if tipo == "poda":
        return f"{d.get('alvo')}: {len(d.get('diff') or [])} diferença(s) contra o contrato; regras {', '.join(d.get('regras') or [])}"
    if tipo == "intervencao":
        return f"{d.get('tipo')} de {d.get('verbete')}: rótulo {d.get('rotulo_antes')} para {d.get('rotulo_depois')}"
    if tipo == "inferencia":
        return f"{d.get('etapa')}: {_num(d.get('segundos'))} s"
    if tipo == "candidatos":
        return f"{sum(1 for i in d.get('itens') or [] if i.get('escolhido'))} de {len(d.get('itens') or [])} verbetes entregues"
    if tipo == "entrada":
        return f"caso {d.get('caso')}"
    if tipo in ("cura", "acao", "incidente", "revisao", "edicao_biblioteca", "prompt"):
        return _cel(json.dumps({k: v for k, v in d.items() if not isinstance(v, (dict, list))}, ensure_ascii=False))[:160]
    return ""


def relatorio_do_caso_v2(eventos: list[dict], tid: str, comando_reexecucao: str | None = None, pasta_blobs: Path | None = None) -> str:
    """O relatório de um caso da trilha v2, na ordem fixa da especificação (seção 11): veredito com selo e carimbo
    de conflito; evidência (diff do contrato ao lado do trecho podado, com hash); contraste; FONTE com conferência e
    intervenção; linha de ação com o comando de reexecução; a árvore completa recolhida, com a avaliação contra o
    gabarito por último e à parte (só quando houve gabarito)."""
    blobs = tr.blobs_de(eventos, pasta_blobs)
    seq = [e for e in eventos if e["trilha"] == tid]
    if not seq:
        raise KeyError(f"trilha {tid!r} não está no arquivo")
    cab = next((e["dados"] for e in eventos if e["tipo"] == "corrida"), {})
    por_tipo: dict[str, list[dict]] = {}
    for e in seq:
        por_tipo.setdefault(e["tipo"], []).append(e)
    entrada = (por_tipo.get("entrada") or [{"dados": {}}])[0]["dados"]
    decl = {e["dados"]["campo"]: e["dados"] for e in por_tipo.get("declaracao", []) if e["dados"].get("campo") in NOME_DO_CAMPO}
    citadas = [e["dados"] for e in por_tipo.get("declaracao", []) if e["dados"].get("campo") == "fonte_citada"]
    ver = [e["dados"] for e in por_tipo.get("verificacao", [])]
    sem_gabarito = [v for v in ver if not v.get("usa_gabarito")]
    com_gabarito = [v for v in ver if v.get("usa_gabarito")]
    nos = [e for e in por_tipo.get("decisao", [])]
    diag = next((e["dados"] for e in reversed(nos) if e["dados"].get("decisao") == "diagnostico"), None)
    intervencoes = [e["dados"] for e in por_tipo.get("intervencao", [])]
    podas = [e for e in por_tipo.get("poda", [])]
    interceptacoes = [e for e in por_tipo.get("interceptacao", [])]
    caso = entrada.get("caso", tid)

    def valor(chave: str) -> str:
        d = decl.get(chave)
        if d is None or d.get("ausente"):
            return "**a linha não está na resposta**"
        return f"`{_cel(d.get('valor'))}`"

    confianca = (diag or {}).get("confianca") or {}
    selo = confianca.get("selo") or "sem selo"
    divergencia = (diag or {}).get("divergencia") or {}
    veredito = [f"**CAUSA_RAIZ:** {valor('causa_raiz')} · **CAMPO:** {valor('campo')} · selo de probabilidade: **{selo}**"
                + (f" (p = {_prob(confianca.get('p_rotulo'))})" if confianca.get("p_rotulo") is not None else "")
                + (f" · **CONFLITO**: {_cel(divergencia.get('detalhe') or 'o declarado diverge do medido')}" if divergencia.get("ha") else ""),
                "", f"**IMPACTO (declarado):** {valor('impacto')}", ""]
    if diag is not None:
        veredito += [f"Justificativa ({MARCA_DO_MOLDE}): {diag.get('justificativa') or justificativa_por_molde(diag, eventos, sem_gabarito, intervencoes)}", ""]
    else:
        veredito += ["Nenhum nó de decisão de diagnóstico nesta trilha.", ""]

    evidencia = []
    if podas:
        for e in podas:
            d = e["dados"]
            linhas = [[_cel(x.get("campo")), _cel(x.get("esperado")), _cel(x.get("recebido"))] for x in d.get("diff") or []]
            evidencia += [f"Poda de `{d.get('alvo')}` (evento {e['seq']}): regras {', '.join(d.get('regras') or [])}; "
                          f"antes {_cel(json.dumps(d.get('antes'), ensure_ascii=False))}, depois {_cel(json.dumps(d.get('depois'), ensure_ascii=False))}.", ""]
            if linhas:
                evidencia += [_tabela(["Campo do contrato", "Esperado", "Recebido"], linhas), ""]
            if d.get("sha") in blobs:
                texto = blobs[d["sha"]]
                evidencia += [f"Trecho podado (hash `{d['sha']}`):", "", _bloco(texto if texto is not None else f"(gravado fora da linha: {d['sha']})"), ""]
    for e in interceptacoes:
        d = e["dados"]
        evidencia += [f"Interceptação (evento {e['seq']}): `{d.get('metodo')} {d.get('caminho')}` status {d.get('status')}; corpo `{d.get('corpo')}`, "
                      f"árvore `{d.get('arvore')}`.", ""]
    if not podas and not interceptacoes:
        texto_caso = blobs.get(entrada.get("texto")) if entrada.get("texto") else None
        evidencia += ["Não houve interceptação nem poda nesta trilha: o caso entrou em texto." + ("" if texto_caso is None else " Como foi posto no prompt:"), ""]
        if texto_caso is not None:
            evidencia += [_bloco(texto_caso), ""]

    contraste = []
    if diag is not None:
        contraste += [diag.get("contraste") or contraste_por_molde(diag), ""]
        alternativas = sorted(diag.get("alternativas") or [], key=lambda a: -(a.get("escore") if isinstance(a.get("escore"), (int, float)) else -1))
        if alternativas:
            contraste += [_tabela(["Alternativa", "Probabilidade ou escore", "Escolhida"],
                                  [[_cel(a.get("opcao")), _prob(a.get("escore")), "sim" if a.get("opcao") == diag.get("escolha") else ""] for a in alternativas]), ""]
    else:
        contraste += ["Sem nó de diagnóstico, não há contraste.", ""]

    fonte = [f"Linha FONTE como veio: {valor('fonte')}; verbetes citados: " + (", ".join(f"`{_cel(c.get('valor'))}`" for c in citadas) or "nenhum") + ".", ""]
    conf_fonte = [v for v in sem_gabarito if str(v.get("regra", "")).startswith("fonte_") or v.get("regra") == "rotulo_sustentado_por_verbete_do_contexto"]
    if conf_fonte:
        fonte += [_tabela(["Conferência", "Sobre", "Resultado", "Evidência"],
                          [[ROTULO_DA_REGRA.get(v["regra"], v["regra"]), f"`{_cel(v['alvo'])}`" if v.get("alvo") else "",
                            ROTULO_DO_RESULTADO.get(v["resultado"], v["resultado"]), _evidencia(v)] for v in conf_fonte]), ""]
    if intervencoes:
        fonte += [_tabela(["Intervenção", "Verbete", "Rótulo antes", "Rótulo depois", "p antes", "p depois", "Efeito"],
                          [[_cel(i.get("tipo")), f"`{_cel(i.get('verbete'))}`", _cel(i.get("rotulo_antes")), _cel(i.get("rotulo_depois")),
                            _prob(i.get("p_antes")), _prob(i.get("p_depois")),
                            ("mudou a resposta: o verbete pesou na decisão" if i.get("mudou_rotulo") else "sem efeito medido do contexto")
                            + (" (só um limite inferior da queda: o rótulo saiu das alternativas devolvidas)" if i.get("limite_inferior") else "")]
                           for i in intervencoes]), ""]
    else:
        fonte += ["Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.", ""]

    campo_decl = (decl.get("campo") or {}).get("lido")
    onde = next((f"`{e['dados'].get('metodo')} {e['dados'].get('caminho')}`" for e in interceptacoes), None)
    acao = [("Confira o campo `" + _cel(campo_decl) + "`" if campo_decl else "Confira a resposta") + (f" em {onde}" if onde else " no caso de entrada")
            + " e compare com o contrato esperado pela interface.", "",
            f"Comando para reexecutar o caso: `{comando_reexecucao}`" if comando_reexecucao else "Comando de reexecução: não registrado nesta trilha.", ""]

    linhas_arvore = [[str(e["seq"]), str(e.get("passo")), e["tipo"], e["camada"], e["origem"], _cel(e.get("ts")), _resumo_do_evento(e, blobs)] for e in seq]
    arvore = [f"<details><summary>{len(seq)} eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>", "",
              _tabela(["seq", "passo", "Tipo", "Camada", "Origem", "Quando", "Resumo"], linhas_arvore), "", "</details>", ""]
    if nos:
        arvore += ["Nós de decisão:", ""]
        for e in nos:
            d = e["dados"]
            ev = ", ".join(f"evento {x['seq']} ({x.get('papel')}{', ' + x['id'] if x.get('id') else ''})" for x in d.get("evidencia") or []) or "nenhuma"
            arvore += [f"- evento {e['seq']}, `{d.get('decisao')}`: escolha `{_cel(d.get('escolha'))}`; resultado {_cel(d.get('resultado'))}; evidência: {ev}; "
                       f"divergência: {'sim' if (d.get('divergencia') or {}).get('ha') else 'não'}; falha: {_cel(d.get('falha') or 'nenhuma')}; "
                       f"prov.used: {', '.join(d.get('prov', {}).get('used') or []) or 'nenhum'}" + (f" (gen_ai: {tr.exportar_nome_gen_ai(d.get('decisao'))})" if tr.exportar_nome_gen_ai(d.get("decisao")) else "")]
        arvore += [""]
    if com_gabarito:
        arvore += ["### Avaliação contra o gabarito", "", "Esta é a única parte que usa o gabarito do caso; nada acima depende dele.", "",
                   _tabela(["Pergunta", "Respondido", "Esperado", "Resultado"],
                           [[ROTULO_DA_REGRA.get(v["regra"], v["regra"]), f"`{_cel(v['alvo'])}`" if v.get("alvo") else "nada",
                             f"`{_cel((v.get('evidencia') or {}).get('gabarito'))}`" if isinstance(v.get("evidencia"), dict) and v["evidencia"].get("gabarito") else "",
                             ROTULO_DO_RESULTADO.get(v["resultado"], v["resultado"])] for v in com_gabarito]), ""]
    else:
        arvore += ["Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.", ""]

    partes = [
        "<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.",
        "     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->",
        f"# Caso `{caso}`: o que o agente fez, declarou e conferiu",
        "",
        f"Trilha `{tid}`; modelo `{cab.get('modelo')}`, Ollama {cab.get('versao_ollama')}" + (f", Playwright {cab.get('playwright')} com navegador {cab.get('navegador')}" if cab.get("playwright") else "")
        + f"; esquema v{cab.get('versao_do_esquema', 2)}. Origem dos eventos: " + ", ".join(sorted({e["origem"] for e in seq})) + ".",
        "",
        "## 1. Veredito", "", *veredito,
        "## 2. Evidência", "", *evidencia,
        "## 3. Contraste com a segunda causa", "", *contraste,
        "## 4. FONTE declarada e conferida", "", *fonte,
        "## 5. Linha de ação", "", *acao,
        "## 6. Árvore completa", "", *arvore,
        "## Rastro", "",
        f"Gerado dos eventos {seq[0]['seq']} a {seq[-1]['seq']} da trilha; hash dos eventos deste caso: `{hash_da_trilha(eventos, tid)}`. "
        "Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.", "",
    ]
    return "\n".join(partes)


# ------------------------------------------------------------------ indicadores de uma ou mais trilhas

def indicadores(eventos: list[dict]) -> dict:
    """Contagens de uma trilha: quantos diagnósticos, em quantos o modelo não escreveu raciocínio, o resultado de cada
    conferência que não usa o gabarito, a avaliação contra o gabarito, o nível de prova dos prompts e o acerto separado
    por "a causa respondida é tratada por algum verbete do contexto" (sinal que o agente pode calcular sozinho)."""
    trilhas = tr.por_trilha(eventos)
    diag = {k: v for k, v in trilhas.items() if any(e["tipo"] == "inferencia" for e in v)}
    regras: dict[str, Counter] = {}
    avaliacao: dict[str, Counter] = {}
    provas: Counter = Counter()
    sustentacao = {"sustentado": Counter(), "nao_sustentado": Counter()}
    sem_raciocinio = 0
    propostas: Counter = Counter()
    for seq in diag.values():
        ver = [e["dados"] for e in seq if e["tipo"] == "verificacao"]
        for v in ver:
            if v["regra"] == "validador_da_biblioteca":
                propostas[v["resultado"]] += 1
            elif v["regra"] == "revisao_humana_da_edicao":
                propostas["humano: " + v["resultado"]] += 1
            elif v["usa_gabarito"]:
                avaliacao.setdefault(v["regra"], Counter())[v["resultado"]] += 1
            else:
                regras.setdefault(v["regra"], Counter())[v["resultado"]] += 1
        sem_raciocinio += any(e["tipo"] == "declaracao" and e["dados"]["campo"] == "raciocinio" and e["dados"]["vazio"] for e in seq)
        provas[next(e["dados"]["nivel"] for e in seq if e["tipo"] == "prompt" and e["dados"].get("etapa") == "diagnostico")] += 1
        sus = next((v["resultado"] for v in ver if v["regra"] == "rotulo_sustentado_por_verbete_do_contexto"), None)
        certo = next((v["resultado"] for v in ver if v["regra"] == "causa_correta"), None)
        if sus in ("confere", "nao_confere") and certo:
            sustentacao["sustentado" if sus == "confere" else "nao_sustentado"][certo] += 1
    ordem = [r for r in ROTULO_DA_REGRA if r in regras]

    def taxa(c: Counter) -> dict:
        n = c["confere"] + c["nao_confere"]
        return {"n": n, "acertos": c["confere"], "acerto_pct": round(100 * c["confere"] / n, 1) if n else None}

    return {"diagnosticos": len(diag), "sem_raciocinio_antes_das_linhas": sem_raciocinio,
            "conferencias": [{"regra": r, **{k: regras[r][k] for k in ("confere", "nao_confere", "nao_se_aplica", "nao_verificavel", "informativo") if regras[r][k]}} for r in ordem],
            "avaliacao": {r: dict(c) for r, c in avaliacao.items()},
            "prova_do_prompt": dict(provas),
            "acerto_por_sustentacao": {k: taxa(c) for k, c in sustentacao.items()},
            "propostas": dict(propostas)}


def montar(trilhas: list[tuple[str, str, int, list[dict]]], gerado_em: str | None = None) -> dict:
    return {"metadados": {"gerado_em": gerado_em or datetime.now().isoformat(timespec="seconds"),
                          "fonte": "trilhas remontadas por trilha.adaptar_corrida a partir dos registros das corridas"},
            "corridas": [{"corrida": c, "modelo": m, "biblioteca_epoca": v,
                          # quem escreveu a biblioteca lida (na troca cruzada não é o modelo que diagnostica)
                          "dono_da_biblioteca": next((e["dados"].get("dono_da_biblioteca") for e in ev if e["tipo"] == "corrida"), m),
                          **indicadores(ev)} for c, m, v, ev in trilhas]}


def render(dado: dict) -> str:
    f = a3b.f
    cs = dado["corridas"]

    def nome(x: dict) -> str:
        dono = "" if x.get("dono_da_biblioteca", x["modelo"]) == x["modelo"] else f" do `{x['dono_da_biblioteca']}`"
        return f"`{x['corrida']}`, `{x['modelo']}`, L{x['biblioteca_epoca']}{dono}"

    def n(c: dict, k: str) -> str:
        return str(c.get(k, 0))

    blocos = [
        a3b.tab("tb_rac_corridas", ["Trilha (corrida, modelo, biblioteca)", "Diagnósticos", "Sem raciocínio antes das quatro linhas", "Prompt inteiro provado",
                                    "Só a documentação provada", "Não comprovado", "Acerto quando algum verbete do contexto trata da causa respondida",
                                    "Acerto quando nenhum trata"],
                [[nome(x), str(x["diagnosticos"]), str(x["sem_raciocinio_antes_das_linhas"]), n(x["prova_do_prompt"], "prompt_inteiro"), n(x["prova_do_prompt"], "contexto"),
                  n(x["prova_do_prompt"], "nao_comprovado"),
                  f'{f(x["acerto_por_sustentacao"]["sustentado"]["acerto_pct"])}% ({x["acerto_por_sustentacao"]["sustentado"]["acertos"]} de {x["acerto_por_sustentacao"]["sustentado"]["n"]})',
                  f'{f(x["acerto_por_sustentacao"]["nao_sustentado"]["acerto_pct"])}% ({x["acerto_por_sustentacao"]["nao_sustentado"]["acertos"]} de {x["acerto_por_sustentacao"]["nao_sustentado"]["n"]})']
                 for x in cs]),
        a3b.tab("tb_rac_conferencias", ["Trilha", "Conferência (sem usar o gabarito)", "Confere", "Não confere", "Não se aplica", "Não verificável ou informativo"],
                [[nome(x), ROTULO_DA_REGRA[c["regra"]], n(c, "confere"), n(c, "nao_confere"), n(c, "nao_se_aplica"), str(c.get("nao_verificavel", 0) + c.get("informativo", 0))]
                 for x in cs for c in x["conferencias"]]),
        a3b.tab("tb_rac_avaliacao", ["Trilha", "Pergunta (com o gabarito)", "Confere", "Não confere"],
                [[nome(x), ROTULO_DA_REGRA[r], n(c, "confere"), n(c, "nao_confere")] for x in cs for r, c in x["avaliacao"].items()]),
    ]
    cab = pf.cabecalho("Indicadores do relatório de raciocínio", "gerar_relatorio_raciocinio.py", "trilhas remontadas das corridas gravadas", dado["metadados"]["gerado_em"][:10])
    cab += ["", "Cada linha conta os eventos da trilha de uma corrida. As conferências da segunda tabela não usam o gabarito: são as que o agente poderá fazer "
                "sozinho na Fase 4. A frase de impacto e a nota exata que o modelo usou dentro de um verbete não têm como ser conferidas por código, e a tabela diz isso.", ""]
    return "\n".join(cab) + "\n\n" + "\n\n".join(blocos) + "\n"


# ------------------------------------------------------------------ linha de comando

def _outras_versoes(corrida: str, modelo: str, caso: str) -> list[dict]:
    """O mesmo caso nas versões da biblioteca que a corrida gravou (lido dos registros, não das trilhas)."""
    pasta = caminhos.fase3(corrida)["raiz"] / executar_fase3._slug(modelo)
    saida = []
    for arq in sorted(pasta.glob("diagnosticos__L*.jsonl")):
        for r in tr._jsonl(arq):
            if r["caso"] == caso:
                saida.append({"versao": r["biblioteca_epoca"], "causa": avaliar.extrair(r["resposta"])["causa_raiz"], "verbetes": r["verbetes_ids"]})
    return saida


def _destino(corrida: str, modelo: str, versao: int) -> Path:
    return tr.pasta_derivados() / "relatorios" / f"{corrida}__{executar_fase3._slug(modelo)}__L{versao}"


def gerar_vitrine(gravar: bool) -> tuple[list[tuple[str, str, int, list[dict]]], dict[Path, str]]:
    """Remonta as trilhas da vitrine e os relatórios dos casos dela. Devolve as trilhas e {arquivo: texto}; com
    gravar=True grava as trilhas em pre_fase4/trilhas/ e os relatórios em pre_fase4/relatorios/."""
    trilhas, arquivos = [], {}
    for corrida, modelo, versao, particao in VITRINE:
        t = tr.adaptar_corrida(corrida, modelo, versao)
        slug = executar_fase3._slug(modelo)
        arq_trilha = tr.pasta_derivados() / "trilhas" / f"{corrida}__{slug}__L{versao}.jsonl"
        if gravar:
            t.gravar(arq_trilha)
        trilhas.append((corrida, modelo, versao, t.eventos))
        pasta = _destino(corrida, modelo, versao)
        linhas_indice = []
        for tid, seq in tr.por_trilha(t.eventos).items():
            if "@" not in tid:
                continue
            entrada = next(e["dados"] for e in seq if e["tipo"] == "entrada")
            if particao and entrada.get("particao") != particao:
                continue
            caso = entrada["caso"]
            arquivos[pasta / f"{caso}.md"] = relatorio_do_caso(t.eventos, tid, _outras_versoes(corrida, modelo, caso), arq_trilha.name)
            ver = [e["dados"] for e in seq if e["tipo"] == "verificacao"]
            causa = next((e["dados"].get("lido") for e in seq if e["tipo"] == "declaracao" and e["dados"]["campo"] == "causa_raiz"), None)
            certo = next((v["resultado"] for v in ver if v["regra"] == "causa_correta"), "")
            falhas = [FRASE_DA_FALHA.get(v["regra"], v["regra"]) for v in ver if not v["usa_gabarito"] and v["resultado"] == "nao_confere"]
            linhas_indice.append([f"[`{caso}`]({caso}.md)", str(entrada["classe"]), str(entrada["nivel"]), f"`{_cel(causa)}`",
                                  "sim" if certo == "confere" else "**não**", "; ".join(falhas) or "nada"])
        indice = "\n".join([
            "<!-- ! Alteração de IA - Revisar: índice DERIVADO, gerado por gerar_relatorio_raciocinio.py --vitrine; não editar à mão.",
            "     ! Motivo: um relatório por caso é ilegível sem uma lista que diga em quais vale a pena entrar; a última coluna aponta os casos em que alguma conferência não confere. -->",
            f"# Relatórios de raciocínio: `{corrida}`, `{modelo}`, biblioteca L{versao}", "",
            f"{len(linhas_indice)} casos" + (f" da partição de {particao}" if particao else "") + f". Trilha bruta: `../../trilhas/{arq_trilha.name}`.", "",
            _tabela(["Caso", "Classe", "Nível", "Causa respondida", "Acertou", "O que não confere (sem usar o gabarito)"], linhas_indice), ""])
        arquivos[pasta / "INDICE.md"] = indice
    if gravar:
        for arq, texto in arquivos.items():
            arq.parent.mkdir(parents=True, exist_ok=True)
            arq.write_text(texto, encoding="utf-8", newline="\n")
    return trilhas, arquivos


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--vitrine", action="store_true", help="gera as trilhas, os relatórios e os indicadores da vitrine")
    ap.add_argument("--check", action="store_true", help="com --vitrine: regera e compara com o que está gravado")
    ap.add_argument("--colar", action="store_true", help="com --vitrine: cola os blocos tb_rac_* no relatório da Pré-Fase 4")
    ap.add_argument("--corrida")
    ap.add_argument("--modelo", default="qwen2.5:7b")
    ap.add_argument("--versao", type=int, default=1)
    ap.add_argument("--caso")
    args = ap.parse_args()
    print(caminhos.descricao())
    if args.vitrine:
        trilhas, arquivos = gerar_vitrine(gravar=not (args.check or args.colar))
        dado = montar(trilhas)
        codigo = pf.fechar(NOME, dado, render(dado), PREFIXO, check=args.check, colar=args.colar)
        if args.check:
            diferentes = [a for a, texto in arquivos.items() if not a.exists() or a.read_text(encoding="utf-8") != texto]
            trilhas_dif = [f"{c}__{executar_fase3._slug(m)}__L{v}.jsonl" for c, m, v, ev in trilhas
                           if not (tr.pasta_derivados() / "trilhas" / f"{c}__{executar_fase3._slug(m)}__L{v}.jsonl").exists()
                           or tr.ler(tr.pasta_derivados() / "trilhas" / f"{c}__{executar_fase3._slug(m)}__L{v}.jsonl") != json.loads(json.dumps(ev, ensure_ascii=False))]
            if diferentes or trilhas_dif:
                print(f"--check: DIFERE ({len(diferentes)} relatório(s) e {len(trilhas_dif)} trilha(s) fora de dia: {[a.name for a in diferentes][:5]} {trilhas_dif})")
                return 1
            print(f"--check: {len(arquivos)} relatórios e {len(trilhas)} trilhas batem com os registros")
        elif not args.colar:
            print(f"gravado: {len(trilhas)} trilhas, {len(arquivos)} arquivos de relatório em {tr.pasta_derivados() / 'relatorios'}")
        return codigo
    if not (args.corrida and args.caso):
        ap.error("informe --vitrine ou --corrida e --caso")
    t = tr.adaptar_corrida(args.corrida, args.modelo, args.versao)
    tid = f"{args.corrida}/{executar_fase3._slug(args.modelo)}/{args.caso}@L{args.versao}"
    destino = _destino(args.corrida, args.modelo, args.versao) / f"{args.caso}.md"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(relatorio_do_caso(t.eventos, tid, _outras_versoes(args.corrida, args.modelo, args.caso)), encoding="utf-8", newline="\n")
    print(f"gravado: {destino}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
