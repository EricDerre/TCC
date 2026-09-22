<!-- ! Alteração de IA - Revisar: arquivo criado em 11/09/2026 como esqueleto pré-registrado do
     relatório da Fase 3 (biblioteca gerida pelo próprio modelo), com as seções do relatório da
     2-B, as hipóteses e o protocolo já escritos e os lugares dos números marcados com
     "(a preencher ... após a bateria)".
     ! Motivo: a bateria da Fase 3 leva ~60 h de CPU e decide o modelo final do TCC; escrever o
     protocolo e as hipóteses só depois de ver o resultado abriria espaço para ajustar a
     pergunta ao que saiu. Com o esqueleto pronto antes, preencher vira substituir marcação por
     número saído de `resumo_fase3.json` e `avaliacao_fase3.json`, e qualquer seção que ficar
     sem preencher fica visível. As seções 1, 2 e 11 já estão completas: dependem do desenho,
     não do resultado. -->
<!-- ! Alteração de IA - Revisar: em 12/09/2026 (revisão final): a nota de estado passou para
     12/09 (implementação concluída; piloto de 10 casos rodado; bateria por rodar); em §1 a
     linha "Máquina" nomeia a versão do Ollama (0.34.0, com as versões 0.33.2 da Verificação 0
     e 0.33.3 da 2-B) e a linha "Porta de entrada" diz 30 códigos em 26 checagens; §6 diz
     "30 códigos"; as quatro citações de `task-4-report.md`/`task-7-report.md` (§1 e §6/§9)
     dizem onde o arquivo fica e o que é reproduzível; §11 ganhou o item sobre a versão do
     Ollama. As hipóteses H1–H6 e o restante do pré-registro não mudaram.
     ! Motivo: (1) o Ollama atualizou sozinho de 0.33.3 para 0.34.0 em 12/09/2026, antes da
     bateria, e não foi revertido (máquina corporativa, atualização automática) — sem dizer
     isso aqui, o pareamento 2-B A2 × F3 L0 seria lido como só ruído de execução; (2)
     `CODIGOS_REJEICAO` tem 30 códigos, não 26 (26 é o número de checagens); (3)
     `.superpowers/` está fora do git (`.gitignore` l. 19) e o piloto de fumaça da T7 foi
     apagado e o parser mudou depois dele, então quem for reproduzir precisa do comando
     (`rodar_fase3.ps1 -Piloto`, `executar_fase3.py --so-projecao --modelos` com os 4 modelos), não do relatório. -->
<!-- ! Alteração de IA - Revisar: segunda passada de 12/09/2026 — (1) o comando da projeção de
     67,18 h, na tag acima e em §1 "Custo estimado", ganhou `--modelos` com os quatro modelos;
     (2) em §1 "Máquina" e em §11 a versão 0.33.2 deixou de ser atribuída à Verificação 0 desta
     máquina e passou a ser a do achado 4.21, medido no Ryzen em 03/09/2026.
     ! Motivo: (1) `python executar_fase3.py --so-projecao` sem `--modelos` não roda — o argparse
     de `executar_fase3.py` declara `--modelos` com `required=True` e encerra com "the following
     arguments are required: --modelos"; com os quatro modelos, a saída conferida em 12/09/2026
     termina em "total: 67.18 h". (2) O "0.33.2" entrou no commit 603c423 (03/09/2026), antes da
     decisão 25 (07/09) que fez do i5 a máquina-alvo: é a versão do Ryzen quando o 4.21 foi
     medido. Na máquina-alvo o `maquina.json` da 2-B registra "ollama version is 0.33.3" desde
     07/09/2026 09:18, e o `fase2b.log` mostra a Verificação 0 rodando às 09:29 do mesmo dia —
     nenhum artefato sustenta uma passagem 0.33.2 → 0.33.3 nesta máquina. -->
<!-- ! Alteração de IA - Revisar: em 22/09/2026 as seções §2–§9 e §12 foram preenchidas com os números da
     bateria de 13–15/09/2026; §1 recebeu início, RAM, inferências e horas reais; §11 ganhou a ponte de versão
     da 3-B, a revisão feita por IA e a ressalva do custo por versão. As tabelas entram como blocos
     `<!-- tabela:NOME -->` colados de `resultados_alvo/fase3/tabelas_relatorio.md` (gerado por
     `gerar_tabelas_relatorio_fase3.py`, que com `--check` acusa qualquer célula diferente de
     `resumo_fase3.json`). As hipóteses H1–H6 não mudaram uma letra; os vereditos entraram na coluna própria.
     ! Motivo: o esqueleto pré-registrado dizia "(a preencher após a bateria)" em nove lugares e o
     Memorial não podia fechar com o relatório da fase que decide o modelo vazio; colar tabelas à mão
     violaria a regra de nenhum número digitado (decisão 36), por isso o bloco marcado e conferido por script. -->
# Fase 3 — biblioteca gerida pelo próprio modelo: relatório por modelo

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). Leitura das fases anteriores em [fase-2a-relatorio-por-modelo.md](fase-2a-relatorio-por-modelo.md) e [fase-2b-relatorio-por-modelo.md](fase-2b-relatorio-por-modelo.md); a leitura das três juntas está em [comparacao-entre-fases.md](comparacao-entre-fases.md). Gráficos em `Programacao/AgenteCore/experimentos/resultados_alvo/graficos/12…17`; respostas cruas, propostas de edição caso a caso e diffs de cada época em `resultados_alvo/fase3/relatorio_fase3.html`. **Nenhum número deste arquivo foi digitado à mão**: todos saem de `avaliar_fase3.py` (`avaliacao_fase3.json`, `resumo_fase3.json`), de `comparar_fases.py` e de `decidir_modelo.py`, com o corte citado em cada seção; as tabelas são blocos `<!-- tabela:NOME -->` colados de `resultados_alvo/fase3/tabelas_relatorio.md` e conferidos por `gerar_tabelas_relatorio_fase3.py --check`.

<!-- ! Alteração de IA - Revisar: linha de estado nova (21/09/2026); a anterior fica como histórico, sem negrito.
     ! Motivo: a bateria rodou de 13/09 08:45 a 15/09 18:44 (`resultados_alvo/fase3/fase3.log`, `FIM … 58h59`, 0 falhas, Ollama 0.34.0) e o cabeçalho ainda dizia "bateria não executada"; as seções §2–§8 e §12 são preenchidas pelo plano complementar de 21/09. -->
> **Estado em 22/09/2026: bateria concluída (13–15/09/2026, 2.088 inferências, 0 falhas, Ollama 0.34.0); resultados em `resultados_alvo/fase3/` (commit b9f9ad9); §2–§9 e §12 preenchidas em 22/09/2026; ponte de versão da 3-B em §11; revisão das edições em primeira passada por IA (§7); decisão do modelo em §12 e em [analise-decisoria-modelo-final.md](analise-decisoria-modelo-final.md).**
>
> Estado anterior (21/09/2026): bateria concluída; relatório em preenchimento pelo plano complementar de 21/09/2026.
>
> Estado anterior (12/09/2026): pré-registrado; a bateria ainda não tinha rodado. A implementação do harness está concluída e revisada; o piloto de 10 casos do orquestrador (`rodar_fase3.ps1 -Piloto`) rodou em 12/09/2026 e os números dele entram em §9; a bateria completa (~60 h) aguarda a decisão do Eric. As seções 1, 2 e 11 valem como estão — descrevem o desenho. As demais estão marcadas com *(a preencher…)* e só recebem número depois da bateria.

## 1. O que foi medido

