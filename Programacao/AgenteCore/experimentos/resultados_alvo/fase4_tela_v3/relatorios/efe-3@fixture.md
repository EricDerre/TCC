<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-3`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/efe-3@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `imagem` · selo de probabilidade: **baixo** (p = 0,57)

**IMPACTO (declarado):** `Os cartões aparecem sem foto nenhuma, pois o campo imagem está ausente na resposta.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo imagem porque os verbetes entidade-produto, contrato-produto, campo_ausente estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,26. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,57); trate como hipótese e confira o campo imagem antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "destaque": true}]

SINTOMA OBSERVADO: Os cartoes aparecem sem foto nenhuma (nem o espaco da imagem e desenhado), mas nome e preco corretos.
```

## 3. Contraste com a segunda causa

campo_ausente e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 0,57 contra 0,26; verbete(s) na evidência: entidade-produto, contrato-produto, campo_ausente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 0,57 | sim |
| colecao_no_lugar_de_objeto | 0,26 |  |
| resposta_truncada | 0,09 |  |
| tipo_divergente | 0,04 |  |
| corpo_nao_e_json | 0,03 |  |
| corpo_vazio | 0,03 |  |
| formato_de_data_divergente | 0,01 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente]`; verbetes citados: `campo_ausente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `contrato-produto`, `campo_ausente` |
| fonte_formato_valido | `[campo_ausente]` | confere | {"ids": ["campo_ausente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_ausente` | confere | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `imagem` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids efe-3 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 591 | 1 | entrada | programa | ao_vivo | 2026-11-05T19:01:49 | caso efe-3 |
| 592 | 2 | candidatos | programa | ao_vivo | 2026-11-05T19:01:49 | 3 de 39 verbetes entregues |
| 594 | 3 | prompt | programa | ao_vivo | 2026-11-05T19:01:49 | {"etapa": "diagnostico", "sha": "11a3fe94e7df2dcc", "prompt_sha256": "11a3fe94e7df", "chars": 3419, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 596 | 4 | inferencia | programa | ao_vivo | 2026-11-05T19:01:49 | diagnostico: 48,8 s |
| 597 | 5 | declaracao | modelo | ao_vivo | 2026-11-05T19:01:49 | causa_raiz: `campo_ausente` |
| 598 | 6 | declaracao | modelo | ao_vivo | 2026-11-05T19:01:49 | campo: `imagem` |
| 599 | 7 | declaracao | modelo | ao_vivo | 2026-11-05T19:01:49 | impacto: `Os cartões aparecem sem foto nenhuma, pois o campo imagem está ausente na resposta.` |
| 600 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T19:01:49 | fonte: `[campo_ausente]` |
| 601 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T19:01:49 | fonte_citada: `campo_ausente` |
| 602 | 10 | verificacao | verificacao | ao_vivo | 2026-11-05T19:01:49 | quatro_linhas_presentes: confere |
| 603 | 11 | verificacao | verificacao | ao_vivo | 2026-11-05T19:01:49 | rotulo_no_conjunto: confere |
| 604 | 12 | verificacao | verificacao | ao_vivo | 2026-11-05T19:01:49 | fonte_existe_na_biblioteca: confere |
| 605 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T19:01:49 | fonte_estava_no_contexto: confere |
| 606 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T19:01:49 | campo_existe_no_caso: confere |
| 607 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T19:01:49 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 608 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T19:01:49 | notas_nos_verbetes_citados: informativo |
| 609 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T19:01:49 | impacto: nao_verificavel |
| 610 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T19:01:49 | fonte_formato_valido: confere |
| 611 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T19:01:49 | fonte_contem_termo_da_causa: confere |
| 612 | 20 | decisao | programa | ao_vivo | 2026-11-05T19:01:49 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 612, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 592 (verbete_entregue, entidade-produto), evento 592 (verbete_entregue, contrato-produto), evento 592 (verbete_entregue, campo_ausente), evento 596 (resposta), evento 601 (verbete_citado, campo_ausente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, campo_ausente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 591 a 612 da trilha; hash dos eventos deste caso: `f710efc58c23cc79`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
