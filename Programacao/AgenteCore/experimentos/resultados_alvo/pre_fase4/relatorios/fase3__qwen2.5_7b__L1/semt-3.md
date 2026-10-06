<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `semt-3` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3/qwen2.5_7b/semt-3@L1`. Corrida `fase3`, Ollama 0.34.0; classe 3, nível 2; texto dos casos: anterior à correção de 28/09/2026. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`contrato-pedido`, `estado_da_tela_divergente`, `valor_fora_do_dominio`); prompt de 1238 tokens; resposta de 73 tokens em 85,5 s |
| O que o modelo declarou | causa `valor_fora_do_dominio`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 6 de 6 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Pendente", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: A reserva nao aparece nem como ativa nem como cancelada na area do cliente.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/pedidos`, entidade `Pedido`, status `200`, 37 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `contrato-pedido` | 33,658 | 30,658 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `estado_da_tela_divergente` | 31,131 | 31,131 | 0,0 | 0,0 | 0,0 | entregue ao modelo |
| 3 | `valor_fora_do_dominio` | 28,622 | 25,622 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 4 | `pedido-reserva` | 22,739 | 19,739 | 2,0 | 1,0 | 0,0 | descartado |
| 5 | `chave_de_juncao_errada` | 22,003 | 19,003 | 2,0 | 1,0 | 0,0 | descartado |
| 6 | `formato_de_data_divergente` | 20,759 | 17,759 | 2,0 | 1,0 | 0,0 | descartado |

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

**`valor_fora_do_dominio`**

```text
[valor_fora_do_dominio] Valor fora do domínio
Tipo certo, valor fora do conjunto permitido: status diferente de 'Em Análise'/'Cancelado', destaque diferente de true/false, pessoas menor que 1. Sinais: reserva nem ativa nem cancelada na tela: status inesperado; 0 ou negativo em pessoas: o mínimo só existe no HTML. Causa: status e destaque são ENUM no banco (schema_completo.sql:37); pessoas ≥ 1 é só min= do HTML (registrar_reserva.php:55); a API não valida o que devolve. Notas: Retificação: onde diz "Valor fora do domínio", leia: Adicionar validação no status do pedido na API para evitar valores fora do domínio.
```

### Prompt

4000 caracteres em 7 partes (hash `7a8d5363f39f6c56`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1238 tokens, saída de 73 (teto de 600); 85,5 s no total (66869 ms lendo o prompt, 16494 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: valor_fora_do_dominio
CAMPO: status
IMPACTO: O usuário vê a reserva como "Pendente" na área do cliente, que não é um valor permitido, causando confusão.
FONTE: [contrato-pedido], [valor_força_do_dominio]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `valor_fora_do_dominio` | caracteres 12 a 33 da resposta |
| CAMPO | `status` | caracteres 41 a 47 da resposta |
| IMPACTO | `O usuário vê a reserva como "Pendente" na área do cliente, que não é um valor permitido, causando confusão.` | caracteres 57 a 164 da resposta |
| FONTE | `[contrato-pedido], [valor_força_do_dominio]` | caracteres 172 a 215 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `valor_fora_do_dominio` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `estado_da_tela_divergente`, `valor_fora_do_dominio` |
| O campo apontado aparece no caso | `status` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `valor_fora_do_dominio` | confere | verbetes: `contrato-pedido`, `valor_fora_do_dominio` |
| Notas escritas pelo modelo nos verbetes citados | `contrato-pedido` | informativo | `contrato-pedido`: sem notas do modelo. A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário vê a reserva como "Pendente" na área do cliente, que não é um valor permitido, causando confusão.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `valor_fora_do_dominio` | `valor_fora_do_dominio` | confere |
| O campo respondido é o esperado | `status` | `status` | confere |
| O verbete da causa esperada estava no contexto | `valor_fora_do_dominio` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `valor_fora_do_dominio` | `contrato-pedido`, `estado_da_tela_divergente`, `valor_fora_do_dominio` |
| L1 | `valor_fora_do_dominio` | `contrato-pedido`, `estado_da_tela_divergente`, `valor_fora_do_dominio` |
| L2 | `valor_fora_do_dominio` | `contrato-pedido`, `estado_da_tela_divergente`, `valor_fora_do_dominio` |
| L3 | `valor_fora_do_dominio` | `contrato-pedido`, `estado_da_tela_divergente`, `valor_fora_do_dominio` |

## Rastro

Gerado dos eventos 369 a 392 da trilha `fase3__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `6a46a0777126c611`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
