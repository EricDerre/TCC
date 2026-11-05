<!-- ! Alteração de IA - Revisar: (05/11/2026) README refeito como porta de entrada: o que é o projeto, como o agente trabalha, onde está, o que já descobriu (figura, como ler e o que mostra) e como rodar. O detalhe técnico saiu para `DETALHES-TECNICOS.md`, com as tags antigas de cada trecho.
     ! Motivo: o Eric pediu (05/11/2026) uma revisão geral: o README tinha 96 mil caracteres, com tabelas cujas células passavam de 4 mil, e quem chegava não achava o resultado no meio dos dados. O pedido foi deixar a leitura com gráficos e a explicação de cada um, em linguagem direta, e os valores de cada rodada num documento à parte. O histórico das versões anteriores está no git. -->
# Agente de QA E2E Autônomo com Self-Healing

[![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-2ea44f)](LICENSE)
[![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](Programacao/CobaiaAPI/requirements.txt)
[![PHP 8.2](https://img.shields.io/badge/PHP-8.2-777BB4?logo=php&logoColor=white)](Programacao/CobaiaFront)
[![Modelo local](https://img.shields.io/badge/LLM%20local-Ollama%20%C2%B7%20qwen2.5%3A7b-1f6feb)](Programacao/AgenteCore/experimentos)
[![Painel do projeto](https://img.shields.io/badge/painel-do%20projeto-8957e5)](https://claude.ai/artifact/LhXeAccx5NMk1HprycHApN)

Trabalho de Conclusão de Curso em Ciência da Computação (Universidade Cidade de São Paulo, 2026). É um agente de testes que abre um sistema web como uma pessoa abriria, percebe quando algo quebrou, diz por que quebrou e, quando a causa é só um seletor que mudou, conserta o próprio teste. Tudo roda na máquina de quem testa: o modelo de linguagem é local (Ollama, só CPU, sem nuvem).

> **Em 05/11/2026:** a Fase 4, em que o agente passa a trabalhar na tela de verdade, está em andamento, com quatro corridas por fazer antes da Fase 5. Os números da tela ainda podem mudar quando elas rodarem.

| Quero... | Vá para |
|---|---|
| Entender o projeto e ver os resultados | as seções abaixo |
| Explorar cada resultado, um assunto por aba | [Painel do projeto](https://claude.ai/artifact/LhXeAccx5NMk1HprycHApN) |
| Ler o trabalho formal, nas normas da ABNT | [Documento do TCC em Word](Documentacao/TCC_v3_20261105.docx) e a [fonte em Markdown](Documentacao/TCC%20-%20ABNT%2014724%20-%20V1.md) |
| Ver scripts, configurações e os valores de cada rodada | [Detalhes técnicos](DETALHES-TECNICOS.md) |
| Ver o número exato por trás de cada figura | [Dados das figuras](Documentacao/figuras/dados-das-figuras.md) |
| Saber o que foi decidido e por quê | [Memorial](Documentacao/Memorial%20de%20Desenvolvimento.md), [roadmap](Documentacao/memorial/roadmap.md), [pendências](Documentacao/memorial/pendencias.md) e [relatório da Fase 4](Documentacao/memorial/3-resultados-e-analises/fase-4-relatorio.md) |
| Ver a cópia no repositório da disciplina | [squad-24-projeto](https://github.com/unicid-projeto-software-2026-2/squad-24-projeto) (privado; este repositório é o principal) |
| Instalar e rodar | [Instalar e rodar](#instalar-e-rodar) |

## O problema

Quando o front-end e a API de um sistema evoluem separados, a API pode mudar o formato de uma resposta sem avisar: um campo some, muda de nome ou de tipo. O teste de ponta a ponta falha, mas a mensagem raramente diz o motivo, e alguém precisa abrir o navegador, comparar a resposta com o combinado e achar a causa. Esse desencontro se chama **deriva de contrato**, e é o foco deste trabalho.

O segundo problema é mais simples. A tela muda um `id` ou um texto, o **localizador** do teste não acha mais o botão, e o teste quebra sem que o sistema tenha defeito nenhum.

O agente trata os dois: explica a causa da deriva de contrato e conserta sozinho o localizador. Ele também mantém a própria **biblioteca**, um conjunto de **verbetes**, fichas curtas de documentação sobre o sistema testado (um contrato, um erro conhecido, uma regra de negócio).

## Como o agente trabalha

![Fluxo do agente em seis passos, do roteiro na tela até os três resultados, com a trilha embaixo](Documentacao/figuras/como-o-agente-trabalha.png)

**Como ler:** siga as setas a partir do passo 1. O azul é código comum, que dá sempre o mesmo resultado. O laranja é o passo em que o modelo responde. As caixas cinza são o que sai no fim, e a trilha, embaixo, guarda tudo para quem for revisar.

**A ideia central:** o modelo dá a opinião e o código confere. Nada que o modelo escreve vai para a biblioteca, nem chega a quem lê como certeza, sem passar por uma conferência em código.

## Onde o projeto está

| Fase | A pergunta que ela responde | Estado |
|---|---|---|
| 1 | Temos um ambiente de teste controlado, com falhas que se repetem? | Concluída |
| 2-A | Um modelo local consegue diagnosticar sem documentação nenhuma? | Concluída |
| 2-B | Documentação escrita por pessoas ajuda? | Concluída |
| 3 | O próprio modelo consegue manter essa documentação? Qual modelo fica? | Concluída |
| 3-B | O resultado se sustenta com casos novos e com outro modelo lendo? | Concluída |
| Pré-Fase 4 | Modelos maiores cabem nesta máquina? Dá para abrir o raciocínio do agente? | Concluída |
| 4 | O agente funciona na tela de verdade, e não só em casos escritos? | Em andamento |
| 5 | Ele resolve mais rápido que uma pessoa? | Não iniciada |

**O que falta antes da Fase 5:**

- repetir as duas medidas na tela com o caso encurtado, porque o prompt, o texto que o modelo recebe, ficou maior que o limite do plano (corridas 18c e 21c, decisão 90);
- testar em separado duas mudanças no prompt, sem mexer no prompt do agente (corrida 23, decisão 91);
- conferir e ler outros 36 casos inéditos (corrida 24, decisão 92);
- rever o que o agente entrega ao analista, porque hoje os verbetes são difíceis de entender.

## O que já descobrimos

Cada figura responde a uma pergunta. O número exato de cada uma está em [Dados das figuras](Documentacao/figuras/dados-das-figuras.md), e as condições de cada rodada, em [Detalhes técnicos](DETALHES-TECNICOS.md).

<!-- fonte dos números desta seção: Documentacao/figuras/dados-das-figuras.md, gerado de resultados_alvo/ por gerar_figuras_documentos.py; adesão ao verbete errado: fase3/comparacao_fases.json, adesao_cega_2B_A5_pct; margem do ensaio: fase4/cenarios_v2.json, geral; erros pegos pelo selo baixo: fase4/calibracao.json, limiares; lote nos inéditos: fase4/biblioteca.json, regra_r5 e relatório da Fase 4, seção 7. -->

### A documentação faz diferença?

![Quatro linhas, uma por modelo, do acerto sem documentação até o acerto com a biblioteca escrita pelo modelo](Documentacao/figuras/documentacao-e-acerto.png)

**Como ler:** cada linha é um modelo, e cada ponto é quanto ele acertou nos mesmos 36 casos. Da esquerda para a direita, o modelo recebe mais ajuda. Linha subindo quer dizer mais causas certas.

**O que isso mostra:** a documentação certa ajuda os quatro modelos da figura, e quem acertava menos ganha mais: o `qwen2.5-coder:3b` sai de 19% para 69%. Só o `qwen2.5:7b` ganha mais de um caso com a biblioteca que ele mesmo escreveu, de 78% para 89%, e mesmo isso fica abaixo do que 36 casos conseguem comprovar. A linha do `granite4.2:8b` fica reta no último trecho porque nenhuma edição dele foi aceita. O outro lado é o risco: na Fase 2-B, o `granite4.2:8b` e o `qwen2.5-coder:3b` seguiram um verbete errado, acompanhado de um registro de incidente falso, em 93% e 96% dos casos. É por isso que nada entra na biblioteca sem conferência.

### Qual modelo ficou?

![Pontos por modelo: tempo por caso no eixo horizontal e acurácia balanceada no vertical, com o escolhido em destaque](Documentacao/figuras/escolha-do-modelo.png)

**Como ler:** cada ponto é um modelo com a biblioteca num certo estado. Quanto mais alto, mais acerta; quanto mais à esquerda, mais rápido. A **acurácia balanceada** é o acerto calculado causa por causa, com o mesmo peso para todas, para que responder sempre a causa mais comum não pareça bom. A linha vertical no ponto escolhido mostra a incerteza: com só 36 casos, o valor verdadeiro pode estar em qualquer lugar dela. Entre versões da biblioteca de um mesmo modelo, o tempo não se compara, porque foi medido em momentos diferentes da corrida.

**O que isso mostra:** pela regra fixada antes de rodar, ficou o `qwen2.5:7b` com a primeira versão da biblioteca escrita por ele (decisão 52), depois curada e guardada em `Programacao/AgenteCore/biblioteca_producao/`. O `qwen2.5-coder:3b` é bem mais rápido, mas acerta menos, e o `granite4.2:8b` acerta perto, mas leva mais de 120 segundos por caso.

### A biblioteca serve para qualquer modelo?

![Pares de barras: casos certos de cada modelo com a biblioteca original e com a biblioteca escrita pelo qwen2.5:7b](Documentacao/figuras/quem-le-a-biblioteca.png)

**Como ler:** cada par de barras é o mesmo modelo lendo os mesmos 36 casos. A barra cinza usa a biblioteca original, e a azul, a que o `qwen2.5:7b` escreveu.

**O que isso mostra:** quem escreveu ganha 4 casos, o `qwen2.5-coder:7b` ganha 1 e o `qwen2.5-coder:3b` perde 4. Por isso o padrão do agente é o modelo com a biblioteca que ele mesmo escreveu (decisão 69). E o ganho não é garantido em casos novos: em 36 casos inéditos, essa versão fez 26 certos, contra 27 da biblioteca original ([figura dos casos inéditos](Documentacao/figuras/casos-ineditos.png)).

### O agente sabe quando pode estar errado?

![Barras por selo de confiança, alto, médio e baixo, com os casos certos e errados de cada um](Documentacao/figuras/selo-de-confianca.png)

**Como ler:** cada barra reúne os casos que receberam o mesmo selo. O azul são os certos, e o laranja, os errados. O selo vem da probabilidade que o próprio modelo dá à causa que escolheu.

**O que isso mostra:** o selo separa os extremos. No alto, são 3 erros em 37 casos; no baixo, 15 em 27. Mandar para revisão só o selo baixo pega 15 dos 22 erros olhando 27 dos 90 casos. Os cortes de cada selo foram calculados nesses mesmos casos, então esse resultado ainda precisa se repetir em casos novos.

### Ler da tela é tão bom quanto ler um caso escrito?

![Três barras: casos certos lendo o caso escrito, a tela com o caso revisado e a tela na primeira versão](Documentacao/figuras/tela-e-caso-escrito.png)

**Como ler:** são os mesmos 37 casos. A barra de cima é o modelo lendo o caso escrito à mão. As de baixo são o mesmo caso montado a partir da tela, antes e depois de revisarmos como essa montagem é feita.

**O que isso mostra:** ler da tela ainda perde, 26 contra 31. A primeira versão dava 16, porque a montagem não dizia o que tinha mudado contra a tela normal. A regra fixada antes de rodar aceitava no máximo 3 casos em que um lado acerta e o outro erra, e foram 9; isso fica declarado como limitação (decisão 82). Além disso, os prompts na tela passaram do limite do plano ([figura do limite](Documentacao/figuras/prompt-e-limite.png)), e as duas medidas vão ser repetidas com o caso encurtado.

### Quanto tempo o agente leva?

![Barras por cenário de falha, com os segundos da detecção até o resultado](Documentacao/figuras/tempo-por-cenario.png)

**Como ler:** cada barra é um cenário de falha, rodado uma vez, do momento em que o agente percebe a falha até ter o resultado. No azul, o resultado é o diagnóstico conferido. No laranja, é o teste passando de novo depois do conserto.

**O que isso mostra:** os 10 cenários chegaram ao resultado, em 105 segundos na média. Quase todo esse tempo é o modelo pensando ([figura de onde vai o tempo](Documentacao/figuras/onde-vai-o-tempo.png)): o conserto de localizador só em código levou 0,64 segundo e funcionou nas 160 quebras armadas.

### O que o agente escreve entra na biblioteca sem controle?

![Funil: propostas do modelo, as que passam por cada conferência e as que ficam na biblioteca](Documentacao/figuras/funil-da-biblioteca.png)

**Como ler:** de cima para baixo, quantas propostas sobrevivem a cada conferência. Ao lado de cada etapa, o motivo mais comum de quem ficou pelo caminho.

**O que isso mostra:** das 92 propostas do modelo, 19 chegaram ao lote, e 11 ficaram na biblioteca depois da revisão. Esse lote não mudou nenhum acerto nos 36 casos inéditos. O que encurtou a distância da tela foi revisar a montagem do caso, não a biblioteca.

### O que ainda não dá para afirmar

- **Que o agente é mais rápido que uma pessoa.** Ainda não há a medida com pessoas; ela é a Fase 5.
- **Que os 10 de 10 se repetem.** Foi uma repetição por cenário, e com dez execuções a margem de incerteza vai de 72% a 100%.
- **Que o conserto de localizador funciona em qualquer quebra.** As 160 quebras foram armadas de propósito, com o elemento certo ainda na página.
- **Que a leitura da tela chegou ao nível do caso escrito.** A regra não foi cumprida, e as corridas 18c e 21c ainda vão rodar.
- **Que os sinais da trilha apontam os erros.** A corrida teve só 5 erros, poucos para pôr os sinais em ordem ([figura dos sinais](Documentacao/figuras/sinais-da-trilha.png)).
- **Que o relatório ajuda quem revisa.** A medida com revisor humano não foi feita (decisões 85 a 87).

## Os dois sistemas de teste

Medir sem depender de opinião pede um ambiente controlado. Por isso o repositório traz dois sistemas "cobaia", que compartilham o mesmo banco de dados, e falhas que podem ser ligadas e desligadas sempre do mesmo jeito.

| Sistema | O que é | Para que serve |
|---|---|---|
| **CobaiaFront** | Site PHP legado de um restaurante, mantido como veio | Falhas de página completa e erros clássicos de sistema antigo |
| **CobaiaAPI** | API JSON em Python (FastAPI), com injeção de falhas | Deriva de contrato em respostas reais, o foco do agente |

A avaliação usa 90 casos de falha com a resposta certa conhecida, e as regras de decisão são fixadas antes de cada rodada. A arquitetura e o detalhe de cada sistema estão em [Detalhes técnicos](DETALHES-TECNICOS.md#arquitetura).

## Instalar e rodar

Precisa de Windows 10/11, Linux ou macOS e de internet: o instalador baixa PHP, MariaDB e os pacotes Python que faltarem. No Linux, ele usa `sudo` e `apt-get`; no macOS, o [Homebrew](https://brew.sh).

**No Windows, o caminho mais curto** é dar dois cliques em `Cobaia.exe`: ele instala, sobe tudo e abre o navegador. Na primeira vez, o Windows pode mostrar "Windows protegeu seu PC", porque o arquivo não é assinado; clique em "Mais informações" e depois em "Executar assim mesmo".

**Por partes**, na raiz do repositório:

```
# Windows (clique duplo ou pelo terminal)
install.cmd
run.cmd
```

```bash
# Linux / macOS
./install.sh
./run.sh
```

Depois de subir:

- **CobaiaFront:** http://localhost:8080
- **CobaiaAPI (documentação interativa):** http://localhost:8000/docs

`Ctrl+C` encerra tudo. As contas de teste já vêm no banco:

| Login | Senha | Uso |
|---|---|---|
| `admin` | `admin123` | Painel do administrador (`/admin/login.php`) |
| `11122233344` | `123456` | Área do cliente, com reservas (mesmo formulário) |

Máquina sem administrador, o que o instalador faz passo a passo, os testes e as soluções para erros comuns estão em [Detalhes técnicos](DETALHES-TECNICOS.md#instalação-em-detalhe).

## Estrutura do repositório

```
TCC/
├── README.md                 # esta página
├── DETALHES-TECNICOS.md      # scripts, configurações e os valores de cada rodada
├── Cobaia.exe                # Windows: instala, roda e abre o navegador
├── install.* / run.*         # instalador e inicialização, nos três sistemas
├── ferramentas/              # scripts locais: painel, documento do TCC, conferências
├── claude-memoria/           # memória do Claude e os registros de passagem entre sessões
├── Documentacao/
│   ├── TCC - ABNT 14724 - V1.md   # fonte do documento do TCC (o nome fica "V1" em todas as versões)
│   ├── TCC_v3_20261105.docx       # documento do TCC em Word
│   ├── figuras/                   # as figuras desta página e a tabela de cada uma
│   ├── dashboard/                 # o painel do projeto
│   └── memorial/                  # decisões, pesquisa, relatórios, roadmap e pendências
└── Programacao/
    ├── AgenteCore/               # o agente, a biblioteca e as baterias de avaliação
    ├── CobaiaFront/              # o site PHP legado
    └── CobaiaAPI/                # a API com injeção de falhas
```

A árvore completa está em [Detalhes técnicos](DETALHES-TECNICOS.md#estrutura-do-repositório).

## Segurança

Este é um **ambiente de teste**: as senhas fracas, a injeção de SQL no CobaiaFront e o CORS liberado na CobaiaAPI são conhecidos e ficam de propósito, porque fazem parte do que o agente precisa enfrentar. Não reutilize esses padrões fora deste projeto. Problemas reais nos instaladores e nas ferramentas seguem a [política de segurança](SECURITY.md).

## Como contribuir

Leia o [guia de contribuição](CONTRIBUTING.md) (fluxo de trabalho, convenções,
o que nunca muda e os testes obrigatórios) e o
[código de conduta](CODE_OF_CONDUCT.md). Defeitos e propostas entram por issue,
com os modelos em `.github/ISSUE_TEMPLATE/`; pull requests seguem o modelo em
`.github/PULL_REQUEST_TEMPLATE.md`. Problemas de segurança reais seguem a
[política de segurança](SECURITY.md), pelo canal privado do GitHub.

## Como citar

O arquivo [`CITATION.cff`](CITATION.cff) alimenta o botão "Cite this repository"
do GitHub. Em texto:

> DERRE, E. C. et al. **Desenvolvimento de um agente de QA end-to-end (E2E)
> autônomo com capacidades de self-healing: focado na fronteira de integração.**
> Trabalho de Conclusão de Curso (Ciência da Computação). Universidade Cidade de
> São Paulo, São Paulo, 2026. Repositório: https://github.com/EricDerre/TCC.

## Licença

O código e a documentação deste repositório estão sob a [licença MIT](LICENSE).
Componentes de terceiros mantêm as próprias licenças: Bootstrap 3.3.7 e jQuery
(MIT) e PHPMailer 5.2.27 (LGPL 2.1, com o texto em
`Programacao/CobaiaFront/PHPMailer/LICENSE`) no CobaiaFront; AngularJS 1.6.9 e
Chart.js 4.4.1 carregados de CDN (MIT). Os notebooks de apoio do livro-texto
(Faceli et al., 3. ed., 2025) são material dos autores e da editora, ficam fora
do repositório e não estão cobertos por esta licença. Os modelos de
linguagem não são distribuídos aqui: o Ollama os baixa sob a licença de cada um
(Apache 2.0 para o `qwen2.5:7b` e o `qwen2.5-coder:7b`; Qwen Research License
para o `qwen2.5-coder:3b`).

## Autores

Grupo de Ciência da Computação da Universidade Cidade de São Paulo (UNICID),
2026: Eric Conde Derre, Erick do Carmo Esteves, Guilherme Penha dos Santos,
João Victor Fonseca Silva, Kennedy Fernando de Oliveira Gundim, Leandro
Henrique da Silva Patricio e Pedro Henrique Torres Gonçalves. O repositório é
mantido por
[@EricDerre](https://github.com/EricDerre).

## Convenções para alterações por IA

Ver [`.claude/CLAUDE.md`](.claude/CLAUDE.md) para as regras completas de
colaboração com IA neste repositório (não commitar automaticamente, marcar
alterações com `! Alteração de IA - Revisar`, conferir colunas reais antes
de escrever SQL, priorizar causa raiz sobre contorno).
