<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
<!-- ! Alteração de IA - Revisar: revisão de 11/09/2026 — o marcador sobre i-quants e cache KV,
     que era o único sem fonte da seção, ganhou MCLEOD (2024) e KURT (2026) com a ressalva de
     hardware; o bloco "O que entra no desenho" passou a dizer que é decisão do projeto; e foi
     acrescentada a âncora no Cap. 10 do livro-texto (FACELI et al., 2025).
     ! Motivo: o marcador afirmava que i-quants são mais lentos em CPU e que o cache KV em
     q4_0 chega a ser 92% mais lento em contexto longo, sem dizer de onde vinham os números -
     e a rodada de verificação de 11/09/2026 não confirmou os 92%, que estavam atribuídos a uma
     fonte de blog que não os traz. Deixar o número sem marca faria ele ser copiado para o
     relatório final como se fosse medido. -->
# Pesquisa bibliográfica — Quantização

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá.

### 6.4 Quantização

Verificado nesta máquina (`ollama show`): os seis modelos comparados estão em **Q4_K_M**, a quantização padrão das tags sem sufixo.

- Lee et al. (IJCAI 2025), 1B–405B em 13 datasets: a 4 bits, **Llama-3.2-1B perde 10,1 pp** (GPTQ) ou 5,7 pp (AWQ) em média e **16,0 pp no IFEval**; **3B perde 1,8 pp** (IFEval −0,75); **8B perde 1,3–1,8 pp** (IFEval −2,1). Modelos quantizados sofrem mais em seguir instrução; só inglês foi avaliado.
- *Low-Bit Quantization Favors Undertrained LLMs* (Ouyang et al., ACL 2025), 1.500 checkpoints de 160M a 12B: **modelos pequenos com muitos tokens de treino degradam mais** — o Qwen2.5 (18T tokens) é o caso extremo, e o `1.5b` o mais exposto.
- *Accuracy is Not All You Need* (Dutta et al., NeurIPS 2024): acurácia agregada igual (±2%) esconde **até 13,6% de *flips*** — respostas que mudam de certo para errado e vice-versa —, com a KL-divergência correlacionada a **0,981** (Spearman) com essa taxa no MMLU. Comparar quantizações exige medir flips, não só acerto; é o mesmo motivo pelo qual a comparação entre modelos se faz sobre a matriz de confusão e não sobre a média (FACELI et al., 2025, cap. 10 — Avaliação de Modelos Preditivos) *[capítulo inferido do sumário; conferir no exemplar]*.
- *A Systematic Evaluation of On-Device LLMs* (Song et al., 2025): limiar prático em ~3,5 bits por peso; modelo maior quantizado supera modelo menor em precisão alta.
- Em CPU: i-quants (IQ*) usam *codebook* com muitas leituras de tabela e são mais lentos que k-quants. Sobre o cache KV, MCLEOD (2024) mede que quantizá-lo em `q8_0` no Ollama custa apenas **+0,0043 de perplexidade** (8,3891 → 8,3934 no Qwen 2.5 Coder 7B Q6_K), contra +0,206 a +0,25 em `q4_0`, e corta o cache de um modelo 8B com 32K de contexto de ~6 GB (F16) para ~3 GB (`q8_0`) ou ~2 GB (`q4_0`). A vazão fica em KURT (2026), que mede no llama.cpp geração entre **2,83 e 9,91 tokens/s** contra processamento de prompt entre **57,39 e 92,52 tokens/s**, com a média FP16 de 69,47% caindo só 0,4% em Q4_K_S e 5,7% em Q3_K_S — **[conferir]**, porque essa medição foi feita em CPU dual Intel Xeon Platinum 8488C de 96 núcleos com AVX-512, e não em notebook, de modo que os números valem como ordem de grandeza e não como previsão para o i5-1235U. O valor de "92% mais lento em `q4_0` em contexto longo", anotado na primeira leitura, **[conferir]**: a rodada de verificação de 11/09/2026 não o encontrou na fonte de blog a que estava atribuído, e ele fica fora do relatório até ser relido. **Nada disso muda na Fase 2-B** — mudaria as condições contra a 2-A.

**O que entra no desenho** (decisão deste projeto à luz das fontes acima, não afirmação bibliográfica)**:** uma ablação barata no piso — `qwen2.5-coder:1.5b` em `q8_0` e `fp16` (tags verificadas no registro) no braço linear, 180 inferências — para saber se o 7,4% é limitação do modelo ou artefato do Q4 num modelo pequeno e supertreinado, reportando flips contra o Q4_K_M. Se mudar muito, a conclusão "1,5B é inviável" precisa de ressalva.
