<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por gerar_conferencia_ineditos.py a partir de banco_casos_ineditos_fase4.py, reproducibilidade_ineditos.json e conferencia_ineditos_preanalise.json (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Conferência dos 36 inéditos da ficha 27, gerada em 2026-11-05

Os casos que a corrida 24 vai medir (decisão 92). O agente recebe cada caso sem o gabarito e escolhe uma das 23 causas; um caso ruim mede o modelo contra algo que o sistema não produz, ou contra uma resposta com mais de uma leitura honesta. A pergunta de cada caso: a causa do gabarito é a leitura certa do que o corpo e o sintoma mostram? A pré-análise é do Claude, feita só lendo o código, e diz onde olhar com mais cuidado: 10 casos para olhar e 26 sem nada a apontar. Ela não é a conferência: quem confere é o Eric. "Na corrida 17" diz o que a falha injetada fez de verdade: 25 casos reproduzem na tela e 11 ficam fora dela, porque a rota não tem tela ou o caso é um cenário descrito.

<!-- tabela:tb_f4_conferencia_classes -->
| Classe | Casos | Reproduzem na tela | Sem nada a apontar | Para olhar |
|---|---|---|---|---|
| 1 | 6 | 5 | 5 | 1 |
| 2 | 6 | 6 | 5 | 1 |
| 3 | 6 | 5 | 4 | 2 |
| 4 | 6 | 5 | 5 | 1 |
| 5 | 6 | 4 | 4 | 2 |
| 6 | 6 | 0 | 3 | 3 |
<!-- /tabela:tb_f4_conferencia_classes -->
<!-- tabela:tb_f4_conferencia_ver -->
| Caso | Causa do gabarito | Outra causa que caberia | O que olhar | Onde |
|---|---|---|---|---|
| `lex-27` | `codificacao_incorreta` | `valor_fora_do_dominio` | O contrato do caso diz que status e 'Em Analise' ou 'Cancelado', e o corpo traz 'Em AnÃ¡lise', que sai desse conjunto; um modelo pode responder valor_fora_do_dominio, justamente a causa que o gabarito proíbe. A observação ainda cita 'Em Análise' com acento, enquanto o contrato escreve sem acento. Caso sem tela (POST de pedidos), então a reação da tela não se aplica. | `CobaiaAPI/app/routers/pedidos.py:63` |
| `sin-24` | `estrutura_aninhada_divergente` | `tipo_divergente` | O contrato pede tipo como texto e chegou um objeto; pela definição 'tipo trocado' de tipo_divergente isso também cabe, e o diff de contrato da corrida 17 classificou este caso como tipo_diferente. O que decide a favor do gabarito é o objeto {valor, moeda} embrulhando o texto original. | `CobaiaAPI/app/fault_injection.py:193` |
| `semt-26` | `nulo_inesperado` | `estado_da_tela_divergente` | O contrato do caso e a observação dizem que resumo aceita nulo, então o null em si não é 'inesperado'; o que há de errado é a lista ter trazido o texto e o detalhe do mesmo produto vir sem ele, e o cartão e o modal da tela divergirem. Um modelo pode responder estado_da_tela_divergente (ou campo_ausente) com boa razão. | `CobaiaAPI/app/schemas.py:19` |
| `semt-27` | `valor_fora_do_dominio` | `recurso_inexistente` | O corpo mostrado (GET /api/produtos) tem ids negativos, mas o sintoma gira em torno do 404 do detalhe, então recurso_inexistente é uma leitura natural, e ela está nos termos proibidos. Confira se o gabarito deixa claro que o 404 é consequência do id negativo vindo da lista. Também cabe chave_de_juncao_errada, já que é o id usado para ligar cartão e detalhe. | `CobaiaAPI/app/routers/produtos.py:63` |
| `tra-27` | `escala_ou_unidade_errada` | nenhuma | O sintoma diz que a conferência de preço do roteiro falha comparando o detalhe com o cartão, mas o modal de produtos_api.php:121-122 só mostra nome e resumo, então a tela não faz essa comparação sozinha. Só a leitura do código não prova que o harness da Fase 4 tem essa conferência para o detalhe (a corrida 17 só registrou diferença de corpo neste caso). | `CobaiaFront/produtos_api.php:121` |
| `run-26` | `dado_desatualizado` | nenhuma | A CobaiaAPI não tem cache (o próprio comentário do caso admite) e cancelar_pedido grava e faz commit antes de responder, então o sistema nunca produz este corpo; é um cenário descrito, sem modo, e a corrida 17 o deixou fora. Decida se vale medir o modelo contra algo que a API não gera. | `CobaiaAPI/app/routers/pedidos.py:69` |
| `run-27` | `registro_duplicado` | `erro_interno_do_servidor` | O sintoma abre com um 500 seguido de nova tentativa, então erro_interno_do_servidor é uma leitura honesta (foi o 500 que levou à duplicata, e criar_pedido faz commit antes do apply_fault). Ela está nos termos proibidos, mas confira se o enunciado separa bem 'o que o modelo deve apontar' (duas reservas iguais na listagem) da origem do problema. Caso sem tela, e a sequência 500 e retry só se confirma rodando. | `CobaiaAPI/app/routers/pedidos.py:53` |
| `efe-24` | `localizador_quebrado` | `estado_da_tela_divergente` | O clique funciona e o modal não abre, sem nenhuma requisição na rede; sem ler o nth=0 no seletor, estado_da_tela_divergente também caberia. O que sustenta o gabarito é que o primeiro button do cartão é o de preço (produtos_api.php:81), sem handler de clique. | `CobaiaFront/produtos_api.php:81` |
| `efe-26` | `estado_da_tela_divergente` | `tempo_de_resposta_excedido` | O sintoma diz que a resposta do id 3 chega cerca de 2 segundos depois da do id 9, então tempo_de_resposta_excedido é uma leitura possível, embora esteja nos termos proibidos. A sobreposição do modal pela resposta tardia (produtos_api.php:120-123, sem conferir qual clique foi o último) é o que sustenta o gabarito. Depende de execução: se o harness consegue armar a ordem inversa. | `CobaiaFront/produtos_api.php:112` |
| `efe-27` | `estado_da_tela_divergente` | `dado_desatualizado` | O cartão mostra o preço antigo e a API devolve o novo, o que é muito parecido com dado_desatualizado (que o gabarito proíbe). A diferença é que a defasagem está na página, que busca a lista uma só vez (produtos_api.php:132), e não no dado servido pela API. O Eric deve decidir se essa distinção é clara o bastante para um modelo. | `CobaiaFront/produtos_api.php:132` |
<!-- /tabela:tb_f4_conferencia_ver -->

## Os casos, com os para olhar primeiro

### `lex-27`, classe 1, nível 3: `codificacao_incorreta` (para olhar)

- **Requisição:** `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 3, "data_pedido": "2026-12-05"})`
- **Status:** 201
- **Contrato:** `id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto`
- **Corpo:** `{"id_pedido": 10, "pessoas": 3, "data_pedido": "2026-12-05", "status": "Em AnÃ¡lise", "nome": "Cliente Teste", "cpf": "11122233344"}`
- **Sintoma:** A reserva e criada (status 201), mas o campo status da resposta traz 'Em AnÃ¡lise', com simbolos estranhos no lugar do acento.
- **Observação:** Consultando o banco direto, tbpedido_reserva guarda a reserva 10 com status 'Em Análise'.
- **Gabarito:** causa `codificacao_incorreta`; campo `status`; termos esperados `codifica`, `encoding`, `acent`; termos proibidos `fora_do_dominio`, `tipo_divergente`
- **Na corrida 17:** fora: sem tela: a rota 'POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 3, "data_pedido": "2026-12-05"})' não é consumida por página nenhuma
- **Pré-análise:** O contrato do caso diz que status e 'Em Analise' ou 'Cancelado', e o corpo traz 'Em AnÃ¡lise', que sai desse conjunto; um modelo pode responder valor_fora_do_dominio, justamente a causa que o gabarito proíbe. A observação ainda cita 'Em Análise' com acento, enquanto o contrato escreve sem acento. Caso sem tela (POST de pedidos), então a reação da tela não se aplica. Outra causa que caberia: `valor_fora_do_dominio`. (`CobaiaAPI/app/routers/pedidos.py:63`)

### `sin-24`, classe 2, nível 2: `estrutura_aninhada_divergente` (para olhar)

- **Requisição:** `GET /api/produtos`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `[{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": {"valor": "Carnes", "moeda": "BRL"}, "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": {"valor": "Carnes", "moeda": "BRL"}, "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]`
- **Sintoma:** Sob o nome de cada produto, a linha da categoria mostra o texto {"valor":"Carnes","moeda":"BRL"} em vez de apenas Carnes. O resto de cada cartao esta normal.
- **Gabarito:** causa `estrutura_aninhada_divergente`; campo `tipo`; termos esperados `aninhad`, `objeto`, `valor`; termos proibidos `renomead`, `truncad`
- **Na corrida 17:** reproduz: diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais
- **Pré-análise:** O contrato pede tipo como texto e chegou um objeto; pela definição 'tipo trocado' de tipo_divergente isso também cabe, e o diff de contrato da corrida 17 classificou este caso como tipo_diferente. O que decide a favor do gabarito é o objeto {valor, moeda} embrulhando o texto original. Outra causa que caberia: `tipo_divergente`. (`CobaiaAPI/app/fault_injection.py:193`)

### `semt-26`, classe 3, nível 3: `nulo_inesperado` (para olhar)

- **Requisição:** `GET /api/produtos/12`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `{"id": 12, "nome": "Queijo Coalho", "resumo": null, "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true}`
- **Sintoma:** O cartao do Queijo Coalho na grade mostra a descricao 'Queijo coalho grelhado com mel', mas o modal aberto pelo 'Saiba Mais...' desse mesmo produto mostra '(sem descrição)'. As duas respostas chegaram com status 200.
- **Observação:** A listagem GET /api/produtos, feita antes do clique, trouxe este produto (id 12) com o resumo preenchido. O contrato permite resumo nulo (texto|nulo).
- **Gabarito:** causa `nulo_inesperado`; campo `resumo`; termos esperados `nulo`, `null`, `resumo`; termos proibidos `campo_ausente`, `desatualizad`
- **Na corrida 17:** reproduz: corpo diferente da referência em modo normal; árvore diferente da referência: 15 linha(s) a menos e 15 a mais
- **Pré-análise:** O contrato do caso e a observação dizem que resumo aceita nulo, então o null em si não é 'inesperado'; o que há de errado é a lista ter trazido o texto e o detalhe do mesmo produto vir sem ele, e o cartão e o modal da tela divergirem. Um modelo pode responder estado_da_tela_divergente (ou campo_ausente) com boa razão. Outra causa que caberia: `estado_da_tela_divergente`. (`CobaiaAPI/app/schemas.py:19`)

### `semt-27`, classe 3, nível 3: `valor_fora_do_dominio` (para olhar)

- **Requisição:** `GET /api/produtos`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `[{"id": -2, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": -3, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 84.9, "imagem": "picanha_sem.jpg", "destaque": false}]`
- **Sintoma:** A grade carrega os 14 cartoes sem erro, mas qualquer 'Saiba Mais...' abre o modal com 'Erro' no titulo e 'HTTP 404' no corpo. Ao clicar no botao da Picanha ao Alho, a requisicao disparada foi GET /api/produtos/-2 e a resposta foi 404.
- **Observação:** O corpo mostra so os itens da Picanha ao Alho e da Picanha Simples; a lista completa tem 14.
- **Gabarito:** causa `valor_fora_do_dominio`; campo `id`; termos esperados `negativ`, `dominio`, `-2`; termos proibidos `recurso_inexistente`, `campo_ausente`
- **Na corrida 17:** reproduz: corpo diferente da referência em modo normal
- **Pré-análise:** O corpo mostrado (GET /api/produtos) tem ids negativos, mas o sintoma gira em torno do 404 do detalhe, então recurso_inexistente é uma leitura natural, e ela está nos termos proibidos. Confira se o gabarito deixa claro que o 404 é consequência do id negativo vindo da lista. Também cabe chave_de_juncao_errada, já que é o id usado para ligar cartão e detalhe. Outra causa que caberia: `recurso_inexistente`. (`CobaiaAPI/app/routers/produtos.py:63`)

### `tra-27`, classe 4, nível 3: `escala_ou_unidade_errada` (para olhar)

- **Requisição:** `GET /api/produtos/2`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `{"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 8490.0, "imagem": "picanha_sem.jpg", "destaque": false}`
- **Sintoma:** O modal da Picanha Simples abre normal (ele so mostra nome e descricao), mas a conferencia de preco do roteiro falha: o preco do detalhe nao bate com o do cartao.
- **Observação:** A listagem GET /api/produtos, feita antes, trouxe este produto (id 2) com preco 84.9, e o cartao mostra 'R$ 84,90'.
- **Gabarito:** causa `escala_ou_unidade_errada`; campo `preco`; termos esperados `escala`, `100`, `8490`; termos proibidos `desatualizad`, `fora_do_dominio`
- **Na corrida 17:** reproduz: corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais
- **Pré-análise:** O sintoma diz que a conferência de preço do roteiro falha comparando o detalhe com o cartão, mas o modal de produtos_api.php:121-122 só mostra nome e resumo, então a tela não faz essa comparação sozinha. Só a leitura do código não prova que o harness da Fase 4 tem essa conferência para o detalhe (a corrida 17 só registrou diferença de corpo neste caso). (`CobaiaFront/produtos_api.php:121`)

### `run-26`, classe 5, nível 3: `dado_desatualizado` (para olhar)

- **Requisição:** `GET /api/pedidos?login=11122233344`
- **Status:** 200
- **Contrato:** `id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto`
- **Corpo:** `[{"id_pedido": 8, "pessoas": 2, "data_pedido": "2026-11-20", "status": "Cancelado", "nome": "Cliente Teste", "cpf": "11122233344"}, {"id_pedido": 9, "pessoas": 4, "data_pedido": "2026-12-05", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]`
- **Sintoma:** Logo depois de POST /api/pedidos/9/cancelar responder 200 com status 'Cancelado', a consulta GET /api/pedidos?login=11122233344 ainda lista a reserva 9 como 'Em Analise'. A reserva 8, cancelada ontem, ja aparece como 'Cancelado'.
- **Observação:** Uma consulta direta ao banco (tbpedido_reserva) ja mostra a reserva 9 como 'Cancelado'. A mesma consulta GET /api/pedidos repetida cerca de 5 minutos depois traz o status novo.
- **Gabarito:** causa `dado_desatualizado`; campo nenhum; termos esperados `desatualizad`, `cache`, `antigo`; termos proibidos `estado_da_tela`, `valor_fora`
- **Na corrida 17:** fora: sem modo para a causa dado_desatualizado
- **Pré-análise:** A CobaiaAPI não tem cache (o próprio comentário do caso admite) e cancelar_pedido grava e faz commit antes de responder, então o sistema nunca produz este corpo; é um cenário descrito, sem modo, e a corrida 17 o deixou fora. Decida se vale medir o modelo contra algo que a API não gera. (`CobaiaAPI/app/routers/pedidos.py:69`)

### `run-27`, classe 5, nível 3: `registro_duplicado` (para olhar)

- **Requisição:** `GET /api/pedidos?login=11122233344`
- **Status:** 200
- **Contrato:** `id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto`
- **Corpo:** `[{"id_pedido": 18, "pessoas": 4, "data_pedido": "2026-12-19", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}, {"id_pedido": 19, "pessoas": 4, "data_pedido": "2026-12-19", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]`
- **Sintoma:** O roteiro envia POST /api/pedidos para uma reserva de 4 pessoas em 2026-12-19: a primeira tentativa respondeu 500, o roteiro tentou de novo e a segunda respondeu 201. A consulta GET /api/pedidos seguinte lista duas reservas identicas (ids 18 e 19, mesma data e mesmo numero de pessoas), embora so uma tenha sido pedida.
- **Observação:** O corpo mostra so as duas ultimas reservas do cliente. A resposta 500 da primeira tentativa nao trouxe nenhuma reserva, so uma mensagem de erro.
- **Gabarito:** causa `registro_duplicado`; campo nenhum; termos esperados `duplicad`, `repetid`, `500`; termos proibidos `erro_interno`, `contagem_inconsistente`
- **Na corrida 17:** fora: sem tela: a rota 'GET /api/pedidos?login=11122233344' não é consumida por página nenhuma
- **Pré-análise:** O sintoma abre com um 500 seguido de nova tentativa, então erro_interno_do_servidor é uma leitura honesta (foi o 500 que levou à duplicata, e criar_pedido faz commit antes do apply_fault). Ela está nos termos proibidos, mas confira se o enunciado separa bem 'o que o modelo deve apontar' (duas reservas iguais na listagem) da origem do problema. Caso sem tela, e a sequência 500 e retry só se confirma rodando. Outra causa que caberia: `erro_interno_do_servidor`. (`CobaiaAPI/app/routers/pedidos.py:53`)

### `efe-24`, classe 6, nível 2: `localizador_quebrado` (para olhar)

- **Requisição:** `GET /api/produtos`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `[{"id": 5, "nome": "Alcatra na Pedra", "resumo": "Alcatra grelhada servida na pedra quente", "tipo": "Carnes", "preco": 74.9, "imagem": "alcatra_pedra.jpg", "destaque": false}, {"id": 6, "nome": "Maminha", "resumo": "Corte macio grelhado na brasa", "tipo": "Carnes", "preco": 72.9, "imagem": "maminha.jpg", "destaque": false}]`
- **Sintoma:** O passo 'abrir os detalhes da Alcatra na Pedra' clica no seletor sem erro, mas o modal nao abre: o passo seguinte, que espera #modalDetalhe visivel, esgota o tempo. Depois do clique nao aparece nenhuma requisicao GET /api/produtos/5 na rede.
- **Seletor quebrado:** `.thumbnail:has-text("Alcatra na Pedra") button >> nth=0`
- **Árvore da tela:**

```text
document "Churrascaria Fornalha - Produtos (API)"
  navigation
    link "PRODUTOS"
    link "PRODUTOS (API)"
  main
    heading "Produtos via API" level=2
    group
      heading "Alcatra na Pedra" level=3
      text "Carnes"
      button "R$ 74,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="5"
    group
      heading "Maminha" level=3
      text "Carnes"
      button "R$ 72,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="6"

```

- **Gabarito:** causa `localizador_quebrado`; campo nenhum; termos esperados `seletor`, `botao`, `preco`; termos proibidos `recurso_inexistente`, `tempo_de_resposta`
- **Na corrida 17:** fora: armada pelo harness (ficha 29): localizador_quebrado
- **Pré-análise:** O clique funciona e o modal não abre, sem nenhuma requisição na rede; sem ler o nth=0 no seletor, estado_da_tela_divergente também caberia. O que sustenta o gabarito é que o primeiro button do cartão é o de preço (produtos_api.php:81), sem handler de clique. Outra causa que caberia: `estado_da_tela_divergente`. (`CobaiaFront/produtos_api.php:81`)

### `efe-26`, classe 6, nível 3: `estado_da_tela_divergente` (para olhar)

- **Requisição:** `GET /api/produtos/9`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `{"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", "destaque": true}`
- **Sintoma:** O roteiro clica em 'Saiba Mais...' da Fraldinha e, logo em seguida, no do Balde de Cerveja. As duas requisicoes (GET /api/produtos/3 e GET /api/produtos/9) respondem 200 com o corpo certo, mas a de id 3 chega cerca de 2 segundos depois da de id 9. O modal fica com o titulo e a descricao da Fraldinha; a verificacao esperava o Balde de Cerveja.
- **Observação:** O corpo mostrado e o da ultima requisicao disparada (id 9); a resposta do id 3 tambem tinha o corpo certo.
- **Árvore da tela:**

```text
document "Churrascaria Fornalha - Produtos (API)"
  navigation
    link "PRODUTOS"
    link "PRODUTOS (API)"
  main
    heading "Produtos via API" level=2
    group
      heading "Fraldinha" level=3
      text "Carnes"
      button "R$ 69,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    group
      heading "Balde de Cerveja" level=3
      text "Bebidas"
      button "R$ 45,00"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="9"
  dialog
    button "×" class="close"
    heading "Fraldinha" level=4 id="modalDetalheTitulo"
    text "Corte grelhado na brasa, fatiado na hora" id="modalDetalheCorpo"

```

- **Gabarito:** causa `estado_da_tela_divergente`; campo nenhum; termos esperados `estado`, `tela`, `ordem`; termos proibidos `tempo_de_resposta`, `chave_de_juncao`
- **Na corrida 17:** fora: armada pelo harness (ficha 29): estado_da_tela_divergente
- **Pré-análise:** O sintoma diz que a resposta do id 3 chega cerca de 2 segundos depois da do id 9, então tempo_de_resposta_excedido é uma leitura possível, embora esteja nos termos proibidos. A sobreposição do modal pela resposta tardia (produtos_api.php:120-123, sem conferir qual clique foi o último) é o que sustenta o gabarito. Depende de execução: se o harness consegue armar a ordem inversa. Outra causa que caberia: `tempo_de_resposta_excedido`. (`CobaiaFront/produtos_api.php:112`)

### `efe-27`, classe 6, nível 3: `estado_da_tela_divergente` (para olhar)

- **Requisição:** `GET /api/produtos/2`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `{"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 94.9, "imagem": "picanha_sem.jpg", "destaque": false}`
- **Sintoma:** A pagina foi aberta as 10:00 e mostrou a Picanha Simples por 'R$ 84,90'. As 10:05 o preco desse produto foi alterado no banco para 94,90. As 10:07 o roteiro consultou GET /api/produtos/2, que respondeu 200 com preco 94.9, e comparou com o cartao, que continua mostrando 'R$ 84,90'.
- **Observação:** A pagina nao foi recarregada entre as 10:00 e as 10:07.
- **Árvore da tela:**

```text
document "Churrascaria Fornalha - Produtos (API)"
  navigation
    link "PRODUTOS"
    link "PRODUTOS (API)"
  main
    heading "Produtos via API" level=2
    group
      heading "Picanha ao Alho" level=3
      text "Carnes"
      button "R$ 89,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      button "R$ 84,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"

```

- **Gabarito:** causa `estado_da_tela_divergente`; campo nenhum; termos esperados `estado`, `tela`, `recarreg`; termos proibidos `dado_desatualizado`, `escala`
- **Na corrida 17:** fora: armada pelo harness (ficha 29): estado_da_tela_divergente
- **Pré-análise:** O cartão mostra o preço antigo e a API devolve o novo, o que é muito parecido com dado_desatualizado (que o gabarito proíbe). A diferença é que a defasagem está na página, que busca a lista uma só vez (produtos_api.php:132), e não no dado servido pela API. O Eric deve decidir se essa distinção é clara o bastante para um modelo. Outra causa que caberia: `dado_desatualizado`. (`CobaiaFront/produtos_api.php:132`)

### `lex-22`, classe 1, nível 1: `corpo_nao_e_json`

- **Requisição:** `GET /api/produtos`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `<html><body><h1>Erro</h1><p>Falha ao montar a resposta.</p></body></html>`
- **Sintoma:** A pagina Produtos (API) abre sem nenhum cartao. A linha de status acima da grade fica vermelha e mostra 'Erro ao carregar produtos da CobaiaAPI:' seguido de uma mensagem do navegador que cita o caractere inesperado '<' e diz que o texto nao e JSON valido. O status HTTP da resposta e 200.
- **Observação:** O Content-Type da resposta e text/html, nao application/json.
- **Gabarito:** causa `corpo_nao_e_json`; campo nenhum; termos esperados `html`, `nao e json`, `text/html`; termos proibidos `truncad`, `erro_interno`
- **Na corrida 17:** reproduz: corpo nao_json; corpo diferente da referência em modo normal; árvore diferente da referência: 140 linha(s) a menos e 1 a mais; conferência 'grid com 14 cartões' falhou
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:231`)

### `lex-23`, classe 1, nível 1: `corpo_vazio`

- **Requisição:** `GET /api/produtos/6`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** ``
- **Sintoma:** Ao clicar em 'Saiba Mais...' da Maminha, o modal abre com 'Erro' no titulo e, no corpo, uma mensagem do navegador sobre 'Unexpected end of JSON input'. A resposta chegou com status 200 e Content-Length 0.
- **Gabarito:** causa `corpo_vazio`; campo nenhum; termos esperados `vazio`, `sem corpo`, `unexpected end`; termos proibidos `truncad`, `html`
- **Na corrida 17:** reproduz: corpo vazio; árvore diferente da referência: 144 linha(s) a menos e 1 a mais; conferência 'grid carregado antes do detalhe' falhou
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:229`)

