<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-6`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/lex-6@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `recurso_inexistente` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,58)

**IMPACTO (declarado):** `A área do cliente não lista nenhuma reserva devido à resposta 404, indicando que o pedido não foi encontrado.`

Justificativa (gerada por molde): O agente respondeu recurso_inexistente porque os verbetes corpo_nao_e_json, recurso_inexistente, valor_fora_do_dominio estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,25. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,58); trate como hipótese e confira o caso antes de agir.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 1 recusada(s) (palavra_chave_invalida) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 1 edição(ões) para o caso lex-6. A proposta 1 (retificacao em [corpo_nao_e_json]) foi recusada por a validação da Fase 3 com o código palavra_chave_invalida: item de lista inválido: 'unexpected token <'.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | retificacao | `corpo_nao_e_json` | recusada: `palavra_chave_invalida` | nenhum | recusada: `palavra_chave_invalida` |  |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
<!DOCTYPE html><html><head><title>404 Not Found</title></head></html>

SINTOMA OBSERVADO: A area do cliente nao lista nenhuma reserva e o console acusa erro de parsing.
```

## 3. Contraste com a segunda causa

recurso_inexistente e não corpo_nao_e_json: a escolha tem probabilidade 0,58 contra 0,25; verbete(s) na evidência: corpo_nao_e_json, recurso_inexistente, valor_fora_do_dominio

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| recurso_inexistente | 0,58 | sim |
| corpo_nao_e_json | 0,25 |  |
| corpo_vazio | 0,25 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[recurso_inexistente]`; verbetes citados: `recurso_inexistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `recurso_inexistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `recurso_inexistente` | confere | contexto: `corpo_nao_e_json`, `recurso_inexistente`, `valor_fora_do_dominio` |
| Algum verbete do contexto trata da causa respondida | `recurso_inexistente` | confere | verbetes: `recurso_inexistente` |
| fonte_formato_valido | `[recurso_inexistente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["recurso_inexistente"]} |
| fonte_contem_termo_da_causa | `recurso_inexistente` | confere | {"termo": "recurso_inexistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 556 | 1 | entrada | programa | ao_vivo | 2026-11-03T22:02:45 | caso lex-6 |
| 557 | 2 | candidatos | programa | ao_vivo | 2026-11-03T22:02:45 | 3 de 40 verbetes entregues |
| 559 | 3 | prompt | programa | ao_vivo | 2026-11-03T22:02:45 | {"chars": 3649, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "83dde638a3bf", "sha": "83dde638a3bf2604"} |
| 561 | 4 | inferencia | programa | ao_vivo | 2026-11-03T22:02:45 | diagnostico: 70,8 s |
| 562 | 5 | declaracao | modelo | ao_vivo | 2026-11-03T22:02:45 | causa_raiz: `recurso_inexistente` |
| 563 | 6 | declaracao | modelo | ao_vivo | 2026-11-03T22:02:45 | campo: `nenhum` |
| 564 | 7 | declaracao | modelo | ao_vivo | 2026-11-03T22:02:45 | impacto: `A área do cliente não lista nenhuma reserva devido à resposta 404, indicando que o pedido não foi encontrado.` |
| 565 | 8 | declaracao | modelo | ao_vivo | 2026-11-03T22:02:45 | fonte: `[recurso_inexistente]` |
| 566 | 9 | declaracao | modelo | ao_vivo | 2026-11-03T22:02:45 | fonte_citada: `recurso_inexistente` |
| 567 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T22:02:45 | quatro_linhas_presentes: confere |
| 568 | 11 | verificacao | verificacao | ao_vivo | 2026-11-03T22:02:45 | rotulo_no_conjunto: confere |
| 569 | 12 | verificacao | verificacao | ao_vivo | 2026-11-03T22:02:45 | fonte_existe_na_biblioteca: confere |
| 570 | 13 | verificacao | verificacao | ao_vivo | 2026-11-03T22:02:45 | fonte_estava_no_contexto: confere |
| 571 | 14 | verificacao | verificacao | ao_vivo | 2026-11-03T22:02:45 | campo_existe_no_caso: nao_se_aplica |
| 572 | 15 | verificacao | verificacao | ao_vivo | 2026-11-03T22:02:45 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 573 | 16 | verificacao | verificacao | ao_vivo | 2026-11-03T22:02:45 | notas_nos_verbetes_citados: informativo |
| 574 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T22:02:45 | impacto: nao_verificavel |
| 575 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T22:02:45 | fonte_formato_valido: confere |
| 576 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T22:02:45 | fonte_contem_termo_da_causa: confere |
| 577 | 20 | decisao | programa | ao_vivo | 2026-11-03T22:02:45 | diagnostico: escolha recurso_inexistente; divergência não |
| 580 | 21 | inferencia | programa | ao_vivo | 2026-11-03T22:04:00 | proposta: 133,1 s |
| 582 | 22 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:04:00 | proposta 1: retificacao em [corpo_nao_e_json]: recusada: palavra_chave_invalida |
| 583 | 23 | decisao | programa | ao_vivo | 2026-11-03T22:04:00 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 577, `diagnostico`: escolha `recurso_inexistente`; resultado rotulo_emitido; evidência: evento 557 (verbete_entregue, corpo_nao_e_json), evento 557 (verbete_entregue, recurso_inexistente), evento 557 (verbete_entregue, valor_fora_do_dominio), evento 561 (resposta), evento 566 (verbete_citado, recurso_inexistente); divergência: não; falha: nenhuma; prov.used: corpo_nao_e_json, recurso_inexistente, valor_fora_do_dominio (gen_ai: chat)
- evento 583, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 561 (resposta), evento 580 (resposta), evento 582 (verbete_entregue, corpo_nao_e_json); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: corpo_nao_e_json, recurso_inexistente, valor_fora_do_dominio

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 556 a 583 da trilha; hash dos eventos deste caso: `caa08cbe1abf72da`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
