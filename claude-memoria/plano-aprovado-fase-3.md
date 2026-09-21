<!-- ! Alteração de IA - Revisar: arquivo novo com a cópia integral do plano da Fase 3 aprovado
     pelo Eric em modo de planejamento do Claude Code (fonte:
     `%USERPROFILE%\.claude\plans\delegated-hopping-steele.md`), com este cabeçalho
     acrescentado por cima; o conteúdo do plano em si não foi reescrito.
     ! Motivo: o plano aprovado fica na pasta de planos do Claude Code, fora do repositório, e
     essa pasta não viaja entre máquinas pelo git — mesmo problema já registrado para a
     memória do Claude em `claude-memoria/README.md`. Sem esta cópia versionada, a
     máquina-alvo perderia o registro do que foi decidido e aprovado antes de a Fase 3 começar
     a ser implementada. -->
<!-- ! Alteração de IA - Revisar: em 12/09/2026 a nota de estado passou para 12/09 (implementação
     concluída e revisada; piloto executado; bateria aguardando o Eric) e foi acrescentado, ao
     final do arquivo, o anexo "Desvios do plano registrados no livro-razão". O texto do plano
     em si continua sem reescrita.
     ! Motivo: a nota dizia "implementação em andamento", e o que falta agora é a bateria, não
     código; e o plano diverge do que foi implementado em pontos que quem compara os dois
     precisa achar num lugar só (26 códigos × 30; `tipo_invalido` que não existe; diffs fora de
     `epoca-<n>/`; 172 verificações × 166; parser tolerante a FIM ausente; Ollama 0.34.0). Os
     rulings ficam no livro-razão em `.superpowers/`, fora do git; o anexo é a cópia versionada. -->

**Aprovado pelo Eric em 11/09/2026.**

> <!-- ! Alteração de IA - Revisar: linha de estado de 21/09/2026 acrescentada acima da de 13/09. ! Motivo: a bateria rodou (13–15/09, 58h59, 0 falhas) e o texto abaixo ainda dizia "aguardando decisão do Eric"; o fechamento (relatórios, pesquisa, Fase 3-B) segue o plano complementar de 21/09/2026. -->
> **Estado em 21/09/2026: bateria completa executada em 13–15/09/2026 (`FIM … 58h59`, 0 falhas, Ollama 0.34.0; resultados no commit b9f9ad9); o que resta (relatórios, rodada 2 da pesquisa, revisão humana, Fase 3-B) está no plano complementar de 21/09/2026.**
>
> Estado em 13/09/2026: implementação concluída, revisada e corrigida na onda final (revisão da T12 + duas lentes por onda; 60 testes em `testar_fase3.py`); piloto de 10 casos executado duas vezes (`rodar_fase3.ps1 -Piloto`: v1 em 12/09, 00h13, 0 de 6 propostas aceitas antes da decisão 41; v2 em 13/09, 00h15, 2 de 6 aceitas — §9 do relatório da Fase 3); bateria completa aguardando decisão do Eric (~60 h no plano; 67,18 h na projeção do executor). Ver `README.md` (seção "AgenteCore — experimentos com os modelos locais") para os scripts e o **anexo ao final deste arquivo** para os desvios do plano.

---

# Plano — Fase 3 de testes: biblioteca gerida pelo próprio modelo, por modelo e por época

Data: 11/09/2026 · Máquina: i5-1235U (TARGET_TSP030) · Repositório: `c:\Users\Eric.Derre\Documents\TCC`

> **Aviso de custo (mudou desde a pergunta ao Eric):** a estimativa recalculada com os ms/token medidos na 2-B é **~55–60 h de máquina** para 4 modelos × 3 épocas (Granite ≈ 23 h), não ~42 h. O piloto (§10) mede o valor real antes de comprometer a máquina; as alavancas para cortar ~30% estão em §4.3.

## 1. Contexto

A Fase 2-B mostrou que a biblioteca **recuperada** (top-3) sobe o acerto em todos os modelos (Granite 66,7 → 76,7%; `qwen2.5-coder:3b` 23,3 → 63,3%), que o teto é o recuperador (com o verbete certo o Granite acerta 100%) e que **documentação errada é seguida em 93–96% dos casos**. A decisão 13/13' do Memorial adiou para a Fase 3 a pergunta seguinte: **o próprio modelo consegue melhorar a documentação que consulta, sem estragá-la?** A resposta decide o modelo final do TCC.

O que existe: harness em `Programacao/AgenteCore/experimentos/` (Python padrão + matplotlib, sem dependência nova), 36 verbetes em `base_conhecimento/`, validador em código (`biblioteca.validar()`), recuperador BM25 + sinais em código, executor resumível por JSONL, avaliação com Wilson/McNemar, gráficos 01–11, relatório HTML, orquestrador `.ps1`. O que **não** existe: função de escrita de verbete, noção de época, isolamento de biblioteca por modelo.

Pesquisa feita hoje (workflow com 8 tópicos, 172 verificações adversariais de citação, fontes 2024+; resultado bruto em `…\5c1c8fa0-…\subagents\workflows\wf_add7e8f0-e81\journal.jsonl`, rodada complementar em andamento): sustenta o desenho e impõe três travas, todas já previstas pelo Eric — escrita **aditiva e incremental** (uma reescrita monolítica derrubou 18.282 tokens/66,7% para 122 tokens/57,1% na literatura), **validação em código antes de aceitar** (portão determinístico rejeitou 63,1% dos candidatos e subiu o F1; 4 de 5 sinais custam < 65 ms), e **medição época a época** (curvas de automelhoria sobem e caem, ~17 pp entre pico e fim). O gargalo medido é o **escritor**, não o leitor: modelos pequenos como curadores tiveram ganho atenuado ou negativo. O livro orientador (Faceli, Lorena, Gama, Almeida e Carvalho) está na **3ª edição, 2025** (LTC/GEN, ISBN 9788521639206, 376 p., 19 capítulos; Cap. 10 = avaliação de modelos preditivos); o documento ABNT cita a 2ª (2021) e precisa ser corrigido.

## 2. Decisões já tomadas pelo Eric (11/09/2026)

| Decisão | Escolha |
|---|---|
| Sinal de aprendizado | **Com gabarito, em partição**: 54 casos de aprendizado (3 por célula classe×nível) e 36 de avaliação (2 por célula). Só nos 54 o modelo vê a causa correta e propõe edições. Os 36 nunca recebem feedback. |
| Escala | **4 modelos × 3 épocas**: `granite4.2:8b`, `qwen2.5:7b`, `qwen2.5-coder:7b`, `qwen2.5-coder:3b`. `phi4-mini` e `1.5b` ficam de fora. |
| Fixtures do achado 4.20 | **Corrigir antes** (`sin-1`, `sin-2`, `semt-13`, `efe-13`). |
| "Criadas → criadas" | **Diffs entre snapshots + hit@k do recuperador por biblioteca** (sem troca cruzada entre modelos). |

Regras duras: a original fica intocada; o modelo **nunca apaga, esvazia, remove ou substitui** texto; corrigir = **acrescentar** texto retificando; toda edição carrega **o quê + motivo**; toda edição passa por **validação em código** antes de entrar.

## 3. Nomenclatura (decisão nº 29 a registrar)

| Nome oficial | O que é | Estado |
|---|---|---|
| Fase 2-A | 6 modelos × 90 casos × 3 estratégias, sem biblioteca (Ryzen) — "teste 1" | concluída |
| Fase 2-B | biblioteca compartilhada, só leitura, A0–A5 (i5) — "teste 2" | concluída |
| **Fase 3** | **biblioteca por modelo, editada pelo modelo em épocas, atrás de validação em código (i5) — "teste 3"** | este plano |
| Fase 4 | interceptador Playwright + poda da árvore de acessibilidade + cura de seletor | depois |
| Fase 5 | MTTR / Task Success com injeção de falhas | depois |

