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

<!-- ! Alteração de IA - Revisar: bloco novo (01/10/2026) com as fichas 17 e 18, abertas no encerramento das Fases 3 e 3-B.
     ! Motivo: o Eric pediu a verificação de que os tópicos das duas fases podem ser dados por concluídos antes do planejamento da Fase 4; a verificação achou duas decisões que só ele pode tomar (o que fazer com as corridas opcionais e com as conferências que ficaram para depois, e se a cópia curada é medida antes de a Fase 4 usá-la). -->
## Abertas em 01/10/2026 (encerramento das Fases 3 e 3-B)

<!-- ! Alteração de IA - Revisar: fichas 17 a 20 fechadas em 06/10/2026 com as respostas do Eric (17 b, 18 a, 19 a, 20 a); o texto das fichas não muda, só o Estado e a Decisão.
     ! Motivo: o Eric respondeu as quatro no chat de 06/10, e a regra é fechar a ficha trocando o Estado e preenchendo a Decisão, nunca apagando; as corridas das fichas 18 e 19 viraram um comando só (sonda com -Versoes 0,1 -Curada), e a sequência de comandos da noite está no roadmap §2 (corrida 12). -->

Com a troca cruzada rodada, todas as corridas previstas da Fase 3-B estão feitas e analisadas (`3-resultados-e-analises/fase-3b-relatorio.md`, com a lista de fechamento no §9). Sobram duas decisões, e nenhuma impede o planejamento da Fase 4.

### 17. Encerrar a Fase 3-B: corridas opcionais e conferências que ficaram para depois
- **Estado:** fechada em 06/10/2026
- **Quem decide:** Eric
- **Aberta em:** 01/10/2026
- **O que é:** Todas as corridas previstas da Fase 3-B rodaram e estão analisadas. Ficaram de fora duas corridas marcadas como opcionais desde o início: a corrida 5 (o modelo recebe documentação errada de propósito, para ver se a biblioteca que ele mesmo escreveu muda a obediência cega; 72 inferências, cerca de 1h20) e a corrida 7 (o Coder 7B nos 36 casos inéditos; 108 inferências, cerca de 2 h). E duas conferências suas que tinham ficado para depois: os 6 casos inéditos de amostra (`lex-16`, `sin-20`, `semt-18`, `tra-19`, `run-20` e `efe-20`, em `banco_casos_ineditos.py`) e a planilha da curadoria da L1 (`resultados_alvo/fase3/curadoria_L1__qwen2.5_7b.md`, 40 linhas; também na aba Curadoria da L1 do painel).
- **Por que importa:** Sem a sua palavra a fase fica quase fechada. As duas corridas não mudam a decisão do modelo, mas a 7 é a única medida que falta no comparativo qwen × Coder. As duas conferências são as únicas partes da 3-B em que nenhuma pessoa olhou o que a IA escreveu (os casos novos) e julgou (30 das 40 avaliações da curadoria). E enquanto alguma corrida puder precisar deles, os dois Coder continuam ocupando 6,6 GB no Ollama.
- **Opções:**
  - (a) Encerrar agora: as opcionais não rodam, as duas conferências ficam como ressalva declarada no relatório da 3-B (limitação 5), e os dois Coder saem do Ollama (`ollama rm qwen2.5-coder:7b qwen2.5-coder:3b`).
  - (b) Encerrar depois de você conferir os 6 casos e a planilha (cerca de uma hora de leitura; basta dizer "ok como está" ou o número das linhas que mudam); as opcionais não rodam.
  - (c) Antes de encerrar, rodar a corrida 7 numa noite (o comando está no roadmap), com ou sem as conferências.
- **Recomendação:** (b). A leitura não bloqueia o planejamento da Fase 4, tira duas ressalvas do relatório, e a planilha decide o que fica na biblioteca que a Fase 4 vai usar. As opcionais não mudam a decisão: o Coder 7B não alcançou o qwen na troca cruzada, e a obediência cega já tem medida na Fase 2-B.
- **Decisão:** (b), em 06/10/2026: o Eric conferiu os 6 casos inéditos de amostra e as 40 linhas da planilha da curadoria ("verifiquei cada um, estão OK"); nenhuma linha muda, e as duas ressalvas saem do relatório da 3-B (§8, limitação 6; §9, linhas 6 e 13). As corridas opcionais 5 e 7 não rodam. Como nenhuma corrida restante usa os dois Coder, eles podem sair do Ollama (`ollama rm qwen2.5-coder:7b qwen2.5-coder:3b`); o comando fica por último na sequência da noite, e é o Eric quem o roda. Em 06/10 à tarde o Eric rodou as duas opcionais mesmo assim (corridas 5 e 7, feitas e analisadas: relatório da 3-B §4.1 e §4.2); o resultado da 7 abriu a ficha 21.

### 18. Medir a cópia curada da L1 antes de a Fase 4 usá-la
- **Estado:** fechada em 06/10/2026
- **Quem decide:** Eric
- **Aberta em:** 01/10/2026
- **O que é:** A biblioteca que a Fase 4 vai usar (`Programacao/AgenteCore/biblioteca_producao/`) é a L1 do `qwen2.5:7b` sem as 17 edições que a curadoria reprovou: ficam 23 das 40. Essa cópia nunca foi medida. O que se mediu foi a L1 inteira: 88,9% de acerto nos 36 casos oficiais e 72,2% nos 36 inéditos, contra 77,8% e 75,0% com a biblioteca original.
- **Por que importa:** A revisão das edições mostrou que o ganho da Fase 3 não pode ser creditado à verdade das notas (achado 4.35), e de onde ele vem não foi isolado; por isso não dá para prever se tirar 17 notas mexe no resultado. E a troca cruzada mostrou que uma nota num verbete muito recuperado muda respostas (achado 4.42). Sem essa medida a Fase 4 começa sem saber quanto a própria biblioteca rende na versão atual do Ollama.
- **Opções:**
  - (a) Rodar agora, numa noite: `qwen2.5:7b` lendo a cópia curada nos 36 casos oficiais e nos 36 inéditos, mais a biblioteca original nos inéditos na versão atual do Ollama (108 inferências, cerca de 2h15). Pede um modo novo no executor da 3-B para ler a pasta da cópia curada, que o Claude escreve e testa antes. A comparação com a L1 inteira, medida na Fase 3, vale porque a ponte de 30/09 deixou o `qwen2.5:7b` dentro do limite (1 caso de diferença em 36).
  - (b) Pôr essa medição como a primeira corrida do plano da Fase 4 (mesma conta, mesmo modo novo).
  - (c) Não medir: a L1 curada entra na Fase 4 como ponto de partida sem número próprio.
- **Recomendação:** (a). É uma noite de máquina, e o resultado pode mudar o que o plano da Fase 4 assume sobre a biblioteca de partida; o planejamento segue enquanto a corrida roda.
- **Decisão:** (a), em 06/10/2026: a cópia curada roda na mesma noite da sonda de confiança (ficha 19), como a versão reservada L100 ("L1 curada" nas análises) de `sonda_confianca.py --curada`, nos 36 casos oficiais e nos 36 inéditos, já com as probabilidades por token; a biblioteca original nos inéditos na versão atual do Ollama sai da mesma corrida (L0 nos 72). Comando único, em `Programacao/AgenteCore/experimentos`: `powershell -ExecutionPolicy Bypass -File rodar_sonda_confianca.ps1 -Versoes 0,1 -Curada` (216 inferências, cerca de 4 h). O modo foi escrito e testado antes (`testar_pre_fase4.py`, 47 testes). Rodou em 06/10/2026 (14:46 a 18:47, 04h01, sem falhas): a cópia curada rende como a L1 inteira (80,6% contra 81,9% nos 72 casos; b/c 1/2) e custa menos (61,1 contra 70,5 s por diagnóstico); relatório da Pré-Fase 4 §4.2, achado 4.50, decisão 71.

## Abertas em 01/10/2026 (Pré-Fase 4)

<!-- ! Alteração de IA - Revisar: bloco novo (01/10/2026) com as duas decisões que a Pré-Fase 4 deixou com o Eric: a noite da sonda de confiança e o custo da parte B da pesquisa bibliográfica.
     ! Motivo: as duas perguntas foram feitas no chat, e a regra do projeto é que toda pendência nova vire ficha aqui, para aparecer no painel na lista do que depende do Eric. Sem as fichas, a corrida 12 e a parte B ficariam paradas sem registro do porquê. -->

### 19. Combinar a noite da sonda de confiança (corrida 12)
- **Estado:** fechada em 06/10/2026
- **Quem decide:** Eric
- **Aberta em:** 01/10/2026
- **O que é:** A corrida 12 mede se a probabilidade que o modelo dá ao rótulo da causa separa acerto de erro. O `qwen2.5:7b` lê a biblioteca L1 dele nos 36 casos oficiais de avaliação e nos 36 inéditos, com o mesmo executor e o mesmo prompt da Fase 3, e o Ollama grava a probabilidade de cada token num arquivo ao lado do registro (`logprobs__L1.jsonl`). O script está pronto e testado (`sonda_confianca.py` e `rodar_sonda_confianca.ps1`). A máquina precisa estar livre: o modelo pede 6,5 GB de RAM livres, e com o VS Code e a sessão do Claude abertos sobram cerca de 5.
- **Por que importa:** É a medição que diz se o agente da Fase 4 pode usar a probabilidade do rótulo para pedir revisão humana. Nos 72 casos o modelo erra cerca de 14 (pelas corridas já feitas com a L1); com tão poucos erros a medida sai com intervalo largo, e por isso a opção de rodar também com a biblioteca original (L0).
- **Opções:**
  - (a) Uma noite com L0 e L1: em `Programacao/AgenteCore/experimentos`, `powershell -ExecutionPolicy Bypass -File rodar_sonda_confianca.ps1 -Versoes 0,1` (144 inferências, cerca de 2h40).
  - (b) Só a L1: o mesmo comando sem `-Versoes` (72 inferências, cerca de 1h15).
  - (c) Não rodar: a Fase 4 fica com os dois sinais que não custam inferência (a causa respondida ser tratada por um verbete do contexto, e a causa respondida ser de uma classe que a rota de busca aponta; relatório da Pré-Fase 4, seções 3.3 e 4.1).
- **Recomendação:** (a). Dobra o número de erros na amostra pelo custo de uma hora e meia a mais na mesma noite. Se a ficha 18 sair como (a), a cópia curada pode entrar na mesma noite.
- **Decisão:** (a), em 06/10/2026: L0 e L1 na mesma noite, junto com a cópia curada da ficha 18. Comando único: `powershell -ExecutionPolicy Bypass -File rodar_sonda_confianca.ps1 -Versoes 0,1 -Curada`. A máquina precisa estar sem o VS Code e sem a sessão do Claude (o script espera 6,5 GB livres); a análise (`analisar_confianca.py`) roda sozinha no fim e o resultado entra no relatório da Pré-Fase 4 e no painel na sessão seguinte. Rodou em 06/10/2026 (216 inferências, 04h01, sem falhas): AUROC 0,783 para a probabilidade conjunta do rótulo, contra 0,541 e 0,626 dos dois sinais grátis; metade dos erros sai confiante, e o sinal vale como triagem, não como barreira; relatório §4.2, achado 4.49.

### 20. Parte B da pesquisa bibliográfica (raciocínio aberto): com que custo
- **Estado:** fechada em 06/10/2026
- **Quem decide:** Eric
- **Aberta em:** 01/10/2026
- **O que é:** A rodada 5 da pesquisa tem duas partes. A parte A (o repositório colibri, as pesquisas que ele cita, inferência com os pesos fora da RAM, modelos MoE pequenos e atlas) rodou e está integrada ao levantamento (§6.14.1 a §6.14.5): 31 agentes e cerca de 1,13 milhão de tokens. A estimativa que dei para as duas partes juntas era de cerca de 1,5 milhão; a parte A sozinha gastou três quartos disso. A parte B são seis tópicos sobre o raciocínio aberto: se o raciocínio escrito é o que decidiu a resposta, formatos de trilha e exigências de registro, relatório para quem desenvolve, atribuição ao contexto, confiança por probabilidade e uso das trilhas para melhorar o sistema.
- **Por que importa:** A especificação da trilha e do relatório para a Fase 4 e a leitura da sonda de confiança se apoiam nessa literatura. O plano aprovado já autoriza a rodada; o que mudou foi o custo, e a regra de economia de tokens é sua.
- **Opções:**
  - (a) Mesmo rigor da parte A: até 16 afirmações verificadas por tópico, cerca de 37 agentes, estimativa de 1,3 milhão de tokens.
  - (b) Até 12 afirmações verificadas por tópico: estimativa de 1,1 milhão de tokens; as que passarem do teto ficam registradas como não verificadas.
  - (c) Só os três tópicos de que a especificação mais depende (formatos de trilha, confiança por probabilidade e uso das trilhas): cerca de metade do custo; os outros três ficam para depois.
- **Recomendação:** (a). A diferença para (b) é de cerca de 15%, e as afirmações além do teto são justamente as que ficariam sem verificação. Se a prioridade for economia, (c) cobre o que a especificação precisa.
- **Decisão:** (a), em 06/10/2026: mesmo rigor da parte A (até 16 afirmações verificadas por tópico, cerca de 37 agentes, estimativa de 1,3 milhão de tokens). O Workflow roda na sessão seguinte à noite de corridas, porque as corridas pedem a máquina sem a sessão do Claude aberta.

<!-- ! Alteração de IA - Revisar: bloco novo (06/10/2026) com a ficha 21, aberta pelo resultado da corrida 7 (o Coder 7B nos 36 inéditos), que o Eric rodou na tarde de 06/10.
     ! Motivo: o comparativo qwen × Coder (§9) tinha deixado escrita a condição que reabriria a decisão 52: "o Coder vencer o qwen nos casos inéditos". Ela se cumpriu em parte, dentro do ruído; o que fazer com isso é decisão do Eric, e a regra do projeto é que toda decisão dele vire ficha. -->
## Abertas em 06/10/2026 (depois das corridas 5 e 7)

<!-- ! Alteração de IA - Revisar: parágrafo novo (22/10/2026) com a resposta do Eric à ficha 21 e, na ficha, a linha Decisão com a escolha dele e o caminho até a corrida; a ficha continua aberta.
     ! Motivo: o Eric escolheu a opção (b), repetir a corrida antes de decidir, na primeira sessão do Claude Code no aplicativo; a ficha só fecha com a leitura dessa corrida, e o painel lê o estado e a decisão daqui. Como o Ollama passou de 0.34.4 (corridas de 06/10) para 0.40.2, a repetição pede uma ponte de versão antes (decisão 47). -->
