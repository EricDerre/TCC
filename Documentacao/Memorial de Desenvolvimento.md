<!-- ! Alteração de IA - Revisar: documento novo, memorial de desenvolvimento do projeto.
     ! Motivo: o histórico de decisões, achados experimentais e referências estava espalhado
     entre commits, comentários de código e conversas — sem consolidação, a redação do relatório
     final teria de reconstruir tudo do zero. Aqui o código é referenciado por commit e resumido,
     porque o foco do TCC é o método e os resultados, não a implementação. -->

# Memorial de Desenvolvimento

**Projeto:** Agente de QA End-to-End Autônomo com Capacidades de Self-Healing — UNICID, Ciência da Computação.
**Finalidade deste documento:** servir de insumo para a redação do relatório final. Reúne decisões tomadas e por quem, achados experimentais, correções feitas no projeto de pesquisa e as referências levantadas. As alterações de código aparecem apenas resumidas e referenciadas por commit.

**Período coberto:** 31/08/2026 a 02/09/2026.

---

## 1. Ponto de partida

O repositório continha apenas o commit `e854a0e` — a clonagem de um site PHP de terceiro ("Churrascaria Fornalha", cedido por um integrante do grupo para servir de cobaia). As pastas `AgenteCore` e `CobaiaAPI` existiam vazias.

**O primeiro achado condicionou todo o resto do projeto:** o `CobaiaFront` é um monolito PHP que renderiza tudo no servidor e consulta o banco diretamente via `mysqli` — **sem nenhuma chamada `fetch`/AJAX a uma API JSON**. Como o conceito central da pesquisa é *Contract Drift* na fronteira Front-to-Back, não havia fronteira alguma para o agente interceptar. Sem resolver isso, o objeto de estudo não existiria.

Também se constatou que o dump `banco/bancoatualizado.sql` estava incompleto em relação ao código: definia `tbtipos`, `tbprodutos`, `tbusuarios` e a view `vw_tbprodutos`, mas o fluxo de reservas usava `tbpedido_reserva` e `vw_tbpedidos`, inexistentes. E não havia nenhum `INSERT` — o site subia vazio e sem usuário para login.

---

## 2. Decisões tomadas

Registradas com a autoria, porque a distinção entre o que foi decidido pelo grupo e o que foi recomendação técnica importa para a seção de metodologia.

| # | Decisão | Quem decidiu | Fundamento |
|---|---|---|---|
| 1 | **Dois alvos separados**: manter o `CobaiaFront` intocado como sistema legado e construir uma `CobaiaAPI` nova para o cenário de API JSON | Eric, entre 3 opções apresentadas | Preserva o site cedido sem risco e cria a fronteira HTTP que a pesquisa exige |
| 2 | `CobaiaAPI` em **Python + FastAPI** | Eric | Tipagem do Pydantic facilita simular quebra de contrato; alinha com o vocabulário já usado no documento |
| 3 | **Um único banco compartilhado** entre os dois alvos | Eric | Evita dado inconsistente; produz o cenário realista de duas interfaces sobre o mesmo backend |
| 4 | A aba de API é uma **página nova dentro do próprio site**, com o mesmo layout | Eric | Mantém a navegação e a aparência do sistema legado, isolando a diferença na origem dos dados |
| 5 | Credencial SMTP exposta no código **fica como está** | Eric | Ambiente de teste, sem dado real de pessoa ou empresa |
| 6 | Repositório **"hit and run"**: um instalador único cobre tudo, em Windows e Linux | Eric | Facilita o uso pelos 9 integrantes e a demonstração ao vivo na banca |
| 7 | **LLM 100% local e gratuito** (Ollama), substituindo o Google Colab + FastAPI + Ngrok do projeto original | Eric | A ferramenta precisa ser usável fora da universidade, sem custo e sem configurar nuvem |
| 8 | Escopo do Self-Healing: **diagnóstico + cura de seletor**, sem propor patch do código da aplicação | Eric, entre 3 opções | Tarefa restrita o bastante para um modelo quantizado pequeno acertar, e mensurável por MTTR e Task Success |
| 9 | Navegador do agente: **Chromium do próprio Playwright**, não Chrome/Edge do sistema | Eric (após apontar que Edge inviabiliza Linux) | Versão fixa garante reprodutibilidade das métricas; mesmo comando nos dois sistemas |
| 10 | Convenção de comentários: a marca de alteração por IA **nunca vem sozinha** — sempre com o que foi feito e o motivo | Eric | O revisor precisa entender o contexto sem reabrir a investigação |
| 11 | Nomenclatura CamelCase com prefixo húngaro é **do projeto ERP, não deste** | Eric, entre 3 opções | Evita duas convenções conflitantes no mesmo repositório; aqui vale PEP8 |
| 12 | Correções no projeto de pesquisa ABNT feitas **diretamente no arquivo**, marcadas | Eric, entre 4 opções | Mais rápido; o grupo revisa depois |
| 13 | Cada modelo constrói a **própria biblioteca**, com uma **rodada de controle** usando biblioteca de referência | Eric, entre 3 opções | Separa "biblioteca ruim" de "raciocínio ruim", que ficariam confundidos numa nota única |
| 14 | Resultados em **imagens + relatório HTML** | Eric | Imagens alimentam o documento; o relatório permite explorar os dados |
| 15 | **5 a 6 modelos** na comparação | Eric, entre 3 faixas | Equilíbrio entre abrangência e profundidade da análise por modelo |
| 16 | Manter `qwen2.5-coder:3b` apesar da licença de pesquisa | Eric | Documentar a restrição; trocar apenas o padrão de produção |
| 17 | `.gitignore` mínimo, revisto depois com base em evidência | Eric | Ver seção 4.11 |

