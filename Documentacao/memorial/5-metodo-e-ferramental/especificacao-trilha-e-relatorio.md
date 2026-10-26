<!-- ! Alteração de IA - Revisar: documento novo (23/10/2026) com a especificação da linha de raciocínio aberta do agente para a Fase 4: o arquivo de trilha (esquema de evento, versão 2, compatível com o v1 do protótipo trilha.py), as três camadas, a árvore de decisão com um nó por decisão, as conferências em código, os testes de intervenção e a atribuição ao contexto, a probabilidade do rótulo como campo, a justificativa humanizada por molde, a taxonomia de falhas, a regressão por trilha de referência, o aprendizado a partir das trilhas, o trace do Playwright, o relatório por caso para quem desenvolve e a avaliação da própria trilha.
     ! Motivo: pedido do Eric em 23/10/2026: verificar toda a arquitetura necessária para a linha de raciocínio aberta (tracking de cada decisão e ação com a justificativa em linguagem humana, formando uma árvore de decisão navegável, para avaliar o modelo durante o projeto e para o desenvolvedor achar o ponto do erro). Cada escolha abaixo vem de uma linha do mapa de arquitetura da onda 1 da parte B da pesquisa (levantamento §6.14.16) ou do que o projeto já mediu; o que a literatura descartou fica registrado com o motivo, como insumo do documento final. A onda 2 da pesquisa (confiança por probabilidade, Brainiac, grafos, visualização da rede), integrada no mesmo dia, entra na seção 14. -->
<!-- ! Alteração de IA - Revisar: (26/10/2026) 25 trecho(s) corrigido(s) por script no fechamento da Pré-Fase 4, depois da revisão deste documento por um revisor (frases desatualizadas, contradições entre seções, números de decisão e de ficha, texto sem travessão nem seta); a lista com o trecho antigo, o novo e o motivo de cada um está em `Documentacao/memorial/5-metodo-e-ferramental/dados/revisao-pre-fase-4-2026-10-26.json`.
     ! Motivo: o fechamento (P7) previa um revisor por documento de texto; as correções entram declaradas, como as das sínteses da pesquisa, para o texto continuar rastreável. -->

# Especificação da trilha de raciocínio aberta e do relatório por caso (Fase 4)

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). Versão 1, de 23/10/2026, escrita depois da onda 1 da parte B da pesquisa da Pré-Fase 4 ([levantamento §6.14](../2-pesquisa-e-literatura/levantamento-2026-10-01-pre-fase-4.md), subseções §6.14.6 a §6.14.9 e §6.14.11, e o mapa "Parte B, onda 1" em §6.14.16) e sobre o protótipo já medido ([relatório da Pré-Fase 4](../3-resultados-e-analises/pre-fase-4-relatorio.md), seção 4; `Programacao/AgenteCore/experimentos/trilha.py` e `gerar_relatorio_raciocinio.py`). Ela diz o que a Fase 4 implementa; não implementa nada. Onde cita um número da literatura, aponta a linha do mapa ou a subseção do levantamento de onde ele vem; os números do projeto vêm dos relatórios já integrados.

<!-- ! Alteração de IA - Revisar: (23/10/2026, fim do dia) registro da aprovação e da decisão sobre a gramática nesta linha, na seção 14 e na seção 15.
     ! Motivo: o Eric aprovou a versão 1 como base da Fase 4 (ficha 23, decisão 77) e adiou a saída restrita por gramática (ficha 24, decisão 78); sem o registro, o documento diria que as duas decisões ainda estavam abertas. -->
**Aprovada pelo Eric em 23/10/2026 como base da Fase 4** (ficha 23, decisão 77). No mesmo dia ele adiou a saída restrita por gramática que o roadmap §4.1 previa (ficha 24, decisão 78): a Fase 4 confere as quatro linhas em código e lê a probabilidade no token do rótulo, como a seção 14 descreve.

## 1. O que a trilha tem de responder

A linha de raciocínio aberta existe para duas pessoas. Para quem avalia o modelo durante o projeto, ela tem de mostrar, caso a caso, o que entrou, o que o programa fez com isso, o que o modelo declarou e o que o código conseguiu conferir, de modo que um erro possa ser atribuído a uma etapa (interceptação, poda, busca, prompt, modelo, cura, biblioteca) e não "à IA" em bloco. Para quem desenvolve o sistema sob teste, ela tem de levar em poucos segundos ao ponto em que a decisão divergiu da evidência, com uma justificativa em linguagem humana e uma linha de ação.

Quatro princípios, todos sustentados pela literatura da onda 1 e pelo que o projeto mediu:

