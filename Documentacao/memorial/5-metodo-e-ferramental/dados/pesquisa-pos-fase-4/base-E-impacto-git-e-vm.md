<!-- ! Alteração de IA - Revisar: arquivo novo (07/11/2026): leitura feita por um subagente do Claude (modelo Sonnet) sobre seleção de testes pelo diff do Git e a máquina virtual sugerida pelo orientador, na rodada 6 da pesquisa (Pós-Fase 4); é um arquivo de dados que ferramentas/integrar_pesquisa_pos_fase4.py lê para montar o levantamento §6.15, e o integrador tira este comentário do texto que entra lá.
     ! Motivo: o Eric pediu em 07/11/2026 a base de pesquisa de cada ponto da Pós-Fase 4 e a validação de oito repositórios do GitHub; a leitura fica versionada como dado para o levantamento ser regerado por script e conferido pelo --check. O texto é o que o subagente escreveu, sem edição, com a marca de confiança que ele deu a cada fonte (aberta e lida; só o resumo de busca; de memória). -->
# Base E: impacto por git e VM (levantamento de 7 nov. 2026)

Convenção: "aberta" = a página ou o PDF foi aberto e lido nesta pesquisa. "Resumo secundário" = só li um resumo de terceiros.

## Ponto 1

### 1.1 Rothermel e Harrold (1997) - aberta (PDF do artigo)

ROTHERMEL, G.; HARROLD, M. J. A safe, efficient regression test selection technique. **ACM Transactions on Software Engineering and Methodology**, v. 6, n. 2, p. 173-210, abr. 1997. DOI 10.1145/248233.248262. Disponível em: https://www.cs.purdue.edu/homes/xyzhang/spring07/Papers/p173-rothermel.pdf. Acesso em: 7 nov. 2026.

- Estabelece: prova que, sob certas condições, o conjunto selecionado inclui todo teste da suíte original capaz de expor falha no programa modificado (seleção "segura"); pode incluir testes que não expõem falha, mas é tão preciso quanto outros algoritmos seguros. Estudos empíricos iniciais indicam redução significativa do custo (o resumo não traz percentual).
- Aplicação: é a definição de "segura" para o desenho: na dúvida, selecionar a mais, nunca a menos. Nosso mapa arquivo-verbete é por convenção (frontmatter), não por prova, então a segurança aqui é só aproximada e precisa de um plano B.

### 1.2 Yoo e Harman (2012) - resumo secundário

YOO, S.; HARMAN, M. Regression testing minimization, selection and prioritization: a survey. **Software Testing, Verification and Reliability**, v. 22, n. 2, p. 67-120, mar. 2012. DOI 10.1002/stvr.430. Disponível em: https://acawiki.org/Regression_testing_minimization,_selection_and_prioritization:_a_survey. Acesso em: 7 nov. 2026.

- Estabelece (segundo o resumo, não o artigo): separa três problemas, minimização, seleção e priorização. Na seleção lista abordagens por firewall em torno dos módulos modificados (conservadora), fluxo de dados, execução simbólica, fatias, grafo de dependência de controle e baseada em projeto. A tentativa de abrir o PDF do Chalmers deu timeout; os números (por exemplo a contagem de artigos) não foram conferidos.
- Aplicação: nossa ligação diff para verbete é uma seleção "baseada em modificação" de granularidade grossa (arquivo), da família do firewall, que o levantamento classifica como conservadora. Citar o artigo original só depois de conferir o PDF.

### 1.3 Gligoric, Eloussi e Marinov (2015), Ekstazi - aberta (resumo no site do autor)

GLIGORIC, M.; ELOUSSI, L.; MARINOV, D. Practical regression test selection with dynamic file dependencies. In: INTERNATIONAL SYMPOSIUM ON SOFTWARE TESTING AND ANALYSIS (ISSTA), 2015, Baltimore. **Proceedings** [...]. New York: ACM, 2015. DOI 10.1145/2771783.2771784. Disponível em: https://users.ece.utexas.edu/~gligoric/papers/abstracts/GligoricETAL15Ekstazi.txt. Acesso em: 7 nov. 2026.

