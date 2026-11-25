#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (16/11/2026, Fase 5, decisão 135): o tutorial que os três integrantes da linha de base
# manual leem antes da sessão. O conteúdo é escrito uma vez, em blocos (`secoes`), e dele saem o Markdown que fica no Memorial
# (`em_markdown`) e o trecho de página (`secoes_em_html`) que abre a página da sessão de cada integrante.
# ! Motivo: o Eric pediu um tutorial para as pessoas entenderem o que fazer. É material que a pessoa lê antes de ser medida, e
# por isso tem três amarras: os três recebem o mesmo texto; os números (cenários, limite, minutos do dia, as 23 causas) vêm das
# constantes do ajudante, e não de digitação; e nada nele vem das cobaias: os exemplos são de um sistema inventado (uma agenda de
# consultas e um formulário de cadastro), e o exemplo resolvido usa uma causa que não é resposta de nenhum cenário nem do
# treino. O teste `teste_tutorial_do_integrante_explica_a_sessao_pela_pagina_sem_entregar_resposta` confere as três.
# ! Alteração de IA - Revisar: (16/11/2026, decisão 136) o tutorial foi reescrito para a sessão feita pela página publicada: saem o
# facilitador ao lado, as ferramentas do desenvolvedor do navegador e o bloco de notas; entram o material que a página mostra
# (a chamada à API, o contrato, a foto da tela, o HTML da página e a caixa Testar seletor), os avisos que a página dá e, no fim,
# a seção que explica o botão Começar. A página avulsa do tutorial deixou de existir: ele agora abre a página de cada sessão.
# ! Motivo: o Eric decidiu que os integrantes fazem a sessão por um endereço, sem instalar nada, com tudo o que precisa rodar já
# rodado na máquina do projeto, e pediu o botão Começar no fim do tutorial, bem explicado. Com o tutorial antigo a pessoa leria
# instruções de uma sessão presencial que não vai acontecer.
"""O tutorial do integrante da linha de base manual (Fase 5): conteúdo, Markdown e o trecho que abre a página da sessão."""
from __future__ import annotations

import html
import re
from pathlib import Path

import cenarios_fase4 as cen
import linha_de_base_manual as lbm
import taxonomia

RAIZ = Path(__file__).resolve().parents[3]
ARQUIVO_MD = RAIZ / "Documentacao" / "memorial" / "5-metodo-e-ferramental" / "tutorial-do-integrante.md"
TITULO = "Tutorial do integrante"
ID_DO_BOTAO = "botao-comecar"
# a documentação que o integrante pode consultar durante a sessão
DOCUMENTACAO = {"seletores_css": "https://developer.mozilla.org/pt-BR/docs/Web/CSS/CSS_selectors"}
# a causa do exemplo resolvido: uma das 23, fora das respostas dos dez cenários e do treino (o teste confere)
CAUSA_DO_EXEMPLO = "formato_de_data_divergente"


def teto_da_sessao() -> str:
    """Quanto a sessão leva se todo cenário for até o limite: abertura, treino e fecho do plano mais os cenários vezes o limite."""
    minutos = sum(lbm.MINUTOS_DA_SESSAO.values()) + len(cen.CENARIOS_DO_ENSAIO) * lbm.LIMITE_S // 60
    return f"{minutos // 60}h{minutos % 60:02d}"


