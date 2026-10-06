<!-- ! Alteração de IA - Revisar: índice DERIVADO, gerado por gerar_relatorio_raciocinio.py --vitrine; não editar à mão.
     ! Motivo: um relatório por caso é ilegível sem uma lista que diga em quais vale a pena entrar; a última coluna aponta os casos em que alguma conferência não confere. -->
# Relatórios de raciocínio: `fase3b_ineditos`, `qwen2.5:7b`, biblioteca L1

36 casos. Trilha bruta: `../../trilhas/fase3b_ineditos__qwen2.5_7b__L1.jsonl`.

| Caso | Classe | Nível | Causa respondida | Acertou | O que não confere (sem usar o gabarito) |
|---|---|---|---|---|---|
| [`lex-16`](lex-16.md) | 1 | 1 | `resposta_truncada` | sim | nada |
| [`lex-17`](lex-17.md) | 1 | 1 | `corpo_vazio` | sim | nada |
| [`lex-18`](lex-18.md) | 1 | 2 | `tipo_divergente` | **não** | nada |
| [`lex-19`](lex-19.md) | 1 | 2 | `erro_interno_do_servidor` | **não** | nada |
| [`lex-20`](lex-20.md) | 1 | 3 | `resposta_truncada` | sim | nada |
| [`lex-21`](lex-21.md) | 1 | 3 | `codificacao_incorreta` | sim | nenhum verbete do contexto trata da causa respondida |
| [`sin-16`](sin-16.md) | 2 | 1 | `campo_ausente` | sim | nada |
| [`sin-17`](sin-17.md) | 2 | 1 | `campo_renomeado` | sim | nada |
| [`sin-18`](sin-18.md) | 2 | 2 | `estrutura_aninhada_divergente` | sim | nada |
| [`sin-19`](sin-19.md) | 2 | 2 | `colecao_no_lugar_de_objeto` | sim | nada |
| [`sin-20`](sin-20.md) | 2 | 3 | `campo_ausente` | sim | nada |
| [`sin-21`](sin-21.md) | 2 | 3 | `estrutura_aninhada_divergente` | sim | nada |
| [`semt-16`](semt-16.md) | 3 | 1 | `tipo_divergente` | sim | nada |
| [`semt-17`](semt-17.md) | 3 | 1 | `nulo_inesperado` | sim | nada |
| [`semt-18`](semt-18.md) | 3 | 2 | `tipo_divergente` | sim | nada |
| [`semt-19`](semt-19.md) | 3 | 2 | `formato_de_data_divergente` | sim | nada |
| [`semt-20`](semt-20.md) | 3 | 3 | `tipo_divergente` | **não** | nada |
| [`semt-21`](semt-21.md) | 3 | 3 | `campo_ausente` | **não** | nada |
| [`tra-16`](tra-16.md) | 4 | 1 | `contagem_inconsistente` | **não** | nenhum verbete do contexto trata da causa respondida |
| [`tra-17`](tra-17.md) | 4 | 1 | `tipo_divergente` | **não** | nada |
| [`tra-18`](tra-18.md) | 4 | 2 | `contagem_inconsistente` | sim | nenhum verbete do contexto trata da causa respondida |
| [`tra-19`](tra-19.md) | 4 | 2 | `escala_ou_unidade_errada` | sim | nada |
| [`tra-20`](tra-20.md) | 4 | 3 | `chave_de_juncao_errada` | sim | nada |
| [`tra-21`](tra-21.md) | 4 | 3 | `contagem_inconsistente` | sim | nada |
| [`run-16`](run-16.md) | 5 | 1 | `recurso_inexistente` | sim | nada |
| [`run-17`](run-17.md) | 5 | 1 | `erro_interno_do_servidor` | sim | nada |
| [`run-18`](run-18.md) | 5 | 2 | `limite_de_requisicoes` | sim | nada |
| [`run-19`](run-19.md) | 5 | 2 | `tempo_de_resposta_excedido` | sim | nada |
| [`run-20`](run-20.md) | 5 | 3 | `dado_desatualizado` | sim | nada |
| [`run-21`](run-21.md) | 5 | 3 | `registro_duplicado` | sim | nenhum verbete do contexto trata da causa respondida |
| [`efe-16`](efe-16.md) | 6 | 1 | `tempo_de_resposta_excedido` | **não** | nada |
| [`efe-17`](efe-17.md) | 6 | 1 | `localizador_quebrado` | sim | nada |
| [`efe-18`](efe-18.md) | 6 | 2 | `localizador_quebrado` | sim | nada |
| [`efe-19`](efe-19.md) | 6 | 2 | `localizador_quebrado` | **não** | nada |
| [`efe-20`](efe-20.md) | 6 | 3 | `corpo_vazio` | **não** | nada |
| [`efe-21`](efe-21.md) | 6 | 3 | `nulo_inesperado` | **não** | nada |