### `lex-24`, classe 1, nível 2: `codificacao_incorreta`

- **Requisição:** `GET /api/produtos/14`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `{"id": 14, "nome": "Abacaxi na Brasa", "resumo": "Com canela e aÃ§Ãºcar", "tipo": "Sobremesas", "preco": 14.9, "imagem": "abacaxi.jpg", "destaque": false}`
- **Sintoma:** O modal do Abacaxi na Brasa abre com o titulo certo, mas o texto de descricao aparece como 'Com canela e aÃ§Ãºcar': cada letra acentuada virou um par de simbolos estranhos.
- **Gabarito:** causa `codificacao_incorreta`; campo `resumo`; termos esperados `codifica`, `encoding`, `acent`; termos proibidos `fora_do_dominio`, `tipo_divergente`
- **Na corrida 17:** reproduz: corpo diferente da referência em modo normal; árvore diferente da referência: 5 linha(s) a menos e 5 a mais
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:190`)

### `lex-25`, classe 1, nível 2: `codificacao_incorreta`

- **Requisição:** `GET /api/produtos`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `[{"id": 11, "nome": "PÃ£o de Alho", "resumo": "Pão de alho grelhado na brasa", "tipo": "Acompanhamentos", "preco": 16.9, "imagem": "paodealho.png", "destaque": false}, {"id": 12, "nome": "Queijo Coalho", "resumo": "Queijo coalho grelhado com mel", "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true}, {"id": 13, "nome": "HambÃºrguer Artesanal", "resumo": "Blend da casa, pão brioche", "tipo": "Acompanhamentos", "preco": 32.9, "imagem": "hamburger.png", "destaque": false}]`
- **Sintoma:** Na grade de acompanhamentos, os titulos 'PÃ£o de Alho' e 'HambÃºrguer Artesanal' aparecem com simbolos estranhos no lugar das letras acentuadas, enquanto 'Queijo Coalho' (sem acento no nome) aparece normal. A descricao de cada cartao, logo abaixo do titulo, esta com os acentos certos.
- **Gabarito:** causa `codificacao_incorreta`; campo `nome`; termos esperados `codifica`, `encoding`, `utf`, `acent`; termos proibidos `fora_do_dominio`, `tipo_divergente`
- **Na corrida 17:** reproduz: corpo diferente da referência em modo normal; árvore diferente da referência: 6 linha(s) a menos e 6 a mais
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:190`)

### `lex-26`, classe 1, nível 3: `codificacao_incorreta`

- **Requisição:** `GET /api/produtos/11`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `{"id": 11, "nome": "PÃ£o de Alho", "resumo": "Pão de alho grelhado na brasa", "tipo": "Acompanhamentos", "preco": 16.9, "imagem": "paodealho.png", "destaque": false}`
- **Sintoma:** Na mesma tela, o cartao do Pão de Alho mostra o titulo 'Pão de Alho', mas o modal aberto pelo 'Saiba Mais...' desse mesmo cartao mostra o titulo 'PÃ£o de Alho'. A grade foi carregada antes do clique e as duas respostas chegaram com status 200.
- **Observação:** A listagem GET /api/produtos, feita antes do clique, trouxe este produto (id 11) com o nome 'Pão de Alho'; so a resposta do detalhe veio com os simbolos estranhos.
- **Gabarito:** causa `codificacao_incorreta`; campo `nome`; termos esperados `codifica`, `encoding`, `utf`, `acent`; termos proibidos `desatualizad`, `juncao`
- **Na corrida 17:** reproduz: corpo diferente da referência em modo normal; árvore diferente da referência: 7 linha(s) a menos e 7 a mais
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/routers/produtos.py:66`)

### `sin-22`, classe 2, nível 1: `campo_ausente`

- **Requisição:** `GET /api/produtos`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `[{"id": 5, "resumo": "Alcatra grelhada servida na pedra quente", "tipo": "Carnes", "preco": 74.9, "imagem": "alcatra_pedra.jpg", "destaque": false}, {"id": 6, "resumo": "Corte macio grelhado na brasa", "tipo": "Carnes", "preco": 72.9, "imagem": "maminha.jpg", "destaque": false}]`
- **Sintoma:** Todos os cartoes da grade aparecem com o titulo '(sem nome)'. As fotos, as descricoes, os precos e os botoes 'Saiba Mais...' continuam normais.
- **Gabarito:** causa `campo_ausente`; campo `nome`; termos esperados `ausente`, `nome`, `falt`; termos proibidos `renomead`, `nulo`
- **Na corrida 17:** reproduz: diff do contrato: ausente; corpo diferente da referência em modo normal; árvore diferente da referência: 28 linha(s) a menos e 28 a mais
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:171`)

### `sin-23`, classe 2, nível 1: `campo_renomeado`

- **Requisição:** `GET /api/produtos/10`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `{"id": 10, "nome": "Refrigerante", "tipo": "Bebidas", "preco": 7.0, "imagem": "refrigerante.png", "destaque": false, "resumo_v2": "Lata 350ml, diversos sabores"}`
- **Sintoma:** O modal do Refrigerante abre com o titulo certo, mas o texto de descricao aparece como '(sem descrição)'.
- **Gabarito:** causa `campo_renomeado`; campo `resumo`; termos esperados `renomead`, `resumo_v2`, `resumo`; termos proibidos `nulo`, `aninhad`
- **Na corrida 17:** reproduz: diff do contrato: renomeado; corpo diferente da referência em modo normal; árvore diferente da referência: 15 linha(s) a menos e 15 a mais
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:173`)

