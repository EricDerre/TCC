<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `tra-20` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3b_ineditos/qwen2.5_7b/tra-20@L1`. Corrida `fase3b_ineditos`, Ollama 0.34.1; classe 4, nível 3; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`entidade-produto`, `chave_de_juncao_errada`, `contrato-produto`); prompt de 1623 tokens; resposta de 69 tokens em 96,4 s |
| O que o modelo declarou | causa `chave_de_juncao_errada`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 6 de 6 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Sobremesas", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Sobremesas", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]

SINTOMA OBSERVADO: Fraldinha e Costelona (os dois cortes de carne) aparecem na categoria Sobremesas; os demais produtos de carne da listagem continuam certos em Carnes.

OBSERVAÇÃO ADICIONAL: tbprodutos.id_tipo_produto de id 3 e id 4 aponta pra 1 (Carnes) no banco; so esses dois produtos vem errados na resposta, o que sugere troca pontual de id_tipo_produto pra 4 (Sobremesas) nesses dois registros, nao um bug geral de juncao.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/produtos`, entidade `Produto`, status `200`, 91 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `entidade-produto` | 62,632 | 59,632 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `chave_de_juncao_errada` | 47,385 | 45,385 | 2,0 | 0,0 | 0,0 | entregue ao modelo |
| 3 | `contrato-produto` | 46,779 | 43,779 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 4 | `tipo_divergente` | 36,269 | 33,269 | 2,0 | 1,0 | 0,0 | descartado |
| 5 | `valor_fora_do_dominio` | 26,481 | 24,481 | 2,0 | 0,0 | 0,0 | descartado |
| 6 | `nulo_inesperado` | 26,467 | 24,467 | 2,0 | 0,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`entidade-produto`**

```text
[entidade-produto] Produto e sua categoria
Item do cardápio em tbprodutos, ligado a uma categoria de tbtipos (Carnes, Bebidas, Acompanhamentos, Sobremesas). 14 produtos; o id 1 é Picanha ao Alho, Carnes, 89,90. Sinais: título com nome de categoria: junção trocada; preço com grandeza estranha: conversão de valor_produto. Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano. Notas: Retificação: onde diz "Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano.", leia: Corrigir a conversão do preço e destaque no _to_dict de produtos.py. Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro.
```

**`chave_de_juncao_errada`**

```text
[chave_de_juncao_errada] Chave de junção errada
Tipo e formato certos, mas o valor é de OUTRO registro: categoria ou imagem alheia no produto, nome ou cpf de outro usuário na reserva. Sinais: afeta campo derivado de junção (tipo, nome, cpf, imagem), não os próprios; o dado existe no banco, ligado ao registro errado. Causa: Junções: id_tipo_produto e id_clientes (models.py). No site, cliente/index.php:4 usa LIKE '%login%' — CPF substring de outro casa mais de um cliente. Notas: Retificação: onde diz "Tipo e formato certos, mas o valor é de OUTRO registro: categoria ou imagem alheia no produto, nome ou cpf de outro usuário na reserva. Sinais: afeta campo derivado de junção (tipo, nome, cpf, imagem), não os próprios; o dado existe no banco, ligado ao registro errado. Causa: Junções: id_tipo_produto e id_clientes (models.py). No site, cliente/index.php:4 usa LIKE '%login%' — CPF substring de outro casa mais de um cliente.", leia: Corrigir a junção entre tbprodutos e tbtipos, garantindo que id_tipo_produto esteja corretamente ligado a tbtipos.id_tipo.
```

**`contrato-produto`**

```text
[contrato-produto] Contrato de /api/produtos
GET /api/produtos devolve lista; GET /api/produtos/{id} devolve objeto (404 "produto não encontrado"). Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano. Sinais: chave a mais ou a menos: campo ausente ou renomeado; lista onde se espera objeto, ou o inverso. Causa: Origem tbprodutos + rótulo de tbtipos (produtos.py _to_dict). preco sai 89.9 (número), embora o schema declare Decimal. Notas: Notar que o contrato especifica a estrutura do JSON esperado, mas não aborda o truncamento de resposta. Retificação: onde diz "Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano.", leia: Corrigir "preco número" para "preco Decimal" para refletir o tipo correto em valor_produto. Retificação: onde diz "Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano.", leia: Adicionar observação sobre possíveis nomes diferentes para o campo tipo no verbete.
```

### Prompt

5200 caracteres em 7 partes (hash `178e5cf382de5b9d`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1623 tokens, saída de 69 (teto de 600); 96,4 s no total (78128 ms lendo o prompt, 16112 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: chave_de_juncao_errada
CAMPO: tipo
IMPACTO: Os produtos Fraldinha e Costelona, que são cortes de carne, aparecem incorretamente na categoria Sobremesas na interface web.
FONTE: [chave_de_juncao_errada]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `chave_de_juncao_errada` | caracteres 12 a 34 da resposta |
| CAMPO | `tipo` | caracteres 42 a 46 da resposta |
| IMPACTO | `Os produtos Fraldinha e Costelona, que são cortes de carne, aparecem incorretamente na categoria Sobremesas na interface web.` | caracteres 56 a 181 da resposta |
| FONTE | `[chave_de_juncao_errada]` | caracteres 189 a 213 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `chave_de_juncao_errada` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `chave_de_juncao_errada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `chave_de_juncao_errada` | confere | contexto: `entidade-produto`, `chave_de_juncao_errada`, `contrato-produto` |
| O campo apontado aparece no caso | `tipo` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `chave_de_juncao_errada` | confere | verbetes: `entidade-produto`, `chave_de_juncao_errada` |
| Notas escritas pelo modelo nos verbetes citados | `chave_de_juncao_errada` | informativo | `chave_de_juncao_errada`: 1 nota(s) do modelo (Correta: 1). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `Os produtos Fraldinha e Costelona, que são cortes de carne, aparecem incorretamente na categoria Sobremesas na interface web.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `chave_de_juncao_errada` | `chave_de_juncao_errada` | confere |
| O campo respondido é o esperado | `tipo` | `tipo` | confere |
| O verbete da causa esperada estava no contexto | `chave_de_juncao_errada` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `chave_de_juncao_errada` | `entidade-produto`, `contrato-produto`, `chave_de_juncao_errada` |
| L1 | `chave_de_juncao_errada` | `entidade-produto`, `chave_de_juncao_errada`, `contrato-produto` |
| L3 | `chave_de_juncao_errada` | `entidade-produto`, `chave_de_juncao_errada`, `contrato-produto` |

## Rastro

Gerado dos eventos 551 a 572 da trilha `fase3b_ineditos__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `c47154b6d0637706`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