| Item | Valor |
|---|---|
| Máquina | **máquina-alvo** `TARGET_TSP030`: Intel i5-1235U (10 núcleos, 12 threads), 15,7 GB de RAM, sem GPU dedicada, Windows 11 Pro — a mesma da Fase 2-B. **Ollama 0.34.0**: o runtime atualizou sozinho de 0.33.3 (versão de toda a 2-B nesta máquina, inclusive a Verificação 0 do cache de prefixo registrada no `fase2b.log` em 07/09/2026; o achado 4.21 é a Verificação 0 medida no Ryzen em 03/09/2026, e essa rodou em 0.33.2) para 0.34.0 em 12/09/2026, antes da bateria da Fase 3, e não foi revertido — a máquina é corporativa e a atualização é automática. `maquina.json` grava a versão e, pela decisão 44, ela vai em todo registro e a corrida aborta se mudar no meio. Início **13/09/2026 08:46** (`maquina.json` → `inicio`), RAM livre 5,5 GB na largada e 7; 8,8; 10,4 e 10,3 GB no início de cada modelo (marcas do `fase3.log`); fim 15/09/2026 18:44 (`FIM … 58h59`); um relance por modelo (`relances`, 3 entradas), todos em 0.34.0 |
| Pergunta | o próprio modelo consegue melhorar a documentação que consulta, sem estragá-la? (decisão 13', adiada da 2-B) |
| Casos | os mesmos 90 da 2-B, com os 4 fixtures do achado 4.20 corrigidos (decisão 34) |
| Partição | **54 de aprendizado / 36 de avaliação**, 3 e 2 por célula classe×nível, sorteio pelo hash `sha256("fase3:" + id)` (decisão 31). Os 4 fixtures corrigidos caíram em aprendizado, logo **os 36 de avaliação são texto por texto os mesmos da 2-B** (origem: relatório da tarefa da partição, `task-4-report.md` — relatório interno em `.superpowers/`, fora do git, `.gitignore` l. 19; reproduzível por `resultados_alvo/fase3/particao.json` e por `evolucao_biblioteca.particionar`) |
| Modelos | **4** (decisão 32): `granite4.2:8b`, `qwen2.5:7b`, `qwen2.5-coder:7b`, `qwen2.5-coder:3b`. `phi4-mini:3.8b` e `qwen2.5-coder:1.5b` ficaram fora, descartados pela 2-B |
| Épocas | **3** de edição, mais a época 0 (cópia intocada da original). Versões da biblioteca: **L0, L1, L2, L3** |
| Condição | sempre **A2** — 3 verbetes recuperados (filtro por frontmatter + BM25 + sinais em código), a condição vencedora da 2-B |
| Prompt de diagnóstico | `linear_com_biblioteca`, **byte a byte igual ao da 2-B** — é a condição da comparação entre fases |
| Prompt de proposta | começa com o prompt do diagnóstico mais a resposta do modelo, literalmente, e acrescenta a causa correta, o verbete dedicado à causa e as regras de edição |
| Tetos de resposta | 600 tokens no diagnóstico, 700 na proposta; no máximo 2 propostas por caso |
| Tetos da biblioteca | 550 caracteres nas 4 seções originais de cada verbete (que nunca crescem), 800 caracteres e 6 notas de acréscimo por verbete, 6 verbetes novos por época, 1.800 tokens de contexto recuperado |
| Regra de edição | **só acréscimo**: nota, retificação apontando o trecho, ou verbete novo em `aprendidos/`; nada é apagado, esvaziado ou substituído (decisão 30). Conferido no fechamento de cada época |
| Porta de entrada | validação em código antes de qualquer edição entrar, com **30 códigos de rejeição**, em 26 checagens de ordem fixa (decisão 33; `CODIGOS_REJEICAO` em `evolucao_biblioteca.py`) |
| Inferências | **522 por modelo** (4 × 90 diagnósticos + 3 × 54 propostas), 2.088 no total — `n_diagnosticos` 1.440 e `n_propostas` 648 (`resumo_fase3.json` → `metadados`); `erros_infra` = 0 em todas as células; `contexto_estourou_n` = 0; `formato_valido_pct` abaixo de 100 só no `qwen2.5-coder:7b` com L1, L2 e L3 (97,8%, 98,9% e 96,7% nos 90); propostas cortadas no teto de 700 tokens (`n_respostas_truncadas`) só no `granite4.2:8b`: 9, 8 e 8 nas três épocas |
| Custo estimado | **~60 h de CPU** para os 4 modelos, estimativa do plano a partir dos ms/token medidos na 2-B; a projeção que o próprio executor imprime antes de começar dá **67,18 h** (saída registrada no relatório da tarefa do executor, `task-7-report.md`, relatório interno em `.superpowers/`, fora do git — `.gitignore` l. 19; a mesma projeção é reproduzível por `python executar_fase3.py --so-projecao --modelos granite4.2:8b qwen2.5:7b qwen2.5-coder:7b qwen2.5-coder:3b` — `--modelos` é obrigatório: sem ele o script encerra com "the following arguments are required: --modelos"; é o comando que `rodar_fase3.ps1` roda antes da corrida, e a saída conferida em 12/09/2026 termina em "total: 67.18 h"). O piloto de fumaça da implementação já mediu o `qwen2.5-coder:3b` (§9); o valor real: **58h59** no total (`FIM` do `fase3.log`, 13/09 08:45 → 15/09 18:44); por modelo, pelas marcas do log: `qwen2.5-coder:3b` 05h02, `qwen2.5:7b` 13h53, `qwen2.5-coder:7b` 12h06, `granite4.2:8b` 26h58 (§9) — 12% abaixo da projeção de 67,18 h |
| Estatística | IC 95% de Wilson; McNemar exato pareado contra L0, com Holm nas 3 comparações da mesma célula; Q de Cochran sobre L0..L3; acurácia balanceada (macro-recall por causa) como métrica primária da escolha do modelo (decisão 36) |

## 2. Hipóteses pré-registradas

Escritas antes de a bateria rodar (achado 4.29 e §4.4 do plano aprovado). Os vereditos foram dados em 22/09/2026, com os números de `resumo_fase3.json` (campo citado em cada um); o texto das hipóteses não mudou.

| # | Hipótese | Veredito |
|---|---|---|
| H1 | Nos 36 de avaliação, acerto com L3 > L0 nos modelos de 7–8B (McNemar exato, α = 0,05) | **Não confirmada.** Nos 36 (`pareado_vs_L0`, partição `avaliacao`, L3 vs L0): `qwen2.5:7b` +8,3 pp (b/c 3/0, p = 0,25), `qwen2.5-coder:7b` +2,8 pp (3/2, p = 1,0), `granite4.2:8b` 0,0 pp (0/0). Nenhum p < 0,05; o efeito mínimo detectável é 19,4 pp (§4) — falta resolução, não sinal: nos dois Qwen nenhum caso piorou de L0 para L3 |
| H2 | O ganho concentra-se nas classes em que a recuperação é fraca (tradução: hit@3 = 46,7%), via aumento do hit@3 da biblioteca do modelo | **Não.** O hit@3 da biblioteca do modelo não subiu (`recuperacao`, nos 90: 80,0 em L0 → 77,8 em L1 e 78,9 em L3 no `qwen2.5:7b`), e na classe de tradução o verbete de ouro seguiu no contexto em 46,7% dos casos (`por_modelo_biblioteca_classe` → `ouro_no_contexto_pct`; 40,0% em L1). Os 4 casos ganhos em L1 nos 36 são das classes 6, 2, 4 e 5 — não se concentram na tradução; o acerto de tradução do `qwen2.5:7b` só cresce em L2–L3 (46,7% → 60,0% nos 90), sem mudança na recuperação |
| H3 | Nos 54 de aprendizado o ganho é maior que nos 36; a diferença quantifica a memorização | **Não; no vencedor, invertida.** `qwen2.5:7b`: +11,1 pp nos 36 contra +1,8 nos 54 em L1; +8,3 contra +5,5 em L3. `qwen2.5-coder:7b`: 0,0 contra +5,6 em L1, +2,8 contra 0,0 em L3. `qwen2.5-coder:3b`: +2,8 contra 0,0 (L1) e +1,8 (L3). `granite4.2:8b`: 0,0 contra −1,9. `tentativas_de_decorar` = 0 em todas as épocas: a memorização que H3 queria quantificar não apareceu |
| H4 | A taxa de aceitação das propostas cresce com o porte; o 3B tem mais rejeições por formato | **Parcial.** A segunda metade vale: o 3B tem mais rejeições por formato (`bloco_malformado` em 91 de 151 rejeições, 60%). A primeira não: a aceitação não cresce com o porte — `qwen2.5-coder:3b` 10 de 161 propostas (6,2%), `qwen2.5-coder:7b` 39 de 162 (24,1%), `qwen2.5:7b` 61 de 264 (23,1%) e `granite4.2:8b`, o maior, **0 de 181**, barrado por `texto_longo` em 133 (achado 4.30) |
| H5 | Autoenvenenamento (casos certos em L(n) que viram errados em L(n+1), nos 36) fica abaixo de 10%; se superar o ganho, o modelo é vetado | **Sim.** Autoenvenenamento máximo nos 36 (`flips` → `autoenvenenamento_pct`): 5,6% (`qwen2.5:7b`, L1→L2), 2,8% nos dois Coder, 0,0% no Granite — todos abaixo do teto de 10%; nenhum modelo vetado (decisão 36; `decisao_modelo.md` §1) |
| H6 | A curva não é monótona: reportar o melhor L e o L3, nunca só o último | **Sim.** A curva não é monótona: `qwen2.5:7b` 81,2% → **91,7%** (L1) → 84,2% → 86,2% de acurácia balanceada nos 36; `qwen2.5-coder:7b` 80,0 / 80,0 / 80,0 / 84,2 nos 36 mas 75,8 / **78,9** / 77,8 / 75,4 nos 90; `granite4.2:8b` plano (biblioteca idêntica nas quatro versões); `qwen2.5-coder:3b` 68,8 / 70,4 / 71,2 / 71,2. O melhor L é L1 em três modelos nos 90 (`comparacao_fases.md`, coluna "F3 melhor") e reportar só L3 esconderia o pico (achado 4.34) |

## 3. Curva por versão da biblioteca

Acerto de causa raiz por modelo e por versão da biblioteca, separado pelas duas partições. A coluna dos 36 é a que responde se o modelo **aprendeu**; a dos 54 mede quanto ele **decorou** o que viu.

Origem: `resumo_fase3.json` → `por_modelo_biblioteca_particao` (`causa_correta_pct`, `acuracia_balanceada_pct`), `por_modelo_biblioteca_classe` e `por_modelo_biblioteca_nivel`; gráfico 12 `fase3-acerto-por-epoca` (um painel por modelo, linha cheia nos 36 e tracejada nos 54).

**Acerto de causa raiz** (`causa_correta_pct`):

<!-- tabela:curva_acerto -->
| Modelo | L0 (36) | L1 (36) | L2 (36) | L3 (36) | L0 (54) | L1 (54) | L2 (54) | L3 (54) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `granite4.2:8b` | 80,6% | 80,6% | 80,6% | 80,6% | 74,1% | 75,9% | 70,4% | 72,2% |
| `qwen2.5-coder:7b` | 75,0% | 75,0% | 75,0% | 77,8% | 68,5% | 74,1% | 72,2% | 68,5% |
| `qwen2.5:7b` | 77,8% | 88,9% | 83,3% | 86,1% | 66,7% | 68,5% | 68,5% | 72,2% |
| `qwen2.5-coder:3b` | 69,4% | 72,2% | 72,2% | 72,2% | 63,0% | 63,0% | 63,0% | 64,8% |
<!-- /tabela:curva_acerto -->

**Acurácia balanceada** (macro-recall por causa, `acuracia_balanceada_pct` — a métrica primária):

<!-- tabela:curva_balanceada -->
| Modelo | L0 (36) | L1 (36) | L2 (36) | L3 (36) | L0 (54) | L1 (54) | L2 (54) | L3 (54) | L0 (90) | L1 (90) | L2 (90) | L3 (90) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `granite4.2:8b` | 83,3% | 83,3% | 83,3% | 83,3% | 76,4% | 77,2% | 73,7% | 75,2% | 79,6% | 80,2% | 78,0% | 78,7% |
| `qwen2.5-coder:7b` | 80,0% | 80,0% | 80,0% | 84,2% | 73,7% | 82,1% | 74,4% | 69,9% | 75,8% | 78,9% | 77,8% | 75,4% |
| `qwen2.5:7b` | 81,2% | 91,7% | 84,2% | 86,2% | 74,1% | 79,3% | 74,3% | 76,4% | 75,7% | 83,0% | 78,1% | 80,7% |
| `qwen2.5-coder:3b` | 68,8% | 70,4% | 71,2% | 71,2% | 70,3% | 70,3% | 69,5% | 70,3% | 71,5% | 72,6% | 72,0% | 72,6% |
<!-- /tabela:curva_balanceada -->

Leitura. Nos 36, só o `qwen2.5:7b` sai do lugar: 77,8% → 88,9% de acerto em L1 (quatro casos ganhos, nenhum perdido — `efe-1`, `sin-14`, `tra-8` e `run-10`, este último um caso em que a resposta com L0 trazia o rótulo entre colchetes, `[limite_de_requisicoes]`, que o avaliador conta como errado), recuando para 83,3% em L2 (perde `sin-14` e `run-10`) e 86,1% em L3. O `granite4.2:8b` tem a mesma biblioteca nas quatro versões (0 edições aceitas, §6) e os mesmos 29 acertos nos 36 — a linha plana é a reprodução exata de uma condição repetida quatro vezes. O `qwen2.5-coder:7b` só muda em L3 (+2,8 pp, 3 ganhos e 2 perdas) e o `qwen2.5-coder:3b` ganha um caso em L1 (`tra-4`) e o mantém. Nos 54, os movimentos são menores e nos dois sentidos (H3, §2).

**Forma das respostas nos 36** — rótulo mais frequente e sua parcela (`rotulo_mais_frequente`, `parcela_rotulo_mais_frequente_pct`), rótulos distintos (`n_rotulos_distintos`), formato ok com conteúdo errado (`formato_ok_conteudo_errado_pct`), fora do conjunto (`fora_do_conjunto_pct`), citação de verbete (`citou_verbete_pct`), verbete de ouro entre os 3 recuperados (`ouro_no_contexto_pct`), contexto com nota do modelo (`contexto_com_nota_pct`) e verbete novo no contexto (`verbete_novo_no_contexto_pct`):

<!-- tabela:qualidade -->
| Modelo | L | Rótulo mais frequente (parcela) | Rótulos distintos | Formato ok / conteúdo errado | Fora do conjunto | Citou verbete | Ouro no contexto | Contexto com nota | Verbete novo no contexto |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `granite4.2:8b` | L0 | `localizador_quebrado` (11,1%) | 20 | 19,4% | 0,0% | 100,0% | 86,1% | 0,0% | 0,0% |
| `granite4.2:8b` | L1 | `localizador_quebrado` (11,1%) | 20 | 19,4% | 0,0% | 100,0% | 86,1% | 0,0% | 0,0% |
| `granite4.2:8b` | L2 | `campo_renomeado` (11,1%) | 20 | 19,4% | 0,0% | 100,0% | 86,1% | 0,0% | 0,0% |
| `granite4.2:8b` | L3 | `localizador_quebrado` (11,1%) | 20 | 19,4% | 0,0% | 100,0% | 86,1% | 0,0% | 0,0% |
| `qwen2.5-coder:7b` | L0 | `estrutura_aninhada_divergente` (11,1%) | 19 | 25,0% | 2,8% | 100,0% | 86,1% | 0,0% | 0,0% |
| `qwen2.5-coder:7b` | L1 | `estrutura_aninhada_divergente` (11,1%) | 19 | 25,0% | 2,8% | 100,0% | 86,1% | 72,2% | 0,0% |
| `qwen2.5-coder:7b` | L2 | `estrutura_aninhada_divergente` (13,9%) | 19 | 25,0% | 2,8% | 100,0% | 83,3% | 100,0% | 0,0% |
| `qwen2.5-coder:7b` | L3 | `estrutura_aninhada_divergente` (13,9%) | 19 | 22,2% | 0,0% | 100,0% | 86,1% | 100,0% | 0,0% |
| `qwen2.5:7b` | L0 | `codificacao_incorreta` (8,3%) | 20 | 22,2% | 2,8% | 100,0% | 86,1% | 0,0% | 0,0% |
| `qwen2.5:7b` | L1 | `localizador_quebrado` (11,1%) | 20 | 11,1% | 0,0% | 100,0% | 83,3% | 94,4% | 0,0% |
| `qwen2.5:7b` | L2 | `localizador_quebrado` (11,1%) | 21 | 16,7% | 2,8% | 100,0% | 83,3% | 94,4% | 0,0% |
| `qwen2.5:7b` | L3 | `campo_ausente` (8,3%) | 20 | 13,9% | 2,8% | 100,0% | 86,1% | 94,4% | 0,0% |
| `qwen2.5-coder:3b` | L0 | `campo_ausente` (19,4%) | 18 | 30,6% | 0,0% | 100,0% | 86,1% | 0,0% | 0,0% |
| `qwen2.5-coder:3b` | L1 | `campo_ausente` (19,4%) | 18 | 27,8% | 0,0% | 100,0% | 86,1% | 8,3% | 0,0% |
| `qwen2.5-coder:3b` | L2 | `campo_ausente` (16,7%) | 18 | 27,8% | 0,0% | 100,0% | 86,1% | 36,1% | 0,0% |
| `qwen2.5-coder:3b` | L3 | `campo_ausente` (16,7%) | 18 | 27,8% | 0,0% | 100,0% | 86,1% | 50,0% | 0,0% |
<!-- /tabela:qualidade -->

Nenhum modelo colapsa num rótulo (parcela máxima 19,4%, no 3B; 18 a 21 rótulos distintos em 23) e o rótulo inventado fica em 0,0–2,8% — os dois vetos que o mapa de decisões pedia (§6.10, linhas 19 e 25: REIF; SCHWARTZ, 2024; TAM et al., 2024) não disparam. Dois números explicam o resto: o verbete de ouro está no contexto em 83,3–86,1% dos 36 em todas as bibliotecas (a recuperação não muda, §5), e as notas do modelo chegam ao prompt em 94,4% dos casos do `qwen2.5:7b` desde L1 (72,2% → 100% no Coder 7B; 8,3% → 50,0% no 3B), mas **nenhum verbete novo entra no contexto em caso algum** (`verbete_novo_no_contexto_pct` = 0,0 em todas as células): os 9 verbetes criados pelo `qwen2.5:7b` nunca foram recuperados nos 36. O que muda a resposta, quando muda, são as notas coladas aos verbetes originais.

**Por classe de defeito** (nos 90; o resumo não desmembra a classe por partição):

<!-- tabela:por_classe -->
| Modelo | Classe (n) | L0 | L1 | L2 | L3 |
| --- | --- | --- | --- | --- | --- |
| `granite4.2:8b` | 1 lexica (15) | 86,7% | 86,7% | 86,7% | 86,7% |
| `granite4.2:8b` | 2 sintatica (15) | 93,3% | 93,3% | 86,7% | 93,3% |
| `granite4.2:8b` | 3 semantica (15) | 73,3% | 73,3% | 73,3% | 73,3% |
| `granite4.2:8b` | 4 traducao (15) | 33,3% | 33,3% | 26,7% | 26,7% |
| `granite4.2:8b` | 5 runtime (15) | 93,3% | 93,3% | 93,3% | 93,3% |
| `granite4.2:8b` | 6 efeito (15) | 80,0% | 86,7% | 80,0% | 80,0% |
| `qwen2.5-coder:7b` | 1 lexica (15) | 93,3% | 93,3% | 93,3% | 86,7% |
| `qwen2.5-coder:7b` | 2 sintatica (15) | 80,0% | 80,0% | 73,3% | 66,7% |
| `qwen2.5-coder:7b` | 3 semantica (15) | 60,0% | 66,7% | 73,3% | 73,3% |
| `qwen2.5-coder:7b` | 4 traducao (15) | 26,7% | 40,0% | 33,3% | 33,3% |
| `qwen2.5-coder:7b` | 5 runtime (15) | 93,3% | 93,3% | 93,3% | 86,7% |
| `qwen2.5-coder:7b` | 6 efeito (15) | 73,3% | 73,3% | 73,3% | 86,7% |
| `qwen2.5:7b` | 1 lexica (15) | 86,7% | 86,7% | 80,0% | 86,7% |
| `qwen2.5:7b` | 2 sintatica (15) | 73,3% | 80,0% | 73,3% | 80,0% |
| `qwen2.5:7b` | 3 semantica (15) | 80,0% | 80,0% | 86,7% | 86,7% |
| `qwen2.5:7b` | 4 traducao (15) | 46,7% | 46,7% | 53,3% | 60,0% |
| `qwen2.5:7b` | 5 runtime (15) | 80,0% | 100,0% | 86,7% | 86,7% |
| `qwen2.5:7b` | 6 efeito (15) | 60,0% | 66,7% | 66,7% | 66,7% |
| `qwen2.5-coder:3b` | 1 lexica (15) | 73,3% | 73,3% | 86,7% | 80,0% |
| `qwen2.5-coder:3b` | 2 sintatica (15) | 80,0% | 80,0% | 80,0% | 80,0% |
| `qwen2.5-coder:3b` | 3 semantica (15) | 53,3% | 53,3% | 60,0% | 66,7% |
| `qwen2.5-coder:3b` | 4 traducao (15) | 40,0% | 46,7% | 40,0% | 40,0% |
| `qwen2.5-coder:3b` | 5 runtime (15) | 93,3% | 93,3% | 86,7% | 86,7% |
| `qwen2.5-coder:3b` | 6 efeito (15) | 53,3% | 53,3% | 46,7% | 53,3% |
<!-- /tabela:por_classe -->

**Por nível de dificuldade** (nos 90):

<!-- tabela:por_nivel -->
| Modelo | Nível (n) | L0 | L1 | L2 | L3 |
| --- | --- | --- | --- | --- | --- |
| `granite4.2:8b` | 1 facil (30) | 73,3% | 73,3% | 73,3% | 73,3% |
| `granite4.2:8b` | 2 medio (30) | 76,7% | 76,7% | 76,7% | 76,7% |
| `granite4.2:8b` | 3 dificil (30) | 80,0% | 83,3% | 73,3% | 76,7% |
| `qwen2.5-coder:7b` | 1 facil (30) | 66,7% | 63,3% | 73,3% | 80,0% |
| `qwen2.5-coder:7b` | 2 medio (30) | 76,7% | 80,0% | 76,7% | 73,3% |
| `qwen2.5-coder:7b` | 3 dificil (30) | 70,0% | 80,0% | 70,0% | 63,3% |
| `qwen2.5:7b` | 1 facil (30) | 66,7% | 76,7% | 80,0% | 80,0% |
| `qwen2.5:7b` | 2 medio (30) | 73,3% | 76,7% | 73,3% | 80,0% |
| `qwen2.5:7b` | 3 dificil (30) | 73,3% | 76,7% | 70,0% | 73,3% |
| `qwen2.5-coder:3b` | 1 facil (30) | 66,7% | 66,7% | 63,3% | 66,7% |
| `qwen2.5-coder:3b` | 2 medio (30) | 63,3% | 63,3% | 70,0% | 70,0% |
| `qwen2.5-coder:3b` | 3 dificil (30) | 66,7% | 70,0% | 66,7% | 66,7% |
<!-- /tabela:por_nivel -->

A tradução (classe 4) continua a classe difícil de todos: 26,7–46,7% em L0 contra 53–93% nas outras, com o verbete de ouro no contexto em 46,7% dos casos (4.23). É nela que o `qwen2.5:7b` mais cresce ao longo das épocas (46,7% → 60,0% em L3) e o `qwen2.5-coder:7b` em L1 (26,7% → 40,0%), sem que a recuperação da classe tenha subido — o ganho veio com o verbete de ouro ausente do contexto, o que aponta para as notas gravadas nos verbetes vizinhos (contrato, entidade) e não para o verbete da causa (H2, §2). Por nível, o `qwen2.5:7b` ganha mais nos casos fáceis (66,7% → 80,0%), o que é coerente com notas que reforçam sinais já explícitos.

## 4. Pareado e Cochran

Cada versão da biblioteca contra L0, no mesmo modelo e na mesma partição (mesmos casos, mesmo prompt, mesma máquina — o pareamento por caso é exato):

Origem: `resumo_fase3.json` → `pareado_vs_L0` (`n_pares`, `acerto_L0_pct`, `acerto_pct`, `delta_pp`, `b`, `c`, `p_mcnemar`, `p_holm`, `g_cohen`) e `cochran_q`:

<!-- tabela:pareado -->
| Modelo | Partição (n) | L1 vs L0 | L2 vs L0 | L3 vs L0 | Q de Cochran (L0..L3) |
| --- | --- | --- | --- | --- | --- |
| `granite4.2:8b` | avaliacao (36) | 80,6%→80,6% (Δ 0,0 pp; b/c 0/0; p 1,0000; Holm 1,0000; g —) | 80,6%→80,6% (Δ 0,0 pp; b/c 0/0; p 1,0000; Holm 1,0000; g —) | 80,6%→80,6% (Δ 0,0 pp; b/c 0/0; p 1,0000; Holm 1,0000; g —) | Q 0,0, gl 3, p 1,0000 |
| `granite4.2:8b` | aprendizado (54) | 74,1%→75,9% (Δ 1,8 pp; b/c 1/0; p 1,0000; Holm 1,0000; g 0,5) | 74,1%→70,4% (Δ -3,7 pp; b/c 0/2; p 0,5000; Holm 1,0000; g -0,5) | 74,1%→72,2% (Δ -1,9 pp; b/c 0/1; p 1,0000; Holm 1,0000; g -0,5) | Q 6,0, gl 3, p 0,1116 |
| `granite4.2:8b` | todos (90) | 76,7%→77,8% (Δ 1,1 pp; b/c 1/0; p 1,0000; Holm 1,0000; g 0,5) | 76,7%→74,4% (Δ -2,3 pp; b/c 0/2; p 0,5000; Holm 1,0000; g -0,5) | 76,7%→75,6% (Δ -1,1 pp; b/c 0/1; p 1,0000; Holm 1,0000; g -0,5) | Q 6,0, gl 3, p 0,1116 |
| `qwen2.5-coder:7b` | avaliacao (36) | 75,0%→75,0% (Δ 0,0 pp; b/c 0/0; p 1,0000; Holm 1,0000; g —) | 75,0%→75,0% (Δ 0,0 pp; b/c 1/1; p 1,0000; Holm 1,0000; g 0,0) | 75,0%→77,8% (Δ 2,8 pp; b/c 3/2; p 1,0000; Holm 1,0000; g 0,1) | Q 0,5, gl 3, p 0,9124 |
| `qwen2.5-coder:7b` | aprendizado (54) | 68,5%→74,1% (Δ 5,6 pp; b/c 4/1; p 0,3750; Holm 1,0000; g 0,3) | 68,5%→72,2% (Δ 3,7 pp; b/c 4/2; p 0,6875; Holm 1,0000; g 0,2) | 68,5%→68,5% (Δ 0,0 pp; b/c 6/6; p 1,0000; Holm 1,0000; g 0,0) | Q 1,6, gl 3, p 0,6621 |
| `qwen2.5-coder:7b` | todos (90) | 71,1%→74,4% (Δ 3,3 pp; b/c 4/1; p 0,3750; Holm 1,0000; g 0,3) | 71,1%→73,3% (Δ 2,2 pp; b/c 5/3; p 0,7266; Holm 1,0000; g 0,1) | 71,1%→72,2% (Δ 1,1 pp; b/c 9/8; p 1,0000; Holm 1,0000; g 0,0) | Q 0,9, gl 3, p 0,8297 |
| `qwen2.5:7b` | avaliacao (36) | 77,8%→88,9% (Δ 11,1 pp; b/c 4/0; p 0,1250; Holm 0,3750; g 0,5) | 77,8%→83,3% (Δ 5,5 pp; b/c 2/0; p 0,5000; Holm 0,5000; g 0,5) | 77,8%→86,1% (Δ 8,3 pp; b/c 3/0; p 0,2500; Holm 0,5000; g 0,5) | Q 5,5, gl 3, p 0,1371 |
| `qwen2.5:7b` | aprendizado (54) | 66,7%→68,5% (Δ 1,8 pp; b/c 3/2; p 1,0000; Holm 1,0000; g 0,1) | 66,7%→68,5% (Δ 1,8 pp; b/c 4/3; p 1,0000; Holm 1,0000; g 0,1) | 66,7%→72,2% (Δ 5,5 pp; b/c 5/2; p 0,4531; Holm 1,0000; g 0,2) | Q 1,7, gl 3, p 0,6309 |
| `qwen2.5:7b` | todos (90) | 71,1%→76,7% (Δ 5,6 pp; b/c 7/2; p 0,1797; Holm 0,3594; g 0,3) | 71,1%→74,4% (Δ 3,3 pp; b/c 6/3; p 0,5078; Holm 0,5078; g 0,2) | 71,1%→77,8% (Δ 6,7 pp; b/c 8/2; p 0,1094; Holm 0,3282; g 0,3) | Q 4,8, gl 3, p 0,1834 |
| `qwen2.5-coder:3b` | avaliacao (36) | 69,4%→72,2% (Δ 2,8 pp; b/c 1/0; p 1,0000; Holm 1,0000; g 0,5) | 69,4%→72,2% (Δ 2,8 pp; b/c 2/1; p 1,0000; Holm 1,0000; g 0,2) | 69,4%→72,2% (Δ 2,8 pp; b/c 1/0; p 1,0000; Holm 1,0000; g 0,5) | Q 0,8, gl 3, p 0,8451 |
| `qwen2.5-coder:3b` | aprendizado (54) | 63,0%→63,0% (Δ 0,0 pp; b/c 0/0; p 1,0000; Holm 1,0000; g —) | 63,0%→63,0% (Δ 0,0 pp; b/c 2/2; p 1,0000; Holm 1,0000; g 0,0) | 63,0%→64,8% (Δ 1,8 pp; b/c 2/1; p 1,0000; Holm 1,0000; g 0,2) | Q 0,5, gl 3, p 0,9124 |
| `qwen2.5-coder:3b` | todos (90) | 65,6%→66,7% (Δ 1,1 pp; b/c 1/0; p 1,0000; Holm 1,0000; g 0,5) | 65,6%→66,7% (Δ 1,1 pp; b/c 4/3; p 1,0000; Holm 1,0000; g 0,1) | 65,6%→67,8% (Δ 2,2 pp; b/c 3/1; p 0,6250; Holm 1,0000; g 0,2) | Q 0,9, gl 3, p 0,8358 |
<!-- /tabela:pareado -->

Leitura. **Nenhuma das 36 comparações pareadas tem p < 0,05, e nenhum Q de Cochran rejeita a igualdade das quatro versões** (menor p = 0,1094, `qwen2.5:7b` L3 vs L0 nos 90; Cochran mínimo p = 0,1116, Granite nos 54, puxado por três perdas em L2). A maior diferença observada é +11,1 pp (`qwen2.5:7b`, L1 nos 36, b/c 4/0, p = 0,125, g = 0,5) — abaixo dos 19,4 pp que o desenho consegue apontar com n = 36 (tabela do efeito mínimo abaixo). Lido com o mapa de decisões (§6.10, linhas 5 a 7): é falta de resolução, não ausência de efeito; e a direção é consistente — nos dois Qwen de 7B, entre L0 e qualquer L nos 36, os casos que mudaram foram 9 ganhos contra 0 perdas no `qwen2.5:7b` e 4 contra 3 no Coder 7B. A correção de Holm por célula (3 comparações) só reforça o quadro.

<!-- ! Alteração de IA - Revisar: em 12/09/2026 (item M14 da revisão final) a frase sobre o "efeito
     mínimo detectável" deixou de falar em "poder 0,8" e passou a dizer o que
     `avaliar_fase3.efeito_minimo_detectavel` calcula de fato. -->
<!-- ! Motivo: o plano (§8.2) e este esqueleto prometiam um efeito mínimo detectável com "poder 0,8",
     mas o script não faz cálculo de poder (isso exigiria supor a distribuição das discordâncias):
     ele procura, para cada n, o menor b acima de d/2 com `mcnemar_exato(b, d − b) < 0,05`, supondo
     d = round(0,2·n) pares discordantes, e grava `{n, discordantes, b_min, delta_pp}` em
     `resumo_fase3.json` → `efeito_minimo_detectavel`. Deixar "poder 0,8" aqui faria o leitor
     procurar um número que o arquivo não contém; o desvio está no anexo "Desvios do plano" de
     `claude-memoria/plano-aprovado-fase-3.md`. -->
**Flips entre versões consecutivas** — ✓→✗ é o autoenvenenamento da H5, ✗→✓ é o ganho: tabela abaixo (`flips`; por classe em `flips_por_classe` do `resumo_fase3.json`). Junto vai a **menor diferença significativa** que o desenho consegue apontar com n = 36, 54 e 90 (McNemar exato, α = 0,05, supondo 20 % de pares discordantes, `d = round(0,2·n)`; calculada por `avaliar_fase3.efeito_minimo_detectavel` e gravada em `resumo_fase3.json` → `efeito_minimo_detectavel`) — não é um cálculo de poder, ao contrário do que o plano §8.2 dizia ("poder 0,8"; ver o anexo "Desvios do plano" em `claude-memoria/plano-aprovado-fase-3.md`) —, para separar "não houve efeito" de "a amostra não alcança".

<!-- tabela:flips -->
| Modelo | Partição (n) | L0→L1: ✓→✗ / ✗→✓ (autoenv.) | L1→L2: ✓→✗ / ✗→✓ (autoenv.) | L2→L3: ✓→✗ / ✗→✓ (autoenv.) |
| --- | --- | --- | --- | --- |
| `granite4.2:8b` | avaliacao (36) | 0 / 0 (0,0%) | 0 / 0 (0,0%) | 0 / 0 (0,0%) |
| `granite4.2:8b` | aprendizado (54) | 0 / 1 (0,0%) | 3 / 0 (5,6%) | 0 / 1 (0,0%) |
| `qwen2.5-coder:7b` | avaliacao (36) | 0 / 0 (0,0%) | 1 / 1 (2,8%) | 1 / 2 (2,8%) |
| `qwen2.5-coder:7b` | aprendizado (54) | 1 / 4 (1,9%) | 4 / 3 (7,4%) | 5 / 3 (9,3%) |
| `qwen2.5:7b` | avaliacao (36) | 0 / 4 (0,0%) | 2 / 0 (5,6%) | 1 / 2 (2,8%) |
| `qwen2.5:7b` | aprendizado (54) | 2 / 3 (3,7%) | 3 / 3 (5,6%) | 0 / 2 (0,0%) |
| `qwen2.5-coder:3b` | avaliacao (36) | 0 / 1 (0,0%) | 1 / 1 (2,8%) | 1 / 1 (2,8%) |
| `qwen2.5-coder:3b` | aprendizado (54) | 0 / 0 (0,0%) | 2 / 2 (3,7%) | 1 / 2 (1,9%) |
<!-- /tabela:flips -->

O autoenvenenamento máximo nos 36 é 5,6% (`qwen2.5:7b`, L1→L2: `sin-14` e `run-10`, os dois casos ganhos em L1 que L2 devolve) — abaixo do teto de 10% da H5 em todos os modelos; nos 54 o pico é 9,3% (`qwen2.5-coder:7b`, L2→L3), ainda sob o teto, mas o número que mais se aproximou dele.

**Menor diferença que o McNemar exato aponta** (`efeito_minimo_detectavel`):

<!-- tabela:mde -->
| n | Pares discordantes supostos | b mínimo (p < 0,05) | Δ mínimo (pp) |
| --- | --- | --- | --- |
| 36 | 7 | 7 | 19,4 |
| 54 | 11 | 10 | 16,7 |
| 90 | 18 | 14 | 11,1 |
<!-- /tabela:mde -->

## 5. Recuperação por biblioteca

A 2-B tinha um hit@3 único, de 78,9%, comum aos seis modelos, porque a biblioteca era a mesma e o recuperador é determinístico (4.23). Na Fase 3 cada modelo tem a sua biblioteca, e o hit@k passa a ser resultado, não constante.

Origem: `resumo_fase3.json` → `recuperacao` (por modelo × L: `hit@1`, `hit@3`, `hit@5`, `mrr` nos 90 e nos 36; `n_verbetes`, `n_verbetes_novos`, `tokens_estimados`, `ouro_deslocado_por_novo`, `ouro_recuperavel_apos_edicao`); gráfico 13 `fase3-recuperacao-por-epoca`.

<!-- tabela:recuperacao -->
| Modelo | L | Verbetes (novos) | Tokens est. | hit@1 / hit@3 / hit@5 / MRR (90) | hit@1 / hit@3 / hit@5 / MRR (36) | Ouro deslocado por novo | Ouro recuperável após edição |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `granite4.2:8b` | L0 | 36 (0) | 6582 | 38,9 / 80,0 / 91,1 / 0,596 | 38,9 / 86,1 / 94,4 / 0,621 | 0 | — |
| `granite4.2:8b` | L1 | 36 (0) | 6582 | 38,9 / 80,0 / 91,1 / 0,596 | 38,9 / 86,1 / 94,4 / 0,621 | 0 | 0 |
| `granite4.2:8b` | L2 | 36 (0) | 6582 | 38,9 / 80,0 / 91,1 / 0,596 | 38,9 / 86,1 / 94,4 / 0,621 | 0 | 0 |
| `granite4.2:8b` | L3 | 36 (0) | 6582 | 38,9 / 80,0 / 91,1 / 0,596 | 38,9 / 86,1 / 94,4 / 0,621 | 0 | 0 |
| `qwen2.5-coder:7b` | L0 | 36 (0) | 6582 | 38,9 / 80,0 / 91,1 / 0,596 | 38,9 / 86,1 / 94,4 / 0,621 | 0 | — |
| `qwen2.5-coder:7b` | L1 | 36 (0) | 7977 | 37,8 / 80,0 / 90,0 / 0,587 | 38,9 / 86,1 / 91,7 / 0,616 | 0 | 0 |
| `qwen2.5-coder:7b` | L2 | 36 (0) | 8369 | 36,7 / 77,8 / 90,0 / 0,581 | 36,1 / 83,3 / 91,7 / 0,600 | 0 | 1 |
| `qwen2.5-coder:7b` | L3 | 36 (0) | 8765 | 37,8 / 78,9 / 90,0 / 0,589 | 36,1 / 86,1 / 91,7 / 0,603 | 0 | 0 |
| `qwen2.5:7b` | L0 | 36 (0) | 6582 | 38,9 / 80,0 / 91,1 / 0,596 | 38,9 / 86,1 / 94,4 / 0,621 | 0 | — |
| `qwen2.5:7b` | L1 | 42 (6) | 9820 | 36,7 / 77,8 / 92,2 / 0,580 | 38,9 / 83,3 / 94,4 / 0,609 | 0 | 1 |
| `qwen2.5:7b` | L2 | 43 (7) | 10806 | 36,7 / 78,9 / 90,0 / 0,583 | 38,9 / 83,3 / 91,7 / 0,607 | 0 | 0 |
| `qwen2.5:7b` | L3 | 45 (9) | 11377 | 36,7 / 78,9 / 88,9 / 0,579 | 38,9 / 86,1 / 88,9 / 0,604 | 0 | 0 |
| `qwen2.5-coder:3b` | L0 | 36 (0) | 6582 | 38,9 / 80,0 / 91,1 / 0,596 | 38,9 / 86,1 / 94,4 / 0,621 | 0 | — |
| `qwen2.5-coder:3b` | L1 | 36 (0) | 6831 | 38,9 / 80,0 / 92,2 / 0,595 | 38,9 / 86,1 / 94,4 / 0,621 | 0 | 0 |
| `qwen2.5-coder:3b` | L2 | 36 (0) | 7037 | 37,8 / 80,0 / 92,2 / 0,591 | 36,1 / 86,1 / 94,4 / 0,607 | 0 | 0 |
| `qwen2.5-coder:3b` | L3 | 37 (1) | 7236 | 37,8 / 81,1 / 93,3 / 0,591 | 36,1 / 86,1 / 94,4 / 0,609 | 0 | 0 |
<!-- /tabela:recuperacao -->

Leitura. A recuperação **não melhorou com a edição**: o hit@3 nos 90 vai de 80,0 (L0, igual para todos) a 77,8–78,9 no `qwen2.5:7b` e 77,8–80,0 no Coder 7B, e o MRR cai de 0,596 para 0,579–0,589 exatamente em quem mais editou — o efeito previsto pela dependência do IDF do BM25 em N e df (ROBERTSON; ZARAGOZA, 2009; mapa §6.10, linha 22): cada nota acrescentada muda os escores de todos os termos. `ouro_deslocado_por_novo` = 0 em todas as células, e `ouro_recuperavel_apos_edicao` chega a 1 (uma edição do `qwen2.5:7b` em E1 e uma do Coder 7B em E2 tornaram o verbete de ouro recuperável para o caso que as originou). O mecanismo da H2 (ganho via hit@3) fica descartado: o ganho do `qwen2.5:7b` em L1 aconteceu com recuperação um pouco pior, não melhor.

Duas medidas específicas desta fase, calculadas junto: **`ouro_deslocado_por_novo`** — casos em que um verbete criado pelo modelo entrou no top-3 e empurrou o verbete de ouro para fora — e as **edições que tornaram o verbete de ouro recuperável no top-3 para o caso que as originou**. O verbete de ouro de cada causa não muda entre L0 e L3 (só verbetes de `tipo: erro` são de ouro, e esses nunca são criados pelo modelo), o que mantém o hit@k comparável entre as quatro versões.

## 6. Documentação produzida

O que cada modelo escreveu, por época: propostas geradas, aceitas pela validação em código, motivos de rejeição, notas e retificações aplicadas, verbetes novos, caracteres e tokens acrescentados, e o crescimento da biblioteca.

Origem: `resumo_fase3.json` → `documentacao` (por modelo × época: `n_propostas`, `n_aceitas`, `por_operacao`, `n_nenhuma`, `n_fim_ausente`, `n_respostas_truncadas`, `tokens_md_estimados_acrescentados`, `biblioteca`, `quando_errou`, `quando_acertou`, `motivos_rejeicao`); gráficos 14 `fase3-propostas-por-motivo` e 15 `fase3-crescimento-da-biblioteca`.

<!-- tabela:documentacao -->
| Modelo | Época | Propostas | Aceitas | % | Notas | Retificações | Verbetes novos | NENHUMA | Sem FIM | Cortadas no teto | Tokens acrescentados (est.) | Biblioteca ao fechar (verbetes / tokens est.) | Aceitas quando errou / quando acertou |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `granite4.2:8b` | E1 | 58 | 0 | 0,0% | 0 | 0 | 0 | 1 | 17 | 9 | 0 | 36 / 6582 | 0 de 18 / 0 de 40 |
| `granite4.2:8b` | E2 | 62 | 0 | 0,0% | 0 | 0 | 0 | 0 | 16 | 8 | 0 | 36 / 6582 | 0 de 20 / 0 de 42 |
| `granite4.2:8b` | E3 | 61 | 0 | 0,0% | 0 | 0 | 0 | 0 | 17 | 8 | 0 | 36 / 6582 | 0 de 22 / 0 de 39 |
| `qwen2.5-coder:3b` | E1 | 54 | 4 | 7,4% | 0 | 4 | 0 | 0 | 12 | 0 | 741 | 36 / 6831 | 1 de 20 / 3 de 34 |
| `qwen2.5-coder:3b` | E2 | 54 | 3 | 5,6% | 0 | 3 | 0 | 0 | 8 | 0 | 590 | 36 / 7037 | 1 de 20 / 2 de 34 |
| `qwen2.5-coder:3b` | E3 | 53 | 3 | 5,7% | 0 | 2 | 1 | 1 | 8 | 0 | 745 | 37 / 7236 | 2 de 19 / 1 de 34 |
| `qwen2.5-coder:7b` | E1 | 54 | 25 | 46,3% | 14 | 11 | 0 | 0 | 54 | 0 | 4760 | 36 / 7977 | 6 de 17 / 19 de 37 |
| `qwen2.5-coder:7b` | E2 | 54 | 7 | 13,0% | 4 | 3 | 0 | 0 | 54 | 0 | 1373 | 36 / 8369 | 2 de 14 / 5 de 40 |
| `qwen2.5-coder:7b` | E3 | 54 | 7 | 13,0% | 7 | 0 | 0 | 0 | 54 | 0 | 1381 | 36 / 8765 | 1 de 15 / 6 de 39 |
| `qwen2.5:7b` | E1 | 87 | 40 | 46,0% | 12 | 22 | 6 | 0 | 87 | 0 | 8639 | 42 / 9820 | 14 de 29 / 26 de 58 |
| `qwen2.5:7b` | E2 | 86 | 12 | 14,0% | 6 | 5 | 1 | 1 | 84 | 0 | 2643 | 43 / 10806 | 3 de 28 / 9 de 58 |
| `qwen2.5:7b` | E3 | 91 | 9 | 9,9% | 6 | 1 | 2 | 0 | 89 | 0 | 1787 | 45 / 11377 | 5 de 30 / 4 de 61 |
<!-- /tabela:documentacao -->

**Histograma dos códigos de rejeição** (`motivos_rejeicao`, somado nas três épocas; só os códigos com ocorrência, de 30 possíveis):

<!-- tabela:rejeicoes -->
| Código de rejeição | `granite4.2:8b` | `qwen2.5-coder:7b` | `qwen2.5:7b` | `qwen2.5-coder:3b` | Total |
| --- | --- | --- | --- | --- | --- |
| `texto_longo` | 133 | 0 | 1 | 0 | 134 |
| `bloco_malformado` | 26 | 0 | 10 | 91 | 127 |
| `duplicada` | 0 | 33 | 53 | 3 | 89 |
| `palavra_chave_invalida` | 0 | 25 | 44 | 5 | 74 |
| `arquivo_inexistente` | 12 | 10 | 13 | 17 | 52 |
| `trecho_nao_encontrado` | 0 | 11 | 18 | 11 | 40 |
| `teto_notas_verbete` | 0 | 2 | 33 | 0 | 35 |
| `id_repetido` | 5 | 0 | 23 | 5 | 33 |
| `motivo_longo` | 0 | 26 | 2 | 3 | 31 |
| `texto_curto` | 0 | 1 | 2 | 14 | 17 |
| `retificacao_sem_trecho` | 0 | 15 | 0 | 1 | 16 |
| `vocabulario` | 2 | 0 | 3 | 0 | 5 |
| `operacao_invalida` | 3 | 0 | 0 | 0 | 3 |
| `alvo_inexistente` | 0 | 0 | 1 | 0 | 1 |
| `alvo_nao_visto` | 0 | 0 | 0 | 1 | 1 |
| **Total de rejeições** | 181 | 123 | 203 | 151 | 658 |
<!-- /tabela:rejeicoes -->

Leitura, em quatro pontos. (1) **Quem escreveu**: 61 edições aceitas no `qwen2.5:7b` (40 na E1: 12 notas, 22 retificações e 6 verbetes novos; biblioteca de 6.582 para 9.820 tokens estimados numa época e 11.377 ao fim, +73%), 39 no Coder 7B (só notas e retificações, 6.582 → 8.765), 10 no 3B (9 retificações e 1 verbete novo, 6.582 → 7.236) e **0 no Granite**. (2) **Granite**: 181 propostas em três épocas, 133 barradas por `texto_longo` (o TEXTO passou de 280 caracteres), 26 por `bloco_malformado` e 25 respostas cortadas no teto de 700 tokens — com 508 a 528 tokens de saída por proposta, o modelo escreve o dobro do que o formato aceita; é incompatibilidade entre política de edição e formato, não incapacidade (achado 4.30; mapa §6.10, linha 11). (3) **Saturação**: as aceitas caem de 40 para 12 e 9 no `qwen2.5:7b` e de 25 para 7 e 7 no Coder 7B, e os motivos das épocas 2 e 3 são `duplicada` (53 e 33), `teto_notas_verbete` (33 no `qwen2.5:7b`) e `palavra_chave_invalida` — a biblioteca de 36 verbetes esgota o que cabe acrescentar sob a regra de só acréscimo (achado 4.32; mapa, linha 12). (4) **Decorar**: `tentativas_de_decorar` = 0 nas 12 épocas — nenhuma proposta rejeitada por copiar o texto do caso ou citar o identificador; e o modelo propõe tanto quando erra quanto quando acerta (`qwen2.5:7b` na E1: 14 aceitas de 29 propostas nos 18 casos errados, 26 de 58 nos 36 certos).

**Custo do prefixo compartilhado**: em 10 das 12 épocas o prefill por token da proposta (`prefill_ms_por_token_proposta`) é menor que o do diagnóstico da mesma época (`prefill_ms_por_token_diagnostico`) — Granite 68,0 → 43,3 ms, Coder 7B 52,4 → 31,6, `qwen2.5:7b` 52,4 → 31,5, 3B 21,2 → 15,0 na E1; as exceções são as épocas 2 e 3 do 3B (8,5 → 15,1 e 9,0 → 14,9), em que o diagnóstico já vinha barato. O cache de prefixo agiu na proposta (continuação literal do prompt de diagnóstico), como na 2-B (4.21, 4.28).

Três recortes que só esta fase produz: o **histograma dos 30 códigos de rejeição** por modelo (diz se o modelo erra o formato ou erra o conteúdo — é o que H4 pergunta); as **tentativas de decorar o caso**, isto é, propostas rejeitadas por copiar o texto do caso ou citar o identificador dele; e a diferença entre o que o modelo propõe **quando errou** o diagnóstico e **quando acertou**. O custo do prefixo compartilhado entre diagnóstico e proposta (ms por token de prefill de um e de outro) entra aqui: é a verificação de que o cache de prefixo agiu também na proposta, como agiu na 2-B (4.21, 4.28). Os três recortes estão nas tabelas e na leitura acima: o histograma por modelo, `tentativas_de_decorar` = 0 e as colunas `quando_errou` / `quando_acertou`.

**Uma recusa já apareceu no piloto e mudou o parser.** No piloto de fumaça da implementação (`task-7-report.md`, relatório interno em `.superpowers/`, fora do git — `.gitignore` l. 19; esse piloto foi apagado e o parser mudou depois dele, então é registro histórico, não reproduzível; o piloto reproduzível é `rodar_fase3.ps1 -Piloto`), o `qwen2.5-coder:3b` teve **6 de 6 propostas recusadas por `bloco_malformado`** — cinco por não escrever a linha `FIM` e uma por faltar o campo `TEXTO`. As respostas não estavam cortadas: 185 a 192 tokens de saída contra um teto de 700. O modelo escrevia os campos todos, encerrava no `MOTIVO` e parava. Recusar por isso faria a biblioteca dele nunca crescer e esta fase não medir nada nesse modelo, então o parser passou a aceitar o bloco sem `FIM` quando a resposta não foi cortada, e a ausência virou a métrica `fim_ausente` (decisão 38). A contagem de `fim_ausente` por modelo entra nesta seção: ela diz quanto da leitura de H4 ("o 3B tem mais rejeições por formato") é formato de verdade e quanto era rigidez do parser. Na bateria, `n_fim_ausente` por época: Granite 17, 16 e 17 blocos sem `FIM` (de 58, 62 e 61 propostas), 3B 12, 8 e 8, Coder 7B 54, 54 e 54 (todas) e `qwen2.5:7b` 87, 84 e 89 (quase todas): os dois modelos de 7B **nunca** escrevem `FIM`, e sem a decisão 38 a fase não teria medido nada neles.

## 7. Revisão humana das edições

Amostra determinística de até 30 edições aceitas por modelo (10 por época, estratificadas por operação), em `resultados_alvo/fase3/revisao_edicoes__<modelo>.md`, com o Eric marcando cada uma como `Correta`, `Parcial` ou `Errada`. A validação em código diz se a edição **pode** entrar; só a leitura humana diz se ela **está certa** sobre o sistema.

<!-- ! Alteração de IA - Revisar: a revisão das 63 edições foi feita em primeira passada pelo Claude em 22/09/2026, a pedido do Eric, e apurada por decidir_modelo.py lendo as planilhas direto da pasta.
     ! Motivo: o Eric pediu que a IA adiantasse a revisão para a análise decisória não ficar com o critério "qualidade das edições" em branco; resumo_fase3.json é registro oficial e não foi regravado, por isso a apuração lê as planilhas. -->
**Primeira passada feita pelo Claude em 22/09/2026, a pedido do Eric**, conferindo cada texto contra o código do cobaia (`produtos.py`, `pedidos.py`, `fault_injection.py`, `database.py`, `produtos_api.php`, `schema_completo.sql`, `seed.sql`), o caso citado (`banco_casos*.py`) e o verbete original; os vereditos ficam provisórios até a revisão do Eric. Critério aplicado: `Correta` = verdadeiro sobre o sistema e pertinente ao diagnóstico (o comentário marca "Redundante" quando o verbete já dizia aquilo); `Parcial` = vago, recomendação sem fato novo ou verdade fora de lugar; `Errada` = afirma o que o código não faz ou atribui a causa a outro componente. Apuração por `decidir_modelo.py` (`decisao_modelo.md` §7; `revisao_humana` → `fonte` diz que as planilhas foram lidas direto da pasta, porque `resumo_fase3.json` é registro oficial e não é regravado):

<!-- tabela:revisao -->
| Modelo | n | Correta | Parcial | Errada | Sem avaliação |
| --- | --- | --- | --- | --- | --- |
| `qwen2.5-coder:3b` | 10 | 40,0% | 20,0% | 40,0% | 0,0% |
| `qwen2.5-coder:7b` | 24 | 41,7% | 29,2% | 29,2% | 0,0% |
| `qwen2.5:7b` | 29 | 31,0% | 27,6% | 41,4% | 0,0% |

_Fonte: planilhas revisao_edicoes__<slug>.md lidas direto da pasta da corrida._
<!-- /tabela:revisao -->

Leitura. Das 63 edições, 23 são corretas, 17 parciais e 23 erradas — e **21 das 23 corretas repetem o que o verbete original já dizia** (as duas exceções são do Coder 7B: a nota sobre `Allowed memory size exhausted` em `lex-12` e a nota sobre a resposta antiga sobrescrever a nova em `efe-13`). No vencedor, `qwen2.5:7b`, 12 das 29 (41,4%) afirmam algo que o código não faz — "a API lê dados antigos do banco", "aplicar o fator correto na conversão de `valor_produto`", "corrigir a lógica do LEFT JOIN" — e nas 10 da época 1 (a biblioteca L1 escolhida) o placar é 3 corretas, 4 parciais e 3 erradas. Duas consequências: o ganho de L1 (§3) coexiste com notas erradas e não pode ser creditado à verdade do que foi escrito — é coerente com ZHAO, W. et al. (2026), agentes que não usam a experiência que escreveram (mapa §6.10, linha 17), e com o fato de as notas alterarem `sintomas` e `palavras_chave` do frontmatter, que alimentam a recuperação; e a biblioteca de produção precisa de curadoria humana antes de ir para a Fase 4 (§12; achado 4.35). Um único revisor, sem medida de concordância (§11).

## 8. Perfil por modelo

Um bloco por modelo, na forma dos relatórios anteriores: o que ganhou entre L0 e L3, onde ganhou, o que escreveu, o que foi rejeitado, quanto custou e qual é o papel dele na decisão final.

### `granite4.2:8b`
**Não escreveu nada que entrasse**: 0 de 181 propostas aceitas (133 `texto_longo`, 26 `bloco_malformado`, 25 respostas cortadas no teto de 700 tokens — escreve 508–528 tokens por proposta). A biblioteca ficou idêntica nas quatro versões (hash `3196327e7fd5`), e por isso a curva é plana: 80,6% de acerto e 83,3% de acurácia balanceada nos 36 em L0..L3, 76,7% → 75,6% nos 90 (Q de Cochran p = 0,1116 nos 54, por três perdas em L2 — a biblioteca não mudou, então são variações do próprio modelo entre passadas). É o segundo colocado da regra 36 (83,3% nos 36) e o primeiro em 16 dos 36 cortes de estabilidade (`decisao_modelo.md` §3), mas custa 131,3 s por diagnóstico e 264–286 s por proposta (26h58 no total) e não pôde rodar a ponte de versão (§11). Papel na decisão: referência de acerto estável, sem ganho de biblioteca e com o maior custo; o reteste com `TEXTO_MAX` = 600 (menu da 3-B, item d) seria a única forma de saber se ele documenta — e depende de 8 GB livres que a máquina não teve em 21/09 (decisão 52).

### `qwen2.5-coder:7b`
39 edições aceitas (25 na E1, 7 e 7 depois; só notas e retificações, nenhum verbete novo), biblioteca de 6.582 para 8.765 tokens. Nos 36 a curva só se move em L3 (75,0% → 77,8% de acerto; 80,0% → 84,2% de acurácia balanceada, 3 ganhos e 2 perdas); nos 90 o melhor é L1 (78,9%) e L3 fica abaixo de L0 (75,4%). É o único modelo com `formato_valido_pct` abaixo de 100 (97,8–96,7% nos 90 com L1–L3) e o de maior autoenvenenamento nos 54 (9,3% em L2→L3). Revisão das edições: 10 corretas (8 redundantes), 7 parciais, 7 erradas em 24. Custo mediano de 68,7 s (L0) a 49,8 s (L3) por diagnóstico e 118–130 s por proposta; 12h06. Papel: quarto na regra 36 (84,2% em L3, atrás das três versões editadas do `qwen2.5:7b`); não domina o `qwen2.5:7b` em nenhum eixo do Pareto.

### `qwen2.5:7b`
**O vencedor.** 61 edições aceitas (40 na E1: 12 notas, 22 retificações, 6 verbetes novos; 12 e 9 depois, com `duplicada` e `teto_notas_verbete` dominando as rejeições), biblioteca de 6.582 para 11.377 tokens (45 verbetes). Nos 36: 77,8% → 88,9% de acerto em L1 (b/c 4/0, p = 0,125), 83,3% em L2, 86,1% em L3; acurácia balanceada 81,2 → **91,7** → 84,2 → 86,2 — pico em L1 e regressão, o padrão de LIN (2026). Nos 90: 75,7 → 83,0 (L1) → 78,1 → 80,7. Autoenvenenamento máximo 5,6% (L1→L2, nos 36). Recuperação levemente pior em quem editou (MRR 0,596 → 0,580 em L1) e nenhum dos 9 verbetes novos recuperado nos 36. Revisão das edições: 9 corretas (todas redundantes), 8 parciais, 12 erradas em 29. Custo mediano 66,8 s (L0) a 47,0 s (L3) por diagnóstico, 155–175 s por proposta; 13h53. Papel: primeiro na regra 36 (91,7%), P(top-1) de 77,6% no bootstrap dos 36 e 50,0% nos 90, vencedor do escore ponderado e único de 7B na fronteira de Pareto (L1 e L3).

### `qwen2.5-coder:3b`
10 edições aceitas (9 retificações e 1 verbete novo) em 161 propostas: 91 rejeitadas por `bloco_malformado` (o modelo omite o campo TEXTO — o formato que a H4 previa) e 17 por `arquivo_inexistente`. Nos 36: 69,4% → 72,2% desde L1 (um caso ganho, `tra-4`, e mantido); acurácia balanceada 68,8 → 70,4 → 71,2 → 71,2. Autoenvenenamento máximo 2,8%. Revisão das edições: 4 corretas (todas redundantes), 2 parciais, 4 erradas em 10. É o mais barato de longe — 30,8 s (L0) a 18,4 s (L3) por diagnóstico, 57 s por proposta, 05h02 no total — e por isso ocupa a fronteira de Pareto em L1 e L2 e vence o escore ponderado quando o peso do custo chega a 0,75 (`decisao_modelo.md` §5). Papel: a alternativa barata, a 20 pp do vencedor em acurácia balanceada nos 36.

## 9. Custo na máquina-alvo

Mediana e p95 por caso, com prefill e geração separados, por modelo e por tipo de inferência (diagnóstico e proposta), mais o total de horas por modelo.

**O que o piloto de fumaça da implementação já mediu** (origem: relatório da tarefa do executor, `task-7-report.md`, relatório interno em `.superpowers/`, fora do git — `.gitignore` l. 19; o piloto foi apagado e o parser mudou, logo é registro histórico, não reproduzível — o reproduzível é `rodar_fase3.ps1 -Piloto`; `qwen2.5-coder:3b`, 3 casos na época 1 mais 6 casos no teste de retomada, na máquina-alvo, só CPU): prefill de **24 a 26 ms por token** no diagnóstico com a biblioteca recém-lida; **≈ 32 s por diagnóstico** (25,6 a 34,8 s) e **≈ 57 s por proposta** (54,2 a 60,5 s). O **cache de prefixo agiu também na proposta**, que é a continuação literal do prompt de diagnóstico: o prefill dela custou o dos ~1.090 tokens novos e não o dos 2.106 do prompt inteiro — **32,9 s contra os 54,8 s** que custaria sem reaproveitar o prefixo. É a confirmação, dentro desta fase, do que a Verificação 0 da 2-B tinha medido (4.21).

<!-- ! Alteração de IA - Revisar: em 13/09/2026 o parágrafo "(a preencher …)" deu lugar ao bloco
     "Piloto de 10 casos do orquestrador (v2)" e a linha do `qwen2.5-coder:3b` da tabela recebeu os
     números desse piloto; as três outras linhas ficam para a bateria.
     ! Motivo: o item 12 da onda final pedia os números do piloto com origem. Vêm de
     `resultados_alvo/fase3_piloto/` (fora do git, `.gitignore`): `qwen2.5-coder_3b/*.jsonl` (tempo e
     tokens por inferência), `resumo_fase3.json` (medianas, prefill, documentação por época),
     `bibliotecas/qwen2.5-coder_3b/{epoca-0,epoca-1}/fechamento.json`, `diff__E1.md` e `fase3.log`
     (marcos de tempo). O piloto v1 (12/09, `task-12-report.md` em `.superpowers/`, fora do git) rodou
     antes da decisão 41 e teve 0 de 6 propostas aceitas; o v2 é o reproduzível (`rodar_fase3.ps1
     -Piloto`). Nenhum número abaixo foi digitado sem esses arquivos. -->
**Piloto de 10 casos do orquestrador (v2 — 13/09/2026, `rodar_fase3.ps1 -Piloto`: `qwen2.5-coder:3b`, 10 casos com 6 de aprendizado, 1 época + passada final, Ollama 0.34.0, só CPU).** Duração total **00h15** (marco `FIM` do `fase3.log`; código de saída 0 e "modelos com falha: nenhum"): a época 1 (10 diagnósticos com L0 + 6 propostas) levou 11,1 min, a passada final (10 diagnósticos com L1) 3,4 min, e avaliação, comparação, gráficos 12–17 e relatório HTML somaram 3 s. A projeção impressa antes de começar foi 0,48 h (0,33 h de diagnóstico + 0,15 h de proposta) contra 0,25 h reais: as constantes de ms/token da 2-B são conservadoras para o 3B, como o livro-razão registra; o mesmo cálculo para a bateria completa (4 modelos × 3 épocas × 90 casos) dá 67,18 h, e para o 3B sozinho 9,81 h.

Custo por inferência (`resumo_fase3.json`, medianas dos 10 casos): diagnóstico com L0 **30,9 s** (prefill 21,4 s; 55 tokens de saída em média), com L1 **20,2 s** — a segunda passada é mais rápida com biblioteca quase igual (cache de prefixo entre chamadas consecutivas, o mesmo efeito da Verificação 0); proposta **55,8 s** de mediana com 179 tokens de saída em média. O **cache de prefixo agiu na proposta**: prefill de **14,54 ms/token** na proposta contra **20,58 ms/token** no diagnóstico — a proposta é continuação literal do prompt de diagnóstico e só o sufixo é processado.

Documentação escrita (`propostas__E1.jsonl`, `fechamento.json`, `diff__E1.md`): **2 de 6 propostas aceitas** (33,3%), as duas `retificacao` (lex-2 em `[corpo_nao_e_json]`, lex-5 em `[resposta_truncada]`), ambas com o TRECHO entre aspas, agora normalizadas (decisão 41); **4 rejeitadas por `bloco_malformado`** — o modelo escreveu TRECHO e MOTIVO sem TEXTO, omissão do modelo e não do parser, que conta para a H4; 0 `NENHUMA`; 1 bloco sem `FIM` (aceito, `fim_ausente`). Biblioteca: `epoca-0` (hash `3196327e7fd5`) → `epoca-1` (hash `c1e25b70c7b5`), 36 verbetes (0 novos), 0 notas, 2 retificações; texto renderizado de 6.582 para 6.718 tokens estimados; no `.md` cru, 2 arquivos tocados, +971 caracteres (+373 tokens estimados), 12 linhas acrescentadas e 4 "removidas" — são as linhas `sintomas:` e `palavras_chave:` dos dois verbetes, reescritas com a lista antiga como prefixo da nova (o invariante somente-acréscimo passou no fechamento). `historico.jsonl` (2 linhas) e `revisao_edicoes__qwen2.5-coder_3b.md` (2 edições a avaliar, §7) foram gerados pela primeira vez a partir de inferência real. Os dois textos aceitos passam no validador mas são fracos como conhecimento ("Adiciona um exemplo de erro específico…", "Ajuste o código para garantir…"): é exatamente o que a revisão humana existe para julgar.

Acerto (10 casos, `avaliacao_fase3.json`): L0 = L1 = **50,0%** (66,7% nos 6 de aprendizado, 25,0% nos 4 de avaliação; IC95 de 23,7 a 76,3 nos 10); b = c = 0, Q de Cochran = 0, flips 0 — as duas retificações entraram no contexto de 3 dos 10 diagnósticos com L1 (`nota%` = 30,0) sem mudar veredito. Registros: `versao_ollama` em todos os 26 registros e nos 2 `fechamento.json`; `fase3.log` sem bytes nulos e sem acentos trocados (as correções do `.ps1` da onda final, confirmadas na prática). A retomada foi testada no piloto v1 (época reconstruída com hash idêntico, `task-12-report.md`) e não foi repetida no v2.

**Bateria inteira** (`resumo_fase3.json` → `por_modelo_biblioteca_particao`, partição `todos`: `segundos_mediana`, `segundos_p95`, `prefill_ms_mediana`, `geracao_ms_mediana`, `tokens_saida_medio`; `documentacao`: `segundos_mediana_proposta`, `tokens_saida_medio_proposta`, `prefill_ms_por_token_*`; horas pelas marcas `== <modelo>:` do `fase3.log`; a linha do piloto acima fica como histórico):

<!-- tabela:custo -->
| Modelo | Inferência | Mediana s (p95) | Prefill / geração (mediana, s) | Tokens de saída (média) | Prefill ms/token | Horas do modelo (log) |
| --- | --- | --- | --- | --- | --- | --- |
| `granite4.2:8b` | diagnóstico com L0 (época 1) | 131,3 (210,1) | 72,2 / 58,5 | 233 | 68,0 | 26h58 |
| `granite4.2:8b` | diagnóstico com L1 (época 2) | 130,9 (210,3) | 71,9 / 55,7 | 223 | 68,0 |  |
| `granite4.2:8b` | diagnóstico com L2 (época 3) | 132,3 (185,3) | 76,8 / 58,7 | 217 | 68,8 |  |
| `granite4.2:8b` | diagnóstico com L3 (passada final) | 132,6 (244,2) | 75,1 / 60,8 | 225 | — |  |
| `granite4.2:8b` | proposta na época 1 | 263,8 | — | 509 | 43,3 |  |
| `granite4.2:8b` | proposta na época 2 | 270,7 | — | 528 | 43,0 |  |
| `granite4.2:8b` | proposta na época 3 | 285,6 | — | 508 | 46,4 |  |
| `qwen2.5-coder:7b` | diagnóstico com L0 (época 1) | 68,7 (86,7) | 50,9 / 14,6 | 82 | 52,4 | 12h06 |
| `qwen2.5-coder:7b` | diagnóstico com L1 (época 2) | 67,4 (97,9) | 47,5 / 15,2 | 87 | 39,8 |  |
| `qwen2.5-coder:7b` | diagnóstico com L2 (época 3) | 65,5 (102,4) | 47,7 / 14,4 | 84 | 38,7 |  |
| `qwen2.5-coder:7b` | diagnóstico com L3 (passada final) | 49,8 (104,6) | 24,7 / 15,3 | 90 | — |  |
| `qwen2.5-coder:7b` | proposta na época 1 | 117,7 | — | 196 | 31,6 |  |
| `qwen2.5-coder:7b` | proposta na época 2 | 122,3 | — | 198 | 31,6 |  |
| `qwen2.5-coder:7b` | proposta na época 3 | 130,1 | — | 203 | 31,9 |  |
| `qwen2.5:7b` | diagnóstico com L0 (época 1) | 66,8 (78,8) | 51,1 / 13,8 | 62 | 52,4 | 13h53 |
| `qwen2.5:7b` | diagnóstico com L1 (época 2) | 78,2 (94,3) | 61,6 / 13,8 | 63 | 47,4 |  |
| `qwen2.5:7b` | diagnóstico com L2 (época 3) | 77,6 (102,4) | 61,6 / 14,1 | 63 | 43,1 |  |
| `qwen2.5:7b` | diagnóstico com L3 (passada final) | 47,0 (90,6) | 29,4 / 14,4 | 63 | — |  |
| `qwen2.5:7b` | proposta na época 1 | 154,5 | — | 322 | 31,5 |  |
| `qwen2.5:7b` | proposta na época 2 | 168,0 | — | 339 | 29,8 |  |
| `qwen2.5:7b` | proposta na época 3 | 174,7 | — | 368 | 29,1 |  |
| `qwen2.5-coder:3b` | diagnóstico com L0 (época 1) | 30,8 (36,9) | 22,5 / 6,0 | 56 | 21,2 | 05h02 |
| `qwen2.5-coder:3b` | diagnóstico com L1 (época 2) | 16,6 (36,4) | 8,8 / 5,9 | 56 | 8,5 |  |
| `qwen2.5-coder:3b` | diagnóstico com L2 (época 3) | 17,8 (35,9) | 9,5 / 5,8 | 56 | 9,0 |  |
| `qwen2.5-coder:3b` | diagnóstico com L3 (passada final) | 18,4 (35,1) | 9,8 / 5,9 | 56 | — |  |
| `qwen2.5-coder:3b` | proposta na época 1 | 57,8 | — | 194 | 15,0 |  |
| `qwen2.5-coder:3b` | proposta na época 2 | 57,5 | — | 189 | 15,1 |  |
| `qwen2.5-coder:3b` | proposta na época 3 | 56,8 | — | 188 | 14,9 |  |
<!-- /tabela:custo -->

Leitura. O tempo é dominado pelo prefill e pela prolixidade, não pelo porte (4.13, 4.28; mapa §6.10, linha 27): o Granite gasta 72 s de prefill e 58 s de geração por diagnóstico porque escreve 217–233 tokens onde o `qwen2.5:7b` escreve 62–63; na proposta, 508–528 tokens contra 322–368. O Coder 7B e o `qwen2.5:7b` têm a mesma geração (14–15 s) e o mesmo prefill em L0 (51 s); a diferença de 12h06 para 13h53 é a proposta mais longa do `qwen2.5:7b` (322–368 tokens, 155–175 s). Três cuidados na leitura do custo por versão: (1) no `qwen2.5:7b` o prefill do diagnóstico sobe de 51,1 s (L0) para 61,6 s (L1 e L2) porque os verbetes recuperados passam a carregar as notas (contexto com nota em 94,4% dos 36, §3) — a biblioteca maior custa no prefill, como 4.28 previa; (2) a passada final com L3 é mais barata nos três modelos que editaram (prefill 29,4 / 24,7 / 9,8 s) e no 3B a queda aparece já em L1 (22,5 → 8,8 s): a passada final roda os 90 diagnósticos sem propostas intercaladas, e o executor não controla o estado do cache do runtime entre passadas — logo `segundos_mediana` de versões diferentes da mesma corrida não é comparável como custo da biblioteca, e a diferença de 79,5 s (L1) para 53,9 s (L3) nos 36 do `qwen2.5:7b` (`decisao_modelo.md` §4) não diz que a L3 é mais barata; (3) o custo de L0 reproduz entre corridas: a ponte de versão (§11) repetiu L0 nos 36 e deu 68,0 s de mediana no `qwen2.5:7b`, 70,8 s no Coder 7B e 32,3 s no 3B, contra 69,5, 70,7 e 32,2 s na bateria. Total real: **58h59** contra 67,18 h projetadas.

## 10. Comparação com as fases anteriores

A leitura das três fases juntas — o que é comparável, o que não é, e a recomendação do modelo final — está em [comparacao-entre-fases.md](comparacao-entre-fases.md), gerada de `comparacao_fases.json`/`comparacao_fases.md` por `comparar_fases.py`. Dois pareamentos nascem aqui: **2-B A2 × Fase 3 L0** (mesma máquina, mesmo prompt, mesma biblioteca — mede a reprodutibilidade entre execuções, nos 36 e nos 86 casos não alterados) e **Fase 3 L0 × L3** (mede o efeito da biblioteca escrita pelo modelo). Gráficos 16 `comparacao-entre-fases` e 17 `custo-versus-acerto-tres-fases`.

## 11. Ameaças à validade

Estas já valem: decorrem do desenho, não do resultado.

- **Memorização parcial nos 54**: os casos de aprendizado são exatamente aqueles cujas lacunas o modelo teve chance de documentar. O ganho nos 54 mistura aprender e decorar; é por isso que a leitura principal é a dos 36, e por isso as duas partições aparecem em toda tabela. As barreiras contra decorar (proibição de copiar o texto do caso, proibição de citar o identificador, motivo fora do índice de busca) reduzem, não eliminam.
- **Os 4 fixtures corrigidos** (achado 4.20) caem todos no aprendizado. Os 36 de avaliação pareiam com a 2-B sem ressalva; nos 90, a comparação com 2-A e 2-B vale sobre 86 casos.
- **A estimativa de tokens por caracteres não é o tokenizador**: 4.18 mediu 2,62 a 2,83 caracteres por token nos modelos desta fase (Granite e Qwen2.5), contra os 3,3 estimados. Por isso os tetos são checados também com a contagem real do tokenizador em toda inferência, e um caso que encoste no contexto aborta a época em vez de ser truncado em silêncio.
- **Um único revisor humano** das edições: as proporções de `Correta`/`Parcial`/`Errada` não têm medida de concordância entre revisores.
- **Prompts idênticos aos da 2-B são condição, não escolha estética**: formatação de prompt muda resultado, e comparar fases com prompts diferentes mediria a formatação. O preço é não poder melhorar o prompt de diagnóstico nesta fase.
- **36 casos de avaliação** é uma amostra pequena: só efeitos grandes ficam significativos no McNemar. O efeito mínimo detectável é reportado junto com cada teste (§4), e a acurácia balanceada é a métrica primária justamente porque o acerto simples em 36 casos é grosseiro.
- **Uma execução por condição**, temperatura 0,1, um modelo residente por vez, só CPU — como nas fases anteriores. A reprodutibilidade entre execuções é estimada pelo pareamento 2-B A2 × Fase 3 L0 (§10).
- **A versão do Ollama não é a da 2-B**: a 2-B rodou inteira em 0.33.3 nesta máquina, inclusive a Verificação 0 do cache de prefixo registrada no `fase2b.log` (o achado 4.21, Verificação 0 medida no Ryzen em 03/09/2026, é que rodou em 0.33.2); o runtime atualizou sozinho para **0.34.0** em 12/09/2026, antes da bateria desta fase, e não foi revertido — a máquina é corporativa e a atualização é automática. Nenhuma comparação com a 2-B controla esse fator: o pareamento 2-B A2 × Fase 3 L0 nos 36 e nos 86 casos (§10) passa a medir também o efeito da versão, e é assim que ele deve ser lido. Dentro da Fase 3 o fator não existe: L0 é medido de novo em 0.34.0, todas as comparações entre L0..L3 e entre modelos são na mesma versão, `maquina.json` grava a versão e, pela decisão 44, ela vai em todo registro e a corrida aborta se mudar no meio.
- **Cada modelo escreve a própria biblioteca**, então a biblioteca deixa de ser variável controlada: diferenças entre modelos em L3 misturam quem lê melhor com quem escreve melhor. Os diffs e o hit@k por biblioteca (§5) são o que separa as duas coisas sem gastar inferência.
<!-- ! Alteração de IA - Revisar: três ameaças acrescentadas em 22/09/2026 (ponte de versão da 3-B, revisão por IA, custo por versão).
     ! Motivo: decorrem do que aconteceu depois da bateria — o Ollama passou a 0.34.1, o Granite não coube na RAM para a ponte, a revisão das edições foi adiantada pela IA e a tabela de custo mostrou a passada final mais barata sem que a biblioteca fosse a causa. -->
- **Ponte de versão (3-B, 21/09/2026; decisão 47)**: o Ollama passou a 0.34.1 depois da bateria; L0 foi repetido nos 36 com o mesmo prompt em três modelos (`rodar_fase3b.ps1 -Modo ponte`, `resultados_alvo/fase3b_ponte/`, apurado em `decisao_modelo.md` §6): `qwen2.5-coder:3b` b/c 0/0, `qwen2.5-coder:7b` 0/0, `qwen2.5:7b` 1/1 (`sin-14` passou a certo e `tra-10` a errado — os mesmos dois casos que oscilam entre versões da biblioteca na bateria, §3), p = 1,0 nos três; medianas 32,3 / 70,8 / 68,0 s contra 32,2 / 70,7 / 69,5 s. Critério b + c ≤ 2 satisfeito: qualquer teste da 3-B nesses três modelos é pareável com a Fase 3. O `granite4.2:8b` **não tem ponte**: exige 8 GB de RAM livre e a máquina ofereceu 7,8 GB nas duas tentativas (21/09, dia e noite); o Eric decidiu não insistir (decisão 52) — nenhum teste da 3-B inclui o Granite, e a decisão do modelo não depende dele.
- **Revisão das edições feita em primeira passada por IA** (§7): os vereditos das 63 edições foram dados pelo Claude e conferidos contra o código, mas são de um único revisor não humano até o Eric revisar; a proporção de `Errada` (36,5% no total) é o número mais sensível a essa condição.
- **Custo por versão não comparável dentro da corrida** (§9): a passada final e o estado do cache do runtime fazem `segundos_mediana` variar entre L0..L3 sem que a biblioteca seja a causa; o custo que entra no Pareto é o de cada (modelo, L) tal como medido, e a ponte mostra que L0 reproduz.

## 12. Conclusões e o que decidir

1. **O modelo consegue melhorar a documentação que consulta sem estragá-la?** Em parte. Um modelo (`qwen2.5:7b`) melhorou o próprio acerto nos casos nunca vistos (+11,1 pp em L1, 4 ganhos e 0 perdas) sem estragar (autoenvenenamento máximo 5,6%, sob o teto de 10%); um (`qwen2.5-coder:7b`) ficou no mesmo lugar nos 36; um (`qwen2.5-coder:3b`) ganhou um caso; e um (`granite4.2:8b`) não conseguiu escrever nada que o formato aceitasse. Nenhuma diferença alcança o efeito mínimo detectável de 19,4 pp (§4): o resultado é direcional, não estatisticamente resolvido (achado 4.33).
2. **O ganho não veio da verdade do que foi escrito.** A revisão das edições (§7) mostra 41,4% de notas erradas no vencedor e nenhuma nota correta que o verbete já não dissesse; a recuperação não melhorou (§5); nenhum verbete novo foi recuperado nos 36 (§3). O que mudou foram as notas anexadas aos verbetes originais — e o que elas mudam é a consulta (frontmatter) e o texto que o modelo lê junto com o verbete de ouro. A Fase 3-B (troca cruzada de bibliotecas, casos inéditos) é o que separa efeito do conteúdo de efeito da forma (achado 4.35).
3. **Decisão do modelo** (decisão 36; `decisao_modelo.md`; análise completa em [analise-decisoria-modelo-final.md](analise-decisoria-modelo-final.md)): **`qwen2.5:7b` com a biblioteca no estado L1** — 91,7% de acurácia balanceada nos 36 (acerto 88,9%), sem veto; P(top-1) de 77,6% no bootstrap dos 36 e 50,0% nos 90; vencedor do escore ponderado, que só troca de mão com peso de custo de 0,50 (para a própria L3) ou 0,75 (para o 3B em L1). Confirmada pelo Eric em 22/09/2026 (decisão 52), com o Granite sem ponte de versão.
4. **O que fica para a produção**: a cópia L1 do `qwen2.5:7b` só vai para a Fase 4 depois de curadoria humana das 40 edições da E1 (10 revisadas em §7: 3 erradas a remover) — a regra pré-registrada escolhe o estado medido; o estado implantado é o medido menos o que a revisão reprovar, e isso fica como pendência em [../pendencias.md](../pendencias.md).
5. **O que decidir agora**: quais testes da 3-B rodar (menu com custos em [analise-decisoria-modelo-final.md](analise-decisoria-modelo-final.md), §10). A troca cruzada (L1 e L3 do `qwen2.5:7b` lidas pelo Coder 7B e pelo 3B: 144 inferências, ~2,5 h) e os 36 casos inéditos (autoria de ~1 dia mais ~3 h de máquina para `qwen2.5:7b` e 3B) são os que acrescentam evidência; o reteste do Granite com `TEXTO_MAX` = 600 fica inviável sem 8 GB livres, e o A5 sobre L3 é a última prioridade.
