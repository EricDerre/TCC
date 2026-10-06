<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `tra-18` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3b_ineditos/qwen2.5_7b/tra-18@L1`. Corrida `fase3b_ineditos`, Ollama 0.34.1; classe 4, nível 2; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`contrato-pedido`, `pedido-reserva`, `estado_da_tela_divergente`); prompt de 1446 tokens; resposta de 66 tokens em 72,1 s |
| O que o modelo declarou | causa `contagem_inconsistente`; 2 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 7 de 8 conferências conferem; o que não confere: nenhum verbete do contexto trata da causa respondida (`contagem_inconsistente`) |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: A resposta de GET /api/pedidos traz so 1 reserva do Cliente Teste, mas ele fez 3 reservas nos ultimos meses; as outras duas nao aparecem nem como ativas nem como canceladas.

OBSERVAÇÃO ADICIONAL: A consulta filtra por id_clientes = cliente.id_usuario; as 3 reservas estao todas com o mesmo id_clientes no banco.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/pedidos`, entidade `Pedido`, status `200`, 62 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `contrato-pedido` | 50,810 | 47,810 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `pedido-reserva` | 36,026 | 33,026 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `estado_da_tela_divergente` | 33,903 | 33,903 | 0,0 | 0,0 | 0,0 | entregue ao modelo |
| 4 | `chave_de_juncao_errada` | 29,123 | 26,123 | 2,0 | 1,0 | 0,0 | descartado |
| 5 | `valor_fora_do_dominio` | 26,895 | 23,895 | 2,0 | 1,0 | 0,0 | descartado |
| 6 | `formato_de_data_divergente` | 25,437 | 22,437 | 2,0 | 1,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`contrato-pedido`**

```text
[contrato-pedido] Contrato de /api/pedidos
GET /api/pedidos?login=<cpf>; POST /api/pedidos {id_clientes, pessoas, data_pedido} → 201; POST /api/pedidos/{id}/cancelar. Campos: id_pedido, pessoas, data_pedido AAAA-MM-DD, status 'Em Análise'|'Cancelado', nome, cpf. Sinais: data noutro formato ou como número; status fora dos dois valores. Causa: cpf vem de login_usuario (pedidos.py). Busca exata na API; o site usa LIKE '%login%' (cliente/index.php:4).
```

**`pedido-reserva`**

```text
[pedido-reserva] Reserva de mesa (pedido)
Reserva em tbpedido_reserva: id_pedido, id_clientes (chave para tbusuarios), pessoas, data_pedido, status. Status só admite 'Em Análise' (inicial) e 'Cancelado'. Sinais: status com outro texto: fora do domínio; linha de reserva toda vazia: cliente que ainda não reservou. Causa: A leitura usa vw_tbpedidos, LEFT JOIN de tbusuarios (schema_completo.sql:57): cliente sem reserva vira linha com campos nulos, que reserva_cli.php renderiza. Notas: Retificação: onde diz "cliente sem reserva vira linha com campos nulos, que reserva_cli.php renderiza.", leia: Corrigir a renderização para não exibir linhas com campos nulos quando o cliente não reservou. Retificação: onde diz "Status só admite 'Em Análise' (inicial) e 'Cancelado'.", leia: Adicionar validação no backend para verificar se o status está dentro do domínio permitido. Retificação: onde diz "A leitura usa vw_tbpedidos, LEFT JOIN de tbusuarios (schema_completo.sql:57): cliente sem reserva vira linha com campos nulos, que reserva_cli.php renderiza.", leia: Corrigir a lógica do LEFT JOIN para evitar linhas nulas quando o cliente não tem reserva.
```

**`estado_da_tela_divergente`**

```text
[estado_da_tela_divergente] Estado da tela divergente da resposta
A rede está certa — status e corpo conferem — e o usuário vê outra coisa: "Carregando" parado, lista vazia, botão que não muda. Sinais: nenhum erro de console nem status de erro; recarregar corrige: o estado não foi atualizado. Causa: produtos_api.php só limpa "Carregando..." no then() do fetch e substitui o grid por innerHTML; na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7). Notas: Retificação: onde diz "na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7).", leia: Corrigir a lógica de cancelamento para não depender de redirect, garantindo a atualização do estado da tela. Retificação: onde diz "na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7).", leia: Corrigir a implementação do cancelamento para que não dependa apenas do redirect, mas também limpe o estado da tela corretamente. Retificação: onde diz "na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7).", leia: Corrigir a lógica de cancelamento para não depender do redirect, garantindo que a interface seja atualizada corretamente.
```

### Prompt

4770 caracteres em 7 partes (hash `ec05187c0649b1d5`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1446 tokens, saída de 66 (teto de 600); 72,1 s no total (54610 ms lendo o prompt, 15314 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: contagem_inconsistente
CAMPO: id_pedido
IMPACTO: O usuário vê apenas uma das três reservas do Cliente Teste, enquanto as outras duas não são exibidas.
FONTE: [pedido-reserva] [estado_da_tela_divergente]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `contagem_inconsistente` | caracteres 12 a 34 da resposta |
| CAMPO | `id_pedido` | caracteres 42 a 51 da resposta |
| IMPACTO | `O usuário vê apenas uma das três reservas do Cliente Teste, enquanto as outras duas não são exibidas.` | caracteres 61 a 162 da resposta |
| FONTE | `[pedido-reserva] [estado_da_tela_divergente]` | caracteres 170 a 214 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `contagem_inconsistente` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `pedido-reserva` | confere |  |
| O verbete citado existe na biblioteca | `estado_da_tela_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `pedido-reserva` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `estado_da_tela_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `estado_da_tela_divergente` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `estado_da_tela_divergente` |
| O campo apontado aparece no caso | `id_pedido` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | **não confere** | nenhum verbete do contexto trata dessa causa |
| Notas escritas pelo modelo nos verbetes citados | `pedido-reserva`, `estado_da_tela_divergente` | informativo | `pedido-reserva`: 3 nota(s) do modelo (Errada: 3); `estado_da_tela_divergente`: 3 nota(s) do modelo (Errada: 3). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário vê apenas uma das três reservas do Cliente Teste, enquanto as outras duas não são exibidas.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `contagem_inconsistente` | `contagem_inconsistente` | confere |
| O campo respondido é o esperado | `id_pedido` |  | **não confere** |
| O verbete da causa esperada estava no contexto | `contagem_inconsistente` |  | **não confere** |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `contagem_inconsistente` | `contrato-pedido`, `pedido-reserva`, `estado_da_tela_divergente` |
| L1 | `contagem_inconsistente` | `contrato-pedido`, `pedido-reserva`, `estado_da_tela_divergente` |
| L3 | `contagem_inconsistente` | `contrato-pedido`, `pedido-reserva`, `estado_da_tela_divergente` |

## Rastro

Gerado dos eventos 499 a 523 da trilha `fase3b_ineditos__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `31792e414097f6cb`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
