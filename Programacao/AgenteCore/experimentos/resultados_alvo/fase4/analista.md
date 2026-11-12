<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase4.py --analista a partir de `fase4_analista` (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# O analista de documentação com a ficha curta do caso (corrida 27, medida M2), gerada em 2026-11-12

Medida M2 da proposta do analista de documentação (corrida 27, decisão 121). Nos casos de aprendizado da corrida 20, o modelo foi chamado no papel de analista de documentação: recebeu as instruções próprias (hash `cbc4505b3c2052f1`), o verbete da causa certa e a ficha curta do caso, montada por código a partir da trilha da corrida 20, com o gabarito no lugar da decisão da pessoa, e devolveu uma proposta só. A biblioteca é a de antes do lote da corrida 20 e só foi lida; nada do agente mudou.

Regra fixada antes da corrida (decisão 121). Três leituras contra a corrida 20, cada uma com um teste exato bilateral e o corte de 0,05. A abstenção: os casos em que o modelo responde que não há o que acrescentar, pareados caso a caso com a corrida 20 (McNemar). A forma do texto: a parcela das propostas com texto que afirmam um fato, isto é, que passam no portão da forma de instrução, contra a mesma conta nas propostas da corrida 20 (Fisher). A parcela correta: entre as propostas que passam nos filtros de hoje, as que a revisão humana às cegas julga corretas, contra as edições da corrida 20 (Fisher); essa leitura só tem veredito depois da revisão. Vale com a corrida completa e a ponte da versão do Ollama pareável com a Fase 3 (b + c até 2, decisão 47). Nenhum resultado muda o agente: a proposta do analista de documentação é base de desenho para depois da Fase 5.

A corrida rodou em outra versão do Ollama que a corrida 20; a ponte dessa versão (`fase3b_ponte_04015`) deu b = 1 e c = 0 em 35 casos, pareável com a Fase 3 (limite 2).

O que o analista respondeu em 54 casos: 0 abstenções, 20 respostas sem proposta válida e 34 propostas (19 sinais de busca, 15 notas e 0 retificações). Das 15 propostas com texto, 14 afirmam um fato e passam no portão da forma; na corrida 20 eram 6 de 92. Passam nos filtros de hoje 8 (na corrida 20, 20 de 92), e nos cinco portões 4. Cada chamada leu 1153,5 tokens e escreveu 110 na mediana, em 49,36 s; na corrida 20 eram 2358, 361 e 158,22 s.

<!-- tabela:tb_f4_analista_resumo -->
| Casos | Abstenções | Sem proposta válida | Propostas | Sinais de busca | Notas | Retificações | Com texto | Afirmam um fato | Passam nos filtros de hoje | Passam nos cinco portões | Cópias do exemplo das instruções | Tokens lidos (mediana) | Tokens escritos (mediana) | Segundos (mediana) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 54 | 0 | 20 | 34 | 19 | 15 | 0 | 15 | 14 | 8 | 4 | 1 | 1153,5 | 110 | 49,36 |
<!-- /tabela:tb_f4_analista_resumo -->
<!-- tabela:tb_f4_analista_leituras -->
| Leitura | Corrida 27 | Corrida 20 | Teste | p | Veredito |
|---|---|---|---|---|---|
| abstenção | 0 de 54 | 0 de 54 | McNemar pareado por caso | 1,000 | dentro do ruído |
| forma do texto | 14 de 15 | 6 de 92 | Fisher | 0,000 | sai do ruído: mais afirmações na corrida 27 |
| parcela correta | sem revisão | 2 de 20 | Fisher | n/d | sem veredito: falta a revisão humana às cegas das propostas |
<!-- /tabela:tb_f4_analista_leituras -->
<!-- tabela:tb_f4_analista_portoes -->
| Portão | Propostas avaliadas | Recusa | Passa | Não se aplica | Propostas que pararam aqui |
|---|---|---|---|---|---|
| portão 1, o validador da Fase 3 | 34 | 8 | 26 | 0 | 8 |
| portão 2, os filtros da Fase 4 | 26 | 18 | 8 | 8 | 18 |
| portão 3, a forma de instrução | 15 | 1 | 14 | 19 | 0 |
| portão 4, os filtros de texto | 15 | 1 | 14 | 19 | 0 |
| portão 5, a busca | 26 | 17 | 9 | 8 | 4 |
<!-- /tabela:tb_f4_analista_portoes -->
<!-- tabela:tb_f4_analista_destino -->
| O que aconteceu com a resposta | Casos |
|---|---|
| abstenção | 0 |
| sem proposta válida | 20 |
| recusada pelo validador da Fase 3 | 8 |
| recusada pelos filtros da Fase 4 | 18 |
| recusada pela forma de instrução | 0 |
| recusada pelos filtros de texto | 0 |
| recusada pelo portão da busca | 4 |
| passa nos cinco portões | 4 |
<!-- /tabela:tb_f4_analista_destino -->
<!-- tabela:tb_f4_analista_lacuna -->
| Grupo de casos | Casos | Abstenções | Sem proposta válida | Propostas | Passam nos filtros de hoje | Passam nos cinco portões |
|---|---|---|---|---|---|---|
| com lacuna | 20 | 0 | 3 | 17 | 5 | 1 |
| sem lacuna | 34 | 0 | 17 | 17 | 3 | 3 |
| diagnóstico certo | 37 | 0 | 17 | 20 | 3 | 3 |
| diagnóstico errado | 17 | 0 | 3 | 14 | 5 | 1 |
<!-- /tabela:tb_f4_analista_lacuna -->
<!-- tabela:tb_f4_analista_origem -->
| De onde o diagnóstico leu o caso | Casos | Abstenções | Sem proposta válida | Propostas | Passam nos filtros de hoje | Passam nos cinco portões |
|---|---|---|---|---|---|---|
| fixture | 30 | 0 | 13 | 17 | 2 | 0 |
| tela | 24 | 0 | 7 | 17 | 6 | 4 |
<!-- /tabela:tb_f4_analista_origem -->
<!-- tabela:tb_f4_analista_codigos -->
| Portão em que parou | Código da recusa | Casos |
|---|---|---|
| formato | bloco_malformado | 20 |
| filtros | sem_evidencia_do_caso | 15 |
| busca | busca | 4 |
| validador | palavra_chave_invalida | 4 |
| filtros | redundante | 2 |
| validador | texto_curto | 2 |
| filtros | mensagem_nao_encontrada_no_codigo | 1 |
| validador | copia_do_caso | 1 |
| validador | duplicada | 1 |
<!-- /tabela:tb_f4_analista_codigos -->
<!-- tabela:tb_f4_analista_casos -->
| Caso | Origem | Diagnóstico certo | Com lacuna | Operação | O que aconteceu | Código | Afirma um fato | Texto ou termos | Tokens lidos | Segundos |
|---|---|---|---|---|---|---|---|---|---|---|
| `lex-2` | tela | sim | não | nota | passa nos cinco portões |  | sim | A resposta não é JSON: veio como página ou texto com marcação. | 1237 | 83,14 |
| `lex-3` | tela | sim | não | nota | recusada pelos filtros da Fase 4 | redundante | sim | Nenhuma resposta ou resposta vazia pode ser retornada por nenhuma rota da CobaiaAPI. | 1196 | 47,89 |
| `lex-5` | fixture | sim | não | nota | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso | sim | O modo malformed_json devolve corpo cortado de propósito (produtos.py:19). Fora dele: limite num proxy, conexão encerrada durante o envio, ou Content-Length menor que o esperado. | 1120 | 50,68 |
| `sin-1` | tela | sim | não | nota | passa nos cinco portões |  | sim | O campo preco retorna undefined quando ausente, causando botões sem valor. | 1152 | 47,91 |
| `sin-2` | tela | sim | não |  | sem proposta válida | bloco_malformado |  | O campo preco veio com o nome preco_v2. | 1218 | 48,36 |
| `sin-3` | tela | não | sim |  | sem proposta válida | bloco_malformado |  | Adicionar exemplo de estrutura aninhada divergente no verbete | 1242 | 54,22 |
| `semt-2` | tela | sim | não |  | sem proposta válida | bloco_malformado |  | O campo destaque é convertido incorretamente, causando falhas em ordenação e soma. | 1150 | 51,43 |
| `semt-4` | fixture | sim | não |  | sem proposta válida | bloco_malformado |  | A API devolve data_pedido.isoformat() (pedidos.py:23), sempre AAAA-MM-DD. Em escala_ou_unidade_errada a data é legível mas deslocada; aqui é ilegível. | 1084 | 53,2 |
| `tra-2` | fixture | não | sim | sinal_de_busca | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso |  | junção, registro errado, campo derivado, nome de usuário incorreto, reserva de outro cliente, junção incorreta | 1319 | 64,24 |
| `tra-3` | tela | não | sim | sinal_de_busca | recusada pelo portão da busca | busca |  | junção, tipo, produto, campo derivado, campo tipo divergente, tipo de produto errado, junção incorreta | 1262 | 39,47 |
| `tra-5` | fixture | não | sim | sinal_de_busca | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso |  | escala, unidade, arredondamento, conversão, fator, reserva_inconsistente, quantidade_incorreta, listagem_diferente | 1275 | 77 |
| `run-3` | tela | sim | sim | sinal_de_busca | recusada pelo validador da Fase 3 | palavra_chave_invalida |  | 429, excesso_de_requisicoes, limitador, main.py, CORS, funcionalidade intermitente, recarregamento, objeto em vez de lista, campos ausentes | 1205 | 56,43 |
| `run-5` | fixture | sim | sim | sinal_de_busca | recusada pelo validador da Fase 3 | palavra_chave_invalida |  | duplicidade, POST, idempotência, POST /api/pedidos seguido de GET /api/pedidos, registros idênticos | 1094 | 46,36 |
| `efe-4` | fixture | não | sim | sinal_de_busca | recusada pelo validador da Fase 3 | copia_do_caso |  | api, resposta, lista, estado, divergência, lista_vazia, carregando_parado, filtro_categoria | 1111 | 49,84 |
| `lex-6` | fixture | não | sim | nota | recusada pelo validador da Fase 3 | duplicada | não | Adicionar um exemplo de sintoma específico, como "Página de erro HTML em vez de JSON", para melhorar a identificação de casos onde o corpo da resposta não é JSON. | 1142 | 47,63 |
| `lex-9` | tela | sim | não | nota | passa nos cinco portões |  | sim | A resposta não é JSON: veio como página ou texto com marcação. | 1238 | 37,05 |
| `lex-12` | tela | sim | não | nota | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso | sim | A resposta não é JSON: veio como página ou texto com marcação. | 1238 | 19,76 |
| `sin-6` | tela | sim | não | nota | recusada pelo validador da Fase 3 | texto_curto | sim | O campo nome é retornado como undefined no JavaScript. | 1143 | 47,23 |
| `sin-8` | fixture | sim | não |  | sem proposta válida | bloco_malformado |  | O campo "tipo" deve ser tratado como uma string, não uma lista. | 1166 | 46,38 |
| `sin-9` | tela | sim | não |  | sem proposta válida | bloco_malformado |  | O campo nome veio com o nome nome_v2, causando desalinhamento na exibição da tela. | 1211 | 56,19 |
| `sin-12` | fixture | não | sim | sinal_de_busca | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso |  | campo ausente, contrato, pedido, reserva, item desaparecido na tela, campo ausente no objeto retornado, reserva incompleta | 1083 | 50,67 |
| `sin-13` | tela | não | sim | nota | passa nos cinco portões |  | sim | O campo tipo pode ser representado como um objeto ou uma lista simples, dependendo da versão do contrato. | 1276 | 57,48 |
| `sin-15` | fixture | sim | não | nota | recusada pelos filtros da Fase 4 | redundante | sim | O campo "tipo" deve ser tratado como uma string, não uma lista. | 1155 | 44,73 |
| `semt-6` | tela | não | sim | sinal_de_busca | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso |  | type_drift, campo_inteiro, converção_erros, campo_id_texto, lista_incompleta, ids_faltantes | 1206 | 49,98 |
| `semt-7` | fixture | não | sim | sinal_de_busca | recusada pelo portão da busca | busca |  | soma_total, reservas, campo_inteiro, soma errada, campo reservas como texto, ordenação incorreta | 1077 | 38,9 |
| `semt-10` | tela | sim | não |  | sem proposta válida | bloco_malformado |  | O campo destaque é convertido incorretamente em texto. | 1150 | 37,66 |
| `semt-11` | fixture | sim | não |  | sem proposta válida | bloco_malformado |  | O contrato define status como 'Em Análise'/'Cancelado'. | 1117 | 44,9 |
| `semt-12` | fixture | sim | não |  | sem proposta válida | bloco_malformado |  | O serviço de e-mail responde 202 antes de entregar a mensagem. | 1096 | 49,35 |
| `semt-13` | tela | sim | não | sinal_de_busca | recusada pelo validador da Fase 3 | palavra_chave_invalida |  | tipo_divergente, campo_preco, convercao_numerica, campo com valor numérico vindo como texto, falha ao ordenar ou somar, converção incorreta de vírgula para ponto | 1057 | 46,1 |
| `semt-15` | fixture | sim | não |  | sem proposta válida | bloco_malformado |  | Adicionar validação no status do pedido na API para evitar valores fora do domínio. | 1148 | 49,36 |
| `tra-6` | tela | sim | não | sinal_de_busca | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso |  | arredondamento, conversão, unidade, decimal, float, arredondamento incorreto, conversão decimal para float, unidade de medida errada | 1358 | 73,97 |
| `tra-7` | tela | não | sim | sinal_de_busca | recusada pelo portão da busca | busca |  | junção, registro, campo derivado, campo derivado incorreto, junção incorreta, valor de registro errado | 1375 | 44,2 |
| `tra-9` | fixture | não | sim | sinal_de_busca | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso |  | formato_de_data, divergência, data_pedido, data deslocada um dia, formato de data divergente | 1276 | 54,37 |
| `tra-12` | tela | sim | não | sinal_de_busca | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso |  | arredondamento, conversão, decimal, float, arredondamento incorreto, conversão decimal para float, valores fora da escala esperada | 1376 | 49,25 |
| `tra-13` | tela | não | sim | sinal_de_busca | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso |  | junção, registro, campo derivado, campo imagem errado, junção incorreta, substring de CPF | 1288 | 39,04 |
| `tra-14` | tela | sim | não |  | sem proposta válida | bloco_malformado |  | GET /api/produtos devolve lista com menos itens que o total indicado no envelope. | 1151 | 49,38 |
| `run-6` | fixture | sim | não | nota | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso | sim | O banco inacessível ou defeito na rota pode causar erro interno do servidor (500) com detalhes genéricos. | 1183 | 55,58 |
| `run-7` | tela | sim | não |  | sem proposta válida | bloco_malformado |  | A resposta veio como objeto sem campos esperados. | 1267 | 54,83 |
| `run-8` | fixture | sim | não | nota | recusada pelo validador da Fase 3 | texto_curto | sim | "Cada 404 com mensagem vem de db.get/filter vazio na rota." | 1183 | 36,36 |
| `run-11` | fixture | não | sim |  | sem proposta válida | bloco_malformado |  | A API lê o banco de dados diretamente, mas a interface web usa cache. | 1111 | 47,73 |
| `run-12` | fixture | sim | não |  | sem proposta válida | bloco_malformado |  | Este erro pode ocorrer de forma intermitente, sem padrão, devido a falhas no banco de dados ou em rotas, resultando em uma mensagem genérica que pode esconder problemas específicos. | 1200 | 63,15 |
| `run-14` | fixture | sim | não |  | sem proposta válida | bloco_malformado |  | A API lê o banco a cada requisição (database.py) e não envia cache; leitura defasada indica proxy ou cache do navegador entre a página e a API. | 1111 | 54,59 |
| `run-15` | tela | sim | sim | sinal_de_busca | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso |  | tempo_de_resposta, latência, fetch, dormência, latência_inesperada, tempo_de_resposta_longo, dormência_fixa | 1106 | 49,84 |
| `efe-6` | fixture | sim | não |  | sem proposta válida | bloco_malformado |  | O seletor pode ser ambíguo, encontrando mais de um elemento com o mesmo identificador. | 1148 | 46,75 |
| `efe-8` | fixture | sim | não | sinal_de_busca | recusada pelo validador da Fase 3 | palavra_chave_invalida |  | estado_da_tela_divergente, fetch, innerHTML, redirect, API responde com sucesso, mas tela não atualiza; fetch não atualiza estado corretamente | 1072 | 46,46 |
| `efe-9` | fixture | sim | não |  | sem proposta válida | bloco_malformado |  | O seletor pode ser ambíguo, encontrando mais de um elemento com o mesmo atributo. | 1145 | 53,05 |
| `efe-10` | fixture | não | sim | sinal_de_busca | recusada pelo portão da busca | busca |  | estado_da_tela_divergente, fetch, innerHTML, cliente_cancelar.php, preco_incorreto, carregamento_parado, grid_vazio | 1171 | 60,73 |
| `efe-11` | fixture | não | sim | sinal_de_busca | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso |  | estado_da_tela_divergente, fetch, innerHTML, grid, cliente_cancelar.php, recarregamento da página, ordem aleatória dos cartões, localizador quebrado | 1061 | 46,63 |
| `efe-12` | fixture | sim | não |  | sem proposta válida | bloco_malformado |  | O seletor pode ser ambíguo, encontrando mais de um botão de preço. | 1142 | 47,74 |
| `efe-13` | fixture | não | sim |  | sem proposta válida | bloco_malformado |  | A tela mostra o preço antigo do produto 3, embora a última resposta da API traga 74.9; a página substitui o grid inteiro a cada resposta recebida. | 1160 | 56,11 |
| `efe-15` | fixture | sim | não |  | sem proposta válida | bloco_malformado |  | O cliente_cancelar.php:7 não executa o redirect após o cancelamento, deixando o estado do pedido inalterado na tela. | 1109 | 46,74 |
| `lex-13` | fixture | sim | não | nota | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso | sim | Nenhuma resposta ou resposta vazia pode ser retornada por nenhuma rota da CobaiaAPI. | 1112 | 44,11 |
| `lex-14` | fixture | sim | não | nota | recusada pelos filtros da Fase 4 | sem_evidencia_do_caso | sim | O modo malformed_json devolve corpo cortado de propósito (produtos.py:19). Fora dele: limite num proxy, conexão encerrada durante o envio, verifique o Content-Length na documentação. | 1127 | 51,8 |
| `lex-15` | tela | sim | não | nota | recusada pelos filtros da Fase 4 | mensagem_nao_encontrada_no_codigo | sim | O sintoma "Erro ao carregar produtos da CobaiaAPI: Unexpected token '<', \"<html><bod\"... is not valid JSON" é um caso específico de [corpo_nao_e_json]. | 1238 | 51,83 |
<!-- /tabela:tb_f4_analista_casos -->
