<!-- ! Alteração de IA - Revisar: arquivo gerado por ferramentas/integrar_pesquisa_pos_fase4.py a partir das leituras guardadas em 5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/ (rodada 6 da pesquisa, 07/11/2026). NÃO editar as subseções à mão (o --check compara com o regerado).
     ! Motivo: a Pós-Fase 4 foi especificada pelo Eric em 07/11/2026 em três partes, e o plano dela precisa apontar a fonte de cada ponto; a pesquisa entra por script, nunca colada à mão, e o que não serve fica registrado com o motivo (§6.15.15). -->

# Levantamento bibliográfico: Pós-Fase 4 (07/11/2026)

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). Continua o [levantamento da Pré-Fase 4](levantamento-2026-10-01-pre-fase-4.md) (§6.14). O que motivou: o Eric especificou a Pós-Fase 4 em três partes: (1) o visual e a usabilidade do agente, com um hub central à imagem de uma pull request, a integração com o Git, a barra de progresso, a árvore de decisão e a normalização das respostas por filtros determinísticos; (2) o projeto contra o syllabus CTFL 4.0 do ISTQB, na tradução do BSTQB; (3) oito repositórios do GitHub, com a viabilidade para o Claude Code e para o agente ([roadmap](../roadmap.md), §4.8; plano aprovado em `claude-memoria/plano-aprovado-pos-fase-4.md`). Referências completas em [referencias.md](referencias.md).

### 6.15 Levantamento da Pós-Fase 4

14 leituras em 07/11/2026: 5 bases da parte 1 (o visual e a usabilidade do agente), 1 da parte 2 (o projeto contra o syllabus CTFL 4.0) e 8 da parte 3 (os oito repositórios do GitHub), com 78 fontes com endereço no total. Diferente das rodadas 1 a 5, esta rodada não passou por um Workflow com pesquisador, verificadores céticos e síntese: cada leitura foi feita por um subagente (as bases e os repositórios) ou pelo Claude na sessão principal (o syllabus), que abriu as páginas, os README e os PDF que conseguiu e marcou, fonte a fonte, o que leu por inteiro, o que só viu em resumo de busca e o que veio de memória. Um número citado vale com a marca da fonte de onde veio; nenhuma afirmação foi conferida por um segundo agente. Os textos entram como os leitores os escreveram, com os títulos rebaixados para caber na numeração; o mapa final é do Claude.

| Subseção | Parte | Leitura | Fontes com endereço |
|---|---|---|---|
| §6.15.1 | 1 | `pos4-revisao-estilo-pr` | 9 |
| §6.15.2 | 1 | `pos4-indicador-de-progresso` | 8 |
| §6.15.3 | 1 | `pos4-arvore-de-decisao` | 9 |
| §6.15.4 | 1 | `pos4-metricas-de-prolixidade` | 10 |
| §6.15.5 | 1 | `pos4-impacto-git-e-vm` | 16 |
| §6.15.6 | 2 | `pos4-syllabus-ctfl` | 1 |
| §6.15.7 | 3 | `pos4-repo-dimensional-drawing` | 3 |
| §6.15.8 | 3 | `pos4-repo-rag-anything` | 2 |
| §6.15.9 | 3 | `pos4-repo-mcptoon` | 7 |
| §6.15.10 | 3 | `pos4-repo-understand-anything` | 1 |
| §6.15.11 | 3 | `pos4-repo-agenttrail` | 4 |
| §6.15.12 | 3 | `pos4-repo-eagle-4` | 2 |
| §6.15.13 | 3 | `pos4-repo-gepa` | 2 |
| §6.15.14 | 3 | `pos4-repo-claude-obsidian` | 4 |

Quatro avisos sobre o texto abaixo:

1. **Sem verificação cética.** As rodadas 1 a 5 passaram cada afirmação por um verificador; esta não. O que cada leitura afirma vale com a marca de confiança que o leitor pôs na fonte (aberta e lida; só o resumo de busca; de memória), e as leituras dizem o que não conseguiram abrir.
2. **Fontes sem revisão por pares.** Os repositórios, a documentação do GitHub, do Azure DevOps, da Apple, do Material e do Ollama e os blogs citados não têm revisão por pares; os artigos citados trazem o veículo e o ano. Os números de desempenho dos repositórios são medições dos próprios autores, lidas nos README.
3. **Grafia.** O texto das leituras entra como foi escrito, sem travessão nem seta, como manda a regra de documentação; títulos e citações literais das fontes ficam como na fonte.
4. **O que já foi decidido.** As decisões 101 a 106 (fichas 49 a 54) foram tomadas pelo Eric no quadro da sessão de 07/11/2026 lendo estas leituras; o mapa do §6.15.15 foi escrito pelo Claude, e o plano que o incorpora foi aprovado como está (ficha 54, decisão 105), sem sessão de teste para os repositórios marcados como opcionais (ficha 53, decisão 106).


#### 6.15.1 O hub central à imagem de uma pull request: o modelo de revisão do GitHub e do Azure DevOps (`pos4-revisao-estilo-pr`; 9 fontes com endereço)

*Leitura de:* subagente, em 07/11/2026; arquivo `base-A-revisao-estilo-pr.md` em `5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/`.

Consulta feita em 7 nov. 2026. Todas as páginas abaixo foram abertas (WebFetch), salvo onde indicado.

##### a) Modelo de revisão do GitHub e do Azure DevOps

**1. GITHUB. About pull request reviews.** GitHub Docs. Disponível em: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews. Acesso em: 7 nov. 2026.
- Uma revisão termina em um de três estados: Comment (feedback geral), Approve (pronto para integrar) e Request changes (o autor deve tratar antes de integrar). Comentários de linha aparecem na linha do tempo da PR.
- Aplicação: o hub precisa de exatamente esses três desfechos para o diagnóstico (comentar, aprovar, pedir mudança).

**2. GITHUB. Reviewing proposed changes in a pull request.** GitHub Docs. Disponível em: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/reviewing-proposed-changes-in-a-pull-request. Acesso em: 7 nov. 2026.
- Comentário pode abranger várias linhas (primeira linha mais shift+clique na última). Comentários de linha ficam pendentes e visíveis só ao autor até o envio da revisão com um resumo; dá para descartar tudo. Arquivo marcado como "Viewed" colapsa, há barra de progresso, e a marca some se o arquivo muda depois.
- Aplicação: comentário ancorado em trecho da evidência, rascunho antes de enviar, e marca de "já li" que se invalida quando o agente refaz o diagnóstico.

**3. GITHUB. Incorporating feedback in your pull request.** GitHub Docs. Disponível em: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/incorporating-feedback-in-your-pull-request. Acesso em: 7 nov. 2026.
- "Suggested changes" propõem edição exata; podem ser aplicadas uma a uma ou em lote, com o sugeridor creditado como coautor. A página aberta não cobre "resolver conversa".
- Aplicação: o análogo é o analista propor o rótulo de causa corrigido, registrado com autoria.

**4. MICROSOFT. Review and comment on pull requests (Azure Repos).** Microsoft Learn, atualizada em 8 set. 2026. Disponível em: https://learn.microsoft.com/en-us/azure/devops/repos/git/review-pull-requests?view=azure-devops. Acesso em: 7 nov. 2026.
- Comentários em linha, em intervalo de linhas, em arquivo inteiro (nível de arquivo) e gerais na aba Overview. Cada thread tem estado: Active (padrão), Pending, Resolved, Won't fix, Closed; filtro por estado e "What's new" desde a última abertura. Votos: Approve, Approve with suggestions, Wait for author, Reject (com comentário explicando); Wait for author e Reject de revisor obrigatório bloqueiam. Aba Updates numera as iterações (push) e permite ver só o que mudou desde a última revisão; "Mark as reviewed" por arquivo. Revisão do Copilot sempre sai como Comment e não bloqueia.
- Aplicação: é o modelo mais completo para o hub (threads com estado, iterações, voto de cinco valores, IA que só comenta e nunca aprova).

##### b) Pesquisa sobre revisão de código

**5. BACCHELLI, A.; BIRD, C. Expectations, outcomes, and challenges of modern code review.** In: INTERNATIONAL CONFERENCE ON SOFTWARE ENGINEERING (ICSE), 35., 2013, São Francisco. Anais [...]. IEEE, 2013. p. 712-721. DOI 10.1109/ICSE.2013.6606617. Disponível em: https://2013.icse-conferences.org/content/expectations-outcomes-and-challenges-modern-code-review.html. Acesso em: 7 nov. 2026. (Páginas, DOI e local conferidos só por resultado de busca; a página aberta traz autores e resumo.)
- Estudo na Microsoft (observação, entrevistas, pesquisa, classificação manual de centenas de comentários): achar defeitos é o objetivo declarado, mas a revisão rende menos defeitos que o esperado e mais transferência de conhecimento, consciência do time e soluções alternativas. Entender o código e a mudança é o núcleo, e as ferramentas apoiam mal as estratégias que os revisores usam para isso.
- Aplicação: o hub deve gastar seu desenho em ajudar o analista a entender o diagnóstico (contexto, evidência ao lado), não em checklist de defeitos.

**6. SADOWSKI, C. et al. Modern code review: a case study at Google.** In: ICSE-SEIP, 2018. Disponível em: https://research.google/pubs/modern-code-review-a-case-study-at-google/. Acesso em: 7 nov. 2026.
- 12 entrevistas, pesquisa com 44 respondentes e logs de 9 milhões de mudanças revisadas: revisão leve, baseada em ferramenta. Latência (mediana de aprovação abaixo de 4 horas) vem de fontes secundárias, não confirmada no texto do artigo (conferir o DOI 10.1145/3183519.3183525 antes de citar).
- Aplicação: sustenta que o formato leve e rápido funciona em escala; o hub deve manter o custo por revisão baixo.

##### c) Humanos revisando saída de IA

**7. CYNTHIA, S. T. et al. "Go Home Copilot, You're Drunk": understanding developer responses to agent-generated code review comments.** arXiv:2607.21997, 24 jul. 2026 (v2, 29 jul. 2026), preprint. Disponível em: https://arxiv.org/abs/2607.21997. Acesso em: 7 nov. 2026.
- 54.791 comentários de cinco agentes (Copilot, Cursor, Codex, Devin, Claude) em 342 repositórios Python. Sugestão em linha foi o maior preditor de resolução; comentários longos e complexos são menos atendidos; entre 470 discussões não resolvidas, os motivos mais comuns foram sugestão incorreta e decisão de projeto intencional.
- Aplicação: o diagnóstico do agente deve vir curto, ancorado e com correção concreta, e o analista precisa poder registrar "o agente errou" ou "decisão intencional" como desfecho.

##### d) Comentários objetivos

**8. GOOGLE. The standard of code review.** Google Engineering Practices. Disponível em: https://google.github.io/eng-practices/review/reviewer/standard.html. Acesso em: 7 nov. 2026.
- Aprovar quando a mudança melhora claramente a saúde do código, mesmo imperfeita; prefixar com "Nit:" o que não é essencial; marcar como opcional o comentário educativo; fatos técnicos pesam mais que preferência.
- Aplicação: dá o critério de aprovação do diagnóstico (correto o bastante e útil) e a distinção bloqueante e não bloqueante.

**9. CONVENTIONAL COMMENTS. Conventional Comments.** Disponível em: https://conventionalcomments.org/. Acesso em: 7 nov. 2026.
- Formato `<rótulo> [decorações]: <assunto>` mais discussão opcional; rótulos praise, nitpick, suggestion, issue, todo, question, thought, chore, note; decorações (blocking), (non-blocking), (if-minor). Justificativa: previsível e legível por máquina.
- Aplicação: rótulos estruturados viram campo do comentário e dão dado analisável para o TCC.

##### O que isso fixa para o desenho

Para ser fiel ao modelo de PR, o hub precisa de: (1) região do artefato à vista, com evidência (resposta HTTP, árvore da tela, contrato) ao lado do diagnóstico; (2) comentário ancorado em trecho, com intervalo, mais comentário geral da revisão e opcionalmente por bloco (equivalente a nível de arquivo); (3) threads com estado (ativo, resolvido, não será tratado), rascunho pendente enviado junto com o veredito; (4) veredito de três a cinco valores, em que a IA nunca aprova sozinha; (5) iterações numeradas com "o que mudou desde a sua última revisão" e marca de lido que se invalida; (6) uma sugestão estruturada (causa corrigida) em vez de texto livre; (7) rótulo e decoração de bloqueio no comentário. Não precisa de: diff de linhas (o artefato não é código, basta comparar iterações), branches, merge, políticas de revisores obrigatórios, commit de sugestão, curtidas, nem edição de arquivo. A pesquisa pede foco em compreensão e brevidade, não em volume de comentários.

##### O que não achei

Nenhuma medição em interface de revisão de diagnóstico de falha de teste ou de causa raiz por IA; os estudos de revisão de saída de IA (item 7) tratam de código. A página de GitHub aberta não detalha "resolver conversa" nem "alterações desde a última revisão" (só confirmado no Azure DevOps). O artigo de Bacchelli e Bird não foi aberto no PDF (repositório da TU Delft recusou conexão) e o de Sadowski só no resumo; números de latência vêm de fontes secundárias. O item 7 é preprint sem revisão por pares confirmada. Não localizei estudo que meça a eficácia dos Conventional Comments; é guia de comunidade, não pesquisa.

#### 6.15.2 A barra de progresso para a espera da inferência local (`pos4-indicador-de-progresso`; 8 fontes com endereço)

*Leitura de:* subagente, em 07/11/2026; arquivo `base-B-indicador-de-progresso.md` em `5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/`.

Levantamento de 7 nov. 2026. Cada fonte marca se a página foi aberta e lida. O que está fora das fontes é inferência minha e vem sinalizado.

##### 1. Limites de tempo de resposta

**NIELSEN, Jakob. Response times: the 3 important limits. Nielsen Norman Group, 1 jan. 1993 (trecho de Usability Engineering; atualizado em 2014). Disponível em: https://www.nngroup.com/articles/response-times-3-important-limits/. Acesso em: 7 nov. 2026.** (aberta e lida)
- Estabelece os limites de 0,1 s (reação sentida como instantânea), 1,0 s (o fluxo de raciocínio se mantém) e 10 s (limite da atenção; depois disso o usuário passa a fazer outra coisa). Acima de 10 s, recomenda indicador de porcentagem concluída e dizer quando o computador espera terminar. Diz que isso mostra que o sistema não travou e deixa o usuário decidir fazer outra coisa. Prefere barra gráfica a estimativa numérica sozinha. O feedback pesa mais quando o tempo varia muito.
- Aplicação: a inferência de 40 a 130 s está de 4 a 13 vezes acima do limite de 10 s, e o tempo varia. Cai exatamente no caso em que a fonte pede indicador de porcentagem com estimativa.

##### 2. Percent-done e percepção de duração

**MYERS, Brad A. Using percent-done progress indicators to enhance user interfaces. In: GRAPHICS INTERFACE '85, 1985, Montréal. Proceedings [...]. 1985. p. 167-170. DOI 10.20380/GI1985.24. Disponível em: https://graphicsinterface.org/wp-content/uploads/2015/03/gi1985-24.pdf. Acesso em: 7 nov. 2026.** (aberta e lida; é o resumo estendido do artigo de CHI '85, que não consegui abrir)
- Resume o experimento do artigo de CHI '85 (MYERS, B. A. The importance of percent-done progress indicators for computer-human interfaces. In: CHI '85, São Francisco, 14-18 abr. 1985, p. 11-17): 48 sujeitos, versões com e sem indicador, preferência pelo indicador com p = 0,0006 e 86,1% dos sujeitos gostando dele. O indicador mostra "se o programa travou", ao contrário de ampulheta estática. Não achou preferência significativa por tempo constante contra variável (p = 0,2046).
- Aplicação: base mais antiga para dizer que o indicador de fração concluída é preferido e distingue espera de travamento. Citar o CHI '85 pelo resumo exige a ressalva de que li o resumo, não o original.

**HARRISON, Chris; AMENTO, Brian; KUZNETSOV, Stacey; BELL, Robert. Rethinking the progress bar. In: ACM SYMPOSIUM ON USER INTERFACE SOFTWARE AND TECHNOLOGY (UIST), 20., 2007, Newport. Proceedings [...]. New York: ACM, 2007. p. 115-118. Disponível em: https://chrisharrison.net/projects/progressbars/ProgBarHarrison.pdf. Acesso em: 7 nov. 2026.** (PDF aberto e lido)
- 22 participantes, 990 comparações pareadas de 9 funções de avanço da barra. Barras com pausas perto do fim foram percebidas como mais lentas que a linear; as de avanço acelerado no fim (funções exponenciais) foram percebidas como mais rápidas. Os usuários toleram mais os trechos lentos ou irregulares no começo da operação do que no fim. A primeira função vista foi preferida em 38% das comparações contra 26% da segunda.
- Aplicação: a barra não deve parar nem congelar perto de 100%. Se a estimativa errar, errar para menos no começo é menos prejudicial do que travar no final.

##### 3. Determinado e indeterminado

**APPLE. Human Interface Guidelines: Progress indicators. Cupertino: Apple, 2023 (alterado em 12 set. 2023). Disponível em: https://developer.apple.com/design/human-interface-guidelines/progress-indicators. Acesso em: 7 nov. 2026.** (aberta e lida, em versão Markdown da mesma página)
- Pede indicador determinado "quando possível", porque o indeterminado só mostra que há processo e não ajuda a estimar a duração; o determinado ajuda a decidir se espera, refaz depois ou abandona. Pede avanço regular (exemplo ruim: 90% em 5 s e os 10% finais em 5 min), indicador sempre em movimento (parado é lido como travado), trocar de indeterminado para determinado assim que a duração for conhecida, descrição curta e precisa (sem "carregando") e botão de cancelar quando for viável.
- Aplicação: é a fonte mais próxima do desenho: começa indeterminado nos primeiros segundos e vira barra determinada quando a estimativa existir, sem mudar o formato (não trocar de círculo para barra).

**MATERIAL COMPONENTS ANDROID. Progress indicator. GitHub: material-components-android, docs/components/ProgressIndicator.md. Disponível em: https://github.com/material-components/material-components-android/blob/master/docs/components/ProgressIndicator.md. Acesso em: 7 nov. 2026.** (aberta e lida; as páginas m2.material.io e m3.material.io não devolveram texto)
- Determinado: preenche de 0% a 100%, para quando progresso e espera são conhecidos. Indeterminado: movimento sem fração, para quando são desconhecidos. Um indeterminado pode virar determinado quando o progresso passa a ser informado.
- Aplicação: mesma regra de decisão da Apple, com a transição indeterminado para determinado prevista no componente.

**NIELSEN NORMAN GROUP. Progress indicators make a slow system less insufferable. Disponível em: https://www.nngroup.com/articles/progress-indicators/. Acesso em: 7 nov. 2026.** (aberta e lida; o texto buscado não trazia o nome do autor nem o ano, confirmar antes de citar na ABNT)
- Indicador para qualquer ação acima de cerca de 1 s. Animação em laço (sem informação de tempo) para 2 a 10 s; porcentagem concluída para 10 s ou mais. Laço acima de 10 s faz o usuário perder a confiança de que há avanço. Evitar texto estático como "Carregando...". Se as estimativas variam muito, baixar o corte para dar porcentagem a mais casos. Para séries, usar contagem ("3 de 50").
- Aplicação: 40 a 130 s fica muito acima do corte de 10 s. A fonte pede porcentagem mais texto de etapa, e a contagem de etapas serve para o que o agente fizer antes e depois da inferência.

##### 4. Estimar o tempo restante da inferência

**OLLAMA. API reference: generate a completion. GitHub: ollama/ollama, docs/api.md. Disponível em: https://github.com/ollama/ollama/blob/main/docs/api.md. Acesso em: 7 nov. 2026.** (aberta e lida)
- Campos em nanossegundos: total_duration, load_duration, prompt_eval_duration (tokens do prompt que não vieram do cache) e eval_duration (geração). Contagens: prompt_eval_count e eval_count. Em stream, os objetos intermediários trazem a resposta parcial com done = false, e o último (done = true) traz as estatísticas, com o campo response vazio. Tokens por segundo = eval_count / eval_duration x 10^9.
- Aplicação: as durações só chegam no fim. Durante a espera o stream entrega a contagem de tokens gerados, mas nenhuma estatística de tempo. A taxa de prefill (prompt_eval_count / prompt_eval_duration) e a de geração das respostas anteriores são o que alimenta a estimativa da próxima. Inferência minha: o fim do prefill não aparece nos campos do stream; só dá para detectá-lo pelo chegada do primeiro objeto com texto.

