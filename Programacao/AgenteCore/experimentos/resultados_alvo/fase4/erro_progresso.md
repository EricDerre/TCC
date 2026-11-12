<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por progresso.py --erro a partir de trilha_*.jsonl das corridas vigentes e taxas_progresso.json (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Erro da estimativa da barra de progresso sobre os registros gravados (Pós-Fase 4, pacote Q4), gerada em 2026-11-08

cada inferência gravada é estimada pelos caracteres do prompt (evento prompt da trilha) e comparada com prefill_ms e geracao_ms do evento inferencia; fora_da_corrida usa as taxas das outras duas corridas (o que a barra vê numa corrida nova), na_amostra usa as taxas de todas, as de taxas_progresso.json; erro = estimado menos medido (negativo quer dizer que a barra acabaria antes do real); total_s é prefill mais geração, parede_s é o tempo de relógio da chamada, que inclui a carga do modelo.

## qwen2.5:7b, taxas das outras corridas (o que a barra vê numa corrida nova): 120 inferências

<!-- tabela:tb_f4_progresso_erro_fora_da_corrida_qwen2_5_7b -->
| Fase | n | Erro mediano (s) | Erro absoluto mediano (s) | Erro absoluto P90 (s) | Erro relativo mediano | Subestimadas |
|---|---|---|---|---|---|---|
| prefill | 120 | 0,1 | 9,9 | 23,2 | 18,7% | 59 de 120 |
| geração | 120 | -0,0 | 1,1 | 3,3 | 7,8% | 61 de 120 |
| prefill mais geração | 120 | -0,7 | 10,3 | 23,1 | 16,2% | 64 de 120 |
| tempo de relógio da chamada | 120 | -3,1 | 11,4 | 22,3 | 16,8% | 67 de 120 |
<!-- /tabela:tb_f4_progresso_erro_fora_da_corrida_qwen2_5_7b -->

Tokens do prompt estimados pelos caracteres: erro mediano de 7,0 tokens (absoluto mediano 20,0, máximo 91) em 120 prompts.

## qwen2.5:7b, taxas de todas as corridas (as do arquivo): 120 inferências

<!-- tabela:tb_f4_progresso_erro_na_amostra_qwen2_5_7b -->
| Fase | n | Erro mediano (s) | Erro absoluto mediano (s) | Erro absoluto P90 (s) | Erro relativo mediano | Subestimadas |
|---|---|---|---|---|---|---|
| prefill | 120 | 0,3 | 10,9 | 21,1 | 20,4% | 59 de 120 |
| geração | 120 | -0,0 | 1,1 | 3,3 | 7,8% | 61 de 120 |
| prefill mais geração | 120 | 0,2 | 10,6 | 21,2 | 16,3% | 59 de 120 |
| tempo de relógio da chamada | 120 | -2,2 | 12,7 | 21,5 | 17,7% | 68 de 120 |
<!-- /tabela:tb_f4_progresso_erro_na_amostra_qwen2_5_7b -->

Tokens do prompt estimados pelos caracteres: erro mediano de -0,5 tokens (absoluto mediano 16,5, máximo 89) em 120 prompts.
