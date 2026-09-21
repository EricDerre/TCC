---
paths:
  - "Programacao/AgenteCore/experimentos/**/*.py"
---
<!-- ! Alteração de IA - Revisar: regra carregada só ao editar o harness de experimentos (21/09/2026).
     ! Motivo: concentrar num arquivo pequeno as invariantes que cada tarefa de código da Fase 3/3-B repetia no brief. -->
# Harness de experimentos (Programacao/AgenteCore/experimentos)
- Só biblioteca padrão (+ matplotlib apenas nos scripts de gráficos, na venv `Programacao/AgenteCore/.venv`). PEP8 snake_case em português; tipagem moderna nas assinaturas públicas; docstrings curtas com a decisão e o número medido.
- `base_conhecimento/` nunca é escrita pelos experimentos (só `INDICE.md` por `validar_banco.py --indice`). `executar_fase3.py`, `estrategias.py` e `evolucao_biblioteca.py` não mudam depois da bateria de 13–15/09/2026: a Fase 3-B vive em arquivos novos.
- Um modelo residente por vez no Ollama (`ollama ps` vazio antes de inferir); só CPU (`num_gpu=0`); `num_ctx=8192`; temperatura 0,1.
- Toda saída de corrida vai para `caminhos.fase3(nome)`; os registros oficiais em `resultados_alvo/fase3/` (JSONL, `avaliacao_fase3.json`, `resumo_fase3.json`, `comparacao_fases.*`, snapshots, gráficos 12–17) nunca são regravados por scripts novos — só documentos DERIVADOS deles (como `decisao_modelo.json/.md`) podem nascer nessa pasta, e só por script com `--check`. Nunca rodar `gerar_graficos_fase3.py`/`avaliar_fase3.py` contra `--saida fase3` fora de uma regeneração combinada com o Eric.
- Nenhum número digitado à mão em Markdown: tabelas saem de script com modo `--check`.
- Testes: asserts em Python puro, `teste_<nome>()`, runner que termina em `N testes ok`; TDD (RED pelo motivo certo antes do GREEN); rodar com `PYTHONIOENCODING=utf-8`.
- Tag `# ! Alteração de IA - Revisar: …` + `# ! Motivo: …` em toda função nova e trecho alterado; sem jargão teórico.
