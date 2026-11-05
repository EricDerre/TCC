<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-13`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/lex-13@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `corpo_vazio` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 0,99)

**IMPACTO (declarado):** `A área do cliente mostra a tabela de reservas sem nenhuma linha, sem erro, pois a API retornou um corpo vazio, indicando que não há dados disponíveis para serem exibidos.`

Justificativa (gerada por molde): O agente respondeu corpo_vazio porque os verbetes corpo_vazio, contrato-pedido, pedido-reserva estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,01. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 1 recusada(s) (id_repetido) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 1 edição(ões) para o caso lex-13. A proposta 1 (novo_verbete em [corpo_vazio]) foi recusada por a validação da Fase 3 com o código id_repetido: 'corpo_vazio' já é id de verbete ou nome de causa raiz.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | novo_verbete | `corpo_vazio` | recusada: `id_repetido` | nenhum | recusada: `id_repetido` |  |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
   

SINTOMA OBSERVADO: A area do cliente mostra a tabela de reservas sem nenhuma linha, sem erro.
```

## 3. Contraste com a segunda causa

corpo_vazio e não resposta_truncada: a escolha tem probabilidade 0,99 contra 0,01; verbete(s) na evidência: corpo_vazio, contrato-pedido, pedido-reserva

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| corpo_vazio | 0,99 | sim |
| resposta_truncada | 0,01 |  |
| corpo_nao_e_json | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[corpo_vazio]`; verbetes citados: `corpo_vazio`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `corpo_vazio` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `corpo_vazio` | confere | contexto: `corpo_vazio`, `contrato-pedido`, `pedido-reserva` |
| Algum verbete do contexto trata da causa respondida | `corpo_vazio` | confere | verbetes: `corpo_vazio` |
| fonte_formato_valido | `[corpo_vazio]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["corpo_vazio"]} |
| fonte_contem_termo_da_causa | `corpo_vazio` | confere | {"termo": "corpo_vazio"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1895 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:26:51 | caso lex-13 |
| 1896 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:26:51 | 3 de 40 verbetes entregues |
| 1898 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:26:51 | {"chars": 3204, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "b129fe44add6", "sha": "b129fe44add6ce3c"} |
| 1900 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:26:51 | diagnostico: 66,1 s |
| 1901 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:26:51 | causa_raiz: `corpo_vazio` |
| 1902 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:26:51 | campo: `nenhum` |
| 1903 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:26:51 | impacto: `A área do cliente mostra a tabela de reservas sem nenhuma linha, sem erro, pois a API retornou um corpo vazio, indicando que não há dados disponíveis para serem exibidos.` |
| 1904 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:26:51 | fonte: `[corpo_vazio]` |
| 1905 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:26:51 | fonte_citada: `corpo_vazio` |
| 1906 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T00:26:51 | quatro_linhas_presentes: confere |
| 1907 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:26:51 | rotulo_no_conjunto: confere |
| 1908 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:26:51 | fonte_existe_na_biblioteca: confere |
| 1909 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:26:51 | fonte_estava_no_contexto: confere |
| 1910 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:26:51 | campo_existe_no_caso: nao_se_aplica |
| 1911 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:26:51 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1912 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:26:51 | notas_nos_verbetes_citados: informativo |
| 1913 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:26:51 | impacto: nao_verificavel |
| 1914 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:26:51 | fonte_formato_valido: confere |
| 1915 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:26:51 | fonte_contem_termo_da_causa: confere |
| 1916 | 20 | decisao | programa | ao_vivo | 2026-11-04T00:26:51 | diagnostico: escolha corpo_vazio; divergência não |
| 1919 | 21 | inferencia | programa | ao_vivo | 2026-11-04T00:28:01 | proposta: 117,1 s |
| 1921 | 22 | edicao_biblioteca | programa | ao_vivo | 2026-11-04T00:28:01 | proposta 1: novo_verbete em [corpo_vazio]: recusada: id_repetido |
| 1922 | 23 | decisao | programa | ao_vivo | 2026-11-04T00:28:01 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 1916, `diagnostico`: escolha `corpo_vazio`; resultado rotulo_emitido; evidência: evento 1896 (verbete_entregue, corpo_vazio), evento 1896 (verbete_entregue, contrato-pedido), evento 1896 (verbete_entregue, pedido-reserva), evento 1900 (resposta), evento 1905 (verbete_citado, corpo_vazio); divergência: não; falha: nenhuma; prov.used: corpo_vazio, contrato-pedido, pedido-reserva (gen_ai: chat)
- evento 1922, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 1900 (resposta), evento 1919 (resposta), evento 1921 (verbete_entregue, corpo_vazio); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: contrato-pedido, corpo_vazio, pedido-reserva

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1895 a 1922 da trilha; hash dos eventos deste caso: `9272b8ad156761fe`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