---

## 3. O que foi construído (referência por commit)

O código não é o foco do relatório; segue apenas o resumo por commit.

| Commit | Data | Conteúdo |
|---|---|---|
| `e854a0e` | 31/08 | Clonagem do site PHP cedido (197 arquivos) — ponto de partida |
| `ab4da6a` | 31/08 | Estrutura base: instalador cross-platform, `CobaiaAPI` completa (FastAPI + SQLAlchemy + PyMySQL), schema e seed do banco, página `produtos_api.php`, mecanismo de injeção de falhas |
| `26432d2` | 31/08 | `Cobaia.exe` (PyInstaller), README, correções de empacotamento |
| `dc1a7b8` | 01/09 | `.gitignore` revisto com base em evidência; correção da regra para outros sistemas operacionais |
| `084fce0` | 01/09 | Retrofit dos comentários de IA (20 arquivos) e normalização de nomenclatura |
| `1b0c4b8` | 01/09 | Correções no projeto de pesquisa ABNT e ajustes de planejamento |
| `4299b19` | 02/09 | Preparação dos modelos e primeira leva de testes de prolixidade e eficiência |

**Componentes resultantes:** `CobaiaFront` (PHP legado, intocado exceto por um link de menu e uma página nova); `CobaiaAPI` (FastAPI, 5 endpoints, 7 modos de injeção de falha); instalador único (`install.*`/`run.*`/`Cobaia.exe`) idempotente para Windows e Linux; e `AgenteCore/experimentos` com o harness de benchmark.

---

## 4. Achados experimentais

Esta é a seção com maior valor para o relatório: são resultados obtidos executando, não deduções. Vários contradizem a expectativa inicial.

### 4.1 O objeto de estudo não existia no material de partida
O site cedido não faz nenhuma requisição JSON. Toda a premissa de interceptar quebra de contrato dependia de construir essa fronteira. **Implicação metodológica:** a "aplicação-alvo determinística" que o projeto de pesquisa menciona no plural precisou ser, em parte, construída.

### 4.2 Schema incompleto e conta de cliente impossível
Além das duas estruturas ausentes, `tbusuarios` não tinha as colunas `nome` e `cpf` que a view exige, e seu ENUM de nível só admitia `'sup'` — ou seja, **uma conta de cliente era fisicamente impossível de existir**, e o fluxo de reservas era código morto. Reconstruído por engenharia reversa das consultas reais do código, sem alterar nenhum arquivo PHP.

### 4.3 A extensão `mbstring` era obrigatória, não opcional
`mb_strimwidth()` é usada em 5 páginas de produtos, incluindo a home. Sem a extensão carregada é **erro fatal**, não aviso. Só apareceu ao inspecionar a página inteira — um teste superficial buscando uma string passava, porque o conteúdo anterior ao ponto de falha ainda era emitido.