**Decidido pelo Eric em 22/10/2026:** ficha 21, opção (b): repetir o `qwen2.5-coder:7b` e o `qwen2.5:7b` com a L1 de cada um nos 36 inéditos, numa corrida só, antes de decidir sobre a decisão 52. Como o Ollama já está em 0.40.2 (as corridas de 06/10 rodaram em 0.34.4), entra antes uma ponte de versão com os dois modelos. Os comandos são as corridas 14 e 15 do [roadmap](roadmap.md) §2; a ficha fica aberta até a leitura dessa corrida.

### 21. O Coder 7B ficou à frente nos 36 inéditos: rever a decisão 52?
- **Estado:** fechada em 23/10/2026
- **Quem decide:** Eric
- **Aberta em:** 06/10/2026
- **O que é:** A corrida 7 (`resultados_alvo/fase3b_ineditos_coder7b/`, Ollama 0.34.4) pôs o `qwen2.5-coder:7b` nos mesmos 36 casos inéditos que o `qwen2.5:7b` rodou em 28/09, com a biblioteca original e com as versões que cada um escreveu. Com a biblioteca original, o Coder acerta 83,3% contra 75,0% (b/c 4/1, p = 0,375); com a L1 de cada um, 86,1% contra 72,2% (b/c 6/1, p = 0,125); com a L3, 75,0% contra 80,6% (b/c 1/3). Somando os 36 oficiais da Fase 3 e os 36 inéditos, com a L1 de cada um, o placar é 7/7 (p = 1,00): o que o Coder ganha nos inéditos é o que perde nos oficiais. Por classe com a L1 (6 casos cada), o Coder ganha em lexica, semantica, efeito e empata nas outras. Relatório da 3-B §4.1; comparativo §9; achado 4.52.
- **Por que importa:** O comparativo qwen × Coder (§9, item 4) tinha escrito antes da corrida o que mudaria a decisão 52: "o Coder vencer o qwen nos casos inéditos, ou ler a biblioteca do qwen melhor do que o próprio qwen". A segunda condição não se cumpriu (troca cruzada, 01/10). A primeira se cumpriu em parte: o Coder vence com L0 e L1, por 3 e 5 casos de saldo, e perde com L3; nenhuma diferença passa do efeito mínimo detectável (19,4 pontos nos 36) nem do ruído de uma corrida por condição (de 0 a 3 casos em 36). A decisão 52 saiu da regra pré-registrada nos 36 oficiais, em que o qwen fica à frente em todas as versões; os dois modelos custam o mesmo (cerca de 70 s por diagnóstico) e têm a mesma licença (Apache-2.0). Trocar o modelo agora invalidaria a L1 curada já medida (decisão 71) e a comparação com as fases anteriores.
- **Opções:**
  - (a) Manter a decisão 52 e registrar o resultado como limitação declarada: a regra pré-registrada vale nos 36 oficiais, o resultado nos inéditos fica dentro do ruído, e o plano da Fase 4 ganha o item "mais casos inéditos antes de qualquer troca de modelo" (o Coder 7B entra como candidato declarado para uma reavaliação com mais casos).
  - (b) Antes de decidir, repetir o Coder 7B e o `qwen2.5:7b` com a L1 de cada um nos 36 inéditos, numa corrida só (72 inferências, cerca de 1h30), para saber se o saldo de 5 casos se mantém fora da variação entre corridas.
  - (c) Rever a decisão 52 agora e adotar o Coder 7B com a L1 que ele escreveu: exigiria repetir a curadoria da biblioteca dele, a medição da cópia curada e a sonda de confiança (cerca de duas noites), e deixaria a Fase 4 com um modelo que perde nos 36 oficiais e empata nos 72.
- **Recomendação:** (a). A regra foi fixada antes da bateria para não ser mudada por um resultado dentro do ruído, e é isso que este é; a (b) custa uma noite e, com b/c 6/1, ainda ficaria abaixo do efeito mínimo detectável. O registro honesto (comparativo §9 e achado 4.52) basta para a banca, e a Fase 4 pode reabrir a pergunta com mais casos.
- **Decisão:** (b) em 22/10/2026 e, com a repetição lida, (a) em 23/10/2026 (decisão 73): a decisão 52 fica. As corridas 14 e 15 rodaram em 23/10 (Ollama 0.40.2): na ponte os dois modelos ficaram pareáveis com a Fase 3 (b/c 1/0 nos dois); na repetição dos 36 inéditos com a L1 de cada um, o Coder 7B acertou 83,3% e o qwen2.5:7b 72,2%, b/c 5/1 (p = 0,219), saldo +4 contra +5 na corrida 7, um caso acima da maior variação entre corridas iguais (3 casos); nos 72 casos nunca vistos, 6/7 (empate, como os 7/7 da corrida 7). O saldo se reproduz, mas não separa os dois no teste pareado e some quando os 36 oficiais entram na conta; a regra pré-registrada (decisão 36) decide pelos 36 oficiais, onde o qwen está à frente. Fica como limitação declarada no comparativo (§9.1) e no relatório da 3-B (§4.3), e o plano da Fase 4 ganha o item "mais casos inéditos". Números em `analise_fase3b.json` (blocos `tb_pontes`, `tb_repeticao`, `tb_repeticao_modelos`) e `comparativo_qwen_coder.json`; achado 4.53.

## Abertas em 22/10/2026 (cópia no repositório do orientador)

<!-- ! Alteração de IA - Revisar: bloco novo com a ficha 22, aberta ao preparar a cópia do TCC para o repositório da disciplina (decisão 72).
     ! Motivo: o script de sincronização precisou deixar a `.venv` da CobaiaAPI fora da cópia e, ao fazê-lo, mostrou que ela está rastreada no principal apesar do `.gitignore`; tirá-la do rastreio é comando do Eric (regra do CLAUDE.md), então vira ficha. -->

### 22. A `.venv` da CobaiaAPI está versionada apesar de o `.gitignore` mandar não versionar
- **Estado:** fechada em 23/10/2026
- **Quem decide:** Eric
- **Aberta em:** 22/10/2026
- **O que é:** `Programacao/CobaiaAPI/.venv/` tem 2.113 arquivos rastreados pelo git (`git ls-files Programacao/CobaiaAPI/.venv | wc -l`), embora o `.gitignore` tenha a regra `.venv/` com o aviso de que a pasta grava caminhos absolutos desta máquina (`pyvenv.cfg` com `C:\Python314`) e só tem binários de Windows. A pasta entrou no primeiro commit do repositório (`ab4da6a1`, 31/08/2026), antes da regra, e o `.gitignore` não tira do rastreio o que já estava rastreado. Quem clona recebe a pasta inteira, com um `ruff.exe` de 25 MB, e o `install.py` a recria de qualquer forma. O script `ferramentas/sincronizar_orientador.py` já a deixa fora da cópia do orientador.
- **Por que importa:** dos 4.671 arquivos rastreados, 2.113 são essa venv, que não funciona em outra máquina e confunde quem lê o repositório; e o README, na seção "O que é versionado e por quê", diz que a `.venv` não é versionada.
- **Opções:**
  - (a) Tirar do rastreio sem apagar do disco: `git rm -r --cached Programacao/CobaiaAPI/.venv` e commitar; a pasta continua na máquina e a regra do `.gitignore` passa a valer. O histórico antigo guarda os arquivos (o repositório não encolhe sem reescrever o histórico).
  - (b) Deixar como está e registrar a exceção no `.gitignore` e no README.
- **Recomendação:** (a): é o que o `.gitignore` e o README já dizem; comando único, reversível, e o instalador recria a venv em segundos.
- **Decisão:** (a), pelo Eric em 23/10/2026 (decisão 74): a `.venv` sai do rastreio sem sair do disco. O comando é do Eric, antes do commit: `git rm -r --cached Programacao/CobaiaAPI/.venv` (o Claude não mexe no índice, regra do CLAUDE.md; em 23/10 a tentativa dele foi barrada pelo próprio modo automático). Depois do commit a regra `.venv/` do `.gitignore` passa a valer, o README já descreve a pasta como não versionada e o script de sincronização continua a deixá-la fora da cópia do orientador.

<!-- ! Alteração de IA - Revisar: fichas 23 e 24 abertas em 23/10/2026, depois da parte B da pesquisa da Pré-Fase 4 (nove tópicos em duas ondas), e fechadas no mesmo dia pelo Eric (decisões 77 e 78).
     ! Motivo: a onda 1 virou a especificação da trilha de raciocínio aberta (versão 1), que a Fase 4 implementa e que precisa do aval do Eric; a onda 2 marcou como adiada a saída restrita por gramática que o roadmap §4.1 previa, porque ela muda a probabilidade do rótulo que a trilha usa como sinal, e isso é decisão dele. -->
### 23. Especificação da trilha de raciocínio aberta: aprovar a versão 1 como base da Fase 4
- **Estado:** fechada em 23/10/2026
- **Quem decide:** Eric
- **Aberta em:** 23/10/2026
- **O que é:** A especificação `Documentacao/memorial/5-metodo-e-ferramental/especificacao-trilha-e-relatorio.md` (versão 1, 23/10/2026) diz o que a Fase 4 registra em cada passo do agente: um arquivo JSONL por corrida (esquema versão 2, compatível com o protótipo `trilha.py`, com cabeçalho de corrida e texto grande gravado uma vez por hash); um nó de decisão por decisão (alternativas consideradas, evidência, resultado, contraste "por que esta causa e não a segunda", divergência obrigatória entre o que o modelo declarou e o que o código mediu, probabilidade do rótulo e justificativa em linguagem humana gerada por molde em código); as conferências em código; os testes de intervenção (remover, trocar ou tirar o verbete citado e refazer a inferência) só por gatilho ou numa amostra, porque cada inferência extra custa de 47 a 78 s; a taxonomia de falhas com a origem do defeito (programa, modelo, cura, biblioteca, harness); a regressão por trilha de referência; o aprendizado só por acréscimo validado; o trace do Playwright como evidência do nó que falhou; o relatório por caso em ordem fixa; e a avaliação da própria trilha nos 36 casos de avaliação. Cada escolha vem do mapa de arquitetura da onda 1 da parte B da pesquisa (levantamento §6.14.16: 18 adotadas, 2 adiadas, 10 descartadas) ou do que o projeto já mediu; o que a literatura descartou (segunda chamada ao modelo para explicar, raciocínio antes da resposta, localizar o erro por LLM, OpenTelemetry como formato nativo) está lá com o motivo.
- **Por que importa:** É o desenho que a Fase 4 implementa para abrir o raciocínio do agente, pedido do Eric em 23/10/2026 (tracking de cada decisão e ação com a justificativa em linguagem humana, formando uma árvore navegável, para avaliar o modelo durante o projeto e para o desenvolvedor achar o ponto do erro). Sem o aval, a Fase 4 começaria sem saber o que gravar em cada passo, e cada opção descartada poderia voltar sem o motivo registrado.
- **Opções:**
  - (a) Aprovar a versão 1 como base da Fase 4, com os limiares do selo de probabilidade (alto, médio, baixo) a fixar pela curva risco-cobertura nos 90 casos antes da primeira corrida (seção 14 da especificação).
  - (b) Aprovar com mudanças: dizer quais seções mudam (por exemplo, os gatilhos de intervenção da seção 6.1 ou a ordem do relatório da seção 11) e o que trocar.
  - (c) Devolver para uma versão 2 depois de uma prova de conceito sobre as corridas já gravadas (o `trilha.py` já remonta 3 trilhas e 108 relatórios de caso, 36 por trilha, sem rodar modelo; o número foi corrigido em 26/10/2026, a ficha dizia 111, que é a contagem com os três índices).
- **Recomendação:** (a): a versão 1 só adota o que a literatura verificada e as medições do projeto sustentam, e o que ela deixa em aberto (limiares, tamanho da trilha e do trace) só se mede na Fase 4.
- **Decisão:** (a), pelo Eric em 23/10/2026 (decisão 77): a versão 1 da especificação é a base da Fase 4; os limiares do selo de probabilidade (alto, médio, baixo) saem da curva risco-cobertura nos 90 casos antes da primeira corrida da Fase 4 (seção 14 da especificação).

### 24. Saída restrita por gramática na Fase 4: manter o que o roadmap previa ou adiar, como diz o mapa da onda 2
- **Estado:** fechada em 23/10/2026
- **Quem decide:** Eric
- **Aberta em:** 23/10/2026
- **O que é:** O roadmap (§4.1) prevê, no diagnóstico da Fase 4, saída restrita por gramática (a lista fechada das 23 causas imposta ao modelo por GBNF ou JSON schema do Ollama), herdada do mapa das LLMs locais (decisão 55). O mapa de viabilidade da onda 2 da parte B da pesquisa (levantamento §6.14.16, "Parte B, onda 2") marca essa opção como adiada: nos estudos verificados, a restrição degrada modelos ajustados por instrução e os empurra para alternativas de menor confiança, e a probabilidade do rótulo medida sob gramática não é a mesma que a trilha vai usar como sinal de confiança (§6.14.10). Hoje as quatro linhas da resposta são conferidas em código, sem gramática (conferência `quatro_linhas_presentes` do `trilha.py`).
- **Por que importa:** A probabilidade do rótulo é um campo da trilha (especificação, seções 6.3 e 14) e é o sinal que separa acerto de erro na corrida 12 (AUROC 0,78, relatório da Pré-Fase 4). Se a gramática entrar, o limiar de abstenção e a comparação com as Fases 2-A a 3-B precisam ser refeitos com e sem ela (risco 4 do mapa da onda 2). Se não entrar, a Fase 4 continua dependendo da conferência em código das quatro linhas, que já existe.
- **Opções:**
  - (a) Adiar a gramática: Fase 4 sem decodificação restrita, com a conferência das quatro linhas em código e a probabilidade lida no token do rótulo, como a especificação já prevê; a gramática só volta se o formato inválido passar a custar casos, medido na trilha.
  - (b) Manter a gramática prevista: rodar os 90 casos com e sem ela antes da Fase 4 (cerca de 1h40 por corrida, pela resposta mediana de 66,7 s), comparar acerto e AUROC e recalibrar o limiar.
- **Recomendação:** (a): o formato já é conferido em código, e a gramática mexeria no único sinal interno barato que o projeto tem, sem ganho medido.
- **Decisão:** (a), pelo Eric em 23/10/2026 (decisão 78): a Fase 4 roda sem decodificação restrita; as quatro linhas continuam conferidas em código e a probabilidade é lida no token do rótulo; a gramática só volta se o formato inválido passar a custar casos, medido na trilha. O roadmap §4.1 foi atualizado.