### `sin-25`, classe 2, nível 2: `colecao_no_lugar_de_objeto`

- **Requisição:** `GET /api/produtos/4`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `[{"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]`
- **Sintoma:** Ao clicar em 'Saiba Mais...' da Costelona, o modal abre com o titulo 'Produto #4' e o texto '(sem descrição)', como se o produto nao tivesse dados.
- **Gabarito:** causa `colecao_no_lugar_de_objeto`; campo nenhum; termos esperados `colec`, `lista`, `array`; termos proibidos `campo_ausente`, `nulo`
- **Na corrida 17:** reproduz: diff do contrato: forma_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 2 linha(s) a menos e 2 a mais
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/routers/produtos.py:72`)

### `sin-26`, classe 2, nível 3: `campo_ausente`

- **Requisição:** `GET /api/produtos`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", "destaque": true}, {"id": 10, "nome": "Refrigerante", "resumo": "Lata 350ml, diversos sabores", "tipo": "Bebidas", "imagem": "refrigerante.png", "destaque": false}]`
- **Sintoma:** Na grade de bebidas, o botao de preco da Agua Mineral e o do Refrigerante mostram 'undefined', e o do Balde de Cerveja mostra 'R$ 45,00'. Ao recarregar a pagina, os produtos afetados mudam.
- **Observação:** O corpo mostra so os itens de id 8 a 10; a lista completa tem 14.
- **Gabarito:** causa `campo_ausente`; campo `preco`; termos esperados `ausente`, `preco`, `alguns`; termos proibidos `renomead`, `nulo`
- **Na corrida 17:** reproduz: diff do contrato: ausente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais; conferência 'preço do primeiro cartão' falhou
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:118`)

### `sin-27`, classe 2, nível 3: `campo_renomeado`

- **Requisição:** `GET /api/produtos`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `[{"id": 12, "nome": "Queijo Coalho", "resumo": "Queijo coalho grelhado com mel", "tipo": "Acompanhamentos", "preco": 22.9, "destaque": true, "imagem_v2": "queijo.png"}, {"id": 13, "nome": "Hambúrguer Artesanal", "resumo": "Blend da casa, pão brioche", "tipo": "Acompanhamentos", "preco": 32.9, "imagem": "hamburger.png", "destaque": false}, {"id": 14, "nome": "Abacaxi na Brasa", "resumo": "Com canela e açúcar", "tipo": "Sobremesas", "preco": 14.9, "destaque": false, "imagem_v2": "abacaxi.jpg"}]`
- **Sintoma:** Na grade, o Queijo Coalho e o Abacaxi na Brasa aparecem sem foto, enquanto o Hamburguer Artesanal mostra a foto normalmente. Nome, categoria, preco e botoes estao certos nos tres. Ao recarregar a pagina, os cartoes sem foto mudam.
- **Observação:** O corpo mostra so os itens de id 12 a 14; a lista completa tem 14.
- **Gabarito:** causa `campo_renomeado`; campo `imagem`; termos esperados `renomead`, `imagem_v2`, `alguns`; termos proibidos `nulo`, `aninhad`
- **Na corrida 17:** reproduz: diff do contrato: renomeado; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 0 a mais
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:173`)

