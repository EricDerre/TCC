<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
# O que foi construído, por commit

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá.

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
| *(working tree)* | 02–03/09 | Fase 2-A: taxonomia (6 classes × 3 níveis, 23 causas raiz), banco de 90 casos, três estratégias de prompt, bateria resumível um modelo por vez, avaliação e 6 gráficos. Fase 2-B (preparada em 03/09; execução iniciada na mesma noite): biblioteca base com 36 verbetes em `AgenteCore/base_conhecimento/`, módulos `biblioteca.py` (parser/validador), `recuperacao.py` (BM25 + sinais em código + contextos A1–A5), `validar_banco.py`, `verificar_cache_prefixo.py`, `gerar_relatorio.py`; `avaliar.py` com Δ, McNemar, Wilson, ancoragem e flips; 5 gráficos novos. Correções de revisão: `FAULT_TARGET_FIELD` no `.env` (o modo por variável de ambiente não agia sem campo-alvo), desligamento limpo do MariaDB via `mariadb-admin`, checagem exata do modelo no `ollama list`, 10 testes novos na CobaiaAPI (13 passando), decomposição de tempo do Ollama gravada por inferência |

**Componentes resultantes:** `CobaiaFront` (PHP legado, intocado exceto por um link de menu e uma página nova); `CobaiaAPI` (FastAPI, 5 endpoints, 7 modos de injeção de falha); instalador único (`install.*`/`run.*`/`Cobaia.exe`) idempotente para Windows e Linux; e `AgenteCore/experimentos` com o harness de benchmark.


