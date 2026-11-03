<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-16`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/sin-16@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `destaque` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O campo destaque obrigatório não é exibido, causando inconsistência na interface.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo destaque porque os verbetes entidade-produto, contrato-produto, campo_ausente estavam entre os entregues ao modelo. A segunda causa, campo_renomeado, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/1 (modo field_missing, campo destaque)

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg"}

SINTOMA OBSERVADO: A resposta de GET /api/produtos/1 deixa de trazer o campo destaque; o modal 'Saiba Mais...' (que so le nome e resumo) continua abrindo normal, mas o campo e obrigatorio no contrato (ProdutoOut.destaque: bool, sem valor default).
```

## 3. Contraste com a segunda causa

campo_ausente e não campo_renomeado: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, campo_ausente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 1,00 | sim |
| campo_renomeado | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| tipo_divergente | 0,00 |  |
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

Confira o campo `destaque` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids sin-16 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1510 | 1 | entrada | programa | ao_vivo | 2026-11-01T12:08:15 | caso sin-16 |
| 1511 | 2 | candidatos | programa | ao_vivo | 2026-11-01T12:08:15 | 3 de 40 verbetes entregues |
| 1513 | 3 | prompt | programa | ao_vivo | 2026-11-01T12:08:15 | {"etapa": "diagnostico", "sha": "fdcccc84311ce56b", "prompt_sha256": "fdcccc84311c", "chars": 3595, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1515 | 4 | inferencia | programa | ao_vivo | 2026-11-01T12:08:15 | diagnostico: 47,0 s |
| 1516 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T12:08:15 | causa_raiz: `campo_ausente` |
| 1517 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T12:08:15 | campo: `destaque` |
| 1518 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T12:08:15 | impacto: `O campo destaque obrigatório não é exibido, causando inconsistência na interface.` |
| 1519 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T12:08:15 | fonte: `[campo_ausente]` |
| 1520 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T12:08:15 | fonte_citada: `campo_ausente` |
| 1521 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T12:08:15 | quatro_linhas_presentes: confere |
| 1522 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T12:08:15 | rotulo_no_conjunto: confere |
| 1523 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T12:08:15 | fonte_existe_na_biblioteca: confere |
| 1524 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T12:08:15 | fonte_estava_no_contexto: confere |
| 1525 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T12:08:15 | campo_existe_no_caso: confere |
| 1526 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T12:08:15 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1527 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T12:08:15 | notas_nos_verbetes_citados: informativo |
| 1528 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T12:08:15 | impacto: nao_verificavel |
| 1529 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T12:08:15 | fonte_formato_valido: confere |
| 1530 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T12:08:15 | fonte_contem_termo_da_causa: confere |
| 1531 | 20 | decisao | programa | ao_vivo | 2026-11-01T12:08:15 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 1531, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 1511 (verbete_entregue, entidade-produto), evento 1511 (verbete_entregue, contrato-produto), evento 1511 (verbete_entregue, campo_ausente), evento 1515 (resposta), evento 1520 (verbete_citado, campo_ausente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, campo_ausente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1510 a 1531 da trilha; hash dos eventos deste caso: `1257003606bd308b`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
