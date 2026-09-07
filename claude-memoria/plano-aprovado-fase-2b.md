# Plano — Fase 2-B: biblioteca de documentação como fonte da verdade

## Contexto

A Fase 2-A mediu **6 modelos × 90 casos × 3 estratégias**, em CPU, **sem documentação do sistema**. Resultado consolidado (o Granite ainda termina as estratégias em estágios — 123/270 — mas o braço linear dele já fechou):

| Modelo | Causa (linear) | Causa (agregado) | Fora do conjunto | Seg/caso |
|---|---|---|---|---|
| `granite4.2:8b` | **67,8%** | — | 0,0% | 47 |
| `qwen2.5:7b` | 53,3% | 50,0% | 2,6% | 18 |
| `qwen2.5-coder:7b` | 48,9% | 50,0% | 1,9% | 25 |
| `qwen2.5-coder:3b` | 25,6% | 27,0% | 0,0% | 9 |
| `phi4-mini:3.8b` | 23,3% | 18,9% | **17,8%** | 10 |
| `qwen2.5-coder:1.5b` | 5,6% | 7,4% | 0,0% | 7 |

**Achado que decide o desenho desta fase:** agregando os 5 modelos completos, **linear (37,4%) vence as duas estratégias em estágios** (29,7% "compilador", 31,1% "domínio"). Confirma o prior da literatura registrado no Memorial §6.2. Logo, a Fase 2-B **fixa o prompt em linear** e passa a variar a biblioteca — cruzar 3 estratégias × condições de biblioteca triplicaria o custo sem responder nada novo.

O teto atual é 67,8%, logo abaixo da meta de 70–80%. A pergunta da Fase 2-B: **uma biblioteca de documentação fecha essa lacuna, por quê, e a que custo de tempo?**

Decisões já tomadas por você nesta rodada: **grade completa** (~2.000 inferências) e **documentar os defeitos conhecidos com marcação separada** no frontmatter.

Nesta fase os modelos **só consultam** a biblioteca. A geração/gestão dela pelo próprio modelo (decisão nº 13 do Memorial) passa a ser Fase 3.

**Nada roda até o Granite terminar.** Esta fase é preparação: biblioteca, harness, validadores, memorial.

---

## 1. O que a pesquisa disse (2024+) e o que muda no desenho

Cada item abaixo entra no `Memorial de Desenvolvimento.md` (§6.3–6.5) com a citação completa.

### 1.1 Documentação no contexto: ajuda, mas a posição e a quantidade importam

- **Lost in the Middle** (Liu et al., TACL 2024): com 20 documentos, GPT-3.5-Turbo acerta **75,8%** se o documento certo está na posição 1, **53,8%** na posição 10 e **63,2%** na 20 — e o meio fica **abaixo do closed-book (56,1%)**. LongChat-13B: 68,6% → 55,3% → 55,0%. Modelos abertos pequenos não têm a recuperação no fim.
- **Context Rot** (Hong, Troynikov & Huber, Chroma, 2025): 18 modelos; degradação perceptível já **a partir de ~2.500 tokens**; **um único distrator** já reduz o acerto, quatro compõem; haystack coerente é *pior* que embaralhado.
- **Classifier Context Rot** (Martin & Roger, 2026): classificadores erram **2× a 30× mais** quando o alvo vem depois de muito contexto benigno — é exatamente o formato da nossa tarefa (classificação num conjunto fechado).
- **Long Context vs RAG** (Li, Cao, Ma & Sun, 2024, arXiv 2501.01880): contexto inteiro vence para modelos fortes; **modelos abertos pequenos se beneficiam da recuperação** por capacidade limitada de contexto longo; recuperação por chunk perde para recuperação por resumo.
- **The Power of Noise** (Cuconasu et al., SIGIR 2024) achou +30% com documentos aleatórios; **The Powerless Noise** (Mazuryk et al., SIGIR 2026) reproduziu e mostrou que o efeito **aparece, enfraquece ou some** com pequenas mudanças de prompt e de limite de decodificação, e que truncamento explica boa parte da variância. Ligação direta com o nosso artefato do `num_predict=400`.

