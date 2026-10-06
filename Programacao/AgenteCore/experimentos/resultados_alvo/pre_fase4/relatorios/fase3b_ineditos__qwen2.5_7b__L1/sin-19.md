<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `sin-19` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3b_ineditos/qwen2.5_7b/sin-19@L1`. Corrida `fase3b_ineditos`, Ollama 0.34.1; classe 2, nível 2; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`contrato-pedido`, `estado_da_tela_divergente`, `colecao_no_lugar_de_objeto`); prompt de 1391 tokens; resposta de 68 tokens em 80,1 s |
| O que o modelo declarou | causa `colecao_no_lugar_de_objeto`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 6 de 6 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: POST /api/pedidos/7/cancelar

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto (recurso unico, nao lista)

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Cancelado", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: A resposta de POST /api/pedidos/7/cancelar vem como lista com um item, em vez do objeto unico que o contrato descreve; ler resposta.status direto da undefined.
```

### Busca na biblioteca

Consulta montada em código: endpoint `POST /api/pedidos/{id}/cancelar`, entidade `Pedido`, status `200`, 51 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `contrato-pedido` | 48,853 | 45,853 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `estado_da_tela_divergente` | 39,892 | 39,892 | 0,0 | 0,0 | 0,0 | entregue ao modelo |
| 3 | `colecao_no_lugar_de_objeto` | 32,406 | 32,406 | 0,0 | 0,0 | 0,0 | entregue ao modelo |
| 4 | `fluxo-reserva-e-cancelamento` | 27,677 | 24,677 | 2,0 | 1,0 | 0,0 | descartado |
| 5 | `formato_de_data_divergente` | 22,723 | 21,723 | 0,0 | 1,0 | 0,0 | descartado |
| 6 | `campo_ausente` | 22,608 | 22,608 | 0,0 | 0,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`contrato-pedido`**

```text
[contrato-pedido] Contrato de /api/pedidos
GET /api/pedidos?login=<cpf>; POST /api/pedidos {id_clientes, pessoas, data_pedido} → 201; POST /api/pedidos/{id}/cancelar. Campos: id_pedido, pessoas, data_pedido AAAA-MM-DD, status 'Em Análise'|'Cancelado', nome, cpf. Sinais: data noutro formato ou como número; status fora dos dois valores. Causa: cpf vem de login_usuario (pedidos.py). Busca exata na API; o site usa LIKE '%login%' (cliente/index.php:4).
```

**`estado_da_tela_divergente`**

```text
[estado_da_tela_divergente] Estado da tela divergente da resposta
A rede está certa — status e corpo conferem — e o usuário vê outra coisa: "Carregando" parado, lista vazia, botão que não muda. Sinais: nenhum erro de console nem status de erro; recarregar corrige: o estado não foi atualizado. Causa: produtos_api.php só limpa "Carregando..." no then() do fetch e substitui o grid por innerHTML; na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7). Notas: Retificação: onde diz "na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7).", leia: Corrigir a lógica de cancelamento para não depender de redirect, garantindo a atualização do estado da tela. Retificação: onde diz "na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7).", leia: Corrigir a implementação do cancelamento para que não dependa apenas do redirect, mas também limpe o estado da tela corretamente. Retificação: onde diz "na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7).", leia: Corrigir a lógica de cancelamento para não depender do redirect, garantindo que a interface seja atualizada corretamente.
```

**`colecao_no_lugar_de_objeto`**

```text
[colecao_no_lugar_de_objeto] Coleção no lugar de objeto (ou o inverso)
Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (["Carnes"]). Sinais: modal "Produto #1"/"(sem descrição)": p é lista; categoria com colchetes: campo veio como lista. Causa: GET /api/produtos devolve lista, GET /api/produtos/{id} objeto (produtos.py); a página não confere a forma antes de ler os campos. Notas: Retificação: onde diz "Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (['Carnes']).", leia: Corrigir que GET /api/produtos/{id} deve devolver um objeto, não uma lista. Retificação: onde diz "Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (['Carnes']).", leia: Corrigir que o campo "tipo" deve ser tratado como uma string, não uma lista.
```

### Prompt

4513 caracteres em 7 partes (hash `5ef4fdb53ae296f4`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1391 tokens, saída de 68 (teto de 600); 80,1 s no total (62241 ms lendo o prompt, 15735 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: colecao_no_lugar_de_objeto
CAMPO: id_pedido
IMPACTO: O usuário vê um objeto dentro de uma lista, o que pode causar confusão e dificuldade na manipulação da resposta.
FONTE: [colecao_no_lugar_de_objeto]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `colecao_no_lugar_de_objeto` | caracteres 12 a 38 da resposta |
| CAMPO | `id_pedido` | caracteres 46 a 55 da resposta |
| IMPACTO | `O usuário vê um objeto dentro de uma lista, o que pode causar confusão e dificuldade na manipulação da resposta.` | caracteres 65 a 177 da resposta |
| FONTE | `[colecao_no_lugar_de_objeto]` | caracteres 185 a 213 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `colecao_no_lugar_de_objeto` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `colecao_no_lugar_de_objeto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `colecao_no_lugar_de_objeto` | confere | contexto: `contrato-pedido`, `estado_da_tela_divergente`, `colecao_no_lugar_de_objeto` |
| O campo apontado aparece no caso | `id_pedido` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `colecao_no_lugar_de_objeto` |
| Notas escritas pelo modelo nos verbetes citados | `colecao_no_lugar_de_objeto` | informativo | `colecao_no_lugar_de_objeto`: 2 nota(s) do modelo (Correta: 1, Errada: 1). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário vê um objeto dentro de uma lista, o que pode causar confusão e dificuldade na manipulação da resposta.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | confere |
| O campo respondido é o esperado | `id_pedido` |  | **não confere** |
| O verbete da causa esperada estava no contexto | `colecao_no_lugar_de_objeto` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `colecao_no_lugar_de_objeto` | `contrato-pedido`, `estado_da_tela_divergente`, `colecao_no_lugar_de_objeto` |
| L1 | `colecao_no_lugar_de_objeto` | `contrato-pedido`, `estado_da_tela_divergente`, `colecao_no_lugar_de_objeto` |
| L3 | `colecao_no_lugar_de_objeto` | `contrato-pedido`, `estado_da_tela_divergente`, `colecao_no_lugar_de_objeto` |

## Rastro

Gerado dos eventos 232 a 254 da trilha `fase3b_ineditos__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `81bcb2a5fa2f9099`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
