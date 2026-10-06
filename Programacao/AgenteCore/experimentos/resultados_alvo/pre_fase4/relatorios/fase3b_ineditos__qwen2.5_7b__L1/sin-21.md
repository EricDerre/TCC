<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `sin-21` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3b_ineditos/qwen2.5_7b/sin-21@L1`. Corrida `fase3b_ineditos`, Ollama 0.34.1; classe 2, nível 3; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`estrutura_aninhada_divergente`, `entidade-produto`, `pagina-produtos-api`); prompt de 1400 tokens; resposta de 72 tokens em 96,6 s |
| O que o modelo declarou | causa `estrutura_aninhada_divergente`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 6 de 6 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "{'id': 1, 'nome': 'Carnes'}", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: A categoria do produto aparece como o texto literal {'id': 1, 'nome': 'Carnes'} no card (aspas simples, no estilo de repr do Python), em vez de 'Carnes' — diferente de um objeto de verdade, que apareceria como [object Object].

OBSERVAÇÃO ADICIONAL: tipo e uma STRING cujo conteudo por acaso parece um dicionario serializado errado (aspas simples); nao e um objeto JSON aninhado de verdade, por isso o card nao mostra [object Object].
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/produtos`, entidade `Produto`, status `200`, 76 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `estrutura_aninhada_divergente` | 70,580 | 67,580 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `entidade-produto` | 61,587 | 58,587 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `pagina-produtos-api` | 50,663 | 48,663 | 2,0 | 0,0 | 0,0 | entregue ao modelo |
| 4 | `tipo_divergente` | 50,578 | 47,578 | 2,0 | 1,0 | 0,0 | descartado |
| 5 | `contrato-produto` | 49,070 | 46,070 | 2,0 | 1,0 | 0,0 | descartado |
| 6 | `colecao_no_lugar_de_objeto` | 41,277 | 38,277 | 2,0 | 1,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`estrutura_aninhada_divergente`**

```text
[estrutura_aninhada_divergente] Estrutura aninhada divergente
Chaves existem, mas noutro nível: lista num envelope ({"data": {"itens": [...]}}) ou campo simples como objeto ({"id": 1, "nome": "Carnes"}). Sinais: envelope na raiz: Array.isArray falha, "Nenhum produto retornado"; campo como objeto: cartão imprime [object Object]. Causa: Contrato real: lista crua na raiz e tipo como texto (produtos.py _to_dict); envelope ou aninhamento veio de outra versão ou intermediário. Notas: Retificação: onde diz "Chaves existem, mas noutro nível: lista num envelope ({'data': {'itens': [...]}}) ou campo simples como objeto ({'id': 1, 'nome': 'Carnes'}).", leia: Adicionar exemplo de estrutura aninhada divergente no verbete. Retificação: onde diz "Chaves existem, mas noutro nível: lista num envelope ({'data': {'itens': [...]}}) ou campo simples como objeto ({'id': 1, 'nome': 'Carnes'}).", leia: Corrigir a estrutura da resposta da API para ser consistente, evitando envelopes ou campos simples aninhados, para padronizar o desenpacotamento dos dados.
```

**`entidade-produto`**

```text
[entidade-produto] Produto e sua categoria
Item do cardápio em tbprodutos, ligado a uma categoria de tbtipos (Carnes, Bebidas, Acompanhamentos, Sobremesas). 14 produtos; o id 1 é Picanha ao Alho, Carnes, 89,90. Sinais: título com nome de categoria: junção trocada; preço com grandeza estranha: conversão de valor_produto. Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano. Notas: Retificação: onde diz "Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano.", leia: Corrigir a conversão do preço e destaque no _to_dict de produtos.py. Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro.
```

**`pagina-produtos-api`**

```text
[pagina-produtos-api] Aba "Produtos (API)", a fronteira JSON
produtos_api.php monta os cartões com fetch() em localhost:8000/api/produtos — a única fronteira JSON do cobaia; detalhe via GET /api/produtos/{id}. Sinais: "Carregando..." parado: o fetch nunca resolveu; "Nenhum produto retornado pela API.": não é lista, ou vazia. Causa: formatarPreco() usa Number(): preço não numérico sai cru; tipo objeto sai via JSON.stringify; botão button.saiba-mais[data-id].
```

### Prompt

4436 caracteres em 7 partes (hash `469c734aa8c87e04`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1400 tokens, saída de 72 (teto de 600); 96,6 s no total (77874 ms lendo o prompt, 16623 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: estrutura_aninhada_divergente
CAMPO: tipo
IMPACTO: O usuário vê a categoria do produto como o texto literal {'id': 1, 'nome': 'Carnes'} em vez de 'Carnes'.
FONTE: [estrutura_aninhada_divergente]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `estrutura_aninhada_divergente` | caracteres 12 a 41 da resposta |
| CAMPO | `tipo` | caracteres 49 a 53 da resposta |
| IMPACTO | `O usuário vê a categoria do produto como o texto literal {'id': 1, 'nome': 'Carnes'} em vez de 'Carnes'.` | caracteres 63 a 167 da resposta |
| FONTE | `[estrutura_aninhada_divergente]` | caracteres 175 a 206 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `estrutura_aninhada_divergente` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `estrutura_aninhada_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `estrutura_aninhada_divergente` | confere | contexto: `estrutura_aninhada_divergente`, `entidade-produto`, `pagina-produtos-api` |
| O campo apontado aparece no caso | `tipo` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `estrutura_aninhada_divergente` | confere | verbetes: `estrutura_aninhada_divergente` |
| Notas escritas pelo modelo nos verbetes citados | `estrutura_aninhada_divergente` | informativo | `estrutura_aninhada_divergente`: 2 nota(s) do modelo (Errada: 1, Parcial: 1). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário vê a categoria do produto como o texto literal {'id': 1, 'nome': 'Carnes'} em vez de 'Carnes'.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | confere |
| O campo respondido é o esperado | `tipo` | `tipo` | confere |
| O verbete da causa esperada estava no contexto | `estrutura_aninhada_divergente` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente`, `entidade-produto`, `pagina-produtos-api` |
| L1 | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente`, `entidade-produto`, `pagina-produtos-api` |
| L3 | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente`, `entidade-produto`, `pagina-produtos-api` |

## Rastro

Gerado dos eventos 279 a 301 da trilha `fase3b_ineditos__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `1e16b672442dfb0d`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
