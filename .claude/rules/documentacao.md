---
paths:
  - "Documentacao/**/*.md"
  - "claude-memoria/**/*.md"
  - "README.md"
---
<!-- ! Alteração de IA - Revisar: regra carregada só ao editar a documentação (21/09/2026).
     ! Motivo: as convenções do Memorial (tag em comentário HTML, números só de script, formato das seções de pesquisa) viviam em briefs e no chat; aqui ficam onde o editor de Markdown as vê. -->
# Documentação (Memorial, ABNT, README, claude-memoria)
- Tag em comentário HTML logo acima do trecho tocado: `<!-- ! Alteração de IA - Revisar: … ! Motivo: … -->`, motivo amarrado ao defeito real.
- Nenhum número de resultado digitado à mão: copiar de `resumo_fase3.json`, `comparacao_fases.md`, `decisao_modelo.md` ou do relatório de tarefa, citando o campo na primeira menção; o que não tem origem fica `[conferir]`.
- Hipóteses H1–H6 (achado 4.29, plano da Fase 3, relatório §2) não mudam uma letra; vereditos entram em linhas separadas.
- Seções da pesquisa (`levantamento-*.md`) seguem o formato `#### 6.9.N Título (`key` — X aprovadas, Y rejeitadas)` / `*Título da síntese:*` / `##### Texto` / `##### Implicações para a Fase 3` (`* `) / `##### Lacunas` (`* `) / `##### Referências ABNT do tópico` (`- `); referências ABNT NBR 6023 com "Disponível em: … Acesso em: …".
- Tudo que foi avaliado e descartado fica registrado com o motivo (é insumo do documento final do TCC).
- Links relativos ao arquivo; conferir com `ferramentas/conferir_docs.py` antes de entregar.