<!-- ! Alteração de IA - Revisar: ficha 25 aberta em 26/10/2026, no fechamento da Pré-Fase 4 (P7).
     ! Motivo: o handoff de 22/10 previa, no fechamento da fase, uma ficha sobre o texto da Pré-Fase 4 para o projeto ABNT, que só se aplica com o sim do Eric; o item 10 do projeto (referencial do TCC final) é o único ainda aberto na entrega, e as sínteses do colibri citam documentos do repositório com letras e títulos inconsistentes, o que precisa ser unificado antes de entrar no texto formal. -->
<!-- ! Alteração de IA - Revisar: ficha 25 fechada em 03/11/2026 pela opção (b), com a mudança de alvo que o Eric pediu (documento do TCC no molde do orientador em vez de versão 5 do projeto de pesquisa); só o Estado e a Decisão mudaram.
     ! Motivo: o Eric respondeu a ficha nesta sessão ("pode seguir a opção B, para termos um novo documento provisório") e pediu o molde do orientador e a norma do próprio documento; sem a Decisão preenchida o painel seguiria mostrando a ficha aberta. -->
### 25. Levar os achados da Pré-Fase 4 ao texto do projeto ABNT: o quê e quando
- **Estado:** fechada em 03/11/2026
- **Quem decide:** Eric
- **Aberta em:** 26/10/2026
- **O que é:** A Pré-Fase 4 produziu três coisas que cabem no texto formal: fundamentação (o levantamento §6.14, 14 tópicos com 617 referências no arquivo, sobre modelos grandes pelo disco, atlas, raciocínio aberto, confiança por probabilidade, memória e visualização), método (a especificação da trilha de raciocínio aberta, versão 1, decisão 77) e resultados (o veredito do colibri, o atlas dos dados do projeto e a sonda de confiança, corrida 12). O projeto de pesquisa ABNT está na versão 4-beta (30/09/2026) e só o item 10 (referencial do TCC final) ficou para a entrega. As sínteses do colibri citam os documentos do repositório `JustVugg/colibri` com letras (2026a, 2026b) e títulos que não batem entre si; para o texto formal, as citações precisam ser unificadas numa entrada ABNT por documento.
- **Por que importa:** Sem decidir o que entra e quando, o material fica só no Memorial, e o texto formal do TCC (a próxima versão do projeto e o TCC final) não cita a literatura verificada nem o desenho da trilha; decidir tarde significa reescrever na entrega.
- **Opções:**
  - (a) Na entrega final do TCC, junto com o item 10: uma seção de fundamentação (raciocínio aberto e confiança por probabilidade), uma de método (a trilha, resumida da especificação) e o veredito do colibri como trabalho relacionado; as citações do repositório unificadas nessa hora. Até lá, nada muda no projeto v4-beta.
  - (b) Agora, numa versão 5 do projeto de pesquisa: as mesmas três partes, com revisão ABNT das citações antes da próxima reunião com o orientador.
  - (c) Só o raciocínio aberto e a confiança entram no texto formal; o colibri e o atlas ficam no Memorial como trabalho avaliado e descartado.
- **Recomendação:** (a): o projeto v4-beta já foi entregue com os itens 1 a 9, e o texto final é quando o referencial se consolida; o Memorial já guarda tudo com as fontes, então nada se perde esperando.
- **Decisão:** (b), pelo Eric em 03/11/2026 (decisão 83), com um acréscimo: o documento provisório sai já no molde do orientador (`Template_TCC_ABNT.docx` e a estrutura de `TCC/README.md` do repositório da disciplina) e na norma do TCC (NBR 14724), não como versão 5 do projeto de pesquisa. A versão 1 é gerada por `ferramentas/gerar_tcc_docx.py` a partir de `Documentacao/TCC - ABNT 14724 - V1.md` (texto com as três partes da ficha e tudo o que as Fases 1 a 4 já mediram, números copiados do Memorial com a origem em comentário), gravada em `Documentacao/TCC_v1_20261103.docx` e copiada para a pasta `TCC/` do clone. A revisão ABNT das citações do colibri e a leitura do grupo ficam para a versão 2, antes da próxima reunião com o orientador.

## Abertas em 26/10/2026 (plano da Fase 4)

<!-- ! Alteração de IA - Revisar: bloco novo com as fichas 26 a 36, abertas ao escrever o plano da Fase 4 (`claude-memoria/plano-aprovado-fase-4.md`, seção 4), uma por decisão que só o Eric pode tomar antes de o código do agente começar.
     ! Motivo: o plano assume a recomendação de cada ficha até a resposta; sem as fichas, as escolhas (sinais de revisão, conjunto de avaliação, modos de injeção, quebra de localizador, k, limiares, verbetes novos, tamanho da trilha, prompt, cobertura da cura, cenários da Fase 5) ficariam só no plano, que o Eric não lê pelo painel. Os números citados vêm dos blocos indicados (`confianca.md`, `experimento_recuperador.md`, relatório da Pré-Fase 4) e de uma contagem por script sobre os bancos de casos em 26/10/2026. -->

<!-- ! Alteração de IA - Revisar: fichas 26 a 36 fechadas em 26/10/2026 com as respostas que o Eric deu uma a uma no quadro da sessão do Claude, no mesmo dia em que aprovou o plano como está: dez pela recomendação (decisão 79) e a 29 pela opção (c), as duas formas de quebra de localizador (decisão 80). Só o Estado e a Decisão de cada ficha mudaram; o caminho do plano no comentário do bloco passou a `claude-memoria/plano-aprovado-fase-4.md`.
     ! Motivo: o Eric pediu as perguntas no quadro em vez do painel; sem a Decisão preenchida, o painel continuaria mostrando as 11 fichas abertas e o plano aprovado apontaria para decisões ainda não registradas. -->
### 26. Sinais de revisão humana: qual manda e o que os outros dois fazem
- **Estado:** fechada em 26/10/2026
- **Quem decide:** Eric
- **Aberta em:** 26/10/2026
- **O que é:** A corrida 12 (06/10) mediu três sinais que o agente calcula sem gabarito para dizer "este diagnóstico merece um humano": a probabilidade que o modelo dá ao rótulo (lida nos tokens da resposta; separa acerto de erro com AUROC 0,783 nos 216 diagnósticos, bloco `tb_conf_resumo` de `resultados_alvo/pre_fase4/confianca.md`), "a causa respondida é tratada por um verbete do contexto" (AUROC 0,541) e "a causa respondida é de uma classe que a rota de busca aponta" (0,626). AUROC é a chance de um erro receber nota pior que um acerto; 0,5 é o mesmo que sortear. Nenhum dos três é barreira: metade dos erros sai confiante. O plano da Fase 4 (seção 4) precisa saber como os três entram na trilha, no relatório e no gatilho de intervenção.
- **Por que importa:** É o que define a ordem da fila de revisão humana e o gatilho de intervenção, que custa de 141 a 234 s por caso disparado; sinal demais manda caso certo para revisão à toa, sinal de menos deixa erro passar.
- **Opções:**
  - (a) A probabilidade manda; os dois sinais grátis só desempatam casos de probabilidade igual e viram aviso no relatório ("a causa respondida não é tratada por nenhum verbete entregue").
  - (b) Só a probabilidade; os outros dois ficam como campo da trilha, sem uso.
  - (c) Os três somados numa nota única, com pesos ajustados nos 90 casos da calibração (corrida 16 do plano).
- **Recomendação:** (a): é o sinal mais forte e o mais barato; os outros dois custam zero e ajudam quem lê o relatório, mas combiná-los numa nota única exigiria ajustar pesos em 90 casos com poucos erros.
- **Decisão:** (a), pelo Eric em 26/10/2026, perguntada no quadro da sessão (decisão 79): a probabilidade do rótulo manda na fila de revisão humana e no gatilho de intervenção; os dois sinais grátis só desempatam probabilidade igual e viram aviso no relatório ("a causa respondida não é tratada por nenhum verbete entregue"). Entra no diagnóstico ao vivo do plano aprovado (seção 3.5, pacote P3).

### 27. Conjunto de avaliação da Fase 4: os 72 casos e quantos inéditos a mais
- **Estado:** fechada em 26/10/2026
- **Quem decide:** Eric
- **Aberta em:** 26/10/2026
- **O que é:** A decisão 73 pede "mais casos inéditos" antes de qualquer troca de modelo, e o roadmap (§7) põe os 72 casos (36 oficiais de avaliação e 36 inéditos) como conjunto de avaliação. Os 72 continuam como estão, lidos do texto. A pergunta é quantos inéditos a mais, escritos por quem e quando. Os 36 inéditos de 23/09 foram escritos por um agente que leu só o código das cobaias; o Eric conferiu 6 (ficha 12) e depois a planilha inteira (ficha 17), sem mudar nenhum. Com os modos novos da ficha 28, casos novos podem nascer já reproduzíveis na tela.
- **Por que importa:** Com 36 casos o efeito mínimo detectável é de 19,4 pontos (resumo oficial da Fase 3, campo `efeito_minimo_detectavel`) e a variação entre corridas iguais é de 0 a 3 casos; sem mais casos, nenhuma diferença pequena da Fase 4 (tela contra texto, k, lotes da biblioteca) se separa do ruído. Escrever casos custa uma sessão de agente e a conferência do Eric.
- **Opções:**
  - (a) Mais 36 inéditos (6 por classe, 2 por nível), escritos por um agente que lê só o código das cobaias e os modos da ficha 28, conferidos pelo Eric antes da primeira corrida medida (corrida 16 do plano); o conjunto de avaliação passa a 108 casos.
  - (b) Só os 72.
  - (c) Mais 18 (3 por classe), conferidos pelo Eric.
- **Recomendação:** (a): o custo é uma sessão de agente e uma conferência; o ganho é um conjunto de 108 casos em que uma diferença de 4 ou 5 casos deixa de ser ruído, e parte dos casos novos nasce reproduzível na tela.
- **Decisão:** (a), pelo Eric em 26/10/2026 (decisão 79): mais 36 inéditos (6 por classe, 2 por nível), escritos por um agente que lê só o código das cobaias e os modos novos da ficha 28, conferidos pelo Eric antes da corrida 16; o conjunto de avaliação passa a 108 casos (pacotes P2 e P3 do plano aprovado).

### 28. Modos de injeção novos na CobaiaAPI: a tela só reproduz 20 dos 72 casos
- **Estado:** fechada em 26/10/2026
- **Quem decide:** Eric
- **Aberta em:** 26/10/2026
- **O que é:** A CobaiaAPI tem sete modos de injeção de falha (`Programacao/CobaiaAPI/app/fault_injection.py`: `normal`, `error_500`, `latency`, `type_drift`, `field_missing`, `field_renamed`, `malformed_json`), ligados por `POST /api/admin/fault-mode`. Contagem por script em 26/10/2026 sobre os bancos de casos e a partição oficial: esses modos produzem 6 das 23 causas da taxonomia; têm uma dessas causas 11 dos 36 oficiais de avaliação, 9 dos 36 inéditos (20 dos 72) e 15 dos 54 de aprendizado; nenhum caso das classes tradução (`escala_ou_unidade_errada`, `chave_de_juncao_errada`, `contagem_inconsistente`) e efeito (`localizador_quebrado`, `estado_da_tela_divergente`) sai de um modo atual. Os outros 52 dos 72 só existem como texto. A CobaiaAPI é do grupo e pode ganhar modos; o front legado não muda.
- **Por que importa:** A Fase 4 é "o agente na tela": com os modos atuais, só 20 dos 72 casos chegam à tela e o resto continua em texto; e a Fase 5 ("cenários cobrindo os modos injetados e a quebra de localizador") ficaria com seis cenários de contrato, todos na mesma página (`produtos_api.php`).
- **Opções:**
  - (a) Um modo novo por causa que a tela consegue mostrar, começando pelas classes sem nenhum modo: `escala_ou_unidade_errada` (preço em centavos), `formato_de_data_divergente` (data do pedido em outro formato), `chave_de_juncao_errada` (tipo de outro produto), `contagem_inconsistente` (lista com um item a menos), `nulo_inesperado`, `valor_fora_do_dominio`, `corpo_vazio`, `corpo_nao_e_json` (HTML com 200), `codificacao_incorreta`, `limite_de_requisicoes` (429), `recurso_inexistente` (404 em id válido), `registro_duplicado`, `estrutura_aninhada_divergente` e `colecao_no_lugar_de_objeto`, cada um com teste em `tests/test_fault_injection.py`; `localizador_quebrado` e `estado_da_tela_divergente` são armados pelo harness no navegador (ficha 29).
  - (b) Manter os sete modos; o resto dos casos fica em texto, declarado como limitação.
  - (c) Só os modos das classes tradução e efeito (as que não têm nenhum).
- **Recomendação:** (a): cada modo é uma função de poucas linhas no mesmo arquivo, com teste; é o que faz a avaliação na tela cobrir as seis classes e dá à Fase 5 cenários fora de uma página só. Ordem de implementação: tradução e efeito primeiro.
- **Decisão:** (a), pelo Eric em 26/10/2026 (decisão 79): a CobaiaAPI ganha um modo novo por causa que a tela consegue mostrar, cada um com teste em `tests/test_fault_injection.py`, começando pelas classes tradução e efeito; `localizador_quebrado` e `estado_da_tela_divergente` ficam com o harness no navegador e com a variante do PHP (ficha 29). Pacote P2 do plano aprovado.

### 29. Quebra de localizador: armada pelo harness no navegador ou variante no PHP
- **Estado:** fechada em 26/10/2026
- **Quem decide:** Eric
- **Aberta em:** 26/10/2026
- **O que é:** A cura de seletor precisa de localizadores quebrados de propósito (o botão "Saiba mais" muda de texto, o grid muda de id, o cartão ganha um contêiner novo). O front PHP legado foi cedido por um integrante e é mantido intocado; ele não tem `data-testid` nem variantes de tela. Duas formas de quebrar: o harness injeta no navegador, antes de a página carregar (`add_init_script` do Playwright), uma mutação determinística do DOM (renomear id, trocar classe, mudar texto, envolver o elemento, reordenar irmãos), uma por cenário; ou o PHP ganha um modo de quebra por parâmetro de URL ou cookie.
- **Por que importa:** Define o realismo dos cenários de "quebra de localizador" da Fase 5 e se o front legado continua intocado.
- **Opções:**
  - (a) Pelo harness, no navegador, com modos determinísticos documentados em `cenarios_fase4.py` e registrados na trilha como evento do programa.
  - (b) Variante no PHP, com o front alterado.
  - (c) Os dois, e o relatório da fase compara.
