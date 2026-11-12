<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por impacto_git.py --prova a partir de git log e git diff --name-only do repositório, biblioteca_producao/ e cenarios_fase4.py (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Seleção de cenários pelo diff do Git: a prova sobre o histórico do repositório (Pós-Fase 4, pacote Q4), gerada em 2026-11-08

O mapa liga 6 cenários base (10 do ensaio da Fase 5) e 39 verbetes (38 com `arquivos:`, 24 com `endpoints:`) a 33 arquivos da aplicação. Nos 7 pares de commits consecutivos que mexeram nas cobaias, a seleção rodaria tudo em 2, parte dos cenários em 3 e nada em 2; 21 cenários ficaram registrados como deixados de fora, para a conferência contra a rodada completa.

## As três regras

- **fora_do_mapa_roda_tudo**: arquivo da aplicação que nenhum cenário nem verbete declara dispara a rodada completa, nunca nada (Azure DevOps TIA: arquivo que o mapa não entende roda tudo; Rothermel e Harrold, 1997: na dúvida, selecionar a mais)
- **rodada_completa_periodica**: a seleção não substitui a rodada completa: ela continua em periodicidade fixa, e também quando nenhum arquivo da aplicação mudou (Azure DevOps TIA: rodada completa configurada, recomendada)
- **conferencia_contra_a_rodada_completa**: cada seleção registra os cenários que deixou de rodar, e a rodada completa seguinte confere se algum deles falhou (Azure DevOps TIA: comparar T1, os selecionados, com T2, todos)

## A seleção par a par

<!-- tabela:tb_f4_impacto_pares -->
| Commit testado | Commit atual | Data | Assunto | Alterados | Fora da aplicação | Ignorados | No mapa | Fora do mapa | Veredito | Cenários selecionados | Deixados de fora |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `e854a0eb` | `ab4da6a1` | 2026-08-31 | Estrutura Base Auxiliada por IA - Claude - PT1 | 3873 | 10 | 3844 | 14 | 5 | roda tudo | api-catalogo, api-detalhe, front-admin-login, front-admin-produtos, front-busca, front-cliente-reserva | nenhum |
| `ab4da6a1` | `26432d2c` | 2026-08-31 | Parte 2 | 1762 | 10 | 1752 | 0 | 0 | nada a rodar | nenhum | api-catalogo, api-detalhe, front-admin-login, front-admin-produtos, front-busca, front-cliente-reserva |
| `26432d2c` | `084fce09` | 2026-09-01 | Correção comentários e nomenclatura normalizada | 21 | 8 | 1 | 9 | 3 | roda tudo | api-catalogo, api-detalhe, front-admin-login, front-admin-produtos, front-busca, front-cliente-reserva | nenhum |
| `084fce09` | `603c423e` | 2026-09-03 | Teste 1 Concluído, resultados, relatórios e refatoração geral + refatoração da documentação + inicio da preparaçãod a fase 2 de testes | 106 | 102 | 1 | 3 | 0 | seleção parcial | api-catalogo | api-detalhe, front-admin-login, front-admin-produtos, front-busca, front-cliente-reserva |
| `603c423e` | `3e8cfc14` | 2026-10-23 | Ajuste de gitignore com retirada de informações da venv e continuações das pesquisas pré fase 4 | 4381 | 2269 | 2112 | 0 | 0 | nada a rodar | nenhum | api-catalogo, api-detalhe, front-admin-login, front-admin-produtos, front-busca, front-cliente-reserva |
| `3e8cfc14` | `4f3b3e26` | 2026-10-27 | Fase 4 - Inicialização | 240 | 237 | 1 | 2 | 0 | seleção parcial | api-catalogo, api-detalhe | front-admin-login, front-admin-produtos, front-busca, front-cliente-reserva |
| `4f3b3e26` | `633ebb27` | 2026-11-03 | Fase 4 - Inicio das rodadas + ajustes de parâmetros | 555 | 550 | 0 | 5 | 0 | seleção parcial | api-catalogo, api-detalhe, front-admin-login, front-admin-produtos, front-busca, front-cliente-reserva | nenhum |
<!-- /tabela:tb_f4_impacto_pares -->

## Por que, em cada par

### `e854a0eb` para `ab4da6a1` (2026-08-31): roda tudo

roda tudo: 5 arquivo(s) da aplicação fora do mapa (Programacao/CobaiaAPI/app/__init__.py, Programacao/CobaiaAPI/app/routers/__init__.py, Programacao/CobaiaAPI/pyproject.toml e mais 2); regra 1, arquivo fora do mapa roda tudo, nunca nada.

- `Programacao/CobaiaAPI/.env.example`: no mapa; no mapa: cenários nenhum; verbetes modos-de-injecao
- `Programacao/CobaiaAPI/app/__init__.py`: fora do mapa; arquivo da aplicação que nenhum cenário nem verbete declara: pela regra 1, roda tudo
- `Programacao/CobaiaAPI/app/config.py`: no mapa; no mapa: cenários nenhum; verbetes codificacao_incorreta
- `Programacao/CobaiaAPI/app/database.py`: no mapa; no mapa: cenários api-catalogo; verbetes dado_desatualizado
- `Programacao/CobaiaAPI/app/fault_injection.py`: no mapa; no mapa: cenários api-catalogo; verbetes campo_ausente, campo_renomeado, erro_interno_do_servidor, modos-de-injecao, resposta_truncada, tempo_de_resposta_excedido, tipo_divergente
- `Programacao/CobaiaAPI/app/main.py`: no mapa; no mapa: cenários api-catalogo; verbetes limite_de_requisicoes
- `Programacao/CobaiaAPI/app/models.py`: no mapa; no mapa: cenários api-catalogo, api-detalhe; verbetes chave_de_juncao_errada, entidade-produto, escala_ou_unidade_errada, novo_verbete, nulo_inesperado, usuario-e-login, valor_fora_do_dominio
- `Programacao/CobaiaAPI/app/routers/__init__.py`: fora do mapa; arquivo da aplicação que nenhum cenário nem verbete declara: pela regra 1, roda tudo
- `Programacao/CobaiaAPI/app/routers/admin_fault.py`: no mapa; no mapa: cenários api-detalhe; verbetes mensagens-de-erro-do-codigo, modos-de-injecao, recurso_inexistente
- `Programacao/CobaiaAPI/app/routers/pedidos.py`: no mapa; no mapa: cenários api-catalogo, api-detalhe; verbetes chave_de_juncao_errada, contrato-pedido, dado_desatualizado, escala_ou_unidade_errada, fluxo-reserva-e-cancelamento, formato_de_data_divergente, mensagens-de-erro-do-codigo, pedido-reserva, recurso_inexistente, registro_duplicado
- `Programacao/CobaiaAPI/app/routers/produtos.py`: no mapa; no mapa: cenários api-catalogo, api-detalhe; verbetes colecao_no_lugar_de_objeto, contagem_inconsistente, contrato-produto, entidade-produto, erro_interno_do_servidor, escala_ou_unidade_errada, limites-do-sistema, localizador_quebrado, mensagens-de-erro-do-codigo, nulo_inesperado, recurso_inexistente, resposta_truncada, tipo_divergente
- `Programacao/CobaiaAPI/app/schemas.py`: no mapa; no mapa: cenários api-catalogo, api-detalhe; verbetes campo_renomeado, contrato-pedido, contrato-produto, estrutura_aninhada_divergente, formato_de_data_divergente, limites-do-sistema
- `Programacao/CobaiaAPI/pyproject.toml`: fora do mapa; arquivo da aplicação que nenhum cenário nem verbete declara: pela regra 1, roda tudo
- `Programacao/CobaiaAPI/requirements-dev.txt`: fora do mapa; arquivo da aplicação que nenhum cenário nem verbete declara: pela regra 1, roda tudo
- `Programacao/CobaiaAPI/requirements.txt`: fora do mapa; arquivo da aplicação que nenhum cenário nem verbete declara: pela regra 1, roda tudo
- `Programacao/CobaiaFront/banco/schema_completo.sql`: no mapa; no mapa: cenários api-catalogo; verbetes codificacao_incorreta, nulo_inesperado, pedido-reserva, valor_fora_do_dominio
- `Programacao/CobaiaFront/banco/seed.sql`: no mapa; no mapa: cenários api-catalogo, api-detalhe; verbetes entidade-produto
- `Programacao/CobaiaFront/menu_publico.php`: no mapa; no mapa: cenários api-catalogo, api-detalhe, front-busca; verbetes nenhum
- `Programacao/CobaiaFront/produtos_api.php`: no mapa; no mapa: cenários api-catalogo, api-detalhe; verbetes atualizacao-da-tela, campo_ausente, colecao_no_lugar_de_objeto, corpo_nao_e_json, corpo_vazio, estado_da_tela_divergente, estrutura_aninhada_divergente, limite_de_requisicoes, localizador_quebrado, mensagens-de-erro-do-codigo, pagina-produtos-api, tempo_de_resposta_excedido, tipo_divergente

Verbetes atingidos: `atualizacao-da-tela` (1 arquivo(s)); `campo_ausente` (2 arquivo(s)); `campo_renomeado` (2 arquivo(s)); `chave_de_juncao_errada` (2 arquivo(s)); `codificacao_incorreta` (2 arquivo(s)); `colecao_no_lugar_de_objeto` (2 arquivo(s)); `contagem_inconsistente` (1 arquivo(s)); `contrato-pedido` (2 arquivo(s)); `contrato-produto` (2 arquivo(s)); `corpo_nao_e_json` (1 arquivo(s)); `corpo_vazio` (1 arquivo(s)); `dado_desatualizado` (2 arquivo(s)); `entidade-produto` (3 arquivo(s)); `erro_interno_do_servidor` (2 arquivo(s)); `escala_ou_unidade_errada` (3 arquivo(s)); `estado_da_tela_divergente` (1 arquivo(s)); `estrutura_aninhada_divergente` (2 arquivo(s)); `fluxo-reserva-e-cancelamento` (1 arquivo(s)); `formato_de_data_divergente` (2 arquivo(s)); `limite_de_requisicoes` (2 arquivo(s)); `limites-do-sistema` (2 arquivo(s)); `localizador_quebrado` (2 arquivo(s)); `mensagens-de-erro-do-codigo` (4 arquivo(s)); `modos-de-injecao` (3 arquivo(s)); `novo_verbete` (1 arquivo(s)); `nulo_inesperado` (3 arquivo(s)); `pagina-produtos-api` (1 arquivo(s)); `pedido-reserva` (2 arquivo(s)); `recurso_inexistente` (3 arquivo(s)); `registro_duplicado` (1 arquivo(s)); `resposta_truncada` (2 arquivo(s)); `tempo_de_resposta_excedido` (2 arquivo(s)); `tipo_divergente` (3 arquivo(s)); `usuario-e-login` (1 arquivo(s)); `valor_fora_do_dominio` (2 arquivo(s)).

Cenários do ensaio a rodar: contrato-error_500, contrato-escala_ou_unidade_errada, contrato-field_missing, contrato-field_renamed, contrato-malformed_json, contrato-type_drift, localizador-front-admin-login, localizador-front-admin-produtos, localizador-front-busca, localizador-front-cliente-reserva.

### `ab4da6a1` para `26432d2c` (2026-08-31): nada a rodar

nenhum arquivo da aplicação no mapa mudou (10 fora da aplicação, 1752 ignorados): nada a rodar pela seleção; vale a rodada completa periódica (regra 2).


### `26432d2c` para `084fce09` (2026-09-01): roda tudo

roda tudo: 3 arquivo(s) da aplicação fora do mapa (Programacao/CobaiaAPI/pyproject.toml, Programacao/CobaiaAPI/requirements-dev.txt, Programacao/CobaiaAPI/requirements.txt); regra 1, arquivo fora do mapa roda tudo, nunca nada.

- `Programacao/CobaiaAPI/.env.example`: no mapa; no mapa: cenários nenhum; verbetes modos-de-injecao
- `Programacao/CobaiaAPI/app/config.py`: no mapa; no mapa: cenários nenhum; verbetes codificacao_incorreta
- `Programacao/CobaiaAPI/app/database.py`: no mapa; no mapa: cenários api-catalogo; verbetes dado_desatualizado
- `Programacao/CobaiaAPI/app/main.py`: no mapa; no mapa: cenários api-catalogo; verbetes limite_de_requisicoes
- `Programacao/CobaiaAPI/app/routers/admin_fault.py`: no mapa; no mapa: cenários api-detalhe; verbetes mensagens-de-erro-do-codigo, modos-de-injecao, recurso_inexistente
- `Programacao/CobaiaAPI/app/routers/pedidos.py`: no mapa; no mapa: cenários api-catalogo, api-detalhe; verbetes chave_de_juncao_errada, contrato-pedido, dado_desatualizado, escala_ou_unidade_errada, fluxo-reserva-e-cancelamento, formato_de_data_divergente, mensagens-de-erro-do-codigo, pedido-reserva, recurso_inexistente, registro_duplicado
- `Programacao/CobaiaAPI/app/routers/produtos.py`: no mapa; no mapa: cenários api-catalogo, api-detalhe; verbetes colecao_no_lugar_de_objeto, contagem_inconsistente, contrato-produto, entidade-produto, erro_interno_do_servidor, escala_ou_unidade_errada, limites-do-sistema, localizador_quebrado, mensagens-de-erro-do-codigo, nulo_inesperado, recurso_inexistente, resposta_truncada, tipo_divergente
- `Programacao/CobaiaAPI/pyproject.toml`: fora do mapa; arquivo da aplicação que nenhum cenário nem verbete declara: pela regra 1, roda tudo
- `Programacao/CobaiaAPI/requirements-dev.txt`: fora do mapa; arquivo da aplicação que nenhum cenário nem verbete declara: pela regra 1, roda tudo
- `Programacao/CobaiaAPI/requirements.txt`: fora do mapa; arquivo da aplicação que nenhum cenário nem verbete declara: pela regra 1, roda tudo
- `Programacao/CobaiaFront/menu_publico.php`: no mapa; no mapa: cenários api-catalogo, api-detalhe, front-busca; verbetes nenhum
- `Programacao/CobaiaFront/produtos_api.php`: no mapa; no mapa: cenários api-catalogo, api-detalhe; verbetes atualizacao-da-tela, campo_ausente, colecao_no_lugar_de_objeto, corpo_nao_e_json, corpo_vazio, estado_da_tela_divergente, estrutura_aninhada_divergente, limite_de_requisicoes, localizador_quebrado, mensagens-de-erro-do-codigo, pagina-produtos-api, tempo_de_resposta_excedido, tipo_divergente

Verbetes atingidos: `atualizacao-da-tela` (1 arquivo(s)); `campo_ausente` (1 arquivo(s)); `chave_de_juncao_errada` (1 arquivo(s)); `codificacao_incorreta` (1 arquivo(s)); `colecao_no_lugar_de_objeto` (2 arquivo(s)); `contagem_inconsistente` (1 arquivo(s)); `contrato-pedido` (1 arquivo(s)); `contrato-produto` (1 arquivo(s)); `corpo_nao_e_json` (1 arquivo(s)); `corpo_vazio` (1 arquivo(s)); `dado_desatualizado` (2 arquivo(s)); `entidade-produto` (1 arquivo(s)); `erro_interno_do_servidor` (1 arquivo(s)); `escala_ou_unidade_errada` (2 arquivo(s)); `estado_da_tela_divergente` (1 arquivo(s)); `estrutura_aninhada_divergente` (1 arquivo(s)); `fluxo-reserva-e-cancelamento` (1 arquivo(s)); `formato_de_data_divergente` (1 arquivo(s)); `limite_de_requisicoes` (2 arquivo(s)); `limites-do-sistema` (1 arquivo(s)); `localizador_quebrado` (2 arquivo(s)); `mensagens-de-erro-do-codigo` (4 arquivo(s)); `modos-de-injecao` (2 arquivo(s)); `nulo_inesperado` (1 arquivo(s)); `pagina-produtos-api` (1 arquivo(s)); `pedido-reserva` (1 arquivo(s)); `recurso_inexistente` (3 arquivo(s)); `registro_duplicado` (1 arquivo(s)); `resposta_truncada` (1 arquivo(s)); `tempo_de_resposta_excedido` (1 arquivo(s)); `tipo_divergente` (2 arquivo(s)).

Cenários do ensaio a rodar: contrato-error_500, contrato-escala_ou_unidade_errada, contrato-field_missing, contrato-field_renamed, contrato-malformed_json, contrato-type_drift, localizador-front-admin-login, localizador-front-admin-produtos, localizador-front-busca, localizador-front-cliente-reserva.

### `084fce09` para `603c423e` (2026-09-03): seleção parcial

seleção parcial: 1 de 6 cenários, pelos arquivos no mapa; os 5 deixados de fora ficam registrados para a conferência contra a rodada completa (regra 3).

- `Programacao/CobaiaAPI/.env.example`: no mapa; no mapa: cenários nenhum; verbetes modos-de-injecao
- `Programacao/CobaiaAPI/app/config.py`: no mapa; no mapa: cenários nenhum; verbetes codificacao_incorreta
- `Programacao/CobaiaAPI/app/fault_injection.py`: no mapa; no mapa: cenários api-catalogo; verbetes campo_ausente, campo_renomeado, erro_interno_do_servidor, modos-de-injecao, resposta_truncada, tempo_de_resposta_excedido, tipo_divergente

Verbetes atingidos: `campo_ausente` (1 arquivo(s)); `campo_renomeado` (1 arquivo(s)); `codificacao_incorreta` (1 arquivo(s)); `erro_interno_do_servidor` (1 arquivo(s)); `modos-de-injecao` (2 arquivo(s)); `resposta_truncada` (1 arquivo(s)); `tempo_de_resposta_excedido` (1 arquivo(s)); `tipo_divergente` (1 arquivo(s)).

Cenários do ensaio a rodar: contrato-error_500, contrato-escala_ou_unidade_errada, contrato-field_missing, contrato-field_renamed, contrato-malformed_json, contrato-type_drift.

### `603c423e` para `3e8cfc14` (2026-10-23): nada a rodar

nenhum arquivo da aplicação no mapa mudou (2269 fora da aplicação, 2112 ignorados): nada a rodar pela seleção; vale a rodada completa periódica (regra 2).


### `3e8cfc14` para `4f3b3e26` (2026-10-27): seleção parcial

seleção parcial: 2 de 6 cenários, pelos arquivos no mapa; os 4 deixados de fora ficam registrados para a conferência contra a rodada completa (regra 3).

- `Programacao/CobaiaAPI/app/fault_injection.py`: no mapa; no mapa: cenários api-catalogo; verbetes campo_ausente, campo_renomeado, erro_interno_do_servidor, modos-de-injecao, resposta_truncada, tempo_de_resposta_excedido, tipo_divergente
- `Programacao/CobaiaAPI/app/routers/produtos.py`: no mapa; no mapa: cenários api-catalogo, api-detalhe; verbetes colecao_no_lugar_de_objeto, contagem_inconsistente, contrato-produto, entidade-produto, erro_interno_do_servidor, escala_ou_unidade_errada, limites-do-sistema, localizador_quebrado, mensagens-de-erro-do-codigo, nulo_inesperado, recurso_inexistente, resposta_truncada, tipo_divergente

Verbetes atingidos: `campo_ausente` (1 arquivo(s)); `campo_renomeado` (1 arquivo(s)); `colecao_no_lugar_de_objeto` (1 arquivo(s)); `contagem_inconsistente` (1 arquivo(s)); `contrato-produto` (1 arquivo(s)); `entidade-produto` (1 arquivo(s)); `erro_interno_do_servidor` (2 arquivo(s)); `escala_ou_unidade_errada` (1 arquivo(s)); `limites-do-sistema` (1 arquivo(s)); `localizador_quebrado` (1 arquivo(s)); `mensagens-de-erro-do-codigo` (1 arquivo(s)); `modos-de-injecao` (1 arquivo(s)); `nulo_inesperado` (1 arquivo(s)); `recurso_inexistente` (1 arquivo(s)); `resposta_truncada` (2 arquivo(s)); `tempo_de_resposta_excedido` (1 arquivo(s)); `tipo_divergente` (2 arquivo(s)).

Cenários do ensaio a rodar: contrato-error_500, contrato-escala_ou_unidade_errada, contrato-field_missing, contrato-field_renamed, contrato-malformed_json, contrato-type_drift.

### `4f3b3e26` para `633ebb27` (2026-11-03): seleção parcial

seleção parcial: 6 de 6 cenários, pelos arquivos no mapa; os 0 deixados de fora ficam registrados para a conferência contra a rodada completa (regra 3).

- `Programacao/CobaiaFront/admin/login.php`: no mapa; no mapa: cenários front-admin-login, front-admin-produtos, front-cliente-reserva; verbetes senha-sem-hash, usuario-e-login
- `Programacao/CobaiaFront/admin/produtos_lista.php`: no mapa; no mapa: cenários front-admin-produtos; verbetes nenhum
- `Programacao/CobaiaFront/cliente/registrar_reserva.php`: no mapa; no mapa: cenários api-catalogo, front-cliente-reserva; verbetes consultas-sem-checagem, fluxo-reserva-e-cancelamento, registro_duplicado, valor_fora_do_dominio
- `Programacao/CobaiaFront/menu_publico.php`: no mapa; no mapa: cenários api-catalogo, api-detalhe, front-busca; verbetes nenhum
- `Programacao/CobaiaFront/quebra.php`: no mapa; no mapa: cenários api-catalogo, api-detalhe, front-admin-login, front-admin-produtos, front-busca, front-cliente-reserva; verbetes nenhum

Verbetes atingidos: `consultas-sem-checagem` (1 arquivo(s)); `fluxo-reserva-e-cancelamento` (1 arquivo(s)); `registro_duplicado` (1 arquivo(s)); `senha-sem-hash` (1 arquivo(s)); `usuario-e-login` (1 arquivo(s)); `valor_fora_do_dominio` (1 arquivo(s)).

Cenários do ensaio a rodar: contrato-error_500, contrato-escala_ou_unidade_errada, contrato-field_missing, contrato-field_renamed, contrato-malformed_json, contrato-type_drift, localizador-front-admin-login, localizador-front-admin-produtos, localizador-front-busca, localizador-front-cliente-reserva.

## O mapa dos cenários

<!-- tabela:tb_f4_impacto_cenarios -->
| Cenário | Cobaia | Página | Endpoint | Verbetes ligados pelo endpoint | Arquivos no mapa |
|---|---|---|---|---|---|
| api-catalogo | api | `produtos_api.php` | GET /api/produtos | campo_ausente, campo_renomeado, chave_de_juncao_errada, colecao_no_lugar_de_objeto, contagem_inconsistente, contrato-produto, dado_desatualizado, entidade-produto, erro_interno_do_servidor, escala_ou_unidade_errada, estrutura_aninhada_divergente, limite_de_requisicoes, nulo_inesperado, pagina-produtos-api, tempo_de_resposta_excedido, tipo_divergente, valor_fora_do_dominio | 17 |
| api-detalhe | api | `produtos_api.php` | GET /api/produtos/{id} | colecao_no_lugar_de_objeto, contrato-produto, entidade-produto, pagina-produtos-api, recurso_inexistente | 11 |
| front-busca | front | `index.php` | nenhum | nenhum | 8 |
| front-admin-login | front | `admin/login.php` | nenhum | nenhum | 3 |
| front-admin-produtos | front | `admin/produtos_lista.php` | nenhum | nenhum | 6 |
| front-cliente-reserva | front | `cliente/index.php` | nenhum | nenhum | 7 |
<!-- /tabela:tb_f4_impacto_cenarios -->

Fontes: Rothermel e Harrold (1997): seleção segura inclui todo teste capaz de expor falha no programa modificado; Gligoric, Eloussi e Marinov (2015), Ekstazi: dependência em nível de arquivo cortou o tempo de teste em 32% a 54%; Memon et al. (2017), Google TAP: os alvos que dependem dos arquivos modificados são a base da seleção; Azure DevOps, Test Impact Analysis: mapa à mão e aproximado (TIA.UserMapFile), arquivo desconhecido roda tudo, rodada completa periódica, T1 contra T2.
