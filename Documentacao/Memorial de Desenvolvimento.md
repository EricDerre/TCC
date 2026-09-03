<!-- ! Alteração de IA - Revisar: o memorial único virou este índice; o conteúdo foi movido,
     sem reescrita, para a pasta memorial/, separado por tema.
     ! Motivo: com mais de 400 linhas misturando decisões, achados, pesquisa e referências, o
     arquivo único ficou difícil de revisar e de citar. O nome deste arquivo foi mantido porque
     README, plano e comentários de código apontam para ele. A numeração das seções (1–9, 4.x,
     6.x) é a do documento original e continua sendo usada nas referências cruzadas. -->

# Memorial de Desenvolvimento

**Projeto:** Agente de QA End-to-End Autônomo com Capacidades de Self-Healing — UNICID, Ciência da Computação.
**Finalidade:** servir de insumo para a redação do relatório final. Reúne decisões tomadas e por quem, achados experimentais, correções feitas no projeto de pesquisa e as referências levantadas. As alterações de código aparecem apenas resumidas e referenciadas por commit.
**Período coberto:** 31/08/2026 a 03/09/2026.

O conteúdo está dividido por tema na pasta [`memorial/`](memorial/). A numeração das seções é a do memorial original: "4.12" é sempre o mesmo achado, esteja em que arquivo estiver.

## Sumário

### 1. Decisões e histórico — [`memorial/1-decisoes-e-historico/`](memorial/1-decisoes-e-historico/)
- [Ponto de partida](memorial/1-decisoes-e-historico/ponto-de-partida.md) — §1: o que havia no repositório e o achado que condicionou todo o projeto.
- [Decisões tomadas](memorial/1-decisoes-e-historico/decisoes.md) — §2: as decisões, com quem decidiu e o fundamento de cada uma.
- [O que foi construído, por commit](memorial/1-decisoes-e-historico/historico-por-commit.md) — §3.

### 2. Pesquisa e literatura — [`memorial/2-pesquisa-e-literatura/`](memorial/2-pesquisa-e-literatura/)
Duas frentes, ambas com o objetivo de evitar decisão por intuição.
- [Cenário de modelos livres e locais](memorial/2-pesquisa-e-literatura/modelos-locais-e-portugues.md) — §6.1: candidatos, licenças, português.
- [Raciocínio em estágios para modelos pequenos](memorial/2-pesquisa-e-literatura/raciocinio-em-estagios.md) — §6.2: CoT, fases de compilador, PA-Tool, Constraint Tax.
- [Documentação como contexto (RAG)](memorial/2-pesquisa-e-literatura/documentacao-como-contexto-rag.md) — §6.3: posição no contexto, distração, fidelidade, recuperação em CPU, GPT-2/3.
- [Quantização](memorial/2-pesquisa-e-literatura/quantizacao.md) — §6.4: níveis, modelos pequenos, flips, CPU.
- [Medição de tempo em CPU e estatística](memorial/2-pesquisa-e-literatura/medicao-em-cpu-e-estatistica.md) — §6.5: prefill × decode, cache de prefixo, McNemar, Wilson.
- [Referências levantadas](memorial/2-pesquisa-e-literatura/referencias.md) — §9: todas as fontes, por tema.

### 3. Resultados e análises — [`memorial/3-resultados-e-analises/`](memorial/3-resultados-e-analises/)
Resultados obtidos executando, não deduções.
- [Achados — ambiente cobaia](memorial/3-resultados-e-analises/achados-do-ambiente-cobaia.md) — §4.1 a 4.11: o que a montagem do ambiente revelou.
- [Achados — modelos e experimentos](memorial/3-resultados-e-analises/achados-dos-modelos.md) — §4.12 a 4.21: diff pré-calculado, prolixidade, linear × estágios, tokenizador, recuperação, cache de prefixo.
- [Validação da hipótese de uso de Cython](memorial/3-resultados-e-analises/validacao-cython.md) — §7.
- [**Fase 2-A — relatório por modelo**](memorial/3-resultados-e-analises/fase-2a-relatorio-por-modelo.md) — protocolo, quadro geral, estratégias, classes × níveis, modos de falha, perfil de cada um dos 6 modelos, custo, ameaças à validade e as hipóteses registradas para a 2-B.

### 4. Projeto de pesquisa (ABNT) — [`memorial/4-projeto-de-pesquisa-abnt/`](memorial/4-projeto-de-pesquisa-abnt/)
- [Correções aplicadas](memorial/4-projeto-de-pesquisa-abnt/correcoes-aplicadas.md) — §5: trecho, antes, depois e motivo de cada correção.

### Pendências
- [Pendências e questões em aberto](memorial/pendencias.md) — §8.
