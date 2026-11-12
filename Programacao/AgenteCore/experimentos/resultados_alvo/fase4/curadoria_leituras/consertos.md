<!-- ! Alteração de IA - Revisar: lista DERIVADA dos consertos do Claude nos textos da curadoria das leituras dos verbetes, gerada por ferramentas/curadoria_leituras.py --aplicar a partir de consertos.json; não editar à mão.
     ! Motivo: o texto que o analista escreveu na curadoria trazia frases erradas sobre o projeto, formato quebrado e termos sem explicação; o Eric escolheu aplicar a curadoria com consertos, e cada troca fica aqui com o motivo, o trecho de antes e o de depois, para ele conferir. -->
# Consertos do Claude na curadoria das leituras, aplicados em 10/11/2026

77 consertos em 26 leituras. Cada conserto troca um trecho do texto que o analista escreveu e o Eric colou na página da curadoria; o resto do texto dele ficou como estava. O arquivo de cada leitura está em `Programacao/AgenteCore/biblioteca_producao_leitura/`.

## `atualizacao-da-tela` (1 conserto)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

## `campo_preco_ausente` (3 consertos)

1. Motivo: conferido em Programacao/CobaiaFront/produtos_api.php (função formatarPreco, linhas 64 a 66): sem o campo, o botão do preço mostra só "undefined", nunca "R$ undefined", e não é o botão de compra nem o de detalhes; e "frontend" estava sem o significado na primeira menção

   Antes:

   ~~~text
   A omissão da chave preco no objeto da API faz com que a renderização do botão de compra/detalhes no frontend exiba o literal undefined (ou R$ undefined), em vez do valor numérico formatado.
   ~~~

   Depois:

   ~~~text
   A omissão da chave `preco` no objeto da API faz com que o botão do preço, na página `produtos_api.php`, mostre o texto `undefined` no lugar do valor formatado.
   ~~~

2. Motivo: a linha reproduz o campo arquivos do cabeçalho, que neste verbete está vazio; o arquivo apontado pelo analista é o certo, mas não está no cabeçalho, e a busca não o lê de lá

   Antes:

   ~~~text
   - Arquivos: Programacao/CobaiaFront/produtos_api.php.
   ~~~

   Depois:

   ~~~text
   - Arquivos: nenhum declarado no cabeçalho do verbete. A página que mostra o preço é `Programacao/CobaiaFront/produtos_api.php` (apontada pelo analista na curadoria e conferida no código).
   ~~~

3. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; e "frontend" estava sem o significado

   Antes:

   ~~~text
   Verbete revisado e aprovado. A definição do sintoma foi refinada para detalhar a exibição do literal undefined no frontend e o mapeamento do arquivo produtos_api.php foi preenchido.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada. A definição do sintoma foi refinada para detalhar a exibição do texto `undefined` na página, e o arquivo `produtos_api.php` foi apontado em "Onde está no código".
   ~~~

## `campo_renomeado` (3 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas

   Antes:

   ~~~text
   ## Notas do modelo
   
   
   ## Curadoria
   ~~~

   Depois:

   ~~~text
   ## Notas do modelo
   
   O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/erros/campo_renomeado.md`.
   
   ## Curadoria
   ~~~

3. Motivo: a nota repetia entre aspas uma frase inteira do texto, e a repetição fazia a leitura reprovar no filtro de repetição; e a nota não dizia que o texto do modelo saiu só desta leitura e continua no verbete que o modelo lê

   Antes:

   ~~~text
   A redação original de "O que conferir" ("contrato mudou no servidor sem atualizar o cliente") se mantém, pois é tecnicamente mais precisa. A nota confusa gerada pelo modelo foi descartada.
   ~~~

   Depois:

   ~~~text
   A redação original de "O que conferir" se mantém, pois é tecnicamente mais precisa do que a retificação que o modelo propôs. A nota do modelo foi retirada desta leitura; continua no verbete que o modelo lê.
   ~~~

## `chave_de_juncao_errada` (3 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas

   Antes:

   ~~~text
   ## Notas do modelo
   
   ## Curadoria
   ~~~

   Depois:

   ~~~text
   ## Notas do modelo
   
   O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/erros/chave_de_juncao_errada.md`.
   
   ## Curadoria
   ~~~

