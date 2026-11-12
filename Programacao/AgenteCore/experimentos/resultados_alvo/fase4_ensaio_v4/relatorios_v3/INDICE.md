<!-- ! Alteração de IA - Revisar: índice DERIVADO, gerado por gerar_relatorio_raciocinio.gerar_v3_da_pasta; não editar à mão.
     ! Motivo: um relatório por caso é ilegível sem uma lista que diga a causa, a confiança e o campo de cada um; os relatórios v2 da corrida ficam como estavam. -->
# Relatórios de defeito (v3) da corrida `fase4_ensaio_v4`

10 relatórios no molde da seção 5.5 do CTFL 4.0, gerados da trilha `trilha_cenarios.jsonl` (modo `cenarios`). Severidade, prioridade e estado estão em branco em todos: são do analista.

| Relatório | Título | Causa respondida | Confiança | Campo | Classe e nível |
|---|---|---|---|---|---|
| [`contrato-malformed_json__r1`](contrato-malformed_json__r1.md) | Resposta truncada em `GET /api/produtos` | `resposta_truncada` | o agente está seguro desta causa | nenhum | classe 1, nível 1 |
| [`contrato-field_missing__r1`](contrato-field_missing__r1.md) | Campo ausente em `GET /api/produtos`, campo `preco` | `campo_ausente` | o agente está seguro desta causa | `preco` | classe 2, nível 1 |
| [`contrato-field_renamed__r1`](contrato-field_renamed__r1.md) | Campo renomeado em `GET /api/produtos`, campo `preco` | `campo_renomeado` | o agente está seguro desta causa | `preco` | classe 2, nível 2 |
| [`contrato-type_drift__r1`](contrato-type_drift__r1.md) | Tipo divergente em `GET /api/produtos`, campo `preco` | `tipo_divergente` | o agente está seguro desta causa | `preco` | classe 3, nível 2 |
| [`contrato-escala_ou_unidade_errada__r1`](contrato-escala_ou_unidade_errada__r1.md) | Escala ou unidade errada em `GET /api/produtos`, campo `preco` | `escala_ou_unidade_errada` | o agente tem dúvida entre causas vizinhas; confira antes de agir | `preco` | classe 4, nível 2 |
| [`contrato-error_500__r1`](contrato-error_500__r1.md) | Erro interno do servidor (500) em `GET /api/produtos` | `erro_interno_do_servidor` | o agente está seguro desta causa | nenhum | classe 5, nível 1 |
| [`localizador-front-busca__r1`](localizador-front-busca__r1.md) | Localizador (seletor) quebrado no passo 2 do roteiro `front-busca` (localizador `#buscar`), curado pelo agente | `localizador_quebrado` | o agente tem dúvida entre causas vizinhas; confira antes de agir | nenhum | não declarados |
| [`localizador-front-admin-login__r1`](localizador-front-admin-login__r1.md) | Localizador (seletor) quebrado no passo 5 do roteiro `front-admin-login` (localizador `button.btn-primary`), curado pelo agente | `localizador_quebrado` | o agente tem dúvida entre causas vizinhas; confira antes de agir | nenhum | não declarados |
| [`localizador-front-admin-produtos__r1`](localizador-front-admin-produtos__r1.md) | Localizador (seletor) quebrado no passo 11 do roteiro `front-admin-produtos` (localizador `role=button[name=/EXCLUIR$/] >> nth=0`), curado pelo agente | `localizador_quebrado` | o agente está seguro desta causa | nenhum | não declarados |
| [`localizador-front-cliente-reserva__r1`](localizador-front-cliente-reserva__r1.md) | Localizador (seletor) quebrado no passo 11 do roteiro `front-cliente-reserva` (localizador `#reserva_login > input[type=submit]`), curado pelo agente | `localizador_quebrado` | o agente está seguro desta causa | nenhum | não declarados |