### 4.4 `output_buffering` mascarava um bug pré-existente de sessão
`cliente/index.php` emite HTML antes de `reserva_cli.php` incluir `acesso_com.php`, que só então chama `session_start()`. Sem buffer de saída, isso vira "headers already sent", a sessão do login não é retomada e a página **trunca logo após a saudação**. Um XAMPP típico traz `output_buffering` ligado por padrão, o que esconde o defeito. Resolvido por configuração do PHP, sem tocar no código.

### 4.5 `INNER JOIN` apagava clientes sem reserva
A primeira versão da view `vw_tbpedidos` usava junção interna a partir de `tbpedido_reserva`: um cliente recém-criado, ainda sem reservas, sumia inteiramente da view e a saudação quebrava. Corrigido com `LEFT JOIN` a partir de `tbusuarios`.

### 4.6 O MariaDB do winget não registra serviço no Windows
Instalado sem privilégios de administrador, os binários e o diretório de dados são criados, mas **nenhum serviço do Windows é registrado**. Por isso o banco passou a ser gerenciado como subprocesso comum, igual ao servidor PHP e ao uvicorn — o que, de quebra, eliminou a necessidade de elevação em toda a instalação.

### 4.7 O `extension_dir` do PHP vem apontando para o lugar errado
O build Windows aponta por padrão para `C:\php\ext`, que não corresponde ao caminho real de instalação via winget. Sem sobrescrever explicitamente, as extensões falham a carregar **silenciosamente**.

### 4.8 Um executável PyInstaller não consegue criar ambientes virtuais
Duas falhas distintas ao empacotar o instalador: `Path(__file__)` aponta para a pasta temporária de extração, não para onde o executável está; e `venv.EnvBuilder` falha ao copiar `venvlauncher.exe`, porque o interpretador embutido não tem o layout de uma instalação Python normal. Resolvido usando `sys.executable` quando congelado e delegando a criação do ambiente a um Python real via subprocesso.

### 4.9 Acentuação quebra o interpretador de arquivos `.cmd`
Testado isoladamente: o `cmd.exe` lê o arquivo na codepage OEM, e os bytes UTF-8 de `ç`/`ã` re-tokenizam a linha de comentário, fazendo o script imprimir um erro espúrio antes de rodar. Os arquivos `.cmd` do projeto usam marcador sem acento por isso.

### 4.10 A política de execução do PowerShell bloqueia o instalador
Erro de segurança ao chamar `.ps1` diretamente. Resolvido com atalhos `.cmd` que invocam o PowerShell com `-ExecutionPolicy Bypass` — válido apenas para aquela execução, sem alterar configuração permanente da máquina.

### 4.11 O ambiente virtual versionado era inutilizável por terceiros
A intenção inicial era versionar tudo, inclusive o `.venv`, para reforçar o "hit and run". A inspeção mostrou o contrário: o `pyvenv.cfg` grava **caminhos absolutos da máquina de origem** (`home = C:\Python314`), e a pasta contém 16 executáveis e 14 bibliotecas compiladas só de Windows, sem o diretório `bin/` que o Linux usa. São 67 MB **inutilizáveis no Linux e quebrados em qualquer outra máquina Windows** — o oposto do objetivo. O instalador recria o ambiente correto para cada sistema em cerca de 30 segundos.

### 4.12 Modelos pequenos erram a causa raiz quando recebem o JSON cru
No cenário de campo renomeado (`preco` → `preco_v2`), **os três portes testados erraram**: 1.5B e 7B culparam a conversão numérica por "não lidar com decimais"; o 3B acertou apenas o nome do campo. O 1.5B ainda **inventou um bloco JSON de erro que não existia** na entrada.

Levantou-se a hipótese de que comparar chaves entre estruturas é trabalho de código, não de modelo de linguagem. Repetindo o mesmo cenário com a divergência **pré-calculada em código**, 3B e 7B passaram a acertar — o 3B respondeu literalmente *"a API retornou um campo `preco_v2` que não estava previsto no contrato da interface"*.

**Consequência arquitetural:** o interceptador calcula o diff de contrato deterministicamente e envia o diff ao modelo, nunca o JSON bruto para comparação. Isso foi posteriormente confirmado pela literatura (ver seção 6.2).