**→ Mudanças:** (a) a biblioteca entra **no início** do prompt e o caso **no fim** — as duas posições boas, e a única ordem compatível com cache de prefixo; (b) manter **dois braços de biblioteca** (inteira e recuperada), porque a literatura prevê que recuperada ≥ inteira nos modelos pequenos — hipótese testável; (c) teto de **4.000 tokens** para a biblioteca inteira (orçamento: 4.000 + caso ≤1.200 + formato ~300 + resposta ≤1.200 < 8.192).

### 1.2 O modelo segue a documentação ou a memória?

- **Investigating Context-Faithfulness** (Li et al., ACL 2025): quanto mais forte a memória paramétrica, mais o modelo ignora a evidência; evidência **parafraseada** aumenta a adesão muito mais que repetição literal.
- **Knowledge Conflicts survey** (Xu et al., EMNLP 2024) e **ConflictBank** (Su et al., 2024): viés sistemático a favor da evidência que concorda com o prior.

**→ Mudanças:** (d) verbetes escritos como **paráfrase em linguagem de domínio**, não cópia do código — o código fica como referência (`arquivo:linha`), a explicação vem reescrita; (e) o braço **adversarial (A5)** deixa de ser opcional: é o único que mede se o modelo confia na documentação quando ela contradiz o prior.

### 1.3 Recuperação em CPU

- BM25 segue forte fora de domínio (BEIR); híbrido BM25+denso via RRF ganhou **+8,1 pp Recall@5** em documentos com tabelas (arXiv 2604.01733); **reranking não se justifica em corpus pequeno e curado** onde a recuperação já acerta no topo.
- Chunking (Vectara, NAACL 2025; arXiv 2505.21700): **tamanho fixo venceu chunking semântico**; a configuração pesa tanto quanto o modelo de embedding; faixa 256–512 tokens.
- **MTEB-BR** (Stekel, 2026): 93 modelos em 22 tarefas em pt-BR; **`embeddinggemma-300m` fez 0,649** contra 0,670 do Qwen3-Embedding-8B — os seis líderes ficam a 0,020 um do outro. Está no Ollama (`embeddinggemma:300m`, verificado no registro).

**→ Mudanças:** (f) recuperação principal = **filtro estruturado por frontmatter + BM25** em biblioteca padrão — **zero dependência nova**, preserva o "hit and run"; (g) sem reranker; (h) *k* = 3, com sensibilidade a *k* ∈ {1, 3, 5} medida **offline** contra o gabarito de recuperação (sem inferência de LLM); (i) embedding denso (`embeddinggemma` via `/api/embed` do Ollama, sem dependência Python) entra **só como ablação de recuperação**, também offline.

### 1.4 Formato e medição

- **Does Prompt Formatting Have Any Impact?** (He et al., 2024): até **40% de variação** no GPT-3.5 conforme o formato; GPT-4 robusto. Sem vencedor universal.
- **Dietterich (1998)**, referência canônica: para algoritmos executados **uma vez** sobre o mesmo conjunto, **McNemar** é o único teste com erro tipo I aceitável. É exatamente o nosso caso.
- Prefill é limitado por computação; decodificação, por banda de memória (SARATHI, 2023; literatura de serving). A biblioteca infla o **prefill**.
- **Cache de prefixo no Ollama**: o llama.cpp reaproveita o KV do prefixo comum por slot (`cache_prompt`). No Ollama, a issue **#14780** documenta que o backend de CPU do motor novo **não reaproveitava nada** na v0.17.1 (tempo crescendo linearmente por turno); correções aparecem referenciadas na v0.30.8. Esta máquina está na **0.33.2** — **não dá para assumir**: precisa de medição.

**→ Mudanças:** (j) Markdown mantido, **sem ablação de formato** (custo) — registrado como ameaça à validade; (k) `avaliar.py` ganha **McNemar pareado por caso** e **IC de Wilson**; (l) **Verificação 0**, antes de qualquer bateria: duas chamadas consecutivas com o mesmo prefixo, comparando `prompt_eval_count` e `prompt_eval_duration`. Se o cache funciona, o prefill da biblioteca é pago uma vez por modelo e o braço "inteira" fica quase de graça em tempo; se não, o custo é real e entra no resultado.

### 1.5 Quantização (documentação + uma ablação barata)

Verificado nesta máquina: **os 6 modelos estão em Q4_K_M** (`ollama show`), a quantização padrão das tags sem sufixo.