Corrigir o ponteiro errado do handoff (`claude-memoria/contexto/2026-09-09-…md` diz que as seções Fase 3/4 estão em `plano-aprovado-fase-2b.md`; não estão).

## 4. Desenho experimental

### 4.1 Partição determinística (54/36) — por hash, não por posição

Em cada uma das 18 células `(classe, nivel)` (5 casos cada), ordenar os ids por `sha256("fase3:" + id)`; os **3 primeiros → aprendizado**, os **2 últimos → avaliação**. Por hash e não por posição no arquivo: os 30 casos de `banco_casos.py` e os 60 de `banco_casos_extra.py` não se distribuem igual por célula, e "os 3 primeiros" enviesaria o aprendizado para os casos-base. Já calculado: **os 4 fixtures corrigidos caem em aprendizado**, logo **os 36 de avaliação são byte a byte os mesmos da 2-B** (Fase 3 L0 × 2-B A2 pareável sem ressalva nesses 36 — registrar no Memorial). Gravado em `fase3/particao.json` (`regra`, `semente`, `casos: {id: {particao, classe, nivel, hash}}`), regravado idêntico a cada execução e conferido (divergência aborta).

### 4.2 Protocolo de época (por modelo)

Notação: **L0** = cópia intocada da original; **L(n)** = biblioteca do modelo após n rodadas de edição. Condição sempre **A2** (k = 3), prompt de diagnóstico **byte a byte igual ao da 2-B** (`linear_com_biblioteca`), `max_tokens = 600`.

Para cada modelo, do mais rápido ao mais lento (`3b`, `qwen2.5:7b`, `coder:7b`, `granite`):

1. **Época 0 (sem inferência)**: `fase3/bibliotecas/<slug>/epoca-0/` ← `base_conhecimento/` (`copytree` sem `INDICE.md`), índice regerado, `fechamento.json` com o hash (igual entre os 4 modelos: assert).
2. **Época n = 1..3**: leitura em `epoca-(n−1)/` (fechada); escrita em `epoca-n/` (aberta, criada como cópia da anterior). Para cada caso, na ordem dos 90:
   1. **Diagnóstico** com L(n−1) → `fase3/<slug>/diagnosticos__L<n−1>.jsonl`.
   2. **Se o caso é de aprendizado — Proposta**, logo em seguida, com o **prompt do diagnóstico + a resposta do modelo como prefixo literal** (§5), `max_tokens = 700` → parse → validação (§6) → aceitas **aplicadas na hora em `epoca-n/`** → linha completa em `propostas__E<n>.jsonl`. Como os diagnósticos leem `epoca-(n−1)/`, o efeito é o de "aplicar ao final da época".
   3. Casos de avaliação: nunca há proposta nem gabarito no prompt.
   
   **Fechamento**: `bib.validar(L(n), teto_global=None)` vazio + `conferir_somente_acrescimo(L(n−1), L(n))` vazio (falha = bug do harness → `SystemExit`, nada é descartado em silêncio) → `INDICE.md` → `diff__E<n>` (contra a anterior e contra a original) → `fechamento.json`.
3. **Passada final**: diagnóstico dos 90 com **L3** → `diagnosticos__L3.jsonl`. Sem propostas.
4. `oll.descarregar(modelo)`; `um_modelo_por_vez()`.

Total por modelo: **4 × 90 diagnósticos + 3 × 54 propostas = 522 inferências**. A passada com L0 **é** o baseline.

### 4.3 Custo estimado (calibrar no piloto)

Derivado dos ms/token e tok/s medidos na 2-B (Granite 61,8 ms/tok prefill e 3,9 tok/s; coder-7b 44 ms e 4,2; qwen-7b 43,8 ms e 4,1; 3b 20 ms e 6,3), prompt de diagnóstico ~1.350 tokens (cresce com as notas), proposta com prefill só do sufixo (~1.600 tokens, graças ao prefixo compartilhado) e ~350 tokens gerados:

| Modelo | 360 diagnósticos | 162 propostas | Total |
|---|---|---|---|
| `granite4.2:8b` | ~13,8 h | ~8,8 h | ~22,6 h |
| `qwen2.5-coder:7b` | ~8,0 h | ~6,9 h | ~14,9 h |
| `qwen2.5:7b` | ~7,5 h | ~7,0 h | ~14,5 h |
| `qwen2.5-coder:3b` | ~3,6 h | ~4,0 h | ~7,6 h |
| **Total** | ~33 h | ~27 h | **~60 h** (sem o cache de prefixo na proposta: ~75 h) |

O executor imprime a projeção por modelo antes de começar. Alavancas (decisão do Eric): `MAX_PROPOSTAS_POR_CASO = 1` e `--max-tokens-proposta 500` (≈ −30% nas propostas); ou 3 modelos.

### 4.4 Hipóteses pré-registradas (entram no Memorial antes de rodar)

- **H1** — Nos 36 de avaliação, acerto com L3 > L0 nos modelos de 7–8B (McNemar exato, α = 0,05).
- **H2** — O ganho concentra-se nas classes em que a recuperação é fraca (tradução: hit@3 = 46,7%), via aumento do hit@3 da biblioteca do modelo.
- **H3** — Nos 54 de aprendizado o ganho é maior que nos 36; a diferença quantifica a memorização.
- **H4** — A taxa de aceitação das propostas cresce com o porte; o 3B tem mais rejeições por formato.
- **H5** — Autoenvenenamento (casos certos em L(n) que viram errados em L(n+1), nos 36) fica abaixo de 10%; se superar o ganho, o modelo é vetado.
- **H6** — A curva não é monótona: reportar o melhor L e o L3, nunca só o último.

## 5. Prompt de proposta (`estrategias.py`)

`proposta_de_edicao(prompt_diagnostico, resposta_diagnostico, caso, acertou, causa_respondida, verbete_ouro_renderizado, ids_visiveis) -> str`. Começa **exatamente** com `prompt_diagnostico + "\n\n" + resposta_diagnostico` (condição do cache de prefixo; testada), depois:

