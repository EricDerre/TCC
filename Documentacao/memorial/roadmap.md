<!-- ! Alteração de IA - Revisar: roadmap do projeto em 28/09/2026 — onde cada fase está, o que ainda precisa rodar (comando, duração, o que fecha), o esqueleto das Fases 4 e 5 e uma tabela para o Eric encaixar os pontos dele por fase.
     ! Motivo: o Eric pediu "um roadmap de onde estamos e o que precisamos rodar" para arquitetar o novo plano; o plano complementar de 21/09 vive fora do git e as pendências dizem o que falta, mas nenhum documento junta estado por fase, corridas pendentes e o desenho das próximas fases num lugar só. Números de custo são as estimativas da análise decisória §10 e as medianas da bateria; nenhum número novo. -->
<!-- ! Alteração de IA - Revisar: na noite de 28/09/2026 a célula "Estado" da tabela §1 passou a começar com Concluída / Em andamento / Não iniciada, a tabela §2 ganhou a coluna "Estado" (feita / rodando / pendente / opcional / aguarda), a corrida dos inéditos foi registrada como lançada (20:13, 3B primeiro) e as referências passaram a apontar para as fichas de pendencias.md e para o painel do projeto (dashboard/painel-do-projeto.html).
     ! Motivo: o painel do projeto (ferramentas/gerar_dashboard.py, via ferramentas/painel_textos.py) lê estas duas tabelas para desenhar a faixa de fases e os cartões de corrida, e colore cada um pela primeira palavra do estado — sem a palavra fixa no começo da célula ele não tem como saber o que está feito, rodando ou pendente. -->
# Roadmap — 28/09/2026

Parte do [Memorial de Desenvolvimento](../Memorial%20de%20Desenvolvimento.md). Pendências e decisões em aberto em [pendencias.md](pendencias.md) (fichas 1–14 do bloco de 23/09); decisões numeradas em [decisoes.md](1-decisoes-e-historico/decisoes.md); painel do projeto (pendências, roadmap e resultados dos testes numa página só) em [`dashboard/painel-do-projeto.html`](../dashboard/painel-do-projeto.html) (gerado por `ferramentas/gerar_dashboard.py`).

## 1. Onde estamos, por fase

| Fase | O que é | Estado em 28/09/2026 |
|---|---|---|
| 1 — Ambiente e cobaias | Instalador único, CobaiaFront (PHP legado) e CobaiaAPI (FastAPI) com 7 modos de injeção de falha, banco de 90 casos | Concluída — dois casos do banco corrigidos em 28/09 (`efe-3`, `efe-10`, achado 4.36) |
| 2-A — Prompts sem documentação | 6 modelos × estratégias de prompt, máquina de desenvolvimento (Ryzen) | Concluída — relatório em `3-resultados-e-analises/fase-2a-relatorio-por-modelo.md` |
| 2-B — Biblioteca recuperada | 6 modelos × condições A0–A5 na máquina-alvo (i5) | Concluída (07–09/09) — definiu recuperação A2 e validação em código |
| 3 — Biblioteca gerida pelo modelo | 4 modelos × 3 épocas × 90 casos (13–15/09, 58h59) | Concluída e analisada — **decisão 52: `qwen2.5:7b` com L1**; relatório, comparação, análise decisória, achados 4.29–4.35, vereditos H1–H6 |
| 3-B — Testes complementares | Ponte de versão, troca cruzada, casos inéditos, sonda de correção | Em andamento — ponte feita (21/09); **casos inéditos rodados em 28/09 (20:13–23:15, 03h02, sem falhas; primeira leitura em §2.1)**; troca cruzada pronta para rodar (comando abaixo; ficha 4); sonda de detecção de correção rodada em 28/09 (§3) |
| 4 — Agente na tela | Interceptador Playwright (rede + árvore de acessibilidade), poda em código, cura de seletor, biblioteca em produção com ciclo de correção | Não iniciada — ferramental já decidido (decisão 55) e requisitos novos em §4 |
| 5 — Medição de valor | MTTR e Task Success contra linha de base manual, nas duas cobaias | Não iniciada — protocolo já escrito no projeto ABNT §3.4 |
| Documentação | Memorial (5 pastas), projeto de pesquisa ABNT, TCC final | Em andamento — Memorial em dia (decisões até 59, achados até 4.36, painel do projeto); ABNT com 11 modificações propostas em `4-projeto-de-pesquisa-abnt/correcoes-aplicadas.md` §5.1 (ficha 10); TCC final não começado |

