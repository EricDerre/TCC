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

# ! Alteração de IA - Revisar: (07/11/2026, Pós-Fase 4, Q1) a camada de leitura dos verbetes e a taxonomia entram para o relatório v3.
# ! Motivo: o v3 cita os verbetes pela camada de leitura (decisão 103) e escreve classe e nível do caso com o significado ao lado.
import biblioteca_leitura as bl
import caminhos
import executar_fase3
import pre_fase4 as pf
import taxonomia
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


# ! Alteração de IA - Revisar: (05/11/2026, sessão de revisão) `_cod`: valor declarado pelo modelo entre crases, com as crases que ele escreveu trocadas por aspas simples.
# ! Motivo: numa frase de impacto com crases, o trecho de código do relatório quebrava no meio (na linha IMPACTO da seção 1 e na linha da árvore).
def _cod(valor) -> str:
    return "`" + _cel(valor).replace("`", "'") + "`"


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
    """Só os verbetes que a evidência do nó aponta pelo id, cada um uma vez: é tudo o que o molde pode citar.
    ! Alteração de IA - Revisar: (27/10/2026, P3) o mesmo id não entra duas vezes.
    ! Motivo: no diagnóstico ao vivo o verbete citado na FONTE também foi entregue pela busca e aparece na evidência
    com os dois papéis; a fumaça da corrida 18 mostrou a justificativa listando os três verbetes duas vezes."""
    vistos: list[str] = []
    for e in no.get("evidencia") or []:
        if e.get("id") and e.get("papel") in PAPEIS_COM_VERBETE and e["id"] not in vistos:
            vistos.append(e["id"])
    return vistos


def _ids_entregues(no: dict) -> list[str]:
    """Só os verbetes que a busca entregou (papel `verbete_entregue`): um verbete citado na FONTE fora do contexto
    não pode aparecer como entregue (a frase da FONTE é que diz que ele ficou fora)."""
    vistos: list[str] = []
    for e in no.get("evidencia") or []:
        if e.get("id") and e.get("papel") == "verbete_entregue" and e["id"] not in vistos:
            vistos.append(e["id"])
    return vistos


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
    if no.get("escolha") is None:
        return "sem rótulo: a resposta não tem a linha CAUSA_RAIZ, nenhuma causa a contrastar"
    if segunda is None:
        return f"{no['escolha']} sem alternativa registrada no nó"
    ids = _ids_da_evidencia(no)
    texto = (f"{no['escolha']} e não {segunda['opcao']}: a escolha tem probabilidade {_prob(_escore_da_escolha(no))} "
             f"contra {_prob(segunda.get('escore'))}")
    return texto + (f"; verbete(s) na evidência: {', '.join(ids)}" if ids else "; nenhum verbete entregue na evidência")


def _campo_e_sinal(no: dict, por_seq: dict[int, dict]) -> tuple[str | None, str | None, str | None]:
    """O campo, o sinal em código que a evidência aponta (evento de poda com o diff contra o contrato, ou o campo
    declarado na trilha) e onde o sinal está (na resposta HTTP ou na tela); sem eventos, só o que o nó trouxer em `campo`.
    ! Alteração de IA - Revisar: (27/10/2026, P3) a poda da árvore (alvo `arvore`) nunca dá o campo (o diff dela diz
    "arvore") e o sinal dela é dito como presente na tela, não na resposta HTTP; diff sem campo (corpo truncado,
    vazio ou não JSON) vira só "esperado X, recebido Y".
    ! Motivo: na fumaça da corrida 18 a justificativa dizia que "o sinal arvore: esperado 22 linha(s) ... está presente
    na resposta HTTP", porque o único diff do caso era o da árvore; o molde só pode dizer o que o evento mede."""
    campo, sinal, onde = no.get("campo"), None, None
    tid = None
    for e in no.get("evidencia") or []:
        ev = por_seq.get(e["seq"])
        if ev is None:
            continue
        tid = tid or ev.get("trilha")
        if ev["tipo"] == "poda" and ev["dados"].get("diff"):
            d = ev["dados"]["diff"][0]
            da_arvore = ev["dados"].get("alvo") == "arvore"
            if not da_arvore:
                campo = campo or d.get("campo")
            if sinal is None:
                sinal = (f"{d['campo']}: " if d.get("campo") else "") + f"esperado {d.get('esperado')}, recebido {d.get('recebido')}"
                onde = "na tela" if da_arvore else "na resposta HTTP"
        elif e.get("papel") == "sinal_em_codigo" and ev["dados"].get("sinal"):
            sinal = sinal or str(ev["dados"]["sinal"])
            onde = onde or "no caso"
    if campo is None and tid is not None:
        for ev in por_seq.values():
            if ev.get("trilha") == tid and ev["tipo"] == "declaracao" and ev["dados"].get("campo") == "campo" and ev["dados"].get("lido"):
                lido = str(ev["dados"]["lido"])
                # "CAMPO: nenhum" é a resposta prevista pelo prompt quando não há campo: não vira "no campo nenhum"
                if "nenhum" not in lido.lower():
                    campo = lido
                break
    return campo, sinal, onde


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
    campo, sinal, onde = _campo_e_sinal(no, por_seq)
    ids = _ids_entregues(no)
    partes = []
    # ! Alteração de IA - Revisar: (27/10/2026, P3, revisão) sem rótulo a frase diz que a linha CAUSA_RAIZ não veio, e a
    # frase dos entregues cita só os verbetes que a busca entregou (papel verbete_entregue).
    # ! Motivo: o revisor do P3 reproduziu "O agente respondeu None" numa resposta sem a linha, e um verbete citado na
    # FONTE fora do contexto saindo como "entregue" na mesma justificativa que o dizia fora do contexto.
    base = (f"O agente respondeu {escolha}" + (f" no campo {campo}" if campo else "")) if escolha is not None \
        else "O agente não escreveu a linha CAUSA_RAIZ (nenhuma causa respondida)"
    motivos = []
    if sinal:
        motivos.append(f"o sinal {sinal} está presente {onde or 'na resposta HTTP'}")
    if ids:
        motivos.append(f"o verbete {ids[0]} estava entre os entregues ao modelo" if len(ids) == 1
                       else f"os verbetes {', '.join(ids)} estavam entre os entregues ao modelo")
    if escolha is None:
        partes.append(base + ("; " + " e ".join(motivos) if motivos else "") + ".")
    else:
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
    # ! Alteração de IA - Revisar: (27/10/2026, P3) a frase da intervenção passa a dizer o tipo dela (remoção, troca por
    # verbete errado, inferência sem documentação, repetição da inferência de base) e marca quando a probabilidade
    # registrada é só um limite inferior; sem `tipo` a frase continua a da remoção, byte a byte.
    # ! Motivo: diagnostico_ao_vivo.py roda as quatro intervenções da especificação (6.1) e passa todas ao molde; com a
    # frase única, "a remoção do verbete None" apareceria para a inferência sem documentação e para a repetição.
    for i in intervencoes:
        v = i.get("verbete")
        tipo = i.get("tipo") or "remocao"
        if i.get("rotulo_antes") is None:
            partes.append(f"A intervenção {tipo} não teve rótulo de base para comparar.")
            continue
        sujeito = {"remocao": f"A remoção do verbete {v}", "troca": f"A troca do verbete {v} por um verbete errado",
                   "sem_documentacao": "A inferência sem documentação",
                   "repeticao_da_base": "A repetição da inferência de base"}.get(tipo, f"A intervenção {tipo}")
        limite = " (a probabilidade registrada é só um limite inferior: o rótulo saiu das alternativas devolvidas)" if i.get("limite_inferior") else ""
        if i.get("mudou_rotulo"):
            partes.append(f"{sujeito} mudou a resposta (de {i.get('rotulo_antes')} para {i.get('rotulo_depois')})"
                          + (", então ele pesou na decisão." if tipo == "remocao" else ".") + limite)
        else:
            partes.append(f"{sujeito} não mudou a resposta" + (": sem efeito medido do contexto." if tipo in ("remocao", "troca") else ".") + limite)
    if any(v.get("regra") == "impacto" and v.get("resultado") == "nao_verificavel" for v in verificacoes):
        partes.append("O que não dá para conferir por código: a frase de impacto.")
    d = no.get("divergencia") or {}
    if d.get("ha"):
        partes.append("O que o modelo declarou diverge do que o código mediu"
                      + (f" (entre {' e '.join(d['entre'])})" if d.get("entre") else "") + (f": {d['detalhe']}." if d.get("detalhe") else "."))
    if no.get("falha"):
        partes.append(f"Este nó está marcado com a falha {no['falha']} (origem: {tr.origem_da_falha(no['falha'])}).")
    if no.get("intervencoes_puladas"):
        partes.append(f"As intervenções não rodaram: {no['intervencoes_puladas']}.")
    incerteza = frase_de_incerteza(no, campo)
    if incerteza:
        partes.append(incerteza)
    return " ".join(partes)


# ! Alteração de IA - Revisar: (01/11/2026, Fase 4, pacote P4) o molde da justificativa da cura de seletor, escrito em
# código a partir do evento `cura` da trilha (cura_seletor.evento_de_cura): o passo que falhou, quantos candidatos foram
# gerados, quantos passaram as quatro verificações estáticas, qual levou o roteiro ao fim e se é o mesmo elemento da
# referência; sem cura, diz a falha da taxonomia e os candidatos recusados na reexecução.
# ! Motivo: o nó `cura` leva a justificativa como o nó `diagnostico` (especificação, seção 7), e ela precisa sair de dados
# medidos, nunca de texto livre; o relatório marca "gerada por molde" ao apresentá-la.
ROTULO_DA_VERIFICACAO_DA_CURA = {"resolve_um_elemento": "um elemento", "visivel_e_habilitado": "visível e habilitado", "mesmo_papel": "mesmo papel",
                                 "nome_parecido": "nome parecido", "efeito_na_reexecucao": "efeito na reexecução"}


def justificativa_da_cura(cura: dict) -> str:
    cands = cura.get("candidatos") or []
    gerados = [c for c in cands if c.get("gerado")]
    estaticos = [c for c in gerados if c.get("passou_estaticas")]
    recusados = [c for c in gerados if c.get("reexecutado") and not c.get("aplicado")]
    ap = cura.get("aplicado") or {}
    partes = [f"O passo {cura.get('passo')} ({cura.get('localizador')}) falhou: {_cel(cura.get('erro') or 'o localizador não resolveu')}."]
    partes.append(f"Dos {len(cands)} candidatos previstos, {len(gerados)} foram gerados da árvore podada e do alvo da referência; "
                  f"{len(estaticos)} passaram as quatro verificações em código (um elemento só, visível e habilitado, mesmo papel, nome parecido acima de "
                  f"{cura.get('limiar_nome')}).")
    if cura.get("curado") and ap:
        frase = f"O primeiro que passou, `{ap.get('estrategia')}` ({ap.get('seletor')}), levou o roteiro ao fim na reexecução"
        mesmo = cura.get("mesmo_elemento")
        frase += (" e resolve o mesmo elemento da referência." if mesmo else (", mas resolve outro elemento, não o alvo da referência." if mesmo is False
                                                                              else "; a impressão do elemento não foi comparada."))
        partes.append(frase)
        if recusados:
            partes.append("Antes dele, " + "; ".join(f"`{c['estrategia']}` foi recusado na reexecução ({_cel((c.get('efeito') or {}).get('detalhe'))})" for c in recusados) + ".")
    else:
        if recusados:
            partes.append("Nenhum levou o roteiro ao fim: " + "; ".join(f"`{c['estrategia']}` ({_cel((c.get('efeito') or {}).get('detalhe'))})" for c in recusados)
                          + f". Falha registrada: {cura.get('falha')}.")
        else:
            partes.append(f"Nenhum chegou à reexecução. Falha registrada: {cura.get('falha')}.")
    if cura.get("mttr_s") is not None:
        partes.append(f"Da detecção à reexecução validada: {_num(cura.get('mttr_s'), 1)} s.")
    return " ".join(partes)


