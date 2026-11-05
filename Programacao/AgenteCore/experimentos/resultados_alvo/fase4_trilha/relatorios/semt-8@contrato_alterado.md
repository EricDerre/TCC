<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-8@contrato_alterado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-8@contrato_alterado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `nulo_inesperado` · **CAMPO:** `preco` · selo de probabilidade: **baixo** (p = 0,74)

**IMPACTO (declarado):** `O usuário vê 'R$ 0,00' em vez do preço correto de R$ 89,90.`

Justificativa (gerada por molde): O agente respondeu nulo_inesperado no campo preco porque o sinal id: esperado texto, recebido inteiro está presente na resposta HTTP e os verbetes entidade-produto, nulo_inesperado, contrato-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,15. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,74); trate como hipótese e confira o campo preco antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 2662): regras diff_contra_contrato; antes {"chars": 149}, depois {"chars": 149}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | texto | inteiro |
| preco | numero | nulo |

Trecho podado (hash `c36e9bb22382f8e9`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": null, "imagem": "picanha_alho.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

nulo_inesperado e não tipo_divergente: a escolha tem probabilidade 0,74 contra 0,15; verbete(s) na evidência: entidade-produto, nulo_inesperado, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| nulo_inesperado | 0,74 | sim |
| tipo_divergente | 0,15 |  |
| valor_fora_do_dominio | 0,07 |  |
| formato_de_data_divergente | 0,02 |  |
| resposta_truncada | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[nulo_inesperado]`; verbetes citados: `nulo_inesperado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `entidade-produto`, `nulo_inesperado`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `nulo_inesperado` |
| fonte_formato_valido | `[nulo_inesperado]` | confere | {"ids": ["nulo_inesperado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids semt-8 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2661 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:31:31 | caso semt-8@contrato_alterado |
| 2662 | 2 | poda | programa | ao_vivo | 2026-11-05T01:31:31 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2663 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:31:31 | poda: escolha json/lista; id:tipo_diferente, preco:nulo_inesperado; divergência não |
| 2664 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:31:31 | 3 de 39 verbetes entregues |
| 2665 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:31:31 | recuperacao: escolha entidade-produto,nulo_inesperado,contrato-produto; divergência não |
| 2667 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:31:31 | {"etapa": "diagnostico", "sha": "6b9c8bb5c293ceff", "prompt_sha256": "6b9c8bb5c293", "chars": 3348, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2668 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:31:31 | diagnostico: 38,3 s |
| 2669 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:31:31 | causa_raiz: `nulo_inesperado` |
| 2670 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:31:31 | campo: `preco` |
| 2671 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:31:31 | impacto: `O usuário vê 'R$ 0,00' em vez do preço correto de R$ 89,90.` |
| 2672 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:31:31 | fonte: `[nulo_inesperado]` |
| 2673 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:31:31 | fonte_citada: `nulo_inesperado` |
| 2674 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:31:31 | quatro_linhas_presentes: confere |
| 2675 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:31:31 | rotulo_no_conjunto: confere |
| 2676 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:31:31 | fonte_existe_na_biblioteca: confere |
| 2677 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:31:31 | fonte_estava_no_contexto: confere |
| 2678 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:31:31 | campo_existe_no_caso: confere |
| 2679 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:31:31 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2680 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:31:31 | notas_nos_verbetes_citados: informativo |
| 2681 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:31:31 | impacto: nao_verificavel |
| 2682 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:31:31 | fonte_formato_valido: confere |
| 2683 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:31:31 | fonte_contem_termo_da_causa: confere |
| 2684 | 23 | decisao | programa | ao_vivo | 2026-11-05T01:31:31 | diagnostico: escolha nulo_inesperado; divergência não |

</details>

Nós de decisão:

- evento 2663, `poda`: escolha `json/lista; id:tipo_diferente, preco:nulo_inesperado`; resultado sinais_em_codigo; evidência: evento 2662 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id, preco (gen_ai: plan)
- evento 2665, `recuperacao`: escolha `entidade-produto,nulo_inesperado,contrato-produto`; resultado verbetes_entregues; evidência: evento 2664 (verbete_entregue, entidade-produto), evento 2664 (verbete_entregue, nulo_inesperado), evento 2664 (verbete_entregue, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, nulo_inesperado, contrato-produto (gen_ai: retrieval)
- evento 2684, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 2662 (sinal_em_codigo), evento 2664 (verbete_entregue, entidade-produto), evento 2664 (verbete_entregue, nulo_inesperado), evento 2664 (verbete_entregue, contrato-produto), evento 2668 (resposta), evento 2673 (verbete_citado, nulo_inesperado); divergência: não; falha: nenhuma; prov.used: entidade-produto, nulo_inesperado, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2661 a 2684 da trilha; hash dos eventos deste caso: `c81078afe53c9c50`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
