#!/usr/bin/env python3
# ! Alteração de IA - Revisar: abas por tópico do painel do projeto (30/09/2026, pedido do Eric): comparativo
# qwen2.5:7b × qwen2.5-coder:7b, Fase 3-B (inéditos, ponte, sonda e corridas), curadoria da L1, recuperador,
# ablação base × instruct, pesquisa bibliográfica e ferramental. Cada função secao_* lê os JSON/MD versionados
# e devolve os dados dos gráficos (Chart.js, desenhados pelo JS de gerar_dashboard.py) e o HTML da seção.
# ! Motivo: o Eric pediu "a aba do comparativo do qwen 2.5 7b e o coder" e que o painel seja "o grande
# compilador / centralizador das análises e dados, com cada aba específica falando sobre os tópicos ...
# sumarizado e focando no visual e facilidade de entendimento"; gerar_dashboard.py já passava de 900 linhas,
# então as abas novas vivem aqui, no mesmo padrão: pergunta, resposta em uma frase, números-chave, um ou
# dois gráficos, leitura curta e as tabelas completas recolhidas. Nenhum número é digitado à mão.
"""Abas por tópico do painel do projeto. Uso: importado por gerar_dashboard.py (montar(ctx))."""
from __future__ import annotations

import html
import unicodedata
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

import painel_atlas as pa
import painel_explorador as pe
import painel_textos as pt

# ! Alteração de IA - Revisar: (05/11/2026, sessão de revisão) o endereço da página da sessão, gerada por ferramentas/sessao_revisao.py.
# ! Motivo: o Eric decide pelo painel, e a aba da trilha aponta para onde a sessão acontece.
URL_SESSAO_REVISAO = "https://claude.ai/artifact/7UrQ4gaqHj9qnvo22tfDgS"

RAIZ = Path(__file__).resolve().parent.parent
EXP = RAIZ / "Programacao" / "AgenteCore" / "experimentos"
RES = EXP / "resultados_alvo"
MEMORIAL = RAIZ / "Documentacao" / "memorial"
PESQUISA = MEMORIAL / "2-pesquisa-e-literatura"
FERRAMENTAL = MEMORIAL / "5-metodo-e-ferramental"

A, B = "qwen2.5:7b", "qwen2.5-coder:7b"
COD3B = "qwen2.5-coder:3b"
CLASSES = {1: "léxica", 2: "sintática", 3: "semântica", 4: "tradução", 5: "runtime", 6: "efeito"}
# Cor de cada série: posição fixa na paleta validada (tokens --s1..--s8 no CSS de gerar_dashboard.py). A ordem
# das posições é o que garante que séries vizinhas se distinguem, inclusive para quem não vê cores.
SLOTS = {"qwen2.5:7b": 1, "granite4.2:8b": 2, "qwen2.5-coder:7b": 3, "qwen2.5-coder:3b": 4, "phi4-mini:3.8b": 5,
         "qwen2.5-coder:1.5b": 6, "qwen2.5-coder:1.5b-instruct-fp16": 7, "qwen2.5-coder:1.5b-instruct-q8_0": 8,
         "qwen2.5:0.5b-instruct": 1, "qwen2.5:0.5b-base": 2}

# Mapa do painel: grupo → (id da seção, nome na aba, o que a aba responde). É a fonte da barra lateral de navegação e
# da lista "Mapa do painel" da aba Início. A ordem é a de importância para quem decide: primeiro o projeto e o que
# depende do Eric, depois a decisão e os resultados que a sustentam, a biblioteca gerida pelo modelo (o experimento
# central), a Pré-Fase 4 (a fase em andamento), a pesquisa e o método e, por último, as fases anteriores.
# ! Alteração de IA - Revisar: (06/10/2026) grupos renomeados e reordenados por importância, com a aba mais importante
# de cada grupo em primeiro (Decisão antes de Resultados; Pesquisa antes de Ferramental).
# ! Motivo: pedido do Eric em 06/10: com 23 abas a faixa horizontal ficou ilegível, e a ordem antiga era a de
# construção (Resultados antes da Decisão, Fases anteriores antes da Pesquisa), não a de leitura.
# ! Alteração de IA - Revisar: (11/11/2026) o mapa passa a ser por fase: "Visão geral", um grupo por fase do roadmap (que abre pela aba de visão da fase, vinda de
# painel_fases.py) e "Pesquisa e documentação". As abas dos tópicos só mudaram de grupo, cada uma com os comentários que tinha; quatro ganharam nome novo, porque o
# nome antigo repetia o do grupo, e a aba "Fases 2-A e 2-B" virou duas.
# ! Motivo: o Eric pediu, em 11/11/2026, abas que detalhem cada fase, com as abas dos tópicos de cada uma embaixo, na lógica do documento do TCC: a ordem por
# importância de 06/10/2026 não dizia de que fase era cada aba. Dentro de cada fase a ordem é a do documento do TCC (seções 6.1 a 6.7), com o fechamento no fim.
# Toda aba nova de tópico entra no grupo da fase dela; painel_fases.abas_fora_de_lugar e os testes acusam fase sem grupo ou atalho para aba que não existe.
NAV = [
    ("Visão geral", [
        # ! Alteração de IA - Revisar: (11/11/2026) a descrição do Início passa a dizer o que a aba virou: o resumo do projeto inteiro.
        # ! Motivo: o Eric pediu que o Início seja um resumo visual do projeto como um todo; a descrição antiga falava da lista de pendências e do mapa do painel.
        ("inicio", "Início", "O projeto em uma página: o problema, como o agente trabalha, o caminho das fases e o que já se descobriu."),
        # ! Alteração de IA - Revisar: (11/11/2026) a descrição do Roadmap passa a dizer o formato novo, com uma linha por fase.
        # ! Motivo: os cartões estreitos e altos das fases viraram cartões em linha, com a pergunta que a fase responde e o "Saiba mais".
        ("roadmap", "Roadmap", "Uma linha por fase, com a pergunta que ela responde e o estado, e as corridas de cada fase com o comando pronto."),
        ("pendencias", "Pendências", "Uma ficha por decisão: o que é, por que importa, opções, recomendação e decisão."),
        # ! Alteração de IA - Revisar: (11/11/2026) aba nova do glossário; a seção vem de painel_glossario.secao_glossario.
        # ! Motivo: o Eric pediu que o painel explique os métodos e os termos técnicos para quem não acompanhou o projeto.
        ("glossario", "Glossário e métodos", "As palavras do projeto e os métodos de medida em linguagem direta, cada método com o que o projeto faz com ele e a fonte."),
    ]),
    ("Fase 1", [
        # ! Alteração de IA - Revisar: (11/11/2026) aba de visão da Fase 1; a seção vem de painel_fases.secao_fase.
        # ! Motivo: o Eric pediu uma aba que detalhe cada fase; é ela que abre o grupo, e o cabeçalho da fase na lateral leva a ela.
        ("f-1", "Visão da Fase 1", "A fase em uma página: o instalador, os dois sistemas de teste, as falhas ligadas de propósito e o banco de casos."),
    ]),
    ("Fase 2-A", [
        # ! Alteração de IA - Revisar: (11/11/2026) aba de visão da Fase 2-A; a seção vem de painel_fases.secao_fase.
        # ! Motivo: o Eric pediu uma aba que detalhe cada fase; é ela que abre o grupo, e o cabeçalho da fase na lateral leva a ela.
        ("f-2a", "Visão da Fase 2-A", "A fase em uma página: o que um modelo local diagnostica sem documentação nenhuma."),
        # ! Alteração de IA - Revisar: (11/11/2026) a aba "Fases 2-A e 2-B" virou duas; esta é a da Fase 2-A.
        # ! Motivo: cada fase passou a ter o seu grupo, e uma aba só para as duas ficaria fora de ambos.
        ("fase2a", "Prompts sem documentação", "Os modelos sem documentação nenhuma, em mais de uma forma de pergunta: o acerto por modelo e por forma."),
    ]),
    ("Fase 2-B", [
        # ! Alteração de IA - Revisar: (11/11/2026) aba de visão da Fase 2-B; a seção vem de painel_fases.secao_fase.
        # ! Motivo: o Eric pediu uma aba que detalhe cada fase; é ela que abre o grupo, e o cabeçalho da fase na lateral leva a ela.
        ("f-2b", "Visão da Fase 2-B", "A fase em uma página: quanto a documentação escrita por pessoas ajuda, e quanto a errada atrapalha."),
        # ! Alteração de IA - Revisar: (11/11/2026) a aba "Fases 2-A e 2-B" virou duas; esta é a da Fase 2-B.
        # ! Motivo: cada fase passou a ter o seu grupo, e uma aba só para as duas ficaria fora de ambos.
        ("fase2b", "Biblioteca em seis condições", "A biblioteca escrita à mão em seis condições, de nenhuma documentação até o verbete errado de propósito."),
    ]),
    ("Fase 3", [
        # ! Alteração de IA - Revisar: (11/11/2026) aba de visão da Fase 3; a seção vem de painel_fases.secao_fase.
        # ! Motivo: o Eric pediu uma aba que detalhe cada fase; é ela que abre o grupo, e o cabeçalho da fase na lateral leva a ela.
        ("f-3", "Visão da Fase 3", "A fase em uma página: o modelo editando a própria documentação, e a escolha do modelo pela regra fixada antes."),
        # ! Alteração de IA - Revisar: (11/11/2026) a aba "Fase 3" passa a se chamar "Edições da biblioteca".
        # ! Motivo: com a navegação por fase, o nome antigo repetia o do cabeçalho do grupo, e a aba não se distinguia dele.
        ("fase3", "Edições da biblioteca", "A biblioteca gerida pelo modelo: edições, rejeições, recuperação, custo e revisão humana."),
        ("visao", "Resultados", "O que os testes decidiram: acurácia por versão da biblioteca e as três fases lado a lado."),
        ("modelos", "Modelos", "Veredito e números de cada modelo, acerto por classe de defeito e por nível."),
        ("decisao", "Decisão", "A regra pré-registrada, o bootstrap, a fronteira de Pareto e a frase da decisão."),
        ("hipoteses", "Hipóteses", "As seis hipóteses pré-registradas, o veredito de cada uma e os achados novos."),
        ("comparacao", "Entre fases", "O que cada etapa acrescentou, nos 90 e nos 36, com custo e riscos."),
        ("metodo", "Método e limites", "Como a Fase 3 foi medida, as limitações declaradas e a Fase 3-B."),
    ]),
    ("Fase 3-B", [
        # ! Alteração de IA - Revisar: (11/11/2026) aba de visão da Fase 3-B; a seção vem de painel_fases.secao_fase.
        # ! Motivo: o Eric pediu uma aba que detalhe cada fase; é ela que abre o grupo, e o cabeçalho da fase na lateral leva a ela.
        ("f-3b", "Visão da Fase 3-B", "A fase em uma página: as dúvidas que a Fase 3 deixou, uma por teste."),
        # ! Alteração de IA - Revisar: (11/11/2026) a aba "Fase 3-B" passa a se chamar "Inéditos, pontes e sonda".
        # ! Motivo: com a navegação por fase, o nome antigo repetia o do cabeçalho do grupo, e a aba não se distinguia dele.
        ("tresb", "Inéditos, pontes e sonda", "Casos inéditos, ponte de versão, sonda de correção e as corridas complementares."),
        ("cruzada", "Troca cruzada", "A biblioteca escrita por um modelo, lida por outros dois: o ganho é dela ou de quem a lê?"),
        ("comparativo", "qwen × Coder", "Em que cenários o qwen2.5-coder:7b seria melhor que o qwen2.5:7b, e por que a decisão ficou."),
        ("curadoria", "Curadoria da L1", "O que a cópia de produção herdou da biblioteca escrita pelo modelo."),
        ("recuperador", "Recuperador", "A busca por palavras contra a busca por significado e a mistura das duas: vale trocar?"),
        ("ablacao", "Ablação", "Sem ajuste por instrução, o modelo faz a tarefa? O piso da família."),
        # ! Alteração de IA - Revisar: (11/11/2026) a aba "Fechamento" passa a se chamar "Fechamento das Fases 3 e 3-B".
        # ! Motivo: dentro do grupo da Fase 3-B o nome precisa dizer de que fases é o fechamento, porque a Fase 4 tem o dela.
        ("fechamento", "Fechamento das Fases 3 e 3-B", "As Fases 3 e 3-B podem ser dadas por concluídas? O estado de cada tópico e o que depende do Eric."),
    ]),
    # grupo da Pré-Fase 4 (01/10/2026): um id só entra neste mapa junto com a seção dele, porque
    # teste_toda_aba_do_mapa_existe_na_pagina exige que todo botão da navegação tenha a sua seção
    ("Pré-Fase 4", [
        # ! Alteração de IA - Revisar: (11/11/2026) aba de visão da Pré-Fase 4; a seção vem de painel_fases.secao_fase.
        # ! Motivo: o Eric pediu uma aba que detalhe cada fase; é ela que abre o grupo, e o cabeçalho da fase na lateral leva a ela.
        ("f-pre4", "Visão da Pré-Fase 4", "A fase em uma página: as três frentes de pesquisa antes de levar o agente à tela."),
        ("colibri", "Modelos grandes pelo disco", "Dá para rodar nesta máquina um modelo gigante lendo os pesos do SSD? O que o colibri pede, o que foi medido aqui e o que se aproveita."),
        ("atlas", "Atlas", "Que verbetes a busca entrega para cada tipo de defeito e o que o modelo faz com eles: o mapa, a rota de cada caso e as trocas entre causas."),
        ("raciocinio", "Raciocínio aberto", "Dá para ver por que o modelo respondeu o que respondeu? A trilha bruta, o relatório por caso, o que o código consegue conferir e o que a literatura sustenta para a arquitetura da trilha."),
        ("cerebro", "Cérebro e memória", "Dá para mostrar a rede neural como o cérebro do agente, ao vivo? O Brainiac e os grafos do código e do conhecimento servem? O que a literatura sustenta nesta máquina e neste painel."),
    ]),
    # grupo da Fase 4 (27/10/2026): a corrida 17 é a primeira análise da fase; o id entra junto com a seção (secao_reproducao)
    ("Fase 4", [
        # ! Alteração de IA - Revisar: (11/11/2026) aba de visão da Fase 4; a seção vem de painel_fases.secao_fase.
        # ! Motivo: o Eric pediu uma aba que detalhe cada fase; é ela que abre o grupo, e o cabeçalho da fase na lateral leva a ela.
        ("f-4", "Visão da Fase 4", "A fase em uma página: o agente trabalhando na tela, passo a passo, com o que cada passo mediu."),
        ("reproducao", "Reprodução na tela", "Quantos casos de avaliação a tela consegue reproduzir, com que custo por cenário e o que fica fora: a corrida 17 nos 72 casos e a mesma corrida nos 36 inéditos da ficha 27."),
        # aba da corrida 16 (27/10/2026, P3): o id entra junto com a seção (secao_calibracao)
        ("calibracao", "Calibração", "Quantos verbetes entregar ao modelo, onde ficam os cortes do selo de confiança e quanto a probabilidade da resposta separa acerto de erro: a corrida 16 nos 90 casos."),
        ("tela", "Tela e caso escrito", "O agente dá o mesmo diagnóstico ao caso lido da tela e ao mesmo caso escrito? As corridas 18 a 18e nos casos que reproduzem, com a regra que compara os dois lados, os selos, as causas respondidas e o tamanho do prompt."),
        # aba da corrida 19 (01/11/2026, P4): o id entra junto com a seção (secao_cura)
        ("cura", "Cura de seletor", "Quando o localizador de um passo quebra, o agente acha outro em código e o roteiro passa na reexecução? A corrida 19 nos quatro roteiros do front legado, com quatro modos de quebra nas duas formas, a taxa de cura e o tempo até o resultado."),
        # aba da corrida 20 (03/11/2026, P5): o id entra junto com a seção (secao_biblioteca)
        ("biblioteca", "Biblioteca em produção", "O que o agente propõe para a biblioteca passa pelos filtros em código, melhora os casos inéditos, e a marca de corrigido acerta? A corrida 20: o lote, os filtros, a reavaliação, a correção e a sonda."),
        # ! Alteração de IA - Revisar: (04/11/2026, P6) aba da corrida 21; o id entra junto com a seção (secao_cenarios).
        # ! Motivo: o ensaio dos cenários da Fase 5 é a sexta análise da Fase 4 e, pela regra do painel, vira uma aba.
        ("cenarios", "Cenários da Fase 5", "Quanto tempo o agente leva da detecção ao resultado nos dez cenários da ficha 36 e em quantos acerta? As corridas 21, 21b, 21c e 21d, o ensaio de uma repetição: tempo até o resultado, quantos chegaram a ele, a ficha da falha de cada cenário e o protocolo da medida com pessoas."),
        # ! Alteração de IA - Revisar: (04/11/2026, P7) aba da corrida 22; o id entra junto com a seção (secao_trilha).
        # ! Motivo: a avaliação da própria trilha é a sétima análise da Fase 4 e, pela regra do painel, vira uma aba.
        ("trilha", "Avaliação da trilha", "A trilha do agente aponta os erros reais e o passo certo quando a falha é injetada de propósito? A corrida 22 nos 36 casos de avaliação: os sinais de alerta, as mudanças de propósito na entrada e a amostra de relatórios da sessão de revisão."),
        # ! Alteração de IA - Revisar: (05/11/2026, decisão 92) aba da conferência dos 36 inéditos; o id entra junto com a seção (secao_conferencia).
        # ! Motivo: o Eric decide pelo painel, e a ficha 46 pede a conferência dele antes da corrida 24.
        # ! Alteração de IA - Revisar: (05/11/2026, decisão 91) aba da corrida 23; o id entra junto com a seção (secao_experimento).
        # ! Motivo: o experimento dos itens da decisão 55 é uma análise nova da Fase 4 e, pela regra do painel, vira uma aba.
        ("experimento", "Exemplar e rótulos", "Um exemplar resolvido ou os rótulos escritos em palavras mudam o acerto do modelo? A corrida 23 nos 90 casos, uma condição por item, contra a calibração da corrida 16."),
        ("conferencia", "Conferência dos inéditos", "Os 36 casos que a corrida 24 mede estão certos? Cada caso com o gabarito, o que a corrida 17 viu, a pré-análise do Claude e a resposta do Eric."),
        # ! Alteração de IA - Revisar: (06/11/2026) aba da corrida 24; o id entra junto com a seção (secao_ineditos_f4).
        # ! Motivo: a medida da biblioteca final em casos que ela nunca viu é uma análise nova da Fase 4 e, pela regra do painel, vira uma aba.
        ("ineditosf4", "Inéditos em texto", "A biblioteca final acerta em casos que nunca viu? A corrida 24 nos 36 inéditos da ficha 27, conferidos pelo Eric: o acerto por classe e por nível, o verbete certo no contexto, o selo e a comparação com a corrida 18e."),
        # ! Alteração de IA - Revisar: (05/11/2026, P8) a aba do fechamento abre o grupo; o id entra junto com a seção (secao_fechamento_f4).
        # ! Motivo: é a aba da fase que o plano previa (seção 3.8): quem abre o grupo vê primeiro o que fechou e o que ficou como limitação.
        ("fechamentof4", "Fechamento da fase", "A Fase 4 fez o que o plano pediu? As regras uma a uma, o que fica como limitação declarada, o que depende do Eric e o que o documento do TCC precisa carregar, lidos do relatório da fase."),
    ]),
    # ! Alteração de IA - Revisar: (07/11/2026) grupo da Pós-Fase 4, com a aba do que o Eric pediu em três partes; o id entra junto com a seção (secao_pos_fase4).
    # ! Motivo: a Pós-Fase 4 foi especificada e pesquisada em 07/11/2026 (levantamento §6.15), e as fichas 53 e 54 estão abertas: o Eric decide pelo painel.
    ("Pós-Fase 4", [
        # ! Alteração de IA - Revisar: (11/11/2026) aba de visão da Pós-Fase 4; a seção vem de painel_fases.secao_fase.
        # ! Motivo: o Eric pediu uma aba que detalhe cada fase; é ela que abre o grupo, e o cabeçalho da fase na lateral leva a ela.
        ("f-pos4", "Visão da Pós-Fase 4", "A fase em uma página: o que chega a quem lê os relatórios do agente."),
        # ! Alteração de IA - Revisar: (11/11/2026) a aba "Pós-Fase 4" passa a se chamar "O pedido e a pesquisa".
        # ! Motivo: com a navegação por fase, o nome antigo repetia o do cabeçalho do grupo, e a aba não se distinguia dele.
        ("posfase4", "O pedido e a pesquisa", "O que o Eric pediu em três partes, o que a pesquisa sustenta, os vereditos dos oito repositórios e das cinco bases, as decisões do quadro e o plano aprovado, com os pacotes antes e depois da Fase 5."),
        # ! Alteração de IA - Revisar: (07/11/2026, pacote Q2) aba dos filtros de texto; o id entra junto com a seção (secao_texto).
        # ! Motivo: a leitura antes e depois dos textos que chegam ao analista é uma análise nova da Pós-Fase 4 e, pela regra do painel, vira uma aba lida do JSON.
        ("texto", "O que chega ao analista", "Os relatórios e os verbetes ficaram mais curtos e diretos? Os oito filtros de prolixidade e objetividade, calibrados no corpus dos comentários deste repositório, aplicados aos relatórios v2 e v3 das três corridas vigentes e aos verbetes contra a camada de leitura."),
        # ! Alteração de IA - Revisar: (08/11/2026, pacote Q3) aba da árvore de decisão; o id entra junto com a seção (secao_arvore).
        # ! Motivo: a árvore por caso é uma análise nova da Pós-Fase 4 (plano, seção 3.4) e, pela regra do painel, vira uma aba lida dos JSON gravados.
        ("arvore", "Árvore de decisão", "Dá para ver por que o agente decidiu o que decidiu, passo a passo? Uma árvore por trilha das corridas vigentes: o que o modelo leu depois da poda, que verbetes entraram, a causa contra a segunda com a confiança em palavras, a cura quando houve, e a origem de cada afirmação (observado, conferido, declarado, desconhecido)."),
        # ! Alteração de IA - Revisar: (08/11/2026, pacote Q4) aba da barra de progresso e do protótipo do Git; o id entra junto com a seção (secao_progresso).
        # ! Motivo: as duas análises do Q4 (plano, seções 3.5 e 3.7) viram uma aba lida dos JSON gravados, como manda a regra do painel.
        ("progresso", "Barra e Git", "Dá para saber quanto falta enquanto o modelo pensa, e o que rodar quando o código das cobaias muda? As taxas do modelo nesta máquina, o erro da estimativa da barra por fase, medido nos registros gravados, e a seleção de cenários pelo diff do Git, provada no histórico do repositório."),
        # ! Alteração de IA - Revisar: (10/11/2026, pacote Q5) aba da sessão com revisor humano; o id entra junto com a seção (secao_revisao_v3).
        # ! Motivo: a medida com revisor humano (ficha 40, opção b) é uma análise nova da Pós-Fase 4 e, pela regra do painel, vira uma aba lida do JSON gravado.
        ("revisaov3", "Revisão humana", "O relatório v3 com a árvore de decisão ajuda uma pessoa a decidir? A sessão de revisão da corrida 24: os 36 relatórios lidos um a um, às cegas, todos por um analista de QA da empresa a quem o Eric passou os relatórios, com a adesão apropriada (aceitar o diagnóstico certo e recusar o errado), o erro localizado e a utilidade."),
        # ! Alteração de IA - Revisar: (10/11/2026, decisão 116) aba da corrida 25; o id entra junto com a seção (secao_sem_notas).
        # ! Motivo: o experimento da ficha 63 (opção b) é uma análise nova e, pela regra do painel, vira uma aba lida do JSON gravado, antes e depois da corrida.
        ("semnotas", "Notas do modelo", ("As notas que o modelo escreveu na biblioteca ajudam ou atrapalham o diagnóstico? A corrida 25: a biblioteca de produção sem as notas do modelo e sem os "
                                        "verbetes aprendidos, nos 36 casos oficiais e nos 36 inéditos, contra as corridas 22 e 24, com a prévia sem modelo e a regra fixada antes.")),
        # ! Alteração de IA - Revisar: (10/11/2026, decisão 118) aba da pesquisa das três ideias do Eric para o fluxo do agente; o id entra junto com a seção (secao_fluxo).
        # ! Motivo: a rodada 7 da pesquisa (levantamento §6.16) é uma análise nova e, pela regra do painel, vira uma aba lida dos JSON gravados; as fichas 65 a 67 estão abertas, e o Eric decide por ela.
        ("fluxo", "Fluxo do agente", ("As três ideias do Eric para o fluxo do agente entram? O que a literatura e os dados do projeto sustentam para o raciocínio em passos, o ciclo de "
                                      "reavaliação e o analista de documentação, o veredito por ideia, a proposta de desenho e as fichas 65 a 67.")),
        # ! Alteração de IA - Revisar: (10/11/2026, decisão 120) aba da corrida 26; o id entra junto com a seção (secao_segundo_passe).
        # ! Motivo: o experimento da ficha 66 (opção b) é uma análise nova e, pela regra do painel, vira uma aba lida do JSON gravado, antes e depois da corrida.
        ("segpasse", "Segundo passe", ("Um segundo pedido de diagnóstico, só quando um sinal acende e com outros verbetes, conserta mais do que estraga? A corrida 26: os casos com o selo "
                                       "baixo ou a FONTE divergente, os verbetes seguintes da mesma busca, a regra de escolha fixada antes e a prévia sem modelo.")),
        # ! Alteração de IA - Revisar: (10/11/2026, decisão 121) aba das duas medidas da proposta do analista de documentação; o id entra junto com a seção (secao_analista).
        # ! Motivo: a medida M1 (sem modelo, já rodada) e a corrida 27 (a medida M2) são análises novas e, pela regra do painel, viram uma aba lida dos JSON gravados.
        ("analista", "Analista de documentação", ("Os portões novos barram o que a pessoa barrou, e a entrada própria muda o que o modelo escreve na biblioteca? A medida M1 (os portões 3, "
                                                  "4 e 5 nas 92 propostas da corrida 20, contra a revisão humana) e a corrida 27 (o analista com a ficha curta do caso).")),
    ]),
    ("Fase 5", [
        # ! Alteração de IA - Revisar: (11/11/2026) aba de visão da Fase 5; a seção vem de painel_fases.secao_fase.
        # ! Motivo: o Eric pediu uma aba que detalhe cada fase; é ela que abre o grupo, e o cabeçalho da fase na lateral leva a ela.
        ("f-5", "Visão da Fase 5", "A fase em uma página: o agente contra a linha de base manual."),
    ]),
    ("Pesquisa e documentação", [
        ("pesquisa", "Pesquisa", "As rodadas de literatura, as afirmações verificadas e os filtros adotados."),
        ("ferramental", "Ferramental", "As ferramentas locais, a economia de tokens e a medição do servidor de memória do código."),
    ]),
]


# ------------------------------------------------------------------ utilidades

def esc(s) -> str:
    return html.escape(str(s), quote=False)


def fmt(v, casas: int = 1) -> str:
    if v is None:
        return "—"
    return f"{v:.{casas}f}".replace(".", ",")


def pp(v) -> str:
    """Diferença em pontos percentuais, com sinal tipográfico."""
    if v is None:
        return "—"
    return f"{v:+.1f}".replace(".", ",").replace("-", "−") + " pp"


def kpis(itens: list[tuple[str, str, str]]) -> str:
    """Cartões de número-chave; valores compridos (três números com setas) descem um degrau de tamanho."""
    return '<div class="kpis">' + "".join(
        f"<div class='kpi'><span>{esc(t)}</span><b{' class=longo' if len(b) > 14 else ''}>{esc(b)}</b><small>{esc(s)}</small></div>" for t, b, s in itens) + "</div>"


_NUM = re.compile(r"^[+−\-]?[\d.,]+( pp|%| s)?$")


def tabela(cab: list[str], linhas: list[list], raw: bool = False, classe: str = "") -> str:
    """Tabela HTML. Com raw=True as células já vêm em HTML (não são escapadas)."""
    def td(c) -> str:
        s = str(c)
        num = bool(_NUM.match(re.sub(r"<[^>]+>", "", s).strip())) or s.strip() in {"—", "-"}
        return f'<td{" class=num" if num else ""}>{s if raw else esc(s)}</td>'
    th = "".join(f"<th>{esc(c)}</th>" for c in cab)
    trs = "".join("<tr>" + "".join(td(c) for c in r) + "</tr>" for r in linhas)
    return f'<div class="tabela {classe}"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>'


def detalhes(titulo: str, corpo: str) -> str:
    return f"<details><summary>{esc(titulo)}</summary>{corpo}</details>"


def leitura(itens: list[str]) -> str:
    """Lista de leitura curta; os itens já vêm em HTML (podem levar <strong> e <code>)."""
    return '<ul class="leitura">' + "".join(f"<li>{i}</li>" for i in itens) + "</ul>"


def fontes(itens: list[str]) -> str:
    return '<p class="nota fontes"><strong>Fontes:</strong> ' + "; ".join(itens) + ".</p>"


def chip(classe: str, texto: str) -> str:
    return f'<span class="chip {classe}">{esc(texto)}</span>'


def celula_duelo(a, b, modelo_a: str = A, modelo_b: str = B) -> str:
    """Célula 'a / b' tingida com a cor de quem está à frente; a intensidade acompanha a diferença."""
    if a is None or b is None:
        return "<td class=num>—</td>"
    d = round(b - a, 1)
    if abs(d) < 0.05:
        return f"<td class='num dc'>{fmt(a)} / {fmt(b)} <span class='delta zero'>=</span></td>"
    venc = modelo_b if d > 0 else modelo_a
    forca = min(60, int(abs(d) * 3) + 8)
    return (f"<td class='num dc' style='background:color-mix(in srgb, var(--s{SLOTS[venc]}) {forca}%, transparent)'>"
            f"{fmt(a)} / {fmt(b)} <span class='delta {'pos' if d > 0 else 'neg'}'>{pp(d)}</span></td>")


def heat(v, piso: float = 0.0, teto: float = 100.0) -> str:
    if v is None:
        return "transparent"
    a = max(0.0, min(1.0, (v - piso) / (teto - piso)))
    return f"color-mix(in srgb, var(--acento) {int(a * 55)}%, transparent)"


# ------------------------------------------------------------------ 1. comparativo qwen × Coder

ROTULO_FASE = {"2A_linear_ryzen": "2-A (Ryzen)", "2B_A0": "2-B A0", "2B_A2": "2-B A2", "F3_L0": "F3 L0",
               "F3_L1": "F3 L1", "F3_L2": "F3 L2", "F3_L3": "F3 L3"}


def secao_comparativo(cq: dict, blocos_cq: dict, md_para_html, road: dict, cartoes_corridas, analise3b: dict | None = None) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões, títulos e parágrafos à vista da aba reescritos em frases curtas, sem p, b/c, hit@3, L1 nem "casos discordantes".
    # ! Motivo: o texto à vista trazia siglas e números soltos (p de McNemar, b/c, hit@3, L1, P(top-1)) que o Eric pediu para tirar; os números continuam nas tabelas recolhidas.
    meta = cq["metadados"]
    LA, LB =meta["melhor_L_nos_36"][A], meta["melhor_L_nos_36"][B]
    v36 = {x["contexto"]: x for x in cq["fase3_versoes"]}
    melhor_A = v36[f"F3 · L{LA} · 36 de avaliação"]["acerto_A"]
    melhor_B = v36[f"F3 · L{LB} · 36 de avaliação"]["acerto_B"]
    l1 = v36["F3 · L1 · 36 de avaliação"]
    conf = {x["contexto"]: x for x in cq["confronto_f3"]}
    c1 = conf["F3 · L1 · 36 de avaliação"]
    doc1 = next(x for x in cq["fase3_documentacao"] if x["epoca"] == 1)
    tot = {s: {k: sum((x.get(f"{k}_{s}") or 0) for x in cq["fase3_revisao"]) for k in ("Correta", "Parcial", "Errada")} for s in "AB"}
    corr = {s: 100 * tot[s]["Correta"] / max(1, sum(tot[s].values())) for s in "AB"}
    rec1 = next(x for x in cq["fase3_recuperacao"] if x["L"] == 1)
    boot36 = cq["decisao"]["bootstrap"]["nos_36"]
    p_max_B = max(v["p_top1"] for k, v in boot36.items() if k.startswith(B + "/"))
    est = cq["decisao"]["estabilidade_top1"]
    vence = sorted(cq["onde_o_coder_vence"], key=lambda x: -x["delta"])
    n_vence, max_delta = len(vence), max(x["delta"] for x in vence)
    n_vence_36 = sum(1 for x in vence if "36" in x["onde"])
    # dados dos gráficos
    traj = {"36": [], "90": []}
    for x in cq["entre_fases"]:
        chave, conj = x["contexto"].split(" · nos ")
        if chave in ROTULO_FASE:
            traj[conj].append({"rot": ROTULO_FASE[chave], "acerto_A": x["acerto_A"], "acerto_B": x["acerto_B"],
                               "bal_A": x["bal_A"], "bal_B": x["bal_B"]})
    confronto = {"36": [], "90": []}
    for x in cq["confronto_2b"]:
        confronto["90"].append({"rot": x["contexto"].replace(" · ", " "), "so_A": x["so_qwen"], "so_B": x["so_coder"],
                                "ambos": x["ambos"], "nenhum": x["nenhum"], "p": x["p_mcnemar"]})
    for x in cq["confronto_f3"]:
        conj = "36" if "36" in x["contexto"] else "90"
        confronto[conj].append({"rot": x["contexto"].split(" · ")[1], "so_A": x["so_qwen"], "so_B": x["so_coder"],
                                "ambos": x["ambos"], "nenhum": x["nenhum"], "p": x["p_mcnemar"]})
    revisao = {s: {k: round(100 * tot[s][k] / max(1, sum(tot[s].values())), 1) for k in tot[s]} | {"n": sum(tot[s].values())} for s in "AB"}
    dados = {"A": A, "B": B, "trajetoria": traj, "confronto": confronto, "revisao": revisao}
    # tabelas por classe e por nível (duelo)
    contextos_classe = [("2-A (linear)", cq["fase2a_classe"]), ("2-B A2", cq["fase2b_classe_A2"]), ("F3 L0 (90)", cq["fase3_classe_L0"]),
                        ("F3 L1 (90)", cq["fase3_classe_L1"]), (f"F3 melhor L (qwen L{LA} × Coder L{LB})", cq["fase3_classe_melhor"])]
    linhas = []
    for i, nome in CLASSES.items():
        cels = []
        for _, lista in contextos_classe:
            x = next((r for r in lista if r["classe"].startswith(f"{i} ")), None)
            cels.append(celula_duelo(x["acerto_A"], x["acerto_B"]) if x else "<td>—</td>")
        linhas.append(f"<tr><td>{i} {nome}</td>{''.join(cels)}</tr>")
    th = "".join(f"<th>{esc(n)}</th>" for n, _ in contextos_classe)
    tab_classes = f'<div class="tabela duelo"><table><thead><tr><th>Classe</th>{th}</tr></thead><tbody>{"".join(linhas)}</tbody></table></div>'
    contextos_nivel = [("2-B A2", cq["fase2b_nivel_A2"]), ("F3 L0 (90)", cq["fase3_nivel_L0"]), ("F3 L1 (90)", cq["fase3_nivel_L1"])]
    linhas = []
    for x0 in cq["fase2b_nivel_A2"]:
        nivel = x0["nivel"]
        cels = [celula_duelo(x["acerto_A"], x["acerto_B"]) if (x := next((r for r in lista if r["nivel"] == nivel), None)) else "<td>—</td>"
                for _, lista in contextos_nivel]
        linhas.append(f"<tr><td>{esc(nivel)}</td>{''.join(cels)}</tr>")
    th = "".join(f"<th>{esc(n)}</th>" for n, _ in contextos_nivel)
    tab_niveis = f'<div class="tabela duelo"><table><thead><tr><th>Nível</th>{th}</tr></thead><tbody>{"".join(linhas)}</tbody></table></div>'
    tab_vence = tabela(["Onde", "Métrica", A, B, "Diferença", "n"],
                       [[x["onde"], x["metrica"], fmt(x["A"]), fmt(x["B"]), pp(x["delta"]), x["n"]] for x in vence])
    tab_doc = tabela(["Época", "Propostas (qwen / Coder)", "Aceitas", "Aceitação", "Tokens acrescentados", "Verbetes"],
                     [[x["epoca"], f'{x["propostas_A"]} / {x["propostas_B"]}', f'{x["aceitas_A"]} / {x["aceitas_B"]}',
                       f'{fmt(x["aceitas_pct_A"])}% / {fmt(x["aceitas_pct_B"])}%', f'{x["tokens_A"]:,} / {x["tokens_B"]:,}'.replace(",", "."),
                       f'{x["verbetes_A"]} / {x["verbetes_B"]}'] for x in cq["fase3_documentacao"]])
    tab_rec = tabela(["Versão", "hit@3 nos 90 (qwen / Coder)", "hit@3 nos 36", "Verbetes"],
                     [[f'L{x["L"]}', f'{fmt(x["hit3_90_A"])}% / {fmt(x["hit3_90_B"])}%', f'{fmt(x["hit3_36_A"])}% / {fmt(x["hit3_36_B"])}%',
                       f'{x["verbetes_A"]} / {x["verbetes_B"]}'] for x in cq["fase3_recuperacao"]])
    B_ = lambda nome: md_para_html(blocos_cq[nome]) if nome in blocos_cq else ""  # noqa: E731
    # ! Alteração de IA - Revisar: (06/10/2026) o confronto nos 36 inéditos (corrida 7) entra no cartão, na frase de abertura e numa seção própria.
    # ! Motivo: a aba dizia que a corrida 7 só rodaria "se o Eric quiser"; ele rodou em 06/10, e o resultado toca a decisão 52 (ficha 21).
    ined_cq = {x["L"]: x for x in cq.get("confronto_ineditos", [])}
    i1 = ined_cq.get(1)
    # ! Alteração de IA - Revisar: (23/10/2026) a repetição dos inéditos (corrida 15) entra no cartão, na frase de abertura e numa seção
    # própria; o veredito da ficha 21 (saldo do Coder dentro ou fora da variação entre corridas iguais) é lido de analise_fase3b.json.
    # ! Motivo: o Eric escolheu repetir a corrida antes de decidir (ficha 21, opção b); a aba precisa mostrar a repetição ao lado da corrida 7
    # e dizer o que ela decidiu, sem número digitado.
    r1 = {x["L"]: x for x in cq.get("confronto_ineditos_repeticao", [])}.get(1)
    rep_an = next((x for x in (analise3b or {}).get("repeticao", {}).get("entre_modelos", []) if x["modelo"] == B and x["biblioteca_epoca"] == 1), None)
    if rep_an:
        veredito = (f'a diferença cabe na variação normal entre corridas iguais (até {rep_an["limiar_ruido"]} casos) e a decisão 52 fica (decisão 73)' if rep_an["dentro_da_variacao"]
                    else f'a diferença passa em um caso a variação normal entre corridas iguais (até {rep_an["limiar_ruido"]} casos), mas não separa os dois; '
                         f'nos 72 casos nunca vistos o Coder acerta sozinho {rep_an["somados"]["b"]} e o qwen {rep_an["somados"]["c"]}. A decisão 52 fica, '
                         'com o saldo registrado como limitação declarada (decisão 73)')
        frase_rep = (f' Na <strong>repetição de 23/10</strong> (corrida 15, Ollama 0.40.2, a biblioteca que cada um escreveu), {r1["so_coder"]} casos só o Coder acertou contra {r1["so_qwen"]} só o qwen: '
                     f'saldo {rep_an["saldo"]:+d}, contra {rep_an["saldo_original"]:+d} na corrida 7. {veredito[0].upper() + veredito[1:]}.') if r1 else ""
    else:
        frase_rep = ""
    frase_ineditos = (f'Nos <strong>36 inéditos</strong> (corrida 7, 06/10) o Coder fica à frente com L0 e L1 (com a L1 de cada um, {i1["so_coder"]} casos só dele contra '
                      f'{i1["so_qwen"]} só do qwen, p = {fmt(i1["p_mcnemar"], 3)}) e atrás com L3; nos 72 casos com L1 o placar empata. É a condição 1 do que mudaria a decisão 52, '
                      'parcialmente cumprida e dentro do ruído: o que fazer com ela era a ficha 21.' + frase_rep if i1 else "")
    itens_kpi = [
        ("Onde o Coder fica à frente", str(n_vence), f"cenários, todos por pouco (até {pp(max_delta)}); {n_vence_36} nos 36 nunca vistos"),
        ("36 nunca vistos, 1ª corrida (06/10)", f'{i1["so_qwen"]} × {i1["so_coder"]}' if i1 else "não rodou", f'só o qwen × só o Coder; acerto {fmt(i1["acerto_A"])}% × {fmt(i1["acerto_B"])}%' if i1 else "corrida 7"),
        ("36 nunca vistos, repetição (23/10)", f'{r1["so_qwen"]} × {r1["so_coder"]}' if r1 else "não rodou",
         ('só o qwen × só o Coder' + (f'; saldo {rep_an["saldo"]:+d}' if rep_an else "")) if r1 else "corrida 15"),
        ("Melhor versão nos 36 nunca vistos", f"{fmt(melhor_A)}% × {fmt(melhor_B)}%", "acerto de cada um com a sua melhor versão"),
        ("Disputa nos 36 de avaliação", f'{c1["so_qwen"]} × {c1["so_coder"]}', f'só o qwen × só o Coder; {c1["ambos"]} acertados pelos dois'),
        ("Edições aceitas na 1ª época", f'{doc1["aceitas_A"]} × {doc1["aceitas_B"]}', f'de {doc1["propostas_A"]} × {doc1["propostas_B"]} propostas; corretas na revisão {fmt(corr["A"])}% × {fmt(corr["B"])}%'),
        ("Verbete certo entre os três (90)", f'{fmt(rec1["hit3_90_A"])}% × {fmt(rec1["hit3_90_B"])}%', f'com a 1ª versão de cada um ({rec1["verbetes_A"]} × {rec1["verbetes_B"]} verbetes)'),
        ("Chance de o Coder ser o 1º", f"≤ {fmt(100 * p_max_B)}%", f'1º em {est.get(B, 0)} × {est.get(A, 0)} de {cq["decisao"]["total_rankings"]} ordenações; {fmt(l1["s_A"])} × {fmt(l1["s_B"])} s por diagnóstico'),
    ]
    corridas = cartoes_corridas(road, numeros=["1", "7", "14", "15"], sufixo="-cq")
    html_ = f'''<section id="comparativo" hidden>
<h1>qwen2.5:7b × qwen2.5-coder:7b: em que cenários o Coder seria melhor?</h1>
<p class="lead">Pergunta do Eric em 29/09: "pode ser que em alguns cenários o coder seja mais interessante". Resposta: o Coder fica à frente em <strong>{n_vence} células</strong>, todas pequenas (a maior por {pp(max_delta)}) e quase todas nos 54 casos de aprendizado e nas classes léxica, runtime e efeito. Nos <strong>36 casos nunca vistos</strong> o qwen2.5:7b vence em todas as versões da biblioteca ({fmt(melhor_A)}% × {fmt(melhor_B)}% na melhor versão de cada um), e em nenhuma ordenação o Coder tem chance real de ser o primeiro (P(top-1) ≤ {fmt(100 * p_max_B)}%). Como escritor, o Coder é mais contido e mais certo ({fmt(corr["B"])}% de edições corretas contra {fmt(corr["A"])}%). A decisão 52 fica. {frase_ineditos}</p>
{kpis(itens_kpi)}
<h2>A trajetória dos dois pelas três fases</h2>
<p>Os mesmos casos, da Fase 2-A (sem documentação, máquina de desenvolvimento) à Fase 3 (biblioteca editada pelo próprio modelo). Nos 36 de avaliação, o qwen abre vantagem a partir da primeira versão da biblioteca escrita pelo modelo (L1); nos 90 as curvas se cruzam.</p>
<div class="controles"><label>Conjunto <select id="sel-cq-conj"><option value="36">36 de avaliação</option><option value="90">90 (todos)</option></select></label>
<label>Métrica <select id="sel-cq-met"><option value="acerto">acerto simples</option><option value="bal">acurácia balanceada</option></select></label></div>
<div class="chart"><canvas id="g-cq-traj"></canvas></div>
<h2>Quem acerta o que o outro erra</h2>
<p>Em cada condição, as barras mostram os casos em que só um dos dois acertou. Nos 36 de avaliação com a primeira versão (L1), {c1["so_qwen"]} casos são só do qwen e {c1["so_coder"]} só do Coder; {c1["ambos"]} foram acertados pelos dois. A diferença cabe na variação normal: não separa os dois.</p>
<div class="controles"><label>Conjunto <select id="sel-cq-conf"><option value="36">36 de avaliação (Fase 3)</option><option value="90">90 (2-B e Fase 3)</option></select></label></div>
<div class="chart"><canvas id="g-cq-conf"></canvas></div>
<h2>Por classe de defeito e por nível</h2>
<p>Cada célula mostra <em>qwen / Coder</em> e a diferença; a cor é a de quem está à frente (azul = qwen, verde-água = Coder) e fica mais forte quanto maior a diferença. O Coder leva vantagem em léxica, runtime e efeito; o qwen em sintática, semântica e tradução.</p>
{tab_classes}
{tab_niveis}
<h2>Como escritor da biblioteca</h2>
<p>Na época 1, o Coder propôs menos e teve aceitação igual ({fmt(doc1["aceitas_pct_A"])}% × {fmt(doc1["aceitas_pct_B"])}%), escreveu menos da metade dos tokens e não criou verbetes novos. Na revisão humana das edições aceitas, a fração correta é maior no Coder.</p>
<div class="chart baixo"><canvas id="g-cq-rev"></canvas></div>
{tab_doc}
<h2>Se o verbete certo chega entre os três entregues, e as trocas de causa respondida</h2>
<p>Com a primeira versão escrita pelo Coder (L1), o verbete certo chega entre os três entregues em {fmt(rec1["hit3_90_B"])}% dos 90 casos, contra {fmt(rec1["hit3_90_A"])}% com a do qwen. A biblioteca menor e sem verbetes novos não atrapalha a busca (BM25).</p>
{tab_rec}
{detalhes("Trocas de rótulo entre versões (autoenvenenamento, ✓→✗ e ✗→✓)", B_("cq_flips"))}
{detalhes("Rejeições do validador por modelo", B_("cq_rejeicoes"))}
<h2>Onde o Coder vence, célula a célula</h2>
{detalhes(f"As {n_vence} células em que o Coder fica à frente", tab_vence)}
<h2>A decisão, revista com os dois lado a lado</h2>
{detalhes("Regra 36 (ranking por acurácia balanceada nos 36)", B_("cq_regra36"))}
{detalhes("Bootstrap: P(top-1) e intervalos", B_("cq_bootstrap"))}
{detalhes("Escore ponderado e fronteira de Pareto", B_("cq_escore_pareto"))}
{detalhes("Ponte de versão do Ollama (0.34.0 → 0.34.1)", B_("cq_ponte"))}
{detalhes("Riscos entre fases", B_("cq_riscos"))}
<h2>Nos 36 casos inéditos (corrida 7, 06/10/2026)</h2>
<p>O Coder 7B diagnosticou os mesmos 36 casos nunca vistos que o qwen rodou em 28/09, com a biblioteca original e com as versões que ele mesmo escreveu. A tabela mostra caso a caso, por versão e por classe.</p>
{B_("cq_ineditos")}
{detalhes("Por classe, com a L1 de cada um", B_("cq_ineditos_classe"))}
<h2>Repetição nos 36 inéditos (corrida 15, 23/10/2026)</h2>
<p>Os dois modelos repetiram os mesmos 36 casos nunca vistos, cada um com a primeira versão da biblioteca que ele mesmo escreveu, numa corrida só e no Ollama 0.40.2, depois da ponte de versão (corrida 14). A primeira tabela compara os dois; a segunda mostra quanto cada modelo mudou sozinho contra a própria corrida original (corrida 2 para o qwen, 7 para o Coder).{(" " + frase_rep.strip()) if frase_rep else ""}</p>
{B_("cq_ineditos_repeticao")}
{detalhes("Cada modelo contra a própria corrida original", B_("cq_repeticao_vs_original"))}
{detalhes("Por classe, na repetição", B_("cq_ineditos_repeticao_classe"))}
<h2>As corridas desta pergunta</h2>
{corridas}
{fontes(["<code>comparativo-qwen25-7b-vs-coder-7b.md</code> (Memorial, 3-resultados-e-analises)", "<code>comparativo_qwen_coder.json</code> e <code>.md</code> gerados por <code>comparar_qwen_coder.py</code> (--check)", "<code>analise_fase3b.json</code>, bloco <code>repeticao</code> (saldo contra a variação entre corridas iguais)", "achados 4.38, 4.52 e 4.53; decisões 52 e 73"])}
</section>'''
    return dados, html_


# ------------------------------------------------------------------ 2. Fase 3-B

def secao_tres_b(ined: dict, dados: dict, road: dict, cartoes_corridas, md_doc_para_html, an: dict | None = None) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões, títulos e parágrafos à vista reescritos sem b/c, p, hit@3, L0/L1/L3 soltos nem setas.
    # ! Motivo: o texto à vista trazia siglas e números soltos (b + c, p de McNemar, hit@3) que o Eric pediu para tirar; os números continuam nas tabelas recolhidas.
    # ! Alteração de IA - Revisar: em 01/10/2026 a aba ganhou a soma dos 36 oficiais com os 36 inéditos e a tabela dos
    # casos que mudam entre corridas iguais (lidas de `analise_fase3b.json`, parâmetro `an`), e três textos mudaram: o
    # rótulo do cartão do 3B, a frase de abertura e a remissão à troca cruzada.
    # ! Motivo: o cartão dizia "a biblioteca do qwen não muda o 3B", mas nos inéditos cada modelo leu a biblioteca que
    # ele mesmo escreveu (hash 53ccf19abeac e d9a86e383103 no 3B); a abertura dizia que faltava a troca cruzada, que
    # rodou em 01/10 e ganhou aba própria.
    cur: dict = defaultdict(dict)
    for x in ined["por_modelo_biblioteca_particao"]:
        cur[x["modelo"]][str(x["biblioteca_epoca"])] = {"acerto": x["causa_correta_pct"], "bal": x["acuracia_balanceada_pct"], "s": x["segundos_mediana"]}
    modelos = [m for m in (A, B, COD3B) if m in cur]
    Ls = sorted({L for m in modelos for L in cur[m]}, key=int)
    oficial = {m: {L: {"acerto": dados["curvas"]["36"][m][L]["acerto"], "bal": dados["curvas"]["36"][m][L]["balanceada"]} for L in Ls} for m in modelos}
    rec: dict = defaultdict(dict)
    for x in ined["recuperacao"]:
        rec[x["modelo"]][str(x["biblioteca_epoca"])] = x["hit@3"]
    rec_of = {m: {L: dados["recuperacao"][m][L]["hit3_36"] for L in Ls} for m in modelos}
    par = [x for x in ined["pareado_vs_L0"] if x.get("particao", "avaliacao") == "avaliacao"]
    # ! Alteração de IA - Revisar: a aba passa a ler todas as pontes de versão (`dados["pontes"]`, montado em
    # gerar_dashboard.pontes_de_versao) e a resumir a mais recente (30/09/2026, noite).
    # ! Motivo: só a ponte de 21/09 (Ollama 0.34.1) era lida, pelo nome fixo `fase3b_ponte`; a de 30/09 (0.34.4)
    # deu o Coder 7B com b + c = 4, acima do limite da decisão 47, e o texto fixo "a ponte é pareável" ficaria errado.
    pontes = dados.get("pontes", [])
    ult = pontes[-1] if pontes else {"versao": "?", "linhas": []}
    q = cur[A]
    L_ult = Ls[-1]
    p_ult = next((x for x in par if x["modelo"] == A and str(x["biblioteca_epoca"]) == L_ult), {})
    corr3b = [c for c in road["corridas"] if c.comando and "-Modo" in c.comando]
    n_feitas = sum(c.classe == "feita" for c in corr3b)
    n_pend = sum(c.classe in ("pendente", "aguarda") for c in corr3b)
    n_opc = sum(c.classe == "opcional" for c in corr3b)
    n_par = sum(x["pareavel"] for x in ult["linhas"])
    acima = [x["modelo"] for x in ult["linhas"] if not x["pareavel"]]
    if not ult["linhas"]:
        ponte_frase = "A ponte de versão do Ollama ainda não foi registrada na decisão."
    elif acima:
        ponte_frase = (f'Na ponte de versão mais recente (Ollama {ult["versao"]}), {n_par} de {len(ult["linhas"])} modelos continuam pareáveis com a Fase 3; '
                       f'{", ".join(acima)} passou do limite e é lido contra a própria ponte.')
    else:
        ponte_frase = f'A ponte de versão mais recente (Ollama {ult["versao"]}) é pareável nos {len(ult["linhas"])} modelos.'
    dados_js = {"modelos": modelos, "Ls": Ls, "ineditos": {m: cur[m] for m in modelos}, "oficiais": oficial,
                "rec_ineditos": {m: rec[m] for m in modelos}, "rec_oficiais": rec_of}
    tab_par = tabela(["Modelo", "Versão", "Diferença contra L0", "b / c (✗→✓ / ✓→✗)", "p (McNemar exato)"],
                     [[x["modelo"], f'L{x["biblioteca_epoca"]}', pp(x.get("delta_pp")), f'{x.get("b", "—")} / {x.get("c", "—")}', fmt(x.get("p_mcnemar"), 3)] for x in par])
    tab_ponte = tabela(["Ponte", "Modelo", "Acerto em L0 (36)", "Acurácia balanceada", "b / c contra a Fase 3", "p (McNemar exato)", "Leitura"],
                       [[f'Ollama {p["versao"]}', x["modelo"], f'{fmt(x["acerto"])}%', f'{fmt(x["bal"])}%', f'{x["b"]} / {x["c"]}', fmt(x["p"], 3),
                         "pareável" if x["pareavel"] else "divergente"] for p in pontes for x in p["linhas"]])
    sec = {t[:3]: c for t, c in road["secoes"]}
    leitura_ined = next((c for t, c in road["secoes"] if t.startswith("2.1")), "")
    leitura_ponte = next(((t, c) for t, c in road["secoes"] if t.startswith("2.3")), None)
    sonda = next((c for t, c in road["secoes"] if t.startswith("3. ")), "")
    itens_kpi = [
        (f"{A} nos 36 nunca vistos", " / ".join(f'{fmt(q[L]["acerto"])}%' for L in Ls), "com a biblioteca original, a 1ª e a 3ª versão"),
        (f"{COD3B} nos 36 nunca vistos", " / ".join(f'{fmt(cur[COD3B][L]["acerto"])}%' for L in Ls) if COD3B in cur else "—", "a biblioteca que ele escreveu não muda o acerto"),
        (f"Versão {L_ult} contra a original, no qwen", pp(p_ult.get("delta_pp")), f'só a versão {L_ult} acertou {p_ult.get("b", "—")} casos; só a original, {p_ult.get("c", "—")}'),
        ("Verbete certo entre os três (qwen)", " / ".join(f'{fmt(rec[A][L])}%' for L in Ls), f'nos 36 nunca vistos; nos 36 oficiais: ' + " / ".join(f'{fmt(rec_of[A][L])}%' for L in Ls)),
        ("Ponte de versão", f"{n_par} de {len(ult['linhas'])} pareáveis", f"no Ollama {ult['versao']}; pareável = até 2 casos em que só um lado acertou"),
        ("Corridas da 3-B", f"{n_feitas} feitas · {n_pend} pendentes", f"{n_opc} opcionais"),
    ]
    # ! Alteração de IA - Revisar: (06/10/2026) as duas corridas opcionais, rodadas pelo Eric em 06/10, entram na aba lidas de
    # analise_fase3b.json: o Coder 7B contra o qwen nos mesmos inéditos (corrida 7) e a adesão cega com a L3 própria (corrida 5).
    # ! Motivo: sem isto a aba diria que as corridas eram opcionais e não rodadas, e os números ficariam só no relatório.
    entre = (an or {}).get("ineditos", {}).get("entre_modelos", [])
    a5 = (an or {}).get("a5", {}).get("linhas", [])
    c7 = {x["biblioteca_epoca"]: x for x in entre if x["modelo"] == B}
    if B in cur:
        itens_kpi.insert(2, (f"Coder 7B nos 36 nunca vistos (06/10)", " / ".join(f'{fmt(cur[B][L]["acerto"])}%' for L in Ls),
                             f'só o Coder acertou {c7[1]["b"]}, só o qwen {c7[1]["c"]}; nos 72, {c7[1]["somados"]["b"]} e {c7[1]["somados"]["c"]}' if 1 in c7 else "sem confronto"))
    if a5:
        itens_kpi.insert(3, ("Seguiu a causa errada plantada (06/10)", " · ".join(f'{fmt(l["seguiu_pct"])}%' for l in a5),
                             "; ".join(f'{NOME_CURTO.get(l["modelo"], l["modelo"])}: {l["seguiu"]} de {l["n"]}' for l in a5)))
    # a análise identifica a classe pelo id sem acento (lexica, traducao); o painel mostra o nome com acento
    classes_entre = [("".join(ch for ch in unicodedata.normalize("NFKD", nome) if not unicodedata.combining(ch)), nome) for _, nome in sorted(CLASSES.items(), key=lambda kv: int(kv[0]))]
    tab_entre = ('<div class="tabela"><table><thead><tr><th>Modelo</th><th>Biblioteca de cada um</th><th>Acerto nos 36 inéditos</th><th>Acerto do qwen2.5:7b</th>'
                 '<th>b / c (só o modelo / só o qwen)</th><th>Diferença</th><th>p (McNemar exato)</th><th>Nos 72 (oficiais + inéditos): b / c</th>'
                 + "".join(f"<th>{esc(n)}</th>" for _, n in classes_entre) + "</tr></thead><tbody>"
                 + "".join(f'<tr data-entre-modelos="{html.escape(x["modelo"] + "/L" + str(x["biblioteca_epoca"]), quote=True)}"><td>{esc(x["modelo"])}</td><td>L{x["biblioteca_epoca"]}</td>'
                           f'<td class=num>{fmt(x["acerto_pct"])}%</td><td class=num>{fmt(x["acerto_doador_pct"])}%</td><td class=num>{x["b"]} / {x["c"]}</td><td class=num>{pp(x["delta_pp"])}</td>'
                           f'<td class=num>{fmt(x["p_mcnemar"], 3)}</td><td class=num>{x["somados"]["b"]} / {x["somados"]["c"]}</td>'
                           + "".join(f'<td class=num>{x["por_classe"][i]["acertos"]} / {x["por_classe"][i]["acertos_doador"]} de {x["por_classe"][i]["n"]}</td>' if i in x["por_classe"] else "<td>n/d</td>" for i, _ in classes_entre)
                           + "</tr>" for x in entre) + "</tbody></table></div>")
    tab_a5 = ('<div class="tabela"><table><thead><tr><th>Modelo</th><th>Biblioteca</th><th>Casos</th><th>Seguiu a causa plantada</th><th>Acertou mesmo assim</th>'
              '<th>O mesmo modelo, a mesma biblioteca, na condição normal (A2, Fase 3)</th><th>Adesão cega na Fase 2-B (biblioteca original)</th></tr></thead><tbody>'
              + "".join(f'<tr data-a5="{html.escape(l["modelo"], quote=True)}"><td>{esc(l["modelo"])}</td><td>L{l["biblioteca_epoca"]} própria</td><td class=num>{l["n"]}</td>'
                        f'<td class=num>{l["seguiu"]} ({fmt(l["seguiu_pct"])}%)</td><td class=num>{l["acertos"]} ({fmt(l["acerto_pct"])}%)</td><td class=num>{fmt(l["acerto_a2_pct"])}%</td>'
                        f'<td class=num>{"não medida" if l["adesao_2b_pct"] is None else fmt(l["adesao_2b_pct"]) + "%"}</td></tr>' for l in a5) + "</tbody></table></div>")
    bloco_opcionais = ""
    if entre or a5:
        bloco_opcionais = ('<h2>As duas corridas que eram opcionais (06/10/2026)</h2>'
                           + ('<h3>Modelo contra modelo nos mesmos 36 inéditos (corrida 7)</h3><p>O Coder 7B rodou os 36 inéditos em 06/10 com a biblioteca original e com as versões que '
                              'ele mesmo escreveu; o qwen e o Coder 3B tinham rodado em 28/09. A tabela conta os casos que só o modelo da linha acertou e os que só o qwen acertou; as colunas '
                              'por classe trazem os acertos do modelo e do qwen nos 6 casos da classe.</p>' + tab_entre if entre else "")
                           + ('<h3>Se o modelo segue a documentação errada, com a biblioteca que ele escreveu (corrida 5)</h3><p>Neste teste o contexto afirma uma causa errada para o sintoma e '
                              'nunca traz o verbete certo. Na Fase 2-B isso foi medido com a biblioteca original; aqui cada modelo leu a 3ª versão que ele mesmo escreveu (L3), nos 36 oficiais.</p>' + tab_a5 if a5 else ""))
    agrupado = (an or {}).get("ineditos", {}).get("agrupado", [])
    tab_agrupado = tabela(["Modelo", "Biblioteca", "Casos", "Acerto com L0", "Acerto com a biblioteca", "Oficiais: b / c", "Inéditos: b / c", "Somados: b / c", "Diferença", "p (McNemar exato)"],
                          [[x["modelo"], f'L{x["biblioteca_epoca"]}', x["n_comuns"], f'{fmt(x["acerto_l0_pct"])}%', f'{fmt(x["acerto_pct"])}%', f'{x["oficiais"]["b"]} / {x["oficiais"]["c"]}',
                            f'{x["ineditos"]["b"]} / {x["ineditos"]["c"]}', f'{x["b"]} / {x["c"]}', pp(x["delta_pp"]), fmt(x["p_mcnemar"], 3)] for x in agrupado])
    mde = {x["n"]: x["delta_pp"] for x in (an or {}).get("ineditos", {}).get("efeito_minimo_detectavel", [])}
    maior = max((x["delta_pp"] for x in agrupado), default=None)
    frase_72 = (f'Somando os 36 oficiais e os 36 inéditos, o maior ganho é de {pp(maior)}, abaixo do efeito mínimo detectável com 72 casos ({fmt(mde.get(72))} pontos): '
                "a biblioteca fica acima de L0 nas duas versões, sem resolução estatística." if agrupado and mde.get(72) else "")
    ruido = (an or {}).get("ruido_l0", [])
    # ! Alteração de IA - Revisar: a variação entre corridas passa a ser contada com a mesma entrada (01/10/2026, depois da
    # revisão independente do relatório da 3-B): sai da conta o caso cujo texto foi corrigido entre as duas corridas.
    # ! Motivo: o `efe-3` teve o sintoma corrigido em 28/09; contá-lo como "caso que mudou entre corridas iguais" dava 4
    # casos no Coder 7B, e com a mesma entrada são 3.
    tab_ruido = tabela(["Modelo (L0, 36 casos)", "Corrida A", "Corrida B", "Casos que mudaram de acerto", "Com a mesma entrada", "Só B acertou", "Só A acertou", "Rótulos que mudaram", "Quais"],
                       [[x["modelo"], x["corrida_a"], x["corrida_b"], x["discordantes"], x.get("discordantes_mesma_entrada", x["discordantes"]), x["b"], x["c"], x.get("rotulos_diferentes", "—"),
                         ", ".join(x["casos"]) or "nenhum"] for x in ruido])
    mesma = [x.get("discordantes_mesma_entrada", x["discordantes"]) for x in ruido]
    saldo_mesma = max((abs(x.get("b_mesma_entrada", x["b"]) - x.get("c_mesma_entrada", x["c"])) for x in ruido), default=0)
    frase_ruido = (f'Com a mesma entrada, entre duas corridas iguais do mesmo modelo mudam de acerto de {min(mesma)} a {max(mesma)} casos em 36, com saldo de até {saldo_mesma}: é a régua para ler '
                   f'qualquer diferença pequena deste painel. A coluna "Casos que mudaram de acerto" conta também o efe-3, cujo texto foi corrigido em 28/09 e que não é a mesma entrada.' if ruido else "")
    html_ = f'''<section id="tresb" hidden>
<h1>Fase 3-B: o ganho da biblioteca generaliza para casos nunca vistos?</h1>
<p class="lead">Trinta e seis casos inéditos, escritos só a partir do código do sistema-cobaia e nunca vistos por nenhum modelo, foram diagnosticados com a biblioteca original (L0) e com as versões que cada modelo escreveu (L1 e L3). O qwen acerta {" → ".join(f'{fmt(q[L]["acerto"])}%' for L in Ls)}: o ganho de L1 medido nos 36 oficiais <strong>não reaparece</strong>, e L{L_ult} rende {pp(p_ult.get("delta_pp"))} (b/c {p_ult.get("b", "—")}/{p_ult.get("c", "—")}, p = {fmt(p_ult.get("p_mcnemar"), 3)}). O 3B acerta o mesmo nas três versões. {esc(frase_72)} {esc(ponte_frase)} A troca cruzada, que separa quem escreveu a biblioteca de quem a lê, tem <a href="#cruzada" data-ir="cruzada|">aba própria</a>.</p>
{kpis(itens_kpi)}
<h2>Oficiais × inéditos</h2>
<p>Linha cheia: os 36 casos oficiais de avaliação (vistos em quatro passadas por modelo). Linha tracejada: os 36 inéditos. Se o ganho fosse da biblioteca, as duas linhas subiriam juntas.</p>
<div class="controles"><label>Métrica <select id="sel-tb-met"><option value="acerto">acerto simples</option><option value="bal">acurácia balanceada</option></select></label></div>
<div class="chart"><canvas id="g-tb-gen"></canvas></div>
<h2>O verbete certo chega entre os três entregues? Nos casos nunca vistos</h2>
<p>O gráfico mostra com que frequência o verbete certo está entre os três entregues ao modelo. Nos casos nunca vistos o recuperador acerta menos e piora com as notas acrescentadas; nos oficiais fica estável.</p>
<div class="chart baixo"><canvas id="g-tb-rec"></canvas></div>
{tab_par}
{"<h2>Oficiais e inéditos somados (72 casos)</h2><p>Cada versão da biblioteca contra a original, nos dois conjuntos e na soma. A tabela conta os casos em que só a versão nova acertou e os em que só a original acertou.</p>" + tab_agrupado if agrupado else ""}
{bloco_opcionais}
<h2>Ponte de versão do Ollama</h2>
<p>A bateria oficial rodou no Ollama 0.34.0, e o Ollama se atualiza sozinho. A cada versão nova, a ponte repete a biblioteca original nos 36 casos e compara caso a caso com a Fase 3. Se até 2 casos mudam de lado (só a ponte ou só a Fase 3 acertou), as corridas dessa versão são pareáveis com a Fase 3. Acima disso, o modelo é lido contra a própria ponte e a ressalva vai para o relatório (decisão 47).</p>
{tab_ponte}
{"<h3>Quanto o resultado varia sozinho</h3><p>" + esc(frase_ruido) + "</p>" + tab_ruido if ruido else ""}
{detalhes(f"Leitura da ponte mais recente (roadmap §{leitura_ponte[0][:3]})", md_doc_para_html(leitura_ponte[1])) if leitura_ponte else ""}
<h2>Corridas da Fase 3-B</h2>
{cartoes_corridas(road, numeros=[c.numero for c in corr3b], sufixo="-3b")}
{detalhes("Primeira leitura dos inéditos (roadmap §2.1)", md_doc_para_html(leitura_ined))}
{detalhes("Sonda de detecção de correção (roadmap §3)", md_doc_para_html(sonda))}
{fontes(["<code>resultados_alvo/fase3b_ineditos/resumo_fase3.json</code> (corrida 2, 28/09) e <code>fase3b_ineditos_coder7b/</code> (corrida 7, 06/10)", "<code>resultados_alvo/fase3b_a5/</code> (corrida 5, 06/10)", "<code>decisao_modelo.json</code> (pontes de versão: " + ", ".join(p["saida"] for p in pontes) + ")", "<code>resultados_alvo/fase3/analise_fase3b.json</code> (72 casos somados, variação entre corridas, modelo contra modelo e adesão cega)", "<code>roadmap.md</code> §2, §2.1, §2.3 e §3", "achados 4.37, 4.43 e 4.44; relatório <code>fase-3b-relatorio.md</code>"])}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ 3. curadoria da L1

def secao_curadoria(cur: dict, planilha_md: str) -> tuple[dict, str]:
    cab, linhas, _ = pt.primeira_tabela(pt.sem_comentarios(planilha_md))
    col = {c: i for i, c in enumerate(cab)}
    cont: dict = defaultdict(Counter)
    for r in linhas:
        cont[r[col["Operação"]]][r[col["Avaliação"]]] += 1
    operacoes = list(cont)
    aval = Counter(r[col["Avaliação"]] for r in linhas)
    ret = cont.get("retificacao", Counter())
    dados_js = {"operacoes": operacoes, "por": {o: dict(cont[o]) for o in operacoes}}
    removidas = tabela(["#", "Caso", "Verbete", "Operação", "Texto", "Por que saiu"],
                       [[x["numero"], x["caso"], x["verbete"], x["operacao"], x["texto"], x.get("comentario", "")] for x in cur["removidas"]])
    completa = tabela(cab, [[pt.inline(c) for c in r] for r in linhas], raw=True)
    itens_kpi = [
        ("Edições da época 1", str(cur["edicoes_na_epoca"]), f'{aval.get("Correta", 0)} corretas · {aval.get("Parcial", 0)} parciais · {aval.get("Errada", 0)} erradas'),
        ("Mantidas na produção", str(cur["mantidas"]), f'{len(cur["removidas"])} removidas (avaliação {", ".join(cur["politica"].get("remover", []))})'),
        ("Retificações", f'{ret.get("Errada", 0)} de {sum(ret.values())} erradas', "a operação que mais errou"),
        ("Verbetes na cópia curada", str(cur["n_verbetes"]), f'hash {cur["hash_curada"]}'),
        ("Reconstrução conferida", "hash igual", f'reaplicar as {cur["edicoes_na_epoca"]} edições reproduz {cur["hash_oficial"]}'),
    ]
    html_ = f'''<section id="curadoria" hidden>
<h1>Curadoria da L1: o que a produção herdou da biblioteca escrita pelo modelo?</h1>
<p class="lead">A versão L1 do qwen2.5:7b foi a que mais acertou nos 36 oficiais, mas suas {cur["edicoes_na_epoca"]} edições nunca tinham sido conferidas uma a uma. A revisão contra o código do sistema-cobaia deu {aval.get("Correta", 0)} corretas, {aval.get("Parcial", 0)} parciais e {aval.get("Errada", 0)} erradas; as erradas foram removidas e a cópia de produção (<code>biblioteca_producao/</code>) ficou com {cur["mantidas"]} edições em {cur["n_verbetes"]} verbetes. Um teste reaplica todas as edições e exige o hash oficial da época 1, para a cópia ter origem rastreável.</p>
{kpis(itens_kpi)}
<h2>Acerto das edições por tipo de operação</h2>
<p>As notas (acréscimo de contexto a um verbete) são em maioria corretas ou parciais; as retificações (correção de um trecho) erram na maior parte; os verbetes novos não acertaram nenhum.</p>
<div class="chart baixo"><canvas id="g-cur-op"></canvas></div>
<h2>O que saiu da cópia de produção</h2>
{removidas}
{detalhes(f"Planilha completa da curadoria ({len(linhas)} edições)", completa)}
{leitura([
    "O ganho de L1 nos 36 oficiais veio com edições em maioria erradas ou redundantes: a forma (notas e cabeçalhos no contexto) pesou mais que a verdade do conteúdo (achado 4.35).",
    "A cópia curada é o ponto de partida da Fase 4; a versão oficial em <code>resultados_alvo/fase3/</code> não muda.",
    "Se um veredito da planilha mudar, apagar <code>biblioteca_producao/</code> e rodar <code>curar_biblioteca.py --curar</code> de novo.",
])}
{fontes(["<code>resultados_alvo/fase3/curadoria_L1__qwen2.5_7b.md</code> (planilha)", "<code>Programacao/AgenteCore/biblioteca_producao/curadoria.json</code>", "<code>curar_biblioteca.py</code>; achado 4.40; ficha 2"])}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ 4. recuperador

def secao_recuperador(rec: dict, ineditos_rec_txt: str = "") -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões e parágrafos à vista reescritos sem hit@3, hit@5, embedding solto nem "harness".
    # ! Motivo: o texto à vista trazia siglas que o Eric pediu para tirar; os números continuam nas tabelas e nos gráficos.
    res =rec["resultados"]
    metodos = list(dict.fromkeys(x["metodo"] for x in res))
    bibs = list(dict.fromkeys(x["biblioteca"] for x in res))
    conjs = list(dict.fromkeys(x["conjunto"] for x in res))
    val: dict = defaultdict(lambda: defaultdict(dict))
    for x in res:
        val[x["biblioteca"]][x["conjunto"]][x["metodo"]] = {k: x[k] for k in ("hit@1", "hit@3", "hit@5", "mrr")}
    bib0, conj0 = bibs[0], conjs[0]
    bm25 = next(m for m in metodos if m.lower().startswith("bm25"))
    v0 = val[bib0][conj0]
    ordem = sorted(metodos, key=lambda m: -v0[m]["hit@3"])
    denso = [m for m in metodos if "denso" in m.lower()]
    hib = [m for m in metodos if "híbrido" in m.lower() or "hibrido" in m.lower()]
    dados_js = {"metodos": metodos, "bibliotecas": bibs, "conjuntos": conjs, "valores": {b: {c: dict(val[b][c]) for c in val[b]} for b in val}}

    def tab_classes(conj: str) -> str:
        linhas = []
        for i, nome in CLASSES.items():
            cels = []
            for m in metodos:
                x = next((r for r in res if r["biblioteca"] == bib0 and r["conjunto"] == conj and r["metodo"] == m), None)
                v = (x or {}).get("por_classe", {}).get(str(i), {}).get("hit@3")
                cels.append(f'<td class="num" style="background:{heat(v)}">{fmt(v)}%</td>' if v is not None else "<td>—</td>")
            linhas.append(f"<tr><td>{i} {nome}</td>{''.join(cels)}</tr>")
        th = "".join(f"<th>{esc(m)}</th>" for m in metodos)
        return f'<div class="tabela heat"><table><thead><tr><th>Classe ({esc(conj)}, {esc(bib0)})</th>{th}</tr></thead><tbody>{"".join(linhas)}</tbody></table></div>'

    completa = tabela(["Biblioteca", "Conjunto", "Método", "hit@1", "hit@3", "hit@5", "MRR", "n"],
                      [[x["biblioteca"], x["conjunto"], x["metodo"], f'{fmt(x["hit@1"])}%', f'{fmt(x["hit@3"])}%', f'{fmt(x["hit@5"])}%', fmt(x["mrr"], 3), x["n"]] for x in res])
    trad = next((r for r in res if r["biblioteca"] == bib0 and r["conjunto"] == conj0 and r["metodo"] == bm25), {}).get("por_classe", {}).get("4", {}).get("hit@3")
    conj_ined = next((c for c in conjs if "inédit" in c or "inedit" in c), conjs[-1])
    melhor_hib = max(hib, key=lambda m: v0[m]["hit@3"]) if hib else None
    itens_kpi = [
        (f"Busca por palavras com sinais, BM25 ({conj0})", f'{fmt(v0[bm25]["hit@3"])}%', f'verbete certo entre os três; entre os cinco, {fmt(v0[bm25]["hit@5"])}%'),
        *([(f"{melhor_hib} ({conj0})", f'{fmt(v0[melhor_hib]["hit@3"])}%', "o melhor híbrido, entre os três")] if melhor_hib else []),
        *[(f"{m} ({conj0})", f'{fmt(v0[m]["hit@3"])}%', "verbete certo entre os três") for m in sorted(denso, key=lambda m: -v0[m]["hit@3"])][:2],
        (f"Busca por palavras (BM25) nos {conj_ined}", f'{fmt(val[bib0][conj_ined][bm25]["hit@3"])}%', "entre os três, em casos que a Fase 3 nunca viu"),
        ("Classe tradução (BM25)", f"{fmt(trad)}%", "a classe mais fraca, entre os três"),
    ]
    html_ = f'''<section id="recuperador" hidden>
<h1>Recuperador: vale trocar a busca por palavras por uma busca por significado?</h1>
<p class="lead">Não, nesta medição. A decisão 55 tinha adotado a recuperação híbrida pela literatura, sem medida própria. Medido offline com o <code>{esc(rec["metadados"]["embedding"])}</code> nos 90 casos oficiais e nos 36 inéditos, o BM25 com sinais em código chega a {fmt(v0[bm25]["hit@3"])}% de hit@3 ({fmt(v0[bm25]["hit@5"])}% em hit@5), o embedding denso a {", ".join(fmt(v0[m]["hit@3"]) + "%" for m in denso)} e o híbrido a {", ".join(fmt(v0[m]["hit@3"]) + "%" for m in hib)}: o híbrido fica <strong>abaixo do BM25 sozinho</strong>. A recuperação híbrida saiu do desenho da Fase 4 (decisão 61); o ganho barato a medir é k = 5.</p>
{kpis(itens_kpi)}
<h2>Os métodos, lado a lado</h2>
<p>Consulta em termos usa os sinais que o código extrai do caso (rota, campos, mensagens); consulta em texto usa o caso escrito por extenso. A busca por significado (embedding) só funciona razoavelmente com os termos, e mesmo assim fica longe do BM25.</p>
<div class="controles"><label>Biblioteca <select id="sel-rec-bib">{"".join(f'<option value="{esc(b)}">{esc(b)}</option>' for b in bibs)}</select></label>
<label>Métrica <select id="sel-rec-met"><option value="hit@3">hit@3</option><option value="hit@1">hit@1</option><option value="hit@5">hit@5</option><option value="mrr">MRR</option></select></label></div>
<div class="chart"><canvas id="g-rec-met"></canvas></div>
<h2>Por classe de defeito</h2>
<p>Quantas vezes o verbete certo vem entre os três entregues, por classe, na biblioteca original. A classe tradução (mapeamento entre camadas) é a mais fraca em todos os métodos; os sinais em código continuam sendo o caminho para ela.</p>
{tab_classes(conj0)}
{tab_classes(conj_ined)}
{detalhes(f"Tabela completa ({len(res)} combinações)", completa)}
{leitura([
    "O corpus é pequeno (dezenas de verbetes curtos) e a consulta é técnica e em português: a busca lexical com sinais extraídos por código vence a semântica.",
    "Trocar o modelo de busca por significado (embedding) só faria sentido se a Fase 4 mostrasse necessidade; por ora, nada muda no próprio teste.",
])}
{fontes(["<code>resultados_alvo/recuperador/experimento_recuperador.json</code> e <code>.md</code> (<code>experimento_recuperador.py</code>, --check)", "achado 4.39; decisão 61; ficha 11(f)"])}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ 5. ablação base × instruct

def secao_ablacao(abl: dict, ref3b_90, ref3b_ined) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões e parágrafo à vista reescritos sem "(A0)/(A2)", "rótulo" nem "acurácia balanceada".
    # ! Motivo: o texto à vista trazia siglas e termos de método que o Eric pediu para tirar; os números seguem na tabela recolhida.
    linhas = abl["por_modelo_condicao"]
    dados_js = {"linhas": [{"modelo": x["modelo"], "cond": x["condicao"], "acerto": x["causa_correta_pct"], "formato": x["formato_valido_pct"],
                            "fora": x["fora_do_conjunto_pct"], "ic": x["causa_correta_ic95"]} for x in linhas]}
    tab = tabela(["Modelo", "Condição", "Acerto", "IC 95%", "Campo correto", "Formato válido", "Formato ok, conteúdo errado", "Rótulo fora do conjunto", "s / caso"],
                 [[x["modelo"], x["condicao"], f'{fmt(x["causa_correta_pct"])}%', f'{fmt(x["causa_correta_ic95"][0])}–{fmt(x["causa_correta_ic95"][1])}',
                   f'{fmt(x["campo_correto_pct"])}%', f'{fmt(x["formato_valido_pct"])}%', f'{fmt(x["formato_ok_conteudo_errado_pct"])}%',
                   f'{fmt(x["fora_do_conjunto_pct"])}%', fmt(x["segundos_medio"])] for x in linhas])
    g = {(x["modelo"], x["condicao"]): x for x in linhas}
    base, inst = "qwen2.5:0.5b-base", "qwen2.5:0.5b-instruct"
    itens_kpi = [
        ("Base, sem biblioteca", f'{fmt(g[(base, "A0")]["causa_correta_pct"])}%', f'formato certo em {fmt(g[(base, "A0")]["formato_valido_pct"])}%'),
        ("Base, com biblioteca", f'{fmt(g[(base, "A2")]["causa_correta_pct"])}%', f'formato certo em {fmt(g[(base, "A2")]["formato_valido_pct"])}%; causa inventada em {fmt(g[(base, "A2")]["fora_do_conjunto_pct"])}%'),
        ("Instruct 0,5B, sem biblioteca", f'{fmt(g[(inst, "A0")]["causa_correta_pct"])}%', f'formato certo em {fmt(g[(inst, "A0")]["formato_valido_pct"])}%'),
        ("Instruct 0,5B, com biblioteca", f'{fmt(g[(inst, "A2")]["causa_correta_pct"])}%', f'o formato certo cai para {fmt(g[(inst, "A2")]["formato_valido_pct"])}%'),
        ("Referência: qwen2.5-coder:3b", f"{fmt(ref3b_90)}%", f"nos 90 casos; {fmt(ref3b_ined)}% nos nunca vistos"),
    ]
    html_ = f'''<section id="ablacao" hidden>
<h1>Sem ajuste por instrução, o modelo faz a tarefa?</h1>
<p class="lead">Não. O piso metodológico pedido na ficha 11(d): o <code>qwen2.5:0.5b-base</code> (só pré-treinado) e o <code>qwen2.5:0.5b-instruct</code> (mesmo porte, com ajuste por instrução) nos 90 casos, sem biblioteca (A0) e com a biblioteca recuperada (A2). O base acerta <strong>0 de 90</strong> nas duas condições: com a biblioteca ele copia a forma dos verbetes ({fmt(g[(base, "A2")]["formato_valido_pct"])}% no formato) mas inventa o rótulo em {fmt(g[(base, "A2")]["fora_do_conjunto_pct"])}% dos casos. O instruct de 0,5B chega a {fmt(g[(inst, "A0")]["causa_correta_pct"])}% e piora com a biblioteca. O ajuste por instrução é condição necessária, não suficiente: o piso da família está no porte.</p>
{kpis(itens_kpi)}
<h2>Acertar, responder no formato e inventar o rótulo</h2>
<p>Responder no formato e acertar são coisas diferentes, e o gráfico separa as duas. Ele também conta as causas inventadas, fora da lista permitida. A biblioteca no prompt ensina a forma ao modelo base, não o conteúdo.</p>
<div class="chart"><canvas id="g-abl"></canvas></div>
{tab}
{fontes(["<code>resultados_alvo/ablacao_base_instruct/resumo_metricas.json</code> (<code>executar_bateria.py</code>, estratégia linear, 360 inferências, 29/09)", "achado 4.41; ficha 11(d)"])}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ 6. pesquisa bibliográfica

_TOPICO = re.compile(r"^#### (\d+\.\d+\.\d+) (.+?) \(`([^`]+)` — (\d+) aprovadas?, (\d+) rejeitadas?(?:, (\d+) não verificadas?)?\)\s*$")
# ! Alteração de IA - Revisar: (01/10/2026) a lista ganhou a rodada 5 (Pré-Fase 4), os rótulos deixaram de usar
# travessão e o arquivo do mapa de filtros passou a ter nome próprio; a leitura de um mapa adotado, adiado,
# descartado saiu de dentro de secao_pesquisa para _mapa_de_vereditos, que as abas Pesquisa e "Modelos grandes pelo
# disco" usam; _secoes_do_levantamento e _pre_fase4_no_levantamento leem as sínteses e os mapas do §6.14.
# ! Motivo: secao_pesquisa lia o mapa de filtros de RODADAS[-1], "o último levantamento da lista"; com a rodada 5 no
# fim da lista ela procuraria o §6.13.10 no arquivo errado e a geração do painel pararia com ValueError. O mapa de
# filtros é o da rodada 4; o da rodada 5 (viabilidade) e as sínteses dela vão para a aba do colibri, porque é por
# ela que o Eric lê a análise que pediu em 01/10.
LEVANTAMENTO_FILTROS = "levantamento-2026-09-29-documentacao-autogerida.md"
LEVANTAMENTO_PRE_FASE4 = "levantamento-2026-10-01-pre-fase-4.md"
LEVANTAMENTO_FLUXO = "levantamento-2026-11-10-fluxo-do-agente.md"
RODADAS = [
    ("levantamento-2026-09-11-fase-3.md", "Rodadas 1 e 2 (11 e 23/09): Fase 3", "Fase 3"),
    ("levantamento-2026-09-22-llms-locais.md", "Rodada 3 (22/09): LLMs locais", "LLMs locais"),
    (LEVANTAMENTO_FILTROS, "Rodada 4 (29/09): documentação autogerida", "documentação autogerida"),
    (LEVANTAMENTO_PRE_FASE4, "Rodada 5 (01/10): Pré-Fase 4", "Pré-Fase 4"),
    # ! Alteração de IA - Revisar: (10/11/2026) a rodada 7 (as três ideias para o fluxo do agente, §6.16) entra na lista das rodadas com afirmações verificadas.
    # ! Motivo: ela teve segunda leitura de cada fonte e o cabeçalho das subseções segue o formato que esta aba lê; a rodada 6 (Pós-Fase 4, §6.15) continua fora, porque não teve verificação.
    (LEVANTAMENTO_FLUXO, "Rodada 7 (10/11): fluxo do agente", "fluxo do agente"),
]
_POR_EXTENSO = {4: "Quatro", 5: "Cinco", 6: "Seis", 7: "Sete"}


def _veredito(celula: str) -> str:
    v = re.sub(r"[*`_]", "", celula).strip().lower()  # a coluna vem em negrito no Markdown (**adotado**)
    return "adotado" if v.startswith("adot") else "adiado" if v.startswith("adia") else "descartado" if v.startswith("desc") else "outro"


def _mapa_de_vereditos(trecho: str, id_tabela: str, rotulo: str) -> tuple[str, Counter, int]:
    """A primeira tabela Tema, Opção, Veredito, Motivo, Fonte do trecho, com os botões de filtro por veredito.
    Devolve o HTML, a contagem por veredito e o número de linhas."""
    cab, linhas, _ = pt.primeira_tabela(trecho)
    col = {c: i for i, c in enumerate(cab)}
    cont = Counter(_veredito(r[col["Veredito"]]) for r in linhas)
    trs = []
    for r in linhas:
        v = _veredito(r[col["Veredito"]])
        trs.append(f'<tr data-valor="{v}"><td>{pt.inline(r[col["Tema"]])}</td><td>{pt.inline(r[col["Opção"]])}</td>'
                   f'<td>{chip(v, v)}</td><td>{pt.inline(r[col["Motivo"]])}</td><td class="nota">{pt.inline(r[col.get("Fonte", len(cab) - 1)])}</td></tr>')
    mapa = (f'<div class="filtros filtro-tabela" data-alvo="{id_tabela}" role="group" aria-label="{rotulo}">'
            f'<button type="button" data-valor="todos" aria-pressed="true">Todos ({len(linhas)})</button>'
            + "".join(f'<button type="button" data-valor="{v}" aria-pressed="false">{v.capitalize()} ({cont[v]})</button>' for v in ("adotado", "adiado", "descartado") if cont[v])
            + f'</div><div class="tabela" id="{id_tabela}"><table><thead><tr><th>Tema</th><th>Opção</th><th>Veredito</th><th>Motivo</th><th>Fonte</th></tr></thead><tbody>{"".join(trs)}</tbody></table></div>')
    return mapa, cont, len(linhas)


def _secoes_do_levantamento(lev: str) -> list[dict]:
    """As subseções de tópico de um levantamento: número, título, chave, contagens, texto da síntese, implicações
    e lacunas (o que vem sob cada título de nível 5)."""
    saida = []
    for parte in re.split(r"(?m)^(?=#### )", lev.replace("\r\n", "\n")):
        linhas = parte.split("\n")
        m = _TOPICO.match(linhas[0])
        if not m:
            continue
        blocos: dict[str, list[str]] = {}
        atual = None
        for l in linhas[1:]:
            mh = re.match(r"^##### (.+?)\s*$", l)
            if mh:
                atual = mh.group(1)
                blocos[atual] = []
            elif atual:
                blocos[atual].append(l)
        implicacoes = next((v for k, v in blocos.items() if k.startswith("Implicações")), [])
        saida.append({"secao": m.group(1), "titulo": m.group(2), "chave": m.group(3), "aprovadas": int(m.group(4)), "rejeitadas": int(m.group(5)),
                      "nao_verificadas": int(m.group(6) or 0), "texto": "\n".join(blocos.get("Texto", [])).strip(),
                      "implicacoes": [l[2:] for l in implicacoes if l.startswith("* ")],
                      "lacunas": [l[2:] for l in blocos.get("Lacunas", []) if l.startswith("* ")]})
    return saida


def _pre_fase4_no_levantamento(lev: str | None) -> dict | None:
    """Do levantamento da Pré-Fase 4 (§6.14): as subseções já integradas, as chaves dos tópicos da parte A, quantos
    tópicos ainda não rodaram, o trecho dos mapas e os números das subseções de rejeitadas e de mapas, lidos do
    próprio arquivo (§6.14.15 e §6.14.16 desde 23/10/2026; eram §6.14.12 e §6.14.13)."""
    # ! Alteração de IA - Revisar: (23/10/2026) o número da subseção dos mapas (e o das rejeitadas) passou a ser lido do
    # arquivo por expressão regular, em vez do literal "#### 6.14.13".
    # ! Motivo: com os três tópicos acrescentados à parte B em 23/10/2026, as duas subseções finais do levantamento
    # mudaram de número (§6.14.15 e §6.14.16); com o literal antigo a aba do colibri deixaria de achar o mapa.
    lev = (lev or "").replace("\r\n", "\n")
    m_mapas = re.search(r"^#### (6\.14\.\d+) Mapas adotado", lev, re.M)
    if not m_mapas:
        return None
    m_rej = re.search(r"^#### (6\.14\.\d+) Afirmações rejeitadas", lev, re.M)
    cab, linhas, _ = pt.primeira_tabela(lev)  # a primeira tabela do arquivo é a das subseções, com a parte de cada tópico
    col = {c: i for i, c in enumerate(cab)}
    parte_a = {re.sub(r"[`*]", "", r[col["Tópico"]]).strip() for r in linhas if r[col["Parte"]].strip() == "A"}
    faltam = sum(1 for r in linhas if "ainda não rodou" in r[col["Aprovadas"]])
    # ! Alteração de IA - Revisar: (05/10/2026) além do aviso "O que mudou", a aba recebe os avisos do cabeçalho sobre a
    # memória da máquina e sobre as correções da revisão, quando existem no arquivo.
    # ! Motivo: as sínteses mostradas na aba passaram a ser as corrigidas depois da revisão de 01/10; sem os avisos o
    # leitor não saberia que o texto foi corrigido, nem que "15,69 GB" é a RAM que o Windows enxerga (a instalada é 16 GB).
    avisos = [m.group(1) for titulo in ("O que mudou depois de a parte A ser escrita", "Memória da máquina", "Correções da revisão")
              for m in [re.search(r"^\d+\. (\*\*" + re.escape(titulo) + r"\.\*\* .*)$", lev, re.M)] if m]
    return {"secoes": _secoes_do_levantamento(lev), "parte_a": parte_a, "faltam": faltam, "mapas": lev[m_mapas.start():],
            "secao_mapas": m_mapas.group(1), "secao_rejeitadas": m_rej.group(1) if m_rej else "",
            "mudou": re.search(r"^\d+\. (\*\*O que mudou depois de a parte A ser escrita\.\*\* .*)$", lev, re.M), "avisos": avisos}


def secao_pesquisa() -> tuple[dict, str]:
    topicos = []
    for arquivo, rodada, curto in RODADAS:
        for l in (PESQUISA / arquivo).read_text(encoding="utf-8").splitlines():
            m = _TOPICO.match(l)
            if m:
                topicos.append({"rodada": rodada, "curto": curto, "secao": m.group(1), "titulo": m.group(2), "chave": m.group(3),
                                "aprovadas": int(m.group(4)), "rejeitadas": int(m.group(5)), "nao_verificadas": int(m.group(6) or 0)})
    n_ref = sum(1 for l in (PESQUISA / "referencias.md").read_text(encoding="utf-8").splitlines() if l.startswith("- "))
    tot_ap = sum(t["aprovadas"] for t in topicos)
    tot_rej = sum(t["rejeitadas"] for t in topicos)
    tot_nv = sum(t["nao_verificadas"] for t in topicos)
    # mapa dos filtros (rodada 4, §6.13.10)
    r4 = (PESQUISA / LEVANTAMENTO_FILTROS).read_text(encoding="utf-8")
    mapa, cont, n_filtros = _mapa_de_vereditos(r4[r4.index("#### 6.13.10"):], "tab-mapa", "Filtro do mapa")
    # rodada 5 (Pré-Fase 4): o que já foi integrado e o que ainda não rodou
    r5 = _pre_fase4_no_levantamento((PESQUISA / LEVANTAMENTO_PRE_FASE4).read_text(encoding="utf-8"))
    do_r5 = [t for t in topicos if t["curto"] == "Pré-Fase 4"]
    falta_r5 = r5["faltam"] if r5 else 0
    frase_r5 = (f' A rodada 5 (01/10) é a da Pré-Fase 4: {len(do_r5)} tópicos integrados, com {sum(t["aprovadas"] for t in do_r5)} afirmações aprovadas'
                + (f', e {falta_r5} tópicos da parte B (raciocínio aberto, memória e visualização) ainda por rodar' if falta_r5 else '')
                + '; o mapa de viabilidade e as sínteses dela estão na aba <a href="#colibri" data-ir="colibri|">Modelos grandes pelo disco</a>.') if do_r5 else ""
    # ! Alteração de IA - Revisar: (10/11/2026) frase da rodada 7 (as três ideias para o fluxo do agente, §6.16) e o aviso de que a rodada 6 não entra nesta conta.
    # ! Motivo: a aba dizia "§6.9 a §6.14" e contava cinco rodadas; a rodada 7 teve segunda leitura de cada fonte e entra na conta, e a rodada 6 (Pós-Fase 4) não teve verificação.
    do_r7 = [t for t in topicos if t["curto"] == "fluxo do agente"]
    frase_r7 = (f' A rodada 7 (10/11) pesquisou as três ideias do Eric para o fluxo do agente: {len(do_r7)} tópicos, com {sum(t["aprovadas"] for t in do_r7)} afirmações aprovadas por uma segunda '
                'leitura de cada fonte; os vereditos e as fichas estão na aba <a href="#fluxo" data-ir="fluxo|">Fluxo do agente</a>. A rodada 6 (07/11, Pós-Fase 4) não teve verificação '
                'e por isso não entra nesta conta: está na aba <a href="#posfase4" data-ir="posfase4|">Pós-Fase 4</a>.') if do_r7 else ""
    # tabela dos tópicos com barra
    trs = []
    for t in topicos:
        n = t["aprovadas"] + t["rejeitadas"] + t["nao_verificadas"]
        pa = 100 * t["aprovadas"] / n if n else 0
        pr = 100 * t["rejeitadas"] / n if n else 0
        barra = f'<div class="barra" title="{t["aprovadas"]} aprovadas, {t["rejeitadas"]} rejeitadas, {t["nao_verificadas"]} não verificadas"><span class="ap" style="width:{pa:.0f}%"></span><span class="rej" style="width:{pr:.0f}%"></span></div>'
        trs.append(f'<tr><td class="nota">{esc(t["rodada"])}</td><td>§{t["secao"]} {pt.inline(t["titulo"])}</td><td class="num">{t["aprovadas"]}</td><td class="num">{t["rejeitadas"]}</td><td class="num">{t["nao_verificadas"]}</td><td>{barra}</td></tr>')
    tab_topicos = f'<div class="tabela"><table><thead><tr><th>Rodada</th><th>Tópico</th><th>Aprovadas</th><th>Rejeitadas</th><th>Não verificadas</th><th>Proporção</th></tr></thead><tbody>{"".join(trs)}</tbody></table></div>'
    por_rodada = Counter(t["curto"] for t in topicos)
    itens_kpi = [
        ("Entradas em referencias.md", str(n_ref), "referências levantadas e deduplicadas por script"),
        ("Tópicos sintetizados", str(len(topicos)), " · ".join(f"{n} ({r})" for r, n in por_rodada.items())),
        ("Afirmações verificadas", f"{tot_ap} aprovadas", f"{tot_rej} rejeitadas · {tot_nv} não verificadas; cada uma checada por um agente cético"),
        ("Filtros para a documentação autogerida", f'{cont["adotado"]} adotados', f'{cont["adiado"]} adiados · {cont["descartado"]} descartados (rodada 4, ficha 16)'),
    ]
    n_rodadas = len(RODADAS) + 1  # o primeiro arquivo guarda as rodadas 1 e 2
    html_ = f'''<section id="pesquisa" hidden>
<h1>Pesquisa bibliográfica: o que a literatura diz e o que entrou no projeto</h1>
<p class="lead">{_POR_EXTENSO.get(n_rodadas, str(n_rodadas))} rodadas de levantamento, cada tópico pesquisado por um agente, cada afirmação verificada por outro agente cético contra a fonte, e a síntese integrada ao Memorial (§6.9 a §6.14 e §6.16) com as referências no padrão ABNT. A rodada 4 (29/09) respondeu ao pedido do Eric sobre como melhorar a documentação autogerida e evitar alucinação: {len([t for t in topicos if t["rodada"].startswith("Rodada 4")])} tópicos, {sum(t["aprovadas"] for t in topicos if t["rodada"].startswith("Rodada 4"))} afirmações aprovadas e um mapa de {n_filtros} filtros, dos quais {cont["adotado"]} entram como candidatos ao plano da Fase 4 (ficha 16).{frase_r5}{frase_r7}</p>
{kpis(itens_kpi)}
<h2>As afirmações, rodada a rodada</h2>
<div class="chart baixo"><canvas id="g-pe-rodadas"></canvas></div>
<h2>Filtros para a documentação autogerida (rodada 4)</h2>
<p>Cada linha é uma prática que a literatura sustenta, com o veredito para este projeto: <em>adotado</em> entra no plano da Fase 4, <em>adiado</em> espera medição de custo, <em>descartado</em> não cabe no desenho (prompt fixo, CPU, um modelo residente).</p>
{mapa}
<h2>Tópicos por rodada</h2>
<p>Barra verde = afirmações aprovadas; vermelha = rejeitadas; o restante, não verificadas. As rejeitadas ficam registradas com o motivo nos levantamentos.</p>
{tab_topicos}
{leitura([
    "Rodadas 1 e 2 fundamentaram a Fase 3 (tokenização, arquitetura em CPU, memória gerida pelo modelo, métricas); o mapa de decisões (§6.10) diz o que cada achado previa e o que a Fase 3 mediu.",
    "Rodada 3 avaliou o ferramental das LLMs locais: cache de respostas exato adotado, cache semântico descartado, MCP e skills descartados para o agente local.",
    "Rodada 4 é o insumo direto da ficha 16 (filtros na geração e na gestão da documentação).",
    "Rodada 5 abriu a Pré-Fase 4: rodar modelo grande lendo os pesos do disco, as pesquisas em que o colibri se apoia, modelos MoE pequenos em CPU e o atlas de especialistas."
    + (f" Os {falta_r5} tópicos sobre o raciocínio aberto ainda não rodaram." if falta_r5 else " Os tópicos sobre o raciocínio aberto também estão integrados."),
    *([("Rodada 7 respondeu à decisão 118: o raciocínio em passos, o ciclo de reavaliação e a separação de um analista de documentação, com um leitor e um verificador por tópico; "
        "nada mudou no agente, e as decisões de implementar são as fichas 65 a 67.")] if do_r7 else []),
])}
{fontes(["<code>2-pesquisa-e-literatura/levantamento-2026-09-11-fase-3.md</code>, <code>-22-llms-locais.md</code>, <code>-29-documentacao-autogerida.md</code>, <code>levantamento-2026-10-01-pre-fase-4.md</code>, <code>levantamento-2026-11-10-fluxo-do-agente.md</code>", "<code>mapa-de-decisoes-fase-3.md</code>, <code>fichamento-referencias-projeto.md</code>, <code>referencias.md</code>"])}
</section>'''
    por_afirmacoes: dict[str, dict] = {}
    for t_ in topicos:
        r_ = por_afirmacoes.setdefault(t_["curto"], {"rodada": t_["curto"], "aprovadas": 0, "rejeitadas": 0, "nao_verificadas": 0})
        for chave_ in ("aprovadas", "rejeitadas", "nao_verificadas"):
            r_[chave_] += t_[chave_]
    return {"rodadas": list(por_afirmacoes.values())}, html_


# ------------------------------------------------------------------ 7. ferramental

def secao_ferramental(med: dict | None, readme: str) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) a tabela de ferramentas vem de DETALHES-TECNICOS.md (o parâmetro continua `readme`, o texto que traz a seção "Ferramentas de apoio").
    # ! Motivo: a seção saiu do README para o documento técnico, a pedido do Eric.
    ini = readme.index("## Ferramentas de apoio")
    fim = readme.find("\n## ", ini + 5)
    cab, linhas, _ = pt.primeira_tabela(pt.sem_comentarios(readme[ini:fim if fim > 0 else None]))
    tab_ferr = tabela(cab, [[pt.inline(c) for c in r] for r in linhas], raw=True)
    dados_js: dict = {}
    bloco_mcp = ""
    if med:
        pa = med["por_agente"]
        tarefas = {"t1": "Onde a constante é usada", "t2": "Caminho entre duas funções", "t3": "Quem lê o fechamento.json"}

        def media(t, braco, campo):
            return sum(pa[f"{t}_{braco}_r{i}"][campo] for i in (1, 2)) / 2
        serie = [{"tarefa": nome, "grep_total": media(t, "grep", "total"), "mcp_total": media(t, "mcp", "total"),
                  "grep_novos": media(t, "grep", "novos"), "mcp_novos": media(t, "mcp", "novos")} for t, nome in tarefas.items()]
        sg, sm = sum(x["grep_total"] for x in serie), sum(x["mcp_total"] for x in serie)
        ng, nm = sum(x["grep_novos"] for x in serie), sum(x["mcp_novos"] for x in serie)
        var_t, var_n = 100 * (sm / sg - 1), 100 * (nm / ng - 1)
        dados_js = {"mcp": serie}
        itens_kpi = [
            ("Servidor × grep, tokens no total", pp(var_t).replace(" pp", "%"), "soma das três tarefas; a regra exigia −20%"),
            ("Servidor × grep, tokens novos", pp(var_n).replace(" pp", "%"), "sem contar a leitura de cache"),
            ("Acerto das respostas", "igual", "gabarito tirado do código por script; 12 subagentes Sonnet"),
            ("Incidentes", "0", "Defender sem detecção; nada gravado no repositório"),
            ("Veredito", "removido", "decisão 62 (regra de permanência da decisão 49)"),
        ]
        bloco_mcp = f'''<h2>O servidor de memória do código (codebase-memory-mcp)</h2>
<p>Instalado com salvaguardas em 22/09 sob uma regra fixada antes: fica só se cortar 20% ou mais dos tokens em três tarefas fixas, sem incidente. Em 29/09, com o servidor ativo, cada tarefa foi feita duas vezes só com busca de texto (grep) e duas só com o servidor, por subagentes iguais; o consumo foi somado dos transcritos com <code>medir_tokens.py --agentes</code>.</p>
{kpis(itens_kpi)}
<div class="controles"><label>Métrica <select id="sel-fer-met"><option value="total">tokens no total</option><option value="novos">tokens novos (sem leitura de cache)</option></select></label></div>
<div class="chart"><canvas id="g-fer-mcp"></canvas></div>
<p class="nota">Por que perdeu: cada chamada do subagente relê o contexto inteiro, e o braço do servidor gasta uma chamada só para carregar as ferramentas; num repositório de cerca de 80 arquivos Python, duas ou três buscas de texto já acham o que é preciso.</p>'''
    html_ = f'''<section id="ferramental" hidden>
<h1>Ferramental: o que a máquina faz antes do modelo</h1>
<p class="lead">Regra do projeto desde 21/09: <strong>primeiro a máquina, depois o modelo</strong>. Busca, contagem, render de tabela, conciliação, medição e verificação rodam em scripts locais (Python padrão, pasta <code>ferramentas/</code>); o modelo lê só o resumo. Este painel é um exemplo: todo número dele sai dos mesmos arquivos do Memorial, e o <code>--check</code> acusa qualquer edição manual.</p>
<h2>As ferramentas</h2>
{tab_ferr}
<h2>Economia de tokens</h2>
{leitura([
    "Saídas longas de testes e baterias passam pelo gancho <code>gancho_pre_bash.py</code> → <code>resumir_saida.py</code> antes de entrar no contexto.",
    "Subagentes só para trabalho mecânico e verificação de citações (modelos menores); um revisor por entregável; ondas de no máximo 30 agentes.",
    "Modelo, esforço e plugins fixados no início da sessão (cache de prefixo); regras por tipo de arquivo em <code>.claude/rules/</code>.",
    "Nenhum JSON de resultado colado em prompt: agentes leem arquivos; a medição de consumo é local (<code>medir_tokens.py</code>).",
])}
{bloco_mcp}
{fontes(["<code>DETALHES-TECNICOS.md</code> (tabela das ferramentas)", "<code>5-metodo-e-ferramental/ferramental-do-claude-code.md</code> §7.2 e §7.9", "<code>5-metodo-e-ferramental/dados/medicao-permanencia-mcp.json</code>", "decisões 49 e 62"])}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ 8. troca cruzada

# ! Alteração de IA - Revisar: aba nova (01/10/2026) com a troca cruzada da Fase 3-B: a biblioteca escrita pelo
# qwen2.5:7b lida pelos dois Coder. Tudo vem de `resultados_alvo/fase3/analise_fase3b.json` (analisar_fase3b.py).
# ! Motivo: era a última corrida prevista da 3-B e a que responde se o ganho da Fase 3 é da biblioteca ou de quem a
# lê; pela regra do painel, toda análise nova ganha aba (pergunta, resposta, números-chave, gráficos, leitura, fontes).
NOME_CURTO = {"qwen2.5:7b": "qwen2.5:7b", "qwen2.5-coder:7b": "Coder 7B", "qwen2.5-coder:3b": "Coder 3B"}
NOME_CONTRA = {"l0_ponte": "o próprio L0 na ponte (mesma versão do Ollama)", "propria": "a própria biblioteca na Fase 3",
               "doador": "o doador lendo a mesma biblioteca (Fase 3)"}


def _saldo_txt(b: int, c: int) -> str:
    s = b - c
    if s == 0:
        return "saldo zero"
    return f'{abs(s)} caso{"s" if abs(s) != 1 else ""} {"a mais" if s > 0 else "a menos"}'


def secao_cruzada(an: dict, road: dict, cartoes_corridas) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões, títulos e itens de leitura à vista reescritos sem b/c, p, L0/L1 soltos, "rótulo", setas nem o "(4 casos)" digitado à mão.
    # ! Motivo: o texto à vista trazia siglas e números soltos que o Eric pediu para tirar; o "4 casos" estava escrito no texto em vez de vir dos dados, e os números seguem nas tabelas recolhidas.
    cz, meta = an["cruzada"], an["metadados"]
    doador, leitores = meta["doador"], meta["leitores"]
    nome = lambda m: NOME_CURTO.get(m, m)  # noqa: E731
    cel = {(c["leitor"], c["origem"], c["biblioteca_epoca"]): c for c in cz["celulas"]}
    par = {(p["leitor"], p["biblioteca_epoca"], p["contra"]): p for p in cz["pareados"]}
    rot = {(r["leitor"], r["biblioteca"]): r for r in cz["rotulos"]}
    agr = {(l["modelo"], l["biblioteca_epoca"]): l for l in an["ineditos"]["agrupado"]}
    ponto = lambda c: {"acerto": c["acerto_pct"], "bal": c["acuracia_balanceada_pct"]}  # noqa: E731
    versoes = ["0", "1", "3"]
    doador_lido = {m: {"0": ponto(cel[(m, "ponte", 0)]), "1": ponto(cel[(m, "cruzada", 1)]), "3": ponto(cel[(m, "cruzada", 3)])} for m in leitores}
    propria = {m: {v: ponto(cel[(m, "fase3", int(v))]) for v in versoes} for m in [doador] + leitores}
    # rótulos curtos: o eixo do gráfico corta o começo de um rótulo comprido
    trocas = [{"leitor": doador, "epoca": e, "rot": f"{nome(doador)} · própria L{e}", "b": agr[(doador, e)]["oficiais"]["b"], "c": agr[(doador, e)]["oficiais"]["c"]}
              for e in (1, 3) if (doador, e) in agr]
    trocas += [{"leitor": m, "epoca": e, "rot": f"{nome(m)} · L{e} do doador", "b": par[(m, e, "l0_ponte")]["b"], "c": par[(m, e, "l0_ponte")]["c"]} for m in leitores for e in (1, 3)]
    dados_js = {"doador": doador, "leitores": leitores, "versoes": versoes, "doador_lido": doador_lido, "propria": propria, "trocas": trocas}

    q1 = cel[(doador, "fase3", 1)]
    versao = meta["versao_da_ponte_de_base"]
    frases = [f'{nome(m)}: {fmt(cel[(m, "ponte", 0)]["acerto_pct"])}% com a biblioteca original e {fmt(cel[(m, "cruzada", 1)]["acerto_pct"])}% com a L1 do {nome(doador)} '
              f'({_saldo_txt(par[(m, 1, "l0_ponte")]["b"], par[(m, 1, "l0_ponte")]["c"])})' for m in leitores]
    pior = min(leitores, key=lambda m: par[(m, 1, "l0_ponte")]["b"] - par[(m, 1, "l0_ponte")]["c"])
    r_pior = rot[(pior, "L1 do doador")]
    ruido = an["ruido_l0"]
    itens_kpi = [(f"{nome(m)} lendo a biblioteca do {nome(doador)}", f'de {fmt(cel[(m, "ponte", 0)]["acerto_pct"])}% para {fmt(cel[(m, "cruzada", 1)]["acerto_pct"])}%',
                  f'contra a biblioteca original: {_saldo_txt(par[(m, 1, "l0_ponte")]["b"], par[(m, 1, "l0_ponte")]["c"])}') for m in leitores]
    itens_kpi += [
        ("A mesma biblioteca, lida por quem a escreveu", f'{fmt(q1["acerto_pct"])}%', "contra ele: " + "; ".join(f'{nome(m)} {_saldo_txt(par[(m, 1, "doador")]["b"], par[(m, 1, "doador")]["c"])}' for m in leitores)),
        (f"Causa que o {nome(pior)} passa a responder", f'de {r_pior["respostas_no_rotulo_com_l0"]} para {r_pior["respostas_no_rotulo"]} respostas',
         f'{r_pior["rotulo_mais_frequente"]}; ' + ("nenhum dos 36 casos tem essa causa" if r_pior["casos_com_esse_gabarito"] == 0 else f'{r_pior["casos_com_esse_gabarito"]} dos 36 casos têm essa causa')),
        ("Contextos com nota do doador", f'{fmt(cel[(pior, "cruzada", 1)]["contexto_com_nota_pct"])}%',
         "na própria: " + "; ".join(f'{nome(m)} {fmt(cel[(m, "fase3", 1)]["contexto_com_nota_pct"])}%' for m in leitores)),
        ("Variação entre corridas iguais", f'{min(x["discordantes_mesma_entrada"] for x in ruido)} a {max(x["discordantes_mesma_entrada"] for x in ruido)} casos',
         f'em 36, saldo de até {max(abs(x["b_mesma_entrada"] - x["c_mesma_entrada"]) for x in ruido)}; régua para os saldos acima'),
    ]
    linhas_par = "".join(
        f'<tr data-valor="{p["contra"]}"><td>{esc(nome(p["leitor"]))} lendo L{p["biblioteca_epoca"]}</td><td>{esc(NOME_CONTRA[p["contra"]])}</td>'
        f'<td>{"sim" if p["pareavel_pela_ponte"] else "não"}</td><td class=num>{p["b"]} / {p["c"]}</td>'
        f'<td class=num>{pp(p["delta_pp"])}</td><td class=num>{fmt(p["p_mcnemar"], 3)}</td><td class=num>{p["b_mesma_entrada"]} / {p["c_mesma_entrada"]}</td><td class=num>{p["rotulos_diferentes"]}</td></tr>'
        for p in cz["pareados"])
    cont = Counter(p["contra"] for p in cz["pareados"])
    tab_par = ('<div class="filtros filtro-tabela" data-alvo="tab-cz-par" role="group" aria-label="Filtro dos pareamentos">'
               f'<button type="button" data-valor="todos" aria-pressed="true">Todos ({len(cz["pareados"])})</button>'
               + "".join(f'<button type="button" data-valor="{k}" aria-pressed="false">Contra {esc(NOME_CONTRA[k])} ({cont[k]})</button>' for k in NOME_CONTRA if cont[k])
               + '</div><div class="tabela" id="tab-cz-par"><table><thead><tr><th>Leitor e biblioteca do doador</th><th>Comparado com</th><th>Pareável pela ponte</th>'
               f'<th>b / c</th><th>Diferença</th><th>p (McNemar exato)</th><th>b / c sem o caso de texto corrigido</th><th>Rótulos que mudaram</th></tr></thead><tbody>{linhas_par}</tbody></table></div>')
    # as listas de casos de cada pareamento ficam num bloco recolhido: na tabela principal elas a deixavam larga demais
    tab_par_casos = tabela(["Leitor e biblioteca do doador", "Comparado com", "Ganhou", "Perdeu", "Trocas em casos que já oscilam entre corridas de L0"],
                           [[f'{nome(p["leitor"])} lendo L{p["biblioteca_epoca"]}', NOME_CONTRA[p["contra"]], ", ".join(p["ganhos"]) or "nenhum", ", ".join(p["perdas"]) or "nenhum",
                             (", ".join(p["em_casos_que_oscilam"]) or "nenhuma") if p["contra"] == "l0_ponte" else "—"] for p in cz["pareados"]])
    classes = list(dict.fromkeys(l["classe"] for l in cz["por_classe"]))
    por_classe = {(l["leitor"], l["biblioteca"], l["classe"]): l for l in cz["por_classe"]}
    tab_classe = tabela(["Quem lê", "Biblioteca lida"] + classes,
                        [[nome(m), b] + [f'{por_classe[(m, b, c)]["acertos"]} / {por_classe[(m, b, c)]["n"]}' if (m, b, c) in por_classe else "—" for c in classes]
                         for m, b in dict.fromkeys((l["leitor"], l["biblioteca"]) for l in cz["por_classe"])])
    tab_celulas = tabela(["Quem lê", "Biblioteca lida", "Acerto nos 36", "IC 95%", "Acurácia balanceada", "Contexto com nota", "Citou verbete anotado", "Tokens de entrada", "s por diagnóstico"],
                         [[nome(c["leitor"]), c["biblioteca"], f'{fmt(c["acerto_pct"])}%', f'{fmt(c["ic95"][0])} a {fmt(c["ic95"][1])}', f'{fmt(c["acuracia_balanceada_pct"])}%',
                           f'{fmt(c["contexto_com_nota_pct"])}%', f'{fmt(c["citou_verbete_anotado_pct"])}%', fmt(c["tokens_entrada_mediana"], 0), fmt(c["segundos_mediana"])] for c in cz["celulas"]])
    tab_rot = tabela(["Quem lê", "Biblioteca lida", "Rótulo mais respondido", "Respostas com ele", "Com L0", "Casos com essa causa", "Verbetes mais citados como fonte", "Verbetes mais presentes no contexto"],
                     [[nome(r["leitor"]), r["biblioteca"], r["rotulo_mais_frequente"], f'{r["respostas_no_rotulo"]} ({fmt(r["parcela_rotulo_pct"])}%)', r["respostas_no_rotulo_com_l0"], r["casos_com_esse_gabarito"],
                       "; ".join(f'{x["verbete"]} ({x["respostas"]})' for x in r["fontes_mais_citadas"]), "; ".join(f'{x["verbete"]} ({x["casos"]})' for x in r["verbetes_mais_presentes"])] for r in cz["rotulos"]])
    tab_casos = tabela(["Quem lê", "Biblioteca", "Caso", "Passou a", "Causa do gabarito", "Resposta com L0", "Resposta com a biblioteca do doador", "Fonte citada", "Verbete de ouro no contexto", "O doador acerta"],
                       [[nome(c["leitor"]), f'L{c["biblioteca_epoca"]}', c["caso"], c["mudou_para"], c["esperado"], c["resposta_l0"], c["resposta"], ", ".join(c["fontes_citadas"]) or "—",
                         "sim" if c["ouro_no_contexto"] else "não", "sim" if c["doador_acertou"] else "não"] for c in cz["casos"]])
    perdas_pior = [c for c in cz["casos"] if c["leitor"] == pior and c["biblioteca_epoca"] == 1 and c["mudou_para"] == "errado"]
    no_rotulo = sum(1 for c in perdas_pior if c["resposta"] == r_pior["rotulo_mais_frequente"])
    com_ouro = sum(1 for c in perdas_pior if c["ouro_no_contexto"])
    fonte_top = r_pior["fontes_mais_citadas"][0] if r_pior["fontes_mais_citadas"] else None
    melhor = max(leitores, key=lambda m: par[(m, 1, "l0_ponte")]["b"] - par[(m, 1, "l0_ponte")]["c"])
    itens_leitura = [
        f'<strong>O ganho não é da biblioteca sozinha.</strong> Lida por quem a escreveu, a primeira versão (L1) rende {fmt(q1["acerto_pct"])}%. Lida pelo {esc(nome(melhor))}, fica com {_saldo_txt(par[(melhor, 1, "l0_ponte")]["b"], par[(melhor, 1, "l0_ponte")]["c"])} '
        f'sobre a biblioteca original, dentro da variação entre corridas ({len(par[(melhor, 1, "l0_ponte")]["em_casos_que_oscilam"])} das {par[(melhor, 1, "l0_ponte")]["b"] + par[(melhor, 1, "l0_ponte")]["c"]} trocas caem em casos que já '
        f'oscilam sozinhos). Lida pelo {esc(nome(pior))}, fica com {_saldo_txt(par[(pior, 1, "l0_ponte")]["b"], par[(pior, 1, "l0_ponte")]["c"])}: é o único saldo fora dessa variação, e ainda assim pequeno demais para valer como prova.',
        f'<strong>No {esc(nome(pior))} as notas do doador são lidas e seguidas, para pior.</strong> Ele passa a responder <code>{esc(r_pior["rotulo_mais_frequente"])}</code> ({r_pior["respostas_no_rotulo_com_l0"]} respostas com a biblioteca original, {r_pior["respostas_no_rotulo"]} com a do doador), '
        + ("causa que nenhum dos 36 casos tem" if r_pior["casos_com_esse_gabarito"] == 0 else f'causa de {r_pior["casos_com_esse_gabarito"]} dos 36 casos') + (f', e cita <code>{esc(fonte_top["verbete"])}</code> como fonte em {fonte_top["respostas"]} respostas' if fonte_top else "") +
        f'. Em {no_rotulo} das {len(perdas_pior)} perdas a resposta nova é essa causa, e em {com_ouro} das {len(perdas_pior)} o verbete certo estava no contexto: nessas, a falha é de uso, não de busca. '
        f'A causa respondida muda em {par[(pior, 1, "l0_ponte")]["rotulos_diferentes"]} das 36 respostas; entre corridas iguais dele muda de {min(x["rotulos_diferentes"] for x in ruido if x["modelo"] == pior)} a '
        f'{max(x["rotulos_diferentes"] for x in ruido if x["modelo"] == pior)}.',
        f'<strong>O que a cruzada não separa.</strong> O ganho medido na Fase 3 não acompanha a biblioteca quando muda quem a lê, mas o {esc(nome(doador))} não leu a biblioteca de outro modelo: não dá para dizer se o ganho é '
        "do par (o modelo com a biblioteca que ele mesmo escreveu) ou do leitor. E o ganho dele com a biblioteca que ele mesmo escreveu também cabe na variação normal.",
        f'<strong>O que fica para a Fase 4.</strong> O padrão do agente é o {esc(nome(doador))} com a biblioteca que ele mesmo escreveu (decisão 69): trocar o modelo que lê exige medir de novo, e a ideia de escrever com o melhor '
        "modelo e ler com o mais barato sai. Uma nota em verbete que aparece em quase metade dos contextos alcança quase metade dos diagnósticos.",
    ]
    numeros = [c.numero for c in road["corridas"] if c.saida in (meta["fontes"]["cruzada"], meta["ponte_de_base"])]
    html_ = f'''<section id="cruzada" hidden>
<h1>Troca cruzada: o ganho é da biblioteca ou de quem a lê?</h1>
<p class="lead">Não é da biblioteca sozinha. Os dois Coder diagnosticaram os mesmos 36 casos, com o mesmo prompt e a mesma busca, lendo a biblioteca escrita pelo {esc(nome(doador))}. {esc("; ".join(frases))}. Lida por quem a escreveu, a mesma L1 rende {fmt(q1["acerto_pct"])}%. O ganho medido na Fase 3 não acompanha a biblioteca quando muda quem a lê.</p>
{kpis(itens_kpi)}
<h2>Acerto por versão da biblioteca, por quem lê</h2>
<p>Linha cheia: a biblioteca escrita pelo {esc(nome(doador))} (no primeiro ponto, a biblioteca original; para os dois Coder, medida na ponte em Ollama {esc(versao)}). Linha tracejada: cada Coder lendo a biblioteca que ele mesmo escreveu, na Fase 3. Se o ganho fosse da biblioteca, as linhas cheias subiriam juntas.</p>
<div class="controles"><label>Métrica <select id="sel-cz-met"><option value="acerto">acerto simples</option><option value="bal">acurácia balanceada</option></select></label></div>
<div class="chart"><canvas id="g-cz-leit"></canvas></div>
<h2>Casos ganhos e perdidos contra a biblioteca original, no mesmo modelo</h2>
<p>Cada barra compara um modelo com uma versão da biblioteca contra ele mesmo com a biblioteca original: à direita os casos que passou a acertar, à esquerda os que deixou de acertar. Os dois Coder são comparados na mesma versão do Ollama (ponte de 30/09); o {esc(nome(doador))}, dentro da Fase 3.</p>
<div class="chart"><canvas id="g-cz-trocas"></canvas></div>
<h2>Cada comparação, uma a uma</h2>
<p>A tabela conta os casos que só o leitor com a biblioteca do doador acertou e os que só o outro lado acertou. Só a comparação contra a ponte é feita na mesma versão do Ollama e com o mesmo texto dos casos; as outras duas cruzam versões e, para o Coder 7B, não são pareáveis (decisão 47). Nelas, a coluna "sem o caso de texto corrigido" tira o efe-3, corrigido em 28/09.</p>
{tab_par}
{detalhes("Casos ganhos e perdidos em cada pareamento", tab_par_casos)}
<h2>Leitura</h2>
{leitura(itens_leitura)}
{detalhes("Todas as células: quem lê, o que lê e quanto acerta", tab_celulas)}
{detalhes("Acertos por classe de defeito (6 casos por classe)", tab_classe)}
{detalhes("Rótulo mais respondido e verbetes citados", tab_rot)}
{detalhes("Casos que mudaram contra o próprio L0, um a um", tab_casos)}
<h2>As corridas</h2>
{cartoes_corridas(road, numeros=numeros, sufixo="-cz")}
{fontes(["<code>resultados_alvo/fase3/analise_fase3b.json</code> e <code>.md</code>, gerados por <code>analisar_fase3b.py</code> (--check)", "<code>resultados_alvo/fase3b_cruzada_qwen/</code> e <code>fase3b_ponte_0344/</code>", "relatório <code>fase-3b-relatorio.md</code> §5 e §6", "achados 4.42 e 4.43; decisão 69"])}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ 9. fechamento das Fases 3 e 3-B

# ! Alteração de IA - Revisar: aba nova (01/10/2026) com a lista de fechamento das Fases 3 e 3-B, lida da tabela do
# §9 de `3-resultados-e-analises/fase-3b-relatorio.md`, e com as fichas de pendência que continuam abertas.
# ! Motivo: o Eric pediu a verificação de que todos os tópicos das duas fases podem ser dados por concluídos antes de
# passar o planejamento da Fase 4; ele decide pelo painel, e a resposta precisa estar numa tela só, tópico por tópico.
ESTADOS_FECHAMENTO = {"concluido": ("Concluído", "concluida"), "ressalva": ("Concluído com ressalva", "andamento"),
                      "nao_rodado": ("Não rodado", "opcional"), "descartado": ("Descartado", "descartado"), "outro": ("Em aberto", "outro")}


def _classe_fechamento(estado: str) -> str:
    e = estado.strip().lower()
    if "ressalva" in e:
        return "ressalva"
    if e.startswith("conclu"):
        return "concluido"
    if e.startswith("não rodado") or e.startswith("nao rodado"):
        return "nao_rodado"
    if e.startswith("descartado"):
        return "descartado"
    return "outro"


def secao_fechamento(relatorio_md: str, pend: list, md_doc_para_html) -> tuple[dict, str]:
    md = pt.sem_comentarios(relatorio_md)
    secs = {t.split(".")[0]: c for t, c in pt.secoes(md) if t and t[0].isdigit()}
    cab, linhas, _ = pt.primeira_tabela(secs["9"])
    col = {c: i for i, c in enumerate(cab)}
    cont = Counter(_classe_fechamento(r[col["Estado"]]) for r in linhas)
    abertas = [f for b in pend for f in b.fichas if f.aberta]
    trs = "".join(
        f'<tr data-valor="{_classe_fechamento(r[col["Estado"]])}"><td class=num>{esc(r[col["#"]])}</td><td>{pt.inline(r[col["Tópico"]])}</td><td>{esc(r[col["Fase"]])}</td>'
        f'<td>{chip(ESTADOS_FECHAMENTO[_classe_fechamento(r[col["Estado"]])][1], r[col["Estado"]])}</td><td>{pt.inline(r[col["Evidência"]])}</td><td>{pt.inline(r[col["O que fica"]])}</td></tr>'
        for r in linhas)
    tab = ('<div class="filtros filtro-tabela" data-alvo="tab-fechamento" role="group" aria-label="Filtro do fechamento">'
           f'<button type="button" data-valor="todos" aria-pressed="true">Todos ({len(linhas)})</button>'
           + "".join(f'<button type="button" data-valor="{k}" aria-pressed="false">{esc(ESTADOS_FECHAMENTO[k][0])} ({cont[k]})</button>' for k in ESTADOS_FECHAMENTO if cont[k])
           + '</div><div class="tabela" id="tab-fechamento"><table><thead><tr><th>#</th><th>Tópico</th><th>Fase</th><th>Estado</th><th>Evidência</th><th>O que fica</th></tr></thead>'
           f'<tbody>{trs}</tbody></table></div>')
    fechado = cont["outro"] == 0
    resposta = ("Sim. Nenhum tópico obrigatório está aberto." if fechado else f'Ainda não: {cont["outro"]} tópico(s) em aberto.')
    lista = "".join(f'<li><a href="#{f.id_html}" data-ir="pendencias|{f.id_html}"><span class="numero">{f.numero}</span> {pt.inline(f.titulo)}</a>'
                    f'<br><span class="nota">Recomendação: {pt.inline(f.campos.get("Recomendação", "—"))}</span></li>' for f in abertas)
    itens_kpi = [
        ("Concluídos", str(cont["concluido"]), f"de {len(linhas)} tópicos"),
        ("Concluídos com ressalva", str(cont["ressalva"]), "a ressalva está na coluna O que fica"),
        ("Não rodados", str(cont["nao_rodado"]), "corridas opcionais ou inviáveis; o motivo está na tabela"),
        ("Descartados com motivo", str(cont["descartado"]), "registrados para o texto final"),
        ("Decisões do Eric em aberto", str(len(abertas)), "fichas na aba Pendências; não impedem o planejamento da Fase 4" if abertas else "nenhuma ficha aberta"),
    ]
    html_ = f'''<section id="fechamento" hidden>
<h1>Fechamento: as Fases 3 e 3-B podem ser dadas por concluídas?</h1>
<p class="lead">{esc(resposta)} Dos {len(linhas)} tópicos, {cont["concluido"]} estão concluídos, {cont["ressalva"]} concluídos com ressalva declarada, {cont["nao_rodado"]} não rodaram (corridas opcionais ou inviáveis) e {cont["descartado"]} {"foi descartado" if cont["descartado"] == 1 else "foram descartados"} com motivo. {"Faltam " + str(len(abertas)) + " decisões do Eric, que não impedem o planejamento da Fase 4." if abertas else "Não há decisão pendente."}</p>
{kpis(itens_kpi)}
<h2>O que depende do Eric</h2>
{"<ol class='lista-eric'>" + lista + "</ol>" if abertas else "<p>Nenhuma ficha aberta.</p>"}
<h2>Tópico por tópico</h2>
{tab}
{detalhes("O que muda e o que não muda com a Fase 3-B (relatório §7)", md_doc_para_html(secs.get("7", "")))}
{detalhes("O que a literatura previa e o que saiu (relatório §6)", md_doc_para_html(secs.get("6", "")))}
{detalhes("Limitações que ficam (relatório §8)", md_doc_para_html(secs.get("8", "")))}
{fontes(["<code>3-resultados-e-analises/fase-3b-relatorio.md</code> §6 a §9", "<code>pendencias.md</code> (fichas abertas)", "<code>roadmap.md</code>"])}
</section>'''
    return {"contagem": dict(cont), "fichas_abertas": len(abertas), "fechado": fechado}, html_


# ------------------------------------------------------------------ 10. Pré-Fase 4: modelos grandes pelo disco

# ! Alteração de IA - Revisar: aba nova (01/10/2026) da Pré-Fase 4: a conta de viabilidade do repositório colibri nesta
# máquina, a leitura medida do NVMe e a amostra de probabilidades por token do Ollama.
# ! Motivo: o Eric pediu a viabilidade de rodar modelo grande lendo os pesos do disco, só com CPU, com ganhos e custos, e
# a regra do painel é uma aba por análise. Todo número vem de resultados_alvo/pre_fase4/viabilidade_modelos_grandes.json
# (gerado por viabilidade_modelos_grandes.py, com --check) e da amostra gravada por sondar_logprobs.py; a comparação de
# tempos mistura duas grandezas de propósito e diz isso no gráfico: o tempo de hoje é o do diagnóstico inteiro, e o do
# colibri é só o da geração da resposta, porque o repositório não mede a leitura do prompt em máquina pequena.

def _milhar(v) -> str:
    return f"{float(v):,.0f}".replace(",", ".")


def _amostra_de_tokens(amostra: dict | None) -> dict | None:
    """Da amostra de sondar_logprobs.py: os tokens da primeira linha da resposta, com a probabilidade de cada um, e as
    alternativas no ponto em que o modelo escolhe a causa (o primeiro token depois de 'CAUSA_RAIZ:')."""
    lp = ((((amostra or {}).get("chamadas") or {}).get("a") or {}).get("resposta") or {}).get("logprobs") or []
    if not lp:
        return None
    linha, acumulado, i_rotulo = [], "", None
    for i, t in enumerate(lp):
        if i_rotulo is None and re.search(r"CAUSA_RAIZ\s*:\s*$", acumulado) and t["token"].strip():
            i_rotulo = i
        linha.append({"token": t["token"], "p": math.exp(t["logprob"])})
        acumulado += t["token"]
        if "\n" in t["token"]:
            break
    alternativas = ([{"token": a["token"], "p": math.exp(a["logprob"])} for a in (lp[i_rotulo].get("top_logprobs") or [])[:5]]
                    if i_rotulo is not None else [])
    return {"linha": linha, "alternativas": alternativas, "rotulo": acumulado.split(":", 1)[1].strip() if ":" in acumulado else ""}


# ! Alteração de IA - Revisar: (01/10/2026) bloco "O que a literatura sustenta" da aba do colibri, lido do levantamento
# §6.14: o mapa adotado, adiado, descartado da parte A com filtro por veredito, os riscos, a leitura do mapa e as
# sínteses verificadas por extenso, recolhidas.
# ! Motivo: o Eric pediu "uma análise densa do conteúdo e das pesquisas que ele se baseia" com ganhos e custos, e
# decide pelo painel, não pelo arquivo .md; sem este bloco a análise ficaria só no levantamento. Nada é digitado aqui:
# o texto vem do arquivo gerado por integrar_pesquisa_pre_fase4.py, inclusive o aviso do que mudou depois de a parte A
# ser escrita (a sonda de probabilidades e a decisão do Eric sobre a telemetria).
def _literatura_do_colibri(lev: str | None) -> tuple[str, list[tuple[str, str, str]], str | None]:
    """Devolve o HTML do bloco, os cartões de número-chave que ele acrescenta e a linha de fonte."""
    lit = _pre_fase4_no_levantamento(lev)
    if not lit:
        return ('<p class="nota">A rodada 5 da pesquisa (o repositório por inteiro, as pesquisas que ele cita, inferência com os pesos fora da RAM, modelos MoE '
                'pequenos e atlas de especialistas) ainda não foi integrada ao levantamento, como §6.14.</p>'), [], None
    mapa, cont, n = _mapa_de_vereditos(lit["mapas"], "tab-mapa-co", "Filtro do mapa de viabilidade")
    _, riscos, _ = pt.primeira_tabela(lit["mapas"][lit["mapas"].index("**Riscos**"):])
    tab_riscos = ('<div class="tabela"><table><thead><tr><th>Risco</th><th>Mitigação</th><th>Fonte</th></tr></thead><tbody>'
                  + "".join(f'<tr data-risco="{i}"><td>{pt.inline(r[0])}</td><td>{pt.inline(r[1])}</td><td class="nota">{pt.inline(r[2])}</td></tr>' for i, r in enumerate(riscos, 1))
                  + "</tbody></table></div>")
    resto = lit["mapas"][lit["mapas"].index("**Leitura**") + len("**Leitura**"):]
    fim = resto.find("\n**Parte ")
    leitura_do_mapa = pt.md_doc_para_html((resto if fim < 0 else resto[:fim]).strip())
    secoes = [s for s in lit["secoes"] if s["chave"] in lit["parte_a"]]
    aprovadas, rejeitadas = sum(s["aprovadas"] for s in secoes), sum(s["rejeitadas"] for s in secoes)
    sinteses = "".join(
        f'<details data-sintese="{html.escape(s["chave"], quote=True)}"><summary>§{s["secao"]} {esc(s["titulo"])} ({s["aprovadas"]} afirmações aprovadas)</summary>'
        f'<div class="relatorio">{pt.md_doc_para_html(s["texto"])}<h4>O que isso implica para o agente e para a Fase 4</h4>{leitura([pt.inline(x) for x in s["implicacoes"]])}'
        f'<h4>O que a literatura não responde</h4>{leitura([pt.inline(x) for x in s["lacunas"]])}</div></details>' for s in secoes)
    mudou = "".join(f'<p class="nota">{pt.inline(a)}</p>' for a in lit["avisos"])  # o que mudou, a memória da máquina e as correções da revisão
    bloco = f'''<h2>O que a literatura sustenta</h2>
<p>A rodada 5 da pesquisa leu o repositório por inteiro, as pesquisas que ele cita e a literatura independente sobre inferência com os pesos fora da RAM: {len(secoes)} tópicos, {aprovadas} afirmações aprovadas por verificadores céticos e {rejeitadas} {"rejeitada" if rejeitadas == 1 else "rejeitadas"}. O mapa dá o veredito de cada opção para esta máquina: <em>adotado</em> serve agora, sem trocar o modelo decidido; <em>adiado</em> só serviria com outra máquina, outro motor ou depois da Fase 4; <em>descartado</em> não serve, com o motivo.</p>
{mapa}
{mudou}
{detalhes("Riscos que a literatura aponta e a mitigação de cada um", tab_riscos)}
{detalhes("Leitura do mapa, por extenso", leitura_do_mapa)}
<h3>As sínteses, por extenso</h3>
<p>Cada síntese foi escrita só com as afirmações que sobreviveram à verificação. As referências completas e as afirmações rejeitadas, com o motivo, estão no levantamento (§{lit["secao_rejeitadas"]}) e em <code>referencias.md</code>.</p>
{sinteses}'''
    cartoes = [("Opções avaliadas pela literatura", f'{cont["adotado"]} adotadas', f'{cont["adiado"]} adiadas · {cont["descartado"]} descartadas, de {n} no mapa da rodada 5')]
    fonte = f'<code>2-pesquisa-e-literatura/{LEVANTAMENTO_PRE_FASE4}</code> (§{secoes[0]["secao"]} a §{secoes[-1]["secao"]} e mapa em §{lit["secao_mapas"]})' if secoes else None
    return bloco, cartoes, fonte


def secao_colibri(v: dict | None, amostra: dict | None, road: dict, cartoes_corridas, levantamento: str | None = None) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões de RAM, leitura do disco e resposta em máquina parecida encurtados, e "rótulo" trocado por "causa respondida" no texto à vista.
    # ! Motivo: os cartões passavam de 90 caracteres com detalhes que já estão nas tabelas recolhidas (leituras, blocos, threads); o texto usava "rótulo", termo que o Eric pediu para tirar.
    titulo = "Dá para rodar nesta máquina um modelo gigante lendo os pesos do disco?"
    if not v:
        return {"barras": []}, (f'<section id="colibri" hidden>\n<h1>{titulo}</h1>\n<p class="lead">As sondas da Pré-Fase 4 ainda não foram rodadas '
                                'nesta máquina: faltam <code>resultados_alvo/pre_fase4/disco.json</code> e <code>viabilidade_modelos_grandes.json</code> '
                                '(<code>python ferramentas/medir_disco.py</code> e <code>python viabilidade_modelos_grandes.py</code>).</p>\n</section>')
    maq, med, meta = v["maquina"], v["medianas_do_agente"], v["metadados"]
    fam = v["familias"]
    # ! Alteração de IA - Revisar: (01/10/2026, tarde) o veredito de cada modelo passou a ter três estados: roda com
    # folga, fica no limite (cabe no disco livre e pede exatamente a RAM instalada) ou não roda.
    # ! Motivo: a conta comparava o "16 GB min" do repositório com os 15,69 GB que o Windows enxerga e a aba dizia que a
    # RAM mínima "passa da instalada"; a máquina tem 16 GB instalados, o mínimo declarado. A resposta da aba fica mais
    # exata: um modelo roda com folga e dois grandes ficam no limite, sem medida publicada nessa classe de máquina.
    rodam = [f for f in fam if f["roda"] == "sim"]
    no_limite = [f for f in fam if f["roda"] == "no_limite"]
    instalada = maq["ram_instalada_gb"]
    glm = next(f for f in fam if f["nome"] == "GLM-5.2")
    nvme = v["cenarios_de_disco"][0]
    terceiros = v["medidas_de_terceiros"]
    do_glm = [x for x in terceiros if x["modelo"] == "GLM-5.2"]
    perto = next((x for x in do_glm if "12600K" in x["maquina"]), do_glm[0])
    perto_partes = [p.strip() for p in perto["maquina"].split(",")]
    seg_hoje = float(med["segundos"])
    tokens = float(med["tokens_saida"])

    # rótulo em três linhas curtas (lista de textos no Chart.js): numa linha só, e mesmo em duas, o começo do nome era
    # cortado à esquerda do eixo nas larguras menores
    barras = [{"rot": [meta["modelo_do_agente"], "neste notebook, hoje", "diagnóstico inteiro"], "minutos": round(seg_hoje / 60, 2), "hoje": True,
               "nota": f"diagnóstico inteiro: leitura do prompt e resposta ({fmt(seg_hoje)} s de mediana)"}]
    for x in terceiros:
        p = [s.strip() for s in x["maquina"].split(",")]
        rot = [x["modelo"], p[0].replace("Intel ", ""), p[1] + (" · opção com perda" if "perda" in x["nota"] else "")]
        barras.append({"rot": rot, "minutos": round(x["minutos_por_resposta"], 2), "hoje": False,
                       "nota": f'{fmt(x["tok_por_s"], 2)} token/s; {x["nota"]}'})
    dados_js = {"barras": barras, "tokens": tokens}

    def cabe(ok: bool, sim: str, nao: str) -> str:
        return chip("adotado" if ok else "descartado", sim if ok else nao)

    chip_da_ram = {"sim": chip("adotado", "cabe"), "no_minimo": chip("adiado", "no mínimo"), "nao": chip("descartado", "não cabe")}
    chip_do_veredito = {"sim": chip("adotado", "roda"), "no_limite": chip("adiado", "no limite"), "nao": chip("descartado", "não roda")}

    def linha_familia(x: dict) -> str:
        par = "não informado" if x["parametros_bi"] is None else _milhar(x["parametros_bi"])
        atv = "não informado" if x["ativos_bi"] is None else _milhar(x["ativos_bi"])
        return (f'<tr data-familia="{html.escape(x["nome"], quote=True)}" data-veredito="{x["roda"]}"><td><strong>{esc(x["nome"])}</strong></td><td class=num>{par}</td><td class=num>{atv}</td>'
                f'<td class=num>{fmt(float(x["disco_gb"]))} GB</td><td><code>{esc(x["ram_texto"])}</code></td>'
                f'<td>{cabe(x["disco_livre"], "cabe", "não cabe")}</td><td>{chip_da_ram[x["ram"]]}</td>'
                f'<td>{chip_do_veredito[x["roda"]]}</td></tr>')

    tab_fam = ('<div class="tabela"><table><thead><tr><th>Modelo</th><th>Parâmetros (bilhões)</th><th>Ativos por token (bilhões)</th><th>Disco pedido</th>'
               '<th>RAM pedida (texto do repositório)</th><th>Disco livre desta máquina</th><th>RAM pedida contra a instalada</th><th>Veredito</th></tr></thead><tbody>'
               + "".join(linha_familia(x) for x in fam) + "</tbody></table></div>")
    nem_vazio = [x["nome"] for x in fam if not x["disco_total"]]
    tab_disco = tabela(["Disco", "Leitura (GB/s)", "Medido ou premissa", "Segundos de disco por token frio", "Teto de tokens por segundo", "Minutos só de leitura para a resposta mediana"],
                       [[c["disco"], fmt(c["gb_por_s"], 2), "premissa" if c["premissa"] else "medido", fmt(c["segundos_por_token_frio"]), fmt(c["tokens_por_s_teto"], 3),
                         fmt(c["minutos_de_leitura_por_resposta"])] for c in v["cenarios_de_disco"]])
    tab_ter = tabela(["Máquina (medida publicada no repositório)", "Modelo", "Tokens por segundo", "Condição", "Minutos só de geração para a nossa resposta mediana",
                      "Vezes o tempo total de um diagnóstico de hoje", "Issue"],
                     [[x["maquina"], x["modelo"], fmt(x["tok_por_s"], 2), x["nota"], fmt(x["minutos_por_resposta"]), fmt(x["vezes_o_tempo_de_hoje"]), f'#{x["issue"]}']
                      for x in terceiros])
    min_glm = [x["minutos_por_resposta"] for x in do_glm]
    dm = v["disco_medido"]
    premissas = v["cenarios_de_disco"][1:]

    itens_kpi = [
        ("Famílias do colibri que rodam aqui", f"{len(rodam)} de {len(fam)}",
         ("com folga, só " + ", ".join(f["nome"] for f in rodam) if rodam else "nenhuma com folga")
         + (f'; no limite de RAM: {", ".join(f["nome"] for f in no_limite)}' if no_limite else "")),
        ("RAM instalada", f'{fmt(instalada)} GB', f'o sistema enxerga {fmt(maq["ram_gb"], 2)} GB; o GLM-5.2 pede {glm["ram_min_gb"]} GB no mínimo'),
        ("Disco livre", f'{fmt(maq["disco_livre_gb"])} GB', f'o GLM-5.2 pede {_milhar(glm["disco_gb"])} GB'),
        ("Velocidade de leitura do disco (NVMe)", f'{fmt(nvme["gb_por_s"], 2)} GB/s', f'medida sem usar o cache do sistema ({dm["blocos"]} leituras de {dm["bloco_bytes"] // 2**20} MB)'),
        ("Uma resposta nossa em máquina parecida", f'{fmt(perto["minutos_por_resposta"])} min', f'só gerar, a {fmt(perto["tok_por_s"], 2)} token/s ({perto_partes[0]}); hoje o diagnóstico inteiro leva {fmt(seg_hoje)} s'),
    ]

    bloco_sonda = ""
    am = _amostra_de_tokens(amostra)
    if am:
        ma, conf = amostra["metadados"], amostra["conferencias"]
        ch = amostra["chamadas"]
        itens_kpi.append(("Probabilidade por token no Ollama", "disponível", f'{conf["a"]["top_por_posicao_max"]} alternativas por posição; valor de {conf["temperatura"]["veredito"]} da temperatura'))

        def tok(t: dict) -> str:
            txt = t["token"].replace("\n", "\\n").replace(" ", "␣")
            return f'<span class="tok" style="--p:{round(t["p"] * 45)}%"><code>{esc(txt)}</code><small>{fmt(t["p"] * 100)}%</small></span>'

        linhas_alt = "".join(f'<tr data-alternativa="{i}"><td><code>{esc(a["token"].replace(" ", chr(0x2423)))}</code></td><td class=num>{fmt(a["p"] * 100, 2)}%</td></tr>'
                             for i, a in enumerate(am["alternativas"], 1))
        tab_conf = tabela(["O que foi conferido", "Resultado"], [
            ["Tokens da resposta com probabilidade", f'{conf["a"]["tokens_com_logprob"]} de {ch["a"]["resposta"].get("eval_count")} gerados'],
            ["Alternativas devolvidas por posição", str(conf["a"]["top_por_posicao_max"])],
            ["Vêm os bytes de cada token (acento partido entre dois tokens se remonta)", "sim" if conf["a"]["tem_bytes"] else "não"],
            ["Os tokens, juntos, são a resposta devolvida", "sim" if conf["a"]["texto_bate"] else "não"],
            ["A probabilidade é a de antes ou a de depois da temperatura", f'{conf["temperatura"]["veredito"]} (razão {fmt(conf["temperatura"]["razao"], 3)} entre a chamada a 0,1 e a chamada a 1,0; 1 seria igual)'],
            ["Tokens do prompt lidos do cache na segunda chamada", f'{ch["b"]["resposta"].get("prompt_eval_cached_count")} de {ch["b"]["resposta"].get("prompt_eval_count")} (campo prompt_eval_cached_count)'],
            ["A resposta sai igual com e sem o pedido de probabilidades", "sim" if conf["resposta_igual_sem_logprobs"] else "não: mesma causa e mesmos campos, frase de impacto com outras palavras (temperatura 0,1, sem semente)"],
        ])
        bloco_sonda = f'''<h2>O que a sonda do Ollama mostrou</h2>
<p>Amostra de ferramenta, com o <code>{esc(ma["modelo"])}</code> no caso <code>{esc(ma["caso"])}</code> e a versão {ma["biblioteca_epoca"]} da biblioteca que ele escreveu, no Ollama {esc(ma["versao_ollama"])}; não é resultado de corrida. O Ollama devolve, para cada token que o modelo escreve, a probabilidade que ele deu a esse token e às alternativas. Abaixo, a primeira linha da resposta, token a token; o símbolo <code>␣</code> marca um espaço.</p>
<div class="toks">{"".join(tok(t) for t in am["linha"])}</div>
<p>O modelo decide a causa no primeiro token depois de <code>CAUSA_RAIZ:</code>; daí em diante o resto da causa respondida sai quase certo. Nesse ponto, as opções que ele pesou foram estas:</p>
<div class="tabela estreita"><table><thead><tr><th>Token candidato</th><th>Probabilidade</th></tr></thead><tbody>{linhas_alt}</tbody></table></div>
<p>É esse número que a corrida 12 grava para os 72 casos: se a probabilidade da causa respondida for baixa justamente onde o modelo erra, ela serve de aviso para chamar um humano.</p>
{detalhes("O que a sonda conferiu", tab_conf)}'''

    leitura_itens = [
        f'<strong>O que barra os modelos grandes aqui é o espaço em disco e a RAM, não a velocidade do disco.</strong> O NVMe entrega {fmt(nvme["gb_por_s"], 2)} GB/s, o que daria cerca de {fmt(nvme["segundos_por_token_frio"])} s de leitura por token do GLM-5.2. Mas o modelo pede {_milhar(glm["disco_gb"])} GB de disco e a máquina tem {fmt(maq["disco_livre_gb"])} GB livres. Na RAM, os {fmt(instalada)} GB instalados são exatamente o mínimo que o repositório declara para ele, e cerca de {fmt(maq["ram_livre_no_inicio_de_corrida_gb"])} GB ficam livres no início de uma corrida.',
        f'<strong>Mesmo onde ele roda, o tempo não serve ao agente.</strong> Nas máquinas parecidas com a nossa em que o repositório publica medida, uma resposta de {fmt(tokens, 0)} tokens levaria de {fmt(min(min_glm))} a {fmt(max(min_glm))} minutos só para ser gerada. Hoje o diagnóstico inteiro leva {fmt(seg_hoje)} s.',
        ("<strong>O único modelo que roda com folga não é candidato a motor do agente.</strong> " + ", ".join(f'{f["nome"]} ({_milhar(f["parametros_bi"])} bilhões de parâmetros no total, {_milhar(f["ativos_bi"])} em uso a cada token)' for f in rodam)
         + " cabe na máquina, mas trocar de modelo exige medir de novo (decisão 69). Ele entra na corrida 13 só como material do atlas."),
        "<strong>Disco comum e HD.</strong> O repositório não publica medida em HD. Pela leitura por token que ele declara, só o disco custaria "
        + " e ".join(f'{fmt(c["segundos_por_token_frio"])} s por token em {c["disco"].split(" (")[0]}' for c in premissas) + " (velocidades postas como premissa, não medidas).",
        "<strong>O que se aproveita sem trocar de motor</strong> é a ideia da escolha fechada por probabilidade: em vez de só ler a causa que o modelo escreveu, ler também a probabilidade que ele deu a ela. O nosso diagnóstico é uma escolha entre 23 causas, e o Ollama instalado já devolve esse número."
    ]
    if no_limite:
        # a medida publicada com menos memória: a do GLM-5.2 na máquina de menor RAM, sem a opção com perda
        com_ram = [(int(re.search(r"(\d+) GB", x["maquina"]).group(1)), x) for x in do_glm if re.search(r"(\d+) GB", x["maquina"]) and "perda" not in x["nota"]]
        menor_ram, menor = min(com_ram, key=lambda par: par[0]) if com_ram else (None, None)
        leitura_itens.insert(1, f'<strong>{"Dois modelos grandes ficam" if len(no_limite) == 2 else "Há modelo grande que fica"} no limite.</strong> '
                                + " e ".join(f'{f["nome"]} ({_milhar(f["parametros_bi"])} bilhões de parâmetros, {_milhar(f["disco_gb"])} GB em disco)' for f in no_limite)
                                + f' cabem no disco livre e pedem exatamente a RAM instalada. O repositório não publica medida de nenhum deles numa máquina de {fmt(instalada, 0)} GB'
                                + (f'; a medida com menos memória que ele publica é a do GLM-5.2 numa máquina de {menor_ram} GB, a {fmt(menor["tok_por_s"], 2)} token/s.' if menor else '.')
                                + ' Rodar um deles seria uma medição nova, fora do que a corrida 13 prevê.')
    if nem_vazio:
        leitura_itens.insert(1, f'<strong>Nem com o disco vazio</strong> caberia {", ".join(nem_vazio)}: o disco tem {fmt(maq["disco_total_gb"])} GB no total.')
    conferido = (f'conferidas pela rodada 5 da pesquisa (ressalva: {esc(meta["ressalva_da_conferencia"])})' if meta["conferido_pela_rodada_5"]
                 else "ainda não conferidas pela rodada 5 da pesquisa")
    bloco_literatura, cartoes_literatura, fonte_literatura = _literatura_do_colibri(levantamento)
    itens_kpi += cartoes_literatura
    html_ = f'''<section id="colibri" hidden>
<h1>{titulo}</h1>
<p class="lead">Só no limite, e não para o agente. O colibri roda modelos de centenas de bilhões de parâmetros deixando na RAM a parte que todo token usa e lendo do NVMe, a cada token, só os especialistas que o modelo aciona. Das {len(fam)} famílias que ele suporta, {len(rodam)} roda com folga nesta máquina ({", ".join(f["nome"] for f in rodam) or "nenhuma"}){f" e {len(no_limite)} cabem no disco livre e ficam exatamente no mínimo de RAM que o repositório declara ({', '.join(f['nome'] for f in no_limite)}), sem nenhuma medida publicada numa máquina dessa classe" if no_limite else ""}; as outras esbarram no espaço em disco ou na RAM. Nas máquinas maiores em que ele foi medido, uma resposta do tamanho das nossas levaria de {fmt(min(min_glm))} a {fmt(max(min_glm))} minutos só para ser gerada.</p>
{kpis(itens_kpi)}
<h2>O que cada modelo pede e o que esta máquina tem</h2>
<p>Requisitos da tabela do README do repositório (acesso em {esc(meta["acesso"])}), comparados com a máquina medida por <code>ferramentas/medir_disco.py</code>. Roda com folga o modelo que cabe no disco livre e pede menos RAM do que a instalada; fica no limite o que cabe no disco livre e pede exatamente a RAM instalada, que é o mínimo declarado pelo repositório.</p>
{tab_fam}
<h2>Quanto tempo levaria um diagnóstico</h2>
<p>A primeira barra é o tempo de hoje, do diagnóstico inteiro. As outras são as velocidades que o repositório publica para cada máquina, aplicadas à nossa resposta mediana de {fmt(tokens, 0)} tokens: contam só a geração, porque a leitura do prompt em máquina pequena não é medida lá. O tempo real seria maior.</p>
<div class="chart alto"><canvas id="g-co-min"></canvas></div>
{detalhes("Medidas publicadas no repositório, aplicadas à nossa resposta", tab_ter)}
{detalhes("Quanto o disco sozinho custaria por token, por tipo de disco", tab_disco)}
{bloco_sonda}
<h2>Leitura</h2>
{leitura(leitura_itens)}
{bloco_literatura}
<h2>As medições desta frente</h2>
{cartoes_corridas(road, numeros=["11", "12", "13"], sufixo="-co")}
{fontes(["<code>resultados_alvo/pre_fase4/viabilidade_modelos_grandes.json</code> (<code>viabilidade_modelos_grandes.py</code>, com <code>--check</code>)", "<code>resultados_alvo/pre_fase4/disco.json</code> (<code>ferramentas/medir_disco.py</code>)", "amostra de <code>sondar_logprobs.py</code> em <code>resultados_alvo/pre_fase4/</code>", f'constantes do repositório <a href="{esc(meta["repositorio"])}">JustVugg/colibri</a>, {conferido}'] + ([fonte_literatura] if fonte_literatura else []) + ["decisão 70; roadmap §3.1"])}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ 11. Pré-Fase 4: raciocínio aberto

# ! Alteração de IA - Revisar: aba nova (01/10/2026) da Pré-Fase 4 com o que a trilha bruta e o relatório de raciocínio
# mostram das corridas já gravadas: quantos diagnósticos foram remontados, em quantos o modelo não escreveu raciocínio,
# o que o código consegue conferir sem o gabarito e um relatório de caso inteiro, como exemplo.
# ! Motivo: o Eric pediu (01/10/2026) o "pensamento" da IA aberto, com arquivo bruto e relatório para humanos; a regra
# do painel é uma aba por análise. Os números vêm de resultados_alvo/pre_fase4/indicadores_raciocinio.json (gerado por
# gerar_relatorio_raciocinio.py --vitrine, com --check) e o exemplo é um dos relatórios versionados. O conversor de
# Markdown do painel não trata cerca de código nem <details>, que o relatório usa; por isso a seção tem o próprio
# conversor, que rebaixa os títulos para caberem dentro da aba e mantém os blocos como texto literal.

def _relatorio_para_html(md: str) -> str:
    linhas = pt.sem_comentarios(md).split("\n")
    out: list[str] = []
    par: list[str] = []
    i = 0

    def fecha() -> None:
        if par:
            out.append(f"<p>{pt.inline(' '.join(par))}</p>")
            par.clear()

    while i < len(linhas):
        l = linhas[i]
        if l.startswith("```"):
            fecha()
            cerca = l[:len(l) - len(l.lstrip("`"))]
            i += 1
            bloco = []
            while i < len(linhas) and not linhas[i].startswith(cerca):
                bloco.append(linhas[i])
                i += 1
            i += 1
            out.append('<pre class="bruto"><code>' + html.escape("\n".join(bloco), quote=False) + "</code></pre>")
            continue
        m = re.match(r"^<details><summary>(.*?)</summary>\s*$", l)
        if m:
            fecha()
            out.append(f"<details><summary>{esc(m.group(1))}</summary>")
            i += 1
            continue
        if l.strip() == "</details>":
            fecha()
            out.append("</details>")
            i += 1
            continue
        if not l.strip():
            fecha()
            i += 1
            continue
        if l.startswith("|"):
            fecha()
            tab = []
            while i < len(linhas) and linhas[i].startswith("|"):
                tab.append(linhas[i])
                i += 1
            out.append(pt.tabela_html(tab))
            continue
        # ! Alteração de IA - Revisar: (05/11/2026) linha começada por "- " vira item de lista, com o mesmo montador dos documentos do painel.
        # ! Motivo: as linhas da lista do Rastro no relatório v2 caíam no parágrafo e saíam coladas umas nas outras na página da sessão de revisão.
        if re.match(r"^\s*- ", l):
            fecha()
            bloco, i = pt._lista(linhas, i)
            out.append(bloco)
            continue
        m = re.match(r"^(#{1,4}) (.+)$", l)
        if m:
            fecha()
            nivel = min(len(m.group(1)) + 2, 6)      # o título do relatório vira h3; as seções, h4; as subseções, h5
            out.append(f"<h{nivel}>{pt.inline(m.group(2))}</h{nivel}>")
            i += 1
            continue
        par.append(l.strip())
        i += 1
    fecha()
    return "\n".join(out)


# Nome das três conferências que usam o gabarito, para o bloco de avaliação do explorador de casos.
ROTULO_AVALIACAO = {"causa_correta": "A causa respondida é a do caso", "campo_correto": "O campo apontado é o do caso",
                    "verbete_de_ouro_no_contexto": "O verbete que trata da causa certa estava no contexto"}
# O caso que o explorador abre escolhido: o mesmo do relatório de exemplo (a conferência em código acusa a resposta errada).
CASO_PADRAO_DO_EXPLORADOR = ("fase3b_cruzada_qwen__qwen2.5-coder_3b__L1", "sin-4")


# ! Alteração de IA - Revisar: (23/10/2026) bloco "O que a literatura sustenta para a arquitetura da trilha" da aba "Raciocínio
# aberto", lido do levantamento §6.14 (parte B, onda 1): o mapa de decisões de arquitetura com filtro por veredito, os
# riscos, a leitura e as cinco sínteses por extenso (fidelidade do raciocínio, trilha e observabilidade, relatório para
# humanos, atribuição ao contexto, uso das trilhas). Os mapas do §6.14 vêm um por Workflow, separados pelo nome em
# negrito ("Parte A: ...", "Parte B, onda 1: ...", "Parte B, onda 2: ..."); _blocos_dos_mapas os separa.
# ! Motivo: o Eric decide pelo painel, e a especificação da linha de raciocínio aberta (próximo passo) sai deste mapa;
# sem o bloco a análise ficaria só no levantamento. Nada é digitado aqui: tudo vem do arquivo gerado por
# integrar_pesquisa_pre_fase4.py, e a onda 2 (confiança, Brainiac, grafos, visualização) terá a sua própria aba.
TOPICOS_RACIOCINIO = ("r5-fidelidade-do-raciocinio", "r5-trilha-e-observabilidade", "r5-relatorio-para-humanos", "r5-atribuicao-ao-contexto", "r5-uso-das-trilhas")
TOPICOS_VISUALIZACAO = ("r5-confianca-por-probabilidade", "r5-brainiac-segundo-cerebro", "r5-codebase-memory-visual", "r5-visualizacao-da-rede-neural")


def _blocos_dos_mapas(trecho: str) -> dict[str, str]:
    """Os mapas do §6.14, um por Workflow, pelo nome em negrito que abre cada um; o valor é o texto até o mapa seguinte."""
    blocos = {}
    for m in re.finditer(r"^\*\*(Parte [^*\n]+)\*\*\n", trecho, re.M):
        inicio = m.end()
        prox = re.search(r"^\*\*Parte ", trecho[inicio:], re.M)
        blocos[m.group(1)] = trecho[inicio:inicio + prox.start()] if prox else trecho[inicio:]
    return blocos


def _mapa_de_um_bloco(bloco: str, id_tabela: str, rotulo: str) -> tuple[str, Counter, int, str, str]:
    """De um bloco de mapa (tabela, riscos, leitura): a tabela com filtro, a contagem por veredito, o número de linhas,
    a tabela de riscos e a leitura em HTML."""
    mapa, cont, n = _mapa_de_vereditos(bloco, id_tabela, rotulo)
    _, riscos, _ = pt.primeira_tabela(bloco[bloco.index("**Riscos**"):])
    tab_riscos = ('<div class="tabela"><table><thead><tr><th>Risco</th><th>Mitigação</th><th>Fonte</th></tr></thead><tbody>'
                  + "".join(f'<tr data-risco="{i}"><td>{pt.inline(r[0])}</td><td>{pt.inline(r[1])}</td><td class="nota">{pt.inline(r[2])}</td></tr>' for i, r in enumerate(riscos, 1))
                  + "</tbody></table></div>")
    leitura_md = bloco[bloco.index("**Leitura**") + len("**Leitura**"):].strip()
    return mapa, cont, n, tab_riscos, pt.md_doc_para_html(leitura_md)


def _sinteses_por_extenso(secoes: list[dict]) -> str:
    return "".join(
        f'<details data-sintese="{esc(s["chave"])}"><summary>§{s["secao"]} {esc(s["titulo"])} ({s["aprovadas"]} afirmações aprovadas)</summary>'
        f'<div class="relatorio">{pt.md_doc_para_html(s["texto"])}<h4>O que isso implica para o agente e para a Fase 4</h4>{leitura([pt.inline(x) for x in s["implicacoes"]])}'
        f'<h4>O que a literatura não responde</h4>{leitura([pt.inline(x) for x in s["lacunas"]])}</div></details>' for s in secoes)


def _literatura_do_raciocinio(lev: str | None) -> tuple[str, list[tuple[str, str, str]], str | None]:
    """Devolve o HTML do bloco, os cartões de número-chave que ele acrescenta e a linha de fonte."""
    lit = _pre_fase4_no_levantamento(lev)
    blocos = _blocos_dos_mapas(lit["mapas"]) if lit else {}
    nome = next((k for k in blocos if k.startswith("Parte B, onda 1")), None)
    if not lit or not nome or "ainda não rodou" in blocos[nome]:
        return ('<h2>O que a literatura sustenta para a arquitetura da trilha</h2>\n<p class="nota">A parte B da rodada 5 da pesquisa (raciocínio aberto) ainda não foi '
                'integrada ao levantamento, como §6.14.</p>'), [], None
    mapa, cont, n, tab_riscos, leitura_do_mapa = _mapa_de_um_bloco(blocos[nome], "tab-mapa-ra", "Filtro do mapa de arquitetura")
    secoes = [s for s in lit["secoes"] if s["chave"] in TOPICOS_RACIOCINIO]
    aprovadas, rejeitadas = sum(s["aprovadas"] for s in secoes), sum(s["rejeitadas"] for s in secoes)
    bloco_html = f'''<h2>O que a literatura sustenta para a arquitetura da trilha</h2>
<p>A parte B da rodada 5 da pesquisa (onda 1, 23/10/2026) leu a literatura sobre fidelidade do raciocínio escrito, formatos de trilha e exigências de registro, relatório para quem desenvolve, atribuição ao contexto e uso das trilhas para melhorar o sistema: {len(secoes)} tópicos, {aprovadas} afirmações aprovadas por verificadores céticos e {rejeitadas} {"rejeitada" if rejeitadas == 1 else "rejeitadas"}. O mapa dá o veredito de cada opção de arquitetura para esta máquina: <em>adotado</em> entra na arquitetura da linha de raciocínio aberta da Fase 4; <em>adiado</em> só com outra máquina, outro motor ou depois da Fase 4; <em>descartado</em> não serve, com o motivo.</p>
{mapa}
{detalhes("Riscos que a literatura aponta e a mitigação de cada um", tab_riscos)}
{detalhes("Leitura do mapa, por extenso", leitura_do_mapa)}
<h3>As sínteses, por extenso</h3>
<p>Cada síntese foi escrita só com as afirmações que sobreviveram à verificação. As referências completas e as afirmações rejeitadas, com o motivo, estão no levantamento (§{lit["secao_rejeitadas"]}) e em <code>referencias.md</code>.</p>
{_sinteses_por_extenso(secoes)}'''
    cartoes = [("Opções de arquitetura da trilha avaliadas pela literatura", f'{cont["adotado"]} adotadas', f'{cont["adiado"]} adiadas · {cont["descartado"]} descartadas, de {n} no mapa da onda 1 da parte B')]
    fonte = (f'<code>2-pesquisa-e-literatura/{LEVANTAMENTO_PRE_FASE4}</code> (§{secoes[0]["secao"]} a §{secoes[-1]["secao"]} e o mapa "Parte B, onda 1" em §{lit["secao_mapas"]})'
             if secoes else None)
    return bloco_html, cartoes, fonte


# ! Alteração de IA - Revisar: (23/10/2026) aba nova "Cérebro e memória" (id cerebro), lida só do levantamento §6.14 (parte B,
# onda 2): o mapa de viabilidade com filtro por veredito, um gráfico de vereditos por tema, os riscos, a leitura, as
# quatro sínteses por extenso (confiança por probabilidade, Brainiac, grafos do código e do conhecimento, visualização
# da rede neural) e uma leitura curta montada das linhas do próprio mapa.
# ! Motivo: o Eric perguntou em 23/10/2026 se dá para mostrar a rede neural como o "cérebro" do agente no painel, ao
# vivo, se o Brainiac serve e se o grafo do código seria um toque a mais; ele decide pelo painel, e a regra do projeto
# é uma aba por análise. Nada é digitado aqui: tudo vem do arquivo gerado por integrar_pesquisa_pre_fase4.py.
TEMAS_DA_LEITURA_CE = ("Cérebro ao vivo", "Rede neural como figura estática", "Atenção e ativações ao vivo", "Brainiac", "Grafo do conhecimento no painel",
                       "Grafo do código no painel", "Confiança pela probabilidade do rótulo", "Decodificação restrita")


def secao_cerebro(levantamento: str | None) -> tuple[dict, str]:
    titulo = "Dá para mostrar o cérebro do agente no painel, e o Brainiac ou um grafo do código servem?"
    lit = _pre_fase4_no_levantamento(levantamento)
    blocos = _blocos_dos_mapas(lit["mapas"]) if lit else {}
    nome = next((k for k in blocos if k.startswith("Parte B, onda 2")), None)
    if not lit or not nome or "ainda não rodou" in blocos[nome]:
        return {"temas": []}, (f'<section id="cerebro" hidden>\n<h1>{titulo}</h1>\n<p class="lead">A onda 2 da parte B da rodada 5 da pesquisa (confiança por '
                               'probabilidade, Brainiac, grafos, visualização da rede neural) ainda não foi integrada ao levantamento, como §6.14.</p>\n</section>')
    bloco = blocos[nome]
    mapa, cont, n, tab_riscos, leitura_do_mapa = _mapa_de_um_bloco(bloco, "tab-mapa-ce", "Filtro do mapa de viabilidade do painel")
    cab, linhas, _ = pt.primeira_tabela(bloco)
    col = {c: i for i, c in enumerate(cab)}
    temas: list[dict] = []
    por_tema: dict[str, list] = {}
    for r in linhas:
        tema = re.sub(r"[*`_]", "", r[col["Tema"]]).strip()
        v = _veredito(r[col["Veredito"]])
        t = next((x for x in temas if x["tema"] == tema), None)
        if not t:
            t = {"tema": tema, "adotado": 0, "adiado": 0, "descartado": 0, "outro": 0}
            temas.append(t)
        t[v] += 1
        por_tema.setdefault(tema, []).append((v, r[col["Opção"]], r[col["Motivo"]]))
    secoes = [s for s in lit["secoes"] if s["chave"] in TOPICOS_VISUALIZACAO]
    aprovadas, rejeitadas = sum(s["aprovadas"] for s in secoes), sum(s["rejeitadas"] for s in secoes)
    com_adotado = sum(1 for t in temas if t["adotado"])
    itens_kpi = [("Opções avaliadas pela literatura", f'{cont["adotado"]} servem agora', f'{cont["adiado"]} só com outra máquina ou depois · {cont["descartado"]} não servem, de {n} no mapa da onda 2'),
                 ("Tópicos da onda 2", f"{len(secoes)}", f'{aprovadas} afirmações aprovadas por verificadores céticos · {rejeitadas} {"rejeitada" if rejeitadas == 1 else "rejeitadas"}'),
                 ("Temas do mapa", f"{len(temas)}", f"{com_adotado} com ao menos uma opção que serve agora")]
    lead = (f'Em parte. Dos {n} caminhos avaliados pela onda 2 da parte B da rodada 5 da pesquisa (23/10/2026), {cont["adotado"]} servem agora nesta máquina, sem trocar o '
            f'modelo nem o motor decididos; {cont["adiado"]} só serviriam com outra máquina, outro motor ou depois da Fase 4; {cont["descartado"]} não servem. O veredito de cada '
            'um, com o motivo e a fonte, está no mapa abaixo; o que vale para a trilha de raciocínio entrou na especificação da trilha (Memorial, seção 5).')
    pontos = []
    for tema in TEMAS_DA_LEITURA_CE:
        for v, opcao, motivo in por_tema.get(tema, []):
            pontos.append(f"<strong>{pt.inline(opcao)}:</strong> {chip(v, v)} {pt.inline(motivo)}")
            break
    html_ = f'''<section id="cerebro" hidden>
<h1>{titulo}</h1>
<p class="lead">{lead}</p>
{kpis(itens_kpi)}
<h2>Vereditos por tema</h2>
<p>Cada barra é um tema do mapa de viabilidade; as cores dizem quantas opções daquele tema servem agora nesta máquina, quantas só serviriam com outra máquina, outro motor ou depois da Fase 4, e quantas não servem.</p>
<div class="chart" style="height:{max(260, 28 * len(temas) + 80)}px"><canvas id="g-ce-temas"></canvas></div>
<h2>O mapa de viabilidade, opção por opção</h2>
<p><em>Adotado</em> serve agora, nesta máquina, sem trocar o modelo nem o motor decididos; <em>adiado</em> só serviria com outra máquina (o mapa diz quanta RAM, GPU ou disco), outro motor, ou depois da Fase 4; <em>descartado</em> não serve, com o motivo.</p>
{mapa}
{detalhes("Riscos que a literatura aponta e a mitigação de cada um", tab_riscos)}
{detalhes("Leitura do mapa, por extenso", leitura_do_mapa)}
<h2>As sínteses, por extenso</h2>
<p>Cada síntese foi escrita só com as afirmações que sobreviveram à verificação. As referências completas e as afirmações rejeitadas, com o motivo, estão no levantamento (§{lit["secao_rejeitadas"]}) e em <code>referencias.md</code>.</p>
{_sinteses_por_extenso(secoes)}
<h2>Leitura</h2>
{leitura(pontos)}
{fontes([f'<code>2-pesquisa-e-literatura/{LEVANTAMENTO_PRE_FASE4}</code> (§{secoes[0]["secao"]} a §{secoes[-1]["secao"]} e o mapa "Parte B, onda 2" em §{lit["secao_mapas"]})' if secoes else f'<code>2-pesquisa-e-literatura/{LEVANTAMENTO_PRE_FASE4}</code>', "<code>5-metodo-e-ferramental/especificacao-trilha-e-relatorio.md</code> (seção 14)", "decisões 61, 70 e 75; roadmap §3.1"])}
</section>'''
    return {"temas": temas}, html_


def secao_raciocinio(ind: dict | None, exemplo: str | None, trilhas: dict | None = None, confianca: dict | None = None, levantamento: str | None = None) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões, título e parágrafos à vista reescritos sem AUROC solto, b/c, p, "rótulo" nem "L1" sem explicação.
    # ! Motivo: o texto à vista trazia siglas que o Eric pediu para tirar; a probabilidade do "rótulo" passa a ser a da causa respondida, e os números seguem nas tabelas recolhidas.
    titulo = "Dá para ver por que o modelo respondeu o que respondeu?"
    if not ind:
        return {"trilhas": [], "explorador": {"trilhas": []}}, (f'<section id="raciocinio" hidden>\n<h1>{titulo}</h1>\n<p class="lead">As trilhas ainda não foram geradas nesta máquina: falta '
                                 '<code>resultados_alvo/pre_fase4/indicadores_raciocinio.json</code> (<code>python gerar_relatorio_raciocinio.py --vitrine</code>).</p>\n</section>')
    cs = ind["corridas"]

    corrida_curta = {"fase3": "Fase 3, 90 casos", "fase3b_ineditos": "36 casos inéditos", "fase3b_cruzada_qwen": "troca cruzada, 36 casos"}

    def nome(c: dict) -> str:
        dono = c.get("dono_da_biblioteca") or c["modelo"]
        de_quem = "" if dono == c["modelo"] else f' do {NOME_CURTO.get(dono, dono)}'
        return f'{NOME_CURTO.get(c["modelo"], c["modelo"])} · {corrida_curta.get(c["corrida"], c["corrida"])} · biblioteca L{c["biblioteca_epoca"]}{de_quem}'

    def soma(regra: str, chave: str) -> int:
        return sum(x.get(chave, 0) for c in cs for x in c["conferencias"] if x["regra"] == regra)

    total = sum(c["diagnosticos"] for c in cs)
    sem = sum(c["sem_raciocinio_antes_das_linhas"] for c in cs)
    inteiro = sum(c["prova_do_prompt"].get("prompt_inteiro", 0) for c in cs)
    so_doc = sum(c["prova_do_prompt"].get("contexto", 0) for c in cs)
    nao_comp = sum(c["prova_do_prompt"].get("nao_comprovado", 0) for c in cs)
    fora_ctx = soma("fonte_estava_no_contexto", "nao_confere")
    citadas = soma("fonte_estava_no_contexto", "confere") + fora_ctx
    fora_conj = soma("rotulo_no_conjunto", "nao_confere")
    inexistentes = soma("fonte_existe_na_biblioteca", "nao_confere")
    sem_apoio = sum(c["acerto_por_sustentacao"]["nao_sustentado"]["n"] for c in cs)
    com_grupo = [c for c in cs if c["acerto_por_sustentacao"]["nao_sustentado"]["n"] and c["acerto_por_sustentacao"]["sustentado"]["n"]]
    texto_sinal = ""
    if com_grupo:
        pior = min(com_grupo, key=lambda c: c["acerto_por_sustentacao"]["nao_sustentado"]["acerto_pct"])
        ps, pn = pior["acerto_por_sustentacao"]["sustentado"], pior["acerto_por_sustentacao"]["nao_sustentado"]
        texto_sinal = (f' Na trilha em que a documentação mais atrapalhou ({esc(nome(pior))}), o acerto foi de {fmt(ps["acerto_pct"])}% quando sim ({ps["acertos"]} de {ps["n"]}) '
                       f'e de {fmt(pn["acerto_pct"])}% quando não ({pn["acertos"]} de {pn["n"]}).')
    if fora_ctx == 0 and inexistentes == 0:
        leitura_fontes = (f"<strong>Nestas trilhas o modelo não inventou fonte:</strong> os {citadas} verbetes citados existiam e estavam no contexto entregue. "
                          f"Respostas com causa fora das 23 permitidas: {fora_conj} em {total}.")
    else:
        leitura_fontes = (f"<strong>Fontes citadas:</strong> {fora_ctx} de {citadas} estavam fora do contexto entregue e {inexistentes} não existiam na biblioteca. "
                          f"Respostas com causa fora das 23 permitidas: {fora_conj} em {total}.")
    # o arquivo de cada trilha é <corrida>__<modelo com _ no lugar de :>__L<versão>; o nome legível é o da tabela
    nomes_das_trilhas = {f'{c["corrida"]}__{c["modelo"].replace(":", "_").replace("/", "_")}__L{c["biblioteca_epoca"]}': nome(c) for c in cs}
    explorador = pe.dados_do_explorador(trilhas, nomes_das_trilhas, {**ROTULO_CONFERENCIA, **ROTULO_AVALIACAO}, CLASSES, CASO_PADRAO_DO_EXPLORADOR)
    # ! Alteração de IA - Revisar: (06/10/2026) a sonda de confiança (corrida 12) entra na aba: AUROC de cada sinal por
    # biblioteca, o que a revisão dos 10%, 20% e 30% de menor probabilidade pega, e o acerto da cópia curada contra a L1 e a L0.
    # ! Motivo: a aba prometia a análise "quando a corrida 12 terminar"; ela rodou em 06/10 (fichas 18 e 19). Tudo vem de
    # resultados_alvo/pre_fase4/confianca.json.
    conf = confianca or {}
    resumos = conf.get("resumos") or []
    tot = resumos[0] if resumos else None
    por_bib = [r for r in resumos[1:]] if resumos else []
    SINAIS = [("p_conjunta", "probabilidade conjunta do rótulo"), ("p_primeiro", "primeiro token"), ("um_menos_massa", "1 menos a massa de outra causa"),
              ("sustentado", "causa tratada por verbete do contexto"), ("coerente", "causa na classe que a rota aponta")]
    dados_conf = {"sinais": [n for _, n in SINAIS],
                  "bibliotecas": [{"rot": r["nome"].split(", ")[-1], "auroc": [(r["sinais"].get(s) or {}).get("auroc") for s, _ in SINAIS]} for r in por_bib]}
    bloco_conf, itens_conf = "", []
    if tot:
        ac = conf.get("acerto", [])
        pares = {(x["comparacao"], x["conjunto"]): x for x in conf.get("pares", [])}
        rev = {x["fracao"]: x for x in tot["revisao"]}
        a72 = {x["rotulo"]: x for x in ac if x["conjunto"] == "todos"}
        cur = a72.get("L1 curada")
        l1 = a72.get("L1")
        p_cur = pares.get(("L1 curada contra L1", "todos"))
        confiantes = sum(1 for l in conf.get("casos", []) if not l["acerto"] and (l["p_conjunta"] or 0) > 0.85)
        itens_conf = [
            ("O quanto a probabilidade da causa separa erros de acertos (AUROC)", fmt(tot["sinais"]["p_conjunta"]["auroc"], 3),
             f'em {tot["casos"]} diagnósticos; verbete do contexto {fmt(tot["sinais"]["sustentado"]["auroc"], 3)}, classe da rota {fmt((tot["sinais"].get("coerente") or {}).get("auroc"), 3)}'),
            ("Revisar os 10% menos prováveis", f'{rev[0.1]["erros_pegos"]} de {tot["erros"]} erros', f'{rev[0.1]["revisados"]} casos revisados, {rev[0.1]["acertos_revisados"]} deles acertos; com 30%: {rev[0.3]["erros_pegos"]} de {tot["erros"]}'),
            ("Erros confiantes", f"{confiantes} de {tot['erros']}", f'probabilidade acima de 0,85; mediana {fmt(tot["p_conjunta_mediana"]["certos"], 3)} nos certos e {fmt(tot["p_conjunta_mediana"]["errados"], 3)} nos errados'),
        ]
        if cur and l1 and p_cur:
            itens_conf.append(("Cópia curada contra a 1ª versão inteira (72 casos)", f'{fmt(cur["acerto_pct"])}% × {fmt(l1["acerto_pct"])}%',
                               f'só a cópia acertou {p_cur["b"]}, só a inteira {p_cur["c"]}; {fmt(cur["segundos_mediana"])} × {fmt(l1["segundos_mediana"])} s por diagnóstico'))
        tab_res = tabela(["Recorte", "Casos", "Erros"] + [n for _, n in SINAIS] + ["Mediana nos certos", "Mediana nos errados", "Erros com a causa certa em 2º"],
                         [[r["nome"], r["casos"], r["erros"]] + [("n/d" if not r["sinais"].get(s) or r["sinais"][s].get("auroc") is None else f'{fmt(r["sinais"][s]["auroc"], 3)} [{fmt(r["sinais"][s]["ic95"][0], 2)} a {fmt(r["sinais"][s]["ic95"][1], 2)}]') for s, _ in SINAIS]
                          + [fmt(r["p_conjunta_mediana"]["certos"], 3), fmt(r["p_conjunta_mediana"]["errados"], 3), f'{r["erros_com_o_gabarito_na_segunda"]} de {r["erros"]}'] for r in resumos])
        tab_rev = tabela(["Recorte", "Parcela revisada", "Casos revisados", "Erros pegos", "Acertos revisados à toa", "Risco no que sobra"],
                         [[r["nome"], f'{fmt(100 * x["fracao"], 0)}%', x["revisados"], f'{x["erros_pegos"]} de {x["erros"]}', x["acertos_revisados"], "n/d" if x["risco_no_que_sobra"] is None else f'{fmt(100 * x["risco_no_que_sobra"])}%']
                          for r in resumos for x in r["revisao"]])
        tab_ac = ('<div class="tabela"><table><thead><tr><th>Biblioteca</th><th>Conjunto</th><th>Casos</th><th>Acertos</th><th>Acerto</th><th>s por diagnóstico (mediana)</th><th>Tokens do prompt (mediana)</th></tr></thead><tbody>'
                  + "".join(f'<tr data-conf-acerto="{html.escape(x["rotulo"] + "/" + x["conjunto"], quote=True)}"><td>{esc(x["rotulo"])}</td><td>{esc(x["conjunto"])}</td><td class=num>{x["n"]}</td><td class=num>{x["acertos"]}</td>'
                            f'<td class=num>{fmt(x["acerto_pct"])}%</td><td class=num>{fmt(x["segundos_mediana"])}</td><td class=num>{fmt(x["tokens_entrada_mediana"], 0)}</td></tr>' for x in ac) + "</tbody></table></div>")
        tab_par = tabela(["Comparação", "Conjunto", "Casos", "Acerto da primeira", "Acerto da segunda", "b", "c", "Diferença", "p (McNemar exato)", "Casos que mudaram"],
                         [[x["comparacao"], x["conjunto"], x["n"], f'{fmt(x["acerto_pct"])}%', f'{fmt(x["acerto_base_pct"])}%', x["b"], x["c"], pp(x["delta_pp"]), fmt(x["p_mcnemar"], 4), ", ".join(x["ganhos"] + x["perdas"]) or "nenhum"]
                          for x in conf.get("pares", []) + conf.get("contra_corridas_anteriores", [])])
        bloco_conf = f"""<h2>A probabilidade da causa respondida separa acerto de erro? (corrida 12, 06/10/2026)</h2>
<p>O Ollama devolve a probabilidade de cada token que o modelo escreve. A corrida 12 gravou essa probabilidade para a causa respondida nos 72 casos que nenhuma biblioteca viu, com o qwen2.5:7b lendo a biblioteca original (L0), a primeira versão escrita pelo modelo inteira (L1) e a cópia curada dela que a Fase 4 vai usar: {tot["casos"]} diagnósticos, {tot["erros"]} erros. A medida principal, fixada antes da corrida, é a probabilidade conjunta dos tokens da causa. O quanto cada sinal separa erros de acertos (AUROC) vai de 0,5, que é sortear, a 1,0, que separa tudo.</p>
{kpis(itens_conf)}
<div class="chart"><canvas id="g-ra-conf"></canvas></div>
{tab_res}
{leitura([f"<strong>Separa, e melhor que os dois sinais grátis, mas metade dos erros sai confiante.</strong> O sinal separa erros de acertos em {fmt(tot['sinais']['p_conjunta']['auroc'], 3)}, contra {fmt(tot['sinais']['sustentado']['auroc'], 3)} e {fmt((tot['sinais'].get('coerente') or {}).get('auroc'), 3)} dos outros dois. Além disso, {confiantes} dos {tot['erros']} erros têm probabilidade acima de 0,85, e em {tot['erros_com_o_gabarito_na_segunda']} deles a causa certa era a segunda opção.",
          f"<strong>Serve de triagem, não de barreira.</strong> Mandar para revisão os 10% de menor probabilidade ({rev[0.1]['revisados']} casos) pega {rev[0.1]['erros_pegos']} dos {tot['erros']} erros; 30% ({rev[0.3]['revisados']} casos) pega {rev[0.3]['erros_pegos']}, revisando {rev[0.3]['acertos_revisados']} acertos à toa. Para a Fase 4, vale como ordem de prioridade de revisão e como aviso na trilha."]
         + ([f"<strong>A cópia curada rende como a primeira versão inteira e custa menos.</strong> {fmt(cur['acerto_pct'])}% contra {fmt(l1['acerto_pct'])}% nos 72 casos na mesma corrida ({p_cur['b']} casos só da cópia, {p_cur['c']} só da inteira), dentro da variação entre corridas iguais; {fmt(cur['segundos_mediana'])} s contra {fmt(l1['segundos_mediana'])} s por diagnóstico, com menos texto no contexto. Segue como ponto de partida da Fase 4 (decisão 71)."] if cur and l1 and p_cur else []))}
{detalhes("Revisão humana por parcela de menor probabilidade", tab_rev)}
{detalhes("Acerto de cada biblioteca na corrida 12 (36 oficiais, 36 inéditos, 72)", tab_ac)}
{detalhes("Pares caso a caso: entre as bibliotecas da corrida e contra as corridas anteriores", tab_par)}
"""
    dados_js = {"explorador": explorador, "confianca": dados_conf,
                "trilhas": [{"rot": nome(c).split(" · "), "sustentado": c["acerto_por_sustentacao"]["sustentado"]["acerto_pct"],
                             "nao": c["acerto_por_sustentacao"]["nao_sustentado"]["acerto_pct"],
                             "n_sus": c["acerto_por_sustentacao"]["sustentado"]["n"], "n_nao": c["acerto_por_sustentacao"]["nao_sustentado"]["n"]} for c in cs]}
    itens_kpi = [
        ("Diagnósticos remontados", str(total), f"{len(cs)} corridas gravadas, sem rodar modelo"),
        ("Sem raciocínio escrito", f"{sem} de {total}", "o modelo vai direto às quatro linhas pedidas"),
        ("Prompt provado por inteiro", f"{inteiro} de {total}", f"nos outros {so_doc} só a documentação entregue tem prova gravada" + (f"; {nao_comp} não comprovados" if nao_comp else "")),
        ("Verbetes citados fora do contexto", f"{fora_ctx} de {citadas}", "o modelo só citou o que recebeu" if fora_ctx == 0 else "citações a verbete que não foi entregue"),
        ("Causa fora das 23 permitidas", str(fora_conj), "respostas com causa inventada"),
        ("Causa sem apoio no contexto", str(sem_apoio), "respostas cuja causa nenhum verbete entregue trata"),
    ]
    linhas_conf = "".join(
        f'<tr data-conferencia="{html.escape(x["regra"], quote=True)}"><td>{esc(nome(c))}</td><td>{esc(ROTULO_CONFERENCIA.get(x["regra"], x["regra"]))}</td>'
        f'<td class=num>{x.get("confere", 0)}</td><td class=num>{x.get("nao_confere", 0)}</td><td class=num>{x.get("nao_se_aplica", 0)}</td>'
        f'<td class=num>{x.get("nao_verificavel", 0) + x.get("informativo", 0)}</td></tr>' for c in cs for x in c["conferencias"])
    tab_conf = ('<div class="tabela"><table><thead><tr><th>Trilha</th><th>Conferência (sem usar o gabarito)</th><th>Confere</th><th>Não confere</th>'
                f'<th>Não se aplica</th><th>Não verificável ou informativo</th></tr></thead><tbody>{linhas_conf}</tbody></table></div>')
    tab_sus = tabela(["Trilha", "Diagnósticos", "Acerto quando algum verbete do contexto trata da causa respondida", "Acerto quando nenhum trata"],
                     [[nome(c), c["diagnosticos"],
                       f'{fmt(c["acerto_por_sustentacao"]["sustentado"]["acerto_pct"])}% ({c["acerto_por_sustentacao"]["sustentado"]["acertos"]} de {c["acerto_por_sustentacao"]["sustentado"]["n"]})',
                       f'{fmt(c["acerto_por_sustentacao"]["nao_sustentado"]["acerto_pct"])}% ({c["acerto_por_sustentacao"]["nao_sustentado"]["acertos"]} de {c["acerto_por_sustentacao"]["nao_sustentado"]["n"]})']
                      for c in cs])
    bloco_exemplo = ""
    if exemplo:
        bloco_exemplo = ('<h2>Como é o relatório de um caso</h2>\n<p>Um dos relatórios da vitrine, inteiro: um caso da troca cruzada em que o Coder 3B, lendo a biblioteca do '
                         '<code>qwen2.5:7b</code>, respondeu uma causa que nenhum verbete entregue tratava. O relatório é gerado por script, só do arquivo bruto; as três '
                         'camadas vêm separadas, e a resposta certa aparece numa seção só.</p>\n'
                         + detalhes("Abrir o relatório do caso", '<div class="relatorio">' + _relatorio_para_html(exemplo) + "</div>"))
    # (23/10/2026) o bloco da literatura da parte B (onda 1): mapa de arquitetura, riscos, leitura e sínteses
    bloco_literatura, cartoes_literatura, fonte_literatura = _literatura_do_raciocinio(levantamento)
    itens_kpi += cartoes_literatura
    html_ = f'''<section id="raciocinio" hidden>
<h1>{titulo}</h1>
<p class="lead">Em parte. Dá para ver tudo o que o programa fez (o que a busca pontuou e entregou, o prompt, a resposta, os tempos) e conferir por código o que o modelo declarou. O raciocínio em si não está lá: em {sem} dos {total} diagnósticos remontados o modelo não escreveu nenhum, foi direto às quatro linhas. Por isso o relatório separa três camadas e nunca trata a alegação do modelo como fato.</p>
{kpis(itens_kpi)}
<h2>As três camadas</h2>
{leitura(["<strong>O que o programa fez</strong> é fato: o caso que entrou, os verbetes que a busca pontuou e os que entregou, o prompt montado, a resposta crua, os tempos. Nas corridas gravadas o prompt não foi guardado; ele é remontado pelas mesmas funções do executor, e cada trilha diz até onde essa remontagem está provada.",
          "<strong>O que o modelo declarou</strong> é alegação: a causa, o campo, a frase de impacto e os verbetes citados, sempre como trecho literal da resposta, com a posição.",
          "<strong>O que o código conferiu</strong> é o que se pôde checar da alegação sem saber a resposta certa. O que não dá para conferir por código (a frase de impacto, e qual nota de um verbete o modelo usou) é dito, não omitido."])}
<h2>Um sinal que o agente pode calcular sozinho</h2>
<p>Em cada resposta o código pergunta: algum verbete entregue ao modelo trata da causa que ele respondeu? Não precisa de gabarito.{texto_sinal} Os grupos "quando não" são pequenos; a sonda de confiança (corrida 12) mede o mesmo sinal junto com a probabilidade da causa respondida.</p>
<div class="chart"><canvas id="g-ra-sus"></canvas></div>
{tab_sus}
<h2>O que o código conferiu, por trilha</h2>
<p>Oito conferências por resposta, todas sem usar o gabarito. As duas últimas não dão veredito: a lista das notas do modelo nos verbetes citados é informativa, e a frase de impacto não tem como ser conferida por código.</p>
{detalhes("Todas as conferências, trilha por trilha", tab_conf)}
{bloco_conf}
{pe.bloco_html(explorador)}
{bloco_exemplo}
{bloco_literatura}
<h2>Leitura</h2>
{leitura([
    f"<strong>O modelo decidido não mostra o caminho.</strong> Em {sem} de {total} respostas não há texto antes das quatro linhas, embora o prompt peça uma explicação curta. O que se abre é o caminho do programa e a conferência das alegações, não um raciocínio escrito.",
    leitura_fontes,
    "<strong>O erro mais comum não é inventar, é responder uma causa que a documentação entregue não trata.</strong> Esse caso é detectável em código, na hora, e vira candidato a aviso para quem desenvolve.",
    "<strong>O relatório mostra de quem é cada nota.</strong> Quando o verbete citado tem notas escritas pelo modelo, o relatório lista quantas são e o veredito da revisão humana de cada uma; não dá para saber qual delas pesou na resposta, e isso fica escrito.",
    ("<strong>A probabilidade da causa respondida é o melhor dos três sinais, e nenhum deles é barreira.</strong> A seção da corrida 12, acima, traz os números; o que a literatura da parte B sustenta para a arquitetura da trilha está na seção acima, e a especificação da trilha para a Fase 4 sai dela." if tot
     else "A análise da probabilidade da causa respondida entra nesta aba quando a corrida 12 terminar; o que a literatura da parte B sustenta para a arquitetura da trilha está na seção acima, e a especificação da trilha para a Fase 4 sai dela.")])}
{fontes(["<code>resultados_alvo/pre_fase4/confianca.json</code> e <code>.md</code> (<code>analisar_confianca.py</code>, corrida 12 em <code>resultados_alvo/pre_fase4_confianca/</code>)", "<code>resultados_alvo/pre_fase4/indicadores_raciocinio.json</code> (<code>gerar_relatorio_raciocinio.py --vitrine</code>, com <code>--check</code>)", "trilhas em <code>resultados_alvo/pre_fase4/trilhas/</code> (<code>trilha.py</code>) e relatórios em <code>resultados_alvo/pre_fase4/relatorios/</code>"] + ([fonte_literatura] if fonte_literatura else []) + ["decisão 70; roadmap §3.1"])}
</section>'''
    return dados_js, html_


ROTULO_CONFERENCIA = {
    "quatro_linhas_presentes": "A resposta tem as quatro linhas pedidas",
    "rotulo_no_conjunto": "A causa está entre as permitidas",
    "fonte_existe_na_biblioteca": "O verbete citado existe na biblioteca",
    "fonte_estava_no_contexto": "O verbete citado estava no contexto entregue ao modelo",
    "campo_existe_no_caso": "O campo apontado aparece no caso",
    "rotulo_sustentado_por_verbete_do_contexto": "Algum verbete do contexto trata da causa respondida",
    "notas_nos_verbetes_citados": "Notas escritas pelo modelo nos verbetes citados",
    "impacto": "Frase de impacto",
}


# ------------------------------------------------------------------ JS e CSS das abas novas

JS_TOPICOS = r"""
const T = D.topicos;
// ! Alteração de IA - Revisar: (05/11/2026) nomes legíveis nos eixos e nas legendas dos gráficos das abas da Fase 4; os identificadores seguem nas tabelas recolhidas.
// ! Motivo: os eixos mostravam nomes de código, como regra_b_por_gatilho e contrato-malformed_json, que só quem leu o script entende; o Eric pediu a leitura sem jargão.
const NOMES = {divergencia:'divergência, como a corrida rodou', por_gatilho:'divergência, só por gatilho', regra_b:'regra alternativa, em todos os casos', regra_b_por_gatilho:'regra alternativa, só por gatilho',
  remocao_ou_troca:'tirar ou trocar o verbete muda a resposta', sem_documentacao:'sem documentação, a resposta muda', repeticao_mudou:'repetir a pergunta muda a resposta', selo_baixo:'selo de confiança baixo', falha:'conferência em código não passa', qualquer:'qualquer um dos sinais',
  verbete_trocado:'verbete trocado', contrato_alterado:'contrato alterado', seletor_quebrado:'seletor quebrado',
  'front-busca':'busca', 'front-admin-login':'login do administrador', 'front-admin-produtos':'lista de produtos do administrador', 'front-cliente-reserva':'reserva do cliente',
  'contrato-malformed_json':'resposta cortada no meio', 'contrato-field_missing':'campo sumiu da resposta', 'contrato-field_renamed':'campo mudou de nome', 'contrato-type_drift':'campo mudou de tipo', 'contrato-escala_ou_unidade_errada':'preço na escala errada', 'contrato-error_500':'API devolve erro 500',
  'localizador-front-busca':'localizador: busca', 'localizador-front-admin-login':'localizador: login do administrador', 'localizador-front-admin-produtos':'localizador: lista de produtos', 'localizador-front-cliente-reserva':'localizador: reserva do cliente'};
const nome = s => NOMES[s] || String(s).replace(/_/g, ' ');
const rgba = (hex, a) => { const n = parseInt(hex.slice(1), 16); return `rgba(${n>>16&255},${n>>8&255},${n&255},${a})`; };
// ! Alteração de IA - Revisar: (05/11/2026) gráficos das abas Modelos, Entre fases e Pesquisa, que só tinham tabela.
// ! Motivo: o Eric pediu o gráfico à vista e os dados em "mais informações"; essas abas ficariam sem nada para ver com as tabelas recolhidas.
function modGraficos(){
  const L = document.getElementById('sel-mod-l').value;
  const barras = (id, fonte, nomes) => { const chaves = Object.keys(nomes);
    grafico(id, {type:'bar', data:{labels: chaves.map(k => nomes[k]), datasets: D.modelos.map(m => ({label:m, data: chaves.map(k => ((fonte[m]||{})[k]||{})[L] ?? null), backgroundColor:cor(m)}))},
      options:{responsive:true, maintainAspectRatio:false, scales:{y:{min:0, max:100, title:{display:true, text:'acerto nos 90 casos (%)'}}}, plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+c.formattedValue+'%'}}}}}); };
  barras('g-mod-classe', D.classes, {1:'léxica', 2:'sintática', 3:'semântica', 4:'tradução', 5:'runtime', 6:'efeito'});
  barras('g-mod-nivel', D.niveis, {1:'fácil', 2:'médio', 3:'difícil'});
}
function cmpEtapas(){
  const conj = document.getElementById('sel-cmp-conj').value, met = document.getElementById('sel-cmp-met').value;
  const cols = ['2A_linear_ryzen','2B_A0','2B_A2','F3_L0','F3_L1','F3_L2','F3_L3'];
  const rot = ['Sem documentação (2-A)','Sem documentação (2-B)','Biblioteca à mão (2-B)','Original (Fase 3)','1ª versão do modelo','2ª versão','3ª versão'];
  grafico('g-cmp-etapas', {type:'line', data:{labels: rot, datasets: D.modelos.map(m => ({label:m, data: cols.map(c => (((D.fases[m]||{})[conj]||{})[c]||{})[met] ?? null), borderColor:cor(m), backgroundColor:cor(m), tension:.15, pointRadius:4, spanGaps:true}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{min:0, max:100, title:{display:true, text: met==='balanceada'?'acurácia balanceada (%)':'acerto (%)'}}}, plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+c.formattedValue+'%'}}}}});
}
function peRodadas(){
  const R = (T.pesquisa||{}).rodadas||[]; if(!R.length) return;
  grafico('g-pe-rodadas', {type:'bar', data:{labels: R.map(x => x.rodada), datasets:[
      {label:'aprovadas', data: R.map(x => x.aprovadas), backgroundColor: css('--bom')},
      {label:'rejeitadas', data: R.map(x => x.rejeitadas), backgroundColor: css('--ruim')},
      {label:'não verificadas', data: R.map(x => x.nao_verificadas), backgroundColor: css('--s4')}]},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true, beginAtZero:true, title:{display:true, text:'afirmações'}}, y:{stacked:true}}}});
}
function cqTrajetoria(){
  const conj = document.getElementById('sel-cq-conj').value, met = document.getElementById('sel-cq-met').value; const pts = T.cq.trajetoria[conj];
  grafico('g-cq-traj', {type:'line', data:{labels: pts.map(p => p.rot), datasets:[T.cq.A, T.cq.B].map(m => ({label:m, data: pts.map(p => p[met+(m===T.cq.A?'_A':'_B')]), borderColor:cor(m), backgroundColor:cor(m), tension:.2, pointRadius:4}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text: met==='bal'?'acurácia balanceada (%)':'acerto (%)'}, suggestedMin:40, suggestedMax:95}}, plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+c.formattedValue+'%'}}}}});
}
function cqConfronto(){
  const conj = document.getElementById('sel-cq-conf').value; const rows = T.cq.confronto[conj];
  grafico('g-cq-conf', {type:'bar', data:{labels: rows.map(r => r.rot), datasets:[{label:'só o '+T.cq.A+' acertou', data: rows.map(r => r.so_A), backgroundColor:cor(T.cq.A)}, {label:'só o '+T.cq.B+' acertou', data: rows.map(r => r.so_B), backgroundColor:cor(T.cq.B)}]},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'casos'}, beginAtZero:true}}, plugins:{tooltip:{callbacks:{afterLabel: c => { const r = rows[c.dataIndex]; return `ambos ${r.ambos} · nenhum ${r.nenhum} · p (McNemar) ${r.p}`; }}}}}});
}
function cqRevisao(){
  const cats = ['Correta','Parcial','Errada'], cores = {Correta:css('--bom'),Parcial:css('--meio'),Errada:css('--ruim')}; const mods = [T.cq.A, T.cq.B];
  grafico('g-cq-rev', {type:'bar', data:{labels: mods, datasets: cats.map(k => ({label:k, data: mods.map(m => T.cq.revisao[m===T.cq.A?'A':'B'][k]), backgroundColor: cores[k]}))},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true, max:100, title:{display:true,text:'% das edições revisadas'}}, y:{stacked:true}}, plugins:{tooltip:{callbacks:{afterLabel: c => 'n = '+T.cq.revisao[c.label===T.cq.A?'A':'B'].n}}}}});
}
function tbGeneraliza(){
  const met = document.getElementById('sel-tb-met').value; const ds = [];
  T.tresb.modelos.forEach(m => { ds.push({label:m+' · 36 oficiais', data: T.tresb.Ls.map(l => T.tresb.oficiais[m][l][met]), borderColor:cor(m), backgroundColor:cor(m), tension:.2, pointRadius:4});
    ds.push({label:m+' · 36 inéditos', data: T.tresb.Ls.map(l => T.tresb.ineditos[m][l][met]), borderColor:cor(m), backgroundColor:cor(m), borderDash:[6,4], tension:.2, pointRadius:4, pointStyle:'rectRot'}); });
  grafico('g-tb-gen', {type:'line', data:{labels: T.tresb.Ls.map(l => 'L'+l), datasets: ds},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text: met==='bal'?'acurácia balanceada (%)':'acerto (%)'}, suggestedMin:50, suggestedMax:95}}, plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+c.formattedValue+'%'}}}}});
}
function tbRecuperacao(){
  const ds = [];
  T.tresb.modelos.forEach(m => { ds.push({label:m+' · inéditos', data: T.tresb.Ls.map(l => T.tresb.rec_ineditos[m][l]), backgroundColor:cor(m)}); ds.push({label:m+' · oficiais', data: T.tresb.Ls.map(l => T.tresb.rec_oficiais[m][l]), backgroundColor:rgba(cor(m), .4)}); });
  grafico('g-tb-rec', {type:'bar', data:{labels: T.tresb.Ls.map(l => 'L'+l), datasets: ds}, options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'verbete certo entre os três entregues (%)'}, min:0, max:100}}}});
}
function curOperacoes(){
  const cats = ['Correta','Parcial','Errada'], cores = {Correta:css('--bom'),Parcial:css('--meio'),Errada:css('--ruim')};
  grafico('g-cur-op', {type:'bar', data:{labels: T.curadoria.operacoes, datasets: cats.map(k => ({label:k, data: T.curadoria.operacoes.map(o => T.curadoria.por[o][k]||0), backgroundColor: cores[k]}))},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true, title:{display:true,text:'edições'}, beginAtZero:true}, y:{stacked:true}}}});
}
function recMetodos(){
  const bib = document.getElementById('sel-rec-bib').value, met = document.getElementById('sel-rec-met').value; const v = T.recuperador.valores[bib]||{};
  grafico('g-rec-met', {type:'bar', data:{labels: T.recuperador.metodos, datasets: T.recuperador.conjuntos.map((c, i) => ({label:c, data: T.recuperador.metodos.map(m => (v[c]||{})[m] ? v[c][m][met] : null), backgroundColor: css('--s'+(i+1))}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text: met==='mrr'?'MRR':met+' (%)'}, min:0, max: met==='mrr'?1:100}}}});
}
function ablBarras(){
  const L = T.ablacao.linhas; const series = [['acerto','acerto (%)'],['formato','formato válido (%)'],['fora','rótulo fora do conjunto (%)']];
  grafico('g-abl', {type:'bar', data:{labels: L.map(x => x.modelo.replace('qwen2.5:','')+' · '+x.cond), datasets: series.map(([k, nome], i) => ({label:nome, data: L.map(x => x[k]), backgroundColor: css('--s'+(i+1))}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{min:0, max:100, title:{display:true,text:'% dos 90 casos'}}}, plugins:{tooltip:{callbacks:{afterLabel: c => c.datasetIndex===0 ? 'IC 95% '+L[c.dataIndex].ic.join('–') : ''}}}}});
}
function czLeitores(){
  const met = document.getElementById('sel-cz-met').value; const C = T.cruzada; const ds = [];
  ds.push({label: C.doador+' · a biblioteca que ele escreveu (Fase 3)', data: C.versoes.map(v => C.propria[C.doador][v][met]), borderColor:cor(C.doador), backgroundColor:cor(C.doador), tension:.2, pointRadius:4});
  C.leitores.forEach(m => { ds.push({label: m+' · a biblioteca do '+C.doador, data: C.versoes.map(v => C.doador_lido[m][v][met]), borderColor:cor(m), backgroundColor:cor(m), tension:.2, pointRadius:4});
    ds.push({label: m+' · a própria biblioteca (Fase 3)', data: C.versoes.map(v => C.propria[m][v][met]), borderColor:cor(m), backgroundColor:cor(m), borderDash:[6,4], tension:.2, pointRadius:4, pointStyle:'rectRot'}); });
  grafico('g-cz-leit', {type:'line', data:{labels: C.versoes.map(v => 'L'+v), datasets: ds},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text: met==='bal'?'acurácia balanceada nos 36 (%)':'acerto nos 36 (%)'}, suggestedMin:50, suggestedMax:95}}, plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+c.formattedValue+'%'}}}}});
}
function czTrocas(){
  const R = T.cruzada.trocas;
  grafico('g-cz-trocas', {type:'bar', data:{labels: R.map(r => r.rot), datasets:[{label:'passou a acertar', data: R.map(r => r.b), backgroundColor: css('--bom')}, {label:'deixou de acertar', data: R.map(r => -r.c), backgroundColor: css('--ruim')}]},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true, title:{display:true,text:'casos em 36 (perdas à esquerda, ganhos à direita)'}, ticks:{stepSize:1, callback: v => Math.abs(v)}}, y:{stacked:true, ticks:{autoSkip:false}}},
      plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+Math.abs(c.raw)+' caso(s)', afterBody: it => { const r = R[it[0].dataIndex]; return 'saldo: '+(r.b - r.c > 0 ? '+' : '')+(r.b - r.c); }}}}}});
}
function coMinutos(){
  const B = (T.colibri||{}).barras||[]; if(!B.length) return;
  grafico('g-co-min', {type:'bar', data:{labels: B.map(b => b.rot), datasets:[
      {label:'este projeto hoje: diagnóstico inteiro', data: B.map(b => b.hoje ? b.minutos : null), backgroundColor: css('--s1')},
      {label:'colibri em máquinas de terceiros: só a geração da resposta', data: B.map(b => b.hoje ? null : b.minutos), backgroundColor: css('--s2')}]},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false,
      scales:{x:{stacked:true, beginAtZero:true, title:{display:true, text:'minutos para uma resposta de '+T.colibri.tokens+' tokens'}}, y:{stacked:true, ticks:{autoSkip:false}}},
      plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+c.formattedValue+' min', afterLabel: c => B[c.dataIndex].nota}}}}});
}
function raSustentacao(){
  const L = (T.raciocinio||{}).trilhas||[]; if(!L.length) return;
  grafico('g-ra-sus', {type:'bar', data:{labels: L.map(x => x.rot), datasets:[
      {label:'algum verbete do contexto trata da causa respondida', data: L.map(x => x.sustentado), backgroundColor: css('--s1')},
      {label:'nenhum verbete do contexto trata', data: L.map(x => x.nao), backgroundColor: css('--s2')}]},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{min:0, max:100, title:{display:true, text:'acerto (%)'}}},
      plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+c.formattedValue+'%', afterLabel: c => 'n = '+(c.datasetIndex===0 ? L[c.dataIndex].n_sus : L[c.dataIndex].n_nao)}}}}});
}
function raConfianca(){
  const C = (T.raciocinio||{}).confianca; if(!C || !C.bibliotecas.length) return;
  grafico('g-ra-conf', {type:'bar', data:{labels: C.sinais, datasets: C.bibliotecas.map((b, i) => ({label: b.rot, data: b.auroc, backgroundColor: css('--s' + (i + 1))}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{min:0.4, max:1, title:{display:true, text:'AUROC (0,5 = sortear)'}}},
      plugins:{tooltip:{callbacks:{label: c => c.dataset.label + ': ' + (c.raw === null ? 'n/d' : c.formattedValue)}}}}});
}
function ceTemas(){
  const Tm = (T.cerebro||{}).temas||[]; if(!Tm.length) return;
  grafico('g-ce-temas', {type:'bar', data:{labels: Tm.map(t => t.tema), datasets:[
      {label:'serve agora', data: Tm.map(t => t.adotado), backgroundColor: css('--bom')},
      {label:'só com outra máquina, outro motor ou depois da Fase 4', data: Tm.map(t => t.adiado), backgroundColor: css('--s3')},
      {label:'não serve', data: Tm.map(t => t.descartado), backgroundColor: css('--ruim')}]},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false,
      scales:{x:{stacked:true, beginAtZero:true, ticks:{stepSize:1}, title:{display:true, text:'opções avaliadas no mapa da onda 2'}}, y:{stacked:true, ticks:{autoSkip:false}}},
      plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+c.formattedValue}}}}});
}
function ferMcp(){
  if(!T.ferramental.mcp) return; const met = document.getElementById('sel-fer-met').value; const S = T.ferramental.mcp;
  grafico('g-fer-mcp', {type:'bar', data:{labels: S.map(x => x.tarefa), datasets:[{label:'grep, Glob e Read', data: S.map(x => Math.round(x['grep_'+met])), backgroundColor: css('--s1')}, {label:'servidor codebase-memory', data: S.map(x => Math.round(x['mcp_'+met])), backgroundColor: css('--s2')}]},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'tokens (média de 2 repetições)'}, beginAtZero:true}}}});
}
function repClasses(){
  const R = T.reproducao||{}; const C = R.classes||[]; if(!C.length || !C.some(c => c.avaliacao)) return;
  const rot = R.rotulos||{};
  const ds = [{label:(rot.avaliacao||'avaliação')+': com tela e modo', data: C.map(c => c.avaliacao ? c.avaliacao.na_tela : null), backgroundColor: css('--s1')},
              {label:(rot.avaliacao||'avaliação')+': reproduzem', data: C.map(c => c.avaliacao ? c.avaliacao.reproduzem : null), backgroundColor: css('--s2')}];
  if(C.some(c => c.ineditos)) ds.push({label:(rot.ineditos||'inéditos')+': com tela e modo', data: C.map(c => c.ineditos ? c.ineditos.na_tela : null), backgroundColor: css('--s3')},
                                      {label:(rot.ineditos||'inéditos')+': reproduzem', data: C.map(c => c.ineditos ? c.ineditos.reproduzem : null), backgroundColor: css('--s4')});
  grafico('g-rep-classe', {type:'bar', data:{labels: C.map(c => c.classe+' '+c.nome), datasets: ds},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'casos'}, beginAtZero:true, ticks:{stepSize:2}}}}});
}
// aba Calibração (27/10/2026, P3): acerto, acurácia balanceada e AUROC por k; curva risco-cobertura do k escolhido
function calK(){
  const C = T.calibracao||{}; const K = C.por_k||[]; if(!K.length) return;
  grafico('g-cal-k', {type:'bar', data:{labels: K.map(x => x.k+' verbetes (k = '+x.k+')'), datasets:[
    {label:'acerto (%)', data: K.map(x => x.acerto_pct), backgroundColor: css('--s1')},
    {label:'acurácia balanceada (%)', data: K.map(x => x.acuracia_balanceada_pct), backgroundColor: css('--s2')},
    {label:'quanto a probabilidade separa erros de acertos (AUROC x 100)', data: K.map(x => x.auroc_p == null ? null : Math.round(x.auroc_p * 1000) / 10), backgroundColor: css('--s3')}]},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{beginAtZero:true, max:100, title:{display:true,text:'%'}}}}});
}
function calCurva(){
  const C = T.calibracao||{}; const P = C.curva||[]; if(!P.length) return;
  grafico('g-cal-curva', {type:'line', data:{labels: P.map(p => Math.round(p.cobertura * 100) + '%'),
    datasets:[{label:'risco (erros entre os casos respondidos, %)', data: P.map(p => Math.round(p.risco * 1000) / 10), borderColor: css('--s2'), backgroundColor: css('--s2'), fill:false, pointRadius:2, tension:0}]},
    options:{responsive:true, maintainAspectRatio:false, scales:{x:{title:{display:true,text:'cobertura (da maior probabilidade para a menor)'}}, y:{beginAtZero:true, title:{display:true,text:'risco (%)'}}}}});
}
// ! Alteração de IA - Revisar: (06/11/2026) a aba da corrida 24: certos e errados por classe de defeito e com e sem o verbete certo no contexto.
// ! Motivo: são as duas coisas que a corrida mostrou: a classe de tradução é onde mais erra, e o verbete certo é o que mais pesa.
function inedClasse(){
  const C = (T.ineditosf4||{}).por_classe||[]; if(!C.length) return;
  grafico('g-ined-classe', {type:'bar', data:{labels: C.map(c => c.classe+' '+c.nome), datasets:[
    {label:'acertos', data: C.map(c => c.acertos), backgroundColor: css('--bom')},
    {label:'erros', data: C.map(c => c.erros), backgroundColor: css('--ruim')}]},
    options:{responsive:true, maintainAspectRatio:false, indexAxis:'y', scales:{x:{stacked:true, beginAtZero:true, ticks:{stepSize:1}, title:{display:true,text:'casos'}}, y:{stacked:true}}}});
}
function inedVerbete(){
  const V = (T.ineditosf4||{}).verbete; if(!V) return;
  const lados = [['com o verbete certo', V.presente], ['sem o verbete certo', V.ausente]];
  grafico('g-ined-verbete', {type:'bar', data:{labels: lados.map(x => x[0]), datasets:[
    {label:'acertos', data: lados.map(x => x[1].acertos), backgroundColor: css('--bom')},
    {label:'erros', data: lados.map(x => x[1].casos - x[1].acertos), backgroundColor: css('--ruim')}]},
    options:{responsive:true, maintainAspectRatio:false, indexAxis:'y', scales:{x:{stacked:true, beginAtZero:true, title:{display:true,text:'casos'}}, y:{stacked:true}}}});
}
// aba Pós-Fase 4 (07/11/2026): fontes com endereço por leitura da rodada 6, coloridas pela parte do pedido
// ! Alteração de IA - Revisar: (07/11/2026, Pós-Fase 4, pacote Q2) os dois gráficos da aba "O que chega ao analista": a parcela de textos dentro de cada limiar, por grupo e versão, e os termos sem o significado antes e depois.
// ! Motivo: a aba nova segue a regra do painel (um ou dois gráficos lidos do JSON); as cores vêm da paleta validada (--s1, --s2, --s4, --s6), e a legenda nomeia cada série.
function txtCriterios(){
  const C = (T.texto||{}).criterios; if(!C) return;
  grafico('g-texto-criterios', {type:'bar', data:{labels: C.rotulos, datasets: C.series.map(s => ({label: s.nome, data: s.pct, backgroundColor: css(s.cor)}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{min:0, max:100, title:{display:true, text:'textos dentro do limiar (%)'}}}, plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+c.formattedValue+'%'}}}}});
}
function txtTermos(){
  const R = (T.texto||{}).termos; if(!R || !R.rotulos.length) return;
  grafico('g-texto-termos', {type:'bar', data:{labels: R.rotulos, datasets:[{label:'antes (v2 e verbetes)', data: R.antes, backgroundColor: css('--s4')}, {label:'depois (v3 e camada de leitura)', data: R.depois, backgroundColor: css('--s1')}]},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, scales:{x:{beginAtZero:true, title:{display:true, text:'textos em que o termo aparece sem o significado'}}}}});
}
function posFontes(){
  const L = (T.posfase4||{}).leituras||[]; if(!L.length) return;
  grafico('g-pos4-fontes', {type:'bar', data:{labels: L.map(x => x.rotulo), datasets:[
    {label:'fontes com endereço', data: L.map(x => x.fontes), backgroundColor: L.map(x => css(x.cor))}]},
    options:{responsive:true, maintainAspectRatio:false, indexAxis:'y', plugins:{legend:{display:false}}, scales:{x:{beginAtZero:true, ticks:{stepSize:2}, title:{display:true,text:'fontes com endereço'}}}}});
}
// aba Tela e fixture (01/11/2026, corrida 18): acerto na tela e no fixture por classe; rótulos dados em cada lado
function telaClasses(){
  const D = T.tela||{}; const C = D.por_classe||[]; if(!C.length) return;
  // ! Alteração de IA - Revisar: (05/11/2026, corrida 18c) com a 18c, o gráfico compara a tela antes e depois do corte com o caso escrito, e a corrida 18 fica na tabela.
  // ! Motivo: cinco séries por grupo não se liam, e o que importa agora é a 18c contra a 18b; a corrida 18 mediu um defeito do caso de entrada, já corrigido.
  // ! Alteração de IA - Revisar: (06/11/2026, decisão 97) com a 18d, o gráfico compara a tela antes e depois dos sinais novos da busca com o caso escrito.
  // ! Motivo: é o que a corrida mediu; as séries das corridas de antes continuam na tabela recolhida.
  if(C.some(c => c.acerto_tela_v4 != null)){
    grafico('g-tela-classe', {type:'bar', data:{labels: C.map(c => c.classe+' '+c.nome), datasets:[
      {label:'casos', data: C.map(c => c.casos), backgroundColor: css('--s4')},
      {label:'acerto na tela (18c, antes dos sinais da busca)', data: C.map(c => c.acerto_tela_v3), backgroundColor: css('--s3')},
      {label:'acerto na tela (18d, com os sinais da busca)', data: C.map(c => c.acerto_tela_v4), backgroundColor: css('--s1')},
      {label:'acerto no caso escrito (18d)', data: C.map(c => c.acerto_fixture_v4), backgroundColor: css('--s2')}]},
      options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'casos'}, beginAtZero:true, ticks:{stepSize:1}}}}});
    return;
  }
  if(C.some(c => c.acerto_tela_v3 != null)){
    grafico('g-tela-classe', {type:'bar', data:{labels: C.map(c => c.classe+' '+c.nome), datasets:[
      {label:'casos', data: C.map(c => c.casos), backgroundColor: css('--s4')},
      {label:'acerto na tela (18b, prompt acima do limite)', data: C.map(c => c.acerto_tela_v2), backgroundColor: css('--s3')},
      {label:'acerto na tela (18c, prompt dentro do limite)', data: C.map(c => c.acerto_tela_v3), backgroundColor: css('--s1')},
      {label:'acerto no caso escrito (18c)', data: C.map(c => c.acerto_fixture_v3), backgroundColor: css('--s2')}]},
      options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'casos'}, beginAtZero:true, ticks:{stepSize:1}}}}});
    return;
  }
  const ds = [
    {label:'casos', data: C.map(c => c.casos), backgroundColor: css('--s4')},
    {label:'acerto na tela (18)', data: C.map(c => c.acerto_tela), backgroundColor: css('--s1')},
    {label:'acerto no caso escrito', data: C.map(c => c.acerto_fixture), backgroundColor: css('--s2')},
    ];
  // ! Alteração de IA - Revisar: (05/11/2026) o gráfico deixa de trazer as séries "mesmo rótulo", que seguem na tabela recolhida.
  // ! Motivo: seis séries por grupo não se liam; nos casos desta corrida, "mesmo rótulo" fica perto do acerto na tela.
  if(C.some(c => c.acerto_tela_v2 != null)) ds.push({label:'acerto na tela (18b, caso revisado)', data: C.map(c => c.acerto_tela_v2), backgroundColor: css('--s3')});
  grafico('g-tela-classe', {type:'bar', data:{labels: C.map(c => c.classe+' '+c.nome), datasets: ds},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'casos'}, beginAtZero:true, ticks:{stepSize:1}}}}});
}
function telaRotulos(){
  const D = T.tela||{}; const R = D.rotulos||[]; if(!R.length) return;
  const com18c = R.some(x => x.tela_v3 != null);
  const com18d = R.some(x => x.tela_v4 != null);
  const ds = com18d ? [
    {label:'é o gabarito de', data: R.map(x => x.gabarito), backgroundColor: css('--s4')},
    {label:'respondida na tela (18d)', data: R.map(x => x.tela_v4), backgroundColor: css('--s1')},
    {label:'respondida no caso escrito (18d)', data: R.map(x => x.fixture_v4), backgroundColor: css('--s2')}] : com18c ? [
    {label:'é o gabarito de', data: R.map(x => x.gabarito), backgroundColor: css('--s4')},
    {label:'respondida na tela (18c)', data: R.map(x => x.tela_v3), backgroundColor: css('--s1')},
    {label:'respondida no caso escrito (18c)', data: R.map(x => x.fixture_v3), backgroundColor: css('--s2')}] : [
    {label:'é o gabarito de', data: R.map(x => x.gabarito), backgroundColor: css('--s4')},
    {label:'respondida na tela (18)', data: R.map(x => x.tela), backgroundColor: css('--s1')},
    {label:'respondida no caso escrito', data: R.map(x => x.fixture), backgroundColor: css('--s2')}];
  if(!com18c && R.some(x => x.tela_v2 != null)) ds.push({label:'respondida na tela (18b, caso revisado)', data: R.map(x => x.tela_v2), backgroundColor: css('--s5')});
  grafico('g-tela-rotulos', {type:'bar', data:{labels: R.map(x => nome(x.rotulo)), datasets: ds},
    options:{responsive:true, maintainAspectRatio:false, indexAxis:'y', scales:{x:{title:{display:true,text:'casos'}, beginAtZero:true, ticks:{stepSize:2}}, y:{ticks:{autoSkip:false, font:{size:11}}}}}});
}
// ! Alteração de IA - Revisar: (05/11/2026, corrida 18c) o que mudou de uma corrida para outra e o acerto com e sem o verbete certo no contexto.
// ! Motivo: a primeira responde se o corte ajudou, e a segunda explica o que ainda separa a tela do caso escrito.
function telaCorridas(){
  const L = (T.tela||{}).corridas||[]; if(!L.length) return;
  grafico('g-tela-corridas', {type:'bar', data:{labels: L.map(x => 'corrida '+x.nome), datasets:[
    {label:'acerto na tela', data: L.map(x => x.acerto_tela), backgroundColor: css('--s1')},
    {label:'acerto no caso escrito', data: L.map(x => x.acerto_fixture), backgroundColor: css('--s2')},
    {label:'mesma causa nos dois lados', data: L.map(x => x.concordam), backgroundColor: css('--s3')}]},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'casos, de '+L[L.length-1].casos}, beginAtZero:true}}}});
}
// ! Alteração de IA - Revisar: (06/11/2026, decisão 98) o que a tela perde e o que ela ganha para o caso escrito, corrida a corrida, contra o limite da regra R2.
// ! Motivo: a regra passou a contar só os casos que a tela perde, e o gráfico mostra as duas contas lado a lado, como o Eric fixou antes da corrida 18d.
function telaRegra(){
  const D = T.tela||{}; const L = D.regra||[]; if(!L.length) return;
  grafico('g-tela-regra', {type:'bar', data:{labels: L.map(x => x.rotulo), datasets:[
    {label:'casos que a tela perde para o caso escrito', data: L.map(x => x.perde), backgroundColor: css('--ruim')},
    {label:'casos que a tela ganha do caso escrito', data: L.map(x => x.ganha), backgroundColor: css('--bom')},
    {type:'line', label:'limite de casos perdidos', data: L.map(() => D.limite_r2), borderColor: css('--s4'), backgroundColor: css('--s4'), pointRadius:0, borderWidth:2, fill:false}]},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'casos'}, beginAtZero:true, ticks:{stepSize:2}}}}});
}
function telaVerbete(){
  const D = T.tela||{}; const V = (D.v4||D.v3||{}).verbete; if(!V) return;
  const lados = [['tela, com o verbete certo', V.tela.presente], ['tela, sem o verbete certo', V.tela.ausente], ['caso escrito, com o verbete certo', V.fixture.presente], ['caso escrito, sem o verbete certo', V.fixture.ausente]];
  grafico('g-tela-verbete', {type:'bar', data:{labels: lados.map(x => x[0]), datasets:[
    {label:'acertos', data: lados.map(x => x[1].acertos), backgroundColor: css('--bom')},
    {label:'erros', data: lados.map(x => x[1].casos - x[1].acertos), backgroundColor: css('--ruim')}]},
    options:{responsive:true, maintainAspectRatio:false, indexAxis:'y', scales:{x:{stacked:true, beginAtZero:true, title:{display:true,text:'casos'}}, y:{stacked:true, afterFit: s => { s.width = Math.max(s.width, 220); }}}}});
}
// ! Alteração de IA - Revisar: (05/11/2026, decisão 91) a aba do experimento: acerto de cada condição e os casos que só um lado acerta.
// ! Motivo: a pergunta é se a condição muda o acerto, e a resposta só aparece com a contagem caso a caso ao lado do acerto.
function expAcerto(){
  const E = T.experimento||{}; const C = E.condicoes||[]; if(!C.length) return;
  const L = [{nome:'corrida 16', acerto_pct:E.base.acerto_pct, avaliacao_pct:E.base.avaliacao_pct}].concat(C);
  grafico('g-exp-acerto', {type:'bar', data:{labels: L.map(x => x.nome), datasets:[
    {label:'acerto nos 90 casos', data: L.map(x => x.acerto_pct), backgroundColor: css('--s1')},
    {label:'acerto nos 36 de avaliação', data: L.map(x => x.avaliacao_pct), backgroundColor: css('--s2')}]},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{title:{display:true,text:'% de acerto'}, beginAtZero:true, max:100}}}});
}
function expTrocas(){
  const C = (T.experimento||{}).condicoes||[]; if(!C.length) return;
  grafico('g-exp-trocas', {type:'bar', data:{labels: C.map(x => x.nome), datasets:[
    {label:'só a condição acerta', data: C.map(x => x.b), backgroundColor: css('--bom')},
    {label:'só a corrida 16 acerta', data: C.map(x => x.c), backgroundColor: css('--ruim')}]},
    options:{responsive:true, maintainAspectRatio:false, indexAxis:'y', scales:{x:{beginAtZero:true, ticks:{stepSize:1}, title:{display:true,text:'casos'}}}}});
}
// aba Cura de seletor (01/11/2026, corrida 19): execuções por modo e por roteiro, empilhadas pela regra R3; MTTR por roteiro
function curaEmpilhado(id, L, chave){
  if(!L.length) return;
  grafico(id, {type:'bar', data:{labels: L.map(x => nome(x[chave])), datasets:[
      {label:'curadas, mesmo elemento', data: L.map(x => x.mesmo_elemento), backgroundColor: css('--bom')},
      {label:'curadas, outro elemento', data: L.map(x => x.outro_elemento), backgroundColor: css('--meio')},
      {label:'não curadas', data: L.map(x => x.nao_curadas), backgroundColor: css('--ruim')},
      {label:'não quebrou', data: L.map(x => x.nao_quebrou), backgroundColor: css('--s4')}]},
    options:{responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true}, y:{stacked:true, beginAtZero:true, ticks:{stepSize:2}, title:{display:true, text:'execuções'}}},
      plugins:{tooltip:{callbacks:{afterBody: it => { const x = L[it[0].dataIndex]; return 'taxa de cura ' + (x.taxa == null ? 'n/d' : x.taxa + '%') + ' · MTTR mediana ' + (x.mttr == null ? 'n/d' : x.mttr + ' s'); }}}}}});
}
function curaModos(){ const C = T.cura||{}; curaEmpilhado('g-cura-modo', C.por_modo||[], 'modo'); }
function curaRoteiros(){ const C = T.cura||{}; curaEmpilhado('g-cura-roteiro', C.por_roteiro||[], 'roteiro'); }
// aba Biblioteca em produção (03/11/2026, corrida 20): o que cada filtro barrou e a regra R5 nos inéditos
function bibFiltros(){
  const B = T.biblioteca||{}; const F = B.filtros||[];
  if(!F.length) return;
  grafico('g-bib-filtros', {type:'bar', data:{labels: F.map(x => nome(x.filtro)), datasets:[{label:'propostas barradas ou seguradas', data: F.map(x => x.recusas), backgroundColor: css('--s3')}]},
    options:{responsive:true, maintainAspectRatio:false, indexAxis:'y', scales:{x:{beginAtZero:true, ticks:{stepSize:1}, title:{display:true, text:'propostas'}}}}});
}
function bibReavaliacao(){
  const B = T.biblioteca||{}; const R = B.reavaliacao;
  if(!R) return;
  // ! Alteração de IA - Revisar: (05/11/2026) o gráfico fica só com os dois acertos; b e c seguem no texto da aba e nos cartões.
  // ! Motivo: porcentagem e contagem de casos dividiam o mesmo eixo, e as barras de b e c, com valor zero, não apareciam.
  grafico('g-bib-reavaliacao', {type:'bar', data:{labels:['com a cópia curada', 'com o lote'],
      datasets:[{label:'acerto nos 36 inéditos (%)', data:[R.acerto_base_pct, R.acerto_novo_pct], backgroundColor:[css('--s2'), css('--s1')]}]},
    options:{responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}}, scales:{y:{min:0, max:100, title:{display:true, text:'acerto nos 36 inéditos (%)'}}}}});
}
// aba Cenários da Fase 5 (04/11/2026, corrida 21): MTTR médio e Task Success por cenário, contrato e localizador em cores diferentes
function cenMttr(){
  const C = T.cenarios||{}; const L = C.por_cenario||[];
  if(!L.length) return;
  const ds = C.duas_corridas
    ? [{label:C.rotulo_anterior, data: L.map(x => x.mttr_anterior), backgroundColor: css('--s4')}, {label:C.rotulo_vigente, data: L.map(x => x.mttr_media_s), backgroundColor: css('--s1')}]
    : [{label:'MTTR médio (s)', data: L.map(x => x.mttr_media_s), backgroundColor: L.map(x => x.tipo === 'contrato' ? css('--s1') : css('--s2'))}];
  grafico('g-cen-mttr', {type:'bar', data:{labels: L.map(x => nome(x.cenario)), datasets: ds},
    options:{responsive:true, maintainAspectRatio:false, indexAxis:'y', plugins:{legend:{display: !!C.duas_corridas}},
      scales:{x:{beginAtZero:true, title:{display:true, text:'segundos, da detecção até o resultado'}}, y:{afterFit: s => { s.width = Math.max(s.width, 240); }}}}});
}
function cenSucesso(){
  const C = T.cenarios||{}; const L = C.por_cenario||[];
  if(!L.length) return;
  grafico('g-cen-ts', {type:'bar', data:{labels: L.map(x => nome(x.cenario)), datasets:[
      {label:'chegou ao resultado (Task Success)', data: L.map(x => x.sucessos), backgroundColor: css('--bom')},
      {label:'não chegou', data: L.map(x => x.n - x.sucessos), backgroundColor: css('--ruim')}]},
    options:{responsive:true, maintainAspectRatio:false, indexAxis:'y', scales:{x:{stacked:true, beginAtZero:true, ticks:{stepSize:1}, title:{display:true, text:'execuções'}},
      y:{stacked:true, afterFit: s => { s.width = Math.max(s.width, 240); }}}}});
}
// aba Avaliação da trilha (04/11/2026, corrida 22): TPR, TNR e o produto por sinal (o acaso dá 0,25) e as mutações pelo nó apontado
function triSinais(){
  const A = T.trilha||{}; const S = A.sinais||[];
  if(!S.length) return;
  grafico('g-tri-sinais', {type:'bar', data:{labels: S.map(x => nome(x.sinal)), datasets:[
      {label:'erros que pegou (TPR)', data: S.map(x => x.tpr), backgroundColor: css('--s1')},
      {label:'acertos que deixou em paz (TNR)', data: S.map(x => x.tnr), backgroundColor: css('--s2')},
      {label:'nota (TPR x TNR)', data: S.map(x => x.produto), backgroundColor: css('--s3')}]},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, scales:{x:{beginAtZero:true, max:1, title:{display:true, text:'de 0 a 1; na nota, o acaso dá 0,25'}}, y:{ticks:{autoSkip:false}, afterFit: s => { s.width = Math.max(s.width, 250); }}}}});
}
function triMutacoes(){
  const A = T.trilha||{}; const M = A.mutacoes||[];
  if(!M.length) return;
  grafico('g-tri-mutacoes', {type:'bar', data:{labels: M.map(x => nome(x.tipo)), datasets:[
      {label:'apontou o nó previsto', data: M.map(x => x.previsto), backgroundColor: css('--bom')},
      {label:'apontou outro nó', data: M.map(x => x.outro_no), backgroundColor: css('--ruim')},
      {label:'sem divergência', data: M.map(x => x.sem_divergencia), backgroundColor: css('--meio')},
      {label:'sem alvo', data: M.map(x => x.sem_alvo), backgroundColor: css('--s4')}]},
    options:{responsive:true, maintainAspectRatio:false, indexAxis:'y', scales:{x:{stacked:true, beginAtZero:true, ticks:{stepSize:4}, title:{display:true, text:'casos (roteiros, no seletor)'}},
      y:{stacked:true, afterFit: s => { s.width = Math.max(s.width, 200); }}}}});
}
// ! Alteração de IA - Revisar: (08/11/2026, Pós-Fase 4, pacote Q3) os dois gráficos e o explorador da aba "Árvore de decisão": as afirmações por rótulo de origem e os
// casos por faixa de confiança, por corrida, e a árvore de um caso montada dos JSON gravados (decisões, afirmações com o chip da origem, alternativas, texto do modelo).
// ! Motivo: a aba nova segue a regra do painel (um ou dois gráficos lidos do JSON); as cores dos rótulos vêm da paleta validada (--s1, --s2, --s4, --s6) e as da confiança
// são as semânticas do painel (--bom, --meio, --ruim). O explorador não copia os arquivos Markdown: monta a árvore dos dados compactados em Python.
function progErro(){
  const E = (T.progresso||{}).erro; if(!E) return;
  grafico('g-prog-erro', {type:'bar', data:{labels: E.fases, datasets: E.series.map(s => ({label: s.nome, data: s.n, backgroundColor: css(s.cor)}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{beginAtZero:true, title:{display:true, text:'segundos'}}}, plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+c.formattedValue+' s'}}}}});
}
function progGit(){
  const G = (T.progresso||{}).git; if(!G || !G.pares.length) return;
  grafico('g-git-pares', {type:'bar', data:{labels: G.pares, datasets:[{label:'cenários base a rodar (de '+G.total+')', data: G.selecionados, backgroundColor: G.cores.map(c => css(c))}]},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{beginAtZero:true, max: G.total, ticks:{stepSize:1}, title:{display:true, text:'cenários a rodar'}}}, plugins:{tooltip:{callbacks:{label: c => G.vereditos[c.dataIndex]+': '+c.formattedValue+' de '+G.total}}}}});
}
function revV3Adesao(){
  const A = (T.revisaov3||{}).adesao; if(!A) return;
  grafico('g-revv3-adesao', {type:'bar', data:{labels: A.grupos, datasets: A.series.map(s => ({label: s.nome, data: s.n, backgroundColor: css(s.cor)}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true}, y:{stacked:true, beginAtZero:true, ticks:{stepSize:5}, title:{display:true, text:'relatórios'}}}}});
}
function revV3Utilidade(){
  const U = (T.revisaov3||{}).utilidade; if(!U) return;
  grafico('g-revv3-utilidade', {type:'bar', data:{labels: U.notas.map(n => 'nota ' + n), datasets: U.series.map(s => ({label: s.nome, data: s.n, backgroundColor: css(s.cor)}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true}, y:{stacked:true, beginAtZero:true, ticks:{stepSize:5}, title:{display:true, text:'relatórios'}}}}});
}
function semNotasContexto(){
  const P = (T.semnotas||{}).previa; if(!P) return;
  grafico('g-semnotas-contexto', {type:'bar', data:{labels: P.grupos, datasets: P.series.map(s => ({label: s.nome, data: s.n, backgroundColor: css(s.cor)}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true}, y:{stacked:true, beginAtZero:true, ticks:{stepSize:6}, title:{display:true, text:'casos'}}}}});
}
function semNotasPares(){
  const L = (T.semnotas||{}).pares; if(!L) return;
  grafico('g-semnotas-pares', {type:'bar', data:{labels: L.grupos, datasets: L.series.map(s => ({label: s.nome, data: s.n, backgroundColor: css(s.cor)}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{beginAtZero:true, ticks:{stepSize:6}, title:{display:true, text:'acertos'}}}}});
}
// ! Alteração de IA - Revisar: (10/11/2026, decisão 120) os dois gráficos da aba "Segundo passe" (corrida 26): por sinal, onde está o verbete da causa certa nos casos com sinal
// (barras empilhadas) e os erros e acertos da primeira resposta com, depois da corrida, o que a segunda consertaria, estragaria e o que a regra trocou (barras lado a lado).
// ! Motivo: a aba nova segue a regra do painel (um ou dois gráficos lidos do JSON); os dois existem antes e depois da corrida, porque todo gráfico tem a sua leitura em painel_leituras.
function segPasseAlcance(){
  const A = (T.segpasse||{}).alcance; if(!A) return;
  grafico('g-segpasse-alcance', {type:'bar', data:{labels: A.grupos, datasets: A.series.map(s => ({label: s.nome, data: s.n, backgroundColor: css(s.cor)}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true}, y:{stacked:true, beginAtZero:true, ticks:{stepSize:2}, title:{display:true, text:'casos com sinal'}}}}});
}
function segPasseResultado(){
  const R = (T.segpasse||{}).resultado; if(!R) return;
  grafico('g-segpasse-resultado', {type:'bar', data:{labels: R.grupos, datasets: R.series.map(s => ({label: s.nome, data: s.n, backgroundColor: css(s.cor)}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{beginAtZero:true, ticks:{stepSize:1}, title:{display:true, text:'casos'}}}}});
}
// ! Alteração de IA - Revisar: (10/11/2026, decisão 121) os gráficos da aba "Analista de documentação": na medida M1, o que cada portão recusaria entre as edições revisadas por
// uma pessoa (barras lado a lado: erradas, parciais e corretas) e o que sobra depois de cada portão, pelo veredito da revisão humana (barras empilhadas).
// ! Motivo: a aba nova segue a regra do painel (gráficos lidos do JSON); as cores dos vereditos são as semânticas do painel (--bom, --meio, --ruim).
function analistaPortoes(){
  const P = (T.analista||{}).portoes; if(!P) return;
  grafico('g-analista-portoes', {type:'bar', data:{labels: P.grupos, datasets: P.series.map(s => ({label: s.nome, data: s.n, backgroundColor: css(s.cor)}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{beginAtZero:true, ticks:{stepSize:1}, title:{display:true, text:'edições revisadas'}}}}});
}
function analistaSequencia(){
  const S = (T.analista||{}).sequencia; if(!S) return;
  grafico('g-analista-sequencia', {type:'bar', data:{labels: S.grupos, datasets: S.series.map(s => ({label: s.nome, data: s.n, backgroundColor: css(s.cor)}))},
    options:{responsive:true, maintainAspectRatio:false, indexAxis:'y', scales:{x:{stacked:true, beginAtZero:true, ticks:{stepSize:2}, title:{display:true, text:'edições que sobram'}},
      y:{stacked:true, afterFit: s => { s.width = Math.max(s.width, 260); }}}}});
}
// ! Alteração de IA - Revisar: (11/11/2026, decisão 121) os dois gráficos da corrida 27 (medida M2) na aba "Analista de documentação": as três leituras da regra, em
// percentual do total de cada uma, na corrida 20 e, depois da corrida, na 27 (a dica mostra a contagem, "x de y"); e os casos com lacuna e sem lacuna na documentação,
// com quem o desenho chamaria e, depois da corrida, as abstenções, as propostas e as que passam nos cinco portões.
// ! Motivo: os dois existem antes e depois da corrida, porque todo gráfico da página tem a sua leitura em painel_leituras; as três leituras têm totais diferentes
// (casos, propostas com texto, edições revisadas), e só o percentual as põe no mesmo eixo.
function analistaLeituras(){
  const L = (T.analista||{}).leituras; if(!L) return;
  grafico('g-analista-leituras', {type:'bar', data:{labels: L.grupos, datasets: L.series.map(s => ({label: s.nome, data: s.n, backgroundColor: css(s.cor)}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{beginAtZero:true, max:100, title:{display:true, text:'% do total de cada leitura'}}},
      plugins:{tooltip:{callbacks:{label: c => c.dataset.label+': '+L.series[c.datasetIndex].rotulos[c.dataIndex]}}}}});
}
function analistaCasos(){
  const C = (T.analista||{}).casos; if(!C) return;
  grafico('g-analista-casos', {type:'bar', data:{labels: C.grupos, datasets: C.series.map(s => ({label: s.nome, data: s.n, backgroundColor: css(s.cor)}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{y:{beginAtZero:true, ticks:{stepSize:5}, title:{display:true, text:'casos'}}}}});
}
// aba Fluxo do agente (10/11/2026, decisão 118): a conferência depois da resposta, a posição do verbete certo, o custo do analista de documentação e as afirmações por tópico
function fluxoConferencia(){
  const C = (T.fluxo||{}).conferencia; if(!C) return;
  grafico('g-fluxo-conferencia', {type:'bar', data:{labels: C.corridas, datasets: C.series.map(s => ({label: s.nome, data: s.n, backgroundColor: css(s.cor)}))},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true, beginAtZero:true, ticks:{stepSize:2}, title:{display:true, text:'erros da corrida'}}, y:{stacked:true}}}});
}
function fluxoPosicao(){
  const P = (T.fluxo||{}).posicao; if(!P) return;
  grafico('g-fluxo-posicao', {type:'bar', data:{labels: P.faixas, datasets: P.series.map(s => ({label: s.nome, data: s.n, backgroundColor: css(s.cor)}))},
    options:{responsive:true, maintainAspectRatio:false, scales:{x:{title:{display:true, text:'posição do verbete da causa certa na lista da busca'}}, y:{beginAtZero:true, ticks:{stepSize:1}, title:{display:true, text:'erros'}}}}});
}
function fluxoCusto(){
  const C = (T.fluxo||{}).custo; if(!C) return;
  grafico('g-fluxo-custo', {type:'bar', data:{labels: C.cenarios, datasets:[{label:'segundos por chamada', data: C.segundos, backgroundColor: C.cores.map(c => css(c))}]},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}}, scales:{x:{beginAtZero:true, title:{display:true, text:'segundos por chamada do analista de documentação'}}}}});
}
function fluxoAfirmacoes(){
  const A = (T.fluxo||{}).afirmacoes; if(!A) return;
  grafico('g-fluxo-afirmacoes', {type:'bar', data:{labels: A.topicos, datasets: A.series.map(s => ({label: s.nome, data: s.n, backgroundColor: css(s.cor)}))},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true, beginAtZero:true, title:{display:true, text:'afirmações tiradas das fontes'}}, y:{stacked:true}}}});
}
function arvRotulos(){
  const R = (T.arvore||{}).rotulos; if(!R) return;
  grafico('g-arvore-rotulos', {type:'bar', data:{labels: R.corridas, datasets: R.series.map(s => ({label: s.nome, data: s.n, backgroundColor: css(s.cor)}))},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true, beginAtZero:true, title:{display:true, text:'afirmações das árvores'}}, y:{stacked:true}}}});
}
function arvConfianca(){
  const C = (T.arvore||{}).confianca; if(!C) return;
  grafico('g-arvore-confianca', {type:'bar', data:{labels: C.corridas, datasets: C.series.map(s => ({label: s.nome, data: s.n, backgroundColor: css(s.cor)}))},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, scales:{x:{stacked:true, beginAtZero:true, title:{display:true, text:'casos por faixa de confiança'}}, y:{stacked:true}}}});
}
function arvExplorar(){
  const E = (T.arvore||{}).explorador, raiz = document.querySelector('#arvore .arv-explorador');
  if(!E || !E.corridas || !E.corridas.length || !raiz || raiz.dataset.pronto) return; raiz.dataset.pronto = '1';
  const selC = raiz.querySelector('.arv-sel-corrida'), selK = raiz.querySelector('.arv-sel-caso'), alvo = raiz.querySelector('.arv-arvore');
  const el = (tag, attrs, texto) => { const e = document.createElement(tag); Object.entries(attrs || {}).forEach(([k, v]) => e.setAttribute(k, v)); if(texto != null) e.textContent = texto; return e; };
  // o texto das afirmações vem em Markdown simples: o que está entre crases vira <code>
  const comCodigo = (texto) => { const s = el('span'); String(texto || '').split('`').forEach((parte, i) => { if(!parte) return; s.append(i % 2 ? el('code', {}, parte) : document.createTextNode(parte)); }); return s; };
  const chip = (origem) => el('span', {class: 'chip origem-' + origem}, origem);
  E.corridas.forEach((c, k) => selC.append(el('option', {value: String(k)}, `${c.nome} (${c.casos.length} casos)`)));
  function casos(){
    const c = E.corridas[Number(selC.value)]; selK.replaceChildren();
    [['com divergência', x => x.resumo.divergencia], ['sem divergência', x => !x.resumo.divergencia]].forEach(([nome, f]) => { const itens = c.casos.filter(f); if(!itens.length) return;
      const g = el('optgroup', {label: `${nome} (${itens.length})`}); itens.forEach(x => g.append(el('option', {value: x.nome}, x.nome))); selK.append(g); });
  }
  function decisao(d){
    const bloco = el('div', {class: 'arv-decisao'});
    bloco.append(el('h4', {}, `Decisão ${d.numero}: ${d.titulo}`));
    let escolha = d.escolha == null ? 'nada registrado' : String(d.escolha);
    if(d.chave === 'causa') escolha = d.escolha == null ? 'nenhuma causa respondida' : '`' + d.escolha + '`' + (d.causa_em_palavras ? ' (' + d.causa_em_palavras + ')' : '') + (d.segunda ? '; segunda: `' + d.segunda + '`' : '') + (d.confianca ? '; confiança ' + d.confianca : '');
    if(d.chave === 'cura') escolha = d.escolha && d.escolha !== 'nenhuma' ? '`' + d.escolha + '`' + (d.seletor ? ' (`' + d.seletor + '`)' : '') : 'nenhum candidato aplicado';
    const p = el('p', {class: 'arv-escolha'}); p.append(el('strong', {}, 'Escolha: '), comCodigo(escolha)); bloco.append(p);
    const ul = el('ul', {class: 'arv-afirmacoes'});
    d.afirmacoes.forEach(a => { const li = el('li'); li.append(comCodigo(a[0]), chip(a[1])); ul.append(li); });
    bloco.append(ul);
    if(d.erro){ const q = el('blockquote', {class: 'arv-erro'}, d.erro); bloco.append(el('p', {class: 'nota'}, 'Mensagem do navegador, como veio:'), q); }
    if(d.alternativas && d.alternativas.length){
      const det = el('details'); det.append(el('summary', {}, `Alternativas (${d.alternativas_total})`));
      const caixa = el('div', {class: 'tabela'}), tab = el('table'), thead = el('thead'), cab = el('tr'); ['Alternativa', 'Detalhe', 'Escolhida'].forEach(h => cab.append(el('th', {}, h))); thead.append(cab);
      const corpo = el('tbody'); d.alternativas.forEach(a => { const tr = el('tr'); const c1 = el('td'); c1.append(comCodigo(a[0])); const c2 = el('td'); c2.append(comCodigo(a[1] || '')); tr.append(c1, c2, el('td', {}, a[2] ? 'sim' : '')); corpo.append(tr); });
      tab.append(thead, corpo); caixa.append(tab); det.append(caixa); bloco.append(det);
    }
    return bloco;
  }
  function mostrar(){
    const c = E.corridas[Number(selC.value)], x = c.casos.find(k => k.nome === selK.value) || c.casos[0]; if(!x) return;
    const r = x.resumo, cab = el('p', {class: 'nota'});
    cab.textContent = `Trilha ${x.trilha}: ${r.decisoes} decisões e ${r.afirmacoes} afirmações (${Object.entries(r.rotulos).filter(([, n]) => n).map(([k, n]) => `${n} ${k}`).join(', ')}); ` +
      (r.divergencia ? 'há divergência entre o declarado e o conferido' : 'nenhuma divergência entre o declarado e o conferido') + (r.cura ? '; houve cura de localizador' : '') + (r.confianca ? `; confiança ${r.confianca}` : '') + `. Arquivo: arvores/${x.arquivo}` + (x.relatorio_v3 ? `; relatório de defeito: ${x.relatorio_v3.replace('../', '')}` : '') + '.';
    const blocos = [cab, ...x.decisoes.map(decisao)];
    const tm = el('div', {class: 'arv-decisao arv-modelo'}); tm.append(el('h4', {}, 'Texto do modelo'));
    tm.append(el('p', {class: 'nota'}, 'As linhas escritas pelo modelo, como vieram e sem garantia:'));
    const bq = el('blockquote'); bq.append(el('div', {}, 'IMPACTO: ' + (x.texto_do_modelo.impacto || '(a linha não veio na resposta)')), el('div', {}, 'FONTE: ' + (x.texto_do_modelo.fonte || '(a linha não veio na resposta)'))); tm.append(bq);
    blocos.push(tm);
    alvo.replaceChildren(...blocos);
  }
  selC.addEventListener('change', () => { casos(); mostrar(); });
  selK.addEventListener('change', mostrar);
  selC.value = String(E.padrao.corrida); casos();
  if(E.padrao.caso && E.corridas[E.padrao.corrida].casos.some(k => k.nome === E.padrao.caso)) selK.value = E.padrao.caso;
  mostrar();
}
""" + pa.JS_ATLAS + pe.JS_EXPLORADOR

DESENHAR_TOPICOS = {"modelos": ["modGraficos"], "comparacao": ["cmpEtapas"], "pesquisa": ["peRodadas"], "comparativo": ["cqTrajetoria", "cqConfronto", "cqRevisao"], "tresb": ["tbGeneraliza", "tbRecuperacao"],
                    "cruzada": ["czLeitores", "czTrocas"], "colibri": ["coMinutos"], "raciocinio": ["raSustentacao", "raConfianca", "raExplorar"], "atlas": ["atlasIniciar"], "cerebro": ["ceTemas"],
                    "curadoria": ["curOperacoes"], "recuperador": ["recMetodos"], "ablacao": ["ablBarras"], "ferramental": ["ferMcp"],
                    "reproducao": ["repClasses"], "calibracao": ["calK", "calCurva"], "tela": ["telaRegra", "telaCorridas", "telaVerbete", "telaClasses", "telaRotulos"], "ineditosf4": ["inedClasse", "inedVerbete"], "posfase4": ["posFontes"], "texto": ["txtCriterios", "txtTermos"], "cura": ["curaModos", "curaRoteiros"],
                    "arvore": ["arvRotulos", "arvConfianca", "arvExplorar"],
                    "progresso": ["progErro", "progGit"],
                    "revisaov3": ["revV3Adesao", "revV3Utilidade"],
                    "semnotas": ["semNotasContexto", "semNotasPares"],
                    "fluxo": ["fluxoConferencia", "fluxoPosicao", "fluxoCusto", "fluxoAfirmacoes"],
                    "segpasse": ["segPasseAlcance", "segPasseResultado"],
                    "analista": ["analistaPortoes", "analistaSequencia", "analistaLeituras", "analistaCasos"],
                    "biblioteca": ["bibFiltros", "bibReavaliacao"], "cenarios": ["cenMttr", "cenSucesso"], "trilha": ["triSinais", "triMutacoes"], "experimento": ["expAcerto", "expTrocas"]}
SELETORES_TOPICOS = {"sel-cq-conj": "cqTrajetoria", "sel-cq-met": "cqTrajetoria", "sel-cq-conf": "cqConfronto", "sel-tb-met": "tbGeneraliza", "sel-cz-met": "czLeitores",
                     "sel-rec-bib": "recMetodos", "sel-rec-met": "recMetodos", "sel-fer-met": "ferMcp"}

CSS_TOPICOS = r"""
.chip.nao_cumprida{background:color-mix(in srgb,var(--ruim) 18%,transparent);color:var(--ruim)}
.leitura{padding-left:22px;max-width:90ch}.leitura li{margin:6px 0}.fontes{max-width:none}
main > section{scroll-margin-top:120px}.kpi b.longo{font-size:20px}
.dc{white-space:nowrap}.delta{display:inline-block;font:600 11px var(--fm);padding:0 5px;border-radius:4px;margin-left:4px;background:var(--bg2);color:var(--ink)}
.delta.zero{color:var(--ink2)}
.duelo td:first-child,.heat td:first-child{white-space:nowrap}
.barra{display:flex;height:10px;width:100%;min-width:120px;background:color-mix(in srgb,var(--ink2) 15%,transparent);border-radius:5px;overflow:hidden}
.barra .ap{background:var(--bom);height:100%}.barra .rej{background:var(--ruim);height:100%}
.mapa-painel{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));gap:12px;margin:14px 0}
.mapa-painel div{background:var(--bg2);border:1px solid var(--linha);border-radius:10px;padding:12px 14px}
.mapa-painel h3{margin:0 0 6px;font-size:13px;text-transform:uppercase;letter-spacing:.05em;color:var(--ink2);font-family:var(--fb)}
.mapa-painel ul{list-style:none;padding:0;margin:0}.mapa-painel li{margin:6px 0;font-size:13px}.mapa-painel a{color:var(--acento);font-weight:600;text-decoration:none}.mapa-painel a:hover{text-decoration:underline}
.toks{display:flex;flex-wrap:wrap;gap:4px;margin:12px 0}
.tok{display:inline-flex;flex-direction:column;align-items:center;gap:2px;padding:4px 7px;border-radius:6px;border:1px solid var(--linha);background:color-mix(in srgb,var(--s1) var(--p,0%),transparent)}
.tok code{background:none;padding:0;font:500 13px var(--fm);color:var(--ink)}.tok small{font:400 10px var(--fb);color:var(--ink2)}
.tabela.estreita{max-width:420px}
pre.bruto{margin:8px 0;background:var(--acento2);border-radius:6px;padding:10px 12px;font:12px/1.5 var(--fm);white-space:pre-wrap;overflow-wrap:anywhere;max-width:100%}
pre.bruto code{background:none;padding:0;font:inherit}
.relatorio{border-left:3px solid var(--linha);padding:2px 0 8px 16px;margin:8px 0}.relatorio h3{margin-top:10px}.relatorio h5{font:600 13px var(--fb);margin:14px 0 6px}
.chip.adotado{background:color-mix(in srgb,var(--bom) 18%,transparent);color:var(--bom)}.chip.adiado{background:color-mix(in srgb,var(--meio) 18%,transparent);color:var(--meio)}.chip.descartado{background:color-mix(in srgb,var(--ruim) 16%,transparent);color:var(--ruim)}
.chip.origem-observado{background:color-mix(in srgb,var(--s1) 18%,transparent);color:var(--s1)}.chip.origem-conferido{background:color-mix(in srgb,var(--s2) 18%,transparent);color:var(--s2)}
.chip.origem-declarado{background:color-mix(in srgb,var(--s4) 18%,transparent);color:var(--s4)}.chip.origem-desconhecido{background:color-mix(in srgb,var(--s6) 18%,transparent);color:var(--s6)}
.arv-controles{display:flex;flex-wrap:wrap;gap:10px 18px;font-size:13px;color:var(--ink2);margin:10px 0}.arv-controles select{max-width:100%;margin-left:4px}
.arv-arvore{display:grid;gap:14px;align-items:start}
.arv-decisao{background:var(--bg2);border:1px solid var(--linha);border-radius:10px;padding:14px 16px;min-width:0}.arv-decisao h4{margin:0 0 6px}
.arv-escolha{margin:4px 0 8px;font-size:13px}.arv-afirmacoes{list-style:none;padding:0;margin:6px 0;font-size:13px}.arv-afirmacoes li{margin:7px 0;display:flex;flex-wrap:wrap;gap:3px 8px;align-items:baseline}
.arv-afirmacoes code,.arv-escolha code,.arv-decisao td code{overflow-wrap:anywhere}.arv-decisao details{margin:8px 0 0}.arv-decisao table{font-size:12px}.arv-decisao td,.arv-decisao th{padding:4px 7px}
.arv-decisao blockquote{margin:6px 0;padding:6px 12px;border-left:3px solid var(--linha);font:12px/1.5 var(--fm);white-space:pre-wrap;overflow-wrap:anywhere}
""" + pa.CSS_ATLAS + pe.CSS_EXPLORADOR


# ! Alteração de IA - Revisar: (01/10/2026) bloco da aba Atlas com a validação do texto do Gemini, lido da subseção
# "3.1" do relatório da Pré-Fase 4: uma linha por afirmação, com o veredito em destaque (certo, com ressalva, errado).
# ! Motivo: o Eric pediu que a descrição que o Gemini deu das imagens fosse validada; a resposta, com a fonte de cada
# veredito, está no relatório, e é pelo painel que ele lê. O texto não é copiado para o código: vem do arquivo.
RELATORIO_PRE_FASE4 = MEMORIAL / "3-resultados-e-analises" / "pre-fase-4-relatorio.md"


def validacao_do_gemini() -> str:
    if not RELATORIO_PRE_FASE4.exists():
        return ""
    md = pt.sem_comentarios(RELATORIO_PRE_FASE4.read_text(encoding="utf-8").replace("\r\n", "\n"))
    ini = md.find("### 3.1 ")
    if ini < 0:
        return ""
    fim = md.find("\n### ", ini + 4)
    trecho = md[ini:fim if fim > 0 else len(md)]
    cab, linhas, resto = pt.primeira_tabela(trecho.split("\n", 1)[1])
    if not linhas:
        return ""

    def classe(veredito: str) -> tuple[str, str]:
        v = veredito.strip().lower()
        if v.startswith("errado"):
            return "errado", "descartado"
        return ("certo", "adotado") if v == "correto" else ("ressalva", "adiado")

    trs = []
    for k, r in enumerate(linhas, 1):
        nome, cor = classe(r[1])
        trs.append(f'<tr data-afirmacao="{k}" data-veredito="{nome}"><td>{pt.inline(r[0])}</td><td>{chip(cor, r[1])}</td><td>{pt.inline(r[2])}</td>'
                   f'<td class="nota">{pt.inline(r[3])}</td></tr>')
    paragrafos = [p.strip() for p in resto.split("\n\n") if p.strip()]
    antes = pt.inline(paragrafos[0]) if paragrafos else ""
    depois = "".join(f"<p>{pt.inline(p)}</p>" for p in paragrafos[1:])
    cont = Counter(classe(r[1])[0] for r in linhas)
    resumo = (f"A descrição do Gemini estava certa? Das {len(linhas)} afirmações conferidas, {cont['certo']} estão certas, "
              f"{cont['ressalva']} valem em parte ou com ressalva e {cont['errado']} estão erradas")
    return (f'<details class="at-gemini"><summary>{esc(resumo)}</summary>\n<p>{antes}</p>\n'
            f'<div class="tabela"><table><thead><tr>{"".join(f"<th>{esc(c)}</th>" for c in cab)}</tr></thead><tbody>{"".join(trs)}</tbody></table></div>\n{depois}</details>')


# ------------------------------------------------------------------ montagem

# ! Alteração de IA - Revisar: aba nova (27/10/2026) "Reprodução na tela", a primeira da Fase 4: a corrida 17 sobre os
# 72 casos de avaliação e a mesma corrida sobre os 36 inéditos da ficha 27, lidas de
# resultados_alvo/fase4/reproducibilidade.json e reproducibilidade_ineditos.json (avaliar_fase4.py, com --check).
# ! Motivo: a regra do painel é uma aba por análise e a corrida 17 (pacote P2) tinha ficado só no roadmap; o Eric
# decide pelo painel quais casos a tela reproduz antes de gastar modelo (corridas 16 e 18) e de conferir os inéditos.
# Sem os arquivos a aba mostra o estado vazio, como as da Pré-Fase 4.
def secao_reproducao(rep: dict | None, ined: dict | None, road: dict, cartoes_corridas) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões de tempo e de corte da árvore encurtados, e "harness" e "poda" soltos trocados por "o próprio teste" e "o corte em código do que o modelo lê (poda)".
    # ! Motivo: os cartões traziam milissegundos da API e tamanhos do corpo que já estão nas tabelas recolhidas, e o texto usava termos de método que o Eric pediu para tirar.
    def por(d: dict | None, chave: str, campo: str) -> dict:
        return {x[campo]: x for x in d[chave]} if d else {}

    pc, pi = por(rep, "por_classe", "classe"), por(ined, "por_classe", "classe")
    campos = ("casos", "na_tela", "reproduzem", "fora")
    classes = [{"classe": i, "nome": nome,
                "avaliacao": {k: pc[i][k] for k in campos} if i in pc else None,
                "ineditos": {k: pi[i][k] for k in campos} if i in pi else None} for i, nome in CLASSES.items()]
    rotulos = {"avaliacao": f'{rep["resumo"]["casos"]} de avaliação' if rep else "casos de avaliação",
               "ineditos": f'{ined["resumo"]["casos"]} inéditos' if ined else "inéditos"}
    dados_js = {"classes": classes, "rotulos": rotulos}
    fontes_ = fontes(["<code>resultados_alvo/fase4/reproducibilidade.json</code> e <code>.md</code> (<code>avaliar_fase4.py --reproducao</code>, com <code>--check</code>; blocos <code>tb_f4_reproducao_*</code>)",
                      "<code>resultados_alvo/fase4/reproducibilidade_ineditos.json</code> e <code>.md</code> (a mesma avaliação com <code>--nome reproducibilidade_ineditos</code>)",
                      "<code>executar_fase4.py --modo reproducao</code> (regra R1; <code>--banco</code> escolhe os casos); roadmap §2.8; plano aprovado da Fase 4, seções 5 e 6; fichas 27, 28 e 29"])
    if not rep:
        html_ = f'''<section id="reproducao" hidden>
<h1>Reprodução na tela: quantos casos de avaliação a tela consegue reproduzir?</h1>
<p class="lead">A corrida 17 ainda não foi rodada nesta máquina: falta <code>resultados_alvo/fase4/reproducibilidade.json</code>, gerado por <code>avaliar_fase4.py --reproducao</code> depois de <code>executar_fase4.py --modo reproducao --saida fase4_reproducao</code>.</p>
{cartoes_corridas(road, numeros=["17"], sufixo="-rep")}
{fontes_}
</section>'''
        return dados_js, html_
    r = rep["resumo"]
    ri = ined["resumo"] if ined else None
    t, tam = rep["tempo"], rep["tamanhos"]
    fora_motivos = "; ".join(f'{x["casos"]} {x["motivo"]}' for x in rep["fora_por_motivo"]).replace("pelo harness", "pelo próprio teste")
    itens_kpi = [
        ("Reproduzem na tela (corrida 17)", f'{r["reproduzem"]} de {r["casos"]}',
         f'{fmt(r["reproduzem_pct"])}% do conjunto; {fmt(r["reproduzem_dos_na_tela_pct"])}% dos {r["na_tela"]} com tela e modo'),
        ("Ficam fora", str(r["fora"]), fora_motivos),
        ("Tempo por cenário", f'{fmt(t["mediana_s"], 3)} s', f'mediana; o maior, {fmt(t["max_s"])} s, vem de casos de latência'),
        ("Corte da árvore da tela (poda)", f'{tam["arvore_antes_mediana"]} para {tam["arvore_depois_mediana"]}',
         f'nós antes e linhas depois, em medianas; o caso ao vivo fica com {tam["caso_chars_mediana"]} caracteres'),
        (("Inéditos da ficha 27", f'{ri["reproduzem"]} de {ri["casos"]}', f'{fmt(ri["reproduzem_pct"])}% dos {ri["casos"]}; {ri["fora"]} fora; corrida de {"/".join(reversed(ined["metadados"]["gerado_em"][:10].split("-")))}')
         if ri else ("Inéditos da ficha 27", "ainda não rodada", "a mesma corrida sobre os 36 inéditos")),
    ]

    def linha(rotulo: str, a: dict | None, i: dict | None) -> list:
        vazio = ("—", "—", "—", "—")
        return [rotulo, *((a["casos"], a["na_tela"], a["reproduzem"], a["fora"]) if a else vazio),
                *((i["casos"], i["na_tela"], i["reproduzem"], i["fora"]) if i else vazio)]

    cab_duplo = ["Classe", "Casos", "Com tela e modo", "Reproduzem", "Fora", "Inéditos: casos", "Com tela e modo", "Reproduzem", "Fora"]
    por_classe = tabela(cab_duplo, [linha(f'{c["classe"]} {c["nome"]}', c["avaliacao"], c["ineditos"]) for c in classes])
    pn, pni = por(rep, "por_nivel", "nivel"), por(ined, "por_nivel", "nivel")
    por_nivel = tabela([h.replace("Classe", "Nível") for h in cab_duplo], [linha(str(n), pn[n], pni.get(n)) for n in sorted(pn)])
    pm, pmi = por(rep, "por_modo", "modo"), por(ined, "por_modo", "modo")
    modos = sorted(set(pm) | set(pmi))
    por_modo = tabela(["Modo de injeção", "Casos", "Reproduzem", "Inéditos: casos", "Reproduzem", "Motivos registrados"],
                      [[f"<code>{esc(m)}</code>", pm.get(m, {}).get("casos", "—"), pm.get(m, {}).get("reproduzem", "—"),
                        pmi.get(m, {}).get("casos", "—"), pmi.get(m, {}).get("reproduzem", "—"),
                        esc("; ".join(dict.fromkeys(list(pm.get(m, {}).get("motivos", [])) + list(pmi.get(m, {}).get("motivos", [])))))] for m in modos], raw=True)

    def linhas_casos(d: dict | None, rotulo: str) -> list[list]:
        return [[esc(rotulo), f"<code>{esc(c['id'])}</code>", c["classe"], c["nivel"], f"<code>{esc(c['causa'])}</code>", f"<code>{esc(c['modo'])}</code>",
                 esc(c["cenario"]), "sim" if c["reproduz"] else "não", esc(c["motivo"]), fmt(c.get("segundos"), 3)] for c in (d["casos"] if d else [])]

    casos = tabela(["Corrida", "Caso", "Classe", "Nível", "Causa", "Modo", "Cenário", "Reproduz", "Motivo", "Segundos"],
                   linhas_casos(rep, rotulos["avaliacao"]) + linhas_casos(ined, rotulos["ineditos"]), raw=True)
    fora = tabela(["Corrida", "Caso", "Classe", "Nível", "Causa", "Por que ficou fora"],
                  [[esc(rot), f"<code>{esc(x['id'])}</code>", x["classe"], x["nivel"], f"<code>{esc(x['causa'])}</code>", esc(x["motivo"])]
                   for d, rot in ((rep, rotulos["avaliacao"]), (ined, rotulos["ineditos"])) if d for x in d["fora"]], raw=True)
    n_casos = len(rep["casos"]) + (len(ined["casos"]) if ined else 0)
    n_fora = r["fora"] + (ri["fora"] if ri else 0)
    lead = (f'Todos os que têm um modo de injeção e uma rota com página: {r["reproduzem"]} dos {r["casos"]} casos de avaliação na corrida 17 '
            f'({fmt(r["reproduzem_pct"])}% do conjunto, {fmt(r["reproduzem_dos_na_tela_pct"])}% dos {r["na_tela"]} com tela e modo) e, na mesma corrida sobre os inéditos da ficha 27, '
            + (f'{ri["reproduzem"]} dos {ri["casos"]} ({fmt(ri["reproduzem_pct"])}%). ' if ri else 'os 36 inéditos ainda não foram medidos. ')
            + f'Ficam fora {r["fora"]} dos {r["casos"]}: {fora_motivos}. Sem modelo: a regra R1 compara a chamada à API, o corpo e a árvore de acessibilidade '
              'com a corrida de referência em modo normal e confere o roteiro.')
    leitura_ = leitura([
        f"<strong>Quem tem tela e modo reproduz.</strong> Na corrida 17, {r['na_tela']} casos tinham os dois e {r['reproduzem']} reproduziram (bloco <code>tb_f4_reproducao_resumo</code>); "
        f"{r['roteiro_falhou']} deles também derrubaram uma conferência do roteiro.",
        f"<strong>O que fica fora não é falha da tela.</strong> {esc(fora_motivos)}: as rotas de pedido não têm página, <code>dado_desatualizado</code> não tem modo de injeção "
        "e as causas de efeito (localizador quebrado e estado da tela) são armadas pelo próprio teste no navegador, pela ficha 29.",
        (f"<strong>Os inéditos nasceram com os modos novos da ficha 28.</strong> {ri['na_tela']} dos {ri['casos']} têm tela e modo e "
         + ("todos reproduzem" if ri["reproduzem"] == ri["na_tela"] else f"{ri['reproduzem']} reproduzem")
         + f"; os {ri['fora']} fora são da mesma natureza. Eles esperam a conferência do Eric antes da corrida 16.") if ri
        else "<strong>Os 36 inéditos da ficha 27 ainda não passaram por esta corrida.</strong>",
        f"<strong>Custo.</strong> Mediana de {fmt(t['mediana_s'], 3)} s por cenário; os de latência chegam a {fmt(t['max_s'])} s porque o modo dorme por item da lista. "
        f"O corte em código do que o modelo lê (poda) leva a árvore de {tam['arvore_antes_mediana']} nós a {tam['arvore_depois_mediana']} linhas.",
    ])
    html_ = f'''<section id="reproducao" hidden>
<h1>Reprodução na tela: quantos casos de avaliação a tela consegue reproduzir?</h1>
<p class="lead">{lead}</p>
{kpis(itens_kpi)}
<h2>Por classe de defeito</h2>
<p>Quantos casos de cada classe têm tela e modo e quantos reproduzem, nos {esc(rotulos["avaliacao"])} e nos {esc(rotulos["ineditos"])}. A classe de efeito fica fora por desenho: a quebra de localizador é armada pelo próprio teste, não pela API.</p>
<div class="chart"><canvas id="g-rep-classe"></canvas></div>
{por_classe}
<h2>Por nível e por modo de injeção</h2>
{por_nivel}
{detalhes(f"Por modo de injeção ({len(modos)} modos)", por_modo)}
{detalhes(f"Todos os casos com tela e modo ({n_casos})", casos)}
{detalhes(f"Casos fora ({n_fora})", fora)}
<h2>A corrida no roadmap</h2>
{cartoes_corridas(road, numeros=["17"], sufixo="-rep")}
{leitura_}
{fontes_}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ 19. Fase 4: calibração e ponte (corrida 16)

# ! Alteração de IA - Revisar: aba nova (27/10/2026, Fase 4, pacote P3) com a leitura da corrida 16 (calibração e ponte),
# lida de resultados_alvo/fase4/calibracao.json e limiares.json (avaliar_fase4.py --calibracao): o k que a regra R8
# escolheu, os limiares do selo (regra R7, ficha 31), a AUROC da probabilidade do rótulo nos 90 casos com intervalo, a
# revisão humana por parcela, a curva risco-cobertura, a ponte de versão (regra R6) e a sondagem dos logprobs; sem o
# arquivo, o estado vazio com o cartão da corrida, como as outras abas.
# ! Motivo: a regra do painel é uma aba por análise, lida dos JSON; a corrida 16 fixa o k e os limiares que a corrida 18
# usa, e o Eric decide pelo painel.
def secao_calibracao(cal: dict | None, lim: dict | None, road: dict, cartoes_corridas) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões, títulos e itens de leitura à vista reescritos sem AUROC, IC, b/c, "acurácia balanceada", "gatilho" nem "rótulo" soltos.
    # ! Motivo: o texto à vista trazia siglas e números soltos que o Eric pediu para tirar; "k" passa a vir com o nome (número de verbetes entregues) e os valores seguem nas tabelas recolhidas.
    fontes_ = fontes(["<code>resultados_alvo/fase4/calibracao.json</code> e <code>.md</code> (<code>avaliar_fase4.py --calibracao</code>, com <code>--check</code>; blocos <code>tb_f4_calibracao_*</code>)",
                      "<code>resultados_alvo/fase4/limiares.json</code> (regra R7, ficha 31) e <code>pontes.json</code> (regra R6, decisão 47)",
                      "<code>executar_fase4.py --modo calibracao</code> (sondagem, ponte, L1 curada nos 90 com cada k, pelo executor congelado da Fase 3); roadmap §2.9; plano aprovado da Fase 4, seções 5, 6 e 8; fichas 30 e 31"])
    vazio = {"por_k": [], "curva": [], "k_escolhido": None, "limiares": None, "por_selo": []}
    if not cal:
        html_ = f'''<section id="calibracao" hidden>
<h1>Calibração: quantos verbetes entregar ao modelo e onde ficam os cortes do selo?</h1>
<p class="lead">A corrida 16 ainda não foi rodada nesta máquina: falta <code>resultados_alvo/fase4/calibracao.json</code>, gerado por <code>avaliar_fase4.py --calibracao</code> depois de <code>executar_fase4.py --modo calibracao --saida fase4_calibracao --k 3,5</code> (noite A do plano aprovado).</p>
{cartoes_corridas(road, numeros=["16"], sufixo="-cal")}
{fontes_}
</section>'''
        return vazio, html_
    por_k = cal["por_k"]
    r8 = cal["r8"]
    limi = cal.get("limiares") or {}
    ponte = cal.get("ponte") or {}
    son = cal.get("sondagem") or {}
    escolhido = next((x for x in por_k if x["k"] == cal["k_escolhido"]), por_k[0])

    def auroc(x: dict, sinal: str) -> dict:
        return (x.get("sinais") or {}).get(sinal) or {}

    def auroc_txt(s: dict) -> str:
        if s.get("auroc") is None:
            return "n/d"
        ic = s.get("ic95")
        return fmt(s["auroc"], 3) + (f" [{fmt(ic[0], 3)}; {fmt(ic[1], 3)}]" if ic else "")

    dados_js = {"por_k": [{"k": x["k"], "n": x["n"], "acertos": x["acertos"], "acerto_pct": x["acerto_pct"], "acuracia_balanceada_pct": x["acuracia_balanceada_pct"],
                           "auroc_p": auroc(x, "p_rotulo").get("auroc"), "auroc_conjunta": auroc(x, "p_conjunta").get("auroc")} for x in por_k],
                "curva": [{"cobertura": p["cobertura"], "risco": p["risco"]} for p in escolhido.get("curva", [])],
                "k_escolhido": cal["k_escolhido"], "limiares": {"baixo_ate": limi.get("baixo_ate"), "alto_a_partir_de": limi.get("alto_a_partir_de")},
                "por_selo": cal.get("por_selo") or []}
    a_p = auroc(escolhido, "p_rotulo")
    # ! Alteração de IA - Revisar: (28/10/2026, leitura da corrida 16) a aba mostra os casos e os erros por selo (bloco
    # `tb_f4_calibracao_selos` de calibracao.json): cartão "Erros com selo alto", tabela e item da leitura.
    # ! Motivo: o selo alto é o que o agente mostra como confiável; quantos erros saem com ele é o número que a leitura
    # da corrida 16 precisa citar, e ele só existe no JSON desde a mesma data (antes só a parcela baixa era contada).
    por_selo = cal.get("por_selo") or []
    alto = next((x for x in por_selo if x["selo"] == "alto"), None)

    def erros_txt(x: dict) -> str:
        return f'{x["errados"]} {"erro" if x["errados"] == 1 else "erros"} em {x["casos"]} casos ({fmt(x["erro_pct"])}%)'
    parcela = limi.get("parcela_baixa")
    itens_kpi = [("Número de verbetes entregues (k) escolhido, regra R8", f'k = {cal["k_escolhido"]}', esc(r8["motivo"]))]
    for x in por_k:
        itens_kpi.append((f"Acerto com {x['k']} verbetes entregues", f'{x["acertos"]} de {x["n"]}',
                          f'{fmt(x["acerto_pct"])}%; {fmt(x["segundos_mediana"])} s por diagnóstico'
                          + ("" if x.get("completo", True) else "; corrida incompleta")))
    itens_kpi += [
        ("Selo baixo até", fmt(limi.get("baixo_ate"), 3),
         (f'os {fmt(100 * parcela, 0)}% menos prováveis: {limi.get("erros_pegos")} dos {limi.get("erros")} erros e {limi.get("acertos_revisados")} acertos revisados'
          if parcela is not None else "sem limiares")),
        ("Selo alto a partir de", fmt(limi.get("alto_a_partir_de"), 3), "mediana da probabilidade nos acertos (ficha 31, opção a); médio fica entre os dois"),
        ("O quanto a probabilidade separa erros de acertos", fmt(a_p.get("auroc"), 3) if a_p.get("auroc") is not None else "n/d",
         f'{a_p.get("n", escolhido["n"])} casos; pela probabilidade conjunta, {fmt(auroc(escolhido, "p_conjunta").get("auroc"), 3)}'),
        ("Ponte de versão (regra R6)", f'Ollama {ponte.get("versao", "n/d")}',
         (f'{"pareável" if ponte.get("pareavel") else "não pareável"} com a Fase 3: só a ponte acertou {ponte.get("b")}, só a Fase 3 {ponte.get("c")}, em {ponte.get("n")} casos; '
          + ("feita nesta corrida" if ponte.get("feita_nesta_corrida") else "já registrada")) if ponte else "sem ponte registrada"),
        ("Sondagem das probabilidades por token (logprobs)", ("ok" if son.get("ok") else "problema") if son else "não rodou",
         (f'até {son.get("top_por_posicao_max")} alternativas por posição; ' + ("com avisos (ver a tabela)" if son.get("mensagens") else "sem avisos")) if son else ""),
    ]
    if alto:
        itens_kpi.insert(4, ("Erros com selo alto", f'{alto["errados"]} de {alto["casos"]}',
                             f'{fmt(alto["erro_pct"])}% dos casos com selo alto saem errados (os nomes estão na tabela)'))
    tab_selos = tabela(["Selo", "Casos", "Certos", "Errados", "Erro (%)", "Casos errados"],
                       [[esc(x["selo"]), x["casos"], x["certos"], x["errados"], fmt(x["erro_pct"]), ", ".join(f"<code>{esc(c)}</code>" for c in x["casos_errados"]) or "nenhum"]
                        for x in por_selo], raw=True) if por_selo else ""
    bloco_selos = f"<p>Casos e erros por selo com os limiares desta corrida (regra R7; bloco <code>tb_f4_calibracao_selos</code>).</p>\n{tab_selos}" if por_selo else ""
    tab_k = tabela(["k", "Casos", "Completo", "Acertos", "Acerto (%)", "Acurácia balanceada (%)", "Nos 36 de avaliação (%)", "Nos 54 de aprendizado (%)",
                    "s por diagnóstico (mediana)", "Tokens de entrada (mediana)", "AUROC p do rótulo [IC 95%]", "AUROC p conjunta [IC 95%]", "Sem rótulo"],
                   [[f'k = {x["k"]}', x["n"], "sim" if x.get("completo", True) else "não", x["acertos"], fmt(x["acerto_pct"]), fmt(x["acuracia_balanceada_pct"]),
                     fmt(((x.get("por_particao") or {}).get("avaliacao") or {}).get("acerto_pct")), fmt(((x.get("por_particao") or {}).get("aprendizado") or {}).get("acerto_pct")),
                     fmt(x["segundos_mediana"]), fmt(x["tokens_entrada_mediana"], 0), auroc_txt(auroc(x, "p_rotulo")), auroc_txt(auroc(x, "p_conjunta")), x["sem_rotulo"]] for x in por_k])
    tab_rev = tabela(["k", "Parcela revisada", "Casos revisados", "Erros pegos", "Acertos revisados à toa", "Risco no que sobra"],
                     [[f'k = {x["k"]}', f'{fmt(100 * rv["fracao"], 0)}%', rv["revisados"], f'{rv["erros_pegos"]} de {rv["erros"]}', rv["acertos_revisados"],
                       "n/d" if rv["risco_no_que_sobra"] is None else f'{fmt(100 * rv["risco_no_que_sobra"])}%'] for x in por_k for rv in x.get("revisao", [])])
    par = r8.get("par") or {}
    tab_r8 = tabela(["Acurácia balanceada k = 3 (%)", "Acurácia balanceada k = 5 (%)", "b (só k = 5 acerta)", "c (só k = 3 acerta)", "p (McNemar exato)", "k escolhido", "Motivo"],
                    [[fmt(next((x["acuracia_balanceada_pct"] for x in por_k if x["k"] == 3), None)), fmt(next((x["acuracia_balanceada_pct"] for x in por_k if x["k"] == 5), None)),
                      par.get("b", "—"), par.get("c", "—"), fmt(par.get("p_mcnemar"), 3), f'k = {r8["k"]}', r8["motivo"]]])
    tab_ponte = tabela(["Ollama", "Corrida da ponte", "Feita nesta corrida", "Casos pareados", "b", "c", "Pareável (limite)", "Casos de texto corrigido fora"],
                       [[ponte.get("versao", "n/d"), ponte.get("corrida", "n/d"), "sim" if ponte.get("feita_nesta_corrida") else "não", ponte.get("n", "—"), ponte.get("b", "—"), ponte.get("c", "—"),
                         f'{"sim" if ponte.get("pareavel") else "não"} ({ponte.get("limite")})' if ponte else "n/d", ", ".join(ponte.get("casos_de_texto_alterado") or []) or "nenhum"]])
    tab_son = tabela(["Ollama", "Tokens com probabilidade", "Alternativas por posição (máx.)", "Bytes por token", "Texto remontado bate", "Probabilidade antes ou depois da temperatura",
                      "Resposta igual sem logprobs", "Rótulo lido", "p do rótulo", "Avisos"],
                     [[son.get("versao_ollama", "n/d"), son.get("tokens_com_logprob", "—"), son.get("top_por_posicao_max", "—"), "sim" if son.get("tem_bytes") else "não",
                       "sim" if son.get("texto_bate") else "não", son.get("temperatura", "n/d"), "sim" if son.get("resposta_igual_sem_logprobs") else "não",
                       son.get("rotulo_lido", "n/d"), fmt(son.get("p_rotulo"), 3), "; ".join(son.get("mensagens") or []) or "nenhum"]] if son else [["não rodou"] + ["—"] * 9])
    casos = tabela(["Caso", "Partição", "Gabarito", "Rótulo", "Resultado", "p do rótulo", "p conjunta", "Segunda causa", "Selo"],
                   [[f"<code>{esc(l['caso'])}</code>", esc(l.get("particao") or "—"), f"<code>{esc(l['gabarito'])}</code>", f"<code>{esc(l['rotulo'])}</code>",
                     "certo" if l["acerto"] else "errado", fmt(l["p"], 3), fmt(l["p_conjunta"], 3), esc(l.get("segunda") or "—"),
                     esc(("baixo" if l["p"] is not None and limi.get("baixo_ate") is not None and l["p"] <= limi["baixo_ate"]
                          else "alto" if l["p"] is not None and limi.get("alto_a_partir_de") is not None and l["p"] >= limi["alto_a_partir_de"]
                          else "médio" if l["p"] is not None else "—"))]
                    for l in sorted(escolhido.get("casos", []), key=lambda l: (l["p"] is None, l["p"] or 0, l["caso"]))], raw=True)
    lead = (f'A regra R8 escolheu k = {cal["k_escolhido"]}: {esc(r8["motivo"])}. Com esse k, o selo baixo vai até a probabilidade {fmt(limi.get("baixo_ate"), 3)} '
            f'(os {fmt(100 * parcela, 0) if parcela is not None else "—"}% de menor probabilidade, que pegam {limi.get("erros_pegos")} de {limi.get("erros")} erros) e o selo alto começa em '
            f'{fmt(limi.get("alto_a_partir_de"), 3)}; a probabilidade do rótulo separa acerto de erro com AUROC {fmt(a_p.get("auroc"), 3)} nos {escolhido["n"]} casos. '
            + (f'A ponte de versão (Ollama {ponte.get("versao")}) {"é pareável" if ponte.get("pareavel") else "não é pareável"} com a Fase 3 (b = {ponte.get("b")}, c = {ponte.get("c")}). ' if ponte else "")
            + (f'Sondagem dos logprobs: {"ok" if son.get("ok") else "com problema"}.' if son else ""))
    leitura_ = leitura([
        f"<strong>O número de verbetes entregues (k) da Fase 4.</strong> {esc(r8['motivo'])} (bloco <code>tb_f4_calibracao_r8</code>); a corrida 18 lê o k de <code>limiares.json</code>.",
        f"<strong>Os limiares do selo.</strong> Ficha 31 (a): baixo é a parcela de {fmt(100 * parcela, 0) if parcela is not None else '—'}% de menor probabilidade (o aviso que dispara a checagem extra e a revisão humana), "
        f"alto fica acima da mediana dos acertos. Revisar {limi.get('revisados')} casos pega {limi.get('erros_pegos')} de {limi.get('erros')} erros e deixa "
        f"{fmt(100 * limi['risco_no_que_sobra']) if limi.get('risco_no_que_sobra') is not None else '—'}% de erro no que sobra (<code>tb_f4_calibracao_revisao</code>).",
        f"<strong>A probabilidade é triagem, não barreira.</strong> O quanto o sinal separa erros de acertos é {fmt(a_p.get('auroc'), 3)} pelo primeiro token da causa e {fmt(auroc(escolhido, 'p_conjunta').get('auroc'), 3)} pela probabilidade conjunta, com k = {escolhido['k']} "
        "(blocos <code>tb_f4_calibracao_resumo</code> e <code>tb_f4_calibracao_por_k</code>): parte dos erros sai confiante, então o selo alto não dispensa a conferência (especificação da trilha, seção 6.3).",
        *([f"<strong>Erros por selo.</strong> " + "; ".join(f"selo {esc(x['selo'])}: {erros_txt(x)}" for x in por_selo) + " (<code>tb_f4_calibracao_selos</code>)."] if por_selo else []),
        (f"<strong>Ponte de versão.</strong> Ollama {ponte.get('versao')}: só a ponte acertou {ponte.get('b')} casos e só a Fase 3 {ponte.get('c')}, {'dentro' if ponte.get('pareavel') else 'fora'} do limite da decisão 47"
         + (" (feita nesta corrida)." if ponte.get("feita_nesta_corrida") else f" ({esc(str(ponte.get('corrida')))}).")) if ponte else "<strong>Ponte de versão.</strong> Não registrada.",
        f"<strong>Custo.</strong> " + "; ".join(f"k = {x['k']}: {fmt(x['segundos_mediana'])} s por diagnóstico, {fmt(x['tokens_entrada_mediana'], 0)} tokens de entrada na mediana" for x in por_k) + ".",
    ])
    html_ = f'''<section id="calibracao" hidden>
<h1>Calibração: quantos verbetes entregar ao modelo e onde ficam os cortes do selo?</h1>
<p class="lead">{lead}</p>
{kpis(itens_kpi)}
<h2>Acerto e separação de erros e acertos, por número de verbetes entregues (k)</h2>
<p>A cópia curada da primeira versão escrita pelo modelo (L1 curada) nos 90 casos oficiais com cada k, pelo mesmo executor e o mesmo prompt da Fase 3. A probabilidade da causa respondida é lida no primeiro token depois de CAUSA_RAIZ.</p>
<div class="chart baixo"><canvas id="g-cal-k"></canvas></div>
{tab_k}
<h2>Quanto se erra ao responder só os mais prováveis, com {escolhido["k"]} verbetes entregues</h2>
<p>Respondendo só os casos de maior probabilidade: a cobertura (quantos são respondidos) e o risco (erros entre eles). É dela que saem os limiares.</p>
<div class="chart baixo"><canvas id="g-cal-curva"></canvas></div>
{tab_rev}
{bloco_selos}
<h2>Qual número de verbetes ficou, a ponte de versão e a sondagem das probabilidades</h2>
{tab_r8}
{detalhes("Ponte de versão (regra R6)", tab_ponte)}
{detalhes("Sondagem dos logprobs no Ollama instalado", tab_son)}
{detalhes(f"Caso a caso com k = {escolhido['k']} ({len(escolhido.get('casos', []))} casos, da menor probabilidade para a maior)", casos)}
<h2>A corrida no roadmap</h2>
{cartoes_corridas(road, numeros=["16"], sufixo="-cal")}
{leitura_}
{fontes_}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ 20. Fase 4: tela e fixture (corrida 18)

# ! Alteração de IA - Revisar: aba nova (01/11/2026, Fase 4) com a leitura da corrida 18 (o mesmo caso lido da tela e do
# fixture, na mesma sessão do Ollama), lida de resultados_alvo/fase4/tela.json (avaliar_fase4.py --tela): a regra R2
# (mesmo rótulo nos dois lados, b e c, McNemar), o acerto de cada lado por classe, os selos e gatilhos na tela, os rótulos
# dados em cada lado contra o gabarito, o prompt da tela contra o maior da calibração e o caso a caso; sem o arquivo, o
# estado vazio com o cartão da corrida, como as outras abas.
# ! Motivo: a regra do painel é uma aba por análise, lida dos JSON; a corrida 18 decide se o molde do sintoma e a poda
# voltam para revisão antes da noite C (regra R2), e o Eric decide pelo painel.
# ! Alteração de IA - Revisar: (05/11/2026, decisão 90) secao_tela recebe também a leitura da 18c (tela_v3.json): com ela, os cartões, o primeiro parágrafo e os gráficos passam à corrida vigente, e a 18 e a 18b ficam recolhidas como o registro de antes do corte.
# ! Motivo: a decisão 90 diz que a leitura nova passa a valer quando a corrida rodar; as abas continuam funcionando sem o arquivo, como nas outras corridas.
def secao_tela(tela: dict | None, tela_v2: dict | None, road: dict, cartoes_corridas, tela_v3: dict | None = None, tela_v4: dict | None = None, tela_ineditos: dict | None = None, teto_prompt: dict | None = None) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões, títulos e itens de leitura à vista reescritos sem b + c, p, "fixture", "rótulo", "gatilho", "poda" nem "harness" soltos.
    # ! Motivo: o texto à vista trazia siglas e números soltos que o Eric pediu para tirar; o cartão do corte sem diferença perdeu o trecho sobre o CORPO, que já está no item "Onde a tela perde" e nas tabelas.
    fontes_ = fontes(["<code>resultados_alvo/fase4/tela.json</code> e <code>.md</code> (<code>avaliar_fase4.py --tela</code>, com <code>--check</code>; blocos <code>tb_f4_tela_*</code>); a repetição com o caso ao vivo revisado em <code>tela_v2.json</code> (<code>--nome tela_v2</code>) a repetição com o prompt dentro do limite em <code>tela_v3.json</code> (<code>--nome tela_v3</code>), os sinais novos da busca em <code>tela_v4.json</code> (<code>--nome tela_v4</code>), os inéditos em <code>tela_ineditos.json</code> (<code>--nome tela_ineditos</code>) e o teto nas listas em <code>teto_prompt_tela.json</code> (<code>conferir_corte_tela.py</code>)",
                      "<code>executar_fase4.py --modo tela</code> (os casos que reproduzem em <code>reproducibilidade.json</code>, k e limiares de <code>limiares.json</code>, ponte de <code>pontes.json</code>; relatórios v2 por caso em <code>fase4_tela/relatorios/</code>)",
                      "roadmap §2.10, §2.16, §2.19 e §2.21; plano aprovado da Fase 4, seções 3.3, 5 e 6 (regra R2); fichas 37, 42, 47 e 48; decisões 82, 90 e 96 a 99"])
    vazio = {"resumo": None, "por_classe": [], "rotulos": [], "v2": None, "v3": None, "v4": None, "ineditos": None, "corridas": [], "regra": [], "limite_r2": None}
    if not tela:
        html_ = f'''<section id="tela" hidden>
<h1>Tela e caso escrito: o agente dá o mesmo diagnóstico nos dois?</h1>
<p class="lead">A corrida 18 ainda não foi rodada nesta máquina: falta <code>resultados_alvo/fase4/tela.json</code>, gerado por <code>avaliar_fase4.py --tela</code> depois de <code>executar_fase4.py --modo tela --saida fase4_tela</code> (noite B do plano aprovado).</p>
{cartoes_corridas(road, numeros=["18", "18b", "18c", "18d", "18e"], sufixo="-tela")}
{fontes_}
</section>'''
        return vazio, html_
    r = tela["resumo"]
    casos = tela["casos"]
    pcc = tela.get("prompt_contra_calibracao") or {}
    n = r["casos"] or 1
    # ! Alteração de IA - Revisar: (01/11/2026, ficha 37) a aba também lê a repetição da corrida 18 com o caso ao vivo
    # revisado (`tela_v2.json`, corrida 18b): cartão próprio, séries nos dois gráficos, colunas por classe e a comparação
    # caso a caso com a corrida original; sem o arquivo, mostra só a corrida 18.
    # ! Motivo: a regra R2 é relida na repetição, e o Eric decide pelo painel se a revisão do caso ao vivo resolveu.
    v2 = tela_v2 if tela_v2 and tela_v2.get("resumo") else None
    r2 = v2["resumo"] if v2 else None
    casos_v2 = {l["caso"]: l for l in (v2["casos"] if v2 else [])}
    classes_v2 = {x["classe"]: x for x in (v2["por_classe"] if v2 else [])}
    v3 = tela_v3 if tela_v3 and tela_v3.get("resumo") else None
    r3 = v3["resumo"] if v3 else None
    casos_v3 = {l["caso"]: l for l in (v3["casos"] if v3 else [])}
    classes_v3 = {x["classe"]: x for x in (v3["por_classe"] if v3 else [])}
    # ! Alteração de IA - Revisar: (06/11/2026, decisões 97 e 98) a aba lê também a corrida 18d (`tela_v4.json`) e os inéditos (`tela_ineditos.json`, corrida 18e): a regra pelos casos que a tela perde, nas cinco corridas, com a 18c recolhida.
    # ! Motivo: a regra fechou na 18d pela leitura fixada antes dela, e os inéditos são a conferência em casos que a busca nunca viu; sem os arquivos, a aba fica como era.
    v4 = tela_v4 if tela_v4 and tela_v4.get("resumo") else None
    r4 = v4["resumo"] if v4 else None
    casos_v4 = {l["caso"]: l for l in (v4["casos"] if v4 else [])}
    classes_v4 = {x["classe"]: x for x in (v4["por_classe"] if v4 else [])}
    ine = tela_ineditos if tela_ineditos and tela_ineditos.get("resumo") else None
    ri = ine["resumo"] if ine else None

    def contagem(campo: str, lista=None) -> dict:
        c: dict = {}
        for l in (casos if lista is None else lista):
            chave = l.get(campo) or "sem rótulo"
            c[chave] = c.get(chave, 0) + 1
        return c

    ct, cf, cg = contagem("rotulo_tela"), contagem("rotulo_fixture"), contagem("gabarito")
    ct2 = contagem("rotulo_tela", list(casos_v2.values())) if v2 else {}
    ct3 = contagem("rotulo_tela", list(casos_v3.values())) if v3 else {}
    cf3 = contagem("rotulo_fixture", list(casos_v3.values())) if v3 else {}
    ct4 = contagem("rotulo_tela", list(casos_v4.values())) if v4 else {}
    cf4 = contagem("rotulo_fixture", list(casos_v4.values())) if v4 else {}
    rotulos = [{"rotulo": x, "tela": ct.get(x, 0), "fixture": cf.get(x, 0), "gabarito": cg.get(x, 0), "tela_v2": ct2.get(x, 0) if v2 else None,
                "tela_v3": ct3.get(x, 0) if v3 else None, "fixture_v3": cf3.get(x, 0) if v3 else None, "tela_v4": ct4.get(x, 0) if v4 else None, "fixture_v4": cf4.get(x, 0) if v4 else None}
               for x in sorted(set(ct) | set(cf) | set(cg) | set(ct2) | set(ct3) | set(cf3) | set(ct4) | set(cf4), key=lambda x: (-(ct.get(x, 0) + cf.get(x, 0) + cg.get(x, 0) + ct2.get(x, 0) + ct3.get(x, 0) + cf3.get(x, 0) + ct4.get(x, 0) + cf4.get(x, 0)), x))]
    mais_tela = max(rotulos, key=lambda x: x["tela"]) if rotulos else None
    por_classe = [{"classe": x["classe"], "nome": CLASSES.get(x["classe"], ""), "casos": x["casos"], "acerto_tela": x["acerto_tela"],
                   "acerto_fixture": x["acerto_fixture"], "concordam": x["concordam"],
                   "acerto_tela_v2": classes_v2.get(x["classe"], {}).get("acerto_tela") if v2 else None,
                   "concordam_v2": classes_v2.get(x["classe"], {}).get("concordam") if v2 else None,
                   "acerto_tela_v3": classes_v3.get(x["classe"], {}).get("acerto_tela") if v3 else None,
                   "acerto_fixture_v3": classes_v3.get(x["classe"], {}).get("acerto_fixture") if v3 else None,
                   "concordam_v3": classes_v3.get(x["classe"], {}).get("concordam") if v3 else None,
                   "acerto_tela_v4": classes_v4.get(x["classe"], {}).get("acerto_tela") if v4 else None,
                   "acerto_fixture_v4": classes_v4.get(x["classe"], {}).get("acerto_fixture") if v4 else None,
                   "concordam_v4": classes_v4.get(x["classe"], {}).get("concordam") if v4 else None} for x in tela["por_classe"]]
    comparacao = []
    if v2:
        for l in casos:
            l2 = casos_v2.get(l["caso"])
            if l2:
                comparacao.append({"caso": l["caso"], "gabarito": l["gabarito"], "tela_18": l["rotulo_tela"], "tela_18b": l2["rotulo_tela"], "fixture_18b": l2["rotulo_fixture"],
                                   "acerto_18": l["acerto_tela"], "acerto_18b": l2["acerto_tela"], "concordam_18": l["concordam"], "concordam_18b": l2["concordam"],
                                   "mudou": l["rotulo_tela"] != l2["rotulo_tela"]})
    ganhos = sum(1 for c in comparacao if c["acerto_18b"] and not c["acerto_18"])
    perdas = sum(1 for c in comparacao if c["acerto_18"] and not c["acerto_18b"])
    pior = min(por_classe, key=lambda x: (x["acerto_tela"] / x["casos"] if x["casos"] else 1, -x["casos"])) if por_classe else None
    rotulos_diferentes = r["casos"] - r["concordam"]
    st, sf = r.get("selos_tela") or {}, r.get("selos_fixture") or {}
    acima = pcc.get("acima") or []
    dentro = bool(r.get("dentro_do_limite_r2"))
    cp = tela.get("corpo") or {}
    sem_dif = cp.get("sem_diferenca_contra_contrato")
    chaves_resumo = ("casos", "acerto_tela", "acerto_fixture", "concordam", "b", "c", "discordantes", "limite_r2", "dentro_do_limite_r2", "p_mcnemar",
                     "gatilhos_tela", "divergencias_tela", "segundos_tela_mediana", "segundos_fixture_mediana", "p_tela_mediana", "p_fixture_mediana", "trilha_bytes")
    comparacao_v3 = []
    if v3 and v2:
        for c, l3 in casos_v3.items():
            l2 = casos_v2.get(c)
            if l2:
                comparacao_v3.append({"caso": c, "gabarito": l3["gabarito"], "tela_18b": l2["rotulo_tela"], "tela_18c": l3["rotulo_tela"], "fixture_18b": l2["rotulo_fixture"], "fixture_18c": l3["rotulo_fixture"],
                                      "acerto_18b": l2["acerto_tela"], "acerto_18c": l3["acerto_tela"], "mudou": l2["rotulo_tela"] != l3["rotulo_tela"], "mudou_fixture": l2["rotulo_fixture"] != l3["rotulo_fixture"]})
    ganhos_v3 = sum(1 for c in comparacao_v3 if c["acerto_18c"] and not c["acerto_18b"])
    perdas_v3 = sum(1 for c in comparacao_v3 if c["acerto_18b"] and not c["acerto_18c"])
    comparacao_v4 = []
    if v4 and v3:
        for c, l4 in casos_v4.items():
            l3 = casos_v3.get(c)
            if l3:
                comparacao_v4.append({"caso": c, "gabarito": l4["gabarito"], "tela_18c": l3["rotulo_tela"], "tela_18d": l4["rotulo_tela"], "fixture_18d": l4["rotulo_fixture"],
                                      "acerto_18c": l3["acerto_tela"], "acerto_18d": l4["acerto_tela"], "mudou": l3["rotulo_tela"] != l4["rotulo_tela"], "mudou_fixture": l3["rotulo_fixture"] != l4["rotulo_fixture"]})
    ganhos_v4 = [c["caso"] for c in comparacao_v4 if c["acerto_18d"] and not c["acerto_18c"]]
    perdas_v4 = [c["caso"] for c in comparacao_v4 if c["acerto_18c"] and not c["acerto_18d"]]
    corridas_lidas = [("18", r), *([("18b", r2)] if v2 else []), *([("18c", r3)] if v3 else []), *([("18d", r4)] if v4 else [])]
    regra = [{"nome": nome_, "rotulo": f"corrida {nome_}", "casos": x["casos"], "perde": x["c"], "ganha": x["b"]} for nome_, x in corridas_lidas]
    if ri:
        regra.append({"nome": "18e", "rotulo": "corrida 18e, inéditos", "casos": ri["casos"], "perde": ri["c"], "ganha": ri["b"]})
    dados_js = {"resumo": {k: r.get(k) for k in chaves_resumo}, "por_classe": por_classe, "rotulos": rotulos,
                "v2": {"resumo": {k: r2.get(k) for k in chaves_resumo}, "ganhos": ganhos, "perdas": perdas, "mudaram": sum(1 for c in comparacao if c["mudou"])} if v2 else None,
                "v3": {"resumo": {k: r3.get(k) for k in chaves_resumo}, "ganhos": ganhos_v3, "perdas": perdas_v3, "mudaram": sum(1 for c in comparacao_v3 if c["mudou"]),
                       "verbete": v3.get("verbete_certo"), "selo": v3.get("acerto_por_selo")} if v3 else None,
                "v4": {"resumo": {k: r4.get(k) for k in chaves_resumo}, "ganhos": ganhos_v4, "perdas": perdas_v4, "mudaram": sum(1 for c in comparacao_v4 if c["mudou"]),
                       "verbete": v4.get("verbete_certo"), "selo": v4.get("acerto_por_selo")} if v4 else None,
                "ineditos": {"resumo": {k: ri.get(k) for k in chaves_resumo}, "verbete": ine.get("verbete_certo"), "selo": ine.get("acerto_por_selo")} if ine else None,
                "regra": regra if v4 else [], "limite_r2": r.get("limite_r2"),
                "corridas": [{"nome": nome_, "casos": x["casos"], "acerto_tela": x["acerto_tela"], "acerto_fixture": x["acerto_fixture"], "concordam": x["concordam"]} for nome_, x in corridas_lidas] if v3 else []}
    # ! Alteração de IA - Revisar: (06/11/2026, decisão 98) os textos da aba, também os das corridas 18 e 18b, dizem a regra R2 pelos casos que a tela perde, com os que ela ganha ao lado.
    # ! Motivo: `dentro_do_limite_r2` passou a contar só os que a tela perde; manter "só um lado acerta em N, limite 3" ao lado dele faria a aba dizer "dentro" com N acima de 3 quando a tela passar à frente do caso escrito.
    itens_kpi = [
        ("Mesma causa na tela e no caso escrito (regra R2)", f'{r["concordam"]} de {r["casos"]}',
         f'{fmt(100 * r["concordam"] / n)}%; a tela perde {r["c"]} e ganha {r["b"]}; o limite é de {r["limite_r2"]} perdidos: {"dentro" if dentro else "fora"}'),
        ("Acerto na tela", f'{r["acerto_tela"]} de {r["casos"]}', f'{fmt(100 * r["acerto_tela"] / n)}%; no caso escrito {r["acerto_fixture"]} de {r["casos"]} ({fmt(100 * r["acerto_fixture"] / n)}%)'),
        ("Causa mais respondida na tela", f'{esc(mais_tela["rotulo"])} em {mais_tela["tela"]}' if mais_tela else "n/d",
         f'no caso escrito, em {mais_tela["fixture"]}; é o gabarito de {mais_tela["gabarito"]} dos {r["casos"]} casos' if mais_tela else ""),
        ("Selos na tela (alto / médio / baixo)", f'{st.get("alto", 0)} / {st.get("medio", 0)} / {st.get("baixo", 0)}',
         f'no caso escrito {sf.get("alto", 0)} / {sf.get("medio", 0)} / {sf.get("baixo", 0)}; probabilidade mediana {fmt(r["p_tela_mediana"], 2)} contra {fmt(r["p_fixture_mediana"], 2)}'),
        ("Avisos de checagem extra e divergências na tela", f'{r["gatilhos_tela"]} e {r["divergencias_tela"]}', f'intervenções desligadas nesta corrida ({r.get("intervencoes_tela", 0)} rodadas)'),
        ("Prompt da tela acima do limite da calibração", f'{len(acima)} de {r["casos"]}',
         f'limite de {pcc.get("limite_mais_10_pct")} tokens; o maior prompt da tela tem {pcc.get("maximo_da_tela")}'),
        ("Tempo por caso", f'{fmt(r["segundos_tela_mediana"])} s', f'mediana na tela; {fmt(r["segundos_fixture_mediana"])} s no caso escrito'),
    ]
    if sem_dif is not None:
        itens_kpi.insert(3, ("Casos em que o corte não achou diferença contra o contrato", f'{sem_dif} de {cp.get("casos_lidos")}',
                             f'mesma causa em {cp.get("sem_diferenca_concordam")}; com diferença de campo, em {cp.get("com_diferenca_concordam")} de {cp.get("com_diferenca_contra_contrato")}'))
    if v2:
        n2 = r2["casos"] or 1
        itens_kpi.insert(1, ("Repetição com o caso ao vivo revisado (corrida 18b)", f'{r2["concordam"]} de {r2["casos"]} com a mesma causa',
                             f'acerto na tela {r2["acerto_tela"]} ({fmt(100 * r2["acerto_tela"] / n2)}%) contra {r["acerto_tela"]} na 18; {ganhos} ganhos, {perdas} perdas'))
    tab_comparacao = tabela(["Caso", "Gabarito", "Rótulo na tela (18)", "Rótulo na tela (18b)", "Rótulo no fixture (18b)", "Tela 18", "Tela 18b", "Mesmo rótulo 18", "Mesmo rótulo 18b", "Rótulo da tela mudou"],
                            [[f"<code>{esc(c['caso'])}</code>", f"<code>{esc(c['gabarito'])}</code>", f"<code>{esc(c['tela_18'] or 'sem rótulo')}</code>", f"<code>{esc(c['tela_18b'] or 'sem rótulo')}</code>",
                              f"<code>{esc(c['fixture_18b'] or 'sem rótulo')}</code>", "certo" if c["acerto_18"] else "errado", "certo" if c["acerto_18b"] else "errado",
                              "sim" if c["concordam_18"] else "não", "sim" if c["concordam_18b"] else "não", "sim" if c["mudou"] else "não"] for c in comparacao], raw=True) if v2 else ""
    # ! Alteração de IA - Revisar: (05/11/2026, corrida 18c) as tabelas recolhidas ganham as colunas da 18c, e o caso a caso passa à leitura vigente.
    # ! Motivo: na página publicada, "Caso a caso" ainda listava a corrida 18 com a 18c já valendo, e quem abrisse a tabela veria rótulos de antes das duas revisões.
    tab_classe = tabela(["Classe", "Casos", "Acerto na tela", "Acerto no fixture", "Mesmo rótulo"] + (["Acerto na tela (18b)", "Mesmo rótulo (18b)"] if v2 else []) + (["Acerto na tela (18c)", "Acerto no fixture (18c)", "Mesmo rótulo (18c)"] if v3 else []) + (["Acerto na tela (18d)", "Acerto no fixture (18d)", "Mesmo rótulo (18d)"] if v4 else []),
                        [[f'{x["classe"]} {x["nome"]}', x["casos"], x["acerto_tela"], x["acerto_fixture"], x["concordam"]]
                         + ([x["acerto_tela_v2"] if x["acerto_tela_v2"] is not None else "—", x["concordam_v2"] if x["concordam_v2"] is not None else "—"] if v2 else [])
                         + ([x["acerto_tela_v3"], x["acerto_fixture_v3"], x["concordam_v3"]] if v3 else [])
                         + ([x["acerto_tela_v4"], x["acerto_fixture_v4"], x["concordam_v4"]] if v4 else []) for x in por_classe])
    tab_rotulos = tabela(["Rótulo", "Dado na tela", "Dado no fixture", "É o gabarito de"] + (["Dado na tela (18b)"] if v2 else []) + (["Dado na tela (18c)", "Dado no fixture (18c)"] if v3 else []) + (["Dado na tela (18d)", "Dado no fixture (18d)"] if v4 else []),
                         [[f"<code>{esc(x['rotulo'])}</code>", x["tela"], x["fixture"], x["gabarito"]] + ([x["tela_v2"]] if v2 else []) + ([x["tela_v3"], x["fixture_v3"]] if v3 else []) + ([x["tela_v4"], x["fixture_v4"]] if v4 else []) for x in rotulos], raw=True)

    def tabela_de_casos(lista: list[dict]) -> str:
        return tabela(["Caso", "Classe", "Gabarito", "Rótulo na tela", "Rótulo no fixture", "Tela", "Fixture", "Mesmo rótulo", "p tela", "Selo tela", "p fixture", "Selo fixture",
                       "Gatilho", "Divergência", "s tela", "s fixture"],
                      [[f"<code>{esc(l['caso'])}</code>", l["classe"], f"<code>{esc(l['gabarito'])}</code>", f"<code>{esc(l['rotulo_tela'] or 'sem rótulo')}</code>",
                        f"<code>{esc(l['rotulo_fixture'] or 'sem rótulo')}</code>", "certo" if l["acerto_tela"] else "errado", "certo" if l["acerto_fixture"] else "errado",
                        "sim" if l["concordam"] else "não", fmt(l["p_tela"], 2), esc(l.get("selo_tela") or "—"), fmt(l["p_fixture"], 2), esc(l.get("selo_fixture") or "—"),
                        "sim" if l["gatilho_tela"] else "não", "sim" if l["divergencia_tela"] else "não", fmt(l["segundos_tela"]), fmt(l["segundos_fixture"])] for l in lista], raw=True)

    tab_casos = tabela_de_casos(list(casos_v4.values()) if v4 else list(casos_v3.values()) if v3 else casos)
    lead = (f'{"Sim" if dentro else "Não"}. Nos {r["casos"]} casos que reproduzem, o agente dá o mesmo rótulo na tela e no fixture em {r["concordam"]} ({fmt(100 * r["concordam"] / n)}%): '
            f'acerta {r["acerto_tela"]} na tela e {r["acerto_fixture"]} no fixture; só a tela acerta em {r["b"]}, só o fixture em {r["c"]} '
            f'(limite da regra R2 = {r["limite_r2"]} para os que a tela perde: {"dentro" if dentro else "fora"} do limite; p = {fmt(r["p_mcnemar"], 3)}). '
            + (f'Na tela o rótulo mais dado é <code>{esc(mais_tela["rotulo"])}</code>, em {mais_tela["tela"]} casos ({mais_tela["fixture"]} no fixture; gabarito de {mais_tela["gabarito"]}). ' if mais_tela else "")
            + f'{len(acima)} dos {r["casos"]} prompts da tela passam do limite de tokens da calibração.'
            + (f' Na repetição com o caso ao vivo revisado (corrida 18b), o mesmo rótulo sai em {r2["concordam"]} de {r2["casos"]} e a tela acerta {r2["acerto_tela"]} '
               f'(perde {r2["c"]} para o fixture e ganha {r2["b"]}, {"dentro" if r2.get("dentro_do_limite_r2") else "fora"} do limite da regra R2).' if v2 else ""))
    leitura_ = leitura([
        *([f"<strong>Repetição com o caso ao vivo revisado (corrida 18b).</strong> A mesma causa passou de {r['concordam']} para {r2['concordam']} dos {r2['casos']} casos e o acerto na tela de "
           f"{r['acerto_tela']} para {r2['acerto_tela']} (caso escrito: {r['acerto_fixture']} e {r2['acerto_fixture']}). A tela perde {r2['c']} casos para o caso escrito e ganha {r2['b']}, contra o limite de {r2['limite_r2']} perdidos: a regra que compara tela e caso escrito (R2) "
           f"{'passa a valer' if r2.get('dentro_do_limite_r2') else 'continua fora do limite'}. Caso a caso, {ganhos} passaram a acertar na tela e {perdas} deixaram de acertar; "
           f"a causa respondida na tela mudou em {sum(1 for c in comparacao if c['mudou'])} casos (tabela de comparação; blocos <code>tb_f4_tela_resumo</code> e <code>tb_f4_tela_casos</code> de <code>tela_v2.json</code>)."] if v2 else []),
        (f"<strong>Regra que compara tela e caso escrito (R2) {'cumprida' if dentro else 'não cumprida'}.</strong> {rotulos_diferentes} casos recebem causas diferentes nos dois lados; a tela perde {r['c']} para o caso escrito e ganha {r['b']} "
         f"(bloco <code>tb_f4_tela_resumo</code>); o limite é de {r['limite_r2']} perdidos. "
         + ("" if dentro else "Pelo plano aprovado (regra R2), o molde do sintoma e o corte em código do que o modelo lê no caso ao vivo (poda) voltam para revisão antes da próxima noite com modelo.")),
        (f"<strong>A causa que a tela puxa.</strong> <code>{esc(mais_tela['rotulo'])}</code> sai {mais_tela['tela']} vezes na tela, {mais_tela['fixture']} no caso escrito, e é o gabarito de "
         f"{mais_tela['gabarito']} casos (tabela de causas): o caso ao vivo leva o modelo para uma causa que o caso escrito não sugere." if mais_tela else "<strong>Causas respondidas.</strong> Sem casos."),
        *([f"<strong>Onde a tela perde.</strong> Em {sem_dif} dos {cp.get('casos_lidos')} casos o corte não achou diferença de campo contra o contrato e o CORPO levou ao modelo o primeiro item "
           f"normal da lista (bloco <code>tb_f4_tela_corpo</code>): só {cp.get('sem_diferenca_concordam')} dão a mesma causa e {cp.get('sem_diferenca_colecao_na_tela')} viram "
           f"<code>colecao_no_lugar_de_objeto</code>; em {cp.get('sintoma_sem_medida')} o sintoma por molde diz \"Nenhuma diferença medida contra a referência\". "
           f"Nos {cp.get('com_diferenca_contra_contrato')} casos com diferença de campo, {cp.get('com_diferenca_concordam')} dão a mesma causa. As falhas de lista (contagem, duplicado, "
           "codificação, escala, latência) não são diferenças de campo: o caso ao vivo precisa dizer o que mudou contra a referência em modo normal, que o próprio teste já mede."] if sem_dif is not None else []),
        (f"<strong>A pior classe na tela.</strong> {pior['classe']} {esc(pior['nome'])}: {pior['acerto_tela']} de {pior['casos']} na tela contra {pior['acerto_fixture']} no caso escrito "
         f"(bloco <code>tb_f4_tela_por_classe</code>)." if pior else "<strong>Por classe.</strong> Sem dados."),
        f"<strong>Prompt maior que o da calibração.</strong> {len(acima)} dos {r['casos']} prompts da tela passam de {pcc.get('limite_mais_10_pct')} tokens (o maior da tela tem {pcc.get('maximo_da_tela')}; "
        f"o maior da calibração, {pcc.get('maximo_da_calibracao')}): o caso ao vivo é mais longo que o caso escrito, e os limiares do selo foram calibrados no escrito (plano, seção 3.3).",
        f"<strong>Selos e avisos de checagem extra.</strong> Na tela {st.get('baixo', 0)} casos ficam com selo baixo e {r['gatilhos_tela']} disparam o aviso que dispara a checagem extra; as intervenções ficaram desligadas nesta corrida, "
        f"então a FONTE fica declarada, não verificada. No caso escrito {sf.get('alto', 0)} casos têm selo alto, na tela {st.get('alto', 0)}.",
        f"<strong>Custo.</strong> {fmt(r['segundos_tela_mediana'])} s por caso na tela e {fmt(r['segundos_fixture_mediana'])} s no caso escrito (medianas); a trilha v2 da corrida tem {r['trilha_bytes']} bytes.",
    ])
    # ! Alteração de IA - Revisar: (05/11/2026, decisão 90) o bloco da 18c: cartões, os dois gráficos novos, a leitura e a comparação caso a caso com a 18b.
    # ! Motivo: é a leitura que vale agora. Na 18c o prompt coube no limite e o que ainda separa a tela do caso escrito é a busca, e o Eric precisa ver isso antes dos números das corridas anteriores.
    bloco_v3, comparacao_v3_html, kpis_antigos = "", "", kpis(itens_kpi)

    def de(x: dict | None) -> str:
        return f'{(x or {}).get("acertos", 0)} de {(x or {}).get("casos", 0)}'

    itens_v3: list = []
    leitura_v3 = ""
    if v3:
        n3 = r3["casos"] or 1
        pcc3, pcc2 = v3.get("prompt_contra_calibracao") or {}, (v2.get("prompt_contra_calibracao") or {}) if v2 else {}
        vc = v3.get("verbete_certo") or {"tela": {"presente": {"casos": 0, "acertos": 0}, "ausente": {"casos": 0, "acertos": 0}}, "fixture": {"presente": {"casos": 0, "acertos": 0}, "ausente": {"casos": 0, "acertos": 0}}}
        vc2 = (v2.get("verbete_certo") if v2 else None) or vc
        selo3, selo2 = v3.get("acerto_por_selo") or {}, (v2.get("acerto_por_selo") if v2 else None) or {}
        dentro3 = bool(r3.get("dentro_do_limite_r2"))
        mais_tela3 = max(rotulos, key=lambda x: x["tela_v3"] or 0) if rotulos else None
        itens_v3 = [
            ("Mesma causa na tela e no caso escrito (corrida 18c)", f'{r3["concordam"]} de {r3["casos"]}', f'{fmt(100 * r3["concordam"] / n3)}%; a tela perde {r3["c"]} e ganha {r3["b"]}; o limite é de {r3["limite_r2"]} perdidos (decisão 98): {"dentro" if dentro3 else "fora"}'),
            ("Acerto na tela", f'{r3["acerto_tela"]} de {r3["casos"]}', f'{fmt(100 * r3["acerto_tela"] / n3)}%; no caso escrito {r3["acerto_fixture"]} de {r3["casos"]} ({fmt(100 * r3["acerto_fixture"] / n3)}%)'),
            ("Com o verbete certo no contexto", de(vc["tela"]["presente"]), f'acertos na tela; sem ele, {de(vc["tela"]["ausente"])}'),
            ("O verbete certo chega ao modelo", f'{vc["tela"]["presente"]["casos"]} de {r3["casos"]}', f'na tela; no caso escrito, em {vc["fixture"]["presente"]["casos"]} de {r3["casos"]}'),
            ("Selo alto na tela", de(selo3.get("alto")), f'acertos; no selo baixo, {de(selo3.get("baixo"))}'),
            ("Prompt da tela acima do limite", f'{len(pcc3.get("acima") or [])} de {r3["casos"]}', f'limite de {pcc3.get("limite_mais_10_pct")} tokens; o maior tem {pcc3.get("maximo_da_tela")}; na 18b eram {len(pcc2.get("acima") or [])}'),
            ("Tempo por caso na tela", f'{fmt(r3["segundos_tela_mediana"])} s', f'mediana; na 18b, {fmt(r2["segundos_tela_mediana"])} s; no caso escrito, {fmt(r3["segundos_fixture_mediana"])} s' if v2 else f'mediana; no caso escrito, {fmt(r3["segundos_fixture_mediana"])} s'),
        ]
        mudou_fixture = sum(1 for c in comparacao_v3 if c["mudou_fixture"])
        lead = (f'{"Sim" if dentro3 else "Não dentro do limite"}. Na corrida 18c, com o caso ao vivo encurtado, o agente dá a mesma causa na tela e no caso escrito em {r3["concordam"]} dos {r3["casos"]} casos ({fmt(100 * r3["concordam"] / n3)}%): '
                f'acerta {r3["acerto_tela"]} na tela e {r3["acerto_fixture"]} no caso escrito; só a tela acerta em {r3["b"]}, só o caso escrito em {r3["c"]} (limite da regra R2 = {r3["limite_r2"]} para os que a tela perde, decisão 98; p = {fmt(r3["p_mcnemar"], 3)}). '
                f'{len(pcc3.get("acima") or [])} dos {r3["casos"]} prompts da tela passam do limite de {pcc3.get("limite_mais_10_pct")} tokens.')
        leitura_v3 = leitura([
            f'<strong>O corte fez o que devia.</strong> Os {r3["casos"]} prompts ficaram dentro do limite de {pcc3.get("limite_mais_10_pct")} tokens, o maior com {pcc3.get("maximo_da_tela")} (na 18b, o maior tinha {pcc2.get("maximo_da_tela")}). O tempo por caso na tela caiu de {fmt(r2["segundos_tela_mediana"]) if v2 else "n/d"} s para {fmt(r3["segundos_tela_mediana"])} s. No caso escrito, que não encurtou, foi de {fmt(r2["segundos_fixture_mediana"]) if v2 else "n/d"} s para {fmt(r3["segundos_fixture_mediana"])} s: o ganho vem do prompt menor, não da versão do Ollama.',
            f'<strong>A regra que compara os dois lados (R2) {"está dentro do limite" if dentro3 else "segue fora do limite"}.</strong> A tela perde {r3["c"]} casos para o caso escrito (eram {r2["c"] if v2 else "n/d"}) e ganha {r3["b"]}; o limite é de {r3["limite_r2"]} perdidos (decisão 98, fixada antes da corrida 18d; pela conta de antes, b + c = {r3["discordantes"]}). A mesma causa subiu de {r2["concordam"] if v2 else "n/d"} para {r3["concordam"]} dos {r3["casos"]}; o acerto na tela, de {r2["acerto_tela"] if v2 else "n/d"} para {r3["acerto_tela"]}; o do caso escrito, de {r2["acerto_fixture"] if v2 else "n/d"} para {r3["acerto_fixture"]}.',
            f'<strong>O que ainda separa os dois lados é a busca.</strong> Com o verbete da causa certa entre os entregues, a tela acerta {de(vc["tela"]["presente"])}; sem ele, {de(vc["tela"]["ausente"])}. No caso escrito é parecido: {de(vc["fixture"]["presente"])} e {de(vc["fixture"]["ausente"])}. A diferença está em quantas vezes o verbete chega: {vc["tela"]["presente"]["casos"]} na tela e {vc["fixture"]["presente"]["casos"]} no caso escrito (na 18b, {vc2["tela"]["presente"]["casos"]} na tela). O Eric decidiu mexer na busca (ficha 47, decisão 97), e as corridas 18d, 21d e 18e medem o efeito.',
            *([f'<strong>A causa que a tela puxa.</strong> <code>{esc(mais_tela3["rotulo"])}</code> sai {mais_tela3["tela_v3"]} vezes na tela, {mais_tela3["fixture_v3"]} no caso escrito, e é o gabarito de {mais_tela3["gabarito"]} casos: sem o verbete certo, é para ela que o modelo vai.'] if mais_tela3 else []),
            f'<strong>O selo de confiança ficou mais útil.</strong> Com o prompt do tamanho da calibração, o selo alto acerta {de(selo3.get("alto"))}, o médio {de(selo3.get("medio"))} e o baixo {de(selo3.get("baixo"))}; na 18b eram {de(selo2.get("alto"))}, {de(selo2.get("medio"))} e {de(selo2.get("baixo"))}. São poucos casos: serve de triagem, não de barreira.',
            f'<strong>Caso a caso, contra a 18b.</strong> {ganhos_v3} casos passaram a acertar na tela e {perdas_v3} deixaram de acertar; a causa respondida na tela mudou em {sum(1 for c in comparacao_v3 if c["mudou"])}. A 18c também trocou a versão do Ollama e a biblioteca (a de produção, depois do lote), e o caso escrito serve de controle: ali a causa mudou em {mudou_fixture} dos {r3["casos"]}.',
        ])
        bloco_v3 = f"""<h2>O que mudou de uma corrida para outra</h2>
<p>A corrida 18 mediu um defeito do caso de entrada; a 18b corrigiu o caso, com o prompt acima do limite; a 18c encurtou o prompt até caber no limite do plano.</p>
<div class="chart baixo"><canvas id="g-tela-corridas"></canvas></div>
<h2>O verbete certo no contexto é o que mais pesa</h2>
<p>Cada barra separa os casos em que o verbete da causa certa estava entre os três entregues ao modelo e os casos em que não estava.</p>
<div class="chart baixo"><canvas id="g-tela-verbete"></canvas></div>
{leitura_v3}"""
        kpis_antigos = detalhes("As corridas 18 e 18b, em números", kpis(itens_kpi))
        itens_kpi = itens_v3
        comparacao_v3_html = detalhes(f"Corrida 18b contra a 18c, caso a caso ({len(comparacao_v3)} casos)", tabela(
            ["Caso", "Gabarito", "Rótulo na tela (18b)", "Rótulo na tela (18c)", "Rótulo no caso escrito (18c)", "Tela 18b", "Tela 18c", "Rótulo da tela mudou"],
            [[f"<code>{esc(c['caso'])}</code>", f"<code>{esc(c['gabarito'])}</code>", f"<code>{esc(c['tela_18b'] or 'sem rótulo')}</code>", f"<code>{esc(c['tela_18c'] or 'sem rótulo')}</code>",
              f"<code>{esc(c['fixture_18c'] or 'sem rótulo')}</code>", "certo" if c["acerto_18b"] else "errado", "certo" if c["acerto_18c"] else "errado", "sim" if c["mudou"] else "não"] for c in comparacao_v3], raw=True))
    comparacao_v4_html, ineditos_html, leitura_18c_html = "", "", ""
    if v4:
        n4 = r4["casos"] or 1
        pcc4 = v4.get("prompt_contra_calibracao") or {}
        vc4, selo4 = v4["verbete_certo"], v4.get("acerto_por_selo") or {}
        vc3_ = (v3.get("verbete_certo") if v3 else None) or vc4
        dentro4 = bool(r4.get("dentro_do_limite_r2"))
        mudou_fixture4 = sum(1 for c in comparacao_v4 if c["mudou_fixture"])

        def lista_de_casos(ids: list[str]) -> str:
            return ", ".join(f"<code>{esc(c)}</code>" for c in ids) or "nenhum"

        perdidos = [l for l in casos_v4.values() if l["acerto_fixture"] and not l["acerto_tela"]]
        erram_os_dois = [l["caso"] for l in casos_v4.values() if not l["acerto_fixture"] and not l["acerto_tela"]]
        pares: dict = {}
        for l in perdidos:
            pares.setdefault((l["gabarito"], l["rotulo_tela"]), []).append(l["caso"])
        texto_perdidos = "; ".join(f"<code>{esc(g_)}</code> lido como <code>{esc(rt or 'sem rótulo')}</code> em {lista_de_casos(ids)}" for (g_, rt), ids in pares.items())
        selos_perdidos = {l.get("selo_tela") for l in perdidos}
        itens_v4 = [
            ("A tela perde para o caso escrito (regra R2, corrida 18d)", f'{r4["c"]} de {r4["casos"]}', f'a tela perde {r4["c"]} e ganha {r4["b"]}; o limite é de {r4["limite_r2"]} perdidos (decisão 98): {"dentro" if dentro4 else "fora"}; pela soma dos dois lados, {r4["discordantes"]}'),
            ("Acerto na tela", f'{r4["acerto_tela"]} de {r4["casos"]}', f'{fmt(100 * r4["acerto_tela"] / n4)}%; no caso escrito {r4["acerto_fixture"]} de {r4["casos"]} ({fmt(100 * r4["acerto_fixture"] / n4)}%); eram {r3["acerto_tela"] if v3 else "n/d"} na 18c'),
            *([("Nos inéditos, que a busca nunca viu (corrida 18e)", f'{ri["acerto_tela"]} de {ri["casos"]} na tela', f'{ri["acerto_fixture"]} no caso escrito; a tela perde {ri["c"]} e ganha {ri["b"]}')] if ri else []),
            ("O verbete certo chega ao modelo", f'{vc4["tela"]["presente"]["casos"]} de {r4["casos"]}', f'na tela (eram {vc3_["tela"]["presente"]["casos"]} na 18c); no caso escrito, em {vc4["fixture"]["presente"]["casos"]} de {r4["casos"]}'),
            ("Com o verbete certo no contexto", de(vc4["tela"]["presente"]), f'acertos na tela; sem ele, {de(vc4["tela"]["ausente"])}'),
            ("Selo alto na tela", de(selo4.get("alto")), f'acertos; no médio, {de(selo4.get("medio"))}; no baixo, {de(selo4.get("baixo"))}'),
            ("Prompt da tela acima do limite", f'{len(pcc4.get("acima") or [])} de {r4["casos"]}', f'limite de {pcc4.get("limite_mais_10_pct")} tokens; o maior tem {pcc4.get("maximo_da_tela")}'),
            ("Tempo por caso na tela", f'{fmt(r4["segundos_tela_mediana"])} s', f'mediana; na 18c, {fmt(r3["segundos_tela_mediana"])} s; no caso escrito, {fmt(r4["segundos_fixture_mediana"])} s' if v3 else f'mediana; no caso escrito, {fmt(r4["segundos_fixture_mediana"])} s'),
        ]
        lead = (f'{"Dentro do que a regra aceita" if dentro4 else "Ainda fora do limite"}. Na corrida 18d, com a busca lendo o que o caso mede contra a referência, o agente acerta {r4["acerto_tela"]} dos {r4["casos"]} na tela e {r4["acerto_fixture"]} no caso escrito; '
                f'a tela perde {r4["c"]} casos para o caso escrito e ganha {r4["b"]} (limite da regra R2 = {r4["limite_r2"]} para os que a tela perde, decisão 98; pela soma dos dois lados, {r4["discordantes"]}; p = {fmt(r4["p_mcnemar"], 3)}). '
                + (f'Nos {ri["casos"]} inéditos, que a busca nunca viu (corrida 18e), são {ri["acerto_tela"]} na tela e {ri["acerto_fixture"]} no caso escrito, e a tela perde {ri["c"]} e ganha {ri["b"]} (p = {fmt(ri["p_mcnemar"], 3)}).' if ri else ""))
        itens_leitura_v4 = [
            f'<strong>A regra que compara os dois lados (R2) {"está dentro do limite" if dentro4 else "segue fora do limite"}.</strong> A tela perde {r4["c"]} casos para o caso escrito (eram {r3["c"] if v3 else "n/d"} na 18c) e ganha {r4["b"]} (eram {r3["b"] if v3 else "n/d"}); o limite é de {r4["limite_r2"]} perdidos. É o limite exato, sem folga, e corridas iguais já variaram até {r4["limite_r2"]} casos. A leitura foi fixada antes da corrida, sem conhecer o resultado dela (ficha 48, decisão 98). Pela conta de antes, a soma dos dois lados daria {r4["discordantes"]}, e a regra ficaria fora pelo lado bom.',
            f'<strong>O que mudou foi a busca.</strong> O verbete certo chega em {vc4["tela"]["presente"]["casos"]} dos {r4["casos"]} casos na tela (eram {vc3_["tela"]["presente"]["casos"]}) e em {vc4["fixture"]["presente"]["casos"]} no caso escrito. O acerto na tela foi de {r3["acerto_tela"] if v3 else "n/d"} para {r4["acerto_tela"]}, e o caso escrito ficou em {r4["acerto_fixture"]}, com a causa mudando em {mudou_fixture4} casos: ele é o controle. A diferença vem dos sinais, que ficam só do lado da tela. Isso não quer dizer que o modelo lê melhor da tela: o caso da tela leva uma medida contra a referência que o caso escrito não tem.',
        ]
        if ri:
            vci = ine["verbete_certo"]
            itens_leitura_v4.append(f'<strong>A conferência limpa (corrida 18e).</strong> Os sinais foram escritos olhando os {r4["casos"]} casos, então a conta deles pode estar favorecida. Nos {ri["casos"]} inéditos, que a busca nunca viu, o agente acerta {ri["acerto_tela"]} na tela e {ri["acerto_fixture"]} no caso escrito; a tela perde {ri["c"]} e ganha {ri["b"]}, e o verbete certo chega em {vci["tela"]["presente"]["casos"]} de {ri["casos"]} na tela, contra {vci["fixture"]["presente"]["casos"]} no caso escrito. São poucos casos: o teste pareado não separa os dois lados (p = {fmt(ri["p_mcnemar"], 3)}), e a conferência da ficha 46 ainda não foi feita. Depois desta leitura, esses casos não servem mais de conferência limpa para outro ajuste na busca.')
        itens_leitura_v4 += [
            f'<strong>O que a tela ainda perde.</strong> {texto_perdidos}{"; todos com selo baixo" if selos_perdidos == {"baixo"} else ""}. Erram também no caso escrito: {lista_de_casos(erram_os_dois)}.',
            f'<strong>O selo de confiança.</strong> O selo alto acerta {de(selo4.get("alto"))}, o médio {de(selo4.get("medio"))} e o baixo {de(selo4.get("baixo"))}. Os limiares são os da corrida 16, sem recalibrar, e são poucos casos: serve de triagem, não de barreira.',
            f'<strong>Caso a caso, contra a 18c.</strong> Passaram a acertar na tela {lista_de_casos(ganhos_v4)}, e deixou de acertar {lista_de_casos(perdas_v4)}; a causa respondida na tela mudou em {sum(1 for c in comparacao_v4 if c["mudou"])} casos. O prompt ficou dentro do limite nos {r4["casos"]}, com o maior em {pcc4.get("maximo_da_tela")} tokens, e o tempo na tela foi de {fmt(r3["segundos_tela_mediana"]) if v3 else "n/d"} s para {fmt(r4["segundos_tela_mediana"])} s; no caso escrito, que não mudou, de {fmt(r3["segundos_fixture_mediana"]) if v3 else "n/d"} s para {fmt(r4["segundos_fixture_mediana"])} s.',
        ]
        if ine and (ine.get("prompt_contra_calibracao") or {}).get("acima"):
            pcci = ine["prompt_contra_calibracao"]
            antes_i = {l["caso"]: l for l in ine["casos"]}
            medidos = {l["caso"]: l for l in ((teto_prompt or {}).get("corridas") or {}).get("18e", {}).get("linhas", [])}
            partes_i = []
            for c_ in pcci["acima"]:
                m_ = medidos.get(f"{c_}@tela") or {}
                depois = m_.get("tokens_medidos") or m_.get("tokens_estimados")
                partes_i.append(f'<code>{esc(c_)}</code> com {antes_i[c_]["tokens_entrada_tela"]} tokens' + (f', que caiu para {depois}' if depois else ""))
            itens_leitura_v4.append(f'<strong>Dois prompts dos inéditos passaram do limite.</strong> {"; ".join(partes_i)}; o limite é {pcci.get("limite_mais_10_pct")}. A causa era a lista sem teto, quando a resposta muda inteira. Os dois erram nos dois lados, então a regra R2 não depende deles. O caso ao vivo ganhou um teto nas listas (decisão 99), sem corrida nova: os prompts das corridas 18d e 21d não mudaram, salvo o tempo medido na hora.')
        leitura_v4 = leitura(itens_leitura_v4)
        bloco_v3 = f"""<h2>A regra: o que a tela perde e o que ela ganha</h2>
<p>A regra R2 aceita que a tela perca até {r4["limite_r2"]} casos para o caso escrito. Cada grupo é uma corrida; a última são os inéditos, que a busca nunca viu.</p>
<div class="chart baixo"><canvas id="g-tela-regra"></canvas></div>
<h2>O que mudou de uma corrida para outra</h2>
<p>A corrida 18 mediu um defeito do caso de entrada; a 18b corrigiu o caso, com o prompt acima do limite; a 18c encurtou o prompt até caber no limite do plano; a 18d traduziu para a busca o que o caso mede contra a referência.</p>
<div class="chart baixo"><canvas id="g-tela-corridas"></canvas></div>
<h2>O verbete certo no contexto é o que mais pesa</h2>
<p>Cada barra separa os casos em que o verbete da causa certa estava entre os três entregues ao modelo e os casos em que não estava, na corrida 18d.</p>
<div class="chart baixo"><canvas id="g-tela-verbete"></canvas></div>
{leitura_v4}"""
        if v3:
            leitura_18c_html = detalhes("A leitura da corrida 18c", kpis(itens_v3) + leitura_v3)
        itens_kpi = itens_v4
        comparacao_v4_html = detalhes(f"Corrida 18c contra a 18d, caso a caso ({len(comparacao_v4)} casos)", tabela(
            ["Caso", "Gabarito", "Rótulo na tela (18c)", "Rótulo na tela (18d)", "Rótulo no caso escrito (18d)", "Tela 18c", "Tela 18d", "Rótulo da tela mudou"],
            [[f"<code>{esc(c['caso'])}</code>", f"<code>{esc(c['gabarito'])}</code>", f"<code>{esc(c['tela_18c'] or 'sem rótulo')}</code>", f"<code>{esc(c['tela_18d'] or 'sem rótulo')}</code>",
              f"<code>{esc(c['fixture_18d'] or 'sem rótulo')}</code>", "certo" if c["acerto_18c"] else "errado", "certo" if c["acerto_18d"] else "errado", "sim" if c["mudou"] else "não"] for c in comparacao_v4], raw=True))
        if ine:
            ineditos_html = detalhes(f"Caso a caso, nos inéditos, corrida 18e ({ri['casos']} casos)", tabela_de_casos(ine["casos"]))
    html_ = f'''<section id="tela" hidden>
<h1>Tela e caso escrito: o agente dá o mesmo diagnóstico nos dois?</h1>
<p class="lead">{lead}</p>
{kpis(itens_kpi) if v3 else kpis_antigos}
{bloco_v3}
<h2>Acerto e concordância por classe de defeito</h2>
<p>Cada caso que reproduz foi diagnosticado duas vezes na mesma sessão do Ollama: lido da tela (roteiro, interceptação, corte em código do que o modelo lê e sintoma por molde) e lido do caso escrito. O gabarito entra só nesta leitura.</p>
<div class="chart"><canvas id="g-tela-classe"></canvas></div>
{tab_classe}
<h2>Que causas cada lado responde</h2>
<p>Quantas vezes cada causa foi respondida na tela e no caso escrito, contra quantas vezes ela é o gabarito.</p>
<div class="chart alto"><canvas id="g-tela-rotulos"></canvas></div>
{tab_rotulos}
{detalhes(f"Caso a caso, na corrida 18d ({r4['casos']} casos)" if v4 else f"Caso a caso, na corrida 18c ({r3['casos']} casos)" if v3 else f"Caso a caso ({len(casos)} casos)", tab_casos)}
{ineditos_html}
{comparacao_v4_html}
{comparacao_v3_html}
{detalhes(f"Corrida 18 contra a repetição 18b, caso a caso ({len(comparacao)} casos)", tab_comparacao) if v2 else ""}
{kpis_antigos if v3 else ""}
{detalhes(f"Prompts da tela acima do limite, na corrida 18 ({len(acima)})" if v3 else f"Prompts da tela acima do limite da calibração ({len(acima)})", "<p>" + ", ".join(f"<code>{esc(c)}</code>" for c in acima) + "</p>" if acima else "<p>nenhum</p>")}
<h2>As corridas no roadmap</h2>
{cartoes_corridas(road, numeros=["18", "18b", "18c", "18d", "18e"], sufixo="-tela")}
{leitura_18c_html}
{detalhes("A leitura das corridas 18 e 18b", leitura_) if v3 else leitura_}
{fontes_}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ 21. Fase 4: cura de seletor (corrida 19)

# ! Alteração de IA - Revisar: aba nova (01/11/2026, Fase 4, pacote P4) com a leitura da corrida 19 (cura de seletor), lida
# de resultados_alvo/fase4/cura.json (avaliar_fase4.py --cura): a taxa de cura pela regra R3 (uma cura só conta quando o
# roteiro passa na reexecução; "mesmo elemento" separado de "outro elemento"), o MTTR da detecção à reexecução validada,
# por modo de quebra, por roteiro e pelas duas formas da quebra (harness e variante do PHP, decisão 80), o rendimento de
# cada estratégia de candidato e os casos "outro elemento"; sem o arquivo, o estado vazio com o cartão da corrida.
# ! Motivo: a regra do painel é uma aba por análise, lida dos JSON; a corrida 19 é a primeira medida de MTTR só do agente
# e o Eric decide pelo painel se a cura em código basta para a Fase 5.
def secao_cura(cura: dict | None, road: dict, cartoes_corridas) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões, títulos e itens de leitura à vista reescritos com "tempo até o resultado (MTTR)" e "o próprio teste" no lugar de MTTR e harness soltos.
    # ! Motivo: o texto à vista trazia siglas que o Eric pediu para tirar; o cartão da quebra armada pelo teste contra a variante do PHP ficou com menos texto, e os valores seguem nas tabelas recolhidas.
    fontes_ = fontes(["<code>resultados_alvo/fase4/cura.json</code> e <code>.md</code> (<code>avaliar_fase4.py --cura</code>, com <code>--check</code>; blocos <code>tb_f4_cura_*</code>)",
                      "<code>executar_fase4.py --modo cura</code> (<code>cura_seletor.py</code>: candidatos em ordem fixa e verificação em código; <code>cenarios_fase4.QUEBRAS</code>: as 16 células; "
                      "<code>Programacao/CobaiaFront/quebra.php</code>: a variante do front ligada por <code>?quebra=</code> ou cookie; relatórios v2 por execução em <code>fase4_cura/relatorios/</code>)",
                      "roadmap §2.11; plano aprovado da Fase 4, seções 3.6, 5 (regra R3) e 6; fichas 29 (opção c, decisão 80), 35 e 36"])
    vazio = {"resumo": None, "por_modo": [], "por_roteiro": [], "por_forma": [], "estrategias": []}
    if not cura or not cura.get("resumo"):
        html_ = f'''<section id="cura" hidden>
<h1>Cura de seletor: quando o localizador quebra, o agente acha outro em código e o roteiro passa?</h1>
<p class="lead">A corrida 19 ainda não foi rodada nesta máquina: falta <code>resultados_alvo/fase4/cura.json</code>, gerado por <code>avaliar_fase4.py --cura</code> depois de <code>executar_fase4.py --modo cura --saida fase4_cura</code> (pacote P4 do plano aprovado, sem modelo).</p>
{cartoes_corridas(road, numeros=["19"], sufixo="-cura")}
{fontes_}
</section>'''
        return vazio, html_
    r = cura["resumo"]
    f = cura.get("formas") or {}
    por_modo = [{"modo": x["modo"], "execucoes": x["execucoes"], "quebrou": x["quebrou"], "curadas": x["curadas"], "mesmo_elemento": x["mesmo_elemento"],
                 "outro_elemento": x["outro_elemento"], "nao_curadas": x["nao_curadas"], "nao_quebrou": x["nao_quebrou"], "taxa": x["taxa_de_cura_pct"],
                 "mttr": x["mttr_mediana_s"]} for x in cura["por_modo"]]
    por_roteiro = [{"roteiro": x["roteiro"], "execucoes": x["execucoes"], "quebrou": x["quebrou"], "curadas": x["curadas"], "mesmo_elemento": x["mesmo_elemento"],
                    "outro_elemento": x["outro_elemento"], "nao_curadas": x["nao_curadas"], "nao_quebrou": x["nao_quebrou"], "taxa": x["taxa_de_cura_pct"],
                    "mttr": x["mttr_mediana_s"]} for x in cura["por_roteiro"]]
    por_forma = [{"forma": x["forma"], "quebrou": x["quebrou"], "curadas": x["curadas"], "taxa": x["taxa_de_cura_pct"], "mttr": x["mttr_mediana_s"],
                  "mesmo_elemento": x["mesmo_elemento"], "outro_elemento": x["outro_elemento"]} for x in cura["por_forma"]]
    estrategias = [{"estrategia": x["estrategia"], "gerada": x["gerada"], "passou_estaticas": x["passou_estaticas"], "reexecutada": x["reexecutada"], "aplicada": x["aplicada"],
                    "recusada_em": x["recusada_em"]} for x in cura.get("por_estrategia") or []]
    mais_aplicada = max(estrategias, key=lambda x: x["aplicada"]) if estrategias else None
    pior_modo = min(por_modo, key=lambda x: (x["taxa"] if x["taxa"] is not None else 101, -x["quebrou"])) if por_modo else None
    melhor_modo = max(por_modo, key=lambda x: (x["taxa"] if x["taxa"] is not None else -1, x["quebrou"])) if por_modo else None
    dados_js = {"resumo": {k: r.get(k) for k in ("execucoes", "quebras_detectadas", "nao_quebrou", "curadas", "nao_curadas", "taxa_de_cura_pct", "mesmo_elemento",
                                                 "outro_elemento", "mttr_mediana_s", "mttr_min_s", "mttr_max_s", "repeticoes", "limiar_nome", "formas")},
                "por_modo": por_modo, "por_roteiro": por_roteiro, "por_forma": por_forma, "estrategias": estrategias}
    fh = next((x for x in por_forma if x["forma"] == "harness"), None)
    fp = next((x for x in por_forma if x["forma"] == "php"), None)
    itens_kpi = [
        ("Curadas, pela regra R3 (o roteiro precisa passar)", f'{r["curadas"]} de {r["quebras_detectadas"]}',
         f'{fmt(r["taxa_de_cura_pct"])}% das quebras detectadas; {r["nao_quebrou"]} execuções não quebraram'
         if r["taxa_de_cura_pct"] is not None else f'{r["execucoes"]} execuções; nenhuma quebra detectada'),
        ("Mesmo elemento da referência", f'{r["mesmo_elemento"]} de {r["curadas"]}',
         f'{r["outro_elemento"]} cura(s) com outro elemento que fez o roteiro passar (regra R3, tabela abaixo)'),
        ("Tempo até o resultado (MTTR), mediana", f'{fmt(r["mttr_mediana_s"])} s' if r["mttr_mediana_s"] is not None else "n/d",
         f'da detecção à reexecução validada; entre {fmt(r["mttr_min_s"])} e {fmt(r["mttr_max_s"])} s' if r["mttr_mediana_s"] is not None else "nenhuma cura validada"),
        ("Quebra armada pelo próprio teste contra a variante do PHP", f'{f.get("mesmo_resultado", 0)} de {f.get("celulas_comparadas", 0)} células com o mesmo resultado',
         f'árvore da página igual em {f.get("arvore_igual", 0)} células'
         + (f'; difere em {", ".join(f.get("arvore_diferente") or [])}' if f.get("arvore_diferente") else "")
         + (f'; cura {fmt(fh["taxa"])}% no próprio teste e {fmt(fp["taxa"])}% no PHP' if fh and fp and fh["taxa"] is not None and fp["taxa"] is not None else "")),
        ("Estratégia que mais curou", f'{esc(mais_aplicada["estrategia"])} em {mais_aplicada["aplicada"]}' if mais_aplicada else "n/d",
         "; ".join(f'{esc(x["estrategia"])} {x["aplicada"]}' for x in estrategias if x["aplicada"] and x is not mais_aplicada) or "nenhuma outra estratégia curou"),
        ("Limiar do nome parecido", fmt(r["limiar_nome"]), "o quanto o nome do candidato precisa se parecer; fixado no P4"),
    ]
    tab_modo = tabela(["Modo de quebra", "Execuções", "Quebraram", "Curadas", "Taxa de cura (%)", "Mesmo elemento", "Outro elemento", "Não curadas", "Não quebrou", "MTTR mediana (s)"],
                      [[f"<code>{esc(x['modo'])}</code>", x["execucoes"], x["quebrou"], x["curadas"], fmt(x["taxa"]) if x["taxa"] is not None else "n/d", x["mesmo_elemento"], x["outro_elemento"],
                        x["nao_curadas"], x["nao_quebrou"], fmt(x["mttr"]) if x["mttr"] is not None else "n/d"] for x in por_modo], raw=True)
    tab_roteiro = tabela(["Roteiro", "Execuções", "Quebraram", "Curadas", "Taxa de cura (%)", "Mesmo elemento", "Outro elemento", "Não curadas", "Não quebrou", "MTTR mediana (s)"],
                         [[f"<code>{esc(x['roteiro'])}</code>", x["execucoes"], x["quebrou"], x["curadas"], fmt(x["taxa"]) if x["taxa"] is not None else "n/d", x["mesmo_elemento"], x["outro_elemento"],
                           x["nao_curadas"], x["nao_quebrou"], fmt(x["mttr"]) if x["mttr"] is not None else "n/d"] for x in por_roteiro], raw=True)
    tab_forma = tabela(["Forma da quebra", "Quebraram", "Curadas", "Taxa de cura (%)", "Mesmo elemento", "Outro elemento", "MTTR mediana (s)"],
                       [[esc(x["forma"]), x["quebrou"], x["curadas"], fmt(x["taxa"]) if x["taxa"] is not None else "n/d", x["mesmo_elemento"], x["outro_elemento"],
                         fmt(x["mttr"]) if x["mttr"] is not None else "n/d"] for x in por_forma], raw=True)
    verifs = ["resolve_um_elemento", "visivel_e_habilitado", "mesmo_papel", "nome_parecido", "efeito_na_reexecucao"]
    tab_estr = tabela(["Estratégia", "Gerada", "Passou as estáticas", "Reexecutada", "Aplicada (curou)"] + [f"Recusada em {v}" for v in verifs],
                      [[f"<code>{esc(x['estrategia'])}</code>", x["gerada"], x["passou_estaticas"], x["reexecutada"], x["aplicada"]] + [x["recusada_em"].get(v, 0) for v in verifs]
                       for x in estrategias], raw=True)
    tab_outro = tabela(["Execução", "Roteiro", "Modo", "Forma", "Estratégia", "Seletor curado", "MTTR (s)"],
                       [[f"<code>{esc(x['id'])}</code>", esc(x["roteiro"]), f"<code>{esc(x['modo'])}</code>", esc(x["forma"]), f"<code>{esc(x['aplicado'])}</code>",
                         f"<code>{esc(x['seletor_curado'])}</code>", fmt(x["mttr_s"]) if x.get("mttr_s") is not None else "n/d"] for x in cura.get("outro_elemento") or []], raw=True)
    tab_nao = tabela(["Execução", "Roteiro", "Modo", "Forma", "Falha", "Reexecuções"],
                     [[f"<code>{esc(x['id'])}</code>", esc(x["roteiro"]), f"<code>{esc(x['modo'])}</code>", esc(x["forma"]), f"<code>{esc(x.get('falha') or '')}</code>", x["reexecucoes"]]
                      for x in cura.get("nao_curadas") or []], raw=True)
    tab_exec = tabela(["Execução", "Localizador", "Quebrou", "Curada", "Estratégia", "Seletor curado", "Mesmo elemento", "MTTR (s)", "Reexecuções"],
                      [[f"<code>{esc(x['id'])}</code>", f"<code>{esc(x['localizador'])}</code>", "sim" if x["quebrou"] else "não", "sim" if x["curado"] else "não",
                        f"<code>{esc(x['aplicado'])}</code>" if x.get("aplicado") else "", f"<code>{esc(x['seletor_curado'])}</code>" if x.get("seletor_curado") else "",
                        {True: "sim", False: "não"}.get(x["mesmo_elemento"], "n/d"), fmt(x["mttr_s"]) if x.get("mttr_s") is not None else "n/d", x["reexecucoes"]]
                       for x in cura.get("execucoes") or []], raw=True)
    lead = (f'{"Sim" if r["taxa_de_cura_pct"] is not None and r["taxa_de_cura_pct"] >= 50 else "Não"}, na medida da corrida 19: de {r["quebras_detectadas"]} quebras detectadas em '
            f'{r["execucoes"]} execuções (quatro roteiros do front legado, quatro modos de quebra, {len(r.get("formas") or [])} formas, {r["repeticoes"]} repetições), '
            f'{r["curadas"]} foram curadas pela regra R3 ({fmt(r["taxa_de_cura_pct"]) if r["taxa_de_cura_pct"] is not None else "n/d"}%), {r["mesmo_elemento"]} com o mesmo elemento da referência e '
            f'{r["outro_elemento"]} com outro elemento que fez o roteiro passar; o MTTR do agente, da detecção à reexecução validada, tem mediana de '
            f'{fmt(r["mttr_mediana_s"]) if r["mttr_mediana_s"] is not None else "n/d"} s. '
            + (f'O modo mais curado é <code>{esc(melhor_modo["modo"])}</code> ({fmt(melhor_modo["taxa"])}%) e o menos, <code>{esc(pior_modo["modo"])}</code> ({fmt(pior_modo["taxa"]) if pior_modo["taxa"] is not None else "n/d"}%). '
               if melhor_modo and pior_modo else "")
            + (f'As duas formas de quebra dão o mesmo resultado em {f.get("mesmo_resultado", 0)} das {f.get("celulas_comparadas", 0)} células comparadas.' if f.get("celulas_comparadas") else ""))
    leitura_ = leitura([
        f"<strong>Regra R3.</strong> Só conta como cura a reexecução em que o roteiro inteiro passa com o candidato no lugar do localizador: {r['curadas']} de {r['quebras_detectadas']} "
        f"(bloco <code>tb_f4_cura_resumo</code>); {r['outro_elemento']} dessas passaram com outro elemento, listado na tabela própria, e {r['nao_curadas']} não foram curadas.",
        (f"<strong>Por modo de quebra.</strong> <code>{esc(melhor_modo['modo'])}</code> cura {melhor_modo['curadas']} de {melhor_modo['quebrou']} e <code>{esc(pior_modo['modo'])}</code> "
         f"{pior_modo['curadas']} de {pior_modo['quebrou']} (bloco <code>tb_f4_cura_por_modo</code>): é onde a geração em código mais falha." if melhor_modo and pior_modo else "<strong>Por modo.</strong> Sem dados."),
        (f"<strong>Estratégias.</strong> <code>{esc(mais_aplicada['estrategia'])}</code> é a que mais levou o roteiro ao fim ({mais_aplicada['aplicada']} vezes); a tabela de estratégias diz em que "
         f"verificação cada uma foi recusada (bloco <code>tb_f4_cura_estrategias</code>)." if mais_aplicada else "<strong>Estratégias.</strong> Sem dados."),
        (f"<strong>Quebra armada pelo próprio teste contra a variante do PHP (decisão 80).</strong> A árvore da página quebrada é a mesma nas duas formas em {f.get('arvore_igual', 0)} das {f.get('celulas_comparadas', 0)} células e o "
         f"resultado é o mesmo em {f.get('mesmo_resultado', 0)}" + (f"; taxa de cura {fmt(fh['taxa'])}% no próprio teste e {fmt(fp['taxa'])}% no PHP" if fh and fp and fh["taxa"] is not None and fp["taxa"] is not None else "")
         + " (blocos <code>tb_f4_cura_formas</code> e <code>tb_f4_cura_por_forma</code>)."),
        f"<strong>Tempo até o resultado (MTTR).</strong> Mediana de {fmt(r['mttr_mediana_s']) if r['mttr_mediana_s'] is not None else 'n/d'} s, entre {fmt(r['mttr_min_s']) if r['mttr_min_s'] is not None else 'n/d'} e "
        f"{fmt(r['mttr_max_s']) if r['mttr_max_s'] is not None else 'n/d'} s: é a primeira medida de MTTR só do agente, sem linha de base manual (a linha de base é a Fase 5).",
        "<strong>Limitação declarada.</strong> A quebra é armada, não ocorrida; cada célula usa, no passo do alvo, o estilo de localizador que o modo quebra (por id, por classe, por texto ou "
        "por caminho na estrutura), e a mudança de texto acrescenta uma palavra; um sinônimo ficaria abaixo do limiar do nome.",
    ])
    html_ = f'''<section id="cura" hidden>
<h1>Cura de seletor: quando o localizador quebra, o agente acha outro em código e o roteiro passa?</h1>
<p class="lead">{lead}</p>
{kpis(itens_kpi)}
<h2>Cura por modo de quebra</h2>
<p>Cada barra empilha as execuções do modo: curadas com o mesmo elemento da referência, curadas com outro elemento (regra R3), não curadas e as que não quebraram (o localizador sobreviveu à mutação).</p>
<div class="chart"><canvas id="g-cura-modo"></canvas></div>
{tab_modo}
<h2>Cura por roteiro e tempo até o resultado (MTTR)</h2>
<p>As mesmas contagens por roteiro do front legado; o tempo é a mediana, em segundos, da detecção à reexecução validada.</p>
<div class="chart"><canvas id="g-cura-roteiro"></canvas></div>
{tab_roteiro}
<h2>As duas formas da quebra</h2>
{tab_forma}
{detalhes("O que cada estratégia de candidato rendeu", tab_estr)}
{detalhes(f"Curas com outro elemento ({len(cura.get('outro_elemento') or [])})", tab_outro)}
{detalhes(f"Execuções não curadas ({len(cura.get('nao_curadas') or [])})", tab_nao)}
{detalhes(f"Execução a execução ({len(cura.get('execucoes') or [])})", tab_exec)}
<h2>A corrida no roadmap</h2>
{cartoes_corridas(road, numeros=["19"], sufixo="-cura")}
{leitura_}
{fontes_}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ Fase 4: biblioteca em produção e ciclo de correção (corrida 20)

# ! Alteração de IA - Revisar: (03/11/2026, Fase 4, pacote P5) a aba "Biblioteca em produção", lida de
# resultados_alvo/fase4/biblioteca.json (avaliar_fase4.py --biblioteca): o lote, o que cada filtro barrou, a regra R5 nos
# inéditos, a regra R4 no ciclo de correção, a sonda repetida com recuperação por id e a recuperação dos verbetes aprendidos.
# ! Motivo: regra do painel (uma aba por análise, números só dos JSON); a corrida 20 é a quinta análise da Fase 4.
def secao_biblioteca(bibl: dict | None, road: dict, cartoes_corridas) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões e itens de leitura à vista reescritos sem b = / c = e sem p; a regra R5 passa a dizer "N passaram a acertar e M passaram a errar".
    # ! Motivo: o texto à vista trazia b e c soltos, que o Eric pediu para tirar; os mesmos números aparecem agora na frase, e o teste de painel confere a frase nova.
    fontes_ = fontes(["<code>resultados_alvo/fase4/biblioteca.json</code> e <code>.md</code> (<code>avaliar_fase4.py --biblioteca</code>, com <code>--check</code>; blocos <code>tb_f4_biblioteca_*</code>)",
                      "<code>executar_fase4.py --modo biblioteca</code> (<code>biblioteca_fase4.py</code>: os 13 filtros em código da decisão 65, a operação de correção, a recuperação por id, a regra R5; "
                      "<code>sonda_correcao.py --recuperacao-por-id</code>; relatórios v2 por caso em <code>fase4_biblioteca/relatorios/</code>)",
                      "roadmap §2.12 e §4.2; plano aprovado da Fase 4, seções 3.7, 5 (regras R4 e R5) e 6; fichas 32 e 26; decisão 65"])
    vazio = {"resumo": None, "filtros": [], "reavaliacao": None, "correcao": None}
    if not bibl or not bibl.get("resumo") or not bibl["resumo"].get("casos"):
        html_ = f'''<section id="biblioteca" hidden>
<h1>Biblioteca em produção: o que o agente propõe passa pelos filtros, melhora os inéditos e o ciclo de correção marca o que foi corrigido?</h1>
<p class="lead">A corrida 20 ainda não foi rodada nesta máquina: falta <code>resultados_alvo/fase4/biblioteca.json</code>, gerado por <code>avaliar_fase4.py --biblioteca</code> depois de <code>executar_fase4.py --modo biblioteca --saida fase4_biblioteca</code> (pacote P5 do plano aprovado, com modelo, noite C).</p>
{cartoes_corridas(road, numeros=["20"], sufixo="-bib")}
{fontes_}
</section>'''
        return vazio, html_
    r = bibl["resumo"]
    lote = bibl.get("lote") or {}
    reav = bibl.get("reavaliacao")
    corr = bibl.get("correcao")
    sonda = bibl.get("sonda")
    rec_ = bibl.get("recuperacao") or {}
    filtros_ = [{"filtro": x["filtro"], "recusas": x["recusas"]} for x in bibl.get("filtros") or []]
    mais_barra = max(filtros_, key=lambda x: x["recusas"]) if filtros_ and any(x["recusas"] for x in filtros_) else None
    sem_rec = rec_.get("aprendidos_sem_recuperacao") or []
    dados_js = {"resumo": {k: r.get(k) for k in ("casos", "da_tela", "do_fixture", "acertos_diagnostico", "acerto_pct", "propostas", "aceitas", "abstencoes", "para_revisao",
                                                 "recusadas_p5", "recusadas_fase3", "inferencias", "segundos")},
                "filtros": filtros_, "reavaliacao": ({k: reav.get(k) for k in ("n", "b", "c", "acerto_base_pct", "acerto_novo_pct", "veredito", "p_mcnemar")} if reav else None),
                "correcao": ({k: corr.get(k) for k in ("universo", "desligados", "marcados", "acertos", "falsos_positivos", "perdidos", "precisao_pct", "revocacao_pct", "kappa")} if corr else None)}
    itens_kpi = [
        ("Edições no lote", f'{r["aceitas"]} de {r["propostas"]}',
         f'propostas nos {r["casos"]} casos de aprendizado; em {r["abstencoes"]} o modelo respondeu NENHUMA (sem proposta)'),
        ("Barradas e seguradas", f'{r["recusadas_p5"] + r["para_revisao"]} pelos filtros do P5',
         f'{r["recusadas_p5"]} recusadas pelos 13 filtros em código; {r["para_revisao"]} seguradas para revisão humana'),
        ("Regra R5: o lote melhora os inéditos?", f'{reav["veredito"]}: {reav["b"]} passaram a acertar, {reav["c"]} a errar' if reav else "não medida",
         f'acerto {fmt(reav["acerto_base_pct"])}% com a cópia curada e {fmt(reav["acerto_novo_pct"])}% com o lote, nos {reav["n"]} inéditos pareados' if reav else "sem reavaliação"),
        ("Regra R4, ciclo de correção", f'precisão {fmt(corr["precisao_pct"])}%, revocação {fmt(corr["revocacao_pct"])}%' if corr and corr.get("precisao_pct") is not None else
         (f'{corr["marcados"]} marcada(s) de {corr["desligados"]} desligado(s)' if corr else "não medida"),
         f'{corr["marcados"]} marcada(s) como corrigido em {corr["universo"]} casos; {corr["acertos"]} certa(s), {corr["falsos_positivos"]} sem razão, {corr["perdidos"]} perdida(s)' if corr else "sem ciclo de correção"),
        ("Sonda com recuperação por id", f'{sonda["mudaram_proposta"]} de {sonda["casos"] - sonda["sem_sonda_anterior"]} mudaram a proposta' if sonda and sonda["casos"] > sonda["sem_sonda_anterior"] else (f'{sonda["casos"]} casos' if sonda else "não repetida"),
         f'{sonda["mencionam_correcao"]} mencionam a correção; {sonda["abstencoes"]} NENHUMA; {sonda["com_verbete_por_id"]} com verbete pelo id; {sonda["sem_sonda_anterior"]} sem sonda anterior' if sonda else "a sonda de 28/09 não foi repetida"),
        ("Verbetes aprendidos (ficha 32)", f'{len(sem_rec)} de {len(rec_.get("aprendidos_na_calibracao") or {})} nunca recuperados',
         f'na calibração com k = {r.get("k")}; nesta corrida {rec_.get("casos_com_verbete_por_id", 0)} caso(s) receberam verbete pelo id'),
    ]
    tab_filtros = tabela(["Filtro em código (decisão 65)", "Propostas barradas ou seguradas"], [[f"<code>{esc(x['filtro'])}</code>", x["recusas"]] for x in filtros_], raw=True)
    tab_lote = tabela(["Verbete", "Operação", "Caso", "Peso", "Granularidade"],
                      [[f"<code>{esc(e['verbete'])}</code>", esc(e["operacao"]), f"<code>{esc(e['caso'])}</code>", e.get("peso"), esc(e.get("granularidade") or "")] for e in lote.get("lista") or []], raw=True)
    tab_rev = tabela(["Verbete", "Operação", "Caso", "Peso"], [[f"<code>{esc(e['verbete'])}</code>", esc(e["operacao"]), f"<code>{esc(e['caso'])}</code>", e.get("peso")] for e in lote.get("revisao") or []], raw=True)
    tab_corr = tabela(["Caso", "Modo", "Verbetes", "Modo desligado", "Reproduziu antes", "Passou depois", "Fio mudou", "Árvore mudou", "Marcado", "Motivo"],
                      [[f"<code>{esc(c['caso'])}</code>", f"<code>{esc(c['modo'])}</code>", ", ".join(f"<code>{esc(v)}</code>" for v in c.get("verbetes") or []), "sim" if c["desligado"] else "não",
                        "sim" if c["reproduziu_antes"] else "não", "sim" if c["passou_depois"] else "não", "sim" if c["ha_diff_http"] else "não", "sim" if c["ha_diff_arvore"] else "não",
                        "sim" if c["marcado"] else "não", esc(c.get("motivo") or "")] for c in (corr or {}).get("por_caso") or []], raw=True)
    tab_sonda = tabela(["Caso", "Rótulo agora", "Acertou", "Propostas", "Aceitas", "NENHUMA", "Motivos", "Menciona a correção", "Verbetes pelo id", "Rótulo em 28/09", "Propostas em 28/09", "Mudou"],
                       [[f"<code>{esc(x['caso'])}</code>", esc(x["rotulo"] or ""), "sim" if x["acertou"] else "não", x["n_propostas"], x["n_aceitas"], "sim" if x["abstencao"] else "não",
                         ", ".join(f"<code>{esc(m)}</code>" for m in x["motivos"]) or "nenhum", "sim" if x["menciona_correcao"] else "não", ", ".join(f"<code>{esc(v)}</code>" for v in x["por_id"]) or "nenhum",
                         esc(x["rotulo_anterior"] or "n/d"), x["n_propostas_anterior"] if x["n_propostas_anterior"] is not None else "n/d",
                         "sem sonda anterior" if x["mudou_proposta"] is None else ("sim" if x["mudou_proposta"] else "não")] for x in (sonda or {}).get("por_caso") or []], raw=True)
    tab_rec = tabela(["Verbete aprendido", f"Vezes na calibração (k = {r.get('k')})", "Vezes pelo id nesta corrida"],
                     [[f"<code>{esc(v)}</code>", n, (rec_.get("verbetes_por_id") or {}).get(v, 0)] for v, n in sorted((rec_.get("aprendidos_na_calibracao") or {}).items())], raw=True)
    tab_casos = tabela(["Caso", "Origem", "Rótulo", "Acertou", "Selo", "Propostas", "Aceitas", "Para revisão", "Recusadas", "NENHUMA", "Pelo id", "Verbetes editados"],
                       [[f"<code>{esc(c['caso'])}</code>", esc(c["origem"] or ""), esc(c["rotulo"] or ""), "sim" if c["acertou"] else "não", esc(c["selo"] or ""), c["n_propostas"], c["n_aceitas"], c["para_revisao"],
                         ", ".join(f"<code>{esc(m)}</code>" for m in c.get("recusadas") or []), "sim" if c["abstencao"] else "não", ", ".join(f"<code>{esc(v)}</code>" for v in c.get("recuperacao_por_id") or []),
                         ", ".join(f"<code>{esc(v)}</code>" for v in c.get("verbetes_editados") or [])] for c in bibl.get("casos") or []], raw=True)
    lead = (f'Na corrida 20, o modelo propôs {r["propostas"]} edições nos {r["casos"]} casos de aprendizado e {r["aceitas"]} entraram no lote; os filtros em código barraram {r["recusadas_p5"]} e '
            f'seguraram {r["para_revisao"]} para revisão humana (o validador da Fase 3 recusou {r["recusadas_fase3"]} antes). '
            + (f'Nos {reav["n"]} inéditos, o lote {"entra" if reav["veredito"] == "aceito" else "fica em espera"} pela regra R5: b = {reav["b"]} passaram a acertar e c = {reav["c"]} passaram a errar '
               f'({fmt(reav["acerto_base_pct"])}% para {fmt(reav["acerto_novo_pct"])}% de acerto). ' if reav else "A regra R5 não foi medida. ")
            + (f'No ciclo de correção, a marca corrigido teve precisão {fmt(corr["precisao_pct"])}% e revocação {fmt(corr["revocacao_pct"])}% contra os {corr["desligados"]} casos com o modo desligado (regra R4). '
               if corr and corr.get("precisao_pct") is not None else (f'No ciclo de correção, {corr["marcados"]} de {corr["desligados"]} casos desligados foram marcados. ' if corr else ""))
            + (f'Na sonda repetida com recuperação por id, {sonda["mudaram_proposta"]} caso(s) mudaram a proposta em relação a 28/09 e {sonda["mencionam_correcao"]} mencionam a correção registrada.' if sonda else ""))
    leitura_ = leitura([
        f"<strong>Lote e filtros.</strong> {r['aceitas']} edições entraram (peso {lote.get('peso', 0)}); "
        + (f"o filtro que mais barrou foi <code>{esc(mais_barra['filtro'])}</code> ({mais_barra['recusas']})" if mais_barra else "nenhum filtro do P5 barrou proposta")
        + f" (blocos <code>tb_f4_biblioteca_filtros</code> e <code>tb_f4_biblioteca_rejeicoes</code>); {r['abstencoes']} abstenções contam como saída válida.",
        (f"<strong>Regra R5.</strong> Nos {reav['n']} inéditos, {reav['b']} passaram a acertar e {reav['c']} passaram a errar: {reav['veredito']} (bloco <code>tb_f4_biblioteca_reavaliacao</code>); a base é {esc(reav.get('origem_da_base') or 'n/d')}."
         if reav else "<strong>Regra R5.</strong> Não medida."),
        (f"<strong>Regra R4.</strong> {corr['marcados']} marcadas, {corr['acertos']} certas, {corr['falsos_positivos']} marcadas sem razão e {corr['perdidos']} perdidas em {corr['universo']} casos com sintoma antes "
         f"(bloco <code>tb_f4_biblioteca_correcao</code>); concordância além do acaso (kappa) {fmt(corr['kappa'], 3) if corr.get('kappa') is not None else 'n/d'}." if corr else "<strong>Regra R4.</strong> Não medida."),
        (f"<strong>Sonda.</strong> {sonda['casos']} casos reapresentados com os verbetes do próprio caso no contexto: {sonda['mudaram_proposta']} mudaram a proposta, {sonda['mencionam_correcao']} mencionam a correção, "
         f"{sonda['abstencoes']} abstiveram-se (bloco <code>tb_f4_biblioteca_sonda</code>)." if sonda else "<strong>Sonda.</strong> Não repetida."),
        f"<strong>Ficha 32.</strong> {len(sem_rec)} verbetes aprendidos nunca entraram num contexto da calibração ({', '.join(f'<code>{esc(v)}</code>' for v in sem_rec) or 'nenhum'}); "
        "a decisão da ficha os manda para <code>aprendidos_em_espera/</code> (<code>biblioteca_fase4.py --espera</code>, comando do Eric).",
        "<strong>O que não muda sozinho.</strong> A biblioteca de produção só recebe o lote por <code>biblioteca_fase4.py --promover</code>, depois da planilha de revisão humana preenchida (porta final da decisão 65).",
    ])
    html_ = f'''<section id="biblioteca" hidden>
<h1>Biblioteca em produção: o que o agente propõe passa pelos filtros, melhora os inéditos e o ciclo de correção marca o que foi corrigido?</h1>
<p class="lead">{lead}</p>
{kpis(itens_kpi)}
<h2>O que cada filtro barrou</h2>
<p>Os 13 filtros em código da decisão 65, na ordem fixa; a regra dos 40% segura (não recusa) a nota em verbete presente em 40% ou mais dos contextos da calibração.</p>
<div class="chart"><canvas id="g-bib-filtros"></canvas></div>
{tab_filtros}
<h2>Regra R5: o lote nos inéditos</h2>
<div class="chart"><canvas id="g-bib-reavaliacao"></canvas></div>
{detalhes(f"Edições do lote ({lote.get('edicoes', 0)})", tab_lote)}
{detalhes(f"Seguradas para revisão humana ({lote.get('para_revisao', 0)})", tab_rev)}
<h2>Regra R4: o ciclo de correção</h2>
{tab_corr}
<h2>A sonda de 28/09 repetida com recuperação por id</h2>
{tab_sonda}
{detalhes("Verbetes aprendidos: recuperação na calibração e pelo id", tab_rec)}
{detalhes(f"Caso a caso ({len(bibl.get('casos') or [])})", tab_casos)}
<h2>A corrida no roadmap</h2>
{cartoes_corridas(road, numeros=["20"], sufixo="-bib")}
{leitura_}
{fontes_}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ Fase 4: ensaio dos cenários da Fase 5 (corrida 21)

# ! Alteração de IA - Revisar: (04/11/2026, Fase 4, pacote P6) a aba "Cenários da Fase 5", lida de
# resultados_alvo/fase4/cenarios.json (avaliar_fase4.py --cenarios): Task Success com intervalo de Wilson e MTTR com intervalo
# por reamostragem, no geral, por tipo e por cenário, a ficha da falha de cada cenário (o que a detecção acusou), o tempo por
# execução com a estimativa da Fase 5 e o protocolo da linha de base manual.
# ! Motivo: regra do painel (uma aba por análise, números só dos JSON); a corrida 21 é a sexta análise da Fase 4, e a ficha da
# falha de cada cenário é o que o protocolo da linha de base manual entrega ao integrante.
# ! Alteração de IA - Revisar: (04/11/2026, corrida 21b) secao_cenarios recebe também a leitura da repetição (cenarios_v2.json): com ela, os
# números principais são os da 21b, o gráfico do MTTR mostra as duas corridas, entra a tabela "As duas corridas" e a execução sem Task
# Success aparece com o nome da corrida.
# ! Motivo: a 21b roda com a correção da cura e é a leitura vigente do ensaio; a 21 é o registro de como o defeito apareceu, e o painel,
# onde o Eric decide, tem de mostrar as duas, como a aba "Tela e fixture" faz com as corridas 18 e 18b.
# ! Alteração de IA - Revisar: (05/11/2026, decisão 90) secao_cenarios recebe também a leitura da 21c (cenarios_v3.json): os cartões e os gráficos passam a ela, e a comparação cenário a cenário é contra a 21b.
# ! Motivo: a 21c e a 21b só diferem no tamanho do prompt, com a mesma versão do Ollama e a mesma biblioteca: é a comparação que mede o corte.
# ! Alteração de IA - Revisar: (06/11/2026, decisão 97) secao_cenarios recebe também a leitura da 21d (cenarios_v4.json), e a comparação cenário a cenário é contra a 21c.
# ! Motivo: da 21c para a 21d só mudou a busca; é essa comparação que diz se os sinais novos mexeram nos dez cenários da Fase 5.
def secao_cenarios(cen_: dict | None, cen_v2: dict | None, road: dict, cartoes_corridas, cen_v3: dict | None = None, cen_v4: dict | None = None) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões, títulos e itens de leitura à vista reescritos com "chegou ao resultado (Task Success)" e "tempo até o resultado (MTTR)", sem Wilson nem reamostragem.
    # ! Motivo: o texto à vista trazia siglas e nomes de método estatístico que o Eric pediu para tirar; o título "Execuções sem Task Success" passou a "Execuções que não chegaram ao resultado" e o teste do painel foi ajustado.
    protocolo = ("<p>A linha de base manual da Fase 5 segue o protocolo em <code>Documentacao/memorial/5-metodo-e-ferramental/protocolo-linha-de-base-manual.md</code>: "
                 "três integrantes, cada um nos dez cenários numa ordem sorteada com semente fixa, com a falha ligada pelo ajudante "
                 "<code>linha_de_base_manual.py</code> (as mesmas funções da corrida) e a planilha <code>planilha-linha-de-base-manual.csv</code>.</p>")
    fontes_ = fontes([("<code>resultados_alvo/fase4/cenarios.json</code> e <code>.md</code> (<code>avaliar_fase4.py --cenarios</code>, com <code>--check</code>; blocos <code>tb_f4_cenarios_*</code>); "
                       "a repetição com a correção da cura em <code>cenarios_v2.json</code> (<code>--nome cenarios_v2</code>) a repetição com o prompt dentro do limite em <code>cenarios_v3.json</code> (<code>--nome cenarios_v3</code>) e a repetição com os sinais novos da busca em <code>cenarios_v4.json</code> (<code>--nome cenarios_v4</code>)"),
                      ("<code>executar_fase4.py --modo cenarios</code> (catálogo <code>cenarios_fase4.CENARIOS_DO_ENSAIO</code>; cronômetro <code>mttr_monotonico</code>; "
                       "conferência do diagnóstico <code>diagnostico_conferido</code>; relatórios v2 por execução em <code>fase4_ensaio/relatorios/</code>, <code>fase4_ensaio_v2/relatorios/</code>, <code>fase4_ensaio_v3/relatorios/</code> e <code>fase4_ensaio_v4/relatorios/</code>)"),
                      "protocolo da linha de base manual; roadmap §2.13, §2.14, §2.17 e §2.20 (corridas 21, 21b, 21c e 21d); plano aprovado da Fase 4, seções 3.9 e 5 (P6); fichas 35, 36, 42 e 47, decisões 79, 90 e 97"])
    vazio = {"geral": None, "por_tipo": [], "por_cenario": []}
    if not cen_ or not (cen_.get("geral") or {}).get("n"):
        html_ = f'''<section id="cenarios" hidden>
<h1>Cenários da Fase 5: quanto tempo o agente leva da detecção ao resultado e em quantos cenários acerta?</h1>
<p class="lead">A corrida 21 ainda não foi rodada nesta máquina: falta <code>resultados_alvo/fase4/cenarios.json</code>, gerado por <code>avaliar_fase4.py --cenarios</code> depois de <code>rodar_fase4.ps1 -Modo cenarios -Saida fase4_ensaio -Repeticoes 1</code> (pacote P6 do plano aprovado, com modelo, de dia).</p>
{protocolo}
{cartoes_corridas(road, numeros=["21", "21b", "21c", "21d"], sufixo="-cen")}
{fontes_}
</section>'''
        return vazio, html_
    corridas_cen = [(n_, c_) for n_, c_ in (("21", cen_), ("21b", cen_v2), ("21c", cen_v3), ("21d", cen_v4)) if c_ and (c_.get("geral") or {}).get("n")]
    por_nome_cen = dict(corridas_cen)
    nome_vig, cen_ = corridas_cen[-1]
    nome_ant, anterior = corridas_cen[-2] if len(corridas_cen) > 1 else (None, None)
    ROTULOS_DA_CORRIDA = {"21": "corrida 21", "21b": "corrida 21b, prompt acima do limite" if nome_vig == "21c" else "corrida 21b, com a correção da cura", "21c": "corrida 21c, prompt dentro do limite", "21d": "corrida 21d, com os sinais novos da busca"}
    ARQUIVO_DA_CORRIDA = {"21": "cenarios.md", "21b": "cenarios_v2.md", "21c": "cenarios_v3.md", "21d": "cenarios_v4.md"}
    antes = {x["cenario"]: x for x in (anterior or {}).get("por_cenario") or []}
    g, t = cen_["geral"], cen_.get("tempo") or {}
    cond, det = cen_.get("condicoes") or {}, cen_.get("deteccao") or {}
    nav, banco = cen_.get("navegador") or {}, cen_.get("banco") or {}
    por_tipo = {x["tipo"]: x for x in cen_.get("por_tipo") or []}

    def nd(v, casas: int = 1) -> str:
        return "n/d" if v is None else fmt(v, casas)

    def ts(x: dict) -> str:
        return f'{x["sucessos"]} de {x["n"]}'

    def faixa(lo, hi, unidade: str) -> str:
        return "sem intervalo" if lo is None else f"{nd(lo)} a {nd(hi)}{unidade}"

    dados_js = {"geral": {k: g.get(k) for k in ("n", "sucessos", "task_success_pct", "mttr_media_s")},
                "por_tipo": [{k: x.get(k) for k in ("tipo", "n", "sucessos", "mttr_media_s")} for x in cen_.get("por_tipo") or []],
                "por_cenario": [{**{k: x.get(k) for k in ("cenario", "tipo", "n", "sucessos", "mttr_media_s")}, "mttr_anterior": (antes.get(x["cenario"]) or {}).get("mttr_media_s")}
                                for x in cen_.get("por_cenario") or []],
                "duas_corridas": bool(anterior), "rotulo_anterior": ROTULOS_DA_CORRIDA.get(nome_ant), "rotulo_vigente": ROTULOS_DA_CORRIDA.get(nome_vig)}
    itens_kpi = [("Chegou ao resultado (Task Success)", ts(g), f'{nd(g["task_success_pct"])}% das {g["n"]} execuções; margem de incerteza de {faixa(g["wilson_lo_pct"], g["wilson_hi_pct"], "%")}')]
    itens_kpi.append(("Tempo até o resultado (MTTR), média", f'{nd(g["mttr_media_s"])} s', f'margem de incerteza de {faixa(g["mttr_ic_lo_s"], g["mttr_ic_hi_s"], " s")}; mediana {nd(g["mttr_mediana_s"])} s'))
    for tipo, nome in (("contrato", "Contrato (ficha 35)"), ("localizador", "Localizador")):
        if tipo in por_tipo:
            x = por_tipo[tipo]
            itens_kpi.append((nome, ts(x), f'chegaram ao resultado; tempo médio {nd(x["mttr_media_s"])} s ({faixa(x["mttr_ic_lo_s"], x["mttr_ic_hi_s"], " s")})'))
    itens_kpi.append(("Tempo por execução", f'{nd(t.get("segundos_media"))} s', f'{t.get("execucoes")} execuções em {nd(t.get("segundos_total"))} s; a Fase 5 levaria {nd(t.get("estimativa_fase5_h"), 2)} h'))
    itens_kpi.append(("Detecção", f'{sum(det.values())} de {g["n"]}', f'{det.get("conferencia_do_roteiro", 0)} pelo roteiro, {det.get("contrato_no_fio", 0)} pelo fio (regra R1), {det.get("passo_do_localizador", 0)} pelo localizador'))
    tab_tipo = tabela(["Tipo", "Execuções", "Task Success", "Task Success (%)", "Wilson 95% (%)", "MTTR médio (s)", "Reamostragem 95% (s)", "MTTR mediano (s)"],
                      [[esc(x["tipo"]), x["n"], x["sucessos"], nd(x["task_success_pct"]), faixa(x["wilson_lo_pct"], x["wilson_hi_pct"], ""), nd(x["mttr_media_s"]),
                        faixa(x["mttr_ic_lo_s"], x["mttr_ic_hi_s"], ""), nd(x["mttr_mediana_s"])] for x in cen_.get("por_tipo") or []], raw=True)
    # ! Alteração de IA - Revisar: (04/11/2026, leitura da corrida 21) a ficha da falha sai da tabela por cenário para uma tabela própria.
    # ! Motivo: com os dados reais a tabela passava da largura da página e a coluna da ficha, a que o protocolo da linha de base manual usa, ficava fora da vista.
    tab_cen = tabela(["Cenário", "Tipo", "Classe", "Causa esperada", "Execuções", "Task Success", "MTTR médio (s)", "Rótulos do diagnóstico", "Segundos por execução"],
                     [[f"<code>{esc(x['cenario'])}</code>", esc(x["tipo"]), x.get("classe"), f"<code>{esc(x.get('causa_esperada') or '')}</code>", x["n"], x["sucessos"], nd(x["mttr_media_s"]),
                       ", ".join(f"<code>{esc(k)}</code> {v}" for k, v in (x.get("rotulos") or {}).items()), nd(x.get("segundos_media"))] for x in cen_.get("por_cenario") or []], raw=True)
    tab_fichas = tabela(["Cenário", "O que a detecção acusou"],
                        [[f"<code>{esc(x['cenario'])}</code>", esc(" / ".join(x.get("fichas_da_falha") or []) or "n/d")] for x in cen_.get("por_cenario") or []], raw=True)
    # ! Alteração de IA - Revisar: (04/11/2026, leitura da corrida 21) as execuções sem Task Success, com o rótulo e a falha da cura.
    # ! Motivo: na corrida 21 a tabela por cenário só mostrava o zero do login; quem decide pelo painel precisa ver que o diagnóstico acertou
    # e que a cura falhou, e a explicação fica no roadmap, mostrado no cartão da corrida.
    sem_ts = [(n_, x) for n_, c_ in corridas_cen for x in c_.get("sem_task_success") or []]
    bloco_sem = ""
    if sem_ts:
        tab_sem = tabela(["Corrida", "Cenário", "Repetição", "Tipo", "Detectou", "Rótulo do diagnóstico", "Causa esperada", "Falha da cura", "Segundos"],
                         [[n_, f"<code>{esc(x['cenario'])}</code>", x.get("repeticao"), esc(x["tipo"]), "sim" if x.get("detectou") else "não", f"<code>{esc(x.get('rotulo') or 'n/d')}</code>",
                           f"<code>{esc(x.get('causa_esperada') or '')}</code>", f"<code>{esc(x.get('falha_da_cura') or 'n/d')}</code>", nd(x.get("segundos"))] for n_, x in sem_ts], raw=True)
        bloco_sem = f'<h2>Execuções que não chegaram ao resultado (sem Task Success)</h2>\n<p>Bloco <code>tb_f4_cenarios_sem_sucesso</code>; a explicação de cada uma fica no roadmap, no cartão da corrida abaixo.</p>\n{tab_sem}'
    bloco_duas = ""
    itens_duas: list[str] = []
    if anterior:
        por = cen_.get("por_cenario") or []
        mesmo = sum(1 for x in por if (antes.get(x["cenario"]) or {}).get("rotulos") == x.get("rotulos"))
        tab_duas = tabela(["Cenário", "Tipo", f"Task Success {nome_ant}", f"Task Success {nome_vig}", f"MTTR {nome_ant} (s)", f"MTTR {nome_vig} (s)", f"Segundos {nome_ant}", f"Segundos {nome_vig}", "Mesmo rótulo"],
                          [[f"<code>{esc(x['cenario'])}</code>", esc(x["tipo"]), (antes.get(x["cenario"]) or {}).get("sucessos"), x["sucessos"], nd((antes.get(x["cenario"]) or {}).get("mttr_media_s")),
                            nd(x["mttr_media_s"]), nd((antes.get(x["cenario"]) or {}).get("segundos_media")), nd(x.get("segundos_media")),
                            "sim" if (antes.get(x["cenario"]) or {}).get("rotulos") == x.get("rotulos") else "não"] for x in por], raw=True)
        explica = {"21b": "A corrida 21, antes da correção da cura, e a 21b, depois dela", "21c": "A corrida 21b, com o prompt acima do limite, e a 21c, com o prompt dentro dele, na mesma versão do Ollama e com a mesma biblioteca",
                  "21d": "A corrida 21c e a 21d, com os sinais novos da busca, na mesma versão do Ollama e com a mesma biblioteca"}[nome_vig]
        bloco_duas = f'<h2>As duas últimas corridas, cenário a cenário</h2>\n<p>{explica}: blocos <code>tb_f4_cenarios_por_cenario</code> de <code>{ARQUIVO_DA_CORRIDA[nome_ant]}</code> e <code>{ARQUIVO_DA_CORRIDA[nome_vig]}</code>.</p>\n{tab_duas}'
        pcc_ant, pcc_vig = anterior.get("prompt") or {}, cen_.get("prompt") or {}
        if nome_vig == "21d":
            c21b, c21c = por_nome_cen.get("21b"), por_nome_cen.get("21c")
            itens_duas.append(f"<strong>Os sinais novos da busca.</strong> Da 21c para a 21d só mudou a busca. Chegaram ao resultado {ts(anterior['geral'])} e {ts(g)}, com a mesma causa em {mesmo} de {len(por)} cenários. O tempo até o resultado foi de {nd(anterior['geral'].get('mttr_media_s'))} s para {nd(g.get('mttr_media_s'))} s em média, dentro da margem de uma repetição ({faixa(g['mttr_ic_lo_s'], g['mttr_ic_hi_s'], ' s')}), e o maior prompt, de {pcc_ant.get('maximo_da_tela')} para {pcc_vig.get('maximo_da_tela')} tokens, abaixo do limite de {pcc_vig.get('limite_mais_10_pct')}. Os sinais não mudaram os dez cenários: o verbete certo já chegava em quase todos. A explicação está no roadmap, §2.20.")
            if c21b and c21c:
                itens_duas.append(f"<strong>O corte do prompt.</strong> Da 21b para a 21c, o tempo até o resultado caiu de {nd(c21b['geral'].get('mttr_media_s'))} s para {nd(c21c['geral'].get('mttr_media_s'))} s em média, sem mudar nenhuma causa (roadmap, §2.17).")
        else:
            itens_duas = [(f"<strong>O corte do prompt.</strong> Da 21b para a 21c só mudou o tamanho do prompt: os prompts acima do limite de {pcc_vig.get('limite_mais_10_pct')} tokens foram de {len(pcc_ant.get('acima') or [])} para {len(pcc_vig.get('acima') or [])} dos {g['n']}, e o maior foi de {pcc_ant.get('maximo_da_tela')} para {pcc_vig.get('maximo_da_tela')} tokens. "
                       f"O tempo até o resultado caiu de {nd(anterior['geral'].get('mttr_media_s'))} s para {nd(g.get('mttr_media_s'))} s em média, e o tempo por execução, de {nd((anterior.get('tempo') or {}).get('segundos_media'))} s para {nd(t.get('segundos_media'))} s. Chegaram ao resultado {ts(anterior['geral'])} e {ts(g)}, com a mesma causa em {mesmo} de {len(por)} cenários. A corrida 21, antes da correção da cura, teve {ts(corridas_cen[0][1]['geral'])}. A explicação está no roadmap, §2.13, §2.14 e §2.17.")
                      if nome_vig == "21c" else
                      (f"<strong>As duas corridas.</strong> Na corrida 21 chegaram ao resultado {ts(anterior['geral'])} execuções e, na 21b, com os candidatos da cura verificados numa página refeita até o passo que falhou, {ts(g)}. "
                       f"A mesma causa respondida em {mesmo} de {len(por)} cenários. O tempo por execução passou de {nd((anterior.get('tempo') or {}).get('segundos_media'))} s a {nd(t.get('segundos_media'))} s. A explicação está no roadmap, §2.13 e §2.14.")]
    ct, lc = por_tipo.get("contrato"), por_tipo.get("localizador")
    abertura = (f'Na repetição com os sinais novos da busca (corrida 21d: {cond.get("repeticoes")} repetição dos dez cenários da ficha 36, {esc(cond.get("modelo") or "")}, Ollama {esc(cond.get("versao_ollama") or "n/d")}), '
                f'o agente teve Task Success em {ts(g)} execuções, como na corrida 21c ({ts(anterior["geral"])}), e MTTR médio de ' if nome_vig == "21d" else
                f'Na repetição com o prompt dentro do limite (corrida 21c: {cond.get("repeticoes")} repetição dos dez cenários da ficha 36, {esc(cond.get("modelo") or "")}, Ollama {esc(cond.get("versao_ollama") or "n/d")}), '
                f'o agente teve Task Success em {ts(g)} execuções, como na corrida 21b ({ts(anterior["geral"])}), e MTTR médio de ' if nome_vig == "21c" else
                f'Na repetição do ensaio (corrida 21b: {cond.get("repeticoes")} repetição dos dez cenários da ficha 36, {esc(cond.get("modelo") or "")}, Ollama {esc(cond.get("versao_ollama") or "n/d")}), já com a correção da cura, '
                f'o agente teve Task Success em {ts(g)} execuções, contra {ts(anterior["geral"])} na corrida 21, e MTTR médio de ' if anterior else
                f'No ensaio da corrida 21 ({cond.get("repeticoes")} repetição dos dez cenários da ficha 36, {esc(cond.get("modelo") or "")}, Ollama {esc(cond.get("versao_ollama") or "n/d")}), '
                f'o agente teve Task Success em {ts(g)} execuções e MTTR médio de ')
    lead = (abertura + f'{nd(g["mttr_media_s"])} s da detecção ao fim do cronômetro'
            + (f'; no contrato, {ts(ct)}, e no localizador, {ts(lc)}' if ct and lc else "")
            + f'. Cada execução levou {nd(t.get("segundos_media"))} s em média, o que põe a Fase 5 (dez cenários com cinco repetições) em {nd(t.get("estimativa_fase5_h"), 2)} h de máquina.')
    leitura_ = leitura([
        *itens_duas,
        ("<strong>O que o cronômetro mede.</strong> No contrato (ficha 35), da detecção ao diagnóstico conferido em código (quatro linhas, causa dentro das 23, campo existente no caso), "
         "e chegar ao resultado (Task Success) é acertar a causa e o campo; no localizador, da detecção à reexecução validada, descontada a restauração do banco, e chegar ao resultado é aplicar a cura com o roteiro concluído sem erro."),
        (f"<strong>Condições.</strong> Navegador {', '.join(esc(v) for v in nav.get('versoes') or []) or 'n/d'} em todas as execuções ({'uma versão só' if nav.get('unica') else 'versões diferentes'}); "
         f"banco restaurado e conferido por hash no começo de cada repetição ({'o mesmo hash em todas' if banco.get('unico') else 'hashes diferentes'})."),
        "<strong>Ensaio, não Fase 5.</strong> Uma repetição serve para dimensionar a noite da Fase 5 e conferir o protocolo; as margens de incerteza com uma execução por cenário são largas e não sustentam comparação.",
        "<strong>Linha de base manual.</strong> A coluna \"O que a detecção acusou\" é a ficha da falha que o integrante recebe na sessão, a mesma frase que a detecção do agente acusou.",
    ])
    html_ = f'''<section id="cenarios" hidden>
<h1>Cenários da Fase 5: quanto tempo o agente leva da detecção ao resultado e em quantos cenários acerta?</h1>
<p class="lead">{lead}</p>
{kpis(itens_kpi)}
<h2>Tempo até o resultado (MTTR) por cenário</h2>
<div class="chart"><canvas id="g-cen-mttr"></canvas></div>
<h2>Chegou ao resultado (Task Success), por cenário</h2>
<div class="chart"><canvas id="g-cen-ts"></canvas></div>
{tab_tipo}
{bloco_sem}
{bloco_duas}
<h2>Cenário a cenário</h2>
<p>Blocos <code>tb_f4_cenarios_resumo</code>, <code>tb_f4_cenarios_por_tipo</code>, <code>tb_f4_cenarios_por_cenario</code> e <code>tb_f4_cenarios_tempo</code> de <code>{ARQUIVO_DA_CORRIDA[nome_vig]}</code>.</p>
{tab_cen}
<h2>A ficha da falha de cada cenário</h2>
<p>O que a detecção do agente acusou: a frase que o integrante recebe na sessão da linha de base manual.</p>
{tab_fichas}
<h2>A linha de base manual</h2>
{protocolo}
<h2>As corridas no roadmap</h2>
{cartoes_corridas(road, numeros=["21", "21b", "21c", "21d"], sufixo="-cen")}
{leitura_}
{fontes_}
</section>'''
    return dados_js, html_


# ------------------------------------------------------------------ Fase 4: fechamento da fase (pacote P8)

# ! Alteração de IA - Revisar: (05/11/2026, decisão 91) a aba da corrida 23, lida de `resultados_alvo/fase4/experimento_prompt.json`: o acerto de cada condição contra a corrida 16 e os casos que só um lado acerta.
# ! Motivo: a regra do painel é uma aba por análise, lida dos JSON; o número dos dois itens vai para o TCC e não decide nada na Fase 5, e a aba precisa dizer isso.
def secao_experimento(exp: dict | None, road: dict, cartoes_corridas) -> tuple[dict, str]:
    titulo = "Exemplar e rótulos: um exemplar resolvido ou os rótulos em palavras mudam o acerto?"
    fontes_ = fontes(["<code>resultados_alvo/fase4/experimento_prompt.json</code> e <code>.md</code> (<code>avaliar_fase4.py --experimento_prompt</code>, com <code>--check</code>; blocos <code>tb_f4_exp_*</code>)",
                      "<code>corridas_em_texto.py</code> (as duas condições, como transformação de texto do prompt pronto, conferidas em teste)", "registros da corrida 16 em <code>fase4_calibracao/k3/</code>",
                      "roadmap §2.18; fichas 34 e 43; decisões 55, 79 e 91"])
    if not exp or not exp.get("por_condicao"):
        return {"base": None, "condicoes": []}, (f'<section id="experimento" hidden>\n<h1>{titulo}</h1>\n<p class="lead">A corrida 23 ainda não foi rodada nesta máquina: falta <code>resultados_alvo/fase4/experimento_prompt.json</code>, gerado por '
                                                 f'<code>rodar_fase4.ps1 -Modo experimento_prompt -Saida fase4_experimento</code>.</p>\n{cartoes_corridas(road, numeros=["23"], sufixo="-exp")}\n{fontes_}\n</section>')
    b, conds = exp["base"], exp["por_condicao"]
    nomes = {"exemplar": "Exemplar resolvido", "rotulos_por_extenso": "Rótulos em palavras"}

    def nome_de(x: dict) -> str:
        return nomes.get(x["condicao"], x["condicao"])

    dados_js = {"base": {"acerto_pct": b["acerto_pct"], "avaliacao_pct": b["avaliacao"]["acerto_pct"]},
                "condicoes": [{"nome": nome_de(x), "acerto_pct": x["acerto_pct"], "avaliacao_pct": x["avaliacao"]["acerto_pct"], "b": x["b"], "c": x["c"]} for x in conds]}
    itens_kpi = [("Corrida 16, sem mudança", f'{b["acertos"]} de {b["n"]}', f'{fmt(b["acerto_pct"])}%; nos casos de avaliação, {b["avaliacao"]["acertos"]} de {b["avaliacao"]["n"]}')]
    for x in conds:
        itens_kpi.append((nome_de(x), f'{x["acertos"]} de {x["n"]}', f'{fmt(x["acerto_pct"])}%; só ela acerta em {x["b"]}, só a corrida 16 em {x["c"]}; nos casos de avaliação, {x["avaliacao"]["acertos"]} de {x["avaliacao"]["n"]}'))
    exemplar = next((x for x in conds if x["condicao"] == "exemplar"), None)
    extenso = next((x for x in conds if x["condicao"] == "rotulos_por_extenso"), None)
    fora_extenso = [c for c in exp.get("casos_que_mudaram") or [] if c["condicao"] == "rotulos_por_extenso" and "[" in str(c.get("rotulo_condicao"))]
    tab_resumo = tabela(["Condição", "Casos", "Acertos", "Acerto (%)", "Acurácia balanceada (%)", "Só a condição acerta", "Só a corrida 16 acerta", "p (McNemar)", "Nos casos de avaliação", "Trocas de causa", "Fora da lista", "Tokens de entrada (mediana)", "Segundos (mediana)"],
                        [["corrida 16", b["n"], b["acertos"], fmt(b["acerto_pct"]), fmt(b["acuracia_balanceada_pct"]), "", "", "", f'{b["avaliacao"]["acertos"]} de {b["avaliacao"]["n"]}', "", "", fmt(b["tokens_entrada_mediana"]), fmt(b["segundos_mediana"])]]
                        + [[nome_de(x), x["n"], x["acertos"], fmt(x["acerto_pct"]), fmt(x["acuracia_balanceada_pct"]), x["b"], x["c"], fmt(x["p_mcnemar"], 3), f'{x["avaliacao"]["acertos"]} de {x["avaliacao"]["n"]}', x["trocas_de_rotulo"], x["fora_do_conjunto"] + x["sem_rotulo"],
                            fmt(x["tokens_entrada_mediana"]), fmt(x["segundos_mediana"])] for x in conds])
    tab_mudaram = tabela(["Condição", "Caso", "Gabarito", "Corrida 16", "Na condição", "Efeito"],
                         [[esc(nomes.get(c["condicao"], c["condicao"])), f"<code>{esc(c['caso'])}</code>", f"<code>{esc(c['gabarito'])}</code>", f"<code>{esc(str(c['rotulo_base']))}</code>", f"<code>{esc(str(c['rotulo_condicao']))}</code>", esc(c["efeito"])]
                          for c in exp.get("casos_que_mudaram") or []], raw=True)
    lead = (f'Não dá para dizer que mudam. Nos {b["n"]} casos, a corrida 16 acertou {b["acertos"]} ({fmt(b["acerto_pct"])}%); '
            + "; ".join(f'{nome_de(x).lower()}, {x["acertos"]} ({fmt(x["acerto_pct"])}%), com {x["b"]} casos que só ela acerta e {x["c"]} que só a corrida 16 acerta (p = {fmt(x["p_mcnemar"], 3)})' for x in conds)
            + ". O prompt do agente continua congelado (decisão 91).")
    saldo = "; ".join(f'{nome_de(x)}: {x["b"]} casos a favor e {x["c"]} contra, p = {fmt(x["p_mcnemar"], 3)}' for x in conds)
    nos_36 = ", ".join(f'{nome_de(x).lower()} {x["avaliacao"]["acertos"]}' for x in conds)
    itens_leitura = [f'<strong>Nenhuma das duas condições se separa do acaso.</strong> {saldo}. Nos {b["avaliacao"]["n"]} casos de avaliação, a corrida 16 acertou {b["avaliacao"]["acertos"]}, {nos_36}: diferença de poucos casos, dentro da variação entre corridas iguais.']
    if exemplar:
        itens_leitura.append(f"<strong>O exemplar custa tempo e não puxa a resposta.</strong> Ele leva o prompt de {fmt(b['tokens_entrada_mediana'])} para {fmt(exemplar['tokens_entrada_mediana'])} tokens (medianas). A causa do exemplar, <code>erro_interno_do_servidor</code>, foi respondida {exemplar['causa_do_exemplar_respondida']} vezes, contra {exemplar['causa_do_exemplar_na_base']} na corrida 16: o modelo não copia o exemplo.")
    if extenso:
        forma = extenso.get("forma") or {}
        texto_fora = f" Em <code>{esc(fora_extenso[0]['caso'])}</code> a causa certa veio entre colchetes, com o título do verbete, e conta como fora da lista, como no leitor oficial." if fora_extenso else ""
        itens_leitura.append(f"<strong>O modelo escreve como a lista pede.</strong> Com os rótulos em palavras, {forma.get('por_extenso', 0)} das {extenso['n']} respostas vieram em palavras, e {extenso['fora_do_conjunto']} ficaram fora da lista.{texto_fora} Isso quer dizer que mostrar o nome da causa em palavras a quem lê não pede mudar o prompt: um mapa em código basta.")
    itens_leitura.append("<strong>Cuidado na comparação.</strong> A corrida 16 rodou em outra versão do Ollama, e o tempo não se compara com ela; o acerto, com o que a ponte de versão mostrou, sim. O número vai para o TCC e não muda nada na Fase 5.")
    html_ = f'''<section id="experimento" hidden>
<h1>{titulo}</h1>
<p class="lead">{lead}</p>
{kpis(itens_kpi)}
<h2>Acerto em cada condição</h2>
<p>As duas condições rodaram nos mesmos 90 casos, com a mesma biblioteca e os mesmos três verbetes da corrida 16. Cada uma muda um item só, e o resto do prompt fica igual, byte a byte.</p>
<div class="chart baixo"><canvas id="g-exp-acerto"></canvas></div>
<h2>Os casos que só um lado acerta</h2>
<div class="chart baixo"><canvas id="g-exp-trocas"></canvas></div>
{leitura(itens_leitura)}
{detalhes("Os números de cada condição (bloco tb_f4_exp_resumo)", tab_resumo)}
{detalhes(f"Os casos que mudaram de certo para errado ou o contrário ({len(exp.get('casos_que_mudaram') or [])}; bloco tb_f4_exp_mudaram)", tab_mudaram)}
<h2>A corrida no roadmap</h2>
{cartoes_corridas(road, numeros=["23"], sufixo="-exp")}
{fontes_}
</section>'''
    return dados_js, html_


# ! Alteração de IA - Revisar: (05/11/2026, decisão 92) a aba da conferência dos 36 inéditos, lida de `resultados_alvo/fase4/conferencia_ineditos.json`.
# ! Motivo: o Eric decide pelo painel, e a ficha 46 pede a conferência dele antes da corrida 24; a aba mostra cada caso com o gabarito, o que a corrida 17 viu
# e a pré-análise, sem número nem trecho de caso digitado à mão. Sem gráfico: a leitura aqui é caso a caso.
# ! Alteração de IA - Revisar: (06/11/2026) a aba da corrida 24, lida de `resultados_alvo/fase4/ineditos.json`: o acerto, por classe e por nível, com e sem o verbete certo, o selo e a comparação com a corrida 18e.
# ! Motivo: é a única medida da biblioteca final em casos que ela nunca viu, e o número vai para o TCC; a aba diz também o que ela não mede, porque há uma condição só e os dois conjuntos de casos não são pareados.
def secao_ineditos_f4(ined: dict | None, road: dict, cartoes_corridas, analise3b: dict | None = None) -> tuple[dict, str]:
    fontes_ = fontes(["<code>resultados_alvo/fase4/ineditos.json</code> e <code>.md</code> (<code>avaliar_fase4.py --ineditos</code>, com <code>--check</code>; blocos <code>tb_f4_ineditos_*</code>)",
                      "<code>rodar_fase4.ps1 -Modo ineditos</code> (<code>corridas_em_texto.py</code>; casos em <code>banco_casos_ineditos_fase4.py</code>)",
                      "<code>conferencia_ineditos_respostas.json</code> (a conferência do Eric); roadmap §2.22; decisões 92 e 100; ficha 46"])
    titulo = "Inéditos em texto: a biblioteca final acerta em casos que nunca viu?"
    if not ined or not ined.get("resumo"):
        return {"resumo": None, "por_classe": [], "verbete": None}, (f'''<section id="ineditosf4" hidden>
<h1>{titulo}</h1>
<p class="lead">A corrida 24 ainda não foi rodada nesta máquina: falta <code>resultados_alvo/fase4/ineditos.json</code>, gerado por <code>avaliar_fase4.py --ineditos</code> depois de <code>rodar_fase4.ps1 -Modo ineditos -Saida fase4_ineditos</code>.</p>
{cartoes_corridas(road, numeros=["24"], sufixo="-ined")}
{fontes_}
</section>''')
    r, ref = ined["resumo"], ined.get("referencia") or {}
    v, e = ined["verbete_certo"], ined.get("lado_escrito_18e") or {}
    selos = {x["selo"]: x for x in ined["por_selo"]}
    niveis = {x["nivel"]: x for x in ined["por_nivel"]}
    por_classe = [{"classe": x["classe"], "nome": CLASSES.get(x["classe"], ""), "casos": x["casos"], "acertos": x["acertos"], "erros": x["erros"]} for x in ined["por_classe"]]
    pior = min(por_classe, key=lambda x: x["acertos"] / (x["casos"] or 1))
    erradas = Counter(c["rotulo"] for c in ined["casos"] if not c["acerto"]).most_common(3)
    sem_verbete_erros = sum(1 for c in ined["casos"] if not c["acerto"] and not c["verbete_certo_no_contexto"])
    qwen3b = next((l for l in ((analise3b or {}).get("ineditos") or {}).get("linhas", []) if l["modelo"] == "qwen2.5:7b" and l["biblioteca_epoca"] == 1), None)

    def de(x: dict) -> str:
        return f'{x["acertos"]} de {x["casos"]}'

    tab_casos = tabela(["Caso", "Classe", "Nível", "Gabarito", "Rótulo", "Certo", "Probabilidade", "Selo", "Verbete certo no contexto"],
                       [[f'<code>{esc(c["caso"])}</code>', c["classe"], c["nivel"], f'<code>{esc(c["gabarito"])}</code>', f'<code>{esc(c["rotulo"] or "sem rótulo")}</code>', "sim" if c["acerto"] else "não",
                         fmt(c["p_rotulo"], 3), esc(c.get("selo") or "n/d"), "sim" if c["verbete_certo_no_contexto"] else "não"] for c in ined["casos"]], raw=True)
    tab_nivel = tabela(["Nível", "Casos", "Acertos", "Erros"], [[x["nivel"], x["casos"], x["acertos"], x["erros"]] for x in ined["por_nivel"]])
    itens_kpi = [("Acerto nos inéditos", f'{r["acertos"]} de {r["casos"]}', f'{fmt(r["acerto_pct"])}%; margem de incerteza de {fmt(r["wilson_lo_pct"])} a {fmt(r["wilson_hi_pct"])}%'),
                 ("Nos casos de avaliação", f'{ref.get("acertos")} de {ref.get("casos")}', f'{fmt(ref.get("acerto_pct"))}%; corrida 22, mesma biblioteca; não são os mesmos casos'),
                 ("Com o verbete certo no contexto", de(v["presente"]), f'sem ele, {de(v["ausente"])}; ele chega em {v["presente"]["casos"]} de {r["casos"]}'),
                 (f'Classe mais fraca: {pior["nome"]}', f'{pior["acertos"]} de {pior["casos"]}', "as outras classes ficam de 4 a 6 de 6" if all(x["acertos"] >= 4 for x in por_classe if x is not pior) else "por classe, na tabela"),
                 ("Selo alto", de(selos["alto"]), f'no médio, {de(selos["medio"])}; no baixo, {de(selos["baixo"])}'),
                 ("Lidos duas vezes em texto", f'{e.get("mesmo_rotulo")} de {e.get("casos")}', "com o mesmo rótulo na corrida 18e")]
    lead = (f'Menos que nos casos de avaliação. A biblioteca de produção acerta {r["acertos"]} dos {r["casos"]} inéditos ({fmt(r["acerto_pct"])}%; margem de {fmt(r["wilson_lo_pct"])} a {fmt(r["wilson_hi_pct"])}%), contra {ref.get("acertos")} de {ref.get("casos")} nos casos de avaliação (corrida 22). '
            f'Com o verbete certo no contexto são {de(v["presente"])}; sem ele, {de(v["ausente"])}.')
    leitura_ = leitura([
        '<strong>A diferença não mede só a biblioteca.</strong> São conjuntos diferentes, escritos por autores diferentes, então não há comparação caso a caso.' + (f' O número fica perto do que a Fase 3-B mediu em outros 36 inéditos: {qwen3b["acertos"]} de {qwen3b["n"]} com a primeira biblioteca do mesmo modelo.' if qwen3b else ""),
        f'<strong>O verbete certo pesa de novo.</strong> Em texto ele chega em {v["presente"]["casos"]} dos {r["casos"]} casos, porque os sinais da busca (decisão 97) só existem na tela, e {sem_verbete_erros} dos {r["casos"] - r["acertos"]} erros são de casos sem ele.',
        f'<strong>Onde erra.</strong> {pior["nome"].capitalize()} faz {de(pior)}; o nível 3, feito para enganar, {de(niveis[3])}, contra {de(niveis[1])} no nível 1 e {de(niveis[2])} no nível 2. As respostas erradas mais comuns são ' + ", ".join(f"<code>{esc(a)}</code> ({n})" for a, n in erradas) + ".",
        f'<strong>A repetição bate.</strong> Os {e.get("casos")} casos que a corrida 18e também leu em texto deram o mesmo rótulo em {e.get("mesmo_rotulo")}. Lidos da tela, os mesmos casos fazem {e.get("acertos_tela")}, contra {e.get("acertos_escrito")} em texto: é o efeito dos sinais da busca, e só nos casos que têm tela.',
        f'<strong>O selo.</strong> O alto acerta {de(selos["alto"])}, o médio {de(selos["medio"])} e o baixo {de(selos["baixo"])}, com os limiares da corrida 16: serve de triagem, não de barreira.',
        "<strong>O que esta corrida não diz.</strong> Há uma condição só, a biblioteca final: como estes casos não foram lidos sem biblioteca, ela não diz quanto a biblioteca ajuda neles. A conferência dos casos seguiu as recomendações do Claude, e três tensões ficaram aceitas (decisão 100).",
    ])
    html_ = f'''<section id="ineditosf4" hidden>
<h1>{titulo}</h1>
<p class="lead">{lead}</p>
{kpis(itens_kpi)}
<h2>Acerto por classe de defeito</h2>
<p>Seis casos por classe, lidos em texto, com a biblioteca de produção (corrida 24).</p>
<div class="chart"><canvas id="g-ined-classe"></canvas></div>
<h2>O verbete certo no contexto</h2>
<p>Os casos em que o verbete da causa certa estava entre os três entregues ao modelo e os casos em que não estava.</p>
<div class="chart baixo"><canvas id="g-ined-verbete"></canvas></div>
{leitura_}
{detalhes(f"Caso a caso ({r['casos']} casos)", tab_casos)}
{detalhes("Por nível", tab_nivel)}
<h2>A corrida no roadmap</h2>
{cartoes_corridas(road, numeros=["24"], sufixo="-ined")}
{fontes_}
</section>'''
    return {"resumo": {k: r.get(k) for k in ("casos", "acertos", "acerto_pct", "wilson_lo_pct", "wilson_hi_pct")}, "por_classe": por_classe, "verbete": v}, html_


# ! Alteração de IA - Revisar: (06/11/2026, decisão 100) a aba lê também as respostas do Eric: cada caso ganha a resposta, e os cartões, o primeiro parágrafo e a leitura passam a dizer que os casos foram conferidos.
# ! Motivo: a ficha 44 nasceu de a conferência não estar registrada; depois da resposta, a aba diria "nenhuma pessoa os conferiu ainda". Sem o arquivo, ela fica como era.
def secao_conferencia(conf: dict | None, respostas: dict | None = None) -> tuple[dict, str]:
    if not conf:
        return {}, ('<section id="conferencia" hidden>\n<h1>Conferência dos inéditos: os casos da corrida 24 estão certos?</h1>\n'
                    '<p class="lead">O documento ainda não foi gerado: falta <code>resultados_alvo/fase4/conferencia_ineditos.json</code>, que sai de <code>gerar_conferencia_ineditos.py</code>.</p>\n</section>')
    r = conf["resumo"]

    def termos(lista: list | None) -> str:
        return ", ".join(lista or []) or "nenhum"

    def bloco(x: dict) -> str:
        e, g = x["entrada"], x["gabarito"]
        linhas = [["Requisição", e.get("requisicao")], ["Status", e.get("status")], ["Contrato", e.get("contrato")], ["Corpo", e.get("corpo")], ["Sintoma", e.get("sintoma")]]
        linhas += [[rotulo, e[chave]] for rotulo, chave in (("Observação", "observacao"), ("Seletor quebrado", "seletor_quebrado"), ("Árvore da tela", "arvore")) if e.get(chave)]
        linhas += [["Causa do gabarito", g["causa_raiz"]], ["Campo afetado", g.get("campo_afetado") or "nenhum"], ["Termos esperados", termos(g.get("termos_esperados"))],
                   ["Termos proibidos", termos(g.get("termos_proibidos"))], ["Na corrida 17", x["tela"] or "não aparece na leitura"]]
        if x["veredito"] == "ver":
            linhas.append(["Pré-análise", x["o_que_olhar"]])
            if x.get("causa_vizinha"):
                linhas.append(["Outra causa que caberia", x["causa_vizinha"]])
        else:
            linhas.append(["Pré-análise", "nada a apontar"])
        linhas.append(["Onde a pré-análise leu", x.get("evidencia") or "n/d"])
        if respostas:
            linhas.append(["Resposta do Eric", respostas["respostas"].get(x["caso"]) or respostas["outros"]])
        marca = chip("nao_cumprida", "para olhar") if x["veredito"] == "ver" else chip("adotado", "sem apontamento")
        return (f'<details><summary><code>{esc(x["caso"])}</code> classe {esc(str(x["classe"]))}, nível {esc(str(x["nivel"]))}: <code>{esc(g["causa_raiz"])}</code> {marca}</summary>'
                # as aspas também são escapadas: a árvore da tela traz texto como id="modalDetalheTitulo", que seria lido como um id repetido da página
                f'{tabela(["Campo", "O que está no caso"], [[esc(a), esc(str(b)).replace(chr(34), "&quot;")] for a, b in linhas], raw=True)}</details>')

    para_olhar = [x for x in conf["casos"] if x["veredito"] == "ver"]
    tabela_ver = tabela(["Caso", "Causa do gabarito", "Outra causa que caberia", "O que olhar"],
                        [[f'<code>{esc(x["caso"])}</code>', f'<code>{esc(x["gabarito"]["causa_raiz"])}</code>', f'<code>{esc(x["causa_vizinha"])}</code>' if x.get("causa_vizinha") else "nenhuma", esc(x["o_que_olhar"])]
                         for x in para_olhar], raw=True) if para_olhar else "<p>Nenhum caso apontado.</p>"
    classes = tabela(["Classe", "Casos", "Reproduzem na tela", "Sem apontamento", "Para olhar"], [[x["classe"], x["casos"], x["reproduzem"], x["ok"], x["ver"]] for x in conf["por_classe"]])
    n_ver = len((respostas or {}).get("respostas") or {})
    mudaram = (respostas or {}).get("mudancas") or []
    itens_kpi = [("Casos", str(r["casos"]), f'{len(conf["por_classe"])} classes; ' + (f'conferidos pelo Eric, {len(mudaram)} mudaram' if respostas else "nenhuma pessoa conferiu ainda")), ("Reproduzem na tela", f'{r["reproduzem"]} de {r["casos"]}', f'corrida 17; {r["fora_da_tela"]} ficam fora da tela'),
                 ("Sem apontamento", str(r["ok"]), "pré-análise do Claude, só lendo o código"), ("Para olhar", str(r["ver"]), "a pré-análise aponta uma dúvida")]
    lead_ = (f'Conferidos. O Eric leu os {n_ver} apontados pela pré-análise, um a um, e passou os olhos nos outros {r["casos"] - n_ver}: {"nenhum caso mudou" if not mudaram else f"{len(mudaram)} mudaram"} (ficha 46, decisão 100). A corrida 24 mede a biblioteca final nestes {r["casos"]} casos, na aba "Inéditos em texto". As recomendações que ele viu foram escritas pelo Claude, que já conhecia os resultados da corrida 18e, e ele as seguiu em todos os casos; isso fica declarado.' if respostas else
             f'A corrida 24 vai medir a biblioteca final nestes {r["casos"]} casos, e nenhuma pessoa os conferiu ainda. A pré-análise, de um agente do Claude que só leu o código, não aponta nada em {r["ok"]} e aponta {r["ver"]}. Ela indica onde olhar; quem confere é você, e a resposta vai na ficha 46.')
    item_mudar = ("<strong>Nenhum texto mudou</strong>, então nenhuma corrida se repete, e o lado escrito da corrida 18e vale como rodou." if respostas and not mudaram else
                  f"<strong>Mudar o texto de um caso</strong> não mexe nas corridas 17, 18c, 18d, 21c, 21d e 23, porque nenhuma delas lê esse texto com o modelo. A corrida 18e leu, no caso escrito, os {r['reproduzem']} que reproduzem: o caso que mudar roda de novo. O que for trocado é refeito e conferido de novo por script antes da corrida 24.")
    html_ = f"""<section id="conferencia" hidden>
<h1>Conferência dos inéditos: os {r["casos"]} casos da corrida 24 estão certos?</h1>
<p class="lead">{lead_}</p>
{kpis(itens_kpi)}
<h2>Os casos para olhar</h2>
<p>Nestes, a pré-análise acha que outra causa da lista também caberia, ou que o sistema não produz o que o caso descreve.</p>
{tabela_ver}
<h2>Todos os casos, com os para olhar primeiro</h2>
{"".join(bloco(x) for x in conf["casos"])}
{detalhes("Os casos por classe", classes)}
{leitura([
    "<strong>A pergunta de cada caso:</strong> a causa do gabarito é a leitura certa do que o corpo e o sintoma mostram? Um caso ruim mede o modelo contra algo que o sistema não produz, ou contra uma resposta com mais de uma leitura honesta.",
    "<strong>Na corrida 17</strong> diz o que a falha injetada fez de verdade: <em>reproduz</em> quando a chamada à CobaiaAPI saiu do normal na tela; <em>fora</em> quando a rota não tem tela ou o caso é um cenário descrito, sem modo de falha.",
    item_mudar,
])}
{fontes(["<code>resultados_alvo/fase4/conferencia_ineditos.json</code> e <code>.md</code> (<code>gerar_conferencia_ineditos.py</code>, com <code>--check</code>)", "<code>banco_casos_ineditos_fase4.py</code>", "<code>reproducibilidade_ineditos.json</code> (corrida 17)", "<code>conferencia_ineditos_preanalise.json</code> (pré-análise do Claude)", "<code>conferencia_ineditos_respostas.json</code> (as respostas do Eric)", "decisões 92 e 100 e ficha 46"])}
</section>"""
    return {}, html_


# ! Alteração de IA - Revisar: (07/11/2026) a aba "Pós-Fase 4": o que o Eric pediu em três partes, o que a pesquisa da rodada 6 sustenta (levantamento §6.15: a tabela do cabeçalho e o mapa), as quatro decisões do quadro e as fichas abertas (pendencias.md, fichas 49 a 54) e os pacotes do plano (títulos "### Qn." de claude-memoria/plano-aprovado-pos-fase-4.md, ou do rascunho plano-pos-fase-4.md enquanto não aprovado).
# ! Motivo: a regra do painel é uma aba por análise, e o Eric decide pelo painel: as fichas 53 e 54 estão abertas, e a aba mostra o que cada uma pergunta com os vereditos que a sustentam. Nenhum número é digitado aqui: tudo é lido por expressão regular dos três arquivos.
_POS4_CABECALHO = re.compile(r"^\| §6\.15\.(\d+) \| (\d) \| `([^`]+)` \| (\d+) \|$", re.MULTILINE)
_POS4_TITULO = re.compile(r"^#### 6\.15\.(\d+) (.+?) \(`([^`]+)`; (\d+) fontes? com endereço\)$", re.MULTILINE)
_POS4_PACOTE = re.compile(r"^### (Q\d)\. (.+?) \((.+?)\)$", re.MULTILINE)
POS4_ROTULOS = {"pos4-revisao-estilo-pr": "Hub estilo PR", "pos4-indicador-de-progresso": "Barra de progresso", "pos4-arvore-de-decisao": "Árvore de decisão",
                "pos4-metricas-de-prolixidade": "Métricas de prolixidade", "pos4-impacto-git-e-vm": "Impacto pelo Git e VM", "pos4-syllabus-ctfl": "Syllabus CTFL 4.0"}
POS4_COR_DA_PARTE = {"1": "--s1", "2": "--s2", "3": "--s3"}
POS4_CHIP = {"adotado": "adotado", "ideia": "andamento", "adiado": "outro", "descartado": "nao_cumprida"}


def _pos4_leituras(lev: str) -> list[dict]:
    """As linhas da tabela do cabeçalho do §6.15, com o título lido da subseção de cada chave."""
    titulos = {m.group(3): m.group(2) for m in _POS4_TITULO.finditer(lev)}
    saida = []
    for m in _POS4_CABECALHO.finditer(lev):
        n, parte, chave, fontes = m.groups()
        saida.append({"n": int(n), "parte": parte, "chave": chave, "titulo": titulos.get(chave, chave), "fontes": int(fontes),
                      "rotulo": POS4_ROTULOS.get(chave, chave.replace("pos4-repo-", "").replace("pos4-", "")), "cor": POS4_COR_DA_PARTE.get(parte, "--s8")})
    return saida


def _pos4_mapa(lev: str) -> list[dict]:
    """As linhas da tabela do mapa do levantamento: leitura, chave, o que vale para o Claude Code e para o agente, o que fica, veredito."""
    ini = lev.find("Mapa adotado, ideia, adiado, descartado")
    if ini < 0:
        return []
    saida = []
    for l in lev[ini:].splitlines():
        if not l.startswith("| ") or l.startswith(("| Leitura", "|---")):
            continue
        cel = [c.strip() for c in l.strip().strip("|").split(" | ")]
        if len(cel) != 5:
            continue
        m = re.match(r"^(.*) \(`([^`]+)`\)$", cel[0])
        saida.append({"leitura": m.group(1) if m else cel[0], "chave": m.group(2) if m else "", "claude": cel[1], "agente": cel[2], "fica": cel[3], "veredito": cel[4].strip("*")})
    return saida


def _pos4_tabela_do_syllabus(lev: str) -> tuple[list[str], list[list[str]]]:
    """A tabela "Onde o projeto cabe" da leitura do syllabus (§6.15.6): cabeçalho e linhas, como texto."""
    ini = lev.find("| Dimensão do syllabus |")
    if ini < 0:
        return [], []
    linhas = []
    for l in lev[ini:].splitlines():
        if not l.startswith("|"):
            break
        if l.startswith("|---"):
            continue
        linhas.append([c.strip() for c in l.strip().strip("|").split(" | ")])
    return linhas[0], linhas[1:]


def secao_pos_fase4(levantamento: str | None, plano: str | None, pend: list) -> tuple[dict, str]:
    titulo = "Pós-Fase 4: o que chega ao analista. O que o Eric pediu, o que a pesquisa sustenta e o que entra antes e depois da Fase 5?"
    if not levantamento:
        return {}, (f'<section id="posfase4" hidden>\n<h1>{titulo}</h1>\n<p class="lead">O levantamento ainda não foi integrado: falta '
                    '<code>Documentacao/memorial/2-pesquisa-e-literatura/levantamento-2026-11-07-pos-fase-4.md</code>, que sai de <code>integrar_pesquisa_pos_fase4.py</code>.</p>\n</section>')
    leituras, mapa = _pos4_leituras(levantamento), _pos4_mapa(levantamento)
    por_parte = Counter(x["parte"] for x in leituras)
    vereditos = Counter(m["veredito"] for m in mapa if m["chave"].startswith("pos4-repo-"))
    fichas = {f.numero: f for b in pend for f in b.fichas if 49 <= f.numero <= 54}
    fechadas = [f for n, f in sorted(fichas.items()) if not f.aberta]
    abertas = [f for n, f in sorted(fichas.items()) if f.aberta]
    pacotes = _POS4_PACOTE.findall(plano or "")
    total_fontes = sum(x["fontes"] for x in leituras)
    repos = [m for m in mapa if m["chave"].startswith("pos4-repo-")]
    itens_kpi = [("Leituras", str(len(leituras)), f'{por_parte.get("1", 0)} bases, {por_parte.get("2", 0)} syllabus, {por_parte.get("3", 0)} repositórios; sem verificação cética'),
                 ("Fontes com endereço", str(total_fontes), "contadas pelo integrador; valem com a marca de confiança de cada leitura"),
                 ("Repositórios que entram", f'{vereditos.get("adotado", 0)} de {len(repos)}', f'ideia: {vereditos.get("ideia", 0)}; adiado: {vereditos.get("adiado", 0)}; descartado: {vereditos.get("descartado", 0)}'),
                 ("Decisões do Eric", str(len(fechadas)), "no quadro da sessão de 07/11/2026" if fechadas else "nenhuma ainda"),
                 ("Fichas abertas", str(len(abertas)), ", ".join(f"ficha {f.numero}" for f in abertas) or "nenhuma")]
    pendentes = (f'{len(abertas)} fichas esperam resposta: ' + "; ".join(f"ficha {f.numero}, {esc(f.titulo)}" for f in abertas) + "." if abertas
                 else "nenhuma ficha espera resposta.")
    lead_ = (f'Em 07/11/2026 o Eric especificou a fase em três partes e a pesquisa foi feita no mesmo dia: {len(leituras)} leituras com {total_fontes} fontes com endereço. '
             f'Dos {len(repos)} repositórios, {vereditos.get("adotado", 0)} entram como peça do agente; {vereditos.get("ideia", 0)} deixam uma ideia e {vereditos.get("adiado", 0)} ficam como candidatos futuros. '
             f'{len(fechadas)} decisões foram tomadas no quadro e {pendentes}')
    tab_decisoes = tabela(["Ficha", "Pergunta", "Decisão"], [[str(f.numero), esc(f.titulo), pt.inline(f.campos.get("Decisão", ""))] for f in fechadas], raw=True) if fechadas else "<p>Nenhuma ficha fechada ainda.</p>"
    tab_leituras = tabela(["Subseção", "Parte", "Leitura", "Fontes com endereço"], [[f'§6.15.{x["n"]}', x["parte"], f'{esc(x["titulo"])} (<code>{esc(x["chave"])}</code>)', str(x["fontes"])] for x in leituras], raw=True)
    tab_mapa = tabela(["Leitura", "Para o Claude Code", "Para o agente", "O que fica", "Veredito"],
                      [[esc(m["leitura"]), pt.inline(m["claude"]), pt.inline(m["agente"]), pt.inline(m["fica"]), chip(POS4_CHIP.get(m["veredito"], "outro"), m["veredito"])] for m in mapa], raw=True)
    cab_s, linhas_s = _pos4_tabela_do_syllabus(levantamento)
    tab_syllabus = tabela(cab_s, [[pt.inline(c) for c in l] for l in linhas_s], raw=True) if linhas_s else "<p>A leitura do syllabus ainda não está no levantamento.</p>"
    tab_pacotes = tabela(["Pacote", "O que entrega", "Sessões e máquina"], [[p, esc(t), esc(c)] for p, t, c in pacotes], raw=True) if pacotes else "<p>O plano em rascunho ainda não existe.</p>"

    def bloco_ficha(f) -> str:
        opcoes = "".join(f"<li>{pt.inline(o)}</li>" for o in f.listas.get("Opções", []))
        return (f'<details open><summary>ficha {f.numero}: {esc(f.titulo)}</summary><p>{pt.inline(f.campos.get("O que é", ""))}</p><ul>{opcoes}</ul>'
                f'<p><strong>Recomendação:</strong> {pt.inline(f.campos.get("Recomendação", ""))}</p></details>')

    html_ = f"""<section id="posfase4" hidden>
<h1>{titulo}</h1>
<p class="lead">{lead_}</p>
{kpis(itens_kpi)}
<h2>O que o Eric pediu</h2>
<p>Três partes: (1) o visual e a usabilidade do agente, com um hub central à imagem de uma pull request, a integração com o Git, a barra de progresso, a árvore de decisão e a normalização das respostas por filtros determinísticos, tudo local na máquina do dev de QA; (2) o projeto contra o syllabus CTFL 4.0 do ISTQB, na tradução do BSTQB; (3) oito repositórios do GitHub, com a viabilidade para o Claude Code e para o agente.</p>
<h2>As decisões do quadro</h2>
{tab_decisoes}
<h2>O que depende do Eric</h2>
{"".join(bloco_ficha(f) for f in abertas) or "<p>Nenhuma ficha aberta: as fichas 49 a 54 foram respondidas no quadro da sessão de 07/11/2026.</p>"}
<h2>Fontes por leitura</h2>
<p>Quantas fontes com endereço cada leitura cita; a cor é a parte do pedido. Nenhuma passou por verificação cética: o número vale com a marca de confiança da leitura.</p>
<div class="chart"><canvas id="g-pos4-fontes"></canvas></div>
{detalhes("As leituras, uma a uma", tab_leituras)}
<h2>O mapa: o que entra, o que fica como ideia, o que sai</h2>
{tab_mapa}
<h2>O projeto contra o syllabus</h2>
{tab_syllabus}
<h2>Os pacotes do plano aprovado</h2>
{tab_pacotes}
{leitura([
    "<strong>A divisão</strong> (decisão 101): o que muda o que o analista lê entra antes da Fase 5; o hub e a integração com o Git, depois dela, como a decisão 93 previa.",
    "<strong>O mapa</strong> foi escrito pelo Claude; o plano que o incorpora foi aprovado como está (ficha 54, decisão 105), e nenhum dos dois repositórios opcionais ganha sessão de teste (ficha 53, decisão 106).",
    "<strong>Pelo syllabus</strong>, o agente faz teste funcional, caixa-preta e automatizado, de regressão e de confirmação, nos níveis de sistema e de integração de sistema, sobre tarefas de ponta a ponta; o que faltava era o relatório de defeitos da seção 5.5 (decisão 104).",
])}
{fontes(["<code>Documentacao/memorial/2-pesquisa-e-literatura/levantamento-2026-11-07-pos-fase-4.md</code> (<code>integrar_pesquisa_pos_fase4.py</code>, com <code>--check</code>; leituras em <code>5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/</code>)",
         "<code>claude-memoria/plano-aprovado-pos-fase-4.md</code> (aprovado pela decisão 105)", "<code>pendencias.md</code>, fichas 49 a 54; decisões 101 a 106; roadmap §4.8"])}
</section>"""
    return {"leituras": leituras, "mapa": mapa, "vereditos": dict(vereditos)}, html_


# ! Alteração de IA - Revisar: (07/11/2026, Pós-Fase 4, pacote Q2) a aba "O que chega ao analista": lê resultados_alvo/fase4/texto.json (avaliar_fase4.py --texto) e
# mostra quantos relatórios e leituras passam nos oito filtros de prolixidade e objetividade antes e depois, a parcela por critério, os termos sem o significado, as
# médias, os limiares com a fonte, o que o plano antecipou para as frases e o corpus da calibração; o id entra no NAV e os dois gráficos em DESENHAR_TOPICOS.
# ! Motivo: a regra do painel é uma aba por análise, lida do JSON versionado, e o plano da Pós-Fase 4 (seção 3.3) pede a aba com a leitura antes e depois; nenhum
# número é digitado aqui.
NOME_CURTO_DO_CRITERIO = {"palavras_por_frase_media": "palavras por frase (média)", "palavras_por_frase_max": "palavras por frase (máximo)", "preenchimento_razao": "preenchimento",
                          "repeticao_razao": "repetição", "compressao": "compressão", "termos_sem_expansao_n": "termo sem o significado"}
REGRA_EM_PALAVRAS = {"ate": "até o limiar", "alarme_abaixo": "alarme abaixo do valor", "zero": "nenhuma ocorrência", "comparacao": "só para comparar", "covariavel": "covariável, nunca critério"}
CASAS_DO_LIMIAR = {"palavras_por_frase_media": 1, "palavras_por_frase_max": 1, "flesch": 0, "preenchimento_razao": 4, "repeticao_razao": 4, "compressao": 3, "termos_sem_expansao_n": 0}


def _txt_num(v, casas: int = 2) -> str:
    if v is None:
        return "sem valor"
    if isinstance(v, bool):
        return "sim" if v else "não"
    if isinstance(v, int) or casas == 0:
        return str(round(v))
    return f"{v:.{casas}f}".replace(".", ",")


def _txt_pct(v) -> str:
    return "sem valor" if v is None else f"{v:.1f}%".replace(".", ",")


# ! Alteração de IA - Revisar: (10/11/2026) `secao_texto` ganhou o parâmetro `curadoria` (as respostas e os consertos da curadoria das leituras) e passou a mostrar
# quantas leituras estão curadas, quantas o analista aprovou como estavam e quantas reescreveu, os consertos do Claude e a tabela leitura a leitura.
# ! Motivo: a regra do painel pede que toda curadoria apareça numa aba lida dos arquivos; a aba dizia que o que ainda reprovava ficava "para a curadoria do Eric", e as
# 39 leituras foram curadas em 10/11/2026 por um analista, a quem o Eric passou as leituras, com consertos do Claude (decisão 115).
def secao_texto(texto: dict | None, curadoria: dict | None = None) -> tuple[dict, str]:
    titulo = "O que chega ao analista ficou mais curto e direto? Os filtros de prolixidade e objetividade nos relatórios v2 e v3 das três corridas vigentes e nos verbetes contra a camada de leitura."
    if not texto:
        return {}, (f'<section id="texto" hidden>\n<h1>{titulo}</h1>\n<p class="lead">A leitura ainda não foi gravada: falta <code>resultados_alvo/fase4/texto.json</code>, '
                    'que sai de <code>avaliar_fase4.py --texto</code> depois de <code>filtros_de_texto.py --calibrar</code>.</p>\n</section>')
    rel, ver, mo = texto["resumo"]["relatorios"], texto["resumo"]["verbetes"], texto["modelo"]
    ra, rd, va, vd = rel["antes"], rel["depois"], ver["antes"], ver["depois"]
    lim = texto["limiares"]
    valores, corpus = lim["valores"], lim.get("corpus") or {}
    por_metrica = lim.get("corpus_por_metrica") or {}
    chaves = [m["chave"] for m in texto["metricas"] if m["regra"] in ("ate", "zero")]
    series = [("relatórios v2", "--s4", ra), ("relatórios v3", "--s1", rd), ("verbetes", "--s6", va), ("camada de leitura", "--s2", vd)]
    criterios = {"rotulos": [NOME_CURTO_DO_CRITERIO.get(ch, ch) for ch in chaves], "chaves": chaves,
                 "series": [{"nome": n, "cor": cor, "pct": [ag["criterios"][ch]["passam_pct"] for ch in chaves]} for n, cor, ag in series]}
    termos_antes = Counter(ra["termos_sem_expansao"]) + Counter(va["termos_sem_expansao"])
    termos_depois = Counter(rd["termos_sem_expansao"]) + Counter(vd["termos_sem_expansao"])
    rotulos_t = sorted(set(termos_antes) | set(termos_depois), key=lambda t: (-(termos_antes.get(t, 0) + termos_depois.get(t, 0)), t))
    termos = {"rotulos": rotulos_t, "antes": [termos_antes.get(t, 0) for t in rotulos_t], "depois": [termos_depois.get(t, 0) for t in rotulos_t]}
    oc_ra, oc_rd = sum(ra["termos_sem_expansao"].values()), sum(rd["termos_sem_expansao"].values())
    oc_va, oc_vd = sum(va["termos_sem_expansao"].values()), sum(vd["termos_sem_expansao"].values())
    por_fonte = corpus.get("por_fonte") or {}
    frases_c = por_metrica.get("palavras_por_frase_media") or {}
    flesch_c = por_metrica.get("flesch") or {}
    prov_rd = rd.get("provisorios_do_plano") or {}
    itens_kpi = [("Relatórios v3 que passam em tudo", f'{rd["aprovados"]} de {rd["n"]}', f'relatórios v2: {ra["aprovados"]} de {ra["n"]}'),
                 ("Leituras que passam em tudo", f'{vd["aprovados"]} de {vd["n"]}', f'verbetes como estão: {va["aprovados"]} de {va["n"]}'),
                 ("Leituras curadas", f'{sum(1 for p in next((g for g in texto["grupos"] if g["id"] == "camada_de_leitura"), {"pares": []})["pares"] if p.get("curado"))} de {vd["n"]}',
                  "curadoria por um analista na página, com consertos do Claude (decisão 115)" if (curadoria or {}).get("respostas") else "a camada é gerada por código e curada à mão"),
                 ("Termos sem o significado nos relatórios", f"de {oc_ra} para {oc_rd}", "ocorrências nos textos, v2 e v3"),
                 ("Alarme do Flesch nos relatórios", f'de {ra["alarme_flesch"]} para {rd["alarme_flesch"]}', "textos abaixo de 50; o alarme não reprova"),
                 ("Frases do modelo que passam", f'{mo["aprovados"]} de {mo["n"]}', "a linha IMPACTO, medida como o modelo a escreveu"),
                 ("Corpus da calibração", f'{corpus.get("itens", 0)} textos', ", ".join(f"{n} {'comentários' if f == 'motivo' else 'itens do exemplo canônico'}" for f, n in por_fonte.items()) or "sem corpus")]
    lead_ = (f'Nos relatórios, {rd["aprovados"]} de {rd["n"]} passam em todos os filtros depois (v3), contra {ra["aprovados"]} de {ra["n"]} antes (v2); nos verbetes, '
             f'{vd["aprovados"]} de {vd["n"]} leituras passam, contra {va["aprovados"]} de {va["n"]} verbetes como estão. Os termos da lista fechada sem o significado na primeira '
             f'menção caíram de {oc_ra} ocorrências para {oc_rd} nos relatórios e de {oc_va} para {oc_vd} nos verbetes; o alarme do Flesch acendia em {ra["alarme_flesch"]} relatórios v2 '
             f'e acende em {rd["alarme_flesch"]} v3. Os limiares calibrados são o percentil 95 do corpus de referência ({corpus.get("itens", 0)} textos); os de fonte são o alarme '
             f'do Flesch em 50 e nenhum termo sem o significado.')
    tab_metricas = tabela(["Métrica", "Regra", "Limiar", "De onde vem o limiar", "Fonte"],
                          [[esc(m["nome"]), REGRA_EM_PALAVRAS.get(m["regra"], m["regra"]), _txt_num(m["limiar"], CASAS_DO_LIMIAR.get(m["chave"], 2)),
                            {"calibracao": "calibração (percentil 95 do corpus)", "fonte": "valor da fonte", "fixo": "fixado", "comparacao": "sem limiar: só para comparar", None: "sem limiar"}.get(m.get("tipo"), m.get("tipo") or "sem limiar")
                            + (f'; o plano antecipou {m["provisorio_do_plano"]}' if m.get("provisorio_do_plano") is not None else ""), esc(m["fonte"])] for m in texto["metricas"]]
                          + [[esc(texto["covariavel"]["nome"]), REGRA_EM_PALAVRAS["covariavel"], "não há", "sem limiar", esc(texto["covariavel"]["fonte"])]], raw=True)

    def linha_media(rotulo: str, versao: str, ag: dict) -> list[str]:
        md = ag["medias"]
        return [rotulo, versao, str(ag["n"]), f'{ag["aprovados"]} ({_txt_pct(ag["aprovados_pct"])})', f'{ag["alarme_flesch"]} ({_txt_pct(ag["alarme_flesch_pct"])})',
                _txt_num(md["palavras_por_frase_media"]), _txt_num(md["palavras_por_frase_max"], 1), _txt_num(md["flesch"], 1), _txt_num(md["preenchimento_razao"], 4),
                _txt_num(md["repeticao_razao"], 4), _txt_num(md["compressao"], 3), _txt_num(md["termos_sem_expansao_n"], 2), _txt_num(md["densidade_dominio"], 3), _txt_num(ag["palavras_mediana"], 0)]

    linhas_medias, linhas_termos, linhas_prov, linhas_casos = [], [], [], []
    for g in texto["grupos"]:
        a, d = g["antes"], g["depois"]
        versoes = ("relatório v2", "relatório v3") if g["tipo"] == "relatorios" else ("verbete", "leitura")
        linhas_medias += [linha_media(g["rotulo"], versoes[0], a), linha_media(g["rotulo"], versoes[1], d)]
        for t in sorted(set(a["termos_sem_expansao"]) | set(d["termos_sem_expansao"]), key=lambda x: (-(a["termos_sem_expansao"].get(x, 0) + d["termos_sem_expansao"].get(x, 0)), x)):
            linhas_termos.append([g["rotulo"], t, str(a["termos_sem_expansao"].get(t, 0)), str(d["termos_sem_expansao"].get(t, 0))])
        for versao, ag in ((versoes[0], a), (versoes[1], d)):
            pr = ag.get("provisorios_do_plano") or {}
            linhas_prov.append([g["rotulo"], versao, str(ag["n"])] + [f'{pr[ch]["passam"]} ({_txt_pct(pr[ch]["passam_pct"])})' if ch in pr else "sem valor" for ch in ("palavras_por_frase_media", "palavras_por_frase_max")])
        for par in g["pares"]:
            pa, pd = par["antes"], par["depois"]
            linhas_casos.append([g["rotulo"], par.get("nome") or par.get("id"), _txt_num(pa["aprovado"]), _txt_num(pd["aprovado"]), _txt_num(pa["palavras_por_frase_max"]), _txt_num(pd["palavras_por_frase_max"]),
                                 _txt_num(pa["flesch"], 1), _txt_num(pd["flesch"], 1), ", ".join(pa["termos_sem_expansao"]) or "nenhum", ", ".join(pd["termos_sem_expansao"]) or "nenhum",
                                 str(pa["palavras"]), str(pd["palavras"])])
    tab_medias = tabela(["Grupo", "Versão", "Textos", "Passam em tudo", "Alarme do Flesch", "Palavras por frase (média)", "Palavras por frase (máximo)", "Flesch", "Preenchimento", "Repetição",
                         "Compressão", "Termos sem o significado", "Densidade do domínio", "Palavras (mediana)"], linhas_medias)
    tab_termos = tabela(["Grupo", "Termo", "Textos antes", "Textos depois"], linhas_termos or [["nenhum", "nenhum", "0", "0"]])
    tab_prov = tabela(["Grupo", "Versão", "Textos", "Passam com média até 20", "Passam com máximo até 30"], linhas_prov)
    tab_casos = tabela(["Grupo", "Texto", "Passa antes", "Passa depois", "Maior frase antes", "Maior frase depois", "Flesch antes", "Flesch depois", "Termos antes", "Termos depois", "Palavras antes", "Palavras depois"], linhas_casos)
    tab_corpus = tabela(["Métrica", "Mediana no corpus", "Percentil 75", "Percentil 90", "Percentil 95", "Limiar"],
                        [[esc(m["nome"]), _txt_num((por_metrica.get(m["chave"]) or {}).get("mediana"), CASAS_DO_LIMIAR.get(m["chave"], 2) or 1), _txt_num((por_metrica.get(m["chave"]) or {}).get("percentil_75"), CASAS_DO_LIMIAR.get(m["chave"], 2) or 1),
                          _txt_num((por_metrica.get(m["chave"]) or {}).get("percentil_90"), CASAS_DO_LIMIAR.get(m["chave"], 2) or 1), _txt_num((por_metrica.get(m["chave"]) or {}).get("percentil_95"), CASAS_DO_LIMIAR.get(m["chave"], 2) or 1),
                          _txt_num(m["limiar"], CASAS_DO_LIMIAR.get(m["chave"], 2))] for m in texto["metricas"] if por_metrica.get(m["chave"])], raw=True)
    sobra = ", ".join(f"<code>{esc(t)}</code> ({n})" for t, n in vd["termos_sem_expansao"].items()) or "nenhum"
    camada = next((g for g in texto["grupos"] if g["id"] == "camada_de_leitura"), {"pares": []})
    curadas = sum(1 for p in camada["pares"] if p.get("curado"))
    respostas_c, consertos_c = (curadoria or {}).get("respostas") or [], (curadoria or {}).get("consertos") or {}
    aprovadas_c = sum(1 for x in respostas_c if x["estado"] == "aprovada")
    reescritas_c = sum(1 for x in respostas_c if x["estado"] == "editada")
    n_consertos = sum(len(v) for v in consertos_c.values())
    dados_curadoria = {"curadas": curadas, "aprovadas": aprovadas_c, "reescritas": reescritas_c, "consertos": n_consertos, "leituras_consertadas": len(consertos_c)}
    if curadas and respostas_c:
        dia = max(x["salvo_em"] for x in respostas_c if x.get("salvo_em"))[:10]
        item_camada = (f'<strong>Na camada de leitura</strong> passam {vd["aprovados"]} de {vd["n"]} leituras, contra {va["aprovados"]} verbetes como estão. As {curadas} de {vd["n"]} leituras foram '
                       f'curadas em {dia[8:10]}/{dia[5:7]}/{dia[0:4]} na página da curadoria por um analista, a quem o Eric passou cada leitura e de quem colou a resposta: {aprovadas_c} aprovadas como estavam e '
                       f'{reescritas_c} reescritas. Depois vieram {n_consertos} consertos do Claude em {len(consertos_c)} delas, a pedido do Eric, no que era fato errado ou formato quebrado: notas que '
                       'diziam que a busca é vetorial e que as épocas são treinamento, uma linha colada na seguinte, uma mensagem literal da API alterada e termos ainda sem o significado '
                       '(decisão 115). As notas que o modelo acrescentou aos verbetes saíram das leituras e continuam nos verbetes que o modelo lê.')
    elif curadas:
        item_camada = (f'<strong>Na camada de leitura</strong> passam {vd["aprovados"]} de {vd["n"]} leituras, contra {va["aprovados"]} verbetes como estão; {curadas} de {vd["n"]} leituras estão curadas.')
    else:
        item_camada = (f'<strong>Na camada de leitura</strong> passam {vd["aprovados"]} de {vd["n"]} leituras, contra {va["aprovados"]} verbetes como estão; o que sobra é texto do próprio verbete ({sobra}), '
                       'que a curadoria reescreve.')
    por_id = {p["id"]: p for p in camada["pares"]}
    tab_curadoria = tabela(["Leitura", "Resposta do analista", "Consertos do Claude", "Passa nos filtros depois da curadoria"],
                           [[f"<code>{esc(x['id'])}</code>", "aprovada como estava" if x["estado"] == "aprovada" else "reescrita" if x["estado"] == "editada" else esc(x["estado"]),
                             str(len(consertos_c.get(x["id"]) or [])), _txt_num((por_id.get(x["id"]) or {}).get("depois", {}).get("aprovado"))]
                            for x in sorted(respostas_c, key=lambda x: x["id"])], raw=True) if respostas_c else ""
    # ! Alteração de IA - Revisar: (08/11/2026) a leitura das frases longas e a nota da tabela do que o plano antecipou citam o fechamento da ficha 56 (decisão 108, opção a).
    # ! Motivo: o Eric respondeu a ficha no quadro da sessão em 08/11/2026; sem a citação, a aba diria que o limiar de frase ainda espera decisão.
    itens_leitura = [
        (f'<strong>O molde do relatório v3 foi ajustado até passar</strong>, como o plano manda (seção 9): os termos da lista fechada ganharam o significado na primeira menção, o que veio '
         f'do caso e do navegador virou citação, a classe e o nível saem em palavras do molde e as frases repetidas em blocos vizinhos foram encurtadas. Os relatórios v2 reprovam todos '
         f'({ra["aprovados"]} de {ra["n"]}), por termos da trilha sem o significado ({", ".join(list(ra["termos_sem_expansao"])[:5])}); os v3 passam {rd["aprovados"]} de {rd["n"]}.'),
        (f'<strong>As frases do corpus de referência são longas</strong>: mediana de {_txt_num(frases_c.get("mediana"), 1)} palavras por frase, e {frases_c.get("itens_de_uma_frase", "?")} dos '
         f'{corpus.get("itens", 0)} textos têm uma frase só, encadeada por ponto e vírgula e dois-pontos. Por isso o percentil 95 ficou em {_txt_num(valores["palavras_por_frase_media"]["valor"], 1)} '
         f'palavras na média e {_txt_num(valores["palavras_por_frase_max"]["valor"], 1)} na frase mais longa, bem acima dos 20 e 30 que o plano antecipou. Vale o calibrado, por decisão do Eric (ficha 56, fechada em 08/11/2026, decisão 108); com os antecipados, '
         f'passariam {prov_rd.get("palavras_por_frase_media", {}).get("passam", "?")} de {rd["n"]} relatórios v3 na média e {prov_rd.get("palavras_por_frase_max", {}).get("passam", "?")} na frase mais longa.'),
        item_camada,
        (f'<strong>O Flesch é alarme, não critério</strong>: a mediana do corpus de referência é {_txt_num(flesch_c.get("mediana"), 1)} (o alarme acende abaixo de 50); os relatórios v2 acendiam em '
         f'{ra["alarme_flesch"]} de {ra["n"]} e os v3 em {rd["alarme_flesch"]}. O índice só olha frase e sílaba, e a literatura o chama de superficial.'),
        (f'<strong>As frases de impacto do modelo</strong> ({mo["n"]}, medidas como vieram) passam em {mo["aprovados"]}; {mo["alarme_flesch"]} acendem o alarme do Flesch; preenchimentos achados: '
         f'{", ".join(f"{t} ({n})" for t, n in mo["preenchimentos"].items()) or "nenhum"}. O tamanho em palavras entra só como covariável.'),
    ]
    html_ = f"""<section id="texto" hidden>
<h1>{titulo}</h1>
<p class="lead">{lead_}</p>
{kpis(itens_kpi)}
<h2>Os oito filtros e os limiares</h2>
<p class="nota">Cada métrica sai com o limiar e a fonte declarados (levantamento §6.15.4, base D). Os limiares calibrados são o percentil 95 do corpus de referência: os textos "! Motivo:" dos comentários de IA deste repositório e o exemplo canônico do resumo técnico do Eric, lido da memória do repositório TargetERP sem copiar texto nenhum para cá.</p>
{tab_metricas}
<h2>Quantos textos ficam dentro de cada limiar, antes e depois</h2>
<div class="chart"><canvas id="g-texto-criterios"></canvas></div>
{detalhes("As médias por grupo e versão", tab_medias)}
<h2>Os termos sem o significado na primeira menção</h2>
<div class="chart"><canvas id="g-texto-termos"></canvas></div>
{detalhes("Os termos por grupo", tab_termos)}
<h2>O que o plano antecipou para as frases</h2>
<p class="nota">Segunda conta, só para comparar: o limiar que vale é o calibrado (ficha 56, fechada pelo Eric em 08/11/2026 pela decisão 108).</p>
{tab_prov}
{detalhes("O corpus da calibração, métrica a métrica", tab_corpus)}
{detalhes("Texto a texto", tab_casos)}
{detalhes("A curadoria, leitura a leitura", tab_curadoria) if tab_curadoria else ""}
{leitura(itens_leitura)}
{fontes(["<code>resultados_alvo/fase4/texto.json</code> e <code>texto.md</code> (<code>avaliar_fase4.py --texto</code>, com <code>--check</code>)",
         "<code>resultados_alvo/fase4/limiares_texto.json</code> (<code>filtros_de_texto.py --calibrar</code>)", "<code>experimentos/filtros_de_texto.py</code> (as oito métricas, as listas fechadas e a calibração)",
         "levantamento §6.15.4 e <code>5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/base-D-metricas-de-prolixidade.md</code>", "plano aprovado da Pós-Fase 4, seções 3.3 e 7 (pacote Q2)",
         "<code>resultados_alvo/fase4/curadoria_leituras/</code>: <code>respostas.json</code> (o que a página da curadoria gravou), <code>consertos.json</code> e <code>consertos.md</code> (cada troca do Claude, com o motivo)"])}
</section>"""
    return {"criterios": criterios, "termos": termos, "resumo": texto["resumo"], "curadoria": dados_curadoria}, html_


# ! Alteração de IA - Revisar: (08/11/2026, Pós-Fase 4, pacote Q3) a aba "Árvore de decisão": os números lidos dos `arvores/INDICE.json` das três corridas vigentes
# (árvores, nós da trilha que viraram decisões, afirmações por rótulo de origem, casos com divergência e com cura, confiança em palavras, filtros do Q2), dois
# gráficos, o explorador que mostra a árvore de cada caso (lida do JSON de cada trilha, compactada por _caso_compacto) e os índices recolhidos.
# ! Motivo: o plano da Pós-Fase 4 (seção 3.4 e pacote Q3) pede a árvore no explorador do painel; pela regra do painel, a análise nova vira uma aba lida dos JSON
# gravados por `arvore_de_decisao.py --saida`, e o Eric decide por ela. Nenhum número é digitado aqui.
ROTULO_CORRIDA_ARVORE = {"fase4_tela_v4": "corrida 18d (tela e caso escrito)", "fase4_ensaio_v4": "corrida 21d (ensaio dos cenários)", "fase4_ineditos": "corrida 24 (inéditos em texto)"}
ROTULOS_DE_ORIGEM = (("observado", "--s1"), ("conferido", "--s2"), ("declarado", "--s4"), ("desconhecido", "--s6"))
CONFIANCAS_ARVORE = (("alta", "--bom"), ("média", "--meio"), ("baixa", "--ruim"), ("desconhecida", "--s6"))
NOME_DO_NO = {"diagnostico": "diagnóstico", "cura": "cura", "reexecucao": "reexecução"}
ALTERNATIVAS_MOSTRADAS = 6
CASO_PADRAO_DA_ARVORE = ("fase4_ensaio_v4", "localizador-front-busca__r1")


def _caso_compacto(arv: dict) -> dict:
    """O que o explorador precisa de uma árvore: as decisões com a escolha, as afirmações rotuladas (pares [texto, origem]), as alternativas (até
    ALTERNATIVAS_MOSTRADAS, como [opção, detalhe, escolhida]), a divergência e a mensagem do navegador; o texto do modelo; o resumo. O resto (eventos,
    rastro) fica no arquivo da árvore. Os pares em vez de dicionários poupam cerca de um terço do tamanho da página."""
    decisoes = []
    for d in arv["decisoes"]:
        decisoes.append({"numero": d["numero"], "chave": d["chave"], "titulo": d["titulo"], "escolha": d.get("escolha"), "seletor": d.get("seletor"),
                         "causa_em_palavras": d.get("causa_em_palavras"), "segunda": d.get("segunda"), "confianca": (d.get("confianca") or {}).get("palavra"),
                         "afirmacoes": [[a["texto"], a["origem"]] for a in d["afirmacoes"]],
                         "alternativas": [[a.get("opcao"), a.get("detalhe"), bool(a.get("escolhida"))] for a in (d.get("alternativas") or [])[:ALTERNATIVAS_MOSTRADAS]],
                         "alternativas_total": len(d.get("alternativas") or []), "divergencia": (d.get("divergencia") or {}).get("detalhe") if d.get("divergencia") else None,
                         "erro": d.get("erro")})
    tm = arv.get("texto_do_modelo") or {}
    return {"nome": arv["nome"], "caso": arv["caso"], "trilha": arv["trilha"], "resumo": arv["resumo"], "decisoes": decisoes,
            "texto_do_modelo": {"impacto": tm.get("impacto"), "fonte": tm.get("fonte")}, "arquivo": f"{arv['nome']}.md", "relatorio_v3": arv.get("relatorio_v3")}


def secao_arvore(arvores: list[dict] | None) -> tuple[dict, str]:
    titulo = "Dá para ver por que o agente decidiu o que decidiu, passo a passo? A árvore de decisão de cada caso das corridas vigentes, com a origem de cada afirmação."
    if not arvores:
        return {}, (f'<section id="arvore" hidden>\n<h1>{titulo}</h1>\n<p class="lead">As árvores ainda não foram gravadas: falta <code>arvores/INDICE.json</code> nas pastas das '
                    'corridas vigentes, que sai de <code>arvore_de_decisao.py --saida &lt;corrida&gt;</code>.</p>\n</section>')
    resumos = [(c["corrida"], c["indice"]["resumo"]) for c in arvores]
    total = sum(r["trilhas"] for _, r in resumos)
    nos = Counter()
    decisoes = Counter()
    rotulos = Counter()
    confiancas = Counter()
    filtros_n = filtros_ap = 0
    for _, r in resumos:
        nos.update(r.get("nos_por_decisao") or {})
        decisoes.update(r.get("decisoes_por_chave") or {})
        rotulos.update(r.get("rotulos") or {})
        confiancas.update(r.get("por_confianca") or {})
        if r.get("filtros"):
            filtros_n += r["filtros"]["n"]
            filtros_ap += r["filtros"]["aprovados"]
    com_div = sum(r["com_divergencia"] for _, r in resumos)
    com_cura = sum(r["com_cura"] for _, r in resumos)
    afirmacoes = sum(rotulos.values())
    # os motivos da divergência, lidos de cada árvore: a falha do nó de diagnóstico, ou a ordem fixa da cura
    motivos: Counter = Counter()
    casos_compactos = []
    for c in arvores:
        casos = []
        for arv in c["casos"].values():
            casos.append(_caso_compacto(arv))
            for d in arv["decisoes"]:
                if d.get("divergencia"):
                    motivos[("cura: dois candidatos passaram as checagens, e a ordem fixa decidiu" if d["chave"] == "cura" else
                             (f"diagnóstico: falha `{d.get('falha')}`" if d.get("falha") else "diagnóstico: divergência sem falha registrada"))] += 1
        casos_compactos.append({"corrida": c["corrida"], "nome": ROTULO_CORRIDA_ARVORE.get(c["corrida"], c["corrida"]), "casos": casos})
    padrao = next((k for k, c in enumerate(casos_compactos) if c["corrida"] == CASO_PADRAO_DA_ARVORE[0]), 0)
    explorador = {"corridas": casos_compactos, "padrao": {"corrida": padrao, "caso": CASO_PADRAO_DA_ARVORE[1]},
                  "rotulos": {k: v for k, v in (arvores[0]["casos"][next(iter(arvores[0]["casos"]))].get("rotulos") or {}).items()} if arvores[0]["casos"] else {}}
    dados_js = {"explorador": explorador,
                "rotulos": {"corridas": [ROTULO_CORRIDA_ARVORE.get(c, c) for c, _ in resumos],
                            "series": [{"nome": rot, "cor": cor, "n": [(r.get("rotulos") or {}).get(rot, 0) for _, r in resumos]} for rot, cor in ROTULOS_DE_ORIGEM]},
                "confianca": {"corridas": [ROTULO_CORRIDA_ARVORE.get(c, c) for c, _ in resumos],
                              "series": [{"nome": conf, "cor": cor, "n": [(r.get("por_confianca") or {}).get(conf, 0) for _, r in resumos]} for conf, cor in CONFIANCAS_ARVORE
                                         if any((r.get("por_confianca") or {}).get(conf) for _, r in resumos)]},
                "resumo": {"arvores": total, "nos": sum(nos.values()), "decisoes": sum(decisoes.values()), "afirmacoes": afirmacoes, "rotulos": dict(rotulos),
                           "com_divergencia": com_div, "com_cura": com_cura, "filtros": {"n": filtros_n, "aprovados": filtros_ap}}}
    por_corrida = ", ".join(f"{r['trilhas']} da {ROTULO_CORRIDA_ARVORE.get(c, c).split(' (')[0]}" for c, r in resumos)
    nos_txt = ", ".join(f"{n} de {NOME_DO_NO.get(k, k)}" for k, n in sorted(nos.items(), key=lambda x: -x[1]))
    conf_txt = ", ".join(f"{confiancas.get(conf, 0)} {conf}" for conf, _ in CONFIANCAS_ARVORE if confiancas.get(conf))
    lead_ = (f"{total} árvores, uma por trilha com nó de decisão ({por_corrida}); os {sum(nos.values())} nós de decisão da trilha ({nos_txt}) viraram {sum(decisoes.values())} decisões "
             f"da árvore, em quatro tipos (o que o modelo lê, que verbetes entram, a causa e a cura). Das {afirmacoes} afirmações, {rotulos.get('observado', 0)} são o que o código mediu, "
             f"{rotulos.get('conferido', 0)} o que ele conferiu do que o modelo disse, {rotulos.get('declarado', 0)} o que o modelo só declarou e {rotulos.get('desconhecido', 0)} o que faltou na trilha. "
             f"{com_div} casos têm divergência entre o declarado e o conferido, e {com_cura} têm cura de localizador; a confiança do agente ficou {conf_txt}. "
             f"Os filtros de texto do pacote Q2 aprovam {filtros_ap} das {filtros_n} árvores.")
    itens_kpi = [("Árvores geradas", f"{total}", f"uma por trilha com nó de decisão: {por_corrida}"),
                 ("Nós da trilha que viraram decisões", f"{sum(nos.values())} em {sum(decisoes.values())}", nos_txt),
                 ("Afirmações medidas pelo código", f"{rotulos.get('observado', 0)} de {afirmacoes}", f"{rotulos.get('conferido', 0)} conferidas, {rotulos.get('declarado', 0)} declaradas pelo modelo, {rotulos.get('desconhecido', 0)} desconhecidas"),
                 ("Casos com divergência", f"{com_div} de {total}", "o declarado pelo modelo não bate com o conferido pelo código"),
                 ("Casos com cura de localizador", f"{com_cura} de {total}", "a decisão 4 só existe neles"),
                 ("Árvores que passam nos filtros do Q2", f"{filtros_ap} de {filtros_n}", "repetição, preenchimento, jargão sem o significado e frases longas")]
    linhas_indice = []
    for c in arvores:
        for a in c["indice"]["arvores"]:
            f = a.get("filtros") or {}
            linhas_indice.append([ROTULO_CORRIDA_ARVORE.get(c["corrida"], c["corrida"]), a["nome"], a.get("escolha") or "nenhuma", a.get("confianca") or "desconhecida",
                                  "sim" if a["divergencia"] else "não", "sim" if a["cura"] else "não", str(a["decisoes"]),
                                  "/".join(str(a["rotulos"].get(rot, 0)) for rot, _ in ROTULOS_DE_ORIGEM), "passa" if f.get("aprovado") else ("não passa" if f else "não medido")])
    tab_indice = tabela(["Corrida", "Árvore", "Causa escolhida", "Confiança", "Divergência", "Cura", "Decisões", "Afirmações (observado/conferido/declarado/desconhecido)", "Filtros do Q2"], linhas_indice)
    tab_motivos = tabela(["Motivo da divergência", "Casos"], [[pt.inline(m), str(n)] for m, n in motivos.most_common()] or [["nenhuma divergência", "0"]], raw=True)
    tab_resumo = tabela(["Corrida", "Árvores", "Nós da trilha", "Decisões", "Afirmações", "Observado", "Conferido", "Declarado", "Desconhecido", "Com divergência", "Com cura", "Passam nos filtros"],
                        [[ROTULO_CORRIDA_ARVORE.get(c, c), str(r["trilhas"]), str(sum((r.get("nos_por_decisao") or {}).values())), str(sum((r.get("decisoes_por_chave") or {}).values())),
                          str(r["afirmacoes"])] + [str((r.get("rotulos") or {}).get(rot, 0)) for rot, _ in ROTULOS_DE_ORIGEM]
                         + [str(r["com_divergencia"]), str(r["com_cura"]), f'{r["filtros"]["aprovados"]} de {r["filtros"]["n"]}' if r.get("filtros") else "não medido"] for c, r in resumos])
    desconhecidas = rotulos.get("desconhecido", 0)
    itens_leitura = [
        ("<strong>A árvore mostra o que o relatório não mostra: as alternativas.</strong> Em cada caso, os verbetes que ficaram de fora com a pontuação, a segunda causa com a probabilidade lida "
         "e, na cura, os candidatos descartados com o motivo em código. Tudo sai da trilha gravada, sem chamar o modelo de novo."),
        (f"<strong>A maior parte das afirmações é medida, não declarada.</strong> {rotulos.get('observado', 0)} das {afirmacoes} afirmações são o que o código mediu, e {rotulos.get('conferido', 0)} são o que ele "
         f"conferiu do que o modelo disse; o modelo só declara {rotulos.get('declarado', 0)} (a causa, o campo e a FONTE), e o que ele escreveu fica num bloco à parte, rotulado como texto do modelo."
         + (f" As {desconhecidas} afirmações desconhecidas são casos em que a trilha não guarda um sinal medido em código para a causa (as execuções de localizador do ensaio), e nenhuma delas vira percentual."
            if desconhecidas else "")),
        (f"<strong>A divergência aparece em {com_div} casos.</strong> A tabela dos motivos diz de onde ela vem: quase sempre a causa respondida não é tratada por nenhum verbete entregue; uma vez a resposta "
         f"veio sem a linha FONTE; e nas {com_cura} curas dois candidatos passaram as checagens em código e a ordem fixa decidiu, o que a árvore registra como divergência entre o programa e a verificação."),
        ("<strong>A confiança sai em palavras, com a taxa de acerto da faixa.</strong> Alta, média ou baixa pelos cortes da calibração, e em cada árvore a frase diz quantos casos daquela faixa o agente "
         "acertou na corrida de calibração; sem a leitura da calibração, a faixa fica sem taxa e a afirmação é marcada como desconhecida."),
        (f"<strong>O molde da árvore foi ajustado até passar nos filtros do pacote Q2</strong>, como o plano manda (seção 9): a primeira versão repetia a mesma frase para cada verbete citado e para cada "
         f"candidato da cura e reprovava na repetição de trigramas; as frases viraram uma só, e os valores medidos (o que o código esperava e recebeu) saíram da prosa para os trechos de código e para as "
         f"tabelas. Depois do ajuste, {filtros_ap} das {filtros_n} árvores passam."),
    ]
    html_ = f"""<section id="arvore" hidden>
<h1>{titulo}</h1>
<p class="lead">{lead_}</p>
{kpis(itens_kpi)}
<h2>De onde vem cada afirmação da árvore</h2>
<div class="chart"><canvas id="g-arvore-rotulos"></canvas></div>
{detalhes("O resumo por corrida", tab_resumo)}
<h2>A confiança do agente em palavras, por corrida</h2>
<div class="chart"><canvas id="g-arvore-confianca"></canvas></div>
<h2>Explorar a árvore de um caso</h2>
<p>Escolha a corrida e o caso. Cada bloco é uma decisão do agente, na ordem em que aconteceu; cada frase traz a origem: <span class="chip origem-observado">observado</span> é o que o código mediu, <span class="chip origem-conferido">conferido</span> é o que ele checou do que o modelo disse, <span class="chip origem-declarado">declarado</span> é o que o modelo escreveu sem garantia, e <span class="chip origem-desconhecido">desconhecido</span> é o que faltou na trilha. O arquivo Markdown de cada árvore está em <code>arvores/</code> na pasta da corrida.</p>
<div class="arv-explorador">
<div class="arv-controles"><label>Corrida <select class="arv-sel-corrida"></select></label><label>Caso <select class="arv-sel-caso"></select></label></div>
<div class="arv-arvore"><p class="nota">Sem o script da página, as mesmas árvores estão em <code>arvores/&lt;caso&gt;.md</code> na pasta de cada corrida.</p></div>
</div>
<h2>Por que há divergência</h2>
{tab_motivos}
{detalhes("Todas as árvores, uma linha por caso", tab_indice)}
{leitura(itens_leitura)}
{fontes(["<code>arvores/INDICE.json</code> e <code>arvores/INDICE.md</code> nas pastas <code>fase4_tela_v4</code>, <code>fase4_ensaio_v4</code> e <code>fase4_ineditos</code> (<code>arvore_de_decisao.py --saida &lt;corrida&gt;</code>, com <code>--check</code>)",
         "um <code>.md</code> e um <code>.json</code> por trilha em <code>arvores/</code>", "<code>experimentos/arvore_de_decisao.py</code> (as quatro decisões, os rótulos de origem e a confiança em palavras)",
         "<code>resultados_alvo/fase4/calibracao.json</code> e <code>limiares.json</code> (a taxa de acerto por faixa e os cortes do selo)", "plano aprovado da Pós-Fase 4, seções 3.4 e 7 (pacote Q3)"])}
</section>"""
    return dados_js, html_


# ! Alteração de IA - Revisar: (08/11/2026, Pós-Fase 4, pacote Q4) a aba "Barra e Git": as taxas do modelo nesta máquina (taxas_progresso.json), o erro da
# estimativa da barra por fase (erro_progresso.json), a fumaça real quando houver (fumaca_progresso.json) e a prova da seleção pelo diff do Git no histórico
# do repositório (impacto_git.json); dois gráficos pela paleta, cartões, "Como ler" e as tabelas recolhidas. Nenhum número digitado: tudo vem dos JSON.
# ! Motivo: a barra de progresso e o protótipo do Git são as análises novas do pacote Q4 (plano, seções 3.5 e 3.7) e, pela regra do painel, viram uma aba
# lida dos JSON gravados por script; o Eric decide pelo painel.
VEREDITO_GIT = {"roda tudo": "--s4", "seleção parcial": "--s1", "nada a rodar": "--s6"}
FASES_DO_ERRO = (("prefill_s", "prefill"), ("geracao_s", "geração"), ("total_s", "prefill mais geração"))
MEDIDAS_DAS_TAXAS = (("prefill_tokens_por_s", "prefill (tokens por segundo)", 1), ("geracao_tokens_por_s", "geração (tokens por segundo)", 2), ("tokens_entrada", "tokens do prompt", 0),
                     ("tokens_saida", "tokens gerados", 0), ("chars_por_token", "caracteres por token do prompt", 2), ("carga_ms", "carga do modelo (ms)", 0))


def _num_q4(v, casas: int = 1) -> str:
    if v is None:
        return "n/d"
    return f"{v:.{casas}f}".replace(".", ",")


def _pct_q4(v) -> str:
    return "n/d" if v is None else f"{v * 100:.0f}%"


def _data_curta(iso: str) -> str:
    return f"{iso[8:10]}/{iso[5:7]}" if iso and len(iso) >= 10 else (iso or "")


def secao_progresso(taxas: dict | None, erro: dict | None, impacto: dict | None, fumaca: dict | None = None) -> tuple[dict, str]:
    titulo = ("Dá para saber quanto falta enquanto o modelo pensa, e o que rodar quando o código das cobaias muda? A barra de progresso em duas fases, com o erro da "
              "estimativa medido nos registros gravados, e o protótipo da seleção de cenários pelo diff do Git, provado no histórico do repositório.")
    if not (taxas and erro and impacto):
        return {}, (f'<section id="progresso" hidden>\n<h1>{titulo}</h1>\n<p class="lead">Os derivados do pacote Q4 ainda não foram gravados: faltam <code>taxas_progresso.json</code>, '
                    '<code>erro_progresso.json</code> ou <code>impacto_git.json</code> em <code>resultados_alvo/fase4/</code>, que saem de <code>progresso.py --taxas</code>, '
                    '<code>progresso.py --erro</code> e <code>impacto_git.py --prova</code>.</p>\n</section>')
    modelo = next(iter(taxas["por_modelo"]))
    m = taxas["por_modelo"][modelo]
    b = erro["por_modelo"][modelo]
    fora = b["fora_da_corrida"]
    pre, ger, saida_t = m["prefill_tokens_por_s"], m["geracao_tokens_por_s"], m["tokens_saida"]
    teto = ", ".join(str(x) for x in m.get("teto_tokens") or []) or "n/d"
    r, pares, total_cen = impacto["resumo"], impacto["pares"], impacto["mapa"]["cenarios"]
    ft, fp, fg = fora["total_s"], fora["prefill_s"], fora["geracao_s"]
    erro_js = {"fases": [nome for _, nome in FASES_DO_ERRO],
               "series": [{"nome": "erro absoluto mediano (taxas das outras corridas)", "cor": "--s1", "n": [fora[ch]["erro_abs_mediana_s"] for ch, _ in FASES_DO_ERRO]},
                          {"nome": "erro absoluto no percentil 90", "cor": "--s4", "n": [fora[ch]["erro_abs_p90_s"] for ch, _ in FASES_DO_ERRO]}]}
    git_js = {"pares": [f"{p['atual'][:8]} ({_data_curta(p['data'])})" for p in pares], "selecionados": [len(p["selecao"]["cenarios"]) for p in pares],
              "vereditos": [p["veredito"] for p in pares], "cores": [VEREDITO_GIT.get(p["veredito"], "--s6") for p in pares], "total": total_cen}
    fum = None
    if fumaca and fumaca.get("por_fase"):
        pf_ = fumaca["por_fase"]
        fum = {"corrida": fumaca["metadados"].get("corrida"), "inferencias": fumaca.get("inferencias"), "por_fase": pf_}
    dados_js = {"erro": erro_js, "git": git_js, "fumaca": fum,
                "resumo": {"modelo": modelo, "registros": m["n"], "prefill_mediana": pre["mediana"], "geracao_mediana": ger["mediana"], "erro_total_mediano_s": ft["erro_abs_mediana_s"],
                           "pares": r["pares"], "rodar_tudo": r["rodar_tudo"], "selecao_parcial": r["selecao_parcial"], "nada_a_rodar": r["nada_a_rodar"]}}
    deixados = r.get("cenarios_deixados_de_fora_no_total", 0)
    lead_ = (f"Nesta máquina o {modelo} lê o prompt a {_num_q4(pre['mediana'], 1)} tokens por segundo na mediana de {pre['n']} respostas (de {_num_q4(pre['p10'], 1)} a {_num_q4(pre['p90'], 1)} em oito de cada dez) "
             f"e escreve a resposta a {_num_q4(ger['mediana'], 2)} tokens por segundo ({_num_q4(ger['p10'], 2)} a {_num_q4(ger['p90'], 2)}), com {_num_q4(saida_t['mediana'], 0)} tokens gerados na mediana e teto de {teto}. "
             f"Estimada pelas taxas das outras corridas, como a barra vê numa corrida nova, a soma do prefill com a geração erra {_num_q4(ft['erro_abs_mediana_s'], 1)} s na mediana "
             f"({_pct_q4(ft['erro_relativo_mediana'])} do tempo medido; {_num_q4(ft['erro_abs_p90_s'], 1)} s no percentil 90), quase tudo no prefill ({_num_q4(fp['erro_abs_mediana_s'], 1)} s) e pouco na geração "
             f"({_num_q4(fg['erro_abs_mediana_s'], 1)} s); {ft['subestimados']} das {ft['n']} inferências ficaram subestimadas, as outras superestimadas. "
             f"No protótipo do Git, dos {r['pares']} pares de commits consecutivos que mexeram nas cobaias, a seleção rodaria parte dos {total_cen} cenários em {r['selecao_parcial']} de {r['pares']}, "
             f"tudo em {r['rodar_tudo']} (regra 1: arquivo fora do mapa) e nada em {r['nada_a_rodar']} (só arquivos ignorados mudaram); {deixados} cenários ficaram registrados como deixados de fora.")
    if fum:
        ftot = fum["por_fase"].get("total_s") or fum["por_fase"].get("parede_s") or {}
        fumaca_kpi = ("Fumaça real com o modelo", f"{_num_q4(ftot.get('erro_abs_mediana_s'), 1)} s de erro", f"{fum['inferencias']} inferência(s) na corrida {fum['corrida']}, prefill mais geração")
    else:
        fumaca_kpi = ("Fumaça real com o modelo", "pendente", "o comando está pronto; roda com o sim do Eric e a máquina livre")
    itens_kpi = [("Taxa de prefill nesta máquina", f"{_num_q4(pre['mediana'], 1)} tokens/s", f"mediana de {pre['n']} respostas; de {_num_q4(pre['p10'], 1)} a {_num_q4(pre['p90'], 1)} em oito de cada dez"),
                 ("Taxa de geração", f"{_num_q4(ger['mediana'], 2)} tokens/s", f"de {_num_q4(ger['p10'], 2)} a {_num_q4(ger['p90'], 2)}; {_num_q4(saida_t['mediana'], 0)} tokens gerados na mediana (teto {teto})"),
                 ("Erro da estimativa: prefill mais geração", f"{_num_q4(ft['erro_abs_mediana_s'], 1)} s", f"mediano, com as taxas das outras corridas; {_pct_q4(ft['erro_relativo_mediana'])} do medido; {_num_q4(ft['erro_abs_p90_s'], 1)} s no percentil 90"),
                 ("Erro só do prefill", f"{_num_q4(fp['erro_abs_mediana_s'], 1)} s", f"{_pct_q4(fp['erro_relativo_mediana'])} do medido: é onde a estimativa erra, pelo cache do prefixo do Ollama"),
                 ("Erro só da geração", f"{_num_q4(fg['erro_abs_mediana_s'], 1)} s", f"{_pct_q4(fg['erro_relativo_mediana'])} do medido: a taxa de geração quase não varia"),
                 ("Pares de commits com seleção parcial", f"{r['selecao_parcial']} de {r['pares']}", f"{r['rodar_tudo']} rodam tudo pela regra 1 e {r['nada_a_rodar']} não rodam nada; {deixados} cenários deixados de fora, registrados"),
                 fumaca_kpi]
    tab_taxas = tabela(["Medida", "Mediana", "P10", "P90", "Mínimo", "Máximo", "n", "De onde vem"],
                       [[nome, _num_q4(m[ch]["mediana"], casas), _num_q4(m[ch]["p10"], casas), _num_q4(m[ch]["p90"], casas), _num_q4(m[ch]["min"], casas), _num_q4(m[ch]["max"], casas), str(m[ch]["n"]), m[ch]["origem"]]
                        for ch, nome, casas in MEDIDAS_DAS_TAXAS if m.get(ch)])
    linhas_erro = []
    for modo, rotulo in (("fora_da_corrida", "taxas das outras corridas"), ("na_amostra", "taxas de todas as corridas")):
        for ch, nome in FASES_DO_ERRO + (("parede_s", "tempo de relógio da chamada"),):
            e = b[modo].get(ch)
            if e:
                linhas_erro.append([rotulo, nome, str(e["n"]), _num_q4(e["erro_mediana_s"], 1), _num_q4(e["erro_abs_mediana_s"], 1), _num_q4(e["erro_abs_p90_s"], 1), _pct_q4(e["erro_relativo_mediana"]), f'{e["subestimados"]} de {e["n"]}'])
    tab_erro = tabela(["Como as taxas foram tiradas", "Fase", "n", "Erro mediano (s)", "Erro absoluto mediano (s)", "Erro absoluto P90 (s)", "Erro relativo mediano", "Subestimadas"], linhas_erro)
    tab_pares = tabela(["Commit testado", "Commit atual", "Data", "Assunto", "Alterados", "Fora da aplicação", "Ignorados", "No mapa", "Fora do mapa", "Veredito", "Cenários a rodar", "Deixados de fora"],
                       [[f"<code>{esc(p['testado'][:8])}</code>", f"<code>{esc(p['atual'][:8])}</code>", esc(p["data"]), esc(p["assunto"]), str(p["resumo"]["alterados"]), str(p["resumo"]["fora_da_aplicacao"]),
                         str(p["resumo"]["ignorados"]), str(p["resumo"]["no_mapa"]), str(p["resumo"]["fora_do_mapa"]), esc(p["veredito"]),
                         esc(", ".join(p["selecao"]["cenarios"]) or "nenhum"), esc(", ".join(p["selecao"]["deixados_de_fora"]["cenarios"]) or "nenhum")] for p in pares], raw=True)
    linhas_motivos = []
    for p in pares:
        for a in p["selecao"]["arquivos"]:
            linhas_motivos.append([f"<code>{esc(p['atual'][:8])}</code>", f"<code>{esc(a['arquivo'])}</code>", esc(a["classe"].replace("_", " ")), esc(a["motivo"])])
    tab_motivos = tabela(["Commit atual", "Arquivo da aplicação", "Classe", "Motivo"], linhas_motivos, raw=True)
    por_cenario = impacto["mapa"].get("por_cenario") or {}
    tab_mapa = tabela(["Cenário", "Cobaia", "Página", "Endpoint", "Verbetes ligados pelo endpoint", "Arquivos no mapa"],
                      [[cid, c["cobaia"], f"<code>{esc(c['pagina'])}</code>", esc(", ".join(c["endpoints"]) or "nenhum"), esc(", ".join(c["verbetes"]) or "nenhum"), str(c["arquivos"])] for cid, c in por_cenario.items()], raw=True)
    tab_regras = tabela(["Regra", "O que diz"], [[esc(k.replace("_", " ")), esc(v)] for k, v in impacto["regras"].items()])
    if fum:
        linhas_f = [[nome, str(e["n"]), _num_q4(e["erro_mediana_s"], 1), _num_q4(e["erro_abs_mediana_s"], 1), _pct_q4(e["erro_relativo_mediana"])]
                    for ch, nome in FASES_DO_ERRO + (("parede_s", "tempo de relógio da chamada"),) for e in [fum["por_fase"].get(ch)] if e]
        bloco_fumaca = (f'<p>A fumaça real rodou na corrida <code>{esc(str(fum["corrida"]))}</code>, com {fum["inferencias"]} inferência(s) do modelo: a tabela compara, por fase, o que a barra estimou antes de enviar '
                        'com o que o Ollama mediu.</p>' + tabela(["Fase", "n", "Erro mediano (s)", "Erro absoluto mediano (s)", "Erro relativo mediano"], linhas_f))
    else:
        bloco_fumaca = ('<p>A fumaça real com o modelo ainda não rodou: ela mede o erro da barra numa inferência de verdade, de ponta a ponta, e só roda com o sim do Eric, com a máquina livre '
                        '(<code>ollama ps</code> vazio e a RAM que o <code>.ps1</code> exige), lançada pelo <code>rodar_fase4.ps1</code>. Enquanto isso, o erro acima é o medido sobre as '
                        f'{m["n"]} inferências já gravadas das corridas vigentes, sem o modelo.</p>')
    vereditos_txt = {v: [f"<code>{p['atual'][:8]}</code>" for p in pares if p["veredito"] == v] for v in VEREDITO_GIT}
    itens_leitura = [
        (f"<strong>A estimativa acerta na média e erra cerca de um quinto em cada inferência.</strong> O erro mediano com sinal fica perto de zero ({_num_q4(ft['erro_mediana_s'], 1)} s), mas o erro "
         f"absoluto é de {_num_q4(ft['erro_abs_mediana_s'], 1)} s ({_pct_q4(ft['erro_relativo_mediana'])}), quase todo no prefill: a taxa de leitura do prompt varia de {_num_q4(pre['p10'], 1)} a "
         f"{_num_q4(pre['p90'], 1)} tokens por segundo porque o Ollama reaproveita a parte do prompt que já estava em memória (o cache do prefixo), e quanto disso vai ser reaproveitado só se sabe depois da resposta."),
        (f"<strong>A geração é previsível.</strong> A taxa fica entre {_num_q4(ger['p10'], 2)} e {_num_q4(ger['p90'], 2)} tokens por segundo e o modelo escreve de {_num_q4(saida_t['min'], 0)} a {_num_q4(saida_t['max'], 0)} tokens, "
         f"bem abaixo do teto de {teto}; por isso a barra usa a mediana de tokens gerados para a estimativa e o teto só como máximo, e o erro dessa fase fica em {_num_q4(fg['erro_abs_mediana_s'], 1)} s."),
        ("<strong>A barra nunca para antes do fim.</strong> Começa indeterminada com a etapa nomeada, vira determinada assim que a estimativa existe, sem trocar de forma, chega a 90% quando o tempo decorrido "
         "iguala a estimativa e depois segue devagar, com a estimativa refeita; Ctrl+C grava o estado como cancelado. Como a chamada ao modelo não é em fluxo, a fase mostrada é inferida pelo relógio, "
         "não observada: a correção token a token é a ficha 59."),
        (f"<strong>No histórico real, as três regras fizeram o que devem.</strong> A regra 1 rodou tudo em {', '.join(vereditos_txt['roda tudo']) or 'nenhum par'} (arquivos da aplicação que o mapa não conhece, "
         f"como estilos, scripts e configuração do projeto); a seleção foi parcial em {', '.join(vereditos_txt['seleção parcial']) or 'nenhum par'}, apontando o verbete e o endpoint de cada cenário; "
         f"e não rodou nada em {', '.join(vereditos_txt['nada a rodar']) or 'nenhum par'}, quando só a venv entrou ou saiu do git. O mapa dos includes do PHP liga <code>menu_publico.php</code> às páginas "
         "que o incluem, o que a lista de páginas sozinha não faria."),
        ("<strong>O que o protótipo não prova.</strong> O mapa é declarado à mão e aproximado (como o mapa do Azure DevOps): a conferência contra a rodada completa registra o que ficou de fora, mas medir o "
         "que a seleção perdeu exige rodar os cenários, o que fica para o pacote Q7, depois da Fase 5. A fumaça real da barra mede o erro de ponta a ponta numa inferência de verdade e depende do Eric."),
    ]
    html_ = f"""<section id="progresso" hidden>
<h1>{titulo}</h1>
<p class="lead">{lead_}</p>
{kpis(itens_kpi)}
<h2>Quanto a estimativa da barra erra, por fase</h2>
<div class="chart"><canvas id="g-prog-erro"></canvas></div>
{detalhes("As taxas do modelo, medida a medida", tab_taxas)}
{detalhes("O erro por fase, nos dois jeitos de tirar as taxas", tab_erro)}
<h2>A fumaça real com o modelo</h2>
{bloco_fumaca}
<h2>O que a seleção pelo diff do Git rodaria em cada commit das cobaias</h2>
<div class="chart"><canvas id="g-git-pares"></canvas></div>
{detalhes("A seleção par a par no histórico", tab_pares)}
{detalhes("Por que cada arquivo da aplicação contou", tab_motivos)}
{detalhes("O mapa dos cenários", tab_mapa)}
{detalhes("As três regras da base E", tab_regras)}
{leitura(itens_leitura)}
{fontes(["<code>resultados_alvo/fase4/taxas_progresso.json</code> (<code>progresso.py --taxas</code>, com <code>--check</code>)", "<code>erro_progresso.json</code> (<code>progresso.py --erro</code>)",
         "<code>impacto_git.json</code> (<code>impacto_git.py --prova</code>)", "<code>fumaca_progresso.json</code> (<code>progresso.py --fumaca</code>, depois da fumaça real)",
         "<code>experimentos/progresso.py</code> e <code>experimentos/impacto_git.py</code>", "plano aprovado da Pós-Fase 4, seções 3.5 e 3.7 (pacote Q4)", "levantamento §6.15.2 (indicador de progresso) e §6.15.5 (seleção pelo diff)"])}
</section>"""
    return dados_js, html_


# ! Alteração de IA - Revisar: (10/11/2026, Pós-Fase 4, pacote Q5) a aba "Revisão humana": a sessão com revisor humano dos relatórios v3 e das árvores de decisão da
# corrida 24 (leitura_revisao_v3.json, de avaliar_fase4.py --revisao_v3): a adesão apropriada por grupo, o erro localizado, o tempo até a decisão, a utilidade, a
# avaliação do revisor contra o gabarito e a tabela caso a caso com o comentário dele; dois gráficos pela paleta, cartões, "Como ler" e as tabelas recolhidas.
# Nenhum número digitado: tudo vem do JSON (o tempo da sessão de 05/11 vem de leitura_revisao_trilha.json, quando existe).
# ! Motivo: a ficha 40 foi fechada em 08/11/2026 pela opção (b) e a sessão rodou em 09 e 10/11/2026 na página com cronômetro; é a medida da especificação da
# trilha (seção 12 c) que a Fase 4 deixou como limitação declarada (decisões 87 e 95), e o Eric decide pelo painel.
# ! Alteração de IA - Revisar: (10/11/2026) a aba passou a dizer quem respondeu cada relatório (a tabela e o cartão "Quem respondeu") e a dar o tempo só onde a
# página mediu uma leitura; o parágrafo, os cartões e a leitura foram reescritos a partir de `por_origem`, `tempo` e `pagina` do JSON.
# ! Motivo: a versão publicada em 10/11/2026 dizia que o Eric tinha lido os 36 relatórios, com 31 s de mediana; no mesmo dia ele declarou que passou os relatórios
# a um analista e colou as respostas dele (decisão 114), e o registro da página mostra que o tempo medido era o da troca entre os dois.
def _n_q5(v, casas: int = 1) -> str:
    if v is None:
        return "n/d"
    return f"{v:.{casas}f}".replace(".", ",") if isinstance(v, float) else str(v)


def _wilson_q5(ic) -> str:
    return "n/d" if not ic else f"{_n_q5(float(ic[0]))} a {_n_q5(float(ic[1]))}"


def secao_revisao_v3(rev: dict | None, rev_trilha: dict | None = None) -> tuple[dict, str]:
    titulo = ("O relatório v3 com a árvore de decisão ajuda uma pessoa a decidir? A sessão de revisão da corrida 24: os 36 relatórios lidos um a um, às cegas, com a adesão "
              "apropriada, o erro localizado e a utilidade, e quem respondeu cada um.")
    if not rev:
        return {}, (f'<section id="revisaov3" hidden>\n<h1>{titulo}</h1>\n<p class="lead">A leitura da sessão ainda não foi gravada: falta <code>leitura_revisao_v3.json</code> em '
                    '<code>resultados_alvo/fase4/</code>, que sai de <code>avaliar_fase4.py --revisao_v3</code> depois de a planilha <code>revisao_v3.md</code> estar inteira.</p>\n</section>')
    r, a = rev["resumo"], rev["avaliacao"]
    ades = {x["grupo"]: x for x in rev["adesao"]}
    loc = {x["grupo"]: x for x in rev["localizacao"]}
    tempo = {x["grupo"]: x for x in rev["tempo"]}
    util = {x["grupo"]: x for x in rev["utilidade"]}
    origem = {x["origem"]: x for x in rev["por_origem"]}
    casos = rev["casos"]
    n = r["relatorios"]
    certos, errados = ades["diagnóstico certo"], ades["diagnóstico errado"]
    certos_recusados = [c for c in casos if c["acerto"] and c["decisao"] == "recusar"]
    errados_aceitos = [c for c in casos if not c["acerto"] and c["decisao"] == "aceitar"]
    notas = [str(v) for v in range(1, 6)]
    t_all = tempo["todos"]
    u_all, u_e = util["todos"], util["diagnóstico errado"]
    n_analista = (origem.get("analista") or {}).get("n", 0)
    n_eric = (origem.get("revisor") or {}).get("n", 0)
    pg = rev.get("pagina") or {}
    dados_js = {"adesao": {"grupos": [certos["grupo"], errados["grupo"]],
                           "series": [{"nome": "decisão apropriada", "cor": "--s1", "n": [certos["apropriadas"], errados["apropriadas"]]},
                                      {"nome": "decisão inapropriada", "cor": "--s4", "n": [certos["n"] - certos["apropriadas"], errados["n"] - errados["apropriadas"]]}]},
                "utilidade": {"notas": notas, "series": [{"nome": "diagnóstico certo", "cor": "--s1", "n": [util["diagnóstico certo"]["contagem"][v] for v in notas]},
                                                           {"nome": "diagnóstico errado", "cor": "--s4", "n": [u_e["contagem"][v] for v in notas]}]},
                "resumo": {"relatorios": n, "adesao_apropriada": r["adesao_apropriada"], "adesao_pct": r["adesao_pct"], "tempo_mediana_s": r["tempo_mediana_s"],
                           "utilidade_mediana": r["utilidade_mediana"], "erros_localizados": r["erros_localizados"], "erros_na_amostra": r["erros_na_amostra"],
                           "respostas_do_analista": n_analista, "respostas_do_eric": n_eric, "tempo_medido_em": t_all["n"]}}
    # ! Alteração de IA - Revisar: (10/11/2026, decisão 117) o caso de um leitor só: as respostas todas do analista, descrito pela declaração de `quem_leu`, e o tempo
    # sem número nenhum.
    # ! Motivo: o Eric declarou no quadro (ficha 62) que as 36 respostas são de um analista de QA da empresa, inclusive a do relatório 2, que a aba dava como dele, com
    # 214 s; a aba dizia "medido em 1 de 36" e que quem leu não estava registrado.
    quem_leu = rev.get("quem_leu") or {}
    o_analista = quem_leu.get("quem") or "um analista"
    so_o_analista = bool(n_analista) and not n_eric
    if so_o_analista:
        relacao = f", que {quem_leu['relacao_com_o_projeto']}" if quem_leu else ""
        quem = (f"Os {n} relatórios da corrida 24 foram lidos por {o_analista}{relacao}: o Eric passou cada relatório, ele devolveu a resposta e o Eric a digitou ou colou "
                "na página da sessão. ")
        frase_tempo = (f"O tempo até a decisão não foi medido em nenhum dos {n}: o que a página mediu foi a troca entre os dois"
                       + (f", com {pg['intervalo_entre_relatorios_mediana_s']} s na mediana entre abrir um relatório e abrir o seguinte" if pg else "") + ", não uma leitura. ")
    elif n_analista:
        quem = (f"Dos {n} relatórios da corrida 24, {n_analista} de {n} foram lidos por um analista: o Eric passou o relatório, ele devolveu a resposta e o Eric a colou na página da sessão; "
                f"{'o outro foi lido' if n_eric == 1 else f'os outros {n_eric} foram lidos'} pelo próprio Eric na página. ")
        frase_tempo = (f"O tempo até a decisão só foi medido em {t_all['n']} de {n} ({_n_q5(t_all['mediana'])} s): nos do analista, o que a página mediu foi a troca entre os dois"
                       + (f", com {pg['intervalo_entre_relatorios_mediana_s']} s na mediana entre abrir um relatório e abrir o seguinte" if pg else "") + ", não uma leitura. ")
    else:
        quem = f"O leitor leu os {n} relatórios da corrida 24 na página da sessão, um por vez. "
        frase_tempo = f"A decisão levou {_n_q5(t_all['mediana'])} s na mediana (de {t_all['minimo']} a {t_all['maximo']} s). "
    lead_ = (quem + "Todos sem o nome do caso, a classe nem o nível. "
             f"A decisão foi apropriada em {r['adesao_apropriada']} de {n} ({_n_q5(r['adesao_pct'])}%; Wilson 95% de {_wilson_q5(r['adesao_ic'])}): {certos['aceitou']} dos {certos['n']} diagnósticos "
             f"certos aceitos e {errados['recusou']} dos {errados['n']} errados recusados. Nos errados, o leitor achou onde está o erro do agente em {loc['diagnóstico errado']['sim']} de "
             f"{loc['diagnóstico errado']['n']}. A utilidade do relatório ficou em {_n_q5(r['utilidade_mediana'])} na mediana, com nota 5 em {u_all['contagem']['5']} dos {u_all['n']}. "
             + frase_tempo + f"A avaliação bateu com o gabarito em {a['acertos']} de {a['n']} ({_n_q5(a['pct'])}%).")
    kpi_quem = (("Quem respondeu", f"{n_analista} de {n}", f"respostas de um analista, coladas pelo Eric; {'a outra é' if n_eric == 1 else f'as outras {n_eric} são'} do Eric, lendo na página")
                if n_analista else ("Quem respondeu", f"{n_eric} de {n}", "respostas dadas na página por quem leu"))
    kpi_tempo = (("Tempo até a decisão", f"medido em {t_all['n']} de {n}", f"{_n_q5(t_all['mediana'])} s no relatório que o Eric leu na página; nos do analista a página mediu a troca entre os dois")
                 if n_analista else ("Tempo até a decisão", f"{_n_q5(t_all['mediana'])} s", f"mediana; de {t_all['minimo']} a {t_all['maximo']} s, medido pela página, descontadas as pausas"))
    if so_o_analista:
        kpi_quem = ("Quem respondeu", f"{n_analista} de {n}", f"respostas de {o_analista}, digitadas ou coladas pelo Eric na página")
        kpi_tempo = ("Tempo até a decisão", "não medido", f"não foi medido em nenhum dos {n}: a página mediu a troca entre os dois, não a leitura")
    itens_kpi = [("Decisões apropriadas", f"{r['adesao_apropriada']} de {n}", f"{_n_q5(r['adesao_pct'])}%; Wilson 95% de {_wilson_q5(r['adesao_ic'])}"),
                 ("Diagnósticos certos aceitos", f"{certos['aceitou']} de {certos['n']}", f"{_n_q5(certos['pct'])}%; os {certos['recusou']} recusados estão na leitura abaixo"),
                 ("Diagnósticos errados recusados", f"{errados['recusou']} de {errados['n']}", f"{_n_q5(errados['pct'])}%; {errados['aceitou']} aceito(s)"),
                 ("Erro do agente localizado", f"{loc['diagnóstico errado']['sim']} de {loc['diagnóstico errado']['n']}", "nos diagnósticos errados, o leitor disse onde o relatório mostra o erro"),
                 kpi_quem, kpi_tempo,
                 ("Utilidade do relatório", f"{_n_q5(r['utilidade_mediana'])} de 5", f"mediana; nota 5 em {u_all['contagem']['5']}, 4 em {u_all['contagem']['4']} e 3 em {u_all['contagem']['3']} dos {u_all['n']}")]
    rotulo = {"revisor": "resposta do Eric, lendo na página", "analista": "resposta de um analista, digitada ou colada pelo Eric", "parecer_aprovado": "parecer aprovado"}
    tab_origem = tabela(["Quem respondeu", "Relatórios", "Decisões apropriadas", "Apropriadas (%)", "Wilson 95%", "Avaliação igual ao gabarito"],
                        [[rotulo.get(x["origem"], x["origem"]), str(x["n"]), str(x["apropriadas"]), _n_q5(x["pct"]), _wilson_q5(x["ic"]), str(x["avaliacao_bate"])] for x in rev["por_origem"]])
    tab_adesao = tabela(["Grupo", "Relatórios", "Aceitou", "Recusou", "Apropriadas", "Apropriadas (%)", "Wilson 95%"],
                        [[x["grupo"], str(x["n"]), str(x["aceitou"]), str(x["recusou"]), str(x["apropriadas"]), _n_q5(x["pct"]), _wilson_q5(x["ic"])] for x in rev["adesao"]])
    tab_loc = tabela(["Grupo", "Relatórios", "Achou um erro", "Não achou", "Não viu erro", "Achou (%)", "Wilson 95%"],
                     [[x["grupo"], str(x["n"]), str(x["sim"]), str(x["nao"]), str(x["na"]), _n_q5(x["pct_sim"]), _wilson_q5(x["ic"])] for x in rev["localizacao"]])
    tab_tempo = tabela(["Grupo", "Relatórios com tempo medido", "Mediana (s)", "Mínimo (s)", "Máximo (s)"],
                       [[x["grupo"], str(x["n"]), _n_q5(x["mediana"]), _n_q5(x["minimo"]), _n_q5(x["maximo"])] for x in rev["tempo"]])
    tab_util = tabela(["Grupo", "Relatórios", "Mediana", "1", "2", "3", "4", "5"],
                      [[x["grupo"], str(x["n"]), _n_q5(x["mediana"])] + [str(x["contagem"][v]) for v in notas] for x in rev["utilidade"]])
    tab_aval = tabela(["Diagnóstico", "O leitor disse certo", "O leitor disse errado"],
                      [["certo", str(a["certo_disse_certo"]), str(a["certo_disse_errado"])], ["errado", str(a["errado_disse_certo"]), str(a["errado_disse_errado"])]])
    tab_casos = tabela(["#", "Caso", "Gabarito", "Rótulo do agente", "Resultado", "Selo", "Quem respondeu", "Tempo (s)", "Erro localizado", "Decisão", "Apropriada", "Utilidade", "Avaliação", "Comentário de quem leu"],
                       [[str(c["posicao"]), f"<code>{esc(c['caso'])}</code>", f"<code>{esc(c['gabarito'])}</code>", f"<code>{esc(c['rotulo'])}</code>", "certo" if c["acerto"] else "errado",
                         esc(str(c["selo"])), "analista" if c["origem"] == "analista" else "Eric", "não medido" if c["segundos"] is None else str(c["segundos"]), esc(c["erro_localizado"]), esc(c["decisao"]),
                         "sim" if c["apropriada"] else "não", str(c["utilidade"]), esc(c["avaliacao"]), esc(c["comentario"])] for c in casos], raw=True)

    def lista(cs: list[dict]) -> str:
        return ", ".join(f"<code>relatorio-{c['posicao']}</code> (<code>{esc(c['caso'])}</code>, <code>{esc(c['rotulo'])}</code>)" for c in cs) or "nenhum"

    if so_o_analista:
        item_tempo = ("<strong>O tempo de leitura não foi medido.</strong> "
                      + (f"Pelo registro da página, entre abrir um relatório e abrir o seguinte passaram {pg['intervalo_entre_relatorios_mediana_s']} s na mediana, e o comentário, com "
                         f"{pg['comentario_mediana_chars']} caracteres na mediana, foi salvo {pg['decisao_ao_salvamento_mediana_s']} s depois da decisão: em {pg['comentarios_acima_de_10_chars_por_s']} "
                         f"dos {pg['comentarios_medidos']} relatórios não trocados depois, ele entrou mais depressa do que se digita, isto é, chegou pronto e foi colado. " if pg else "")
                      + "O que a página mediu foi a troca entre os dois, não a leitura. As versões desta aba publicadas em 10/11/2026 davam primeiro 31 s de mediana como tempo de "
                      "leitura dos 36 e depois o tempo medido em um relatório, o segundo, cuja resposta o Eric digitou na página: eram tempos da troca, e saíram.")
        data_decl = "/".join(reversed(quem_leu["declarado_em"][:10].split("-"))) if quem_leu else ""
        sem_declarar = [x for x, k in (("o que ele recebeu para ler", "o_que_recebeu"), ("se usou alguma ferramenta para ler ou redigir", "ferramenta_de_ia")) if not quem_leu.get(k)]
        item_limite = ("<strong>O que esta medida é e o que ela não é.</strong> Quem leu os relatórios foi uma pessoa que não é o autor do trabalho, como a ficha 40 pedia"
                       + (f": {esc(o_analista)}, que {esc(quem_leu['relacao_com_o_projeto'])}, pela declaração do Eric em {data_decl}" if quem_leu else "")
                       + ". Ela decidiu sem o nome do caso, a classe nem o nível. "
                       + (f"Não foi declarado {' nem '.join(sem_declarar)}, e o tempo não foi medido. " if sem_declarar else "O tempo não foi medido. ")
                       + "É um leitor só. A medida fica feita na adesão, na localização e na utilidade, e em aberto no tempo (decisão 114, que revê a 113, e decisão 117, que "
                       "fecha a ficha 62).")
    elif n_analista:
        item_tempo = ("<strong>O tempo de leitura não foi medido.</strong> "
                      + (f"Pelo registro da página, entre abrir um relatório e abrir o seguinte passaram {pg['intervalo_entre_relatorios_mediana_s']} s na mediana, e o comentário, com "
                         f"{pg['comentario_mediana_chars']} caracteres na mediana, foi salvo {pg['decisao_ao_salvamento_mediana_s']} s depois da decisão: em {pg['comentarios_acima_de_10_chars_por_s']} "
                         f"dos {pg['comentarios_medidos']} relatórios não trocados depois, ele entrou mais depressa do que se digita, isto é, chegou pronto e foi colado. " if pg else "")
                      + f"O que a página mediu nesses relatórios foi a troca entre os dois, não a leitura; o tempo só vale no relatório que o Eric leu na página ({_n_q5(t_all['mediana'])} s). "
                      "A versão desta aba publicada em 10/11/2026 dava 31 s de mediana como tempo de leitura dos 36: era o tempo da troca, e saiu.")
        item_limite = ("<strong>O que esta medida é e o que ela não é.</strong> Quem leu quase todos os relatórios foi uma pessoa que não é o autor do trabalho, como a ficha 40 pedia, e ela decidiu sem "
                       "o nome do caso, a classe nem o nível. Mas não está registrado quem é o analista, o que ele conhecia do agente, o que recebeu para ler nem se usou alguma ferramenta para ler ou "
                       "redigir, e o tempo não foi medido. A medida fica feita na adesão, na localização e na utilidade, e em aberto no tempo e na descrição de quem leu (decisão 114, que revê a 113; "
                       "ficha 62).")
    else:
        t05 = next((x for x in (rev_trilha or {}).get("tempo", []) if x["grupo"] == "todos" and x.get("mediana") is not None), None)
        contra_05 = f" (contra {_n_q5(t05['mediana'])} s no único relatório respondido com tempo na sessão de 05/11/2026, no formato antigo)" if t05 else ""
        item_tempo = (f"<strong>O tempo até a decisão.</strong> A mediana foi de {_n_q5(t_all['mediana'])} s por relatório{contra_05}, medida pela página só com o relatório à vista.")
        item_limite = ("<strong>O que esta medida não é.</strong> Um leitor só; a medida com mais de um revisor continua como limitação declarada (ficha 40).")
    itens_leitura = [
        (f"<strong>O relatório deixa o leitor decidir certo na maior parte das vezes, e recusar o errado quase sempre.</strong> Das {n} decisões, {r['adesao_apropriada']} foram "
         f"apropriadas; nos {errados['n']} diagnósticos errados o leitor recusou {errados['recusou']} e localizou o erro do agente em {loc['diagnóstico errado']['sim']}, e nos {certos['n']} certos "
         f"aceitou {certos['aceitou']}. A nota 5 de utilidade em {u_all['contagem']['5']} dos {u_all['n']} diz que o relatório bastou para decidir; ela cai um pouco nos diagnósticos errados "
         f"(mediana {_n_q5(u_e['mediana'])}, com nota 3 em {u_e['contagem']['3']} deles)."),
        (f"<strong>Onde o leitor divergiu do gabarito.</strong> Foram recusados {len(certos_recusados)} diagnóstico(s) certo(s): {lista(certos_recusados)}. Nos comentários, o motivo é o mesmo em todos: "
         "a causa respondida não estava em nenhum dos verbetes entregues pela busca (a divergência que a árvore marca como causa sem verbete que a trate), e o leitor tratou a resposta fora do "
         f"contexto como erro do agente, embora a causa estivesse certa. Foi aceito {len(errados_aceitos)} diagnóstico(s) errado(s): {lista(errados_aceitos)}, em que a causa respondida parecia "
         "sustentada pelo sintoma."),
        item_tempo,
        item_limite,
    ]
    bloco_tempo = detalhes("Tempo até a decisão, só onde a página mediu uma leitura", tab_tempo) + "\n" if t_all["n"] else ""
    html_ = f"""<section id="revisaov3" hidden>
<h1>{titulo}</h1>
<p class="lead">{lead_}</p>
{kpis(itens_kpi)}
<h2>Adesão apropriada por grupo: aceitar o certo, recusar o errado</h2>
<div class="chart"><canvas id="g-revv3-adesao"></canvas></div>
<h2>Utilidade do relatório, de 1 a 5, por grupo</h2>
<div class="chart"><canvas id="g-revv3-utilidade"></canvas></div>
{detalhes("Quem respondeu", tab_origem)}
{detalhes("Adesão apropriada", tab_adesao)}
{detalhes("Erro localizado", tab_loc)}
{bloco_tempo}{detalhes("Utilidade percebida", tab_util)}
{detalhes("Avaliação de quem leu contra o gabarito", tab_aval)}
{detalhes("Os 36 relatórios, um a um, com o comentário de quem leu", tab_casos)}
{leitura(itens_leitura)}
{fontes(["<code>resultados_alvo/fase4/leitura_revisao_v3.json</code> (<code>avaliar_fase4.py --revisao_v3</code>, com <code>--check</code>)",
         "<code>resultados_alvo/fase4/revisao_v3.md</code> (a planilha da sessão) e <code>sessao_revisao_v3/</code> (as cópias lidas, o registro da página em <code>respostas.json</code>, o que foi para a planilha em <code>respostas_planilha.json</code> e a declaração de quem leu em <code>quem_leu.json</code>)",
         "<code>experimentos/revisao_v3.py</code> e <code>ferramentas/sessao_revisao.py --perfil v3</code>", "especificação da trilha, seção 12 c; fichas 40 e 62 e decisões 113, 114 e 117",
         "<code>resultados_alvo/fase4/leitura_revisao_trilha.json</code> (a sessão de 05/11/2026)"])}
</section>"""
    return dados_js, html_


# ! Alteração de IA - Revisar: (10/11/2026, ficha 63 opção b, decisão 116) a aba "Notas do modelo": a prévia sem modelo da corrida 25 (sem_notas_previa.json) e, quando
# a corrida tiver rodado, os pares contra as corridas 22 e 24 e o veredito (sem_notas.json). Nenhum número é digitado aqui.
# ! Motivo: o Eric escolheu no quadro medir quanto pesam as notas que o modelo escreveu na biblioteca; a corrida roda na janela dele, e a aba diz o que já se sabe
# sem o modelo, qual é a regra fixada antes e, depois, o resultado. Pela regra do painel, toda análise vira uma aba lida do JSON gravado.
NOME_DO_BANCO_SEM_NOTAS = {"avaliacao": "os 36 oficiais de avaliação", "ineditos": "os 36 inéditos da ficha 27"}
CORES_DA_MUDANCA = {"contexto idêntico": "--s3", "mesmos verbetes, sem as notas": "--s1", "mesmos verbetes, outra ordem": "--s4", "verbetes diferentes": "--s2"}


def _p_q5(v) -> str:
    return "n/d" if v is None else f"{v:.3f}".replace(".", ",")


def secao_sem_notas(previa: dict | None, lei: dict | None = None) -> tuple[dict, str]:
    titulo = ("As notas que o modelo escreveu na biblioteca ajudam ou atrapalham o diagnóstico? A corrida 25: a biblioteca de produção sem as notas do modelo e sem os verbetes "
              "aprendidos, nos 36 casos oficiais e nos 36 inéditos, contra as corridas 22 e 24.")
    if not previa:
        return {}, (f'<section id="semnotas" hidden>\n<h1>{titulo}</h1>\n<p class="lead">A prévia sem modelo ainda não foi gravada: falta <code>sem_notas_previa.json</code> em '
                    '<code>resultados_alvo/fase4/</code>, que sai de <code>python experimento_sem_notas.py --previa</code>.</p>\n</section>')
    b, r, bancos = previa["biblioteca"], previa["resumo"], previa["por_banco"]
    n = r["casos"]
    lote = "/".join(reversed(str(b.get("lote_promovido_em") or "")[:10].split("-")))

    def codigos(ids) -> str:
        return ", ".join(f"<code>{esc(i)}</code>" for i in ids) or "nenhum"

    dados_js = {"previa": {"casos": n, "grupos": [NOME_DO_BANCO_SEM_NOTAS.get(x["banco"], x["banco"]) for x in bancos],
                           "series": [{"nome": m, "cor": CORES_DA_MUDANCA[m], "n": [next(y["casos"] for y in x["mudancas"] if y["mudanca"] == m) for x in bancos]} for m in CORES_DA_MUDANCA]}}
    # o gráfico dos pares existe sempre: antes da corrida só com os acertos das referências; depois, com os acertos sem as notas ao lado
    serie_ref = {"nome": "acertos com a biblioteca inteira (corridas 22 e 24)", "cor": "--s4", "n": [x["acertos_referencia"] for x in bancos]}
    dados_js["pares"] = {"grupos": dados_js["previa"]["grupos"], "series": [serie_ref]}
    o_que_se_sabe = (f"A biblioteca de produção tem {b['notas_retiradas']} notas do modelo em {b['verbetes_com_notas']} dos {b['verbetes_producao']} verbetes, "
                     f"{b['notas_em_forma_de_instrucao']} de {b['notas_retiradas']} escritas como instrução. Nas corridas de referência, {r['com_nota_na_referencia']} de {n} contextos traziam "
                     f"ao menos uma nota e {r['com_aprendido_na_referencia']} de {n} traziam um verbete aprendido. Sem as notas, o contexto entregue ao modelo muda em "
                     f"{r['contextos_que_mudam']} de {n}: em {r['mesmos_verbetes_sem_as_notas']} os verbetes são os mesmos, na mesma ordem, só sem as notas; em "
                     f"{r['mesmos_verbetes_outra_ordem']} mudam de ordem; em {r['verbetes_diferentes']} a busca troca um verbete. O verbete da causa certa estava entre os entregues em "
                     f"{r['verbete_certo_antes']} casos e continua em {r['verbete_certo_depois']}.")
    itens_kpi = [("Notas do modelo na biblioteca", f"{b['notas_retiradas']} notas", (f"em {b['verbetes_com_notas']} dos {b['verbetes_producao']} verbetes; {b['notas_em_forma_de_instrucao']} de "
                                                                                    f"{b['notas_retiradas']} escritas como instrução")),
                 ("Contextos que mudam sem as notas", f"{r['contextos_que_mudam']} de {n}", (f"{r['mesmos_verbetes_sem_as_notas']} só perdem as notas; {r['mesmos_verbetes_outra_ordem']} mudam de ordem; "
                                                                                    f"{r['verbetes_diferentes']} trocam um verbete")),
                 ("Verbetes aprendidos nos contextos", f"{r['com_aprendido_na_referencia']} de {n}", "nenhum contexto de referência trazia verbete aprendido: nestes casos a corrida mede as notas"),
                 ("Verbete da causa certa entre os entregues", f"{r['verbete_certo_depois']} de {n}", f"eram {r['verbete_certo_antes']} com as notas; a presença muda em {r['verbete_certo_mudou']} casos"),
                 ("Acertos das corridas de referência", f"{r['acertos_referencia']} de {n}", "com a biblioteca de produção inteira: "
                  + " e ".join(f"{x['acertos_referencia']} de {x['casos']} na {x['referencia']}" for x in bancos)),
                 ("Tamanho da biblioteca", f"{b['tokens_estimados_sem_notas']} tokens", f"contra {b['tokens_estimados_producao']} com as notas e os aprendidos (estimativa da biblioteca inteira)")]
    tab_bib = tabela(["Biblioteca", "Hash", "Verbetes", "Notas do modelo", "Verbetes com nota", "Notas em forma de instrução", "Tokens estimados"],
                     [["produção", f"<code>{esc(b['origem_hash'])}</code>", str(b["verbetes_producao"]), str(b["notas_retiradas"]), str(b["verbetes_com_notas"]), str(b["notas_em_forma_de_instrucao"]),
                       str(b["tokens_estimados_producao"])],
                      ["sem as notas e sem os aprendidos", f"<code>{esc(b['hash'])}</code>", str(b["verbetes_sem_notas"]), "0", "0", "0", str(b["tokens_estimados_sem_notas"])]], raw=True)
    tab_bancos = tabela(["Banco", "Referência", "Casos", "Com nota na referência", "Com verbete aprendido na referência"] + [m[0].upper() + m[1:] for m in CORES_DA_MUDANCA]
                        + ["Caracteres do contexto (mediana) na referência", "Caracteres do contexto (mediana) sem as notas"],
                        [[NOME_DO_BANCO_SEM_NOTAS.get(x["banco"], x["banco"]), x["referencia"], str(x["casos"]), str(x["com_nota_na_referencia"]), str(x["com_aprendido_na_referencia"])]
                         + [str(next(y["casos"] for y in x["mudancas"] if y["mudanca"] == m)) for m in CORES_DA_MUDANCA]
                         + [_n_q5(x["chars_do_contexto_mediana_referencia"]), _n_q5(x["chars_do_contexto_mediana_sem_notas"])] for x in bancos])
    tab_trocas = tabela(["Caso", "Banco", "Saiu", "Entrou", "Verbetes na referência", "Verbetes sem as notas"],
                        [[f"<code>{esc(x['caso'])}</code>", esc(x["banco"]), codigos(x["saiu"]), codigos(x["entrou"]), codigos(x["antes"]), codigos(x["depois"])]
                         for x in previa["casos_com_verbetes_diferentes"]] or [["nenhum", "", "", "", "", ""]], raw=True)
    item_mede = (f"<strong>O que a corrida mede.</strong> Tirar as notas muda o texto de {r['contextos_que_mudam']} dos {n} prompts e, em "
                 f"{r['mesmos_verbetes_outra_ordem'] + r['verbetes_diferentes']}, também o que a busca entrega, porque o texto das notas entra no índice da busca. Como "
                 f"{r['com_aprendido_na_referencia']} de {n} contextos traziam verbete aprendido, a retirada deles não pesa nestes casos: a corrida mede as notas.")
    item_regra = f"<strong>A regra foi fixada antes da corrida.</strong> {esc(previa['regra'])}"
    item_16 = ("<strong>Por que as corridas 22 e 24, e não a 16.</strong> A ficha 63 citava a corrida 16 para os casos oficiais. Ela leu a biblioteca de antes do lote"
               + (f" de {lote}" if lote else "") + ", em outra versão do Ollama; a corrida 22 leu os mesmos 36 casos com a biblioteca de hoje. Cada caso é pareado com a corrida 22 (oficiais) ou a "
               "corrida 24 (inéditos), e a corrida 16 entra como segunda comparação.")
    item_ponte = ("<strong>A ponte da versão do Ollama.</strong> As referências rodaram numa versão, e o Ollama se atualiza sozinho. Se a versão no ar não tiver ponte, o lançador roda a ponte "
                  "antes (a biblioteca original nos 36 casos de avaliação, regra R6); sem ponte pareável a leitura sai sem veredito.")
    fontes_ = ["<code>resultados_alvo/fase4/sem_notas_previa.json</code> (<code>experimento_sem_notas.py --previa</code>, com <code>--check</code>)",
               "<code>resultados_alvo/fase4/sem_notas.json</code>, quando a corrida tiver rodado (<code>avaliar_fase4.py --sem_notas</code>)",
               "<code>experimentos/experimento_sem_notas.py</code> e o lançador <code>experimentos/rodar_experimento_sem_notas.ps1</code>",
               "as referências: <code>resultados_alvo/fase4_trilha/</code> (corrida 22), <code>fase4_ineditos/</code> (corrida 24) e <code>fase4_calibracao/k3/</code> (corrida 16)",
               "ficha 63 e decisão 116; <code>3-resultados-e-analises/parecer-do-analista-2026-11-10.md</code>"]
    if not lei:
        lead_ = ("A corrida 25 ainda não rodou: está pronta para o Eric lançar da janela dele, com <code>rodar_experimento_sem_notas.ps1</code> (ficha 63, decisão 116). O que já se sabe sem "
                 "o modelo: " + o_que_se_sabe + f" Pela mediana das corridas de referência, as {r['inferencias']} inferências levam cerca de "
                 f"{r['minutos_estimados_pela_mediana_das_referencias']} minutos, mais a ponte da versão do Ollama, se faltar.")
        itens_kpi.append(("Corrida 25", "pronta para rodar", f"cerca de {r['minutos_estimados_pela_mediana_das_referencias']} minutos de modelo para {r['inferencias']} inferências, mais a ponte"))
        blocos_resultado, itens_resultado = "", []
    else:
        s, regra = lei["resumo"], lei["regra"]
        ponte = regra.get("ponte") or {}
        if regra.get("mesma_versao_das_referencias"):
            sobre_a_ponte = "A corrida rodou na mesma versão do Ollama das referências."
        elif ponte:
            sobre_a_ponte = (f"A ponte da versão do Ollama da corrida (<code>{esc(str(ponte.get('corrida')))}</code>) deu b = {ponte.get('b')} e c = {ponte.get('c')} em {ponte.get('n')} casos, "
                             f"{'pareável' if ponte.get('pareavel') else 'não pareável'} com a Fase 3.")
        else:
            sobre_a_ponte = "A versão do Ollama da corrida não tem ponte registrada."
        lead_ = (f"Veredito pela regra fixada antes: {esc(s['veredito'])}. Sem as notas do modelo, o agente acertou {s['acertos_sem_notas']} de {s['casos']} ({_n_q5(s['acerto_sem_notas_pct'])}%); "
                 f"com a biblioteca de produção inteira, {s['acertos_referencia']} de {s['casos']} ({_n_q5(s['acerto_referencia_pct'])}%). Passaram a acertar {s['b']} casos e passaram a errar "
                 f"{s['c']} (p do teste pareado = {_p_q5(s['p'])}); o rótulo ficou igual em {s['mesmo_rotulo']}. {sobre_a_ponte} " + o_que_se_sabe)
        itens_kpi = [("Veredito", esc(s["veredito"]), f"teste pareado dos {s['casos']} casos: p = {_p_q5(s['p'])}; o corte é 0,05"),
                     ("Acertos sem as notas", f"{s['acertos_sem_notas']} de {s['casos']}", f"{_n_q5(s['acerto_sem_notas_pct'])}%; Wilson 95% de {_n_q5(s.get('wilson_lo_pct'))} a {_n_q5(s.get('wilson_hi_pct'))}"),
                     ("Acertos com a biblioteca inteira", f"{s['acertos_referencia']} de {s['casos']}", f"{_n_q5(s['acerto_referencia_pct'])}%, nas corridas 22 e 24"),
                     ("Passaram a acertar e a errar", f"{s['b']} e {s['c']}", f"saldo de {s['saldo']}; o rótulo ficou igual em {s['mesmo_rotulo']} casos")] + itens_kpi
        dados_js["pares"] = {"grupos": [NOME_DO_BANCO_SEM_NOTAS.get(x["banco"], x["banco"]) for x in lei["por_banco"]],
                             "series": [{"nome": "acertos sem as notas", "cor": "--s1", "n": [x["acertos_sem_notas"] for x in lei["por_banco"]]},
                                        {**serie_ref, "n": [x["acertos_referencia"] for x in lei["por_banco"]]}]}
        tab_res = tabela(["Banco", "Referência", "Casos", "Acertos sem as notas", "Acertos na referência", "Passaram a acertar (b)", "Passaram a errar (c)", "p do teste pareado", "Mesmo rótulo",
                          "Quais passaram a acertar", "Quais passaram a errar"],
                         [[NOME_DO_BANCO_SEM_NOTAS.get(x["banco"], x["banco"]), esc(x["referencia"]), str(x["casos"]), str(x["acertos_sem_notas"]), str(x["acertos_referencia"]), str(x["b"]), str(x["c"]),
                           _p_q5(x["p"]), str(x["mesmo_rotulo"]), codigos(x["ganhos"]), codigos(x["perdas"])] for x in lei["por_banco"]], raw=True)
        tab_mud = tabela(["O que mudou no contexto", "Casos", "Acertos sem as notas", "Acertos na referência", "Passaram a acertar (b)", "Passaram a errar (c)", "Mesmo rótulo"],
                         [[x["mudanca"], str(x["casos"]), str(x["acertos_sem_notas"]), str(x["acertos_referencia"]), str(x["b"]), str(x["c"]), str(x["mesmo_rotulo"])] for x in lei["por_mudanca_do_contexto"]])
        c16 = lei.get("contra_a_corrida_16")
        tab_16 = tabela(["Casos oficiais também lidos na corrida 16", "Acertos sem as notas", "Acertos na corrida 16", "Passaram a acertar (b)", "Passaram a errar (c)", "p do teste pareado",
                         "Biblioteca da corrida 16", "Ollama da corrida 16"],
                        [[str(c16["casos"]), str(c16["acertos_sem_notas"]), str(c16["acertos_referencia"]), str(c16["b"]), str(c16["c"]), _p_q5(c16["p"]), f"<code>{esc(c16['biblioteca'])}</code>",
                          esc(c16["versao_ollama"])]] if c16 else [["sem os registros da corrida 16", "", "", "", "", "", "", ""]], raw=True)
        mudaram = [c for c in lei["casos"] if c.get("mudou")]
        tab_casos = tabela(["Caso", "Banco", "Gabarito", "Rótulo sem as notas", "Rótulo na referência", "Mudou", "O que mudou no contexto", "Verbetes sem as notas", "Verbetes na referência"],
                           [[f"<code>{esc(c['caso'])}</code>", esc(c["banco"]), f"<code>{esc(str(c['gabarito']))}</code>", f"<code>{esc(str(c['rotulo']))}</code>",
                             f"<code>{esc(str(c['rotulo_referencia']))}</code>", esc(c["mudou"]), esc(c["mudanca_do_contexto"]), codigos(c["verbetes_ids"]), codigos(c["verbetes_ids_referencia"])]
                            for c in mudaram] or [["nenhum caso mudou de acerto", "", "", "", "", "", "", "", ""]], raw=True)
        blocos_resultado = "\n".join([detalhes("Os pares por banco", tab_res), detalhes("Os pares pelo que mudou no contexto", tab_mud),
                                      detalhes("Segunda comparação: os casos oficiais contra a corrida 16", tab_16), detalhes("Os casos que mudaram de acerto", tab_casos)]) + "\n"
        itens_resultado = [(f"<strong>O resultado.</strong> {esc(s['veredito'][0].upper() + s['veredito'][1:])}: {s['b']} casos passaram a acertar sem as notas e {s['c']} passaram a errar, "
                            f"com p = {_p_q5(s['p'])} no teste pareado dos {s['casos']} casos. Pela decisão 116, o agente só muda se a diferença sair do ruído, e mudar é outra decisão.")]
    html_ = f"""<section id="semnotas" hidden>
<h1>{titulo}</h1>
<p class="lead">{lead_}</p>
{kpis(itens_kpi)}
<h2>Acertos por banco: com a biblioteca inteira e, depois da corrida, sem as notas</h2>
<div class="chart"><canvas id="g-semnotas-pares"></canvas></div>
<h2>O que muda no contexto de cada caso quando as notas saem</h2>
<div class="chart"><canvas id="g-semnotas-contexto"></canvas></div>
{blocos_resultado}{detalhes("A biblioteca com e sem as notas", tab_bib)}
{detalhes("A prévia por banco", tab_bancos)}
{detalhes("Os casos em que a busca troca um verbete", tab_trocas)}
{leitura(itens_resultado + [item_mede, item_regra, item_16, item_ponte])}
{fontes(fontes_)}
</section>"""
    return dados_js, html_


# ! Alteração de IA - Revisar: (10/11/2026, ficha 66 opção b, decisão 120) a aba "Segundo passe": a prévia sem modelo da corrida 26 (segundo_passe_previa.json) e, quando a
# corrida tiver rodado, o que a segunda resposta consertaria e estragaria, o que a regra de escolha trocou e o veredito (segundo_passe.json). Nenhum número é digitado aqui.
# ! Motivo: o Eric escolheu no quadro medir o segundo passe do diagnóstico antes da Fase 5; a corrida roda na janela dele, e a aba diz o que a conta sem modelo já mostra (o
# teto do ganho e por que o resultado não tem como sair do ruído), qual é a regra fixada antes, que desenhos foram descartados e, depois, o resultado. Pela regra do painel,
# toda análise vira uma aba lida do JSON gravado.
def secao_segundo_passe(previa: dict | None, lei: dict | None = None) -> tuple[dict, str]:
    titulo = ("Um segundo pedido de diagnóstico, só quando um sinal acende e com outros verbetes, conserta mais do que estraga? A corrida 26: os casos das corridas 22 e 24 "
              "com o selo baixo ou a FONTE divergente, com os verbetes seguintes da mesma busca e a escolha entre as duas respostas por regra em código.")
    if not previa:
        return {}, (f'<section id="segpasse" hidden>\n<h1>{titulo}</h1>\n<p class="lead">A prévia sem modelo ainda não foi gravada: falta <code>segundo_passe_previa.json</code> em '
                    '<code>resultados_alvo/fase4/</code>, que sai de <code>python experimento_segundo_passe.py --previa</code>.</p>\n</section>')
    r, des, sinais = previa["resumo"], previa["desenho"], previa["por_sinal"]
    primeiro, entre_os_seguintes, fora = des["alcances"]
    grupos = [x["sinal"] for x in sinais]
    posicoes = f"posições {des['posicoes'][0]} a {des['posicoes'][-1]}"

    def codigos(ids) -> str:
        return ", ".join(f"<code>{esc(i)}</code>" for i in ids) or "nenhum"

    def conta(grupo: str, acerto: bool, alcances: tuple) -> int:
        return sum(1 for c in previa["casos"] if c["sinal"] == grupo and c["acerto_primeira"] is acerto and c["alcance"] in alcances)

    series_alcance = [("erros com o verbete da causa certa entre os seguintes", "--bom", False, (entre_os_seguintes,)),
                      ("erros com o verbete da causa certa já entregue no primeiro pedido", "--s4", False, (primeiro,)),
                      ("erros com o verbete da causa certa fora dos dois pedidos", "--s7", False, (fora,)),
                      ("acertos que perdem o verbete da causa certa", "--ruim", True, (primeiro,)),
                      ("acertos que não tinham o verbete da causa certa", "--s1", True, (entre_os_seguintes, fora))]
    dados_js = {"alcance": {"grupos": grupos, "series": [{"nome": nome, "cor": cor, "n": [conta(g, acerto, alc) for g in grupos]} for nome, cor, acerto, alc in series_alcance]}}
    # o gráfico do resultado existe sempre: antes da corrida só com os erros e os acertos da primeira resposta; depois, com o que a segunda faria e o que a regra trocou
    series_primeira = [{"nome": "erros na primeira resposta", "cor": "--s2", "n": [x["erros"] for x in sinais]}, {"nome": "acertos na primeira resposta", "cor": "--s1", "n": [x["acertos"] for x in sinais]}]
    dados_js["resultado"] = {"grupos": grupos, "series": series_primeira}
    o_que_se_sabe = (f"Um sinal em código acendeu na primeira resposta de {r['com_sinal']} de {r['casos']} casos das corridas 22 e 24: {r['so_selo_baixo']} só com o selo baixo, "
                     f"{r['so_fonte_divergente']} só com a FONTE divergente e {r['os_dois_sinais']} com os dois. Neles estão {r['erros_com_sinal']} dos {r['erros']} erros das duas corridas e "
                     f"{r['acertos_com_sinal']} acertos. O verbete da causa certa fica entre os que o segundo pedido entrega em {r['erros_ao_alcance']} dos {r['erros_com_sinal']} erros com sinal; "
                     f"em {r['erros_com_o_verbete_certo_ja_entregue']} ele já estava no primeiro pedido, e em {r['erros_fora_do_alcance']} fica fora dos dois. Dos {r['acertos_com_sinal']} "
                     f"acertos com sinal, {r['acertos_que_perdem_o_verbete_certo']} tinham o verbete da causa certa no primeiro pedido e deixam de recebê-lo no segundo.")
    itens_kpi = [("Casos com sinal", f"{r['com_sinal']} de {r['casos']}", f"{r['so_selo_baixo']} só com o selo baixo, {r['so_fonte_divergente']} só com a FONTE divergente, {r['os_dois_sinais']} com os dois"),
                 ("Erros que os sinais pegam", f"{r['erros_com_sinal']} dos {r['erros']}", f"e {r['acertos_com_sinal']} acertos também recebem o segundo pedido; {r['erros_sem_sinal']} erros ficam sem sinal"),
                 ("Erros com o verbete certo ao alcance", f"{r['erros_ao_alcance']} dos {r['erros_com_sinal']}", (f"{r['erros_com_o_verbete_certo_ja_entregue']} já o tinham no primeiro pedido e "
                                                                                                     f"{r['erros_fora_do_alcance']} ficam fora dos dois")),
                 ("Acertos que perdem o verbete certo", f"{r['acertos_que_perdem_o_verbete_certo']} dos {r['acertos_com_sinal']}", "tinham o verbete da causa certa entre os três primeiros"),
                 ("Melhor cenário do teste pareado", f"p = {_p_q5(r['p_do_melhor_cenario'])}", (f"com os {r['erros_ao_alcance']} erros ao alcance consertados e nenhum acerto perdido; para passar do "
                                                                                           f"corte de 0,05 seriam {r['consertos_para_sair_do_ruido']} consertos sem perda")),
                 ("Tamanho do segundo pedido", f"{_n_q5(r['tokens_estimados_mediana'], 0)} tokens", (f"mediana estimada, contra {_n_q5(r['tokens_mediana_do_primeiro_pedido'], 0)} do primeiro; "
                                                                                                f"{r['acima_do_limite']} de {r['com_sinal']} acima do limite de {des['limite_de_tokens']} da tela"))]
    tab_sinal = tabela(["Sinal aceso na primeira resposta", "Casos", "Erros", "Acertos", "Erros com o verbete certo entre os seguintes", "Acertos que perdem o verbete certo"],
                       [[x["sinal"], str(x["casos"]), str(x["erros"]), str(x["acertos"]), str(x["erros_ao_alcance"]), str(x["acertos_que_perdem_o_verbete_certo"])] for x in sinais])
    tab_banco = tabela(["Banco", "Primeira resposta", "Casos do banco", "Com sinal", "Erros com sinal", "Acertos com sinal", "Erros com o verbete certo entre os seguintes"],
                       [[NOME_DO_BANCO_SEM_NOTAS.get(x["banco"], x["banco"]), x["referencia"], str(x["casos"]), str(x["com_sinal"]), str(x["erros_com_sinal"]), str(x["acertos_com_sinal"]),
                         str(x["erros_ao_alcance"])] for x in previa["por_banco"]])
    tab_alt = tabela(["Desenho do segundo pedido", "Verbetes no pedido", "Erros com o verbete certo ao alcance", "Tokens estimados (mediana)", "Tokens estimados (máximo)",
                      "Acima do limite de tokens", "O que ficou"],
                     [[x["desenho"], str(x["verbetes_no_pedido"]), str(x["erros_ao_alcance"]), _n_q5(x["tokens_estimados_mediana"]), str(x["tokens_estimados_maximo"]), str(x["acima_do_limite"]), x["motivo"]]
                      for x in previa["alternativas"]])
    tab_casos_previa = tabela(["Caso", "Banco", "Sinal", "Gabarito", "Primeira resposta", "Certa", "Probabilidade", "Posição do verbete certo na busca", "Verbete da causa certa",
                               "Verbetes do segundo pedido", "Tokens estimados"],
                              [[f"<code>{esc(c['caso'])}</code>", esc(c["banco"]), esc(c["sinal"]), f"<code>{esc(c['gabarito'])}</code>", f"<code>{esc(str(c['rotulo_primeira']))}</code>",
                                "sim" if c["acerto_primeira"] else "não", _p_q5(c["p_primeira"]), "n/d" if c["posicao_do_verbete_certo"] is None else str(c["posicao_do_verbete_certo"]),
                                esc(c["alcance"]), codigos(c["seguintes"]), str(c["tokens_estimados"])] for c in previa["casos"]], raw=True)
    item_mede = (f"<strong>O que a corrida mede.</strong> Só nos {r['com_sinal']} casos com sinal, o agente recebe um segundo pedido de diagnóstico, uma única vez: o mesmo prompt congelado, o "
                 f"mesmo modelo e os {des['verbetes_seguintes']} verbetes seguintes da mesma busca ({posicoes}) no lugar dos três primeiros. A primeira resposta é a que a corrida de referência "
                 "gravou e não é repetida, e o segundo pedido não fala dela. A leitura conta quantos erros a segunda resposta conserta e quantas respostas certas ela estraga, por sinal.")
    item_teto = (f"<strong>O resultado não tem como sair do ruído.</strong> O verbete da causa certa só fica ao alcance do segundo pedido em {r['erros_ao_alcance']} dos "
                 f"{r['erros_com_sinal']} erros com sinal. Com os {r['erros_ao_alcance']} consertados e nenhum acerto perdido, o teste pareado dá p = {_p_q5(r['p_do_melhor_cenario'])}; para "
                 f"passar do corte seriam precisos {r['consertos_para_sair_do_ruido']} consertos sem nenhuma perda. A corrida serve para contar o que o segundo passe conserta e o que estraga.")
    item_regra = f"<strong>A regra foi fixada antes da corrida.</strong> {esc(previa['regra'])}"
    item_desenho = (f"<strong>Por que só os verbetes seguintes, e por que {des['verbetes_seguintes']}.</strong> Juntar os três primeiros aos seguintes repete o contexto da primeira resposta, que "
                    "é o desenho que a pesquisa diz que troca resposta certa por errada, e passa do limite de tokens em quase todos os casos. Com três verbetes o pedido tem o mesmo tamanho do "
                    "primeiro e do que calibrou o selo; com dois o alcance é o mesmo, mas o pedido sai do que foi calibrado; com sete o alcance cresce e o prompt quase dobra. A tabela dos "
                    "desenhos traz os números de cada um.")
    item_ponte = ("<strong>A ponte da versão do Ollama.</strong> As primeiras respostas vieram de uma versão, e o Ollama se atualiza sozinho. A fila roda antes a ponte da versão que estiver "
                  "no ar (regra R6); sem ponte pareável a leitura sai sem veredito.")
    fontes_ = ["<code>resultados_alvo/fase4/segundo_passe_previa.json</code> (<code>experimento_segundo_passe.py --previa</code>, com <code>--check</code>)",
               "<code>resultados_alvo/fase4/segundo_passe.json</code>, quando a corrida tiver rodado (<code>avaliar_fase4.py --segundo_passe</code>)",
               "<code>experimentos/experimento_segundo_passe.py</code>, o modo <code>segundo_passe</code> de <code>rodar_fase4.ps1</code> e a fila <code>experimentos/rodar_fila_pre_fase5.ps1</code>",
               "as primeiras respostas: <code>resultados_alvo/fase4_trilha/</code> (corrida 22) e <code>fase4_ineditos/</code> (corrida 24)",
               "ficha 66 e decisão 120; levantamento §6.16.4 e §6.16.5; <code>dados/pesquisa-fluxo-do-agente/medidas_do_repositorio.json</code>"]
    if not lei:
        lead_ = ("A corrida 26 ainda não rodou: está pronta para o Eric lançar da janela dele, pela fila <code>rodar_fila_pre_fase5.ps1</code> ou sozinha (ficha 66, decisão 120). O que já se "
                 "sabe sem o modelo: " + o_que_se_sabe + f" No melhor cenário o teste pareado dá p = {_p_q5(r['p_do_melhor_cenario'])}, acima do corte de 0,05. Pelo tempo das corridas de "
                 f"referência, as {r['inferencias']} inferências levam cerca de {r['minutos_estimados']} minutos.")
        itens_kpi.append(("Corrida 26", "pronta para rodar", f"cerca de {r['minutos_estimados']} minutos de modelo para {r['inferencias']} inferências, depois da ponte"))
        blocos_resultado, itens_resultado = "", []
    else:
        s, regra = lei["resumo"], lei["regra"]
        ponte = regra.get("ponte") or {}
        if regra.get("mesma_versao_das_referencias"):
            sobre_a_ponte = "A corrida rodou na mesma versão do Ollama das corridas de referência."
        elif ponte:
            sobre_a_ponte = (f"A ponte da versão do Ollama da corrida (<code>{esc(str(ponte.get('corrida')))}</code>) deu b = {ponte.get('b')} e c = {ponte.get('c')} em {ponte.get('n')} casos, "
                             f"{'pareável' if ponte.get('pareavel') else 'não pareável'} com a Fase 3.")
        else:
            sobre_a_ponte = "A versão do Ollama da corrida não tem ponte registrada."
        lead_ = (f"Veredito pela regra fixada antes: {esc(s['veredito'])}. Se a segunda resposta valesse sempre, ela consertaria {s['consertaria']} dos {s['erros_primeira_com_sinal']} erros com "
                 f"sinal e estragaria {s['estragaria']} dos {s['acertos_primeira_com_sinal']} acertos com sinal. Pela regra de escolha, a resposta trocou em {s['trocas']} casos: {s['b']} passaram "
                 f"a acertar e {s['c']} passaram a errar (p do teste pareado = {_p_q5(s['p'])}), e o agente iria de {s['acertos_primeira']} a {s['acertos_final']} acertos em {s['casos']}. "
                 f"{sobre_a_ponte} " + o_que_se_sabe)
        itens_kpi = [("Veredito", esc(s["veredito"]), f"teste pareado: p = {_p_q5(s['p'])}; o corte é 0,05"),
                     ("A segunda resposta consertaria", f"{s['consertaria']} dos {s['erros_primeira_com_sinal']}", "erros com sinal, se ela valesse sempre"),
                     ("A segunda resposta estragaria", f"{s['estragaria']} dos {s['acertos_primeira_com_sinal']}", f"acertos com sinal, se ela valesse sempre; a causa foi a mesma em {s['mesmo_rotulo']} casos"),
                     ("Pela regra de escolha", f"{s['b']} ganhos e {s['c']} perdas", f"{s['trocas']} trocas; o agente iria de {s['acertos_primeira']} a {s['acertos_final']} acertos em {s['casos']}"),
                     ("Tamanho medido do segundo pedido", f"{_n_q5(s['tokens_entrada_mediana'], 0)} tokens", (f"mediana, contra {_n_q5(s['tokens_entrada_mediana_primeira'], 0)} do primeiro; "
                                                                                                         f"{s['acima_do_limite']} acima do limite de {s['limite_de_tokens']}; {_n_q5(s['segundos_mediana'])} s por caso"))] + itens_kpi
        por_sinal = {x["sinal"]: x for x in lei["por_sinal"]}
        # depois da corrida os erros e os acertos da primeira resposta são os dos casos que tiveram o segundo pedido (numa corrida completa, os mesmos da prévia)
        series_da_leitura = [{**series_primeira[0], "n": [por_sinal.get(g, {}).get("erros_primeira", 0) for g in grupos]},
                             {**series_primeira[1], "n": [por_sinal.get(g, {}).get("acertos_primeira", 0) for g in grupos]}]
        dados_js["resultado"] = {"grupos": grupos, "series": series_da_leitura + [
            {"nome": "a segunda resposta consertaria", "cor": "--bom", "n": [por_sinal.get(g, {}).get("consertaria", 0) for g in grupos]},
            {"nome": "a segunda resposta estragaria", "cor": "--ruim", "n": [por_sinal.get(g, {}).get("estragaria", 0) for g in grupos]},
            {"nome": "passaram a acertar pela regra", "cor": "--s3", "n": [por_sinal.get(g, {}).get("b", 0) for g in grupos]},
            {"nome": "passaram a errar pela regra", "cor": "--s8", "n": [por_sinal.get(g, {}).get("c", 0) for g in grupos]}]}
        cab_grupo = ["Casos com segundo passe", "Erros na primeira resposta", "Acertos na primeira resposta", "A segunda consertaria", "A segunda estragaria", "Mesma causa nas duas",
                     "Trocas pela regra", "Passaram a acertar (b)", "Passaram a errar (c)"]

        def linha(x: dict, casos: int | None = None) -> list[str]:
            return [str(x["casos"] if casos is None else casos), str(x["erros_primeira"]), str(x["acertos_primeira"]), str(x["consertaria"]), str(x["estragaria"]), str(x["mesmo_rotulo"]),
                    str(x["trocas"]), str(x["b"]), str(x["c"])]

        tab_res_sinal = tabela(["Sinal aceso na primeira resposta", *cab_grupo], [[x["sinal"], *linha(x)] for x in lei["por_sinal"]])
        tab_res_banco = tabela(["Banco", "Primeira resposta", "Casos do banco", "Com sinal", *cab_grupo],
                               [[NOME_DO_BANCO_SEM_NOTAS.get(x["banco"], x["banco"]), x["referencia"], str(x["casos"]), str(x["com_sinal"]), *linha(x, x["segundos_passes"])] for x in lei["por_banco"]])
        tab_res_alcance = tabela(["Onde está o verbete da causa certa", *cab_grupo], [[x["alcance"], *linha(x)] for x in lei["por_alcance"]])
        tab_regras = tabela(["Se a escolha fosse", "Trocas de causa", "Passariam a acertar (b)", "Passariam a errar (c)", "Acertos nos casos todos", "p do teste pareado"],
                            [[x["regra"], str(x["trocas"]), str(x["b"]), str(x["c"]), str(x["acertos"]), _p_q5(x["p"])] for x in lei["por_regra"]])
        tab_motivos = tabela(["O que a regra de escolha achou", "Casos", "Fica"], [[x["motivo"], str(x["casos"]), "a segunda" if x["troca"] else "a primeira"] for x in lei["motivos"]])
        tab_casos = tabela(["Caso", "Banco", "Sinal", "Gabarito", "Primeira resposta", "Probabilidade", "Segunda resposta", "Probabilidade", "A segunda sozinha", "Fica", "Motivo", "Mudou",
                            "Verbetes do segundo pedido", "Tokens de entrada"],
                           [[f"<code>{esc(c['caso'])}</code>", esc(c["banco"]), esc(str(c["sinal"])), f"<code>{esc(str(c['gabarito']))}</code>", f"<code>{esc(str(c['rotulo_primeira']))}</code>",
                             _p_q5(c["p_primeira"]), f"<code>{esc(str(c['rotulo_segunda']))}</code>", _p_q5(c["p_segunda"]), esc(c["efeito_da_segunda"]), f"a {esc(c['fica'])}", esc(c["motivo"]),
                             esc(c["mudou"]), codigos(c["verbetes_segunda"]), str(c["tokens_entrada"])] for c in lei["casos"]] or [["nenhum"] + [""] * 13], raw=True)
        blocos_resultado = "\n".join([detalhes("O resultado por sinal", tab_res_sinal), detalhes("O resultado por banco", tab_res_banco),
                                      detalhes("O resultado pelo lugar do verbete da causa certa", tab_res_alcance), detalhes("O que cada regra de escolha daria", tab_regras),
                                      detalhes("Os motivos da regra de escolha", tab_motivos), detalhes("Os casos com segundo passe, um a um", tab_casos)]) + "\n"
        itens_resultado = [(f"<strong>O resultado.</strong> {esc(s['veredito'][0].upper() + s['veredito'][1:])}: a segunda resposta sozinha consertaria {s['consertaria']} erros e estragaria "
                            f"{s['estragaria']} acertos; pela regra de escolha, {s['b']} casos passaram a acertar e {s['c']} passaram a errar, com p = {_p_q5(s['p'])} no teste pareado. Pela "
                            "decisão 120, o agente só muda se a diferença sair do ruído, e mudar é outra decisão.")]
    html_ = f"""<section id="segpasse" hidden>
<h1>{titulo}</h1>
<p class="lead">{lead_}</p>
{kpis(itens_kpi)}
<h2>Erros e acertos da primeira resposta por sinal e, depois da corrida, o que o segundo passe conserta e estraga</h2>
<div class="chart"><canvas id="g-segpasse-resultado"></canvas></div>
<h2>O que o segundo pedido alcança: onde está o verbete da causa certa nos casos com sinal</h2>
<div class="chart"><canvas id="g-segpasse-alcance"></canvas></div>
{blocos_resultado}{detalhes("A prévia por sinal", tab_sinal)}
{detalhes("A prévia por banco", tab_banco)}
{detalhes("Os desenhos do segundo pedido: o escolhido e os descartados", tab_alt)}
{detalhes("Os casos com sinal, um a um, antes da corrida", tab_casos_previa)}
{leitura(itens_resultado + [item_mede, item_teto, item_regra, item_desenho, item_ponte])}
{fontes(fontes_)}
</section>"""
    return dados_js, html_


# ! Alteração de IA - Revisar: (10/11/2026, ficha 67 opção b, decisão 121) a aba "Analista de documentação": a medida M1 (portoes_m1.json: os portões 3, 4 e 5 da proposta de
# desenho aplicados às 92 propostas da corrida 20, contra a revisão humana do lote) e a corrida 27, que é a medida M2 (a prévia sem modelo e, depois, a leitura). Nenhum
# número é digitado aqui.
# ! Motivo: o Eric aprovou a proposta do analista de documentação como base de desenho e pediu as duas medidas antes da Fase 5; a M1 já rodou, sem modelo, e a corrida 27
# roda na janela dele. Pela regra do painel, toda análise vira uma aba lida do JSON gravado, e é por ela que o Eric decide.
CORES_DO_VEREDITO = {"Correta": "--bom", "Parcial": "--meio", "Errada": "--ruim"}
PLURAL_DO_VEREDITO = {"Correta": ("correta", "corretas"), "Parcial": ("parcial", "parciais"), "Errada": ("errada", "erradas")}


def _vereditos_por_extenso(x: dict) -> str:
    """Os vereditos de um grupo de edições com o plural certo: "1 correta, 8 parciais e 6 erradas"."""
    partes = [f"{x[v]} {um if x[v] == 1 else varios}" for v, (um, varios) in PLURAL_DO_VEREDITO.items()]
    return f"{partes[0]}, {partes[1]} e {partes[2]}"


def _bloco_m1(m1: dict) -> tuple[dict, list, str, list, list]:
    """Os dados dos dois gráficos, os cartões, as tabelas recolhidas, os itens de leitura e as fontes da medida M1."""
    r, portoes, vered = m1["resumo"], m1["por_portao"], m1["resumo"]["por_veredito"]
    etapas = m1["em_sequencia"] + m1["outras_sequencias"]

    def recusa(p: dict, veredito: str) -> int:
        return next(x["recusa"] for x in p["nas_revisadas"]["por_veredito"] if x["veredito"] == veredito)

    def de(p: dict, veredito: str) -> str:
        return f"{recusa(p, veredito)} de {vered[veredito]}"

    dados_js = {"portoes": {"grupos": [p["nome"] for p in portoes],
                            "series": [{"nome": "edições erradas que recusaria", "cor": "--bom", "n": [recusa(p, "Errada") for p in portoes]},
                                       {"nome": "edições parciais que recusaria", "cor": "--meio", "n": [recusa(p, "Parcial") for p in portoes]},
                                       {"nome": "edições corretas que perderia", "cor": "--ruim", "n": [recusa(p, "Correta") for p in portoes]}]},
                "sequencia": {"grupos": [x["etapa"] for x in etapas],
                              "series": [{"nome": PLURAL_DO_VEREDITO[v][1], "cor": CORES_DO_VEREDITO[v], "n": [x[v] for x in etapas]} for v in CORES_DO_VEREDITO]}}
    forma, texto, busca = portoes
    final, sem_forma = m1["em_sequencia"][-1], m1["outras_sequencias"][0]
    itens_kpi = [("Propostas da corrida 20", str(r["propostas"]), f"em {r['casos']} casos; {r['revisadas']} passaram nos filtros de hoje e foram revisadas por uma pessoa"),
                 ("Revisão humana do lote", f"{vered['Correta']} corretas", f"{vered['Parcial']} parciais e {vered['Errada']} erradas, em {r['revisadas']}"),
                 ("Portão 3, a forma de instrução", f"{r['forma_recusa']} das {r['propostas']}", (f"recusaria; nas revisadas, {de(forma, 'Errada')} erradas, {de(forma, 'Parcial')} parciais e "
                                                                                             f"{de(forma, 'Correta')} corretas")),
                 ("Portão 4, os filtros de texto", f"{r['texto_recusa']} das {r['propostas']}", (f"recusaria; nas revisadas, {de(texto, 'Errada')} erradas, {de(texto, 'Parcial')} parciais e "
                                                                                            f"{de(texto, 'Correta')} corretas")),
                 ("Portão 5, a busca", f"{r['busca_recusa']} das {r['revisadas']}", (f"edições recusadas: {de(busca, 'Errada')} erradas, {de(busca, 'Parcial')} parciais e "
                                                                                 f"{de(busca, 'Correta')} corretas; o verbete certo sai {m1['busca']['verbete_certo_sai']} vezes e entra "
                                                                                 f"{m1['busca']['verbete_certo_entra']}")),
                 ("Os três portões em sequência", f"{r['sobram_depois_dos_tres']} de {r['revisadas']}", (f"edições sobram: {_vereditos_por_extenso(final)}; sem o portão da forma sobram "
                                                                                                     f"{sem_forma['sobram']} ({_vereditos_por_extenso(sem_forma)})"))]
    tab_portoes = tabela(["Portão", "Regra", "Recusa nas propostas", "Passa nas propostas", "Não se aplica", "Recusa nas revisadas", "Erradas recusadas", "Parciais recusadas",
                          "Corretas perdidas"],
                         [[p["nome"], p["regra"], str(p["nas_propostas"]["recusa"]), str(p["nas_propostas"]["passa"]), str(p["nas_propostas"]["nao_se_aplica"]),
                           str(p["nas_revisadas"]["recusa"]), de(p, "Errada"), de(p, "Parcial"), de(p, "Correta")] for p in portoes])
    tab_seq = tabela(["Etapa", "Edições que sobram", "Corretas", "Parciais", "Erradas"], [[x["etapa"], str(x["sobram"]), str(x["Correta"]), str(x["Parcial"]), str(x["Errada"])] for x in etapas])
    tab_destino = tabela(["O que os filtros de hoje fizeram", "Propostas", "O portão 3 recusaria", "O portão 4 recusaria"],
                         [[x["destino"], str(x["propostas"]), str(x["forma_recusa"]), str(x["texto_recusa"])] for x in m1["por_destino"]])
    tab_criterios = tabela(["Medida do portão 4", "Propostas reprovadas", "Reprovadas entre as revisadas"],
                           [[x["nome"], str(x["reprovadas"]), str(x["reprovadas_nas_revisadas"])] for x in m1["criterios_do_texto"]])
    tab_palavras = tabela(["Primeira palavra do texto", "Propostas", "O portão 3"],
                          [[f"<code>{esc(x['palavra'])}</code>", str(x["propostas"]), "recusa" if x["recusada_pela_forma"] else "passa"] for x in m1["primeiras_palavras"]], raw=True)

    def passa(v) -> str:
        return "n/a" if v is None else ("passa" if v else "recusa")

    tab_revisadas = tabela(["Caso", "Verbete", "Operação", "Revisão humana", "Portão 3", "Portão 4", "Portão 5", "Verbete certo entra", "Verbete certo sai", "Passa nos três", "Texto"],
                           [[f"<code>{esc(i['caso'])}</code>", f"<code>{esc(str(i['verbete']))}</code>", esc(str(i["operacao"])), esc(i["veredito"]), passa(i["forma"]["passa"]),
                             passa(i["texto_passa"]), passa(i["busca"]["passa"]), str(i["busca"]["verbete_certo_entra"]), str(i["busca"]["verbete_certo_sai"]),
                             "sim" if i["passa_nos_tres"] else "não", esc(i["texto"])] for i in m1["revisadas"]], raw=True)
    blocos = "\n".join([detalhes("M1: cada portão contra a revisão humana", tab_portoes), detalhes("M1: os portões em sequência", tab_seq),
                        detalhes("M1: os portões 3 e 4 pelo que os filtros de hoje fizeram com a proposta", tab_destino), detalhes("M1: as medidas do portão 4 que reprovam", tab_criterios),
                        detalhes("M1: a primeira palavra de cada proposta", tab_palavras), detalhes("M1: as 20 edições revisadas, uma a uma", tab_revisadas)])
    itens = [(f"<strong>M1: o que cada portão barraria.</strong> O portão 3 (a forma de instrução) recusaria {r['forma_recusa']} das {r['propostas']} propostas da corrida 20. Entre as "
              f"{r['revisadas']} revisadas, recusaria {de(forma, 'Errada')} erradas e {de(forma, 'Parcial')} parciais, e perderia {de(forma, 'Correta')} corretas: aplicado ao que o modelo "
              "escreve hoje, ele esvazia o lote. Só faz sentido com um prompt que peça a frase como ela vai ficar no verbete, e é isso que a corrida 27 mede."),
             (f"<strong>M1: o portão da busca e o dos filtros de texto.</strong> O portão 5 recusaria {de(busca, 'Errada')} erradas e {de(busca, 'Parcial')} parciais, e perderia "
              f"{de(busca, 'Correta')} corretas, olhando só o efeito da edição na busca dos {m1['busca']['casos_com_gabarito']} casos com gabarito. O portão 4 recusaria {de(texto, 'Errada')} "
              f"erradas e {de(texto, 'Parcial')} parciais, e perderia {de(texto, 'Correta')} corretas."),
             (f"<strong>M1: os portões não substituem a pessoa.</strong> Em sequência, os três deixariam {r['sobram_depois_dos_tres']} de {r['revisadas']} edições "
              f"({_vereditos_por_extenso(final)}, pela revisão humana). Sem o portão da forma sobrariam {sem_forma['sobram']} ({_vereditos_por_extenso(sem_forma)}). Nenhum portão em código "
              "diz se a afirmação é verdadeira: a aprovação de uma pessoa continua sendo a porta final."),
             (f"<strong>M1: a contagem da forma mudou.</strong> A pesquisa da ficha 64 contou {r['forma_pela_lista_da_pesquisa']} propostas em forma de instrução, com cinco radicais; a lista "
              f"fechada do portão pega também \"Retificar\", \"Adicionado\", \"Cria\" e os rótulos seguidos de dois-pontos, e chega a {r['forma_recusa']}.")]
    fontes_ = ["<code>resultados_alvo/fase4/portoes_m1.json</code> (<code>experimentos/portoes_de_edicao.py --m1</code>, com <code>--check</code>)",
               "<code>resultados_alvo/fase4_biblioteca/</code> (as propostas, o lote e a revisão do lote da corrida 20) e <code>limiares_texto.json</code>",
               "<code>5-metodo-e-ferramental/proposta-analista-de-documentacao.md</code>, seções 4.5 e 6; ficha 67 e decisão 121"]
    return dados_js, itens_kpi, blocos, itens, fontes_


# ! Alteração de IA - Revisar: (11/11/2026, decisão 121) a parte da corrida 27 (medida M2) na aba "Analista de documentação": lê `analista_previa.json` (os 54 casos, a
# ficha curta, o tamanho do pedido, as instruções congeladas com o hash e quanto cada leitura precisa mostrar) e, depois da corrida, `analista.json` (as três leituras
# contra a corrida 20, os cinco portões, o que aconteceu com cada resposta e a revisão humana às cegas, quando já foi gravada). Nenhum número é digitado aqui.
# ! Motivo: a corrida 27 roda na janela do Eric, e o prompt do analista é a peça que ele aprova antes; a aba mostra o texto inteiro do prompt, o que a conta sem modelo
# já diz e, depois, o resultado. Os dois gráficos existem antes e depois da corrida, porque todo gráfico da página tem a sua leitura em `painel_leituras`.
_FRACAO = re.compile(r"(\d+) de (\d+)")
GRUPOS_DAS_LEITURAS_M2 = ["abstenção", "afirmam um fato", "corretas na revisão humana"]
GRUPOS_DE_LACUNA_M2 = [("com lacuna na documentação", True), ("sem lacuna", False)]


def _fracao(texto: str) -> float | None:
    """'5 de 6' vira 83,3 (percentual, uma casa); o que não é uma contagem, como 'sem revisão', fica sem barra."""
    m = _FRACAO.fullmatch(str(texto).strip())
    if not m or int(m.group(2)) == 0:
        return None
    return round(100 * int(m.group(1)) / int(m.group(2)), 1)


def _bloco_m2(previa: dict, lei: dict | None) -> tuple[dict, str, list, str, list, list]:
    """Os dados dos dois gráficos, o parágrafo do estado, os cartões, as tabelas recolhidas, os itens de leitura e as fontes da corrida 27 (medida M2)."""
    p, c20, prompt, poder = previa["resumo"], previa["corrida_20"], previa["prompt"], previa["poder"]
    casos_previa = previa["casos"]
    erros_com_lacuna = sum(1 for c in casos_previa if c["lacuna"] and not c["acertou"])

    def bruto(texto: str) -> str:
        return '<pre class="bruto"><code>' + html.escape(str(texto), quote=False) + "</code></pre>"

    def sim(v) -> str:
        return "sim" if v else "não"

    rotulos_20 = [f"{c20['abstencoes']} de {c20['casos']}", f"{c20['afirmacoes']} de {c20['com_texto']}", f"{c20['por_veredito']['Correta']} de {c20['passaram_nos_filtros']}"]
    series_leituras = [{"nome": "corrida 20", "cor": "--s1", "n": [_fracao(x) for x in rotulos_20], "rotulos": rotulos_20}]
    chamaria = [sum(1 for c in casos_previa if c["seria_chamado"] and bool(c["lacuna"]) is valor) for _, valor in GRUPOS_DE_LACUNA_M2]
    series_casos = [{"nome": "casos do grupo", "cor": "--s1", "n": [p["com_lacuna"], p["sem_lacuna"]]}, {"nome": "o desenho chamaria o analista", "cor": "--s4", "n": chamaria}]
    tab_casos_previa = tabela(["Caso", "De onde o diagnóstico leu", "Diagnóstico certo", "Causa respondida", "Causa certa", "Selo", "Posição do verbete certo na busca", "Com lacuna",
                               "O verbete já registra o caso", "O desenho chamaria o analista", "Tokens da ficha", "Tokens do pedido"],
                              [[f"<code>{esc(c['caso'])}</code>", esc(c["origem"]), sim(c["acertou"]), f"<code>{esc(str(c['causa_respondida']))}</code>", f"<code>{esc(str(c['gabarito']))}</code>",
                                esc(str(c["selo"])), "n/d" if c["posicao_do_ouro"] is None else str(c["posicao_do_ouro"]), sim(c["lacuna"]), sim(c["verbete_ja_registra_o_caso"]),
                                sim(c["seria_chamado"]), str(c["ficha_tokens"]), str(c["prompt_tokens"])] for c in casos_previa], raw=True)
    blocos_previa = [detalhes(f"M2: as instruções do analista, a parte fixa do prompt (hash {prompt['hash_das_instrucoes']})", bruto(prompt["instrucoes"])),
                     detalhes(f"M2: o prompt inteiro de um caso ({prompt['caso_do_exemplo']}): as instruções, o verbete da causa certa e a ficha curta", bruto(prompt["exemplo"])),
                     detalhes(f"M2: os {p['casos']} casos antes da corrida", tab_casos_previa)]
    item_mede = (f"<strong>M2: o que a corrida 27 mede.</strong> Nos {p['casos']} casos de aprendizado da corrida 20, o mesmo modelo é chamado no papel de analista de documentação: recebe "
                 "instruções próprias, o verbete da causa certa e uma ficha curta do caso, montada por código a partir da trilha da corrida 20, com o gabarito no lugar da decisão da pessoa. "
                 "Devolve uma proposta só (um sinal de busca, uma nota ou uma retificação) ou responde que não há o que acrescentar. A biblioteca é a de antes do lote da corrida 20 "
                 f"(<code>{esc(p['biblioteca'])}</code>) e só é lida; nada do agente muda.")
    item_regra = f"<strong>M2: a regra foi fixada antes da corrida.</strong> {esc(previa['regra'])}"
    item_poder = (f"<strong>M2: quanto cada leitura precisa mostrar.</strong> Contra a corrida 20, a abstenção sai do ruído com {poder['abstencoes_para_sair_do_ruido']} casos ou mais (lá foram "
                  f"{rotulos_20[0]}); a forma do texto, com {poder['afirmacoes_em_54_para_sair_do_ruido']} afirmações ou mais se as {p['casos']} respostas forem propostas com texto (lá foram "
                  f"{rotulos_20[1]}); a parcela correta, com {poder['corretas_em_20_para_sair_do_ruido']} corretas ou mais em {c20['passaram_nos_filtros']} revisadas (lá foram {rotulos_20[2]}).")
    item_lacuna = (f"<strong>M2: onde há o que escrever.</strong> A proposta de desenho só chama o analista quando há lacuna na documentação: o diagnóstico errou, ou nenhum verbete entregue "
                   f"tratava da causa respondida. Isso acontece em {p['com_lacuna']} de {p['casos']} casos ({erros_com_lacuna} erros do diagnóstico e {p['acertos_com_lacuna']} acertos), e em "
                   f"{p['verbete_ja_registra_o_caso']} casos o verbete da causa certa já registra o caso. A corrida chama o analista nos {p['casos']}, para medir também se ele se abstém onde "
                   "não há o que acrescentar.")
    item_portoes = ("<strong>M2: os cinco portões, sem modelo.</strong> Cada proposta passa pelo validador da Fase 3 e pelos filtros da Fase 4 (os dois são os filtros de hoje), pelo portão "
                    "da forma de instrução, pelos filtros de texto e pelo portão da busca. As que passam nos filtros de hoje vão para a revisão humana, como na corrida 20.")
    # ! Alteração de IA - Revisar: (11/11/2026, decisão 123) o item da revisão e a lista de fontes passaram a dizer que quem revisa as propostas é o Eric.
    # ! Motivo: o texto dizia que quem revisa era resposta dele, ainda por vir; ele respondeu a ficha 69 no quadro ("Eu reviso"). O campo de quem respondeu continua
    # sendo gravado só na hora da revisão, por `revisao_propostas.py --gravar --quem`.
    item_revisao = ("<strong>M2: a revisão humana é às cegas.</strong> Depois da corrida, <code>ferramentas/revisao_propostas.py --gerar</code> monta a página e a planilha com as propostas da "
                    f"corrida 27 e, por padrão, as {c20['passaram_nos_filtros']} edições da corrida 20 que já foram revisadas, em ordem embaralhada e sem dizer a origem, para a mesma pessoa "
                    "julgar as duas. A cegueira tem um limite: o tipo verbete novo só existe na corrida 20, e o jeito de escrever pode denunciar a origem. Quem revisa é o Eric "
                    "(ficha 69, decisão 123); o registro de quem respondeu é gravado na hora da revisão.")
    fontes_ = ["<code>resultados_alvo/fase4/analista_previa.json</code> (<code>experimentos/experimento_analista.py --previa</code>, com <code>--check</code>)",
               "<code>resultados_alvo/fase4/analista.json</code>, quando a corrida 27 tiver rodado (<code>avaliar_fase4.py --analista</code>)",
               ("<code>experimentos/experimento_analista.py</code>, o modo <code>analista</code> de <code>rodar_fase4.ps1</code>, a fila <code>experimentos/rodar_fila_pre_fase5.ps1</code> e "
                "<code>ferramentas/revisao_propostas.py</code>"),
               "ficha 68 e decisão 122 (o prompt do analista); ficha 69 e decisão 123 (o Eric revisa as propostas às cegas)"]
    if not lei:
        # ! Alteração de IA - Revisar: (11/11/2026, decisão 122) a frase do estado passou a dizer que o Eric aprovou o prompt como está.
        # ! Motivo: ela dizia que o prompt era a peça que o Eric aprova antes de rodar; ele respondeu a ficha 68 no quadro ("Sim, como está"), e a corrida só espera o lançamento.
        estado = (f"A corrida 27 (a medida M2) ainda não rodou. O código, os testes e a prévia sem modelo estão prontos, e o prompt do analista (hash "
                  f"<code>{esc(prompt['hash_das_instrucoes'])}</code>) foi aprovado pelo Eric como está (ficha 68, decisão 122). Ela roda pela fila <code>rodar_fila_pre_fase5.ps1</code> ou "
                  f"sozinha: {p['inferencias']} inferências, cerca de {p['minutos_estimados']} minutos de modelo, depois da ponte da versão do Ollama.")
        itens_kpi = [("Corrida 27 (medida M2)", "ainda não rodou", f"{p['inferencias']} inferências, cerca de {p['minutos_estimados']} minutos de modelo, depois da ponte da versão do Ollama"),
                     ("Casos de aprendizado da corrida 20", str(p["casos"]), (f"{p['origem_tela']} lidos da tela e {p['origem_fixture']} do fixture; o diagnóstico acertou "
                                                                            f"{p['acertos_do_diagnostico']} e errou {p['erros_do_diagnostico']}")),
                     ("Casos com lacuna na documentação", f"{p['com_lacuna']} de {p['casos']}", (f"{erros_com_lacuna} erros do diagnóstico e {p['acertos_com_lacuna']} acertos sem verbete que "
                                                                                             f"trate da causa; o desenho chamaria o analista em {p['seriam_chamados']}")),
                     ("Ficha curta do caso", f"{_n_q5(p['ficha_tokens_mediana'])} tokens", (f"mediana estimada; a maior tem {p['ficha_tokens_maximo']}, e o orçamento é de "
                                                                                          f"{p['orcamento_da_ficha']} ({p['fichas_acima_do_orcamento']} acima)")),
                     ("Tamanho do pedido", f"{_n_q5(p['prompt_tokens_mediana'])} tokens", (f"mediana estimada (máximo {p['prompt_tokens_maximo']}), contra "
                                                                                         f"{_n_q5(p['prompt_tokens_da_proposta_de_hoje'], 0)} da proposta de edição de hoje; cerca de "
                                                                                         f"{_n_q5(p['segundos_estimados_mediana'])} s por chamada, contra {_n_q5(p['segundos_da_proposta_de_hoje'])}")),
                     ("Instruções do analista", str(prompt["hash_das_instrucoes"]), (f"hash da parte fixa do prompt, com cerca de {prompt['instrucoes_tokens']} tokens; o texto inteiro está "
                                                                                    "recolhido abaixo"))]
        blocos, itens = blocos_previa, [item_mede, item_regra, item_poder, item_lacuna, item_portoes, item_revisao]
    else:
        s, regra, rev = lei["resumo"], lei["regra"], lei.get("revisao")
        le = {x["leitura"]: x for x in lei["leituras"]}
        ab, fo, pc = le["abstencao"], le["forma"], le["parcela_correta"]
        ponte = regra.get("ponte") or {}
        if regra.get("mesma_versao_da_corrida_20"):
            sobre_a_ponte = "A corrida rodou na mesma versão do Ollama da corrida 20."
        elif ponte:
            sobre_a_ponte = (f"A ponte da versão do Ollama da corrida (<code>{esc(str(ponte.get('corrida')))}</code>) deu b = {ponte.get('b')} e c = {ponte.get('c')} em {ponte.get('n')} casos, "
                             f"{'pareável' if ponte.get('pareavel') else 'não pareável'} com a Fase 3.")
        else:
            sobre_a_ponte = "A versão do Ollama da corrida não tem ponte registrada."
        estado = (f"A corrida 27 (a medida M2) rodou em {s['casos']} casos: {s['abstencoes']} abstenções, {s['sem_bloco']} respostas sem proposta válida e {s['propostas']} propostas. "
                  f"Abstenção: {esc(ab['corrida_27'])}, contra {esc(ab['corrida_20'])} na corrida 20 ({esc(ab['veredito'])}). Forma do texto: {esc(fo['corrida_27'])} propostas com texto afirmam "
                  f"um fato, contra {esc(fo['corrida_20'])} ({esc(fo['veredito'])}). Parcela correta na revisão humana: {esc(pc['corrida_27'])}, contra {esc(pc['corrida_20'])} "
                  f"({esc(pc['veredito'])}). {sobre_a_ponte}")
        itens_kpi = [("Abstenção", ab["corrida_27"], f"casos em que o analista respondeu que não há o que acrescentar; na corrida 20, {ab['corrida_20']}; p = {_p_q5(ab['p'])}: {ab['veredito']}"),
                     ("Forma do texto", fo["corrida_27"], f"propostas com texto que afirmam um fato; na corrida 20, {fo['corrida_20']}; p = {_p_q5(fo['p'])}: {fo['veredito']}"),
                     ("Parcela correta", pc["corrida_27"], f"propostas julgadas corretas na revisão humana às cegas; na corrida 20, {pc['corrida_20']}; p = {_p_q5(pc['p'])}: {pc['veredito']}"),
                     ("Passam nos cinco portões", f"{s['passam_nos_cinco']} de {s['propostas']}", (f"propostas; nos filtros de hoje passam {s['passam_nos_filtros_de_hoje']}, que são as que vão "
                                                                                               "para a revisão humana")),
                     ("Custo de cada chamada", f"{_n_q5(s['tokens_entrada_mediana'], 0)} tokens", (f"lidos na mediana, e {_n_q5(s['tokens_saida_mediana'], 0)} escritos, em "
                                                                                                 f"{_n_q5(s['segundos_mediana'])} s; na corrida 20 eram "
                                                                                                 f"{_n_q5(lei['corrida_20']['tokens_entrada_mediana'], 0)}, "
                                                                                                 f"{_n_q5(lei['corrida_20']['tokens_saida_mediana'], 0)} e "
                                                                                                 f"{_n_q5(lei['corrida_20']['segundos_mediana'])} s")),
                     ("Casos com lacuna na documentação", f"{p['com_lacuna']} de {p['casos']}", (f"{erros_com_lacuna} erros do diagnóstico e {p['acertos_com_lacuna']} acertos sem verbete que "
                                                                                             "trate da causa"))]
        rotulos_27 = [ab["corrida_27"], fo["corrida_27"], pc["corrida_27"]]
        rotulos_20_lidos = [ab["corrida_20"], fo["corrida_20"], pc["corrida_20"]]
        series_leituras = [{"nome": "corrida 20", "cor": "--s1", "n": [_fracao(x) for x in rotulos_20_lidos], "rotulos": rotulos_20_lidos},
                           {"nome": "corrida 27", "cor": "--s3", "n": [_fracao(x) for x in rotulos_27], "rotulos": rotulos_27}]
        por_lacuna = {x["grupo"]: x for x in lei["por_lacuna"]}
        rodaram = {c["caso"] for c in lei["casos"]}
        grupos_lidos = [por_lacuna.get(nome, {}) for nome in ("com lacuna", "sem lacuna")]
        series_casos = [{"nome": "casos do grupo", "cor": "--s1", "n": [g.get("casos", 0) for g in grupos_lidos]},
                        {"nome": "o desenho chamaria o analista", "cor": "--s4",
                         "n": [sum(1 for c in casos_previa if c["caso"] in rodaram and c["seria_chamado"] and bool(c["lacuna"]) is valor) for _, valor in GRUPOS_DE_LACUNA_M2]},
                        {"nome": "abstenções", "cor": "--s6", "n": [g.get("abstencoes", 0) for g in grupos_lidos]},
                        {"nome": "propostas", "cor": "--s2", "n": [g.get("propostas", 0) for g in grupos_lidos]},
                        {"nome": "passam nos cinco portões", "cor": "--bom", "n": [g.get("passam_nos_cinco", 0) for g in grupos_lidos]}]
        cab_grupo = ["Casos", "Abstenções", "Sem proposta válida", "Propostas", "Passam nos filtros de hoje", "Passam nos cinco portões"]

        def linha(x: dict) -> list[str]:
            return [str(x["casos"]), str(x["abstencoes"]), str(x["sem_bloco"]), str(x["propostas"]), str(x["passam_nos_filtros_de_hoje"]), str(x["passam_nos_cinco"])]

        tab_leituras = tabela(["Leitura", "Corrida 27", "Corrida 20", "Teste", "p", "Veredito"],
                              [[x["nome"], x["corrida_27"], x["corrida_20"], x["teste"], _p_q5(x["p"]), x["veredito"]] for x in lei["leituras"]])
        tab_portoes = tabela(["Portão", "Propostas avaliadas", "Recusa", "Passa", "Não se aplica", "Propostas que pararam aqui"],
                             [[x["nome"], str(x["avaliadas"]), str(x["recusa"]), str(x["passa"]), str(x["nao_se_aplica"]), str(x["parou_aqui"])] for x in lei["por_portao"]])
        tab_destino = tabela(["O que aconteceu com a resposta", "Casos"], [[x["destino"], str(x["casos"])] for x in lei["por_destino"]])
        tab_grupos = tabela(["Grupo de casos", *cab_grupo], [[x["grupo"], *linha(x)] for x in lei["por_lacuna"] + lei["por_acerto"]]
                            + [[f"lidos de: {x['origem']}", *linha(x)] for x in lei["por_origem"]])
        tab_codigos = tabela(["Portão em que parou", "Código da recusa", "Casos"], [[x["portao"], x["codigo"], str(x["casos"])] for x in lei["codigos"]] or [["nenhuma recusa", "", ""]])
        tab_casos = tabela(["Caso", "De onde o diagnóstico leu", "Diagnóstico certo", "Com lacuna", "Operação", "O que aconteceu", "Código", "Afirma um fato", "Texto ou termos",
                            "Tokens lidos", "Segundos"],
                           [[f"<code>{esc(c['caso'])}</code>", esc(str(c["origem"])), sim(c["acertou_diagnostico"]), sim(c["lacuna"]), esc(str(c["operacao"] or "")), esc(c["destino"] or ""),
                             esc(c["codigo"] or ""), "" if c["forma_passa"] is None else sim(c["forma_passa"]), esc(c["texto"] or c["termos"] or ""), _n_q5(c["tokens_entrada"], 0),
                             _n_q5(c["segundos"])] for c in lei["casos"]] or [["nenhum"] + [""] * 10], raw=True)
        blocos = [detalhes("M2: as três leituras contra a corrida 20", tab_leituras), detalhes("M2: o que cada portão fez com as propostas", tab_portoes),
                  detalhes("M2: o que aconteceu com cada resposta", tab_destino), detalhes("M2: o resultado por grupo de casos", tab_grupos),
                  detalhes("M2: os códigos de recusa", tab_codigos), detalhes("M2: as respostas do analista, caso a caso", tab_casos)]
        item_resultado = (f"<strong>M2: o resultado.</strong> Abstenção: {esc(ab['corrida_27'])} casos, contra {esc(ab['corrida_20'])} na corrida 20 (p = {_p_q5(ab['p'])}; "
                          f"{esc(ab['veredito'])}). Forma do texto: {esc(fo['corrida_27'])} propostas com texto afirmam um fato, contra {esc(fo['corrida_20'])} (p = {_p_q5(fo['p'])}; "
                          f"{esc(fo['veredito'])}). Parcela correta: {esc(pc['corrida_27'])}, contra {esc(pc['corrida_20'])} (p = {_p_q5(pc['p'])}; {esc(pc['veredito'])}). Nos cinco portões "
                          f"passam {s['passam_nos_cinco']} de {s['propostas']} propostas. Nenhum resultado muda o agente: a proposta é base de desenho para depois da Fase 5.")
        itens = [item_resultado]
        if rev:
            v27, v20 = rev["corrida_27"], rev.get("corrida_20_pelo_mesmo_revisor")
            do_lote = rev["corrida_20_na_revisao_do_lote"]
            sobre_a_20 = (f"As edições da corrida 20, julgadas de novo pelo mesmo revisor sem saber a origem, ficaram em {_vereditos_por_extenso(v20)}; na revisão do lote tinham ficado em "
                          f"{_vereditos_por_extenso(do_lote)}." if v20 else
                          f"As edições da corrida 20 não entraram nesta revisão; a comparação usa a revisão do lote ({_vereditos_por_extenso(do_lote)}).")
            cinco = rev["passam_nos_cinco_por_veredito"]
            itens.append(f"<strong>M2: a revisão humana às cegas.</strong> Quem revisou: {esc(str(rev.get('quem')))}. Das propostas da corrida 27, {rev['revisadas']} têm veredito "
                         f"({_vereditos_por_extenso(v27)}) e faltam {rev['pendentes']}. {sobre_a_20} Entre as que passam nos cinco portões, a revisão julgou {_vereditos_por_extenso(cinco)}.")
            tab_contra = tabela(["Portão", "Propostas revisadas e avaliadas", "Erradas recusadas", "Parciais recusadas", "Corretas perdidas", "Corretas que passam"],
                                [[x["nome"], str(x["avaliadas"]), str(x["Errada"]["recusa"]), str(x["Parcial"]["recusa"]), str(x["Correta"]["recusa"]), str(x["Correta"]["passa"])]
                                 for x in rev["portoes_contra_a_revisao"]])
            blocos.append(detalhes("M2: os portões 3, 4 e 5 contra a revisão humana das propostas da corrida 27", tab_contra))
        else:
            itens.append(item_revisao)
        blocos += blocos_previa
        itens += [item_mede, item_regra, item_lacuna, item_portoes]
    dados_js = {"leituras": {"grupos": GRUPOS_DAS_LEITURAS_M2, "series": series_leituras}, "casos": {"grupos": [nome for nome, _ in GRUPOS_DE_LACUNA_M2], "series": series_casos}}
    return dados_js, estado, itens_kpi, "\n".join(blocos), itens, fontes_


def secao_analista(m1: dict | None, previa: dict | None = None, lei: dict | None = None) -> tuple[dict, str]:
    titulo = ("Os portões novos barram o que a pessoa barrou, e a entrada própria muda o que o modelo escreve na biblioteca? A medida M1 (os portões 3, 4 e 5 nas propostas da "
              "corrida 20) e a corrida 27, a medida M2 (o analista de documentação com a ficha curta do caso).")
    if not m1:
        return {}, (f'<section id="analista" hidden>\n<h1>{titulo}</h1>\n<p class="lead">A medida M1 ainda não foi gravada: falta <code>portoes_m1.json</code> em '
                    '<code>resultados_alvo/fase4/</code>, que sai de <code>python portoes_de_edicao.py --m1</code>.</p>\n</section>')
    r = m1["resumo"]
    dados_js, itens_kpi, blocos_m1, itens_m1, fontes_ = _bloco_m1(m1)
    lead_ = (f"A medida M1 rodou, sem modelo (ficha 67, decisão 121): das {r['propostas']} propostas de edição da corrida 20, o portão da forma recusaria {r['forma_recusa']} das "
             f"{r['propostas']}, o dos filtros de texto {r['texto_recusa']} e, entre as {r['revisadas']} que viraram edição e passaram pela revisão humana, o portão da busca recusaria "
             f"{r['busca_recusa']}. Em sequência, os três deixariam {r['sobram_depois_dos_tres']} de {r['revisadas']} edições.")
    # ! Alteração de IA - Revisar: (11/11/2026, decisão 121) a aba passou a trazer, depois da M1, a corrida 27 (medida M2): o estado, os cartões, os dois gráficos e as
    # tabelas recolhidas de `_bloco_m2`; sem a prévia gravada, só um aviso de que ela falta.
    # ! Motivo: a aba só mostrava a M1, e os argumentos da prévia e da leitura da corrida 27 chegavam sem uso; o Eric decide pelo painel e precisa ver ali o prompt que
    # aprova e, depois da corrida, o resultado.
    if previa:
        dados_m2, estado_m2, kpis_m2, blocos_m2, itens_m2, fontes_m2 = _bloco_m2(previa, lei)
        dados_js = {**dados_js, **dados_m2}
        parte_m2 = f"""<h2>Corrida 27 (medida M2): o analista de documentação com a ficha curta do caso</h2>
{kpis(kpis_m2)}
<h2>M2: as três leituras da regra, na corrida 20 e, depois da corrida, na corrida 27</h2>
<div class="chart"><canvas id="g-analista-leituras"></canvas></div>
<h2>M2: os casos com lacuna e sem lacuna na documentação e, depois da corrida, o que o analista respondeu em cada grupo</h2>
<div class="chart"><canvas id="g-analista-casos"></canvas></div>
{blocos_m2}"""
        lead_ += " " + estado_m2
    else:
        itens_m2, fontes_m2 = [], []
        parte_m2 = ('<h2>Corrida 27 (medida M2)</h2>\n<p>A prévia sem modelo da corrida 27 ainda não foi gravada: falta <code>analista_previa.json</code> em '
                    '<code>resultados_alvo/fase4/</code>, que sai de <code>python experimento_analista.py --previa</code>.</p>')
    html_ = f"""<section id="analista" hidden>
<h1>{titulo}</h1>
<p class="lead">{lead_}</p>
{kpis(itens_kpi)}
<h2>M1: o que cada portão recusaria entre as edições que uma pessoa revisou</h2>
<div class="chart"><canvas id="g-analista-portoes"></canvas></div>
<h2>M1: o que sobra depois de cada portão, pelo veredito da revisão humana</h2>
<div class="chart"><canvas id="g-analista-sequencia"></canvas></div>
{parte_m2}
{blocos_m1}
{leitura(itens_m2 + itens_m1)}
{fontes(fontes_m2 + fontes_)}
</section>"""
    return dados_js, html_


# ! Alteração de IA - Revisar: (05/11/2026, Fase 4, pacote P8) a aba "Fechamento da fase": a tabela das regras (seção 10) e as seções 1, 11, 12 e 15 lidas do relatório da fase, os cartões lidos dos JSON das leituras vigentes (tela_v2, cura, cenarios_v2, leitura_revisao_trilha) e as fichas abertas.
# ! Motivo: o plano previa uma aba da fase (seção 3.8), e as sete abas por análise não dizem o que fechou, o que ficou como limitação e o que depende do Eric. Ele decide pelo painel, não pelo Markdown. Nenhum número é digitado aqui.
ESTADOS_REGRA = {"cumprida": ("Cumprida", "concluida"), "ressalva": ("Cumprida com ressalva", "andamento"), "medida": ("Medida", "outro"), "nao": ("Não cumprida", "nao_cumprida")}


def _classe_regra(estado: str) -> str:
    e = estado.strip().lower()
    if e.startswith("não cumprida") or e.startswith("nao cumprida"):
        return "nao"
    if "ressalva" in e:
        return "ressalva"
    return "cumprida" if e.startswith("cumprida") else "medida"


def _celula_regra(estado: str) -> str:
    """O chip com o estado e, abaixo dele, o que vem depois dos dois-pontos: um chip longo não quebra linha e esprime as outras colunas."""
    classe = _classe_regra(estado)
    resto = estado.partition(":")[2].strip()
    return chip(ESTADOS_REGRA[classe][1], ESTADOS_REGRA[classe][0]) + (f'<br><span class="nota">{pt.inline(resto)}</span>' if resto else "")


# ! Alteração de IA - Revisar: (05/11/2026, decisões 90 a 92) as corridas da Fase 4 que o roadmap ainda não marca como feitas viram um cartão de número, uma frase na resposta e os cartões de corrida, e a seção 13 do relatório fica à vista.
# ! Motivo: com as fichas 42 a 45 fechadas, a aba dizia só "nenhuma ficha aberta", como se não restasse nada, e as corridas 18c, 21c, 23 e 24 ainda vão rodar. Lidas pelo estado no roadmap, elas saem da lista sozinhas quando a linha passar a `feita`.
def _corridas_que_faltam_f4(road: dict | None) -> list[str]:
    """As corridas da Fase 4 (da 16 em diante) que o roadmap ainda não marca como feitas."""
    faltam = []
    for c in (road or {}).get("corridas", []):
        m = re.match(r"\d+", c.numero)
        if m and int(m.group()) >= 16 and c.classe != "feita":
            faltam.append(c.numero)
    return faltam


def _lista_em_frase(itens: list[str]) -> str:
    return " e ".join(itens) if len(itens) < 3 else ", ".join(itens[:-1]) + " e " + itens[-1]


def secao_fechamento_f4(relatorio_md: str | None, pend: list, md_doc_para_html, tela: dict | None = None, cura: dict | None = None, cenarios: dict | None = None, revisao: dict | None = None,
                        road: dict | None = None, cartoes_corridas=None, corrida_tela: str = "18b", corrida_cenarios: str = "21b") -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) três cartões (tela, cura, cenários) reescritos sem "b + c", "rótulo", MTTR e Task Success soltos.
    # ! Motivo: o texto à vista trazia siglas que o Eric pediu para tirar; os números são os mesmos, lidos dos mesmos JSON.
    titulo = "Fechamento da Fase 4: o agente na tela fez o que o plano pediu?"
    if not relatorio_md:
        return {"contagem": {}, "fichas_abertas": 0}, (f'<section id="fechamentof4" hidden>\n<h1>{titulo}</h1>\n<p class="lead">O relatório da fase ainda não existe: '
                                                       '<code>Documentacao/memorial/3-resultados-e-analises/fase-4-relatorio.md</code> sai do pacote P8.</p>\n</section>')
    md = pt.sem_comentarios(relatorio_md)
    secs = {t.split(".")[0]: c for t, c in pt.secoes(md) if t and t[0].isdigit()}
    cab, linhas, _ = pt.primeira_tabela(secs["10"])
    col = {c: i for i, c in enumerate(cab)}
    cont = Counter(_classe_regra(r[col["Estado"]]) for r in linhas)
    nomes_nao = [r[col["Regra"]] for r in linhas if _classe_regra(r[col["Estado"]]) == "nao"]
    abertas = [f for b in pend for f in b.fichas if f.aberta]
    faltam = _corridas_que_faltam_f4(road)
    trs = "".join(
        f'<tr data-valor="{_classe_regra(r[col["Estado"]])}"><td>{pt.inline(r[col["Regra"]])}</td><td>{pt.inline(r[col["O que ela pede"]])}</td><td>{esc(r[col["Corrida"]])}</td>'
        f'<td>{pt.inline(r[col["Resultado"]])}</td><td>{_celula_regra(r[col["Estado"]])}</td></tr>'
        for r in linhas)
    tab = ('<div class="filtros filtro-tabela" data-alvo="tab-regras-f4" role="group" aria-label="Filtro das regras">'
           f'<button type="button" data-valor="todos" aria-pressed="true">Todas ({len(linhas)})</button>'
           + "".join(f'<button type="button" data-valor="{k}" aria-pressed="false">{esc(ESTADOS_REGRA[k][0])} ({cont[k]})</button>' for k in ESTADOS_REGRA if cont[k])
           + '</div><div class="tabela" id="tab-regras-f4"><table><thead><tr><th>Regra</th><th>O que ela pede</th><th>Corrida</th><th>Resultado</th><th>Estado</th></tr></thead>'
           f'<tbody>{trs}</tbody></table></div>')
    lista = "".join(f'<li><a href="#{f.id_html}" data-ir="pendencias|{f.id_html}"><span class="numero">{f.numero}</span> {pt.inline(f.titulo)}</a>'
                    f'<br><span class="nota">Recomendação: {pt.inline(f.campos.get("Recomendação", "n/d"))}</span></li>' for f in abertas)
    itens_kpi = [("Regras cumpridas", f'{cont["cumprida"] + cont["ressalva"]} de {len(linhas)}', f'{cont["ressalva"]} com ressalva, indicada na coluna Estado' + (f'; {cont["medida"]} só medida, sem limite fixado' if cont["medida"] else "")),
                 ("Não cumpridas", str(cont["nao"]), " e ".join(nomes_nao) or "nenhuma")]
    if tela:
        r = tela["resumo"]
        itens_kpi.append(("Mesma causa na tela e no caso escrito", f'{r["concordam"]} de {r["casos"]}', f'corrida {corrida_tela}; a tela perde {r["c"]} e ganha {r["b"]}, limite de {r["limite_r2"]} perdidos (decisão 98): ' + ("dentro" if r.get("dentro_do_limite_r2") else "fora; limitação declarada")))
    if cura:
        r = cura["resumo"]
        itens_kpi.append(("Quebras curadas em código", f'{r["curadas"]} de {r["execucoes"]}', f'corrida 19, sem modelo; mediana {fmt(r["mttr_mediana_s"], 3)} s até o resultado; os 100% vêm do desenho'))
    if cenarios:
        g = cenarios["geral"]
        itens_kpi.append(("Cenários que chegaram ao resultado (Task Success)", f'{g["sucessos"]} de {g["n"]}', f'corrida {corrida_cenarios}; média de {fmt(g["mttr_media_s"], 1)} s até o resultado; uma repetição, sem linha de base'))
    if revisao:
        r = revisao["resumo"]
        itens_kpi.append(("Medida com revisor humano", "em aberto", f'{r["respostas_do_revisor"]} resposta do Eric e {r["pareceres_aprovados"]} pareceres do Claude aprovados'))
    if faltam:
        # ! Alteração de IA - Revisar: (10/11/2026, decisão 116) o cartão deixou de dizer que as corridas que faltam foram pedidas pelas fichas 42 a 44.
        # ! Motivo: valia para as corridas 18c, 21c, 23 e 24; a corrida 25 veio da ficha 63, e o cartão de cada corrida, lido do roadmap, já diz de onde ela veio.
        itens_kpi.append(("Corridas que faltam antes da Fase 5", str(len(faltam)), f'{_lista_em_frase(faltam)}; o comando e o pré-requisito de cada uma estão nos cartões abaixo'))
    itens_kpi.append(("Decisões do Eric em aberto", str(len(abertas)), "fichas na aba Pendências; não impedem a Fase 5" if abertas else "nenhuma ficha aberta"))
    # ! Alteração de IA - Revisar: (06/11/2026, decisão 98) a resposta deixa de dizer "em parte" e "0 não: nenhuma" quando nenhuma regra ficou de fora.
    # ! Motivo: a regra R2 fechou na corrida 18d e a tabela ficou sem regra não cumprida; o que falta é a medida com revisor humano e as corridas, que a frase diz em seguida.
    resposta = (f'{"Em parte" if cont["nao"] else "Nas regras, sim"}. Das {len(linhas)} regras, {cont["cumprida"]} {"foi cumprida" if cont["cumprida"] == 1 else "foram cumpridas"} sem ressalva, {cont["ressalva"]} com ressalva'
                + (f', {cont["medida"]} só medida' if cont["medida"] else "")
                + (f' e {cont["nao"]} não: {" e ".join(nomes_nao)}' if cont["nao"] else ", e nenhuma ficou de fora")
                + '. A medida com revisor humano da especificação da trilha está em aberto: será feita depois da Pós-Fase 4 (decisão 95).'
                + ((f' Falta {len(abertas)} decisão do Eric, que não impede a Fase 5.' if len(abertas) == 1 else f' Faltam {len(abertas)} decisões do Eric, que não impedem a Fase 5.') if abertas else "")
                + (f' Antes da Fase 5 faltam as corridas {_lista_em_frase(faltam)}, e as leituras delas podem mudar estes números.' if faltam else ""))
    html_ = f'''<section id="fechamentof4" hidden>
<h1>{titulo}</h1>
<p class="lead">{pt.inline(resposta)}</p>
{kpis(itens_kpi)}
<h2>O que depende do Eric</h2>
{"<ol class='lista-eric'>" + lista + "</ol>" if abertas else ("<p>Nenhuma ficha aberta. Os pré-requisitos das corridas abaixo dizem o que ainda depende dele.</p>" if faltam else "<p>Nenhuma ficha aberta.</p>")}
{"<h2>O que falta antes da Fase 5</h2>" + cartoes_corridas(road, numeros=faltam, sufixo="-f4") if faltam and cartoes_corridas else ""}
<h2>O que o plano previa e não saiu</h2>
{md_doc_para_html(secs.get("13", ""))}
<h2>As regras, uma a uma</h2>
{tab}
{detalhes("O que a fase perguntou e o que respondeu (relatório, seção 1)", md_doc_para_html(secs.get("1", "")))}
{detalhes("Limitações declaradas (relatório, seção 12)", md_doc_para_html(secs.get("12", "")))}
{detalhes("O que a Fase 4 entrega à Fase 5 (relatório, seção 11)", md_doc_para_html(secs.get("11", "")))}
{detalhes("O que a próxima versão do documento do TCC precisa carregar (relatório, seção 15)", md_doc_para_html(secs.get("15", "")))}
{fontes(["<code>3-resultados-e-analises/fase-4-relatorio.md</code>, seções 1, 10, 11, 12, 13 e 15, com os blocos <code>tb_f4_*</code> colados por <code>avaliar_fase4.py --colar</code>", "<code>resultados_alvo/fase4/tela_v4.json</code>, <code>cura.json</code>, <code>cenarios_v4.json</code> e <code>leitura_revisao_trilha.json</code>", "<code>pendencias.md</code> (fichas abertas)", "<code>roadmap.md</code>, §2 (as corridas que faltam, pelo estado)", "anexo de <code>claude-memoria/plano-aprovado-fase-4.md</code> (desvios do plano)"])}
</section>'''
    return {"contagem": dict(cont), "fichas_abertas": len(abertas)}, html_


# ------------------------------------------------------------------ Fase 4: avaliação da própria trilha (corrida 22)

# ! Alteração de IA - Revisar: (04/11/2026, Fase 4, pacote P7) a aba "Avaliação da trilha", lida de resultados_alvo/fase4/trilha.json
# (avaliar_fase4.py --trilha): TPR x TNR de cada sinal da trilha contra os erros reais (o principal é a divergência do nó; acaso
# 0,25), as intervenções com o limite inferior, a repetição da base, a sonda de pós-racionalização, as três mutações contra o nó
# previsto (verbete trocado: recuperacao; contrato alterado: poda; seletor quebrado: cura), o seletor roteiro a roteiro, a amostra
# dos relatórios da sessão de revisão e a tabela caso a caso; sem o arquivo, o estado vazio com o cartão da corrida.
# ! Motivo: regra do painel (uma aba por análise, números só dos JSON); a corrida 22 é a sétima análise da Fase 4 e o Eric decide
# pelo painel se a trilha vale como prova (especificação da trilha, seção 12).
# ! Alteração de IA - Revisar: (05/11/2026, leitura da corrida 22) a aba ganhou a divergência só por gatilho e o selo baixo nos cartões, os intervalos de
# Wilson, o controle da sonda e a tabela das inferências de mesmo prompt; `revisao_preenchida` guarda a tabela caso a caso até a planilha da sessão de
# revisão estar preenchida, e o texto das mutações diz que os 100% são esperados por construção.
# ! Motivo: a sessão de revisão é às cegas e este painel é publicado e é o que o Eric lê: a tabela diz quais relatórios estão certos. Com só 5 erros, um
# número sem intervalo engana; e dizer "100% no nó previsto" sem dizer que o nó sai em código da entrada mutada faria parecer um resultado do modelo.
def secao_trilha(tri: dict | None, road: dict, cartoes_corridas, revisao_preenchida: bool = False, rev: dict | None = None) -> tuple[dict, str]:
    # ! Alteração de IA - Revisar: (05/11/2026) cartões, títulos, o parágrafo "O que a aba mede" e itens de leitura à vista reescritos sem TPR x TNR, Wilson, "gatilho", "poda" e "rótulo" soltos.
    # ! Motivo: o texto à vista trazia siglas que o Eric pediu para tirar; o cartão das mutações perdeu o detalhe por tipo, que já está no gráfico e na tabela, e os números seguem lidos do JSON.
    fontes_ = fontes(["<code>resultados_alvo/fase4/trilha.json</code> e <code>.md</code> (<code>avaliar_fase4.py --trilha</code>, com <code>--check</code>; blocos <code>tb_f4_trilha_*</code>); "
                      "a planilha da sessão de revisão em <code>resultados_alvo/fase4/revisao_trilha.md</code>, os relatórios dela em <code>resultados_alvo/fase4/relatorios_revisao_trilha/</code>, a pré-análise do Claude em <code>resultados_alvo/fase4/pre_analise_revisao_trilha.md</code> e a leitura em <code>resultados_alvo/fase4/leitura_revisao_trilha.json</code> (<code>avaliar_fase4.py --revisao</code>, blocos <code>tb_f4_revisao_*</code>)",
                      "<code>executar_fase4.py --modo avaliacao_trilha</code> (<code>avaliacao_trilha.py</code>: os nós <code>poda</code> e <code>recuperacao</code> em código, as quatro "
                      "intervenções de <code>diagnostico_ao_vivo.py</code>, a sonda, as mutações e o diff de <code>trilha.diff_contra_referencia</code>)",
                      "especificação da trilha, seções 5, 6.1, 9 e 12; plano aprovado da Fase 4, seções 5 (P7) e 6 (corrida 22); roadmap §2.15; ficha 39"])
    o_que_mede = ("<p>Três perguntas da especificação da trilha (seção 12), respondidas sem gabarito no agente e com gabarito só na leitura: (a) a divergência que a trilha "
                  "sinaliza coincide com os erros reais? A medida é a nota que sobe quando o sinal pega os erros e deixa os acertos em paz (TPR x TNR); um sinal jogado ao acaso dá 0,25. (b) Quando a "
                  "falha é injetada de propósito (um verbete trocado na busca, o contrato alterado no corte em código do que o modelo lê, o seletor quebrado na cura), o primeiro nó que diverge da trilha "
                  "da base é o nó previsto? (c) A FONTE só justifica a resposta depois de dada (pós-racionalização)? Um trecho que afirma a causa respondida é plantado num verbete entregue que a FONTE não citou, "
                  "e a sonda mede se ela passa a citá-lo com a mesma causa respondida. Depois da corrida, uma sessão de revisão com o Eric, de até 12 relatórios (até 6 certos e até 6 errados, "
                  "sorteados com semente fixa), mede o tempo até a decisão, a localização do erro e a adesão apropriada.</p>")
    vazio = {"sinais": [], "mutacoes": [], "resumo": None}
    if not tri or not (tri.get("resumo") or {}).get("casos"):
        html_ = f'''<section id="trilha" hidden>
<h1>Avaliação da trilha: ela aponta os erros reais e o passo certo quando a falha é injetada?</h1>
<p class="lead">A corrida 22 ainda não foi rodada nesta máquina: falta <code>resultados_alvo/fase4/trilha.json</code>, gerado por <code>avaliar_fase4.py --trilha</code> depois de <code>rodar_fase4.ps1 -Modo avaliacao_trilha -Saida fase4_trilha</code> (noite D do plano aprovado, com modelo).</p>
{o_que_mede}
{cartoes_corridas(road, numeros=["22"], sufixo="-tri")}
{fontes_}
</section>'''
        return vazio, html_
    r, so, fo, rep, cond = tri["resumo"], tri.get("sonda") or {}, tri.get("fonte") or {}, tri.get("repeticao") or {}, tri.get("condicoes") or {}
    sinais = tri.get("sinais") or []
    mutacoes = tri.get("mutacoes") or []
    por_tipo = {m["tipo"]: m for m in mutacoes}
    sel = tri.get("seletor") or {}
    amostra = tri.get("amostra_revisao") or []
    intervencoes = tri.get("intervencoes") or []
    inter = {x["tipo"]: x for x in intervencoes}
    pares = tri.get("mesmo_prompt") or []
    par_troca = next((x for x in pares if x["par"] == "verbete_trocado_e_troca"), None)
    por_sinal = {s["sinal"]: s for s in sinais}
    principal, gat, selo = por_sinal.get("divergencia"), por_sinal.get("por_gatilho"), por_sinal.get("selo_baixo")

    def nd(v, casas: int = 2) -> str:
        return "n/d" if v is None else fmt(v, casas)

    def de(a, b) -> str:
        return f"{a} de {b}"

    def wilson_(ic) -> str:
        return "n/d" if not ic else f"{fmt(ic[0])} a {fmt(ic[1])}"

    def pegou(s: dict | None, verbo: str = "pegou") -> str:
        return "n/d" if not s else f"{verbo} {s['vp']} de {s['erros']} erros e acusou {s['fp']} de {s['acertos']} acertos"

    texto = [m for m in mutacoes if m["tipo"] != "seletor_quebrado"]
    prev_texto, apl_texto = sum(m["previsto"] for m in texto), sum(m["aplicaveis"] for m in texto)
    prev_total, apl_total = sum(m["previsto"] for m in mutacoes), sum(m["aplicaveis"] for m in mutacoes)
    dados_js = {"sinais": [{k: s.get(k) for k in ("sinal", "tpr", "tnr", "produto")} for s in sinais],
                "mutacoes": [{k: m.get(k) for k in ("tipo", "previsto", "outro_no", "sem_divergencia", "sem_alvo")} for m in mutacoes],
                "resumo": {k: r.get(k) for k in ("casos", "acertos", "erros", "tpr", "tnr", "produto")}}
    previstas = cond.get("inferencias_previstas")
    itens_kpi = [("Nota da divergência, com todas as intervenções", nd(r.get("produto")), f'{pegou(principal)}; o acaso dá {fmt(r.get("acaso"), 2)}'),
                 ("Nota só pelo aviso de checagem extra, como o agente roda", nd((gat or {}).get("produto")), f'{pegou(gat, "pegaria")} (contado, não rodado assim)'),
                 ("Nota do selo baixo, sem inferência a mais", nd((selo or {}).get("produto")), f'{pegou(selo)}'),
                 ("Acerto nos casos", de(r["acertos"], r["casos"]), f'{nd(r.get("acerto_pct"), 1)}% no caso escrito; {cond.get("modelo") or ""}, Ollama {cond.get("versao_ollama") or "n/d"}'),
                 ("Falhas injetadas que apontaram o nó previsto", de(prev_total, apl_total), "esperado por construção: o nó sai em código da entrada mutada (ver a leitura)"),
                 ("FONTE que só justifica a resposta (pós-racionalização)", f'{nd(so.get("taxa_pct"), 1)}%', f'{de(so.get("pos_racionalizacao"), so.get("com_alvo"))} casos citaram o verbete plantado; sem plantar, {de(so.get("controle_cita", 0), so.get("controle_n", 0))}'),
                 ("Inferências", str(r.get("inferencias")), f'{previstas} previstas; a diferença são as mutações de contrato sem alvo' if previstas is not None else "")]
    tab_sinais = tabela(["Sinal", "O que é", "Pegou (VP)", "Deixou passar (FN)", "Acusou acerto (FP)", "Deixou em paz (VN)", "TPR", "TNR", "TPR x TNR", "TPR, Wilson 95% (%)", "TNR, Wilson 95% (%)"],
                        [[f"<code>{esc(s['sinal'])}</code>", esc(s.get("descricao") or ""), s["vp"], s["fn"], s["fp"], s["vn"], nd(s["tpr"]), nd(s["tnr"]), nd(s["produto"]), wilson_(s.get("ic_tpr")), wilson_(s.get("ic_tnr"))] for s in sinais], raw=True)
    tab_inter = tabela(["Intervenção", "O que é", "Rodou em", "Mudou o rótulo", "Só limite inferior", "Queda média de p"],
                       [[f"<code>{esc(x['tipo'])}</code>", esc(x.get("descricao") or ""), x["n"], x["mudou_rotulo"], x["limite_inferior"], nd(x.get("queda_media_p"))] for x in intervencoes], raw=True)
    tab_pares = tabela(["Par de inferências", "O que é", "Pares", "Mesmo prompt", "Mesma resposta", "Mesma FONTE", "Mesmo rótulo"],
                       [[f"<code>{esc(x['par'])}</code>", esc(x.get("descricao") or ""), x["n"], x["mesmo_prompt"], x["mesma_resposta"], x["mesma_fonte"], x["mesmo_rotulo"]] for x in pares], raw=True)
    tab_mut = tabela(["Mutação", "Nó previsto", "Casos", "Aplicáveis", "Sem alvo", "Apontou o nó previsto", "Apontou outro nó", "Sem divergência", "Rótulo mudou", "Previsto (%)"],
                     [[f"<code>{esc(m['tipo'])}</code>", f"<code>{esc(m['no_previsto'])}</code>", m["casos"], m["aplicaveis"], m["sem_alvo"], m["previsto"], m["outro_no"], m["sem_divergencia"],
                       m["rotulo_mudou"], nd(m.get("previsto_pct"), 1)] for m in mutacoes], raw=True)
    tab_sel = tabela(["Roteiro", "Modo mutado", "Cura dourada", "Cura mutada", "Rótulo dourado", "Rótulo mutado", "Primeiro nó divergente", "Previsto (cura)"],
                     [[f"<code>{esc(x['roteiro'])}</code>", f"<code>{esc(x.get('modo_mutado') or '')}</code>",
                       f"<code>{esc(x['estrategia_dourada'])}</code>" if x.get("curada_dourada") else "sem cura", f"<code>{esc(x['estrategia_mutada'])}</code>" if x.get("curada_mutada") else "sem cura",
                       f"<code>{esc(x.get('rotulo_dourado') or 'n/d')}</code>", f"<code>{esc(x.get('rotulo_mutado') or 'n/d')}</code>",
                       f"<code>{esc(x['primeiro_no'])}</code>" if x.get("primeiro_no") else "sem divergência", "sim" if x.get("aponta_o_previsto") else ("não" if x.get("aponta_o_previsto") is False else "n/d")]
                      for x in sel.get("roteiros") or []], raw=True)
    # ! Alteração de IA - Revisar: (05/11/2026, sessão de revisão) a lista dos casos da amostra só entra depois da sessão; antes, a aba aponta para a página da sessão.
    # ! Motivo: o nome e a classe dizem a família do defeito e estreitam a causa verdadeira, e a posição na lista é a mesma da página, que mostra só um nome neutro.
    tab_amostra = (tabela(["Posição", "Caso", "Classe", "Relatório"], [[x["posicao"], f"<code>{esc(x['caso'])}</code>", x.get("classe"), f"<code>{esc(x['relatorio'])}</code>"] for x in amostra], raw=True)
                   if revisao_preenchida else
                   ('<p class="nota">A lista dos casos entra aqui depois da sessão: o nome e a classe dizem a família do defeito, e a posição na lista é a mesma da '
                    f'<a href="{URL_SESSAO_REVISAO}" target="_blank" rel="noopener">página da sessão de revisão</a>, que mostra só um nome neutro.</p>'))
    if revisao_preenchida:
        tab_casos = tabela(["Caso", "Classe", "Gabarito", "Rótulo", "Resultado", "p", "Selo", "Falha", "Divergência", "Por gatilho", "Remoção ou troca", "Sem documentação", "Limite inferior", "Sonda", "Verbete trocado", "Contrato alterado"],
                           [[f"<code>{esc(c['caso'])}</code>", c.get("classe"), f"<code>{esc(c['gabarito'])}</code>", f"<code>{esc(c.get('rotulo') or 'n/d')}</code>", "certo" if c["acerto"] else "errado",
                             nd(c.get("p_rotulo")), esc(c.get("selo") or "n/d"), esc(c.get("falha") or ""), "sim" if c["sinais"]["divergencia"] else "não", "sim" if c["sinais"].get("por_gatilho") else "não",
                             "sim" if c["sinais"]["remocao_ou_troca"] else "não", "sim" if c["sinais"]["sem_documentacao"] else "não", c.get("limite_inferior"), esc(c.get("sonda") or ""), esc(c.get("verbete_trocado") or ""),
                             esc(c.get("contrato_alterado") or "")] for c in tri.get("casos") or []], raw=True)
        bloco_casos = detalhes("Caso a caso (bloco tb_f4_trilha_casos)", tab_casos)
    else:
        bloco_casos = ('<p class="nota">A tabela com o resultado de cada caso entra nesta aba depois da sessão de revisão, quando a planilha <code>revisao_trilha.md</code> estiver preenchida: '
                       'a sessão é às cegas, e a tabela diria quais relatórios estão certos. Por isso também vale não abrir <code>trilha.md</code> nem <code>trilha.json</code> antes dela.</p>')
    # ! Alteração de IA - Revisar: (05/11/2026, decisão 86) o bloco da sessão: quem decidiu cada relatório, o parecer do Claude contra o gabarito, o caso a caso e o aviso de que a medida com revisor humano não foi feita.
    # ! Motivo: o Eric lê pela aba; somar tudo como revisão humana apagaria justamente a limitação das decisões 85 e 86, e os números vêm de leitura_revisao_trilha.json.
    bloco_rev = ""
    if rev:
        rr, pa_ = rev.get("resumo") or {}, rev.get("parecer") or {}
        rotulo_origem = {"revisor": "resposta do revisor", "parecer_aprovado": "parecer do Claude aprovado"}
        n_rev = rr.get("respostas_do_revisor")
        tempo_ = next((x for x in rev.get("tempo") or [] if x.get("grupo") == "todos"), {})
        aviso_rev = (f'Só {n_rev} dos {rr.get("relatorios")} relatórios {"tem" if n_rev == 1 else "têm"} resposta própria do revisor, dada antes de ele ler a pré-análise do Claude. Os outros {rr.get("pareceres_aprovados")} são o parecer do Claude, '
                     'aprovado pelo Eric sem resposta própria (decisões 85 e 86). Por isso esta sessão não cumpre a medida com revisor humano da especificação (seção 12 c), que fica em aberto até a Pós-Fase 4 (decisão 95); o que ela dá é o parecer do Claude conferido contra o gabarito. '
                     f'O tempo até a decisão só existe onde o revisor respondeu: {tempo_.get("n", 0)} relatório, mediana de {nd(tempo_.get("mediana"), 0)} s com a página à vista.') if rr.get("pareceres_aprovados") else ""
        duvida_rev = (f'<p class="nota">Em {", ".join(f"<code>{esc(x)}</code>" for x in rev["duvidas_de_leitura"])}, o revisor marcou que achou o erro num diagnóstico que avaliou como certo. Ele pode ter lido "erro" como o defeito do sistema, e a conta trata isso como apontar um erro onde não há; a resposta fica como ele deu.</p>'
                      if rev.get("duvidas_de_leitura") else "")
        tab_origem = tabela(["Quem decidiu", "Relatórios", "Decisões apropriadas", "Apropriadas (%)", "Wilson 95% (%)", "Avaliação igual ao gabarito"],
                            [[esc(rotulo_origem.get(x["origem"], x["origem"])), x["n"], x["apropriadas"], nd(x.get("pct"), 1), wilson_(x.get("ic")), x.get("avaliacao_bate")] for x in rev.get("por_origem") or []], raw=True)
        tab_parecer = (tabela(["Relatórios", "Decisões apropriadas", "Apropriadas (%)", "Wilson 95% (%)", "Causa certa", "Causa certa (%)", "Avaliação igual ao gabarito", "Errou a decisão", "Errou a causa"],
                              [[pa_.get("n"), pa_.get("apropriadas"), nd(pa_.get("pct"), 1), wilson_(pa_.get("ic")), pa_.get("causa_certa"), nd(pa_.get("pct_causa"), 1), pa_.get("avaliacao_bate"),
                                ", ".join(f"<code>{esc(x)}</code>" for x in pa_.get("errou_a_decisao") or []) or "nenhum", ", ".join(f"<code>{esc(x)}</code>" for x in pa_.get("errou_a_causa") or []) or "nenhum"]], raw=True) if pa_ else "")
        tab_sessao = tabela(["#", "Caso", "Gabarito", "Rótulo", "Resultado", "Quem decidiu", "Tempo (s)", "Erro localizado", "Decisão", "Apropriada", "Utilidade", "Avaliação", "Causa no parecer do Claude"],
                            [[c.get("posicao"), f"<code>{esc(c['caso'])}</code>", f"<code>{esc(c['gabarito'])}</code>", f"<code>{esc(c.get('rotulo') or 'n/d')}</code>", "certo" if c["acerto"] else "errado", esc(rotulo_origem.get(c.get("origem"), "")),
                              c.get("segundos") if c.get("segundos") is not None else "não medido", esc(c.get("erro_localizado") or ""), esc(c.get("decisao") or ""), "sim" if c.get("apropriada") else "não", c.get("utilidade"), esc(c.get("avaliacao") or ""),
                              f"<code>{esc((c.get('parecer') or {}).get('causa_dada') or 'n/d')}</code>"] for c in rev.get("casos") or []], raw=True)
        bloco_rev = (f'<h2>A sessão de revisão: quem decidiu e o parecer do Claude contra o gabarito</h2>\n<p>{aviso_rev}</p>\n{duvida_rev}\n<p>Bloco <code>tb_f4_revisao_origem</code>.</p>\n{tab_origem}\n'
                     f'<p>Bloco <code>tb_f4_revisao_parecer</code>: o parecer do Claude nos relatórios todos, escrito sem abrir o gabarito, por quem sabia quantos erros a amostra tem.</p>\n{tab_parecer}\n'
                     + detalhes("A sessão caso a caso (bloco tb_f4_revisao_casos)", tab_sessao))
    lead = (f'Na corrida 22 ({r["casos"]} casos de avaliação lidos do fixture, {esc(cond.get("modelo") or "")}, Ollama {esc(cond.get("versao_ollama") or "n/d")}), com as quatro intervenções em todos os casos, a divergência '
            f'{pegou(principal)}: TPR x TNR de {nd(r.get("produto"))}, contra {fmt(r.get("acaso"), 2)} do acaso. Contada como o agente roda fora da avaliação, só por gatilho, ela daria {nd((gat or {}).get("produto"))}, '
            f'e o selo baixo sozinho dá {nd((selo or {}).get("produto"))}. As mutações apontaram o nó previsto em {de(prev_total, apl_total)} casos e roteiros aplicáveis, o esperado por construção; '
            f'a FONTE citou o verbete plantado, com o mesmo rótulo, em {de(so.get("pos_racionalizacao"), so.get("com_alvo"))} casos, contra {de(so.get("controle_cita", 0), so.get("controle_n", 0))} sem plantar nada. São só {r["erros"]} erros.')
    if rev:
        rr_, pa__ = rev.get("resumo") or {}, rev.get("parecer") or {}
        item_sessao = (f"<strong>O que o parecer do Claude diz.</strong> Ele acertou {de(pa__.get('apropriadas'), pa__.get('n'))} decisões e {de(pa__.get('causa_certa'), pa__.get('n'))} causas, o que mostra que a evidência para julgar estava no relatório e na biblioteca, para um leitor forte. "
                       f"Não mostra que o relatório funciona para quem lê: esse leitor sabia quantos erros a amostra tem e consultou a biblioteca, e só {de(rr_.get('erros_localizados'), rr_.get('erros_na_amostra'))} erros estavam à vista no próprio relatório. Por isso a medida com revisor humano fica em aberto (decisão 95).")
    else:
        item_sessao = (f"<strong>Sessão de revisão.</strong> Os {len(amostra)} relatórios da amostra são lidos um por vez na <a href='{URL_SESSAO_REVISAO}' target='_blank' rel='noopener'>página da sessão</a>, na ordem sorteada, com um nome neutro no lugar do nome do caso e sem dizer qual está certo; "
                       "a página mede o tempo até a decisão, e o revisor aceita ou recusa, diz se achou o erro e dá a utilidade de 1 a 5.")
    leitura_ = leitura([
        (f"<strong>O que a nota diz.</strong> Ela sobe quando o sinal pega os erros e deixa os acertos em paz (TPR x TNR): 1,0 seria pegar todo erro sem acusar acerto nenhum, e 0,25 é o que um sinal jogado ao acaso dá. "
         f"A margem de incerteza dos erros pegos pela divergência vai de {wilson_((principal or {}).get('ic_tpr'))}%: com {r['erros']} erros, a tabela mostra a ordem de grandeza e não sustenta ordenar os sinais."),
        (f"<strong>Por que a divergência acende tanto.</strong> Ela acende quando qualquer intervenção muda a causa respondida, e as intervenções mudam a causa também quando o modelo está certo: a remoção em "
         f"{de((inter.get('remocao') or {}).get('mudou_rotulo'), (inter.get('remocao') or {}).get('n'))} casos, a troca em {de((inter.get('troca') or {}).get('mudou_rotulo'), (inter.get('troca') or {}).get('n'))} e a inferência sem documentação em "
         f"{de((inter.get('sem_documentacao') or {}).get('mudou_rotulo'), (inter.get('sem_documentacao') or {}).get('n'))}. A documentação pesar na resposta é o esperado, não um conflito; com o mesmo prompt, a causa respondida ficou igual em {de(rep.get('manteve'), rep.get('n'))} na repetição da base e em {de((par_troca or {}).get('mesmo_rotulo'), (par_troca or {}).get('n'))} no outro par, então a variação natural não explica essas mudanças."),
        ("<strong>Só pelo aviso de checagem extra.</strong> As quatro intervenções rodaram em todos os casos só por causa da amostra fixa da avaliação. Fora dela, rodam quando a probabilidade está baixa ou a FONTE diverge; o sinal "
         "<code>por_gatilho</code> conta a divergência assim, a partir desta corrida, sem ter rodado desse jeito. Pela decisão 88, a regra do carimbo de conflito fica como está, e o TCC reporta as duas contas."),
        (f"<strong>Falhas injetadas (mutações).</strong> Por tipo, apontaram o nó previsto " + "; ".join(f'{m["tipo"].replace("_", " ")} {de(m["previsto"], m["aplicaveis"])}' for m in mutacoes) + f". Os 100% são esperados: os nós <code>poda</code> e <code>recuperacao</code> saem em código da entrada mutada e o diff é determinístico. Isso prova que a trilha registra a mudança no nó certo, e que nenhum nó anterior muda, "
         f"mas não diz nada sobre o modelo; o que diz é a coluna \"Rótulo mudou\". \"Sem alvo\" é o caso em que a mutação não tinha o que mudar (sem contrato, corpo que não é JSON). No seletor, o nó <code>diagnostico</code> vem antes da cura e não mudou em nenhum roteiro: lá sim a divergência na cura diz algo."),
        (f"<strong>A mutação do verbete repete a troca.</strong> As duas montam o mesmo prompt em {de((par_troca or {}).get('mesmo_prompt'), (par_troca or {}).get('n'))} casos, defeito do desenho do P7: a mutação não trouxe medida nova sobre o modelo e virou uma segunda medida da variação, com a mesma causa respondida em {de((par_troca or {}).get('mesmo_rotulo'), (par_troca or {}).get('n'))}."),
        (f"<strong>Sonda.</strong> A taxa mede consistência da FONTE, não fidelidade ao mecanismo interno: {de(so.get('cita_plantado', 0), so.get('com_alvo', 0))} casos citaram o verbete plantado e {so.get('mudou_rotulo', 0)} mudaram a causa respondida (esses não contam como pós-racionalização). O controle é a repetição da base: "
         f"{de(so.get('controle_cita', 0), so.get('controle_n', 0))} citaram o mesmo verbete sem nada plantado."),
        item_sessao,
    ])
    html_ = f'''<section id="trilha" hidden>
<h1>Avaliação da trilha: ela aponta os erros reais e o passo certo quando a falha é injetada?</h1>
<p class="lead">{lead}</p>
{kpis(itens_kpi)}
<h2>Quanto cada sinal pega os erros e deixa os acertos em paz</h2>
<div class="chart alto"><canvas id="g-tri-sinais"></canvas></div>
<h2>Falhas injetadas: o nó que a trilha apontou</h2>
<div class="chart"><canvas id="g-tri-mutacoes"></canvas></div>
<h2>Os sinais da trilha contra os erros reais</h2>
<p>Bloco <code>tb_f4_trilha_sinais</code> de <code>trilha.md</code>; o sinal <code>por_gatilho</code> é a divergência contada pelo aviso de checagem extra, sem a amostra fixa.</p>
{tab_sinais}
<h2>Intervenções</h2>
<p>Blocos <code>tb_f4_trilha_intervencoes</code> e <code>tb_f4_trilha_sonda</code>: as quatro intervenções da especificação (6.1) rodaram em todos os casos pela amostra fixa; "só limite inferior" é a queda de probabilidade que o Ollama não pôde pontuar porque a causa respondida saiu das alternativas devolvidas (risco 6).</p>
{tab_inter}
<h2>O mesmo prompt, duas vezes</h2>
<p>Bloco <code>tb_f4_trilha_mesmo_prompt</code>: com a temperatura de 0,1, o mesmo prompt nem sempre dá a mesma resposta; a causa respondida é o que varia menos.</p>
{tab_pares}
<h2>Falhas injetadas de propósito (mutações)</h2>
<p>Blocos <code>tb_f4_trilha_mutacoes</code> e <code>tb_f4_trilha_seletor</code>.</p>
{tab_mut}
{tab_sel}
<h2>A amostra da sessão de revisão: {len(amostra)} relatórios</h2>
<p>Bloco <code>tb_f4_trilha_amostra</code>; as respostas vão para <code>resultados_alvo/fase4/revisao_trilha.md</code>.</p>
{tab_amostra}
{bloco_rev}
{bloco_casos}
{o_que_mede}
<h2>A corrida no roadmap</h2>
{cartoes_corridas(road, numeros=["22"], sufixo="-tri")}
{leitura_}
{fontes_}
</section>'''
    return dados_js, html_


# ! Alteração de IA - Revisar: (10/11/2026, decisão 118, sessão da pesquisa) a aba "Fluxo do agente": as três ideias do Eric para o fluxo do agente (o roteiro de raciocínio em
# passos com lista de conferência, o ciclo de reavaliação e a separação de um analista de documentação), com o veredito de cada uma, as fichas 65 a 67, a prévia da conferência em
# código depois da resposta, a posição do verbete da causa certa na busca, o custo e os portões do analista de documentação, o mapa e as afirmações da pesquisa por tópico. Lê
# `resumo_para_o_painel.json` (de integrar_pesquisa_fluxo_do_agente.py), `medidas_do_repositorio.json` (de medidas_fluxo_do_agente.py), as fichas de pendencias.md e, para a tabela
# dos portões, a proposta de desenho gerada; o id entra no NAV e os quatro gráficos em DESENHAR_TOPICOS.
# ! Motivo: a regra do painel é uma aba por análise, lida dos arquivos versionados, e o Eric decide por ela: as três fichas novas estão abertas. Nenhum número é digitado aqui.
FLUXO_ROTULOS = {"r7-raciocinio-em-passos-em-modelo-pequeno": "Raciocínio em passos", "r7-raciocinio-calibracao-e-primeiro-token": "Raciocínio e selo de confiança",
                 "r7-lista-de-conferencia-em-codigo": "Lista de conferência em código", "r7-reavaliacao-quando-ajuda": "Rever a própria resposta",
                 "r7-disparo-parada-e-evidencia-nova": "Segundo passe por sinal", "r7-curador-separado-da-base": "Papel separado para a base",
                 "r7-degradacao-e-portoes-da-base": "Degradação e portões"}
FLUXO_CAMPOS_DO_VEREDITO = (("literatura", "O que a literatura sustenta"), ("repositorio", "O que o repositório já mediu"), ("forma_que_escapa", "A forma que escapa do que já foi medido"),
                            ("como_medir", "Como seria medida"), ("custo", "Quanto custa nesta máquina"), ("recomendacao", "Recomendação"))


def _fluxo_quadro(resumo: dict, nome: str) -> str:
    """Um quadro das medidas do repositório (cabeçalho e linhas, gravados no resumo pelo integrador) como tabela da página."""
    q = (resumo.get("tabelas") or {}).get(nome)
    return tabela(q["cabecalho"], [[pt.inline(c) for c in l] for l in q["linhas"]], raw=True) if q else ""


def _fluxo_recolhido(resumo: dict, nome: str, titulo: str) -> str:
    """O mesmo quadro, recolhido sob um título que diz o que ele mostra (a tabela solta iria para um bloco "Mais informações" sem nome próprio)."""
    quadro = _fluxo_quadro(resumo, nome)
    return detalhes(titulo, quadro) if quadro else ""


def _fluxo_portoes(proposta: str | None) -> str:
    """A tabela dos portões da proposta de desenho do analista de documentação (seção 4.5), lida do documento gerado."""
    if not proposta or "### 4.5" not in proposta:
        return ""
    cab, linhas, _ = pt.primeira_tabela(proposta[proposta.index("### 4.5"):])
    return tabela(cab, [[pt.inline(c) for c in l] for l in linhas], raw=True) if linhas else ""


def secao_fluxo(resumo: dict | None, medidas: dict | None, pend: list, proposta: str | None = None) -> tuple[dict, str]:
    titulo = "As três ideias para o fluxo do agente: o que a literatura e os dados do projeto sustentam, e o que fica para decidir?"
    if not resumo or not medidas:
        return {}, (f'<section id="fluxo" hidden>\n<h1>{titulo}</h1>\n<p class="lead">A pesquisa ainda não foi integrada: faltam <code>resumo_para_o_painel.json</code> e '
                    '<code>medidas_do_repositorio.json</code> em <code>Documentacao/memorial/5-metodo-e-ferramental/dados/pesquisa-fluxo-do-agente/</code>, que saem de '
                    '<code>integrar_pesquisa_fluxo_do_agente.py</code> e de <code>medidas_fluxo_do_agente.py</code>.</p>\n</section>')
    tot, maq = resumo["totais"], medidas["maquina"]
    i1, i2, i3 = medidas["ideia_1"], medidas["ideia_2"], medidas["ideia_3"]
    conf = i1["conferencia_depois_da_resposta"]
    por_corrida = conf["por_corrida"]  # na ordem do script: corrida 16 (os 90), corrida 16 (os 54 de aprendizado), corrida 22, corrida 24
    c24, c22, os72 = i2["corrida_24"], i2["corrida_22"]["cruzamento"], i2["os_72_casos"]
    teto = [t["erros_ao_alcance"] for t in os72["teto_de_um_segundo_passe"]]
    forma, cen, portao = i3["forma_de_instrucao"], i3["cenarios_do_analista"], i3["portao_da_busca_no_lote"]
    ficha_curta = cen["cenarios"][-1]
    rodou = bool((i3.get("corrida_25") or {}).get("rodou"))
    fichas = {f.numero: f for b in pend for f in b.fichas if 64 <= f.numero <= 67}
    abertas = [f for n, f in sorted(fichas.items()) if f.aberta]
    fechadas = [f for n, f in sorted(fichas.items()) if not f.aberta]
    estado_25 = ("A corrida 25, que mede quanto pesam as notas que o modelo já escreveu na biblioteca, já rodou; o resultado dela está na aba Notas do modelo." if rodou
                 else "A corrida 25, que mede quanto pesam as notas que o modelo já escreveu na biblioteca, ainda não rodou.")
    pendentes = (f'{len(abertas)} fichas esperam resposta: ' + ", ".join(f"ficha {f.numero}" for f in abertas) + "." if abertas else "Nenhuma ficha desta pesquisa espera resposta.")
    lead_ = (f'O Eric mandou pesquisar as três ideias antes de qualquer mudança (ficha 64, decisão 118), e a pesquisa foi feita em {esc(resumo["data"])}, sem máquina e sem modelo: '
             f'{tot["topicos"]} tópicos e {tot["fontes"]} fontes, cada uma aberta por um leitor e por um verificador, com {tot["aprovadas"]} de {tot["afirmacoes"]} afirmações aprovadas '
             f'({tot["parciais"]} delas com o texto corrigido pela segunda leitura). Nada mudou no agente. {pendentes} {estado_25}')
    itens_kpi = [
        ("Fontes lidas e conferidas", f'{tot["fontes"]} fontes', f'{tot["topicos"]} tópicos; cada fonte aberta por um leitor e por um verificador'),
        ("Afirmações aprovadas", f'{tot["aprovadas"]} de {tot["afirmacoes"]}', f'{tot["parciais"]} corrigidas pela segunda leitura; {tot["rejeitadas"]} rejeitadas'),
        ("Raciocínio em passos", f'+{_txt_num(maq["segundos_de_um_raciocinio_em_passos"], 0)} s por caso', "o que custaria o modelo escrever o raciocínio nesta máquina"),
        ("Conferência depois da resposta", f'{por_corrida[3]["erros_contraditos"]} de {por_corrida[3]["erros"]} erros', "marcados na corrida 24, sem marcar nenhum acerto (prévia sem modelo)"),
        ("Segundo passe por sinal", f'{teto[0]} a {teto[-1]} de {os72["erros"]} erros', f'ao alcance; os sinais acenderiam em {os72["disparos"]} de {os72["casos"]} casos'),
        ("Propostas em forma de instrução", f'{forma["em_forma_de_instrucao"]} de {forma["propostas"]}', "corrida 20; nenhum filtro de hoje olha a forma"),
        ("Fichas abertas", str(len(abertas)), ", ".join(f"ficha {f.numero}" for f in abertas) or "nenhuma"),
    ]

    def bloco_veredito(v: dict) -> str:
        itens = "".join(f"<li><strong>{rotulo}:</strong> {pt.inline(v.get(campo, ''))}</li>" for campo, rotulo in FLUXO_CAMPOS_DO_VEREDITO)
        return f'<details open><summary>Ideia {v["ideia"]}: {esc(v["nome"])}</summary><p><strong>{pt.inline(v.get("veredito", ""))}</strong></p><ul>{itens}</ul></details>'

    def bloco_ficha(f) -> str:
        opcoes = "".join(f"<li>{pt.inline(o)}</li>" for o in f.listas.get("Opções", []))
        return (f'<details open><summary>ficha {f.numero}: {esc(f.titulo)}</summary><p>{pt.inline(f.campos.get("O que é", ""))}</p><p><strong>Por que importa:</strong> '
                f'{pt.inline(f.campos.get("Por que importa", ""))}</p><ul>{opcoes}</ul><p><strong>Recomendação:</strong> {pt.inline(f.campos.get("Recomendação", ""))}</p></details>')

    tab_fechadas = (tabela(["Ficha", "Pergunta", "Decisão"], [[str(f.numero), esc(f.titulo), pt.inline(f.campos.get("Decisão", ""))] for f in fechadas], raw=True) if fechadas else "")
    mapa = resumo.get("mapa") or []
    cont = Counter(l["veredito"] for l in mapa)
    trs = "".join(f'<tr data-valor="{esc(l["veredito"])}"><td>{esc(l["tema"])}</td><td>{pt.inline(l["opcao"])}</td><td>{chip(l["veredito"], l["veredito"])}</td>'
                  f'<td>{pt.inline(l["motivo"])}</td><td class="nota">{pt.inline(l["fonte"])}</td></tr>' for l in mapa)
    tab_mapa = ('<div class="filtros filtro-tabela" data-alvo="tab-mapa-fluxo" role="group" aria-label="Filtro do mapa do fluxo do agente">'
                f'<button type="button" data-valor="todos" aria-pressed="true">Todos ({len(mapa)})</button>'
                + "".join(f'<button type="button" data-valor="{v}" aria-pressed="false">{v.capitalize()} ({cont[v]})</button>' for v in ("adotado", "adiado", "descartado") if cont[v])
                + '</div><div class="tabela" id="tab-mapa-fluxo"><table><thead><tr><th>Tema</th><th>Opção</th><th>Veredito</th><th>Motivo</th><th>Fonte</th></tr></thead>'
                f'<tbody>{trs}</tbody></table></div>')
    topicos = resumo["topicos"]
    tab_topicos = tabela(["Subseção", "Ideia", "Tópico", "Fontes", "Aprovadas", "Corrigidas", "Rejeitadas", "Não verificadas"],
                         [[f'§{t["secao"]}', t["frente"], f'{esc(t["titulo"])} (<code>{esc(t["chave"])}</code>)', str(t["fontes"]), str(t["aprovadas"]), str(t["parciais"]), str(t["rejeitadas"]),
                           str(t["nao_verificadas"])] for t in topicos], raw=True)
    implicacoes = "".join(f'<details><summary>§{t["secao"]} {esc(t["titulo"])}</summary><p><em>{pt.inline(t["titulo_da_sintese"])}</em></p><ul>'
                          + "".join(f"<li>{pt.inline(x)}</li>" for x in t["implicacoes"]) + '</ul><p class="nota"><strong>O que a literatura não cobre:</strong> '
                          + " ".join(pt.inline(x) for x in t["lacunas"]) + "</p></details>" for t in topicos)
    portoes = _fluxo_portoes(proposta)
    html_ = f"""<section id="fluxo" hidden>
<h1>{titulo}</h1>
<p class="lead">{lead_}</p>
{kpis(itens_kpi)}
<h2>O veredito por ideia</h2>
<p>Cada veredito junta o que a literatura sustenta, o que o repositório já mediu e a forma da ideia que escapa do que já foi medido. Nenhum muda o agente: a decisão é das fichas abaixo.</p>
{"".join(bloco_veredito(v) for v in resumo.get("vereditos") or [])}
<h2>O que depende do Eric</h2>
{"".join(bloco_ficha(f) for f in abertas) or "<p>Nenhuma ficha aberta: as fichas desta pesquisa já foram respondidas.</p>"}
{tab_fechadas}
<h2>Ideia 1: a lista de conferência que cabe é a feita em código, depois da resposta</h2>
<p>O código mede um fato no próprio caso e marca quando ele desmente a causa que o modelo respondeu, sem mexer no prompt nem no selo de confiança. Numa prévia sem modelo, {conf["quantas"]} conferências de exemplo, escritas fora do agente, marcam {por_corrida[3]["erros_contraditos"]} de {por_corrida[3]["erros"]} erros da corrida 24, {por_corrida[2]["erros_contraditos"]} de {por_corrida[2]["erros"]} da corrida 22 e {por_corrida[0]["erros_contraditos"]} de {por_corrida[0]["erros"]} da corrida 16, sem marcar nenhum acerto. Elas foram escritas olhando os erros das corridas 22 e 24; nos casos de aprendizado da corrida 16, que não foram olhados, marcam {por_corrida[1]["erros_contraditos"]} de {por_corrida[1]["erros"]} erros.</p>
<div class="chart"><canvas id="g-fluxo-conferencia"></canvas></div>
{_fluxo_recolhido(resumo, "conferencia", "A prévia da conferência, corrida a corrida")}
{_fluxo_recolhido(resumo, "ideia_1", "O que o repositório já mediu sobre a ideia 1")}
<h2>Ideia 2: o que falta nos erros é o verbete da causa certa, e ele quase nunca está logo abaixo dos três entregues</h2>
<p>Um segundo passe do diagnóstico só ajudaria o erro cujo verbete certo ficou um pouco abaixo dos três que chegam ao modelo. Nos {os72["casos"]} casos das corridas 22 e 24, os dois sinais que o agente já calcula acenderiam em {os72["disparos"]}, pegariam {os72["erros_pegos"]} dos {os72["erros"]} erros e acenderiam também em {os72["acertos_incomodados"]} acertos; o verbete certo estaria ao alcance em {teto[0]} erros com 5 verbetes e em {teto[-1]} com 10.</p>
<div class="chart"><canvas id="g-fluxo-posicao"></canvas></div>
{_fluxo_recolhido(resumo, "posicao", "A posição do verbete da causa certa, em casos e em erros")}
{_fluxo_recolhido(resumo, "gatilhos", "O que cada sinal pegaria e em quantos acertos acenderia")}
{_fluxo_recolhido(resumo, "teto", "O teto de um segundo passe nos casos das duas corridas")}
{_fluxo_recolhido(resumo, "ideia_2", "O que o repositório já mediu sobre a ideia 2")}
<h2>Ideia 3: o analista de documentação custa menos com uma ficha curta, e os portões novos já mostram o que barrariam</h2>
<p>A proposta de desenho está em <code>Documentacao/memorial/5-metodo-e-ferramental/proposta-analista-de-documentacao.md</code>: o analista de documentação é chamado em segundo plano, só para relatórios que uma pessoa já decidiu e em que há lacuna na documentação; lê uma ficha curta do caso, de cerca de {_txt_num(ficha_curta["minutos"], 1)} minuto por chamada; propõe uma edição por caso; e cada edição passa por filtros e portões antes de uma pessoa aprovar. Das {forma["propostas"]} propostas da corrida 20, {forma["em_forma_de_instrucao"]} começam por verbo de instrução, e {forma["passaram_em_forma_de_instrucao"]} das {forma["passaram_nos_filtros"]} que passaram nos filtros de hoje também.</p>
<div class="chart"><canvas id="g-fluxo-custo"></canvas></div>
{_fluxo_recolhido(resumo, "cenarios", "O custo de uma chamada, conforme o que o analista de documentação lê")}
{_fluxo_recolhido(resumo, "custo_dos_portoes", "O custo dos portões")}
<p>O portão da busca, sem modelo, aplicado a cada uma das {portao["edicoes"]} edições do lote da corrida 20 em {portao["casos_com_gabarito"]} casos com gabarito: o verbete da causa certa sai dos três entregues {portao["verbete_certo_sai_no_total"]} vezes e entra {portao["verbete_certo_entra_no_total"]}. Como ler a tabela: uma edição boa não tira o verbete certo de nenhum caso; a última coluna diz quantos casos leriam a edição, que é quantos diagnósticos um portão do diagnóstico teria de refazer.</p>
{_fluxo_recolhido(resumo, "portao_por_edicao", "O portão da busca, edição por edição")}
{_fluxo_recolhido(resumo, "ideia_3", "O que o repositório já mediu sobre a ideia 3")}
{detalhes("Os portões da proposta de desenho, na ordem", portoes) if portoes else ""}
<h2>O mapa: o que já é assim, o que espera decisão e o que sai</h2>
<p><em>Adotado</em> é o que o agente já faz e a pesquisa confirma; <em>adiado</em> só entra com decisão do Eric e medida própria, sem mudar o agente antes da Fase 5; <em>descartado</em> não serve, com o motivo.</p>
{tab_mapa}
<h2>A pesquisa: as afirmações por tópico</h2>
<p>Cada tópico teve um leitor, que abriu as fontes e escreveu as afirmações com o número e a condição, e um verificador, que abriu de novo cada fonte e deu o veredito de cada afirmação. {tot["referencias_corrigidas"]} referências tiveram os autores, o evento ou a versão corrigidos pela segunda leitura.</p>
<div class="chart"><canvas id="g-fluxo-afirmacoes"></canvas></div>
{detalhes("Os tópicos, um a um", tab_topicos)}
{detalhes("O que cada tópico diz para o agente", implicacoes)}
{detalhes("A máquina: as taxas usadas nas contas de custo", _fluxo_quadro(resumo, "maquina"))}
{leitura([
    "<strong>O que não entra:</strong> o roteiro de raciocínio escrito pelo modelo e a revisão da própria resposta com o mesmo contexto. Os dois custam tempo, e a literatura mede perda neste porte de modelo.",
    "<strong>O que sobra de cada ideia é código:</strong> a conferência depois da resposta, o segundo passe decidido por sinal e por regra, e os filtros e portões do analista de documentação.",
    "<strong>O gargalo dos erros é a primeira busca:</strong> na maior parte deles o verbete da causa certa não chegou ao modelo, e ele costuma estar longe dos três entregues.",
    "<strong>A terceira ideia depende de uma pessoa:</strong> o rótulo de certo ou errado vem da decisão sobre o relatório, que só existe com o hub, depois da Fase 5.",
])}
{fontes(["<code>Documentacao/memorial/2-pesquisa-e-literatura/levantamento-2026-11-10-fluxo-do-agente.md</code> (§6.16; <code>integrar_pesquisa_fluxo_do_agente.py</code>, com <code>--check</code>)",
         "<code>5-metodo-e-ferramental/dados/pesquisa-fluxo-do-agente/</code>: as leituras e as segundas leituras em JSON, <code>sinteses.json</code>, <code>medidas_do_repositorio.json</code> (<code>medidas_fluxo_do_agente.py</code>, com <code>--check</code>) e <code>resumo_para_o_painel.json</code>",
         "<code>5-metodo-e-ferramental/proposta-analista-de-documentacao.md</code>", "<code>pendencias.md</code>, fichas 64 a 67; decisão 118; roadmap §4.8"])}
</section>"""
    dados = {
        "afirmacoes": {"topicos": [FLUXO_ROTULOS.get(t["chave"], t["chave"]) for t in topicos],
                       "series": [{"nome": "confirmadas", "n": [t["aprovadas"] - t["parciais"] for t in topicos], "cor": "--s1"},
                                  {"nome": "corrigidas pela segunda leitura", "n": [t["parciais"] for t in topicos], "cor": "--s2"},
                                  {"nome": "rejeitadas", "n": [t["rejeitadas"] for t in topicos], "cor": "--s4"},
                                  {"nome": "não verificadas", "n": [t["nao_verificadas"] for t in topicos], "cor": "--s8"}]},
        "conferencia": {"corridas": [c["corrida"] for c in por_corrida],
                        "series": [{"nome": "erros com a causa desmentida por um fato medido", "n": [c["erros_contraditos"] for c in por_corrida], "cor": "--s1"},
                                   {"nome": "erros que as conferências não marcam", "n": [c["erros"] - c["erros_contraditos"] for c in por_corrida], "cor": "--s4"}]},
        "posicao": {"faixas": [p["faixa"] + (" (os entregues)" if i == 0 else "") for i, p in enumerate(c24["posicao_do_verbete_certo"])],
                    "series": [{"nome": "erros da corrida 24 (inéditos)", "n": [p["erros"] for p in c24["posicao_do_verbete_certo"]], "cor": "--s1"},
                               {"nome": "erros da corrida 22 (oficiais)", "n": [p["erros"] for p in c22["posicao_do_verbete_certo"]], "cor": "--s3"}]},
        "custo": {"cenarios": ["a proposta de edição de hoje (medido)"] + [c["cenario"] + " (estimado)" for c in cen["cenarios"]],
                  "segundos": [cen["medido_hoje"]["segundos"]] + [c["segundos"] for c in cen["cenarios"]],
                  "cores": ["--s4"] + ["--s1"] * len(cen["cenarios"])},
        "totais": tot,
    }
    return dados, html_


def montar(ctx: dict) -> tuple[dict, str]:
    """ctx: dados (montar_dados), road, cartoes_corridas, md_para_html, md_doc_para_html, cq, blocos_cq, ineditos,
    curadoria, planilha_curadoria, recuperador, ablacao, medicao_mcp, readme. Devolve (dados_topicos, html)."""
    dados, road = ctx["dados"], ctx["road"]
    partes: list[tuple[str, dict, str]] = []
    d, h = secao_comparativo(ctx["cq"], ctx["blocos_cq"], ctx["md_para_html"], road, ctx["cartoes_corridas"], ctx.get("analise3b"))
    partes.append(("cq", d, h))
    d, h = secao_tres_b(ctx["ineditos"], dados, road, ctx["cartoes_corridas"], ctx["md_doc_para_html"], ctx.get("analise3b"))
    partes.append(("tresb", d, h))
    d, h = secao_curadoria(ctx["curadoria"], ctx["planilha_curadoria"])
    partes.append(("curadoria", d, h))
    d, h = secao_recuperador(ctx["recuperador"])
    partes.append(("recuperador", d, h))
    ined = partes[1][1]["ineditos"]
    d, h = secao_ablacao(ctx["ablacao"], dados["curvas"]["90"][COD3B]["0"]["acerto"], ined.get(COD3B, {}).get("0", {}).get("acerto"))
    partes.append(("ablacao", d, h))
    d, h = secao_pesquisa()
    partes.append(("pesquisa", d, h))
    d, h = secao_ferramental(ctx.get("medicao_mcp"), ctx["readme"])
    partes.append(("ferramental", d, h))
    if ctx.get("analise3b"):
        d, h = secao_cruzada(ctx["analise3b"], road, ctx["cartoes_corridas"])
        partes.append(("cruzada", d, h))
    if ctx.get("relatorio3b"):
        d, h = secao_fechamento(ctx["relatorio3b"], ctx.get("pend", []), ctx["md_doc_para_html"])
        partes.append(("fechamento", d, h))
    # a aba da Pré-Fase 4 existe sempre (o mapa de navegação a lista); sem os arquivos das sondas ela mostra o estado vazio
    lev = PESQUISA / LEVANTAMENTO_PRE_FASE4
    d, h = secao_colibri(ctx.get("viabilidade"), ctx.get("logprobs_amostra"), road, ctx["cartoes_corridas"], lev.read_text(encoding="utf-8") if lev.exists() else None)
    partes.append(("colibri", d, h))
    d, h = pa.secao_atlas(ctx.get("atlas"), kpis, leitura, fontes, detalhes, validacao_do_gemini())
    partes.append(("atlas", d, h))
    d, h = secao_raciocinio(ctx.get("indicadores_raciocinio"), ctx.get("relatorio_exemplo"), ctx.get("trilhas"), ctx.get("confianca"), lev.read_text(encoding="utf-8") if lev.exists() else None)
    partes.append(("raciocinio", d, h))
    d, h = secao_cerebro(lev.read_text(encoding="utf-8") if lev.exists() else None)
    partes.append(("cerebro", d, h))
    # a aba da Fase 4 existe sempre (o mapa de navegação a lista); sem as avaliações ela mostra o estado vazio
    d, h = secao_reproducao(ctx.get("reproducao"), ctx.get("reproducao_ineditos"), road, ctx["cartoes_corridas"])
    partes.append(("reproducao", d, h))
    d, h = secao_calibracao(ctx.get("calibracao"), ctx.get("limiares"), road, ctx["cartoes_corridas"])
    partes.append(("calibracao", d, h))
    d, h = secao_tela(ctx.get("tela"), ctx.get("tela_v2"), road, ctx["cartoes_corridas"], tela_v3=ctx.get("tela_v3"), tela_v4=ctx.get("tela_v4"), tela_ineditos=ctx.get("tela_ineditos"), teto_prompt=ctx.get("teto_prompt"))
    partes.append(("tela", d, h))
    d, h = secao_cura(ctx.get("cura"), road, ctx["cartoes_corridas"])
    partes.append(("cura", d, h))
    d, h = secao_biblioteca(ctx.get("biblioteca"), road, ctx["cartoes_corridas"])
    partes.append(("biblioteca", d, h))
    d, h = secao_cenarios(ctx.get("cenarios"), ctx.get("cenarios_v2"), road, ctx["cartoes_corridas"], cen_v3=ctx.get("cenarios_v3"), cen_v4=ctx.get("cenarios_v4"))
    partes.append(("cenarios", d, h))
    d, h = secao_trilha(ctx.get("trilha"), road, ctx["cartoes_corridas"], revisao_preenchida=bool(ctx.get("revisao_trilha_preenchida")), rev=ctx.get("revisao_trilha"))
    partes.append(("trilha", d, h))
    d, h = secao_experimento(ctx.get("experimento_prompt"), road, ctx["cartoes_corridas"])
    partes.append(("experimento", d, h))
    d, h = secao_conferencia(ctx.get("conferencia_ineditos"), ctx.get("conferencia_respostas"))
    partes.append(("conferencia", d, h))
    d, h = secao_ineditos_f4(ctx.get("ineditos_f4"), road, ctx["cartoes_corridas"], ctx.get("analise3b"))
    partes.append(("ineditosf4", d, h))
    d, h = secao_fechamento_f4(ctx.get("relatorio_f4"), ctx.get("pend", []), ctx["md_doc_para_html"], tela=ctx.get("tela_v4") or ctx.get("tela_v3") or ctx.get("tela_v2"), cura=ctx.get("cura"), cenarios=ctx.get("cenarios_v4") or ctx.get("cenarios_v3") or ctx.get("cenarios_v2"), revisao=ctx.get("revisao_trilha"), road=road, cartoes_corridas=ctx["cartoes_corridas"], corrida_tela="18d" if ctx.get("tela_v4") else "18c" if ctx.get("tela_v3") else "18b", corrida_cenarios="21d" if ctx.get("cenarios_v4") else "21c" if ctx.get("cenarios_v3") else "21b")
    partes.append(("fechamentof4", d, h))
    # a aba da Pós-Fase 4 existe sempre (o mapa de navegação a lista); sem o levantamento §6.15 ela mostra o estado vazio
    d, h = secao_pos_fase4(ctx.get("levantamento_pos4"), ctx.get("plano_pos4"), ctx.get("pend", []))
    partes.append(("posfase4", d, h))
    # a aba dos filtros de texto existe sempre (o mapa de navegação a lista); sem texto.json ela mostra o estado vazio
    d, h = secao_texto(ctx.get("texto"), ctx.get("curadoria_leituras"))
    partes.append(("texto", d, h))
    # a aba da árvore de decisão existe sempre (o mapa de navegação a lista); sem as pastas arvores/ ela mostra o estado vazio
    d, h = secao_arvore(ctx.get("arvores"))
    partes.append(("arvore", d, h))
    # a aba da barra e do Git existe sempre (o mapa de navegação a lista); sem os JSON do Q4 ela mostra o estado vazio
    d, h = secao_progresso(ctx.get("taxas_progresso"), ctx.get("erro_progresso"), ctx.get("impacto_git"), ctx.get("fumaca_progresso"))
    partes.append(("progresso", d, h))
    # a aba da revisão humana existe sempre (o mapa de navegação a lista); sem leitura_revisao_v3.json ela mostra o estado vazio
    d, h = secao_revisao_v3(ctx.get("revisao_v3"), ctx.get("revisao_trilha"))
    partes.append(("revisaov3", d, h))
    # a aba das notas do modelo existe sempre (o mapa de navegação a lista); sem sem_notas_previa.json ela mostra o estado vazio
    d, h = secao_sem_notas(ctx.get("sem_notas_previa"), ctx.get("sem_notas"))
    partes.append(("semnotas", d, h))
    # a aba do fluxo do agente existe sempre (o mapa de navegação a lista); sem os JSON da rodada 7 da pesquisa ela mostra o estado vazio
    d, h = secao_fluxo(ctx.get("fluxo_resumo"), ctx.get("fluxo_medidas"), ctx.get("pend", []), ctx.get("fluxo_proposta"))
    partes.append(("fluxo", d, h))
    # a aba do segundo passe existe sempre (o mapa de navegação a lista); sem segundo_passe_previa.json ela mostra o estado vazio
    d, h = secao_segundo_passe(ctx.get("segundo_passe_previa"), ctx.get("segundo_passe"))
    partes.append(("segpasse", d, h))
    # a aba do analista de documentação existe sempre (o mapa de navegação a lista); sem portoes_m1.json ela mostra o estado vazio
    d, h = secao_analista(ctx.get("portoes_m1"), ctx.get("analista_previa"), ctx.get("analista"))
    partes.append(("analista", d, h))
    return {k: d for k, d, _ in partes}, "\n".join(h for _, _, h in partes)
