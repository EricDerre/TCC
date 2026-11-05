<!-- ! Alteração de IA - Revisar: passagem de bastão de 05/11/2026 (pacote P8): a Fase 4 fechada, o que a sessão mudou, como conferir, as armadilhas e o que vem depois.
     ! Motivo: o P8 é o último pacote da fase; a sessão seguinte precisa saber o que já está fechado, que nada foi commitado, quais fichas ficaram abertas e que comando confere cada leitura com a corrida certa, sem reler o chat. Os resultados ficam no relatório da fase, de onde este arquivo aponta, para nenhum número ser digitado à mão aqui. -->
<!-- ! Alteração de IA - Revisar: (05/11/2026, depois do P8) título, seção 2 e próximos passos passaram a dizer as respostas do Eric às fichas 42 a 45 (decisões 90 a 93) e o que a medida sem modelo do prompt mostrou.
     ! Motivo: a passagem dizia que as fichas dependiam dele e que a Fase 5 vinha em seguida; três respostas pedem trabalho antes dela, e a sessão seguinte precisa do que já foi medido para não refazer. -->
# Fase 4: pacote P8 e as respostas às fichas 42 a 45 (05/11/2026)

Escrito para: o Claude que continuar depois da Fase 4. Continua [a passagem da Fase 4](2026-10-26-fase-4-plano-e-p0.md), onde estão as armadilhas dos pacotes P0 a P7. Ler antes: `.claude/CLAUDE.md`, `.claude/rules/` e o [relatório da fase](../../Documentacao/memorial/3-resultados-e-analises/fase-4-relatorio.md). O livro-razão é `.superpowers/sdd/fase-4/progress.md` (fora do git).

## 1. O que está feito

| Frente | Estado |
|---|---|
| **Pacotes e corridas** | P0 a P8 feitos; corridas 16 a 22 rodadas e lidas. As leituras vigentes são a 18b (decisão 82) e a 21b (roadmap §2.14) |
| **Relatório da fase** | `Documentacao/memorial/3-resultados-e-analises/fase-4-relatorio.md`: o texto foi montado por script a partir dos JSON de `resultados_alvo/fase4/`, com todos os blocos `tb_f4_*` colados por `avaliar_fase4.py --colar`. A seção 10 traz as regras uma a uma, a 12 as limitações e a 15 o que o documento do TCC precisa carregar |
| **Limitações declaradas** | A regra R1, que rodou mais larga que o texto do plano (relatório, seção 3); a regra R2 (decisão 82); a medida com revisor humano, que passou a em aberto (decisão 95, para depois da Pós-Fase 4); as duas contas do carimbo de conflito (decisão 88); a poda consertada depois das corridas, sem corrida nova (decisão 89) |
| **Código do P8** | `avaliar_fase4.py`: `LEITURA_NO_RELATORIO` e `fechar_no_relatorio` (de qual leitura são os blocos do relatório) e `_tres` (p, kappa e MTTR da cura em três casas). `pre_fase4.fechar`: parâmetro `blocos_de`. `painel_topicos.py`: aba "Fechamento da fase" (`secao_fechamento_f4`), lida do relatório. Testes novos em `testar_fase4.py` e `testar_painel_topicos.py`, escritos antes do código |
| **Derivados regravados** | `resultados_alvo/fase4/*.md` ganharam as três casas só no corpo (cabeçalho e JSON intactos), e `calibracao.json` ganhou o campo `ponte.completa`, que faltava desde a regravação de `pontes.json`. `limiares.json` não foi tocado: é o arquivo que a corrida 16 gravou. Nenhuma pasta de corrida foi regravada |
| **Documentos** | Achados 4.54 a 4.62; fichas 42 a 45; roadmap §1, §2.15, §4.7, §5, §6 e §7; README; índice do Memorial; anexo de desvios em `claude-memoria/plano-aprovado-fase-4.md`; um revisor por documento, com as correções em `Documentacao/memorial/5-metodo-e-ferramental/dados/revisao-fase-4-2026-11-05.json` |
| **Painel** | Regerado, testado e republicado no mesmo endereço, https://claude.ai/artifact/LhXeAccx5NMk1HprycHApN. O `painel_fase4.py` do plano não foi criado, porque as abas ficam em `painel_topicos.py` |
| **Git** | Nada commitado. O working tree de 05/11 traz também o que as sessões da corrida 22 e da revisão deixaram. O Eric commita |

