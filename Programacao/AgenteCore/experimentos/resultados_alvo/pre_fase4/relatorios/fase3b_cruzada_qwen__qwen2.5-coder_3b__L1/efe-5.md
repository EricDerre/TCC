<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `efe-5` pelo `qwen2.5-coder:3b` com a biblioteca L1

Trilha `fase3b_cruzada_qwen/qwen2.5-coder_3b/efe-5@L1`. Corrida `fase3b_cruzada_qwen`, Ollama 0.34.4; classe 6, nível 3; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`localizador_quebrado`, `ancora-saiba-mais`, `corpo_nao_e_json`); prompt de 1245 tokens; resposta de 54 tokens em 29,6 s |
| O que o modelo declarou | causa `localizador_quebrado`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 5 de 6 conferências conferem; o que não confere: campo apontado que não aparece no caso (`seletor`) |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: (sem falha de rede) passo do roteiro: clicar em Saiba Mais da Picanha ao Alho

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


SELETOR QUE FALHOU: button.saiba-mais

SINTOMA OBSERVADO: O roteiro falha porque o seletor encontrou dois elementos em vez de um.
```

### Busca na biblioteca

Consulta montada em código: endpoint `None`, entidade `Interface`, status `200`, 26 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `localizador_quebrado` | 53,881 | 52,881 | 0,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `ancora-saiba-mais` | 21,381 | 20,381 | 0,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `corpo_nao_e_json` | 8,743 | 7,743 | 0,0 | 0,0 | 1,0 | entregue ao modelo |
| 4 | `limites-do-sistema` | 7,685 | 7,685 | 0,0 | 0,0 | 0,0 | descartado |
| 5 | `entidade-produto` | 7,646 | 7,646 | 0,0 | 0,0 | 0,0 | descartado |
| 6 | `tempo_de_resposta_excedido` | 7,562 | 6,562 | 0,0 | 0,0 | 1,0 | descartado |

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

**`corpo_nao_e_json`**

```text
[corpo_nao_e_json] Corpo não é JSON
A resposta chega (às vezes 200 e Content-Type application/json), mas o corpo é HTML, XML ou aviso em texto — o parse falha no primeiro caractere. Sinais: console "Unexpected token <"; texto legível antes ou no lugar do JSON: Warning do PHP, página de gateway, "Atenção ERRO". Causa: Falha de conexão no site imprime "Atenção ERRO" em HTML (connect.php:16); Warning/Fatal do PHP saem antes da saída; gateway fora devolve a própria página. Notas: Adicionar um exemplo de sintoma específico, como "Página de erro HTML em vez de JSON", para melhorar a identificação de casos onde o corpo da resposta não é JSON. Adicionar um exemplo de sintoma para clarificar que XML também pode causar parse falho.
```

### Prompt

3944 caracteres em 7 partes (hash `ac54599a0d0983b0`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1245 tokens, saída de 54 (teto de 600); 29,6 s no total (21689 ms lendo o prompt, 5794 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: localizador_quebrado
CAMPO: seletor
IMPACTO: O roteiro falha porque o seletor encontrou dois elementos em vez de um.
FONTE: [localizador_quebrado]
```

## O que o modelo declarou

O `qwen2.5-coder:3b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `localizador_quebrado` | caracteres 12 a 32 da resposta |
| CAMPO | `seletor` | caracteres 40 a 47 da resposta |
| IMPACTO | `O roteiro falha porque o seletor encontrou dois elementos em vez de um.` | caracteres 57 a 128 da resposta |
| FONTE | `[localizador_quebrado]` | caracteres 136 a 158 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `localizador_quebrado` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `ancora-saiba-mais`, `corpo_nao_e_json` |
| O campo apontado aparece no caso | `seletor` | **não confere** | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado`, `ancora-saiba-mais` |
| Notas escritas pelo modelo nos verbetes citados | `localizador_quebrado` | informativo | `localizador_quebrado`: 1 nota(s) do modelo (Correta: 1). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O roteiro falha porque o seletor encontrou dois elementos em vez de um.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `localizador_quebrado` | `localizador_quebrado` | confere |
| O campo respondido é o esperado | `seletor` |  | **não confere** |
| O verbete da causa esperada estava no contexto | `localizador_quebrado` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L1 | `localizador_quebrado` | `localizador_quebrado`, `ancora-saiba-mais`, `corpo_nao_e_json` |
| L3 | `localizador_quebrado` | `localizador_quebrado`, `ancora-saiba-mais`, `corpo_nao_e_json` |

## Rastro

Gerado dos eventos 378 a 400 da trilha `fase3b_cruzada_qwen__qwen2.5-coder_3b__L1.jsonl`; hash dos eventos deste caso: `0a45e17fa184a735`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