# ! Alteração de IA - Revisar: (16/11/2026, decisões 135 e 136) `secoes`: o conteúdo do tutorial. Cada seção tem um id (a âncora da
# página), um título e blocos: parágrafo ("p"), lista ("ul", "ol"), aviso, bloco de código com legenda, tabela, a linha do tempo
# da sessão ("tempo"), os dois tipos de cenário lado a lado ("par"), termo e explicação ("termos"), a lista das 23 causas
# ("causas") e o botão Começar ("botao"). O texto usa só três marcas: `código`, **destaque** e [texto](endereço).
# ! Motivo: com o conteúdo em blocos, o Markdown e a página não podem dizer coisas diferentes. A ordem é a de quem vai ser
# medido: primeiro o que não fazer antes, depois como é a sessão e como ler o material, depois como resolver cada tipo de
# cenário, e por último o que o botão faz, para ele só ser clicado por quem leu o resto.
def secoes() -> list[dict]:
    cenarios, causas, limite = len(cen.CENARIOS_DO_ENSAIO), len(lbm.DEFINICAO_DAS_CAUSAS), lbm.LIMITE_S // 60
    m, avisos = lbm.MINUTOS_DA_SESSAO, lbm.AVISOS_DA_PAGINA
    perguntas = [c["pergunta"] for _, c in sorted(taxonomia.CLASSES.items())]
    return [
        {"id": "antes", "titulo": "Antes de tudo: quatro combinados", "blocos": [
            ("p", "Este tutorial é o único material de preparo, e é igual para os três integrantes. Leia com calma: o botão Começar fica no fim da página."),
            ("ol", [
                "Até a sua sessão acabar, não abra o repositório do projeto, o painel do projeto, o README nem o documento do TCC. As respostas dos "
                "cenários estão lá, e quem já leu não pode participar.",
                "Não converse sobre a sessão com os outros integrantes: nem antes da sua, nem depois, enquanto houver sessão por fazer.",
                "Não use assistente de IA. O que se quer saber é quanto tempo uma pessoa leva.",
                f"Faça num computador, com teclado, e de uma vez só: reserve {teto_da_sessao()} sem interrupção.",
            ]),
            ("aviso", "Se você já leu", "Se já abriu algum desses materiais e viu a lista dos cenários ou as respostas, avise o facilitador antes de "
                                        "começar. Não é problema seu: ele só precisa saber."),
        ]},
        # o id não é "sessao" porque a página da sessão já usa esse id na área em que as telas aparecem
        {"id": "o-que-e", "titulo": "O que é a sessão", "blocos": [
            ("p", "O projeto construiu um agente que conserta testes automatizados quando eles quebram. Para saber se ele vale a pena, o projeto compara "
                  "o tempo do agente com o tempo de uma pessoa fazendo o mesmo conserto à mão. Você é essa pessoa: a linha de base manual."),
            ("p", f"São {cenarios} cenários. Em cada um, um teste automatizado de um site de teste parou ou acusou um problema, porque uma falha foi "
                  "armada de propósito. Tudo isso já rodou na máquina do projeto: você recebe o registro do que aconteceu e diz o que quebrou. Mede-se "
                  "quanto tempo cada cenário leva e se a resposta está certa."),
            ("p", "O que se mede é o trabalho feito à mão, não você. O seu nome não entra em nenhum arquivo: nos registros você é o integrante 1, 2 ou 3."),
            ("tempo", [
                ("Antes de começar", f"{m['abertura']} min", "este tutorial e três perguntas sobre a sua experiência"),
                ("Treino, sem cronômetro", f"{m['treino']} min", "um cenário de cada tipo, fora dos que valem; só aqui a página diz a resposta certa"),
                (f"Os {cenarios} cenários", f"até {limite} min cada", "com pausa livre entre um e outro"),
                ("Fim", f"{m['fecho']} min", "a página diz se guardou a sua sessão"),
            ]),
            ("p", f"Reserve {teto_da_sessao()}: é quanto a sessão leva se todo cenário for até o limite."),
        ]},
        {"id": "cenario", "titulo": "Como é um cenário", "blocos": [
            ("p", "Cada cenário é uma tela desta página. Nela você recebe:"),
            ("ul", [
                "a **ficha da falha**: a frase que o teste automático acusou;",
                "o **roteiro do teste**, passo a passo, com o valor de cada preenchimento;",
                "o **material registrado** quando o teste rodou: no cenário de contrato, a chamada à API com a resposta que chegou, o contrato esperado "
                "e a foto da tela; no de localizador, a foto da tela e o HTML da página no passo que quebrou;",
                f"nos cenários de contrato, a **lista das {causas} causas**.",
            ]),
            ("p", "Há dois tipos de cenário, e a resposta de cada um é diferente."),
            ("par", [
                ("Cenário de contrato", [
                    "O site pede dados a uma API, e a resposta da API saiu do combinado.",
                    f"Você responde com **uma causa** da lista de {causas} e **o campo** afetado, ou `nenhum`.",
                    "A entrega é uma só. O tempo para na entrega, certa ou errada, e a página não diz se você acertou.",
                ]),
                ("Cenário de localizador", [
                    "O teste procura um elemento da página por um seletor, e o seletor não acha mais o elemento. No roteiro, o passo que quebrou vem marcado.",
                    "Você responde com **um seletor CSS novo** que ache o elemento.",
                    "A página confere na hora. Se passar, o tempo para. Se não passar, o tempo segue e você tenta de novo.",
                ]),
            ]),
            ("p", f"O tempo de um cenário só começa quando você clica em **Abrir o cenário**. O limite é de {limite} minutos: passou disso, a página "
                  "fecha o cenário, e ele conta como não resolvido. Entre um cenário e outro a pausa é livre, e o tempo não corre."),
            # ! Alteração de IA - Revisar: (17/11/2026, ficha 77, decisão 137) o tutorial passa a dizer que, no fim de cada cenário, a
            # página pergunta se algo de fora atrapalhou, o que conta, o que não conta e quem decide o que fazer com o aviso.
            # ! Motivo: sem facilitador ao lado, só a pessoa sabe que o computador travou ou que foi interrompida, e o plano
            # (regra L14) só tira um cenário da conta se a falha for anotada na hora. Dito antes, no tutorial, os três
            # integrantes usam a caixa pelo mesmo critério.
            ("aviso", "Se algo de fora atrapalhar", f"No fim de cada cenário, com o tempo já parado, a página pergunta: **{lbm.PERGUNTA_DA_OCORRENCIA}** "
                                                    f"Escreva ali, na hora, só o que não é do cenário: {lbm.O_QUE_CONTA_COMO_OCORRENCIA}. Não entra: "
                                                    f"{lbm.O_QUE_NAO_CONTA_COMO_OCORRENCIA}. Se nada atrapalhou, deixe em branco. O facilitador lê o aviso "
                                                    "antes de ver os tempos e decide se aquele cenário fica fora da conta."),
        ]},
        {"id": "avisos", "titulo": "O que a página avisa", "blocos": [
            ("p", "Não há ninguém ao lado para tirar dúvida durante um cenário. A página só mostra estes avisos:"),
            ("termos", [
                (avisos["dois_minutos"], f"quando faltam {lbm.AVISO_FINAL_S // 60} minutos para o limite do cenário."),
                (avisos["esgotado"], "quando o limite acabou. O cenário fecha sozinho."),
                (avisos["nao_passou"], "no localizador, quando o seu seletor não achou o elemento certo."),
                (avisos["passou"], "no localizador, quando o seu seletor achou o elemento certo."),
            ]),
            ("p", "No cenário de contrato a página só confirma que recebeu a resposta. Dúvida sobre as regras? Pergunte ao facilitador antes de clicar "
                  "em Começar."),
        ]},
        {"id": "regras", "titulo": "O que pode e o que não pode", "blocos": [
            ("p", f"**Pode:** {lbm.PODE_NA_PAGINA}."),
            ("p", f"**Não pode:** {lbm.NAO_PODE_NA_PAGINA}."),
            ("p", f"A documentação que você pode consultar: [seletores CSS, na MDN]({DOCUMENTACAO['seletores_css']})."),
        ]},
        {"id": "material", "titulo": "Como ler o material de um cenário", "blocos": [
            ("termos", [
                ("A chamada à API", "o que o site pediu e o que a API respondeu: o código de status, quanto tempo levou e o corpo da resposta, como chegou."),
                ("O contrato", "a lista dos campos que a resposta tem de trazer, com o tipo de cada um."),
                ("A foto da tela", "como a página do site estava quando o teste parou ou terminou."),
                ("O HTML da página", "no cenário de localizador, o HTML da página no passo que quebrou, uma linha por elemento, com o `id`, as classes "
                                     "e os outros atributos de cada um. Use a busca do navegador (Ctrl+F) para achar um texto."),
                ("A caixa Testar seletor", "diz quantos elementos do HTML o seu seletor acha e mostra o primeiro. Testar não conta como tentativa: só "
                                           "o botão Entregar conta."),
            ]),
        ]},
        {"id": "contrato", "titulo": "Cenário de contrato, passo a passo", "blocos": [
            ("p", "Um contrato é a lista dos campos que a resposta de uma API tem de trazer: o nome de cada campo e o tipo dele. A página mostra o "
                  "contrato e a resposta que chegou. O trabalho é achar onde as duas diferem."),
            ("ol", [
                "Leia a ficha da falha. Ela diz o que o teste automático viu de errado, e é a melhor pista de onde olhar.",
                "Olhe o código de status e o tempo da chamada. 200 quer dizer que a API respondeu sem erro; os que começam com 4 ou 5 são erro.",
                "Olhe o corpo da resposta e compare com o contrato, campo a campo.",
                f"Procure na lista das {causas} causas a linha que descreve o que você achou.",
                "Escolha a causa e escreva o campo onde o problema está. Se o problema é da resposta inteira, e não de um campo, o campo é `nenhum`.",
            ]),
            ("p", "Na comparação, estas seis perguntas cobrem tudo o que pode estar errado:"),
            ("ul", perguntas),
            ("aviso", "Um exemplo, de outro sistema", "Uma agenda de consultas, que não tem nada a ver com a sessão. Serve só para mostrar o jeito de "
                                                      "comparar e de responder."),
            ("codigo", "O contrato de cada consulta, como ele aparece na página",
             "id: inteiro | paciente: texto | data: texto, no formato AAAA-MM-DD | confirmada: booleano"),
            ("codigo", "A resposta que chegou", '[{"id": 7, "paciente": "Ana Lima", "data": "19/11/2026", "confirmada": true}]'),
            ("p", "O status é 200 e o corpo é JSON inteiro. Os quatro campos vieram, com os nomes do contrato. O que difere é o campo `data`: o "
                  "contrato pede ano, mês e dia, e a resposta trouxe dia, mês e ano. Na lista, a linha que descreve isso é a de "
                  f"`{CAUSA_DO_EXEMPLO}`: {lbm.DEFINICAO_DAS_CAUSAS[CAUSA_DO_EXEMPLO]}."),
            ("codigo", "O que você responde", f"causa: {CAUSA_DO_EXEMPLO}\ncampo: data"),
        ]},
        {"id": "localizador", "titulo": "Cenário de localizador, passo a passo", "blocos": [
            ("p", "Um teste automatizado acha cada elemento da página por um seletor: um texto curto que descreve o elemento. Quando a página muda, o "
                  "seletor antigo pode não achar mais nada, e o teste para. No roteiro, o passo que quebrou vem marcado, com o seletor que deixou de "
                  "funcionar."),
            ("ol", [
                "Leia o roteiro até o passo marcado. Ele diz o que o teste ia fazer ali: clicar, preencher ou esperar um elemento.",
                "Olhe a foto da tela e ache o elemento que o passo usa.",
                "Ache esse elemento no HTML da página e veja o que o identifica.",
                "Escreva um seletor CSS novo.",
                "Use a caixa Testar seletor. O melhor é o seletor achar um elemento só: o que você quer.",
                "Clique em Entregar.",
            ]),
            ("p", "Há vários jeitos de escrever um seletor CSS. Os exemplos são de um formulário de cadastro inventado."),
            ("tabela", ["O que identifica o elemento", "Seletor", "Como se lê"], [
                ["o `id`", "`#salvar`", "o elemento com o id salvar"],
                ["uma classe", "`button.confirmar`", "o botão com a classe confirmar"],
                ["um atributo", "`input[name=email]`", "o campo com o atributo name igual a email"],
                ["um pedaço de um atributo", '`a[href*="ajuda"]`', "o link cujo endereço contém ajuda"],
                ["o lugar na página", "`#cadastro > button`", "o botão que é filho direto do elemento com o id cadastro"],
                ["a posição entre iguais", "`table tr:nth-child(2) td:first-child`", "a primeira célula da segunda linha da tabela"],
            ]),
            ("p", "O que quer dizer passar: o primeiro elemento que o seu seletor acha no HTML tem de ser o elemento do passo que quebrou. Depois da "
                  "sessão, o projeto roda o teste de verdade com o seletor que passou, e é esse resultado que vale."),
        ]},
        {"id": "causas", "titulo": f"As {causas} causas", "blocos": [
            ("p", "É a mesma lista que aparece nos cenários de contrato. Lá você escolhe uma delas."),
            ("causas",),
        ]},
        {"id": "duvidas", "titulo": "Perguntas comuns", "blocos": [
            ("termos", [
                ("Vou saber se acertei?", "No cenário de localizador, sim, na hora. No de contrato, não: saber se acertou um cenário mudaria o que você "
                                          "responde nos seguintes."),
                ("E se eu não souber a resposta?", "No contrato, a entrega é uma só e o tempo para nela, certa ou errada; sem entrega até o limite, o "
                                                   "cenário conta como não resolvido. No localizador, você pode tentar quantas vezes couberem no limite. "
                                                   "Nos dois há o botão Encerrar sem resposta."),
                ("Posso parar no meio?", "Entre um cenário e outro, sim: a página guarda onde você parou. Com um cenário aberto, não: o tempo continua "
                                         "correndo mesmo com a página fechada."),
                ("E se o computador travar ou alguém me interromper?", "Siga como der: o tempo do cenário não para. No fim dele, escreva o que houve na "
                                                                       "caixa do aviso, antes de abrir o próximo. Se a página fechou, abra o mesmo endereço "
                                                                       "no mesmo navegador: ela volta de onde parou."),
                ("O que fica gravado sobre mim?", "As respostas às três perguntas do começo, o tempo e a resposta de cada cenário, o que você escrever na "
                                                  "caixa do aviso e o tipo de navegador, pelo número do integrante. O nome, não."),
                ("Posso contar para os outros como foi?", "Só depois que as três sessões acabarem."),
            ]),
        ]},
        {"id": "glossario", "titulo": "Palavras que aparecem na sessão", "blocos": [
            ("termos", [
                ("API", "o serviço que entrega os dados ao site. O site chama a API e mostra na tela o que ela responde."),
                ("JSON", "o formato de texto em que a API responde, com chaves, colchetes e pares de nome e valor."),
                ("Contrato", "o combinado sobre a resposta da API: os campos que vêm e o tipo de cada um."),
                ("Campo", "cada par de nome e valor da resposta, como `data` no exemplo."),
                ("Código de status", "o número com que a API diz como a chamada terminou: 200 é sem erro, 4xx e 5xx são erro."),
                ("Seletor", "o texto que diz ao teste qual elemento da página usar."),
                ("Roteiro", "a lista dos passos que o teste automatizado executa, na ordem."),
                ("Ficha da falha", "a frase em que o teste automático diz o que viu de errado."),
            ]),
        ]},
        {"id": "comecar", "titulo": "O botão Começar", "blocos": [
            ("p", "Tudo o que precisava rodar já rodou antes, na máquina do projeto: em cada cenário a falha foi armada, o teste automatizado foi "
                  "executado, e o que ele e o navegador registraram está guardado nesta página. Você não instala nada e não precisa de nenhum outro "
                  "programa aberto."),
            ("p", "Quando você clica em Começar, a página faz, nesta ordem:"),
            ("ol", [
                "Confere se consegue guardar a sua sessão. Se não conseguir, ela avisa, e no fim mostra um código da sessão para você copiar e mandar "
                "ao facilitador.",
                "Faz as três perguntas sobre a sua experiência.",
                "Abre o treino, sem cronômetro: um cenário de contrato e um exercício de seletor, com a resposta certa dita no fim de cada um.",
                f"Mostra os {cenarios} cenários, um por vez, na ordem sorteada para você. Cada um espera o seu clique em **Abrir o cenário**, e é nesse "
                "clique que o tempo dele começa.",
                "No fim, diz se a sessão ficou guardada e mostra o código da sessão.",
            ]),
            ("p", "A página guarda cada resposta na hora. Se ela fechar ou a internet cair entre um cenário e outro, abra o mesmo endereço de novo, no "
                  "mesmo navegador: ela volta de onde você parou."),
            ("aviso", "Antes de clicar", "Depois do Começar não há pausa dentro de um cenário. Confira que você tem o tempo reservado e tire com o "
                                         "facilitador as dúvidas sobre as regras."),
            ("botao", "Começar"),
        ]},
    ]


