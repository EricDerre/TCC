<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase4.py a partir de cura.jsonl e condicoes_fase4.json da corrida (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Cura de seletor (corrida 19), gerada em 2026-11-01

Uma cura só conta quando a conferência final do roteiro passa na reexecução com o candidato no lugar do localizador (regra R3 do plano aprovado); "mesmo elemento" e "outro elemento" saem da impressão do DOM (tag, type, name, action do formulário, data-nome, href), que nenhum modo de quebra muda. O MTTR vai da detecção (o passo do alvo falhou) à reexecução validada, descontado o tempo de restaurar o banco. As duas formas da quebra (pelo harness no navegador e pela variante do front PHP, ficha 29 c) são comparadas célula a célula pela árvore da página quebrada e pelo resultado.


<!-- tabela:tb_f4_cura_resumo -->
| Execuções | Quebras detectadas | Não quebrou | Curadas | Não curadas | Taxa de cura (%) | Mesmo elemento | Outro elemento | MTTR mediana (s) | MTTR mínimo (s) | MTTR máximo (s) | Reexecuções (mediana) | Repetições | Limiar do nome | Formas | Tempo limite (ms) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 160 | 160 | 0 | 160 | 0 | 100,0 | 160 | 0 | 0,639 | 0,355 | 0,887 | 1,0 | 5 | 0,6 | harness, php | 5000 |
<!-- /tabela:tb_f4_cura_resumo -->

<!-- tabela:tb_f4_cura_por_modo -->
| Modo de quebra | Execuções | Quebraram | Curadas | Taxa de cura (%) | Mesmo elemento | Outro elemento | Não curadas | Não quebrou | MTTR mediana (s) | MTTR máximo (s) | Estratégias aplicadas |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `id_renomeado` | 40 | 40 | 40 | 100,0 | 40 | 0 | 0 | 0 | 0,617 | 0,887 | `papel_e_nome` 40 |
| `classe_trocada` | 40 | 40 | 40 | 100,0 | 40 | 0 | 0 | 0 | 0,631 | 0,824 | `papel_e_nome` 40 |
| `texto_alterado` | 40 | 40 | 40 | 100,0 | 40 | 0 | 0 | 0 | 0,675 | 0,886 | `papel_e_nome` 10, `papel_e_nome_parecido` 30 |
| `estrutura_alterada` | 40 | 40 | 40 | 100,0 | 40 | 0 | 0 | 0 | 0,619 | 0,822 | `papel_e_nome` 40 |
<!-- /tabela:tb_f4_cura_por_modo -->

<!-- tabela:tb_f4_cura_por_roteiro -->
| Roteiro | Execuções | Quebraram | Curadas | Taxa de cura (%) | Mesmo elemento | Outro elemento | Não curadas | Não quebrou | MTTR mediana (s) | MTTR máximo (s) | Estratégias aplicadas |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `front-busca` | 40 | 40 | 40 | 100,0 | 40 | 0 | 0 | 0 | 0,510 | 0,713 | `papel_e_nome` 40 |
| `front-admin-login` | 40 | 40 | 40 | 100,0 | 40 | 0 | 0 | 0 | 0,395 | 0,448 | `papel_e_nome` 30, `papel_e_nome_parecido` 10 |
| `front-admin-produtos` | 40 | 40 | 40 | 100,0 | 40 | 0 | 0 | 0 | 0,776 | 0,887 | `papel_e_nome` 30, `papel_e_nome_parecido` 10 |
| `front-cliente-reserva` | 40 | 40 | 40 | 100,0 | 40 | 0 | 0 | 0 | 0,714 | 0,886 | `papel_e_nome` 30, `papel_e_nome_parecido` 10 |
<!-- /tabela:tb_f4_cura_por_roteiro -->

<!-- tabela:tb_f4_cura_por_forma -->
| Forma da quebra | Execuções | Quebraram | Curadas | Taxa de cura (%) | Mesmo elemento | Outro elemento | Não curadas | Não quebrou | MTTR mediana (s) | MTTR máximo (s) | Estratégias aplicadas |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `harness` | 80 | 80 | 80 | 100,0 | 80 | 0 | 0 | 0 | 0,632 | 0,886 | `papel_e_nome` 65, `papel_e_nome_parecido` 15 |
| `php` | 80 | 80 | 80 | 100,0 | 80 | 0 | 0 | 0 | 0,639 | 0,887 | `papel_e_nome` 65, `papel_e_nome_parecido` 15 |
<!-- /tabela:tb_f4_cura_por_forma -->

<!-- tabela:tb_f4_cura_formas -->
| Células comparadas (harness e php) | Mesma árvore da página quebrada | Árvore diferente em | Mesmo resultado (quebrou, curou, estratégia) |
|---|---|---|---|
| 16 | 16 | nenhuma | 16 |
<!-- /tabela:tb_f4_cura_formas -->

<!-- tabela:tb_f4_cura_estrategias -->
| Estratégia | Gerada | Passou as estáticas | Reexecutada | Aplicada (curou) | Recusada em resolve_um_elemento | Recusada em visivel_e_habilitado | Recusada em mesmo_papel | Recusada em nome_parecido | Recusada em efeito_na_reexecucao |
|---|---|---|---|---|---|---|---|---|---|
| `papel_e_nome` | 130 | 130 | 130 | 130 | 0 | 0 | 0 | 0 | 0 |
| `papel_e_nome_parecido` | 30 | 30 | 30 | 30 | 0 | 0 | 0 | 0 | 0 |
| `texto_contido` | 110 | 70 | 0 | 0 | 0 | 0 | 40 | 0 | 0 |
| `data_id` | 40 | 30 | 0 | 0 | 10 | 0 | 0 | 0 | 0 |
| `caminho_do_ancestral_com_id` | 160 | 120 | 0 | 0 | 40 | 0 | 0 | 0 | 0 |
| `posicao_entre_irmaos` | 160 | 150 | 0 | 0 | 0 | 0 | 0 | 10 | 0 |
<!-- /tabela:tb_f4_cura_estrategias -->

<!-- tabela:tb_f4_cura_outro_elemento -->
| Execução | Roteiro | Modo | Forma | Estratégia aplicada | Seletor curado | MTTR (s) |
|---|---|---|---|---|---|---|
| nenhuma |  |  |  |  |  |  |
<!-- /tabela:tb_f4_cura_outro_elemento -->

<!-- tabela:tb_f4_cura_nao_curadas -->
| Execução | Roteiro | Modo | Forma | Falha | Reexecuções | Fora do passo do alvo | Erro |
|---|---|---|---|---|---|---|---|
| nenhuma |  |  |  |  |  |  |  |
<!-- /tabela:tb_f4_cura_nao_curadas -->

<!-- tabela:tb_f4_cura_execucoes -->
| Execução | Localizador | Quebrou | Passo | Curada | Estratégia | Seletor curado | Mesmo elemento | Falha | MTTR (s) | Reexecuções | Segundos |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `front-busca/id_renomeado/harness/r1` | `#buscar` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,519 | 1 | 5,8 |
| `front-busca/id_renomeado/harness/r2` | `#buscar` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,511 | 1 | 5,8 |
| `front-busca/id_renomeado/harness/r3` | `#buscar` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,476 | 1 | 5,8 |
| `front-busca/id_renomeado/harness/r4` | `#buscar` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,539 | 1 | 5,8 |
| `front-busca/id_renomeado/harness/r5` | `#buscar` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,514 | 1 | 5,8 |
| `front-busca/id_renomeado/php/r1` | `#buscar` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,562 | 1 | 5,9 |
| `front-busca/id_renomeado/php/r2` | `#buscar` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,506 | 1 | 5,8 |
| `front-busca/id_renomeado/php/r3` | `#buscar` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,508 | 1 | 5,8 |
| `front-busca/id_renomeado/php/r4` | `#buscar` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,489 | 1 | 5,8 |
| `front-busca/id_renomeado/php/r5` | `#buscar` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,503 | 1 | 5,8 |
| `front-busca/classe_trocada/harness/r1` | `#form-busca input.form-control` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,623 | 1 | 5,9 |
| `front-busca/classe_trocada/harness/r2` | `#form-busca input.form-control` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,506 | 1 | 5,8 |
| `front-busca/classe_trocada/harness/r3` | `#form-busca input.form-control` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,490 | 1 | 5,8 |
| `front-busca/classe_trocada/harness/r4` | `#form-busca input.form-control` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,498 | 1 | 5,8 |
| `front-busca/classe_trocada/harness/r5` | `#form-busca input.form-control` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,511 | 1 | 5,8 |
| `front-busca/classe_trocada/php/r1` | `#form-busca input.form-control` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,502 | 1 | 5,8 |
| `front-busca/classe_trocada/php/r2` | `#form-busca input.form-control` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,511 | 1 | 5,8 |
| `front-busca/classe_trocada/php/r3` | `#form-busca input.form-control` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,547 | 1 | 5,8 |
| `front-busca/classe_trocada/php/r4` | `#form-busca input.form-control` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,492 | 1 | 5,8 |
| `front-busca/classe_trocada/php/r5` | `#form-busca input.form-control` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,522 | 1 | 5,8 |
| `front-busca/texto_alterado/harness/r1` | `input[placeholder="Buscar produto"]` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,536 | 1 | 5,8 |
| `front-busca/texto_alterado/harness/r2` | `input[placeholder="Buscar produto"]` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,517 | 1 | 5,8 |
| `front-busca/texto_alterado/harness/r3` | `input[placeholder="Buscar produto"]` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,479 | 1 | 5,8 |
| `front-busca/texto_alterado/harness/r4` | `input[placeholder="Buscar produto"]` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,461 | 1 | 5,7 |
| `front-busca/texto_alterado/harness/r5` | `input[placeholder="Buscar produto"]` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,520 | 1 | 5,8 |
| `front-busca/texto_alterado/php/r1` | `input[placeholder="Buscar produto"]` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,713 | 1 | 6,0 |
| `front-busca/texto_alterado/php/r2` | `input[placeholder="Buscar produto"]` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,502 | 1 | 5,9 |
| `front-busca/texto_alterado/php/r3` | `input[placeholder="Buscar produto"]` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,483 | 1 | 5,8 |
| `front-busca/texto_alterado/php/r4` | `input[placeholder="Buscar produto"]` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,536 | 1 | 5,8 |
| `front-busca/texto_alterado/php/r5` | `input[placeholder="Buscar produto"]` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,528 | 1 | 5,8 |
| `front-busca/estrutura_alterada/harness/r1` | `#form-busca > div > input` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,583 | 1 | 5,9 |
| `front-busca/estrutura_alterada/harness/r2` | `#form-busca > div > input` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,504 | 1 | 5,8 |
| `front-busca/estrutura_alterada/harness/r3` | `#form-busca > div > input` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,520 | 1 | 5,8 |
| `front-busca/estrutura_alterada/harness/r4` | `#form-busca > div > input` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,498 | 1 | 5,8 |
| `front-busca/estrutura_alterada/harness/r5` | `#form-busca > div > input` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,489 | 1 | 5,8 |
| `front-busca/estrutura_alterada/php/r1` | `#form-busca > div > input` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,499 | 1 | 5,8 |
| `front-busca/estrutura_alterada/php/r2` | `#form-busca > div > input` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,599 | 1 | 5,9 |
| `front-busca/estrutura_alterada/php/r3` | `#form-busca > div > input` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,509 | 1 | 5,8 |
| `front-busca/estrutura_alterada/php/r4` | `#form-busca > div > input` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,511 | 1 | 5,8 |
| `front-busca/estrutura_alterada/php/r5` | `#form-busca > div > input` | sim | 1 | sim | `papel_e_nome` | `role=searchbox[name="search"]` | sim |  | 0,496 | 1 | 5,8 |
| `front-admin-login/id_renomeado/harness/r1` | `#login_usuario` | sim | 1 | sim | `papel_e_nome` | `role=textbox[name="Login"]` | sim |  | 0,402 | 1 | 5,6 |
| `front-admin-login/id_renomeado/harness/r2` | `#login_usuario` | sim | 1 | sim | `papel_e_nome` | `role=textbox[name="Login"]` | sim |  | 0,373 | 1 | 5,6 |
| `front-admin-login/id_renomeado/harness/r3` | `#login_usuario` | sim | 1 | sim | `papel_e_nome` | `role=textbox[name="Login"]` | sim |  | 0,377 | 1 | 5,6 |
| `front-admin-login/id_renomeado/harness/r4` | `#login_usuario` | sim | 1 | sim | `papel_e_nome` | `role=textbox[name="Login"]` | sim |  | 0,396 | 1 | 5,6 |
| `front-admin-login/id_renomeado/harness/r5` | `#login_usuario` | sim | 1 | sim | `papel_e_nome` | `role=textbox[name="Login"]` | sim |  | 0,387 | 1 | 5,6 |
| `front-admin-login/id_renomeado/php/r1` | `#login_usuario` | sim | 1 | sim | `papel_e_nome` | `role=textbox[name="Login"]` | sim |  | 0,365 | 1 | 5,5 |
| `front-admin-login/id_renomeado/php/r2` | `#login_usuario` | sim | 1 | sim | `papel_e_nome` | `role=textbox[name="Login"]` | sim |  | 0,440 | 1 | 5,6 |
| `front-admin-login/id_renomeado/php/r3` | `#login_usuario` | sim | 1 | sim | `papel_e_nome` | `role=textbox[name="Login"]` | sim |  | 0,431 | 1 | 5,6 |
| `front-admin-login/id_renomeado/php/r4` | `#login_usuario` | sim | 1 | sim | `papel_e_nome` | `role=textbox[name="Login"]` | sim |  | 0,442 | 1 | 5,6 |
| `front-admin-login/id_renomeado/php/r5` | `#login_usuario` | sim | 1 | sim | `papel_e_nome` | `role=textbox[name="Login"]` | sim |  | 0,401 | 1 | 5,6 |
| `front-admin-login/classe_trocada/harness/r1` | `button.btn-primary` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,388 | 1 | 5,6 |
| `front-admin-login/classe_trocada/harness/r2` | `button.btn-primary` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,398 | 1 | 5,6 |
| `front-admin-login/classe_trocada/harness/r3` | `button.btn-primary` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,376 | 1 | 5,6 |
| `front-admin-login/classe_trocada/harness/r4` | `button.btn-primary` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,399 | 1 | 5,7 |
| `front-admin-login/classe_trocada/harness/r5` | `button.btn-primary` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,384 | 1 | 5,6 |
| `front-admin-login/classe_trocada/php/r1` | `button.btn-primary` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,414 | 1 | 5,6 |
| `front-admin-login/classe_trocada/php/r2` | `button.btn-primary` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,393 | 1 | 5,6 |
| `front-admin-login/classe_trocada/php/r3` | `button.btn-primary` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,404 | 1 | 5,6 |
| `front-admin-login/classe_trocada/php/r4` | `button.btn-primary` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,390 | 1 | 5,6 |
| `front-admin-login/classe_trocada/php/r5` | `button.btn-primary` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,407 | 1 | 5,7 |
| `front-admin-login/texto_alterado/harness/r1` | `role=button[name="Entrar"]` | sim | 4 | sim | `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | sim |  | 0,355 | 1 | 5,6 |
| `front-admin-login/texto_alterado/harness/r2` | `role=button[name="Entrar"]` | sim | 4 | sim | `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | sim |  | 0,406 | 1 | 5,6 |
| `front-admin-login/texto_alterado/harness/r3` | `role=button[name="Entrar"]` | sim | 4 | sim | `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | sim |  | 0,372 | 1 | 5,6 |
| `front-admin-login/texto_alterado/harness/r4` | `role=button[name="Entrar"]` | sim | 4 | sim | `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | sim |  | 0,407 | 1 | 5,7 |
| `front-admin-login/texto_alterado/harness/r5` | `role=button[name="Entrar"]` | sim | 4 | sim | `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | sim |  | 0,373 | 1 | 5,6 |
| `front-admin-login/texto_alterado/php/r1` | `role=button[name="Entrar"]` | sim | 4 | sim | `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | sim |  | 0,405 | 1 | 5,7 |
| `front-admin-login/texto_alterado/php/r2` | `role=button[name="Entrar"]` | sim | 4 | sim | `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | sim |  | 0,371 | 1 | 5,6 |
| `front-admin-login/texto_alterado/php/r3` | `role=button[name="Entrar"]` | sim | 4 | sim | `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | sim |  | 0,448 | 1 | 5,7 |
| `front-admin-login/texto_alterado/php/r4` | `role=button[name="Entrar"]` | sim | 4 | sim | `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | sim |  | 0,391 | 1 | 5,6 |
| `front-admin-login/texto_alterado/php/r5` | `role=button[name="Entrar"]` | sim | 4 | sim | `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | sim |  | 0,356 | 1 | 5,6 |
| `front-admin-login/estrutura_alterada/harness/r1` | `.login-form form > button` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,401 | 1 | 5,6 |
| `front-admin-login/estrutura_alterada/harness/r2` | `.login-form form > button` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,407 | 1 | 5,6 |
| `front-admin-login/estrutura_alterada/harness/r3` | `.login-form form > button` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,378 | 1 | 5,6 |
| `front-admin-login/estrutura_alterada/harness/r4` | `.login-form form > button` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,383 | 1 | 5,6 |
| `front-admin-login/estrutura_alterada/harness/r5` | `.login-form form > button` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,400 | 1 | 5,6 |
| `front-admin-login/estrutura_alterada/php/r1` | `.login-form form > button` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,370 | 1 | 5,6 |
| `front-admin-login/estrutura_alterada/php/r2` | `.login-form form > button` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,390 | 1 | 5,6 |
| `front-admin-login/estrutura_alterada/php/r3` | `.login-form form > button` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,387 | 1 | 5,6 |
| `front-admin-login/estrutura_alterada/php/r4` | `.login-form form > button` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,433 | 1 | 5,7 |
| `front-admin-login/estrutura_alterada/php/r5` | `.login-form form > button` | sim | 4 | sim | `papel_e_nome` | `role=button[name="Entrar"]` | sim |  | 0,403 | 1 | 5,7 |
| `front-admin-produtos/id_renomeado/harness/r1` | `button[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,745 | 1 | 6,3 |
| `front-admin-produtos/id_renomeado/harness/r2` | `button[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,793 | 1 | 6,3 |
| `front-admin-produtos/id_renomeado/harness/r3` | `button[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,772 | 1 | 6,3 |
| `front-admin-produtos/id_renomeado/harness/r4` | `button[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,792 | 1 | 6,3 |
| `front-admin-produtos/id_renomeado/harness/r5` | `button[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,746 | 1 | 6,3 |
| `front-admin-produtos/id_renomeado/php/r1` | `button[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,776 | 1 | 6,3 |
| `front-admin-produtos/id_renomeado/php/r2` | `button[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,887 | 1 | 6,4 |
| `front-admin-produtos/id_renomeado/php/r3` | `button[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,791 | 1 | 6,4 |
| `front-admin-produtos/id_renomeado/php/r4` | `button[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,746 | 1 | 6,3 |
| `front-admin-produtos/id_renomeado/php/r5` | `button[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,825 | 1 | 6,4 |
| `front-admin-produtos/classe_trocada/harness/r1` | `button.delete[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,746 | 1 | 6,3 |
| `front-admin-produtos/classe_trocada/harness/r2` | `button.delete[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,793 | 1 | 6,3 |
| `front-admin-produtos/classe_trocada/harness/r3` | `button.delete[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,746 | 1 | 6,3 |
| `front-admin-produtos/classe_trocada/harness/r4` | `button.delete[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,777 | 1 | 6,3 |
| `front-admin-produtos/classe_trocada/harness/r5` | `button.delete[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,779 | 1 | 6,3 |
| `front-admin-produtos/classe_trocada/php/r1` | `button.delete[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,746 | 1 | 6,3 |
| `front-admin-produtos/classe_trocada/php/r2` | `button.delete[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,776 | 1 | 6,3 |
| `front-admin-produtos/classe_trocada/php/r3` | `button.delete[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,761 | 1 | 6,2 |
| `front-admin-produtos/classe_trocada/php/r4` | `button.delete[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,824 | 1 | 6,4 |
| `front-admin-produtos/classe_trocada/php/r5` | `button.delete[data-id='1']` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,802 | 1 | 6,4 |
| `front-admin-produtos/texto_alterado/harness/r1` | `role=button[name=/EXCLUIR$/] >> nth=0` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | sim |  | 0,747 | 1 | 6,3 |
| `front-admin-produtos/texto_alterado/harness/r2` | `role=button[name=/EXCLUIR$/] >> nth=0` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | sim |  | 0,773 | 1 | 6,3 |
| `front-admin-produtos/texto_alterado/harness/r3` | `role=button[name=/EXCLUIR$/] >> nth=0` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | sim |  | 0,754 | 1 | 6,3 |
| `front-admin-produtos/texto_alterado/harness/r4` | `role=button[name=/EXCLUIR$/] >> nth=0` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | sim |  | 0,775 | 1 | 6,3 |
| `front-admin-produtos/texto_alterado/harness/r5` | `role=button[name=/EXCLUIR$/] >> nth=0` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | sim |  | 0,747 | 1 | 6,2 |
| `front-admin-produtos/texto_alterado/php/r1` | `role=button[name=/EXCLUIR$/] >> nth=0` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | sim |  | 0,774 | 1 | 6,4 |
| `front-admin-produtos/texto_alterado/php/r2` | `role=button[name=/EXCLUIR$/] >> nth=0` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | sim |  | 0,780 | 1 | 6,3 |
| `front-admin-produtos/texto_alterado/php/r3` | `role=button[name=/EXCLUIR$/] >> nth=0` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | sim |  | 0,774 | 1 | 6,4 |
| `front-admin-produtos/texto_alterado/php/r4` | `role=button[name=/EXCLUIR$/] >> nth=0` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | sim |  | 0,770 | 1 | 6,3 |
| `front-admin-produtos/texto_alterado/php/r5` | `role=button[name=/EXCLUIR$/] >> nth=0` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name=" EXCLUIR ITEM"] >> nth=0` | sim |  | 0,762 | 1 | 6,3 |
| `front-admin-produtos/estrutura_alterada/harness/r1` | `table.table tbody tr:first-child td:last-child > button` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,777 | 1 | 6,3 |
| `front-admin-produtos/estrutura_alterada/harness/r2` | `table.table tbody tr:first-child td:last-child > button` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,810 | 1 | 6,4 |
| `front-admin-produtos/estrutura_alterada/harness/r3` | `table.table tbody tr:first-child td:last-child > button` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,741 | 1 | 6,3 |
| `front-admin-produtos/estrutura_alterada/harness/r4` | `table.table tbody tr:first-child td:last-child > button` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,808 | 1 | 6,4 |
| `front-admin-produtos/estrutura_alterada/harness/r5` | `table.table tbody tr:first-child td:last-child > button` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,796 | 1 | 6,3 |
| `front-admin-produtos/estrutura_alterada/php/r1` | `table.table tbody tr:first-child td:last-child > button` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,755 | 1 | 6,3 |
| `front-admin-produtos/estrutura_alterada/php/r2` | `table.table tbody tr:first-child td:last-child > button` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,787 | 1 | 6,3 |
| `front-admin-produtos/estrutura_alterada/php/r3` | `table.table tbody tr:first-child td:last-child > button` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,787 | 1 | 6,4 |
| `front-admin-produtos/estrutura_alterada/php/r4` | `table.table tbody tr:first-child td:last-child > button` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,754 | 1 | 6,3 |
| `front-admin-produtos/estrutura_alterada/php/r5` | `table.table tbody tr:first-child td:last-child > button` | sim | 10 | sim | `papel_e_nome` | `role=button[name=" EXCLUIR"] >> nth=0` | sim |  | 0,789 | 1 | 6,3 |
| `front-cliente-reserva/id_renomeado/harness/r1` | `#enviar` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,705 | 1 | 6,9 |
| `front-cliente-reserva/id_renomeado/harness/r2` | `#enviar` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,766 | 1 | 6,9 |
| `front-cliente-reserva/id_renomeado/harness/r3` | `#enviar` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,735 | 1 | 6,9 |
| `front-cliente-reserva/id_renomeado/harness/r4` | `#enviar` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,711 | 1 | 6,9 |
| `front-cliente-reserva/id_renomeado/harness/r5` | `#enviar` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,737 | 1 | 6,9 |
| `front-cliente-reserva/id_renomeado/php/r1` | `#enviar` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,671 | 1 | 6,8 |
| `front-cliente-reserva/id_renomeado/php/r2` | `#enviar` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,689 | 1 | 6,9 |
| `front-cliente-reserva/id_renomeado/php/r3` | `#enviar` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,730 | 1 | 6,9 |
| `front-cliente-reserva/id_renomeado/php/r4` | `#enviar` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,706 | 1 | 6,8 |
| `front-cliente-reserva/id_renomeado/php/r5` | `#enviar` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,686 | 1 | 6,8 |
| `front-cliente-reserva/classe_trocada/harness/r1` | `#reserva_login input.btn-danger` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,721 | 1 | 6,8 |
| `front-cliente-reserva/classe_trocada/harness/r2` | `#reserva_login input.btn-danger` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,715 | 1 | 6,8 |
| `front-cliente-reserva/classe_trocada/harness/r3` | `#reserva_login input.btn-danger` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,754 | 1 | 7,0 |
| `front-cliente-reserva/classe_trocada/harness/r4` | `#reserva_login input.btn-danger` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,786 | 1 | 7,0 |
| `front-cliente-reserva/classe_trocada/harness/r5` | `#reserva_login input.btn-danger` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,754 | 1 | 6,9 |
| `front-cliente-reserva/classe_trocada/php/r1` | `#reserva_login input.btn-danger` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,743 | 1 | 6,8 |
| `front-cliente-reserva/classe_trocada/php/r2` | `#reserva_login input.btn-danger` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,707 | 1 | 6,9 |
| `front-cliente-reserva/classe_trocada/php/r3` | `#reserva_login input.btn-danger` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,640 | 1 | 6,8 |
| `front-cliente-reserva/classe_trocada/php/r4` | `#reserva_login input.btn-danger` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,671 | 1 | 6,8 |
| `front-cliente-reserva/classe_trocada/php/r5` | `#reserva_login input.btn-danger` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,714 | 1 | 6,9 |
| `front-cliente-reserva/texto_alterado/harness/r1` | `input[value="Reservar"]` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name="Reservar mesa"]` | sim |  | 0,719 | 1 | 6,8 |
| `front-cliente-reserva/texto_alterado/harness/r2` | `input[value="Reservar"]` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name="Reservar mesa"]` | sim |  | 0,728 | 1 | 6,8 |
| `front-cliente-reserva/texto_alterado/harness/r3` | `input[value="Reservar"]` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name="Reservar mesa"]` | sim |  | 0,886 | 1 | 7,0 |
| `front-cliente-reserva/texto_alterado/harness/r4` | `input[value="Reservar"]` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name="Reservar mesa"]` | sim |  | 0,734 | 1 | 6,9 |
| `front-cliente-reserva/texto_alterado/harness/r5` | `input[value="Reservar"]` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name="Reservar mesa"]` | sim |  | 0,771 | 1 | 6,9 |
| `front-cliente-reserva/texto_alterado/php/r1` | `input[value="Reservar"]` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name="Reservar mesa"]` | sim |  | 0,683 | 1 | 6,8 |
| `front-cliente-reserva/texto_alterado/php/r2` | `input[value="Reservar"]` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name="Reservar mesa"]` | sim |  | 0,774 | 1 | 7,0 |
| `front-cliente-reserva/texto_alterado/php/r3` | `input[value="Reservar"]` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name="Reservar mesa"]` | sim |  | 0,666 | 1 | 6,8 |
| `front-cliente-reserva/texto_alterado/php/r4` | `input[value="Reservar"]` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name="Reservar mesa"]` | sim |  | 0,781 | 1 | 6,9 |
| `front-cliente-reserva/texto_alterado/php/r5` | `input[value="Reservar"]` | sim | 10 | sim | `papel_e_nome_parecido` | `role=button[name="Reservar mesa"]` | sim |  | 0,708 | 1 | 6,9 |
| `front-cliente-reserva/estrutura_alterada/harness/r1` | `#reserva_login > input[type=submit]` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,641 | 1 | 6,7 |
| `front-cliente-reserva/estrutura_alterada/harness/r2` | `#reserva_login > input[type=submit]` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,822 | 1 | 7,0 |
| `front-cliente-reserva/estrutura_alterada/harness/r3` | `#reserva_login > input[type=submit]` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,674 | 1 | 7,0 |
| `front-cliente-reserva/estrutura_alterada/harness/r4` | `#reserva_login > input[type=submit]` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,763 | 1 | 6,9 |
| `front-cliente-reserva/estrutura_alterada/harness/r5` | `#reserva_login > input[type=submit]` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,711 | 1 | 6,9 |
| `front-cliente-reserva/estrutura_alterada/php/r1` | `#reserva_login > input[type=submit]` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,694 | 1 | 6,8 |
| `front-cliente-reserva/estrutura_alterada/php/r2` | `#reserva_login > input[type=submit]` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,711 | 1 | 6,8 |
| `front-cliente-reserva/estrutura_alterada/php/r3` | `#reserva_login > input[type=submit]` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,638 | 1 | 6,8 |
| `front-cliente-reserva/estrutura_alterada/php/r4` | `#reserva_login > input[type=submit]` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,739 | 1 | 6,9 |
| `front-cliente-reserva/estrutura_alterada/php/r5` | `#reserva_login > input[type=submit]` | sim | 10 | sim | `papel_e_nome` | `role=button[name="Reservar"]` | sim |  | 0,663 | 1 | 6,7 |
<!-- /tabela:tb_f4_cura_execucoes -->
