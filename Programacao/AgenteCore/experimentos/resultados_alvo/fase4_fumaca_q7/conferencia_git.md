# Conferência da seleção pelo Git contra a rodada completa: `fase4_fumaca_q7` contra `fase5_agente_b`

A corrida `fase4_fumaca_q7` rodou 10 cenários e deixou 0 de fora. Falhas perdidas (cenário deixado de fora que não passou em todas as execuções da rodada completa `fase5_agente_b`): nenhuma. A seleção foi segura para esta mudança.

| Cenário | Na seleção | Rodada completa | Corrida selecionada | Situação |
|---|---|---|---|---|
| `contrato-error_500` | sim | 5 de 5 | 1 de 1 | rodou nas duas e o resultado é o mesmo |
| `contrato-escala_ou_unidade_errada` | sim | 5 de 5 | 1 de 1 | rodou nas duas e o resultado é o mesmo |
| `contrato-field_missing` | sim | 5 de 5 | 1 de 1 | rodou nas duas e o resultado é o mesmo |
| `contrato-field_renamed` | sim | 5 de 5 | 1 de 1 | rodou nas duas e o resultado é o mesmo |
| `contrato-malformed_json` | sim | 4 de 5 | 1 de 1 | rodou nas duas e o resultado não é o mesmo |
| `contrato-type_drift` | sim | 5 de 5 | 1 de 1 | rodou nas duas e o resultado é o mesmo |
| `localizador-front-admin-login` | sim | 5 de 5 | 1 de 1 | rodou nas duas e o resultado é o mesmo |
| `localizador-front-admin-produtos` | sim | 5 de 5 | 1 de 1 | rodou nas duas e o resultado é o mesmo |
| `localizador-front-busca` | sim | 5 de 5 | 1 de 1 | rodou nas duas e o resultado é o mesmo |
| `localizador-front-cliente-reserva` | sim | 5 de 5 | 1 de 1 | rodou nas duas e o resultado é o mesmo |

Regra aplicada: cada seleção registra os cenários que deixou de rodar, e a rodada completa seguinte confere se algum deles falhou (Azure DevOps TIA: comparar T1, os selecionados, com T2, todos).
