<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `efe-21` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3b_ineditos/qwen2.5_7b/efe-21@L1`. Corrida `fase3b_ineditos`, Ollama 0.34.1; classe 6, nível 3; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`nulo_inesperado`, `colecao_no_lugar_de_objeto`, `pagina-produtos-api`); prompt de 1181 tokens; resposta de 67 tokens em 67,0 s |
| O que o modelo declarou | causa `nulo_inesperado`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 5 de 5 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano (lista)

CORPO DA RESPOSTA:
null

SINTOMA OBSERVADO: A pagina mostra 'Nenhum produto retornado pela API.', dando a entender que o cadastro esta vazio; na verdade a API devolveu null, nao uma lista vazia — sao situacoes diferentes que a tela nao diferencia.

OBSERVAÇÃO ADICIONAL: produtos_api.php trata qualquer valor que nao seja array (incluindo null) do mesmo jeito que uma lista vazia.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/produtos`, entidade `Produto`, status `200`, 42 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `nulo_inesperado` | 32,005 | 30,005 | 2,0 | 0,0 | 0,0 | entregue ao modelo |
| 2 | `colecao_no_lugar_de_objeto` | 24,476 | 21,476 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `pagina-produtos-api` | 23,640 | 21,640 | 2,0 | 0,0 | 0,0 | entregue ao modelo |
| 4 | `corpo_vazio` | 23,519 | 23,519 | 0,0 | 0,0 | 0,0 | descartado |
| 5 | `mensagens-de-erro-do-codigo` | 21,511 | 21,511 | 0,0 | 0,0 | 0,0 | descartado |
| 6 | `contagem_inconsistente` | 20,301 | 17,301 | 2,0 | 1,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`nulo_inesperado`**

```text
[nulo_inesperado] Nulo inesperado
A chave existe e vem null onde o contrato promete valor. Diferente de campo_ausente: a chave está lá. Sinais: nome nulo: "Olá, !" na área do cliente; preco nulo: cartão sem valor; tipo nulo: produto some de filtros por categoria. Causa: Origens legítimas: resumo, valor_produto e imagem_produto são nullable (models.py:33-35) e vw_tbpedidos faz LEFT JOIN. tipo nulo não sai de produtos.py (p.tipo.rotulo_tipo).
```

**`colecao_no_lugar_de_objeto`**

```text
[colecao_no_lugar_de_objeto] Coleção no lugar de objeto (ou o inverso)
Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (["Carnes"]). Sinais: modal "Produto #1"/"(sem descrição)": p é lista; categoria com colchetes: campo veio como lista. Causa: GET /api/produtos devolve lista, GET /api/produtos/{id} objeto (produtos.py); a página não confere a forma antes de ler os campos. Notas: Retificação: onde diz "Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (['Carnes']).", leia: Corrigir que GET /api/produtos/{id} deve devolver um objeto, não uma lista. Retificação: onde diz "Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (['Carnes']).", leia: Corrigir que o campo "tipo" deve ser tratado como uma string, não uma lista.
```

**`pagina-produtos-api`**

```text
[pagina-produtos-api] Aba "Produtos (API)", a fronteira JSON
produtos_api.php monta os cartões com fetch() em localhost:8000/api/produtos — a única fronteira JSON do cobaia; detalhe via GET /api/produtos/{id}. Sinais: "Carregando..." parado: o fetch nunca resolveu; "Nenhum produto retornado pela API.": não é lista, ou vazia. Causa: formatarPreco() usa Number(): preço não numérico sai cru; tipo objeto sai via JSON.stringify; botão button.saiba-mais[data-id].
```

### Prompt

3802 caracteres em 7 partes (hash `c981a841ae820fab`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1181 tokens, saída de 67 (teto de 600); 67,0 s no total (49583 ms lendo o prompt, 15232 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: nulo_inesperado
CAMPO: nenhum
IMPACTO: A página exibe "Nenhum produto retornado pela API.", sugerindo que a lista de produtos está vazia, quando na verdade a API retornou null.
FONTE: [nulo_inesperado]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `nulo_inesperado` | caracteres 12 a 27 da resposta |
| CAMPO | `nenhum` | caracteres 35 a 41 da resposta |
| IMPACTO | `A página exibe "Nenhum produto retornado pela API.", sugerindo que a lista de produtos está vazia, quando na verdade a API retornou null.` | caracteres 51 a 188 da resposta |
| FONTE | `[nulo_inesperado]` | caracteres 196 a 213 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `nulo_inesperado` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `nulo_inesperado`, `colecao_no_lugar_de_objeto`, `pagina-produtos-api` |
| O campo apontado aparece no caso | `nenhum` | não se aplica | o modelo não apontou campo |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `nulo_inesperado` |
| Notas escritas pelo modelo nos verbetes citados | `nulo_inesperado` | informativo | `nulo_inesperado`: sem notas do modelo. A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `A página exibe "Nenhum produto retornado pela API.", sugerindo que a lista de produtos está vazia, quando na verdade a API retornou null.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `nulo_inesperado` | `estado_da_tela_divergente` | **não confere** |
| O campo respondido é o esperado | `nenhum` |  | confere |
| O verbete da causa esperada estava no contexto | `estado_da_tela_divergente` |  | **não confere** |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `nulo_inesperado` | `nulo_inesperado`, `colecao_no_lugar_de_objeto`, `corpo_vazio` |
| L1 | `nulo_inesperado` | `nulo_inesperado`, `colecao_no_lugar_de_objeto`, `pagina-produtos-api` |
| L3 | `nulo_inesperado` | `nulo_inesperado`, `colecao_no_lugar_de_objeto`, `pagina-produtos-api` |

## Rastro

Gerado dos eventos 862 a 883 da trilha `fase3b_ineditos__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `6e215c928fa11924`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
