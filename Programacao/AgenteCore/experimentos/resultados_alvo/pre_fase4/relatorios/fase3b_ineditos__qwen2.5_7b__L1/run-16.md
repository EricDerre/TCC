<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `run-16` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3b_ineditos/qwen2.5_7b/run-16@L1`. Corrida `fase3b_ineditos`, Ollama 0.34.1; classe 5, nível 1; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`recurso_inexistente`, `contrato-pedido`, `mensagens-de-erro-do-codigo`); prompt de 1098 tokens; resposta de 64 tokens em 76,0 s |
| O que o modelo declarou | causa `recurso_inexistente`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 6 de 6 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=55566677788

STATUS HTTP: 404

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
{"detail": "cliente nao encontrado"}

SINTOMA OBSERVADO: Consultar as reservas de um cpf que nunca fez cadastro (55566677788) devolve 404; a mensagem indica cliente nao encontrado, nao uma lista vazia de reservas.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/pedidos`, entidade `Pedido`, status `404`, 39 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `recurso_inexistente` | 55,811 | 52,811 | 2,0 | 0,0 | 1,0 | entregue ao modelo |
| 2 | `contrato-pedido` | 35,465 | 31,465 | 2,0 | 1,0 | 1,0 | entregue ao modelo |
| 3 | `mensagens-de-erro-do-codigo` | 26,944 | 25,944 | 0,0 | 0,0 | 1,0 | entregue ao modelo |
| 4 | `contagem_inconsistente` | 26,568 | 26,568 | 0,0 | 0,0 | 0,0 | descartado |
| 5 | `contrato-produto` | 23,375 | 22,375 | 0,0 | 0,0 | 1,0 | descartado |
| 6 | `rotas-inexistentes` | 20,107 | 19,107 | 0,0 | 0,0 | 1,0 | descartado |

### Documentação entregue ao modelo

**`recurso_inexistente`**

```text
[recurso_inexistente] Recurso inexistente (404 e vizinhos)
404: id ou rota inexistente. O detail diz qual: "produto não encontrado" (produtos.py:52), "cliente não encontrado" (pedidos.py:37,52), "pedido não encontrado" (pedidos.py:74); "Not Found" genérico é rota inexistente (ex.: /api/produto). Sinais: id válido e ainda 404: campo de busca errado (login × id); vizinhos: 403 no admin sem token; 422 sem login. Causa: Cada 404 com mensagem vem de db.get/filter vazio na rota. Notas: Adicionar um exemplo de campo de busca errado, como login × id, para ilustrar melhor a causa raiz.
```

**`contrato-pedido`**

```text
[contrato-pedido] Contrato de /api/pedidos
GET /api/pedidos?login=<cpf>; POST /api/pedidos {id_clientes, pessoas, data_pedido} → 201; POST /api/pedidos/{id}/cancelar. Campos: id_pedido, pessoas, data_pedido AAAA-MM-DD, status 'Em Análise'|'Cancelado', nome, cpf. Sinais: data noutro formato ou como número; status fora dos dois valores. Causa: cpf vem de login_usuario (pedidos.py). Busca exata na API; o site usa LIKE '%login%' (cliente/index.php:4).
```

**`mensagens-de-erro-do-codigo`**

```text
[mensagens-de-erro-do-codigo] Índice de mensagens literais do código
Página: "Carregando produtos da CobaiaAPI..."; "Nenhum produto retornado pela API." (não é lista, ou vazia); "Erro ao carregar produtos da CobaiaAPI: <msg>" ("HTTP <n>" se resp.ok falso). API: "produto/cliente/pedido não encontrado" (404), "token inválido" (403), "modo inválido" (400), "fault injection: error_500 em <ent>" (500). PHP: "Atenção ERRO: ..." (connect.php:16), "falha no email" (rodape_contato_envia.php:33).
```

### Prompt

3288 caracteres em 7 partes (hash `e6ec9af0f6475312`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1098 tokens, saída de 64 (teto de 600); 76,0 s no total (59489 ms lendo o prompt, 14405 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: recurso_inexistente
CAMPO: cpf
IMPACTO: O usuário recebe uma mensagem de erro 404 indicando que o cliente não foi encontrado, ao invés de uma lista vazia de pedidos.
FONTE: [recurso_inexistente]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `recurso_inexistente` | caracteres 12 a 31 da resposta |
| CAMPO | `cpf` | caracteres 39 a 42 da resposta |
| IMPACTO | `O usuário recebe uma mensagem de erro 404 indicando que o cliente não foi encontrado, ao invés de uma lista vazia de pedidos.` | caracteres 52 a 177 da resposta |
| FONTE | `[recurso_inexistente]` | caracteres 185 a 206 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `recurso_inexistente` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `recurso_inexistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `recurso_inexistente` | confere | contexto: `recurso_inexistente`, `contrato-pedido`, `mensagens-de-erro-do-codigo` |
| O campo apontado aparece no caso | `cpf` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `recurso_inexistente` | confere | verbetes: `recurso_inexistente`, `contrato-pedido`, `mensagens-de-erro-do-codigo` |
| Notas escritas pelo modelo nos verbetes citados | `recurso_inexistente` | informativo | `recurso_inexistente`: 1 nota(s) do modelo (Correta: 1). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário recebe uma mensagem de erro 404 indicando que o cliente não foi encontrado, ao invés de uma lista vazia de pedidos.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `recurso_inexistente` | `recurso_inexistente` | confere |
| O campo respondido é o esperado | `cpf` |  | **não confere** |
| O verbete da causa esperada estava no contexto | `recurso_inexistente` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `recurso_inexistente` | `recurso_inexistente`, `contrato-pedido`, `mensagens-de-erro-do-codigo` |
| L1 | `recurso_inexistente` | `recurso_inexistente`, `contrato-pedido`, `mensagens-de-erro-do-codigo` |
| L3 | `recurso_inexistente` | `recurso_inexistente`, `contrato-pedido`, `mensagens-de-erro-do-codigo` |

## Rastro

Gerado dos eventos 598 a 621 da trilha `fase3b_ineditos__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `8cb23f9eb1fa970d`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
