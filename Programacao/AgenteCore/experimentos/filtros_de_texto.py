#!/usr/bin/env python3
# ! Alteração de IA - Revisar: módulo novo (07/11/2026, Pós-Fase 4, pacote Q2): os filtros determinísticos de prolixidade e
# objetividade. Mede qualquer texto que chega ao analista (relatório v3, camada de leitura dos verbetes, frase livre do modelo) e
# devolve as oito métricas da base D do levantamento §6.15.4, cada uma com o limiar e a fonte declarados: palavras por frase (média e
# máximo), Flesch adaptado ao português (fórmula do NILC-Metrix, com separador silábico próprio conferido em amostra), razão de
# preenchimento por lista fechada, repetição interna (trigramas repetidos), taxa de compressão, jargão e sigla sem expansão na primeira
# menção por lista fechada, densidade de termos do domínio e o tamanho em palavras só como covariável. Calibra os limiares no corpus
# de referência (os textos "! Motivo:" dos comentários de IA deste repositório e o exemplo canônico do resumo técnico do Eric, lido da
# memória do repositório TargetERP sem copiar texto nenhum para cá) pelo percentil 95, grava `resultados_alvo/fase4/limiares_texto.json`
# e lê os textos antes e depois (relatórios v2 contra v3 das três corridas vigentes; verbetes contra a camada de leitura) para
# `avaliar_fase4.py --texto`. Só biblioteca padrão; os módulos do agente são importados dentro das funções que leem as corridas.
# ! Motivo: plano aprovado da Pós-Fase 4, seção 3.3 e pacote Q2: a normalização das respostas precisa de medida em código, porque um
# modelo julgando o próprio texto cai no texto mais longo (Zheng et al., 2023: 91,3% dos casos em dois dos três juízes testados); cada
# limiar tem fonte, e os calibrados no nosso corpus são declarados como calibração, não como valor de fonte (princípio 5 do plano).
# O corpus de referência é o que segue a regra de escrita do Eric; a calibração guarda só a origem, o hash e as medidas de cada texto.
"""Uso (em Programacao/AgenteCore/experimentos):
  PYTHONIOENCODING=utf-8 python filtros_de_texto.py --calibrar [--check]      # corpus dos "! Motivo:" + exemplo canônico -> resultados_alvo/fase4/limiares_texto.json
  PYTHONIOENCODING=utf-8 python filtros_de_texto.py --medir <arquivo.md> ...  # mede textos contra os limiares gravados
A leitura antes e depois (relatórios v2 contra v3; verbetes contra a camada de leitura) sai por:
  RESULTADOS_DIR=resultados_alvo python avaliar_fase4.py --texto [--check]
"""
from __future__ import annotations

import argparse
import bisect
import contextlib
import hashlib
import json
import re
import statistics
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    with contextlib.suppress(OSError, ValueError, AttributeError):
        sys.stdout.reconfigure(encoding="utf-8")

AQUI = Path(__file__).resolve().parent
RAIZ_DO_REPOSITORIO = AQUI.parent.parent.parent
RA = AQUI / "resultados_alvo"
ARQ_LIMIARES = RA / "fase4" / "limiares_texto.json"
NOME = "texto"
PREFIXO = "tb_f4_texto_"
TITULO = "O que chega ao analista: os filtros de prolixidade e objetividade, antes e depois (Pós-Fase 4, pacote Q2)"
LEITURAS_VIGENTES = ("tela_v4.json", "cenarios_v4.json", "ineditos.json")
ROTULO_DA_CORRIDA = {"fase4_tela_v4": "corrida 18d (o mesmo caso lido da tela e do caso escrito)", "fase4_ensaio_v4": "corrida 21d (ensaio dos cenários da Fase 5)",
                     "fase4_ineditos": "corrida 24 (os 36 inéditos em texto)"}
# O exemplo canônico do resumo técnico do Eric vive na memória do repositório TargetERP, fora deste repositório; só as medidas dele entram aqui.
MEMORIA_EXEMPLO = Path.home() / ".claude" / "projects" / "C--Trabalho-TargetERP" / "memory" / "feedback-resumo-tecnico-aba-ocorrencia.md"
MEMORIA_EXEMPLO_CURTA = "~/.claude/projects/C--Trabalho-TargetERP/memory/feedback-resumo-tecnico-aba-ocorrencia.md"

FLESCH_ALARME = 50.0
FORMULA_FLESCH = (248.835, 1.015, 84.6)     # NILC-Metrix (Leal et al., 2023): 248,835 - 1,015 x palavras por frase - 84,6 x sílabas por palavra
PERCENTIL = 95
JANELA = 100                                 # palavras por janela da repetição e da compressão, para o tamanho do texto não decidir a medida
MINIMO_DE_PALAVRAS_DO_CORPUS = 5
PLACEHOLDER = re.compile(r"^x\d+$")          # o que fica no lugar de cada trecho entre crases

# As oito métricas da base D (levantamento §6.15.4), com a regra de leitura e a fonte de cada limiar.
METRICAS = (
    {"chave": "palavras_por_frase_media", "nome": "Palavras por frase (média)", "regra": "ate", "calibrada": True, "provisorio_do_plano": 20,
     "fonte": "calibração no corpus de referência (percentil 95 das médias); a Lei 15.263/2025 (art. 5) e a ISO 24495-1 só dizem \"frases curtas\" (base D, itens 8 e 9)"},
    {"chave": "palavras_por_frase_max", "nome": "Palavras por frase (máximo)", "regra": "ate", "calibrada": True, "provisorio_do_plano": 30,
     "fonte": "calibração no corpus de referência (percentil 95 do comprimento de todas as frases do corpus); mesma base da média"},
    {"chave": "flesch", "nome": "Flesch adaptado ao português", "regra": "alarme_abaixo", "calibrada": False, "valor": FLESCH_ALARME,
     "fonte": "fórmula do NILC-Metrix (Leal et al., 2023): 248,835 - 1,015 x palavras por frase - 84,6 x sílabas por palavra; 50 é a fronteira da faixa "
              "\"fácil\" de Martins et al. (1996), citada pela dissertação da PUC-Rio; só alarme, porque a literatura chama o índice de superficial (base D, itens 1 a 3)"},
    {"chave": "preenchimento_razao", "nome": "Razão de preenchimento (lista fechada)", "regra": "ate", "calibrada": True,
     "fonte": "lista traduzida do guia de tom do Google (base D, item 11) e das marcas de hesitação de Zhang, Das e Zhang (2024, item 6); limiar: percentil 95 do corpus"},
    {"chave": "repeticao_razao", "nome": "Repetição interna (trigramas repetidos)", "regra": "ate", "calibrada": True,
     "fonte": "ataque da lista repetitiva de Zheng et al. (2023, item 4): dois dos três juízes-modelo caíram em 91,3% dos casos; limiar: percentil 95 do corpus"},
    {"chave": "compressao", "nome": "Taxa de compressão (palavras de conteúdo por palavra distinta, em janelas de 100)", "regra": "ate", "calibrada": True,
     "fonte": "verboso como \"comprimível\" (Zhang, Das e Zhang, 2024, item 6); o denominador (palavras distintas de conteúdo, por janela de 100 palavras) é desenho nosso; "
              "limiar: percentil 95 do corpus"},
    {"chave": "termos_sem_expansao_n", "nome": "Jargão e sigla sem expansão na primeira menção (lista fechada)", "regra": "zero", "calibrada": False, "valor": 0,
     "fonte": "Lei 15.263/2025, art. 5 (jargão trocado ou explicado; nome completo antes da sigla); a lista é deste repositório: a regra dos comentários de IA (CLAUDE.md), "
              "os termos da trilha vetados nos testes do Q1 e os termos de modelo e de estatística das abas da Fase 4"},
    {"chave": "densidade_dominio", "nome": "Densidade de termos do domínio por palavra (lista fechada)", "regra": "comparacao", "calibrada": False, "valor": None,
     "fonte": "Adams et al. (2023, item 7), densidade de entidades por token, adaptada à lista fechada de nomes do projeto mais os trechos entre crases; só para comparar, sem limiar"},
)
COVARIAVEL = {"chave": "palavras", "nome": "Tamanho em palavras", "regra": "covariavel",
              "fonte": "Dubois et al. (2024) e Zheng et al. (2023): o tamanho infla a nota de qualquer juiz-modelo; entra nas tabelas e nunca como critério (base D, itens 4 e 5)"}
CHAVES_DO_ITEM = ("palavras", "frases", "silabas_por_palavra", "palavras_por_frase_media", "palavras_por_frase_max", "flesch", "preenchimento_razao",
                  "repeticao_razao", "compressao", "termos_sem_expansao_n", "densidade_dominio", "trechos_em_codigo")

