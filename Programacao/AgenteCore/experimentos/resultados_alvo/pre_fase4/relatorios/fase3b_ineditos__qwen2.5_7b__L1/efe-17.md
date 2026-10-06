<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `efe-17` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3b_ineditos/qwen2.5_7b/efe-17@L1`. Corrida `fase3b_ineditos`, Ollama 0.34.1; classe 6, nível 1; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`localizador_quebrado`, `entidade-produto`, `ancora-saiba-mais`); prompt de 1319 tokens; resposta de 58 tokens em 77,8 s |
| O que o modelo declarou | causa `localizador_quebrado`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 5 de 5 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: (sem falha de rede) passo do roteiro: localizar o titulo 'Picanha ao Alho' como heading de nivel 2

STATUS HTTP: 200

CORPO DA RESPOSTA:
(nenhuma requisicao falhou)

ÁRVORE DE ACESSIBILIDADE DA PÁGINA:
document "Churrascaria Fornalha - Produtos (API)"
  navigation
    link "PRODUTOS"
    link "PRODUTOS (API)"
  main
    heading "Produtos via API" level=2
    group
      heading "Picanha ao Alho" level=3
      text "Carnes"
      button "R$ 89,90" disabled
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      button "R$ 69,90" disabled
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"


SELETOR QUE FALHOU: heading "Picanha ao Alho" level=2

SINTOMA OBSERVADO: O roteiro nao encontra o titulo do produto; na arvore de acessibilidade o nome do produto e um heading de nivel 3, nao 2.
```

### Busca na biblioteca

Consulta montada em código: endpoint `None`, entidade `Interface`, status `200`, 38 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `localizador_quebrado` | 39,526 | 38,526 | 0,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `entidade-produto` | 29,236 | 29,236 | 0,0 | 0,0 | 0,0 | entregue ao modelo |
| 3 | `ancora-saiba-mais` | 20,455 | 19,455 | 0,0 | 1,0 | 0,0 | entregue ao modelo |
| 4 | `tempo_de_resposta_excedido` | 13,344 | 12,344 | 0,0 | 0,0 | 1,0 | descartado |
| 5 | `campo_ausente` | 11,812 | 11,812 | 0,0 | 0,0 | 0,0 | descartado |
| 6 | `estrutura_aninhada_divergente` | 11,729 | 11,729 | 0,0 | 0,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`localizador_quebrado`**

```text
[localizador_quebrado] Localizador (seletor) quebrado
Nenhuma requisição falhou: o roteiro não acha o elemento (seletor não casa) ou acha mais de um (ambíguo). O problema é o localizador, não o dado. Sinais: "Ver mais" vs "Saiba Mais...", data-produto vs data-id: texto ou atributo inexistente; nth-child que funciona às vezes: ordem não garantida. Causa: Elementos reais de produtos_api.php: #produtos-api-grid, .thumbnail, button.saiba-mais[data-id], #modalDetalhe; a lista da API não tem ORDER BY (produtos.py:38). Notas: Adicionado que o localizador pode ser ambíguo, encontrando mais de um elemento com o mesmo seletor.
```

**`entidade-produto`**

```text
[entidade-produto] Produto e sua categoria
Item do cardápio em tbprodutos, ligado a uma categoria de tbtipos (Carnes, Bebidas, Acompanhamentos, Sobremesas). 14 produtos; o id 1 é Picanha ao Alho, Carnes, 89,90. Sinais: título com nome de categoria: junção trocada; preço com grandeza estranha: conversão de valor_produto. Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano. Notas: Retificação: onde diz "Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano.", leia: Corrigir a conversão do preço e destaque no _to_dict de produtos.py. Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro.
```

**`ancora-saiba-mais`**

```text
[ancora-saiba-mais] Link "Saiba Mais..." abre produto vazio
Nas listagens do site PHP, "Saiba Mais..." abre produto_detalhes.php?id_produto= vazio: a aspa que fecha o href vem antes do id (produtos_geral.php:51); o link da imagem (linha 34) está certo. Sinais: Saiba Mais leva a produto sem dados; roteiro que procura o link pelo id não o encontra. Causa: Defeito do código original, sem correção. Na aba de API o botão é button.saiba-mais[data-id], sem esse problema.
```

### Prompt

4099 caracteres em 7 partes (hash `f7068e9ab64f6691`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1319 tokens, saída de 58 (teto de 600); 77,8 s no total (62422 ms lendo o prompt, 13261 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: localizador_quebrado
CAMPO: nenhum
IMPACTO: O usuário não encontra o título correto do produto, visto que o seletor está configurado incorretamente.
FONTE: [localizador_quebrado]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `localizador_quebrado` | caracteres 12 a 32 da resposta |
| CAMPO | `nenhum` | caracteres 40 a 46 da resposta |
| IMPACTO | `O usuário não encontra o título correto do produto, visto que o seletor está configurado incorretamente.` | caracteres 56 a 160 da resposta |
| FONTE | `[localizador_quebrado]` | caracteres 168 a 190 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `localizador_quebrado` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `entidade-produto`, `ancora-saiba-mais` |
| O campo apontado aparece no caso | `nenhum` | não se aplica | o modelo não apontou campo |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado`, `ancora-saiba-mais` |
| Notas escritas pelo modelo nos verbetes citados | `localizador_quebrado` | informativo | `localizador_quebrado`: 1 nota(s) do modelo (Correta: 1). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário não encontra o título correto do produto, visto que o seletor está configurado incorretamente.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `localizador_quebrado` | `localizador_quebrado` | confere |
| O campo respondido é o esperado | `nenhum` |  | confere |
| O verbete da causa esperada estava no contexto | `localizador_quebrado` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `localizador_quebrado` | `localizador_quebrado`, `entidade-produto`, `ancora-saiba-mais` |
| L1 | `localizador_quebrado` | `localizador_quebrado`, `entidade-produto`, `ancora-saiba-mais` |
| L3 | `localizador_quebrado` | `localizador_quebrado`, `entidade-produto`, `ancora-saiba-mais` |

## Rastro

Gerado dos eventos 770 a 791 da trilha `fase3b_ineditos__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `802ee9cd058c32e2`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
