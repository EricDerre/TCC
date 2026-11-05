<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-17`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/efe-17@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `localizador_quebrado` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário não encontra o título "Picanha ao Alho" como heading de nível 2, o que causa confusão na navegação da página.`

Justificativa (gerada por molde): O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, entidade-produto, ancora-saiba-mais estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: (sem falha de rede) passo do roteiro: localizar o titulo 'Picanha ao Alho' como heading de nivel 2

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


SELETOR QUE FALHOU: heading "Picanha ao Alho" level=2

SINTOMA OBSERVADO: O roteiro nao encontra o titulo do produto; na arvore de acessibilidade o nome do produto e um heading de nivel 3, nao 2.
```

## 3. Contraste com a segunda causa

localizador_quebrado e não estrutura_aninhada_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: localizador_quebrado, entidade-produto, ancora-saiba-mais

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| localizador_quebrado | 1,00 | sim |
| estrutura_aninhada_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| nulo_inesperado | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `entidade-produto`, `ancora-saiba-mais` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado`, `ancora-saiba-mais` |
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
| 2742 | 1 | entrada | programa | ao_vivo | 2026-11-04T01:12:48 | caso efe-17 |
| 2743 | 2 | candidatos | programa | ao_vivo | 2026-11-04T01:12:48 | 3 de 46 verbetes entregues |
| 2745 | 3 | prompt | programa | ao_vivo | 2026-11-04T01:12:48 | {"chars": 3973, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "9f9f0131a049", "sha": "9f9f0131a049cda7"} |
| 2747 | 4 | inferencia | programa | ao_vivo | 2026-11-04T01:12:48 | diagnostico: 68,2 s |
| 2748 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T01:12:48 | causa_raiz: `localizador_quebrado` |
| 2749 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T01:12:48 | campo: `nenhum` |
| 2750 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T01:12:48 | impacto: `O usuário não encontra o título "Picanha ao Alho" como heading de nível 2, o que causa confusão na navegação da página.` |
| 2751 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T01:12:48 | fonte: `[localizador_quebrado]` |
| 2752 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T01:12:48 | fonte_citada: `localizador_quebrado` |
| 2753 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T01:12:48 | quatro_linhas_presentes: confere |
| 2754 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T01:12:48 | rotulo_no_conjunto: confere |
| 2755 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T01:12:48 | fonte_existe_na_biblioteca: confere |
| 2756 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T01:12:48 | fonte_estava_no_contexto: confere |
| 2757 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T01:12:48 | campo_existe_no_caso: nao_se_aplica |
| 2758 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T01:12:48 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2759 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T01:12:48 | notas_nos_verbetes_citados: informativo |
| 2760 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T01:12:48 | impacto: nao_verificavel |
| 2761 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T01:12:48 | fonte_formato_valido: confere |
| 2762 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T01:12:48 | fonte_contem_termo_da_causa: confere |
| 2763 | 20 | decisao | programa | ao_vivo | 2026-11-04T01:12:48 | diagnostico: escolha localizador_quebrado; divergência não |

</details>

Nós de decisão:

- evento 2763, `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido; evidência: evento 2743 (verbete_entregue, localizador_quebrado), evento 2743 (verbete_entregue, entidade-produto), evento 2743 (verbete_entregue, ancora-saiba-mais), evento 2747 (resposta), evento 2752 (verbete_citado, localizador_quebrado); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, entidade-produto, ancora-saiba-mais (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2742 a 2763 da trilha; hash dos eventos deste caso: `7eb41a4d3c4613d7`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
