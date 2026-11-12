# ! Alteração de IA - Revisar: arquivo novo (11/11/2026) com a organização do painel por fase: a navegação lateral em que cada fase é um cabeçalho com as suas
# abas recuadas embaixo (`html_navegacao`), a faixa do alto de cada aba dizendo de que fase ela é e quais são as abas irmãs (`com_trilho`), os cartões do roadmap
# em linha, com a pergunta que a fase responde, o estado e o "Saiba mais" (`cartoes_do_roadmap`, `secao_roadmap`), a aba de visão de cada fase, com o caminho da
# fase em passos, o que ela mostrou, os tópicos e as corridas (`secao_fase`, `secoes_das_fases`), e o Início como resumo do projeto inteiro (`secao_inicio`).
# ! Motivo: o Eric pediu, em 11/11/2026, seis mudanças no painel. Os cartões das fases no Roadmap eram estreitos e altos, com o texto do estado descendo por
# várias rolagens; a navegação lateral listava 44 abas em oito grupos que não diziam de que fase era cada uma, e não dava para distinguir o título do grupo da aba
# clicável; e o Início era uma lista de fichas e corridas, sem dizer o que o projeto é. A estrutura segue o documento do TCC (seção 5.1 e seções 6.1 a 6.7): uma
# fase por vez, cada uma com a pergunta que responde. O texto do estado, as perguntas, as descobertas e as figuras são lidos do roadmap e do README por código;
# aqui ficam só os passos de cada fase, em palavras, sem número de resultado.
"""Painel por fase: navegação, cartões do roadmap, visão de cada fase, Início e a faixa de sub-abas."""
from __future__ import annotations

import base64
import html
import json
import re
from collections.abc import Callable
from pathlib import Path

import painel_textos as pt

RAIZ = Path(__file__).resolve().parents[1]
README = RAIZ / "README.md"
CALIBRACAO = RAIZ / "Programacao" / "AgenteCore" / "experimentos" / "resultados_alvo" / "fase4" / "calibracao.json"

GERAL = "Visão geral"
APOIO = "Pesquisa e documentação"
ROTULO_ESTADO = {"concluida": "Concluída", "andamento": "Em andamento", "nao_iniciada": "Não iniciada", "outro": "Sem estado"}
# Quem faz cada passo: a mesma legenda da figura "Como o agente trabalha" (azul para código, laranja para o modelo), mais as pessoas e o que sai no fim.
TIPOS = {"codigo": "Feito em código", "modelo": "Feito pelo modelo de linguagem", "pessoa": "Feito ou decidido por pessoas", "saida": "O que sai no fim"}

# O fluxo do agente, nos mesmos seis passos e três saídas da figura do README (gerar_figuras_documentos.py). `{k}` e `{modelo}` vêm de fase4/calibracao.json.
# Cada item: tipo, título, texto e a aba em que o passo é medido ("" quando não há uma aba só dele).
PASSOS_DO_AGENTE = [
    ("codigo", "Roda o roteiro", "Abre a página no navegador e segue os passos, olhando a tela e as chamadas à API.", "reproducao"),
    ("codigo", "Detecta a falha", "Uma conferência do roteiro não passa, ou a resposta da API mudou.", ""),
    ("codigo", "Reduz o que viu", "Fica só o que mudou contra a tela normal: é a poda, feita em código.", "tela"),
    ("codigo", "Busca na biblioteca", "Separa os {k} verbetes de documentação mais parecidos com o caso.", "calibracao"),
    ("modelo", "O modelo diagnostica", "{modelo}, na própria máquina, só com CPU, escolhe a causa numa lista fechada.", "tela"),
    ("codigo", "Confere e dá um selo", "O código confere a resposta e dá um selo de confiança: alto, médio ou baixo.", "calibracao"),
]
SAIDAS_DO_AGENTE = [
    ("Falha de contrato", "A API mudou: sai um relatório para o analista, com a causa e o selo.", "texto"),
    ("Localizador quebrado", "A tela mudou: o código acha outro seletor e testa de novo, sem o modelo.", "cura"),
    ("Aprendizado", "O modelo propõe um acréscimo à biblioteca; filtros em código decidem se entra.", "biblioteca"),
]
TRILHA_DO_AGENTE = ("Trilha aberta", "Cada passo acima fica gravado: o que o agente viu, o que o modelo respondeu e o que o código conferiu. O relatório para quem revisa sai dessa trilha.", "trilha")