1. **O que o modelo escreve é declaração, nunca prova.** Vieses no prompt mudaram a resposta de outros modelos sem que a explicação os mencionasse na maioria dos casos, e citações corretas podem ser pós-racionalizadas (até 57% num teste adversarial com um único modelo; §6.14.6 e §6.14.9; no Qwen2.5-7B-Instruct, em perguntas da Wikipédia, cerca de 1 citação em 7, mapa linha 18). No projeto, o modelo decidido não escreve raciocínio em nenhuma resposta oficial e segue documentação errada em 81 a 96% dos casos (relatório da Fase 3-B). Por isso a trilha separa, em cada nó, o que o programa fez (fato), o que o modelo declarou (alegação) e o que o código conferiu (teste), como o `trilha.py` já faz (mapa linha 5).
2. **Nenhuma segunda chamada ao modelo para explicar, localizar o erro ou julgar a trilha.** Uma autoexplicação em texto livre somaria de 47 a 78 s por caso e poderia ser uma racionalização da resposta já dada (mapa linha 8); pedir raciocínio antes da resposta não ajudou modelos de 1,5 a 8B na Fase 3 e o ganho do raciocínio em cadeia se concentra em tarefas simbólicas (mapa linha 9); trocar por um 7B com modo de raciocínio multiplicaria o custo (no OLMo-3-7B-Think, mediana de cerca de 3.818 tokens de cadeia) e esse modelo ficou entre os menos fiéis dos 12 testados (mapa linha 10); modelos de fronteira localizaram o passo errado em 14,2% dos casos no Who&When e juízes por LLM ficaram abaixo de 70% de precisão (mapa linha 21). A justificativa humanizada sai de um molde em código a partir dos campos medidos (mapa linha 7).
3. **Tudo local, sem coletor e sem servidor.** O painel é um arquivo HTML gerado por Python, e o Windows corporativo não permite subir serviços; as convenções gen_ai do OpenTelemetry estão todas em desenvolvimento e o span DECISION do OpenInference não tem atributos dedicados para alternativas nem justificativa (candidatos e escolha vão em JSON livre) e o OpenInference não define atributo para a probabilidade do rótulo (mapa linhas 1 a 3). O formato é um JSONL próprio por corrida, com vocabulário de proveniência do W3C PROV nas arestas da árvore (mapa linha 4) e uma tabela de exportação para nomes gen_ai, opcional.
4. **Custo extra só por gatilho ou amostra.** Cada inferência extra custa de 47 a 78 s nesta CPU; três intervenções por caso somam de 141 a 234 s, o que é inviável em todos os casos mas cabe num gatilho (probabilidade baixa, FONTE divergente) ou numa amostra fixa dos 36 casos de avaliação (mapa linha 11 e risco 4).

## 2. O que a literatura sustenta, item a item

O mapa "Parte B, onda 1" do levantamento (§6.14.16) tem 30 linhas: 18 adotadas, 2 adiadas e 10 descartadas, com o motivo e a fonte de cada uma. A tabela abaixo resume onde cada linha entra nesta especificação; o texto completo de cada motivo está no levantamento e na aba "Raciocínio aberto" do painel.

| Tema do mapa | Veredito | Onde entra aqui |
|---|---|---|
| Formato da trilha: JSONL próprio, cabeçalho de corrida, prompt uma vez por hash, exportação gen_ai opcional | adotado | seção 3 |
| OpenTelemetry e plataformas (Langfuse, MLflow) como formato nativo; OpenInference como esquema do nó | descartado | seção 3 (motivo) |
| Proveniência W3C PROV nas arestas (used, wasDerivedFrom, wasGeneratedBy), sem RDF | adotado | seção 4.3 |
| Três camadas em cada nó | adotado | seção 4.1 |
| Árvore de decisão com alternativas, evidência, resultado, contraste e divergência obrigatória | adotado | seção 4.2 |
| Justificativa humanizada por molde; segunda chamada ao modelo; raciocínio antes da resposta; modelo com modo de raciocínio | adotado; descartado; descartado; descartado | seção 7 (molde) e seção 1, princípio 2 (os três descartes) |
| Teste de intervenção em código (remover, trocar, sem documentação), por gatilho ou amostra | adotado | seção 6.1 |
| Atribuição por remoção exata de cada um dos 3 verbetes (leave-one-out); ContextCite; atenção bruta; gradiente ou atenção treinada; Shapley exato | adotado; descartado; descartado; adiado; adiado | seção 6.2 |
| Conferência da linha FONTE em código; sonda de pós-racionalização com controle | adotado; adotado | seção 5 |
| Probabilidade do rótulo como campo, selo e gatilho, nunca verificador | adotado | seção 6.3 |
| Taxonomia de falhas dos nós, com origem do defeito; localização do erro por LLM | adotado; descartado | seção 8 |
| Regressão por trilha de referência (trilha dourada, diff determinístico); autocorreção com o mesmo modelo | adotado; descartado | seção 9 |
| Revisão humana guiada pela trilha (painel que abre no primeiro nó marcado) | adotado | seção 11 |
| Aprender das trilhas sem retreinar: biblioteca só por acréscimo validado, origem de cada verbete | adotado | seção 10 |
| Trace do Playwright em retain-on-failure como evidência do nó | adotado | seção 4.4 |
| Exigências de registro declaradas como boa prática; LGPD e lei europeia como obrigação | adotado; descartado | seção 13 |
| Relatório para o desenvolvedor em ordem fixa | adotado | seção 11 |
| Avaliação da própria trilha nos 36 casos, com injeção de falhas | adotado | seção 12 |

## 3. O arquivo de trilha

### 3.1 Forma

