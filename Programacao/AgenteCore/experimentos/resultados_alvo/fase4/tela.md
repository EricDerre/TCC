<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase4.py a partir de os registros da tela e do fixture, tela.jsonl e a trilha da corrida 18 (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Diagnóstico ao vivo e o mesmo caso do fixture (corrida 18), gerada em 2026-11-01

Regra R2 do plano aprovado: nos casos que reproduzem, o rótulo dado ao caso lido da tela e o rótulo dado ao caso lido do fixture, na mesma sessão do Ollama, diferem em no máximo 3 casos (a variação entre corridas iguais); acima disso, o molde do sintoma e a poda são revistos antes da próxima noite. O gabarito entra só nesta leitura, nunca no agente. Prompt contra a calibração (seção 3.3 do plano): maior prompt da tela 1939 tokens, limite de 1409 (10% acima do maior da calibração, 1281); casos acima: `lex-1`, `lex-4`, `sin-4`, `sin-5`, `semt-1`, `tra-1`, `tra-4`, `run-1`, `run-2`, `efe-3`, `lex-7`, `lex-8`, `lex-10`, `lex-11`, `sin-11`, `sin-14`, `semt-8`, `semt-9`, `semt-14`, `tra-8`, `tra-11`, `run-9`, `lex-16`, `lex-18`, `sin-16`, `sin-20`, `sin-21`, `semt-16`, `semt-17`, `semt-20`, `semt-21`, `tra-17`, `tra-19`, `tra-20`, `tra-21`, `run-19`, `run-21`.


<!-- tabela:tb_f4_tela_resumo -->
| Casos | Reproduzem na tela | Acerto na tela | Acerto no fixture | Concordam (mesmo rótulo) | Concordância (%) | b (só a tela acerta) | c (só o fixture acerta) | b + c | Limite R2 | Dentro do limite | p (McNemar exato) | Selos na tela (alto / médio / baixo) | Gatilhos na tela | Divergências na tela | s por caso na tela (mediana) | s por caso no fixture (mediana) | Trilha (bytes) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 37 | 37 | 16 (43,2%) | 31 (83,8%) | 16 | 43,2 | 1 | 16 | 17 | 3 | não | 0,000 | 5 / 22 / 10 | 12 | 6 | 81,1 | 56,2 | 2122521 |
<!-- /tabela:tb_f4_tela_resumo -->

<!-- tabela:tb_f4_tela_por_classe -->
| Classe | Casos | Acerto na tela | Acerto no fixture | Concordam |
|---|---|---|---|---|
| 1 | 8 | 4 | 7 | 4 |
| 2 | 7 | 5 | 5 | 4 |
| 3 | 8 | 4 | 6 | 5 |
| 4 | 8 | 1 | 7 | 1 |
| 5 | 5 | 1 | 5 | 1 |
| 6 | 1 | 1 | 1 | 1 |
<!-- /tabela:tb_f4_tela_por_classe -->

<!-- tabela:tb_f4_tela_rotulos -->
| Rótulo | Dado na tela | Dado no fixture | É o gabarito de |
|---|---|---|---|
| `colecao_no_lugar_de_objeto` | 12 | 3 | 1 |
| `campo_ausente` | 5 | 4 | 4 |
| `tipo_divergente` | 6 | 4 | 2 |
| `resposta_truncada` | 4 | 3 | 3 |
| `contagem_inconsistente` | 1 | 4 | 4 |
| `nulo_inesperado` | 2 | 3 | 3 |
| `codificacao_incorreta` | 0 | 3 | 4 |
| `estrutura_aninhada_divergente` | 2 | 2 | 2 |
| `tempo_de_resposta_excedido` | 0 | 3 | 3 |
| `valor_fora_do_dominio` | 0 | 2 | 3 |
| `escala_ou_unidade_errada` | 0 | 2 | 2 |
| `chave_de_juncao_errada` | 0 | 1 | 2 |
| `corpo_vazio` | 1 | 1 | 1 |
| `erro_interno_do_servidor` | 1 | 1 | 1 |
| `campo_renomeado` | 1 | 0 | 1 |
| `formato_de_data_divergente` | 2 | 0 | 0 |
| `registro_duplicado` | 0 | 1 | 1 |
<!-- /tabela:tb_f4_tela_rotulos -->

<!-- tabela:tb_f4_tela_corpo -->
| Casos com o caso ao vivo lido | Sem diferença contra o contrato | Desses, mesmo rótulo | Desses, acerto na tela | Desses, colecao_no_lugar_de_objeto na tela | Com diferença contra o contrato | Desses, mesmo rótulo | Desses, acerto na tela | Sintoma "Nenhuma diferença medida" |
|---|---|---|---|---|---|---|---|---|
| 37 | 22 | 5 | 5 | 11 | 15 | 11 | 11 | 5 |
<!-- /tabela:tb_f4_tela_corpo -->

<!-- tabela:tb_f4_tela_casos -->
| Caso | Classe | Gabarito | Rótulo na tela | Rótulo no fixture | Tela | Fixture | Concordam | p tela | Selo tela | p fixture | Selo fixture | Gatilho | Divergência | s tela | s fixture | Diferenças contra o contrato | CORPO do caso ao vivo (começo) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `lex-1` | 1 | `resposta_truncada` | `resposta_truncada` | `resposta_truncada` | certo | certo | sim | 0,878 | medio | 1,000 | alto | não | não | 98,2 | 59,5 | 0 | `...[{"id": 1, "nome": "resposta truncada de propos` |
| `lex-4` | 1 | `codificacao_incorreta` | `colecao_no_lugar_de_objeto` | `codificacao_incorreta` | errado | certo | não | 0,906 | medio | 0,999 | alto | não | não | 85,2 | 40,7 | 0 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `sin-4` | 2 | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | certo | certo | sim | 0,998 | alto | 0,880 | medio | não | não | 66,6 | 56,6 | 1 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `sin-5` | 2 | `campo_ausente` | `campo_ausente` | `colecao_no_lugar_de_objeto` | certo | errado | não | 0,985 | medio | 0,758 | baixo | não | não | 86,4 | 48,3 | 1 | `{"resumo": "(ausente)"}` |
| `semt-1` | 3 | `tipo_divergente` | `tipo_divergente` | `tipo_divergente` | certo | certo | sim | 0,997 | alto | 0,805 | baixo | não | não | 88,5 | 65,9 | 1 | `{"preco": "89.9"}` |
| `tra-1` | 4 | `escala_ou_unidade_errada` | `formato_de_data_divergente` | `escala_ou_unidade_errada` | errado | certo | não | 0,477 | baixo | 0,995 | alto | sim | sim | 94,3 | 68,6 | 0 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `tra-4` | 4 | `contagem_inconsistente` | `contagem_inconsistente` | `contagem_inconsistente` | certo | certo | sim | 0,394 | baixo | 0,982 | medio | sim | sim | 72,2 | 69,9 | 0 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `run-1` | 5 | `erro_interno_do_servidor` | `erro_interno_do_servidor` | `erro_interno_do_servidor` | certo | certo | sim | 0,990 | medio | 0,985 | medio | sim | sim | 97,4 | 64,5 | 9 | `{"detail": "fault injection: error_500 em produto", "id": "(` |
| `run-2` | 5 | `tempo_de_resposta_excedido` | `colecao_no_lugar_de_objeto` | `tempo_de_resposta_excedido` | errado | certo | não | 0,849 | medio | 0,999 | alto | não | não | 37,1 | 57,8 | 0 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `efe-3` | 6 | `campo_ausente` | `campo_ausente` | `campo_ausente` | certo | certo | sim | 0,995 | alto | 0,585 | baixo | não | não | 62,4 | 31,9 | 1 | `{"imagem": "(ausente)"}` |
| `lex-7` | 1 | `corpo_vazio` | `corpo_vazio` | `corpo_vazio` | certo | certo | sim | 0,977 | medio | 1,000 | alto | não | não | 90,8 | 53,3 | 0 | n/d |
| `lex-8` | 1 | `codificacao_incorreta` | `colecao_no_lugar_de_objeto` | `codificacao_incorreta` | errado | certo | não | 0,616 | baixo | 0,749 | baixo | sim | não | 47,0 | 65,2 | 0 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `lex-10` | 1 | `resposta_truncada` | `resposta_truncada` | `resposta_truncada` | certo | certo | sim | 0,876 | medio | 1,000 | alto | não | não | 20,4 | 52,0 | 0 | `...[{"id": 1, "nome": "resposta truncada de propos` |
| `lex-11` | 1 | `codificacao_incorreta` | `colecao_no_lugar_de_objeto` | `codificacao_incorreta` | errado | certo | não | 0,894 | medio | 1,000 | alto | não | não | 55,4 | 57,3 | 0 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `sin-11` | 2 | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | certo | certo | sim | 0,985 | medio | 1,000 | alto | não | não | 108,9 | 69,7 | 1 | `{"preco": {"valor": 89.9, "moeda": "BRL"}}` |
| `sin-14` | 2 | `campo_renomeado` | `estrutura_aninhada_divergente` | `colecao_no_lugar_de_objeto` | errado | errado | não | 0,985 | medio | 0,301 | baixo | não | não | 96,2 | 50,3 | 1 | `{"imagem_v2": "picanha_alho.jpg"}` |
| `semt-8` | 3 | `nulo_inesperado` | `nulo_inesperado` | `nulo_inesperado` | certo | certo | sim | 0,963 | medio | 0,850 | medio | não | não | 93,1 | 63,9 | 1 | `{"preco": null}` |
| `semt-9` | 3 | `valor_fora_do_dominio` | `tipo_divergente` | `tipo_divergente` | errado | errado | sim | 0,999 | alto | 0,995 | alto | não | não | 93,7 | 47,1 | 1 | `{"destaque": "talvez"}` |
| `semt-14` | 3 | `nulo_inesperado` | `nulo_inesperado` | `nulo_inesperado` | certo | certo | sim | 0,934 | medio | 0,740 | baixo | não | não | 87,9 | 49,0 | 1 | `{"tipo": null}` |
| `tra-8` | 4 | `contagem_inconsistente` | `resposta_truncada` | `contagem_inconsistente` | errado | certo | não | 0,407 | baixo | 0,876 | medio | sim | sim | 17,6 | 35,3 | 0 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `tra-11` | 4 | `contagem_inconsistente` | `colecao_no_lugar_de_objeto` | `contagem_inconsistente` | errado | certo | não | 0,666 | baixo | 0,986 | medio | sim | não | 73,1 | 59,5 | 0 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `run-9` | 5 | `tempo_de_resposta_excedido` | `colecao_no_lugar_de_objeto` | `tempo_de_resposta_excedido` | errado | certo | não | 0,801 | baixo | 0,999 | alto | sim | não | 68,2 | 51,1 | 0 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `lex-16` | 1 | `resposta_truncada` | `resposta_truncada` | `resposta_truncada` | certo | certo | sim | 0,981 | medio | 1,000 | alto | não | não | 95,9 | 66,1 | 0 | `...[{"id": 1, "nome": "resposta truncada de propos` |
| `lex-18` | 1 | `codificacao_incorreta` | `colecao_no_lugar_de_objeto` | `valor_fora_do_dominio` | errado | errado | não | 0,616 | baixo | 0,492 | baixo | sim | não | 46,3 | 67,5 | 0 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `sin-16` | 2 | `campo_ausente` | `campo_ausente` | `campo_ausente` | certo | certo | sim | 0,961 | medio | 0,997 | alto | não | não | 97,3 | 47,0 | 1 | `{"destaque": "(ausente)"}` |
| `sin-20` | 2 | `campo_ausente` | `campo_ausente` | `campo_ausente` | certo | certo | sim | 0,999 | alto | 0,997 | alto | não | não | 91,8 | 42,2 | 1 | `{"id": "(ausente)"}` |
| `sin-21` | 2 | `estrutura_aninhada_divergente` | `tipo_divergente` | `estrutura_aninhada_divergente` | errado | certo | não | 0,983 | medio | 0,999 | alto | sim | sim | 101,3 | 73,2 | 1 | `{"tipo": {"valor": "Carnes", "moeda": "BRL"}}` |
| `semt-16` | 3 | `tipo_divergente` | `tipo_divergente` | `tipo_divergente` | certo | certo | sim | 0,976 | medio | 0,948 | medio | não | não | 64,1 | 47,5 | 1 | `{"tipo": 1}` |
| `semt-17` | 3 | `nulo_inesperado` | `campo_ausente` | `nulo_inesperado` | errado | certo | não | 0,883 | medio | 0,913 | medio | não | não | 59,4 | 56,2 | 1 | `{"id": null}` |
| `semt-20` | 3 | `valor_fora_do_dominio` | `tipo_divergente` | `valor_fora_do_dominio` | errado | certo | não | 0,876 | medio | 0,464 | baixo | não | não | 85,2 | 34,5 | 0 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `semt-21` | 3 | `valor_fora_do_dominio` | `campo_renomeado` | `campo_ausente` | errado | errado | não | 0,481 | baixo | 0,961 | medio | sim | não | 87,3 | 45,2 | 0 | `{"id": 1, "nome": "Picanha ao Alho (inválido)", "resumo": "P` |
| `tra-17` | 4 | `chave_de_juncao_errada` | `colecao_no_lugar_de_objeto` | `tipo_divergente` | errado | errado | não | 0,856 | medio | 0,952 | medio | não | não | 35,6 | 33,8 | 0 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `tra-19` | 4 | `escala_ou_unidade_errada` | `formato_de_data_divergente` | `escala_ou_unidade_errada` | errado | certo | não | 0,497 | baixo | 0,612 | baixo | sim | sim | 21,9 | 39,2 | 0 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `tra-20` | 4 | `chave_de_juncao_errada` | `colecao_no_lugar_de_objeto` | `chave_de_juncao_errada` | errado | certo | não | 0,855 | medio | 0,997 | alto | não | não | 18,2 | 65,3 | 0 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `tra-21` | 4 | `contagem_inconsistente` | `colecao_no_lugar_de_objeto` | `contagem_inconsistente` | errado | certo | não | 0,891 | medio | 0,967 | medio | não | não | 45,1 | 49,6 | 0 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `run-19` | 5 | `tempo_de_resposta_excedido` | `tipo_divergente` | `tempo_de_resposta_excedido` | errado | certo | não | 0,321 | baixo | 1,000 | alto | sim | não | 81,1 | 63,9 | 0 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
| `run-21` | 5 | `registro_duplicado` | `colecao_no_lugar_de_objeto` | `registro_duplicado` | errado | certo | não | 0,898 | medio | 0,604 | baixo | não | não | 52,5 | 59,1 | 0 | `{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grel` |
<!-- /tabela:tb_f4_tela_casos -->
