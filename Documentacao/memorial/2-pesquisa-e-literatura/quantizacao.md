<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
# Pesquisa bibliográfica — Quantização

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá.

### 6.4 Quantização

Verificado nesta máquina (`ollama show`): os seis modelos comparados estão em **Q4_K_M**, a quantização padrão das tags sem sufixo.

- Lee et al. (IJCAI 2025), 1B–405B em 13 datasets: a 4 bits, **Llama-3.2-1B perde 10,1 pp** (GPTQ) ou 5,7 pp (AWQ) em média e **16,0 pp no IFEval**; **3B perde 1,8 pp** (IFEval −0,75); **8B perde 1,3–1,8 pp** (IFEval −2,1). Modelos quantizados sofrem mais em seguir instrução; só inglês foi avaliado.
- *Low-Bit Quantization Favors Undertrained LLMs* (Ouyang et al., ACL 2025), 1.500 checkpoints de 160M a 12B: **modelos pequenos com muitos tokens de treino degradam mais** — o Qwen2.5 (18T tokens) é o caso extremo, e o `1.5b` o mais exposto.
- *Accuracy is Not All You Need* (Dutta et al., NeurIPS 2024): acurácia agregada igual (±2%) esconde **até 13,6% de *flips*** — respostas que mudam de certo para errado e vice-versa. Comparar quantizações exige medir flips, não só acerto.
- *A Systematic Evaluation of On-Device LLMs* (Song et al., 2025): limiar prático em ~3,5 bits por peso; modelo maior quantizado supera modelo menor em precisão alta.
- Em CPU: i-quants (IQ*) usam *codebook* com muitas leituras de tabela e são mais lentos que k-quants; cache KV em `q8_0` é quase sem perda mas exige *flash attention*, e `q4_0` chega a 92% mais lento em contexto longo. **Nada disso muda na Fase 2-B** — mudaria as condições contra a 2-A.

**O que entra no desenho:** uma ablação barata no piso — `qwen2.5-coder:1.5b` em `q8_0` e `fp16` (tags verificadas no registro) no braço linear, 180 inferências — para saber se o 7,4% é limitação do modelo ou artefato do Q4 num modelo pequeno e supertreinado, reportando flips contra o Q4_K_M. Se mudar muito, a conclusão "1,5B é inviável" precisa de ressalva.
