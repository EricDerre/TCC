<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
<!-- ! Alteração de IA - Revisar: em 11/09/2026 foram fechadas as pendências dos fixtures do
     achado 4.20 e da escolha do padrão de produção, e acrescentadas as que a Fase 3 abre
     (rodar a bateria, preencher os relatórios, revisar as edições, rodada complementar da
     pesquisa, conferir o Faceli 3. ed., o log fora do git).
     ! Motivo: as duas primeiras já tinham sido resolvidas — os 4 fixtures foram corrigidos
     (decisão 34) e a escolha do modelo passou a ser o resultado da Fase 3 (decisão 36) —, e
     pendência resolvida que continua na lista faz o Eric reabrir uma investigação encerrada.
     As novas ficam registradas antes de a bateria rodar porque uma delas (quando ocupar a
     máquina por ~60 h) é decisão dele, não do harness. -->
<!-- ! Alteração de IA - Revisar: o link do cabeçalho para o índice virou
     ../Memorial%20de%20Desenvolvimento.md (era ../../).
     ! Motivo: este arquivo fica em Documentacao/memorial/, um nível acima dos demais tópicos,
     que ficam em memorial/1-.../ e por isso usam ../../. Com dois níveis, o caminho saía de
     Documentacao/ e apontava para a raiz do repositório, onde não existe
     "Memorial de Desenvolvimento.md" - o link do topo não abria. -->
<!-- ! Alteração de IA - Revisar: em 12/09/2026 (revisão final da Fase 3): a pendência do PDF
     passou a dizer quantos comentários de marcação há para remover (20); a da bateria registra
     o piloto de 10 casos e a projeção do executor; a da rodada complementar da pesquisa passou
     a dizer o que ela é (as lacunas das oito seções "Lacunas" do levantamento, uma por tópico)
     e por que continua adiada; e entraram quatro pendências novas do Eric — Ollama 0.34.0 (não
     reverter), `Tee-Object` em `rodar_fase2b.ps1`/`fase2b.log`, cinco referências ABNT sem
     URL/DOI e o cronograma do ABNT sem linha para a Fase 3.
     ! Motivo: cada uma tem origem verificada e nenhuma estava aqui — a contagem de 20 é
     `grep -c "<!--"` no documento ABNT em 12/09/2026, já com as duas marcações da revisão
     final do mesmo dia (§2.4 e §3.4); o piloto e a projeção vêm dos
     relatórios da T12 e da T7; "8 lacunas" não dizia que lacunas eram; o Ollama atualizou
     sozinho antes da bateria e a decisão de não reverter precisa ficar visível para o Eric;
     o defeito do `Tee-Object` foi achado no piloto (`fase3.log` com bytes UTF-16) e existe
     igual no `.ps1` da 2-B, que é fase fechada — mexer nele é decisão do Eric; as cinco
     referências e o cronograma vieram da revisão do documento ABNT (T15). -->
<!-- ! Alteração de IA - Revisar: segunda passada de 12/09/2026 — no bullet do `Tee-Object`,
     "limitação conhecida, sem correção" dos acentos no `fase3.log` passou a registrar que a
     correção existe e já está no `rodar_fase3.ps1`; no bullet do cronograma do ABNT, a tabela
     passou a ser descrita como é (Mês 1 a Mês 7, sem linha para a biblioteca gerida pelo modelo).
     ! Motivo: a revisão da T12 (12/09) concluiu que `[Console]::OutputEncoding` em UTF-8 resolve
     os acentos e que o relatório da T12 errava ao dizer "sem correção"; a onda final de correções
     pôs `[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)` no
     `rodar_fase3.ps1`, antes de chamar o Python (arquivo gravado às 19:26 de 12/09; o
     `fase3.log` do piloto, das 10:46, é anterior e continua com `├º`). Pendência que diz "sem
     correção" quando há uma manda o Eric conviver com um defeito já resolvido. O cronograma do
     ABNT (§5) tem sete linhas, Mês 1 a Mês 7 — "vai de Mês 2 a Mês 3" descrevia uma tabela de
     duas linhas. -->
