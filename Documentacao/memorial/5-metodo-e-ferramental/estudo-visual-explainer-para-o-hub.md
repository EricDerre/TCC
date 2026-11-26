<!-- ! Alteração de IA - Revisar: arquivo novo (25/11/2026, Pós-Fase 4, pacote Q6, etapa 4): o estudo de viabilidade do plugin `visual-explainer` para a página do hub central, pedido pela decisão 126 (ficha 70). A leitura dos arquivos do plugin foi feita por um subagente, só leitura, e as afirmações centrais foram conferidas por busca nos próprios arquivos (o endereço de fontes em `kit/render.mjs`, a regra do estado em forma em `SKILL.md`, a regra da pergunta sem resposta em `commands/diff-review.md`, a versão e a licença em `.claude-plugin/plugin.json`).
     ! Motivo: a decisão 126 pôs o estudo dentro do pacote Q6, e a regra do projeto pede que tudo o que foi avaliado fique registrado com o motivo, inclusive o que não serve. Sem a nota, o TCC não teria de onde dizer por que o hub não usa o plugin e quais ideias de apresentação vieram dele. -->

# Estudo de viabilidade: o `visual-explainer` e a página do hub central (25/11/2026)

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md), seção 5 (método e ferramental). Atende à decisão 126 ([decisões](../1-decisoes-e-historico/decisoes.md)) e à ficha 70 ([pendências](../pendencias.md)): o plugin entrou no trabalho com o Claude só para explicar coisas na sessão, e o estudo do que dele serve aos relatórios do hub ficou para o pacote Q6 da Pós-Fase 4.

## A pergunta e a resposta

**Pergunta:** o `visual-explainer` serve para montar os relatórios do hub, ou alguma parte dele serve à página?

**Resposta:** o plugin não entra no hub como programa, e nenhum relatório passa a ser escrito por ele. O que serve são ideias de apresentação e de interação. Duas foram aplicadas na página nesta data, cinco já estavam no desenho do hub por outro caminho, e três ficam registradas para depois.

## O que foi lido