```
=====

CORREÇÃO DESTE CASO
CAUSA_RAIZ CORRETA: {causa_correta}
CAMPO AFETADO: {campo_afetado ou "nenhum"}
SEU DIAGNÓSTICO: {causa_respondida ou "(sem CAUSA_RAIZ)"} — {correto | incorreto}

VERBETE DEDICADO A ESSA CAUSA (pode não ter aparecido antes):
{verbete_ouro_renderizado}

Agora você pode melhorar a documentação para que um PRÓXIMO caso parecido — não este — seja diagnosticado certo. Regras:
- A documentação nunca é apagada nem reescrita: você só ACRESCENTA. "nota" acrescenta uma observação a um verbete; "retificacao" acrescenta uma correção apontando o trecho errado; "novo_verbete" cria um verbete novo.
- Escreva sobre o sistema e o tipo de falha, em termos gerais. Não copie o sintoma, a observação nem o corpo deste caso; não cite o identificador do caso.
- No MOTIVO, diga com suas palavras qual evidência do caso mostrou a lacuna.
- Só cite arquivos, endpoints e tabelas que apareçam na documentação acima.
- Só use como VERBETE os identificadores que apareceram acima entre colchetes: {ids_visiveis}.
- TEXTO com 60 a 280 caracteres, uma ou duas frases, sem lista. MOTIVO com 20 a 240 caracteres.
- No máximo 2 propostas. Se a documentação já bastava, responda só a palavra: NENHUMA

Formato, exatamente assim, um bloco por proposta:

PROPOSTA 1
OPERACAO: nota | retificacao | novo_verbete
VERBETE: <id entre colchetes; em novo_verbete, um id novo em minusculas-com-hifens>
TRECHO: <so em retificacao: trecho curto do verbete que esta errado, copiado igual>
TITULO: <so em novo_verbete>
SISTEMA: <so em novo_verbete: CobaiaFront | CobaiaAPI | Infraestrutura | Ambos>
ENTIDADE: <so em novo_verbete: Produto | Tipo | Usuario | Pedido | Interface | Infraestrutura>
CAUSAS: <so em novo_verbete: 1 a 3 valores de CAUSA_RAIZ separados por virgula>
ARQUIVOS: <opcional: caminhos citados na documentacao acima, ou "nenhum">
PALAVRAS_CHAVE: <ate 5 termos novos separados por virgula, ou "nenhuma">
SINTOMAS: <ate 3 sintomas novos separados por virgula, ou "nenhum">
TEXTO: <o que acrescentar>
MOTIVO: <por que isso faria o proximo diagnostico acertar, e qual evidencia deste caso mostrou a lacuna>
FIM

Valores permitidos para CAUSAS:
{_LISTA_CAUSAS}
```

Texto, não JSON (coerente com "reason free, constrain late" da 2-A e com `avaliar.extrair`). O verbete dedicado é sempre mostrado: nos 21% de casos em que a recuperação falhou, a edição útil é dar palavras-chave ao verbete certo. Saída estruturada por `format`/GBNF fica como ablação futura (mudaria o regime de prompt).

## 6. Parser, validação e aplicação — módulo novo `evolucao_biblioteca.py`

### 6.1 Constantes

| Constante | Valor | Por quê |
|---|---|---|
| `MAX_PROPOSTAS_POR_CASO` | 2 | custo de geração; obriga a escolher a edição que importa |
| `TEXTO_MIN / TEXTO_MAX` | 60 / 280 chars | < 60 não é conhecimento; 280 ≈ 108 tokens cabe 2–3× num verbete |
| `MOTIVO_MIN / MOTIVO_MAX` | 20 / 240 | motivo vazio inutiliza a revisão; longo é raciocínio |
| `MAX_PALAVRAS_CHAVE_NOVAS / MAX_SINTOMAS_NOVOS` | 5 / 3 por proposta | entram no BM25: excesso vira "decorar" por outro caminho |
| item de lista | ≤ 40 chars, `^[a-z0-9 _\-\.\$]+$` após `normalizar` | o frontmatter plano quebra com vírgula/colchete |
| `bib.TETO_CHARS_VERBETE` | 550 (mantido, só para `render_base`) | as 4 seções originais nunca crescem |
| `bib.TETO_CHARS_NOTAS_VERBETE` | 800 chars renderizados | ≈ 308 tokens; 3 verbetes ficam ≤ ~1.700 tokens |
| `bib.TETO_NOTAS_POR_VERBETE` | 6 | além disso vira lista de exceções; força retificação/verbete novo |
| `TETO_VERBETES_NOVOS_POR_EPOCA` | 6 por modelo | cada verbete novo compete com o dedicado no BM25 (medido) e a revisão precisa caber |
| `TETO_TOKENS_CONTEXTO` | 1.800 tokens estimados | abaixo dos ~2.500 em que a literatura mede degradação |
| `ORCAMENTO_PROMPT_DIAG / _PROP` | `NUM_CTX − 600 − 64` / `NUM_CTX − 700 − 64` | guarda dura contra truncamento silencioso do prefixo |
| `LIMIAR_COPIA_PROPOSTA` | 0,30 dos 5-gramas **da proposta** | normalizado pela proposta (curta): copiar 12 palavras seguidas do caso é rejeitado |

Conta: por verbete ≤ 60 (título) + 550 + 800 = 1.410 chars ≈ 543 tokens; 3 verbetes + cabeçalho ≈ 1.675 ≤ 1.800; prompt de diagnóstico ≤ ~2.500 + 600 de resposta; prompt de proposta ≤ ~4.600 + 700 ≪ 8.192.

### 6.2 Parser — `parsear_propostas(resposta) -> {"nenhuma", "blocos": [{numero, campos, malformado}], "truncada"}`
Remove `*` e crases; `NENHUMA` isolada e sem bloco válido → `nenhuma=True`; bloco = `^PROPOSTA\s+(\d+)` até `^FIM`; linhas `CAMPO:` abrem campo, linhas soltas anexam ao campo aberto; `VERBETE` aceita `[id]` ou `id`; sem `FIM` → `malformado="sem FIM"`; sem OPERACAO/VERBETE/TEXTO/MOTIVO → `"falta <CAMPO>"`; `truncada` se não termina em FIM/NENHUMA e `tokens_saida >= max_tokens`.

### 6.3 Códigos de rejeição (estáveis; viram histograma) — `validar_proposta(bloco, ctx) -> {"aceita", "motivo", "detalhe", "edicao"}`

Ordem de checagem (a primeira que falha decide): 1 `sem_bloco` · 2 `bloco_malformado` · 3 `excesso_de_propostas` · 4 `operacao_invalida` · 5 `alvo_inexistente` · 6 `alvo_nao_visto` (id existe mas ∉ 3 recuperados ∪ ouro: não anota o que não leu) · 7 `id_invalido` (`^[a-z0-9]+(-[a-z0-9]+)*$`, ≤ 40) · 8 `id_repetido` (inclui os 23 nomes de causa) · 9 `teto_verbetes_novos` · 10 `tipo_invalido`/`pasta_invalida` (defensivos) · 11 `vocabulario` (SISTEMA/ENTIDADE presentes mas fora dos conjuntos; **ausentes → padrão `Ambos` e entidade inferida de `rec.sinais_do_caso`**, para não punir o 3B por campo esquecido) · 12 `causa_fora_do_conjunto` (vazio, > 3 ou fora das 23) · 13 `arquivo_inexistente` · 14 `endpoint_inexistente`/`tabela_inexistente` (regex `\b(GET|POST) /api/[\w/{}]+` e `\b(tb|vw_)\w+` no TEXTO) · 15 `texto_curto`/`texto_longo` · 16 `motivo_ausente`/`motivo_curto`/`motivo_longo` · 17 `retificacao_sem_trecho` · 18 `trecho_nao_encontrado` (normalizado, substring de `render_base(alvo)`) · 19 `palavra_chave_invalida` (rejeita a proposta inteira, nunca poda em silêncio) · 20 `duplicada` · 21 `copia_do_caso` (5-gramas da proposta vs cada um dos 90 casos; também qualquer `\b(lex|sin|semt|tra|run|efe)-\d+\b` no texto) · 22 `teto_notas_verbete` (> 800 chars ou > 6 notas após aplicar) · 23 `teto_verbete_novo` (> 550) · 24 `teto_prompt` (aplica em memória, reindexa, e para algum dos 90 casos o contexto > 1.800 tokens ou o prompt + 600 > NUM_CTX − 64) · 25 `copia_do_caso_acumulada` (`bib.validar` acusa ≥ 30% normalizado pelo caso: a soma de notas não pode reconstruir um caso) · 26 `biblioteca_invalida` (qualquer outro problema de `bib.validar`).

