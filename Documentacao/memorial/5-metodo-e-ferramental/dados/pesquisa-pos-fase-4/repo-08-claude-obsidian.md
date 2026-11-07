<!-- ! Alteração de IA - Revisar: arquivo novo (07/11/2026): leitura feita por um subagente do Claude (modelo Sonnet) sobre repositório AgriciDaniel/claude-obsidian, na rodada 6 da pesquisa (Pós-Fase 4); é um arquivo de dados que ferramentas/integrar_pesquisa_pos_fase4.py lê para montar o levantamento §6.15, e o integrador tira este comentário do texto que entra lá.
     ! Motivo: o Eric pediu em 07/11/2026 a base de pesquisa de cada ponto da Pós-Fase 4 e a validação de oito repositórios do GitHub; a leitura fica versionada como dado para o levantamento ser regerado por script e conferido pelo --check. O texto é o que o subagente escreveu, sem edição, com a marca de confiança que ele deu a cada fonte (aberta e lida; só o resumo de busca; de memória). -->
# claude-obsidian (AgriciDaniel)

Fonte: página do repositório, README bruto e docs/windows-wsl.md, lidos em 7 nov. 2026. A listagem de docs/ mostra 13 arquivos (install-guide, windows-wsl, methodology-modes-guide, retrieval-evaluation, entre outros); só li o windows-wsl.

## 1 O que é e como funciona por dentro

- É um plugin do Claude Code que trata uma pasta de arquivos Markdown como um "segundo cérebro". O Obsidian é só o visualizador: abre-se a mesma pasta com "Open folder as vault". O README diz que nenhum plugin do Obsidian é necessário.
- O que liga o Claude à pasta são skills (15) e agentes (3, somente leitura) do Claude Code, mais um núcleo de transação que é o único que escreve. Há também uma CLI em Python (`scripts/claude-obsidian.py`).
- Segue o padrão "LLM Wiki" de Karpathy (gist de 4 abr. 2026): fontes brutas imutáveis, uma wiki mantida pelo LLM e um arquivo de esquema com as convenções. Operações: ingest, query, lint.
- Fluxo: a pessoa joga fontes em `inbox/`. O `wiki-ingest` lê, extrai e gera páginas ligadas (fontes, conceitos, entidades, sessões), índices e mapas de conteúdo. Os originais ficam intactos, em cópias endereçadas por conteúdo. `wiki-query` responde a partir das notas, `save` guarda uma boa resposta como nota, `wiki-lint` checa contradições, órfãs e lacunas.
- Escrita segura: o Claude lê cada nota que vai tocar e guarda o hash SHA-256; os ajudantes devolvem rascunhos; tudo é aplicado em uma transação única, com diário de backups e `transaction recover`. Se a nota mudar no meio, a escrita para com conflito.
- O vault é marcado por `.claude-obsidian.json` ou pela variável `CLAUDE_OBSIDIAN_VAULT`. O `wiki-mode` escolhe a organização: genérico (padrão), LYT, PARA ou Zettelkasten. Trocar de modo não move notas antigas.
- Skills de extensão: autoresearch, canvas, defuddle (limpeza de páginas web), wiki-fold, wiki-retrieve, wiki-cli (usa a CLI oficial do Obsidian), obsidian-markdown, obsidian-bases, think.
- A página mostra arquivos de regras para outros hospedeiros (Cursor, Windsurf, Codex, Gemini), instalados por `scripts/setup-multi-agent.sh`.

## 2 Pilha, dependências e exigências

- Exigências declaradas: Claude Code, Python 3.11 ou mais novo, Obsidian (só para a parte visual) e Bash para os scripts de instalação. Git só para desenvolvimento e checkpoints.
- Node.js e chave de API: o README não diz que sejam necessários (procurei no README bruto e na página). Serviço em nuvem: o vault é local; o conteúdo que o Claude Code lê vai ao Claude, como qualquer arquivo. Pesquisa web, reranking remoto e checkpoints Git pedem aprovação.
- Instalação: `claude plugin marketplace add AgriciDaniel/claude-obsidian` e depois `claude plugin install claude-obsidian@agricidaniel-claude-obsidian`.
- Windows: o docs/windows-wsl.md diz que o Windows nativo (inclusive Git Bash) é somente leitura. Inspeção, simulação e busca funcionam; `transaction apply`, `init`, `adopt`, `migrate` e `mode set` são recusados com `UNSUPPORTED_PLATFORM`. Escrever exige WSL, Linux ou macOS. Os hooks SessionStart e Stop precisam de `python3` no PATH; o instalador do python.org só traz `python.exe`, e sem `python3` os hooks não fazem nada, em silêncio.
- Licença: MIT.
- Maturidade: 16,2 mil estrelas, 1,6 mil forks, 18 issues e 7 pull requests abertos, 351 commits em main, versão 3.0.1 (selo do README). Seção Releases vazia na página. Data do último commit: não visto (a página não mostra datas). Data de criação: não vista. Linguagens: percentual não visto; há Python, scripts Bash e Markdown.