## 2. O que o Eric decidiu depois do fechamento

As fichas 42 a 45 de [pendencias.md](../../Documentacao/memorial/pendencias.md) foram abertas no fechamento, ao conferir o plano contra o que rodou, e ele respondeu as quatro no mesmo dia, uma a uma no quadro da sessão (decisões 90 a 93). Três pedem trabalho antes da Fase 5, e as corridas só disparam com o sim dele:

- **42, opção (b), contra a recomendação:** o prompt na tela passou do limite que o plano fixou, e a poda não apertou. O caso ao vivo encurta, sem tocar no prompt fixo, e as corridas 18c e 21c repetem a 18b e a 21b em pasta nova.
- **43, opção (a), contra a recomendação:** o experimento em texto da ficha 34 não rodou. Ele é escrito em código novo e roda como corrida 23, uma condição por item, cerca de 3 h; o prompt do agente continua congelado.
- **44, opção (a):** os 36 inéditos da ficha 27 não têm conferência registrada, e nenhuma corrida com modelo os leu. O Eric confere primeiro, e depois a corrida 24 os lê em texto com a biblioteca de produção.
- **45, opção (a):** o trace na falha, o "Cérebro ao vivo" e o explorador com a trilha v2 não foram feitos. Os três entram na interface para o analista, que o Eric especifica, para depois da Fase 5 (roadmap §7).

O que a medida sem modelo do prompt já mostrou (`medir_prompt_tela.py`, `resultados_alvo/fase4/prompt_tela_blocos.json`), para o corte da ficha 42:

- A árvore sozinha não basta, e os números estão na decisão 90. O corte precisa alcançar também a linha OBSERVAÇÃO ADICIONAL e as listas `faltam` e `sobram` do SINTOMA.
- O que sobra acima do limite depois disso são linhas que a referência podada não tem (o rodapé, quando a tela de erro muda a estrutura) e linhas repetidas (`button " ALTERAR"`, nas páginas do front sem referência guardada), além das frases "O campo X não veio na resposta", uma por campo, no erro 500.
- `recuperacao.py` monta a busca com o SINTOMA e a OBSERVAÇÃO, então os verbetes recuperados podem mudar: conferir sem modelo antes da corrida.
- A árvore podada inteira continua na trilha; só o prompt encurta. Os tokens vêm do Ollama nas corridas e são estimados antes delas pela razão de tokens por caractere.

## 3. Como conferir

Em `Programacao/AgenteCore/experimentos`, com `RESULTADOS_DIR=resultados_alvo` e `PYTHONIOENCODING=utf-8`, cada leitura com a corrida dela:

```bash
python avaliar_fase4.py --reproducao --saida fase4_reproducao --check
```

```bash
python avaliar_fase4.py --reproducao --saida fase4_reproducao_ineditos --nome reproducibilidade_ineditos --check
```

```bash
python avaliar_fase4.py --calibracao --saida fase4_calibracao --check
```

```bash
python avaliar_fase4.py --tela --saida fase4_tela --check
```

```bash
python avaliar_fase4.py --tela --saida fase4_tela_v2 --nome tela_v2 --check
```

```bash
python avaliar_fase4.py --cura --saida fase4_cura --check
```

```bash
python avaliar_fase4.py --biblioteca --saida fase4_biblioteca --check
```

```bash
python avaliar_fase4.py --cenarios --saida fase4_ensaio --check
```

```bash
python avaliar_fase4.py --cenarios --saida fase4_ensaio_v2 --nome cenarios_v2 --check
```

```bash
python avaliar_fase4.py --trilha --saida fase4_trilha --check
```

```bash
python avaliar_fase4.py --revisao --check
```

```bash
python avaliar_fase4.py --pontes --check
```

Na raiz: `python ferramentas/gerar_dashboard.py --check`, `python ferramentas/testar_painel_topicos.py`, `python ferramentas/testar_painel_textos.py`, `python ferramentas/testar_sessao_revisao.py` e `python ferramentas/conferir_docs.py`.

## 4. Armadilhas pagas nesta sessão

