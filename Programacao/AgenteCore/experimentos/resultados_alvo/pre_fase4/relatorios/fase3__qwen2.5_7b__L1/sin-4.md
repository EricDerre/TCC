<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `sin-4` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3/qwen2.5_7b/sin-4@L1`. Corrida `fase3`, Ollama 0.34.0; classe 2, nível 1; texto dos casos: anterior à correção de 28/09/2026. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`entidade-produto`, `colecao_no_lugar_de_objeto`, `contrato-produto`); prompt de 1463 tokens; resposta de 72 tokens em 86,2 s |
| O que o modelo declarou | causa `colecao_no_lugar_de_objeto`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 6 de 6 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/1

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano (recurso unico, nao lista)

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: A tela de detalhe do produto nao preenche nenhum campo.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/produtos/{id}`, entidade `Produto`, status `200`, 40 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `entidade-produto` | 40,244 | 37,244 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `colecao_no_lugar_de_objeto` | 38,305 | 35,305 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `contrato-produto` | 32,917 | 29,917 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 4 | `estado_da_tela_divergente` | 28,280 | 28,280 | 0,0 | 0,0 | 0,0 | descartado |
| 5 | `estrutura_aninhada_divergente` | 23,659 | 22,659 | 0,0 | 1,0 | 0,0 | descartado |
| 6 | `pagina-produtos-api` | 23,048 | 21,048 | 2,0 | 0,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`entidade-produto`**

```text
[entidade-produto] Produto e sua categoria
Item do cardápio em tbprodutos, ligado a uma categoria de tbtipos (Carnes, Bebidas, Acompanhamentos, Sobremesas). 14 produtos; o id 1 é Picanha ao Alho, Carnes, 89,90. Sinais: título com nome de categoria: junção trocada; preço com grandeza estranha: conversão de valor_produto. Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano. Notas: Retificação: onde diz "Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano.", leia: Corrigir a conversão do preço e destaque no _to_dict de produtos.py. Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro.
```

**`colecao_no_lugar_de_objeto`**

```text
[colecao_no_lugar_de_objeto] Coleção no lugar de objeto (ou o inverso)
Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (["Carnes"]). Sinais: modal "Produto #1"/"(sem descrição)": p é lista; categoria com colchetes: campo veio como lista. Causa: GET /api/produtos devolve lista, GET /api/produtos/{id} objeto (produtos.py); a página não confere a forma antes de ler os campos. Notas: Retificação: onde diz "Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (['Carnes']).", leia: Corrigir que GET /api/produtos/{id} deve devolver um objeto, não uma lista. Retificação: onde diz "Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (['Carnes']).", leia: Corrigir que o campo "tipo" deve ser tratado como uma string, não uma lista.
```

**`contrato-produto`**

```text
[contrato-produto] Contrato de /api/produtos
GET /api/produtos devolve lista; GET /api/produtos/{id} devolve objeto (404 "produto não encontrado"). Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano. Sinais: chave a mais ou a menos: campo ausente ou renomeado; lista onde se espera objeto, ou o inverso. Causa: Origem tbprodutos + rótulo de tbtipos (produtos.py _to_dict). preco sai 89.9 (número), embora o schema declare Decimal. Notas: Notar que o contrato especifica a estrutura do JSON esperado, mas não aborda o truncamento de resposta. Retificação: onde diz "Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano.", leia: Corrigir "preco número" para "preco Decimal" para refletir o tipo correto em valor_produto. Retificação: onde diz "Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano.", leia: Adicionar observação sobre possíveis nomes diferentes para o campo tipo no verbete.
```

### Prompt

