<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase4.py a partir de reproducao.jsonl e fora.json da corrida (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Reprodução dos casos na tela (corrida 17), gerada em 2026-10-26

Um caso reproduz na tela quando a chamada à CobaiaAPI sai do normal (status, corpo, contrato ou tempo acima do orçamento) ou quando uma conferência do roteiro falha (regra R1 do plano aprovado). Os casos fora são os de rota sem página (pedidos), os de causa sem modo de injeção e os de quebra de localizador, que o harness arma (ficha 29).


<!-- tabela:tb_f4_reproducao_resumo -->
| Casos de avaliação | Com tela e modo | Reproduzem na tela | Fora (sem tela, sem modo ou pelo harness) | Reproduzem (% dos casos) | Reproduzem (% dos com tela) | Roteiro falhou | Com erro do harness |
|---|---|---|---|---|---|---|---|
| 72 | 37 | 37 | 35 | 51,4 | 100,0 | 12 | 0 |
<!-- /tabela:tb_f4_reproducao_resumo -->

<!-- tabela:tb_f4_reproducao_por_classe -->
| Classe | Casos | Com tela e modo | Reproduzem | Fora | Reproduzem (%) |
|---|---|---|---|---|---|
| 1 | 12 | 8 | 8 | 4 | 66,7 |
| 2 | 12 | 7 | 7 | 5 | 58,3 |
| 3 | 12 | 8 | 8 | 4 | 66,7 |
| 4 | 12 | 8 | 8 | 4 | 66,7 |
| 5 | 12 | 5 | 5 | 7 | 41,7 |
| 6 | 12 | 1 | 1 | 11 | 8,3 |
<!-- /tabela:tb_f4_reproducao_por_classe -->

<!-- tabela:tb_f4_reproducao_por_nivel -->
| Nível | Casos | Com tela e modo | Reproduzem | Fora | Reproduzem (%) |
|---|---|---|---|---|---|
| 1 | 24 | 13 | 13 | 11 | 54,2 |
| 2 | 24 | 11 | 11 | 13 | 45,8 |
| 3 | 24 | 13 | 13 | 11 | 54,2 |
<!-- /tabela:tb_f4_reproducao_por_nivel -->

<!-- tabela:tb_f4_reproducao_por_modo -->
| Modo de injeção | Casos | Reproduzem | Motivos registrados |
|---|---|---|---|
| `chave_de_juncao_errada` | 2 | 2 | corpo diferente da referência em modo normal |
| `codificacao_incorreta` | 4 | 4 | corpo diferente da referência em modo normal; árvore diferente da referência: 4 linha(s) a menos e 4 a mais; corpo diferente da referência em modo normal; árvore diferente da referência: 6 linha(s) a menos e 6 a mais |
| `colecao_no_lugar_de_objeto` | 1 | 1 | diff do contrato: forma_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 2 linha(s) a menos e 2 a mais |
| `contagem_inconsistente` | 4 | 4 | corpo diferente da referência em modo normal; árvore diferente da referência: 10 linha(s) a menos e 0 a mais; conferência 'grid com 14 cartões' falhou |
| `corpo_vazio` | 1 | 1 | corpo vazio; árvore diferente da referência: 144 linha(s) a menos e 1 a mais; conferência 'grid carregado antes do detalhe' falhou |
| `error_500` | 1 | 1 | status 500; diff do contrato: ausente, forma_diferente, inesperado; corpo diferente da referência em modo normal; árvore diferente da referência: 140 linha(s) a menos e 1 a mais; conferência 'grid com 14 cartões' falhou |
| `escala_ou_unidade_errada` | 2 | 2 | corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais |
| `estrutura_aninhada_divergente` | 2 | 2 | diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais; diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais; conferência 'preço do primeiro cartão' falhou |
| `field_missing` | 4 | 4 | diff do contrato: ausente; corpo diferente da referência em modo normal; diff do contrato: ausente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 0 a mais; diff do contrato: ausente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais |
| `field_renamed` | 1 | 1 | diff do contrato: renomeado; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 0 a mais |
| `latency` | 3 | 3 | tempo de resposta 2013 ms acima do orçamento de 1000 ms; tempo de resposta 28024 ms acima do orçamento de 1000 ms; tempo de resposta 28028 ms acima do orçamento de 1000 ms |
| `malformed_json` | 3 | 3 | corpo truncado; corpo diferente da referência em modo normal; árvore diferente da referência: 140 linha(s) a menos e 1 a mais; conferência 'grid com 14 cartões' falhou; corpo truncado; árvore diferente da referência: 144 linha(s) a menos e 1 a mais; conferência 'grid carregado antes do detalhe' falhou |
| `nulo_inesperado` | 3 | 3 | diff do contrato: nulo_inesperado; corpo diferente da referência em modo normal; diff do contrato: nulo_inesperado; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais |
| `registro_duplicado` | 1 | 1 | corpo diferente da referência em modo normal; árvore diferente da referência: 0 linha(s) a menos e 10 a mais; conferência 'grid com 14 cartões' falhou |
| `type_drift` | 2 | 2 | diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais |
| `valor_fora_do_dominio` | 3 | 3 | corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais; conferência 'preço do primeiro cartão' falhou; corpo diferente da referência em modo normal; árvore diferente da referência: 28 linha(s) a menos e 28 a mais; diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais |
<!-- /tabela:tb_f4_reproducao_por_modo -->

<!-- tabela:tb_f4_reproducao_custo -->
| Tempo por cenário (mediana, s) | Tempo por cenário (máximo, s) | Tempo total dos cenários (s) | Tempo da chamada à API (mediana, ms) | Árvore antes da poda (mediana, nós) | Árvore depois (mediana, linhas) | Corpo HTTP (mediana, caracteres) | Caso ao vivo (mediana, caracteres) |
|---|---|---|---|---|---|---|---|
| 0,3 | 31,0 | 97,6 | 19,3 | 193 | 39 | 2068 | 2603 |
<!-- /tabela:tb_f4_reproducao_custo -->

<!-- tabela:tb_f4_reproducao_casos -->
| Caso | Classe | Nível | Causa | Modo | Campo | Cenário | Reproduz | Motivo | Status | Segundos |
|---|---|---|---|---|---|---|---|---|---|---|
| `lex-1` | 1 | 1 | `resposta_truncada` | `malformed_json` |  | api-catalogo | sim | corpo truncado; corpo diferente da referência em modo normal; árvore diferente da referência: 140 linha(s) a menos e 1 a mais; conferência 'grid com 14 cartões' falhou | 200 | 0,2 |
| `lex-4` | 1 | 2 | `codificacao_incorreta` | `codificacao_incorreta` | `nome` | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 6 linha(s) a menos e 6 a mais | 200 | 0,3 |
| `sin-4` | 2 | 1 | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` |  | api-detalhe | sim | diff do contrato: forma_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 2 linha(s) a menos e 2 a mais | 200 | 0,5 |
| `sin-5` | 2 | 3 | `campo_ausente` | `field_missing` | `resumo` | api-catalogo | sim | diff do contrato: ausente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,4 |
| `semt-1` | 3 | 2 | `tipo_divergente` | `type_drift` | `preco` | api-catalogo | sim | diff do contrato: tipo_diferente; corpo diferente da referência em modo normal | 200 | 0,5 |
| `tra-1` | 4 | 2 | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | `preco` | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,3 |
| `tra-4` | 4 | 3 | `contagem_inconsistente` | `contagem_inconsistente` |  | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 10 linha(s) a menos e 0 a mais; conferência 'grid com 14 cartões' falhou | 200 | 0,3 |
| `run-1` | 5 | 1 | `erro_interno_do_servidor` | `error_500` |  | api-catalogo | sim | status 500; diff do contrato: ausente, forma_diferente, inesperado; corpo diferente da referência em modo normal; árvore diferente da referência: 140 linha(s) a menos e 1 a mais; conferência 'grid com 14 cartões' falhou | 500 | 0,2 |
| `run-2` | 5 | 1 | `tempo_de_resposta_excedido` | `latency` |  | api-catalogo | sim | tempo de resposta 28024 ms acima do orçamento de 1000 ms | 200 | 28,3 |
| `efe-3` | 6 | 2 | `campo_ausente` | `field_missing` | `imagem` | api-catalogo | sim | diff do contrato: ausente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 0 a mais | 200 | 0,2 |
| `lex-7` | 1 | 1 | `corpo_vazio` | `corpo_vazio` |  | api-detalhe | sim | corpo vazio; árvore diferente da referência: 144 linha(s) a menos e 1 a mais; conferência 'grid carregado antes do detalhe' falhou | 200 | 0,2 |
| `lex-8` | 1 | 2 | `codificacao_incorreta` | `codificacao_incorreta` | `resumo` | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 4 linha(s) a menos e 4 a mais | 200 | 0,3 |
| `lex-10` | 1 | 3 | `resposta_truncada` | `malformed_json` |  | api-catalogo | sim | corpo truncado; corpo diferente da referência em modo normal; árvore diferente da referência: 140 linha(s) a menos e 1 a mais; conferência 'grid com 14 cartões' falhou | 200 | 0,2 |
| `lex-11` | 1 | 3 | `codificacao_incorreta` | `codificacao_incorreta` | `nome` | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 6 linha(s) a menos e 6 a mais | 200 | 0,3 |
| `sin-11` | 2 | 2 | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` |  | api-catalogo | sim | diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais; conferência 'preço do primeiro cartão' falhou | 200 | 0,2 |
| `sin-14` | 2 | 3 | `campo_renomeado` | `field_renamed` | `imagem` | api-catalogo | sim | diff do contrato: renomeado; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 0 a mais | 200 | 0,2 |
| `semt-8` | 3 | 1 | `nulo_inesperado` | `nulo_inesperado` | `preco` | api-catalogo | sim | diff do contrato: nulo_inesperado; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,2 |
| `semt-9` | 3 | 1 | `valor_fora_do_dominio` | `valor_fora_do_dominio` | `destaque` | api-catalogo | sim | diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,3 |
| `semt-14` | 3 | 3 | `nulo_inesperado` | `nulo_inesperado` | `tipo` | api-catalogo | sim | diff do contrato: nulo_inesperado; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,3 |
| `tra-8` | 4 | 1 | `contagem_inconsistente` | `contagem_inconsistente` |  | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 10 linha(s) a menos e 0 a mais; conferência 'grid com 14 cartões' falhou | 200 | 0,3 |
| `tra-11` | 4 | 2 | `contagem_inconsistente` | `contagem_inconsistente` |  | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 10 linha(s) a menos e 0 a mais; conferência 'grid com 14 cartões' falhou | 200 | 0,2 |
| `run-9` | 5 | 2 | `tempo_de_resposta_excedido` | `latency` |  | api-catalogo | sim | tempo de resposta 28028 ms acima do orçamento de 1000 ms | 200 | 28,7 |
| `lex-16` | 1 | 1 | `resposta_truncada` | `malformed_json` |  | api-detalhe | sim | corpo truncado; árvore diferente da referência: 144 linha(s) a menos e 1 a mais; conferência 'grid carregado antes do detalhe' falhou | 200 | 0,2 |
| `lex-18` | 1 | 2 | `codificacao_incorreta` | `codificacao_incorreta` | `resumo` | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 4 linha(s) a menos e 4 a mais | 200 | 0,3 |
| `sin-16` | 2 | 1 | `campo_ausente` | `field_missing` | `destaque` | api-detalhe | sim | diff do contrato: ausente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,6 |
| `sin-20` | 2 | 3 | `campo_ausente` | `field_missing` | `id` | api-catalogo | sim | diff do contrato: ausente; corpo diferente da referência em modo normal | 200 | 0,3 |
| `sin-21` | 2 | 3 | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | `tipo` | api-catalogo | sim | diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,3 |
| `semt-16` | 3 | 1 | `tipo_divergente` | `type_drift` | `tipo` | api-catalogo | sim | diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,3 |
| `semt-17` | 3 | 1 | `nulo_inesperado` | `nulo_inesperado` | `id` | api-catalogo | sim | diff do contrato: nulo_inesperado; corpo diferente da referência em modo normal | 200 | 0,3 |
| `semt-20` | 3 | 3 | `valor_fora_do_dominio` | `valor_fora_do_dominio` | `preco` | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais; conferência 'preço do primeiro cartão' falhou | 200 | 0,3 |
| `semt-21` | 3 | 3 | `valor_fora_do_dominio` | `valor_fora_do_dominio` | `nome` | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 28 linha(s) a menos e 28 a mais | 200 | 0,3 |
| `tra-17` | 4 | 1 | `chave_de_juncao_errada` | `chave_de_juncao_errada` | `tipo` | api-catalogo | sim | corpo diferente da referência em modo normal | 200 | 0,3 |
| `tra-19` | 4 | 2 | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | `preco` | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,3 |
| `tra-20` | 4 | 3 | `chave_de_juncao_errada` | `chave_de_juncao_errada` | `tipo` | api-catalogo | sim | corpo diferente da referência em modo normal | 200 | 0,3 |
| `tra-21` | 4 | 3 | `contagem_inconsistente` | `contagem_inconsistente` |  | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 10 linha(s) a menos e 0 a mais; conferência 'grid com 14 cartões' falhou | 200 | 0,3 |
| `run-19` | 5 | 2 | `tempo_de_resposta_excedido` | `latency` |  | api-detalhe | sim | tempo de resposta 2013 ms acima do orçamento de 1000 ms | 200 | 31,0 |
| `run-21` | 5 | 3 | `registro_duplicado` | `registro_duplicado` |  | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 0 linha(s) a menos e 10 a mais; conferência 'grid com 14 cartões' falhou | 200 | 0,2 |
<!-- /tabela:tb_f4_reproducao_casos -->

<!-- tabela:tb_f4_reproducao_fora -->
| Caso | Classe | Nível | Causa | Por que ficou fora |
|---|---|---|---|---|
| `semt-3` | 3 | 2 | `valor_fora_do_dominio` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `semt-5` | 3 | 3 | `nulo_inesperado` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `run-4` | 5 | 3 | `dado_desatualizado` | sem modo para a causa dado_desatualizado |
| `efe-1` | 6 | 1 | `localizador_quebrado` | armada pelo harness (ficha 29): localizador_quebrado |
| `efe-2` | 6 | 2 | `estado_da_tela_divergente` | armada pelo harness (ficha 29): estado_da_tela_divergente |
| `efe-5` | 6 | 3 | `localizador_quebrado` | armada pelo harness (ficha 29): localizador_quebrado |
| `sin-7` | 2 | 1 | `campo_ausente` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `sin-10` | 2 | 2 | `campo_renomeado` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `tra-10` | 4 | 1 | `chave_de_juncao_errada` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `tra-15` | 4 | 3 | `escala_ou_unidade_errada` | sem tela: a rota 'POST /api/pedidos (pessoas=4) -> GET /api/pedidos' não é consumida por página nenhuma |
| `run-10` | 5 | 2 | `limite_de_requisicoes` | sem tela: a rota 'GET /api/produtos (12a requisicao em 1 min)' não é consumida por página nenhuma |
| `run-13` | 5 | 3 | `registro_duplicado` | sem tela: a rota 'POST /api/pedidos (clique duplo no botao)' não é consumida por página nenhuma |
| `efe-7` | 6 | 1 | `localizador_quebrado` | armada pelo harness (ficha 29): localizador_quebrado |
| `efe-14` | 6 | 3 | `localizador_quebrado` | armada pelo harness (ficha 29): localizador_quebrado |
| `lex-17` | 1 | 1 | `corpo_vazio` | sem tela: a rota 'POST /api/pedidos' não é consumida por página nenhuma |
| `lex-19` | 1 | 2 | `corpo_nao_e_json` | sem tela: a rota 'POST /api/pedidos/7/cancelar' não é consumida por página nenhuma |
| `lex-20` | 1 | 3 | `resposta_truncada` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `lex-21` | 1 | 3 | `codificacao_incorreta` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `sin-17` | 2 | 1 | `campo_renomeado` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `sin-18` | 2 | 2 | `estrutura_aninhada_divergente` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `sin-19` | 2 | 2 | `colecao_no_lugar_de_objeto` | sem tela: a rota 'POST /api/pedidos/7/cancelar' não é consumida por página nenhuma |
| `semt-18` | 3 | 2 | `tipo_divergente` | sem tela: a rota 'GET /api/produtos (modo type_drift, campo destaque)' não é consumida por página nenhuma |
| `semt-19` | 3 | 2 | `formato_de_data_divergente` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `tra-16` | 4 | 1 | `escala_ou_unidade_errada` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `tra-18` | 4 | 2 | `contagem_inconsistente` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `run-16` | 5 | 1 | `recurso_inexistente` | sem tela: a rota 'GET /api/pedidos?login=55566677788' não é consumida por página nenhuma |
| `run-17` | 5 | 1 | `erro_interno_do_servidor` | sem tela: a rota 'POST /api/pedidos/7/cancelar' não é consumida por página nenhuma |
| `run-18` | 5 | 2 | `limite_de_requisicoes` | sem tela: a rota 'POST /api/pedidos (6a tentativa de reserva no mesmo minuto)' não é consumida por página nenhuma |
| `run-20` | 5 | 3 | `dado_desatualizado` | sem modo para a causa dado_desatualizado |
| `efe-16` | 6 | 1 | `localizador_quebrado` | armada pelo harness (ficha 29): localizador_quebrado |
| `efe-17` | 6 | 1 | `localizador_quebrado` | armada pelo harness (ficha 29): localizador_quebrado |
| `efe-18` | 6 | 2 | `localizador_quebrado` | armada pelo harness (ficha 29): localizador_quebrado |
| `efe-19` | 6 | 2 | `estado_da_tela_divergente` | armada pelo harness (ficha 29): estado_da_tela_divergente |
| `efe-20` | 6 | 3 | `estado_da_tela_divergente` | armada pelo harness (ficha 29): estado_da_tela_divergente |
| `efe-21` | 6 | 3 | `estado_da_tela_divergente` | armada pelo harness (ficha 29): estado_da_tela_divergente |
<!-- /tabela:tb_f4_reproducao_fora -->
