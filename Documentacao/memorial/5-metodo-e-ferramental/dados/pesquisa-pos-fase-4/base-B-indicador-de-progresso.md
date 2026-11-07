<!-- ! Alteração de IA - Revisar: arquivo novo (07/11/2026): leitura feita por um subagente do Claude (modelo Sonnet) sobre a barra de progresso para a espera da inferência local, na rodada 6 da pesquisa (Pós-Fase 4); é um arquivo de dados que ferramentas/integrar_pesquisa_pos_fase4.py lê para montar o levantamento §6.15, e o integrador tira este comentário do texto que entra lá.
     ! Motivo: o Eric pediu em 07/11/2026 a base de pesquisa de cada ponto da Pós-Fase 4 e a validação de oito repositórios do GitHub; a leitura fica versionada como dado para o levantamento ser regerado por script e conferido pelo --check. O texto é o que o subagente escreveu, sem edição, com a marca de confiança que ele deu a cada fonte (aberta e lida; só o resumo de busca; de memória). -->
# Base B: indicador de progresso para a espera da inferência local

Levantamento de 7 nov. 2026. Cada fonte marca se a página foi aberta e lida. O que está fora das fontes é inferência minha e vem sinalizado.

## 1. Limites de tempo de resposta

**NIELSEN, Jakob. Response times: the 3 important limits. Nielsen Norman Group, 1 jan. 1993 (trecho de Usability Engineering; atualizado em 2014). Disponível em: https://www.nngroup.com/articles/response-times-3-important-limits/. Acesso em: 7 nov. 2026.** (aberta e lida)
- Estabelece os limites de 0,1 s (reação sentida como instantânea), 1,0 s (o fluxo de raciocínio se mantém) e 10 s (limite da atenção; depois disso o usuário passa a fazer outra coisa). Acima de 10 s, recomenda indicador de porcentagem concluída e dizer quando o computador espera terminar. Diz que isso mostra que o sistema não travou e deixa o usuário decidir fazer outra coisa. Prefere barra gráfica a estimativa numérica sozinha. O feedback pesa mais quando o tempo varia muito.
- Aplicação: a inferência de 40 a 130 s está de 4 a 13 vezes acima do limite de 10 s, e o tempo varia. Cai exatamente no caso em que a fonte pede indicador de porcentagem com estimativa.

## 2. Percent-done e percepção de duração

**MYERS, Brad A. Using percent-done progress indicators to enhance user interfaces. In: GRAPHICS INTERFACE '85, 1985, Montréal. Proceedings [...]. 1985. p. 167-170. DOI 10.20380/GI1985.24. Disponível em: https://graphicsinterface.org/wp-content/uploads/2015/03/gi1985-24.pdf. Acesso em: 7 nov. 2026.** (aberta e lida; é o resumo estendido do artigo de CHI '85, que não consegui abrir)
- Resume o experimento do artigo de CHI '85 (MYERS, B. A. The importance of percent-done progress indicators for computer-human interfaces. In: CHI '85, São Francisco, 14-18 abr. 1985, p. 11-17): 48 sujeitos, versões com e sem indicador, preferência pelo indicador com p = 0,0006 e 86,1% dos sujeitos gostando dele. O indicador mostra "se o programa travou", ao contrário de ampulheta estática. Não achou preferência significativa por tempo constante contra variável (p = 0,2046).
- Aplicação: base mais antiga para dizer que o indicador de fração concluída é preferido e distingue espera de travamento. Citar o CHI '85 pelo resumo exige a ressalva de que li o resumo, não o original.

