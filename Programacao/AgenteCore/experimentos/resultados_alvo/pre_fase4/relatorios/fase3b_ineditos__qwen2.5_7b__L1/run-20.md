<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `run-20` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3b_ineditos/qwen2.5_7b/run-20@L1`. Corrida `fase3b_ineditos`, Ollama 0.34.1; classe 5, nível 3; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`dado_desatualizado`, `entidade-produto`, `contrato-produto`); prompt de 1515 tokens; resposta de 63 tokens em 104,4 s |
| O que o modelo declarou | causa `dado_desatualizado`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 6 de 6 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: admin atualiza preco da Fraldinha para R$ 74,90 -> GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
GET devolveu {"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false} — o preco antigo, mesmo apos a atualizacao confirmada no painel.

SINTOMA OBSERVADO: Depois de o administrador mudar o preco da Fraldinha pra R$ 74,90 no painel, GET /api/produtos continua devolvendo 69.9 por varios minutos.

OBSERVAÇÃO ADICIONAL: tbprodutos e a mesma tabela do painel PHP e da CobaiaAPI; listar_produtos le do banco a cada chamada, sem cache proprio — a defasagem apontaria pra um cache fora da CobaiaAPI.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/produtos`, entidade `Produto`, status `200`, 75 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `dado_desatualizado` | 55,899 | 52,899 | 2,0 | 0,0 | 1,0 | entregue ao modelo |
| 2 | `entidade-produto` | 40,116 | 37,116 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `contrato-produto` | 38,669 | 35,669 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 4 | `nulo_inesperado` | 28,800 | 26,800 | 2,0 | 0,0 | 0,0 | descartado |
| 5 | `campo_renomeado` | 24,733 | 21,733 | 2,0 | 1,0 | 0,0 | descartado |
| 6 | `pagina-produtos-api` | 24,553 | 22,553 | 2,0 | 0,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`dado_desatualizado`**

```text
[dado_desatualizado] Dado desatualizado (cache)
Uma escrita confirmada (201/200) não aparece na leitura seguinte e surge minutos depois sem nova ação — a leitura veio de uma cópia antiga. Sinais: cabeçalhos Age ou Cache-Control: max-age no GET; o painel PHP (lê o banco direto) já mostra o dado; só a API atrasa. Causa: A CobaiaAPI consulta o banco a cada requisição (database.py) e não envia cache; leitura defasada indica proxy ou cache do navegador entre a página e a API. Notas: Retificação: onde diz "Sinais: cabeçalhos Age ou Cache-Control: max-age no GET; o painel PHP (lê o banco direto) já mostra o dado; só a API atrasa.", leia: Adicionar "A leitura defasada indica que a API está lendo dados antigos do banco, enquanto o painel PHP atualiza em tempo real.".
```

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

### Prompt

4794 caracteres em 7 partes (hash `9a5ca4bad1e7926a`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1515 tokens, saída de 63 (teto de 600); 104,4 s no total (86783 ms lendo o prompt, 15458 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: dado_desatualizado
CAMPO: preco
IMPACTO: O usuário vê o preço antigo da Fraldinha, R$ 69.9, mesmo após a atualização no painel.
FONTE: [dado_desatualizado]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `dado_desatualizado` | caracteres 12 a 30 da resposta |
| CAMPO | `preco` | caracteres 38 a 43 da resposta |
| IMPACTO | `O usuário vê o preço antigo da Fraldinha, R$ 69.9, mesmo após a atualização no painel.` | caracteres 53 a 139 da resposta |
| FONTE | `[dado_desatualizado]` | caracteres 147 a 167 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `dado_desatualizado` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `dado_desatualizado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `dado_desatualizado` | confere | contexto: `dado_desatualizado`, `entidade-produto`, `contrato-produto` |
| O campo apontado aparece no caso | `preco` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `dado_desatualizado` | confere | verbetes: `dado_desatualizado` |
| Notas escritas pelo modelo nos verbetes citados | `dado_desatualizado` | informativo | `dado_desatualizado`: 1 nota(s) do modelo (Errada: 1). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário vê o preço antigo da Fraldinha, R$ 69.9, mesmo após a atualização no painel.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `dado_desatualizado` | `dado_desatualizado` | confere |
| O campo respondido é o esperado | `preco` | `preco` | confere |
| O verbete da causa esperada estava no contexto | `dado_desatualizado` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `dado_desatualizado` | `dado_desatualizado`, `entidade-produto`, `contrato-produto` |
| L1 | `dado_desatualizado` | `dado_desatualizado`, `entidade-produto`, `contrato-produto` |
| L3 | `dado_desatualizado` | `dado_desatualizado`, `entidade-produto`, `contrato-produto` |

## Rastro

Gerado dos eventos 695 a 717 da trilha `fase3b_ineditos__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `517f6155d245692c`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