3. Motivo: a nota dizia que a retirada protegia a busca ("RAG", "vetorial", "indexação semântica"), mas a camada de leitura não é buscada nem lida pelo modelo, e a busca deste projeto é por palavras; a nota retirada continua no verbete que o modelo lê

   Antes:

   ~~~text
   Nota do modelo removida para evitar poluição semântica no mecanismo de busca do RAG e manter o foco estrito na taxonomia do defeito.
   ~~~

   Depois:

   ~~~text
   A nota do modelo foi retirada desta leitura para manter o foco na descrição do defeito; continua no verbete que o modelo lê.
   ~~~

## `colecao_no_lugar_de_objeto` (3 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas

   Antes:

   ~~~text
   ## Notas do modelo
   
   
   ## Curadoria
   ~~~

   Depois:

   ~~~text
   ## Notas do modelo
   
   O verbete que o modelo lê traz 2 notas do modelo. A curadoria de 10/11/2026 as retirou desta leitura; elas continuam em `biblioteca_producao/erros/colecao_no_lugar_de_objeto.md`.
   
   ## Curadoria
   ~~~

3. Motivo: a nota dizia que a retirada protegia a busca ("RAG", "vetorial", "indexação semântica"), mas a camada de leitura não é buscada nem lida pelo modelo, e a busca deste projeto é por palavras; a nota retirada continua no verbete que o modelo lê; e a nota chamava as épocas de "treinamento"; neste projeto o modelo não é treinado: época é a rodada em que ele propôs acréscimos à biblioteca; a nota retirada continua no verbete que o modelo lê

   Antes:

   ~~~text
   As duas anotações do modelo das rodadas de treinamento (épocas 1 e 101) sobre o tratamento do array "tipo" foram apagadas para resguardar a integridade da semântica de busca do RAG e manter a finalidade de taxonomia pura.
   ~~~

   Depois:

   ~~~text
   As duas notas do modelo (épocas 1 e 101) sobre o tratamento do campo `tipo` foram retiradas desta leitura; continuam no verbete que o modelo lê.
   ~~~

## `contagem_inconsistente` (3 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas

   Antes:

   ~~~text
   ## Notas do modelo
   
   
   ## Curadoria
   ~~~

   Depois:

   ~~~text
   ## Notas do modelo
   
   O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/erros/contagem_inconsistente.md`.
   
   ## Curadoria
   ~~~

3. Motivo: a nota dizia que a retirada protegia a busca ("RAG", "vetorial", "indexação semântica"), mas a camada de leitura não é buscada nem lida pelo modelo, e a busca deste projeto é por palavras; a nota retirada continua no verbete que o modelo lê

   Antes:

   ~~~text
   A anotação do modelo (época 101) prescrevendo a reengenharia do envelope da API foi excluída para preservar o mapeamento neutro e a semântica correta do RAG
   ~~~

   Depois:

   ~~~text
   A nota do modelo (época 101), que pedia para incluir o total na resposta da API, foi retirada desta leitura; continua no verbete que o modelo lê.
   ~~~

## `contrato-pedido` (3 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas

   Antes:

   ~~~text
   ## Notas do modelo
   
   
   ## Curadoria
   ~~~

   Depois:

   ~~~text
   ## Notas do modelo
   
   O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/contratos/contrato-pedido.md`.
   
   ## Curadoria
   ~~~

3. Motivo: a nota chamava as épocas de "treinamento"; neste projeto o modelo não é treinado: época é a rodada em que ele propôs acréscimos à biblioteca; a nota retirada continua no verbete que o modelo lê

   Antes:

   ~~~text
   A nota de treinamento referente à idempotência em POST foi removida para evitar sobreposição semântica com a taxonomia registro_duplicado e manter o foco estrito nas regras da rota.
   ~~~

   Depois:

   ~~~text
   A nota do modelo sobre registros duplicados no POST foi retirada desta leitura, porque repete o que a causa `registro_duplicado` já trata; continua no verbete que o modelo lê.
   ~~~

