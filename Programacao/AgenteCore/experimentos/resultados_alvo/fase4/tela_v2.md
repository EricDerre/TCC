<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase4.py a partir de os registros da tela e do fixture, tela.jsonl e a trilha da corrida 18 (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Diagnóstico ao vivo e o mesmo caso do fixture (corrida 18), gerada em 2026-11-01

Regra R2 do plano aprovado: nos casos que reproduzem, o rótulo dado ao caso lido da tela e o rótulo dado ao caso lido do fixture, na mesma sessão do Ollama, diferem em no máximo 3 casos (a variação entre corridas iguais); acima disso, o molde do sintoma e a poda são revistos antes da próxima noite. O gabarito entra só nesta leitura, nunca no agente. Prompt contra a calibração (seção 3.3 do plano): maior prompt da tela 2034 tokens, limite de 1409 (10% acima do maior da calibração, 1281); casos acima: `lex-1`, `lex-4`, `sin-4`, `sin-5`, `semt-1`, `tra-1`, `tra-4`, `run-1`, `run-2`, `efe-3`, `lex-7`, `lex-8`, `lex-10`, `lex-11`, `sin-11`, `sin-14`, `semt-8`, `semt-9`, `semt-14`, `tra-8`, `tra-11`, `run-9`, `lex-16`, `lex-18`, `sin-16`, `sin-20`, `sin-21`, `semt-16`, `semt-17`, `semt-20`, `semt-21`, `tra-17`, `tra-19`, `tra-20`, `tra-21`, `run-19`, `run-21`.


<!-- tabela:tb_f4_tela_resumo -->
| Casos | Reproduzem na tela | Acerto na tela | Acerto no fixture | Concordam (mesmo rótulo) | Concordância (%) | b (só a tela acerta) | c (só o fixture acerta) | b + c | Limite R2 | Dentro do limite | p (McNemar exato) | Selos na tela (alto / médio / baixo) | Gatilhos na tela | Divergências na tela | s por caso na tela (mediana) | s por caso no fixture (mediana) | Trilha (bytes) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 37 | 37 | 26 (70,3%) | 31 (83,8%) | 26 | 70,3 | 2 | 7 | 9 | 3 | não | 0,2 | 11 / 18 / 8 | 15 | 9 | 82,5 | 51,5 | 2200836 |
<!-- /tabela:tb_f4_tela_resumo -->

<!-- tabela:tb_f4_tela_por_classe -->
| Classe | Casos | Acerto na tela | Acerto no fixture | Concordam |
|---|---|---|---|---|
| 1 | 8 | 6 | 7 | 6 |
| 2 | 7 | 5 | 5 | 3 |
| 3 | 8 | 4 | 6 | 5 |
| 4 | 8 | 6 | 7 | 7 |
| 5 | 5 | 4 | 5 | 4 |
| 6 | 1 | 1 | 1 | 1 |
<!-- /tabela:tb_f4_tela_por_classe -->

<!-- tabela:tb_f4_tela_rotulos -->
| Rótulo | Dado na tela | Dado no fixture | É o gabarito de |
|---|---|---|---|
| `tipo_divergente` | 8 | 4 | 2 |
| `campo_ausente` | 5 | 4 | 4 |
| `contagem_inconsistente` | 4 | 4 | 4 |
| `codificacao_incorreta` | 2 | 3 | 4 |
| `resposta_truncada` | 3 | 3 | 3 |
| `nulo_inesperado` | 2 | 3 | 3 |
| `tempo_de_resposta_excedido` | 2 | 3 | 3 |
| `colecao_no_lugar_de_objeto` | 2 | 3 | 1 |
| `escala_ou_unidade_errada` | 2 | 2 | 2 |
| `valor_fora_do_dominio` | 0 | 2 | 3 |
| `estrutura_aninhada_divergente` | 0 | 2 | 2 |
| `campo_renomeado` | 2 | 0 | 1 |
| `chave_de_juncao_errada` | 0 | 1 | 2 |
| `corpo_vazio` | 1 | 1 | 1 |
| `erro_interno_do_servidor` | 1 | 1 | 1 |
| `registro_duplicado` | 1 | 1 | 1 |
| `formato_de_data_divergente` | 2 | 0 | 0 |
<!-- /tabela:tb_f4_tela_rotulos -->

<!-- tabela:tb_f4_tela_corpo -->
| Casos com o caso ao vivo lido | Sem diferença contra o contrato | Desses, mesmo rótulo | Desses, acerto na tela | Desses, colecao_no_lugar_de_objeto na tela | Com diferença contra o contrato | Desses, mesmo rótulo | Desses, acerto na tela | Sintoma "Nenhuma diferença medida" |
|---|---|---|---|---|---|---|---|---|
| 37 | 22 | 16 | 15 | 1 | 15 | 10 | 11 | 0 |
<!-- /tabela:tb_f4_tela_corpo -->

<!-- tabela:tb_f4_tela_casos -->
| Caso | Classe | Gabarito | Rótulo na tela | Rótulo no fixture | Tela | Fixture | Concordam | p tela | Selo tela | p fixture | Selo fixture | Gatilho | Divergência | s tela | s fixture | Diferenças contra o contrato | CORPO do caso ao vivo (começo) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `lex-1` | 1 | `resposta_truncada` | `resposta_truncada` | `resposta_truncada` | certo | certo | sim | 0,9 | medio | 1,0 | alto | não | não | 95,5 | 58,4 | 0 | `...[{"id": 1, "nome": "resposta truncada de propos` |
| `lex-4` | 1 | `codificacao_incorreta` | `codificacao_incorreta` | `codificacao_incorreta` | certo | certo | sim | 0,9 | medio | 1,0 | alto | sim | sim | 86,8 | 40,0 | 0 | `lista com 14 itens (referência em modo normal: 14); nome dif` |
| `sin-4` | 2 | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | certo | certo | sim | 1,0 | alto | 0,9 | medio | não | não | 81,3 | 58,1 | 1 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `sin-5` | 2 | `campo_ausente` | `campo_ausente` | `colecao_no_lugar_de_objeto` | certo | errado | não | 1,0 | medio | 0,8 | baixo | não | não | 88,8 | 49,3 | 1 | `{"resumo": "(ausente)"}` |
| `semt-1` | 3 | `tipo_divergente` | `tipo_divergente` | `tipo_divergente` | certo | certo | sim | 1,0 | alto | 0,8 | baixo | não | não | 90,5 | 64,6 | 1 | `{"preco": "89.9"}` |
| `tra-1` | 4 | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | certo | certo | sim | 0,8 | baixo | 1,0 | alto | sim | não | 97,3 | 62,8 | 0 | `lista com 14 itens (referência em modo normal: 14); preco di` |
| `tra-4` | 4 | `contagem_inconsistente` | `contagem_inconsistente` | `contagem_inconsistente` | certo | certo | sim | 1,0 | alto | 1,0 | medio | não | não | 100,9 | 54,6 | 0 | `lista com 13 itens (referência em modo normal: 14); falta o ` |
| `run-1` | 5 | `erro_interno_do_servidor` | `erro_interno_do_servidor` | `erro_interno_do_servidor` | certo | certo | sim | 1,0 | medio | 1,0 | medio | sim | sim | 100,4 | 62,9 | 9 | `{"detail": "fault injection: error_500 em produto", "id": "(` |
| `run-2` | 5 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | certo | certo | sim | 1,0 | medio | 1,0 | alto | sim | sim | 66,1 | 57,3 | 0 | `lista com 14 itens, igual à referência em modo normal; prime` |
| `efe-3` | 6 | `campo_ausente` | `campo_ausente` | `campo_ausente` | certo | certo | sim | 1,0 | alto | 0,6 | baixo | não | não | 64,2 | 31,0 | 1 | `{"imagem": "(ausente)"}` |
| `lex-7` | 1 | `corpo_vazio` | `corpo_vazio` | `corpo_vazio` | certo | certo | sim | 1,0 | medio | 1,0 | alto | não | não | 89,4 | 52,5 | 0 | n/d |
| `lex-8` | 1 | `codificacao_incorreta` | `formato_de_data_divergente` | `codificacao_incorreta` | errado | certo | não | 0,2 | baixo | 0,7 | baixo | sim | sim | 78,9 | 65,0 | 0 | `lista com 14 itens (referência em modo normal: 14); resumo d` |
| `lex-10` | 1 | `resposta_truncada` | `resposta_truncada` | `resposta_truncada` | certo | certo | sim | 0,9 | medio | 1,0 | alto | não | não | 20,2 | 51,5 | 0 | `...[{"id": 1, "nome": "resposta truncada de propos` |
| `lex-11` | 1 | `codificacao_incorreta` | `codificacao_incorreta` | `codificacao_incorreta` | certo | certo | sim | 0,9 | medio | 1,0 | alto | sim | sim | 82,5 | 56,4 | 0 | `lista com 14 itens (referência em modo normal: 14); nome dif` |
| `sin-11` | 2 | `estrutura_aninhada_divergente` | `tipo_divergente` | `estrutura_aninhada_divergente` | errado | certo | não | 0,7 | baixo | 1,0 | alto | sim | não | 96,7 | 68,3 | 1 | `{"preco": {"valor": 89.9, "moeda": "BRL"}}` |
| `sin-14` | 2 | `campo_renomeado` | `campo_renomeado` | `colecao_no_lugar_de_objeto` | certo | errado | não | 1,0 | alto | 0,3 | baixo | sim | sim | 90,5 | 51,1 | 1 | `{"imagem_v2": "picanha_alho.jpg"}` |
| `semt-8` | 3 | `nulo_inesperado` | `nulo_inesperado` | `nulo_inesperado` | certo | certo | sim | 1,0 | medio | 0,9 | medio | não | não | 92,1 | 62,3 | 1 | `{"preco": null}` |
| `semt-9` | 3 | `valor_fora_do_dominio` | `tipo_divergente` | `tipo_divergente` | errado | errado | sim | 1,0 | alto | 1,0 | alto | não | não | 96,5 | 48,1 | 1 | `{"destaque": "talvez"}` |
| `semt-14` | 3 | `nulo_inesperado` | `nulo_inesperado` | `nulo_inesperado` | certo | certo | sim | 1,0 | medio | 0,7 | baixo | não | não | 62,6 | 48,9 | 1 | `{"tipo": null}` |
| `tra-8` | 4 | `contagem_inconsistente` | `contagem_inconsistente` | `contagem_inconsistente` | certo | certo | sim | 1,0 | medio | 0,9 | medio | não | não | 31,7 | 34,3 | 0 | `lista com 13 itens (referência em modo normal: 14); falta o ` |
| `tra-11` | 4 | `contagem_inconsistente` | `contagem_inconsistente` | `contagem_inconsistente` | certo | certo | sim | 1,0 | alto | 1,0 | medio | não | não | 75,3 | 33,6 | 0 | `lista com 13 itens (referência em modo normal: 14); falta o ` |
| `run-9` | 5 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | certo | certo | sim | 1,0 | medio | 1,0 | alto | sim | sim | 67,9 | 51,1 | 0 | `lista com 14 itens, igual à referência em modo normal; prime` |
| `lex-16` | 1 | `resposta_truncada` | `resposta_truncada` | `resposta_truncada` | certo | certo | sim | 1,0 | medio | 1,0 | alto | não | não | 94,1 | 64,9 | 0 | `...[{"id": 1, "nome": "resposta truncada de propos` |
| `lex-18` | 1 | `codificacao_incorreta` | `formato_de_data_divergente` | `valor_fora_do_dominio` | errado | errado | não | 0,2 | baixo | 0,5 | baixo | sim | sim | 82,0 | 67,7 | 0 | `lista com 14 itens (referência em modo normal: 14); resumo d` |
| `sin-16` | 2 | `campo_ausente` | `campo_ausente` | `campo_ausente` | certo | certo | sim | 1,0 | alto | 1,0 | alto | não | não | 99,0 | 48,5 | 1 | `{"destaque": "(ausente)"}` |
| `sin-20` | 2 | `campo_ausente` | `campo_ausente` | `campo_ausente` | certo | certo | sim | 1,0 | alto | 1,0 | alto | não | não | 60,6 | 42,1 | 1 | `{"id": "(ausente)"}` |
| `sin-21` | 2 | `estrutura_aninhada_divergente` | `tipo_divergente` | `estrutura_aninhada_divergente` | errado | certo | não | 1,0 | medio | 1,0 | alto | não | não | 104,6 | 72,7 | 1 | `{"tipo": {"valor": "Carnes", "moeda": "BRL"}}` |
| `semt-16` | 3 | `tipo_divergente` | `tipo_divergente` | `tipo_divergente` | certo | certo | sim | 1,0 | medio | 0,9 | medio | não | não | 65,8 | 46,4 | 1 | `{"tipo": 1}` |
| `semt-17` | 3 | `nulo_inesperado` | `campo_ausente` | `nulo_inesperado` | errado | certo | não | 0,4 | baixo | 0,9 | medio | sim | não | 90,2 | 54,9 | 1 | `{"id": null}` |
| `semt-20` | 3 | `valor_fora_do_dominio` | `tipo_divergente` | `valor_fora_do_dominio` | errado | certo | não | 0,6 | baixo | 0,5 | baixo | sim | não | 78,9 | 34,1 | 0 | `lista com 14 itens (referência em modo normal: 14); preco di` |
| `semt-21` | 3 | `valor_fora_do_dominio` | `campo_renomeado` | `campo_ausente` | errado | errado | não | 1,0 | alto | 1,0 | medio | não | não | 102,5 | 44,7 | 0 | `lista com 14 itens (referência em modo normal: 14); nome dif` |
| `tra-17` | 4 | `chave_de_juncao_errada` | `tipo_divergente` | `tipo_divergente` | errado | errado | sim | 1,0 | medio | 1,0 | medio | não | não | 70,9 | 33,9 | 0 | `lista com 14 itens (referência em modo normal: 14); tipo dif` |
| `tra-19` | 4 | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | certo | certo | sim | 0,8 | baixo | 0,6 | baixo | sim | não | 78,2 | 39,5 | 0 | `lista com 14 itens (referência em modo normal: 14); preco di` |
| `tra-20` | 4 | `chave_de_juncao_errada` | `tipo_divergente` | `chave_de_juncao_errada` | errado | certo | não | 1,0 | medio | 1,0 | alto | não | não | 33,1 | 63,8 | 0 | `lista com 14 itens (referência em modo normal: 14); tipo dif` |
| `tra-21` | 4 | `contagem_inconsistente` | `contagem_inconsistente` | `contagem_inconsistente` | certo | certo | sim | 1,0 | medio | 1,0 | medio | não | não | 92,4 | 41,4 | 0 | `lista com 13 itens (referência em modo normal: 14); falta o ` |
| `run-19` | 5 | `tempo_de_resposta_excedido` | `colecao_no_lugar_de_objeto` | `tempo_de_resposta_excedido` | errado | certo | não | 0,4 | baixo | 1,0 | alto | sim | não | 77,6 | 63,1 | 0 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `run-21` | 5 | `registro_duplicado` | `registro_duplicado` | `registro_duplicado` | certo | certo | sim | 1,0 | alto | 0,7 | baixo | sim | sim | 72,1 | 42,7 | 0 | `lista com 15 itens (referência em modo normal: 14); o id 1 (` |
<!-- /tabela:tb_f4_tela_casos -->
