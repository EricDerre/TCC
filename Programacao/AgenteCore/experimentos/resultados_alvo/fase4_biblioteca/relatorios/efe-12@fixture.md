<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-12`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/efe-12@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `localizador_quebrado` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário não consegue clicar no botão de preço correto, pois o seletor que deveria encontrar apenas um botão ficou ambíguo, encontrando dois.`

Justificativa (gerada por molde): O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, ancora-saiba-mais, corpo_nao_e_json estavam entre os entregues ao modelo. A segunda causa, nulo_inesperado, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 2 recusada(s) (redundante, texto_longo) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso efe-12. A proposta 1 (nota em [localizador_quebrado]) foi recusada por o filtro redundancia com o código redundante: 67% dos 3-gramas do TEXTO já estão em [localizador_quebrado]. A proposta 2 (retificacao em [localizador_quebrado]) foi recusada por a validação da Fase 3 com o código texto_longo: TEXTO com 296 caracteres (máximo 280).

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `localizador_quebrado` | aceita | redundancia | recusada: `redundante` | 1 |
| 2 | retificacao | `localizador_quebrado` | recusada: `texto_longo` | nenhum | recusada: `texto_longo` |  |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: (sem falha de rede) passo: clicar no primeiro botao de preco

STATUS HTTP: 200

CORPO DA RESPOSTA:
(nenhuma requisicao falhou)

ÁRVORE DE ACESSIBILIDADE DA PÁGINA:
document "Churrascaria Fornalha - Produtos (API)"
  navigation
    link "PRODUTOS"
    link "PRODUTOS (API)"
  main
    heading "Produtos via API" level=2
    group
      heading "Picanha ao Alho" level=3
      text "Carnes"
      button "R$ 89,90" disabled
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      button "R$ 69,90" disabled
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"


SELETOR QUE FALHOU: button[disabled]

SINTOMA OBSERVADO: O roteiro falha porque o seletor casou com dois botoes de preco.
```

## 3. Contraste com a segunda causa

localizador_quebrado e não nulo_inesperado: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: localizador_quebrado, ancora-saiba-mais, corpo_nao_e_json

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| localizador_quebrado | 1,00 | sim |
| nulo_inesperado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| contagem_inconsistente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `ancora-saiba-mais`, `corpo_nao_e_json` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado`, `ancora-saiba-mais` |
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
| 1798 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:14:35 | caso efe-12 |
| 1799 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:14:35 | 3 de 40 verbetes entregues |
| 1801 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:14:35 | {"chars": 3919, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "bfd1a441cf7f", "sha": "bfd1a441cf7f1d70"} |
| 1803 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:14:35 | diagnostico: 76,8 s |
| 1804 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:14:35 | causa_raiz: `localizador_quebrado` |
| 1805 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:14:35 | campo: `nenhum` |
| 1806 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:14:35 | impacto: `O usuário não consegue clicar no botão de preço correto, pois o seletor que deveria encontrar apenas um botão ficou ambíguo, encontrando dois.` |
| 1807 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:14:35 | fonte: `[localizador_quebrado]` |
| 1808 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:14:35 | fonte_citada: `localizador_quebrado` |
| 1809 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T00:14:35 | quatro_linhas_presentes: confere |
| 1810 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:14:35 | rotulo_no_conjunto: confere |
| 1811 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:14:35 | fonte_existe_na_biblioteca: confere |
| 1812 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:14:35 | fonte_estava_no_contexto: confere |
| 1813 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:14:35 | campo_existe_no_caso: nao_se_aplica |
| 1814 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:14:35 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1815 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:14:35 | notas_nos_verbetes_citados: informativo |
| 1816 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:14:35 | impacto: nao_verificavel |
| 1817 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:14:35 | fonte_formato_valido: confere |
| 1818 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:14:35 | fonte_contem_termo_da_causa: confere |
| 1819 | 20 | decisao | programa | ao_vivo | 2026-11-04T00:14:35 | diagnostico: escolha localizador_quebrado; divergência não |
| 1822 | 21 | inferencia | programa | ao_vivo | 2026-11-04T00:15:56 | proposta: 189,8 s |
| 1824 | 22 | edicao_biblioteca | programa | ao_vivo | 2026-11-04T00:15:56 | proposta 1: nota em [localizador_quebrado]: recusada: redundante |
| 1826 | 23 | edicao_biblioteca | programa | ao_vivo | 2026-11-04T00:15:56 | proposta 2: retificacao em [localizador_quebrado]: recusada: texto_longo |
| 1827 | 24 | decisao | programa | ao_vivo | 2026-11-04T00:15:56 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 1819, `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido; evidência: evento 1799 (verbete_entregue, localizador_quebrado), evento 1799 (verbete_entregue, ancora-saiba-mais), evento 1799 (verbete_entregue, corpo_nao_e_json), evento 1803 (resposta), evento 1808 (verbete_citado, localizador_quebrado); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, ancora-saiba-mais, corpo_nao_e_json (gen_ai: chat)
- evento 1827, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 1803 (resposta), evento 1822 (resposta), evento 1824 (verbete_entregue, localizador_quebrado), evento 1826 (verbete_entregue, localizador_quebrado); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: ancora-saiba-mais, corpo_nao_e_json, localizador_quebrado

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1798 a 1827 da trilha; hash dos eventos deste caso: `28bd596e407018ff`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
