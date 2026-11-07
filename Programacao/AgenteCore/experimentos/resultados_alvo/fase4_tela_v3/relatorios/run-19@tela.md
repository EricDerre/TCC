<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-19`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/run-19@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `preco` · selo de probabilidade: **baixo** (p = 0,55)

**IMPACTO (declarado):** `O usuário vê o preço formatado incorretamente, sem o sinal de moeda e com casas decimais ausentes.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo preco porque o sinal tempo_ms: esperado 18 ms (referência em modo normal), recebido 2015 ms está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, estado_da_tela_divergente estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,33. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,55); trate como hipótese e confira o campo preco antes de agir.

## 2. Evidência

Poda de `arvore` (evento 2108): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 197}, depois {"linhas": 42}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 0 linha(s) da referência | 0 linha(s) novas |

Trecho podado (hash `1d807eb42e97c234`):

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
  dialog
    heading "Picanha ao Alho" level=4
    text "Picanha grelhada com alho laminado na brasa"

```

Poda de `corpo_http` (evento 2109): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 161}, depois {"chars": 174}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tempo_ms | 18 ms (referência em modo normal) | 2015 ms |

Trecho podado (hash `b78f8a85ed458c1a`):

```text
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 2103): `GET /api/produtos` status 200; corpo `4b1bdd056e7a8c3b`, árvore `None`.

Interceptação (evento 2104): `GET /api/produtos/1` status 200; corpo `b5a0d0b69ce86861`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 0,55 contra 0,33; verbete(s) na evidência: entidade-produto, contrato-produto, estado_da_tela_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,55 | sim |
| colecao_no_lugar_de_objeto | 0,33 |  |
| campo_ausente | 0,08 |  |
| campo_renomeado | 0,08 |  |
| resposta_truncada | 0,01 |  |
| estrutura_aninhada_divergente | 0,01 |  |
| formato_de_data_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| tempo_de_resposta_excedido | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estado_da_tela_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estado_da_tela_divergente` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `contrato-produto` |
| fonte_formato_valido | `[entidade-produto], [contrato-produto]` | confere | {"ids": ["entidade-produto", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids run-19 --k 3`

## 6. Árvore completa