def _resumo_do_evento(e: dict, blobs: dict) -> str:
    d = e["dados"]
    tipo = e["tipo"]
    if tipo == "decisao":
        return f"{d.get('decisao')}: escolha {d.get('escolha')}; divergência {'sim' if (d.get('divergencia') or {}).get('ha') else 'não'}"
    if tipo == "declaracao":
        return f"{d.get('campo')}: " + ("ausente" if d.get("ausente") else _cod(d.get('valor')))
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
    if tipo == "cura":
        ap = d.get("aplicado") or {}
        return (f"{'curado' if d.get('curado') else 'não curado'}: {len(d.get('candidatos') or [])} candidatos, {d.get('reexecucoes', 0)} reexecução(ões)"
                + (f"; aplicado {ap.get('estrategia')}" if ap else "") + (f"; MTTR {_num(d.get('mttr_s'), 1)} s" if d.get("mttr_s") is not None else ""))
    if tipo == "edicao_biblioteca":
        # ! Alteração de IA - Revisar: (03/11/2026, P5) o resumo do evento de edição da biblioteca: a proposta (número, operação,
        # verbete e o que aconteceu com ela) ou a correção (verbete e estado).
        # ! Motivo: o genérico de antes só despejava os campos escalares em JSON; a árvore da trilha precisa dizer em uma
        # linha se a edição entrou, ficou para revisão ou foi recusada e por qual código.
        if d.get("etapa") == "correcao":
            return f"correção de [{d.get('verbete')}] pelo caso {d.get('caso')}: {d.get('estado_antes')} para {d.get('estado_depois')}"
        estado = "aplicada" if d.get("aplicada") else ("para revisão humana" if d.get("para_revisao") else f"recusada: {d.get('codigo')}")
        return f"proposta {d.get('numero')}: {d.get('operacao')} em [{d.get('verbete')}]: {estado}"
    if tipo in ("acao", "incidente", "revisao", "prompt"):
        return _cel(json.dumps({k: v for k, v in d.items() if not isinstance(v, (dict, list))}, ensure_ascii=False))[:160]
    return ""


_EFEITO_DA_INTERVENCAO = {"remocao": ("mudou a resposta: o verbete pesou na decisão", "sem efeito medido do contexto"),
                          "troca": ("mudou a resposta: o verbete errado pesou na decisão", "sem efeito medido do contexto"),
                          "sem_documentacao": ("sem documentação a resposta muda: a documentação pesou na decisão", "sem documentação a resposta fica a mesma"),
                          "repeticao_da_base": ("a resposta mudou com o mesmo prompt: variação natural", "o mesmo prompt manteve o rótulo")}


def _efeito_da_intervencao(i: dict) -> str:
    """O que a intervenção mediu, pelo tipo dela; um tipo desconhecido cai na frase da remoção (a forma da trilha da Pré-Fase 4)."""
    mudou, manteve = _EFEITO_DA_INTERVENCAO.get(i.get("tipo") or "remocao", _EFEITO_DA_INTERVENCAO["remocao"])
    return mudou if i.get("mudou_rotulo") else manteve


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
    # ! Alteração de IA - Revisar: (01/11/2026, P4) a trilha de uma execução da cura de seletor (sem modelo) tem o evento
    # `cura` e os nós `cura` e `reexecucao` no lugar do diagnóstico: o veredito diz a cura, a evidência lista todos os
    # candidatos com o resultado de cada verificação, o contraste é o do nó `cura` e a linha de ação traz a sugestão de
    # localizador (o agente não altera a aplicação).
    # ! Motivo: plano aprovado, seção 3.6 ("o relatório mostra todos os candidatos com o resultado de cada verificação")
    # e seção 3.2 ("apresenta como sugestão no relatório"); sem isso o relatório da corrida 19 diria "nenhum nó de
    # diagnóstico" e esconderia a cura.
    no_cura = next((e["dados"] for e in reversed(nos) if e["dados"].get("decisao") == "cura"), None)
    cura = (por_tipo.get("cura") or [{"dados": None}])[-1]["dados"]
    intervencoes = [e["dados"] for e in por_tipo.get("intervencao", [])]
    # ! Alteração de IA - Revisar: (03/11/2026, P5) a trilha de um caso de aprendizado da corrida 20 tem, depois do diagnóstico,
    # a inferência de proposta, um evento `edicao_biblioteca` por bloco e o nó `edicao_biblioteca`; a de um caso do ciclo de
    # correção tem o evento e o nó com a operação `correcao`. O veredito ganha a linha "Biblioteca" e a evidência a tabela das
    # propostas com o veredito da Fase 3, o filtro do P5 e o resultado.
    # ! Motivo: plano aprovado, seção 3.7 e 3.8: o relatório por caso mostra o que entrou na biblioteca e o que o código
    # recusou; sem isso a corrida 20 ficaria com a decisão de edição só na árvore de eventos.
    nos_bib = [e["dados"] for e in nos if e["dados"].get("decisao") == "edicao_biblioteca"]
    edicoes = [e["dados"] for e in por_tipo.get("edicao_biblioteca", [])]
    podas = [e for e in por_tipo.get("poda", [])]
    interceptacoes = [e for e in por_tipo.get("interceptacao", [])]
    caso = entrada.get("caso", tid)

    def valor(chave: str) -> str:
        d = decl.get(chave)
        if d is None or d.get("ausente"):
            return "**a linha não está na resposta**"
        return _cod(d.get('valor'))

    confianca = (diag or {}).get("confianca") or {}
    selo = confianca.get("selo") or "sem selo"
    divergencia = (diag or {}).get("divergencia") or {}
    veredito = [f"**CAUSA_RAIZ:** {valor('causa_raiz')} · **CAMPO:** {valor('campo')} · selo de probabilidade: **{selo}**"
                + (f" (p = {_prob(confianca.get('p_rotulo'))})" if confianca.get("p_rotulo") is not None else "")
                + (f" · **CONFLITO**: {_cel(divergencia.get('detalhe') or 'o declarado diverge do medido')}" if divergencia.get("ha") else ""),
                "", f"**IMPACTO (declarado):** {valor('impacto')}", ""]
    if diag is not None:
        veredito += [f"Justificativa ({MARCA_DO_MOLDE}): {diag.get('justificativa') or justificativa_por_molde(diag, eventos, sem_gabarito, intervencoes)}", ""]
    elif cura is not None:
        ap = cura.get("aplicado") or {}
        mesmo = cura.get("mesmo_elemento")
        if cura.get("curado"):
            veredito = [f"**Cura de seletor:** aplicada: `{ap.get('estrategia')}` (`{_cel(ap.get('seletor'))}`) · reexecução validada · "
                        + ("mesmo elemento da referência: sim" if mesmo else ("**outro elemento** fez o roteiro passar (regra R3)" if mesmo is False else "mesmo elemento: não comparado")), ""]
        else:
            veredito = [f"**Cura de seletor:** não curado · falha: `{_cel(cura.get('falha'))}` · {cura.get('reexecucoes', 0)} reexecução(ões) sem levar o roteiro ao fim", ""]
        veredito += [f"Passo {cura.get('passo')} do roteiro, localizador `{_cel(cura.get('localizador'))}`: {_cel(cura.get('erro') or 'o localizador não resolveu')}", ""]
        if cura.get("mttr_s") is not None:
            veredito += [f"Da detecção à reexecução validada: {_num(cura.get('mttr_s'), 1)} s (detecção {_cel(cura.get('deteccao'))}; validação {_cel(cura.get('validacao'))}).", ""]
        veredito += [f"Justificativa ({MARCA_DO_MOLDE}): {(no_cura or {}).get('justificativa') or justificativa_da_cura(cura)}", ""]
    else:
        veredito += ["Nenhum nó de decisão de diagnóstico nesta trilha.", ""]
    for no_bib in nos_bib:
        if no_bib.get("operacao") == "correcao":
            estados = no_bib.get("estados") or {}
            veredito += [f"**Biblioteca (ciclo de correção):** {'corrigido' if no_bib.get('escolha') == 'corrigido' else 'não corrigido'}: "
                         + (", ".join(f"[{v}] {a} para {b}" for v, (a, b) in ((k, tuple(x)) for k, x in estados.items())) or "nenhum verbete mudou de estado") + ".", ""]
        else:
            aplicadas = no_bib.get("aplicadas") or []
            seguradas = no_bib.get("para_revisao") or []
            recusadas = no_bib.get("recusadas") or []
            veredito += [f"**Biblioteca:** {len(aplicadas)} edição(ões) aplicada(s)" + (f" ({', '.join(f'[{v}]' for v in aplicadas)})" if aplicadas else "")
                         + f", {len(seguradas)} para revisão humana" + (f" ({', '.join(f'[{v}]' for v in seguradas)})" if seguradas else "")
                         + f", {len(recusadas)} recusada(s)" + (f" ({', '.join(str(r.get('codigo')) for r in recusadas)})" if recusadas else "")
                         + (f" · falha: `{no_bib.get('falha')}`" if no_bib.get("falha") else "") + ".", ""]
        veredito += [f"Justificativa ({MARCA_DO_MOLDE}): {no_bib.get('justificativa') or ''}", ""]

    evidencia = []
    propostas_bib = [d for d in edicoes if d.get("etapa") == "proposta"]
    if propostas_bib:
        evidencia += ["Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):", "",
                      _tabela(["Proposta", "Operação", "Verbete", "Validador da Fase 3", "Filtro do P5", "Resultado", "Peso"],
                              [[str(d.get("numero")), _cel(d.get("operacao")), f"`{_cel(d.get('verbete'))}`",
                                "aceita" if (d.get("veredito_fase3") or {}).get("aceita") else f"recusada: `{_cel((d.get('veredito_fase3') or {}).get('motivo'))}`",
                                _cel(d.get("filtro") or "nenhum"),
                                "**aplicada**" if d.get("aplicada") else ("para revisão humana" if d.get("para_revisao") else f"recusada: `{_cel(d.get('codigo'))}`"),
                                _cel(d.get("peso"))] for d in propostas_bib]), ""]
    correcoes_bib = [d for d in edicoes if d.get("etapa") == "correcao"]
    for d in correcoes_bib:
        ev = d.get("evidencia") or {}
        evidencia += [f"Ciclo de correção do verbete [{_cel(d.get('verbete'))}] pelo caso {_cel(d.get('caso'))}: estado {_cel(d.get('estado_antes'))} para {_cel(d.get('estado_depois'))}; "
                      f"evidência: reexecução {'passou' if ev.get('passou_depois') else 'falhou'}, fio {'mudou' if ev.get('ha_diff_http') else 'igual'}, "
                      f"árvore {'mudou' if ev.get('ha_diff_arvore') else 'igual'}.", ""]
    if cura is not None:
        alvo = cura.get("alvo") or {}
        evidencia += [f"Alvo registrado na corrida de referência: {_cel(alvo.get('papel'))} \"{_cel(alvo.get('nome'))}\" (ocorrência {alvo.get('ocorrencia')}; "
                      f"tag `{_cel(alvo.get('tag'))}`; caminho `{_cel(alvo.get('caminho'))}`; atributos "
                      f"{_cel(json.dumps({k: v for k, v in (alvo.get('atributos') or {}).items() if v}, ensure_ascii=False))}).", "",
                      f"Candidatos na ordem fixa (limiar do nome {cura.get('limiar_nome')}); verificações na ordem fixa:", ""]
        linhas_c = []
        for c in cura.get("candidatos") or []:
            v = c.get("verificacoes") or {}
            if not c.get("gerado"):
                linhas_c.append([f"`{c['estrategia']}`", f"não gerado: {_cel(c.get('motivo'))}"] + ["não se aplica"] * 5 + [""])
                continue
            celulas = []
            for chave in ROTULO_DA_VERIFICACAO_DA_CURA:
                r = (v.get(chave) or {}).get("resultado")
                rot = {"confere": "confere", "nao_confere": "**não confere**", "nao_se_aplica": "não se aplica", "nao_tentado": "não tentado"}.get(r, _cel(r))
                det = (v.get(chave) or {}).get("detalhe")
                celulas.append(rot + (f" ({_cel(det)})" if det and r in ("nao_confere", "confere") and chave in ("nome_parecido", "efeito_na_reexecucao") else ""))
            linhas_c.append([f"`{c['estrategia']}`", f"`{_cel(c.get('seletor'))}`"] + celulas + ["**sim**" if c.get("aplicado") else ""])
        evidencia += [_tabela(["Estratégia", "Seletor"] + list(ROTULO_DA_VERIFICACAO_DA_CURA.values()) + ["Aplicado"], linhas_c), ""]
    if podas:
        for e in podas:
            d = e["dados"]
            # ! Alteração de IA - Revisar: (05/11/2026, sessão de revisão) a linha do corpo que não é JSON sai com o nome "(corpo inteiro)" na coluna do campo.
            # ! Motivo: essa linha não tem campo (avaliacao_trilha.linhas_diff_do_contrato) e a primeira coluna saía vazia, sem dizer do que a linha falava.
            # ! Alteração de IA - Revisar: (05/11/2026, ficha 41) quando a diferença só aparece a partir do segundo item, a coluna do campo diz o item.
            # ! Motivo: a poda passou a olhar todos os itens da lista; sem o item, a tabela afirmaria que o campo falta na lista inteira.
            linhas = [[_cel((x.get("campo") or "(corpo inteiro)") + (f" (item {x['item']})" if x.get("item") else "")), _cel(x.get("esperado")), _cel(x.get("recebido"))] for x in d.get("diff") or []]
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
    # ! Alteração de IA - Revisar: (05/11/2026, leitura da corrida 22) um caso lido em texto mostra sempre como foi ao prompt: sem poda, como
    # antes; com poda (os casos da corrida 22), antes dela, no começo da seção.
    # ! Motivo: o texto só saía quando a trilha não tinha poda, e o P7 passou a emitir poda nos casos de texto; os 11 relatórios da amostra da
    # corrida 22 ficaram sem o sintoma, a requisição e o contrato, e quem revisa não teria como julgar o diagnóstico.
    texto_caso = blobs.get(entrada.get("texto")) if entrada.get("texto") else None
    if not podas and not interceptacoes and cura is None:
        evidencia += ["Não houve interceptação nem poda nesta trilha: o caso entrou em texto." + ("" if texto_caso is None else " Como foi posto no prompt:"), ""]
        if texto_caso is not None:
            evidencia += [_bloco(texto_caso), ""]
    elif texto_caso is not None:
        evidencia = ["O caso, como foi posto no prompt:", "", _bloco(texto_caso), ""] + evidencia

    contraste = []
    no_principal = diag if diag is not None else no_cura
    if no_principal is not None:
        contraste += [no_principal.get("contraste") or (contraste_por_molde(diag) if diag is not None else ""), ""]
        alternativas = sorted(no_principal.get("alternativas") or [], key=lambda a: -(a.get("escore") if isinstance(a.get("escore"), (int, float)) else -1))
        if alternativas:
            contraste += [_tabela(["Alternativa", "Probabilidade ou escore", "Escolhida"],
                                  [[_cel(a.get("opcao")), _prob(a.get("escore")) if diag is not None else f"{a.get('escore')} de 5 verificações",
                                    "sim" if a.get("opcao") == no_principal.get("escolha") else ""] for a in alternativas]), ""]
    else:
        contraste += ["Sem nó de diagnóstico, não há contraste.", ""]

    if cura is not None and diag is None:
        fonte = ["Não se aplica: a cura de seletor roda sem modelo; nenhum verbete foi citado.", ""]
    else:
        fonte = [f"Linha FONTE como veio: {valor('fonte')}; verbetes citados: " + (", ".join(_cod(c.get('valor')) for c in citadas) or "nenhum") + ".", ""]
    conf_fonte = [v for v in sem_gabarito if str(v.get("regra", "")).startswith("fonte_") or v.get("regra") == "rotulo_sustentado_por_verbete_do_contexto"]
    if conf_fonte:
        fonte += [_tabela(["Conferência", "Sobre", "Resultado", "Evidência"],
                          [[ROTULO_DA_REGRA.get(v["regra"], v["regra"]), f"`{_cel(v['alvo'])}`" if v.get("alvo") else "",
                            ROTULO_DO_RESULTADO.get(v["resultado"], v["resultado"]), _evidencia(v)] for v in conf_fonte]), ""]
    if cura is not None and diag is None:
        pass
    elif intervencoes:
        # ! Alteração de IA - Revisar: (05/11/2026, leitura da corrida 22) o Efeito sai por tipo de intervenção (_efeito_da_intervencao) e a célula do
        # verbete diz "não se aplica" onde a intervenção não tem verbete.
        # ! Motivo: a tabela dizia "o verbete pesou na decisão" na inferência sem documentação, que não tem verbete, e "sem efeito medido do contexto" na
        # repetição da base; quem revisa lê essa coluna, e o molde promete não afirmar mais do que foi medido (especificação, seção 7).
        fonte += [_tabela(["Intervenção", "Verbete", "Rótulo antes", "Rótulo depois", "p antes", "p depois", "Efeito"],
                          [[_cel(i.get("tipo")), f"`{_cel(i.get('verbete'))}`" if i.get("verbete") else "não se aplica", _cel(i.get("rotulo_antes")), _cel(i.get("rotulo_depois")),
                            _prob(i.get("p_antes")), _prob(i.get("p_depois")), _efeito_da_intervencao(i)
                            + (" (só um limite inferior da queda: o rótulo saiu das alternativas devolvidas)" if i.get("limite_inferior") else "")]
                           for i in intervencoes]), ""]
    else:
        fonte += ["Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.", ""]

    campo_decl = (decl.get("campo") or {}).get("lido")
    onde = next((f"`{e['dados'].get('metodo')} {e['dados'].get('caminho')}`" for e in interceptacoes), None)
    # ! Alteração de IA - Revisar: (04/11/2026, leitura da corrida 21) a linha de ação da cura vale sempre que a trilha tem o evento `cura`,
    # mesmo com diagnóstico, e o campo declarado "nenhum" não vira "Confira o campo `nenhum`".
    # ! Motivo: os casos de localizador da Fase 5 têm diagnóstico e cura; o relatório exigia não haver diagnóstico e mandava conferir o
    # campo `nenhum` contra o contrato numa página sem contrato. Nos cenários de contrato sem campo (malformed_json, error_500) a frase
    # também não fazia sentido.
    if str(campo_decl or "").strip().lower() == "nenhum":
        campo_decl = None
    if cura is not None:
        ap = cura.get("aplicado") or {}
        if cura.get("curado"):
            acao = [f"Sugestão (o agente não altera a aplicação): no passo {cura.get('passo')} do roteiro, trocar o localizador `{_cel(cura.get('localizador'))}` por "
                    f"`{_cel(ap.get('seletor'))}` (estratégia `{ap.get('estrategia')}`)"
                    + (", que resolve o mesmo elemento da referência." if cura.get("mesmo_elemento") else
                       (" e conferir à mão: o roteiro passou, mas com outro elemento, não o alvo da referência." if cura.get("mesmo_elemento") is False else ".")), ""]
        else:
            acao = [(f"Sugestão (o agente não altera a aplicação): nenhum candidato levou o roteiro ao fim no passo {cura.get('passo')} "
                     f"(localizador `{_cel(cura.get('localizador'))}`); o roteiro precisa de um localizador novo escrito à mão. Falha registrada: `{_cel(cura.get('falha'))}`."), ""]
        acao += [f"Comando para reexecutar o caso: `{comando_reexecucao}`" if comando_reexecucao else "Comando de reexecução: não registrado nesta trilha.", ""]
    else:
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
    elif cura is not None and diag is None:
        arvore += ["Sem gabarito nem modelo: a cura de seletor é toda em código; a regra R3 separa o mesmo elemento da referência de outro que fez o roteiro passar.", ""]
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