# As fases, na ordem do roadmap. `grupo` é o nome do grupo na navegação; `sid` é a aba de visão da fase; `readme` é a chave da linha na tabela "Onde o projeto
# está" do README; `roadmap` é o começo do nome da linha na tabela 1 do roadmap; `tcc` é a seção do documento do TCC que a aba segue; `passos` é o caminho da
# fase (tipo, título, texto, aba). Nenhum texto daqui traz número de resultado: os números ficam nas abas, lidos dos registros.
FASES: list[dict] = [
    {"grupo": "Fase 1", "sid": "f-1", "readme": "1", "roadmap": "1 ", "curto": "Ambiente e cobaias", "titulo": "Fase 1: o ambiente de teste e as cobaias", "tcc": "6.1",
     "passos": [
         ("codigo", "Instalador único", "Um instalador prepara a máquina com tudo o que as medições pedem, no Windows e no Linux.", ""),
         ("pessoa", "CobaiaFront", "O site em PHP de um restaurante, cedido por um integrante do grupo e mantido como veio. É o sistema antigo que o agente usa pela tela.", ""),
         ("codigo", "CobaiaAPI", "Uma API escrita para o projeto, sobre o mesmo banco de dados. O site original não chamava nenhuma API, então a fronteira que a pesquisa estuda foi construída.", ""),
         ("codigo", "Falhas ligadas de propósito", "Modos de falha que se ligam e desligam sempre do mesmo jeito, para a resposta certa ser conhecida de antemão.", ""),
         ("pessoa", "Banco de casos", "Cada caso é uma falha com o gabarito: a causa certa, tirada de uma lista fechada em seis classes.", ""),
     ]},
    {"grupo": "Fase 2-A", "sid": "f-2a", "readme": "2-A", "roadmap": "2-A", "curto": "Prompts sem documentação", "titulo": "Fase 2-A: o modelo sozinho, sem documentação", "tcc": "6.2",
     "passos": [
         ("codigo", "Os casos do banco", "Cada modelo recebe os mesmos casos, um por vez, sem nenhuma documentação do sistema.", ""),
         ("pessoa", "Formas de perguntar", "O pedido é escrito de mais de um jeito, para ver se organizar o raciocínio em etapas ajuda.", "fase2a"),
         ("modelo", "O modelo responde", "Só com o que já sabe, o modelo escolhe a causa da falha numa lista fechada.", "fase2a"),
         ("codigo", "O código confere", "Cada resposta é comparada com o gabarito, e sai o acerto por modelo, por forma de pergunta e por tipo de defeito.", "fase2a"),
         ("pessoa", "O que ficou decidido", "O pedido simples, sem etapas, virou o padrão das fases seguintes (decisão 19).", ""),
     ]},
    {"grupo": "Fase 2-B", "sid": "f-2b", "readme": "2-B", "roadmap": "2-B", "curto": "Biblioteca recuperada", "titulo": "Fase 2-B: a documentação escrita por pessoas", "tcc": "6.3",
     "passos": [
         ("pessoa", "Biblioteca escrita à mão", "Verbetes curtos sobre o sistema testado: contratos, erros conhecidos e regras de negócio.", ""),
         ("codigo", "Seis condições", "Os mesmos casos são repetidos de seis jeitos: sem documentação, com a biblioteca inteira, com os verbetes mais parecidos, só com o verbete certo e com verbetes errados de propósito.", "fase2b"),
         ("modelo", "O modelo responde", "Com o que recebeu, o modelo escolhe a causa na mesma lista fechada.", "fase2b"),
         ("codigo", "O código confere", "O acerto de cada condição mostra quanto a documentação ajuda e quanto a documentação errada atrapalha.", "fase2b"),
         ("pessoa", "O que ficou decidido", "Entregar só os verbetes mais parecidos com o caso virou o modo de operação, e nada entra na biblioteca sem conferência em código (decisão 28).", ""),
     ]},
    {"grupo": "Fase 3", "sid": "f-3", "readme": "3", "roadmap": "3 ", "curto": "Biblioteca gerida pelo modelo", "titulo": "Fase 3: o modelo cuida da própria documentação", "tcc": "6.4",
     "passos": [
         ("codigo", "Casos em dois grupos", "Num grupo o modelo vê a resposta certa, para aprender. O outro fica só para avaliar, e o modelo nunca vê a resposta.", "metodo"),
         ("modelo", "O modelo diagnostica e propõe", "Em três rodadas, chamadas épocas, cada modelo diagnostica os casos e propõe acréscimos à sua cópia da biblioteca.", "fase3"),
         ("codigo", "O código decide o que entra", "Um validador confere cada proposta. Só entra acréscimo: nota, correção de trecho ou verbete novo.", "fase3"),
         ("codigo", "A regra fixada antes", "A escolha do modelo segue uma regra escrita antes da bateria (decisão 36), e depois é posta à prova por sorteios dos casos e por outros critérios.", "decisao"),
         ("pessoa", "O que ficou decidido", "O agente usa o modelo que venceu pela regra, com a primeira versão da biblioteca escrita por ele (decisão 52).", "decisao"),
     ]},
    {"grupo": "Fase 3-B", "sid": "f-3b", "readme": "3-B", "roadmap": "3-B", "curto": "Testes complementares", "titulo": "Fase 3-B: as dúvidas que a Fase 3 deixou", "tcc": "6.5",
     "passos": [
         ("codigo", "Ponte de versão", "O programa que roda o modelo se atualiza sozinho. Antes de toda medição nova, os mesmos casos são relidos para provar que a versão nova repete a antiga.", "tresb"),
         ("modelo", "Casos inéditos", "O ganho se repete em casos que nenhuma biblioteca viu?", "tresb"),
         ("modelo", "Troca cruzada", "A biblioteca escrita por um modelo serve para outro modelo ler?", "cruzada"),
         ("modelo", "O modelo de programação", "O modelo da mesma família voltado a programação seria uma escolha melhor?", "comparativo"),
         ("codigo", "Busca e piso", "A busca por significado rende mais que a busca por palavras? E um modelo sem ajuste por instrução faz a tarefa?", "recuperador"),
         ("pessoa", "Biblioteca de produção", "A versão escolhida foi revisada e virou a biblioteca que o agente usa.", "curadoria"),
         ("pessoa", "O que ficou decidido", "O padrão do agente é o modelo com a biblioteca que ele mesmo escreveu, e trocar o modelo que lê pede medir de novo (decisão 69).", "fechamento"),
     ]},
    {"grupo": "Pré-Fase 4", "sid": "f-pre4", "readme": "Pré-Fase 4", "roadmap": "Pré-Fase 4", "curto": "Pesquisa antes da tela", "titulo": "Pré-Fase 4: a pausa de pesquisa antes da tela", "tcc": "6.6",
     "passos": [
         ("pessoa", "Modelos grandes pelo disco", "Um modelo maior, lido aos poucos do disco, caberia nesta máquina? A via foi medida e fechada como motor do agente (decisão 75).", "colibri"),
         ("codigo", "Atlas das competências", "Um mapa de quais verbetes a busca entrega para cada tipo de defeito e do que o modelo faz com eles.", "atlas"),
         ("modelo", "Raciocínio aberto", "A probabilidade que o modelo dá à própria resposta separa acertos de erros o bastante para triagem.", "raciocinio"),
         ("pessoa", "Especificação da trilha", "O desenho do registro de cada passo do agente e do relatório por caso foi aprovado como base da Fase 4 (decisão 77).", "raciocinio"),
     ]},
    {"grupo": "Fase 4", "sid": "f-4", "readme": "4", "roadmap": "4 ", "curto": "Agente na tela", "titulo": "Fase 4: o agente na tela", "tcc": "6.7", "passos": "agente"},
    {"grupo": "Pós-Fase 4", "sid": "f-pos4", "readme": "Pós-Fase 4", "roadmap": "Pós-Fase 4", "curto": "O que chega a quem lê", "titulo": "Pós-Fase 4: o que chega a quem lê", "tcc": "",
     "passos": [
         ("codigo", "Relatório no molde do syllabus", "O relatório de cada caso segue o molde do relatório de defeito do programa de estudo do ISTQB.", "texto"),
         ("codigo", "Leitura dos verbetes", "Cada verbete ganhou uma versão para pessoas, gerada em código e revisada por um analista.", "texto"),
         ("codigo", "Filtros de texto", "Medidas em código acusam texto longo, repetido ou com termo sem explicação.", "texto"),
         ("codigo", "Árvore de decisão", "Cada caso mostra, passo a passo, o que foi lido, o que entrou e por que a causa foi escolhida.", "arvore"),
         ("codigo", "Barra de progresso e Git", "Uma barra diz quanto falta enquanto o modelo pensa, e um protótipo lê o que mudou no código para dizer o que rodar.", "progresso"),
         ("pessoa", "Revisão humana", "Um analista de teste leu os relatórios, um por vez e às cegas, e disse o que decidiria em cada um.", "revisaov3"),
         ("modelo", "Experimentos antes da Fase 5", "As notas do modelo ajudam? Um segundo pedido conserta mais do que estraga? Um analista de documentação escreve melhor?", "semnotas"),
     ]},
    {"grupo": "Fase 5", "sid": "f-5", "readme": "5", "roadmap": "5 ", "curto": "Medição de valor", "titulo": "Fase 5: o agente contra uma pessoa", "tcc": "5.7",
     "passos": [
         ("codigo", "Os mesmos cenários de falha", "O agente e as pessoas recebem os mesmos cenários, com quebras de contrato e quebras de localizador.", "cenarios"),
         ("pessoa", "Linha de base manual", "Integrantes do grupo resolvem cada cenário à mão, com o tempo cronometrado.", ""),
         ("modelo", "O agente", "O agente roda os mesmos cenários, com repetições, e o banco de dados é restaurado entre uma e outra.", "cenarios"),
         ("codigo", "As duas medidas", "O tempo médio de reparo e a parcela dos cenários resolvidos, lidos em separado para contrato e para localizador.", ""),
     ]},
]
_POR_GRUPO = {f["grupo"]: f for f in FASES}

# De que fase é cada corrida do roadmap, pelo número. As corridas 14 e 15 rodaram durante a Pré-Fase 4, mas fecham a Fase 3-B (ponte de versão e a repetição do
# confronto nos inéditos); a de letra Q é da Pós-Fase 4.
FAIXAS_DE_CORRIDAS = [(1, 10, "Fase 3-B"), (11, 13, "Pré-Fase 4"), (14, 15, "Fase 3-B"), (16, 24, "Fase 4"), (25, 27, "Pós-Fase 4")]

# Cada descoberta do README ("O que já descobrimos"): a fase em que foi medida e a aba com o detalhe.
DESCOBERTAS = {
    "A documentação faz diferença?": ("Fase 2-B", "fase2b"),
    "Qual modelo ficou?": ("Fase 3", "decisao"),
    "A biblioteca serve para qualquer modelo?": ("Fase 3-B", "cruzada"),
    "O agente sabe quando pode estar errado?": ("Fase 4", "calibracao"),
    "Ler da tela é tão bom quanto ler um caso escrito?": ("Fase 4", "tela"),
    "E em casos que a biblioteca nunca viu?": ("Fase 4", "ineditosf4"),
    "Quanto tempo o agente leva?": ("Fase 4", "cenarios"),
    "O que o agente escreve entra na biblioteca sem controle?": ("Fase 4", "biblioteca"),
}
TITULO_DOS_LIMITES = "O que ainda não dá para afirmar"


