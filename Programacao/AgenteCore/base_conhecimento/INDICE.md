<!-- ! Alteração de IA - Revisar: índice humano da biblioteca, GERADO por
     validar_banco.py --indice a partir do frontmatter dos verbetes; não editar à mão.
     ! Motivo: o modelo recebe os verbetes renderizados, não este arquivo — ele existe
     para quem revisa a biblioteca enxergar cobertura e tipos num lugar só. -->

# Índice da biblioteca base

36 verbetes. 36 verbetes {'contratos': 2, 'defeitos_conhecidos': 3, 'erros': 24, 'falhas_injetadas': 1, 'negocio': 6}; biblioteca inteira: 17113 caracteres ≈ 6582 tokens

| Pasta | Id | Título | Tipo | Causas |
|---|---|---|---|---|
| contratos | `contrato-pedido` | Contrato de /api/pedidos | contrato | formato_de_data_divergente, valor_fora_do_dominio, recurso_inexistente, campo_ausente |
| contratos | `contrato-produto` | Contrato de /api/produtos | contrato | campo_ausente, campo_renomeado, colecao_no_lugar_de_objeto, tipo_divergente, recurso_inexistente |
| defeitos_conhecidos | `ancora-saiba-mais` | Link "Saiba Mais..." abre produto vazio | defeito_conhecido | localizador_quebrado, recurso_inexistente, estado_da_tela_divergente |
| defeitos_conhecidos | `consultas-sem-checagem` | Consultas sem checagem e cancelamento sem dono | defeito_conhecido | dado_desatualizado, estado_da_tela_divergente, registro_duplicado |
| defeitos_conhecidos | `senha-sem-hash` | Senha em texto puro, MD5 na edição, sem hash no login | defeito_conhecido | estado_da_tela_divergente, valor_fora_do_dominio |
| erros | `campo_ausente` | Campo ausente | erro | campo_ausente |
| erros | `campo_renomeado` | Campo renomeado | erro | campo_renomeado |
| erros | `chave_de_juncao_errada` | Chave de junção errada | erro | chave_de_juncao_errada |
| erros | `codificacao_incorreta` | Codificação de caracteres incorreta | erro | codificacao_incorreta |
| erros | `colecao_no_lugar_de_objeto` | Coleção no lugar de objeto (ou o inverso) | erro | colecao_no_lugar_de_objeto |
| erros | `contagem_inconsistente` | Contagem inconsistente | erro | contagem_inconsistente |
| erros | `corpo_nao_e_json` | Corpo não é JSON | erro | corpo_nao_e_json |
| erros | `corpo_vazio` | Corpo vazio | erro | corpo_vazio |
| erros | `dado_desatualizado` | Dado desatualizado (cache) | erro | dado_desatualizado |
| erros | `erro_interno_do_servidor` | Erro interno do servidor (500) | erro | erro_interno_do_servidor |
| erros | `escala_ou_unidade_errada` | Escala ou unidade errada | erro | escala_ou_unidade_errada |
| erros | `estado_da_tela_divergente` | Estado da tela divergente da resposta | erro | estado_da_tela_divergente |
| erros | `estrutura_aninhada_divergente` | Estrutura aninhada divergente | erro | estrutura_aninhada_divergente |
| erros | `formato_de_data_divergente` | Formato de data divergente | erro | formato_de_data_divergente |
| erros | `limite_de_requisicoes` | Limite de requisições (429) | erro | limite_de_requisicoes |
| erros | `localizador_quebrado` | Localizador (seletor) quebrado | erro | localizador_quebrado |
| erros | `mensagens-de-erro-do-codigo` | Índice de mensagens literais do código | funcionamento | recurso_inexistente, erro_interno_do_servidor, corpo_nao_e_json, corpo_vazio, estado_da_tela_divergente |
| erros | `nulo_inesperado` | Nulo inesperado | erro | nulo_inesperado |
| erros | `recurso_inexistente` | Recurso inexistente (404 e vizinhos) | erro | recurso_inexistente |
| erros | `registro_duplicado` | Registro duplicado | erro | registro_duplicado |
| erros | `resposta_truncada` | Resposta truncada | erro | resposta_truncada |
| erros | `tempo_de_resposta_excedido` | Tempo de resposta excedido | erro | tempo_de_resposta_excedido |
| erros | `tipo_divergente` | Tipo divergente | erro | tipo_divergente |
| erros | `valor_fora_do_dominio` | Valor fora do domínio | erro | valor_fora_do_dominio |
| falhas_injetadas | `modos-de-injecao` | Injeção de falhas da CobaiaAPI | funcionamento | erro_interno_do_servidor, tempo_de_resposta_excedido, tipo_divergente, campo_ausente, campo_renomeado, resposta_truncada |
| negocio | `entidade-produto` | Produto e sua categoria | funcionamento | chave_de_juncao_errada, escala_ou_unidade_errada, tipo_divergente |
| negocio | `fluxo-reserva-e-cancelamento` | Fluxo de reservar e cancelar | regra | valor_fora_do_dominio, dado_desatualizado, estado_da_tela_divergente |
| negocio | `limites-do-sistema` | O que o sistema não faz | limite | valor_fora_do_dominio, campo_ausente, tipo_divergente, dado_desatualizado |
| negocio | `pagina-produtos-api` | Aba "Produtos (API)", a fronteira JSON | funcionamento | estado_da_tela_divergente, localizador_quebrado, corpo_vazio, tipo_divergente |
| negocio | `pedido-reserva` | Reserva de mesa (pedido) | funcionamento | valor_fora_do_dominio, nulo_inesperado, chave_de_juncao_errada |
| negocio | `usuario-e-login` | Usuário, níveis e login | funcionamento | chave_de_juncao_errada, nulo_inesperado |