### 6.4 Invariante somente-acréscimo — `conferir_somente_acrescimo(raiz_antiga, raiz_nova) -> list[str]`
Todo `.md` antigo existe no novo; frontmatter novo contém todas as chaves antigas com o mesmo valor escalar, ou com a lista antiga como **prefixo** da nova; corpo antigo é **prefixo** do corpo novo; `id`, `tipo`, `causa_raiz` idênticos; arquivos novos só em `aprendidos/`. Conferido no fechamento e nos testes; violação = bug → `SystemExit`.

### 6.5 Aplicação — `aplicar_edicao(raiz, edicao) -> Path` (edição textual, preserva os comentários `# ! Alteração de IA` originais)
- Listas: `palavras_chave: [...]` recebe `, item1, item2]` (deduplicado); `sintomas` criada antes do `---` se não existir.
- Corpo: cria `## Notas do modelo` se não houver; anexa `- [E<n> · <caso> · nota] <TEXTO> — Motivo: <MOTIVO>` ou `- [E<n> · <caso> · retificação de "<TRECHO>"] <TEXTO> — Motivo: <MOTIVO>`.
- Frontmatter: linha `# ! Alteração por modelo <tag> (E<n>, caso <id>) - Revisar: nota acrescentada.` (o parser ignora `#`).
- Novo verbete: `aprendidos/<id>.md`, frontmatter gerado (`# ! Alteração de IA - Revisar: verbete criado pelo modelo … (Fase 3).` / `# ! Motivo: <MOTIVO>` / `id, titulo, sistema, entidade_principal, tipo: aprendido, status: ativo, arquivos, sintomas, palavras_chave, causas_relacionadas`), corpo `## Resumo` = TEXTO (+ `## Sinais` se houver sintomas).

### 6.6 Como a edição chega ao prompt e ao índice (`biblioteca.py`, `recuperacao.py`)
- `SECOES += ("Notas do modelo",)`; `TIPOS |= {"aprendido"}`; `_ORDEM_PASTAS += ("aprendidos",)`; `NOTA_RE` + `notas(v) -> list[dict]` (linha que não casa → `validar` acusa "nota malformada").
- `render_base(v)` = o `render` atual, byte a byte; `render_notas(v)` = `" Notas: " + textos` e `'Retificação: onde diz "trecho", leia: texto.'`; `render = render_base + render_notas`. Para a original, `render == render_base` (teste). Época, caso e **motivo ficam fora do prompt** (tokens) e fora do BM25.
- `validar(verbetes, casos, limiar_sobreposicao=0.3, teto_global: int | None = TETO_TOKENS_BIBLIOTECA)`: teto por verbete em duas partes (base ≤ 550; notas ≤ 800 e ≤ 6); `tipo: aprendido` exige pasta `aprendidos/` e `causas_relacionadas`; a Fase 3 passa `teto_global=None` (A1 não roda; o orçamento que importa é o do prompt, checagem 24); a 2-B não muda.
- `por_causa` continua só `tipo: erro` → **o verbete de ouro nunca muda** (hit@k comparável entre L0..L3). `verbete_ouro` troca o `KeyError` por `LookupError` com mensagem clara.
- `recuperacao._texto_indexavel`: 4 seções base + textos das notas (sem motivo) + listas. Para verbete sem notas, idêntico ao de hoje (teste).
- `validar_banco.escrever_indice(verbetes, raiz=bib.BASE)` e `--raiz PASTA` para validar/medir uma cópia.

### 6.7 Snapshot, hash, diff, histórico
`hash_biblioteca(raiz)` = sha256 de (caminho relativo posix, bytes) ordenados, `.md` sem `INDICE.md`, 12 hex = `biblioteca_versao` de todo registro · `fechamento.json` (`modelo, epoca, hash, n_verbetes, n_verbetes_novos, n_notas, n_retificacoes, chars, tokens_estimados, aceitas_na_epoca, fechado_em`) · `diff_bibliotecas(a, b)` (`arquivos_novos, arquivos_tocados, linhas/chars/tokens acrescentados, por_verbete, unificado` via `difflib`) gravado em `diff__E<n>.json/.md` e `diff__E<n>__vs_original` · `historico.jsonl` por modelo (uma linha por edição aceita + `ordem, acertou_diagnostico, hash_apos`).

## 7. Estrutura de diretórios e arquivos a criar/alterar

