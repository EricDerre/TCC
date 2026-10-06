<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `tra-15` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3/qwen2.5_7b/tra-15@L1`. Corrida `fase3`, Ollama 0.34.0; classe 4, nível 3; texto dos casos: anterior à correção de 28/09/2026. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`contrato-pedido`, `fluxo-reserva-e-cancelamento`, `pedido-reserva`); prompt de 1224 tokens; resposta de 54 tokens em 80,6 s |
| O que o modelo declarou | causa `valor_fora_do_dominio`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 6 de 6 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: POST /api/pedidos (pessoas=4) -> GET /api/pedidos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
POST enviou {"pessoas": 4}; GET devolveu [{"id_pedido": 8, "pessoas": 8, "data_pedido": "2026-09-12", "status": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: A reserva confirmada mostra o dobro de pessoas do que foi solicitado.
```

### Busca na biblioteca

Consulta montada em código: endpoint `POST /api/pedidos`, entidade `Pedido`, status `200`, 36 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `contrato-pedido` | 53,565 | 50,565 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `fluxo-reserva-e-cancelamento` | 31,257 | 28,257 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `pedido-reserva` | 30,162 | 29,162 | 0,0 | 1,0 | 0,0 | entregue ao modelo |
| 4 | `valor_fora_do_dominio` | 27,409 | 26,409 | 0,0 | 1,0 | 0,0 | descartado |
| 5 | `formato_de_data_divergente` | 20,894 | 17,894 | 2,0 | 1,0 | 0,0 | descartado |
| 6 | `chave_de_juncao_errada` | 19,743 | 18,743 | 0,0 | 1,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`contrato-pedido`**

```text
[contrato-pedido] Contrato de /api/pedidos
GET /api/pedidos?login=<cpf>; POST /api/pedidos {id_clientes, pessoas, data_pedido} → 201; POST /api/pedidos/{id}/cancelar. Campos: id_pedido, pessoas, data_pedido AAAA-MM-DD, status 'Em Análise'|'Cancelado', nome, cpf. Sinais: data noutro formato ou como número; status fora dos dois valores. Causa: cpf vem de login_usuario (pedidos.py). Busca exata na API; o site usa LIKE '%login%' (cliente/index.php:4).
```

**`fluxo-reserva-e-cancelamento`**

```text
[fluxo-reserva-e-cancelamento] Fluxo de reservar e cancelar
Reserva em cliente/registrar_reserva.php e cancelamento em reserva_cli.php; a API espelha em POST /api/pedidos e POST /api/pedidos/{id}/cancelar. Sinais: regra de data e quantidade só no navegador; reserva alheia cancelada sem checagem de dono. Causa: Data hoje+2 a hoje+90 e pessoas ≥ 1 são só min/max do HTML (registrar_reserva.php:28-35,55); cancelar grava 'Cancelado' (pedidos.py:75).
```

**`pedido-reserva`**

```text
[pedido-reserva] Reserva de mesa (pedido)
Reserva em tbpedido_reserva: id_pedido, id_clientes (chave para tbusuarios), pessoas, data_pedido, status. Status só admite 'Em Análise' (inicial) e 'Cancelado'. Sinais: status com outro texto: fora do domínio; linha de reserva toda vazia: cliente que ainda não reservou. Causa: A leitura usa vw_tbpedidos, LEFT JOIN de tbusuarios (schema_completo.sql:57): cliente sem reserva vira linha com campos nulos, que reserva_cli.php renderiza. Notas: Retificação: onde diz "cliente sem reserva vira linha com campos nulos, que reserva_cli.php renderiza.", leia: Corrigir a renderização para não exibir linhas com campos nulos quando o cliente não reservou. Retificação: onde diz "Status só admite 'Em Análise' (inicial) e 'Cancelado'.", leia: Adicionar validação no backend para verificar se o status está dentro do domínio permitido. Retificação: onde diz "A leitura usa vw_tbpedidos, LEFT JOIN de tbusuarios (schema_completo.sql:57): cliente sem reserva vira linha com campos nulos, que reserva_cli.php renderiza.", leia: Corrigir a lógica do LEFT JOIN para evitar linhas nulas quando o cliente não tem reserva.
```

### Prompt

3875 caracteres em 7 partes (hash `bf71088d7dd2437a`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1224 tokens, saída de 54 (teto de 600); 80,6 s no total (66407 ms lendo o prompt, 11995 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: valor_fora_do_dominio
CAMPO: pessoas
IMPACTO: O usuário vê que a reserva confirmada mostra o dobro de pessoas do que foi solicitado.
FONTE: [contrato-pedido]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `valor_fora_do_dominio` | caracteres 12 a 33 da resposta |
| CAMPO | `pessoas` | caracteres 41 a 48 da resposta |
| IMPACTO | `O usuário vê que a reserva confirmada mostra o dobro de pessoas do que foi solicitado.` | caracteres 58 a 144 da resposta |
| FONTE | `[contrato-pedido]` | caracteres 152 a 169 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `valor_fora_do_dominio` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `fluxo-reserva-e-cancelamento`, `pedido-reserva` |
| O campo apontado aparece no caso | `pessoas` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `valor_fora_do_dominio` | confere | verbetes: `contrato-pedido`, `fluxo-reserva-e-cancelamento`, `pedido-reserva` |
| Notas escritas pelo modelo nos verbetes citados | `contrato-pedido` | informativo | `contrato-pedido`: sem notas do modelo. A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário vê que a reserva confirmada mostra o dobro de pessoas do que foi solicitado.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `valor_fora_do_dominio` | `escala_ou_unidade_errada` | **não confere** |
| O campo respondido é o esperado | `pessoas` | `pessoas` | confere |
| O verbete da causa esperada estava no contexto | `escala_ou_unidade_errada` |  | **não confere** |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `contagem_inconsistente` | `contrato-pedido`, `pedido-reserva`, `fluxo-reserva-e-cancelamento` |
| L1 | `valor_fora_do_dominio` | `contrato-pedido`, `fluxo-reserva-e-cancelamento`, `pedido-reserva` |
| L2 | `valor_fora_do_dominio` | `contrato-pedido`, `fluxo-reserva-e-cancelamento`, `pedido-reserva` |
| L3 | `valor_fora_do_dominio` | `contrato-pedido`, `fluxo-reserva-e-cancelamento`, `pedido-reserva` |

## Rastro

Gerado dos eventos 1896 a 1917 da trilha `fase3__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `ce4785b2be5caada`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
