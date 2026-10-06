<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir da trilha bruta do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo; o hash no fim prova de que eventos ele saiu. -->
# Diagnóstico do caso `efe-14` pelo `qwen2.5-coder:3b` com a biblioteca L1

Trilha `fase3b_cruzada_qwen/qwen2.5-coder_3b/efe-14@L1`. Corrida `fase3b_cruzada_qwen`, Ollama 0.34.4; classe 6, nível 3; texto dos casos: atual. Cada item abaixo diz de que camada é: o que o programa fez é fato; o que o modelo declarou é alegação; o que o código conferiu é o que se pôde checar da alegação.

| Camada | Resumo |
|---|---|
| O que o programa fez | buscou entre 42 verbetes e entregou 3 (`localizador_quebrado`, `ancora-saiba-mais`, `limites-do-sistema`); prompt de 1206 tokens; resposta de 70 tokens em 30,2 s |
| O que o modelo declarou | causa `localizador_quebrado`; 1 verbete(s) citado(s); não escreveu raciocínio antes das quatro linhas |
| O que o código conferiu | 6 de 6 conferências conferem |

## O que o programa fez

### Entrada

O caso como foi posto no prompt:

```text
REQUISIÇÃO: (sem falha de rede) passo: clicar no botao do segundo cartao

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


SELETOR QUE FALHOU: div.thumbnail:nth-child(3) button.saiba-mais

SINTOMA OBSERVADO: O roteiro funciona em alguns dias e falha em outros.

OBSERVAÇÃO ADICIONAL: A ordem dos produtos na resposta nao e garantida pela API.
```

### Busca na biblioteca

Consulta montada em código: endpoint `None`, entidade `Interface`, status `200`, 33 termos. A busca pontuou os 42 verbetes e entregou os 3 primeiros; abaixo, os mais bem pontuados.

| Posição | Verbete | Pontuação | BM25 | Reforço por endpoint | Reforço por entidade | Reforço por status | Destino |
|---|---|---|---|---|---|---|---|
| 1 | `localizador_quebrado` | 56,906 | 55,906 | 0,0 | 1,0 | 0,0 | entregue ao modelo |
| 2 | `ancora-saiba-mais` | 14,560 | 13,560 | 0,0 | 1,0 | 0,0 | entregue ao modelo |
| 3 | `limites-do-sistema` | 12,929 | 12,929 | 0,0 | 0,0 | 0,0 | entregue ao modelo |
| 4 | `pagina-produtos-api` | 12,794 | 11,794 | 0,0 | 1,0 | 0,0 | descartado |
| 5 | `corpo_vazio` | 12,650 | 12,650 | 0,0 | 0,0 | 0,0 | descartado |
| 6 | `estado_da_tela_divergente` | 11,096 | 10,096 | 0,0 | 1,0 | 0,0 | descartado |

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

**`limites-do-sistema`**

```text
[limites-do-sistema] O que o sistema não faz
Não valida data nem pessoas no servidor; não confere o retorno de $conn->query() em página nenhuma; não checa se a reserva cancelada é do cliente; não faz hash da senha no login. Sinais: dado inválido gravado sem mensagem; redireciona como se tivesse gravado e nada mudou: SQL falhou em silêncio. Causa: A API não revalida a resposta: rotas devolvem JSONResponse cru (produtos.py:1-7); o /docs mostra o esperado, não o que sai pela rede.
```

### Prompt

3768 caracteres em 7 partes (hash `d8ce141556d1c772`). O prompt não foi gravado pela corrida: foi remontado pelas mesmas funções do executor, e está provado até: a documentação entregue; o texto do caso vem do banco atual e não tem prova gravada.

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

Entrada de 1206 tokens, saída de 70 (teto de 600); 30,2 s no total (20570 ms lendo o prompt, 7500 ms gerando). A corrida não gravou a probabilidade dos tokens.

Resposta, como veio:

```text
CAUSA_RAIZ: localizador_quebrado
CAMPO: data-id
IMPACTO: O botão "Saiba Mais..." não abre o produto correto, pois o localizador está quebrado e pode encontrar mais de um elemento com o mesmo seletor.
FONTE: [localizador_quebrado]
```

## O que o modelo declarou

O `qwen2.5-coder:3b` não escreveu raciocínio antes das quatro linhas: a resposta começa direto pelo formato pedido. O que segue é só o que ele declarou nas linhas.

| Linha | Valor (trecho literal da resposta) | Onde está |
|---|---|---|
| CAUSA_RAIZ | `localizador_quebrado` | caracteres 12 a 32 da resposta |
| CAMPO | `data-id` | caracteres 40 a 47 da resposta |
| IMPACTO | `O botão "Saiba Mais..." não abre o produto correto, pois o localizador está quebrado e pode encontrar mais de um elemento com o mesmo seletor.` | caracteres 57 a 199 da resposta |
| FONTE | `[localizador_quebrado]` | caracteres 207 a 229 da resposta |

## O que o código conferiu

Conferências que não dependem de saber a resposta certa:

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| A resposta tem as quatro linhas pedidas |  | confere | todas presentes |
| A causa está entre as permitidas | `localizador_quebrado` | confere | 23 causas permitidas |
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `ancora-saiba-mais`, `limites-do-sistema` |
| O campo apontado aparece no caso | `data-id` | confere | procurado no contrato, no corpo, na requisição, na árvore e no seletor do caso |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado`, `ancora-saiba-mais` |
| Notas escritas pelo modelo nos verbetes citados | `localizador_quebrado` | informativo | `localizador_quebrado`: 1 nota(s) do modelo (Correta: 1). A linha FONTE cita o verbete, não a nota: não dá para saber qual nota o modelo usou. |
| Frase de impacto | `O botão "Saiba Mais..." não abre o produto correto, pois o localizador está quebrado e pode encontrar mais de um elemento com o mesmo seletor.` | não dá para conferir por código | a frase de impacto não tem contraparte no caso para conferir por código |

## Avaliação contra o gabarito

Esta é a única seção que usa o gabarito do caso; nada acima depende dele.

| Pergunta | Respondido | Esperado | Resultado |
|---|---|---|---|
| A causa respondida é a esperada | `localizador_quebrado` | `localizador_quebrado` | confere |
| O campo respondido é o esperado | `data-id` |  | **não confere** |
| O verbete da causa esperada estava no contexto | `localizador_quebrado` |  | confere |

## O mesmo caso com as outras versões da biblioteca

| Versão | Causa respondida | Verbetes entregues |
|---|---|---|
| L1 | `localizador_quebrado` | `localizador_quebrado`, `ancora-saiba-mais`, `limites-do-sistema` |
| L3 | `localizador_quebrado` | `localizador_quebrado`, `ancora-saiba-mais`, `pagina-produtos-api` |

## Rastro

Gerado dos eventos 844 a 866 da trilha `fase3b_cruzada_qwen__qwen2.5-coder_3b__L1.jsonl`; hash dos eventos deste caso: `385b945074276c83`. Origem de cada evento: `registro` (gravado pela corrida), `recalculado` (refeito agora a partir dos mesmos insumos) ou `humano` (julgado por pessoa).
