<!-- ! Alteração de IA - Revisar: registro dos 23 cartões históricos criados em 26/10/2026 no Kanban do orientador (projeto "Squad 24 - Kanban", número 24 da organização unicid-projeto-software-2026-2), com número de issue, título, tipo, sprint e coluna, mais os quatro cartões existentes ajustados no mesmo dia.
     ! Motivo: o Eric pediu "no kanban do github, adicione os cards para todas as tarefas que já passaram e já concluímos também, para manter a organização e o histórico"; sem este arquivo, a próxima sessão não saberia quais tarefas concluídas já têm cartão (e com que número), e repetiria ou duplicaria o trabalho. Os cartões foram criados pelo formulário de issue do modelo task.yml, ligados ao projeto 24, movidos para a coluna Producao e fechados como concluídos; a lista foi confirmada pelo Eric antes da criação. -->
# Kanban do orientador: cartões históricos (26/10/2026)

Escrito para: o Claude (ou o Eric) que precisar saber o que já está no quadro "Squad 24 - Kanban" do orientador, antes de criar cartão novo.

## 1. O que foi feito

Pedido do Eric em 26/10/2026: criar no Kanban do GitHub os cartões das tarefas já concluídas, para manter a organização e o histórico. Levantamento feito a partir de `Documentacao/memorial/roadmap.md` (§1 e §2), `1-decisoes-e-historico/historico-por-commit.md` e `1-decisoes-e-historico/decisoes.md`, só leitura. A lista de 23 cartões foi mostrada ao Eric e confirmada por ele (opção "Sim, criar os 23"); ele também aprovou acertar quatro cartões existentes (ver §3).

Cada cartão entrou pelo formulário `task.yml` do repositório `unicid-projeto-software-2026-2/squad-24-projeto`, com os campos de texto passados na query string da URL (`template`, `title`, `projects`, `task_id`, `descricao`, `criterios_aceite`, `feature_ref`) e os dois menus (Tipo de Tarefa e Sprint) escolhidos no navegador; o projeto 24 foi marcado no formulário; a coluna foi definida no campo Status do painel lateral da issue e a issue fechada como concluída em seguida. Critérios de aceite entraram já marcados (`- [x]`), porque descrevem o que foi entregue. Os caminhos de evidência nas descrições usam o prefixo `projeto/`, que é onde a cópia do repositório principal vive no clone do orientador (decisão 72).

## 2. Os 23 cartões criados (todos em Producao, fechados como concluídos)

| Issue | ID | Título | Tipo | Feature | Sprint |
|---|---|---|---|---|---|
| #29 | TSK-F1-001 | Fase 1: ambiente e cobaias (CobaiaFront, CobaiaAPI, instalador único e injeção de falhas) | Desenvolvimento | FT001 | 1 (Setembro) |
| #30 | TSK-F2A-001 | Fase 2-A: taxonomia de defeitos, banco de 90 casos e bateria de prompts com 6 modelos | Testes | FT002 | 1 |
| #31 | TSK-F2B-001 | Fase 2-B: biblioteca base, recuperação BM25 e bateria A0 a A5 na máquina-alvo | Testes | FT002 / FT003 | 1 |
| #32 | TSK-F3-001 | Fase 3: harness da biblioteca gerida pelo modelo (validação em código, partição 54/36 e piloto) | Desenvolvimento | FT003 | 1 |
| #33 | TSK-F3-002 | Fase 3: bateria de 57h59 na máquina-alvo (4 modelos x 3 épocas x 90 casos) | Testes | FT003 | 1 |
| #34 | TSK-F3-003 | Fase 3: análise decisória e escolha do modelo (qwen2.5:7b com a biblioteca L1, decisão 52) | Pesquisa/Spike | FT003 | 1 |
| #35 | TSK-F3-004 | Curadoria da cópia L1 (biblioteca_producao/) e comparativo qwen2.5:7b x qwen2.5-coder:7b | Desenvolvimento | FT003 | 1 |
| #36 | TSK-F3B-001 | Fase 3-B: pontes de versão do Ollama 0.34.1 (21/09) e 0.34.4 (30/09) | Testes | FT003 | 1 |
| #37 | TSK-F3B-002 | Fase 3-B: 36 casos inéditos, corrida dos inéditos e sonda de correção (efe-3 e efe-10) | Testes | FT003 | 1 |
| #38 | TSK-F3B-003 | Fase 3-B: ablação base x instruct e experimento offline do recuperador (corridas 8 e 9) | Testes | FT003 | 1 |
| #39 | TSK-PESQ-001 | Pesquisa bibliográfica, rodadas 1 e 2: levantamento da Fase 3 (§6.9) e mapa de decisões (§6.10) | Pesquisa/Spike | EP001 | 1 |
| #40 | TSK-PESQ-002 | Pesquisa bibliográfica, rodada 3: LLMs locais e ferramental da Fase 4 (§6.12, decisão 55) | Pesquisa/Spike | FT004 | 1 |
| #41 | TSK-PESQ-003 | Pesquisa bibliográfica, rodada 4: documentação autogerida e filtros contra alucinação (§6.13, decisão 65) | Pesquisa/Spike | FT003 | 1 |
| #42 | TSK-INFRA-001 | Economia de tokens e ferramental do Claude Code (hooks, regras por tipo de arquivo, medição) | Configuracao | EP001 | 1 |
| #43 | TSK-DOC-003 | Memorial de Desenvolvimento em cinco pastas (decisões, pesquisa, resultados, ABNT, método) | Documentacao | EP001 | 1 |
| #44 | TSK-DOC-004 | Painel do projeto (painel-do-projeto.html), pendências em fichas e roadmap | Documentacao | EP001 | 1 |
| #45 | TSK-DOC-005 | Projeto de pesquisa ABNT: itens 1 a 8 aplicados, PDF beta e fichamento das referências | Documentacao | EP001 | 1 |
| #46 | TSK-DOC-006 | README como porta de entrada e padrões de comunidade do GitHub (licença MIT, decisão 67) | Documentacao | EP001 | 1 |
| #47 | TSK-F3B-004 | Fase 3-B: troca cruzada de bibliotecas (corrida 1) e fechamento das Fases 3 e 3-B (decisão 69) | Testes | FT003 | 2 (Outubro) |
| #48 | TSK-PF4-006 | Pré-Fase 4: plano aprovado, sondas de disco e de probabilidades (corrida 11) e veredito sobre modelos grandes pelo disco (colibri) | Pesquisa/Spike | FT002 | 2 |
| #49 | TSK-PF4-007 | Pesquisa bibliográfica, rodada 5 parte A: modelos grandes pelo disco e atlas (§6.14.1 a §6.14.5) | Pesquisa/Spike | EP001 | 2 |
| #50 | TSK-PF4-008 | Pré-Fase 4: atlas visual e trilha de raciocínio aberto com relatório por caso (abas Atlas e Raciocínio aberto) | Desenvolvimento | FT004 | 2 |
| #51 | TSK-PF4-009 | Pré-Fase 4: sonda de confiança e cópia curada (corrida 12) e corridas opcionais 5 e 7 (fichas 17 a 20, decisão 71) | Testes | FT003 | 2 |