Posição no cronograma do projeto ABNT (§5, sem datas): fim do **Mês 2** (ambiente e comparação de modelos), com o Mês 1 (revisão bibliográfica) ampliado e parte do Mês 6 (redação) adiantada pelo Memorial. Os Meses 3–5 são as Fases 4 e 5.

## 2. O que precisamos rodar (máquina), em ordem

| # | Corrida | Comando (em `Programacao/AgenteCore/experimentos`) | Inferências / tempo | Pré-requisito | O que fecha | Estado |
|---|---|---|---|---|---|---|
| 1 | **Troca cruzada** — L1 e L3 do `qwen2.5:7b` lidas pelos dois Coder nos 36 | `powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo cruzada -Saida fase3b_cruzada_qwen -Doador qwen2.5:7b -Versoes 1,3 -Modelos qwen2.5-coder:7b,qwen2.5-coder:3b` | 144 / ~2,5 h (uma noite; espera 6,5 GB de RAM livre) | nada | Limitação 7 (escritor × leitor); entra em `decisao_modelo.md` §6 por `--saidas-3b fase3b_ponte fase3b_cruzada_qwen`. Ressalva: `efe-3` (nos 36) mudou de texto em 28/09 — 1 caso não pareável byte a byte com a Fase 3 | pendente — uma noite com a máquina livre (ficha 4) |
| 2 | **Casos inéditos** — 36 casos novos, `qwen2.5-coder:3b` e `qwen2.5:7b` em L0, L1 e L3 | `powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo ineditos -Saida fase3b_ineditos -Versoes 0,1,3 -Modelos qwen2.5-coder:3b,qwen2.5:7b` | 216 / 03h02 medidos (3B 54 min, 7B 2h07) | Eric autorizou em 28/09 sem a conferência prévia dos 6 casos (ficha 12) | Limitação 2 (teste reutilizado): o ganho de L1 generaliza? Avaliação por `avaliar_fase3b.py --saida fase3b_ineditos` | feita em 28/09 (20:13–23:15; sem falhas; avaliada) — leitura em §2.1 |
| 3 | **Regeneração combinada** de `resumo_fase3.json` com a revisão das edições | `RESULTADOS_DIR=resultados_alvo python avaliar_fase3.py --saida fase3` | 1 min, sem modelo | "pode gravar" do Eric (ficha 1) | `revisao_humana` deixa de vir só das planilhas; ensaio já feito numa cópia (só esse arquivo muda) | aguarda decisão (ficha 1) |
| 4 | **Sonda de detecção de correção** (feita em 28/09) | `RESULTADOS_DIR=resultados_alvo python sonda_correcao.py --saida fase3b_correcao --modelo qwen2.5:7b --versao 1 --casos efe-3 efe-10` | 4 / ~10 min | casos corrigidos (feito) | Primeira leitura do requisito do ciclo de correção (§4.2); repetir depois de cada correção de código na Fase 4 | feita em 28/09 |
| 5 | (opcional) **A5 sobre L3** nos 36 — documentação própria e adesão cega | `powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo a5 -Saida fase3b_a5 -Modelos qwen2.5:7b,qwen2.5-coder:3b` | 72 / ~1,3 h | nada | Mais um argumento sobre H5; não muda a decisão | opcional — só se sobrar uma noite |
| 6 | **Integração da 3-B** (P6) — `decidir_modelo.py --saidas-3b …`, `gerar_tabelas_relatorio_fase3.py`, blocos do relatório §11/§12 e da análise §9/§10, handoff | — (scripts de análise, sem modelo) | 1 sessão, sem modelo | corridas 1 e 2 | Fecha o plano complementar de 21/09 | pendente — depois das corridas 1 e 2 |