- **Recomendação:** (a): não toca o legado, é determinístico, vale para as duas cobaias e fica na trilha; a limitação (quebra armada, não ocorrida) fica declarada.
- **Decisão:** (c), pelo Eric em 26/10/2026, diferente da recomendação (decisão 80): as duas formas. O harness arma a quebra no navegador (mutações determinísticas por cenário em `cenarios_fase4.py`, registradas na trilha como evento do programa) e o front PHP legado ganha uma variante de quebra ligada só por parâmetro de URL ou cookie (sem ele, o front se comporta como hoje), documentada; o relatório da fase compara as duas. A regra "front intocado" do plano passa a "front só com a variante de quebra, desligada por padrão"; a cura (seção 3.6, pacote P4), os cenários (pacote P6) e a corrida 19 cobrem as duas formas.

### 30. k da recuperação: 3 (como medido) ou 5
- **Estado:** fechada em 26/10/2026
- **Quem decide:** Eric
- **Aberta em:** 26/10/2026
- **O que é:** k é quantos verbetes a busca entrega ao prompt. Toda medição até hoje usou k = 3. O experimento do recuperador (corrida 9, `resultados_alvo/recuperador/experimento_recuperador.md`, decisão 61) mediu que o verbete certo está entre os 3 primeiros em 80,0% dos 90 casos e entre os 5 primeiros em 91,1% (nos inéditos, 69,4% nos dois). Com k = 5 o prompt cresce (mais dois verbetes de até 550 caracteres) e o tempo de prefill também; a L1 curada custa 61,1 s por diagnóstico com k = 3 (bloco `tb_conf_acerto`).
- **Por que importa:** Muda o custo por caso e pode mudar o acerto; mas trocar k rompe a comparação com as fases anteriores, então precisa de medida própria.
- **Opções:**
  - (a) Medir os dois na calibração (corrida 16 do plano: L1 curada nos 90 com k = 3 e com k = 5, cerca de 1h50 a mais de máquina) e decidir pela regra pré-registrada R8 do plano: k = 5 só se acertar mais por acurácia balanceada com b + c acima de 3; empate fica com k = 3.
  - (b) Fixar k = 5 sem medir.
  - (c) Manter k = 3.
- **Recomendação:** (a): é a única forma de saber se os 11 pontos de hit@5 viram acerto; custa parte de uma noite.
- **Decisão:** (a), pelo Eric em 26/10/2026 (decisão 79): a calibração (corrida 16) roda a L1 curada nos 90 casos com k = 3 e com k = 5; k = 5 só entra pela regra pré-registrada R8 do plano (acurácia balanceada maior, com b + c acima de 3; empate fica com k = 3). Pacotes P0 e P3.

### 31. Limiares do selo de confiança e do gatilho: que parcela vai para revisão humana
- **Estado:** fechada em 26/10/2026
- **Quem decide:** Eric
- **Aberta em:** 26/10/2026
- **O que é:** A especificação da trilha (seções 6.3 e 14, decisão 77) deixa para a Fase 4 fixar os limiares do selo (alto, médio, baixo) e do gatilho de intervenção e de revisão humana pela curva risco-cobertura nos 90 casos: para cada parcela dos casos de menor probabilidade mandada para revisão, quantos erros ela pega e quantos acertos revisa à toa. Na corrida 12, com a L1 curada nos 72 casos (bloco `tb_conf_revisao` de `confianca.md`): revisar 10% (7 casos) pega 4 dos 14 erros e revisa 3 acertos à toa; 20% (14 casos) pega 4 e revisa 10 à toa; 30% (22 casos) pega 7 e revisa 15 à toa, com 14,0% de risco no que sobra. A curva será refeita nos 90 na corrida 16 e os números exatos gravados em `limiares.json`; a decisão aqui é a parcela.
- **Por que importa:** A parcela é o custo de revisão humana aceito por corrida, e a intervenção custa de 141 a 234 s por caso disparado.
- **Opções:**
  - (a) 30%: baixo = os 30% de menor probabilidade (gatilho de intervenção e de revisão), alto = acima da mediana dos acertos, médio = entre os dois.
  - (b) 20%.
  - (c) 10%.
- **Recomendação:** (a): metade dos erros sai confiante (relatório da Pré-Fase 4 §4.2), então uma parcela pequena pega poucos erros; 30% ainda cabe no custo de intervenção (22 casos em 72, cerca de 1 hora de máquina).
- **Decisão:** (a), pelo Eric em 26/10/2026 (decisão 79): 30%. Baixo = os 30% de menor probabilidade (gatilho de intervenção e de revisão humana), alto = acima da mediana dos acertos, médio = entre os dois; os números exatos saem da curva risco-cobertura nos 90 casos na corrida 16 e ficam em `limiares.json` antes da primeira corrida na tela (regra R7). Pacote P3.

### 32. O lugar dos verbetes novos escritos pelo modelo, que a busca nunca entregou
- **Estado:** fechada em 26/10/2026
- **Quem decide:** Eric
- **Aberta em:** 26/10/2026
- **O que é:** A L1 curada (`Programacao/AgenteCore/biblioteca_producao/`) tem 40 verbetes: os 36 originais e 4 escritos pelo modelo na época 1 (pasta `aprendidos/`). O atlas (relatório da Pré-Fase 4 §3.3, tabela `tb_atlas_verbetes`) mostrou que a busca nunca entregou nenhum deles em caso nenhum, em nenhuma corrida: eles só aumentam a biblioteca. O ganho medido da L1 veio das notas acrescentadas a verbetes que já existiam.
- **Por que importa:** Um verbete que nunca é recuperado não ajuda e ainda concorre na busca; apagar é perder o que o modelo escreveu e contraria a regra de só acrescentar.
- **Opções:**
  - (a) Ficam; ganham recuperação pelo id do caso de origem (as notas já carregam `[E1 · caso · …]`) e sinais de busca calculados em código a partir do frontmatter (endpoint, entidade, status); a calibração (corrida 16) mede se passam a ser recuperados; se continuarem em zero, vão para uma pasta de espera (`aprendidos_em_espera/`), fora do índice, sem apagar.
  - (b) Pasta de espera já, sem medir.
  - (c) Removidos da cópia de produção (a época 1 oficial em `resultados_alvo/fase3/` continua intocada).
- **Recomendação:** (a): a recuperação por id é exigida pelo ciclo de correção de qualquer forma, e a medida diz se o problema é o texto do verbete ou a busca; a pasta de espera é o fim previsto se nada mudar.
- **Decisão:** (a), pelo Eric em 26/10/2026 (decisão 79): os 4 verbetes ficam; ganham recuperação pelo id do caso de origem e sinais de busca calculados em código a partir do frontmatter (endpoint, entidade, status); a corrida 16 mede se passam a ser recuperados e, se continuarem em zero, vão para `aprendidos_em_espera/`, fora do índice, sem apagar. Pacote P5.

### 33. Tamanho da trilha e do trace: limites, quando gravar o trace e por quanto tempo guardar
- **Estado:** fechada em 26/10/2026
- **Quem decide:** Eric
- **Aberta em:** 26/10/2026
- **O que é:** A especificação (seção 3.1) manda declarar no cabeçalho de cada corrida os limites da trilha: o tamanho máximo de texto gravado na própria linha (acima disso o texto vai para um arquivo ao lado, citado pelo hash), o número máximo de nós por diagnóstico e por cura, e se o trace do Playwright (a gravação do DOM, da rede e do localizador de cada passo, que o Trace Viewer abre) é gravado sempre ou só quando um passo falha. O tamanho de um trace não tem número oficial (levantamento §6.14.7); as trilhas remontadas das corridas de 36 casos estão em `resultados_alvo/pre_fase4/trilhas/`.
- **Por que importa:** São 218 GB livres no NVMe e nenhum servidor: trace sempre ligado pesa e deixa a corrida mais lenta; trace nunca gravado tira a evidência do nó que falhou.
- **Opções:**
  - (a) Trace só na falha (retain-on-failure), 64 KB por texto na linha, até 40 nós por diagnóstico e 20 por cura, retenção de seis meses das corridas medidas, tudo medido na corrida 17 e gravado no fim de cada corrida.
  - (b) Trace sempre ligado nas corridas de cura e de cenários (evidência completa; custo a medir).
  - (c) Sem trace; só a árvore podada como evidência.
- **Recomendação:** (a): é o que a especificação e o mapa da onda 1 (linha 26) sustentam; os limites são revistos com a medida da corrida 17.
- **Decisão:** (a), pelo Eric em 26/10/2026 (decisão 79): trace só na falha (retain-on-failure), 64 KB por texto na linha (acima disso, arquivo ao lado citado pelo hash), até 40 nós por diagnóstico e 20 por cura, retenção de seis meses das corridas medidas; limites declarados no cabeçalho de cada corrida, medidos na corrida 17 e gravados no fim de cada corrida. Pacotes P1 e P3.

### 34. O prompt do diagnóstico na Fase 4: congelado byte a byte ou versão 2 com os itens da decisão 55
- **Estado:** fechada em 26/10/2026
- **Quem decide:** Eric
- **Aberta em:** 26/10/2026
- **O que é:** O prompt do diagnóstico (`estrategias.linear_com_biblioteca`) está congelado byte a byte desde a Fase 2-A, e o projeto ABNT (§3.4) só compara etapas com prompts idênticos. A decisão 55 adotou dois itens que mudam o prompt (um exemplar resolvido fixo no bloco estável, o "few-shot", e a forma dos rótulos, com o teste do espaço inicial do token) e adiou um terceiro (a ordem do prompt, que conflita com o cache de prefixo). Nenhum foi implementado. A Fase 4 pode manter o prompt congelado ou abrir uma versão 2.
- **Por que importa:** Com o prompt congelado, a Fase 4 compara direto com as Fases 2-A a 3-B e a trilha de referência vale; com a versão 2, toda calibração (limiares, k, lotes da biblioteca) teria de ser refeita e as fases anteriores viram "lado a lado", não diferença testada.
- **Opções:**
  - (a) Congelado na Fase 4 inteira; os itens da decisão 55 viram um experimento em texto nos 90 casos (uma noite a mais, cerca de 1h30), reportado, sem entrar no agente desta fase.
  - (b) Versão 2 medida antes da calibração (os 90 com e sem, cerca de 3h) e adotada se ganhar além de 3 casos.
  - (c) Congelado, e os itens da decisão 55 arquivados como descartados por conflito com a comparabilidade.
- **Recomendação:** (a): preserva a comparabilidade que a banca vai cobrar e ainda mede o que a literatura promete, com um número para a decisão na Fase 5.
- **Decisão:** (a), pelo Eric em 26/10/2026 (decisão 79): o prompt de `estrategias.linear_com_biblioteca` fica congelado byte a byte na Fase 4 inteira; os itens da decisão 55 (exemplar resolvido fixo e forma dos rótulos) viram um experimento em texto nos 90 casos, cerca de 1h30 a mais de máquina, reportado com número para a decisão na Fase 5 e sem entrar no agente desta fase. Pacotes P0 e P3.

### 35. O que a cura cobre nas quebras de contrato: só o diagnóstico ou também a conferência do roteiro
- **Estado:** fechada em 26/10/2026
- **Quem decide:** Eric
- **Aberta em:** 26/10/2026
- **O que é:** O projeto ABNT (§2.1 e §3.4) define Task Success como "fluxo restaurado e roteiro concluído sem erro" e o MTTR como o tempo da detecção até a correção validada na reexecução. Na quebra de localizador isso é direto: o agente acha outro localizador e o roteiro passa. Na quebra de contrato (campo renomeado, tipo trocado, erro 500) o agente não corrige a API (sem patch no código-alvo, escopo decidido): ele diagnostica. Falta dizer o que conta como "correção" nesses cenários.
- **Por que importa:** Define metade dos cenários da Fase 5 e o que o MTTR mede neles; sem a definição, o Task Success dos cenários de contrato seria sempre zero ou sempre ambíguo.
- **Opções:**
  - (a) Só o localizador tem cura; nas quebras de contrato o resultado é o diagnóstico conferido em código (quatro linhas válidas, causa dentro das 23, campo existente no caso), o MTTR mede da detecção até esse diagnóstico e o Task Success nesses cenários é diagnóstico com a causa e o campo certos, declarado assim no texto da Fase 5.
  - (b) O agente também adapta a conferência do roteiro (aceitar `preco_v2` como `preco`, aceitar número em texto) e a reexecução valida: cura de contrato do lado do teste, apresentada como sugestão.
  - (c) As duas medidas lado a lado.
- **Recomendação:** (a): é o escopo decidido (diagnóstico e cura de localizador) e mantém o MTTR comparável entre cenários; a adaptação da conferência (b) esconderia a quebra de contrato que o agente existe para apontar.
- **Decisão:** (a), pelo Eric em 26/10/2026 (decisão 79): só o localizador tem cura; nas quebras de contrato o resultado é o diagnóstico conferido em código (quatro linhas válidas, causa dentro das 23, campo existente no caso), o MTTR mede da detecção até esse diagnóstico e o Task Success nesses cenários é diagnóstico com a causa e o campo certos, declarado assim no texto da Fase 5. Pacotes P4 e P6.

### 36. Os cerca de dez cenários da Fase 5 e a linha de base manual
- **Estado:** fechada em 26/10/2026
- **Quem decide:** Eric
- **Aberta em:** 26/10/2026
- **O que é:** O protocolo (ABNT §3.4) pede cerca de dez cenários com cinco repetições, nas duas cobaias, cobrindo os modos injetados e a quebra de localizador, com o banco restaurado entre execuções, e a linha de base manual: os mesmos cenários resolvidos por integrantes do grupo, cronometrados da apresentação da falha à correção do teste. Nada disso existe ainda (nem a lista de cenários, nem a planilha, nem o script de restauração do banco). A Fase 4 deixa tudo pronto (plano, seção 3.9); a escolha dos cenários e da linha de base é do Eric e do grupo.
- **Por que importa:** É o que a Fase 5 mede; os cenários precisam existir antes do pacote P6 para o ensaio (corrida 21) rodar, e a sessão cronometrada precisa de agenda com os integrantes.
- **Opções:**
  - (a) 10 cenários: 6 de contrato em `produtos_api.php` (um por modo: `error_500`, `latency`, `type_drift` em `preco`, `field_missing` em `preco`, `field_renamed` em `preco`, `malformed_json`) e 4 de localizador no front legado (busca, login do administrador, lista de produtos do administrador, reserva do cliente); linha de base por três integrantes, cada um nos dez cenários, numa sessão agendada com o protocolo escrito.
  - (b) 12 cenários (um por classe de defeito em cada cobaia), usando os modos novos da ficha 28.
  - (c) Decidir depois do ensaio da corrida 21.
