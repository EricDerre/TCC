<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-1@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-1@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `preco` · selo de probabilidade: **medio** (p = 0,97)

**IMPACTO (declarado):** `A ordenação incorreta do preço afeta a exibição ordenada dos produtos no front-end.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo preco porque o sinal preco: esperado numero, recebido texto está presente na resposta HTTP e os verbetes entidade-produto, tipo_divergente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,02. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 499): regras diff_contra_contrato; antes {"chars": 152}, depois {"chars": 152}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | numero | texto |

Trecho podado (hash `20cdbc76d4a473bf`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": "89.90", "imagem": "picanha_alho.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

tipo_divergente e não valor_fora_do_dominio: a escolha tem probabilidade 0,97 contra 0,02; verbete(s) na evidência: entidade-produto, tipo_divergente, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,97 | sim |
| valor_fora_do_dominio | 0,02 |  |
| formato_de_data_divergente | 0,01 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tipo_divergente] [entidade-produto]`; verbetes citados: `tipo_divergente`, `entidade-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `entidade-produto`, `tipo_divergente`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `tipo_divergente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `tipo_divergente`, `contrato-produto` |
| fonte_formato_valido | `[tipo_divergente] [entidade-produto]` | confere | {"ids": ["tipo_divergente", "entidade-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `entidade-produto` | confere | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids semt-1 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 498 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:29:45 | caso semt-1@sonda |
| 499 | 2 | poda | programa | ao_vivo | 2026-11-04T23:29:45 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 500 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:29:45 | poda: escolha json/lista; preco:tipo_diferente; divergência não |
| 501 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:29:45 | 3 de 39 verbetes entregues |
| 502 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:29:45 | recuperacao: escolha entidade-produto,tipo_divergente,contrato-produto; divergência não |
| 504 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:29:45 | {"etapa": "diagnostico", "sha": "21093d988e603cbb", "prompt_sha256": "21093d988e60", "chars": 3673, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 506 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:29:45 | diagnostico: 71,4 s |
| 507 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:29:45 | causa_raiz: `tipo_divergente` |
| 508 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:29:45 | campo: `preco` |
| 509 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:29:45 | impacto: `A ordenação incorreta do preço afeta a exibição ordenada dos produtos no front-end.` |
| 510 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:29:45 | fonte: `[tipo_divergente] [entidade-produto]` |
| 511 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:29:45 | fonte_citada: `tipo_divergente` |
| 512 | 13 | declaracao | modelo | ao_vivo | 2026-11-04T23:29:45 | fonte_citada: `entidade-produto` |
| 513 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:29:45 | quatro_linhas_presentes: confere |
| 514 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:29:45 | rotulo_no_conjunto: confere |
| 515 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:29:45 | fonte_existe_na_biblioteca: confere |
| 516 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:29:45 | fonte_existe_na_biblioteca: confere |
| 517 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:29:45 | fonte_estava_no_contexto: confere |
| 518 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:29:45 | fonte_estava_no_contexto: confere |
| 519 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:29:45 | campo_existe_no_caso: confere |
| 520 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:29:45 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 521 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:29:45 | notas_nos_verbetes_citados: informativo |
| 522 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T23:29:45 | impacto: nao_verificavel |
| 523 | 24 | verificacao | verificacao | ao_vivo | 2026-11-04T23:29:45 | fonte_formato_valido: confere |
| 524 | 25 | verificacao | verificacao | ao_vivo | 2026-11-04T23:29:45 | fonte_contem_termo_da_causa: confere |
| 525 | 26 | verificacao | verificacao | ao_vivo | 2026-11-04T23:29:45 | fonte_contem_termo_da_causa: confere |
| 526 | 27 | decisao | programa | ao_vivo | 2026-11-04T23:29:45 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 500, `poda`: escolha `json/lista; preco:tipo_diferente`; resultado sinais_em_codigo; evidência: evento 499 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: preco (gen_ai: plan)
- evento 502, `recuperacao`: escolha `entidade-produto,tipo_divergente,contrato-produto`; resultado verbetes_entregues; evidência: evento 501 (verbete_entregue, entidade-produto), evento 501 (verbete_entregue, tipo_divergente), evento 501 (verbete_entregue, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, tipo_divergente, contrato-produto (gen_ai: retrieval)
- evento 526, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 499 (sinal_em_codigo), evento 501 (verbete_entregue, entidade-produto), evento 501 (verbete_entregue, tipo_divergente), evento 501 (verbete_entregue, contrato-produto), evento 506 (resposta), evento 511 (verbete_citado, tipo_divergente), evento 512 (verbete_citado, entidade-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, tipo_divergente, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 498 a 526 da trilha; hash dos eventos deste caso: `49f8f71501fe6c2f`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
