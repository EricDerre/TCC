<!-- ! Alteração de IA - Revisar: arquivo novo (07/11/2026): leitura feita por um subagente do Claude (modelo Sonnet) sobre repositório activeing123/mcptoon, na rodada 6 da pesquisa (Pós-Fase 4); é um arquivo de dados que ferramentas/integrar_pesquisa_pos_fase4.py lê para montar o levantamento §6.15, e o integrador tira este comentário do texto que entra lá.
     ! Motivo: o Eric pediu em 07/11/2026 a base de pesquisa de cada ponto da Pós-Fase 4 e a validação de oito repositórios do GitHub; a leitura fica versionada como dado para o levantamento ser regerado por script e conferido pelo --check. O texto é o que o subagente escreveu, sem edição, com a marca de confiança que ele deu a cada fonte (aberta e lida; só o resumo de busca; de memória). -->
# Repositório 03: activeing123/mcptoon

Fontes lidas em 7 nov. 2026: página https://github.com/activeing123/mcptoon e README bruto (raw.githubusercontent.com/.../HEAD/README.md). Os arquivos docs/faq.md, docs/real-world-benchmark.md e docs/tiktoken-benchmarks.md são citados no README, mas não foram abertos; os números abaixo vêm só do README e são medições do próprio autor.

## 1 O que é e como funciona por dentro

mcptoon é uma CLI local em Python, sem dependências, que faz de "porta única" para servidores MCP e skills de agentes. O objetivo é não mandar o esquema completo de todas as ferramentas a cada turno.

- Em vez do esquema inteiro, expõe um índice compacto de nomes (`manifest`). O esquema de uma ferramenta só vem sob demanda (`inspect`), e `call` executa. `select "<tarefa>"` devolve as poucas ferramentas mais prováveis.
- Para skills, um ponteiro residente custa 39 tokens e `skills resolve` devolve uma lista curta (791 tokens para 5 skills) ranqueada por BM25 offline.
- `call --toon` recodifica o resultado no formato TOON (padrão aberto, v4.1, MIT, github.com/toon-format/toon, via python-toon vendorizado). É uma codificação estruturada reversível; se a decodificação falha, cai para JSON. Há também o formato SLIM (nomes mais tipos dos parâmetros), criado pelo mcptoon e que não é TOON.
- Resultados byte a byte idênticos na sessão viram referência (dedup); `retrieve` recupera o original.
- Três modos: CLI (custo fixo zero por turno), serve (custo fixo pequeno, uma entrada MCP por stdio ou HTTP) e direct (todos os esquemas carregados, o mais caro). Uma instalação nova pode ficar em direct e não economizar nada até rodar `mcptoon quickstart`.
- Barreiras sobre resultados: bloqueio de ação destrutiva, varredura de injeção de prompt e detecção de vazamento de credencial.

Números de redução da página (todos medições do autor, com `tiktoken cl100k_base`):

| Amostra | Antes | Depois | Redução |
|---|---:|---:|---:|
| 255 ferramentas sintéticas, 50 servidores: JSON para TOON | 71.929 | 47.438 | 34% |
| mesma amostra, SLIM | 71.929 | 8.282 | 88,5% |
| mesma amostra, Compact | 71.929 | 581 | 99,2% |
| 7 servidores públicos reais, 209 ferramentas | 640.606 | 905 | 99,86% |
| máquina local, 212 esquemas (manifest) | 640.787 | 914 | 99,85% |
| máquina local, 480 arquivos de skill (ponteiro) | 1.572.330 | 39 | 99,99% |

Ressalvas que o próprio README faz: o 99,2% é "do lado da definição" (não carregar esquemas), não compressão de resultado, e cresce com o tamanho do catálogo. O ganho do TOON sobre resultados depende da forma: amostra mista 5,7% menor, faixa de 1,8% a 48,6% (lista de registros quase não encolhe, registro único cai pela metade), e o texto avisa para não assumir 34% fixos. Os números de terceiros (Anthropic 150.000 para 2.000; Firecrawl 1.365 contra 44.026; Scalekit 10 a 32 vezes mais barato) são citados, não medidos por ele. `mcptoon bench` mede o catálogo do usuário.

## 2 Pilha, dependências e exigências

