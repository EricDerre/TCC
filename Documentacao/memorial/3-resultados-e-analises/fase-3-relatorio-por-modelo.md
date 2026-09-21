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
# Fase 3 — biblioteca gerida pelo próprio modelo: relatório por modelo

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). Leitura das fases anteriores em [fase-2a-relatorio-por-modelo.md](fase-2a-relatorio-por-modelo.md) e [fase-2b-relatorio-por-modelo.md](fase-2b-relatorio-por-modelo.md); a leitura das três juntas está em [comparacao-entre-fases.md](comparacao-entre-fases.md). Gráficos em `Programacao/AgenteCore/experimentos/resultados_alvo/graficos/12…17`; respostas cruas, propostas de edição caso a caso e diffs de cada época em `resultados_alvo/fase3/relatorio_fase3.html`. **Nenhum número deste arquivo foi digitado à mão**: todos saem de `avaliar_fase3.py` (`avaliacao_fase3.json`, `resumo_fase3.json`) e de `comparar_fases.py`, com o corte citado em cada seção.

<!-- ! Alteração de IA - Revisar: linha de estado nova (21/09/2026); a anterior fica como histórico, sem negrito.
     ! Motivo: a bateria rodou de 13/09 08:45 a 15/09 18:44 (`resultados_alvo/fase3/fase3.log`, `FIM … 58h59`, 0 falhas, Ollama 0.34.0) e o cabeçalho ainda dizia "bateria não executada"; as seções §2–§8 e §12 são preenchidas pelo plano complementar de 21/09. -->
> **Estado em 21/09/2026: bateria concluída (13–15/09/2026, 2.088 inferências, 0 falhas, Ollama 0.34.0); resultados em `resultados_alvo/fase3/` (commit b9f9ad9); relatório em preenchimento pelo plano complementar de 21/09/2026.**
>
> Estado anterior (12/09/2026): pré-registrado; a bateria ainda não tinha rodado. A implementação do harness está concluída e revisada; o piloto de 10 casos do orquestrador (`rodar_fase3.ps1 -Piloto`) rodou em 12/09/2026 e os números dele entram em §9; a bateria completa (~60 h) aguarda a decisão do Eric. As seções 1, 2 e 11 valem como estão — descrevem o desenho. As demais estão marcadas com *(a preencher…)* e só recebem número depois da bateria.

## 1. O que foi medido

| Item | Valor |
|---|---|
| Máquina | **máquina-alvo** `TARGET_TSP030`: Intel i5-1235U (10 núcleos, 12 threads), 15,7 GB de RAM, sem GPU dedicada, Windows 11 Pro — a mesma da Fase 2-B. **Ollama 0.34.0**: o runtime atualizou sozinho de 0.33.3 (versão de toda a 2-B nesta máquina, inclusive a Verificação 0 do cache de prefixo registrada no `fase2b.log` em 07/09/2026; o achado 4.21 é a Verificação 0 medida no Ryzen em 03/09/2026, e essa rodou em 0.33.2) para 0.34.0 em 12/09/2026, antes da bateria da Fase 3, e não foi revertido — a máquina é corporativa e a atualização é automática. `maquina.json` grava a versão e, pela decisão 44, ela vai em todo registro e a corrida aborta se mudar no meio. RAM livre e horário de início *(a preencher com `fase3/maquina.json`)* |
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
| Inferências | **522 por modelo** (4 × 90 diagnósticos + 3 × 54 propostas), 2.088 no total *(erros de infraestrutura, respostas cortadas no teto e casos que estouraram o contexto: a preencher com `resumo_fase3.json`)* |
| Custo estimado | **~60 h de CPU** para os 4 modelos, estimativa do plano a partir dos ms/token medidos na 2-B; a projeção que o próprio executor imprime antes de começar dá **67,18 h** (saída registrada no relatório da tarefa do executor, `task-7-report.md`, relatório interno em `.superpowers/`, fora do git — `.gitignore` l. 19; a mesma projeção é reproduzível por `python executar_fase3.py --so-projecao --modelos granite4.2:8b qwen2.5:7b qwen2.5-coder:7b qwen2.5-coder:3b` — `--modelos` é obrigatório: sem ele o script encerra com "the following arguments are required: --modelos"; é o comando que `rodar_fase3.ps1` roda antes da corrida, e a saída conferida em 12/09/2026 termina em "total: 67.18 h"). O piloto de fumaça da implementação já mediu o `qwen2.5-coder:3b` (§9); o valor real dos quatro modelos *(a preencher após o piloto de 10 casos do orquestrador e a bateria)* |
| Estatística | IC 95% de Wilson; McNemar exato pareado contra L0, com Holm nas 3 comparações da mesma célula; Q de Cochran sobre L0..L3; acurácia balanceada (macro-recall por causa) como métrica primária da escolha do modelo (decisão 36) |

## 2. Hipóteses pré-registradas

