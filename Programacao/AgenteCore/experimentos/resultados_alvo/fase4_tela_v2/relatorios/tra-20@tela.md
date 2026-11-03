<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-20`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/tra-20@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `tipo` · selo de probabilidade: **medio** (p = 0,97)

**IMPACTO (declarado):** `O usuário vê categorias incorretas nos cartões de produtos na página, o que pode levar a confusão sobre as características dos itens.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo tipo porque o sinal tipo: esperado "Carnes" (referência em modo normal), recebido "Bebidas" em 4 itens está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, contagem_inconsistente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,03. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 2072): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 2073): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2068}, depois {"chars": 409}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tipo | "Carnes" (referência em modo normal) | "Bebidas" em 4 itens |

Trecho podado (hash `5b2f70798bfcb548`):

```text
lista com 14 itens (referência em modo normal: 14); tipo diferente em 4 itens; por exemplo: {"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Bebidas", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}; {"id": 10, "nome": "Refrigerante", "resumo": "Lata 350ml, diversos sabores", "tipo": "Acompanhamentos", "preco": 7.0, "imagem": "refrigerante.png", "destaque": false}
```

Interceptação (evento 2068): `GET /api/produtos` status 200; corpo `0ef7077cc7a06cfa`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 0,97 contra 0,03; verbete(s) na evidência: entidade-produto, contrato-produto, contagem_inconsistente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,97 | sim |
| campo_ausente | 0,03 |  |
| campo_renomeado | 0,03 |  |
| valor_fora_do_dominio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [entidade-produto]`; verbetes citados: `contrato-produto`, `entidade-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente` |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `contrato-produto` |
| fonte_formato_valido | `[contrato-produto] [entidade-produto]` | confere | {"ids": ["contrato-produto", "entidade-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids tra-20 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2062 | 1 | entrada | programa | ao_vivo | 2026-11-01T15:26:06 | caso tra-20 |
| 2063 | 2 | acao | programa | ao_vivo | 2026-11-01T15:26:07 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 179.0, "falhou": false} |
| 2064 | 3 | acao | programa | ao_vivo | 2026-11-01T15:26:07 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 7.0, "falhou": false} |
| 2065 | 4 | acao | programa | ao_vivo | 2026-11-01T15:26:07 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.3, "falhou": false} |
| 2066 | 5 | acao | programa | ao_vivo | 2026-11-01T15:26:07 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 6.9, "falhou": false} |
| 2067 | 6 | acao | programa | ao_vivo | 2026-11-01T15:26:07 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 4.9, "falhou": false} |
| 2068 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T15:26:07 | GET /api/produtos 200 |
| 2069 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T15:26:07 | conferencia_do_roteiro: confere |
| 2070 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T15:26:07 | conferencia_do_roteiro: confere |
| 2071 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T15:26:07 | conferencia_do_roteiro: confere |
| 2072 | 11 | poda | programa | ao_vivo | 2026-11-01T15:26:07 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 2073 | 12 | poda | programa | ao_vivo | 2026-11-01T15:26:07 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 2074 | 13 | candidatos | programa | ao_vivo | 2026-11-01T15:26:07 | 3 de 40 verbetes entregues |
| 2076 | 14 | prompt | programa | ao_vivo | 2026-11-01T15:26:07 | {"etapa": "diagnostico", "sha": "ef5b342fca3cf5c7", "prompt_sha256": "ef5b342fca3c", "chars": 5675, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2078 | 15 | inferencia | programa | ao_vivo | 2026-11-01T15:26:07 | diagnostico: 33,1 s |
| 2079 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T15:26:07 | causa_raiz: `tipo_divergente` |
| 2080 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T15:26:07 | campo: `tipo` |
| 2081 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T15:26:07 | impacto: `O usuário vê categorias incorretas nos cartões de produtos na página, o que pode levar a confusão sobre as características dos itens.` |
| 2082 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T15:26:07 | fonte: `[contrato-produto] [entidade-produto]` |
| 2083 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T15:26:07 | fonte_citada: `contrato-produto` |
| 2084 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T15:26:07 | fonte_citada: `entidade-produto` |
| 2085 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T15:26:07 | quatro_linhas_presentes: confere |
| 2086 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T15:26:07 | rotulo_no_conjunto: confere |
| 2087 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T15:26:07 | fonte_existe_na_biblioteca: confere |
| 2088 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T15:26:07 | fonte_existe_na_biblioteca: confere |
| 2089 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T15:26:07 | fonte_estava_no_contexto: confere |
| 2090 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T15:26:07 | fonte_estava_no_contexto: confere |
| 2091 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T15:26:07 | campo_existe_no_caso: confere |
| 2092 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T15:26:07 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2093 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T15:26:07 | notas_nos_verbetes_citados: informativo |
| 2094 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T15:26:07 | impacto: nao_verificavel |
| 2095 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T15:26:07 | fonte_formato_valido: confere |
| 2096 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T15:26:07 | fonte_contem_termo_da_causa: nao_confere |
| 2097 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T15:26:07 | fonte_contem_termo_da_causa: nao_confere |
| 2098 | 35 | decisao | programa | ao_vivo | 2026-11-01T15:26:07 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 2098, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 2073 (sinal_em_codigo), evento 2072 (arvore_podada), evento 2068 (corpo_http), evento 2074 (verbete_entregue, entidade-produto), evento 2074 (verbete_entregue, contrato-produto), evento 2074 (verbete_entregue, contagem_inconsistente), evento 2078 (resposta), evento 2083 (verbete_citado, contrato-produto), evento 2084 (verbete_citado, entidade-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, contagem_inconsistente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2062 a 2098 da trilha; hash dos eventos deste caso: `daa4e68415452adc`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