O plugin `visual-explainer`, versão 0.15.0, licença MIT, de terceiros (https://github.com/nicobailon/visual-explainer), como está instalado na máquina do projeto. Foram lidos o arquivo de instruções (`SKILL.md`), os comandos de revisão (`commands/diff-review.md`, `plan-review.md`, `compare.md`, `fact-check.md`, `state-machine.md`, `project-recap.md`), as referências de estilo e de componentes (`references/style-guide.md`, `kit.md`, `plans.md`, `themes.md`, `diagrams.md`, `machines.md`, `motion.md`) e os dois moldes de página (`templates/page.html` e `templates/plan.html`). Os programas do kit (`kit/`, `plan/`, `mcp/`) foram lidos por amostra, só para saber do que dependem.

## Por que o plugin não entra no hub como programa

- **Quem escreve o texto é o modelo.** No plugin, o assistente escreve um arquivo de origem em HTML e um programa em Node o transforma na página final. No projeto, o relatório por caso, a árvore de decisão e o painel saem de código, a partir dos registros gravados, e nenhum número é digitado à mão (plano da Pós-Fase 4, princípios 1 e 2). Uma página que o modelo escreve a cada pedido não sai igual duas vezes e não tem teste.
- **Ele pede o Node.** O renderizador e os componentes são módulos `.mjs`. O hub roda só com o Python da biblioteca padrão (plano, seção 9: "sem runtime novo").
- **A página gerada busca fontes fora.** O renderizador põe na página um endereço do Google Fonts. O hub manda ao navegador a regra de só carregar o que vem do próprio endereço (`Content-Security-Policy: default-src 'self'`), e tudo roda sem rede.
- **Gráficos e diagramas por biblioteca de fora.** Mermaid, three.js e Chart.js aparecem nas referências do plugin; nenhum cabe na regra acima.

Nada no plugin roda sozinho: não há ganchos, e o arquivo de descrição só traz nome, versão e licença. Há um servidor MCP local e uma extensão para outro programa, que não foram ligados. Não foi achado envio de dados de uso.

## Ideias de apresentação e o que foi feito com cada uma

| Ideia do plugin | Onde está nele | No hub |
|---|---|---|
| O trecho do texto e a parte da figura que tratam da mesma coisa se acendem juntos | `references/diagrams.md` | **Aplicada em 25/11/2026:** passar o mouse (ou o foco do teclado) numa conversa acende o trecho comentado no relatório, e passar no trecho acende a conversa (`hub_pagina.py`; teste `teste_pagina_conversa_e_trecho_comentado_se_acendem_juntos`) |
| Números alinhados em coluna, medida de linha curta, escala fixa de espaços | `references/style-guide.md` | **Aplicada em parte em 25/11/2026:** os números das tabelas e das contagens usam algarismos de largura igual; a medida da linha já era limitada pelas duas colunas |
| O estado vai na forma, não só na cor ("Never color alone") | `SKILL.md` | **Já estava:** cada etiqueta de origem da árvore traz a palavra (observado, conferido, declarado, desconhecido), e a de desconhecido tem a borda tracejada; a conversa traz o estado escrito |
| Comentar um trecho selecionado, com o botão aparecendo só depois da seleção | `kit/reply.js` | **Já estava**, pelo modelo de revisão do GitHub e do Azure DevOps (levantamento §6.15.1) |
| A pergunta que o leitor deixou sem resposta não vale como "sim" | `commands/diff-review.md` | **Já estava, mais estrito:** o veredito nunca vem escolhido, e a página recusa enviar a revisão sem ele. O plugin deixa uma opção sugerida pelo assistente; no hub o agente só comenta (plano, princípio 4) |
| A primeira tela é a resposta; depois a evidência, os riscos e os próximos passos | `SKILL.md` | **Já estava:** o caso abre pelo comentário do agente e pelo título, com a evidência ao lado |
| Tema claro e escuro por variáveis de estilo, seguindo o sistema | `kit/kit.css` | **Já estava:** as cores são as do painel do projeto, com o tema escuro pelo sistema |
| Árvore de afirmações em que cada frase pode ser falsa e aponta a sua prova | `references/plans.md` | **Registrada, não aplicada:** a árvore de decisão do hub já traz a origem de cada afirmação; falta o salto da afirmação para o evento da trilha que a sustenta (o JSON da árvore guarda os números dos eventos), que fica como trabalho futuro |
| Passo a passo com um evento por vez e a explicação ao lado, sem tocar sozinho | `references/motion.md` | **Registrada, não aplicada:** serviria para refazer o caminho do agente na aba Trilha; hoje a aba mostra a tabela dos eventos com filtro por tipo |
| Máquina de estados desenhada do código, com os caminhos que quebram uma regra | `references/machines.md` | **Registrada, não aplicada:** dependeria de rodar o código do projeto dentro do Node; a ideia de marcar o caminho que quebra a regra serve ao roteiro de cada cenário, se um dia ele for desenhado |

## O que não serve, com o motivo

- **Qualquer página em que o modelo escreve o conteúdo:** o relatório tem de sair de código.
- **O renderizador e as marcas próprias do kit (`ve-ask`, `ve-opt` e as outras):** pedem o Node; só o que eles produzem é HTML comum, e copiar o resultado sem o programa não traria vantagem sobre escrever a página à mão, como foi feito.
- **As fontes do Google Fonts e as bibliotecas de gráfico por endereço de fora:** quebram a regra de só carregar o que vem do próprio hub.
- **Vídeo, slides e exportação para PowerPoint:** não fazem parte de uma página de revisão.
- **A opção já marcada como sugestão do assistente:** no hub seria o agente aprovando por omissão.

## Limites deste estudo

Foi uma leitura dos arquivos, sem gerar página nenhuma com o plugin. Os programas do kit foram lidos por amostra. A versão lida é a 0.15.0; uma versão nova pode mudar o que está aqui.
