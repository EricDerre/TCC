<!-- ! Alteração de IA - Revisar: arquivo novo (07/11/2026): leitura feita por um subagente do Claude (modelo Sonnet) sobre o hub central à imagem de uma pull request: o modelo de revisão do GitHub e do Azure DevOps, na rodada 6 da pesquisa (Pós-Fase 4); é um arquivo de dados que ferramentas/integrar_pesquisa_pos_fase4.py lê para montar o levantamento §6.15, e o integrador tira este comentário do texto que entra lá.
     ! Motivo: o Eric pediu em 07/11/2026 a base de pesquisa de cada ponto da Pós-Fase 4 e a validação de oito repositórios do GitHub; a leitura fica versionada como dado para o levantamento ser regerado por script e conferido pelo --check. O texto é o que o subagente escreveu, sem edição, com a marca de confiança que ele deu a cada fonte (aberta e lida; só o resumo de busca; de memória). -->
# Base A: interface de revisão no estilo pull request

Consulta feita em 7 nov. 2026. Todas as páginas abaixo foram abertas (WebFetch), salvo onde indicado.

## a) Modelo de revisão do GitHub e do Azure DevOps

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

## b) Pesquisa sobre revisão de código

**5. BACCHELLI, A.; BIRD, C. Expectations, outcomes, and challenges of modern code review.** In: INTERNATIONAL CONFERENCE ON SOFTWARE ENGINEERING (ICSE), 35., 2013, São Francisco. Anais [...]. IEEE, 2013. p. 712-721. DOI 10.1109/ICSE.2013.6606617. Disponível em: https://2013.icse-conferences.org/content/expectations-outcomes-and-challenges-modern-code-review.html. Acesso em: 7 nov. 2026. (Páginas, DOI e local conferidos só por resultado de busca; a página aberta traz autores e resumo.)
- Estudo na Microsoft (observação, entrevistas, pesquisa, classificação manual de centenas de comentários): achar defeitos é o objetivo declarado, mas a revisão rende menos defeitos que o esperado e mais transferência de conhecimento, consciência do time e soluções alternativas. Entender o código e a mudança é o núcleo, e as ferramentas apoiam mal as estratégias que os revisores usam para isso.
- Aplicação: o hub deve gastar seu desenho em ajudar o analista a entender o diagnóstico (contexto, evidência ao lado), não em checklist de defeitos.

**6. SADOWSKI, C. et al. Modern code review: a case study at Google.** In: ICSE-SEIP, 2018. Disponível em: https://research.google/pubs/modern-code-review-a-case-study-at-google/. Acesso em: 7 nov. 2026.
- 12 entrevistas, pesquisa com 44 respondentes e logs de 9 milhões de mudanças revisadas: revisão leve, baseada em ferramenta. Latência (mediana de aprovação abaixo de 4 horas) vem de fontes secundárias, não confirmada no texto do artigo (conferir o DOI 10.1145/3183519.3183525 antes de citar).
- Aplicação: sustenta que o formato leve e rápido funciona em escala; o hub deve manter o custo por revisão baixo.

## c) Humanos revisando saída de IA

**7. CYNTHIA, S. T. et al. "Go Home Copilot, You're Drunk": understanding developer responses to agent-generated code review comments.** arXiv:2607.21997, 24 jul. 2026 (v2, 29 jul. 2026), preprint. Disponível em: https://arxiv.org/abs/2607.21997. Acesso em: 7 nov. 2026.
- 54.791 comentários de cinco agentes (Copilot, Cursor, Codex, Devin, Claude) em 342 repositórios Python. Sugestão em linha foi o maior preditor de resolução; comentários longos e complexos são menos atendidos; entre 470 discussões não resolvidas, os motivos mais comuns foram sugestão incorreta e decisão de projeto intencional.
- Aplicação: o diagnóstico do agente deve vir curto, ancorado e com correção concreta, e o analista precisa poder registrar "o agente errou" ou "decisão intencional" como desfecho.

## d) Comentários objetivos

**8. GOOGLE. The standard of code review.** Google Engineering Practices. Disponível em: https://google.github.io/eng-practices/review/reviewer/standard.html. Acesso em: 7 nov. 2026.
- Aprovar quando a mudança melhora claramente a saúde do código, mesmo imperfeita; prefixar com "Nit:" o que não é essencial; marcar como opcional o comentário educativo; fatos técnicos pesam mais que preferência.
- Aplicação: dá o critério de aprovação do diagnóstico (correto o bastante e útil) e a distinção bloqueante e não bloqueante.

**9. CONVENTIONAL COMMENTS. Conventional Comments.** Disponível em: https://conventionalcomments.org/. Acesso em: 7 nov. 2026.
- Formato `<rótulo> [decorações]: <assunto>` mais discussão opcional; rótulos praise, nitpick, suggestion, issue, todo, question, thought, chore, note; decorações (blocking), (non-blocking), (if-minor). Justificativa: previsível e legível por máquina.
- Aplicação: rótulos estruturados viram campo do comentário e dão dado analisável para o TCC.

## O que isso fixa para o desenho

Para ser fiel ao modelo de PR, o hub precisa de: (1) região do artefato à vista, com evidência (resposta HTTP, árvore da tela, contrato) ao lado do diagnóstico; (2) comentário ancorado em trecho, com intervalo, mais comentário geral da revisão e opcionalmente por bloco (equivalente a nível de arquivo); (3) threads com estado (ativo, resolvido, não será tratado), rascunho pendente enviado junto com o veredito; (4) veredito de três a cinco valores, em que a IA nunca aprova sozinha; (5) iterações numeradas com "o que mudou desde a sua última revisão" e marca de lido que se invalida; (6) uma sugestão estruturada (causa corrigida) em vez de texto livre; (7) rótulo e decoração de bloqueio no comentário. Não precisa de: diff de linhas (o artefato não é código, basta comparar iterações), branches, merge, políticas de revisores obrigatórios, commit de sugestão, curtidas, nem edição de arquivo. A pesquisa pede foco em compreensão e brevidade, não em volume de comentários.

## O que não achei

Nenhuma medição em interface de revisão de diagnóstico de falha de teste ou de causa raiz por IA; os estudos de revisão de saída de IA (item 7) tratam de código. A página de GitHub aberta não detalha "resolver conversa" nem "alterações desde a última revisão" (só confirmado no Azure DevOps). O artigo de Bacchelli e Bird não foi aberto no PDF (repositório da TU Delft recusou conexão) e o de Sadowski só no resumo; números de latência vêm de fontes secundárias. O item 7 é preprint sem revisão por pares confirmada. Não localizei estudo que meça a eficácia dos Conventional Comments; é guia de comunidade, não pesquisa.
