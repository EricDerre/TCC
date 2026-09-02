<!-- ! Alteração de IA - Revisar: tabela gerada por benchmark_modelos.py.
     ! Motivo: saída de medição, reescrita a cada execução — não editar à mão;
     a leitura e as conclusões estão em RESULTADO_FASE2.md. -->

| Modelo | Tarefa | Mediana (s) | Faixa (s) | Tokens ent./saída | Memória | Só CPU |
|---|---|---|---|---|---|---|
| qwen2.5-coder:1.5b | diagnostico | 10.24 | 8.36–11.04 | 479/172 | 1116 MB | sim |
| qwen2.5-coder:1.5b | seletor | 2.49 | 2.3–2.5 | 369/10 | 1116 MB | sim |
| qwen2.5-coder:3b | diagnostico | 5.98 | 5.68–6.16 | 479/52 | 2064 MB | sim |
| qwen2.5-coder:3b | seletor | 3.94 | 3.8–3.99 | 369/24 | 2064 MB | sim |
| qwen2.5-coder:7b | diagnostico | 16.08 | 15.63–18.5 | 479/86 | 4828 MB | sim |
| qwen2.5-coder:7b | seletor | 6.45 | 5.39–6.55 | 369/22 | 4828 MB | sim |
