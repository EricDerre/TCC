<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase4.py a partir de reproducao.jsonl e fora.json da corrida (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Reprodução na tela (corrida 17 sobre os 36 inéditos da ficha 27), gerada em 2026-10-27

Um caso reproduz na tela quando a chamada à CobaiaAPI sai do normal (status, corpo, contrato ou tempo acima do orçamento) ou quando uma conferência do roteiro falha (regra R1 do plano aprovado). Os casos fora são os de rota sem página (pedidos), os de causa sem modo de injeção e os de quebra de localizador, que o harness arma (ficha 29).


<!-- tabela:tb_f4_reproducao_resumo -->
| Casos de avaliação | Com tela e modo | Reproduzem na tela | Fora (sem tela, sem modo ou pelo harness) | Reproduzem (% dos casos) | Reproduzem (% dos com tela) | Roteiro falhou | Com erro do harness |
|---|---|---|---|---|---|---|---|
| 36 | 25 | 25 | 11 | 69,4 | 100,0 | 8 | 0 |
<!-- /tabela:tb_f4_reproducao_resumo -->

<!-- tabela:tb_f4_reproducao_por_classe -->
| Classe | Casos | Com tela e modo | Reproduzem | Fora | Reproduzem (%) |
|---|---|---|---|---|---|
| 1 | 6 | 5 | 5 | 1 | 83,3 |
| 2 | 6 | 6 | 6 | 0 | 100,0 |
| 3 | 6 | 5 | 5 | 1 | 83,3 |
| 4 | 6 | 5 | 5 | 1 | 83,3 |
| 5 | 6 | 4 | 4 | 2 | 66,7 |
| 6 | 6 | 0 | 0 | 6 | 0,0 |
<!-- /tabela:tb_f4_reproducao_por_classe -->

<!-- tabela:tb_f4_reproducao_por_nivel -->
| Nível | Casos | Com tela e modo | Reproduzem | Fora | Reproduzem (%) |
|---|---|---|---|---|---|
| 1 | 12 | 9 | 9 | 3 | 75,0 |
| 2 | 12 | 9 | 9 | 3 | 75,0 |
| 3 | 12 | 7 | 7 | 5 | 58,3 |
<!-- /tabela:tb_f4_reproducao_por_nivel -->

<!-- tabela:tb_f4_reproducao_por_modo -->
| Modo de injeção | Casos | Reproduzem | Motivos registrados |
|---|---|---|---|
| `chave_de_juncao_errada` | 2 | 2 | corpo diferente da referência em modo normal |
| `codificacao_incorreta` | 3 | 3 | corpo diferente da referência em modo normal; árvore diferente da referência: 5 linha(s) a menos e 5 a mais; corpo diferente da referência em modo normal; árvore diferente da referência: 6 linha(s) a menos e 6 a mais; corpo diferente da referência em modo normal; árvore diferente da referência: 7 linha(s) a menos e 7 a mais |
| `colecao_no_lugar_de_objeto` | 1 | 1 | diff do contrato: forma_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 2 linha(s) a menos e 2 a mais |
| `contagem_inconsistente` | 1 | 1 | corpo diferente da referência em modo normal; árvore diferente da referência: 10 linha(s) a menos e 0 a mais; conferência 'grid com 14 cartões' falhou |
| `corpo_nao_e_json` | 1 | 1 | corpo nao_json; corpo diferente da referência em modo normal; árvore diferente da referência: 140 linha(s) a menos e 1 a mais; conferência 'grid com 14 cartões' falhou |
| `corpo_vazio` | 1 | 1 | corpo vazio; árvore diferente da referência: 144 linha(s) a menos e 1 a mais; conferência 'grid carregado antes do detalhe' falhou |
| `escala_ou_unidade_errada` | 2 | 2 | corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais |
| `estrutura_aninhada_divergente` | 1 | 1 | diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais |
| `field_missing` | 2 | 2 | diff do contrato: ausente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais; conferência 'preço do primeiro cartão' falhou; diff do contrato: ausente; corpo diferente da referência em modo normal; árvore diferente da referência: 28 linha(s) a menos e 28 a mais |
| `field_renamed` | 2 | 2 | diff do contrato: renomeado; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 0 a mais; diff do contrato: renomeado; corpo diferente da referência em modo normal; árvore diferente da referência: 15 linha(s) a menos e 15 a mais |
| `latency` | 1 | 1 | tempo de resposta 2008 ms acima do orçamento de 1000 ms |
| `limite_de_requisicoes` | 1 | 1 | status 429; diff do contrato: ausente, forma_diferente, inesperado; corpo diferente da referência em modo normal; árvore diferente da referência: 140 linha(s) a menos e 1 a mais; conferência 'grid com 14 cartões' falhou |
| `nulo_inesperado` | 2 | 2 | corpo diferente da referência em modo normal; árvore diferente da referência: 15 linha(s) a menos e 15 a mais; diff do contrato: nulo_inesperado; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais |
| `recurso_inexistente` | 1 | 1 | status 404; diff do contrato: ausente, forma_diferente, inesperado; árvore diferente da referência: 144 linha(s) a menos e 1 a mais; conferência 'grid carregado antes do detalhe' falhou |
| `registro_duplicado` | 1 | 1 | corpo diferente da referência em modo normal; árvore diferente da referência: 0 linha(s) a menos e 10 a mais; conferência 'grid com 14 cartões' falhou |
| `type_drift` | 1 | 1 | diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais |
| `valor_fora_do_dominio` | 2 | 2 | corpo diferente da referência em modo normal; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais; conferência 'preço do primeiro cartão' falhou |
<!-- /tabela:tb_f4_reproducao_por_modo -->

<!-- tabela:tb_f4_reproducao_custo -->
| Tempo por cenário (mediana, s) | Tempo por cenário (máximo, s) | Tempo total dos cenários (s) | Tempo da chamada à API (mediana, ms) | Árvore antes da poda (mediana, nós) | Árvore depois (mediana, linhas) | Corpo HTTP (mediana, caracteres) | Caso ao vivo (mediana, caracteres) |
|---|---|---|---|---|---|---|---|
| 0,3 | 30,7 | 38,4 | 15,9 | 193 | 39 | 1888 | 2618 |
<!-- /tabela:tb_f4_reproducao_custo -->

<!-- tabela:tb_f4_reproducao_casos -->
| Caso | Classe | Nível | Causa | Modo | Campo | Cenário | Reproduz | Motivo | Status | Segundos |
|---|---|---|---|---|---|---|---|---|---|---|
| `lex-22` | 1 | 1 | `corpo_nao_e_json` | `corpo_nao_e_json` |  | api-catalogo | sim | corpo nao_json; corpo diferente da referência em modo normal; árvore diferente da referência: 140 linha(s) a menos e 1 a mais; conferência 'grid com 14 cartões' falhou | 200 | 0,2 |
| `lex-23` | 1 | 1 | `corpo_vazio` | `corpo_vazio` |  | api-detalhe | sim | corpo vazio; árvore diferente da referência: 144 linha(s) a menos e 1 a mais; conferência 'grid carregado antes do detalhe' falhou | 200 | 0,2 |
| `lex-24` | 1 | 2 | `codificacao_incorreta` | `codificacao_incorreta` | `resumo` | api-detalhe | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 5 linha(s) a menos e 5 a mais | 200 | 0,6 |
| `lex-25` | 1 | 2 | `codificacao_incorreta` | `codificacao_incorreta` | `nome` | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 6 linha(s) a menos e 6 a mais | 200 | 0,4 |
| `lex-26` | 1 | 3 | `codificacao_incorreta` | `codificacao_incorreta` | `nome` | api-detalhe | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 7 linha(s) a menos e 7 a mais | 200 | 0,6 |
| `sin-22` | 2 | 1 | `campo_ausente` | `field_missing` | `nome` | api-catalogo | sim | diff do contrato: ausente; corpo diferente da referência em modo normal; árvore diferente da referência: 28 linha(s) a menos e 28 a mais | 200 | 0,3 |
| `sin-23` | 2 | 1 | `campo_renomeado` | `field_renamed` | `resumo` | api-detalhe | sim | diff do contrato: renomeado; corpo diferente da referência em modo normal; árvore diferente da referência: 15 linha(s) a menos e 15 a mais | 200 | 0,6 |
| `sin-24` | 2 | 2 | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | `tipo` | api-catalogo | sim | diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,2 |
| `sin-25` | 2 | 2 | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` |  | api-detalhe | sim | diff do contrato: forma_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 2 linha(s) a menos e 2 a mais | 200 | 0,6 |
| `sin-26` | 2 | 3 | `campo_ausente` | `field_missing` | `preco` | api-catalogo | sim | diff do contrato: ausente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais; conferência 'preço do primeiro cartão' falhou | 200 | 0,2 |
| `sin-27` | 2 | 3 | `campo_renomeado` | `field_renamed` | `imagem` | api-catalogo | sim | diff do contrato: renomeado; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 0 a mais | 200 | 0,3 |
| `semt-22` | 3 | 1 | `nulo_inesperado` | `nulo_inesperado` | `preco` | api-catalogo | sim | diff do contrato: nulo_inesperado; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,3 |
| `semt-23` | 3 | 1 | `valor_fora_do_dominio` | `valor_fora_do_dominio` | `preco` | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais; conferência 'preço do primeiro cartão' falhou | 200 | 0,2 |
| `semt-24` | 3 | 2 | `tipo_divergente` | `type_drift` | `destaque` | api-catalogo | sim | diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,3 |
| `semt-26` | 3 | 3 | `nulo_inesperado` | `nulo_inesperado` | `resumo` | api-detalhe | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 15 linha(s) a menos e 15 a mais | 200 | 0,5 |
| `semt-27` | 3 | 3 | `valor_fora_do_dominio` | `valor_fora_do_dominio` | `id` | api-catalogo | sim | corpo diferente da referência em modo normal | 200 | 0,3 |
| `tra-22` | 4 | 1 | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | `preco` | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,3 |
| `tra-24` | 4 | 2 | `chave_de_juncao_errada` | `chave_de_juncao_errada` | `tipo` | api-catalogo | sim | corpo diferente da referência em modo normal | 200 | 0,3 |
| `tra-25` | 4 | 2 | `contagem_inconsistente` | `contagem_inconsistente` |  | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 10 linha(s) a menos e 0 a mais; conferência 'grid com 14 cartões' falhou | 200 | 0,2 |
| `tra-26` | 4 | 3 | `chave_de_juncao_errada` | `chave_de_juncao_errada` | `id` | api-catalogo | sim | corpo diferente da referência em modo normal | 200 | 0,2 |
| `tra-27` | 4 | 3 | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | `preco` | api-detalhe | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais | 200 | 0,5 |
| `run-22` | 5 | 1 | `limite_de_requisicoes` | `limite_de_requisicoes` |  | api-catalogo | sim | status 429; diff do contrato: ausente, forma_diferente, inesperado; corpo diferente da referência em modo normal; árvore diferente da referência: 140 linha(s) a menos e 1 a mais; conferência 'grid com 14 cartões' falhou | 429 | 0,2 |
| `run-23` | 5 | 1 | `recurso_inexistente` | `recurso_inexistente` |  | api-detalhe | sim | status 404; diff do contrato: ausente, forma_diferente, inesperado; árvore diferente da referência: 144 linha(s) a menos e 1 a mais; conferência 'grid carregado antes do detalhe' falhou | 404 | 0,2 |
| `run-24` | 5 | 2 | `registro_duplicado` | `registro_duplicado` |  | api-catalogo | sim | corpo diferente da referência em modo normal; árvore diferente da referência: 0 linha(s) a menos e 10 a mais; conferência 'grid com 14 cartões' falhou | 200 | 0,2 |
| `run-25` | 5 | 2 | `tempo_de_resposta_excedido` | `latency` |  | api-detalhe | sim | tempo de resposta 2008 ms acima do orçamento de 1000 ms | 200 | 30,7 |
<!-- /tabela:tb_f4_reproducao_casos -->

<!-- tabela:tb_f4_reproducao_fora -->
| Caso | Classe | Nível | Causa | Por que ficou fora |
|---|---|---|---|---|
| `lex-27` | 1 | 3 | `codificacao_incorreta` | sem tela: a rota 'POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 3, "data_pedido": "2026-12-05"})' não é consumida por página nenhuma |
| `semt-25` | 3 | 2 | `formato_de_data_divergente` | sem tela: a rota 'POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 6, "data_pedido": "2026-12-20"})' não é consumida por página nenhuma |
| `tra-23` | 4 | 1 | `escala_ou_unidade_errada` | sem tela: a rota 'POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 4, "data_pedido": "2026-12-19"})' não é consumida por página nenhuma |
| `run-26` | 5 | 3 | `dado_desatualizado` | sem modo para a causa dado_desatualizado |
| `run-27` | 5 | 3 | `registro_duplicado` | sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma |
| `efe-22` | 6 | 1 | `localizador_quebrado` | armada pelo harness (ficha 29): localizador_quebrado |
| `efe-23` | 6 | 1 | `localizador_quebrado` | armada pelo harness (ficha 29): localizador_quebrado |
| `efe-24` | 6 | 2 | `localizador_quebrado` | armada pelo harness (ficha 29): localizador_quebrado |
| `efe-25` | 6 | 2 | `localizador_quebrado` | armada pelo harness (ficha 29): localizador_quebrado |
| `efe-26` | 6 | 3 | `estado_da_tela_divergente` | armada pelo harness (ficha 29): estado_da_tela_divergente |
| `efe-27` | 6 | 3 | `estado_da_tela_divergente` | armada pelo harness (ficha 29): estado_da_tela_divergente |
<!-- /tabela:tb_f4_reproducao_fora -->
