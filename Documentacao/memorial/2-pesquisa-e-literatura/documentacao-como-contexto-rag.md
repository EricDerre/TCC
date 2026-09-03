<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
# Pesquisa bibliográfica — Documentação como contexto (RAG) para modelos pequenos

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá.

### 6.3 Documentação como contexto (RAG) para modelos pequenos

Levantamento feito para desenhar a Fase 2-B, com fontes de 2024 em diante. A pergunta era se dar ao modelo uma biblioteca do sistema fecha a lacuna entre os 67,8% da Fase 2-A e a meta de 70–80%, e como medir isso sem se enganar.

**Posição e quantidade de contexto importam mais que a presença dele.**
- *Lost in the Middle* (Liu et al., TACL 2024): com 20 documentos, o GPT-3.5-Turbo acerta **75,8%** se o documento certo está na posição 1, **53,8%** na posição 10 e **63,2%** na 20 — o meio fica **abaixo do closed-book (56,1%)**. LongChat-13B, modelo aberto de porte próximo aos nossos, vai de 68,6% a 55,3% e **não recupera no fim** (55,0%).
- *Context Rot* (Hong, Troynikov e Huber, Chroma, 2025): 18 modelos; degradação perceptível **a partir de ~2.500 tokens**; um único distrator já reduz o acerto e quatro compõem; haystack coerente é pior que embaralhado.
- *Classifier Context Rot* (Martin e Roger, 2026): classificadores erram 2× a 30× mais quando o alvo vem depois de muito contexto benigno — o formato exato da nossa tarefa.
- *Long Context vs. RAG* (Li, Cao, Ma e Sun, 2024): contexto inteiro vence para modelos fortes; **modelos abertos pequenos se beneficiam da recuperação** por capacidade limitada de contexto longo.
- *The Power of Noise* (Cuconasu et al., SIGIR 2024) relatou +30% com documentos aleatórios; *The Powerless Noise* (Mazuryk et al., SIGIR 2026) reproduziu e mostrou que o efeito aparece, enfraquece ou some com pequenas mudanças de prompt e de limite de decodificação, e que **truncamento explica boa parte da variância** — a mesma armadilha do nosso `num_predict=400`.

**O modelo segue a documentação ou a memória?** *Investigating Context-Faithfulness* (Li et al., ACL 2025): quanto mais forte a memória paramétrica, mais o modelo ignora a evidência; evidência **parafraseada** aumenta a adesão muito mais que repetição literal. O survey *Knowledge Conflicts for LLMs* (Xu et al., EMNLP 2024) documenta viés sistemático a favor da evidência que concorda com o prior.

**Recuperação em CPU.** BM25 segue forte fora de domínio (BEIR); híbrido BM25+denso via RRF ganhou +8,1 pp de Recall@5 em documentos com tabelas (2026); reranking não se justifica em corpus pequeno e curado. Em chunking, tamanho fixo venceu chunking semântico e a configuração pesa tanto quanto o modelo de embedding (2025). Para português: a *MTEB-BR* (Stekel, 2026), 93 modelos em 22 tarefas em pt-BR, coloca o **`embeddinggemma-300m` em 0,649** contra 0,670 do Qwen3-Embedding-8B — os seis líderes ficam a 0,020 um do outro, e o de 300M roda em CPU pelo próprio Ollama.

**Formato e ancoragem.** *Does Prompt Formatting Have Any Impact?* (He et al., 2024): até 40% de variação no GPT-3.5 conforme o formato; modelos maiores são robustos; não há vencedor universal. Markdown foi mantido, sem ablação de formato (custo), registrado como ameaça à validade.

**O que mudou no desenho por causa disso:** (a) biblioteca no **início** do prompt, caso no fim; (b) **dois braços** de biblioteca — inteira e recuperada — porque a literatura prevê que recuperada ≥ inteira em modelos pequenos, hipótese testável; (c) braços de **ouro, distrator plausível e adversarial** (verbete errado + registro falso afirmando a causa errada para o sintoma), sem os quais "com biblioteca" não separa falha de recuperação de falha de raciocínio nem mede adesão cega; (d) verbetes escritos como **paráfrase em linguagem de domínio**, com o código só como referência `arquivo:linha`; (e) recuperação por BM25 + sinais em código, sem dependência nova; embedding denso só como ablação offline; (f) **GPT-2 e GPT-3 descartados**: GPT-3 nunca teve pesos liberados e os modelos originais foram desligados em 04/01/2024; GPT-2 até cabe no contexto (medido com o tokenizador dele: 0% dos prompts lineares acima de 1.024 tokens, 8–9% dos em estágios), mas é modelo base sem instrução, treinado só em inglês e fora da biblioteca oficial do Ollama — três variáveis de confusão ao mesmo tempo. O piso metodologicamente limpo seria `qwen2.5:0.5b-base` × `0.5b-instruct` (mesma família, tokenizador e corpus, diferindo só pelo instruction tuning), que existe no registro do Ollama; ficou como opção futura.
