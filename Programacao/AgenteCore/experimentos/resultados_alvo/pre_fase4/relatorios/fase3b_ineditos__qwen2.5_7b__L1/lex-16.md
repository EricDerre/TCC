<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `lex-16` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3b_ineditos/qwen2.5_7b/lex-16@L1`. Corrida `fase3b_ineditos`, Ollama 0.34.1; classe 1, nível 1; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`resposta_truncada`, `entidade-produto`, `corpo_nao_e_json`); prompt de 1226 tokens; resposta de 57 tokens em 83,5 s |
| O que o modelo declarou | causa `resposta_truncada`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 5 de 5 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/1 (modo malformed_json ligado)

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "resposta truncada de propos

SINTOMA OBSERVADO: Ao clicar em 'Saiba Mais...' da Picanha ao Alho, o modal abre mostrando 'Erro' no titulo e uma mensagem de erro de interpretacao do JSON no corpo, mesmo com a resposta chegando em 200.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/produtos/{id}`, entidade `Produto`, status `200`, 40 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `resposta_truncada` | 36,835 | 36,835 | 0,0 | 0,0 | 0,0 | entregue ao modelo |
| 2 | `entidade-produto` | 26,953 | 23,953 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `corpo_nao_e_json` | 25,873 | 24,873 | 0,0 | 0,0 | 1,0 | entregue ao modelo |
| 4 | `mensagens-de-erro-do-codigo` | 22,663 | 22,663 | 0,0 | 0,0 | 0,0 | descartado |
| 5 | `pagina-produtos-api` | 19,997 | 17,997 | 2,0 | 0,0 | 0,0 | descartado |
| 6 | `corpo_vazio` | 16,684 | 16,684 | 0,0 | 0,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`resposta_truncada`**

```text
[resposta_truncada] Resposta truncada
O corpo começa como JSON válido e termina no meio de um valor ou chave — faltam bytes; o parse falha com "Unexpected end of JSON input". Sinais: primeiros itens íntegros, o último cortado ou sem o colchete final; Content-Length menor que o esperado. Causa: O modo malformed_json devolve corpo cortado de propósito (produtos.py:19). Fora dele: limite num proxy, conexão encerrada durante o envio. Notas: Retificação: onde diz "Fora dele: limite num proxy, conexão encerrada durante o envio.", leia: Corrigir a descrição para incluir que o truncamento pode ser causado por limites de proxy ou interrupção de conexão. Adicione um exemplo de como verificar o Content-Length na documentação para evitar esse problema.
```

**`entidade-produto`**

```text
[entidade-produto] Produto e sua categoria
Item do cardápio em tbprodutos, ligado a uma categoria de tbtipos (Carnes, Bebidas, Acompanhamentos, Sobremesas). 14 produtos; o id 1 é Picanha ao Alho, Carnes, 89,90. Sinais: título com nome de categoria: junção trocada; preço com grandeza estranha: conversão de valor_produto. Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano. Notas: Retificação: onde diz "Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano.", leia: Corrigir a conversão do preço e destaque no _to_dict de produtos.py. Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro.
```

**`corpo_nao_e_json`**

```text
[corpo_nao_e_json] Corpo não é JSON
A resposta chega (às vezes 200 e Content-Type application/json), mas o corpo é HTML, XML ou aviso em texto — o parse falha no primeiro caractere. Sinais: console "Unexpected token <"; texto legível antes ou no lugar do JSON: Warning do PHP, página de gateway, "Atenção ERRO". Causa: Falha de conexão no site imprime "Atenção ERRO" em HTML (connect.php:16); Warning/Fatal do PHP saem antes da saída; gateway fora devolve a própria página. Notas: Adicionar um exemplo de sintoma específico, como "Página de erro HTML em vez de JSON", para melhorar a identificação de casos onde o corpo da resposta não é JSON. Adicionar um exemplo de sintoma para clarificar que XML também pode causar parse falho.
```

### Prompt

4067 caracteres em 7 partes (hash `2679a5ec817aedc1`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1226 tokens, saída de 57 (teto de 600); 83,5 s no total (68497 ms lendo o prompt, 12893 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: resposta_truncada
CAMPO: nenhum
IMPACTO: O usuário vê um erro ao tentar abrir o modal com informações do produto, devido à resposta JSON truncada.
FONTE: [resposta_truncada]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `resposta_truncada` | caracteres 12 a 29 da resposta |
| CAMPO | `nenhum` | caracteres 37 a 43 da resposta |
| IMPACTO | `O usuário vê um erro ao tentar abrir o modal com informações do produto, devido à resposta JSON truncada.` | caracteres 53 a 158 da resposta |
| FONTE | `[resposta_truncada]` | caracteres 166 a 185 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `resposta_truncada` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `resposta_truncada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `resposta_truncada` | confere | contexto: `resposta_truncada`, `entidade-produto`, `corpo_nao_e_json` |
| O campo apontado aparece no caso | `nenhum` | não se aplica | o modelo não apontou campo |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | confere | verbetes: `resposta_truncada`, `corpo_nao_e_json` |
| Notas escritas pelo modelo nos verbetes citados | `resposta_truncada` | informativo | `resposta_truncada`: 2 nota(s) do modelo (Correta: 1, Parcial: 1). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário vê um erro ao tentar abrir o modal com informações do produto, devido à resposta JSON truncada.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `resposta_truncada` | `resposta_truncada` | confere |
| O campo respondido é o esperado | `nenhum` |  | confere |
| O verbete da causa esperada estava no contexto | `resposta_truncada` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `resposta_truncada` | `resposta_truncada`, `entidade-produto`, `corpo_nao_e_json` |
| L1 | `resposta_truncada` | `resposta_truncada`, `entidade-produto`, `corpo_nao_e_json` |
| L3 | `resposta_truncada` | `resposta_truncada`, `entidade-produto`, `corpo_nao_e_json` |

## Rastro

Gerado dos eventos 3 a 30 da trilha `fase3b_ineditos__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `833aff038be4b91c`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