Um arquivo JSONL por corrida (`trilha_<corrida>_<modelo>_<versao>.jsonl` nas corridas gravadas; na Fase 4, um por execução do agente), uma linha por evento, na ordem em que aconteceu. A versão 1 do esquema é a do protótipo (`trilha.py`, campo `v`): `seq` (número no arquivo), `trilha` (identificador do caso ou da execução), `passo` (número dentro da trilha), `pai` (o `seq` do evento de que este deriva), `tipo`, `camada`, `origem`, `ts` e `dados`. A versão 2, desta especificação, mantém todos esses campos e acrescenta os da seção 4; um leitor da versão 2 lê arquivos da versão 1.

Três decisões de forma vêm do mapa (linha 1) e dos riscos 3 e 11:

- **Cabeçalho de corrida** (evento `corrida`, o primeiro do arquivo): modelo, quantização, versão do Ollama, `top_logprobs` e modo de leitura da probabilidade, `num_ctx`, temperatura, semente, hash da biblioteca L1 (o `contexto_sha256` do harness cobre só a biblioteca; o cabeçalho passa a ter também o hash do prompt fixo e o do índice BM25), data e hora de início e de fim, e a versão do esquema. É o que permite comparar corridas quando o Ollama se atualiza sozinho ou quando uma convenção externa muda.
- **Texto grande uma vez só**: prompt, resposta crua, árvore de acessibilidade podada e trace do Playwright entram como evento `blob` identificado por hash SHA-256; os outros eventos citam o hash. O prompt fixo do diagnóstico, igual em todos os casos de uma corrida, fica gravado uma vez por hash.
- **Limites declarados**: número máximo de nós por diagnóstico e por cura, tamanho máximo de blob inline (acima disso o conteúdo vai para arquivo ao lado, citado pelo hash e pelo caminho), e o tamanho da trilha medido e registrado no fim da corrida (risco 3).

### 3.2 Origem de cada evento

`origem` continua com os quatro valores do protótipo: `ao_vivo` (emitido pelo agente da Fase 4 no momento), `registro` (lido de uma corrida gravada), `recalculado` (refeito agora a partir dos mesmos insumos, como o prompt remontado das corridas da Fase 3) e `humano` (veredito de revisão). Um relatório nunca mistura as origens sem dizer qual é.

### 3.3 Tipos de evento

Os nove tipos do protótipo ficam: `corrida`, `blob`, `entrada` (o caso que entrou), `candidatos` (o que a busca pontuou e o que escolheu), `prompt`, `inferencia` (tempos, contagens de tokens, `prompt_eval_cached_count`), `declaracao` (as quatro linhas, cada uma como trecho literal da resposta, com posição), `verificacao` e `acao`. A Fase 4 acrescenta:

| Tipo | Camada | O que registra |
|---|---|---|
| `interceptacao` | programa | requisição e resposta HTTP capturadas pelo Playwright (método, caminho, status, hashes dos corpos), a árvore de acessibilidade da página (hash do blob) e a aresta de chamada HTTP entre o front-end PHP e a rota FastAPI, montada em código a partir do tráfego capturado |
| `poda` | programa | o que a poda em código tirou e deixou (contagens antes e depois, regras aplicadas), com o hash do resultado |
| `decisao` | programa | um nó da árvore (seção 4.2): a decisão, as alternativas, a evidência, o resultado, a divergência e a justificativa |
| `intervencao` | verificacao | um teste de intervenção ou uma remoção (seção 6): o que mudou no contexto, o rótulo e a probabilidade antes e depois |
| `cura` | programa | candidatos de seletor gerados da árvore de acessibilidade, a verificação em código de cada um e a aplicação na reexecução (só depois de verificada, mapa linha 26) |
| `edicao_biblioteca` | programa | proposta de acréscimo à biblioteca, validação em código, aceite ou recusa, origem do texto (seção 10) |
| `incidente` | programa | falha do próprio harness (Ollama fora do ar, tempo esgotado, trace ausente), com o que foi feito a seguir (seção 13) |
| `revisao` | humano | veredito de pessoa sobre um nó (certo, errado, não dá para saber) e o comentário |

### 3.4 Por que não um formato pronto

O OpenTelemetry gen_ai tem 18 operações, todas em desenvolvimento e sem release publicado; amarrar o esquema a elas exporia a trilha a mudanças externas (mapa linha 1). Langfuse e MLflow Tracing pedem SDK, coletor ou plataforma hospedada, e o painel não tem servidor (linha 2). O span DECISION do OpenInference põe candidatos e escolha em JSON livre, não tem campo de justificativa e não define atributo para a probabilidade do rótulo, que é o sinal que separa acerto de erro no projeto (linha 3). Da organização do Langfuse aproveita-se só a ideia de árvore de spans; dos nomes gen_ai, uma tabela de exportação (diagnóstico como chat, cura como execute_tool, poda como plan, BM25 como retrieval) que não muda o esquema próprio.

## 4. O nó de decisão e a árvore

### 4.1 As três camadas

Cada nó carrega as três camadas separadas, como hipótese, teste e conclusão (mapa linha 5):

