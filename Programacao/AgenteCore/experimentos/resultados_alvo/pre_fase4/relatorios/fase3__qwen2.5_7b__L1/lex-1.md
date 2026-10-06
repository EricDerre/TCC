<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `lex-1` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3/qwen2.5_7b/lex-1@L1`. Corrida `fase3`, Ollama 0.34.0; classe 1, nível 1; texto dos casos: anterior à correção de 28/09/2026. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`entidade-produto`, `contrato-produto`, `resposta_truncada`); prompt de 1317 tokens; resposta de 70 tokens em 92,2 s |
| O que o modelo declarou | causa `resposta_truncada`; 2 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 8 de 8 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "tipo": "Carnes", "preco": 89.9

SINTOMA OBSERVADO: A listagem fica vazia e o console acusa erro ao interpretar a resposta.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/produtos`, entidade `Produto`, status `200`, 28 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `entidade-produto` | 28,372 | 25,372 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `contrato-produto` | 21,984 | 18,984 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `resposta_truncada` | 19,607 | 19,607 | 0,0 | 0,0 | 0,0 | entregue ao modelo |
| 4 | `pagina-produtos-api` | 15,302 | 13,302 | 2,0 | 0,0 | 0,0 | descartado |
| 5 | `corpo_nao_e_json` | 14,364 | 13,364 | 0,0 | 0,0 | 1,0 | descartado |
| 6 | `mensagens-de-erro-do-codigo` | 13,268 | 13,268 | 0,0 | 0,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`entidade-produto`**

```text
[entidade-produto] Produto e sua categoria
Item do cardápio em tbprodutos, ligado a uma categoria de tbtipos (Carnes, Bebidas, Acompanhamentos, Sobremesas). 14 produtos; o id 1 é Picanha ao Alho, Carnes, 89,90. Sinais: título com nome de categoria: junção trocada; preço com grandeza estranha: conversão de valor_produto. Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano. Notas: Retificação: onde diz "Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano.", leia: Corrigir a conversão do preço e destaque no _to_dict de produtos.py. Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro.
```

**`contrato-produto`**

```text
[contrato-produto] Contrato de /api/produtos
GET /api/produtos devolve lista; GET /api/produtos/{id} devolve objeto (404 "produto não encontrado"). Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano. Sinais: chave a mais ou a menos: campo ausente ou renomeado; lista onde se espera objeto, ou o inverso. Causa: Origem tbprodutos + rótulo de tbtipos (produtos.py _to_dict). preco sai 89.9 (número), embora o schema declare Decimal. Notas: Notar que o contrato especifica a estrutura do JSON esperado, mas não aborda o truncamento de resposta. Retificação: onde diz "Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano.", leia: Corrigir "preco número" para "preco Decimal" para refletir o tipo correto em valor_produto. Retificação: onde diz "Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano.", leia: Adicionar observação sobre possíveis nomes diferentes para o campo tipo no verbete.
```

**`resposta_truncada`**

```text
[resposta_truncada] Resposta truncada
O corpo começa como JSON válido e termina no meio de um valor ou chave — faltam bytes; o parse falha com "Unexpected end of JSON input". Sinais: primeiros itens íntegros, o último cortado ou sem o colchete final; Content-Length menor que o esperado. Causa: O modo malformed_json devolve corpo cortado de propósito (produtos.py:19). Fora dele: limite num proxy, conexão encerrada durante o envio. Notas: Retificação: onde diz "Fora dele: limite num proxy, conexão encerrada durante o envio.", leia: Corrigir a descrição para incluir que o truncamento pode ser causado por limites de proxy ou interrupção de conexão. Adicione um exemplo de como verificar o Content-Length na documentação para evitar esse problema.
```

### Prompt

4286 caracteres em 7 partes (hash `0d7ab2a28fcd6c1d`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1317 tokens, saída de 70 (teto de 600); 92,2 s no total (73965 ms lendo o prompt, 16046 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: resposta_truncada
CAMPO: preco
IMPACTO: O usuário vê uma listagem vazia de produtos devido ao preço inacabado na resposta, levando ao erro de interpretação do JSON.
FONTE: [resposta_truncada] [contrato-produto]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `resposta_truncada` | caracteres 12 a 29 da resposta |
| CAMPO | `preco` | caracteres 37 a 42 da resposta |
| IMPACTO | `O usuário vê uma listagem vazia de produtos devido ao preço inacabado na resposta, levando ao erro de interpretação do JSON.` | caracteres 52 a 176 da resposta |
| FONTE | `[resposta_truncada] [contrato-produto]` | caracteres 184 a 222 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `resposta_truncada` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `resposta_truncada` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `resposta_truncada` | confere | contexto: `entidade-produto`, `contrato-produto`, `resposta_truncada` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `resposta_truncada` |
| O campo apontado aparece no caso | `preco` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | confere | verbetes: `resposta_truncada` |
| Notas escritas pelo modelo nos verbetes citados | `resposta_truncada`, `contrato-produto` | informativo | `resposta_truncada`: 2 nota(s) do modelo (Correta: 1, Parcial: 1); `contrato-produto`: 3 nota(s) do modelo (Errada: 2, Parcial: 1). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário vê uma listagem vazia de produtos devido ao preço inacabado na resposta, levando ao erro de interpretação do JSON.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `resposta_truncada` | `resposta_truncada` | confere |
| O campo respondido é o esperado | `preco` |  | **não confere** |
| O verbete da causa esperada estava no contexto | `resposta_truncada` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `resposta_truncada` | `entidade-produto`, `resposta_truncada`, `contrato-produto` |
| L1 | `resposta_truncada` | `entidade-produto`, `contrato-produto`, `resposta_truncada` |
| L2 | `resposta_truncada` | `entidade-produto`, `contrato-produto`, `resposta_truncada` |
| L3 | `resposta_truncada` | `entidade-produto`, `contrato-produto`, `resposta_truncada` |

## Rastro

Gerado dos eventos 3 a 33 da trilha `fase3__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `490aa4df56912f46`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
