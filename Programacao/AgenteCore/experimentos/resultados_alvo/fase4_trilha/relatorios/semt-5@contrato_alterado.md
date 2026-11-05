<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-5@contrato_alterado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-5@contrato_alterado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `nulo_inesperado` · **CAMPO:** `nome` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `A saudação na área do cliente exibe 'Olá, !', indicando que o campo nome está nulo na resposta da API.`

Justificativa (gerada por molde): O agente respondeu nulo_inesperado no campo nome porque o sinal id_pedido: esperado texto, recebido inteiro está presente na resposta HTTP e os verbetes nulo_inesperado, contrato-pedido, usuario-e-login estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 785): regras diff_contra_contrato; antes {"chars": 121}, depois {"chars": 121}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id_pedido | texto | inteiro |
| nome | texto | nulo |

Trecho podado (hash `83e91442cbd302d4`):

```text
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": null, "cpf": "11122233344"}]
```

## 3. Contraste com a segunda causa

nulo_inesperado e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: nulo_inesperado, contrato-pedido, usuario-e-login

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| nulo_inesperado | 1,00 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[nulo_inesperado]`; verbetes citados: `nulo_inesperado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `nulo_inesperado`, `contrato-pedido`, `usuario-e-login` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `nulo_inesperado`, `usuario-e-login` |
| fonte_formato_valido | `[nulo_inesperado]` | confere | {"ids": ["nulo_inesperado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids semt-5 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 784 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:45:05 | caso semt-5@contrato_alterado |
| 785 | 2 | poda | programa | ao_vivo | 2026-11-04T23:45:05 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato |
| 786 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:45:05 | poda: escolha json/lista; id_pedido:tipo_diferente, nome:nulo_inesperado; divergência não |
| 787 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:45:05 | 3 de 39 verbetes entregues |
| 788 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:45:05 | recuperacao: escolha nulo_inesperado,contrato-pedido,usuario-e-login; divergência não |
| 790 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:45:05 | {"etapa": "diagnostico", "sha": "0712b39020f899c0", "prompt_sha256": "0712b39020f8", "chars": 3316, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 792 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:45:05 | diagnostico: 38,8 s |
| 793 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:45:05 | causa_raiz: `nulo_inesperado` |
| 794 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:45:05 | campo: `nome` |
| 795 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:45:05 | impacto: `A saudação na área do cliente exibe 'Olá, !', indicando que o campo nome está nulo na resposta da API.` |
| 796 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:45:05 | fonte: `[nulo_inesperado]` |
| 797 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:45:05 | fonte_citada: `nulo_inesperado` |
| 798 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:45:05 | quatro_linhas_presentes: confere |
| 799 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:45:05 | rotulo_no_conjunto: confere |
| 800 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:45:05 | fonte_existe_na_biblioteca: confere |
| 801 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:45:05 | fonte_estava_no_contexto: confere |
| 802 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:45:05 | campo_existe_no_caso: confere |
| 803 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:45:05 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 804 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:45:05 | notas_nos_verbetes_citados: informativo |
| 805 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:45:05 | impacto: nao_verificavel |
| 806 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:45:05 | fonte_formato_valido: confere |
| 807 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:45:05 | fonte_contem_termo_da_causa: confere |
| 808 | 23 | decisao | programa | ao_vivo | 2026-11-04T23:45:05 | diagnostico: escolha nulo_inesperado; divergência não |

</details>

Nós de decisão:

- evento 786, `poda`: escolha `json/lista; id_pedido:tipo_diferente, nome:nulo_inesperado`; resultado sinais_em_codigo; evidência: evento 785 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id_pedido, nome (gen_ai: plan)
- evento 788, `recuperacao`: escolha `nulo_inesperado,contrato-pedido,usuario-e-login`; resultado verbetes_entregues; evidência: evento 787 (verbete_entregue, nulo_inesperado), evento 787 (verbete_entregue, contrato-pedido), evento 787 (verbete_entregue, usuario-e-login); divergência: não; falha: nenhuma; prov.used: nulo_inesperado, contrato-pedido, usuario-e-login (gen_ai: retrieval)
- evento 808, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 785 (sinal_em_codigo), evento 787 (verbete_entregue, nulo_inesperado), evento 787 (verbete_entregue, contrato-pedido), evento 787 (verbete_entregue, usuario-e-login), evento 792 (resposta), evento 797 (verbete_citado, nulo_inesperado); divergência: não; falha: nenhuma; prov.used: nulo_inesperado, contrato-pedido, usuario-e-login (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 784 a 808 da trilha; hash dos eventos deste caso: `afe74027db1f5d12`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