- **programa**: o que o código fez e com que entrada, sempre citando os eventos (`seq`) e os blobs (hash) de onde veio;
- **modelo**: o que o modelo declarou, sempre como trecho literal da resposta, com a posição; nunca parafraseado;
- **verificacao**: o que o código conferiu da declaração sem usar o gabarito (seção 5), com veredito `confere`, `nao_confere`, `nao_se_aplica` ou `informativo`, e o campo `usa_gabarito` para as conferências que só valem na avaliação.

### 4.2 Campos do nó

```json
{"tipo": "decisao", "camada": "programa", "dados": {
  "decisao": "diagnostico",
  "alternativas": [{"opcao": "campo_renomeado", "escore": 0.63}, {"opcao": "tipo_incompativel", "escore": 0.21}],
  "escolha": "campo_renomeado",
  "evidencia": [{"seq": 12, "papel": "sinal_em_codigo"}, {"seq": 15, "papel": "verbete_entregue"}],
  "resultado": "rotulo_emitido",
  "contraste": "campo_renomeado e nao tipo_incompativel porque o sinal 'chave ausente na resposta' esta presente e o verbete v-07 trata do mesmo campo",
  "divergencia": {"ha": false, "entre": [], "detalhe": null},
  "confianca": {"logprob_rotulo": -0.46, "p_rotulo": 0.63, "alternativas_top": 3, "selo": "medio"},
  "justificativa": "O agente respondeu 'campo_renomeado' porque ...",
  "falha": null,
  "prov": {"used": ["v-07", "v-12"], "wasDerivedFrom": [], "wasGeneratedBy": null}}}
```

Regras dos campos:

- `decisao` é um valor fechado: `interceptacao`, `poda`, `recuperacao` (quais verbetes entram), `montagem_do_prompt`, `diagnostico`, `cura`, `edicao_biblioteca`, `reexecucao`. Cada etapa da Fase 4 emite ao menos um nó.
- `alternativas` lista o que foi considerado e descartado, com o escore que o decidiu: no diagnóstico, as outras causas da taxonomia de 23 com a probabilidade do rótulo (as alternativas devolvidas em `top_logprobs`); na recuperação, os verbetes candidatos com a pontuação BM25 e os sinais; na cura, os candidatos de seletor com o resultado da verificação (mapa linha 6).
- `evidencia` aponta eventos, nunca copia texto.
- `contraste` responde "por que esta e não a segunda": é preenchido pelo molde (seção 7) a partir dos campos, não pelo modelo.
- `divergencia` é obrigatória: diz se o que o modelo declarou difere do que o código mediu (a FONTE cita um verbete que não estava no contexto; a causa não é tratada por nenhum verbete entregue; a intervenção mudou o rótulo) e entre quais camadas. É o marcador que esta especificação usa para levar o desenvolvedor ao ponto do erro; a literatura mediu só que, no Who&When, o melhor método com LLMs localizou o passo decisivo em 14,2% dos casos (mapa linha 6). A ausência de divergência significa "nada detectado pelos testes", nunca "o modelo é fiel" (risco 2).
- `confianca` guarda a probabilidade do rótulo e das alternativas (seção 6.3).
- `justificativa` é o texto humanizado gerado por molde (seção 7).
- `falha` recebe o tipo da taxonomia da seção 8 quando uma regra em código ou uma revisão humana marca o nó.

### 4.3 Arestas e proveniência

A árvore é causal, não um log plano: `pai` liga cada nó ao que o originou (o nó de diagnóstico ao de montagem do prompt; o de cura ao de diagnóstico; o de edição da biblioteca ao de cura verificada). Nas arestas que importam para rastrear um erro até a origem, o vocabulário é o do W3C PROV, em campos JSON, sem RDF (mapa linha 4): `used` liga a declaração aos verbetes citados e aos sinais que entraram no prompt; `wasDerivedFrom` liga um verbete editado da L1 ao caso e ao diagnóstico que o geraram; `wasGeneratedBy` liga um seletor curado ao nó de cura que o produziu. É por essas arestas que um diagnóstico errado chega ao verbete e à edição que o originaram, o que importa num sistema em que a documentação errada é seguida em 81 a 96% dos casos.

### 4.4 O que a Fase 4 emite em cada passo

| Passo da Fase 4 | Eventos | Nó de decisão | O que o código confere | Custo de modelo |
|---|---|---|---|---|
| Interceptação (Playwright) | `interceptacao`, `blob` da árvore e dos corpos | `interceptacao` (o que foi capturado e o que foi ignorado) | contrato esperado presente; corpos com hash | nenhum |
| Poda em código | `poda` | `poda` (regras aplicadas, contagens) | o que saiu não continha o campo em disputa | nenhum |
| Recuperação (BM25 com sinais) | `candidatos` | `recuperacao` (candidatos, escolhidos, pontuação) | k verbetes, hash do índice | nenhum |
| Montagem do prompt | `prompt` (hash) | `montagem_do_prompt` | prompt igual ao fixo mais o caso e os verbetes (hash) | nenhum |
| Diagnóstico | `inferencia`, `declaracao` | `diagnostico` (alternativas com probabilidade, escolha, contraste, divergência, selo) | as conferências da seção 5 | 1 inferência |
| Intervenção (se disparada) | `intervencao` | atualiza `divergencia` e `confianca` do nó de diagnóstico | mudança de rótulo e variação de probabilidade | 1 a 3 inferências |
| Cura de seletor | `cura` | `cura` (candidatos, verificação, escolha) | candidato existe na árvore; único; estável na reexecução | nenhum (a geração é em código) |
| Reexecução de verificação | `acao`, `blob` do trace (se falhou) | `reexecucao` | o fluxo passou; a cura só vira "aplicada" aqui | nenhum |
| Edição da biblioteca | `edicao_biblioteca` | `edicao_biblioteca` (proposta, validação, aceite) | validação em código; origem do texto | 1 inferência (proposta), quando houver |
| Falha do harness | `incidente` | nenhum | o que foi tentado a seguir | nenhum |

