<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `fase4_ensaio/qwen2.5_7b/localizador-front-busca#1`: o que o agente fez, declarou e conferiu

Trilha `fase4_ensaio/qwen2.5_7b/localizador-front-busca#1`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `localizador_quebrado` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário não consegue interagir com o campo de busca, resultando em uma experiência incompleta.`

Justificativa (gerada por molde): O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, tempo_de_resposta_excedido, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Alvo registrado na corrida de referência: searchbox "search" (ocorrência 1; tag `input`; caminho `#form-busca > div:nth-of-type(1) > input:nth-of-type(1)`; atributos {"id": "buscar", "class": "form-control", "name": "buscar", "type": "search", "placeholder": "Buscar produto", "aria-label": "search"}).

Candidatos na ordem fixa (limiar do nome 0.6); verificações na ordem fixa:

| Estratégia | Seletor | um elemento | visível e habilitado | mesmo papel | nome parecido | efeito na reexecução | Aplicado |
|---|---|---|---|---|---|---|---|
| `papel_e_nome` | `role=searchbox[name="search"]` | confere | confere | confere | confere ("search" contra "search": similaridade 1.00 (limiar 0.6)) | confere (o roteiro chegou ao fim: 2 conferência(s) passaram em 0.373 s) | **sim** |
| `papel_e_nome_parecido` | não gerado: nenhum searchbox da árvore podada tem nome parecido com "search" acima do limiar 0.6 | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `texto_contido` | não gerado: o alvo da referência não tem texto visível | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `data_id` | não gerado: o alvo da referência não tem data-id | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `caminho_do_ancestral_com_id` | `#form-busca > div:nth-of-type(1) > input:nth-of-type(1)` | confere | confere | confere | confere ("search" contra "search": similaridade 1.00 (limiar 0.6)) | não tentado |  |
| `posicao_entre_irmaos` | `#form-busca > div:nth-of-type(1) >> role=searchbox >> nth=0` | confere | confere | confere | confere ("search" contra "search": similaridade 1.00 (limiar 0.6)) | não tentado |  |

Poda de `arvore` (evento 245): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 250}, depois {"linhas": 37}.

Trecho podado (hash `81a89f6a009d036c`):