- Linguagem: Python puro, só biblioteca padrão (CI verifica com `scripts/check_zero_deps.py`). Página descreve 41.185 linhas em 56 módulos. Pacote de 565 KB. Testes: "3035 passed, 2 skipped" (declarado).
- GPU: não. Nuvem: não é exigida; README diz sem telemetria. Única chamada externa: `install --search`, que consulta registros (Smithery, Registro MCP Oficial). Chave de API: não para o gateway em si (os servidores MCP que ele fronteia podem exigir as suas).
- Node: não para o núcleo; `uvx mcptoon demo --quick` exige Node. Instala por `pip install mcptoon`, pipx, venv, a partir do código-fonte, plugin do Claude Code ou Nix. Windows descrito como alvo de primeira classe.
- Licença: Apache-2.0 (com NOTICE creditando o padrão TOON). Declara-se projeto independente, sem vínculo com a Anthropic.
- Maturidade: 423 estrelas, 26 forks, 2 observadores, 535 commits em `main`, 1 issue e 1 pull request abertos. Data do último commit: não visto (a página mostra só a contagem, sem data). Data de criação: não vista. Versão ou release: não vista (as seções Releases e Tags não mostraram contagem). Contribuidores: não visto. Há pasta `docs/`, `claude-code-plugin/`, `skills/mcptoon`, `plugin/mcptoon-skills`.
- Ponto de cautela: projeto de terceiro, único autor aparente na página, com afirmações de compatibilidade (103 clientes, 3035 testes) que não pude verificar.

## 3 Aplicação ao desenvolvimento com o Claude Code neste projeto

Serve em tese, com ganho pequeno aqui. A economia do mcptoon vem de catálogos grandes de ferramentas MCP e de muitas skills. Este projeto já usa poucas integrações e o Claude Code do aplicativo já adia o carregamento de ferramentas (ferramentas diferidas aparecem só pelo nome e o esquema é buscado sob demanda), que é o mesmo mecanismo do `manifest` e `inspect`. Parte do ganho já existe sem instalar nada.

Onde poderia ajudar:
- Reduzir o custo fixo de esquemas se o Eric ligar muitos servidores MCP ao mesmo tempo. A regra do projeto (plugins e MCP fixados no início da sessão, para manter o cache de prefixo) vai no mesmo sentido, então o gateway só compensa se o número de servidores crescer.
- `skills resolve` com BM25 poderia aliviar listas longas de skills; a lista de skills desta sessão é grande, mas já é carregada como descrições de uma linha.
- `retrieve` e dedup de resultados repetidos, útil em sessões com muitas leituras iguais.

Custo de instalar e manter:
- Instalação em venv sem administrador é viável (`pip install mcptoon`, sem dependências). O custo real está em `mcptoon quickstart`, que reescreve a configuração dos clientes (takeover; há `restore`, `off` e `uninstall --dry`). Pelas regras deste projeto, o Claude não edita o `~/.claude.json` (memória do projeto: modo automático), então o Eric teria de rodar os comandos, com caminho completo e cwd em minúsculo.
- Mais uma peça entre o Claude e as ferramentas: se der erro, a depuração passa por ela. Atualizações exigem acompanhar um projeto de terceiro cujo ritmo de releases não vi.
- Mudar plugins e MCP no meio do trabalho quebra o cache de prefixo e invalida as medições de tokens do projeto; qualquer adoção exigiria medir antes e depois com `ferramentas/medir_tokens.py`.

## 4 Aplicação dentro do agente ou do produto

Não serve em nenhum módulo. O agente não usa MCP: o harness em Python chama o Ollama, o Playwright e o BM25 próprio diretamente. O mcptoon resolve um problema (esquema de ferramentas MCP inflando o contexto) que o agente não tem.

Módulo por módulo:
- Poda: não aplicável. A poda decide o que do DOM e do corpo da resposta entra no prompt, é regra em código sobre dados da aplicação-alvo, não esquemas de ferramentas.
- Busca: já existe BM25 com sinais em código sobre 40 verbetes. O `skills resolve` do mcptoon também usa BM25, mas sobre skills, sem os sinais próprios e sem o frontmatter do projeto. Trocar a busca atual por ele perderia os sinais contra a referência (decisão 97) e exigiria remedir a recuperação.
- Diagnóstico: aqui está o conflito central. O prompt do diagnóstico é congelado byte a byte; qualquer recodificação do contexto (por exemplo, passar o corpo ou o diff em TOON) muda os bytes enviados ao qwen2.5:7b e obriga a medir tudo de novo (corridas 16 a 24). O TOON ainda economiza só 1,8% a 48,6% conforme a forma, e um modelo de 7B em CPU nunca foi avaliado lendo TOON, então a precisão do rótulo poderia cair. A tela já está no limite de 1.409 tokens medido em `medir_prompt_tela.py`; um ganho de tokens poderia ajudar nisso, mas só ao custo de reabrir o prompt congelado.
- Trilha e relatório: a trilha v2 é JSONL por passo e o relatório Markdown é gerado por código, ambos legíveis por pessoas e pelos testes. Trocar por TOON não traria ganho para o modelo (a trilha não vai ao prompt) e quebraria a leitura direta e as ferramentas de avaliação.
- Cura de seletor, painel e hub do analista: nenhum usa esquemas MCP. O painel é HTML estático gerado por Python.

