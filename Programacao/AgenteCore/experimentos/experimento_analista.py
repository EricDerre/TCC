#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (11/11/2026, ficha 67 opção b, decisão 121) com a corrida 27, a medida M2 da proposta de desenho do analista de documentação
# (`5-metodo-e-ferramental/proposta-analista-de-documentacao.md`, seções 4.3, 4.4 e 6): um experimento em texto que não muda o agente. Nos 54 casos de aprendizado da
# corrida 20, o modelo é chamado num papel próprio, o de analista de documentação: recebe um prompt novo (instruções fixas, o verbete da causa certa e uma ficha curta do
# caso, montada por código a partir da trilha da corrida 20, com o gabarito no lugar da decisão da pessoa) e devolve uma proposta só, de um de quatro tipos: sinal de busca
# (palavras-chave e sintomas novos num verbete que já existe), nota (uma frase que afirma um fato do sistema), retificação, ou nenhuma. Cada proposta passa, em código, pelos
# dois portões que já existem (o validador da Fase 3 e os filtros da Fase 4) e pelos três novos de `portoes_de_edicao.py` (forma de instrução, filtros de texto e busca).
# Traz a leitura da corrida 20 pela trilha (`casos_da_corrida_20`), a ficha (`ficha_do_caso`), o prompt congelado com hash (`INSTRUCOES`, `prompt_do_analista`), o leitor da
# resposta (`parsear_resposta`), a validação do sinal de busca (`validar_sinal_de_busca`), a cadeia dos portões (`aplicar_portoes`), a prévia sem modelo (`previa`), a corrida
# (`rodar`, modo `analista` de executar_fase4.py) e a leitura contra a corrida 20 (`resumir` e `render`, por avaliar_fase4.py --analista).
# ! Motivo: o Eric aprovou a proposta como base de desenho para depois da Fase 5 e escolheu medir antes, sem tocar no agente, se a entrada própria e uma proposta por caso
# mudam a parcela correta, a abstenção e a forma do texto, com o mesmo modelo e os mesmos casos (é a comparação que a literatura lida não tem). Por isso o código é novo: o
# prompt do diagnóstico e o da proposta de edição de hoje (`estrategias.py`), o validador (`evolucao_biblioteca.py`), os filtros (`biblioteca_fase4.py`), a busca e as
# bibliotecas entram só para leitura. O analista lê a biblioteca de antes do lote da corrida 20 e a resposta que o agente deu naquela corrida, senão o verbete já traria as
# notas dos mesmos casos e a comparação não valeria. A edição entra sempre no verbete da causa certa, que é o único que o analista lê inteiro; o verbete novo fica de fora,
# como a proposta manda. O prompt é peça medida: fica congelado com hash, e a regra das três leituras fica escrita aqui e testada antes de a corrida rodar.
"""Corrida 27 (medida M2): o analista de documentação com a ficha curta do caso, nos 54 casos de aprendizado da corrida 20. Em texto, sem navegador.

Uso (em Programacao/AgenteCore/experimentos, com RESULTADOS_DIR=resultados_alvo):
  python experimento_analista.py --previa [--check]   a prévia sem modelo: as fichas, o tamanho do prompt, a seleção e o prompt inteiro de um caso
                                                      (resultados_alvo/fase4/analista_previa.{json,md})
A corrida roda por rodar_fase4.ps1 -Modo analista -Saida fase4_analista (a fila rodar_fila_pre_fase5.ps1 roda antes a ponte da versão do Ollama e as corridas 25 e 26) e a
leitura por avaliar_fase4.py --analista --saida fase4_analista. A revisão humana às cegas das propostas sai de ferramentas/revisao_propostas.py.
"""
from __future__ import annotations

import argparse
import collections
import copy
import hashlib
import json
import math
import platform
import re
import sys
import time
from pathlib import Path

import analisar_fase3b as a3b
import avaliar
import biblioteca as bib
import biblioteca_fase4 as b4
import caminhos
import corridas_em_texto as ct
import diagnostico_ao_vivo as dv
import evolucao_biblioteca as evo
import executar_bateria
import executar_fase3
import executar_fase3b as e3b
import filtros_de_texto as ft
import medir_prompt_tela as mp
import poda
import portoes_de_edicao as pe
import pre_fase4 as pf
import progresso

CORRIDA = 27
MEDIDA = "M2"
NOME, PREFIXO = "analista", "tb_f4_analista_"
NOME_PREVIA = "analista_previa"
ALFA = 0.05                                    # o corte dos testes exatos, fixado antes da corrida (decisão 121; o mesmo das decisões 116 e 120)
EPOCA = 127                                    # o rótulo das edições desta corrida, para nunca se confundirem com as da corrida 20 (época 101)
ORCAMENTO_DA_FICHA = 400                       # tokens da ficha curta do caso (proposta de desenho, seção 4.3)
OPERACOES = ("sinal_de_busca", "nota", "retificacao")
ABSTENCAO = "nenhuma"
COM_TEXTO = ("nota", "retificacao")           # as operações que escrevem uma frase no verbete; o sinal de busca só acrescenta termos
CAMPOS = ("OPERACAO", "PALAVRAS_CHAVE", "SINTOMAS", "TRECHO", "TEXTO", "MOTIVO")
PORTOES = ("validador", "filtros", "forma", "texto", "busca")
NOME_DO_PORTAO = {"validador": "portão 1, o validador da Fase 3", "filtros": "portão 2, os filtros da Fase 4", "forma": "portão 3, a forma de instrução",
                  "texto": "portão 4, os filtros de texto", "busca": "portão 5, a busca"}
DESTINOS = ("abstenção", "sem proposta válida", "recusada pelo validador da Fase 3", "recusada pelos filtros da Fase 4", "recusada pela forma de instrução",
            "recusada pelos filtros de texto", "recusada pelo portão da busca", "passa nos cinco portões")
CODIGOS_NOVOS = ("sinal_sem_termo_novo",)      # código de recusa que o validador da Fase 3 não tem, porque ele não conhece o sinal de busca
K = ct.K_DO_EXPERIMENTO
MODELO = dv.MODELO_PADRAO
CORRIDA_20 = pe.CORRIDA_20
LIMITE_DE_CITACAO = 19                          # um trecho entre aspas na ficha nunca chega aos 20 caracteres que o filtro da Fase 4 trata como cópia do corpo HTTP
FALHA_DA_LACUNA = "causa_sem_verbete_que_a_trate"
SELOS = {"alto": "alta", "medio": "média", "baixo": "baixa"}
EXEMPLO_DE_FORMA = "O serviço de e-mail responde 202 antes de entregar a mensagem."
LEMBRETE_FINAL = "Responda só com o bloco PROPOSTA, no formato acima."

# As instruções do analista: a parte fixa do prompt, igual em todos os casos e posta na frente, para o Ollama reaproveitar a leitura dela de uma chamada para a outra.
# Os limites de tamanho são os do validador da Fase 3, lidos de lá. O exemplo de forma é de outro sistema, de propósito: se o modelo o copiar, a leitura conta.
INSTRUCOES = f"""Você cuida da documentação de um sistema: uma interface web e a API que ela chama. Um agente de testes usou essa documentação para apontar a causa de uma falha, e uma pessoa conferiu o diagnóstico. Depois destas instruções vêm o verbete da causa certa e a ficha do caso. Diga se o verbete precisa de um acréscimo para que um PRÓXIMO caso parecido, e não este, seja diagnosticado certo.

Escolha UMA saída:
- sinal_de_busca: o verbete já explica a causa, mas a busca não o entregou ao agente. Dê palavras-chave ou sintomas que um caso parecido traria, para a busca achar o verbete.
- nota: falta no verbete um fato sobre o sistema. Escreva a frase como ela vai ficar no verbete.
- retificacao: um trecho do verbete está errado. Copie o trecho igual e escreva a frase certa.
- nenhuma: o verbete já bastava, ou a ficha não mostra o que falta.

Regras:
- O TEXTO é a frase que entra no verbete, escrita como afirmação sobre o sistema. Exemplo de forma, de outro sistema: "{EXEMPLO_DE_FORMA}" Não escreva pedido nem instrução: nada de "Adicionar", "Corrigir", "Incluir" ou "Verificar".
- Fale do sistema e do tipo de falha, em termos gerais. Não copie o sintoma da ficha e não cite o identificador do caso.
- Só cite arquivos, rotas e tabelas que apareçam no verbete.
- TEXTO com {evo.TEXTO_MIN} a {evo.TEXTO_MAX} caracteres, uma ou duas frases, sem lista. MOTIVO com {evo.MOTIVO_MIN} a {evo.MOTIVO_MAX} caracteres: diga qual dado da ficha mostrou a lacuna.
- Uma proposta só.

Formato, exatamente assim:

PROPOSTA
OPERACAO: sinal_de_busca | nota | retificacao | nenhuma
PALAVRAS_CHAVE: <ate {evo.MAX_PALAVRAS_CHAVE_NOVAS} termos novos separados por virgula, ou "nenhuma">
SINTOMAS: <ate {evo.MAX_SINTOMAS_NOVOS} sintomas novos separados por virgula, ou "nenhum">
TRECHO: <so em retificacao: o trecho do verbete que esta errado, copiado igual>
TEXTO: <so em nota e retificacao: a frase como vai ficar no verbete>
MOTIVO: <qual dado da ficha mostrou a lacuna>
FIM"""
HASH_DAS_INSTRUCOES = "cbc4505b3c2052f1"


def hash_das_instrucoes() -> str:
    """O hash da parte fixa do prompt do analista; o teste o compara com `HASH_DAS_INSTRUCOES`, e a corrida o grava nas condições e em cada registro."""
    return hashlib.sha256(INSTRUCOES.encode("utf-8")).hexdigest()[:16]


def prompt_do_analista(ficha: str, verbete: str) -> str:
    """O prompt inteiro de um caso: as instruções fixas, o verbete da causa certa, a ficha do caso e o lembrete do formato. Não continua o prompt do diagnóstico."""
    return (f"{INSTRUCOES}\n\n=====\n\nVERBETE DA CAUSA CERTA (é nele que o acréscimo entra)\n{verbete}\n\n=====\n\n"
            f"FICHA DO CASO (montada por código, a partir do que o agente registrou)\n{ficha}\n\n{LEMBRETE_FINAL}")


_TAXAS: dict = {}


def _taxas() -> dict:
    """As taxas do modelo nesta máquina (`taxas_progresso.json`): caracteres por token, tokens lidos e escritos por segundo. Sem o arquivo, a razão de `biblioteca.py`."""
    if not _TAXAS:
        arq = caminhos.RESULTADOS / "fase4" / "taxas_progresso.json"
        dado = (json.loads(arq.read_text(encoding="utf-8")).get("por_modelo") or {}).get(MODELO) if arq.exists() else None

        def mediana(chave: str, padrao: float | None) -> float | None:
            return ((dado or {}).get(chave) or {}).get("mediana") or padrao

        _TAXAS.update({"chars_por_token": mediana("chars_por_token", bib.CHARS_POR_TOKEN), "prefill": mediana("prefill_tokens_por_s", None), "geracao": mediana("geracao_tokens_por_s", None)})
    return _TAXAS


def tokens_estimados(texto: str) -> int:
    """Os tokens de um texto pela razão de caracteres por token medida nos prompts das corridas vigentes."""
    return round(len(texto) / _taxas()["chars_por_token"])


# ------------------------------------------------------------------ a corrida 20, lida pela trilha