Fora da máquina, na mesma ordem: aprovar (ou descartar) o servidor de memória do código e instalar o `pyright-lsp` (ficha 5); remover do Ollama os modelos que não voltam (ficha 3: Granite, phi4-mini e os três 1.5b agora; os dois Coder depois das corridas 1 e 2); `git add -f` dos dois logs (ficha 7); commit do working tree.

## 2.1 Casos inéditos — primeira leitura (28/09/2026, 23:15)

<!-- ! Alteração de IA - Revisar: seção nova com a primeira leitura da corrida 2 (casos inéditos), escrita ao fim da bateria em 28/09/2026.
     ! Motivo: o resultado muda uma pergunta aberta (qual versão da biblioteca levar para a Fase 4) e precisa estar no roadmap antes da integração formal, que só acontece depois da troca cruzada (corrida 6). Todos os números vêm de `resultados_alvo/fase3b_ineditos/resumo_fase3.json`, com o campo citado; nenhum foi digitado de cabeça. -->
Corrida 2 do §2: 216 diagnósticos, sem falhas, das 20:13 às 23:15; registro em `resultados_alvo/fase3b_ineditos/` (`resumo_fase3.json`, `avaliacao_fase3.json`, um JSONL por modelo e versão, `fase3b.log`). Os 36 casos inéditos entram todos na partição "avaliação" — nenhum passou por época de aprendizado de modelo nenhum. Origem dos números em `resumo_fase3.json`: acerto, intervalo de confiança e acurácia balanceada de `por_modelo_biblioteca_particao`; ganhos/perdas e p de `pareado_vs_L0` (McNemar exato de cada versão contra L0); hit@3 de `recuperacao`; segundos de `segundos_mediana`.

| Modelo | Biblioteca | Acerto (IC 95%) | Acurácia balanceada | Contra L0 (ganhos/perdas, p) | hit@3 | s/diagnóstico |
|---|---|---|---|---|---|---|
| `qwen2.5-coder:3b` | L0 | 58,3% (42,2–72,9) | 68,1% | — | 69,4% | 38,1 |
| `qwen2.5-coder:3b` | L1 | 58,3% (42,2–72,9) | 68,1% | 0/0, p = 1 | 69,4% | 22,3 |
| `qwen2.5-coder:3b` | L3 | 58,3% (42,2–72,9) | 68,1% | 0/0, p = 1 | 69,4% | 27,8 |
| `qwen2.5:7b` | L0 | 75,0% (58,9–86,2) | 81,2% | — | 69,4% | 73,0 |
| `qwen2.5:7b` | L1 | 72,2% (56,0–84,2) | 79,0% | 0/1, p = 1 | 66,7% | 75,5 |
| `qwen2.5:7b` | L3 | 80,6% (65,0–90,2) | 87,0% | 3/1, p = 0,625 | 63,9% | 66,0 |

