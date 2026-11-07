<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-24`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/semt-24@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `destaque` · selo de probabilidade: **alto** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê "destaque: True" e "destaque: False" em inglês, em vez de "destaque: Sim" e "destaque: Não".`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo destaque porque os verbetes entidade-produto, tipo_divergente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": "True"}, {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 84.9, "imagem": "picanha_sem.jpg", "destaque": "False"}]

SINTOMA OBSERVADO: Nos cartoes da grade, a linha de destaque mostra 'destaque: True' e 'destaque: False' (em ingles, com inicial maiuscula) em vez de 'destaque: Sim' e 'destaque: Não'.
```

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: entidade-produto, tipo_divergente, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,99 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tipo_divergente]`; verbetes citados: `tipo_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `entidade-produto`, `tipo_divergente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `tipo_divergente`, `contrato-produto` |
| fonte_formato_valido | `[tipo_divergente]` | confere | {"ids": ["tipo_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `destaque` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids semt-24 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 899 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:59:48 | caso semt-24 |
| 900 | 2 | candidatos | programa | ao_vivo | 2026-11-06T11:59:48 | 3 de 39 verbetes entregues |
| 902 | 3 | prompt | programa | ao_vivo | 2026-11-06T11:59:48 | {"etapa": "diagnostico", "sha": "50caa34492c84cec", "prompt_sha256": "50caa34492c8", "chars": 3841, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 904 | 4 | inferencia | programa | ao_vivo | 2026-11-06T11:59:48 | diagnostico: 85,3 s |
| 905 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T11:59:48 | causa_raiz: `tipo_divergente` |
| 906 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T11:59:48 | campo: `destaque` |
| 907 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T11:59:48 | impacto: `O usuário vê "destaque: True" e "destaque: False" em inglês, em vez de "destaque: Sim" e "destaque: Não".` |
| 908 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T11:59:48 | fonte: `[tipo_divergente]` |
| 909 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T11:59:48 | fonte_citada: `tipo_divergente` |
| 910 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:59:48 | quatro_linhas_presentes: confere |
| 911 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:59:48 | rotulo_no_conjunto: confere |
| 912 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:59:48 | fonte_existe_na_biblioteca: confere |
| 913 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:59:48 | fonte_estava_no_contexto: confere |
| 914 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T11:59:48 | campo_existe_no_caso: confere |
| 915 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T11:59:48 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 916 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T11:59:48 | notas_nos_verbetes_citados: informativo |
| 917 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:59:48 | impacto: nao_verificavel |
| 918 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:59:48 | fonte_formato_valido: confere |
| 919 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:59:48 | fonte_contem_termo_da_causa: confere |
| 920 | 20 | decisao | programa | ao_vivo | 2026-11-06T11:59:48 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 920, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 900 (verbete_entregue, entidade-produto), evento 900 (verbete_entregue, tipo_divergente), evento 900 (verbete_entregue, contrato-produto), evento 904 (resposta), evento 909 (verbete_citado, tipo_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, tipo_divergente, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 899 a 920 da trilha; hash dos eventos deste caso: `b0353d1b96c68190`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
