#!/usr/bin/env python3
# ! Alteração de IA - Revisar: cria evolucao_biblioteca.py — partição fixa dos 90 casos em
# aprendizado/avaliação, parser das propostas de edição que o modelo devolve em texto livre,
# e a gestão de snapshot da cópia da biblioteca de cada modelo (hash, cópia, diff, fechamento
# de época).
# ! Motivo: na Fase 3 cada modelo recebe uma cópia própria de base_conhecimento/ e edita essa
# cópia por acréscimo ao longo de várias épocas. Sem uma partição travada em código, a mesma
# "avaliação" cairia em casos diferentes a cada execução e a comparação pareada entre modelos
# deixaria de valer; sem um parser tolerante ao texto livre do modelo (negrito, colchetes
# opcionais em VERBETE, campo partido em duas linhas), qualquer variação de formatação
# derrubaria a leitura da proposta inteira; sem hash/diff por arquivo, não haveria como provar
# no Memorial o que cada modelo escreveu de uma época para a próxima, nem fechar um número de
# "biblioteca cresceu N caracteres" sem digitar à mão.
"""Partição determinística aprendizado/avaliação dos 90 casos, parser das propostas de
edição em texto livre (blocos PROPOSTA n .. FIM) e gestão de snapshot — hash, cópia, diff
e fechamento de época — da cópia da biblioteca de cada modelo na Fase 3. validar_proposta
e aplicar_edicao (parte B, tarefa seguinte) usam os dicionários e constantes definidos
aqui."""
# ! Alteração de IA - Revisar: a parte B acrescenta os imports copy, recuperacao,
# estrategias e validar_banco.
# ! Motivo: validar_proposta mede a proposta DEPOIS de aplicada — precisa de copy.deepcopy
# para editar os dicionários dos verbetes sem tocar na lista do chamador, de recuperacao
# (Indice/contexto/sinais_do_caso) e estrategias (linear_com_biblioteca) para conferir se o
# prompt de diagnóstico continua cabendo no num_ctx de 8192 depois do acréscimo, e
# fechar_epoca usa validar_banco.escrever_indice para regravar o INDICE.md da cópia.
import copy
import difflib
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

import biblioteca as bib
import cliente_ollama as oll
import estrategias as est
import recuperacao as rec
import validar_banco
# CAUSAS_RAIZ não é usado por nenhuma função desta parte A; importado aqui porque a parte B
# (validar_proposta, tarefa seguinte, no mesmo módulo) precisa dele para conferir se um
# verbete novo aponta causas do conjunto fechado.
from taxonomia import CAUSAS_RAIZ

# ! Alteração de IA - Revisar: força UTF-8 na saída do console, copiado de
# biblioteca.py:25-32.
# ! Motivo: no Windows o console pode estar em cp1252, que não representa os símbolos usados
# nos relatórios (≈, →) — sem isso o script aborta com UnicodeEncodeError ao imprimir.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# --------------------------------------------------------------------- constantes

# O prompt de proposta pede no máximo 2 blocos PROPOSTA por resposta — acima disso a
# validação (parte B) não teria como decidir qual aplicar sem um critério de desempate novo.
MAX_PROPOSTAS_POR_CASO = 2

# Tamanho do campo TEXTO de cada proposta: curto o bastante para não estourar sozinho o teto
# de 800 caracteres renderizados por verbete (bib.TETO_CHARS_NOTAS_VERBETE já soma até 6
# notas); longo o bastante para não virar uma palavra solta sem explicar o que mudou.
TEXTO_MIN, TEXTO_MAX = 60, 280            # chars

# MOTIVO é mais curto que TEXTO porque nunca vai ao prompt (bib.render_notas descarta o
# motivo) — só serve para quem revisa a biblioteca depois de a época fechar.
MOTIVO_MIN, MOTIVO_MAX = 20, 240

# Teto do que um verbete NOVO (operação novo_verbete) pode acrescentar ao frontmatter: o
# mesmo motivo do teto de notas por verbete — sem limite, o frontmatter cresceria a cada
# época até o verbete estourar TETO_CHARS_VERBETE sozinho.
MAX_PALAVRAS_CHAVE_NOVAS, MAX_SINTOMAS_NOVOS = 5, 3

# Cada item de palavra-chave/sintoma novo não pode virar uma frase — 40 caracteres é o maior
# item já usado nos verbetes de base_conhecimento/ (conferido no frontmatter deles).
MAX_CHARS_ITEM_LISTA = 40
ITEM_LISTA_RE = re.compile(r"^[a-z0-9 _\-\.\$]+$")     # aplicado após bib.normalizar

# Nº máximo de verbetes 'aprendidos' novos por época: cada um entra no render_biblioteca do
# braço A1 e no índice do BM25 de todo mundo depois; sem teto, uma época otimista encheria a
# pasta aprendidos/ e inflaria o prompt de quem usa a biblioteca inteira.
TETO_VERBETES_NOVOS_POR_EPOCA = 6

# Teto de tokens estimados (bib.estimar_tokens) para o contexto (verbetes recuperados, k=3,
# mais as notas que já acumularam em épocas anteriores) que entra no prompt de diagnóstico e,
# por continuação literal, no de proposta — validar_proposta recusa (teto_prompt) a edição
# que faria o contexto de algum dos 90 casos passar disso.
TETO_TOKENS_CONTEXTO = 1800                # tokens estimados (bib.estimar_tokens)

# Espaço que sobra para biblioteca + caso no prompt de diagnóstico, descontando o teto de
# tokens de saída (600 — ver executar_bateria) mais uma margem de 64 tokens que o próprio
# Ollama consome de formatação do template.
ORCAMENTO_PROMPT_DIAG = oll.NUM_CTX - 600 - 64
# ! Alteração de IA - Revisar: ORCAMENTO_PROMPT_PROP (NUM_CTX - 700 - 64) foi removida —
# onda final de correções.
# ! Motivo: nenhuma checagem a lia. O prompt de proposta é o de diagnóstico mais a resposta
# do modelo (~200 tokens) e as instruções fixas (~600 tokens); com o contexto preso a
# TETO_TOKENS_CONTEXTO (1.800) e o prompt de diagnóstico a ORCAMENTO_PROMPT_DIAG, o de
# proposta fica sempre abaixo de ~3.900 tokens — metade do num_ctx de 8.192 —, e a guarda
# de tokens reais do executor (guarda_tokens_reais) ainda aborta a época se um dia encostar.
# Conferir os 54 prompts de proposta por época contra um orçamento próprio custaria uma
# montagem de prompt por caso a cada proposta, para acusar um limite que não é alcançável.

# Mesmo limiar de bib.validar (limiar_sobreposicao=0.3): acima disso a proposta está copiando
# o caso em vez de generalizar, o mesmo risco de "medição virar busca de par" que a checagem
# de sobreposição da Fase 2-B já existe para impedir.
LIMIAR_COPIA_PROPOSTA = 0.30

# Fixa para toda a Fase 3: nenhuma execução pode gerar uma partição aprendizado/avaliação
# diferente por acidente (ver gravar_ou_conferir_particao).
SEMENTE_PARTICAO = "fase3"

# Reconhece um id de caso (ex.: "sin-4", "efe-13") dentro de texto livre — a parte B usa para
# achar, no MOTIVO de uma proposta, qual caso originou a nota (mesmo formato que
# bib.NOTA_RE grava) e para não contar essa menção como cópia do caso ao medir
# LIMIAR_COPIA_PROPOSTA (citar o id não é reescrever o sintoma do caso).
CASO_ID_RE = re.compile(r"\b(lex|sin|semt|tra|run|efe)-\d+\b")

# As três operações que uma proposta pode pedir — a parte B (validar_proposta) rejeita
# OPERACAO fora deste conjunto, do mesmo jeito que bib.TIPOS/bib.STATUS fecham o que o
# frontmatter de um verbete aceita.
OPERACOES = ("nota", "retificacao", "novo_verbete")

# Nome da pasta onde o modelo grava verbete tipo 'aprendido' — o mesmo literal já checado em
# bib.validar() (m.get("tipo") == "aprendido" -> pasta == "aprendidos").
PASTA_APRENDIDOS = "aprendidos"

# Arquivos que nunca contam como verbete nem entram no hash/diff nem no invariante de
# somente-acréscimo: o índice humano (INDICE.md, gerado por validar_banco.py --indice), que
# descreve a biblioteca mas não é ele próprio um verbete, e o fechamento.json que
# fechar_snapshot grava dentro da cópia.
# ! Alteração de IA - Revisar: fechamento.json entrou na lista — onda final de correções.
# ! Motivo: conferir_somente_acrescimo passou a varrer TODOS os arquivos novos da cópia (não
# só os .md), e o fechamento.json da própria época seria acusado como "arquivo novo fora de
# aprendidos/" na segunda tentativa de fechar (a corrida caiu entre o fechamento e a gravação).
ARQUIVOS_IGNORADOS = {"INDICE.md", "fechamento.json"}

# Conjunto fechado de nomes de campo que uma proposta pode abrir — uma linha "Exemplo: ..."
# escrita pelo modelo dentro do TEXTO não pode virar um campo novo e cortar o texto ao meio
# (ver _RE_CAMPO/parsear_propostas); qualquer nome fora daqui é tratado como continuação do
# campo aberto por último.
CAMPOS_PROPOSTA = ("OPERACAO", "VERBETE", "TRECHO", "TITULO", "SISTEMA", "ENTIDADE", "CAUSAS",
                   "ARQUIVOS", "PALAVRAS_CHAVE", "SINTOMAS", "TEXTO", "MOTIVO")


# ----------------------------------------------------------------------- partição

# ! Alteração de IA - Revisar: particionar() agrupa os 90 casos por (classe, nível) e usa
# sha256(semente + id) para decidir, dentro de cada célula de 5, quais 3 vão para
# aprendizado e quais 2 vão para avaliação.
# ! Motivo: sem uma regra travada em código, bastaria reordenar banco_casos.py ou rodar de
# novo para a partição mudar — e a Fase 3 compara o MESMO modelo entre épocas e o desempenho
# de avaliação teria de ser sempre sobre os mesmos casos para dar para comparar. O hash (e
# não, por exemplo, a ordem de chegada) desacopla a partição da ordem em que os casos estão
# escritos nos arquivos — o achado 4.20 do Memorial já mostrou que a ordem do banco de casos
# muda com correções, e uma partição presa à ordem mudaria junto.
def particionar(casos: list[dict], semente: str = SEMENTE_PARTICAO) -> dict:
    """Agrupa os casos por (classe, nível) — tem de dar 18 células de 5 — e usa o hash de
    cada id para separar, em cada célula, 3 casos para 'aprendizado' e 2 para 'avaliacao'.
    Devolve também o hash de cada caso, para gravar_ou_conferir_particao notar qualquer
    divergência célula a célula."""
    por_celula: dict[tuple[int, int], list[dict]] = {}
    for c in casos:
        por_celula.setdefault((c["classe"], c["nivel"]), []).append(c)
    # ! Alteração de IA - Revisar: confere também o NÚMERO de células, não só o tamanho de
    # cada uma — round 1 de revisão.
    # ! Motivo: taxonomia.CLASSES x taxonomia.NIVEIS é uma grade fixa de 6 x 3 = 18 células;
    # uma célula a mais (classe/nível fora da grade, por um id com classe ou nível errado no
    # banco de casos) passava batido pela checagem "5 por célula" se, por acidente, também
    # tivesse exatamente 5 casos — só contar as células fecha esse buraco.
    if len(por_celula) != 18:
        raise ValueError(f"esperado 18 células (classe, nível), achou {len(por_celula)}")
    for (classe, nivel), grupo in por_celula.items():
        if len(grupo) != 5:
            raise ValueError(f"célula classe={classe} nivel={nivel} tem {len(grupo)} "
                             f"caso(s), esperado 5")

    particao_por_id, hash_por_id = {}, {}
    for grupo in por_celula.values():
        ordenados = sorted(grupo, key=lambda c: hashlib.sha256(
            f"{semente}:{c['id']}".encode()).hexdigest())
        for i, c in enumerate(ordenados):
            hash_por_id[c["id"]] = hashlib.sha256(f"{semente}:{c['id']}".encode()).hexdigest()
            particao_por_id[c["id"]] = "aprendizado" if i < 3 else "avaliacao"

    casos_saida, n_aprendizado, n_avaliacao = {}, 0, 0
    for c in casos:
        particao = particao_por_id[c["id"]]
        casos_saida[c["id"]] = {"particao": particao, "classe": c["classe"],
                                "nivel": c["nivel"], "hash": hash_por_id[c["id"]]}
        if particao == "aprendizado":
            n_aprendizado += 1
        else:
            n_avaliacao += 1

    return {"regra": "sha256(semente + ':' + id) ordena os 5 casos de cada celula (classe, "
                     "nivel); 3 primeiros = aprendizado, 2 ultimos = avaliacao",
            "semente": semente, "n_aprendizado": n_aprendizado, "n_avaliacao": n_avaliacao,
            "casos": casos_saida}