def _esc(s) -> str:
    return html.escape(str(s), quote=True)


def _chip(classe: str, texto: str | None = None) -> str:
    return f'<span class="chip {classe}">{_esc(texto or ROTULO_ESTADO.get(classe, ROTULO_ESTADO["outro"]))}</span>'


ROTULO_CORRIDA = {"feita": "Feita", "rodando": "Rodando", "pendente": "Pendente", "opcional": "Opcional", "aguarda": "Aguarda decisão", "outro": "Sem estado"}


def _estado_que_acrescenta(estado: str, classe: str) -> str:
    """O estado curto do README quando ele diz mais do que a etiqueta (por exemplo, quais pacotes já saíram); vazio quando é só a etiqueta."""
    return "" if estado.strip().lower() == ROTULO_ESTADO.get(classe, "").lower() else estado.strip()


# ------------------------------------------------------------------ leitura do README e do roadmap

def _secao(md: str, titulo: str) -> str:
    """O corpo da seção de nível 2 com esse título, sem os comentários; vazio se não existir."""
    for t, corpo in pt.secoes(pt.sem_comentarios(md)):
        if t.strip() == titulo:
            return corpo
    return ""


def _paragrafos(md: str) -> list[str]:
    return [" ".join(l.strip() for l in p.splitlines()) for p in re.split(r"\n\s*\n", md.strip()) if p.strip()]


def apresentacao_do_readme(readme_md: str) -> str:
    """O parágrafo que apresenta o projeto, logo abaixo do título e dos selos do README."""
    topo = pt.sem_comentarios(readme_md).split("\n## ")[0]
    for p in _paragrafos(topo):
        if not p.startswith(("#", "[![", ">", "|")):
            return p
    return ""


def tabela_do_readme(readme_md: str) -> dict[str, tuple[str, str]]:
    """A tabela "Onde o projeto está" do README: {fase: (a pergunta que ela responde, o estado)}. As linhas são lidas uma a uma, porque há comentários entre elas."""
    linhas = [pt.celulas(l) for l in _secao(readme_md, "Onde o projeto está").splitlines() if l.startswith("|")]
    return {r[0]: (r[1], r[2]) for r in linhas[1:] if len(r) >= 3 and not set(r[0]) <= set("-: ")}


def descobertas_do_readme(readme_md: str) -> list[dict]:
    """As subseções de "O que já descobrimos", menos a dos limites: a pergunta, a figura (arquivo e descrição), como ler e o que isso mostra (parágrafos)."""
    achados = []
    for titulo, corpo in pt.secoes(_secao(readme_md, "O que já descobrimos"), 3):
        if not titulo or titulo.strip() == TITULO_DOS_LIMITES:
            continue
        figura = re.search(r"!\[([^\]]*)\]\(([^)\s]+)\)", corpo)
        pars = [p for p in _paragrafos(corpo) if not p.startswith("![")]
        como_ler = next((p[len("**Como ler:**"):].strip() for p in pars if p.startswith("**Como ler:**")), "")
        ini = next((i for i, p in enumerate(pars) if p.startswith("**O que isso mostra:**")), None)
        mostra = [] if ini is None else [pars[ini][len("**O que isso mostra:**"):].strip()] + pars[ini + 1:]
        achados.append({"pergunta": titulo.strip(), "figura": figura.group(2) if figura else "", "alt": figura.group(1) if figura else "", "como_ler": como_ler, "mostra": mostra})
    return achados


def limites_do_readme(readme_md: str) -> list[str]:
    """Os itens de "O que ainda não dá para afirmar", um por linha da lista."""
    for titulo, corpo in pt.secoes(_secao(readme_md, "O que já descobrimos"), 3):
        if titulo.strip() == TITULO_DOS_LIMITES:
            return [l[2:].strip() for l in corpo.splitlines() if l.startswith("- ")]
    return []


def problema_do_readme(readme_md: str) -> list[str]:
    """Os parágrafos da seção "O problema" do README."""
    return _paragrafos(_secao(readme_md, "O problema"))


def ideia_central_do_readme(readme_md: str) -> str:
    """A frase "A ideia central" da seção "Como o agente trabalha" do README, sem o rótulo."""
    for p in _paragrafos(_secao(readme_md, "Como o agente trabalha")):
        if p.startswith("**A ideia central:**"):
            return p[len("**A ideia central:**"):].strip()
    return ""


def cobaias_do_readme(readme_md: str) -> str:
    """A seção "Os dois sistemas de teste" do README: o texto de antes da tabela, cada linha da tabela como um cartão (o nome do sistema e cada coluna com o
    rótulo dela) e o texto de depois. Em cartão, e não em tabela, porque o painel recolhe toda tabela solta em "Mais informações", como se fosse dado."""
    linhas = _secao(readme_md, "Os dois sistemas de teste").strip().splitlines()
    tabela = [i for i, l in enumerate(linhas) if l.startswith("|")]
    if not tabela:
        return "".join(f"<p>{pt.inline(p)}</p>" for p in _paragrafos("\n".join(linhas)))
    cab = pt.celulas(linhas[tabela[0]])
    corpo = [pt.celulas(linhas[i]) for i in tabela[1:] if not set(pt.celulas(linhas[i])[0]) <= set("-: ")]
    cartoes = "".join("<div><h3>" + pt.inline(r[0]) + "</h3>" + "".join(f'<p><span class="rotulo">{pt.inline(c)}</span>{pt.inline(v)}</p>' for c, v in zip(cab[1:], r[1:])) + "</div>"
                      for r in corpo)
    antes = "".join(f"<p>{pt.inline(p)}</p>" for p in _paragrafos("\n".join(linhas[:tabela[0]])))
    depois = "".join(f"<p>{pt.inline(p)}</p>" for p in _paragrafos("\n".join(linhas[tabela[-1] + 1:])))
    return f'{antes}<div class="problema cobaias">{cartoes}</div>{depois}'


def ler_fluxo(caminho: Path = CALIBRACAO) -> dict:
    """Os dois dados que a figura do fluxo do agente usa: quantos verbetes vão ao modelo e qual é o modelo (fase4/calibracao.json)."""
    cal = json.loads(caminho.read_text(encoding="utf-8"))
    return {"k": cal["k_escolhido"], "modelo": cal["metadados"]["modelo"]}


def carregar_figura(relativo: str, raiz: Path = RAIZ) -> str | None:
    """A figura do README como endereço embutido (data URI), ou None se o arquivo não existir ou sair da pasta do projeto."""
    alvo = (raiz / relativo).resolve()
    if raiz.resolve() not in alvo.parents or not alvo.is_file() or alvo.suffix.lower() != ".png":
        return None
    return "data:image/png;base64," + base64.b64encode(alvo.read_bytes()).decode("ascii")


def fase_do_grupo(grupo: str) -> dict | None:
    return _POR_GRUPO.get(grupo)


def linha_do_roadmap(road: dict, fase: dict):
    """A linha da tabela 1 do roadmap que é desta fase (o nome começa pelo prefixo da fase), ou None."""
    return next((f for f in road["fases"] if f.nome.startswith(fase["roadmap"])), None)


def fase_da_corrida(numero: str) -> str | None:
    """O grupo (a fase) de uma corrida do roadmap, pelo número: "18b" é da faixa do 18; as de letra Q são da Pós-Fase 4."""
    m = re.match(r"\d+", numero.strip())
    if not m:
        return "Pós-Fase 4" if numero.strip().upper().startswith("Q") else None
    n = int(m.group())
    return next((grupo for ini, fim, grupo in FAIXAS_DE_CORRIDAS if ini <= n <= fim), None)


def corridas_da_fase(road: dict, grupo: str) -> list:
    return [c for c in road["corridas"] if fase_da_corrida(c.numero) == grupo]


