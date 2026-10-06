<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `lex-19` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3b_ineditos/qwen2.5_7b/lex-19@L1`. Corrida `fase3b_ineditos`, Ollama 0.34.1; classe 1, nível 2; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`corpo_nao_e_json`, `erro_interno_do_servidor`, `fluxo-reserva-e-cancelamento`); prompt de 1177 tokens; resposta de 64 tokens em 82,8 s |
| O que o modelo declarou | causa `erro_interno_do_servidor`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 5 de 5 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: POST /api/pedidos/7/cancelar

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
<html><head><title>500 Internal Server Error</title></head><body><h1>Internal Server Error</h1></body></html>

SINTOMA OBSERVADO: A resposta de POST /api/pedidos/7/cancelar chega com status 200 e Content-Type application/json, mas o corpo e uma pagina HTML de erro; nao da pra confirmar se a reserva foi cancelada de fato.
```

### Busca na biblioteca

Consulta montada em código: endpoint `POST /api/pedidos/{id}/cancelar`, entidade `Pedido`, status `200`, 54 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `corpo_nao_e_json` | 70,232 | 69,232 | 0,0 | 0,0 | 1,0 | entregue ao modelo |
| 2 | `erro_interno_do_servidor` | 57,592 | 57,592 | 0,0 | 0,0 | 0,0 | entregue ao modelo |
| 3 | `fluxo-reserva-e-cancelamento` | 36,039 | 33,039 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 4 | `valor_fora_do_dominio` | 28,934 | 27,934 | 0,0 | 1,0 | 0,0 | descartado |
| 5 | `contrato-pedido` | 22,812 | 19,812 | 2,0 | 1,0 | 0,0 | descartado |
| 6 | `estado_da_tela_divergente` | 21,817 | 21,817 | 0,0 | 0,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`corpo_nao_e_json`**

```text
[corpo_nao_e_json] Corpo não é JSON
A resposta chega (às vezes 200 e Content-Type application/json), mas o corpo é HTML, XML ou aviso em texto — o parse falha no primeiro caractere. Sinais: console "Unexpected token <"; texto legível antes ou no lugar do JSON: Warning do PHP, página de gateway, "Atenção ERRO". Causa: Falha de conexão no site imprime "Atenção ERRO" em HTML (connect.php:16); Warning/Fatal do PHP saem antes da saída; gateway fora devolve a própria página. Notas: Adicionar um exemplo de sintoma específico, como "Página de erro HTML em vez de JSON", para melhorar a identificação de casos onde o corpo da resposta não é JSON. Adicionar um exemplo de sintoma para clarificar que XML também pode causar parse falho.
```

**`erro_interno_do_servidor`**

```text
[erro_interno_do_servidor] Erro interno do servidor (500)
500 com {"detail": ...}: falha própria da API. detail "fault injection: error_500 em produto" é o injetor; "Internal Server Error" é exceção não tratada. Sinais: intermitente sem padrão: injetor com probability < 1; em toda requisição: banco inacessível ou defeito na rota. Causa: Rotas convertem ErrorFault em 500 (produtos.py:42). No site PHP, banco fora NÃO dá 500: imprime "Atenção ERRO" em HTML (connect.php:16). Notas: Adicionar que este erro pode ocorrer devido a falhas no banco de dados ou em rotas, e que a mensagem genérica pode esconder problemas específicos. Adicionar que este erro pode ocorrer de forma intermitente, sem padrão, e que pode ser causado por problemas no banco de dados ou rota.
```

**`fluxo-reserva-e-cancelamento`**

```text
[fluxo-reserva-e-cancelamento] Fluxo de reservar e cancelar
Reserva em cliente/registrar_reserva.php e cancelamento em reserva_cli.php; a API espelha em POST /api/pedidos e POST /api/pedidos/{id}/cancelar. Sinais: regra de data e quantidade só no navegador; reserva alheia cancelada sem checagem de dono. Causa: Data hoje+2 a hoje+90 e pessoas ≥ 1 são só min/max do HTML (registrar_reserva.php:28-35,55); cancelar grava 'Cancelado' (pedidos.py:75).
```

### Prompt

3810 caracteres em 7 partes (hash `515c2ef9bebb7975`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1177 tokens, saída de 64 (teto de 600); 82,8 s no total (66209 ms lendo o prompt, 14460 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: erro_interno_do_servidor
CAMPO: nenhum
IMPACTO: O usuário recebe uma página de erro HTML em vez de uma resposta JSON, o que impede a confirmação do cancelamento da reserva.
FONTE: [erro_interno_do_servidor]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `erro_interno_do_servidor` | caracteres 12 a 36 da resposta |
| CAMPO | `nenhum` | caracteres 44 a 50 da resposta |
| IMPACTO | `O usuário recebe uma página de erro HTML em vez de uma resposta JSON, o que impede a confirmação do cancelamento da reserva.` | caracteres 60 a 184 da resposta |
| FONTE | `[erro_interno_do_servidor]` | caracteres 192 a 218 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `erro_interno_do_servidor` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `erro_interno_do_servidor` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `erro_interno_do_servidor` | confere | contexto: `corpo_nao_e_json`, `erro_interno_do_servidor`, `fluxo-reserva-e-cancelamento` |
| O campo apontado aparece no caso | `nenhum` | não se aplica | o modelo não apontou campo |
| Algum verbete do contexto trata da causa respondida | `erro_interno_do_servidor` | confere | verbetes: `corpo_nao_e_json`, `erro_interno_do_servidor` |
| Notas escritas pelo modelo nos verbetes citados | `erro_interno_do_servidor` | informativo | `erro_interno_do_servidor`: 2 nota(s) do modelo (Correta: 2). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário recebe uma página de erro HTML em vez de uma resposta JSON, o que impede a confirmação do cancelamento da reserva.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `erro_interno_do_servidor` | `corpo_nao_e_json` | **não confere** |
| O campo respondido é o esperado | `nenhum` |  | confere |
| O verbete da causa esperada estava no contexto | `corpo_nao_e_json` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `erro_interno_do_servidor` | `corpo_nao_e_json`, `erro_interno_do_servidor`, `fluxo-reserva-e-cancelamento` |
| L1 | `erro_interno_do_servidor` | `corpo_nao_e_json`, `erro_interno_do_servidor`, `fluxo-reserva-e-cancelamento` |
| L3 | `corpo_nao_e_json` | `corpo_nao_e_json`, `erro_interno_do_servidor`, `fluxo-reserva-e-cancelamento` |

## Rastro

Gerado dos eventos 83 a 106 da trilha `fase3b_ineditos__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `a4ba65b06e833dc0`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