```
resultados_alvo\fase3\
  maquina.json  particao.json  fase3.log
  bibliotecas\<slug>\historico.jsonl ; epoca-0..3\ (snapshot completo + INDICE.md + fechamento.json + diff__E<n>*)
  <slug>\diagnosticos__L0..L3.jsonl ; propostas__E1..E3.jsonl
  avaliacao_fase3.json  resumo_fase3.json  comparacao_fases.json/.md  revisao_edicoes__<slug>.md  relatorio_fase3.html
resultados_alvo\graficos\12-…17-…   (sequência única de figuras)
resultados_alvo\fase3_piloto\        (descartável; entra no .gitignore)
```
`slug = modelo.replace(":", "_")`. Tudo em `fase3\` para `avaliar.carregar()` e `gerar_relatorio.py` (não recursivos) continuarem ignorando a Fase 3. Versionável (~1 MB de snapshots + ~2 MB de propostas por modelo).

| Arquivo | Mudança (tag `! Alteração de IA - Revisar` + `! Motivo:` em tudo) |
|---|---|
| `caminhos.py` | `fase3(nome="fase3") -> dict` com `raiz, bibliotecas, particao, maquina, log, avaliacao, resumo, comparacao, comparacao_md, relatorio, graficos` (gráficos na pasta comum, salvo piloto). Todo script da Fase 3 aceita `--saida`. |
| `biblioteca.py` | §6.6. `BASE` continua a original; nunca é escrita pela Fase 3. |
| `recuperacao.py` | `_texto_indexavel` com notas (sem motivo); `verbete_ouro` com `LookupError` claro. |
| `validar_banco.py` | `escrever_indice(verbetes, raiz)`; `--raiz`. |
| `executar_bateria.py` | refatoração mínima sem mudar saída: `ler_jsonl`, `guarda_estimativa`, `guarda_tokens_reais`, `ambiente_residente`, `inferir_seguro` viram funções de módulo usadas pelos dois executores; verificar com 1 caso A2 em `RESULTADOS_DIR=tmp_check` que as chaves do registro são as mesmas de `resultados_alvo\qwen2.5-coder_3b__A2.jsonl`. |
| `evolucao_biblioteca.py` (**novo**) | `particionar`, `parsear_propostas`, `validar_proposta`, `aplicar_edicao`, `conferir_somente_acrescimo`, `copiar_biblioteca`, `hash_biblioteca`, `fechar_snapshot`, `diff_bibliotecas`, `abrir_epoca` (reconstrói do JSONL). |
| `estrategias.py` | `+proposta_de_edicao` (§5). `linear_com_biblioteca` **inalterado**. |
| `executar_fase3.py` (**novo**) | CLI `--modelos`, `--epocas 3`, `--casos 0`, `--k 3`, `--max-tokens-diagnostico 600`, `--max-tokens-proposta 700`, `--saida fase3`, `--original`; laço §4.2; retomada por `(modelo, epoca, caso, tipo)`: época com `fechamento.json` é pulada; época aberta é reconstruída de `propostas__E<n>.jsonl` (re-valida e confere que a decisão bate); proposta órfã refeita lendo a resposta do diagnóstico no JSONL; guarda estimada por época e guarda real em **toda** inferência (registro `contexto_estourou`, época aborta); projeção de tempo impressa antes de começar; `maquina.json`. |
| `avaliar_fase3.py` (**novo**) | §8. |
| `comparar_fases.py` (**novo**) | §9. |
| `gerar_graficos_fase3.py` (**novo**) | figuras 12–17 (§8.4), importando `_base, _titular, _salvar, _rotular, _curto, SERIES, RAMPA, …` de `gerar_graficos.py`. |
| `gerar_relatorio_fase3.py` (**novo**) | HTML único com dados embutidos: resumo modelo × L × partição; documentação por época; pareados e Cochran; propostas caso a caso (prompt, resposta crua, decisões, filtros); diagnósticos por L e partição; diffs por época. Junção com eixo de época. |
| `rodar_fase3.ps1` (**novo**, UTF-8 com BOM, sem travessão) | `param(-Resultados "resultados_alvo", -Modelos @(4), -Epocas 3, -Piloto, -SemAvaliacao)`; copia literal de `Marco, Falha, Rodar, RamLivreGB, Residentes, EsperarRam` e das checagens da 2-B; `validar_banco.py --indice` → `testar_fase3.py` → laço de modelos (`executar_fase3.py --modelos m --epocas N --saida S`) → `avaliar_fase3.py --gerar-revisao` → `comparar_fases.py` → `gerar_graficos_fase3.py` (venv) → `gerar_relatorio_fase3.py`; log `fase3.log`. `-Piloto` = `qwen2.5-coder:3b`, `--casos 10`, `--epocas 1`, pasta `fase3_piloto`. |
| `testar_fase3.py` (**novo**) | §10.1. |
| `banco_casos.py`, `banco_casos_extra.py` | §7.1. |
| `.gitignore` | `Programacao/AgenteCore/experimentos/resultados_alvo/fase3_piloto/`. |

### 7.1 Correção dos 4 fixtures (conferido em `Programacao/CobaiaFront/produtos_api.php:64-67,104`)

`formatarPreco(preco)` faz `Number(preco)`; se NaN, devolve `String(preco)` (sem "R$"); o grid é substituído por `grid.innerHTML = …` a cada resposta. Só `sintoma`/`observacao`/`corpo`/`requisicao`/termos mudam; `id`, `classe`, `nivel`, `causa`, `campo` ficam. Comentário com tag + motivo acima de cada `_c(...)`.

| Caso | Mudança |
|---|---|
| `sin-1` (`banco_casos.py:86-91`) | sintoma: `"O botao de preco de cada cartao mostra a palavra 'undefined', sem 'R$'."`; termos mantidos |
| `sin-2` (`:92-97`) | sintoma: `"O botao de preco de cada cartao mostra a palavra 'undefined', sem 'R$'; o restante do cartao esta correto."` (igual ao de sin-1 de propósito: a distinção está no corpo); termos mantidos |
| `semt-13` (`banco_casos_extra.py:150-155`) | sintoma: `"O botao de preco mostra '89,90' cru, sem 'R$' e sem formatacao."`; observacao: `"O separador decimal veio como virgula, no formato brasileiro; precos com ponto decimal aparecem formatados como 'R$ 89,90'."`; corpo e termos mantidos |
| `efe-13` (`:316-320`) | requisicao: `"GET /api/produtos (chamado duas vezes em sequencia; a primeira resposta chegou depois da segunda)"`; corpo: `'(primeira resposta: 14 itens, produto 3 a 69.9; segunda resposta: 14 itens, produto 3 a 74.9, apos alteracao no cadastro)'`; sintoma: `"A tela mostra o preco antigo (R$ 69,90) do produto 3, embora a ultima resposta da API traga 74.9; nenhum erro no console."`; observacao: `"A pagina substitui o grid inteiro a cada resposta recebida; a resposta mais antiga chegou por ultimo e sobrescreveu a mais nova."`; esperados `["tela", "sobrescr", "antig"]`; proibidos `["500", "cache", "duplicad"]` |

Verificação: `python validar_banco.py --indice` sem problema; posições do verbete-ouro dos 4 casos antes/depois (hoje: sin-1 4, sin-2 3, semt-13 2, efe-13 24) e hit@k global recalculado registrados no Memorial (era 37,8 / 78,9 / 90,0 / MRR 0,584); nota no comentário de `banco_casos.py:5-7` e no achado 4.20.

## 8. Avaliação (`avaliar_fase3.py`; importa `avaliar_registro, wilson, mcnemar_exato, agregar, _normalizar` de `avaliar.py`)

### 8.1 Por modelo × versão da biblioteca (L0..L3) × partição (54 / 36 / 90), e por classe/nível
Acerto (+ IC Wilson), **acurácia balanceada** (macro-recall por causa; métrica primária da escolha, penaliza o colapso num rótulo), campo, formato, fora do conjunto, formato-ok-conteúdo-errado, **distribuição dos rótulos preditos** (parcela do mais frequente; nº distintos), `citou_verbete`, `ouro_no_contexto`, `contexto_com_nota`, `citou_verbete_anotado`, `citou_verbete_novo`, tempos (mediana e p95; prefill e geração separados), tokens, `contexto_estourou`.

### 8.2 Pareado e omnibus
- `pareado_vs_L0`: por modelo × L ∈ {1,2,3} × partição: `n_pares, acerto_L0_pct, acerto_pct, delta_pp, b, c, p_mcnemar, p_holm` (Holm nas 3 comparações da mesma (modelo, partição)), **g de Cohen** (`b/(b+c) − 0,5`) e razão `b/c`.
- `cochran_q` por modelo × partição sobre L0..L3: `Q, gl=3, p` — `p` via `qui_quadrado_sf(x, gl)` só com `math` (gl par: soma finita de Poisson; gl ímpar: `erfc` + série finita); `holm(ps)`.
- **Flips** entre versões consecutivas: ✓→✗ (autoenvenenamento) e ✗→✓, por partição e classe.
- Efeito mínimo detectável com n = 36 e n = 90 (McNemar, α 0,05, poder 0,8), reportado.

### 8.3 Recuperação e documentação
- `recuperacao`: por modelo × L: `rec.avaliar_recuperacao` nos 90 e nos 36 (hit@1/3/5, MRR) + `ouro_deslocado_por_novo` (verbete de `aprendidos/` no top-3 e o ouro fora) + "edições que tornaram o ouro recuperável no top-3 para o caso de origem".
- `documentacao` por modelo × época: `n_nenhuma, n_respostas_truncadas, n_propostas, n_aceitas, aceitas_pct, por_operacao, motivos_rejeicao{}, tentativas_de_decorar, chars/tokens acrescentados, verbetes_tocados, verbetes_novos, quando_errou{}, quando_acertou{}, biblioteca{n_verbetes, n_notas, chars, tokens_estimados, hash}, segundos_mediana_proposta, tokens_saida_medio_proposta, prefill_ms_por_token_proposta vs diagnóstico` (prova se o cache de prefixo agiu).
- `reconstrucao_ok`: 10 diagnósticos por modelo com prompt reconstruído do snapshot e `contexto_sha256` conferido.
- **Revisão humana**: `--gerar-revisao` cria `revisao_edicoes__<slug>.md` (idempotente) com até 30 edições aceitas por modelo (10 por época, estratificadas por operação, amostra determinística por hash): `| # | Época | Caso | Verbete | Operação | Texto | Motivo | Avaliação | Comentário |`; o Eric escreve `Correta`/`Parcial`/`Errada`; `avaliar_fase3.py` lê e apura por modelo e operação (`sem_avaliacao` listado). Um revisor: proporções, sem kappa.

