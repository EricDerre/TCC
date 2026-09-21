<!-- ! Alteração de IA - Revisar: o memorial único virou este índice; o conteúdo foi movido,
     sem reescrita, para a pasta memorial/, separado por tema.
     ! Motivo: com mais de 400 linhas misturando decisões, achados, pesquisa e referências, o
     arquivo único ficou difícil de revisar e de citar. O nome deste arquivo foi mantido porque
     README, plano e comentários de código apontam para ele. A numeração das seções (1–9, 4.x,
     6.x) é a do documento original e continua sendo usada nas referências cruzadas. -->
<!-- ! Alteração de IA - Revisar: índice atualizado em 11/09/2026 com a Fase 3 — os dois
     relatórios novos (Fase 3 por modelo e comparação entre fases), o achado 4.29, as
     seções de pesquisa 6.6 a 6.8 e o levantamento de 11/09, decisões até a 38 e o período
     coberto estendido.
     ! Motivo: o sumário é o único lugar que diz onde está cada assunto, e quem abre o
     Memorial pelo índice não encontraria o pré-registro da Fase 3 nem os relatórios novos.
     As quatro seções de pesquisa listadas em 6.6 a 6.8 e o levantamento foram escritas na
     mesma rodada de documentação da Fase 3, em outros arquivos. -->
<!-- ! Alteração de IA - Revisar: em 12/09/2026 o índice passou a dizer decisões 1 a 44, período
     coberto até 12/09/2026 e o rótulo §6.9 na linha do levantamento; a frase da tag anterior
     que mandava conferir links pendentes foi retirada.
     ! Motivo: as decisões 39 a 44 entraram em `decisoes.md` na revisão final de 12/09; o
     levantamento é a §6.9 do Memorial (é o título do arquivo) e era o único item da lista sem
     número de seção; e os quatro arquivos das §6.6 a §6.9 existem e a varredura de links de
     12/09/2026 não achou link quebrado, então o aviso deixou de ser verdade. -->

# Memorial de Desenvolvimento

**Projeto:** Agente de QA End-to-End Autônomo com Capacidades de Self-Healing — UNICID, Ciência da Computação.
**Finalidade:** servir de insumo para a redação do relatório final. Reúne decisões tomadas e por quem, achados experimentais, correções feitas no projeto de pesquisa e as referências levantadas. As alterações de código aparecem apenas resumidas e referenciadas por commit.
<!-- ! Alteração de IA - Revisar: período coberto estendido a 21/09/2026 (bateria da Fase 3 de 13–15/09 e plano complementar de 21/09).
     ! Motivo: o Memorial dizia cobrir até 12/09 e a bateria inteira (58 h) ficou fora de qualquer registro narrativo; a data acompanha a última sessão documentada. -->
**Período coberto:** 31/08/2026 a 21/09/2026.

O conteúdo está dividido por tema na pasta [`memorial/`](memorial/). A numeração das seções é a do memorial original: "4.12" é sempre o mesmo achado, esteja em que arquivo estiver.

## Sumário

### 1. Decisões e histórico — [`memorial/1-decisoes-e-historico/`](memorial/1-decisoes-e-historico/)
- [Ponto de partida](memorial/1-decisoes-e-historico/ponto-de-partida.md) — §1: o que havia no repositório e o achado que condicionou todo o projeto.
- [Decisões tomadas](memorial/1-decisoes-e-historico/decisoes.md) — §2: as decisões 1 a 44, com quem decidiu e o fundamento de cada uma.
- [O que foi construído, por commit](memorial/1-decisoes-e-historico/historico-por-commit.md) — §3.

### 2. Pesquisa e literatura — [`memorial/2-pesquisa-e-literatura/`](memorial/2-pesquisa-e-literatura/)
Duas frentes, ambas com o objetivo de evitar decisão por intuição.
- [Cenário de modelos livres e locais](memorial/2-pesquisa-e-literatura/modelos-locais-e-portugues.md) — §6.1: candidatos, licenças, português.
- [Raciocínio em estágios para modelos pequenos](memorial/2-pesquisa-e-literatura/raciocinio-em-estagios.md) — §6.2: CoT, fases de compilador, PA-Tool, Constraint Tax.
- [Documentação como contexto (RAG)](memorial/2-pesquisa-e-literatura/documentacao-como-contexto-rag.md) — §6.3: posição no contexto, distração, fidelidade, recuperação em CPU, GPT-2/3.
- [Quantização](memorial/2-pesquisa-e-literatura/quantizacao.md) — §6.4: níveis, modelos pequenos, flips, CPU.
- [Medição de tempo em CPU e estatística](memorial/2-pesquisa-e-literatura/medicao-em-cpu-e-estatistica.md) — §6.5: prefill × decode, cache de prefixo, McNemar, Wilson.
- [Memória gerida pelo próprio modelo](memorial/2-pesquisa-e-literatura/memoria-gerida-pelo-modelo.md) — §6.6: o que a literatura mostra sobre modelo que escreve a própria documentação — escrita aditiva, portão de validação, curvas que sobem e caem.
- [Tokenização e arquitetura](memorial/2-pesquisa-e-literatura/tokenizacao-e-arquitetura.md) — §6.7: como o texto vira token, o que isso custa em contexto e por que a estimativa por caracteres erra.
- [Métricas e desenho experimental](memorial/2-pesquisa-e-literatura/metricas-e-desenho-experimental.md) — §6.8: acurácia balanceada, Q de Cochran, Holm, poder de teste e partição — amplia a §6.5.
<!-- ! Alteração de IA - Revisar: em 21/09/2026 a linha do levantamento passou a descrever as duas rodadas (§6.9.1–6.9.17) e entrou a linha do mapa de decisões (§6.10).
     ! Motivo: a rodada 2 da pesquisa (oito temas: conflito contexto × conhecimento, validação em código de artefatos, estágios em modelos pequenos, qualidade de documentação, aprender sem atualizar pesos, taxonomia e rótulos-ouro, agentes autônomos de QA, recuperação em corpus pequeno) foi integrada em 21/09 e o mapa é o arquivo que a análise decisória da Fase 3 cita; sem as linhas o índice não os alcançaria. -->
