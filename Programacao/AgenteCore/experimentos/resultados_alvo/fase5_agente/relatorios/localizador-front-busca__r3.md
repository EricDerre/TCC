<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `fase5_agente/qwen2.5_7b/localizador-front-busca#3`: o que o agente fez, declarou e conferiu

Trilha `fase5_agente/qwen2.5_7b/localizador-front-busca#3`; modelo `qwen2.5:7b`, Ollama 0.40.16, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `localizador_quebrado` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,87)

**IMPACTO (declarado):** `O usuário não consegue iniciar uma busca, pois o seletor do campo de busca não está sendo encontrado.`

Justificativa (gerada por molde): O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, tempo_de_resposta_excedido, limites-do-sistema estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Alvo registrado na corrida de referência: searchbox "search" (ocorrência 1; tag `input`; caminho `#form-busca > div:nth-of-type(1) > input:nth-of-type(1)`; atributos {"id": "buscar", "class": "form-control", "name": "buscar", "type": "search", "placeholder": "Buscar produto", "aria-label": "search"}).

Candidatos na ordem fixa (limiar do nome 0.6); verificações na ordem fixa:

| Estratégia | Seletor | um elemento | visível e habilitado | mesmo papel | nome parecido | efeito na reexecução | Aplicado |
|---|---|---|---|---|---|---|---|
| `papel_e_nome` | `role=searchbox[name="search"]` | confere | confere | confere | confere ("search" contra "search": similaridade 1.00 (limiar 0.6)) | confere (o roteiro chegou ao fim: 2 conferência(s) passaram em 0.33 s) | **sim** |
| `papel_e_nome_parecido` | não gerado: nenhum searchbox da árvore podada tem nome parecido com "search" acima do limiar 0.6 | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `texto_contido` | não gerado: o alvo da referência não tem texto visível | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `data_id` | não gerado: o alvo da referência não tem data-id | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `caminho_do_ancestral_com_id` | `#form-busca > div:nth-of-type(1) > input:nth-of-type(1)` | confere | confere | confere | confere ("search" contra "search": similaridade 1.00 (limiar 0.6)) | não tentado |  |
| `posicao_entre_irmaos` | `#form-busca > div:nth-of-type(1) >> role=searchbox >> nth=0` | confere | confere | confere | confere ("search" contra "search": similaridade 1.00 (limiar 0.6)) | não tentado |  |

Poda de `arvore` (evento 1000): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 250}, depois {"linhas": 37}.

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

localizador_quebrado e não tempo_de_resposta_excedido: a escolha tem probabilidade 0,87 contra 0,00; verbete(s) na evidência: localizador_quebrado, tempo_de_resposta_excedido, limites-do-sistema

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| localizador_quebrado | 0,87 | sim |
| tempo_de_resposta_excedido | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `tempo_de_resposta_excedido`, `limites-do-sistema` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado` |
| fonte_formato_valido | `[localizador_quebrado]` | confere | {"ids": ["localizador_quebrado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `localizador_quebrado` | confere | {"termo": "localizador_quebrado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Sugestão (o agente não altera a aplicação): no passo 2 do roteiro, trocar o localizador `#buscar` por `role=searchbox[name="search"]` (estratégia `papel_e_nome`), que resolve o mesmo elemento da referência.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase5_agente_reexec --repeticoes 1`

## 6. Árvore completa

