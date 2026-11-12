<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase4.py --texto a partir de relatorios/ e relatorios_v3/ das corridas vigentes, biblioteca_producao/ e biblioteca_producao_leitura/, e limiares_texto.json (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# O que chega ao analista: os filtros de prolixidade e objetividade, antes e depois (Pós-Fase 4, pacote Q2), gerada em 2026-11-10

Um texto passa quando fica dentro dos limiares de palavras por frase (média e máximo), preenchimento, repetição e compressão e não tem termo da lista fechada sem expansão na primeira menção; o Flesch abaixo de 50 só acende o alarme; densidade e tamanho não aprovam nem reprovam. Os limiares calibrados vêm do percentil 95 do corpus de referência (os textos "! Motivo:" dos comentários de IA deste repositório e o exemplo canônico do resumo técnico do Eric, lido da memória do repositório TargetERP sem copiar texto) e são declarados como calibração; os valores de fonte são o alarme do Flesch (50) e o zero de jargão sem expansão (Lei 15.263/2025, art. 5). O tamanho em palavras entra como covariável e nunca como critério.


<!-- tabela:tb_f4_texto_resumo -->
| Grupo | Textos | Passam em tudo antes | Passam em tudo depois | Alarme do Flesch antes | Alarme do Flesch depois | Termos sem expansão antes (ocorrências) | Termos sem expansão depois (ocorrências) | Palavras antes (mediana) | Palavras depois (mediana) | De onde vem o antes |
|---|---|---|---|---|---|---|---|---|---|---|
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | 74 | 0 (0,0%) | 74 (100,0%) | 74 | 0 | 333 | 0 | 354 | 1030 | v2 gravado em 74 e regerado da trilha em 0 |
| corrida 21d (ensaio dos cenários da Fase 5) | 10 | 0 (0,0%) | 10 (100,0%) | 10 | 0 | 40 | 0 | 380 | 1104 | v2 gravado em 10 e regerado da trilha em 0 |
| corrida 24 (os 36 inéditos em texto) | 36 | 0 (0,0%) | 36 (100,0%) | 35 | 0 | 180 | 0 | 294 | 930 | v2 gravado em 0 e regerado da trilha em 36 |
| verbetes da biblioteca de produção e a camada de leitura | 39 | 14 (35,9%) | 39 (100,0%) | 15 | 3 | 12 | 0 | 95 | 277 | leitura gerada por biblioteca_leitura.py |
<!-- /tabela:tb_f4_texto_resumo -->

<!-- tabela:tb_f4_texto_metricas -->
| Métrica | Regra | Limiar | Tipo do limiar | Valor provisório do plano | Fonte |
|---|---|---|---|---|---|
| Palavras por frase (média) | até o limiar | 77,0000 | calibracao | 20 | calibração no corpus de referência (percentil 95 das médias); a Lei 15.263/2025 (art. 5) e a ISO 24495-1 só dizem "frases curtas" (base D, itens 8 e 9) |
| Palavras por frase (máximo) | até o limiar | 78,9000 | calibracao | 30 | calibração no corpus de referência (percentil 95 do comprimento de todas as frases do corpus); mesma base da média |
| Flesch adaptado ao português | alarme abaixo do valor | 50,0000 | fonte | não há | fórmula do NILC-Metrix (Leal et al., 2023): 248,835 - 1,015 x palavras por frase - 84,6 x sílabas por palavra; 50 é a fronteira da faixa "fácil" de Martins et al. (1996), citada pela dissertação da PUC-Rio; só alarme, porque a literatura chama o índice de superficial (base D, itens 1 a 3) |
| Razão de preenchimento (lista fechada) | até o limiar | 0,0000 | calibracao | não há | lista traduzida do guia de tom do Google (base D, item 11) e das marcas de hesitação de Zhang, Das e Zhang (2024, item 6); limiar: percentil 95 do corpus |
| Repetição interna (trigramas repetidos) | até o limiar | 0,0314 | calibracao | não há | ataque da lista repetitiva de Zheng et al. (2023, item 4): dois dos três juízes-modelo caíram em 91,3% dos casos; limiar: percentil 95 do corpus |
| Taxa de compressão (palavras de conteúdo por palavra distinta, em janelas de 100) | até o limiar | 1,4818 | calibracao | não há | verboso como "comprimível" (Zhang, Das e Zhang, 2024, item 6); o denominador (palavras distintas de conteúdo, por janela de 100 palavras) é desenho nosso; limiar: percentil 95 do corpus |
| Jargão e sigla sem expansão na primeira menção (lista fechada) | zero ocorrências | 0 | fonte | não há | Lei 15.263/2025, art. 5 (jargão trocado ou explicado; nome completo antes da sigla); a lista é deste repositório: a regra dos comentários de IA (CLAUDE.md), os termos da trilha vetados nos testes do Q1 e os termos de modelo e de estatística das abas da Fase 4 |
| Densidade de termos do domínio por palavra (lista fechada) | só para comparar | sem valor | comparacao | não há | Adams et al. (2023, item 7), densidade de entidades por token, adaptada à lista fechada de nomes do projeto mais os trechos entre crases; só para comparar, sem limiar |
| Tamanho em palavras | covariável, nunca critério | não há | sem limiar | não há | Dubois et al. (2024) e Zheng et al. (2023): o tamanho infla a nota de qualquer juiz-modelo; entra nas tabelas e nunca como critério (base D, itens 4 e 5) |
<!-- /tabela:tb_f4_texto_metricas -->

<!-- tabela:tb_f4_texto_medias -->
| Grupo | Versão | Textos | Passam em tudo | Alarme do Flesch | Palavras por frase (média) | Palavras por frase (máximo, média dos textos) | Flesch | Preenchimento | Repetição | Compressão | Termos sem expansão (média) | Densidade do domínio | Palavras (mediana) | Trechos em código (média) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | relatório v2 | 74 | 0 (0,0%) | 74 (100,0%) | 14,73 | 57,9 | 37,4 | 0,0000 | 0,0300 | 1,278 | 4,50 | 0,3410 | 354 | 36,7 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | relatório v3 | 74 | 74 (100,0%) | 0 (0,0%) | 15,98 | 50,7 | 64,9 | 0,0000 | 0,0110 | 1,201 | 0,00 | 0,2990 | 1030 | 109,7 |
| corrida 21d (ensaio dos cenários da Fase 5) | relatório v2 | 10 | 0 (0,0%) | 10 (100,0%) | 16,27 | 63,0 | 36,3 | 0,0000 | 0,0380 | 1,272 | 4,00 | 0,3490 | 380 | 45,8 |
| corrida 21d (ensaio dos cenários da Fase 5) | relatório v3 | 10 | 10 (100,0%) | 0 (0,0%) | 15,58 | 49,2 | 64,6 | 0,0000 | 0,0160 | 1,203 | 0,00 | 0,2980 | 1104 | 129,8 |
| corrida 24 (os 36 inéditos em texto) | relatório v2 | 36 | 0 (0,0%) | 35 (97,2%) | 13,95 | 52,2 | 36,6 | 0,0000 | 0,0360 | 1,295 | 5,00 | 0,3500 | 294 | 34,1 |
| corrida 24 (os 36 inéditos em texto) | relatório v3 | 36 | 36 (100,0%) | 0 (0,0%) | 15,71 | 50,3 | 62,8 | 0,0000 | 0,0100 | 1,190 | 0,00 | 0,3070 | 930 | 95,0 |
| verbetes da biblioteca de produção e a camada de leitura | verbete | 39 | 14 (35,9%) | 15 (38,5%) | 16,00 | 29,3 | 54,1 | 0,0010 | 0,0480 | 1,293 | 0,31 | 0,1500 | 95 | 0,0 |
| verbetes da biblioteca de produção e a camada de leitura | leitura | 39 | 39 (100,0%) | 3 (7,7%) | 14,26 | 32,2 | 57,8 | 0,0000 | 0,0050 | 1,195 | 0,00 | 0,2790 | 277 | 28,4 |
<!-- /tabela:tb_f4_texto_medias -->

<!-- tabela:tb_f4_texto_criterios -->
| Grupo | Critério | Limiar | Passam antes | Passam depois |
|---|---|---|---|---|
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | Palavras por frase (média) | 77,0000 | 74 de 74 (100,0%) | 74 de 74 (100,0%) |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | Palavras por frase (máximo) | 78,9000 | 74 de 74 (100,0%) | 74 de 74 (100,0%) |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | Razão de preenchimento (lista fechada) | 0,0000 | 74 de 74 (100,0%) | 74 de 74 (100,0%) |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | Repetição interna (trigramas repetidos) | 0,0314 | 49 de 74 (66,2%) | 74 de 74 (100,0%) |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | Taxa de compressão (palavras de conteúdo por palavra distinta, em janelas de 100) | 1,4818 | 74 de 74 (100,0%) | 74 de 74 (100,0%) |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | Jargão e sigla sem expansão na primeira menção (lista fechada) | 0 | 0 de 74 (0,0%) | 74 de 74 (100,0%) |
| corrida 21d (ensaio dos cenários da Fase 5) | Palavras por frase (média) | 77,0000 | 10 de 10 (100,0%) | 10 de 10 (100,0%) |
| corrida 21d (ensaio dos cenários da Fase 5) | Palavras por frase (máximo) | 78,9000 | 10 de 10 (100,0%) | 10 de 10 (100,0%) |
| corrida 21d (ensaio dos cenários da Fase 5) | Razão de preenchimento (lista fechada) | 0,0000 | 10 de 10 (100,0%) | 10 de 10 (100,0%) |
| corrida 21d (ensaio dos cenários da Fase 5) | Repetição interna (trigramas repetidos) | 0,0314 | 4 de 10 (40,0%) | 10 de 10 (100,0%) |
| corrida 21d (ensaio dos cenários da Fase 5) | Taxa de compressão (palavras de conteúdo por palavra distinta, em janelas de 100) | 1,4818 | 10 de 10 (100,0%) | 10 de 10 (100,0%) |
| corrida 21d (ensaio dos cenários da Fase 5) | Jargão e sigla sem expansão na primeira menção (lista fechada) | 0 | 0 de 10 (0,0%) | 10 de 10 (100,0%) |
| corrida 24 (os 36 inéditos em texto) | Palavras por frase (média) | 77,0000 | 36 de 36 (100,0%) | 36 de 36 (100,0%) |
| corrida 24 (os 36 inéditos em texto) | Palavras por frase (máximo) | 78,9000 | 36 de 36 (100,0%) | 36 de 36 (100,0%) |
| corrida 24 (os 36 inéditos em texto) | Razão de preenchimento (lista fechada) | 0,0000 | 36 de 36 (100,0%) | 36 de 36 (100,0%) |
| corrida 24 (os 36 inéditos em texto) | Repetição interna (trigramas repetidos) | 0,0314 | 19 de 36 (52,8%) | 36 de 36 (100,0%) |
| corrida 24 (os 36 inéditos em texto) | Taxa de compressão (palavras de conteúdo por palavra distinta, em janelas de 100) | 1,4818 | 36 de 36 (100,0%) | 36 de 36 (100,0%) |
| corrida 24 (os 36 inéditos em texto) | Jargão e sigla sem expansão na primeira menção (lista fechada) | 0 | 0 de 36 (0,0%) | 36 de 36 (100,0%) |
| verbetes da biblioteca de produção e a camada de leitura | Palavras por frase (média) | 77,0000 | 39 de 39 (100,0%) | 39 de 39 (100,0%) |
| verbetes da biblioteca de produção e a camada de leitura | Palavras por frase (máximo) | 78,9000 | 39 de 39 (100,0%) | 39 de 39 (100,0%) |
| verbetes da biblioteca de produção e a camada de leitura | Razão de preenchimento (lista fechada) | 0,0000 | 36 de 39 (92,3%) | 39 de 39 (100,0%) |
| verbetes da biblioteca de produção e a camada de leitura | Repetição interna (trigramas repetidos) | 0,0314 | 22 de 39 (56,4%) | 39 de 39 (100,0%) |
| verbetes da biblioteca de produção e a camada de leitura | Taxa de compressão (palavras de conteúdo por palavra distinta, em janelas de 100) | 1,4818 | 34 de 39 (87,2%) | 39 de 39 (100,0%) |
| verbetes da biblioteca de produção e a camada de leitura | Jargão e sigla sem expansão na primeira menção (lista fechada) | 0 | 29 de 39 (74,4%) | 39 de 39 (100,0%) |
<!-- /tabela:tb_f4_texto_criterios -->

<!-- tabela:tb_f4_texto_termos -->
| Grupo | Termo sem expansão na primeira menção | Textos antes | Textos depois |
|---|---|---|---|
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | gen_ai | 74 | 0 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | hash | 74 | 0 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | ollama | 74 | 0 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | prov.used | 74 | 0 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | prompt | 37 | 0 |
| corrida 21d (ensaio dos cenários da Fase 5) | gen_ai | 10 | 0 |
| corrida 21d (ensaio dos cenários da Fase 5) | hash | 10 | 0 |
| corrida 21d (ensaio dos cenários da Fase 5) | ollama | 10 | 0 |
| corrida 21d (ensaio dos cenários da Fase 5) | prov.used | 10 | 0 |
| corrida 24 (os 36 inéditos em texto) | gen_ai | 36 | 0 |
| corrida 24 (os 36 inéditos em texto) | hash | 36 | 0 |
| corrida 24 (os 36 inéditos em texto) | ollama | 36 | 0 |
| corrida 24 (os 36 inéditos em texto) | prompt | 36 | 0 |
| corrida 24 (os 36 inéditos em texto) | prov.used | 36 | 0 |
| verbetes da biblioteca de produção e a camada de leitura | token | 4 | 0 |
| verbetes da biblioteca de produção e a camada de leitura | enum | 2 | 0 |
| verbetes da biblioteca de produção e a camada de leitura | frontend | 2 | 0 |
| verbetes da biblioteca de produção e a camada de leitura | hash | 2 | 0 |
| verbetes da biblioteca de produção e a camada de leitura | backend | 1 | 0 |
| verbetes da biblioteca de produção e a camada de leitura | schema | 1 | 0 |
<!-- /tabela:tb_f4_texto_termos -->

<!-- tabela:tb_f4_texto_preenchimentos -->
| Grupo | Preenchimento (lista fechada) | Textos antes | Textos depois |
|---|---|---|---|
| verbetes da biblioteca de produção e a camada de leitura | claramente | 2 | 0 |
| verbetes da biblioteca de produção e a camada de leitura | na verdade | 1 | 0 |
<!-- /tabela:tb_f4_texto_preenchimentos -->

<!-- tabela:tb_f4_texto_modelo -->
| Frases do modelo | Por corrida | Passam em tudo | Alarme do Flesch | Palavras por frase (média) | Flesch | Preenchimento | Repetição | Termos sem expansão | Palavras (mediana) |
|---|---|---|---|---|---|---|---|---|---|
| 120 | fase4_ensaio_v4 10, fase4_ineditos 36, fase4_tela_v4 74 | 118 (98,3%) | 58 (48,3%) | 18,36 | 49,1 | 0,0010 | 0,0000 | nenhum | 18 |
<!-- /tabela:tb_f4_texto_modelo -->

<!-- tabela:tb_f4_texto_calibracao -->
| Origem dos limiares | Calibrada em | Itens do corpus | Por fonte | Frases do corpus | Métrica | Mediana no corpus | Limiar |
|---|---|---|---|---|---|---|---|
| calibração no corpus de referência | 2026-11-07T19:55:59 | 1674 | exemplo_canonico 17, motivo 1657 | 2663 | Palavras por frase (média) | 34,0000 | 77,0000 |
| calibração no corpus de referência | 2026-11-07T19:55:59 | 1674 | exemplo_canonico 17, motivo 1657 | 2663 | Palavras por frase (máximo) | 38,0000 | 78,9000 |
| calibração no corpus de referência | 2026-11-07T19:55:59 | 1674 | exemplo_canonico 17, motivo 1657 | 2663 | Flesch adaptado ao português | 52,4600 | 50,0000 |
| calibração no corpus de referência | 2026-11-07T19:55:59 | 1674 | exemplo_canonico 17, motivo 1657 | 2663 | Razão de preenchimento (lista fechada) | 0,0000 | 0,0000 |
| calibração no corpus de referência | 2026-11-07T19:55:59 | 1674 | exemplo_canonico 17, motivo 1657 | 2663 | Repetição interna (trigramas repetidos) | 0,0000 | 0,0314 |
| calibração no corpus de referência | 2026-11-07T19:55:59 | 1674 | exemplo_canonico 17, motivo 1657 | 2663 | Taxa de compressão (palavras de conteúdo por palavra distinta, em janelas de 100) | 1,0645 | 1,4818 |
| calibração no corpus de referência | 2026-11-07T19:55:59 | 1674 | exemplo_canonico 17, motivo 1657 | 2663 | Jargão e sigla sem expansão na primeira menção (lista fechada) | sem valor | 0 |
| calibração no corpus de referência | 2026-11-07T19:55:59 | 1674 | exemplo_canonico 17, motivo 1657 | 2663 | Densidade de termos do domínio por palavra (lista fechada) | 0,0548 | sem valor |
<!-- /tabela:tb_f4_texto_calibracao -->

<!-- tabela:tb_f4_texto_casos -->
| Grupo | Texto | Passa antes | Passa depois | Maior frase antes | Maior frase depois | Flesch antes | Flesch depois | Repetição antes | Repetição depois | Termos sem expansão antes | Termos sem expansão depois | Palavras antes | Palavras depois |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `efe-3@fixture` | não | sim | 47 | 49 | 41,8 | 64,1 | 0,015 | 0,007 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 307 | 942 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `efe-3@tela` | não | sim | 60 | 49 | 38,7 | 67,6 | 0,016 | 0,013 | gen_ai, hash, ollama, prov.used | nenhum | 359 | 1073 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `lex-10@fixture` | não | sim | 52 | 53 | 39,1 | 62,9 | 0,029 | 0,013 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 287 | 959 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `lex-10@tela` | não | sim | 59 | 56 | 41,8 | 66,1 | 0,015 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 391 | 1108 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `lex-11@fixture` | não | sim | 47 | 53 | 32,7 | 62,1 | 0,025 | 0,016 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 285 | 955 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `lex-11@tela` | não | sim | 65 | 52 | 29,0 | 64,9 | 0,019 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 370 | 1117 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `lex-16@fixture` | não | sim | 53 | 49 | 48,5 | 65,7 | 0,060 | 0,007 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 293 | 924 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `lex-16@tela` | não | sim | 77 | 49 | 41,8 | 66,6 | 0,036 | 0,013 | gen_ai, hash, ollama, prov.used | nenhum | 380 | 1068 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `lex-18@fixture` | não | sim | 60 | 49 | 39,9 | 62,7 | 0,030 | 0,011 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 376 | 1006 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `lex-18@tela` | não | sim | 60 | 49 | 33,2 | 66,1 | 0,028 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 374 | 1083 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `lex-1@fixture` | não | sim | 47 | 49 | 40,7 | 65,2 | 0,025 | 0,007 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 281 | 924 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `lex-1@tela` | não | sim | 62 | 49 | 39,0 | 67,2 | 0,016 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 358 | 1067 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `lex-4@fixture` | não | sim | 55 | 49 | 35,9 | 62,4 | 0,023 | 0,006 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 352 | 967 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `lex-4@tela` | não | sim | 65 | 49 | 29,0 | 65,3 | 0,019 | 0,011 | gen_ai, hash, ollama, prov.used | nenhum | 370 | 1097 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `lex-7@fixture` | não | sim | 55 | 49 | 45,8 | 66,1 | 0,052 | 0,007 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 293 | 928 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `lex-7@tela` | não | sim | 74 | 49 | 47,0 | 68,0 | 0,030 | 0,014 | gen_ai, hash, ollama, prov.used | nenhum | 382 | 1045 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `lex-8@fixture` | não | sim | 47 | 49 | 32,9 | 62,0 | 0,016 | 0,008 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 300 | 951 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `lex-8@tela` | não | sim | 60 | 49 | 33,2 | 66,1 | 0,028 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 374 | 1083 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `run-19@fixture` | não | sim | 55 | 49 | 38,9 | 63,1 | 0,067 | 0,015 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 295 | 941 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `run-19@tela` | não | sim | 66 | 49 | 38,7 | 66,3 | 0,042 | 0,018 | gen_ai, hash, ollama, prov.used | nenhum | 385 | 1081 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `run-1@fixture` | não | sim | 55 | 49 | 39,7 | 64,6 | 0,066 | 0,010 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 299 | 953 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `run-1@tela` | não | sim | 73 | 51 | 38,2 | 66,5 | 0,042 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 379 | 1098 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `run-21@fixture` | não | sim | 56 | 56 | 37,6 | 61,1 | 0,013 | 0,013 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 346 | 1016 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `run-21@tela` | não | sim | 60 | 59 | 36,3 | 65,2 | 0,016 | 0,011 | gen_ai, hash, ollama, prov.used | nenhum | 366 | 1091 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `run-2@fixture` | não | sim | 63 | 49 | 43,7 | 64,2 | 0,063 | 0,006 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 313 | 936 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `run-2@tela` | não | sim | 66 | 49 | 39,5 | 67,2 | 0,039 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 381 | 1076 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `run-9@fixture` | não | sim | 47 | 49 | 38,1 | 63,0 | 0,025 | 0,015 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 281 | 937 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `run-9@tela` | não | sim | 66 | 49 | 39,5 | 66,3 | 0,039 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 381 | 1072 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `semt-14@fixture` | não | sim | 52 | 55 | 35,9 | 62,0 | 0,015 | 0,011 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 307 | 978 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `semt-14@tela` | não | sim | 60 | 54 | 35,2 | 66,4 | 0,016 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 354 | 1082 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `semt-16@fixture` | não | sim | 47 | 49 | 39,0 | 64,6 | 0,025 | 0,007 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 281 | 940 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `semt-16@tela` | não | sim | 60 | 49 | 37,2 | 68,3 | 0,016 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 354 | 1078 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `semt-17@fixture` | não | sim | 52 | 49 | 36,0 | 63,6 | 0,024 | 0,007 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 293 | 954 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `semt-17@tela` | não | sim | 60 | 49 | 35,7 | 67,6 | 0,016 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 354 | 1076 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `semt-1@fixture` | não | sim | 47 | 49 | 38,6 | 63,5 | 0,025 | 0,007 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 285 | 936 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `semt-1@tela` | não | sim | 65 | 49 | 35,9 | 66,8 | 0,016 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 360 | 1088 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `semt-20@fixture` | não | sim | 51 | 55 | 36,7 | 62,1 | 0,015 | 0,009 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 310 | 980 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `semt-20@tela` | não | sim | 66 | 58 | 36,1 | 66,4 | 0,038 | 0,013 | gen_ai, hash, ollama, prov.used | nenhum | 395 | 1148 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `semt-21@fixture` | não | sim | 46 | 55 | 37,7 | 63,4 | 0,025 | 0,011 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 280 | 958 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `semt-21@tela` | não | sim | 68 | 54 | 33,8 | 65,0 | 0,029 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 431 | 1131 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `semt-8@fixture` | não | sim | 47 | 49 | 36,2 | 64,2 | 0,025 | 0,007 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 281 | 940 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `semt-8@tela` | não | sim | 60 | 49 | 34,9 | 67,8 | 0,016 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 354 | 1066 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `semt-9@fixture` | não | sim | 47 | 49 | 39,0 | 64,8 | 0,025 | 0,007 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 281 | 930 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `semt-9@tela` | não | sim | 60 | 49 | 36,2 | 67,2 | 0,016 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 354 | 1075 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `sin-11@fixture` | não | sim | 52 | 49 | 31,5 | 61,9 | 0,047 | 0,006 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 298 | 924 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `sin-11@tela` | não | sim | 63 | 49 | 30,0 | 65,8 | 0,029 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 361 | 1106 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `sin-14@fixture` | não | sim | 46 | 53 | 38,6 | 63,4 | 0,019 | 0,009 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 308 | 974 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `sin-14@tela` | não | sim | 62 | 52 | 39,2 | 67,0 | 0,019 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 359 | 1084 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `sin-16@fixture` | não | sim | 47 | 49 | 40,0 | 65,3 | 0,025 | 0,007 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 281 | 926 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `sin-16@tela` | não | sim | 60 | 49 | 37,1 | 68,7 | 0,019 | 0,016 | gen_ai, hash, ollama, prov.used | nenhum | 364 | 1064 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `sin-20@fixture` | não | sim | 47 | 53 | 41,2 | 63,5 | 0,025 | 0,013 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 287 | 947 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `sin-20@tela` | não | sim | 65 | 52 | 37,4 | 66,4 | 0,019 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 366 | 1105 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `sin-21@fixture` | não | sim | 50 | 53 | 27,9 | 61,6 | 0,045 | 0,014 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 288 | 953 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `sin-21@tela` | não | sim | 76 | 52 | 33,5 | 65,2 | 0,039 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 383 | 1107 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `sin-4@fixture` | não | sim | 56 | 49 | 41,9 | 65,4 | 0,081 | 0,011 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 302 | 960 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `sin-4@tela` | não | sim | 69 | 49 | 39,5 | 69,0 | 0,053 | 0,014 | gen_ai, hash, ollama, prov.used | nenhum | 390 | 1088 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `sin-5@fixture` | não | sim | 46 | 53 | 38,9 | 63,2 | 0,016 | 0,009 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 301 | 972 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `sin-5@tela` | não | sim | 60 | 52 | 38,7 | 67,0 | 0,016 | 0,011 | gen_ai, hash, ollama, prov.used | nenhum | 359 | 1091 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `tra-11@fixture` | não | sim | 57 | 49 | 34,2 | 61,8 | 0,061 | 0,006 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 303 | 929 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `tra-11@tela` | não | sim | 60 | 49 | 35,0 | 64,8 | 0,021 | 0,006 | gen_ai, hash, ollama, prov.used | nenhum | 390 | 1079 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `tra-17@fixture` | não | sim | 47 | 49 | 39,0 | 63,8 | 0,025 | 0,009 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 281 | 939 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `tra-17@tela` | não | sim | 68 | 49 | 41,5 | 68,4 | 0,039 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 379 | 1074 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `tra-19@fixture` | não | sim | 51 | 49 | 36,3 | 61,5 | 0,015 | 0,008 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 314 | 963 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `tra-19@tela` | não | sim | 72 | 49 | 38,9 | 65,8 | 0,044 | 0,015 | gen_ai, hash, ollama, prov.used | nenhum | 387 | 1076 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `tra-1@fixture` | não | sim | 53 | 49 | 38,1 | 62,4 | 0,046 | 0,009 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 305 | 933 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `tra-1@tela` | não | sim | 72 | 49 | 38,9 | 65,8 | 0,044 | 0,015 | gen_ai, hash, ollama, prov.used | nenhum | 387 | 1076 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `tra-20@fixture` | não | sim | 53 | 52 | 42,2 | 63,1 | 0,063 | 0,016 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 295 | 953 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `tra-20@tela` | não | sim | 68 | 51 | 41,5 | 67,0 | 0,039 | 0,011 | gen_ai, hash, ollama, prov.used | nenhum | 379 | 1090 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `tra-21@fixture` | não | sim | 47 | 52 | 33,2 | 61,3 | 0,025 | 0,013 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 283 | 953 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `tra-21@tela` | não | sim | 65 | 55 | 36,9 | 64,2 | 0,013 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 439 | 1136 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `tra-4@fixture` | não | sim | 51 | 52 | 29,7 | 61,3 | 0,044 | 0,012 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 291 | 949 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `tra-4@tela` | não | sim | 65 | 55 | 36,9 | 64,2 | 0,013 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 439 | 1136 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `tra-8@fixture` | não | sim | 51 | 49 | 29,7 | 62,8 | 0,044 | 0,006 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 291 | 933 |
| corrida 18d (o mesmo caso lido da tela e do caso escrito) | `tra-8@tela` | não | sim | 65 | 49 | 36,9 | 65,5 | 0,013 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 439 | 1120 |
| corrida 21d (ensaio dos cenários da Fase 5) | `contrato-error_500__r1` | não | sim | 68 | 51 | 39,5 | 67,1 | 0,040 | 0,011 | gen_ai, hash, ollama, prov.used | nenhum | 373 | 1092 |
| corrida 21d (ensaio dos cenários da Fase 5) | `contrato-escala_ou_unidade_errada__r1` | não | sim | 72 | 49 | 38,9 | 65,9 | 0,044 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 387 | 1084 |
| corrida 21d (ensaio dos cenários da Fase 5) | `contrato-field_missing__r1` | não | sim | 65 | 49 | 37,2 | 67,8 | 0,019 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 366 | 1116 |
| corrida 21d (ensaio dos cenários da Fase 5) | `contrato-field_renamed__r1` | não | sim | 62 | 49 | 39,7 | 67,3 | 0,019 | 0,013 | gen_ai, hash, ollama, prov.used | nenhum | 359 | 1101 |
| corrida 21d (ensaio dos cenários da Fase 5) | `contrato-malformed_json__r1` | não | sim | 62 | 49 | 39,0 | 67,2 | 0,016 | 0,012 | gen_ai, hash, ollama, prov.used | nenhum | 358 | 1075 |
| corrida 21d (ensaio dos cenários da Fase 5) | `contrato-type_drift__r1` | não | sim | 65 | 49 | 35,9 | 66,8 | 0,016 | 0,011 | gen_ai, hash, ollama, prov.used | nenhum | 360 | 1096 |
| corrida 21d (ensaio dos cenários da Fase 5) | `localizador-front-admin-login__r1` | não | sim | 57 | 49 | 31,3 | 60,8 | 0,058 | 0,021 | gen_ai, hash, ollama, prov.used | nenhum | 432 | 1122 |
| corrida 21d (ensaio dos cenários da Fase 5) | `localizador-front-admin-produtos__r1` | não | sim | 63 | 49 | 34,1 | 62,2 | 0,066 | 0,026 | gen_ai, hash, ollama, prov.used | nenhum | 460 | 1161 |
| corrida 21d (ensaio dos cenários da Fase 5) | `localizador-front-busca__r1` | não | sim | 57 | 49 | 30,5 | 59,1 | 0,057 | 0,022 | gen_ai, hash, ollama, prov.used | nenhum | 438 | 1108 |
| corrida 21d (ensaio dos cenários da Fase 5) | `localizador-front-cliente-reserva__r1` | não | sim | 59 | 49 | 36,9 | 62,0 | 0,046 | 0,024 | gen_ai, hash, ollama, prov.used | nenhum | 443 | 1137 |
| corrida 24 (os 36 inéditos em texto) | `efe-22` | não | sim | 47 | 49 | 33,3 | 63,4 | 0,026 | 0,010 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 272 | 912 |
| corrida 24 (os 36 inéditos em texto) | `efe-23` | não | sim | 47 | 49 | 33,3 | 63,4 | 0,026 | 0,010 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 272 | 912 |
| corrida 24 (os 36 inéditos em texto) | `efe-24` | não | sim | 47 | 49 | 30,4 | 62,2 | 0,025 | 0,010 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 280 | 908 |
| corrida 24 (os 36 inéditos em texto) | `efe-25` | não | sim | 47 | 49 | 32,7 | 62,1 | 0,034 | 0,010 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 276 | 918 |
| corrida 24 (os 36 inéditos em texto) | `efe-26` | não | sim | 61 | 53 | 39,9 | 63,0 | 0,059 | 0,022 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 313 | 975 |
| corrida 24 (os 36 inéditos em texto) | `efe-27` | não | sim | 57 | 53 | 34,2 | 60,5 | 0,037 | 0,015 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 340 | 988 |
| corrida 24 (os 36 inéditos em texto) | `lex-22` | não | sim | 55 | 49 | 47,3 | 66,7 | 0,073 | 0,011 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 290 | 915 |
| corrida 24 (os 36 inéditos em texto) | `lex-23` | não | sim | 55 | 49 | 51,3 | 65,9 | 0,053 | 0,010 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 288 | 900 |
| corrida 24 (os 36 inéditos em texto) | `lex-24` | não | sim | 60 | 49 | 33,6 | 61,4 | 0,023 | 0,010 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 353 | 949 |
| corrida 24 (os 36 inéditos em texto) | `lex-25` | não | sim | 56 | 49 | 32,6 | 61,4 | 0,038 | 0,010 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 335 | 945 |
| corrida 24 (os 36 inéditos em texto) | `lex-26` | não | sim | 57 | 52 | 33,5 | 61,1 | 0,041 | 0,009 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 336 | 970 |
| corrida 24 (os 36 inéditos em texto) | `lex-27` | não | sim | 55 | 52 | 37,4 | 61,6 | 0,042 | 0,009 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 357 | 974 |
| corrida 24 (os 36 inéditos em texto) | `run-22` | não | sim | 56 | 49 | 36,1 | 63,4 | 0,033 | 0,010 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 314 | 928 |
| corrida 24 (os 36 inéditos em texto) | `run-23` | não | sim | 47 | 49 | 29,6 | 63,9 | 0,025 | 0,010 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 282 | 920 |
| corrida 24 (os 36 inéditos em texto) | `run-24` | não | sim | 60 | 49 | 32,3 | 60,6 | 0,023 | 0,009 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 347 | 964 |
| corrida 24 (os 36 inéditos em texto) | `run-25` | não | sim | 49 | 49 | 36,1 | 62,2 | 0,053 | 0,009 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 329 | 960 |
| corrida 24 (os 36 inéditos em texto) | `run-26` | não | sim | 55 | 55 | 38,7 | 61,6 | 0,045 | 0,008 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 358 | 978 |
| corrida 24 (os 36 inéditos em texto) | `run-27` | não | sim | 52 | 55 | 34,8 | 61,7 | 0,025 | 0,010 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 284 | 935 |
| corrida 24 (os 36 inéditos em texto) | `semt-22` | não | sim | 47 | 49 | 35,8 | 64,2 | 0,026 | 0,009 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 276 | 898 |
| corrida 24 (os 36 inéditos em texto) | `semt-23` | não | sim | 51 | 49 | 36,1 | 63,7 | 0,025 | 0,009 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 285 | 924 |
| corrida 24 (os 36 inéditos em texto) | `semt-24` | não | sim | 47 | 49 | 38,4 | 63,5 | 0,026 | 0,009 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 276 | 894 |
| corrida 24 (os 36 inéditos em texto) | `semt-25` | não | sim | 53 | 49 | 39,6 | 63,5 | 0,064 | 0,009 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 291 | 910 |
| corrida 24 (os 36 inéditos em texto) | `semt-26` | não | sim | 47 | 54 | 35,8 | 62,3 | 0,026 | 0,010 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 276 | 929 |
| corrida 24 (os 36 inéditos em texto) | `semt-27` | não | sim | 48 | 54 | 35,9 | 62,7 | 0,019 | 0,011 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 305 | 952 |
| corrida 24 (os 36 inéditos em texto) | `sin-22` | não | sim | 47 | 49 | 41,0 | 65,0 | 0,025 | 0,009 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 282 | 904 |
| corrida 24 (os 36 inéditos em texto) | `sin-23` | não | sim | 47 | 49 | 35,5 | 64,3 | 0,026 | 0,009 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 276 | 894 |
| corrida 24 (os 36 inéditos em texto) | `sin-24` | não | sim | 53 | 49 | 30,4 | 61,3 | 0,027 | 0,009 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 307 | 927 |
| corrida 24 (os 36 inéditos em texto) | `sin-25` | não | sim | 56 | 49 | 41,7 | 64,4 | 0,082 | 0,009 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 297 | 914 |
| corrida 24 (os 36 inéditos em texto) | `sin-26` | não | sim | 57 | 52 | 39,8 | 61,6 | 0,038 | 0,008 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 336 | 974 |
| corrida 24 (os 36 inéditos em texto) | `sin-27` | não | sim | 50 | 52 | 40,1 | 62,7 | 0,026 | 0,010 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 309 | 937 |
| corrida 24 (os 36 inéditos em texto) | `tra-22` | não | sim | 51 | 49 | 34,9 | 62,6 | 0,015 | 0,010 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 305 | 931 |
| corrida 24 (os 36 inéditos em texto) | `tra-23` | não | sim | 58 | 49 | 40,7 | 63,8 | 0,044 | 0,010 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 316 | 935 |
| corrida 24 (os 36 inéditos em texto) | `tra-24` | não | sim | 53 | 49 | 40,8 | 63,2 | 0,065 | 0,010 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 290 | 911 |
| corrida 24 (os 36 inéditos em texto) | `tra-25` | não | sim | 57 | 49 | 37,2 | 60,5 | 0,041 | 0,010 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 342 | 940 |
| corrida 24 (os 36 inéditos em texto) | `tra-26` | não | sim | 44 | 51 | 36,2 | 62,7 | 0,021 | 0,010 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 277 | 941 |
| corrida 24 (os 36 inéditos em texto) | `tra-27` | não | sim | 49 | 51 | 30,9 | 61,5 | 0,020 | 0,010 | gen_ai, hash, ollama, prompt, prov.used | nenhum | 287 | 943 |
| verbetes da biblioteca de produção e a camada de leitura | `ancora-saiba-mais` | sim | sim | 36 | 36 | 83,8 | 56,1 | 0,000 | 0,000 | nenhum | nenhum | 72 | 211 |
| verbetes da biblioteca de produção e a camada de leitura | `atualizacao-da-tela` | sim | sim | 22 | 39 | 19,5 | 46,2 | 0,000 | 0,000 | nenhum | nenhum | 27 | 220 |
| verbetes da biblioteca de produção e a camada de leitura | `campo_ausente` | não | sim | 22 | 28 | 48,9 | 52,1 | 0,038 | 0,000 | nenhum | nenhum | 95 | 227 |
| verbetes da biblioteca de produção e a camada de leitura | `campo_preco_ausente` | sim | sim | 17 | 36 | 50,9 | 58,7 | 0,000 | 0,000 | nenhum | nenhum | 25 | 241 |
| verbetes da biblioteca de produção e a camada de leitura | `campo_renomeado` | não | sim | 62 | 32 | 42,2 | 60,0 | 0,130 | 0,008 | nenhum | nenhum | 127 | 299 |
| verbetes da biblioteca de produção e a camada de leitura | `chave_de_juncao_errada` | não | sim | 37 | 32 | 60,0 | 66,9 | 0,142 | 0,019 | nenhum | nenhum | 189 | 300 |
| verbetes da biblioteca de produção e a camada de leitura | `codificacao_incorreta` | sim | sim | 23 | 32 | 56,8 | 58,2 | 0,000 | 0,000 | nenhum | nenhum | 64 | 218 |
| verbetes da biblioteca de produção e a camada de leitura | `colecao_no_lugar_de_objeto` | não | sim | 41 | 29 | 52,3 | 59,2 | 0,199 | 0,008 | frontend | nenhum | 162 | 278 |
| verbetes da biblioteca de produção e a camada de leitura | `consultas-sem-checagem` | sim | sim | 24 | 29 | 59,7 | 48,2 | 0,000 | 0,000 | nenhum | nenhum | 67 | 205 |
| verbetes da biblioteca de produção e a camada de leitura | `contagem_inconsistente` | não | sim | 29 | 32 | 51,7 | 59,8 | 0,047 | 0,015 | nenhum | nenhum | 120 | 308 |
| verbetes da biblioteca de produção e a camada de leitura | `contrato-pedido` | não | sim | 30 | 29 | 47,5 | 59,5 | 0,049 | 0,012 | nenhum | nenhum | 118 | 286 |
| verbetes da biblioteca de produção e a camada de leitura | `contrato-produto` | não | sim | 23 | 33 | 54,1 | 57,8 | 0,021 | 0,004 | schema | nenhum | 111 | 307 |
| verbetes da biblioteca de produção e a camada de leitura | `corpo_nao_e_json` | não | sim | 40 | 33 | 63,7 | 65,4 | 0,037 | 0,014 | token | nenhum | 178 | 330 |
| verbetes da biblioteca de produção e a camada de leitura | `corpo_vazio` | não | sim | 49 | 32 | 36,9 | 60,1 | 0,014 | 0,000 | nenhum | nenhum | 161 | 285 |
| verbetes da biblioteca de produção e a camada de leitura | `dado_desatualizado` | sim | sim | 28 | 34 | 56,5 | 52,1 | 0,000 | 0,000 | nenhum | nenhum | 73 | 230 |
| verbetes da biblioteca de produção e a camada de leitura | `entidade-produto` | não | sim | 20 | 31 | 42,9 | 57,9 | 0,024 | 0,000 | backend, enum, frontend | nenhum | 97 | 238 |
| verbetes da biblioteca de produção e a camada de leitura | `erro_interno_do_servidor` | não | sim | 39 | 32 | 54,5 | 65,8 | 0,151 | 0,000 | nenhum | nenhum | 185 | 310 |
| verbetes da biblioteca de produção e a camada de leitura | `escala_ou_unidade_errada` | não | sim | 44 | 35 | 39,0 | 57,8 | 0,253 | 0,015 | nenhum | nenhum | 160 | 303 |
| verbetes da biblioteca de produção e a camada de leitura | `estado_da_tela_divergente` | não | sim | 28 | 34 | 49,6 | 55,0 | 0,042 | 0,000 | nenhum | nenhum | 108 | 297 |
| verbetes da biblioteca de produção e a camada de leitura | `estrutura_aninhada_divergente` | não | sim | 31 | 29 | 41,8 | 54,7 | 0,165 | 0,000 | nenhum | nenhum | 115 | 298 |
| verbetes da biblioteca de produção e a camada de leitura | `fluxo-reserva-e-cancelamento` | não | sim | 25 | 31 | 68,3 | 61,2 | 0,035 | 0,012 | nenhum | nenhum | 65 | 200 |
| verbetes da biblioteca de produção e a camada de leitura | `formato_de_data_divergente` | sim | sim | 17 | 28 | 49,1 | 54,0 | 0,000 | 0,011 | nenhum | nenhum | 65 | 213 |
| verbetes da biblioteca de produção e a camada de leitura | `limite_de_requisicoes` | não | sim | 43 | 30 | 42,5 | 56,3 | 0,183 | 0,000 | nenhum | nenhum | 134 | 295 |
| verbetes da biblioteca de produção e a camada de leitura | `limites-do-sistema` | não | sim | 33 | 42 | 65,4 | 61,7 | 0,000 | 0,000 | hash | nenhum | 74 | 261 |
| verbetes da biblioteca de produção e a camada de leitura | `localizador_quebrado` | sim | sim | 23 | 29 | 43,5 | 57,2 | 0,031 | 0,015 | nenhum | nenhum | 146 | 305 |
| verbetes da biblioteca de produção e a camada de leitura | `mensagens-de-erro-do-codigo` | não | sim | 26 | 36 | 46,8 | 53,3 | 0,019 | 0,008 | token | nenhum | 59 | 299 |
| verbetes da biblioteca de produção e a camada de leitura | `modos-de-injecao` | não | sim | 27 | 34 | 59,6 | 53,0 | 0,000 | 0,000 | token | nenhum | 63 | 277 |
| verbetes da biblioteca de produção e a camada de leitura | `novo_verbete` | sim | sim | 19 | 35 | 47,5 | 50,2 | 0,000 | 0,000 | nenhum | nenhum | 25 | 250 |
| verbetes da biblioteca de produção e a camada de leitura | `nulo_inesperado` | sim | sim | 19 | 32 | 70,4 | 65,6 | 0,000 | 0,000 | nenhum | nenhum | 69 | 230 |
| verbetes da biblioteca de produção e a camada de leitura | `pagina-produtos-api` | sim | sim | 25 | 26 | 58,9 | 48,3 | 0,000 | 0,000 | nenhum | nenhum | 59 | 197 |
| verbetes da biblioteca de produção e a camada de leitura | `pedido-reserva` | sim | sim | 26 | 32 | 52,1 | 53,3 | 0,000 | 0,000 | nenhum | nenhum | 66 | 200 |
| verbetes da biblioteca de produção e a camada de leitura | `recurso_inexistente` | não | sim | 31 | 31 | 67,7 | 63,0 | 0,049 | 0,024 | token | nenhum | 117 | 334 |
| verbetes da biblioteca de produção e a camada de leitura | `registro_duplicado` | sim | sim | 20 | 32 | 57,5 | 57,8 | 0,000 | 0,000 | nenhum | nenhum | 62 | 213 |
| verbetes da biblioteca de produção e a camada de leitura | `resposta_truncada` | não | sim | 33 | 28 | 43,6 | 61,3 | 0,096 | 0,000 | nenhum | nenhum | 154 | 298 |
| verbetes da biblioteca de produção e a camada de leitura | `senha-sem-hash` | não | sim | 22 | 31 | 63,8 | 56,8 | 0,018 | 0,004 | hash | nenhum | 65 | 267 |
| verbetes da biblioteca de produção e a camada de leitura | `tempo_de_resposta_excedido` | sim | sim | 27 | 33 | 76,0 | 64,8 | 0,000 | 0,005 | nenhum | nenhum | 74 | 233 |
| verbetes da biblioteca de produção e a camada de leitura | `tipo_divergente` | não | sim | 30 | 28 | 56,2 | 62,4 | 0,078 | 0,015 | nenhum | nenhum | 130 | 314 |
| verbetes da biblioteca de produção e a camada de leitura | `usuario-e-login` | não | sim | 24 | 30 | 75,2 | 60,5 | 0,000 | 0,000 | nenhum | nenhum | 73 | 199 |
| verbetes da biblioteca de produção e a camada de leitura | `valor_fora_do_dominio` | não | sim | 29 | 41 | 53,0 | 63,0 | 0,056 | 0,014 | enum | nenhum | 120 | 335 |
<!-- /tabela:tb_f4_texto_casos -->