- [Levantamento bibliográfico para a Fase 3 (rodadas de 11/09 e 21/09/2026)](memorial/2-pesquisa-e-literatura/levantamento-2026-09-11-fase-3.md) — §6.9: as sínteses verificadas das duas rodadas (§6.9.1–6.9.8 os oito tópicos do plano; §6.9.9–6.9.16 as oito lacunas fechadas em 21/09), as afirmações rejeitadas com o motivo (§6.9.17) e as lacunas que restam.
- [Mapa de decisões — o que a literatura previa para a Fase 3](memorial/2-pesquisa-e-literatura/mapa-de-decisoes-fase-3.md) — §6.10: achado → número → fonte → critério de leitura dos resultados, riscos com mitigação, métricas sustentadas pela literatura e os capítulos do livro-guia por seção.
- [Referências levantadas](memorial/2-pesquisa-e-literatura/referencias.md) — §9: todas as fontes, por tema.

### 3. Resultados e análises — [`memorial/3-resultados-e-analises/`](memorial/3-resultados-e-analises/)
Resultados obtidos executando, não deduções.
- [Achados — ambiente cobaia](memorial/3-resultados-e-analises/achados-do-ambiente-cobaia.md) — §4.1 a 4.11: o que a montagem do ambiente revelou.
- [Achados — modelos e experimentos](memorial/3-resultados-e-analises/achados-dos-modelos.md) — §4.12 a 4.29: diff pré-calculado, prolixidade, linear × estágios, tokenizador, recuperação, cache de prefixo, os achados da 2-B (recuperada × inteira, teto da recuperação, adesão cega, 3B ≈ 8B, máquinas, quantização), o fechamento do 4.20 e o pré-registro da Fase 3 (4.29).
- [Validação da hipótese de uso de Cython](memorial/3-resultados-e-analises/validacao-cython.md) — §7.
- [**Fase 2-A — relatório por modelo**](memorial/3-resultados-e-analises/fase-2a-relatorio-por-modelo.md) — protocolo, quadro geral, estratégias, classes × níveis, modos de falha, perfil de cada um dos 6 modelos, custo, ameaças à validade e as hipóteses registradas para a 2-B.
- [**Fase 2-B — biblioteca de documentação: relatório por modelo**](memorial/3-resultados-e-analises/fase-2b-relatorio-por-modelo.md) — máquina-alvo, linha de base em duas máquinas, recuperada × inteira, teto da recuperação, efeito por classe, adesão cega, quantização, custo no i5, perfil dos 6 modelos, comparação com a 2-A e as decisões a tomar.
- [**Fase 3 — biblioteca gerida pelo próprio modelo: relatório por modelo**](memorial/3-resultados-e-analises/fase-3-relatorio-por-modelo.md) — protocolo, partição 54/36, hipóteses pré-registradas, curva por versão da biblioteca, recuperação por biblioteca, documentação produzida, revisão humana das edições, perfil por modelo, custo e ameaças à validade. *Pré-registrado em 11/09/2026; bateria executada em 13–15/09/2026; preenchimento em andamento pelo plano complementar de 21/09/2026.*
- [**Comparação entre as fases**](memorial/3-resultados-e-analises/comparacao-entre-fases.md) — o que é comparável entre 2-A, 2-B e Fase 3 (máquina, fixtures, prompts), as tabelas que o `comparar_fases.py` gera, ganhos/riscos/perdas por fase e a decisão do modelo final.

### 4. Projeto de pesquisa (ABNT) — [`memorial/4-projeto-de-pesquisa-abnt/`](memorial/4-projeto-de-pesquisa-abnt/)
- [Correções aplicadas](memorial/4-projeto-de-pesquisa-abnt/correcoes-aplicadas.md) — §5: trecho, antes, depois e motivo de cada correção.

<!-- ! Alteração de IA - Revisar: seção 5 nova no índice (21/09/2026) para a pasta `memorial/5-metodo-e-ferramental/`.
     ! Motivo: o plano complementar de 21/09/2026 documenta o ferramental do agente de apoio (Claude Code) e das LLMs locais — avaliado, adotado e descartado com motivo — como insumo do documento final; sem a seção o índice não alcança os dois arquivos. -->
### 5. Método e ferramental — [`memorial/5-metodo-e-ferramental/`](memorial/5-metodo-e-ferramental/)
Como o trabalho é feito e com que ferramentas, para que a banca saiba o que foi decidido por método e não por acaso.
- [Ferramental do agente de apoio (Claude Code)](memorial/5-metodo-e-ferramental/ferramental-do-claude-code.md) — §7.1 a 7.6: a máquina e seus limites, os dois repositórios indicados (avaliação e decisão), os outros complementos com o motivo de cada adoção ou descarte, as práticas de economia de tokens e a medição de consumo antes e depois.
- [Ferramental das LLMs locais](memorial/5-metodo-e-ferramental/ferramental-das-llms-locais.md) — §7.7 a 7.9: o que os mesmos repositórios significam para o agente local, o artigo sobre cache de respostas (o que já existe, o que entra, o que foi descartado) e a pesquisa específica de melhorias.

### Pendências
- [Pendências e questões em aberto](memorial/pendencias.md) — §8.