4653 caracteres em 7 partes (hash `072507a6710c71f1`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

| Prova | Resultado |
|---|---|
| O snapshot da biblioteca lido agora é o da corrida | sim |
| Os verbetes entregues, o tamanho e o hash da documentação batem com o registro | sim |
| O prompt de proposta gravado começa por este prompt e por esta resposta | não há proposta gravada para este caso |
| O hash do prompt enviado ao Ollama é o deste prompt | a corrida não guardou esse hash |

<details><summary>Instrução dada ao modelo (228 caracteres)</summary>

```text
=====

Você analisa falhas de integração entre uma interface web e sua API.

Leia os dados abaixo, consulte a documentação acima quando ajudar, explique em no máximo 3 frases o que deu errado, e então responda no formato pedido.
```

</details>

<details><summary>Formato pedido para a resposta (920 caracteres)</summary>

```text
Depois do raciocínio, termine com estas quatro linhas, exatamente neste formato:
CAUSA_RAIZ: <um valor da lista abaixo, escrito igual>
CAMPO: <nome do campo afetado, ou "nenhum">
IMPACTO: <uma frase sobre o que o usuário vê>
FONTE: <identificadores da documentação que usou, entre colchetes, ou "nenhum">

Valores permitidos para CAUSA_RAIZ:
  - corpo_nao_e_json
  - corpo_vazio
  - resposta_truncada
  - codificacao_incorreta
  - campo_ausente
  - campo_renomeado
  - estrutura_aninhada_divergente
  - colecao_no_lugar_de_objeto
  - tipo_divergente
  - valor_fora_do_dominio
  - formato_de_data_divergente
  - nulo_inesperado
  - escala_ou_unidade_errada
  - chave_de_juncao_errada
  - contagem_inconsistente
  - tempo_de_resposta_excedido
  - limite_de_requisicoes
  - dado_desatualizado
  - registro_duplicado
  - erro_interno_do_servidor
  - recurso_inexistente
  - localizador_quebrado
  - estado_da_tela_divergente
```

</details>

### Inferência

Entrada de 1463 tokens, saída de 72 (teto de 600); 86,2 s no total (67509 ms lendo o prompt, 16446 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: colecao_no_lugar_de_objeto
CAMPO: id
IMPACTO: O usuário vê uma tela de detalhe do produto sem nenhum campo preenchido, pois a resposta da API é uma lista em vez de um objeto único.
FONTE: [colecao_no_lugar_de_objeto]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `colecao_no_lugar_de_objeto` | caracteres 12 a 38 da resposta |
| CAMPO | `id` | caracteres 46 a 48 da resposta |
| IMPACTO | `O usuário vê uma tela de detalhe do produto sem nenhum campo preenchido, pois a resposta da API é uma lista em vez de um objeto único.` | caracteres 58 a 192 da resposta |
| FONTE | `[colecao_no_lugar_de_objeto]` | caracteres 200 a 228 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `colecao_no_lugar_de_objeto` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `colecao_no_lugar_de_objeto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `colecao_no_lugar_de_objeto` | confere | contexto: `entidade-produto`, `colecao_no_lugar_de_objeto`, `contrato-produto` |
| O campo apontado aparece no caso | `id` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `colecao_no_lugar_de_objeto`, `contrato-produto` |
| Notas escritas pelo modelo nos verbetes citados | `colecao_no_lugar_de_objeto` | informativo | `colecao_no_lugar_de_objeto`: 2 nota(s) do modelo (Correta: 1, Errada: 1). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário vê uma tela de detalhe do produto sem nenhum campo preenchido, pois a resposta da API é uma lista em vez de um objeto único.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | confere |
| O campo respondido é o esperado | `id` |  | **não confere** |
| O verbete da causa esperada estava no contexto | `colecao_no_lugar_de_objeto` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `colecao_no_lugar_de_objeto` | `entidade-produto`, `colecao_no_lugar_de_objeto`, `contrato-produto` |
| L1 | `colecao_no_lugar_de_objeto` | `entidade-produto`, `colecao_no_lugar_de_objeto`, `contrato-produto` |
| L2 | `colecao_no_lugar_de_objeto` | `entidade-produto`, `colecao_no_lugar_de_objeto`, `contrato-produto` |
| L3 | `colecao_no_lugar_de_objeto` | `entidade-produto`, `colecao_no_lugar_de_objeto`, `contrato-produto` |

## Rastro

Gerado dos eventos 265 a 287 da trilha `fase3__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `1aa6b6ac442327b0`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