- **Lee et al., IJCAI 2025** (arXiv 2409.11055), 1B–405B, 13 datasets: a 4 bits, **Llama-3.2-1B perde 10,1 pp** (GPTQ) / 5,7 pp (AWQ) em média e **16,0 pp no IFEval**; **3B perde 1,8 pp** (IFEval −0,75); **8B perde 1,3–1,8 pp** (IFEval −2,1). Quantizados sofrem mais em seguir instrução. Só inglês.
- **Low-Bit Quantization Favors Undertrained LLMs** (Ouyang et al., ACL 2025): 1.500 checkpoints, 160M–12B; **modelos pequenos com muitos tokens de treino degradam mais**. O Qwen2.5 (18T tokens) é o caso extremo.
- **Accuracy is Not All You Need** (Dutta et al., NeurIPS 2024): mesma acurácia (±2%) esconde **até 13,6% de *flips*** — respostas que mudam de certo para errado e vice-versa. Comparar quantizações exige medir flips.
- **On-Device LLMs** (Song et al., 2025): limiar prático em **~3,5 bits/peso**; modelo maior quantizado > modelo menor em precisão alta.
- i-quants (IQ*) usam *codebook* com muitas leituras de tabela — **mais lentos em CPU**; ficar nos k-quants. Cache KV em `q8_0` é quase sem perda mas exige flash attention; `q4_0` chega a **92% mais lento** em contexto longo — **não mexer** nesta fase (quebraria comparabilidade com a 2-A).

**→ Mudanças:** (m) **ablação de quantização no piso**: `qwen2.5-coder:1.5b` em `q8_0` e `fp16` (tags verificadas) no braço A0-linear — 180 inferências, ~25 min — testa se o 7,4% é limitação do modelo ou artefato do Q4 num modelo pequeno e supertreinado; reporta **flips** contra o Q4_K_M. Se mudar muito, a conclusão "1.5B é inviável" precisa de ressalva. (n) Q4_K_M mantido para os 6 principais; a tabela de níveis com fontes vai para o Memorial §6.4.

---

## 2. A biblioteca base

Uma só, idêntica para todos, versionada em `Programacao/AgenteCore/base_conhecimento/`. Duas seções, como pedido. Todo o conteúdo abaixo foi conferido no código — nada presumido.

### 2.1 Seção teórica — regras de negócio (`negocio/`)

Entidades: **Tipo, Produto, Usuário, Pedido/Reserva** (`tbtipos`, `tbprodutos`, `tbusuarios`, `tbpedido_reserva`, view `vw_tbpedidos`). Um verbete por entidade e um por fluxo (catálogo, busca, detalhe, login, reserva, cancelamento).

