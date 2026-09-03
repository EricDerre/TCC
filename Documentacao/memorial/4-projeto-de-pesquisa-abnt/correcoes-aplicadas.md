<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
# Correções feitas no projeto de pesquisa (ABNT)

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá.

## 5. Correções feitas no projeto de pesquisa (ABNT)

Aplicadas em `Projeto de Pesquisa - ABNT 15287_2025 - V3.md`, commit `1b0c4b8`, cada uma marcada no texto.

| Trecho | Antes | Depois | Motivo |
|---|---|---|---|
| Objetivo geral | "arquitetura de nuvem híbrida"; "propor correções de código" | LLM executado localmente; cura de localizadores + diagnóstico | A implementação é local; correção autônoma de código-fonte foi descartada por inviabilidade com modelo pequeno |
| Objetivo específico 2 | Google Colab + FastAPI + Ngrok | Camada de inferência local (Ollama) | Idem |
| §3.2 | Qwen2.5-Coder em GPU T4 na nuvem | Modelo quantizado em CPU local, com critério do menor porte que atende | A dependência de nuvem **contradizia o próprio problema de pesquisa**, que pergunta como operar sob restrição de hardware local |
| §3.3 | Túnel Ngrok + API de ponte | Comunicação por loopback; regra de truncamento que preserva chaves e tipos | Sem servidor remoto, não há o que tunelar. Truncar chave destruiria o sinal de quebra de contrato |
| §3.4 | Métricas nomeadas sem definição | Fórmula de MTTR, definição de Task Success, grupo de controle manual, volume e condições de determinismo | Não havia fórmula, linha de base nem número de execuções — o Mês 5 chegaria sem protocolo |
| §4 | "viabilidade... através da topologia de nuvem híbrida" | Execução local sem custo de infraestrutura | Recorrer a GPU em nuvem **contorna** a restrição em vez de demonstrar viabilidade sob ela |
| §2.1 | Oscilava entre autonomia total e copiloto | Correção aplicada automaticamente na verificação, apresentada como sugestão | A ambiguidade tornaria o Task Success indefinido |
| §2.4 | Só Prune4Web | + Joseph (2026), fixando que a poda incide **sobre a árvore de acessibilidade** | O texto nomeava dois artefatos sem nunca relacioná-los |
| §2.5 e §2.6 | Inexistentes | Quebra de contrato de API (Maciak) e RAG (Shi, Li e Chen) | Três referências constavam na lista **sem citação no corpo** — defeito perante a NBR 6023 |
| Cronograma, Mês 2 | Colab, FastAPI, Ngrok | Ollama com modelo quantizado, incluindo comparação de portes | Coerência com §3.2 |
| Glossário | Continha Ngrok, com definição na direção oposta à proposta | Removido; acrescentados 8 termos usados no corpo mas não definidos | Accessibility Tree, Attention Dilution, DOM Pruning, MTTR, Ollama, Quantização, RAG, Task Success |

**Pendência:** o arquivo `.pdf` na mesma pasta é anterior a essas correções e precisa ser regerado. As marcações são comentários HTML, invisíveis na conversão, mas convém removê-las antes da entrega final.


