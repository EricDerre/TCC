<!-- ! Alteração de IA - Revisar: documento de passagem de bastão da sessão de trabalho no
     Ryzen (31/08 a 09/09/2026) para o Claude Code que vai continuar o projeto na máquina-alvo.
     ! Motivo: uma sessão do Claude não viaja entre máquinas; o que viaja é a memória (pasta
     memory/), as regras (CLAUDE.md) e o repositório. Este arquivo cobre o que fica de fora
     disso: como o harness está montado, o que cada script faz, o estado de cada fase, as
     armadilhas já pagas e o jeito de trabalhar que o Eric espera. É para ser lido UMA vez,
     no início da primeira sessão na máquina-alvo, e depois consultado por tópico. -->

<!-- ! Alteração de IA - Revisar: atualização de 11/09/2026 — tabela de fases (§2) separa a
     Fase 3 (biblioteca gerida pelo modelo) da Fase 4 (interceptador Playwright), que antes
     estavam numa linha só; corrigido o ponteiro que apontava para seções inexistentes de
     `plano-aprovado-fase-2b.md`; acrescentadas as linhas dos scripts novos da Fase 3 em §3
     (harness) e duas armadilhas novas em §4 (regex do slug corrigida; pastas novas no
     `.gitignore`).
     ! Motivo: este arquivo é lido uma vez, no início da primeira sessão numa máquina nova;
     sem a atualização ele continuaria mandando ler seções que não existem no plano da 2-B e
     omitindo que a Fase 3 já está em implementação desde 11/09. -->
<!-- ! Alteração de IA - Revisar: atualização de 12/09/2026 (revisão final da Fase 3) — na
     tabela de §2 a Fase 3 passa a "implementada e revisada; piloto executado; bateria
     aguardando decisão"; em §3 os seis scripts perdem a marca "(em implementação)" e o
     validador passa a "30 códigos de rejeição em 26 checagens"; em §4 a armadilha dos fixtures
     4.20 é marcada como feita; em §5 o item que se chamava "Fase 3 (plano aprovado)" passa a
     "Fase 4 (desenho aprovado no plano da 2-B)", o baseline de 82,4% recebe [conferir] e a lista
     de decisões pendentes do Eric deixa de incluir os fixtures 4.20.
     ! Motivo: (1) todos os scripts da Fase 3 existem, foram revisados e rodaram no piloto de
     12/09/2026 — "em implementação" mandaria o leitor esperar código que já está pronto;
     (2) `CODIGOS_REJEICAO` tem 30 códigos, não 26; (3) os fixtures foram corrigidos em 11/09
     (decisão 34) e "corrigir antes de nova bateria" faria alguém corrigir de novo; (4) o item
     de §5 descrevia o interceptador Playwright, a poda e a cura de seletor — que a tabela de
     §2 e a decisão 29 chamam de **Fase 4** — sob o nome "Fase 3", contradizendo o próprio
     arquivo; e os 82,4% não têm origem conferida neste repositório (o Memorial §6.1 cita
     JOSEPH, 2026, como fonte a conferir). -->
