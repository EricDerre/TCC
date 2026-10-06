<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `efe-19` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3b_ineditos/qwen2.5_7b/efe-19@L1`. Corrida `fase3b_ineditos`, Ollama 0.34.1; classe 6, nível 2; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`ancora-saiba-mais`, `registro_duplicado`, `pagina-produtos-api`); prompt de 1116 tokens; resposta de 57 tokens em 60,3 s |
| O que o modelo declarou | causa `localizador_quebrado`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 5 de 5 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: clique em 'Saiba Mais...' da Fraldinha (data-id=3); antes da resposta chegar, clique em 'Saiba Mais...' da Picanha ao Alho (data-id=1); a resposta do produto 1 chega primeiro

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
GET /api/produtos/1 responde em 150ms; GET /api/produtos/3 (disparado antes, pelo primeiro clique) responde em 900ms

SINTOMA OBSERVADO: O ultimo produto clicado foi a Picanha ao Alho, mas o modal termina mostrando os dados da Fraldinha (o clique anterior); nenhum erro aparece no console, e cada resposta em separado esta correta.

OBSERVAÇÃO ADICIONAL: Cada clique dispara um fetch independente pra /api/produtos/{id}; nao ha verificacao de qual clique foi o mais recente antes de preencher o modal.
```

### Busca na biblioteca

Consulta montada em código: endpoint `None`, entidade `None`, status `200`, 80 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `ancora-saiba-mais` | 42,453 | 42,453 | 0,0 | 0,0 | 0,0 | entregue ao modelo |
| 2 | `registro_duplicado` | 39,337 | 39,337 | 0,0 | 0,0 | 0,0 | entregue ao modelo |
| 3 | `pagina-produtos-api` | 36,010 | 36,010 | 0,0 | 0,0 | 0,0 | entregue ao modelo |
| 4 | `corpo_nao_e_json` | 33,574 | 32,574 | 0,0 | 0,0 | 1,0 | descartado |
| 5 | `colecao_no_lugar_de_objeto` | 33,434 | 33,434 | 0,0 | 0,0 | 0,0 | descartado |
| 6 | `entidade-produto` | 31,823 | 31,823 | 0,0 | 0,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`ancora-saiba-mais`**

```text
[ancora-saiba-mais] Link "Saiba Mais..." abre produto vazio
Nas listagens do site PHP, "Saiba Mais..." abre produto_detalhes.php?id_produto= vazio: a aspa que fecha o href vem antes do id (produtos_geral.php:51); o link da imagem (linha 34) está certo. Sinais: Saiba Mais leva a produto sem dados; roteiro que procura o link pelo id não o encontra. Causa: Defeito do código original, sem correção. Na aba de API o botão é button.saiba-mais[data-id], sem esse problema.
```

**`registro_duplicado`**

```text
[registro_duplicado] Registro duplicado
A mesma escrita gravada mais de uma vez: reservas iguais com ids consecutivos, duas respostas 201 para um único gesto. Sinais: registros idênticos exceto pelo id; dois POST com o mesmo corpo na sequência. Causa: POST /api/pedidos insere sem chave de idempotência (pedidos.py:46-66): clique duplo vira duas linhas. registrar_reserva.php insere a cada POST — recarregar após reservar reenvia o formulário.
```

**`pagina-produtos-api`**

```text
[pagina-produtos-api] Aba "Produtos (API)", a fronteira JSON
produtos_api.php monta os cartões com fetch() em localhost:8000/api/produtos — a única fronteira JSON do cobaia; detalhe via GET /api/produtos/{id}. Sinais: "Carregando..." parado: o fetch nunca resolveu; "Nenhum produto retornado pela API.": não é lista, ou vazia. Causa: formatarPreco() usa Number(): preço não numérico sai cru; tipo objeto sai via JSON.stringify; botão button.saiba-mais[data-id].
```

### Prompt

3534 caracteres em 7 partes (hash `041e4e4095f5a2ab`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1116 tokens, saída de 57 (teto de 600); 60,3 s no total (45317 ms lendo o prompt, 12790 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: localizador_quebrado
CAMPO: nenhum
IMPACTO: O usuário vê os dados do produto errado no modal, causando confusão na visualização.
FONTE: [ancora-saiba-mais]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `localizador_quebrado` | caracteres 12 a 32 da resposta |
| CAMPO | `nenhum` | caracteres 40 a 46 da resposta |
| IMPACTO | `O usuário vê os dados do produto errado no modal, causando confusão na visualização.` | caracteres 56 a 140 da resposta |
| FONTE | `[ancora-saiba-mais]` | caracteres 148 a 167 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `localizador_quebrado` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `ancora-saiba-mais` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `ancora-saiba-mais` | confere | contexto: `ancora-saiba-mais`, `registro_duplicado`, `pagina-produtos-api` |
| O campo apontado aparece no caso | `nenhum` | não se aplica | o modelo não apontou campo |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `ancora-saiba-mais`, `pagina-produtos-api` |
| Notas escritas pelo modelo nos verbetes citados | `ancora-saiba-mais` | informativo | `ancora-saiba-mais`: sem notas do modelo. A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário vê os dados do produto errado no modal, causando confusão na visualização.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `localizador_quebrado` | `estado_da_tela_divergente` | **não confere** |
| O campo respondido é o esperado | `nenhum` |  | confere |
| O verbete da causa esperada estava no contexto | `estado_da_tela_divergente` |  | **não confere** |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `localizador_quebrado` | `ancora-saiba-mais`, `registro_duplicado`, `corpo_nao_e_json` |
| L1 | `localizador_quebrado` | `ancora-saiba-mais`, `registro_duplicado`, `pagina-produtos-api` |
| L3 | `localizador_quebrado` | `ancora-saiba-mais`, `registro_duplicado`, `pagina-produtos-api` |

## Rastro

Gerado dos eventos 816 a 837 da trilha `fase3b_ineditos__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `85ec371c9ea75eba`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
