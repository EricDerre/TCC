<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por analisar_fase3b.py a partir dos registros avaliados da Fase 3 e da Fase 3-B (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Fase 3-B do Memorial cola estes blocos. -->
# Análise de fechamento da Fase 3-B, gerada em 2026-10-01

Doador da troca cruzada: `qwen2.5:7b`. Leitores: `qwen2.5-coder:7b`, `qwen2.5-coder:3b`. Linha de base da cruzada: L0 da ponte `fase3b_ponte_0344` (Ollama 0.34.4). b conta os casos que só a primeira condição acertou; c, os que só a segunda acertou. Uma ponte é pareável com a Fase 3 quando b + c fica em até 2 (decisão 47).


<!-- tabela:tb_corridas -->
| Corrida (pasta em `resultados_alvo/`) | Modo | Modelos | Registros | Ollama nos registros | Erros | Bibliotecas lidas (hash) | Início | Fim |
|---|---|---|---|---|---|---|---|---|
| `fase3b_ponte` | ponte | qwen2.5-coder:3b, qwen2.5-coder:7b, qwen2.5:7b | 108 | 0.34.1 | 0 | L0=3196327e7fd5 | 21/09 14:24 | 21/09 18:35 |
| `fase3b_ponte_0344` | ponte | qwen2.5-coder:3b, qwen2.5-coder:7b, qwen2.5:7b | 108 | 0.34.4 | 0 | L0=3196327e7fd5 | 30/09 20:39 | 30/09 22:25 |
| `fase3b_ineditos` | ineditos | qwen2.5-coder:3b, qwen2.5:7b | 216 | 0.34.1 | 0 | L0=3196327e7fd5; L1=3394d203cab9; L1=53ccf19abeac; L3=71258b553152; L3=d9a86e383103 | 28/09 20:13 | 28/09 23:15 |
| `fase3b_cruzada_qwen` | cruzada | qwen2.5-coder:3b, qwen2.5-coder:7b | 144 | 0.34.4 | 0 | L1=3394d203cab9; L3=71258b553152 | 30/09 23:58 | 01/10 02:09 |
<!-- /tabela:tb_corridas -->

<!-- tabela:tb_pontes -->
| Ponte (Ollama) | Modelo | Acerto em L0 nos 36 (IC 95%) | Acurácia balanceada | b | c | p (McNemar) | Passaram a certos | Passaram a errados | Pareável (b + c até 2) | b / c sem o caso de texto corrigido | Caso de texto corrigido entre as corridas |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.34.1 | `qwen2.5-coder:3b` | 69,4% (53,1 a 82,0) | 68,8% | 0 | 0 | 1,0000 | nenhum | nenhum | sim | 0 / 0 | nenhum |
| 0.34.1 | `qwen2.5-coder:7b` | 75,0% (58,9 a 86,2) | 80,0% | 0 | 0 | 1,0000 | nenhum | nenhum | sim | 0 / 0 | nenhum |
| 0.34.1 | `qwen2.5:7b` | 77,8% (61,9 a 88,3) | 78,8% | 1 | 1 | 1,0000 | `sin-14` | `tra-10` | sim | 1 / 1 | nenhum |
| 0.34.4 | `qwen2.5-coder:3b` | 72,2% (56,0 a 84,2) | 70,4% | 1 | 0 | 1,0000 | `tra-4` | nenhum | sim | 1 / 0 | `efe-3` |
| 0.34.4 | `qwen2.5-coder:7b` | 80,6% (65,0 a 90,2) | 82,5% | 3 | 1 | 0,6250 | `efe-3`, `semt-14`, `tra-11` | `sin-14` | **não** | 2 / 1 | `efe-3` |
| 0.34.4 | `qwen2.5:7b` | 75,0% (58,9 a 86,2) | 79,6% | 0 | 1 | 1,0000 | nenhum | `tra-4` | sim | 0 / 1 | `efe-3` |
<!-- /tabela:tb_pontes -->

<!-- tabela:tb_ruido -->
| Modelo (L0, 36 casos) | Corrida A | Corrida B | Casos que mudaram de acerto | Com a mesma entrada (sem o caso de texto corrigido) | Só B acertou | Só A acertou | Rótulos que mudaram | Quais mudaram de acerto |
|---|---|---|---|---|---|---|---|---|
| `qwen2.5:7b` | Fase 3 (0.34.0) | ponte 0.34.1 | 2 | 2 | 1 | 1 | 3 | `sin-14`, `tra-10` |
| `qwen2.5:7b` | Fase 3 (0.34.0) | ponte 0.34.4 | 1 | 1 | 0 | 1 | 3 | `tra-4` |
| `qwen2.5:7b` | ponte 0.34.1 | ponte 0.34.4 | 3 | 3 | 1 | 2 | 3 | `sin-14`, `tra-10`, `tra-4` |
| `qwen2.5-coder:7b` | Fase 3 (0.34.0) | ponte 0.34.1 | 0 | 0 | 0 | 0 | 1 | nenhum |
| `qwen2.5-coder:7b` | Fase 3 (0.34.0) | ponte 0.34.4 | 4 | 3 | 3 | 1 | 4 | `efe-3`, `semt-14`, `sin-14`, `tra-11` |
| `qwen2.5-coder:7b` | ponte 0.34.1 | ponte 0.34.4 | 4 | 3 | 3 | 1 | 4 | `efe-3`, `semt-14`, `sin-14`, `tra-11` |
| `qwen2.5-coder:3b` | Fase 3 (0.34.0) | ponte 0.34.1 | 0 | 0 | 0 | 0 | 2 | nenhum |
| `qwen2.5-coder:3b` | Fase 3 (0.34.0) | ponte 0.34.4 | 1 | 1 | 1 | 0 | 2 | `tra-4` |
| `qwen2.5-coder:3b` | ponte 0.34.1 | ponte 0.34.4 | 1 | 1 | 1 | 0 | 4 | `tra-4` |
<!-- /tabela:tb_ruido -->

<!-- tabela:tb_ineditos -->
| Modelo | Biblioteca | Acerto nos 36 inéditos (IC 95%) | Acurácia balanceada | Contra L0: b / c | p (McNemar) | Rótulos que mudaram contra L0 | s por diagnóstico (mediana) |
|---|---|---|---|---|---|---|---|
| `qwen2.5-coder:3b` | L0 | 58,3% (42,2 a 72,9) | 68,1% | n/a | n/a | n/a | 38,1 |
| `qwen2.5-coder:3b` | L1 | 58,3% (42,2 a 72,9) | 68,1% | 0 / 0 | 1,0000 | 0 | 22,3 |
| `qwen2.5-coder:3b` | L3 | 58,3% (42,2 a 72,9) | 68,1% | 0 / 0 | 1,0000 | 1 | 27,8 |
| `qwen2.5:7b` | L0 | 75,0% (58,9 a 86,2) | 81,2% | n/a | n/a | n/a | 73,0 |
| `qwen2.5:7b` | L1 | 72,2% (56,0 a 84,2) | 79,0% | 0 / 1 | 1,0000 | 3 | 75,5 |
| `qwen2.5:7b` | L3 | 80,6% (65,0 a 90,2) | 87,0% | 3 / 1 | 0,6250 | 6 | 66,0 |
<!-- /tabela:tb_ineditos -->

<!-- tabela:tb_agrupado -->
| Modelo | Biblioteca | Casos (oficiais + inéditos) | Acerto com L0 | Acerto com a biblioteca | Oficiais: b / c | Inéditos: b / c | Somados: b / c | Diferença | p (McNemar) |
|---|---|---|---|---|---|---|---|---|---|
| `qwen2.5-coder:3b` | L1 | 72 | 63,9% | 65,3% | 1 / 0 | 0 / 0 | 1 / 0 | +1,4 pp | 1,0000 |
| `qwen2.5-coder:3b` | L3 | 72 | 63,9% | 65,3% | 1 / 0 | 0 / 0 | 1 / 0 | +1,4 pp | 1,0000 |
| `qwen2.5:7b` | L1 | 72 | 76,4% | 80,6% | 4 / 0 | 0 / 1 | 4 / 1 | +4,2 pp | 0,3750 |
| `qwen2.5:7b` | L3 | 72 | 76,4% | 83,3% | 3 / 0 | 3 / 1 | 6 / 1 | +6,9 pp | 0,1250 |
<!-- /tabela:tb_agrupado -->

<!-- tabela:tb_cruzada -->
| Quem lê | Biblioteca lida | Acerto nos 36 (IC 95%) | Acurácia balanceada | Verbete de ouro no contexto | Contexto com nota | Citou verbete anotado | Tokens de entrada (mediana) | s por diagnóstico (mediana) |
|---|---|---|---|---|---|---|---|---|
| `qwen2.5:7b` | L0, Fase 3 (Ollama 0.34.0) | 77,8% (61,9 a 88,3) | 81,2% | 86,1% | 0,0% | 0,0% | 1044 | 69,5 |
| `qwen2.5:7b` | L0, ponte (Ollama 0.34.4) | 75,0% (58,9 a 86,2) | 79,6% | 86,1% | 0,0% | 0,0% | 1044 | 68,9 |
| `qwen2.5:7b` | L1 própria, Fase 3 (Ollama 0.34.0) | 88,9% (74,7 a 95,6) | 91,7% | 83,3% | 94,4% | 66,7% | 1294 | 79,5 |
| `qwen2.5:7b` | L3 própria, Fase 3 (Ollama 0.34.0) | 86,1% (71,3 a 93,9) | 86,2% | 86,1% | 94,4% | 83,3% | 1438 | 53,9 |
| `qwen2.5-coder:7b` | L0, Fase 3 (Ollama 0.34.0) | 75,0% (58,9 a 86,2) | 80,0% | 86,1% | 0,0% | 0,0% | 1044 | 70,7 |
| `qwen2.5-coder:7b` | L0, ponte (Ollama 0.34.4) | 80,6% (65,0 a 90,2) | 82,5% | 86,1% | 0,0% | 0,0% | 1044 | 72,0 |
| `qwen2.5-coder:7b` | L1 própria, Fase 3 (Ollama 0.34.0) | 75,0% (58,9 a 86,2) | 80,0% | 86,1% | 72,2% | 55,6% | 1102 | 65,8 |
| `qwen2.5-coder:7b` | L3 própria, Fase 3 (Ollama 0.34.0) | 77,8% (61,9 a 88,3) | 84,2% | 86,1% | 100,0% | 55,6% | 1207 | 56,6 |
| `qwen2.5-coder:7b` | L1 do doador, cruzada (Ollama 0.34.4) | 83,3% (68,1 a 92,1) | 88,3% | 83,3% | 94,4% | 69,4% | 1295 | 76,6 |
| `qwen2.5-coder:7b` | L3 do doador, cruzada (Ollama 0.34.4) | 83,3% (68,1 a 92,1) | 88,3% | 86,1% | 94,4% | 77,8% | 1438 | 71,3 |
| `qwen2.5-coder:3b` | L0, Fase 3 (Ollama 0.34.0) | 69,4% (53,1 a 82,0) | 68,8% | 86,1% | 0,0% | 0,0% | 1044 | 32,2 |
| `qwen2.5-coder:3b` | L0, ponte (Ollama 0.34.4) | 72,2% (56,0 a 84,2) | 70,4% | 86,1% | 0,0% | 0,0% | 1044 | 30,9 |
| `qwen2.5-coder:3b` | L1 própria, Fase 3 (Ollama 0.34.0) | 72,2% (56,0 a 84,2) | 70,4% | 86,1% | 8,3% | 8,3% | 1046 | 17,8 |
| `qwen2.5-coder:3b` | L3 própria, Fase 3 (Ollama 0.34.0) | 72,2% (56,0 a 84,2) | 71,2% | 86,1% | 50,0% | 27,8% | 1074 | 20,9 |
| `qwen2.5-coder:3b` | L1 do doador, cruzada (Ollama 0.34.4) | 61,1% (44,9 a 75,2) | 60,4% | 83,3% | 94,4% | 52,8% | 1295 | 35,2 |
| `qwen2.5-coder:3b` | L3 do doador, cruzada (Ollama 0.34.4) | 61,1% (44,9 a 75,2) | 60,4% | 86,1% | 94,4% | 77,8% | 1438 | 29,5 |
<!-- /tabela:tb_cruzada -->

<!-- tabela:tb_cruzada_pareados -->
| Leitor com a biblioteca do doador | Comparado com | Mesma versão do Ollama | Pareável pela ponte | b (ganhos) | c (perdas) | Diferença | p (McNemar) | b / c sem o caso de texto corrigido | Rótulos que mudaram | Ganhou | Perdeu | Trocas em casos que já oscilam entre corridas de L0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `qwen2.5-coder:7b` lendo L1 | o próprio L0 na ponte (mesma versão do Ollama) | sim | sim | 3 | 2 | +2,8 pp | 1,0000 | 3 / 2 | 5 | `semt-8`, `sin-14`, `tra-10` | `semt-14`, `sin-5` | `semt-14`, `sin-14` |
| `qwen2.5-coder:7b` lendo L1 | a própria biblioteca na Fase 3 | não | não | 4 | 1 | +8,3 pp | 0,3750 | 3 / 1 | 6 | `efe-3`, `semt-8`, `tra-10`, `tra-11` | `sin-5` | n/a |
| `qwen2.5-coder:7b` lendo L1 | o doador lendo a mesma biblioteca (Fase 3) | não | não | 1 | 3 | -5,6 pp | 0,6250 | 0 / 3 | 5 | `efe-3` | `semt-14`, `tra-4`, `tra-8` | n/a |
| `qwen2.5-coder:7b` lendo L3 | o próprio L0 na ponte (mesma versão do Ollama) | sim | sim | 3 | 2 | +2,8 pp | 1,0000 | 3 / 2 | 5 | `semt-8`, `sin-14`, `tra-10` | `semt-14`, `tra-11` | `semt-14`, `sin-14`, `tra-11` |
| `qwen2.5-coder:7b` lendo L3 | a própria biblioteca na Fase 3 | não | não | 2 | 0 | +5,6 pp | 0,5000 | 2 / 0 | 2 | `sin-14`, `sin-5` | nenhum | n/a |
| `qwen2.5-coder:7b` lendo L3 | o doador lendo a mesma biblioteca (Fase 3) | não | não | 3 | 4 | -2,8 pp | 1,0000 | 3 / 4 | 7 | `efe-1`, `run-10`, `sin-14` | `semt-14`, `tra-11`, `tra-4`, `tra-8` | n/a |
| `qwen2.5-coder:3b` lendo L1 | o próprio L0 na ponte (mesma versão do Ollama) | sim | sim | 1 | 5 | -11,1 pp | 0,2188 | 1 / 5 | 8 | `semt-3` | `efe-3`, `semt-8`, `sin-11`, `sin-14`, `sin-5` | nenhum |
| `qwen2.5-coder:3b` lendo L1 | a própria biblioteca na Fase 3 | não | sim | 1 | 5 | -11,1 pp | 0,2188 | 1 / 4 | 7 | `semt-3` | `efe-3`, `semt-8`, `sin-11`, `sin-14`, `sin-5` | n/a |
| `qwen2.5-coder:3b` lendo L1 | o doador lendo a mesma biblioteca (Fase 3) | não | sim | 0 | 10 | -27,8 pp | 0,0020 | 0 / 10 | 13 | nenhum | `efe-1`, `efe-2`, `lex-1`, `lex-4`, `semt-14`, `semt-8`, `sin-11`, `sin-14`, `sin-4`, `tra-10` | n/a |
| `qwen2.5-coder:3b` lendo L3 | o próprio L0 na ponte (mesma versão do Ollama) | sim | sim | 1 | 5 | -11,1 pp | 0,2188 | 1 / 5 | 8 | `semt-3` | `efe-3`, `semt-8`, `sin-11`, `sin-14`, `sin-5` | nenhum |
| `qwen2.5-coder:3b` lendo L3 | a própria biblioteca na Fase 3 | não | sim | 1 | 5 | -11,1 pp | 0,2188 | 1 / 4 | 8 | `tra-4` | `efe-3`, `semt-8`, `sin-11`, `sin-14`, `sin-5` | n/a |
| `qwen2.5-coder:3b` lendo L3 | o doador lendo a mesma biblioteca (Fase 3) | não | sim | 1 | 10 | -25,0 pp | 0,0117 | 1 / 9 | 13 | `run-10` | `efe-2`, `efe-3`, `lex-1`, `lex-4`, `semt-14`, `semt-8`, `sin-11`, `sin-4`, `sin-5`, `tra-10` | n/a |
<!-- /tabela:tb_cruzada_pareados -->

<!-- tabela:tb_cruzada_classe -->
| Quem lê | Biblioteca lida | lexica (acertos / casos) | sintatica (acertos / casos) | semantica (acertos / casos) | traducao (acertos / casos) | runtime (acertos / casos) | efeito (acertos / casos) |
|---|---|---|---|---|---|---|---|
| `qwen2.5-coder:7b` | L0 (ponte) | 6 / 6 | 5 / 6 | 4 / 6 | 2 / 6 | 6 / 6 | 6 / 6 |
| `qwen2.5-coder:7b` | L1 do doador | 6 / 6 | 5 / 6 | 4 / 6 | 3 / 6 | 6 / 6 | 6 / 6 |
| `qwen2.5-coder:7b` | L3 do doador | 6 / 6 | 6 / 6 | 4 / 6 | 2 / 6 | 6 / 6 | 6 / 6 |
| `qwen2.5-coder:7b` | L1 própria (Fase 3) | 6 / 6 | 6 / 6 | 3 / 6 | 1 / 6 | 6 / 6 | 5 / 6 |
| `qwen2.5-coder:7b` | L3 própria (Fase 3) | 6 / 6 | 4 / 6 | 4 / 6 | 2 / 6 | 6 / 6 | 6 / 6 |
| `qwen2.5-coder:3b` | L0 (ponte) | 4 / 6 | 5 / 6 | 3 / 6 | 4 / 6 | 6 / 6 | 4 / 6 |
| `qwen2.5-coder:3b` | L1 do doador | 4 / 6 | 2 / 6 | 3 / 6 | 4 / 6 | 6 / 6 | 3 / 6 |
| `qwen2.5-coder:3b` | L3 do doador | 4 / 6 | 2 / 6 | 3 / 6 | 4 / 6 | 6 / 6 | 3 / 6 |
| `qwen2.5-coder:3b` | L1 própria (Fase 3) | 4 / 6 | 5 / 6 | 3 / 6 | 4 / 6 | 6 / 6 | 4 / 6 |
| `qwen2.5-coder:3b` | L3 própria (Fase 3) | 4 / 6 | 5 / 6 | 4 / 6 | 3 / 6 | 6 / 6 | 4 / 6 |
<!-- /tabela:tb_cruzada_classe -->

<!-- tabela:tb_cruzada_rotulos -->
| Quem lê | Biblioteca lida | Rótulo mais respondido | Respostas com ele | Respostas com ele em L0 | Casos com essa causa no gabarito | Rótulos distintos | Verbetes mais citados na linha FONTE (respostas) | Verbetes mais presentes no contexto (casos) |
|---|---|---|---|---|---|---|---|---|
| `qwen2.5-coder:7b` | L1 do doador | `estrutura_aninhada_divergente` | 4 (11,1%) | 3 | 1 | 20 | `entidade-produto` (5); `localizador_quebrado` (4); `contrato-pedido` (3) | `entidade-produto` (18); `contrato-produto` (15); `contrato-pedido` (9) |
| `qwen2.5-coder:7b` | L3 do doador | `estrutura_aninhada_divergente` | 4 (11,1%) | 3 | 1 | 19 | `estrutura_aninhada_divergente` (4); `localizador_quebrado` (4); `contrato-pedido` (3) | `entidade-produto` (18); `contrato-produto` (15); `contrato-pedido` (9) |
| `qwen2.5-coder:7b` | L0 (ponte) | `campo_ausente` | 4 (11,1%) | 4 | 3 | 19 | `contrato-pedido` (4); `localizador_quebrado` (4); `entidade-produto` (3) | `entidade-produto` (19); `contrato-produto` (16); `contrato-pedido` (9) |
| `qwen2.5-coder:3b` | L1 do doador | `corpo_nao_e_json` | 7 (19,4%) | 2 | 0 | 17 | `contrato-produto` (10); `contrato-pedido` (6); `contagem_inconsistente` (4) | `entidade-produto` (18); `contrato-produto` (15); `contrato-pedido` (9) |
| `qwen2.5-coder:3b` | L3 do doador | `corpo_nao_e_json` | 7 (19,4%) | 2 | 0 | 17 | `contrato-produto` (10); `contrato-pedido` (6); `contagem_inconsistente` (3) | `entidade-produto` (18); `contrato-produto` (15); `contrato-pedido` (9) |
| `qwen2.5-coder:3b` | L0 (ponte) | `campo_ausente` | 6 (16,7%) | 6 | 3 | 18 | `contrato-produto` (6); `contrato-pedido` (5); `contagem_inconsistente` (4) | `entidade-produto` (19); `contrato-produto` (16); `contrato-pedido` (9) |
<!-- /tabela:tb_cruzada_rotulos -->

<!-- tabela:tb_cruzada_casos -->
| Quem lê | Biblioteca do doador | Caso | Passou a | Causa do gabarito | Resposta com L0 | Resposta com a biblioteca do doador | Fonte citada com L0 | Fonte citada com a biblioteca do doador | Verbete de ouro no contexto | O doador acerta este caso com ela |
|---|---|---|---|---|---|---|---|---|---|---|
| `qwen2.5-coder:7b` | L1 | `semt-14` | errado | `nulo_inesperado` | `nulo_inesperado` | `campo_ausente` | `entidade-produto` | `contrato-produto` | sim | sim |
| `qwen2.5-coder:7b` | L1 | `semt-8` | certo | `nulo_inesperado` | `valor_fora_do_dominio` | `nulo_inesperado` | `contrato-produto` | `nulo_inesperado` | sim | sim |
| `qwen2.5-coder:7b` | L1 | `sin-14` | certo | `campo_renomeado` | `campo_ausente` | `campo_renomeado` | `contrato-produto` | `campo_renomeado` | sim | sim |
| `qwen2.5-coder:7b` | L1 | `sin-5` | errado | `campo_ausente` | `campo_ausente` | `estrutura_aninhada_divergente` | `campo_ausente` | `entidade-produto` | não | não |
| `qwen2.5-coder:7b` | L1 | `tra-10` | certo | `chave_de_juncao_errada` | `valor_fora_do_dominio` | `chave_de_juncao_errada` | `contrato-pedido` | `contrato-pedido` | não | sim |
| `qwen2.5-coder:7b` | L3 | `semt-14` | errado | `nulo_inesperado` | `nulo_inesperado` | `tipo_divergente` | `entidade-produto` | `contrato-produto` | sim | sim |
| `qwen2.5-coder:7b` | L3 | `semt-8` | certo | `nulo_inesperado` | `valor_fora_do_dominio` | `nulo_inesperado` | `contrato-produto` | `nulo_inesperado` | sim | sim |
| `qwen2.5-coder:7b` | L3 | `sin-14` | certo | `campo_renomeado` | `campo_ausente` | `campo_renomeado` | `contrato-produto` | `campo_renomeado` | sim | não |
| `qwen2.5-coder:7b` | L3 | `tra-10` | certo | `chave_de_juncao_errada` | `valor_fora_do_dominio` | `chave_de_juncao_errada` | `contrato-pedido` | `contrato-pedido` | não | sim |
| `qwen2.5-coder:7b` | L3 | `tra-11` | errado | `contagem_inconsistente` | `contagem_inconsistente` | `estrutura_aninhada_divergente` | `contagem_inconsistente` | `estrutura_aninhada_divergente` | sim | sim |
| `qwen2.5-coder:3b` | L1 | `efe-3` | errado | `campo_ausente` | `campo_ausente` | `corpo_nao_e_json` | `campo_ausente` | `contrato-produto` | sim | não |
| `qwen2.5-coder:3b` | L1 | `semt-3` | certo | `valor_fora_do_dominio` | `estado_da_tela_divergente` | `valor_fora_do_dominio` | `estado_da_tela_divergente` | `contrato-pedido` | sim | sim |
| `qwen2.5-coder:3b` | L1 | `semt-8` | errado | `nulo_inesperado` | `nulo_inesperado` | `corpo_nao_e_json` | `nulo_inesperado` | `contrato-produto` | sim | sim |
| `qwen2.5-coder:3b` | L1 | `sin-11` | errado | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | `corpo_vazio` | `estrutura_aninhada_divergente` | `entidade-produto`, `contagem_inconsistente` | sim | sim |
| `qwen2.5-coder:3b` | L1 | `sin-14` | errado | `campo_renomeado` | `campo_renomeado` | `corpo_nao_e_json` | `campo_renomeado` | `contrato-produto` | sim | sim |
| `qwen2.5-coder:3b` | L1 | `sin-5` | errado | `campo_ausente` | `campo_ausente` | `corpo_nao_e_json` | `campo_ausente` | `contrato-produto` | não | não |
| `qwen2.5-coder:3b` | L3 | `efe-3` | errado | `campo_ausente` | `campo_ausente` | `corpo_nao_e_json` | `campo_ausente` | `entidade-produto`, `contrato-produto` | sim | sim |
| `qwen2.5-coder:3b` | L3 | `semt-3` | certo | `valor_fora_do_dominio` | `estado_da_tela_divergente` | `valor_fora_do_dominio` | `estado_da_tela_divergente` | `contrato-pedido`, `valor_fora_do_dominio` | sim | sim |
| `qwen2.5-coder:3b` | L3 | `semt-8` | errado | `nulo_inesperado` | `nulo_inesperado` | `corpo_nao_e_json` | `nulo_inesperado` | `contrato-produto` | sim | sim |
| `qwen2.5-coder:3b` | L3 | `sin-11` | errado | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | `corpo_vazio` | `estrutura_aninhada_divergente` | nenhum | sim | sim |
| `qwen2.5-coder:3b` | L3 | `sin-14` | errado | `campo_renomeado` | `campo_renomeado` | `corpo_nao_e_json` | `campo_renomeado` | `contrato-produto` | sim | não |
| `qwen2.5-coder:3b` | L3 | `sin-5` | errado | `campo_ausente` | `campo_ausente` | `corpo_nao_e_json` | `campo_ausente` | `contrato-produto` | sim | sim |
<!-- /tabela:tb_cruzada_casos -->
