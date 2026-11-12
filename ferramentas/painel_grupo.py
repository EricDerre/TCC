# ! Alteração de IA - Revisar: arquivo novo (11/11/2026) com a troca do nome do autor e de "você" por "grupo" no texto que o painel mostra. `texto_para_o_grupo`
# aplica as regras a um trecho; `para_o_grupo` aplica à página inteira, só no que a pessoa lê ou copia (texto entre as marcações, alguns atributos e o conteúdo dos
# scripts, onde ficam os dados dos gráficos); `sobras` lista o que ainda cita o nome ou "você", para o teste da página.
# ! Motivo: o Eric pediu que o painel fale do grupo, e não dele: "tudo o que cita meu nome vamos mudar para Grupo, assim como você também". O painel é montado das
# fichas, do roadmap e das decisões do Memorial, que são o registro interno de quem decidiu o quê e continuam como estão; o nome aparecia 510 vezes no texto do
# painel e "você" 42. A troca acontece na montagem da página, numa função só, para não espalhar a regra por cinco mil linhas de gerador. Marcação, classe,
# identificador, estilo e imagem embutida não são texto e não mudam (o filtro das fichas usa `data-quem="eric"`). O caminho do Windows com o nome do usuário vira
# `C:\Users\usuario`, porque o painel é público.
"""Troca do nome do autor e de "você" por "grupo" no texto do painel. Uso: `para_o_grupo(html)` na montagem da página."""
from __future__ import annotations

import re

# As regras, em ordem: primeiro as frases que pedem cuidado, depois a preposição ou o artigo com o nome, por fim o nome e o "você" sozinhos.
# Em cada par, `\1` guarda a primeira letra para a maiúscula do começo da frase continuar onde estava.
_REGRAS: list[tuple[re.Pattern, str]] = [(re.compile(p), s) for p, s in (
    (r"Eric\.Derre", "usuario"),                                                   # o caminho C:\Users\<nome>\...
    (r"da empresa em que o Eric trabalha", "da empresa de um integrante do grupo"),
    (r"\b([Dd])a janela dele\b", r"\1e uma janela do PowerShell"),                 # "lançada pelo Eric da janela dele"
    (r"\b([Nn])a janela dele\b", r"\1uma janela do PowerShell"),
    (r"\b([Dd])o próprio Eric\b", r"\1o próprio grupo"),
    (r"\b([Pp])elo próprio Eric\b", r"\1elo próprio grupo"),
    (r"\b([Oo]) próprio Eric\b", r"\1 próprio grupo"),
    (r"\b([Dd])o Eric\b", r"\1o grupo"),
    (r"\b([Pp])elo Eric\b", r"\1elo grupo"),
    (r"\b([Aa])o Eric\b", r"\1o grupo"),
    (r"\b([Nn])o Eric\b", r"\1o grupo"),
    (r"\b([Oo]) Eric\b", r"\1 grupo"),
    (r"(^|[:—|>]\s*)Eric\b", r"\1Grupo"),                                          # "Quem decide: Eric", "— Eric aprovou", começo do trecho
    (r"\bEric\b", "o grupo"),
    (r"\b([Dd])e você\b", r"\1o grupo"),
    (r"\b([Pp])ara você\b", r"\1ara o grupo"),
    (r"\b([Pp])or você\b", r"\1elo grupo"),
    (r"\b([Cc])om você\b", r"\1om o grupo"),
    (r"\b([Aa]) você\b", r"\1o grupo"),
    (r"\bVocês?\b", "O grupo"),
    (r"\bvocês?\b", "o grupo"),
)]
_RE_PARTES = re.compile(r"(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<[^>]+>)", re.DOTALL)
# Os atributos que a pessoa lê (dica, rótulo, texto alternativo) ou copia (o comando do botão "copiar").
_RE_ATRIBUTO = re.compile(r"""\b(title|aria-label|alt|placeholder|data-cmd)=("[^"]*"|'[^']*')""")
_RE_SOBRA = re.compile(r"\bEric\b|\b[Vv]ocês?\b")


def texto_para_o_grupo(texto: str) -> str:
    """O trecho com o nome do autor e "você" trocados por "grupo", mantendo a preposição, o artigo e a maiúscula do começo da frase."""
    for padrao, troca in _REGRAS:
        texto = padrao.sub(troca, texto)
    return texto


def _marcacao(tag: str) -> str:
    return _RE_ATRIBUTO.sub(lambda m: f"{m.group(1)}={m.group(2)[0]}{texto_para_o_grupo(m.group(2)[1:-1])}{m.group(2)[0]}", tag)


def _script(bloco: str) -> str:
    fim_da_abertura = bloco.index(">") + 1
    inicio_do_fecho = bloco.rindex("</")
    return bloco[:fim_da_abertura] + texto_para_o_grupo(bloco[fim_da_abertura:inicio_do_fecho]) + bloco[inicio_do_fecho:]


def para_o_grupo(html: str) -> str:
    """A página com a troca aplicada ao texto entre as marcações, aos atributos que a pessoa lê ou copia e ao conteúdo dos scripts; o resto fica byte a byte."""
    partes = _RE_PARTES.split(html)
    for i, parte in enumerate(partes):
        if i % 2 == 0:
            partes[i] = texto_para_o_grupo(parte)
        elif parte[:7].lower() == "<script":
            partes[i] = _script(parte)
        elif parte[:6].lower() != "<style":
            partes[i] = _marcacao(parte)
    return "".join(partes)


def sobras(html: str) -> list[str]:
    """Os trechos que ainda citam o nome ou "você" no que a pessoa lê ou copia; lista vazia quando a troca cobriu a página."""
    achados = []
    partes = _RE_PARTES.split(html)
    for i, parte in enumerate(partes):
        if i % 2 == 0 or parte[:7].lower() == "<script":
            alvos = [parte]
        elif parte[:6].lower() == "<style":
            alvos = []
        else:
            alvos = [m.group(2) for m in _RE_ATRIBUTO.finditer(parte)]
        for alvo in alvos:
            achados += [alvo[max(0, m.start() - 40):m.end() + 40].strip() for m in _RE_SOBRA.finditer(alvo)]
    return achados
