<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-18`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/sin-18@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `estrutura_aninhada_divergente` · **CAMPO:** `status` · selo de probabilidade: **baixo** (p = 0,71)

**IMPACTO (declarado):** `O usuário vê uma descrição detalhada do status em vez do valor simplificado 'Em Análise' ou 'Cancelado'.`

Justificativa (gerada por molde): O agente respondeu estrutura_aninhada_divergente no campo status porque os verbetes contrato-pedido, pedido-reserva, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,17 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,71); trate como hipótese e confira o campo status antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": {"codigo": "EA", "descricao": "Em Analise"}, "nome": "Cliente Teste", "cpf": "11122233344"}]

SINTOMA OBSERVADO: O campo status de cada reserva chega como objeto ({'codigo': ..., 'descricao': ...}) em vez do texto simples que o contrato descreve; comparar direto com 'Em Analise'/'Cancelado' nunca bate.
```

## 3. Contraste com a segunda causa

estrutura_aninhada_divergente e não tipo_divergente: a escolha tem probabilidade 0,71 contra 0,17; verbete(s) na evidência: contrato-pedido, pedido-reserva, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| estrutura_aninhada_divergente | 0,71 | sim |
| tipo_divergente | 0,17 |  |
| campo_ausente | 0,11 |  |
| campo_renomeado | 0,11 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[pedido-reserva]`; verbetes citados: `pedido-reserva`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `pedido-reserva` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `pedido-reserva` | confere | contexto: `contrato-pedido`, `pedido-reserva`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `estrutura_aninhada_divergente` | confere | verbetes: `estrutura_aninhada_divergente` |
| fonte_formato_valido | `[pedido-reserva]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["pedido-reserva"]} |
| fonte_contem_termo_da_causa | `pedido-reserva` | **não confere** | {"termo": "estrutura_aninhada_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `status` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2181 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:47:32 | caso sin-18 |
| 2182 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:47:32 | 3 de 46 verbetes entregues |
| 2184 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:47:32 | {"chars": 3762, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "69a7916b492d", "sha": "69a7916b492df820"} |
| 2186 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:47:32 | diagnostico: 55,9 s |
| 2187 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:47:32 | causa_raiz: `estrutura_aninhada_divergente` |
| 2188 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:47:32 | campo: `status` |
| 2189 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:47:32 | impacto: `O usuário vê uma descrição detalhada do status em vez do valor simplificado 'Em Análise' ou 'Cancelado'.` |
| 2190 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:47:32 | fonte: `[pedido-reserva]` |
| 2191 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:47:32 | fonte_citada: `pedido-reserva` |
| 2192 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T00:47:32 | quatro_linhas_presentes: confere |
| 2193 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:47:32 | rotulo_no_conjunto: confere |
| 2194 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:47:32 | fonte_existe_na_biblioteca: confere |
| 2195 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:47:32 | fonte_estava_no_contexto: confere |
| 2196 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:47:32 | campo_existe_no_caso: confere |
| 2197 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:47:32 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2198 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:47:32 | notas_nos_verbetes_citados: informativo |
| 2199 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:47:32 | impacto: nao_verificavel |
| 2200 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:47:32 | fonte_formato_valido: confere |
| 2201 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:47:32 | fonte_contem_termo_da_causa: nao_confere |
| 2202 | 20 | decisao | programa | ao_vivo | 2026-11-04T00:47:32 | diagnostico: escolha estrutura_aninhada_divergente; divergência não |

</details>

Nós de decisão:

- evento 2202, `diagnostico`: escolha `estrutura_aninhada_divergente`; resultado rotulo_emitido; evidência: evento 2182 (verbete_entregue, contrato-pedido), evento 2182 (verbete_entregue, pedido-reserva), evento 2182 (verbete_entregue, estrutura_aninhada_divergente), evento 2186 (resposta), evento 2191 (verbete_citado, pedido-reserva); divergência: não; falha: nenhuma; prov.used: contrato-pedido, pedido-reserva, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2181 a 2202 da trilha; hash dos eventos deste caso: `d177847aa0e7faae`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
