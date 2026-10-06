<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `tra-8` pelo `qwen2.5-coder:3b` com a biblioteca L1

Trilha `fase3b_cruzada_qwen/qwen2.5-coder_3b/tra-8@L1`. Corrida `fase3b_cruzada_qwen`, Ollama 0.34.4; classe 4, nível 1; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`contagem_inconsistente`, `entidade-produto`, `estrutura_aninhada_divergente`); prompt de 1315 tokens; resposta de 51 tokens em 17,6 s |
| O que o modelo declarou | causa `contagem_inconsistente`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 6 de 6 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos?pagina=1

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano | envelope: {total: inteiro, itens: lista}

CORPO DA RESPOSTA:
{"total": 0, "itens": [{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]}

SINTOMA OBSERVADO: A tela informa 'Nenhum produto encontrado' mas exibe cartoes.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/produtos`, entidade `Produto`, status `200`, 38 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `contagem_inconsistente` | 44,524 | 41,524 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `entidade-produto` | 39,926 | 36,926 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `estrutura_aninhada_divergente` | 34,350 | 31,350 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 4 | `contrato-produto` | 30,160 | 27,160 | 2,0 | 1,0 | 0,0 | descartado |
| 5 | `tipo_divergente` | 19,098 | 16,098 | 2,0 | 1,0 | 0,0 | descartado |
| 6 | `valor_fora_do_dominio` | 18,741 | 16,741 | 2,0 | 0,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`contagem_inconsistente`**

```text
[contagem_inconsistente] Contagem inconsistente
Dois números que deveriam bater não batem: total 14 e lista com 1; total 0 com itens; página 2 vazia com total 14; contador de destaques diferente dos cartões. Sinais: total e lista vêm de consultas diferentes; rótulo numérico que não corresponde ao renderizado. Causa: GET /api/produtos devolve a lista crua, sem total nem paginação (produtos.py:34-43); o seed tem 14 produtos, 5 em destaque. Envelope com total indica outra versão.
```

**`entidade-produto`**

```text
[entidade-produto] Produto e sua categoria
Item do cardápio em tbprodutos, ligado a uma categoria de tbtipos (Carnes, Bebidas, Acompanhamentos, Sobremesas). 14 produtos; o id 1 é Picanha ao Alho, Carnes, 89,90. Sinais: título com nome de categoria: junção trocada; preço com grandeza estranha: conversão de valor_produto. Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano. Notas: Retificação: onde diz "Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano.", leia: Corrigir a conversão do preço e destaque no _to_dict de produtos.py. Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro.
```

**`estrutura_aninhada_divergente`**

```text
[estrutura_aninhada_divergente] Estrutura aninhada divergente
Chaves existem, mas noutro nível: lista num envelope ({"data": {"itens": [...]}}) ou campo simples como objeto ({"id": 1, "nome": "Carnes"}). Sinais: envelope na raiz: Array.isArray falha, "Nenhum produto retornado"; campo como objeto: cartão imprime [object Object]. Causa: Contrato real: lista crua na raiz e tipo como texto (produtos.py _to_dict); envelope ou aninhamento veio de outra versão ou intermediário. Notas: Retificação: onde diz "Chaves existem, mas noutro nível: lista num envelope ({'data': {'itens': [...]}}) ou campo simples como objeto ({'id': 1, 'nome': 'Carnes'}).", leia: Adicionar exemplo de estrutura aninhada divergente no verbete. Retificação: onde diz "Chaves existem, mas noutro nível: lista num envelope ({'data': {'itens': [...]}}) ou campo simples como objeto ({'id': 1, 'nome': 'Carnes'}).", leia: Corrigir a estrutura da resposta da API para ser consistente, evitando envelopes ou campos simples aninhados, para padronizar o desenpacotamento dos dados.
```

### Prompt

4137 caracteres em 7 partes (hash `5c5c39c3ae8b1fe4`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1315 tokens, saída de 51 (teto de 600); 17,6 s no total (9840 ms lendo o prompt, 5574 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: contagem_inconsistente
CAMPO: total
IMPACTO: A tela exibe cartões, mas informa 'Nenhum produto encontrado'.
FONTE: [contagem_inconsistente]
```

## O que o modelo declarou

O `qwen2.5-coder:3b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `contagem_inconsistente` | caracteres 12 a 34 da resposta |
| CAMPO | `total` | caracteres 42 a 47 da resposta |
| IMPACTO | `A tela exibe cartões, mas informa 'Nenhum produto encontrado'.` | caracteres 57 a 119 da resposta |
| FONTE | `[contagem_inconsistente]` | caracteres 127 a 151 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `contagem_inconsistente` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `contagem_inconsistente`, `entidade-produto`, `estrutura_aninhada_divergente` |
| O campo apontado aparece no caso | `total` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | confere | verbetes: `contagem_inconsistente`, `estrutura_aninhada_divergente` |
| Notas escritas pelo modelo nos verbetes citados | `contagem_inconsistente` | informativo | `contagem_inconsistente`: sem notas do modelo. A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `A tela exibe cartões, mas informa 'Nenhum produto encontrado'.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `contagem_inconsistente` | `contagem_inconsistente` | confere |
| O campo respondido é o esperado | `total` |  | **não confere** |
| O verbete da causa esperada estava no contexto | `contagem_inconsistente` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L1 | `contagem_inconsistente` | `contagem_inconsistente`, `entidade-produto`, `estrutura_aninhada_divergente` |
| L3 | `contagem_inconsistente` | `contagem_inconsistente`, `entidade-produto`, `estrutura_aninhada_divergente` |

## Rastro

Gerado dos eventos 660 a 681 da trilha `fase3b_cruzada_qwen__qwen2.5-coder_3b__L1.jsonl`; hash dos eventos deste caso: `7de3138d06329731`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
