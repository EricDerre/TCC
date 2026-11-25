#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (04/11/2026, Fase 4, pacote P6): o ajudante da sessão cronometrada da linha de base
# manual da Fase 5 (protocolo em Documentacao/memorial/5-metodo-e-ferramental/protocolo-linha-de-base-manual.md), com quatro
# comandos: `ordem` sorteia com semente fixa a ordem dos dez cenários de cada integrante e grava a planilha modelo; `armar`
# restaura o banco, liga a falha do cenário da vez (o modo na CobaiaAPI, ou a quebra do localizador pelos cookies da variante
# PHP do front) e abre para o integrante o mesmo Chromium do agente, mostrando a ficha da falha que a corrida 21 gravou;
# `conferir` roda o roteiro de localizador com o seletor do integrante e diz se ele chegou ao fim sem erro; `desarmar` volta a
# CobaiaAPI ao modo normal. O facilitador chama o cenário pela vez (integrante e posição na ordem), e o nome do cenário, que diz
# o modo de falha, não aparece na tela.
# ! Motivo: a decisão 79 (ficha 36) pede a linha de base por três integrantes, cada um nos dez cenários, numa sessão agendada com
# o protocolo escrito. Para o tempo do integrante ser comparável ao MTTR do agente, a falha tem de ser ligada pelas mesmas funções
# da corrida (executar_fase4.ligar_modo e cenarios_fase4.armar_quebra), no mesmo navegador, e o "corrigido" do localizador tem de
# ser conferido pela mesma reexecução (cenarios_fase4.roteiro_com_seletor e task_success); feito à mão, cada um desses passos
# poderia sair diferente do que o agente teve.
# ! Alteração de IA - Revisar: (16/11/2026, Fase 5, pacote F2) o ajudante passa à versão 2 do protocolo (decisão 131, ficha 73).
# O que entra: o registro da sessão em resultados_alvo/fase5_manual/sessao.jsonl, uma linha por evento com a hora do relógio em
# milésimos (o `armar --vez` grava o início e o fim da janela; o comando novo `entregar` grava o fim do cenário de contrato no
# Enter do facilitador, antes de pedir a causa e o campo, e recusa causa fora das 23; o `conferir --vez --seletor` grava cada
# tentativa, o resultado e os segundos do banco); `treino` (o cenário de contrato `latency` e um exercício de seletor no botão
# "Saiba Mais..." de produtos_api.php, fora dos dez cenários e sem cronômetro); `planilha` (preenche a planilha a partir do
# registro, sem trocar célula preenchida); `perfil` (as três perguntas da seção 4.1 do plano, em participantes.json, sem o nome);
# `falas`, `folha` e `protocolo` (o texto fixo do facilitador e a folha do integrante, com a definição de uma linha das 23
# causas, impressos e colados no protocolo). `ordem` e `desarmar` não mudam; `armar` e `conferir` mostram a mesma tela de antes,
# e o ensaio do facilitador (`--cenario <nome>`) continua sem gravar nada.
# ! Motivo: na versão 1 o facilitador copiava da tela para a planilha a hora de início e de fim de cada cenário: 60 horários
# anotados à mão só do lado das pessoas, enquanto o MTTR do agente sai do relógio da máquina (plano da Fase 5, seção 4.4). Com o
# registro, o tempo das pessoas também não é digitado, e a leitura da Fase 5 (avaliar_fase5.py --manual) confere a planilha
# contra ele. O treino e a definição das causas existem para o primeiro cenário medido não cronometrar a pessoa aprendendo a
# forma da resposta ou adivinhando o que o nome de uma causa quer dizer.
"""Ajudante da sessão da linha de base manual (Fase 5). Na venv do AgenteCore, com RESULTADOS_DIR=resultados_alvo e as cobaias
no ar (`python run.py` na raiz do repositório, em outra janela):

  python linha_de_base_manual.py ordem --gravar
  python linha_de_base_manual.py ensaio                     (o passo a passo do ensaio do facilitador)
  python linha_de_base_manual.py falas                      (o texto fixo do facilitador)
  python linha_de_base_manual.py folha --gravar folha.md    (a folha do integrante, com as 23 causas)
  python linha_de_base_manual.py perfil --integrante 1
  python linha_de_base_manual.py treino contrato --integrante 1
  python linha_de_base_manual.py treino seletor --integrante 1
  python linha_de_base_manual.py armar --vez 1 3
  python linha_de_base_manual.py entregar --vez 1 3         (contrato: Enter no instante da entrega)
  python linha_de_base_manual.py conferir --vez 1 3 --seletor "input[name=search]"
  python linha_de_base_manual.py planilha
  python linha_de_base_manual.py desarmar

`--vez N P` é o cenário na posição P da ordem do integrante N (a planilha diz qual é) e grava no registro da sessão;
`--cenario <id>` serve para o ensaio do facilitador e não grava nada. `conferir` sai 0 quando o roteiro chega ao fim sem erro
com o seletor do integrante (corrigido) e 1 quando não. `--registro <pasta>` troca a pasta do registro (padrão fase5_manual)."""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import os
import random
import re
import sys
import threading
import time
import unicodedata
from pathlib import Path
from urllib.parse import urljoin

import cenarios_fase4 as cen

RAIZ = Path(__file__).resolve().parents[3]
SEMENTE_DA_ORDEM = 20261104
INTEGRANTES = 3
SAIDA_DO_ENSAIO = "fase4_ensaio"
PLANILHA = RAIZ / "Documentacao" / "memorial" / "5-metodo-e-ferramental" / "planilha-linha-de-base-manual.csv"
SEPARADOR = ";"   # o Excel em português abre o CSV separado por ponto e vírgula em colunas
COLUNAS_DA_PLANILHA = ("integrante", "ordem", "cenario", "tipo", "inicio", "fim", "segundos", "descontar_s", "causa", "campo",
                       "seletor", "tentativas", "corrigido", "observacoes")

# ! Alteração de IA - Revisar: (16/11/2026, F2) as constantes da versão 2: onde ficam o registro e o perfil, o limite de 10
# minutos por cenário e o aviso dois minutos antes dele, as nove colunas da planilha que saem do registro, a marca da linha
# anotada à mão, os segundos em que a tela de login do front legado volta sozinha, e o protocolo que recebe os textos gerados.
# ! Motivo: o limite, o aviso e os 30 s da tela de login aparecem na folha do integrante, no texto do facilitador e nas contas do
# registro; escritos uma vez aqui, os três lugares dizem o mesmo número (o teste confere os 30 s contra admin/login.php).
VERSAO_DO_REGISTRO = 2
PASTA_DA_SESSAO = "fase5_manual"
NOME_DO_REGISTRO = "sessao.jsonl"
NOME_DOS_PARTICIPANTES = "participantes.json"
LIMITE_S = 600               # protocolo, seção 6: 10 minutos por cenário
AVISO_FINAL_S = 120          # a fala "Faltam dois minutos." sai quando falta isto para o limite
SEGUNDOS_DA_VOLTA_DO_LOGIN = 30   # <meta http-equiv="refresh" content="30;..."> em CobaiaFront/admin/login.php
COLUNAS_DO_REGISTRO = ("inicio", "fim", "segundos", "descontar_s", "causa", "campo", "seletor", "tentativas", "corrigido")
MARCA_A_MAO = "anotada à mão"
EVENTOS_DA_VEZ = ("inicio", "entrega", "resposta", "tentativa", "fim_do_armar")
PROTOCOLO = RAIZ / "Documentacao" / "memorial" / "5-metodo-e-ferramental" / "protocolo-linha-de-base-manual.md"

# ! Alteração de IA - Revisar: (16/11/2026, F2) o treino, fora dos dez cenários: o cenário de contrato é o modo `latency` da
# CobaiaAPI (a resposta chega certa, com atraso), que saiu do catálogo pela troca da ficha 36, e o exercício de seletor é achar
# o botão "Saiba Mais..." do primeiro produto em produtos_api.php, página que não está nos quatro roteiros de localizador.
# ! Motivo: o plano (seção 4.3) pede um treino sem cronômetro antes do primeiro cenário medido, com material que não ensine a
# resposta de nenhum dos dez; a causa do treino (`tempo_de_resposta_excedido`) não é a resposta de nenhum deles.
TREINO_DE_CONTRATO = {"id": "treino-contrato", "cenario": "api-catalogo", "modo": cen.TROCA_DA_FICHA_36["sai"], "campo": None,
                      "causa": next(causa for causa, modo in cen.MODO_POR_CAUSA.items() if modo == cen.TROCA_DA_FICHA_36["sai"])}
TREINO_DE_SELETOR = {"id": "treino-seletor", "cenario": "api-catalogo", "pagina": cen.cenario("api-catalogo")["pagina"],
                     "alvo": cen.cenario("api-catalogo")["alvo"], "referencia": cen.GRID}

# ! Alteração de IA - Revisar: (16/11/2026, F2) a definição de uma linha de cada uma das 23 causas, na ordem da lista fechada
# (taxonomia.CAUSAS_RAIZ), que a folha do integrante traz.
# ! Motivo: a decisão 131 pede a explicação de uma linha de cada causa, para o tempo não medir a pessoa adivinhando o que o nome
# quer dizer. O plano dizia que ela viria do Apêndice A do documento do TCC, mas o Apêndice A só traz os 23 nomes e a descrição
# das seis classes; as linhas abaixo foram escritas neste pacote, e o Eric as aceitou como estão em 16/11/2026 (ficha 76,
# decisão 134). Cada uma diz o que o nome significa, sem citar campo, página ou a forma como a falha é armada nos cenários, e
# os exemplos são de fora das cobaias. Depois da primeira sessão com integrante o texto não muda: os três recebem a mesma folha.
DEFINICAO_DAS_CAUSAS = {
    "corpo_nao_e_json": "a resposta chega, mas o corpo não é JSON: vem uma página HTML ou um texto solto",
    "corpo_vazio": "a resposta chega sem nada no corpo",
    "resposta_truncada": "o corpo começa como JSON e é cortado antes do fim",
    "codificacao_incorreta": "as letras acentuadas chegam trocadas por outros símbolos",
    "campo_ausente": "um campo que o contrato exige não vem na resposta",
    "campo_renomeado": "o valor vem, mas num campo com um nome diferente do que o contrato diz",
    "estrutura_aninhada_divergente": "o campo vem dentro de outro objeto, ou num nível diferente do que o contrato diz",
    "colecao_no_lugar_de_objeto": "vem uma lista onde o contrato pede um objeto só, ou o inverso",
    "tipo_divergente": "o campo vem com um tipo diferente do que o contrato declara",
    "valor_fora_do_dominio": "o tipo está certo, mas o valor não é um dos permitidos, como uma opção que não existe",
    "formato_de_data_divergente": "a data vem escrita num formato diferente do que o contrato pede",
    "nulo_inesperado": "um campo obrigatório vem com o valor nulo",
    "escala_ou_unidade_errada": "o número vem em outra escala ou unidade, como gramas no lugar de quilos",
    "chave_de_juncao_errada": "o registro vem ligado ao item errado de outra tabela",
    "contagem_inconsistente": "a quantidade de itens que vem não é a que deveria vir",
    "tempo_de_resposta_excedido": "a resposta chega certa, mas demora mais do que o tempo aceito",
    "limite_de_requisicoes": "o servidor recusa a chamada por excesso de requisições (status 429)",
    "dado_desatualizado": "a resposta traz um dado antigo, que já mudou no banco",
    "registro_duplicado": "o mesmo registro vem mais de uma vez na resposta",
    "erro_interno_do_servidor": "o servidor falha ao atender a chamada e responde com erro (status 500)",
    "recurso_inexistente": "o endereço ou o registro pedido não existe (status 404)",
    "localizador_quebrado": "a página mudou e o seletor que o teste usa não acha mais o elemento",
    "estado_da_tela_divergente": "a resposta da API está certa, mas a tela mostra outra coisa",
}

# ! Alteração de IA - Revisar: (16/11/2026, F2) as três perguntas de perfil da seção 4.1 do plano, a anotação do facilitador sobre
# quem escreveu ou conhece o código das cobaias, e as falas fixas: as três do plano (seção 4.3) e as quatro que só repetem o que
# a ferramenta mostrou (causa fora da lista, seletor que não passou, seletor que passou, tempo esgotado).
# ! Motivo: o perfil explica o tempo de cada um sem guardar o nome (o repositório é público), e o plano manda declarar quando o
# autor do site legado participa, porque ele conhece o HTML das páginas dos cenários de localizador. As falas fixas existem para o
# facilitador não dar dica: o que ele disser além delas vai para as observações. As quatro falas da ferramenta não estavam no
# plano; sem elas o facilitador teria de improvisar a frase toda vez que o `entregar` recusa uma causa ou o `conferir` responde.
PERGUNTAS_DE_PERFIL = {
    "pratica": "Quanto tempo de prática você tem com teste de software ou com programação para a web?",
    "ja_usou_as_ferramentas_do_desenvolvedor": "Você já usou as ferramentas do desenvolvedor do navegador (a tecla F12)?",
    "ja_leu_a_lista_dos_cenarios": (f"Você já leu a lista dos {len(cen.CENARIOS_DO_ENSAIO)} cenários ou as causas esperadas no painel, no README, "
                                    "no documento do TCC ou no repositório?"),
}
ANOTACAO_DO_FACILITADOR = {
    "conhece_o_codigo_das_cobaias": ("Anotação do facilitador, não é pergunta ao integrante: ele escreveu ou conhece o código das aplicações "
                                     "da sessão (o site legado ou a CobaiaAPI)?"),
}
CAMPOS_DO_PERFIL = (*PERGUNTAS_DE_PERFIL, *ANOTACAO_DO_FACILITADOR, "o_que_conhece")
FALAS_DO_PLANO = ("O tempo está correndo.", "Faltam dois minutos.", "Pode entregar quando quiser.")
FALAS_DA_FERRAMENTA = (f"A causa precisa ser uma das {len(DEFINICAO_DAS_CAUSAS)} da lista, escrita como está na folha.", "Não passou. O tempo segue.",
                       "Passou. O tempo parou.", "Tempo esgotado.")