- **Recomendação:** (a) como mínimo, trocando cenários de contrato pelos modos novos da ficha 28 que cobrirem mais classes; três integrantes dão três tempos por cenário para a linha de base.
- **Decisão:** (a), pelo Eric em 26/10/2026 (decisão 79): 10 cenários (6 de contrato em `produtos_api.php`, um por modo, e 4 de localizador no front legado: busca, login do administrador, lista de produtos do administrador, reserva do cliente), trocando cenários de contrato pelos modos novos da ficha 28 que cobrirem mais classes; linha de base manual por três integrantes, cada um nos dez cenários, numa sessão agendada com o protocolo escrito. Pacote P6; ensaio na corrida 21.

<!-- ! Alteração de IA - Revisar: bloco novo (01/11/2026) com a ficha 37, aberta pela leitura da corrida 18 (roadmap §2.10).
     ! Motivo: a regra R2 do plano aprovado não foi cumprida e o plano manda rever o molde do sintoma e a poda antes da próxima noite com modelo; a forma da revisão e a repetição da corrida são decisão do Eric, e ele decide pelo painel, que lê esta ficha. Números dos blocos `tb_f4_tela_*` de `resultados_alvo/fase4/tela.json`. -->
## Aberta pela corrida 18 (01/11/2026)

### 37. O caso ao vivo nas falhas de lista: o que levar ao modelo antes de repetir a corrida 18
- **Estado:** fechada em 01/11/2026
- **Quem decide:** Eric
- **Aberta em:** 01/11/2026
- **O que é:** Na corrida 18 (roadmap §2.10) o agente deu o mesmo rótulo ao caso lido da tela e ao caso escrito em só 16 dos 37 casos que reproduzem: acerto de 43,2% na tela contra 83,8% no fixture, b + c = 17 contra o limite 3 da regra R2 (bloco `tb_f4_tela_resumo` de `resultados_alvo/fase4/tela.json`). O mecanismo está no bloco `tb_f4_tela_corpo`: em 22 casos a poda do corpo (`poda.py`, regra `diff_contra_contrato`) não achou diferença de campo contra o contrato do OpenAPI e o CORPO do caso ao vivo levou ao modelo o primeiro produto da lista, normal (`{"id": 1, "nome": "Picanha ao Alho", ...}`); 11 desses viraram `colecao_no_lugar_de_objeto`. Nas falhas de lista (contagem, duplicado, codificação, escala, latência, chave de junção) a diferença não é de campo: é um item a menos ou a mais, um nome com acento estragado, um preço em centavos, uma chamada de 28 segundos. O harness já mede isso na regra R1 (`executar_fase4.py`, modo `reproducao`: "corpo diferente da referência em modo normal", "esperava 14 elementos; viu 13", tempo do cenário), mas `caso_ao_vivo.sintoma_por_molde` e a poda do corpo só olham o contrato e a conferência do roteiro, e em 5 casos o sintoma saiu "Nenhuma diferença medida contra a referência" (`run-2`, `run-9`, `run-19`, `tra-17`, `tra-20`). O caso escrito diz isso em uma linha ("13 itens retornados; falta o id 13"; "sem resposta apos 30s").
- **Por que importa:** O plano aprovado (regra R2) manda rever o molde do sintoma e a poda antes da próxima noite com modelo. Sem a revisão, a Fase 4 mede um agente que lê a tela pior do que lê texto por um defeito do caso de entrada, não do modelo, e o P4 (cura de seletor) e a noite C (biblioteca em produção) herdam o defeito. Repetir a corrida 18 custa 01h24 de máquina.
- **Opções:**
  - (a) Caso ao vivo com o diff contra a referência em modo normal: quando a poda não acha diferença de campo contra o contrato, o CORPO passa a dizer a forma e a contagem da lista contra a referência ("lista com 13 itens; a referência tem 14; falta o id 13", "15 itens; o id 5 aparece duas vezes"), o diff de valores item a item contra o corpo da referência (nome com acento estragado, preço 8990 em vez de 89.9, tipo com id trocado) e o tempo da chamada contra o da referência ("a chamada levou 28,0 s; na referência, 0,02 s"); o sintoma por molde recebe as mesmas frases e, sem diferença medida, continua dizendo que não mediu. Reaproveita a referência de cada cenário que `executar_fase4.py` já guarda. Depois, repetir a corrida 18 em pasta nova (`-Saida fase4_tela_v2`), sem apagar a primeira, e reler a regra R2.
  - (b) Só avisar a forma: acrescentar ao caso ao vivo a linha "FORMA DA RESPOSTA: lista com N itens (a rota devolve uma lista)" e manter o resto; repetir a corrida 18.
  - (c) Aceitar o resultado como limitação declarada e seguir para o P4 sem repetir a corrida 18.
- **Recomendação:** (a): é o que o caso escrito já faz e o que o harness já mede; (b) tira o rótulo de coleção mas deixa o modelo sem o sinal das falhas de lista e de latência; (c) deixaria a Fase 4 medindo o harness, não o agente. Com (a), os limiares do selo ficam os da corrida 16 (o prompt da tela continua maior que o da calibração, e isso fica registrado na leitura).
- **Decisão:** (a), pelo Eric em 01/11/2026, no quadro da sessão. Feito na mesma tarde: `caso_ao_vivo.diff_referencia` compara o corpo com o da referência em modo normal (itens a menos e a mais pelo `id`, repetidos, valores item a item, tempo da chamada contra o orçamento da regra R1); `frases_da_referencia` entra no SINTOMA (sem repetir campo que o diff do contrato já descreveu); `corpo_do_caso` troca o CORPO quando não há diferença de campo contra o contrato (forma, contagem, o que falta, sobra ou se repete, campos diferentes e até dois itens de exemplo; sem diferença, "lista com N itens, igual à referência em modo normal; primeiro item: ..."); `linhas_diff_da_referencia` grava um sinal por diferença no evento de poda do corpo (regra `diff_contra_referencia`), que a justificativa do nó de decisão lê; `executar_fase4.Tela.rodar_caso` passa o corpo e o tempo da referência; `avaliar_fase4.py --tela` aceita `--nome` (a repetição grava `tela_v2.{json,md}` sem regravar a leitura da corrida original). Teste novo em `testar_fase4.py` (37 testes ok) e fumaça sem modelo nos 9 primeiros casos (modo `reproducao`, 41 s): `tra-4` passou a dizer "lista com 13 itens (referência em modo normal: 14); falta o id 14 ("Abacaxi na Brasa")", `run-2` "A chamada levou 28,0 s; na referência em modo normal, 54 ms", `lex-4` "nome diferente em 3 itens" com o item de acento estragado como exemplo, `tra-1` "preco diferente em 14 itens" com o preço 8990.0; os casos com diferença de campo (`sin-5`, `semt-1`) ficaram como estavam. A repetição da corrida 18 (`rodar_fase4.ps1 -Modo tela -Saida fase4_tela_v2 -Nome tela_v2`, cerca de 01h24) espera o sim do Eric; a corrida original fica em `resultados_alvo/fase4_tela/`.

<!-- ! Alteração de IA - Revisar: ficha 38 (01/11/2026, fim da tarde), aberta pela leitura da repetição da corrida 18 (corrida 18b, roadmap §2.10).
     ! Motivo: a regra R2 continua fora do limite de 3 depois da revisão do caso ao vivo, mas por outro motivo; aceitar a corrida, revisar o molde de novo ou rever o limite é decisão do Eric, e ele decide pelo painel. Números dos blocos `tb_f4_tela_*` de `resultados_alvo/fase4/tela_v2.json`. -->
### 38. Regra R2 depois da repetição: aceitar a corrida 18b ou revisar o molde de novo
- **Estado:** fechada em 01/11/2026
- **Quem decide:** Eric
- **Aberta em:** 01/11/2026
- **O que é:** Na repetição da corrida 18 com o caso ao vivo revisado (corrida 18b, roadmap §2.10) o agente dá o mesmo rótulo na tela e no fixture em 26 dos 37 casos (70,3%; eram 16) e acerta 26 na tela (eram 16; o fixture acerta 31); só a tela acerta em 2 e só o fixture em 7 (b + c = 9; p = 0,180; blocos `tb_f4_tela_resumo` e `tb_f4_tela_casos` de `resultados_alvo/fase4/tela_v2.json`). O limite da regra R2 é 3, então ela continua fora do limite, mas o defeito do caso de entrada acabou: nos 22 casos sem diferença de campo contra o contrato, 16 dão o mesmo rótulo (eram 5) e `colecao_no_lugar_de_objeto` cai de 12 para 2 na tela (bloco `tb_f4_tela_corpo`). Os 11 erros que sobram na tela são confusões entre rótulos vizinhos: `tipo_divergente` no lugar de estrutura aninhada (`sin-11`, `sin-21`), de valor fora do domínio (`semt-9`, `semt-20`) e de chave de junção (`tra-17`, `tra-20`); `campo_ausente` para nulo (`semt-17`); `formato_de_data_divergente` para codificação (`lex-8`, `lex-18`); `campo_renomeado` para valor fora do domínio (`semt-21`); `colecao_no_lugar_de_objeto` na latência do detalhe (`run-19`). Em `semt-9` e `tra-17` o fixture erra igual.
- **Por que importa:** O plano aprovado manda rever o molde do sintoma e a poda enquanto a regra R2 estiver fora do limite, antes da noite C. Mas o molde não pode citar a causa (ficha 34, prompt congelado) e as confusões que sobram são de leitura da taxonomia pelo modelo (objeto aninhado lido como tipo errado, nulo lido como campo ausente, acento estragado lido como formato de data), que também aparecem no fixture. Outra repetição custa cerca de 01h30 de máquina, e o P4 e a noite C esperam a decisão.
- **Opções:**
  - (a) Aceitar a corrida 18b como a corrida 18 válida da Fase 4: registrar a regra R2 como não cumprida no limite de 3 (b + c = 9, p = 0,180), com o saldo de +10 acertos na tela contra a corrida original, e seguir para o P4; as confusões restantes ficam como limitação declarada e insumo do P5 (a biblioteca em produção pode ganhar verbetes que separem estrutura aninhada de tipo e nulo de ausente).
  - (b) Terceira revisão do molde, só na forma de descrever, sem citar causa: objeto aninhado ("veio um objeto com as chaves valor e moeda no lugar do número"), nulo ("veio nulo; o campo existe"), valor fora do domínio ("preço negativo", "nome vazio") e chave de junção ("o tipo do item 1 é o do item 3"); repetir a corrida (18c, cerca de 01h30) e reler a regra R2.
  - (c) Rever o limite da regra R2: a variação entre corridas iguais com modelo (3 casos na Fase 3-B) mais os casos em que o fixture também erra.
- **Recomendação:** (a). A regra R2 existe para pegar defeito do caso de entrada; esse defeito foi corrigido e medido. O que sobra é o modelo lendo a taxonomia, e descrever melhor sem citar a causa (b) começa a escrever a resposta no sintoma; (c) muda a regra depois de ver o resultado.
- **Decisão:** (a), pelo Eric em 01/11/2026, no quadro da sessão (decisão 82): a corrida 18b vale como a corrida 18 da Fase 4; a regra R2 fica registrada como não cumprida no limite de 3 (b + c = 9, p = 0,180), com o saldo de +10 acertos na tela contra a corrida original, como limitação declarada da fase; as confusões restantes entre rótulos vizinhos (estrutura aninhada e tipo, nulo e ausente, codificação e formato de data, chave de junção e tipo) são insumo do P5 (biblioteca em produção). Próximo pacote: P4 (cura de seletor e a variante de quebra no front PHP, ficha 29 c). O limite de 3 da regra R2 não muda.

<!-- ! Alteração de IA - Revisar: bloco novo (05/11/2026) com a ficha 39, aberta pela leitura da corrida 22 (roadmap §2.15). Números de `resultados_alvo/fase4/trilha.json`, escritos por script.
     ! Motivo: a divergência que o relatório mostra como carimbo de conflito quase não separou erro de acerto com as intervenções em todos os casos, e mudar o que ela conta muda a especificação (seções 4.2 e 11): é decisão do Eric, e depende da sessão de revisão. -->
## Aberta pela corrida 22 (05/11/2026)

### 39. O carimbo de conflito do relatório: o que ele deve contar depois da corrida 22
- **Estado:** fechada em 05/11/2026
- **Quem decide:** Eric
- **Aberta em:** 05/11/2026
- **O que é:** O relatório de cada caso mostra o carimbo **CONFLITO** quando a divergência do nó de diagnóstico está ligada: uma conferência em código não conferiu, ou uma intervenção mudou o rótulo. Na corrida 22, com as quatro intervenções em todos os 36 casos, ele acendeu em 24: pegou 4 dos 5 erros e acusou 20 dos 31 acertos (TPR x TNR de 0,284, contra 0,250 do acaso). Ele acende tanto porque a documentação pesa na resposta, o que é o esperado: sem documentação nenhuma, o rótulo mudou em 16 de 36 casos. Contado como o agente roda fora da avaliação, com intervenção só quando a probabilidade está baixa ou a FONTE diverge, o carimbo daria 0,542; o selo baixo sozinho, sem nenhuma inferência a mais, dá 0,523. Leitura no roadmap, §2.15.
- **Por que importa:** O carimbo é a primeira coisa que o desenvolvedor lê no relatório (especificação, seção 11). Se ele aparece na maioria dos casos certos, ensina a ignorá-lo. Mas a medida é fraca: são só 5 erros, com o TPR entre 37,6 a 96,4%, e a conta por gatilho é feita sobre uma corrida que não rodou desse jeito.
- **Opções:**
  - (a) Manter a regra como está: fora da avaliação, as intervenções só rodam por gatilho, e o carimbo acende em 6 de 36, com 3 erros e 3 alarmes falsos (TPR x TNR de 0,542). A especificação e o molde não mudam, e o TCC reporta as duas contas. Continua contando como conflito o caso em que só a inferência sem documentação mudou a resposta.
  - (b) Mudar a regra da divergência: o carimbo passa a contar só a conferência em código e a remoção ou a troca do verbete; a inferência sem documentação vira informação na seção da FONTE. Nesta corrida, remoção ou troca dá 0,465, com 13 alarmes falsos. Muda a especificação (seção 4.2) e o molde do relatório.
  - (c) Deixar a divergência como registro na trilha e tirar o carimbo do topo do relatório: a primeira linha passa a avisar pelo selo baixo, e o conflito fica na seção da FONTE. Custa zero inferência. Muda a especificação (seção 11).