<details><summary>38 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2095 | 1 | entrada | programa | ao_vivo | 2026-11-05T19:51:43 | caso run-19 |
| 2096 | 2 | acao | programa | ao_vivo | 2026-11-05T19:52:15 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 121.6, "falhou": false} |
| 2097 | 3 | acao | programa | ao_vivo | 2026-11-05T19:52:15 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 28500.7, "falhou": false |
| 2098 | 4 | acao | programa | ao_vivo | 2026-11-05T19:52:15 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 1.7, "falhou": false} |
| 2099 | 5 | acao | programa | ao_vivo | 2026-11-05T19:52:15 | {"passo": 4, "acao": "clicar", "seletor": "#produtos-api-grid .saiba-mais[data-id='1']", "url": null, "tempo_ms": 26.7, "falhou": false} |
| 2100 | 6 | acao | programa | ao_vivo | 2026-11-05T19:52:15 | {"passo": 5, "acao": "esperar", "seletor": "#modalDetalhe", "url": null, "tempo_ms": 2381.9, "falhou": false} |
| 2101 | 7 | acao | programa | ao_vivo | 2026-11-05T19:52:15 | {"passo": 6, "acao": "conferir", "seletor": "#modalDetalheTitulo", "url": null, "tempo_ms": 3.0, "falhou": false} |
| 2102 | 8 | acao | programa | ao_vivo | 2026-11-05T19:52:15 | {"passo": 7, "acao": "conferir", "seletor": "#modalDetalheCorpo", "url": null, "tempo_ms": 3.0, "falhou": false} |
| 2103 | 9 | interceptacao | programa | ao_vivo | 2026-11-05T19:52:15 | GET /api/produtos 200 |
| 2104 | 10 | interceptacao | programa | ao_vivo | 2026-11-05T19:52:15 | GET /api/produtos/1 200 |
| 2105 | 11 | verificacao | verificacao | ao_vivo | 2026-11-05T19:52:15 | conferencia_do_roteiro: confere |
| 2106 | 12 | verificacao | verificacao | ao_vivo | 2026-11-05T19:52:15 | conferencia_do_roteiro: confere |
| 2107 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T19:52:15 | conferencia_do_roteiro: confere |
| 2108 | 14 | poda | programa | ao_vivo | 2026-11-05T19:52:15 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 2109 | 15 | poda | programa | ao_vivo | 2026-11-05T19:52:15 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 2110 | 16 | candidatos | programa | ao_vivo | 2026-11-05T19:52:15 | 3 de 39 verbetes entregues |
| 2112 | 17 | prompt | programa | ao_vivo | 2026-11-05T19:52:15 | {"etapa": "diagnostico", "sha": "bddf35f6cc23da97", "prompt_sha256": "bddf35f6cc23", "chars": 3627, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2114 | 18 | inferencia | programa | ao_vivo | 2026-11-05T19:52:15 | diagnostico: 51,3 s |
| 2115 | 19 | declaracao | modelo | ao_vivo | 2026-11-05T19:52:15 | causa_raiz: `tipo_divergente` |
| 2116 | 20 | declaracao | modelo | ao_vivo | 2026-11-05T19:52:15 | campo: `preco` |
| 2117 | 21 | declaracao | modelo | ao_vivo | 2026-11-05T19:52:15 | impacto: `O usuário vê o preço formatado incorretamente, sem o sinal de moeda e com casas decimais ausentes.` |
| 2118 | 22 | declaracao | modelo | ao_vivo | 2026-11-05T19:52:15 | fonte: `[entidade-produto], [contrato-produto]` |
| 2119 | 23 | declaracao | modelo | ao_vivo | 2026-11-05T19:52:15 | fonte_citada: `entidade-produto` |
| 2120 | 24 | declaracao | modelo | ao_vivo | 2026-11-05T19:52:15 | fonte_citada: `contrato-produto` |
| 2121 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T19:52:15 | quatro_linhas_presentes: confere |
| 2122 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T19:52:15 | rotulo_no_conjunto: confere |
| 2123 | 27 | verificacao | verificacao | ao_vivo | 2026-11-05T19:52:15 | fonte_existe_na_biblioteca: confere |
| 2124 | 28 | verificacao | verificacao | ao_vivo | 2026-11-05T19:52:15 | fonte_existe_na_biblioteca: confere |
| 2125 | 29 | verificacao | verificacao | ao_vivo | 2026-11-05T19:52:15 | fonte_estava_no_contexto: confere |
| 2126 | 30 | verificacao | verificacao | ao_vivo | 2026-11-05T19:52:15 | fonte_estava_no_contexto: confere |
| 2127 | 31 | verificacao | verificacao | ao_vivo | 2026-11-05T19:52:15 | campo_existe_no_caso: confere |
| 2128 | 32 | verificacao | verificacao | ao_vivo | 2026-11-05T19:52:15 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2129 | 33 | verificacao | verificacao | ao_vivo | 2026-11-05T19:52:15 | notas_nos_verbetes_citados: informativo |
| 2130 | 34 | verificacao | verificacao | ao_vivo | 2026-11-05T19:52:15 | impacto: nao_verificavel |
| 2131 | 35 | verificacao | verificacao | ao_vivo | 2026-11-05T19:52:15 | fonte_formato_valido: confere |
| 2132 | 36 | verificacao | verificacao | ao_vivo | 2026-11-05T19:52:15 | fonte_contem_termo_da_causa: nao_confere |
| 2133 | 37 | verificacao | verificacao | ao_vivo | 2026-11-05T19:52:15 | fonte_contem_termo_da_causa: nao_confere |
| 2134 | 38 | decisao | programa | ao_vivo | 2026-11-05T19:52:15 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 2134, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 2109 (sinal_em_codigo), evento 2108 (arvore_podada), evento 2104 (corpo_http), evento 2110 (verbete_entregue, entidade-produto), evento 2110 (verbete_entregue, contrato-produto), evento 2110 (verbete_entregue, estado_da_tela_divergente), evento 2114 (resposta), evento 2119 (verbete_citado, entidade-produto), evento 2120 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, estado_da_tela_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2095 a 2134 da trilha; hash dos eventos deste caso: `7886844b6ae9b429`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
