<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-15`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/efe-15@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `estado_da_tela_divergente` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê o botão de cancelar ainda habilitado e a reserva como ativa, enquanto a API confirmou o cancelamento.`

Justificativa (gerada por molde): O agente respondeu estado_da_tela_divergente porque os verbetes estado_da_tela_divergente, consultas-sem-checagem, contrato-pedido estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 2 recusada(s) (id_repetido, sem_evidencia_do_caso) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso efe-15. A proposta 1 (novo_verbete em [estado_da_tela_divergente]) foi recusada por a validação da Fase 3 com o código id_repetido: 'estado_da_tela_divergente' já é id de verbete ou nome de causa raiz. A proposta 2 (retificacao em [estado_da_tela_divergente]) foi recusada por o filtro evidencia_obrigatoria com o código sem_evidencia_do_caso: o MOTIVO não cita nenhum termo da evidência do caso (campo, status, rota, sintoma, chaves do corpo).

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | novo_verbete | `estado_da_tela_divergente` | recusada: `id_repetido` | nenhum | recusada: `id_repetido` |  |
| 2 | retificacao | `estado_da_tela_divergente` | aceita | evidencia_obrigatoria | recusada: `sem_evidencia_do_caso` | 2 |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: POST /api/pedidos/7/cancelar -> 200 | tela permanece aberta

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
A API confirmou {"id_pedido": 7, "status": "Cancelado"}

SINTOMA OBSERVADO: O botao de cancelar continua habilitado e a reserva segue como ativa na tela.

OBSERVAÇÃO ADICIONAL: Recarregando a pagina, o estado aparece correto.
```

## 3. Contraste com a segunda causa

estado_da_tela_divergente e não formato_de_data_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: estado_da_tela_divergente, consultas-sem-checagem, contrato-pedido

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| estado_da_tela_divergente | 1,00 | sim |
| formato_de_data_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| tipo_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[estado_da_tela_divergente]`; verbetes citados: `estado_da_tela_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `estado_da_tela_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `estado_da_tela_divergente` | confere | contexto: `estado_da_tela_divergente`, `consultas-sem-checagem`, `contrato-pedido` |
| Algum verbete do contexto trata da causa respondida | `estado_da_tela_divergente` | confere | verbetes: `estado_da_tela_divergente`, `consultas-sem-checagem` |
| fonte_formato_valido | `[estado_da_tela_divergente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["estado_da_tela_divergente"]} |
| fonte_contem_termo_da_causa | `estado_da_tela_divergente` | confere | {"termo": "estado_da_tela_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1864 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:22:57 | caso efe-15 |
| 1865 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:22:57 | 3 de 40 verbetes entregues |
| 1867 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:22:57 | {"chars": 3207, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "de8e4c46afc1", "sha": "de8e4c46afc1674c"} |
| 1869 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:22:57 | diagnostico: 56,6 s |
| 1870 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:22:57 | causa_raiz: `estado_da_tela_divergente` |
| 1871 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:22:57 | campo: `nenhum` |
| 1872 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:22:57 | impacto: `O usuário vê o botão de cancelar ainda habilitado e a reserva como ativa, enquanto a API confirmou o cancelamento.` |
| 1873 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:22:57 | fonte: `[estado_da_tela_divergente]` |
| 1874 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:22:57 | fonte_citada: `estado_da_tela_divergente` |
| 1875 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T00:22:57 | quatro_linhas_presentes: confere |
| 1876 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:22:57 | rotulo_no_conjunto: confere |
| 1877 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:22:57 | fonte_existe_na_biblioteca: confere |
| 1878 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:22:57 | fonte_estava_no_contexto: confere |
| 1879 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:22:57 | campo_existe_no_caso: nao_se_aplica |
| 1880 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:22:57 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1881 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:22:57 | notas_nos_verbetes_citados: informativo |
| 1882 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:22:57 | impacto: nao_verificavel |
| 1883 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:22:57 | fonte_formato_valido: confere |
| 1884 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:22:57 | fonte_contem_termo_da_causa: confere |
| 1885 | 20 | decisao | programa | ao_vivo | 2026-11-04T00:22:57 | diagnostico: escolha estado_da_tela_divergente; divergência não |
| 1888 | 21 | inferencia | programa | ao_vivo | 2026-11-04T00:23:58 | proposta: 168,7 s |
| 1890 | 22 | edicao_biblioteca | programa | ao_vivo | 2026-11-04T00:23:58 | proposta 1: novo_verbete em [estado_da_tela_divergente]: recusada: id_repetido |
| 1892 | 23 | edicao_biblioteca | programa | ao_vivo | 2026-11-04T00:23:58 | proposta 2: retificacao em [estado_da_tela_divergente]: recusada: sem_evidencia_do_caso |
| 1893 | 24 | decisao | programa | ao_vivo | 2026-11-04T00:23:58 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 1885, `diagnostico`: escolha `estado_da_tela_divergente`; resultado rotulo_emitido; evidência: evento 1865 (verbete_entregue, estado_da_tela_divergente), evento 1865 (verbete_entregue, consultas-sem-checagem), evento 1865 (verbete_entregue, contrato-pedido), evento 1869 (resposta), evento 1874 (verbete_citado, estado_da_tela_divergente); divergência: não; falha: nenhuma; prov.used: estado_da_tela_divergente, consultas-sem-checagem, contrato-pedido (gen_ai: chat)
- evento 1893, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 1869 (resposta), evento 1888 (resposta), evento 1890 (verbete_entregue, estado_da_tela_divergente), evento 1892 (verbete_entregue, estado_da_tela_divergente); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: consultas-sem-checagem, contrato-pedido, estado_da_tela_divergente

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1864 a 1893 da trilha; hash dos eventos deste caso: `78e6d121ee5dcf51`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
