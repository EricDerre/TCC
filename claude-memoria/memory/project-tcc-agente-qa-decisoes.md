---
name: project-tcc-agente-qa-decisoes
description: "Decisões de arquitetura do TCC (Agente de QA E2E) que não dá pra deduzir do código — LLM local, escopo do self-healing, dois alvos, máquina-alvo dos experimentos, um modelo por vez"
metadata: 
  node_type: memory
  type: project
  originSessionId: f03b12ad-c757-4edb-aaa2-0cb57f2610aa
  modified: 2026-09-07T12:00:29.899Z
---

Decisões tomadas com o Eric no TCC "Agente de QA End-to-End Autônomo com Self-Healing" (UNICID, 9 autores, defesa prevista 2026) que **não são dedutíveis do código nem do histórico**:

- **LLM 100% local e gratuito** (Ollama + modelos quantizados), substituindo o Google Colab + FastAPI + Ngrok que o projeto de pesquisa ABNT original propõe. Motivo: a ferramenta precisa ser usável por qualquer um fora da universidade, sem configurar Colab nem gastar dinheiro, rodando em máquina corporativa com pouco recurso.
- **Escopo do Self-Healing: diagnóstico + cura de seletor.** O agente gera o relatório de pré-análise e conserta localizadores quebrados para retomar o fluxo. **Não** propõe patch do código da aplicação-alvo (modelo quantizado pequeno erra demais nisso). A correção é aplicada na re-execução de verificação e exposta como sugestão, nunca commitada sozinha.
- **Dois alvos de teste, de propósito:** `CobaiaFront` (PHP+MySQL monolítico legado, cedido por um integrante, mantido intocado) e `CobaiaAPI` (FastAPI) + a aba `produtos_api.php`. O monolítico é abrangência/legado; a API JSON é o foco (Contract Drift). Ambos compartilham o mesmo banco.
- **Navegador do agente: Chromium do próprio Playwright** (`playwright install chromium`), headless — por reprodutibilidade (versão fixa, essencial para as métricas MTTR/Task Success) e por funcionar igual em Windows e Linux. Edge foi descartado por não ser padrão no Linux.
- **Repositório "hit and run":** qualquer um clona e roda com o mínimo de passos (`Cobaia.exe` no Windows, `install.sh`/`run.sh` no Linux). Precisa funcionar em Windows e Linux; macOS só se sair de graça.
- **Máquina-alvo dos experimentos é o notebook corporativo** (Intel i5-1235U, 16 GB de RAM, sem GPU dedicada), **não** o Ryzen 7 5800H em que o ambiente foi desenvolvido e a Fase 2-A (6 modelos × 90 casos × 3 estratégias) foi medida. Os tempos que valem para a tese são os medidos nela. A Fase 2-B — e a linha de base A0 **refeita** lá, porque as comparações são pareadas caso a caso e não podem misturar máquinas — grava em `Programacao/AgenteCore/experimentos/resultados_alvo/` (variável de ambiente `RESULTADOS_DIR`, lida por `caminhos.py`); os resultados do Ryzen ficam em `resultados/` como referência de desenvolvimento. Decidido pelo Eric em 07/09/2026.
- **Experimentos com LLM: um modelo residente por vez, só CPU (`num_gpu=0`), `num_ctx` fixo em 8192.** Pedido explícito do Eric, para não haver disputa de memória nem processamento paralelo entre modelos; a bateria confere em `/api/ps` e se recusa a começar com outro modelo carregado.

**Why:** São escolhas que divergem do documento acadêmico ou que não deixam rastro no código — sem isso registrado, uma sessão futura reintroduz Colab/Ngrok, tenta gerar patch de código, mede tempo na máquina errada ou roda dois modelos ao mesmo tempo.

**How to apply:**
- Ao mexer no `AgenteCore`, respeitar a restrição acadêmica dura: diagnóstico só a partir da **fronteira** (accessibility tree + tráfego HTTP no navegador), **sem acoplar à lógica interna do servidor**.
- O documento ABNT ainda descreve a topologia de nuvem — corrigi-lo faz parte do trabalho, não é opcional.
- Bateria pesada roda na máquina-alvo; em outra máquina, sempre com `RESULTADOS_DIR` apontando para outra pasta — nunca misturar resultados de máquinas na mesma pasta.
- Convenção de nomes aqui é PEP8 snake_case (Python) e padrão legado (PHP) — ver [[feedback-comentar-alteracoes-ia-motivo]].
