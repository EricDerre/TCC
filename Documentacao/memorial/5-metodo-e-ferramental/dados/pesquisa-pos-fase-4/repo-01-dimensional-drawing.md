<!-- ! Alteração de IA - Revisar: arquivo novo (07/11/2026): leitura feita por um subagente do Claude (modelo Sonnet) sobre repositório enesozturk/dimensional-drawing, na rodada 6 da pesquisa (Pós-Fase 4); é um arquivo de dados que ferramentas/integrar_pesquisa_pos_fase4.py lê para montar o levantamento §6.15, e o integrador tira este comentário do texto que entra lá.
     ! Motivo: o Eric pediu em 07/11/2026 a base de pesquisa de cada ponto da Pós-Fase 4 e a validação de oito repositórios do GitHub; a leitura fica versionada como dado para o levantamento ser regerado por script e conferido pelo --check. O texto é o que o subagente escreveu, sem edição, com a marca de confiança que ele deu a cada fonte (aberta e lida; só o resumo de busca; de memória). -->
# Repositório 01: enesozturk/dimensional-drawing

Fontes lidas: página do repositório no GitHub e README bruto (raw.githubusercontent.com). Não há pasta docs/ nem artigo citado; o README cita apenas a página de desenhos dimensionais da Apple e um post no X.

## 1 O que é e como funciona por dentro

- É um conjunto de duas "skills" de agente (pastas com SKILL.md em Markdown, mais exemplos e modelos). Não é biblioteca nem programa: é texto de instrução que o agente carrega.
- A skill `dimensional-drawing` manda o agente transformar um componente de interface (cartão, diálogo) em uma folha técnica de uma página, no estilo dos desenhos dimensionais da Apple. A folha traz bloco de título, notas, vista em planta, camadas explodidas, vistas de detalhe e tabelas de variáveis.
- O mecanismo é um conjunto de regras de redação: só tons de cinza; rótulos de arquitetura e não de conteúdo (por exemplo `TITLE SLOT · FLEX`); relações como variáveis (`H1 = 2·S1 + H3`) e não números soltos; nomes neutros (`UI-CARD-001`); valores desconhecidos marcados `[TBD]` em vez de inventados.
- A entrada é uma fonte indicada pelo usuário (arquivo do repositório, story do Storybook, URL ou captura de tela). A saída são arquivos HTML (há exemplos de cartão e diálogo).
- A segunda skill, `dimensional-drawing-motion`, anima a folha pronta em um filme de cerca de 10 s (aproximação, planta, camadas se separando, recuo). Tem dois adaptadores: o artefato Motion do Claude (alvo principal) e um renderizador headless com Playwright e ffmpeg.

## 2 Pilha, dependências e exigências

- GPU: não. Nuvem: a skill de desenho roda no agente que a carrega; o caminho principal da skill de movimento usa o artefato Motion do Claude (serviço do Claude, não local). Chave de API: não citada pelo repositório. Outro modelo residente: não.
- Skill de desenho: só um agente com suporte a skills (Claude Code, claude.ai, Claude desktop ou qualquer agente via `npx skills add`).
- Skill de movimento headless: Node 18 ou superior, ffmpeg e pacotes npm incluindo Playwright (Chromium). Remotion, Motion Canvas, GSAP e Lottie não foram testados.
- Licença: MIT (Enes Ozturk).
- Maturidade: cerca de 1,9 mil estrelas, 136 forks, 4 pull requests abertos, tópicos skills e ui. Histórico com um único commit visível. Data de criação, data do último commit e releases: não visto (a página mostra Releases e Packages vazios; procurei na página do repositório e no README).

## 3 Aplicação ao desenvolvimento com o Claude Code neste projeto

- Serve? Praticamente não. O assunto é desenho técnico de componentes de interface, e este projeto não projeta interface própria de produto: o painel é HTML estático gerado por Python, e a interface do analista está adiada para depois da Fase 4.
- Uso marginal possível: gerar uma folha de especificação do painel ou do futuro hub do analista como figura para o documento do TCC. É estética, não ganho de método.
- Custo de instalar: baixo (copiar duas pastas para `~/.claude/skills/`). Manutenção: quase nula (texto), mas cada skill instalada entra na lista de skills do contexto e pesa um pouco no prefixo de cache, o que vai contra a regra de economia de tokens do projeto. A parte headless traria Node, ffmpeg e npm, runtimes que o projeto não usa.
- Recomendação: não instalar de forma permanente. Se houver necessidade pontual, ler o SKILL.md e copiar as regras (variáveis em vez de números, `[TBD]` em vez de invenção) para uma instrução local.

## 4 Aplicação dentro do agente ou do produto

- Serve? Não, em nenhum módulo (poda, busca, diagnóstico, trilha e relatório, cura de seletor). O repositório não faz nada com DOM, seletores, falhas de teste ou diagnóstico.
- Painel ou hub do analista: único módulo com alguma ligação, e só como inspiração de apresentação (folha com título, notas e tabela de variáveis). Não há código reaproveitável.
- A ideia "valores desconhecidos viram `[TBD]`, nunca inventados" é parente da regra do projeto de validar em código e não confiar no modelo, mas já está coberta pela trilha v2 e pelos relatórios gerados por código.
- Conflitos com o contexto:
  - Prompt congelado byte a byte: incluir qualquer skill ou texto novo no diagnóstico obrigaria a medir tudo de novo.
  - Só biblioteca padrão no harness em Python: a parte headless exige Node 18+, npm, ffmpeg e Playwright via npm.
  - Sem administrador no Windows 11 corporativo: instalar Node e ffmpeg pode esbarrar na restrição.
  - Nada em nuvem: o alvo principal da skill de movimento é o artefato Motion do Claude.
  - Um modelo residente por vez em CPU: gerar folhas e filmes por LLM competiria com o qwen2.5:7b, e um 7B local não teria a qualidade de agente esperada pela skill.
  - Relatório gerado por código: a folha da skill é escrita pelo modelo, o oposto da regra "primeiro a máquina, depois o modelo".

## 5 Risco, esforço e veredito

- Risco: baixo para o Claude (arquivos de texto, licença MIT), mas com custo de contexto e de dispersão. Para o agente: alto em relação ao ganho, porque violaria várias restrições sem benefício para o diagnóstico.
- Esforço: Claude, cerca de meia sessão para instalar e testar uma folha do painel; agente, não se aplica (nenhuma sessão recomendada).
- Veredito para o Claude Code: não adotar; no máximo uso pontual para uma figura do painel, sem instalação permanente.
- Veredito para o agente: não serve; sem módulo de aplicação e com conflito com prompt congelado, biblioteca padrão, ausência de nuvem e CPU única.

## 6 Referências ABNT NBR 6023

- OZTURK, Enes. **dimensional-drawing**: agent skills para criar desenhos dimensionais de componentes de interface. Disponível em: https://github.com/enesozturk/dimensional-drawing. Acesso em: 7 nov. 2026.
- Artigos citados pelo repositório: nenhum artigo científico. Os links do README são páginas de terceiros, listados para rastreio:
  - APPLE. **Accessories: dimensional drawings**. Disponível em: https://developer.apple.com/accessories/dimensional-drawings/. Acesso em: 7 nov. 2026. (citada pelo README, não aberta por mim)
  - STORM, Andreas. Publicação no X. Disponível em: https://x.com/avstorm. Acesso em: 7 nov. 2026. (citada pelo README, não aberta por mim; título e data não vistos)
