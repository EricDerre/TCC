<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-2`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/run-2@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tempo_de_resposta_excedido` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `A página fica carregando e depois exibe erro de rede, pois a requisição demorou mais do que o esperado e foi encerrada pelo cliente.`

Justificativa (gerada por molde): O agente respondeu tempo_de_resposta_excedido porque os verbetes tempo_de_resposta_excedido, limite_de_requisicoes, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, limite_de_requisicoes, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
(sem resposta apos 30s; conexao encerrada pelo cliente)

SINTOMA OBSERVADO: A pagina fica carregando e depois exibe erro de rede.
```

## 3. Contraste com a segunda causa

tempo_de_resposta_excedido e não limite_de_requisicoes: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: tempo_de_resposta_excedido, limite_de_requisicoes, estado_da_tela_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tempo_de_resposta_excedido | 1,00 | sim |
| limite_de_requisicoes | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tempo_de_resposta_excedido]`; verbetes citados: `tempo_de_resposta_excedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tempo_de_resposta_excedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tempo_de_resposta_excedido` | confere | contexto: `tempo_de_resposta_excedido`, `limite_de_requisicoes`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | confere | verbetes: `tempo_de_resposta_excedido`, `limite_de_requisicoes` |
| fonte_formato_valido | `[tempo_de_resposta_excedido]` | confere | {"ids": ["tempo_de_resposta_excedido"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tempo_de_resposta_excedido` | confere | {"termo": "tempo_de_resposta_excedido"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids run-2 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 532 | 1 | entrada | programa | ao_vivo | 2026-11-05T18:59:53 | caso run-2 |
| 533 | 2 | candidatos | programa | ao_vivo | 2026-11-05T18:59:53 | 3 de 39 verbetes entregues |
| 535 | 3 | prompt | programa | ao_vivo | 2026-11-05T18:59:53 | {"etapa": "diagnostico", "sha": "2c4d4396829210af", "prompt_sha256": "2c4d43968292", "chars": 3445, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 537 | 4 | inferencia | programa | ao_vivo | 2026-11-05T18:59:53 | diagnostico: 71,6 s |
| 538 | 5 | declaracao | modelo | ao_vivo | 2026-11-05T18:59:53 | causa_raiz: `tempo_de_resposta_excedido` |
| 539 | 6 | declaracao | modelo | ao_vivo | 2026-11-05T18:59:53 | campo: `nenhum` |
| 540 | 7 | declaracao | modelo | ao_vivo | 2026-11-05T18:59:53 | impacto: `A página fica carregando e depois exibe erro de rede, pois a requisição demorou mais do que o esperado e foi encerrada pelo cliente.` |
| 541 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T18:59:53 | fonte: `[tempo_de_resposta_excedido]` |
| 542 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T18:59:53 | fonte_citada: `tempo_de_resposta_excedido` |
| 543 | 10 | verificacao | verificacao | ao_vivo | 2026-11-05T18:59:53 | quatro_linhas_presentes: confere |
| 544 | 11 | verificacao | verificacao | ao_vivo | 2026-11-05T18:59:53 | rotulo_no_conjunto: confere |
| 545 | 12 | verificacao | verificacao | ao_vivo | 2026-11-05T18:59:53 | fonte_existe_na_biblioteca: confere |
| 546 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T18:59:53 | fonte_estava_no_contexto: confere |
| 547 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T18:59:53 | campo_existe_no_caso: nao_se_aplica |
| 548 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T18:59:53 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 549 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T18:59:53 | notas_nos_verbetes_citados: informativo |
| 550 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T18:59:53 | impacto: nao_verificavel |
| 551 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T18:59:53 | fonte_formato_valido: confere |
| 552 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T18:59:53 | fonte_contem_termo_da_causa: confere |
| 553 | 20 | decisao | programa | ao_vivo | 2026-11-05T18:59:53 | diagnostico: escolha tempo_de_resposta_excedido; divergência não |

</details>

Nós de decisão:

- evento 553, `diagnostico`: escolha `tempo_de_resposta_excedido`; resultado rotulo_emitido; evidência: evento 533 (verbete_entregue, tempo_de_resposta_excedido), evento 533 (verbete_entregue, limite_de_requisicoes), evento 533 (verbete_entregue, estado_da_tela_divergente), evento 537 (resposta), evento 542 (verbete_citado, tempo_de_resposta_excedido); divergência: não; falha: nenhuma; prov.used: tempo_de_resposta_excedido, limite_de_requisicoes, estado_da_tela_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 532 a 553 da trilha; hash dos eventos deste caso: `7d89d1ca5be04f98`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