def abas_fora_de_lugar(nav: list) -> list[str]:
    """O que impede a navegação por fase: fase sem grupo, grupo de fase que não começa pela aba de visão, passo ou descoberta apontando para aba que não existe."""
    erros = []
    ids = {sid for _, abas in nav for sid, _, _ in abas}
    grupos = dict(nav)
    for f in FASES:
        if f["grupo"] not in grupos:
            erros.append(f'{f["grupo"]}: a fase não tem grupo na navegação')
        elif not grupos[f["grupo"]] or grupos[f["grupo"]][0][0] != f["sid"]:
            erros.append(f'{f["grupo"]}: a primeira aba do grupo precisa ser a visão da fase ({f["sid"]})')
        erros += [f'{f["grupo"]}: o passo "{t}" aponta para a aba {alvo}, que não existe' for _, t, _, alvo in _passos(f, {"k": 0, "modelo": ""}) if alvo and alvo not in ids]
    erros += [f'descoberta "{p}": aponta para a aba {alvo}, que não existe' for p, (_, alvo) in DESCOBERTAS.items() if alvo not in ids]
    erros += [f'saída do agente "{t}": aponta para a aba {alvo}, que não existe' for t, _, alvo in [*SAIDAS_DO_AGENTE, TRILHA_DO_AGENTE] if alvo not in ids]
    return erros


def _passos(fase: dict, fluxo: dict) -> list[tuple]:
    if fase["passos"] == "agente":
        return [(tipo, t, x.format(**fluxo), alvo) for tipo, t, x, alvo in PASSOS_DO_AGENTE]
    return fase["passos"]


def _nome_curto_da_corrida(nome: str) -> str:
    m = re.search(r"\*\*(.+?)\*\*", nome)
    return m.group(1) if m else nome.split(" — ")[0]


# ------------------------------------------------------------------ navegação lateral e a faixa de sub-abas

def html_navegacao(nav: list, road: dict) -> str:
    """A navegação lateral: os grupos gerais com o título em letra pequena e as abas embaixo; cada fase com um cabeçalho que abre a visão da fase, a bolinha do
    estado e as abas dela recuadas, à vista só na fase aberta (o script abre a fase da aba atual)."""
    partes = []
    for grupo, abas in nav:
        fase = fase_do_grupo(grupo)
        if fase is None:
            botoes = "".join(f'<button data-alvo="{sid}">{_esc(nome)}</button>' for sid, nome, _ in abas)
            partes.append(f'<div class="nav-grupo" data-grupo="{_esc(grupo)}"><span class="grupo">{_esc(grupo)}</span>{botoes}</div>')
            continue
        linha = linha_do_roadmap(road, fase)
        classe = linha.classe if linha else "outro"
        subs = "".join(f'<button data-alvo="{sid}">{_esc(nome)}</button>' for sid, nome, _ in abas[1:])
        partes.append(
            f'<div class="nav-grupo nav-fase {classe}" data-grupo="{_esc(grupo)}">'
            f'<button class="fase-topo" data-alvo="{abas[0][0]}" aria-expanded="false" title="{_esc(ROTULO_ESTADO.get(classe, ROTULO_ESTADO["outro"]))}">'
            f'<span class="bolinha" aria-hidden="true"></span><span class="rot">{_esc(grupo)}</span><span class="nome">{_esc(fase["curto"])}</span>'
            f'<span class="qtd" aria-hidden="true">{len(abas) - 1 or ""}</span></button><div class="nav-sub">{subs}</div></div>')
    return "".join(partes)


_AQUI = ' class="aqui"'


def _trilho(grupo: str, abas: list, fase: dict, classe: str, atual: str) -> str:
    botoes = "".join(f'<button data-alvo="{sid}"{_AQUI if sid == atual else ""}>{_esc("Visão da fase" if i == 0 else nome)}</button>'
                     for i, (sid, nome, _) in enumerate(abas))
    return (f'<nav class="trilho {classe}" aria-label="Abas da {_esc(grupo)}"><span class="trilho-fase"><b>{_esc(grupo)}</b> {_esc(fase["curto"])} {_chip(classe)}</span>'
            f'<span class="trilho-abas">{botoes}</span></nav>')


def com_trilho(pagina: str, nav: list, road: dict) -> str:
    """A página com a faixa de sub-abas no alto de cada aba que pertence a uma fase: o nome da fase, o estado e as abas irmãs, com a atual marcada."""
    for grupo, abas in nav:
        fase = fase_do_grupo(grupo)
        if fase is None:
            continue
        linha = linha_do_roadmap(road, fase)
        classe = linha.classe if linha else "outro"
        for sid, _, _ in abas:
            m = re.search(rf'<section id="{re.escape(sid)}"[^>]*>', pagina)
            if m and not pagina[m.end():m.end() + 30].lstrip().startswith('<nav class="trilho'):
                pagina = pagina[:m.end()] + "\n" + _trilho(grupo, abas, fase, classe, sid) + pagina[m.end():]
    return pagina


# ------------------------------------------------------------------ peças visuais

def cadeia(passos: list[tuple], nav_ids: set[str] | None = None) -> str:
    """O caminho em passos numerados, cada um com a cor de quem faz (código, modelo, pessoa) e o atalho para a aba em que ele é medido."""
    itens = []
    for tipo, titulo, texto, alvo in passos:
        atalho = f'<a href="#{alvo}" data-ir="{alvo}|">ver na aba</a>' if alvo and (nav_ids is None or alvo in nav_ids) else ""
        itens.append(f'<li class="{tipo}"><b>{_esc(titulo)}</b><p>{_esc(texto)}</p>{atalho}</li>')
    return f'<ol class="cadeia">{"".join(itens)}</ol>'


def legenda_da_cadeia(tipos: list[str]) -> str:
    return '<p class="legenda-cadeia">' + "".join(f'<span><i class="{t}"></i>{_esc(TIPOS[t])}</span>' for t in TIPOS if t in tipos) + "</p>"


def fluxo_do_agente(fluxo: dict, nav_ids: set[str] | None = None) -> str:
    """O fluxo do agente em seis passos, as três saídas e a trilha, como na figura do README, desenhado em HTML para acompanhar o tema claro e o escuro."""
    passos = [(tipo, t, x.format(**fluxo), alvo) for tipo, t, x, alvo in PASSOS_DO_AGENTE]

    def atalho(alvo: str) -> str:
        return f'<a href="#{alvo}" data-ir="{alvo}|">ver na aba</a>' if alvo and (nav_ids is None or alvo in nav_ids) else ""

    saidas = "".join(f"<div><b>{_esc(t)}</b><p>{_esc(x)}</p>{atalho(alvo)}</div>" for t, x, alvo in SAIDAS_DO_AGENTE)
    t, x, alvo = TRILHA_DO_AGENTE
    return (f'<div class="fluxo-agente">{cadeia(passos, nav_ids)}<p class="liga">Depois do selo, sai uma destas três coisas</p><div class="saidas">{saidas}</div>'
            f'<div class="trilha-caixa"><b>{_esc(t)}</b><p>{_esc(x)}</p>{atalho(alvo)}</div>{legenda_da_cadeia(["codigo", "modelo", "saida"])}'
            '<p class="como-ler"><strong>Como ler:</strong> siga os passos na ordem dos números. O azul é código comum, que dá sempre o mesmo resultado. O laranja é o passo em que '
            'o modelo responde. As caixas tracejadas são o que sai no fim, e a trilha guarda tudo para quem for revisar.</p></div>')


def caminho_do_projeto(road: dict, perguntas: dict) -> str:
    """As fases em sequência, cada uma com o estado e a pergunta que responde; cada cartão abre a visão da fase."""
    itens = []
    for f in FASES:
        linha = linha_do_roadmap(road, f)
        classe = linha.classe if linha else "outro"
        pergunta = perguntas.get(f["readme"], ("", ""))[0]
        itens.append(f'<li class="{classe}"><a href="#{f["sid"]}" data-ir="{f["sid"]}|"><b>{_esc(f["grupo"])}</b><span class="estado">{_esc(ROTULO_ESTADO.get(classe, ROTULO_ESTADO["outro"]))}</span>'
                     f'<span class="q">{pt.inline(pergunta)}</span></a></li>')
    classes = [(linha_do_roadmap(road, f).classe if linha_do_roadmap(road, f) else "outro") for f in FASES]
    feitas, andando = classes.count("concluida"), classes.count("andamento")
    barra = "".join(f'<i class="{c}" style="flex:1"></i>' for c in classes)
    resumo = f'{feitas} de {len(FASES)} fases concluídas' + (f', {andando} em andamento' if andando else "")
    return (f'<div class="barra-fases" role="img" aria-label="{_esc(resumo)}">{barra}</div><p class="nota">{_esc(resumo)}. Cada cartão abre a visão da fase.</p>'
            f'<ol class="caminho">{"".join(itens)}</ol>')