```text
document "Churrascaria Fornalha"
  navigation
    link "Logotipo Fornalha"
    link "DESTAQUES" href="index.php#destaques"
    link "PRODUTOS" href="index.php#produtos"
    link "PRODUTOS (API)" href="produtos_api.php"
    button "TIPOS" class="dropdown-toggle"
    link "CONTATO" href="index.php#contato"
    searchbox "search" id="buscar_v2" name="buscar" class="form-control"
  main
    heading "Destaques" level=2
    group
      heading "Picanha ao Alho" level=3
      text "Carnes"
      text "Picanha grelhada com alho laminado na b..."
      button "R$ 89,90" class="btn btn-default disable"
      link "Saiba Mais..." href="produto_detalhes.php?id_produto=1"
    group
      heading "Costelona" level=3
      text "Carnes"
      text "Costela assada lentamente por horas"
      button "R$ 79,90" class="btn btn-default disable"
      link "Saiba Mais..." href="produto_detalhes.php?id_produto=4"
    group
      heading "Cupim" level=3
      text "Carnes"
      text "Cupim assado lentamente, bem macio"
      button "R$ 76,90" class="btn btn-default disable"
      link "Saiba Mais..." href="produto_detalhes.php?id_produto=7"
    text "(mais 16 cartões omitidos pela poda)"
    heading "Produtos Gerais" level=2
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

## 3. Contraste com a segunda causa

localizador_quebrado e não tempo_de_resposta_excedido: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: localizador_quebrado, tempo_de_resposta_excedido, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| localizador_quebrado | 1,00 | sim |
| tempo_de_resposta_excedido | 0,00 |  |
| nulo_inesperado | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `tempo_de_resposta_excedido`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado` |
| fonte_formato_valido | `[localizador_quebrado]` | confere | {"ids": ["localizador_quebrado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `localizador_quebrado` | confere | {"termo": "localizador_quebrado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_reexec --repeticoes 1`

## 6. Árvore completa

<details><summary>37 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 241 | 1 | entrada | programa | ao_vivo | 2026-11-04T20:30:44 | caso None |
| 242 | 2 | acao | programa | ao_vivo | 2026-11-04T20:30:49 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "index.php", "tempo_ms": 154.8, "falhou": false, "reexecucao": 0} |
| 243 | 3 | acao | programa | ao_vivo | 2026-11-04T20:30:49 | {"passo": 2, "acao": "esperar", "seletor": "#buscar", "url": null, "tempo_ms": 5017.3, "falhou": true, "reexecucao": 0} |
| 245 | 4 | poda | programa | ao_vivo | 2026-11-04T20:30:49 | arvore: 0 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 246 | 5 | candidatos | programa | ao_vivo | 2026-11-04T20:30:49 | 3 de 39 verbetes entregues |
| 248 | 6 | prompt | programa | ao_vivo | 2026-11-04T20:30:49 | {"etapa": "diagnostico", "sha": "1a27c99f4bf7327d", "prompt_sha256": "1a27c99f4bf7", "chars": 5631, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 250 | 7 | inferencia | programa | ao_vivo | 2026-11-04T20:30:49 | diagnostico: 104,0 s |
| 251 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T20:30:49 | causa_raiz: `localizador_quebrado` |
| 252 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T20:30:49 | campo: `nenhum` |
| 253 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T20:30:49 | impacto: `O usuário não consegue interagir com o campo de busca, resultando em uma experiência incompleta.` |
| 254 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T20:30:49 | fonte: `[localizador_quebrado]` |
| 255 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T20:30:49 | fonte_citada: `localizador_quebrado` |
| 256 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T20:30:49 | quatro_linhas_presentes: confere |
| 257 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T20:30:49 | rotulo_no_conjunto: confere |
| 258 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T20:30:49 | fonte_existe_na_biblioteca: confere |
| 259 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T20:30:49 | fonte_estava_no_contexto: confere |
| 260 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T20:30:49 | campo_existe_no_caso: nao_se_aplica |
| 261 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T20:30:49 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 262 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T20:30:49 | notas_nos_verbetes_citados: informativo |
| 263 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T20:30:49 | impacto: nao_verificavel |
| 264 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T20:30:49 | fonte_formato_valido: confere |
| 265 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T20:30:49 | fonte_contem_termo_da_causa: confere |
| 266 | 23 | decisao | programa | ao_vivo | 2026-11-04T20:30:49 | diagnostico: escolha localizador_quebrado; divergência não |
| 267 | 24 | cura | programa | ao_vivo | 2026-11-04T20:32:35 | curado: 6 candidatos, 1 reexecução(ões); aplicado papel_e_nome; MTTR 106,5 s |
| 268 | 25 | decisao | programa | ao_vivo | 2026-11-04T20:32:35 | cura: escolha papel_e_nome; divergência sim |
| 269 | 26 | acao | programa | ao_vivo | 2026-11-04T20:32:35 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "index.php", "tempo_ms": 178.9, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado": f |
| 270 | 27 | acao | programa | ao_vivo | 2026-11-04T20:32:35 | {"passo": 2, "acao": "esperar", "seletor": "role=searchbox[name=\"search\"]", "url": null, "tempo_ms": 5.0, "falhou": false, "reexecucao": 1, "candidato": "pape |
| 271 | 28 | acao | programa | ao_vivo | 2026-11-04T20:32:35 | {"passo": 3, "acao": "preencher", "seletor": "role=searchbox[name=\"search\"]", "url": null, "tempo_ms": 7.4, "falhou": false, "reexecucao": 1, "candidato": "pa |
| 272 | 29 | acao | programa | ao_vivo | 2026-11-04T20:32:35 | {"passo": 4, "acao": "clicar", "seletor": "#form-busca button[type=submit]", "url": null, "tempo_ms": 92.2, "falhou": false, "reexecucao": 1, "candidato": "pape |
| 273 | 30 | acao | programa | ao_vivo | 2026-11-04T20:32:35 | {"passo": 5, "acao": "esperar", "seletor": ".thumbnail", "url": null, "tempo_ms": 29.7, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado": |
| 274 | 31 | acao | programa | ao_vivo | 2026-11-04T20:32:35 | {"passo": 6, "acao": "conferir", "seletor": ".thumbnail", "url": null, "tempo_ms": 11.7, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado" |
| 275 | 32 | acao | programa | ao_vivo | 2026-11-04T20:32:35 | {"passo": 7, "acao": "conferir", "seletor": "h2.breadcrumb", "url": null, "tempo_ms": 4.9, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curad |
| 276 | 33 | verificacao | verificacao | ao_vivo | 2026-11-04T20:32:35 | conferencia_do_roteiro: confere |
| 277 | 34 | verificacao | verificacao | ao_vivo | 2026-11-04T20:32:35 | conferencia_do_roteiro: confere |
| 278 | 35 | decisao | programa | ao_vivo | 2026-11-04T20:32:35 | reexecucao: escolha validada; divergência não |
| 279 | 36 | incidente | programa | ao_vivo | 2026-11-04T20:32:35 | {"tipo": "cdn_fora_do_har", "url": "https://code.jquery.com/jquery-2.2.0.min-js", "host": "code.jquery.com", "decisao": "har", "tipo_recurso": "script", "quando |
| 280 | 37 | incidente | programa | ao_vivo | 2026-11-04T20:32:35 | {"tipo": "cdn_fora_do_har", "url": "https://cdn.jsdelivr.net/npm/slick/slick.min.js", "host": "cdn.jsdelivr.net", "decisao": "har", "tipo_recurso": "script", "q |

</details>

Nós de decisão:

- evento 266, `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido; evidência: evento 245 (arvore_podada), evento 246 (verbete_entregue, localizador_quebrado), evento 246 (verbete_entregue, tempo_de_resposta_excedido), evento 246 (verbete_entregue, colecao_no_lugar_de_objeto), evento 250 (resposta), evento 255 (verbete_citado, localizador_quebrado); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, tempo_de_resposta_excedido, colecao_no_lugar_de_objeto (gen_ai: chat)
- evento 268, `cura`: escolha `papel_e_nome`; resultado cura_aplicada; evidência: evento 267 (candidato_de_seletor), evento 245 (arvore_podada); divergência: sim; falha: nenhuma; prov.used: papel_e_nome, caminho_do_ancestral_com_id, posicao_entre_irmaos (gen_ai: execute_tool)
- evento 278, `reexecucao`: escolha `validada`; resultado roteiro_concluido; evidência: evento 267 (candidato_de_seletor), evento 276 (sinal_em_codigo), evento 277 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: papel_e_nome

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 241 a 280 da trilha; hash dos eventos deste caso: `e9e4e3529b940a8a`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
