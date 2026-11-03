<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-11`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/tra-11@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `contagem_inconsistente` · **CAMPO:** `itens` · selo de probabilidade: **medio** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê uma segunda página vazia, enquanto espera por 14 itens.`

Justificativa (gerada por molde): O agente respondeu contagem_inconsistente no campo itens porque os verbetes contagem_inconsistente, estrutura_aninhada_divergente, tempo_de_resposta_excedido estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos?pagina=2

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano | envelope: {total: inteiro, itens: lista}

CORPO DA RESPOSTA:
{"total": 14, "itens": []}

SINTOMA OBSERVADO: A segunda pagina da listagem aparece vazia, mesmo havendo 14 produtos.
```

## 3. Contraste com a segunda causa

contagem_inconsistente e não estrutura_aninhada_divergente: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: contagem_inconsistente, estrutura_aninhada_divergente, tempo_de_resposta_excedido

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| contagem_inconsistente | 0,99 | sim |
| estrutura_aninhada_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contagem_inconsistente]`; verbetes citados: `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `contagem_inconsistente`, `estrutura_aninhada_divergente`, `tempo_de_resposta_excedido` |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | confere | verbetes: `contagem_inconsistente`, `estrutura_aninhada_divergente` |
| fonte_formato_valido | `[contagem_inconsistente]` | confere | {"ids": ["contagem_inconsistente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | confere | {"termo": "contagem_inconsistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `itens` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids tra-11 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1266 | 1 | entrada | programa | ao_vivo | 2026-11-01T11:58:00 | caso tra-11 |
| 1267 | 2 | candidatos | programa | ao_vivo | 2026-11-01T11:58:00 | 3 de 40 verbetes entregues |
| 1269 | 3 | prompt | programa | ao_vivo | 2026-11-01T11:58:00 | {"etapa": "diagnostico", "sha": "d430d355dd85e985", "prompt_sha256": "d430d355dd85", "chars": 3361, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1271 | 4 | inferencia | programa | ao_vivo | 2026-11-01T11:58:00 | diagnostico: 59,5 s |
| 1272 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T11:58:00 | causa_raiz: `contagem_inconsistente` |
| 1273 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T11:58:00 | campo: `itens` |
| 1274 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T11:58:00 | impacto: `O usuário vê uma segunda página vazia, enquanto espera por 14 itens.` |
| 1275 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T11:58:00 | fonte: `[contagem_inconsistente]` |
| 1276 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T11:58:00 | fonte_citada: `contagem_inconsistente` |
| 1277 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T11:58:00 | quatro_linhas_presentes: confere |
| 1278 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T11:58:00 | rotulo_no_conjunto: confere |
| 1279 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T11:58:00 | fonte_existe_na_biblioteca: confere |
| 1280 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T11:58:00 | fonte_estava_no_contexto: confere |
| 1281 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T11:58:00 | campo_existe_no_caso: confere |
| 1282 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T11:58:00 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1283 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T11:58:00 | notas_nos_verbetes_citados: informativo |
| 1284 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T11:58:00 | impacto: nao_verificavel |
| 1285 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T11:58:00 | fonte_formato_valido: confere |
| 1286 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T11:58:00 | fonte_contem_termo_da_causa: confere |
| 1287 | 20 | decisao | programa | ao_vivo | 2026-11-01T11:58:00 | diagnostico: escolha contagem_inconsistente; divergência não |

</details>

Nós de decisão:

- evento 1287, `diagnostico`: escolha `contagem_inconsistente`; resultado rotulo_emitido; evidência: evento 1267 (verbete_entregue, contagem_inconsistente), evento 1267 (verbete_entregue, estrutura_aninhada_divergente), evento 1267 (verbete_entregue, tempo_de_resposta_excedido), evento 1271 (resposta), evento 1276 (verbete_citado, contagem_inconsistente); divergência: não; falha: nenhuma; prov.used: contagem_inconsistente, estrutura_aninhada_divergente, tempo_de_resposta_excedido (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1266 a 1287 da trilha; hash dos eventos deste caso: `916854089a9facee`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
