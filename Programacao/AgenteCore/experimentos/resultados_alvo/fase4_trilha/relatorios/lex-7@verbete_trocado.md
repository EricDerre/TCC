<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-7@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/lex-7@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `resposta_truncada` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,71) · **CONFLITO**: nenhum verbete entregue trata da causa respondida resposta_truncada

**IMPACTO (declarado):** `A tela de detalhe abre em branco, sem mensagem de erro, pois a resposta da API é truncada e não contém os dados do produto.`

Justificativa (gerada por molde): O agente respondeu resposta_truncada porque o sinal esperado JSON completo e válido, recebido corpo vazio está presente na resposta HTTP e os verbetes recurso_inexistente, ancora-saiba-mais, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,11. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida resposta_truncada. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,71); trate como hipótese e confira o caso antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 1754): regras diff_contra_contrato; antes {"chars": 0}, depois {"chars": 0}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo vazio |

Trecho podado (hash `e3b0c44298fc1c14`):

```text

```

## 3. Contraste com a segunda causa

resposta_truncada e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 0,71 contra 0,11; verbete(s) na evidência: recurso_inexistente, ancora-saiba-mais, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| resposta_truncada | 0,71 | sim |
| colecao_no_lugar_de_objeto | 0,11 |  |
| corpo_nao_e_json | 0,10 |  |
| corpo_vazio | 0,10 |  |
| campo_ausente | 0,03 |  |
| campo_renomeado | 0,03 |  |
| tipo_divergente | 0,01 |  |
| nulo_inesperado | 0,01 |  |
| recurso_inexistente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[recurso_inexistente]`; verbetes citados: `recurso_inexistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `recurso_inexistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `recurso_inexistente` | confere | contexto: `recurso_inexistente`, `ancora-saiba-mais`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[recurso_inexistente]` | confere | {"ids": ["recurso_inexistente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `recurso_inexistente` | **não confere** | {"termo": "resposta_truncada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids lex-7 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1753 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:44:19 | caso lex-7@verbete_trocado |
| 1754 | 2 | poda | programa | ao_vivo | 2026-11-05T00:44:19 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1755 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:44:19 | poda: escolha vazio; divergência não |
| 1756 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:44:19 | 3 de 39 verbetes entregues |
| 1757 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:44:19 | recuperacao: escolha recurso_inexistente,ancora-saiba-mais,colecao_no_lugar_de_objeto; divergência não |
| 1758 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:44:19 | {"etapa": "diagnostico", "sha": "34850b10fe63ae17", "prompt_sha256": "34850b10fe63", "chars": 3490, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1760 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:44:19 | diagnostico: 16,8 s |
| 1761 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:44:19 | causa_raiz: `resposta_truncada` |
| 1762 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:44:19 | campo: `nenhum` |
| 1763 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:44:19 | impacto: `A tela de detalhe abre em branco, sem mensagem de erro, pois a resposta da API é truncada e não contém os dados do produto.` |
| 1764 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:44:19 | fonte: `[recurso_inexistente]` |
| 1765 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:44:19 | fonte_citada: `recurso_inexistente` |
| 1766 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:44:19 | quatro_linhas_presentes: confere |
| 1767 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:44:19 | rotulo_no_conjunto: confere |
| 1768 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:44:19 | fonte_existe_na_biblioteca: confere |
| 1769 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:44:19 | fonte_estava_no_contexto: confere |
| 1770 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:44:19 | campo_existe_no_caso: nao_se_aplica |
| 1771 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:44:19 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 1772 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:44:19 | notas_nos_verbetes_citados: informativo |
| 1773 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:44:19 | impacto: nao_verificavel |
| 1774 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:44:19 | fonte_formato_valido: confere |
| 1775 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:44:19 | fonte_contem_termo_da_causa: nao_confere |
| 1776 | 23 | decisao | programa | ao_vivo | 2026-11-05T00:44:19 | diagnostico: escolha resposta_truncada; divergência sim |

</details>

Nós de decisão:

- evento 1755, `poda`: escolha `vazio`; resultado sinais_em_codigo; evidência: evento 1754 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1757, `recuperacao`: escolha `recurso_inexistente,ancora-saiba-mais,colecao_no_lugar_de_objeto`; resultado verbetes_entregues; evidência: evento 1756 (verbete_entregue, recurso_inexistente), evento 1756 (verbete_entregue, ancora-saiba-mais), evento 1756 (verbete_entregue, colecao_no_lugar_de_objeto); divergência: não; falha: nenhuma; prov.used: recurso_inexistente, ancora-saiba-mais, colecao_no_lugar_de_objeto (gen_ai: retrieval)
- evento 1776, `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido; evidência: evento 1754 (sinal_em_codigo), evento 1756 (verbete_entregue, recurso_inexistente), evento 1756 (verbete_entregue, ancora-saiba-mais), evento 1756 (verbete_entregue, colecao_no_lugar_de_objeto), evento 1760 (resposta), evento 1765 (verbete_citado, recurso_inexistente); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: recurso_inexistente, ancora-saiba-mais, colecao_no_lugar_de_objeto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1753 a 1776 da trilha; hash dos eventos deste caso: `edfab0cab073fbdf`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
