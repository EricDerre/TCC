<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `run-9` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3/qwen2.5_7b/run-9@L1`. Corrida `fase3`, Ollama 0.34.0; classe 5, nível 2; texto dos casos: anterior à correção de 28/09/2026. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`entidade-produto`, `contrato-produto`, `tipo_divergente`); prompt de 1381 tokens; resposta de 78 tokens em 45,3 s |
| O que o modelo declarou | causa `tempo_de_resposta_excedido`; 2 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 6 de 7 conferências conferem; o que não confere: nenhum verbete do contexto trata da causa respondida (`tempo_de_resposta_excedido`) |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}] (recebido apos 9,4 s)

SINTOMA OBSERVADO: A listagem carrega, mas demora quase 10 segundos.

OBSERVAÇÃO ADICIONAL: O mesmo endpoint respondia em 120 ms na semana anterior.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/produtos`, entidade `Produto`, status `200`, 46 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `entidade-produto` | 43,011 | 40,011 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `contrato-produto` | 28,960 | 25,960 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `tipo_divergente` | 20,581 | 17,581 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 4 | `resposta_truncada` | 19,607 | 19,607 | 0,0 | 0,0 | 0,0 | descartado |
| 5 | `tempo_de_resposta_excedido` | 17,305 | 14,305 | 2,0 | 0,0 | 1,0 | descartado |
| 6 | `chave_de_juncao_errada` | 16,617 | 14,617 | 2,0 | 0,0 | 0,0 | descartado |

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

**`tipo_divergente`**

```text
[tipo_divergente] Tipo divergente
Chave certa com o tipo JSON errado: número entre aspas ("89.90"), booleano como texto ("Sim") ou número (1), inteiro como texto ("4"). Sinais: texto numérico com ponto ainda formata; a falha aparece ao ordenar ou somar; "89,90" com vírgula não converte; destaque fora de true/false sai literal. Causa: O modo type_drift aplica str() ao campo-alvo (fault_injection.py:76). A API converte DECIMAL em número e 'Sim'/'Não' em booleano (_to_dict). Notas: Retificação: onde diz "destaque fora de true/false sai literal.", leia: Corrigir que destaque booleano saia literal, garantindo que seja convertido corretamente para True ou False.
```

### Prompt

4360 caracteres em 7 partes (hash `fbea6e2379ea7d9a`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1381 tokens, saída de 78 (teto de 600); 45,3 s no total (25179 ms lendo o prompt, 17846 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: tempo_de_resposta_excedido
CAMPO: nenhum
IMPACTO: O usuário percebeu uma demora significativa na resposta, aproximadamente 9,4 segundos, o que é considerado muito alto e pode afetar a experiência do usuário.
FONTE: [contrato-produto] [entidade-produto]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `tempo_de_resposta_excedido` | caracteres 12 a 38 da resposta |
| CAMPO | `nenhum` | caracteres 46 a 52 da resposta |
| IMPACTO | `O usuário percebeu uma demora significativa na resposta, aproximadamente 9,4 segundos, o que é considerado muito alto e pode afetar a experiência do usuário.` | caracteres 62 a 219 da resposta |
| FONTE | `[contrato-produto] [entidade-produto]` | caracteres 227 a 264 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `tempo_de_resposta_excedido` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| O campo apontado aparece no caso | `nenhum` | não se aplica | o modelo não apontou campo |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | **não confere** | nenhum verbete do contexto trata dessa causa |
| Notas escritas pelo modelo nos verbetes citados | `contrato-produto`, `entidade-produto` | informativo | `contrato-produto`: 3 nota(s) do modelo (Errada: 2, Parcial: 1); `entidade-produto`: 2 nota(s) do modelo (Errada: 1, Parcial: 1). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário percebeu uma demora significativa na resposta, aproximadamente 9,4 segundos, o que é considerado muito alto e pode afetar a experiência do usuário.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | confere |
| O campo respondido é o esperado | `nenhum` |  | confere |
| O verbete da causa esperada estava no contexto | `tempo_de_resposta_excedido` |  | **não confere** |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `tempo_de_resposta_excedido` | `entidade-produto`, `contrato-produto`, `resposta_truncada` |
| L1 | `tempo_de_resposta_excedido` | `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| L2 | `tempo_de_resposta_excedido` | `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| L3 | `tempo_de_resposta_excedido` | `entidade-produto`, `contrato-produto`, `tipo_divergente` |

## Rastro

Gerado dos eventos 2010 a 2034 da trilha `fase3__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `65574ab2d7fe39f9`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
