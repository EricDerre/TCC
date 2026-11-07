<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase4.py a partir de cenarios.jsonl e condicoes_fase4.json da corrida (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Repetição do ensaio dos cenários da Fase 5 com o prompt dentro do limite (corrida 21c), gerada em 2026-11-05

Os dez cenários da ficha 36 (seis de contrato em produtos_api.php, um por modo, e quatro de localizador no front legado), cada um com o agente inteiro: diagnóstico ao vivo nos dez e cura de seletor nos quatro de localizador. No contrato (ficha 35), o MTTR vai da detecção ao diagnóstico conferido em código e o Task Success é a causa e o campo certos; no localizador, o MTTR vai da detecção à reexecução validada e o Task Success é o roteiro concluído sem erro depois da cura. O banco é restaurado e conferido por hash no começo de cada repetição. Prompt contra a calibração (seção 3.3 do plano): maior prompt da tela 1340 tokens, limite de 1409 (10% acima do maior da calibração, 1281); casos acima: nenhum.


<!-- tabela:tb_f4_cenarios_resumo -->
| Execuções | Task Success | Task Success (%) | Wilson 95% (%) | Detectadas | Com MTTR | MTTR médio (s) | Reamostragem 95% (s) | MTTR mediano (s) | Navegador | Banco no começo das repetições |
|---|---|---|---|---|---|---|---|---|---|---|
| 10 | 10 | 100,0 | 72,2 a 100,0 | 10 | 10 | 72,5 | 63,9 a 80,0 | 72,6 | 156.0.8078.4 | o mesmo hash em todas: 9fe5e7cb64288c9d |
<!-- /tabela:tb_f4_cenarios_resumo -->

<!-- tabela:tb_f4_cenarios_por_tipo -->
| Tipo | Execuções | Task Success | Task Success (%) | Wilson 95% (%) | Detectadas | Com MTTR | MTTR médio (s) | Reamostragem 95% (s) | MTTR mediano (s) |
|---|---|---|---|---|---|---|---|---|---|
| contrato | 6 | 6 | 100,0 | 61,0 a 100,0 | 6 | 6 | 79,9 | 74,4 a 86,0 | 78,1 |
| localizador | 4 | 4 | 100,0 | 51,0 a 100,0 | 4 | 4 | 61,5 | 48,0 a 70,2 | 66,0 |
<!-- /tabela:tb_f4_cenarios_por_tipo -->

<!-- tabela:tb_f4_cenarios_por_cenario -->
| Cenário | Tipo | Modo | Classe | Causa esperada | Execuções | Task Success | MTTR médio (s) | MTTR mediano (s) | Rótulos do diagnóstico | Segundos por execução | O que a detecção acusou |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `contrato-malformed_json` | contrato | `malformed_json` | 1 | `resposta_truncada` | 1 | 1 | 88,4 | 88,4 | `resposta_truncada` 1 | 88,6 | a conferência "grid com 14 cartões" (passo 3) falhou: esperado 14 elementos, observado 0 elementos |
| `contrato-field_missing` | contrato | `field_missing` | 2 | `campo_ausente` | 1 | 1 | 72,6 | 72,6 | `campo_ausente` 1 | 73,1 | a conferência "preço do primeiro cartão" (passo 4) falhou: esperado texto no padrão ^R\$ \d+,\d{2}$, observado undefined |
| `contrato-field_renamed` | contrato | `field_renamed` | 2 | `campo_renomeado` | 1 | 1 | 72,6 | 72,6 | `campo_renomeado` 1 | 73,0 | a conferência "preço do primeiro cartão" (passo 4) falhou: esperado texto no padrão ^R\$ \d+,\d{2}$, observado undefined |
| `contrato-type_drift` | contrato | `type_drift` | 3 | `tipo_divergente` | 1 | 1 | 72,7 | 72,7 | `tipo_divergente` 1 | 73,1 | o roteiro passou na tela, mas o fio acusou: diff do contrato: tipo_diferente; corpo diferente da referência em modo normal |
| `contrato-escala_ou_unidade_errada` | contrato | `escala_ou_unidade_errada` | 4 | `escala_ou_unidade_errada` | 1 | 1 | 89,5 | 89,5 | `escala_ou_unidade_errada` 1 | 89,9 | o roteiro passou na tela, mas o fio acusou: corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais |
| `contrato-error_500` | contrato | `error_500` | 5 | `erro_interno_do_servidor` | 1 | 1 | 83,4 | 83,4 | `erro_interno_do_servidor` 1 | 83,8 | a conferência "grid com 14 cartões" (passo 3) falhou: esperado 14 elementos, observado 0 elementos |
| `localizador-front-busca` | localizador | `id_renomeado` | 6 | `localizador_quebrado` | 1 | 1 | 71,8 | 71,8 | `localizador_quebrado` 1 | 77,7 | o passo 2 (esperar #buscar visível) não terminou: TimeoutError: Page.wait_for_selector: Timeout 5000ms exceeded. Call log: - waiting for locator("#buscar") to be visible |
| `localizador-front-admin-login` | localizador | `classe_trocada` | 6 | `localizador_quebrado` | 1 | 1 | 42,2 | 42,2 | `localizador_quebrado` 1 | 47,9 | o passo 5 (clicar em button.btn-primary) não terminou: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("button.btn-primary") |
| `localizador-front-admin-produtos` | localizador | `texto_alterado` | 6 | `localizador_quebrado` | 1 | 1 | 66,5 | 66,5 | `localizador_quebrado` 1 | 72,9 | o passo 11 (clicar em role=button[name=/EXCLUIR$/] >> nth=0) não terminou: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("role=button[name=/EXCLUIR$/]").first |
| `localizador-front-cliente-reserva` | localizador | `estrutura_alterada` | 6 | `localizador_quebrado` | 1 | 1 | 65,5 | 65,5 | `localizador_quebrado` 1 | 73,1 | o passo 11 (clicar em #reserva_login > input[type=submit]) não terminou: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("#reserva_login > input[type=submit]") |
<!-- /tabela:tb_f4_cenarios_por_cenario -->

<!-- tabela:tb_f4_cenarios_tempo -->
| Execuções | Segundos por execução (média) | Segundos no total | Estimativa da Fase 5 (10 cenários x 5 repetições, h) | Detecção pela conferência do roteiro | Detecção pelo fio (regra R1) | Detecção pelo passo do localizador |
|---|---|---|---|---|---|---|
| 10 | 75,3 | 753,1 | 1,1 | 4 | 2 | 4 |
<!-- /tabela:tb_f4_cenarios_tempo -->

<!-- tabela:tb_f4_cenarios_sem_sucesso -->
| Cenário | Repetição | Tipo | Detectou | Rótulo do diagnóstico | Causa esperada | Falha da cura | Segundos |
|---|---|---|---|---|---|---|---|
| nenhuma |  |  |  |  |  |  |  |
<!-- /tabela:tb_f4_cenarios_sem_sucesso -->