# ------------------------------------------------------------------ versão 3: o relatório de defeito no molde da seção 5.5 do CTFL 4.0

# ! Alteração de IA - Revisar: (07/11/2026, Pós-Fase 4, pacote Q1) o relatório v3 por caso, no molde do relatório de defeitos da
# seção 5.5 do syllabus CTFL 4.0 (decisão 104): os onze campos da 5.5 primeiro, preenchidos da trilha v2 (identificador, título,
# data e autor, objeto e ambiente, contexto, descrição para reproduzir, esperado contra real, referências), com severidade,
# prioridade e estado em branco para o analista; depois os seis blocos do v2 (veredito, evidência, contraste, FONTE, ação, árvore),
# reescritos com cada código de situação acompanhado do significado e sem os nomes internos da trilha. Os verbetes são citados
# pela camada de leitura (`biblioteca_leitura.py`); nada aqui chama modelo; `relatorio_do_caso_v2` continua byte a byte igual, para
# as corridas gravadas. `gerar_v3_da_pasta` regera os relatórios de uma pasta de corrida inteira (`--v3 --saida`, com `--check`).
# ! Motivo: plano aprovado da Pós-Fase 4, seção 3.1: o relatório v2 tem seis seções fixas e não tem metade dos campos que a 5.5
# lista (identificador, data e autor, objeto e ambiente, contexto, passos para reproduzir, severidade, prioridade, estado); o que o
# código sabe vem da trilha, e o que é do analista fica em branco com a classe e o nível do caso ao lado. A linguagem segue a
# regra de escrita do Eric (seção 1.4 do plano); os filtros do pacote Q2 medem cada frase gerada aqui.
CAMPOS_55 = ("Identificador", "Título", "Data, organização e autor", "Objeto de teste e ambiente", "Contexto", "Descrição para reproduzir",
             "Resultado esperado e resultado real", "Severidade", "Prioridade", "Estado", "Referências")
SECOES_MANTIDAS_V3 = ("Veredito do agente", "Evidência", "Contraste com a segunda causa", "FONTE declarada e conferida", "Linha de ação", "Árvore completa")
EM_BRANCO = "em branco: preenche o analista"
SEM_SELO = "sem selo: a resposta não trouxe a linha CAUSA_RAIZ, e não há probabilidade a ler"
SELO_EM_PALAVRAS = {"alto": "o agente está seguro desta causa",
                    "medio": "o agente tem dúvida entre causas vizinhas; confira antes de agir",
                    "baixo": "o agente não está seguro desta causa; trate como hipótese e confira antes de agir"}
STATUS_EM_PALAVRAS = {200: "a API respondeu sem código de erro", 201: "a API criou o registro", 204: "a API respondeu sem corpo",
                      400: "a API recusou a requisição como mal formada", 403: "a API recusou o acesso", 404: "a API não achou o recurso",
                      422: "a API recusou os dados enviados", 429: "a API barrou por excesso de requisições", 500: "a API falhou por erro interno",
                      502: "o servidor da frente não conseguiu falar com a API", 503: "a API estava indisponível"}
# O que cada modo de injeção da CobaiaAPI faz (conferido em CobaiaAPI/app/fault_injection.py) e o que cada modo de quebra de
# localizador faz (as quatro frases de cenarios_fase4.DESCRICAO_DO_MODO, copiadas porque aquele módulo importa o navegador).
MODO_EM_PALAVRAS = {
    "normal": "sem falha injetada",
    "error_500": "a CobaiaAPI responde com erro interno, status 500",
    "latency": "a CobaiaAPI demora de propósito antes de responder",
    "type_drift": "um campo da resposta vem com outro tipo: número vira texto, e texto vira o inteiro 1",
    "field_missing": "um campo do contrato é apagado da resposta",
    "field_renamed": "um campo da resposta vem com o nome trocado, com o sufixo _v2",
    "malformed_json": "a CobaiaAPI devolve o JSON cortado no meio, de propósito",
    "escala_ou_unidade_errada": "um valor numérico vem multiplicado por 100",
    "formato_de_data_divergente": "a data vem como dia/mês/ano em vez de ano-mês-dia",
    "chave_de_juncao_errada": "o rótulo de junção (o tipo) vem trocado entre os itens da lista",
    "contagem_inconsistente": "a lista vem sem o último item",
    "nulo_inesperado": "um campo obrigatório vem nulo",
    "valor_fora_do_dominio": "um valor vem fora do domínio permitido (número negativo, status desconhecido, booleano como texto)",
    "corpo_vazio": "a resposta vem sem corpo",
    "corpo_nao_e_json": "a resposta vem em HTML, não em JSON",
    "codificacao_incorreta": "os acentos vêm trocados: texto gravado em UTF-8 e lido como latin-1",
    "limite_de_requisicoes": "a CobaiaAPI responde 429, limite de requisições",
    "recurso_inexistente": "a CobaiaAPI responde 404, recurso não encontrado",
    "registro_duplicado": "o primeiro item da lista vem repetido",
    "estrutura_aninhada_divergente": "um campo vem aninhado dentro de um objeto com valor e moeda",
    "colecao_no_lugar_de_objeto": "vem uma lista onde se espera um objeto, ou o inverso",
    "id_renomeado": "o id (ou o atributo identificador) do alvo é renomeado",
    "classe_trocada": "a classe que o localizador usa é trocada por outra",
    "texto_alterado": "o texto do alvo (ou o seu valor ou placeholder) ganha uma palavra",
    "estrutura_alterada": "o alvo é envolvido num contêiner novo e trocado de posição entre os irmãos",
}
ESTRATEGIA_EM_PALAVRAS = {"papel_e_nome": "o elemento é achado pelo papel e pelo nome acessíveis, iguais aos do alvo",
                          "papel_e_nome_parecido": "o elemento é achado pelo papel igual e pelo nome parecido com o do alvo",
                          "texto_contido": "o elemento é achado pelo texto, que contém o texto do alvo",
                          "data_id": "o elemento é achado pelo mesmo data-id do alvo",
                          "caminho_do_ancestral_com_id": "o elemento é achado pelo caminho a partir do ancestral com id mais próximo",
                          "posicao_entre_irmaos": "o elemento é achado pela posição entre os irmãos, dentro do pai do alvo"}