# Lista fechada de enchimento: as marcas do guia de tom do Google ("please note", "at this time", passo "simples" ou "fácil", metáfora e enfeite)
# traduzidas, mais as hesitações que Zhang, Das e Zhang (2024) ligam à resposta verbosa.
PREENCHIMENTO = (
    "vale ressaltar", "vale lembrar", "vale destacar", "vale notar", "vale a pena", "é importante ressaltar", "é importante destacar", "é importante notar",
    "é importante lembrar", "cabe ressaltar", "cabe destacar", "cabe lembrar", "note que", "observe que", "perceba que", "neste momento", "no momento atual",
    "atualmente", "simplesmente", "basicamente", "de fato", "na verdade", "em outras palavras", "por favor", "claramente", "obviamente", "evidentemente",
    "certamente", "realmente", "extremamente", "bastante", "de forma geral", "de maneira geral", "em geral", "a fim de", "no sentido de", "com o objetivo de",
    "com a finalidade de", "levando em consideração", "tendo em vista", "a nível de", "conforme mencionado", "como mencionado", "como dito", "como já dito",
    "como visto", "e assim por diante", "etc", "é possível observar", "pode-se observar", "pode-se notar", "nota-se que", "percebe-se que", "sendo que",
    "talvez", "possivelmente", "provavelmente", "acredito que", "acho que", "parece que", "pode ser que", "em princípio", "aparentemente",
    "de certa forma", "de alguma forma", "meio que",
)
# "fácil" e "facilmente" ficam fora da lista, embora o guia do Google vete chamar um passo de fácil: "fácil" é o nome do nível 1 da taxonomia de
# dificuldade dos casos (NIVEIS em taxonomia.py), e o relatório precisa escrevê-lo.
# Lista fechada de jargão e sigla: termo -> (padrão, expansões aceitas na mesma frase da primeira menção, em minúsculas). Expansão vazia quer dizer
# que o termo não tem forma aceita (a regra dos comentários de IA deste repositório o veta) e conta sempre.
TERMOS_FECHADOS: dict[str, tuple[str, tuple[str, ...]]] = {
    # vetados pela regra dos comentários de IA (CLAUDE.md: "sem jargão teórico")
    "snapshot": (r"\bsnapshots?\b", ()), "race condition": (r"\brace[ -]conditions?\b", ()), "guard-rail": (r"\bguard[ -]?rails?\b", ()),
    "last writer wins": (r"\blast[ -]writer[ -]wins\b", ()),
    # termos da trilha vetados nos testes do Q1 (não são para o analista ler)
    "prov.used": (r"\bprov\.used\b", ()), "gen_ai": (r"\bgen_ai\b", ()), "wasDerivedFrom": (r"\bwasderivedfrom\b", ()),
    "logprob": (r"\blogprobs?\b", ("probabilidade",)), "hit@3": (r"\bhit@\d+", ("entre os três", "entre os 3", "três primeiros", "três entregues")),
    # termos de modelo e de estatística que as abas da Fase 4 explicam em palavras
    "auroc": (r"\bauroc\b", ("separa", "área sob a curva", "sortear")), "tpr": (r"\btpr\b", ("verdadeiros positivos", "parcela dos erros", "erros que")),
    "tnr": (r"\btnr\b", ("verdadeiros negativos", "parcela dos acertos", "acertos que")), "logit": (r"\blogits?\b", ()), "softmax": (r"\bsoftmax\b", ()),
    "bootstrap": (r"\bbootstrap\b", ("reamostragem", "sorteia", "sorteio")), "embedding": (r"\bembeddings?\b", ("significado", "vetor")),
    "prefill": (r"\bprefill\b", ("ler o prompt", "lendo o prompt", "leitura do prompt", "lê o texto")), "token": (r"\btokens?\b", ("pedaço", "pedaços", "unidade de texto", "fragmento")),
    "num_ctx": (r"\bnum_ctx\b", ("janela de contexto", "contexto")), "quantização": (r"\bquantiza[çc][ãa]o\b", ("bits", "pesos", "precisão")),
    "temperatura": (r"\btemperaturas?\b", ("aleatoriedade", "sorteio", "variação", "determin", "sempre a mesma")),
    "llm": (r"\bllms?\b", ("modelo de linguagem", "modelo grande")), "rag": (r"\brag\b", ("recuperação", "busca")), "bm25": (r"\bbm25\b", ("busca por palavras", "palavras")),
    "mttr": (r"\bmttr\b", ("tempo",)), "task success": (r"\btask[ -]success\b", ("chegaram ao resultado", "chegou ao resultado", "tarefa concluída", "sucesso da tarefa")),
    "mcp": (r"\bmcp\b", ("servidor", "protocolo")), "ctfl": (r"\bctfl\b", ("foundation level", "certified tester", "certificação", "certificado")),
    "istqb": (r"\bistqb\b", ("international software testing", "conselho", "comitê", "qualificação")), "tdd": (r"\btdd\b", ("teste antes", "testes antes", "test-driven", "primeiro o teste")),
    "e2e": (r"\be2e\b", ("ponta a ponta",)),
    # termos de programa e de infraestrutura que pedem o significado na primeira menção (Lei 15.263/2025, art. 5)
    "hash": (r"\bhash(es)?\b", ("impressão digital", "resumo", "identificador", "assinatura")), "frontmatter": (r"\bfrontmatter\b", ("cabeçalho",)),
    "endpoint": (r"\bendpoints?\b", ("rota", "rotas")), "payload": (r"\bpayloads?\b", ("corpo",)), "timeout": (r"\btimeouts?\b", ("tempo limite", "tempo-limite", "espera", "esperou")),
    "fallback": (r"\bfallbacks?\b", ("alternativa", "plano b")), "pipeline": (r"\bpipelines?\b", ()), "deploy": (r"\bdeploys?\b", ("publica",)),
    "trade-off": (r"\btrade[ -]?offs?\b", ("troca",)), "overhead": (r"\boverhead\b", ("custo", "sobrecarga")), "default": (r"\bdefaults?\b", ("padrão",)),
    "parser": (r"\bparsers?\b", ("leitor", "lê")), "schema": (r"\bschemas?\b", ("esquema",)), "backend": (r"\bback-?end\b", ("servidor",)),
    "frontend": (r"\bfront-?end\b", ("site", "página", "interface")), "feature": (r"\bfeatures?\b", ("funcionalidade",)), "workaround": (r"\bworkarounds?\b", ("contorno",)),
    "bug": (r"\bbugs?\b", ("defeito",)), "stack trace": (r"\bstack[ -]?traces?\b", ("rastro", "pilha")), "headless": (r"\bheadless\b", ("sem janela",)),
    "fixture": (r"\bfixtures?\b", ("caso escrito", "arquivo", "gravado")), "harness": (r"\bharness\b", ("programa que roda", "executor", "roda os casos")),
    "prompt": (r"\bprompts?\b", ("texto que o modelo recebe", "texto entregue ao modelo", "o que o modelo lê", "o modelo recebe")),
    "ollama": (r"\bollama\b", ("roda o modelo", "executa o modelo", "serve o modelo", "servidor do modelo", "programa que roda")),
    "playwright": (r"\bplaywright\b", ("navegador",)), "blob": (r"\bblobs?\b", ("arquivo", "fora da linha", "à parte")),
    "latência": (r"\blat[êe]ncias?\b", ("demora", "tempo de resposta", "espera")), "enum": (r"\benums?\b", ("valores permitidos", "lista fechada", "lista de valores", "lista de opções")),
    "regex": (r"\bregex(es)?\b", ("expressão regular", "padrão")),
}
# Lista fechada de termos do domínio (o vocabulário do agente, das cobaias e do contrato), contados palavra a palavra em minúsculas.
TERMOS_DO_DOMINIO = frozenset((
    "contrato", "contratos", "verbete", "verbetes", "roteiro", "roteiros", "passo", "passos", "localizador", "localizadores", "seletor", "seletores",
    "conferência", "conferências", "referência", "poda", "trilha", "trilhas", "corrida", "corridas", "caso", "casos", "campo", "campos", "requisição",
    "requisições", "status", "corpo", "resposta", "respostas", "tela", "árvore", "selo", "probabilidade", "causa", "causas", "rótulo", "rótulos", "sintoma",
    "sintomas", "diagnóstico", "diagnósticos", "biblioteca", "busca", "modelo", "agente", "página", "páginas", "navegador", "evento", "eventos", "cura",
    "candidato", "candidatos", "estratégia", "elemento", "elementos", "api", "json", "http", "banco", "tabela", "tabelas", "produto", "produtos", "tipo",
    "tipos", "reserva", "reservas", "usuário", "usuários", "cliente", "clientes", "pedido", "pedidos", "cartão", "cartões", "imagem", "preço", "destaque",
    "cobaia", "cobaias", "cobaiaapi", "cobaiafront", "interface", "gabarito", "classe", "nível", "modo", "falha", "falhas", "defeito", "defeitos", "erro",
    "erros", "injeção", "injetada", "fonte", "impacto", "veredito", "evidência", "contraste", "divergência", "intervenção", "intervenções", "inferência",
    "declaração", "verificação", "verificações", "interceptação", "reexecução", "analista", "site", "rota", "rotas", "tbprodutos", "tbtipos", "tbusuarios",
    "tbreservas", "admin", "login", "reservar", "catálogo",
))
# Palavras funcionais do português, fora da conta das palavras de conteúdo da compressão.
PALAVRAS_FUNCIONAIS = frozenset((
    "o", "a", "os", "as", "um", "uma", "uns", "umas", "de", "do", "da", "dos", "das", "em", "no", "na", "nos", "nas", "por", "pelo", "pela", "pelos", "pelas",
    "para", "pra", "com", "sem", "sob", "sobre", "entre", "até", "contra", "desde", "e", "ou", "mas", "que", "se", "não", "sim", "ao", "aos", "à", "às", "é",
    "são", "foi", "era", "eram", "ser", "está", "estão", "estava", "estavam", "como", "quando", "onde", "qual", "quais", "quem", "cujo", "cuja", "isso", "isto",
    "aquilo", "este", "esta", "estes", "estas", "esse", "essa", "esses", "essas", "aquele", "aquela", "aqueles", "aquelas", "ele", "ela", "eles", "elas", "eu",
    "nós", "você", "vocês", "lhe", "lhes", "me", "te", "seu", "sua", "seus", "suas", "meu", "minha", "dele", "dela", "deles", "delas", "também", "já", "ainda",
    "só", "mais", "menos", "muito", "pouco", "cada", "todo", "toda", "todos", "todas", "outro", "outra", "outros", "outras", "mesmo", "mesma", "nem", "então",
    "porque", "pois", "assim", "aqui", "ali", "lá", "há", "tem", "têm", "ter", "sido", "sendo", "foram", "vai", "vão", "num", "numa", "nesse", "nessa", "neste",
    "nesta", "desse", "dessa", "deste", "desta", "disso", "nisso", "daquele", "daquela", "depois", "antes", "agora", "sempre", "nunca", "nada", "algo", "tudo",
    "qualquer", "sua", "seu", "lo", "la", "los", "las", "se", "x",
))
ABREVIATURAS = frozenset(("p", "ex", "n", "etc", "cf", "obs", "art", "fig", "tab", "ed", "séc", "sec", "sr", "dr", "prof", "pág", "pag", "seç", "vol", "núm", "num",
                          "cap", "inc", "al", "op", "v", "nº"))
