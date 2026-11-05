<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-8`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-8@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `nulo_inesperado` · **CAMPO:** `preco` · selo de probabilidade: **medio** (p = 0,86) · **CONFLITO**: a remoção do verbete nulo_inesperado mudou a resposta de nulo_inesperado para tipo_divergente; a troca do verbete nulo_inesperado por um errado mudou a resposta de nulo_inesperado para valor_fora_do_dominio; a inferência sem documentação mudou a resposta de nulo_inesperado para valor_fora_do_dominio

**IMPACTO (declarado):** `O usuário vê 'R$ 0,00' em vez do preço correto de R$ 89,90.`

Justificativa (gerada por molde): O agente respondeu nulo_inesperado no campo preco porque o sinal preco: esperado numero, recebido nulo está presente na resposta HTTP e os verbetes entidade-produto, nulo_inesperado, contrato-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,08. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete nulo_inesperado mudou a resposta (de nulo_inesperado para tipo_divergente), então ele pesou na decisão. A troca do verbete nulo_inesperado por um verbete errado mudou a resposta (de nulo_inesperado para valor_fora_do_dominio). A inferência sem documentação mudou a resposta (de nulo_inesperado para valor_fora_do_dominio). A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a remoção do verbete nulo_inesperado mudou a resposta de nulo_inesperado para tipo_divergente; a troca do verbete nulo_inesperado por um errado mudou a resposta de nulo_inesperado para valor_fora_do_dominio; a inferência sem documentação mudou a resposta de nulo_inesperado para valor_fora_do_dominio.

## 2. Evidência

Poda de `corpo_http` (evento 2574): regras diff_contra_contrato; antes {"chars": 149}, depois {"chars": 149}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | numero | nulo |

Trecho podado (hash `c36e9bb22382f8e9`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": null, "imagem": "picanha_alho.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

nulo_inesperado e não tipo_divergente: a escolha tem probabilidade 0,86 contra 0,08; verbete(s) na evidência: entidade-produto, nulo_inesperado, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| nulo_inesperado | 0,86 | sim |
| tipo_divergente | 0,08 |  |
| valor_fora_do_dominio | 0,05 |  |
| formato_de_data_divergente | 0,01 |  |
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

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `nulo_inesperado` | nulo_inesperado | tipo_divergente | 0,86 | 0,00 | mudou a resposta: o verbete pesou na decisão |
| troca | `nulo_inesperado` | nulo_inesperado | valor_fora_do_dominio | 0,86 | 0,04 | mudou a resposta: o verbete pesou na decisão |
| sem_documentacao | `` | nulo_inesperado | valor_fora_do_dominio | 0,86 | 0,00 | mudou a resposta: o verbete pesou na decisão |
| repeticao_da_base | `` | nulo_inesperado | nulo_inesperado | 0,86 | 0,87 | sem efeito medido do contexto |

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids semt-8 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2572 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:27:05 | caso semt-8 |
| 2574 | 2 | poda | programa | ao_vivo | 2026-11-05T01:27:05 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2575 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:27:05 | poda: escolha json/lista; preco:nulo_inesperado; divergência não |
| 2576 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:27:05 | 3 de 39 verbetes entregues |
| 2577 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:27:05 | recuperacao: escolha entidade-produto,nulo_inesperado,contrato-produto; divergência não |
| 2579 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:27:05 | {"etapa": "diagnostico", "sha": "c24829ec7be8e8b1", "prompt_sha256": "c24829ec7be8", "chars": 3350, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2581 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:27:05 | diagnostico: 33,9 s |
| 2582 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:27:05 | causa_raiz: `nulo_inesperado` |
| 2583 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:27:05 | campo: `preco` |
| 2584 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:27:05 | impacto: `O usuário vê 'R$ 0,00' em vez do preço correto de R$ 89,90.` |
| 2585 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:27:05 | fonte: `[nulo_inesperado]` |
| 2586 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:27:05 | fonte_citada: `nulo_inesperado` |
| 2587 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T01:27:05 | quatro_linhas_presentes: confere |
| 2588 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:27:05 | rotulo_no_conjunto: confere |
| 2589 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:27:05 | fonte_existe_na_biblioteca: confere |
| 2590 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:27:05 | fonte_estava_no_contexto: confere |
| 2591 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:27:05 | campo_existe_no_caso: confere |
| 2592 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:27:05 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2593 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:27:05 | notas_nos_verbetes_citados: informativo |
| 2594 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:27:05 | impacto: nao_verificavel |
| 2595 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:27:05 | fonte_formato_valido: confere |
| 2596 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:27:05 | fonte_contem_termo_da_causa: confere |
| 2599 | 23 | inferencia | programa | ao_vivo | 2026-11-05T01:27:05 | intervencao:remocao: 35,5 s |
| 2600 | 24 | intervencao | verificacao | ao_vivo | 2026-11-05T01:27:05 | remocao de nulo_inesperado: rótulo nulo_inesperado para tipo_divergente |
| 2603 | 25 | inferencia | programa | ao_vivo | 2026-11-05T01:27:05 | intervencao:troca: 54,2 s |
| 2604 | 26 | intervencao | verificacao | ao_vivo | 2026-11-05T01:27:05 | troca de nulo_inesperado: rótulo nulo_inesperado para valor_fora_do_dominio |
| 2607 | 27 | inferencia | programa | ao_vivo | 2026-11-05T01:27:05 | intervencao:sem_documentacao: 31,5 s |
| 2608 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T01:27:05 | sem_documentacao de None: rótulo nulo_inesperado para valor_fora_do_dominio |
| 2609 | 29 | inferencia | programa | ao_vivo | 2026-11-05T01:27:05 | intervencao:repeticao_da_base: 16,2 s |
| 2610 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T01:27:05 | repeticao_da_base de None: rótulo nulo_inesperado para nulo_inesperado |
| 2611 | 31 | decisao | programa | ao_vivo | 2026-11-05T01:27:05 | diagnostico: escolha nulo_inesperado; divergência sim |

</details>

Nós de decisão:

- evento 2575, `poda`: escolha `json/lista; preco:nulo_inesperado`; resultado sinais_em_codigo; evidência: evento 2574 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: preco (gen_ai: plan)
- evento 2577, `recuperacao`: escolha `entidade-produto,nulo_inesperado,contrato-produto`; resultado verbetes_entregues; evidência: evento 2576 (verbete_entregue, entidade-produto), evento 2576 (verbete_entregue, nulo_inesperado), evento 2576 (verbete_entregue, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, nulo_inesperado, contrato-produto (gen_ai: retrieval)
- evento 2611, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 2574 (sinal_em_codigo), evento 2576 (verbete_entregue, entidade-produto), evento 2576 (verbete_entregue, nulo_inesperado), evento 2576 (verbete_entregue, contrato-produto), evento 2581 (resposta), evento 2586 (verbete_citado, nulo_inesperado); divergência: sim; falha: nenhuma; prov.used: entidade-produto, nulo_inesperado, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2572 a 2611 da trilha; hash dos eventos deste caso: `73a390b9a0523315`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