ACAO_EM_PALAVRAS = {"abrir": "Abrir", "esperar": "Esperar aparecer", "clicar": "Clicar em", "preencher": "Preencher", "conferir": "Conferir"}
ROTULO_DA_REGRA_V3 = {**ROTULO_DA_REGRA, "fonte_formato_valido": "A linha FONTE só tem identificadores, no formato pedido",
                      "fonte_contem_termo_da_causa": "O verbete citado fala da causa respondida", "conferencia_do_roteiro": "Conferência do roteiro"}
RESULTADO_EM_PALAVRAS = {"confere": "confere", "nao_confere": "não confere", "nao_se_aplica": "não se aplica", "nao_verificavel": "não dá para conferir por código",
                         "informativo": "só informa"}
# ! Alteração de IA - Revisar: (07/11/2026, Pós-Fase 4, pacote Q2) o molde do relatório v3 ajustado pelos filtros de texto (filtros_de_texto.py): a classe e o nível
# do caso saem em palavras do molde (CLASSE_EM_PALAVRAS, NIVEL_EM_PALAVRAS), e não no texto copiado de taxonomia.py; a prioridade cita a classe e o nível na forma
# curta, em vez de repetir a frase inteira da severidade; os termos que a lista fechada pede explicados ganham o significado na primeira menção (Ollama, Playwright,
# CTFL e ISTQB no parágrafo de abertura; hash no identificador; harness no autor; quantização, num_ctx, tokens, temperatura e prompt no ambiente); o que veio de fora
# (o sintoma do caso, a observação adicional, a mensagem de erro do navegador, a descrição da quebra) vai em citação do Markdown (`_citacao`); as conferências do
# roteiro que passaram viram uma frase só (a tabela do bloco 7 traz cada uma); a poda diz o tamanho antes e depois em palavras; os nós de decisão da árvore saem em
# subitens. Nada muda no v2 nem nos campos da 5.5.
# ! Motivo: a leitura exploratória do Q2 sobre os 120 relatórios v3 das corridas 18d, 21d e 24 reprovou todos: nove termos da lista fechada sem o significado em cada
# relatório (ctfl, istqb, hash, harness, ollama, prompt, quantização, num_ctx, temperatura), "enum" em 22, os preenchimentos "claramente" e "de fato" trazidos da
# taxonomia, e a repetição de trigramas acima do percentil 95 do corpus (0,031) em 71 dos 74 da tela, por causa da frase da classe e do nível repetida em três blocos
# vizinhos e das conferências escritas uma a uma. O plano (seção 9) manda ajustar o molde até passar e registrar a leitura antes e depois.
CLASSE_EM_PALAVRAS = {1: "léxica: o corpo da resposta nem dá para ler", 2: "sintática: a forma da resposta não é a esperada",
                      3: "semântica: os tipos ou os domínios dos valores não fazem sentido", 4: "tradução: o mapeamento entre as camadas está errado",
                      5: "tempo e estado: o comportamento no tempo ou no estado está errado", 6: "efeito: o que o usuário vê na tela está errado"}
NIVEL_EM_PALAVRAS = {"facil": "fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu",
                     "medio": "médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato",
                     "dificil": "difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela"}
BANCO_EM_PALAVRAS = {"tela": "`banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação)",
                     "ineditos": "`banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27)",
                     "cenarios": "`cenarios_fase4.py` (catálogo dos dez cenários do ensaio da Fase 5, ficha 36)",
                     "calibracao": "`banco_casos.py` ou `banco_casos_extra.py` (os 90 casos da calibração)"}
PREFIXO_DA_LEITURA = bl.PASTA_LEITURA.relative_to(bl.RAIZ_DO_REPOSITORIO).as_posix()
PREFIXO_DA_BIBLIOTECA = bl.PASTA_BIBLIOTECA.relative_to(bl.RAIZ_DO_REPOSITORIO).as_posix()
_ROTULOS_DO_CASO = (("REQUISIÇÃO", "requisicao"), ("STATUS HTTP", "status"), ("CONTRATO ESPERADO PELA INTERFACE", "contrato"),
                    ("CORPO DA RESPOSTA", "corpo"), ("ÁRVORE DE ACESSIBILIDADE DA PÁGINA", "arvore"), ("SELETOR QUE FALHOU", "seletor_quebrado"),
                    ("SINTOMA OBSERVADO", "sintoma"), ("OBSERVAÇÃO ADICIONAL", "observacao"))


def _prosa(texto) -> str:
    """Texto vindo dos dados (sintoma, descrição da quebra, erro) posto em frase corrida: sem travessão nem seta, numa linha."""
    return " ".join(bl._sem_travessao(str("" if texto is None else texto)).split()).replace(" .", ".")


def _contrato_do_caso(dados: dict) -> str | None:
    """O contrato esperado pela interface, quando o caso traz um: `n/a` e o aviso entre parênteses das páginas do front legado
    (que não têm contrato de API) contam como ausência."""
    contrato = str(dados.get("contrato") or "").strip()
    return contrato if contrato and contrato != "n/a" and not contrato.startswith("(") else None


def _data_hora(ts) -> str:
    if not ts:
        return "não registrada"
    try:
        return datetime.fromisoformat(str(ts)).strftime("%d/%m/%Y %H:%M:%S")
    except ValueError:
        return str(ts)


def _classe_em_palavras(classe, curta: bool = False) -> str | None:
    """A classe do caso (taxonomia.CLASSES) nas palavras do molde; `curta` dá só o nome (léxica, sintática, ...)."""
    try:
        taxonomia.CLASSES[int(classe)]
        texto = CLASSE_EM_PALAVRAS[int(classe)]
    except (KeyError, TypeError, ValueError):
        return None
    return f"classe {classe} ({texto.split(':')[0] if curta else texto})"


def _nivel_em_palavras(nivel, curta: bool = False) -> str | None:
    """O nível do caso (taxonomia.NIVEIS) nas palavras do molde; `curta` dá só o nome (fácil, médio, difícil)."""
    try:
        n = taxonomia.NIVEIS[int(nivel)]
    except (KeyError, TypeError, ValueError):
        return None
    texto = NIVEL_EM_PALAVRAS.get(n["id"], n["id"])
    return f"nível {nivel} ({texto.split(':')[0] if curta else texto})"


def _citacao(texto) -> list[str]:
    """Texto trazido de fora (o sintoma do caso, a mensagem do navegador, a descrição da quebra) em citação do Markdown: o analista o lê como
    veio, e os filtros de texto não o medem como escrita do molde."""
    return ["> " + _prosa(texto)]


def _tamanho_em_palavras(d) -> str:
    """O tamanho que a poda registra ({"nos": 179}, {"linhas": 39}, {"chars": 1718}) em palavras."""
    if not isinstance(d, dict) or not d:
        return _cel(json.dumps(d, ensure_ascii=False))
    nomes = {"nos": "nós", "linhas": "linhas", "chars": "caracteres", "itens": "itens", "campos": "campos"}
    return ", ".join(f"{v} {nomes.get(k, k)}" for k, v in d.items())


def _status_em_palavras(status) -> str:
    if status is None or status == "":
        return "status não registrado"
    try:
        codigo = int(status)
    except (TypeError, ValueError):
        return f"status {status}"
    return f"status {codigo} ({STATUS_EM_PALAVRAS.get(codigo, 'código fora da lista deste relatório')})"


def _modo_em_palavras(modo) -> str:
    return f"`{modo}` ({MODO_EM_PALAVRAS.get(modo, 'modo fora da lista deste relatório')})" if modo else "sem modo registrado"


def _campos_do_caso_escrito(texto: str) -> dict:
    """Os campos de um caso lido em texto (o formato de estrategias._dados_do_caso): requisição, status, contrato, corpo, árvore, seletor,
    sintoma e observação; o status vira inteiro quando é só dígitos."""
    saida: dict = {}
    atual = None
    for linha in texto.splitlines():
        for rotulo, chave in _ROTULOS_DO_CASO:
            if linha.startswith(rotulo + ":"):
                atual = chave
                saida[chave] = linha[len(rotulo) + 1:].strip()
                break
        else:
            if atual is not None:
                saida[atual] = (saida[atual] + "\n" + linha) if saida[atual] else linha
    saida = {k: v.strip() for k, v in saida.items()}
    if str(saida.get("status", "")).isdigit():
        saida["status"] = int(saida["status"])
    return saida


def _causa_em_palavras(escolha, leituras: dict | None) -> str:
    """O título do verbete de erro da causa, pela camada de leitura; sem leitura, o rótulo com espaços no lugar dos sublinhados."""
    if escolha is None:
        return "sem causa respondida"
    for l in (leituras or {}).values():
        if l.get("causa_raiz") == escolha and l.get("tipo") == "erro":
            return l["titulo"]
    return str(escolha).replace("_", " ").capitalize()


def _referencia_do_verbete(i: str, leituras: dict | None) -> str:
    l = (leituras or {}).get(i)
    if l is None:
        return f"`{i}` (sem leitura gerada na camada de leitura)"
    return (f"`{i}` ({l['titulo']}; leitura: `{PREFIXO_DA_LEITURA}/{l['caminho']}`; verbete: "
            f"`{PREFIXO_DA_BIBLIOTECA}/{l.get('verbete') or l['caminho']}`)")


def nome_do_relatorio(tid: str) -> str:
    """O nome do arquivo do relatório de uma trilha: o último trecho do id, com `#` (repetição de um cenário) escrito como `__r`."""
    return tid.rsplit("/", 1)[-1].replace("#", "__r")


def comando_de_reexecucao(modo: str | None, saida: str, tid: str, k: int = 3) -> str:
    """O comando que reexecuta só este caso numa saída própria, como o executor grava nos relatórios v2 de cada modo."""
    nome = tid.rsplit("/", 1)[-1]
    caso = nome.split("@")[0].split("#")[0]
    base = f"RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo {modo or 'tela'} --saida {saida}_reexec"
    if modo == "tela":
        return f"{base} --ids {caso} --k {k}"
    if modo == "cenarios":
        return f"{base} --repeticoes 1"
    if modo == "ineditos":
        return f"{base} --ids {caso}"
    return base