def cartoes_do_roadmap(nav: list, road: dict, perguntas: dict) -> str:
    """Um cartão em linha por fase do roadmap: a fase e o estado à esquerda, a pergunta que ela responde e o que foi feito no meio, e o "Saiba mais" à direita,
    que abre a visão da fase. O texto longo do estado não entra aqui: fica na visão da fase, em "Mais detalhes". As linhas do roadmap que não são fase (a da
    documentação) vêm no fim, com o estado recolhido."""
    grupos = dict(nav)
    linhas, usadas = [], set()
    for f in FASES:
        linha = linha_do_roadmap(road, f)
        if linha is None:
            continue
        usadas.add(linha.nome)
        pergunta, estado_curto = perguntas.get(f["readme"], ("", ""))
        n_abas = max(len(grupos.get(f["grupo"], [])) - 1, 0)
        n_corr = len(corridas_da_fase(road, f["grupo"]))
        conta = " · ".join(x for x in (f'{n_abas} tópico{"" if n_abas == 1 else "s"}' if n_abas else "", f'{n_corr} corrida{"" if n_corr == 1 else "s"}' if n_corr else "") if x)
        linhas.append(
            f'<article class="linha-fase {linha.classe}"><div class="lf-id"><b>{_esc(f["grupo"])}</b><small>{_esc(f["curto"])}</small>{_chip(linha.classe)}</div>'
            f'<div class="lf-corpo"><p><span class="rotulo">A pergunta que ela responde</span>{pt.inline(pergunta)}</p>'
            f'<p><span class="rotulo">O que é</span>{pt.inline(linha.o_que_e)}</p>'
            + (f'<p><span class="rotulo">Estado</span>{pt.inline(_estado_que_acrescenta(estado_curto, linha.classe))}</p>' if _estado_que_acrescenta(estado_curto, linha.classe) else "") + "</div>"
            f'<div class="lf-acao"><a class="saiba-mais" href="#{f["sid"]}" data-ir="{f["sid"]}|">Saiba mais</a><small>{_esc(conta)}</small></div></article>')
    for linha in road["fases"]:
        if linha.nome in usadas:
            continue
        linhas.append(
            f'<article class="linha-fase {linha.classe}"><div class="lf-id"><b>{pt.inline(linha.nome)}</b>{_chip(linha.classe)}</div>'
            f'<div class="lf-corpo"><p><span class="rotulo">O que é</span>{pt.inline(linha.o_que_e)}</p>'
            f'<details><summary>Estado completo</summary><p>{pt.inline(linha.estado)}</p></details></div><div class="lf-acao"></div></article>')
    return f'<div class="linhas-fase">{"".join(linhas)}</div>'


# ------------------------------------------------------------------ as abas

def secao_roadmap(road: dict, nav: list, cartoes_corridas: Callable, readme_md: str | None = None) -> str:
    """A aba Roadmap: as fases em cartões em linha, as corridas agrupadas por fase (abertas só onde ainda há o que rodar) e o resto do roadmap recolhido por título."""
    readme_md = README.read_text(encoding="utf-8") if readme_md is None else readme_md
    perguntas = tabela_do_readme(readme_md)
    grupos_corridas = []
    for f in FASES:
        corridas = corridas_da_fase(road, f["grupo"])
        if not corridas:
            continue
        falta = [c for c in corridas if c.classe in ("pendente", "rodando", "aguarda")]
        feitas = sum(c.classe == "feita" for c in corridas)
        resumo = f'{len(corridas)} corrida{"" if len(corridas) == 1 else "s"}: {feitas} feita{"" if feitas == 1 else "s"}' + (f', {len(falta)} por rodar' if falta else "")
        grupos_corridas.append(f'<details class="grupo-corridas"{" open" if falta else ""}><summary>{_esc(f["grupo"])} <span class="nota">{_esc(resumo)}</span></summary>'
                               f'{cartoes_corridas(road, [c.numero for c in corridas])}</details>')
    sem_fase = [c.numero for c in road["corridas"] if fase_da_corrida(c.numero) is None]
    if sem_fase:
        grupos_corridas.append(f'<details class="grupo-corridas" open><summary>Sem fase</summary>{cartoes_corridas(road, sem_fase)}</details>')
    resto = "".join(f'<details class="secao-roadmap"><summary>{pt.inline(t)}</summary>{pt.md_doc_para_html(c)}</details>' for t, c in road["secoes"])
    return f'''<section id="roadmap" hidden>
<h1>Roadmap: onde estamos e o que falta rodar</h1>
<p class="lead">Uma linha por fase, com a pergunta que ela responde e o estado. O botão "Saiba mais" abre a visão da fase, com o caminho, o que ela mostrou e os tópicos. Abaixo, as corridas de cada fase com o comando pronto. Fonte: <code>roadmap.md</code> de {_esc(road["data"])} e a tabela de fases do <code>README.md</code>.</p>
<h2>1. Onde estamos, por fase</h2>
{cartoes_do_roadmap(nav, road, perguntas)}
{pt.md_doc_para_html(road["posicao"])}
<h2>2. O que precisamos rodar (máquina), por fase</h2>
<p>As corridas ficam agrupadas pela fase a que pertencem. O grupo já vem aberto quando ainda tem corrida por rodar.</p>
{"".join(grupos_corridas)}
{pt.md_doc_para_html(road["fora_da_maquina"])}
<h2>3. Leituras e planos, como estão no roadmap</h2>
<p>Cada título abaixo é uma seção do <code>roadmap.md</code>: a primeira leitura de cada corrida e o plano de cada fase. O texto abre ao clicar.</p>
{resto}
</section>'''


def _achado(a: dict, figura: Callable | None, nav_ids: set[str]) -> str:
    alvo = DESCOBERTAS.get(a["pergunta"], ("", ""))[1]
    src = figura(a["figura"]) if figura and a["figura"] else None
    fig = (f'<figure><img src="{src}" alt="{_esc(a["alt"])}"><figcaption>{_esc(a["alt"])}.</figcaption></figure>' if src else "")
    como = f'<p class="como-ler"><strong>Como ler:</strong> {pt.inline(a["como_ler"])}</p>' if a["como_ler"] else ""
    mostra = "".join(f'<p>{"<strong>O que isso mostra:</strong> " if i == 0 else ""}{pt.inline(p)}</p>' for i, p in enumerate(a["mostra"]))
    atalho = f'<p><a class="saiba-mais" href="#{alvo}" data-ir="{alvo}|">Ver os números na aba</a></p>' if alvo in nav_ids else ""
    return f'<article class="achado"><h3>{pt.inline(a["pergunta"])}</h3>{fig}{como}{mostra}{atalho}</article>'


