<!-- ! Alteração de IA - Revisar: arquivo novo (30/09/2026) com o guia de contribuição do repositório: fluxo de trabalho, convenções de código e de documentação, o que nunca muda, testes obrigatórios e a regra das alterações feitas com IA.
     ! Motivo: a lista de padrões de comunidade do GitHub marcava "Contributing" como pendente; as regras já existiam espalhadas (CLAUDE.md, .claude/rules/, README) e quem chegasse de fora não as encontraria num lugar só. Nada aqui é regra nova: é o que o grupo já pratica. -->
# Como contribuir

Este repositório é o Trabalho de Conclusão de Curso de um grupo de nove pessoas (Ciência da Computação, UNICID, 2026). Contribuições de fora do grupo são bem-vindas, de preferência começando por uma issue. Ao participar, você concorda com o [Código de Conduta](CODE_OF_CONDUCT.md).

## Antes de começar

1. Leia o [README](README.md): ele explica o que é o ambiente-alvo, o que já foi medido e como instalar e rodar tudo.
2. Instale o ambiente pelo caminho descrito lá (`Cobaia.exe` no Windows ou `install.*` nos três sistemas). Os experimentos com modelos locais só precisam do Ollama; o site e a API não.
3. Veja o [painel do projeto](https://claude.ai/artifact/LhXeAccx5NMk1HprycHApN) e o [roadmap](Documentacao/memorial/roadmap.md) para saber em que fase o trabalho está e o que ainda falta rodar.

## Fluxo de trabalho

1. **Abra uma issue** (há um modelo para defeito e outro para proposta) descrevendo o que quer mudar e por quê.
2. **Crie um ramo** a partir de `main` com nome curto e descritivo, por exemplo `correcao/instalador-mariadb` ou `experimento/recuperador-k5`.
3. **Faça commits pequenos**, com mensagem em português, no imperativo e com um assunto por commit (`Corrige a detecção do PHP no instalador`).
4. **Abra um pull request** preenchendo o modelo. Um integrante do grupo revisa; quem revisa não é quem escreveu.
5. Quem commita e faz o merge é sempre uma pessoa. Assistentes de IA nunca commitam neste repositório.

## Convenções de código

- **Python:** PEP 8, nomes em `snake_case` e em português (`carregar_biblioteca`, `avaliar_registro`), verificados com `ruff`. Só biblioteca padrão nos scripts de `experimentos/` e de `ferramentas/`; a CobaiaAPI usa o que está em `requirements.txt`.
- **PHP do CobaiaFront:** é código legado cedido por um integrante e fica **intocado**, inclusive os defeitos listados no README em "Problemas conhecidos". Correções entram só na CobaiaAPI ou nos instaladores.
- **PowerShell (`.ps1`):** sempre em UTF-8 com BOM e sem travessão nas strings; o Windows PowerShell 5.1 lê o arquivo sem BOM na página de código ANSI e o travessão quebra o parse.
- **SQL:** conferir as colunas reais das tabelas antes de escrever uma consulta; não assumir nomes por convenção.
- **Comentários:** linguagem técnica amarrada ao processo real (função, tabela, tela, mensagem de erro), sem jargão teórico.

## O que nunca muda

- `executar_fase3.py`, `estrategias.py` e `evolucao_biblioteca.py`: são o executor, o prompt e o validador pré-registrados da Fase 3. Testes novos vivem em arquivos novos (`executar_fase3b.py` é o exemplo).
- `Programacao/AgenteCore/base_conhecimento/`: a biblioteca original nunca é escrita por script.
- `Programacao/AgenteCore/experimentos/resultados_alvo/`: registros oficiais das baterias. Nunca são editados à mão nem regenerados; os documentos derivados (`decisao_modelo.md`, `tabelas_relatorio.md`, os blocos colados no Memorial, o painel) saem de scripts com a opção `--check`, que acusa qualquer diferença.
- Nenhum número de resultado é digitado à mão em documento nenhum: todo valor vem de um JSON de registro, citado na primeira menção.

## Alterações feitas com IA

Todo trecho criado ou alterado por um assistente de IA leva, no comentário da linguagem, a tag `! Alteração de IA - Revisar:` seguida do que foi feito e, na linha seguinte, `! Motivo:` com o defeito ou a necessidade real que motivou a mudança. A tag nunca vem sozinha. Em `.cmd`/`.bat` a tag vai sem acento (`! Alteracao de IA - Revisar`). As regras completas estão em [`.claude/CLAUDE.md`](.claude/CLAUDE.md) e em [`.claude/rules/`](.claude/rules/); o script `ferramentas/conferir_docs.py` confere se todo arquivo tocado tem tag e motivo.

## Testes obrigatórios antes de abrir o pull request

```powershell
# CobaiaAPI (roda contra o banco real; instale antes)
cd Programacao\CobaiaAPI
.venv\Scripts\python.exe -m pytest -v
.venv\Scripts\python.exe -m ruff check .

# Experimentos (sem chamar modelo; menos de um minuto)
cd ..\AgenteCore\experimentos
python testar_fase3.py
python testar_fase3b.py

# Painel e documentação
cd ..\..\..
python ferramentas/testar_painel_textos.py
python ferramentas/testar_painel_topicos.py
python ferramentas/gerar_dashboard.py --check
python ferramentas/conferir_docs.py
```

No Linux e no macOS, troque `.venv\Scripts\python.exe` por `.venv/bin/python`.

## Documentação

- Decisões numeradas em `Documentacao/memorial/1-decisoes-e-historico/decisoes.md`; pendências em fichas em `Documentacao/memorial/pendencias.md`; estado por fase em `Documentacao/memorial/roadmap.md`.
- Toda análise nova ganha uma aba no painel (`ferramentas/painel_topicos.py`) e uma entrada no Memorial. Depois de mudar `pendencias.md`, `roadmap.md` ou um registro de resultado, regere o painel com `python ferramentas/gerar_dashboard.py`.
- Texto corrido sem travessões e sem setas; blocos de código, comandos e diagramas ficam como estão.

## Experimentos com modelos locais

- Um modelo residente no Ollama por vez, sempre em CPU (`num_gpu=0`) e com contexto de 8.192 tokens: é a condição experimental declarada no projeto.
- Baterias longas rodam na máquina-alvo (notebook i5, 16 GB) e gravam em `resultados_alvo/`; tempos só são comparáveis dentro da mesma pasta.
- Antes de propor uma bateria nova, abra uma issue de proposta com a pergunta que ela responde, o número de inferências e o tempo estimado.