Leitura:
- **O ganho da L1 medido nos 36 oficiais da Fase 3 não reaparece nos 36 inéditos.** Lá o `qwen2.5:7b` subiu 11,1 pontos de acerto de L0 para L1 (base da decisão 52); aqui, com L1, ele perde 1 caso e não ganha nenhum contra L0.
- **L3 fica 2 casos líquidos acima de L0** (3 ganhos, 1 perda; p = 0,625; Q de Cochran L0/L1/L3 = 3,5, p = 0,1738, campo `cochran_q`). É pouco para 36 casos: o efeito mínimo detectável do resumo oficial da Fase 3 para n = 36 é de 19,4 pontos (`efeito_minimo_detectavel`), então nada aqui é conclusivo — nem a favor, nem contra.
- **O 3B responde exatamente igual com L0, L1 e L3** (0 trocas de rótulo): as edições que ele mesmo aceitou nas três épocas não mudam nenhuma resposta em casos novos.
- **A recuperação por palavras acha o verbete certo entre os três primeiros em 69,4% dos inéditos com a biblioteca original** (contra 79% nos 90 oficiais, que ajudaram a calibrar a biblioteca) e cai um pouco com as bibliotecas escritas pelo 7B (66,7% com L1, 63,9% com L3): as notas novas concorrem com os verbetes originais na busca.
- **O que muda:** a limitação 2 da análise decisória ("teste reutilizado") passa a ter medida. A escolha de L1 se sustenta nos 36 oficiais, mas não é confirmada em casos nunca vistos; qual versão levar para a Fase 4 (L1 curada ou L3) volta a ser pergunta e entra na integração da 3-B (corrida 6), junto com a troca cruzada — é lá que `decidir_modelo.py --saidas-3b` recalcula a regra 36 com as saídas novas, e o relatório §11/§12 e a análise §9/§10 recebem o texto. Ressalva de medição: os tempos por diagnóstico saíram com a sessão do VS Code aberta (o 3B em L0 rodou durante a geração do painel) e valem como ordem de grandeza, não como custo comparável ao da Fase 3; o acerto não é afetado.

## 3. Sonda de detecção de correção (28/09/2026)

O que foi testado: os casos `efe-3` e `efe-10` tiveram o sintoma corrigido (achado 4.36) e foram apresentados de novo ao `qwen2.5:7b`, lendo uma cópia da própria biblioteca L1 (que contém a retificação e o verbete `interface-frontend` escritos a partir do `efe-10` antigo), numa época de aprendizado só com esses dois casos. Resultado (registro em `resultados_alvo/fase3b_correcao/`: `sonda.log`, `qwen2.5_7b/diagnosticos__L1.jsonl`, `qwen2.5_7b/propostas__E2.jsonl`, `bibliotecas/qwen2.5_7b/epoca-2`, hash 1202f1be9a75):

| Caso corrigido | Diagnóstico | O que o modelo propôs | Decisão do validador |
|---|---|---|---|
| `efe-3` (cartão sem foto) | `campo_ausente`, campo `imagem` — **correto** | Retificação em `contrato-produto` repetindo a sugestão da época 1 ("preco Decimal", formatação no front) e nota em `campo_ausente` idêntica à da época 1 | Ambas rejeitadas: `teto_notas_verbete` (858 > 800 caracteres) e `duplicada` |
| `efe-10` (tela com preço antigo, API já com o novo) | `dado_desatualizado` — **errado** (gabarito `estado_da_tela_divergente`, que estava no contexto) | A mesma retificação da época 1 sobre "cancelar depende do redirect" e um verbete novo genérico `atualizacao-da-interface` ("manter a interface atualizada com a API") | Retificação rejeitada (`teto_notas_verbete`, 908 > 800); verbete novo **aceito** (forma válida, conteúdo vazio) |

Leitura: com o prompt pré-registrado da Fase 3, o modelo não percebe que a documentação que ele mesmo escreveu ficou desatualizada — repete as edições antigas e só os tetos do validador impedem a biblioteca de acumular o mesmo texto de novo; nada foi registrado como "erro + solução sugerida + solução aplicada". A recuperação por palavras não trouxe as notas ligadas ao caso (`[E1 · efe-10 · …]`), e o prompt não pede ao modelo que compare o caso novo com o que a biblioteca afirma. Consequências para o desenho da Fase 4 estão em §4.2 (decisão 58). Observação: o `efe-10` corrigido é um caso mais difícil que o antigo — a distinção entre tela não redesenhada e dado desatualizado é exatamente o que ele testa.

## 4. Fase 4 — esqueleto do plano (para o Eric arquitetar)

### 4.1 O que a Fase 4 entrega (objetivos específicos 3 e 4 do projeto ABNT)
- **Interceptador Playwright**: captura das requisições e respostas da CobaiaAPI e da árvore de acessibilidade da página, com poda em código (decisão 55: poda da árvore, não do DOM bruto).
- **Diagnóstico em produção**: `qwen2.5:7b` com a biblioteca L1 curada, prompt congelado byte a byte, saída restrita por gramática (enum de causas), recuperação híbrida BM25 + embedding pequeno, cache exato só fora de corrida medida.
- **Cura de seletor**: candidatos gerados a partir da árvore de acessibilidade e verificados em código antes de reexecutar; a correção é aplicada na reexecução de verificação e apresentada ao desenvolvedor como sugestão (ABNT §2.1).

