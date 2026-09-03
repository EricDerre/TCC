<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
# Pesquisa bibliográfica — Cenário de modelos livres e locais

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá.

### 6.1 Cenário de modelos livres e locais

Levantamento de 12 candidatos executáveis via Ollama, com licença, tamanho, capacidade em português e estabilidade da tag.

**Eliminados por critério objetivo:** OpenCoder (oficialmente só inglês e chinês); StarCoder2 3B/7B (são modelos *base*, não seguem instrução); CodeLlama (2 anos, base Llama 2, português fraco); Mistral 7B (defasado, português fraco); Codestral (22B e licença de não-produção); DeepSeek-Coder-V2 (8,9 GB, acima do orçamento de memória).

**Achado mais valioso:** `qwen2.5-coder:7b` **vs** `qwen2.5:7b` formam um experimento controlado quase perfeito — mesma base, tamanho, licença, tokenização e mês de treino, diferindo **apenas** pelo fine-tuning em código. Responde "especialização em código ajuda nesta tarefa?" sem variáveis de confusão.

**Alerta de licença:** `qwen2.5-coder:3b` está sob **Qwen Research License (não-comercial)**, enquanto o `:7b` da mesma família é Apache 2.0. Decidiu-se mantê-lo na comparação com a restrição documentada, trocando apenas o padrão de produção.

**Português (PoETa v2, nov/2025):** Qwen2.5 7B lidera entre os abertos pequenos com 63,7 NPM; Llama 3.1 8B fica em 53,5. Achado relevante para o dimensionamento: **modelos abaixo de 5B têm perda desproporcional em português** (5,1 pontos de diferença EN↔PT, contra 3,8 nos de 10B+) — o que justifica metodologicamente manter a faixa de 7–8B apesar da latência.

**Riscos operacionais documentados:** tags do Ollama são ponteiros mutáveis, não imutáveis — é preciso registrar o digest sha256 de cada modelo para o experimento ser reproduzível; o modo *thinking* de Qwen3 e Granite 4.2 multiplica a latência e precisa ser desativado; e o cache KV de modelos com 128K de contexto estoura a memória antes do peso do modelo, exigindo fixar `num_ctx`.

**Baseline não-neural:** existe um algoritmo de prioridade em 10 níveis que recupera 82,4% dos localizadores em menos de 1 s, sem LLM. Entra como piso obrigatório da tarefa de seletor — se os modelos não o superarem, esse é um resultado honesto.