- **Depois da sessão (05/11/2026):** a sessão não mediu o carimbo com um leitor humano (decisões 85 e 86). Pelo gabarito, na amostra ele acendeu em 4 dos 5 errados e em 3 dos 6 certos. A opção (b) manteria os 4 errados e deixaria 1 dos 3 alarmes falsos. Na única resposta humana, o Eric aceitou um diagnóstico certo com o carimbo aceso.
- **Conta por gatilho (05/11/2026):** com as intervenções em todos os casos, a regra atual acende em 24 de 36, com 4 erros e 20 alarmes falsos (TPR x TNR de 0,284), e a opção (b), em 18 de 36, com 4 erros e 14 alarmes falsos (TPR x TNR de 0,439). Por gatilho, que é como o agente roda fora da avaliação, a regra atual acende em 6 de 36, com 3 erros e 3 alarmes falsos (TPR x TNR de 0,542); a opção (b), em 5 de 36, com 3 erros e 2 alarmes falsos (TPR x TNR de 0,561); e o selo baixo da opção (c), em 7 de 36, com 3 erros e 4 alarmes falsos (TPR x TNR de 0,523). Bloco `tb_f4_trilha_sinais` de `trilha.md`.
- **Recomendação:** (a). Por gatilho, o carimbo já acende pouco, e a opção (b) só tiraria mais 1 alarme falso, ao custo de mudar a especificação e o molde. Com 5 erros, nenhuma conta separa as opções. Esta recomendação substitui a anterior, de ir para (b), feita antes desta conta. Nada disso impede o P8.
- **Decisão:** (a), pelo Eric em 05/11/2026, no quadro da sessão (decisão 88): a regra fica como está, a especificação e o molde não mudam, e o TCC reporta as duas contas, dizendo que a contagem por gatilho sai de uma corrida que não rodou assim.

<!-- ! Alteração de IA - Revisar: bloco novo (05/11/2026) com as fichas 40 e 41, abertas pelo fechamento da sessão de revisão da corrida 22. Números de `resultados_alvo/fase4/leitura_revisao_trilha.json`, escritos por script.
     ! Motivo: a medida com revisor humano não ficou feita (decisões 85 e 86) e a pré-análise achou dois defeitos da poda; fazer a medida com um colega e mexer na poda antes da Fase 5 são decisões do Eric. -->
## Abertas pelo fechamento da sessão de revisão (05/11/2026)

<!-- ! Alteração de IA - Revisar: ficha 40 reaberta em 05/11/2026 (decisão 95): título, Estado, O que é, Por que importa, Opções, Recomendação e Decisão. O texto da decisão anterior é: "(a), pelo Eric em 05/11/2026, no quadro da sessão (decisão 87): a medida com revisor humano fica como limitação declarada, sem nova sessão".
     ! Motivo: o Eric pediu para deixar em aberto, porque usou a pré-análise por agora e a revisão será feita depois de as respostas serem normalizadas; a ficha fechada diria que não haveria nova sessão. -->
### 40. A medida com revisor humano: em aberto até as respostas serem normalizadas na Pós-Fase 4
- **Estado:** aberta
- **Quem decide:** Eric
- **Aberta em:** 05/11/2026
- **O que é:** A especificação da trilha (seção 12 c) pede, com um revisor humano, a localização do erro, o tempo até a decisão e a adesão apropriada. Na sessão de 05/11, só 1 dos 11 relatórios teve resposta sua, dada antes de ler a pré-análise; os outros 10 são o parecer do Claude, que você aprovou (decisões 85 e 86). O parecer acertou 11 de 11 decisões e 11 de 11 causas. Isso mede um leitor que sabia quantos erros a amostra tem e consultou a biblioteca, não o que o relatório vale para quem lê. A ficha fechou em 05/11 pela opção de declarar como limitação (decisão 87), e você a reabriu no mesmo dia (decisão 95): usou a pré-análise por agora, a revisão será feita, e primeiro as respostas são normalizadas e melhoradas na Pós-Fase 4.
- **Por que importa:** É a única parte do P7 que responde se o relatório ajuda uma pessoa a decidir. Medir agora mediria um formato de resposta que vai mudar. Você já não serve como revisor às cegas dos relatórios 2 a 11 da sessão de 05/11, porque leu o parecer.
- **Opções:**
  - (a) Um colega do grupo faz a sessão às cegas, com os relatórios já no formato da Pós-Fase 4, na mesma página, no encontro da linha de base manual: cerca de 1 hora dele. A página precisa de uma coleção de respostas por revisor e do compartilhamento. Ele recebe só o link da página: a planilha, os arquivos da trilha, a pré-análise e a aba do painel trazem o resultado.
  - (b) Você faz a sessão, com relatórios de casos que ainda não leu e no formato novo, por exemplo uma amostra dos 36 inéditos da corrida 24. É mais simples de marcar, mas você conhece o agente e a biblioteca, e isso entra na leitura.
- **Recomendação:** (a), quando a Pós-Fase 4 fechar o formato. Um leitor que não construiu o agente é o que a medida pede, e o encontro da linha de base manual já vai acontecer.
- **Decisão:** em aberto

### 41. Dois defeitos da poda: corrigir antes da Fase 5 ou deixar como estão
- **Estado:** fechada em 05/11/2026
- **Quem decide:** Eric
- **Aberta em:** 05/11/2026
- **O que é:** A pré-análise achou dois defeitos, conferidos no código e no gabarito. Primeiro: `poda.diff_contrato` só olha o primeiro item de uma lista, então em `sin-5`, onde o segundo item não tem `resumo`, a poda disse "sem diferença" e o agente errou a causa. Segundo: ela chama um número em campo booleano de tipo diferente, enquanto a biblioteca separa `destaque 1` (`tipo_divergente`) de `destaque 2` (`valor_fora_do_dominio`); em `semt-9`, o sinal da poda aponta para o rótulo errado, com selo alto e sem nenhum alarme.
- **O tamanho da mudança:** uma contagem sem modelo, em 05/11/2026, mostra que a poda mudaria em 5 dos 72 casos do banco: 4 pelo primeiro item da lista e 1 pelo booleano. Na corrida 22, 2 dos 5 erros estão nesses casos (`semt-9`, `sin-5`).
- **Por que importa:** O relatório não ajuda a ver esses dois erros. Mas a poda entra no prompt dos casos na tela: corrigir agora faz as corridas seguintes deixarem de ser comparáveis às da Fase 4, embora as já feitas não mudem.
- **Opções:**
  - (a) Corrigir antes da Fase 5, com teste: a poda passa a olhar todos os itens da lista e a seguir a regra da biblioteca para booleano. A Fase 5 registra a mudança, e uma corrida curta só nos casos afetados mede o efeito.
  - (b) Não mexer e declarar como limitação: preserva a comparação com a Fase 4, e os dois defeitos seguem presentes na Fase 5.
- **Recomendação:** (a). São defeitos de código com conserto pequeno e que afetam poucos casos, então o custo em comparabilidade é baixo e fica medido.
- **Decisão:** (a), pelo Eric em 05/11/2026, no quadro da sessão (decisão 89): os dois defeitos foram consertados, com teste, em `poda.diff_contrato`.
- **Correção (05/11/2026):** esta ficha dizia que o conserto mudava o que o modelo recebe, e isso estava errado para os casos de texto. Nos casos de texto, o prompt leva o corpo inteiro e o resultado da poda não chega ao modelo: ela só alimenta a trilha, a tabela do contrato e a justificativa do relatório. Por isso os erros de `sin-5` e `semt-9` na corrida 22 não vieram dos defeitos da poda. Só nos casos na tela o trecho da poda vai ao prompt, e ali nenhum corpo guardado muda. A corrida curta prevista na opção (a) não é necessária. Comparada com a versão anterior, sem modelo, a poda muda em 5 dos 65 casos de texto com contrato (`sin-5`, `semt-9`, `semt-14`, `sin-20`, `semt-17`) e em nenhum dos 209 corpos guardados nas 7 corridas na tela, 158 deles listas com mais de um item, inclusive os cenários da Fase 5 (`resultados_alvo/fase4/poda_antes_e_depois.json`).

<!-- ! Alteração de IA - Revisar: bloco novo (05/11/2026, pacote P8) com as fichas 42 a 45, abertas no fechamento da Fase 4.
     ! Motivo: ao conferir o plano aprovado contra o que rodou, quatro pontos ficaram sem entrega e sem decisão: a regra do tamanho do prompt, o experimento da ficha 34, os 36 inéditos da ficha 27 e o trace, o "Cérebro ao vivo" e o explorador. A decisão é do Eric, e a regra das pendências manda abrir ficha; nenhuma impede a Fase 5. Números de `tela_v2.json`, dos registros das corridas 18b e 21b e de `biblioteca_producao/fechamento.json`, lidos por script. -->
<!-- ! Alteração de IA - Revisar: (05/11/2026, pacote P8) 6 trecho(s) corrigido(s) por script no fechamento da Fase 4, depois da revisão deste documento por um revisor; a lista com o trecho antigo, o novo e o motivo de cada um está em `Documentacao/memorial/5-metodo-e-ferramental/dados/revisao-fase-4-2026-11-05.json`.
     ! Motivo: o plano aprovado (P8) prevê um revisor por documento de texto; as correções entram declaradas, para o texto continuar rastreável. -->
<!-- ! Alteração de IA - Revisar: (05/11/2026) fichas 42 a 45 fechadas com as respostas do Eric no quadro da sessão (decisões 90 a 93); o resto de cada ficha ficou como foi aberta. Os números da ficha 42 vêm de `resultados_alvo/fase4/prompt_tela_blocos.json`, lidos por script.
     ! Motivo: o Eric respondeu uma a uma, e fechar é trocar o Estado e preencher a Decisão; a ficha 42 ganhou a medida porque a opção (b) falava só da poda da árvore, e a árvore sozinha não cabe no limite. -->
## Abertas pelo fechamento da Fase 4 (05/11/2026)

### 42. O prompt na tela passou do limite do plano: declarar como limitação ou apertar a poda antes da Fase 5
- **Estado:** fechada em 05/11/2026
- **Quem decide:** Eric
- **Aberta em:** 05/11/2026
- **O que é:** O plano aprovado (seção 3.3) fixou antes de rodar que o prompt montado da tela não pode passar o maior prompt da calibração em mais de 10%, e que, se passar, a poda aperta antes da próxima corrida. O limite dá 1409 tokens. Na corrida 18b os 37 prompts passaram do limite, o maior com 2034 tokens, e nos dez cenários da corrida 21b 9 de 10 passam do limite. A poda não apertou, e nenhuma decisão tratou disso: a decisão 82 fala só da regra R2.
- **Por que importa:** O MTTR da Fase 5 (tempo da detecção da falha até a correção validada na reexecução) é quase todo o tempo do diagnóstico, e 83,1% desse tempo (mediana da corrida 21b) é o modelo lendo o prompt. Prompt maior é MTTR maior. Além disso, os limiares do selo de confiança foram calibrados com prompts de até 1281 tokens.
- **Opções:**
  - (a) Declarar como limitação e ir para a Fase 5 com o prompt como está.
  - (b) Apertar a poda da árvore antes da Fase 5 e repetir as corridas 18 e 21, cerca de 1h47 de máquina. Isso muda o caso ao vivo pela terceira vez.
  - (c) Mudar o limite da regra, com o motivo escrito.
- **Recomendação:** (a). Os dez cenários acertaram com esse tamanho de prompt, e apertar a poda agora abriria outra revisão do caso ao vivo logo antes da Fase 5. O custo é um MTTR maior, que fica declarado junto com a regra descumprida.
- **Decisão:** (b), pelo Eric em 05/11/2026, no quadro da sessão (decisão 90); a recomendação era (a). O caso ao vivo encurta antes da Fase 5, sem tocar no prompt fixo, e as corridas 18 e 21 são repetidas em pasta nova (18c e 21c, roadmap §2). A medida sem modelo nos prompts guardados (`medir_prompt_tela.py`, `resultados_alvo/fase4/prompt_tela_blocos.json`) mostra que só a árvore não basta: reduzida ao título e ao que difere da referência em modo normal, ela ainda deixa 12 de 37 prompts da corrida 18b e 5 de 10 da 21b acima de 1409 tokens, e sem nenhuma árvore ficam 4 e 1. Tirando também a linha OBSERVAÇÃO ADICIONAL e as listas `faltam` e `sobram` do SINTOMA, sobram 1 e 3, por causa de linhas repetidas e de linhas que a referência podada não tem, que o corte em código trata. Por isso o corte alcança esses dois blocos do caso ao vivo, e isso revê a decisão 82 só no ponto em que ela dizia que o molde do sintoma não passaria por terceira revisão: o molde perde texto e não ganha descrição.

### 43. O experimento da ficha 34 não rodou: rodar antes da Fase 5 ou registrar como não feito
- **Estado:** fechada em 05/11/2026
- **Quem decide:** Eric
- **Aberta em:** 05/11/2026
- **O que é:** A ficha 34, opção (a), manteve o prompt congelado e mandou medir em texto, nos 90 casos, os itens da decisão 55 (exemplar resolvido fixo e forma dos rótulos), cerca de 1h30 de máquina, com número para decidir na Fase 5. O experimento não entrou na tabela de corridas do plano (seção 6), o código não foi escrito e nenhuma corrida o mediu.
- **Por que importa:** A decisão 79 diz que ele seria reportado, e sem ele o TCC não tem número para esses dois itens. O agente não muda em nenhuma das duas opções, porque o prompt continua congelado.
- **Opções:**
  - (a) Escrever e rodar antes da Fase 5: uma sessão de código e cerca de 1h30 de máquina.
  - (b) Registrar como não feito, com o prompt congelado também na Fase 5. Os dois itens ficam como trabalho futuro no TCC.
- **Recomendação:** (b). Mudar o prompt na Fase 5 quebraria a comparação entre as etapas (projeto ABNT §3.4) e pediria nova calibração, então o número ficaria como trabalho futuro, e não como a decisão para a Fase 5 que a ficha 34 previa.
- **Decisão:** (a), pelo Eric em 05/11/2026, no quadro da sessão (decisão 91); a recomendação era (b). O experimento é escrito e roda antes da Fase 5, em texto, nos 90 casos (corrida 23, roadmap §2), em código novo e com o prompt do agente congelado: o número vai para o TCC e não muda o agente, nem na Fase 5. A estimativa de cerca de 1h30 da ficha 34 é de uma condição; medir os dois itens separados são duas condições, cerca de 3 h de máquina.