# ! Alteração de IA - Revisar: (16/11/2026, F2) a pasta de teste do ensaio do facilitador e, para cada cenário de localizador, um
# seletor que conserta o roteiro: o seletor que o roteiro usava antes da quebra (`seletor_original`), menos na busca, em que a
# quebra troca justamente o id que o roteiro usava e o que continua valendo é o atributo `name` do campo.
# ! Motivo: no ensaio o facilitador precisa ver o `conferir` dizer "CORRIGIDO" em cada um dos quatro, e para isso precisa de um
# seletor que funcione com a quebra armada; os quatro foram conferidos na fumaça com as cobaias reais. O ensaio dos comandos que
# gravam vai para outra pasta, para o registro das três sessões não receber linha de ensaio.
# ! Alteração de IA - Revisar: (16/11/2026, decisão 135) o que o integrante pode e não pode fazer saiu do texto da folha para duas
# constantes, e entraram os minutos da abertura, do treino e do fecho da sessão (plano da Fase 5, seção 4.3).
# ! Motivo: o tutorial do integrante (tutorial_do_integrante.py) repete as regras da folha e diz como é o dia; com as frases e os
# minutos escritos uma vez, a folha e o tutorial não podem dizer coisas diferentes (o teste confere os minutos contra o plano).
O_QUE_PODE = ("navegar, inspecionar a página, ver as chamadas à API na aba de rede, abrir a API pelo navegador e consultar a documentação de "
              "seletores CSS e do Playwright")
O_QUE_NAO_PODE = ("abrir o código das aplicações, o código do agente ou o repositório, usar assistente de IA, ver a planilha do facilitador nem "
                  "falar com outro integrante sobre os cenários")
MINUTOS_DA_SESSAO = {"abertura": 10, "treino": 15, "fecho": 5}
# ! Alteração de IA - Revisar: (16/11/2026, decisão 136) o que pode e o que não pode na sessão feita pela página publicada, e os
# quatro avisos que a página mostra (as mesmas frases das falas do facilitador).
# ! Motivo: na página não há navegador do cenário nem facilitador ao lado: a pessoa lê o material capturado e a página é quem
# avisa do tempo e do resultado do seletor. O tutorial e a página usam estas constantes para dizerem a mesma coisa.
PODE_NA_PAGINA = "ler o material do cenário quantas vezes quiser, usar a caixa Testar seletor e consultar a documentação de seletores CSS"
NAO_PODE_NA_PAGINA = ("abrir o repositório, o painel, o README ou o documento do TCC do projeto, usar assistente de IA nem falar com outro integrante "
                      "sobre os cenários")
AVISOS_DA_PAGINA = {"dois_minutos": FALAS_DO_PLANO[1], "esgotado": FALAS_DA_FERRAMENTA[3], "nao_passou": FALAS_DA_FERRAMENTA[1],
                    "passou": FALAS_DA_FERRAMENTA[2]}
# ! Alteração de IA - Revisar: (17/11/2026, ficha 77, decisão 137) o aviso do integrante na sessão pela página: a pergunta que a
# página faz no fim de cada cenário, o que conta e o que não conta como motivo, o tamanho máximo do texto, o nome do evento no
# registro, o rótulo que vai para as observações da planilha e a marca da linha anulada. `texto_da_ocorrencia` limpa o texto
# antes de ele ir para o registro, e `observacao_da_ocorrencia` monta o que vai para a planilha.
# ! Motivo: a regra L14 do plano só anula a medida de um cenário por falha do protocolo anotada na hora (equipamento que travou,
# interrupção de fora), e quem anotava era o facilitador, que na sessão pela página não está ao lado. Quem escreve na hora passa
# a ser a própria pessoa; a decisão de anular continua do facilitador, pelo motivo escrito, e a planilha a recebe com `ANULADA`
# no começo das observações, que é o que a leitura (`avaliar_fase5.MARCA_ANULADA`) procura. O ponto e vírgula sai do texto
# porque é o separador da planilha; o rótulo na frente impede que um aviso que comece com a palavra anule a linha sozinho.
MARCA_ANULADA = "ANULADA"
EVENTO_DA_OCORRENCIA = "ocorrencia"
LIMITE_DA_OCORRENCIA = 300
ROTULO_DA_OCORRENCIA = "aviso do integrante"
PERGUNTA_DA_OCORRENCIA = "Alguma coisa de fora atrapalhou este cenário?"
O_QUE_CONTA_COMO_OCORRENCIA = "o computador ou o navegador travou, a página não carregou, alguém interrompeu você"
O_QUE_NAO_CONTA_COMO_OCORRENCIA = "cenário difícil, dúvida sobre a resposta ou tempo curto"


def texto_da_ocorrencia(texto) -> str | None:
    """O aviso como vai para o registro: quebras e espaços seguidos viram um espaço, o ponto e vírgula vira vírgula e o tamanho
    fica no limite da página; None se não é texto ou se ficou vazio."""
    if not isinstance(texto, str):
        return None
    return " ".join(texto.replace(SEPARADOR, ",").split())[:LIMITE_DA_OCORRENCIA].strip() or None


def observacao_da_ocorrencia(texto: str, anulada: bool) -> str:
    """O que vai para as observações da linha da planilha: o aviso, com a marca da linha anulada no começo quando o facilitador anulou."""
    return f"{MARCA_ANULADA}: {ROTULO_DA_OCORRENCIA}: {texto}" if anulada else f"{ROTULO_DA_OCORRENCIA} (linha mantida): {texto}"


PASTA_DO_ENSAIO = "fase5_manual_ensaio"
SELETOR_DO_ENSAIO ={c["id"]: "input[name=buscar]" if c["cenario"] == "front-busca" else cen.quebra(c["cenario"], c["modo"])["seletor_original"]
                     for c in cen.CENARIOS_DE_LOCALIZADOR}


def cenario_do_ensaio(cenario_id: str) -> dict:
    c = next((x for x in cen.CENARIOS_DO_ENSAIO if x["id"] == cenario_id), None)
    if c is None:
        raise ValueError(f"{cenario_id!r} não é um dos dez cenários do ensaio: use um de {[x['id'] for x in cen.CENARIOS_DO_ENSAIO]}")
    return c


def roteiro_do_integrante(cenario_id: str, seletor: str | None = None) -> tuple[dict, dict]:
    """O roteiro do cenário de localizador com o seletor do integrante no lugar do quebrado (sem seletor, o roteiro do agente,
    com o localizador quebrado) e a quebra do cenário."""
    c = cenario_do_ensaio(cenario_id)
    if c["tipo"] != "localizador":
        raise ValueError(f"{cenario_id!r} é de contrato: só os cenários de localizador têm seletor para conferir")
    q = cen.quebra(c["cenario"], c["modo"])
    base = cen.cenario_com_localizador(cen.cenario(c["cenario"]), q)
    return (cen.roteiro_com_seletor(base, q, seletor) if seletor else base), q


def ordem_dos_integrantes(integrantes: int = INTEGRANTES, semente: int = SEMENTE_DA_ORDEM) -> dict[int, list[str]]:
    """A ordem dos dez cenários de cada integrante, sorteada com a semente mais o número do integrante: o que um integrante
    aprende num cenário se espalha entre os cenários, e a mesma semente dá sempre a mesma ordem."""
    ordens = {}
    for n in range(1, integrantes + 1):
        ids = [c["id"] for c in cen.CENARIOS_DO_ENSAIO]
        random.Random(semente + n).shuffle(ids)
        ordens[n] = ids
    return ordens


def cenario_da_vez(integrante: int, posicao: int, semente: int = SEMENTE_DA_ORDEM) -> str:
    ordens = ordem_dos_integrantes(max(INTEGRANTES, integrante), semente)
    if integrante < 1 or not 1 <= posicao <= len(ordens[integrante]):
        raise ValueError(f"vez fora da planilha: integrante {integrante}, posição {posicao}")
    return ordens[integrante][posicao - 1]


def planilha_modelo(ordens: dict[int, list[str]]) -> str:
    """A planilha da sessão: uma linha por integrante e cenário, na ordem sorteada, com as colunas da medição em branco."""
    tipos = {c["id"]: c["tipo"] for c in cen.CENARIOS_DO_ENSAIO}
    saida = io.StringIO()
    w = csv.writer(saida, delimiter=SEPARADOR, lineterminator="\n")
    w.writerow(COLUNAS_DA_PLANILHA)
    for n, ids in sorted(ordens.items()):
        for i, cid in enumerate(ids, 1):
            w.writerow([n, i, cid, tipos[cid]] + [""] * (len(COLUNAS_DA_PLANILHA) - 4))
    return saida.getvalue()


def ficha_da_falha(cenario_id: str, registros: list[dict]) -> str | None:
    """O que a detecção acusou na primeira execução do cenário que detectou, como o ensaio gravou em cenarios.jsonl."""
    for r in sorted((r for r in registros if r.get("cenario") == cenario_id), key=lambda r: r.get("repeticao") or 0):
        if r.get("detectou") and r.get("motivo_deteccao"):
            return r["motivo_deteccao"]
    return None


def endereco_inicial(cenario_id: str) -> str:
    """O endereço do primeiro passo `abrir` do roteiro: o integrante começa por onde o roteiro começa."""
    c = cenario_do_ensaio(cenario_id)
    primeiro = next(p for p in cen.cenario(c["cenario"])["passos"] if p.get("acao") == "abrir")
    return urljoin(cen.BASE_PADRAO, primeiro["url"])


# ! Alteração de IA - Revisar: (16/11/2026, F2) a lista numerada dos passos saiu de `passos_do_roteiro` para `_passos_numerados`,
# que recebe o roteiro pronto; `passos_do_roteiro` devolve o mesmo texto de antes.
# ! Motivo: o treino de contrato mostra o roteiro `api-catalogo` do mesmo jeito que um cenário de contrato, mas não é um dos dez,
# e `passos_do_roteiro` só aceita cenário do ensaio.
def _passos_numerados(roteiro: dict, alvo: int | None = None) -> list[str]:
    linhas = []
    for i, p in enumerate(roteiro["passos"]):
        texto = cen._descrever(p)
        if p.get("acao") == "preencher":
            texto += f" com {cen.valor_do_passo(p)!r}"
        if i == alvo:
            texto += " (o passo que quebrou: este localizador não acha mais o elemento)"
        linhas.append(f"{i + 1}. {texto}")
    return linhas


def passos_do_roteiro(cenario_id: str) -> list[str]:
    """Os passos do roteiro numerados, com o valor de cada preenchimento, e o passo do localizador quebrado marcado."""
    c = cenario_do_ensaio(cenario_id)
    if c["tipo"] == "localizador":
        roteiro, q = roteiro_do_integrante(cenario_id)
        alvo = q["passo_alvo"]
    else:
        roteiro, alvo = cen.cenario(c["cenario"]), None
    return _passos_numerados(roteiro, alvo)


# ------------------------------------------------------------------ versão 2: o registro da sessão (sessao.jsonl)

# ! Alteração de IA - Revisar: (16/11/2026, F2) o registro da sessão: `montar_evento` e `gravar_evento` (uma linha JSON por evento,
# só acréscimo, com a hora local em milésimos e o mesmo instante em segundos desde 1970), `ler_registro`, `arquivo_do_registro` e
# `arquivo_dos_participantes` (resultados_alvo/fase5_manual por padrão; caminho absoluto para os testes e para a fumaça) e
# `vez_do_cenario` (integrante, posição, cenário e tipo, que todo evento de um cenário carrega).
# ! Motivo: a hora que o `armar` mostrava era `time.strftime('%H:%M:%S')`, sem fração de segundo e só na tela. O MTTR do agente é
# medido com três casas; para a comparação não carregar o arredondamento de um lado só, o registro guarda o milésimo. A gravação
# tenta de novo por dois segundos quando outro processo segura o arquivo, como o `_marcador` das corridas (27/10/2026).
def _relogio() -> float:
    """O relógio da máquina, em segundos desde 1970 (os testes trocam esta função)."""
    return time.time()


def _milesimos(t: float) -> int:
    return round(t * 1000)


def hora_do_relogio(t: float) -> str:
    """A hora local com milésimos (2026-11-19T14:03:22.417) do instante `t`."""
    ms = _milesimos(t)
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(ms // 1000)) + f".{ms % 1000:03d}"


def montar_evento(evento: str, vez: dict, t: float, **campos) -> dict:
    """Um evento do registro: a vez (integrante, ordem, cenário, tipo; o treino só tem o integrante), a hora e os campos dele."""
    return {"registro": VERSAO_DO_REGISTRO, "evento": evento, "integrante": vez.get("integrante"), "ordem": vez.get("ordem"),
            "cenario": vez.get("cenario"), "tipo": vez.get("tipo"), "hora": hora_do_relogio(t), "relogio_s": _milesimos(t) / 1000, **campos}


def gravar_evento(arquivo: Path, evento: str, vez: dict, relogio=None, **campos) -> dict:
    """Monta o evento com a hora de agora e o acrescenta ao registro; devolve o evento gravado."""
    e = montar_evento(evento, vez, (relogio or _relogio)(), **campos)
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    linha = json.dumps(e, ensure_ascii=False) + "\n"
    for tentativa in range(10):
        try:
            with open(arquivo, "a", encoding="utf-8", newline="\n") as f:
                f.write(linha)
                f.flush()
                os.fsync(f.fileno())
            return e
        except OSError:
            if tentativa == 9:
                raise
            time.sleep(0.2)
    return e


def ler_registro(arquivo: Path) -> list[dict]:
    """Os eventos do registro, na ordem em que foram gravados; lista vazia se o arquivo não existe. Linha que não é JSON
    (cortada por uma queda no meio da gravação) é pulada."""
    if not arquivo.exists():
        return []
    eventos = []
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        try:
            e = json.loads(linha)
        except json.JSONDecodeError:
            continue
        if isinstance(e, dict):
            eventos.append(e)
    return eventos


def _pasta(pasta: str | Path = PASTA_DA_SESSAO) -> Path:
    import caminhos
    p = Path(pasta)
    return p if p.is_absolute() else caminhos.RESULTADOS / p


def arquivo_do_registro(pasta: str | Path = PASTA_DA_SESSAO) -> Path:
    return _pasta(pasta) / NOME_DO_REGISTRO


def arquivo_dos_participantes(pasta: str | Path = PASTA_DA_SESSAO) -> Path:
    return _pasta(pasta) / NOME_DOS_PARTICIPANTES


def vez_do_cenario(integrante: int, posicao: int) -> dict:
    cid = cenario_da_vez(integrante, posicao)
    return {"integrante": integrante, "ordem": posicao, "cenario": cid, "tipo": cenario_do_ensaio(cid)["tipo"]}


# ! Alteração de IA - Revisar: (16/11/2026, F2) o que o `entregar` confere e calcula: `causa_da_lista` (a causa dentro das 23, sem
# cobrar maiúscula, acento ou sublinhado), `campo_entregue` ("nenhum" e vazio viram nenhum campo) e `resultado_da_entrega` (a regra
# do agente, cenarios_fase4.task_success_contrato, com a causa e o campo esperados do cenário).
# ! Motivo: o protocolo (seção 6) só para o cronômetro com a causa dentro das 23, e a seção 7 mede o integrante pela mesma régua
# do agente. Exigir a grafia exata mediria a digitação do facilitador, não o diagnóstico: é o que avaliar.py já faz com a
# resposta do modelo ("coleção_no_lugar_de_objeto" conta como "colecao_no_lugar_de_objeto").
def _sem_acento(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c))


