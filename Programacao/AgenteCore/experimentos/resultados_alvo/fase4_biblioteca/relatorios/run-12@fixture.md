<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-12`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/run-12@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `erro_interno_do_servidor` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,94)

**IMPACTO (declarado):** `O usuário vê uma mensagem genérica de erro interno, sem detalhes específicos sobre o problema.`

Justificativa (gerada por molde): O agente respondeu erro_interno_do_servidor porque os verbetes erro_interno_do_servidor, estrutura_aninhada_divergente, contagem_inconsistente estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 1 edição(ões) aplicada(s) ([erro_interno_do_servidor]), 0 para revisão humana, 1 recusada(s) (duplicada).

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso run-12. A proposta 1 (nota em [erro_interno_do_servidor]) foi recusada por a validação da Fase 3 com o código duplicada: [erro_interno_do_servidor] já tem uma nota com este texto. A proposta 2 (nota em [erro_interno_do_servidor], peso 1) passou pela validação da Fase 3 e pelos filtros e entrou no lote.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `erro_interno_do_servidor` | recusada: `duplicada` | nenhum | recusada: `duplicada` |  |
| 2 | nota | `erro_interno_do_servidor` | aceita | nenhum | **aplicada** | 1 |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos (1 em cada 3 tentativas)

STATUS HTTP: 500

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"detail": "erro interno"}

SINTOMA OBSERVADO: A listagem falha de forma intermitente, sem padrao de horario.
```

## 3. Contraste com a segunda causa

erro_interno_do_servidor e não corpo_nao_e_json: a escolha tem probabilidade 0,94 contra 0,00; verbete(s) na evidência: erro_interno_do_servidor, estrutura_aninhada_divergente, contagem_inconsistente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| erro_interno_do_servidor | 0,94 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[erro_interno_do_servidor]`; verbetes citados: `erro_interno_do_servidor`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `erro_interno_do_servidor` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `erro_interno_do_servidor` | confere | contexto: `erro_interno_do_servidor`, `estrutura_aninhada_divergente`, `contagem_inconsistente` |
| Algum verbete do contexto trata da causa respondida | `erro_interno_do_servidor` | confere | verbetes: `erro_interno_do_servidor` |
| fonte_formato_valido | `[erro_interno_do_servidor]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["erro_interno_do_servidor"]} |
| fonte_contem_termo_da_causa | `erro_interno_do_servidor` | confere | {"termo": "erro_interno_do_servidor"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1534 | 1 | entrada | programa | ao_vivo | 2026-11-03T23:43:09 | caso run-12 |
| 1535 | 2 | candidatos | programa | ao_vivo | 2026-11-03T23:43:09 | 3 de 40 verbetes entregues |
| 1537 | 3 | prompt | programa | ao_vivo | 2026-11-03T23:43:09 | {"chars": 3602, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "d15a25bc6853", "sha": "d15a25bc6853fd3e"} |
| 1539 | 4 | inferencia | programa | ao_vivo | 2026-11-03T23:43:09 | diagnostico: 67,4 s |
| 1540 | 5 | declaracao | modelo | ao_vivo | 2026-11-03T23:43:09 | causa_raiz: `erro_interno_do_servidor` |
| 1541 | 6 | declaracao | modelo | ao_vivo | 2026-11-03T23:43:09 | campo: `nenhum` |
| 1542 | 7 | declaracao | modelo | ao_vivo | 2026-11-03T23:43:09 | impacto: `O usuário vê uma mensagem genérica de erro interno, sem detalhes específicos sobre o problema.` |
| 1543 | 8 | declaracao | modelo | ao_vivo | 2026-11-03T23:43:09 | fonte: `[erro_interno_do_servidor]` |
| 1544 | 9 | declaracao | modelo | ao_vivo | 2026-11-03T23:43:09 | fonte_citada: `erro_interno_do_servidor` |
| 1545 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T23:43:09 | quatro_linhas_presentes: confere |
| 1546 | 11 | verificacao | verificacao | ao_vivo | 2026-11-03T23:43:09 | rotulo_no_conjunto: confere |
| 1547 | 12 | verificacao | verificacao | ao_vivo | 2026-11-03T23:43:09 | fonte_existe_na_biblioteca: confere |
| 1548 | 13 | verificacao | verificacao | ao_vivo | 2026-11-03T23:43:09 | fonte_estava_no_contexto: confere |
| 1549 | 14 | verificacao | verificacao | ao_vivo | 2026-11-03T23:43:09 | campo_existe_no_caso: nao_se_aplica |
| 1550 | 15 | verificacao | verificacao | ao_vivo | 2026-11-03T23:43:09 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1551 | 16 | verificacao | verificacao | ao_vivo | 2026-11-03T23:43:09 | notas_nos_verbetes_citados: informativo |
| 1552 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T23:43:09 | impacto: nao_verificavel |
| 1553 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T23:43:09 | fonte_formato_valido: confere |
| 1554 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T23:43:09 | fonte_contem_termo_da_causa: confere |
| 1555 | 20 | decisao | programa | ao_vivo | 2026-11-03T23:43:09 | diagnostico: escolha erro_interno_do_servidor; divergência não |
| 1558 | 21 | inferencia | programa | ao_vivo | 2026-11-03T23:44:20 | proposta: 170,1 s |
| 1560 | 22 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T23:44:20 | proposta 1: nota em [erro_interno_do_servidor]: recusada: duplicada |
| 1562 | 23 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T23:44:20 | proposta 2: nota em [erro_interno_do_servidor]: aplicada |
| 1563 | 24 | decisao | programa | ao_vivo | 2026-11-03T23:44:20 | edicao_biblioteca: escolha proposta_2; divergência sim |

</details>

Nós de decisão:

- evento 1555, `diagnostico`: escolha `erro_interno_do_servidor`; resultado rotulo_emitido; evidência: evento 1535 (verbete_entregue, erro_interno_do_servidor), evento 1535 (verbete_entregue, estrutura_aninhada_divergente), evento 1535 (verbete_entregue, contagem_inconsistente), evento 1539 (resposta), evento 1544 (verbete_citado, erro_interno_do_servidor); divergência: não; falha: nenhuma; prov.used: erro_interno_do_servidor, estrutura_aninhada_divergente, contagem_inconsistente (gen_ai: chat)
- evento 1563, `edicao_biblioteca`: escolha `proposta_2`; resultado lote; evidência: evento 1539 (resposta), evento 1558 (resposta), evento 1560 (verbete_entregue, erro_interno_do_servidor), evento 1562 (verbete_entregue, erro_interno_do_servidor); divergência: sim; falha: nenhuma; prov.used: contagem_inconsistente, erro_interno_do_servidor, estrutura_aninhada_divergente

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1534 a 1563 da trilha; hash dos eventos deste caso: `fec4368583c003b4`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
