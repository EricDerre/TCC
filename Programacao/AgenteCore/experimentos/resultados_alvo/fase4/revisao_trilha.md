<!-- ! Alteração de IA - Revisar: planilha DERIVADA da sessão de revisão dos relatórios da trilha (Fase 4, P7), gerada por avaliar_fase4.py --trilha a partir de trilha.json; só as células do revisor são preenchidas à mão, e o harness não a regrava depois de preenchida.
     ! Motivo: a especificação da trilha (seção 12 c) mede, com um revisor humano, o acerto da localização do erro, o tempo até a decisão e a adesão apropriada (aceitar o diagnóstico certo e recusar o errado), com a utilidade percebida como medida secundária; sem a planilha a sessão não teria registro conferível. -->
# Sessão de revisão dos relatórios da trilha (corrida fase4_trilha)

Como preencher, um relatório por vez, na ordem da tabela: abra só o relatório indicado (o caminho é relativo a esta pasta; os de `fase4_trilha/relatorios/` não servem, porque saíram sem o caso), cronometre do início da leitura até decidir se aceita ou recusa o diagnóstico e anote os segundos em "Tempo até a decisão"; diga se achou no relatório onde está o erro (sim, não ou n.a. quando não vê erro); a decisão (aceitar ou recusar); a utilidade do relatório de 1 (nenhuma) a 5 (decidiu sozinho); e a sua avaliação do diagnóstico (certo ou errado). Não consulte `trilha.md` nem `trilha.json` antes de preencher: eles dizem o resultado de cada caso, e a adesão apropriada só vale às cegas.

| # | Caso | Classe | Relatório | Tempo até a decisão (s) | Erro localizado (sim, não, n.a.) | Decisão (aceitar, recusar) | Utilidade (1 a 5) | Avaliação (certo, errado) | Comentário |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `run-4` | 5 | `relatorios_revisao_trilha/run-4@base.md` | 307 | sim | aceitar | 4 | certo |  |
| 2 | `run-1` | 5 | `relatorios_revisao_trilha/run-1@base.md` | não medido | n.a. | aceitar | 3 | certo | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 3 | `lex-10` | 1 | `relatorios_revisao_trilha/lex-10@base.md` | não medido | n.a. | aceitar | 4 | certo | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 4 | `semt-9` | 3 | `relatorios_revisao_trilha/semt-9@base.md` | não medido | não | recusar | 2 | errado | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 5 | `tra-15` | 4 | `relatorios_revisao_trilha/tra-15@base.md` | não medido | sim | recusar | 4 | errado | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 6 | `sin-11` | 2 | `relatorios_revisao_trilha/sin-11@base.md` | não medido | n.a. | aceitar | 3 | certo | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 7 | `lex-8` | 1 | `relatorios_revisao_trilha/lex-8@base.md` | não medido | n.a. | aceitar | 3 | certo | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 8 | `efe-1` | 6 | `relatorios_revisao_trilha/efe-1@base.md` | não medido | sim | recusar | 5 | errado | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 9 | `semt-5` | 3 | `relatorios_revisao_trilha/semt-5@base.md` | não medido | n.a. | aceitar | 4 | certo | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 10 | `sin-5` | 2 | `relatorios_revisao_trilha/sin-5@base.md` | não medido | sim | recusar | 3 | errado | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
| 11 | `sin-14` | 2 | `relatorios_revisao_trilha/sin-14@base.md` | não medido | sim | recusar | 5 | errado | Parecer do Claude, aprovado pelo Eric sem resposta própria (decisão 86). |
