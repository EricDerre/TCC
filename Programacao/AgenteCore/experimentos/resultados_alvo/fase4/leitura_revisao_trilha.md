<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase4.py a partir de revisao_trilha.md preenchida e trilha.json (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Sessão de revisão dos relatórios da trilha (corrida 22), gerada em 2026-11-05

Especificação da trilha, seção 12 c: com um revisor humano, o acerto da localização do erro, o tempo até a decisão e a adesão apropriada (aceitar o diagnóstico quando está certo e recusar quando está errado), com a utilidade percebida como medida secundária. A conta foi escrita e testada antes de abrir o gabarito, e a planilha foi preenchida sem ver o resultado de cada caso.

Um revisor só, o autor do trabalho, que conhece o banco de casos. A amostra traz 5 dos 5 erros da corrida e 6 dos 31 acertos, e o revisor sabia disso, então a proporção de errados nela não é a da corrida. Erro localizado é o que o revisor declarou: num diagnóstico errado, achar um erro é ter encontrado o erro do agente no relatório; num diagnóstico certo, é ter apontado um erro onde não há. O tempo conta só com o relatório à vista.

Só 1 dos 11 relatórios tem resposta própria do revisor, dada antes de ele ler a pré-análise do Claude. Os outros 10 são o parecer do Claude, aprovado pelo Eric sem resposta própria (decisões 85 e 86), e ficam sem tempo medido. Por isso esta leitura não cumpre a medida com revisor humano da especificação: na maior parte, a adesão, a localização e a utilidade abaixo são do Claude. A medida fica em aberto e será feita depois da Pós-Fase 4 (decisão 95).

O parecer do Claude, nos 11 relatórios, foi escrito sem abrir o gabarito, mas por quem sabia quantos erros a amostra tem e já tinha visto os nomes dos casos; os limites estão em `pre_analise_revisao_trilha.md`.

Em `run-4`, o revisor marcou que achou o erro num diagnóstico que avaliou como certo. Ele pode ter lido "erro" como o defeito do sistema, e não como o erro do agente; a conta de localização trata isso como apontar um erro onde não há, e a resposta fica como ele deu.

Somando a resposta do revisor e o parecer aprovado, a planilha avalia 11 de 11 diagnósticos como o gabarito (100,0%, Wilson 95% 74,1 a 100,0). Decisão e avaliação discordam em 0 relatório(s).


<!-- tabela:tb_f4_revisao_resumo -->
| Relatórios | Com resposta do revisor | Com parecer aprovado | Diagnósticos certos | Diagnósticos errados | Adesão apropriada | Adesão (%) | Wilson 95% | Tempo mediano (s) | Erros achados | Utilidade mediana |
|---|---|---|---|---|---|---|---|---|---|---|
| 11 | 1 | 10 | 6 | 5 | 11 | 100,0 | 74,1 a 100,0 | 307 | 4 de 5 | 4 |
<!-- /tabela:tb_f4_revisao_resumo -->

<!-- tabela:tb_f4_revisao_origem -->
| Quem decidiu | Relatórios | Decisões apropriadas | Apropriadas (%) | Wilson 95% | Avaliação igual ao gabarito |
|---|---|---|---|---|---|
| resposta do revisor | 1 | 1 | 100,0 | 20,7 a 100,0 | 1 |
| parecer do Claude aprovado | 10 | 10 | 100,0 | 72,2 a 100,0 | 10 |
<!-- /tabela:tb_f4_revisao_origem -->

<!-- tabela:tb_f4_revisao_parecer -->
| Relatórios | Decisões apropriadas | Apropriadas (%) | Wilson 95% | Causa certa | Causa certa (%) | Avaliação igual ao gabarito | Errou a decisão | Errou a causa |
|---|---|---|---|---|---|---|---|---|
| 11 | 11 | 100,0 | 74,1 a 100,0 | 11 | 100,0 | 11 | nenhum | nenhum |
<!-- /tabela:tb_f4_revisao_parecer -->

<!-- tabela:tb_f4_revisao_adesao -->
| Grupo | Relatórios | Aceitou | Recusou | Apropriadas | Apropriadas (%) | Wilson 95% |
|---|---|---|---|---|---|---|
| diagnóstico certo | 6 | 6 | 0 | 6 | 100,0 | 61,0 a 100,0 |
| diagnóstico errado | 5 | 0 | 5 | 5 | 100,0 | 56,6 a 100,0 |
| todos | 11 | 6 | 5 | 11 | 100,0 | 74,1 a 100,0 |
<!-- /tabela:tb_f4_revisao_adesao -->

<!-- tabela:tb_f4_revisao_localizacao -->
| Grupo | Relatórios | Achou um erro | Não achou | Não viu erro | Achou (%) | Wilson 95% |
|---|---|---|---|---|---|---|
| diagnóstico errado | 5 | 4 | 1 | 0 | 80,0 | 37,6 a 96,4 |
| diagnóstico certo | 6 | 1 | 0 | 5 | 16,7 | 3,0 a 56,4 |
<!-- /tabela:tb_f4_revisao_localizacao -->

<!-- tabela:tb_f4_revisao_tempo -->
| Grupo | Relatórios | Mediana (s) | Mínimo (s) | Máximo (s) |
|---|---|---|---|---|
| todos | 1 | 307 | 307 | 307 |
| diagnóstico certo | 1 | 307 | 307 | 307 |
| diagnóstico errado | 0 | não medido | não medido | não medido |
| aceitos | 1 | 307 | 307 | 307 |
| recusados | 0 | não medido | não medido | não medido |
<!-- /tabela:tb_f4_revisao_tempo -->

<!-- tabela:tb_f4_revisao_utilidade -->
| Grupo | Relatórios | Mediana | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|---|
| todos | 11 | 4 | 0 | 1 | 4 | 4 | 2 |
| diagnóstico certo | 6 | 3,5 | 0 | 0 | 3 | 3 | 0 |
| diagnóstico errado | 5 | 4 | 0 | 1 | 1 | 1 | 2 |
<!-- /tabela:tb_f4_revisao_utilidade -->

<!-- tabela:tb_f4_revisao_avaliacao -->
| Diagnóstico | Revisor disse certo | Revisor disse errado |
|---|---|---|
| certo | 6 | 0 |
| errado | 0 | 5 |
<!-- /tabela:tb_f4_revisao_avaliacao -->

<!-- tabela:tb_f4_revisao_casos -->
| # | Caso | Gabarito | Rótulo | Resultado | Selo | Quem decidiu | Tempo (s) | Erro localizado | Decisão | Apropriada | Utilidade | Avaliação | Causa no parecer do Claude | Comentário |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `run-4` | `dado_desatualizado` | `dado_desatualizado` | certo | alto | resposta do revisor | 307 | sim | aceitar | sim | 4 | certo | `dado_desatualizado` |  |
| 2 | `run-1` | `erro_interno_do_servidor` | `erro_interno_do_servidor` | certo | medio | parecer do Claude aprovado | não medido | n.a. | aceitar | sim | 3 | certo | `erro_interno_do_servidor` | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 3 | `lex-10` | `resposta_truncada` | `resposta_truncada` | certo | alto | parecer do Claude aprovado | não medido | n.a. | aceitar | sim | 4 | certo | `resposta_truncada` | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 4 | `semt-9` | `valor_fora_do_dominio` | `tipo_divergente` | errado | alto | parecer do Claude aprovado | não medido | não | recusar | sim | 2 | errado | `valor_fora_do_dominio` | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 5 | `tra-15` | `escala_ou_unidade_errada` | `registro_duplicado` | errado | baixo | parecer do Claude aprovado | não medido | sim | recusar | sim | 4 | errado | `escala_ou_unidade_errada` | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 6 | `sin-11` | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | certo | alto | parecer do Claude aprovado | não medido | n.a. | aceitar | sim | 3 | certo | `estrutura_aninhada_divergente` | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 7 | `lex-8` | `codificacao_incorreta` | `codificacao_incorreta` | certo | baixo | parecer do Claude aprovado | não medido | n.a. | aceitar | sim | 3 | certo | `codificacao_incorreta` | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 8 | `efe-1` | `localizador_quebrado` | `tempo_de_resposta_excedido` | errado | medio | parecer do Claude aprovado | não medido | sim | recusar | sim | 5 | errado | `localizador_quebrado` | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 9 | `semt-5` | `nulo_inesperado` | `nulo_inesperado` | certo | alto | parecer do Claude aprovado | não medido | n.a. | aceitar | sim | 4 | certo | `nulo_inesperado` | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 10 | `sin-5` | `campo_ausente` | `colecao_no_lugar_de_objeto` | errado | baixo | parecer do Claude aprovado | não medido | sim | recusar | sim | 3 | errado | `campo_ausente` | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 11 | `sin-14` | `campo_renomeado` | `colecao_no_lugar_de_objeto` | errado | baixo | parecer do Claude aprovado | não medido | sim | recusar | sim | 5 | errado | `campo_renomeado` | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
<!-- /tabela:tb_f4_revisao_casos -->