Escritas antes de a bateria rodar (achado 4.29 e §4.4 do plano aprovado). O veredito de cada uma é preenchido depois, com o número que a sustenta.

| # | Hipótese | Veredito |
|---|---|---|
| H1 | Nos 36 de avaliação, acerto com L3 > L0 nos modelos de 7–8B (McNemar exato, α = 0,05) | *(a preencher)* |
| H2 | O ganho concentra-se nas classes em que a recuperação é fraca (tradução: hit@3 = 46,7%), via aumento do hit@3 da biblioteca do modelo | *(a preencher)* |
| H3 | Nos 54 de aprendizado o ganho é maior que nos 36; a diferença quantifica a memorização | *(a preencher)* |
| H4 | A taxa de aceitação das propostas cresce com o porte; o 3B tem mais rejeições por formato | *(a preencher)* |
| H5 | Autoenvenenamento (casos certos em L(n) que viram errados em L(n+1), nos 36) fica abaixo de 10%; se superar o ganho, o modelo é vetado | *(a preencher)* |
| H6 | A curva não é monótona: reportar o melhor L e o L3, nunca só o último | *(a preencher)* |

## 3. Curva por versão da biblioteca

Acerto de causa raiz por modelo e por versão da biblioteca, separado pelas duas partições. A coluna dos 36 é a que responde se o modelo **aprendeu**; a dos 54 mede quanto ele **decorou** o que viu.

*(a preencher com `resumo_fase3.json` após a bateria; gráfico 12 `fase3-acerto-por-epoca` — um painel por modelo, linha cheia nos 36 e tracejada nos 54)*

| Modelo | L0 (36) | L1 (36) | L2 (36) | L3 (36) | L0 (54) | L1 (54) | L2 (54) | L3 (54) |
|---|---|---|---|---|---|---|---|---|
| `granite4.2:8b` | — | — | — | — | — | — | — | — |
| `qwen2.5-coder:7b` | — | — | — | — | — | — | — | — |
| `qwen2.5:7b` | — | — | — | — | — | — | — | — |
| `qwen2.5-coder:3b` | — | — | — | — | — | — | — | — |

Acurácia balanceada (macro-recall por causa), parcela do rótulo mais frequente, rótulos distintos, formato-ok-conteúdo-errado e fora do conjunto, nas mesmas células: *(a preencher)*. Por classe e por nível: *(a preencher)*.

## 4. Pareado e Cochran

Cada versão da biblioteca contra L0, no mesmo modelo e na mesma partição (mesmos casos, mesmo prompt, mesma máquina — o pareamento por caso é exato):

*(a preencher: `n_pares`, acerto de L0, acerto de L, Δ em pontos percentuais, b/c, p do McNemar exato, p corrigido por Holm, g de Cohen e a razão b/c)*

| Modelo | Partição | L1 vs L0 | L2 vs L0 | L3 vs L0 | Q de Cochran (L0..L3) |
|---|---|---|---|---|---|
| `granite4.2:8b` | 36 / 54 | — | — | — | — |
| `qwen2.5-coder:7b` | 36 / 54 | — | — | — | — |
| `qwen2.5:7b` | 36 / 54 | — | — | — | — |
| `qwen2.5-coder:3b` | 36 / 54 | — | — | — | — |

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
**Flips entre versões consecutivas** — ✓→✗ é o autoenvenenamento da H5, ✗→✓ é o ganho: *(a preencher, por partição e por classe)*. Junto vai a **menor diferença significativa** que o desenho consegue apontar com n = 36, 54 e 90 (McNemar exato, α = 0,05, supondo 20 % de pares discordantes, `d = round(0,2·n)`; calculada por `avaliar_fase3.efeito_minimo_detectavel` e gravada em `resumo_fase3.json` → `efeito_minimo_detectavel`) — não é um cálculo de poder, ao contrário do que o plano §8.2 dizia ("poder 0,8"; ver o anexo "Desvios do plano" em `claude-memoria/plano-aprovado-fase-3.md`) —, para separar "não houve efeito" de "a amostra não alcança".

## 5. Recuperação por biblioteca

A 2-B tinha um hit@3 único, de 78,9%, comum aos seis modelos, porque a biblioteca era a mesma e o recuperador é determinístico (4.23). Na Fase 3 cada modelo tem a sua biblioteca, e o hit@k passa a ser resultado, não constante.

*(a preencher: hit@1/3/5 e MRR por modelo × L, nos 90 e nos 36; gráfico 13 `fase3-recuperacao-por-epoca`)*

Duas medidas específicas desta fase, calculadas junto: **`ouro_deslocado_por_novo`** — casos em que um verbete criado pelo modelo entrou no top-3 e empurrou o verbete de ouro para fora — e as **edições que tornaram o verbete de ouro recuperável no top-3 para o caso que as originou**. O verbete de ouro de cada causa não muda entre L0 e L3 (só verbetes de `tipo: erro` são de ouro, e esses nunca são criados pelo modelo), o que mantém o hit@k comparável entre as quatro versões.

