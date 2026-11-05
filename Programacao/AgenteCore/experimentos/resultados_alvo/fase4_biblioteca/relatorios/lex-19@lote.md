<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-19`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/lex-19@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `erro_interno_do_servidor` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,81)

**IMPACTO (declarado):** `O usuário recebe uma página de erro HTML em vez de uma resposta JSON, indicando que o pedido de cancelamento não foi processado corretamente.`

Justificativa (gerada por molde): O agente respondeu erro_interno_do_servidor porque os verbetes corpo_nao_e_json, erro_interno_do_servidor, fluxo-reserva-e-cancelamento estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,18. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,81); trate como hipótese e confira o caso antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: POST /api/pedidos/7/cancelar

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
<html><head><title>500 Internal Server Error</title></head><body><h1>Internal Server Error</h1></body></html>

SINTOMA OBSERVADO: A resposta de POST /api/pedidos/7/cancelar chega com status 200 e Content-Type application/json, mas o corpo e uma pagina HTML de erro; nao da pra confirmar se a reserva foi cancelada de fato.
```

## 3. Contraste com a segunda causa

erro_interno_do_servidor e não corpo_nao_e_json: a escolha tem probabilidade 0,81 contra 0,18; verbete(s) na evidência: corpo_nao_e_json, erro_interno_do_servidor, fluxo-reserva-e-cancelamento

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| erro_interno_do_servidor | 0,81 | sim |
| corpo_nao_e_json | 0,18 |  |
| corpo_vazio | 0,18 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[erro_interno_do_servidor]`; verbetes citados: `erro_interno_do_servidor`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `erro_interno_do_servidor` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `erro_interno_do_servidor` | confere | contexto: `corpo_nao_e_json`, `erro_interno_do_servidor`, `fluxo-reserva-e-cancelamento` |
| Algum verbete do contexto trata da causa respondida | `erro_interno_do_servidor` | confere | verbetes: `corpo_nao_e_json`, `erro_interno_do_servidor` |
| fonte_formato_valido | `[erro_interno_do_servidor]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["erro_interno_do_servidor"]} |
| fonte_contem_termo_da_causa | `erro_interno_do_servidor` | confere | {"termo": "erro_interno_do_servidor"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2066 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:41:02 | caso lex-19 |
| 2067 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:41:02 | 3 de 46 verbetes entregues |
| 2069 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:41:02 | {"chars": 3897, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "193525b2b591", "sha": "193525b2b591564e"} |
| 2071 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:41:02 | diagnostico: 72,4 s |
| 2072 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:41:02 | causa_raiz: `erro_interno_do_servidor` |
| 2073 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:41:02 | campo: `nenhum` |
| 2074 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:41:02 | impacto: `O usuário recebe uma página de erro HTML em vez de uma resposta JSON, indicando que o pedido de cancelamento não foi processado corretamente.` |
| 2075 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:41:02 | fonte: `[erro_interno_do_servidor]` |
| 2076 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:41:02 | fonte_citada: `erro_interno_do_servidor` |
| 2077 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T00:41:02 | quatro_linhas_presentes: confere |
| 2078 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:41:02 | rotulo_no_conjunto: confere |
| 2079 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:41:02 | fonte_existe_na_biblioteca: confere |
| 2080 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:41:02 | fonte_estava_no_contexto: confere |
| 2081 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:41:02 | campo_existe_no_caso: nao_se_aplica |
| 2082 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:41:02 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2083 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:41:02 | notas_nos_verbetes_citados: informativo |
| 2084 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:41:02 | impacto: nao_verificavel |
| 2085 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:41:02 | fonte_formato_valido: confere |
| 2086 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:41:02 | fonte_contem_termo_da_causa: confere |
| 2087 | 20 | decisao | programa | ao_vivo | 2026-11-04T00:41:02 | diagnostico: escolha erro_interno_do_servidor; divergência não |

</details>

Nós de decisão:

- evento 2087, `diagnostico`: escolha `erro_interno_do_servidor`; resultado rotulo_emitido; evidência: evento 2067 (verbete_entregue, corpo_nao_e_json), evento 2067 (verbete_entregue, erro_interno_do_servidor), evento 2067 (verbete_entregue, fluxo-reserva-e-cancelamento), evento 2071 (resposta), evento 2076 (verbete_citado, erro_interno_do_servidor); divergência: não; falha: nenhuma; prov.used: corpo_nao_e_json, erro_interno_do_servidor, fluxo-reserva-e-cancelamento (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2066 a 2087 da trilha; hash dos eventos deste caso: `3c729aa9fe7e4ac4`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