## 3 Aplicação ao desenvolvimento com o Claude Code neste projeto

- Serve em tese: o Memorial do TCC (decisões, fichas, roadmap, levantamentos) e a biblioteca do TargetERP já são Markdown em pasta, que é exatamente o formato que o plugin espera. O Obsidian abriria essas pastas como vault sem mudar nada, e daria grafo, retroligações e busca para o Eric navegar.
- Obstáculo central: a escrita (ingest, save, init, adopt) só funciona em WSL, Linux ou macOS. Na máquina do Eric (Windows 11 corporativo sem administrador), habilitar WSL exige ativar recursos do Windows e reiniciar, o que normalmente pede administrador (o doc cita prompt elevado para reparo). Sem isso, o plugin é só leitura, ou seja, perde o sentido principal.
- O que o plugin faz de útil já existe aqui: CLAUDE.md, memória em Markdown, fichas, ingestão manual do Memorial e o painel HTML gerado por Python. Instalá-lo duplicaria a memória (um segundo índice, um segundo esquema) e criaria conflito com a regra do projeto de documentação em Markdown com tag de alteração de IA e decisões numeradas.
- Para a biblioteca de 1436 artigos do TargetERP: ela já tem frontmatter e índice JSON lido pelo Claude Code. O `wiki-lint` (órfãs, contradições, lacunas) seria a parte mais aproveitável, mas dá para obter o mesmo com um script local de Python, em linha com a regra "primeiro a máquina, depois o modelo".
- Custo de instalação e manutenção: plugin de terceiros com 15 skills e hooks, versão 3.x ainda em mudança; revisão de segurança antes de rodar em repositório corporativo; manter sincronizado com a atualização do Claude Code. Obsidian sem administrador: não verifiquei na fonte. O README não trata disso; a CLI oficial do Obsidian é opcional. Não afirmo nada além disso.
- Uso viável sem custo: abrir o Memorial no Obsidian só como leitor, se o Eric já tiver o app instalado. Isso não depende do plugin.

## 4 Aplicação dentro do agente ou do produto

- Não serve. O agente de QA roda offline com Ollama qwen2.5:7b só em CPU, harness em Python com biblioteca padrão. O plugin é um complemento do Claude Code (nuvem), exige Python 3.11 com transações e hooks, e é feito para um humano alimentar uma wiki, não para um laço automático de teste.
- A ideia aproveitável é o formato: notas atômicas pequenas, ligadas por links explícitos, com frontmatter e um índice, mais o ciclo ingest, query e lint (checar órfãs e contradições). A biblioteca de verbetes do agente já é recuperada e validada por código; adicionar campos de ligação entre verbetes (ex.: "relacionado a") e um lint local de verbetes órfãos ou duplicados seria barato e compatível com biblioteca padrão. O modelo de escrita em transação com hash e backup também é uma boa prática para o agente gravar verbetes novos sem corromper a biblioteca, mas é uma ideia, não precisa do plugin.

## 5 Risco, esforço e veredito

- Risco: médio. Plugin de terceiros popular mas jovem (padrão Karpathy de abr. 2026), com hooks que rodam no início e fim de sessão; escrita bloqueada no Windows nativo; possível duplicação da memória do projeto; dependência de WSL, que o ambiente corporativo pode proibir.
- Esforço: de 1 a 2 sessões só para testar a leitura no Windows nativo (instalar o plugin, rodar `wiki-lint` em modo simulação sobre uma cópia do Memorial); mais 2 a 3 sessões se WSL puder ser habilitado, mais a revisão de segurança. Para o agente: 0 sessões (não aplicar); 1 sessão para um lint de ligações na biblioteca de verbetes, por script próprio.
- Veredito para o Claude Code: não instalar agora; o ganho é pequeno diante do que o CLAUDE.md, a memória e a biblioteca indexada já fazem, e a escrita não roda no Windows sem WSL. Vale só ler o padrão de Karpathy e copiar o lint por script.
- Veredito para o agente: não serve como componente; apenas a ideia de notas ligadas com lint pode inspirar a biblioteca de verbetes.

## 6 Referências ABNT NBR 6023

AGRICIDANIEL. **claude-obsidian**: self-organizing AI second brain for Obsidian + Claude Code. Disponível em: https://github.com/AgriciDaniel/claude-obsidian. Acesso em: 7 nov. 2026.

KARPATHY, Andrej. **LLM Wiki**. 4 abr. 2026. Disponível em: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f. Acesso em: 7 nov. 2026.

KEPANO. **obsidian-skills**. Disponível em: https://github.com/kepano/obsidian-skills. Acesso em: 7 nov. 2026. (Citada no README; não lida por mim.)

AGRICIDANIEL. **Windows e WSL**. In: claude-obsidian, docs/windows-wsl.md. Disponível em: https://github.com/AgriciDaniel/claude-obsidian/blob/main/docs/windows-wsl.md. Acesso em: 7 nov. 2026.
