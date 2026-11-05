<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-3@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/efe-3@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `resposta_truncada` · **CAMPO:** `imagem` · selo de probabilidade: **baixo** (p = 0,37) · **CONFLITO**: nenhum verbete entregue trata da causa respondida resposta_truncada

**IMPACTO (declarado):** `Os cartões aparecem sem foto nenhuma, pois a chave "imagem" está ausente na resposta.`

Justificativa (gerada por molde): O agente respondeu resposta_truncada no campo imagem porque o sinal imagem: esperado texto|nulo, recebido None está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, campo_ausente estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,21. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida resposta_truncada. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,37); trate como hipótese e confira o campo imagem antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 1522): regras diff_contra_contrato; antes {"chars": 119}, depois {"chars": 119}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| imagem | texto\|nulo |  |

Trecho podado (hash `55555e369bef5da7`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "destaque": true}]
```

## 3. Contraste com a segunda causa

resposta_truncada e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 0,37 contra 0,21; verbete(s) na evidência: entidade-produto, contrato-produto, campo_ausente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| resposta_truncada | 0,37 | sim |
| colecao_no_lugar_de_objeto | 0,21 |  |
| tipo_divergente | 0,18 |  |
| campo_ausente | 0,17 |  |
| campo_renomeado | 0,17 |  |
| corpo_nao_e_json | 0,04 |  |
| corpo_vazio | 0,04 |  |
| formato_de_data_divergente | 0,02 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente]`; verbetes citados: `campo_ausente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[campo_ausente]` | confere | {"ids": ["campo_ausente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_ausente` | **não confere** | {"termo": "resposta_truncada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `imagem` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids efe-3 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1521 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:31:07 | caso efe-3@sonda |
| 1522 | 2 | poda | programa | ao_vivo | 2026-11-05T00:31:07 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1523 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:31:07 | poda: escolha json/lista; imagem:ausente; divergência não |
| 1524 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:31:07 | 3 de 39 verbetes entregues |
| 1525 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:31:07 | recuperacao: escolha entidade-produto,contrato-produto,campo_ausente; divergência não |
| 1527 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:31:07 | {"etapa": "diagnostico", "sha": "faeaa65506a93668", "prompt_sha256": "faeaa65506a9", "chars": 3530, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1529 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:31:07 | diagnostico: 62,5 s |
| 1530 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:31:07 | causa_raiz: `resposta_truncada` |
| 1531 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:31:07 | campo: `imagem` |
| 1532 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:31:07 | impacto: `Os cartões aparecem sem foto nenhuma, pois a chave "imagem" está ausente na resposta.` |
| 1533 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:31:07 | fonte: `[campo_ausente]` |
| 1534 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:31:07 | fonte_citada: `campo_ausente` |
| 1535 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T00:31:07 | quatro_linhas_presentes: confere |
| 1536 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:31:07 | rotulo_no_conjunto: confere |
| 1537 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:31:07 | fonte_existe_na_biblioteca: confere |
| 1538 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:31:07 | fonte_estava_no_contexto: confere |
| 1539 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:31:07 | campo_existe_no_caso: confere |
| 1540 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:31:07 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 1541 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:31:07 | notas_nos_verbetes_citados: informativo |
| 1542 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:31:07 | impacto: nao_verificavel |
| 1543 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:31:07 | fonte_formato_valido: confere |
| 1544 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:31:07 | fonte_contem_termo_da_causa: nao_confere |
| 1545 | 23 | decisao | programa | ao_vivo | 2026-11-05T00:31:07 | diagnostico: escolha resposta_truncada; divergência sim |

</details>

Nós de decisão:

- evento 1523, `poda`: escolha `json/lista; imagem:ausente`; resultado sinais_em_codigo; evidência: evento 1522 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: imagem (gen_ai: plan)
- evento 1525, `recuperacao`: escolha `entidade-produto,contrato-produto,campo_ausente`; resultado verbetes_entregues; evidência: evento 1524 (verbete_entregue, entidade-produto), evento 1524 (verbete_entregue, contrato-produto), evento 1524 (verbete_entregue, campo_ausente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, campo_ausente (gen_ai: retrieval)
- evento 1545, `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido; evidência: evento 1522 (sinal_em_codigo), evento 1524 (verbete_entregue, entidade-produto), evento 1524 (verbete_entregue, contrato-produto), evento 1524 (verbete_entregue, campo_ausente), evento 1529 (resposta), evento 1534 (verbete_citado, campo_ausente); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, campo_ausente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1521 a 1545 da trilha; hash dos eventos deste caso: `ebad376d77531e02`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
