<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por gerar_atlas.py a partir de os registros de diagnóstico das corridas `fase3`, `fase3b_ineditos`, `fase3b_cruzada_qwen` (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Atlas da busca e do uso dos verbetes, gerada em 2026-10-01

Método do `expert_atlas` do repositório colibri aplicado ao que o projeto mede: o item é o caso de teste, a entidade é o verbete da biblioteca, e a escolha é a da busca (os k verbetes que a busca põe no contexto do caso). Especialista: especialização a partir de 0,5 em pelo menos 2 casos distintos. Entropia máxima: 2,585 bits (seis classes).

Ressalvas:

- Parte da afinidade vem do desenho da biblioteca: há um verbete de erro por causa, e a busca soma reforços por endpoint, entidade e status calculados em código.
- A posição no desenho é a média das âncoras das classes ponderada pela afinidade medida; não é semelhança de significado.
- Os modelos do projeto são densos: o atlas descreve a busca e o uso que cada modelo fez do contexto, não o interior do modelo.

<!-- tabela:tb_atlas_bibliotecas -->
| Biblioteca | Verbetes | Recuperados em algum caso | Especialistas | Generalistas | Sem repetição | Nunca recuperados |
|---|---|---|---|---|---|---|
| L1 do `qwen2.5-coder:7b` (`0f0a6b7f3b37`) | 36 | 34 | 18 | 12 | 4 | 2 |
| L3 do `qwen2.5-coder:7b` (`2b7c441cb9e3`) | 36 | 34 | 19 | 11 | 4 | 2 |
| original, L0 (`3196327e7fd5`) | 36 | 34 | 20 | 10 | 4 | 2 |
| L1 do `qwen2.5:7b` (`3394d203cab9`) | 42 | 34 | 19 | 13 | 2 | 8 |
| L1 do `qwen2.5-coder:3b` (`53ccf19abeac`) | 36 | 34 | 20 | 10 | 4 | 2 |
| L2 do `qwen2.5:7b` (`5aa8cf796035`) | 43 | 34 | 18 | 14 | 2 | 9 |
| L2 do `qwen2.5-coder:7b` (`6791ba8b281c`) | 36 | 33 | 18 | 12 | 3 | 3 |
| L3 do `qwen2.5:7b` (`71258b553152`) | 45 | 34 | 17 | 15 | 2 | 11 |
| L2 do `qwen2.5-coder:3b` (`959db34be15c`) | 36 | 34 | 20 | 10 | 4 | 2 |
| L3 do `qwen2.5-coder:3b` (`d9a86e383103`) | 37 | 34 | 20 | 10 | 4 | 3 |
<!-- /tabela:tb_atlas_bibliotecas -->

Verbetes da biblioteca da fatia decidida (L1 do `qwen2.5:7b` (`3394d203cab9`)), do mais recuperado para o menos:

<!-- tabela:tb_atlas_verbetes -->
| Verbete | Pasta | Casos em que entrou no contexto | Vezes em primeiro | Classe dominante | Especialização | Entropia (bits) | Rótulo | Notas do modelo |
|---|---|---|---|---|---|---|---|---|
| `entidade-produto` | negocio | 42 | 35 | sintática | 0,08 | 2,37 | generalista | 2 |
| `contrato-produto` | contratos | 38 | 1 | sintática | 0,06 | 2,43 | generalista | 3 |
| `contrato-pedido` | contratos | 23 | 17 | semântica | 0,06 | 2,44 | generalista | 0 |
| `pedido-reserva` | negocio | 14 | 0 | tradução | 0,26 | 1,92 | generalista | 3 |
| `contagem_inconsistente` | erros | 13 | 6 | runtime | 0,33 | 1,74 | generalista | 0 |
| `estado_da_tela_divergente` | erros | 13 | 1 | efeito | 0,35 | 1,67 | generalista | 3 |
| `tipo_divergente` | erros | 13 | 0 | semântica | 0,27 | 1,89 | generalista | 1 |
| `estrutura_aninhada_divergente` | erros | 12 | 0 | runtime | 0,40 | 1,55 | generalista | 2 |
| `localizador_quebrado` | erros | 9 | 7 | efeito | 0,81 | 0,50 | especialista | 1 |
| `ancora-saiba-mais` | defeitos_conhecidos | 8 | 0 | efeito | 0,79 | 0,54 | especialista | 0 |
| `corpo_nao_e_json` | erros | 7 | 5 | léxica | 0,67 | 0,86 | especialista | 2 |
| `colecao_no_lugar_de_objeto` | erros | 6 | 0 | sintática | 0,44 | 1,46 | generalista | 2 |
| `tempo_de_resposta_excedido` | erros | 6 | 2 | nenhuma | 0,26 | 1,92 | generalista | 0 |
| `campo_ausente` | erros | 5 | 0 | sintática | 0,72 | 0,72 | especialista | 1 |
| `erro_interno_do_servidor` | erros | 5 | 3 | runtime | 0,62 | 0,97 | especialista | 2 |
| `formato_de_data_divergente` | erros | 5 | 1 | semântica | 0,26 | 1,92 | generalista | 1 |
| `valor_fora_do_dominio` | erros | 5 | 0 | nenhuma | 0,41 | 1,52 | generalista | 1 |
| `corpo_vazio` | erros | 4 | 3 | léxica | 0,69 | 0,81 | especialista | 2 |
| `dado_desatualizado` | erros | 4 | 1 | runtime | 0,69 | 0,81 | especialista | 1 |
| `mensagens-de-erro-do-codigo` | erros | 4 | 0 | runtime | 0,69 | 0,81 | especialista | 0 |
| `campo_renomeado` | erros | 3 | 1 | sintática | 1,00 | 0,00 | especialista | 1 |
| `codificacao_incorreta` | erros | 3 | 1 | léxica | 0,65 | 0,92 | especialista | 0 |
| `fluxo-reserva-e-cancelamento` | negocio | 3 | 0 | nenhuma | 0,39 | 1,58 | generalista | 0 |
| `limite_de_requisicoes` | erros | 3 | 2 | runtime | 1,00 | 0,00 | especialista | 0 |
| `nulo_inesperado` | erros | 3 | 0 | semântica | 1,00 | 0,00 | especialista | 0 |
| `recurso_inexistente` | erros | 3 | 2 | runtime | 0,65 | 0,92 | especialista | 1 |
| `resposta_truncada` | erros | 3 | 0 | léxica | 1,00 | 0,00 | especialista | 2 |
| `usuario-e-login` | negocio | 3 | 1 | tradução | 0,65 | 0,92 | especialista | 0 |
| `escala_ou_unidade_errada` | erros | 2 | 0 | tradução | 1,00 | 0,00 | especialista | 2 |
| `limites-do-sistema` | negocio | 2 | 0 | efeito | 1,00 | 0,00 | especialista | 0 |
| `pagina-produtos-api` | negocio | 2 | 0 | nenhuma | 0,61 | 1,00 | especialista | 0 |
| `registro_duplicado` | erros | 2 | 1 | nenhuma | 0,61 | 1,00 | especialista | 0 |
| `chave_de_juncao_errada` | erros | 1 | 0 | semântica | 1,00 | 0,00 | sem repetição | 1 |
| `consultas-sem-checagem` | defeitos_conhecidos | 1 | 0 | efeito | 1,00 | 0,00 | sem repetição | 0 |
| `atualizacao_imediata` | aprendidos | 0 | 0 | nenhuma | n/d | n/d | nunca recuperado | 0 |
| `conversao-de-unidade` | aprendidos | 0 | 0 | nenhuma | n/d | n/d | nunca recuperado | 0 |
| `conversao-de-valor` | aprendidos | 0 | 0 | nenhuma | n/d | n/d | nunca recuperado | 0 |
| `interface-estados` | aprendidos | 0 | 0 | nenhuma | n/d | n/d | nunca recuperado | 0 |
| `interface-frontend` | aprendidos | 0 | 0 | nenhuma | n/d | n/d | nunca recuperado | 0 |
| `modos-de-injecao` | falhas_injetadas | 0 | 0 | nenhuma | n/d | n/d | nunca recuperado | 0 |
| `rotas-inexistentes` | aprendidos | 0 | 0 | nenhuma | n/d | n/d | nunca recuperado | 0 |
| `senha-sem-hash` | defeitos_conhecidos | 0 | 0 | nenhuma | n/d | n/d | nunca recuperado | 0 |
<!-- /tabela:tb_atlas_verbetes -->

Validação: o atlas de cada biblioteca prevê a classe de um caso pelos verbetes da rota dele. Na primeira coluna de acerto o caso previsto ficou de fora da montagem do atlas; na segunda, o atlas dos casos oficiais prevê os casos inéditos.

<!-- tabela:tb_atlas_validacao -->
| Biblioteca | Casos | Acertos deixando um de fora | Acerto | Empates | Sem evidência | Inéditos previstos | Acerto nos inéditos | Acaso |
|---|---|---|---|---|---|---|---|---|
| L1 do `qwen2.5-coder:7b` (`0f0a6b7f3b37`) | 90 | 57 | 63,3% | 0 | 0 | n/d | n/d | 16,7% |
| L3 do `qwen2.5-coder:7b` (`2b7c441cb9e3`) | 90 | 56 | 62,2% | 1 | 0 | n/d | n/d | 16,7% |
| original, L0 (`3196327e7fd5`) | 90 | 59 | 65,6% | 1 | 0 | 23 de 36 | 63,9% | 16,7% |
| L1 do `qwen2.5:7b` (`3394d203cab9`) | 90 | 56 | 62,2% | 0 | 0 | 23 de 36 | 63,9% | 16,7% |
| L1 do `qwen2.5-coder:3b` (`53ccf19abeac`) | 90 | 59 | 65,6% | 1 | 0 | 23 de 36 | 63,9% | 16,7% |
| L2 do `qwen2.5:7b` (`5aa8cf796035`) | 90 | 56 | 62,2% | 0 | 0 | n/d | n/d | 16,7% |
| L2 do `qwen2.5-coder:7b` (`6791ba8b281c`) | 90 | 57 | 63,3% | 1 | 0 | n/d | n/d | 16,7% |
| L3 do `qwen2.5:7b` (`71258b553152`) | 90 | 56 | 62,2% | 0 | 0 | 24 de 36 | 66,7% | 16,7% |
| L2 do `qwen2.5-coder:3b` (`959db34be15c`) | 90 | 61 | 67,8% | 1 | 0 | n/d | n/d | 16,7% |
| L3 do `qwen2.5-coder:3b` (`d9a86e383103`) | 90 | 62 | 68,9% | 0 | 0 | 22 de 36 | 61,1% | 16,7% |
<!-- /tabela:tb_atlas_validacao -->

Por fatia (corrida, modelo e versão da biblioteca): o acerto do modelo, as citações e dois cruzamentos. O primeiro usa o gabarito: a rota aponta a classe verdadeira do caso? O segundo não usa: a causa que o modelo respondeu é de uma classe que a rota aponta? (Nos casos em que a rota empata ou não tem evidência o segundo cruzamento não se aplica.)

<!-- tabela:tb_atlas_fatias -->
| Fatia | Casos | Acerto do modelo | Verbetes citados (distintos) | Citações fora do contexto | Rota aponta a classe: acerto | Rota não aponta: acerto | Resposta na classe da rota: acerto | Resposta fora da classe da rota: acerto |
|---|---|---|---|---|---|---|---|---|
| `fase3/granite4.2_8b/L0` | 90 | 76,7% (69) | 29 | 0 | 91,5% (54 de 59) | 48,4% (15 de 31) | 82,1% (55 de 67) | 59,1% (13 de 22) |
| `fase3/granite4.2_8b/L1` | 90 | 77,8% (70) | 31 | 1 | 91,5% (54 de 59) | 51,6% (16 de 31) | 84,6% (55 de 65) | 58,3% (14 de 24) |
| `fase3/granite4.2_8b/L2` | 90 | 74,4% (67) | 31 | 0 | 91,5% (54 de 59) | 41,9% (13 de 31) | 82,1% (55 de 67) | 50,0% (11 de 22) |
| `fase3/granite4.2_8b/L3` | 90 | 75,6% (68) | 31 | 1 | 91,5% (54 de 59) | 45,2% (14 de 31) | 83,3% (55 de 66) | 52,2% (12 de 23) |
| `fase3/qwen2.5-coder_3b/L0` | 90 | 65,6% (59) | 27 | 0 | 74,6% (44 de 59) | 48,4% (15 de 31) | 81,8% (45 de 55) | 38,2% (13 de 34) |
| `fase3/qwen2.5-coder_3b/L1` | 90 | 66,7% (60) | 27 | 1 | 74,6% (44 de 59) | 51,6% (16 de 31) | 80,4% (45 de 56) | 42,4% (14 de 33) |
| `fase3/qwen2.5-coder_3b/L2` | 90 | 66,7% (60) | 28 | 0 | 78,7% (48 de 61) | 41,4% (12 de 29) | 81,7% (49 de 60) | 34,5% (10 de 29) |
| `fase3/qwen2.5-coder_3b/L3` | 90 | 67,8% (61) | 26 | 0 | 77,4% (48 de 62) | 46,4% (13 de 28) | 84,5% (49 de 58) | 37,5% (12 de 32) |
| `fase3/qwen2.5-coder_7b/L0` | 90 | 71,1% (64) | 24 | 0 | 83,1% (49 de 59) | 48,4% (15 de 31) | 80,3% (49 de 61) | 50,0% (14 de 28) |
| `fase3/qwen2.5-coder_7b/L1` | 90 | 74,4% (67) | 25 | 0 | 86,0% (49 de 57) | 54,5% (18 de 33) | 86,0% (49 de 57) | 54,5% (18 de 33) |
| `fase3/qwen2.5-coder_7b/L2` | 90 | 73,3% (66) | 25 | 0 | 86,0% (49 de 57) | 51,5% (17 de 33) | 87,5% (49 de 56) | 48,5% (16 de 33) |
| `fase3/qwen2.5-coder_7b/L3` | 90 | 72,2% (65) | 26 | 0 | 82,1% (46 de 56) | 55,9% (19 de 34) | 85,5% (47 de 55) | 50,0% (17 de 34) |
| `fase3/qwen2.5_7b/L0` | 90 | 71,1% (64) | 29 | 1 | 81,4% (48 de 59) | 51,6% (16 de 31) | 80,0% (48 de 60) | 51,7% (15 de 29) |
| `fase3/qwen2.5_7b/L1` | 90 | 76,7% (69) | 28 | 0 | 89,3% (50 de 56) | 55,9% (19 de 34) | 82,0% (50 de 61) | 65,5% (19 de 29) |
| `fase3/qwen2.5_7b/L2` | 90 | 74,4% (67) | 28 | 0 | 87,5% (49 de 56) | 52,9% (18 de 34) | 81,7% (49 de 60) | 60,0% (18 de 30) |
| `fase3/qwen2.5_7b/L3` | 90 | 77,8% (70) | 29 | 0 | 85,7% (48 de 56) | 64,7% (22 de 34) | 80,3% (49 de 61) | 72,4% (21 de 29) |
| `fase3b_ineditos/qwen2.5-coder_3b/L0` | 36 | 58,3% (21) | 22 | 1 | 69,6% (16 de 23) | 38,5% (5 de 13) | 72,7% (16 de 22) | 35,7% (5 de 14) |
| `fase3b_ineditos/qwen2.5-coder_3b/L1` | 36 | 58,3% (21) | 23 | 2 | 69,6% (16 de 23) | 38,5% (5 de 13) | 72,7% (16 de 22) | 35,7% (5 de 14) |
| `fase3b_ineditos/qwen2.5-coder_3b/L3` | 36 | 58,3% (21) | 21 | 1 | 72,7% (16 de 22) | 35,7% (5 de 14) | 69,6% (16 de 23) | 38,5% (5 de 13) |
| `fase3b_ineditos/qwen2.5_7b/L0` | 36 | 75,0% (27) | 25 | 0 | 82,6% (19 de 23) | 61,5% (8 de 13) | 90,5% (19 de 21) | 53,3% (8 de 15) |
| `fase3b_ineditos/qwen2.5_7b/L1` | 36 | 72,2% (26) | 24 | 0 | 78,3% (18 de 23) | 61,5% (8 de 13) | 78,3% (18 de 23) | 61,5% (8 de 13) |
| `fase3b_ineditos/qwen2.5_7b/L3` | 36 | 80,6% (29) | 25 | 0 | 83,3% (20 de 24) | 75,0% (9 de 12) | 76,9% (20 de 26) | 90,0% (9 de 10) |
| `fase3b_cruzada_qwen/qwen2.5-coder_3b/L1` | 36 | 61,1% (22) | 17 | 0 | 68,2% (15 de 22) | 50,0% (7 de 14) | 88,2% (15 de 17) | 36,8% (7 de 19) |
| `fase3b_cruzada_qwen/qwen2.5-coder_3b/L3` | 36 | 61,1% (22) | 18 | 1 | 66,7% (16 de 24) | 50,0% (6 de 12) | 88,9% (16 de 18) | 33,3% (6 de 18) |
| `fase3b_cruzada_qwen/qwen2.5-coder_7b/L1` | 36 | 83,3% (30) | 21 | 0 | 90,9% (20 de 22) | 71,4% (10 de 14) | 95,5% (21 de 22) | 64,3% (9 de 14) |
| `fase3b_cruzada_qwen/qwen2.5-coder_7b/L3` | 36 | 83,3% (30) | 20 | 0 | 91,7% (22 de 24) | 66,7% (8 de 12) | 92,0% (23 de 25) | 63,6% (7 de 11) |
<!-- /tabela:tb_atlas_fatias -->