### 4.13 O modelo menor é o mais lento
Contra a intuição, o 1.5B levou 10,24 s no diagnóstico contra 5,98 s do 3B — porque gera 172 tokens onde o 3B gera 52. **O tempo é dominado pela prolixidade, não pelo tamanho do modelo.**

### 4.14 Candidatos de seletor são plausíveis mas ambíguos
Na tarefa de cura de localizador: o 1.5B devolveu **CSS sintaticamente inválido** (espaços no lugar de pontos); o 3B devolveu seletores válidos mas que casam com **dois** cartões; só o 7B produziu um seletor único, no segundo candidato. Isso valida a etapa de validação prevista: aceita-se apenas candidato que resolva para **exatamente um** elemento na página viva. Sem ela, a resposta do 3B seria aceita e o teste passaria a clicar no cartão errado silenciosamente.

### 4.15 Cython não traria ganho neste projeto
Ver seção 7.

---

## 5. Correções feitas no projeto de pesquisa (ABNT)

Aplicadas em `Projeto de Pesquisa - ABNT 15287_2025 - V3.md`, commit `1b0c4b8`, cada uma marcada no texto.

| Trecho | Antes | Depois | Motivo |
|---|---|---|---|
| Objetivo geral | "arquitetura de nuvem híbrida"; "propor correções de código" | LLM executado localmente; cura de localizadores + diagnóstico | A implementação é local; correção autônoma de código-fonte foi descartada por inviabilidade com modelo pequeno |
| Objetivo específico 2 | Google Colab + FastAPI + Ngrok | Camada de inferência local (Ollama) | Idem |
| §3.2 | Qwen2.5-Coder em GPU T4 na nuvem | Modelo quantizado em CPU local, com critério do menor porte que atende | A dependência de nuvem **contradizia o próprio problema de pesquisa**, que pergunta como operar sob restrição de hardware local |
| §3.3 | Túnel Ngrok + API de ponte | Comunicação por loopback; regra de truncamento que preserva chaves e tipos | Sem servidor remoto, não há o que tunelar. Truncar chave destruiria o sinal de quebra de contrato |
| §3.4 | Métricas nomeadas sem definição | Fórmula de MTTR, definição de Task Success, grupo de controle manual, volume e condições de determinismo | Não havia fórmula, linha de base nem número de execuções — o Mês 5 chegaria sem protocolo |
| §4 | "viabilidade... através da topologia de nuvem híbrida" | Execução local sem custo de infraestrutura | Recorrer a GPU em nuvem **contorna** a restrição em vez de demonstrar viabilidade sob ela |
| §2.1 | Oscilava entre autonomia total e copiloto | Correção aplicada automaticamente na verificação, apresentada como sugestão | A ambiguidade tornaria o Task Success indefinido |
| §2.4 | Só Prune4Web | + Joseph (2026), fixando que a poda incide **sobre a árvore de acessibilidade** | O texto nomeava dois artefatos sem nunca relacioná-los |
| §2.5 e §2.6 | Inexistentes | Quebra de contrato de API (Maciak) e RAG (Shi, Li e Chen) | Três referências constavam na lista **sem citação no corpo** — defeito perante a NBR 6023 |
| Cronograma, Mês 2 | Colab, FastAPI, Ngrok | Ollama com modelo quantizado, incluindo comparação de portes | Coerência com §3.2 |
| Glossário | Continha Ngrok, com definição na direção oposta à proposta | Removido; acrescentados 8 termos usados no corpo mas não definidos | Accessibility Tree, Attention Dilution, DOM Pruning, MTTR, Ollama, Quantização, RAG, Task Success |

**Pendência:** o arquivo `.pdf` na mesma pasta é anterior a essas correções e precisa ser regerado. As marcações são comentários HTML, invisíveis na conversão, mas convém removê-las antes da entrega final.

---

## 6. Pesquisa bibliográfica

Duas frentes, ambas com o objetivo de evitar decisão por intuição.

### 6.1 Cenário de modelos livres e locais

Levantamento de 12 candidatos executáveis via Ollama, com licença, tamanho, capacidade em português e estabilidade da tag.

