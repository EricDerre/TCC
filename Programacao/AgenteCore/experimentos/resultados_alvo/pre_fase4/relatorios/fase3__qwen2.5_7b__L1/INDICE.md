<!-- ! Alteração de IA - Revisar: índice DERIVADO, gerado por gerar_relatorio_raciocinio.py --vitrine; não editar à mão.
     ! Motivo: um relatório por caso é ilegível sem uma lista que diga em quais vale a pena entrar; a última coluna aponta os casos em que alguma conferência não confere. -->
# Relatórios de raciocínio: `fase3`, `qwen2.5:7b`, biblioteca L1

36 casos da partição de avaliacao. Trilha bruta: `../../trilhas/fase3__qwen2.5_7b__L1.jsonl`.

| Caso | Classe | Nível | Causa respondida | Acertou | O que não confere (sem usar o gabarito) |
|---|---|---|---|---|---|
| [`lex-1`](lex-1.md) | 1 | 1 | `resposta_truncada` | sim | nada |
| [`lex-4`](lex-4.md) | 1 | 2 | `codificacao_incorreta` | sim | nenhum verbete do contexto trata da causa respondida |
| [`sin-4`](sin-4.md) | 2 | 1 | `colecao_no_lugar_de_objeto` | sim | nada |
| [`sin-5`](sin-5.md) | 2 | 3 | `tipo_divergente` | **não** | nada |
| [`semt-1`](semt-1.md) | 3 | 2 | `tipo_divergente` | sim | nada |
| [`semt-3`](semt-3.md) | 3 | 2 | `valor_fora_do_dominio` | sim | nada |
| [`semt-5`](semt-5.md) | 3 | 3 | `nulo_inesperado` | sim | nada |
| [`tra-1`](tra-1.md) | 4 | 2 | `escala_ou_unidade_errada` | sim | nada |
| [`tra-4`](tra-4.md) | 4 | 3 | `contagem_inconsistente` | sim | nada |
| [`run-1`](run-1.md) | 5 | 1 | `erro_interno_do_servidor` | sim | nada |
| [`run-2`](run-2.md) | 5 | 1 | `tempo_de_resposta_excedido` | sim | nada |
| [`run-4`](run-4.md) | 5 | 3 | `dado_desatualizado` | sim | nada |
| [`efe-1`](efe-1.md) | 6 | 1 | `localizador_quebrado` | sim | nada |
| [`efe-2`](efe-2.md) | 6 | 2 | `estado_da_tela_divergente` | sim | nada |
| [`efe-3`](efe-3.md) | 6 | 2 | `tipo_divergente` | **não** | nada |
| [`efe-5`](efe-5.md) | 6 | 3 | `localizador_quebrado` | sim | nada |
| [`lex-7`](lex-7.md) | 1 | 1 | `corpo_vazio` | sim | nada |
| [`lex-8`](lex-8.md) | 1 | 2 | `codificacao_incorreta` | sim | nada |
| [`lex-10`](lex-10.md) | 1 | 3 | `resposta_truncada` | sim | nada |
| [`lex-11`](lex-11.md) | 1 | 3 | `codificacao_incorreta` | sim | nada |
| [`sin-7`](sin-7.md) | 2 | 1 | `campo_ausente` | sim | nada |
| [`sin-10`](sin-10.md) | 2 | 2 | `campo_renomeado` | sim | nada |
| [`sin-11`](sin-11.md) | 2 | 2 | `estrutura_aninhada_divergente` | sim | nada |
| [`sin-14`](sin-14.md) | 2 | 3 | `campo_renomeado` | sim | nada |
| [`semt-8`](semt-8.md) | 3 | 1 | `nulo_inesperado` | sim | nada |
| [`semt-9`](semt-9.md) | 3 | 1 | `tipo_divergente` | **não** | nada |
| [`semt-14`](semt-14.md) | 3 | 3 | `nulo_inesperado` | sim | nada |
| [`tra-8`](tra-8.md) | 4 | 1 | `contagem_inconsistente` | sim | nada |
| [`tra-10`](tra-10.md) | 4 | 1 | `chave_de_juncao_errada` | sim | nada |
| [`tra-11`](tra-11.md) | 4 | 2 | `contagem_inconsistente` | sim | nada |
| [`tra-15`](tra-15.md) | 4 | 3 | `valor_fora_do_dominio` | **não** | nada |
| [`run-9`](run-9.md) | 5 | 2 | `tempo_de_resposta_excedido` | sim | nenhum verbete do contexto trata da causa respondida |
| [`run-10`](run-10.md) | 5 | 2 | `limite_de_requisicoes` | sim | nada |
| [`run-13`](run-13.md) | 5 | 3 | `registro_duplicado` | sim | nada |
| [`efe-7`](efe-7.md) | 6 | 1 | `localizador_quebrado` | sim | nada |
| [`efe-14`](efe-14.md) | 6 | 3 | `localizador_quebrado` | sim | nada |
