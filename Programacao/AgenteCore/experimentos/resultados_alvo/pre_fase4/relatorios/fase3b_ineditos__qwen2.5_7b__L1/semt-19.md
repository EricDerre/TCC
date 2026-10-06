<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `semt-19` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3b_ineditos/qwen2.5_7b/semt-19@L1`. Corrida `fase3b_ineditos`, Ollama 0.34.1; classe 3, nível 2; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`formato_de_data_divergente`, `contrato-pedido`, `pedido-reserva`); prompt de 1422 tokens; resposta de 61 tokens em 97,1 s |
| O que o modelo declarou | causa `formato_de_data_divergente`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 6 de 6 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10T00:00:00Z", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: O campo data_pedido chega como '2026-09-10T00:00:00Z' (data e hora, com Z de UTC) em vez do formato so-data (AAAA-MM-DD) do contrato; quem espera so a data tem que lidar com hora e fuso que nao deveriam estar ali.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/pedidos`, entidade `Pedido`, status `200`, 56 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `formato_de_data_divergente` | 77,936 | 74,936 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `contrato-pedido` | 68,668 | 65,668 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `pedido-reserva` | 28,777 | 25,777 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 4 | `chave_de_juncao_errada` | 23,576 | 20,576 | 2,0 | 1,0 | 0,0 | descartado |
| 5 | `escala_ou_unidade_errada` | 21,529 | 19,529 | 2,0 | 0,0 | 0,0 | descartado |
| 6 | `fluxo-reserva-e-cancelamento` | 19,017 | 18,017 | 0,0 | 1,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`formato_de_data_divergente`**

```text
[formato_de_data_divergente] Formato de data divergente
data_pedido deve ser texto AAAA-MM-DD. Chega noutro formato (10/09/2026), como segundos (1789084800) ou com hora e fuso — e o cliente não interpreta. Sinais: "Invalid Date" na listagem: formato brasileiro ou texto não reconhecido; número grande no lugar da data: timestamp. Causa: A API devolve data_pedido.isoformat() (pedidos.py:23), sempre AAAA-MM-DD. Em escala_ou_unidade_errada a data é legível mas deslocada; aqui é ilegível. Notas: Retificação: onde diz "data_pedido deve ser texto AAAA-MM-DD. Chega noutro formato (10/09/2026), como segundos (1789084800) ou com hora e fuso — e o cliente não interpreta.", leia: Adicione que o formato ISO 8601 é obrigatório e que datas devem ser passadas no formato AAAA-MM-DD, sem hora ou fuso horário. Corrija que o timestamp deve ser convertido para o formato ISO 8601 antes de ser devolvido.
```

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

### Prompt

4418 caracteres em 7 partes (hash `4a48ee6a47d21063`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1422 tokens, saída de 61 (teto de 600); 97,1 s no total (81014 ms lendo o prompt, 13930 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: formato_de_data_divergente
CAMPO: data_pedido
IMPACTO: O usuário recebe uma data com hora e fuso UTC, enquanto esperava apenas a data no formato AAAA-MM-DD.
FONTE: [formato_de_data_divergente]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `formato_de_data_divergente` | caracteres 12 a 38 da resposta |
| CAMPO | `data_pedido` | caracteres 46 a 57 da resposta |
| IMPACTO | `O usuário recebe uma data com hora e fuso UTC, enquanto esperava apenas a data no formato AAAA-MM-DD.` | caracteres 67 a 168 da resposta |
| FONTE | `[formato_de_data_divergente]` | caracteres 176 a 204 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `formato_de_data_divergente` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `formato_de_data_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `formato_de_data_divergente` | confere | contexto: `formato_de_data_divergente`, `contrato-pedido`, `pedido-reserva` |
| O campo apontado aparece no caso | `data_pedido` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `formato_de_data_divergente` | confere | verbetes: `formato_de_data_divergente`, `contrato-pedido` |
| Notas escritas pelo modelo nos verbetes citados | `formato_de_data_divergente` | informativo | `formato_de_data_divergente`: 1 nota(s) do modelo (Errada: 1). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário recebe uma data com hora e fuso UTC, enquanto esperava apenas a data no formato AAAA-MM-DD.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `formato_de_data_divergente` | `formato_de_data_divergente` | confere |
| O campo respondido é o esperado | `data_pedido` | `data_pedido` | confere |
| O verbete da causa esperada estava no contexto | `formato_de_data_divergente` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `formato_de_data_divergente` | `formato_de_data_divergente`, `contrato-pedido`, `pedido-reserva` |
| L1 | `formato_de_data_divergente` | `formato_de_data_divergente`, `contrato-pedido`, `pedido-reserva` |
| L3 | `formato_de_data_divergente` | `formato_de_data_divergente`, `contrato-pedido`, `pedido-reserva` |

## Rastro

Gerado dos eventos 374 a 396 da trilha `fase3b_ineditos__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `67d8b7d456539469`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