##### 5. Percepção de espera com feedback

**BUELL, Ryan W.; NORTON, Michael I. The labor illusion: how operational transparency increases perceived value. Management Science, v. 57, n. 9, p. 1564-1579, 2011. DOI 10.1287/mnsc.1110.1376. Disponível em: https://ideas.repec.org/a/inm/ormnsc/v57y2011i9p1564-1579.html. Acesso em: 7 nov. 2026.** (só o resumo e os dados bibliográficos, em índice RePEc; não abri o artigo completo)
- Cinco experimentos (viagens e encontros on-line simulados): quando o site mostra que está trabalhando, as pessoas podem preferir a versão mais lenta à que devolve o mesmo resultado na hora, e o efeito passa pela percepção de esforço e de reciprocidade.
- Aplicação: apoia mostrar o que o agente está fazendo (lendo o prompt, gerando o diagnóstico) em vez de um spinner mudo. Cuidado de escopo: o estudo trata de valor percebido pelo cliente, não de tolerância à espera de um analista.

##### O que isso fixa para o desenho

Usar uma barra determinada, com texto de etapa e tempo restante estimado, e não um spinner puro: a inferência passa muito de 10 s, o tempo varia, e as três fontes de interface (Nielsen, Apple, Material) pedem determinado quando a duração é estimável. A estimativa vem do que o Ollama já devolveu em respostas anteriores do mesmo modelo: taxa de prefill em tokens por segundo (tokens do prompt conhecidos antes de enviar, pela contagem) e taxa de geração (eval_count / eval_duration), guardadas por modelo e máquina. O prefill é cerca de 79% a 83% do tempo medido pelo projeto, então a barra deve ter duas fases: a primeira, longa, estimada por tokens do prompt dividido pela taxa de prefill; a segunda, pela taxa de geração contra um teto de tokens de saída. Nos primeiros segundos mostrar o indicador indeterminado já com a etapa nomeada ("lendo o contexto do caso, N tokens"), imediatamente após a ação, e passar para a barra determinada assim que a estimativa existir, no mesmo formato, para não trocar de forma no meio (Apple). A barra deve se mover sempre, avançar de modo regular, não parar em 99% (Apple, Harrison: pausas no fim parecem mais lentas) e oferecer cancelar. Quando a geração começar, o stream permite contar tokens recebidos e corrigir a fração. Se a estimativa estiver errada, preferir errar para o lado de acabar depois, sem congelar o final. Isto último é inferência a partir de Harrison, não afirmação de uma das fontes.

##### O que não achei

Não achei fonte que trate de estimar o tempo restante de prefill mais geração em LLM local a partir de tokens por segundo medidos antes; a documentação do Ollama dá só os campos e a fórmula de tokens por segundo, e a regra de duas fases é derivação minha. Não consegui abrir as páginas do Material Design 3 e m2.material.io (conteúdo dinâmico, voltou só o título), então a fonte de Material é a documentação do componente no GitHub. O artigo original de Myers em CHI '85 não foi aberto; usei o resumo estendido do próprio autor. O artigo completo de Buell e Norton não foi aberto (só resumo em índice RePEc), e não há evidência nele sobre analistas técnicos em espera de 40 a 130 s. A autoria e o ano do artigo "Progress indicators" da NN/g precisam ser conferidos. Não busquei estudos de tolerância à espera acima de 60 s nem de barras com estimativa errada.

#### 6.15.3 A árvore de decisão legível para o analista (`pos4-arvore-de-decisao`; 9 fontes com endereço)

*Leitura de:* subagente, em 07/11/2026; arquivo `base-C-arvore-de-decisao.md` em `5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/`.

Legenda de confiança: "aberta" = página aberta e lida nesta sessão; "snippet" = só resumo de busca; "memória" = dado bibliográfico que não consegui abrir.

##### a) Explicações contrastivas e "por que não"

**1. MILLER, Tim. Explanation in artificial intelligence: insights from the social sciences. Artificial Intelligence, v. 267, p. 1-38, 2019. Preprint: arXiv:1706.07269. Disponível em: https://arxiv.org/abs/1706.07269. Acesso em: 7 nov. 2026.**
- Estabelece (página do arXiv, aberta): a explicação em IA deve se apoiar em filosofia, psicologia e ciência cognitiva sobre como pessoas definem, selecionam, avaliam e apresentam explicações; pessoas trazem vieses e expectativas sociais, e boa parte da IA explicável usa só a intuição dos pesquisadores.
- Atenção: o resumo não cita "contrastiva" nem "por que não". Que as pessoas pedem explicações contrastivas ("por que P e não Q") vem do corpo do artigo, que não consegui abrir (403 no editor). Volume e páginas vêm da memória.
- No ponto: justifica que cada nó mostre a escolhida contra as alternativas descartadas, em vez de só "porque a causa é X".

**2. LIM, Brian Y.; DEY, Anind K. Assessing demand for intelligibility in context-aware applications. In: INTERNATIONAL CONFERENCE ON UBIQUITOUS COMPUTING (UbiComp), 11., 2009. Anais [...]. ACM, 2009. p. 195-204. Disponível em: https://dblp.uni-trier.de/rec/conf/huc/LimD09.html. Acesso em: 7 nov. 2026.**
- Estabelece (snippet de busca, não abri o texto): com cenários de quatro aplicações reais, dois experimentos medem que informação os usuários querem de sistemas opacos, e discutem por que pedem certos tipos e como oferecê-los. O resumo não diz qual tipo foi mais pedido.
- Fonte complementar, só bibliográfica (página aberta): LIM, B. Y.; DEY, A. K.; AVRAHAMI, D. Why and why not explanations improve the intelligibility of context-aware intelligent systems. In: CHI, 27., 2009. Proceedings [...]. ACM, 2009. p. 2119-2128. DOI 10.1145/1518701.1519023. Disponível em: https://bibtex.github.io/CHI-2009-LimDA.html. Acesso em: 7 nov. 2026. Pelo título, é o estudo que testa as explicações "por que" e "por que não"; não li o resumo.
- No ponto: sustenta oferecer "por que" e "por que não" como tipos de pergunta do analista, sem exibir o interior do sistema inteiro.

##### b) Fidelidade do raciocínio em texto

**3. TURPIN, Miles; MICHAEL, Julian; PEREZ, Ethan; BOWMAN, Samuel R. Language models don't always say what they think: unfaithful explanations in chain-of-thought prompting. In: NEURAL INFORMATION PROCESSING SYSTEMS (NeurIPS), 37., 2023. Disponível em: https://arxiv.org/abs/2305.04388. Acesso em: 7 nov. 2026.**
- Estabelece (aberta): a explicação em cadeia de pensamento pode deturpar sistematicamente a razão real da previsão. Ao inserir um viés (por exemplo, reordenar opções para a resposta ser sempre "A"), a resposta muda e o texto não menciona isso; o texto racionaliza a resposta errada, com queda de até 36% de acurácia em 13 tarefas (GPT-3.5 e Claude 1.0).
- No ponto: o raciocínio aberto do modelo não pode ser a justificativa de um nó.

**4. LANHAM, Tamera et al. Measuring faithfulness in chain-of-thought reasoning. Anthropic, 2023. arXiv:2307.13702. Disponível em: https://arxiv.org/abs/2307.13702. Acesso em: 7 nov. 2026.**
- Estabelece (aberta): a fidelidade varia por tarefa e tamanho do modelo; segundo o resumo, modelos maiores e mais capazes produzem raciocínio menos fiel na maioria das tarefas estudadas.
- No ponto: trocar de modelo ou de tamanho pode mudar o quanto o texto reflete o que ocorreu, mais um motivo para ancorar a árvore em sinais conferidos por código.

##### c) Visualização de trilhas de agentes

**5. LANGCHAIN. LangSmith: observability concepts. Disponível em: https://docs.langchain.com/langsmith/observability-concepts. Acesso em: 7 nov. 2026.**
- Mostra (aberta): um "run" é uma unidade de trabalho (chamada de modelo, ferramenta, busca), equivalente a um span do OpenTelemetry; um "trace" é a árvore de runs de uma operação, com entradas e saídas completas e aninhamento preservado. Latência, tokens e custo: a página não confirma.

**6. LANGFUSE. Data model. Disponível em: https://langfuse.com/docs/observability/data-model. Acesso em: 7 nov. 2026.**
- Mostra (aberta): trace é uma operação; observações (span, generation, event) são os passos individuais e podem ser aninhadas. Campos de entrada, saída, custo e latência não aparecem nessa página.
- Complemento (aberta): https://langfuse.com/docs/observability/features/agent-graphs descreve as abas Árvore, Linha do tempo e Grafo, com o grafo inferido de tempos e aninhamento (Acesso em: 7 nov. 2026).

**7. OPENTELEMETRY. Semantic conventions for generative AI. Disponível em: https://github.com/open-telemetry/semantic-conventions-genai. Acesso em: 7 nov. 2026.**
- Mostra (aberta): as convenções migraram para esse repositório e cobrem spans, métricas e eventos de clientes GenAI e MCP. As páginas antigas em opentelemetry.io/docs/specs/semconv/gen-ai/ só apontam para lá. Os nomes de span de agente (invoke_agent, execute_tool) não consegui confirmar abrindo páginas.
- No ponto (5 a 7): essas ferramentas servem ao desenvolvedor (árvore de chamadas, entradas, saídas), não ao analista de QA. Confirmam que o modelo de dados passo a passo da trilha é o padrão, mas a árvore de decisão exige uma camada própria de leitura.

##### d) Orientação para não especialistas