def base_da_corrida_20() -> Path:
    """A biblioteca de antes do lote da corrida 20, que é a que o analista lê e em que cada edição é conferida."""
    return pe.base_da_corrida_20()


def _valor_do_bloco(blocos: dict, nome: str) -> str | None:
    texto = blocos.get(nome)
    return None if texto is None else texto[len(dict(mp.CABECALHOS)[nome]):].strip()


def caso_lido(prompt: str, caso: dict) -> dict:
    """O caso como o diagnóstico da corrida 20 o leu, tirado do prompt gravado: a requisição, o status, o contrato, o corpo, o sintoma e a observação. É o que os filtros
    da Fase 4 usam como evidência do caso; o gabarito vem do banco de casos e só entra nos portões e na leitura."""
    blocos = mp.blocos_do_prompt(prompt)
    status = _valor_do_bloco(blocos, "status")
    entrada = {"requisicao": _valor_do_bloco(blocos, "requisicao") or "", "status": int(status) if status and status.lstrip("-").isdigit() else None,
               "contrato": _valor_do_bloco(blocos, "contrato") or "", "corpo": _valor_do_bloco(blocos, "corpo"), "sintoma": _valor_do_bloco(blocos, "sintoma") or ""}
    for chave, bloco in (("observacao", "observacao"), ("seletor_quebrado", "seletor")):
        valor = _valor_do_bloco(blocos, bloco)
        if valor:
            entrada[chave] = valor
    return {"id": caso["id"], "classe": caso.get("classe"), "nivel": caso.get("nivel"), "entrada": entrada, "gabarito": caso["gabarito"]}


_CORRIDA_20: dict = {}


def casos_da_corrida_20(modelo: str = MODELO) -> list[dict]:
    """Os 54 casos de aprendizado como a corrida 20 os diagnosticou, na ordem dela, lidos da trilha gravada e do banco de casos: a origem (tela ou caso escrito), o
    prompt do diagnóstico, a lista da busca, o nó de decisão (causa, campo, selo, conferências), o corpo HTTP e o registro. Nada é recalculado nem repetido. Para
    (SystemExit) se faltar alguma peça de um caso, porque aí a ficha dele sairia incompleta."""
    if modelo in _CORRIDA_20:
        return _CORRIDA_20[modelo]
    pasta, slug = caminhos.fase3(CORRIDA_20)["raiz"], executar_fase3._slug(modelo)
    particao = e3b._particao_oficial(e3b._oficial())
    aprendizado = {c["id"]: c for c in e3b.TODOS_OS_CASOS if evo.particao_de(particao, c["id"]) == "aprendizado"}
    registros = {str(r["caso"]).split("@")[0]: r for r in executar_bateria.ler_jsonl(pasta / slug / f"diagnosticos__L{dv.VERSAO_CURADA}.jsonl")}
    eventos = executar_bateria.ler_jsonl(pasta / "trilha_biblioteca.jsonl")
    blobs = {e["dados"]["sha"]: e["dados"].get("texto") for e in eventos if e.get("tipo") == "blob" and e.get("dados")}
    prefixo = f"{CORRIDA_20}/{slug}/"
    por_caso: dict[str, dict] = {}
    for e in eventos:
        tid = str(e.get("trilha") or "")
        if not tid.startswith(prefixo):
            continue
        caso_id, _, origem = tid[len(prefixo):].partition("@")
        if origem not in ("tela", "fixture") or caso_id not in aprendizado:
            continue
        d = e.get("dados") or {}
        alvo = por_caso.setdefault(caso_id, {"origem": origem, "tid": tid})
        if e["tipo"] == "candidatos":
            alvo["candidatos"] = d
        elif e["tipo"] == "prompt" and d.get("etapa") == "diagnostico":
            alvo["prompt"] = blobs.get(d.get("sha"))
        elif e["tipo"] == "interceptacao" and d.get("corpo") and "corpo_http" not in alvo:
            alvo["corpo_http"] = blobs.get(d["corpo"])
        elif e["tipo"] == "decisao" and d.get("decisao") == "diagnostico":
            alvo["no"] = d
    verbetes = {v["id"]: v for v in bib.carregar(base_da_corrida_20())}
    itens = []
    for caso_id, reg in registros.items():
        if caso_id not in aprendizado:
            continue
        caso, lido_da_trilha = aprendizado[caso_id], por_caso.get(caso_id) or {}
        faltam = [k for k in ("candidatos", "prompt", "no") if not lido_da_trilha.get(k)]
        if faltam:
            raise SystemExit(f"corrida 20: o caso {caso_id} não tem {', '.join(faltam)} na trilha de {CORRIDA_20}; a ficha dele sairia incompleta")
        g = caso["gabarito"]["causa_raiz"]
        cand, no = lido_da_trilha["candidatos"], lido_da_trilha["no"]
        entregues = list(reg.get("verbetes_ids") or [])
        posicao = next((i["posicao"] for i in cand.get("itens") or [] if i["id"] == g), None)
        acertou = ct.rotulo_lido(reg.get("resposta")) == g
        corpo_http = lido_da_trilha.get("corpo_http") if lido_da_trilha["origem"] == "tela" else None
        if corpo_http is None:
            corpo_http = str(caso["entrada"].get("corpo") or "") or None
        lacuna = (not acertou) or no.get("falha") == FALHA_DA_LACUNA
        ja_registra = g in verbetes and caso_id in b4.casos_do_verbete(verbetes[g])
        itens.append({"caso": caso, "origem": lido_da_trilha["origem"], "tid": lido_da_trilha["tid"], "prompt_do_diagnostico": lido_da_trilha["prompt"],
                      "lido": caso_lido(lido_da_trilha["prompt"], caso), "candidatos": cand, "no": no, "registro": reg, "corpo_http": corpo_http, "entregues": entregues,
                      "posicao_do_ouro": posicao, "ouro_entregue": g in entregues, "acertou": acertou,
                      "selecao": {"lacuna": lacuna, "verbete_ja_registra_o_caso": ja_registra, "seria_chamado": lacuna and not ja_registra}})
    _CORRIDA_20[modelo] = itens
    return itens


# ------------------------------------------------------------------ a ficha curta do caso

_ROTA_COM_ID = re.compile(r"/api/\w+/\d+")
_ROTA_DE_LISTA = re.compile(r"\bGET\s+/api/\w+(?![/\w])")


def _sem_trecho_do_corpo(texto: str, corpo_http: str | None, minimo: int = b4.MIN_CHARS_TRECHO_PROIBIDO) -> str:
    """O texto numa linha só e sem nenhum pedaço literal do corpo HTTP do caso: cada trecho de 20 caracteres ou mais que esteja igual no corpo (a medida do filtro da
    Fase 4 que recusa texto de origem proibida) fica reduzido ao começo dele, seguido de reticências. É o que impede a ficha de entregar ao modelo um trecho que ele
    copiaria para a proposta."""
    texto = re.sub(r"\s+", " ", texto or "").strip()
    corpo = re.sub(r"\s+", " ", corpo_http or "").strip()
    if not corpo:
        return texto
    saida, i = [], 0
    while i < len(texto):
        if len(texto) - i >= minimo and texto[i:i + minimo] in corpo:
            j = i + minimo
            while j < len(texto) and texto[i:j + 1] in corpo:
                j += 1
            saida.append(texto[i:i + LIMITE_DE_CITACAO - 3] + "...")
            i = j
        else:
            saida.append(texto[i])
            i += 1
    return "".join(saida)


