<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
<!-- ! Alteração de IA - Revisar: revisão de 11/09/2026 — acrescentadas as referências da rodada
     de pesquisa de 11/09/2026 em cinco blocos novos (fontes brasileiras e o livro-texto,
     tokenização e arquitetura, memória gerida pelo modelo, métricas e desenho experimental,
     self-healing e contrato) e nos blocos já existentes de RAG, quantização e raciocínio, sem
     repetir as que já constavam; entradas que estavam incompletas (BEIR, PoETa v2, Tucano 2,
     o baseline não-neural e o benchmark BM25) ganharam autor, ano e veículo; e as fontes que
     o verificador marcou como de suporte parcial receberam a marca
     *(suporte parcial - conferir)*.
     ! Motivo: este arquivo é de onde as referências saem para o relatório final, e havia
     entradas sem autor ("PoETa v2: benchmark de português", "Zero-Cost Self-Healing locator
     repair via accessibility tree") que não dão para transcrever em ABNT. A marca de suporte
     parcial existe porque a rodada de verificação encontrou, nessas fontes, número ou condição
     divergente do que o resumo preliminar dizia - copiar a referência sem a marca faria o
     número errado voltar ao texto. -->
# Referências levantadas

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá. A íntegra das sínteses que produziram as referências de 11/09/2026, com a condição de cada medição e as lacunas de cada tópico, está em [levantamento-2026-09-11-fase-3.md](levantamento-2026-09-11-fase-3.md).

## 9. Referências levantadas

Além das 7 do projeto de pesquisa, o levantamento produziu as **175** referências abaixo, organizadas por tema. Nem todas precisam entrar no relatório; estão aqui para consulta.

Duas convenções de leitura. A marca *(suporte parcial — conferir)* indica fonte em que a rodada de verificação de 11/09/2026 confirmou a afirmação mas corrigiu o número, a condição de medição ou a atribuição de autoria — a correção está escrita no parágrafo correspondente do [levantamento](levantamento-2026-09-11-fase-3.md), e a referência não deve ir ao relatório final sem essa leitura. As entradas seguem o formato de trabalho deste arquivo (sobrenome, iniciais, título em negrito, veículo, ano e URL), não o ABNT completo; a versão ABNT de cada uma das referências de 11/09/2026 está no levantamento.

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
- LI, Y. et al. **Small Models Struggle to Learn from Strong Reasoners**. Findings of ACL, 2025. https://arxiv.org/abs/2502.12143 *(suporte parcial — conferir)*

### Saída estruturada e modelos pequenos
- TAM, Z. R. et al. **Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance of LLMs**. EMNLP Industry Track, 2024. p. 1218-1236. https://arxiv.org/abs/2408.02442 *(suporte parcial — conferir)*
- **Say What You Mean: A Response to 'Let Me Speak Freely'**. dottxt, 2024. https://blog.dottxt.ai/say-what-you-mean.html *(refutação metodológica)*
- RAY, J. **The Constraint Tax: Measuring Validity-Correctness Tradeoffs in Structured Outputs for Small Language Models**. 2026. https://arxiv.org/abs/2605.26128
- **Don't Adapt Small Language Models for Tools; Adapt Tool Schemas to the Models**. ACL, 2026. https://arxiv.org/abs/2510.07248 *(citado na §6.2 como "PA-Tool")*
- **Focused Chain-of-Thought: Efficient LLM Reasoning via Structured Context**. 2026. https://arxiv.org/html/2511.22176v1 *(citado na §6.2 como "F-CoT")*
- GENG, S. et al. **JSONSchemaBench: A Rigorous Benchmark of Structured Outputs for Language Models**. 2025. https://arxiv.org/abs/2501.10868 *(suporte parcial — conferir)*

### Diagnóstico de falhas e automação de testes
- **LLM-Based Automated Diagnosis of Integration Test Failures at Google**. 2026. https://arxiv.org/html/2604.12108v1
- JOSEPH, R. N. **Beyond LLM-based test automation: a zero-cost self-healing approach using DOM accessibility tree extraction**. arXiv preprint arXiv:2603.20358 [cs.SE], 2026. https://arxiv.org/abs/2603.20358 *(baseline não-neural: 31/31 testes, seletor obsoleto redescoberto em &lt;1 s, custo de API zero; os 82,4% anotados na primeira leitura não constam das afirmações verificadas — conferir no artigo)*
- **WebTestBench**. 2026. https://arxiv.org/html/2603.25226

### Modelos e português
- ALMEIDA, T. S.; PIRES, R.; ABONIZIO, H.; NOGUEIRA, R.; PEDRINI, H. **PoETa v2: Toward More Robust Evaluation of Large Language Models in Portuguese**. 2025. https://arxiv.org/abs/2511.17808
- **P3B3: viés PT-EU vs PT-BR**. 2026. https://arxiv.org/pdf/2606.16753
- CORRÊA, N. K.; SEN, A.; FATIMAH, S.; FALK, S.; LANDGRAF, L.; KASTNER, J.; FLEK, L. **Tucano 2 Cool: Better Open Source LLMs for Portuguese**. arXiv, 2026. https://arxiv.org/abs/2603.03543 *(suporte parcial — conferir: o valor de 2,68 caracteres/token é do Qwen3-0.6B, e não dos três modelos listados — Llama-3.2-1B, SmolLM3-3B-Base e OLMo-2-0425-1B, que ficam em 2,72, 2,72 e 2,71)*
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
- CUCONASU, F. et al. **The Power of Noise: Redefining Retrieval for RAG Systems**. SIGIR, 2024. p. 719-729. https://arxiv.org/abs/2401.14887 *(suporte parcial — conferir)*
- MAZURYK, M. et al. **The Powerless Noise: How Experimental Settings Shape the Reported Power of Noise**. SIGIR, 2026. https://arxiv.org/abs/2607.03615
- LI, Y. et al. **Investigating Context-Faithfulness in Large Language Models: The Roles of Memory Strength and Evidence Style**. ACL, 2025. https://arxiv.org/abs/2409.10955
- XU, R. et al. **Knowledge Conflicts for LLMs: A Survey**. EMNLP, 2024. https://arxiv.org/abs/2403.08319
- AKARSU, M.; KARAMAN, R. K.; MIERBACH, C. **From BM25 to Corrective RAG: Benchmarking Retrieval Strategies for Text-and-Table Documents**. 2026. https://arxiv.org/abs/2604.01733
- **Rethinking Chunk Size for Long-Document Retrieval: A Multi-Dataset Analysis**. 2025. https://arxiv.org/pdf/2505.21700
- STEKEL, T. R. C. **MTEB-BR: A Text Embedding Benchmark for Brazilian Portuguese**. 2026. https://arxiv.org/abs/2607.04581
- HE, J. et al. **Does Prompt Formatting Have Any Impact on LLM Performance?** 2024. https://arxiv.org/abs/2411.10541
- DIETTERICH, T. G. **Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms**. Neural Computation, v. 10, n. 7, p. 1895–1923, 1998.

- ASAI, A.; WU, Z.; WANG, Y.; SIL, A.; HAJISHIRZI, H. **Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection**. ICLR, 2024. https://arxiv.org/abs/2310.11511
- ES, S.; JAMES, J.; ESPINOSA ANKE, L.; SCHOCKAERT, S. **RAGAs: Automated Evaluation of Retrieval Augmented Generation**. EACL System Demonstrations, 2024. p. 150-158. https://aclanthology.org/2024.eacl-demo.16/
- JEONG, S. et al. **Adaptive-RAG: Learning to Adapt Retrieval-Augmented Large Language Models through Question Complexity**. NAACL-HLT, 2024. p. 7036-7050. https://aclanthology.org/2024.naacl-long.389/
- LI, Z.; LI, C.; ZHANG, M.; MEI, Q.; BENDERSKY, M. **Retrieval Augmented Generation or Long-Context LLMs? A Comprehensive Study and Hybrid Approach**. EMNLP Industry Track, 2024. p. 881-893. https://aclanthology.org/2024.emnlp-industry.66/ *(suporte parcial — conferir)*
- MODARRESSI, A. et al. **NoLiMa: Long-Context Evaluation Beyond Literal Matching**. ICML, PMLR v. 267, p. 44554-44570, 2025. https://proceedings.mlr.press/v267/modarressi25a.html
- PAN, Z. et al. **LLMLingua-2: Data Distillation for Efficient and Faithful Task-Agnostic Prompt Compression**. Findings of ACL, 2024. p. 963-981. https://aclanthology.org/2024.findings-acl.57/
- PANDEY, S. **Can Small Language Models Use What They Retrieve? An Empirical Study of Retrieval Utilization Across Model Scale**. 2026. https://arxiv.org/abs/2603.11513
- QU, R.; TU, R.; BAO, F. S. **Is Semantic Chunking Worth the Computational Cost?**. Findings of NAACL, 2025. p. 2155-2177. https://aclanthology.org/2025.findings-naacl.114/
- RU, D. et al. **RAGChecker: a fine-grained framework for diagnosing retrieval-augmented generation**. NeurIPS Datasets and Benchmarks Track, 2024. https://proceedings.neurips.cc/paper_files/paper/2024/hash/27245589131d17368cccdfa990cbf16e-Abstract-Datasets_and_Benchmarks_Track.html
- SAAD-FALCON, J.; KHATTAB, O.; POTTS, C.; ZAHARIA, M. **ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems**. NAACL-HLT, 2024. p. 338-354. https://aclanthology.org/2024.naacl-long.20/
- THAKUR, N. et al. **BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models**. NeurIPS Datasets and Benchmarks Track, 2021. https://arxiv.org/abs/2104.08663
- WANG, F.; WAN, X.; SUN, R.; CHEN, J.; ARIK, S. Ö. **Astute RAG: Overcoming Imperfect Retrieval Augmentation and Knowledge Conflicts for Large Language Models**. ACL, 2025. https://aclanthology.org/2025.acl-long.1476/
- WU, K.; WU, E.; ZOU, J. **ClashEval: Quantifying the tug-of-war between an LLM's internal prior and external evidence**. NeurIPS Datasets and Benchmarks Track, 2024. https://arxiv.org/abs/2404.10198
- YAN, S.-Q.; GU, J.-C.; ZHU, Y.; LING, Z.-H. **Corrective Retrieval Augmented Generation**. 2024. https://arxiv.org/abs/2401.15884
- YU, T.; XU, A.; AKKIRAJU, R. **In Defense of RAG in the Era of Long-Context Language Models**. 2024. https://arxiv.org/abs/2409.01666 *(suporte parcial — conferir)*
- ZOU, W.; GENG, R.; WANG, B.; JIA, J. **PoisonedRAG: Knowledge Corruption Attacks to Retrieval-Augmented Generation of Large Language Models**. USENIX Security '25, 2025. p. 3827-3844. https://www.usenix.org/conference/usenixsecurity25/presentation/zou-poisonedrag

### Quantização
- LEE, J. et al. **Exploring the Trade-Offs: Quantization Methods, Task Difficulty, and Model Size in Large Language Models From Edge to Giant**. IJCAI, 2025. https://arxiv.org/abs/2409.11055
- OUYANG, X. et al. **Low-Bit Quantization Favors Undertrained LLMs: Scaling Laws for Quantized LLMs with 100T Training Tokens**. ACL, 2025. https://arxiv.org/abs/2411.17691
- DUTTA, A. et al. **Accuracy is Not All You Need**. NeurIPS, 2024. https://arxiv.org/abs/2407.09141
- SONG, Q. et al. **A Systematic Evaluation of On-Device LLMs: Quantization, Performance, and Resources**. 2025. https://arxiv.org/abs/2505.15030 *(suporte parcial — conferir)*
- KUSAMA, K. et al. **How Small is Enough? Empirical Evidence of Quantized Small Language Models for Automated Program Repair**. ESEM, 2025. https://arxiv.org/abs/2508.16499
- KURT, U. **Which Quantization Should I Use? A Unified Evaluation of llama.cpp Quantization on Llama-3.1-8B-Instruct**. 2026. https://arxiv.org/abs/2601.14277 *(suporte parcial — conferir)*
- MCLEOD, S. **Bringing K/V Context Quantisation to Ollama**. smcleod.net, 4 dez. 2024. https://smcleod.net/2024/12/bringing-k/v-context-quantisation-to-ollama/
- OOBABOOGA. **Gemma 4 and Qwen 3.6 with q8_0 and q4_0 KV cache: KL divergence results**. LocalBench (Substack), 2026. https://localbench.substack.com/p/kv-cache-quantization-benchmark *(suporte parcial — conferir)*

### Fontes brasileiras e o livro-texto (levantamento de 11/09/2026)
- FACELI, K.; LORENA, A. C.; GAMA, J.; ALMEIDA, T. A. de; CARVALHO, A. C. P. L. F. de. **Inteligência artificial: uma abordagem de aprendizado de máquina**. 3. ed. Rio de Janeiro: LTC (Grupo GEN), 2025. 376 p. ISBN 9788521639206. https://www.grupogen.com.br/livro-inteligencia-artificial-uma-abordagem-de-aprendizado-de-maquina-katti-faceli-ana-carolina-lorena-joao-gama-tiago-a-de-almeida-e-andre-c-p-l-f-de-carvalho-editora-ltc-9788521639206 *(livro-texto orientador do TCC; a 2. ed., de 2021, ISBN 9788521637349, 400 p., ainda circula em catálogos de biblioteca e no varejo — citar a 3. ed. O mapeamento capítulo-a-tema usado nas §6.1 a §6.8 vem do sumário, não do exemplar)*
- CENTRO DE CIÊNCIAS EM GESTÃO E TECNOLOGIA (CCGT). **Professores do CCGT lançam 3ª edição do livro "Inteligência Artificial – Uma Abordagem de Aprendizado de Máquina"**. Sorocaba: UFSCar, 2025. https://www.ccgt.ufscar.br/pt-br/professores-do-ccgt-lancam-3a-edicao-do-livro-inteligencia-artificial-uma-abordagem-de-aprendizado-de-maquina *(suporte parcial — conferir)*
- ABONIZIO, H. et al. **Sabiá-3 Technical Report**. 2024. https://arxiv.org/abs/2410.12049 *(suporte parcial — conferir)*
- LAITZ, T. et al. **Sabiá-4 Technical Report**. 2026. https://arxiv.org/abs/2603.10213
- ASSIS, G.; FREITAS, C.; PAES, A. **Exploring Brazil's LLM Fauna: Investigating the Generative Performance of Large Language Models in Portuguese**. JBCS, v. 31, 2025. https://journals-sol.sbc.org.br/index.php/jbcs/article/view/5814 *(suporte parcial — conferir)*
- CATTAI, L.; BALDASSIN, A.; DANTAS, A. **Otimização de Inferência em LLMs na CPU: Análise do Cenário Atual**. ERAD-SP, 2025. p. 78-81. https://sol.sbc.org.br/index.php/eradsp/article/view/36423
- CORRÊA, N. K.; FALK, S.; FATIMAH, S.; SEN, A.; OLIVEIRA, N. de. **TeenyTinyLlama: open-source tiny language models trained in Brazilian Portuguese**. Machine Learning with Applications, v. 16, art. 100558, 2024. https://arxiv.org/abs/2401.16640
- CORRÊA, N. K.; SEN, A.; FALK, S.; FATIMAH, S. **Tucano: Advancing Neural Text Generation for Portuguese**. Patterns, v. 6, n. 11, 2025 (preprint arXiv:2411.07854, 2024). https://arxiv.org/abs/2411.07854
- CRUZ-CASTAÑEDA, W. A.; AMADEUS, M. **Large Languages Models in Brazilian Portuguese: A Chronological Survey**. JBCS, v. 31, n. 1, 2025. https://journals-sol.sbc.org.br/index.php/jbcs/article/view/5789 *(suporte parcial — conferir)*
- FINARDI, P. et al. **The Chronicles of RAG: The Retriever, the Chunk and the Generator**. 2024. https://arxiv.org/abs/2401.07883
- GARCIA, G. L.; PAIOLA, P. H.; GARCIA, E.; MANESCO, J. R. R.; PAPA, J. P. **GemBode and PhiBode: Adapting Small Language Models to Brazilian Portuguese**. CIARP, LNCS, 2024. p. 228-243. https://doi.org/10.1007/978-3-031-76607-7_17
- MEDEIROS, L. S. F.; OLIVEIRA, H. T. A. de. **Comparação de Modelos de Embeddings e LLMs para Geração Aumentada por Recuperação em Português**. SEMISH 52, 2025. p. 429-440. https://sol.sbc.org.br/index.php/semish/article/view/36829
- SANTOS, J. G. A.; BONÁS, G. K.; LAITZ, T.; ALMEIDA, T. S.; PEDRINI, H. **BLUEX v2: Benchmarking LLMs on Open-Ended Questions from Brazilian University Entrance Exams**. 2026. https://arxiv.org/abs/2606.22723
- SCHUCK, A. da F.; GARCIA, G. L.; MANESCO, J. R. R.; PAIOLA, P. H.; PAPA, J. P. **Evaluating Large Language Models for Brazilian Portuguese Sentiment Analysis**. JBCS, v. 31, n. 1, 2025. https://journals-sol.sbc.org.br/index.php/jbcs/article/view/5793
- SILVA, E. C. O.; COELHO, R. de S.; SILVA, L. F. da. **LLMs as Test Generators: A Comparative Benchmarking Study**. SBES 39, 2025. https://sol.sbc.org.br/index.php/sbes/article/view/36983
- SILVA, J.; GOMES, L.; BRANCO, A. **CLARIN-PT-LDB: An Open LLM Leaderboard for Portuguese to assess Language, Culture and Civility**. PROPOR, 2026. p. 67-77. https://aclanthology.org/2026.propor-1.7/

### Tokenização e arquitetura (levantamento de 11/09/2026)
- ABDIN, M. et al. **Phi-3 Technical Report: A Highly Capable Language Model Locally on Your Phone**. 2024. https://arxiv.org/abs/2404.14219
- AHIA, O. et al. **Do All Languages Cost the Same? Tokenization in the Era of Commercial Language Models**. EMNLP, 2023. p. 9904-9923. https://aclanthology.org/2023.emnlp-main.614/
- AINSLIE, J. et al. **GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints**. EMNLP, 2023. p. 4895-4901. https://arxiv.org/abs/2305.13245
- BAI, TJ; EISNER, J. **Accelerating Language Model Workflows with Prompt Choreography**. TACL, 2025 (no prelo). https://arxiv.org/abs/2512.23049
- CHURCHILL, G.; SKIENA, S. **Reducing Tokenization Premiums for Low-Resource Languages**. 2026. https://arxiv.org/abs/2601.13328
- DAGAN, G.; SYNNAEVE, G.; ROZIÈRE, B. **Getting the most out of your tokenizer for pre-training and domain adaptation**. ICML, PMLR v. 235, p. 9784-9805, 2024. https://proceedings.mlr.press/v235/dagan24a.html
- DONG, Y. et al. **XGrammar: Flexible and Efficient Structured Generation Engine for Large Language Models**. MLSys, 2025. https://arxiv.org/abs/2411.15100 *(suporte parcial — conferir)*
- GEMMA TEAM; KAMATH, A. et al. **Gemma 3 Technical Report**. 2025. https://arxiv.org/abs/2503.19786 *(suporte parcial — conferir)*
- GERGANOV, G.; CONTRIBUIDORES DO PROJETO LLAMA.CPP. **GBNF Guide (grammars/README.md)**. Documentação oficial do llama.cpp, branch master, 2025a. https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md
- GERGANOV, G.; CONTRIBUIDORES DO PROJETO LLAMA.CPP. **llama.cpp HTTP Server (tools/server/README.md)**. Documentação oficial do llama.cpp, branch master, 2025b. https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
- GOPE, D.; MANSELL, D.; LOH, D.; BRATT, I. **Highly Optimized Kernels and Fine-Grained Codebooks for LLM Inference on Arm CPUs**. 2024. https://arxiv.org/abs/2501.00032
- GRANITE TEAM, IBM. **Granite 3.0 Language Models**. Relatório técnico. Armonk: IBM Research, 2024. https://github.com/ibm-granite/granite-3.0-language-models *(suporte parcial — conferir)*
- GRATTAFIORI, A. et al. (Llama Team, AI @ Meta). **The Llama 3 Herd of Models**. 2024. https://arxiv.org/abs/2407.21783
- HAN, T. et al. **Token-Budget-Aware LLM Reasoning**. Findings of ACL, 2025. p. 24842-24855. https://aclanthology.org/2025.findings-acl.1274/ *(suporte parcial — conferir)*
- JI, J.; KUMAR, R. **Gemma explained: What's new in Gemma 3**. Google Developers Blog, 2025. https://developers.googleblog.com/en/gemma-explained-whats-new-in-gemma-3/ *(suporte parcial — conferir)*
- KULIGOWSKI, A. (akuligowski9). **Chat history and embedding truncation happens silently with no user-visible indication**. GitHub, ollama/ollama, Issue #14259, 14 fev. 2026. https://github.com/ollama/ollama/issues/14259 *(suporte parcial — conferir)*
- LASKARIDIS, S.; KATEVAS, K.; MINTO, L.; HADDADI, H. **MELTing point: Mobile Evaluation of Language Transformers**. ACM MobiCom, 2024. https://arxiv.org/abs/2403.12844
- LOTZ, J. F. et al. **Beyond Text Compression: Evaluating Tokenizers Across Scales**. ACL, 2025. https://aclanthology.org/2025.acl-long.1546/
- LU, Z. et al. **Small Language Models: Survey, Measurements, and Insights**. 2024. https://arxiv.org/abs/2409.15790 *(suporte parcial — conferir)*
- MIND-TERCERO-ROLDAN. **[Tutorial] Mastering Host-Memory Prompt Caching in llama-server (Discussion #20574)**. GitHub: ggml-org/llama.cpp, 2026. https://github.com/ggml-org/llama.cpp/discussions/20574 *(suporte parcial — conferir)*
- NAYEEM, M. T. et al. **Beyond Fertility: Analyzing STRR as a Metric for Multilingual Tokenization Evaluation**. NeurIPS Workshop, 2025. https://arxiv.org/abs/2510.09947 *(suporte parcial — conferir)*
- OLLAMA. **Context length**. Documentação oficial, 2025. https://docs.ollama.com/context-length *(suporte parcial — conferir)*
- OLLAMA. **FAQ**. Documentação oficial, 2026. https://docs.ollama.com/faq
- OLLAMA. **Structured outputs**. Ollama Blog, 6 dez. 2024. https://ollama.com/blog/structured-outputs *(suporte parcial — conferir)*
- OPENAI. **Counting tokens**. OpenAI API Guides, 2025. https://developers.openai.com/api/docs/guides/token-counting *(complementar: **What are tokens and how to count them?**, OpenAI Help Center, 2025; suporte parcial — conferir)*
- QWEN TEAM (Alibaba Cloud). **Key Concepts**. Qwen Documentation (v2.5), 2024. https://qwen.readthedocs.io/en/v2.5/getting_started/concepts.html
- REIF, Y.; SCHWARTZ, R. **Beyond Performance: Quantifying and Mitigating Label Bias in LLMs**. NAACL, 2024. p. 6784-6798. https://aclanthology.org/2024.naacl-long.378/
- RENZE, M.; GUVEN, E. **The Effect of Sampling Temperature on Problem Solving in Large Language Models**. Findings of EMNLP, 2024. p. 7346-7356. https://aclanthology.org/2024.findings-emnlp.432/
- ROY, A.; ROY, P.; PATEL, H. **Measuring the Tokenization Premium: A Cost Audit for Underserved Language Communities**. 2026. https://arxiv.org/abs/2608.09046
- TAO, C. et al. **Scaling Laws with Vocabulary: Larger Models Deserve Larger Vocabularies**. NeurIPS, 2024. https://arxiv.org/abs/2407.13623
- TURGUTLU, K.; KARPATHY, A. **Let's Build the GPT Tokenizer: A Complete Guide to Tokenization in LLMs**. fast.ai, 2025. https://www.fast.ai/posts/2025-10-16-karpathy-tokenizers.html *(suporte parcial — conferir)*
- YANG, A. et al. **Qwen2.5 Technical Report**. 2024. https://arxiv.org/abs/2412.15115
- ZHANG, Y.; DAS, S. S. S.; ZHANG, R. **Verbosity ≠ Veracity: Demystify Verbosity Compensation Behavior of Large Language Models**. UncertaiNLP, 2025. p. 168-190. https://aclanthology.org/2025.uncertainlp-main.14/
- ZHAO, J.; LI, J.; WU, C. **Sandwich: Joint Configuration Search and Hot-Switching for Efficient CPU LLM Serving**. DAC '26, 2026. https://arxiv.org/abs/2507.18454
- ZHENG, L. et al. **SGLang: Efficient Execution of Structured Language Model Programs**. NeurIPS, 2024. https://proceedings.neurips.cc/paper_files/paper/2024/file/724be4472168f31ba1c9ac630f15dec8-Paper-Conference.pdf *(suporte parcial — conferir)*

### Memória gerida pelo modelo (levantamento de 11/09/2026)
- CHEN, J. et al. **Rethinking Continual Experience Internalization for Self-Evolving LLM Agents**. 2026. https://arxiv.org/abs/2606.04703 *(suporte parcial — conferir)*
- CHHIKARA, P.; KHANT, D.; ARYAN, S.; SINGH, T.; YADAV, D. **Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory**. 2025. https://arxiv.org/abs/2504.19413 *(suporte parcial — conferir)*
- COCHRAN, T. O. **Progressive Disclosure for LLM-Maintained Wiki Knowledge Bases: a Preregistered Ablation**. 2026. https://arxiv.org/abs/2607.04576
- OUYANG, S. et al. **ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory**. 2025. https://arxiv.org/abs/2509.25140
- OUYANG, S. et al. **SkillOS: Learning Skill Curation for Self-Evolving Agents**. 2026. https://arxiv.org/abs/2605.06614 *(suporte parcial — conferir)*
- SHAO, S. et al. **Your Agent May Misevolve: Emergent Risks in Self-evolving LLM Agents**. 2025. https://arxiv.org/abs/2509.26354
- SHUMAILOV, I. et al. **AI models collapse when trained on recursively generated data**. Nature, v. 631, n. 8022, p. 755-759, 2024. https://www.nature.com/articles/s41586-024-07566-y
- SUZGUN, M.; YUKSEKGONUL, M.; BIANCHI, F.; JURAFSKY, D.; ZOU, J. **Dynamic Cheatsheet: Test-Time Learning with Adaptive Memory**. 2025. https://arxiv.org/abs/2504.07952
- WANG, G. et al. **Voyager: An Open-Ended Embodied Agent with Large Language Models**. 2023. https://arxiv.org/abs/2305.16291
- WANG, X. et al. **Towards Reliable, Generalizable, and Specific In-Context Knowledge Editing via Multi-Objective Reinforcement Learning**. 2026. https://arxiv.org/abs/2608.25100 *(suporte parcial — conferir)*
- WANG, Z.; MAO, J.; FRIED, D.; NEUBIG, G. **Agent Workflow Memory**. 2024. https://arxiv.org/abs/2409.07429 *(suporte parcial — conferir)*
- XIANG, Z. et al. **MemSyco-Bench: Benchmarking Sycophancy in Agent Memory**. 2026. https://arxiv.org/abs/2607.01071
- XIONG, Z. et al. **How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following Behavior**. ACL, 2026. https://aclanthology.org/2026.acl-long.27/
- XU, W.; LIANG, Z.; MEI, K.; GAO, H.; TAN, J.; ZHANG, Y. **A-MEM: Agentic Memory for LLM Agents**. NeurIPS, 2025. https://arxiv.org/abs/2502.12110
- ZHANG, G. et al. **Adaptive Memory Admission Control for LLM Agents**. 2026. https://arxiv.org/abs/2603.04549
- ZHANG, Q. et al. **Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models**. 2025. https://arxiv.org/abs/2510.04618 *(suporte parcial — conferir)*
- ZHAO, A.; HUANG, D.; XU, Q.; LIN, M.; LIU, Y.-J.; HUANG, G. **ExpeL: LLM Agents Are Experiential Learners**. AAAI, v. 38, n. 17, p. 19632-19642, 2024. https://arxiv.org/abs/2308.10144 *(suporte parcial — conferir)*
- ZHAO, W. et al. **Large Language Model Agents Are Not Always Faithful Self-Evolvers**. 2026. https://arxiv.org/abs/2601.22436 *(suporte parcial — conferir)*

### Métricas e desenho experimental (levantamento de 11/09/2026)
- WILSON, E. B. **Probable inference, the law of succession, and statistical inference**. Journal of the American Statistical Association, v. 22, n. 158, p. 209-212, 1927.
- COHEN, J. **Statistical power analysis for the behavioral sciences**. 2. ed. New York: Routledge, 1988. *(suporte parcial — conferir)*
- DEMŠAR, J. **Statistical Comparisons of Classifiers over Multiple Data Sets**. JMLR, v. 7, p. 1-30, 2006. https://www.jmlr.org/papers/v7/demsar06a.html
- GARCÍA, S.; HERRERA, F. **An Extension on "Statistical Comparisons of Classifiers over Multiple Data Sets" for all Pairwise Comparisons**. JMLR, v. 9, p. 2677-2694, 2008. https://www.jmlr.org/papers/volume9/garcia08a/garcia08a.pdf *(suporte parcial — conferir)*
- SILLA JR., C. N.; FREITAS, A. A. **A survey of hierarchical classification across different application domains**. Data Mining and Knowledge Discovery, v. 22, n. 1-2, p. 31-72, 2011. https://doi.org/10.1007/s10618-010-0175-9 *(suporte parcial — conferir)*
- RASCHKA, S. **Model Evaluation, Model Selection, and Algorithm Selection in Machine Learning**. 2018 (v3, 2020). https://arxiv.org/abs/1811.12808
- CARD, D. et al. **With Little Power Comes Great Responsibility**. EMNLP, 2020. p. 9263-9274. https://aclanthology.org/2020.emnlp-main.745/ *(suporte parcial — conferir)*
- SCLAR, M.; CHOI, Y.; TSVETKOV, Y.; SUHR, A. **Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design**. ICLR, 2024. https://arxiv.org/abs/2310.11324
- OPITZ, J. **A Closer Look at Classification Evaluation Metrics and a Critical Reflection of Common Evaluation Practice**. TACL, v. 12, p. 820-836, 2024. https://aclanthology.org/2024.tacl-1.46/
- PLAUD, R.; LABEAU, M.; SAILLENFEST, A.; BONALD, T. **Revisiting Hierarchical Text Classification: Inference and Metrics**. CoNLL, 2024. https://arxiv.org/abs/2410.01305 *(suporte parcial — conferir)*
- BEN-SHACHAR, M. S. et al. **cohens_g: Effect Size for Paired Contingency Tables**. Documentação do pacote effectsize (easystats/CRAN), 2024. https://easystats.github.io/effectsize/reference/cohens_g.html *(suporte parcial — conferir)*
- MANGIAFICO, S. S. **cohenG: Cohen's g and odds ratio for paired contingency tables**. Manual do pacote rcompanion (CRAN), 2024. https://rdrr.io/cran/rcompanion/man/cohenG.html *(suporte parcial — conferir)*
- BOWYER, S.; AITCHISON, L.; IVANOVA, D. R. **Position: Don't Use the CLT in LLM Evals With Fewer Than a Few Hundred Datapoints**. ICML, 2025. https://arxiv.org/abs/2503.01747
- HE, H.; THINKING MACHINES LAB. **Defeating Nondeterminism in LLM Inference**. Thinking Machines Lab: Connectionism, 2025. https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/ *(suporte parcial — conferir)*
- BALTES, S. et al. **Guidelines for Empirical Studies in Software Engineering involving Large Language Models**. Empirical Software Engineering (aceito), 2025/2026. https://arxiv.org/abs/2508.15503
- LEE, C.; ZENG, T.; JEONG, J.; SOHN, J.; LEE, K. **How to Correctly Report LLM-as-a-Judge Evaluations**. ICML, 2026 (preprint arXiv:2511.21140, 2025). https://arxiv.org/abs/2511.21140
- MLCOMMONS et al. **MLPerf Inference v5.0 Advances Language Model Capabilities for GenAI**. MLCommons Blog, 2025. https://mlcommons.org/2025/04/llm-inference-v5/ *(suporte parcial — conferir)*
- COLLOT, S. et al. **Balanced Accuracy: The Right Metric for Evaluating LLM Judges — Explained through Youden's J statistic**. EACL Industry Track, 2026. p. 927-936. https://aclanthology.org/2026.eacl-industry.69/
- KOTAWALA, A. **Resolution Diagnostics for Paired LLM Evaluation**. 2026. https://arxiv.org/abs/2605.30315
- LIN, J. **Self-Improvement Can Self-Regress: The Rise-and-Collapse Failure Mode of LLM Self-Training**. 2026. https://arxiv.org/abs/2606.21090
- NORMAN, J. D.; RIVERA, M. U.; HUGHES, D. A. **Reliability without Validity: A Systematic, Large-Scale Evaluation of LLM-as-a-Judge Models Across Agreement, Consistency, and Bias**. 2026. https://arxiv.org/abs/2606.19544

### Self-healing, árvore de acessibilidade e contrato (levantamento de 11/09/2026)
- XAVIER, L.; BRITO, A.; HORA, A.; VALENTE, M. T. **Historical and impact analysis of API breaking changes: a large-scale study**. SANER, 2017. p. 138-147. https://ieeexplore.ieee.org/document/7884616/ *(suporte parcial — conferir)*
- STOCCO, A.; YANDRAPALLY, R.; MESBAH, A. **Visual web test repair**. ESEC/FSE, 2018. p. 503-514. https://dl.acm.org/doi/10.1145/3236024.3236063
- DECROP, A.; DEVROEY, X.; PAPADAKIS, M.; SCHOBBENS, P.-Y.; PERROUIN, G. **You Can REST Now: Automated REST API Documentation and Testing via LLM-Assisted Request Mutations**. 2024. https://arxiv.org/abs/2402.05102
- RICCA, F.; MARCHETTO, A.; STOCCO, A. **A Multi-Year Grey Literature Review on AI-assisted Test Automation**. 2024. https://arxiv.org/abs/2408.06224
- ZHOU, S. et al. **WebArena: A Realistic Web Environment for Building Autonomous Agents**. ICLR, 2024. https://arxiv.org/abs/2307.13854
- YANG, K. et al. **AgentOccam: A Simple Yet Strong Baseline for LLM-Based Web Agents**. ICLR, 2025. https://arxiv.org/abs/2410.13825
- SONG, Y.; XU, F. F.; ZHOU, S.; NEUBIG, G. **Beyond Browsing: API-Based Web Agents**. Findings of ACL, 2025. p. 11066-11085. https://arxiv.org/abs/2410.16464
- KERBOUA, I. et al. **FocusAgent: Simple Yet Effective Ways of Trimming the Large Context of Web Agents**. 2025. https://arxiv.org/abs/2510.03204 *(suporte parcial — conferir)*
- XUE, T. et al. **An Illusion of Progress? Assessing the Current State of Web Agents**. COLM, 2025. https://arxiv.org/abs/2504.01382
- FATIN, S. et al. **LELANTE: LEveraging LLM for Automated ANdroid TEsting**. 2025. https://arxiv.org/abs/2504.20896 *(suporte parcial — conferir)*
- VARDANYAN, A. **Building Browser Agents: Architecture, Security, and Practical Solutions**. 2025. https://arxiv.org/abs/2511.19477
- ENOMOTO, M.; OBARA, R.; ZHANG, H.; OYAMADA, M. **Read More, Think More: Revisiting Observation Reduction for Web Agents**. 2026. https://arxiv.org/abs/2604.01535
- KWON, D.; LEE, D. **Region4Web: Rethinking Observation Space Granularity for Web Agents**. 2026. https://arxiv.org/abs/2605.07134
- LEE, H. **Practical Limits of Autonomous Test Repair: A Multi-Agent Case Study with LLM-Driven Discovery and Self-Correction**. 2026. https://arxiv.org/abs/2605.01471 *(suporte parcial — conferir)*
- SIGDEL, A.; BARAL, R. **Schema First Tool APIs for LLM Agents: A Controlled Study of Tool Misuse, Recovery, and Budgeted Performance**. 2026. https://arxiv.org/abs/2603.13404
- KIM, T.; PARK, W.; YUN, H.; LEE, K. **Why Do AI Agents Systematically Fail at Cloud Root Cause Analysis?**. 2026. https://arxiv.org/abs/2602.09937
- GROVER, A. **Playwright CLI: The Token-Efficient Alternative to Playwright MCP for AI Coding Agents**. TestCollab Blog, 2026. https://testcollab.com/blog/playwright-cli *(suporte parcial — conferir)*
