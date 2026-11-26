<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por impacto_git.py --conferir-historico a partir de git log e git diff --name-only do repositório e fase5_agente_b/cenarios.jsonl (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Seleção pelo Git conferida contra a rodada completa: a conta retrospectiva sobre o histórico (Pós-Fase 4, pacote Q7), gerada em 2026-11-25

Esta é uma conta retrospectiva: nenhuma das seleções abaixo rodou de verdade. Para cada par de commits consecutivos que mexeram nas cobaias, ela pergunta que cenários a seleção deixaria de fora e o que a rodada completa `fase5_agente_b` mostra deles. Nessa rodada, 49 das 50 execuções tiveram Task Success; os cenários com alguma execução sem sucesso foram: `contrato-malformed_json`. Dos 8 pares, 3 rodam tudo pela regra 1, 6 não deixam de fora nenhum cenário com falha e 2 deixariam de fora um cenário que falhou na rodada completa. É para esses que existe a regra 2: a rodada completa volta em prazo fixo, e a seleção só vale entre duas delas.

<!-- tabela:tb_f4_conferencia_pares -->
| Commit testado | Commit atual | Data | Veredito da seleção | Cenários selecionados | Deixados de fora | Falhas perdidas | Segura |
|---|---|---|---|---|---|---|---|
| `e854a0eb` | `ab4da6a1` | 2026-08-31 | roda tudo | 10 | 0 | nenhuma | sim |
| `ab4da6a1` | `26432d2c` | 2026-08-31 | nada a rodar | 0 | 10 | contrato-malformed_json | não |
| `26432d2c` | `084fce09` | 2026-09-01 | roda tudo | 10 | 0 | nenhuma | sim |
| `084fce09` | `603c423e` | 2026-09-03 | seleção parcial | 6 | 4 | nenhuma | sim |
| `603c423e` | `3e8cfc14` | 2026-10-23 | nada a rodar | 0 | 10 | contrato-malformed_json | não |
| `3e8cfc14` | `4f3b3e26` | 2026-10-27 | seleção parcial | 6 | 4 | nenhuma | sim |
| `4f3b3e26` | `633ebb27` | 2026-11-03 | seleção parcial | 10 | 0 | nenhuma | sim |
| `633ebb27` | `717f68c2` | 2026-11-12 | roda tudo | 10 | 0 | nenhuma | sim |
<!-- /tabela:tb_f4_conferencia_pares -->

Regra aplicada: cada seleção registra os cenários que deixou de rodar, e a rodada completa seguinte confere se algum deles falhou (Azure DevOps TIA: comparar T1, os selecionados, com T2, todos).

Fontes: Rothermel e Harrold (1997): seleção segura inclui todo teste capaz de expor falha no programa modificado; Gligoric, Eloussi e Marinov (2015), Ekstazi: dependência em nível de arquivo cortou o tempo de teste em 32% a 54%; Memon et al. (2017), Google TAP: os alvos que dependem dos arquivos modificados são a base da seleção; Azure DevOps, Test Impact Analysis: mapa à mão e aproximado (TIA.UserMapFile), arquivo desconhecido roda tudo, rodada completa periódica, T1 contra T2.
