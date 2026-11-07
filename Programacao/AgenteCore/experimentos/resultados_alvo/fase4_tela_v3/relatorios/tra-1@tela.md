<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-1`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/tra-1@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `escala_ou_unidade_errada` · **CAMPO:** `preco` · selo de probabilidade: **baixo** (p = 0,47)

**IMPACTO (declarado):** `O usuário vê preços com uma escala errada, exibidos como R$ 8990,00 em vez de R$ 89,90.`

Justificativa (gerada por molde): O agente respondeu escala_ou_unidade_errada no campo preco porque o sinal preco: esperado 89.9 (referência em modo normal), recebido 8990.0 em 14 itens está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,28 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,47); trate como hipótese e confira o campo preco antes de agir.

## 2. Evidência

Poda de `arvore` (evento 325): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 327): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2096}, depois {"chars": 270}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | 89.9 (referência em modo normal) | 8990.0 em 14 itens |

Trecho podado (hash `1cf6e56bcb7be5a1`):

```text
lista com 14 itens (referência em modo normal: 14); preco diferente em 14 itens; por exemplo: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 8990.0, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 320): `GET /api/produtos` status 200; corpo `61ba8740c5fc1841`, árvore `None`.

## 3. Contraste com a segunda causa

escala_ou_unidade_errada e não valor_fora_do_dominio: a escolha tem probabilidade 0,47 contra 0,28; verbete(s) na evidência: entidade-produto, contrato-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| escala_ou_unidade_errada | 0,47 | sim |
| valor_fora_do_dominio | 0,28 |  |
| tipo_divergente | 0,17 |  |
| formato_de_data_divergente | 0,05 |  |
| colecao_no_lugar_de_objeto | 0,02 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `escala_ou_unidade_errada` | confere | verbetes: `entidade-produto` |
| fonte_formato_valido | `[entidade-produto], [contrato-produto]` | confere | {"ids": ["entidade-produto", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "escala_ou_unidade_errada"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "escala_ou_unidade_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids tra-1 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 313 | 1 | entrada | programa | ao_vivo | 2026-11-05T18:51:29 | caso tra-1 |
| 314 | 2 | acao | programa | ao_vivo | 2026-11-05T18:51:29 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 156.1, "falhou": false} |
| 315 | 3 | acao | programa | ao_vivo | 2026-11-05T18:51:29 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 7.0, "falhou": false} |
| 316 | 4 | acao | programa | ao_vivo | 2026-11-05T18:51:29 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.8, "falhou": false} |
| 317 | 5 | acao | programa | ao_vivo | 2026-11-05T18:51:29 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 3.8, "falhou": false} |
| 318 | 6 | acao | programa | ao_vivo | 2026-11-05T18:51:29 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.4, "falhou": false} |
| 320 | 7 | interceptacao | programa | ao_vivo | 2026-11-05T18:51:29 | GET /api/produtos 200 |
| 321 | 8 | verificacao | verificacao | ao_vivo | 2026-11-05T18:51:29 | conferencia_do_roteiro: confere |
| 322 | 9 | verificacao | verificacao | ao_vivo | 2026-11-05T18:51:29 | conferencia_do_roteiro: confere |
| 323 | 10 | verificacao | verificacao | ao_vivo | 2026-11-05T18:51:29 | conferencia_do_roteiro: confere |
| 325 | 11 | poda | programa | ao_vivo | 2026-11-05T18:51:29 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 327 | 12 | poda | programa | ao_vivo | 2026-11-05T18:51:29 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 328 | 13 | candidatos | programa | ao_vivo | 2026-11-05T18:51:29 | 3 de 39 verbetes entregues |
| 330 | 14 | prompt | programa | ao_vivo | 2026-11-05T18:51:29 | {"etapa": "diagnostico", "sha": "b534319be9a34e24", "prompt_sha256": "b534319be9a3", "chars": 4127, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 332 | 15 | inferencia | programa | ao_vivo | 2026-11-05T18:51:29 | diagnostico: 50,0 s |
| 333 | 16 | declaracao | modelo | ao_vivo | 2026-11-05T18:51:29 | causa_raiz: `escala_ou_unidade_errada` |
| 334 | 17 | declaracao | modelo | ao_vivo | 2026-11-05T18:51:29 | campo: `preco` |
| 335 | 18 | declaracao | modelo | ao_vivo | 2026-11-05T18:51:29 | impacto: `O usuário vê preços com uma escala errada, exibidos como R$ 8990,00 em vez de R$ 89,90.` |
| 336 | 19 | declaracao | modelo | ao_vivo | 2026-11-05T18:51:29 | fonte: `[entidade-produto], [contrato-produto]` |
| 337 | 20 | declaracao | modelo | ao_vivo | 2026-11-05T18:51:29 | fonte_citada: `entidade-produto` |
| 338 | 21 | declaracao | modelo | ao_vivo | 2026-11-05T18:51:29 | fonte_citada: `contrato-produto` |
| 339 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T18:51:29 | quatro_linhas_presentes: confere |
| 340 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T18:51:29 | rotulo_no_conjunto: confere |
| 341 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T18:51:29 | fonte_existe_na_biblioteca: confere |
| 342 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T18:51:29 | fonte_existe_na_biblioteca: confere |
| 343 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T18:51:29 | fonte_estava_no_contexto: confere |
| 344 | 27 | verificacao | verificacao | ao_vivo | 2026-11-05T18:51:29 | fonte_estava_no_contexto: confere |
| 345 | 28 | verificacao | verificacao | ao_vivo | 2026-11-05T18:51:29 | campo_existe_no_caso: confere |
| 346 | 29 | verificacao | verificacao | ao_vivo | 2026-11-05T18:51:29 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 347 | 30 | verificacao | verificacao | ao_vivo | 2026-11-05T18:51:29 | notas_nos_verbetes_citados: informativo |
| 348 | 31 | verificacao | verificacao | ao_vivo | 2026-11-05T18:51:29 | impacto: nao_verificavel |
| 349 | 32 | verificacao | verificacao | ao_vivo | 2026-11-05T18:51:29 | fonte_formato_valido: confere |
| 350 | 33 | verificacao | verificacao | ao_vivo | 2026-11-05T18:51:29 | fonte_contem_termo_da_causa: nao_confere |
| 351 | 34 | verificacao | verificacao | ao_vivo | 2026-11-05T18:51:29 | fonte_contem_termo_da_causa: nao_confere |
| 352 | 35 | decisao | programa | ao_vivo | 2026-11-05T18:51:29 | diagnostico: escolha escala_ou_unidade_errada; divergência não |

</details>

Nós de decisão:

- evento 352, `diagnostico`: escolha `escala_ou_unidade_errada`; resultado rotulo_emitido; evidência: evento 327 (sinal_em_codigo), evento 325 (arvore_podada), evento 320 (corpo_http), evento 328 (verbete_entregue, entidade-produto), evento 328 (verbete_entregue, contrato-produto), evento 328 (verbete_entregue, estrutura_aninhada_divergente), evento 332 (resposta), evento 337 (verbete_citado, entidade-produto), evento 338 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 313 a 352 da trilha; hash dos eventos deste caso: `7f0a7af397d554ba`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