**8. AMERSHI, Saleema et al. Guidelines for human-AI interaction. In: CHI CONFERENCE ON HUMAN FACTORS IN COMPUTING SYSTEMS, 2019. Anais [...]. ACM, 2019. Disponível em: https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/. Acesso em: 7 nov. 2026.**
- Estabelece (página aberta): 18 diretrizes, validadas com 49 profissionais de design em 20 produtos; prêmio de menção honrosa no CHI 2019. O texto das diretrizes veio da biblioteca HAX (https://www.microsoft.com/en-us/haxtoolkit/library/, aberta): G1 "Make clear what the system can do"; G2 "Make clear how well the system can do what it can do" (ajudar a entender com que frequência pode errar); G11 "Make clear why the system did what it did" (acesso a uma explicação do comportamento).
- No ponto: G11 pede a explicação, G2 pede dizer a confiabilidade em linguagem comum (por exemplo, "esse tipo de diagnóstico costuma acertar X de 10"), sem jargão.

##### O que isso fixa para o desenho

Cada nó mostra: a pergunta do passo em linguagem do sistema (o que estava sendo decidido); a alternativa escolhida e as descartadas, cada uma com o motivo de "por que não" (fonte 1 e 2); a evidência concreta citada (campo, trecho de resposta, verbete) em termos do sistema do analista; e uma confiança em palavras ("alta", "média", "baixa") com a taxa histórica de acerto dessa faixa em frases comuns, sem k, logprob nem hit@3 (fonte 8, G2). O analista deve poder abrir a evidência e conferi-la sozinho.

Deve ser declarado como vindo de código: a poda, a busca dos verbetes, as alternativas e suas probabilidades, a conferência das evidências e a divergência entre o dito e o conferido, além do texto de justificativa, montado por molde a partir de sinais conferidos. Deve ser declarado como vindo do modelo: apenas a escolha do rótulo e o que ele citou. O raciocínio aberto, se for exibido, fica separado, rotulado como "texto do modelo, sem garantia de refletir o que ele fez" (fontes 3 e 4). Quando houver divergência entre o que o modelo disse e o que o código conferiu, o nó mostra isso de forma explícita, em vez de esconder.

##### O que não achei

Não abri o corpo de Miller (2019) nem o texto de Lim e Dey (2009), então o achado contrastivo e o ranking dos tipos de pergunta ("por que", "por que não") não foram conferidos por mim em página; o DOI do UbiComp 2009 não foi confirmado. Não confirmei custo e latência nas páginas de LangSmith e Langfuse, nem os nomes de span de agente do OpenTelemetry. Não encontrei fonte oficial dessas ferramentas voltada a usuários não técnicos. Também não achei estudo específico sobre árvores de decisão geradas por molde a partir de logs de agente de QA.

#### 6.15.4 Métricas de prolixidade e objetividade para os filtros determinísticos (`pos4-metricas-de-prolixidade`; 10 fontes com endereço)

*Leitura de:* subagente, em 07/11/2026; arquivo `base-D-metricas-de-prolixidade.md` em `5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/`.

Legenda de confiança: [ABERTA] = abri a página e li o trecho citado; [PARCIAL] = abri, mas só parte foi legível; [SECUNDÁRIA] = o número vem de um texto que cita a fonte.

##### a) Legibilidade em português

###### 1. Martins et al. (1996), adaptação do Flesch  [PARCIAL]

MARTINS, Teresa B. F.; GHIRALDELO, Claudete M.; NUNES, M. das Graças V.; OLIVEIRA JR., Osvaldo N. **Readability formulas applied to textbooks in Brazilian Portuguese**. São Carlos: ICMSC-USP, 1996. (Notas do ICMSC, n. 28). Disponível em: https://repositorio.usp.br/item/000906089. Acesso em: 7 nov. 2026.

- O PDF do repositório é imagem digitalizada, sem camada de texto: não consegui ler a fórmula nele. O que está confirmado é o resumo do repositório e as citações: 120 trechos de livros didáticos, quatro níveis de leitura que seguem as etapas do ensino brasileiro, e os escores de Flesch saem sistematicamente mais baixos em português do que em inglês (palavras com mais sílabas). Um texto que cita o trabalho diz que foram somados 42 pontos aos escores (206,835 + 42 = 248,835).
- Aplicação: é a única fonte primária da adaptação; a fórmula em si tem de vir de 2 (que a transcreve) e a conferência no original fica pendente de OCR.

###### 2. NILC-Metrix (Leal et al., 2023)  [ABERTA]

LEAL, Sidney Evaldo et al. **NILC-Metrix: assessing the complexity of written and spoken language in Brazilian Portuguese**. Language Resources and Evaluation, v. 58, 2023. DOI 10.1007/s10579-023-09693-w. Disponível em: https://arxiv.org/abs/2201.03445. Acesso em: 7 nov. 2026.

- Reúne 200 métricas de complexidade textual para o português do Brasil (código em github.com/nilc-nlp/nilcmetrix, AGPLv3). No texto do PDF, a fórmula adaptada vem escrita assim: **Flesch = 248,835 - 1,015 x (palavras por frase) - 84,6 x (sílabas por palavra)**. Traz também o índice Brunet-like de palavras desconhecidas: 0,1579 x (% de palavras fora do Dicionário de Palavras Simples, Biderman 1998) + 0,0496 x (palavras por frase) + 3,6365.
- Aplicação: dá a fórmula do Flesch em português e uma lista pronta de métricas (comprimento de frase, sílabas, palavras raras) que o filtro pode reproduzir em Python puro; a contagem de sílabas em português precisa de regra própria (separação silábica por vogais/ditongos), a testar contra o NILC-Metrix em amostra.

###### 3. Faixas do índice  [SECUNDÁRIA, duas fontes que não batem entre si]

- Dissertação PUC-Rio (Maxwell, arquivo 23892_7.PDF, capítulo 6), citando Martins et al. (1996): quatro faixas. 75 a 100 muito fácil (até a 4a série do fundamental); 50 a 75 fácil (até a 8a série); 25 a 50 difícil (ensino médio ou superior); 0 a 25 muito difícil (áreas acadêmicas específicas). Atenção: essa dissertação escreve a constante como 164,835, o que destoa de 248,835 do NILC; tratar como erro de transcrição dela. Disponível em: https://www.maxwell.vrac.puc-rio.br/23892/23892_7.PDF. Acesso em: 7 nov. 2026.
- RODRIGUES; NETO. Signo, Santa Cruz do Sul, v. 36, n. 60, p. 50-60, 2011, tabela da fórmula original de Flesch (206,835), com a tradução de Goldim (2003): 90-100 muito fácil, 80-90 fácil, 70-80 razoavelmente fácil, 60-70 padrão, 50-60 razoavelmente difícil, 40-50 difícil, 0-30 muito difícil. Essa tabela é da fórmula sem os 42 pontos, então não vale para a adaptada. Disponível em: https://seer.unisc.br/index.php/signo/article/view/1421/1607. Acesso em: 7 nov. 2026.
- Aplicação: para a fórmula adaptada, a referência é a tabela de quatro faixas; relatório para analista de QA deve ficar em 50 ou mais (nível "fácil"), o que é uma escolha nossa apoiada na faixa, não um valor da fonte. Flesch mede só frase e sílaba, a própria literatura chama de superficial; serve como alarme, não como nota.

##### b) Prolixidade e viés de tamanho em modelos

###### 4. Zheng et al. (2023), MT-Bench e Chatbot Arena  [ABERTA]

ZHENG, Lianmin et al. **Judging LLM-as-a-judge with MT-Bench and Chatbot Arena**. arXiv:2306.05685, 2023. Disponível em: https://arxiv.org/abs/2306.05685. Acesso em: 7 nov. 2026.

- Seção 3.3, ataque da "lista repetitiva": em 23 respostas com lista numerada, os autores inseriram no início uma cópia reescrita da lista, sem informação nova. O juiz falhou (preferiu a resposta inflada) em 91,3% dos casos com Claude-v1 e com GPT-3.5, e em 8,7% com GPT-4. Juízes com mais de 80% de concordância com humanos ainda caem em texto mais longo.
- Aplicação: justifica filtro determinístico de tamanho: um modelo julgando o próprio verbete não é confiável contra enchimento; a medida precisa vir de código.

###### 5. Dubois et al. (2024), AlpacaEval com controle de tamanho  [ABERTA]

DUBOIS, Yann; GALAMBOSI, Balázs; LIANG, Percy; HASHIMOTO, Tatsunori B. **Length-Controlled AlpacaEval: a simple way to debias automatic evaluators**. arXiv:2404.04475, 2024. Disponível em: https://arxiv.org/abs/2404.04475. Acesso em: 7 nov. 2026.

- Ajusta um modelo linear generalizado que prevê a preferência do juiz a partir da diferença de tamanho e de outros traços, e recalcula a preferência supondo diferença de tamanho zero. A correlação de Spearman com o Chatbot Arena sobe de 0,94 para 0,98.
- Aplicação: o tamanho é um confundidor medido em código; ao comparar verbetes, comparar a densidade (informação por palavra) e não o tamanho bruto, ou fixar o tamanho como covariável.

###### 6. Zhang, Das e Zhang (2024), compensação por verbosidade  [ABERTA]

ZHANG, Yusen; DAS, Sarkar Snigdha Sarathi; ZHANG, Rui. **Verbosity does not equal veracity: demystify verbosity compensation behavior of large language models**. arXiv:2411.07858, 2024 (v2). Disponível em: https://arxiv.org/abs/2411.07858. Acesso em: 7 nov. 2026.

- Define resposta verbosa como aquela que pode ser comprimida em menos tokens com o mesmo sentido (repete a pergunta, enumera demais, hesita). Em 14 modelos e 5 bases, a frequência é de 50,40% no GPT-4; na base Qasper, respostas verbosas e concisas diferem 27,61% em desempenho; um algoritmo em cascata baixou o Mistral de 63,81% para 16,16%. Verbosas têm mais incerteza. É preprint no arXiv (a versão em evento UncertaiNLP 2025 foi só vista na busca).
- Aplicação: sustenta duas medidas por código, a frequência (parcela de textos acima de um teto) e o achado de que texto verboso anda junto com incerteza do modelo, o que casa com o nó de diagnóstico.

###### 7. Adams et al. (2023), Chain of Density  [ABERTA]

ADAMS, Griffin et al. **From sparse to dense: GPT-4 summarization with Chain of Density prompting**. arXiv:2309.04269, 2023. Disponível em: https://arxiv.org/abs/2309.04269. Acesso em: 7 nov. 2026.

- Resumos "centrados em entidades", cada vez mais densos sem ficar mais longos; estudo de preferência humana em 100 artigos do CNN/DailyMail. A página aberta não define a densidade; no corpo do artigo ela é entidades por token, a conferir lendo o PDF.
- Aplicação: base para uma densidade calculável (entidades do domínio por palavra), com a lista fechada de nomes do projeto no lugar do reconhecedor de entidades.

##### c) Linguagem simples como norma

###### 8. Lei n. 15.263, de 14 de novembro de 2025  [ABERTA]

BRASIL. **Lei n. 15.263, de 14 de novembro de 2025**. Institui a Política Nacional de Linguagem Simples nos órgãos e entidades da administração pública. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15263.htm. Acesso em: 7 nov. 2026.

- Art. 4: linguagem simples é "conjunto de técnicas destinadas à transmissão clara e objetiva de informações". Art. 5: frases curtas e em ordem direta, voz ativa, evitar intercaladas, uma ideia por parágrafo, palavras comuns (jargão trocado ou explicado), nome completo antes da sigla, informação mais importante primeiro, listas e tabelas quando couber, evitar redundância, testar com o público-alvo.
- Aplicação: é a norma brasileira oficial e vale como lista de regras verificáveis em código (frase curta, sigla sem expansão, redundância); não traz número de palavras por frase, o limiar tem de vir de outra fonte.

###### 9. ISO 24495-1:2023, Plain language  [PARCIAL]

ISO. **ISO 24495-1:2023: Plain language, part 1: governing principles and guidelines**. Genebra: ISO, 2023. Disponível em: https://www.iso.org/standard/78907.html (a página da ISO devolveu 403; li a ficha em https://accessible-eu-centre.ec.europa.eu/content-corner/digital-library/iso-24495-12023-plain-language-part-1-governing-principles-and-guidelines_en). Acesso em: 7 nov. 2026.

- Publicada em 1 jun. 2023, 14 páginas, comitê ISO/TC 37. Vale para textos de qualquer língua escrita, com exemplos só em inglês, e cobre também redação técnica. Os princípios e diretrizes em si estão na parte paga; a ficha não os lista, e não vi número de palavras por frase.
- Aplicação: serve de ancoragem internacional para a regra "o leitor acha, entende e usa"; não fornece limiar.

##### d) Orientação para comentários e textos técnicos

###### 10. Google Python Style Guide, seção 3.8.5  [ABERTA]

GOOGLE. **Google Python Style Guide**: block and inline comments. Disponível em: https://google.github.io/styleguide/pyguide.html. Acesso em: 7 nov. 2026.

- Regra: comentar as partes complicadas ("se você vai ter de explicar na revisão de código, comente agora") e "nunca descreva o código", supondo que o leitor sabe Python melhor que você, mas não sabe o que você quer fazer.
- Aplicação: é a regra de estilo do projeto em uma linha; vira filtro de "frase que só repete o que o código/campo já mostra".

###### 11. Google Developer Documentation Style Guide, tom  [ABERTA]

GOOGLE. **Google developer documentation style guide: tone and content**. Disponível em: https://developers.google.com/style/tone. Acesso em: 7 nov. 2026.

- Regras: dizer a informação útil de forma direta; cortar marcadores vazios como "please note" e "at this time"; não chamar passo de "simples" ou "fácil"; palavras simples no lugar de jargão e metáfora; frases curtas; variar o início das frases.
- Aplicação: dá a lista de palavras de preenchimento e de adjetivos de enfeite (versão em português: "vale ressaltar", "neste momento", "simplesmente", "basicamente").

##### e) Métricas calculáveis sem modelo e de onde sai cada uma

| Métrica | Como calcular | Fonte |
|---|---|---|
| Palavras por frase (média e máximo) | contar palavras / frases | NILC-Metrix (2); Lei 15.263 art. 5 (frases curtas); Google tom (11) |
| Flesch adaptado | 248,835 - 1,015 x palavras/frase - 84,6 x sílabas/palavra | NILC-Metrix (2), Martins (1) |
| Taxa de compressão | palavras do texto / palavras do resumo que o conteúdo pede (ex.: número de campos que mudaram) | definição de verboso como "comprimível" em Zhang (6); a escolha do denominador é nossa |
| Razão de preenchimento | palavras da lista fechada de enchimento / palavras | Google tom (11); Zhang (6): repete pergunta, hesita |
| Repetição interna | trechos repetidos (n-gramas de 3 palavras que reaparecem) / total | ataque da lista repetitiva em Zheng (4) |
| Densidade | termos do domínio da lista fechada (campos, tabelas, códigos) / palavras | Adams (7), adaptado a lista fechada |
| Jargão por lista fechada | termos da lista do projeto sem expansão na primeira menção / termos | Lei 15.263 art. 5 (jargão trocado ou explicado, sigla com nome completo) |
| Tamanho absoluto em palavras | contagem; usar como covariável, não como nota | Dubois (5), Zheng (4) |

##### O que isso fixa para o desenho

Entram nos filtros, nesta ordem de confiança: (1) palavras por frase, com teto de 20 de média e 30 no máximo por frase (o teto vem do nosso corpus de comentários bons, medido por script, e não de uma fonte: nem a Lei 15.263 nem o ISO dão número; só a regra "frases curtas" está na lei); (2) Flesch adaptado de 50 ou mais, que é a fronteira entre "fácil" e "difícil" na tabela de quatro faixas de Martins citada pela dissertação da PUC-Rio, usado só como alarme porque a literatura chama o índice de superficial e as duas fontes secundárias divergem na constante; (3) razão de preenchimento por lista fechada, com a lista tirada das regras do guia do Google (11) e traduzida; limiar a calibrar como o percentil 95 do corpus de referência; (4) repetição interna, justificada pelo ataque da lista repetitiva (4), onde juízes caíram em 91,3% dos casos, e pelo conceito de verbosidade como "comprimível" (6); (5) taxa de compressão contra o resumo que o conteúdo pede, onde o denominador (campos que mudaram, rótulo, uma frase de causa) é decisão de desenho; (6) jargão e sigla sem expansão por lista fechada (Lei 15.263 art. 5). Como o tamanho infla a nota de qualquer juiz-modelo (4, 5), o tamanho em palavras entra nas tabelas como covariável e nunca como critério de aprovação; comparações entre verbetes usam densidade, não tamanho. A regra "nunca descreva o código" (10) vira a verificação de que a frase cita um fato do caso (campo, tabela, valor) e não repete o rótulo.

##### O que não achei

Não li a fórmula direto no original de Martins et al. (1996): o PDF é imagem sem texto, a fórmula veio do NILC-Metrix (2) e as faixas, de uma dissertação, que escreve a constante errada. Não achei nenhuma fonte primária com limiar numérico de palavras por frase para português (a Lei 15.263 e o ISO 24495-1 só dão a regra qualitativa; os princípios do ISO estão na parte paga). Não achei limiar publicado de razão de preenchimento nem de taxa de compressão: o que existe é a definição de verbosidade de Zhang (6), então esses dois limiares são calibração nossa e devem ser declarados assim. Não encontrei métrica de densidade de informação validada para o português; a de Adams (7) é para inglês e a definição exata no artigo não foi confirmada pela página do resumo. Não achei padrão ABNT de linguagem simples (só a lei federal e o ISO). Não confirmei o guia oficial de comentários para a regra de tamanho de docstring além da seção 3.8.5.

#### 6.15.5 Seleção de testes pelo diff do Git e a máquina virtual sugerida pelo orientador (`pos4-impacto-git-e-vm`; 16 fontes com endereço)

*Leitura de:* subagente, em 07/11/2026; arquivo `base-E-impacto-git-e-vm.md` em `5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/`.

Convenção: "aberta" = a página ou o PDF foi aberto e lido nesta pesquisa. "Resumo secundário" = só li um resumo de terceiros.

##### Ponto 1

###### 1.1 Rothermel e Harrold (1997) - aberta (PDF do artigo)

ROTHERMEL, G.; HARROLD, M. J. A safe, efficient regression test selection technique. **ACM Transactions on Software Engineering and Methodology**, v. 6, n. 2, p. 173-210, abr. 1997. DOI 10.1145/248233.248262. Disponível em: https://www.cs.purdue.edu/homes/xyzhang/spring07/Papers/p173-rothermel.pdf. Acesso em: 7 nov. 2026.

- Estabelece: prova que, sob certas condições, o conjunto selecionado inclui todo teste da suíte original capaz de expor falha no programa modificado (seleção "segura"); pode incluir testes que não expõem falha, mas é tão preciso quanto outros algoritmos seguros. Estudos empíricos iniciais indicam redução significativa do custo (o resumo não traz percentual).
- Aplicação: é a definição de "segura" para o desenho: na dúvida, selecionar a mais, nunca a menos. Nosso mapa arquivo-verbete é por convenção (frontmatter), não por prova, então a segurança aqui é só aproximada e precisa de um plano B.

###### 1.2 Yoo e Harman (2012) - resumo secundário

YOO, S.; HARMAN, M. Regression testing minimization, selection and prioritization: a survey. **Software Testing, Verification and Reliability**, v. 22, n. 2, p. 67-120, mar. 2012. DOI 10.1002/stvr.430. Disponível em: https://acawiki.org/Regression_testing_minimization,_selection_and_prioritization:_a_survey. Acesso em: 7 nov. 2026.

- Estabelece (segundo o resumo, não o artigo): separa três problemas, minimização, seleção e priorização. Na seleção lista abordagens por firewall em torno dos módulos modificados (conservadora), fluxo de dados, execução simbólica, fatias, grafo de dependência de controle e baseada em projeto. A tentativa de abrir o PDF do Chalmers deu timeout; os números (por exemplo a contagem de artigos) não foram conferidos.
- Aplicação: nossa ligação diff para verbete é uma seleção "baseada em modificação" de granularidade grossa (arquivo), da família do firewall, que o levantamento classifica como conservadora. Citar o artigo original só depois de conferir o PDF.

###### 1.3 Gligoric, Eloussi e Marinov (2015), Ekstazi - aberta (resumo no site do autor)

GLIGORIC, M.; ELOUSSI, L.; MARINOV, D. Practical regression test selection with dynamic file dependencies. In: INTERNATIONAL SYMPOSIUM ON SOFTWARE TESTING AND ANALYSIS (ISSTA), 2015, Baltimore. **Proceedings** [...]. New York: ACM, 2015. DOI 10.1145/2771783.2771784. Disponível em: https://users.ece.utexas.edu/~gligoric/papers/abstracts/GligoricETAL15Ekstazi.txt. Acesso em: 7 nov. 2026.

- Estabelece: o Ekstazi liga cada teste aos arquivos de que ele depende (dependência dinâmica, em nível de arquivo) e não exige integração com controle de versão. Em 615 revisões de 32 projetos (cerca de 5 milhões de linhas), cortou o tempo total de teste em 32% em média e 54% nas suítes mais longas. Terminou mais rápido que outras técnicas mesmo selecionando mais testes. Adotado por Apache Camel, Commons Math e CXF.
- Aplicação: dá respaldo à granularidade de arquivo, que é a nossa. A diferença é que o Ekstazi mede a dependência rodando os testes, e nós declaramos a dependência à mão no frontmatter (`arquivos:`, `endpoints:`). Isso é mais barato e mais sujeito a ficar desatualizado.

###### 1.4 Azure DevOps Test Impact Analysis - aberta

MICROSOFT. Use Test Impact Analysis. **Microsoft Learn**, Azure Pipelines. Disponível em: https://learn.microsoft.com/en-us/azure/devops/pipelines/test/test-impact-analysis. Acesso em: 7 nov. 2026.

- Estabelece: o TIA seleciona os testes impactados por um commit, mais os que falharam antes e os novos. Tem "fallback seguro": para commits que não entende, roda tudo (exemplo da página: alteração em HTML ou CSS). Ao ver tipo de arquivo desconhecido, roda tudo. Permite rodar tudo em periodicidade configurada (recomendado) e aceita um mapa de dependências escrito à mão, em XML versionado no repositório (variável `TIA.UserMapFile`), que "pode até ser aproximado". Cobre código gerenciado e máquina única. Para validar, sugere rodar os selecionados (T1) e depois todos (T2) e comparar as falhas.
- Aplicação: é a prática de mercado quase idêntica ao desenho: mapa declarado à mão, aproximado, e com rede de segurança. Fixa três regras: arquivo fora do mapa roda tudo, rodada completa periódica, e comparar seleção contra rodada completa para medir o que a seleção perdeu.

###### 1.5 Memon et al. (2017), Google - aberta (PDF)

MEMON, A. et al. Taming Google-scale continuous testing. In: INTERNATIONAL CONFERENCE ON SOFTWARE ENGINEERING: SOFTWARE ENGINEERING IN PRACTICE TRACK (ICSE-SEIP), 39., 2017, Buenos Aires. **Proceedings** [...]. Piscataway: IEEE, 2017. p. 233-242. DOI 10.1109/ICSE-SEIP.2017.16. Disponível em: https://huang.isis.vanderbilt.edu/cs4278/readings/googletest.pdf. Acesso em: 7 nov. 2026.

- Estabelece: no TAP do Google, a seleção base é por dependência reversa: regras de build montam a estrutura que devolve todos os alvos de teste que dependem, direta ou indiretamente, dos arquivos modificados (chamados AFFECTED). Marcos chegam a 4,2 milhões de testes assim selecionados. Por dia: mais de 13 mil projetos, 800 mil builds, 150 milhões de execuções de teste. Em média por mudança, menos de 0,5% dos alvos falham, 43% ficam AFFECTED sem rodar e 7,4% são pulados.
- Aplicação: confirma que "arquivo alterado, alvos que dependem dele" é a base também nas grandes empresas, e que a maioria dos testes afetados passa. Aqui o mapa vem do build; o nosso vem do frontmatter.

###### 1.6 Machalica et al. (2019), Facebook - aberta (resumo no arXiv)

MACHALICA, M. et al. Predictive test selection. In: INTERNATIONAL CONFERENCE ON SOFTWARE ENGINEERING: SOFTWARE ENGINEERING IN PRACTICE (ICSE-SEIP), 41., 2019, Montreal. **Proceedings** [...]. IEEE, 2019. arXiv:1810.05286. Disponível em: https://arxiv.org/abs/1810.05286. Acesso em: 7 nov. 2026.

- Estabelece: o Facebook já fazia teste baseado em mudança (rodar tudo que pode ser afetado) e achou inviável. Um modelo simples treinado no histórico de resultados escolhe um subconjunto: corta cerca de metade do custo de infraestrutura de teste, mantendo mais de 95% das falhas individuais e mais de 99,9% das mudanças defeituosas reportadas. Trata testes instáveis. A página do arXiv não cita o evento; o ICSE-SEIP 2019 vem do programa da conferência (resultado de busca).
- Aplicação: é a alternativa que não vamos usar (precisa de histórico grande). Serve para dizer que a seleção por dependência é o patamar de partida e que o ganho adicional vem de aprendizado sobre histórico, fora do escopo do TCC.

###### O que isso fixa para o desenho

A literatura e a prática sustentam três pontos: (1) selecionar testes pelos arquivos que mudaram no diff, em granularidade de arquivo, é técnica estabelecida (Ekstazi: 32% a 54% menos tempo; Google: dependência reversa de arquivos alterados); (2) o mapa pode ser declarado à mão e aproximado, como o `TIA.UserMapFile` do Azure; (3) a seleção só é aceitável com rede de segurança: arquivo desconhecido ou fora do mapa dispara a bateria inteira, há rodada completa periódica, e a seleção é validada contra a rodada completa (T1 contra T2 do Azure; "segura" em Rothermel e Harrold). Para o agente: diff sem nenhum verbete ligado deve rodar tudo, não nada; registrar a cada rodada o que a seleção deixou de rodar; reconstruir o mapa quando o verbete mudar.

###### O que não achei

- Texto do Yoo e Harman aberto (só resumo de terceiros) e números de Rothermel e Harrold (o resumo não os traz; não percorri a seção empírica).
- Documentação do Azure sobre taxa de falsos negativos da seleção.
- Qualquer trabalho que ligue diff a documentação em linguagem natural (verbetes) para selecionar teste. A literatura liga diff a código, cobertura ou dependência de build; a ponte por documentação é nossa e não tem respaldo direto. A busca foi limitada a algumas consultas.
- Taxa de erro de mapas escritos à mão (desatualização). O Azure só diz que o mapa pode ser aproximado.

##### Ponto 2

###### 2.1 Microsoft, WSL: configuração avançada - aberta

MICROSOFT. Advanced settings configuration in WSL. **Microsoft Learn**, 16 out. 2026. Disponível em: https://learn.microsoft.com/en-us/windows/wsl/wsl-config. Acesso em: 7 nov. 2026.

- Estabelece: a VM do WSL 2 recebe por padrão 50% da memória do Windows e o mesmo número de processadores lógicos; swap padrão de 25% da memória, arredondado para cima em GB. Os limites mudam em `%UserProfile%\.wslconfig` (`memory`, `processors`, `swap`), que não exige administrador no arquivo; exige `wsl --shutdown` para valer.
- Aplicação: com 16 GB instalados (o Windows enxerga 15,69), o padrão dá cerca de 8 GB à VM. O qwen2.5:7b quantizado mais o contexto e o resto do sistema ficam apertados; seria preciso subir `memory` à mão, tirando RAM do navegador de teste, do PHP e do MariaDB que rodam no host.

###### 2.2 Microsoft, comparando WSL 1 e 2 - aberta

MICROSOFT. Comparing WSL versions. **Microsoft Learn**. Disponível em: https://learn.microsoft.com/en-us/windows/wsl/compare-versions. Acesso em: 7 nov. 2026.

- Estabelece: o WSL 2 roda um kernel Linux numa "VM utilitária leve" gerenciada, com "pegada de recursos pequena" frente às VMs tradicionais. A memória cresce e encolhe com o uso, mas as páginas em cache não voltam ao Windows até o WSL ser desligado; a página recomenda WSL 1 a quem tem requisitos estritos de memória. Não traz percentual de desempenho em carga de CPU.
- Aplicação: serve para dizer que o custo do WSL 2 em memória é o risco (o cache do modelo de vários GB fica retido), não a CPU. Sem número oficial de sobrecarga de CPU.

###### 2.3 Microsoft, instalar o WSL - aberta

MICROSOFT. Install WSL. **Microsoft Learn**. Disponível em: https://learn.microsoft.com/en-us/windows/wsl/install. Acesso em: 7 nov. 2026.

- Estabelece: o comando `wsl --install` deve ser rodado com o PowerShell aberto "em modo administrador", e depois reinicia-se a máquina; ele habilita os recursos do Windows necessários.
- Aplicação: no Windows 11 corporativo sem administrador o WSL 2 não se instala por conta própria; depende do TI. Isso vale também para quem já tem o recurso habilitado por política: aí só falta a distribuição.

###### 2.4 Microsoft, FAQ do WSL - aberta

MICROSOFT. FAQ's about Windows Subsystem for Linux. **Microsoft Learn**. Disponível em: https://learn.microsoft.com/en-us/windows/wsl/faq. Acesso em: 7 nov. 2026.

- Estabelece: o WSL 2 usa um subconjunto do Hyper-V (componente "Virtual Machine Platform"), disponível em todas as edições de desktop, inclusive Home; dá erro 0x800704ec quando política de grupo bloqueia o WSL ("contate o administrador"); o WSL foi desenhado para ciclo de desenvolvimento interno, e a VM desliga sozinha quando não há uso.
- Aplicação: política de grupo corporativa pode bloquear o WSL mesmo com a máquina capaz. Para uma bateria de várias horas, o desligamento automático da VM também precisa ser desligado (`vmIdleTimeout`, `instanceIdleTimeout` em 2.1).

###### 2.5 Microsoft, requisitos do Hyper-V - aberta

MICROSOFT. System requirements for Hyper-V on Windows and Windows Server. **Microsoft Learn**. Disponível em: https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-requirements. Acesso em: 7 nov. 2026.

- Estabelece: o Hyper-V só liga em Windows 10 ou 11 Professional ou Enterprise; exige processador 64 bits com SLAT, virtualização ligada no BIOS ou UEFI e "ao menos 4 GB de RAM, quanto mais melhor", suficiente para o host e todas as VMs ao mesmo tempo. A página não diz explicitamente que ativar exige administrador (a página de ativação deu 404).
- Aplicação: a exigência de administrador para Hyper-V não foi confirmada na fonte oficial; o recurso do Windows é opcional e na prática vem de quem tem direito de administrador, mas isso é inferência. Nesta máquina o que decide é a edição do Windows e a política do TI.

###### 2.6 Docker, instalação no Windows - aberta

DOCKER. Install Docker Desktop on Windows. **Docker Docs**. Disponível em: https://docs.docker.com/desktop/setup/install/windows-install/. Acesso em: 7 nov. 2026.

- Estabelece: instalação por usuário (padrão) não exige administrador para instalar ou atualizar, mas habilitar o WSL 2 pela primeira vez exige, uma vez por máquina. O backend Hyper-V só existe na instalação para todos os usuários, que exige administrador. Requisitos: Windows 10 22H2 ou 11 23H2 em Pro, Enterprise ou Education; processador 64 bits com SLAT, 8 GB de RAM, virtualização ligada. Não serve para Windows Server.
- Aplicação: Docker Desktop sem administrador só se a TI já tiver habilitado o WSL 2 na máquina. O mínimo oficial de 8 GB de RAM é antes de qualquer modelo: o host de 16 GB mal comporta Docker, WSL 2, modelo de 7B e a bateria de testes juntos.

###### 2.7 Ollama no Docker - aberta

OLLAMA. Docker. **Ollama Docs**. Disponível em: https://docs.ollama.com/docker. Acesso em: 7 nov. 2026.

- Estabelece: o comando para CPU é `docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama`, sem nenhuma flag de GPU. GPU em contêiner exige NVIDIA Container Toolkit e `--gpus=all` (NVIDIA) ou imagem `rocm` e dispositivos `/dev/kfd` e `/dev/dri` (AMD). Não traz medição nem aviso de desempenho em CPU.
- Aplicação: rodar em contêiner sem GPU é suportado, mas a documentação não quantifica o custo. Aqui não há GPU, então o contêiner não perde aceleração (já não há).

###### 2.8 Ollama no Windows e FAQ - abertas

OLLAMA. Windows. **Ollama Docs**. Disponível em: https://docs.ollama.com/windows. Acesso em: 7 nov. 2026.

OLLAMA. FAQ. **Ollama Docs**. Disponível em: https://docs.ollama.com/faq. Acesso em: 7 nov. 2026.

- Estabelece: "A instalação do Ollama não exige Administrador" e vai para o diretório do usuário por padrão; exige Windows 10 22H2 ou superior; a página não fala de RAM nem de CPU. O FAQ diz que "100% CPU" no `ollama ps` significa modelo carregado inteiro em memória do sistema, que a RAM necessária cresce com `OLLAMA_NUM_PARALLEL` vezes `OLLAMA_CONTEXT_LENGTH` e que o padrão de modelos carregados é 3 para CPU. A aceleração por GPU em contêiner vale em Linux ou Windows com WSL 2.
- Aplicação: o caminho nativo atual (Ollama sem administrador, CPU) é o único documentado como possível sem o TI. Cada camada de virtualização acrescentada exige direitos que a máquina não tem. O limite de modelos simultâneos e de paralelismo já controla a memória sem VM.

###### 2.9 SiSoftware: desempenho do Hyper-V - aberta (medição de terceiros, não revisada por pares)

SISOFTWARE. Performance impact of Hyper-V virtualisation (Windows 10 Pro) - Compute. Disponível em: https://www.sisoftware.co.uk/?p=2773. Acesso em: 7 nov. 2026.

- Estabelece: num i9-7900X (10 núcleos, 20 threads), Windows 10 em VM Hyper-V com 20 vCPUs e 24 GB (host com 32 GB) ficou entre 3% e 9% mais lenta que o nativo em cargas SIMD e cerca de 10% mais lenta em inteiros (Dhrystone Integer -11%, Long -13%), com extremos de -15% a -23% (redes neurais recorrentes na inferência -13% a -15%, Black-Scholes -18% a -20%). Inferência de redes convolucionais ficou em cerca de -7%. Operações de memória (criptografia) variaram pouco, e o artigo não mede largura de banda de memória.
- Aplicação: é a melhor ordem de grandeza achada para carga de CPU: a VM custa na faixa de 5% a 15%, com cauda ruim. É dado de outro processador, outro sistema e outro tipo de carga, sem LLM; serve só como indicativo, não como previsão para o i5-1235U.

###### O que isso fixa para o desenho

Uma VM nesta máquina não é viável hoje, e o motivo principal é de permissão e de memória, não de CPU. Permissão: WSL 2, Hyper-V e Docker Desktop com backend Hyper-V pedem administrador (WSL e Docker na primeira habilitação do WSL 2; Hyper-V pelo conjunto de requisitos e só nas edições Pro e Enterprise); só o Ollama nativo, que o Ollama diz não exigir administrador, roda sem o TI. Memória: o padrão do WSL 2 é 50% da RAM (cerca de 8 GB), o Docker pede 8 GB de mínimo, e a VM mantém cache de páginas sem devolver ao Windows até desligar; com 16 GB e o modelo de 7B mais navegador, PHP e MariaDB no host, sobra pouco. CPU: a sobrecarga medida de VM em carga de CPU é da ordem de 5% a 15%, tolerável, então não é o fator decisivo. Resposta ao orientador, em linguagem de decisão: "viável só num servidor", onde alguém com administrador já mantém a virtualização e a RAM fica dedicada; na máquina do dev de QA, a execução nativa permanece.

###### O que não achei

- Medição publicada de inferência de LLM (llama.cpp ou Ollama) em CPU, em VM ou contêiner contra nativo, no Windows. A busca só trouxe blogs sem método; o único número de VM contra nativo para LLM era de Mac com GPU, sem relação com este caso.
- Orientação oficial do Ollama sobre desempenho em VM ou contêiner sem GPU; a documentação só ensina a rodar.
- Medição oficial da Microsoft de sobrecarga de CPU do WSL 2 ou do Hyper-V (o que achei foi a medição de terceiros em 2.9).
- Confirmação oficial de que habilitar o Hyper-V exige administrador (a página de ativação deu 404; a de requisitos não afirma). Para o WSL 2 e o Docker a exigência está confirmada em 2.3 e 2.6.
- Largura de banda de memória em VM, que é o gargalo da inferência em CPU. O artigo de 2.9 remete a um artigo separado que não abri.
- A política real do TI da empresa (se o WSL está bloqueado por política de grupo). Só o administrador sabe.

#### 6.15.6 O projeto contra o syllabus CTFL 4.0 do ISTQB, na tradução do BSTQB (`pos4-syllabus-ctfl`; 1 fonte com endereço)

*Leitura de:* Claude, na sessão principal, em 07/11/2026; arquivo `istqb-ctfl-4.0-validacao.md` em `5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/`.

Leitura feita em 7 nov. 2026 pelo Claude, na sessão principal, sobre o PDF que o orientador subiu em 06/11/2026 ao repositório da disciplina (`TCC/syllabus_ctfl_4.0br.pdf`, commit `f469ecd`). O texto foi extraído com PyMuPDF; as páginas citadas são as do rodapé do PDF ("Página N de 66"), localizadas por busca da frase citada no texto extraído. Nas citações, a hifenização de quebra de linha do PDF foi desfeita e nada mais mudou; dois deslizes da tradução ("Uma equívoco", "Os Teste de Regressão") ficam como estão na fonte. O documento é a versão 4.0 do syllabus, com data de lançamento 21/04/2023 em todas as páginas, na tradução do BSTQB revisada em 29/02/2024 (correção de erros gramaticais), 28/06/2024 (adequação visual) e 06/01/2025 (adequação ao novo padrão visual do ISTQB), segundo o histórico da página 3.

Referência: ISTQB. **Certified Tester Foundation Level (CTFL) Syllabus**: versão 4.0. Tradução: BSTQB. [S. l.]: International Software Testing Qualifications Board, 2023. 66 p. Versão de lançamento de 21 abr. 2023; tradução revisada em 6 jan. 2025. Disponível em: https://bstqb.qa/. Acesso em: 7 nov. 2026. (Em 7 nov. 2026 o endereço antigo `bstqb.org.br/b9/sobre-ctfl`, que a comunidade cita como a página de download, redirecionava para `bstqb.qa`, cuja página inicial não traz o link do PDF; conferir a página de download antes da versão final do TCC. O original em inglês, versão 4.0.1 de 2024, está no site do ISTQB em `www.istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf`, endereço visto só em resultado de busca e não aberto nesta leitura.)

##### 1 As perguntas do Eric

Duas: o projeto está dentro dos parâmetros e dos métodos do syllabus? E é de fato teste de ponta a ponta (E2E)? Depois: o que o syllabus pede e o projeto não tem, para entrar; e como citar o documento no TCC.

##### 2 O que o syllabus diz, seção a seção

###### 2.1 O que é teste, e teste contra depuração (seção 1.1, p. 14 e 15)

"O teste de software é um conjunto de atividades para descobrir defeitos e avaliar a qualidade dos artefatos de software. Esses artefatos, quando estão sendo testados, são conhecidos como objetos de teste." O syllabus avisa contra a ideia de que testar "consistem apenas na execução de testes (ou seja, executar o software e verificar os resultados dos testes)" e separa verificação de validação: "verificar se o sistema atende aos requisitos especificados" e "checar se o sistema atende às necessidades dos usuários". O objetivo de aprendizagem FL-1.1.2 é "Diferenciar teste de depuração" (p. 13), e a seção 1.1.2 diz: "O teste e a depuração são atividades distintas." e "Quando o teste dinâmico (ver capítulo 4) aciona uma falha, a depuração se preocupa em encontrar as causas dessa falha (defeitos), analisar essas causas e eliminá-las." O processo de depuração descrito é "Reproduzir uma falha", "Diagnosticar (encontrar a causa principal)" e "Corrigir a causa", e "O teste de confirmação subsequente verifica se as correções resolveram o problema." (p. 15).

No projeto: o agente roda os roteiros e compara o que vê com o contrato e com a referência em modo normal (verificação); não valida necessidades de usuário. O diagnóstico do agente (a causa entre as 23 da taxonomia) é a etapa "Diagnosticar" da depuração, feita em apoio a quem corrige; a cura de localizador é "Corrigir a causa" só no testware; e a reexecução depois da cura é o teste de confirmação. O TCC deve dizer isso com essas palavras: o agente testa e apoia a depuração.

###### 2.2 Erro, defeito, falha e causa-raiz (seção 1.2.3, p. 16)

"Se um defeito no código for executado, o sistema poderá deixar de fazer o que deveria fazer ou fazer algo que não deveria, causando uma falha." E: "Uma causa-raiz é um motivo fundamental para a ocorrência de um problema (p. ex., uma situação que leva a um erro). As causas-raiz são identificadas por meio da análise de causa-raiz, que normalmente é realizada quando ocorre uma falha ou quando um defeito é identificado."

No projeto: o agente observa a falha na tela, localiza o defeito na resposta da API (o desvio do contrato ou da referência) e nomeia uma causa entre 23 categorias. A "causa raiz" do projeto é mais estreita que a do syllabus: é a categoria do defeito observado, não o motivo fundamental (que pode ser humano ou de processo). O TCC passa a usar os três termos no sentido do syllabus e declara essa diferença no glossário.

###### 2.3 Os sete princípios (seção 1.3, p. 16)

"O teste mostra a presença, não a ausência de defeitos. Os testes podem mostrar que os defeitos estão presentes no objeto de teste, mas não podem provar que não há defeitos (Buxton 1970)." e "Testes exaustivos são impossíveis. Testar tudo não é viável, exceto em casos triviais (Manna 1978)."

No projeto: o relatório por caso diz o que o agente encontrou e nunca que "não há defeitos"; os dez cenários da Fase 5 e os 72 casos de avaliação são uma amostra, e o TCC já declara isso como limitação.

###### 2.4 Atividades de teste: execução, comparação, registro e análise das anomalias (seção 1.4.1, p. 17)

"A Execução do Teste inclui a execução dos testes de acordo com o cronograma de execução ("rodar" o teste). A execução do teste pode ser manual ou automatizada." e "Os resultados reais dos testes são comparados com os resultados esperados. Os resultados do teste são registrados. As anomalias são analisadas para identificar suas causas prováveis. Essa análise nos permite relatar as anomalias com base nas falhas observadas (ver seção 5.5)."

No projeto: é o laço do agente, na ordem do syllabus: rodar o roteiro (Playwright), comparar o real com o esperado (contrato e referência em modo normal), registrar (a trilha v2), analisar as causas prováveis (o diagnóstico, com a causa escolhida e as alternativas) e relatar (o relatório por caso, que a seção 5.5 molda).

###### 2.5 Testware (seção 1.4.3, p. 18)

"O testware é criado como produto de trabalho de saída das atividades de teste descritas na seção 1.4.1."

No projeto: roteiros, localizadores, cenários, contratos, a biblioteca de verbetes e a trilha são testware. A cura de localizador (Fase 4, pacote P4) é manutenção automatizada do testware: quando o localizador de um passo quebra, o código acha outro e o roteiro passa de novo.

###### 2.6 Níveis de teste (seção 2.2.1, p. 26)

"O Teste de Sistema concentra-se no comportamento geral e nos recursos de todo um sistema ou produto, geralmente incluindo o teste funcional de tarefas de ponta a ponta e o teste não funcional de características de qualidade." e "O Teste de Integração de Sistema concentra-se no teste das interfaces do sistema e de outros sistemas e serviços externos. O teste de integração do sistema requer ambientes de teste adequados, de preferência semelhantes ao ambiente operacional."

No projeto: "E2E" não é um nível de teste no syllabus; "tarefas de ponta a ponta" é o conteúdo funcional do Teste de Sistema. O agente percorre a tarefa inteira (abrir a página, listar, abrir o detalhe, entrar, reservar), do front PHP, pela API, até o banco, e a fronteira entre o front e a API é o objeto que ele mais examina: nível de sistema, com conteúdo de integração de sistema (duas aplicações e o banco). O ambiente é o das cobaias reais, levantado nesta máquina.

###### 2.7 Tipos de teste (seção 2.2.2, p. 27)

"O Teste Caixa-Preta (ver seção 4.2) é baseado em especificações e deriva testes da documentação externa ao objeto de teste. O principal objetivo do teste caixa-preta é verificar o comportamento do sistema em relação às suas especificações." E sobre os não funcionais: "Muitos testes não funcionais são derivados de testes funcionais, pois usam os mesmos testes funcionais, mas verificam se, ao executar a função, uma restrição não funcional é atendida (p. ex., verificar se uma função é executada dentro de um tempo especificado ou se uma função pode ser portada para uma nova plataforma)."

No projeto: os contratos (esquemas da API) são a especificação, e o agente não lê o código das cobaias: teste funcional, caixa-preta. O sinal "tempo acima do orçamento" do caso ao vivo é um teste não funcional derivado do funcional, exatamente como o exemplo do syllabus.

###### 2.8 Teste de confirmação, teste de regressão e análise de impacto (seções 2.2.3 e 2.3, p. 28)

"Os Teste de Regressão confirmam que nenhuma consequência adversa foi causada por uma alteração, inclusive uma correção que já tenha sido confirmada após o teste." e "É aconselhável realizar primeiro uma análise de impacto para otimizar a extensão do teste de regressão. A análise de impacto mostra quais partes do software podem ser afetadas." e "os testes de regressão são fortes candidatos à automação. A automação desses testes deve começar no início do projeto." Na manutenção (2.3): "A análise de impacto pode ser feita antes de uma alteração, para ajudar a decidir se a alteração deve ser feita, com base nas possíveis consequências em outras áreas do sistema."

No projeto: os cenários da Fase 5 são testes de regressão automatizados sobre as cobaias; a reexecução depois da cura é teste de confirmação; e a integração com o Git (pacote Q7 do plano da Pós-Fase 4) é a análise de impacto que o syllabus manda fazer antes da regressão: o diff do commit, cruzado com os arquivos e endpoints declarados nos verbetes, diz que cenários rodar.

###### 2.9 Pirâmide e quadrantes de teste (seções 5.1.6 e 5.1.7, p. 45)

"A camada superior representa testes complexos, de alto nível e de ponta a ponta. Esses testes de alto nível geralmente são mais lentos do que os testes das camadas inferiores e, normalmente, verificam uma grande parte da funcionalidade, de modo que, em geral, são necessários apenas alguns deles para obter uma cobertura razoável." e "Outro modelo popular define testes de unidade (componente), testes de integração (integração de componente) e testes de ponta a ponta." Sobre os quadrantes: "Os quadrantes de teste, definidos por Brian Marick (Marick 2003, Crispin 2008), agrupam os níveis de teste com os tipos de teste, as atividades, as técnicas de teste e os produtos de trabalho apropriados no desenvolvimento ágil de software."

No projeto: o agente está no topo da pirâmide: poucos testes (dez cenários), lentos (minutos por cenário, com o modelo em CPU), cobertura larga (a tarefa inteira). É isso que explica, no TCC, por que o número de cenários é pequeno e por que o tempo até o resultado se mede em minutos; e é a segunda passagem do syllabus em que "ponta a ponta" nomeia o que o agente faz.

###### 2.10 Relatório de defeitos (seção 5.5, p. 50 e 51)

"Um relatório de defeitos registrado durante um teste dinâmico normalmente possui: Um identificador exclusivo; Um título com um breve resumo da anomalia que está sendo relatada; A data em que a anomalia foi observada, a organização emissora e o autor, incluindo seu cargo; A identificação do objeto de teste e do ambiente de teste; O contexto do defeito (p. ex., caso de teste que está sendo executado, atividade de teste que está sendo realizada, fase do SDLC e outras informações relevantes, como a técnica de teste, a lista de verificação ou os dados de teste que estão sendo usados); A descrição da falha para permitir a reprodução e a resolução, incluindo as etapas que detectaram a anomalia e todos os registros de teste relevantes, despejos de banco de dados, capturas de tela ou gravações; Os resultados esperados e os resultados reais; A severidade do defeito (grau de impacto) nos interesses dos stakeholders ou nos requisitos; A prioridade de correção; O status do defeito (p. ex., aberto, adiado, duplicado, aguardando correção, aguardando teste de confirmação, reaberto, fechado, rejeitado); As referências (p. ex., ao caso de teste)." E: "Alguns desses dados podem ser incluídos automaticamente ao usar ferramentas de gerenciamento de defeitos (p. ex., identificador, data, autor e status inicial). Modelos de documentos para um relatório de defeitos e exemplos de relatórios de defeitos podem ser encontrados na norma ISO/IEC/IEEE 29119-3".

No projeto: o relatório v2 por caso tem seis seções fixas (veredito, evidência, contraste com a segunda causa, FONTE declarada e conferida, linha de ação, árvore) e não tem metade desses campos. É o que a decisão 104 adota como esqueleto do relatório v3 (tabela na seção 4).

###### 2.11 Ferramentas e os riscos da automação (seções 6.1 e 6.2, p. 53 e 54)

Entre as ferramentas da 6.1: "Ferramentas de gerenciamento: aumentam a eficiência do processo de teste, facilitando o gerenciamento do SDLC, dos requisitos, dos testes, dos defeitos e da configuração" e "Ferramentas de execução e cobertura de testes: facilitam a execução de testes automatizados e a medição da cobertura". Entre os riscos da 6.2: "Expectativas irreais sobre os benefícios de uma ferramenta (incluindo funcionalidade e facilidade de uso)"; "Estimativas imprecisas de tempo, custos e esforço necessários para introduzir uma ferramenta, manter scripts de teste e alterar o processo de teste manual existente"; "Usar uma ferramenta de teste quando o teste manual é mais apropriado"; "Confiar demais em uma ferramenta, por exemplo, ignorando a necessidade do pensamento crítico humano"; e "Usar um software de código aberto que pode ser abandonado".

No projeto: o agente é uma ferramenta de execução (roda os roteiros) e de gerenciamento de defeitos (produz o relatório). Dos riscos, três já têm resposta no desenho: manter scripts de teste é o que a cura de localizador ataca; "confiar demais em uma ferramenta" é o motivo do princípio "a IA nunca aprova sozinha" e da revisão humana (decisão 95); e a dependência de código aberto (Ollama, Playwright, qwen2.5:7b) fica declarada no TCC com as versões fixadas. A Fase 5 responde ao risco das "estimativas imprecisas" medindo o tempo do agente contra a linha de base manual.

##### 3 Onde o projeto cabe

| Dimensão do syllabus | O projeto | Seção e página |
|---|---|---|
| Nível de teste | sistema e integração de sistema: front PHP, API e banco, com a fronteira front e API como objeto principal | 2.2.1, p. 26 |
| Conteúdo | tarefas de ponta a ponta: abrir a página, listar, abrir o detalhe, entrar, reservar | 2.2.1, p. 26; 5.1.6, p. 45 |
| Tipo | funcional, caixa-preta, baseado em especificação (os contratos); o tempo acima do orçamento é um teste não funcional derivado do funcional | 2.2.2, p. 27 |
| Confirmação e regressão | reexecução depois da cura (confirmação); cenários da Fase 5 (regressão automatizada); análise de impacto pelo Git antes da regressão | 2.2.3 e 2.3, p. 28 |
| Atividades | executar, comparar o real com o esperado, registrar (trilha), analisar as causas prováveis (diagnóstico), relatar (relatório) | 1.4.1, p. 17 |
| Testware e manutenção | roteiros, localizadores, contratos, biblioteca de verbetes, trilha; a cura é manutenção automatizada do testware | 1.4.3, p. 18 |
| Teste contra depuração | o agente testa e apoia a depuração: diagnostica a causa, corrige só o testware | 1.1, p. 14 e 15 |
| Pirâmide | topo: poucos testes, lentos, cobertura larga | 5.1.6, p. 45 |
| Ferramenta | execução e gerenciamento de defeitos; os riscos da 6.2 têm resposta no desenho | 6.1 e 6.2, p. 53 e 54 |
| Relatório de defeitos | campos da 5.5 adotados como esqueleto do relatório v3 (decisão 104) | 5.5, p. 50 e 51 |

Resposta às duas perguntas. Dentro dos parâmetros: sim. O agente faz o que o syllabus descreve como execução de teste dinâmico, funcional, caixa-preta, automatizado, de regressão e de confirmação, com análise das anomalias e relato; o que ele faz a mais (diagnosticar a causa e curar o localizador) é apoio à depuração e manutenção do testware, que o syllabus também descreve. Ponta a ponta: sim, com uma precisão. O syllabus não define "E2E" como nível; "ponta a ponta" nomeia as tarefas testadas no nível de sistema e a camada de cima da pirâmide. O nome "agente de QA de ponta a ponta" se sustenta quando o TCC diz que o nível é teste de sistema e de integração de sistema.

##### 4 O que o syllabus pede e o projeto não tinha

1. O relatório de defeitos da seção 5.5 como esqueleto do relatório por caso (decisão 104). Quem preenche cada campo:

| Campo da 5.5 | De onde sai | Quem preenche |
|---|---|---|
| Identificador exclusivo | id do caso e id da trilha | código |
| Título com resumo breve | causa escolhida em palavras e o campo afetado | código, pelo molde |
| Data, organização e autor | data da corrida; autor "agente (qwen2.5:7b, biblioteca de produção pelo hash)" | código |
| Objeto de teste e ambiente | cobaia, página, rota; `ambiente.json`, versão do Ollama, hash da biblioteca | código |
| Contexto | roteiro, passo, modo de injeção, cenário | código |
| Descrição para reproduzir | os passos do roteiro até a falha, a requisição, o status, a resposta (trecho) | código |
| Resultados esperados e reais | contrato e referência em modo normal contra o corpo recebido (o diff que a poda e o caso ao vivo já calculam) | código |
| Severidade e prioridade | em branco, com a classe e o nível do caso ao lado como sugestão | analista, no hub |
| Status | aberto, por padrão | analista, no hub |
| Referências | verbetes citados (pela camada de leitura), caso escrito, trilha | código |

2. A terminologia erro, defeito, falha e causa-raiz no sentido do syllabus, com a diferença declarada: a "causa raiz" do projeto é a categoria do defeito observado (seção 2.2 acima).
3. A análise de impacto antes da regressão (2.2.3 e 2.3) como base formal da integração com o Git.
4. Os riscos da automação (6.2) como base do princípio "a IA nunca aprova sozinha" e da revisão humana (decisão 95).
5. A distinção teste contra depuração (1.1): o agente testa e apoia a depuração.
6. O primeiro princípio (1.3): o relatório nunca afirma ausência de defeitos.

##### 5 Como citar no TCC

A referência acima entra na bibliografia; as citações no texto seguem a forma (ISTQB, 2023, p. 26). Onde entra: a seção 4 (fundamentação) ganha o parágrafo dos níveis e tipos (2.2.1 e 2.2.2), a terminologia (1.2.3) e a pirâmide (5.1.6); a seção 5 (método) nomeia o nível e os tipos e cita a análise de impacto (2.2.3 e 2.3) e os riscos da automação (6.2); a seção 6.9 descreve o relatório v3 pelos campos da 5.5; o glossário alinha "E2E", "defeito", "falha" e "causa raiz" ao texto do syllabus.

##### 6 O que esta leitura não cobre

Só as seções listadas foram lidas por inteiro. Os capítulos 3 (teste estático) e 4 (técnicas de teste) não foram aplicados ao projeto: as técnicas de caixa-preta da seção 4.2 (partição de equivalência, valores-limite, tabela de decisão) poderiam descrever como o banco de 90 casos foi desenhado (duas por classe de causa e por nível), e isso fica como possível acréscimo ao TCC, a conferir contra o texto do capítulo 4. O capítulo 5 foi lido só nas seções 5.1.6, 5.1.7 e 5.5.

#### 6.15.7 Repositório enesozturk/dimensional-drawing (`pos4-repo-dimensional-drawing`; 3 fontes com endereço)

*Leitura de:* subagente, em 07/11/2026; arquivo `repo-01-dimensional-drawing.md` em `5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/`. Interesse declarado pelo Eric: alto.

Fontes lidas: página do repositório no GitHub e README bruto (raw.githubusercontent.com). Não há pasta docs/ nem artigo citado; o README cita apenas a página de desenhos dimensionais da Apple e um post no X.

##### 1 O que é e como funciona por dentro

- É um conjunto de duas "skills" de agente (pastas com SKILL.md em Markdown, mais exemplos e modelos). Não é biblioteca nem programa: é texto de instrução que o agente carrega.
- A skill `dimensional-drawing` manda o agente transformar um componente de interface (cartão, diálogo) em uma folha técnica de uma página, no estilo dos desenhos dimensionais da Apple. A folha traz bloco de título, notas, vista em planta, camadas explodidas, vistas de detalhe e tabelas de variáveis.
- O mecanismo é um conjunto de regras de redação: só tons de cinza; rótulos de arquitetura e não de conteúdo (por exemplo `TITLE SLOT · FLEX`); relações como variáveis (`H1 = 2·S1 + H3`) e não números soltos; nomes neutros (`UI-CARD-001`); valores desconhecidos marcados `[TBD]` em vez de inventados.
- A entrada é uma fonte indicada pelo usuário (arquivo do repositório, story do Storybook, URL ou captura de tela). A saída são arquivos HTML (há exemplos de cartão e diálogo).
- A segunda skill, `dimensional-drawing-motion`, anima a folha pronta em um filme de cerca de 10 s (aproximação, planta, camadas se separando, recuo). Tem dois adaptadores: o artefato Motion do Claude (alvo principal) e um renderizador headless com Playwright e ffmpeg.

##### 2 Pilha, dependências e exigências

- GPU: não. Nuvem: a skill de desenho roda no agente que a carrega; o caminho principal da skill de movimento usa o artefato Motion do Claude (serviço do Claude, não local). Chave de API: não citada pelo repositório. Outro modelo residente: não.
- Skill de desenho: só um agente com suporte a skills (Claude Code, claude.ai, Claude desktop ou qualquer agente via `npx skills add`).
- Skill de movimento headless: Node 18 ou superior, ffmpeg e pacotes npm incluindo Playwright (Chromium). Remotion, Motion Canvas, GSAP e Lottie não foram testados.
- Licença: MIT (Enes Ozturk).
- Maturidade: cerca de 1,9 mil estrelas, 136 forks, 4 pull requests abertos, tópicos skills e ui. Histórico com um único commit visível. Data de criação, data do último commit e releases: não visto (a página mostra Releases e Packages vazios; procurei na página do repositório e no README).

##### 3 Aplicação ao desenvolvimento com o Claude Code neste projeto

- Serve? Praticamente não. O assunto é desenho técnico de componentes de interface, e este projeto não projeta interface própria de produto: o painel é HTML estático gerado por Python, e a interface do analista está adiada para depois da Fase 4.
- Uso marginal possível: gerar uma folha de especificação do painel ou do futuro hub do analista como figura para o documento do TCC. É estética, não ganho de método.
- Custo de instalar: baixo (copiar duas pastas para `~/.claude/skills/`). Manutenção: quase nula (texto), mas cada skill instalada entra na lista de skills do contexto e pesa um pouco no prefixo de cache, o que vai contra a regra de economia de tokens do projeto. A parte headless traria Node, ffmpeg e npm, runtimes que o projeto não usa.
- Recomendação: não instalar de forma permanente. Se houver necessidade pontual, ler o SKILL.md e copiar as regras (variáveis em vez de números, `[TBD]` em vez de invenção) para uma instrução local.

##### 4 Aplicação dentro do agente ou do produto

- Serve? Não, em nenhum módulo (poda, busca, diagnóstico, trilha e relatório, cura de seletor). O repositório não faz nada com DOM, seletores, falhas de teste ou diagnóstico.
- Painel ou hub do analista: único módulo com alguma ligação, e só como inspiração de apresentação (folha com título, notas e tabela de variáveis). Não há código reaproveitável.
- A ideia "valores desconhecidos viram `[TBD]`, nunca inventados" é parente da regra do projeto de validar em código e não confiar no modelo, mas já está coberta pela trilha v2 e pelos relatórios gerados por código.
- Conflitos com o contexto:
  - Prompt congelado byte a byte: incluir qualquer skill ou texto novo no diagnóstico obrigaria a medir tudo de novo.
  - Só biblioteca padrão no harness em Python: a parte headless exige Node 18+, npm, ffmpeg e Playwright via npm.
  - Sem administrador no Windows 11 corporativo: instalar Node e ffmpeg pode esbarrar na restrição.
  - Nada em nuvem: o alvo principal da skill de movimento é o artefato Motion do Claude.
  - Um modelo residente por vez em CPU: gerar folhas e filmes por LLM competiria com o qwen2.5:7b, e um 7B local não teria a qualidade de agente esperada pela skill.
  - Relatório gerado por código: a folha da skill é escrita pelo modelo, o oposto da regra "primeiro a máquina, depois o modelo".

##### 5 Risco, esforço e veredito

- Risco: baixo para o Claude (arquivos de texto, licença MIT), mas com custo de contexto e de dispersão. Para o agente: alto em relação ao ganho, porque violaria várias restrições sem benefício para o diagnóstico.
- Esforço: Claude, cerca de meia sessão para instalar e testar uma folha do painel; agente, não se aplica (nenhuma sessão recomendada).
- Veredito para o Claude Code: não adotar; no máximo uso pontual para uma figura do painel, sem instalação permanente.
- Veredito para o agente: não serve; sem módulo de aplicação e com conflito com prompt congelado, biblioteca padrão, ausência de nuvem e CPU única.

##### 6 Referências ABNT NBR 6023

- OZTURK, Enes. **dimensional-drawing**: agent skills para criar desenhos dimensionais de componentes de interface. Disponível em: https://github.com/enesozturk/dimensional-drawing. Acesso em: 7 nov. 2026.
- Artigos citados pelo repositório: nenhum artigo científico. Os links do README são páginas de terceiros, listados para rastreio:
  - APPLE. **Accessories: dimensional drawings**. Disponível em: https://developer.apple.com/accessories/dimensional-drawings/. Acesso em: 7 nov. 2026. (citada pelo README, não aberta por mim)
  - STORM, Andreas. Publicação no X. Disponível em: https://x.com/avstorm. Acesso em: 7 nov. 2026. (citada pelo README, não aberta por mim; título e data não vistos)

#### 6.15.8 Repositório HKUDS/RAG-Anything (`pos4-repo-rag-anything`; 2 fontes com endereço)

*Leitura de:* subagente, em 07/11/2026; arquivo `repo-02-rag-anything.md` em `5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/`. Interesse declarado pelo Eric: médio.

Fontes lidas: página do repositório no GitHub e README bruto (raw.githubusercontent.com). Não foram lidos o artigo completo nem os arquivos de docs/ (a página lista só os nomes `context_aware_processing.md`, `batch_processing.md` e `multimodal_rag_failure_modes.md`).

##### 1 O que é e como funciona por dentro

Framework de RAG multimodal construído sobre o LightRAG. Ingere documentos com texto, imagens, tabelas e equações num só fluxo de quatro etapas.
- Parsing: um parser escolhido na configuração (`RAGAnythingConfig`) quebra o documento em blocos. MinerU é o padrão; Docling e PaddleOCR são alternativas. O parser é fixo na inicialização.
- Análise multimodal: texto segue o caminho de texto. Imagens, tabelas e equações vão para processadores que usam um LLM ou modelo de visão para gerar descrições textuais.
- Grafo de conhecimento: o LightRAG extrai entidades e relações; os elementos multimodais são ligados ao texto e a hierarquia do documento é guardada por relações "belongs_to".
- Recuperação: busca vetorial combinada com travessia do grafo (modos `hybrid`, `local`, `global`, `naive`). Há consulta com visão (imagens recuperadas vão ao modelo de visão) e consulta com tabela ou equação anexada.
Em resumo: converte tudo em texto por meio de modelos, indexa em vetores mais grafo e responde por LLM.

##### 2 Pilha, dependências e exigências

- Linguagem: Python 3.10 ou superior (MinerU 3.x suporta 3.10 a 3.13).
- LLM: obrigatório. Os exemplos usam `gpt-4o-mini` da OpenAI.
- Modelo de visão: usado para imagens e consultas com visão (exemplos com `gpt-4o`).
- Modelo de embedding: obrigatório (exemplos com `text-embedding-3-large`, dimensão 3072). Ou seja, exige um segundo e um terceiro modelo além do LLM.
- Chave de API: necessária no processamento completo dos exemplos. Os exemplos usam funções no estilo OpenAI com `base_url` opcional; o README não menciona Ollama nem modelos locais.
- GPU: opcional (MinerU acelera com CUDA). Sem GPU roda em CPU, mais lento.
- Nuvem: não obrigatória em tese, mas o caminho documentado é a API da OpenAI. Áudio usa faster-whisper (local).
- LibreOffice: só para arquivos Office (doc, docx, ppt, pptx, xls, xlsx).
- Node: não exigido. Instalação: `pip install raganything` ou `uv sync` a partir do código-fonte.
- Licença: MIT (página do GitHub). O texto do README não a declara.
- Maturidade: cerca de 24,5 mil estrelas, 2,9 mil forks, 526 commits. Release: nenhuma listada. Data do último commit: não visto (a página não mostra datas). Data de criação: não vista. Artigo: arXiv 2510.12323, outubro de 2025.

##### 3 Aplicação ao desenvolvimento com o Claude Code neste projeto

Não serve. O desenvolvimento já se apoia em CLAUDE.md, memória persistente, skills e subagentes, e o conteúdo a consultar (código, painel, livro-razão, notas em Markdown) é texto, não PDF com figuras e equações. Indexar a documentação do projeto exigiria um LLM, um modelo de embedding e provavelmente chave de API, tudo fora do fluxo atual, e o embedding já perdeu em medição neste corpus. Instalar custaria Python 3.10+, MinerU (pesado), LibreOffice opcional e manutenção de índice e grafo. Um único uso marginal: ingerir PDFs de artigos e do livro (Faceli) para consulta pelo Claude. Esse uso é coberto por leitura direta de PDF com PyMuPDF e pelo painel de pesquisa já existente, sem custo extra.

##### 4 Aplicação dentro do agente ou do produto

Não serve em nenhum módulo. Conflitos com o contexto:
- Busca: o embedding foi medido e descartado (hit@3 de 35,6% contra 80,0% do BM25 com sinais em código na biblioteca de 40 verbetes). O RAG-Anything depende de embedding mais grafo; trocar a busca exige repetir toda a medição.
- Modelo residente único: o framework quer LLM, visão e embedding. Com um modelo por vez em CPU (qwen2.5:7b, num_ctx 8192), alternar três modelos custa carga de memória a cada troca em 16 GB.
- Prompt do diagnóstico congelado byte a byte: o contexto injetado pelo grafo mudaria o prompt e obrigaria a medir tudo de novo.
- Nuvem e chave de API: o caminho documentado usa OpenAI, o que viola "nada em nuvem". Com endpoint local (compatível com OpenAI) seria teoricamente possível, mas o README não confirma.
- Harness só com biblioteca padrão: o framework puxa LightRAG, MinerU e dependências pesadas; sem administrador no Windows corporativo, instalar MinerU e LibreOffice é arriscado.
- Corpus: 40 verbetes Markdown curtos não têm imagens, tabelas ou equações; o ganho multimodal não se aplica. Poda, trilha, relatório, cura de seletor e painel não têm parte de documento multimodal para ingerir.
- Possível ideia isolada: a seção "multimodal_rag_failure_modes.md" da documentação pode interessar como leitura sobre modos de falha, mas não foi lida.

##### 5 Risco, esforço e veredito

- Uso com o Claude Code: risco baixo, ganho próximo de zero. Esforço de 1 a 2 sessões para instalar e configurar, mais manutenção. Veredito: não adotar; só citar como trabalho relacionado.
- Uso no agente: risco alto (quebra restrições de modelo único, prompt congelado, nuvem e medição já feita). Esforço de várias sessões mais nova bateria de medição. Veredito: não adotar; registrar como descartado por conflito de restrições.

##### 6 Referências ABNT NBR 6023

GUO, Zirui et al. **RAG-Anything**: All-in-One RAG Framework. Disponível em: https://github.com/HKUDS/RAG-Anything. Acesso em: 7 nov. 2026.

GUO, Zirui; REN, Xubin; XU, Lingrui; ZHANG, Jiahao; HUANG, Chao. **RAG-Anything**: All-in-One RAG Framework. arXiv:2510.12323, 2025. Disponível em: https://arxiv.org/abs/2510.12323. Acesso em: 7 nov. 2026.

#### 6.15.9 Repositório activeing123/mcptoon (`pos4-repo-mcptoon`; 7 fontes com endereço)

*Leitura de:* subagente, em 07/11/2026; arquivo `repo-03-mcptoon.md` em `5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/`. Interesse declarado pelo Eric: alto.

Fontes lidas em 7 nov. 2026: página https://github.com/activeing123/mcptoon e README bruto (raw.githubusercontent.com/.../HEAD/README.md). Os arquivos docs/faq.md, docs/real-world-benchmark.md e docs/tiktoken-benchmarks.md são citados no README, mas não foram abertos; os números abaixo vêm só do README e são medições do próprio autor.

##### 1 O que é e como funciona por dentro

mcptoon é uma CLI local em Python, sem dependências, que faz de "porta única" para servidores MCP e skills de agentes. O objetivo é não mandar o esquema completo de todas as ferramentas a cada turno.

- Em vez do esquema inteiro, expõe um índice compacto de nomes (`manifest`). O esquema de uma ferramenta só vem sob demanda (`inspect`), e `call` executa. `select "<tarefa>"` devolve as poucas ferramentas mais prováveis.
- Para skills, um ponteiro residente custa 39 tokens e `skills resolve` devolve uma lista curta (791 tokens para 5 skills) ranqueada por BM25 offline.
- `call --toon` recodifica o resultado no formato TOON (padrão aberto, v4.1, MIT, github.com/toon-format/toon, via python-toon vendorizado). É uma codificação estruturada reversível; se a decodificação falha, cai para JSON. Há também o formato SLIM (nomes mais tipos dos parâmetros), criado pelo mcptoon e que não é TOON.
- Resultados byte a byte idênticos na sessão viram referência (dedup); `retrieve` recupera o original.
- Três modos: CLI (custo fixo zero por turno), serve (custo fixo pequeno, uma entrada MCP por stdio ou HTTP) e direct (todos os esquemas carregados, o mais caro). Uma instalação nova pode ficar em direct e não economizar nada até rodar `mcptoon quickstart`.
- Barreiras sobre resultados: bloqueio de ação destrutiva, varredura de injeção de prompt e detecção de vazamento de credencial.

Números de redução da página (todos medições do autor, com `tiktoken cl100k_base`):

| Amostra | Antes | Depois | Redução |
|---|---:|---:|---:|
| 255 ferramentas sintéticas, 50 servidores: JSON para TOON | 71.929 | 47.438 | 34% |
| mesma amostra, SLIM | 71.929 | 8.282 | 88,5% |
| mesma amostra, Compact | 71.929 | 581 | 99,2% |
| 7 servidores públicos reais, 209 ferramentas | 640.606 | 905 | 99,86% |
| máquina local, 212 esquemas (manifest) | 640.787 | 914 | 99,85% |
| máquina local, 480 arquivos de skill (ponteiro) | 1.572.330 | 39 | 99,99% |

Ressalvas que o próprio README faz: o 99,2% é "do lado da definição" (não carregar esquemas), não compressão de resultado, e cresce com o tamanho do catálogo. O ganho do TOON sobre resultados depende da forma: amostra mista 5,7% menor, faixa de 1,8% a 48,6% (lista de registros quase não encolhe, registro único cai pela metade), e o texto avisa para não assumir 34% fixos. Os números de terceiros (Anthropic 150.000 para 2.000; Firecrawl 1.365 contra 44.026; Scalekit 10 a 32 vezes mais barato) são citados, não medidos por ele. `mcptoon bench` mede o catálogo do usuário.

##### 2 Pilha, dependências e exigências

- Linguagem: Python puro, só biblioteca padrão (CI verifica com `scripts/check_zero_deps.py`). Página descreve 41.185 linhas em 56 módulos. Pacote de 565 KB. Testes: "3035 passed, 2 skipped" (declarado).
- GPU: não. Nuvem: não é exigida; README diz sem telemetria. Única chamada externa: `install --search`, que consulta registros (Smithery, Registro MCP Oficial). Chave de API: não para o gateway em si (os servidores MCP que ele fronteia podem exigir as suas).
- Node: não para o núcleo; `uvx mcptoon demo --quick` exige Node. Instala por `pip install mcptoon`, pipx, venv, a partir do código-fonte, plugin do Claude Code ou Nix. Windows descrito como alvo de primeira classe.
- Licença: Apache-2.0 (com NOTICE creditando o padrão TOON). Declara-se projeto independente, sem vínculo com a Anthropic.
- Maturidade: 423 estrelas, 26 forks, 2 observadores, 535 commits em `main`, 1 issue e 1 pull request abertos. Data do último commit: não visto (a página mostra só a contagem, sem data). Data de criação: não vista. Versão ou release: não vista (as seções Releases e Tags não mostraram contagem). Contribuidores: não visto. Há pasta `docs/`, `claude-code-plugin/`, `skills/mcptoon`, `plugin/mcptoon-skills`.
- Ponto de cautela: projeto de terceiro, único autor aparente na página, com afirmações de compatibilidade (103 clientes, 3035 testes) que não pude verificar.

##### 3 Aplicação ao desenvolvimento com o Claude Code neste projeto

Serve em tese, com ganho pequeno aqui. A economia do mcptoon vem de catálogos grandes de ferramentas MCP e de muitas skills. Este projeto já usa poucas integrações e o Claude Code do aplicativo já adia o carregamento de ferramentas (ferramentas diferidas aparecem só pelo nome e o esquema é buscado sob demanda), que é o mesmo mecanismo do `manifest` e `inspect`. Parte do ganho já existe sem instalar nada.

Onde poderia ajudar:
- Reduzir o custo fixo de esquemas se o Eric ligar muitos servidores MCP ao mesmo tempo. A regra do projeto (plugins e MCP fixados no início da sessão, para manter o cache de prefixo) vai no mesmo sentido, então o gateway só compensa se o número de servidores crescer.
- `skills resolve` com BM25 poderia aliviar listas longas de skills; a lista de skills desta sessão é grande, mas já é carregada como descrições de uma linha.
- `retrieve` e dedup de resultados repetidos, útil em sessões com muitas leituras iguais.

Custo de instalar e manter:
- Instalação em venv sem administrador é viável (`pip install mcptoon`, sem dependências). O custo real está em `mcptoon quickstart`, que reescreve a configuração dos clientes (takeover; há `restore`, `off` e `uninstall --dry`). Pelas regras deste projeto, o Claude não edita o `~/.claude.json` (memória do projeto: modo automático), então o Eric teria de rodar os comandos, com caminho completo e cwd em minúsculo.
- Mais uma peça entre o Claude e as ferramentas: se der erro, a depuração passa por ela. Atualizações exigem acompanhar um projeto de terceiro cujo ritmo de releases não vi.
- Mudar plugins e MCP no meio do trabalho quebra o cache de prefixo e invalida as medições de tokens do projeto; qualquer adoção exigiria medir antes e depois com `ferramentas/medir_tokens.py`.

##### 4 Aplicação dentro do agente ou do produto

Não serve em nenhum módulo. O agente não usa MCP: o harness em Python chama o Ollama, o Playwright e o BM25 próprio diretamente. O mcptoon resolve um problema (esquema de ferramentas MCP inflando o contexto) que o agente não tem.

Módulo por módulo:
- Poda: não aplicável. A poda decide o que do DOM e do corpo da resposta entra no prompt, é regra em código sobre dados da aplicação-alvo, não esquemas de ferramentas.
- Busca: já existe BM25 com sinais em código sobre 40 verbetes. O `skills resolve` do mcptoon também usa BM25, mas sobre skills, sem os sinais próprios e sem o frontmatter do projeto. Trocar a busca atual por ele perderia os sinais contra a referência (decisão 97) e exigiria remedir a recuperação.
- Diagnóstico: aqui está o conflito central. O prompt do diagnóstico é congelado byte a byte; qualquer recodificação do contexto (por exemplo, passar o corpo ou o diff em TOON) muda os bytes enviados ao qwen2.5:7b e obriga a medir tudo de novo (corridas 16 a 24). O TOON ainda economiza só 1,8% a 48,6% conforme a forma, e um modelo de 7B em CPU nunca foi avaliado lendo TOON, então a precisão do rótulo poderia cair. A tela já está no limite de 1.409 tokens medido em `medir_prompt_tela.py`; um ganho de tokens poderia ajudar nisso, mas só ao custo de reabrir o prompt congelado.
- Trilha e relatório: a trilha v2 é JSONL por passo e o relatório Markdown é gerado por código, ambos legíveis por pessoas e pelos testes. Trocar por TOON não traria ganho para o modelo (a trilha não vai ao prompt) e quebraria a leitura direta e as ferramentas de avaliação.
- Cura de seletor, painel e hub do analista: nenhum usa esquemas MCP. O painel é HTML estático gerado por Python.

Conflitos com as restrições do contexto:
- Prompt congelado: conflito direto, como acima.
- Harness só com a biblioteca padrão: o mcptoon também é só biblioteca padrão, então não conflita nesse ponto, mas adicionaria um pacote de 41 mil linhas de terceiro ao ambiente sem necessidade.
- Nada em nuvem: o núcleo roda local, mas `install --search` consulta registros externos; teria de ficar desligado. Não há administrador, o que a instalação em venv contorna.
- Um modelo residente por vez, num_ctx 8192, CPU: o mcptoon não consome RAM relevante (CLI sem daemon), então não conflita; também não ajuda o gargalo, que é a inferência do 7B.
- Medição: qualquer mudança na forma dos dados lidos pelo modelo invalida as leituras vigentes (`tela_v4`, `cenarios_v4`).

##### 5 Risco, esforço e veredito

Claude Code (desenvolvimento)
- Risco: médio-baixo. Reescreve a configuração de clientes (reversível por `restore`), é projeto de terceiro de um autor, com avisos de segurança próprios (injeção de prompt, vazamento) cuja eficácia não vi testada. Mexe no prefixo e no cache.
- Esforço: cerca de 1 sessão para instalar em venv, rodar `mcptoon bench` no catálogo real e comparar tokens antes e depois; mais 1 sessão se for adotado e precisar de manutenção. O Eric precisa executar os comandos que tocam o `~/.claude.json`.
- Veredito: só vale testar com `mcptoon bench` e `--dry` se o número de servidores MCP crescer; hoje o ganho é pequeno porque o Claude Code já adia os esquemas, então não adotar agora.

Agente (produto do TCC)
- Risco: alto para o rigor da pesquisa, porque tocar na forma do contexto lido pelo modelo reabre o prompt congelado e invalida as corridas 16 a 24.
- Esforço: 3 ou mais sessões (adaptar a poda, remedir a calibração, a tela, a cura e a biblioteca) para um ganho de 1,8% a 48,6% em formas de dado específicas, sem evidência de que o qwen2.5:7b lê TOON com a mesma precisão.
- Veredito: não aplicar; no máximo registrar o TOON como trabalho futuro e citar o resultado do autor como referência de redução de tokens por serialização.

##### 6 Referências ABNT NBR 6023

ACTIVEING123. **mcptoon**: one zero-dependency MCP gateway CLI for every server and agent skill. [S. l.]: GitHub, [20--?]. Disponível em: https://github.com/activeing123/mcptoon. Acesso em: 7 nov. 2026.

ACTIVEING123. **README do mcptoon**. [S. l.]: GitHub, [20--?]. Disponível em: https://raw.githubusercontent.com/activeing123/mcptoon/HEAD/README.md. Acesso em: 7 nov. 2026.

TOON FORMAT. **TOON**: Token-Oriented Object Notation, especificação v4.1. [S. l.]: GitHub, [20--?]. Disponível em: https://github.com/toon-format/toon. Acesso em: 7 nov. 2026. (Citada pelo README; não aberta diretamente.)

ANTHROPIC. **Code execution with MCP**. [S. l.]: Anthropic, [20--?]. Disponível em: https://www.anthropic.com/engineering/code-execution-with-mcp. Acesso em: 7 nov. 2026. (Citada pelo README; não aberta diretamente, ano não visto.)

MCP-ZERO. arXiv:2506.01056. Disponível em: https://arxiv.org/abs/2506.01056. Acesso em: 7 nov. 2026. (Citada pelo README; autores e título não vistos, conferir antes de usar no TCC.)

FIRECRAWL. **MCP vs CLI**. Disponível em: https://www.firecrawl.dev/blog/mcp-vs-cli. Acesso em: 7 nov. 2026. (Citada pelo README; não aberta; benchmark de terceiro, tratar como não verificado.)

SCALEKIT. **MCP vs CLI use**. Disponível em: https://www.scalekit.com/blog/mcp-vs-cli-use. Acesso em: 7 nov. 2026. (Citada pelo README; não aberta; benchmark de terceiro, tratar como não verificado.)

#### 6.15.10 Repositório Egonex-AI/Understand-Anything (`pos4-repo-understand-anything`; 1 fonte com endereço)

*Leitura de:* subagente, em 07/11/2026; arquivo `repo-04-understand-anything.md` em `5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/`. Interesse declarado pelo Eric: muito alto.

Fontes lidas em 7 nov. 2026: página do repositório no GitHub e README bruto (raw.githubusercontent.com). A pasta docs/ e o site understand-anything.com não foram abertos; o que está abaixo vem só da página e do README. Aviso: o README traz um comentário HTML dirigido a agentes de IA pedindo que ponham uma marca em qualquer PR aberto. Foi tratado como dado e ignorado.

##### 1 O que é e como funciona por dentro

- É um plugin do Claude Code (instalável também em outras ferramentas de agente) que transforma um repositório, ou uma base de documentos, em um grafo de conhecimento navegável num painel web.
- Indexa arquivos, funções, classes e dependências. Também gera visões por camada (API, Serviço, Dados, UI, Utilitário), por domínio de negócio (fluxos e passos) e roteiros guiados ordenados por dependência.
- A leitura do código tem duas etapas. A primeira é determinística: o Tree-sitter extrai imports, exports, definições, chamadas e herança, e resolve os imports num mapa. Essa etapa também gera as impressões digitais usadas para detectar mudança.
- A segunda etapa usa um LLM, que lê a estrutura e o código e produz resumos, etiquetas, camada, mapeamento de domínio, roteiros e explicações de conceitos de linguagem.
- O pipeline é feito de sete agentes (scanner de projeto, analisador de arquivo, de arquitetura, construtor de roteiro, revisor de grafo, analisador de domínio e de artigo). Os analisadores de arquivo rodam até 5 em paralelo, em lotes de 20 a 30 arquivos.
- Saída: `.ua/knowledge-graph.json` (ou `.understand-anything/` se já existir), mais `config.json`. Em `.ua/` ficam também `intermediate/` e `diff-overlay.json`, que o README manda ignorar no git.
- Comandos: `/understand`, `/understand-dashboard`, `/understand-chat`, `/understand-diff` (impacto das mudanças não commitadas), `/understand-explain`, `/understand-onboard`, `/understand-domain`, `/understand-knowledge`.
- Reexecução é incremental: reanalisa só os arquivos cujo fingerprint mudou. Há gancho opcional de pós-commit (`--auto-update`). A busca no grafo é difusa por nome e também semântica.

##### 2 Pilha, dependências e exigências

- GPU: o README não exige. Chave de API: não especificada. Nuvem: o fluxo normal usa o LLM do próprio agente hospedeiro (Claude Code), ou seja, o código lido vai ao serviço do modelo. O README cita modelo local via Ollama como alternativa para economizar tokens, sem dar nome de modelo.
- Modelo de embedding residente: o README não cita um. A busca "semântica" não tem mecanismo descrito na página; "não visto".
- Runtime: Node.js 18 ou superior para o visualizador; build a partir do clone usa pnpm e TypeScript (há vitest, eslint). Tree-sitter entra na análise. Instalador `install.ps1` clona para `~/.understand-anything/repo` e cria links simbólicos.
- Visualizador somente leitura roda por `npx` a partir de um tarball, sem chamada a LLM e sem dados saindo da máquina.
- Licença: MIT (Yuxiang Lin e Infinite Universe, Inc.).
- Maturidade: cerca de 91,2 mil estrelas, 7,8 mil forks, 873 commits em `main`. Data do último commit: não visto (a página não mostra). Versão ou release: não visto (seção Releases vazia). Data de criação: não visto. Linguagens: não visto (seção sem detalhamento).
- Aviso de custo: a primeira execução em projeto grande gasta muitos tokens; o README recomenda plano ou assinatura.

##### 3 Aplicação ao desenvolvimento com o Claude Code neste projeto

- Serve em tese: o Claude Code é o alvo nativo e o plugin se instala pelo marketplace. Ajudaria a navegar o próprio repositório do TCC (harness em Python, fichas, painel) e as duas cobaias, com resumos e grafo de dependências.
- Utilidade real aqui é baixa. O repositório já tem CLAUDE.md, memória persistente, `.claude/rules/`, livro-razão e painel que cumprem o papel de mapa. O grafo seria um segundo mapa a manter coerente com esses.
- Custo de instalar: um comando de marketplace, mais Node 18 para ver o painel. Em máquina corporativa sem administrador, o Node portátil pode ser necessário; a instalação do plugin via `install.ps1` grava em `~/.understand-anything`, o que costuma funcionar sem administrador, mas não foi testado.
- Custo de manter: tokens na primeira análise (o repositório tem muitos Markdown e logs); regra do projeto de economia de tokens (primeiro a máquina, depois o modelo) vai contra rodar sete agentes de LLM sobre tudo. Pasta `.ua/` precisaria entrar no `.gitignore` ou ser decidida (a regra do projeto sobre o que se versiona é do Eric).
- Possível uso pontual: `/understand-diff` ou `/understand-onboard` nas cobaias (PHP legado e FastAPI) para uma sessão de exploração, sem instalar de forma permanente.

##### 4 Aplicação dentro do agente ou do produto

Em geral não serve como componente do agente. Motivo central: a análise semântica depende de um LLM. Para o agente isso significa o qwen2.5:7b em CPU, com num_ctx 8192, um modelo por vez, sobre 20 a 30 arquivos por lote e sete etapas de agente. Não há descrição de que o pipeline funcione com modelo de 7B; o próprio README fala de "modelo local" apenas de forma geral.

Por módulo:
- Poda: não serve. A poda do projeto é determinística em código sobre o corpo da resposta; o grafo é de código-fonte, outro objeto.
- Busca: não serve. A busca BM25 com sinais em código sobre 40 verbetes está fechada, e a busca híbrida com embedding foi medida e descartada. A busca "semântica" do plugin entra no mesmo caso e, se usar embedding, conflita com "um modelo residente por vez".
- Diagnóstico: não serve. O prompt está congelado byte a byte; qualquer contexto extra vindo do grafo muda o prompt e obriga a medir tudo de novo.
- Trilha e relatório: não serve. A trilha v2 em JSONL e o relatório em Markdown já são gerados por código; o grafo em JSON de outro formato não se encaixa nos eventos.
- Cura de seletor: não serve. É por nome parecido no DOM, sem relação com grafo do código.
- Painel e hub do analista: a ideia de grafo navegável e roteiros guiados é um bom modelo de inspiração para o painel, mas copiar o código traz Node, painel em React/TypeScript e dependências, contra "painel em HTML estático gerado por Python". Só como referência de desenho.

Ideia de o agente ler o que mudou no git das cobaias para preparar testes:
- A parte útil é a detecção de mudança por fingerprint e o `/understand-diff` (impacto das mudanças). Mas isso se faz com o `git diff` e a lista de arquivos alterados, em Python da biblioteca padrão, sem LLM. É o caminho coerente com "primeiro a máquina, depois o modelo".
- Usar o plugin para isso conflita com: nada em nuvem (o fluxo usa o LLM do hospedeiro), sem administrador e Node como runtime extra, harness só com a biblioteca padrão do Python, CPU sem GPU e 7B, um modelo por vez, e prompt congelado se o resultado alimentar o diagnóstico.
- Hipótese que valeria testar sem o plugin: um script que mapeia arquivos alterados do PHP e da FastAPI para rotas e telas afetadas e escolhe os cenários a rodar. É trabalho próprio da Fase 5, fora do plugin.

##### 5 Risco, esforço e veredito

- Uso com o Claude Code: risco baixo (plugin MIT, reversível). Esforço: 1 sessão para instalar e testar nas cobaias; manutenção contínua não compensa. Veredito: opcional e de baixo valor, testar no máximo uma vez nas cobaias e não adotar de forma permanente.
- Uso dentro do agente: risco alto (LLM de 7B em CPU sobre lotes grandes, Node, dados fora da máquina se o hospedeiro for nuvem, prompt congelado). Esforço: 3 a 5 sessões para adaptar, com resultado incerto. Veredito: não usar; aproveitar apenas a ideia (fingerprint e impacto de diff), feita em Python local com `git diff`.

##### 6 Referências ABNT NBR 6023

LIN, Yuxiang; INFINITE UNIVERSE, INC. (Egonex-AI). **Understand-Anything**. Disponível em: https://github.com/Egonex-AI/Understand-Anything. Acesso em: 7 nov. 2026.

Artigos citados pelo repositório: a página do README informa que não cita artigos acadêmicos (procurado na página do repositório e no README bruto). Links citados, não acadêmicos: gist do padrão de wiki de LLM atribuído a Karpathy e documentação de plugins do Claude Code; não foram abertos, logo não são referenciados aqui.

#### 6.15.11 Repositório sodiumsun/agenttrail (`pos4-repo-agenttrail`; 4 fontes com endereço)

*Leitura de:* subagente, em 07/11/2026; arquivo `repo-05-agenttrail.md` em `5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/`. Interesse declarado pelo Eric: alto.

Fontes lidas: página do repositório, README.md, docs/INGEST.md, docs/OBSERVABILITY.md e package.json (raw.githubusercontent.com, ramo HEAD), em 7 nov. 2026. Não há artigo ou paper citado; a página do GitHub não lista releases.

##### 1 O que é e como funciona por dentro

- É um observador local de agentes de programação (Claude Code, Codex, pi e outros). Descrição da página: mostra o projeto como um mapa vivo do que cada agente está fazendo. Não roda agentes e não decide quando uma tarefa terminou.
- O que grava/lê: logs locais do Claude Code (`~/.claude/projects`) e do Codex (`~/.codex/sessions`), mudanças de arquivo via watcher, Git em modo leitura (branches, worktrees) e, opcionalmente, eventos de hooks do Claude Code. Lê só logs tocados nas últimas 2 horas e no máximo os últimos 2 MiB de cada um.
- Formato dos eventos de ingestão: JSON por POST em `127.0.0.1:<porta>/hook` (portas 5330 a 5344). Campos comuns: `hook_event_name`, `cwd`, `session_id`, `agent`. Tipos: SessionStart, PreToolUse, PostToolUse, PostToolUseFailure, TodoUpdate, Stop, SessionEnd, SubagentStop. Há `tool_use_id` e `files_written`.
- Não há campo de pai/filho: o doc de ingestão diz que não define parent. SubagentStop fecha "a linha de subagente aberta mais antiga", sem referenciar id.
- Estrutura de intenção: um `PLAN.md` com convenção própria (componentes `## Título {#id}`, tarefas `- [~] ... {#id}` com marcadores x, ~, !, vazio; campos `files:`, `needs:`, `links:`, `by:`, `from:`, `kind:`; seção `## decisions` com linhas datadas em texto livre).
- Como mostra: uma página estática em `localhost:5330` com cartões de componentes ligados por setas (`needs:`/`links:`), cartões de execução com ferramenta atual e trilha de arquivos, e uma visão inferida do Git quando não há plano. Há também um painel no app desktop Herdr e `GET /panel` (resumo versionado, somente leitura).
- Rótulos de evidência: "reportado", "observado", "inferido", "desconhecido"; progresso ausente nunca vira percentual. Isso é o ponto conceitualmente mais útil.
- Armazena em `~/.agenttrail` atividade recente, resumos e posições de leitura, com texto de comando encurtado (não guarda respostas completas nem saída de ferramenta).
- O doc de observabilidade diz expressamente que não há conceito de decisão, alternativa ou raciocínio, e que não oferece trilha completa de requisições ao modelo.

##### 2 Pilha, dependências e exigências

- Linguagem: daemon Node sem dependências e página estática (a página não mostra o gráfico de linguagens; "não visto" a divisão exata).
- Exige Node 20 ou superior (package.json: `engines: node >=20`). Sem `dependencies` declaradas. Uso via `npx agenttrail`.
- GPU: não. Nuvem: não (liga só em 127.0.0.1, sem conta, sem telemetria, sem chamadas a modelo). Chave de API: não. Framework de agente específico: não, mas os adaptadores nativos são para Claude Code, Codex e pi; outros agentes precisam postar eventos.
- Windows: o README diz que é "não testado"; as verificações automáticas rodam em Linux e macOS. O endpoint de hook não exige token (qualquer processo local pode postar).
- Licença: MIT.
- Maturidade: 989 estrelas, 70 forks, 5 observadores, 147 commits na main; versão 0.4.1 (package.json). Releases: nenhuma listada na página. Data de criação: não vista (página não mostra). Data do último commit: não vista (a página não exibe datas). Contribuidores: seção sem entradas visíveis. O README cita um projeto aposentado, "Kitchen", ainda no npm como `agenttrail-kitchen`.
- O repositório tem `CLAUDE.md`, `AGENTS.md`, `PLAN.md`, `CONTRIBUTING.md`, e pastas `docs/`, `integrations/pi`, `herdr/`, `public/`, `test/`, `bin/`.

##### 3 Aplicação ao desenvolvimento com o Claude Code neste projeto

- Serve? Parcialmente, como observador do próprio trabalho de desenvolvimento. Lê automaticamente os logs do Claude Code e mostra sessões, ferramentas, arquivos tocados, subagentes e listas de tarefas (TaskCreate/TodoWrite). Isso encaixa com as ondas de subagentes e o livro-razão `.superpowers/sdd/`.
- Para quê: ver numa página quais sessões/subagentes mexeram em quais pastas, e ligar isso a um `PLAN.md`. O projeto já tem plano, fichas e painel próprio, então o ganho é pequeno e duplica o painel do projeto.
- Custo de instalar: baixo (`npx agenttrail`, nada instalado de forma permanente), mas exige Node 20 na máquina. Windows corporativo sem administrador: Node portátil seria necessário; Windows não é testado pelo autor, então caminhos de `~/.claude` e o watcher podem falhar.
- Custo de manter: o autor avisa que formatos de log locais mudam entre versões do agente; é preciso acompanhar o pacote. O `init` escreve em CLAUDE.md/AGENTS.md e hooks em `.claude/settings.local.json`; isso alteraria arquivos que a regra do projeto manda marcar com a tag de IA, então só se usaria sem `init` (observação passiva, que não grava nada).
- Conflito com a regra de economia: Node é um runtime a mais; não pesa em tokens, mas pesa em manutenção.

##### 4 Aplicação dentro do agente ou do produto

- Como base da árvore de decisão lida da trilha v2: não como código nem como formato. O agenttrail registra o que o agente fez (ferramentas, arquivos, tarefas), não por que escolheu um caminho. Não existe alternativa considerada, motivo, evidência por escolha ou divergência. Também não existe `pai` entre eventos (só `session_id`, `tool_use_id`). A trilha v2 tem nós com id e pai, alternativas, evidências e divergência: é mais rica no que importa para "Decisão 1, 2, 3".
- Semelhança de formato: apenas superficial (um evento por passo em JSON, id de sessão, id de chamada). Um evento por linha JSONL não é o formato dele: ele usa POST de JSON e logs próprios dos agentes.
- Ideias aproveitáveis, sem importar nada: (a) os quatro rótulos de evidência (reportado, observado, inferido, desconhecido) para dizer ao analista de onde veio cada afirmação de uma Decisão, e a regra de nunca mostrar percentual quando falta dado; (b) a seção `decisions` datada do `PLAN.md` como modelo de registro curto e legível; (c) o mapa de componentes com setas `needs`/`links` como inspiração visual da árvore. Módulo: trilha e relatório (rótulos) e painel/hub do analista (visual).
- Conflitos com o contexto:
  - Windows 11 corporativo sem administrador: Node 20+ não faz parte do ambiente (exigiria runtime extra); o autor não testa em Windows.
  - Harness em Python só com biblioteca padrão e painel em HTML estático gerado por Python: um daemon Node e uma página própria quebram essa regra.
  - Prompt congelado e trilha v2 já definida: o formato do agenttrail não traz alternativas nem pai; adotá-lo exigiria remodelar a trilha.
  - Um modelo por vez, 16 GB, CPU: sem efeito direto (ele não chama modelo), mas rodar um daemon permanente é carga a mais.
  - Nada em nuvem: compatível (127.0.0.1 só).
  - Observar o agente de QA: ele lê logs do Claude Code e Codex; o agente do TCC usa Ollama e Playwright, sem adaptador, então só entraria por POST manual, o que replica o que a trilha já grava.

##### 5 Risco, esforço e veredito

- Uso no Claude Code: risco baixo a médio (Windows não testado, Node a mais, `init` altera CLAUDE.md e hooks, endpoint sem token, formatos de log sujeitos a mudança). Esforço: cerca de 1 sessão de trabalho para experimentar passivamente com `npx`, mais manutenção eventual. Ganho marginal, porque o painel e o livro-razão do projeto já cobrem.
- Uso no agente/produto: como dependência, risco alto (quebra as regras de Python puro, estático e sem runtime extra). Como inspiração conceitual, risco nulo. Esforço: cerca de 0,5 sessão para copiar os rótulos de evidência e o texto das decisões para o relatório por caso e para a leitura da árvore.
- Veredito para o Claude Code: opcional e de baixo valor; testar só de forma passiva com `npx agenttrail` (sem `init`) se houver Node 20 portátil, senão dispensar.
- Veredito para o agente: não adotar como base nem como formato da árvore de decisão (não registra alternativas nem pai); aproveitar apenas a ideia dos rótulos reportado/observado/inferido/desconhecido e o registro datado de decisões, implementados em Python na trilha e no relatório.

##### 6 Referências ABNT NBR 6023

SODIUMSUN. **agenttrail**: local observability for AI coding agents. Disponível em: https://github.com/sodiumsun/agenttrail. Acesso em: 7 nov. 2026.

SODIUMSUN. **agenttrail**: README.md. Disponível em: https://raw.githubusercontent.com/sodiumsun/agenttrail/HEAD/README.md. Acesso em: 7 nov. 2026.

SODIUMSUN. **agenttrail**: docs/INGEST.md. Disponível em: https://raw.githubusercontent.com/sodiumsun/agenttrail/HEAD/docs/INGEST.md. Acesso em: 7 nov. 2026.

SODIUMSUN. **agenttrail**: docs/OBSERVABILITY.md. Disponível em: https://raw.githubusercontent.com/sodiumsun/agenttrail/HEAD/docs/OBSERVABILITY.md. Acesso em: 7 nov. 2026.

Artigos citados pelo repositório: nenhum. Procurado no README, em docs/INGEST.md, docs/OBSERVABILITY.md e na página principal; só há links para o npm, o app Herdr (herdr.dev) e arquivos do próprio repositório.

#### 6.15.12 Repositório eagle-hq/EAGLE-4 (`pos4-repo-eagle-4`; 2 fontes com endereço)

*Leitura de:* subagente, em 07/11/2026; arquivo `repo-06-eagle-4.md` em `5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/`. Interesse declarado pelo Eric: médio.

Fontes lidas: página do repositório no GitHub e README bruto (raw.githubusercontent.com). Não li docs/ nem o PDF EAGLE4_Paper.pdf (interesse MÉDIO; a página e o README bastam para o veredito).

##### 1 O que é e como funciona por dentro

- É decodificação especulativa: um modelo rascunho (drafter) propõe tokens candidatos e o modelo alvo os verifica em lote; a saída final é a mesma que o alvo geraria sozinho (README: "same answers", temperatura 0).
- O pacote `eagle-harness` liga drafters EAGLE-4 a três motores de servidor: SGLang, vLLM e TokenSpeed. Ele mede custos reais no hardware instalado e ajusta o tamanho da árvore de rascunho conforme tamanho do lote, hardware e carga.
- Residente: o modelo alvo e o drafter EAGLE-4 ficam carregados juntos no mesmo servidor (download inicial de cerca de 62 GB no quick start). Os primeiros pedidos após a partida compilam kernels e calibram, por isso são mais lentos.
- Ganhos medidos (Qwen3.8-27B, temperatura 0, cliente SPEED-Bench, 4 GPUs NVIDIA B300): SGLang 3,42x com 1 requisição, 2,09x com 8, 1,39x com 64; vLLM 2,83x, 1,72x, 1,14x; TokenSpeed 3,09x, 2,02x, 1,41x. Em uma AMD MI355X com SGLang: 2,07x com 8 requisições e 1,56x com 32.
- O ganho cai conforme a concorrência sobe. Nenhuma medição em CPU, em laptop ou com modelo de 7B aparece na página.

##### 2 Pilha, dependências e exigências

- GPU: sim, obrigatória. Quick start testado em uma B300 com Linux e driver CUDA 13; ROCm suportado para MI355X. Pip exige Python 3.12, CUDA toolkit e compilador C++.
- Nuvem e chave de API: não exigidos (é servidor local), mas o hardware alvo é de datacenter.
- Outro modelo residente: sim, o drafter fica junto do alvo.
- Runtime: SGLang (pin `sglang==0.5.23.dev252+eagle.9`), vLLM ou TokenSpeed; imagem Docker `ghcr.io/eagle-hq/eagle-4-sglang:0.1.3`. Não há suporte declarado a Ollama nem a llama.cpp. Tópicos do repositório: eagle, gpu, llm-inference, sglang, speculative-decoding, tokenspeed, vllm.
- Licença: Eagle 4 Source-Available License, "não OSI" (código disponível, não é open source). Uso comercial de oferta concorrente exige licença comercial; demais usos comerciais têm teto de US$ 20 milhões de receita agregada em 12 meses. Contribuições sob termos próprios da Eagle AI Corp. Para um TCC acadêmico sem receita o uso seria permitido, mas a licença é restritiva.
- Maturidade: 1,2 mil estrelas, 40 forks, 77 commits em main, 2 issues e 1 PR abertos. Releases e tags: nenhum listado. Data de criação: não vista na página. Data do último commit: não vista na página (procurei na página principal do repositório). Há CHANGELOG.md, CITATION.cff, SECURITY.md e docs/ (não lidos). Versão visível: imagem 0.1.3 e pin de SGLang em dev.

##### 3 Aplicação ao desenvolvimento com o Claude Code neste projeto

- Não serve. O Claude Code consome modelos hospedados pela Anthropic; não há ponto onde um drafter local acelere a geração dele.
- Custo de instalar e manter: inviável sem GPU NVIDIA/AMD recente e Linux. Nenhum benefício para CLAUDE.md, memória, skills ou subagentes.

##### 4 Aplicação dentro do agente ou do produto

O módulo candidato seria o diagnóstico com o qwen2.5:7b servido pelo Ollama. Conflitos com o contexto:

- CPU sem GPU: o repositório exige GPU (CUDA 13 ou ROCm) e os kernels são de GPU. Conflito direto e bloqueante.
- Ollama como runtime: o pacote só se integra a SGLang, vLLM e TokenSpeed. Trocar de runtime quebraria o harness, o prompt congelado byte a byte e a leitura de probabilidade por token já validada no Ollama.
- Um modelo residente por vez: o EAGLE-4 mantém alvo e drafter residentes. Mesma razão pela qual o projeto adiou a decodificação especulativa.
- 16 GB de RAM e Windows 11 sem administrador: o quick start baixa cerca de 62 GB e pressupõe Linux e Docker/compilador C++; nada disso cabe na máquina-alvo.
- Nada em nuvem e só biblioteca padrão no harness: o pacote traz pilha pesada de dependências (SGLang, PyTorch cu130, índices extras), fora do padrão do harness.
- Prompt congelado e fidelidade: a saída idêntica em temperatura 0 seria um ponto a favor, mas o ganho medido é para lotes e GPU, não para CPU com uma requisição de 7B.
- Licença source-available: exigiria revisão para qualquer redistribuição junto ao produto.

##### 5 Risco, esforço e veredito

- Risco: alto de tempo perdido (hardware inexistente, runtime diferente, licença restritiva, sem releases formais).
- Esforço: não aplicável na máquina atual. Mesmo como estudo teórico, uma sessão de leitura do paper bastaria para citar como trabalho relacionado.
- Veredito Claude Code: não serve, o Claude Code roda modelos hospedados e o repositório só acelera servidores locais com GPU.
- Veredito agente: não serve, exige GPU, SGLang/vLLM e um segundo modelo residente, conflitando com CPU, 16 GB, um modelo por vez e Ollama; vale no máximo como citação de trabalho relacionado sobre decodificação especulativa adiada.

##### 6 Referências ABNT NBR 6023

EAGLE-4 TEAM. **EAGLE-4**: official inference code of EAGLE-4. Disponível em: https://github.com/eagle-hq/eagle-4. Acesso em: 7 nov. 2026.

EAGLE-4 TEAM. **EAGLE-4**: one flexible drafter for all batch sizes and hardware. Preprint, 2026. Disponível em: https://github.com/eagle-hq/eagle-4 (arquivo EAGLE4_Paper.pdf). Acesso em: 7 nov. 2026.

Os artigos EAGLE, EAGLE-2 e EAGLE-3 são citados apenas por nome em CITATION.cff; o README não traz autores, títulos nem URLs, então não os referencio (procurei no README e na página principal).

#### 6.15.13 Repositório gepa-ai/gepa (`pos4-repo-gepa`; 2 fontes com endereço)

*Leitura de:* subagente, em 07/11/2026; arquivo `repo-07-gepa.md` em `5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/`. Interesse declarado pelo Eric: muito alto.

Fontes lidas em 7 nov. 2026: página do repositório no GitHub, README bruto (raw.githubusercontent.com) e resumo do artigo em arxiv.org/abs/2507.19457. Os textos lidos foram tratados como dado.

Resposta curta à pergunta do Eric: o GEPA NÃO é um filtro de respostas. É um otimizador de texto (prompts, código, configurações) que roda offline, por evolução com feedback em texto. Ele melhora o prompt; não inspeciona nem barra a resposta de cada inferência.

##### 1 O que é e como funciona por dentro

GEPA (Genetic-Pareto) otimiza qualquer artefato textual (prompt, código, configuração) contra uma métrica que você define. Entra: um candidato inicial (o prompt atual), um conjunto de treino e outro de validação, uma função avaliadora (que pode devolver também texto de diagnóstico, os "logs acionáveis") e um orçamento (`max_metric_calls`, com exemplos de 100 a 150). Sai: o melhor candidato (`result.best_candidate`), isto é, um texto de prompt melhorado.

O laço: (1) escolhe um candidato da fronteira de Pareto (candidatos que vencem em subconjuntos diferentes de exemplos); (2) roda num minilote e guarda o rastro completo (erros, raciocínio); (3) um LLM de reflexão lê o rastro e diagnostica a falha; (4) o mesmo LLM propõe um prompt novo, levando em conta as lições dos ancestrais; (5) aceita se melhorar e atualiza a fronteira; opcionalmente funde dois candidatos bons. Há dois modelos: o modelo da tarefa (executa o prompt) e o modelo de reflexão (separado, o README dá exemplos com modelos hospedados). O README não fixa quantas chamadas uma rodada custa; só o orçamento total de avaliações. Cada avaliação é uma inferência do modelo da tarefa, mais uma chamada de reflexão por iteração. O README afirma 100 a 500 avaliações, contra 5.000 a 25.000 ou mais do GRPO.

##### 2 Pilha, dependências e exigências

- Python, `pip install gepa`. GPU: não mencionada; o método não precisa de pesos do modelo, funciona com modelos só por API.
- Nuvem e chave de API: os exemplos usam modelos hospedados (OpenAI); o README não lista a configuração de chaves, mas nada impede apontar para um servidor compatível local (isto é inferência minha, não visto no README). Extras opcionais: `gepa[confidence]`, `gepa[langchain]`.
- Modelo forte para refletir: o artigo e o README tratam a reflexão como o ponto central e usam modelos fortes nos exemplos; com um 7B local a qualidade da reflexão não é garantida (inferência, não medido por eles na página lida).
- DSPy: opcional. Existe `dspy.GEPA`, mas roda sozinho por `gepa.optimize` e `optimize_anything`. Integra com MLflow, Opik, Pydantic AI, Google ADK.
- Licença: MIT.
- Maturidade (página do GitHub): 7,3 mil estrelas, 611 forks, 946 commits na main. Releases e Packages vazios na página; versão no PyPI: não vista; data do último commit: não vista; data de criação: não vista (procurado na página do repositório e no README). O artigo foi submetido em 25 jul. 2025 (v1) e revisado em 14 fev. 2026 (v2). Existe também plugin de skill para o Claude Code: `/plugin marketplace add gepa-ai/gepa`, `/plugin install gepa-optimize-anything@gepa`.
- Números do artigo: contra o GRPO (aprendizado por reforço), 6% melhor em média em seis tarefas, até 20% numa tarefa, com até 35 vezes menos rollouts; contra o MIPROv2, mais de 10% melhor, incluindo +12% de acurácia na AIME 2025. Números do README (relatos, não conferidos): GPT-4.1 Mini de 46,6% para 56,6% na AIME 2025; Nubank de 68,88% para 88,89%; NER clínico até +12,5% de F1. Quantas rodadas cada ganho custou: o resumo do artigo não informa; o README dá a ordem de 100 a 500 avaliações.

##### 3 Aplicação ao desenvolvimento com o Claude Code neste projeto

Serve em tese, com ressalvas. O GEPA otimiza texto contra uma métrica; os textos candidatos aqui seriam prompts de subagentes e descrições/corpos de skills. Condição: existir um conjunto de exemplos com métrica automática (por exemplo, "o subagente de verificação de citação acertou X de Y casos conhecidos"). Hoje esses subagentes são avaliados por leitura humana, sem métrica em código, então o primeiro custo é construir o avaliador e o conjunto de treino e validação. Sem isso o GEPA não tem o que otimizar.

Custo: cada avaliação é uma execução de subagente (tokens do Claude), mais chamadas de reflexão; ordem de 100 a 150 avaliações por prompt segundo os exemplos do README. Isso colide com a regra de economia de tokens do projeto ("primeiro a máquina, depois o modelo"), então só vale para um prompt de subagente que rode muitas vezes e tenha gabarito barato. O plugin de skill do próprio repositório existe, mas instalar plugin muda o conjunto de plugins fixado no início da sessão (cache de prefixo), então exigiria decisão do Eric.

##### 4 Aplicação dentro do agente ou do produto

Como filtro de respostas: NÃO serve. O GEPA não valida, não barra e não reescreve a resposta de uma inferência; ele roda antes, offline, e entrega um prompt novo. O filtro das respostas da LLM do projeto continua sendo código (validação por regra, selo de confiança pela probabilidade do rótulo, gatilhos), que é o desenho já adotado. O repositório também lista o adaptador `ConfidenceAdapter`/`gepa[confidence]` (usa `llm-structured-confidence`), que mexe com confiança de saídas estruturadas; li só o nome, sem detalhe, então não afirmo que sirva de filtro. Valeria uma leitura própria antes de descartar.

O que serviria do mesmo repositório: o uso como otimizador offline do texto do prompt, em dois módulos possíveis:
- Prompt de cura (o DSPy para ele já foi adiado): é o candidato natural, porque ainda não está congelado. O GEPA faria o papel que o DSPy faria.
- Prompt do diagnóstico: está congelado byte a byte. Rodar o GEPA nele é possível só como experimento fora da produção; qualquer prompt novo obriga a recalibrar os limiares e repetir as medições.

Restrições do contexto em conflito:
- Prompt congelado: o produto do GEPA é justamente um prompt diferente; adotá-lo no diagnóstico quebra o congelamento e invalida a calibração (limiares e selo).
- Custo por inferência em CPU (50 a 70 s): 100 a 150 avaliações de modelo da tarefa são de 1,5 a 3 horas por rodada só no modelo local, sem contar a reflexão; as 100 a 500 do README chegam a 1,5 a 10 horas. Cada rodada de busca pesa mais que uma bateria inteira.
- Modelo residente único: a tarefa (qwen2.5:7b) e a reflexão precisam de dois modelos. Com um só residente, ou o 7B reflete sobre si mesmo (reflexão fraca, não medida) ou a reflexão vai a um modelo em nuvem, o que viola "nada em nuvem".
- Harness só com biblioteca padrão: o GEPA é uma dependência Python externa (instalável por pip na venv, mas fora do padrão do harness).
- Máquina corporativa sem administrador: pip na venv funciona, mas a política de rede/pacotes não foi verificada.
- Dados: o conjunto de validação do diagnóstico é o gabarito 54/36 da Fase 3; usá-lo para otimizar prompt contamina a medição se não houver partição separada.

##### 5 Risco, esforço e veredito

- Risco: alto para o agente (quebra o congelamento, 1,5 a 10 h por rodada em CPU, reflexão fraca com 7B ou violação de "nada em nuvem", contaminação do gabarito). Médio-baixo para o Claude Code (custo de tokens e de montar a métrica; sem risco ao produto).
- Esforço estimado: Claude Code, 2 a 3 sessões (avaliador com gabarito, conjunto, uma rodada de teste num subagente). Agente, 3 a 4 sessões mais várias horas de máquina para um experimento só no prompt de cura, mais outra bateria completa se o resultado for adotado no diagnóstico.
- Veredito para o Claude Code: opcional e adiável; só vale para um subagente que rode muitas vezes e tenha métrica automática, e não como prioridade antes da Fase 5.
- Veredito para o agente: não é filtro de respostas; descartar para esse fim, e guardar como candidato a substituto do DSPy no prompt de cura, em experimento offline, sem tocar no prompt congelado do diagnóstico.

##### 6 Referências ABNT NBR 6023

GEPA-AI. **GEPA**: optimize prompts, code, and more with AI-powered reflective optimization. Disponível em: https://github.com/gepa-ai/gepa. Acesso em: 7 nov. 2026.

AGRAWAL, Lakshya A. et al. **GEPA**: reflective prompt evolution can outperform reinforcement learning. arXiv:2507.19457, 2025. Disponível em: https://arxiv.org/abs/2507.19457. Acesso em: 7 nov. 2026.

#### 6.15.14 Repositório AgriciDaniel/claude-obsidian (`pos4-repo-claude-obsidian`; 4 fontes com endereço)

*Leitura de:* subagente, em 07/11/2026; arquivo `repo-08-claude-obsidian.md` em `5-metodo-e-ferramental/dados/pesquisa-pos-fase-4/`. Interesse declarado pelo Eric: médio.

Fonte: página do repositório, README bruto e docs/windows-wsl.md, lidos em 7 nov. 2026. A listagem de docs/ mostra 13 arquivos (install-guide, windows-wsl, methodology-modes-guide, retrieval-evaluation, entre outros); só li o windows-wsl.

##### 1 O que é e como funciona por dentro

- É um plugin do Claude Code que trata uma pasta de arquivos Markdown como um "segundo cérebro". O Obsidian é só o visualizador: abre-se a mesma pasta com "Open folder as vault". O README diz que nenhum plugin do Obsidian é necessário.
- O que liga o Claude à pasta são skills (15) e agentes (3, somente leitura) do Claude Code, mais um núcleo de transação que é o único que escreve. Há também uma CLI em Python (`scripts/claude-obsidian.py`).
- Segue o padrão "LLM Wiki" de Karpathy (gist de 4 abr. 2026): fontes brutas imutáveis, uma wiki mantida pelo LLM e um arquivo de esquema com as convenções. Operações: ingest, query, lint.
- Fluxo: a pessoa joga fontes em `inbox/`. O `wiki-ingest` lê, extrai e gera páginas ligadas (fontes, conceitos, entidades, sessões), índices e mapas de conteúdo. Os originais ficam intactos, em cópias endereçadas por conteúdo. `wiki-query` responde a partir das notas, `save` guarda uma boa resposta como nota, `wiki-lint` checa contradições, órfãs e lacunas.
- Escrita segura: o Claude lê cada nota que vai tocar e guarda o hash SHA-256; os ajudantes devolvem rascunhos; tudo é aplicado em uma transação única, com diário de backups e `transaction recover`. Se a nota mudar no meio, a escrita para com conflito.
- O vault é marcado por `.claude-obsidian.json` ou pela variável `CLAUDE_OBSIDIAN_VAULT`. O `wiki-mode` escolhe a organização: genérico (padrão), LYT, PARA ou Zettelkasten. Trocar de modo não move notas antigas.
- Skills de extensão: autoresearch, canvas, defuddle (limpeza de páginas web), wiki-fold, wiki-retrieve, wiki-cli (usa a CLI oficial do Obsidian), obsidian-markdown, obsidian-bases, think.
- A página mostra arquivos de regras para outros hospedeiros (Cursor, Windsurf, Codex, Gemini), instalados por `scripts/setup-multi-agent.sh`.

##### 2 Pilha, dependências e exigências

- Exigências declaradas: Claude Code, Python 3.11 ou mais novo, Obsidian (só para a parte visual) e Bash para os scripts de instalação. Git só para desenvolvimento e checkpoints.
- Node.js e chave de API: o README não diz que sejam necessários (procurei no README bruto e na página). Serviço em nuvem: o vault é local; o conteúdo que o Claude Code lê vai ao Claude, como qualquer arquivo. Pesquisa web, reranking remoto e checkpoints Git pedem aprovação.
- Instalação: `claude plugin marketplace add AgriciDaniel/claude-obsidian` e depois `claude plugin install claude-obsidian@agricidaniel-claude-obsidian`.
- Windows: o docs/windows-wsl.md diz que o Windows nativo (inclusive Git Bash) é somente leitura. Inspeção, simulação e busca funcionam; `transaction apply`, `init`, `adopt`, `migrate` e `mode set` são recusados com `UNSUPPORTED_PLATFORM`. Escrever exige WSL, Linux ou macOS. Os hooks SessionStart e Stop precisam de `python3` no PATH; o instalador do python.org só traz `python.exe`, e sem `python3` os hooks não fazem nada, em silêncio.
- Licença: MIT.
- Maturidade: 16,2 mil estrelas, 1,6 mil forks, 18 issues e 7 pull requests abertos, 351 commits em main, versão 3.0.1 (selo do README). Seção Releases vazia na página. Data do último commit: não visto (a página não mostra datas). Data de criação: não vista. Linguagens: percentual não visto; há Python, scripts Bash e Markdown.

##### 3 Aplicação ao desenvolvimento com o Claude Code neste projeto

- Serve em tese: o Memorial do TCC (decisões, fichas, roadmap, levantamentos) e a biblioteca do TargetERP já são Markdown em pasta, que é exatamente o formato que o plugin espera. O Obsidian abriria essas pastas como vault sem mudar nada, e daria grafo, retroligações e busca para o Eric navegar.
- Obstáculo central: a escrita (ingest, save, init, adopt) só funciona em WSL, Linux ou macOS. Na máquina do Eric (Windows 11 corporativo sem administrador), habilitar WSL exige ativar recursos do Windows e reiniciar, o que normalmente pede administrador (o doc cita prompt elevado para reparo). Sem isso, o plugin é só leitura, ou seja, perde o sentido principal.
- O que o plugin faz de útil já existe aqui: CLAUDE.md, memória em Markdown, fichas, ingestão manual do Memorial e o painel HTML gerado por Python. Instalá-lo duplicaria a memória (um segundo índice, um segundo esquema) e criaria conflito com a regra do projeto de documentação em Markdown com tag de alteração de IA e decisões numeradas.
- Para a biblioteca de 1436 artigos do TargetERP: ela já tem frontmatter e índice JSON lido pelo Claude Code. O `wiki-lint` (órfãs, contradições, lacunas) seria a parte mais aproveitável, mas dá para obter o mesmo com um script local de Python, em linha com a regra "primeiro a máquina, depois o modelo".
- Custo de instalação e manutenção: plugin de terceiros com 15 skills e hooks, versão 3.x ainda em mudança; revisão de segurança antes de rodar em repositório corporativo; manter sincronizado com a atualização do Claude Code. Obsidian sem administrador: não verifiquei na fonte. O README não trata disso; a CLI oficial do Obsidian é opcional. Não afirmo nada além disso.
- Uso viável sem custo: abrir o Memorial no Obsidian só como leitor, se o Eric já tiver o app instalado. Isso não depende do plugin.

##### 4 Aplicação dentro do agente ou do produto

- Não serve. O agente de QA roda offline com Ollama qwen2.5:7b só em CPU, harness em Python com biblioteca padrão. O plugin é um complemento do Claude Code (nuvem), exige Python 3.11 com transações e hooks, e é feito para um humano alimentar uma wiki, não para um laço automático de teste.
- A ideia aproveitável é o formato: notas atômicas pequenas, ligadas por links explícitos, com frontmatter e um índice, mais o ciclo ingest, query e lint (checar órfãs e contradições). A biblioteca de verbetes do agente já é recuperada e validada por código; adicionar campos de ligação entre verbetes (ex.: "relacionado a") e um lint local de verbetes órfãos ou duplicados seria barato e compatível com biblioteca padrão. O modelo de escrita em transação com hash e backup também é uma boa prática para o agente gravar verbetes novos sem corromper a biblioteca, mas é uma ideia, não precisa do plugin.

##### 5 Risco, esforço e veredito

- Risco: médio. Plugin de terceiros popular mas jovem (padrão Karpathy de abr. 2026), com hooks que rodam no início e fim de sessão; escrita bloqueada no Windows nativo; possível duplicação da memória do projeto; dependência de WSL, que o ambiente corporativo pode proibir.
- Esforço: de 1 a 2 sessões só para testar a leitura no Windows nativo (instalar o plugin, rodar `wiki-lint` em modo simulação sobre uma cópia do Memorial); mais 2 a 3 sessões se WSL puder ser habilitado, mais a revisão de segurança. Para o agente: 0 sessões (não aplicar); 1 sessão para um lint de ligações na biblioteca de verbetes, por script próprio.
- Veredito para o Claude Code: não instalar agora; o ganho é pequeno diante do que o CLAUDE.md, a memória e a biblioteca indexada já fazem, e a escrita não roda no Windows sem WSL. Vale só ler o padrão de Karpathy e copiar o lint por script.
- Veredito para o agente: não serve como componente; apenas a ideia de notas ligadas com lint pode inspirar a biblioteca de verbetes.

##### 6 Referências ABNT NBR 6023

AGRICIDANIEL. **claude-obsidian**: self-organizing AI second brain for Obsidian + Claude Code. Disponível em: https://github.com/AgriciDaniel/claude-obsidian. Acesso em: 7 nov. 2026.

KARPATHY, Andrej. **LLM Wiki**. 4 abr. 2026. Disponível em: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f. Acesso em: 7 nov. 2026.

KEPANO. **obsidian-skills**. Disponível em: https://github.com/kepano/obsidian-skills. Acesso em: 7 nov. 2026. (Citada no README; não lida por mim.)

AGRICIDANIEL. **Windows e WSL**. In: claude-obsidian, docs/windows-wsl.md. Disponível em: https://github.com/AgriciDaniel/claude-obsidian/blob/main/docs/windows-wsl.md. Acesso em: 7 nov. 2026.

#### 6.15.15 Mapa adotado, ideia, adiado, descartado

Um veredito por leitura, escrito pelo Claude a partir das leituras e dos critérios do projeto (máquina sem GPU e sem administrador, prompt congelado, biblioteca medida, nenhuma segunda chamada ao modelo). *Adotado* = serve de base a um pacote do plano da Pós-Fase 4; *ideia* = a ferramenta não entra, mas uma ideia dela entra, em código próprio; *adiado* = só com outra máquina ou depois da Fase 5; *descartado* = não serve, com o motivo. Os vereditos foram escritos pelo Claude; o Eric aprovou o plano que os incorpora (ficha 54, decisão 105) e decidiu não testar os dois repositórios marcados como opcionais para o Claude Code (ficha 53, decisão 106).

| Leitura | Para o Claude Code | Para o agente | O que fica | Veredito |
|---|---|---|---|---|
| O hub central à imagem de uma pull request: o modelo de revisão do GitHub e do Azure DevOps (`pos4-revisao-estilo-pr`) | o próprio fluxo de revisão de PR do GitHub e do Azure DevOps que o Eric já usa | base do hub central (pacote Q6): três desfechos da revisão, comentário ancorado com rascunho, threads com estado, iterações numeradas, veredito de cinco valores e a regra de que a IA só comenta | o desenho do hub, com as fontes | **adotado** |
| A barra de progresso para a espera da inferência local (`pos4-indicador-de-progresso`) | n/a | base da barra de progresso (pacote Q4): os limites de 0,1, 1 e 10 s, o indicador de porcentagem, as pausas perto do fim que parecem mais lentas, a barra determinada quando a duração é estimável e os campos de contagem do Ollama | a estimativa em duas fases, com as fontes | **adotado** |
| A árvore de decisão legível para o analista (`pos4-arvore-de-decisao`) | n/a | base da árvore de decisão (pacote Q3): explicação contrastiva com o por que não, o raciocínio escrito rotulado como texto sem garantia, as diretrizes G2 e G11 e os formatos de trilha das ferramentas de observabilidade | um nó por decisão, com a escolhida contra as descartadas e o rótulo de origem de cada afirmação | **adotado** |
| Métricas de prolixidade e objetividade para os filtros determinísticos (`pos4-metricas-de-prolixidade`) | as mesmas métricas valem para o texto que o Claude escreve nos documentos | base dos filtros determinísticos (pacote Q2): o Flesch adaptado ao português, palavras por frase, preenchimento por lista fechada, repetição interna, taxa de compressão, jargão sem expansão, densidade e o tamanho só como covariável | oito métricas em Python puro, com o limiar e a fonte de cada uma | **adotado** |
| Seleção de testes pelo diff do Git e a máquina virtual sugerida pelo orientador (`pos4-impacto-git-e-vm`) | n/a | base da integração com o Git (pacote Q7): seleção segura por arquivo, mapa escrito à mão como o do Azure DevOps, arquivo fora do mapa roda tudo, rodada completa periódica e conferência contra ela; a VM fica registrada como viável só num servidor (decisão 102) | o mapa por frontmatter dos verbetes e as três regras; a resposta ao orientador sobre a VM | **adotado** |
| O projeto contra o syllabus CTFL 4.0 do ISTQB, na tradução do BSTQB (`pos4-syllabus-ctfl`) | n/a | base do relatório por caso no molde do relatório de defeitos (seção 5.5; decisão 104), da terminologia erro, defeito, falha e causa-raiz no TCC e do enquadramento do agente como teste funcional, caixa-preta e automatizado, nos níveis de sistema e de integração de sistema | a referência na bibliografia do TCC e os campos do relatório v3 | **adotado** |
| Repositório enesozturk/dimensional-drawing (`pos4-repo-dimensional-drawing`) | não adotar; no máximo uma figura pontual de um componente, por pedido | não serve: são instruções de desenho de interface, sem relação com o diagnóstico | nada | **descartado** |
| Repositório HKUDS/RAG-Anything (`pos4-repo-rag-anything`) | não adotar | não: exige embedding (descartado por medição, decisão 61), três modelos e serviços na nuvem por padrão | nada | **descartado** |
| Repositório activeing123/mcptoon (`pos4-repo-mcptoon`) | só se o número de servidores MCP crescer (`mcptoon bench` mede o custo fixo por turno) | não: recodificar o contexto do agente reabriria o prompt congelado | trabalho futuro, se os servidores MCP crescerem | **adiado** |
| Repositório Egonex-AI/Understand-Anything (`pos4-repo-understand-anything`) | opcional e de baixo valor: testar uma vez nas cobaias, sem adotar (ficha 53: não testado, decisão 106) | não: depende de um modelo na nuvem e de Node; a ideia do impacto das mudanças por diff vale, feita em Python local, sem modelo | a ideia da seleção por diff do pacote Q7 | **ideia** |
| Repositório sodiumsun/agenttrail (`pos4-repo-agenttrail`) | opcional: só passivo, com Node 20 portátil, sem `init` (ficha 53: não testado, decisão 106) | não como base nem como formato: não registra alternativas nem o pai de cada passo, que a trilha v2 já tem | os rótulos de evidência (reportado, observado, inferido, desconhecido) e o registro datado de decisões, no pacote Q3 | **ideia** |
| Repositório eagle-hq/EAGLE-4 (`pos4-repo-eagle-4`) | não serve | não: exige GPU, SGLang ou vLLM e um segundo modelo residente; nenhuma medida em CPU ou com modelo de 7B | citação de trabalho relacionado no TCC | **descartado** |
| Repositório gepa-ai/gepa (`pos4-repo-gepa`) | opcional e adiável: só para um subagente com métrica automática | não é filtro de respostas: é um otimizador offline de prompt por evolução com reflexão em texto; no máximo um experimento no prompt de cura, no lugar do DSPy adiado, nunca no prompt congelado | candidato futuro para o prompt de cura | **adiado** |
| Repositório AgriciDaniel/claude-obsidian (`pos4-repo-claude-obsidian`) | não instalar: a escrita só roda em WSL, Linux ou macOS | não serve: é um segundo cérebro em Markdown para o Claude Code, sem relação com o diagnóstico | o lint de notas órfãs, por script | **ideia** |
