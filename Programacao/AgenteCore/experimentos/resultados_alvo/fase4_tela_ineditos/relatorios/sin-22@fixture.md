<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-22`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/sin-22@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `nome` · selo de probabilidade: **medio** (p = 0,94)

**IMPACTO (declarado):** `O título dos produtos na interface web não é exibido corretamente, mostrando '(sem nome)' em todos os cartões.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo nome porque os verbetes entidade-produto, contrato-produto, campo_ausente estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,04. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 5, "resumo": "Alcatra grelhada servida na pedra quente", "tipo": "Carnes", "preco": 74.9, "imagem": "alcatra_pedra.jpg", "destaque": false}, {"id": 6, "resumo": "Corte macio grelhado na brasa", "tipo": "Carnes", "preco": 72.9, "imagem": "maminha.jpg", "destaque": false}]

SINTOMA OBSERVADO: Todos os cartoes da grade aparecem com o titulo '(sem nome)'. As fotos, as descricoes, os precos e os botoes 'Saiba Mais...' continuam normais.
```

## 3. Contraste com a segunda causa

campo_ausente e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 0,94 contra 0,04; verbete(s) na evidência: entidade-produto, contrato-produto, campo_ausente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 0,94 | sim |
| colecao_no_lugar_de_objeto | 0,04 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

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

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids sin-22 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 377 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:41:14 | caso sin-22 |
| 378 | 2 | candidatos | programa | ao_vivo | 2026-11-06T11:41:14 | 3 de 39 verbetes entregues |
| 380 | 3 | prompt | programa | ao_vivo | 2026-11-06T11:41:14 | {"etapa": "diagnostico", "sha": "89680f6cdd0757e3", "prompt_sha256": "89680f6cdd07", "chars": 3621, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 382 | 4 | inferencia | programa | ao_vivo | 2026-11-06T11:41:14 | diagnostico: 54,6 s |
| 383 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T11:41:14 | causa_raiz: `campo_ausente` |
| 384 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T11:41:14 | campo: `nome` |
| 385 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T11:41:14 | impacto: `O título dos produtos na interface web não é exibido corretamente, mostrando '(sem nome)' em todos os cartões.` |
| 386 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T11:41:14 | fonte: `[campo_ausente]` |
| 387 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T11:41:14 | fonte_citada: `campo_ausente` |
| 388 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:41:14 | quatro_linhas_presentes: confere |
| 389 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:41:14 | rotulo_no_conjunto: confere |
| 390 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:41:14 | fonte_existe_na_biblioteca: confere |
| 391 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:41:14 | fonte_estava_no_contexto: confere |
| 392 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T11:41:14 | campo_existe_no_caso: confere |
| 393 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T11:41:14 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 394 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T11:41:14 | notas_nos_verbetes_citados: informativo |
| 395 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:41:14 | impacto: nao_verificavel |
| 396 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:41:14 | fonte_formato_valido: confere |
| 397 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:41:14 | fonte_contem_termo_da_causa: confere |
| 398 | 20 | decisao | programa | ao_vivo | 2026-11-06T11:41:14 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 398, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 378 (verbete_entregue, entidade-produto), evento 378 (verbete_entregue, contrato-produto), evento 378 (verbete_entregue, campo_ausente), evento 382 (resposta), evento 387 (verbete_citado, campo_ausente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, campo_ausente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 377 a 398 da trilha; hash dos eventos deste caso: `3ddb2db7ccfd3960`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
