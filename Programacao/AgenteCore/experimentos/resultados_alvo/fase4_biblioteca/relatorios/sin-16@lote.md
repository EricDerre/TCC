<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-16`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/sin-16@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `destaque` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O campo destaque é obrigatório no contrato, mas não está presente na resposta, causando um erro na interface que exige este campo.`

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
| chave_de_juncao_errada | 0,00 |  |
| tipo_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente]`; verbetes citados: `campo_ausente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `contrato-produto`, `campo_ausente` |
| fonte_formato_valido | `[campo_ausente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["campo_ausente"]} |
| fonte_contem_termo_da_causa | `campo_ausente` | confere | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `destaque` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2135 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:44:54 | caso sin-16 |
| 2136 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:44:54 | 3 de 46 verbetes entregues |
| 2138 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:44:54 | {"chars": 3595, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "fdcccc84311c", "sha": "fdcccc84311ce56b"} |
| 2140 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:44:54 | diagnostico: 69,9 s |
| 2141 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:44:54 | causa_raiz: `campo_ausente` |
| 2142 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:44:54 | campo: `destaque` |
| 2143 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:44:54 | impacto: `O campo destaque é obrigatório no contrato, mas não está presente na resposta, causando um erro na interface que exige este campo.` |
| 2144 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:44:54 | fonte: `[campo_ausente]` |
| 2145 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:44:54 | fonte_citada: `campo_ausente` |
| 2146 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T00:44:54 | quatro_linhas_presentes: confere |
| 2147 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:44:54 | rotulo_no_conjunto: confere |
| 2148 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:44:54 | fonte_existe_na_biblioteca: confere |
| 2149 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:44:54 | fonte_estava_no_contexto: confere |
| 2150 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:44:54 | campo_existe_no_caso: confere |
| 2151 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:44:54 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2152 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:44:54 | notas_nos_verbetes_citados: informativo |
| 2153 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:44:54 | impacto: nao_verificavel |
| 2154 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:44:54 | fonte_formato_valido: confere |
| 2155 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:44:54 | fonte_contem_termo_da_causa: confere |
| 2156 | 20 | decisao | programa | ao_vivo | 2026-11-04T00:44:54 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 2156, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 2136 (verbete_entregue, entidade-produto), evento 2136 (verbete_entregue, contrato-produto), evento 2136 (verbete_entregue, campo_ausente), evento 2140 (resposta), evento 2145 (verbete_citado, campo_ausente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, campo_ausente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2135 a 2156 da trilha; hash dos eventos deste caso: `ca40744def6e66b5`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
