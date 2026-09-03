#!/usr/bin/env python3
# ! Alteração de IA - Revisar: taxonomia de erros do experimento — 6 classes derivadas
# das fases de compilador e 3 níveis de dificuldade, mais o conjunto fechado de causas raiz.
# ! Motivo: sem taxonomia fixa não dá para medir acerto POR CLASSE nem POR DIFICULDADE, que
# é o que revela onde cada modelo quebra (uma nota única esconderia isso). As classes seguem
# as fases de compilador porque é a estrutura pedida para organizar o corpus de erros.
#
# Distinção importante entre duas coisas que parecem a mesma:
#   - CLASSES: como o corpus de erros é ORGANIZADO e rotulado (nomes de fase de compilador).
#   - CAUSAS_RAIZ: o que o modelo precisa RESPONDER (nomes do domínio HTTP/API).
# Os nomes das causas são de domínio de propósito. O trabalho PA-Tool (ACL 2026) mediu
# +17 pontos no Qwen2.5-3B só por alinhar nomes ao que o modelo viu no pré-treino; pedir
# que ele responda "analise_lexica" puxaria o prior de tokenizar código-fonte, que é a
# tarefa errada. Se a estrutura de fases ajuda ou atrapalha é justamente o que os braços
# B e C do experimento medem.

CLASSES = {
    1: {
        "id": "lexica",
        "fase_compilador": "Análise léxica",
        "pergunta": "O corpo da resposta é sequer legível?",
        "descricao": "Falhas em que o dado não chega em forma processável.",
    },
    2: {
        "id": "sintatica",
        "fase_compilador": "Análise sintática",
        "pergunta": "A forma da resposta bate com a esperada?",
        "descricao": "Estrutura divergente: campo ausente, renomeado, aninhamento errado.",
    },
    3: {
        "id": "semantica",
        "fase_compilador": "Análise semântica",
        "pergunta": "Os tipos e os domínios fazem sentido?",
        "descricao": "Forma correta, conteúdo incompatível: tipo trocado, enum inválido, formato de data.",
    },
    4: {
        "id": "traducao",
        "fase_compilador": "Geração de código intermediário",
        "pergunta": "O mapeamento entre as camadas está correto?",
        "descricao": "Dado válido, porém traduzido errado: escala, unidade, chave de junção trocada.",
    },
    5: {
        "id": "runtime",
        "fase_compilador": "Otimização de código",
        "pergunta": "O comportamento no tempo e no estado está correto?",
        "descricao": "Latência, limite de requisições, cache servindo dado velho, duplicação.",
    },
    6: {
        "id": "efeito",
        "fase_compilador": "Geração de código objeto",
        "pergunta": "O que o usuário de fato vê está correto?",
        "descricao": "Falha observável só na interface, sem erro de rede aparente.",
    },
}

NIVEIS = {
    1: {
        "id": "facil",
        "criterio": "Sinal local e explícito: status de erro, corpo que não parseia, "
                    "campo claramente ausente. Detectável por regra determinística.",
    },
    2: {
        "id": "medio",
        "criterio": "HTTP 200 e corpo válido, mas o contrato divergiu (tipo, enum, formato). "
                    "Exige comparar com o contrato esperado.",
    },
    3: {
        "id": "dificil",
        "criterio": "HTTP 200, corpo válido e tipos corretos. A falha é de lógica ou estado, "
                    "normalmente só visível cruzando duas requisições ou requisição contra a tela.",
    },
}

# Conjunto fechado que o modelo deve escolher. Nomes de domínio, não de compilador.
CAUSAS_RAIZ = [
    "corpo_nao_e_json",
    "corpo_vazio",
    "resposta_truncada",
    "codificacao_incorreta",
    "campo_ausente",
    "campo_renomeado",
    "estrutura_aninhada_divergente",
    "colecao_no_lugar_de_objeto",
    "tipo_divergente",
    "valor_fora_do_dominio",
    "formato_de_data_divergente",
    "nulo_inesperado",
    "escala_ou_unidade_errada",
    "chave_de_juncao_errada",
    "contagem_inconsistente",
    "tempo_de_resposta_excedido",
    "limite_de_requisicoes",
    "dado_desatualizado",
    "registro_duplicado",
    "erro_interno_do_servidor",
    "recurso_inexistente",
    "localizador_quebrado",
    "estado_da_tela_divergente",
]


def rotulo_classe(numero: int) -> str:
    return CLASSES[numero]["id"]


def validar_caso(caso: dict) -> list[str]:
    """Confere se um caso do banco tem gabarito utilizável. Devolve a lista de
    problemas encontrados — vazia significa caso válido."""
    problemas = []
    for campo in ("id", "classe", "nivel", "entrada", "gabarito"):
        if campo not in caso:
            problemas.append(f"falta o campo '{campo}'")
    if problemas:
        return problemas

    if caso["classe"] not in CLASSES:
        problemas.append(f"classe {caso['classe']} não existe")
    if caso["nivel"] not in NIVEIS:
        problemas.append(f"nível {caso['nivel']} não existe")

    gab = caso["gabarito"]
    if gab.get("causa_raiz") not in CAUSAS_RAIZ:
        problemas.append(f"causa_raiz '{gab.get('causa_raiz')}' fora do conjunto fechado")
    if not gab.get("termos_esperados"):
        problemas.append("gabarito sem 'termos_esperados' (nada para pontuar)")
    return problemas
