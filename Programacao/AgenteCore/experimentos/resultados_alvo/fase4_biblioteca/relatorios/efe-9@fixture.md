<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-9`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/efe-9@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `localizador_quebrado` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário não consegue acessar as informações detalhadas do produto 1.`

Justificativa (gerada por molde): O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, ancora-saiba-mais, limites-do-sistema estavam entre os entregues ao modelo. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 2 recusada(s) (palavra_chave_invalida, palavra_chave_invalida) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso efe-9. A proposta 1 (nota em [localizador_quebrado]) foi recusada por a validação da Fase 3 com o código palavra_chave_invalida: item de lista inválido: '"ver mais" vs "saiba mais..."'. A proposta 2 (retificacao em [localizador_quebrado]) foi recusada por a validação da Fase 3 com o código palavra_chave_invalida: item de lista inválido: 'nth-child que funciona as vezes: ordem nao garantida'.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `localizador_quebrado` | recusada: `palavra_chave_invalida` | nenhum | recusada: `palavra_chave_invalida` |  |
| 2 | retificacao | `localizador_quebrado` | recusada: `palavra_chave_invalida` | nenhum | recusada: `palavra_chave_invalida` |  |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: (sem falha de rede) passo: abrir detalhes do produto 1

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


SELETOR QUE FALHOU: button[data-produto='1']

SINTOMA OBSERVADO: O roteiro nao localiza o botao; o atributo presente na pagina e data-id.
```

## 3. Contraste com a segunda causa

localizador_quebrado sem alternativa registrada no nó

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| localizador_quebrado | 1,00 | sim |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `ancora-saiba-mais`, `limites-do-sistema` |
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
| 1701 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:02:44 | caso efe-9 |
| 1702 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:02:44 | 3 de 40 verbetes entregues |
| 1704 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:02:44 | {"chars": 3680, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "edd9c6363198", "sha": "edd9c636319897b9"} |
| 1706 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:02:44 | diagnostico: 68,7 s |
| 1707 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:02:44 | causa_raiz: `localizador_quebrado` |
| 1708 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:02:44 | campo: `nenhum` |
| 1709 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:02:44 | impacto: `O usuário não consegue acessar as informações detalhadas do produto 1.` |
| 1710 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:02:44 | fonte: `[localizador_quebrado]` |
| 1711 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:02:44 | fonte_citada: `localizador_quebrado` |
| 1712 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T00:02:44 | quatro_linhas_presentes: confere |
| 1713 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:02:44 | rotulo_no_conjunto: confere |
| 1714 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:02:44 | fonte_existe_na_biblioteca: confere |
| 1715 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:02:44 | fonte_estava_no_contexto: confere |
| 1716 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:02:44 | campo_existe_no_caso: nao_se_aplica |
| 1717 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:02:44 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1718 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:02:44 | notas_nos_verbetes_citados: informativo |
| 1719 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:02:44 | impacto: nao_verificavel |
| 1720 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:02:44 | fonte_formato_valido: confere |
| 1721 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:02:44 | fonte_contem_termo_da_causa: confere |
| 1722 | 20 | decisao | programa | ao_vivo | 2026-11-04T00:02:44 | diagnostico: escolha localizador_quebrado; divergência não |
| 1725 | 21 | inferencia | programa | ao_vivo | 2026-11-04T00:03:57 | proposta: 158,2 s |
| 1727 | 22 | edicao_biblioteca | programa | ao_vivo | 2026-11-04T00:03:57 | proposta 1: nota em [localizador_quebrado]: recusada: palavra_chave_invalida |
| 1729 | 23 | edicao_biblioteca | programa | ao_vivo | 2026-11-04T00:03:57 | proposta 2: retificacao em [localizador_quebrado]: recusada: palavra_chave_invalida |
| 1730 | 24 | decisao | programa | ao_vivo | 2026-11-04T00:03:57 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 1722, `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido; evidência: evento 1702 (verbete_entregue, localizador_quebrado), evento 1702 (verbete_entregue, ancora-saiba-mais), evento 1702 (verbete_entregue, limites-do-sistema), evento 1706 (resposta), evento 1711 (verbete_citado, localizador_quebrado); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, ancora-saiba-mais, limites-do-sistema (gen_ai: chat)
- evento 1730, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 1706 (resposta), evento 1725 (resposta), evento 1727 (verbete_entregue, localizador_quebrado), evento 1729 (verbete_entregue, localizador_quebrado); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: ancora-saiba-mais, limites-do-sistema, localizador_quebrado

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1701 a 1730 da trilha; hash dos eventos deste caso: `c991101604ab40b6`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
