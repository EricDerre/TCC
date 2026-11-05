<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-18`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/efe-18@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `localizador_quebrado` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário não vê nenhum card de produto, pois o roteiro não encontra nenhum elemento com o seletor fornecido.`

Justificativa (gerada por molde): O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, ancora-saiba-mais, pagina-produtos-api estavam entre os entregues ao modelo. A segunda causa, estado_da_tela_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: (sem falha de rede) passo do roteiro: localizar o card do produto pelo atributo data-testid

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


SELETOR QUE FALHOU: [data-testid="produto-card"]

SINTOMA OBSERVADO: O roteiro nao encontra nenhum card de produto; a pagina nao usa atributo data-testid em elemento nenhum.
```

## 3. Contraste com a segunda causa

localizador_quebrado e não estado_da_tela_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: localizador_quebrado, ancora-saiba-mais, pagina-produtos-api

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| localizador_quebrado | 1,00 | sim |
| estado_da_tela_divergente | 0,00 |  |
| nulo_inesperado | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `ancora-saiba-mais`, `pagina-produtos-api` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado`, `ancora-saiba-mais`, `pagina-produtos-api` |
| fonte_formato_valido | `[localizador_quebrado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["localizador_quebrado"]} |
| fonte_contem_termo_da_causa | `localizador_quebrado` | confere | {"termo": "localizador_quebrado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2765 | 1 | entrada | programa | ao_vivo | 2026-11-04T01:14:01 | caso efe-18 |
| 2766 | 2 | candidatos | programa | ao_vivo | 2026-11-04T01:14:01 | 3 de 46 verbetes entregues |
| 2768 | 3 | prompt | programa | ao_vivo | 2026-11-04T01:14:01 | {"chars": 3834, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "8b33ff7f7b0d", "sha": "8b33ff7f7b0da2c4"} |
| 2770 | 4 | inferencia | programa | ao_vivo | 2026-11-04T01:14:01 | diagnostico: 55,8 s |
| 2771 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T01:14:01 | causa_raiz: `localizador_quebrado` |
| 2772 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T01:14:01 | campo: `nenhum` |
| 2773 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T01:14:01 | impacto: `O usuário não vê nenhum card de produto, pois o roteiro não encontra nenhum elemento com o seletor fornecido.` |
| 2774 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T01:14:01 | fonte: `[localizador_quebrado]` |
| 2775 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T01:14:01 | fonte_citada: `localizador_quebrado` |
| 2776 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T01:14:01 | quatro_linhas_presentes: confere |
| 2777 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T01:14:01 | rotulo_no_conjunto: confere |
| 2778 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T01:14:01 | fonte_existe_na_biblioteca: confere |
| 2779 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T01:14:01 | fonte_estava_no_contexto: confere |
| 2780 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T01:14:01 | campo_existe_no_caso: nao_se_aplica |
| 2781 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T01:14:01 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2782 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T01:14:01 | notas_nos_verbetes_citados: informativo |
| 2783 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T01:14:01 | impacto: nao_verificavel |
| 2784 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T01:14:01 | fonte_formato_valido: confere |
| 2785 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T01:14:01 | fonte_contem_termo_da_causa: confere |
| 2786 | 20 | decisao | programa | ao_vivo | 2026-11-04T01:14:01 | diagnostico: escolha localizador_quebrado; divergência não |

</details>

Nós de decisão:

- evento 2786, `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido; evidência: evento 2766 (verbete_entregue, localizador_quebrado), evento 2766 (verbete_entregue, ancora-saiba-mais), evento 2766 (verbete_entregue, pagina-produtos-api), evento 2770 (resposta), evento 2775 (verbete_citado, localizador_quebrado); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, ancora-saiba-mais, pagina-produtos-api (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2765 a 2786 da trilha; hash dos eventos deste caso: `9cfb422cc75b9741`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
