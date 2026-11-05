<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-19`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/run-19@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tempo_de_resposta_excedido` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário espera por cerca de 8 segundos para que o modal de detalhes abra, o que causa uma experiência ruim e aumenta a percepção de lentidão do sistema.`

Justificativa (gerada por molde): O agente respondeu tempo_de_resposta_excedido porque os verbetes tempo_de_resposta_excedido, pagina-produtos-api, registro_duplicado estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/1 (clique em 'Saiba Mais...')

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
(recebido apos 7,8 s)

SINTOMA OBSERVADO: O modal de detalhes demora quase 8 segundos pra abrir depois do clique; o mesmo clique respondia em menos de 200ms antes.

OBSERVAÇÃO ADICIONAL: fetch() nao tem timeout configurado em produtos_api.php; o modal so abre quando a Promise resolve, por mais que demore.
```

## 3. Contraste com a segunda causa

tempo_de_resposta_excedido e não tipo_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: tempo_de_resposta_excedido, pagina-produtos-api, registro_duplicado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tempo_de_resposta_excedido | 1,00 | sim |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tempo_de_resposta_excedido]`; verbetes citados: `tempo_de_resposta_excedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tempo_de_resposta_excedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tempo_de_resposta_excedido` | confere | contexto: `tempo_de_resposta_excedido`, `pagina-produtos-api`, `registro_duplicado` |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | confere | verbetes: `tempo_de_resposta_excedido` |
| fonte_formato_valido | `[tempo_de_resposta_excedido]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["tempo_de_resposta_excedido"]} |
| fonte_contem_termo_da_causa | `tempo_de_resposta_excedido` | confere | {"termo": "tempo_de_resposta_excedido"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2646 | 1 | entrada | programa | ao_vivo | 2026-11-04T01:08:10 | caso run-19 |
| 2647 | 2 | candidatos | programa | ao_vivo | 2026-11-04T01:08:10 | 3 de 46 verbetes entregues |
| 2649 | 3 | prompt | programa | ao_vivo | 2026-11-04T01:08:10 | {"chars": 3233, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "42e866b1d8b8", "sha": "42e866b1d8b8e105"} |
| 2651 | 4 | inferencia | programa | ao_vivo | 2026-11-04T01:08:10 | diagnostico: 66,9 s |
| 2652 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T01:08:10 | causa_raiz: `tempo_de_resposta_excedido` |
| 2653 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T01:08:10 | campo: `nenhum` |
| 2654 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T01:08:10 | impacto: `O usuário espera por cerca de 8 segundos para que o modal de detalhes abra, o que causa uma experiência ruim e aumenta a percepção de lentidão do sistema.` |
| 2655 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T01:08:10 | fonte: `[tempo_de_resposta_excedido]` |
| 2656 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T01:08:10 | fonte_citada: `tempo_de_resposta_excedido` |
| 2657 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T01:08:10 | quatro_linhas_presentes: confere |
| 2658 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T01:08:10 | rotulo_no_conjunto: confere |
| 2659 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T01:08:10 | fonte_existe_na_biblioteca: confere |
| 2660 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T01:08:10 | fonte_estava_no_contexto: confere |
| 2661 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T01:08:10 | campo_existe_no_caso: nao_se_aplica |
| 2662 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T01:08:10 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2663 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T01:08:10 | notas_nos_verbetes_citados: informativo |
| 2664 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T01:08:10 | impacto: nao_verificavel |
| 2665 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T01:08:10 | fonte_formato_valido: confere |
| 2666 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T01:08:10 | fonte_contem_termo_da_causa: confere |
| 2667 | 20 | decisao | programa | ao_vivo | 2026-11-04T01:08:10 | diagnostico: escolha tempo_de_resposta_excedido; divergência não |

</details>

Nós de decisão:

- evento 2667, `diagnostico`: escolha `tempo_de_resposta_excedido`; resultado rotulo_emitido; evidência: evento 2647 (verbete_entregue, tempo_de_resposta_excedido), evento 2647 (verbete_entregue, pagina-produtos-api), evento 2647 (verbete_entregue, registro_duplicado), evento 2651 (resposta), evento 2656 (verbete_citado, tempo_de_resposta_excedido); divergência: não; falha: nenhuma; prov.used: tempo_de_resposta_excedido, pagina-produtos-api, registro_duplicado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2646 a 2667 da trilha; hash dos eventos deste caso: `812fd15af74593e9`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