def _contexto_v3(eventos: list[dict], tid: str, pasta_blobs: Path | None = None, leituras: dict | None = None) -> dict:
    """Tudo o que o relatório v3 e o índice precisam de uma trilha, lido uma vez: os eventos por tipo, o caso (ao vivo ou escrito), o
    nó de diagnóstico, a cura, o título e a causa em palavras."""
    blobs = tr.blobs_de(eventos, pasta_blobs)
    seq = [e for e in eventos if e["trilha"] == tid]
    if not seq:
        raise KeyError(f"trilha {tid!r} não está no arquivo")
    cab = next((e["dados"] for e in eventos if e["tipo"] == "corrida"), {})
    por_tipo: dict[str, list[dict]] = {}
    for e in seq:
        por_tipo.setdefault(e["tipo"], []).append(e)
    ev_entrada = (por_tipo.get("entrada") or [{"dados": {}, "ts": None}])[0]
    entrada = ev_entrada["dados"]
    decl = {e["dados"]["campo"]: e["dados"] for e in por_tipo.get("declaracao", []) if e["dados"].get("campo") in NOME_DO_CAMPO}
    citadas = [e["dados"] for e in por_tipo.get("declaracao", []) if e["dados"].get("campo") == "fonte_citada"]
    ver = [e["dados"] for e in por_tipo.get("verificacao", [])]
    nos = por_tipo.get("decisao", [])
    diag = next((e["dados"] for e in reversed(nos) if e["dados"].get("decisao") == "diagnostico"), None)
    no_cura = next((e["dados"] for e in reversed(nos) if e["dados"].get("decisao") == "cura"), None)
    cura = (por_tipo.get("cura") or [{"dados": None}])[-1]["dados"]
    acoes = [e["dados"] for e in por_tipo.get("acao", [])]
    acoes_originais = [a for a in acoes if not a.get("reexecucao")]
    passo_falho = next((a for a in acoes_originais if a.get("falhou")), None)
    conferencias = [v for v in ver if v.get("regra") == "conferencia_do_roteiro" and not (v.get("evidencia") or {}).get("reexecucao")]
    interceptacoes = por_tipo.get("interceptacao", [])
    inter = interceptacoes[0]["dados"] if interceptacoes else None
    caso_vivo = None
    if entrada.get("caso_ao_vivo") and blobs.get(entrada["caso_ao_vivo"]):
        try:
            caso_vivo = json.loads(blobs[entrada["caso_ao_vivo"]])
        except ValueError:
            caso_vivo = None
    texto_caso = blobs.get(entrada["texto"]) if entrada.get("texto") else None
    caso_escrito = _campos_do_caso_escrito(texto_caso) if texto_caso else {}
    dados_do_caso = (caso_vivo or {}).get("entrada") or caso_escrito
    requisicao = dados_do_caso.get("requisicao") or (f"{inter['metodo']} {inter['caminho']}" if inter else None)
    campo_decl = (decl.get("campo") or {}).get("lido")
    if str(campo_decl or "").strip().lower() == "nenhum":
        campo_decl = None
    escolha = diag.get("escolha") if diag else None
    classe, nivel = entrada.get("classe"), entrada.get("nivel")
    if classe is None and caso_vivo:
        classe, nivel = caso_vivo.get("classe"), caso_vivo.get("nivel")
    c = {"blobs": blobs, "seq": seq, "cab": cab, "por_tipo": por_tipo, "entrada": entrada, "ts_entrada": ev_entrada.get("ts"), "decl": decl,
         "citadas": citadas, "ver": ver, "sem_gabarito": [v for v in ver if not v.get("usa_gabarito")], "com_gabarito": [v for v in ver if v.get("usa_gabarito")],
         "nos": nos, "diag": diag, "no_cura": no_cura, "cura": cura, "nos_bib": [e["dados"] for e in nos if e["dados"].get("decisao") == "edicao_biblioteca"],
         "edicoes": [e["dados"] for e in por_tipo.get("edicao_biblioteca", [])], "intervencoes": [e["dados"] for e in por_tipo.get("intervencao", [])],
         "podas": por_tipo.get("poda", []), "interceptacoes": interceptacoes, "inter": inter, "acoes": acoes, "acoes_originais": acoes_originais,
         "passo_falho": passo_falho, "conferencias": conferencias, "nome": tid.rsplit("/", 1)[-1], "caso_id": entrada.get("caso") or tid.rsplit("/", 1)[-1],
         "leituras": leituras or {}, "caso_vivo": caso_vivo, "texto_caso": texto_caso, "caso_escrito": caso_escrito, "dados_do_caso": dados_do_caso,
         "requisicao": requisicao, "pagina": next((a.get("url") for a in acoes_originais if a.get("acao") == "abrir" and a.get("url")), None),
         "eh_localizador": entrada.get("localizador") is not None or cura is not None, "eh_texto": texto_caso is not None and not acoes and not interceptacoes,
         "escolha": escolha, "campo": (diag or {}).get("campo") or campo_decl, "confianca": (diag or {}).get("confianca") or {},
         "modo": entrada.get("modo"), "roteiro": entrada.get("roteiro") or entrada.get("cenario"), "classe": classe, "nivel": nivel,
         "modo_da_corrida": cab.get("modo"), "entregues": [], "titulo": ""}
    c["eventos"] = eventos
    c["selo"] = c["confianca"].get("selo")
    c["causa_em_palavras"] = _causa_em_palavras(escolha, leituras)
    cand = (por_tipo.get("candidatos") or [{"dados": {}}])[0]["dados"]
    entregues = [i["id"] for i in cand.get("itens") or [] if i.get("escolhido")]
    if not entregues:
        entregues = next((p["dados"]["verbetes_ids"] for p in por_tipo.get("prompt", [])
                          if p["dados"].get("etapa") == "diagnostico" and p["dados"].get("verbetes_ids")), [])
    c["entregues"] = list(entregues)
    c["titulo"] = _titulo_v3(c)
    return c


def _titulo_v3(c: dict) -> str:
    inicio = c["causa_em_palavras"] if c["escolha"] is not None else "Sem causa respondida (a linha CAUSA_RAIZ não veio)"
    cura = c["cura"] or {}
    if c["eh_localizador"]:
        passo = (c["passo_falho"] or {}).get("passo") or cura.get("passo")
        loc = c["entrada"].get("localizador") or cura.get("localizador")
        titulo = f"{inicio} no passo {passo} do roteiro `{c['roteiro']}` (localizador `{_cel(loc)}`)"
        return titulo + (", curado pelo agente" if cura.get("curado") else "")
    titulo = f"{inicio} em `{c['requisicao']}`" if c["requisicao"] else f"{inicio} no caso `{c['caso_id']}`"
    return titulo + (f", campo `{_cel(c['campo'])}`" if c["campo"] else "")


def _objeto_e_ambiente(c: dict) -> list[str]:
    cab, inter = c["cab"], c["inter"]
    if c["eh_texto"]:
        objeto = (f"A requisição `{c['requisicao']}` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a "
                  "requisição, o status, o contrato, o corpo e o sintoma).")
    elif c["eh_localizador"]:
        alvo = c["entrada"].get("alvo") or (c["cura"] or {}).get("alvo") or {}
        objeto = (f"O roteiro `{c['roteiro']}` do site PHP (CobaiaFront), a partir da página `{c['pagina'] or 'não registrada'}`; o alvo do passo que falhou é "
                  f"{_cel(alvo.get('papel') or 'um elemento')} \"{_cel(alvo.get('nome'))}\" (localizador `{_cel(c['entrada'].get('localizador') or (c['cura'] or {}).get('localizador'))}`).")
    elif inter:
        objeto = (f"A página `{c['pagina'] or 'não registrada'}` do site PHP (CobaiaFront), que chama a CobaiaAPI em `{inter.get('metodo')} {inter.get('caminho')}` "
                  f"(host {inter.get('host') or 'não registrado'}).")
    else:
        objeto = f"A página `{c['pagina']}` do site PHP (CobaiaFront)." if c["pagina"] else f"O caso `{c['caso_id']}`, sem página nem requisição registradas na trilha."
    ambiente = (f"Modelo `{cab.get('modelo')}`" + (f" (quantização {cab['quantizacao']}: os pesos do modelo guardados com menos bits, para caber na memória)" if cab.get("quantizacao") else "")
                + f" no Ollama {cab.get('versao_ollama')}, só CPU. Janela de contexto num_ctx {cab.get('num_ctx')} tokens (os pedaços de texto que o modelo lê de uma vez) e "
                f"temperatura {_num(cab.get('temperatura'), 1)} (quase nenhuma aleatoriedade na resposta).")
    if cab.get("playwright"):
        ambiente += f" Playwright {cab['playwright']} com o navegador {cab.get('navegador')} (canal {cab.get('canal') or 'não registrado'}, sem janela)."
    else:
        ambiente += " Esta corrida rodou sem navegador."
    ambiente += (f" Biblioteca de produção `{cab.get('hash_biblioteca')}`, índice da busca `{cab.get('hash_indice')}` e prompt fixo `{cab.get('hash_prompt_fixo')}` "
                 f"(o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); {cab.get('k', 3)} verbetes por consulta. "
                 "As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.")
    return [objeto, "", ambiente, ""]


def _contexto_em_texto(c: dict) -> list[str]:
    e = c["entrada"]
    classe_nivel = "; ".join(x for x in (_classe_em_palavras(c["classe"]), _nivel_em_palavras(c["nivel"])) if x)
    if c["eh_texto"]:
        banco = BANCO_EM_PALAVRAS.get(c["modo_da_corrida"], "o banco da corrida")
        return [f"Caso escrito `{c['caso_id']}`, de {banco}" + (f"; {classe_nivel}" if classe_nivel else "")
                + ". Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.", ""]
    if c["eh_localizador"]:
        cura = c["cura"] or {}
        passo = (c["passo_falho"] or {}).get("passo") or cura.get("passo")
        acao = (c["passo_falho"] or {}).get("acao")
        armado = e.get("armado") or {}
        texto = (f"Roteiro `{c['roteiro']}` do site PHP"
                 + (f" (cenário `{e['cenario_da_fase_5']}` do ensaio da Fase 5, execução {e.get('repeticao', 1)})" if e.get("cenario_da_fase_5") else "")
                 + f"; quebra de localizador {_modo_em_palavras(e.get('modo'))}, forma `{e.get('forma') or 'não registrada'}`"
                 + (f" ({_prosa(armado.get('como'))})" if armado.get("como") else "")
                 + f". O passo {passo}" + (f" ({ACAO_EM_PALAVRAS.get(acao, acao).lower()} `{_cel((c['passo_falho'] or {}).get('seletor'))}`)" if acao else "") + " falhou.")
        return [texto + (f" {classe_nivel[0].upper() + classe_nivel[1:]}." if classe_nivel else ""), ""]
    texto = f"Roteiro `{c['roteiro'] or 'não registrado'}` da tela, com a falha injetada {_modo_em_palavras(c['modo'])}"
    if e.get("campo"):
        texto += f" no campo `{_cel(e['campo'])}`"
    if c["passo_falho"]:
        pf_ = c["passo_falho"]
        texto += f". O roteiro parou no passo {pf_.get('passo')} ({ACAO_EM_PALAVRAS.get(pf_.get('acao'), pf_.get('acao')).lower()} `{_cel(pf_.get('seletor') or pf_.get('url'))}`)"
    texto += f". Caso `{c['caso_id']}`"
    if c["modo_da_corrida"] in BANCO_EM_PALAVRAS:
        texto += f", de {BANCO_EM_PALAVRAS[c['modo_da_corrida']]}"
    return [texto + (f"; {classe_nivel}." if classe_nivel else "."), ""]


def _passos_do_roteiro(c: dict) -> list[str]:
    linhas = []
    for n, a in enumerate(c["acoes_originais"], start=1):
        alvo = a.get("url") if a.get("acao") == "abrir" else a.get("seletor")
        linha = f"{n}. {ACAO_EM_PALAVRAS.get(a.get('acao'), a.get('acao'))} `{_cel(alvo)}`"
        if a.get("tempo_ms") is not None:
            linha += f" ({_num(float(a['tempo_ms']) / 1000, 1)} s)"
        linhas.append(linha + (": falhou aqui." if a.get("falhou") else "."))
    return linhas