# ! Alteração de IA - Revisar: gravar_ou_conferir_particao grava particao.json na primeira
# chamada e, nas seguintes, só confere — nunca sobrescreve uma partição diferente.
# ! Motivo: cada modelo roda em sessões separadas (às vezes em dias diferentes) e todas
# precisam usar a MESMA partição; se um script rodasse particionar() de novo com um
# banco_casos.py alterado (outra correção tipo o achado 4.20) e regravasse por cima, os
# modelos já testados ficariam com aprendizado/avaliação diferente dos que rodarem depois,
# sem ninguém perceber. SystemExit (e não só um aviso) porque seguir com partição misturada
# invalida a comparação pareada entre modelos.
def gravar_ou_conferir_particao(caminho: Path, particao: dict) -> dict:
    """Se `caminho` não existe, grava `particao` e a devolve; se existe, lê o que está
    gravado e compara — divergência para a execução com SystemExit."""
    if not caminho.exists():
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text(json.dumps(particao, ensure_ascii=False, indent=2),
                           encoding="utf-8")
        return particao
    lido = json.loads(caminho.read_text(encoding="utf-8"))
    if lido != particao:
        raise SystemExit("particao.json existente difere da regra atual — não misture execuções")
    return lido


def particao_de(particao: dict, caso_id: str) -> str:
    """! Alteração de IA - Revisar: atalho de leitura sobre o dicionário de particionar().
    ! Motivo: quem roda a época de um caso (executar_bateria da Fase 3) só precisa saber se
    ele é de aprendizado ou avaliação — sem este atalho, cada chamador reimplementaria
    particao["casos"][caso_id]["particao"] e um typo na chave não seria notado em nenhum
    teste específico."""
    return particao["casos"][caso_id]["particao"]


# -------------------------------------------------------------------------- parser

# Início/fim de bloco: "PROPOSTA 2" ou "FIM" sozinhos na linha, sem exigir maiúsculas — o
# modelo às vezes copia o rótulo do prompt em minúsculas.
_RE_INICIO_BLOCO = re.compile(r"^PROPOSTA\s+(\d+)\s*$", re.IGNORECASE)
_RE_FIM_BLOCO = re.compile(r"^FIM\s*$", re.IGNORECASE)
# Candidata a abrir um campo: um "nome:" no início da linha. Só abre de fato se o nome
# normalizado estiver em CAMPOS_PROPOSTA (ver _nome_campo) — qualquer outro nome pertence ao
# campo aberto por último (TEXTO/MOTIVO em duas linhas).
_RE_CAMPO = re.compile(r"^(\w+)\s*:\s*(.*)$")

_ORDEM_CAMPOS_OBRIGATORIOS = ("OPERACAO", "VERBETE", "TEXTO", "MOTIVO")


# ! Alteração de IA - Revisar: normaliza uma linha (sem acento, maiúsculas, sem pontuação)
# para reconhecer a palavra NENHUMA fora de blocos mesmo com variação de pontuação.
# ! Motivo: o prompt pede a palavra NENHUMA sozinha, mas o modelo às vezes devolve
# "Nenhuma." ou "NENHUMA!" — exigir a grafia exata faria uma resposta correta em espírito
# virar 'nenhuma=False' e a proposta ausente ser tratada como malformada.
def _normalizar_linha(linha: str) -> str:
    sem_pontuacao = re.sub(r"[^\w\s]", "", bib.normalizar(linha))
    return re.sub(r"\s+", " ", sem_pontuacao).strip().upper()


# ! Alteração de IA - Revisar: normaliza (maiúsculas, sem acento) o nome candidato a campo
# antes de conferir CAMPOS_PROPOSTA — round 1 de revisão.
# ! Motivo: _RE_CAMPO sozinho casava qualquer "palavra:" no início da linha — uma linha como
# "Exemplo: 10 e 10.0 sao considerados iguais", escrita pelo modelo dentro do TEXTO, virava
# um campo novo "EXEMPLO" e cortava o texto ao meio (o TEXTO ficava só com a primeira linha).
# Normalizar antes de comparar cobre o modelo escrever o nome do campo com acento (ex.:
# "título") ou em minúsculas ("texto:"), sem abrir uma exceção por campo conhecido.
def _nome_campo(candidato: str) -> str:
    return bib.normalizar(candidato).upper()


# ! Alteração de IA - Revisar: VERBETE aceita tanto "[id]" quanto "id" — o valor guardado
# nunca leva os colchetes.
# ! Motivo: o prompt pede "[id_do_verbete]" (igual ao FONTE do diagnóstico), mas o modelo às
# vezes devolve sem colchetes; guardar com ou sem colchetes conforme o modelo escreveu
# obrigaria a parte B a normalizar de novo em todo lugar que lê VERBETE.
def _extrair_verbete(valor: str) -> str:
    m = re.match(r"^\[(.+)\]$", valor)
    return m.group(1).strip() if m else valor


# ! Alteração de IA - Revisar: decide se um bloco fechado com FIM está completo — falta
# CAMPO na ordem OPERACAO/VERBETE/TEXTO/MOTIVO, exceto quando OPERACAO é 'nenhuma'.
# ! Motivo: o prompt permite responder "NENHUMA" tanto como linha solta quanto dentro de um
# bloco PROPOSTA (alguns modelos só respondem em bloco); sem a exceção, todo bloco
# "OPERACAO: nenhuma" seria acusado de "falta VERBETE", quando na verdade é uma resposta
# válida de que não há proposta nesta rodada.
def _validar_campos_do_bloco(bloco: dict) -> None:
    if bloco["campos"].get("OPERACAO", "").strip().lower() == "nenhuma":
        return
    for campo in _ORDEM_CAMPOS_OBRIGATORIOS:
        if not bloco["campos"].get(campo):
            bloco["malformado"] = f"falta {campo}"
            return


# ! Alteração de IA - Revisar: parsear_propostas lê a resposta de texto livre do modelo linha
# a linha e devolve os blocos PROPOSTA/FIM já separados em campos, mais se a resposta foi
# "sem proposta" (NENHUMA) e se parece truncada pelo teto de tokens de saída.
# ! Motivo: o modelo escreve a proposta como texto solto (não JSON — um `num_predict` curto
# interrompe JSON no meio e ele fica sem sintaxe para recuperar nenhum campo). Formatação de
# markdown (negrito), campo partido em duas linhas e colchetes opcionais em VERBETE são
# variações observadas nos pilotos de texto livre com estes modelos; sem tolerar todas, a
# maior parte das respostas seria descartada como malformada e a Fase 3 mediria a paciência
# do parser, não a qualidade da proposta.
def parsear_propostas(resposta: str, tokens_saida: int | None = None,
                      max_tokens: int | None = None) -> dict:
    """{"nenhuma": bool, "truncada": bool,
        "blocos": [{"numero", "campos", "malformado", "fim_ausente"}]}."""
    limpa = resposta.replace("*", "").replace("`", "")
    blocos: list[dict] = []
    bloco: dict | None = None
    linha_nenhuma_fora_de_blocos = False

    for linha_bruta in limpa.splitlines():
        linha = linha_bruta.strip()

        m_inicio = _RE_INICIO_BLOCO.match(linha)
        if m_inicio:
            if bloco is not None:
                bloco["_sem_fim"] = True
                blocos.append(bloco)
            bloco = {"numero": int(m_inicio.group(1)), "campos": {}, "malformado": None,
                     "_aberto": None, "_sem_fim": False}
            continue

        if bloco is not None:
            if _RE_FIM_BLOCO.match(linha):
                _validar_campos_do_bloco(bloco)
                blocos.append(bloco)
                bloco = None
                continue
            m_campo = _RE_CAMPO.match(linha)
            nome_candidato = _nome_campo(m_campo.group(1)) if m_campo else None
            if m_campo and nome_candidato in CAMPOS_PROPOSTA:
                nome, valor = nome_candidato, m_campo.group(2).strip()
                if nome == "VERBETE":
                    valor = _extrair_verbete(valor)
                bloco["campos"][nome] = valor
                bloco["_aberto"] = nome
            elif bloco["_aberto"] and linha:
                nome = bloco["_aberto"]
                bloco["campos"][nome] = (bloco["campos"][nome] + " " + linha).strip()
            continue

        if _normalizar_linha(linha) == "NENHUMA":
            linha_nenhuma_fora_de_blocos = True

    if bloco is not None:
        bloco["_sem_fim"] = True
        blocos.append(bloco)

    truncada = bool(tokens_saida is not None and max_tokens is not None
                   and tokens_saida >= max_tokens
                   and not limpa.rstrip().upper().endswith(("FIM", "NENHUMA")))

    # ! Alteração de IA - Revisar: bloco que termina sem a linha FIM só é acusado quando a
    # resposta foi cortada pelo teto de tokens; sem corte, ele passa pela mesma conferência de
    # campos de um bloco fechado com FIM e sai marcado com fim_ausente=True — round 2 de
    # revisão, depois do piloto.
    # ! Motivo: no piloto da Fase 3 o qwen2.5-coder:3b escreveu os 12 campos das 6 propostas e
    # não escreveu o FIM em nenhuma; as respostas tinham 185 a 192 tokens de saída para um
    # teto de 700, ou seja, terminaram sozinhas. As 6 foram recusadas como "sem FIM" e a
    # biblioteca do modelo não cresceu em época nenhuma — a Fase 3 estaria medindo se o modelo
    # copia a palavra FIM, não a qualidade da proposta. Quem distingue resposta completa de
    # resposta cortada é a contagem de tokens (tokens_saida >= max_tokens), que já vinha
    # calculada aqui; a marca fim_ausente fica no bloco para a avaliação contar quantas
    # propostas chegaram sem o FIM.
    # ! Alteração de IA - Revisar: a marca "sem FIM" por resposta cortada só vale para o
    # ÚLTIMO bloco; um bloco fechado pela PROPOSTA seguinte é conferido como completo —
    # onda final de correções.
    # ! Motivo: `truncada` é uma propriedade da resposta inteira, mas o corte pelo teto de
    # tokens só pode ter atingido o bloco que estava aberto quando a resposta acabou. Com a
    # regra anterior, "PROPOSTA 1 completa (sem FIM) + PROPOSTA 2 cortada" recusava as duas
    # como "sem FIM", e a primeira — que tem os quatro campos e foi encerrada pelo próprio
    # modelo ao abrir a segunda — era perdida por um corte que não a atingiu.
    ultimo = blocos[-1] if blocos else None
    for b in blocos:
        if not b["_sem_fim"]:
            continue
        if truncada and b is ultimo:
            b["malformado"] = "sem FIM"
        else:
            _validar_campos_do_bloco(b)

    blocos_finais = [{"numero": b["numero"], "campos": b["campos"],
                      "malformado": b["malformado"], "fim_ausente": b["_sem_fim"]}
                     for b in blocos]

    tem_bloco_nenhuma = any(b["malformado"] is None
                           and b["campos"].get("OPERACAO", "").strip().lower() == "nenhuma"
                           for b in blocos_finais)
    tem_bloco_valido = any(b["malformado"] is None for b in blocos_finais)
    nenhuma = tem_bloco_nenhuma or (linha_nenhuma_fora_de_blocos and not tem_bloco_valido)

    return {"nenhuma": nenhuma, "blocos": blocos_finais, "truncada": truncada}


# ------------------------------------------------------------- snapshot, hash, cópia, diff

# ! Alteração de IA - Revisar: lista, sem os arquivos ignorados, os .md de uma raiz de
# biblioteca, indexados pelo caminho relativo em posix — usado por hash_biblioteca e
# diff_bibliotecas para não duplicar a mesma varredura. O filtro de ARQUIVOS_IGNORADOS
# compara em maiúsculas (round 1 de revisão).
# ! Motivo: hash_biblioteca precisa da ordem de caminho relativo posix (o mesmo hash tem de
# sair igual em Windows e Linux, onde o separador de pasta muda) e diff_bibliotecas precisa
# comparar as duas raízes pelo mesmo caminho relativo — repetir esta varredura em cada função
# arriscava as duas divergirem no critério de quais arquivos entram. A comparação em
# maiúsculas segue bib.carregar() (arq.name.upper() == "INDICE.MD"): sem ela, um índice
# gravado como "indice.md" entraria na varredura como se fosse um verbete novo, e
# hash_biblioteca/diff_bibliotecas passariam a depender de como o índice foi nomeado.
# ! Alteração de IA - Revisar: o filtro de arquivos ignorados passou a ser _e_gerado (parte
# B), que cobre também os diff__*.md — antes só o INDICE.md saía da varredura.
# ! Motivo: quando fechar_epoca ainda gravava diff__E1.md e diff__E1__vs_original.md dentro
# da pasta epoca-1, hash_biblioteca(epoca-1) mudava depois do fechamento e deixava de bater
# com o hash gravado no fechamento.json — foi assim que o teste de fechar_epoca falhou. O
# round 0 de revisão tirou os diffs de dentro das pastas de época; o filtro fica como defesa,
# porque esta varredura é rglob e qualquer .md solto na pasta vira "verbete" para o hash e
# para o diff.
def _arquivos_md(raiz: Path) -> dict[str, Path]:
    return {a.relative_to(raiz).as_posix(): a
            for a in raiz.rglob("*.md") if not _e_gerado(a.name)}


