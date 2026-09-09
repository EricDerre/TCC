<!-- ! Alteração de IA - Revisar: documento de passagem de bastão da sessão de trabalho no
     Ryzen (31/08 a 09/09/2026) para o Claude Code que vai continuar o projeto na máquina-alvo.
     ! Motivo: uma sessão do Claude não viaja entre máquinas; o que viaja é a memória (pasta
     memory/), as regras (CLAUDE.md) e o repositório. Este arquivo cobre o que fica de fora
     disso: como o harness está montado, o que cada script faz, o estado de cada fase, as
     armadilhas já pagas e o jeito de trabalhar que o Eric espera. É para ser lido UMA vez,
     no início da primeira sessão na máquina-alvo, e depois consultado por tópico. -->
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
| Fase 3 — interceptador Playwright, poda da árvore de acessibilidade, cura de seletor, gestão da biblioteca pelo modelo | **não começou** | plano aprovado em `plano-aprovado-fase-2b.md` (seções Fase 3 e 4) |
| Fase 5 — MTTR / Task Success com injeção de falhas | não começou | plano, seção Fase 5 |

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
  resultados/               Ryzen (2-A + 48 casos parciais de Q8)      resultados_alvo/   i5 (2-B completa, maquina.json)
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
- **Fixtures que contradizem o código** (achado 4.20: "R$ NaN", cartões duplicados) — corrigir antes de nova bateria.
- Gráficos: até 3 matizes por figura, rótulo em cada barra, `ylim` com folga acima de 100% (rótulo colidia com o subtítulo), variantes de quantização fora das figuras de condição.

## 5. O que o Eric pediu para as próximas fases (e o que ainda não decidiu)

- Continuar tudo **nesta máquina**.
- **Fase 3 (plano aprovado):** interceptador em Playwright Python (Chromium do Playwright, headless) que dispara em erro HTTP ≥ 400, JSON que não parseia, divergência de contrato (diff em código), exceção de página ou falha de localizador; coleta o "cenário"; **poda sobre a árvore de acessibilidade** (não sobre o DOM); orçamento de tokens por inferência; cura de seletor com validação na página viva (aceita só candidato que resolve para exatamente 1 elemento); gestão da biblioteca pelo modelo **atrás de validação por código** (achado 4.24); baseline não-neural de seletor (10 níveis, 82,4%) como piso obrigatório.
- **Fase 5:** MTTR = tempo entre detecção e restauração verificada; Task Success = fluxo restaurado e roteiro verde; ~10 cenários × 5 repetições; banco reaplicado do zero entre runs; `FAULT_MODE`/`FAULT_TARGET_FIELD` no `.env` para runs determinísticos.
- **Decisões pendentes dele:** modelo padrão de produção (3B/A2 × 7B/A2 × Granite/A2); k da recuperação; se corrige agora os fixtures 4.20; versionar o log.
- Restrição acadêmica dura, sempre: diagnóstico só a partir da **fronteira** (árvore de acessibilidade + tráfego HTTP), sem acoplar à lógica interna do servidor; a biblioteca é conhecimento prévio curado, não sonda no servidor.

## 6. Jeito de trabalhar que funcionou

- Planejar em modo de plano e submeter; ele aprova rápido quando o plano tem números e alternativas.
- Antes de rodar bateria longa, **perguntar** (ele decide quando a máquina fica ocupada); depois, orquestrar em segundo plano e avisar ao terminar.
- Pesquisa bibliográfica: fontes de 2024+, com número medido e condição, tudo para o Memorial (`memorial/2-pesquisa-e-literatura/`) e referências completas em `referencias.md`.
- Corrigir a si mesmo por escrito quando um número estava errado (aconteceu com "linear vence estágios" e com o veredito do cache) — ele prefere a correção explícita.
- Ao final de cada bloco de trabalho: o que foi feito, o que foi verificado, o que ficou de fora e por quê, e o `git status` para ele commitar.
