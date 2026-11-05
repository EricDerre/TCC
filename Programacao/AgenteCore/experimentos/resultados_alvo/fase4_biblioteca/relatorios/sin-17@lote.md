<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-17`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/sin-17@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_renomeado` · **CAMPO:** `documento` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê um campo extra "documento" no lugar do esperado "cpf", causando confusão na interpretação dos dados.`

Justificativa (gerada por molde): O agente respondeu campo_renomeado no campo documento porque os verbetes contrato-pedido, chave_de_juncao_errada, campo_renomeado estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": "Cliente Teste", "documento": "11122233344"}]

SINTOMA OBSERVADO: A resposta de GET /api/pedidos traz o campo documento no lugar de cpf; quem le o contrato antigo (CONTRATO_PEDIDO) nao encontra a chave cpf em lugar nenhum do item.
```

## 3. Contraste com a segunda causa

campo_renomeado e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-pedido, chave_de_juncao_errada, campo_renomeado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_renomeado | 1,00 | sim |
| campo_ausente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_renomeado]`; verbetes citados: `campo_renomeado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | confere | contexto: `contrato-pedido`, `chave_de_juncao_errada`, `campo_renomeado` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `campo_renomeado` |
| fonte_formato_valido | `[campo_renomeado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["campo_renomeado"]} |
| fonte_contem_termo_da_causa | `campo_renomeado` | confere | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `documento` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2158 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:46:08 | caso sin-17 |
| 2159 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:46:08 | 3 de 46 verbetes entregues |
| 2161 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:46:08 | {"chars": 4234, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "ee961cba93e8", "sha": "ee961cba93e87d53"} |
| 2163 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:46:08 | diagnostico: 79,3 s |
| 2164 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:46:08 | causa_raiz: `campo_renomeado` |
| 2165 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:46:08 | campo: `documento` |
| 2166 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:46:08 | impacto: `O usuário vê um campo extra "documento" no lugar do esperado "cpf", causando confusão na interpretação dos dados.` |
| 2167 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:46:08 | fonte: `[campo_renomeado]` |
| 2168 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:46:08 | fonte_citada: `campo_renomeado` |
| 2169 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T00:46:08 | quatro_linhas_presentes: confere |
| 2170 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:46:08 | rotulo_no_conjunto: confere |
| 2171 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:46:08 | fonte_existe_na_biblioteca: confere |
| 2172 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:46:08 | fonte_estava_no_contexto: confere |
| 2173 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:46:08 | campo_existe_no_caso: confere |
| 2174 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:46:08 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2175 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:46:08 | notas_nos_verbetes_citados: informativo |
| 2176 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:46:08 | impacto: nao_verificavel |
| 2177 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:46:08 | fonte_formato_valido: confere |
| 2178 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:46:08 | fonte_contem_termo_da_causa: confere |
| 2179 | 20 | decisao | programa | ao_vivo | 2026-11-04T00:46:08 | diagnostico: escolha campo_renomeado; divergência não |

</details>

Nós de decisão:

- evento 2179, `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido; evidência: evento 2159 (verbete_entregue, contrato-pedido), evento 2159 (verbete_entregue, chave_de_juncao_errada), evento 2159 (verbete_entregue, campo_renomeado), evento 2163 (resposta), evento 2168 (verbete_citado, campo_renomeado); divergência: não; falha: nenhuma; prov.used: contrato-pedido, chave_de_juncao_errada, campo_renomeado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2158 a 2179 da trilha; hash dos eventos deste caso: `113e84903db5edbb`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
