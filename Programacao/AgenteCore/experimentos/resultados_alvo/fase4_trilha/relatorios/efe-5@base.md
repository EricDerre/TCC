<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-5`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/efe-5@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `localizador_quebrado` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,98) · **CONFLITO**: a remoção do verbete localizador_quebrado mudou a resposta de localizador_quebrado para registro_duplicado; a troca do verbete localizador_quebrado por um errado mudou a resposta de localizador_quebrado para estrutura_aninhada_divergente; a inferência sem documentação mudou a resposta de localizador_quebrado para registro_duplicado

**IMPACTO (declarado):** `O usuário não consegue acessar os detalhes do produto "Picanha ao Alho" corretamente.`

Justificativa (gerada por molde): O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, ancora-saiba-mais, corpo_nao_e_json estavam entre os entregues ao modelo. A segunda causa, nulo_inesperado, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete localizador_quebrado mudou a resposta (de localizador_quebrado para registro_duplicado), então ele pesou na decisão. A troca do verbete localizador_quebrado por um verbete errado mudou a resposta (de localizador_quebrado para estrutura_aninhada_divergente). A inferência sem documentação mudou a resposta (de localizador_quebrado para registro_duplicado). A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a remoção do verbete localizador_quebrado mudou a resposta de localizador_quebrado para registro_duplicado; a troca do verbete localizador_quebrado por um errado mudou a resposta de localizador_quebrado para estrutura_aninhada_divergente; a inferência sem documentação mudou a resposta de localizador_quebrado para registro_duplicado.

## 2. Evidência

Poda de `corpo_http` (evento 1601): regras diff_contra_contrato; antes {"chars": 27}, depois {"chars": 27}.

Trecho podado (hash `48ffb95010655367`):

```text
(nenhuma requisicao falhou)
```

## 3. Contraste com a segunda causa

localizador_quebrado e não nulo_inesperado: a escolha tem probabilidade 0,98 contra 0,00; verbete(s) na evidência: localizador_quebrado, ancora-saiba-mais, corpo_nao_e_json

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| localizador_quebrado | 0,98 | sim |
| nulo_inesperado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `ancora-saiba-mais`, `corpo_nao_e_json` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado`, `ancora-saiba-mais` |
| fonte_formato_valido | `[localizador_quebrado]` | confere | {"ids": ["localizador_quebrado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `localizador_quebrado` | confere | {"termo": "localizador_quebrado"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `localizador_quebrado` | localizador_quebrado | registro_duplicado | 0,98 | 0,00 | mudou a resposta: o verbete pesou na decisão |
| troca | `localizador_quebrado` | localizador_quebrado | estrutura_aninhada_divergente | 0,98 | 0,04 | mudou a resposta: o verbete pesou na decisão |
| sem_documentacao | `` | localizador_quebrado | registro_duplicado | 0,98 | 0,00 | mudou a resposta: o verbete pesou na decisão |
| repeticao_da_base | `` | localizador_quebrado | localizador_quebrado | 0,98 | 0,99 | sem efeito medido do contexto |

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids efe-5 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1600 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:33:13 | caso efe-5 |
| 1601 | 2 | poda | programa | ao_vivo | 2026-11-05T00:33:13 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1602 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:33:13 | poda: escolha sem_contrato; divergência não |
| 1603 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:33:13 | 3 de 39 verbetes entregues |
| 1604 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:33:13 | recuperacao: escolha localizador_quebrado,ancora-saiba-mais,corpo_nao_e_json; divergência não |
| 1606 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:33:13 | {"etapa": "diagnostico", "sha": "7929a737345c27ba", "prompt_sha256": "7929a737345c", "chars": 4046, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1608 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:33:13 | diagnostico: 75,2 s |
| 1609 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:33:13 | causa_raiz: `localizador_quebrado` |
| 1610 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:33:13 | campo: `nenhum` |
| 1611 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:33:13 | impacto: `O usuário não consegue acessar os detalhes do produto "Picanha ao Alho" corretamente.` |
| 1612 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:33:13 | fonte: `[localizador_quebrado]` |
| 1613 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:33:13 | fonte_citada: `localizador_quebrado` |
| 1614 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:33:13 | quatro_linhas_presentes: confere |
| 1615 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:33:13 | rotulo_no_conjunto: confere |
| 1616 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:33:13 | fonte_existe_na_biblioteca: confere |
| 1617 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:33:13 | fonte_estava_no_contexto: confere |
| 1618 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:33:13 | campo_existe_no_caso: nao_se_aplica |
| 1619 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:33:13 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1620 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:33:13 | notas_nos_verbetes_citados: informativo |
| 1621 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:33:13 | impacto: nao_verificavel |
| 1622 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:33:13 | fonte_formato_valido: confere |
| 1623 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:33:13 | fonte_contem_termo_da_causa: confere |
| 1626 | 23 | inferencia | programa | ao_vivo | 2026-11-05T00:33:13 | intervencao:remocao: 65,5 s |
| 1627 | 24 | intervencao | verificacao | ao_vivo | 2026-11-05T00:33:13 | remocao de localizador_quebrado: rótulo localizador_quebrado para registro_duplicado |
| 1630 | 25 | inferencia | programa | ao_vivo | 2026-11-05T00:33:13 | intervencao:troca: 73,9 s |
| 1631 | 26 | intervencao | verificacao | ao_vivo | 2026-11-05T00:33:13 | troca de localizador_quebrado: rótulo localizador_quebrado para estrutura_aninhada_divergente |
| 1634 | 27 | inferencia | programa | ao_vivo | 2026-11-05T00:33:13 | intervencao:sem_documentacao: 44,5 s |
| 1635 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T00:33:13 | sem_documentacao de None: rótulo localizador_quebrado para registro_duplicado |
| 1636 | 29 | inferencia | programa | ao_vivo | 2026-11-05T00:33:13 | intervencao:repeticao_da_base: 15,4 s |
| 1637 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T00:33:13 | repeticao_da_base de None: rótulo localizador_quebrado para localizador_quebrado |
| 1638 | 31 | decisao | programa | ao_vivo | 2026-11-05T00:33:13 | diagnostico: escolha localizador_quebrado; divergência sim |

</details>

Nós de decisão:

- evento 1602, `poda`: escolha `sem_contrato`; resultado sem_contrato; evidência: evento 1601 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1604, `recuperacao`: escolha `localizador_quebrado,ancora-saiba-mais,corpo_nao_e_json`; resultado verbetes_entregues; evidência: evento 1603 (verbete_entregue, localizador_quebrado), evento 1603 (verbete_entregue, ancora-saiba-mais), evento 1603 (verbete_entregue, corpo_nao_e_json); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, ancora-saiba-mais, corpo_nao_e_json (gen_ai: retrieval)
- evento 1638, `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido; evidência: evento 1603 (verbete_entregue, localizador_quebrado), evento 1603 (verbete_entregue, ancora-saiba-mais), evento 1603 (verbete_entregue, corpo_nao_e_json), evento 1608 (resposta), evento 1613 (verbete_citado, localizador_quebrado); divergência: sim; falha: nenhuma; prov.used: localizador_quebrado, ancora-saiba-mais, corpo_nao_e_json (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1600 a 1638 da trilha; hash dos eventos deste caso: `11640578f06c2577`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