## `contrato-produto` (3 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas

   Antes:

   ~~~text
   ## Notas do modelo
   
   
   ## Curadoria
   ~~~

   Depois:

   ~~~text
   ## Notas do modelo
   
   O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/contratos/contrato-produto.md`.
   
   ## Curadoria
   ~~~

3. Motivo: a nota não dizia que o texto do modelo saiu só desta leitura e continua no verbete que o modelo lê

   Antes:

   ~~~text
   A nota do modelo referente ao truncamento de resposta foi removida para manter o documento restrito às regras puras do contrato.
   ~~~

   Depois:

   ~~~text
   A nota do modelo sobre o truncamento de resposta foi retirada desta leitura, para ela ficar só com as regras do contrato; continua no verbete que o modelo lê.
   ~~~

## `corpo_nao_e_json` (4 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas

   Antes:

   ~~~text
   ## Notas do modelo
   
   
   ## Curadoria
   ~~~

   Depois:

   ~~~text
   ## Notas do modelo
   
   O verbete que o modelo lê traz 2 notas do modelo. A curadoria de 10/11/2026 as retirou desta leitura; elas continuam em `biblioteca_producao/erros/corpo_nao_e_json.md`.
   
   ## Curadoria
   ~~~

3. Motivo: a nota dizia que a retirada protegia a busca ("RAG", "vetorial", "indexação semântica"), mas a camada de leitura não é buscada nem lida pelo modelo, e a busca deste projeto é por palavras; a nota retirada continua no verbete que o modelo lê

   Antes:

   ~~~text
   O termo "token" foi contextualizado para adequação à métrica Q2 de termos técnicos. Ambas as anotações do modelo (referentes a exemplos em HTML e XML) foram apagadas para resguardar a pureza semântica do RAG
   ~~~

   Depois:

   ~~~text
   O termo `token` foi explicado na primeira menção, para o filtro de termos técnicos do pacote Q2. As duas notas do modelo (exemplos em HTML e XML) foram retiradas desta leitura; continuam no verbete que o modelo lê.
   ~~~

4. Motivo: o termo continuava sem o significado na primeira menção, e os filtros de texto do pacote Q2 seguiam reprovando a leitura

   Antes:

   ~~~text
   - erro no console do navegador acusando caractere inválido (ex: "Unexpected token <", referindo-se a um token ou símbolo não esperado na leitura do JSON).
   ~~~

   Depois:

   ~~~text
   - erro no console do navegador acusando caractere inválido: `Unexpected token <`, em que token é o pedaço do texto que o leitor de JSON não esperava.
   ~~~

## `corpo_vazio` (3 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas

   Antes:

   ~~~text
   ## Notas do modelo
   
   
   ## Curadoria
   ~~~

   Depois:

   ~~~text
   ## Notas do modelo
   
   O verbete que o modelo lê traz 2 notas do modelo. A curadoria de 10/11/2026 as retirou desta leitura; elas continuam em `biblioteca_producao/erros/corpo_vazio.md`.
   
   ## Curadoria
   ~~~

3. Motivo: a nota dizia que a retirada protegia a busca ("RAG", "vetorial", "indexação semântica"), mas a camada de leitura não é buscada nem lida pelo modelo, e a busca deste projeto é por palavras; a nota retirada continua no verbete que o modelo lê; e a nota chamava as épocas de "treinamento"; neste projeto o modelo não é treinado: época é a rodada em que ele propôs acréscimos à biblioteca; a nota retirada continua no verbete que o modelo lê

   Antes:

   ~~~text
   As notas metalinguísticas injetadas pelo agente em épocas de treino foram removidas para garantir aderência estrita à taxonomia e limpar a indexação semântica.
   ~~~

   Depois:

   ~~~text
   As duas notas do modelo foram retiradas desta leitura; continuam no verbete que o modelo lê.
   ~~~

## `entidade-produto` (2 consertos)

1. Motivo: a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas

   Antes:

   ~~~text
   ## Notas do modelo
   
   
   ## Curadoria
   ~~~

   Depois:

   ~~~text
   ## Notas do modelo
   
   O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/negocio/entidade-produto.md`.
   
   ## Curadoria
   ~~~

2. Motivo: o termo continuava sem o significado na primeira menção, e os filtros de texto do pacote Q2 seguiam reprovando a leitura

   Antes:

   ~~~text
   destaque_produto é um enumerador de valores fixos (ENUM('Sim','Não'))
   ~~~

   Depois:

   ~~~text
   destaque_produto é `ENUM('Sim','Não')`, uma lista fechada de valores permitidos
   ~~~