# Pendências e questões em aberto

Parte do [Memorial de Desenvolvimento](../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá.

## 8. Pendências e questões em aberto

- **Regerar o PDF** do projeto de pesquisa a partir do Markdown corrigido, e remover os **20 comentários de marcação** (`<!-- ! Alteração de IA … -->`, contados em 12/09/2026, depois da revisão final) antes da entrega final.
- **Fichamento formal** das 7 referências: o recorte de cada uma já está embutido nas seções 2.2 a 2.6 do projeto de pesquisa, mas não existe documento de fichamento separado.
- **Fechada em 11/09/2026 — padrão de produção do modelo**: deixou de ser uma escolha a fazer sobre os números da 2-B e passou a ser o resultado da Fase 3, pela acurácia balanceada nos 36 casos de avaliação, com veto por autoenvenenamento (decisão 36). A restrição de licença continua valendo como critério de desempate — `qwen2.5-coder:3b` tem licença de pesquisa; `qwen2.5:7b` e `granite4.2:8b` são Apache 2.0 — e o `install.py` segue apontando para o 3b até a decisão sair.
- **Validação em Linux**: o instalador foi testado apenas em Windows. Os caminhos de `apt` e `brew` seguem convenções estabelecidas, mas não foram executados.
- **Critérios de aceitação quantitativos**: definidos no planejamento (fórmula de MTTR, Task Success, linha de base manual, volume), mas ainda não incorporados ao corpo do projeto de pesquisa além da §3.4.
- **Fase 2-B concluída na máquina-alvo** (07–09/09/2026; relatório em `3-resultados-e-analises/fase-2b-relatorio-por-modelo.md`). Decisões que ela deixou para o Eric:
  - **Modelo padrão de produção** entre `qwen2.5-coder:3b` + A2 (63%, 30 s, 2,3 GB, licença de pesquisa), `qwen2.5:7b` + A2 (70%, 61 s, 5,2 GB, Apache 2.0) e `granite4.2:8b` + A2 (77%, 124 s, 6,6 GB, Apache 2.0). O `install.py` ainda aponta para o 3b. **Passou a ser decidida pela Fase 3** (ver acima).
  - **Modo de operação do agente = biblioteca recuperada (A2)**; biblioteca inteira no prompt descartada.
  - **Melhorar o recuperador antes de trocar de modelo**: hit@3 de 79% limita o Granite a 77% (com o verbete certo, 100%). Experimentos baratos e offline: k = 5 (hit@5 já é 90%), sinais em código para a classe de tradução (verbete certo no top-3 em só 47%), embedding denso `embeddinggemma:300m` via `validar_banco.py --embedding`.
  - **Validação por código como porta obrigatória da biblioteca** na Fase 3 (achado 4.24: verbete errado é seguido em 93–96% dos casos).
- **O `fase2b.log` da máquina-alvo não foi versionado** (`*.log` no `.gitignore`); ele contém a Verificação 0 do i5. Versionar com `git add -f` ou tirar `*.log` da regra para `experimentos/resultados_alvo/`. **O mesmo vale para o `fase3.log`**, que a bateria da Fase 3 grava em `resultados_alvo/fase3/`: sai do commit pela mesma regra, e é o único registro corrido da execução (projeções de tempo, época a época, abortos). Se interessar guardar, é `git add -f`.
- **Fechada em 11/09/2026 — corrigir os fixtures que contradizem o código** (4.20): os quatro (`sin-1`, `sin-2`, `semt-13`, `efe-13`) foram corrigidos antes de a Fase 3 rodar (decisão 34), com o efeito na recuperação e no pareamento entre fases registrado no fechamento do achado 4.20. **Não é pendência** a imprecisão equivalente dentro da biblioteca original — o verbete `negocio/pagina-produtos-api.md` lista nos `sintomas` a mesma descrição que o código não produz: ela foi mantida de propósito (é a versão L0 de todos os modelos e é a mesma com que a 2-B rodou) e vira alvo de observação na Fase 3.
- **Ablação base × instruct** (`qwen2.5:0.5b-base` × `0.5b-instruct`) como piso metodológico, se a banca pedir um "modelo sem instrução" no lugar do GPT-2.

### Abertas pela Fase 3 (11/09/2026)

<!-- ! Alteração de IA - Revisar: pendência fechada em 21/09/2026 (a bateria rodou em 13–15/09) e bloco novo "Abertas pelo plano complementar (21/09/2026)" ao fim do arquivo.
     ! Motivo: o texto ainda dizia "o Eric decide quando a máquina pode ficar ocupada"; os marcos vêm de `resultados_alvo/fase3/fase3.log` e de `maquina.json` (Ollama 0.34.0; 3 relances = 1 por modelo). -->
- **Fechada em 15/09/2026 — Rodar a bateria da Fase 3** (rodou de 13/09 08:45 a 15/09 18:44: `FIM da Fase 3 - duracao total 58h59 - modelos com falha: nenhum`, 57h59 entre o primeiro e o último marco; 2.088 inferências; Ollama 0.34.0; resultados no commit b9f9ad9). Texto original da pendência: 4 modelos × 3 épocas, 522 inferências por modelo, **~60 h de CPU** na máquina-alvo. O Eric decide quando a máquina pode ficar ocupada; o piloto mede a projeção real antes. A bateria é resumível (época fechada é pulada, época aberta é reconstruída do JSONL), então pode ser partida em pedaços. O piloto de 10 casos do orquestrador rodou em 12/09/2026 (`rodar_fase3.ps1 -Piloto`: `qwen2.5-coder:3b`, 1 época, 00h13, 0 de 6 propostas aceitas; a retomada reconstruiu a `epoca-1` com o mesmo hash); a projeção do executor (`--so-projecao`) para os 4 modelos × 3 épocas é de **67,18 h**, contra ~60 h do plano.
<!-- ! Alteração de IA - Revisar: duas pendências fechadas em 22/09/2026 (relatórios preenchidos; revisão das edições em primeira passada pela IA, a pedido do Eric). ! Motivo: os textos abaixo são os originais; o que restou de cada uma (revisão dos vereditos pelo Eric, regeneração combinada do resumo) está no bloco de 22/09 ao fim do arquivo. -->
- **Fechada em 22/09/2026 — Preencher os relatórios da Fase 3** (§2–§9 e §12 do relatório, §3–§6 da comparação, vereditos no 4.29 e achados 4.30–4.35, mais [`analise-decisoria-modelo-final.md`](3-resultados-e-analises/analise-decisoria-modelo-final.md); tabelas por `gerar_tabelas_relatorio_fase3.py --check`). Texto original: `3-resultados-e-analises/fase-3-relatorio-por-modelo.md` e `comparacao-entre-fases.md` estão pré-registrados com os lugares dos números marcados; cada número sai de `resumo_fase3.json`, `avaliacao_fase3.json` e `comparacao_fases.md`, nenhum digitado à mão. Os vereditos das hipóteses H1–H6 entram no achado 4.29.
- **Fechada em 22/09/2026 (primeira passada pela IA; o Eric revisa) — Revisão humana das edições**. Texto original: o Eric preenche `Correta` / `Parcial` / `Errada` nos arquivos `resultados_alvo/fase3/revisao_edicoes__<modelo>.md` (até 30 edições por modelo) e `avaliar_fase3.py` reapura. A validação em código diz se a edição podia entrar; só a leitura humana diz se ela está certa sobre o sistema.
<!-- ! Alteração de IA - Revisar: pendência fechada em 21/09/2026 (rodada 2 integrada em §6.9.9–6.9.17 e mapa em §6.10). ! Motivo: o Workflow pesquisa-r2 fechou as oito lacunas (146 aprovadas, 6 rejeitadas, 1 além do teto em 153 verificações; 104 referências novas) e a integração foi feita por ferramentas/integrar_pesquisa.py; o texto abaixo é o original da pendência. -->
- **Fechada em 21/09/2026 — Rodada complementar da pesquisa bibliográfica**: as lacunas das oito seções "Lacunas" do levantamento de 11/09/2026 (uma por tópico) não chegaram a ser pesquisadas, por limite de sessão, e continuam adiadas até a onda final da Fase 3 terminar — em 12/09 dois workflows simultâneos derrubaram agentes por limite de sessão, e nada no repositório depende dessa rodada para o Eric commitar. Ficam listadas em [`2-pesquisa-e-literatura/levantamento-2026-09-11-fase-3.md`](2-pesquisa-e-literatura/levantamento-2026-09-11-fase-3.md), para não se perderem.
- **Conferir os capítulos do Faceli 3. ed. (2025) com o exemplar**: a edição e o sumário foram verificados na ficha da editora, mas o conteúdo dos capítulos citados (Cap. 10, avaliação de modelos preditivos, entre outros) não foi lido no livro. Citação com número de página exige o exemplar em mãos (decisão 37).
- **Ollama 0.34.0 — não reverter**: o runtime atualizou sozinho de 0.33.3 (bateria da 2-B) para 0.34.0 em 12/09/2026, antes da bateria da Fase 3 (a máquina é corporativa e a atualização é automática). Decidido não reverter: a Fase 3 roda em 0.34.0, `maquina.json` grava a versão e a decisão 44 a põe em todo registro; o relatório da Fase 3 (§11) e a comparação entre fases declaram a diferença de versão como fator não controlado no pareamento 2-B A2 × F3 L0. Registrado para o Eric saber que a bateria não roda na versão da 2-B.
- **`Tee-Object` em `rodar_fase2b.ps1` grava o log em UTF-16** (o `fase2b.log` já gravado tem trechos assim, com bytes nulos): é o mesmo defeito encontrado e corrigido em `rodar_fase3.ps1` no piloto de 12/09/2026 (trocado por `ForEach-Object` + `Add-Content -Encoding utf8`). A 2-B está fechada e seus arquivos em `resultados_alvo/` não mudam; aplicar o mesmo patch em `rodar_fase2b.ps1` (só corridas futuras) é decisão do Eric. Os acentos trocados no `fase3.log` do piloto (`recupera├º├úo`) eram outro defeito — o PowerShell decodificava a saída do Python pela codepage do console — e têm correção: a revisão da T12 (12/09) concluiu que `[Console]::OutputEncoding` em UTF-8 resolve, e a onda final de correções pôs `[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)` no `rodar_fase3.ps1`, antes de chamar o Python; conferido no piloto v2 de 13/09/2026 (`fase3.log` novo: 0 bytes nulos e 0 acentos trocados). <!-- ! Alteração de IA - Revisar: em 13/09/2026 "conferir no próximo lançamento" virou o resultado da conferência. ! Motivo: o piloto foi repetido com o .ps1 corrigido e o log saiu legível; deixar a frase antiga mandaria o Eric conferir o que já está conferido. --> Afeta só a legibilidade do log; os JSONL/JSON gravados pelos scripts Python estão em UTF-8 correto.
- **Cinco referências do projeto ABNT sem URL/DOI** — BISWAS, JÚNIOR, MACIAK, SHI e ZHANG, J.: o endereço não existe em nenhum arquivo do repositório; completar exige localizar a fonte (Eric).
- **Cronograma (§5) do projeto ABNT sem linha para a Fase 3**: a tabela (Mês 1 a Mês 7) passa de "Mês 2 — configuração do ambiente e da camada de inferência, incluindo a comparação entre portes de modelo" a "Mês 3 — Módulo de Filtragem de Contexto e extração da Accessibility Tree" sem nenhuma linha para a biblioteca gerida pelo modelo, que a §3.2 já descreve (Eric).
  Sugestão de linha (21/09/2026), para o Eric colar na tabela do §5 entre o Mês 2 e o Mês 3: `| Mês 2 (continuação) | Comparação experimental dos modelos em três fases: prompts sem documentação (2-A), biblioteca de documentação recuperada (2-B) e biblioteca editada pelo próprio modelo em épocas atrás de validação em código (3), com análise decisória do modelo final. |`

## Abertas pelo plano complementar (21/09/2026)

<!-- ! Alteração de IA - Revisar: bloco novo com o que o plano complementar de 21/09/2026 abriu ou deixou para o Eric.
     ! Motivo: o plano vive fora do repositório (`~/.claude/plans/`) e o handoff em `claude-memoria/contexto/`; a lista de pendências precisa dizer sozinha o que falta e quem faz. -->
- **Fechada em 22/09/2026 (primeira passada pela IA) — Revisão humana das 63 edições** (`resultados_alvo/fase3/revisao_edicoes__qwen2.5-coder_3b.md` 10 linhas, `…__qwen2.5-coder_7b.md` 24, `…__qwen2.5_7b.md` 29): o Claude escreveu `Correta` / `Parcial` / `Errada` e um comentário por linha, conferindo contra o código do cobaia (decisão 53). Resultado: 23 / 17 / 23; no `qwen2.5:7b`, 9 / 8 / 12. O que resta ao Eric está no bloco de 22/09 abaixo.
- **Versionar os logs das baterias**: `git add -f Programacao/AgenteCore/experimentos/resultados_alvo/fase3/fase3.log Programacao/AgenteCore/experimentos/resultados_alvo/fase2b.log` (decisão do Eric em 21/09; a regra `*.log` do `.gitignore` continua). — Eric.
- **Fechada em 22/09/2026 — Atualizar o Claude Code**: o Eric atualizou pela própria instalação; o atalho antigo do npm (`%AppData%\npm\claude.ps1`) ficou apontando para um `claude.exe` inexistente — conferir `claude --version` num terminal novo e remover o atalho se ainda estiver no PATH (detalhe no handoff de 22/09). Texto original: (2.1.245 → atual): `claude update` falhou nesta máquina sem acesso ao npm; a estatística de cache do `/usage` só existe a partir da 2.1.251.
- **Fechada em 21/09/2026 à noite, sem o Granite — Ponte de versão do Ollama** (0.34.0 na bateria → 0.34.1): `qwen2.5-coder:3b`, `qwen2.5:7b` e `qwen2.5-coder:7b` nos 36 (b/c 0/0, 0/0 e 1/1; `decisao_modelo.md` §6; relatório §11); o `granite4.2:8b` foi pulado nas duas tentativas (7,8 GB livres contra 8 GB) e o Eric decidiu não insistir (decisão 52): fica sem ponte e fora da 3-B. Texto original: 144 diagnósticos com a biblioteca original nos 36 casos de avaliação, 4 modelos, ~2,5 h, antes de qualquer teste da Fase 3-B; relançar com `powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo ponte -Saida fase3b_ponte` — o script retoma de onde parou.
- **Fase 3-B (testes complementares)**: menu com custo e recomendação em [`analise-decisoria-modelo-final.md`](3-resultados-e-analises/analise-decisoria-modelo-final.md) §10 — (b) troca cruzada primeiro (L1 e L3 do `qwen2.5:7b` lidas pelo Coder 7B e pelo 3B, 144 inferências, ~2,5 h, uma noite: `powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo cruzada -Saida fase3b_cruzada_qwen -Doador qwen2.5:7b -Versoes 1 3 -Modelos qwen2.5-coder:7b qwen2.5-coder:3b`), depois (a) casos inéditos (autoria por agente + 6 casos conferidos pelo Eric, ~3 h de máquina); (c) A5 por último; (d) Granite inviável. — Eric escolhe.
- **`install.py` e README apontam para o `qwen2.5-coder:3b` como modelo padrão**: a decisão saiu em 22/09/2026 (decisão 52: `qwen2.5:7b` com a biblioteca L1); trocar o padrão de `install.py` para `qwen2.5:7b` e apontar a biblioteca de produção para a cópia L1 curada (item abaixo). — Eric.

## Abertas pela análise decisória (22/09/2026)

<!-- ! Alteração de IA - Revisar: bloco novo com o que a análise decisória e a revisão das edições deixaram para o Eric.
     ! Motivo: a decisão do modelo saiu com dois "depois" que só o Eric fecha — revisar os vereditos que a IA deu e curar a cópia L1 — e o resumo oficial da bateria não é regravado sem combinar. -->
- **Revisar os 63 vereditos dados pela IA** nas três planilhas `revisao_edicoes__*.md` (coluna Avaliação e Comentário preenchidos; critério na tag do arquivo e no relatório §7). Trocar o que discordar; a apuração é automática (`decidir_modelo.py` lê as planilhas). — Eric.
- **Regeneração combinada de `resumo_fase3.json` e `relatorio_fase3.html`** com a revisão apurada: `python avaliar_fase3.py --saida fase3` (com `RESULTADOS_DIR=resultados_alvo`, na venv ou no Python do sistema) — só `revisao_humana` e `gerado_em` mudam; conferir com `git diff` antes de commitar. Até lá `decidir_modelo.py` lê as planilhas direto (campo `fonte`). — Eric autoriza; Claude roda.
- **Curadoria da cópia L1 do `qwen2.5:7b`** antes da Fase 4: revisar as 30 edições da época 1 que ficaram fora da amostra (a planilha cobre 10 das 40), remover as reprovadas numa **cópia** de `resultados_alvo/fase3/bibliotecas/qwen2.5_7b/epoca-1/` (o snapshot oficial não muda) e registrar o hash da cópia curada; as 3 já reprovadas estão em `analise-decisoria-modelo-final.md` §8. — Eric (a IA pode fazer a primeira passada, como nas 63).
- **Commit do working tree de 22/09** (relatórios, análise decisória, achados 4.30–4.35, mapa, decisões 52–54, planilhas, `gerar_tabelas_relatorio_fase3.py`, `tabelas_relatorio.md`, `decidir_modelo.py`, `testar_fase3b.py`, `cache_respostas.py` e teste, `integrar_pesquisa_llms.py`, levantamento das LLMs locais, `resultados_alvo/fase3b_ponte/`; e, se ficarem, `.mcp.json` e `.cbmignore`). — Eric.
- **codebase-memory-mcp — regra de permanência** (decisão 49): o servidor está instalado (npm, 0.11.0) e registrado em `.mcp.json` (escopo de projeto); na próxima abertura do Claude Code ele pede confirmação. Na primeira sessão com o servidor ativo: indexar o repositório (`.cbmignore` já exclui venvs, `resultados*`, `base_conhecimento`, `.superpowers`, PHPMailer, `Documentacao/`), repetir as três tarefas fixas pelas ferramentas MCP (usos de `TETO_TOKENS_CONTEXTO`; rastro `validar_proposta → aplicar_edicao`; quem lê `fechamento.json`) e comparar com `medir_tokens.py`; fica só com ≥ 20% de economia sem incidente, senão `npm uninstall -g codebase-memory-mcp`, remover `.mcp.json`/`.cbmignore` e registrar em `ferramental-do-claude-code.md` §7.2 (leitura preliminar pela CLI: tendência a sair). — Claude na próxima sessão; Eric decide.
- **Confirmar a instalação do `pyright-lsp`** na próxima abertura (ligado em `.claude/settings.json`); se o marketplace não instalar sozinho, `/plugin` → instalar `pyright-lsp@claude-plugins-official`. — Eric/Claude.
- **Três scripts da raiz sem BOM e com travessão em comentário** (`build_exe.ps1`, `install.ps1`, `run.ps1`, anteriores à regra do CLAUDE.md): `ferramentas/conferir_docs.py` os reporta como aviso; o parse no Windows PowerShell 5.1 foi conferido em 21/09/2026 (os travessões estão em comentários, não em strings). Decidir se padroniza com BOM ou mantém. — Eric.
