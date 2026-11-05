<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-15`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/sin-15@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `tipo` · selo de probabilidade: **medio** (p = 0,98)

**IMPACTO (declarado):** `O usuário vê a categoria "Carnes" com colchetes ao redor no cartão, indicando que o formato não é o esperado.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto no campo tipo porque os verbetes entidade-produto, contrato-produto, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,02. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 1 edição(ões) aplicada(s) ([colecao_no_lugar_de_objeto]), 0 para revisão humana, 1 recusada(s) (redundante).

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso sin-15. A proposta 1 (nota em [colecao_no_lugar_de_objeto], peso 1) passou pela validação da Fase 3 e pelos filtros e entrou no lote. A proposta 2 (nota em [contrato-produto]) foi recusada por o filtro redundancia com o código redundante: 70% dos 3-gramas do TEXTO já estão em [contrato-produto].

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `colecao_no_lugar_de_objeto` | aceita | nenhum | **aplicada** | 1 |
| 2 | nota | `contrato-produto` | aceita | redundancia | recusada: `redundante` | 1 |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": ["Carnes"], "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: A categoria aparece como 'Carnes' com colchetes ao redor no cartao.
```

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não estrutura_aninhada_divergente: a escolha tem probabilidade 0,98 contra 0,02; verbete(s) na evidência: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,98 | sim |
| estrutura_aninhada_divergente | 0,02 |  |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [colecao_no_lugar_de_objeto]`; verbetes citados: `contrato-produto`, `colecao_no_lugar_de_objeto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `colecao_no_lugar_de_objeto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| O verbete citado estava no contexto entregue ao modelo | `colecao_no_lugar_de_objeto` | confere | contexto: `entidade-produto`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto`, `colecao_no_lugar_de_objeto` |
| fonte_formato_valido | `[contrato-produto] [colecao_no_lugar_de_objeto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto", "colecao_no_lugar_de_objeto"]} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |
| fonte_contem_termo_da_causa | `colecao_no_lugar_de_objeto` | confere | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>29 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 857 | 1 | entrada | programa | ao_vivo | 2026-11-03T22:32:25 | caso sin-15 |
| 858 | 2 | incidente | programa | ao_vivo | 2026-11-03T22:32:25 | {"detalhe": "nenhuma diferença medida contra o contrato, a referência e o roteiro", "tipo": "tela_nao_reproduz"} |
| 859 | 3 | candidatos | programa | ao_vivo | 2026-11-03T22:32:25 | 3 de 40 verbetes entregues |
| 861 | 4 | prompt | programa | ao_vivo | 2026-11-03T22:32:25 | {"chars": 3672, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "e599d4b8b0c5", "sha": "e599d4b8b0c59c86"} |
| 863 | 5 | inferencia | programa | ao_vivo | 2026-11-03T22:32:25 | diagnostico: 40,3 s |
| 864 | 6 | declaracao | modelo | ao_vivo | 2026-11-03T22:32:25 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 865 | 7 | declaracao | modelo | ao_vivo | 2026-11-03T22:32:25 | campo: `tipo` |
| 866 | 8 | declaracao | modelo | ao_vivo | 2026-11-03T22:32:25 | impacto: `O usuário vê a categoria "Carnes" com colchetes ao redor no cartão, indicando que o formato não é o esperado.` |
| 867 | 9 | declaracao | modelo | ao_vivo | 2026-11-03T22:32:25 | fonte: `[contrato-produto] [colecao_no_lugar_de_objeto]` |
| 868 | 10 | declaracao | modelo | ao_vivo | 2026-11-03T22:32:25 | fonte_citada: `contrato-produto` |
| 869 | 11 | declaracao | modelo | ao_vivo | 2026-11-03T22:32:25 | fonte_citada: `colecao_no_lugar_de_objeto` |
| 870 | 12 | verificacao | verificacao | ao_vivo | 2026-11-03T22:32:25 | quatro_linhas_presentes: confere |
| 871 | 13 | verificacao | verificacao | ao_vivo | 2026-11-03T22:32:25 | rotulo_no_conjunto: confere |
| 872 | 14 | verificacao | verificacao | ao_vivo | 2026-11-03T22:32:25 | fonte_existe_na_biblioteca: confere |
| 873 | 15 | verificacao | verificacao | ao_vivo | 2026-11-03T22:32:25 | fonte_existe_na_biblioteca: confere |
| 874 | 16 | verificacao | verificacao | ao_vivo | 2026-11-03T22:32:25 | fonte_estava_no_contexto: confere |
| 875 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T22:32:25 | fonte_estava_no_contexto: confere |
| 876 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T22:32:25 | campo_existe_no_caso: confere |
| 877 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T22:32:25 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 878 | 20 | verificacao | verificacao | ao_vivo | 2026-11-03T22:32:25 | notas_nos_verbetes_citados: informativo |
| 879 | 21 | verificacao | verificacao | ao_vivo | 2026-11-03T22:32:25 | impacto: nao_verificavel |
| 880 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T22:32:25 | fonte_formato_valido: confere |
| 881 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T22:32:25 | fonte_contem_termo_da_causa: nao_confere |
| 882 | 24 | verificacao | verificacao | ao_vivo | 2026-11-03T22:32:25 | fonte_contem_termo_da_causa: confere |
| 883 | 25 | decisao | programa | ao_vivo | 2026-11-03T22:32:25 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |
| 886 | 26 | inferencia | programa | ao_vivo | 2026-11-03T22:33:09 | proposta: 146,6 s |
| 888 | 27 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:33:09 | proposta 1: nota em [colecao_no_lugar_de_objeto]: aplicada |
| 890 | 28 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:33:09 | proposta 2: nota em [contrato-produto]: recusada: redundante |
| 891 | 29 | decisao | programa | ao_vivo | 2026-11-03T22:33:09 | edicao_biblioteca: escolha proposta_1; divergência sim |

</details>

Nós de decisão:

- evento 883, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 859 (verbete_entregue, entidade-produto), evento 859 (verbete_entregue, contrato-produto), evento 859 (verbete_entregue, colecao_no_lugar_de_objeto), evento 863 (resposta), evento 868 (verbete_citado, contrato-produto), evento 869 (verbete_citado, colecao_no_lugar_de_objeto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto (gen_ai: chat)
- evento 891, `edicao_biblioteca`: escolha `proposta_1`; resultado lote; evidência: evento 863 (resposta), evento 886 (resposta), evento 888 (verbete_entregue, colecao_no_lugar_de_objeto), evento 890 (verbete_entregue, contrato-produto); divergência: sim; falha: nenhuma; prov.used: colecao_no_lugar_de_objeto, contrato-produto, entidade-produto

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 857 a 891 da trilha; hash dos eventos deste caso: `4db93538243a1de9`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
