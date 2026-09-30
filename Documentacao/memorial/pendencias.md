<!-- ! Alteração de IA - Revisar: arquivo reorganizado em 28/09/2026 — cada pendência aberta virou uma ficha com campos fixos (Estado, Quem decide, Aberta em, O que é, Por que importa, Opções, Recomendação, Decisão), escrita em linguagem direta; as fechadas e as antigas foram para o bloco "Histórico", com o texto original preservado; o painel do projeto (ferramentas/gerar_dashboard.py, via ferramentas/painel_textos.py) lê as fichas e mostra uma por cartão.
     ! Motivo: o Eric disse que ler as pendências no Markdown "é bem ruim" e pediu um relatório visual por pergunta, sem jargão — o formato de ficha é o que permite ao gerador do painel montar um cartão por pergunta sem ninguém digitar nada duas vezes, e a linguagem direta segue a mesma regra dos comentários de código (o quê + motivo, amarrado ao processo real: arquivos, comandos e telas de verdade). Nenhuma pendência foi apagada: as fechadas continuam abaixo com o texto de quando foram abertas. -->
# Pendências e questões em aberto

Parte do [Memorial de Desenvolvimento](../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá. O estado por fase e as corridas que faltam estão em [roadmap.md](roadmap.md); as decisões numeradas em [decisoes.md](1-decisoes-e-historico/decisoes.md).

**Como ler este arquivo.** Cada pendência aberta é uma ficha com os mesmos campos: *O que é* (o fato, com os arquivos e comandos reais), *Por que importa*, *Opções*, *Recomendação* e *Decisão*. Termos técnicos vêm explicados na primeira vez em que aparecem. O painel do projeto ([`dashboard/painel-do-projeto.html`](../dashboard/painel-do-projeto.html), gerado por `ferramentas/gerar_dashboard.py`) lê estas fichas e mostra uma por cartão — por isso o formato dos campos não muda (regra em `.claude/rules/documentacao.md`). Pendência fechada não é apagada: o *Estado* vira `fechada em <data>` e a *Decisão* registra o que foi feito.

## Abertas em 23/09/2026 (fechamento das pontas soltas antes do novo plano)

**Decidido pelo Eric em 29/09/2026:** todas as fichas responderam (1 a 11, 14 e 15): opção (a) em todas as que tinham opções; na 10, itens 3 a 8 aprovados (6 com ressalva), 9 a 11 pré-aprovados como versão beta e 1 e 2 à espera do comparativo qwen × coder; na 11, "faça tudo agora". O que foi feito está na Decisão de cada ficha.

**Decidido pelo Eric em 23/09/2026:** os testes complementares da Fase 3-B são os recomendados — troca cruzada e casos inéditos (decisão 56); os 63 vereditos da revisão das edições, dados pela IA, valem como estão; a cópia L1 "está ok"; o trabalho de 22/09 foi commitado (`f86e65d`).

**Fechado pela sessão de 23/09/2026:** o instalador (`install.py`) passou a baixar o `qwen2.5:7b`; a licença do `qwen2.5-coder:3b` foi corrigida para Qwen Research License nos arquivos da decisão (decisão 57); o script das corridas da 3-B (`rodar_fase3b.ps1`) passou a aceitar listas separadas por vírgula; os 36 casos inéditos foram escritos por um agente que só leu o código do sistema-cobaia; a análise decisória ganhou o veredito por modelo (§8.1); o projeto de pesquisa ABNT foi revisado ponto a ponto (`4-projeto-de-pesquisa-abnt/correcoes-aplicadas.md` §5.1); as cinco referências sem endereço foram localizadas; o servidor de memória do código foi diagnosticado (ficha 5).

### 1. Regravar o resumo oficial da Fase 3 com a revisão das edições
- **Estado:** fechada em 29/09/2026
- **Quem decide:** Eric
- **Aberta em:** 22/09/2026
- **O que é:** O arquivo `resumo_fase3.json` (em `Programacao/AgenteCore/experimentos/resultados_alvo/fase3/`) é o resumo oficial da bateria da Fase 3: todas as tabelas do Memorial saem dele. Ele foi gravado antes de existir a revisão das 63 edições que os modelos fizeram na biblioteca, então o bloco `revisao_humana` dentro dele está vazio; por enquanto o script da decisão (`decidir_modelo.py`) lê a revisão direto das três planilhas `revisao_edicoes__*.md`. Regravar o resumo é rodar `python avaliar_fase3.py --saida fase3` (com a variável `RESULTADOS_DIR=resultados_alvo`). O ensaio feito em 23/09 numa cópia mostrou que só esse arquivo muda — e nele só a data de geração e o bloco da revisão; o arquivo caso a caso (`avaliacao_fase3.json`) sai idêntico.
- **Por que importa:** A pasta `resultados_alvo/fase3/` é o registro oficial da bateria, e a regra do projeto é não regravar nada nela sem o seu "pode gravar". Enquanto isso não acontece, quem abrir o resumo acha que não houve revisão.
- **Opções:**
  - (a) Autorizar: o Claude roda o comando e o `git diff` mostra só essa mudança.
  - (b) Deixar como está e registrar que a revisão vive nas planilhas.
- **Recomendação:** (a).
- **Decisão:** (a) — feito em 29/09/2026: `avaliar_fase3.py --saida fase3` regravou `resumo_fase3.json` (só `metadados.gerado_em` e o bloco `revisao_humana`; 82 linhas no `git diff`); `decisao_modelo.json/.md`, `tabelas_relatorio.md` e os blocos colados no relatório da Fase 3, na comparação entre fases e na análise decisória foram regerados (a fonte da revisão passou a ser o resumo); todos os `--check` limpos.

### 2. O que fazer com a cópia L1 do qwen2.5:7b antes da Fase 4
- **Estado:** fechada em 29/09/2026
- **Quem decide:** Eric
- **Aberta em:** 22/09/2026
- **O que é:** "L1" é a biblioteca de conhecimento depois da primeira rodada de edições feitas pelo próprio modelo — a versão escolhida para produção (decisão 52). Nessa rodada o `qwen2.5:7b` fez 40 edições; a revisão leu 10 delas (amostra) e achou 3 erradas; somando as outras épocas, 12 edições do modelo estão marcadas como erradas, e as 30 restantes da época 1 nunca foram lidas. Em 23/09 você disse que a cópia L1 "está ok". Falta saber o que isso significa: usar a pasta `epoca-1` exatamente como está (com as edições erradas dentro), ou o Claude ler as 30 restantes, retirar as reprovadas numa **cópia** (por exemplo `Programacao/AgenteCore/biblioteca_producao/`) e registrar o código de verificação (hash) dessa cópia. A pasta oficial `resultados_alvo/fase3/bibliotecas/qwen2.5_7b/epoca-1/` não muda em nenhum dos casos. **Atualização de 28/09 (23:15):** nos 36 casos inéditos a L1 não repetiu o ganho (perdeu 1 caso contra L0 e não ganhou nenhum) e a L3 ficou 2 casos acima de L0 — tudo dentro do ruído de 36 casos (`roadmap.md` §2.1). Qual versão levar para a Fase 4 (L1 curada ou L3) volta a ser pergunta e será recalculada na integração da 3-B, depois da troca cruzada; a curadoria continua valendo para a versão que for escolhida.
- **Por que importa:** A análise decisória (§8) mostrou que o ganho da L1 veio da forma das notas, não da verdade do que elas dizem. Levar notas erradas para a Fase 4 é levar documentação que o agente vai seguir em produção.
- **Opções:**
  - (a) O Claude faz a primeira passada das 30 edições restantes e grava a cópia curada, com o hash registrado; você confere o que quiser.
  - (b) Usar a `epoca-1` como está.
- **Recomendação:** (a), antes de a Fase 4 começar.
- **Decisão:** (a) — feita em 29/09/2026. `curar_biblioteca.py --listar` gerou a planilha `resultados_alvo/fase3/curadoria_L1__qwen2.5_7b.md` (as 40 edições da época 1: 10 vereditos vindos da planilha oficial e 30 dados pela IA contra o código, com o mesmo critério). `--curar` conferiu que reaplicar as 40 edições a partir da época 0 reproduz o hash oficial (3394d203cab9) e gravou a cópia de produção em `Programacao/AgenteCore/biblioteca_producao/` (hash 1fca10f1a6f6; 40 verbetes; 23 edições mantidas, 17 removidas — todas as marcadas *Errada*, 3 da planilha oficial e 14 da curadoria; as parciais ficaram), com `curadoria.json` listando o que saiu e por quê. Você confere o que quiser na planilha; se mudar um veredito, apague a pasta e rode `--curar` de novo. A pesquisa de literatura sobre os filtros é a rodada 4 do levantamento (`2-pesquisa-e-literatura/levantamento-2026-09-29-documentacao-autogerida.md`, §6.13). Qual versão vai para a Fase 4 (L1 curada ou L3) continua a ser recalculada na integração da 3-B — e o teste `teste_curar_reaplicar_todas_reproduz_hash_oficial` fixa a reconstrução fiel.

### 3. Apagar do Ollama os modelos que não voltam
- **Estado:** fechada em 29/09/2026
- **Quem decide:** Eric
- **Aberta em:** 23/09/2026
- **O que é:** O `ollama list` de 23/09 mostra 24,8 GB de modelos no disco. Os que não têm mais uso no projeto: `granite4.2:8b` (5,3 GB), `phi4-mini:3.8b` (2,5), `qwen2.5-coder:1.5b` (1,0), `qwen2.5-coder:1.5b-instruct-fp16` (3,1) e `qwen2.5-coder:1.5b-instruct-q8_0` (1,6) — 13,5 GB. Os dois Coder (`qwen2.5-coder:7b` e `qwen2.5-coder:3b`, 6,6 GB) ainda servem de leitores nas corridas da 3-B (troca cruzada e casos inéditos) e podem sair depois delas. `ollama rm <modelo>` apaga o arquivo; voltar atrás é baixar de novo.
- **Por que importa:** Disco e clareza: fica só o modelo escolhido. O registro do que cada modelo fez continua na documentação e no painel.
- **Opções:**
  - (a) Apagar os cinco agora e os dois Coder depois das corridas da 3-B.
  - (b) Manter tudo até o fim do TCC.
- **Recomendação:** (a). O Claude só roda o `ollama rm` com a sua confirmação por escrito, modelo a modelo.
- **Decisão:** (a) — feito em 29/09/2026: `ollama rm` de `granite4.2:8b`, `phi4-mini:3.8b`, `qwen2.5-coder:1.5b`, `qwen2.5-coder:1.5b-instruct-fp16` e `qwen2.5-coder:1.5b-instruct-q8_0` (13,5 GB liberados). Ficam `qwen2.5:7b`, `qwen2.5-coder:7b` e `qwen2.5-coder:3b` (os dois Coder saem depois da troca cruzada). Entraram para os experimentos da ficha 11: `qwen2.5:0.5b-base` e `qwen2.5:0.5b-instruct` (0,8 GB, ablação) e `embeddinggemma:300m` (0,6 GB, recuperador) — podem sair quando os experimentos fecharem.

### 4. Quem lança a troca cruzada, e quando
- **Estado:** fechada em 29/09/2026
- **Quem decide:** Eric
- **Aberta em:** 23/09/2026
- **O que é:** A troca cruzada faz os dois Coder lerem a biblioteca escrita pelo `qwen2.5:7b` (versões L1 e L3) nos 36 casos de avaliação; responde se o ganho medido é da biblioteca ou de quem a escreveu. São 144 diagnósticos, cerca de 2,5 h. O script espera até 6,5 GB de RAM livre para carregar o Coder 7B; com a sessão do VS Code aberta há cerca de 5 GB, então de dia ele tende a pular esse modelo (e retoma de onde parou quando é relançado). Comando, na pasta `Programacao/AgenteCore/experimentos`: `powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo cruzada -Saida fase3b_cruzada_qwen -Doador qwen2.5:7b -Versoes 1,3 -Modelos qwen2.5-coder:7b,qwen2.5-coder:3b`.
- **Por que importa:** É uma das duas corridas que fecham o plano complementar de 21/09; sem ela, a limitação 7 da análise decisória (escritor e leitor confundidos) fica em aberto no relatório.
- **Opções:**
  - (a) Você lança à noite, com a máquina livre (tempos medidos limpos).
  - (b) O Claude lança de dia, em segundo plano, e relança quando a RAM liberar.
- **Recomendação:** (a). Os casos inéditos (ficha 12) rodaram em 28/09 das 20:13 às 23:15, com o 3B primeiro e o 7B na sequência, sem pulo; a cruzada pode ir na próxima noite com a máquina livre.
- **Decisão:** (a) — o Eric lança a troca cruzada à noite com o comando do roadmap (corrida 1). A análise comparativa `qwen2.5:7b` × `qwen2.5-coder:7b` foi feita em 29/09/2026: `comparar_qwen_coder.py` (tabelas, confronto caso a caso e a lista de toda célula em que o Coder fica à frente) e o documento `3-resultados-e-analises/comparativo-qwen25-7b-vs-coder-7b.md`. Em resumo: o Coder fica à frente em 26 células, todas pequenas, concentradas nos 54 casos de aprendizado da Fase 3 e nas classes léxica, runtime e efeito; nos 36 casos nunca vistos o qwen vence em todas as versões da biblioteca; como escritor da biblioteca o Coder é mais contido e um pouco mais certo; a decisão 52 se mantém. O que fecharia a pergunta: a troca cruzada e, opcionalmente, o Coder 7B nos 36 inéditos (corrida 7 do roadmap).

### 5. Servidor de memória do código (codebase-memory-mcp) e o plugin pyright-lsp
- **Estado:** fechada em 29/09/2026
- **Quem decide:** Eric
- **Aberta em:** 22/09/2026
- **O que é:** Em 21/09 foi instalado o `codebase-memory-mcp`, um servidor que indexa o código para o Claude consultar a estrutura do projeto sem ler arquivo por arquivo (economia de tokens). Ele está registrado no arquivo `.mcp.json` do projeto, mas o Claude Code não o liga sem a sua aprovação: `claude mcp list` mostra "Pending approval" e a configuração do projeto está com a lista de servidores permitidos vazia. A regra de permanência (decisão 49) diz que ele só fica se cortar 20% ou mais dos tokens em três tarefas fixas — medição que ainda não pôde ser feita. Também ficou faltando o plugin `pyright-lsp` (o verificador de tipos do Python; ajuda o Claude a achar erros sem rodar o código), que não instalou sozinho.
- **Por que importa:** Enquanto o servidor está "pendente", ele não ajuda nem sai; a leitura preliminar pela linha de comando apontou que ele tende a sair (`ferramental-do-claude-code.md` §7.2).
- **Opções:**
  - (a) Aprovar o servidor (`/mcp` numa sessão sua) ou pôr `"enableAllProjectMcpServers": true` em `.claude/settings.json`; o Claude faz a medição e aplica a regra de permanência.
  - (b) Desistir já: `npm uninstall -g codebase-memory-mcp`, apagar `.mcp.json` e `.cbmignore` e registrar no ferramental §7.2.
  - (c) Para o pyright, em qualquer caso: `/plugin install pyright-lsp@claude-plugins-official` numa sessão sua.
- **Recomendação:** (b) para o servidor e (c) para o pyright.
- **Decisão:** (a) — feito pelo Claude em 29/09/2026: `"enableAllProjectMcpServers": true` em `.claude/settings.json` (backup em `.superpowers/sdd/fase3b-e-fechamento/backups-p4/`) e o servidor registrado como aprovado no `~/.claude.json` deste projeto (`enabledMcpjsonServers: ["codebase-memory"]`; backup `.claude.json.bak-2026-09-29`); o `pyright-lsp@claude-plugins-official` foi instalado pela linha de comando (escopo usuário). **Tarde:** o servidor continuava "Pending approval"; o seu `claude` no PowerShell respondeu "não é reconhecido" porque o comando não está no PATH desta máquina (só existe o programa dentro da extensão do VS Code), e o que faltava era a confiança na pasta, que o Claude não pode ligar — você ligou pelo PowerShell. **Noite:** o servidor subiu e a regra de permanência foi medida com as três tarefas fixas, cada uma feita duas vezes só com busca de texto (grep) e duas só com o servidor, e as respostas conferidas contra um gabarito tirado do código. O servidor gastou 8,6% a mais de tokens no total e 4,3% a menos nos tokens novos, longe dos 20% exigidos, com acerto praticamente igual. Por isso ele **saiu**, como a regra manda: `.mcp.json` e `.cbmignore` apagados, a chave que aprovava servidores de projeto retirada do `.claude/settings.json`, pacote desinstalado (`npm uninstall -g codebase-memory-mcp`) e cache do índice apagado; o PATH ficou igual ao de antes da instalação e o Defender não acusou nada. O `pyright-lsp` fica. Números e método no ferramental §7.2; decisão 62.

### 6. Remover o atalho quebrado do Claude instalado pelo npm
- **Estado:** fechada em 29/09/2026
- **Quem decide:** Eric
- **Aberta em:** 22/09/2026
- **O que é:** Existe um atalho antigo, instalado pelo npm (`%AppData%\npm\claude.ps1`, do pacote `@anthropic-ai/claude-code` 2.1.245), que aponta para um programa que não existe mais. A extensão do VS Code usa o próprio binário (2.1.278) e não depende dele. Remover: `npm uninstall -g @anthropic-ai/claude-code`.
- **Por que importa:** Quem digitar `claude` num terminal recebe erro, e ficam duas instalações confundindo o diagnóstico.
- **Opções:**
  - (a) Remover.
  - (b) Deixar.
- **Recomendação:** (a).
- **Decisão:** (a) — feito em 29/09/2026: `npm uninstall -g @anthropic-ai/claude-code` removeu o atalho (não há mais `claude*` em `%AppData%\npm`); o `codebase-memory-mcp` instalado pelo npm continua lá.

### 7. Guardar no git os registros corridos das baterias (os logs)
- **Estado:** fechada em 29/09/2026
- **Quem decide:** Eric
- **Aberta em:** 21/09/2026
- **O que é:** Os arquivos `fase3.log` (bateria da Fase 3) e `fase2b.log` (Fase 2-B) são o único registro linha a linha das execuções (horários, projeções de tempo, relances, abortos). A regra `*.log` do `.gitignore` os deixa fora do commit; `git add -f` inclui os dois uma vez, sem mudar a regra. Você decidiu versioná-los em 21/09; falta rodar o comando: `git add -f Programacao/AgenteCore/experimentos/resultados_alvo/fase3/fase3.log Programacao/AgenteCore/experimentos/resultados_alvo/fase2b.log`. Os logs das corridas da 3-B (`fase3b.log` em cada pasta de saída) entram do mesmo jeito.
- **Por que importa:** Sem eles, o repositório não tem como mostrar quando cada corrida começou e terminou nem quantas vezes foi retomada.
- **Opções:**
  - (a) Rodar o comando junto do próximo commit.
  - (b) Tirar `*.log` do `.gitignore` só para `experimentos/resultados_alvo/`.
- **Recomendação:** (a).
- **Decisão:** (a) e depois (b) — em 29/09/2026 você colocou os seis logs no índice com `git add -f` e, na mesma noite, pediu para não precisar mais disso: o `.gitignore` ganhou uma exceção ao `*.log` para `Programacao/AgenteCore/experimentos/resultados_alvo/**/*.log`. Conferido com `git check-ignore`: os logs das próximas corridas (como o `fase3b_cruzada_qwen/fase3b.log` desta noite) entram no `git add` normal; o log do piloto continua fora, porque a pasta `fase3_piloto/` inteira é ignorada, e logs fora de `resultados_alvo/` também. Decisão 63.

### 8. Corrigir a gravação do log no script da Fase 2-B
- **Estado:** fechada em 29/09/2026
- **Quem decide:** Eric
- **Aberta em:** 12/09/2026
- **O que é:** `rodar_fase2b.ps1` grava o log com `Tee-Object`, que no Windows PowerShell 5.1, quando o script é chamado por `-File`, escreve em UTF-16 — o `fase2b.log` já gravado tem trechos com bytes nulos. O mesmo defeito foi corrigido em `rodar_fase3.ps1` no piloto de 12/09 (trocado por `ForEach-Object` + `Add-Content -Encoding utf8`). A Fase 2-B está fechada e seus resultados não mudam: o patch só vale para corridas futuras.
- **Por que importa:** Só a legibilidade do log; os JSON gravados pelos scripts Python estão certos.
- **Opções:**
  - (a) Aplicar o mesmo patch, com tag e motivo.
  - (b) Só registrar.
- **Recomendação:** (a).
- **Decisão:** (a) — feito em 29/09/2026: em `rodar_fase2b.ps1` os três pipes com `Tee-Object` passaram a `ForEach-Object` + `Add-Content -Encoding utf8` e o console passou a decodificar a saída dos processos em UTF-8 (`[Console]::OutputEncoding`), com tag e motivo; BOM e CRLF preservados; `conferir_docs.py` limpo. Os resultados da 2-B não mudam.

### 9. Padronizar os três scripts PowerShell da raiz (BOM e travessão)
- **Estado:** fechada em 29/09/2026
- **Quem decide:** Eric
- **Aberta em:** 22/09/2026
- **O que é:** `build_exe.ps1`, `install.ps1` e `run.ps1` são anteriores à regra do CLAUDE.md: não têm a marca de UTF-8 no início do arquivo (o BOM) e usam travessão em comentários. O `conferir_docs.py` avisa disso a cada conferência. Conferido em 21/09: como os travessões estão em comentários e não dentro de textos, os scripts rodam normalmente.
- **Por que importa:** Só consistência e silêncio do aviso; nenhum defeito em execução.
- **Opções:**
  - (a) Padronizar (gravar com BOM e trocar o travessão por `-`), com tag e motivo.
  - (b) Manter e conviver com o aviso.
- **Recomendação:** (a).
- **Decisão:** (a) — feito em 29/09/2026: `build_exe.ps1`, `install.ps1` e `run.ps1` gravados em UTF-8 com BOM, travessões dos comentários trocados por hífen, tag e motivo acrescentados (o `build_exe.ps1` ganhou a linha de motivo que faltava); a lista de exceções de `ferramentas/conferir_docs.py` esvaziou — daqui em diante qualquer `.ps1` sem BOM ou com travessão é falha, não aviso.

### 10. Aprovar as 11 modificações propostas para o projeto de pesquisa (ABNT)
- **Estado:** fechada em 30/09/2026
- **Quem decide:** Eric
- **Aberta em:** 23/09/2026
- **O que é:** A revisão ponto a ponto de 23/09 (`4-projeto-de-pesquisa-abnt/correcoes-aplicadas.md` §5.1) propôs 11 mudanças no documento ABNT: (1) o modelo é o Qwen2.5, não o Qwen2.5-Coder; (2) a escolha do modelo pela regra da decisão 36 no lugar de "o menor modelo que atenda"; (3) uma linha para a Fase 3 no cronograma; (4) a sequência das fases como aconteceu; (5) como declarar a revisão feita por IA; (6) "fuzzing" trocado por injeção determinística de falhas; (7) a reprodutibilidade da Fase 3; (8) os endereços das 5 referências que estavam sem URL, com a autoria de MACIAK a confirmar (o artigo é assinado "InstaTunnel"); (9) Faceli conferido no exemplar; (10) o referencial do TCC final; (11) retirar as marcações de IA e regerar o PDF na entrega.
- **Por que importa:** O projeto de pesquisa ainda descreve o plano de antes da Fase 3; sem as mudanças, ele contradiz o Memorial.
- **Opções:** Aprovar item a item; o Claude aplica os aprovados, com tag e motivo, e deixa os demais registrados como não aplicados.
- **Recomendação:** Aprovar 1 a 8 agora; 9, 10 e 11 ficam para a entrega.
- **Decisão:** Registrada em 29/09/2026 e aplicada no documento com marcação: itens 3 (linha "Mês 2 (continuação)" no cronograma), 4 (parágrafo de abertura da §3 ligando as fases aos objetivos), 5 (revisão em primeira passada por IA, ratificada por um revisor), 7 (frase sobre a reprodutibilidade da Fase 3) e 8 (endereços em BISWAS, JÚNIOR, SHI e ZHANG, J.; a entrada MACIAK virou INSTATUNNEL, porque a página é assinada "InstaTunnel" e não mostra nenhum Maciak — se você tiver a origem do nome, a entrada volta); item 6 aplicado com a sua ressalva (injeção determinística dominante; Fuzzing reservado a fases de teste posteriores, também na linha do Mês 5). Pré-aprovados como versão beta: 11 gerou `Projeto de Pesquisa - ABNT 15287_2025 - V4-beta.pdf` (`ferramentas/gerar_pdf_abnt.py`, pelo Edge; as marcações saem só da cópia, o `.md` continua com elas); 9 depende do exemplar do Faceli; 10 não muda o projeto (as fontes das rodadas 2, 3 e 4 entram no TCC final). **Itens 1 e 2 aguardam você:** o comparativo qwen × coder (ficha 4) manteve a decisão 52, e os textos propostos em 23/09 (modelo da família Qwen2.5 com a variante definida experimentalmente; critério da decisão 36 no lugar de "o menor modelo que atenda") continuam válidos — aplico com o seu ok. **30/09/2026:** os itens 1 e 2 foram liberados por você ("ok, pode seguir") e aplicados com marcação: (1) o modelo passou a ser "um modelo da família Qwen2.5 em variante quantizada, com porte e variante (instrução geral ou código) definidos experimentalmente" no objetivo específico 2, na §3.2, no Mês 2 do cronograma e no glossário (entrada "Qwen2.5 / Qwen2.5-Coder"); (2) o critério "o menor modelo que atenda à tarefa" virou a regra fixada antes dos testes (acurácia balanceada nos casos de avaliação nunca vistos, veto por autoenvenenamento, desempate por licença), com latência e memória na análise de robustez. O item 9 fechou: você confirmou no exemplar a 3. ed. de 2025. O PDF beta foi regerado. O item 10 (referencial do TCC final) fica no roadmap §6, para a entrega. Registro item a item em `4-projeto-de-pesquisa-abnt/correcoes-aplicadas.md` §5.2. Ficha fechada.

### 11. Pendências antigas que continuam de pé
- **Estado:** fechada em 30/09/2026
- **Quem decide:** Eric
- **Aberta em:** 23/09/2026
- **O que é:** Sete itens antigos (do bloco "Histórico" abaixo) nunca receberam uma decisão: (a) o fichamento formal das 7 referências do projeto de pesquisa — o recorte de cada uma já está nas seções 2.2 a 2.6, mas não há documento separado; (b) a validação do instalador em Linux — testado só em Windows; (c) os critérios de aceitação quantitativos (MTTR, Task Success, linha de base manual) — já estão na §3.4 desde 12/09; (d) a ablação base × instruct (`qwen2.5:0.5b-base` × `qwen2.5:0.5b-instruct`) como piso metodológico, se a banca pedir um modelo sem instrução; (e) conferir os capítulos citados do Faceli 3. ed. (2025) no exemplar — o sumário foi conferido na ficha da editora, o conteúdo não; (f) melhorar o recuperador da biblioteca (k = 5, sinais para a classe de tradução, embedding denso) — o levantamento das LLMs locais (decisão 55) já adotou a recuperação híbrida para a Fase 4; (g) regerar o PDF e retirar as 20 marcações de IA — só na entrega.
- **Por que importa:** Pendência sem decisão reaparece em toda conferência; cada uma precisa de "faz agora", "fica para o TCC final", "limitação declarada" ou "descartada, com motivo".
- **Opções:** Para cada letra: fazer agora, deixar para o TCC final, manter como limitação declarada, ou descartar.
- **Recomendação:** (a) TCC final; (b) limitação declarada; (c) fechar como feita; (d) manter "só se a banca pedir"; (e) você diz se o exemplar está em mãos; (f) entra na Fase 4; (g) entrega.
- **Decisão:** "Faça tudo agora" (29/09/2026), feito o que era possível: (a) fichamento formal das 7 referências originais em `2-pesquisa-e-literatura/fichamento-referencias-projeto.md` (fontes lidas pela web; BISWAS só por busca, o ResearchGate bloqueia); (b) validação em Linux: esta máquina não tem WSL nem Docker — continua como limitação declarada; (c) fechada: os critérios quantitativos estão na §3.4 desde 12/09; (d) ablação base × instruct feita (29/09, 11:38–13:55; `qwen2.5:0.5b-base` × `qwen2.5:0.5b-instruct`, A0 e A2 nos 90; `resultados_alvo/ablacao_base_instruct/`): o modelo base acerta 0 de 90 nas duas condições e inventa o rótulo em 87,8% dos casos quando recebe a biblioteca; o instruct de 0,5B fica em 4,4% e 1,1% — o piso está medido, leitura no roadmap §2.2 e achado 4.41; (e) Faceli no exemplar: só você; (f) experimento offline do recuperador (`experimento_recuperador.py`, `resultados_alvo/recuperador/`): o BM25 com sinais em código da Fase 3 continua muito à frente do embedding denso (`embeddinggemma:300m`) e do híbrido por fusão de posições — a recuperação híbrida da decisão 55 não se sustenta com este modelo de embedding (números no roadmap §2.2); (g) PDF beta gerado (ficha 10). Fica aberta só pelo item (e). **30/09/2026:** (e) fechado — você confirmou a 3. ed. (2025) no exemplar e colocou os notebooks de apoio do livro em `Documentacao/notebooks/` (14 capítulos, 16 notebooks; chegaram a ser versionados de manhã e saíram do git à noite, decisão 68: material de terceiros sem licença, 330 MB sem uso pelos scripts; o README desse material diz "2ª edição", sinal de que o repositório do livro não foi atualizado — a referência segue o exemplar). Ficha fechada.

### 12. Casos inéditos — conferir 6 antes da corrida, ou rodar
- **Estado:** fechada em 28/09/2026
- **Quem decide:** Eric
- **Aberta em:** 23/09/2026
- **O que é:** Os 36 casos inéditos (`banco_casos_ineditos.py`) foram escritos por um agente que só leu o código do sistema-cobaia, nunca os resultados dos modelos. O gate mecânico passou em 23/09 (36 casos, 2 por célula classe × nível, ids 16–21, validação de formato, nenhum repetido dos 90, nenhuma sobreposição de texto com as bibliotecas dos modelos) e um teste de fumaça do modo `ineditos` também. O que faltava era você conferir 6 casos, um por classe, os de fato mais forte: `lex-16` (corpo real do modo `malformed_json`), `sin-20` (item sem `id` vira `data-id="undefined"`, 422 e modal "Erro"), `semt-18` (modo `type_drift`, `"True"` com maiúscula), `tra-19` (Balde de Cerveja a R$ 4,50 contra 45,00 no `seed.sql`), `run-20` (painel PHP grava na mesma tabela que a API lê, sem cache) e `efe-20` (lista vazia sai antes de limpar a grade).
- **Por que importa:** Um caso errado nos inéditos mede o modelo contra um sintoma que a tela não produz — o mesmo defeito dos achados 4.20 e 4.36.
- **Opções:**
  - (a) Conferir os 6 e depois rodar.
  - (b) Rodar já e conferir depois; se um caso mudar, os registros dele são refeitos.
- **Recomendação:** (a).
- **Decisão:** (b) — em 28/09 você mandou rodar ("já pode começar a rodá-los"). Corrida lançada às 20:13 de 28/09, em segundo plano, com o `qwen2.5-coder:3b` primeiro (cabe nos 5 GB de RAM livres) e o `qwen2.5:7b` na sequência; saída em `resultados_alvo/fase3b_ineditos/` (log `fase3b.log`). Se o 7B for pulado por falta de RAM (o script espera 6,5 GB livres), o Claude relança o mesmo comando quando a memória liberar — o executor retoma do ponto em que parou. A conferência dos 6 casos continua valendo, depois: se algum for corrigido, os registros desse caso são apagados da saída e a corrida relançada, e o executor refaz só o que falta. **Terminou às 23:15 de 28/09** (03h02; 216 diagnósticos; nenhum modelo com falha; a RAM liberou e o 7B rodou na sequência, sem pulo); `avaliar_fase3b.py` gravou `avaliacao_fase3.json` e `resumo_fase3.json` na pasta. Primeira leitura em `roadmap.md` §2.1.

### 13. Dois casos do banco descreviam sintomas que a tela não produz (efe-3 e efe-10)
- **Estado:** fechada em 28/09/2026
- **Quem decide:** Eric
- **Aberta em:** 23/09/2026
- **O que é:** Ao escrever os inéditos, o agente apontou que `efe-3` dizia "ícone de imagem quebrada" quando, sem o campo `imagem`, o cartão simplesmente não desenha imagem nenhuma; e que `efe-10` dizia "R$ 0,00" quando a função de formatação de preço nunca produz isso a partir de um número válido. Mesmo defeito dos quatro casos do achado 4.20, mas descoberto depois da bateria.
- **Por que importa:** A Fase 3 e a 2-B rodaram com esses textos; corrigi-los muda o banco para as corridas futuras (o `efe-3` está nos 36 de avaliação, então 1 caso deixa de ser comparável um a um com a Fase 3).
- **Opções:**
  - (a) Corrigir agora (achado 4.36) e usar a correção como primeira medição do ciclo de correção (ficha 14).
  - (b) Deixar como limitação declarada.
- **Recomendação:** (a).
- **Decisão:** (a) — corrigidos em 28/09 (decisão 58; achado 4.36); os registros oficiais da Fase 3 não mudam; a sonda de detecção de correção rodou sobre os dois (`sonda_correcao.py`, saída em `resultados_alvo/fase3b_correcao/`; leitura em `roadmap.md` §3).

### 14. Ciclo de correção da biblioteca — o que a sonda mostrou e o que entra na Fase 4
- **Estado:** fechada em 29/09/2026
- **Quem decide:** Eric
- **Aberta em:** 28/09/2026
- **O que é:** Você definiu o requisito em 28/09: quando um erro que o agente documentou na biblioteca é corrigido no sistema — com a sugestão dele ou não —, o agente deve perceber e registrar que foi corrigido, sem apagar o histórico (erro + solução sugerida + solução aplicada). A sonda de 28/09 apresentou os dois casos corrigidos ao `qwen2.5:7b` lendo a própria biblioteca L1 e mostrou que, com o prompt congelado da Fase 3, ele **não percebe**: repete as edições antigas, só os limites do validador impedem o texto de entrar de novo, e diagnostica o `efe-10` corrigido com a causa errada. O desenho do que falta (uma operação de edição "correção", um estado por verbete, recuperação das notas pelo id do caso e validação em código) está em `roadmap.md` §4.2.
- **Por que importa:** É parte da função do agente; sem isso a biblioteca acumula erros já corrigidos e o agente segue documentação velha.
- **Opções:**
  - (a) Encaixar o desenho do §4.2 no plano da Fase 4 e guardar a saída da sonda (`resultados_alvo/fase3b_correcao/`) no commit como primeira medição.
  - (b) Encaixar na Fase 4 sem versionar a sonda.
- **Recomendação:** (a).
- **Decisão:** (a) — o desenho do §4.2 do roadmap entra no plano da Fase 4 e a saída da sonda (`resultados_alvo/fase3b_correcao/`) entra no commit (você adiciona). A rodada 4 do levantamento (§6.13, tópico "manutenção e atualização de documentação por LLM") traz a literatura que fundamenta o ciclo de correção.

### 15. O registro das condições da 3-B guarda só o último modelo quando o script roda vários
- **Estado:** fechada em 29/09/2026
- **Quem decide:** Eric
- **Aberta em:** 28/09/2026
- **O que é:** `rodar_fase3b.ps1` chama `executar_fase3b.py` uma vez por modelo, e cada chamada regrava `condicoes_3b.json` na pasta de saída com a própria lista de modelos — ao fim fica só o último. Em `resultados_alvo/fase3b_ineditos/condicoes_3b.json` consta `"modelos": ["qwen2.5:7b"]`, embora o `qwen2.5-coder:3b` também tenha rodado (achado ao fechar a corrida, 28/09 23:15). Os resultados não são afetados: `resumo_fase3.json` (`metadados.modelos`) e os JSONL por modelo estão completos; a ponte de 21/09 tem o mesmo comportamento.
- **Por que importa:** É o arquivo que diz sob que condições a corrida rodou (modo, versões, Ollama, modelos); quem ler só ele acha que a corrida teve um modelo.
- **Opções:**
  - (a) Corrigir `executar_fase3b.py` para juntar a lista de modelos já gravada à nova ao regravar o arquivo (com teste em `testar_fase3b.py`), e regravar o arquivo de `fase3b_ineditos/` e o de `fase3b_ponte/` pela mesma função, com a lista completa.
  - (b) Só registrar aqui.
- **Recomendação:** (a) — a correção é pequena e vale para a troca cruzada, que também roda dois modelos.
- **Decisão:** (a) — feito em 29/09/2026: `_gravar_condicoes` (`executar_fase3b.py`) passou a juntar a lista de modelos de chamadas sucessivas na mesma pasta, mantendo o `criado_em` da primeira, e a recusar um modo diferente na mesma saída; a opção `--completar-condicoes` refez os arquivos de `fase3b_ineditos` (`['qwen2.5:7b', 'qwen2.5-coder:3b']`) e `fase3b_ponte` (`['qwen2.5-coder:7b', 'qwen2.5-coder:3b', 'qwen2.5:7b']`) a partir dos JSONL de diagnóstico; dois testes novos em `testar_fase3b.py` (21 ok).

### 16. Quais filtros da documentação autogerida entram no plano da Fase 4
- **Estado:** fechada em 30/09/2026
- **Quem decide:** Eric
- **Aberta em:** 29/09/2026
- **O que é:** A rodada 4 do levantamento (`2-pesquisa-e-literatura/levantamento-2026-09-29-documentacao-autogerida.md`, §6.13: 8 tópicos, 121 afirmações verificadas — 100 confirmadas e 21 parciais — por 8 pesquisadores e 8 verificadores céticos, 3 rejeitadas) terminou num mapa de 26 filtros (§6.13.10): 14 adotados, 6 adiados, 6 descartados, com o motivo e a fonte de cada um. Os adotados, em resumo: (1) reordenar os campos do bloco de edição para a evidência (TRECHO e id do caso) vir antes do texto; (2) proposta decomposta em alegações curtas, cada uma amarrada a um trecho; (3) retificação só com TRECHO e id do caso preenchidos e cruzados; (5) uma segunda chamada ao modelo com a opção explícita de "nenhuma edição" (custa uma inferência a mais por proposta); (6) abstenção premiada — "NENHUMA" válida e pontuada; (8) checagem em código de nome de arquivo, endpoint e mensagem citados contra o sistema, antes dos 30 motivos; (10) dois tipos de saída para o mesmo trecho — "sinalizar" e "retificar"; (11) peso por tipo de edição na admissão (retificação exige mais); (12) redundância por n-gramas contra o próprio verbete, em código; (13) proveniência por edição (id do caso, data, solução sugerida e aplicada) — é o ciclo de correção da ficha 14; (14) auditoria separada de admissão e de atualização; (15) resolução determinística de conflito entre edições no mesmo trecho; (22) métricas de qualidade calculadas a cada rodada sem humano; (23) revisão humana amostral como porta final. Adiados (dependem de medir custo ou de mais dados): decodificação restrita por gramática (9), verificador de fidelidade pequeno (16), verificação por execução (17), consolidação periódica (18), juiz pequeno especializado (20), classificador de vacuidade (25). Descartados: confiança verbalizada como corte (4), segunda passada de autocrítica do próprio modelo (7 e 19), juiz genérico por LLM (21), detector por estado interno (24), grafo de propagação entre verbetes (26).
- **Por que importa:** É a resposta da literatura à sua pergunta de 29/09 (filtros na geração e na gestão da documentação, mantendo a revisão humana); o que você aprovar vira requisito do plano da Fase 4, junto com o ciclo de correção (ficha 14) e a cópia curada (ficha 2).
- **Opções:**
  - (a) Aprovar os 14 adotados como requisitos do plano, marcando o 5 (segunda chamada) como "medir o custo no i5 antes".
  - (b) Aprovar só os que rodam em código puro (1, 2, 3, 6, 8, 10, 11, 12, 13, 14, 15, 22, 23) e deixar o 5 para depois da medição.
  - (c) Rever linha a linha na hora de arquitetar o plano.
- **Recomendação:** (b) — tudo o que roda em código entra já; a segunda chamada (5) só depois de medida, porque cada inferência do 7B custa de 47 a 78 segundos nesta máquina.
- **Decisão:** (b), em 30/09/2026 ("seguir com a opção recomendada"): os filtros adotados que rodam em código entram no plano da Fase 4 já (mapa em §6.13.10 do levantamento; roadmap §4.4); a segunda chamada ao modelo (filtro 5) só depois de medido o custo, porque cada inferência do 7B leva de 47 a 78 segundos nesta máquina. Decisão 65.

## Histórico — pendências fechadas ou consolidadas (texto original preservado)

<!-- ! Alteração de IA - Revisar: bloco criado em 28/09/2026 com o texto ORIGINAL das pendências anteriores (lista da seção 8 do Memorial e blocos de 11/09, 21/09 e 22/09), movido sem reescrita; as que continuam de pé apontam para a ficha que as consolidou ("→ ficha N"); os comentários de alteração antigos deste arquivo vêm logo abaixo, também sem mudança.
     ! Motivo: o Eric pediu as pendências em linguagem direta, mas não a perda do registro — cada bullet abaixo é o que se sabia quando a pendência foi aberta ou fechada, e é o que a documentação do TCC vai citar. -->
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

### Lista original (seção 8 do Memorial)

- **Regerar o PDF** do projeto de pesquisa a partir do Markdown corrigido, e remover os **20 comentários de marcação** (`<!-- ! Alteração de IA … -->`, contados em 12/09/2026, depois da revisão final) antes da entrega final. → ficha 11(g).
- **Fichamento formal** das 7 referências: o recorte de cada uma já está embutido nas seções 2.2 a 2.6 do projeto de pesquisa, mas não existe documento de fichamento separado. → ficha 11(a).
- **Fechada em 11/09/2026 — padrão de produção do modelo**: deixou de ser uma escolha a fazer sobre os números da 2-B e passou a ser o resultado da Fase 3, pela acurácia balanceada nos 36 casos de avaliação, com veto por autoenvenenamento (decisão 36). A restrição de licença continua valendo como critério de desempate — `qwen2.5-coder:3b` tem licença de pesquisa; `qwen2.5:7b` e `granite4.2:8b` são Apache 2.0 — e o `install.py` segue apontando para o 3b até a decisão sair. **Atualização de 23/09/2026:** a decisão saiu (`qwen2.5:7b` com L1, decisão 52) e o `install.py` passou a baixar `qwen2.5:7b`.
- **Validação em Linux**: o instalador foi testado apenas em Windows. Os caminhos de `apt` e `brew` seguem convenções estabelecidas, mas não foram executados. → ficha 11(b).
- **Critérios de aceitação quantitativos**: definidos no planejamento (fórmula de MTTR, Task Success, linha de base manual, volume), mas ainda não incorporados ao corpo do projeto de pesquisa além da §3.4. → ficha 11(c).
- **Fase 2-B concluída na máquina-alvo** (07–09/09/2026; relatório em `3-resultados-e-analises/fase-2b-relatorio-por-modelo.md`). Decisões que ela deixou para o Eric:
  - **Modelo padrão de produção** entre `qwen2.5-coder:3b` + A2 (63%, 30 s, 2,3 GB, licença de pesquisa), `qwen2.5:7b` + A2 (70%, 61 s, 5,2 GB, Apache 2.0) e `granite4.2:8b` + A2 (77%, 124 s, 6,6 GB, Apache 2.0). O `install.py` ainda aponta para o 3b. **Passou a ser decidida pela Fase 3** (ver acima) — decidida em 22/09/2026: `qwen2.5:7b` com a biblioteca L1 (decisão 52); `install.py` trocado em 23/09.
  - **Modo de operação do agente = biblioteca recuperada (A2)**; biblioteca inteira no prompt descartada. — Adotado na Fase 3 (condição A2, k = 3) e na decisão 52.
  - **Melhorar o recuperador antes de trocar de modelo**: hit@3 de 79% limita o Granite a 77% (com o verbete certo, 100%). Experimentos baratos e offline: k = 5 (hit@5 já é 90%), sinais em código para a classe de tradução (verbete certo no top-3 em só 47%), embedding denso `embeddinggemma:300m` via `validar_banco.py --embedding`. — **Em aberto em 23/09/2026**: é candidata ao novo plano (Fase 4); o levantamento das LLMs locais (§6.12, decisão 55) já adotou a recuperação híbrida BM25 + embedding pequeno com reordenação. → ficha 11(f).
  - **Validação por código como porta obrigatória da biblioteca** na Fase 3 (achado 4.24: verbete errado é seguido em 93–96% dos casos). — Feita: 30 códigos de rejeição em `evolucao_biblioteca.py`, 658 rejeições na bateria.
- **O `fase2b.log` da máquina-alvo não foi versionado** (`*.log` no `.gitignore`); ele contém a Verificação 0 do i5. Versionar com `git add -f` ou tirar `*.log` da regra para `experimentos/resultados_alvo/`. **O mesmo vale para o `fase3.log`**, que a bateria da Fase 3 grava em `resultados_alvo/fase3/`: sai do commit pela mesma regra, e é o único registro corrido da execução (projeções de tempo, época a época, abortos). Se interessar guardar, é `git add -f`. — **Ainda fora do git em 23/09/2026** (`git ls-files` não lista nenhum dos dois). → ficha 7.
- **Fechada em 11/09/2026 — corrigir os fixtures que contradizem o código** (4.20): os quatro (`sin-1`, `sin-2`, `semt-13`, `efe-13`) foram corrigidos antes de a Fase 3 rodar (decisão 34), com o efeito na recuperação e no pareamento entre fases registrado no fechamento do achado 4.20. **Não é pendência** a imprecisão equivalente dentro da biblioteca original — o verbete `negocio/pagina-produtos-api.md` lista nos `sintomas` a mesma descrição que o código não produz: ela foi mantida de propósito (é a versão L0 de todos os modelos e é a mesma com que a 2-B rodou) e vira alvo de observação na Fase 3.
- **Ablação base × instruct** (`qwen2.5:0.5b-base` × `0.5b-instruct`) como piso metodológico, se a banca pedir um "modelo sem instrução" no lugar do GPT-2. → ficha 11(d).

### Abertas pela Fase 3 (11/09/2026)

<!-- ! Alteração de IA - Revisar: pendência fechada em 21/09/2026 (a bateria rodou em 13–15/09) e bloco novo "Abertas pelo plano complementar (21/09/2026)" ao fim do arquivo.
     ! Motivo: o texto ainda dizia "o Eric decide quando a máquina pode ficar ocupada"; os marcos vêm de `resultados_alvo/fase3/fase3.log` e de `maquina.json` (Ollama 0.34.0; 3 relances = 1 por modelo). -->
- **Fechada em 15/09/2026 — Rodar a bateria da Fase 3** (rodou de 13/09 08:45 a 15/09 18:44: `FIM da Fase 3 - duracao total 58h59 - modelos com falha: nenhum`, 57h59 entre o primeiro e o último marco; 2.088 inferências; Ollama 0.34.0; resultados no commit b9f9ad9). Texto original da pendência: 4 modelos × 3 épocas, 522 inferências por modelo, **~60 h de CPU** na máquina-alvo. O Eric decide quando a máquina pode ficar ocupada; o piloto mede a projeção real antes. A bateria é resumível (época fechada é pulada, época aberta é reconstruída do JSONL), então pode ser partida em pedaços. O piloto de 10 casos do orquestrador rodou em 12/09/2026 (`rodar_fase3.ps1 -Piloto`: `qwen2.5-coder:3b`, 1 época, 00h13, 0 de 6 propostas aceitas; a retomada reconstruiu a `epoca-1` com o mesmo hash); a projeção do executor (`--so-projecao`) para os 4 modelos × 3 épocas é de **67,18 h**, contra ~60 h do plano.
<!-- ! Alteração de IA - Revisar: duas pendências fechadas em 22/09/2026 (relatórios preenchidos; revisão das edições em primeira passada pela IA, a pedido do Eric). ! Motivo: os textos abaixo são os originais; o que restou de cada uma (revisão dos vereditos pelo Eric, regeneração combinada do resumo) está no bloco de 22/09 ao fim do arquivo. -->
- **Fechada em 22/09/2026 — Preencher os relatórios da Fase 3** (§2–§9 e §12 do relatório, §3–§6 da comparação, vereditos no 4.29 e achados 4.30–4.35, mais [`analise-decisoria-modelo-final.md`](3-resultados-e-analises/analise-decisoria-modelo-final.md); tabelas por `gerar_tabelas_relatorio_fase3.py --check`). Texto original: `3-resultados-e-analises/fase-3-relatorio-por-modelo.md` e `comparacao-entre-fases.md` estão pré-registrados com os lugares dos números marcados; cada número sai de `resumo_fase3.json`, `avaliacao_fase3.json` e `comparacao_fases.md`, nenhum digitado à mão. Os vereditos das hipóteses H1–H6 entram no achado 4.29.
- **Fechada em 22/09/2026 (primeira passada pela IA; o Eric revisa) — Revisão humana das edições**. Texto original: o Eric preenche `Correta` / `Parcial` / `Errada` nos arquivos `resultados_alvo/fase3/revisao_edicoes__<modelo>.md` (até 30 edições por modelo) e `avaliar_fase3.py` reapura. A validação em código diz se a edição podia entrar; só a leitura humana diz se ela está certa sobre o sistema.
<!-- ! Alteração de IA - Revisar: pendência fechada em 21/09/2026 (rodada 2 integrada em §6.9.9–6.9.17 e mapa em §6.10). ! Motivo: o Workflow pesquisa-r2 fechou as oito lacunas (146 aprovadas, 6 rejeitadas, 1 além do teto em 153 verificações; 104 referências novas) e a integração foi feita por ferramentas/integrar_pesquisa.py; o texto abaixo é o original da pendência. -->
- **Fechada em 21/09/2026 — Rodada complementar da pesquisa bibliográfica**: as lacunas das oito seções "Lacunas" do levantamento de 11/09/2026 (uma por tópico) não chegaram a ser pesquisadas, por limite de sessão, e continuam adiadas até a onda final da Fase 3 terminar — em 12/09 dois workflows simultâneos derrubaram agentes por limite de sessão, e nada no repositório depende dessa rodada para o Eric commitar. Ficam listadas em [`2-pesquisa-e-literatura/levantamento-2026-09-11-fase-3.md`](2-pesquisa-e-literatura/levantamento-2026-09-11-fase-3.md), para não se perderem.
- **Conferir os capítulos do Faceli 3. ed. (2025) com o exemplar**: a edição e o sumário foram verificados na ficha da editora, mas o conteúdo dos capítulos citados (Cap. 10, avaliação de modelos preditivos, entre outros) não foi lido no livro. Citação com número de página exige o exemplar em mãos (decisão 37). → ficha 11(e).
- **Ollama 0.34.0 — não reverter**: o runtime atualizou sozinho de 0.33.3 (bateria da 2-B) para 0.34.0 em 12/09/2026, antes da bateria da Fase 3 (a máquina é corporativa e a atualização é automática). Decidido não reverter: a Fase 3 roda em 0.34.0, `maquina.json` grava a versão e a decisão 44 a põe em todo registro; o relatório da Fase 3 (§11) e a comparação entre fases declaram a diferença de versão como fator não controlado no pareamento 2-B A2 × F3 L0. Registrado para o Eric saber que a bateria não roda na versão da 2-B. — **Fechada em 23/09/2026**: o Ollama passou a 0.34.1 depois da bateria e a ponte de versão de 21/09 mostrou os três Qwen pareáveis (decisão 47; relatório §11).
- **`Tee-Object` em `rodar_fase2b.ps1` grava o log em UTF-16** (o `fase2b.log` já gravado tem trechos assim, com bytes nulos): é o mesmo defeito encontrado e corrigido em `rodar_fase3.ps1` no piloto de 12/09/2026 (trocado por `ForEach-Object` + `Add-Content -Encoding utf8`). A 2-B está fechada e seus arquivos em `resultados_alvo/` não mudam; aplicar o mesmo patch em `rodar_fase2b.ps1` (só corridas futuras) é decisão do Eric. Os acentos trocados no `fase3.log` do piloto (`recupera├º├úo`) eram outro defeito — o PowerShell decodificava a saída do Python pela codepage do console — e têm correção: a revisão da T12 (12/09) concluiu que `[Console]::OutputEncoding` em UTF-8 resolve, e a onda final de correções pôs `[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)` no `rodar_fase3.ps1`, antes de chamar o Python; conferido no piloto v2 de 13/09/2026 (`fase3.log` novo: 0 bytes nulos e 0 acentos trocados). <!-- ! Alteração de IA - Revisar: em 13/09/2026 "conferir no próximo lançamento" virou o resultado da conferência. ! Motivo: o piloto foi repetido com o .ps1 corrigido e o log saiu legível; deixar a frase antiga mandaria o Eric conferir o que já está conferido. --> Afeta só a legibilidade do log; os JSONL/JSON gravados pelos scripts Python estão em UTF-8 correto. → ficha 8.
- **Cinco referências do projeto ABNT sem URL/DOI** — BISWAS, JÚNIOR, MACIAK, SHI e ZHANG, J.: o endereço não existe em nenhum arquivo do repositório; completar exige localizar a fonte (Eric). — **Localizadas em 23/09/2026** (busca na web; endereços em `4-projeto-de-pesquisa-abnt/correcoes-aplicadas.md` §5.1, item 8); falta conferir a autoria de MACIAK (o artigo é assinado "InstaTunnel") e o Eric aplicar no documento. → ficha 10, item 8.
- **Cronograma (§5) do projeto ABNT sem linha para a Fase 3**: a tabela (Mês 1 a Mês 7) passa de "Mês 2 — configuração do ambiente e da camada de inferência, incluindo a comparação entre portes de modelo" a "Mês 3 — Módulo de Filtragem de Contexto e extração da Accessibility Tree" sem nenhuma linha para a biblioteca gerida pelo modelo, que a §3.2 já descreve (Eric). Sugestão de linha (21/09/2026), para o Eric colar na tabela do §5 entre o Mês 2 e o Mês 3: `| Mês 2 (continuação) | Comparação experimental dos modelos em três fases: prompts sem documentação (2-A), biblioteca de documentação recuperada (2-B) e biblioteca editada pelo próprio modelo em épocas atrás de validação em código (3), com análise decisória do modelo final. |` — Proposta completa (Mês 2 e linha nova) em `correcoes-aplicadas.md` §5.1, itens 1 e 3. → ficha 10, item 3.

### Abertas pelo plano complementar (21/09/2026)

<!-- ! Alteração de IA - Revisar: bloco novo com o que o plano complementar de 21/09/2026 abriu ou deixou para o Eric.
     ! Motivo: o plano vive fora do repositório (`~/.claude/plans/`) e o handoff em `claude-memoria/contexto/`; a lista de pendências precisa dizer sozinha o que falta e quem faz. -->
- **Fechada em 22/09/2026 (primeira passada pela IA) — Revisão humana das 63 edições** (`resultados_alvo/fase3/revisao_edicoes__qwen2.5-coder_3b.md` 10 linhas, `…__qwen2.5-coder_7b.md` 24, `…__qwen2.5_7b.md` 29): o Claude escreveu `Correta` / `Parcial` / `Errada` e um comentário por linha, conferindo contra o código do cobaia (decisão 53). Resultado: 23 / 17 / 23; no `qwen2.5:7b`, 9 / 8 / 12.
- **Versionar os logs das baterias**: `git add -f Programacao/AgenteCore/experimentos/resultados_alvo/fase3/fase3.log Programacao/AgenteCore/experimentos/resultados_alvo/fase2b.log` (decisão do Eric em 21/09; a regra `*.log` do `.gitignore` continua). — Eric. → ficha 7.
- **Fechada em 22/09/2026 — Atualizar o Claude Code**: o Eric atualizou pela própria instalação; o atalho antigo do npm (`%AppData%\npm\claude.ps1`) ficou apontando para um `claude.exe` inexistente — conferir `claude --version` num terminal novo e remover o atalho se ainda estiver no PATH (detalhe no handoff de 22/09). Conferido em 23/09: a extensão roda o binário nativo 2.1.278; o atalho do npm continua quebrado (→ ficha 6). Texto original: (2.1.245 → atual): `claude update` falhou nesta máquina sem acesso ao npm; a estatística de cache do `/usage` só existe a partir da 2.1.251.
- **Fechada em 21/09/2026 à noite, sem o Granite — Ponte de versão do Ollama** (0.34.0 na bateria → 0.34.1): `qwen2.5-coder:3b`, `qwen2.5:7b` e `qwen2.5-coder:7b` nos 36 (b/c 0/0, 0/0 e 1/1; `decisao_modelo.md` §6; relatório §11); o `granite4.2:8b` foi pulado nas duas tentativas (7,8 GB livres contra 8 GB) e o Eric decidiu não insistir (decisão 52): fica sem ponte e fora da 3-B. Texto original: 144 diagnósticos com a biblioteca original nos 36 casos de avaliação, 4 modelos, ~2,5 h, antes de qualquer teste da Fase 3-B; relançar com `powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo ponte -Saida fase3b_ponte` — o script retoma de onde parou.
- **Fechada em 23/09/2026 — Fase 3-B (testes complementares)**: o Eric escolheu o recomendado (decisão 56): (b) troca cruzada e depois (a) casos inéditos; os comandos corrigidos, com as listas separadas por vírgula, estão no README ("Fase 3-B") e na análise decisória §10 — o comando abaixo, com espaços, falhava na vinculação de parâmetros do PowerShell, e `rodar_fase3b.ps1` passou a dividir as listas. Texto original: menu com custo e recomendação em [`analise-decisoria-modelo-final.md`](3-resultados-e-analises/analise-decisoria-modelo-final.md) §10 — (b) troca cruzada primeiro (L1 e L3 do `qwen2.5:7b` lidas pelo Coder 7B e pelo 3B, 144 inferências, ~2,5 h, uma noite: `powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo cruzada -Saida fase3b_cruzada_qwen -Doador qwen2.5:7b -Versoes 1 3 -Modelos qwen2.5-coder:7b qwen2.5-coder:3b`), depois (a) casos inéditos (autoria por agente + 6 casos conferidos pelo Eric, ~3 h de máquina); (c) A5 por último; (d) Granite inviável. — Eric escolhe.
- **Fechada em 23/09/2026 — `install.py` e README apontam para o `qwen2.5-coder:3b` como modelo padrão**: `install.py` passou a baixar `qwen2.5:7b` (a variável `COBAIA_MODELO_LLM` continua mandando); a biblioteca de produção segue na ficha 2 (curadoria). Texto original: a decisão saiu em 22/09/2026 (decisão 52: `qwen2.5:7b` com a biblioteca L1); trocar o padrão de `install.py` para `qwen2.5:7b` e apontar a biblioteca de produção para a cópia L1 curada (item abaixo). — Eric.

### Abertas pela análise decisória (22/09/2026)

<!-- ! Alteração de IA - Revisar: bloco novo com o que a análise decisória e a revisão das edições deixaram para o Eric.
     ! Motivo: a decisão do modelo saiu com dois "depois" que só o Eric fecha — revisar os vereditos que a IA deu e curar a cópia L1 — e o resumo oficial da bateria não é regravado sem combinar. -->
- **Fechada em 23/09/2026 — o Eric aceitou os vereditos como estão.** Texto original: **Revisar os 63 vereditos dados pela IA** nas três planilhas `revisao_edicoes__*.md` (coluna Avaliação e Comentário preenchidos; critério na tag do arquivo e no relatório §7). Trocar o que discordar; a apuração é automática (`decidir_modelo.py` lê as planilhas). — Eric.
- **Regeneração combinada de `resumo_fase3.json` e `relatorio_fase3.html`** com a revisão apurada: `python avaliar_fase3.py --saida fase3` (com `RESULTADOS_DIR=resultados_alvo`, na venv ou no Python do sistema) — só `revisao_humana` e `gerado_em` mudam; conferir com `git diff` antes de commitar. Até lá `decidir_modelo.py` lê as planilhas direto (campo `fonte`). — Eric autoriza; Claude roda. Ensaio feito em 23/09/2026 numa cópia: só `resumo_fase3.json` muda. → ficha 1.
- **Curadoria da cópia L1 do `qwen2.5:7b`** antes da Fase 4: revisar as 30 edições da época 1 que ficaram fora da amostra (a planilha cobre 10 das 40), remover as reprovadas numa **cópia** de `resultados_alvo/fase3/bibliotecas/qwen2.5_7b/epoca-1/` (o snapshot oficial não muda) e registrar o hash da cópia curada; as 3 já reprovadas estão em `analise-decisoria-modelo-final.md` §8. — Eric (a IA pode fazer a primeira passada, como nas 63). Em 23/09 o Eric disse que a cópia L1 "está ok"; falta dizer se fica como está ou se a IA faz a primeira passada. → ficha 2.
- **Commit do working tree de 22/09** (relatórios, análise decisória, achados 4.30–4.35, mapa, decisões 52–54, planilhas, `gerar_tabelas_relatorio_fase3.py`, `tabelas_relatorio.md`, `decidir_modelo.py`, `testar_fase3b.py`, `cache_respostas.py` e teste, `integrar_pesquisa_llms.py`, levantamento das LLMs locais, `resultados_alvo/fase3b_ponte/`; e, se ficarem, `.mcp.json` e `.cbmignore`). — Eric. **Fechada em 22/09/2026**: commit `f86e65d`.
- **codebase-memory-mcp — regra de permanência** (decisão 49): o servidor está instalado (npm, 0.11.0) e registrado em `.mcp.json` (escopo de projeto); na próxima abertura do Claude Code ele pede confirmação. Na primeira sessão com o servidor ativo: indexar o repositório (`.cbmignore` já exclui venvs, `resultados*`, `base_conhecimento`, `.superpowers`, PHPMailer, `Documentacao/`), repetir as três tarefas fixas pelas ferramentas MCP (usos de `TETO_TOKENS_CONTEXTO`; rastro `validar_proposta → aplicar_edicao`; quem lê `fechamento.json`) e comparar com `medir_tokens.py`; fica só com ≥ 20% de economia sem incidente, senão `npm uninstall -g codebase-memory-mcp`, remover `.mcp.json`/`.cbmignore` e registrar em `ferramental-do-claude-code.md` §7.2 (leitura preliminar pela CLI: tendência a sair). — Claude na próxima sessão; Eric decide. **23/09/2026**: o servidor não subiu — `claude mcp list` mostra "Pending approval" e o projeto tem `enabledMcpjsonServers: []`; depende de o Eric aprovar (`/mcp`) ou de `enableAllProjectMcpServers: true` (ferramental §7.2). → ficha 5.
- **Confirmar a instalação do `pyright-lsp`** na próxima abertura (ligado em `.claude/settings.json`); se o marketplace não instalar sozinho, `/plugin` → instalar `pyright-lsp@claude-plugins-official`. — Eric/Claude. **23/09/2026**: não instalou sozinho (não consta em `installed_plugins.json`); precisa do `/plugin install` pelo Eric. → ficha 5.
- **Três scripts da raiz sem BOM e com travessão em comentário** (`build_exe.ps1`, `install.ps1`, `run.ps1`, anteriores à regra do CLAUDE.md): `ferramentas/conferir_docs.py` os reporta como aviso; o parse no Windows PowerShell 5.1 foi conferido em 21/09/2026 (os travessões estão em comentários, não em strings). Decidir se padroniza com BOM ou mantém. — Eric. → ficha 9.