- Estabelece: o Ekstazi liga cada teste aos arquivos de que ele depende (dependência dinâmica, em nível de arquivo) e não exige integração com controle de versão. Em 615 revisões de 32 projetos (cerca de 5 milhões de linhas), cortou o tempo total de teste em 32% em média e 54% nas suítes mais longas. Terminou mais rápido que outras técnicas mesmo selecionando mais testes. Adotado por Apache Camel, Commons Math e CXF.
- Aplicação: dá respaldo à granularidade de arquivo, que é a nossa. A diferença é que o Ekstazi mede a dependência rodando os testes, e nós declaramos a dependência à mão no frontmatter (`arquivos:`, `endpoints:`). Isso é mais barato e mais sujeito a ficar desatualizado.

### 1.4 Azure DevOps Test Impact Analysis - aberta

MICROSOFT. Use Test Impact Analysis. **Microsoft Learn**, Azure Pipelines. Disponível em: https://learn.microsoft.com/en-us/azure/devops/pipelines/test/test-impact-analysis. Acesso em: 7 nov. 2026.

- Estabelece: o TIA seleciona os testes impactados por um commit, mais os que falharam antes e os novos. Tem "fallback seguro": para commits que não entende, roda tudo (exemplo da página: alteração em HTML ou CSS). Ao ver tipo de arquivo desconhecido, roda tudo. Permite rodar tudo em periodicidade configurada (recomendado) e aceita um mapa de dependências escrito à mão, em XML versionado no repositório (variável `TIA.UserMapFile`), que "pode até ser aproximado". Cobre código gerenciado e máquina única. Para validar, sugere rodar os selecionados (T1) e depois todos (T2) e comparar as falhas.
- Aplicação: é a prática de mercado quase idêntica ao desenho: mapa declarado à mão, aproximado, e com rede de segurança. Fixa três regras: arquivo fora do mapa roda tudo, rodada completa periódica, e comparar seleção contra rodada completa para medir o que a seleção perdeu.

### 1.5 Memon et al. (2017), Google - aberta (PDF)

MEMON, A. et al. Taming Google-scale continuous testing. In: INTERNATIONAL CONFERENCE ON SOFTWARE ENGINEERING: SOFTWARE ENGINEERING IN PRACTICE TRACK (ICSE-SEIP), 39., 2017, Buenos Aires. **Proceedings** [...]. Piscataway: IEEE, 2017. p. 233-242. DOI 10.1109/ICSE-SEIP.2017.16. Disponível em: https://huang.isis.vanderbilt.edu/cs4278/readings/googletest.pdf. Acesso em: 7 nov. 2026.

- Estabelece: no TAP do Google, a seleção base é por dependência reversa: regras de build montam a estrutura que devolve todos os alvos de teste que dependem, direta ou indiretamente, dos arquivos modificados (chamados AFFECTED). Marcos chegam a 4,2 milhões de testes assim selecionados. Por dia: mais de 13 mil projetos, 800 mil builds, 150 milhões de execuções de teste. Em média por mudança, menos de 0,5% dos alvos falham, 43% ficam AFFECTED sem rodar e 7,4% são pulados.
- Aplicação: confirma que "arquivo alterado, alvos que dependem dele" é a base também nas grandes empresas, e que a maioria dos testes afetados passa. Aqui o mapa vem do build; o nosso vem do frontmatter.

### 1.6 Machalica et al. (2019), Facebook - aberta (resumo no arXiv)

MACHALICA, M. et al. Predictive test selection. In: INTERNATIONAL CONFERENCE ON SOFTWARE ENGINEERING: SOFTWARE ENGINEERING IN PRACTICE (ICSE-SEIP), 41., 2019, Montreal. **Proceedings** [...]. IEEE, 2019. arXiv:1810.05286. Disponível em: https://arxiv.org/abs/1810.05286. Acesso em: 7 nov. 2026.

