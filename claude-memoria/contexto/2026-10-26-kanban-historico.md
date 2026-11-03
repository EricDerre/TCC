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

<!-- ! Alteração de IA - Revisar: seção nova (03/11/2026) com os 12 cartões da Fase 4 criados no Kanban do orientador (issues #52 a #63) e os cinco cartões existentes movidos no mesmo dia, com número, ID, título, tipo, feature, sprint e coluna.
     ! Motivo: o Eric pediu em 03/11/2026 "vamos replicar os commits que fizemos no principal para lá também, atualizando o kanban tbm"; sem esta seção a próxima sessão não saberia que os pacotes P0 a P4 e as corridas 16 a 19 já têm cartão (e com que número), nem que P5 a P8 já estão no quadro, e repetiria ou duplicaria o trabalho. Mesmo método da seção 1: formulário task.yml com os campos na URL, menus no navegador, Status no painel da issue e fechamento como concluída; a lista foi confirmada pelo Eric no quadro de perguntas da sessão antes da criação. -->
## 7. Cartões da Fase 4 (03/11/2026)

Pedido do Eric em 03/11/2026: levar ao Kanban o que foi concluído desde 26/10 (Fase 4) e o que está em curso, com o mesmo método dos 23 cartões históricos. Levantamento, só leitura, em `Documentacao/memorial/roadmap.md` (§1, §2 linhas 16 a 19, §2.8 a §2.11 e §4.6), `decisoes.md` (decisões 79 a 82), `pendencias.md` (fichas 25 a 38), `claude-memoria/plano-aprovado-fase-4.md` (§5 e §6) e nos commits 3befaa2e, 4f3b3e26 e 633ebb27. O Eric confirmou a lista no quadro de perguntas ("Sim, criar os 11", "Sim, mover os 5" e "Sim, criar" o cartão da ficha 25).

### 7.1 Os 12 cartões criados

| Issue | ID | Título | Tipo | Feature | Sprint | Coluna |
|---|---|---|---|---|---|---|
| #52 | TSK-F4-002 | Fase 4, pacotes P0 e P1: ambiente da Fase 4 (Playwright, Chromium, PHP 8.2 e MariaDB portátil), fixtures reais, trilha v2 e relatório v2 | Desenvolvimento | FT001 / FT004 | 2 (Outubro) | Producao, fechada |
| #53 | TSK-F4-003 | Fase 4, pacote P2: caso ao vivo na tela (interceptador, poda, sintoma por molde, seis cenários) e corrida 17 de reprodução (37 de 72 casos reproduzem) | Desenvolvimento | FT004 / FT001 | 2 | Producao, fechada |
| #54 | TSK-F4-004 | Fase 4: banco de 36 casos inéditos (ficha 27, lex-22 a efe-27) e corrida 17 sobre eles (25 de 36 reproduzem) | Testes | FT004 | 2 | Producao, fechada |
| #55 | TSK-F4-005 | Fase 4, pacote P3: diagnóstico ao vivo com selo de confiança e corrida 16 de calibração (k = 3, limiares do selo, ponte 0.40.2) | Desenvolvimento | FT004 | 2 | Producao, fechada |
| #56 | TSK-F4-006 | Fase 4: corridas 18 e 18b (diagnóstico lido da tela contra o fixture), revisão do caso ao vivo e regra R2 como limitação declarada (fichas 37 e 38, decisões 81 e 82) | Testes | FT004 | 3 (Novembro) | Producao, fechada |
| #57 | TSK-F4-007 | Fase 4, pacote P4: cura de seletor em código (seis candidatos, 16 quebras nas duas formas) e corrida 19 (160 de 160 curadas, MTTR mediana 0,639 s) | Desenvolvimento | FT005 | 3 | Producao, fechada |
| #58 | TSK-F4-008 | Fase 4, pacote P5: biblioteca em produção e ciclo de correção; corrida 20 (regras R4 e R5) | Desenvolvimento | FT003 | 3 | A Fazer |
| #59 | TSK-F4-009 | Fase 4, pacote P6: cenários da Fase 5, MTTR e Task Success; corrida 21 (ensaio dos dez cenários) | Desenvolvimento | FT006 | 3 | Backlog |
| #60 | TSK-F4-010 | Fase 4, pacote P7: avaliação da própria trilha (mutações, intervenções, pós-racionalização); corrida 22 | Testes | FT004 | 3 | Backlog |
| #61 | TSK-F4-011 | Fase 4, pacote P8: painel da Fase 4, relatório da fase e documentação (roadmap, README, handoff) | Documentacao | EP001 | 3 | Backlog |
| #62 | TSK-DOC-007 | Réplica dos commits do repositório principal (26/10 a 03/11/2026) na pasta projeto/ deste repositório (decisão 72) | Deploy | EP001 | 3 | A Fazer |
| #63 | TSK-DOC-008 | Projeto de pesquisa ABNT versão 5: achados da Pré-Fase 4 no texto formal (ficha 25, opção b) | Documentacao | EP001 | 3 | A Fazer |

Numeração dos IDs: F4 continua de TSK-F4-001 (#26, o plano da Fase 4) e DOC continua de TSK-DOC-006 (#46). Sprint 2 (Outubro) para o que foi feito até 31/10 e Sprint 3 (Novembro) de 01/11 em diante, inclusive os pacotes planejados. Os critérios de aceite dos seis cartões concluídos entraram marcados; os dos seis planejados, em aberto. Os caminhos de evidência usam o prefixo `projeto/`, como na seção 2. O script descartável que montou as URLs (`kanban_fase4.py`, mesma forma do de 26/10) ficou só no scratchpad da sessão.

### 7.2 Cartões existentes movidos no mesmo dia (com o sim do Eric)

| Issue | ID | O que mudou |
|---|---|---|
| #25 | TSK-PF4-005 (fechamento da Pré-Fase 4) | Do Backlog para Producao; fechada como concluída (feito em 26/10, P7 da Pré-Fase 4). |
| #26 | TSK-F4-001 (plano da Fase 4) | Do Backlog para Producao; fechada como concluída (aprovado em 26/10, decisão 79). |
| #28 | TSK-DOC-002 (.docx do TCC) | De A Fazer para Fazendo (versão 1 provisória em escrita em 03/11). |
| #18 | FT004 (diagnóstico de causa raiz) | De Refinamento para Fazendo (P3 feito; P5 e P7 ainda pendentes). |
| #19 | FT005 (self-healing de localizadores) | Do Backlog para Testes em DEV (P4 feito e medido na corrida 19; falta a Fase 5). |

Ficaram como estavam: #14 (EP001, Fazendo), #20 (FT006, Backlog) e #27 (TSK-DOC-001, Fazendo).

### 7.3 Estado do quadro ao fim (filtros `-status:Producao` e `status:Producao`)

- No Status: 9 (Status Reports #5 a #13; os #3 e #4 aparecem em Producao, fechados, e não foram tocados por esta sessão).
- Backlog: 4 (#20, #59, #60, #61).
- Refinamento: 0.
- A Fazer: 3 (#58, #62, #63).
- Fazendo: 4 (#14, #18, #27, #28).
- Merge, Testes em HOM: 0.
- Testes em DEV: 1 (#19).
- Producao: 42 (os 32 de 26/10, mais #3, #4, #25, #26 e os seis novos #52 a #57).

Nenhum cartão recusado pelo GitHub. Em três issues (#56, #59 e #60) o painel de projeto não apareceu logo após a criação; recarregar a página resolveu, como em 26/10. A sessão do GitHub no navegador interno do aplicativo tinha expirado antes do primeiro cartão (o formulário redirecionou para o login); o Eric entrou de novo e a criação seguiu, sem credenciais digitadas pela IA.

### 7.4 O que não foi feito e o que fica para o Eric

- Nada foi commitado; este registro é o único arquivo do repositório principal tocado por esta sessão.
- A réplica dos três commits no clone do orientador (#62) e o commit e push lá são do Eric, com a ferramenta `ferramentas/replicar_commits_orientador.py` em preparação na sessão principal.
- Os 36 casos inéditos da ficha 27 (#54) seguem à espera da conferência do Eric; o cartão diz isso na descrição.
