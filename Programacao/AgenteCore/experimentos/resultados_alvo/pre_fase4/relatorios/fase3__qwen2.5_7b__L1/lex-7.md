<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `lex-7` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3/qwen2.5_7b/lex-7@L1`. Corrida `fase3`, Ollama 0.34.0; classe 1, nível 1; texto dos casos: anterior à correção de 28/09/2026. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`corpo_vazio`, `ancora-saiba-mais`, `colecao_no_lugar_de_objeto`); prompt de 1175 tokens; resposta de 60 tokens em 78,5 s |
| O que o modelo declarou | causa `corpo_vazio`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 5 de 5 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/1

STATUS HTTP: 204

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:


SINTOMA OBSERVADO: A tela de detalhe abre em branco, sem mensagem de erro.
```

### Busca na biblioteca

Consulta montada em código: endpoint `GET /api/produtos/{id}`, entidade `Produto`, status `204`, 14 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `corpo_vazio` | 29,236 | 28,236 | 0,0 | 0,0 | 1,0 | entregue ao modelo |
| 2 | `ancora-saiba-mais` | 11,570 | 11,570 | 0,0 | 0,0 | 0,0 | entregue ao modelo |
| 3 | `colecao_no_lugar_de_objeto` | 10,512 | 7,512 | 2,0 | 1,0 | 0,0 | entregue ao modelo |
| 4 | `recurso_inexistente` | 7,649 | 5,649 | 2,0 | 0,0 | 0,0 | descartado |
| 5 | `campo_ausente` | 7,558 | 6,558 | 0,0 | 1,0 | 0,0 | descartado |
| 6 | `pagina-produtos-api` | 7,294 | 5,294 | 2,0 | 0,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`corpo_vazio`**

```text
[corpo_vazio] Corpo vazio
Status de sucesso e nenhum byte útil no corpo (vazio, só espaços, ou 204). Diferente de "[]", lista vazia, que é JSON válido. Sinais: resp.json() falha em zero caracteres: "Erro ao carregar produtos" ou "Carregando..." parado; "[]" mostra "Nenhum produto retornado pela API.". Causa: Nenhuma rota da CobaiaAPI devolve 204 nem corpo vazio; se chega vazio, foi cortado antes de sair (servidor, proxy) ou a rota errada respondeu. Notas: Adicionar exemplo de sintoma: "Tabela de reservas vazia, sem erro.". Adicionar: "Nenhuma resposta ou resposta vazia pode ser retornada por nenhuma rota da CobaiaAPI.".
```

**`ancora-saiba-mais`**

```text
[ancora-saiba-mais] Link "Saiba Mais..." abre produto vazio
Nas listagens do site PHP, "Saiba Mais..." abre produto_detalhes.php?id_produto= vazio: a aspa que fecha o href vem antes do id (produtos_geral.php:51); o link da imagem (linha 34) está certo. Sinais: Saiba Mais leva a produto sem dados; roteiro que procura o link pelo id não o encontra. Causa: Defeito do código original, sem correção. Na aba de API o botão é button.saiba-mais[data-id], sem esse problema.
```

**`colecao_no_lugar_de_objeto`**

```text
[colecao_no_lugar_de_objeto] Coleção no lugar de objeto (ou o inverso)
Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (["Carnes"]). Sinais: modal "Produto #1"/"(sem descrição)": p é lista; categoria com colchetes: campo veio como lista. Causa: GET /api/produtos devolve lista, GET /api/produtos/{id} objeto (produtos.py); a página não confere a forma antes de ler os campos. Notas: Retificação: onde diz "Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (['Carnes']).", leia: Corrigir que GET /api/produtos/{id} deve devolver um objeto, não uma lista. Retificação: onde diz "Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (['Carnes']).", leia: Corrigir que o campo "tipo" deve ser tratado como uma string, não uma lista.
```

### Prompt

3701 caracteres em 7 partes (hash `975fbd6faa384564`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1175 tokens, saída de 60 (teto de 600); 78,5 s no total (62942 ms lendo o prompt, 13424 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: corpo_vazio
CAMPO: nenhum
IMPACTO: A tela de detalhe abre em branco, sem exibir nenhum produto ou mensagem de erro, pois a resposta da API está vazia.
FONTE: [corpo_vazio]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `corpo_vazio` | caracteres 12 a 23 da resposta |
| CAMPO | `nenhum` | caracteres 31 a 37 da resposta |
| IMPACTO | `A tela de detalhe abre em branco, sem exibir nenhum produto ou mensagem de erro, pois a resposta da API está vazia.` | caracteres 47 a 162 da resposta |
| FONTE | `[corpo_vazio]` | caracteres 170 a 183 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `corpo_vazio` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `corpo_vazio` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `corpo_vazio` | confere | contexto: `corpo_vazio`, `ancora-saiba-mais`, `colecao_no_lugar_de_objeto` |
| O campo apontado aparece no caso | `nenhum` | não se aplica | o modelo não apontou campo |
| Algum verbete do contexto trata da causa respondida | `corpo_vazio` | confere | verbetes: `corpo_vazio` |
| Notas escritas pelo modelo nos verbetes citados | `corpo_vazio` | informativo | `corpo_vazio`: 2 nota(s) do modelo (Correta: 1, Parcial: 1). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `A tela de detalhe abre em branco, sem exibir nenhum produto ou mensagem de erro, pois a resposta da API está vazia.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `corpo_vazio` | `corpo_vazio` | confere |
| O campo respondido é o esperado | `nenhum` |  | confere |
| O verbete da causa esperada estava no contexto | `corpo_vazio` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `corpo_vazio` | `corpo_vazio`, `ancora-saiba-mais`, `colecao_no_lugar_de_objeto` |
| L1 | `corpo_vazio` | `corpo_vazio`, `ancora-saiba-mais`, `colecao_no_lugar_de_objeto` |
| L2 | `corpo_vazio` | `corpo_vazio`, `ancora-saiba-mais`, `colecao_no_lugar_de_objeto` |
| L3 | `corpo_vazio` | `corpo_vazio`, `ancora-saiba-mais`, `colecao_no_lugar_de_objeto` |

## Rastro

Gerado dos eventos 891 a 912 da trilha `fase3__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `c773987852da2db5`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
