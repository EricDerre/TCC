<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-20`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/tra-20@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,86)

**IMPACTO (declarado):** `A interface exibe uma lista de produtos em vez de um único produto, causando confusão no usuário.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto porque o sinal arvore: esperado 0 linha(s) da referência, recebido 0 linha(s) novas está presente na tela e os verbetes entidade-produto, contrato-produto, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,04 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 2053): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 0 linha(s) da referência | 0 linha(s) novas |

Trecho podado (hash `e4870f4dbbc1b73d`):

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
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
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

Poda de `corpo_http` (evento 2054): regras diff_contra_contrato; antes {"chars": 2068}, depois {"chars": 174}.

Trecho podado (hash `b78f8a85ed458c1a`):

```text
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 2049): `GET /api/produtos` status 200; corpo `0ef7077cc7a06cfa`, árvore `None`.

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não corpo_nao_e_json: a escolha tem probabilidade 0,86 contra 0,04; verbete(s) na evidência: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,86 | sim |
| corpo_nao_e_json | 0,04 |  |
| corpo_vazio | 0,04 |  |
| resposta_truncada | 0,04 |  |
| tipo_divergente | 0,03 |  |
| formato_de_data_divergente | 0,02 |  |
| estrutura_aninhada_divergente | 0,01 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [colecao_no_lugar_de_objeto]`; verbetes citados: `contrato-produto`, `colecao_no_lugar_de_objeto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `colecao_no_lugar_de_objeto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| O verbete citado estava no contexto entregue ao modelo | `colecao_no_lugar_de_objeto` | confere | contexto: `entidade-produto`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto`, `colecao_no_lugar_de_objeto` |
| fonte_formato_valido | `[contrato-produto] [colecao_no_lugar_de_objeto]` | confere | {"ids": ["contrato-produto", "colecao_no_lugar_de_objeto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |
| fonte_contem_termo_da_causa | `colecao_no_lugar_de_objeto` | confere | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids tra-20 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2043 | 1 | entrada | programa | ao_vivo | 2026-11-01T12:25:34 | caso tra-20 |
| 2044 | 2 | acao | programa | ao_vivo | 2026-11-01T12:25:34 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 115.8, "falhou": false} |
| 2045 | 3 | acao | programa | ao_vivo | 2026-11-01T12:25:34 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 15.8, "falhou": false} |
| 2046 | 4 | acao | programa | ao_vivo | 2026-11-01T12:25:34 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 12.3, "falhou": false} |
| 2047 | 5 | acao | programa | ao_vivo | 2026-11-01T12:25:34 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 7.9, "falhou": false} |
| 2048 | 6 | acao | programa | ao_vivo | 2026-11-01T12:25:34 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 8.9, "falhou": false} |
| 2049 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T12:25:34 | GET /api/produtos 200 |
| 2050 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T12:25:34 | conferencia_do_roteiro: confere |
| 2051 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T12:25:34 | conferencia_do_roteiro: confere |
| 2052 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T12:25:34 | conferencia_do_roteiro: confere |
| 2053 | 11 | poda | programa | ao_vivo | 2026-11-01T12:25:34 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 2054 | 12 | poda | programa | ao_vivo | 2026-11-01T12:25:34 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2055 | 13 | candidatos | programa | ao_vivo | 2026-11-01T12:25:34 | 3 de 40 verbetes entregues |
| 2056 | 14 | prompt | programa | ao_vivo | 2026-11-01T12:25:34 | {"etapa": "diagnostico", "sha": "64332b968215cf4b", "prompt_sha256": "64332b968215", "chars": 5509, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2057 | 15 | inferencia | programa | ao_vivo | 2026-11-01T12:25:34 | diagnostico: 18,2 s |
| 2058 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T12:25:34 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 2059 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T12:25:34 | campo: `nenhum` |
| 2060 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T12:25:34 | impacto: `A interface exibe uma lista de produtos em vez de um único produto, causando confusão no usuário.` |
| 2061 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T12:25:34 | fonte: `[contrato-produto] [colecao_no_lugar_de_objeto]` |
| 2062 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T12:25:34 | fonte_citada: `contrato-produto` |
| 2063 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T12:25:34 | fonte_citada: `colecao_no_lugar_de_objeto` |
| 2064 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T12:25:34 | quatro_linhas_presentes: confere |
| 2065 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T12:25:34 | rotulo_no_conjunto: confere |
| 2066 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T12:25:34 | fonte_existe_na_biblioteca: confere |
| 2067 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T12:25:34 | fonte_existe_na_biblioteca: confere |
| 2068 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T12:25:34 | fonte_estava_no_contexto: confere |
| 2069 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T12:25:34 | fonte_estava_no_contexto: confere |
| 2070 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T12:25:34 | campo_existe_no_caso: nao_se_aplica |
| 2071 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T12:25:34 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2072 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T12:25:34 | notas_nos_verbetes_citados: informativo |
| 2073 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T12:25:34 | impacto: nao_verificavel |
| 2074 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T12:25:34 | fonte_formato_valido: confere |
| 2075 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T12:25:34 | fonte_contem_termo_da_causa: nao_confere |
| 2076 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T12:25:34 | fonte_contem_termo_da_causa: confere |
| 2077 | 35 | decisao | programa | ao_vivo | 2026-11-01T12:25:34 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 2077, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 2054 (sinal_em_codigo), evento 2053 (arvore_podada), evento 2049 (corpo_http), evento 2055 (verbete_entregue, entidade-produto), evento 2055 (verbete_entregue, contrato-produto), evento 2055 (verbete_entregue, colecao_no_lugar_de_objeto), evento 2057 (resposta), evento 2062 (verbete_citado, contrato-produto), evento 2063 (verbete_citado, colecao_no_lugar_de_objeto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2043 a 2077 da trilha; hash dos eventos deste caso: `e93e6527d688a26d`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
