<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `contrato-field_renamed#1`: o que o agente fez, declarou e conferiu

Trilha `fase4_ensaio_v2/qwen2.5_7b/contrato-field_renamed#1`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_renomeado` · **CAMPO:** `preco` · selo de probabilidade: **medio** (p = 0,97) · **CONFLITO**: a FONTE cita o verbete preco_v2, que não existe na biblioteca; a FONTE cita o verbete preco_v2, fora do contexto entregue

**IMPACTO (declarado):** `O usuário vê botões com texto indefinido em vez de preços corretos, e a lista de produtos exibe um número incorreto de itens.`

Justificativa (gerada por molde): O agente respondeu campo_renomeado no campo preco porque o sinal preco: esperado preco, recebido preco_v2 está presente na resposta HTTP e os verbetes contagem_inconsistente, campo_ausente, nulo_inesperado estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,01 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), 2 fora do contexto entregue (campo_renomeado, preco_v2). O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a FONTE cita o verbete preco_v2, que não existe na biblioteca; a FONTE cita o verbete preco_v2, fora do contexto entregue. Este nó está marcado com a falha citacao_inexistente (origem: modelo).

## 2. Evidência

Poda de `arvore` (evento 92): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `714120f74ce44bb6`):

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
      text "Carnes"
      text "Picanha grelhada com alho laminado na brasa"
      text "destaque: Sim"
      button "undefined" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "undefined" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "undefined" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 94): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2110}, depois {"chars": 18}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | preco | preco_v2 |

Trecho podado (hash `3ca91df248763374`):

```text
{"preco_v2": 89.9}
```

Interceptação (evento 89): `GET /api/produtos` status 200; corpo `4f7726df03992678`, árvore `None`.

## 3. Contraste com a segunda causa

campo_renomeado e não corpo_nao_e_json: a escolha tem probabilidade 0,97 contra 0,01; verbete(s) na evidência: contagem_inconsistente, campo_ausente, nulo_inesperado, campo_renomeado, preco_v2

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_renomeado | 0,97 | sim |
| corpo_nao_e_json | 0,01 |  |
| corpo_vazio | 0,01 |  |
| campo_ausente | 0,01 |  |
| resposta_truncada | 0,00 |  |
| nulo_inesperado | 0,00 |  |
| contagem_inconsistente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_renomeado] [preco_v2]`; verbetes citados: `campo_renomeado`, `preco_v2`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado existe na biblioteca | `preco_v2` | **não confere** |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | **não confere** | contexto: `contagem_inconsistente`, `campo_ausente`, `nulo_inesperado` |
| O verbete citado estava no contexto entregue ao modelo | `preco_v2` | **não confere** | contexto: `contagem_inconsistente`, `campo_ausente`, `nulo_inesperado` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `campo_ausente` |
| fonte_formato_valido | `[campo_renomeado] [preco_v2]` | confere | {"ids": ["campo_renomeado", "preco_v2"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_renomeado` | confere | {"termo": "campo_renomeado"} |
| fonte_contem_termo_da_causa | `preco_v2` | não se aplica | verbete não encontrado na biblioteca |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v2_reexec --repeticoes 1`

## 6. Árvore completa

<details><summary>33 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 83 | 1 | entrada | programa | ao_vivo | 2026-11-04T21:36:15 | caso contrato-field_renamed#1 |
| 84 | 2 | acao | programa | ao_vivo | 2026-11-04T21:36:15 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 117.5, "falhou": false} |
| 85 | 3 | acao | programa | ao_vivo | 2026-11-04T21:36:15 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 9.0, "falhou": false} |
| 86 | 4 | acao | programa | ao_vivo | 2026-11-04T21:36:15 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.4, "falhou": false} |
| 87 | 5 | acao | programa | ao_vivo | 2026-11-04T21:36:15 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 4.4, "falhou": true} |
| 89 | 6 | interceptacao | programa | ao_vivo | 2026-11-04T21:36:15 | GET /api/produtos 200 |
| 90 | 7 | verificacao | verificacao | ao_vivo | 2026-11-04T21:36:15 | conferencia_do_roteiro: confere |
| 91 | 8 | verificacao | verificacao | ao_vivo | 2026-11-04T21:36:15 | conferencia_do_roteiro: nao_confere |
| 92 | 9 | poda | programa | ao_vivo | 2026-11-04T21:36:15 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 94 | 10 | poda | programa | ao_vivo | 2026-11-04T21:36:15 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 95 | 11 | candidatos | programa | ao_vivo | 2026-11-04T21:36:15 | 3 de 39 verbetes entregues |
| 97 | 12 | prompt | programa | ao_vivo | 2026-11-04T21:36:15 | {"etapa": "diagnostico", "sha": "d9aa01c028017fb6", "prompt_sha256": "d9aa01c02801", "chars": 5455, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 99 | 13 | inferencia | programa | ao_vivo | 2026-11-04T21:36:15 | diagnostico: 114,8 s |
| 100 | 14 | declaracao | modelo | ao_vivo | 2026-11-04T21:36:15 | causa_raiz: `campo_renomeado` |
| 101 | 15 | declaracao | modelo | ao_vivo | 2026-11-04T21:36:15 | campo: `preco` |
| 102 | 16 | declaracao | modelo | ao_vivo | 2026-11-04T21:36:15 | impacto: `O usuário vê botões com texto indefinido em vez de preços corretos, e a lista de produtos exibe um número incorreto de itens.` |
| 103 | 17 | declaracao | modelo | ao_vivo | 2026-11-04T21:36:15 | fonte: `[campo_renomeado] [preco_v2]` |
| 104 | 18 | declaracao | modelo | ao_vivo | 2026-11-04T21:36:15 | fonte_citada: `campo_renomeado` |
| 105 | 19 | declaracao | modelo | ao_vivo | 2026-11-04T21:36:15 | fonte_citada: `preco_v2` |
| 106 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T21:36:15 | quatro_linhas_presentes: confere |
| 107 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T21:36:15 | rotulo_no_conjunto: confere |
| 108 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T21:36:15 | fonte_existe_na_biblioteca: confere |
| 109 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T21:36:15 | fonte_existe_na_biblioteca: nao_confere |
| 110 | 24 | verificacao | verificacao | ao_vivo | 2026-11-04T21:36:15 | fonte_estava_no_contexto: nao_confere |
| 111 | 25 | verificacao | verificacao | ao_vivo | 2026-11-04T21:36:15 | fonte_estava_no_contexto: nao_confere |
| 112 | 26 | verificacao | verificacao | ao_vivo | 2026-11-04T21:36:15 | campo_existe_no_caso: confere |
| 113 | 27 | verificacao | verificacao | ao_vivo | 2026-11-04T21:36:15 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 114 | 28 | verificacao | verificacao | ao_vivo | 2026-11-04T21:36:15 | notas_nos_verbetes_citados: informativo |
| 115 | 29 | verificacao | verificacao | ao_vivo | 2026-11-04T21:36:15 | impacto: nao_verificavel |
| 116 | 30 | verificacao | verificacao | ao_vivo | 2026-11-04T21:36:15 | fonte_formato_valido: confere |
| 117 | 31 | verificacao | verificacao | ao_vivo | 2026-11-04T21:36:15 | fonte_contem_termo_da_causa: confere |
| 118 | 32 | verificacao | verificacao | ao_vivo | 2026-11-04T21:36:15 | fonte_contem_termo_da_causa: nao_se_aplica |
| 119 | 33 | decisao | programa | ao_vivo | 2026-11-04T21:36:15 | diagnostico: escolha campo_renomeado; divergência sim |

</details>

Nós de decisão:

- evento 119, `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido; evidência: evento 94 (sinal_em_codigo), evento 92 (arvore_podada), evento 89 (corpo_http), evento 95 (verbete_entregue, contagem_inconsistente), evento 95 (verbete_entregue, campo_ausente), evento 95 (verbete_entregue, nulo_inesperado), evento 99 (resposta), evento 104 (verbete_citado, campo_renomeado), evento 105 (verbete_citado, preco_v2); divergência: sim; falha: citacao_inexistente; prov.used: contagem_inconsistente, campo_ausente, nulo_inesperado, campo_renomeado, preco_v2 (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 83 a 119 da trilha; hash dos eventos deste caso: `a02a8eb1e75dc6c0`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
