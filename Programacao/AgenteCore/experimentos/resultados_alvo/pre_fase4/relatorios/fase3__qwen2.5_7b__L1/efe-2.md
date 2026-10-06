<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `efe-2` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3/qwen2.5_7b/efe-2@L1`. Corrida `fase3`, Ollama 0.34.0; classe 6, nível 2; texto dos casos: anterior à correção de 28/09/2026. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`contrato-pedido`, `estado_da_tela_divergente`, `fluxo-reserva-e-cancelamento`); prompt de 1165 tokens; resposta de 65 tokens em 54,6 s |
| O que o modelo declarou | causa `estado_da_tela_divergente`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 5 de 5 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: POST /api/pedidos/7/cancelar -> 200 | tela do cliente

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
A API devolveu {"id_pedido": 7, "status": "Cancelado"}

SINTOMA OBSERVADO: A tela continua exibindo a reserva 7 como 'Em Analise' apos o cancelamento.
```

### Busca na biblioteca

Consulta montada em código: endpoint `POST /api/pedidos/{id}/cancelar`, entidade `Pedido`, status `200`, 23 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `contrato-pedido` | 24,015 | 21,015 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `estado_da_tela_divergente` | 21,585 | 21,585 | 0,0 | 0,0 | 0,0 | entregue ao modelo |
| 3 | `fluxo-reserva-e-cancelamento` | 18,926 | 15,926 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 4 | `valor_fora_do_dominio` | 18,670 | 17,670 | 0,0 | 1,0 | 0,0 | descartado |
| 5 | `pedido-reserva` | 18,284 | 17,284 | 0,0 | 1,0 | 0,0 | descartado |
| 6 | `consultas-sem-checagem` | 14,838 | 13,838 | 0,0 | 1,0 | 0,0 | descartado |

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

**`fluxo-reserva-e-cancelamento`**

```text
[fluxo-reserva-e-cancelamento] Fluxo de reservar e cancelar
Reserva em cliente/registrar_reserva.php e cancelamento em reserva_cli.php; a API espelha em POST /api/pedidos e POST /api/pedidos/{id}/cancelar. Sinais: regra de data e quantidade só no navegador; reserva alheia cancelada sem checagem de dono. Causa: Data hoje+2 a hoje+90 e pessoas ≥ 1 são só min/max do HTML (registrar_reserva.php:28-35,55); cancelar grava 'Cancelado' (pedidos.py:75).
```

### Prompt

3774 caracteres em 7 partes (hash `fd3cfbf28ebbd1c9`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1165 tokens, saída de 65 (teto de 600); 54,6 s no total (37971 ms lendo o prompt, 14516 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: estado_da_tela_divergente
CAMPO: nenhum
IMPACTO: A tela do cliente não reflete o status 'Cancelado' do pedido 7, continuando a exibir 'Em Analise'.
FONTE: [estado_da_tela_divergente]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `estado_da_tela_divergente` | caracteres 12 a 37 da resposta |
| CAMPO | `nenhum` | caracteres 45 a 51 da resposta |
| IMPACTO | `A tela do cliente não reflete o status 'Cancelado' do pedido 7, continuando a exibir 'Em Analise'.` | caracteres 61 a 159 da resposta |
| FONTE | `[estado_da_tela_divergente]` | caracteres 167 a 194 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `estado_da_tela_divergente` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `estado_da_tela_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `estado_da_tela_divergente` | confere | contexto: `contrato-pedido`, `estado_da_tela_divergente`, `fluxo-reserva-e-cancelamento` |
| O campo apontado aparece no caso | `nenhum` | não se aplica | o modelo não apontou campo |
| Algum verbete do contexto trata da causa respondida | `estado_da_tela_divergente` | confere | verbetes: `estado_da_tela_divergente`, `fluxo-reserva-e-cancelamento` |
| Notas escritas pelo modelo nos verbetes citados | `estado_da_tela_divergente` | informativo | `estado_da_tela_divergente`: 3 nota(s) do modelo (Errada: 3). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `A tela do cliente não reflete o status 'Cancelado' do pedido 7, continuando a exibir 'Em Analise'.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `estado_da_tela_divergente` | `estado_da_tela_divergente` | confere |
| O campo respondido é o esperado | `nenhum` | `status` | **não confere** |
| O verbete da causa esperada estava no contexto | `estado_da_tela_divergente` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `estado_da_tela_divergente` | `estado_da_tela_divergente`, `contrato-pedido`, `pedido-reserva` |
| L1 | `estado_da_tela_divergente` | `contrato-pedido`, `estado_da_tela_divergente`, `fluxo-reserva-e-cancelamento` |
| L2 | `estado_da_tela_divergente` | `contrato-pedido`, `estado_da_tela_divergente`, `fluxo-reserva-e-cancelamento` |
| L3 | `estado_da_tela_divergente` | `contrato-pedido`, `estado_da_tela_divergente`, `fluxo-reserva-e-cancelamento` |

## Rastro

Gerado dos eventos 754 a 776 da trilha `fase3__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `bd695397c82806f7`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