def _descricao_para_reproduzir(c: dict, comando_reexecucao: str | None) -> list[str]:
    blobs, inter, dados = c["blobs"], c["inter"], c["dados_do_caso"]
    partes: list[str] = []
    if c["eh_texto"]:
        partes += ["O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):", "",
                   f"1. Requisição `{dados.get('requisicao') or 'não informada'}`, {_status_em_palavras(dados.get('status'))}."]
        if _contrato_do_caso(dados):
            partes.append(f"2. Contrato da interface: `{_contrato_do_caso(dados)}`.")
        if dados.get("corpo") is not None:
            partes += ["3. Corpo da resposta:", "", _bloco(dados["corpo"]), ""]
        if dados.get("arvore"):
            partes += ["Árvore de acessibilidade da página, como o caso a trouxe:", "", _bloco(dados["arvore"]), ""]
        if dados.get("seletor_quebrado"):
            partes.append(f"Seletor que falhou: `{_cel(dados['seletor_quebrado'])}`.")
        partes += ["4. Sintoma observado (texto do caso):", "", *_citacao(dados.get("sintoma") or "não informado"), ""]
        if dados.get("observacao"):
            partes += ["5. Observação adicional (texto do caso):", "", *_citacao(dados["observacao"]), ""]
    else:
        passos = _passos_do_roteiro(c)
        if passos:
            partes += ["Passos do roteiro, na ordem em que o agente os executou (os tempos são os medidos):", "", *passos, ""]
        if c["eh_localizador"]:
            e, cura = c["entrada"], c["cura"] or {}
            passo = (c["passo_falho"] or {}).get("passo") or cura.get("passo")
            loc = e.get("localizador") or cura.get("localizador")
            partes += [f"O passo {passo} (localizador `{_cel(loc)}`) falhou com a mensagem abaixo (do navegador, como veio):", "",
                       *_citacao(cura.get("erro") or "o localizador não resolveu nenhum elemento"), ""]
            if e.get("descricao"):
                como = (f" (forma `{e.get('forma')}`" + (f", armada por {_prosa((e.get('armado') or {}).get('como'))}" if (e.get("armado") or {}).get("como") else "") + ")"
                        if e.get("forma") else "")
                partes += [f"Como provocar a mesma quebra{como}:", "", *_citacao(e["descricao"]), ""]
            mutacoes = [f"- Mutação `{_cel(m.get('op'))}` no seletor `{_cel(m.get('seletor'))}`" + (f", novo valor `{_cel(m['para'])}`" if m.get("para") else "") + "."
                        for m in e.get("mutacoes") or []]
            if mutacoes:
                partes += mutacoes + [""]
        if inter:
            partes.append(f"A página chamou `{inter.get('metodo')} {inter.get('caminho')}`" + (f" em {inter['host']}" if inter.get("host") else "")
                          + f" e recebeu {_status_em_palavras(inter.get('status'))}"
                          + (f", `{inter['content_type']}`" if inter.get("content_type") else "")
                          + (f", {inter['corpo_chars']} caracteres" if inter.get("corpo_chars") is not None else "")
                          + (f", em {_num(inter.get('tempo_ms'), 1)} ms" if inter.get("tempo_ms") is not None else "") + ".")
            partes.append("")
        falharam = [v for v in c["conferencias"] if v.get("resultado") != "confere"]
        for v in falharam:
            ev = v.get("evidencia") or {}
            partes.append(f"A conferência do roteiro `{_cel(v.get('alvo'))}` {RESULTADO_EM_PALAVRAS.get(v.get('resultado'), v.get('resultado'))}: "
                          f"esperava {_prosa(ev.get('esperado'))} e observou {_prosa(ev.get('observado'))}.")
        passaram = len(c["conferencias"]) - len(falharam)
        if passaram == 1:
            partes.append(("A outra conferência" if falharam else "A conferência") + " do roteiro confere (a tabela do bloco 7 a traz).")
        elif passaram > 1:
            partes.append((f"As outras {passaram} conferências" if falharam else f"As {passaram} conferências") + " do roteiro conferem (a tabela do bloco 7 traz cada uma).")
        if c["conferencias"]:
            partes.append("")
        if dados.get("sintoma"):
            partes += ["Sintoma, como o código o descreveu para o agente:", "", *_citacao(dados["sintoma"]), ""]
        trecho = None
        for e in c["podas"]:
            d = e["dados"]
            if d.get("alvo") == "corpo_http" and d.get("sha") in blobs and blobs[d["sha"]] is not None:
                trecho = (d["sha"], blobs[d["sha"]])
                break
        if trecho is None and inter and inter.get("corpo") in blobs and blobs[inter["corpo"]] is not None:
            trecho = (inter["corpo"], blobs[inter["corpo"]])
        if trecho:
            partes += [f"Trecho da resposta, como a poda em código deixou para o agente (hash `{trecho[0]}`):", "", _bloco(trecho[1]), ""]
    partes.append(f"Comando para reexecutar o caso: `{comando_reexecucao}`" if comando_reexecucao else "Comando de reexecução: não registrado nesta trilha.")
    return partes + [""]


def _esperado_e_real(c: dict) -> list[str]:
    dados = c["dados_do_caso"]
    partes: list[str] = []
    contrato = _contrato_do_caso(dados)
    if contrato:
        partes += [f"Contrato esperado pela interface: `{contrato}`.", ""]
    linhas: list[list[str]] = []
    onde_corpo = f"corpo de `{c['requisicao']}`" if c["requisicao"] else "corpo da resposta"
    for e in c["podas"]:
        d = e["dados"]
        for x in d.get("diff") or []:
            if d.get("alvo") == "arvore":
                linhas.append(["tela (árvore de acessibilidade, contra a referência em modo normal)", _cel(x.get("esperado")), _cel(x.get("recebido"))])
            else:
                onde = onde_corpo + (f", campo `{_cel(x['campo'])}`" if x.get("campo") else " (corpo inteiro)") + (f" (item {x['item']})" if x.get("item") else "")
                linhas.append([onde, _cel(x.get("esperado")), _cel(x.get("recebido") if x.get("recebido") is not None else "ausente")])
    for v in c["conferencias"]:
        ev = v.get("evidencia") or {}
        linhas.append([f"conferência do roteiro `{_cel(v.get('alvo'))}`", _cel(ev.get("esperado")), _cel(ev.get("observado"))])
    if c["eh_localizador"]:
        e, cura = c["entrada"], c["cura"] or {}
        alvo = e.get("alvo") or cura.get("alvo") or {}
        passo = (c["passo_falho"] or {}).get("passo") or cura.get("passo")
        tempo = (c["passo_falho"] or {}).get("tempo_ms")
        linhas.append([f"passo {passo}, localizador `{_cel(e.get('localizador') or cura.get('localizador'))}`",
                       f"um elemento {_cel(alvo.get('papel') or '')} \"{_cel(alvo.get('nome'))}\" visível, como na referência",
                       (f"nenhum elemento em {_num(float(tempo) / 1000, 1)} s" if tempo is not None else "nenhum elemento") + (f": {_cel(cura.get('erro'))}" if cura.get("erro") else "")])
    if c["eh_texto"]:
        linhas.append([onde_corpo, "um JSON com os campos do contrato acima" if contrato else "a resposta que a interface espera",
                       "o corpo abaixo" if dados.get("corpo") is not None else "não informado"])
        if dados.get("sintoma"):
            linhas.append(["o que a interface mostrou", "a página com os dados da resposta", _cel(_prosa(dados["sintoma"]))])
    if linhas:
        partes += ["O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):", "",
                   _tabela(["Onde", "Esperado", "Recebido"], linhas), ""]
    else:
        partes += ["A trilha não guardou diferença medida em código entre o esperado e o recebido para este caso.", ""]
    if c["eh_texto"] and dados.get("corpo") is not None:
        partes += ["Corpo recebido, como veio no caso:", "", _bloco(dados["corpo"]), ""]
    ref = f"{c['cab'].get('corrida')}/referencia/{c['roteiro']}@normal" if c["roteiro"] else None
    if ref and any(e.get("trilha") == ref for e in c["eventos"]):
        partes += [f"A referência em modo normal desta corrida é a trilha `{ref}`: é contra ela que a poda comparou a tela e o corpo.", ""]
    return partes


def _referencias(c: dict, arquivo_trilha: str | None, relatorio_v2: str | None, comando_reexecucao: str | None, eventos: list[dict], tid: str) -> list[str]:
    citados = []
    for d in c["citadas"]:
        if d.get("valor") and d["valor"] not in citados:
            citados.append(d["valor"])
    entregues = [i for i in c["entregues"] if i not in citados]
    partes = ["- Verbetes citados pelo agente na linha FONTE: " + ("; ".join(_referencia_do_verbete(i, c["leituras"]) for i in citados) if citados else "nenhum") + ".",
              "- Verbetes entregues pela busca e não citados: " + ("; ".join(_referencia_do_verbete(i, c["leituras"]) for i in entregues) if entregues else "nenhum") + "."]
    if c["modo_da_corrida"] in BANCO_EM_PALAVRAS:
        partes.append(f"- Caso escrito: `{c['caso_id']}` em {BANCO_EM_PALAVRAS[c['modo_da_corrida']]}.")
    partes.append(f"- Trilha: `{tid}`" + (f" em `{arquivo_trilha}`" if arquivo_trilha else "")
                  + f", eventos {c['seq'][0]['seq']} a {c['seq'][-1]['seq']}, hash dos eventos `{hash_da_trilha(eventos, tid)}`.")
    if relatorio_v2:
        partes.append(f"- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `{relatorio_v2}`.")
    if comando_reexecucao:
        partes.append(f"- Comando de reexecução: `{comando_reexecucao}`.")
    partes.append("- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.")
    return partes + [""]


def _veredito_v3(c: dict) -> list[str]:
    diag, cura, no_cura, conf = c["diag"], c["cura"], c["no_cura"], c["confianca"]
    partes: list[str] = []
    if diag is not None:
        causa = f"`{_cel(c['escolha'])}` ({c['causa_em_palavras']})" if c["escolha"] is not None else "nenhuma: a resposta não trouxe a linha CAUSA_RAIZ"
        campo = f"`{_cel(c['campo'])}`" if c["campo"] else "nenhum apontado"
        confianca = SELO_EM_PALAVRAS.get(c["selo"], SEM_SELO)
        if conf.get("p_rotulo") is not None:
            confianca += f" (probabilidade {_prob(conf.get('p_rotulo'))} no rótulo; selo `{c['selo']}` pelos limiares da calibração)"
        partes += [f"Causa respondida: {causa}. Campo: {campo}. Confiança: {confianca}.", ""]
        impacto = c["decl"].get("impacto")
        partes += ["Impacto, nas palavras do modelo (texto do modelo, não conferido por código): "
                   + (_cod(impacto.get("valor")) if impacto and not impacto.get("ausente") else "a linha IMPACTO não veio na resposta") + ".", ""]
        partes += [f"Justificativa ({MARCA_DO_MOLDE} na corrida, como está na trilha):", "",
                   *_citacao(diag.get("justificativa") or justificativa_por_molde(diag, c["seq"], c["sem_gabarito"], c["intervencoes"])), ""]
        d = diag.get("divergencia") or {}
        if d.get("ha"):
            partes += ["Conflito: o que o modelo declarou diverge do que o código mediu"
                       + (f" (entre {' e '.join(d['entre'])})" if d.get("entre") else "") + (f": {_prosa(d['detalhe'])}." if d.get("detalhe") else ".") + "", ""]
        if diag.get("falha"):
            partes += [f"Falha registrada no nó: `{diag['falha']}` (origem: {tr.origem_da_falha(diag['falha'])}).", ""]
    if cura is not None:
        ap = cura.get("aplicado") or {}
        mesmo = cura.get("mesmo_elemento")
        if cura.get("curado"):
            texto = (f"Cura do localizador: aplicada `{_cel(ap.get('seletor'))}` (estratégia `{ap.get('estrategia')}`: "
                     f"{ESTRATEGIA_EM_PALAVRAS.get(ap.get('estrategia'), 'estratégia fora da lista deste relatório')}); reexecução validada; "
                     + ("é o mesmo elemento da referência." if mesmo else ("é outro elemento, não o alvo da referência (regra R3): o roteiro passou, mas confira à mão." if mesmo is False
                                                                          else "a impressão do elemento não foi comparada com a da referência.")))
        else:
            texto = (f"Cura do localizador: não curado; falha `{_cel(cura.get('falha'))}`; {cura.get('reexecucoes', 0)} reexecução(ões) sem levar o roteiro ao fim.")
        partes += [texto, ""]
        if cura.get("mttr_s") is not None:
            partes += [f"Da detecção à reexecução validada: {_num(cura.get('mttr_s'), 1)} s (detecção {_data_hora(cura.get('deteccao'))}; validação {_data_hora(cura.get('validacao'))}).", ""]
        partes += [f"Justificativa da cura ({MARCA_DO_MOLDE}, copiada da trilha):", "",
                   *_citacao((no_cura or {}).get("justificativa") or cura.get("justificativa") or justificativa_da_cura(cura)), ""]
    for no_bib in c["nos_bib"]:
        if no_bib.get("operacao") == "correcao":
            partes += [f"Biblioteca (ciclo de correção): {'corrigido' if no_bib.get('escolha') == 'corrigido' else 'não corrigido'}.", ""]
        else:
            partes += [(f"Biblioteca: {len(no_bib.get('aplicadas') or [])} edição(ões) aplicada(s), {len(no_bib.get('para_revisao') or [])} para revisão humana, "
                        f"{len(no_bib.get('recusadas') or [])} recusada(s)."), ""]
    if diag is None and cura is None and not c["nos_bib"]:
        partes += ["Nenhum nó de decisão nesta trilha.", ""]
    return partes


