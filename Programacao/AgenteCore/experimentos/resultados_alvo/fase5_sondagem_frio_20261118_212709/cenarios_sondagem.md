<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase4.py a partir de cenarios.jsonl e condicoes_fase4.json da corrida (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Ensaio dos cenários da Fase 5: MTTR e Task Success (corrida 21), gerada em 2026-11-18

Os dez cenários da ficha 36 (seis de contrato em produtos_api.php, um por modo, e quatro de localizador no front legado), cada um com o agente inteiro: diagnóstico ao vivo nos dez e cura de seletor nos quatro de localizador. No contrato (ficha 35), o MTTR vai da detecção ao diagnóstico conferido em código e o Task Success é a causa e o campo certos; no localizador, o MTTR vai da detecção à reexecução validada e o Task Success é o roteiro concluído sem erro depois da cura. O banco é restaurado e conferido por hash no começo de cada repetição. Prompt contra a calibração (seção 3.3 do plano): maior prompt da tela 1218 tokens, limite de 1409 (10% acima do maior da calibração, 1281); casos acima: nenhum.


<!-- tabela:tb_f4_cenarios_resumo -->
| Execuções | Task Success | Task Success (%) | Wilson 95% (%) | Detectadas | Com MTTR | MTTR médio (s) | Reamostragem 95% (s) | MTTR mediano (s) | Navegador | Banco no começo das repetições |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 2 | 100,0 | 34,2 a 100,0 | 2 | 2 | 79,3 | 77,8 a 80,8 | 79,3 | 156.0.8078.4 | o mesmo hash em todas: 9fe5e7cb64288c9d |
<!-- /tabela:tb_f4_cenarios_resumo -->

<!-- tabela:tb_f4_cenarios_por_tipo -->
| Tipo | Execuções | Task Success | Task Success (%) | Wilson 95% (%) | Detectadas | Com MTTR | MTTR médio (s) | Reamostragem 95% (s) | MTTR mediano (s) |
|---|---|---|---|---|---|---|---|---|---|
| contrato | 2 | 2 | 100,0 | 34,2 a 100,0 | 2 | 2 | 79,3 | 77,8 a 80,8 | 79,3 |
<!-- /tabela:tb_f4_cenarios_por_tipo -->

<!-- tabela:tb_f4_cenarios_por_cenario -->
| Cenário | Tipo | Modo | Classe | Causa esperada | Execuções | Task Success | MTTR médio (s) | MTTR mediano (s) | Rótulos do diagnóstico | Segundos por execução | O que a detecção acusou |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `contrato-malformed_json` | contrato | `malformed_json` | 1 | `resposta_truncada` | 2 | 2 | 79,3 | 79,3 | `resposta_truncada` 2 | 79,5 | a conferência "grid com 14 cartões" (passo 3) falhou: esperado 14 elementos, observado 0 elementos |
<!-- /tabela:tb_f4_cenarios_por_cenario -->

<!-- tabela:tb_f4_cenarios_tempo -->
| Execuções | Segundos por execução (média) | Segundos no total | Estimativa da Fase 5 (10 cenários x 5 repetições, h) | Detecção pela conferência do roteiro | Detecção pelo fio (regra R1) | Detecção pelo passo do localizador |
|---|---|---|---|---|---|---|
| 2 | 79,5 | 159,1 | 1,1 | 2 | 0 | 0 |
<!-- /tabela:tb_f4_cenarios_tempo -->

<!-- tabela:tb_f4_cenarios_sem_sucesso -->
| Cenário | Repetição | Tipo | Detectou | Rótulo do diagnóstico | Causa esperada | Falha da cura | Segundos |
|---|---|---|---|---|---|---|---|
| nenhuma |  |  |  |  |  |  |  |
<!-- /tabela:tb_f4_cenarios_sem_sucesso -->
