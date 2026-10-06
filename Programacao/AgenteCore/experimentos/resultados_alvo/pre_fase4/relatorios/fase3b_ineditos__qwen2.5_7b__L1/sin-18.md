<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `sin-18` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3b_ineditos/qwen2.5_7b/sin-18@L1`. Corrida `fase3b_ineditos`, Ollama 0.34.1; classe 2, nível 2; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`contrato-pedido`, `pedido-reserva`, `estrutura_aninhada_divergente`); prompt de 1417 tokens; resposta de 58 tokens em 68,4 s |
| O que o modelo declarou | causa `estrutura_aninhada_divergente`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 6 de 6 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": {"codigo": "EA", "descricao": "Em Analise"}, "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: O campo status de cada reserva chega como objeto ({'codigo': ..., 'descricao': ...}) em vez do texto simples que o contrato descreve; comparar direto com 'Em Analise'/'Cancelado' nunca bate.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/pedidos`, entidade `Pedido`, status `200`, 49 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `contrato-pedido` | 47,335 | 44,335 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `pedido-reserva` | 35,745 | 32,745 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `estrutura_aninhada_divergente` | 28,767 | 28,767 | 0,0 | 0,0 | 0,0 | entregue ao modelo |
| 4 | `campo_renomeado` | 28,159 | 26,159 | 2,0 | 0,0 | 0,0 | descartado |
| 5 | `valor_fora_do_dominio` | 26,129 | 23,129 | 2,0 | 1,0 | 0,0 | descartado |
| 6 | `colecao_no_lugar_de_objeto` | 22,591 | 22,591 | 0,0 | 0,0 | 0,0 | descartado |

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

**`estrutura_aninhada_divergente`**

```text
[estrutura_aninhada_divergente] Estrutura aninhada divergente
Chaves existem, mas noutro nível: lista num envelope ({"data": {"itens": [...]}}) ou campo simples como objeto ({"id": 1, "nome": "Carnes"}). Sinais: envelope na raiz: Array.isArray falha, "Nenhum produto retornado"; campo como objeto: cartão imprime [object Object]. Causa: Contrato real: lista crua na raiz e tipo como texto (produtos.py _to_dict); envelope ou aninhamento veio de outra versão ou intermediário. Notas: Retificação: onde diz "Chaves existem, mas noutro nível: lista num envelope ({'data': {'itens': [...]}}) ou campo simples como objeto ({'id': 1, 'nome': 'Carnes'}).", leia: Adicionar exemplo de estrutura aninhada divergente no verbete. Retificação: onde diz "Chaves existem, mas noutro nível: lista num envelope ({'data': {'itens': [...]}}) ou campo simples como objeto ({'id': 1, 'nome': 'Carnes'}).", leia: Corrigir a estrutura da resposta da API para ser consistente, evitando envelopes ou campos simples aninhados, para padronizar o desenpacotamento dos dados.
```

### Prompt

4570 caracteres em 7 partes (hash `57825348f30aa00c`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1417 tokens, saída de 58 (teto de 600); 68,4 s no total (52753 ms lendo o prompt, 13540 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: estrutura_aninhada_divergente
CAMPO: status
IMPACTO: O usuário vê o status como um objeto em vez de um texto simples, o que causa confusão na interface.
FONTE: [pedido-reserva]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `estrutura_aninhada_divergente` | caracteres 12 a 41 da resposta |
| CAMPO | `status` | caracteres 49 a 55 da resposta |
| IMPACTO | `O usuário vê o status como um objeto em vez de um texto simples, o que causa confusão na interface.` | caracteres 65 a 164 da resposta |
| FONTE | `[pedido-reserva]` | caracteres 172 a 188 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `estrutura_aninhada_divergente` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `pedido-reserva` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `pedido-reserva` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `estrutura_aninhada_divergente` |
| O campo apontado aparece no caso | `status` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `estrutura_aninhada_divergente` | confere | verbetes: `estrutura_aninhada_divergente` |
| Notas escritas pelo modelo nos verbetes citados | `pedido-reserva` | informativo | `pedido-reserva`: 3 nota(s) do modelo (Errada: 3). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário vê o status como um objeto em vez de um texto simples, o que causa confusão na interface.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | confere |
| O campo respondido é o esperado | `status` | `status` | confere |
| O verbete da causa esperada estava no contexto | `estrutura_aninhada_divergente` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `estrutura_aninhada_divergente` | `contrato-pedido`, `pedido-reserva`, `estrutura_aninhada_divergente` |
| L1 | `estrutura_aninhada_divergente` | `contrato-pedido`, `pedido-reserva`, `estrutura_aninhada_divergente` |
| L3 | `estrutura_aninhada_divergente` | `contrato-pedido`, `pedido-reserva`, `campo_renomeado` |

## Rastro

Gerado dos eventos 208 a 230 da trilha `fase3b_ineditos__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `bf1562fac212a7d8`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
