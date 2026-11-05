<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-5@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/efe-5@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `localizador_quebrado` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,99)

**IMPACTO (declarado):** `O usuário não consegue acessar os detalhes do produto "Picanha ao Alho" corretamente.`

Justificativa (gerada por molde): O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, ancora-saiba-mais, corpo_nao_e_json estavam entre os entregues ao modelo. A segunda causa, nulo_inesperado, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 1640): regras diff_contra_contrato; antes {"chars": 27}, depois {"chars": 27}.

Trecho podado (hash `48ffb95010655367`):

```text
(nenhuma requisicao falhou)
```

## 3. Contraste com a segunda causa

localizador_quebrado e não nulo_inesperado: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: localizador_quebrado, ancora-saiba-mais, corpo_nao_e_json

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| localizador_quebrado | 0,99 | sim |
| nulo_inesperado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `ancora-saiba-mais`, `corpo_nao_e_json` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado`, `ancora-saiba-mais` |
| fonte_formato_valido | `[localizador_quebrado]` | confere | {"ids": ["localizador_quebrado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `localizador_quebrado` | confere | {"termo": "localizador_quebrado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids efe-5 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1639 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:37:52 | caso efe-5@sonda |
| 1640 | 2 | poda | programa | ao_vivo | 2026-11-05T00:37:52 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1641 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:37:52 | poda: escolha sem_contrato; divergência não |
| 1642 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:37:52 | 3 de 39 verbetes entregues |
| 1643 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:37:52 | recuperacao: escolha localizador_quebrado,ancora-saiba-mais,corpo_nao_e_json; divergência não |
| 1645 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:37:52 | {"etapa": "diagnostico", "sha": "f5a06891a410df44", "prompt_sha256": "f5a06891a410", "chars": 4164, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1646 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:37:52 | diagnostico: 62,7 s |
| 1647 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:37:52 | causa_raiz: `localizador_quebrado` |
| 1648 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:37:52 | campo: `nenhum` |
| 1649 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:37:52 | impacto: `O usuário não consegue acessar os detalhes do produto "Picanha ao Alho" corretamente.` |
| 1650 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:37:52 | fonte: `[localizador_quebrado]` |
| 1651 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:37:52 | fonte_citada: `localizador_quebrado` |
| 1652 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:37:52 | quatro_linhas_presentes: confere |
| 1653 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:37:52 | rotulo_no_conjunto: confere |
| 1654 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:37:52 | fonte_existe_na_biblioteca: confere |
| 1655 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:37:52 | fonte_estava_no_contexto: confere |
| 1656 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:37:52 | campo_existe_no_caso: nao_se_aplica |
| 1657 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:37:52 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1658 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:37:52 | notas_nos_verbetes_citados: informativo |
| 1659 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:37:52 | impacto: nao_verificavel |
| 1660 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:37:52 | fonte_formato_valido: confere |
| 1661 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:37:52 | fonte_contem_termo_da_causa: confere |
| 1662 | 23 | decisao | programa | ao_vivo | 2026-11-05T00:37:52 | diagnostico: escolha localizador_quebrado; divergência não |

</details>

Nós de decisão:

- evento 1641, `poda`: escolha `sem_contrato`; resultado sem_contrato; evidência: evento 1640 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1643, `recuperacao`: escolha `localizador_quebrado,ancora-saiba-mais,corpo_nao_e_json`; resultado verbetes_entregues; evidência: evento 1642 (verbete_entregue, localizador_quebrado), evento 1642 (verbete_entregue, ancora-saiba-mais), evento 1642 (verbete_entregue, corpo_nao_e_json); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, ancora-saiba-mais, corpo_nao_e_json (gen_ai: retrieval)
- evento 1662, `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido; evidência: evento 1642 (verbete_entregue, localizador_quebrado), evento 1642 (verbete_entregue, ancora-saiba-mais), evento 1642 (verbete_entregue, corpo_nao_e_json), evento 1646 (resposta), evento 1651 (verbete_citado, localizador_quebrado); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, ancora-saiba-mais, corpo_nao_e_json (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1639 a 1662 da trilha; hash dos eventos deste caso: `c19a4425343e62e2`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