- Estabelece: o Facebook já fazia teste baseado em mudança (rodar tudo que pode ser afetado) e achou inviável. Um modelo simples treinado no histórico de resultados escolhe um subconjunto: corta cerca de metade do custo de infraestrutura de teste, mantendo mais de 95% das falhas individuais e mais de 99,9% das mudanças defeituosas reportadas. Trata testes instáveis. A página do arXiv não cita o evento; o ICSE-SEIP 2019 vem do programa da conferência (resultado de busca).
- Aplicação: é a alternativa que não vamos usar (precisa de histórico grande). Serve para dizer que a seleção por dependência é o patamar de partida e que o ganho adicional vem de aprendizado sobre histórico, fora do escopo do TCC.

### O que isso fixa para o desenho

A literatura e a prática sustentam três pontos: (1) selecionar testes pelos arquivos que mudaram no diff, em granularidade de arquivo, é técnica estabelecida (Ekstazi: 32% a 54% menos tempo; Google: dependência reversa de arquivos alterados); (2) o mapa pode ser declarado à mão e aproximado, como o `TIA.UserMapFile` do Azure; (3) a seleção só é aceitável com rede de segurança: arquivo desconhecido ou fora do mapa dispara a bateria inteira, há rodada completa periódica, e a seleção é validada contra a rodada completa (T1 contra T2 do Azure; "segura" em Rothermel e Harrold). Para o agente: diff sem nenhum verbete ligado deve rodar tudo, não nada; registrar a cada rodada o que a seleção deixou de rodar; reconstruir o mapa quando o verbete mudar.

### O que não achei

- Texto do Yoo e Harman aberto (só resumo de terceiros) e números de Rothermel e Harrold (o resumo não os traz; não percorri a seção empírica).
- Documentação do Azure sobre taxa de falsos negativos da seleção.
- Qualquer trabalho que ligue diff a documentação em linguagem natural (verbetes) para selecionar teste. A literatura liga diff a código, cobertura ou dependência de build; a ponte por documentação é nossa e não tem respaldo direto. A busca foi limitada a algumas consultas.
- Taxa de erro de mapas escritos à mão (desatualização). O Azure só diz que o mapa pode ser aproximado.

## Ponto 2

### 2.1 Microsoft, WSL: configuração avançada - aberta

MICROSOFT. Advanced settings configuration in WSL. **Microsoft Learn**, 16 out. 2026. Disponível em: https://learn.microsoft.com/en-us/windows/wsl/wsl-config. Acesso em: 7 nov. 2026.

- Estabelece: a VM do WSL 2 recebe por padrão 50% da memória do Windows e o mesmo número de processadores lógicos; swap padrão de 25% da memória, arredondado para cima em GB. Os limites mudam em `%UserProfile%\.wslconfig` (`memory`, `processors`, `swap`), que não exige administrador no arquivo; exige `wsl --shutdown` para valer.
- Aplicação: com 16 GB instalados (o Windows enxerga 15,69), o padrão dá cerca de 8 GB à VM. O qwen2.5:7b quantizado mais o contexto e o resto do sistema ficam apertados; seria preciso subir `memory` à mão, tirando RAM do navegador de teste, do PHP e do MariaDB que rodam no host.

### 2.2 Microsoft, comparando WSL 1 e 2 - aberta

MICROSOFT. Comparing WSL versions. **Microsoft Learn**. Disponível em: https://learn.microsoft.com/en-us/windows/wsl/compare-versions. Acesso em: 7 nov. 2026.

- Estabelece: o WSL 2 roda um kernel Linux numa "VM utilitária leve" gerenciada, com "pegada de recursos pequena" frente às VMs tradicionais. A memória cresce e encolhe com o uso, mas as páginas em cache não voltam ao Windows até o WSL ser desligado; a página recomenda WSL 1 a quem tem requisitos estritos de memória. Não traz percentual de desempenho em carga de CPU.
- Aplicação: serve para dizer que o custo do WSL 2 em memória é o risco (o cache do modelo de vários GB fica retido), não a CPU. Sem número oficial de sobrecarga de CPU.

### 2.3 Microsoft, instalar o WSL - aberta

MICROSOFT. Install WSL. **Microsoft Learn**. Disponível em: https://learn.microsoft.com/en-us/windows/wsl/install. Acesso em: 7 nov. 2026.

