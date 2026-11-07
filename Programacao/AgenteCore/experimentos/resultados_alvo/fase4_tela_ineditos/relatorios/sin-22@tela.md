<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-22`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/sin-22@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `nome` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `A tela exibe um título vazio, pois o campo nome ausente não fornece o título correto para os produtos.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo nome porque o sinal nome: esperado texto, recebido None está presente na resposta HTTP e os verbetes campo_ausente, contrato-produto, entidade-produto estavam entre os entregues ao modelo. A segunda causa, campo_renomeado, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 348): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `a59adb210fd17df3`):

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
      heading "(sem nome)" level=3
      text "Carnes"
      text "Picanha grelhada com alho laminado na brasa"
      text "destaque: Sim"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "(sem nome)" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "(sem nome)" level=3
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

Poda de `corpo_http` (evento 350): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 1752}, depois {"chars": 21}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| nome | texto |  |

Trecho podado (hash `5406a4e0bdccaf7e`):

```text
{"nome": "(ausente)"}
```

Interceptação (evento 343): `GET /api/produtos` status 200; corpo `5e634a53e6e1c806`, árvore `None`.

## 3. Contraste com a segunda causa

campo_ausente e não campo_renomeado: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: campo_ausente, contrato-produto, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 1,00 | sim |
| campo_renomeado | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente] [contrato-produto]`; verbetes citados: `campo_ausente`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `campo_ausente`, `contrato-produto`, `entidade-produto` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `campo_ausente`, `contrato-produto`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `campo_ausente`, `contrato-produto` |
| fonte_formato_valido | `[campo_ausente] [contrato-produto]` | confere | {"ids": ["campo_ausente", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_ausente` | confere | {"termo": "campo_ausente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids sin-22 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 336 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:40:00 | caso sin-22 |
| 337 | 2 | acao | programa | ao_vivo | 2026-11-06T11:40:01 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 91.3, "falhou": false} |
| 338 | 3 | acao | programa | ao_vivo | 2026-11-06T11:40:01 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 6.9, "falhou": false} |
| 339 | 4 | acao | programa | ao_vivo | 2026-11-06T11:40:01 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.4, "falhou": false} |
| 340 | 5 | acao | programa | ao_vivo | 2026-11-06T11:40:01 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 5.8, "falhou": false} |
| 341 | 6 | acao | programa | ao_vivo | 2026-11-06T11:40:01 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.6, "falhou": false} |
| 343 | 7 | interceptacao | programa | ao_vivo | 2026-11-06T11:40:01 | GET /api/produtos 200 |
| 344 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T11:40:01 | conferencia_do_roteiro: confere |
| 345 | 9 | verificacao | verificacao | ao_vivo | 2026-11-06T11:40:01 | conferencia_do_roteiro: confere |
| 346 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:40:01 | conferencia_do_roteiro: confere |
| 348 | 11 | poda | programa | ao_vivo | 2026-11-06T11:40:01 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 350 | 12 | poda | programa | ao_vivo | 2026-11-06T11:40:01 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 351 | 13 | candidatos | programa | ao_vivo | 2026-11-06T11:40:01 | 3 de 39 verbetes entregues |
| 353 | 14 | prompt | programa | ao_vivo | 2026-11-06T11:40:01 | {"etapa": "diagnostico", "sha": "848ac816f0d17009", "prompt_sha256": "848ac816f0d1", "chars": 3440, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 355 | 15 | inferencia | programa | ao_vivo | 2026-11-06T11:40:01 | diagnostico: 69,3 s |
| 356 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T11:40:01 | causa_raiz: `campo_ausente` |
| 357 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T11:40:01 | campo: `nome` |
| 358 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T11:40:01 | impacto: `A tela exibe um título vazio, pois o campo nome ausente não fornece o título correto para os produtos.` |
| 359 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T11:40:01 | fonte: `[campo_ausente] [contrato-produto]` |
| 360 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T11:40:01 | fonte_citada: `campo_ausente` |
| 361 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T11:40:01 | fonte_citada: `contrato-produto` |
| 362 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:40:01 | quatro_linhas_presentes: confere |
| 363 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:40:01 | rotulo_no_conjunto: confere |
| 364 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:40:01 | fonte_existe_na_biblioteca: confere |
| 365 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:40:01 | fonte_existe_na_biblioteca: confere |
| 366 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:40:01 | fonte_estava_no_contexto: confere |
| 367 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T11:40:01 | fonte_estava_no_contexto: confere |
| 368 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T11:40:01 | campo_existe_no_caso: confere |
| 369 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T11:40:01 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 370 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T11:40:01 | notas_nos_verbetes_citados: informativo |
| 371 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T11:40:01 | impacto: nao_verificavel |
| 372 | 32 | verificacao | verificacao | ao_vivo | 2026-11-06T11:40:01 | fonte_formato_valido: confere |
| 373 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T11:40:01 | fonte_contem_termo_da_causa: confere |
| 374 | 34 | verificacao | verificacao | ao_vivo | 2026-11-06T11:40:01 | fonte_contem_termo_da_causa: nao_confere |
| 375 | 35 | decisao | programa | ao_vivo | 2026-11-06T11:40:01 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 375, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 350 (sinal_em_codigo), evento 348 (arvore_podada), evento 343 (corpo_http), evento 351 (verbete_entregue, campo_ausente), evento 351 (verbete_entregue, contrato-produto), evento 351 (verbete_entregue, entidade-produto), evento 355 (resposta), evento 360 (verbete_citado, campo_ausente), evento 361 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: campo_ausente, contrato-produto, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 336 a 375 da trilha; hash dos eventos deste caso: `ef4202c5b3e04a48`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