### `semt-22`, classe 3, nível 1: `nulo_inesperado`

- **Requisição:** `GET /api/produtos`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `[{"id": 6, "nome": "Maminha", "resumo": "Corte macio grelhado na brasa", "tipo": "Carnes", "preco": null, "imagem": "maminha.jpg", "destaque": false}, {"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Carnes", "preco": null, "imagem": "cupim.jpg", "destaque": true}]`
- **Sintoma:** Todos os botoes de preco da grade mostram 'R$ 0,00'. Os nomes, as categorias e as fotos estao normais.
- **Gabarito:** causa `nulo_inesperado`; campo `preco`; termos esperados `nulo`, `null`, `preco`; termos proibidos `campo_ausente`, `escala`
- **Na corrida 17:** reproduz: diff do contrato: nulo_inesperado; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:186`)

### `semt-23`, classe 3, nível 1: `valor_fora_do_dominio`

- **Requisição:** `GET /api/produtos`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `[{"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": -80.9, "imagem": "costelona.jpg", "destaque": true}, {"id": 5, "nome": "Alcatra na Pedra", "resumo": "Alcatra grelhada servida na pedra quente", "tipo": "Carnes", "preco": -75.9, "imagem": "alcatra_pedra.jpg", "destaque": false}]`
- **Sintoma:** Os botoes de preco da grade mostram valores negativos, por exemplo 'R$ -80,90' na Costelona e 'R$ -75,90' na Alcatra na Pedra.
- **Gabarito:** causa `valor_fora_do_dominio`; campo `preco`; termos esperados `dominio`, `negativ`, `preco`; termos proibidos `escala`, `tipo_divergente`
- **Na corrida 17:** reproduz: corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais; conferência 'preço do primeiro cartão' falhou
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:133`)