# ! Alteração de IA - Revisar: hash_biblioteca resume todos os .md de uma raiz (caminho +
# conteúdo, em ordem de caminho relativo posix) num hash de 12 caracteres.
# ! Motivo: é o número que fechar_snapshot grava para provar, no Memorial, que duas cópias da
# biblioteca são byte a byte iguais (ou não) sem precisar comparar arquivo por arquivo à mão;
# 12 caracteres hex (48 bits) bastam para não colidir entre as poucas dezenas de snapshots da
# Fase 3 e caber legível numa linha de log.
def hash_biblioteca(raiz: Path) -> str:
    h = hashlib.sha256()
    for rel, arq in sorted(_arquivos_md(raiz).items()):
        h.update(rel.encode() + b"\0" + arq.read_bytes() + b"\0")
    return h.hexdigest()[:12]


# ! Alteração de IA - Revisar: copiar_biblioteca clona a pasta da biblioteca para cada modelo
# usar como cópia própria, sem o INDICE.md (que descreve a biblioteca de origem, não a cópia).
# ! Motivo: cada modelo da Fase 3 precisa de uma pasta própria para editar por acréscimo sem
# um interferir na do outro; copiar com o INDICE.md antigo deixaria um índice desatualizado
# (e potencialmente enganoso) dentro da cópia assim que a primeira nota fosse acrescentada. O
# FileExistsError é levantado ANTES do shutil.copytree para dar uma mensagem que diz qual
# pasta já existe, em vez do "[Errno 17]" genérico do sistema operacional.
def copiar_biblioteca(origem: Path, destino: Path) -> Path:
    if destino.exists():
        raise FileExistsError(f"destino já existe: {destino} — apague ou escolha outra "
                              "pasta antes de copiar a biblioteca")
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(origem, destino, ignore=shutil.ignore_patterns("INDICE.md", "__pycache__"))
    return destino


def contar_notas(verbetes: list[dict]) -> tuple[int, int]:
    """! Alteração de IA - Revisar: soma as notas de todos os verbetes em (n_notas,
    n_retificacoes), usando bib.notas.
    ! Motivo: fechar_snapshot e o relatório da Fase 3 precisam do total da biblioteca
    inteira, não verbete a verbete — sem esta função, cada chamador repetiria o mesmo laço
    sobre bib.notas(v)."""
    n_notas = n_retificacoes = 0
    for v in verbetes:
        for nota in bib.notas(v):
            if nota["operacao"] == "retificacao":
                n_retificacoes += 1
            else:
                n_notas += 1
    return n_notas, n_retificacoes