Conflitos com as restrições do contexto:
- Prompt congelado: conflito direto, como acima.
- Harness só com a biblioteca padrão: o mcptoon também é só biblioteca padrão, então não conflita nesse ponto, mas adicionaria um pacote de 41 mil linhas de terceiro ao ambiente sem necessidade.
- Nada em nuvem: o núcleo roda local, mas `install --search` consulta registros externos; teria de ficar desligado. Não há administrador, o que a instalação em venv contorna.
- Um modelo residente por vez, num_ctx 8192, CPU: o mcptoon não consome RAM relevante (CLI sem daemon), então não conflita; também não ajuda o gargalo, que é a inferência do 7B.
- Medição: qualquer mudança na forma dos dados lidos pelo modelo invalida as leituras vigentes (`tela_v4`, `cenarios_v4`).

## 5 Risco, esforço e veredito

Claude Code (desenvolvimento)
- Risco: médio-baixo. Reescreve a configuração de clientes (reversível por `restore`), é projeto de terceiro de um autor, com avisos de segurança próprios (injeção de prompt, vazamento) cuja eficácia não vi testada. Mexe no prefixo e no cache.
- Esforço: cerca de 1 sessão para instalar em venv, rodar `mcptoon bench` no catálogo real e comparar tokens antes e depois; mais 1 sessão se for adotado e precisar de manutenção. O Eric precisa executar os comandos que tocam o `~/.claude.json`.
- Veredito: só vale testar com `mcptoon bench` e `--dry` se o número de servidores MCP crescer; hoje o ganho é pequeno porque o Claude Code já adia os esquemas, então não adotar agora.

Agente (produto do TCC)
- Risco: alto para o rigor da pesquisa, porque tocar na forma do contexto lido pelo modelo reabre o prompt congelado e invalida as corridas 16 a 24.
- Esforço: 3 ou mais sessões (adaptar a poda, remedir a calibração, a tela, a cura e a biblioteca) para um ganho de 1,8% a 48,6% em formas de dado específicas, sem evidência de que o qwen2.5:7b lê TOON com a mesma precisão.
- Veredito: não aplicar; no máximo registrar o TOON como trabalho futuro e citar o resultado do autor como referência de redução de tokens por serialização.

## 6 Referências ABNT NBR 6023

ACTIVEING123. **mcptoon**: one zero-dependency MCP gateway CLI for every server and agent skill. [S. l.]: GitHub, [20--?]. Disponível em: https://github.com/activeing123/mcptoon. Acesso em: 7 nov. 2026.

ACTIVEING123. **README do mcptoon**. [S. l.]: GitHub, [20--?]. Disponível em: https://raw.githubusercontent.com/activeing123/mcptoon/HEAD/README.md. Acesso em: 7 nov. 2026.

TOON FORMAT. **TOON**: Token-Oriented Object Notation, especificação v4.1. [S. l.]: GitHub, [20--?]. Disponível em: https://github.com/toon-format/toon. Acesso em: 7 nov. 2026. (Citada pelo README; não aberta diretamente.)

ANTHROPIC. **Code execution with MCP**. [S. l.]: Anthropic, [20--?]. Disponível em: https://www.anthropic.com/engineering/code-execution-with-mcp. Acesso em: 7 nov. 2026. (Citada pelo README; não aberta diretamente, ano não visto.)

MCP-ZERO. arXiv:2506.01056. Disponível em: https://arxiv.org/abs/2506.01056. Acesso em: 7 nov. 2026. (Citada pelo README; autores e título não vistos, conferir antes de usar no TCC.)

FIRECRAWL. **MCP vs CLI**. Disponível em: https://www.firecrawl.dev/blog/mcp-vs-cli. Acesso em: 7 nov. 2026. (Citada pelo README; não aberta; benchmark de terceiro, tratar como não verificado.)

SCALEKIT. **MCP vs CLI use**. Disponível em: https://www.scalekit.com/blog/mcp-vs-cli-use. Acesso em: 7 nov. 2026. (Citada pelo README; não aberta; benchmark de terceiro, tratar como não verificado.)