### `semt-24`, classe 3, nível 2: `tipo_divergente`

- **Requisição:** `GET /api/produtos`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": "True"}, {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 84.9, "imagem": "picanha_sem.jpg", "destaque": "False"}]`
- **Sintoma:** Nos cartoes da grade, a linha de destaque mostra 'destaque: True' e 'destaque: False' (em ingles, com inicial maiuscula) em vez de 'destaque: Sim' e 'destaque: Não'.
- **Gabarito:** causa `tipo_divergente`; campo `destaque`; termos esperados `tipo`, `texto`, `bool`; termos proibidos `fora_do_dominio`, `nulo`
- **Na corrida 17:** reproduz: diff do contrato: tipo_diferente; corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:165`)

### `semt-25`, classe 3, nível 2: `formato_de_data_divergente`

- **Requisição:** `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 6, "data_pedido": "2026-12-20"})`
- **Status:** 201
- **Contrato:** `id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto`
- **Corpo:** `{"id_pedido": 11, "pessoas": 6, "data_pedido": "20/12/2026", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}`
- **Sintoma:** A reserva e criada (status 201), mas a resposta devolve a data como '20/12/2026' para uma reserva pedida com '2026-12-20'; quem le o campo como data ISO (AAAA-MM-DD) nao consegue interpretar o valor.
- **Gabarito:** causa `formato_de_data_divergente`; campo `data_pedido`; termos esperados `data`, `formato`, `iso`; termos proibidos `tipo_divergente`, `valor_fora`
- **Na corrida 17:** fora: sem tela: a rota 'POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 6, "data_pedido": "2026-12-20"})' não é consumida por página nenhuma
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:184`)

