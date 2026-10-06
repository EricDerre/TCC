<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `lex-8` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3/qwen2.5_7b/lex-8@L1`. Corrida `fase3`, Ollama 0.34.0; classe 1, nível 2; texto dos casos: anterior à correção de 28/09/2026. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`codificacao_incorreta`, `contrato-produto`, `entidade-produto`); prompt de 1315 tokens; resposta de 64 tokens em 88,6 s |
| O que o modelo declarou | causa `codificacao_incorreta`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 5 de 5 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]

SINTOMA OBSERVADO: A descricao aparece com simbolos no lugar dos acentos.

OBSERVAÇÃO ADICIONAL: O cabecalho declara charset=utf-8 mas os bytes estao em latin-1.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/produtos`, entidade `Produto`, status `200`, 43 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `codificacao_incorreta` | 28,445 | 28,445 | 0,0 | 0,0 | 0,0 | entregue ao modelo |
| 2 | `contrato-produto` | 25,986 | 22,986 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `entidade-produto` | 24,335 | 21,335 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 4 | `estado_da_tela_divergente` | 22,901 | 22,901 | 0,0 | 0,0 | 0,0 | descartado |
| 5 | `tipo_divergente` | 21,293 | 18,293 | 2,0 | 1,0 | 0,0 | descartado |
| 6 | `campo_renomeado` | 18,617 | 15,617 | 2,0 | 1,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`codificacao_incorreta`**

```text
[codificacao_incorreta] Codificação de caracteres incorreta
JSON válido e estrutura certa, mas textos com acento corrompidos: bytes latin-1 declarados utf-8, ou utf-8 convertido duas vezes ("Pão" vira "PÃ£o"). Sinais: só campos de texto livre afetados; números e chaves intactos; parte dos registros certa e parte errada: conversão dupla parcial. Causa: Banco e conexões em utf8 (connect.php:7, config.py); se corrompe, o dado foi gravado errado ou um intermediário reconverteu.
```

**`contrato-produto`**

```text
[contrato-produto] Contrato de /api/produtos
GET /api/produtos devolve lista; GET /api/produtos/{id} devolve objeto (404 "produto não encontrado"). Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano. Sinais: chave a mais ou a menos: campo ausente ou renomeado; lista onde se espera objeto, ou o inverso. Causa: Origem tbprodutos + rótulo de tbtipos (produtos.py _to_dict). preco sai 89.9 (número), embora o schema declare Decimal. Notas: Notar que o contrato especifica a estrutura do JSON esperado, mas não aborda o truncamento de resposta. Retificação: onde diz "Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano.", leia: Corrigir "preco número" para "preco Decimal" para refletir o tipo correto em valor_produto. Retificação: onde diz "Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano.", leia: Adicionar observação sobre possíveis nomes diferentes para o campo tipo no verbete.
```

**`entidade-produto`**

```text
[entidade-produto] Produto e sua categoria
Item do cardápio em tbprodutos, ligado a uma categoria de tbtipos (Carnes, Bebidas, Acompanhamentos, Sobremesas). 14 produtos; o id 1 é Picanha ao Alho, Carnes, 89,90. Sinais: título com nome de categoria: junção trocada; preço com grandeza estranha: conversão de valor_produto. Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano. Notas: Retificação: onde diz "Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano.", leia: Corrigir a conversão do preço e destaque no _to_dict de produtos.py. Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro.
```

### Prompt

4175 caracteres em 7 partes (hash `fbc0dec5aadd8a47`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1315 tokens, saída de 64 (teto de 600); 88,6 s no total (71285 ms lendo o prompt, 15197 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: codificacao_incorreta
CAMPO: nenhum
IMPACTO: A descrição da resposta aparece com símbolos no lugar dos acentos, devido à codificação incorreta dos caracteres.
FONTE: [codificacao_incorreta]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `codificacao_incorreta` | caracteres 12 a 33 da resposta |
| CAMPO | `nenhum` | caracteres 41 a 47 da resposta |
| IMPACTO | `A descrição da resposta aparece com símbolos no lugar dos acentos, devido à codificação incorreta dos caracteres.` | caracteres 57 a 170 da resposta |
| FONTE | `[codificacao_incorreta]` | caracteres 178 a 201 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `codificacao_incorreta` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `codificacao_incorreta` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `codificacao_incorreta` | confere | contexto: `codificacao_incorreta`, `contrato-produto`, `entidade-produto` |
| O campo apontado aparece no caso | `nenhum` | não se aplica | o modelo não apontou campo |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | confere | verbetes: `codificacao_incorreta` |
| Notas escritas pelo modelo nos verbetes citados | `codificacao_incorreta` | informativo | `codificacao_incorreta`: sem notas do modelo. A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `A descrição da resposta aparece com símbolos no lugar dos acentos, devido à codificação incorreta dos caracteres.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `codificacao_incorreta` | `codificacao_incorreta` | confere |
| O campo respondido é o esperado | `nenhum` | `resumo` | **não confere** |
| O verbete da causa esperada estava no contexto | `codificacao_incorreta` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `codificacao_incorreta` | `codificacao_incorreta`, `contrato-produto`, `entidade-produto` |
| L1 | `codificacao_incorreta` | `codificacao_incorreta`, `contrato-produto`, `entidade-produto` |
| L2 | `codificacao_incorreta` | `codificacao_incorreta`, `contrato-produto`, `entidade-produto` |
| L3 | `codificacao_incorreta` | `codificacao_incorreta`, `contrato-produto`, `entidade-produto` |

## Rastro

Gerado dos eventos 914 a 936 da trilha `fase3__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `f7aec03d56e8a9dd`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