EXCLUIDOS_DO_CORPUS = ("Programacao/AgenteCore/experimentos/resultados_alvo/", "Programacao/AgenteCore/experimentos/resultados/",
                       "Programacao/AgenteCore/biblioteca_producao/", "Programacao/AgenteCore/biblioteca_producao_leitura/",
                       "Programacao/AgenteCore/aprendidos_em_espera/", "Documentacao/dashboard/", ".superpowers/")
EXTENSOES_DO_CORPUS = frozenset((".py", ".md", ".ps1", ".php", ".js", ".sql", ".cmd", ".bat", ".sh", ".yml", ".yaml", ".toml", ".txt", ".cff", ".example", ".html", ".gitignore"))

# ------------------------------------------------------------------ sílabas, frases e palavras

_VOGAIS = frozenset("aeiouyáéíóúâêôãõàü")
_FORTES = frozenset("aeoáéóâêôàãõ")
_ACENTUADAS = frozenset("áéíóúâêôàãõ")
_FRACAS_ACENTUADAS = frozenset("íú")
_CONSOANTE_FINAL = re.compile(r"[rlzmn]s?$")


def _nucleos(grupo: str, final: bool, consoante_final: bool, acento_fora: bool) -> int:
    """Quantas sílabas há num grupo de vogais seguidas (separação silábica padrão do português do Brasil): ditongo decrescente (ai, eu, ou) e
    ditongo nasal (ão, ãe, õe) ficam numa sílaba; duas vogais fortes (a, e, o) ou i/u acentuado depois de vogal são hiato; i/u + vogal forte é
    hiato (di-a, pi-a-no, a-tu-al), salvo no fim da palavra, átono, com acento em outra sílaba (fa-mí-lia, sé-rie, prê-mio); vogal fraca seguida
    de consoante final r, l, z, m ou n abre sílaba (sa-ir, ra-iz, ru-im)."""
    nucleos = 1
    for k in range(1, len(grupo)):
        ant, cur = grupo[k - 1], grupo[k]
        if ant in "ãõ" and cur in "eoi":
            continue
        if cur in "iuyü":
            if consoante_final and k == len(grupo) - 1:
                nucleos += 1
            continue
        if ant in _FORTES or ant in _FRACAS_ACENTUADAS:
            nucleos += 1
            continue
        if final and cur not in _ACENTUADAS and acento_fora and k == len(grupo) - 1:
            continue
        nucleos += 1
    return nucleos


def silabas(palavra: str) -> int:
    """Sílabas de uma palavra, pelas regras de `_nucleos` sobre os grupos de vogais; u depois de q ou g é mudo ou semivogal (que, qua, guer);
    palavra com dígito (número, versão, identificador) conta uma unidade; palavra sem vogal conta uma."""
    p = palavra.lower()
    if "-" in p:
        partes = [x for x in p.split("-") if x]
        return sum(silabas(x) for x in partes) if partes else 1
    if any(ch.isdigit() for ch in p):
        return 1
    if not any(ch in _VOGAIS for ch in p):
        return 1
    total, i, n = 0, 0, len(p)
    while i < n:
        if p[i] not in _VOGAIS:
            i += 1
            continue
        ini = i
        while i < n and p[i] in _VOGAIS:
            i += 1
        grupo = p[ini:i]
        if ini > 0 and p[ini - 1] in "qg" and grupo[0] in "uü" and len(grupo) > 1:
            grupo = grupo[1:]
        resto = p[i:]
        acento_fora = any(ch in _ACENTUADAS for ch in p[:ini] + resto)
        total += _nucleos(grupo, resto in ("", "s"), bool(_CONSOANTE_FINAL.fullmatch(resto)), acento_fora)
    return max(total, 1)


_PALAVRA = re.compile(r"\d+(?:[.,:/-]\d+)*|[^\W\d_][^\W_]*(?:[-'’][^\W_]+)*")
_FIM_DE_FRASE = re.compile(r"([.!?]+)(?=\s|$)")


def palavras(frase: str) -> list[str]:
    """As palavras de uma frase: números (com vírgula, ponto, dois-pontos, barra ou hífen internos: 0,99, 1.64.1, 10:16:39, 06/11/2026) e
    palavras começadas por letra, com hífen interno."""
    return _PALAVRA.findall(frase)


def frases(prosa: str) -> list[str]:
    """As frases da prosa: cada linha é um limite, e dentro da linha o limite é ponto, exclamação ou interrogação seguidos de espaço (o ponto
    de uma abreviatura conhecida, como ex., p. ou etc., não encerra a frase). Frase sem palavra não conta."""
    saida: list[str] = []
    for linha in prosa.splitlines():
        linha = linha.strip()
        if not linha:
            continue
        ini = 0
        for m in _FIM_DE_FRASE.finditer(linha):
            trecho = linha[ini:m.end()]
            anterior = re.search(r"([^\W\d_]+)\.$", trecho)
            if m.group(1) == "." and anterior and anterior.group(1).lower() in ABREVIATURAS and m.end() < len(linha):
                continue
            if trecho.strip():
                saida.append(trecho.strip())
            ini = m.end()
        resto = linha[ini:].strip()
        if resto:
            saida.append(resto)
    return [f for f in saida if palavras(f)]


# ------------------------------------------------------------------ prosa do Markdown

_COMENTARIO_HTML = re.compile(r"<!--.*?-->", re.DOTALL)
_BLOCO_DE_CODIGO = re.compile(r"```.*?```", re.DOTALL)
_CODIGO_INLINE = re.compile(r"`([^`\n]*)`")
_TAG_HTML = re.compile(r"<[^>\n]+>")
_LINK = re.compile(r"\[([^\]]*)\]\([^)\s]*\)")
_MARCADOR_DE_LISTA = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
_REGUA = re.compile(r"^[-*_]{3,}$")


def prosa_de_markdown(texto: str) -> dict:
    """A prosa que o analista lê num Markdown: saem os comentários HTML (a tag de IA), os blocos de código, as tabelas, os títulos, as réguas,
    as citações (linhas começadas por `>`: texto trazido do caso, do navegador ou do modelo, que o molde não escreveu), as etiquetas HTML (o
    texto de um <summary> fica), os marcadores de lista, o negrito e o endereço dos links. Cada trecho entre crases vira um marcador (x1, x2,
    ... um por conteúdo distinto): conta como uma palavra na frase, fica fora do Flesch, e o total deles sai em `trechos_em_codigo`."""
    t = _COMENTARIO_HTML.sub(" ", texto)
    t = _BLOCO_DE_CODIGO.sub(" ", t)
    codigos: list[str] = []
    n_codigos = 0

    def marcador(m: re.Match) -> str:
        nonlocal n_codigos
        n_codigos += 1
        conteudo = m.group(1).strip()
        if conteudo not in codigos:
            codigos.append(conteudo)
        return f" x{codigos.index(conteudo) + 1} "

    t = _CODIGO_INLINE.sub(marcador, t)
    linhas = []
    for linha in t.splitlines():
        s = linha.strip()
        if not s or s.startswith(("|", "#", ">")) or _REGUA.fullmatch(s):
            continue
        s = _TAG_HTML.sub(" ", s)
        s = _LINK.sub(r"\1", s)
        s = _MARCADOR_DE_LISTA.sub("", s)
        s = s.replace("**", "").replace("__", "")
        s = re.sub(r"\s+", " ", s).strip()
        if s:
            linhas.append(s)
    return {"prosa": "\n".join(linhas), "trechos_em_codigo": n_codigos, "trechos_em_codigo_distintos": len(codigos)}


# ------------------------------------------------------------------ as oito métricas

