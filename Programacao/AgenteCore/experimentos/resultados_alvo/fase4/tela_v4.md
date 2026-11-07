<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase4.py a partir de os registros da tela e do fixture, tela.jsonl e a trilha da corrida 18 (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# A tela com os sinais novos da busca (corrida 18d), gerada em 2026-11-06

Regra R2 do plano aprovado (a tela não piora): nos casos que reproduzem, o caso lido da tela e o mesmo caso lido do fixture, na mesma sessão do Ollama, não se afastam mais que a variação entre corridas iguais, 3 casos. Desde 06/11/2026 (decisão 98, antes da corrida 18d) o limite vale para os casos que a tela perde para o fixture (c); os que só a tela acerta (b) e a soma b + c, a conta usada até a corrida 18c, ficam ao lado. O gabarito entra só nesta leitura, nunca no agente. Prompt contra a calibração (seção 3.3 do plano): maior prompt da tela 1385 tokens, limite de 1409 (10% acima do maior da calibração, 1281); casos acima: nenhum.


<!-- tabela:tb_f4_tela_resumo -->
| Casos | Reproduzem na tela | Acerto na tela | Acerto no fixture | Concordam (mesmo rótulo) | Concordância (%) | b (só a tela acerta) | c (só o fixture acerta) | b + c | Limite R2 (c) | Dentro do limite | b + c até o limite (conta de antes) | p (McNemar exato) | Selos na tela (alto / médio / baixo) | Gatilhos na tela | Divergências na tela | s por caso na tela (mediana) | s por caso no fixture (mediana) | Trilha (bytes) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 37 | 37 | 32 (86,5%) | 30 (81,1%) | 28 | 75,7 | 5 | 3 | 8 | 3 | sim | não | 0,727 | 20 / 12 / 5 | 6 | 5 | 59,2 | 58,0 | 2051641 |
<!-- /tabela:tb_f4_tela_resumo -->

<!-- tabela:tb_f4_tela_por_classe -->
| Classe | Casos | Acerto na tela | Acerto no fixture | Concordam |
|---|---|---|---|---|
| 1 | 8 | 8 | 7 | 7 |
| 2 | 7 | 7 | 5 | 5 |
| 3 | 8 | 6 | 5 | 6 |
| 4 | 8 | 5 | 7 | 4 |
| 5 | 5 | 5 | 5 | 5 |
| 6 | 1 | 1 | 1 | 1 |
<!-- /tabela:tb_f4_tela_por_classe -->

<!-- tabela:tb_f4_tela_verbete -->
| Lado | Verbete da causa certa entre os entregues | Casos | Acertos | Acerto (%) |
|---|---|---|---|---|
| tela | sim | 36 | 32 | 88,9 |
| tela | não | 1 | 0 | 0,0 |
| fixture | sim | 27 | 26 | 96,3 |
| fixture | não | 10 | 4 | 40,0 |
<!-- /tabela:tb_f4_tela_verbete -->

<!-- tabela:tb_f4_tela_selo -->
| Selo na tela | Casos | Acertos | Acerto (%) |
|---|---|---|---|
| alto | 20 | 18 | 90,0 |
| medio | 12 | 12 | 100,0 |
| baixo | 5 | 2 | 40,0 |
<!-- /tabela:tb_f4_tela_selo -->

<!-- tabela:tb_f4_tela_rotulos -->
| Rótulo | Dado na tela | Dado no fixture | É o gabarito de |
|---|---|---|---|
| `campo_ausente` | 4 | 4 | 4 |
| `resposta_truncada` | 6 | 3 | 3 |
| `codificacao_incorreta` | 4 | 3 | 4 |
| `tipo_divergente` | 3 | 5 | 2 |
| `contagem_inconsistente` | 1 | 4 | 4 |
| `nulo_inesperado` | 3 | 3 | 3 |
| `tempo_de_resposta_excedido` | 3 | 3 | 3 |
| `escala_ou_unidade_errada` | 2 | 2 | 2 |
| `estrutura_aninhada_divergente` | 2 | 2 | 2 |
| `chave_de_juncao_errada` | 2 | 1 | 2 |
| `colecao_no_lugar_de_objeto` | 1 | 3 | 1 |
| `valor_fora_do_dominio` | 1 | 1 | 3 |
| `campo_renomeado` | 2 | 0 | 1 |
| `corpo_vazio` | 1 | 1 | 1 |
| `erro_interno_do_servidor` | 1 | 1 | 1 |
| `registro_duplicado` | 1 | 1 | 1 |
<!-- /tabela:tb_f4_tela_rotulos -->

<!-- tabela:tb_f4_tela_corpo -->
| Casos com o caso ao vivo lido | Sem diferença contra o contrato | Desses, mesmo rótulo | Desses, acerto na tela | Desses, colecao_no_lugar_de_objeto na tela | Com diferença contra o contrato | Desses, mesmo rótulo | Desses, acerto na tela | Sintoma "Nenhuma diferença medida" |
|---|---|---|---|---|---|---|---|---|
| 37 | 22 | 15 | 18 | 0 | 15 | 13 | 14 | 0 |
<!-- /tabela:tb_f4_tela_corpo -->

<!-- tabela:tb_f4_tela_casos -->
| Caso | Classe | Gabarito | Rótulo na tela | Rótulo no fixture | Tela | Fixture | Concordam | p tela | Selo tela | p fixture | Selo fixture | Gatilho | Divergência | s tela | s fixture | Diferenças contra o contrato | CORPO do caso ao vivo (começo) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `lex-1` | 1 | `resposta_truncada` | `resposta_truncada` | `resposta_truncada` | certo | certo | sim | 0,999 | alto | 1,000 | alto | não | não | 87,8 | 69,1 | 0 | `...[{"id": 1, "nome": "resposta truncada de propos` |
| `lex-4` | 1 | `codificacao_incorreta` | `codificacao_incorreta` | `codificacao_incorreta` | certo | certo | sim | 0,989 | medio | 0,999 | alto | não | não | 76,4 | 51,1 | 0 | `lista com 14 itens (referência em modo normal: 14); nome dif` |
| `sin-4` | 2 | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | certo | certo | sim | 0,998 | alto | 0,865 | medio | não | não | 84,1 | 40,2 | 1 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `sin-5` | 2 | `campo_ausente` | `campo_ausente` | `colecao_no_lugar_de_objeto` | certo | errado | não | 0,949 | medio | 0,625 | baixo | não | não | 67,5 | 58,9 | 1 | `{"resumo": "(ausente)"}` |
| `semt-1` | 3 | `tipo_divergente` | `tipo_divergente` | `tipo_divergente` | certo | certo | sim | 0,999 | alto | 0,929 | medio | não | não | 71,3 | 73,7 | 1 | `{"preco": "89.9"}` |
| `tra-1` | 4 | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | certo | certo | sim | 0,980 | medio | 0,996 | alto | não | não | 88,5 | 83,5 | 0 | `lista com 14 itens (referência em modo normal: 14); preco di` |
| `tra-4` | 4 | `contagem_inconsistente` | `resposta_truncada` | `contagem_inconsistente` | errado | certo | não | 0,507 | baixo | 0,968 | medio | sim | sim | 68,7 | 77,7 | 0 | `lista com 13 itens (referência em modo normal: 14); falta o ` |
| `run-1` | 5 | `erro_interno_do_servidor` | `erro_interno_do_servidor` | `erro_interno_do_servidor` | certo | certo | sim | 0,991 | alto | 0,979 | medio | não | não | 83,9 | 60,3 | 9 | `{"detail": "fault injection: error_500 em produto", "id": "(` |
| `run-2` | 5 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | certo | certo | sim | 0,999 | alto | 1,000 | alto | não | não | 54,5 | 70,5 | 0 | `lista com 14 itens, igual à referência em modo normal; prime` |
| `efe-3` | 6 | `campo_ausente` | `campo_ausente` | `campo_ausente` | certo | certo | sim | 0,989 | medio | 0,566 | baixo | não | não | 36,7 | 48,8 | 1 | `{"imagem": "(ausente)"}` |
| `lex-7` | 1 | `corpo_vazio` | `corpo_vazio` | `corpo_vazio` | certo | certo | sim | 0,996 | alto | 0,999 | alto | não | não | 80,8 | 58,0 | 0 | n/d |
| `lex-8` | 1 | `codificacao_incorreta` | `codificacao_incorreta` | `codificacao_incorreta` | certo | certo | sim | 0,981 | medio | 0,679 | baixo | não | não | 42,5 | 64,8 | 0 | `lista com 14 itens (referência em modo normal: 14); resumo d` |
| `lex-10` | 1 | `resposta_truncada` | `resposta_truncada` | `resposta_truncada` | certo | certo | sim | 0,999 | alto | 1,000 | alto | não | sim | 16,0 | 75,5 | 0 | `...[{"id": 1, "nome": "resposta truncada de propos` |
| `lex-11` | 1 | `codificacao_incorreta` | `codificacao_incorreta` | `codificacao_incorreta` | certo | certo | sim | 0,989 | medio | 1,000 | alto | não | não | 43,3 | 71,1 | 0 | `lista com 14 itens (referência em modo normal: 14); nome dif` |
| `sin-11` | 2 | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | certo | certo | sim | 0,957 | medio | 1,000 | alto | não | não | 76,0 | 77,3 | 1 | `{"preco": {"valor": 89.9, "moeda": "BRL"}}` |
| `sin-14` | 2 | `campo_renomeado` | `campo_renomeado` | `colecao_no_lugar_de_objeto` | certo | errado | não | 0,998 | alto | 0,309 | baixo | não | não | 70,6 | 55,6 | 1 | `{"imagem_v2": "picanha_alho.jpg"}` |
| `semt-8` | 3 | `nulo_inesperado` | `nulo_inesperado` | `nulo_inesperado` | certo | certo | sim | 0,996 | alto | 0,850 | medio | não | não | 68,5 | 70,3 | 1 | `{"preco": null}` |
| `semt-9` | 3 | `valor_fora_do_dominio` | `tipo_divergente` | `tipo_divergente` | errado | errado | sim | 0,998 | alto | 0,998 | alto | não | não | 73,4 | 54,3 | 1 | `{"destaque": "talvez"}` |
| `semt-14` | 3 | `nulo_inesperado` | `nulo_inesperado` | `nulo_inesperado` | certo | certo | sim | 0,997 | alto | 0,740 | baixo | não | não | 35,6 | 54,2 | 1 | `{"tipo": null}` |
| `tra-8` | 4 | `contagem_inconsistente` | `resposta_truncada` | `contagem_inconsistente` | errado | certo | não | 0,474 | baixo | 0,976 | medio | sim | sim | 15,5 | 38,1 | 0 | `lista com 13 itens (referência em modo normal: 14); falta o ` |
| `tra-11` | 4 | `contagem_inconsistente` | `contagem_inconsistente` | `contagem_inconsistente` | certo | certo | sim | 0,777 | baixo | 0,979 | medio | sim | não | 48,9 | 68,7 | 0 | `lista com 13 itens (referência em modo normal: 14); falta o ` |
| `run-9` | 5 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | certo | certo | sim | 0,999 | alto | 0,999 | alto | não | não | 55,7 | 55,8 | 0 | `lista com 14 itens, igual à referência em modo normal; prime` |
| `lex-16` | 1 | `resposta_truncada` | `resposta_truncada` | `resposta_truncada` | certo | certo | sim | 0,999 | alto | 1,000 | alto | não | não | 88,2 | 54,1 | 0 | `...[{"id": 1, "nome": "resposta truncada de propos` |
| `lex-18` | 1 | `codificacao_incorreta` | `codificacao_incorreta` | `valor_fora_do_dominio` | certo | errado | não | 0,981 | medio | 0,423 | baixo | não | não | 42,6 | 58,0 | 0 | `lista com 14 itens (referência em modo normal: 14); resumo d` |
| `sin-16` | 2 | `campo_ausente` | `campo_ausente` | `campo_ausente` | certo | certo | sim | 0,992 | alto | 0,997 | alto | não | não | 52,8 | 39,0 | 1 | `{"destaque": "(ausente)"}` |
| `sin-20` | 2 | `campo_ausente` | `campo_ausente` | `campo_ausente` | certo | certo | sim | 0,986 | medio | 0,997 | alto | não | não | 54,0 | 46,2 | 1 | `{"id": "(ausente)"}` |
| `sin-21` | 2 | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | certo | certo | sim | 0,993 | alto | 0,999 | alto | não | não | 83,8 | 69,2 | 1 | `{"tipo": {"valor": "Carnes", "moeda": "BRL"}}` |
| `semt-16` | 3 | `tipo_divergente` | `tipo_divergente` | `tipo_divergente` | certo | certo | sim | 0,999 | alto | 0,960 | medio | não | não | 36,7 | 51,9 | 1 | `{"tipo": 1}` |
| `semt-17` | 3 | `nulo_inesperado` | `nulo_inesperado` | `nulo_inesperado` | certo | certo | sim | 0,972 | medio | 0,913 | medio | não | não | 37,1 | 60,7 | 1 | `{"id": null}` |
| `semt-20` | 3 | `valor_fora_do_dominio` | `valor_fora_do_dominio` | `tipo_divergente` | certo | errado | não | 0,644 | baixo | 0,527 | baixo | sim | não | 81,5 | 36,7 | 0 | `lista com 14 itens (referência em modo normal: 14); preco di` |
| `semt-21` | 3 | `valor_fora_do_dominio` | `campo_renomeado` | `campo_ausente` | errado | errado | não | 0,998 | alto | 0,960 | medio | sim | sim | 44,9 | 51,5 | 0 | `lista com 14 itens (referência em modo normal: 14); nome dif` |
| `tra-17` | 4 | `chave_de_juncao_errada` | `chave_de_juncao_errada` | `tipo_divergente` | certo | errado | não | 0,995 | alto | 0,878 | medio | não | não | 85,5 | 35,3 | 0 | `lista com 14 itens (referência em modo normal: 14); tipo dif` |
| `tra-19` | 4 | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | certo | certo | sim | 0,980 | medio | 0,612 | baixo | não | não | 17,8 | 43,1 | 0 | `lista com 14 itens (referência em modo normal: 14); preco di` |
| `tra-20` | 4 | `chave_de_juncao_errada` | `chave_de_juncao_errada` | `chave_de_juncao_errada` | certo | certo | sim | 0,995 | alto | 0,997 | alto | não | não | 17,9 | 71,2 | 0 | `lista com 14 itens (referência em modo normal: 14); tipo dif` |
| `tra-21` | 4 | `contagem_inconsistente` | `resposta_truncada` | `contagem_inconsistente` | errado | certo | não | 0,791 | baixo | 0,986 | medio | sim | sim | 47,3 | 54,7 | 0 | `lista com 13 itens (referência em modo normal: 14); falta o ` |
| `run-19` | 5 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | certo | certo | sim | 0,981 | medio | 1,000 | alto | não | não | 71,2 | 61,1 | 0 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `run-21` | 5 | `registro_duplicado` | `registro_duplicado` | `registro_duplicado` | certo | certo | sim | 0,999 | alto | 0,895 | medio | não | não | 59,2 | 65,5 | 0 | `lista com 15 itens (referência em modo normal: 14); o id 1 (` |
<!-- /tabela:tb_f4_tela_casos -->
