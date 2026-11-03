<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-1`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/run-1@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `erro_interno_do_servidor` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,98)

**IMPACTO (declarado):** `A aba de produtos via API exibe a mensagem "Erro ao carregar produtos da CobaiaAPI: erro interno (fault injection)".`

Justificativa (gerada por molde): O agente respondeu erro_interno_do_servidor porque os verbetes erro_interno_do_servidor, mensagens-de-erro-do-codigo, pagina-produtos-api estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 500

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"detail": "erro interno (fault injection)"}

SINTOMA OBSERVADO: A aba de produtos via API mostra a mensagem de erro ao carregar.
```

## 3. Contraste com a segunda causa

erro_interno_do_servidor e não corpo_nao_e_json: a escolha tem probabilidade 0,98 contra 0,00; verbete(s) na evidência: erro_interno_do_servidor, mensagens-de-erro-do-codigo, pagina-produtos-api

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| erro_interno_do_servidor | 0,98 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| tipo_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[erro_interno_do_servidor]`; verbetes citados: `erro_interno_do_servidor`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `erro_interno_do_servidor` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `erro_interno_do_servidor` | confere | contexto: `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo`, `pagina-produtos-api` |
| Algum verbete do contexto trata da causa respondida | `erro_interno_do_servidor` | confere | verbetes: `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo` |
| fonte_formato_valido | `[erro_interno_do_servidor]` | confere | {"ids": ["erro_interno_do_servidor"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `erro_interno_do_servidor` | confere | {"termo": "erro_interno_do_servidor"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids run-1 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 489 | 1 | entrada | programa | ao_vivo | 2026-11-01T14:27:05 | caso run-1 |
| 490 | 2 | candidatos | programa | ao_vivo | 2026-11-01T14:27:05 | 3 de 40 verbetes entregues |
| 492 | 3 | prompt | programa | ao_vivo | 2026-11-01T14:27:05 | {"etapa": "diagnostico", "sha": "6427b8a01c726fa1", "prompt_sha256": "6427b8a01c72", "chars": 3350, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 494 | 4 | inferencia | programa | ao_vivo | 2026-11-01T14:27:05 | diagnostico: 62,9 s |
| 495 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T14:27:05 | causa_raiz: `erro_interno_do_servidor` |
| 496 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T14:27:05 | campo: `nenhum` |
| 497 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T14:27:05 | impacto: `A aba de produtos via API exibe a mensagem "Erro ao carregar produtos da CobaiaAPI: erro interno (fault injection)".` |
| 498 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T14:27:05 | fonte: `[erro_interno_do_servidor]` |
| 499 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T14:27:05 | fonte_citada: `erro_interno_do_servidor` |
| 500 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T14:27:05 | quatro_linhas_presentes: confere |
| 501 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T14:27:05 | rotulo_no_conjunto: confere |
| 502 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T14:27:05 | fonte_existe_na_biblioteca: confere |
| 503 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T14:27:05 | fonte_estava_no_contexto: confere |
| 504 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T14:27:05 | campo_existe_no_caso: nao_se_aplica |
| 505 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T14:27:05 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 506 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T14:27:05 | notas_nos_verbetes_citados: informativo |
| 507 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T14:27:05 | impacto: nao_verificavel |
| 508 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T14:27:05 | fonte_formato_valido: confere |
| 509 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T14:27:05 | fonte_contem_termo_da_causa: confere |
| 510 | 20 | decisao | programa | ao_vivo | 2026-11-01T14:27:05 | diagnostico: escolha erro_interno_do_servidor; divergência não |

</details>

Nós de decisão:

- evento 510, `diagnostico`: escolha `erro_interno_do_servidor`; resultado rotulo_emitido; evidência: evento 490 (verbete_entregue, erro_interno_do_servidor), evento 490 (verbete_entregue, mensagens-de-erro-do-codigo), evento 490 (verbete_entregue, pagina-produtos-api), evento 494 (resposta), evento 499 (verbete_citado, erro_interno_do_servidor); divergência: não; falha: nenhuma; prov.used: erro_interno_do_servidor, mensagens-de-erro-do-codigo, pagina-produtos-api (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 489 a 510 da trilha; hash dos eventos deste caso: `50b783997a4b3019`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
