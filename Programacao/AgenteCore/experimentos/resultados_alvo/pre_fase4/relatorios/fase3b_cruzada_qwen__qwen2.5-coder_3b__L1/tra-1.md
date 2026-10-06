<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `tra-1` pelo `qwen2.5-coder:3b` com a biblioteca L1

Trilha `fase3b_cruzada_qwen/qwen2.5-coder_3b/tra-1@L1`. Corrida `fase3b_cruzada_qwen`, Ollama 0.34.4; classe 4, nível 2; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`entidade-produto`, `escala_ou_unidade_errada`, `contrato-produto`); prompt de 1562 tokens; resposta de 62 tokens em 48,1 s |
| O que o modelo declarou | causa `escala_ou_unidade_errada`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 6 de 6 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 8990, "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: Os precos aparecem cem vezes maiores: 'R$ 8.990,00' para a picanha.

OBSERVAÇÃO ADICIONAL: No banco, tbprodutos.valor_produto do id 1 vale 89.90.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/produtos`, entidade `Produto`, status `200`, 42 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `entidade-produto` | 40,341 | 37,341 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `escala_ou_unidade_errada` | 25,369 | 22,369 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `contrato-produto` | 24,822 | 21,822 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 4 | `estado_da_tela_divergente` | 21,007 | 21,007 | 0,0 | 0,0 | 0,0 | descartado |
| 5 | `tipo_divergente` | 20,630 | 17,630 | 2,0 | 1,0 | 0,0 | descartado |
| 6 | `nulo_inesperado` | 18,812 | 16,812 | 2,0 | 0,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`entidade-produto`**

```text
[entidade-produto] Produto e sua categoria
Item do cardápio em tbprodutos, ligado a uma categoria de tbtipos (Carnes, Bebidas, Acompanhamentos, Sobremesas). 14 produtos; o id 1 é Picanha ao Alho, Carnes, 89,90. Sinais: título com nome de categoria: junção trocada; preço com grandeza estranha: conversão de valor_produto. Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano. Notas: Retificação: onde diz "Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano.", leia: Corrigir a conversão do preço e destaque no _to_dict de produtos.py. Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro.
```

**`escala_ou_unidade_errada`**

```text
[escala_ou_unidade_errada] Escala ou unidade errada
Tipo e formato certos, mas o número está noutra escala ou unidade: centavos por reais (8990), fração (0.899), arredondado (90), data deslocada um dia, quantidade dobrada. Sinais: todos os valores errados pelo mesmo fator: conversão de unidade; só o arredondamento errado. Causa: A API não aplica fator nenhum: float(valor_produto) direto do DECIMAL (produtos.py:28), DATE em isoformat sem fuso (pedidos.py:23); o fator veio de fora dela. Notas: Retificação: onde diz "A API não aplica fator nenhum: float(valor_produto) direto do DECIMAL (produtos.py:28), DATE em isoformat sem fuso (pedidos.py:23); o fator veio de fora dela.", leia: Corrigir a conversão do valor_produto para float, aplicando o fator correto. Retificação: onde diz "Sinais: todos os valores errados pelo mesmo fator: conversão de unidade; só o arredondamento errado. Causa: A API não aplica fator nenhum: float(valor_produto) direto do DECIMAL (produtos.py:28), DATE em isoformat sem fuso (pedidos.py:23); o fator veio de fora dela.", leia: Adicionar exemplo de conversão incorreta de valor_produto DECIMAL(9,2) para float, causando arredondamento.
```

**`contrato-produto`**

```text
[contrato-produto] Contrato de /api/produtos
GET /api/produtos devolve lista; GET /api/produtos/{id} devolve objeto (404 "produto não encontrado"). Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano. Sinais: chave a mais ou a menos: campo ausente ou renomeado; lista onde se espera objeto, ou o inverso. Causa: Origem tbprodutos + rótulo de tbtipos (produtos.py _to_dict). preco sai 89.9 (número), embora o schema declare Decimal. Notas: Notar que o contrato especifica a estrutura do JSON esperado, mas não aborda o truncamento de resposta. Retificação: onde diz "Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano.", leia: Corrigir "preco número" para "preco Decimal" para refletir o tipo correto em valor_produto. Retificação: onde diz "Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano.", leia: Adicionar observação sobre possíveis nomes diferentes para o campo tipo no verbete.
```

### Prompt

4859 caracteres em 7 partes (hash `ea8cacfe81a76f70`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1562 tokens, saída de 62 (teto de 600); 48,1 s no total (39063 ms lendo o prompt, 6934 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: escala_ou_unidade_errada
CAMPO: preco
IMPACTO: Os preços exibidos na interface estão incorretamente formatados, mostrando centavos como reais.
FONTE: [escala_ou_unidade_errada]
```

## O que o modelo declarou

O `qwen2.5-coder:3b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `escala_ou_unidade_errada` | caracteres 12 a 36 da resposta |
| CAMPO | `preco` | caracteres 44 a 49 da resposta |
| IMPACTO | `Os preços exibidos na interface estão incorretamente formatados, mostrando centavos como reais.` | caracteres 59 a 154 da resposta |
| FONTE | `[escala_ou_unidade_errada]` | caracteres 162 a 188 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `escala_ou_unidade_errada` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `escala_ou_unidade_errada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `escala_ou_unidade_errada` | confere | contexto: `entidade-produto`, `escala_ou_unidade_errada`, `contrato-produto` |
| O campo apontado aparece no caso | `preco` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `escala_ou_unidade_errada` | confere | verbetes: `entidade-produto`, `escala_ou_unidade_errada` |
| Notas escritas pelo modelo nos verbetes citados | `escala_ou_unidade_errada` | informativo | `escala_ou_unidade_errada`: 2 nota(s) do modelo (Correta: 1, Errada: 1). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `Os preços exibidos na interface estão incorretamente formatados, mostrando centavos como reais.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | confere |
| O campo respondido é o esperado | `preco` | `preco` | confere |
| O verbete da causa esperada estava no contexto | `escala_ou_unidade_errada` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L1 | `escala_ou_unidade_errada` | `entidade-produto`, `escala_ou_unidade_errada`, `contrato-produto` |
| L3 | `escala_ou_unidade_errada` | `entidade-produto`, `escala_ou_unidade_errada`, `contrato-produto` |

## Rastro

Gerado dos eventos 180 a 202 da trilha `fase3b_cruzada_qwen__qwen2.5-coder_3b__L1.jsonl`; hash dos eventos deste caso: `1a3c0be224af1b21`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