### `tra-22`, classe 4, nível 1: `escala_ou_unidade_errada`

- **Requisição:** `GET /api/produtos`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "preco": 600.0, "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 4500.0, "imagem": "balde_cerveja.png", "destaque": true}]`
- **Sintoma:** Na grade de bebidas, a Agua Mineral aparece por 'R$ 600,00' e o Balde de Cerveja por 'R$ 4500,00'; nomes, categorias e fotos estao certos.
- **Observação:** Antes da falha, a mesma grade mostrava a Agua Mineral por 'R$ 6,00' e o Balde de Cerveja por 'R$ 45,00'.
- **Gabarito:** causa `escala_ou_unidade_errada`; campo `preco`; termos esperados `escala`, `100`, `centavos`; termos proibidos `fora_do_dominio`, `nulo`
- **Na corrida 17:** reproduz: corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:181`)

### `tra-23`, classe 4, nível 1: `escala_ou_unidade_errada`

- **Requisição:** `POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 4, "data_pedido": "2026-12-19"})`
- **Status:** 201
- **Contrato:** `id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto`
- **Corpo:** `{"id_pedido": 12, "pessoas": 400, "data_pedido": "2026-12-19", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}`
- **Sintoma:** A reserva e criada (status 201), mas a resposta mostra 400 pessoas para uma reserva pedida para 4.
- **Observação:** Consultando o banco direto, tbpedido_reserva guarda a reserva 12 com 4 pessoas.
- **Gabarito:** causa `escala_ou_unidade_errada`; campo `pessoas`; termos esperados `escala`, `100`, `pessoas`; termos proibidos `fora_do_dominio`, `tipo_divergente`
- **Na corrida 17:** fora: sem tela: a rota 'POST /api/pedidos (enviado: {"id_clientes": 2, "pessoas": 4, "data_pedido": "2026-12-19"})' não é consumida por página nenhuma
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:181`)