**Eliminados por critério objetivo:** OpenCoder (oficialmente só inglês e chinês); StarCoder2 3B/7B (são modelos *base*, não seguem instrução); CodeLlama (2 anos, base Llama 2, português fraco); Mistral 7B (defasado, português fraco); Codestral (22B e licença de não-produção); DeepSeek-Coder-V2 (8,9 GB, acima do orçamento de memória).

**Achado mais valioso:** `qwen2.5-coder:7b` **vs** `qwen2.5:7b` formam um experimento controlado quase perfeito — mesma base, tamanho, licença, tokenização e mês de treino, diferindo **apenas** pelo fine-tuning em código. Responde "especialização em código ajuda nesta tarefa?" sem variáveis de confusão.

**Alerta de licença:** `qwen2.5-coder:3b` está sob **Qwen Research License (não-comercial)**, enquanto o `:7b` da mesma família é Apache 2.0. Decidiu-se mantê-lo na comparação com a restrição documentada, trocando apenas o padrão de produção.

**Português (PoETa v2, nov/2025):** Qwen2.5 7B lidera entre os abertos pequenos com 63,7 NPM; Llama 3.1 8B fica em 53,5. Achado relevante para o dimensionamento: **modelos abaixo de 5B têm perda desproporcional em português** (5,1 pontos de diferença EN↔PT, contra 3,8 nos de 10B+) — o que justifica metodologicamente manter a faixa de 7–8B apesar da latência.

**Riscos operacionais documentados:** tags do Ollama são ponteiros mutáveis, não imutáveis — é preciso registrar o digest sha256 de cada modelo para o experimento ser reproduzível; o modo *thinking* de Qwen3 e Granite 4.2 multiplica a latência e precisa ser desativado; e o cache KV de modelos com 128K de contexto estoura a memória antes do peso do modelo, exigindo fixar `num_ctx`.

**Baseline não-neural:** existe um algoritmo de prioridade em 10 níveis que recupera 82,4% dos localizadores em menos de 1 s, sem LLM. Entra como piso obrigatório da tarefa de seletor — se os modelos não o superarem, esse é um resultado honesto.

### 6.2 Raciocínio em estágios para modelos pequenos

Investigação motivada pela proposta de estruturar a análise do agente nas fases de um compilador.

**O que está bem estabelecido:**
- Chain-of-Thought **degradava** modelos pequenos no regime de 2022 — LaMDA 8B caiu de 3,2% para 1,6% em GSM8K, e o padrão se repete em toda a faixa abaixo de 10B (Wei et al., 2022). **Ressalva honesta:** eram modelos *base* de 2022; extrapolar para um Qwen2.5-3B-Instruct atual é inferência, não resultado — é justamente a lacuna que nosso experimento mede.
- O ganho de CoT concentra-se em **matemática e lógica simbólica**; fora disso é pequeno (Sprague et al., ICLR 2025).
- Há perda documentada de **até 36,3 pontos** em tarefas de classificação com exceções (Liu et al., ICML 2025) — que é a forma da nossa tarefa.
- Em pipeline de *n* estágios com confiabilidade *p*, o sucesso é *pⁿ*: com 6 estágios e p=0,85, cerca de 38%. Aritmética, não hipótese.

**O que mudou o desenho do experimento:** o trabalho PA-Tool (ACL 2026) mediu **+17 pontos no Qwen2.5-3B apenas por alinhar nomes de schema ao que o modelo viu no pré-treino**, com queda de 80% nos erros de aderência. "Análise léxica" carrega prior fortíssimo de *tokenizar código-fonte*; aplicá-lo a comparação de payload HTTP convida o modelo ao prior errado. Por isso o teste passou de dois para **três braços**: linear, estagiado com nomes de compilador, e estagiado com nomes de domínio — isolando o efeito do *nome* do efeito da *estrutura*.

**Lacuna encontrada:** não existe nenhum trabalho publicado propondo fases de compilador como andaime de prompting. A ausência não prova que a ideia é ruim, mas significa que ninguém documentou ganho com ela — e torna o resultado publicável nos dois sentidos.