<!-- ! Alteração de IA - Revisar: segunda passada de 12/09/2026 — o rótulo do item de §5 que a
     tag acima tinha posto como "Fase 4 (desenho aprovado no plano da 2-B)" passou a "Fase 4
     (pedido do Eric na sessão do Ryzen; nome fixado na decisão 29, plano da Fase 3)".
     ! Motivo: a nota de §2 deste mesmo arquivo diz que `plano-aprovado-fase-2b.md` não tem
     seções Fase 3/Fase 4, e uma busca por Playwright, interceptador, acessibilidade, seletor,
     self-healing e "Fase 4" nesse plano não acha nada do desenho — só a nota de que a gestão da
     biblioteca vira Fase 3. O rótulo anterior apontava uma origem que não existe e contradizia
     a própria nota; o novo é coerente com o título de §5 ("O que o Eric pediu para as próximas
     fases") e com a decisão 29, que é onde o nome "Fase 4" ficou fixado. -->
# Passagem de bastão — sessão no Ryzen, 31/08 → 09/09/2026

Leia primeiro `CLAUDE.md` (regras) e a pasta `memory/` (decisões). Depois este arquivo. Não substitui o Memorial: para decisões, achados e fontes, o lugar é `Documentacao/Memorial de Desenvolvimento.md` (índice) e `Documentacao/memorial/`.

## 1. Quem e o quê

- **Eric** (eric.derre@…) é quem decide, revisa e **commita**; nunca commitar, nunca `git add`. Ele fala português, gosta de relatório detalhado com número e fonte, e de saber por que cada coisa foi feita (a tag `! Alteração de IA - Revisar` + `! Motivo:` em todo arquivo tocado).
- TCC "Agente de QA End-to-End Autônomo com Self-Healing" (UNICID, 9 autores). Objeto: diagnosticar quebra de contrato na fronteira front-end ↔ API com LLM **100% local, só CPU, em máquina corporativa**.
- **Esta máquina (i5-1235U, 16 GB, sem GPU) é a máquina-alvo e, a partir de 09/09, a principal.** Os tempos que valem para a tese são os daqui. O Ryzen 7 5800H foi só desenvolvimento.

## 2. Estado do projeto em 09/09/2026

| Fase | Estado | Onde ler |
|---|---|---|
| Ambiente cobaia (CobaiaFront PHP legado + CobaiaAPI FastAPI + banco único + instalador "hit and run" + `Cobaia.exe`) | pronto, 13 testes passando | `README.md` |
| Fase 1 — fundamentação e correções do documento ABNT | feita | `memorial/4-projeto-de-pesquisa-abnt/` |
| Fase 2-A — 6 modelos × 90 casos × 3 estratégias (Ryzen) | concluída | `memorial/3-resultados-e-analises/fase-2a-relatorio-por-modelo.md` |
| Fase 2-B — biblioteca de documentação, 6 condições (máquina-alvo) | concluída, 2.610 inferências | `…/fase-2b-relatorio-por-modelo.md` |
| **Fase 3** — biblioteca gerida pelo próprio modelo, por modelo e por época (teste 3) | implementada e revisada (12/09); piloto de 10 casos executado; bateria completa (~60 h) aguardando a decisão do Eric | `claude-memoria/plano-aprovado-fase-3.md` |
| Fase 4 — interceptador Playwright, poda da árvore de acessibilidade, cura de seletor | não começou | descrito em §5 deste arquivo |
| Fase 5 — MTTR / Task Success com injeção de falhas | não começou | plano, seção Fase 5 |

Nota (11/09/2026): o plano da 2-B (`plano-aprovado-fase-2b.md`) não tem seções "Fase 3"/"Fase 4"; o que foi aprovado para as fases seguintes está na §5 abaixo e em `plano-aprovado-fase-3.md`.

Os dez achados que mandam no desenho, em uma linha cada (números e fontes no Memorial §4):
1. O modelo não compara estruturas: o diff de contrato é calculado em código e entregue pronto (4.12).
2. O tempo é dominado pela prolixidade, não pelo porte (4.13).
3. Raciocinar em estágios não ajuda modelos de 1,5–7B e prejudica o 8B; prompt fixo em linear (4.16).
4. Três modos de falha diferentes: confusão entre vizinhos, colapso num rótulo, rótulo inventado (4.17).
5. Tokenizador real gasta 2,6–2,8 chars/token; orçamento de `num_ctx` é apertado e o Ollama descarta o **começo** do prompt em silêncio quando estoura (4.18).
6. Recuperação precisa de sinais calculados em código: hit@3 de 59% → 79% (4.19).
7. O cache de prefixo do Ollama funciona em CPU, e `prompt_eval_count` **não** o revela — só `prompt_eval_duration` (4.21).
8. Biblioteca **recuperada** (top-3) sobe o acerto em todos os modelos; a **inteira** não; 3 modelos passam de 70% (4.22).
9. O teto é o recuperador: com o verbete certo o Granite acerta 100% (4.23).
10. Documentação errada é seguida em 93–96% dos casos — validação por código é obrigatória antes de qualquer gestão automática da biblioteca (4.24).

## 3. Como o harness está montado (`Programacao/AgenteCore/`)

```
base_conhecimento/          36 verbetes .md com frontmatter plano (negocio/ contratos/ erros/ falhas_injetadas/ defeitos_conhecidos/), INDICE.md gerado
experimentos/
  caminhos.py               ONDE gravar/ler: RESULTADOS_DIR (env) → resultados_alvo/ ou padrão resultados/ (Ryzen)
  cliente_ollama.py         gerar() só CPU, num_ctx 8192, temp 0.1, grava prefill/geração; embed(); residentes(); descarregar()
  taxonomia.py              6 classes, 3 níveis, 23 causas raiz, validar_caso()
  banco_casos.py (+_extra)  90 fixtures com gabarito — NÃO são chamadas ao vivo
  estrategias.py            linear / estágios (compilador, domínio) / linear_com_biblioteca (biblioteca ANTES do caso)
  biblioteca.py             parser do frontmatter, render() dos verbetes, validador (esquema, referências reais, sobreposição com casos, cobertura das 23 causas), tetos
  recuperacao.py            sinais do caso (endpoint, entidade, status) + sinais em código (JSON parseia? cortado? diff contra contrato?) + BM25; contextos A1–A5
  executar_bateria.py       --modelos M --condicao A0..A5 [--estrategias] ; um modelo por vez; JSONL por caso (resumível); guardas contra estouro de num_ctx
  avaliar.py                gabaritos → avaliacao.json + resumo_metricas.json; Δ vs A0 com McNemar exato; Wilson; ancoragem; recuperação; flips de quantização
  gerar_graficos.py         01–11 em PNG/SVG (paleta de 3 matizes, rótulo em toda barra, "sem dado" explícito)
  gerar_relatorio.py        relatorio.html navegável (respostas cruas)
  validar_banco.py          valida casos + biblioteca + mede a recuperação offline (--embedding MODELO para o denso; --indice regrava INDICE.md)
  verificar_cache_prefixo.py  Verificação 0: cache de prefixo pelo prefill_ms
  rodar_fase2b.ps1          orquestrador da 2-B para esta máquina (checagens, downloads, A0 refeito, A1–A5, avaliação)
  evolucao_biblioteca.py    parser das propostas de edição, validador (30 códigos de rejeição em 26 checagens), aplicação só por acréscimo, hash/diff/fechamento de época
  executar_fase3.py         laço de diagnóstico + proposta por modelo e por época; retomável por (modelo, época, caso, tipo)
  avaliar_fase3.py          pontua por modelo × L0..L3 × partição; McNemar, Cochran Q, Wilson, flips
  comparar_fases.py         junta 2-A, 2-B e Fase 3 em comparacao_fases.json/.md
  gerar_graficos_fase3.py   figuras 12–17 (acerto por época, recuperação, motivos de rejeição, crescimento da biblioteca)
  gerar_relatorio_fase3.py  relatorio_fase3.html navegável por modelo/época/partição
  testar_fase3.py           testes em Python puro (sem pytest) do parser, validador e hash da Fase 3; sem LLM, < 30 s
  rodar_fase3.ps1           orquestrador da Fase 3; -Piloto roda amostra pequena antes da bateria completa
  resultados/               Ryzen (2-A + 48 casos parciais de Q8)      resultados_alvo/   i5 (2-B completa, maquina.json)
  resultados_alvo/fase3/    bibliotecas por modelo (epoca-0..3/), diagnósticos e propostas por época, avaliação, comparação entre fases, relatório
```

Rodar qualquer coisa que leia resultados desta máquina: `$env:RESULTADOS_DIR = "resultados_alvo"` antes (ou o `.ps1` já faz).

## 4. Armadilhas já pagas (não pagar de novo)

- **Um modelo residente por vez**, `num_gpu=0`, `num_ctx=8192` — regra do Eric; os scripts recusam começar com outro modelo carregado (`ollama ps`).
- **`.ps1` só com UTF-8 com BOM** e `-` no lugar de `—` nas strings; sem BOM o PowerShell 5.1 lê `—` como aspas de fechamento e o arquivo inteiro não parseia. A ferramenta de escrita grava sem BOM: converter depois (`[System.IO.File]::WriteAllText(f, t, UTF8Encoding($true))`).
- **Console cp1252**: os scripts reconfiguram `sys.stdout` para UTF-8 (`cliente_ollama.py`/`biblioteca.py`); ao rodar scripts fora deles, `$env:PYTHONIOENCODING = "utf-8"`.
- **Heredocs e `python -c` longos na ferramenta Bash quebram com aspas simples do português**: gravar o script num arquivo (scratchpad) e executar.
- **`num_ctx` estoura em silêncio**: o Ollama descarta o começo do prompt (a biblioteca). As guardas em `executar_bateria.py` (estimativa por caracteres e contagem real na 1ª inferência) existem por isso — não remover.
- **`prompt_eval_count` mente sobre o cache**; usar `prompt_eval_duration`.
- **Tags do Ollama são ponteiros mutáveis**: o digest sha256 vai em cada registro.
- **`*.log` está no `.gitignore`**: o `fase2b.log` desta máquina (com a Verificação 0 do i5) não foi versionado — se ainda existir, `git add -f` vale a pena.
- **Fixtures que contradizem o código** (achado 4.20: "R$ NaN", cartões duplicados) — **feito em 11/09/2026** (decisão 34), antes da Fase 3; os 4 casos caíram na partição de aprendizado, então os 36 de avaliação continuam pareáveis com a 2-B.
- Gráficos: até 3 matizes por figura, rótulo em cada barra, `ylim` com folga acima de 100% (rótulo colidia com o subtítulo), variantes de quantização fora das figuras de condição.
- A memória do Claude usa o slug com `.` trocado por `-` (`c--Users-Eric-Derre-…`); `importar.ps1`/`exportar.ps1` foram corrigidos em 11/09 para isso.
- `.superpowers/` e `resultados_alvo/fase3_piloto/` estão no `.gitignore`.

## 5. O que o Eric pediu para as próximas fases (e o que ainda não decidiu)

- Continuar tudo **nesta máquina**.
- **Fase 4 (pedido do Eric na sessão do Ryzen; nome fixado na decisão 29, plano da Fase 3):** interceptador em Playwright Python (Chromium do Playwright, headless) que dispara em erro HTTP ≥ 400, JSON que não parseia, divergência de contrato (diff em código), exceção de página ou falha de localizador; coleta o "cenário"; **poda sobre a árvore de acessibilidade** (não sobre o DOM); orçamento de tokens por inferência; cura de seletor com validação na página viva (aceita só candidato que resolve para exatamente 1 elemento); gestão da biblioteca pelo modelo **atrás de validação por código** (achado 4.24); baseline não-neural de seletor (10 níveis; os 82,4% estão **[conferir]**, ver Memorial §6.1) como piso obrigatório.
- **Fase 5:** MTTR = tempo entre detecção e restauração verificada; Task Success = fluxo restaurado e roteiro verde; ~10 cenários × 5 repetições; banco reaplicado do zero entre runs; `FAULT_MODE`/`FAULT_TARGET_FIELD` no `.env` para runs determinísticos.
- **Decisões pendentes dele:** modelo padrão de produção (3B/A2 × 7B/A2 × Granite/A2 — passou a ser o resultado da Fase 3, decisão 36); k da recuperação; versionar o log; quando a máquina pode ficar ocupada pelas ~60 h da bateria da Fase 3. Os fixtures 4.20 já foram corrigidos (decisão 34).
- Restrição acadêmica dura, sempre: diagnóstico só a partir da **fronteira** (árvore de acessibilidade + tráfego HTTP), sem acoplar à lógica interna do servidor; a biblioteca é conhecimento prévio curado, não sonda no servidor.

## 6. Jeito de trabalhar que funcionou

- Planejar em modo de plano e submeter; ele aprova rápido quando o plano tem números e alternativas.
- Antes de rodar bateria longa, **perguntar** (ele decide quando a máquina fica ocupada); depois, orquestrar em segundo plano e avisar ao terminar.
- Pesquisa bibliográfica: fontes de 2024+, com número medido e condição, tudo para o Memorial (`memorial/2-pesquisa-e-literatura/`) e referências completas em `referencias.md`.
- Corrigir a si mesmo por escrito quando um número estava errado (aconteceu com "linear vence estágios" e com o veredito do cache) — ele prefere a correção explícita.
- Ao final de cada bloco de trabalho: o que foi feito, o que foi verificado, o que ficou de fora e por quê, e o `git status` para ele commitar.