def _evidencia_v3(c: dict) -> list[str]:
    blobs = c["blobs"]
    partes: list[str] = []
    texto_caso = c["texto_caso"]
    if c["podas"] or c["interceptacoes"] or c["cura"] is not None:
        if texto_caso is not None:
            partes += ["O caso, como foi posto no prompt:", "", _bloco(texto_caso), ""]
    else:
        partes += ["Não houve interceptação nem poda nesta trilha: o caso entrou em texto." + ("" if texto_caso is None else " Como foi posto no prompt:"), ""]
        if texto_caso is not None:
            partes += [_bloco(texto_caso), ""]
    propostas = [d for d in c["edicoes"] if d.get("etapa") == "proposta"]
    if propostas:
        partes += ["Propostas de edição da biblioteca, na ordem em que o modelo as escreveu:", "",
                   _tabela(["Proposta", "Operação", "Verbete", "Resultado"],
                           [[str(d.get("numero")), _cel(d.get("operacao")), f"`{_cel(d.get('verbete'))}`",
                             "aplicada" if d.get("aplicada") else ("para revisão humana" if d.get("para_revisao") else f"recusada: `{_cel(d.get('codigo'))}`")] for d in propostas]), ""]
    cura = c["cura"]
    if cura is not None:
        alvo = cura.get("alvo") or {}
        partes += [(f"Alvo registrado na corrida de referência: {_cel(alvo.get('papel'))} \"{_cel(alvo.get('nome'))}\" (ocorrência {alvo.get('ocorrencia')}; "
                    f"tag `{_cel(alvo.get('tag'))}`; caminho `{_cel(alvo.get('caminho'))}`)."), "",
                   f"Candidatos de localizador, na ordem fixa em que o código os tenta (limiar do nome parecido {cura.get('limiar_nome')}), e o resultado de cada verificação:", ""]
        linhas_c = []
        for cand in cura.get("candidatos") or []:
            v = cand.get("verificacoes") or {}
            if not cand.get("gerado"):
                linhas_c.append([f"`{cand['estrategia']}`", f"não gerado: {_cel(cand.get('motivo'))}"] + ["não se aplica"] * 5 + [""])
                continue
            celulas = []
            for chave in ROTULO_DA_VERIFICACAO_DA_CURA:
                r = (v.get(chave) or {}).get("resultado")
                rot = {"confere": "confere", "nao_confere": "não confere", "nao_se_aplica": "não se aplica", "nao_tentado": "não tentado"}.get(r, _cel(r))
                det = (v.get(chave) or {}).get("detalhe")
                celulas.append(rot + (f" ({_cel(det)})" if det and r in ("nao_confere", "confere") and chave in ("nome_parecido", "efeito_na_reexecucao") else ""))
            linhas_c.append([f"`{cand['estrategia']}`", f"`{_cel(cand.get('seletor'))}`"] + celulas + ["sim" if cand.get("aplicado") else ""])
        partes += [_tabela(["Estratégia", "Seletor"] + list(ROTULO_DA_VERIFICACAO_DA_CURA.values()) + ["Aplicado"], linhas_c), ""]
    # a segunda poda e a segunda interceptação saem mais curtas: a primeira já disse o que é a poda e o que o status quer dizer
    for n, e in enumerate(c["podas"]):
        d = e["dados"]
        regras = d.get("regras") or []
        regras_txt = ", ".join(f"`{r}`" for r in regras) if isinstance(regras, list) else ", ".join(f"`{k}` {v}" for k, v in regras.items())
        if n == 0:
            partes += [(f"Poda de `{d.get('alvo')}` (evento {e['seq']}), feita em código antes de montar o prompt: {_tamanho_em_palavras(d.get('antes'))} antes, "
                        f"{_tamanho_em_palavras(d.get('depois'))} depois. Regras aplicadas: {regras_txt or 'nenhuma'}."), ""]
        else:
            partes += [(f"Também podado em código o `{d.get('alvo')}` (evento {e['seq']}): de {_tamanho_em_palavras(d.get('antes'))} para {_tamanho_em_palavras(d.get('depois'))}, "
                        f"pelas regras {regras_txt or 'nenhuma'}."), ""]
        linhas = [[_cel((x.get("campo") or "(corpo inteiro)") + (f" (item {x['item']})" if x.get("item") else "")), _cel(x.get("esperado")), _cel(x.get("recebido"))]
                  for x in d.get("diff") or []]
        if linhas:
            partes += [_tabela(["Campo do contrato", "Esperado", "Recebido"], linhas), ""]
        if d.get("sha") in blobs:
            texto = blobs[d["sha"]]
            partes += [(f"Trecho podado (hash `{d['sha']}`):" if n == 0 else f"O que sobrou desta poda (hash `{d['sha']}`):"), "",
                       _bloco(texto if texto is not None else f"(gravado fora da linha: {d['sha']})"), ""]
    for n, e in enumerate(c["interceptacoes"]):
        d = e["dados"]
        status = _status_em_palavras(d.get("status")) if n == 0 else f"status {d.get('status')}"
        partes += [f"Interceptação (evento {e['seq']}): `{d.get('metodo')} {d.get('caminho')}`, {status}; corpo guardado com o hash `{d.get('corpo')}`"
                   + (f"; árvore `{d.get('arvore')}`" if d.get("arvore") else "") + ".", ""]
    return partes or ["Nenhuma evidência registrada nesta trilha.", ""]


def _contraste_v3(c: dict) -> list[str]:
    diag, no_cura = c["diag"], c["no_cura"]
    no = diag if diag is not None else no_cura
    if no is None:
        return ["Sem nó de diagnóstico, não há contraste.", ""]
    contraste = no.get("contraste") or (contraste_por_molde(diag) if diag is not None else "")
    partes = ["O contraste registrado na trilha (molde da corrida):", "", *_citacao(contraste), ""] if contraste else []
    alternativas = sorted(no.get("alternativas") or [], key=lambda a: -(a.get("escore") if isinstance(a.get("escore"), (int, float)) else -1))
    if alternativas:
        linhas = []
        for a in alternativas:
            if diag is not None:
                escore = _prob(a.get("escore"))
                nome = f"`{_cel(a.get('opcao'))}` ({_causa_em_palavras(a.get('opcao'), c['leituras'])})"
            else:
                escore = f"{a.get('escore')} de 5 verificações"
                nome = f"`{_cel(a.get('opcao'))}`"
            linhas.append([nome, escore, "sim" if a.get("opcao") == no.get("escolha") else ""])
        partes += [_tabela(["Alternativa", "Probabilidade lida no rótulo" if diag is not None else "Verificações que passou", "Escolhida"], linhas), ""]
    return partes


def _fonte_v3(c: dict) -> list[str]:
    diag, cura = c["diag"], c["cura"]
    if cura is not None and diag is None:
        return ["Não se aplica: a cura de seletor roda sem modelo; nenhum verbete foi citado.", ""]
    fonte = c["decl"].get("fonte")
    valor = _cod(fonte.get("valor")) if fonte and not fonte.get("ausente") else "**a linha não está na resposta**"
    citados = []
    for d in c["citadas"]:
        if d.get("valor") and d["valor"] not in citados:
            citados.append(d["valor"])
    partes = [f"Linha FONTE como veio: {valor}; verbetes citados: " + ("; ".join(_referencia_do_verbete(i, c["leituras"]) for i in citados) or "nenhum") + ".", ""]
    conf_fonte = [v for v in c["sem_gabarito"] if str(v.get("regra", "")).startswith("fonte_") or v.get("regra") == "rotulo_sustentado_por_verbete_do_contexto"]
    if conf_fonte:
        partes += [_tabela(["Conferência em código", "Sobre", "Resultado", "Evidência"],
                           [[ROTULO_DA_REGRA_V3.get(v["regra"], v["regra"]), f"`{_cel(v['alvo'])}`" if v.get("alvo") else "",
                             RESULTADO_EM_PALAVRAS.get(v["resultado"], v["resultado"]), _evidencia(v)] for v in conf_fonte]), ""]
    if c["intervencoes"]:
        partes += [_tabela(["Intervenção", "Verbete", "Rótulo antes", "Rótulo depois", "p antes", "p depois", "Efeito"],
                           [[_cel(i.get("tipo")), f"`{_cel(i.get('verbete'))}`" if i.get("verbete") else "não se aplica", _cel(i.get("rotulo_antes")), _cel(i.get("rotulo_depois")),
                             _prob(i.get("p_antes")), _prob(i.get("p_depois")), _efeito_da_intervencao(i)
                             + (" (só um limite inferior da queda: o rótulo saiu das alternativas devolvidas)" if i.get("limite_inferior") else "")]
                            for i in c["intervencoes"]]), ""]
    else:
        partes += ["Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.", ""]
    return partes


def _acao_v3(c: dict, comando_reexecucao: str | None) -> list[str]:
    cura, inter = c["cura"], c["inter"]
    campo = c["campo"]
    onde = f"`{inter.get('metodo')} {inter.get('caminho')}`" if inter else None
    if cura is not None:
        ap = cura.get("aplicado") or {}
        if cura.get("curado"):
            acao = [f"Sugestão (o agente não altera a aplicação): no passo {cura.get('passo')} do roteiro, trocar o localizador `{_cel(cura.get('localizador'))}` por "
                    f"`{_cel(ap.get('seletor'))}` (estratégia `{ap.get('estrategia')}`)"
                    + (", que resolve o mesmo elemento da referência." if cura.get("mesmo_elemento") else
                       (" e conferir à mão: o roteiro passou, mas com outro elemento, não o alvo da referência." if cura.get("mesmo_elemento") is False else ".")), ""]
        else:
            acao = [(f"Sugestão (o agente não altera a aplicação): nenhum candidato levou o roteiro ao fim no passo {cura.get('passo')} "
                     f"(localizador `{_cel(cura.get('localizador'))}`); o roteiro precisa de um localizador novo escrito à mão. Falha registrada: `{_cel(cura.get('falha'))}`."), ""]
    else:
        acao = [("Confira o campo `" + _cel(campo) + "`" if campo else "Confira a resposta") + (f" em {onde}" if onde else " no caso de entrada")
                + " e compare com o contrato esperado pela interface.", ""]
    acao += [f"Comando para reexecutar o caso: `{comando_reexecucao}`" if comando_reexecucao else "Comando de reexecução: não registrado nesta trilha.", ""]
    return acao


def _resumo_v3(e: dict, blobs: dict) -> str:
    d, tipo = e["dados"], e["tipo"]
    if tipo == "entrada" and not d.get("caso"):
        return f"roteiro {d.get('roteiro')}, passo {d.get('passo')}, localizador {_cel(d.get('localizador'))}" if d.get("roteiro") else "entrada"
    if tipo == "decisao":
        return f"{d.get('decisao')}: escolha {d.get('escolha')}; divergência entre o declarado e o medido: {'sim' if (d.get('divergencia') or {}).get('ha') else 'não'}"
    if tipo == "acao":
        alvo = d.get("url") if d.get("acao") == "abrir" else d.get("seletor")
        return (f"passo {d.get('passo')}: {ACAO_EM_PALAVRAS.get(d.get('acao'), d.get('acao')).lower()} {_cel(alvo)}" + (" (falhou)" if d.get("falhou") else "")
                + (f"; reexecução {d['reexecucao']}" if d.get("reexecucao") else ""))
    if tipo == "prompt":
        return f"{d.get('etapa')}: {d.get('chars')} caracteres; verbetes {', '.join(d.get('verbetes_ids') or [])}"
    return _resumo_do_evento(e, blobs)


def _arvore_v3(c: dict) -> list[str]:
    seq, blobs = c["seq"], c["blobs"]
    linhas = [[str(e["seq"]), str(e.get("passo")), e["tipo"], e["camada"], e["origem"], _cel(e.get("ts")), _resumo_v3(e, blobs)] for e in seq]
    partes = [f"<details><summary>{len(seq)} eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>", "",
              _tabela(["seq", "passo", "Tipo", "Camada", "Origem", "Quando", "Resumo"], linhas), "", "</details>", ""]
    if c["nos"]:
        partes += ["Nós de decisão, na ordem:", ""]
        limpos = True
        for e in c["nos"]:
            d = e["dados"]
            por_evento: dict[tuple, list[str]] = {}
            for x in d.get("evidencia") or []:
                ids = por_evento.setdefault((x["seq"], x.get("papel")), [])
                if x.get("id"):
                    ids.append(f"`{_cel(x['id'])}`")
            ev = "; ".join(f"evento {s} ({p}" + (f": {', '.join(ids)}" if ids else "") + ")" for (s, p), ids in por_evento.items()) or "nenhuma"
            usados = ", ".join(f"`{_cel(u)}`" for u in d.get("prov", {}).get("used") or []) or "nenhum"
            partes += [f"- evento {e['seq']}, decisão `{d.get('decisao')}`: escolha `{_cel(d.get('escolha'))}`; resultado {_cel(d.get('resultado'))}.",
                       f"  - Evidência: {ev}.", f"  - Usou: {usados}."]
            ha, falha = (d.get("divergencia") or {}).get("ha"), d.get("falha")
            if ha or falha:
                limpos = False
                partes.append(f"  - Divergência entre o declarado e o medido: {'sim' if ha else 'não'}; falha: {_cel(falha or 'nenhuma')}.")
        if limpos:
            partes.append("Nenhum nó registrou divergência entre o declarado e o medido, nem falha.")
        partes.append("")
    if c["com_gabarito"]:
        partes += ["### Avaliação contra o gabarito", "", "Esta é a única parte que usa o gabarito do caso; nada acima depende dele.", "",
                   _tabela(["Pergunta", "Respondido", "Esperado", "Resultado"],
                           [[ROTULO_DA_REGRA_V3.get(v["regra"], v["regra"]), f"`{_cel(v['alvo'])}`" if v.get("alvo") else "nada",
                             f"`{_cel((v.get('evidencia') or {}).get('gabarito'))}`" if isinstance(v.get("evidencia"), dict) and v["evidencia"].get("gabarito") else "",
                             RESULTADO_EM_PALAVRAS.get(v["resultado"], v["resultado"])] for v in c["com_gabarito"]]), ""]
    elif c["cura"] is not None and c["diag"] is None:
        partes += ["Sem gabarito nem modelo: a cura de seletor é toda em código; a regra R3 separa o mesmo elemento da referência de outro que fez o roteiro passar.", ""]
    else:
        partes += ["Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.", ""]
    return partes


