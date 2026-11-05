<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por avaliar_fase4.py a partir de cenarios.jsonl e condicoes_fase4.json da corrida (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Repetição do ensaio dos cenários da Fase 5, com a correção da cura (corrida 21b), gerada em 2026-11-04

Os dez cenários da ficha 36 (seis de contrato em produtos_api.php, um por modo, e quatro de localizador no front legado), cada um com o agente inteiro: diagnóstico ao vivo nos dez e cura de seletor nos quatro de localizador. No contrato (ficha 35), o MTTR vai da detecção ao diagnóstico conferido em código e o Task Success é a causa e o campo certos; no localizador, o MTTR vai da detecção à reexecução validada e o Task Success é o roteiro concluído sem erro depois da cura. O banco é restaurado e conferido por hash no começo de cada repetição.


<!-- tabela:tb_f4_cenarios_resumo -->
| Execuções | Task Success | Task Success (%) | Wilson 95% (%) | Detectadas | Com MTTR | MTTR médio (s) | Reamostragem 95% (s) | MTTR mediano (s) | Navegador | Banco no começo das repetições |
|---|---|---|---|---|---|---|---|---|---|---|
| 10 | 10 | 100,0 | 72,2 a 100,0 | 10 | 10 | 105,2 | 90,6 a 118,0 | 114,3 | 156.0.8078.4 | o mesmo hash em todas: 9fe5e7cb64288c9d |
<!-- /tabela:tb_f4_cenarios_resumo -->

<!-- tabela:tb_f4_cenarios_por_tipo -->
| Tipo | Execuções | Task Success | Task Success (%) | Wilson 95% (%) | Detectadas | Com MTTR | MTTR médio (s) | Reamostragem 95% (s) | MTTR mediano (s) |
|---|---|---|---|---|---|---|---|---|---|
| contrato | 6 | 6 | 100,0 | 61,0 a 100,0 | 6 | 6 | 114,7 | 97,1 a 128,0 | 120,3 |
| localizador | 4 | 4 | 100,0 | 51,0 a 100,0 | 4 | 4 | 90,8 | 70,0 a 110,5 | 90,9 |
<!-- /tabela:tb_f4_cenarios_por_tipo -->

<!-- tabela:tb_f4_cenarios_por_cenario -->
| Cenário | Tipo | Modo | Classe | Causa esperada | Execuções | Task Success | MTTR médio (s) | MTTR mediano (s) | Rótulos do diagnóstico | Segundos por execução | O que a detecção acusou |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `contrato-malformed_json` | contrato | `malformed_json` | 1 | `resposta_truncada` | 1 | 1 | 126,0 | 126,0 | `resposta_truncada` 1 | 126,3 | a conferência "grid com 14 cartões" (passo 3) falhou: esperado 14 elementos, observado 0 elementos |
| `contrato-field_missing` | contrato | `field_missing` | 2 | `campo_ausente` | 1 | 1 | 111,8 | 111,8 | `campo_ausente` 1 | 112,2 | a conferência "preço do primeiro cartão" (passo 4) falhou: esperado texto no padrão ^R\$ \d+,\d{2}$, observado undefined |
| `contrato-field_renamed` | contrato | `field_renamed` | 2 | `campo_renomeado` | 1 | 1 | 116,9 | 116,9 | `campo_renomeado` 1 | 117,2 | a conferência "preço do primeiro cartão" (passo 4) falhou: esperado texto no padrão ^R\$ \d+,\d{2}$, observado undefined |
| `contrato-type_drift` | contrato | `type_drift` | 3 | `tipo_divergente` | 1 | 1 | 74,5 | 74,5 | `tipo_divergente` 1 | 75,0 | o roteiro passou na tela, mas o fio acusou: diff do contrato: tipo_diferente; corpo diferente da referência em modo normal |
| `contrato-escala_ou_unidade_errada` | contrato | `escala_ou_unidade_errada` | 4 | `escala_ou_unidade_errada` | 1 | 1 | 135,5 | 135,5 | `escala_ou_unidade_errada` 1 | 135,9 | o roteiro passou na tela, mas o fio acusou: corpo diferente da referência em modo normal; árvore diferente da referência: 14 linha(s) a menos e 14 a mais |
| `contrato-error_500` | contrato | `error_500` | 5 | `erro_interno_do_servidor` | 1 | 1 | 123,8 | 123,8 | `erro_interno_do_servidor` 1 | 124,1 | a conferência "grid com 14 cartões" (passo 3) falhou: esperado 14 elementos, observado 0 elementos |
| `localizador-front-busca` | localizador | `id_renomeado` | 6 | `localizador_quebrado` | 1 | 1 | 117,7 | 117,7 | `localizador_quebrado` 1 | 123,6 | o passo 2 (esperar #buscar visível) não terminou: TimeoutError: Page.wait_for_selector: Timeout 5000ms exceeded. Call log: - waiting for locator("#buscar") to be visible |
| `localizador-front-admin-login` | localizador | `classe_trocada` | 6 | `localizador_quebrado` | 1 | 1 | 63,7 | 63,7 | `localizador_quebrado` 1 | 69,5 | o passo 5 (clicar em button.btn-primary) não terminou: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("button.btn-primary") |
| `localizador-front-admin-produtos` | localizador | `texto_alterado` | 6 | `localizador_quebrado` | 1 | 1 | 93,0 | 93,0 | `localizador_quebrado` 1 | 99,6 | o passo 11 (clicar em role=button[name=/EXCLUIR$/] >> nth=0) não terminou: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("role=button[name=/EXCLUIR$/]").first |
| `localizador-front-cliente-reserva` | localizador | `estrutura_alterada` | 6 | `localizador_quebrado` | 1 | 1 | 88,9 | 88,9 | `localizador_quebrado` 1 | 96,4 | o passo 11 (clicar em #reserva_login > input[type=submit]) não terminou: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("#reserva_login > input[type=submit]") |
<!-- /tabela:tb_f4_cenarios_por_cenario -->

<!-- tabela:tb_f4_cenarios_tempo -->
| Execuções | Segundos por execução (média) | Segundos no total | Estimativa da Fase 5 (10 cenários x 5 repetições, h) | Detecção pela conferência do roteiro | Detecção pelo fio (regra R1) | Detecção pelo passo do localizador |
|---|---|---|---|---|---|---|
| 10 | 108,0 | 1079,8 | 1,5 | 4 | 2 | 4 |
<!-- /tabela:tb_f4_cenarios_tempo -->

<!-- tabela:tb_f4_cenarios_sem_sucesso -->
| Cenário | Repetição | Tipo | Detectou | Rótulo do diagnóstico | Causa esperada | Falha da cura | Segundos |
|---|---|---|---|---|---|---|---|
| nenhuma |  |  |  |  |  |  |  |
<!-- /tabela:tb_f4_cenarios_sem_sucesso -->