- Estabelece: o comando `wsl --install` deve ser rodado com o PowerShell aberto "em modo administrador", e depois reinicia-se a máquina; ele habilita os recursos do Windows necessários.
- Aplicação: no Windows 11 corporativo sem administrador o WSL 2 não se instala por conta própria; depende do TI. Isso vale também para quem já tem o recurso habilitado por política: aí só falta a distribuição.

### 2.4 Microsoft, FAQ do WSL - aberta

MICROSOFT. FAQ's about Windows Subsystem for Linux. **Microsoft Learn**. Disponível em: https://learn.microsoft.com/en-us/windows/wsl/faq. Acesso em: 7 nov. 2026.

- Estabelece: o WSL 2 usa um subconjunto do Hyper-V (componente "Virtual Machine Platform"), disponível em todas as edições de desktop, inclusive Home; dá erro 0x800704ec quando política de grupo bloqueia o WSL ("contate o administrador"); o WSL foi desenhado para ciclo de desenvolvimento interno, e a VM desliga sozinha quando não há uso.
- Aplicação: política de grupo corporativa pode bloquear o WSL mesmo com a máquina capaz. Para uma bateria de várias horas, o desligamento automático da VM também precisa ser desligado (`vmIdleTimeout`, `instanceIdleTimeout` em 2.1).

### 2.5 Microsoft, requisitos do Hyper-V - aberta

MICROSOFT. System requirements for Hyper-V on Windows and Windows Server. **Microsoft Learn**. Disponível em: https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-requirements. Acesso em: 7 nov. 2026.

- Estabelece: o Hyper-V só liga em Windows 10 ou 11 Professional ou Enterprise; exige processador 64 bits com SLAT, virtualização ligada no BIOS ou UEFI e "ao menos 4 GB de RAM, quanto mais melhor", suficiente para o host e todas as VMs ao mesmo tempo. A página não diz explicitamente que ativar exige administrador (a página de ativação deu 404).
- Aplicação: a exigência de administrador para Hyper-V não foi confirmada na fonte oficial; o recurso do Windows é opcional e na prática vem de quem tem direito de administrador, mas isso é inferência. Nesta máquina o que decide é a edição do Windows e a política do TI.

### 2.6 Docker, instalação no Windows - aberta

DOCKER. Install Docker Desktop on Windows. **Docker Docs**. Disponível em: https://docs.docker.com/desktop/setup/install/windows-install/. Acesso em: 7 nov. 2026.

- Estabelece: instalação por usuário (padrão) não exige administrador para instalar ou atualizar, mas habilitar o WSL 2 pela primeira vez exige, uma vez por máquina. O backend Hyper-V só existe na instalação para todos os usuários, que exige administrador. Requisitos: Windows 10 22H2 ou 11 23H2 em Pro, Enterprise ou Education; processador 64 bits com SLAT, 8 GB de RAM, virtualização ligada. Não serve para Windows Server.
- Aplicação: Docker Desktop sem administrador só se a TI já tiver habilitado o WSL 2 na máquina. O mínimo oficial de 8 GB de RAM é antes de qualquer modelo: o host de 16 GB mal comporta Docker, WSL 2, modelo de 7B e a bateria de testes juntos.

### 2.7 Ollama no Docker - aberta

OLLAMA. Docker. **Ollama Docs**. Disponível em: https://docs.ollama.com/docker. Acesso em: 7 nov. 2026.

- Estabelece: o comando para CPU é `docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama`, sem nenhuma flag de GPU. GPU em contêiner exige NVIDIA Container Toolkit e `--gpus=all` (NVIDIA) ou imagem `rocm` e dispositivos `/dev/kfd` e `/dev/dri` (AMD). Não traz medição nem aviso de desempenho em CPU.
- Aplicação: rodar em contêiner sem GPU é suportado, mas a documentação não quantifica o custo. Aqui não há GPU, então o contêiner não perde aceleração (já não há).

### 2.8 Ollama no Windows e FAQ - abertas

OLLAMA. Windows. **Ollama Docs**. Disponível em: https://docs.ollama.com/windows. Acesso em: 7 nov. 2026.

OLLAMA. FAQ. **Ollama Docs**. Disponível em: https://docs.ollama.com/faq. Acesso em: 7 nov. 2026.