def causa_da_lista(texto: str | None) -> str | None:
    """A causa como está em taxonomia.CAUSAS_RAIZ, ou None se o texto não é uma das 23."""
    import taxonomia
    t = re.sub(r"[\s\-]+", "_", _sem_acento((texto or "").strip().lower()))
    return t if t in taxonomia.CAUSAS_RAIZ else None


def campo_entregue(texto: str | None) -> str | None:
    """O campo que o integrante entregou; None quando ele disse "nenhum" ou deixou em branco."""
    t = (texto or "").strip().strip("'\"`")
    return None if not t or _sem_acento(t).lower() in ("nenhum", "-", "nao", "n") else t


def resultado_da_entrega(cenario_id: str, causa: str | None, campo: str | None) -> bool:
    """O Task Success do cenário de contrato para o que o integrante entregou: a causa e o campo esperados do cenário."""
    c = cenario_do_ensaio(cenario_id)
    return cen.task_success_contrato({"conferido": causa is not None, "causa": causa, "campo": campo}, c["causa"], c["campo"])


# ! Alteração de IA - Revisar: (16/11/2026, F2) `resumo_do_registro`: o que o registro diz de cada vez (integrante e posição): o
# início (o primeiro `armar`), o fim, os segundos, o desconto do banco, a causa e o campo ou o seletor e as tentativas, o
# corrigido, se o cenário está fechado e se estourou o limite; `cronometro_da_vez` (quanto tempo já passou numa vez aberta) e
# `avisos_do_limite` (em que segundo cada fala do limite é dita).
# ! Motivo: as regras de começo e de fim do cronômetro são as da seção 6 do protocolo, que espelham as do agente: no contrato o
# fim é a entrega, certa ou errada, com a causa dentro das 23; no localizador é a tentativa em que o roteiro passou, descontado
# o tempo de restaurar o banco de cada tentativa; quem passa de 10 minutos fica sem tempo de fim e não corrigido. Com a conta num
# lugar só, o comando `planilha`, o aviso do facilitador e a leitura da Fase 5 (avaliar_fase5.py --manual) usam a mesma regra.
def _resumo_da_vez(lista: list[dict], limite_s: float) -> dict:
    inicios = [e for e in lista if e["evento"] == "inicio"]
    primeiro = inicios[0]
    ms0 = _milesimos(primeiro["relogio_s"])
    r = {"integrante": primeiro["integrante"], "ordem": primeiro["ordem"], "cenario": primeiro["cenario"], "tipo": primeiro["tipo"],
         "inicio": primeiro["hora"], "inicio_s": primeiro["relogio_s"], "fim": None, "segundos": None, "descontar_s": 0.0, "causa": None,
         "campo": None, "seletor": None, "tentativas": 0, "corrigido": False, "fechado": False, "estourou": False, "entregue": False,
         "entrega_pendente": None, "avisos": []}
    if len(inicios) > 1:
        r["avisos"].append(f"vez armada {len(inicios)} vezes: o cronômetro corre desde o primeiro início ({primeiro['hora'][11:19]})")
    if r["tipo"] == "contrato":
        pendente = None
        for e in lista:
            if e["evento"] == "entrega" and pendente is None:
                pendente = e
            elif e["evento"] == "resposta" and pendente is not None:
                if e.get("recusada"):
                    r["avisos"].append(f"entrega recusada às {pendente['hora'][11:19]}: a causa não era uma das 23, e o tempo seguiu")
                    pendente = None
                    continue
                passado = (_milesimos(pendente["relogio_s"]) - ms0) / 1000
                r["entregue"] = r["fechado"] = True
                if passado > limite_s:
                    r["estourou"] = True
                    r["avisos"].append(f"a entrega veio {passado:.0f} s depois do início, além do limite de {limite_s:.0f} s: sem tempo de fim, e a resposta fica só no registro")
                else:
                    r.update(fim=pendente["hora"], segundos=round(passado, 3), causa=e.get("causa"), campo=e.get("campo"), corrigido=bool(e.get("corrigido")))
                pendente = None
                break
        r["entrega_pendente"] = pendente
    else:
        desconto = 0.0
        for e in lista:
            if e["evento"] != "tentativa":
                continue
            r["tentativas"] += 1
            r["seletor"] = e.get("seletor")
            desconto += e.get("segundos_do_banco") or 0.0
            if e.get("corrigido"):
                passado = (_milesimos(e["relogio_s"]) - ms0) / 1000 - desconto
                r["fechado"] = True
                if passado > limite_s:
                    r["estourou"] = True
                    r["avisos"].append(f"o seletor passou {passado:.0f} s depois do início, além do limite de {limite_s:.0f} s: sem tempo de fim")
                else:
                    r.update(fim=e["hora"], segundos=round(passado, 3), corrigido=True)
                break
        r["descontar_s"] = round(desconto, 3)
    if not r["fechado"]:
        # sem entrega e sem seletor que passou: o cenário só acaba quando a janela do último `armar` é encerrada
        ultimo = max(i for i, e in enumerate(lista) if e["evento"] == "inicio")
        r["fechado"] = any(e["evento"] == "fim_do_armar" for e in lista[ultimo + 1:])
    return r


def resumo_do_registro(eventos: list[dict], limite_s: float = LIMITE_S) -> dict[tuple[int, int], dict]:
    """Por vez (integrante, posição) que foi armada: início, fim, segundos, desconto, causa, campo, seletor, tentativas,
    corrigido, fechado, estourou e avisos. O treino e os eventos sem vez ficam de fora."""
    por_vez: dict[tuple[int, int], list[dict]] = {}
    ocorrencias: dict[tuple[int, int], list[dict]] = {}
    for e in eventos:
        if e.get("evento") in EVENTOS_DA_VEZ and isinstance(e.get("integrante"), int) and isinstance(e.get("ordem"), int):
            por_vez.setdefault((e["integrante"], e["ordem"]), []).append(e)
        elif e.get("evento") == EVENTO_DA_OCORRENCIA and isinstance(e.get("integrante"), int) and isinstance(e.get("ordem"), int):
            ocorrencias.setdefault((e["integrante"], e["ordem"]), []).append(e)
    resumo = {vez: _resumo_da_vez(lista, limite_s) for vez, lista in sorted(por_vez.items()) if any(e["evento"] == "inicio" for e in lista)}
    # ! Alteração de IA - Revisar: (17/11/2026, ficha 77, decisão 137) cada vez do resumo passa a dizer o aviso que o integrante
    # deixou no fim do cenário (`ocorrencia`) e se o facilitador anulou a linha por ele (`anulada`).
    # ! Motivo: o comando `planilha` escreve as observações a partir do resumo; o aviso fica fora de `_resumo_da_vez` porque não
    # muda o tempo, a resposta nem o corrigido do cenário (regra L14: a linha anulada é contada à parte, não é refeita).
    for vez, r in resumo.items():
        dela = ocorrencias.get(vez, [])
        r["ocorrencia"] = " / ".join(str(e.get("texto") or "") for e in dela) or None
        r["anulada"] = any(e.get("anulada") is True for e in dela)
    return resumo


def cronometro_da_vez(eventos: list[dict], integrante: int, ordem: int, agora_s: float) -> dict | None:
    """Quanto do cronômetro já correu na vez (do início até agora, descontado o banco das tentativas) e se ela já fechou."""
    r = resumo_do_registro(eventos).get((integrante, ordem))
    if r is None:
        return None
    return {"passado_s": round(agora_s - r["inicio_s"] - r["descontar_s"], 3), "fechado": r["fechado"]}


def avisos_do_limite() -> list[tuple[int, str]]:
    """Em que segundo do cronômetro o facilitador diz cada fala do limite."""
    return [(LIMITE_S - AVISO_FINAL_S, FALAS_DO_PLANO[1]), (LIMITE_S, FALAS_DA_FERRAMENTA[3])]


# ------------------------------------------------------------------ versão 2: a planilha preenchida pelo registro

# ! Alteração de IA - Revisar: (16/11/2026, F2) `celulas_do_resumo` (as nove células de uma vez, como vão para a planilha),
# `numero` (lê um número com vírgula ou com ponto) e `preencher_planilha` (devolve o texto novo da planilha, o que preencheu e os
# avisos, sem gravar). Só célula vazia é preenchida, e só de cenário fechado; célula preenchida com outro valor fica como está e
# vira aviso; linha preenchida sem registro que a explique recebe `anotada à mão` nas observações se a célula estiver vazia, e
# aviso se já tiver texto sem a marca. As linhas que não mudam voltam byte a byte.
# ! Motivo: o plano (seção 4.5) quer a planilha preenchida a partir do registro e proíbe trocar célula preenchida: se a
# ferramenta falhar num cenário, vale a anotação à mão do cronômetro de reserva, e a leitura precisa saber qual linha é essa. Os
# segundos saem com vírgula decimal porque a planilha foi feita para abrir no Excel em português, que lê 83.417 como 83417; a
# hora sai em HH:MM:SS, como na versão 1 (os milésimos ficam no registro).
def _numero_br(x: float, casas: int) -> str:
    return f"{x:.{casas}f}".replace(".", ",")


def numero(celula: str | None) -> float | None:
    """O número de uma célula, com vírgula ou com ponto decimal; None se a célula está vazia ou não é número."""
    try:
        return float((celula or "").strip().replace(",", "."))
    except ValueError:
        return None


def celulas_do_resumo(r: dict) -> dict[str, str]:
    contrato = r["tipo"] == "contrato"
    return {"inicio": r["inicio"][11:19], "fim": r["fim"][11:19] if r["fim"] else "",
            "segundos": _numero_br(r["segundos"], 3) if r["segundos"] is not None else "",
            "descontar_s": _numero_br(r["descontar_s"], 2) if r["descontar_s"] else "0",
            "causa": (r["causa"] or "") if contrato else "",
            "campo": (r["campo"] or "nenhum") if contrato and r["causa"] else "",
            "seletor": "" if contrato else (r["seletor"] or ""),
            "tentativas": "" if contrato else str(r["tentativas"]),
            "corrigido": "sim" if r["corrigido"] else "não"}


def _mesma_celula(coluna: str, na_planilha: str, do_registro: str) -> bool:
    if coluna in ("segundos", "descontar_s", "tentativas"):
        a, b = numero(na_planilha), numero(do_registro)
        return a is not None and b is not None and abs(a - b) < 0.0005
    if coluna in ("causa", "campo", "corrigido"):
        return _sem_acento(na_planilha.strip().lower()) == _sem_acento(do_registro.strip().lower())
    return na_planilha.strip() == do_registro.strip()


def _linha_csv(celulas: list[str]) -> str:
    saida = io.StringIO()
    csv.writer(saida, delimiter=SEPARADOR, lineterminator="").writerow(celulas)
    return saida.getvalue()