# ------------------------------------------------------------------ Markdown

def _bloco_md(bloco: tuple) -> str:
    tipo = bloco[0]
    if tipo == "p":
        return bloco[1]
    if tipo == "ul":
        return "\n".join(f"- {item}" for item in bloco[1])
    if tipo == "ol":
        return "\n".join(f"{i}. {item}" for i, item in enumerate(bloco[1], 1))
    if tipo == "aviso":
        return f"> **{bloco[1]}.** {bloco[2]}"
    if tipo == "codigo":
        return f"{bloco[1]}:\n\n```text\n{bloco[2]}\n```"
    if tipo == "tabela":
        return "\n".join(["| " + " | ".join(bloco[1]) + " |", "|" + "---|" * len(bloco[1])] + ["| " + " | ".join(linha) + " |" for linha in bloco[2]])
    if tipo == "tempo":
        return "\n".join(["| Parte da sessão | Quanto dura | O que acontece |", "|---|---|---|"] + [f"| {a} | {b} | {c} |" for a, b, c in bloco[1]])
    if tipo == "par":
        return "\n\n".join(f"**{titulo}**\n\n" + "\n".join(f"- {item}" for item in itens) for titulo, itens in bloco[1])
    if tipo == "termos":
        return "\n".join(f"- **{termo}** {texto}" for termo, texto in bloco[1])
    if tipo == "causas":
        return "\n".join(f"{i}. `{causa}`: {definicao}" for i, (causa, definicao) in enumerate(lbm.DEFINICAO_DAS_CAUSAS.items(), 1))
    if tipo == "botao":
        return f"(Na página da sessão, o botão **{bloco[1]}** fica aqui.)"
    raise ValueError(f"bloco desconhecido: {tipo!r}")


