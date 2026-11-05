<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-13`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/sin-13@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `tipo` · selo de probabilidade: **medio** (p = 0,95) · **CONFLITO**: a FONTE cita o verbete tipo_divergente, fora do contexto entregue

**IMPACTO (declarado):** `O usuário vê o tipo do produto como um objeto JSON em vez de uma string, o que causa confusão e não permite a exibição correta dos dados na interface.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo tipo porque o sinal tipo: esperado texto, recebido objeto está presente na resposta HTTP e os verbetes campo_ausente, colecao_no_lugar_de_objeto, contrato-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,04. A FONTE cita 2 verbete(s), 1 fora do contexto entregue (tipo_divergente). O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a FONTE cita o verbete tipo_divergente, fora do contexto entregue. Este nó está marcado com a falha citacao_fora_do_contexto (origem: modelo).

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 1 recusada(s) (duplicada) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 1 edição(ões) para o caso sin-13. A proposta 1 (retificacao em [estrutura_aninhada_divergente]) foi recusada por a validação da Fase 3 com o código duplicada: [estrutura_aninhada_divergente] já tem uma nota com este texto.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | retificacao | `estrutura_aninhada_divergente` | recusada: `duplicada` | nenhum | recusada: `duplicada` |  |

Poda de `arvore` (evento 824): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `44439f441a244cf6`):

