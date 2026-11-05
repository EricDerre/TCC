<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-14`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-14@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `nulo_inesperado` · **CAMPO:** `tipo` · selo de probabilidade: **baixo** (p = 0,74) · **CONFLITO**: a inferência sem documentação mudou a resposta de nulo_inesperado para tipo_divergente

**IMPACTO (declarado):** `O filtro por categoria não exibe corretamente os produtos, pois alguns tipos estão ausentes na resposta.`

Justificativa (gerada por molde): O agente respondeu nulo_inesperado no campo tipo porque os verbetes entidade-produto, contrato-produto, nulo_inesperado estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,25. A FONTE cita 2 verbete(s), todos presentes no contexto. A remoção do verbete contrato-produto não mudou a resposta: sem efeito medido do contexto. A troca do verbete contrato-produto por um verbete errado não mudou a resposta: sem efeito medido do contexto. A inferência sem documentação mudou a resposta (de nulo_inesperado para tipo_divergente). (a probabilidade registrada é só um limite inferior: o rótulo saiu das alternativas devolvidas) A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a inferência sem documentação mudou a resposta de nulo_inesperado para tipo_divergente. O agente não está seguro desta causa (probabilidade 0,74); trate como hipótese e confira o campo tipo antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 2802): regras diff_contra_contrato; antes {"chars": 272}, depois {"chars": 272}.

Trecho podado (hash `10463dd6558b8e48`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 8, "nome": "Agua Mineral", "resumo": "500ml", "tipo": null, "preco": 6.0, "imagem": "agua.png", "destaque": false}]
```

## 3. Contraste com a segunda causa

