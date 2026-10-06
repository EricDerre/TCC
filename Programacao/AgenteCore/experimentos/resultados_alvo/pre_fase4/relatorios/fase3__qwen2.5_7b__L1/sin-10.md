<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `sin-10` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3/qwen2.5_7b/sin-10@L1`. Corrida `fase3`, Ollama 0.34.0; classe 2, nível 2; texto dos casos: anterior à correção de 28/09/2026. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`campo_renomeado`, `contrato-pedido`, `pedido-reserva`); prompt de 1251 tokens; resposta de 53 tokens em 82,6 s |
| O que o modelo declarou | causa `campo_renomeado`; 2 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 8 de 8 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "situacao": "Em Analise", "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: A coluna de situacao da reserva aparece vazia na area do cliente.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/pedidos`, entidade `Pedido`, status `200`, 35 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `campo_renomeado` | 36,524 | 34,524 | 2,0 | 0,0 | 0,0 | entregue ao modelo |
| 2 | `contrato-pedido` | 35,715 | 32,715 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `pedido-reserva` | 26,433 | 23,433 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 4 | `chave_de_juncao_errada` | 23,720 | 20,720 | 2,0 | 1,0 | 0,0 | descartado |
| 5 | `campo_ausente` | 19,802 | 17,802 | 2,0 | 0,0 | 0,0 | descartado |
| 6 | `usuario-e-login` | 19,625 | 19,625 | 0,0 | 0,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`campo_renomeado`**

```text
[campo_renomeado] Campo renomeado
O valor existe sob outra chave: falta a esperada e aparece uma desconhecida com o mesmo tipo e conteúdo (preco → preco_v2, nome → descricao, status → situacao). Sinais: o resto do objeto confere; uma chave sumiu e outra sobrou; vazio ou undefined só naquele campo. Causa: O modo field_renamed troca o campo-alvo por <campo>_v2 (fault_injection.py). Fora dele: contrato mudou no servidor sem atualizar o cliente. Notas: Retificação: onde diz "Fora dele: contrato mudou no servidor sem atualizar o cliente.", leia: Corrigir a afirmação para "Contrato mudou no servidor sem atualizar o cliente e API não reflete as mudanças.".
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

4026 caracteres em 7 partes (hash `d5305b9d4e4e79af`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1251 tokens, saída de 53 (teto de 600); 82,6 s no total (68481 ms lendo o prompt, 11973 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: campo_renomeado
CAMPO: situacao
IMPACTO: O usuário vê a coluna de status vazia na área do cliente.
FONTE: [campo_renomeado] [contrato-pedido]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `campo_renomeado` | caracteres 12 a 27 da resposta |
| CAMPO | `situacao` | caracteres 35 a 43 da resposta |
| IMPACTO | `O usuário vê a coluna de status vazia na área do cliente.` | caracteres 53 a 110 da resposta |
| FONTE | `[campo_renomeado] [contrato-pedido]` | caracteres 118 a 153 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `campo_renomeado` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | confere | contexto: `campo_renomeado`, `contrato-pedido`, `pedido-reserva` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `campo_renomeado`, `contrato-pedido`, `pedido-reserva` |
| O campo apontado aparece no caso | `situacao` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `campo_renomeado` |
| Notas escritas pelo modelo nos verbetes citados | `campo_renomeado`, `contrato-pedido` | informativo | `campo_renomeado`: 1 nota(s) do modelo (Parcial: 1); `contrato-pedido`: sem notas do modelo. A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário vê a coluna de status vazia na área do cliente.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `campo_renomeado` | `campo_renomeado` | confere |
| O campo respondido é o esperado | `situacao` | `status` | **não confere** |
| O verbete da causa esperada estava no contexto | `campo_renomeado` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `campo_renomeado` | `campo_renomeado`, `contrato-pedido`, `pedido-reserva` |
| L1 | `campo_renomeado` | `campo_renomeado`, `contrato-pedido`, `pedido-reserva` |
| L2 | `campo_renomeado` | `campo_renomeado`, `contrato-pedido`, `pedido-reserva` |
| L3 | `campo_renomeado` | `campo_renomeado`, `contrato-pedido`, `pedido-reserva` |

## Rastro

Gerado dos eventos 1173 a 1197 da trilha `fase3__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `76f65be25bac8b24`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