## 6. Documentação produzida

O que cada modelo escreveu, por época: propostas geradas, aceitas pela validação em código, motivos de rejeição, notas e retificações aplicadas, verbetes novos, caracteres e tokens acrescentados, e o crescimento da biblioteca.

*(a preencher com `resumo_fase3.json`; gráfico 14 `fase3-propostas-por-motivo` e gráfico 15 `fase3-crescimento-da-biblioteca`)*

| Modelo | Época | Propostas | Aceitas | % | Notas | Retificações | Verbetes novos | "NENHUMA" | Tokens acrescentados |
|---|---|---|---|---|---|---|---|---|---|
| `granite4.2:8b` | E1–E3 | — | — | — | — | — | — | — | — |
| `qwen2.5-coder:7b` | E1–E3 | — | — | — | — | — | — | — | — |
| `qwen2.5:7b` | E1–E3 | — | — | — | — | — | — | — | — |
| `qwen2.5-coder:3b` | E1–E3 | — | — | — | — | — | — | — | — |

Três recortes que só esta fase produz: o **histograma dos 30 códigos de rejeição** por modelo (diz se o modelo erra o formato ou erra o conteúdo — é o que H4 pergunta); as **tentativas de decorar o caso**, isto é, propostas rejeitadas por copiar o texto do caso ou citar o identificador dele; e a diferença entre o que o modelo propõe **quando errou** o diagnóstico e **quando acertou**. O custo do prefixo compartilhado entre diagnóstico e proposta (ms por token de prefill de um e de outro) entra aqui: é a verificação de que o cache de prefixo agiu também na proposta, como agiu na 2-B (4.21, 4.28). *(a preencher)*

**Uma recusa já apareceu no piloto e mudou o parser.** No piloto de fumaça da implementação (`task-7-report.md`, relatório interno em `.superpowers/`, fora do git — `.gitignore` l. 19; esse piloto foi apagado e o parser mudou depois dele, então é registro histórico, não reproduzível; o piloto reproduzível é `rodar_fase3.ps1 -Piloto`), o `qwen2.5-coder:3b` teve **6 de 6 propostas recusadas por `bloco_malformado`** — cinco por não escrever a linha `FIM` e uma por faltar o campo `TEXTO`. As respostas não estavam cortadas: 185 a 192 tokens de saída contra um teto de 700. O modelo escrevia os campos todos, encerrava no `MOTIVO` e parava. Recusar por isso faria a biblioteca dele nunca crescer e esta fase não medir nada nesse modelo, então o parser passou a aceitar o bloco sem `FIM` quando a resposta não foi cortada, e a ausência virou a métrica `fim_ausente` (decisão 38). A contagem de `fim_ausente` por modelo entra nesta seção: ela diz quanto da leitura de H4 ("o 3B tem mais rejeições por formato") é formato de verdade e quanto era rigidez do parser.

## 7. Revisão humana das edições

Amostra determinística de até 30 edições aceitas por modelo (10 por época, estratificadas por operação), em `resultados_alvo/fase3/revisao_edicoes__<modelo>.md`, com o Eric marcando cada uma como `Correta`, `Parcial` ou `Errada`. A validação em código diz se a edição **pode** entrar; só a leitura humana diz se ela **está certa** sobre o sistema.

*(a preencher com a apuração de `avaliar_fase3.py --gerar-revisao` depois que o Eric preencher as planilhas; um único revisor, então proporções, sem medida de concordância)*

## 8. Perfil por modelo

Um bloco por modelo, na forma dos relatórios anteriores: o que ganhou entre L0 e L3, onde ganhou, o que escreveu, o que foi rejeitado, quanto custou e qual é o papel dele na decisão final.

### `granite4.2:8b`
*(a preencher)*

### `qwen2.5-coder:7b`
*(a preencher)*

### `qwen2.5:7b`
*(a preencher)*

### `qwen2.5-coder:3b`
*(a preencher)*

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

*(a tabela abaixo recebe as três outras linhas com a bateria inteira; o executor imprime a projeção por modelo antes de começar)*

| Modelo | Diagnóstico (prefill / ger. / total) | Proposta (prefill / ger. / total) | Horas no total |
|---|---|---|---|
| `granite4.2:8b` | — | — | — |
| `qwen2.5-coder:7b` | — | — | — |
| `qwen2.5:7b` | — | — | — |
| `qwen2.5-coder:3b` (piloto v2, 10 casos) | prefill 21,4 s · total 30,9 s com L0; 20,2 s com L1 (medianas) | total 55,8 s (mediana); prefill 14,54 ms/token | 0,25 h no piloto; 9,81 h projetadas para 90 casos × 3 épocas |

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

## 12. Conclusões e o que decidir

*(a preencher após a bateria e a revisão humana — inclui a escolha do modelo final do TCC, pela acurácia balanceada nos 36, com veto por autoenvenenamento; ver decisão 36)*