## `erro_interno_do_servidor` (3 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas

   Antes:

   ~~~text
   ## Notas do modelo
   
   
   ## Curadoria
   ~~~

   Depois:

   ~~~text
   ## Notas do modelo
   
   O verbete que o modelo lê traz 2 notas do modelo. A curadoria de 10/11/2026 as retirou desta leitura; elas continuam em `biblioteca_producao/erros/erro_interno_do_servidor.md`.
   
   ## Curadoria
   ~~~

3. Motivo: a nota chamava as épocas de "treinamento"; neste projeto o modelo não é treinado: época é a rodada em que ele propôs acréscimos à biblioteca; a nota retirada continua no verbete que o modelo lê

   Antes:

   ~~~text
   As duas notas redundantes do modelo das rodadas de treinamento (época 1) foram excluídas para manter a coesão documental.
   ~~~

   Depois:

   ~~~text
   As duas notas do modelo (época 1) foram retiradas desta leitura por repetirem o que o texto já diz; continuam no verbete que o modelo lê.
   ~~~

## `escala_ou_unidade_errada` (3 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas

   Antes:

   ~~~text
   ## Notas do modelo
   
   
   ## Curadoria
   ~~~

   Depois:

   ~~~text
   ## Notas do modelo
   
   O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/erros/escala_ou_unidade_errada.md`.
   
   ## Curadoria
   ~~~

3. Motivo: a nota não dizia que o texto do modelo saiu só desta leitura e continua no verbete que o modelo lê

   Antes:

   ~~~text
   A anotação metalinguística de retificação da época 1 foi descartada para evitar repetição de sintomas e assegurar a fidelidade da taxonomia.
   ~~~

   Depois:

   ~~~text
   A nota do modelo (uma retificação da época 1) foi retirada desta leitura para não repetir sintomas; continua no verbete que o modelo lê.
   ~~~

## `estado_da_tela_divergente` (3 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas

   Antes:

   ~~~text
   ## Notas do modelo
   
   
   ## Curadoria
   ~~~

   Depois:

   ~~~text
   ## Notas do modelo
   
   O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/erros/estado_da_tela_divergente.md`.
   
   ## Curadoria
   ~~~

3. Motivo: a nota chamava as épocas de "treinamento"; neste projeto o modelo não é treinado: época é a rodada em que ele propôs acréscimos à biblioteca; a nota retirada continua no verbete que o modelo lê

   Antes:

   ~~~text
   A nota prescritiva remanescente do ciclo de treinamento (época 101) foi removida, mantendo o escopo documental limpo.
   ~~~

   Depois:

   ~~~text
   A nota do modelo (época 101), escrita como instrução, foi retirada desta leitura; continua no verbete que o modelo lê.
   ~~~

## `estrutura_aninhada_divergente` (3 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas

   Antes:

   ~~~text
   ## Notas do modelo
   
   
   ## Curadoria
   ~~~

   Depois:

   ~~~text
   ## Notas do modelo
   
   O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/erros/estrutura_aninhada_divergente.md`.
   
   ## Curadoria
   ~~~

3. Motivo: a nota dizia que a retirada protegia a busca ("RAG", "vetorial", "indexação semântica"), mas a camada de leitura não é buscada nem lida pelo modelo, e a busca deste projeto é por palavras; a nota retirada continua no verbete que o modelo lê; e a nota chamava as épocas de "treinamento"; neste projeto o modelo não é treinado: época é a rodada em que ele propôs acréscimos à biblioteca; a nota retirada continua no verbete que o modelo lê

   Antes:

   ~~~text
   A nota redundante de treinamento foi descartada para garantir o matching preciso e limpo do RAG.
   ~~~

   Depois:

   ~~~text
   A nota do modelo foi retirada desta leitura por repetir o que o texto já diz; continua no verbete que o modelo lê.
   ~~~

## `limite_de_requisicoes` (3 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas

   Antes:

   ~~~text
   ## Notas do modelo
   
   
   ## Curadoria
   ~~~

   Depois:

   ~~~text
   ## Notas do modelo
   
   O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/erros/limite_de_requisicoes.md`.
   
   ## Curadoria
   ~~~

