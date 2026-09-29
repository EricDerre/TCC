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
<!-- ! Alteração de IA - Revisar: duas regras novas (28/09/2026) — o formato de ficha das pendências e as palavras fixas de estado do roadmap.
     ! Motivo: o Eric pediu as pendências em linguagem direta, sem jargão, e um painel que as mostre por pergunta; o painel (ferramentas/gerar_dashboard.py) só consegue montar um cartão por pendência e colorir fases e corridas se o formato e as palavras de estado forem sempre os mesmos. -->
- Pendências (`Documentacao/memorial/pendencias.md`): uma ficha por pendência, no formato `### N. Título` seguido de `- **Estado:**` (`aberta` ou `fechada em DD/MM/AAAA`), `- **Quem decide:**`, `- **Aberta em:**`, `- **O que é:**`, `- **Por que importa:**`, `- **Opções:**` (subitens `  - (a) …`), `- **Recomendação:**` e `- **Decisão:**` (`em aberto` até sair). Linguagem direta, como nos comentários de código: sem jargão, termo técnico explicado na primeira menção, arquivos, comandos e telas reais citados. Fechar é trocar o Estado e preencher a Decisão — nunca apagar; o texto antigo fica no bloco "Histórico". `ferramentas/testar_painel_textos.py` confere o formato.
- Roadmap (`Documentacao/memorial/roadmap.md`): a célula "Estado" da tabela §1 começa com `Concluída`, `Em andamento` ou `Não iniciada`; a coluna "Estado" da tabela §2 começa com `feita`, `rodando`, `pendente`, `opcional` ou `aguarda` — o painel colore por essas palavras. Depois de mudar qualquer um dos dois arquivos, regerar o painel (`python ferramentas/gerar_dashboard.py`) e republicá-lo no mesmo endereço.