def _limite(termo: str) -> re.Pattern:
    return re.compile(r"(?<!\w)" + re.escape(termo) + r"(?!\w)")


_PADROES_DE_PREENCHIMENTO = {termo: _limite(termo) for termo in PREENCHIMENTO}
_PADROES_DE_TERMOS = {nome: (re.compile(padrao, re.IGNORECASE), expansoes) for nome, (padrao, expansoes) in TERMOS_FECHADOS.items()}


def _janelas(tokens: list[str]) -> list[list[str]]:
    """Janelas de JANELA palavras; o resto menor que meia janela entra na última, para não medir um pedaço curto sozinho."""
    if len(tokens) <= JANELA + JANELA // 2:
        return [tokens]
    janelas = [tokens[i:i + JANELA] for i in range(0, len(tokens), JANELA)]
    if len(janelas) > 1 and len(janelas[-1]) < JANELA // 2:
        janelas[-2] += janelas[-1]
        janelas.pop()
    return janelas


def _repeticao_e_compressao(por_frase: list[list[str]]) -> tuple[float, float | None]:
    """Repetição: trigramas de palavras de uma mesma frase que reaparecem dentro da janela (cada frase cai na janela em que começa; um
    trigrama não atravessa frases, para o fim de um item de lista e o começo do seguinte não contarem como repetição), sobre o total de
    trigramas. Compressão: palavras de conteúdo (fora das funcionais, dos marcadores de código e dos números) sobre as distintas, por
    janela; a soma das janelas dá o texto."""
    baixos_por_frase = [[w.lower() for w in t] for t in por_frase]
    tokens = [w for t in baixos_por_frase for w in t]
    janelas = _janelas(tokens)
    fins = []
    for jan in janelas:
        fins.append((fins[-1] if fins else 0) + len(jan))
    tri_por_janela: list[list[tuple[str, ...]]] = [[] for _ in janelas]
    pos = 0
    for t in baixos_por_frase:
        if t:
            j = min(bisect.bisect_right(fins, pos), len(janelas) - 1)
            tri_por_janela[j] += [tuple(t[i:i + 3]) for i in range(len(t) - 2)]
        pos += len(t)
    tri_total = sum(len(tri) for tri in tri_por_janela)
    tri_rep = sum(len(tri) - len(set(tri)) for tri in tri_por_janela)
    cont_total = cont_dist = 0
    for jan in janelas:
        conteudo = [w for w in jan if w not in PALAVRAS_FUNCIONAIS and not PLACEHOLDER.match(w) and not w[0].isdigit()]
        cont_total += len(conteudo)
        cont_dist += len(set(conteudo))
    repeticao = round(tri_rep / tri_total, 4) if tri_total else 0.0
    compressao = round(cont_total / cont_dist, 4) if cont_dist else None
    return repeticao, compressao


def termos_sem_expansao(fr: list[str]) -> list[str]:
    """Os termos da lista fechada cuja primeira menção no texto está numa frase sem nenhuma das expansões aceitas (ordenados)."""
    baixas = [f.lower() for f in fr]
    achados = []
    for nome, (rx, expansoes) in _PADROES_DE_TERMOS.items():
        for f in baixas:
            if rx.search(f):
                if not any(e in f for e in expansoes):
                    achados.append(nome)
                break
    return sorted(achados)


def medir(texto: str) -> dict:
    """As oito métricas da base D de um texto (Markdown ou texto puro), mais as covariáveis: palavras, frases, sílabas, trechos em código e os
    comprimentos das frases (para a calibração do máximo). Palavras por frase contam os marcadores dos trechos em código (o analista os lê);
    o Flesch sai só das palavras de prosa, porque a fórmula foi feita para texto corrido, e um identificador não se lê em sílabas."""
    p = prosa_de_markdown(texto or "")
    fr = frases(p["prosa"])
    por_frase = [palavras(f) for f in fr]
    comprimentos = [len(t) for t in por_frase]
    tokens = [w for t in por_frase for w in t]
    prosa_tokens = [w for w in tokens if not PLACEHOLDER.match(w)]
    n_pal, n_fr, n_prosa = len(tokens), len(fr), len(prosa_tokens)
    n_sil = sum(silabas(w) for w in prosa_tokens)
    ppf = n_pal / n_fr if n_fr else None
    spp = n_sil / n_prosa if n_prosa else None
    flesch = FORMULA_FLESCH[0] - FORMULA_FLESCH[1] * (n_prosa / n_fr) - FORMULA_FLESCH[2] * spp if n_fr and spp is not None else None
    baixa = p["prosa"].lower()
    preench = {termo: len(rx.findall(baixa)) for termo, rx in _PADROES_DE_PREENCHIMENTO.items()}
    preench = {t: n for t, n in preench.items() if n}
    pal_preench = sum(n * len(t.split()) for t, n in preench.items())
    repeticao, compressao = _repeticao_e_compressao(por_frase)
    termos = termos_sem_expansao(fr)
    dominio = sum(1 for w in tokens if w.lower() in TERMOS_DO_DOMINIO) + p["trechos_em_codigo"]
    return {"palavras": n_pal, "palavras_prosa": n_prosa, "frases": n_fr, "silabas": n_sil, "trechos_em_codigo": p["trechos_em_codigo"],
            "silabas_por_palavra": round(spp, 4) if spp is not None else None,
            "palavras_por_frase_media": round(ppf, 2) if ppf is not None else None, "palavras_por_frase_max": max(comprimentos) if comprimentos else None,
            "comprimentos_das_frases": comprimentos, "flesch": round(flesch, 2) if flesch is not None else None,
            "preenchimento_razao": round(pal_preench / n_pal, 4) if n_pal else 0.0, "preenchimentos": dict(sorted(preench.items())),
            "repeticao_razao": repeticao, "compressao": compressao,
            "termos_sem_expansao": termos, "termos_sem_expansao_n": len(termos),
            "termos_do_dominio": dominio, "densidade_dominio": round(dominio / n_pal, 4) if n_pal else 0.0}


def avaliar(medidas: dict, limiares: dict) -> dict:
    """Cada métrica contra o seu limiar: `ate` passa quando o valor não passa do limiar, `zero` quando o valor é zero; alarme e comparação não
    aprovam nem reprovam (`passa` fica None). O Flesch abaixo de 50 só acende `alarme_flesch`."""
    valores = limiares["limiares"]
    criterios = {}
    aprovado = True
    for met in METRICAS:
        ch = met["chave"]
        v = medidas.get(ch)
        limiar = (valores.get(ch) or {}).get("valor")
        if met["regra"] == "ate":
            passa = None if v is None or limiar is None else v <= limiar
        elif met["regra"] == "zero":
            passa = v == 0
        else:
            passa = None
        criterios[ch] = {"valor": v, "limiar": limiar, "passa": passa}
        if passa is False:
            aprovado = False
    flesch = medidas.get("flesch")
    return {"aprovado": aprovado, "alarme_flesch": flesch is not None and flesch < FLESCH_ALARME, "criterios": criterios,
            "termos_sem_expansao": list(medidas.get("termos_sem_expansao") or [])}


# ------------------------------------------------------------------ corpus de referência e calibração

def percentil(valores: list[float], p: float) -> float:
    """Percentil com interpolação linear entre as posições vizinhas (a mesma conta do numpy padrão)."""
    v = sorted(valores)
    if not v:
        raise ValueError("percentil de lista vazia")
    pos = (len(v) - 1) * p / 100
    i = int(pos)
    frac = pos - i
    if i + 1 >= len(v):
        return float(v[-1])
    return float(v[i] + (v[i + 1] - v[i]) * frac)


def sha16(texto: str) -> str:
    return hashlib.sha256(" ".join(texto.split()).encode("utf-8")).hexdigest()[:16]


def arquivo_no_corpus(rel: str) -> bool:
    """Um arquivo do repositório entra no corpus quando é texto com comentário de IA escrito à mão: ficam de fora os derivados de corrida
    (resultados_alvo/), os verbetes escritos pelo modelo (biblioteca_producao/, aprendidos_em_espera/), a camada de leitura gerada, o painel
    gerado e o livro-razão fora do git; só as extensões de texto listadas."""
    rel = rel.replace("\\", "/")
    if any(rel.startswith(x) for x in EXCLUIDOS_DO_CORPUS):
        return False
    nome = rel.rsplit("/", 1)[-1]
    return nome == ".gitignore" or Path(nome).suffix.lower() in EXTENSOES_DO_CORPUS


_MARCA_MOTIVO = re.compile(r"!\s*Motivo:")
_PREFIXO_DE_COMENTARIO = re.compile(r"^\s*(#+|//|--|rem\b|\*)\s?", re.IGNORECASE)
_OUTRA_MARCA = re.compile(r"!\s*(Altera[çc][ãa]o de IA|Alteracao de IA|Motivo:)", re.IGNORECASE)
_ABERTURA_DE_COMENTARIO = re.compile(r"\s*(?:<!--\s*|#+\s*|//\s*|--\s*|rem\s+|\*\s*|/\*\s*)?", re.IGNORECASE)


