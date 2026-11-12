<!-- ! Alteração de IA - Revisar: índice DERIVADO, gerado por gerar_relatorio_raciocinio.gerar_v3_da_pasta; não editar à mão.
     ! Motivo: um relatório por caso é ilegível sem uma lista que diga a causa, a confiança e o campo de cada um; os relatórios v2 da corrida ficam como estavam. -->
# Relatórios de defeito (v3) da corrida `fase4_tela_v4`

74 relatórios no molde da seção 5.5 do CTFL 4.0, gerados da trilha `trilha_tela.jsonl` (modo `tela`). Severidade, prioridade e estado estão em branco em todos: são do analista.

| Relatório | Título | Causa respondida | Confiança | Campo | Classe e nível |
|---|---|---|---|---|---|
| [`lex-1@tela`](lex-1@tela.md) | Resposta truncada em `GET /api/produtos` | `resposta_truncada` | o agente está seguro desta causa | nenhum | classe 1, nível 1 |
| [`lex-1@fixture`](lex-1@fixture.md) | Resposta truncada em `GET /api/produtos` | `resposta_truncada` | o agente está seguro desta causa | nenhum | classe 1, nível 1 |
| [`lex-4@tela`](lex-4@tela.md) | Codificação de caracteres incorreta em `GET /api/produtos`, campo `nome` | `codificacao_incorreta` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `nome` | classe 1, nível 2 |
| [`lex-4@fixture`](lex-4@fixture.md) | Codificação de caracteres incorreta em `GET /api/produtos`, campo `nome` | `codificacao_incorreta` | o agente está seguro desta causa | `nome` | classe 1, nível 2 |
| [`sin-4@tela`](sin-4@tela.md) | Coleção no lugar de objeto (ou o inverso) em `GET /api/produtos/1`, campo `id` | `colecao_no_lugar_de_objeto` | o agente está seguro desta causa | `id` | classe 2, nível 1 |
| [`sin-4@fixture`](sin-4@fixture.md) | Coleção no lugar de objeto (ou o inverso) em `GET /api/produtos/1`, campo `id` | `colecao_no_lugar_de_objeto` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `id` | classe 2, nível 1 |
| [`sin-5@tela`](sin-5@tela.md) | Campo ausente em `GET /api/produtos`, campo `resumo` | `campo_ausente` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `resumo` | classe 2, nível 3 |
| [`sin-5@fixture`](sin-5@fixture.md) | Coleção no lugar de objeto (ou o inverso) em `GET /api/produtos` | `colecao_no_lugar_de_objeto` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | nenhum | classe 2, nível 3 |
| [`semt-1@tela`](semt-1@tela.md) | Tipo divergente em `GET /api/produtos`, campo `preco` | `tipo_divergente` | o agente está seguro desta causa | `preco` | classe 3, nível 2 |
| [`semt-1@fixture`](semt-1@fixture.md) | Tipo divergente em `GET /api/produtos`, campo `preco` | `tipo_divergente` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `preco` | classe 3, nível 2 |
| [`tra-1@tela`](tra-1@tela.md) | Escala ou unidade errada em `GET /api/produtos`, campo `preco` | `escala_ou_unidade_errada` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `preco` | classe 4, nível 2 |
| [`tra-1@fixture`](tra-1@fixture.md) | Escala ou unidade errada em `GET /api/produtos`, campo `preco` | `escala_ou_unidade_errada` | o agente está seguro desta causa | `preco` | classe 4, nível 2 |
| [`tra-4@tela`](tra-4@tela.md) | Resposta truncada em `GET /api/produtos?pagina=1`, campo `id` | `resposta_truncada` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | `id` | classe 4, nível 3 |
| [`tra-4@fixture`](tra-4@fixture.md) | Contagem inconsistente em `GET /api/produtos?pagina=1`, campo `total` | `contagem_inconsistente` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `total` | classe 4, nível 3 |
| [`run-1@tela`](run-1@tela.md) | Erro interno do servidor (500) em `GET /api/produtos` | `erro_interno_do_servidor` | o agente está seguro desta causa | nenhum | classe 5, nível 1 |
| [`run-1@fixture`](run-1@fixture.md) | Erro interno do servidor (500) em `GET /api/produtos` | `erro_interno_do_servidor` | o agente tem dúvida entre causas vizinhas; confira antes de agir | nenhum | classe 5, nível 1 |
| [`run-2@tela`](run-2@tela.md) | Tempo de resposta excedido em `GET /api/produtos` | `tempo_de_resposta_excedido` | o agente está seguro desta causa | nenhum | classe 5, nível 1 |
| [`run-2@fixture`](run-2@fixture.md) | Tempo de resposta excedido em `GET /api/produtos` | `tempo_de_resposta_excedido` | o agente está seguro desta causa | nenhum | classe 5, nível 1 |
| [`efe-3@tela`](efe-3@tela.md) | Campo ausente em `GET /api/produtos`, campo `imagem` | `campo_ausente` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `imagem` | classe 6, nível 2 |
| [`efe-3@fixture`](efe-3@fixture.md) | Campo ausente em `GET /api/produtos`, campo `imagem` | `campo_ausente` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | `imagem` | classe 6, nível 2 |
| [`lex-7@tela`](lex-7@tela.md) | Corpo vazio em `GET /api/produtos/1` | `corpo_vazio` | o agente está seguro desta causa | nenhum | classe 1, nível 1 |
| [`lex-7@fixture`](lex-7@fixture.md) | Corpo vazio em `GET /api/produtos/1` | `corpo_vazio` | o agente está seguro desta causa | nenhum | classe 1, nível 1 |
| [`lex-8@tela`](lex-8@tela.md) | Codificação de caracteres incorreta em `GET /api/produtos`, campo `resumo` | `codificacao_incorreta` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `resumo` | classe 1, nível 2 |
| [`lex-8@fixture`](lex-8@fixture.md) | Codificação de caracteres incorreta em `GET /api/produtos` | `codificacao_incorreta` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | nenhum | classe 1, nível 2 |
| [`lex-10@tela`](lex-10@tela.md) | Resposta truncada em `GET /api/produtos` | `resposta_truncada` | o agente está seguro desta causa | nenhum | classe 1, nível 3 |
| [`lex-10@fixture`](lex-10@fixture.md) | Resposta truncada em `GET /api/produtos` | `resposta_truncada` | o agente está seguro desta causa | nenhum | classe 1, nível 3 |
| [`lex-11@tela`](lex-11@tela.md) | Codificação de caracteres incorreta em `GET /api/produtos`, campo `nome` | `codificacao_incorreta` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `nome` | classe 1, nível 3 |
| [`lex-11@fixture`](lex-11@fixture.md) | Codificação de caracteres incorreta em `GET /api/produtos`, campo `nome` | `codificacao_incorreta` | o agente está seguro desta causa | `nome` | classe 1, nível 3 |
| [`sin-11@tela`](sin-11@tela.md) | Estrutura aninhada divergente em `GET /api/produtos`, campo `preco` | `estrutura_aninhada_divergente` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `preco` | classe 2, nível 2 |
| [`sin-11@fixture`](sin-11@fixture.md) | Estrutura aninhada divergente em `GET /api/produtos`, campo `itens` | `estrutura_aninhada_divergente` | o agente está seguro desta causa | `itens` | classe 2, nível 2 |
| [`sin-14@tela`](sin-14@tela.md) | Campo renomeado em `GET /api/produtos`, campo `imagem` | `campo_renomeado` | o agente está seguro desta causa | `imagem` | classe 2, nível 3 |
| [`sin-14@fixture`](sin-14@fixture.md) | Coleção no lugar de objeto (ou o inverso) em `GET /api/produtos`, campo `imagem_url` | `colecao_no_lugar_de_objeto` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | `imagem_url` | classe 2, nível 3 |
| [`semt-8@tela`](semt-8@tela.md) | Nulo inesperado em `GET /api/produtos`, campo `preco` | `nulo_inesperado` | o agente está seguro desta causa | `preco` | classe 3, nível 1 |
| [`semt-8@fixture`](semt-8@fixture.md) | Nulo inesperado em `GET /api/produtos`, campo `preco` | `nulo_inesperado` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `preco` | classe 3, nível 1 |
| [`semt-9@tela`](semt-9@tela.md) | Tipo divergente em `GET /api/produtos`, campo `destaque` | `tipo_divergente` | o agente está seguro desta causa | `destaque` | classe 3, nível 1 |
| [`semt-9@fixture`](semt-9@fixture.md) | Tipo divergente em `GET /api/produtos`, campo `destaque` | `tipo_divergente` | o agente está seguro desta causa | `destaque` | classe 3, nível 1 |
| [`semt-14@tela`](semt-14@tela.md) | Nulo inesperado em `GET /api/produtos`, campo `tipo` | `nulo_inesperado` | o agente está seguro desta causa | `tipo` | classe 3, nível 3 |
| [`semt-14@fixture`](semt-14@fixture.md) | Nulo inesperado em `GET /api/produtos`, campo `tipo` | `nulo_inesperado` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | `tipo` | classe 3, nível 3 |
| [`tra-8@tela`](tra-8@tela.md) | Resposta truncada em `GET /api/produtos?pagina=1`, campo `id` | `resposta_truncada` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | `id` | classe 4, nível 1 |
| [`tra-8@fixture`](tra-8@fixture.md) | Contagem inconsistente em `GET /api/produtos?pagina=1`, campo `total` | `contagem_inconsistente` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `total` | classe 4, nível 1 |
| [`tra-11@tela`](tra-11@tela.md) | Contagem inconsistente em `GET /api/produtos?pagina=2` | `contagem_inconsistente` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | nenhum | classe 4, nível 2 |
| [`tra-11@fixture`](tra-11@fixture.md) | Contagem inconsistente em `GET /api/produtos?pagina=2`, campo `itens` | `contagem_inconsistente` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `itens` | classe 4, nível 2 |
| [`run-9@tela`](run-9@tela.md) | Tempo de resposta excedido em `GET /api/produtos` | `tempo_de_resposta_excedido` | o agente está seguro desta causa | nenhum | classe 5, nível 2 |
| [`run-9@fixture`](run-9@fixture.md) | Tempo de resposta excedido em `GET /api/produtos` | `tempo_de_resposta_excedido` | o agente está seguro desta causa | nenhum | classe 5, nível 2 |
| [`lex-16@tela`](lex-16@tela.md) | Resposta truncada em `GET /api/produtos/1 (modo malformed_json ligado)` | `resposta_truncada` | o agente está seguro desta causa | nenhum | classe 1, nível 1 |
| [`lex-16@fixture`](lex-16@fixture.md) | Resposta truncada em `GET /api/produtos/1 (modo malformed_json ligado)` | `resposta_truncada` | o agente está seguro desta causa | nenhum | classe 1, nível 1 |
| [`lex-18@tela`](lex-18@tela.md) | Codificação de caracteres incorreta em `GET /api/produtos`, campo `resumo` | `codificacao_incorreta` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `resumo` | classe 1, nível 2 |
| [`lex-18@fixture`](lex-18@fixture.md) | Valor fora do domínio em `GET /api/produtos`, campo `resumo` | `valor_fora_do_dominio` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | `resumo` | classe 1, nível 2 |
| [`sin-16@tela`](sin-16@tela.md) | Campo ausente em `GET /api/produtos/1 (modo field_missing, campo destaque)`, campo `destaque` | `campo_ausente` | o agente está seguro desta causa | `destaque` | classe 2, nível 1 |
| [`sin-16@fixture`](sin-16@fixture.md) | Campo ausente em `GET /api/produtos/1 (modo field_missing, campo destaque)`, campo `destaque` | `campo_ausente` | o agente está seguro desta causa | `destaque` | classe 2, nível 1 |
| [`sin-20@tela`](sin-20@tela.md) | Campo ausente em `GET /api/produtos`, campo `id` | `campo_ausente` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `id` | classe 2, nível 3 |
| [`sin-20@fixture`](sin-20@fixture.md) | Campo ausente em `GET /api/produtos`, campo `id` | `campo_ausente` | o agente está seguro desta causa | `id` | classe 2, nível 3 |
| [`sin-21@tela`](sin-21@tela.md) | Estrutura aninhada divergente em `GET /api/produtos`, campo `tipo` | `estrutura_aninhada_divergente` | o agente está seguro desta causa | `tipo` | classe 2, nível 3 |
| [`sin-21@fixture`](sin-21@fixture.md) | Estrutura aninhada divergente em `GET /api/produtos`, campo `tipo` | `estrutura_aninhada_divergente` | o agente está seguro desta causa | `tipo` | classe 2, nível 3 |
| [`semt-16@tela`](semt-16@tela.md) | Tipo divergente em `GET /api/produtos`, campo `tipo` | `tipo_divergente` | o agente está seguro desta causa | `tipo` | classe 3, nível 1 |
| [`semt-16@fixture`](semt-16@fixture.md) | Tipo divergente em `GET /api/produtos`, campo `tipo` | `tipo_divergente` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `tipo` | classe 3, nível 1 |
| [`semt-17@tela`](semt-17@tela.md) | Nulo inesperado em `GET /api/produtos`, campo `id` | `nulo_inesperado` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `id` | classe 3, nível 1 |
| [`semt-17@fixture`](semt-17@fixture.md) | Nulo inesperado em `GET /api/produtos`, campo `id` | `nulo_inesperado` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `id` | classe 3, nível 1 |
| [`semt-20@tela`](semt-20@tela.md) | Valor fora do domínio em `GET /api/produtos`, campo `preco` | `valor_fora_do_dominio` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | `preco` | classe 3, nível 3 |
| [`semt-20@fixture`](semt-20@fixture.md) | Tipo divergente em `GET /api/produtos`, campo `preco` | `tipo_divergente` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | `preco` | classe 3, nível 3 |
| [`semt-21@tela`](semt-21@tela.md) | Campo renomeado em `GET /api/produtos`, campo `nome` | `campo_renomeado` | o agente está seguro desta causa | `nome` | classe 3, nível 3 |
| [`semt-21@fixture`](semt-21@fixture.md) | Campo ausente em `GET /api/produtos`, campo `nome` | `campo_ausente` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `nome` | classe 3, nível 3 |
| [`tra-17@tela`](tra-17@tela.md) | Chave de junção errada em `GET /api/produtos`, campo `tipo` | `chave_de_juncao_errada` | o agente está seguro desta causa | `tipo` | classe 4, nível 1 |
| [`tra-17@fixture`](tra-17@fixture.md) | Tipo divergente em `GET /api/produtos`, campo `tipo` | `tipo_divergente` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `tipo` | classe 4, nível 1 |
| [`tra-19@tela`](tra-19@tela.md) | Escala ou unidade errada em `GET /api/produtos`, campo `preco` | `escala_ou_unidade_errada` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `preco` | classe 4, nível 2 |
| [`tra-19@fixture`](tra-19@fixture.md) | Escala ou unidade errada em `GET /api/produtos`, campo `preco` | `escala_ou_unidade_errada` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | `preco` | classe 4, nível 2 |
| [`tra-20@tela`](tra-20@tela.md) | Chave de junção errada em `GET /api/produtos`, campo `tipo` | `chave_de_juncao_errada` | o agente está seguro desta causa | `tipo` | classe 4, nível 3 |
| [`tra-20@fixture`](tra-20@fixture.md) | Chave de junção errada em `GET /api/produtos`, campo `tipo` | `chave_de_juncao_errada` | o agente está seguro desta causa | `tipo` | classe 4, nível 3 |
| [`tra-21@tela`](tra-21@tela.md) | Resposta truncada em `GET /api/produtos`, campo `id` | `resposta_truncada` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | `id` | classe 4, nível 3 |
| [`tra-21@fixture`](tra-21@fixture.md) | Contagem inconsistente em `GET /api/produtos` | `contagem_inconsistente` | o agente tem dúvida entre causas vizinhas; confira antes de agir | nenhum | classe 4, nível 3 |
| [`run-19@tela`](run-19@tela.md) | Tempo de resposta excedido em `GET /api/produtos/1 (clique em 'Saiba Mais...')` | `tempo_de_resposta_excedido` | o agente tem dúvida entre causas vizinhas; confira antes de agir | nenhum | classe 5, nível 2 |
| [`run-19@fixture`](run-19@fixture.md) | Tempo de resposta excedido em `GET /api/produtos/1 (clique em 'Saiba Mais...')` | `tempo_de_resposta_excedido` | o agente está seguro desta causa | nenhum | classe 5, nível 2 |
| [`run-21@tela`](run-21@tela.md) | Registro duplicado em `GET /api/produtos` | `registro_duplicado` | o agente está seguro desta causa | nenhum | classe 5, nível 3 |
| [`run-21@fixture`](run-21@fixture.md) | Registro duplicado em `GET /api/produtos`, campo `id` | `registro_duplicado` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `id` | classe 5, nível 3 |
