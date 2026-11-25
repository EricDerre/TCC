<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase5.py a partir de cenarios.jsonl e fase4.log da corrida 21d e o log das três últimas pontes (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Fase 5 do Memorial cola estes blocos, e as contas são as das regras L1 a L15 do plano aprovado, fixadas antes das medidas. -->
# O tempo de máquina da noite medida da Fase 5 (corrida 28), gerada em 2026-11-16

Estimativa feita com os registros da corrida 21d (`fase4_ensaio_v4`), que rodou os dez cenários uma vez. A conta de baixo multiplica o tempo médio de uma execução pelas execuções da noite; a de cima multiplica o tempo do executor inteiro pelas repetições, o que inclui o que ele gasta fora das execuções, e soma o que o lançador gastou fora do executor. A ponte só roda se o Ollama tiver mudado de versão desde a última ponte registrada. O painel, regerado no fim da noite, não está nesta conta.


<!-- tabela:tb_f5_custo_resumo -->
| Execuções da noite | Segundos por execução na corrida 21d (média) | Horas pela média das execuções | Segundos do executor na corrida 21d | Horas pelo executor inteiro | Segundos fora do executor na corrida 21d (bateria de testes e leitura) | Ponte, se o Ollama mudou de versão (min) | Noite sem a ponte (min) | Noite com a ponte (min) |
|---|---|---|---|---|---|---|---|---|
| 50 (10 cenários x 5 repetições) | 76,7 | 1,07 | 808 | 1,12 | 26 | 34 a 42 | 68 | 110 |
<!-- /tabela:tb_f5_custo_resumo -->

<!-- tabela:tb_f5_custo_pontes -->
| Ponte (pasta em `resultados_alvo/`) | Versão do Ollama | Data | Duração (min) |
|---|---|---|---|
| `fase3b_ponte_04014` | 0.40.14 | 2026-11-03 | 42 |
| `fase3b_ponte_04015` | 0.40.15 | 2026-11-11 | 34 |
| `fase3b_ponte_04016` | 0.40.16 | 2026-11-16 | 37 |
<!-- /tabela:tb_f5_custo_pontes -->
