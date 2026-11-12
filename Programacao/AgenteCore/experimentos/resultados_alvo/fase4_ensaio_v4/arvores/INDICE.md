<!-- ! Alteração de IA - Revisar: índice DERIVADO, gerado por arvore_de_decisao.gerar_da_pasta (Pós-Fase 4, pacote Q3); não editar à mão.
     ! Motivo: uma árvore por caso é ilegível sem a lista que diga a causa, a confiança, a divergência e a cura de cada uma; os outros arquivos da corrida ficam como estavam. -->
# Árvores de decisão da corrida `fase4_ensaio_v4`

10 árvores geradas da trilha `trilha_cenarios.jsonl` (modo `cenarios`): 4 com divergência entre o declarado e o conferido, 4 com cura de localizador; 309 afirmações (221 observado, 54 conferido, 30 declarado, 4 desconhecido). A coluna das afirmações conta observado/conferido/declarado/desconhecido. Filtros de texto do pacote Q2: 10 de 10 árvores passam em tudo.

| Árvore | Caso | Causa escolhida | Confiança | Divergência | Cura | Afirmações por origem | Filtros de texto |
|---|---|---|---|---|---|---|---|
| [`contrato-malformed_json__r1`](contrato-malformed_json__r1.md) | `contrato-malformed_json#1` | `resposta_truncada` | alta | não | não | 21/5/3/0 | passa |
| [`contrato-field_missing__r1`](contrato-field_missing__r1.md) | `contrato-field_missing#1` | `campo_ausente` | alta | não | não | 21/6/3/0 | passa |
| [`contrato-field_renamed__r1`](contrato-field_renamed__r1.md) | `contrato-field_renamed#1` | `campo_renomeado` | alta | não | não | 21/6/3/0 | passa |
| [`contrato-type_drift__r1`](contrato-type_drift__r1.md) | `contrato-type_drift#1` | `tipo_divergente` | alta | não | não | 21/6/3/0 | passa |
| [`contrato-escala_ou_unidade_errada__r1`](contrato-escala_ou_unidade_errada__r1.md) | `contrato-escala_ou_unidade_errada#1` | `escala_ou_unidade_errada` | média | não | não | 21/6/3/0 | passa |
| [`contrato-error_500__r1`](contrato-error_500__r1.md) | `contrato-error_500#1` | `erro_interno_do_servidor` | alta | não | não | 21/5/3/0 | passa |
| [`localizador-front-busca__r1`](localizador-front-busca__r1.md) | `localizador-front-busca#1` | `localizador_quebrado` | média | sim | sim | 23/5/3/1 | passa |
| [`localizador-front-admin-login__r1`](localizador-front-admin-login__r1.md) | `localizador-front-admin-login#1` | `localizador_quebrado` | média | sim | sim | 24/5/3/1 | passa |
| [`localizador-front-admin-produtos__r1`](localizador-front-admin-produtos__r1.md) | `localizador-front-admin-produtos#1` | `localizador_quebrado` | alta | sim | sim | 24/5/3/1 | passa |
| [`localizador-front-cliente-reserva__r1`](localizador-front-cliente-reserva__r1.md) | `localizador-front-cliente-reserva#1` | `localizador_quebrado` | alta | sim | sim | 24/5/3/1 | passa |
