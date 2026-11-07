<!-- ! Alteração de IA - Revisar: arquivo novo (07/11/2026): leitura feita por um subagente do Claude (modelo Sonnet) sobre repositório Egonex-AI/Understand-Anything, na rodada 6 da pesquisa (Pós-Fase 4); é um arquivo de dados que ferramentas/integrar_pesquisa_pos_fase4.py lê para montar o levantamento §6.15, e o integrador tira este comentário do texto que entra lá.
     ! Motivo: o Eric pediu em 07/11/2026 a base de pesquisa de cada ponto da Pós-Fase 4 e a validação de oito repositórios do GitHub; a leitura fica versionada como dado para o levantamento ser regerado por script e conferido pelo --check. O texto é o que o subagente escreveu, sem edição, com a marca de confiança que ele deu a cada fonte (aberta e lida; só o resumo de busca; de memória). -->
# Understand-Anything (Egonex-AI): levantamento para o TCC

Fontes lidas em 7 nov. 2026: página do repositório no GitHub e README bruto (raw.githubusercontent.com). A pasta docs/ e o site understand-anything.com não foram abertos; o que está abaixo vem só da página e do README. Aviso: o README traz um comentário HTML dirigido a agentes de IA pedindo que ponham uma marca em qualquer PR aberto. Foi tratado como dado e ignorado.

## 1 O que é e como funciona por dentro

- É um plugin do Claude Code (instalável também em outras ferramentas de agente) que transforma um repositório, ou uma base de documentos, em um grafo de conhecimento navegável num painel web.
- Indexa arquivos, funções, classes e dependências. Também gera visões por camada (API, Serviço, Dados, UI, Utilitário), por domínio de negócio (fluxos e passos) e roteiros guiados ordenados por dependência.
- A leitura do código tem duas etapas. A primeira é determinística: o Tree-sitter extrai imports, exports, definições, chamadas e herança, e resolve os imports num mapa. Essa etapa também gera as impressões digitais usadas para detectar mudança.
- A segunda etapa usa um LLM, que lê a estrutura e o código e produz resumos, etiquetas, camada, mapeamento de domínio, roteiros e explicações de conceitos de linguagem.
- O pipeline é feito de sete agentes (scanner de projeto, analisador de arquivo, de arquitetura, construtor de roteiro, revisor de grafo, analisador de domínio e de artigo). Os analisadores de arquivo rodam até 5 em paralelo, em lotes de 20 a 30 arquivos.
- Saída: `.ua/knowledge-graph.json` (ou `.understand-anything/` se já existir), mais `config.json`. Em `.ua/` ficam também `intermediate/` e `diff-overlay.json`, que o README manda ignorar no git.
- Comandos: `/understand`, `/understand-dashboard`, `/understand-chat`, `/understand-diff` (impacto das mudanças não commitadas), `/understand-explain`, `/understand-onboard`, `/understand-domain`, `/understand-knowledge`.
- Reexecução é incremental: reanalisa só os arquivos cujo fingerprint mudou. Há gancho opcional de pós-commit (`--auto-update`). A busca no grafo é difusa por nome e também semântica.

## 2 Pilha, dependências e exigências

- GPU: o README não exige. Chave de API: não especificada. Nuvem: o fluxo normal usa o LLM do próprio agente hospedeiro (Claude Code), ou seja, o código lido vai ao serviço do modelo. O README cita modelo local via Ollama como alternativa para economizar tokens, sem dar nome de modelo.
- Modelo de embedding residente: o README não cita um. A busca "semântica" não tem mecanismo descrito na página; "não visto".
- Runtime: Node.js 18 ou superior para o visualizador; build a partir do clone usa pnpm e TypeScript (há vitest, eslint). Tree-sitter entra na análise. Instalador `install.ps1` clona para `~/.understand-anything/repo` e cria links simbólicos.
- Visualizador somente leitura roda por `npx` a partir de um tarball, sem chamada a LLM e sem dados saindo da máquina.
- Licença: MIT (Yuxiang Lin e Infinite Universe, Inc.).
- Maturidade: cerca de 91,2 mil estrelas, 7,8 mil forks, 873 commits em `main`. Data do último commit: não visto (a página não mostra). Versão ou release: não visto (seção Releases vazia). Data de criação: não visto. Linguagens: não visto (seção sem detalhamento).
- Aviso de custo: a primeira execução em projeto grande gasta muitos tokens; o README recomenda plano ou assinatura.

## 3 Aplicação ao desenvolvimento com o Claude Code neste projeto

