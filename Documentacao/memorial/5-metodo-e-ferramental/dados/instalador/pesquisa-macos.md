<!-- ! Alteração de IA - Revisar: arquivo novo (18/11/2026) com o relatório de uma pesquisa na web feita por um subagente do Claude, só de leitura, sobre como testar o instalador em macOS a partir de um PC com Windows (licença da Apple, executores do GitHub Actions, Mac alugado, Homebrew); o texto é o que o subagente entregou, sem reescrita, com a URL e a data de acesso de cada fato e a lista do que não foi confirmado no fim.
     ! Motivo: o Eric pediu em 18/11/2026 o teste dos instaladores em máquina limpa nos três sistemas; as fichas 78 a 82 de `pendencias.md` e o plano do instalador único citam fatos de fora do repositório (licença, preços, versões, requisitos), e a regra do projeto é não escrever fato sem origem. O que está marcado como não confirmado não foi usado como fato nas fichas. -->
# Pesquisa: como testar o instalador em macOS limpo a partir de um PC com Windows 11

Data de acesso de todas as fontes: 18/11/2026. Pesquisa só de leitura. Nenhuma busca continha nome de pessoa, e-mail ou nome de projeto.

Observação de método: algumas páginas oficiais devolveram 403/404 ao leitor automático (Scaleway, MacinCloud, pricing do MacStadium com detalhe, AWS com tabela de preço). Onde isso aconteceu, o fato vem de trecho de busca ou de página de documentação e está marcado como "indireto". Os números de "o que decide" estão marcados como confirmados em página oficial ou como cálculo meu.

---

## 1. Licença do macOS e virtualização

Fonte: contrato "Software License Agreement for macOS Tahoe 26", PDF oficial da Apple, edição EA1955, data impressa 07/11/2025 (versão em inglês).
URL: https://www.apple.com/legal/sla/docs/macOSTahoe.pdf (acessado em 18/11/2026; texto extraído do PDF baixado).

- Cláusula 2.A (licença de cópia única, vale para o macOS pré-instalado ou obtido fora da Mac App Store): uma cópia "em um único computador da marca Apple" por vez.
- Cláusula 2.B(iii) (licença da Mac App Store / download automático): permite instalar e rodar até duas (2) cópias ou instâncias adicionais do macOS em ambientes virtuais, em cada computador da marca Apple que o licenciado possua ou controle e que já esteja rodando o macOS. Finalidades permitidas: (a) desenvolvimento de software; (b) teste durante o desenvolvimento de software; (c) uso do macOS Server; (d) uso pessoal não comercial.
- Mesma cláusula 2.B: a permissão de virtualização não cobre uso em "service bureau, time-sharing, terminal sharing, relay service" ou serviços semelhantes.
- Cláusula 2.J (outras restrições): a licença não permite "instalar, usar ou rodar" o software em computador que não seja da marca Apple, nem habilitar terceiros a fazê-lo.
- Citação curta (menos de 15 palavras), cláusula 2.J: "on any non-Apple-branded computer, or to enable others to do so".
- A cláusula 3 (locação, "lease") tem regra própria de virtualização (3.D) e é a base dos aluguéis em nuvem de Mac físico.
- O texto menciona o Sequoia na lista de sistemas do 2.B(i). Não conferi o PDF do Sequoia 15 separadamente; o do Tahoe 26 é o vigente.

Resposta direta: a virtualização é permitida, mas só dentro de um computador Apple que já roda macOS, no máximo 2 instâncias extras, para desenvolvimento, teste de desenvolvimento, macOS Server ou uso pessoal não comercial. Em hardware que não é Apple, nada é permitido.

---

## 2. GitHub Actions, executores de macOS

### 2.1 Rótulos, arquitetura, CPU, memória, disco

Fonte A (tabela de executores padrão): https://docs.github.com/en/actions/reference/runners/github-hosted-runners (18/11/2026).

