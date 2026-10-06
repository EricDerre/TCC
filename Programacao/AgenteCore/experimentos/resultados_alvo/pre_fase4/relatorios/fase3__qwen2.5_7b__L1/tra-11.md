<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `tra-11` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3/qwen2.5_7b/tra-11@L1`. Corrida `fase3`, Ollama 0.34.0; classe 4, nível 2; texto dos casos: anterior à correção de 28/09/2026. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`contagem_inconsistente`, `estrutura_aninhada_divergente`, `tempo_de_resposta_excedido`); prompt de 1163 tokens; resposta de 52 tokens em 76,2 s |
| O que o modelo declarou | causa `contagem_inconsistente`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 6 de 6 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos?pagina=2

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano | envelope: {total: inteiro, itens: lista}

CORPO DA RESPOSTA:
{"total": 14, "itens": []}

SINTOMA OBSERVADO: A segunda pagina da listagem aparece vazia, mesmo havendo 14 produtos.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/produtos`, entidade `Produto`, status `200`, 23 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `contagem_inconsistente` | 49,995 | 46,995 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `estrutura_aninhada_divergente` | 22,361 | 19,361 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `tempo_de_resposta_excedido` | 14,224 | 11,224 | 2,0 | 0,0 | 1,0 | entregue ao modelo |
| 4 | `dado_desatualizado` | 13,048 | 10,048 | 2,0 | 0,0 | 1,0 | descartado |
| 5 | `entidade-produto` | 12,322 | 9,322 | 2,0 | 1,0 | 0,0 | descartado |
| 6 | `escala_ou_unidade_errada` | 10,514 | 7,514 | 2,0 | 1,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`contagem_inconsistente`**

```text
[contagem_inconsistente] Contagem inconsistente
Dois números que deveriam bater não batem: total 14 e lista com 1; total 0 com itens; página 2 vazia com total 14; contador de destaques diferente dos cartões. Sinais: total e lista vêm de consultas diferentes; rótulo numérico que não corresponde ao renderizado. Causa: GET /api/produtos devolve a lista crua, sem total nem paginação (produtos.py:34-43); o seed tem 14 produtos, 5 em destaque. Envelope com total indica outra versão.
```

**`estrutura_aninhada_divergente`**

```text
[estrutura_aninhada_divergente] Estrutura aninhada divergente
Chaves existem, mas noutro nível: lista num envelope ({"data": {"itens": [...]}}) ou campo simples como objeto ({"id": 1, "nome": "Carnes"}). Sinais: envelope na raiz: Array.isArray falha, "Nenhum produto retornado"; campo como objeto: cartão imprime [object Object]. Causa: Contrato real: lista crua na raiz e tipo como texto (produtos.py _to_dict); envelope ou aninhamento veio de outra versão ou intermediário. Notas: Retificação: onde diz "Chaves existem, mas noutro nível: lista num envelope ({'data': {'itens': [...]}}) ou campo simples como objeto ({'id': 1, 'nome': 'Carnes'}).", leia: Adicionar exemplo de estrutura aninhada divergente no verbete. Retificação: onde diz "Chaves existem, mas noutro nível: lista num envelope ({'data': {'itens': [...]}}) ou campo simples como objeto ({'id': 1, 'nome': 'Carnes'}).", leia: Corrigir a estrutura da resposta da API para ser consistente, evitando envelopes ou campos simples aninhados, para padronizar o desenpacotamento dos dados.
```

**`tempo_de_resposta_excedido`**

```text
[tempo_de_resposta_excedido] Tempo de resposta excedido
A resposta demora além do aceitável ou nunca chega: sem status (conexão encerrada) ou 200 tardio. 429 e 500 respondem rápido com um código — aqui não. Sinais: 200 correto com segundos de espera: atraso no servidor ou no caminho; sem status, "Failed to fetch": o cliente desistiu antes. Causa: O modo latency dorme 2 s fixos (fault_injection.py:66); atrasos maiores vêm de banco, rede ou carga; o fetch da página não tem tempo limite.
```

### Prompt

3690 caracteres em 7 partes (hash `b5ce3ac941bcb137`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1163 tokens, saída de 52 (teto de 600); 76,2 s no total (62450 ms lendo o prompt, 11620 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: contagem_inconsistente
CAMPO: itens
IMPACTO: O usuário vê uma segunda página vazia, enquanto espera por 14 itens.
FONTE: [contagem_inconsistente]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `contagem_inconsistente` | caracteres 12 a 34 da resposta |
| CAMPO | `itens` | caracteres 42 a 47 da resposta |
| IMPACTO | `O usuário vê uma segunda página vazia, enquanto espera por 14 itens.` | caracteres 57 a 125 da resposta |
| FONTE | `[contagem_inconsistente]` | caracteres 133 a 157 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `contagem_inconsistente` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `contagem_inconsistente`, `estrutura_aninhada_divergente`, `tempo_de_resposta_excedido` |
| O campo apontado aparece no caso | `itens` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | confere | verbetes: `contagem_inconsistente`, `estrutura_aninhada_divergente` |
| Notas escritas pelo modelo nos verbetes citados | `contagem_inconsistente` | informativo | `contagem_inconsistente`: sem notas do modelo. A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário vê uma segunda página vazia, enquanto espera por 14 itens.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `contagem_inconsistente` | `contagem_inconsistente` | confere |
| O campo respondido é o esperado | `itens` |  | **não confere** |
| O verbete da causa esperada estava no contexto | `contagem_inconsistente` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `contagem_inconsistente` | `contagem_inconsistente`, `estrutura_aninhada_divergente`, `tempo_de_resposta_excedido` |
| L1 | `contagem_inconsistente` | `contagem_inconsistente`, `estrutura_aninhada_divergente`, `tempo_de_resposta_excedido` |
| L2 | `contagem_inconsistente` | `contagem_inconsistente`, `estrutura_aninhada_divergente`, `tempo_de_resposta_excedido` |
| L3 | `contagem_inconsistente` | `contagem_inconsistente`, `estrutura_aninhada_divergente`, `tempo_de_resposta_excedido` |

## Rastro

Gerado dos eventos 1773 a 1794 da trilha `fase3__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `e2a5aa6cf7db273c`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
