<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `sin-14` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3/qwen2.5_7b/sin-14@L1`. Corrida `fase3`, Ollama 0.34.0; classe 2, nível 3; texto dos casos: anterior à correção de 28/09/2026. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`entidade-produto`, `contrato-produto`, `campo_renomeado`); prompt de 1336 tokens; resposta de 67 tokens em 59,0 s |
| O que o modelo declarou | causa `campo_renomeado`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 6 de 6 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem_url": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: Todos os cartoes mostram icone de imagem quebrada; o resto do dado esta certo.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/produtos`, entidade `Produto`, status `200`, 36 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `entidade-produto` | 39,830 | 36,830 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `contrato-produto` | 32,328 | 29,328 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `campo_renomeado` | 28,761 | 25,761 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 4 | `campo_ausente` | 21,206 | 18,206 | 2,0 | 1,0 | 0,0 | descartado |
| 5 | `chave_de_juncao_errada` | 20,435 | 18,435 | 2,0 | 0,0 | 0,0 | descartado |
| 6 | `tipo_divergente` | 18,154 | 15,155 | 2,0 | 1,0 | 0,0 | descartado |

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

**`campo_renomeado`**

```text
[campo_renomeado] Campo renomeado
O valor existe sob outra chave: falta a esperada e aparece uma desconhecida com o mesmo tipo e conteúdo (preco → preco_v2, nome → descricao, status → situacao). Sinais: o resto do objeto confere; uma chave sumiu e outra sobrou; vazio ou undefined só naquele campo. Causa: O modo field_renamed troca o campo-alvo por <campo>_v2 (fault_injection.py). Fora dele: contrato mudou no servidor sem atualizar o cliente. Notas: Retificação: onde diz "Fora dele: contrato mudou no servidor sem atualizar o cliente.", leia: Corrigir a afirmação para "Contrato mudou no servidor sem atualizar o cliente e API não reflete as mudanças.".
```

### Prompt

4284 caracteres em 7 partes (hash `9d78d6a3893adfa2`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1336 tokens, saída de 67 (teto de 600); 59,0 s no total (41478 ms lendo o prompt, 15307 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: campo_renomeado
CAMPO: imagem_url
IMPACTO: O ícone de imagem quebrado indica que o campo `imagem` foi renomeado para `imagem_url` na resposta, mas a interface web ainda espera `imagem`.
FONTE: [campo_renomeado]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `campo_renomeado` | caracteres 12 a 27 da resposta |
| CAMPO | `imagem_url` | caracteres 35 a 45 da resposta |
| IMPACTO | `O ícone de imagem quebrado indica que o campo `imagem` foi renomeado para `imagem_url` na resposta, mas a interface web ainda espera `imagem`.` | caracteres 55 a 197 da resposta |
| FONTE | `[campo_renomeado]` | caracteres 205 a 222 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `campo_renomeado` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_renomeado` |
| O campo apontado aparece no caso | `imagem_url` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `contrato-produto`, `campo_renomeado` |
| Notas escritas pelo modelo nos verbetes citados | `campo_renomeado` | informativo | `campo_renomeado`: 1 nota(s) do modelo (Parcial: 1). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O ícone de imagem quebrado indica que o campo imagem foi renomeado para imagem_url na resposta, mas a interface web ainda espera imagem.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `campo_renomeado` | `campo_renomeado` | confere |
| O campo respondido é o esperado | `imagem_url` | `imagem` | confere |
| O verbete da causa esperada estava no contexto | `campo_renomeado` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `tipo_divergente` | `entidade-produto`, `contrato-produto`, `campo_renomeado` |
| L1 | `campo_renomeado` | `entidade-produto`, `contrato-produto`, `campo_renomeado` |
| L2 | `formato_de_data_divergente` | `entidade-produto`, `contrato-produto`, `campo_renomeado` |
| L3 | `tipo_divergente` | `entidade-produto`, `contrato-produto`, `campo_renomeado` |

## Rastro

Gerado dos eventos 1284 a 1305 da trilha `fase3__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `52681e1246a928ce`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