| Rótulo | Arquitetura | vCPU | RAM | Disco | Grátis em repo público |
|---|---|---|---|---|---|
| macos-latest | arm64 (M1) | 3 | 7 GB | 14 GB | sim |
| macos-15 | arm64 (M1) | 3 | 7 GB | 14 GB | sim |
| macos-26 | arm64 (M1) | 3 | 7 GB | 14 GB | sim |
| macos-15-intel | Intel x64 | 4 | 14 GB | 14 GB | sim |
| macos-26-intel | Intel x64 | 4 | 14 GB | 14 GB | sim |
| xcode-27 | arm64 (M1) | 3 | 7 GB | 14 GB | sim (prévia) |

Fonte B (lista de imagens e rótulos, incluindo -large e -xlarge): https://github.com/actions/runner-images (18/11/2026).
- macOS 26 Arm64: macos-latest, macos-26, macos-26-xlarge.
- macOS 26 x64: macos-26-intel, macos-26-large, macos-latest-large.
- macOS 15 Arm64: macos-15, macos-15-xlarge.
- macOS 15 x64: macos-15-intel, macos-15-large.
- macOS 14 (x64): macos-14, marcado como Deprecated; "todas as imagens macOS 14 saem do GitHub Actions em 2 de novembro de 2026" (já passou). Detalhes no issue #15226 do runner-images (não abri).
- Os sufixos -large e -xlarge são só do macOS. Os executores "larger" (large/xlarge) exigem plano Team ou Enterprise Cloud e não são gratuitos nem em repositório público (https://docs.github.com/en/billing/reference/actions-minute-multipliers).
- Especificação exata de CPU/RAM dos -large (Intel 12 núcleos) e -xlarge (M2 Pro 5 núcleos): a página de preço lista as taxas (US$ 0,077 e US$ 0,102 por minuto), mas não detalhei RAM. Não confirmado em página oficial.

### 2.2 Limite de tempo por job

Fonte: https://docs.github.com/en/actions/reference/limits (18/11/2026). Cada job em executor hospedado roda até 6 horas; o Suporte não aumenta. Limite de 5 jobs macOS simultâneos nos planos Free, Pro e Team. Em alta demanda, jobs de macOS podem demorar para começar.

### 2.3 Custo

- Repositório público: executores padrão são grátis e ilimitados. Fonte: https://docs.github.com/en/billing/concepts/product-billing/github-actions (18/11/2026), frase "GitHub Actions usage is free for standard GitHub-hosted runners in public repositories" (leitura resumida pelo leitor; reconferir a frase literal se for citar).
- Repositório privado, plano Free: a página oficial agora expressa em dólares, não em minutos: US$ 12 por mês de uso incluído. Taxa do macOS padrão (3 ou 4 núcleos, M1 ou Intel): US$ 0,062 por minuto; Linux 2 núcleos: US$ 0,006. Fonte: https://docs.github.com/en/billing/reference/actions-minute-multipliers. O uso é arredondado para cima por minuto cheio por job.
- Cálculo meu (não está escrito na página): 12 / 0,062 = cerca de 193 minutos de macOS por mês, ou seja, multiplicador efetivo de aproximadamente 10x sobre o Linux 2 núcleos (0,062 / 0,006 = 10,3). A página nova não usa a palavra "multiplicador" nem fala "2.000 minutos". Não confirmei se a tabela antiga (2.000 minutos, macOS 10x) ainda existe em outro lugar.

### 2.4 Homebrew e Python pré-instalados

Fontes (READMEs das imagens, acessados em 18/11/2026):
- macOS 15 arm64: https://raw.githubusercontent.com/actions/runner-images/main/images/macos/macos-15-arm64-Readme.md . Imagem 20261104.0514.1. Homebrew 7.0.12. Python padrão `python3` 3.15.2; versões em cache 3.11.9, 3.12.10, 3.13.17, 3.14.10. Xcode padrão 16.4.
- macOS 26 arm64: https://raw.githubusercontent.com/actions/runner-images/main/images/macos/macos-26-arm64-Readme.md . Imagem 20261102.0473.1. Homebrew 7.0.11. Python igual ao acima. Xcode padrão 26.6.
- macOS 15 Intel: https://raw.githubusercontent.com/actions/runner-images/main/images/macos/macos-15-Readme.md . Imagem 20260824.0482.1 (mais velha). Homebrew 6.0.18. Python padrão 3.14.7; também 3.10.21, 3.11.9, 3.12.10, 3.13.15. O leitor inferiu que é a imagem Intel pelos caminhos x64; não está rotulado.
- Importante para o teste do instalador: a imagem já vem com Homebrew e Python, portanto NÃO é uma máquina "limpa" no sentido do instalador (não testa a instalação do Homebrew nem do Xcode Command Line Tools).

---

## 3. Ollama com modelo de 7B (4,7 GB) no executor padrão de macOS

O que encontrei (nenhum relato direto de `qwen2.5:7b` em executor macOS do GitHub Actions):

- Memória: o executor padrão arm64 tem 7 GB de RAM (item 2.1). O arquivo do modelo tem cerca de 4,7 GB e o uso em execução cerca de 5 GB (dado do seu contexto). Sobra cerca de 2 GB para o sistema, o runner e o contexto. Tende a ser apertado. Relato análogo em Linux: em executor de 7 GB, `llama3.2:8b` foi morto por falta de memória (código 137) e `llama3.2:3b` (cerca de 3,5 GB) coube. Fonte: https://brokeit.dev/posts/running-ollama-in-github-actions-ci-what-actually-works/ (blog de terceiros, Linux, não macOS). O executor Intel macos-15-intel/macos-26-intel tem 14 GB e comportaria o modelo em RAM, mas rodaria só em CPU.
- GPU (Metal): sem declaração oficial de que exista. O pedido de "GPU passthrough (Metal)" para executores macOS foi fechado em 15/02/2023 com a resposta de que é "currently impossible due to runners' design"; houve perguntas em 2024 sobre Virtualization.framework sem resposta oficial; nada em 2025. Fonte: https://github.com/actions/runner-images/issues/7085 . Conclusão prática: não contar com Metal; planejar para CPU. O Ollama pode ser forçado a CPU (num_gpu 0), segundo mantenedor citado em https://github.com/ollama/ollama/issues/1046 (trecho de busca; não abri a página).
- Download: o artigo acima mede 8 a 12 minutos para baixar um modelo de cerca de 2 GB sem cache e cerca de 35 s com `actions/cache` (cache de `~/.ollama/models`). Para 4,7 GB, extrapolação minha: algo na faixa de 10 a 25 min no primeiro download, bem abaixo do limite de 6 h por job. Cache do GitHub tem limite por repositório que não conferi (disco do executor: 14 GB, suficiente para 4,7 GB).
- Se o padrão não der: (a) executor `macos-15-intel`/`macos-26-intel` (14 GB, repositório público grátis, CPU lenta, sem Metal); (b) modelo menor só para provar a instalação (por exemplo da família qwen2.5 em 0.5b ou 1.5b, ou um `llama3.2:1b`); não conferi tamanhos atuais na biblioteca do Ollama, então confirmar na página do modelo antes. Para provar a instalação, nem precisa baixar modelo: `ollama --version` e `ollama serve` já provam o binário.

Não encontrei workflow público que rode modelo de 7B em macOS hospedado. Isso fica como "não confirmado".

---

## 4. Mac alugado por hora na nuvem

### AWS EC2 Mac
- Fontes: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-mac-instances.html e https://aws.amazon.com/ec2/instance-types/mac/faqs/ (18/11/2026).
- Disponível só como host dedicado bare metal, "minimum allocation period of 24 hours" antes de liberar o host. Cobrança por segundo, unidade de cobrança é o host. Só sob demanda (sem Spot/Reservada); Savings Plans até 44%.
- Tipos hoje: mac1.metal (Intel i7, 32 GiB), mac2.metal (M1, 16 GiB), mac2-m1ultra.metal, mac2-m2.metal (24 GiB), mac2-m2pro.metal (32 GiB), mac-m4.metal (24 GiB), mac-m4pro.metal (48 GiB).
- Sudo: "The ec2-user account also has sudo privileges". Fonte: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-to-mac-instance.html . Login por SSH com chave; senha desativada.
- Limpa: AMIs de macOS fornecidas pela AWS, sem Xcode pré-instalado (FAQ). Ao parar/terminar, o host passa por rotina de limpeza ("scrubbing"). Subida leva cerca de 6 a 20 min.
- Preço por hora: NÃO confirmei na página oficial (páginas de preço não trouxeram a tabela). Um agregador de terceiros listou mac2-m2.metal a US$ 0,878/h em us-east-1 (cerca de US$ 21 pelas 24 h mínimas); tratar como não confirmado. Conferir em https://aws.amazon.com/ec2/pricing/on-demand/ (aba de host dedicado) ou na calculadora.

### Scaleway Mac mini (Apple silicon)
- Fontes (indiretas, as páginas devolveram 403 ao leitor; dados vindos de resultados de busca do próprio domínio scaleway.com): https://www.scaleway.com/en/pricing/apple-silicon/ , https://www.scaleway.com/en/mac-mini-m4/ , https://www.scaleway.com/en/docs/apple-silicon/faq (18/11/2026).
- Preço: M4 16 GB/256 GB a €0,22/h; 16 GB/512 GB €0,24/h; 32 GB/1 TB €0,29/h; M4 Pro 64 GB €0,49/h. Mínimo de 24 horas por exigência da licença da Apple; desligada continua cobrando (máquina alocada). Compromisso mensal não volta para hora.
- Acesso: SSH com chave; a documentação mostra comandos com `sudo` na máquina (guia de solução de problemas de VNC), e o tutorial de runner do GitHub cria usuário no grupo `admin`. Não confirmei o nome do usuário padrão nem se o login inicial é admin com sudo sem senha.
- Limpa: sem acesso físico nem ao modo de recuperação do macOS (FAQ); vem com "latest macOS", sem confirmação de Tahoe.

### MacStadium
- Fonte: https://macstadium.com/pricing (18/11/2026). Mac mini de US$ 109/mês (M2.S, 8 GB, 256 GB) a US$ 349/mês (M4.L); Mac Studio US$ 249 a US$ 449/mês. Cobrança mensal ou anual; a página não menciona cobrança por hora. Acesso: "full root access". Vem com o macOS mais recente, versões antigas sob pedido; a página não diz "instalação limpa" explicitamente. Prazo mínimo de contrato para Mac individual: a página não informa.

### MacinCloud
- Fonte oficial: https://macincloud.freshdesk.com/support/solutions/articles/8000044698-what-is-macincloud-s-pay-as-you-go-server-plan- (18/11/2026). Plano pague-por-uso é uma conta de usuário em servidor gerenciado; admin limitado (a equipe faz tarefas de administrador sob pedido); para admin/root/sudo próprio, é preciso plano Dedicated. Cobrança por dia tem mínimo de 24 horas consecutivas; cobrança por hora arredonda o total diário para a hora cheia.
- Preço: página de preço oficial retornou 404. Um comparativo de terceiros (2026) cita cerca de US$ 1 por hora; não confirmado.
- Como o plano pague-por-uso é conta em servidor compartilhado e sem sudo, não serve para testar um instalador que precisa de sudo/Homebrew.

### Outros
- CircleCI: plano Free tem 30.000 créditos por mês para macOS (classe m4pro.medium), segundo https://support.circleci.com/en/articles/15091231-are-free-credits-available-for-macos-open-source-projects (resultado de busca; não abri). Um calculador de terceiros estima 200 créditos por minuto, o que daria cerca de 150 minutos por mês (estimativa não confirmada). Útil como alternativa ao GitHub, porém o ambiente também é pré-montado.
- Cirrus CI: encerrou em 01/06/2026 (segundo resultados de busca, https://bitrise.io/blog/post/cirrus-ci-shutting-down-move-to-build-hub). Não usar.

---

## 5. Homebrew hoje

Consulta à API oficial de fórmulas (https://formulae.brew.sh/api/...), 18/11/2026.

- Fórmula `ollama`: versão 0.40.16, não depreciada nem desativada; dependência de execução `mlx-c`; compila com cmake, go, ccache. Só a linha de comando (servidor e CLI). URL: https://formulae.brew.sh/api/formula/ollama.json
- Cask `ollama-app` (token antigo `ollama`, listado em `old_tokens`): versão 0.40.16, `auto_updates: true`, exige macOS 14 ou superior; instala `Ollama.app` em /Applications e também liga o binário `ollama` do pacote em `$HOMEBREW_PREFIX/bin`. Conflita com o cask `ollama-binary`. URL: https://formulae.brew.sh/api/cask/ollama-app.json
- Cask `ollama-binary`: versão 0.40.16, só o binário `ollama` ligado em `$HOMEBREW_PREFIX/bin`, sem aplicativo, macOS 14 ou superior. URL: https://formulae.brew.sh/api/cask/ollama-binary.json
- Diferença: fórmula = binário compilado/engarrafado pelo Homebrew, sem app; `ollama-app` = aplicativo de barra de menu com atualização automática (e serviço launchctl `com.ollama.ollama`); `ollama-binary` = binário oficial sem o app. Não confirmei a diferença de comportamento do servidor entre fórmula e cask (por exemplo `brew services`).
- `php`: 8.5.12 (alias php@8.5); versionadas existentes: php@8.4, php@8.3, php@8.2, php@8.1. URL: https://formulae.brew.sh/api/formula/php.json
- `php@8.2`: 8.2.35, ainda NÃO depreciada; marcada para ser depreciada em 31/12/2026 e desativada em 31/12/2027. URL: https://formulae.brew.sh/api/formula/php@8.2.json
- `mariadb`: 13.0.2, não depreciada; versionadas: 12.3, 11.8, 11.4, 10.11, 10.6, 10.5. URL: https://formulae.brew.sh/api/formula/mariadb.json . Atenção: 13.0.x é série nova; se o projeto foi validado em outra série, fixar `mariadb@11.8` ou similar.
- `python@3.14`: 3.14.10, ativa. URL: https://formulae.brew.sh/api/formula/python@3.14.json . (O README da imagem do GitHub mostra Python 3.15.2 como padrão do `python3`; não verifiquei a fórmula `python@3.15`.)
- Requisitos do Homebrew: https://docs.brew.sh/Installation e o próprio script https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh
  - Apple Silicon é o alvo principal; o script de instalação aborta em Mac Intel com "Homebrew on macOS is only supported on Apple Silicon processors!". Intel é Tier 3 na documentação (sem suporte oficial de instalação pelo script atual). macOS 15.0 a menos de 28.0 suportado; fora disso o script avisa mas continua.
  - Prefixo: Apple Silicon `/opt/homebrew`; Intel `/usr/local` (https://docs.brew.sh/FAQ, descrição de convivência com Rosetta 2).
  - Command Line Tools: o script instala as CLT via `softwareupdate` se faltar `/Library/Developer/CommandLineTools/usr/bin/git` e houver sudo. A documentação diz que CLT/Xcode só são necessários para compilar fórmulas a partir do código-fonte; no Apple Silicon casks e bottles instalam sem ferramentas de desenvolvedor.
  - `NONINTERACTIVE=1` pula a confirmação (o script também ativa sozinho com `CI` definido ou sem terminal). Nesse modo o sudo roda com `-n` e nunca pede senha; então é preciso ter sudo sem senha ou prefixo já gravável.
  - Sudo: precisa de sudo na instalação inicial (criar `/opt/homebrew`). O usuário não precisa ser root (rodar como root é bloqueado fora de contêiner/CI). Depois, instalar fórmulas não exige sudo; alguns casks e serviços exigem. `HOMEBREW_NO_SUDO=1` rejeita os casks que precisam.

---

## 6. Outros caminhos legítimos e o que fica de fora

Caminhos legítimos não listados por você:
- Pedir emprestado ou usar por um dia um Mac físico (colega, laboratório da instituição, loja Apple com demonstração não serve para instalar). Cumpre a licença sem custo e é o único caminho com GPU real.
- Executores macOS de outros provedores de CI com plano gratuito (CircleCI, item 4). Não verifiquei Bitrise, Codemagic ou Xcode Cloud; Xcode Cloud só serve a apps Apple e não roda scripts livres.
- Serviços de teste de navegador em Mac real (BrowserStack, LambdaTest, Sauce Labs): dão macOS real para navegador, não um shell para o instalador. Não conferi planos nem preços.
- Mac mini usado ou recondicionado como compra única (opção de longo prazo, não pesquisei preços).

Fora, em uma linha cada (sem instruções):
- Hackintosh: instala o macOS em computador que não é da marca Apple, o que a cláusula 2.J do contrato proíbe expressamente.
- Máquina virtual de macOS em PC que não é Apple (VMware, VirtualBox, QEMU no Windows): a virtualização só é permitida dentro de um Mac da Apple (cláusula 2.B(iii)), então em PC com Windows fica fora da licença.

---

## O que não consegui confirmar

1. Preço por hora atual do EC2 Mac (mac2.metal, M2, M4) em página oficial da AWS. Só um valor de terceiros (US$ 0,878/h para mac2-m2.metal em us-east-1).
2. Páginas de preço oficiais do Scaleway e do MacinCloud devolveram 403/404; preços e regras vêm de trechos de busca (Scaleway €0,22/h M4 com 24 h mínimas; MacinCloud cerca de US$ 1/h de terceiros).
3. Nome do usuário padrão e se o Scaleway dá sudo no login inicial; se as máquinas do Scaleway e do MacStadium vêm com macOS recém-instalado e qual versão (Tahoe ou Sequoia).
4. MacStadium: cobrança por hora e prazo mínimo (a página lista só mensal/anual).
5. Minutos gratuitos do plano Free em repositório privado: a página oficial dá US$ 12; o valor em minutos (cerca de 193 de macOS) e o multiplicador de cerca de 10x são cálculo meu.
6. Especificação oficial (CPU, RAM) dos executores -large e -xlarge, e o status exato (GA ou não) de macos-15 e macos-26.
7. Se o executor arm64 padrão tem Metal/GPU: nenhuma declaração oficial; o último posicionamento do GitHub é de 2023 ("impossível"). Não encontrei teste real do Ollama com GPU nesse executor.
8. Nenhum relato público encontrado de `qwen2.5:7b` (4,7 GB) rodando em executor macOS do GitHub Actions; a conclusão de "apertado com 7 GB" é inferência. Tempo de download de 4,7 GB é extrapolação.
9. Tamanhos atuais de modelos menores do Ollama (para o plano B) não foram conferidos.
10. Diferença de comportamento entre a fórmula `ollama` e o cask `ollama-app` (serviço, `brew services`, atualização) não foi verificada além dos metadados.
11. Contrato do Sequoia 15 não foi aberto separadamente; foi usado o do Tahoe 26 (EA1955, 07/11/2025).
12. Licença atual do Tart e do CircleCI em créditos exatos: fontes divergentes, não relevantes ao instalador.