O trace do Playwright entra em modo retain-on-failure, anexado como evidência ao nó da etapa que falhou (DOM antes e depois, rede, localizador), e não como trilha do agente; o modo "on" é pesado e o tamanho por teste não é oficial, logo precisa ser medido aqui (mapa linha 26).

## 5. Conferências em código

As oito conferências do protótipo continuam, todas sem gabarito (`trilha.py`, função `verificar`): as quatro linhas presentes; a causa está entre as 23 permitidas; o verbete citado existe na biblioteca; o verbete citado estava no contexto entregue; o campo apontado aparece no caso; algum verbete do contexto trata da causa respondida; notas escritas pelo modelo nos verbetes citados (informativo); frase de impacto (não dá para conferir por código, e o relatório diz isso).

A Fase 4 acrescenta, pelo mapa (linhas 17 e 18):

- `fonte_formato_valido`: a linha FONTE cita só identificadores no formato do projeto, sem texto livre; em dois modelos de 7B testados (LLaMA 2 7B Chat e Zephyr 7B), 54,5% a 62,4% das frases ficaram sem citação e houve, às vezes, citação de documentos inexistentes ou em formato errado.
- `fonte_contem_termo_da_causa`: o verbete citado contém o termo da causa respondida.
- `citacao_recall_precisao` (só com gabarito, `usa_gabarito: true`): recall e precisão da citação contra o verbete-ouro nos 36 casos de avaliação. Mede sustentação, não causa: um verbete citado e correto ainda pode não ter sido o que decidiu a resposta.
- `sonda_de_pos_racionalizacao` (só na avaliação): planta um trecho curto num verbete não citado e compara com a corrida sem inserção, nos 36 casos; o controle é a corrida normal, logo custa uma inferência por caso. Mede a taxa de pós-racionalização da FONTE deste agente, como consistência medida e não como fidelidade ao mecanismo interno.

Toda conferência grava `regra`, `alvo`, `resultado`, `evidencia` e `usa_gabarito`, como no protótipo.

## 6. Intervenção, atribuição e probabilidade

### 6.1 Testes de intervenção

Três intervenções em código por nó de diagnóstico (mapa linha 11): remover o verbete citado (substituído por um marcador neutro, para não mudar o formato do prompt), trocá-lo por um verbete errado e refazer a inferência sem documentação. Cada uma registra a mudança de rótulo e a variação da probabilidade do rótulo original. Só a mudança medida passa a FONTE de "declarada" a "verificada".

Gatilhos: probabilidade do rótulo abaixo do limiar (seção 6.3), FONTE divergente (cita verbete fora do contexto, ou nenhum verbete do contexto trata da causa) ou pertencer à amostra fixa dos 36 casos de avaliação. Custo: de 141 a 234 s por caso quando as três rodam (1,4 a 2,3 h nos 36), por isso nunca em todos os casos (risco 4).

Variação natural: entre corridas iguais mudam de 0 a 3 casos em 36 (relatório da Fase 3-B). Uma mudança de rótulo depois da remoção só conta como efeito do verbete se vier com variação de probabilidade registrada e, nos casos de intervenção, com a inferência de base repetida (risco 5). Quando o rótulo original sai do `top_logprobs` depois da remoção, o Ollama não pontua uma continuação dada, e a trilha registra só um limite inferior da queda (o rótulo ficou abaixo da última alternativa devolvida), marcado como tal (risco 6). Remoção que não muda o rótulo é registrada, por escolha desta especificação, como "sem efeito medido do contexto" (pode ser conhecimento do modelo ou verbete redundante; a literatura levantada não separa os dois casos), e não como falha de atribuição; verbetes que dizem a mesma coisa são marcados como redundantes (risco 7).

### 6.2 Atribuição ao contexto

Com três verbetes por prompt, a remoção exata de cada um (leave-one-out) custa 3 inferências e é mais barata que qualquer método por amostragem (mapa linha 12): verbetes no fim do prompt (para o prefixo em cache reduzir o prefill, registrando `prompt_eval_cached_count`), `num_predict` curto, só até a linha CAUSA_RAIZ, e campos separados para "fonte que causou" (a remoção mudou o rótulo) e "fonte que sustenta" (o verbete trata da causa). Descartados: ContextCite com 32 ablações e Lasso (avaliado em conjuntos com 32,4 a 165,8 fontes por exemplo, em média; aqui custaria de 25 a 42 min por caso, linha 13) e pesos de atenção brutos (o Ollama não expõe atenções, e atenção não é explicação fiel, linha 15). Adiados: atribuição por gradiente ou atenção treinada (o Inseq atende só a modelos do Hugging Face Transformers e o README dele não menciona GGUF nem llama.cpp, e o modelo em precisão cheia não cabe nos cerca de 7 GB livres, linha 16) e Shapley exato sobre os 8 subconjuntos (7 inferências extras, de 329 a 546 s por caso, só numa amostra de casos com verbetes redundantes, depois da Fase 4, linha 14).