Numeração dos IDs: os módulos F1, F2A, F2B, F3, F3B, PESQ e INFRA são novos; PF4 continua de TSK-PF4-005 e DOC continua de TSK-DOC-002, que são os últimos dos 15 cartões de 22/10/2026.

## 3. Cartões existentes ajustados no mesmo dia (com o sim do Eric)

| Issue | ID | O que mudou |
|---|---|---|
| #21 | TSK-PF4-001 (corridas 14 e 15) | Já estava em Producao; fechada como concluída. |
| #22 | TSK-PF4-002 (parte B da pesquisa) | De A Fazer para Producao; fechada como concluída (feita em 23/10). |
| #23 | TSK-PF4-003 (especificação da trilha) | De A Fazer para Producao; fechada como concluída (aprovada em 23/10, decisão 77). |
| #24 | TSK-PF4-004 (corrida 13, colibri) | Já estava fechada como "not planned" (decisão 75); movida de A Fazer para Producao para o quadro mostrar só o que está em curso nas outras colunas. |

## 4. Estado do quadro ao fim (conferido no próprio quadro, filtro `status:Producao`)

- No Status: 11 (Status Reports #3 a #13 do orientador).
- Backlog: 4 (#19 FT005, #20 FT006, #25 fechamento da Pré-Fase 4, #26 plano da Fase 4).
- Refinamento: 1 (#18 FT004).
- A Fazer: 1 (#28, o .docx do TCC).
- Fazendo: 2 (#14 EP001, #27 cópia neste repositório).
- Producao: 32 (#1, #2, #15, #16, #17, #21, #22, #23, #24 e os 23 novos, #29 a #51).

Não houve cartão que o GitHub tenha recusado criar ou mover. Dois cartões (#41 e #50) saíram do formulário sem o painel de projeto renderizado na página da issue; recarregar a página resolveu e o campo Status foi definido normalmente.

## 5. O que não foi feito e o que fica para o Eric

- Nenhum arquivo do repositório principal foi alterado além deste registro; nada foi commitado (regra do projeto).
- Os 15 cartões de 22/10 que seguem abertos (#14, #18, #19, #20, #25, #26, #27, #28) não foram tocados.
- O script descartável que montou as URLs dos formulários ficou só no scratchpad da sessão (`kanban_historico.py`), sem versão no git; a lista dos cartões está inteira na tabela acima.

## 6. Como repetir para um cartão novo

Formulário com os campos na URL, por exemplo `https://github.com/unicid-projeto-software-2026-2/squad-24-projeto/issues/new?template=task.yml&title=...&projects=unicid-projeto-software-2026-2%2F24&task_id=...&descricao=...&criterios_aceite=...&feature_ref=...` (valores codificados para URL). Os menus Tipo de Tarefa e Sprint não aceitam valor pela URL e precisam de clique. Depois de criar, o campo Status fica no painel lateral da issue (seção Projects); se a seção não aparecer logo após a criação, recarregar a página.
