<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `semt-8` pelo `qwen2.5-coder:3b` com a biblioteca L1

Trilha `fase3b_cruzada_qwen/qwen2.5-coder_3b/semt-8@L1`. Corrida `fase3b_cruzada_qwen`, Ollama 0.34.4; classe 3, nível 1; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`entidade-produto`, `nulo_inesperado`, `contrato-produto`); prompt de 1289 tokens; resposta de 63 tokens em 33,8 s |
| O que o modelo declarou | causa `corpo_nao_e_json`; 0 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 3 de 4 conferências conferem; o que não confere: nenhum verbete do contexto trata da causa respondida (`corpo_nao_e_json`) |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": null, "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: O cartao exibe 'R$ 0,00' para um produto que custa 89,90.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/produtos`, entidade `Produto`, status `200`, 32 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `entidade-produto` | 49,756 | 46,756 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `nulo_inesperado` | 42,696 | 40,696 | 2,0 | 0,0 | 0,0 | entregue ao modelo |
| 3 | `contrato-produto` | 29,965 | 26,965 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 4 | `tipo_divergente` | 19,951 | 16,951 | 2,0 | 1,0 | 0,0 | descartado |
| 5 | `pagina-produtos-api` | 17,159 | 15,159 | 2,0 | 0,0 | 0,0 | descartado |
| 6 | `campo_ausente` | 16,222 | 13,222 | 2,0 | 1,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`entidade-produto`**

```text
[entidade-produto] Produto e sua categoria
Item do cardápio em tbprodutos, ligado a uma categoria de tbtipos (Carnes, Bebidas, Acompanhamentos, Sobremesas). 14 produtos; o id 1 é Picanha ao Alho, Carnes, 89,90. Sinais: título com nome de categoria: junção trocada; preço com grandeza estranha: conversão de valor_produto. Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano. Notas: Retificação: onde diz "Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano.", leia: Corrigir a conversão do preço e destaque no _to_dict de produtos.py. Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro.
```

**`nulo_inesperado`**

```text
[nulo_inesperado] Nulo inesperado
A chave existe e vem null onde o contrato promete valor. Diferente de campo_ausente: a chave está lá. Sinais: nome nulo: "Olá, !" na área do cliente; preco nulo: cartão sem valor; tipo nulo: produto some de filtros por categoria. Causa: Origens legítimas: resumo, valor_produto e imagem_produto são nullable (models.py:33-35) e vw_tbpedidos faz LEFT JOIN. tipo nulo não sai de produtos.py (p.tipo.rotulo_tipo).
```

**`contrato-produto`**

```text
[contrato-produto] Contrato de /api/produtos
GET /api/produtos devolve lista; GET /api/produtos/{id} devolve objeto (404 "produto não encontrado"). Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano. Sinais: chave a mais ou a menos: campo ausente ou renomeado; lista onde se espera objeto, ou o inverso. Causa: Origem tbprodutos + rótulo de tbtipos (produtos.py _to_dict). preco sai 89.9 (número), embora o schema declare Decimal. Notas: Notar que o contrato especifica a estrutura do JSON esperado, mas não aborda o truncamento de resposta. Retificação: onde diz "Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano.", leia: Corrigir "preco número" para "preco Decimal" para refletir o tipo correto em valor_produto. Retificação: onde diz "Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano.", leia: Adicionar observação sobre possíveis nomes diferentes para o campo tipo no verbete.
```

### Prompt

4046 caracteres em 7 partes (hash `24bb839644804fcf`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1289 tokens, saída de 63 (teto de 600); 33,8 s no total (24807 ms lendo o prompt, 6889 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: corpo_nao_e_json
CAMPO: preco
IMPACTO: O usuário vê 'R$ 0,00' para um produto que custa 89,90.
FONTE: [contrato-produto, corpo_nao_e_json]
```

## O que o modelo declarou

O `qwen2.5-coder:3b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `corpo_nao_e_json` | caracteres 12 a 28 da resposta |
| CAMPO | `preco` | caracteres 36 a 41 da resposta |
| IMPACTO | `O usuário vê 'R$ 0,00' para um produto que custa 89,90.` | caracteres 51 a 106 da resposta |
| FONTE | `[contrato-produto, corpo_nao_e_json]` | caracteres 114 a 150 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `corpo_nao_e_json` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca |  | não se aplica | nenhum verbete citado na linha FONTE |
| O verbete citado estava no contexto entregue ao modelo |  | não se aplica | nenhum verbete citado na linha FONTE |
| O campo apontado aparece no caso | `preco` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `corpo_nao_e_json` | **não confere** | nenhum verbete do contexto trata dessa causa |
| Notas escritas pelo modelo nos verbetes citados |  | não se aplica | A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário vê 'R$ 0,00' para um produto que custa 89,90.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `corpo_nao_e_json` | `nulo_inesperado` | **não confere** |
| O campo respondido é o esperado | `preco` | `preco` | confere |
| O verbete da causa esperada estava no contexto | `nulo_inesperado` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L1 | `corpo_nao_e_json` | `entidade-produto`, `nulo_inesperado`, `contrato-produto` |
| L3 | `corpo_nao_e_json` | `entidade-produto`, `nulo_inesperado`, `contrato-produto` |

## Rastro

Gerado dos eventos 592 a 612 da trilha `fase3b_cruzada_qwen__qwen2.5-coder_3b__L1.jsonl`; hash dos eventos deste caso: `ead2ccfa407afdf7`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