**Métrica que teria passado despercebida:** *wrong-valid-schema* — resposta que parseia perfeitamente mas está semanticamente errada. O trabalho "The Constraint Tax", único no regime sub-3B, mediu validade subindo de 61,5% para 100% enquanto a acurácia caía de 19,7% para 11,0% e o erro semântico saltava para 88,9%. Medir apenas "parseou?" deixaria cego para a maior parte dos erros.

**Convergência com o achado empírico da seção 4.12:** o trabalho F-CoT mostra que o estágio de *extração* é exatamente onde modelos pequenos falham (um Qwen-3 0.6B gerou contexto estruturado válido em menos de 2% dos casos). Pré-calcular o diff em código é remover do modelo justamente esse estágio — o que havíamos descoberto medindo, antes de encontrar a literatura.

---

## 7. Validação da hipótese de uso de Cython

**A premissa não se confirmou.** Verificação no repositório: nenhum arquivo `.pyx` ou `.pxd`, nenhuma chamada a `cythonize`, nenhum `import cython`, e o Cython sequer está instalado no ambiente. **Não há código Cython nosso no projeto.**

O que existe são **extensões compiladas de dependências de terceiros**, distribuídas já prontas: `httptools` (essa sim, gerada com Cython), `pydantic_core` e `watchfiles` (Rust), além de `greenlet`, `sqlalchemy`, `websockets` e `yaml` (C). São binários que já vêm compilados na instalação — não são código que escrevemos nem que compilamos.

### Medição

Para responder se compilar nosso código traria ganho, mediu-se a decomposição do tempo de uma inferência real de diagnóstico (`qwen2.5-coder:3b`, média de 3 execuções):

| Componente | Tempo | Fração |
|---|---|---|
| Inferência dentro do Ollama | 7,680 s | 79,07% |
| Transporte HTTP e espera de I/O | 2,033 s | 20,93% |
| **Nosso código Python** (serializar/desserializar JSON) | **0,000263 s** | **0,0027%** |
| **Total** | **9,713 s** | 100% |

**Teto de ganho se o nosso código Python fosse infinitamente rápido: 0,0027%.**

### Conclusão

O tempo do projeto é dominado por inferência do modelo (código C++ do llama.cpp, dentro do Ollama) e por espera de entrada e saída — nenhum dos dois acelerável por Cython. O código Python do projeto é orquestração: chama subprocessos, monta requisições e lê respostas.

Há ainda um conflito direto com a regra de projeto do "hit and run": **Cython exige um compilador C na máquina de destino** (MSVC no Windows, gcc no Linux). Foi exatamente por esse motivo que se escolheu `PyMySQL` em vez de `mysqlclient` — decisão já registrada no `requirements.txt`. Adotar Cython reintroduziria a dependência de toolchain que se decidiu evitar, e complicaria o empacotamento do `Cobaia.exe`.

**Recomendação: não adotar.** O ganho máximo teórico é de três milésimos de por cento, contra um custo real em portabilidade e em complexidade de instalação.

**Único ponto onde valeria reavaliar:** a poda da árvore de acessibilidade (Fase 4), que é o primeiro trecho do projeto a fazer trabalho de CPU não trivial em Python. O critério objetivo para reabrir a discussão: se a poda passar a consumir **mais de 5% do tempo total de um ciclo de diagnóstico**, medido com perfilador. Abaixo disso, não se justifica.

---

## 8. Pendências e questões em aberto

- **Regerar o PDF** do projeto de pesquisa a partir do Markdown corrigido, e remover os comentários de marcação antes da entrega final.
- **Fichamento formal** das 7 referências: o recorte de cada uma já está embutido nas seções 2.2 a 2.6 do projeto de pesquisa, mas não existe documento de fichamento separado.
- **Padrão de produção do modelo**: `qwen2.5-coder:3b` permanece na comparação com licença de pesquisa documentada; a escolha do padrão distribuível precisa recair sobre uma opção Apache 2.0 ou MIT.
- **Validação em Linux**: o instalador foi testado apenas em Windows. Os caminhos de `apt` e `brew` seguem convenções estabelecidas, mas não foram executados.
- **Critérios de aceitação quantitativos**: definidos no planejamento (fórmula de MTTR, Task Success, linha de base manual, volume), mas ainda não incorporados ao corpo do projeto de pesquisa além da §3.4.

---

## 9. Referências levantadas