| Regra real | Onde | Por que importa ao diagnóstico |
|---|---|---|
| Reserva só entre **hoje+2** e **hoje+90** dias | [registrar_reserva.php:24-35](Programacao/CobaiaFront/cliente/registrar_reserva.php#L24-L35) | Só como `min`/`max` do `<input type="date">`; **nem PHP nem API validam no servidor** |
| `pessoas` ≥ 1 | [registrar_reserva.php:55](Programacao/CobaiaFront/cliente/registrar_reserva.php#L55) | Só no HTML |
| Status ∈ {`Em Análise`, `Cancelado`} | [schema_completo.sql:37](Programacao/CobaiaFront/banco/schema_completo.sql#L37), [pedidos.py:57,75](Programacao/CobaiaAPI/app/routers/pedidos.py#L57) | Qualquer outro valor é `valor_fora_do_dominio` |
| `destaque_produto` `ENUM('Sim','Não')` → **booleano** na API | [models.py:36](Programacao/CobaiaAPI/app/models.py#L36), [produtos.py:30](Programacao/CobaiaAPI/app/routers/produtos.py#L30) | Tradução entre camadas |
| `valor_produto` `DECIMAL(9,2)` → `float` na API | [produtos.py:28](Programacao/CobaiaAPI/app/routers/produtos.py#L28) | `89.90` vira `89.9`; o schema declara `Decimal`, o fio manda número |
| `login_usuario` **é o CPF** do cliente | [pedidos.py:26,35](Programacao/CobaiaAPI/app/routers/pedidos.py#L26) | Chave de junção |
| **Busca de cliente: substring no monolito, exata na API** | [cliente/index.php:4](Programacao/CobaiaFront/cliente/index.php#L4) (`LIKE '%x%'`) vs [pedidos.py:35](Programacao/CobaiaAPI/app/routers/pedidos.py#L35) (`==`) | Divergência real front×API |
| `vw_tbpedidos` com **LEFT JOIN** de `tbusuarios` | [schema_completo.sql:57-61](Programacao/CobaiaFront/banco/schema_completo.sql#L57-L61) | Cliente sem reserva vira **uma linha com campos nulos**; `reserva_cli.php` usa `do…while` e renderiza essa linha vazia — origem legítima de `nulo_inesperado` e `estado_da_tela_divergente` |
| Login compara senha **em texto puro**; `sup` → admin, `cli` → cliente, falha → `invasor.php` | [login.php:7-29](Programacao/CobaiaFront/admin/login.php#L7-L29) | |

**O que o sistema NÃO faz** (verbetes com `tipo: limite`): não valida data nem `pessoas` no servidor; não confere retorno de `$conn->query()` em página nenhuma (falha SQL **silenciosa**); não checa se a reserva cancelada pertence ao cliente logado ([cliente_cancelar.php:6](Programacao/CobaiaFront/cliente/cliente_cancelar.php#L6)); não faz hash no login; a API **não valida a resposta** pelo `response_model` — o `/docs` descreve o esperado, não o que sai.

### 2.2 Seção técnica (`contratos/`, `erros/`, `falhas_injetadas/`)

**B1. Contratos** — os 6 endpoints, campo a campo, com a coluna "declarado × real" (o bypass por `JSONResponse` em [produtos.py:1-7](Programacao/CobaiaAPI/app/routers/produtos.py#L1-L7)).

**B2. Erros genéricos de requisição** — 400, 403, 404, 408, 422 (validação do FastAPI, ex.: `login` ausente em `GET /api/pedidos`), 429, 500, 502, 503, 504, timeout, CORS, corpo vazio, JSON malformado. Cada um: o que significa nesta fronteira, como aparece no navegador, como distinguir dos vizinhos.

**B3. Erros tratados no código com mensagem própria** — o núcleo do pedido. Cada verbete: arquivo:linha, mensagem literal, condição, motivos possíveis.

| Mensagem literal | Onde | Dispara quando |
|---|---|---|
| `"produto não encontrado"` 404 | [produtos.py:52](Programacao/CobaiaAPI/app/routers/produtos.py#L52) | `db.get` vazio |
| `"cliente não encontrado"` 404 | [pedidos.py:37](Programacao/CobaiaAPI/app/routers/pedidos.py#L37) | nenhum `login_usuario` igual ao `login` |
| `"cliente não encontrado"` 404 | [pedidos.py:52](Programacao/CobaiaAPI/app/routers/pedidos.py#L52) | `id_clientes` inexistente — **mesma mensagem, causa diferente** |
| `"pedido não encontrado"` 404 | [pedidos.py:74](Programacao/CobaiaAPI/app/routers/pedidos.py#L74) | cancelar id inexistente |
| `"token inválido (header X-Admin-Token)"` 403 | [admin_fault.py:20](Programacao/CobaiaAPI/app/routers/admin_fault.py#L20) | header ausente/errado |
| `"modo inválido, use um de: [...]"` 400 | [admin_fault.py:34](Programacao/CobaiaAPI/app/routers/admin_fault.py#L34) | `mode` fora dos 7 |
| `"fault injection: error_500 em <ent>"` 500 | [fault_injection.py:71](Programacao/CobaiaAPI/app/fault_injection.py#L71) | modo `error_500` |
| `"Atenção ERRO: <throwable>"` | [connect.php:16](Programacao/CobaiaFront/conn/connect.php#L16) | falha MySQL — **HTML onde deveria haver JSON** |
| `"HTTP <status>"` | [produtos_api.php:95,117](Programacao/CobaiaFront/produtos_api.php#L95) | `resp.ok` falso |
| `"Nenhum produto retornado pela API."` | [produtos_api.php:100](Programacao/CobaiaFront/produtos_api.php#L100) | não é array **ou** vazio — ambíguo de propósito |
| `"Erro ao carregar produtos da CobaiaAPI: <msg>"` | [produtos_api.php:107](Programacao/CobaiaFront/produtos_api.php#L107) | qualquer rejeição do `fetch` |
| `"falha no email"` + `ErrorInfo` | [rodape_contato_envia.php:33](Programacao/CobaiaFront/rodape_contato_envia.php#L33) | SMTP |

**B4. Os 7 modos de injeção** com efeito exato no fio. **B5. Defeitos mantidos de propósito** (`tipo: defeito_conhecido`): âncora do "Saiba Mais" com aspas fora do lugar em [produtos_geral.php:51](Programacao/CobaiaFront/produtos_geral.php#L51) (a linha 34 está certa — contraste útil), senha texto-puro/MD5, query sem checagem, cancelamento sem dono. **B6. Índice sintoma → verbete.**

### 2.3 Formato

Um `.md` por assunto, frontmatter em **subconjunto plano de YAML** (`chave: valor` e `chave: [a, b]`) parseado por ~20 linhas de biblioteca padrão — sem `pyyaml`, sem ambiguidade de tipo. Campos: `id, titulo, sistema, entidade_principal, tipo (funcionamento|regra|contrato|erro|defeito_conhecido|limite), status, arquivos, endpoints, tabelas, sintomas, palavras_chave, causas_relacionadas`. Corpo em seções fixas; **Resumo** de 1–3 frases é o que entra no prompt no braço recuperado. Texto em paráfrase de domínio (§1.2-d). Cobertura obrigatória: **as 23 causas raiz** (todas aparecem no banco, 2–7 casos cada).

### 2.4 Ameaça à validade

A biblioteca documenta **o sistema**, nunca os 90 casos. Salvaguardas: (1) validador recusa verbete com sobreposição alta com `corpo`/`sintoma` de qualquer caso; (2) resultados separam acerto em casos **com verbete de defeito dedicado** × sem — é a marcação que você escolheu.

---

## 3. Desenho experimental (grade completa)

Prompt **fixo em linear**; biblioteca **antes** do caso.

| Braço | Contexto | Mede | Modelos |
|---|---|---|---|
| A0 | nenhum | linha de base — **reaproveita a 2-A**, não re-roda | 6 (feito) |
| A1 | biblioteca inteira (≤4k tokens) | teto do "tudo em contexto" + custo de prefill | 6 |
| A2 | top-3 recuperado (filtro + BM25) | cenário real | 6 |
| A3 | só o verbete certo (ouro) | **teto superior**; separa recuperação de raciocínio | 3 |
| A4 | 3 verbetes irrelevantes | distração | 3 |
| A5 | verbete com informação **errada** sobre o caso | adesão cega × raciocínio | 3 |
| Q8 | A0-linear, `1.5b` em `q8_0` e `fp16` | artefato de quantização no piso | 1 |

Os 3 modelos das ablações: **`granite4.2:8b`** (melhor), **`qwen2.5-coder:3b`** (mediano e padrão de produção atual) e **`phi4-mini:3.8b`** (piso não-degenerado). O `1.5b` fica fora das ablações porque responde `corpo_nao_e_json` em 84% dos casos — ablação sobre modelo que não faz a tarefa não ensina nada; ele já entra em A1/A2 e na Q8.

**Custo:** 1.080 + 810 + 180 = **~2.070 inferências**. Tempo: **~25–35 h se o cache de prefixo funcionar; 40–60 h se não** (a diferença é o prefill de ~4k tokens em CPU, ~40–160 s/chamada conforme o modelo). Por isso a Verificação 0 vem primeiro e, se o cache não funcionar, a biblioteca inteira é reduzida a ≤2,5k tokens (limiar do Context Rot) antes de rodar A1.

### 3.1 Ordem de execução (depois do Granite)

1. **Verificação 0** — cache de prefixo (5 min).
2. **Q8** — ablação de quantização (25 min).
3. **A1 e A2** nos 6 modelos.
4. **A3, A4, A5** nos 3 modelos.
5. `avaliar.py` → `gerar_graficos.py` → relatório HTML → `RESULTADO_FASE2B.md`.
6. Memorial.

---

## 4. Métricas

Mantém as da 2-A e acrescenta: **Δ vs A0** por modelo/classe/nível; **custo da documentação** (`prompt_eval_count`, `prompt_eval_duration`, `eval_duration` — separados); **recuperação** (verbete certo entre os *k*; sensibilidade a *k* offline); **ancoragem** (a resposta cita o `id` do verbete); **sensibilidade a contexto ruim** (A4, A5 vs A3); **acerto com × sem verbete de defeito dedicado**; **flips** na Q8; **McNemar** pareado por caso entre condições e **IC de Wilson** por proporção; tempo reportado como **mediana e IQR** sobre os 90 casos (não média).

---

## 5. Alterações no harness

| Arquivo | Mudança |
|---|---|
| [cliente_ollama.py:49-73](Programacao/AgenteCore/experimentos/cliente_ollama.py#L49-L73) | `gerar()` passa a gravar `prompt_eval_duration`, `eval_duration`, `load_duration`, `total_duration` (hoje descartados); ganha `embed(modelo, texto)` para a ablação de recuperação |
| [executar_bateria.py](Programacao/AgenteCore/experimentos/executar_bateria.py) | `--condicao {A1,A2,A3,A4,A5}`; chave de retomada vira `(caso, estrategia, condicao)`; arquivo `<modelo>__<condicao>.jsonl`; registro ganha `condicao`, `verbetes_ids`, `tokens_biblioteca` |
| `biblioteca.py` (novo) | carrega `base_conhecimento/`, parser do frontmatter plano, validador (esquema, arquivos/tabelas/endpoints existentes, sobreposição com casos, cobertura das 23 causas), contagem de tokens |
| `recuperacao.py` (novo) | filtro por frontmatter (endpoint, entidade, status) + BM25 em stdlib; `gabarito_recuperacao` (caso → verbetes esperados); avaliação offline de *k* e do embedding |
| `estrategias.py` | `linear_com_biblioteca(caso, contexto)` — biblioteca como prefixo estável, caso e formato no fim |
| [avaliar.py](Programacao/AgenteCore/experimentos/avaliar.py) | cortes por `condicao`; Δ vs A0; McNemar; Wilson; ancoragem; recuperação; flips; erros de infraestrutura contados à parte |
| [gerar_graficos.py](Programacao/AgenteCore/experimentos/gerar_graficos.py) | 5 gráficos novos (Δ por modelo; A1×A2×A3; custo de prefill × acerto; A4/A5; Q8 flips) na mesma paleta |
| `verificar_cache_prefixo.py` (novo) | Verificação 0 |
| `relatorio.html` | navegável por modelo/condição/classe/nível com resposta crua |

---

## 6. Revisão do código não-PHP (pedido desta rodada)

Lido integralmente: instalador, `_env_common`, `run`, `Cobaia`, scripts de shell, CobaiaAPI (app + testes + config), `experimentos/`. O código está bem comentado e coerente; o que segue é o que de fato vale mexer. **Bugs primeiro.**

| # | Onde | O que | Proposta | Prioridade |
|---|---|---|---|---|
| 1 | [config.py:21](Programacao/CobaiaAPI/app/config.py#L21) | Só `fault_mode` é lido do `.env`; **não existe `fault_target_field`**. `FAULT_MODE=type_drift` por variável de ambiente **não faz nada** (em [fault_injection.py:74](Programacao/CobaiaAPI/app/fault_injection.py#L74) `field` fica `None`) — contradiz a promessa de "runs determinísticos por env var" da docstring | Adicionar `fault_target_field: Optional[str] = None` ao `Settings`, passar ao `FaultState`, documentar no `.env.example` | **Alta** — a Fase 5 depende disso |
| 2 | [tests/](Programacao/CobaiaAPI/tests/test_produtos.py) | 3 testes de fumaça; **nenhum protege o bypass do `response_model`**, que é a decisão central da API, nem as rotas de pedido | `test_type_drift_chega_ao_fio` (liga o modo via admin, `GET /api/produtos`, afirma `preco` texto) + testes de `pedidos` | **Alta**, custo baixo |
| 3 | [_env_common.py:346-350](_env_common.py#L346-L350) | `stop_managed_mariadbd` só faz `terminate()` — mata o servidor de forma abrupta; na próxima subida o InnoDB entra em recuperação | `mariadb-admin -u root shutdown` (verificado: `mariadb-admin.exe` existe na instalação do winget), `terminate` como plano B | Média |
| 4 | [_env_common.py:228](_env_common.py#L228) | `modelo in resultado.stdout` é busca de substring — `qwen2.5:7b` casa com `qwen2.5:7b-instruct-q8_0` | Comparar com a primeira coluna de cada linha, ou usar `/api/tags` como já faz `cliente_ollama.instalados()` | Média |
| 5 | [cliente_ollama.py:68-73](Programacao/AgenteCore/experimentos/cliente_ollama.py#L68-L73) | Descarta a decomposição de tempo que o Ollama já devolve | §5 | **Alta** (bloqueia a 2-B) |
| 6 | [executar_bateria.py:24-36](Programacao/AgenteCore/experimentos/executar_bateria.py#L24-L36) | Chave de retomada sem condição | §5 | **Alta** (bloqueia a 2-B) |
| 7 | [install.py:37-95,144-175](install.py#L37-L95) | Quatro blocos "procura → instala → procura de novo → sai" quase iguais (PHP, MariaDB, Ollama, Python) | `ensure_tool(nome, localizar, instaladores_por_so)` em `_env_common` | Baixa — só se for tocar no arquivo |
| 8 | [install.py:133,198-200](install.py#L133), [run.py:49](run.py#L49) | Caminho `Scripts/`×`bin/` da venv calculado de 3 jeitos | `venv_bin(venv, nome)` | Baixa |
| 9 | [install.py:218](install.py#L218) | Padrão `qwen2.5-coder:3b` com comentário citando a Fase 2 antiga; a 2-A mostra 27% contra 68% do Granite | **Não mudar agora** — decidir depois da 2-B, com acerto × tempo; atualizar comentário e `RESULTADO_FASE2.md` com nota de superação | Config |
| 10 | [admin_fault.py:23-27](Programacao/CobaiaAPI/app/routers/admin_fault.py#L23-L27) | `GET /fault-mode` sem token revela o modo ativo | Exigir token no GET também, ou registrar como limite do cenário | Baixa |
| 11 | [avaliar.py:101-127](Programacao/AgenteCore/experimentos/avaliar.py#L101-L127) | Falha de rede (`segundos None`) conta como resposta errada | Contar `erros_infra` à parte | Baixa |
| 12 | `benchmark_modelos.py`, `teste_diff_previo.py` | Cliente do Ollama duplicado (anterior à extração) | **Manter congelados** — são o registro da 1ª leva; só acrescentar nota no cabeçalho | Doc |
| 13 | `taxonomia.validar_caso` | Nunca roda automaticamente sobre os 90 casos | `validar_banco.py` (também valida a biblioteca) | Baixa |

Não encontrei nada que justifique reestruturação de pastas ou troca de biblioteca. `Cobaia.py`, `run.py`, os wrappers `.cmd/.ps1/.sh` e o `build_exe.ps1` estão simples e corretos como estão.

---

## 7. Memorial de Desenvolvimento — o que entra

- §2: decisões **18** (fixar linear), **19** (biblioteca antes do caso), **20** (defeitos com marcação), **21** (grade completa), **22** (BM25 sem dependência; denso só como ablação), **23** (GPT-2/3 descartados — motivo), e nota na **13** (gestão da biblioteca vira Fase 3).
- §4: **4.16** "linear vence estágios" (números finais após o Granite); **4.17** "só 8/23 rótulos no 1.5B e 17,8% fora do conjunto no phi4-mini" (dois modos de falha distintos).
- §6.3 RAG/documentação, §6.4 quantização, §6.5 medição em CPU — todas as fontes de §1 com número e condição.
- §8: Verificação 0 pendente; PDF a regerar; modelo padrão a decidir.
- §9: ~20 referências novas.

---

## 8. Verificação

- `validar_banco.py` recusa: frontmatter inválido; referência a arquivo/tabela/endpoint inexistente; verbete que copia um caso (testado injetando os três de propósito); e acusa causa raiz sem cobertura.
- `verificar_cache_prefixo.py` imprime `prompt_eval_count` e `prompt_eval_duration` das duas chamadas — o segundo deve ser ~0 se o cache funciona.
- Matar `executar_bateria.py` no meio e reiniciar continua **da mesma condição**, sem repetir casos.
- Cada registro novo tem `condicao`, `verbetes_ids`, `tokens_biblioteca`, `prompt_eval_duration`, `somente_cpu = true`, um único modelo residente.
- `avaliar.py` reproduz os números da 2-A para A0 (nada mudou ali) e imprime McNemar A1×A0 e A2×A0 por modelo.
- Gráficos e relatório saem do JSONL; nenhum número digitado.
- `pytest` da CobaiaAPI passa com o teste novo do bypass; `FAULT_MODE=type_drift FAULT_TARGET_FIELD=preco` no `.env` faz `preco` sair como texto sem tocar no endpoint admin.
