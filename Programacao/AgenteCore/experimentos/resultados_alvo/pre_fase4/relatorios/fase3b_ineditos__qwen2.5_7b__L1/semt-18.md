<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `semt-18` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3b_ineditos/qwen2.5_7b/semt-18@L1`. Corrida `fase3b_ineditos`, Ollama 0.34.1; classe 3, nível 2; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`tipo_divergente`, `entidade-produto`, `valor_fora_do_dominio`); prompt de 1300 tokens; resposta de 57 tokens em 88,7 s |
| O que o modelo declarou | causa `tipo_divergente`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 6 de 6 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos (modo type_drift, campo destaque)

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": "True"}]

SINTOMA OBSERVADO: O rotulo do card mostra 'destaque: True' (em ingles, T maiusculo) no lugar de 'Sim' ou 'Nao'.

OBSERVAÇÃO ADICIONAL: O modo type_drift converte o valor com str() do Python, que gera 'True'/'False' com maiuscula — diferente de 'true'/'false' do JSON e de 'Sim'/'Nao' do dominio do produto.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/produtos`, entidade `Produto`, status `200`, 56 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `tipo_divergente` | 76,117 | 73,117 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `entidade-produto` | 53,449 | 50,449 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `valor_fora_do_dominio` | 48,743 | 46,743 | 2,0 | 0,0 | 0,0 | entregue ao modelo |
| 4 | `contrato-produto` | 47,635 | 44,635 | 2,0 | 1,0 | 0,0 | descartado |
| 5 | `campo_renomeado` | 23,519 | 20,519 | 2,0 | 1,0 | 0,0 | descartado |
| 6 | `colecao_no_lugar_de_objeto` | 20,941 | 17,941 | 2,0 | 1,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`tipo_divergente`**

```text
[tipo_divergente] Tipo divergente
Chave certa com o tipo JSON errado: número entre aspas ("89.90"), booleano como texto ("Sim") ou número (1), inteiro como texto ("4"). Sinais: texto numérico com ponto ainda formata; a falha aparece ao ordenar ou somar; "89,90" com vírgula não converte; destaque fora de true/false sai literal. Causa: O modo type_drift aplica str() ao campo-alvo (fault_injection.py:76). A API converte DECIMAL em número e 'Sim'/'Não' em booleano (_to_dict). Notas: Retificação: onde diz "destaque fora de true/false sai literal.", leia: Corrigir que destaque booleano saia literal, garantindo que seja convertido corretamente para True ou False.
```

**`entidade-produto`**

```text
[entidade-produto] Produto e sua categoria
Item do cardápio em tbprodutos, ligado a uma categoria de tbtipos (Carnes, Bebidas, Acompanhamentos, Sobremesas). 14 produtos; o id 1 é Picanha ao Alho, Carnes, 89,90. Sinais: título com nome de categoria: junção trocada; preço com grandeza estranha: conversão de valor_produto. Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano. Notas: Retificação: onde diz "Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano.", leia: Corrigir a conversão do preço e destaque no _to_dict de produtos.py. Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro.
```

**`valor_fora_do_dominio`**

```text
[valor_fora_do_dominio] Valor fora do domínio
Tipo certo, valor fora do conjunto permitido: status diferente de 'Em Análise'/'Cancelado', destaque diferente de true/false, pessoas menor que 1. Sinais: reserva nem ativa nem cancelada na tela: status inesperado; 0 ou negativo em pessoas: o mínimo só existe no HTML. Causa: status e destaque são ENUM no banco (schema_completo.sql:37); pessoas ≥ 1 é só min= do HTML (registrar_reserva.php:55); a API não valida o que devolve. Notas: Retificação: onde diz "Valor fora do domínio", leia: Adicionar validação no status do pedido na API para evitar valores fora do domínio.
```

### Prompt

4078 caracteres em 7 partes (hash `8fe6f8e45236ee00`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1300 tokens, saída de 57 (teto de 600); 88,7 s no total (73453 ms lendo o prompt, 13055 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: tipo_divergente
CAMPO: destaque
IMPACTO: O usuário vê 'destaque: True' em vez de 'destaque: Sim' ou 'destaque: Não'.
FONTE: [tipo_divergente]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `tipo_divergente` | caracteres 12 a 27 da resposta |
| CAMPO | `destaque` | caracteres 35 a 43 da resposta |
| IMPACTO | `O usuário vê 'destaque: True' em vez de 'destaque: Sim' ou 'destaque: Não'.` | caracteres 53 a 128 da resposta |
| FONTE | `[tipo_divergente]` | caracteres 136 a 153 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `tipo_divergente` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `tipo_divergente`, `entidade-produto`, `valor_fora_do_dominio` |
| O campo apontado aparece no caso | `destaque` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `tipo_divergente`, `entidade-produto`, `valor_fora_do_dominio` |
| Notas escritas pelo modelo nos verbetes citados | `tipo_divergente` | informativo | `tipo_divergente`: 1 nota(s) do modelo (Errada: 1). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário vê 'destaque: True' em vez de 'destaque: Sim' ou 'destaque: Não'.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `tipo_divergente` | `tipo_divergente` | confere |
| O campo respondido é o esperado | `destaque` | `destaque` | confere |
| O verbete da causa esperada estava no contexto | `tipo_divergente` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `tipo_divergente` | `tipo_divergente`, `entidade-produto`, `valor_fora_do_dominio` |
| L1 | `tipo_divergente` | `tipo_divergente`, `entidade-produto`, `valor_fora_do_dominio` |
| L3 | `tipo_divergente` | `tipo_divergente`, `entidade-produto`, `contrato-produto` |

## Rastro

Gerado dos eventos 351 a 372 da trilha `fase3b_ineditos__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `558ad9ea4e1633b9`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