def _marca_de_comentario(linha: str, m: re.Match) -> bool:
    """A marca vale quando abre o comentário (só espaço ou o prefixo de comentário antes dela na linha) ou quando a tag de IA vem antes
    dela na mesma linha; uma menção entre aspas no meio de uma frase ("os textos \"! Motivo:\" do repositório") não é um comentário."""
    antes = linha[:m.start()]
    return bool(_ABERTURA_DE_COMENTARIO.fullmatch(antes)) or _OUTRA_MARCA.search(antes) is not None


def _motivos_do_texto(texto: str) -> list[tuple[int, str]]:
    """(linha, texto) de cada "! Motivo:" de um arquivo: num comentário de linha (#, //, --, rem, *) o motivo segue pelas linhas seguintes com o
    mesmo prefixo, até a linha sem prefixo ou com outra marca; num comentário HTML, até o `-->`; fora dos dois, até a linha em branco. Só conta
    a marca que abre um comentário (ou segue a tag de IA na mesma linha): a menção da marca no meio de uma frase fica de fora."""
    linhas = texto.splitlines()
    saida = []
    for i, linha in enumerate(linhas):
        m = _MARCA_MOTIVO.search(linha)
        if not m or not _marca_de_comentario(linha, m):
            continue
        depois = linha[m.end():]
        pref = _PREFIXO_DE_COMENTARIO.match(linha)
        antes = "\n".join(linhas[:i]) + "\n" + linha[:m.start()]
        em_html = antes.rfind("<!--") > antes.rfind("-->")
        partes = [depois.split("-->")[0] if em_html else depois]
        if em_html and "-->" not in depois:
            for prox in linhas[i + 1:]:
                if "-->" in prox:
                    partes.append(prox.split("-->")[0])
                    break
                partes.append(prox)
        elif pref and not em_html:
            prefixo = pref.group(1).lower()
            for prox in linhas[i + 1:]:
                pm = _PREFIXO_DE_COMENTARIO.match(prox)
                if not pm or pm.group(1).lower() != prefixo or _OUTRA_MARCA.search(prox) or not prox[pm.end():].strip():
                    break
                partes.append(prox[pm.end():])
        elif not em_html:
            for prox in linhas[i + 1:]:
                if not prox.strip() or _OUTRA_MARCA.search(prox) or prox.lstrip().startswith(("#", "//", "--", "-->", "!")):
                    break
                partes.append(prox)
        if pref and em_html:
            partes = [re.sub(r"^\s*(#+|//|--|\*)\s?", "", x) for x in partes]
        texto_motivo = " ".join(" ".join(x.split()) for x in partes).strip()
        saida.append((i + 1, texto_motivo))
    return saida


def arquivos_do_git(raiz: Path) -> list[str]:
    saida = subprocess.run(["git", "ls-files"], cwd=raiz, capture_output=True, text=True, encoding="utf-8", check=True).stdout
    return [l.strip() for l in saida.splitlines() if l.strip()]


def corpus_do_repositorio(raiz: Path = RAIZ_DO_REPOSITORIO, arquivos: list[str] | None = None) -> list[dict]:
    """Os textos "! Motivo:" dos comentários de IA do repositório (arquivos rastreados pelo git, ou a lista dada), um item por texto distinto com
    pelo menos MINIMO_DE_PALAVRAS_DO_CORPUS palavras: {origem: "arquivo:linha", fonte: "motivo", texto}."""
    raiz = Path(raiz)
    arquivos = arquivos if arquivos is not None else arquivos_do_git(raiz)
    vistos: set[str] = set()
    itens = []
    for rel in arquivos:
        if not arquivo_no_corpus(rel):
            continue
        arq = raiz / rel
        if not arq.is_file():
            continue
        try:
            texto = arq.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            texto = arq.read_text(encoding="utf-8", errors="replace")
        for linha, motivo in _motivos_do_texto(texto):
            if len(palavras(motivo)) < MINIMO_DE_PALAVRAS_DO_CORPUS:
                continue
            chave = sha16(motivo.lower())
            if chave in vistos:
                continue
            vistos.add(chave)
            itens.append({"origem": f"{rel.replace(chr(92), '/')}:{linha}", "fonte": "motivo", "texto": motivo})
    return itens


def exemplo_canonico(caminho: Path = MEMORIA_EXEMPLO) -> list[str]:
    """As linhas de texto do exemplo canônico do resumo técnico do Eric (o bloco de código depois de "Exemplo canônico" na memória): sem os
    cabeçalhos de arquivo, as setas da árvore e o prefixo "Motivo:", e só as linhas com pelo menos MINIMO_DE_PALAVRAS_DO_CORPUS palavras.
    O texto fica só em memória: a calibração guarda a origem, o hash e as medidas."""
    texto = Path(caminho).read_text(encoding="utf-8")
    ini = texto.find("Exemplo canônico")
    if ini < 0:
        return []
    m = re.search(r"```[^\n]*\n(.*?)```", texto[ini:], re.DOTALL)
    if not m:
        return []
    saida = []
    for linha in m.group(1).splitlines():
        s = linha.strip()
        if not s or s.startswith("["):
            continue
        s = re.sub(r"^(->\s*)+", "", s).strip()
        s = re.sub(r"^Motivo:\s*", "", s).strip()
        if len(palavras(s)) >= MINIMO_DE_PALAVRAS_DO_CORPUS:
            saida.append(s)
    return saida


def _limiares_base() -> dict:
    """Os limiares que não dependem do corpus: o alarme do Flesch e o zero do jargão (valores de fonte), a densidade e o tamanho (sem limiar)."""
    return {"flesch": {"valor": FLESCH_ALARME, "tipo": "fonte", "regra": "alarme_abaixo"},
            "termos_sem_expansao_n": {"valor": 0, "tipo": "fonte", "regra": "zero"},
            "densidade_dominio": {"valor": None, "tipo": "comparacao", "regra": "comparacao"},
            "palavras": {"valor": None, "tipo": "covariavel", "regra": "covariavel"}}


def calibrar(itens: list[dict], gerado_em: str | None = None) -> dict:
    """Mede cada item do corpus e fixa os limiares calibrados no percentil 95 (a média de palavras por frase pelos itens; o máximo pelo comprimento
    de todas as frases do corpus juntas; preenchimento, repetição e compressão pelos itens). Devolve {metadados, limiares, itens}; nenhum texto fica."""
    medidos, pooladas = [], []
    for it in itens:
        m = medir(it["texto"])
        pooladas += m["comprimentos_das_frases"]
        medidos.append({"origem": it["origem"], "fonte": it.get("fonte", "motivo"), "sha16": sha16(it["texto"]), **{k: m[k] for k in CHAVES_DO_ITEM}})

    def p(chave: str, q: float = PERCENTIL) -> float | None:
        vals = [x[chave] for x in medidos if x[chave] is not None]
        return round(percentil(vals, q), 4) if vals else None

    def quantis(chave: str) -> dict:
        """A distribuição no corpus (mediana e percentis 75, 90 e 95), para a leitura pôr o limiar em perspectiva."""
        return {"mediana": p(chave, 50), "percentil_75": p(chave, 75), "percentil_90": p(chave, 90), "percentil_95": p(chave, 95)}

    limiares = _limiares_base()
    limiares["flesch"]["corpus"] = {**quantis("flesch"), "percentil_5": p("flesch", 5), "percentil_25": p("flesch", 25)}
    limiares["densidade_dominio"]["corpus"] = quantis("densidade_dominio")
    limiares["palavras"]["corpus"] = quantis("palavras")
    for met in METRICAS:
        if not met["calibrada"]:
            continue
        ch = met["chave"]
        corpus = quantis(ch)
        if ch == "palavras_por_frase_max":
            valor = round(percentil(pooladas, PERCENTIL), 2) if pooladas else None
            corpus["frases_pooladas"] = {"mediana": round(percentil(pooladas, 50), 2), "percentil_75": round(percentil(pooladas, 75), 2),
                                         "percentil_90": round(percentil(pooladas, 90), 2), "percentil_95": round(percentil(pooladas, 95), 2)} if pooladas else None
        else:
            valor = p(ch)
            if valor is not None:
                valor = round(valor, 2 if ch == "palavras_por_frase_media" else 4)
        if ch == "palavras_por_frase_media":
            corpus["itens_de_uma_frase"] = sum(1 for x in medidos if x["frases"] == 1)
        limiares[ch] = {"valor": valor, "tipo": "calibracao", "regra": met["regra"], "percentil": PERCENTIL, "provisorio_do_plano": met.get("provisorio_do_plano"), "corpus": corpus}
    por_fonte = Counter(x["fonte"] for x in medidos)
    return {"metadados": {"gerado_em": gerado_em or datetime.now().isoformat(timespec="seconds"), "gerado_por": "filtros_de_texto.py --calibrar",
                          "percentil": PERCENTIL, "origem": "calibração no corpus de referência",
                          "corpus": {"itens": len(medidos), "por_fonte": dict(sorted(por_fonte.items())), "frases": len(pooladas)}},
            "limiares": limiares, "itens": medidos}


def limiares_fixos(valores: dict, origem: str) -> dict:
    """Limiares dados de fora (testes, ou uma leitura exploratória), na mesma forma da calibração."""
    limiares = _limiares_base()
    for met in METRICAS:
        if met["calibrada"]:
            limiares[met["chave"]] = {"valor": valores.get(met["chave"]), "tipo": "fixo", "regra": met["regra"], "provisorio_do_plano": met.get("provisorio_do_plano")}
    return {"metadados": {"gerado_em": None, "gerado_por": None, "percentil": None, "origem": origem, "corpus": None}, "limiares": limiares, "itens": []}


