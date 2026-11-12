<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por portoes_de_edicao.py --m1 a partir de `fase4_biblioteca/` (propostas, lote e revisão do lote) e `limiares_texto.json` (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Medida M1: os portões 3, 4 e 5 nas propostas de edição da corrida 20, gerada em 2026-11-10

Medida M1 da proposta do analista de documentação (ficha 67, decisão 121), sem modelo. Na corrida 20 o modelo fez 92 propostas de edição em 54 casos; 20 passaram nos filtros de hoje e a revisão humana do lote julgou 2 corretas, 9 parciais e 9 erradas. Aqui os três portões novos da proposta são aplicados a essas propostas: o portão 3 e o portão 4 leem o texto e valem para as 92; o portão 5 aplica a edição a uma cópia da biblioteca de antes do lote e refaz a busca de 126 casos com gabarito, e por isso só vale para as 20 que viraram edição.

Cada portão sozinho, contra a revisão humana das 20. O portão 3, a forma de instrução, recusaria 8 das 9 erradas e 8 das 9 parciais, e perderia 2 das 2 corretas; nas 92 propostas ele recusaria 86 (a contagem publicada pela pesquisa, com cinco radicais, dava 76). O portão 4, os filtros de texto, recusaria 2 das 9 erradas e 0 das 9 parciais, e perderia 1 das 2 corretas; nas 92 ele recusaria 11. O portão 5, a busca, recusaria 3 das 9 erradas e 1 das 9 parciais, e perderia 0 das 2 corretas: nas 20 edições o verbete da causa certa sai dos três entregues 7 vezes e entra 4.

Os três em sequência. Das 20 edições, sobram 2 depois do portão 3, 2 depois do portão 4 e 1 depois do portão 5: 0 corretas, 0 parciais e 1 errada. Sem o portão da forma, os portões 4 e 5 deixariam 15: 1 correta, 8 parciais e 6 erradas.

Como ler. O portão da forma, aplicado ao que o modelo escreve hoje, esvazia o lote e leva junto as edições corretas: ele só faz sentido com um prompt que peça a frase como ela vai ficar no verbete, que é o que a corrida 27 mede. Os portões em código olham a forma do texto e o efeito na busca; nenhum deles diz se a afirmação é verdadeira, e a revisão de uma pessoa continua sendo a porta final. A corrida 20 não tem proposta do tipo sinal de busca, então a segunda regra do portão 5 (o caso de origem tem de passar a receber o verbete) não foi exercitada aqui.

<!-- tabela:tb_f4_portoes_resumo -->
| Propostas | Casos | Revisadas por uma pessoa | Corretas | Parciais | Erradas | O portão 3 recusaria | O portão 4 recusaria | O portão 5 recusaria (das revisadas) | Sobram depois dos três | Sobram sem o portão da forma |
|---|---|---|---|---|---|---|---|---|---|---|
| 92 | 54 | 20 | 2 | 9 | 9 | 86 | 11 | 4 | 1 | 15 |
<!-- /tabela:tb_f4_portoes_resumo -->
<!-- tabela:tb_f4_portoes_portoes -->
| Portão | Regra | Recusa nas propostas | Passa nas propostas | Não se aplica | Recusa nas revisadas | Erradas recusadas | Parciais recusadas | Corretas perdidas |
|---|---|---|---|---|---|---|---|---|
| portão 3, a forma de instrução | recusa o texto que começa por verbo de edição ou por rótulo seguido de dois-pontos (lista fechada) | 86 | 6 | 0 | 18 | 8 de 9 | 8 de 9 | 2 de 2 |
| portão 4, os filtros de texto | recusa o texto que reprova em alguma das medidas de prolixidade e objetividade do pacote Q2, com os limiares do corpus | 11 | 81 | 0 | 3 | 2 de 9 | 0 de 9 | 1 de 2 |
| portão 5, a busca | recusa a edição que, aplicada numa cópia da biblioteca, tira o verbete da causa certa dos três entregues de algum caso com gabarito; no sinal de busca, exige que o caso de origem passe a receber o verbete | 4 | 16 | 72 | 4 | 3 de 9 | 1 de 9 | 0 de 2 |
<!-- /tabela:tb_f4_portoes_portoes -->
<!-- tabela:tb_f4_portoes_sequencia -->
| Etapa | Edições que sobram | Corretas | Parciais | Erradas |
|---|---|---|---|---|
| passaram nos filtros de hoje e foram revisadas | 20 | 2 | 9 | 9 |
| depois do portão 3 (forma de instrução) | 2 | 0 | 1 | 1 |
| depois do portão 4 (filtros de texto) | 2 | 0 | 1 | 1 |
| depois do portão 5 (busca) | 1 | 0 | 0 | 1 |
| só os portões 4 e 5, sem o da forma | 15 | 1 | 8 | 6 |
| só o portão 5, o da busca | 16 | 2 | 8 | 6 |
<!-- /tabela:tb_f4_portoes_sequencia -->
<!-- tabela:tb_f4_portoes_destino -->
| O que os filtros de hoje fizeram | Propostas | O portão 3 recusaria | O portão 4 recusaria |
|---|---|---|---|
| aceita pelos filtros de hoje | 19 | 17 | 3 |
| segurada para revisão humana (regra dos 40%) | 1 | 1 | 0 |
| recusada pelo validador da Fase 3 | 56 | 53 | 5 |
| recusada pelos filtros da Fase 4 | 16 | 15 | 3 |
<!-- /tabela:tb_f4_portoes_destino -->
<!-- tabela:tb_f4_portoes_criterios -->
| Medida do portão 4 | Propostas reprovadas | Reprovadas entre as revisadas |
|---|---|---|
| Palavras por frase (média) | 0 | 0 |
| Palavras por frase (máximo) | 0 | 0 |
| Razão de preenchimento (lista fechada) | 0 | 0 |
| Repetição interna (trigramas repetidos) | 5 | 0 |
| Taxa de compressão (palavras de conteúdo por palavra distinta, em janelas de 100) | 0 | 0 |
| Jargão e sigla sem expansão na primeira menção (lista fechada) | 6 | 3 |
<!-- /tabela:tb_f4_portoes_criterios -->
<!-- tabela:tb_f4_portoes_palavras -->
| Primeira palavra do texto | Propostas | O portão 3 |
|---|---|---|
| `adicionar` | 56 | recusa |
| `corrigir` | 15 | recusa |
| `retificar` | 4 | recusa |
| `adicione` | 3 | recusa |
| `adicionado` | 2 | recusa |
| `notar` | 2 | recusa |
| `o` | 2 | passa |
| `um` | 2 | passa |
| `adiciona` | 1 | recusa |
| `corrigido` | 1 | recusa |
| `cria` | 1 | recusa |
| `documentação` | 1 | passa |
| `ocorre` | 1 | passa |
| `retificação:` | 1 | recusa |
<!-- /tabela:tb_f4_portoes_palavras -->
<!-- tabela:tb_f4_portoes_revisadas -->
| Caso | Verbete | Operação | Revisão humana | Portão 3 | Portão 4 | Portão 5 | Casos em que os três verbetes mudam | Verbete certo entra | Verbete certo sai | Passa nos três | Texto |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `sin-1` | `campo_preco_ausente` | novo_verbete | Parcial | passa | passa | recusa | 6 | 0 | 1 | não | Um campo preço ausente na resposta da API resulta em botões sem informações relevantes na interface web. |
| `tra-3` | `novo_verbete` | novo_verbete | Parcial | recusa | passa | passa | 4 | 0 | 0 | não | Corrigir a junção entre tbprodutos e tbtipos, garantindo que id_tipo_produto esteja corretamente ligado a tbtipos.id_tipo. |
| `tra-5` | `pessoas_incorretas` | novo_verbete | Errada | recusa | passa | passa | 5 | 0 | 0 | não | Adicionar validação no número de pessoas no pedido para evitar valores incorretos. |
| `run-3` | `limite_de_requisicoes` | retificacao | Correta | recusa | passa | passa | 0 | 0 | 0 | não | Corrigir que o 429 pode ser emitido pelo próprio servidor ou intermediários, não necessariamente pelo CobaiaAPI. |
| `run-5` | `contrato-pedido` | nota | Parcial | recusa | passa | passa | 5 | 0 | 0 | não | Adicionar nota sobre a possibilidade de POST /api/pedidos inserir registros duplicados sem idempotência, causando registros com id consecutivo e duas respostas 201 para um único POST. |
| `efe-4` | `contrato-produto` | nota | Errada | recusa | passa | passa | 9 | 0 | 0 | não | Adicionar nota sobre a necessidade de verificar se a resposta é um objeto ou uma coleção, pois a interface espera um objeto. |
| `efe-4` | `estado_da_tela_divergente` | retificacao | Errada | recusa | passa | recusa | 8 | 0 | 2 | não | Corrigir a lógica para atualizar o estado corretamente, independentemente de ser uma coleção ou um objeto. |
| `sin-15` | `colecao_no_lugar_de_objeto` | nota | Correta | recusa | recusa | passa | 0 | 0 | 0 | não | Adicionar nota sobre a necessidade de tratar a categoria como uma string, não uma lista, no front-end. |
| `semt-6` | `tipo_divergente` | nota | Errada | recusa | recusa | recusa | 6 | 0 | 3 | não | Adicionar nota sobre a necessidade de conversão correta do tipo id em inteiro no front-end, considerando que o backend retorna como string. |
| `semt-7` | `tipo_divergente` | retificacao | Errada | recusa | passa | passa | 5 | 1 | 0 | não | Adicionar exemplo de campo "pessoas" como número em vez de string, causando inconsistência na contagem total de lugares reservados. |
| `semt-10` | `tipo_divergente` | nota | Parcial | recusa | passa | passa | 2 | 0 | 0 | não | Adicionar nota sobre a converção de tipos entre a API e a interface web, especificamente sobre o campo destaque que vem como texto em vez de booleano. |
| `semt-15` | `validacao-na-api` | novo_verbete | Errada | recusa | passa | passa | 3 | 0 | 0 | não | Adicionar validação no status do pedido na API para evitar valores fora do domínio permitido pelo formulário. |
| `tra-6` | `formato_preco` | novo_verbete | Errada | recusa | recusa | recusa | 4 | 0 | 1 | não | Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro. |
| `tra-14` | `contagem_inconsistente` | nota | Parcial | recusa | passa | passa | 3 | 0 | 0 | não | Adicionar nota sobre a necessidade de incluir o total na resposta da API /api/produtos, para evitar contagens inconsistentes. |
| `run-12` | `erro_interno_do_servidor` | nota | Errada | recusa | passa | passa | 0 | 0 | 0 | não | Adicionar que a conversão de ErrorFault em 500 pode ser causada por problemas na rota. |
| `efe-8` | `estado_da_tela_divergente` | nota | Parcial | recusa | passa | passa | 4 | 1 | 0 | não | Adicionar nota sobre a necessidade de atualização correta do estado da tela após a resposta da API. |
| `efe-8` | `atualizacao-da-tela` | novo_verbete | Parcial | recusa | passa | passa | 7 | 1 | 0 | não | Adicionar verbete sobre a necessidade de atualização correta do estado da tela após a resposta da API, utilizando promises ou async/await. |
| `efe-10` | `interface-frontend` | nota | Parcial | recusa | passa | passa | 0 | 0 | 0 | não | Adicionar nota sobre a importância de atualizações corretas do DOM e a dependência de redirects na interface frontend. |
| `efe-11` | `localizador_quebrado` | nota | Parcial | recusa | passa | passa | 2 | 0 | 0 | não | Adicionar que a falta de ORDER BY na consulta pode causar ordem aleatória indeterminada dos produtos. |
| `efe-13` | `estado_da_tela_divergente` | nota | Errada | passa | passa | passa | 6 | 1 | 0 | sim | O cancelamento depende de um redirect, o que pode causar divergência na interface. |
<!-- /tabela:tb_f4_portoes_revisadas -->
<!-- tabela:tb_f4_portoes_propostas -->
| Caso | Proposta | Operação | Verbete | O que os filtros de hoje fizeram | Código da recusa | Revisão humana | Portão 3 | Portão 4 | Medidas reprovadas no portão 4 | Portão 5 | Texto |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `lex-2` | 1 | nota | `corpo_nao_e_json` | recusada pelos filtros da Fase 4 | mensagem_nao_encontrada_no_codigo |  | recusa | recusa | repeticao_razao | n/a | Adicionar um exemplo de sintoma específico, como "Página de erro HTML em vez de JSON", para melhorar a identificação de casos onde o corpo da resposta não é JSON. Adicionar um exemplo de sintoma para clarificar que XML também pode causar parse falho. |
| `lex-3` | 1 | nota | `corpo_vazio` | recusada pelo validador da Fase 3 | duplicada |  | recusa | passa |  | n/a | Adicionar exemplo de sintoma: "Tabela de reservas vazia, sem erro." |
| `lex-3` | 2 | novo_verbete | `resposta_truncada` | recusada pelo validador da Fase 3 | id_repetido |  | recusa | passa |  | n/a | Retificação: onde diz "Fora dele: limite num proxy, conexão encerrada durante o envio.", leia: Corrigir a descrição para incluir que o truncamento pode ser causado por limites de proxy ou interrupção de conexão. Adicione um exemplo de como verificar o Content-Length na documentação para evitar esse problema. |
| `lex-5` | 1 | nota | `resposta_truncada` | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso |  | recusa | passa |  | n/a | Corrigir a descrição para incluir que o truncamento pode ser causado por limites de proxy ou interrupção de conexão. Adicione um exemplo de como verificar o Content-Length na documentação para evitar esse problema. |
| `lex-5` | 2 | novo_verbete | `resposta_truncada` | recusada pelo validador da Fase 3 | id_repetido |  | passa | passa |  | n/a | Ocorre quando o corpo da resposta JSON é cortado antes de ser completamente enviado, resultando em uma lista incompleta ou parse falha. Verifique o Content-Length para evitar esse problema. |
| `sin-1` | 1 | nota | `campo_ausente` | recusada pelos filtros da Fase 4 | texto_nao_atomico |  | recusa | passa |  | n/a | Adicionar: "Sinais: nome ausente: cartão '(sem nome)'; preço ausente: botão imprime 'undefined'; id ausente: botão de detalhe ou cancelar sem identificador, clique sem efeito." |
| `sin-1` | 2 | novo_verbete | `campo_preco_ausente` | aceita pelos filtros de hoje |  | Parcial | passa | passa |  | recusa | Um campo preço ausente na resposta da API resulta em botões sem informações relevantes na interface web. |
| `sin-2` | 1 | nota | `campo_renomeado` | recusada pelos filtros da Fase 4 | mensagem_nao_encontrada_no_codigo |  | recusa | passa |  | n/a | "Corrigir a afirmação para: 'Contrato mudou no servidor sem atualizar o cliente e API não reflete as mudanças.'" |
| `sin-2` | 2 | novo_verbete | `campo_incorreto` | recusada pelos filtros da Fase 4 | mensagem_nao_encontrada_no_codigo |  | passa | passa |  | n/a | "Um campo pode ser renomeado ou ausente no contrato, mas deve ser consistentemente implementado no cliente e servidor." |
| `sin-3` | 1 | retificacao | `estrutura_aninhada_divergente` | recusada pelo validador da Fase 3 | duplicada |  | recusa | passa |  | n/a | Adicionar exemplo de estrutura aninhada divergente no verbete. |
| `sin-3` | 2 | nota | `contrato-produto` | recusada pelo validador da Fase 3 | duplicada |  | recusa | passa |  | n/a | Notar que o contrato especifica a estrutura do JSON esperado, mas não aborda o truncamento de resposta. |
| `semt-2` | 1 | nota | `tipo_divergente` | recusada pelo validador da Fase 3 | texto_curto |  | recusa | passa |  | n/a | Adicionar exemplo de converção incorreta no verbete. |
| `semt-2` | 2 | retificacao | `valor_fora_do_dominio` | recusada pelo validador da Fase 3 | arquivo_inexistente |  | recusa | passa |  | n/a | Retificar a informação sobre a validação do status do pedido na API. |
| `semt-4` | 1 | nota | `formato_de_data_divergente` | recusada pelo validador da Fase 3 | palavra_chave_invalida |  | recusa | passa |  | n/a | Adicionar que o API deve retornar a data_pedido no formato ISO 8601 (AAAA-MM-DD) para evitar interpretação incorreta pelo cliente. |
| `semt-4` | 2 | retificacao | `formato_de_data_divergente` | recusada pelo validador da Fase 3 | palavra_chave_invalida |  | recusa | passa |  | n/a | Corrigir que a data_pedido deve ser sempre retornada no formato ISO 8601 (AAAA-MM-DD) e não deve conter hora ou fuso. |
| `tra-2` | 1 | retificacao | `chave_de_juncao_errada` | recusada pelo validador da Fase 3 | arquivo_inexistente |  | recusa | passa |  | n/a | Corrigir a junção entre tbpedido_reserva e tbusuarios, garantindo que id_clientes esteja corretamente ligado a login_usuario.id. |
| `tra-3` | 1 | retificacao | `chave_de_juncao_errada` | recusada pelo validador da Fase 3 | duplicada |  | recusa | passa |  | n/a | Corrigir a junção entre tbprodutos e tbtipos, garantindo que id_tipo_produto esteja corretamente ligado a tbtipos.id_tipo. |
| `tra-3` | 2 | novo_verbete | `novo_verbete` | aceita pelos filtros de hoje |  | Parcial | recusa | passa |  | passa | Corrigir a junção entre tbprodutos e tbtipos, garantindo que id_tipo_produto esteja corretamente ligado a tbtipos.id_tipo. |
| `tra-5` | 1 | retificacao | `escala_ou_unidade_errada` | recusada pelo validador da Fase 3 | duplicada |  | recusa | passa |  | n/a | Adicionar exemplo de conversão incorreta de valor_produto DECIMAL(9,2) para float, causando arredondamento. |
| `tra-5` | 2 | novo_verbete | `pessoas_incorretas` | aceita pelos filtros de hoje |  | Errada | recusa | passa |  | passa | Adicionar validação no número de pessoas no pedido para evitar valores incorretos. |
| `run-3` | 1 | nota | `contrato-produto` | recusada pelos filtros da Fase 4 | texto_de_origem_proibida |  | recusa | passa |  | n/a | Adicionar nota sobre o status 429 e sua relação com o limite de requisições. |
| `run-3` | 2 | retificacao | `limite_de_requisicoes` | aceita pelos filtros de hoje |  | Correta | recusa | passa |  | passa | Corrigir que o 429 pode ser emitido pelo próprio servidor ou intermediários, não necessariamente pelo CobaiaAPI. |
| `run-5` | 1 | novo_verbete | `registro_duplicado` | recusada pelo validador da Fase 3 | id_repetido |  | recusa | passa |  | n/a | Adicionar que POST /api/pedidos pode inserir registros duplicados sem idempotência, causando registros com id consecutivo e duas respostas 201 para um único POST. |
| `run-5` | 2 | nota | `contrato-pedido` | aceita pelos filtros de hoje |  | Parcial | recusa | passa |  | passa | Adicionar nota sobre a possibilidade de POST /api/pedidos inserir registros duplicados sem idempotência, causando registros com id consecutivo e duas respostas 201 para um único POST. |
| `efe-4` | 1 | nota | `contrato-produto` | segurada para revisão humana (regra dos 40%) | para_revisao_humana | Errada | recusa | passa |  | passa | Adicionar nota sobre a necessidade de verificar se a resposta é um objeto ou uma coleção, pois a interface espera um objeto. |
| `efe-4` | 2 | retificacao | `estado_da_tela_divergente` | aceita pelos filtros de hoje |  | Errada | recusa | passa |  | recusa | Corrigir a lógica para atualizar o estado corretamente, independentemente de ser uma coleção ou um objeto. |
| `lex-6` | 1 | retificacao | `corpo_nao_e_json` | recusada pelo validador da Fase 3 | palavra_chave_invalida |  | recusa | passa |  | n/a | Adicionar um exemplo de sintoma específico, como "Página de erro HTML em vez de JSON", para melhorar a identificação de casos onde o corpo da resposta não é JSON. |
| `lex-9` | 1 | nota | `corpo_nao_e_json` | recusada pelos filtros da Fase 4 | mensagem_nao_encontrada_no_codigo |  | recusa | recusa | repeticao_razao | n/a | Adicionar um exemplo de sintoma específico, como "Página de erro HTML em vez de JSON", para melhorar a identificação de casos onde o corpo da resposta não é JSON. Adicionar um exemplo de sintoma para clarificar que XML também pode causar parse falho. |
| `lex-12` | 1 | nota | `corpo_nao_e_json` | recusada pelo validador da Fase 3 | arquivo_inexistente |  | recusa | recusa | repeticao_razao | n/a | Adicionar um exemplo de sintoma específico, como "Página de erro HTML em vez de JSON", para melhorar a identificação de casos onde o corpo da resposta não é JSON. Adicionar um exemplo de sintoma para clarificar que XML também pode causar parse falho. |
| `sin-6` | 1 | nota | `campo_ausente` | recusada pelo validador da Fase 3 | palavra_chave_invalida |  | recusa | passa |  | n/a | Adicionar nota sobre a remoção de campos no fault_injection.py. |
| `sin-6` | 2 | novo_verbete | `campo_renomeado` | recusada pelo validador da Fase 3 | id_repetido |  | recusa | passa |  | n/a | Adicionar verbete sobre campos renomeados e como isso afeta a documentação. |
| `sin-8` | 1 | nota | `colecao_no_lugar_de_objeto` | recusada pelo validador da Fase 3 | duplicada |  | recusa | passa |  | n/a | Corrigir que o campo "tipo" deve ser tratado como uma string, não uma lista. |
| `sin-8` | 2 | retificacao | `colecao_no_lugar_de_objeto` | recusada pelo validador da Fase 3 | duplicada |  | recusa | passa |  | n/a | Corrigir que o campo "tipo" deve ser tratado como uma string, não uma lista. |
| `sin-9` | 1 | nota | `campo_renomeado` | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso |  | recusa | passa |  | n/a | Adicionar exemplo de estrutura aninhada divergente no verbete. |
| `sin-9` | 2 | novo_verbete | `estrutura_aninhada_divergente` | recusada pelo validador da Fase 3 | id_repetido |  | recusa | passa |  | n/a | Adicionar exemplo de estrutura aninhada divergente no verbete. |
| `sin-12` | 1 | nota | `campo_ausente` | recusada pelo validador da Fase 3 | texto_curto |  | recusa | passa |  | n/a | Adicionado sintomas para campos ausentes em objetos JSON. |
| `sin-12` | 2 | novo_verbete | `campo_ausente` | recusada pelo validador da Fase 3 | id_repetido |  | passa | passa |  | n/a | Documentação adicionada para campos ausentes em objetos JSON, incluindo sintomas e causas. |
| `sin-13` | 1 | retificacao | `estrutura_aninhada_divergente` | recusada pelo validador da Fase 3 | duplicada |  | recusa | passa |  | n/a | Adicionar exemplo de estrutura aninhada divergente no verbete. |
| `sin-15` | 1 | nota | `colecao_no_lugar_de_objeto` | aceita pelos filtros de hoje |  | Correta | recusa | recusa | termos_sem_expansao_n | passa | Adicionar nota sobre a necessidade de tratar a categoria como uma string, não uma lista, no front-end. |
| `sin-15` | 2 | nota | `contrato-produto` | recusada pelos filtros da Fase 4 | redundante |  | recusa | passa |  | n/a | Notar que o contrato especifica a estrutura do JSON esperado, mas não aborda o tratamento da categoria como uma string. |
| `semt-6` | 1 | nota | `tipo_divergente` | aceita pelos filtros de hoje |  | Errada | recusa | recusa | termos_sem_expansao_n | recusa | Adicionar nota sobre a necessidade de conversão correta do tipo id em inteiro no front-end, considerando que o backend retorna como string. |
| `semt-6` | 2 | retificacao | `contagem_inconsistente` | recusada pelo validador da Fase 3 | palavra_chave_invalida |  | recusa | passa |  | n/a | Retificar a descrição para mencionar que a contagem inconsistente pode ocorrer devido a consultas diferentes retornando resultados distintos. |
| `semt-7` | 1 | retificacao | `tipo_divergente` | aceita pelos filtros de hoje |  | Errada | recusa | passa |  | passa | Adicionar exemplo de campo "pessoas" como número em vez de string, causando inconsistência na contagem total de lugares reservados. |
| `semt-7` | 2 | novo_verbete | `contagem_inconsistente` | recusada pelo validador da Fase 3 | id_repetido |  | recusa | passa |  | n/a | Adicionar verbete sobre inconsistência na contagem de reservas devido a tipos divergentes e formatos de data. |
| `semt-10` | 1 | nota | `tipo_divergente` | aceita pelos filtros de hoje |  | Parcial | recusa | passa |  | passa | Adicionar nota sobre a converção de tipos entre a API e a interface web, especificamente sobre o campo destaque que vem como texto em vez de booleano. |
| `semt-10` | 2 | novo_verbete | `tipo_convercao` | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso |  | recusa | passa |  | n/a | Adicionar um novo verbete para documentar a converção de tipos entre a API e a interface web, especificamente sobre o campo destaque que vem como texto em vez de booleano. |
| `semt-11` | 1 | retificacao | `valor_fora_do_dominio` | recusada pelo validador da Fase 3 | arquivo_inexistente |  | recusa | passa |  | n/a | Adicionar validação no status do pedido na API para evitar valores fora do domínio. |
| `semt-12` | 1 | retificacao | `formato_de_data_divergente` | recusada pelo validador da Fase 3 | palavra_chave_invalida |  | recusa | passa |  | n/a | Corrigir a documentação para especificar que a API deve retornar data_pedido no formato ISO AAAA-MM-DD, e que valores como timestamp devem ser convertidos antes da resposta. |
| `semt-13` | 1 | nota | `tipo_divergente` | recusada pelo validador da Fase 3 | teto_notas_verbete |  | recusa | recusa | termos_sem_expansao_n | n/a | Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro. |
| `semt-15` | 1 | retificacao | `valor_fora_do_dominio` | recusada pelo validador da Fase 3 | duplicada |  | recusa | passa |  | n/a | Adicionar validação no status do pedido na API para evitar valores fora do domínio. |
| `semt-15` | 2 | novo_verbete | `validacao-na-api` | aceita pelos filtros de hoje |  | Errada | recusa | passa |  | passa | Adicionar validação no status do pedido na API para evitar valores fora do domínio permitido pelo formulário. |
| `tra-6` | 1 | nota | `escala_ou_unidade_errada` | recusada pelo validador da Fase 3 | duplicada |  | recusa | passa |  | n/a | Adicionar exemplo de conversão incorreta de valor_produto DECIMAL(9,2) para float, causando arredondamento. |
| `tra-6` | 2 | novo_verbete | `formato_preco` | aceita pelos filtros de hoje |  | Errada | recusa | recusa | termos_sem_expansao_n | recusa | Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro. |
| `tra-7` | 1 | nota | `entidade-produto` | recusada pelo validador da Fase 3 | duplicada |  | recusa | recusa | termos_sem_expansao_n | n/a | Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro. |
| `tra-7` | 2 | novo_verbete | `chave_de_juncao_errada` | recusada pelo validador da Fase 3 | id_repetido |  | recusa | passa |  | n/a | Corrigir a junção entre tbprodutos e tbtipos, garantindo que id_tipo_produto esteja corretamente ligado a tbtipos.id_tipo. |
| `tra-9` | 1 | retificacao | `formato_de_data_divergente` | recusada pelo validador da Fase 3 | palavra_chave_invalida |  | recusa | passa |  | n/a | Adicionar exemplo de conversão incorreta de data, causando deslocamento. |
| `tra-9` | 2 | novo_verbete | `deslocamento_de_data` | recusada pelo validador da Fase 3 | palavra_chave_invalida |  | recusa | passa |  | n/a | Adicionar exemplo de conversão incorreta de data, causando deslocamento. |
| `tra-12` | 1 | nota | `escala_ou_unidade_errada` | recusada pelo validador da Fase 3 | duplicada |  | recusa | passa |  | n/a | Adicionar exemplo de conversão incorreta de valor_produto DECIMAL(9,2) para float, causando arredondamento. |
| `tra-12` | 2 | retificacao | `escala_ou_unidade_errada` | recusada pelo validador da Fase 3 | trecho_nao_encontrado |  | recusa | passa |  | n/a | Retificar trecho para: "Adicionar exemplo de conversão incorreta de valor_produto DECIMAL(9,2) para float, causando arredondamento (ex: 89.90 -> 8990.0)." |
| `tra-13` | 1 | nota | `chave_de_juncao_errada` | recusada pelos filtros da Fase 4 | redundante |  | recusa | passa |  | n/a | Adicionar que a junção entre tbprodutos e tbtipos deve ser corrigida, garantindo que id_tipo_produto esteja corretamente ligado a tbtipos.id_tipo. |
| `tra-14` | 1 | nota | `contagem_inconsistente` | aceita pelos filtros de hoje |  | Parcial | recusa | passa |  | passa | Adicionar nota sobre a necessidade de incluir o total na resposta da API /api/produtos, para evitar contagens inconsistentes. |
| `tra-14` | 2 | novo_verbete | `contagem_total_inconsistente` | recusada pelo validador da Fase 3 | palavra_chave_invalida |  | recusa | passa |  | n/a | Adicionar verbete sobre a necessidade de manter consistência entre o total de itens na lista e na interface, evitando contagens inconsistentes. |
| `run-6` | 1 | retificacao | `erro_interno_do_servidor` | recusada pelo validador da Fase 3 | texto_longo |  | recusa | recusa | repeticao_razao | n/a | Adicionar que este erro pode ocorrer devido a falhas no banco de dados ou em rotas, e que a mensagem genérica pode esconder problemas específicos. Adicionar que este erro pode ocorrer de forma intermitente, sem padrão, e que pode ser causado por problemas no banco de dados ou rota. |
| `run-7` | 1 | nota | `recurso_inexistente` | recusada pelo validador da Fase 3 | palavra_chave_invalida |  | recusa | passa |  | n/a | Adicionar um exemplo de campo de busca errado, como login × id, para ilustrar melhor a causa raiz. |
| `run-8` | 1 | retificacao | `recurso_inexistente` | recusada pelo validador da Fase 3 | palavra_chave_invalida |  | recusa | passa |  | n/a | Adicionar um exemplo de campo de busca errado, como login × id, para ilustrar melhor a causa raiz. |
| `run-8` | 2 | novo_verbete | `rotas-inexistentes` | recusada pelo validador da Fase 3 | id_repetido |  | recusa | passa |  | n/a | Adicionar um novo verbete para rotas inexistentes, especificando que um 404 com id válido pode indicar que a rota ou recurso buscado não existe. |
| `run-11` | 1 | retificacao | `dado_desatualizado` | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso |  | recusa | passa |  | n/a | Corrigir a descrição do dado_desatualizado para enfatizar a leitura defasada devido a consultas ao banco em cada requisição. |
| `run-12` | 1 | nota | `erro_interno_do_servidor` | recusada pelo validador da Fase 3 | duplicada |  | recusa | passa |  | n/a | Adicionar que este erro pode ocorrer de forma intermitente, sem padrão, e que pode ser causado por problemas no banco de dados ou rota. |
| `run-12` | 2 | nota | `erro_interno_do_servidor` | aceita pelos filtros de hoje |  | Errada | recusa | passa |  | passa | Adicionar que a conversão de ErrorFault em 500 pode ser causada por problemas na rota. |
| `run-14` | 1 | nota | `dado_desatualizado` | recusada pelo validador da Fase 3 | palavra_chave_invalida |  | recusa | passa |  | n/a | Adiciona que a defasagem pode ser causada por cache do navegador, indicando que o usuário deve limpar cache ou recarregar a página. |
| `run-15` | 1 | nota | `tempo_de_resposta_excedido` | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso |  | recusa | passa |  | n/a | Adicionar nota sobre a necessidade de otimizar o tempo de resposta, evitando dormências fixas e atrasos maiores que possam ocorrer com o banco, rede ou carga. |
| `efe-6` | 1 | nota | `localizador_quebrado` | recusada pelo validador da Fase 3 | palavra_chave_invalida |  | recusa | passa |  | n/a | Adicione que a ausência de ORDER BY na API pode causar localizadores ambíguos. |
| `efe-6` | 2 | novo_verbete | `tempo_de_resposta_excedido` | recusada pelo validador da Fase 3 | id_repetido |  | recusa | passa |  | n/a | Adicione que atrasos maiores podem ser causados por problemas na infraestrutura, como banco de dados, rede ou carga. |
| `efe-8` | 1 | nota | `estado_da_tela_divergente` | aceita pelos filtros de hoje |  | Parcial | recusa | passa |  | passa | Adicionar nota sobre a necessidade de atualização correta do estado da tela após a resposta da API. |
| `efe-8` | 2 | novo_verbete | `atualizacao-da-tela` | aceita pelos filtros de hoje |  | Parcial | recusa | passa |  | passa | Adicionar verbete sobre a necessidade de atualização correta do estado da tela após a resposta da API, utilizando promises ou async/await. |
| `efe-9` | 1 | nota | `localizador_quebrado` | recusada pelo validador da Fase 3 | palavra_chave_invalida |  | recusa | passa |  | n/a | Adicionado que o localizador pode ser ambíguo, encontrando mais de um elemento com o mesmo seletor. |
| `efe-9` | 2 | retificacao | `localizador_quebrado` | recusada pelo validador da Fase 3 | palavra_chave_invalida |  | recusa | passa |  | n/a | Corrigido para "a lista da API não tem ORDER BY (produtos.py:38)." |
| `efe-10` | 1 | nota | `interface-frontend` | aceita pelos filtros de hoje |  | Parcial | recusa | passa |  | passa | Adicionar nota sobre a importância de atualizações corretas do DOM e a dependência de redirects na interface frontend. |
| `efe-10` | 2 | retificacao | `contrato-produto` | recusada pelo validador da Fase 3 | trecho_nao_encontrado |  | recusa | recusa | termos_sem_expansao_n | n/a | Retificar para: Notas: Notar que o contrato especifica a estrutura do JSON esperado, mas não aborda o truncamento de resposta e a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro. |
| `efe-11` | 1 | nota | `localizador_quebrado` | aceita pelos filtros de hoje |  | Parcial | recusa | passa |  | passa | Adicionar que a falta de ORDER BY na consulta pode causar ordem aleatória indeterminada dos produtos. |
| `efe-11` | 2 | novo_verbete | `ordem_aleatoria` | recusada pelo validador da Fase 3 | teto_verbetes_novos |  | recusa | passa |  | n/a | Adicionar que a ordem aleatória dos produtos pode ser causada por falta de ORDER BY na consulta, inconsistências na contagem e problemas no localizador. |
| `efe-12` | 1 | nota | `localizador_quebrado` | recusada pelos filtros da Fase 4 | redundante |  | recusa | passa |  | n/a | Adicionar que o seletor pode ser ambíguo, encontrando mais de um elemento com o mesmo seletor. |
| `efe-12` | 2 | retificacao | `localizador_quebrado` | recusada pelo validador da Fase 3 | texto_longo |  | recusa | passa |  | n/a | Corrigir para "o roteiro não acha o elemento (seletor não casa) ou acha mais de um (ambíguo). O problema é o localizador, não o dado. Elementos reais de produtos_api.php: #produtos-api-grid, .thumbnail, button.saiba-mais[data-id], #modalDetalhe; a lista da API não tem ORDER BY (produtos.py:38)." |
| `efe-13` | 1 | nota | `estado_da_tela_divergente` | aceita pelos filtros de hoje |  | Errada | passa | passa |  | passa | O cancelamento depende de um redirect, o que pode causar divergência na interface. |
| `efe-13` | 2 | novo_verbete | `cancelamento_via_redirect` | recusada pelo validador da Fase 3 | teto_verbetes_novos |  | passa | passa |  | n/a | O cancelamento é feito via redirect, que pode não atualizar a interface corretamente. |
| `efe-15` | 1 | novo_verbete | `estado_da_tela_divergente` | recusada pelo validador da Fase 3 | id_repetido |  | recusa | passa |  | n/a | Adicionar que o cancelamento pode falhar visualmente na tela, mesmo que a API confirme, devido à atualização do DOM via innerHTML. |
| `efe-15` | 2 | retificacao | `estado_da_tela_divergente` | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso |  | recusa | passa |  | n/a | Corrigir para mencionar que o cancelamento depende de um redirect, não apenas da atualização do DOM via innerHTML. |
| `lex-13` | 1 | novo_verbete | `corpo_vazio` | recusada pelo validador da Fase 3 | id_repetido |  | recusa | passa |  | n/a | Adicionar: "Nenhuma resposta ou resposta vazia pode ser retornada por nenhuma rota da CobaiaAPI." |
| `lex-14` | 1 | nota | `resposta_truncada` | recusada pelo validador da Fase 3 | duplicada |  | recusa | passa |  | n/a | Adicione um exemplo de como verificar o Content-Length na documentação para evitar esse problema. |
| `lex-14` | 2 | novo_verbete | `resposta_truncada_correta` | recusada pelo validador da Fase 3 | teto_verbetes_novos |  | recusa | passa |  | n/a | Cria um verbete dedicado para a resposta truncada correta, incluindo o exemplo de verificação do Content-Length. |
| `lex-15` | 1 | nota | `corpo_nao_e_json` | recusada pelos filtros da Fase 4 | mensagem_nao_encontrada_no_codigo |  | recusa | recusa | repeticao_razao | n/a | Adicionar um exemplo de sintoma específico, como "Página de erro HTML em vez de JSON", para melhorar a identificação de casos onde o corpo da resposta não é JSON. Adicionar um exemplo de sintoma para clarificar que XML também pode causar parse falho. |
| `lex-15` | 2 | retificacao | `corpo_nao_e_json` | recusada pelo validador da Fase 3 | retificacao_sem_trecho |  | recusa | passa |  | n/a | Adicionar que este erro pode ocorrer devido a falhas de conexão no site que imprime "Atenção ERRO" em HTML (connect.php:16); Warning/Fatal do PHP saem antes da saída; gateway fora devolve a própria página. |
<!-- /tabela:tb_f4_portoes_propostas -->
