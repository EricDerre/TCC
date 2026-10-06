<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por gerar_relatorio_raciocinio.py a partir de trilhas remontadas das corridas gravadas (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Indicadores do relatório de raciocínio, gerada em 2026-10-01

Cada linha conta os eventos da trilha de uma corrida. As conferências da segunda tabela não usam o gabarito: são as que o agente poderá fazer sozinho na Fase 4. A frase de impacto e a nota exata que o modelo usou dentro de um verbete não têm como ser conferidas por código, e a tabela diz isso.


<!-- tabela:tb_rac_corridas -->
| Trilha (corrida, modelo, biblioteca) | Diagnósticos | Sem raciocínio antes das quatro linhas | Prompt inteiro provado | Só a documentação provada | Não comprovado | Acerto quando algum verbete do contexto trata da causa respondida | Acerto quando nenhum trata |
|---|---|---|---|---|---|---|---|
| `fase3`, `qwen2.5:7b`, L1 | 90 | 90 | 54 | 36 | 0 | 78,3% (65 de 83) | 57,1% (4 de 7) |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | 36 | 36 | 0 | 36 | 0 | 71,9% (23 de 32) | 75,0% (3 de 4) |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | 36 | 36 | 0 | 36 | 0 | 77,8% (21 de 27) | 11,1% (1 de 9) |
<!-- /tabela:tb_rac_corridas -->

<!-- tabela:tb_rac_conferencias -->
| Trilha | Conferência (sem usar o gabarito) | Confere | Não confere | Não se aplica | Não verificável ou informativo |
|---|---|---|---|---|---|
| `fase3`, `qwen2.5:7b`, L1 | A resposta tem as quatro linhas pedidas | 90 | 0 | 0 | 0 |
| `fase3`, `qwen2.5:7b`, L1 | A causa está entre as permitidas | 89 | 1 | 0 | 0 |
| `fase3`, `qwen2.5:7b`, L1 | O verbete citado existe na biblioteca | 117 | 0 | 0 | 0 |
| `fase3`, `qwen2.5:7b`, L1 | O verbete citado estava no contexto entregue ao modelo | 117 | 0 | 0 | 0 |
| `fase3`, `qwen2.5:7b`, L1 | O campo apontado aparece no caso | 53 | 0 | 37 | 0 |
| `fase3`, `qwen2.5:7b`, L1 | Algum verbete do contexto trata da causa respondida | 83 | 7 | 0 | 0 |
| `fase3`, `qwen2.5:7b`, L1 | Notas escritas pelo modelo nos verbetes citados | 0 | 0 | 0 | 90 |
| `fase3`, `qwen2.5:7b`, L1 | Frase de impacto | 0 | 0 | 0 | 90 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | A resposta tem as quatro linhas pedidas | 36 | 0 | 0 | 0 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | A causa está entre as permitidas | 36 | 0 | 0 | 0 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | O verbete citado existe na biblioteca | 43 | 0 | 0 | 0 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | O verbete citado estava no contexto entregue ao modelo | 43 | 0 | 0 | 0 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | O campo apontado aparece no caso | 23 | 0 | 13 | 0 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | Algum verbete do contexto trata da causa respondida | 32 | 4 | 0 | 0 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | Notas escritas pelo modelo nos verbetes citados | 0 | 0 | 0 | 36 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | Frase de impacto | 0 | 0 | 0 | 36 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | A resposta tem as quatro linhas pedidas | 36 | 0 | 0 | 0 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | A causa está entre as permitidas | 36 | 0 | 0 | 0 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | O verbete citado existe na biblioteca | 36 | 0 | 2 | 0 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | O verbete citado estava no contexto entregue ao modelo | 36 | 0 | 2 | 0 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | O campo apontado aparece no caso | 19 | 2 | 15 | 0 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | Algum verbete do contexto trata da causa respondida | 27 | 9 | 0 | 0 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | Notas escritas pelo modelo nos verbetes citados | 0 | 0 | 2 | 34 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | Frase de impacto | 0 | 0 | 0 | 36 |
<!-- /tabela:tb_rac_conferencias -->

<!-- tabela:tb_rac_avaliacao -->
| Trilha | Pergunta (com o gabarito) | Confere | Não confere |
|---|---|---|---|
| `fase3`, `qwen2.5:7b`, L1 | A causa respondida é a esperada | 69 | 21 |
| `fase3`, `qwen2.5:7b`, L1 | O campo respondido é o esperado | 67 | 23 |
| `fase3`, `qwen2.5:7b`, L1 | O verbete da causa esperada estava no contexto | 70 | 20 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | A causa respondida é a esperada | 26 | 10 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | O campo respondido é o esperado | 31 | 5 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | O verbete da causa esperada estava no contexto | 24 | 12 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | A causa respondida é a esperada | 22 | 14 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | O campo respondido é o esperado | 25 | 11 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | O verbete da causa esperada estava no contexto | 30 | 6 |
<!-- /tabela:tb_rac_avaliacao -->