def gravar_limiares(caminho: Path, calibracao: dict) -> None:
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(json.dumps(calibracao, ensure_ascii=False, indent=1), encoding="utf-8")


def carregar_limiares(caminho: Path = ARQ_LIMIARES) -> dict:
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def _sem_data(cal: dict) -> dict:
    return {**cal, "metadados": {k: v for k, v in cal["metadados"].items() if k != "gerado_em"}}


def calibracao_do_repositorio(raiz: Path = RAIZ_DO_REPOSITORIO, memoria: Path = MEMORIA_EXEMPLO, gerado_em: str | None = None) -> dict:
    """A calibração completa: os "! Motivo:" do repositório mais o exemplo canônico (quando a memória existe nesta máquina); a referência ao
    arquivo da memória vai nos metadados, pelo caminho curto, nunca o texto."""
    itens = corpus_do_repositorio(raiz)
    exemplo = exemplo_canonico(memoria) if Path(memoria).exists() else []
    itens += [{"origem": f"exemplo canônico do resumo técnico (memória do Eric, fora do repositório), item {n}", "fonte": "exemplo_canonico", "texto": t}
              for n, t in enumerate(exemplo, start=1)]
    cal = calibrar(itens, gerado_em=gerado_em)
    cal["metadados"]["exemplo_canonico"] = ({"arquivo": MEMORIA_EXEMPLO_CURTA if Path(memoria) == MEMORIA_EXEMPLO else str(memoria), "itens": len(exemplo),
                                             "sha16_do_bloco": sha16("\n".join(exemplo))} if exemplo else {"arquivo": None, "itens": 0, "aviso": "memória não encontrada nesta máquina"})
    cal["metadados"]["arquivos_lidos"] = len({x["origem"].rsplit(":", 1)[0] for x in cal["itens"] if x["fonte"] == "motivo"})
    cal["metadados"]["nota"] = ("retrato datado do corpus: comentários novos mudam o percentil 95; recalibre com --calibrar e regrave a leitura com "
                                "avaliar_fase4.py --texto quando quiser os limiares do dia")
    return cal


# ------------------------------------------------------------------ a leitura antes e depois (avaliar_fase4.py --texto)

def corridas_vigentes(raiz: Path = RA) -> list[tuple[str, Path]]:
    """(corrida, pasta) das três leituras vigentes da Fase 4, lidas de resultados_alvo/fase4/*.json (campo metadados.corrida)."""
    saida = []
    for nome in LEITURAS_VIGENTES:
        corrida = json.loads((Path(raiz) / "fase4" / nome).read_text(encoding="utf-8"))["metadados"]["corrida"]
        saida.append((corrida, Path(raiz) / corrida))
    return saida


def ler_textos(corridas: list[tuple[str, Path]] | None = None, raiz_bib: Path | None = None, raiz_leitura: Path | None = None, raiz: Path = RA) -> dict:
    """Os textos que chegam ao analista, antes e depois: por corrida, o relatório v2 (o gravado em relatorios/, ou regerado da trilha quando a
    corrida não o gravou) e o v3 gravado em relatorios_v3/ de cada trilha com nó de decisão; os verbetes da biblioteca de produção e a leitura
    de cada um (o corpo, sem o cabeçalho); e as frases de impacto escritas pelo modelo (declaração IMPACTO das trilhas)."""
    import biblioteca as bib
    import biblioteca_leitura as bl
    import gerar_relatorio_raciocinio as grr
    import trilha as tr
    corridas = corridas or corridas_vigentes(raiz)
    saida_corridas, modelo = [], []
    for corrida, pasta in corridas:
        pasta = Path(pasta)
        cond = json.loads((pasta / "condicoes_fase4.json").read_text(encoding="utf-8")) if (pasta / "condicoes_fase4.json").exists() else {}
        modo = cond.get("modo")
        k = cond.get("k") if isinstance(cond.get("k"), int) else 3
        arq_trilha = pasta / f"trilha_{modo}.jsonl" if modo else next(iter(sorted(pasta.glob("trilha_*.jsonl"))), None)
        if arq_trilha is None or not arq_trilha.exists():
            raise FileNotFoundError(f"trilha da corrida não encontrada em {pasta}")
        eventos = tr.ler(arq_trilha)
        relatorios = []
        for tid, seq in tr.por_trilha(eventos).items():
            if not any(e["tipo"] == "decisao" for e in seq):
                continue
            nome = grr.nome_do_relatorio(tid)
            arq_v3 = pasta / "relatorios_v3" / f"{nome}.md"
            if not arq_v3.exists():
                raise FileNotFoundError(f"{arq_v3} não existe: grave os relatórios v3 com gerar_relatorio_raciocinio.py --v3 --saida {pasta.name}")
            arq_v2 = pasta / "relatorios" / f"{nome}.md"
            if arq_v2.exists():
                v2, origem = arq_v2.read_text(encoding="utf-8"), "gravado"
            else:
                v2 = grr.relatorio_do_caso_v2(eventos, tid, comando_reexecucao=grr.comando_de_reexecucao(modo, cond.get("saida") or pasta.name, tid, k), pasta_blobs=pasta / "blobs")
                origem = "regerado"
            relatorios.append({"nome": nome, "trilha": tid, "v2": v2, "v3": arq_v3.read_text(encoding="utf-8"), "v2_origem": origem})
            for e in seq:
                d = e["dados"]
                if e["tipo"] == "declaracao" and d.get("campo") == "impacto" and not d.get("ausente") and d.get("valor"):
                    modelo.append({"corrida": corrida, "caso": nome, "texto": str(d["valor"])})
        saida_corridas.append({"id": corrida, "pasta": pasta.as_posix(), "modo": modo, "relatorios": relatorios})
    raiz_bib = Path(raiz_bib or bl.PASTA_BIBLIOTECA)
    raiz_leitura = Path(raiz_leitura or bl.PASTA_LEITURA)
    leituras = bl.carregar(raiz_leitura)
    verbetes = []
    for v in bib.carregar(raiz_bib):
        leitura = leituras.get(v["id"])
        if leitura is None:
            raise FileNotFoundError(f"o verbete {v['id']} não tem leitura em {raiz_leitura}: rode biblioteca_leitura.py --gerar")
        corpo_v = _corpo_sem_cabecalho(Path(v["caminho"]).read_text(encoding="utf-8"))
        corpo_l = _corpo_sem_cabecalho((raiz_leitura / leitura["caminho"]).read_text(encoding="utf-8"))
        verbetes.append({"id": v["id"], "caminho": Path(v["caminho"]).relative_to(raiz_bib).as_posix(), "tipo": v["meta"].get("tipo"), "curado": leitura["curado"],
                         "verbete": corpo_v, "leitura": corpo_l})
    return {"corridas": saida_corridas, "verbetes": verbetes, "modelo": modelo}


def _corpo_sem_cabecalho(texto: str) -> str:
    """O Markdown sem o cabeçalho entre `---` (que traz a tag de IA e os campos da busca, não o texto para o analista)."""
    if texto.startswith("---"):
        fim = texto.find("\n---", 3)
        if fim > 0:
            return texto[fim + 4:]
    return texto


def _pct(parte: int, total: int) -> float | None:
    return round(100 * parte / total, 1) if total else None


def _resumo_de_texto(texto: str, limiares: dict) -> dict:
    """As medidas de um texto com a avaliação dele, sem as listas longas (os comprimentos das frases)."""
    m = medir(texto)
    av = avaliar(m, limiares)
    return {**{k: v for k, v in m.items() if k != "comprimentos_das_frases"}, "aprovado": av["aprovado"], "alarme_flesch": av["alarme_flesch"],
            "criterios": {ch: c["passa"] for ch, c in av["criterios"].items() if c["passa"] is not None}}


def _agregar(resumos: list[dict]) -> dict:
    """Um grupo de textos: quantos passam em tudo, quantos acendem o alarme do Flesch, a média de cada métrica, a mediana do tamanho, quantos
    passam em cada critério, os termos sem expansão e os preenchimentos achados (em quantos textos cada um aparece)."""
    n = len(resumos)
    chaves = [m["chave"] for m in METRICAS] + ["palavras", "frases", "silabas_por_palavra", "trechos_em_codigo"]
    medias = {}
    for ch in chaves:
        vals = [r[ch] for r in resumos if r.get(ch) is not None]
        medias[ch] = round(statistics.fmean(vals), 3) if vals else None
    pal = [r["palavras"] for r in resumos]
    criterios = {}
    for met in METRICAS:
        if met["regra"] not in ("ate", "zero"):
            continue
        ch = met["chave"]
        passam = sum(1 for r in resumos if r["criterios"].get(ch) is True)
        criterios[ch] = {"passam": passam, "passam_pct": _pct(passam, n)}
    termos = Counter(t for r in resumos for t in r["termos_sem_expansao"])
    preench = Counter(t for r in resumos for t in r["preenchimentos"])
    aprovados = sum(1 for r in resumos if r["aprovado"])
    alarme = sum(1 for r in resumos if r["alarme_flesch"])
    # a segunda leitura das frases: com os valores que o plano antecipou (20 e 30), para pôr o percentil 95 do corpus em perspectiva
    provisorios = {}
    for met in METRICAS:
        if met.get("provisorio_do_plano") is not None:
            passam = sum(1 for r in resumos if r.get(met["chave"]) is not None and r[met["chave"]] <= met["provisorio_do_plano"])
            provisorios[met["chave"]] = {"limiar": met["provisorio_do_plano"], "passam": passam, "passam_pct": _pct(passam, n)}
    return {"n": n, "aprovados": aprovados, "aprovados_pct": _pct(aprovados, n), "alarme_flesch": alarme, "alarme_flesch_pct": _pct(alarme, n), "medias": medias,
            "palavras_mediana": statistics.median(pal) if pal else None, "palavras_total": sum(pal), "criterios": criterios, "provisorios_do_plano": provisorios,
            "termos_sem_expansao": dict(sorted(termos.items(), key=lambda x: (-x[1], x[0]))), "preenchimentos": dict(sorted(preench.items(), key=lambda x: (-x[1], x[0])))}


