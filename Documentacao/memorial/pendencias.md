<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
# Pendências e questões em aberto

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá.

## 8. Pendências e questões em aberto

- **Regerar o PDF** do projeto de pesquisa a partir do Markdown corrigido, e remover os comentários de marcação antes da entrega final.
- **Fichamento formal** das 7 referências: o recorte de cada uma já está embutido nas seções 2.2 a 2.6 do projeto de pesquisa, mas não existe documento de fichamento separado.
- **Padrão de produção do modelo**: `qwen2.5-coder:3b` permanece na comparação com licença de pesquisa documentada; a escolha do padrão distribuível precisa recair sobre uma opção Apache 2.0 ou MIT.
- **Validação em Linux**: o instalador foi testado apenas em Windows. Os caminhos de `apt` e `brew` seguem convenções estabelecidas, mas não foram executados.
- **Critérios de aceitação quantitativos**: definidos no planejamento (fórmula de MTTR, Task Success, linha de base manual, volume), mas ainda não incorporados ao corpo do projeto de pesquisa além da §3.4.
- **Fase 2-B pronta para rodar na máquina-alvo** (i5-1235U, 16 GB; decisão 25, 07/09/2026). Um comando, resumível: `powershell -ExecutionPolicy Bypass -File Programacao\AgenteCore\experimentos\rodar_fase2b.ps1`. Ordem: checagens (Python, Ollama, RAM livre por modelo, disco, downloads dos 8 modelos, venv) → `maquina.json` → validação → Verificação 0 **nessa máquina** → Q8/fp16 do `1.5b` → **A0 linear nos seis modelos (linha de base refeita)** → A1/A2 nos seis → A3–A5 em `phi4-mini`, `qwen2.5-coder:3b` e `granite4.2:8b` → avaliação, gráficos e relatório, tudo em `experimentos/resultados_alvo/`. Estimativa: 30–45 h de CPU nessa máquina (é 1,5–2× mais lenta que o Ryzen; a Verificação 0 lá dá o número real de tokens/s). Os 48 casos da ablação Q8 iniciados no Ryzen ficam em `resultados/` como dado do Ryzen — a máquina-alvo refaz a ablação do zero. Ao terminar: relatório da 2-B em `3-resultados-e-analises/`, nos moldes do da 2-A, comparando também A0 Ryzen × A0 i5 (mesmos casos, máquinas diferentes).
- **Corrigir os fixtures que contradizem o código** (4.20: "R$ NaN" e cartões duplicados) — só depois da 2-B, para não quebrar a comparabilidade.
- **Modelo padrão em `install.py`** continua `qwen2.5-coder:3b` por compatibilidade; a 2-A já mostrou 27% contra 68% do Granite. Redecidir ao fim da 2-B com acerto × tempo × biblioteca.
- **Ablação base × instruct** (`qwen2.5:0.5b-base` × `0.5b-instruct`) como piso metodológico, se a banca pedir um "modelo sem instrução" no lugar do GPT-2.