### 8.4 Figuras 12–17 (paleta e regras atuais; ≤ 3 matizes; rótulo em todo ponto; `ylim(0,112)`)
12 `fase3-acerto-por-epoca` (2×2 painéis por modelo; x = L0..L3; cheia = 36, tracejada = 54) · 13 `fase3-recuperacao-por-epoca` (hit@3 nos 36, barras L0..L3 em rampa) · 14 `fase3-propostas-por-motivo` (2×2; barras horizontais: aceitas vs cada código) · 15 `fase3-crescimento-da-biblioteca` (tokens × L, referência tracejada em 6.582) · 16 `comparacao-entre-fases` (barras por modelo: 2-A linear · 2-B A0 · 2-B A2 · F3 L0 · F3 L3; "sem dado") · 17 `custo-versus-acerto-tres-fases` (dispersão; 2-A com marcador vazado: máquina diferente).

## 9. Comparação entre fases (`comparar_fases.py`)

Entradas: `experimentos\avaliacao.json` (2-A; linear), `resultados_alvo\avaliacao.json` (2-B: A0, A2, A5), `fase3\avaliacao_fase3.json` + `resumo_fase3.json`. Só os 4 modelos da Fase 3 nas colunas completas.

`comparacao_fases.json`: por modelo, colunas `2A_linear_ryzen, 2B_A0, 2B_A2, F3_L0, F3_L3` × `{n, acerto_pct, ic95, acuracia_balanceada, segundos_mediana, tokens_saida_medio, fora_do_conjunto_pct, formato_ok_conteudo_errado_pct, hit3, maquina}` em `nos_90` e `nos_36_avaliacao`; `adesao_cega_2B_A5_pct` (Granite e 3b; demais `null`); `tentativas_de_decorar_F3`; `autoenvenenamento_F3`; `pareamentos`: (2A × 2B A0), (2B A0 × 2B A2), (**2B A2 × F3 L0 nos 86 casos não alterados e nos 36** — reprodutibilidade na mesma máquina, mesmo digest e prompt: vira achado), (F3 L0 × F3 L3 nos 36 e nos 54), cada um com `n_comuns, b, c, delta_pp, p_mcnemar, mesma_maquina, mesmos_fixtures`.

`comparacao_fases.md` gerado do JSON: tabela por modelo; modos de falha; pareamentos com coluna "pareável?"; parágrafo de ganhos/riscos/perdas por fase com números interpolados (nenhum digitado). O Memorial `comparacao-entre-fases.md` cola e interpreta. Prompts idênticos entre 2-B e 3 são a condição da comparação (sensibilidade a formato: até 76 pontos por formatação, SCLAR et al., 2024).

## 10. Ordem de execução e verificação

| # | Tarefa | Depende | Verificação |
|---|---|---|---|
| 1 | Fixtures (§7.1) | — | `python validar_banco.py --indice` → 0 problemas; posições dos 4 casos impressas |
| 2 | `biblioteca.py` + `recuperacao.py` + `validar_banco.py` (§6.6) | 1 | `python biblioteca.py` → válida; `python recuperacao.py` → mesmos hit@k da tarefa 1 |
| 3 | `caminhos.fase3()` | — | `python -c "import caminhos;print(caminhos.fase3())"` |
| 4 | Refatoração de `executar_bateria.py` | — | 1 caso A2 em `tmp_check`: mesmas chaves do JSONL da 2-B |
| 5 | `evolucao_biblioteca.py` + `testar_fase3.py` | 2 | `python testar_fase3.py` → `N testes ok` |
| 6 | `estrategias.proposta_de_edicao` | — | teste do prefixo |
| 7 | `executar_fase3.py` | 3–6 | piloto: `$env:RESULTADOS_DIR="resultados_alvo"; python executar_fase3.py --modelos qwen2.5-coder:3b --casos 10 --epocas 1 --saida fase3_piloto` (~20–30 min) → arquivos, hash, `epoca-1/`, `historico.jsonl`, `diff__E1.md`; projeção de tempo impressa |
| 8 | `avaliar_fase3.py` | 7 | roda sobre o piloto; testes de Cochran/Holm |
| 9 | `comparar_fases.py`, `gerar_graficos_fase3.py`, `gerar_relatorio_fase3.py` | 8 | sobre o piloto; figuras 12–17 em `fase3_piloto\graficos\` |
| 10 | `rodar_fase3.ps1` | 7–9 | bytes iniciais `EF BB BF`; nenhum `—`; `-Piloto` completo |
| 11 | Piloto de retomada | 10 | Ctrl+C no meio de uma época e relançar → continua; `epoca-1` reconstruída com o mesmo hash |
| 12 | Pré-registro no Memorial + plano aprovado + handoff corrigido + README | — | textos no lugar antes de rodar |
| 13 | **Perguntar ao Eric quando a máquina pode ficar ocupada (~60 h)**; lançar `rodar_fase3.ps1` em segundo plano; acompanhar `fase3.log`; avisar ao terminar | 11–12 | 4 × 4 `fechamento.json`, 4 × 360 diagnósticos, 4 × 162 propostas (o avaliador acusa faltas) |
| 14 | Eric preenche `revisao_edicoes__*.md`; `avaliar_fase3.py` de novo | 13 | `revisao_humana` sem `sem_avaliacao` |
| 15 | Documentação (§11) | 13–14 | todo número dos `.md` conferido contra os JSON |

### 10.1 Testes (`testar_fase3.py`, asserts em Python puro, `tempfile`, < 30 s, sem LLM)
1 partição (54/36, 3+2 por célula, idempotente, JSON idêntico) · 2 `render == render_base` e `_texto_indexavel` inalterado para a original; `bib.validar` vazio · 3 parser (2 blocos; `NENHUMA`; sem `FIM`; TEXTO em duas linhas; negrito; `[id]`/`id`) · 4 um caso por código de rejeição (26), inclusive `copia_do_caso` com o sintoma de `lex-1` colado e `teto_notas_verbete` após 6 notas · 5 aplicar nota + retificação + novo verbete → invariante vazio, `validar` vazio, `render` com `Notas:`; alterar uma letra do Resumo / apagar palavra-chave → invariante acusa · 6 comentários `# ! Alteração de IA` originais preservados · 7 hash estável/sensível; diff conta 1 novo, N linhas, palavras-chave certas · 8 retomada: `abrir_epoca` reconstrói `epoca-1` com o mesmo hash; `fechamento.json` → pulada · 9 `cochran_q([[1,1,0],[1,0,0],[1,1,1],[0,0,0]])` → Q 3,0, gl 2, p 0,2231; `qui_quadrado_sf(7.815,3)≈0,05`, `(11.345,3)≈0,01`, `(3.841,1)≈0,05`, `(5.991,2)≈0,05`; `holm([0.01,0.04,0.03]) == [0.03,0.06,0.06]`; `mcnemar_exato(0,0) == 1.0`; `cohen_g` · 10 orçamento (3 verbetes no teto ≤ 1.800; 900 chars de notas → `teto_notas_verbete`) · 11 `proposta_de_edicao(p, r, …).startswith(p + "\n\n" + r)` · 12 acurácia balanceada e distribuição de rótulos em exemplo pequeno · 13 fixtures passam em `validar_caso`.

## 11. Documentação a produzir (tag de IA + motivo; números só de script)

