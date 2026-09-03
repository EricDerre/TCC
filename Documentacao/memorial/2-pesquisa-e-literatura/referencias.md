<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
# Referências levantadas

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá.

## 9. Referências levantadas

Além das 7 do projeto de pesquisa, o levantamento produziu as seguintes, organizadas por tema. Nem todas precisam entrar no relatório; estão aqui para consulta.

### Raciocínio, CoT e modelos pequenos
- WEI, J. et al. **Chain-of-Thought Prompting Elicits Reasoning in Large Language Models**. NeurIPS, 2022. https://arxiv.org/abs/2201.11903
- SPRAGUE, Z. et al. **To CoT or not to CoT? Chain-of-thought helps mainly on math and symbolic reasoning**. ICLR, 2025. https://arxiv.org/abs/2409.12183
- LIU, R. et al. **Mind Your Step (by Step): Chain-of-Thought can Reduce Performance on Tasks where Thinking Makes Humans Worse**. ICML, 2025. https://arxiv.org/abs/2410.21333
- **Through the Valley: Path to Effective Long CoT Training for Small Language Models**. 2026. https://arxiv.org/abs/2506.07712
- ZHOU, D. et al. **Least-to-Most Prompting Enables Complex Reasoning in LLMs**. https://arxiv.org/abs/2205.10625
- WANG, L. et al. **Plan-and-Solve Prompting**. ACL, 2023. https://arxiv.org/abs/2305.04091
- KHOT, T. et al. **Decomposed Prompting: A Modular Approach for Solving Complex Tasks**. ICLR, 2023. https://arxiv.org/abs/2210.02406
- WANG, X. et al. **Self-Consistency Improves Chain of Thought Reasoning**. ICLR, 2023. https://arxiv.org/abs/2203.11171
- **Self-Consistency Is Losing Its Edge: Diminishing Returns and Rising Costs**. 2026. https://arxiv.org/html/2511.00751
- **When Self-Consistency Backfires: Majority Vote Hurts the Majority of Problems**. 2026. https://arxiv.org/abs/2608.11403

### Saída estruturada e modelos pequenos
- TAM, Z. R. et al. **Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance of LLMs**. EMNLP Industry Track, 2024. https://arxiv.org/abs/2408.02442
- **Say What You Mean: A Response to 'Let Me Speak Freely'**. dottxt, 2024. https://blog.dottxt.ai/say-what-you-mean.html *(refutação metodológica)*
- RAY, J. **The Constraint Tax: Measuring Validity-Correctness Tradeoffs in Structured Outputs for Small Language Models**. 2026. https://arxiv.org/abs/2605.26128
- **Don't Adapt Small Language Models for Tools; Adapt Tool Schemas to the Models**. ACL, 2026. https://arxiv.org/abs/2510.07248
- **Focused Chain-of-Thought: Efficient LLM Reasoning via Structured Context**. 2026. https://arxiv.org/html/2511.22176v1
- **JSONSchemaBench**. ICML, 2025. https://arxiv.org/abs/2501.10868

### Diagnóstico de falhas e automação de testes
- **LLM-Based Automated Diagnosis of Integration Test Failures at Google**. 2026. https://arxiv.org/html/2604.12108v1
- **Zero-Cost Self-Healing locator repair via accessibility tree**. 2026. https://arxiv.org/abs/2603.20358 *(baseline não-neural, 82,4% em &lt;1 s)*
- **WebTestBench**. 2026. https://arxiv.org/html/2603.25226

### Modelos e português
- **PoETa v2: benchmark de português**. 2025. https://arxiv.org/abs/2511.17808
- **P3B3: viés PT-EU vs PT-BR**. 2026. https://arxiv.org/pdf/2606.16753
- **Tucano 2**. 2026. https://arxiv.org/abs/2603.03543
- HUI, B. et al. **Qwen2.5-Coder Technical Report**. https://arxiv.org/html/2409.12186v3

### Esquecimento catastrófico e especialização
- **Interpretable Catastrophic Forgetting of LLM Fine-tuning**. 2024. https://arxiv.org/html/2406.12227v1
- **An Empirical Study of Catastrophic Forgetting in LLMs During Continual Fine-tuning**. https://arxiv.org/html/2308.08747

