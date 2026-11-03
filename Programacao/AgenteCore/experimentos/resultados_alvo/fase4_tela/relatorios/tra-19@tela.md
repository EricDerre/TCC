<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-19`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/tra-19@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `formato_de_data_divergente` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,50) · **CONFLITO**: nenhum verbete entregue trata da causa respondida formato_de_data_divergente

**IMPACTO (declarado):** `O preço exibido na tela está em um formato não esperado, com valores maiores que o esperado e sem a vírgula como separador decimal, causando confusão para o usuário.`

Justificativa (gerada por molde): O agente respondeu formato_de_data_divergente porque o sinal arvore: esperado 3 linha(s) da referência, recebido 3 linha(s) novas está presente na tela e os verbetes entidade-produto, nulo_inesperado, pagina-produtos-api estavam entre os entregues ao modelo. A segunda causa, contagem_inconsistente, ficou com probabilidade 0,32 e nenhum verbete entregue a sustenta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida formato_de_data_divergente. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,50); trate como hipótese e confira o caso antes de agir.

## 2. Evidência

Poda de `arvore` (evento 1994): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `b68e52486de88711`):

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
      button "R$ 8990,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 8490,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "R$ 6990,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 1995): regras diff_contra_contrato; antes {"chars": 2096}, depois {"chars": 176}.

Trecho podado (hash `3ebb397453143dfc`):

```text
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 8990.0, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 1990): `GET /api/produtos` status 200; corpo `61ba8740c5fc1841`, árvore `None`.

## 3. Contraste com a segunda causa

formato_de_data_divergente e não contagem_inconsistente: a escolha tem probabilidade 0,50 contra 0,32; verbete(s) na evidência: entidade-produto, nulo_inesperado, pagina-produtos-api

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| formato_de_data_divergente | 0,50 | sim |
| contagem_inconsistente | 0,32 |  |
| nulo_inesperado | 0,10 |  |
| tipo_divergente | 0,02 |  |
| escala_ou_unidade_errada | 0,02 |  |
| valor_fora_do_dominio | 0,01 |  |
| resposta_truncada | 0,01 |  |
| corpo_nao_e_json | 0,01 |  |
| corpo_vazio | 0,01 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[sinais: preço com grandeza estranha]`; verbetes citados: nenhum.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca |  | não se aplica | nenhum verbete citado na linha FONTE |
| O verbete citado estava no contexto entregue ao modelo |  | não se aplica | nenhum verbete citado na linha FONTE |
| Algum verbete do contexto trata da causa respondida | `formato_de_data_divergente` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[sinais: preço com grandeza estranha]` | não se aplica | nenhum verbete citado na linha FONTE |
| fonte_contem_termo_da_causa |  | não se aplica | sem causa ou sem verbete citado |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids tra-19 --k 3`

## 6. Árvore completa

<details><summary>30 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1984 | 1 | entrada | programa | ao_vivo | 2026-11-01T12:24:24 | caso tra-19 |
| 1985 | 2 | acao | programa | ao_vivo | 2026-11-01T12:24:24 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 89.7, "falhou": false} |
| 1986 | 3 | acao | programa | ao_vivo | 2026-11-01T12:24:24 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 11.7, "falhou": false} |
| 1987 | 4 | acao | programa | ao_vivo | 2026-11-01T12:24:24 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 3.3, "falhou": false} |
| 1988 | 5 | acao | programa | ao_vivo | 2026-11-01T12:24:24 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 4.8, "falhou": false} |
| 1989 | 6 | acao | programa | ao_vivo | 2026-11-01T12:24:24 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 5.7, "falhou": false} |
| 1990 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T12:24:24 | GET /api/produtos 200 |
| 1991 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:24 | conferencia_do_roteiro: confere |
| 1992 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:24 | conferencia_do_roteiro: confere |
| 1993 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:24 | conferencia_do_roteiro: confere |
| 1994 | 11 | poda | programa | ao_vivo | 2026-11-01T12:24:24 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1995 | 12 | poda | programa | ao_vivo | 2026-11-01T12:24:24 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1996 | 13 | candidatos | programa | ao_vivo | 2026-11-01T12:24:24 | 3 de 40 verbetes entregues |
| 1997 | 14 | prompt | programa | ao_vivo | 2026-11-01T12:24:24 | {"etapa": "diagnostico", "sha": "f6cacfa518fafcc4", "prompt_sha256": "f6cacfa518fa", "chars": 5269, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1999 | 15 | inferencia | programa | ao_vivo | 2026-11-01T12:24:24 | diagnostico: 21,9 s |
| 2000 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T12:24:24 | causa_raiz: `formato_de_data_divergente` |
| 2001 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T12:24:24 | campo: `nenhum` |
| 2002 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T12:24:24 | impacto: `O preço exibido na tela está em um formato não esperado, com valores maiores que o esperado e sem a vírgula como separador decimal, causando confusão para o usuário.` |
| 2003 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T12:24:24 | fonte: `[sinais: preço com grandeza estranha]` |
| 2004 | 20 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:24 | quatro_linhas_presentes: confere |
| 2005 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:24 | rotulo_no_conjunto: confere |
| 2006 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:24 | fonte_existe_na_biblioteca: nao_se_aplica |
| 2007 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:24 | fonte_estava_no_contexto: nao_se_aplica |
| 2008 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:24 | campo_existe_no_caso: nao_se_aplica |
| 2009 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:24 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 2010 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:24 | notas_nos_verbetes_citados: nao_se_aplica |
| 2011 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:24 | impacto: nao_verificavel |
| 2012 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:24 | fonte_formato_valido: nao_se_aplica |
| 2013 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:24 | fonte_contem_termo_da_causa: nao_se_aplica |
| 2014 | 30 | decisao | programa | ao_vivo | 2026-11-01T12:24:24 | diagnostico: escolha formato_de_data_divergente; divergência sim |

</details>

Nós de decisão:

- evento 2014, `diagnostico`: escolha `formato_de_data_divergente`; resultado rotulo_emitido; evidência: evento 1995 (sinal_em_codigo), evento 1994 (arvore_podada), evento 1990 (corpo_http), evento 1996 (verbete_entregue, entidade-produto), evento 1996 (verbete_entregue, nulo_inesperado), evento 1996 (verbete_entregue, pagina-produtos-api), evento 1999 (resposta); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, nulo_inesperado, pagina-produtos-api (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1984 a 2014 da trilha; hash dos eventos deste caso: `f50cf8d8cf4f3ec6`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