- Estabelece: "A instalação do Ollama não exige Administrador" e vai para o diretório do usuário por padrão; exige Windows 10 22H2 ou superior; a página não fala de RAM nem de CPU. O FAQ diz que "100% CPU" no `ollama ps` significa modelo carregado inteiro em memória do sistema, que a RAM necessária cresce com `OLLAMA_NUM_PARALLEL` vezes `OLLAMA_CONTEXT_LENGTH` e que o padrão de modelos carregados é 3 para CPU. A aceleração por GPU em contêiner vale em Linux ou Windows com WSL 2.
- Aplicação: o caminho nativo atual (Ollama sem administrador, CPU) é o único documentado como possível sem o TI. Cada camada de virtualização acrescentada exige direitos que a máquina não tem. O limite de modelos simultâneos e de paralelismo já controla a memória sem VM.

### 2.9 SiSoftware: desempenho do Hyper-V - aberta (medição de terceiros, não revisada por pares)

SISOFTWARE. Performance impact of Hyper-V virtualisation (Windows 10 Pro) - Compute. Disponível em: https://www.sisoftware.co.uk/?p=2773. Acesso em: 7 nov. 2026.

- Estabelece: num i9-7900X (10 núcleos, 20 threads), Windows 10 em VM Hyper-V com 20 vCPUs e 24 GB (host com 32 GB) ficou entre 3% e 9% mais lenta que o nativo em cargas SIMD e cerca de 10% mais lenta em inteiros (Dhrystone Integer -11%, Long -13%), com extremos de -15% a -23% (redes neurais recorrentes na inferência -13% a -15%, Black-Scholes -18% a -20%). Inferência de redes convolucionais ficou em cerca de -7%. Operações de memória (criptografia) variaram pouco, e o artigo não mede largura de banda de memória.
- Aplicação: é a melhor ordem de grandeza achada para carga de CPU: a VM custa na faixa de 5% a 15%, com cauda ruim. É dado de outro processador, outro sistema e outro tipo de carga, sem LLM; serve só como indicativo, não como previsão para o i5-1235U.

### O que isso fixa para o desenho

Uma VM nesta máquina não é viável hoje, e o motivo principal é de permissão e de memória, não de CPU. Permissão: WSL 2, Hyper-V e Docker Desktop com backend Hyper-V pedem administrador (WSL e Docker na primeira habilitação do WSL 2; Hyper-V pelo conjunto de requisitos e só nas edições Pro e Enterprise); só o Ollama nativo, que o Ollama diz não exigir administrador, roda sem o TI. Memória: o padrão do WSL 2 é 50% da RAM (cerca de 8 GB), o Docker pede 8 GB de mínimo, e a VM mantém cache de páginas sem devolver ao Windows até desligar; com 16 GB e o modelo de 7B mais navegador, PHP e MariaDB no host, sobra pouco. CPU: a sobrecarga medida de VM em carga de CPU é da ordem de 5% a 15%, tolerável, então não é o fator decisivo. Resposta ao orientador, em linguagem de decisão: "viável só num servidor", onde alguém com administrador já mantém a virtualização e a RAM fica dedicada; na máquina do dev de QA, a execução nativa permanece.

### O que não achei

- Medição publicada de inferência de LLM (llama.cpp ou Ollama) em CPU, em VM ou contêiner contra nativo, no Windows. A busca só trouxe blogs sem método; o único número de VM contra nativo para LLM era de Mac com GPU, sem relação com este caso.
- Orientação oficial do Ollama sobre desempenho em VM ou contêiner sem GPU; a documentação só ensina a rodar.
- Medição oficial da Microsoft de sobrecarga de CPU do WSL 2 ou do Hyper-V (o que achei foi a medição de terceiros em 2.9).
- Confirmação oficial de que habilitar o Hyper-V exige administrador (a página de ativação deu 404; a de requisitos não afirma). Para o WSL 2 e o Docker a exigência está confirmada em 2.3 e 2.6.
- Largura de banda de memória em VM, que é o gargalo da inferência em CPU. O artigo de 2.9 remete a um artigo separado que não abri.
- A política real do TI da empresa (se o WSL está bloqueado por política de grupo). Só o administrador sabe.
