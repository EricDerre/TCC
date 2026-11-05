<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-16`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/efe-16@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tempo_de_resposta_excedido` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,69)

**IMPACTO (declarado):** `O usuário vê apenas os produtos com data-id 1 e 3, ignorando o produto com data-id 2.`

Justificativa (gerada por molde): O agente respondeu tempo_de_resposta_excedido porque os verbetes localizador_quebrado, ancora-saiba-mais, tempo_de_resposta_excedido estavam entre os entregues ao modelo. A segunda causa, localizador_quebrado, ficou com probabilidade 0,30. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,69); trate como hipótese e confira o caso antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: (sem falha de rede) passo do roteiro: abrir detalhes do produto de data-id=2

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


SELETOR QUE FALHOU: button[data-id='2']

SINTOMA OBSERVADO: O roteiro falha por tempo esgotado; a pagina carregada agora so tem os cards de data-id 1 e 3 (o roteiro foi escrito pensando em outro estado da listagem).
```

## 3. Contraste com a segunda causa

tempo_de_resposta_excedido e não localizador_quebrado: a escolha tem probabilidade 0,69 contra 0,30; verbete(s) na evidência: localizador_quebrado, ancora-saiba-mais, tempo_de_resposta_excedido

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tempo_de_resposta_excedido | 0,69 | sim |
| localizador_quebrado | 0,30 |  |
| estado_da_tela_divergente | 0,00 |  |
| limite_de_requisicoes | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tempo_de_resposta_excedido]`; verbetes citados: `tempo_de_resposta_excedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tempo_de_resposta_excedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tempo_de_resposta_excedido` | confere | contexto: `localizador_quebrado`, `ancora-saiba-mais`, `tempo_de_resposta_excedido` |
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
| 2719 | 1 | entrada | programa | ao_vivo | 2026-11-04T01:11:29 | caso efe-16 |
| 2720 | 2 | candidatos | programa | ao_vivo | 2026-11-04T01:11:29 | 3 de 46 verbetes entregues |
| 2722 | 3 | prompt | programa | ao_vivo | 2026-11-04T01:11:29 | {"chars": 3889, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "eaff54d3f8fa", "sha": "eaff54d3f8fae454"} |
| 2724 | 4 | inferencia | programa | ao_vivo | 2026-11-04T01:11:29 | diagnostico: 75,3 s |
| 2725 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T01:11:29 | causa_raiz: `tempo_de_resposta_excedido` |
| 2726 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T01:11:29 | campo: `nenhum` |
| 2727 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T01:11:29 | impacto: `O usuário vê apenas os produtos com data-id 1 e 3, ignorando o produto com data-id 2.` |
| 2728 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T01:11:29 | fonte: `[tempo_de_resposta_excedido]` |
| 2729 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T01:11:29 | fonte_citada: `tempo_de_resposta_excedido` |
| 2730 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T01:11:29 | quatro_linhas_presentes: confere |
| 2731 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T01:11:29 | rotulo_no_conjunto: confere |
| 2732 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T01:11:29 | fonte_existe_na_biblioteca: confere |
| 2733 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T01:11:29 | fonte_estava_no_contexto: confere |
| 2734 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T01:11:29 | campo_existe_no_caso: nao_se_aplica |
| 2735 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T01:11:29 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2736 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T01:11:29 | notas_nos_verbetes_citados: informativo |
| 2737 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T01:11:29 | impacto: nao_verificavel |
| 2738 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T01:11:29 | fonte_formato_valido: confere |
| 2739 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T01:11:29 | fonte_contem_termo_da_causa: confere |
| 2740 | 20 | decisao | programa | ao_vivo | 2026-11-04T01:11:29 | diagnostico: escolha tempo_de_resposta_excedido; divergência não |

</details>

Nós de decisão:

- evento 2740, `diagnostico`: escolha `tempo_de_resposta_excedido`; resultado rotulo_emitido; evidência: evento 2720 (verbete_entregue, localizador_quebrado), evento 2720 (verbete_entregue, ancora-saiba-mais), evento 2720 (verbete_entregue, tempo_de_resposta_excedido), evento 2724 (resposta), evento 2729 (verbete_citado, tempo_de_resposta_excedido); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, ancora-saiba-mais, tempo_de_resposta_excedido (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2719 a 2740 da trilha; hash dos eventos deste caso: `424a10771cff7252`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
