---
name: project-tcc-agente-qa-decisoes
description: "Decisões de arquitetura do TCC (Agente de QA E2E) que não dá pra deduzir do código — LLM local, escopo do self-healing, dois alvos, máquina-alvo (agora a principal), um modelo por vez, biblioteca recuperada"
metadata: 
  node_type: memory
  type: project
  originSessionId: f03b12ad-c757-4edb-aaa2-0cb57f2610aa
  modified: 2026-09-09T12:01:23.804Z
---

Decisões tomadas com o Eric no TCC "Agente de QA End-to-End Autônomo com Self-Healing" (UNICID, 9 autores, defesa prevista 2026) que **não são dedutíveis do código nem do histórico**:

- **LLM 100% local e gratuito** (Ollama + modelos quantizados), substituindo o Google Colab + FastAPI + Ngrok que o projeto de pesquisa ABNT original propõe. Motivo: a ferramenta precisa ser usável por qualquer um fora da universidade, sem configurar Colab nem gastar dinheiro, rodando em máquina corporativa com pouco recurso.
- **Escopo do Self-Healing: diagnóstico + cura de seletor.** O agente gera o relatório de pré-análise e conserta localizadores quebrados para retomar o fluxo. **Não** propõe patch do código da aplicação-alvo (modelo quantizado pequeno erra demais nisso). A correção é aplicada na re-execução de verificação e exposta como sugestão, nunca commitada sozinha.
- **Dois alvos de teste, de propósito:** `CobaiaFront` (PHP+MySQL monolítico legado, cedido por um integrante, mantido intocado) e `CobaiaAPI` (FastAPI) + a aba `produtos_api.php`. O monolítico é abrangência/legado; a API JSON é o foco (Contract Drift). Ambos compartilham o mesmo banco.
- **Navegador do agente: Chromium do próprio Playwright** (`playwright install chromium`), headless — por reprodutibilidade (versão fixa, essencial para as métricas MTTR/Task Success) e por funcionar igual em Windows e Linux. Edge foi descartado por não ser padrão no Linux.
- **Repositório "hit and run":** qualquer um clona e roda com o mínimo de passos (`Cobaia.exe` no Windows, `install.sh`/`run.sh` no Linux). Precisa funcionar em Windows e Linux; macOS só se sair de graça.
- **Máquina-alvo dos experimentos é o notebook corporativo** (Intel i5-1235U, 16 GB de RAM, sem GPU dedicada) — e, **desde 09/09/2026, também a máquina principal do projeto**: as fases seguintes são desenvolvidas e medidas nela. O Ryzen 7 5800H foi só desenvolvimento (Fase 2-A). Os tempos que valem para a tese são os do i5 (é ~2× mais lento que o Ryzen; a acurácia reproduz entre máquinas). Resultados do i5 em `Programacao/AgenteCore/experimentos/resultados_alvo/` (variável de ambiente `RESULTADOS_DIR`, lida por `caminhos.py`); os do Ryzen em `resultados/`. Nunca misturar máquinas na mesma pasta.
- **Experimentos com LLM: um modelo residente por vez, só CPU (`num_gpu=0`), `num_ctx` fixo em 8192.** Pedido explícito do Eric, para não haver disputa de memória nem processamento paralelo entre modelos; a bateria confere em `/api/ps` e se recusa a começar com outro modelo carregado.
- **A biblioteca de documentação é consultada por recuperação (3 verbetes), nunca inteira no prompt.** Medido na Fase 2-B: recuperada sobe o acerto em todos os modelos (3 passam de 70%); inteira não ajuda e piora o Granite. E **verbete errado é seguido em 93–96% dos casos** — a gestão da biblioteca pelo modelo (Fase 3) só pode existir atrás de validação por código.

**Why:** São escolhas que divergem do documento acadêmico ou que não deixam rastro no código — sem isso registrado, uma sessão futura reintroduz Colab/Ngrok, tenta gerar patch de código, mede tempo na máquina errada, roda dois modelos ao mesmo tempo ou coloca a biblioteca inteira no prompt.

**How to apply:**
- Ao mexer no `AgenteCore`, respeitar a restrição acadêmica dura: diagnóstico só a partir da **fronteira** (accessibility tree + tráfego HTTP no navegador), **sem acoplar à lógica interna do servidor**.
- O documento ABNT ainda descreve a topologia de nuvem — corrigi-lo faz parte do trabalho, não é opcional.
- Bateria pesada roda na máquina-alvo; em outra máquina, sempre com `RESULTADOS_DIR` apontando para outra pasta.
- Contexto operacional das sessões anteriores (harness, armadilhas, próximas fases): `claude-memoria/contexto/` no repositório.
- Convenção de nomes aqui é PEP8 snake_case (Python) e padrão legado (PHP) — ver [[feedback-comentar-alteracoes-ia-motivo]].