nulo_inesperado e não tipo_divergente: a escolha tem probabilidade 0,74 contra 0,25; verbete(s) na evidência: entidade-produto, contrato-produto, nulo_inesperado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| nulo_inesperado | 0,74 | sim |
| tipo_divergente | 0,25 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| valor_fora_do_dominio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [nulo_inesperado]`; verbetes citados: `contrato-produto`, `nulo_inesperado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `nulo_inesperado` |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `entidade-produto`, `contrato-produto`, `nulo_inesperado` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `nulo_inesperado` |
| fonte_formato_valido | `[contrato-produto], [nulo_inesperado]` | confere | {"ids": ["contrato-produto", "nulo_inesperado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "nulo_inesperado"} |
| fonte_contem_termo_da_causa | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `contrato-produto` | nulo_inesperado | nulo_inesperado | 0,74 | 0,93 | sem efeito medido do contexto |
| troca | `contrato-produto` | nulo_inesperado | nulo_inesperado | 0,74 | 0,94 | sem efeito medido do contexto |
| sem_documentacao | `` | nulo_inesperado | tipo_divergente | 0,74 | 0,00 | mudou a resposta: o verbete pesou na decisão (só um limite inferior da queda: o rótulo saiu das alternativas devolvidas) |
| repeticao_da_base | `` | nulo_inesperado | nulo_inesperado | 0,74 | 0,70 | sem efeito medido do contexto |

## 5. Linha de ação

Confira o campo `tipo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids semt-14 --sem-seletor`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2800 | 1 | entrada | programa | ao_vivo | 2026-11-05T01:37:37 | caso semt-14 |
| 2802 | 2 | poda | programa | ao_vivo | 2026-11-05T01:37:37 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2803 | 3 | decisao | programa | ao_vivo | 2026-11-05T01:37:37 | poda: escolha json/lista; sem diferença; divergência não |
| 2804 | 4 | candidatos | programa | ao_vivo | 2026-11-05T01:37:37 | 3 de 39 verbetes entregues |
| 2805 | 5 | decisao | programa | ao_vivo | 2026-11-05T01:37:37 | recuperacao: escolha entidade-produto,contrato-produto,nulo_inesperado; divergência não |
| 2807 | 6 | prompt | programa | ao_vivo | 2026-11-05T01:37:37 | {"etapa": "diagnostico", "sha": "4f40cbe2904603c7", "prompt_sha256": "4f40cbe29046", "chars": 3495, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2809 | 7 | inferencia | programa | ao_vivo | 2026-11-05T01:37:37 | diagnostico: 51,0 s |
| 2810 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T01:37:37 | causa_raiz: `nulo_inesperado` |
| 2811 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T01:37:37 | campo: `tipo` |
| 2812 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T01:37:37 | impacto: `O filtro por categoria não exibe corretamente os produtos, pois alguns tipos estão ausentes na resposta.` |
| 2813 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T01:37:37 | fonte: `[contrato-produto], [nulo_inesperado]` |
| 2814 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T01:37:37 | fonte_citada: `contrato-produto` |
| 2815 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T01:37:37 | fonte_citada: `nulo_inesperado` |
| 2816 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T01:37:37 | quatro_linhas_presentes: confere |
| 2817 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T01:37:37 | rotulo_no_conjunto: confere |
| 2818 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T01:37:37 | fonte_existe_na_biblioteca: confere |
| 2819 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T01:37:37 | fonte_existe_na_biblioteca: confere |
| 2820 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T01:37:37 | fonte_estava_no_contexto: confere |
| 2821 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T01:37:37 | fonte_estava_no_contexto: confere |
| 2822 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T01:37:37 | campo_existe_no_caso: confere |
| 2823 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T01:37:37 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2824 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T01:37:37 | notas_nos_verbetes_citados: informativo |
| 2825 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T01:37:37 | impacto: nao_verificavel |
| 2826 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T01:37:37 | fonte_formato_valido: confere |
| 2827 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T01:37:37 | fonte_contem_termo_da_causa: nao_confere |
| 2828 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T01:37:37 | fonte_contem_termo_da_causa: confere |
| 2831 | 27 | inferencia | programa | ao_vivo | 2026-11-05T01:37:37 | intervencao:remocao: 49,0 s |
| 2832 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T01:37:37 | remocao de contrato-produto: rótulo nulo_inesperado para nulo_inesperado |
| 2835 | 29 | inferencia | programa | ao_vivo | 2026-11-05T01:37:37 | intervencao:troca: 50,1 s |
| 2836 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T01:37:37 | troca de contrato-produto: rótulo nulo_inesperado para nulo_inesperado |
| 2839 | 31 | inferencia | programa | ao_vivo | 2026-11-05T01:37:37 | intervencao:sem_documentacao: 30,6 s |
| 2840 | 32 | intervencao | verificacao | ao_vivo | 2026-11-05T01:37:37 | sem_documentacao de None: rótulo nulo_inesperado para tipo_divergente |
| 2841 | 33 | inferencia | programa | ao_vivo | 2026-11-05T01:37:37 | intervencao:repeticao_da_base: 15,9 s |
| 2842 | 34 | intervencao | verificacao | ao_vivo | 2026-11-05T01:37:37 | repeticao_da_base de None: rótulo nulo_inesperado para nulo_inesperado |
| 2843 | 35 | decisao | programa | ao_vivo | 2026-11-05T01:37:37 | diagnostico: escolha nulo_inesperado; divergência sim |

</details>

Nós de decisão:

- evento 2803, `poda`: escolha `json/lista; sem diferença`; resultado sinais_em_codigo; evidência: evento 2802 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 2805, `recuperacao`: escolha `entidade-produto,contrato-produto,nulo_inesperado`; resultado verbetes_entregues; evidência: evento 2804 (verbete_entregue, entidade-produto), evento 2804 (verbete_entregue, contrato-produto), evento 2804 (verbete_entregue, nulo_inesperado); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, nulo_inesperado (gen_ai: retrieval)
- evento 2843, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 2804 (verbete_entregue, entidade-produto), evento 2804 (verbete_entregue, contrato-produto), evento 2804 (verbete_entregue, nulo_inesperado), evento 2809 (resposta), evento 2814 (verbete_citado, contrato-produto), evento 2815 (verbete_citado, nulo_inesperado); divergência: sim; falha: nenhuma; prov.used: entidade-produto, contrato-produto, nulo_inesperado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2800 a 2843 da trilha; hash dos eventos deste caso: `f3e576e89201ef71`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