**HARRISON, Chris; AMENTO, Brian; KUZNETSOV, Stacey; BELL, Robert. Rethinking the progress bar. In: ACM SYMPOSIUM ON USER INTERFACE SOFTWARE AND TECHNOLOGY (UIST), 20., 2007, Newport. Proceedings [...]. New York: ACM, 2007. p. 115-118. Disponível em: https://chrisharrison.net/projects/progressbars/ProgBarHarrison.pdf. Acesso em: 7 nov. 2026.** (PDF aberto e lido)
- 22 participantes, 990 comparações pareadas de 9 funções de avanço da barra. Barras com pausas perto do fim foram percebidas como mais lentas que a linear; as de avanço acelerado no fim (funções exponenciais) foram percebidas como mais rápidas. Os usuários toleram mais os trechos lentos ou irregulares no começo da operação do que no fim. A primeira função vista foi preferida em 38% das comparações contra 26% da segunda.
- Aplicação: a barra não deve parar nem congelar perto de 100%. Se a estimativa errar, errar para menos no começo é menos prejudicial do que travar no final.

## 3. Determinado e indeterminado

**APPLE. Human Interface Guidelines: Progress indicators. Cupertino: Apple, 2023 (alterado em 12 set. 2023). Disponível em: https://developer.apple.com/design/human-interface-guidelines/progress-indicators. Acesso em: 7 nov. 2026.** (aberta e lida, em versão Markdown da mesma página)
- Pede indicador determinado "quando possível", porque o indeterminado só mostra que há processo e não ajuda a estimar a duração; o determinado ajuda a decidir se espera, refaz depois ou abandona. Pede avanço regular (exemplo ruim: 90% em 5 s e os 10% finais em 5 min), indicador sempre em movimento (parado é lido como travado), trocar de indeterminado para determinado assim que a duração for conhecida, descrição curta e precisa (sem "carregando") e botão de cancelar quando for viável.
- Aplicação: é a fonte mais próxima do desenho: começa indeterminado nos primeiros segundos e vira barra determinada quando a estimativa existir, sem mudar o formato (não trocar de círculo para barra).

**MATERIAL COMPONENTS ANDROID. Progress indicator. GitHub: material-components-android, docs/components/ProgressIndicator.md. Disponível em: https://github.com/material-components/material-components-android/blob/master/docs/components/ProgressIndicator.md. Acesso em: 7 nov. 2026.** (aberta e lida; as páginas m2.material.io e m3.material.io não devolveram texto)
- Determinado: preenche de 0% a 100%, para quando progresso e espera são conhecidos. Indeterminado: movimento sem fração, para quando são desconhecidos. Um indeterminado pode virar determinado quando o progresso passa a ser informado.
- Aplicação: mesma regra de decisão da Apple, com a transição indeterminado para determinado prevista no componente.

**NIELSEN NORMAN GROUP. Progress indicators make a slow system less insufferable. Disponível em: https://www.nngroup.com/articles/progress-indicators/. Acesso em: 7 nov. 2026.** (aberta e lida; o texto buscado não trazia o nome do autor nem o ano, confirmar antes de citar na ABNT)
- Indicador para qualquer ação acima de cerca de 1 s. Animação em laço (sem informação de tempo) para 2 a 10 s; porcentagem concluída para 10 s ou mais. Laço acima de 10 s faz o usuário perder a confiança de que há avanço. Evitar texto estático como "Carregando...". Se as estimativas variam muito, baixar o corte para dar porcentagem a mais casos. Para séries, usar contagem ("3 de 50").
- Aplicação: 40 a 130 s fica muito acima do corte de 10 s. A fonte pede porcentagem mais texto de etapa, e a contagem de etapas serve para o que o agente fizer antes e depois da inferência.

## 4. Estimar o tempo restante da inferência

