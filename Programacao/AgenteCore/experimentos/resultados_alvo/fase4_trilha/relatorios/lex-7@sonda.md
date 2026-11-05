<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-7@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/lex-7@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `corpo_vazio` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: faltam na resposta as linhas FONTE

**IMPACTO (declarado):** `A tela de detalhe abre em branco, sem exibir nenhum conteúdo ou mensagem de erro, pois a resposta da API está vazia.`

Justificativa (gerada por molde): O agente respondeu corpo_vazio porque o sinal esperado JSON completo e válido, recebido corpo vazio está presente na resposta HTTP e os verbetes corpo_vazio, ancora-saiba-mais, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,00. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): faltam na resposta as linhas FONTE. Este nó está marcado com a falha formato_das_quatro_linhas (origem: programa).

## 2. Evidência

Poda de `corpo_http` (evento 1730): regras diff_contra_contrato; antes {"chars": 0}, depois {"chars": 0}.

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

Linha FONTE como veio: **a linha não está na resposta**; verbetes citados: nenhum.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca |  | não se aplica | nenhum verbete citado na linha FONTE |
| O verbete citado estava no contexto entregue ao modelo |  | não se aplica | nenhum verbete citado na linha FONTE |
| Algum verbete do contexto trata da causa respondida | `corpo_vazio` | confere | verbetes: `corpo_vazio` |
| fonte_formato_valido |  | não se aplica | nenhum verbete citado na linha FONTE |
| fonte_contem_termo_da_causa |  | não se aplica | sem causa ou sem verbete citado |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids lex-7 --sem-seletor`

## 6. Árvore completa

<details><summary>22 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1729 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:43:22 | caso lex-7@sonda |
| 1730 | 2 | poda | programa | ao_vivo | 2026-11-05T00:43:22 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1731 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:43:22 | poda: escolha vazio; divergência não |
| 1732 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:43:22 | 3 de 39 verbetes entregues |
| 1733 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:43:22 | recuperacao: escolha corpo_vazio,ancora-saiba-mais,colecao_no_lugar_de_objeto; divergência não |
| 1735 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:43:22 | {"etapa": "diagnostico", "sha": "5012eef54cc89312", "prompt_sha256": "5012eef54cc8", "chars": 3643, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1737 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:43:22 | diagnostico: 53,7 s |
| 1738 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:43:22 | causa_raiz: `corpo_vazio` |
| 1739 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:43:22 | campo: `nenhum` |
| 1740 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:43:22 | impacto: `A tela de detalhe abre em branco, sem exibir nenhum conteúdo ou mensagem de erro, pois a resposta da API está vazia.` |
| 1741 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:43:22 | fonte: ausente |
| 1742 | 12 | verificacao | verificacao | ao_vivo | 2026-11-05T00:43:22 | quatro_linhas_presentes: nao_confere |
| 1743 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:43:22 | rotulo_no_conjunto: confere |
| 1744 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:43:22 | fonte_existe_na_biblioteca: nao_se_aplica |
| 1745 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:43:22 | fonte_estava_no_contexto: nao_se_aplica |
| 1746 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:43:22 | campo_existe_no_caso: nao_se_aplica |
| 1747 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:43:22 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1748 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:43:22 | notas_nos_verbetes_citados: nao_se_aplica |
| 1749 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:43:22 | impacto: nao_verificavel |
| 1750 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:43:22 | fonte_formato_valido: nao_se_aplica |
| 1751 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:43:22 | fonte_contem_termo_da_causa: nao_se_aplica |
| 1752 | 22 | decisao | programa | ao_vivo | 2026-11-05T00:43:22 | diagnostico: escolha corpo_vazio; divergência sim |

</details>

Nós de decisão:

- evento 1731, `poda`: escolha `vazio`; resultado sinais_em_codigo; evidência: evento 1730 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1733, `recuperacao`: escolha `corpo_vazio,ancora-saiba-mais,colecao_no_lugar_de_objeto`; resultado verbetes_entregues; evidência: evento 1732 (verbete_entregue, corpo_vazio), evento 1732 (verbete_entregue, ancora-saiba-mais), evento 1732 (verbete_entregue, colecao_no_lugar_de_objeto); divergência: não; falha: nenhuma; prov.used: corpo_vazio, ancora-saiba-mais, colecao_no_lugar_de_objeto (gen_ai: retrieval)
- evento 1752, `diagnostico`: escolha `corpo_vazio`; resultado rotulo_emitido; evidência: evento 1730 (sinal_em_codigo), evento 1732 (verbete_entregue, corpo_vazio), evento 1732 (verbete_entregue, ancora-saiba-mais), evento 1732 (verbete_entregue, colecao_no_lugar_de_objeto), evento 1737 (resposta); divergência: sim; falha: formato_das_quatro_linhas; prov.used: corpo_vazio, ancora-saiba-mais, colecao_no_lugar_de_objeto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1729 a 1752 da trilha; hash dos eventos deste caso: `99f9837ecab63bf5`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