- Serve em tese: o Claude Code é o alvo nativo e o plugin se instala pelo marketplace. Ajudaria a navegar o próprio repositório do TCC (harness em Python, fichas, painel) e as duas cobaias, com resumos e grafo de dependências.
- Utilidade real aqui é baixa. O repositório já tem CLAUDE.md, memória persistente, `.claude/rules/`, livro-razão e painel que cumprem o papel de mapa. O grafo seria um segundo mapa a manter coerente com esses.
- Custo de instalar: um comando de marketplace, mais Node 18 para ver o painel. Em máquina corporativa sem administrador, o Node portátil pode ser necessário; a instalação do plugin via `install.ps1` grava em `~/.understand-anything`, o que costuma funcionar sem administrador, mas não foi testado.
- Custo de manter: tokens na primeira análise (o repositório tem muitos Markdown e logs); regra do projeto de economia de tokens (primeiro a máquina, depois o modelo) vai contra rodar sete agentes de LLM sobre tudo. Pasta `.ua/` precisaria entrar no `.gitignore` ou ser decidida (a regra do projeto sobre o que se versiona é do Eric).
- Possível uso pontual: `/understand-diff` ou `/understand-onboard` nas cobaias (PHP legado e FastAPI) para uma sessão de exploração, sem instalar de forma permanente.

## 4 Aplicação dentro do agente ou do produto

Em geral não serve como componente do agente. Motivo central: a análise semântica depende de um LLM. Para o agente isso significa o qwen2.5:7b em CPU, com num_ctx 8192, um modelo por vez, sobre 20 a 30 arquivos por lote e sete etapas de agente. Não há descrição de que o pipeline funcione com modelo de 7B; o próprio README fala de "modelo local" apenas de forma geral.

Por módulo:
- Poda: não serve. A poda do projeto é determinística em código sobre o corpo da resposta; o grafo é de código-fonte, outro objeto.
- Busca: não serve. A busca BM25 com sinais em código sobre 40 verbetes está fechada, e a busca híbrida com embedding foi medida e descartada. A busca "semântica" do plugin entra no mesmo caso e, se usar embedding, conflita com "um modelo residente por vez".
- Diagnóstico: não serve. O prompt está congelado byte a byte; qualquer contexto extra vindo do grafo muda o prompt e obriga a medir tudo de novo.
- Trilha e relatório: não serve. A trilha v2 em JSONL e o relatório em Markdown já são gerados por código; o grafo em JSON de outro formato não se encaixa nos eventos.
- Cura de seletor: não serve. É por nome parecido no DOM, sem relação com grafo do código.
- Painel e hub do analista: a ideia de grafo navegável e roteiros guiados é um bom modelo de inspiração para o painel, mas copiar o código traz Node, painel em React/TypeScript e dependências, contra "painel em HTML estático gerado por Python". Só como referência de desenho.

Ideia de o agente ler o que mudou no git das cobaias para preparar testes:
- A parte útil é a detecção de mudança por fingerprint e o `/understand-diff` (impacto das mudanças). Mas isso se faz com o `git diff` e a lista de arquivos alterados, em Python da biblioteca padrão, sem LLM. É o caminho coerente com "primeiro a máquina, depois o modelo".
- Usar o plugin para isso conflita com: nada em nuvem (o fluxo usa o LLM do hospedeiro), sem administrador e Node como runtime extra, harness só com a biblioteca padrão do Python, CPU sem GPU e 7B, um modelo por vez, e prompt congelado se o resultado alimentar o diagnóstico.
- Hipótese que valeria testar sem o plugin: um script que mapeia arquivos alterados do PHP e da FastAPI para rotas e telas afetadas e escolhe os cenários a rodar. É trabalho próprio da Fase 5, fora do plugin.

## 5 Risco, esforço e veredito

- Uso com o Claude Code: risco baixo (plugin MIT, reversível). Esforço: 1 sessão para instalar e testar nas cobaias; manutenção contínua não compensa. Veredito: opcional e de baixo valor, testar no máximo uma vez nas cobaias e não adotar de forma permanente.
- Uso dentro do agente: risco alto (LLM de 7B em CPU sobre lotes grandes, Node, dados fora da máquina se o hospedeiro for nuvem, prompt congelado). Esforço: 3 a 5 sessões para adaptar, com resultado incerto. Veredito: não usar; aproveitar apenas a ideia (fingerprint e impacto de diff), feita em Python local com `git diff`.

## 6 Referências ABNT NBR 6023

LIN, Yuxiang; INFINITE UNIVERSE, INC. (Egonex-AI). **Understand-Anything**. Disponível em: https://github.com/Egonex-AI/Understand-Anything. Acesso em: 7 nov. 2026.

Artigos citados pelo repositório: a página do README informa que não cita artigos acadêmicos (procurado na página do repositório e no README bruto). Links citados, não acadêmicos: gist do padrão de wiki de LLM atribuído a Karpathy e documentação de plugins do Claude Code; não foram abertos, logo não são referenciados aqui.