def preencher_planilha(texto: str, resumo: dict[tuple[int, int], dict]) -> tuple[str, list[str], list[str]]:
    """O texto da planilha com as células vazias preenchidas pelo registro, a lista do que foi preenchido e a dos avisos."""
    linhas = texto.split("\n")
    cabecalho = next(csv.reader([linhas[0]], delimiter=SEPARADOR))
    faltam = [c for c in COLUNAS_DA_PLANILHA if c not in cabecalho]
    if faltam:
        raise ValueError(f"a planilha não tem as colunas {faltam}")
    idx = {c: i for i, c in enumerate(cabecalho)}
    preenchidas, avisos, vistas = [], [], set()
    for n, bruta in enumerate(linhas[1:], 1):
        if not bruta.strip():
            continue
        celulas = next(csv.reader([bruta], delimiter=SEPARADOR))
        celulas += [""] * (len(cabecalho) - len(celulas))
        try:
            vez = (int(celulas[idx["integrante"]]), int(celulas[idx["ordem"]]))
        except ValueError:
            avisos.append(f"linha {n + 1} da planilha: integrante ou ordem que não é número; linha deixada como está")
            continue
        vistas.add(vez)
        onde = f"integrante {vez[0]}, ordem {vez[1]}"
        r = resumo.get(vez)
        mudou = []
        if r is not None and r["fechado"]:
            if r["cenario"] != celulas[idx["cenario"]].strip():
                avisos.append(f"{onde}: a planilha diz o cenário {celulas[idx['cenario']]!r} e o registro diz {r['cenario']!r}; linha deixada como está")
                continue
            for coluna, valor in celulas_do_resumo(r).items():
                atual = celulas[idx[coluna]].strip()
                if not atual:
                    if valor:
                        celulas[idx[coluna]] = valor
                        mudou.append(coluna)
                elif not _mesma_celula(coluna, atual, valor):
                    avisos.append(f"{onde}, coluna {coluna}: a planilha diz {atual!r} e o registro diz {valor!r}; a planilha não foi trocada")
            # ! Alteração de IA - Revisar: (17/11/2026, ficha 77, decisão 137) o aviso que o integrante deixou no fim do cenário vai
            # para as observações da linha, com `ANULADA` no começo quando o facilitador anulou na importação.
            # ! Motivo: a leitura da Fase 5 tira da conta a linha cujas observações começam com `ANULADA` (regra L14). Como nas
            # outras colunas, observação já escrita não é trocada: se ela não traz o aviso, o comando só avisa.
            if r.get("ocorrencia"):
                nota = observacao_da_ocorrencia(r["ocorrencia"], r["anulada"])
                observacoes = " ".join(celulas[idx["observacoes"]:]).strip()
                if not observacoes:
                    celulas[idx["observacoes"]] = nota
                    mudou.append(f"observacoes ({ROTULO_DA_OCORRENCIA})")
                elif _sem_acento(nota.lower()) not in _sem_acento(observacoes.lower()):
                    avisos.append(f"{onde}: há um aviso do integrante ({r['ocorrencia']!r}; linha {'anulada' if r['anulada'] else 'mantida'} na importação) "
                                  "e as observações já têm outro texto; a planilha não foi trocada")
        elif any(celulas[idx[c]].strip() for c in COLUNAS_DO_REGISTRO):
            # alguém preencheu a linha e o registro não tem este cenário fechado: é a anotação do cronômetro de reserva
            observacoes = " ".join(celulas[idx["observacoes"]:])   # um ponto e vírgula digitado na observação abre células a mais
            if not observacoes.strip():
                celulas[idx["observacoes"]] = MARCA_A_MAO
                mudou.append(f"observacoes ({MARCA_A_MAO})")
            elif _sem_acento(MARCA_A_MAO) not in _sem_acento(observacoes.lower()):
                avisos.append(f"{onde}: linha preenchida sem registro da ferramenta; escreva `{MARCA_A_MAO}` nas observações "
                              "(o comando não troca célula preenchida)")
        if mudou:
            linhas[n] = _linha_csv(celulas)
            preenchidas.append(f"{onde}: {', '.join(mudou)}")
    for vez, r in resumo.items():
        if r["fechado"] and vez not in vistas:
            avisos.append(f"integrante {vez[0]}, ordem {vez[1]}: está no registro e não está na planilha")
    return "\n".join(linhas), preenchidas, avisos


# ------------------------------------------------------------------ versão 2: o perfil dos integrantes (participantes.json)

# ! Alteração de IA - Revisar: (16/11/2026, F2) `perfil_do_integrante` (confere que o perfil tem só os campos previstos: as três
# respostas, a anotação do facilitador e o que o integrante conhece do código) e `gravar_perfil` (grava em participantes.json pelo
# número do integrante, com as perguntas ao lado; não troca um perfil já gravado sem `regravar`).
# ! Motivo: o plano (seção 4.1) quer o perfil sem o nome, porque o repositório é público e a leitura fala em integrante 1, 2 e 3.
# Recusar campo a mais é o que impede o nome de entrar por descuido.
def perfil_do_integrante(respostas: dict) -> dict:
    """O perfil conferido, com os campos na ordem fixa; ValueError se sobrar ou faltar campo, ou se um sim/não não for booleano."""
    if set(respostas) != set(CAMPOS_DO_PERFIL):
        raise ValueError(f"o perfil tem de ter exatamente os campos {list(CAMPOS_DO_PERFIL)}: veio {sorted(respostas)}")
    if not isinstance(respostas["pratica"], str) or not respostas["pratica"].strip():
        raise ValueError("a resposta sobre o tempo de prática não pode ficar em branco")
    for campo in ("ja_usou_as_ferramentas_do_desenvolvedor", "ja_leu_a_lista_dos_cenarios", "conhece_o_codigo_das_cobaias"):
        if not isinstance(respostas[campo], bool):
            raise ValueError(f"{campo}: a resposta é sim ou não")
    return {"pratica": respostas["pratica"].strip(), **{c: respostas[c] for c in CAMPOS_DO_PERFIL[1:4]},
            "o_que_conhece": str(respostas["o_que_conhece"] or "").strip()}