### Desempenho de inferência em CPU
- **Deploying LLMs on CPU-only Environments with llama.cpp**. https://ceur-ws.org/Vol-4164/paper11.pdf
- **LLM Inference Acceleration: A Hardware Perspective**. https://arxiv.org/pdf/2410.04466
- AGRAWAL, A. et al. **SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills**. 2023. https://arxiv.org/abs/2308.16369
- Ollama, issue #14780. **KV cache completely non-functional on CPU backend**. https://github.com/ollama/ollama/issues/14780
- llama.cpp, discussão #13606. **Tutorial: KV cache reuse with llama-server**. https://github.com/ggml-org/llama.cpp/discussions/13606

### Documentação como contexto, RAG e recuperação (Fase 2-B)
- LIU, N. F. et al. **Lost in the Middle: How Language Models Use Long Contexts**. TACL, v. 12, 2024. https://aclanthology.org/2024.tacl-1.9/
- HONG, K.; TROYNIKOV, A.; HUBER, J. **Context Rot: How Increasing Input Tokens Impacts LLM Performance**. Chroma, 2025. https://www.trychroma.com/research/context-rot
- MARTIN, S.; ROGER, F. **Classifier Context Rot: Monitor Performance Degrades with Context Length**. 2026. https://arxiv.org/abs/2605.12366
- LI, X. et al. **Long Context vs. RAG for LLMs: An Evaluation and Revisits**. 2024. https://arxiv.org/abs/2501.01880
- CUCONASU, F. et al. **The Power of Noise: Redefining Retrieval for RAG Systems**. SIGIR, 2024. https://arxiv.org/abs/2401.14887
- MAZURYK, M. et al. **The Powerless Noise: How Experimental Settings Shape the Reported Power of Noise**. SIGIR, 2026. https://arxiv.org/abs/2607.03615
- LI, Y. et al. **Investigating Context-Faithfulness in Large Language Models: The Roles of Memory Strength and Evidence Style**. ACL, 2025. https://arxiv.org/abs/2409.10955
- XU, R. et al. **Knowledge Conflicts for LLMs: A Survey**. EMNLP, 2024. https://arxiv.org/abs/2403.08319
- **From BM25 to Corrective RAG: Benchmarking Retrieval Strategies for Text-and-Table Documents**. 2026. https://arxiv.org/html/2604.01733v1
- **Rethinking Chunk Size for Long-Document Retrieval: A Multi-Dataset Analysis**. 2025. https://arxiv.org/pdf/2505.21700
- STEKEL, T. R. C. **MTEB-BR: A Text Embedding Benchmark for Brazilian Portuguese**. 2026. https://arxiv.org/abs/2607.04581
- HE, J. et al. **Does Prompt Formatting Have Any Impact on LLM Performance?** 2024. https://arxiv.org/abs/2411.10541
- DIETTERICH, T. G. **Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms**. Neural Computation, v. 10, n. 7, p. 1895–1923, 1998.

### Quantização
- LEE, J. et al. **Exploring the Trade-Offs: Quantization Methods, Task Difficulty, and Model Size in Large Language Models From Edge to Giant**. IJCAI, 2025. https://arxiv.org/abs/2409.11055
- OUYANG, X. et al. **Low-Bit Quantization Favors Undertrained LLMs: Scaling Laws for Quantized LLMs with 100T Training Tokens**. ACL, 2025. https://arxiv.org/abs/2411.17691
- DUTTA, A. et al. **Accuracy is Not All You Need**. NeurIPS, 2024. https://arxiv.org/abs/2407.09141
- SONG, Q. et al. **A Systematic Evaluation of On-Device LLMs: Quantization, Performance, and Resources**. 2025. https://arxiv.org/abs/2505.15030
- KUSAMA, K. et al. **How Small is Enough? Empirical Evidence of Quantized Small Language Models for Automated Program Repair**. ESEM, 2025. https://arxiv.org/abs/2508.16499
