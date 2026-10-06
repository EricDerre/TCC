<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `sin-17` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3b_ineditos/qwen2.5_7b/sin-17@L1`. Corrida `fase3b_ineditos`, Ollama 0.34.1; classe 2, nível 1; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`contrato-pedido`, `chave_de_juncao_errada`, `campo_renomeado`); prompt de 1261 tokens; resposta de 67 tokens em 71,4 s |
| O que o modelo declarou | causa `campo_renomeado`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 6 de 6 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": "Cliente Teste", "documento": "11122233344"}]

SINTOMA OBSERVADO: A resposta de GET /api/pedidos traz o campo documento no lugar de cpf; quem le o contrato antigo (CONTRATO_PEDIDO) nao encontra a chave cpf em lugar nenhum do item.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/pedidos`, entidade `Pedido`, status `200`, 49 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `contrato-pedido` | 50,307 | 47,307 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `chave_de_juncao_errada` | 34,100 | 31,100 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `campo_renomeado` | 33,002 | 31,002 | 2,0 | 0,0 | 0,0 | entregue ao modelo |
| 4 | `campo_ausente` | 27,525 | 25,525 | 2,0 | 0,0 | 0,0 | descartado |
| 5 | `usuario-e-login` | 26,496 | 26,496 | 0,0 | 0,0 | 0,0 | descartado |
| 6 | `pedido-reserva` | 24,914 | 21,914 | 2,0 | 1,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`contrato-pedido`**

```text
[contrato-pedido] Contrato de /api/pedidos
GET /api/pedidos?login=<cpf>; POST /api/pedidos {id_clientes, pessoas, data_pedido} → 201; POST /api/pedidos/{id}/cancelar. Campos: id_pedido, pessoas, data_pedido AAAA-MM-DD, status 'Em Análise'|'Cancelado', nome, cpf. Sinais: data noutro formato ou como número; status fora dos dois valores. Causa: cpf vem de login_usuario (pedidos.py). Busca exata na API; o site usa LIKE '%login%' (cliente/index.php:4).
```

**`chave_de_juncao_errada`**

```text
[chave_de_juncao_errada] Chave de junção errada
Tipo e formato certos, mas o valor é de OUTRO registro: categoria ou imagem alheia no produto, nome ou cpf de outro usuário na reserva. Sinais: afeta campo derivado de junção (tipo, nome, cpf, imagem), não os próprios; o dado existe no banco, ligado ao registro errado. Causa: Junções: id_tipo_produto e id_clientes (models.py). No site, cliente/index.php:4 usa LIKE '%login%' — CPF substring de outro casa mais de um cliente. Notas: Retificação: onde diz "Tipo e formato certos, mas o valor é de OUTRO registro: categoria ou imagem alheia no produto, nome ou cpf de outro usuário na reserva. Sinais: afeta campo derivado de junção (tipo, nome, cpf, imagem), não os próprios; o dado existe no banco, ligado ao registro errado. Causa: Junções: id_tipo_produto e id_clientes (models.py). No site, cliente/index.php:4 usa LIKE '%login%' — CPF substring de outro casa mais de um cliente.", leia: Corrigir a junção entre tbprodutos e tbtipos, garantindo que id_tipo_produto esteja corretamente ligado a tbtipos.id_tipo.
```

**`campo_renomeado`**

```text
[campo_renomeado] Campo renomeado
O valor existe sob outra chave: falta a esperada e aparece uma desconhecida com o mesmo tipo e conteúdo (preco → preco_v2, nome → descricao, status → situacao). Sinais: o resto do objeto confere; uma chave sumiu e outra sobrou; vazio ou undefined só naquele campo. Causa: O modo field_renamed troca o campo-alvo por <campo>_v2 (fault_injection.py). Fora dele: contrato mudou no servidor sem atualizar o cliente. Notas: Retificação: onde diz "Fora dele: contrato mudou no servidor sem atualizar o cliente.", leia: Corrigir a afirmação para "Contrato mudou no servidor sem atualizar o cliente e API não reflete as mudanças.".
```

### Prompt

4043 caracteres em 7 partes (hash `d69388a9639237cb`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1261 tokens, saída de 67 (teto de 600); 71,4 s no total (53922 ms lendo o prompt, 15343 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: campo_renomeado
CAMPO: cpf
IMPACTO: O usuário vê um campo chamado "documento" em vez do esperado "cpf", o que pode levar a confusão e erros na manipulação dos dados.
FONTE: [campo_renomeado]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `campo_renomeado` | caracteres 12 a 27 da resposta |
| CAMPO | `cpf` | caracteres 35 a 38 da resposta |
| IMPACTO | `O usuário vê um campo chamado "documento" em vez do esperado "cpf", o que pode levar a confusão e erros na manipulação dos dados.` | caracteres 48 a 177 da resposta |
| FONTE | `[campo_renomeado]` | caracteres 185 a 202 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `campo_renomeado` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | confere | contexto: `contrato-pedido`, `chave_de_juncao_errada`, `campo_renomeado` |
| O campo apontado aparece no caso | `cpf` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `campo_renomeado` |
| Notas escritas pelo modelo nos verbetes citados | `campo_renomeado` | informativo | `campo_renomeado`: 1 nota(s) do modelo (Parcial: 1). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário vê um campo chamado "documento" em vez do esperado "cpf", o que pode levar a confusão e erros na manipulação dos dados.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `campo_renomeado` | `campo_renomeado` | confere |
| O campo respondido é o esperado | `cpf` | `cpf` | confere |
| O verbete da causa esperada estava no contexto | `campo_renomeado` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `campo_renomeado` | `contrato-pedido`, `chave_de_juncao_errada`, `campo_renomeado` |
| L1 | `campo_renomeado` | `contrato-pedido`, `chave_de_juncao_errada`, `campo_renomeado` |
| L3 | `campo_renomeado` | `contrato-pedido`, `chave_de_juncao_errada`, `campo_renomeado` |

## Rastro

Gerado dos eventos 183 a 206 da trilha `fase3b_ineditos__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `e2655f4b83cb2bb7`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
