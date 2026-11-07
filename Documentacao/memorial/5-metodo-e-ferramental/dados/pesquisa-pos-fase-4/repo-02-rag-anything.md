<!-- ! Alteração de IA - Revisar: arquivo novo (07/11/2026): leitura feita por um subagente do Claude (modelo Sonnet) sobre repositório HKUDS/RAG-Anything, na rodada 6 da pesquisa (Pós-Fase 4); é um arquivo de dados que ferramentas/integrar_pesquisa_pos_fase4.py lê para montar o levantamento §6.15, e o integrador tira este comentário do texto que entra lá.
     ! Motivo: o Eric pediu em 07/11/2026 a base de pesquisa de cada ponto da Pós-Fase 4 e a validação de oito repositórios do GitHub; a leitura fica versionada como dado para o levantamento ser regerado por script e conferido pelo --check. O texto é o que o subagente escreveu, sem edição, com a marca de confiança que ele deu a cada fonte (aberta e lida; só o resumo de busca; de memória). -->
# HKUDS/RAG-Anything

Fontes lidas: página do repositório no GitHub e README bruto (raw.githubusercontent.com). Não foram lidos o artigo completo nem os arquivos de docs/ (a página lista só os nomes `context_aware_processing.md`, `batch_processing.md` e `multimodal_rag_failure_modes.md`).

## 1 O que é e como funciona por dentro

Framework de RAG multimodal construído sobre o LightRAG. Ingere documentos com texto, imagens, tabelas e equações num só fluxo de quatro etapas.
- Parsing: um parser escolhido na configuração (`RAGAnythingConfig`) quebra o documento em blocos. MinerU é o padrão; Docling e PaddleOCR são alternativas. O parser é fixo na inicialização.
- Análise multimodal: texto segue o caminho de texto. Imagens, tabelas e equações vão para processadores que usam um LLM ou modelo de visão para gerar descrições textuais.
- Grafo de conhecimento: o LightRAG extrai entidades e relações; os elementos multimodais são ligados ao texto e a hierarquia do documento é guardada por relações "belongs_to".
- Recuperação: busca vetorial combinada com travessia do grafo (modos `hybrid`, `local`, `global`, `naive`). Há consulta com visão (imagens recuperadas vão ao modelo de visão) e consulta com tabela ou equação anexada.
Em resumo: converte tudo em texto por meio de modelos, indexa em vetores mais grafo e responde por LLM.

## 2 Pilha, dependências e exigências

- Linguagem: Python 3.10 ou superior (MinerU 3.x suporta 3.10 a 3.13).
- LLM: obrigatório. Os exemplos usam `gpt-4o-mini` da OpenAI.
- Modelo de visão: usado para imagens e consultas com visão (exemplos com `gpt-4o`).
- Modelo de embedding: obrigatório (exemplos com `text-embedding-3-large`, dimensão 3072). Ou seja, exige um segundo e um terceiro modelo além do LLM.
- Chave de API: necessária no processamento completo dos exemplos. Os exemplos usam funções no estilo OpenAI com `base_url` opcional; o README não menciona Ollama nem modelos locais.
- GPU: opcional (MinerU acelera com CUDA). Sem GPU roda em CPU, mais lento.
- Nuvem: não obrigatória em tese, mas o caminho documentado é a API da OpenAI. Áudio usa faster-whisper (local).
- LibreOffice: só para arquivos Office (doc, docx, ppt, pptx, xls, xlsx).
- Node: não exigido. Instalação: `pip install raganything` ou `uv sync` a partir do código-fonte.
- Licença: MIT (página do GitHub). O texto do README não a declara.
- Maturidade: cerca de 24,5 mil estrelas, 2,9 mil forks, 526 commits. Release: nenhuma listada. Data do último commit: não visto (a página não mostra datas). Data de criação: não vista. Artigo: arXiv 2510.12323, outubro de 2025.

## 3 Aplicação ao desenvolvimento com o Claude Code neste projeto

Não serve. O desenvolvimento já se apoia em CLAUDE.md, memória persistente, skills e subagentes, e o conteúdo a consultar (código, painel, livro-razão, notas em Markdown) é texto, não PDF com figuras e equações. Indexar a documentação do projeto exigiria um LLM, um modelo de embedding e provavelmente chave de API, tudo fora do fluxo atual, e o embedding já perdeu em medição neste corpus. Instalar custaria Python 3.10+, MinerU (pesado), LibreOffice opcional e manutenção de índice e grafo. Um único uso marginal: ingerir PDFs de artigos e do livro (Faceli) para consulta pelo Claude. Esse uso é coberto por leitura direta de PDF com PyMuPDF e pelo painel de pesquisa já existente, sem custo extra.

## 4 Aplicação dentro do agente ou do produto

Não serve em nenhum módulo. Conflitos com o contexto:
- Busca: o embedding foi medido e descartado (hit@3 de 35,6% contra 80,0% do BM25 com sinais em código na biblioteca de 40 verbetes). O RAG-Anything depende de embedding mais grafo; trocar a busca exige repetir toda a medição.
- Modelo residente único: o framework quer LLM, visão e embedding. Com um modelo por vez em CPU (qwen2.5:7b, num_ctx 8192), alternar três modelos custa carga de memória a cada troca em 16 GB.
- Prompt do diagnóstico congelado byte a byte: o contexto injetado pelo grafo mudaria o prompt e obrigaria a medir tudo de novo.
- Nuvem e chave de API: o caminho documentado usa OpenAI, o que viola "nada em nuvem". Com endpoint local (compatível com OpenAI) seria teoricamente possível, mas o README não confirma.
- Harness só com biblioteca padrão: o framework puxa LightRAG, MinerU e dependências pesadas; sem administrador no Windows corporativo, instalar MinerU e LibreOffice é arriscado.
- Corpus: 40 verbetes Markdown curtos não têm imagens, tabelas ou equações; o ganho multimodal não se aplica. Poda, trilha, relatório, cura de seletor e painel não têm parte de documento multimodal para ingerir.
- Possível ideia isolada: a seção "multimodal_rag_failure_modes.md" da documentação pode interessar como leitura sobre modos de falha, mas não foi lida.

## 5 Risco, esforço e veredito

- Uso com o Claude Code: risco baixo, ganho próximo de zero. Esforço de 1 a 2 sessões para instalar e configurar, mais manutenção. Veredito: não adotar; só citar como trabalho relacionado.
- Uso no agente: risco alto (quebra restrições de modelo único, prompt congelado, nuvem e medição já feita). Esforço de várias sessões mais nova bateria de medição. Veredito: não adotar; registrar como descartado por conflito de restrições.

## 6 Referências ABNT NBR 6023

GUO, Zirui et al. **RAG-Anything**: All-in-One RAG Framework. Disponível em: https://github.com/HKUDS/RAG-Anything. Acesso em: 7 nov. 2026.

GUO, Zirui; REN, Xubin; XU, Lingrui; ZHANG, Jiahao; HUANG, Chao. **RAG-Anything**: All-in-One RAG Framework. arXiv:2510.12323, 2025. Disponível em: https://arxiv.org/abs/2510.12323. Acesso em: 7 nov. 2026.
