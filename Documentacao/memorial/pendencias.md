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
- **Fase 2-B concluída na máquina-alvo** (07–09/09/2026; relatório em `3-resultados-e-analises/fase-2b-relatorio-por-modelo.md`). Decisões que ela deixou para o Eric:
  - **Modelo padrão de produção** entre `qwen2.5-coder:3b` + A2 (63%, 30 s, 2,3 GB, licença de pesquisa), `qwen2.5:7b` + A2 (70%, 61 s, 5,2 GB, Apache 2.0) e `granite4.2:8b` + A2 (77%, 124 s, 6,6 GB, Apache 2.0). O `install.py` ainda aponta para o 3b.
  - **Modo de operação do agente = biblioteca recuperada (A2)**; biblioteca inteira no prompt descartada.
  - **Melhorar o recuperador antes de trocar de modelo**: hit@3 de 79% limita o Granite a 77% (com o verbete certo, 100%). Experimentos baratos e offline: k = 5 (hit@5 já é 90%), sinais em código para a classe de tradução (verbete certo no top-3 em só 47%), embedding denso `embeddinggemma:300m` via `validar_banco.py --embedding`.
  - **Validação por código como porta obrigatória da biblioteca** na Fase 3 (achado 4.24: verbete errado é seguido em 93–96% dos casos).
- **O `fase2b.log` da máquina-alvo não foi versionado** (`*.log` no `.gitignore`); ele contém a Verificação 0 do i5. Versionar com `git add -f` ou tirar `*.log` da regra para `experimentos/resultados_alvo/`.
- **Corrigir os fixtures que contradizem o código** (4.20: "R$ NaN" e cartões duplicados) — pode ser feito agora; a comparabilidade caso a caso com a 2-A não precisa mais ser preservada.
- **Ablação base × instruct** (`qwen2.5:0.5b-base` × `0.5b-instruct`) como piso metodológico, se a banca pedir um "modelo sem instrução" no lugar do GPT-2.


