<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-14`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/lex-14@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `resposta_truncada` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `A listagem de pedidos não é renderizada corretamente, causando um erro de sintaxe no console.`

Justificativa (gerada por molde): O agente respondeu resposta_truncada porque os verbetes contrato-pedido, resposta_truncada, formato_de_data_divergente estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 2 recusada(s) (duplicada, teto_verbetes_novos) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso lex-14. A proposta 1 (nota em [resposta_truncada]) foi recusada por a validação da Fase 3 com o código duplicada: [resposta_truncada] já tem uma nota com este texto. A proposta 2 (novo_verbete em [resposta_truncada_correta]) foi recusada por a validação da Fase 3 com o código teto_verbetes_novos: 6 verbetes novos nesta época (teto 6).

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `resposta_truncada` | recusada: `duplicada` | nenhum | recusada: `duplicada` |  |
| 2 | novo_verbete | `resposta_truncada_correta` | recusada: `teto_verbetes_novos` | nenhum | recusada: `teto_verbetes_novos` |  |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "sta

SINTOMA OBSERVADO: A listagem de reservas nao renderiza e o console acusa fim inesperado da entrada.
```

## 3. Contraste com a segunda causa

resposta_truncada e não formato_de_data_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-pedido, resposta_truncada, formato_de_data_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| resposta_truncada | 1,00 | sim |
| formato_de_data_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[resposta_truncada] [formato_de_data_divergente]`; verbetes citados: `resposta_truncada`, `formato_de_data_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `resposta_truncada` | confere |  |
| O verbete citado existe na biblioteca | `formato_de_data_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `resposta_truncada` | confere | contexto: `contrato-pedido`, `resposta_truncada`, `formato_de_data_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `formato_de_data_divergente` | confere | contexto: `contrato-pedido`, `resposta_truncada`, `formato_de_data_divergente` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | confere | verbetes: `resposta_truncada` |
| fonte_formato_valido | `[resposta_truncada] [formato_de_data_divergente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["resposta_truncada", "formato_de_data_divergente"]} |
| fonte_contem_termo_da_causa | `resposta_truncada` | confere | {"termo": "resposta_truncada"} |
| fonte_contem_termo_da_causa | `formato_de_data_divergente` | **não confere** | {"termo": "resposta_truncada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>28 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1924 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:30:02 | caso lex-14 |
| 1925 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:30:02 | 3 de 40 verbetes entregues |
| 1927 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:30:02 | {"chars": 3405, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "0d1699183b36", "sha": "0d1699183b36e8dc"} |
| 1929 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:30:02 | diagnostico: 67,5 s |
| 1930 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:30:02 | causa_raiz: `resposta_truncada` |
| 1931 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:30:02 | campo: `nenhum` |
| 1932 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:30:02 | impacto: `A listagem de pedidos não é renderizada corretamente, causando um erro de sintaxe no console.` |
| 1933 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:30:02 | fonte: `[resposta_truncada] [formato_de_data_divergente]` |
| 1934 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:30:02 | fonte_citada: `resposta_truncada` |
| 1935 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T00:30:02 | fonte_citada: `formato_de_data_divergente` |
| 1936 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:30:02 | quatro_linhas_presentes: confere |
| 1937 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:30:02 | rotulo_no_conjunto: confere |
| 1938 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:30:02 | fonte_existe_na_biblioteca: confere |
| 1939 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:30:02 | fonte_existe_na_biblioteca: confere |
| 1940 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:30:02 | fonte_estava_no_contexto: confere |
| 1941 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:30:02 | fonte_estava_no_contexto: confere |
| 1942 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:30:02 | campo_existe_no_caso: nao_se_aplica |
| 1943 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:30:02 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1944 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:30:02 | notas_nos_verbetes_citados: informativo |
| 1945 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T00:30:02 | impacto: nao_verificavel |
| 1946 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T00:30:02 | fonte_formato_valido: confere |
| 1947 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T00:30:02 | fonte_contem_termo_da_causa: confere |
| 1948 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T00:30:02 | fonte_contem_termo_da_causa: nao_confere |
| 1949 | 24 | decisao | programa | ao_vivo | 2026-11-04T00:30:02 | diagnostico: escolha resposta_truncada; divergência não |
| 1952 | 25 | inferencia | programa | ao_vivo | 2026-11-04T00:31:14 | proposta: 158,8 s |
| 1954 | 26 | edicao_biblioteca | programa | ao_vivo | 2026-11-04T00:31:14 | proposta 1: nota em [resposta_truncada]: recusada: duplicada |
| 1956 | 27 | edicao_biblioteca | programa | ao_vivo | 2026-11-04T00:31:14 | proposta 2: novo_verbete em [resposta_truncada_correta]: recusada: teto_verbetes_novos |
| 1957 | 28 | decisao | programa | ao_vivo | 2026-11-04T00:31:14 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 1949, `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido; evidência: evento 1925 (verbete_entregue, contrato-pedido), evento 1925 (verbete_entregue, resposta_truncada), evento 1925 (verbete_entregue, formato_de_data_divergente), evento 1929 (resposta), evento 1934 (verbete_citado, resposta_truncada), evento 1935 (verbete_citado, formato_de_data_divergente); divergência: não; falha: nenhuma; prov.used: contrato-pedido, resposta_truncada, formato_de_data_divergente (gen_ai: chat)
- evento 1957, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 1929 (resposta), evento 1952 (resposta), evento 1954 (verbete_entregue, resposta_truncada); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: contrato-pedido, formato_de_data_divergente, resposta_truncada

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1924 a 1957 da trilha; hash dos eventos deste caso: `84245e47cbed06d4`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