### 6.3 Probabilidade do rótulo

Campo próprio no nó de diagnóstico, com a probabilidade do rótulo e das alternativas devolvidas em `top_logprobs` (a sonda de 01/10/2026, no Ollama 0.34.4, verificou que ele devolve a probabilidade por token, de antes da temperatura; o Ollama já está na 0.40.2, e a verificação se repete antes de cada corrida, mapa da onda 2, linha 8). Usos (mapa linha 19): selo de confiança no relatório (alto, médio, baixo, por limiares a fixar com a análise da corrida 12 e a onda 2 da pesquisa, seção 14), gatilho de intervenção e de revisão humana. Nunca verificador: a corrida 12 mediu AUROC de 0,78 e metade dos erros sai confiante (relatório da Pré-Fase 4, seção 5), então um selo alto não dispensa a conferência.

## 7. Justificativa humanizada por molde

A frase que o desenvolvedor lê é gerada em código a partir dos campos do nó, com custo zero de inferência e fidelidade garantida ao que foi medido, porque o texto só diz o que o código registrou (mapa linha 7). Um molde por tipo de decisão, com três partes fixas:

1. **O que foi decidido e com base em quê**: "O agente respondeu *{causa}* no campo *{campo}* porque o sinal *{sinal}* está presente na resposta HTTP e o verbete *{id}* trata desse campo."
2. **Por que não a alternativa**: "A segunda causa, *{alternativa}*, ficou com probabilidade *{p2}* e nenhum verbete entregue a sustenta."
3. **O que o código conferiu e o que não dá para conferir**: "A FONTE cita *{n}* verbetes, todos presentes no contexto; a remoção do verbete *{id}* mudou a resposta (de *{causa}* para *{outra}*), então ele pesou na decisão." Abaixo do limiar de probabilidade, entra a frase fixa de incerteza: "O agente não está seguro desta causa (probabilidade *{p}*); trate como hipótese e confira o campo *{campo}* antes de agir."

Texto ajustado à confiança interna melhorou a discriminação humana na literatura (§6.14.8), e explicações fluentes sem base aumentam a dependência excessiva (risco 8): por isso o molde nunca afirma mais do que os campos medidos, e a frase de incerteza é obrigatória, não opcional. O relatório marca a justificativa como "gerada por molde", para ninguém a ler como texto do modelo.

## 8. Taxonomia de falhas dos nós

Taxonomia própria, com campo de origem do defeito, rotulada por regras em código e, na avaliação, por anotação humana (mapa linha 20; no MAST, 44,2% das falhas vieram de desenho e especificação, e no TRAIL formato e instrução somaram quase 42% dos erros):

| Origem | Tipos |
|---|---|
| programa | `interceptacao_incompleta`, `poda_removeu_evidencia`, `busca_sem_verbete_relevante`, `prompt_diferente_do_fixo`, `formato_das_quatro_linhas` (tipo separado: a resposta não tem as quatro linhas ou tem texto fora delas) |
| modelo | `rotulo_errado`, `rotulo_fora_da_taxonomia`, `campo_errado`, `citacao_fora_do_contexto`, `citacao_inexistente`, `causa_sem_verbete_que_a_trate` |
| cura | `candidato_invalido`, `candidato_ambiguo`, `reexecucao_falhou` |
| biblioteca | `acrescimo_recusado_pela_validacao`, `texto_de_origem_proibida` (seção 10) |
| harness | `incidente` (Ollama fora do ar, tempo esgotado, trace ausente) |

Separar harness de modelo evita culpar o modelo por erro do programa, e vice-versa. Localizar o erro ou rotular a falha com um LLM lendo a trilha fica descartado (mapa linha 21).

## 9. Regressão por trilha de referência

Para cada caso fixo com gabarito, uma trilha dourada (verbetes recuperados, sinais, rótulo, seletor curado); a cada versão do agente, um diff determinístico em código entre a trilha nova e a dourada, com casamento exato e limiar 1,0 na sequência de nós, que marca o primeiro nó divergente (mapa linha 22). Sem custo de modelo; a escolha de regras determinísticas no lugar de um juiz por LLM é desta especificação (juízes por LLM ficaram abaixo de 70% de precisão na literatura, mapa linha 21), aceitando que regras achem menos divergências do que um leitor acharia. O diff tolera a variação natural de 0 a 3 casos em 36 entre corridas iguais: uma divergência só vira regressão quando se repete em duas corridas ou quando passa do limiar de ruído medido. Autocorreção com o mesmo modelo ("reveja seu diagnóstico") fica descartada: troca mais certo por errado em modelos deste porte e custaria mais 47 a 78 s por rodada (mapa linha 23).

