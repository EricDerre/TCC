<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `run-1` pelo `qwen2.5-coder:3b` com a biblioteca L1

Trilha `fase3b_cruzada_qwen/qwen2.5-coder_3b/run-1@L1`. Corrida `fase3b_cruzada_qwen`, Ollama 0.34.4; classe 5, nível 1; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`erro_interno_do_servidor`, `mensagens-de-erro-do-codigo`, `pagina-produtos-api`); prompt de 1079 tokens; resposta de 50 tokens em 33,0 s |
| O que o modelo declarou | causa `erro_interno_do_servidor`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 5 de 5 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 500

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"detail": "erro interno (fault injection)"}

SINTOMA OBSERVADO: A aba de produtos via API mostra a mensagem de erro ao carregar.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/produtos`, entidade `Produto`, status `500`, 26 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `erro_interno_do_servidor` | 46,222 | 43,222 | 2,0 | 0,0 | 1,0 | entregue ao modelo |
| 2 | `mensagens-de-erro-do-codigo` | 30,460 | 29,460 | 0,0 | 0,0 | 1,0 | entregue ao modelo |
| 3 | `pagina-produtos-api` | 21,824 | 19,824 | 2,0 | 0,0 | 0,0 | entregue ao modelo |
| 4 | `contagem_inconsistente` | 21,490 | 18,490 | 2,0 | 1,0 | 0,0 | descartado |
| 5 | `estrutura_aninhada_divergente` | 20,144 | 17,144 | 2,0 | 1,0 | 0,0 | descartado |
| 6 | `modos-de-injecao` | 17,679 | 16,679 | 0,0 | 0,0 | 1,0 | descartado |

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

**`pagina-produtos-api`**

```text
[pagina-produtos-api] Aba "Produtos (API)", a fronteira JSON
produtos_api.php monta os cartões com fetch() em localhost:8000/api/produtos — a única fronteira JSON do cobaia; detalhe via GET /api/produtos/{id}. Sinais: "Carregando..." parado: o fetch nunca resolveu; "Nenhum produto retornado pela API.": não é lista, ou vazia. Causa: formatarPreco() usa Number(): preço não numérico sai cru; tipo objeto sai via JSON.stringify; botão button.saiba-mais[data-id].
```

### Prompt

3350 caracteres em 7 partes (hash `6427b8a01c726fa1`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1079 tokens, saída de 50 (teto de 600); 33,0 s no total (25476 ms lendo o prompt, 5363 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: erro_interno_do_servidor
CAMPO: nenhum
IMPACTO: A aba de produtos via API mostra a mensagem de erro ao carregar.
FONTE: [erro_interno_do_servidor]
```

## O que o modelo declarou

O `qwen2.5-coder:3b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `erro_interno_do_servidor` | caracteres 12 a 36 da resposta |
| CAMPO | `nenhum` | caracteres 44 a 50 da resposta |
| IMPACTO | `A aba de produtos via API mostra a mensagem de erro ao carregar.` | caracteres 60 a 124 da resposta |
| FONTE | `[erro_interno_do_servidor]` | caracteres 132 a 158 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `erro_interno_do_servidor` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `erro_interno_do_servidor` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `erro_interno_do_servidor` | confere | contexto: `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo`, `pagina-produtos-api` |
| O campo apontado aparece no caso | `nenhum` | não se aplica | o modelo não apontou campo |
| Algum verbete do contexto trata da causa respondida | `erro_interno_do_servidor` | confere | verbetes: `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo` |
| Notas escritas pelo modelo nos verbetes citados | `erro_interno_do_servidor` | informativo | `erro_interno_do_servidor`: 2 nota(s) do modelo (Correta: 2). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `A aba de produtos via API mostra a mensagem de erro ao carregar.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

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
| L1 | `erro_interno_do_servidor` | `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo`, `pagina-produtos-api` |
| L3 | `erro_interno_do_servidor` | `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo`, `pagina-produtos-api` |

## Rastro

Gerado dos eventos 229 a 253 da trilha `fase3b_cruzada_qwen__qwen2.5-coder_3b__L1.jsonl`; hash dos eventos deste caso: `ad234a04d0d008b4`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