def _gravar_json_atomico(caminho: Path, dado: dict) -> None:
    """! Alteração de IA - Revisar: grava o JSON num arquivo temporário ao lado
    (<nome>.tmp) e o troca pelo definitivo com os.replace — onda final (achado M12).
    ! Motivo: fechamento.json é o que snapshot_fechado() lê para decidir se uma época já
    fechou, e maquina.json é relido a cada relance. Com write_text direto, uma queda de
    energia no meio da gravação deixava um JSON pela metade com o nome definitivo: a época
    seguinte tomaria a pasta por fechada e json.loads abortaria com JSONDecodeError na
    primeira leitura. os.replace troca o nome numa operação só do sistema de arquivos, então
    o arquivo definitivo ou é o antigo inteiro ou é o novo inteiro."""
    caminho.parent.mkdir(parents=True, exist_ok=True)
    temporario = caminho.with_name(caminho.name + ".tmp")
    temporario.write_text(json.dumps(dado, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temporario, caminho)


# ! Alteração de IA - Revisar: fechar_snapshot grava fechamento.json com o retrato da
# biblioteca de um modelo ao fim de uma época — hash, contagens e o que foi aceito na época.
# ! Motivo: sem um arquivo próprio por cópia, a única forma de saber "quantos verbetes esse
# modelo tinha na época 3" seria reabrir o JSONL de execução inteiro e recontar; o hash aqui é
# o mesmo de hash_biblioteca, gravado junto para o fechamento servir de prova de integridade
# (se alguém reabrir a cópia depois e o hash não bater, algo mexeu na pasta fora do fluxo).
# ! Alteração de IA - Revisar: ganha o parâmetro versao_ollama (gravado como campo do
# fechamento) e passa a gravar por _gravar_json_atomico — onda final (achados I5 e M12).
# ! Motivo: o Ollama atualizou sozinho de 0.33.3 para 0.34.0 entre a Fase 2-B e a Fase 3;
# sem a versão no fechamento, uma época produzida antes e outra depois de uma atualização
# automática no meio da corrida ficariam indistinguíveis na análise.
def fechar_snapshot(raiz: Path, epoca: int, modelo: str, aceitas_na_epoca: int,
                    quando: str | None = None, versao_ollama: str | None = None) -> dict:
    verbetes = bib.carregar(raiz)
    n_notas, n_retificacoes = contar_notas(verbetes)
    render_completo = bib.render_biblioteca(verbetes)
    dado = {
        "modelo": modelo,
        "epoca": epoca,
        "hash": hash_biblioteca(raiz),
        "n_verbetes": len(verbetes),
        "n_verbetes_novos": sum(1 for v in verbetes if v["pasta"] == PASTA_APRENDIDOS),
        "n_notas": n_notas,
        "n_retificacoes": n_retificacoes,
        "chars": len(render_completo),
        "tokens_estimados": bib.estimar_tokens(render_completo),
        "aceitas_na_epoca": aceitas_na_epoca,
        "versao_ollama": versao_ollama,
        "fechado_em": quando or datetime.now().isoformat(timespec="seconds"),
    }
    _gravar_json_atomico(raiz / "fechamento.json", dado)
    return dado


def snapshot_fechado(raiz: Path) -> bool:
    """! Alteração de IA - Revisar: True se fechar_snapshot já rodou nesta raiz.
    ! Motivo: quem orquestra as épocas (T7/T12, ainda por vir) precisa de uma forma barata
    de perguntar "esta cópia já fechou?" sem reabrir e reler o fechamento.json inteiro."""
    return (raiz / "fechamento.json").exists()


# ! Alteração de IA - Revisar: monta, para cada verbete tocado ou novo entre raiz_a e
# raiz_b, quantas notas/retificações foram ACRESCENTADAS (não o total acumulado) e quais
# itens de palavras-chave/sintomas são novos no frontmatter.
# ! Motivo: a Fase 3 só permite acréscimo — um verbete já pode ter notas de uma época
# anterior (presentes em raiz_a) e ganhar mais notas nesta (só em raiz_b); reportar o total
# de raiz_b escondendo o que já existia em raiz_a mediria a biblioteca inteira do modelo a
# cada diff, não o que ele escreveu NESTA época, que é o número que entra no relatório por
# época.
def _por_verbete(raiz_a: Path, raiz_b: Path, rels_afetados: set[str]) -> dict:
    if not rels_afetados:
        return {}
    por_rel_a = {v["caminho"].relative_to(raiz_a).as_posix(): v for v in bib.carregar(raiz_a)}
    por_rel_b = {v["caminho"].relative_to(raiz_b).as_posix(): v for v in bib.carregar(raiz_b)}

    saida = {}
    for rel in rels_afetados:
        # rels_afetados só traz "tocados" (existem nas duas raízes) e "novos" (só em b) --
        # quem chama esta função nunca passa "removidos", então vb sempre existe.
        vb = por_rel_b[rel]
        va = por_rel_a.get(rel)
        notas_a = bib.notas(va) if va else []
        notas_b = bib.notas(vb)
        novas = notas_b[len(notas_a):] if len(notas_b) >= len(notas_a) else notas_b
        pc_a = set(va["meta"].get("palavras_chave", [])) if va else set()
        sn_a = set(va["meta"].get("sintomas", [])) if va else set()
        saida[vb["id"]] = {
            "notas": sum(1 for n in novas if n["operacao"] == "nota"),
            "retificacoes": sum(1 for n in novas if n["operacao"] == "retificacao"),
            "palavras_chave_novas": [p for p in vb["meta"].get("palavras_chave", [])
                                    if p not in pc_a],
            "sintomas_novos": [s for s in vb["meta"].get("sintomas", []) if s not in sn_a],
        }
    return saida


def _diff_arquivo(rel: str, a_linhas: list[str], b_linhas: list[str], rotulo_a: str,
                  rotulo_b: str) -> list[str]:
    """! Alteração de IA - Revisar: diff unificado de um arquivo, sem quebra de linha nas
    strings (lineterm="") porque quem concatena os arquivos é diff_bibliotecas.
    ! Motivo: extraído para diff_bibliotecas não repetir a mesma chamada a
    difflib.unified_diff três vezes (tocados, novos, removidos) com um `fromfile`/`tofile`
    calculado errado em algum dos três seria fácil de não notar num diff que só cresce."""
    return list(difflib.unified_diff(a_linhas, b_linhas, fromfile=f"{rotulo_a}/{rel}",
                                     tofile=f"{rotulo_b}/{rel}", lineterm=""))


# ! Alteração de IA - Revisar: diff_bibliotecas compara duas cópias da biblioteca por
# arquivo .md (novo/removido/tocado), soma linhas e caracteres acrescentados e devolve o
# diff unificado de cada arquivo mudado.
# ! Motivo: é o número que fecha cada época no relatório da Fase 3 ("o modelo X acrescentou N
# notas, M caracteres, em P verbetes na época 3") e a evidência bruta (unificado) que entra
# no Memorial para mostrar exatamente o que o modelo escreveu, sem precisar abrir as duas
# pastas lado a lado à mão.
def diff_bibliotecas(raiz_a: Path, raiz_b: Path, rotulo_a: str = "a",
                     rotulo_b: str = "b") -> dict:
    mapa_a, mapa_b = _arquivos_md(raiz_a), _arquivos_md(raiz_b)
    textos_a = {rel: p.read_text(encoding="utf-8") for rel, p in mapa_a.items()}
    textos_b = {rel: p.read_text(encoding="utf-8") for rel, p in mapa_b.items()}

    comuns = set(textos_a) & set(textos_b)
    arquivos_novos = sorted(set(textos_b) - set(textos_a))
    arquivos_removidos = sorted(set(textos_a) - set(textos_b))
    arquivos_tocados = sorted(rel for rel in comuns if textos_a[rel] != textos_b[rel])

    triplas = ([(rel, textos_a[rel].splitlines(), textos_b[rel].splitlines())
               for rel in arquivos_tocados]
              + [(rel, [], textos_b[rel].splitlines()) for rel in arquivos_novos]
              + [(rel, textos_a[rel].splitlines(), []) for rel in arquivos_removidos])

    linhas_acrescentadas = linhas_removidas = 0
    pedacos_diff = []
    for rel, a_linhas, b_linhas in triplas:
        diff = _diff_arquivo(rel, a_linhas, b_linhas, rotulo_a, rotulo_b)
        linhas_acrescentadas += sum(1 for l in diff if l.startswith("+")
                                    and not l.startswith("+++"))
        linhas_removidas += sum(1 for l in diff if l.startswith("-")
                                and not l.startswith("---"))
        pedacos_diff.append("\n".join(diff))

    chars_antes = sum(len(t) for t in textos_a.values())
    chars_depois = sum(len(t) for t in textos_b.values())
    chars_acrescentados = chars_depois - chars_antes

    return {
        "arquivos_novos": arquivos_novos,
        "arquivos_removidos": arquivos_removidos,
        "arquivos_tocados": arquivos_tocados,
        "linhas_acrescentadas": linhas_acrescentadas,
        "linhas_removidas": linhas_removidas,
        "chars_antes": chars_antes,
        "chars_depois": chars_depois,
        "chars_acrescentados": chars_acrescentados,
        # Mesma razão chars/token de bib.estimar_tokens (CHARS_POR_TOKEN), aplicada à
        # diferença de caracteres em vez de a um texto — não há um texto contíguo só com
        # "o que foi acrescentado" para passar a estimar_tokens.
        "tokens_estimados_acrescentados": round(chars_acrescentados / bib.CHARS_POR_TOKEN),
        "por_verbete": _por_verbete(raiz_a, raiz_b, set(arquivos_tocados) | set(arquivos_novos)),
        "unificado": "\n".join(pedacos_diff),
    }


# ! Alteração de IA - Revisar: escrever_diff grava o resultado de diff_bibliotecas em
# <destino>.json (sem o texto do diff) e <destino>.md (tabela de totais + o diff dentro de um
# bloco ```diff), os dois GERADOS — não para editar à mão.
# ! Motivo: o .json é o que outro script (comparação entre épocas, relatório da Fase 3) lê de
# volta; o .md é para abrir e ler o diff formatado sem precisar de um visualizador de JSON. Os
# dois vêm da mesma chamada a diff_bibliotecas para nunca divergir um do outro.
def escrever_diff(raiz_a: Path, raiz_b: Path, destino_sem_extensao: Path, rotulo_a: str,
                  rotulo_b: str) -> dict:
    dado = diff_bibliotecas(raiz_a, raiz_b, rotulo_a, rotulo_b)
    destino_sem_extensao.parent.mkdir(parents=True, exist_ok=True)

    # ! Alteração de IA - Revisar: troca destino_sem_extensao.with_suffix(".json"/".md") por
    # with_name(...+ ".json"/".md") — round 1 de revisão.
    # ! Motivo: with_suffix() troca tudo depois do ÚLTIMO ponto do nome, não só acrescenta a
    # extensão; a Fase 3 nomeia os arquivos de diff pelo modelo (ex.: "qwen2.5-coder_3b"), que
    # tem ponto, e with_suffix(".json") sobre "diff__E1__qwen2.5-coder_3b" devolvia
    # "diff__E1__qwen2.json" — truncava o nome do modelo em vez de só acrescentar ".json".
    sem_unificado = {k: v for k, v in dado.items() if k != "unificado"}
    destino_sem_extensao.with_name(destino_sem_extensao.name + ".json").write_text(
        json.dumps(sem_unificado, ensure_ascii=False, indent=2), encoding="utf-8")

    linhas_md = [
        f"<!-- ! Alteração de IA - Revisar: diff entre duas cópias da biblioteca "
        f"({rotulo_a} -> {rotulo_b}), GERADO por evolucao_biblioteca.escrever_diff.",
        "     ! Motivo: os totais e o diff abaixo vêm de comparar os arquivos .md das duas",
        "     pastas byte a byte; reescrever isto à mão ficaria desatualizado na próxima",
        "     época — não editar, só regravar. -->",
        "",
        f"# Diff da biblioteca: {rotulo_a} -> {rotulo_b}",
        "",
        "| Métrica | Valor |",
        "|---|---|",
        f"| Arquivos novos | {len(dado['arquivos_novos'])} |",
        f"| Arquivos removidos | {len(dado['arquivos_removidos'])} |",
        f"| Arquivos tocados | {len(dado['arquivos_tocados'])} |",
        f"| Linhas acrescentadas | {dado['linhas_acrescentadas']} |",
        f"| Linhas removidas | {dado['linhas_removidas']} |",
        f"| Caracteres antes | {dado['chars_antes']} |",
        f"| Caracteres depois | {dado['chars_depois']} |",
        f"| Caracteres acrescentados | {dado['chars_acrescentados']} |",
        f"| Tokens estimados acrescentados | {dado['tokens_estimados_acrescentados']} |",
        "",
        "```diff",
        dado["unificado"],
        "```",
        "",
    ]
    destino_sem_extensao.with_name(destino_sem_extensao.name + ".md").write_text(
        "\n".join(linhas_md), encoding="utf-8")
    return dado


# ------------------------------------------- validação das propostas do modelo (parte B)

# ! Alteração de IA - Revisar: lista fechada de TODOS os códigos que validar_proposta pode
# devolver em "motivo" quando recusa uma proposta.
# ! Motivo: cada recusa vira uma barra no histograma de rejeições do relatório da Fase 3. Com
# o código escrito solto dentro de cada `if`, um erro de digitação ("texto_curto_" no lugar de
# "texto_curto") criaria uma categoria nova sem ninguém notar e a soma do histograma deixaria
# de fechar com o número de propostas recusadas; esta tupla é o que o relatório usa para
# inicializar o histograma em zero e o que o teste confere para nenhum código sumir.
CODIGOS_REJEICAO = (
    "sem_bloco", "bloco_malformado", "excesso_de_propostas", "operacao_invalida",
    "alvo_inexistente", "alvo_nao_visto", "id_invalido", "id_repetido",
    "teto_verbetes_novos", "pasta_invalida", "vocabulario", "causa_fora_do_conjunto",
    "arquivo_inexistente", "endpoint_inexistente", "tabela_inexistente",
    "texto_curto", "texto_longo", "motivo_ausente", "motivo_curto", "motivo_longo",
    "retificacao_sem_trecho", "trecho_nao_encontrado", "palavra_chave_invalida",
    "duplicada", "copia_do_caso", "teto_notas_verbete", "teto_verbete_novo", "teto_prompt",
    "copia_do_caso_acumulada", "biblioteca_invalida",
)

# ! Alteração de IA - Revisar: o formato do id de verbete novo passou a aceitar sublinhado
# além do hífen (`[-_]` como separador) — round 0 de revisão do controlador.
# ! Motivo: só com hífen, um id como 'campo_ausente' era recusado como id_invalido antes de
# chegar à checagem de id_repetido, que vem depois na ordem; como TODOS os ids de erros/ e
# TODOS os 23 nomes de causa raiz de taxonomia.CAUSAS_RAIZ usam sublinhado, a recusa "esse id
# já existe" nunca acontecia e o histograma de rejeições sempre diria 'formato do id' quando
# o defeito real era o modelo tentar recriar um verbete que já existe. As duas formas do
# repositório passam a valer: 'campo_ausente' (erros/) e 'contrato-produto' (contratos/).
# Maiúscula e espaço continuam fora: o id vira o nome do arquivo .md e bib.validar exige
# id == nome do arquivo. 40 caracteres é o teto do nome.
ID_VERBETE_RE = re.compile(r"^[a-z0-9]+([-_][a-z0-9]+)*$")
MAX_CHARS_ID_VERBETE = 40

# Nome de arquivo de código citado dentro do TEXTO da proposta. O \b no fim evita casar
# "arquivo.js" dentro de "arquivo.jsonl" (o sufixo continua em caractere de palavra).
ARQUIVO_CITADO_RE = re.compile(r"[\w/\\.-]+\.(?:py|php|sql|js)\b")
# Endpoint citado no TEXTO; o id numérico vira {id} do mesmo jeito que
# recuperacao.sinais_do_caso normaliza a requisição do caso, para comparar com bib.ENDPOINTS.
# ! Alteração de IA - Revisar: a rota para em espaço, '?', '|' ou ')' — a MESMA classe
# `[^\s?|)]+` de recuperacao.sinais_do_caso — em vez de \S+ — onda final (achado C3).
# ! Motivo: 15 casos do banco apresentam a requisição com query string
# ("GET /api/pedidos?login=11122233344"); o modelo cita o endpoint como o viu, e com \S+ a
# rota comparada com bib.ENDPOINTS levava a query junto e caía em endpoint_inexistente por
# uma rota que existe.
ENDPOINT_CITADO_RE = re.compile(r"\b(GET|POST|PUT|DELETE)\s+(/api/[^\s?|)]+)")
TABELA_CITADA_RE = re.compile(r"\b(tb\w+|vw_\w+)\b")
# ! Alteração de IA - Revisar: palavras que começam com "tb" mas não são tabela do banco e
# não podem cair em tabela_inexistente — onda final (achado M11).
# ! Motivo: "tbody" (o elemento HTML em que produtos_api.php monta os cartões) casava com
# TABELA_CITADA_RE e uma nota que explicava a tela era recusada como se citasse uma tabela
# inexistente.
TABELAS_EXCECOES = ("tbody",)

# Separador entre o texto e o motivo na linha da nota (ver bib.NOTA_RE). Um TEXTO que
# contenha esta sequência partiria a linha no lugar errado ao ser relido.
SEPARADOR_NOTA = " — Motivo:"

# Cabeçalho da seção de notas. Procurado com ^...$ em modo multilinha porque
# bib._parse_secoes zera a seção a cada cabeçalho repetido: um SEGUNDO "## Notas do modelo"
# no mesmo arquivo apagaria do parse todas as notas do primeiro.
CABECALHO_NOTAS_RE = re.compile(r"^## Notas do modelo\s*$", re.MULTILINE)

# Prefixo dos arquivos de diff que escrever_diff GERA (diff__E1.json/.md). Desde o round 0 de
# revisão eles são gravados FORA da pasta da época — irmãos de epoca-n/ —, então normalmente
# não aparecem nas varreduras daqui; o prefixo continua na lista porque hash_biblioteca,
# diff_bibliotecas e conferir_somente_acrescimo varrem a pasta inteira com rglob, e um diff
# gravado por engano lá dentro entraria no hash da cópia como se fosse documentação escrita
# pelo modelo. O INDICE.md já entra por ARQUIVOS_IGNORADOS.
PREFIXOS_IGNORADOS = ("diff__",)

# Pastas que não são código do projeto e não podem virar referência de verbete: dependências
# instaladas (.venv, node_modules, vendor), cache do interpretador (__pycache__), as pastas de
# resultados das baterias, os gráficos, a pasta de trabalho dos agentes e a própria
# biblioteca de documentação.
# ! Alteração de IA - Revisar: entram resultados, resultados_alvo, resultados_piloto,
# .superpowers, graficos e base_conhecimento — onda final de correções (achado C2).
# ! Motivo: o índice de nomes varria resultados_alvo/**, onde ficam as cópias da biblioteca
# de cada modelo (bibliotecas/<modelo>/epoca-*/...): no piloto, "pagina-produtos-api.md" era
# resolvido como "ambíguo: 3 arquivos" (a original mais duas épocas do qwen2.5-coder:3b), e o
# veredito de uma proposta passava a depender de quantas pastas epoca-* existiam quando o
# processo começou — diferente entre o 1º e o 4º modelo da fila e depois de cada relance.
# base_conhecimento/ sai porque verbete não é código: uma proposta que cita um .md da própria
# documentação em ARQUIVOS está citando o que a checagem existe para conferir.
PASTAS_IGNORADAS_REPO = (".venv", "__pycache__", "node_modules", "vendor", "resultados",
                         "resultados_alvo", "resultados_piloto", ".superpowers", "graficos",
                         "base_conhecimento")

_basenames_repo: dict[str, list[str]] | None = None
_shingles_por_caso: dict[str, set] = {}


# ! Alteração de IA - Revisar: varre uma vez só (em cache de módulo) os arquivos sob
# Programacao/ e devolve o índice nome-do-arquivo -> caminhos relativos ao repositório, sem as
# pastas de dependência e de cache.
# ! Motivo: a checagem "o arquivo citado existe?" roda a cada proposta; refazer o rglob por
# proposta somaria segundos a cada época sem ganho nenhum — a árvore do repositório não muda
# durante uma corrida. Guardar os CAMINHOS (e não só os nomes) é o que permite trocar um
# 'connect.php' escrito pelo modelo pelo caminho real que vai para o frontmatter, e contar
# quantos arquivos têm o mesmo nome para recusar a citação ambígua. Sem o filtro de pastas, a
# varredura pegava 7.528 arquivos — quase todos de .venv e __pycache__ — e um nome qualquer de
# dependência instalada passaria a valer como referência da documentação; com o filtro são 366,
# só o que é código do projeto.
def _arquivos_por_nome() -> dict[str, list[str]]:
    global _basenames_repo
    if _basenames_repo is None:
        indice: dict[str, list[str]] = {}
        for arq in (bib.RAIZ_REPO / "Programacao").rglob("*"):
            if not arq.is_file() or set(arq.parts) & set(PASTAS_IGNORADAS_REPO):
                continue
            indice.setdefault(arq.name, []).append(
                arq.relative_to(bib.RAIZ_REPO).as_posix())
        _basenames_repo = indice
    return _basenames_repo


# ! Alteração de IA - Revisar: resolve um arquivo citado pela proposta — descarta o ":linha"
# do fim, aceita o caminho completo como veio e, se for só o nome, devolve o caminho real
# quando esse nome existe em UM lugar só de Programacao/. Round 3 de revisão, depois do
# segundo piloto.
# ! Motivo: no piloto o modelo escreveu `ARQUIVOS: connect.php:16` e a proposta foi recusada
# como arquivo_inexistente, embora Programacao/CobaiaFront/conn/connect.php exista — a
# recusa era pela FORMA da referência, não por alucinação, e é assim que a própria
# documentação escrita à mão cita arquivos em prosa ("fault_injection.py", "produtos.py
# _to_dict"). O caminho devolvido é o real, e não o nome que o modelo escreveu, porque é ele
# que vai para o campo 'arquivos' do frontmatter: bib.validar confere item a item se
# (RAIZ_REPO / caminho) existe, e um 'connect.php' solto lá dentro deixaria a cópia inválida
# no fechamento da época. Nome que casa com mais de um arquivo (index.php aparece 3 vezes em
# CobaiaFront) continua recusado: escolher um dos três seria inventar a referência.
def _resolver_arquivo(citado: str) -> tuple[str | None, str]:
    """(caminho relativo ao repositório, "") quando resolve; (None, motivo) quando não."""
    item = re.sub(r":\d+$", "", citado.strip()).replace("\\", "/")
    if not item:
        return None, "referência vazia"
    # ! Alteração de IA - Revisar: exists() virou is_file() — onda final de correções.
    # ! Motivo: com exists(), "Programacao" ou "Programacao/CobaiaFront/conn" (pastas) eram
    # aceitos como referência de arquivo e iam para o campo 'arquivos' do frontmatter, que
    # bib.validar confere com exists() também — a pasta passava nas duas e a documentação
    # citava um caminho que não é código.
    if (bib.RAIZ_REPO / item).is_file():
        return item, ""
    achados = _arquivos_por_nome().get(item.rsplit("/", 1)[-1], [])
    if len(achados) == 1:
        return achados[0], ""
    if not achados:
        return None, "não existe no repositório"
    return None, f"ambíguo: {len(achados)} arquivos com esse nome em Programacao/"


# ! Alteração de IA - Revisar: 5-gramas de palavras de um caso (sintoma + observação +
# corpo), em cache por id de caso.
# ! Motivo: a checagem de cópia compara a proposta contra os 90 casos; sem cache, cada
# proposta retokenizaria os 90 casos inteiros (o corpo de alguns passa de 1.000 caracteres).
# O texto é montado igual ao de bib.validar para as duas checagens medirem a mesma coisa.
def _shingles_do_caso(caso: dict) -> set:
    if caso["id"] not in _shingles_por_caso:
        e = caso["entrada"]
        texto = " ".join(str(e.get(k, "")) for k in ("sintoma", "observacao", "corpo"))
        _shingles_por_caso[caso["id"]] = bib._shingles(bib.tokens(texto))
    return _shingles_por_caso[caso["id"]]


def _e_gerado(nome: str) -> bool:
    """! Alteração de IA - Revisar: True para arquivo GERADO pela Fase 3 (INDICE.md, escrito
    por validar_banco.escrever_indice, e os diff__*.json/.md de escrever_diff), que não é
    verbete e não pode entrar em nenhuma varredura de biblioteca.
    ! Motivo: as varreduras daqui (hash_biblioteca, diff_bibliotecas,
    conferir_somente_acrescimo) pegam todos os .md da pasta com rglob. Um diff gravado dentro
    da pasta de uma época entraria no hash da cópia como se fosse documentação escrita pelo
    modelo e, na época seguinte, apareceria como 'arquivo sumiu' no invariante de
    somente-acréscimo. Desde o round 0 de revisão os diffs são gravados fora das pastas de
    época, e este filtro é a defesa para uma pasta gerada antes dessa mudança ou para alguém
    voltar a apontar escrever_diff para dentro da cópia."""
    return (nome.upper() in {n.upper() for n in ARQUIVOS_IGNORADOS}
            or nome.startswith(PREFIXOS_IGNORADOS))


def _carregar_verbetes(raiz: Path) -> list[dict]:
    """! Alteração de IA - Revisar: bib.carregar(raiz) sem os arquivos gerados pela própria
    Fase 3 (diff__*.md).
    ! Motivo: bib.carregar só pula INDICE.md. Um diff__E1.md dentro de uma pasta de época
    seria lido como verbete e bib.validar acusaria 'frontmatter ilegível — arquivo não começa
    com ---' (medido), parando o fechamento por um arquivo que a própria ferramenta escreveu.
    Os diffs passaram a ser gravados fora das pastas de época no round 0 de revisão; o filtro
    fica porque quem chama aqui (fechar_epoca, conferir_somente_acrescimo) não tem como saber
    o que já existe na pasta que recebeu."""
    return [v for v in bib.carregar(raiz) if not _e_gerado(v["caminho"].name)]


def _rejeitar(motivo: str, detalhe: str) -> dict:
    """! Alteração de IA - Revisar: monta a resposta de recusa de validar_proposta, sempre
    com edicao=None.
    ! Motivo: são 30 pontos de saída diferentes em validar_proposta; montando o dicionário na
    mão em cada um, bastava esquecer a chave "edicao" em um deles para o executor tentar
    gravar a edição de uma proposta que foi recusada."""
    return {"aceita": False, "motivo": motivo, "detalhe": detalhe, "edicao": None}


def _uma_linha(valor: str) -> str:
    """! Alteração de IA - Revisar: reduz um campo da proposta a uma linha só — quebras de
    linha e espaços repetidos viram um espaço.
    ! Motivo: a nota é gravada como UMA linha do .md e relida por bib.NOTA_RE linha a linha;
    uma quebra no meio do TEXTO partiria a nota em duas e a segunda metade viraria "nota
    malformada na linha N" na validação do verbete, sem dizer de onde veio."""
    return re.sub(r"\s+", " ", valor or "").strip()


def _lista_de_campo(valor: str, normalizar: bool = False) -> list[str]:
    """! Alteração de IA - Revisar: lê um campo de lista da proposta (CAUSAS, ARQUIVOS,
    PALAVRAS_CHAVE, SINTOMAS) separando por vírgula; 'nenhum'/'nenhuma'/vazio dão lista vazia.
    ! Motivo: o prompt pede para escrever NENHUMA quando não há item, e sem tratar essa
    palavra o modelo acabaria com uma palavra-chave literal "nenhuma" no frontmatter do
    verbete — que entraria no índice do BM25 e casaria com qualquer caso."""
    itens = []
    for bruto in (valor or "").split(","):
        item = bib.normalizar(bruto) if normalizar else bruto.strip()
        if not item or item.lower() in ("nenhum", "nenhuma"):
            continue
        itens.append(item)
    return itens


def _itens_a_acrescentar(atuais: list[str], novos: list[str]) -> list[str]:
    """! Alteração de IA - Revisar: itens de `novos` que ainda não estão em `atuais`
    (comparados por bib.normalizar) e sem repetir dentro do próprio `novos`.
    ! Motivo: a mesma regra tem de valer na gravação em disco (aplicar_edicao) e na edição em
    memória (aplicar_em_memoria); se cada uma dedupasse de um jeito, o frontmatter medido
    antes de aceitar a proposta não seria o frontmatter gravado depois. Comparar normalizado
    evita "Undefined" entrar de novo numa lista que já tem "undefined"."""
    vistos = {bib.normalizar(a) for a in atuais}
    saida = []
    for item in novos:
        chave = bib.normalizar(item)
        if chave in vistos:
            continue
        vistos.add(chave)
        saida.append(item)
    return saida


def _linha_nota(edicao: dict) -> str:
    """! Alteração de IA - Revisar: monta a linha que a nota ocupa na seção "## Notas do
    modelo", no formato de bib.NOTA_RE.
    ! Motivo: a linha é montada em dois lugares (a gravação em disco e a edição em memória que
    validar_proposta mede antes de aceitar); escrita duas vezes, uma diferença de espaço faria
    a nota medida não ser a nota gravada."""
    if edicao["operacao"] == "retificacao":
        rotulo = f'retificação de "{edicao["trecho"]}"'
    else:
        rotulo = "nota"
    return (f'- [E{edicao["epoca"]} · {edicao["caso"]} · {rotulo}] '
            f'{edicao["texto"]} — Motivo: {edicao["motivo"]}')


def _palavras_chave_do_novo(edicao: dict) -> list[str]:
    """! Alteração de IA - Revisar: palavras_chave do verbete novo — as que o modelo propôs
    ou, se ele não mandou nenhuma, as palavras do título.
    ! Motivo: palavras_chave está em bib.OBRIGATORIOS, então um verbete novo sem ele deixaria
    a cópia inteira inválida no fechamento da época; e, mesmo passando, um verbete sem
    palavra-chave quase não é recuperado pelo BM25 e só ocuparia espaço na pasta
    aprendidos/."""
    return list(edicao["palavras_chave_novas"]) or bib.tokens(edicao["novo"]["titulo"])


def _raiz_dos_verbetes(verbetes: list[dict]) -> Path:
    """! Alteração de IA - Revisar: descobre a pasta da biblioteca a partir dos próprios
    verbetes (todo verbete mora em <raiz>/<pasta>/<id>.md, então a raiz é a avó do arquivo).
    ! Motivo: aplicar_em_memoria recebe só a lista de verbetes e a edição, e precisa montar o
    "caminho" do verbete novo com o MESMO valor que bib.carregar devolve depois da gravação —
    senão o teste que compara memória com disco acusaria diferença num campo que não tem nada
    a ver com o conteúdo do verbete."""
    return verbetes[0]["caminho"].parent.parent if verbetes else Path(".")


def _caso_de(ctx: dict) -> dict | None:
    """! Alteração de IA - Revisar: acha, entre os 90, o caso que originou a proposta.
    ! Motivo: quando o modelo esquece o campo ENTIDADE de um verbete novo, a entidade sai de
    recuperacao.sinais_do_caso(caso) — e o ctx só traz o id do caso, não o caso."""
    return next((c for c in ctx["casos"] if c["id"] == ctx["caso_id"]), None)


# Pares de aspas que o modelo usa para delimitar o TRECHO copiado do verbete: retas, simples,
# tipográficas e angulares.
_PARES_DE_ASPAS = (('"', '"'), ("'", "'"), ("“", "”"), ("«", "»"), ("‘", "’"))


def _sem_aspas_delimitadoras(texto: str) -> str:
    """! Alteração de IA - Revisar: tira UM par de aspas que envolva o texto inteiro
    (\"...\", '...', “...”, «...», ‘...’) — onda final (achado C1).
    ! Motivo: no piloto, 2 das 4 retificações do qwen2.5-coder:3b vieram como
    TRECHO: "o parse falha no primeiro caractere" — o trecho existia no verbete, mas o
    validador comparava com as aspas e recusava como trecho_nao_encontrado; a troca de
    aspas por apóstrofo só acontecia DEPOIS da comparação. As aspas em volta são só a forma
    como o modelo cita; aspas no meio do trecho continuam fazendo parte dele."""
    t = texto.strip()
    for abre, fecha in _PARES_DE_ASPAS:
        if len(t) >= 2 and t.startswith(abre) and t.endswith(fecha):
            return t[1:-1].strip()
    return t


def _sem_colchetes(valor: str) -> str:
    """! Alteração de IA - Revisar: tira os colchetes que envolvem o valor inteiro
    ("[Campo ausente]" -> "Campo ausente") — onda final (achado M10).
    ! Motivo: o prompt mostra o id do verbete entre colchetes e o modelo estende a forma ao
    TITULO. Gravado assim, "titulo: [Campo ausente]" é lido por bib._parse_frontmatter como
    LISTA, e bib.validar aborta com TypeError ao juntar o título ao texto do verbete
    (_texto_completo faz " ".join) — o executor cairia no meio da época por um par de
    colchetes. Tira também camadas repetidas ("[[Campo ausente]]"): a re-revisão da onda
    final mostrou que, com um par só, o segundo par ia parar no frontmatter e o mesmo
    TypeError voltava na época seguinte."""
    v = valor.strip()
    while len(v) >= 2 and v.startswith("[") and v.endswith("]"):
        v = v[1:-1].strip()
    return v


def _normalizar_sistema(sistema: str) -> str:
    """! Alteração de IA - Revisar: "CobaiaFront, CobaiaAPI" (ou com "/" ou " e ") vira
    "Ambos"; qualquer outro valor volta como está, para a checagem de vocabulário decidir —
    onda final (achado M15).
    ! Motivo: no piloto o modelo escreveu SISTEMA: CobaiaFront, CobaiaAPI em 2 verbetes
    novos; bib.SISTEMAS já tem o valor "Ambos" exatamente para esse caso, e recusar por
    vocabulario uma resposta que só soletrou os dois sistemas mediria a forma, não o
    conteúdo. Lista com algo fora dos dois (ex.: "CobaiaFront, Mainframe") continua caindo
    em vocabulario."""
    partes = [p.strip() for p in re.split(r"\s*(?:,|/|\be\b)\s*", sistema) if p.strip()]
    if len(partes) > 1 and set(partes) == {"CobaiaFront", "CobaiaAPI"}:
        return "Ambos"
    return sistema.strip()


# ! Alteração de IA - Revisar: aplica uma edição aos dicionários de verbete, numa cópia
# profunda da lista, sem tocar em disco.
# ! Motivo: sete das checagens de validar_proposta (teto de notas do verbete, tamanho do
# verbete novo, orçamento do prompt de diagnóstico, sobreposição acumulada com os casos e o
# restante de bib.validar) só podem ser medidas DEPOIS da edição aplicada. Aplicar em disco
# para medir e desfazer em caso de rejeição deixaria a cópia da biblioteca do modelo num
# estado intermediário se a execução caísse no meio; a cópia profunda mede o mesmo resultado
# sem escrever nada. O formato tem de bater byte a byte com o que aplicar_edicao grava (é o
# que teste_aplicar_e_somente_acrescimo confere).
def aplicar_em_memoria(verbetes: list[dict], edicao: dict) -> list[dict]:
    saida = copy.deepcopy(verbetes)
    if edicao["operacao"] == "novo_verbete":
        novo = edicao["novo"]
        meta = {"id": edicao["verbete"], "titulo": novo["titulo"],
                "sistema": novo["sistema"], "entidade_principal": novo["entidade"],
                "tipo": "aprendido", "status": "ativo"}
        if novo["arquivos"]:
            meta["arquivos"] = list(novo["arquivos"])
        if edicao["sintomas_novos"]:
            meta["sintomas"] = list(edicao["sintomas_novos"])
        meta["palavras_chave"] = _palavras_chave_do_novo(edicao)
        meta["causas_relacionadas"] = list(novo["causas"])
        secoes = {"Resumo": edicao["texto"]}
        if edicao["sintomas_novos"]:
            secoes["Sinais"] = "\n".join(f"- {s}" for s in edicao["sintomas_novos"])
        saida.append({
            "id": edicao["verbete"], "pasta": PASTA_APRENDIDOS,
            "caminho": (_raiz_dos_verbetes(saida) / PASTA_APRENDIDOS
                        / f"{edicao['verbete']}.md"),
            "meta": meta, "secoes": secoes})
        return saida

    alvo = next(v for v in saida if v["id"] == edicao["verbete"])
    for chave, propostos in (("palavras_chave", edicao["palavras_chave_novas"]),
                             ("sintomas", edicao["sintomas_novos"])):
        atuais = alvo["meta"].get(chave, [])
        acrescentar = _itens_a_acrescentar(atuais, propostos)
        if acrescentar:
            alvo["meta"][chave] = list(atuais) + acrescentar
    atual = alvo["secoes"].get("Notas do modelo", "")
    linha = _linha_nota(edicao)
    alvo["secoes"]["Notas do modelo"] = f"{atual}\n{linha}" if atual else linha
    return saida


# ! Alteração de IA - Revisar: validar_proposta decide, só em código, se um bloco PROPOSTA
# entra na cópia da biblioteca do modelo; devolve aceita/motivo/detalhe/edicao, com o motivo
# sempre em um dos códigos de CODIGOS_REJEICAO.
# ! Motivo: é a trava central da Fase 3. O achado 4.24 da Fase 2-B mediu que os modelos
# seguem a documentação em 93–96% dos casos mesmo quando ela está errada — então uma
# proposta errada aceita hoje contamina todos os diagnósticos das épocas seguintes, e o
# experimento passaria a medir o estrago em vez do aprendizado. As checagens são as mesmas
# que bib.validar já faz na biblioteca escrita à mão (vocabulário fechado, arquivos/tabelas/
# endpoints que existem, nada de copiar caso do banco), mais os tetos de tamanho que mantêm o
# prompt dentro do num_ctx de 8192. A ordem das checagens é fixa e a primeira que falha
# decide: o histograma de rejeições só é comparável entre modelos se o mesmo defeito cair
# sempre no mesmo código. Nenhuma proposta é truncada, podada ou corrigida em silêncio — ou
# entra inteira, ou é recusada com o código.
def validar_proposta(bloco: dict, ctx: dict) -> dict:
    if bloco is None:
        return _rejeitar("sem_bloco", "resposta sem bloco PROPOSTA e sem NENHUMA")
    if bloco.get("malformado"):
        return _rejeitar("bloco_malformado", bloco["malformado"])

    campos = bloco.get("campos", {})
    texto = _uma_linha(campos.get("TEXTO", ""))
    motivo = _uma_linha(campos.get("MOTIVO", ""))
    if SEPARADOR_NOTA in texto:
        return _rejeitar("bloco_malformado", "texto contém o separador da nota")

    numero = bloco.get("numero", 1)
    if numero > MAX_PROPOSTAS_POR_CASO:
        return _rejeitar("excesso_de_propostas",
                         f"bloco PROPOSTA {numero} acima do teto de "
                         f"{MAX_PROPOSTAS_POR_CASO} por caso")
    if ctx["aceitas_no_caso"] >= MAX_PROPOSTAS_POR_CASO:
        return _rejeitar("excesso_de_propostas",
                         f"{ctx['aceitas_no_caso']} proposta(s) já aceitas neste caso")

    operacao = bib.normalizar(campos.get("OPERACAO", ""))
    if operacao not in OPERACOES:
        return _rejeitar("operacao_invalida",
                         f"OPERACAO '{campos.get('OPERACAO', '')}' fora de {OPERACOES}")

    alvo_id = campos.get("VERBETE", "").strip()
    por_id = {v["id"]: v for v in ctx["verbetes"]}
    alvo = None
    # SISTEMA com os dois sistemas listados é "Ambos" (ver _normalizar_sistema).
    sistema = _normalizar_sistema(campos.get("SISTEMA", ""))
    entidade = campos.get("ENTIDADE", "").strip()
    causas: list[str] = []
    if operacao in ("nota", "retificacao"):
        alvo = por_id.get(alvo_id)
        if alvo is None:
            return _rejeitar("alvo_inexistente", f"não há verbete com id '{alvo_id}'")
        if alvo_id not in ctx["ids_visiveis"]:
            return _rejeitar("alvo_nao_visto",
                             f"'{alvo_id}' não estava entre os verbetes do diagnóstico")
    else:
        if len(alvo_id) > MAX_CHARS_ID_VERBETE or not ID_VERBETE_RE.match(alvo_id):
            return _rejeitar("id_invalido", f"id '{alvo_id}' fora de minusculas com hifen "
                             f"ou sublinhado, ou acima de {MAX_CHARS_ID_VERBETE} chars")
        if alvo_id in por_id or alvo_id in CAUSAS_RAIZ:
            return _rejeitar("id_repetido", f"'{alvo_id}' já é id de verbete ou nome de "
                             "causa raiz")
        if ctx["novos_nesta_epoca"] >= TETO_VERBETES_NOVOS_POR_EPOCA:
            return _rejeitar("teto_verbetes_novos",
                             f"{ctx['novos_nesta_epoca']} verbetes novos nesta época "
                             f"(teto {TETO_VERBETES_NOVOS_POR_EPOCA})")
        if PASTA_APRENDIDOS not in bib._ORDEM_PASTAS:
            return _rejeitar("pasta_invalida", f"pasta '{PASTA_APRENDIDOS}' não está na "
                             "ordem de pastas do prompt")
        if sistema and sistema not in bib.SISTEMAS:
            return _rejeitar("vocabulario", f"sistema '{sistema}' fora de "
                             f"{sorted(bib.SISTEMAS)}")
        if entidade and entidade not in bib.ENTIDADES:
            return _rejeitar("vocabulario", f"entidade '{entidade}' fora de "
                             f"{sorted(bib.ENTIDADES)}")
        causas = _lista_de_campo(campos.get("CAUSAS", ""))
        if not causas or len(causas) > 3 or any(c not in CAUSAS_RAIZ for c in causas):
            return _rejeitar("causa_fora_do_conjunto",
                             f"CAUSAS={causas} (1 a 3 nomes do conjunto fechado)")

    # ! Alteração de IA - Revisar: cada item de ARQUIVOS e cada nome de arquivo citado no
    # TEXTO passa por _resolver_arquivo; o item guardado na edição é o caminho RESOLVIDO —
    # round 3 de revisão, depois do segundo piloto.
    # ! Motivo: o modelo cita arquivo como a documentação cita em prosa, pelo nome e às vezes
    # com a linha ("connect.php:16"); exigir o caminho completo recusava proposta boa por
    # forma da referência. Guardar o caminho resolvido, e não o nome escrito pelo modelo, é o
    # que mantém o campo 'arquivos' do frontmatter válido para bib.validar, que confere se
    # cada caminho existe em disco.
    arquivos = []
    for item in _lista_de_campo(campos.get("ARQUIVOS", "")):
        resolvido, erro = _resolver_arquivo(item)
        if resolvido is None:
            return _rejeitar("arquivo_inexistente", f"ARQUIVOS cita '{item}': {erro}")
        arquivos.append(resolvido)
    for citado in ARQUIVO_CITADO_RE.findall(texto):
        _, erro = _resolver_arquivo(citado)
        if erro:
            return _rejeitar("arquivo_inexistente",
                             f"o TEXTO cita o arquivo '{citado}': {erro}")
    for verbo, caminho in ENDPOINT_CITADO_RE.findall(texto):
        rota = re.sub(r"/\d+(?=/|$)", "/{id}", caminho.rstrip(".,;:!?)"))
        if f"{verbo} {rota}" not in bib.ENDPOINTS:
            return _rejeitar("endpoint_inexistente",
                             f"o TEXTO cita '{verbo} {rota}', que não é rota do CobaiaAPI")
    for tabela in TABELA_CITADA_RE.findall(texto):
        if tabela not in bib.TABELAS and tabela.lower() not in TABELAS_EXCECOES:
            return _rejeitar("tabela_inexistente",
                             f"o TEXTO cita a tabela '{tabela}', que não existe no banco")

    if len(texto) < TEXTO_MIN:
        return _rejeitar("texto_curto", f"TEXTO com {len(texto)} caracteres "
                         f"(mínimo {TEXTO_MIN})")
    if len(texto) > TEXTO_MAX:
        return _rejeitar("texto_longo", f"TEXTO com {len(texto)} caracteres "
                         f"(máximo {TEXTO_MAX})")
    if not motivo:
        return _rejeitar("motivo_ausente", "proposta sem MOTIVO")
    if len(motivo) < MOTIVO_MIN:
        return _rejeitar("motivo_curto", f"MOTIVO com {len(motivo)} caracteres "
                         f"(mínimo {MOTIVO_MIN})")
    if len(motivo) > MOTIVO_MAX:
        return _rejeitar("motivo_longo", f"MOTIVO com {len(motivo)} caracteres "
                         f"(máximo {MOTIVO_MAX})")

    trecho = None
    if operacao == "retificacao":
        # As aspas que o modelo põe em volta do trecho saem ANTES do mínimo de 15
        # caracteres e da busca no verbete (ver _sem_aspas_delimitadoras).
        trecho_bruto = _sem_aspas_delimitadoras(_uma_linha(campos.get("TRECHO", "")))
        if len(trecho_bruto) < 15:
            return _rejeitar("retificacao_sem_trecho",
                             f"TRECHO com {len(trecho_bruto)} caracteres (mínimo 15)")
        if bib.normalizar(trecho_bruto) not in bib.normalizar(bib.render_base(alvo)):
            return _rejeitar("trecho_nao_encontrado",
                             f"'{trecho_bruto[:60]}' não aparece em [{alvo_id}]")
        # As aspas delimitam o trecho na linha da nota (bib.NOTA_RE); uma aspa dentro dele
        # fecharia a retificação no meio da frase ao reler o verbete.
        trecho = trecho_bruto.replace('"', "'")

    palavras = _lista_de_campo(campos.get("PALAVRAS_CHAVE", ""), normalizar=True)
    sintomas = _lista_de_campo(campos.get("SINTOMAS", ""), normalizar=True)
    if len(palavras) > MAX_PALAVRAS_CHAVE_NOVAS:
        return _rejeitar("palavra_chave_invalida",
                         f"{len(palavras)} palavras-chave (teto {MAX_PALAVRAS_CHAVE_NOVAS})")
    if len(sintomas) > MAX_SINTOMAS_NOVOS:
        return _rejeitar("palavra_chave_invalida",
                         f"{len(sintomas)} sintomas (teto {MAX_SINTOMAS_NOVOS})")
    for item in palavras + sintomas:
        if len(item) > MAX_CHARS_ITEM_LISTA or not ITEM_LISTA_RE.match(item):
            return _rejeitar("palavra_chave_invalida",
                             f"item de lista inválido: '{item}'")

    if alvo is not None:
        normalizado = bib.normalizar(texto)
        for nota in bib.notas(alvo):
            if bib.normalizar(nota["texto"]) == normalizado:
                return _rejeitar("duplicada",
                                 f"[{alvo_id}] já tem uma nota com este texto")

    if CASO_ID_RE.search(texto) or CASO_ID_RE.search(motivo):
        return _rejeitar("copia_do_caso", "TEXTO/MOTIVO cita o id de um caso do banco")
    sh_prop = bib._shingles(bib.tokens(
        " ".join([texto, motivo, trecho or "", *palavras, *sintomas])))
    if len(sh_prop) >= 5:
        for caso in ctx["casos"]:
            sh_caso = _shingles_do_caso(caso)
            if not sh_caso:
                continue
            razao = len(sh_prop & sh_caso) / len(sh_prop)
            if razao >= LIMIAR_COPIA_PROPOSTA:
                return _rejeitar("copia_do_caso",
                                 f"{razao:.0%} dos 5-gramas da proposta são do caso "
                                 f"{caso['id']}")

    if operacao == "novo_verbete":
        caso_atual = _caso_de(ctx)
        # SISTEMA/ENTIDADE esquecidos não recusam a proposta: o padrão é 'Ambos' e a
        # entidade que recuperacao.sinais_do_caso lê da requisição do caso (Interface quando
        # o caso não tem endpoint, como nos casos de seletor quebrado).
        entidade_final = entidade or (rec.sinais_do_caso(caso_atual)["entidade"]
                                      if caso_atual else None) or "Interface"
        novo = {"titulo": _sem_colchetes(_uma_linha(campos.get("TITULO", ""))),
                "sistema": sistema or "Ambos", "entidade": entidade_final,
                "causas": causas, "arquivos": arquivos}
        arquivo = f"{PASTA_APRENDIDOS}/{alvo_id}.md"
    else:
        novo = None
        arquivo = alvo["caminho"].relative_to(ctx["raiz"]).as_posix()

    edicao = {"epoca": ctx["epoca"], "caso": ctx["caso_id"], "numero": numero,
              "operacao": operacao, "verbete": alvo_id, "arquivo": arquivo,
              "texto": texto, "motivo": motivo, "trecho": trecho,
              "palavras_chave_novas": palavras, "sintomas_novos": sintomas,
              "novo": novo, "modelo": ctx["modelo"]}

    verbetes_mod = aplicar_em_memoria(ctx["verbetes"], edicao)
    alvo_mod = next(v for v in verbetes_mod if v["id"] == alvo_id)
    rot = f"{alvo_mod['pasta']}/{alvo_mod['caminho'].name}"
    if operacao == "novo_verbete":
        tam = len(bib.render_base(alvo_mod))
        if tam > bib.TETO_CHARS_VERBETE:
            return _rejeitar("teto_verbete_novo", f"verbete novo com {tam} caracteres "
                             f"renderizados (teto {bib.TETO_CHARS_VERBETE})")
    else:
        tam_notas = len(bib.render_notas(alvo_mod))
        n_notas = len(bib.notas(alvo_mod))
        if tam_notas > bib.TETO_CHARS_NOTAS_VERBETE:
            return _rejeitar("teto_notas_verbete", f"[{alvo_id}] ficaria com {tam_notas} "
                             f"caracteres de notas (teto {bib.TETO_CHARS_NOTAS_VERBETE})")
        if n_notas > bib.TETO_NOTAS_POR_VERBETE:
            return _rejeitar("teto_notas_verbete", f"[{alvo_id}] ficaria com {n_notas} "
                             f"notas (teto {bib.TETO_NOTAS_POR_VERBETE})")

    indice_mod = rec.Indice(verbetes_mod)
    for caso in ctx["casos"]:
        ctx_texto = rec.contexto(verbetes_mod, indice_mod, caso, "A2", ctx["k"])["texto"]
        tokens_ctx = bib.estimar_tokens(ctx_texto)
        if tokens_ctx > TETO_TOKENS_CONTEXTO:
            return _rejeitar("teto_prompt", f"contexto do caso {caso['id']} iria a "
                             f"{tokens_ctx} tokens (teto {TETO_TOKENS_CONTEXTO})")
        tokens_prompt = bib.estimar_tokens(est.linear_com_biblioteca(caso, ctx_texto))
        if tokens_prompt > ORCAMENTO_PROMPT_DIAG:
            return _rejeitar("teto_prompt", f"prompt de diagnóstico do caso {caso['id']} "
                             f"iria a {tokens_prompt} tokens (orçamento "
                             f"{ORCAMENTO_PROMPT_DIAG})")

    problemas = bib.validar(verbetes_mod, ctx["casos"], teto_global=None)
    citam_alvo = [p for p in problemas if rot in p]
    copia = next((p for p in citam_alvo if "5-gramas" in p), None)
    if copia:
        return _rejeitar("copia_do_caso_acumulada", copia)
    if problemas:
        return _rejeitar("biblioteca_invalida", (citam_alvo or problemas)[0])

    return {"aceita": True, "motivo": None,
            "detalhe": f"{operacao} em [{alvo_id}]", "edicao": edicao}


# ------------------------------------------------------- aplicação da edição em disco

def _itens_da_linha(linha: str) -> list[str]:
    """! Alteração de IA - Revisar: lê os itens de uma linha de lista do frontmatter
    ("chave: [a, b]") com a mesma regra de bib._parse_frontmatter.
    ! Motivo: a edição é textual (a linha é alterada, não reescrita a partir do dicionário),
    então quem acrescenta itens precisa saber o que já está ESCRITO na linha; usar outra regra
    de leitura faria a dedupe divergir do que bib.carregar lê depois."""
    dentro = linha[linha.find("[") + 1:linha.rfind("]")]
    return [v.strip() for v in dentro.split(",") if v.strip()]


def _linha_com_itens(linha: str, novos: list[str]) -> str:
    """! Alteração de IA - Revisar: acrescenta itens ao FIM de uma linha de lista do
    frontmatter, trocando só o "]" final (e sem a vírgula quando a lista estava vazia).
    ! Motivo: reescrever a linha inteira a partir dos itens mudaria o espaçamento escrito à
    mão e faria o diff da época apontar uma alteração que ninguém pediu; e concatenar ", item"
    numa lista vazia deixaria "[, item]" no arquivo."""
    fecha = linha.rfind("]")
    if fecha < 0:
        return linha
    tem_item = bool(_itens_da_linha(linha))
    juncao = ", ".join(novos)
    return linha[:fecha] + (f", {juncao}" if tem_item else juncao) + linha[fecha:]


# ! Alteração de IA - Revisar: acrescenta ao frontmatter, por edição de texto, os itens
# novos de palavras_chave/sintomas e uma linha de rastreio da edição do modelo.
# ! Motivo: reescrever o frontmatter inteiro a partir do dicionário de bib.carregar
# apagaria os comentários '# ! Alteração de IA - Revisar' / '# ! Motivo' de cada verbete
# (bib._parse_frontmatter pula as linhas com '#', então elas não voltam do parse) e
# perderia a ordem das chaves escrita à mão. Mexendo só na linha da chave, tudo o que já
# estava no arquivo continua exatamente onde estava — que é o que o invariante de
# somente-acréscimo cobra depois.
def _acrescentar_ao_frontmatter(texto: str, edicao: dict) -> str:
    linhas = texto.split("\n")
    fim = next((i for i, l in enumerate(linhas) if i > 0 and l.strip() == "---"), None)
    if fim is None:
        raise ValueError(f"frontmatter sem '---' de fechamento em {edicao['arquivo']}")

    for chave, propostos in (("palavras_chave", edicao["palavras_chave_novas"]),
                             ("sintomas", edicao["sintomas_novos"])):
        if not propostos:
            continue
        indice = next((i for i in range(1, fim)
                       if linhas[i].lstrip().startswith(f"{chave}:")), None)
        if indice is None:
            linhas.insert(fim, f"{chave}: [{', '.join(propostos)}]")
            fim += 1
            continue
        novos = _itens_a_acrescentar(_itens_da_linha(linhas[indice]), propostos)
        if novos:
            linhas[indice] = _linha_com_itens(linhas[indice], novos)

    rotulo = "retificação" if edicao["operacao"] == "retificacao" else "nota"
    linhas.insert(fim, f"# ! Alteração por modelo {edicao['modelo']} "
                       f"(E{edicao['epoca']}, caso {edicao['caso']}) - Revisar: "
                       f"{rotulo} acrescentada.")
    return "\n".join(linhas)


def _texto_verbete_novo(edicao: dict) -> str:
    """! Alteração de IA - Revisar: monta o .md completo de um verbete novo (tipo
    "aprendido"), na mesma ordem de chaves dos verbetes escritos à mão em base_conhecimento/.
    ! Motivo: o arquivo tem de sair válido para bib.validar de primeira (id igual ao nome do
    arquivo, palavras_chave e causas_relacionadas preenchidos, "## Resumo" presente), porque
    um verbete novo inválido só apareceria no fechamento da época, quando já não dá para
    recusar a proposta. As duas primeiras linhas de comentário marcam, dentro do próprio
    verbete, que ele foi escrito por um modelo e em que época e caso."""
    novo = edicao["novo"]
    linhas = [
        "---",
        f"# ! Alteração de IA - Revisar: verbete criado pelo modelo {edicao['modelo']} na "
        f"época {edicao['epoca']} a partir do caso {edicao['caso']} (Fase 3).",
        f"# ! Motivo: {edicao['motivo']}",
        f"id: {edicao['verbete']}",
        f"titulo: {novo['titulo']}",
        f"sistema: {novo['sistema']}",
        f"entidade_principal: {novo['entidade']}",
        "tipo: aprendido",
        "status: ativo",
    ]
    if novo["arquivos"]:
        linhas.append(f"arquivos: [{', '.join(novo['arquivos'])}]")
    if edicao["sintomas_novos"]:
        linhas.append(f"sintomas: [{', '.join(edicao['sintomas_novos'])}]")
    linhas.append(f"palavras_chave: [{', '.join(_palavras_chave_do_novo(edicao))}]")
    linhas.append(f"causas_relacionadas: [{', '.join(novo['causas'])}]")
    linhas += ["---", "## Resumo", edicao["texto"]]
    if edicao["sintomas_novos"]:
        linhas += ["", "## Sinais"] + [f"- {s}" for s in edicao["sintomas_novos"]]
    return "\n".join(linhas) + "\n"


# ! Alteração de IA - Revisar: grava em disco a edição aceita — nota/retificação ao FIM do
# verbete existente, ou o arquivo novo em aprendidos/ — e devolve o caminho escrito.
# ! Motivo: é a única função da Fase 3 que escreve na cópia da biblioteca do modelo, e ela
# só acrescenta: o texto que já existia no arquivo é lido e regravado igual, com a linha da
# nota no fim. O cabeçalho '## Notas do modelo' é procurado antes de ser criado porque
# bib._parse_secoes zera a seção a cada cabeçalho '##' repetido — um segundo cabeçalho no
# mesmo arquivo faria as notas das épocas anteriores sumirem do parse (e, com elas, do
# prompt), sem erro nenhum aparecer.
def aplicar_edicao(raiz: Path, edicao: dict) -> Path:
    destino = raiz / edicao["arquivo"]
    if edicao["operacao"] == "novo_verbete":
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(_texto_verbete_novo(edicao), encoding="utf-8")
        return destino

    texto = _acrescentar_ao_frontmatter(destino.read_text(encoding="utf-8"), edicao)
    if not texto.endswith("\n"):
        texto += "\n"
    if not CABECALHO_NOTAS_RE.search(texto):
        texto += "\n## Notas do modelo\n"
    texto += _linha_nota(edicao) + "\n"
    destino.write_text(texto, encoding="utf-8")
    return destino


# ! Alteração de IA - Revisar: compara duas cópias da biblioteca e devolve a lista de tudo
# que NÃO foi acréscimo — arquivo sumido, campo do frontmatter alterado, item de lista
# removido ou trocado de lugar, corpo mexido fora do fim e arquivo novo fora de aprendidos/.
# ! Motivo: a Fase 3 mede o que acontece quando o modelo acrescenta à documentação; se uma
# edição apagasse ou reescrevesse o que a Fase 2-B mediu, as duas fases deixariam de ser
# comparáveis e o "verbete de ouro" de uma causa raiz poderia simplesmente sumir no meio da
# corrida. A checagem é feita sobre o que está em disco (e não sobre o que validar_proposta
# aceitou) de propósito: é o que pega um bug de aplicar_edicao, que é justamente o risco.
def conferir_somente_acrescimo(raiz_antiga: Path, raiz_nova: Path) -> list[str]:
    violacoes = []
    antigos = {v["caminho"].relative_to(raiz_antiga).as_posix(): v
               for v in _carregar_verbetes(raiz_antiga)}
    novos = {v["caminho"].relative_to(raiz_nova).as_posix(): v
             for v in _carregar_verbetes(raiz_nova)}

    for rel, va in sorted(antigos.items()):
        vn = novos.get(rel)
        if vn is None:
            violacoes.append(f"{rel}: arquivo sumiu")
            continue
        # id/tipo/causa_raiz são comparados com .get dos DOIS lados: acrescentar um
        # causa_raiz a um verbete que não tinha mudaria o verbete de ouro de uma causa.
        for chave in ("id", "tipo", "causa_raiz"):
            if va["meta"].get(chave) != vn["meta"].get(chave):
                violacoes.append(f"{rel}: '{chave}' mudou de {va['meta'].get(chave)!r} "
                                 f"para {vn['meta'].get(chave)!r}")
        for chave, valor in va["meta"].items():
            if chave in ("id", "tipo", "causa_raiz"):
                continue
            atual = vn["meta"].get(chave)
            if isinstance(valor, list):
                if not isinstance(atual, list) or atual[:len(valor)] != valor:
                    violacoes.append(f"{rel}: lista '{chave}' deixou de começar pelo que "
                                     f"já existia ({valor} -> {atual})")
            elif atual != valor:
                violacoes.append(f"{rel}: '{chave}' mudou de {valor!r} para {atual!r}")
        try:
            corpo_antigo = bib._parse_frontmatter(
                va["caminho"].read_text(encoding="utf-8"))[1].rstrip("\n")
            corpo_novo = bib._parse_frontmatter(
                vn["caminho"].read_text(encoding="utf-8"))[1]
        except ValueError as e:
            violacoes.append(f"{rel}: frontmatter ilegível — {e}")
            continue
        if not corpo_novo.startswith(corpo_antigo):
            violacoes.append(f"{rel}: corpo alterado fora de acréscimo")

    # ! Alteração de IA - Revisar: a varredura de "arquivo novo" passou a olhar TODOS os
    # arquivos da cópia (não só os .md carregados como verbete), fora os gerados pelo
    # fechamento (INDICE.md, fechamento.json, diff__*) — onda final (item 3).
    # ! Motivo: um arquivo novo que não fosse .md (ex.: erros/intruso.txt, um .json solto)
    # passava despercebido, e um .txt dentro de aprendidos/ também: só aplicar_edicao pode
    # escrever na cópia, e o único arquivo que ela cria é um verbete .md em aprendidos/. Tudo
    # que fugir disso é bug do harness ou mão humana na pasta, que é o que o invariante
    # existe para acusar.
    for rel in sorted(_arquivos_da_copia(raiz_nova) - _arquivos_da_copia(raiz_antiga)):
        if not rel.startswith(f"{PASTA_APRENDIDOS}/"):
            violacoes.append(f"{rel}: arquivo novo fora de aprendidos/")
        elif not rel.endswith(".md"):
            violacoes.append(f"{rel}: arquivo novo em aprendidos/ que não é verbete .md")
    return violacoes


def _arquivos_da_copia(raiz: Path) -> set[str]:
    """! Alteração de IA - Revisar: caminhos relativos (posix) de todos os arquivos de uma
    cópia da biblioteca, menos os gerados pelo próprio fechamento (_e_gerado) e os .tmp de
    _gravar_json_atomico — onda final (item 3).
    ! Motivo: é a lista que conferir_somente_acrescimo compara entre duas épocas para achar
    arquivo novo de qualquer tipo; separada em função para a regra do que é "gerado" ficar
    num lugar só (a mesma de _arquivos_md e _carregar_verbetes)."""
    return {a.relative_to(raiz).as_posix() for a in raiz.rglob("*")
            if a.is_file() and not _e_gerado(a.name) and a.suffix != ".tmp"}


# --------------------------------------------------- abertura e fechamento de época

def _limpar_gerados(raiz: Path) -> None:
    """! Alteração de IA - Revisar: apaga da pasta da época recém-copiada os arquivos GERADOS
    pelo fechamento da época anterior (fechamento.json, INDICE.md e qualquer diff__*).
    ! Motivo: copiar_biblioteca clona a pasta inteira da época anterior; sem esta limpeza, a
    epoca-n nasceria com o fechamento.json da epoca-(n-1) dentro e snapshot_fechado(epoca-n)
    diria 'já fechada' antes de o primeiro caso rodar — abrir_epoca devolveria a pasta sem
    reaplicar nada e a época inteira seria pulada em silêncio. O INDICE.md descreve a
    biblioteca da época anterior e é regravado no fechamento; os diff__* só aparecem aqui em
    pastas geradas antes de os diffs saírem de dentro das épocas."""
    # Os *.tmp são restos de _gravar_json_atomico interrompido no meio (onda final, M12).
    for gerado in (list(raiz.glob("diff__*")) + list(raiz.glob("*.tmp"))
                   + [raiz / "fechamento.json", raiz / "INDICE.md"]):
        if gerado.is_file():
            gerado.unlink()


# ! Alteração de IA - Revisar: abre a época n — devolve a pasta se ela já fechou; senão
# copia a época anterior e RECONSTRÓI a época reaplicando, em ordem, as edições aceitas dos
# registros, conferindo o hash ao fim de cada caso.
# ! Motivo: a corrida de uma época leva horas em CPU e pode ser interrompida (queda, Ctrl+C,
# um modelo que trava). O JSONL de execução é a fonte da verdade — ele tem todas as decisões
# e o hash da biblioteca depois de cada caso — e a pasta da época é derivada dele; então
# retomar é reconstruir do zero e comparar o hash, em vez de tentar adivinhar em que arquivo
# a gravação parou. Hash diferente do gravado significa que a biblioteca reconstruída NÃO é
# a que o modelo viu naquele caso: seguir daí mediria diagnósticos contra outra documentação,
# então a execução para com SystemExit dizendo o caso e os dois hashes.
def abrir_epoca(pasta_bib: Path, n: int, registros_propostas: list[dict]) -> Path:
    raiz = pasta_bib / f"epoca-{n}"
    if (raiz / "fechamento.json").exists():
        return raiz
    if raiz.exists():
        shutil.rmtree(raiz)
    copiar_biblioteca(pasta_bib / f"epoca-{n - 1}", raiz)
    _limpar_gerados(raiz)

    reaplicadas: list[tuple[dict, dict]] = []
    for registro in registros_propostas:
        for decisao in registro.get("decisoes", []):
            if decisao.get("aceita") and decisao.get("edicao"):
                aplicar_edicao(raiz, decisao["edicao"])
                reaplicadas.append((decisao["edicao"], registro))
        # ! Alteração de IA - Revisar: registro sem hash_biblioteca_apos (chave ausente,
        # vazia ou None) passou a parar a execução, em vez de pular a conferência — round 1
        # de revisão.
        # ! Motivo: com `if esperado and ...`, o registro sem hash simplesmente não era
        # conferido e a época era reconstruída em silêncio. Esse é exatamente o estado que
        # uma corrida interrompida deixa: a edição foi aplicada em disco e a linha do JSONL
        # ainda não tinha sido fechada com o hash. Seguir dali levantaria uma biblioteca que
        # ninguém comparou com a que o modelo viu — e é justamente essa comparação que
        # sustenta "o JSONL é a fonte da verdade, a pasta da época é derivada dele".
        esperado = registro.get("hash_biblioteca_apos")
        if not esperado:
            raise SystemExit(
                f"registro de proposta do caso {registro.get('caso')} sem "
                f"hash_biblioteca_apos — JSONL incompleto; apague a última linha e relance")
        atual = hash_biblioteca(raiz)
        if atual != esperado:
            raise SystemExit(
                f"reconstrução da época {n} divergiu no caso {registro.get('caso')}: "
                f"o JSONL gravou hash {esperado} e a pasta reconstruída deu {atual} — "
                f"a biblioteca reconstruída não é a que o modelo viu neste caso")

    _refazer_historico_da_epoca(pasta_bib, n, reaplicadas)
    return raiz


# ! Alteração de IA - Revisar: depois de reaplicar as edições de uma época, reescreve as
# linhas dessa época em historico.jsonl — apaga as que existiam com `epoca` igual a n e grava
# de novo, na ordem, as que acabaram de ser reaplicadas; as linhas das outras épocas ficam
# como estavam. Round 2 de revisão, depois do piloto.
# ! Motivo: registrar_historico grava a linha do histórico assim que a edição é aplicada, e o
# JSONL da execução só é fechado depois. Uma queda entre as duas gravações deixa no histórico
# uma linha de uma edição que o JSONL não conhece; como a reconstrução reaplica tudo a partir
# do JSONL, essa linha órfã continuaria lá e a edição seguinte entraria duas vezes no
# histórico — os totais de "quantas notas o modelo escreveu na época 3" sairiam errados sem
# nada indicar o problema. O JSONL é a fonte da verdade; o histórico é derivado dele e é
# refeito junto com a pasta da época.
def _refazer_historico_da_epoca(pasta_bib: Path, n: int,
                                reaplicadas: list[tuple[dict, dict]]) -> None:
    caminho = pasta_bib / "historico.jsonl"
    if not caminho.exists() and not reaplicadas:
        return
    mantidas = []
    if caminho.exists():
        for linha in caminho.read_text(encoding="utf-8").splitlines():
            if not linha.strip():
                continue
            try:
                dado = json.loads(linha)
            except json.JSONDecodeError:
                # Linha cortada no meio da gravação: não dá para saber de que época é, e
                # relê-la como histórico seria inventar dado — a mesma tolerância de
                # executar_bateria.ler_jsonl.
                continue
            if dado.get("epoca") != n:
                mantidas.append(linha)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text("".join(f"{linha}\n" for linha in mantidas), encoding="utf-8")
    for ordem, (edicao, registro) in enumerate(reaplicadas, 1):
        registrar_historico(pasta_bib, edicao, {
            "ordem": ordem,
            "acertou_diagnostico": registro.get("acertou_diagnostico"),
            "hash_apos": registro["hash_biblioteca_apos"]})


def registrar_historico(pasta_bib: Path, edicao: dict, extras: dict) -> None:
    """! Alteração de IA - Revisar: acrescenta a historico.jsonl uma linha por edição
    aplicada (a edição inteira mais os extras do executor: ordem, se o diagnóstico daquele
    caso acertou e o hash depois da aplicação).
    ! Motivo: o fechamento.json fecha o total de cada época, mas a pergunta do Memorial é
    'que edição entrou, em que ordem, vinda de qual caso, e o modelo tinha acertado o
    diagnóstico daquele caso?' — sem uma linha por edição não dá para cruzar acerto do
    diagnóstico com qualidade da proposta. Em append com flush por linha porque a corrida
    pode ser interrompida: o que já foi gravado continua legível."""
    pasta_bib.mkdir(parents=True, exist_ok=True)
    with (pasta_bib / "historico.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({**edicao, **extras}, ensure_ascii=False) + "\n")
        f.flush()


# ! Alteração de IA - Revisar: fecha a época n — valida a cópia inteira, confere o
# invariante de somente-acréscimo contra a época anterior, regrava o INDICE.md, grava os dois
# diffs (contra a época anterior e contra a biblioteca original) FORA da pasta da época, e
# por último o fechamento.json.
# ! Motivo: é o ponto em que a época vira resultado. A validação e o invariante rodam ANTES
# de qualquer gravação porque uma cópia inválida ou com verbete alterado invalida a época
# inteira, e é melhor parar aqui do que descobrir na análise; como toda proposta já passou
# por validar_proposta, uma falha aqui é bug do harness (aplicar_edicao), não do modelo — daí
# o SystemExit com a lista. Os diffs são gravados em pasta_bib (irmãos de epoca-n/), e não
# dentro da pasta da época, porque bib.carregar varre a pasta inteira atrás de .md: um
# diff__E1.md dentro de epoca-1 seria lido como verbete e acusado como "frontmatter ilegível
# — arquivo não começa com '---'" (medido) por quem fosse validar a cópia depois, e entraria
# na contagem de verbetes do fechamento. Assim a pasta da época fica só com os verbetes, o
# INDICE.md e o fechamento.json.
def fechar_epoca(pasta_bib: Path, n: int, modelo: str, casos: list[dict],
                 aceitas_na_epoca: int, versao_ollama: str | None = None) -> dict:
    # versao_ollama só é repassada ao fechamento (ver fechar_snapshot, achado I5).
    raiz = pasta_bib / f"epoca-{n}"
    anterior = pasta_bib / f"epoca-{n - 1}"
    original = pasta_bib / "epoca-0"

    verbetes = _carregar_verbetes(raiz)
    problemas = bib.validar(verbetes, casos, teto_global=None)
    if problemas:
        raise SystemExit(f"época {n} do modelo {modelo} não fecha: biblioteca inválida — "
                         + "; ".join(problemas))
    violacoes = conferir_somente_acrescimo(anterior, raiz)
    if violacoes:
        raise SystemExit(f"época {n} do modelo {modelo} não fecha: a cópia deixou de ser "
                         "só acréscimo — " + "; ".join(violacoes))

    validar_banco.escrever_indice(verbetes, raiz)
    escrever_diff(anterior, raiz, pasta_bib / f"diff__E{n}", f"epoca-{n - 1}",
                  f"epoca-{n}")
    escrever_diff(original, raiz, pasta_bib / f"diff__E{n}__vs_original", "epoca-0",
                  f"epoca-{n}")
    return fechar_snapshot(raiz, n, modelo, aceitas_na_epoca, versao_ollama=versao_ollama)


if __name__ == "__main__":
    from banco_casos import CASOS
    from banco_casos_extra import CASOS_EXTRA

    raiz = Path(sys.argv[1]) if len(sys.argv) > 1 else bib.BASE
    verbetes = bib.carregar(raiz)
    print(hash_biblioteca(raiz))
    print(bib.resumo(verbetes))
    problemas = bib.validar(verbetes, CASOS + CASOS_EXTRA, teto_global=None)
    if problemas:
        print(f"{len(problemas)} problema(s):")
        for p in problemas:
            print("  -", p)
    else:
        print("0 problemas")
    print(contar_notas(verbetes))