## 10. Aprender das trilhas sem retreinar

A biblioteca L1 continua como a de partida (decisões 52, 69 e 73) e só cresce por acréscimo validado em código (decisões 30 e 33), e a trilha passa a registrar a origem de cada verbete (humano, edição do modelo, texto do sistema sob teste), o evento de aceite ou recusa e a aresta `wasDerivedFrom` até o caso de origem (mapa linha 25). O prêmio para um verbete é só o acerto conferido nos 36 casos nunca vistos, nunca a qualidade da justificativa (mapa linha 25): em agentes de fronteira treinados por reforço em tarefas de código, penalizar os pensamentos ruins na cadeia de raciocínio ensinou o modelo a ofuscar a intenção, efeito que aqui não foi medido, já que o modelo não é treinado. Dois bloqueios em código (riscos 9 e 10): nenhum acréscimo sem reavaliação nos casos nunca vistos, e nenhum texto extraído de respostas HTTP do sistema sob teste entra na biblioteca sem validação, porque isso envenenaria diagnósticos futuros. O ciclo de correção do roadmap (§4.2: estado por verbete, operação "correção" sem apagar histórico) emite eventos `edicao_biblioteca` com a mesma origem e as mesmas arestas.

## 11. Relatório por caso e revisão guiada pela trilha

O relatório para o desenvolvedor é gerado por script do arquivo bruto, em ordem fixa (mapa linha 29):

1. veredito: CAUSA_RAIZ e CAMPO, com o selo de probabilidade e, se houver, o carimbo de conflito (divergência entre o declarado e o medido);
2. a evidência: o campo divergente do contrato lado a lado com o trecho podado da resposta HTTP, com o hash e o ponteiro para o artefato;
3. o contraste com a segunda causa;
4. a FONTE declarada, com o resultado da conferência e da intervenção, quando houve;
5. uma linha de ação concreta (o que conferir, onde, e o comando para reexecutar o caso);
6. a árvore completa, recolhida, nó a nó, com as três camadas separadas e a seção de avaliação (gabarito) por último e à parte, porque na Fase 4 o agente não terá gabarito.

Explicação só reduz a dependência excessiva quando conferir custa menos que refazer (§6.14.8); por isso a conferência pelo desenvolvedor, nos itens 1 a 5, tem de custar bem menos do que diagnosticar a falha sozinho, na prática segundos de leitura. No painel, a revisão guiada abre no primeiro nó marcado por código (verificador discorda, probabilidade baixa, fonte não citada, cura reprovada), compara duas corridas lado a lado e gera o comando Python para reexecutar o caso a partir de um nó com o contexto editado (mapa linha 24; na literatura os revisores gastaram cerca de 10 de 15 minutos só lendo a trilha, e voltar, editar e reexecutar foi o recurso mais bem avaliado). Como o painel não tem servidor, a reexecução é um comando copiado, não um botão.

## 12. Avaliação da própria trilha

Nos 36 casos de avaliação, com gabarito (mapa linha 30): (a) se a divergência sinalizada coincide com os erros reais, medida como TPR vezes TNR (acaso em 0,25); (b) validação por injeção programada de falhas, mutando verbetes, contratos e seletores, uma corrida por mutação, para saber se a trilha aponta o nó certo; (c) no relatório, acerto da localização do erro, tempo até a decisão e adesão apropriada (aceitar o diagnóstico quando está certo e recusar quando está errado), com um revisor humano, declarando a utilidade percebida como medida secundária. A sonda de pós-racionalização (seção 5) e a repetição da inferência de base (seção 6.1) fazem parte desta avaliação.

## 13. Exigências de registro, declaradas como boa prática

Os casos são sintéticos, sem dados pessoais nem decisão sobre titular, e, na leitura desta especificação, um agente de QA não consta das categorias de alto risco do regulamento europeu de IA: a LGPD (art. 20) e o regulamento não são tratados como obrigações deste agente (mapa linha 28), e o art. 20 entra só como motivação para a explicação ao desenvolvedor. O que se adota, sem pretensão de conformidade, porque custa só campos de cabeçalho (mapa linha 27): declarar as etapas que registram e as que não registram; início e fim de cada corrida; retenção mínima de seis meses das trilhas das corridas medidas; gravação completa de prompt e resposta, decisão explícita por serem dados locais e sintéticos; e nós de incidente para falhas do harness.

## 14. O que a onda 2 da pesquisa acrescenta e o que fica em aberto

A onda 2 (mapa "Parte B, onda 2" do §6.14.16: confiança por probabilidade, Brainiac, grafos do código e do conhecimento, visualização da rede neural; subseções §6.14.10 e §6.14.12 a §6.14.14) fecha quatro pontos desta especificação e abriu uma só decisão, a da gramática; a aprovação da versão 1 vem da onda 1, e o Eric tomou as duas no mesmo dia (fichas 23 e 24 das [pendências](../pendencias.md); decisões 77 e 78):