**OLLAMA. API reference: generate a completion. GitHub: ollama/ollama, docs/api.md. Disponível em: https://github.com/ollama/ollama/blob/main/docs/api.md. Acesso em: 7 nov. 2026.** (aberta e lida)
- Campos em nanossegundos: total_duration, load_duration, prompt_eval_duration (tokens do prompt que não vieram do cache) e eval_duration (geração). Contagens: prompt_eval_count e eval_count. Em stream, os objetos intermediários trazem a resposta parcial com done = false, e o último (done = true) traz as estatísticas, com o campo response vazio. Tokens por segundo = eval_count / eval_duration x 10^9.
- Aplicação: as durações só chegam no fim. Durante a espera o stream entrega a contagem de tokens gerados, mas nenhuma estatística de tempo. A taxa de prefill (prompt_eval_count / prompt_eval_duration) e a de geração das respostas anteriores são o que alimenta a estimativa da próxima. Inferência minha: o fim do prefill não aparece nos campos do stream; só dá para detectá-lo pelo chegada do primeiro objeto com texto.

## 5. Percepção de espera com feedback

**BUELL, Ryan W.; NORTON, Michael I. The labor illusion: how operational transparency increases perceived value. Management Science, v. 57, n. 9, p. 1564-1579, 2011. DOI 10.1287/mnsc.1110.1376. Disponível em: https://ideas.repec.org/a/inm/ormnsc/v57y2011i9p1564-1579.html. Acesso em: 7 nov. 2026.** (só o resumo e os dados bibliográficos, em índice RePEc; não abri o artigo completo)
- Cinco experimentos (viagens e encontros on-line simulados): quando o site mostra que está trabalhando, as pessoas podem preferir a versão mais lenta à que devolve o mesmo resultado na hora, e o efeito passa pela percepção de esforço e de reciprocidade.
- Aplicação: apoia mostrar o que o agente está fazendo (lendo o prompt, gerando o diagnóstico) em vez de um spinner mudo. Cuidado de escopo: o estudo trata de valor percebido pelo cliente, não de tolerância à espera de um analista.

## O que isso fixa para o desenho

Usar uma barra determinada, com texto de etapa e tempo restante estimado, e não um spinner puro: a inferência passa muito de 10 s, o tempo varia, e as três fontes de interface (Nielsen, Apple, Material) pedem determinado quando a duração é estimável. A estimativa vem do que o Ollama já devolveu em respostas anteriores do mesmo modelo: taxa de prefill em tokens por segundo (tokens do prompt conhecidos antes de enviar, pela contagem) e taxa de geração (eval_count / eval_duration), guardadas por modelo e máquina. O prefill é cerca de 79% a 83% do tempo medido pelo projeto, então a barra deve ter duas fases: a primeira, longa, estimada por tokens do prompt dividido pela taxa de prefill; a segunda, pela taxa de geração contra um teto de tokens de saída. Nos primeiros segundos mostrar o indicador indeterminado já com a etapa nomeada ("lendo o contexto do caso, N tokens"), imediatamente após a ação, e passar para a barra determinada assim que a estimativa existir, no mesmo formato, para não trocar de forma no meio (Apple). A barra deve se mover sempre, avançar de modo regular, não parar em 99% (Apple, Harrison: pausas no fim parecem mais lentas) e oferecer cancelar. Quando a geração começar, o stream permite contar tokens recebidos e corrigir a fração. Se a estimativa estiver errada, preferir errar para o lado de acabar depois, sem congelar o final. Isto último é inferência a partir de Harrison, não afirmação de uma das fontes.

## O que não achei

Não achei fonte que trate de estimar o tempo restante de prefill mais geração em LLM local a partir de tokens por segundo medidos antes; a documentação do Ollama dá só os campos e a fórmula de tokens por segundo, e a regra de duas fases é derivação minha. Não consegui abrir as páginas do Material Design 3 e m2.material.io (conteúdo dinâmico, voltou só o título), então a fonte de Material é a documentação do componente no GitHub. O artigo original de Myers em CHI '85 não foi aberto; usei o resumo estendido do próprio autor. O artigo completo de Buell e Norton não foi aberto (só resumo em índice RePEc), e não há evidência nele sobre analistas técnicos em espera de 40 a 130 s. A autoria e o ano do artigo "Progress indicators" da NN/g precisam ser conferidos. Não busquei estudos de tolerância à espera acima de 60 s nem de barras com estimativa errada.