def resumir_texto(bruto: dict, limiares: dict, gerado_em: str | None = None) -> dict:
    """A leitura antes e depois: um grupo por corrida (v2 contra v3), um grupo da camada de leitura (verbete contra leitura), as frases do modelo
    à parte (texto do modelo, sem antes e depois) e o resumo dos relatórios e dos verbetes juntos. Tudo medido contra os mesmos limiares."""
    valores = limiares["limiares"]
    grupos, todos_antes, todos_depois = [], [], []
    for c in bruto["corridas"]:
        pares, antes, depois = [], [], []
        origem = Counter(r["v2_origem"] for r in c["relatorios"])
        for r in sorted(c["relatorios"], key=lambda x: x["nome"]):
            a, d = _resumo_de_texto(r["v2"], limiares), _resumo_de_texto(r["v3"], limiares)
            pares.append({"nome": r["nome"], "trilha": r["trilha"], "v2_origem": r["v2_origem"], "antes": a, "depois": d})
            antes.append(a)
            depois.append(d)
        grupos.append({"id": c["id"], "rotulo": ROTULO_DA_CORRIDA.get(c["id"], c["id"]), "tipo": "relatorios", "modo": c["modo"],
                       "v2_origem": {"gravados": origem.get("gravado", 0), "regerados": origem.get("regerado", 0)}, "antes": _agregar(antes), "depois": _agregar(depois), "pares": pares})
        todos_antes += antes
        todos_depois += depois
    pares_v, antes_v, depois_v = [], [], []
    for v in sorted(bruto["verbetes"], key=lambda x: x["id"]):
        a, d = _resumo_de_texto(v["verbete"], limiares), _resumo_de_texto(v["leitura"], limiares)
        pares_v.append({"id": v["id"], "caminho": v["caminho"], "tipo": v.get("tipo"), "curado": v.get("curado", False), "antes": a, "depois": d})
        antes_v.append(a)
        depois_v.append(d)
    grupos.append({"id": "camada_de_leitura", "rotulo": "verbetes da biblioteca de produção e a camada de leitura", "tipo": "verbetes",
                   "antes": _agregar(antes_v), "depois": _agregar(depois_v), "pares": pares_v})
    resumos_modelo = [_resumo_de_texto(m["texto"], limiares) for m in bruto["modelo"]]
    por_corrida = Counter(m["corrida"] for m in bruto["modelo"])
    metricas = [{**met, "limiar": (valores.get(met["chave"]) or {}).get("valor"), "tipo": (valores.get(met["chave"]) or {}).get("tipo")} for met in METRICAS]
    meta_lim = limiares["metadados"]
    return {"metadados": {"gerado_em": gerado_em or datetime.now().isoformat(timespec="seconds"), "gerado_por": "avaliar_fase4.py --texto", "corrida": None,
                          "fonte": "relatorios/ (v2; regerado da trilha onde a corrida não o gravou) e relatorios_v3/ das corridas vigentes; biblioteca_producao/ e "
                                   "biblioteca_producao_leitura/ (corpo, sem o cabeçalho); declarações IMPACTO das trilhas; limiares de limiares_texto.json",
                          "corridas": [c["id"] for c in bruto["corridas"]],
                          "regra_de_aprovacao": "um texto passa quando fica dentro dos limiares de palavras por frase (média e máximo), preenchimento, repetição e "
                                                "compressão e não tem termo da lista fechada sem expansão na primeira menção; o Flesch abaixo de 50 só acende o alarme; "
                                                "densidade e tamanho não aprovam nem reprovam"},
            "limiares": {"origem": meta_lim.get("origem"), "gerado_em": meta_lim.get("gerado_em"), "corpus": meta_lim.get("corpus"),
                         "valores": {ch: {k: v for k, v in x.items() if k != "corpus"} for ch, x in valores.items()}, "corpus_por_metrica": {ch: x.get("corpus") for ch, x in valores.items()}},
            "metricas": metricas, "covariavel": {**COVARIAVEL, "limiar": None},
            "resumo": {"relatorios": {"antes": _agregar(todos_antes), "depois": _agregar(todos_depois)}, "verbetes": {"antes": _agregar(antes_v), "depois": _agregar(depois_v)}},
            "grupos": grupos,
            "modelo": {"rotulo": "frases de impacto escritas pelo modelo (texto do modelo, medido como está; sem antes e depois)", "por_corrida": dict(sorted(por_corrida.items())),
                       **_agregar(resumos_modelo)}}


# ------------------------------------------------------------------ o Markdown da leitura

def _n(v, casas: int = 2) -> str:
    if v is None:
        return "sem valor"
    if isinstance(v, bool):
        return "sim" if v else "não"
    if isinstance(v, int):
        return str(v)
    return f"{v:.{casas}f}".replace(".", ",")


def _pct_txt(v) -> str:
    return "sem valor" if v is None else f"{v:.1f}%".replace(".", ",")


def _termos_txt(d: dict, maximo: int = 8) -> str:
    itens = list(d.items())
    txt = "; ".join(f"{t} ({n})" for t, n in itens[:maximo])
    return (txt + (f"; e mais {len(itens) - maximo}" if len(itens) > maximo else "")) or "nenhum"


