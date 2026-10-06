<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `run-19` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3b_ineditos/qwen2.5_7b/run-19@L1`. Corrida `fase3b_ineditos`, Ollama 0.34.1; classe 5, nível 2; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`tempo_de_resposta_excedido`, `pagina-produtos-api`, `registro_duplicado`); prompt de 1027 tokens; resposta de 74 tokens em 19,1 s |
| O que o modelo declarou | causa `tempo_de_resposta_excedido`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 5 de 5 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/1 (clique em 'Saiba Mais...')

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
(recebido apos 7,8 s)

SINTOMA OBSERVADO: O modal de detalhes demora quase 8 segundos pra abrir depois do clique; o mesmo clique respondia em menos de 200ms antes.

OBSERVAÇÃO ADICIONAL: fetch() nao tem timeout configurado em produtos_api.php; o modal so abre quando a Promise resolve, por mais que demore.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/produtos/{id}`, entidade `Produto`, status `200`, 40 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `tempo_de_resposta_excedido` | 30,354 | 29,354 | 0,0 | 0,0 | 1,0 | entregue ao modelo |
| 2 | `pagina-produtos-api` | 20,029 | 18,029 | 2,0 | 0,0 | 0,0 | entregue ao modelo |
| 3 | `registro_duplicado` | 18,535 | 18,535 | 0,0 | 0,0 | 0,0 | entregue ao modelo |
| 4 | `colecao_no_lugar_de_objeto` | 15,682 | 12,682 | 2,0 | 1,0 | 0,0 | descartado |
| 5 | `localizador_quebrado` | 15,510 | 15,510 | 0,0 | 0,0 | 0,0 | descartado |
| 6 | `codificacao_incorreta` | 15,300 | 15,300 | 0,0 | 0,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`tempo_de_resposta_excedido`**

```text
[tempo_de_resposta_excedido] Tempo de resposta excedido
A resposta demora além do aceitável ou nunca chega: sem status (conexão encerrada) ou 200 tardio. 429 e 500 respondem rápido com um código — aqui não. Sinais: 200 correto com segundos de espera: atraso no servidor ou no caminho; sem status, "Failed to fetch": o cliente desistiu antes. Causa: O modo latency dorme 2 s fixos (fault_injection.py:66); atrasos maiores vêm de banco, rede ou carga; o fetch da página não tem tempo limite.
```

**`pagina-produtos-api`**

```text
[pagina-produtos-api] Aba "Produtos (API)", a fronteira JSON
produtos_api.php monta os cartões com fetch() em localhost:8000/api/produtos — a única fronteira JSON do cobaia; detalhe via GET /api/produtos/{id}. Sinais: "Carregando..." parado: o fetch nunca resolveu; "Nenhum produto retornado pela API.": não é lista, ou vazia. Causa: formatarPreco() usa Number(): preço não numérico sai cru; tipo objeto sai via JSON.stringify; botão button.saiba-mais[data-id].
```

**`registro_duplicado`**

```text
[registro_duplicado] Registro duplicado
A mesma escrita gravada mais de uma vez: reservas iguais com ids consecutivos, duas respostas 201 para um único gesto. Sinais: registros idênticos exceto pelo id; dois POST com o mesmo corpo na sequência. Causa: POST /api/pedidos insere sem chave de idempotência (pedidos.py:46-66): clique duplo vira duas linhas. registrar_reserva.php insere a cada POST — recarregar após reservar reenvia o formulário.
```

### Prompt

3233 caracteres em 7 partes (hash `42e866b1d8b8e105`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1027 tokens, saída de 74 (teto de 600); 19,1 s no total (226 ms lendo o prompt, 16685 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: tempo_de_resposta_excedido
CAMPO: nenhum
IMPACTO: O usuário espera por cerca de 8 segundos para que o modal de detalhes abra, o que é significativamente mais demorado do que o tempo normal de resposta.
FONTE: [tempo_de_resposta_excedido]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `tempo_de_resposta_excedido` | caracteres 12 a 38 da resposta |
| CAMPO | `nenhum` | caracteres 46 a 52 da resposta |
| IMPACTO | `O usuário espera por cerca de 8 segundos para que o modal de detalhes abra, o que é significativamente mais demorado do que o tempo normal de resposta.` | caracteres 62 a 213 da resposta |
| FONTE | `[tempo_de_resposta_excedido]` | caracteres 221 a 249 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `tempo_de_resposta_excedido` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `tempo_de_resposta_excedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tempo_de_resposta_excedido` | confere | contexto: `tempo_de_resposta_excedido`, `pagina-produtos-api`, `registro_duplicado` |
| O campo apontado aparece no caso | `nenhum` | não se aplica | o modelo não apontou campo |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | confere | verbetes: `tempo_de_resposta_excedido` |
| Notas escritas pelo modelo nos verbetes citados | `tempo_de_resposta_excedido` | informativo | `tempo_de_resposta_excedido`: sem notas do modelo. A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário espera por cerca de 8 segundos para que o modal de detalhes abra, o que é significativamente mais demorado do que o tempo normal de resposta.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

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
| L0 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido`, `pagina-produtos-api`, `registro_duplicado` |
| L1 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido`, `pagina-produtos-api`, `registro_duplicado` |
| L3 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido`, `pagina-produtos-api`, `registro_duplicado` |

## Rastro

Gerado dos eventos 672 a 693 da trilha `fase3b_ineditos__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `d780bf7220cedc5e`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
