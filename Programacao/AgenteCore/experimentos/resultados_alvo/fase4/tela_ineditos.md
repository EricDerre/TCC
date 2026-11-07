<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase4.py a partir de os registros da tela e do fixture, tela.jsonl e a trilha da corrida 18 (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Os inéditos na tela, a conferência limpa dos sinais (corrida 18e), gerada em 2026-11-06

Regra R2 do plano aprovado (a tela não piora): nos casos que reproduzem, o caso lido da tela e o mesmo caso lido do fixture, na mesma sessão do Ollama, não se afastam mais que a variação entre corridas iguais, 3 casos. Desde 06/11/2026 (decisão 98, antes da corrida 18d) o limite vale para os casos que a tela perde para o fixture (c); os que só a tela acerta (b) e a soma b + c, a conta usada até a corrida 18c, ficam ao lado. O gabarito entra só nesta leitura, nunca no agente. Prompt contra a calibração (seção 3.3 do plano): maior prompt da tela 1829 tokens, limite de 1409 (10% acima do maior da calibração, 1281); casos acima: `semt-27`, `tra-26`.


<!-- tabela:tb_f4_tela_resumo -->
| Casos | Reproduzem na tela | Acerto na tela | Acerto no fixture | Concordam (mesmo rótulo) | Concordância (%) | b (só a tela acerta) | c (só o fixture acerta) | b + c | Limite R2 (c) | Dentro do limite | b + c até o limite (conta de antes) | p (McNemar exato) | Selos na tela (alto / médio / baixo) | Gatilhos na tela | Divergências na tela | s por caso na tela (mediana) | s por caso no fixture (mediana) | Trilha (bytes) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 25 | 25 | 22 (88,0%) | 18 (72,0%) | 19 | 76,0 | 4 | 0 | 4 | 3 | sim | não | 0,125 | 10 / 10 / 5 | 5 | 2 | 73,7 | 64,6 | 1515688 |
<!-- /tabela:tb_f4_tela_resumo -->

<!-- tabela:tb_f4_tela_por_classe -->
| Classe | Casos | Acerto na tela | Acerto no fixture | Concordam |
|---|---|---|---|---|
| 1 | 5 | 5 | 5 | 5 |
| 2 | 6 | 6 | 5 | 5 |
| 3 | 5 | 4 | 3 | 3 |
| 4 | 5 | 3 | 1 | 2 |
| 5 | 4 | 4 | 4 | 4 |
<!-- /tabela:tb_f4_tela_por_classe -->

<!-- tabela:tb_f4_tela_verbete -->
| Lado | Verbete da causa certa entre os entregues | Casos | Acertos | Acerto (%) |
|---|---|---|---|---|
| tela | sim | 23 | 21 | 91,3 |
| tela | não | 2 | 1 | 50,0 |
| fixture | sim | 14 | 12 | 85,7 |
| fixture | não | 11 | 6 | 54,5 |
<!-- /tabela:tb_f4_tela_verbete -->

<!-- tabela:tb_f4_tela_selo -->
| Selo na tela | Casos | Acertos | Acerto (%) |
|---|---|---|---|
| alto | 10 | 10 | 100,0 |
| medio | 10 | 9 | 90,0 |
| baixo | 5 | 3 | 60,0 |
<!-- /tabela:tb_f4_tela_selo -->

<!-- tabela:tb_f4_tela_rotulos -->
| Rótulo | Dado na tela | Dado no fixture | É o gabarito de |
|---|---|---|---|
| `codificacao_incorreta` | 3 | 3 | 3 |
| `tipo_divergente` | 2 | 4 | 1 |
| `campo_renomeado` | 2 | 2 | 2 |
| `nulo_inesperado` | 2 | 2 | 2 |
| `campo_ausente` | 2 | 1 | 2 |
| `colecao_no_lugar_de_objeto` | 1 | 3 | 1 |
| `chave_de_juncao_errada` | 1 | 1 | 2 |
| `escala_ou_unidade_errada` | 2 | 0 | 2 |
| `corpo_nao_e_json` | 1 | 1 | 1 |
| `corpo_vazio` | 1 | 1 | 1 |
| `estrutura_aninhada_divergente` | 1 | 1 | 1 |
| `limite_de_requisicoes` | 1 | 1 | 1 |
| `recurso_inexistente` | 1 | 1 | 1 |
| `registro_duplicado` | 1 | 1 | 1 |
| `resposta_truncada` | 1 | 2 | 0 |
| `tempo_de_resposta_excedido` | 1 | 1 | 1 |
| `valor_fora_do_dominio` | 1 | 0 | 2 |
| `contagem_inconsistente` | 1 | 0 | 1 |
<!-- /tabela:tb_f4_tela_rotulos -->

<!-- tabela:tb_f4_tela_corpo -->
| Casos com o caso ao vivo lido | Sem diferença contra o contrato | Desses, mesmo rótulo | Desses, acerto na tela | Desses, colecao_no_lugar_de_objeto na tela | Com diferença contra o contrato | Desses, mesmo rótulo | Desses, acerto na tela | Sintoma "Nenhuma diferença medida" |
|---|---|---|---|---|---|---|---|---|
| 25 | 15 | 10 | 12 | 0 | 10 | 9 | 10 | 0 |
<!-- /tabela:tb_f4_tela_corpo -->

<!-- tabela:tb_f4_tela_casos -->
| Caso | Classe | Gabarito | Rótulo na tela | Rótulo no fixture | Tela | Fixture | Concordam | p tela | Selo tela | p fixture | Selo fixture | Gatilho | Divergência | s tela | s fixture | Diferenças contra o contrato | CORPO do caso ao vivo (começo) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `lex-22` | 1 | `corpo_nao_e_json` | `corpo_nao_e_json` | `corpo_nao_e_json` | certo | certo | sim | 0,929 | medio | 0,920 | medio | não | não | 89,8 | 64,1 | 0 | `<html><body><h1>Erro</h1><p>Falha ao montar a resposta.</p><` |
| `lex-23` | 1 | `corpo_vazio` | `corpo_vazio` | `corpo_vazio` | certo | certo | sim | 0,997 | alto | 0,987 | medio | não | não | 80,8 | 74,6 | 0 | n/d |
| `lex-24` | 1 | `codificacao_incorreta` | `codificacao_incorreta` | `codificacao_incorreta` | certo | certo | sim | 0,977 | medio | 0,999 | alto | não | não | 77,3 | 73,7 | 0 | `{"id": 14, "nome": "Abacaxi na Brasa", "resumo": "Com canela` |
| `lex-25` | 1 | `codificacao_incorreta` | `codificacao_incorreta` | `codificacao_incorreta` | certo | certo | sim | 0,989 | medio | 0,998 | alto | não | não | 47,8 | 67,6 | 0 | `lista com 14 itens (referência em modo normal: 14); nome dif` |
| `lex-26` | 1 | `codificacao_incorreta` | `codificacao_incorreta` | `codificacao_incorreta` | certo | certo | sim | 0,955 | medio | 0,999 | alto | não | não | 50,2 | 74,8 | 0 | `{"id": 11, "nome": "PÃ£o de Alho", "resumo": "Pão de alho gr` |
| `sin-22` | 2 | `campo_ausente` | `campo_ausente` | `campo_ausente` | certo | certo | sim | 0,995 | alto | 0,945 | medio | não | não | 69,3 | 54,6 | 1 | `{"nome": "(ausente)"}` |
| `sin-23` | 2 | `campo_renomeado` | `campo_renomeado` | `campo_renomeado` | certo | certo | sim | 0,999 | alto | 0,999 | alto | não | não | 70,9 | 59,8 | 1 | `{"resumo_v2": "Lata 350ml, diversos sabores"}` |
| `sin-24` | 2 | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | certo | certo | sim | 0,993 | alto | 0,767 | baixo | não | não | 82,6 | 67,6 | 1 | `{"tipo": {"valor": "Carnes", "moeda": "BRL"}}` |
| `sin-25` | 2 | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | certo | certo | sim | 0,922 | medio | 0,995 | alto | não | não | 78,6 | 56,6 | 1 | `{"id": 4, "nome": "Costelona", "resumo": "Costela assada len` |
| `sin-26` | 2 | `campo_ausente` | `campo_ausente` | `resposta_truncada` | certo | errado | não | 0,994 | alto | 0,950 | medio | não | não | 71,7 | 47,2 | 1 | `{"preco": "(ausente)"}` |
| `sin-27` | 2 | `campo_renomeado` | `campo_renomeado` | `campo_renomeado` | certo | certo | sim | 0,997 | alto | 0,413 | baixo | não | não | 57,9 | 69,6 | 1 | `{"imagem_v2": "picanha_alho.jpg"}` |
| `semt-22` | 3 | `nulo_inesperado` | `nulo_inesperado` | `nulo_inesperado` | certo | certo | sim | 0,996 | alto | 0,999 | alto | não | não | 67,5 | 43,7 | 1 | `{"preco": null}` |
| `semt-23` | 3 | `valor_fora_do_dominio` | `valor_fora_do_dominio` | `tipo_divergente` | certo | errado | não | 0,588 | baixo | 0,908 | medio | sim | não | 82,4 | 59,5 | 0 | `lista com 14 itens (referência em modo normal: 14); preco di` |
| `semt-24` | 3 | `tipo_divergente` | `tipo_divergente` | `tipo_divergente` | certo | certo | sim | 0,998 | alto | 0,995 | alto | não | não | 73,7 | 85,3 | 1 | `{"destaque": "True"}` |
| `semt-26` | 3 | `nulo_inesperado` | `nulo_inesperado` | `nulo_inesperado` | certo | certo | sim | 0,987 | medio | 0,907 | medio | não | não | 53,0 | 64,6 | 0 | `{"id": 12, "nome": "Queijo Coalho", "resumo": null, "tipo": ` |
| `semt-27` | 3 | `valor_fora_do_dominio` | `contagem_inconsistente` | `colecao_no_lugar_de_objeto` | errado | errado | não | 0,979 | medio | 0,645 | baixo | não | não | 109,9 | 65,4 | 0 | `lista com 14 itens (referência em modo normal: 14); faltam o` |
| `tra-22` | 4 | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | `tipo_divergente` | certo | errado | não | 0,980 | medio | 0,811 | baixo | não | não | 89,2 | 76,2 | 0 | `lista com 14 itens (referência em modo normal: 14); preco di` |
| `tra-24` | 4 | `chave_de_juncao_errada` | `chave_de_juncao_errada` | `chave_de_juncao_errada` | certo | certo | sim | 0,995 | alto | 0,915 | medio | não | não | 83,2 | 72,7 | 0 | `lista com 14 itens (referência em modo normal: 14); tipo dif` |
| `tra-25` | 4 | `contagem_inconsistente` | `resposta_truncada` | `resposta_truncada` | errado | errado | sim | 0,832 | baixo | 0,997 | alto | sim | sim | 67,4 | 60,2 | 0 | `lista com 13 itens (referência em modo normal: 14); falta o ` |
| `tra-26` | 4 | `chave_de_juncao_errada` | `tipo_divergente` | `colecao_no_lugar_de_objeto` | errado | errado | não | 0,696 | baixo | 0,915 | medio | sim | sim | 91,3 | 63,5 | 0 | `lista com 14 itens (referência em modo normal: 14); nome dif` |
| `tra-27` | 4 | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | `tipo_divergente` | certo | errado | não | 0,938 | medio | 0,958 | medio | não | não | 64,9 | 55,7 | 0 | `{"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre ` |
| `run-22` | 5 | `limite_de_requisicoes` | `limite_de_requisicoes` | `limite_de_requisicoes` | certo | certo | sim | 0,781 | baixo | 0,628 | baixo | sim | não | 82,0 | 55,4 | 9 | `{"detail": "limite de requisições excedido", "id": "(ausente` |
| `run-23` | 5 | `recurso_inexistente` | `recurso_inexistente` | `recurso_inexistente` | certo | certo | sim | 0,968 | medio | 0,995 | alto | não | não | 86,4 | 56,6 | 9 | `{"detail": "produto não encontrado", "id": "(ausente)", "nom` |
| `run-24` | 5 | `registro_duplicado` | `registro_duplicado` | `registro_duplicado` | certo | certo | sim | 0,999 | alto | 0,970 | medio | não | não | 56,5 | 67,7 | 0 | `lista com 15 itens (referência em modo normal: 14); o id 1 (` |
| `run-25` | 5 | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | certo | certo | sim | 0,698 | baixo | 0,835 | medio | sim | não | 72,0 | 73,5 | 0 | `{"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentament` |
<!-- /tabela:tb_f4_tela_casos -->