3. Motivo: a nota dizia que a retirada protegia a busca ("RAG", "vetorial", "indexação semântica"), mas a camada de leitura não é buscada nem lida pelo modelo, e a busca deste projeto é por palavras; a nota retirada continua no verbete que o modelo lê

   Antes:

   ~~~text
   A anotação redundante da época 101 foi descartada para resguardar a qualidade da busca vetorial no RAG.
   ~~~

   Depois:

   ~~~text
   A nota do modelo (época 101) foi retirada desta leitura; continua no verbete que o modelo lê.
   ~~~

## `limites-do-sistema` (3 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: o termo continuava sem o significado na primeira menção, e os filtros de texto do pacote Q2 seguiam reprovando a leitura

   Antes:

   ~~~text
   não aplica função de hash (transformação criptográfica unidirecional) na senha no login
   ~~~

   Depois:

   ~~~text
   não aplica hash (o resumo embaralhado da senha, que não se desfaz) na senha no login
   ~~~

3. Motivo: a nota chamava as épocas de "treinamento"; neste projeto o modelo não é treinado: época é a rodada em que ele propôs acréscimos à biblioteca; a nota retirada continua no verbete que o modelo lê

   Antes:

   ~~~text
   O termo "hash" foi contextualizado em sua primeira menção para satisfazer os critérios do filtro Q2. Documento limpo, neutro e sem resíduos de treinamento.
   ~~~

   Depois:

   ~~~text
   O termo `hash` foi explicado na primeira menção, para o filtro de termos técnicos do pacote Q2. A leitura não tinha notas do modelo.
   ~~~

## `localizador_quebrado` (3 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas

   Antes:

   ~~~text
   ## Notas do modelo
   
   
   ## Curadoria
   ~~~

   Depois:

   ~~~text
   ## Notas do modelo
   
   O verbete que o modelo lê traz 2 notas do modelo. A curadoria de 10/11/2026 as retirou desta leitura; elas continuam em `biblioteca_producao/erros/localizador_quebrado.md`.
   
   ## Curadoria
   ~~~

3. Motivo: a nota dizia que a retirada protegia a busca ("RAG", "vetorial", "indexação semântica"), mas a camada de leitura não é buscada nem lida pelo modelo, e a busca deste projeto é por palavras; a nota retirada continua no verbete que o modelo lê

   Antes:

   ~~~text
   As duas notas redundantes do modelo (épocas 1 e 101) foram excluídas para manter a integridade da semântica de busca do RAG.
   ~~~

   Depois:

   ~~~text
   As duas notas do modelo (épocas 1 e 101) foram retiradas desta leitura; continuam no verbete que o modelo lê.
   ~~~

## `mensagens-de-erro-do-codigo` (3 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: a explicação tinha sido posta dentro das aspas, e a mensagem que a API devolve de verdade é só "token inválido"; entre crases o texto literal não conta como termo sem explicação

   Antes:

   ~~~text
   "token (chave de acesso ou credencial) inválido" (403)
   ~~~

   Depois:

   ~~~text
   `"token inválido"` (403: a chave de acesso do administrador foi recusada)
   ~~~

3. Motivo: a nota falava em "poluição semântica residual", que não descreve nada desta camada, e citava o termo fora de crases, o que fazia a leitura reprovar no mesmo filtro que a nota dizia atender

   Antes:

   ~~~text
   O termo "token" foi contextualizado para satisfazer o filtro Q2 de termos técnicos. O documento funciona como um excelente dicionário de hardcoded strings, livre de notas ou poluição semântica residual.
   ~~~

   Depois:

   ~~~text
   A mensagem literal da API ficou entre crases, com o significado ao lado, para o filtro de termos técnicos do pacote Q2. O documento funciona como um dicionário das mensagens fixas do código, e a leitura não tinha notas do modelo.
   ~~~

## `modos-de-injecao` (3 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: o termo continuava sem o significado na primeira menção, e os filtros de texto do pacote Q2 seguiam reprovando a leitura

   Antes:

   ~~~text
   X-Admin-Token (chave de acesso/autorização)
   ~~~

   Depois:

   ~~~text
   o cabeçalho `X-Admin-Token` (a chave de acesso do administrador)
   ~~~