### 44. Os 36 inéditos da ficha 27: conferir e diagnosticar, ou ficar só na reprodução
- **Estado:** fechada em 05/11/2026
- **Quem decide:** Eric
- **Aberta em:** 05/11/2026
- **O que é:** A ficha 27, opção (a), criou 36 casos inéditos para o conjunto de avaliação chegar a 108 casos, com conferência do Eric antes da corrida 16. Os casos existem (`banco_casos_ineditos_fase4.py`), foram conferidos por script e a corrida 17 os rodou: 25 dos 36 reproduzem na tela. Mas a conferência do Eric não está registrada, e nenhuma corrida com modelo os leu: as corridas 16, 18, 20 e 22 leram outros conjuntos, e os inéditos da regra R5 são os 36 da Fase 3-B.
- **Por que importa:** A biblioteca de produção de agora (`95af35290860`) nunca foi medida em casos inéditos: a regra R5 mediu o lote inteiro (`9f3154eee72d`) nos 36 inéditos da Fase 3-B, antes de a revisão tirar as edições marcadas como erradas, e a corrida 22 leu a produção nos 36 casos de avaliação, que a Fase 3 já tinha usado. Esses 36 são a medida que falta. Sem eles, o TCC fala em 72 casos, não em 108.
- **Opções:**
  - (a) O Eric confere os 36, e uma corrida em texto os diagnostica com a biblioteca de produção: cerca de 40 minutos de máquina, mais uma sessão curta de código, porque hoje só o modo `reproducao` aceita `--banco`.
  - (b) Ficam só na reprodução. O TCC declara os 72 casos e que a biblioteca final não foi medida em casos inéditos.
- **Recomendação:** (a). É a corrida mais barata que sobra e dá a única medida da biblioteca final em casos inéditos.
- **Decisão:** (a), pelo Eric em 05/11/2026, no quadro da sessão (decisão 92): o Eric confere os 36 e, depois da conferência, uma corrida em texto os diagnostica com a biblioteca de produção (corrida 24, roadmap §2), cerca de 40 minutos de máquina, mais uma sessão curta de código. Com ela, o conjunto de avaliação chega aos 108 casos da ficha 27 e sai a medida da biblioteca final em casos inéditos.

### 45. O que o plano previa para a evidência e para o painel e não foi feito: trace na falha, "Cérebro ao vivo" e explorador com a trilha v2
- **Estado:** fechada em 05/11/2026
- **Quem decide:** Eric
- **Aberta em:** 05/11/2026
- **O que é:** Três entregas do plano não saíram. O trace do Playwright gravado só na falha (ficha 33 e plano, seção 3.2): as corridas guardam a árvore, o corpo e os eventos na trilha, mas nenhuma grava trace, e `navegador.py` só traz o comentário que o anuncia. A aba "Cérebro ao vivo" (plano, seções 3.2 e 3.8), com a probabilidade do rótulo, as alternativas e os verbetes regravados num HTML local a cada diagnóstico. E o explorador de casos lendo trilhas v2 (plano, seção 3.8): ele continua lendo só as trilhas da Pré-Fase 4. O Eric tinha dito que detalha a interface para o analista ao fim desta fase (roadmap §7), e é lá que as três cabem.
- **Por que importa:** Nenhuma das três muda número nenhum, e a trilha já guarda o que a árvore de decisão do caso precisa. Mas a ficha 33 decidiu pelo trace, e o TCC não pode dizer que ele existe.
- **Opções:**
  - (a) Juntar as três à interface para o analista, que o Eric especifica agora, para depois da Fase 5, registrando que não foram feitas na Fase 4.
  - (b) Fazer o trace na falha antes da Fase 5, em uma sessão, e o resto como em (a).
  - (c) Descartar as três, com o motivo registrado.
- **Recomendação:** (a). Nada disso muda a medida da Fase 5, e a interface para o analista é o lugar das três.
- **Decisão:** (a), pelo Eric em 05/11/2026, no quadro da sessão (decisão 93): o trace na falha, o "Cérebro ao vivo" e o explorador com a trilha v2 entram na interface para o analista, que o Eric especifica, para depois da Fase 5 (roadmap §7), e ficam registrados como não feitos na Fase 4. A Fase 5 roda sem trace, e o TCC não pode dizer que ele existe: as corridas guardam a árvore, o corpo e os eventos na trilha.

<!-- ! Alteração de IA - Revisar: (06/11/2026) a ficha passa a dizer que a corrida 18e já leu 25 destes casos e a pedir que a conferência olhe o caso, não o resultado.
     ! Motivo: a frase de antes dizia que nenhuma corrida lia esse texto com o modelo, e isso deixou de ser verdade; olhar o resultado antes de mudar um caso contaminaria a corrida 24. -->
<!-- ! Alteração de IA - Revisar: ficha nova em 05/11/2026: a conferência dos 36 inéditos pedida pela decisão 92, com o documento gerado por `gerar_conferencia_ineditos.py` e a pré-análise do Claude.
     ! Motivo: a corrida 24 só roda depois da conferência, e a pergunta precisa estar no painel, onde o Eric decide; os números e os ids vêm de `resultados_alvo/fase4/conferencia_ineditos.json`. -->
<!-- ! Alteração de IA - Revisar: ficha fechada em 06/11/2026 com as respostas do Eric, no quadro da sessão (decisão 100).
     ! Motivo: a resposta libera a corrida 24, e o registro dela é o que a ficha 44 pedia; as respostas ficam em `resultados_alvo/fase4/conferencia_ineditos_respostas.json`. -->
### 46. Os 36 inéditos da ficha 27: a sua conferência antes da corrida 24
- **Estado:** fechada em 06/11/2026
- **Quem decide:** Eric
- **Aberta em:** 05/11/2026
- **O que é:** A decisão 92 manda você conferir os 36 casos antes de a corrida 24 medi-los. O documento está em `resultados_alvo/fase4/conferencia_ineditos.md` (`gerar_conferencia_ineditos.py`) e na aba "Conferência dos inéditos" do painel: cada caso com a requisição, o corpo, o sintoma, o gabarito, o que a corrida 17 viu e a pré-análise. A pré-análise é de um agente do Claude que só leu o código: em 26 casos ela não tem nada a apontar, e aponta estes 10: `lex-27` (`codificacao_incorreta`); `sin-24` (`estrutura_aninhada_divergente`); `semt-26` (`nulo_inesperado`); `semt-27` (`valor_fora_do_dominio`); `tra-27` (`escala_ou_unidade_errada`); `run-26` (`dado_desatualizado`); `run-27` (`registro_duplicado`); `efe-24` (`localizador_quebrado`); `efe-26` (`estado_da_tela_divergente`); `efe-27` (`estado_da_tela_divergente`). Quase todos são casos em que outra causa da lista também caberia; o `run-26` é diferente: a CobaiaAPI não tem cache e grava antes de responder, então ela nunca produz esse corpo (é um cenário descrito, sem modo); e o `semt-26` tem o gabarito `nulo_inesperado` com um contrato que aceita nulo em `resumo`.
- **Por que importa:** Um caso errado mede o modelo contra algo que o sistema não produz, ou contra uma resposta com mais de uma leitura honesta. A corrida 24 é a única medida da biblioteca final em casos inéditos, e o número vai para o TCC. Nenhuma pessoa conferiu esses casos até agora: a ficha 27 previa isso antes da corrida 16, e a conferência não foi registrada (ficha 44). Mudar o texto de um caso não mexe nas corridas 17, 18c, 18d, 21c, 21d e 23, porque nenhuma delas lê esse texto com o modelo. A corrida 18e leu, no caso escrito, os 25 que reproduzem na tela: o caso que mudar roda de novo. Os resultados caso a caso da 18e estão na aba da tela do painel; para a conferência, leia o caso, não o resultado, porque mudar um caso por ter visto que o agente errou nele contaminaria a corrida 24.
- **Opções:**
  - (a) Você lê os 10 apontados com atenção e passa os olhos nos outros 26. Basta dizer "ok como está" ou o id dos que mudam, e o que muda; o que for trocado eu refaço e confiro de novo por script. Pela pré-análise, os pontos que mais pedem a sua palavra são o `run-26` e o `semt-26`.
  - (b) Você lê os 36 com a mesma atenção, como fez com a planilha da curadoria (ficha 17).
  - (c) A pré-análise vale como a conferência: a corrida 24 roda como está, e o TCC declara que os casos foram conferidos por IA, não por uma pessoa.
- **Recomendação:** (a). A pré-análise concentra a sua leitura onde há dúvida, e continua sendo uma pessoa dizendo que os casos estão certos, que é o que a decisão 92 pede. A corrida 24 espera por esta ficha; as corridas 18c, 18d, 18e, 21c, 21d e 23 não dependiam dela e já rodaram.
- **Decisão:** (a), pelo Eric em 06/11/2026, no quadro da sessão (decisão 100): "Ler os 10 apontados", com "Fica como está" em cada um dos 10 e "Ficam como estão" nos outros 26. Nenhum caso mudou, então nenhuma corrida se repete, e a corrida 24 fica liberada. As recomendações que ele viu foram escritas pelo Claude, que já tinha visto os resultados da corrida 18e, e ele as seguiu em todos os casos; a decisão 100 registra isso e as três tensões aceitas, em `semt-26`, `run-26` e `tra-27`.

<!-- ! Alteração de IA - Revisar: ficha nova em 05/11/2026, aberta pela leitura da corrida 18c: a busca na tela recupera o verbete certo menos vezes que no caso escrito.
     ! Motivo: é a única regra da fase ainda não cumprida, e a causa apareceu nesta leitura; a pergunta precisa estar no painel, onde o Eric decide. Os números vêm de `resultados_alvo/fase4/tela_v3.json`, bloco `verbete_certo`. -->
### 47. A busca na tela acha o verbete certo menos vezes: mexer antes da Fase 5 ou deixar como limitação
- **Estado:** fechada em 06/11/2026
- **Quem decide:** Eric
- **Aberta em:** 05/11/2026
- **O que é:** Na corrida 18c, com o prompt dentro do limite, a regra R2 (a que compara a tela com o caso escrito) ainda ficou fora: em 7 casos só um lado acerta, e o limite é 3. A leitura achou a causa principal. Quando o verbete da causa certa está entre os três entregues ao modelo, ele acerta 19 de 21 na tela e 26 de 27 no caso escrito; quando não está, 8 de 16 e 4 de 10. O verbete certo chega em 21 casos na tela e em 27 no caso escrito, porque o sintoma por molde não cita a causa e tem menos termos para a busca que o texto escrito à mão.
- **Por que importa:** É a única regra da fase ainda não cumprida (decisão 82). Mexer pode aproximar os dois lados, mas a busca seria ajustada olhando os mesmos 37 casos que a regra mede, e o número deixaria de ser limpo. Nos dez cenários da Fase 5, a causa saiu certa em todos, então a medida da Fase 5 não depende disso.
- **Opções:**
  - (a) Deixar como está: a regra R2 fica como limitação declarada, com esta explicação no relatório e no TCC.
  - (b) Acrescentar à busca do caso ao vivo sinais em código tirados do que ele já mede contra a referência (por exemplo, acento quebrado ou item faltando na lista), sem escrever nada a mais no prompt. A conferência sem modelo (`conferir_corte_tela.py`, cerca de 2,5 minutos) diz em quantos casos o verbete passa a chegar. Se valer, repetem as corridas 18 e 21 (cerca de 1h30) e os 25 inéditos que reproduzem na tela servem de conferência limpa (cerca de 50 minutos), mais uma sessão de código.
- **Recomendação:** (a). A explicação já é um resultado para o TCC, a Fase 5 não depende disso e o ajuste contaminaria a medida. Se você preferir tentar cumprir a regra, (b) é o caminho, desde que os inéditos façam a conferência.
- **Decisão:** (b), pelo Eric em 06/11/2026, contra a recomendação (decisão 97): "Vamos mexer na busca para tentar ajustar e seguir a regra, se não der, voltamos ao 'ponto seguro' do backup dessa parte". A conferência sem modelo deu o verbete certo em 36 dos 37 casos e em 10 dos 10 cenários. Resultado, em 06/11/2026: na corrida 18d o verbete certo chegou em 36 de 37 casos e o acerto na tela foi de 27 para 32, contra 30 no caso escrito; nos 25 inéditos (corrida 18e), 22 na tela e 18 no caso escrito; os dez cenários não mudaram (corrida 21d). O agente fica com os sinais novos.

<!-- ! Alteração de IA - Revisar: ficha nova em 06/11/2026: como ler a regra R2 se a tela passar a acertar mais que o caso escrito; precisa de resposta antes da corrida 18d.
     ! Motivo: com o verbete certo em 36 dos 37 casos na tela, contra 27 no caso escrito, é provável que a tela passe a acertar casos que o caso escrito erra, e a conta de hoje (b + c) penaliza isso. Decidir depois de ver o resultado seria mudar a regra para caber nele. -->
<!-- ! Alteração de IA - Revisar: (06/11/2026) as fichas 47 e 48 ganham o resultado das corridas 18d, 21d e 18e, lido de `tela_v4.json`, `tela_ineditos.json` e `cenarios_v4.json`.
     ! Motivo: as duas ficaram abertas à espera dessa medida, e quem lê a ficha precisa ver no que deu. -->
<!-- ! Alteração de IA - Revisar: ficha fechada em 06/11/2026 com a resposta do Eric (decisão 98).
     ! Motivo: a resposta veio antes da corrida 18d, que é o que a ficha pedia; sem fechar aqui, o painel continuaria mostrando a pergunta como aberta. -->
### 48. Regra R2: o que conta se a tela passar a acertar mais que o caso escrito
- **Estado:** fechada em 06/11/2026
- **Quem decide:** Eric
- **Aberta em:** 06/11/2026
- **O que é:** A regra R2 se chama "a tela não piora", e a conta usada desde a corrida 18 é b + c até 3: b são os casos que só a tela acerta, e c, os que só o caso escrito acerta. O texto do plano diz que os rótulos "diferem em no máximo 3 casos", sem dizer para que lado. Hoje, na 18c, b = 2 e c = 5. Com os sinais novos, o verbete certo chega em 36 casos na tela e em 27 no caso escrito, e o caso escrito erra 7 dos 37 por conta própria. Se a tela passar a acertar parte deles, b sobe, mesmo com a tela melhor, e a regra pode continuar fora do limite pelo lado bom.
- **Por que importa:** É preciso decidir antes da corrida 18d. Decidir depois de ver o resultado seria mudar a regra para caber nele, e isso não se sustenta no TCC.
- **Opções:**
  - (a) Ler a regra pelo que ela protege: a tela não pode perder mais de 3 casos para o caso escrito (c até 3). O relatório mostra b ao lado e declara que esta leitura foi fixada em 06/11/2026, antes da corrida. Nas corridas antigas nada muda, porque c era 16, 7 e 5.
  - (b) Manter a conta de hoje (b + c até 3). Se a tela passar à frente do caso escrito, a regra fica não cumprida, com a explicação de que foi pelo lado bom.