def relatorio_do_caso_v3(eventos: list[dict], tid: str, comando_reexecucao: str | None = None, pasta_blobs: Path | None = None, leituras: dict | None = None,
                         arquivo_trilha: str | None = None, relatorio_v2: str | None = None) -> str:
    """O relatório de defeito de um caso da trilha v2, no molde da seção 5.5 do CTFL 4.0: os onze campos da 5.5 (severidade, prioridade e
    estado para o analista) e, depois, os seis blocos do v2 em linguagem direta. `leituras` é a camada de leitura (biblioteca_leitura.carregar),
    usada para dizer a causa em palavras e para apontar o arquivo de leitura de cada verbete."""
    c = _contexto_v3(eventos, tid, pasta_blobs, leituras)
    cab, e = c["cab"], c["entrada"]
    classe_nivel = "; ".join(x for x in (_classe_em_palavras(c["classe"]), _nivel_em_palavras(c["nivel"])) if x) or "o caso não tem classe nem nível declarados"
    repeticao = f" (execução {e.get('repeticao')} do cenário `{e.get('cenario_da_fase_5')}`)" if e.get("cenario_da_fase_5") else ""
    identificador = (f"`{tid}`: o caso `{c['caso_id']}` na corrida `{cab.get('corrida')}`{repeticao}; eventos {c['seq'][0]['seq']} a {c['seq'][-1]['seq']} da trilha"
                     + (f" `{arquivo_trilha}`" if arquivo_trilha else "") + f", hash dos eventos `{hash_da_trilha(eventos, tid)}` (a impressão digital destes eventos: "
                     "muda se um byte deles mudar).")
    revisoes = c["por_tipo"].get("revisao", [])
    autor = (f"Observado em {_data_hora(c['ts_entrada'])} (hora do primeiro evento do caso na trilha; a corrida foi de {_data_hora(cab.get('inicio'))} a "
             f"{_data_hora(cab.get('fim'))}). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness "
             f"`executar_fase4.py`, no modo `{c['modo_da_corrida'] or 'não registrado'}`). Autor: o agente (modelo `{cab.get('modelo')}`, "
             f"biblioteca de produção `{cab.get('hash_biblioteca')}`; o resto do ambiente está no bloco 4); "
             + (f"{len(revisoes)} evento(s) de revisão humana nesta trilha." if revisoes else "nenhuma revisão humana registrada nesta trilha: o veredito final é do analista."))
    classe_nivel_curto = "; ".join(x for x in (_classe_em_palavras(c["classe"], curta=True), _nivel_em_palavras(c["nivel"], curta=True)) if x) or classe_nivel
    severidade = (f"{EM_BRANCO}. Para ajudar a decidir, o que o código sabe: {classe_nivel}"
                  + (f"; o roteiro parou no passo {c['passo_falho'].get('passo')}." if c["passo_falho"] else "."))
    prioridade = f"{EM_BRANCO}. A classe e o nível estão na severidade: {classe_nivel_curto}. Confiança do agente: {SELO_EM_PALAVRAS.get(c['selo'], SEM_SELO)}."
    secoes = [
        ("Identificador", [identificador, ""]),
        ("Título", [c["titulo"], ""]),
        ("Data, organização e autor", [autor, ""]),
        ("Objeto de teste e ambiente", _objeto_e_ambiente(c)),
        ("Contexto", _contexto_em_texto(c)),
        ("Descrição para reproduzir", _descricao_para_reproduzir(c, comando_reexecucao)),
        ("Resultado esperado e resultado real", _esperado_e_real(c)),
        ("Severidade", [severidade, ""]),
        ("Prioridade", [prioridade, ""]),
        ("Estado", ["aberto (estado inicial, dado pelo código; o analista muda no hub).", ""]),
        ("Referências", _referencias(c, arquivo_trilha, relatorio_v2, comando_reexecucao, eventos, tid)),
        ("Veredito do agente", _veredito_v3(c)),
        ("Evidência", _evidencia_v3(c)),
        ("Contraste com a segunda causa", _contraste_v3(c)),
        ("FONTE declarada e conferida", _fonte_v3(c)),
        ("Linha de ação", _acao_v3(c, comando_reexecucao)),
        ("Árvore completa", _arvore_v3(c)),
    ]
    assert tuple(n for n, _ in secoes) == CAMPOS_55 + SECOES_MANTIDAS_V3
    partes = [
        ("<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, "
         "no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão."),
        ("     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, "
         "seção 3.1); o hash no fim prova de que eventos ele saiu. -->"),
        f"# Relatório de defeito: {c['titulo']}",
        "",
        f"Caso `{c['caso_id']}` da corrida `{cab.get('corrida')}`; modelo `{cab.get('modelo')}` no Ollama {cab.get('versao_ollama')} (o programa que roda o modelo nesta máquina)"
        + (f"; Playwright {cab.get('playwright')} com o navegador {cab.get('navegador')} (o Playwright controla o navegador, sem janela)" if cab.get("playwright") else "")
        + f"; trilha no esquema v{cab.get('versao_do_esquema', 2)}. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester "
        "Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente "
        "fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.",
        "",
    ]
    for n, (nome, corpo) in enumerate(secoes, start=1):
        partes += [f"## {n}. {nome}", "", *corpo]
    partes += ["## Rastro", "",
               (f"Gerado dos eventos {c['seq'][0]['seq']} a {c['seq'][-1]['seq']} da trilha; hash dos eventos deste caso: `{hash_da_trilha(eventos, tid)}`. "
                "Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`."), ""]
    return "\n".join(partes)


def _indice_v3(pasta: Path, modo: str | None, arquivo_trilha: str, linhas: list[list[str]]) -> str:
    return "\n".join([
        "<!-- ! Alteração de IA - Revisar: índice DERIVADO, gerado por gerar_relatorio_raciocinio.gerar_v3_da_pasta; não editar à mão.",
        "     ! Motivo: um relatório por caso é ilegível sem uma lista que diga a causa, a confiança e o campo de cada um; os relatórios v2 da corrida ficam como estavam. -->",
        f"# Relatórios de defeito (v3) da corrida `{pasta.name}`", "",
        f"{len(linhas)} relatórios no molde da seção 5.5 do CTFL 4.0, gerados da trilha `{arquivo_trilha}`" + (f" (modo `{modo}`)" if modo else "") + ". "
        "Severidade, prioridade e estado estão em branco em todos: são do analista.", "",
        _tabela(["Relatório", "Título", "Causa respondida", "Confiança", "Campo", "Classe e nível"], linhas), ""])


def gerar_v3_da_pasta(pasta: Path, leituras: dict | None = None, check: bool = False) -> dict:
    """Grava (ou, com check, confere) o relatório v3 de cada trilha com nó de decisão da pasta de uma corrida, em `<pasta>/relatorios_v3/`, mais o índice.
    Devolve {pasta, gravados: [nomes], diferentes: [nomes que não batem, só com check]}."""
    pasta = Path(pasta)
    condicoes = json.loads((pasta / "condicoes_fase4.json").read_text(encoding="utf-8")) if (pasta / "condicoes_fase4.json").exists() else {}
    modo = condicoes.get("modo")
    saida = condicoes.get("saida") or pasta.name
    k = condicoes.get("k") or 3
    arquivo_trilha = pasta / f"trilha_{modo}.jsonl" if modo else next(iter(sorted(pasta.glob("trilha_*.jsonl"))), None)
    if arquivo_trilha is None or not arquivo_trilha.exists():
        raise FileNotFoundError(f"trilha da corrida não encontrada em {pasta}")
    eventos = tr.ler(arquivo_trilha)
    destino = pasta / "relatorios_v3"
    arquivos: dict[str, str] = {}
    linhas = []
    for tid, seq in tr.por_trilha(eventos).items():
        if not any(e["tipo"] == "decisao" for e in seq):
            continue
        nome = nome_do_relatorio(tid)
        comando = comando_de_reexecucao(modo, saida, tid, k if isinstance(k, int) else 3)
        v2 = f"../relatorios/{nome}.md" if (pasta / "relatorios" / f"{nome}.md").exists() else None
        arquivos[f"{nome}.md"] = relatorio_do_caso_v3(eventos, tid, comando_reexecucao=comando, pasta_blobs=pasta / "blobs", leituras=leituras,
                                                       arquivo_trilha=arquivo_trilha.name, relatorio_v2=v2)
        c = _contexto_v3(eventos, tid, pasta / "blobs", leituras)
        classe_nivel = ", ".join(x for x in (f"classe {c['classe']}" if c["classe"] is not None else None, f"nível {c['nivel']}" if c["nivel"] is not None else None) if x)
        linhas.append([f"[`{nome}`]({nome}.md)", _cel(c["titulo"]), f"`{_cel(c['escolha'])}`" if c["escolha"] is not None else "nenhuma",
                       _cel(SELO_EM_PALAVRAS.get(c["selo"], "sem selo")), f"`{_cel(c['campo'])}`" if c["campo"] else "nenhum", classe_nivel or "não declarados"])
    arquivos["INDICE.md"] = _indice_v3(pasta, modo, arquivo_trilha.name, linhas)
    diferentes = []
    if check:
        diferentes = [n for n, t in arquivos.items() if not (destino / n).exists() or (destino / n).read_text(encoding="utf-8") != t]
    else:
        destino.mkdir(parents=True, exist_ok=True)
        for n, t in arquivos.items():
            (destino / n).write_text(t, encoding="utf-8", newline="\n")
    return {"pasta": destino, "gravados": list(arquivos), "diferentes": diferentes}


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
    ap.add_argument("--check", action="store_true", help="com --vitrine ou --v3: regera e compara com o que está gravado")
    ap.add_argument("--colar", action="store_true", help="com --vitrine: cola os blocos tb_rac_* no relatório da Pré-Fase 4")
    # ! Alteração de IA - Revisar: (07/11/2026, Pós-Fase 4, Q1) `--v3 --saida <corrida>` grava os relatórios v3 de uma pasta de corrida da Fase 4
    # (`relatorios_v3/`), lendo a camada de leitura se ela existir; com `--check` só confere.
    # ! Motivo: os relatórios das corridas 18d, 21d e 24 são regerados das trilhas gravadas, sem corrida nova (plano da Pós-Fase 4, seção 3.1).
    ap.add_argument("--v3", action="store_true", help="grava os relatórios v3 (molde da seção 5.5 do CTFL 4.0) de uma pasta de corrida da Fase 4")
    ap.add_argument("--saida", help="com --v3: a pasta da corrida em RESULTADOS_DIR (ex.: fase4_tela_v4)")
    ap.add_argument("--corrida")
    ap.add_argument("--modelo", default="qwen2.5:7b")
    ap.add_argument("--versao", type=int, default=1)
    ap.add_argument("--caso")
    args = ap.parse_args()
    print(caminhos.descricao())
    if args.v3:
        if not args.saida:
            ap.error("--v3 pede --saida")
        pasta = caminhos.fase3(args.saida)["raiz"]
        leituras = bl.carregar(bl.PASTA_LEITURA)
        if not leituras:
            print(f"aviso: camada de leitura ausente em {bl.PASTA_LEITURA}; os verbetes saem sem o arquivo de leitura")
        r = gerar_v3_da_pasta(pasta, leituras=leituras or None, check=args.check)
        if args.check:
            if r["diferentes"]:
                print(f"--check: DIFERE ({len(r['diferentes'])} relatório(s) v3 fora de dia em {r['pasta']}: {r['diferentes'][:5]})")
                return 1
            print(f"--check: {len(r['gravados'])} arquivos de {r['pasta']} batem com a trilha")
        else:
            print(f"gravado: {len(r['gravados'])} arquivos em {r['pasta']}")
        return 0
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