def secao_fase(fase: dict, nav: list, road: dict, readme_md: str, fluxo: dict, figura: Callable | None = carregar_figura) -> str:
    """A aba de visão de uma fase: a pergunta que ela responde, o que é e o estado, o caminho em passos, o que a fase mostrou (figura, como ler e leitura, do
    README), os tópicos, as corridas e, recolhido, o estado completo como está no roadmap."""
    grupos = dict(nav)
    nav_ids = {sid for _, abas in nav for sid, _, _ in abas}
    linha = linha_do_roadmap(road, fase)
    classe = linha.classe if linha else "outro"
    pergunta, estado_curto = tabela_do_readme(readme_md).get(fase["readme"], ("", ""))
    abas = grupos.get(fase["grupo"], [])[1:]
    corridas = corridas_da_fase(road, fase["grupo"])
    feitas = sum(c.classe == "feita" for c in corridas)
    conta = " e ".join(x for x in (f'{len(abas)} tópico{"" if len(abas) == 1 else "s"}' if abas else "",
                                   f'{len(corridas)} corrida{"" if len(corridas) == 1 else "s"} no roadmap ({feitas} feita{"" if feitas == 1 else "s"})' if corridas else "") if x)
    if fase["passos"] == "agente":
        caminho = fluxo_do_agente(fluxo, nav_ids)
    else:
        passos = _passos(fase, fluxo)
        caminho = (cadeia(passos, nav_ids) + legenda_da_cadeia(sorted({p[0] for p in passos}))
                   + '<p class="como-ler"><strong>Como ler:</strong> siga os passos na ordem dos números. A cor do alto de cada caixa diz quem faz o passo: o código, o modelo '
                   'de linguagem ou as pessoas do grupo. O atalho de cada caixa abre a aba em que o passo é medido.</p>')
    achados = [a for a in descobertas_do_readme(readme_md) if DESCOBERTAS.get(a["pergunta"], ("", ""))[0] == fase["grupo"]]
    bloco_achados = ('<h2>O que a fase mostrou</h2><p>Cada figura responde a uma pergunta. O número exato de cada uma está nas abas da fase.</p>'
                     + "".join(_achado(a, figura, nav_ids) for a in achados)) if achados else ""
    topicos = "".join(f'<a class="topico" href="#{sid}" data-ir="{sid}|"><b>{_esc(nome)}</b><span>{_esc(desc)}</span><em>Abrir</em></a>' for sid, nome, desc in abas)
    bloco_topicos = (f'<h2>Tópicos desta fase</h2><p>Cada tópico é uma aba, com a pergunta, a resposta, os gráficos e, recolhidos, os números em que eles se baseiam.</p>'
                     f'<div class="topicos-fase">{topicos}</div>') if abas else ""
    linhas_c = "".join(f'<li><span class="numero">{_esc(c.numero)}</span><a href="#roadmap" data-ir="roadmap|corrida-{_esc(c.numero)}">{pt.inline(_nome_curto_da_corrida(c.nome))}</a>'
                       f'{_chip(c.classe, ROTULO_CORRIDA.get(c.classe, "Sem estado"))}</li>' for c in corridas)
    bloco_corridas = (f'<h2>Corridas desta fase</h2><p>Cada corrida é uma execução medida. O nome abre o cartão dela no Roadmap, com o comando e o que ela fecha.</p>'
                      f'<ul class="linhas-corrida">{linhas_c}</ul>') if corridas else ""
    tcc = f' A aba segue a seção {fase["tcc"]} do documento do TCC.' if fase["tcc"] else ""
    detalhes = (f'<details><summary>Mais detalhes: o estado completo da fase, como está no roadmap</summary><p>{pt.inline(linha.estado)}</p></details>' if linha else "")
    return f'''<section id="{fase["sid"]}" hidden>
<h1>{_esc(fase["titulo"])}</h1>
<p class="pergunta-fase">{pt.inline(pergunta)}</p>
<p class="nota">É a pergunta que esta fase responde.{_esc(tcc)}</p>
<div class="resumo-fase"><div><span class="rotulo">O que é</span><p>{pt.inline(linha.o_que_e) if linha else ""}</p></div>
<div><span class="rotulo">Estado</span><p>{_chip(classe)} {pt.inline(_estado_que_acrescenta(estado_curto, classe))}</p>{f'<p class="nota">{_esc(conta)}</p>' if conta else ""}</div></div>
<h2>O caminho da fase</h2>
{caminho}
{bloco_achados}
{bloco_topicos}
{bloco_corridas}
{detalhes}
</section>'''


def secoes_das_fases(nav: list, road: dict, readme_md: str | None = None, fluxo: dict | None = None, figura: Callable | None = carregar_figura) -> str:
    readme_md = README.read_text(encoding="utf-8") if readme_md is None else readme_md
    fluxo = ler_fluxo() if fluxo is None else fluxo
    return "\n".join(secao_fase(f, nav, road, readme_md, fluxo, figura) for f in FASES)


def secao_inicio(dados: dict, pend: list, road: dict, nav: list, readme_md: str | None = None, fluxo: dict | None = None) -> str:
    """A aba Início: o que o projeto é, o problema, como o agente trabalha, o caminho das fases, onde o projeto está, o que já se descobriu, o que ainda não dá
    para afirmar, o que espera decisão, as próximas corridas e o mapa do painel."""
    readme_md = README.read_text(encoding="utf-8") if readme_md is None else readme_md
    fluxo = ler_fluxo() if fluxo is None else fluxo
    nav_ids = {sid for _, abas in nav for sid, _, _ in abas}
    perguntas = tabela_do_readme(readme_md)
    fichas = [f for b in pend for f in b.fichas]
    abertas = [f for f in fichas if f.aberta]
    a_decidir = [f for f in abertas if f.depende_do_eric]
    corr = road["corridas"]
    por_rodar = [c for c in corr if c.classe in ("rodando", "pendente", "aguarda")]
    n_feitas = sum(c.classe == "feita" for c in corr)
    atual = next((f for f in FASES if (linha_do_roadmap(road, f) and linha_do_roadmap(road, f).classe == "andamento")), None)
    rotulo_fase = "Fase atual"
    if atual is None:
        atual = next((f for f in FASES if (linha_do_roadmap(road, f) and linha_do_roadmap(road, f).classe == "nao_iniciada")), None)
        rotulo_fase = "Próxima fase"
    v = dados["vencedor"]
    itens = [(rotulo_fase, atual["grupo"] if atual else "Sem fase aberta", atual["curto"] if atual else ""),
             ("Modelo escolhido", v["modelo"], f'biblioteca L{v["biblioteca_epoca"]} (decisão 52)'),
             ("Fichas abertas", str(len(abertas)), f"{len(a_decidir)} esperam decisão"),
             ("Corridas no roadmap", f"{n_feitas} feitas", f"{len(por_rodar)} por rodar"),
             ("Estado registrado em", road["data"] or "sem data", "roadmap.md e pendencias.md")]
    kp = '<div class="kpis">' + "".join(f"<div class='kpi'><span>{_esc(t)}</span><b>{_esc(b)}</b><small>{_esc(s)}</small></div>" for t, b, s in itens) + "</div>"
    pars = problema_do_readme(readme_md)
    titulos = ["Quando a API muda sem avisar", "Quando só a tela muda", "O que o agente faz"]
    problema = "".join(f"<div><h3>{_esc(t)}</h3><p>{pt.inline(p)}</p></div>" for t, p in zip(titulos, pars))
    ideia = ideia_central_do_readme(readme_md)
    cartoes = []
    for a in descobertas_do_readme(readme_md):
        grupo, alvo = DESCOBERTAS.get(a["pergunta"], ("", ""))
        fase = fase_do_grupo(grupo)
        resposta = a["mostra"][0] if a["mostra"] else ""
        destino = fase["sid"] if fase else alvo
        atalho = f'<a href="#{destino}" data-ir="{destino}|">Ver a figura e a leitura</a>' if destino in nav_ids else ""
        cartoes.append(f'<article class="descoberta"><span class="fase-de">{_esc(grupo)}</span><h3>{pt.inline(a["pergunta"])}</h3><p>{pt.inline(resposta)}</p>{atalho}</article>')
    limites = "".join(f"<li>{pt.inline(l)}</li>" for l in limites_do_readme(readme_md))
    if a_decidir:
        lista = "".join(f'<li><a href="#{f.id_html}" data-ir="pendencias|{f.id_html}"><span class="numero">{f.numero}</span> {pt.inline(f.titulo)}</a>'
                        f'<br><span class="nota">Recomendação: {pt.inline(f.campos.get("Recomendação", "sem recomendação"))}</span></li>' for f in a_decidir)
        bloco_decisao = ('<p>Cada item abre a ficha completa na aba Pendências: o que é, por que importa, as opções e a recomendação.</p>'
                         f'<ol class="lista-eric">{lista}</ol>')
    else:
        bloco_decisao = '<p>Nenhuma decisão em aberto: todas as fichas estão fechadas (aba Pendências).</p>'
    if por_rodar:
        linhas_c = "".join(f'<li><span class="numero">{_esc(c.numero)}</span><a href="#roadmap" data-ir="roadmap|corrida-{_esc(c.numero)}">{pt.inline(_nome_curto_da_corrida(c.nome))}</a>'
                           f'{_chip(c.classe, ROTULO_CORRIDA.get(c.classe, "Sem estado"))}</li>' for c in por_rodar)
        bloco_corridas = f'<ul class="linhas-corrida">{linhas_c}</ul><p class="nota">O nome abre o cartão da corrida no Roadmap, com o comando, o pré-requisito e o que ela fecha.</p>'
    else:
        bloco_corridas = '<p>Nenhuma corrida por rodar: todas as do roadmap estão feitas.</p>'
    mapa = "".join(
        f'<div><h3>{_esc(grupo)}</h3><ul>' + "".join(f'<li><a href="#{sid}" data-ir="{sid}|">{_esc(nome)}</a>: {_esc(desc)}</li>' for sid, nome, desc in abas if sid != "inicio") + "</ul></div>"
        for grupo, abas in nav)
    return f'''<section id="inicio">
<h1>O projeto em uma página</h1>
<p class="lead">{pt.inline(apresentacao_do_readme(readme_md))}</p>
{kp}
<h2>O problema</h2>
<div class="problema">{problema}</div>
<h2>Como o agente trabalha</h2>
{fluxo_do_agente(fluxo, nav_ids)}
{f'<p class="ideia-central"><strong>A ideia central:</strong> {pt.inline(ideia)}</p>' if ideia else ""}
<h2>O caminho do projeto</h2>
<p>O trabalho foi feito em fases, e cada fase responde a uma pergunta. A cor do alto de cada cartão é o estado da fase.</p>
{caminho_do_projeto(road, perguntas)}
<h2>O que já descobrimos</h2>
<p>Cada cartão é uma pergunta do projeto com a resposta em poucas linhas. A figura, a explicação de como ler e os números estão na visão da fase em que a pergunta foi medida.</p>
<div class="descobertas">{"".join(cartoes)}</div>
<h2>O que ainda não dá para afirmar</h2>
<ul class="limites">{limites}</ul>
<h2>Os dois sistemas de teste</h2>
{cobaias_do_readme(readme_md)}
<h2>O que espera decisão</h2>
{bloco_decisao}
<h2>Próximas corridas</h2>
{bloco_corridas}
<details><summary>Mapa do painel: todas as abas, por fase</summary><div class="mapa-painel">{mapa}</div></details>
</section>'''


