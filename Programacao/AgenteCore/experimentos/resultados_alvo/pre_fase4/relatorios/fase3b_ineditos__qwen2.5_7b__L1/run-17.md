<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `run-17` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3b_ineditos/qwen2.5_7b/run-17@L1`. Corrida `fase3b_ineditos`, Ollama 0.34.1; classe 5, nível 1; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`erro_interno_do_servidor`, `mensagens-de-erro-do-codigo`, `modos-de-injecao`); prompt de 1118 tokens; resposta de 55 tokens em 75,5 s |
| O que o modelo declarou | causa `erro_interno_do_servidor`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 5 de 5 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: POST /api/pedidos/7/cancelar

STATUS HTTP: 500

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
{"detail": "erro interno (fault injection) em pedido"}

SINTOMA OBSERVADO: Cancelar a reserva 7 devolve 500; nao da pra saber pela resposta se o status mudou no banco ou nao.
```

### Busca na biblioteca

Consulta montada em código: endpoint `POST /api/pedidos/{id}/cancelar`, entidade `Pedido`, status `500`, 30 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `erro_interno_do_servidor` | 47,444 | 46,444 | 0,0 | 0,0 | 1,0 | entregue ao modelo |
| 2 | `mensagens-de-erro-do-codigo` | 27,519 | 26,519 | 0,0 | 0,0 | 1,0 | entregue ao modelo |
| 3 | `modos-de-injecao` | 24,671 | 23,671 | 0,0 | 0,0 | 1,0 | entregue ao modelo |
| 4 | `tempo_de_resposta_excedido` | 20,265 | 19,265 | 0,0 | 0,0 | 1,0 | descartado |
| 5 | `fluxo-reserva-e-cancelamento` | 19,330 | 16,330 | 2,0 | 1,0 | 0,0 | descartado |
| 6 | `contrato-pedido` | 17,736 | 14,736 | 2,0 | 1,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`erro_interno_do_servidor`**

```text
[erro_interno_do_servidor] Erro interno do servidor (500)
500 com {"detail": ...}: falha própria da API. detail "fault injection: error_500 em produto" é o injetor; "Internal Server Error" é exceção não tratada. Sinais: intermitente sem padrão: injetor com probability < 1; em toda requisição: banco inacessível ou defeito na rota. Causa: Rotas convertem ErrorFault em 500 (produtos.py:42). No site PHP, banco fora NÃO dá 500: imprime "Atenção ERRO" em HTML (connect.php:16). Notas: Adicionar que este erro pode ocorrer devido a falhas no banco de dados ou em rotas, e que a mensagem genérica pode esconder problemas específicos. Adicionar que este erro pode ocorrer de forma intermitente, sem padrão, e que pode ser causado por problemas no banco de dados ou rota.
```

**`mensagens-de-erro-do-codigo`**

```text
[mensagens-de-erro-do-codigo] Índice de mensagens literais do código
Página: "Carregando produtos da CobaiaAPI..."; "Nenhum produto retornado pela API." (não é lista, ou vazia); "Erro ao carregar produtos da CobaiaAPI: <msg>" ("HTTP <n>" se resp.ok falso). API: "produto/cliente/pedido não encontrado" (404), "token inválido" (403), "modo inválido" (400), "fault injection: error_500 em <ent>" (500). PHP: "Atenção ERRO: ..." (connect.php:16), "falha no email" (rodape_contato_envia.php:33).
```

**`modos-de-injecao`**

```text
[modos-de-injecao] Injeção de falhas da CobaiaAPI
Injetor com 7 modos: error_500, latency (2 s), type_drift (campo-alvo vira texto), field_missing (remove), field_renamed (vira <campo>_v2), malformed_json (corpo cortado) e normal. Sinais: só um campo alterado, resto íntegro: modo com campo-alvo; detail "fault injection: error_500 em produto". Causa: Ligado por FAULT_MODE/FAULT_TARGET_FIELD no .env ou POST /api/admin/fault-mode com X-Admin-Token; probability < 1 dá intermitência.
```

### Prompt

3457 caracteres em 7 partes (hash `285239a5efd09ea6`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1118 tokens, saída de 55 (teto de 600); 75,5 s no total (60963 ms lendo o prompt, 12363 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: erro_interno_do_servidor
CAMPO: nenhum
IMPACTO: O usuário não recebe informações específicas sobre o status do pedido, apenas um erro genérico.
FONTE: [erro_interno_do_servidor]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `erro_interno_do_servidor` | caracteres 12 a 36 da resposta |
| CAMPO | `nenhum` | caracteres 44 a 50 da resposta |
| IMPACTO | `O usuário não recebe informações específicas sobre o status do pedido, apenas um erro genérico.` | caracteres 60 a 155 da resposta |
| FONTE | `[erro_interno_do_servidor]` | caracteres 163 a 189 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `erro_interno_do_servidor` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `erro_interno_do_servidor` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `erro_interno_do_servidor` | confere | contexto: `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo`, `modos-de-injecao` |
| O campo apontado aparece no caso | `nenhum` | não se aplica | o modelo não apontou campo |
| Algum verbete do contexto trata da causa respondida | `erro_interno_do_servidor` | confere | verbetes: `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo`, `modos-de-injecao` |
| Notas escritas pelo modelo nos verbetes citados | `erro_interno_do_servidor` | informativo | `erro_interno_do_servidor`: 2 nota(s) do modelo (Correta: 2). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário não recebe informações específicas sobre o status do pedido, apenas um erro genérico.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `erro_interno_do_servidor` | `erro_interno_do_servidor` | confere |
| O campo respondido é o esperado | `nenhum` |  | confere |
| O verbete da causa esperada estava no contexto | `erro_interno_do_servidor` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `erro_interno_do_servidor` | `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo`, `modos-de-injecao` |
| L1 | `erro_interno_do_servidor` | `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo`, `modos-de-injecao` |
| L3 | `erro_interno_do_servidor` | `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo`, `modos-de-injecao` |

## Rastro

Gerado dos eventos 623 a 645 da trilha `fase3b_ineditos__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `d50170149e848cf9`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
