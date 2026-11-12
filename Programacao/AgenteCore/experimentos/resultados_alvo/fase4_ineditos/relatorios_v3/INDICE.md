<!-- ! Alteração de IA - Revisar: índice DERIVADO, gerado por gerar_relatorio_raciocinio.gerar_v3_da_pasta; não editar à mão.
     ! Motivo: um relatório por caso é ilegível sem uma lista que diga a causa, a confiança e o campo de cada um; os relatórios v2 da corrida ficam como estavam. -->
# Relatórios de defeito (v3) da corrida `fase4_ineditos`

36 relatórios no molde da seção 5.5 do CTFL 4.0, gerados da trilha `trilha_ineditos.jsonl` (modo `ineditos`). Severidade, prioridade e estado estão em branco em todos: são do analista.

| Relatório | Título | Causa respondida | Confiança | Campo | Classe e nível |
|---|---|---|---|---|---|
| [`lex-22`](lex-22.md) | Corpo não é JSON em `GET /api/produtos` | `corpo_nao_e_json` | o agente tem dúvida entre causas vizinhas; confira antes de agir | nenhum | classe 1, nível 1 |
| [`lex-23`](lex-23.md) | Corpo vazio em `GET /api/produtos/6` | `corpo_vazio` | o agente tem dúvida entre causas vizinhas; confira antes de agir | nenhum | classe 1, nível 1 |
| [`lex-24`](lex-24.md) | Codificação de caracteres incorreta em `GET /api/produtos/14`, campo `resumo` | `codificacao_incorreta` | o agente está seguro desta causa | `resumo` | classe 1, nível 2 |
| [`lex-25`](lex-25.md) | Codificação de caracteres incorreta em `GET /api/produtos`, campo `nome` | `codificacao_incorreta` | o agente está seguro desta causa | `nome` | classe 1, nível 2 |
| [`lex-26`](lex-26.md) | Codificação de caracteres incorreta em `GET /api/produtos/11`, campo `nome` | `codificacao_incorreta` | o agente está seguro desta causa | `nome` | classe 1, nível 3 |
| [`lex-27`](lex-27.md) | Codificação de caracteres incorreta em `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 3, "data_pedido": "2026-12-05"})`, campo `status` | `codificacao_incorreta` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | `status` | classe 1, nível 3 |
| [`sin-22`](sin-22.md) | Campo ausente em `GET /api/produtos`, campo `nome` | `campo_ausente` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `nome` | classe 2, nível 1 |
| [`sin-23`](sin-23.md) | Campo renomeado em `GET /api/produtos/10`, campo `resumo` | `campo_renomeado` | o agente está seguro desta causa | `resumo` | classe 2, nível 1 |
| [`sin-24`](sin-24.md) | Estrutura aninhada divergente em `GET /api/produtos`, campo `tipo` | `estrutura_aninhada_divergente` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | `tipo` | classe 2, nível 2 |
| [`sin-25`](sin-25.md) | Coleção no lugar de objeto (ou o inverso) em `GET /api/produtos/4`, campo `id` | `colecao_no_lugar_de_objeto` | o agente está seguro desta causa | `id` | classe 2, nível 2 |
| [`sin-26`](sin-26.md) | Resposta truncada em `GET /api/produtos`, campo `preco` | `resposta_truncada` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `preco` | classe 2, nível 3 |
| [`sin-27`](sin-27.md) | Campo renomeado em `GET /api/produtos`, campo `imagem_v2` | `campo_renomeado` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | `imagem_v2` | classe 2, nível 3 |
| [`semt-22`](semt-22.md) | Nulo inesperado em `GET /api/produtos`, campo `preco` | `nulo_inesperado` | o agente está seguro desta causa | `preco` | classe 3, nível 1 |
| [`semt-23`](semt-23.md) | Tipo divergente em `GET /api/produtos`, campo `preco` | `tipo_divergente` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `preco` | classe 3, nível 1 |
| [`semt-24`](semt-24.md) | Tipo divergente em `GET /api/produtos`, campo `destaque` | `tipo_divergente` | o agente está seguro desta causa | `destaque` | classe 3, nível 2 |
| [`semt-25`](semt-25.md) | Formato de data divergente em `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 6, "data_pedido": "2026-12-20"})`, campo `data_pedido` | `formato_de_data_divergente` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `data_pedido` | classe 3, nível 2 |
| [`semt-26`](semt-26.md) | Nulo inesperado em `GET /api/produtos/12`, campo `resumo` | `nulo_inesperado` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `resumo` | classe 3, nível 3 |
| [`semt-27`](semt-27.md) | Coleção no lugar de objeto (ou o inverso) em `GET /api/produtos`, campo `id` | `colecao_no_lugar_de_objeto` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | `id` | classe 3, nível 3 |
| [`tra-22`](tra-22.md) | Tipo divergente em `GET /api/produtos`, campo `preco` | `tipo_divergente` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | `preco` | classe 4, nível 1 |
| [`tra-23`](tra-23.md) | Valor fora do domínio em `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 4, "data_pedido": "2026-12-19"})`, campo `pessoas` | `valor_fora_do_dominio` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | `pessoas` | classe 4, nível 1 |
| [`tra-24`](tra-24.md) | Chave de junção errada em `GET /api/produtos`, campo `tipo` | `chave_de_juncao_errada` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `tipo` | classe 4, nível 2 |
| [`tra-25`](tra-25.md) | Resposta truncada em `GET /api/produtos` | `resposta_truncada` | o agente está seguro desta causa | nenhum | classe 4, nível 2 |
| [`tra-26`](tra-26.md) | Coleção no lugar de objeto (ou o inverso) em `GET /api/produtos`, campo `id` | `colecao_no_lugar_de_objeto` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `id` | classe 4, nível 3 |
| [`tra-27`](tra-27.md) | Tipo divergente em `GET /api/produtos/2`, campo `preco` | `tipo_divergente` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `preco` | classe 4, nível 3 |
| [`run-22`](run-22.md) | Limite de requisições (429) em `GET /api/produtos` | `limite_de_requisicoes` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | nenhum | classe 5, nível 1 |
| [`run-23`](run-23.md) | Recurso inexistente (404 e vizinhos) em `GET /api/produtos/5`, campo `id` | `recurso_inexistente` | o agente está seguro desta causa | `id` | classe 5, nível 1 |
| [`run-24`](run-24.md) | Registro duplicado em `GET /api/produtos`, campo `id` | `registro_duplicado` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `id` | classe 5, nível 2 |
| [`run-25`](run-25.md) | Tempo de resposta excedido em `GET /api/produtos/7` | `tempo_de_resposta_excedido` | o agente tem dúvida entre causas vizinhas; confira antes de agir | nenhum | classe 5, nível 2 |
| [`run-26`](run-26.md) | Registro duplicado em `GET /api/pedidos?login=11122233344` | `registro_duplicado` | o agente não está seguro desta causa; trate como hipótese e confira antes de agir | nenhum | classe 5, nível 3 |
| [`run-27`](run-27.md) | Registro duplicado em `GET /api/pedidos?login=11122233344` | `registro_duplicado` | o agente está seguro desta causa | nenhum | classe 5, nível 3 |
| [`efe-22`](efe-22.md) | Localizador (seletor) quebrado em `GET /api/produtos` | `localizador_quebrado` | o agente está seguro desta causa | nenhum | classe 6, nível 1 |
| [`efe-23`](efe-23.md) | Localizador (seletor) quebrado em `GET /api/produtos` | `localizador_quebrado` | o agente está seguro desta causa | nenhum | classe 6, nível 1 |
| [`efe-24`](efe-24.md) | Localizador (seletor) quebrado em `GET /api/produtos` | `localizador_quebrado` | o agente está seguro desta causa | nenhum | classe 6, nível 2 |
| [`efe-25`](efe-25.md) | Localizador (seletor) quebrado em `GET /api/produtos/3` | `localizador_quebrado` | o agente tem dúvida entre causas vizinhas; confira antes de agir | nenhum | classe 6, nível 2 |
| [`efe-26`](efe-26.md) | Coleção no lugar de objeto (ou o inverso) em `GET /api/produtos/9`, campo `id` | `colecao_no_lugar_de_objeto` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `id` | classe 6, nível 3 |
| [`efe-27`](efe-27.md) | Dado desatualizado (cache) em `GET /api/produtos/2`, campo `preco` | `dado_desatualizado` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `preco` | classe 6, nível 3 |
