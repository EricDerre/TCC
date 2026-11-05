<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-11`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/efe-11@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `localizador_quebrado` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,51)

**IMPACTO (declarado):** `A ordem aleatória dos cartões é causada pela falta de um ORDER BY na consulta da API, resultando em uma ordem indeterminada dos produtos.`

Justificativa (gerada por molde): O agente respondeu localizador_quebrado porque os verbetes contagem_inconsistente, entidade-produto, localizador_quebrado estavam entre os entregues ao modelo. A segunda causa, contagem_inconsistente, ficou com probabilidade 0,47. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,51); trate como hipótese e confira o caso antes de agir.

**Biblioteca:** 1 edição(ões) aplicada(s) ([localizador_quebrado]), 0 para revisão humana, 1 recusada(s) (teto_verbetes_novos).

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso efe-11. A proposta 1 (nota em [localizador_quebrado], peso 1) passou pela validação da Fase 3 e pelos filtros e entrou no lote. A proposta 2 (novo_verbete em [ordem_aleatoria]) foi recusada por a validação da Fase 3 com o código teto_verbetes_novos: 6 verbetes novos nesta época (teto 6).

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `localizador_quebrado` | aceita | nenhum | **aplicada** | 1 |
| 2 | novo_verbete | `ordem_aleatoria` | recusada: `teto_verbetes_novos` | nenhum | recusada: `teto_verbetes_novos` |  |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
(14 itens, na ordem de id 1 a 14)

SINTOMA OBSERVADO: Os cartoes aparecem em ordem aleatoria a cada recarregamento da pagina.
```

## 3. Contraste com a segunda causa

localizador_quebrado e não contagem_inconsistente: a escolha tem probabilidade 0,51 contra 0,47; verbete(s) na evidência: contagem_inconsistente, entidade-produto, localizador_quebrado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| localizador_quebrado | 0,51 | sim |
| contagem_inconsistente | 0,47 |  |
| estrutura_aninhada_divergente | 0,01 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| tempo_de_resposta_excedido | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| resposta_truncada | 0,00 |  |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| nulo_inesperado | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `contagem_inconsistente`, `entidade-produto`, `localizador_quebrado` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado` |
| fonte_formato_valido | `[localizador_quebrado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["localizador_quebrado"]} |
| fonte_contem_termo_da_causa | `localizador_quebrado` | confere | {"termo": "localizador_quebrado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1767 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:10:44 | caso efe-11 |
| 1768 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:10:44 | 3 de 40 verbetes entregues |
| 1770 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:10:44 | {"chars": 3305, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "bafca9d0867d", "sha": "bafca9d0867dc123"} |
| 1772 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:10:44 | diagnostico: 67,0 s |
| 1773 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:10:44 | causa_raiz: `localizador_quebrado` |
| 1774 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:10:44 | campo: `nenhum` |
| 1775 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:10:44 | impacto: `A ordem aleatória dos cartões é causada pela falta de um ORDER BY na consulta da API, resultando em uma ordem indeterminada dos produtos.` |
| 1776 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:10:44 | fonte: `[localizador_quebrado]` |
| 1777 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:10:44 | fonte_citada: `localizador_quebrado` |
| 1778 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T00:10:44 | quatro_linhas_presentes: confere |
| 1779 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:10:44 | rotulo_no_conjunto: confere |
| 1780 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:10:44 | fonte_existe_na_biblioteca: confere |
| 1781 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:10:44 | fonte_estava_no_contexto: confere |
| 1782 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:10:44 | campo_existe_no_caso: nao_se_aplica |
| 1783 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:10:44 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1784 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:10:44 | notas_nos_verbetes_citados: informativo |
| 1785 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:10:44 | impacto: nao_verificavel |
| 1786 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:10:44 | fonte_formato_valido: confere |
| 1787 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:10:44 | fonte_contem_termo_da_causa: confere |
| 1788 | 20 | decisao | programa | ao_vivo | 2026-11-04T00:10:44 | diagnostico: escolha localizador_quebrado; divergência não |
| 1791 | 21 | inferencia | programa | ao_vivo | 2026-11-04T00:11:55 | proposta: 154,8 s |
| 1793 | 22 | edicao_biblioteca | programa | ao_vivo | 2026-11-04T00:11:55 | proposta 1: nota em [localizador_quebrado]: aplicada |
| 1795 | 23 | edicao_biblioteca | programa | ao_vivo | 2026-11-04T00:11:55 | proposta 2: novo_verbete em [ordem_aleatoria]: recusada: teto_verbetes_novos |
| 1796 | 24 | decisao | programa | ao_vivo | 2026-11-04T00:11:55 | edicao_biblioteca: escolha proposta_1; divergência sim |

</details>

Nós de decisão:

- evento 1788, `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido; evidência: evento 1768 (verbete_entregue, contagem_inconsistente), evento 1768 (verbete_entregue, entidade-produto), evento 1768 (verbete_entregue, localizador_quebrado), evento 1772 (resposta), evento 1777 (verbete_citado, localizador_quebrado); divergência: não; falha: nenhuma; prov.used: contagem_inconsistente, entidade-produto, localizador_quebrado (gen_ai: chat)
- evento 1796, `edicao_biblioteca`: escolha `proposta_1`; resultado lote; evidência: evento 1772 (resposta), evento 1791 (resposta), evento 1793 (verbete_entregue, localizador_quebrado); divergência: sim; falha: nenhuma; prov.used: contagem_inconsistente, entidade-produto, estado_da_tela_divergente, localizador_quebrado

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1767 a 1796 da trilha; hash dos eventos deste caso: `d21eaa95cad18ed8`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
