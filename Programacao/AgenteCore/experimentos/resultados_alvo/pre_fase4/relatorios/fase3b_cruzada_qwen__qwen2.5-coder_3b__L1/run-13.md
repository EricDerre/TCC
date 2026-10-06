<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `run-13` pelo `qwen2.5-coder:3b` com a biblioteca L1

Trilha `fase3b_cruzada_qwen/qwen2.5-coder_3b/run-13@L1`. Corrida `fase3b_cruzada_qwen`, Ollama 0.34.4; classe 5, nível 3; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`registro_duplicado`, `contrato-pedido`, `codificacao_incorreta`); prompt de 976 tokens; resposta de 56 tokens em 30,4 s |
| O que o modelo declarou | causa `registro_duplicado`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 5 de 5 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: POST /api/pedidos (clique duplo no botao)

STATUS HTTP: 201

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
Duas respostas 201, com id_pedido 8 e 9, mesmos dados.

SINTOMA OBSERVADO: O cliente reclama de cobranca em duplicidade da mesma reserva.
```

### Busca na biblioteca

Consulta montada em código: endpoint `POST /api/pedidos`, entidade `Pedido`, status `201`, 21 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `registro_duplicado` | 44,213 | 40,213 | 2,0 | 1,0 | 1,0 | entregue ao modelo |
| 2 | `contrato-pedido` | 21,865 | 17,865 | 2,0 | 1,0 | 1,0 | entregue ao modelo |
| 3 | `codificacao_incorreta` | 11,602 | 11,602 | 0,0 | 0,0 | 0,0 | entregue ao modelo |
| 4 | `fluxo-reserva-e-cancelamento` | 9,932 | 6,932 | 2,0 | 1,0 | 0,0 | descartado |
| 5 | `pedido-reserva` | 8,750 | 7,750 | 0,0 | 1,0 | 0,0 | descartado |
| 6 | `recurso_inexistente` | 7,782 | 5,782 | 2,0 | 0,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`registro_duplicado`**

```text
[registro_duplicado] Registro duplicado
A mesma escrita gravada mais de uma vez: reservas iguais com ids consecutivos, duas respostas 201 para um único gesto. Sinais: registros idênticos exceto pelo id; dois POST com o mesmo corpo na sequência. Causa: POST /api/pedidos insere sem chave de idempotência (pedidos.py:46-66): clique duplo vira duas linhas. registrar_reserva.php insere a cada POST — recarregar após reservar reenvia o formulário.
```

**`contrato-pedido`**

```text
[contrato-pedido] Contrato de /api/pedidos
GET /api/pedidos?login=<cpf>; POST /api/pedidos {id_clientes, pessoas, data_pedido} → 201; POST /api/pedidos/{id}/cancelar. Campos: id_pedido, pessoas, data_pedido AAAA-MM-DD, status 'Em Análise'|'Cancelado', nome, cpf. Sinais: data noutro formato ou como número; status fora dos dois valores. Causa: cpf vem de login_usuario (pedidos.py). Busca exata na API; o site usa LIKE '%login%' (cliente/index.php:4).
```

**`codificacao_incorreta`**

```text
[codificacao_incorreta] Codificação de caracteres incorreta
JSON válido e estrutura certa, mas textos com acento corrompidos: bytes latin-1 declarados utf-8, ou utf-8 convertido duas vezes ("Pão" vira "PÃ£o"). Sinais: só campos de texto livre afetados; números e chaves intactos; parte dos registros certa e parte errada: conversão dupla parcial. Causa: Banco e conexões em utf8 (connect.php:7, config.py); se corrompe, o dado foi gravado errado ou um intermediário reconverteu.
```

### Prompt

3066 caracteres em 7 partes (hash `aa1e2459a495da42`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 976 tokens, saída de 56 (teto de 600); 30,4 s no total (22417 ms lendo o prompt, 5821 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: registro_duplicado
CAMPO: nenhum
IMPACTO: O cliente vê duas cobranças para a mesma reserva, causando confusão e possíveis problemas financeiros.
FONTE: [registro_duplicado]
```

## O que o modelo declarou

O `qwen2.5-coder:3b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `registro_duplicado` | caracteres 12 a 30 da resposta |
| CAMPO | `nenhum` | caracteres 38 a 44 da resposta |
| IMPACTO | `O cliente vê duas cobranças para a mesma reserva, causando confusão e possíveis problemas financeiros.` | caracteres 54 a 156 da resposta |
| FONTE | `[registro_duplicado]` | caracteres 164 a 184 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `registro_duplicado` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `registro_duplicado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `registro_duplicado` | confere | contexto: `registro_duplicado`, `contrato-pedido`, `codificacao_incorreta` |
| O campo apontado aparece no caso | `nenhum` | não se aplica | o modelo não apontou campo |
| Algum verbete do contexto trata da causa respondida | `registro_duplicado` | confere | verbetes: `registro_duplicado` |
| Notas escritas pelo modelo nos verbetes citados | `registro_duplicado` | informativo | `registro_duplicado`: sem notas do modelo. A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O cliente vê duas cobranças para a mesma reserva, causando confusão e possíveis problemas financeiros.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `registro_duplicado` | `registro_duplicado` | confere |
| O campo respondido é o esperado | `nenhum` |  | confere |
| O verbete da causa esperada estava no contexto | `registro_duplicado` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L1 | `registro_duplicado` | `registro_duplicado`, `contrato-pedido`, `codificacao_incorreta` |
| L3 | `registro_duplicado` | `registro_duplicado`, `contrato-pedido`, `codificacao_incorreta` |

## Rastro

Gerado dos eventos 797 a 819 da trilha `fase3b_cruzada_qwen__qwen2.5-coder_3b__L1.jsonl`; hash dos eventos deste caso: `e042f05e7c844d51`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