### `tra-24`, classe 4, nível 2: `chave_de_juncao_errada`

- **Requisição:** `GET /api/produtos`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `[{"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Bebidas", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}, {"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", "destaque": true}, {"id": 10, "nome": "Refrigerante", "resumo": "Lata 350ml, diversos sabores", "tipo": "Acompanhamentos", "preco": 7.0, "imagem": "refrigerante.png", "destaque": false}]`
- **Sintoma:** Na grade, o Cupim aparece com a categoria 'Bebidas' e o Refrigerante com 'Acompanhamentos'; a Agua Mineral e o Balde de Cerveja aparecem com 'Bebidas'. Os nomes, os precos e as fotos estao certos.
- **Observação:** O corpo mostra so os itens de id 7 a 10; a lista completa tem 14.
- **Gabarito:** causa `chave_de_juncao_errada`; campo `tipo`; termos esperados `juncao`, `trocad`, `categoria`; termos proibidos `fora_do_dominio`, `tipo_divergente`
- **Na corrida 17:** reproduz: corpo diferente da referência em modo normal
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:212`)

### `tra-25`, classe 4, nível 2: `contagem_inconsistente`

- **Requisição:** `GET /api/produtos`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `[{"id": 12, "nome": "Queijo Coalho", "resumo": "Queijo coalho grelhado com mel", "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true}, {"id": 13, "nome": "Hambúrguer Artesanal", "resumo": "Blend da casa, pão brioche", "tipo": "Acompanhamentos", "preco": 32.9, "imagem": "hamburger.png", "destaque": false}]`
- **Sintoma:** A grade mostra 13 cartoes e termina no Hamburguer Artesanal; a unica sobremesa (Abacaxi na Brasa) nao aparece. A tabela tbprodutos tem 14 linhas.
- **Observação:** O corpo mostra so os dois ultimos itens da lista recebida (13 itens no total, ids de 1 a 13).
- **Gabarito:** causa `contagem_inconsistente`; campo nenhum; termos esperados `contagem`, `13`, `14`; termos proibidos `duplicad`, `truncad`
- **Na corrida 17:** reproduz: corpo diferente da referência em modo normal; árvore diferente da referência: 10 linha(s) a menos e 0 a mais; conferência 'grid com 14 cartões' falhou
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:210`)

### `tra-26`, classe 4, nível 3: `chave_de_juncao_errada`

- **Requisição:** `GET /api/produtos`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `[{"id": 4, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 5, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}, {"id": 6, "nome": "Alcatra na Pedra", "resumo": "Alcatra grelhada servida na pedra quente", "tipo": "Carnes", "preco": 74.9, "imagem": "alcatra_pedra.jpg", "destaque": false}]`
- **Sintoma:** A grade aparece normal, mas cada 'Saiba Mais...' abre o produto vizinho: o botao do cartao da Fraldinha abre o modal da Costelona, o da Costelona abre o da Alcatra na Pedra e o da Alcatra na Pedra abre o da Maminha. O clique no cartao da Fraldinha disparou GET /api/produtos/4, que respondeu 200 com os dados da Costelona.
- **Observação:** O corpo mostra so os cartoes da Fraldinha, da Costelona e da Alcatra na Pedra; a lista completa tem 14.
- **Gabarito:** causa `chave_de_juncao_errada`; campo `id`; termos esperados `juncao`, `trocad`, `vizinho`; termos proibidos `estado_da_tela`, `escala`
- **Na corrida 17:** reproduz: corpo diferente da referência em modo normal
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:212`)

### `run-22`, classe 5, nível 1: `limite_de_requisicoes`

- **Requisição:** `GET /api/produtos`
- **Status:** 429
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `{"detail": "limite de requisições excedido"}`
- **Sintoma:** A pagina Produtos (API) abre sem nenhum cartao; a linha de status acima da grade fica vermelha e mostra 'Erro ao carregar produtos da CobaiaAPI: HTTP 429'.
- **Observação:** A resposta traz o cabecalho Retry-After: 60.
- **Gabarito:** causa `limite_de_requisicoes`; campo nenhum; termos esperados `429`, `limite`, `retry-after`; termos proibidos `500`, `timeout`
- **Na corrida 17:** reproduz: status 429; diff do contrato: ausente, forma_diferente, inesperado; corpo diferente da referência em modo normal; árvore diferente da referência: 140 linha(s) a menos e 1 a mais; conferência 'grid com 14 cartões' falhou
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:233`)

### `run-23`, classe 5, nível 1: `recurso_inexistente`

- **Requisição:** `GET /api/produtos/5`
- **Status:** 404
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `{"detail": "produto não encontrado"}`
- **Sintoma:** A grade foi carregada com os 14 cartoes, entre eles o da Alcatra na Pedra; ao clicar no 'Saiba Mais...' desse cartao, o modal abre com 'Erro' no titulo e 'HTTP 404' no corpo.
- **Observação:** O id 5 aparece na listagem GET /api/produtos feita antes do clique, e GET /api/produtos/5 respondeu 200 em chamadas anteriores.
- **Gabarito:** causa `recurso_inexistente`; campo nenhum; termos esperados `404`, `inexistente`, `nao encontrado`; termos proibidos `500`, `timeout`
- **Na corrida 17:** reproduz: status 404; diff do contrato: ausente, forma_diferente, inesperado; árvore diferente da referência: 144 linha(s) a menos e 1 a mais; conferência 'grid carregado antes do detalhe' falhou
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:239`)