3. Motivo: a nota chamava as épocas de "treinamento"; neste projeto o modelo não é treinado: época é a rodada em que ele propôs acréscimos à biblioteca; a nota retirada continua no verbete que o modelo lê

   Antes:

   ~~~text
   O termo "token" presente na especificação do cabeçalho de administração foi contextualizado para satisfazer o filtro Q2. O arquivo não apresentou resíduos de notas de treinamento e descreve com exatidão o mecanismo do injetor de falhas.
   ~~~

   Depois:

   ~~~text
   O nome do cabeçalho de administração ficou entre crases, com o significado ao lado, para o filtro de termos técnicos do pacote Q2. A leitura não tinha notas do modelo e descreve com exatidão o mecanismo do injetor de falhas.
   ~~~

## `novo_verbete` (2 consertos)

1. Motivo: uma frase colada no fim do item dizia que o cabeçalho traz os sintomas "entidade trocada, dados relacionados nulos, cruzamento indevido"; o cabeçalho do verbete traz `tipo_divergente` e `chave_de_juncao_errada`, como diz a linha logo abaixo, que ficou, e é isso que a busca lê

   Antes:

   ~~~text
   - atributos da entidade relacionada aparecem trocados ou vazios na interface.Sintomas que a busca reconhece (campo sintomas do cabeçalho): entidade trocada, dados relacionados nulos, cruzamento indevido.
   ~~~

   Depois:

   ~~~text
   - atributos da entidade relacionada aparecem trocados ou vazios na interface.
   ~~~

2. Motivo: a nota chamava as épocas de "treinamento"; o texto veio de uma proposta do modelo aceita na biblioteca, e os nomes listados são causas da mesma taxonomia, não de outra; o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado. O texto original consistia em uma alucinação de treinamento, contendo instruções operacionais ("Corrigir a junção") e listando tags de outras taxonomias como sintomas visuais.
   ~~~

   Depois:

   ~~~text
   Leitura revisada. O texto original, escrito pelo modelo na época 101 a partir do caso `tra-3`, era uma instrução ("Corrigir a junção") e listava nomes de causas da taxonomia no lugar de sintomas da tela.
   ~~~

## `recurso_inexistente` (4 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas

   Antes:

   ~~~text
   ## Notas do modelo
   
   
   ## Curadoria
   ~~~

   Depois:

   ~~~text
   ## Notas do modelo
   
   O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/erros/recurso_inexistente.md`.
   
   ## Curadoria
   ~~~

3. Motivo: o termo continuava sem o significado na primeira menção, e os filtros de texto do pacote Q2 seguiam reprovando a leitura

   Antes:

   ~~~text
   - vizinhos: 403 no admin sem token (chave de acesso/autorização); 422 sem login.
   ~~~

   Depois:

   ~~~text
   - vizinhos: 403 no admin sem a chave de acesso (o cabeçalho `X-Admin-Token`); 422 sem login.
   ~~~

4. Motivo: a nota não dizia que o texto do modelo saiu só desta leitura e continua no verbete que o modelo lê; e a nota citava o termo fora de crases, o que fazia a leitura reprovar no mesmo filtro que ela dizia atender

   Antes:

   ~~~text
   O termo "token" foi contextualizado para adequação à métrica Q2. A nota do modelo, que sugeria uma adição já existente no corpo do texto, foi apagada para evitar redundância.
   ~~~

   Depois:

   ~~~text
   O nome do cabeçalho com a chave de acesso ficou entre crases, para o filtro de termos técnicos do pacote Q2. A nota do modelo, que sugeria uma adição já existente no texto, foi retirada desta leitura; continua no verbete que o modelo lê.
   ~~~

## `resposta_truncada` (3 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas

   Antes:

   ~~~text
   ## Notas do modelo
   
   
   ## Curadoria
   ~~~

   Depois:

   ~~~text
   ## Notas do modelo
   
   O verbete que o modelo lê traz 2 notas do modelo. A curadoria de 10/11/2026 as retirou desta leitura; elas continuam em `biblioteca_producao/erros/resposta_truncada.md`.
   
   ## Curadoria
   ~~~

3. Motivo: a nota dizia que a retirada protegia a busca ("RAG", "vetorial", "indexação semântica"), mas a camada de leitura não é buscada nem lida pelo modelo, e a busca deste projeto é por palavras; a nota retirada continua no verbete que o modelo lê

   Antes:

   ~~~text
   As duas notas redundantes do modelo da época 1 foram excluídas para manter a síntese e otimizar o ranqueamento no RAG.
   ~~~

   Depois:

   ~~~text
   As duas notas do modelo (época 1) foram retiradas desta leitura para ela ficar curta; continuam no verbete que o modelo lê.
   ~~~

## `senha-sem-hash` (3 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: o termo continuava sem o significado na primeira menção, e os filtros de texto do pacote Q2 seguiam reprovando a leitura

   Antes:

   ~~~text
   login compara sem hash (função de criptografia irreversível) (login.php:7)
   ~~~

   Depois:

   ~~~text
   login compara sem hash, o resumo embaralhado da senha, que não se desfaz (login.php:7)
   ~~~

3. Motivo: a nota chamava as épocas de "treinamento"; neste projeto o modelo não é treinado: época é a rodada em que ele propôs acréscimos à biblioteca; a nota retirada continua no verbete que o modelo lê

   Antes:

   ~~~text
   O termo "hash" foi contextualizado para satisfazer os critérios do filtro estático Q2. O documento aborda com precisão o defeito intencional de desalinhamento de senhas no sistema legado PHP. Sem notas ou ruídos de treinamento identificados.
   ~~~

   Depois:

   ~~~text
   O termo `hash` foi explicado no texto, para o filtro de termos técnicos do pacote Q2. O documento aborda com precisão o defeito intencional de desalinhamento de senhas no sistema legado PHP. A leitura não tinha notas do modelo.
   ~~~

## `tipo_divergente` (3 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas

   Antes:

   ~~~text
   ## Notas do modelo
   
   
   ## Curadoria
   ~~~

   Depois:

   ~~~text
   ## Notas do modelo
   
   O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/erros/tipo_divergente.md`.
   
   ## Curadoria
   ~~~