- **`selecionar_casos` recusa requisição anotada:** `_ROTA_CATALOGO` não aceita o texto entre parênteses de `run-10` e `semt-18`, que ficaram de fora da corrida 17 como "sem tela" embora a rota de catálogo tenha página. A corrida não foi repetida, e o código não mudou, porque consertar muda o que uma nova corrida 17 selecionaria; o defeito está declarado no relatório, seção 3, e no anexo do plano.
- **`--saida` tem padrão enganoso:** sem ela, toda leitura procura `fase4_reproducao`. E os blocos das leituras de nome padrão das corridas 18 e 21 não são os do relatório: `--colar` agora recusa `tela` e `cenarios`, e exige `--nome tela_v2` e `--nome cenarios_v2` com a corrida certa.
- **`--calibracao` sem `--check` regrava `limiares.json`** com um `gravado_em` novo. Para regravar só a leitura, chame `pre_fase4.fechar` ou grave `calibracao.{json,md}` por script, como esta sessão fez.
- **Uma regravação de `pontes.json` muda o `--check` da calibração:** a leitura copia a entrada da ponte, então um campo novo lá faz `calibracao.json` diferir.
- **O cabeçalho dos `.md` derivados da Fase 4 diz "o relatório da Pré-Fase 4 do Memorial cola estes blocos",** porque `pre_fase4.cabecalho` é comum às duas fases. É só comentário, fora do `--check`; vale trocar na próxima vez que `pre_fase4.py` mudar.
- **Heredoc longo no Bash do aplicativo quebra** ("unexpected EOF"), como a memória avisa: scripts grandes vão pela ferramenta de escrita, e os de montagem desta sessão ficaram no scratchpad dela.
- **Duas mudanças de texto com efeito em teste:** o grupo Fase 4 abre pela aba do fechamento, o que mudou o teste da ordem da navegação; e a tabela da seção 10 do relatório é lida pelo painel, então os nomes das colunas (`Regra`, `O que ela pede`, `Corrida`, `Resultado`, `Estado`) não podem mudar sem mudar `secao_fechamento_f4`.

## 5. Próximos passos

1. O Eric revisa e commita; depois, `python ferramentas/replicar_commits_orientador.py` lista o que falta copiar para o clone do orientador (decisão 84), e o push é dele. O Kanban ainda mostra os cartões #58 a #61 (pacotes P5 a P8) em A Fazer e no Backlog (`claude-memoria/contexto/2026-10-26-kanban-historico.md`, seção 7).
2. O trabalho das decisões 90 a 92. O código está pronto desde a noite de 05/11, com testes: o corte do caso ao vivo e a busca lendo o corpo inteiro (decisão 96), `corridas_em_texto.py` e a fila `rodar_pendencias_fase4.ps1`. O Eric aprovou a fila em 05/11 e a lança na janela dele, com o Claude e o VS Code fechados (18c, 21c e 23, cerca de 5 h); confira os logs em `resultados_alvo/<Saida>/fase4.log` quando ele voltar. Falta ele responder a ficha 46, a conferência dos 36 inéditos, que libera a corrida 24 (`rodar_fase4.ps1 -Modo ineditos -Saida fase4_ineditos`). Depois de rodar: refazer as leituras com o título certo (`--titulo`), passar `avaliar_fase4.LEITURA_NO_RELATORIO` às leituras novas, e atualizar o relatório da fase, a aba de fechamento, as abas "Tela e caso escrito" e "Cenários da Fase 5", uma aba nova para o experimento e a lista da seção 15. A Pós-Fase 4 (decisão 94) vem em seguida, e o Eric a especifica.
3. A sessão da linha de base manual, marcada com o grupo ([protocolo](../../Documentacao/memorial/5-metodo-e-ferramental/protocolo-linha-de-base-manual.md)), e a noite da Fase 5: `rodar_fase4.ps1 -Modo cenarios -Repeticoes 5`, com ponte se o Ollama mudar de versão (regra R6).
4. A próxima versão do documento do TCC, só se o Eric pedir: a lista está na seção 15 do relatório, e o gerador é `ferramentas/gerar_tcc_docx.py`.
5. A interface para o analista, que o Eric especifica, com o trace na falha, o "Cérebro ao vivo" e o explorador com a trilha v2, depois da Fase 5 (roadmap §7, decisão 93).