```text
document "Churrascaria Fornalha - Produtos (API)"
  navigation
    link "Logotipo Fornalha"
    link "DESTAQUES" href="index.php#destaques"
    link "PRODUTOS" href="index.php#produtos"
    link "PRODUTOS (API)" href="produtos_api.php"
    button "TIPOS" class="dropdown-toggle"
    link "CONTATO" href="index.php#contato"
    searchbox "search" id="buscar" name="buscar" class="form-control"
  main
    heading "Produtos via API" level=2
    group
      heading "Picanha ao Alho" level=3
      text "{"valor":"Carnes","moeda":"BRL"}"
      text "Picanha grelhada com alho laminado na brasa"
      text "destaque: Sim"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "{"valor":"Carnes","moeda":"BRL"}"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "{"valor":"Carnes","moeda":"BRL"}"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "R$ 69,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 825): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2404}, depois {"chars": 45}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tipo | texto | objeto |
| tipo | "Carnes" (referência em modo normal) | {"valor": "Carnes", "moeda": "BRL"} em 14 itens |

Trecho podado (hash `8b29b8105a557dd2`):

```text
{"tipo": {"valor": "Carnes", "moeda": "BRL"}}
```

Interceptação (evento 820): `GET /api/produtos` status 200; corpo `8166f86042f25264`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 0,95 contra 0,04; verbete(s) na evidência: campo_ausente, colecao_no_lugar_de_objeto, contrato-produto, estrutura_aninhada_divergente, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,95 | sim |
| campo_ausente | 0,04 |  |
| campo_renomeado | 0,04 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [tipo_divergente]`; verbetes citados: `contrato-produto`, `tipo_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `campo_ausente`, `colecao_no_lugar_de_objeto`, `contrato-produto`, `estrutura_aninhada_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | **não confere** | contexto: `campo_ausente`, `colecao_no_lugar_de_objeto`, `contrato-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[contrato-produto] [tipo_divergente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto", "tipo_divergente"]} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>38 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 814 | 1 | entrada | programa | ao_vivo | 2026-11-03T22:27:46 | caso sin-13 |
| 815 | 2 | acao | programa | ao_vivo | 2026-11-03T22:27:46 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 91.2, "url": "produtos_api.php"} |
| 816 | 3 | acao | programa | ao_vivo | 2026-11-03T22:27:46 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 9.6, "url": null} |
| 817 | 4 | acao | programa | ao_vivo | 2026-11-03T22:27:46 | {"acao": "conferir", "falhou": false, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 2.2, "url": null} |
| 818 | 5 | acao | programa | ao_vivo | 2026-11-03T22:27:46 | {"acao": "conferir", "falhou": false, "passo": 4, "seletor": "#produtos-api-grid .thumbnail .btn-default", "tempo_ms": 4.6, "url": null} |
| 819 | 6 | acao | programa | ao_vivo | 2026-11-03T22:27:46 | {"acao": "conferir", "falhou": false, "passo": 5, "seletor": "#produtos-api-status", "tempo_ms": 5.4, "url": null} |
| 820 | 7 | interceptacao | programa | ao_vivo | 2026-11-03T22:27:46 | GET /api/produtos 200 |
| 821 | 8 | verificacao | verificacao | ao_vivo | 2026-11-03T22:27:46 | conferencia_do_roteiro: confere |
| 822 | 9 | verificacao | verificacao | ao_vivo | 2026-11-03T22:27:46 | conferencia_do_roteiro: confere |
| 823 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T22:27:46 | conferencia_do_roteiro: confere |
| 824 | 11 | poda | programa | ao_vivo | 2026-11-03T22:27:46 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 825 | 12 | poda | programa | ao_vivo | 2026-11-03T22:27:46 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 826 | 13 | candidatos | programa | ao_vivo | 2026-11-03T22:27:46 | 3 de 40 verbetes entregues |
| 828 | 14 | prompt | programa | ao_vivo | 2026-11-03T22:27:46 | {"chars": 6572, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "2905699a2929", "sha": "2905699a292984d8"} |
| 830 | 15 | inferencia | programa | ao_vivo | 2026-11-03T22:27:46 | diagnostico: 121,5 s |
| 831 | 16 | declaracao | modelo | ao_vivo | 2026-11-03T22:27:46 | causa_raiz: `tipo_divergente` |
| 832 | 17 | declaracao | modelo | ao_vivo | 2026-11-03T22:27:46 | campo: `tipo` |
| 833 | 18 | declaracao | modelo | ao_vivo | 2026-11-03T22:27:46 | impacto: `O usuário vê o tipo do produto como um objeto JSON em vez de uma string, o que causa confusão e não permite a exibição correta dos dados na interface.` |
| 834 | 19 | declaracao | modelo | ao_vivo | 2026-11-03T22:27:46 | fonte: `[contrato-produto] [tipo_divergente]` |
| 835 | 20 | declaracao | modelo | ao_vivo | 2026-11-03T22:27:46 | fonte_citada: `contrato-produto` |
| 836 | 21 | declaracao | modelo | ao_vivo | 2026-11-03T22:27:46 | fonte_citada: `tipo_divergente` |
| 837 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T22:27:46 | quatro_linhas_presentes: confere |
| 838 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T22:27:46 | rotulo_no_conjunto: confere |
| 839 | 24 | verificacao | verificacao | ao_vivo | 2026-11-03T22:27:46 | fonte_existe_na_biblioteca: confere |
| 840 | 25 | verificacao | verificacao | ao_vivo | 2026-11-03T22:27:46 | fonte_existe_na_biblioteca: confere |
| 841 | 26 | verificacao | verificacao | ao_vivo | 2026-11-03T22:27:46 | fonte_estava_no_contexto: confere |
| 842 | 27 | verificacao | verificacao | ao_vivo | 2026-11-03T22:27:46 | fonte_estava_no_contexto: nao_confere |
| 843 | 28 | verificacao | verificacao | ao_vivo | 2026-11-03T22:27:46 | campo_existe_no_caso: confere |
| 844 | 29 | verificacao | verificacao | ao_vivo | 2026-11-03T22:27:46 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 845 | 30 | verificacao | verificacao | ao_vivo | 2026-11-03T22:27:46 | notas_nos_verbetes_citados: informativo |
| 846 | 31 | verificacao | verificacao | ao_vivo | 2026-11-03T22:27:46 | impacto: nao_verificavel |
| 847 | 32 | verificacao | verificacao | ao_vivo | 2026-11-03T22:27:46 | fonte_formato_valido: confere |
| 848 | 33 | verificacao | verificacao | ao_vivo | 2026-11-03T22:27:46 | fonte_contem_termo_da_causa: nao_confere |
| 849 | 34 | verificacao | verificacao | ao_vivo | 2026-11-03T22:27:46 | fonte_contem_termo_da_causa: confere |
| 850 | 35 | decisao | programa | ao_vivo | 2026-11-03T22:27:46 | diagnostico: escolha tipo_divergente; divergência sim |
| 853 | 36 | inferencia | programa | ao_vivo | 2026-11-03T22:29:51 | proposta: 148,8 s |
| 854 | 37 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:29:51 | proposta 1: retificacao em [estrutura_aninhada_divergente]: recusada: duplicada |
| 855 | 38 | decisao | programa | ao_vivo | 2026-11-03T22:29:51 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 850, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 825 (sinal_em_codigo), evento 824 (arvore_podada), evento 820 (corpo_http), evento 826 (verbete_entregue, campo_ausente), evento 826 (verbete_entregue, colecao_no_lugar_de_objeto), evento 826 (verbete_entregue, contrato-produto), evento 826 (verbete_entregue, estrutura_aninhada_divergente), evento 830 (resposta), evento 835 (verbete_citado, contrato-produto), evento 836 (verbete_citado, tipo_divergente); divergência: sim; falha: citacao_fora_do_contexto; prov.used: campo_ausente, colecao_no_lugar_de_objeto, contrato-produto, estrutura_aninhada_divergente, tipo_divergente (gen_ai: chat)
- evento 855, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 825 (sinal_em_codigo), evento 824 (arvore_podada), evento 820 (corpo_http), evento 830 (resposta), evento 853 (resposta), evento 854 (verbete_entregue, estrutura_aninhada_divergente); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: campo_ausente, colecao_no_lugar_de_objeto, contrato-produto, estrutura_aninhada_divergente

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 814 a 855 da trilha; hash dos eventos deste caso: `fad001881cd151d2`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