Além das 7 do projeto de pesquisa, o levantamento produziu as seguintes, organizadas por tema. Nem todas precisam entrar no relatório; estão aqui para consulta.

### Raciocínio, CoT e modelos pequenos
- WEI, J. et al. **Chain-of-Thought Prompting Elicits Reasoning in Large Language Models**. NeurIPS, 2022. https://arxiv.org/abs/2201.11903
- SPRAGUE, Z. et al. **To CoT or not to CoT? Chain-of-thought helps mainly on math and symbolic reasoning**. ICLR, 2025. https://arxiv.org/abs/2409.12183
- LIU, R. et al. **Mind Your Step (by Step): Chain-of-Thought can Reduce Performance on Tasks where Thinking Makes Humans Worse**. ICML, 2025. https://arxiv.org/abs/2410.21333
- **Through the Valley: Path to Effective Long CoT Training for Small Language Models**. 2026. https://arxiv.org/abs/2506.07712
- ZHOU, D. et al. **Least-to-Most Prompting Enables Complex Reasoning in LLMs**. https://arxiv.org/abs/2205.10625
- WANG, L. et al. **Plan-and-Solve Prompting**. ACL, 2023. https://arxiv.org/abs/2305.04091
- KHOT, T. et al. **Decomposed Prompting: A Modular Approach for Solving Complex Tasks**. ICLR, 2023. https://arxiv.org/abs/2210.02406
- WANG, X. et al. **Self-Consistency Improves Chain of Thought Reasoning**. ICLR, 2023. https://arxiv.org/abs/2203.11171
- **Self-Consistency Is Losing Its Edge: Diminishing Returns and Rising Costs**. 2026. https://arxiv.org/html/2511.00751
- **When Self-Consistency Backfires: Majority Vote Hurts the Majority of Problems**. 2026. https://arxiv.org/abs/2608.11403

### Saída estruturada e modelos pequenos
- TAM, Z. R. et al. **Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance of LLMs**. EMNLP Industry Track, 2024. https://arxiv.org/abs/2408.02442
- **Say What You Mean: A Response to 'Let Me Speak Freely'**. dottxt, 2024. https://blog.dottxt.ai/say-what-you-mean.html *(refutação metodológica)*
- RAY, J. **The Constraint Tax: Measuring Validity-Correctness Tradeoffs in Structured Outputs for Small Language Models**. 2026. https://arxiv.org/abs/2605.26128
- **Don't Adapt Small Language Models for Tools; Adapt Tool Schemas to the Models**. ACL, 2026. https://arxiv.org/abs/2510.07248
- **Focused Chain-of-Thought: Efficient LLM Reasoning via Structured Context**. 2026. https://arxiv.org/html/2511.22176v1
- **JSONSchemaBench**. ICML, 2025. https://arxiv.org/abs/2501.10868

### Diagnóstico de falhas e automação de testes
- **LLM-Based Automated Diagnosis of Integration Test Failures at Google**. 2026. https://arxiv.org/html/2604.12108v1
- **Zero-Cost Self-Healing locator repair via accessibility tree**. 2026. https://arxiv.org/abs/2603.20358 *(baseline não-neural, 82,4% em &lt;1 s)*
- **WebTestBench**. 2026. https://arxiv.org/html/2603.25226

### Modelos e português
- **PoETa v2: benchmark de português**. 2025. https://arxiv.org/abs/2511.17808
- **P3B3: viés PT-EU vs PT-BR**. 2026. https://arxiv.org/pdf/2606.16753
- **Tucano 2**. 2026. https://arxiv.org/abs/2603.03543
- HUI, B. et al. **Qwen2.5-Coder Technical Report**. https://arxiv.org/html/2409.12186v3

### Esquecimento catastrófico e especialização
- **Interpretable Catastrophic Forgetting of LLM Fine-tuning**. 2024. https://arxiv.org/html/2406.12227v1
- **An Empirical Study of Catastrophic Forgetting in LLMs During Continual Fine-tuning**. https://arxiv.org/html/2308.08747

### Desempenho de inferência em CPU
- **Deploying LLMs on CPU-only Environments with llama.cpp**. https://ceur-ws.org/Vol-4164/paper11.pdf
- **LLM Inference Acceleration: A Hardware Perspective**. https://arxiv.org/pdf/2410.04466
