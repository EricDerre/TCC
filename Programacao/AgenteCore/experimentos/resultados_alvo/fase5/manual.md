<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase5.py a partir de a planilha da linha de base manual e o registro da sessão (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Fase 5 do Memorial cola estes blocos, e as contas são as das regras L1 a L15 do plano aprovado, fixadas antes das medidas. -->
# A linha de base manual na Fase 5: tempo e Task Success dos integrantes, gerada em 2026-11-24

Três integrantes, cada um nos dez cenários, na ordem sorteada. O tempo de cada tentativa é o fim menos o início menos o desconto da restauração do banco; no contrato o cronômetro para na entrega da causa e do campo, certa ou errada, e no localizador, no conferir que passou. A unidade é o cenário (regra L2): por cenário, a média de quem chegou ao fim do cronômetro, com o mínimo e o máximo; no geral e por tipo, a média das médias dos cenários. O intervalo do tempo é a reamostragem dos cenários dentro de cada tipo (2000 reamostras, semente 20261104); o do Task Success é o de Wilson. Quem não chegou ao fim do cronômetro fica fora da média do tempo e dentro do Task Success; a segunda conta põe 600 s no lugar e vale como piso. A linha anulada na hora por falha do protocolo é contada à parte e não entra em conta nenhuma. O tempo pela posição na ordem e por integrante é só descrição: mostra o aprendizado ao longo da sessão.


<!-- tabela:tb_f5_manual_resumo -->
| Tentativas | Task Success | Task Success (%) | Wilson 95% (%) | Cenários com todas certas | Com fim de cronômetro | Sem fim | Tempo médio (s) | Reamostragem 95% (s) | Segunda conta, com 600 s para quem não chegou ao fim (s) | Reamostragem 95% da segunda conta (s) | Só com Task Success (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 30 | 14 | 46,7 | 30,2 a 63,9 | 0 de 10 | 24 | 6 | 219,7 | 172,3 a 264,7 | 289,8 | 241,0 a 339,6 | 246,0 |
<!-- /tabela:tb_f5_manual_resumo -->

<!-- tabela:tb_f5_manual_por_tipo -->
| Tipo | Tentativas | Task Success | Task Success (%) | Wilson 95% (%) | Cenários com todas certas | Com fim de cronômetro | Sem fim | Tempo médio (s) | Reamostragem 95% (s) | Segunda conta, com 600 s para quem não chegou ao fim (s) | Reamostragem 95% da segunda conta (s) | Só com Task Success (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| contrato | 18 | 6 | 33,3 | 16,3 a 56,3 | 0 de 6 | 16 | 2 | 174,8 | 125,7 a 228,6 | 222,2 | 153,4 a 291,0 | 213,2 |
| localizador | 12 | 8 | 66,7 | 39,1 a 86,2 | 0 de 4 | 8 | 4 | 287,0 | 183,0 a 359,3 | 391,4 | 322,0 a 439,6 | 287,0 |
<!-- /tabela:tb_f5_manual_por_tipo -->

<!-- tabela:tb_f5_manual_por_cenario -->
| Cenário | Tipo | Tentativas | Corrigidas | Com fim | Tempo médio (s) | Mínimo (s) | Máximo (s) | Segunda conta (s) | Só as corrigidas (s) |
|---|---|---|---|---|---|---|---|---|---|
| `contrato-malformed_json` | contrato | 3 | 1 | 3 | 109,6 | 50,2 | 151,5 | 109,6 | 127,2 |
| `contrato-field_missing` | contrato | 3 | 1 | 2 | 111,3 | 95,0 | 127,7 | 274,2 | 95,0 |
| `contrato-field_renamed` | contrato | 3 | 2 | 2 | 236,5 | 211,5 | 261,5 | 357,7 | 236,5 |
| `contrato-type_drift` | contrato | 3 | 0 | 3 | 189,0 | 51,4 | 260,6 | 189,0 | n/d |
| `contrato-escala_ou_unidade_errada` | contrato | 3 | 1 | 3 | 280,6 | 35,2 | 454,5 | 280,6 | 454,5 |
| `contrato-error_500` | contrato | 3 | 1 | 3 | 121,8 | 37,8 | 174,9 | 121,8 | 152,6 |
| `localizador-front-busca` | localizador | 3 | 2 | 2 | 385,3 | 289,5 | 481,0 | 456,8 | 385,3 |
| `localizador-front-admin-login` | localizador | 3 | 2 | 2 | 150,1 | 144,6 | 155,7 | 300,1 | 150,1 |
| `localizador-front-admin-produtos` | localizador | 3 | 2 | 2 | 331,2 | 258,7 | 403,7 | 420,8 | 331,2 |
| `localizador-front-cliente-reserva` | localizador | 3 | 2 | 2 | 281,6 | 167,7 | 395,4 | 387,7 | 281,6 |
<!-- /tabela:tb_f5_manual_por_cenario -->

<!-- tabela:tb_f5_manual_por_posicao -->
| Posição na ordem do integrante | Tentativas | Corrigidas | Com fim | Tempo médio (s) |
|---|---|---|---|---|
| 1 | 3 | 2 | 3 | 250,3 |
| 2 | 3 | 0 | 3 | 152,6 |
| 3 | 3 | 1 | 2 | 163,8 |
| 4 | 3 | 2 | 2 | 275,5 |
| 5 | 3 | 2 | 3 | 91,6 |
| 6 | 3 | 1 | 2 | 239,7 |
| 7 | 3 | 1 | 2 | 332,1 |
| 8 | 3 | 1 | 2 | 141,7 |
| 9 | 3 | 2 | 2 | 324,4 |
| 10 | 3 | 2 | 3 | 219,0 |
<!-- /tabela:tb_f5_manual_por_posicao -->

<!-- tabela:tb_f5_manual_por_integrante -->
| Integrante | Tentativas | Corrigidas | Com fim | Tempo médio (s) | Tempo somado (s) |
|---|---|---|---|---|---|
| 1 | 10 | 5 | 10 | 213,9 | 2138,9 |
| 2 | 10 | 0 | 4 | 43,6 | 174,5 |
| 3 | 10 | 9 | 10 | 278,2 | 2781,7 |
<!-- /tabela:tb_f5_manual_por_integrante -->

<!-- tabela:tb_f5_manual_linhas -->
| Linhas esperadas | Preenchidas | Anuladas na hora (fora de toda conta) | Anotadas à mão | Sem fim de cronômetro (estourou o limite ou não entregou) |
|---|---|---|---|---|
| 30 | 30 | nenhuma | nenhuma | linha 14 (integrante 2, ordem 3, `localizador-front-busca`); linha 15 (integrante 2, ordem 4, `localizador-front-admin-login`); linha 17 (integrante 2, ordem 6, `localizador-front-cliente-reserva`); linha 18 (integrante 2, ordem 7, `localizador-front-admin-produtos`); linha 19 (integrante 2, ordem 8, `contrato-field_renamed`); linha 20 (integrante 2, ordem 9, `contrato-field_missing`) |
<!-- /tabela:tb_f5_manual_linhas -->
