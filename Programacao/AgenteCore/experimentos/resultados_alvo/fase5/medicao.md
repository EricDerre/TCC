<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase5.py a partir de os registros da corrida do agente, a planilha da linha de base manual e o registro da sessão (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Fase 5 do Memorial cola estes blocos, e as contas são as das regras L1 a L15 do plano aprovado, fixadas antes das medidas. -->
# A medição de valor da Fase 5: o agente contra a linha de base manual, gerada em 2026-11-24

O agente repara mais rápido que uma pessoa, e resolve tantos cenários quanto ela? As regras desta leitura foram fixadas no plano da fase antes de qualquer medida (regras L1 a L15). A unidade é o cenário (regra L2): por cenário, a média de quem chegou ao fim do cronômetro, com o mínimo e o máximo; no geral e por tipo, a média das médias dos cenários. O intervalo do tempo é a reamostragem dos cenários dentro de cada tipo (2000 reamostras, semente 20261104); o do Task Success é o de Wilson. Quem não chegou ao fim do cronômetro fica fora da média do tempo e dentro do Task Success; a segunda conta põe 600 s no lugar e vale como piso. A diferença de cada cenário é o tempo médio das pessoas menos o MTTR médio do agente: positiva quando o agente foi mais rápido. Diferença menor que 5 s conta como empate e sai do teste dos sinais; cenário em que só um lado chegou ao fim conta para esse lado no teste e fica fora da média das diferenças.

**Tempo de reparo.** O agente reparou mais rápido que as pessoas: a diferença média por cenário (tempo das pessoas menos MTTR do agente) foi de 153,4 s, com intervalo de 95% de 109,0 a 196,1 s, que não contém zero, e o teste dos sinais deu p = 0,0020 (10 cenários com o agente mais rápido, nenhum cenário com as pessoas mais rápidas e nenhum empate).

**Task Success.** O agente resolveu mais cenários que as pessoas: 10 cenários com a parcela do agente maior, nenhum cenário com a das pessoas maior e nenhum cenário igual; o teste dos sinais deu p = 0,0020.

Por tipo de cenário a leitura mostra os números e fica sem veredito (regra L10): com 6 cenários de contrato o menor p que o teste dos sinais alcança é 0,0312, com os 6 na mesma direção e com 4 cenários de localizador o menor p que o teste dos sinais alcança é 0,1250, com os 4 na mesma direção; o veredito pede p abaixo de 0,05.

Conta exploratória, acrescentada em 24/11/2026, depois de ver os números (ficha 91, decisão 151): a mesma comparação refeita sem a sessão de um integrante por vez, com as regras L2 a L11 aplicadas às medidas que sobram. Ela não é o veredito da leitura, que continua sendo o das três sessões, pelas regras fixadas antes das medidas; mostra de que sessão cada veredito depende. O p do Task Success aparece mesmo quando sobram menos cenários diferentes do que a regra L11 pede para o teste valer, e a coluna ao lado diz o que a regra daria.


<!-- tabela:tb_f5_medicao_resumo -->
| MTTR médio do agente (s) | Reamostragem 95% (s) | Tempo médio das pessoas (s) | Reamostragem 95% (s) | Diferença média por cenário, pessoas menos agente (s) | Reamostragem 95% da diferença (s) | Razão entre as médias | Cenários com os dois lados | Agente mais rápido | Pessoas mais rápidas | Empates | p do teste dos sinais | Leitura pela regra L9 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 66,3 | 60,9 a 71,5 | 219,7 | 172,3 a 264,7 | 153,4 | 109,0 a 196,1 | 3,31 | 10 | 10 | 0 | 0 | 0,0020 | O agente reparou mais rápido que as pessoas: a diferença média por cenário (tempo das pessoas menos MTTR do agente) foi de 153,4 s, com intervalo de 95% de 109,0 a 196,1 s, que não contém zero, e o teste dos sinais deu p = 0,0020 (10 cenários com o agente mais rápido, nenhum cenário com as pessoas mais rápidas e nenhum empate). |
<!-- /tabela:tb_f5_medicao_resumo -->

<!-- tabela:tb_f5_medicao_tempo_por_cenario -->
| Cenário | Tipo | MTTR médio do agente (s) | Faixa do agente (s) | Tempo médio das pessoas (s) | Faixa das pessoas (s) | Diferença, pessoas menos agente (s) | Razão | Quem foi mais rápido | As faixas se cruzam |
|---|---|---|---|---|---|---|---|---|---|
| `contrato-malformed_json` | contrato | 81,7 | 78,7 a 85,9 | 109,6 | 50,2 a 151,5 | 27,9 | 1,34 | agente | sim |
| `contrato-field_missing` | contrato | 67,0 | 66,4 a 67,8 | 111,3 | 95,0 a 127,7 | 44,4 | 1,66 | agente | não |
| `contrato-field_renamed` | contrato | 65,3 | 64,9 a 65,9 | 236,5 | 211,5 a 261,5 | 171,2 | 3,62 | agente | não |
| `contrato-type_drift` | contrato | 66,7 | 66,0 a 67,6 | 189,0 | 51,4 a 260,6 | 122,3 | 2,83 | agente | sim |
| `contrato-escala_ou_unidade_errada` | contrato | 80,4 | 78,8 a 82,9 | 280,6 | 35,2 a 454,5 | 200,2 | 3,49 | agente | sim |
| `contrato-error_500` | contrato | 76,6 | 75,0 a 77,3 | 121,8 | 37,8 a 174,9 | 45,2 | 1,59 | agente | sim |
| `localizador-front-busca` | localizador | 65,4 | 64,9 a 65,8 | 385,3 | 289,5 a 481,0 | 319,8 | 5,89 | agente | não |
| `localizador-front-admin-login` | localizador | 39,0 | 38,5 a 40,3 | 150,1 | 144,6 a 155,7 | 111,2 | 3,85 | agente | não |
| `localizador-front-admin-produtos` | localizador | 60,3 | 60,1 a 60,6 | 331,2 | 258,7 a 403,7 | 270,9 | 5,49 | agente | não |
| `localizador-front-cliente-reserva` | localizador | 61,0 | 60,0 a 63,1 | 281,6 | 167,7 a 395,4 | 220,6 | 4,62 | agente | não |
<!-- /tabela:tb_f5_medicao_tempo_por_cenario -->

<!-- tabela:tb_f5_medicao_tempo_por_tipo -->
| Tipo | Cenários com os dois lados | Diferença média, pessoas menos agente (s) | Reamostragem 95% (s) | Razão entre as médias | Agente mais rápido | Pessoas mais rápidas | Empates | Sem medida |
|---|---|---|---|---|---|---|---|---|
| contrato | 6 | 101,9 | 52,0 a 156,4 | 2,40 | 6 | 0 | 0 | 0 |
| localizador | 4 | 230,6 | 138,5 a 295,4 | 5,09 | 4 | 0 | 0 | 0 |
<!-- /tabela:tb_f5_medicao_tempo_por_tipo -->

<!-- tabela:tb_f5_medicao_piso -->
| Segunda conta: quem não chegou ao fim entra com 600 s | Cenários com os dois lados | Diferença média, pessoas menos agente (s) | Reamostragem 95% (s) | Razão entre as médias | Agente mais rápido | Pessoas mais rápidas | Empates | p do teste dos sinais | O que a regra L9 daria nesta conta |
|---|---|---|---|---|---|---|---|---|---|
| piso, não é o veredito da leitura | 10 | 213,1 | 149,2 a 272,8 | 3,78 | 9 | 1 | 0 | 0,0215 | veredito (agente) |
<!-- /tabela:tb_f5_medicao_piso -->

<!-- tabela:tb_f5_medicao_task_success -->
| Lado | Medidas | Task Success | Task Success (%) | Wilson 95% (%) | Cenários com todas certas |
|---|---|---|---|---|---|
| agente | 50 | 49 | 98,0 | 89,5 a 99,6 | 9 de 10 |
| pessoas | 30 | 14 | 46,7 | 30,2 a 63,9 | 0 de 10 |
<!-- /tabela:tb_f5_medicao_task_success -->

<!-- tabela:tb_f5_medicao_task_success_por_cenario -->
| Cenário | Tipo | Agente | Agente (%) | Pessoas | Pessoas (%) | Diferença (pontos) | Parcela maior |
|---|---|---|---|---|---|---|---|
| `contrato-malformed_json` | contrato | 4 de 5 | 80,0 | 1 de 3 | 33,3 | 46,7 | agente |
| `contrato-field_missing` | contrato | 5 de 5 | 100,0 | 1 de 3 | 33,3 | 66,7 | agente |
| `contrato-field_renamed` | contrato | 5 de 5 | 100,0 | 2 de 3 | 66,7 | 33,3 | agente |
| `contrato-type_drift` | contrato | 5 de 5 | 100,0 | 0 de 3 | 0,0 | 100,0 | agente |
| `contrato-escala_ou_unidade_errada` | contrato | 5 de 5 | 100,0 | 1 de 3 | 33,3 | 66,7 | agente |
| `contrato-error_500` | contrato | 5 de 5 | 100,0 | 1 de 3 | 33,3 | 66,7 | agente |
| `localizador-front-busca` | localizador | 5 de 5 | 100,0 | 2 de 3 | 66,7 | 33,3 | agente |
| `localizador-front-admin-login` | localizador | 5 de 5 | 100,0 | 2 de 3 | 66,7 | 33,3 | agente |
| `localizador-front-admin-produtos` | localizador | 5 de 5 | 100,0 | 2 de 3 | 66,7 | 33,3 | agente |
| `localizador-front-cliente-reserva` | localizador | 5 de 5 | 100,0 | 2 de 3 | 66,7 | 33,3 | agente |
<!-- /tabela:tb_f5_medicao_task_success_por_cenario -->

<!-- tabela:tb_f5_medicao_descricao -->
| Só descrição (regra L13) | Agente | Pessoas | Diferença, pessoas menos agente (s) |
|---|---|---|---|
| tempo médio só com as medidas que tiveram Task Success (s) | 66,3 em 10 cenários | 246,0 em 9 cenários | 179,7 |
| tempo total médio da execução do agente, com a detecção (s) | 69,0 | não se aplica | não se aplica |
<!-- /tabela:tb_f5_medicao_descricao -->

<!-- tabela:tb_f5_medicao_sem_um_integrante -->
| Conta exploratória de 24/11/2026, feita depois de ver os números; não é o veredito da leitura | Tentativas das pessoas que sobram | Corrigidas | Tempo médio das pessoas (s) | Diferença média por cenário, pessoas menos agente (s) | Reamostragem 95% (s) | Cenários com o agente mais rápido | Com as pessoas mais rápidas | Empates | p do teste dos sinais no tempo | O que a regra L9 daria | Cenários com a parcela do agente maior | Com a das pessoas maior | Iguais | p do teste dos sinais no Task Success | O que a regra L11 daria |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sem a sessão do integrante 1 | 20 | 9 | 237,4 | 171,1 | 112,2 a 222,7 | 10 | 0 | 0 | 0,0020 | veredito: o agente mais rápido | 10 | 0 | 0 | 0,0020 | veredito: o agente resolveu mais |
| sem a sessão do integrante 2 | 20 | 14 | 246,0 | 179,7 | 127,3 a 235,6 | 10 | 0 | 0 | 0,0020 | veredito: o agente mais rápido | 5 | 0 | 5 | 0,0625 | sem veredito (menos de 6 cenários diferentes) |
| sem a sessão do integrante 3 | 20 | 5 | 175,7 | 109,3 | 78,6 a 139,2 | 10 | 0 | 0 | 0,0020 | veredito: o agente mais rápido | 10 | 0 | 0 | 0,0020 | veredito: o agente resolveu mais |
<!-- /tabela:tb_f5_medicao_sem_um_integrante -->
