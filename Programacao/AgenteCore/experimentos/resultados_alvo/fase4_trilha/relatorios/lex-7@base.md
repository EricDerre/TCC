<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-7`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/lex-7@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `corpo_vazio` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: a remoção do verbete corpo_vazio mudou a resposta de corpo_vazio para resposta_truncada; a troca do verbete corpo_vazio por um errado mudou a resposta de corpo_vazio para resposta_truncada; a inferência sem documentação mudou a resposta de corpo_vazio para resposta_truncada

**IMPACTO (declarado):** `A tela de detalhe abre em branco, sem exibir nenhum conteúdo ou mensagem de erro.`

Justificativa (gerada por molde): O agente respondeu corpo_vazio porque o sinal esperado JSON completo e válido, recebido corpo vazio está presente na resposta HTTP e os verbetes corpo_vazio, ancora-saiba-mais, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete corpo_vazio mudou a resposta (de corpo_vazio para resposta_truncada), então ele pesou na decisão. A troca do verbete corpo_vazio por um verbete errado mudou a resposta (de corpo_vazio para resposta_truncada). A inferência sem documentação mudou a resposta (de corpo_vazio para resposta_truncada). A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a remoção do verbete corpo_vazio mudou a resposta de corpo_vazio para resposta_truncada; a troca do verbete corpo_vazio por um errado mudou a resposta de corpo_vazio para resposta_truncada; a inferência sem documentação mudou a resposta de corpo_vazio para resposta_truncada.

## 2. Evidência

Poda de `corpo_http` (evento 1690): regras diff_contra_contrato; antes {"chars": 0}, depois {"chars": 0}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo vazio |

Trecho podado (hash `e3b0c44298fc1c14`):

```text

```

## 3. Contraste com a segunda causa

corpo_vazio e não resposta_truncada: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: corpo_vazio, ancora-saiba-mais, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| corpo_vazio | 1,00 | sim |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[corpo_vazio]`; verbetes citados: `corpo_vazio`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `corpo_vazio` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `corpo_vazio` | confere | contexto: `corpo_vazio`, `ancora-saiba-mais`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `corpo_vazio` | confere | verbetes: `corpo_vazio` |
| fonte_formato_valido | `[corpo_vazio]` | confere | {"ids": ["corpo_vazio"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `corpo_vazio` | confere | {"termo": "corpo_vazio"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `corpo_vazio` | corpo_vazio | resposta_truncada | 1,00 | 0,06 | mudou a resposta: o verbete pesou na decisão |
| troca | `corpo_vazio` | corpo_vazio | resposta_truncada | 1,00 | 0,07 | mudou a resposta: o verbete pesou na decisão |
| sem_documentacao | `` | corpo_vazio | resposta_truncada | 1,00 | 0,00 | mudou a resposta: o verbete pesou na decisão |
| repeticao_da_base | `` | corpo_vazio | corpo_vazio | 1,00 | 1,00 | sem efeito medido do contexto |

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids lex-7 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1688 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:39:20 | caso lex-7 |
| 1690 | 2 | poda | programa | ao_vivo | 2026-11-05T00:39:20 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1691 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:39:20 | poda: escolha vazio; divergência não |
| 1692 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:39:20 | 3 de 39 verbetes entregues |
| 1693 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:39:20 | recuperacao: escolha corpo_vazio,ancora-saiba-mais,colecao_no_lugar_de_objeto; divergência não |
| 1695 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:39:20 | {"etapa": "diagnostico", "sha": "a67870dd2d9b579b", "prompt_sha256": "a67870dd2d9b", "chars": 3534, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1697 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:39:20 | diagnostico: 65,0 s |
| 1698 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:39:20 | causa_raiz: `corpo_vazio` |
| 1699 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:39:20 | campo: `nenhum` |
| 1700 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:39:20 | impacto: `A tela de detalhe abre em branco, sem exibir nenhum conteúdo ou mensagem de erro.` |
| 1701 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:39:20 | fonte: `[corpo_vazio]` |
| 1702 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:39:20 | fonte_citada: `corpo_vazio` |
| 1703 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:39:20 | quatro_linhas_presentes: confere |
| 1704 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:39:20 | rotulo_no_conjunto: confere |
| 1705 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:39:20 | fonte_existe_na_biblioteca: confere |
| 1706 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:39:20 | fonte_estava_no_contexto: confere |
| 1707 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:39:20 | campo_existe_no_caso: nao_se_aplica |
| 1708 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:39:20 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1709 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:39:20 | notas_nos_verbetes_citados: informativo |
| 1710 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:39:20 | impacto: nao_verificavel |
| 1711 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:39:20 | fonte_formato_valido: confere |
| 1712 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:39:20 | fonte_contem_termo_da_causa: confere |
| 1715 | 23 | inferencia | programa | ao_vivo | 2026-11-05T00:39:20 | intervencao:remocao: 58,2 s |
| 1716 | 24 | intervencao | verificacao | ao_vivo | 2026-11-05T00:39:20 | remocao de corpo_vazio: rótulo corpo_vazio para resposta_truncada |
| 1719 | 25 | inferencia | programa | ao_vivo | 2026-11-05T00:39:20 | intervencao:troca: 66,6 s |
| 1720 | 26 | intervencao | verificacao | ao_vivo | 2026-11-05T00:39:20 | troca de corpo_vazio: rótulo corpo_vazio para resposta_truncada |
| 1723 | 27 | inferencia | programa | ao_vivo | 2026-11-05T00:39:20 | intervencao:sem_documentacao: 34,6 s |
| 1724 | 28 | intervencao | verificacao | ao_vivo | 2026-11-05T00:39:20 | sem_documentacao de None: rótulo corpo_vazio para resposta_truncada |
| 1726 | 29 | inferencia | programa | ao_vivo | 2026-11-05T00:39:20 | intervencao:repeticao_da_base: 13,4 s |
| 1727 | 30 | intervencao | verificacao | ao_vivo | 2026-11-05T00:39:20 | repeticao_da_base de None: rótulo corpo_vazio para corpo_vazio |
| 1728 | 31 | decisao | programa | ao_vivo | 2026-11-05T00:39:20 | diagnostico: escolha corpo_vazio; divergência sim |

</details>

Nós de decisão:

- evento 1691, `poda`: escolha `vazio`; resultado sinais_em_codigo; evidência: evento 1690 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1693, `recuperacao`: escolha `corpo_vazio,ancora-saiba-mais,colecao_no_lugar_de_objeto`; resultado verbetes_entregues; evidência: evento 1692 (verbete_entregue, corpo_vazio), evento 1692 (verbete_entregue, ancora-saiba-mais), evento 1692 (verbete_entregue, colecao_no_lugar_de_objeto); divergência: não; falha: nenhuma; prov.used: corpo_vazio, ancora-saiba-mais, colecao_no_lugar_de_objeto (gen_ai: retrieval)
- evento 1728, `diagnostico`: escolha `corpo_vazio`; resultado rotulo_emitido; evidência: evento 1690 (sinal_em_codigo), evento 1692 (verbete_entregue, corpo_vazio), evento 1692 (verbete_entregue, ancora-saiba-mais), evento 1692 (verbete_entregue, colecao_no_lugar_de_objeto), evento 1697 (resposta), evento 1702 (verbete_citado, corpo_vazio); divergência: sim; falha: nenhuma; prov.used: corpo_vazio, ancora-saiba-mais, colecao_no_lugar_de_objeto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1688 a 1728 da trilha; hash dos eventos deste caso: `12cf1ad7951bde7f`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