| Caminho | Conteúdo |
|---|---|
| `claude-memoria\plano-aprovado-fase-3.md` | este plano, no formato do da 2-B, após aprovação |
| `claude-memoria\contexto\2026-09-09-…md` | ponteiro corrigido; tabela de fases com a nomenclatura de §3 |
| `memorial\1-decisoes-e-historico\decisoes.md` | decisões **29+**: nomenclatura; biblioteca por modelo com original intocada; somente-acréscimo + validação em código como pré-condição; partição 54/36 por hash com gabarito; épocas em lote (aplicação na pasta seguinte); 4 modelos × 3 épocas; teto global desligado e orçamento por prompt; fixtures corrigidos; acurácia balanceada como métrica primária; Faceli **3. ed. 2025** como livro-texto orientador; `historico-por-commit.md` |
| `memorial\3-resultados-e-analises\achados-dos-modelos.md` | 4.20 fechado; §4.29+: reprodutibilidade 2-B A2 × F3 L0 (86 casos); efeito das notas; tentativas de decorar; deslocamento do ouro por verbetes novos; custo do prefixo compartilhado |
| `…\fase-3-relatorio-por-modelo.md` | estrutura do relatório da 2-B: protocolo, partição, hipóteses H1–H6 e vereditos, curva por época, recuperação por biblioteca, documentação produzida, revisão humana, perfil por modelo, custo, ameaças à validade |
| `…\comparacao-entre-fases.md` | cola `comparacao_fases.md` + ganhos, riscos e perdas de cada fase + recomendação do modelo final |
| `memorial\2-pesquisa-e-literatura\` | **novos**: `memoria-gerida-pelo-modelo.md` (§6.6), `tokenizacao-e-arquitetura.md` (§6.7), `metricas-e-desenho-experimental.md` (§6.8, amplia 6.5), `levantamento-2026-09-11-fase-3.md` (as sínteses verificadas e as lacunas, na íntegra, para não se perder); **revisados** §6.1–6.5 com o Faceli 3. ed. 2025 (Cap. 10 avaliação; Cap. 4 distâncias; Cap. 7 conexionistas; Cap. 16 dados dinâmicos; Cap. 19 textos) e com as fontes verificadas (as seções hoje sem citação: baseline 82,4% → JOSEPH, 2026; "lacuna encontrada" em 6.2; BEIR e Wilson 1927 em 6.3/6.5); `referencias.md` recebe as ~110 referências verificadas por bloco, marcando suporte parcial com "[conferir]" |
| `Documentacao\Projeto de Pesquisa - ABNT 15287_2025 - V3.md` | Faceli → **3. ed. 2025**; §2.2, §2.4 (tokenização e janela), §2.6 (RAG e adesão), §3.2/§3.4 (partição, Cochran Q + Holm, revisão humana); REFERÊNCIAS só com o citado no corpo |
| `Documentacao\Memorial de Desenvolvimento.md` | índice: §6.6–6.8, §4.29+, os dois relatórios novos |
| `README.md` (`:433-470`) | scripts da Fase 3, como rodar, `fase3\bibliotecas\` |
| Ressalva | o conteúdo dos capítulos do Faceli foi verificado só pelo sumário; citações com página exigem o exemplar (Eric confirma) |

## 12. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Modelo nunca propõe (`NENHUMA`) ou só produz rejeitadas | é resultado (H4): `n_nenhuma` e histograma de motivos por época; prompt mostra o verbete dedicado e o veredito |
| Autoenvenenamento | flips ✓→✗ por época nos 36; H5 veta; L0 sempre reportado; curva L0..L3 + Cochran |
| Decorar o caso na biblioteca | 5-gramas em duas normalizações, id do caso proibido, motivo fora do BM25, 36 sem proposta; rejeições viram métrica |
| Estouro de `num_ctx` com biblioteca crescendo | tetos por verbete (550 + 800), por contexto (1.800), `teto_prompt` por proposta, guarda real em toda inferência |
| Granite (~38% do tempo) | por último; prefixo compartilhado; `--max-tokens-proposta` e `MAX_PROPOSTAS_POR_CASO` ajustáveis; retomada por caso |
| Interrupção/energia | JSONL com flush; snapshots fechados; época aberta reconstruída do JSONL com decisões re-validadas |
| RAM com 7B/8B | `EsperarRam`; um modelo por vez; `memoria_mb` em todo registro |
| Cache de prefixo não agir na proposta | `prefill_ms/token` da proposta vs diagnóstico reportado; custo real documentado (como a Verificação 0) |
| Parser aceitar saída ambígua | linhas fixas, bloco só com `FIM`, campos obrigatórios; dúvida = rejeição com código |
| Colisão com scripts da 2-B | tudo em `fase3\`; `bib.BASE` nunca escrita; `escrever_indice(raiz)` |
| Estimativa de tempo | ~60 h ditas explicitamente; piloto mede; Eric decide quando a máquina fica ocupada |

## 13. Fora do escopo (pendências a registrar)
Saída estruturada por `format`/GBNF (ablação futura); troca cruzada de bibliotecas; k = 5; embeddings densos; A5 sobre as bibliotecas finais; Friedman/diagrama CD entre fases; Fases 4 e 5.

## 14. Manutenção paralela (pequena)
- **Memória do Claude com dois slugs**: a pasta desta sessão (`…\projects\c--Users-Eric-Derre-Documents-TCC\memory\`) está **vazia**; a memória real está em `…\c--Users-Eric.Derre-Documents-TCC\memory\` (com dois `.recebido-…` ao lado). Causa: `claude-memoria/importar.ps1:19` e `exportar.ps1:11` trocam só `[:\\/]` por `-`; o Claude Code troca todo caractere não alfanumérico (o `.` de `Eric.Derre`). Correção: regex `'[^A-Za-z0-9]'` nos dois scripts (tag + motivo) e, nesta sessão, gravar no slug correto `MEMORY.md` + as 3 memórias (versão de 09/09) + uma memória nova com as decisões de hoje.

---

<!-- ! Alteração de IA - Revisar: anexo acrescentado em 12/09/2026 (revisão final) com os desvios
     entre este plano e o que foi implementado, cada um com a origem (ruling do livro-razão da
     execução, `.superpowers/sdd/…/progress.md`, fora do git, ou relatório de tarefa) e a
     decisão correspondente em `Documentacao/memorial/1-decisoes-e-historico/decisoes.md`.
     ! Motivo: o texto do plano acima é a cópia aprovada pelo Eric e não é reescrito; sem este
     anexo, quem comparasse o plano com o código acharia contradições (26 códigos × 30;
     `tipo_invalido` que não existe; diffs fora de `epoca-<n>/`; 172 verificações × 166) sem
     saber qual dos dois vale e por quê. -->

<!-- ! Alteração de IA - Revisar: segunda passada de 12/09/2026 — no item 15 do anexo, a
     "limitação conhecida" dos acentos trocados no `fase3.log` passou a registrar a correção
     aplicada na onda final (`[Console]::OutputEncoding` em UTF-8 no `rodar_fase3.ps1`).
     ! Motivo: o item repetia do relatório da T12 que não havia correção; a revisão da T12
     concluiu o contrário e a onda final de correções aplicou o ajuste antes da chamada do
     Python (`rodar_fase3.ps1`, gravado às 19:26 de 12/09). O log do piloto, das 10:46, é
     anterior à correção e por isso ainda mostra `recupera├º├úo`. -->

<!-- ! Alteração de IA - Revisar: terceira passada de 12/09/2026 — item 18 do anexo: o §8.2 do
     plano falava em "poder 0,8" para o efeito mínimo detectável; o que
     `avaliar_fase3.efeito_minimo_detectavel` reporta é a diferença mínima significativa supondo
     20 % de pares discordantes.
     ! Motivo: achado M14 da revisão final (`final-fix-brief.md`): sem esta linha, quem lesse o §8.2
     e depois o `resumo_fase3.json` (`efeito_minimo_detectavel` = {n, discordantes, b_min,
     delta_pp}) procuraria um cálculo de poder que o script não faz e não acharia onde isso foi
     decidido. O §4 do relatório por modelo do Memorial foi corrigido na mesma passada. -->

## Anexo — Desvios do plano registrados no livro-razão (12/09/2026)

O texto do plano acima é o aprovado em 11/09/2026 e não foi reescrito. Onde o código ou os relatórios divergem dele, vale o que está abaixo — cada item com a origem e, quando há, a decisão numerada no Memorial (`decisoes.md`).

| # | Onde o plano diz | O que foi feito | Origem / decisão |
|---|---|---|---|
| 1 | §1: "172 verificações adversariais de citação" | Foram **166** (154 aprovadas + 12 rejeitadas), pela tabela por tópico do próprio levantamento (`Documentacao/memorial/2-pesquisa-e-literatura/levantamento-2026-09-11-fase-3.md`, §6.9) | Ruling na T14b: "usar 166" |
| 2 | §6.3: 26 códigos de rejeição, com `tipo_invalido`/`pasta_invalida` na checagem 10 | São **26 checagens em ordem fixa que devolvem 30 códigos** (`CODIGOS_REJEICAO` em `evolucao_biblioteca.py`, contados em 12/09/2026); `tipo_invalido` não existe — a checagem 10 ficou só com `pasta_invalida` | Decisão 33 (texto corrigido em 12/09) |
| 3 | §6.2: "linhas `CAMPO:` abrem campo" | Só abre campo a linha cujo nome (em maiúsculas) está no conjunto fechado `CAMPOS_PROPOSTA` (os 12 nomes do formato); qualquer outra linha com dois-pontos é continuação do campo aberto — resolve "Exemplo: …" dentro do TEXTO | Ruling na T5 |
| 4 | §6.2: "sem `FIM` → `malformado='sem FIM'`" | Bloco sem `FIM` é válido se a resposta não foi cortada no teto (`tokens_saida < max_tokens`) e os 4 campos obrigatórios existem; recebe `fim_ausente: true` (métrica); se cortada, continua "sem FIM". Refinamento da onda final: só o último bloco da resposta herda `truncada` | Decisão 38; item 2 da onda final |
| 5 | §6.3, checagem 7: id novo `^[a-z0-9]+(-[a-z0-9]+)*$` | Aceita também `_`: `^[a-z0-9]+([-_][a-z0-9]+)*$` — os ids originais misturam `_` e `-` | Ruling na T5 |
| 6 | §6.3, checagem 13 (`arquivo_inexistente`) | Itens de `ARQUIVOS` e nomes de arquivo citados no `TEXTO`: sufixo `:linha` descartado; nome sem pasta aceito quando identifica um único arquivo do código do cobaia (índice restrito a `Programacao/`, fora de `resultados*`, `.superpowers`, `graficos` e `base_conhecimento`) | Decisões 39 e 42 |
| 7 | §6.3, checagem 18 (`trecho_nao_encontrado`) | Um par de aspas delimitadoras em volta do `TRECHO` é removido **antes** da busca em `render_base(alvo)` | Decisão 41 |
| 8 | §6.3, checagem 14 (`endpoint_inexistente`, regex `\b(GET|POST) /api/[\w/{}]+`) | O endpoint citado é cortado em `[^\s?|)]`, como em `rec.sinais_do_caso`, para `?login=…` não virar endpoint inexistente | Decisão 43 |
| 9 | §6.7 e §7: `diff__E<n>*` "gravado em epoca-<n>/" | Os diffs ficam **fora** do snapshot: `bibliotecas/<slug>/diff__E<n>.{json,md}` e `diff__E<n>__vs_original.{json,md}`, irmãos de `epoca-<n>/`, para o snapshot conter só verbetes + `INDICE.md` + `fechamento.json` | Ruling na T4 |
| 10 | §7, `executar_fase3.py`: "época aberta é reconstruída de `propostas__E<n>.jsonl`" | Além de reconstruir a pasta, `abrir_epoca` regrava as linhas de `historico.jsonl` da época a partir do JSONL (fonte da verdade) | Decisão 40 |
| 11 | §7, `executar_fase3.py`: CLI com 8 opções | Acrescentados `--so-projecao` (imprime a projeção de tempo e sai, sem inferência) e, em `rodar_modelo_fase3`, um 9º parâmetro opcional `original=bib.BASE`, para a biblioteca de partida chegar até `preparar_epoca_0` | Relatório da T7 |
| 12 | §12: interrupção/energia | Inferência que volta com `erro` é repetida até 3 tentativas no total (pausas de 30 s e 60 s entre elas); persistindo, `SystemExit` sem gravar registro — nunca se propõe edição a partir de diagnóstico com erro | Rulings na revisão da T7 |
| 13 | §4.3: "~60 h" | A projeção impressa pelo executor (`--so-projecao`) dá **67,18 h** para 4 modelos × 3 épocas; ela mantém as constantes de ms/token da 2-B, de propósito conservadora. O piloto de 10 casos (12/09/2026) levou 00h13 e valida o encanamento, não o custo dos quatro modelos | Ruling na T7; relatórios da T7 e da T12 |
| 14 | §10, item 11: "Ctrl+C no meio de uma época e relançar" | O teste de retomada apagou `diagnosticos__L1.jsonl` e o `fechamento.json` da `epoca-1` com o piloto concluído e relançou: a `epoca-1` foi reconstruída com o mesmo hash (`3196327e7fd5`) e só a passada final foi refeita | Relatório da T12 |
| 15 | §7, `rodar_fase3.ps1`: "copia literal de `Marco, Falha, Rodar, …`" | `Rodar` não usa `Tee-Object` (no Windows PowerShell 5.1 ele grava o log em UTF-16): trocado por `ForEach-Object` + `Add-Content -Encoding utf8`. O mesmo defeito continua em `rodar_fase2b.ps1` e no `fase2b.log` já gravado (pendência do Eric). Os acentos trocados no `fase3.log` do piloto vinham da codepage com que o PowerShell decodificava a saída do Python: corrigido na onda final de correções com `[Console]::OutputEncoding` em UTF-8 no `rodar_fase3.ps1`, antes de chamar o Python (achado da revisão da T12); conferido no piloto v2 de 13/09/2026: `fase3.log` sem bytes nulos e sem acentos trocados — só legibilidade do log; JSONL/JSON corretos | Relatório da T12; revisão da T12; onda final de correções; piloto v2 (§9 do relatório da Fase 3) |
| 16 | (não previsto) versão do Ollama | O Ollama atualizou sozinho de 0.33.3 (2-B) para **0.34.0** em 12/09/2026, antes da bateria; decidido não reverter. A versão passa a ir em todo registro e a corrida aborta se ela mudar no meio | Ruling de 12/09; decisão 44 |
| 17 | §11: "decisões 29+" | Registradas as decisões **29 a 44** em `decisoes.md`; as 41 a 44 saíram da revisão final de 12/09/2026 e são implementadas na onda final de correções | `decisoes.md` |
| 18 | §8.2: "Efeito mínimo detectável com n = 36 e n = 90 (McNemar, α 0,05, poder 0,8)" | `avaliar_fase3.efeito_minimo_detectavel` **não calcula poder**: para n = 36, 54 e 90 reporta a menor diferença em pontos percentuais que o McNemar exato aponta como significativa a α 0,05 supondo 20 % de pares discordantes (d = round(0,2·n); menor b acima de d/2 com p < 0,05), gravada em `resumo_fase3.json` → `efeito_minimo_detectavel` como `{n, discordantes, b_min, delta_pp}`. O Memorial (§4 do relatório por modelo) foi corrigido para dizer isso | Achado M14 da revisão final de 12/09/2026 (`final-fix-brief.md`); relatório `final-pilot-report.md` |
