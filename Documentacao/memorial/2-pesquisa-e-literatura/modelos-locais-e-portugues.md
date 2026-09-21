<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
<!-- ! Alteração de IA - Revisar: revisão de 11/09/2026 — acrescentado o parágrafo que diz
     quais blocos desta seção são decisão do projeto e não afirmação bibliográfica, a âncora no
     Cap. 7 do livro-texto (FACELI et al., 2025) e o nome da fonte do baseline não-neural
     (JOSEPH, 2026), que estava citado só pelo número 82,4%.
     ! Motivo: quatro blocos desta seção ("Eliminados por critério objetivo", "Achado mais
     valioso", "Alerta de licença", "Riscos operacionais documentados") vinham de leitura de
     licença, ficha do modelo e registro do Ollama, mas estavam escritos no mesmo formato dos
     blocos com fonte — quem revisasse iria procurar referência para eles e não acharia. E os
     82,4% do algoritmo de prioridade em 10 níveis apareciam sem autor, o que impedia levar o
     número ao relatório final. -->
# Pesquisa bibliográfica — Cenário de modelos livres e locais

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá.

### 6.1 Cenário de modelos livres e locais

Levantamento de 12 candidatos executáveis via Ollama, com licença, tamanho, capacidade em português e estabilidade da tag.

Uma ressalva de leitura: os blocos **Eliminados por critério objetivo**, **Achado mais valioso**, **Alerta de licença** e **Riscos operacionais documentados** abaixo são **decisões e verificações deste projeto** — leitura da licença publicada, da ficha de cada modelo e do registro do Ollama nesta máquina —, e não afirmações tiradas da bibliografia; não há fonte a procurar para eles. O que é generalizar a partir de exemplos, o que muda numa rede profunda quando ela é especializada por ajuste fino e por que isso não é o mesmo que trocar de arquitetura estão no Cap. 7 (Métodos Conexionistas) de FACELI et al. (2025) *[capítulo inferido do sumário; conferir no exemplar]*, o livro-texto adotado como orientador teórico do TCC.

**Eliminados por critério objetivo:** OpenCoder (oficialmente só inglês e chinês); StarCoder2 3B/7B (são modelos *base*, não seguem instrução); CodeLlama (2 anos, base Llama 2, português fraco); Mistral 7B (defasado, português fraco); Codestral (22B e licença de não-produção); DeepSeek-Coder-V2 (8,9 GB, acima do orçamento de memória).

**Achado mais valioso:** `qwen2.5-coder:7b` **vs** `qwen2.5:7b` formam um experimento controlado quase perfeito — mesma base, tamanho, licença, tokenização e mês de treino, diferindo **apenas** pelo fine-tuning em código. Responde "especialização em código ajuda nesta tarefa?" sem variáveis de confusão.

**Alerta de licença:** `qwen2.5-coder:3b` está sob **Qwen Research License (não-comercial)**, enquanto o `:7b` da mesma família é Apache 2.0. Decidiu-se mantê-lo na comparação com a restrição documentada, trocando apenas o padrão de produção.

**Português (PoETa v2, nov/2025):** Qwen2.5 7B lidera entre os abertos pequenos com 63,7 NPM; Llama 3.1 8B fica em 53,5. Achado relevante para o dimensionamento: **modelos abaixo de 5B têm perda desproporcional em português** (5,1 pontos de diferença EN↔PT, contra 3,8 nos de 10B+) — o que justifica metodologicamente manter a faixa de 7–8B apesar da latência.

**Riscos operacionais documentados:** tags do Ollama são ponteiros mutáveis, não imutáveis — é preciso registrar o digest sha256 de cada modelo para o experimento ser reproduzível; o modo *thinking* de Qwen3 e Granite 4.2 multiplica a latência e precisa ser desativado; e o cache KV de modelos com 128K de contexto estoura a memória antes do peso do modelo, exigindo fixar `num_ctx`.

**Baseline não-neural:** JOSEPH (2026) descreve uma hierarquia de localizadores em dez níveis extraída da árvore de acessibilidade do DOM, que redescobre um seletor obsoleto em **menos de 1 s**, com 31/31 testes aprovados em três perfis de dispositivo e **custo de API zero** (`https://arxiv.org/abs/2603.20358`). A taxa de **82,4%** de localizadores recuperados foi anotada na primeira leitura da fonte e **[conferir]**: ela não aparece entre as afirmações que a rodada de verificação de 11/09/2026 confirmou nesse artigo (o que ficou confirmado são os 31/31 testes, o tempo abaixo de 1 s e o custo zero), então precisa ser relida no texto original antes de ir ao relatório final. Entra como piso obrigatório dessa tarefa — se os modelos não o superarem, esse é um resultado honesto. Como referência do que já se obtinha antes dos LLMs, o reparo visual de testes web de STOCCO; YANDRAPALLY; MESBAH (2018) corrigiu **81% das quebras** em 2.672 casos de teste ao longo de 86 releases de quatro aplicações.

<!-- ! Alteração de IA - Revisar: parágrafo-ponte para as subseções da rodada 2 da pesquisa (21/09/2026), acrescentado ao fim da seção.
     ! Motivo: a rodada 2 fechou as lacunas que esta seção apontava; sem o ponteiro, quem lê a seção não sabe que o levantamento cresceu (§6.9.9–6.9.17) nem que existe o mapa de decisões (§6.10). Nenhum número novo é digitado aqui: os números ficam nas subseções citadas. -->
## Complemento da rodada 2 da pesquisa (21/09/2026)

Duas subseções novas do [levantamento](levantamento-2026-09-11-fase-3.md) tocam este tema. A §6.9.13 (aprender sem atualizar pesos) formula o que significa, em termos de aprendizado de máquina, um modelo de pesos congelados melhorar pela biblioteca que ele mesmo escreve: a inserção do verbete certo no contexto é tratada na literatura como equivalente a uma atualização transitória de baixo posto, e a evidência de mecanismo (cabeças de indução) existe para a faixa de 8B, não para 1,5B. A §6.9.16 (arquitetura de agentes autônomos de QA) traz a taxonomia de níveis de autonomia e o padrão gatilho-predicado-ação para as invariantes do agente — material da Fase 4. As implicações para a leitura dos resultados da Fase 3 estão no [mapa de decisões](mapa-de-decisoes-fase-3.md) (§6.10).