def gravar_perfil(arquivo: Path, integrante: int, perfil: dict, agora: str | None = None, regravar: bool = False) -> dict:
    if not 1 <= integrante <= INTEGRANTES:
        raise ValueError(f"integrante {integrante} fora da planilha (1 a {INTEGRANTES})")
    perfil = perfil_do_integrante(perfil)
    dado = json.loads(arquivo.read_text(encoding="utf-8")) if arquivo.exists() else {"integrantes": {}}
    if str(integrante) in dado["integrantes"] and not regravar:
        raise ValueError(f"o integrante {integrante} já tem perfil gravado em {arquivo.name}; use --regravar para trocar")
    dado["integrantes"][str(integrante)] = {**perfil, "respondido_em": agora or dt.datetime.now().isoformat(timespec="seconds")}
    dado["perguntas"] = {**PERGUNTAS_DE_PERFIL, **ANOTACAO_DO_FACILITADOR}
    # a tag vai num campo porque JSON não aceita comentário (como em fixtures_fase4/hashes_areas_so_leitura.json)
    dado["tag_ia"] = {"alteracao": "! Alteração de IA - Revisar: gravado por `linha_de_base_manual.py perfil` (Fase 5, pacote F2): as respostas de cada "
                                   "integrante da linha de base manual às três perguntas de perfil e a anotação do facilitador, pelo número do integrante.",
                      "motivo": "! Motivo: o plano da Fase 5 (seção 4.1) pede o perfil para a leitura declarar quem tinha prática e quem conhecia o código "
                                "das cobaias; o nome não é gravado porque o repositório é público."}
    arquivo.parent.mkdir(parents=True, exist_ok=True)
    arquivo.write_text(json.dumps(dado, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return dado


# ------------------------------------------------------------------ versão 2: os textos que saem por comando

# ! Alteração de IA - Revisar: (16/11/2026, F2) `texto_do_facilitador` (a abertura, o treino, as falas durante um cenário e o
# fecho), `folha_do_integrante` (o que ele recebe, o que pode e não pode, como responde, o limite e as 23 causas com a definição),
# `ficha_do_treino`, e `blocos_do_protocolo` / `conferir_protocolo` (os dois textos como blocos `<!-- tabela:tb_f5_... -->` que o
# protocolo cola, pelo mesmo mecanismo dos relatórios: analisar_fase3b.colar e conferir_doc).
# ! Motivo: o plano (pacote F2) quer estes textos saindo por comando, para não serem digitados: o que o facilitador lê em voz
# alta e o que o integrante recebe têm de ser iguais nas três sessões, e os números que eles citam (limite, cenários, causas)
# vêm das constantes do código. Nenhum dos dois traz nome de cenário, de modo de falha ou de modo de quebra (o teste confere).
def texto_do_facilitador() -> str:
    cenarios, causas, minutos = len(cen.CENARIOS_DO_ENSAIO), len(DEFINICAO_DAS_CAUSAS), LIMITE_S // 60
    linhas = [
        "**Texto fixo do facilitador.** Leia em voz alta, como está escrito. O que for dito além deste texto vai para a coluna `observacoes` da planilha.",
        "",
        "**Abertura**, antes do treino:",
        "",
        f'1. "Esta sessão mede duas coisas em {cenarios} cenários de teste com uma falha: quanto tempo leva para resolver cada um e se a resposta está '
        'certa. O que se mede é o trabalho feito à mão, não você: o seu nome não entra em nenhum arquivo."',
        '2. "Em cada cenário você recebe a ficha da falha, que é a frase que o teste automático acusou, o roteiro do teste passo a passo e o navegador '
        'aberto onde o roteiro começa, com as ferramentas do desenvolvedor, na tecla F12. A sua folha diz tudo isto por escrito."',
        f'3. "Há dois tipos de cenário. No de contrato, a resposta é uma causa da lista de {causas} da sua folha e o campo afetado, ou nenhum. No de '
        'localizador, a resposta é um seletor, CSS ou do Playwright, que ache o elemento do passo que quebrou. Escreva a resposta no bloco de notas ao '
        'lado e me avise."',
        '4. "Você pode navegar, inspecionar a página, ver as chamadas na aba de rede, abrir a API pelo navegador e consultar a documentação de '
        'seletores. Não pode abrir o código das aplicações, o código do agente nem o repositório, usar assistente de IA, ver a minha planilha nem '
        'falar com os outros integrantes sobre os cenários."',
        f'5. "O tempo começa quando o navegador abre. No cenário de contrato ele para quando você entrega; a entrega é uma só, e eu não digo se está '
        f'certa. No de localizador eu confiro o seletor: se o roteiro passar, o tempo para; se não passar, o tempo segue e você pode tentar de novo. O '
        f'limite é de {minutos} minutos por cenário, e entre um cenário e outro a pausa é livre."',
        f'6. "Um aviso sobre a aplicação: a tela de login volta sozinha para a página inicial depois de {SEGUNDOS_DA_VOLTA_DO_LOGIN} segundos. Isso não '
        'é a falha. Se acontecer, abra a tela de login de novo no mesmo navegador."',
        '7. "Durante um cenário eu não respondo perguntas sobre ele e só digo as frases combinadas."',
        '8. "Antes de começar, três perguntas."',
        *[f'   - "{pergunta}"' for pergunta in PERGUNTAS_DE_PERFIL.values()],
        "",
        "As respostas são gravadas com o comando `perfil`, sem o nome. Quem responde que já leu a lista dos cenários não serve de integrante; se não "
        "houver substituto, participa e isso fica declarado na leitura.",
        "",
        "**Treino**, sem cronômetro:",
        "",
        '9. "Agora um treino, sem cronômetro, para você conhecer o material e a forma da resposta: um cenário de contrato e um exercício de seletor '
        'que não estão entre os que valem. Só no treino eu digo a resposta certa."',
        "",
        "**Durante um cenário**, as únicas falas:",
        "",
        f'- "{FALAS_DO_PLANO[0]}" Quando o navegador abre.',
        f'- "{FALAS_DO_PLANO[1]}" Quando a janela do `armar` avisar.',
        f'- "{FALAS_DO_PLANO[2]}" Se o integrante perguntar se já pode entregar.',
        f'- "{FALAS_DA_FERRAMENTA[0]}" Quando o `entregar` recusar a causa.',
        f'- "{FALAS_DA_FERRAMENTA[1]}" Quando o `conferir` disser "não corrigido".',
        f'- "{FALAS_DA_FERRAMENTA[2]}" Quando o `conferir` disser "CORRIGIDO".',
        f'- "{FALAS_DA_FERRAMENTA[3]}" Quando a janela do `armar` avisar que os {minutos} minutos acabaram.',
        "",
        "O cronômetro de reserva, no celular, é disparado na primeira fala e parado na entrega ou no seletor que passou; os dois horários vão para a "
        "folha de papel, com o número do integrante e a posição do cenário.",
        "",
        "**Fecho**:",
        "",
        '- "Acabou. Obrigado."',
        '- "Por favor, não comente os cenários nem as respostas com os outros integrantes até as sessões deles acabarem."',
    ]
    return "\n".join(linhas) + "\n"


def folha_do_integrante() -> str:
    cenarios, causas, minutos = len(cen.CENARIOS_DO_ENSAIO), len(DEFINICAO_DAS_CAUSAS), LIMITE_S // 60
    linhas = [
        "**Folha do integrante.** Fique com esta folha durante a sessão.",
        "",
        f"**O que é a sessão.** São {cenarios} cenários de teste automatizado, cada um com uma falha armada de propósito. Em cada cenário o teste "
        "parou ou acusou um problema, e o seu trabalho é dizer o que quebrou. Mede-se o tempo de cada cenário e se a resposta está certa. O seu nome "
        "não entra em nenhum arquivo.",
        "",
        "**O que você recebe em cada cenário:**",
        "",
        "- a ficha da falha: a frase que o teste automático acusou;",
        "- o roteiro do teste, passo a passo, com o valor de cada preenchimento; nos cenários de localizador, o passo que quebrou vem marcado;",
        f"- nos cenários de contrato, o contrato esperado da resposta da API e a lista das {causas} causas, que está no fim desta folha;",
        "- o navegador aberto onde o roteiro começa, com as ferramentas do desenvolvedor (F12): elementos, rede e console.",
        "",
        f"**Pode:** {O_QUE_PODE}.",
        "",
        f"**Não pode:** {O_QUE_NAO_PODE}.",
        "",
        "**Como responder:**",
        "",
        "- Cenário de contrato: uma causa da lista, escrita como está nesta folha, e o campo afetado (ou nenhum). Escreva no bloco de notas ao lado "
        "do navegador e avise o facilitador. A entrega é uma só, e o facilitador não diz se está certa.",
        "- Cenário de localizador: um seletor, CSS ou do Playwright, que ache o elemento do passo que quebrou. Escreva no bloco de notas e avise o "
        "facilitador, que confere. Se o roteiro não passar, o tempo segue e você pode tentar de novo.",
        "",
        f"**O tempo.** Começa quando o navegador abre. Para na entrega, no cenário de contrato, ou quando o seletor passa, no de localizador. O limite "
        f"é de {minutos} minutos por cenário. Entre um cenário e outro a pausa é livre.",
        "",
        f"**Um aviso sobre a aplicação.** A tela de login volta sozinha para a página inicial depois de {SEGUNDOS_DA_VOLTA_DO_LOGIN} segundos. Isso não "
        "é a falha: abra a tela de login de novo no mesmo navegador.",
        "",
        f"**As {causas} causas** dos cenários de contrato. Escolha uma:",
        "",
        *[f"{i}. `{causa}`: {definicao}" for i, (causa, definicao) in enumerate(DEFINICAO_DAS_CAUSAS.items(), 1)],
    ]
    return "\n".join(linhas) + "\n"


def ficha_do_treino() -> str:
    """A ficha da falha do cenário de contrato do treino, na forma em que a detecção do agente escreve um atraso (executar_fase4.reproduz)."""
    import executar_fase4 as ex
    return f"o roteiro passou na tela, mas o fio acusou: tempo de resposta acima do orçamento de {ex.ORCAMENTO_DE_TEMPO_MS} ms"


# ! Alteração de IA - Revisar: (16/11/2026, F2) `passos_do_ensaio`: o passo a passo do ensaio do facilitador, com os comandos
# montados a partir do catálogo: os dez cenários pelo nome, os quatro de localizador sem seletor e com o seletor que conserta, e
# os comandos da versão 2 numa pasta de teste, com uma vez de contrato e uma de localizador do integrante 1 e a planilha em cópia.
# ! Motivo: o protocolo (seção 4, item 3) pede o ensaio antes das sessões, para conferir que cada cenário abre. Escritos à mão,
# os dez nomes e os seletores ficariam velhos na primeira mudança do catálogo; e um comando com `--vez` sem a pasta de teste
# gravaria no registro da sessão de verdade.
def passos_do_ensaio() -> str:
    py = "python linha_de_base_manual.py"
    reg = f"--registro {PASTA_DO_ENSAIO}"
    tipos = {c["id"]: c["tipo"] for c in cen.CENARIOS_DO_ENSAIO}
    do_um = ordem_dos_integrantes()[1]
    pc = next(i for i, cid in enumerate(do_um, 1) if tipos[cid] == "contrato")
    pl = next(i for i, cid in enumerate(do_um, 1) if tipos[cid] == "localizador")
    BARRA = chr(92)   # a barra invertida dos caminhos do Windows, que o facilitador cola no PowerShell
    pasta = "resultados_alvo" + BARRA + PASTA_DO_ENSAIO
    copia = pasta + BARRA + "planilha.csv"
    origem = BARRA.join(["..", "..", "..", "Documentacao", "memorial", "5-metodo-e-ferramental", PLANILHA.name])
    linhas = [
        f"Ensaio do facilitador: os {len(cen.CENARIOS_DO_ENSAIO)} cenários uma vez, pelo nome, sem cronômetro e sem integrante.",
        "Nada daqui grava no registro da sessão de verdade (resultados_alvo" + BARRA + PASTA_DA_SESSAO + ").",
        "",
        "Preparação",
        "  Janela 1, na raiz do repositório:",
        "    python run.py",
        "  Janelas 2 e 3, em Programacao" + BARRA + "AgenteCore" + BARRA + "experimentos, com a venv do AgenteCore ativa:",
        '    $env:RESULTADOS_DIR = "resultados_alvo"',
        "",
        "1. Os cenários pelo nome, na janela 2. Em cada um: a ficha da falha aparece, o navegador abre na página do roteiro e a falha está lá;",
        "   Enter fecha o navegador e desarma.",
        *[f"    {py} armar --cenario {c['id']}" for c in cen.CENARIOS_DO_ENSAIO],
        "",
        "2. Os de localizador, na janela 2: sem seletor o roteiro não pode passar, porque a quebra está armada (o comando sai com código 0);",
        '   com o seletor, tem de dizer "CORRIGIDO".',
    ]
    for c in cen.CENARIOS_DE_LOCALIZADOR:
        linhas += [f"    {py} conferir --cenario {c['id']}", f'    {py} conferir --cenario {c["id"]} --seletor "{SELETOR_DO_ENSAIO[c["id"]]}"']
    linhas += [
        "",
        f"3. Os comandos da versão 2, numa pasta de teste ({pasta}). O --registro é obrigatório em todos.",
        "   Perfil e treino, na janela 2:",
        f"    {py} perfil --integrante 1 {reg}",
        f"    {py} treino contrato --integrante 1 {reg}",
        f"    {py} treino seletor --integrante 1 {reg}",
        "   Um cenário de contrato: armar na janela 2; na janela 3, deixar o entregar esperando, dar Enter e digitar a causa e o campo;",
        "   depois, Enter na janela 2.",
        f"    {py} armar --vez 1 {pc} {reg}",
        f"    {py} entregar --vez 1 {pc} {reg}",
        "   Um cenário de localizador: armar na janela 2; na janela 3, um seletor errado e depois o certo; Enter na janela 2.",
        f"    {py} armar --vez 1 {pl} {reg}",
        f'    {py} conferir --vez 1 {pl} --seletor "#errado" {reg}',
        f'    {py} conferir --vez 1 {pl} --seletor "{SELETOR_DO_ENSAIO[do_um[pl - 1]]}" {reg}',
        "   A planilha, numa cópia: as duas linhas do integrante 1 têm de sair preenchidas, com 0 aviso.",
        f'    Copy-Item "{origem}" "{copia}"',
        f'    {py} planilha {reg} --planilha "{copia}"',
        "",
        "4. Limpeza: apagar a pasta do ensaio, voltar a CobaiaAPI ao modo normal e Ctrl+C na janela 1.",
        f'    Remove-Item -Recurse -Force "{pasta}"',
        f"    {py} desarmar",
    ]
    return "\n".join(linhas) + "\n"


def _bloco(nome: str, texto: str) -> str:
    return f"<!-- tabela:{nome} -->\n{texto.strip()}\n<!-- /tabela:{nome} -->"


def blocos_do_protocolo() -> str:
    """Os dois textos fixos como os blocos que o protocolo cola."""
    return _bloco("tb_f5_folha_do_integrante", folha_do_integrante()) + "\n\n" + _bloco("tb_f5_texto_do_facilitador", texto_do_facilitador()) + "\n"


def conferir_protocolo() -> list[str]:
    """Os blocos do protocolo que faltam ou que estão diferentes do que o código gera (lista vazia quando está em dia)."""
    import analisar_fase3b as a3b
    gerado = blocos_do_protocolo()
    no_documento = a3b.blocos_de(PROTOCOLO.read_text(encoding="utf-8"))
    return sorted(set(a3b.conferir_doc(PROTOCOLO, gerado)) | {n for n in a3b.blocos_de(gerado) if n not in no_documento})


# ------------------------------------------------------------------ comandos (precisam das cobaias, do banco e do navegador)

def _registros_do_ensaio(saida: str) -> list[dict]:
    import caminhos
    import executar_bateria
    arq = caminhos.fase3(saida)["raiz"] / "cenarios.jsonl"
    return executar_bateria.ler_jsonl(arq) if arq.exists() else []


def _restaurar_banco() -> tuple[str, float]:
    sys.path.insert(0, str(RAIZ))
    import _env_common as env
    import restaurar_banco as rb
    cli = env.find_mysql_cli()
    t0 = time.monotonic()
    if rb.restaurar(cli) != rb.CONTAGENS_DO_SEED:
        raise SystemExit("!! o banco restaurado não tem as contagens do seed")
    return rb.hash_das_tabelas(cli), round(time.monotonic() - t0, 2)


def _cobaias_no_ar() -> bool:
    sys.path.insert(0, str(RAIZ))
    import run
    return run.wait_until_ready(timeout_s=5)


def _cenario_pedido(args: argparse.Namespace) -> tuple[str, str]:
    if args.vez:
        n, p = args.vez
        return cenario_da_vez(n, p), f"integrante {n}, cenário {p} de {len(cen.CENARIOS_DO_ENSAIO)}"
    cenario_do_ensaio(args.cenario)
    return args.cenario, args.cenario


# ! Alteração de IA - Revisar: (16/11/2026, F2) o que os comandos da versão 2 usam em comum: `_ler` (o teclado; sem teclado, como
# na fumaça, responde vazio), `_pasta_do_registro` (recusa gravar o registro fora de resultados_alvo), `_sim_ou_nao`, `_minutos`
# e `_vigiar_o_limite` (um fio em segundo plano que, enquanto a janela do `armar` espera o Enter, lê o registro a cada segundo e
# imprime a fala dos dois minutos e a do tempo esgotado na hora certa, já descontado o banco das tentativas).
# ! Motivo: sem RESULTADOS_DIR=resultados_alvo os experimentos gravam em `resultados/`: o registro da sessão iria para a pasta
# errada sem ninguém notar, e a ficha da falha não seria achada. E o facilitador, que agora não anota mais a hora, não teria como
# saber a hora de dizer "Faltam dois minutos." sem ficar olhando o cronômetro de reserva.
def _ler(texto: str) -> str:
    try:
        return input(texto)
    except EOFError:
        return ""


def _pasta_do_registro(args: argparse.Namespace) -> Path | None:
    import caminhos
    pasta = getattr(args, "registro", None) or PASTA_DA_SESSAO
    if not Path(pasta).is_absolute() and caminhos.RESULTADOS.name != "resultados_alvo":
        print("!! o registro da sessão e a ficha da falha ficam em resultados_alvo: defina RESULTADOS_DIR=resultados_alvo antes do comando "
              '(no PowerShell: $env:RESULTADOS_DIR = "resultados_alvo")')
        return None
    return _pasta(pasta)


def _sim_ou_nao(texto: str | None) -> bool | None:
    t = _sem_acento((texto or "").strip().lower())
    return True if t in ("s", "sim") else False if t in ("n", "nao") else None


def _minutos(segundos: float) -> str:
    return f"{int(segundos // 60):02d}:{int(segundos % 60):02d}"


def _vigiar_o_limite(arquivo: Path, vez: dict, parar: threading.Event) -> threading.Thread:
    def laco() -> None:
        ditos: set[int] = set()
        while not parar.wait(1.0):
            try:
                c = cronometro_da_vez(ler_registro(arquivo), vez["integrante"], vez["ordem"], _relogio())
            except Exception:  # noqa: BLE001 - o aviso nunca derruba a janela do integrante
                continue
            if c is None or c["fechado"]:
                return
            for segundos, fala in avisos_do_limite():
                if c["passado_s"] >= segundos and segundos not in ditos:
                    ditos.add(segundos)
                    print(f'\n>> {segundos // 60} min de cronômetro. Fala do facilitador: "{fala}"'
                          + (" O cenário fica não corrigido, sem tempo de fim; Enter aqui fecha o navegador." if segundos >= LIMITE_S else ""), flush=True)
            if LIMITE_S in ditos:
                return
    fio = threading.Thread(target=laco, daemon=True)
    fio.start()
    return fio


# ! Alteração de IA - Revisar: (16/11/2026, F2) o `armar --vez` grava no registro o início (logo depois de o navegador abrir no
# endereço do roteiro, o mesmo ponto em que a tela dizia "início do cronômetro") e o fim da janela (o Enter), mostra na tela a
# hora que gravou e vigia o limite enquanto espera; avisa quando a vez já tinha sido armada. Pelo nome (`--cenario`), nada muda.
# ! Motivo: decisão 131: quem grava o tempo é a ferramenta. O início fica no mesmo instante da versão 1 para as sessões medirem
# o que o protocolo descreve (seção 6: o cronômetro começa com o navegador aberto e o material na tela).
def armar(args: argparse.Namespace) -> int:
    import executar_fase4 as ex
    import navegador
    import taxonomia
    cid, rotulo = _cenario_pedido(args)
    c = cenario_do_ensaio(cid)
    vez, arq = None, None
    if args.vez:
        pasta = _pasta_do_registro(args)
        if pasta is None:
            return 2
        vez, arq = vez_do_cenario(*args.vez), pasta / NOME_DO_REGISTRO
    if not _cobaias_no_ar():
        print("!! as cobaias não responderam nas portas 8080 e 8000: suba com `python run.py` na raiz do repositório")
        return 2
    if vez:
        ja = resumo_do_registro(ler_registro(arq)).get((vez["integrante"], vez["ordem"]))
        if ja is not None:
            print(f"!! esta vez já foi armada às {ja['inicio'][11:19]}" + (" e já está fechada" if ja["fechado"] and (ja["entregue"] or ja["fim"]) else "")
                  + ": o cronômetro dela continua valendo desde lá; anote o motivo nas observações da planilha")
    h, seg = _restaurar_banco()
    print(f"{rotulo}: banco restaurado e conferido (hash {h}, {seg} s)")
    if c["tipo"] == "contrato":
        ex.ligar_modo(c["modo"], c["campo"], args.token)
        print("falha ligada na CobaiaAPI para GET /api/produtos")
    ficha = ficha_da_falha(cid, _registros_do_ensaio(args.saida))
    print("\n== Ficha da falha (o que a detecção do agente acusou neste cenário na corrida 21)")
    print(ficha or f"(sem ficha: {args.saida}/cenarios.jsonl não tem este cenário; rode a corrida 21 antes da sessão)")
    print("\n== Roteiro do teste")
    print("\n".join(passos_do_roteiro(cid)))
    if c["tipo"] == "contrato":
        print("\n== Contrato esperado de cada produto em GET /api/produtos (o mesmo que o agente recebe)")
        print(ex._contrato_do_produto())
        print("\n== Resposta: uma causa desta lista e o campo afetado (ou nenhum)")
        print(", ".join(taxonomia.CAUSAS_RAIZ))
    else:
        print("\n== Resposta: um seletor (CSS ou do Playwright) que ache o elemento do passo que quebrou")
    with navegador.Navegador(canal=args.canal, headless=False) as nav:
        pagina = nav.nova_pagina()
        if c["tipo"] == "localizador":
            cen.armar_quebra(pagina, cen.quebra(c["cenario"], c["modo"]), args.forma)
        pagina.goto(endereco_inicial(cid))
        versao = nav.versao()["navegador"]
        hora = time.strftime("%H:%M:%S")
        parar = threading.Event()
        if vez:
            inicio = gravar_evento(arq, "inicio", vez, navegador=versao, hash_do_banco=h, segundos_do_banco=seg,
                                   forma=args.forma if c["tipo"] == "localizador" else None, ficha=ficha)
            hora = inicio["hora"][11:19]
        print(f"\nnavegador {versao} aberto para o integrante; início do cronômetro: {hora}")
        if vez:
            print(f'início gravado em {arq}. Fala do facilitador: "{FALAS_DO_PLANO[0]}"')
            fio = _vigiar_o_limite(arq, vez, parar)
        try:
            _ler("Enter fecha o navegador e desarma o cenário (F12 abre as ferramentas do desenvolvedor)... ")
        finally:
            parar.set()
        if vez:
            fio.join(timeout=3)
            gravar_evento(arq, "fim_do_armar", vez)
    if c["tipo"] == "contrato":
        ex.ligar_modo("normal", None, args.token)
        print("CobaiaAPI de volta ao modo normal")
    return 0


# ! Alteração de IA - Revisar: (16/11/2026, F2) o `conferir --vez --seletor` grava no registro cada tentativa: o seletor, se o
# roteiro passou, a hora em que o roteiro terminou, os segundos de restauração do banco e os do roteiro, e o que falhou. Depois
# diz quantas tentativas a vez tem e quanto do cronômetro correu. Sem seletor, ou pelo nome (`--cenario`), nada é gravado.
# ! Motivo: na versão 1 o facilitador anotava o fim, somava à mão os segundos do banco de cada tentativa e contava as tentativas;
# são as três contas que a planilha agora recebe do registro.
def conferir(args: argparse.Namespace) -> int:
    import navegador
    cid, rotulo = _cenario_pedido(args)
    roteiro, q = roteiro_do_integrante(cid, args.seletor)
    vez, arq = None, None
    if args.vez and args.seletor:
        pasta = _pasta_do_registro(args)
        if pasta is None:
            return 2
        vez, arq = vez_do_cenario(*args.vez), pasta / NOME_DO_REGISTRO
    if not _cobaias_no_ar():
        print("!! as cobaias não responderam nas portas 8080 e 8000: suba com `python run.py` na raiz do repositório")
        return 2
    _, seg_banco = _restaurar_banco()
    hora = None
    with navegador.Navegador(canal=args.canal) as nav:
        pagina = nav.nova_pagina()
        cen.armar_quebra(pagina, q, args.forma)
        r = cen.rodar_cenario(roteiro, pagina, None, capturar=False, tempo_limite_ms=cen.TEMPO_LIMITE_QUEBRA_MS)
        ok = cen.task_success(r)
        if vez:
            hora = gravar_evento(arq, "tentativa", vez, seletor=args.seletor, corrigido=ok, segundos_do_banco=seg_banco,
                                 segundos_do_roteiro=r.get("segundos"), motivo=None if ok else cen.motivo_do_roteiro(r))["hora"][11:19]
        pagina.close()
    for conf in r["conferencias"]:
        print(f"  {'confere' if conf['passou'] else 'NÃO confere'}: {conf['nome']}")
    if not args.seletor:
        print(f"{rotulo}, com o localizador quebrado do roteiro: {cen.motivo_do_roteiro(r) or 'o roteiro passou (a quebra não foi armada?)'}")
        return 0 if not ok else 1
    if not ok:
        print(f"  {cen.motivo_do_roteiro(r)}")
    print(f"{rotulo} com o seletor {args.seletor!r}: {'CORRIGIDO (o roteiro chegou ao fim sem erro)' if ok else 'não corrigido'} às "
          f"{hora or time.strftime('%H:%M:%S')}; roteiro em {r['segundos']} s; banco restaurado em {seg_banco} s antes do roteiro (descontar do cronômetro)")
    if vez:
        eventos = ler_registro(arq)
        resumo = resumo_do_registro(eventos).get((vez["integrante"], vez["ordem"]))
        if resumo is None:
            print("!! esta vez não tem início no registro (o `armar --vez` não rodou): a tentativa ficou gravada, mas sem tempo")
        else:
            passado = resumo["segundos"] if resumo["segundos"] is not None else cronometro_da_vez(eventos, vez["integrante"], vez["ordem"], _relogio())["passado_s"]
            print(f"tentativa {resumo['tentativas']} gravada em {arq.name}; cronômetro em {_minutos(passado)}, já descontado o banco. "
                  f'Fala do facilitador: "{FALAS_DA_FERRAMENTA[2] if ok else FALAS_DA_FERRAMENTA[1]}"')
            if resumo["estourou"]:
                print(f"!! passou do limite de {LIMITE_S // 60} minutos: pelo protocolo o cenário fica não corrigido, sem tempo de fim")
    return 0 if ok else 1


# ! Alteração de IA - Revisar: (16/11/2026, F2) comando novo `entregar`: o fim do cenário de contrato. O facilitador deixa o
# comando esperando; no instante em que o integrante entrega, dá Enter, e a hora é gravada na mesma hora (evento `entrega`),
# antes de qualquer digitação. Só depois o comando pede a causa e o campo, confere que a causa é uma das 23 e grava a resposta
# com o corrigido calculado pela regra do agente (evento `resposta`). Causa fora da lista: pede de novo; linha vazia quer dizer
# que o integrante entregou algo que não está na lista, a entrega não vale e o tempo segue. Com `--causa` e `--campo` na linha de
# comando não há pergunta. A tela não diz se a resposta está certa.
# ! Motivo: plano, seção 4.4: o cronômetro do contrato para na entrega, certa ou errada, e não pode incluir o tempo de o
# facilitador digitar. Gravar a hora antes da digitação também protege a medida de uma queda do comando no meio: o próximo
# `entregar` acha o Enter sem resposta e pede só a causa e o campo. O acerto não aparece na tela porque o integrante a vê, e
# saber se acertou um cenário muda o que ele responde nos seguintes (na versão 1 o corrigido do contrato era preenchido depois).
def entregar(args: argparse.Namespace) -> int:
    vez = vez_do_cenario(*args.vez)
    rotulo = f"integrante {vez['integrante']}, cenário {vez['ordem']} de {len(cen.CENARIOS_DO_ENSAIO)}"
    if vez["tipo"] != "contrato":
        print(f"!! {rotulo} é de localizador: o fim dele é o `conferir --vez ... --seletor` que diz CORRIGIDO")
        return 2
    pasta = _pasta_do_registro(args)
    if pasta is None:
        return 2
    arq = pasta / NOME_DO_REGISTRO
    resumo = resumo_do_registro(ler_registro(arq)).get((vez["integrante"], vez["ordem"]))
    if resumo is None:
        print(f"!! {rotulo} não tem início no registro: rode antes o `armar --vez {vez['integrante']} {vez['ordem']}`")
        return 2
    if resumo["entregue"]:
        print(f"!! {rotulo} já tem entrega no registro; uma segunda não é gravada")
        return 2
    entrega = resumo["entrega_pendente"]
    if args.causa is not None:
        causa, campo = causa_da_lista(args.causa), campo_entregue(args.campo)
        if causa is None:
            print(f"!! {args.causa!r} não é uma das {len(DEFINICAO_DAS_CAUSAS)} causas da lista; nada foi gravado")
            return 2
        entrega = entrega or gravar_evento(arq, "entrega", vez)
    else:
        if entrega is not None:
            print(f"há um Enter de entrega às {entrega['hora'][11:19]} sem a causa e o campo: eles são pedidos agora, e a hora continua aquela")
        else:
            _ler("Enter no instante em que o integrante entregar a resposta (o cronômetro para no Enter)... ")
            entrega = gravar_evento(arq, "entrega", vez)
            print(f"cronômetro parado às {entrega['hora'][11:23]}")
        while True:
            texto = _ler(f"causa (uma das {len(DEFINICAO_DAS_CAUSAS)} da lista; linha vazia = a entrega não valeu e o tempo segue): ").strip()
            if not texto:
                gravar_evento(arq, "resposta", vez, causa=None, campo=None, corrigido=False, recusada=True)
                print(f'entrega desfeita: o cronômetro segue valendo. Fala do facilitador: "{FALAS_DA_FERRAMENTA[0]}"')
                return 1
            causa = causa_da_lista(texto)
            if causa is not None:
                break
            print(f"!! {texto!r} não é uma das {len(DEFINICAO_DAS_CAUSAS)} causas da lista; digite de novo")
        campo = campo_entregue(_ler("campo afetado (ou nenhum): "))
    gravar_evento(arq, "resposta", vez, causa=causa, campo=campo, corrigido=resultado_da_entrega(vez["cenario"], causa, campo), recusada=False)
    passado = round(entrega["relogio_s"] - resumo["inicio_s"], 3)
    print(f"{rotulo}: entrega gravada em {arq.name} ({causa}, campo {campo or 'nenhum'}); cronômetro em {_minutos(passado)}")
    if passado > LIMITE_S:
        print(f"!! passou do limite de {LIMITE_S // 60} minutos: pelo protocolo o cenário fica sem tempo de fim, e a resposta fica só no registro")
    return 0


# ! Alteração de IA - Revisar: (16/11/2026, F2) comando novo `treino`, com duas partes. `treino contrato` liga o modo do treino
# na CobaiaAPI, mostra o material na forma de um cenário de contrato (ficha, roteiro, contrato e as 23 causas), abre o navegador
# e, no Enter, pede a causa e o campo e diz a resposta certa. `treino seletor` abre produtos_api.php sem falha nenhuma e confere
# se o seletor do integrante acha o botão "Saiba Mais..." do primeiro produto (com `--seletor`, confere sem abrir janela). Nenhum
# dos dois grava início, entrega ou tentativa: com `--integrante`, fica só um evento `treino` no registro.
# ! Motivo: plano, seção 4.3: 15 minutos de treino sem cronômetro, com um cenário de contrato fora dos dez e um exercício de
# seletor numa página fora dos quatro roteiros de localizador, para a pessoa conhecer o material e a forma da resposta antes do
# primeiro cenário medido. O evento `treino` deixa provado, para a leitura, que cada integrante treinou.
def _seletor_acha_o_alvo(pagina, seletor: str) -> tuple[int, bool]:
    """Quantos elementos o seletor acha e se o primeiro deles é o botão do treino (o primeiro "Saiba Mais..." da página)."""
    achados = pagina.locator(seletor)
    quantos = achados.count()
    if not quantos:
        return 0, False
    return quantos, bool(achados.first.evaluate("(el, referencia) => el === document.querySelector(referencia)", TREINO_DE_SELETOR["referencia"]))


def treino(args: argparse.Namespace) -> int:
    import executar_fase4 as ex
    import navegador
    import taxonomia
    arq = None
    if args.integrante is not None:
        pasta = _pasta_do_registro(args)
        if pasta is None:
            return 2
        arq = pasta / NOME_DO_REGISTRO
    if not _cobaias_no_ar():
        print("!! as cobaias não responderam nas portas 8080 e 8000: suba com `python run.py` na raiz do repositório")
        return 2
    vez = {"integrante": args.integrante}
    endereco = urljoin(cen.BASE_PADRAO, TREINO_DE_SELETOR["pagina"])
    if args.parte == "contrato":
        t = TREINO_DE_CONTRATO
        ex.ligar_modo(t["modo"], t["campo"], args.token)
        try:
            print("treino de contrato, sem cronômetro: a falha do treino está ligada na CobaiaAPI para GET /api/produtos")
            print("\n== Ficha da falha (treino)")
            print(ficha_do_treino())
            print("\n== Roteiro do teste")
            print("\n".join(_passos_numerados(cen.cenario(t["cenario"]))))
            print("\n== Contrato esperado de cada produto em GET /api/produtos (o mesmo que o agente recebe)")
            print(ex._contrato_do_produto())
            print("\n== Resposta: uma causa desta lista e o campo afetado (ou nenhum)")
            print(", ".join(taxonomia.CAUSAS_RAIZ))
            with navegador.Navegador(canal=args.canal, headless=False) as nav:
                pagina = nav.nova_pagina()
                pagina.goto(endereco)
                print(f"\nnavegador {nav.versao()['navegador']} aberto para o treino, sem cronômetro")
                _ler("Enter quando o integrante disser a resposta do treino (fecha o navegador)... ")
        finally:
            ex.ligar_modo("normal", None, args.token)
        causa, campo = None, None
        while True:
            texto = _ler(f"causa do treino (uma das {len(DEFINICAO_DAS_CAUSAS)} da lista; linha vazia = sem resposta): ").strip()
            causa = causa_da_lista(texto)
            if not texto or causa is not None:
                break
            print(f'!! {texto!r} não é uma das {len(DEFINICAO_DAS_CAUSAS)} causas da lista. Fala do facilitador: "{FALAS_DA_FERRAMENTA[0]}"')
        if causa is not None:
            campo = campo_entregue(_ler("campo afetado (ou nenhum): "))
        acertou = causa == t["causa"] and campo == t["campo"]
        print(f"CobaiaAPI de volta ao modo normal. Só no treino a resposta é dita: a causa era {t['causa']} e o campo, {t['campo'] or 'nenhum'}"
              + ("" if causa is None else "; o integrante acertou" if acertou else "; o integrante respondeu outra coisa"))
        if arq is not None:
            gravar_evento(arq, "treino", vez, parte="contrato", causa=causa, campo=campo, acertou=acertou)
        return 0
    ex.ligar_modo("normal", None, args.token)
    alvo = TREINO_DE_SELETOR["alvo"]["nome"]
    if args.seletor:
        with navegador.Navegador(canal=args.canal) as nav:
            pagina = nav.nova_pagina()
            pagina.goto(endereco)
            pagina.wait_for_selector(TREINO_DE_SELETOR["referencia"], timeout=60000)
            quantos, achou = _seletor_acha_o_alvo(pagina, args.seletor)
        print(f"treino de seletor, sem cronômetro: {args.seletor!r} acha {quantos} elemento(s); "
              + (f'o primeiro é o botão "{alvo}" do primeiro produto' if achou else f'o primeiro não é o botão "{alvo}" do primeiro produto'))
        if arq is not None:
            gravar_evento(arq, "treino", vez, parte="seletor", seletor=args.seletor, achou=achou)
        return 0 if achou else 1
    print(f'treino de seletor, sem cronômetro e sem falha armada: escrever um seletor, CSS ou do Playwright, que ache o botão "{alvo}" do primeiro '
          "produto. No console do navegador (F12), document.querySelectorAll('<seletor>') mostra o que um seletor CSS acha.")
    ultimo, achou = None, False
    with navegador.Navegador(canal=args.canal, headless=False) as nav:
        pagina = nav.nova_pagina()
        pagina.goto(endereco)
        pagina.wait_for_selector(TREINO_DE_SELETOR["referencia"], timeout=60000)
        print(f"navegador {nav.versao()['navegador']} aberto para o treino, sem cronômetro")
        while True:
            seletor = _ler("seletor do integrante (linha vazia encerra o treino e fecha o navegador): ").strip()
            if not seletor:
                break
            try:
                quantos, achou = _seletor_acha_o_alvo(pagina, seletor)
            except Exception as e:  # noqa: BLE001 - seletor que o navegador não entende
                quantos, achou = 0, False
                print(f"  o navegador não entendeu o seletor: {' '.join(str(e).split())[:160]}")
            ultimo = seletor
            print(f"  {seletor!r} acha {quantos} elemento(s); " + ("o primeiro é o botão do treino: é assim que o `conferir` responde nos cenários que valem"
                                                              if achou else "o primeiro não é o botão do treino: pode tentar de novo"))
    if arq is not None:
        gravar_evento(arq, "treino", vez, parte="seletor", seletor=ultimo, achou=achou)
    return 0


# ! Alteração de IA - Revisar: (16/11/2026, F2) comando novo `planilha`: lê o registro e a planilha, preenche as células vazias
# dos cenários fechados, mostra o que preencheu e os avisos, e grava a planilha em UTF-8 com BOM só quando algo mudou. Sai 0 sem
# avisos, 1 com avisos e 2 se a planilha do sorteio não existe. `--sem-gravar` só mostra o que faria.
# ! Motivo: plano, seção 4.5: o facilitador escreve só as observações; o resto vem do registro, e o que discordar tem de aparecer
# na tela em vez de ser trocado em silêncio.
def planilha(args: argparse.Namespace) -> int:
    pasta = _pasta_do_registro(args)
    if pasta is None:
        return 2
    arq_planilha = Path(args.planilha) if args.planilha else PLANILHA
    if not arq_planilha.exists():
        print(f"!! {arq_planilha} não existe: grave a planilha do sorteio com `python linha_de_base_manual.py ordem --gravar`")
        return 2
    # ! Alteração de IA - Revisar: (16/11/2026, F2) a planilha é lida em UTF-8 com BOM e, se não for, na codificação do Windows.
    # ! Motivo: o facilitador escreve as observações com a planilha aberta no Excel, e o Excel pode regravar o CSV em cp1252;
    # sem isto o comando parava com UnicodeDecodeError na primeira letra acentuada (a leitura avaliar_fase5.py faz o mesmo).
    cru = arq_planilha.read_bytes()
    try:
        texto = cru.decode("utf-8-sig")
    except UnicodeDecodeError:
        texto = cru.decode("cp1252")
        print(f"{arq_planilha.name} estava na codificação do Windows (regravada pelo Excel); se algo for preenchido, ela volta em UTF-8 com BOM")
    texto = texto.replace("\r\n", "\n")
    resumo = resumo_do_registro(ler_registro(pasta / NOME_DO_REGISTRO))
    novo, preenchidas, avisos = preencher_planilha(texto, resumo)
    for linha in preenchidas:
        print(f"preenchido: {linha}")
    for aviso in avisos:
        print(f"!! {aviso}")
    for r in resumo.values():
        for aviso in r["avisos"]:
            print(f"(registro) integrante {r['integrante']}, ordem {r['ordem']}: {aviso}")
    abertos = [f"{n} {p}" for (n, p), r in resumo.items() if not r["fechado"]]
    if abertos:
        print(f"cenários armados e ainda abertos no registro (não entram na planilha): {', '.join(abertos)}")
    if novo != texto and not args.sem_gravar:
        arq_planilha.write_text(novo, encoding="utf-8-sig")
    print(f"{len(preenchidas)} linha(s) preenchida(s), {len(avisos)} aviso(s); planilha "
          + ("sem mudança" if novo == texto else "não gravada (--sem-gravar)" if args.sem_gravar else f"gravada em {arq_planilha}"))
    return 1 if avisos else 0


# ! Alteração de IA - Revisar: (16/11/2026, F2) comando novo `perfil`: faz as três perguntas ao integrante (o facilitador lê a
# pergunta na tela e digita a resposta), pede a anotação do facilitador sobre o código das cobaias e grava em participantes.json.
# As respostas também podem vir pelas opções. Quem já leu a lista dos cenários é avisado na tela, e o perfil é gravado assim mesmo.
# ! Motivo: plano, seção 4.1: as três perguntas antes de começar; quem já leu a lista não serve de integrante, mas, sem
# substituto, participa e a leitura declara. A decisão de trocar de integrante é do facilitador, não da ferramenta.
def perfil(args: argparse.Namespace) -> int:
    pasta = _pasta_do_registro(args)
    if pasta is None:
        return 2
    arq = pasta / NOME_DOS_PARTICIPANTES

    def sim_ou_nao(dado: str | None, pergunta: str) -> bool:
        resposta = _sim_ou_nao(dado)
        while resposta is None:
            resposta = _sim_ou_nao(_ler(f"{pergunta} [s/n] "))
        return resposta

    p = PERGUNTAS_DE_PERFIL
    pratica = (args.pratica or "").strip()
    while not pratica:
        pratica = _ler(f"{p['pratica']} (resposta curta, sem nome nem dado que identifique a pessoa) ").strip()
    respostas = {"pratica": pratica,
                 "ja_usou_as_ferramentas_do_desenvolvedor": sim_ou_nao(args.devtools, p["ja_usou_as_ferramentas_do_desenvolvedor"]),
                 "ja_leu_a_lista_dos_cenarios": sim_ou_nao(args.leu_a_lista, p["ja_leu_a_lista_dos_cenarios"]),
                 "conhece_o_codigo_das_cobaias": sim_ou_nao(args.conhece_o_codigo, ANOTACAO_DO_FACILITADOR["conhece_o_codigo_das_cobaias"])}
    respostas["o_que_conhece"] = ""
    if respostas["conhece_o_codigo_das_cobaias"]:
        respostas["o_que_conhece"] = (args.o_que_conhece or _ler("O que ele conhece (por exemplo: o HTML do site legado)? ")).strip()
    try:
        gravar_perfil(arq, args.integrante, respostas, regravar=args.regravar)
    except ValueError as e:
        print(f"!! {e}")
        return 2
    print(f"perfil do integrante {args.integrante} gravado em {arq}, sem o nome")
    if respostas["ja_leu_a_lista_dos_cenarios"]:
        print("!! este integrante já leu a lista dos cenários: pelo plano (seção 4.1) ele não serve de integrante; se não houver substituto, "
              "participa e isso fica declarado na leitura")
    return 0


# ! Alteração de IA - Revisar: (16/11/2026, F2) comandos novos `falas` e `folha` (imprimem o texto fixo do facilitador e a folha
# do integrante; `folha --gravar <arquivo>` grava a folha para imprimir) e `protocolo` (`--check` diz se os blocos colados no
# protocolo são os que o código gera; `--colar` cola).
# ! Motivo: os dois textos saem do código para as três sessões lerem e receberem a mesma coisa; o `--check` impede que o
# protocolo fique com um texto antigo depois de uma mudança aqui (o teste roda o mesmo conferidor).
def falas(args: argparse.Namespace) -> int:
    print(texto_do_facilitador(), end="")
    return 0


def folha(args: argparse.Namespace) -> int:
    texto = folha_do_integrante()
    if args.gravar:
        destino = Path(args.gravar)
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(texto, encoding="utf-8")
        print(f"folha do integrante gravada em {destino}")
        return 0
    print(texto, end="")
    return 0


def protocolo(args: argparse.Namespace) -> int:
    import analisar_fase3b as a3b
    if args.colar:
        colados, mudou = a3b.colar(PROTOCOLO, blocos_do_protocolo())
        print(f"{colados} bloco(s) colado(s) em {PROTOCOLO.name}; " + ("arquivo gravado" if mudou else "já estava em dia"))
    divergentes = conferir_protocolo()
    if divergentes:
        print(f"!! {PROTOCOLO.name}: bloco(s) que faltam ou diferem do que o código gera: {divergentes}; rode `protocolo --colar`")
        return 1
    print(f"{PROTOCOLO.name}: os blocos dos textos fixos estão iguais aos que o código gera")
    return 0


def ensaio(args: argparse.Namespace) -> int:
    print(passos_do_ensaio(), end="")
    return 0


# ! Alteração de IA - Revisar: (16/11/2026, decisões 135 e 136) comando novo `tutorial`: imprime o tutorial do integrante em
# Markdown; `--gravar` grava o Markdown no Memorial e `--check` diz se o gravado é o que o código gera. O texto vem de
# tutorial_do_integrante.py; desde a decisão 136 ele é o tutorial da sessão pela página, e a página que o mostra (com o botão
# Começar no fim) é a de cada integrante, montada pelo comando `paginas`.
# ! Motivo: o Eric pediu um tutorial para os integrantes entenderem o que fazer antes da sessão. Ele sai por comando, como a
# folha e o texto do facilitador, para os três receberem o mesmo texto e para os números dele (limite, cenários, causas) serem
# os do código.
def tutorial(args: argparse.Namespace) -> int:
    import tutorial_do_integrante as tut
    if args.gravar:
        for arq in tut.gravar():
            print(f"gravado: {arq}")
        return 0
    if args.check:
        fora = tut.conferir()
        if fora:
            print(f"!! o tutorial gravado difere do que o código gera em {fora}; rode `python linha_de_base_manual.py tutorial --gravar`")
            return 1
        print("o tutorial gravado no Memorial está igual ao que o código gera")
        return 0
    print(tut.em_markdown(), end="")
    return 0


# ! Alteração de IA - Revisar: (16/11/2026, decisão 136) comandos novos da sessão pelo artefato publicado, todos com o trabalho em
# sessao_pelo_artefato.py: `material` (captura aqui, com as cobaias no ar e sem modelo, o que o teste e o navegador registram em
# cada cenário e no treino, e grava em resultados_alvo/fase5_material/material.json; não regrava sem `--regravar`), `paginas`
# (monta a página de cada integrante a partir do material; `--gravar` grava e `--check` confere) e `importar` (traz para o
# registro da sessão o que a página de um integrante gravou).
# ! Motivo: o Eric decidiu que os integrantes fazem a sessão por uma página publicada, sem instalar nada, com tudo o que precisa
# rodar já rodado nesta máquina. Os comandos presenciais (`armar`, `entregar`, `conferir`) continuam como estavam.
def material(args: argparse.Namespace) -> int:
    import caminhos
    import sessao_pelo_artefato as spa
    if caminhos.RESULTADOS.name != "resultados_alvo":
        print('!! o material fica em resultados_alvo: defina RESULTADOS_DIR=resultados_alvo antes do comando (no PowerShell: $env:RESULTADOS_DIR = "resultados_alvo")')
        return 2
    arq = spa.arquivo_do_material()
    if arq.exists() and not args.regravar:
        print(f"!! {arq} já existe: o material das sessões não é regravado sem --regravar (as três páginas saem dele)")
        return 2
    if not _cobaias_no_ar():
        print("!! as cobaias não responderam nas portas 8080 e 8000: suba com `python run.py` na raiz do repositório")
        return 2
    dado = spa.capturar_material(canal=args.canal, token=args.token, saida=args.saida, forma=args.forma)
    spa.gravar_material(dado, arq)
    print(f"material de {len(dado['cenarios'])} cenários e do treino gravado em {arq} (navegador {dado['navegador']}, banco {dado['hash_do_banco']})")
    return 0


def paginas(args: argparse.Namespace) -> int:
    import sessao_pelo_artefato as spa
    if args.gravar:
        for arq in spa.gravar_paginas():
            print(f"gravado: {arq}")
        return 0
    fora = spa.conferir_paginas()
    if fora:
        print(f"!! páginas gravadas que diferem do que o código gera: {fora}; rode `python linha_de_base_manual.py paginas --gravar`")
        return 1
    print("as páginas das sessões estão iguais às que o código gera a partir do material")
    return 0


def _roteiro_de_verdade(args: argparse.Namespace):
    """A função que roda aqui o roteiro do agente com o seletor de um integrante (o mesmo trabalho do `conferir`) e diz se
    ele chegou ao fim sem erro."""
    import navegador

    def confere(cenario_id: str, seletor: str) -> bool:
        roteiro, q = roteiro_do_integrante(cenario_id, seletor)
        _restaurar_banco()
        with navegador.Navegador(canal=args.canal) as nav:
            pagina = nav.nova_pagina()
            cen.armar_quebra(pagina, q, args.forma)
            r = cen.rodar_cenario(roteiro, pagina, None, capturar=False, tempo_limite_ms=cen.TEMPO_LIMITE_QUEBRA_MS)
            pagina.close()
        return cen.task_success(r)
    return confere


# ! Alteração de IA - Revisar: (17/11/2026, ficha 77, decisão 137) `_posicoes_a_anular` lê o que o facilitador escreveu no `--anular`
# do comando `importar`.
# ! Motivo: a decisão de anular é por posição do cenário na ordem do integrante, que é o que o comando mostra ao lado de cada
# aviso; `nenhum` existe para a decisão de não anular ficar escrita, e não subentendida pela falta da opção.
def _posicoes_a_anular(texto: str) -> set[int] | None:
    """As posições do `--anular` ("4,9" vira {4, 9}; "nenhum" vira o conjunto vazio); None se o texto não é isso."""
    limpo = _sem_acento((texto or "").strip().lower())
    if limpo == "nenhum":
        return set()
    partes = [p.strip() for p in limpo.split(",")]
    if not partes or not all(p.isdigit() for p in partes):
        return None
    return {int(p) for p in partes}


def importar(args: argparse.Namespace) -> int:
    import sessao_pelo_artefato as spa
    pasta = _pasta_do_registro(args)
    if pasta is None:
        return 2
    try:
        sessao = spa.ler_codigo(Path(args.arquivo).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as e:
        print(f"!! {args.arquivo}: {e}")
        return 2
    # ! Alteração de IA - Revisar: (17/11/2026, ficha 77, decisão 137) antes de qualquer gravação, o comando mostra os avisos que o
    # integrante deixou (a posição do cenário e o texto, sem tempo nenhum) e só segue com `--anular`, que diz quais posições
    # têm a linha anulada, ou `--anular nenhum`.
    # ! Motivo: a regra L14 só anula uma medida por falha do protocolo anotada na hora, antes de qualquer número ser lido. O
    # facilitador decide aqui, pelo motivo escrito, e a decisão fica gravada no registro antes de o comando `planilha` mostrar
    # os tempos; se a decisão ficasse para depois da planilha, a linha poderia ser tirada depois de vista.
    try:
        avisos_do_integrante = spa.ocorrencias_da_sessao(sessao)
    except ValueError as e:
        print(f"!! a sessão não entrou: {e}")
        return 2
    anular = None
    if args.anular is not None:
        anular = _posicoes_a_anular(args.anular)
        if anular is None:
            print(f"!! --anular {args.anular!r}: escreva as posições separadas por vírgula (por exemplo `--anular 4,9`) ou `--anular nenhum`")
            return 2
    if avisos_do_integrante and anular is None:
        print(f"o integrante {sessao.get('integrante')} deixou {len(avisos_do_integrante)} aviso(s) de que algo de fora atrapalhou um cenário (regra L14):")
        for posicao, texto in avisos_do_integrante:
            print(f"  posição {posicao}: {texto}")
        print("Nada foi gravado. Decida agora, só pelo motivo escrito e antes de ver qualquer tempo, quais avisos são falha do protocolo\n"
              "(equipamento que travou, interrupção de fora), e rode de novo com `--anular` e as posições que têm a linha anulada,\n"
              "separadas por vírgula, ou com `--anular nenhum`.")
        return 2
    confere = None
    if args.sem_conferir:
        print("sem conferir no roteiro de verdade: vale o que a página conferiu (use só no ensaio)")
    else:
        if not _cobaias_no_ar():
            print("!! as cobaias não responderam nas portas 8080 e 8000: suba com `python run.py`, ou use --sem-conferir no ensaio")
            return 2
        confere = _roteiro_de_verdade(args)
    try:
        perfil_ = spa.perfil_da_sessao(sessao, conhece_o_codigo=args.conhece_o_codigo == "sim", o_que_conhece=args.o_que_conhece or "")
        resultado = spa.importar_sessao(sessao, pasta / NOME_DO_REGISTRO, conferir_seletor=confere, anular=anular)
        gravar_perfil(pasta / NOME_DOS_PARTICIPANTES, sessao["integrante"], perfil_, regravar=args.regravar_perfil)
    except ValueError as e:
        print(f"!! a sessão não entrou: {e}")
        return 2
    for aviso in resultado["avisos"]:
        print(f"!! {aviso}")
    for posicao, texto in avisos_do_integrante:
        print(f"aviso do integrante na posição {posicao}: linha {'ANULADA' if posicao in (anular or set()) else 'mantida'} ({texto})")
    print(f"sessão do integrante {sessao['integrante']} trazida para {pasta / NOME_DO_REGISTRO}: {resultado['eventos']} eventos, {resultado['cenarios']} cenários; "
          f"perfil em {NOME_DOS_PARTICIPANTES}. Falta rodar `python linha_de_base_manual.py planilha`")
    if perfil_["ja_leu_a_lista_dos_cenarios"]:
        print("!! este integrante respondeu que já leu a lista dos cenários: isso fica declarado na leitura (plano, seção 4.1)")
    return 0


def desarmar(args: argparse.Namespace) -> int:
    import executar_fase4 as ex
    ex.ligar_modo("normal", None, args.token)
    print("CobaiaAPI de volta ao modo normal; feche o navegador do integrante se ainda estiver aberto")
    return 0


def ordem(args: argparse.Namespace) -> int:
    ordens = ordem_dos_integrantes(args.integrantes, args.semente)
    for n, ids in ordens.items():
        print(f"integrante {n}: " + ", ".join(f"{i}. {cid}" for i, cid in enumerate(ids, 1)))
    if args.gravar:
        texto = planilha_modelo(ordens)
        destino = PLANILHA
        if destino.exists() and destino.read_text(encoding="utf-8-sig") != texto:
            destino = destino.with_suffix(".nova.csv")
            print(f"!! {PLANILHA.name} já tem anotações e foi mantida; a planilha em branco foi para {destino.name}")
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(texto, encoding="utf-8-sig")
        print(f"planilha gravada em {destino}")
    return 0


# ! Alteração de IA - Revisar: (16/11/2026, F2) a linha de comando ganha os comandos `entregar`, `treino`, `planilha`, `perfil`,
# `falas`, `folha`, `protocolo` e `ensaio`, e `armar` e `conferir` ganham `--registro`; as opções e os padrões dos quatro comandos da
# versão 1 não mudam.
# ! Motivo: `--registro <pasta>` deixa o ensaio do facilitador e a fumaça gravarem numa pasta de teste, e não no registro da
# sessão de verdade.
def montar_parser() -> argparse.ArgumentParser:
    import executar_fase4 as ex
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="comando", required=True)
    ajuda_do_registro = f"a pasta do registro da sessão, dentro de resultados_alvo (padrão {PASTA_DA_SESSAO}) ou um caminho inteiro"
    p = sub.add_parser("ordem", help="a ordem sorteada dos dez cenários de cada integrante")
    p.add_argument("--integrantes", type=int, default=INTEGRANTES)
    p.add_argument("--semente", type=int, default=SEMENTE_DA_ORDEM)
    p.add_argument("--gravar", action="store_true", help=f"grava a planilha modelo em {PLANILHA.name}")
    p.set_defaults(funcao=ordem)
    for nome, funcao, ajuda in (("armar", armar, "liga a falha do cenário e abre o navegador do integrante"),
                                ("conferir", conferir, "roda o roteiro de localizador com o seletor do integrante")):
        p = sub.add_parser(nome, help=ajuda)
        qual = p.add_mutually_exclusive_group(required=True)
        qual.add_argument("--vez", type=int, nargs=2, metavar=("INTEGRANTE", "POSICAO"), help="o cenário da vez, pela ordem sorteada")
        qual.add_argument("--cenario", help="o cenário pelo nome (ensaio do facilitador)")
        p.add_argument("--forma", choices=cen.FORMAS_DE_QUEBRA, default="php", help="como armar a quebra de localizador (padrão php)")
        p.add_argument("--canal", default="chromium")
        p.add_argument("--token", default=ex.TOKEN_PADRAO, help="X-Admin-Token da CobaiaAPI")
        p.add_argument("--saida", default=SAIDA_DO_ENSAIO, help="a corrida de onde sai a ficha da falha")
        p.add_argument("--registro", default=PASTA_DA_SESSAO, help=ajuda_do_registro)
        if nome == "conferir":
            p.add_argument("--seletor", help="o seletor do integrante; sem ele, roda com o localizador quebrado e mostra a ficha da falha")
        p.set_defaults(funcao=funcao)
    p = sub.add_parser("entregar", help="contrato: grava o fim do cenário no Enter e depois pede a causa e o campo")
    p.add_argument("--vez", type=int, nargs=2, metavar=("INTEGRANTE", "POSICAO"), required=True)
    p.add_argument("--causa", help="a causa entregue (sem ela, o comando espera o Enter e pergunta)")
    p.add_argument("--campo", help="o campo entregue (padrão nenhum)")
    p.add_argument("--registro", default=PASTA_DA_SESSAO, help=ajuda_do_registro)
    p.set_defaults(funcao=entregar)
    p = sub.add_parser("treino", help="o treino sem cronômetro, fora dos dez cenários")
    p.add_argument("parte", choices=("contrato", "seletor"))
    p.add_argument("--integrante", type=int, choices=range(1, INTEGRANTES + 1), help="grava no registro que este integrante treinou")
    p.add_argument("--seletor", help="treino de seletor: confere este seletor sem abrir janela")
    p.add_argument("--canal", default="chromium")
    p.add_argument("--token", default=ex.TOKEN_PADRAO, help="X-Admin-Token da CobaiaAPI")
    p.add_argument("--registro", default=PASTA_DA_SESSAO, help=ajuda_do_registro)
    p.set_defaults(funcao=treino)
    p = sub.add_parser("planilha", help="preenche a planilha a partir do registro, sem trocar célula preenchida")
    p.add_argument("--registro", default=PASTA_DA_SESSAO, help=ajuda_do_registro)
    p.add_argument("--planilha", help=f"outra planilha no lugar de {PLANILHA.name} (ensaio)")
    p.add_argument("--sem-gravar", action="store_true", help="só mostra o que seria preenchido e os avisos")
    p.set_defaults(funcao=planilha)
    p = sub.add_parser("perfil", help="as três perguntas de perfil do integrante, sem o nome")
    p.add_argument("--integrante", type=int, required=True)
    p.add_argument("--pratica", help="a resposta sobre o tempo de prática")
    for opcao, ajuda in (("--devtools", "já usou as ferramentas do desenvolvedor"), ("--leu-a-lista", "já leu a lista dos cenários"),
                         ("--conhece-o-codigo", "anotação do facilitador: escreveu ou conhece o código das cobaias")):
        p.add_argument(opcao, choices=("sim", "nao"), help=ajuda)
    p.add_argument("--o-que-conhece", help="o que o integrante conhece do código das cobaias")
    p.add_argument("--regravar", action="store_true", help="troca o perfil já gravado deste integrante")
    p.add_argument("--registro", default=PASTA_DA_SESSAO, help=ajuda_do_registro)
    p.set_defaults(funcao=perfil)
    p = sub.add_parser("falas", help="imprime o texto fixo do facilitador")
    p.set_defaults(funcao=falas)
    p = sub.add_parser("folha", help="imprime a folha do integrante, com a definição das 23 causas")
    p.add_argument("--gravar", metavar="ARQUIVO", help="grava a folha neste arquivo, para imprimir")
    p.set_defaults(funcao=folha)
    p = sub.add_parser("protocolo", help="confere ou cola no protocolo os textos fixos gerados")
    modo = p.add_mutually_exclusive_group(required=True)
    modo.add_argument("--check", action="store_true")
    modo.add_argument("--colar", action="store_true")
    p.set_defaults(funcao=protocolo)
    p = sub.add_parser("ensaio", help="imprime o passo a passo do ensaio do facilitador")
    p.set_defaults(funcao=ensaio)
    p = sub.add_parser("material", help="captura aqui o material dos dez cenários e do treino para as páginas da sessão")
    p.add_argument("--regravar", action="store_true", help="captura de novo e grava por cima do material que já existe")
    p.add_argument("--forma", choices=cen.FORMAS_DE_QUEBRA, default="php", help="como armar a quebra de localizador (padrão php)")
    p.add_argument("--canal", default="chromium")
    p.add_argument("--token", default=ex.TOKEN_PADRAO, help="X-Admin-Token da CobaiaAPI")
    p.add_argument("--saida", default=SAIDA_DO_ENSAIO, help="a corrida de onde sai a ficha da falha")
    p.set_defaults(funcao=material)
    p = sub.add_parser("paginas", help="as páginas das sessões, uma por integrante, montadas do material")
    modo = p.add_mutually_exclusive_group(required=True)
    modo.add_argument("--gravar", action="store_true", help="grava as três páginas em Documentacao/dashboard")
    modo.add_argument("--check", action="store_true", help="confere se as três páginas gravadas são as que o código gera")
    p.set_defaults(funcao=paginas)
    p = sub.add_parser("importar", help="traz para o registro a sessão que a página de um integrante gravou")
    p.add_argument("--arquivo", required=True, help="o arquivo com o código da sessão (SESSAO3...) ou com o JSON lido do banco da página")
    p.add_argument("--conhece-o-codigo", choices=("sim", "nao"), required=True, help="anotação do facilitador: o integrante escreveu ou conhece o código das cobaias")
    p.add_argument("--o-que-conhece", help="o que o integrante conhece do código das cobaias")
    p.add_argument("--sem-conferir", action="store_true", help="não roda o roteiro de verdade com os seletores (só no ensaio)")
    p.add_argument("--anular", help="quando o integrante deixou aviso: as posições que têm a linha anulada, separadas por vírgula, ou `nenhum` (regra L14)")
    p.add_argument("--regravar-perfil", action="store_true", help="troca o perfil já gravado deste integrante")
    p.add_argument("--forma", choices=cen.FORMAS_DE_QUEBRA, default="php", help="como armar a quebra de localizador na conferência (padrão php)")
    p.add_argument("--canal", default="chromium")
    p.add_argument("--registro", default=PASTA_DA_SESSAO, help=ajuda_do_registro)
    p.set_defaults(funcao=importar)
    p = sub.add_parser("tutorial", help="o tutorial que os integrantes leem antes de começar")
    modo = p.add_mutually_exclusive_group()
    modo.add_argument("--gravar", action="store_true", help="grava o Markdown do tutorial no Memorial")
    modo.add_argument("--check", action="store_true", help="confere se o Markdown gravado é o que o código gera")
    p.set_defaults(funcao=tutorial)
    p = sub.add_parser("desarmar", help="volta a CobaiaAPI ao modo normal")
    p.add_argument("--token", default=ex.TOKEN_PADRAO)
    p.set_defaults(funcao=desarmar)
    return ap


def main() -> int:
    args = montar_parser().parse_args()
    return args.funcao(args)


if __name__ == "__main__":
    sys.exit(main())