3. Motivo: a nota dizia que a retirada protegia a busca ("RAG", "vetorial", "indexação semântica"), mas a camada de leitura não é buscada nem lida pelo modelo, e a busca deste projeto é por palavras; a nota retirada continua no verbete que o modelo lê

   Antes:

   ~~~text
   A nota redundante da época 101 foi apagada para manter o verbete focado e otimizado para recuperação vetorial.
   ~~~

   Depois:

   ~~~text
   A nota do modelo (época 101) foi retirada desta leitura; continua no verbete que o modelo lê.
   ~~~

## `valor_fora_do_dominio` (4 consertos)

1. Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou

   Antes:

   ~~~text
   Verbete revisado e aprovado.
   ~~~

   Depois:

   ~~~text
   Leitura revisada e aprovada.
   ~~~

2. Motivo: a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas

   Antes:

   ~~~text
   ## Notas do modelo
   
   
   ## Curadoria
   ~~~

   Depois:

   ~~~text
   ## Notas do modelo
   
   O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/erros/valor_fora_do_dominio.md`.
   
   ## Curadoria
   ~~~

3. Motivo: o termo continuava sem o significado na primeira menção, e os filtros de texto do pacote Q2 seguiam reprovando a leitura

   Antes:

   ~~~text
   ENUM (tipo de dado enumerado com valores fixos permitidos) no banco
   ~~~

   Depois:

   ~~~text
   `ENUM` no banco, uma lista fechada de valores permitidos
   ~~~

4. Motivo: a nota dizia que a curadoria era dos 39 verbetes da biblioteca de produção; o que foi curado são as 39 leituras, e a biblioteca que o modelo lê não mudou; e a nota não dizia que o texto do modelo saiu só desta leitura e continua no verbete que o modelo lê

   Antes:

   ~~~text
   O termo técnico "ENUM" foi contextualizado para satisfazer o critério do filtro estático Q2. A nota prescritiva da época 1 foi expurgada por violar o caráter descritivo da base de verbetes. Com este arquivo, encerra-se com sucesso a curadoria do lote completo de 39 verbetes da biblioteca_producao.
   ~~~

   Depois:

   ~~~text
   O termo `ENUM` foi explicado na primeira menção, para o filtro de termos técnicos do pacote Q2. A nota do modelo (época 1), que pedia uma validação na API, foi retirada desta leitura por ser instrução e não descrição; continua no verbete que o modelo lê. Com este arquivo o analista encerrou a curadoria das 39 leituras.
   ~~~
