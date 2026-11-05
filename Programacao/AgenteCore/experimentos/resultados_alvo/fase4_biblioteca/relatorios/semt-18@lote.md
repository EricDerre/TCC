<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-18`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/semt-18@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `destaque` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê 'destaque: True' em maiúsculas, diferente do esperado 'Sim' ou 'Nao'.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo destaque porque os verbetes tipo_divergente, entidade-produto, contrato-produto estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos (modo type_drift, campo destaque)

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": "True"}]

SINTOMA OBSERVADO: O rotulo do card mostra 'destaque: True' (em ingles, T maiusculo) no lugar de 'Sim' ou 'Nao'.

OBSERVAÇÃO ADICIONAL: O modo type_drift converte o valor com str() do Python, que gera 'True'/'False' com maiuscula — diferente de 'true'/'false' do JSON e de 'Sim'/'Nao' do dominio do produto.
```

## 3. Contraste com a segunda causa

tipo_divergente e não valor_fora_do_dominio: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: tipo_divergente, entidade-produto, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 1,00 | sim |
| valor_fora_do_dominio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tipo_divergente]`; verbetes citados: `tipo_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `tipo_divergente`, `entidade-produto`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `tipo_divergente`, `entidade-produto`, `contrato-produto` |
| fonte_formato_valido | `[tipo_divergente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["tipo_divergente"]} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `destaque` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2323 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:54:09 | caso semt-18 |
| 2324 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:54:09 | 3 de 46 verbetes entregues |
| 2326 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:54:09 | {"chars": 4405, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "b8d46c26acce", "sha": "b8d46c26acceb8ff"} |
| 2328 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:54:09 | diagnostico: 82,2 s |
| 2329 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:54:09 | causa_raiz: `tipo_divergente` |
| 2330 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:54:09 | campo: `destaque` |
| 2331 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:54:09 | impacto: `O usuário vê 'destaque: True' em maiúsculas, diferente do esperado 'Sim' ou 'Nao'.` |
| 2332 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:54:09 | fonte: `[tipo_divergente]` |
| 2333 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:54:09 | fonte_citada: `tipo_divergente` |
| 2334 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T00:54:09 | quatro_linhas_presentes: confere |
| 2335 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:54:09 | rotulo_no_conjunto: confere |
| 2336 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:54:09 | fonte_existe_na_biblioteca: confere |
| 2337 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:54:09 | fonte_estava_no_contexto: confere |
| 2338 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:54:09 | campo_existe_no_caso: confere |
| 2339 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:54:09 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2340 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:54:09 | notas_nos_verbetes_citados: informativo |
| 2341 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:54:09 | impacto: nao_verificavel |
| 2342 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:54:09 | fonte_formato_valido: confere |
| 2343 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:54:09 | fonte_contem_termo_da_causa: confere |
| 2344 | 20 | decisao | programa | ao_vivo | 2026-11-04T00:54:09 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 2344, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 2324 (verbete_entregue, tipo_divergente), evento 2324 (verbete_entregue, entidade-produto), evento 2324 (verbete_entregue, contrato-produto), evento 2328 (resposta), evento 2333 (verbete_citado, tipo_divergente); divergência: não; falha: nenhuma; prov.used: tipo_divergente, entidade-produto, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2323 a 2344 da trilha; hash dos eventos deste caso: `8e7971c9a09b5e93`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