- **Recomendação:** (a). A regra existe para a tela não piorar: acima do limite, ela manda rever o molde e a poda, e isso não faz sentido quando a tela acerta mais. Os dois números saem sempre juntos, e quem ler o TCC vê as duas contas.
- **Decisão:** (a), pelo Eric em 06/11/2026, no quadro da sessão (decisão 98): "Sim, ler assim (a)". A leitura foi fixada antes da corrida 18d, sem conhecer o resultado dela: a regra conta os casos que a tela perde para o caso escrito (c até 3), e `avaliar_fase4.py --tela` grava as duas contas, `dentro_do_limite_r2` e `dentro_pela_soma`. Nas corridas 18, 18b e 18c o estado é o mesmo: c foi 16, 7 e 5, e a regra fica fora nas duas contas. Resultado, em 06/11/2026: na corrida 18d, c = 3 e b = 5, e na 18e, c = 0 e b = 4; a regra fecha pela leitura fixada, no limite exato, e pela soma dos dois lados (8 e 4) ficaria fora.

## Abertas pela especificação da Pós-Fase 4 (07/11/2026)
<!-- ! Alteração de IA - Revisar: bloco novo (07/11/2026) com as fichas 49 a 54, abertas quando o Eric especificou a Pós-Fase 4 em três partes; todas respondidas por ele no quadro da sessão no mesmo dia (decisões 101 a 106), as seis fechadas.
     ! Motivo: a decisão 94 deixou a fase "a especificar pelo Eric"; a especificação chegou nesta data e trouxe quatro pontos que conflitavam com decisões anteriores (a 93 sobre a interface, a arquitetura local, a 69 e a 95 sobre o que o modelo lê, e o relatório de defeitos da seção 5.5 do syllabus), que precisavam de decisão dele antes de qualquer plano. O plano em rascunho está em `claude-memoria/plano-pos-fase-4.md`, e a pesquisa, no levantamento §6.15. -->

**Decidido pelo Eric em 07/11/2026, no quadro da sessão:** fichas 49 a 54, todas pela opção (a), a recomendada (decisões 101 a 106); o plano da Pós-Fase 4 foi aprovado como está (`claude-memoria/plano-aprovado-pos-fase-4.md`).

### 49. Pós-Fase 4: o hub central é a interface que a decisão 93 deixou para depois da Fase 5. Em que ordem entra cada parte?
- **Estado:** fechada em 07/11/2026
- **Quem decide:** Eric
- **Aberta em:** 07/11/2026
- **O que é:** A parte 1 da especificação pede um hub central à imagem de uma pull request (GitHub e Azure DevOps): a região em revisão à vista, comentários no trecho e na revisão, ativar e rodar os testes, ler respostas e relatórios; e pede a integração com o Git, para o agente ler o que mudou e preparar os testes pelos contratos. A decisão 93 (ficha 45) tinha deixado a interface para o analista (trace na falha, "Cérebro ao vivo", explorador com a trilha v2) para depois da Fase 5. O mesmo pedido traz coisas que mudam o que o analista lê hoje, sem precisar do hub: a barra de progresso, a árvore de decisão, os filtros e a normalização das respostas e a revisão dos verbetes.
- **Por que importa:** A Fase 5 é a medida de valor do TCC e depende de três integrantes; o hub é a maior peça de código do pedido (cerca de quatro sessões). Fazer tudo antes da Fase 5 empurra a medida; fazer tudo depois deixa a medida com revisor humano (decisão 95) à espera de um formato que o hub não precisa para existir.
- **Opções:**
  - (a) Dividir: antes da Fase 5 entram a barra de progresso, a árvore de decisão gerada da trilha, os filtros e a normalização das respostas e a camada de leitura dos verbetes, com a revisão humana da decisão 95; o hub e a integração com o Git são desenhados, pesquisados e têm a viabilidade provada agora, e são construídos depois da Fase 5, como a decisão 93 previa.
  - (b) Tudo antes da Fase 5.
  - (c) Tudo depois da Fase 5, inclusive a normalização das respostas.
- **Recomendação:** (a).
- **Decisão:** (a), pelo Eric em 07/11/2026, no quadro da sessão (decisão 101): "Dividir". No plano (`claude-memoria/plano-aprovado-pos-fase-4.md`, aprovado pela decisão 105; seção 7), os pacotes Q1 a Q5 vêm antes da Fase 5 e Q6 a Q8 depois.

### 50. VM ou servidor para rodar o agente, como o orientador sugeriu, ou tudo local na máquina do dev de QA?
- **Estado:** fechada em 07/11/2026
- **Quem decide:** Eric
- **Aberta em:** 07/11/2026
- **O que é:** O orientador sugeriu rodar o agente numa VM ou num servidor; o Eric acha o custo alto e pediu o contraponto, "tudo roda localmente na máquina do dev de QA", com a ressalva de que "vale a pesquisa e os testes". A pesquisa (levantamento §6.15.5, base E) diz: WSL 2 e Docker Desktop exigem administrador na primeira habilitação; o Hyper-V só existe nas edições Pro e Enterprise; o WSL 2 fica por padrão com metade da RAM (8 GB numa máquina de 16) e retém o cache do modelo até ser desligado; a sobrecarga de CPU medida por terceiros fica entre 5% e 15%. A máquina-alvo é um Windows 11 corporativo sem administrador, com 16 GB e sem GPU, e o Ollama nativo não pede administrador.
- **Por que importa:** A decisão de arquitetura do TCC é o agente na máquina do dev. Uma VM nesta máquina não tem como ser habilitada e tomaria metade da RAM que o modelo usa; num servidor a sugestão é viável, mas muda a arquitetura e o custo de quem adota o agente.
- **Opções:**
  - (a) Fica local: a VM é registrada como "viável só num servidor", com as fontes, e o TCC responde ao orientador com a pesquisa, sem teste de VM nesta máquina.
  - (b) Pedir administrador à empresa e medir o WSL 2 nesta máquina.
  - (c) Mover o agente para um servidor.
- **Recomendação:** (a).
- **Decisão:** (a), pelo Eric em 07/11/2026, no quadro da sessão (decisão 102): "Fica local". Registrado no plano (seção 3.8) e no levantamento §6.15.5.

### 51. Normalizar os verbetes muda o que o modelo lê: mexer na biblioteca de produção ou numa camada de leitura?
- **Estado:** fechada em 07/11/2026
- **Quem decide:** Eric
- **Aberta em:** 07/11/2026
- **O que é:** O Eric disse que os verbetes estão confusos, e a parte 1 pede normalizar e formatar as respostas junto da revisão dos verbetes. Os 40 verbetes de `biblioteca_producao/` (hash `95af35290860`) são o que a busca entrega ao modelo; a decisão 69 diz que trocar o que o modelo lê obriga a medir de novo, e a 95 deixou a revisão humana para depois da normalização. Reescrever os verbetes mudaria o prompt que as corridas 18d, 21d e 24 mediram.
- **Por que importa:** As leituras vigentes (`tela_v4`, `cenarios_v4`, `ineditos`) e os limiares do selo valem para a biblioteca de hoje; uma reescrita obrigaria a repetir as corridas da Fase 4 antes da Fase 5.
- **Opções:**
  - (a) Camada de leitura fora da biblioteca: um arquivo por verbete, gerado por código do frontmatter e das seções e curado à mão, na linguagem da regra do Eric; é o que o relatório, o hub e a revisão humana mostram. A biblioteca e o hash ficam intactos e nenhuma corrida repete.
  - (b) Reescrever os verbetes da biblioteca e repetir as corridas 18d, 21d e 24.
  - (c) Deixar os verbetes como estão e normalizar só o relatório.
- **Recomendação:** (a).
- **Decisão:** (a), pelo Eric em 07/11/2026, no quadro da sessão (decisão 103): "Camada de leitura". Pacote Q1 do plano (seção 3.2); um teste garante que nenhuma leitura entra no prompt.

### 52. O syllabus CTFL 4.0 pede o relatório de defeitos da seção 5.5: adotar como esqueleto do relatório por caso?
- **Estado:** fechada em 07/11/2026
- **Quem decide:** Eric
- **Aberta em:** 07/11/2026
- **O que é:** A parte 2 pede validar o projeto contra o syllabus do ISTQB (tradução do BSTQB, PDF que o professor subiu em 06/11/2026 ao repositório da disciplina) e trazer o que faltar. A leitura (levantamento §6.15.6) mostra que o projeto cabe como teste funcional, caixa-preta e automatizado, de regressão e de confirmação, nos níveis de sistema e de integração de sistema, sobre "tarefas de ponta a ponta" (seção 2.2.1, p. 26). O que o projeto não tinha é o relatório de defeitos da seção 5.5 (p. 50): identificador, título, data, organização e autor, objeto e ambiente de teste, contexto, descrição para reproduzir, esperado e real, severidade, prioridade, estado e referências. O relatório v2 por caso tem seis seções fixas (veredito, evidência, contraste, FONTE, linha de ação, árvore) e não tem metade desses campos.
- **Por que importa:** É a referência de mercado que o professor subiu; adotar o molde dá ao relatório um formato que qualquer analista reconhece e dá ao TCC a citação. Mas o agente não sabe severidade, prioridade nem estado, e pedi-los ao modelo abriria o prompt congelado (decisões 79 e 91).
- **Opções:**
  - (a) Adotar a 5.5 como esqueleto do relatório v3: o código preenche o que sabe (identificador, título, data e autor, objeto e ambiente, contexto, passos para reproduzir, esperado contra real, referências), e severidade, prioridade e estado ficam para o analista, no hub.
  - (b) Manter as seis seções do v2 e só citar a 5.5 no TCC.
  - (c) Pedir ao modelo os campos que faltam.
- **Recomendação:** (a).
- **Decisão:** (a), pelo Eric em 07/11/2026, no quadro da sessão (decisão 104): "Adotar a 5.5". Pacote Q1 do plano (seção 3.1); o v2 continua para as corridas gravadas e o v3 é regerado das trilhas, sem corrida nova.

### 53. Dos oito repositórios, algum vale uma sessão de teste com o Claude Code?
- **Estado:** fechada em 07/11/2026
- **Quem decide:** Eric
- **Aberta em:** 07/11/2026
- **O que é:** Os oito repositórios da parte 3 foram lidos (levantamento §6.15.7 a §6.15.14) e nenhum entra como componente do agente. Dois ficaram como "opcional" para o Claude Code: o Understand-Anything (plugin que monta um grafo do código com Tree-sitter e um modelo de linguagem; `/understand-diff` dá o impacto das mudanças não commitadas; exige Node e uma chave de modelo na nuvem, e o README traz um comentário dirigido a agentes de IA, tratado como dado), uma vez nas cobaias, só para comparar com o mapa por frontmatter do pacote Q7; e o agenttrail (observador local de agentes de programação; só passivo, com Node 20 portátil, sem `init`), para ver a trilha das sessões do Claude Code. O GEPA fica como candidato futuro para o prompt de cura, nunca para o prompt congelado; o mcptoon, como trabalho futuro se os servidores MCP crescerem; eagle-4, rag-anything, dimensional-drawing e claude-obsidian são descartados (o lint de notas órfãs do claude-obsidian vira script).
- **Por que importa:** Cada teste custa uma sessão curta e instala Node e dependências fora da venv; o que fica dele é um parágrafo no TCC ("provado em código" em vez de "lido"). Sem o teste, o veredito de cada um fica como leitura, com as fontes.
- **Opções:**
  - (a) Nenhum: os vereditos ficam como leitura, e o esforço vai para os pacotes Q1 a Q5.
  - (b) Understand-Anything uma vez nas cobaias (uma sessão curta, com chave de modelo na nuvem).
  - (c) agenttrail passivo numa sessão de trabalho (meia sessão).
  - (d) Os dois.
- **Recomendação:** (a). O mapa por frontmatter faz em Python, sem modelo, o que o Understand-Anything faria com um modelo na nuvem, e o TCC já tem o que precisa dos oito: o que são, por que não entram e o que fica de ideia.
- **Decisão:** (a), pelo Eric em 07/11/2026, no quadro da sessão (decisão 106): "Nenhum". Os vereditos dos oito ficam como leitura, com as fontes (levantamento §6.15.7 a §6.15.14 e o mapa §6.15.15), nenhuma sessão de teste é marcada, e o esforço vai para os pacotes Q1 a Q5.

### 54. Aprovar o plano da Pós-Fase 4 como está
- **Estado:** fechada em 07/11/2026
- **Quem decide:** Eric
- **Aberta em:** 07/11/2026
- **O que é:** O rascunho em `claude-memoria/plano-pos-fase-4.md`: as três partes do pedido, os pacotes Q0 a Q8 (Q1 a Q5 antes da Fase 5: relatório v3 no molde da 5.5 e camada de leitura dos verbetes, filtros determinísticos de prolixidade e objetividade, árvore de decisão, barra de progresso, sessão com revisor humano; Q6 a Q8 depois: hub central, integração com o Git, documentação e TCC), as decisões 101 a 104 incorporadas, cerca de 14 sessões de trabalho, máquina só por minutos, nenhuma corrida repetida, prompt e biblioteca intactos.
- **Por que importa:** Pelo acordo do projeto, nenhum código da fase começa antes do plano aprovado, como nas Fases 3 e 4; a Fase 5 fica depois do pacote Q5.
- **Opções:**
  - (a) Aprovar como está: o arquivo vira `plano-aprovado-pos-fase-4.md` e o Q1 começa na próxima sessão.
  - (b) Aprovar com mudanças (dizer quais).
  - (c) Não aprovar: a Pós-Fase 4 fica só com o registro e a pesquisa (Q0), e a Fase 5 vem antes.
- **Recomendação:** (a).
- **Decisão:** (a), pelo Eric em 07/11/2026, no quadro da sessão (decisão 105): "Aprovar como está". O arquivo passou a `claude-memoria/plano-aprovado-pos-fase-4.md`, sem mudança de texto; o pacote Q1 (relatório v3 no molde da seção 5.5 e camada de leitura dos verbetes) começa na próxima sessão, com os testes antes do código.

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