- **Como ler a probabilidade do rótulo (seção 6.3)**: no primeiro token do rótulo que vem depois de `CAUSA_RAIZ:`, localizado pela análise das quatro linhas, e não no primeiro token da resposta, porque primeiro token e resposta em texto discordam de 10,2% a 51,4% das vezes no MMLU com restrição média de prompt, em modelos ajustados por instrução (mapa da onda 2, linha 2). O limiar de abstenção e do gatilho de intervenção sai da curva risco-cobertura nos 90 casos com gabarito, com o custo da revisão humana declarado (linha 1 e risco 9); margem entre os dois melhores rótulos e entropia normalizada sobre as 20 alternativas devolvidas entram como sinais de inferência única, sem amostragem (linha 3). Sinais por amostragem (autoconsistência, entropia semântica, confiança verbalizada) ficam descartados: de 5,5 a 11 min por caso nesta CPU (linha 6). ECE e AUROC são reportados separados, e a versão do Ollama, o `top_logprobs` e o modo de leitura vão no cabeçalho da corrida (linhas 7 e 8; seção 3.1).
- **Decodificação restrita por gramática**: o roadmap §4.1 previa saída restrita por gramática (enum de causas) na Fase 4; a onda 2 a marca como adiada, porque a restrição empurra o modelo para alternativas de menor confiança e a probabilidade sob gramática não é a mesma que a trilha mede (linha 5). Como a probabilidade do rótulo é um campo desta trilha, o Eric adiou a gramática (ficha 24, decisão 78): as quatro linhas continuam conferidas em código (seção 5), sem gramática, e ela só volta se o formato inválido passar a custar casos, medido na trilha.
- **Visualização ao vivo e o "cérebro" do agente (seções 4 e 11)**: o que se mostra ao vivo é só o que esta inferência devolve: probabilidade do rótulo, as 20 alternativas, margem, tempos de prefill e de geração, verbetes recuperados com pontuação e a árvore da trilha, com o Python regravando o HTML a cada diagnóstico (linha 26). A rede neural entra como figura estática do GGUF no Netron, com a legenda "esquema do modelo, não atividade" (linha 20); atenção ou ativações ao vivo com um segundo modelo ficam descartadas (um modelo residente por vez; mostraria outro modelo, linha 22), e logit lens e figuras de atenção de um modelo pequeno ficam adiados para depois da Fase 4 e rotulados como ilustrativos (linhas 23 e 24), enquanto autoencoders esparsos e grafos de atribuição ficam descartados, com no máximo um link de referência no painel (linha 25). Toda figura de interpretabilidade leva legenda fixa (ilustrativa, esquema ou medida) e teste de sanidade antes de entrar (linha 28; riscos 1 e 2).
- **Brainiac e grafos (seção 10)**: o Brainiac não entra nem como memória do harness nem como motor da biblioteca (repete o padrão de `claude-memoria/` e reabre a busca híbrida descartada pela decisão 61, linhas 9 a 11); desta ferramenta ficam só os princípios, que esta trilha já segue: registros só por acréscimo com hash, Markdown como fonte da verdade e falha explícita em vez de silêncio (linha 12). O grafo do conhecimento (causas, verbetes L1, casos) gerado dos arquivos do projeto e congelado em SVG é o "toque a mais" que cabe no painel (linha 16); o grafo do código entra só como mapa do sistema (linha 14); a aresta "chamada HTTP" entre o front-end PHP e a rota FastAPI, implementada em código a partir do tráfego interceptado, é a que o projeto escolheu por ter valor diagnóstico para quebra de contrato, sem comparação com os outros tipos de aresta da ferramenta (linha 19), e passa a ser campo do nó `interceptacao` (seção 3.3).

Fica em aberto:

- **Tamanho da trilha e do trace** por caso e por corrida: a medir na primeira corrida da Fase 4, com o limite por diagnóstico declarado no cabeçalho.
- **Limiares concretos** do selo (alto, médio, baixo): números a fixar pela curva risco-cobertura, com a análise da corrida 12 (`resultados_alvo/pre_fase4/confianca.json`); até lá, o gatilho por probabilidade fica desligado e valem os outros dois da seção 6.1: FONTE divergente e a amostra fixa dos 36 casos.
- **Implementação**: é da Fase 4 (roadmap §4). O protótipo `trilha.py` (versão 1 do esquema) e `gerar_relatorio_raciocinio.py` são o ponto de partida; os arquivos congelados da Fase 3 não mudam.

## 15. Rastreabilidade

Fontes desta especificação: o mapa "Parte B, onda 1" e as subseções §6.14.6 a §6.14.9 e §6.14.11 do levantamento da Pré-Fase 4 (fidelidade do raciocínio, formatos de trilha e exigências de registro, relatório para humanos, atribuição ao contexto, uso das trilhas); para a seção 14, o mapa "Parte B, onda 2" e as subseções §6.14.10 e §6.14.12 a §6.14.14; o relatório da Pré-Fase 4 (seções 4 e 5: protótipo da trilha e corrida 12); o relatório da Fase 3-B (variação entre corridas iguais, documentação errada seguida); `trilha.py` e `gerar_relatorio_raciocinio.py`; decisões 52, 61, 69, 70, 73, 75, 77 (aprovação desta versão) e 78 (gramática adiada); roadmap §3.1 e §4.
