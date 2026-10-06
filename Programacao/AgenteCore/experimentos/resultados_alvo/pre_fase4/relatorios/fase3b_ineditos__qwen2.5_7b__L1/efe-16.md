<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `efe-16` pelo `qwen2.5:7b` com a biblioteca L1

Trilha `fase3b_ineditos/qwen2.5_7b/efe-16@L1`. Corrida `fase3b_ineditos`, Ollama 0.34.1; classe 6, nível 1; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`localizador_quebrado`, `ancora-saiba-mais`, `tempo_de_resposta_excedido`); prompt de 1225 tokens; resposta de 69 tokens em 89,1 s |
| O que o modelo declarou | causa `tempo_de_resposta_excedido`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 5 de 5 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: (sem falha de rede) passo do roteiro: abrir detalhes do produto de data-id=2

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


SELETOR QUE FALHOU: button[data-id='2']

SINTOMA OBSERVADO: O roteiro falha por tempo esgotado; a pagina carregada agora so tem os cards de data-id 1 e 3 (o roteiro foi escrito pensando em outro estado da listagem).
```

### Busca na biblioteca

Consulta montada em código: endpoint `None`, entidade `Interface`, status `200`, 42 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `localizador_quebrado` | 62,243 | 61,243 | 0,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `ancora-saiba-mais` | 29,177 | 28,177 | 0,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `tempo_de_resposta_excedido` | 24,195 | 23,195 | 0,0 | 0,0 | 1,0 | entregue ao modelo |
| 4 | `fluxo-reserva-e-cancelamento` | 18,329 | 18,329 | 0,0 | 0,0 | 0,0 | descartado |
| 5 | `limites-do-sistema` | 15,471 | 15,471 | 0,0 | 0,0 | 0,0 | descartado |
| 6 | `estrutura_aninhada_divergente` | 14,780 | 14,780 | 0,0 | 0,0 | 0,0 | descartado |

### Documentação entregue ao modelo

**`localizador_quebrado`**

```text
[localizador_quebrado] Localizador (seletor) quebrado
Nenhuma requisição falhou: o roteiro não acha o elemento (seletor não casa) ou acha mais de um (ambíguo). O problema é o localizador, não o dado. Sinais: "Ver mais" vs "Saiba Mais...", data-produto vs data-id: texto ou atributo inexistente; nth-child que funciona às vezes: ordem não garantida. Causa: Elementos reais de produtos_api.php: #produtos-api-grid, .thumbnail, button.saiba-mais[data-id], #modalDetalhe; a lista da API não tem ORDER BY (produtos.py:38). Notas: Adicionado que o localizador pode ser ambíguo, encontrando mais de um elemento com o mesmo seletor.
```

**`ancora-saiba-mais`**

```text
[ancora-saiba-mais] Link "Saiba Mais..." abre produto vazio
Nas listagens do site PHP, "Saiba Mais..." abre produto_detalhes.php?id_produto= vazio: a aspa que fecha o href vem antes do id (produtos_geral.php:51); o link da imagem (linha 34) está certo. Sinais: Saiba Mais leva a produto sem dados; roteiro que procura o link pelo id não o encontra. Causa: Defeito do código original, sem correção. Na aba de API o botão é button.saiba-mais[data-id], sem esse problema.
```

**`tempo_de_resposta_excedido`**

```text
[tempo_de_resposta_excedido] Tempo de resposta excedido
A resposta demora além do aceitável ou nunca chega: sem status (conexão encerrada) ou 200 tardio. 429 e 500 respondem rápido com um código — aqui não. Sinais: 200 correto com segundos de espera: atraso no servidor ou no caminho; sem status, "Failed to fetch": o cliente desistiu antes. Causa: O modo latency dorme 2 s fixos (fault_injection.py:66); atrasos maiores vêm de banco, rede ou carga; o fetch da página não tem tempo limite.
```

### Prompt

3787 caracteres em 7 partes (hash `8af7d21db49f69f1`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1225 tokens, saída de 69 (teto de 600); 89,1 s no total (71213 ms lendo o prompt, 15749 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: tempo_de_resposta_excedido
CAMPO: nenhum
IMPACTO: O usuário não consegue acessar os detalhes do produto com data-id=2, visto que a página carregada não inclui esse item.
FONTE: [tempo_de_resposta_excedido]
```

## O que o modelo declarou

O `qwen2.5:7b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `tempo_de_resposta_excedido` | caracteres 12 a 38 da resposta |
| CAMPO | `nenhum` | caracteres 46 a 52 da resposta |
| IMPACTO | `O usuário não consegue acessar os detalhes do produto com data-id=2, visto que a página carregada não inclui esse item.` | caracteres 62 a 181 da resposta |
| FONTE | `[tempo_de_resposta_excedido]` | caracteres 189 a 217 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `tempo_de_resposta_excedido` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `tempo_de_resposta_excedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tempo_de_resposta_excedido` | confere | contexto: `localizador_quebrado`, `ancora-saiba-mais`, `tempo_de_resposta_excedido` |
| O campo apontado aparece no caso | `nenhum` | não se aplica | o modelo não apontou campo |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | confere | verbetes: `tempo_de_resposta_excedido` |
| Notas escritas pelo modelo nos verbetes citados | `tempo_de_resposta_excedido` | informativo | `tempo_de_resposta_excedido`: sem notas do modelo. A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O usuário não consegue acessar os detalhes do produto com data-id=2, visto que a página carregada não inclui esse item.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `tempo_de_resposta_excedido` | `localizador_quebrado` | **não confere** |
| O campo respondido é o esperado | `nenhum` |  | confere |
| O verbete da causa esperada estava no contexto | `localizador_quebrado` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L0 | `tempo_de_resposta_excedido` | `localizador_quebrado`, `ancora-saiba-mais`, `tempo_de_resposta_excedido` |
| L1 | `tempo_de_resposta_excedido` | `localizador_quebrado`, `ancora-saiba-mais`, `tempo_de_resposta_excedido` |
| L3 | `localizador_quebrado` | `localizador_quebrado`, `ancora-saiba-mais`, `tempo_de_resposta_excedido` |

## Rastro

Gerado dos eventos 745 a 768 da trilha `fase3b_ineditos__qwen2.5_7b__L1.jsonl`; hash dos eventos deste caso: `1c27effc09503af0`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