<details><summary>37 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 997 | 1 | entrada | programa | ao_vivo | 2026-11-18T19:05:51 | caso None |
| 998 | 2 | acao | programa | ao_vivo | 2026-11-18T19:05:56 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "index.php", "tempo_ms": 179.7, "falhou": false, "reexecucao": 0} |
| 999 | 3 | acao | programa | ao_vivo | 2026-11-18T19:05:56 | {"passo": 2, "acao": "esperar", "seletor": "#buscar", "url": null, "tempo_ms": 5005.4, "falhou": true, "reexecucao": 0} |
| 1000 | 4 | poda | programa | ao_vivo | 2026-11-18T19:05:56 | arvore: 0 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1001 | 5 | candidatos | programa | ao_vivo | 2026-11-18T19:05:56 | 3 de 39 verbetes entregues |
| 1002 | 6 | prompt | programa | ao_vivo | 2026-11-18T19:05:56 | {"etapa": "diagnostico", "sha": "31455ff9966de9fd", "prompt_sha256": "31455ff9966d", "chars": 3586, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1003 | 7 | inferencia | programa | ao_vivo | 2026-11-18T19:05:56 | diagnostico: 36,5 s |
| 1004 | 8 | declaracao | modelo | ao_vivo | 2026-11-18T19:05:56 | causa_raiz: `localizador_quebrado` |
| 1005 | 9 | declaracao | modelo | ao_vivo | 2026-11-18T19:05:56 | campo: `nenhum` |
| 1006 | 10 | declaracao | modelo | ao_vivo | 2026-11-18T19:05:56 | impacto: `O usuário não consegue iniciar uma busca, pois o seletor do campo de busca não está sendo encontrado.` |
| 1007 | 11 | declaracao | modelo | ao_vivo | 2026-11-18T19:05:56 | fonte: `[localizador_quebrado]` |
| 1008 | 12 | declaracao | modelo | ao_vivo | 2026-11-18T19:05:56 | fonte_citada: `localizador_quebrado` |
| 1009 | 13 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:56 | quatro_linhas_presentes: confere |
| 1010 | 14 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:56 | rotulo_no_conjunto: confere |
| 1011 | 15 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:56 | fonte_existe_na_biblioteca: confere |
| 1012 | 16 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:56 | fonte_estava_no_contexto: confere |
| 1013 | 17 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:56 | campo_existe_no_caso: nao_se_aplica |
| 1014 | 18 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:56 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1015 | 19 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:56 | notas_nos_verbetes_citados: informativo |
| 1016 | 20 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:56 | impacto: nao_verificavel |
| 1017 | 21 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:56 | fonte_formato_valido: confere |
| 1018 | 22 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:56 | fonte_contem_termo_da_causa: confere |
| 1019 | 23 | decisao | programa | ao_vivo | 2026-11-18T19:05:56 | diagnostico: escolha localizador_quebrado; divergência não |
| 1020 | 24 | cura | programa | ao_vivo | 2026-11-18T19:06:35 | curado: 6 candidatos, 1 reexecução(ões); aplicado papel_e_nome; MTTR 39,3 s |
| 1021 | 25 | decisao | programa | ao_vivo | 2026-11-18T19:06:35 | cura: escolha papel_e_nome; divergência sim |
| 1022 | 26 | acao | programa | ao_vivo | 2026-11-18T19:06:35 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "index.php", "tempo_ms": 137.1, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado": f |
| 1023 | 27 | acao | programa | ao_vivo | 2026-11-18T19:06:35 | {"passo": 2, "acao": "esperar", "seletor": "role=searchbox[name=\"search\"]", "url": null, "tempo_ms": 5.0, "falhou": false, "reexecucao": 1, "candidato": "pape |
| 1024 | 28 | acao | programa | ao_vivo | 2026-11-18T19:06:35 | {"passo": 3, "acao": "preencher", "seletor": "role=searchbox[name=\"search\"]", "url": null, "tempo_ms": 7.6, "falhou": false, "reexecucao": 1, "candidato": "pa |
| 1025 | 29 | acao | programa | ao_vivo | 2026-11-18T19:06:35 | {"passo": 4, "acao": "clicar", "seletor": "#form-busca button[type=submit]", "url": null, "tempo_ms": 90.0, "falhou": false, "reexecucao": 1, "candidato": "pape |
| 1026 | 30 | acao | programa | ao_vivo | 2026-11-18T19:06:35 | {"passo": 5, "acao": "esperar", "seletor": ".thumbnail", "url": null, "tempo_ms": 31.0, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado": |
| 1027 | 31 | acao | programa | ao_vivo | 2026-11-18T19:06:35 | {"passo": 6, "acao": "conferir", "seletor": ".thumbnail", "url": null, "tempo_ms": 12.2, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado" |
| 1028 | 32 | acao | programa | ao_vivo | 2026-11-18T19:06:35 | {"passo": 7, "acao": "conferir", "seletor": "h2.breadcrumb", "url": null, "tempo_ms": 4.8, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curad |
| 1029 | 33 | verificacao | verificacao | ao_vivo | 2026-11-18T19:06:35 | conferencia_do_roteiro: confere |
| 1030 | 34 | verificacao | verificacao | ao_vivo | 2026-11-18T19:06:35 | conferencia_do_roteiro: confere |
| 1031 | 35 | decisao | programa | ao_vivo | 2026-11-18T19:06:35 | reexecucao: escolha validada; divergência não |
| 1032 | 36 | incidente | programa | ao_vivo | 2026-11-18T19:06:35 | {"tipo": "cdn_fora_do_har", "url": "https://code.jquery.com/jquery-2.2.0.min-js", "host": "code.jquery.com", "decisao": "har", "tipo_recurso": "script", "quando |
| 1033 | 37 | incidente | programa | ao_vivo | 2026-11-18T19:06:35 | {"tipo": "cdn_fora_do_har", "url": "https://cdn.jsdelivr.net/npm/slick/slick.min.js", "host": "cdn.jsdelivr.net", "decisao": "har", "tipo_recurso": "script", "q |

</details>

Nós de decisão:

- evento 1019, `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido; evidência: evento 1000 (arvore_podada), evento 1001 (verbete_entregue, localizador_quebrado), evento 1001 (verbete_entregue, tempo_de_resposta_excedido), evento 1001 (verbete_entregue, limites-do-sistema), evento 1003 (resposta), evento 1008 (verbete_citado, localizador_quebrado); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, tempo_de_resposta_excedido, limites-do-sistema (gen_ai: chat)
- evento 1021, `cura`: escolha `papel_e_nome`; resultado cura_aplicada; evidência: evento 1020 (candidato_de_seletor), evento 1000 (arvore_podada); divergência: sim; falha: nenhuma; prov.used: papel_e_nome, caminho_do_ancestral_com_id, posicao_entre_irmaos (gen_ai: execute_tool)
- evento 1031, `reexecucao`: escolha `validada`; resultado roteiro_concluido; evidência: evento 1020 (candidato_de_seletor), evento 1029 (sinal_em_codigo), evento 1030 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: papel_e_nome

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 997 a 1033 da trilha; hash dos eventos deste caso: `cb52f56ea4f876db`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