### 4.2 Requisito novo: ciclo de correção na biblioteca (Eric, 28/09/2026)
Quando um erro documentado pelo agente (na biblioteca, com solução sugerida) é corrigido no sistema — com a sugestão dele ou não —, o agente deve perceber a mudança e registrar na documentação que aquilo foi corrigido, **sem apagar o histórico**: o verbete passa a guardar o erro, a solução sugerida e a solução aplicada. O que isso pede ao harness da Fase 4 (arquivos novos; `evolucao_biblioteca.py` continua congelado para a Fase 3):
1. um campo de estado por verbete de defeito (`status: nao_corrigido | corrigido`) e uma operação nova de edição, "correção", que acrescenta as seções *solução sugerida* e *solução aplicada* com data, sem remover texto;
2. um gatilho: o caso reapresentado ou a inspeção do código mostra que o sintoma documentado não ocorre mais — a sonda de 28/09 mede se o modelo percebe isso sozinho com o prompt atual (§3);
3. recuperação por identificador: as notas do modelo já carregam o id do caso (`[E1 · efe-10 · …]`); ao corrigir um caso, o harness pode trazer ao contexto exatamente as notas ligadas a ele, em vez de depender da busca por palavras;
4. validação em código da correção (o trecho apontado existe; o status só avança; nada é removido) e o mesmo registro "o quê + motivo" das outras operações.

### 4.3 O que já está decidido para a Fase 4
Decisão 55 (mapa do levantamento das LLMs locais, §6.12.10 e §7.9): adotado, adiado e descartado, item a item; decisão 52 (modelo e biblioteca); fichas 2 (curadoria da cópia L1) e 11(f) (recuperador híbrido) de `pendencias.md`.

## 5. Fase 5 — o que já está escrito
Protocolo do projeto ABNT §3.4: MTTR (detecção → correção validada na reexecução) e Task Success (fluxo restaurado / cenários injetados), linha de base manual cronometrada, cerca de dez cenários com cinco repetições, banco restaurado entre execuções, navegador fixo pelo orquestrador, nas duas cobaias.

## 6. Documentação e entrega
1. Aplicar as 11 modificações do projeto ABNT que o Eric aprovar (`correcoes-aplicadas.md` §5.1; ficha 10) e resolver a autoria de MACIAK.
2. Remover as marcações de IA e regerar o PDF na entrega; conferir Faceli no exemplar.
3. TCC final: o Memorial é a matéria-prima (relatórios por fase, análise decisória, achados, referências); o painel do projeto serve às figuras e às tabelas.
4. Defesa.

## 7. Pontos do Eric a encaixar (28/09/2026)

Cada ponto novo entra numa linha desta tabela, na fase em que cabe; os já conhecidos estão listados.

| Ponto | Fase | Depende de | Esforço estimado |
|---|---|---|---|
| Curadoria da cópia L1 (30 edições restantes; 12 já marcadas erradas) | antes da 4 | ficha 2 | 1 sessão (IA) + conferência do Eric |
| Ciclo de correção na biblioteca (§4.2) | 4 | sonda de 28/09 (ficha 14) | desenho + implementação em arquivos novos |
| Recuperador híbrido BM25 + embedding pequeno com reordenação (decisão 55) | 4 | — | 1 sessão + medição no i5 |
| Saída restrita por gramática com enum de causas (decisão 55) | 4 | medir custo no i5 | 1 sessão |
| Fichamento formal das 7 referências (ficha 11a) | documentação | decisão do Eric | — |
| Validação em Linux do instalador (ficha 11b) | documentação | decisão do Eric | — |
| Ablação base × instruct (ficha 11d) | só se a banca pedir | — | — |