CSS = r"""
/* painel por fase (11/11/2026): navegação lateral com cada fase como cabeçalho e as abas dela recuadas; faixa de sub-abas no alto de cada aba de fase */
.lateral nav{gap:2px}.nav-grupo{display:flex;flex-direction:column;gap:1px;margin-bottom:8px}
.nav-fase{border-top:1px solid var(--linha);padding-top:3px;margin:0}
nav .fase-topo{display:grid;grid-template-columns:auto minmax(0,1fr) auto;grid-template-areas:"b rot q" "b nome q";column-gap:8px;align-items:center;padding:6px 8px 6px 10px;color:var(--ink)}
.fase-topo .bolinha{grid-area:b;width:11px;height:11px;border-radius:50%;background:transparent;border:2px solid var(--ink2)}
.nav-fase.concluida .bolinha{background:var(--bom);border-color:var(--bom)}.nav-fase.andamento .bolinha{background:var(--meio);border-color:var(--meio)}
.fase-topo .rot{grid-area:rot;font:600 13px/1.2 var(--fb)}.fase-topo .nome{grid-area:nome;font:400 12px/1.25 var(--fb);color:var(--ink2)}
.fase-topo .qtd{grid-area:q;font:500 11px var(--fm);color:var(--ink2);border:1px solid var(--linha);border-radius:999px;padding:0 6px}.fase-topo .qtd:empty{display:none}
.nav-sub{display:none;flex-direction:column;gap:1px;margin:2px 0 6px 15px;padding-left:8px;border-left:2px solid var(--linha)}
.nav-fase.aberto .nav-sub{display:flex}.nav-fase.aberto .fase-topo .qtd{background:var(--acento2);border-color:var(--acento);color:var(--acento)}
.nav-sub button{font-size:12.5px;padding:3px 8px}
.nav-sub button[aria-selected=true]{border-color:transparent;border-left:3px solid var(--acento);border-radius:0 6px 6px 0;font-weight:600}
nav.trilho{display:flex;flex-direction:column;gap:8px;margin:0 0 18px;padding:10px 12px;background:var(--bg2);border:1px solid var(--linha);border-left:5px solid var(--ink2);border-radius:10px}
nav.trilho.concluida{border-left-color:var(--bom)}nav.trilho.andamento{border-left-color:var(--meio)}
.trilho-fase{display:flex;flex-wrap:wrap;align-items:center;gap:8px;font-size:13px;color:var(--ink2)}.trilho-fase b{color:var(--ink);font:600 15px var(--fd)}
.trilho-abas{display:flex;flex-wrap:wrap;gap:6px}
nav.trilho button{display:inline-block;width:auto;border:1px solid var(--linha);border-radius:999px;padding:3px 11px;font-size:12.5px;background:var(--bg)}
nav.trilho button.aqui,nav.trilho button[aria-selected=true]{background:var(--acento);border-color:var(--acento);color:var(--bg2);font-weight:600}
/* cartões do roadmap em linha: fase e estado, a pergunta e o que é, e o "Saiba mais" */
.linhas-fase{display:flex;flex-direction:column;gap:10px;margin:14px 0}
.linha-fase{display:grid;grid-template-columns:minmax(150px,200px) minmax(0,1fr) auto;gap:6px 20px;align-items:center;background:var(--bg2);border:1px solid var(--linha);border-left:6px solid var(--ink2);border-radius:10px;padding:12px 16px}
.linha-fase.concluida{border-left-color:var(--bom)}.linha-fase.andamento{border-left-color:var(--meio)}.linha-fase.nao_iniciada{border-left-color:var(--linha)}
.lf-id b{display:block;font:600 17px/1.2 var(--fd)}.lf-id small{display:block;color:var(--ink2);font-size:12.5px;margin:2px 0 6px}
.lf-corpo p{margin:3px 0;max-width:none;font-size:14px}.rotulo{display:block;font:600 11px var(--fb);text-transform:uppercase;letter-spacing:.05em;color:var(--ink2)}
.lf-corpo details{margin:6px 0 0}.lf-acao{display:flex;flex-direction:column;align-items:flex-end;gap:4px;white-space:nowrap}.lf-acao small{color:var(--ink2);font-size:12px}
.saiba-mais{display:inline-block;border:1px solid var(--acento);color:var(--acento);background:var(--acento2);font:600 13px var(--fb);padding:6px 14px;border-radius:999px;text-decoration:none}
.saiba-mais:hover{background:var(--acento);color:var(--bg2)}
@media (max-width:760px){.linha-fase{grid-template-columns:minmax(0,1fr)}.lf-acao{flex-direction:row;align-items:center}}
.grupo-corridas>summary .nota{font-weight:400;margin-left:8px}.secao-roadmap{margin:6px 0}
/* no Roadmap cada corrida ocupa a largura inteira, com os quatro fatos lado a lado: o cartão fica baixo em vez de estreito e alto */
.grupo-corridas .corridas{grid-template-columns:minmax(0,1fr);gap:10px;margin-top:12px}.grupo-corridas .corrida{padding:12px 16px}
.grupo-corridas .fatos2{grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));gap:2px 22px}.grupo-corridas .fatos2 div{grid-template-columns:120px minmax(0,1fr)}
.cobaias .rotulo{margin-top:6px}
/* a visão de cada fase: a pergunta, o caminho em passos, os tópicos e as corridas */
.pergunta-fase{font:600 21px/1.3 var(--fd);margin:4px 0 0;max-width:none}
.resumo-fase{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(280px,100%),1fr));gap:12px;margin:14px 0}
.resumo-fase>div{background:var(--bg2);border:1px solid var(--linha);border-radius:10px;padding:12px 16px}.resumo-fase p{margin:4px 0 0;max-width:none}
.cadeia{list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(230px,100%),1fr));gap:16px 24px;padding:0!important;margin:14px 0;counter-reset:passo}
.cadeia li{position:relative;counter-increment:passo;background:var(--bg2);border:1px solid var(--linha);border-top:5px solid var(--ink2);border-radius:10px;padding:10px 12px 12px}
.cadeia li::before{content:counter(passo);display:inline-block;font:600 12px var(--fm);color:var(--bg2);background:var(--ink2);border-radius:999px;min-width:22px;text-align:center;padding:1px 6px;margin-bottom:6px}
.cadeia li:not(:last-child)::after{content:"";position:absolute;right:-17px;top:50%;width:9px;height:9px;border-top:2px solid var(--ink2);border-right:2px solid var(--ink2);transform:translateY(-50%) rotate(45deg)}
.cadeia li.codigo{border-top-color:var(--s1)}.cadeia li.codigo::before{background:var(--s1)}
.cadeia li.modelo{border-top-color:var(--s2);background:color-mix(in srgb,var(--s2) 9%,var(--bg2))}.cadeia li.modelo::before{background:var(--s2)}
.cadeia b{display:block;font:600 14.5px/1.25 var(--fd);margin-bottom:4px}.cadeia p{font-size:13px;margin:0;max-width:none}
.cadeia a,.saidas a,.trilha-caixa a{display:inline-block;margin-top:6px;font:600 12px var(--fb);color:var(--acento);text-decoration:none}
@media (max-width:520px){.cadeia li:not(:last-child)::after{right:50%;top:auto;bottom:-14px;transform:translateX(50%) rotate(135deg)}}
.legenda-cadeia{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:12.5px;color:var(--ink2);margin:6px 0 0;max-width:none}
.legenda-cadeia i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:6px;vertical-align:-1px;background:var(--ink2)}
.legenda-cadeia i.codigo{background:var(--s1)}.legenda-cadeia i.modelo{background:var(--s2)}.legenda-cadeia i.saida{background:transparent;border:1px dashed var(--ink2)}
.liga{font:600 12px var(--fb);text-transform:uppercase;letter-spacing:.05em;color:var(--ink2);margin:14px 0 0}
.saidas{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(230px,100%),1fr));gap:12px;margin:8px 0}
.saidas>div{border:1px dashed var(--ink2);border-radius:10px;padding:10px 12px;background:var(--bg2)}.saidas b,.trilha-caixa b{display:block;font:600 14.5px var(--fd)}
.saidas p,.trilha-caixa p{margin:4px 0 0;font-size:13px;max-width:none}.trilha-caixa{border:1px solid var(--ink2);border-radius:10px;padding:10px 14px;margin:10px 0;background:var(--bg2)}
.achado{background:var(--bg2);border:1px solid var(--linha);border-radius:10px;padding:14px 18px;margin:12px 0}.achado h3{margin:0 0 6px}.achado figure{border:0;padding:0;margin:10px 0}
.topicos-fase{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(260px,100%),1fr));gap:12px;margin:14px 0}
.topico{display:flex;flex-direction:column;gap:6px;background:var(--bg2);border:1px solid var(--linha);border-radius:10px;padding:12px 14px;text-decoration:none;color:inherit}
.topico:hover{border-color:var(--acento);box-shadow:var(--sombra)}.topico b{font:600 15px/1.25 var(--fd)}.topico span{font-size:13px;color:var(--ink2)}
.topico em{margin-top:auto;font:600 12.5px var(--fb);font-style:normal;color:var(--acento)}
.linhas-corrida{list-style:none;padding:0!important;margin:10px 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(340px,100%),1fr));gap:2px 18px}
.linhas-corrida li{display:flex;align-items:center;gap:8px;border-bottom:1px dotted var(--linha);padding:5px 0;font-size:13.5px}
.linhas-corrida a{color:inherit;text-decoration:none;flex:1 1 auto;min-width:0}.linhas-corrida a:hover{color:var(--acento)}
/* o Início: o problema, o caminho do projeto e as descobertas */
.problema{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(280px,100%),1fr));gap:12px;margin:14px 0}
.problema>div{background:var(--bg2);border:1px solid var(--linha);border-radius:10px;padding:14px 16px}.problema h3{margin:0 0 6px}.problema p{margin:0;max-width:none;font-size:14px}
.ideia-central{border-left:4px solid var(--acento);background:var(--acento2);border-radius:0 10px 10px 0;padding:10px 16px;margin:12px 0;max-width:none}
.barra-fases{display:flex;gap:3px;height:10px;margin:12px 0 4px;max-width:560px}.barra-fases i{display:block;border-radius:999px;background:var(--linha)}
.barra-fases i.concluida{background:var(--bom)}.barra-fases i.andamento{background:var(--meio)}
.caminho{list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(170px,100%),1fr));gap:10px;padding:0!important;margin:12px 0}
.caminho a{display:block;height:100%;text-decoration:none;color:inherit;background:var(--bg2);border:1px solid var(--linha);border-top:5px solid var(--linha);border-radius:10px;padding:10px 12px}
.caminho li.concluida a{border-top-color:var(--bom)}.caminho li.andamento a{border-top-color:var(--meio);box-shadow:0 0 0 2px color-mix(in srgb,var(--meio) 30%,transparent)}
.caminho a:hover{border-color:var(--acento)}.caminho b{display:block;font:600 15px/1.2 var(--fd)}
.caminho .estado{display:block;font:600 11px var(--fb);text-transform:uppercase;letter-spacing:.04em;color:var(--ink2);margin:2px 0 6px}
.caminho li.concluida .estado{color:var(--bom)}.caminho li.andamento .estado{color:var(--meio)}.caminho .q{display:block;font-size:12.5px;color:var(--ink2)}
.descobertas{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));gap:12px;margin:14px 0}
.descoberta{background:var(--bg2);border:1px solid var(--linha);border-radius:10px;padding:14px 16px;display:flex;flex-direction:column;gap:6px}
.descoberta h3{margin:0;font-size:16px}.descoberta p{margin:0;font-size:13.5px;max-width:none}
.descoberta .fase-de{font:600 11px var(--fb);text-transform:uppercase;letter-spacing:.05em;color:var(--ink2)}
.descoberta a{margin-top:auto;font:600 13px var(--fb);color:var(--acento);text-decoration:none}
.limites li{margin:4px 0;max-width:86ch}
"""

# O script entra antes do script base do painel: `mostrar(id)` chama `window.aoMostrar(id)` ao trocar de aba, e é aqui que a fase da aba atual abre na lateral.
JS = r"""
window.aoMostrar = function(id){
  const b = document.querySelector('.lateral nav button[data-alvo="' + id + '"]');
  document.querySelectorAll('.lateral .nav-fase').forEach(g => { const aberto = !!b && g.contains(b); g.classList.toggle('aberto', aberto);
    const t = g.querySelector('.fase-topo'); if(t) t.setAttribute('aria-expanded', String(aberto)); });
  if(b && b.scrollIntoView) b.scrollIntoView({block:'nearest'});
};
document.addEventListener('click', e => { const a = e.target.closest ? e.target.closest('[data-ir]') : null; if(!a) return;
  let el = document.getElementById((a.dataset.ir.split('|')[1] || '') || '-');
  while(el){ if(el.tagName === 'DETAILS') el.open = true; el = el.parentElement; } }, true);
"""
