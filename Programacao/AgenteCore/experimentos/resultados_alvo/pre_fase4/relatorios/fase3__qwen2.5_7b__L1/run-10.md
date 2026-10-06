<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `run-10` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3/qwen2.5_7b/run-10@L1`. Corrida `fase3`, Ollama 0.34.0; classe 5, nível 2; texto dos casos: anterior à correção de 28/09/2026. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`limite_de_requisicoes`, `contagem_inconsistente`, `estrutura_aninhada_divergente`); prompt de 1153 tokens; resposta de 75 tokens em 43,6 s |
| O que o modelo declarou | causa `limite_de_requisicoes`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 5 de 5 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos (12a requisicao em 1 min)

STATUS HTTP: 429

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"detail": "rate limit exceeded", "retry_after": 30}

SINTOMA OBSERVADO: Durante a execucao do roteiro de teste, a partir de certo ponto tudo falha.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/produtos`, entidade `Produto`, status `429`, 32 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `limite_de_requisicoes` | 45,159 | 42,159 | 2,0 | 0,0 | 1,0 | entregue ao modelo |
| 2 | `contagem_inconsistente` | 21,116 | 18,116 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `estrutura_aninhada_divergente` | 20,211 | 17,211 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 4 | `valor_fora_do_dominio` | 10,779 | 8,779 | 2,0 | 0,0 | 0,0 | descartado |
| 5 | `tempo_de_resposta_excedido` | 10,547 | 7,547 | 2,0 | 0,0 | 1,0 | descartado |
| 6 | `tipo_divergente` | 9,952 | 6,952 | 2,0 | 1,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`limite_de_requisicoes`**

```text
[limite_de_requisicoes] Limite de requisições (429)
Status 429: o servidor ou um intermediário recusou por excesso de requisições num intervalo. Resposta rápida e com corpo — não é lentidão nem erro interno. Sinais: funciona, depois falha após recarregar muitas vezes; "Erro ao carregar produtos da CobaiaAPI: HTTP 429"; pode vir retry_after. Causa: A CobaiaAPI não tem limitador (main.py só registra CORS e routers); um 429 vem de proxy, gateway ou servidor diferente do esperado.
```

**`contagem_inconsistente`**

```text
[contagem_inconsistente] Contagem inconsistente
Dois números que deveriam bater não batem: total 14 e lista com 1; total 0 com itens; página 2 vazia com total 14; contador de destaques diferente dos cartões. Sinais: total e lista vêm de consultas diferentes; rótulo numérico que não corresponde ao renderizado. Causa: GET /api/produtos devolve a lista crua, sem total nem paginação (produtos.py:34-43); o seed tem 14 produtos, 5 em destaque. Envelope com total indica outra versão.
```

**`estrutura_aninhada_divergente`**

```text
[estrutura_aninhada_divergente] Estrutura aninhada divergente
Chaves existem, mas noutro nível: lista num envelope ({"data": {"itens": [...]}}) ou campo simples como objeto ({"id": 1, "nome": "Carnes"}). Sinais: envelope na raiz: Array.isArray falha, "Nenhum produto retornado"; campo como objeto: cartão imprime [object Object]. Causa: Contrato real: lista crua na raiz e tipo como texto (produtos.py _to_dict); envelope ou aninhamento veio de outra versão ou intermediário. Notas: Retificação: onde diz "Chaves existem, mas noutro nível: lista num envelope ({'data': {'itens': [...]}}) ou campo simples como objeto ({'id': 1, 'nome': 'Carnes'}).", leia: Adicionar exemplo de estrutura aninhada divergente no verbete. Retificação: onde diz "Chaves existem, mas noutro nível: lista num envelope ({'data': {'itens': [...]}}) ou campo simples como objeto ({'id': 1, 'nome': 'Carnes'}).", leia: Corrigir a estrutura da resposta da API para ser consistente, evitando envelopes ou campos simples aninhados, para padronizar o desenpacotamento dos dados.
```

### Prompt

3687 caracteres em 7 partes (hash `d984f6980818e9e5`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1153 tokens, saída de 75 (teto de 600); 43,6 s no total (24640 ms lendo o prompt, 16789 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: limite_de_requisicoes
CAMPO: nenhum
IMPACTO: O usuário recebe um erro de limite de requisições após várias tentativas, indicando que o sistema rejeitou as solicitações devido ao excesso de requisições.
FONTE: [limite_de_requisicoes]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `limite_de_requisicoes` | caracteres 12 a 33 da resposta |
| CAMPO | `nenhum` | caracteres 41 a 47 da resposta |
| IMPACTO | `O usuário recebe um erro de limite de requisições após várias tentativas, indicando que o sistema rejeitou as solicitações devido ao excesso de requisições.` | caracteres 57 a 213 da resposta |
| FONTE | `[limite_de_requisicoes]` | caracteres 221 a 244 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `limite_de_requisicoes` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `limite_de_requisicoes` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `limite_de_requisicoes` | confere | contexto: `limite_de_requisicoes`, `contagem_inconsistente`, `estrutura_aninhada_divergente` |
| O campo apontado aparece no caso | `nenhum` | não se aplica | o modelo não apontou campo |
| Algum verbete do contexto trata da causa respondida | `limite_de_requisicoes` | confere | verbetes: `limite_de_requisicoes` |
| Notas escritas pelo modelo nos verbetes citados | `limite_de_requisicoes` | informativo | `limite_de_requisicoes`: sem notas do modelo. A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário recebe um erro de limite de requisições após várias tentativas, indicando que o sistema rejeitou as solicitações devido ao excesso de requisições.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `limite_de_requisicoes` | `limite_de_requisicoes` | confere |
| O campo respondido é o esperado | `nenhum` |  | confere |
| O verbete da causa esperada estava no contexto | `limite_de_requisicoes` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `[limite_de_requisicoes]` | `limite_de_requisicoes`, `estrutura_aninhada_divergente`, `contagem_inconsistente` |
| L1 | `limite_de_requisicoes` | `limite_de_requisicoes`, `contagem_inconsistente`, `estrutura_aninhada_divergente` |
| L2 | `[limite_de_requisicoes]` | `limite_de_requisicoes`, `estrutura_aninhada_divergente`, `contagem_inconsistente` |
| L3 | `[limite_de_requisicoes]` | `limite_de_requisicoes`, `estrutura_aninhada_divergente`, `contagem_inconsistente` |

## Rastro

Gerado dos eventos 2036 a 2057 da trilha `fase3__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `325d8ee95b0eed75`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