def em_markdown() -> str:
    """O tutorial em Markdown, como fica no Memorial: a tag de documento derivado, o título e as seções numeradas."""
    partes = [
        "<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por `python linha_de_base_manual.py tutorial --gravar` a partir de "
        "`Programacao/AgenteCore/experimentos/tutorial_do_integrante.py` (`tutorial --check` regera e compara); não editar à mão.\n"
        "     ! Motivo: é o tutorial que os três integrantes da linha de base manual da Fase 5 leem antes de começar a sessão (decisões 135 e "
        "136). Os três têm de receber o mesmo texto, os números dele vêm das constantes do ajudante da sessão, e nenhum exemplo vem das "
        "cobaias; na página de cada sessão (`Documentacao/dashboard/sessao-integrante-N.html`) ele sai do mesmo conteúdo, com o botão no fim. -->",
        f"# {TITULO}",
        "O que você precisa saber antes de começar a sessão em que vai consertar testes à mão.",
    ]
    for n, secao in enumerate(secoes(), 1):
        partes.append(f"## {n}. {secao['titulo']}")
        partes += [_bloco_md(b) for b in secao["blocos"]]
    return "\n\n".join(partes) + "\n"


# ------------------------------------------------------------------ o trecho que abre a página da sessão

# ! Alteração de IA - Revisar: (16/11/2026, decisões 135 e 136) o tutorial em HTML: `_marcas` (as três marcas do texto viram
# `<code>`, `<strong>` e `<a>`), `_bloco_html` (um bloco vira o trecho de HTML dele), `secoes_em_html` (o índice e as seções, com
# o botão Começar no fim) e `ESTILO` (as cores em tokens para o tema claro e o escuro, a coluna de leitura, a tabela e o código
# com rolagem própria), que a página da sessão reaproveita.
# ! Motivo: os integrantes não abrem o repositório; o tutorial chega a eles como a primeira parte da página da sessão. O formato é
# o que o artefato do claude.ai aceita (sem esqueleto próprio, fontes só do Google), e a página tem de ler bem em tela estreita.
def _marcas(texto: str) -> str:
    t = html.escape(texto, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    return re.sub(r"\[([^\]]+)\]\((https://[^)\s]+)\)", r'<a href="\2">\1</a>', t)


def _bloco_html(bloco: tuple) -> str:
    tipo = bloco[0]
    if tipo == "p":
        return f"<p>{_marcas(bloco[1])}</p>"
    if tipo in ("ul", "ol"):
        return f"<{tipo}>" + "".join(f"<li>{_marcas(item)}</li>" for item in bloco[1]) + f"</{tipo}>"
    if tipo == "aviso":
        return f'<aside class="aviso"><p class="aviso-titulo">{_marcas(bloco[1])}</p><p>{_marcas(bloco[2])}</p></aside>'
    if tipo == "codigo":
        return f'<figure class="codigo"><figcaption>{_marcas(bloco[1])}</figcaption><pre><code>{html.escape(bloco[2], quote=False)}</code></pre></figure>'
    if tipo == "tabela":
        cabecalho = "".join(f"<th>{_marcas(c)}</th>" for c in bloco[1])
        linhas = "".join("<tr>" + "".join(f"<td>{_marcas(c)}</td>" for c in linha) + "</tr>" for linha in bloco[2])
        return f'<div class="rolagem"><table><thead><tr>{cabecalho}</tr></thead><tbody>{linhas}</tbody></table></div>'
    if tipo == "tempo":
        return '<ol class="tempo">' + "".join(
            f'<li><span class="tempo-duracao">{_marcas(b)}</span><span class="tempo-parte">{_marcas(a)}</span><span class="tempo-texto">{_marcas(c)}</span></li>'
            for a, b, c in bloco[1]) + "</ol>"
    if tipo == "par":
        return '<div class="par">' + "".join(
            f'<section class="tipo"><h3>{_marcas(titulo)}</h3><ul>' + "".join(f"<li>{_marcas(item)}</li>" for item in itens) + "</ul></section>"
            for titulo, itens in bloco[1]) + "</div>"
    if tipo == "termos":
        return '<dl class="termos">' + "".join(f"<div><dt>{_marcas(termo)}</dt><dd>{_marcas(texto)}</dd></div>" for termo, texto in bloco[1]) + "</dl>"
    if tipo == "causas":
        return '<ol class="causas">' + "".join(f"<li><code>{html.escape(causa)}</code><span>{_marcas(definicao)}</span></li>"
                                               for causa, definicao in lbm.DEFINICAO_DAS_CAUSAS.items()) + "</ol>"
    if tipo == "botao":
        return f'<p><button type="button" class="botao" id="{ID_DO_BOTAO}">{_marcas(bloco[1])}</button></p>'
    raise ValueError(f"bloco desconhecido: {tipo!r}")


def secoes_em_html() -> str:
    """O índice e as seções do tutorial, prontos para entrar na página da sessão."""
    lista = secoes()
    partes = ['<nav aria-label="Nesta página"><p class="indice-titulo">Nesta página</p><ol>'
              + "".join(f'<li><a href="#{s["id"]}">{_marcas(s["titulo"])}</a></li>' for s in lista) + "</ol></nav>", "<main>"]
    for n, secao in enumerate(lista, 1):
        partes.append(f'<section id="{secao["id"]}"><h2><span class="numero">{n:02d}</span><span>{_marcas(secao["titulo"])}</span></h2>')
        partes += [_bloco_html(b) for b in secao["blocos"]]
        partes.append("</section>")
    partes.append("</main>")
    return "\n".join(partes)


ESTILO = """
/* folha de bancada: uma coluna de leitura alinhada à esquerda, o índice no topo, os passos numerados e cada tabela ou bloco de código com rolagem própria */
:root {
  --fundo: #f2f4f7; --papel: #ffffff; --tinta: #15202b; --apagado: #50606f; --fio: #d3dae2;
  --destaque: #0b5aa8; --destaque-fundo: #e2edf9; --sobre-destaque: #ffffff; --relogio: #8a5200; --relogio-fundo: #f9edd3; --codigo-fundo: #e8ecf1;
  --certo: #1c6b3a; --certo-fundo: #dff1e5;
  --texto: "IBM Plex Sans", "Segoe UI", system-ui, sans-serif; --titulo: "IBM Plex Sans Condensed", "Arial Narrow", "Segoe UI", sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, "Cascadia Mono", Consolas, monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --fundo: #0e141a; --papel: #161f29; --tinta: #e5eaf0; --apagado: #9babb9; --fio: #2a3745;
    --destaque: #7fb8f6; --destaque-fundo: #15293f; --sobre-destaque: #0e141a; --relogio: #f1ba5c; --relogio-fundo: #33270d; --codigo-fundo: #1c2733;
    --certo: #7fd49c; --certo-fundo: #12301e;
    color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --fundo: #0e141a; --papel: #161f29; --tinta: #e5eaf0; --apagado: #9babb9; --fio: #2a3745;
  --destaque: #7fb8f6; --destaque-fundo: #15293f; --sobre-destaque: #0e141a; --relogio: #f1ba5c; --relogio-fundo: #33270d; --codigo-fundo: #1c2733;
  --certo: #7fd49c; --certo-fundo: #12301e;
  color-scheme: dark;
}
* { box-sizing: border-box; }
body { background: var(--fundo); color: var(--tinta); font-family: var(--texto); font-size: 1rem; line-height: 1.6; }
.pagina { max-width: 46rem; margin: 0 auto; padding-block: 2.5rem 4rem; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); display: flex; flex-direction: column; gap: 2.5rem; }
header { display: flex; flex-direction: column; gap: 0.75rem; border-bottom: 2px solid var(--tinta); padding-bottom: 1.5rem; }
.sobre { margin: 0; font-size: 0.8125rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--destaque); }
h1, h2, h3 { font-family: var(--titulo); font-weight: 600; line-height: 1.15; margin: 0; text-wrap: balance; }
h1 { font-size: 2.5rem; }
h2 { font-size: 1.625rem; display: flex; gap: 0.75rem; align-items: baseline; }
h3 { font-size: 1.125rem; }
p, ul, ol, dl, figure { margin: 0; }
.chamada { font-size: 1.125rem; color: var(--apagado); max-width: 36rem; }
.fatos { list-style: none; padding: 0; display: flex; flex-wrap: wrap; gap: 0.5rem; }
.fatos li { font-family: var(--mono); font-size: 0.8125rem; padding: 0.25rem 0.625rem; border: 1px solid var(--fio); background: var(--papel); border-radius: 2px; }
nav { background: var(--papel); border: 1px solid var(--fio); border-radius: 4px; padding: 1rem 1.25rem; }
.indice-titulo { font-size: 0.8125rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: var(--apagado); margin-bottom: 0.5rem; }
nav ol { padding-left: 1.5rem; columns: 2; column-gap: 2rem; }
nav li { break-inside: avoid; padding-block: 0.125rem; }
main { display: flex; flex-direction: column; gap: 3rem; }
main > section { display: flex; flex-direction: column; gap: 1rem; scroll-margin-top: 1rem; }
.numero { font-family: var(--mono); font-size: 1rem; font-weight: 500; color: var(--destaque); font-variant-numeric: tabular-nums; }
a { color: var(--destaque); text-underline-offset: 0.15em; }
a:focus-visible, button:focus-visible, input:focus-visible, select:focus-visible, textarea:focus-visible { outline: 2px solid var(--destaque); outline-offset: 2px; border-radius: 2px; }
main ul, main ol { padding-left: 1.5rem; display: flex; flex-direction: column; gap: 0.375rem; }
code { font-family: var(--mono); font-size: 0.9em; background: var(--codigo-fundo); padding: 0.05em 0.3em; border-radius: 2px; overflow-wrap: anywhere; }
.aviso { background: var(--relogio-fundo); border: 1px solid var(--relogio); border-radius: 4px; padding: 0.875rem 1rem; display: flex; flex-direction: column; gap: 0.25rem; }
.aviso-titulo { font-size: 0.8125rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; color: var(--relogio); }
.codigo { display: flex; flex-direction: column; gap: 0.375rem; min-width: 0; }
.codigo figcaption { font-size: 0.875rem; color: var(--apagado); }
pre { margin: 0; background: var(--codigo-fundo); border: 1px solid var(--fio); border-radius: 4px; padding: 0.75rem 1rem; overflow-x: auto; }
pre code { background: none; padding: 0; font-size: 0.875rem; overflow-wrap: normal; white-space: pre; }
.rolagem { overflow-x: auto; border: 1px solid var(--fio); border-radius: 4px; background: var(--papel); }
table { border-collapse: collapse; width: 100%; font-size: 0.9375rem; }
th, td { text-align: left; vertical-align: top; padding: 0.5rem 0.75rem; border-bottom: 1px solid var(--fio); }
th { font-size: 0.8125rem; letter-spacing: 0.04em; text-transform: uppercase; color: var(--apagado); font-weight: 600; }
tbody tr:last-child td { border-bottom: 0; }
td code { white-space: nowrap; overflow-wrap: normal; }
td:first-child { min-width: 9rem; }
td:last-child { min-width: 14rem; }
.tempo { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0; border: 1px solid var(--fio); border-radius: 4px; background: var(--papel); }
.tempo li { display: flex; flex-direction: column; gap: 0.25rem; padding: 0.875rem 1rem; border-left: 1px solid var(--fio); min-width: 0; }
.tempo li:first-child { border-left: 0; }
.tempo-duracao { font-family: var(--mono); font-size: 1.0625rem; font-weight: 500; color: var(--relogio); font-variant-numeric: tabular-nums; }
.tempo-parte { font-weight: 600; }
.tempo-texto { font-size: 0.875rem; color: var(--apagado); }
.par { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem; }
.tipo { background: var(--papel); border: 1px solid var(--fio); border-top: 3px solid var(--destaque); padding: 1rem 1.125rem; display: flex; flex-direction: column; gap: 0.625rem; min-width: 0; }
.tipo ul { padding-left: 1.125rem; font-size: 0.9375rem; }
.termos { display: flex; flex-direction: column; gap: 0.875rem; }
.termos div { display: flex; flex-direction: column; gap: 0.125rem; }
dt { font-weight: 600; }
dd { margin: 0; color: var(--apagado); }
.causas { padding-left: 2.25rem; gap: 0.5rem; }
.causas li { padding-left: 0.25rem; }
.causas li::marker { font-family: var(--mono); font-size: 0.875rem; color: var(--apagado); }
.causas code { display: inline-block; margin-right: 0.5rem; font-weight: 500; }
.causas span { color: var(--apagado); }
.botao { font: inherit; font-weight: 600; padding: 0.75rem 1.5rem; border: 2px solid var(--destaque); border-radius: 4px; background: var(--destaque); color: var(--sobre-destaque); cursor: pointer; }
.botao:hover { filter: brightness(1.08); }
.botao.secundario { background: transparent; color: var(--destaque); }
.botao:disabled { opacity: 0.5; cursor: not-allowed; }
footer { border-top: 1px solid var(--fio); padding-top: 1rem; font-size: 0.875rem; color: var(--apagado); }
@media (max-width: 40rem) {
  h1 { font-size: 2rem; }
  h2 { font-size: 1.375rem; }
  nav ol { columns: 1; }
  .tempo { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .tempo li:nth-child(odd) { border-left: 0; }
  .tempo li:nth-child(n+3) { border-top: 1px solid var(--fio); }
  .par { grid-template-columns: minmax(0, 1fr); }
}
"""


# ------------------------------------------------------------------ gravar e conferir

def gravar() -> list[Path]:
    """Grava o Markdown do tutorial no Memorial; devolve o caminho."""
    ARQUIVO_MD.parent.mkdir(parents=True, exist_ok=True)
    ARQUIVO_MD.write_text(em_markdown(), encoding="utf-8", newline="\n")
    return [ARQUIVO_MD]


def conferir() -> list[str]:
    """O arquivo gravado, se falta ou difere do que o código gera (lista vazia quando está em dia)."""
    return [] if ARQUIVO_MD.exists() and ARQUIVO_MD.read_text(encoding="utf-8") == em_markdown() else [ARQUIVO_MD.name]