def render_texto(dado: dict) -> str:
    import analisar_fase3b as a3b
    import pre_fase4 as pf

    def linha_media(rotulo: str, versao: str, ag: dict) -> list[str]:
        md = ag["medias"]
        return [rotulo, versao, str(ag["n"]), f"{ag['aprovados']} ({_pct_txt(ag['aprovados_pct'])})", f"{ag['alarme_flesch']} ({_pct_txt(ag['alarme_flesch_pct'])})",
                _n(md["palavras_por_frase_media"]), _n(md["palavras_por_frase_max"], 1), _n(md["flesch"], 1), _n(md["preenchimento_razao"], 4), _n(md["repeticao_razao"], 4),
                _n(md["compressao"], 3), _n(md["termos_sem_expansao_n"]), _n(md["densidade_dominio"], 4), _n(ag["palavras_mediana"], 0), _n(md["trechos_em_codigo"], 1)]

    cab_medias = ["Grupo", "Versão", "Textos", "Passam em tudo", "Alarme do Flesch", "Palavras por frase (média)", "Palavras por frase (máximo, média dos textos)", "Flesch",
                  "Preenchimento", "Repetição", "Compressão", "Termos sem expansão (média)", "Densidade do domínio", "Palavras (mediana)", "Trechos em código (média)"]
    linhas_medias, linhas_resumo, linhas_criterios, linhas_termos, linhas_preench, linhas_casos = [], [], [], [], [], []
    for g in dado["grupos"]:
        a, d = g["antes"], g["depois"]
        versoes = ("relatório v2", "relatório v3") if g["tipo"] == "relatorios" else ("verbete", "leitura")
        linhas_medias += [linha_media(g["rotulo"], versoes[0], a), linha_media(g["rotulo"], versoes[1], d)]
        linhas_resumo.append([g["rotulo"], str(d["n"]), f"{a['aprovados']} ({_pct_txt(a['aprovados_pct'])})", f"{d['aprovados']} ({_pct_txt(d['aprovados_pct'])})",
                              str(a["alarme_flesch"]), str(d["alarme_flesch"]), str(sum(a["termos_sem_expansao"].values())), str(sum(d["termos_sem_expansao"].values())),
                              _n(a["palavras_mediana"], 0), _n(d["palavras_mediana"], 0),
                              (f"v2 gravado em {g['v2_origem']['gravados']} e regerado da trilha em {g['v2_origem']['regerados']}" if g["tipo"] == "relatorios" else "leitura gerada por biblioteca_leitura.py")])
        for met in METRICAS:
            ch = met["chave"]
            if ch in a["criterios"]:
                linhas_criterios.append([g["rotulo"], met["nome"], _n((dado["limiares"]["valores"].get(ch) or {}).get("valor"), 4), f"{a['criterios'][ch]['passam']} de {a['n']} ({_pct_txt(a['criterios'][ch]['passam_pct'])})",
                                         f"{d['criterios'][ch]['passam']} de {d['n']} ({_pct_txt(d['criterios'][ch]['passam_pct'])})"])
        for termo in sorted(set(a["termos_sem_expansao"]) | set(d["termos_sem_expansao"]), key=lambda t: (-(a["termos_sem_expansao"].get(t, 0) + d["termos_sem_expansao"].get(t, 0)), t)):
            linhas_termos.append([g["rotulo"], termo, str(a["termos_sem_expansao"].get(termo, 0)), str(d["termos_sem_expansao"].get(termo, 0))])
        for termo in sorted(set(a["preenchimentos"]) | set(d["preenchimentos"]), key=lambda t: (-(a["preenchimentos"].get(t, 0) + d["preenchimentos"].get(t, 0)), t)):
            linhas_preench.append([g["rotulo"], termo, str(a["preenchimentos"].get(termo, 0)), str(d["preenchimentos"].get(termo, 0))])
        for par in g["pares"]:
            pa, pd = par["antes"], par["depois"]
            linhas_casos.append([g["rotulo"], f"`{par.get('nome') or par.get('id')}`", _n(pa["aprovado"]), _n(pd["aprovado"]), _n(pa["palavras_por_frase_max"]), _n(pd["palavras_por_frase_max"]),
                                 _n(pa["flesch"], 1), _n(pd["flesch"], 1), _n(pa["repeticao_razao"], 3), _n(pd["repeticao_razao"], 3), ", ".join(pa["termos_sem_expansao"]) or "nenhum",
                                 ", ".join(pd["termos_sem_expansao"]) or "nenhum", str(pa["palavras"]), str(pd["palavras"])])
    mo = dado["modelo"]
    lim = dado["limiares"]
    corpus = lim.get("corpus") or {}
    blocos = [
        a3b.tab(PREFIXO + "resumo", ["Grupo", "Textos", "Passam em tudo antes", "Passam em tudo depois", "Alarme do Flesch antes", "Alarme do Flesch depois",
                                     "Termos sem expansão antes (ocorrências)", "Termos sem expansão depois (ocorrências)", "Palavras antes (mediana)", "Palavras depois (mediana)", "De onde vem o antes"],
                linhas_resumo),
        a3b.tab(PREFIXO + "metricas", ["Métrica", "Regra", "Limiar", "Tipo do limiar", "Valor provisório do plano", "Fonte"],
                [[m["nome"], {"ate": "até o limiar", "alarme_abaixo": "alarme abaixo do valor", "zero": "zero ocorrências", "comparacao": "só para comparar"}[m["regra"]],
                  _n(m["limiar"], 4), m["tipo"] or "sem limiar", _n(m.get("provisorio_do_plano")) if m.get("provisorio_do_plano") is not None else "não há", m["fonte"]] for m in dado["metricas"]]
                + [[dado["covariavel"]["nome"], "covariável, nunca critério", "não há", "sem limiar", "não há", dado["covariavel"]["fonte"]]]),
        a3b.tab(PREFIXO + "medias", cab_medias, linhas_medias),
        a3b.tab(PREFIXO + "criterios", ["Grupo", "Critério", "Limiar", "Passam antes", "Passam depois"], linhas_criterios),
        a3b.tab(PREFIXO + "termos", ["Grupo", "Termo sem expansão na primeira menção", "Textos antes", "Textos depois"], linhas_termos or [["nenhum grupo", "nenhum", "0", "0"]]),
        a3b.tab(PREFIXO + "preenchimentos", ["Grupo", "Preenchimento (lista fechada)", "Textos antes", "Textos depois"], linhas_preench or [["nenhum grupo", "nenhum", "0", "0"]]),
        a3b.tab(PREFIXO + "modelo", ["Frases do modelo", "Por corrida", "Passam em tudo", "Alarme do Flesch", "Palavras por frase (média)", "Flesch", "Preenchimento", "Repetição",
                                     "Termos sem expansão", "Palavras (mediana)"],
                [[str(mo["n"]), ", ".join(f"{c} {n}" for c, n in mo["por_corrida"].items()) or "nenhuma", f"{mo['aprovados']} ({_pct_txt(mo['aprovados_pct'])})",
                  f"{mo['alarme_flesch']} ({_pct_txt(mo['alarme_flesch_pct'])})", _n(mo["medias"]["palavras_por_frase_media"]), _n(mo["medias"]["flesch"], 1),
                  _n(mo["medias"]["preenchimento_razao"], 4), _n(mo["medias"]["repeticao_razao"], 4), _termos_txt(mo["termos_sem_expansao"]), _n(mo["palavras_mediana"], 0)]]),
        a3b.tab(PREFIXO + "calibracao", ["Origem dos limiares", "Calibrada em", "Itens do corpus", "Por fonte", "Frases do corpus", "Métrica", "Mediana no corpus", "Limiar"],
                [[lim.get("origem") or "sem origem", lim.get("gerado_em") or "sem data", _n(corpus.get("itens")), ", ".join(f"{f} {n}" for f, n in (corpus.get("por_fonte") or {}).items()) or "sem corpus",
                  _n(corpus.get("frases")), m["nome"], _n(((dado["limiares"].get("corpus_por_metrica") or {}).get(m["chave"]) or {}).get("mediana"), 4), _n(m["limiar"], 4)] for m in dado["metricas"]]),
        a3b.tab(PREFIXO + "casos", ["Grupo", "Texto", "Passa antes", "Passa depois", "Maior frase antes", "Maior frase depois", "Flesch antes", "Flesch depois", "Repetição antes",
                                    "Repetição depois", "Termos sem expansão antes", "Termos sem expansão depois", "Palavras antes", "Palavras depois"], linhas_casos),
    ]
    cab = pf.cabecalho(TITULO, "avaliar_fase4.py --texto", "relatorios/ e relatorios_v3/ das corridas vigentes, biblioteca_producao/ e biblioteca_producao_leitura/, e limiares_texto.json",
                       dado["metadados"]["gerado_em"][:10])
    cab += ["", dado["metadados"]["regra_de_aprovacao"][0].upper() + dado["metadados"]["regra_de_aprovacao"][1:] + ". Os limiares calibrados vêm do percentil 95 do corpus de referência "
                "(os textos \"! Motivo:\" dos comentários de IA deste repositório e o exemplo canônico do resumo técnico do Eric, lido da memória do repositório TargetERP sem copiar texto) "
                "e são declarados como calibração; os valores de fonte são o alarme do Flesch (50) e o zero de jargão sem expansão (Lei 15.263/2025, art. 5). "
                "O tamanho em palavras entra como covariável e nunca como critério.", ""]
    return "\n".join(cab) + "\n\n" + "\n\n".join(blocos) + "\n"


# ------------------------------------------------------------------ linha de comando

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--calibrar", action="store_true", help="mede o corpus de referência e grava (ou, com --check, confere) limiares_texto.json")
    ap.add_argument("--medir", nargs="*", default=None, metavar="ARQUIVO", help="mede cada arquivo contra os limiares gravados")
    ap.add_argument("--limiares", default=str(ARQ_LIMIARES), help="arquivo dos limiares (padrão: resultados_alvo/fase4/limiares_texto.json)")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    if not args.calibrar and args.medir is None:
        ap.error("informe --calibrar ou --medir")
    arq_lim = Path(args.limiares)
    if args.calibrar:
        cal = calibracao_do_repositorio()
        c = cal["metadados"]["corpus"]
        print(f"corpus: {c['itens']} textos ({c['por_fonte']}), {c['frases']} frases, {cal['metadados']['arquivos_lidos']} arquivos; exemplo canônico: {cal['metadados']['exemplo_canonico']}")
        for met in METRICAS:
            lim = cal["limiares"][met["chave"]]
            print(f"  {met['chave']}: {lim['valor']} ({lim['tipo']}" + (f"; o plano antecipou {lim['provisorio_do_plano']}" if lim.get("provisorio_do_plano") is not None else "") + ")")
        if args.check:
            antigo = carregar_limiares(arq_lim) if arq_lim.exists() else None
            if antigo is not None and _sem_data(antigo) == _sem_data(json.loads(json.dumps(cal, ensure_ascii=False))):
                print(f"--check: {arq_lim.name} bate com o corpus atual")
                return 0
            print(f"--check: {arq_lim.name} DIFERE do corpus atual" + (" (não existe)" if antigo is None else "; é um retrato datado: rode --calibrar para atualizar"))
            return 1
        gravar_limiares(arq_lim, cal)
        print(f"gravado: {arq_lim}")
        return 0
    lim = carregar_limiares(arq_lim)
    codigo = 0
    for nome in args.medir or []:
        texto = Path(nome).read_text(encoding="utf-8")
        m = medir(texto)
        av = avaliar(m, lim)
        print(f"{nome}: {'passa' if av['aprovado'] else 'REPROVA'}; alarme do Flesch: {'sim' if av['alarme_flesch'] else 'não'}; {m['palavras']} palavras, {m['frases']} frases")
        for met in METRICAS:
            c = av["criterios"][met["chave"]]
            estado = {True: "passa", False: "REPROVA", None: "só leitura"}[c["passa"]]
            print(f"  {met['nome']}: {c['valor']} (limiar {c['limiar']}; {estado})")
        if m["termos_sem_expansao"]:
            print(f"  termos sem expansão: {', '.join(m['termos_sem_expansao'])}")
        if m["preenchimentos"]:
            print(f"  preenchimentos: {_termos_txt(m['preenchimentos'])}")
        codigo = max(codigo, 0 if av["aprovado"] else 1)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