def _cortar(texto: str, max_chars: int) -> str:
    """O texto dentro de `max_chars`, cortado no fim de uma frase quando há uma, com a marca de que continua."""
    if len(texto) <= max_chars:
        return texto
    marca = " (...)"
    bruto = texto[: max(0, max_chars - len(marca))]
    fim = max(bruto.rfind(". "), bruto.rfind("; "))
    return (bruto[: fim + 1] if fim > max_chars // 3 else bruto.rstrip()) + marca


def forma_esperada(requisicao: str) -> str | None:
    """A forma que a rota devolve: objeto na rota de detalhe (com id), lista no GET de uma coleção; None quando a requisição não diz."""
    if _ROTA_COM_ID.search(requisicao or ""):
        return "objeto"
    return "lista" if _ROTA_DE_LISTA.search(requisicao or "") else None


def diferenca_contra_o_contrato(contrato: str, corpo: str | None, requisicao: str, status: int | None) -> list[str]:
    """As diferenças do corpo da resposta contra o contrato, medidas em código pela poda do agente (`poda.diff_contrato`) e escritas em frases sem nenhum valor do corpo:
    só nomes de campo, tipos e a forma. É o que a ficha leva no lugar do corpo."""
    if corpo is None:
        return ["não houve resposta" if status is None else "a resposta veio sem corpo"]
    if ":" not in (contrato or ""):
        return ["não medida: o caso não tem contrato de API para comparar"]
    d = poda.diff_contrato(contrato or "", corpo, forma_esperada=forma_esperada(requisicao))
    if d["corpo"] == "vazio":
        return ["a resposta veio vazia"]
    if d["corpo"] == "truncado":
        return ["a resposta veio cortada antes do fim do JSON"]
    if d["corpo"] == "nao_json":
        # no caso escrito o campo do corpo às vezes é uma descrição em palavras ("GET devolveu 14 itens..."), e não um corpo HTTP: só é "não é JSON" o que veio com marcação
        marcado = corpo.strip().startswith("<") or "<html" in corpo.lower()
        return ["a resposta não é JSON: veio como página ou texto com marcação" if marcado else "não medida: o caso descreve a resposta em palavras, sem um corpo para comparar"]
    frases = []
    ausentes: dict = {}
    for x in d["diferencas"]:
        if x["tipo"] == "ausente":
            ausentes.setdefault(x.get("item"), []).append(x["campo"])
    for item, campos in ausentes.items():
        onde = f" no item {item}" if item else ""
        frases.append(f"{'o campo' if len(campos) == 1 else 'os campos'} {', '.join(campos)} {'não veio' if len(campos) == 1 else 'não vieram'}{onde}")
    for x in d["diferencas"]:
        campo, tipo = x.get("campo"), x["tipo"]
        onde = f" no item {x['item']}" if x.get("item") else ""
        if tipo == "renomeado":
            frases.append(f"o campo {x['esperado']} veio com o nome {x['recebido']}{onde}")
        elif tipo == "tipo_diferente":
            frases.append(f"o campo {campo} veio como {x['recebido']} em vez de {x['esperado']}{onde}")
        elif tipo == "fora_do_dominio":
            frases.append(f"o campo {campo} veio com um valor fora do que o contrato aceita{onde}")
        elif tipo == "formato_divergente":
            frases.append(f"o campo {campo} veio em outro formato{onde}")
        elif tipo == "nulo_inesperado":
            frases.append(f"o campo {campo} veio nulo{onde}")
        elif tipo == "inesperado":
            frases.append(f"a resposta trouxe o campo {campo}{onde}, que o contrato não prevê")
        elif tipo == "forma_diferente":
            frases.append(f"a resposta veio como {x['recebido']} em vez de {x['esperado']}")
    if not frases:
        forma = f"uma lista com {d['itens']} itens" if d["forma"] == "lista" else "um objeto" if d["forma"] == "objeto" else "um JSON"
        frases.append(f"nenhuma diferença de campo: a resposta é {forma} com os campos e os tipos do contrato")
    return frases


def ficha_do_caso(item: dict, verbetes: dict[str, dict]) -> str:
    """A ficha curta do caso (proposta de desenho, seção 4.3), montada por código: a requisição e o sintoma como o diagnóstico os leu, a diferença medida contra o
    contrato, os verbetes entregues (identificador e título) e a posição do verbete da causa certa na busca, a resposta do agente (causa, campo e confiança), as
    conferências que não conferiram e a decisão, que nesta corrida sai do gabarito. Ficam de fora o corpo HTTP, a árvore da página, a frase de impacto e a linha FONTE
    do modelo. O sintoma e a observação são cortados para a ficha caber no orçamento de tokens."""
    caso, e, no = item["caso"], item["lido"]["entrada"], item["no"]
    g, corpo_http = caso["gabarito"]["causa_raiz"], item["corpo_http"]

    def titulo(vid: str) -> str:
        return f"[{vid}] {((verbetes.get(vid) or {}).get('meta') or {}).get('titulo', 'verbete fora da biblioteca')}".replace("—", "-")

    posicao = item["posicao_do_ouro"]
    onde = "entre os entregues" if item["ouro_entregue"] else "fora dos entregues"
    busca = (f"BUSCA: entregou ao agente {'; '.join(titulo(v) for v in item['entregues'])}. O verbete da causa certa, [{g}], "
             + (f"ficou na posição {posicao} da busca, {onde}." if posicao else f"não aparece na lista da busca, {onde}."))
    campo_gabarito = caso["gabarito"].get("campo_afetado") or "nenhum"
    diferenca = "; ".join(diferenca_contra_o_contrato(e.get("contrato") or "", corpo_http if item["origem"] == "tela" else e.get("corpo"), e.get("requisicao") or "", e.get("status")))
    fixas = [f"REQUISIÇÃO: {_sem_trecho_do_corpo(e.get('requisicao') or '(não informada)', corpo_http)}"]
    if e.get("status") is not None:
        fixas.append(f"STATUS HTTP: {e['status']}")
    if e.get("seletor_quebrado"):
        fixas.append(f"SELETOR QUE FALHOU: {_sem_trecho_do_corpo(e['seletor_quebrado'], corpo_http)}")
    finais = [f"DIFERENÇA MEDIDA CONTRA O CONTRATO: {diferenca}.", busca,
              f"RESPOSTA DO AGENTE: causa {no.get('escolha') or 'sem causa lida'}; campo {no.get('campo') or 'nenhum'}; confiança {SELOS.get((no.get('confianca') or {}).get('selo'), 'não medida')}.",
              f"CONFERÊNCIAS QUE NÃO CONFERIRAM: {(no.get('divergencia') or {}).get('detalhe') or 'nenhuma'}.",
              f"DECISÃO DE QUEM REVISOU: diagnóstico {'aceito' if item['acertou'] else 'recusado'}. Causa certa: {g}. Campo afetado: {campo_gabarito}."]
    # o sintoma e, no caso escrito, a observação ocupam o que sobra do orçamento; a observação da tela é só o registro interno da poda e não entra
    sobra = int(ORCAMENTO_DA_FICHA * _taxas()["chars_por_token"]) - sum(len(l) + 1 for l in fixas + finais) - len("SINTOMA: ") - 2
    sintoma = _sem_trecho_do_corpo(e.get("sintoma") or "(não informado)", corpo_http)
    observacao = _sem_trecho_do_corpo(e.get("observacao") or "", corpo_http) if item["origem"] == "fixture" else ""
    espaco_da_observacao = min(len(observacao), max(0, sobra // 3)) if observacao else 0
    linhas = [*fixas, f"SINTOMA: {_cortar(sintoma, max(80, sobra - espaco_da_observacao - (len('OBSERVAÇÃO: ') + 1 if observacao else 0)))}"]
    if observacao and espaco_da_observacao >= 40:
        linhas.append(f"OBSERVAÇÃO: {_cortar(observacao, espaco_da_observacao)}")
    return "\n".join(linhas + finais)


# ------------------------------------------------------------------ o leitor da resposta

_RE_INICIO = re.compile(r"^PROPOSTA(\s+\d+)?\s*:?$", re.IGNORECASE)
_RE_FIM = re.compile(r"^FIM\s*\.?$", re.IGNORECASE)
_RE_CAMPO = re.compile(r"^([^\W\d][\w ]*?)\s*:\s*(.*)$")
_VAZIOS = ("", "nenhum", "nenhuma", "n/a", "-")


def _nome_do_campo(candidato: str) -> str:
    return bib.normalizar(candidato).upper().replace(" ", "_")


def parsear_resposta(resposta: str, tokens_saida: int | None = None, teto: int | None = None) -> dict:
    """Lê a resposta do analista: o primeiro bloco PROPOSTA (uma proposta por caso; os outros são contados e ficam de fora), com a operação normalizada e os campos numa
    linha só. `abstencao` é a saída "nenhuma", válida e contada; `malformado` diz por que o bloco não serve (sem bloco, operação fora da lista, campo obrigatório ausente,
    o modelo do formato copiado, resposta cortada pelo teto de tokens). Tolera negrito, crase, acento no nome do campo e campo partido em duas linhas."""
    limpa = (resposta or "").replace("*", "").replace("`", "")
    blocos: list[dict] = []
    bloco: dict | None = None
    aberto: str | None = None
    nenhuma_solta = False
    for bruta in limpa.splitlines():
        linha = bruta.strip()
        if _RE_INICIO.match(linha):
            bloco, aberto = {"campos": {}, "fim": False}, None
            blocos.append(bloco)
            continue
        if bloco is None or bloco["fim"]:
            if bib.normalizar(linha).strip(" .!") in ("nenhuma", "nenhum"):
                nenhuma_solta = True
            m = _RE_CAMPO.match(linha)
            if bloco is None and m and _nome_do_campo(m.group(1)) == "OPERACAO":
                # o modelo esqueceu a linha PROPOSTA e começou pelos campos
                bloco, aberto = {"campos": {}, "fim": False}, None
                blocos.append(bloco)
            else:
                continue
        if _RE_FIM.match(linha):
            bloco["fim"], aberto = True, None
            continue
        m = _RE_CAMPO.match(linha)
        nome = _nome_do_campo(m.group(1)) if m else None
        if nome in CAMPOS:
            bloco["campos"][nome] = m.group(2).strip()
            aberto = nome
        elif aberto and linha:
            bloco["campos"][aberto] = (bloco["campos"][aberto] + " " + linha).strip()
    truncada = bool(tokens_saida is not None and teto is not None and tokens_saida >= teto and not limpa.rstrip().upper().endswith(("FIM", "NENHUMA", "NENHUMA.")))
    saida = {"operacao": None, "abstencao": False, "malformado": None, "campos": {}, "blocos": len(blocos), "fim_ausente": bool(blocos) and not blocos[0]["fim"], "truncada": truncada}
    if not blocos:
        if nenhuma_solta:
            return {**saida, "abstencao": True}
        return {**saida, "malformado": "sem bloco PROPOSTA e sem a palavra NENHUMA"}
    campos = {k: re.sub(r"\s+", " ", v).strip() for k, v in blocos[0]["campos"].items()}
    bruta_op = campos.get("OPERACAO", "")
    if "|" in bruta_op:
        return {**saida, "campos": campos, "malformado": "a OPERACAO copia o modelo do formato, com as quatro opções"}
    operacao = bib.normalizar(bruta_op).strip(" .").replace(" ", "_")
    if operacao in ("nenhuma", "nenhum"):
        return {**saida, "campos": campos, "abstencao": True}
    if truncada and saida["fim_ausente"]:
        return {**saida, "campos": campos, "malformado": "resposta cortada pelo teto de tokens antes do FIM"}
    if operacao not in OPERACOES:
        return {**saida, "campos": campos, "malformado": f"OPERACAO '{bruta_op}' fora de {', '.join(OPERACOES)} e nenhuma"}
    uteis = {k: v for k, v in campos.items() if k != "OPERACAO" and not (k in ("TRECHO", "TEXTO") and bib.normalizar(v).strip(" .") in _VAZIOS)}
    if operacao == OPERACOES[0]:
        uteis.pop("TEXTO", None)
        uteis.pop("TRECHO", None)
        if not evo._lista_de_campo(uteis.get("PALAVRAS_CHAVE", ""), normalizar=True) and not evo._lista_de_campo(uteis.get("SINTOMAS", ""), normalizar=True):
            return {**saida, "operacao": operacao, "campos": uteis, "malformado": "sinal de busca sem PALAVRAS_CHAVE e sem SINTOMAS"}
    else:
        if not uteis.get("TEXTO"):
            return {**saida, "operacao": operacao, "campos": uteis, "malformado": f"{operacao} sem TEXTO"}
        if operacao == "retificacao" and not uteis.get("TRECHO"):
            return {**saida, "operacao": operacao, "campos": uteis, "malformado": "retificacao sem TRECHO"}
        if operacao == "nota":
            uteis.pop("TRECHO", None)
    return {**saida, "operacao": operacao, "campos": uteis}


# ------------------------------------------------------------------ os portões em código

def contexto_dos_portoes(modelo: str = MODELO) -> dict:
    """O que os cinco portões precisam, carregado uma vez: a biblioteca de antes do lote da corrida 20 (só lida), a busca dos casos com gabarito sobre ela, os limiares
    dos filtros de texto, os 90 casos oficiais (o validador da Fase 3 confere a proposta contra todos) e o contexto dos filtros da Fase 4 (as parcelas da calibração
    para a regra dos 40%, o código das cobaias e as rotas)."""
    base = base_da_corrida_20()
    verbetes = bib.carregar(base)
    slug = executar_fase3._slug(modelo)
    calibracao = executar_bateria.ler_jsonl(caminhos.RESULTADOS / "fase4_calibracao" / f"k{K}" / slug / f"diagnosticos__L{dv.VERSAO_CURADA}.jsonl")
    return {"base": base, "hash_da_base": evo.hash_biblioteca(base), "verbetes": verbetes, "por_id": {v["id"]: v for v in verbetes}, "busca": pe.BuscaDosCasos(base),
            "limiares_texto": ft.carregar_limiares(), "casos": list(e3b.TODOS_OS_CASOS), "modelo": modelo, "epoca": EPOCA, "k": K,
            "filtros": {"parcelas": b4.parcela_nos_contextos(calibracao), "corrigidos": {}, "casos_da_rodada": {i["caso"]["id"] for i in casos_da_corrida_20(modelo)},
                        "fontes": b4.fontes_das_cobaias(), "rotas": b4.rotas_do_openapi(), "data": time.strftime("%Y-%m-%d")}}


def validar_sinal_de_busca(campos: dict, lido: dict, ouro: dict, ctx: dict) -> dict:
    """O portão 1 para o sinal de busca, que o validador da Fase 3 não conhece: as mesmas conferências dele que valem para uma edição sem texto, na mesma ordem e com
    os mesmos códigos (o MOTIVO, os itens das listas, a cópia do caso e a biblioteca válida depois da edição), mais uma: o sinal tem de trazer ao menos um termo que o
    verbete ainda não tenha. Devolve aceita, motivo (o código), detalhe e a edição."""
    motivo = evo._uma_linha(campos.get("MOTIVO", ""))
    if not motivo:
        return evo._rejeitar("motivo_ausente", "proposta sem MOTIVO")
    if len(motivo) < evo.MOTIVO_MIN:
        return evo._rejeitar("motivo_curto", f"MOTIVO com {len(motivo)} caracteres (mínimo {evo.MOTIVO_MIN})")
    if len(motivo) > evo.MOTIVO_MAX:
        return evo._rejeitar("motivo_longo", f"MOTIVO com {len(motivo)} caracteres (máximo {evo.MOTIVO_MAX})")
    palavras = evo._lista_de_campo(campos.get("PALAVRAS_CHAVE", ""), normalizar=True)
    sintomas = evo._lista_de_campo(campos.get("SINTOMAS", ""), normalizar=True)
    if len(palavras) > evo.MAX_PALAVRAS_CHAVE_NOVAS:
        return evo._rejeitar("palavra_chave_invalida", f"{len(palavras)} palavras-chave (teto {evo.MAX_PALAVRAS_CHAVE_NOVAS})")
    if len(sintomas) > evo.MAX_SINTOMAS_NOVOS:
        return evo._rejeitar("palavra_chave_invalida", f"{len(sintomas)} sintomas (teto {evo.MAX_SINTOMAS_NOVOS})")
    for item in palavras + sintomas:
        if len(item) > evo.MAX_CHARS_ITEM_LISTA or not evo.ITEM_LISTA_RE.match(item):
            return evo._rejeitar("palavra_chave_invalida", f"item de lista inválido: '{item}'")
    novas_palavras = evo._itens_a_acrescentar(ouro["meta"].get("palavras_chave", []), palavras)
    novos_sintomas = evo._itens_a_acrescentar(ouro["meta"].get("sintomas", []), sintomas)
    if not novas_palavras and not novos_sintomas:
        return evo._rejeitar(CODIGOS_NOVOS[0], f"[{ouro['id']}] já tem todos os termos propostos")
    if evo.CASO_ID_RE.search(motivo):
        return evo._rejeitar("copia_do_caso", "o MOTIVO cita o id de um caso do banco")
    proposta = bib._shingles(bib.tokens(" ".join([motivo, *palavras, *sintomas])))
    if len(proposta) >= 5:
        for caso in ctx["casos"]:
            do_caso = evo._shingles_do_caso(caso)
            if do_caso and len(proposta & do_caso) / len(proposta) >= evo.LIMIAR_COPIA_PROPOSTA:
                return evo._rejeitar("copia_do_caso", f"{len(proposta & do_caso) / len(proposta):.0%} dos 5-gramas da proposta são do caso {caso['id']}")
    modificados = copy.deepcopy(ctx["verbetes"])
    alvo = next(v for v in modificados if v["id"] == ouro["id"])
    for chave, novos in (("palavras_chave", novas_palavras), ("sintomas", novos_sintomas)):
        if novos:
            alvo["meta"][chave] = list(alvo["meta"].get(chave, [])) + novos
    problemas = bib.validar(modificados, ctx["casos"], teto_global=None)
    if problemas:
        rotulo = f"{alvo['pasta']}/{alvo['caminho'].name}"
        return evo._rejeitar("biblioteca_invalida", next((p for p in problemas if rotulo in p), problemas[0]))
    edicao = {"epoca": ctx["epoca"], "caso": lido["id"], "numero": 1, "operacao": OPERACOES[0], "verbete": ouro["id"], "arquivo": ouro["caminho"].relative_to(ctx["base"]).as_posix(),
              "texto": "", "motivo": motivo, "trecho": None, "palavras_chave_novas": palavras, "sintomas_novos": sintomas, "novo": None, "modelo": ctx["modelo"]}
    return {"aceita": True, "motivo": None, "detalhe": f"{OPERACOES[0]} em [{ouro['id']}]", "edicao": edicao}


def aplicar_portoes(parseado: dict, item: dict, ctx: dict) -> dict:
    """A proposta de um caso pelos cinco portões, na ordem da proposta de desenho: o validador da Fase 3 (ou a validação do sinal de busca), os filtros da Fase 4, a
    forma de instrução, os filtros de texto e a busca. O destino é o primeiro portão que recusa; os portões 3 e 4 leem o texto e são medidos sempre que a proposta tem
    texto, e o portão 5 sempre que ela vira edição, mesmo quando um portão anterior recusa, para a leitura saber o que cada um faria sozinho. Cada proposta é conferida
    contra a biblioteca de antes do lote, sem acumular as edições dos outros casos. A abstenção e a resposta sem bloco não chegam aos portões."""
    portoes: dict = dict.fromkeys(PORTOES)
    saida = {"destino": None, "parou_em": None, "codigo": None, "detalhe": None, "edicao": None, "portoes": portoes, "passa_nos_filtros_de_hoje": False, "passa_nos_cinco": False,
             "para_revisao": False}
    if parseado["abstencao"]:
        return {**saida, "destino": DESTINOS[0]}
    if parseado["malformado"]:
        return {**saida, "destino": DESTINOS[1], "parou_em": "formato", "codigo": "bloco_malformado" if parseado["blocos"] else "sem_bloco", "detalhe": parseado["malformado"]}
    operacao, campos, caso = parseado["operacao"], parseado["campos"], item["caso"]
    ouro = ctx["por_id"][caso["gabarito"]["causa_raiz"]]
    antigos = {"OPERACAO": operacao, "VERBETE": ouro["id"], "TRECHO": campos.get("TRECHO", ""), "TEXTO": campos.get("TEXTO", ""), "MOTIVO": campos.get("MOTIVO", ""),
               "PALAVRAS_CHAVE": campos.get("PALAVRAS_CHAVE", "nenhuma"), "SINTOMAS": campos.get("SINTOMAS", "nenhum")}
    if operacao in COM_TEXTO:
        portoes["forma"] = pe.portao_da_forma(antigos["TEXTO"])
        portoes["texto"] = pe.portao_do_texto(antigos["TEXTO"], ctx["limiares_texto"])
        v1 = evo.validar_proposta({"numero": 1, "campos": antigos, "malformado": None},
                                  {"raiz": ctx["base"], "verbetes": ctx["verbetes"], "casos": ctx["casos"], "ids_visiveis": {ouro["id"]}, "epoca": ctx["epoca"], "caso_id": caso["id"],
                                   "modelo": ctx["modelo"], "novos_nesta_epoca": 0, "aceitas_no_caso": 0, "k": ctx["k"]})
    else:
        v1 = validar_sinal_de_busca(campos, item["lido"], ouro, ctx)
    portoes["validador"] = {"passa": bool(v1["aceita"]), "codigo": v1["motivo"], "detalhe": v1["detalhe"]}
    edicao = v1["edicao"]
    if edicao:
        v2 = b4.filtrar_proposta(antigos, edicao, item["lido"], ouro, {**ctx["filtros"], "corpo_http": item["corpo_http"], "pesos_usados": {}})
        portoes["filtros"] = {"passa": bool(v2["aceita"]), "codigo": v2["codigo"], "filtro": v2["filtro"], "detalhe": v2["detalhe"], "para_revisao": bool(v2["para_revisao"])}
        portoes["busca"] = pe.portao_da_busca(ctx["busca"], edicao)
    parou = next((p for p in PORTOES if portoes[p] is not None and not portoes[p]["passa"]), None)
    nos_filtros = bool(portoes["validador"]["passa"] and portoes["filtros"] and portoes["filtros"]["passa"])
    codigo = detalhe = None
    if parou in ("validador", "filtros"):
        codigo, detalhe = portoes[parou]["codigo"], portoes[parou]["detalhe"]
    elif parou in ("forma", "busca"):
        codigo, detalhe = parou, portoes[parou]["motivo"]
    elif parou == "texto":
        codigo, detalhe = "texto", "reprova em: " + ", ".join(portoes["texto"]["reprovados"])
    return {**saida, "destino": DESTINOS[2 + PORTOES.index(parou)] if parou else DESTINOS[-1], "parou_em": parou, "codigo": codigo, "detalhe": detalhe, "edicao": edicao,
            "passa_nos_filtros_de_hoje": nos_filtros, "passa_nos_cinco": parou is None, "para_revisao": bool(portoes["filtros"] and portoes["filtros"]["para_revisao"])}


def copia_o_exemplo(texto: str) -> bool:
    """A proposta repete o exemplo de forma das instruções (que é de outro sistema): metade ou mais dos trigramas do texto estão nele."""
    return bool(texto) and b4.similaridade_ngramas(texto, EXEMPLO_DE_FORMA) >= 0.5


# ------------------------------------------------------------------ os testes exatos e a regra

def fisher_exato(a: int, b: int, c: int, d: int) -> float:
    """O p bilateral do teste exato de Fisher para a tabela 2 por 2 [[a, b], [c, d]]: a soma das probabilidades das tabelas com as mesmas margens que são tão ou menos
    prováveis que a observada. É o teste das duas leituras que não têm par caso a caso (a forma do texto e a parcela correta)."""
    n = a + b + c + d
    if n == 0:
        return 1.0
    linha, coluna = a + b, a + c

    def prob(x: int) -> float:
        return math.comb(coluna, x) * math.comb(n - coluna, linha - x) / math.comb(n, linha)

    observada = prob(a)
    total = sum(p for p in (prob(x) for x in range(max(0, linha - (n - coluna)), min(linha, coluna) + 1)) if p <= observada * (1 + 1e-9))
    return round(min(1.0, total), 4)


def texto_da_regra() -> str:
    corte = f"{ALFA:.2f}".replace(".", ",")
    return (f"Regra fixada antes da corrida (decisão 121). Três leituras contra a corrida 20, cada uma com um teste exato bilateral e o corte de {corte}. A abstenção: os casos "
            "em que o modelo responde que não há o que acrescentar, pareados caso a caso com a corrida 20 (McNemar). A forma do texto: a parcela das propostas com texto que "
            "afirmam um fato, isto é, que passam no portão da forma de instrução, contra a mesma conta nas propostas da corrida 20 (Fisher). A parcela correta: entre as "
            "propostas que passam nos filtros de hoje, as que a revisão humana às cegas julga corretas, contra as edições da corrida 20 (Fisher); essa leitura só tem veredito "
            "depois da revisão. Vale com a corrida completa e a ponte da versão do Ollama pareável com a Fase 3 (b + c até 2, decisão 47). Nenhum resultado muda o agente: a "
            "proposta do analista de documentação é base de desenho para depois da Fase 5.")


def _veredito(p: float | None, completo: bool, pareavel: bool | None, maior: bool, mais: str, menos: str) -> str:
    if not completo:
        return "sem veredito: a corrida não cobriu todos os casos previstos"
    if pareavel is None:
        return "sem veredito: a versão do Ollama desta corrida não tem ponte registrada, e a corrida 20 rodou em outra versão"
    if not pareavel:
        return "sem veredito: a ponte da versão do Ollama desta corrida não é pareável com a Fase 3, e a comparação com a corrida 20 não vale"
    if p is None:
        return "sem veredito: falta a revisão humana às cegas das propostas"
    if p < ALFA:
        return f"sai do ruído: {mais if maior else menos} na corrida {CORRIDA}"
    return "dentro do ruído"


# ------------------------------------------------------------------ a leitura

def comparacao_com_a_corrida_20(modelo: str = MODELO) -> dict:
    """Os números da corrida 20 que a leitura compara, tirados dos registros dela: as propostas, a abstenção por caso, a forma do texto pelo mesmo portão 3, as edições
    que passaram nos filtros e o veredito da revisão humana do lote, e o custo de cada chamada."""
    propostas = pe.propostas_da_corrida_20()
    pasta = caminhos.fase3(CORRIDA_20)["raiz"]
    registros = executar_bateria.ler_jsonl(pasta / executar_fase3._slug(modelo) / "propostas__E101.jsonl")
    revisadas = [p for p in propostas if p["veredito"]]
    return {"casos": len(registros), "propostas": len(propostas), "abstencoes": sum(1 for r in registros if r.get("abstencao")), "passaram_nos_filtros": len(revisadas),
            "com_texto": len(propostas), "afirmacoes": sum(1 for p in propostas if pe.portao_da_forma(p["texto"])["passa"]),
            "por_veredito": {v: sum(1 for p in revisadas if p["veredito"] == v) for v in pe.VEREDITOS},
            "por_operacao": dict(sorted(collections.Counter(str(p["operacao"]) for p in propostas).items())),
            "tokens_entrada_mediana": ct._mediana([r.get("tokens_entrada") for r in registros]), "tokens_saida_mediana": ct._mediana([r.get("tokens_saida") for r in registros]),
            "segundos_mediana": ct._mediana([r.get("segundos") for r in registros]), "versao_ollama": sorted({str(r.get("versao_ollama")) for r in registros}),
            "abstencao_por_caso": {r["caso"]: bool(r.get("abstencao")) for r in registros}}


def _de(parte: int, total: int) -> str:
    return f"{parte} de {total}"


def resumir(registros: list[dict], corrida20: dict, condicoes: dict | None, ponte: dict | None = None, corrida: str | None = None, gerado_em: str | None = None,
            revisao: dict | None = None) -> dict:
    """A corrida 27 contra a corrida 20: o que o analista respondeu por caso (abstenção, tipo de proposta, forma do texto), o que os cinco portões fizeram com cada
    proposta, o custo, e as três leituras da regra fixada antes. `revisao`, quando existe, traz o veredito de cada proposta revisada às cegas (`origem` 27 ou 20)."""
    condicoes = condicoes or {}
    propostas = [r for r in registros if r.get("operacao") and not r.get("malformado")]
    com_texto = [r for r in propostas if r["operacao"] in COM_TEXTO]
    afirmacoes = [r for r in com_texto if (r["portoes"].get("forma") or {}).get("passa")]
    abstencoes = [r for r in registros if r.get("abstencao")]
    para_revisao = [r for r in propostas if r.get("passa_nos_filtros_de_hoje")]
    previstos = condicoes.get("casos") or len(registros)
    completo = len(registros) == previstos and previstos > 0 and not condicoes.get("parcial")
    versao = condicoes.get("versao_ollama")
    da_condicao = condicoes.get("versao_ollama_da_corrida_20") or []
    versoes20 = set(corrida20.get("versao_ollama") or []) or set([da_condicao] if isinstance(da_condicao, str) else da_condicao)
    mesma_versao = versao is not None and versoes20 == {versao}
    pareavel = True if mesma_versao else (bool(ponte.get("pareavel")) if ponte else None)
    por_caso_20 = corrida20.get("abstencao_por_caso") or {}
    b = sum(1 for r in registros if r.get("abstencao") and not por_caso_20.get(r["caso"], False))
    c = sum(1 for r in registros if not r.get("abstencao") and por_caso_20.get(r["caso"], False))
    p_abstencao = avaliar.mcnemar_exato(b, c)
    p_forma = fisher_exato(len(afirmacoes), len(com_texto) - len(afirmacoes), corrida20["afirmacoes"], corrida20["com_texto"] - corrida20["afirmacoes"])
    parcela_27 = len(afirmacoes) / len(com_texto) if com_texto else 0.0
    parcela_20 = corrida20["afirmacoes"] / corrida20["com_texto"] if corrida20["com_texto"] else 0.0
    bloco_revisao, p_correta, correta_27, correta_20, maior_correta = None, None, "sem revisão", _de(corrida20["por_veredito"]["Correta"], corrida20["passaram_nos_filtros"]), False
    if revisao:
        vistos = {i["caso"]: i["veredito"] for i in revisao.get("itens") or [] if i.get("origem") == str(CORRIDA) and i.get("veredito") in pe.VEREDITOS}
        do_20 = [i["veredito"] for i in revisao.get("itens") or [] if i.get("origem") == "20" and i.get("veredito") in pe.VEREDITOS]
        v27 = {v: sum(1 for r in para_revisao if vistos.get(r["caso"]) == v) for v in pe.VEREDITOS}
        v20 = {v: do_20.count(v) for v in pe.VEREDITOS} if do_20 else None
        pendentes = sum(1 for r in para_revisao if r["caso"] not in vistos)
        base20 = v20 or corrida20["por_veredito"]
        n27, n20 = sum(v27.values()), sum(base20.values())
        correta_27, correta_20 = _de(v27["Correta"], n27), _de(base20["Correta"], n20)
        if pendentes == 0 and n27:
            p_correta = fisher_exato(v27["Correta"], n27 - v27["Correta"], base20["Correta"], n20 - base20["Correta"])
            maior_correta = v27["Correta"] / n27 > (base20["Correta"] / n20 if n20 else 0.0)
        contra = []
        for portao in ("forma", "texto", "busca"):
            avaliadas = [r for r in para_revisao if r["caso"] in vistos and r["portoes"].get(portao) is not None]
            contra.append({"portao": portao, "nome": NOME_DO_PORTAO[portao], "avaliadas": len(avaliadas),
                           **{v: {"recusa": sum(1 for r in avaliadas if vistos[r["caso"]] == v and not r["portoes"][portao]["passa"]),
                                  "passa": sum(1 for r in avaliadas if vistos[r["caso"]] == v and r["portoes"][portao]["passa"])} for v in pe.VEREDITOS}})
        bloco_revisao = {"quem": revisao.get("quem"), "revisadas": n27, "pendentes": pendentes, f"corrida_{CORRIDA}": v27, "corrida_20_pelo_mesmo_revisor": v20,
                         "corrida_20_na_revisao_do_lote": corrida20["por_veredito"], "portoes_contra_a_revisao": contra,
                         "passam_nos_cinco_por_veredito": {v: sum(1 for r in para_revisao if vistos.get(r["caso"]) == v and r.get("passa_nos_cinco")) for v in pe.VEREDITOS}}
    leituras = [
        {"leitura": "abstencao", "nome": "abstenção", "teste": "McNemar pareado por caso", f"corrida_{CORRIDA}": _de(len(abstencoes), len(registros)),
         "corrida_20": _de(corrida20["abstencoes"], corrida20["casos"]), "b": b, "c": c, "p": p_abstencao,
         "veredito": _veredito(p_abstencao, completo, pareavel, b > c, "mais abstenção", "menos abstenção")},
        {"leitura": "forma", "nome": "forma do texto", "teste": "Fisher", f"corrida_{CORRIDA}": _de(len(afirmacoes), len(com_texto)),
         "corrida_20": _de(corrida20["afirmacoes"], corrida20["com_texto"]), "p": p_forma,
         "veredito": _veredito(p_forma, completo, pareavel, parcela_27 > parcela_20, "mais afirmações", "menos afirmações")},
        {"leitura": "parcela_correta", "nome": "parcela correta", "teste": "Fisher", f"corrida_{CORRIDA}": correta_27, "corrida_20": correta_20, "p": p_correta,
         "veredito": _veredito(p_correta, completo, pareavel, maior_correta, "parcela correta maior", "parcela correta menor")}]

    def conta(sub: list[dict]) -> dict:
        return {"casos": len(sub), "abstencoes": sum(1 for r in sub if r.get("abstencao")), "sem_bloco": sum(1 for r in sub if r.get("malformado")),
                "propostas": sum(1 for r in sub if r.get("operacao") and not r.get("malformado")), "passam_nos_filtros_de_hoje": sum(1 for r in sub if r.get("passa_nos_filtros_de_hoje")),
                "passam_nos_cinco": sum(1 for r in sub if r.get("passa_nos_cinco"))}

    por_portao = []
    for portao in PORTOES:
        avaliadas = [r for r in propostas if r["portoes"].get(portao) is not None]
        por_portao.append({"portao": portao, "nome": NOME_DO_PORTAO[portao], "avaliadas": len(avaliadas), "recusa": sum(1 for r in avaliadas if not r["portoes"][portao]["passa"]),
                           "passa": sum(1 for r in avaliadas if r["portoes"][portao]["passa"]), "nao_se_aplica": len(propostas) - len(avaliadas),
                           "parou_aqui": sum(1 for r in propostas if r.get("parou_em") == portao)})
    codigos = collections.Counter((r.get("parou_em") or "", r.get("codigo") or "") for r in registros if r.get("parou_em"))
    return {"metadados": {"gerado_em": gerado_em or time.strftime("%Y-%m-%dT%H:%M:%S"), "corrida": corrida, "numero": CORRIDA, "medida": MEDIDA}, "condicoes": condicoes,
            "regra": {"alfa": ALFA, "texto": texto_da_regra(), "pareavel": pareavel, "mesma_versao_da_corrida_20": mesma_versao, "ponte": ponte},
            "resumo": {"casos": len(registros), "previstos": previstos, "completo": completo, "abstencoes": len(abstencoes), "sem_bloco": sum(1 for r in registros if r.get("malformado")),
                       "propostas": len(propostas), "por_operacao": {o: sum(1 for r in propostas if r["operacao"] == o) for o in OPERACOES}, "com_texto": len(com_texto),
                       "afirmacoes": len(afirmacoes), "passam_nos_filtros_de_hoje": len(para_revisao), "passam_nos_cinco": sum(1 for r in propostas if r.get("passa_nos_cinco")),
                       "vao_para_a_revisao": len(para_revisao), "copias_do_exemplo": sum(1 for r in registros if r.get("copia_do_exemplo")),
                       "blocos_a_mais": sum(1 for r in registros if (r.get("blocos") or 0) > 1), "respostas_cortadas": sum(1 for r in registros if r.get("truncada")),
                       "tokens_entrada_mediana": ct._mediana([r.get("tokens_entrada") for r in registros]), "tokens_saida_mediana": ct._mediana([r.get("tokens_saida") for r in registros]),
                       "segundos_mediana": ct._mediana([r.get("segundos") for r in registros]), "segundos_no_total": round(sum(r.get("segundos") or 0 for r in registros), 1),
                       "ficha_tokens_mediana": ct._mediana([r.get("ficha_tokens") for r in registros])},
            "corrida_20": {k: v for k, v in corrida20.items() if k != "abstencao_por_caso"},
            "leituras": leituras, "revisao": bloco_revisao, "por_portao": por_portao,
            "por_destino": [{"destino": d, "casos": sum(1 for r in registros if r.get("destino") == d)} for d in DESTINOS],
            "por_lacuna": [{"grupo": nome, **conta([r for r in registros if bool((r.get("selecao") or {}).get("lacuna")) is valor])} for nome, valor in (("com lacuna", True), ("sem lacuna", False))],
            "por_origem": [{"origem": o, **conta([r for r in registros if r.get("origem") == o])} for o in sorted({str(r.get("origem")) for r in registros})],
            "por_acerto": [{"grupo": nome, **conta([r for r in registros if bool(r.get("acertou_diagnostico")) is valor])}
                           for nome, valor in (("diagnóstico certo", True), ("diagnóstico errado", False))],
            "codigos": [{"portao": p, "codigo": c_, "casos": n} for (p, c_), n in sorted(codigos.items(), key=lambda x: (-x[1], x[0]))],
            "casos": [{"caso": r["caso"], "origem": r.get("origem"), "acertou_diagnostico": r.get("acertou_diagnostico"), "lacuna": bool((r.get("selecao") or {}).get("lacuna")),
                       "operacao": r.get("operacao"), "abstencao": bool(r.get("abstencao")), "destino": r.get("destino"), "parou_em": r.get("parou_em"), "codigo": r.get("codigo"),
                       "forma_passa": (r["portoes"].get("forma") or {}).get("passa") if r.get("portoes") else None, "texto": (r.get("campos") or {}).get("TEXTO", ""),
                       "termos": ", ".join(x for x in ((r.get("campos") or {}).get("PALAVRAS_CHAVE", ""), (r.get("campos") or {}).get("SINTOMAS", ""))
                                           if x and bib.normalizar(x) not in _VAZIOS) if r.get("operacao") == OPERACOES[0] else "",
                       "tokens_entrada": r.get("tokens_entrada"), "tokens_saida": r.get("tokens_saida"), "segundos": r.get("segundos")} for r in registros]}


def _n(v) -> str:
    """O número como vai ao texto: a mediana que é um inteiro sai sem a casa decimal."""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return ct._n(v)


def render(dado: dict) -> str:
    r, regra, c20, cond = dado["resumo"], dado["regra"], dado["corrida_20"], dado.get("condicoes") or {}
    n, p = _n, ct._p
    ponte = regra.get("ponte")
    if regra.get("mesma_versao_da_corrida_20"):
        sobre_a_ponte = "A corrida rodou na mesma versão do Ollama da corrida 20, e a ponte não entra."
    elif ponte:
        sobre_a_ponte = (f"A corrida rodou em outra versão do Ollama que a corrida 20; a ponte dessa versão (`{ponte.get('corrida')}`) deu b = {n(ponte.get('b'))} e c = {n(ponte.get('c'))} em "
                         f"{n(ponte.get('n'))} casos, {'pareável' if ponte.get('pareavel') else 'não pareável'} com a Fase 3 (limite {n(ponte.get('limite'))}).")
    else:
        sobre_a_ponte = "A corrida rodou em outra versão do Ollama que a corrida 20, e essa versão não tem ponte registrada."
    op = r["por_operacao"]
    texto = [(f"Medida {MEDIDA} da proposta do analista de documentação (corrida {CORRIDA}, decisão 121). Nos casos de aprendizado da corrida 20, o modelo foi chamado no papel de "
              "analista de documentação: recebeu as instruções próprias (hash "
              f"`{cond.get('hash_das_instrucoes')}`), o verbete da causa certa e a ficha curta do caso, montada por código a partir da trilha da corrida 20, com o gabarito no lugar da decisão "
              "da pessoa, e devolveu uma proposta só. A biblioteca é a de antes do lote da corrida 20 e só foi lida; nada do agente mudou."),
             "", regra["texto"], "", sobre_a_ponte,
             "", (f"O que o analista respondeu em {n(r['casos'])} casos: {n(r['abstencoes'])} abstenções, {n(r['sem_bloco'])} respostas sem proposta válida e {n(r['propostas'])} propostas "
                  f"({n(op['sinal_de_busca'])} sinais de busca, {n(op['nota'])} notas e {n(op['retificacao'])} retificações). Das {n(r['com_texto'])} propostas com texto, "
                  f"{n(r['afirmacoes'])} afirmam um fato e passam no portão da forma; na corrida 20 eram {n(c20['afirmacoes'])} de {n(c20['com_texto'])}. Passam nos filtros de hoje "
                  f"{n(r['passam_nos_filtros_de_hoje'])} (na corrida 20, {n(c20['passaram_nos_filtros'])} de {n(c20['propostas'])}), e nos cinco portões {n(r['passam_nos_cinco'])}. Cada "
                  f"chamada leu {n(r['tokens_entrada_mediana'])} tokens e escreveu {n(r['tokens_saida_mediana'])} na mediana, em {n(r['segundos_mediana'])} s; na corrida 20 eram "
                  f"{n(c20['tokens_entrada_mediana'])}, {n(c20['tokens_saida_mediana'])} e {n(c20['segundos_mediana'])} s.")]
    rev = dado.get("revisao")
    if rev:
        v27, v20 = rev[f"corrida_{CORRIDA}"], rev.get("corrida_20_pelo_mesmo_revisor")
        texto += ["", (f"A revisão humana às cegas julgou {n(rev['revisadas'])} propostas desta corrida: {n(v27['Correta'])} corretas, {n(v27['Parcial'])} parciais e {n(v27['Errada'])} "
                       f"erradas; faltam {n(rev['pendentes'])}. "
                       + (f"As edições da corrida 20, julgadas de novo pelo mesmo revisor sem saber a origem, ficaram em {n(v20['Correta'])} corretas, {n(v20['Parcial'])} parciais e "
                          f"{n(v20['Errada'])} erradas." if v20 else "As edições da corrida 20 não entraram nesta revisão; a comparação usa a revisão do lote."))]
    blocos = [
        a3b.tab(f"{PREFIXO}resumo", ["Casos", "Abstenções", "Sem proposta válida", "Propostas", "Sinais de busca", "Notas", "Retificações", "Com texto", "Afirmam um fato",
                                    "Passam nos filtros de hoje", "Passam nos cinco portões", "Cópias do exemplo das instruções", "Tokens lidos (mediana)", "Tokens escritos (mediana)",
                                    "Segundos (mediana)"],
                [[n(r["casos"]), n(r["abstencoes"]), n(r["sem_bloco"]), n(r["propostas"]), n(op["sinal_de_busca"]), n(op["nota"]), n(op["retificacao"]), n(r["com_texto"]), n(r["afirmacoes"]),
                  n(r["passam_nos_filtros_de_hoje"]), n(r["passam_nos_cinco"]), n(r["copias_do_exemplo"]), n(r["tokens_entrada_mediana"]), n(r["tokens_saida_mediana"]), n(r["segundos_mediana"])]]),
        a3b.tab(f"{PREFIXO}leituras", ["Leitura", f"Corrida {CORRIDA}", "Corrida 20", "Teste", "p", "Veredito"],
                [[x["nome"], x[f"corrida_{CORRIDA}"], x["corrida_20"], x["teste"], p(x["p"]), x["veredito"]] for x in dado["leituras"]]),
        a3b.tab(f"{PREFIXO}portoes", ["Portão", "Propostas avaliadas", "Recusa", "Passa", "Não se aplica", "Propostas que pararam aqui"],
                [[x["nome"], n(x["avaliadas"]), n(x["recusa"]), n(x["passa"]), n(x["nao_se_aplica"]), n(x["parou_aqui"])] for x in dado["por_portao"]]),
        a3b.tab(f"{PREFIXO}destino", ["O que aconteceu com a resposta", "Casos"], [[x["destino"], n(x["casos"])] for x in dado["por_destino"]]),
        a3b.tab(f"{PREFIXO}lacuna", ["Grupo de casos", "Casos", "Abstenções", "Sem proposta válida", "Propostas", "Passam nos filtros de hoje", "Passam nos cinco portões"],
                [[x["grupo"], n(x["casos"]), n(x["abstencoes"]), n(x["sem_bloco"]), n(x["propostas"]), n(x["passam_nos_filtros_de_hoje"]), n(x["passam_nos_cinco"])]
                 for x in dado["por_lacuna"] + dado["por_acerto"]]),
        a3b.tab(f"{PREFIXO}origem", ["De onde o diagnóstico leu o caso", "Casos", "Abstenções", "Sem proposta válida", "Propostas", "Passam nos filtros de hoje", "Passam nos cinco portões"],
                [[x["origem"], n(x["casos"]), n(x["abstencoes"]), n(x["sem_bloco"]), n(x["propostas"]), n(x["passam_nos_filtros_de_hoje"]), n(x["passam_nos_cinco"])] for x in dado["por_origem"]]),
        a3b.tab(f"{PREFIXO}codigos", ["Portão em que parou", "Código da recusa", "Casos"], [[x["portao"], x["codigo"], n(x["casos"])] for x in dado["codigos"]] or [["nenhuma recusa", "", ""]]),
        a3b.tab(f"{PREFIXO}casos", ["Caso", "Origem", "Diagnóstico certo", "Com lacuna", "Operação", "O que aconteceu", "Código", "Afirma um fato", "Texto ou termos", "Tokens lidos",
                                   "Segundos"],
                [[f"`{x['caso']}`", n(x["origem"]), "sim" if x["acertou_diagnostico"] else "não", "sim" if x["lacuna"] else "não", n(x["operacao"]) if x["operacao"] else "",
                  x["destino"] or "", x["codigo"] or "", "" if x["forma_passa"] is None else ("sim" if x["forma_passa"] else "não"), b4._esc(x["texto"] or x["termos"]),
                  n(x["tokens_entrada"]), n(x["segundos"])] for x in dado["casos"]] or [["nenhum"] + [""] * 10]),
    ]
    cab = pf.cabecalho(f"O analista de documentação com a ficha curta do caso (corrida {CORRIDA}, medida {MEDIDA})", "avaliar_fase4.py --analista", f"`{dado['metadados'].get('corrida')}`",
                       dado["metadados"]["gerado_em"][:10])
    return "\n".join(cab + [""] + texto + [""] + blocos) + "\n"


NOME_DO_REGISTRO = f"propostas__{NOME}.jsonl"
ARQ_DA_REVISAO = "revisao_as_cegas.json"


def ler_revisao(pasta: Path) -> dict | None:
    """A revisão humana às cegas, quando já foi gravada na pasta da corrida por `ferramentas/revisao_propostas.py --gravar`: quem revisou e o veredito de cada proposta,
    com a origem (corrida 27 ou 20) que a página escondia. None enquanto o arquivo não existe."""
    arq = pasta / ARQ_DA_REVISAO
    return json.loads(arq.read_text(encoding="utf-8")) if arq.exists() else None


def ler(saida: str, modelo: str = MODELO) -> dict:
    """Tudo o que a leitura precisa: os registros da corrida, as condições, os números da corrida 20, a ponte da versão em que a corrida rodou e a revisão humana, se já houver."""
    import executar_fase4 as ex
    raiz, slug = caminhos.fase3(saida)["raiz"], executar_fase3._slug(modelo)
    arq_cond = raiz / "condicoes_fase4.json"
    condicoes = json.loads(arq_cond.read_text(encoding="utf-8")) if arq_cond.exists() else {}
    versao = condicoes.get("versao_ollama")
    return {"registros": executar_bateria.ler_jsonl(raiz / slug / NOME_DO_REGISTRO), "condicoes": condicoes, "corrida20": comparacao_com_a_corrida_20(modelo),
            "ponte": ex.ultima_ponte(ex.carregar_pontes(gravar=False), versao) if versao else None, "revisao": ler_revisao(raiz)}


# ------------------------------------------------------------------ a prévia sem modelo

def _minimo_para_sair_do_ruido(p_de) -> int | None:
    """O menor número, de 1 a 60, para o qual `p_de(numero)` fica abaixo do corte; None se nenhum chega lá."""
    return next((x for x in range(1, 61) if p_de(x) < ALFA), None)


def previa(gerado_em: str | None = None) -> dict:
    """Sem modelo: a ficha de cada um dos 54 casos e o tamanho dela contra o orçamento, o tamanho do prompt contra a proposta de edição de hoje, quem a seleção da
    proposta de desenho chamaria, onde a busca deixou o verbete da causa certa, o prompt inteiro de um caso (é a peça que o Eric aprova) e quanto cada leitura
    precisaria mostrar para sair do ruído contra a corrida 20."""
    itens = casos_da_corrida_20()
    verbetes = {v["id"]: v for v in bib.carregar(base_da_corrida_20())}
    c20 = comparacao_com_a_corrida_20()
    taxas = _taxas()
    saida_por_proposta = ct._mediana([r["tokens_saida"] / r["n_propostas"] for r in executar_bateria.ler_jsonl(
        caminhos.fase3(CORRIDA_20)["raiz"] / executar_fase3._slug(MODELO) / "propostas__E101.jsonl") if r.get("n_propostas") and r.get("tokens_saida")])
    casos, exemplo = [], None
    for i in itens:
        g = i["caso"]["gabarito"]["causa_raiz"]
        ficha = ficha_do_caso(i, verbetes)
        prompt = prompt_do_analista(ficha, bib.render(verbetes[g]))
        exemplo = exemplo or prompt
        tokens = tokens_estimados(prompt)
        segundos = round(tokens / taxas["prefill"] + saida_por_proposta / taxas["geracao"], 1) if taxas.get("prefill") and taxas.get("geracao") and saida_por_proposta else None
        casos.append({"caso": i["caso"]["id"], "origem": i["origem"], "acertou": i["acertou"], "causa_respondida": i["no"].get("escolha"), "gabarito": g,
                      "selo": (i["no"].get("confianca") or {}).get("selo"), "falha": i["no"].get("falha"), "ouro_entregue": i["ouro_entregue"], "posicao_do_ouro": i["posicao_do_ouro"],
                      **i["selecao"], "ficha_tokens": tokens_estimados(ficha), "ficha_chars": len(ficha), "prompt_tokens": tokens, "segundos_estimados": segundos, "ficha": ficha})

    def quantos(condicao) -> int:
        return sum(1 for c in casos if condicao(c))

    fichas, prompts = [c["ficha_tokens"] for c in casos], [c["prompt_tokens"] for c in casos]
    return {"metadados": {"gerado_em": gerado_em or time.strftime("%Y-%m-%dT%H:%M:%S"), "numero": CORRIDA, "medida": MEDIDA},
            "prompt": {"hash_das_instrucoes": HASH_DAS_INSTRUCOES, "instrucoes": INSTRUCOES, "instrucoes_tokens": tokens_estimados(INSTRUCOES), "lembrete_final": LEMBRETE_FINAL,
                       "exemplo_de_forma": EXEMPLO_DE_FORMA, "caso_do_exemplo": casos[0]["caso"] if casos else None, "exemplo": exemplo},
            "resumo": {"casos": len(casos), "origem_tela": quantos(lambda c: c["origem"] == "tela"), "origem_fixture": quantos(lambda c: c["origem"] == "fixture"),
                       "acertos_do_diagnostico": quantos(lambda c: c["acertou"]), "erros_do_diagnostico": quantos(lambda c: not c["acertou"]),
                       "ouro_entregue": quantos(lambda c: c["ouro_entregue"]), "ouro_fora_dos_entregues": quantos(lambda c: not c["ouro_entregue"]),
                       "com_lacuna": quantos(lambda c: c["lacuna"]), "sem_lacuna": quantos(lambda c: not c["lacuna"]),
                       "acertos_com_lacuna": quantos(lambda c: c["lacuna"] and c["acertou"]), "verbete_ja_registra_o_caso": quantos(lambda c: c["verbete_ja_registra_o_caso"]),
                       "seriam_chamados": quantos(lambda c: c["seria_chamado"]),
                       "ficha_tokens_mediana": ct._mediana(fichas), "ficha_tokens_maximo": max(fichas, default=None), "orcamento_da_ficha": ORCAMENTO_DA_FICHA,
                       "fichas_acima_do_orcamento": sum(1 for t in fichas if t > ORCAMENTO_DA_FICHA), "prompt_tokens_mediana": ct._mediana(prompts),
                       "prompt_tokens_maximo": max(prompts, default=None), "prompt_tokens_da_proposta_de_hoje": c20["tokens_entrada_mediana"],
                       "tokens_escritos_por_proposta_na_corrida_20": saida_por_proposta, "segundos_estimados_mediana": ct._mediana([c["segundos_estimados"] for c in casos]),
                       "segundos_da_proposta_de_hoje": c20["segundos_mediana"], "inferencias": len(casos),
                       "minutos_estimados": round(sum(c["segundos_estimados"] or 0 for c in casos) / 60), "biblioteca": evo.hash_biblioteca(base_da_corrida_20())},
            "corrida_20": {k: v for k, v in c20.items() if k != "abstencao_por_caso"},
            "poder": {"abstencoes_para_sair_do_ruido": _minimo_para_sair_do_ruido(lambda x: avaliar.mcnemar_exato(x, 0)),
                      "afirmacoes_em_54_para_sair_do_ruido": _minimo_para_sair_do_ruido(lambda x: fisher_exato(min(x, 54), max(0, 54 - x), c20["afirmacoes"], c20["com_texto"] - c20["afirmacoes"])),
                      "corretas_em_20_para_sair_do_ruido": next((x for x in range(c20["por_veredito"]["Correta"] + 1, 21) if fisher_exato(
                          x, 20 - x, c20["por_veredito"]["Correta"], c20["passaram_nos_filtros"] - c20["por_veredito"]["Correta"]) < ALFA), None)},
            "casos": casos, "regra": texto_da_regra()}


def render_previa(dado: dict) -> str:
    r, c20, pr, poder, n = dado["resumo"], dado["corrida_20"], dado["prompt"], dado["poder"], _n
    texto = [(f"Sem modelo. A corrida {CORRIDA} chama o modelo no papel de analista de documentação nos {n(r['casos'])} casos de aprendizado da corrida 20 ({n(r['origem_tela'])} "
              f"diagnosticados pela tela e {n(r['origem_fixture'])} pelo caso escrito; {n(r['acertos_do_diagnostico'])} diagnósticos certos e {n(r['erros_do_diagnostico'])} errados), "
              f"com a biblioteca de antes do lote (`{r['biblioteca']}`), que só é lida. Cada chamada leva as instruções fixas (hash `{pr['hash_das_instrucoes']}`, cerca de "
              f"{n(pr['instrucoes_tokens'])} tokens), o verbete da causa certa e a ficha curta do caso, montada por código a partir da trilha da corrida 20."),
             "", (f"A ficha. Tem mediana de {n(r['ficha_tokens_mediana'])} tokens estimados e máximo de {n(r['ficha_tokens_maximo'])}, dentro do orçamento de {n(r['orcamento_da_ficha'])} "
                  f"({n(r['fichas_acima_do_orcamento'])} acima). O prompt inteiro tem mediana de {n(r['prompt_tokens_mediana'])} tokens e máximo de {n(r['prompt_tokens_maximo'])}, contra "
                  f"{n(r['prompt_tokens_da_proposta_de_hoje'])} da proposta de edição de hoje; pela taxa do modelo nesta máquina, cada chamada leva cerca de "
                  f"{n(r['segundos_estimados_mediana'])} s (hoje, {n(r['segundos_da_proposta_de_hoje'])} s), e as {n(r['inferencias'])} inferências, cerca de {n(r['minutos_estimados'])} "
                  "minutos."),
             "", (f"O que a corrida consegue enxergar. A busca entregou o verbete da causa certa em {n(r['ouro_entregue'])} casos e o deixou fora dos entregues em "
                  f"{n(r['ouro_fora_dos_entregues'])}: é nestes que um sinal de busca faz sentido, e o portão da busca exige que o caso passe a recebê-lo. Pela seleção da proposta de "
                  f"desenho, há lacuna na documentação em {n(r['com_lacuna'])} casos (os {n(r['erros_do_diagnostico'])} diagnósticos errados e {n(r['acertos_com_lacuna'])} certos em que "
                  f"nenhum verbete entregue tratava da causa respondida), e em {n(r['sem_lacuna'])} não há; em {n(r['verbete_ja_registra_o_caso'])} o verbete já registra o caso, e o "
                  f"desenho chamaria o analista em {n(r['seriam_chamados'])}. Nesta corrida ele é chamado nos {n(r['casos'])}, para a comparação com a corrida 20 ser caso a caso, e a "
                  "leitura separa os casos com lacuna dos sem lacuna, em que a saída esperada é nenhuma."),
             "", (f"O que cada leitura precisa mostrar. Na corrida 20 o modelo fez {n(c20['propostas'])} propostas em {n(c20['casos'])} casos e se absteve em {n(c20['abstencoes'])}; "
                  f"{n(c20['afirmacoes'])} das {n(c20['com_texto'])} afirmavam um fato; e, das {n(c20['passaram_nos_filtros'])} que passaram nos filtros, a revisão humana julgou "
                  f"{n(c20['por_veredito']['Correta'])} corretas. Para sair do ruído, a abstenção precisa aparecer em {n(poder['abstencoes_para_sair_do_ruido'])} casos ou mais; a forma, em "
                  f"{n(poder['afirmacoes_em_54_para_sair_do_ruido'])} afirmações ou mais se as {n(r['casos'])} respostas tiverem texto; e a parcela correta, em "
                  f"{n(poder['corretas_em_20_para_sair_do_ruido'])} corretas ou mais se 20 propostas forem revisadas."),
             "", dado["regra"],
             "", f"O prompt inteiro do caso `{pr['caso_do_exemplo']}`, como o modelo o recebe:", "", "```text", pr["exemplo"], "```"]
    blocos = [
        a3b.tab(f"{PREFIXO}previa_resumo", ["Casos", "Pela tela", "Pelo caso escrito", "Diagnósticos certos", "Verbete certo entregue", "Verbete certo fora dos entregues",
                                           "Ficha: tokens (mediana)", "Ficha: tokens (máximo)", "Prompt: tokens (mediana)", "Prompt da proposta de hoje (mediana)",
                                           "Segundos por chamada (estimados)", "Minutos estimados"],
                [[n(r["casos"]), n(r["origem_tela"]), n(r["origem_fixture"]), n(r["acertos_do_diagnostico"]), n(r["ouro_entregue"]), n(r["ouro_fora_dos_entregues"]),
                  n(r["ficha_tokens_mediana"]), n(r["ficha_tokens_maximo"]), n(r["prompt_tokens_mediana"]), n(r["prompt_tokens_da_proposta_de_hoje"]), n(r["segundos_estimados_mediana"]),
                  n(r["minutos_estimados"])]]),
        a3b.tab(f"{PREFIXO}previa_selecao", ["Casos", "Com lacuna na documentação", "Diagnósticos errados", "Certos sem verbete que trate da causa", "Sem lacuna",
                                            "O verbete já registra o caso", "O desenho chamaria o analista"],
                [[n(r["casos"]), n(r["com_lacuna"]), n(r["erros_do_diagnostico"]), n(r["acertos_com_lacuna"]), n(r["sem_lacuna"]), n(r["verbete_ja_registra_o_caso"]), n(r["seriam_chamados"])]]),
        a3b.tab(f"{PREFIXO}previa_poder", ["Leitura", "Corrida 20", f"O que a corrida {CORRIDA} precisa mostrar para sair do ruído"],
                [["abstenção", f"{n(c20['abstencoes'])} de {n(c20['casos'])} casos", f"{n(poder['abstencoes_para_sair_do_ruido'])} casos ou mais"],
                 ["forma do texto", f"{n(c20['afirmacoes'])} de {n(c20['com_texto'])} propostas afirmam um fato", f"{n(poder['afirmacoes_em_54_para_sair_do_ruido'])} afirmações ou mais em 54"],
                 ["parcela correta", f"{n(c20['por_veredito']['Correta'])} de {n(c20['passaram_nos_filtros'])} edições revisadas",
                  f"{n(poder['corretas_em_20_para_sair_do_ruido'])} corretas ou mais em 20 revisadas"]]),
        a3b.tab(f"{PREFIXO}previa_casos", ["Caso", "Origem", "Diagnóstico certo", "Causa respondida", "Causa certa", "Confiança", "Verbete certo entregue", "Posição na busca",
                                          "Com lacuna", "O verbete já registra o caso", "O desenho chamaria", "Ficha: tokens", "Prompt: tokens"],
                [[f"`{c['caso']}`", c["origem"], "sim" if c["acertou"] else "não", f"`{c['causa_respondida']}`", f"`{c['gabarito']}`", SELOS.get(c["selo"], "não medida"),
                  "sim" if c["ouro_entregue"] else "não", n(c["posicao_do_ouro"]), "sim" if c["lacuna"] else "não", "sim" if c["verbete_ja_registra_o_caso"] else "não",
                  "sim" if c["seria_chamado"] else "não", n(c["ficha_tokens"]), n(c["prompt_tokens"])] for c in dado["casos"]]),
    ]
    cab = pf.cabecalho(f"Prévia sem modelo da corrida {CORRIDA}: a ficha curta do caso e o prompt do analista de documentação", "experimento_analista.py --previa",
                       "`fase4_biblioteca/` (trilha, registros e a biblioteca de antes do lote)", dado["metadados"]["gerado_em"][:10])
    return "\n".join(cab + [""] + texto + [""] + blocos) + "\n"


# ------------------------------------------------------------------ a corrida

def _segue_depois_da_ponte(ponte: dict | None, parcial: bool) -> tuple[bool, str]:
    """Se a corrida pode seguir numa versão do Ollama diferente da da corrida 20: só com ponte completa e pareável com a Fase 3 (decisão 47). A fumaça segue de qualquer jeito."""
    if parcial:
        return True, "corrida parcial: segue sem conferir a ponte"
    if not ponte:
        return False, "a versão do Ollama no ar não tem ponte completa registrada (regra R6): rode a ponte antes; rodar_fila_pre_fase5.ps1 faz isso"
    discordantes = (ponte.get("b") or 0) + (ponte.get("c") or 0)
    if not ponte.get("pareavel"):
        return False, (f"a ponte da versão {ponte.get('versao')} não é pareável com a Fase 3 (b + c = {discordantes}, limite {ponte.get('limite')}): a comparação com a corrida 20, "
                       "que rodou em outra versão, não vale, e a corrida para aqui")
    return True, f"a ponte da versão {ponte.get('versao')} é pareável com a Fase 3 (b + c = {discordantes}, limite {ponte.get('limite')})"


def rodar(args: argparse.Namespace) -> int:
    """Corrida 27: uma chamada do analista de documentação por caso de aprendizado da corrida 20, com o prompt congelado, a ficha curta e a biblioteca de antes do lote;
    cada resposta é lida e passa pelos cinco portões em código, sem modelo. Não escreve fora da pasta da corrida e não altera biblioteca nenhuma. Relançar retoma do
    caso em que parou."""
    import executar_fase4 as ex
    saida = caminhos.fase3(args.saida)["raiz"]
    saida.mkdir(parents=True, exist_ok=True)
    marco = ex._marcador(saida / "fase4.log")
    t0 = time.monotonic()
    inicio = time.strftime("%Y-%m-%dT%H:%M:%S")
    modelo, slug = args.modelo, executar_fase3._slug(args.modelo)
    parcial = bool(args.casos)
    versao, segue = ct._guardas(args, marco)
    if not segue:
        return 2
    if hash_das_instrucoes() != HASH_DAS_INSTRUCOES:
        marco(f"!! as instruções do analista mudaram (hash {hash_das_instrucoes()}, esperado {HASH_DAS_INSTRUCOES}): o prompt é peça medida e a corrida não roda com outro texto")
        return 2
    try:
        itens = casos_da_corrida_20(modelo)
        ctx = contexto_dos_portoes(modelo)
    except (SystemExit, OSError) as e:
        marco(f"!! {e}")
        return 2
    if not itens:
        marco(f"!! sem os registros da corrida 20 em {caminhos.fase3(CORRIDA_20)['raiz']}")
        return 2
    versoes20 = {i["registro"].get("versao_ollama") for i in itens}
    ponte = ex.ultima_ponte(ex.carregar_pontes(gravar=False), versao)
    if versoes20 != {versao}:
        ok, motivo = _segue_depois_da_ponte(ponte, parcial)
        marco(("" if ok else "!! ") + motivo)
        if not ok:
            return 2
    previstos = len(itens)
    itens = itens[:args.casos] if args.casos else itens
    pasta_reg = saida / slug
    pasta_reg.mkdir(parents=True, exist_ok=True)
    arq_prop, arq_resumo = pasta_reg / NOME_DO_REGISTRO, saida / f"{NOME}.jsonl"
    try:
        ex._conferir_versao_das_linhas([arq_prop], versao)
    except SystemExit as e:
        marco(f"!! {e}")
        return 2
    feitos = {r["caso"] for r in executar_bateria.ler_jsonl(arq_resumo)}
    teto = args.teto_proposta
    condicoes = {"modo": NOME, "corrida": CORRIDA, "medida": MEDIDA, "criado_em": inicio, "saida": args.saida, "modelo": modelo, "versao_ollama": versao, "casos": len(itens),
                 "casos_da_corrida_20": previstos, "parcial": parcial, "teto_tokens": teto, "epoca": EPOCA, "hash_das_instrucoes": HASH_DAS_INSTRUCOES, "instrucoes": INSTRUCOES,
                 "lembrete_final": LEMBRETE_FINAL, "orcamento_da_ficha": ORCAMENTO_DA_FICHA, "operacoes": [*OPERACOES, ABSTENCAO], "portoes": list(PORTOES),
                 "biblioteca": {"hash": ctx["hash_da_base"], "origem": f"{CORRIDA_20}/bibliotecas/{slug}/epoca-{dv.VERSAO_CURADA} (a biblioteca de antes do lote da corrida 20, só lida)"},
                 "versao_ollama_da_corrida_20": sorted(str(v) for v in versoes20),
                 "decisao_da_pessoa": "o gabarito do caso, no lugar da decisão de uma pessoa sobre o relatório (medida M2 da proposta de desenho)",
                 "o_que_o_analista_recebe": "as instruções fixas, o verbete da causa certa e a ficha curta do caso, montada por código a partir da trilha da corrida 20",
                 "portoes_contra": "cada proposta é conferida contra a biblioteca de antes do lote, sem acumular as edições dos outros casos",
                 "ponte": ponte, "regra": texto_da_regra()}
    (saida / "condicoes_fase4.json").write_text(json.dumps(condicoes, ensure_ascii=False, indent=2), encoding="utf-8")
    marco(f"INÍCIO {NOME}: Ollama {versao}, {modelo}, biblioteca de antes do lote da corrida 20 ({ctx['hash_da_base']}), instruções {HASH_DAS_INSTRUCOES}; {len(itens)} casos; "
          f"{len(feitos)} já feito(s)")
    digest, versao_ollama = e3b._preparar_modelo(modelo)
    if versao_ollama != versao:
        marco(f"!! a versão do Ollama mudou antes de começar: {versao} para {versao_ollama}")
        return 2

    def _loop() -> None:
        for n, item in enumerate(itens, 1):
            caso = item["caso"]
            if caso["id"] in feitos:
                continue
            ouro = ctx["por_id"][caso["gabarito"]["causa_raiz"]]
            ficha = ficha_do_caso(item, ctx["por_id"])
            prompt = prompt_do_analista(ficha, bib.render(ouro))
            progresso.anunciar(f"{caso['id']} · analista de documentação")
            r = executar_fase3.inferir_com_repeticao(modelo, prompt, teto, caso["id"], "analista de documentação")
            executar_bateria.guarda_tokens_reais(r.get("tokens_entrada", 0), teto, "analista de documentação")
            parseado = parsear_resposta(r.get("resposta", ""), r.get("tokens_saida"), teto)
            decisao = aplicar_portoes(parseado, item, ctx)
            registro = {"modelo": modelo, "digest": digest, "versao_ollama": versao_ollama, "maquina": platform.node(), "fase": "4", "tipo": NOME, "corrida": CORRIDA, "epoca": EPOCA,
                        "biblioteca_versao": ctx["hash_da_base"], "caso": caso["id"], "classe": caso.get("classe"), "nivel": caso.get("nivel"), "origem": item["origem"],
                        "acertou_diagnostico": item["acertou"], "causa_respondida": item["no"].get("escolha"), "selo": (item["no"].get("confianca") or {}).get("selo"),
                        "selecao": item["selecao"], "verbete": ouro["id"], "ouro_entregue": item["ouro_entregue"], "posicao_do_ouro": item["posicao_do_ouro"],
                        "hash_das_instrucoes": HASH_DAS_INSTRUCOES, "ficha": ficha, "ficha_tokens": tokens_estimados(ficha), "prompt": prompt, "prompt_sha256": executar_fase3._sha12(prompt),
                        "teto_tokens": teto, **r, "resposta_truncada": parseado["truncada"], "operacao": parseado["operacao"], "abstencao": parseado["abstencao"],
                        "malformado": parseado["malformado"], "blocos": parseado["blocos"], "fim_ausente": parseado["fim_ausente"], "truncada": parseado["truncada"],
                        "campos": parseado["campos"], **decisao, "copia_do_exemplo": copia_o_exemplo(parseado["campos"].get("TEXTO", "")), **executar_bateria.ambiente_residente()}
            executar_fase3._gravar(arq_prop, registro)
            executar_fase3._gravar(arq_resumo, {"caso": caso["id"], "origem": item["origem"], "operacao": parseado["operacao"], "abstencao": parseado["abstencao"],
                                                "destino": decisao["destino"], "parou_em": decisao["parou_em"], "codigo": decisao["codigo"], "segundos": r.get("segundos"),
                                                "tokens_entrada": r.get("tokens_entrada"), "tokens_saida": r.get("tokens_saida")})
            ex._conferir_versao(versao)
            marco(f"[{n}/{len(itens)}] {caso['id']} ({item['origem']}): {parseado['operacao'] or ('nenhuma' if parseado['abstencao'] else 'sem proposta')} | {decisao['destino']}"
                  f"{' (' + str(decisao['codigo']) + ')' if decisao['codigo'] else ''} | {r.get('segundos')} s; {r.get('tokens_entrada')} tokens lidos, {r.get('tokens_saida')} escritos")

    try:
        e3b._com_modelo_descarregado(modelo, _loop)
    except SystemExit as e:
        marco(f"!! corrida parou: {e}")
        return 1
    marco(f"FIM {NOME}: {len(itens)} casos; duração {time.monotonic() - t0:.0f} s")
    return 0


# ------------------------------------------------------------------ linha de comando

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--previa", action="store_true", help=f"grava a prévia sem modelo em resultados_alvo/fase4/{NOME_PREVIA}.json e .md")
    ap.add_argument("--check", action="store_true", help="com --previa: regera e compara com o gravado, sem gravar")
    args = ap.parse_args(argv)
    if args.previa:
        import avaliar_fase4 as av
        dado = previa()
        return pf.fechar(NOME_PREVIA, dado, render_previa(dado), f"{PREFIXO}previa_", check=args.check, pasta=caminhos.RESULTADOS / "fase4", doc=av.RELATORIO)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
