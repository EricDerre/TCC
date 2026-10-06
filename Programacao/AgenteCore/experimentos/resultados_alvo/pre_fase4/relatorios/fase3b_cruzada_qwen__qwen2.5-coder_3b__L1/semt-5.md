<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `semt-5` pelo `qwen2.5-coder:3b` com a biblioteca L1

Trilha `fase3b_cruzada_qwen/qwen2.5-coder_3b/semt-5@L1`. Corrida `fase3b_cruzada_qwen`, Ollama 0.34.4; classe 3, nível 3; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`contrato-pedido`, `nulo_inesperado`, `usuario-e-login`); prompt de 1034 tokens; resposta de 65 tokens em 29,2 s |
| O que o modelo declarou | causa `nulo_inesperado`; 2 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 8 de 8 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": null, "cpf": "11122233344"}]

SINTOMA OBSERVADO: A saudacao da area do cliente mostra 'Ola, !' — o restante da pagina carrega.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/pedidos`, entidade `Pedido`, status `200`, 31 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `contrato-pedido` | 37,795 | 34,795 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `nulo_inesperado` | 36,381 | 33,381 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `usuario-e-login` | 28,149 | 28,149 | 0,0 | 0,0 | 0,0 | entregue ao modelo |
| 4 | `pedido-reserva` | 21,964 | 18,964 | 2,0 | 1,0 | 0,0 | descartado |
| 5 | `chave_de_juncao_errada` | 20,213 | 17,213 | 2,0 | 1,0 | 0,0 | descartado |
| 6 | `formato_de_data_divergente` | 18,354 | 15,354 | 2,0 | 1,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`contrato-pedido`**

```text
[contrato-pedido] Contrato de /api/pedidos
GET /api/pedidos?login=<cpf>; POST /api/pedidos {id_clientes, pessoas, data_pedido} → 201; POST /api/pedidos/{id}/cancelar. Campos: id_pedido, pessoas, data_pedido AAAA-MM-DD, status 'Em Análise'|'Cancelado', nome, cpf. Sinais: data noutro formato ou como número; status fora dos dois valores. Causa: cpf vem de login_usuario (pedidos.py). Busca exata na API; o site usa LIKE '%login%' (cliente/index.php:4).
```

**`nulo_inesperado`**

```text
[nulo_inesperado] Nulo inesperado
A chave existe e vem null onde o contrato promete valor. Diferente de campo_ausente: a chave está lá. Sinais: nome nulo: "Olá, !" na área do cliente; preco nulo: cartão sem valor; tipo nulo: produto some de filtros por categoria. Causa: Origens legítimas: resumo, valor_produto e imagem_produto são nullable (models.py:33-35) e vw_tbpedidos faz LEFT JOIN. tipo nulo não sai de produtos.py (p.tipo.rotulo_tipo).
```

**`usuario-e-login`**

```text
[usuario-e-login] Usuário, níveis e login
Conta em tbusuarios: login_usuario, senha_usuario, nivel_usuario ('sup' admin, 'cli' cliente). Para o cliente o login é o CPF, que vira o campo cpf da API. Sinais: nome ou cpf de outra pessoa na reserva: junção por id trocada; saudação "Olá, !" sem nome: nome nulo vindo da view. Causa: login.php:7 compara a senha em texto puro; 'sup' abre o painel, 'cli' abre cliente/index.php?cliente=<login>, falha vai a invasor.php.
```

### Prompt

3127 caracteres em 7 partes (hash `3e34cd34b809491c`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1034 tokens, saída de 65 (teto de 600); 29,2 s no total (20100 ms lendo o prompt, 7013 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: nulo_inesperado
CAMPO: nome
IMPACTO: A saudação da área do cliente mostra 'Ola, !' porque o campo "nome" está nulo na resposta.
FONTE: [contrato-pedido], [nulo_inesperado]
```

## O que o modelo declarou

O `qwen2.5-coder:3b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `nulo_inesperado` | caracteres 12 a 27 da resposta |
| CAMPO | `nome` | caracteres 35 a 39 da resposta |
| IMPACTO | `A saudação da área do cliente mostra 'Ola, !' porque o campo "nome" está nulo na resposta.` | caracteres 49 a 139 da resposta |
| FONTE | `[contrato-pedido], [nulo_inesperado]` | caracteres 147 a 183 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `nulo_inesperado` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `contrato-pedido` | confere |  |
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-pedido` | confere | contexto: `contrato-pedido`, `nulo_inesperado`, `usuario-e-login` |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `contrato-pedido`, `nulo_inesperado`, `usuario-e-login` |
| O campo apontado aparece no caso | `nome` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `nulo_inesperado`, `usuario-e-login` |
| Notas escritas pelo modelo nos verbetes citados | `contrato-pedido`, `nulo_inesperado` | informativo | `contrato-pedido`: sem notas do modelo; `nulo_inesperado`: sem notas do modelo. A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `A saudação da área do cliente mostra 'Ola, !' porque o campo "nome" está nulo na resposta.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `nulo_inesperado` | `nulo_inesperado` | confere |
| O campo respondido é o esperado | `nome` | `nome` | confere |
| O verbete da causa esperada estava no contexto | `nulo_inesperado` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L1 | `nulo_inesperado` | `contrato-pedido`, `nulo_inesperado`, `usuario-e-login` |
| L3 | `nulo_inesperado` | `contrato-pedido`, `nulo_inesperado`, `usuario-e-login` |

## Rastro

Gerado dos eventos 152 a 178 da trilha `fase3b_cruzada_qwen__qwen2.5-coder_3b__L1.jsonl`; hash dos eventos deste caso: `7b4046599cccf9f5`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
