<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `run-18` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3b_ineditos/qwen2.5_7b/run-18@L1`. Corrida `fase3b_ineditos`, Ollama 0.34.1; classe 5, nível 2; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`limite_de_requisicoes`, `fluxo-reserva-e-cancelamento`, `tempo_de_resposta_excedido`); prompt de 1014 tokens; resposta de 71 tokens em 18,2 s |
| O que o modelo declarou | causa `limite_de_requisicoes`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 5 de 5 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: POST /api/pedidos (6a tentativa de reserva no mesmo minuto)

STATUS HTTP: 429

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
{"detail": "too many requests"}

SINTOMA OBSERVADO: Ao tentar confirmar a reserva varias vezes seguidas em pouco tempo, a API passa a recusar com 429; a reserva nao chega a ser criada.
```

### Busca na biblioteca

Consulta montada em código: endpoint `POST /api/pedidos`, entidade `Pedido`, status `429`, 38 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `limite_de_requisicoes` | 53,567 | 52,567 | 0,0 | 0,0 | 1,0 | entregue ao modelo |
| 2 | `fluxo-reserva-e-cancelamento` | 20,542 | 17,542 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `tempo_de_resposta_excedido` | 18,055 | 17,055 | 0,0 | 0,0 | 1,0 | entregue ao modelo |
| 4 | `contagem_inconsistente` | 15,804 | 15,804 | 0,0 | 0,0 | 0,0 | descartado |
| 5 | `estrutura_aninhada_divergente` | 15,327 | 15,327 | 0,0 | 0,0 | 0,0 | descartado |
| 6 | `pedido-reserva` | 12,646 | 11,646 | 0,0 | 1,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`limite_de_requisicoes`**

```text
[limite_de_requisicoes] Limite de requisições (429)
Status 429: o servidor ou um intermediário recusou por excesso de requisições num intervalo. Resposta rápida e com corpo — não é lentidão nem erro interno. Sinais: funciona, depois falha após recarregar muitas vezes; "Erro ao carregar produtos da CobaiaAPI: HTTP 429"; pode vir retry_after. Causa: A CobaiaAPI não tem limitador (main.py só registra CORS e routers); um 429 vem de proxy, gateway ou servidor diferente do esperado.
```

**`fluxo-reserva-e-cancelamento`**

```text
[fluxo-reserva-e-cancelamento] Fluxo de reservar e cancelar
Reserva em cliente/registrar_reserva.php e cancelamento em reserva_cli.php; a API espelha em POST /api/pedidos e POST /api/pedidos/{id}/cancelar. Sinais: regra de data e quantidade só no navegador; reserva alheia cancelada sem checagem de dono. Causa: Data hoje+2 a hoje+90 e pessoas ≥ 1 são só min/max do HTML (registrar_reserva.php:28-35,55); cancelar grava 'Cancelado' (pedidos.py:75).
```

**`tempo_de_resposta_excedido`**

```text
[tempo_de_resposta_excedido] Tempo de resposta excedido
A resposta demora além do aceitável ou nunca chega: sem status (conexão encerrada) ou 200 tardio. 429 e 500 respondem rápido com um código — aqui não. Sinais: 200 correto com segundos de espera: atraso no servidor ou no caminho; sem status, "Failed to fetch": o cliente desistiu antes. Causa: O modo latency dorme 2 s fixos (fault_injection.py:66); atrasos maiores vêm de banco, rede ou carga; o fetch da página não tem tempo limite.
```

### Prompt

3177 caracteres em 7 partes (hash `5e78fe593b01f3da`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1014 tokens, saída de 71 (teto de 600); 18,2 s no total (220 ms lendo o prompt, 15844 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: limite_de_requisicoes
CAMPO: nenhum
IMPACTO: O usuário recebe um erro 429 indicando que excedeu o limite de requisições, sem que a reserva tenha sido efetivamente criada.
FONTE: [limite_de_requisicoes]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `limite_de_requisicoes` | caracteres 12 a 33 da resposta |
| CAMPO | `nenhum` | caracteres 41 a 47 da resposta |
| IMPACTO | `O usuário recebe um erro 429 indicando que excedeu o limite de requisições, sem que a reserva tenha sido efetivamente criada.` | caracteres 57 a 182 da resposta |
| FONTE | `[limite_de_requisicoes]` | caracteres 190 a 213 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `limite_de_requisicoes` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `limite_de_requisicoes` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `limite_de_requisicoes` | confere | contexto: `limite_de_requisicoes`, `fluxo-reserva-e-cancelamento`, `tempo_de_resposta_excedido` |
| O campo apontado aparece no caso | `nenhum` | não se aplica | o modelo não apontou campo |
| Algum verbete do contexto trata da causa respondida | `limite_de_requisicoes` | confere | verbetes: `limite_de_requisicoes`, `tempo_de_resposta_excedido` |
| Notas escritas pelo modelo nos verbetes citados | `limite_de_requisicoes` | informativo | `limite_de_requisicoes`: sem notas do modelo. A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário recebe um erro 429 indicando que excedeu o limite de requisições, sem que a reserva tenha sido efetivamente criada.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

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
| L0 | `limite_de_requisicoes` | `limite_de_requisicoes`, `fluxo-reserva-e-cancelamento`, `tempo_de_resposta_excedido` |
| L1 | `limite_de_requisicoes` | `limite_de_requisicoes`, `fluxo-reserva-e-cancelamento`, `tempo_de_resposta_excedido` |
| L3 | `limite_de_requisicoes` | `limite_de_requisicoes`, `tempo_de_resposta_excedido`, `fluxo-reserva-e-cancelamento` |

## Rastro

Gerado dos eventos 647 a 670 da trilha `fase3b_ineditos__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `190c716b20ee26b3`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