### `run-24`, classe 5, nível 2: `registro_duplicado`

- **Requisição:** `GET /api/produtos`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 84.9, "imagem": "picanha_sem.jpg", "destaque": false}]`
- **Sintoma:** A grade mostra o cartao da Picanha ao Alho duas vezes seguidas, identicos, e os outros produtos uma vez cada. A grade tem 15 cartoes; a tabela tbprodutos tem 14 linhas.
- **Observação:** O corpo mostra so os 3 primeiros itens da lista recebida (15 itens no total).
- **Gabarito:** causa `registro_duplicado`; campo nenhum; termos esperados `duplicad`, `repetid`, `15`; termos proibidos `contagem_inconsistente`, `truncad`
- **Na corrida 17:** reproduz: corpo diferente da referência em modo normal; árvore diferente da referência: 0 linha(s) a menos e 10 a mais; conferência 'grid com 14 cartões' falhou
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:208`)

### `run-25`, classe 5, nível 2: `tempo_de_resposta_excedido`

- **Requisição:** `GET /api/produtos/7`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `{"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Carnes", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}`
- **Sintoma:** Ao clicar em 'Saiba Mais...' do Cupim, nada acontece por cerca de 2 segundos e so entao o modal abre, com os dados certos. O roteiro espera o modal por 1 segundo e reprova por tempo.
- **Observação:** As outras requisicoes da mesma sessao responderam em menos de 100 ms.
- **Gabarito:** causa `tempo_de_resposta_excedido`; campo nenhum; termos esperados `tempo`, `latencia`, `demor`; termos proibidos `500`, `truncad`
- **Na corrida 17:** reproduz: tempo de resposta 2008 ms acima do orçamento de 1000 ms
- **Pré-análise:** nada a apontar (`CobaiaAPI/app/fault_injection.py:154`)

### `efe-22`, classe 6, nível 1: `localizador_quebrado`

- **Requisição:** `GET /api/produtos`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `[{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]`
- **Sintoma:** O passo 'abrir os detalhes da Fraldinha' do roteiro falha ao clicar em #saiba-mais-3: o Playwright espera 5 segundos e desiste sem ter encontrado nenhum elemento com esse seletor. A grade apareceu inteira, sem mensagem de erro, e GET /api/produtos respondeu 200.
- **Seletor quebrado:** `#saiba-mais-3`
- **Árvore da tela:**

```text
document "Churrascaria Fornalha - Produtos (API)"
  navigation
    link "PRODUTOS"
    link "PRODUTOS (API)"
  main
    heading "Produtos via API" level=2
    group
      heading "Fraldinha" level=3
      text "Carnes"
      button "R$ 69,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    group
      heading "Costelona" level=3
      text "Carnes"
      button "R$ 79,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="4"

```

- **Gabarito:** causa `localizador_quebrado`; campo nenhum; termos esperados `seletor`, `localizador`, `data-id`; termos proibidos `tempo_de_resposta`, `campo_ausente`
- **Na corrida 17:** fora: armada pelo harness (ficha 29): localizador_quebrado
- **Pré-análise:** nada a apontar (`CobaiaFront/produtos_api.php:82`)

### `efe-23`, classe 6, nível 1: `localizador_quebrado`

- **Requisição:** `GET /api/produtos`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `[{"id": 6, "nome": "Maminha", "resumo": "Corte macio grelhado na brasa", "tipo": "Carnes", "preco": 72.9, "imagem": "maminha.jpg", "destaque": false}, {"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Carnes", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}]`
- **Sintoma:** A verificacao 'o titulo do Cupim esta visivel' do roteiro falha: o seletor h2:has-text("Cupim") nao encontra nenhum elemento. O cartao do Cupim aparece normalmente na tela e GET /api/produtos respondeu 200.
- **Seletor quebrado:** `h2:has-text("Cupim")`
- **Árvore da tela:**

```text
document "Churrascaria Fornalha - Produtos (API)"
  navigation
    link "PRODUTOS"
    link "PRODUTOS (API)"
  main
    heading "Produtos via API" level=2
    group
      heading "Maminha" level=3
      text "Carnes"
      button "R$ 72,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="6"
    group
      heading "Cupim" level=3
      text "Carnes"
      button "R$ 76,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="7"

```

- **Gabarito:** causa `localizador_quebrado`; campo nenhum; termos esperados `seletor`, `localizador`, `h3`; termos proibidos `tempo_de_resposta`, `campo_ausente`
- **Na corrida 17:** fora: armada pelo harness (ficha 29): localizador_quebrado
- **Pré-análise:** nada a apontar (`CobaiaFront/produtos_api.php:76`)

### `efe-25`, classe 6, nível 2: `localizador_quebrado`

- **Requisição:** `GET /api/produtos/3`
- **Status:** 200
- **Contrato:** `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`
- **Corpo:** `{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}`
- **Sintoma:** Depois do clique em 'Saiba Mais...' da Fraldinha, o modal aparece na tela com o titulo 'Fraldinha', mas a verificacao do roteiro, que le o texto de '#modalDetalhe .modal-title', esgota o tempo sem encontrar o elemento. GET /api/produtos/3 respondeu 200 com os dados certos.
- **Seletor quebrado:** `#modalDetalhe .modal-title`
- **Árvore da tela:**

```text
document "Churrascaria Fornalha - Produtos (API)"
  navigation
    link "PRODUTOS"
    link "PRODUTOS (API)"
  main
    heading "Produtos via API" level=2
    group
      heading "Fraldinha" level=3
      text "Carnes"
      button "R$ 69,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    group
      heading "Costelona" level=3
      text "Carnes"
      button "R$ 79,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="4"
  dialog
    button "×" class="close"
    heading "Fraldinha" level=4 id="modalDetalheTitulo"
    text "Corte grelhado na brasa, fatiado na hora" id="modalDetalheCorpo"

```

- **Gabarito:** causa `localizador_quebrado`; campo nenhum; termos esperados `seletor`, `localizador`, `modal-title`; termos proibidos `estado_da_tela`, `tempo_de_resposta`
- **Na corrida 17:** fora: armada pelo harness (ficha 29): localizador_quebrado
- **Pré-análise:** nada a apontar (`CobaiaFront/produtos_api.php:45`)
