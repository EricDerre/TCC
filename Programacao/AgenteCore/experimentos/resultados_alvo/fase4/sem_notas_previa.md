<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por experimento_sem_notas.py --previa a partir de `biblioteca_producao/`, `fase4_trilha` e `fase4_ineditos` (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Prévia sem modelo da corrida 25: o que muda no contexto sem as notas do modelo, gerada em 2026-11-10

Sem modelo. A biblioteca de produção (`95af35290860`) tem 39 verbetes e 26 notas do modelo em 20 deles, 25 escritas como instrução. A cópia sem as notas e sem os 3 verbetes aprendidos (`ba5ff9f5f632`) fica com 36 verbetes. Como a busca e a montagem do contexto são código, dá para saber antes da corrida 25 o que muda no contexto de cada caso: a busca perde o texto das notas no índice, e o verbete entregue perde o trecho das notas.

Dos 72 casos, o contexto muda em 72: em 59 os verbetes entregues são os mesmos, na mesma ordem, só sem as notas; em 4 são os mesmos em outra ordem; em 9 a busca troca um verbete. Na referência, 72 contextos traziam ao menos uma nota e 0 traziam um verbete aprendido. O verbete da causa certa estava entre os entregues em 50 casos e continua em 50; a presença dele muda em 0. Pela mediana das corridas de referência, as 72 inferências levam cerca de 80 minutos.

Regra fixada antes da corrida (decisão 116): a diferença sai do ruído quando o teste pareado exato dos casos dos dois bancos juntos (McNemar, bilateral) dá p abaixo de 0,05, com a corrida completa e a ponte da versão do Ollama pareável com a Fase 3 (b + c até 2, decisão 47). Fora disso a diferença fica dentro do ruído e o agente não muda; se sair do ruído, mudar o agente é outra decisão.

<!-- tabela:tb_f4_semnotas_previa_biblioteca -->
| Biblioteca | Hash | Verbetes | Notas do modelo | Verbetes com nota | Notas em forma de instrução | Tokens estimados da biblioteca inteira |
|---|---|---|---|---|---|---|
| produção | `95af35290860` | 39 | 26 | 20 | 25 | 8576 |
| sem as notas e sem os aprendidos | `ba5ff9f5f632` | 36 | 0 | 0 | 0 | 6582 |
<!-- /tabela:tb_f4_semnotas_previa_biblioteca -->
<!-- tabela:tb_f4_semnotas_previa_banco -->
| Banco | Referência | Casos | Acertos na referência | Contexto da referência refeito igual | Com nota na referência | Com verbete aprendido na referência | Contexto idêntico | Mesmos verbetes, sem as notas | Mesmos verbetes, outra ordem | Verbetes diferentes | Verbete certo antes e depois | Verbete certo só antes | Verbete certo só depois | Caracteres do contexto (mediana) na referência | Caracteres do contexto (mediana) sem as notas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| os 36 oficiais de avaliação | corrida 22 | 36 | 31 | 36 | 36 | 0 | 0 | 32 | 1 | 3 | 30 | 0 | 0 | 1937,0 | 1532,5 |
| os 36 inéditos da ficha 27 | corrida 24 | 36 | 25 | 36 | 36 | 0 | 0 | 27 | 3 | 6 | 20 | 0 | 0 | 1927,0 | 1539,0 |
<!-- /tabela:tb_f4_semnotas_previa_banco -->
<!-- tabela:tb_f4_semnotas_previa_verbetes -->
| Caso | Banco | Verbetes na referência | Verbetes sem as notas | Saiu | Entrou |
|---|---|---|---|---|---|
| `sin-5` | avaliacao | `entidade-produto`, `contrato-produto`, `tipo_divergente` | `entidade-produto`, `contrato-produto`, `campo_renomeado` | `tipo_divergente` | `campo_renomeado` |
| `efe-5` | avaliacao | `localizador_quebrado`, `ancora-saiba-mais`, `corpo_nao_e_json` | `localizador_quebrado`, `ancora-saiba-mais`, `entidade-produto` | `corpo_nao_e_json` | `entidade-produto` |
| `efe-14` | avaliacao | `localizador_quebrado`, `ancora-saiba-mais`, `estado_da_tela_divergente` | `localizador_quebrado`, `ancora-saiba-mais`, `limites-do-sistema` | `estado_da_tela_divergente` | `limites-do-sistema` |
| `lex-22` | ineditos | `corpo_nao_e_json`, `mensagens-de-erro-do-codigo`, `corpo_vazio` | `corpo_nao_e_json`, `mensagens-de-erro-do-codigo`, `limite_de_requisicoes` | `corpo_vazio` | `limite_de_requisicoes` |
| `lex-27` | ineditos | `contrato-pedido`, `pedido-reserva`, `formato_de_data_divergente` | `contrato-pedido`, `pedido-reserva`, `estado_da_tela_divergente` | `formato_de_data_divergente` | `estado_da_tela_divergente` |
| `sin-27` | ineditos | `contrato-produto`, `entidade-produto`, `chave_de_juncao_errada` | `contrato-produto`, `entidade-produto`, `campo_ausente` | `chave_de_juncao_errada` | `campo_ausente` |
| `run-22` | ineditos | `limite_de_requisicoes`, `contagem_inconsistente`, `estrutura_aninhada_divergente` | `limite_de_requisicoes`, `estrutura_aninhada_divergente`, `tempo_de_resposta_excedido` | `contagem_inconsistente` | `tempo_de_resposta_excedido` |
| `run-23` | ineditos | `recurso_inexistente`, `contrato-produto`, `mensagens-de-erro-do-codigo` | `recurso_inexistente`, `contrato-produto`, `contagem_inconsistente` | `mensagens-de-erro-do-codigo` | `contagem_inconsistente` |
| `efe-25` | ineditos | `localizador_quebrado`, `contrato-produto`, `entidade-produto` | `localizador_quebrado`, `estado_da_tela_divergente`, `entidade-produto` | `contrato-produto` | `estado_da_tela_divergente` |
<!-- /tabela:tb_f4_semnotas_previa_verbetes -->
