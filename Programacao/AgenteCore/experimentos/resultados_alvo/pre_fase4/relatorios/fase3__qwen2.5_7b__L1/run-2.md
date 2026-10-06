<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `run-2` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3/qwen2.5_7b/run-2@L1`. Corrida `fase3`, Ollama 0.34.0; classe 5, nível 1; texto dos casos: anterior à correção de 28/09/2026. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`tempo_de_resposta_excedido`, `limite_de_requisicoes`, `estado_da_tela_divergente`); prompt de 1135 tokens; resposta de 64 tokens em 54,4 s |
| O que o modelo declarou | causa `tempo_de_resposta_excedido`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 5 de 5 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
(sem resposta apos 30s; conexao encerrada pelo cliente)

SINTOMA OBSERVADO: A pagina fica carregando e depois exibe erro de rede.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/produtos`, entidade `Produto`, status `None`, 21 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `tempo_de_resposta_excedido` | 33,017 | 31,017 | 2,0 | 0,0 | 0,0 | entregue ao modelo |
| 2 | `limite_de_requisicoes` | 15,534 | 13,534 | 2,0 | 0,0 | 0,0 | entregue ao modelo |
| 3 | `estado_da_tela_divergente` | 12,470 | 12,470 | 0,0 | 0,0 | 0,0 | entregue ao modelo |
| 4 | `corpo_nao_e_json` | 12,321 | 12,321 | 0,0 | 0,0 | 0,0 | descartado |
| 5 | `limites-do-sistema` | 11,484 | 11,484 | 0,0 | 0,0 | 0,0 | descartado |
| 6 | `corpo_vazio` | 10,607 | 10,607 | 0,0 | 0,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`tempo_de_resposta_excedido`**

```text
[tempo_de_resposta_excedido] Tempo de resposta excedido
A resposta demora além do aceitável ou nunca chega: sem status (conexão encerrada) ou 200 tardio. 429 e 500 respondem rápido com um código — aqui não. Sinais: 200 correto com segundos de espera: atraso no servidor ou no caminho; sem status, "Failed to fetch": o cliente desistiu antes. Causa: O modo latency dorme 2 s fixos (fault_injection.py:66); atrasos maiores vêm de banco, rede ou carga; o fetch da página não tem tempo limite.
```

**`limite_de_requisicoes`**

```text
[limite_de_requisicoes] Limite de requisições (429)
Status 429: o servidor ou um intermediário recusou por excesso de requisições num intervalo. Resposta rápida e com corpo — não é lentidão nem erro interno. Sinais: funciona, depois falha após recarregar muitas vezes; "Erro ao carregar produtos da CobaiaAPI: HTTP 429"; pode vir retry_after. Causa: A CobaiaAPI não tem limitador (main.py só registra CORS e routers); um 429 vem de proxy, gateway ou servidor diferente do esperado.
```

**`estado_da_tela_divergente`**

```text
[estado_da_tela_divergente] Estado da tela divergente da resposta
A rede está certa — status e corpo conferem — e o usuário vê outra coisa: "Carregando" parado, lista vazia, botão que não muda. Sinais: nenhum erro de console nem status de erro; recarregar corrige: o estado não foi atualizado. Causa: produtos_api.php só limpa "Carregando..." no then() do fetch e substitui o grid por innerHTML; na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7). Notas: Retificação: onde diz "na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7).", leia: Corrigir a lógica de cancelamento para não depender de redirect, garantindo a atualização do estado da tela. Retificação: onde diz "na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7).", leia: Corrigir a implementação do cancelamento para que não dependa apenas do redirect, mas também limpe o estado da tela corretamente. Retificação: onde diz "na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7).", leia: Corrigir a lógica de cancelamento para não depender do redirect, garantindo que a interface seja atualizada corretamente.
```

### Prompt

3741 caracteres em 7 partes (hash `bd68f7cdd45b2d23`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1135 tokens, saída de 64 (teto de 600); 54,4 s no total (37698 ms lendo o prompt, 14298 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: tempo_de_resposta_excedido
CAMPO: nenhum
IMPACTO: A página fica carregando e depois exibe erro de rede, pois o cliente desistiu antes da resposta chegar.
FONTE: [tempo_de_resposta_excedido]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `tempo_de_resposta_excedido` | caracteres 12 a 38 da resposta |
| CAMPO | `nenhum` | caracteres 46 a 52 da resposta |
| IMPACTO | `A página fica carregando e depois exibe erro de rede, pois o cliente desistiu antes da resposta chegar.` | caracteres 62 a 165 da resposta |
| FONTE | `[tempo_de_resposta_excedido]` | caracteres 173 a 201 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `tempo_de_resposta_excedido` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `tempo_de_resposta_excedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tempo_de_resposta_excedido` | confere | contexto: `tempo_de_resposta_excedido`, `limite_de_requisicoes`, `estado_da_tela_divergente` |
| O campo apontado aparece no caso | `nenhum` | não se aplica | o modelo não apontou campo |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | confere | verbetes: `tempo_de_resposta_excedido`, `limite_de_requisicoes` |
| Notas escritas pelo modelo nos verbetes citados | `tempo_de_resposta_excedido` | informativo | `tempo_de_resposta_excedido`: sem notas do modelo. A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `A página fica carregando e depois exibe erro de rede, pois o cliente desistiu antes da resposta chegar.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | confere |
| O campo respondido é o esperado | `nenhum` |  | confere |
| O verbete da causa esperada estava no contexto | `tempo_de_resposta_excedido` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido`, `limite_de_requisicoes`, `estado_da_tela_divergente` |
| L1 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido`, `limite_de_requisicoes`, `estado_da_tela_divergente` |
| L2 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido`, `limite_de_requisicoes`, `estado_da_tela_divergente` |
| L3 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido`, `limite_de_requisicoes`, `estado_da_tela_divergente` |

## Rastro

Gerado dos eventos 616 a 638 da trilha `fase3__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `726320ed32a95207`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
