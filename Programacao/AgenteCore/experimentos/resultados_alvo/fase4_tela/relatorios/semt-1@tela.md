<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-1`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/semt-1@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `preco` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê o preço formatado incorretamente, com um "R$" e uma vírgula, em vez de um valor numérico formatado corretamente.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo preco porque o sinal preco: esperado numero, recebido texto está presente na resposta HTTP e os verbetes campo_ausente, contrato-produto, campo_renomeado estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 280): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 282): regras diff_contra_contrato; antes {"chars": 2096}, depois {"chars": 17}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | numero | texto |

Trecho podado (hash `b48b1bab39e02551`):

```text
{"preco": "89.9"}
```

Interceptação (evento 276): `GET /api/produtos` status 200; corpo `c7c256cfe391ed57`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: campo_ausente, contrato-produto, campo_renomeado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 1,00 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `campo_ausente`, `contrato-produto`, `campo_renomeado` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids semt-1 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 269 | 1 | entrada | programa | ao_vivo | 2026-11-01T11:19:32 | caso semt-1 |
| 270 | 2 | acao | programa | ao_vivo | 2026-11-01T11:19:33 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 97.1, "falhou": false} |
| 271 | 3 | acao | programa | ao_vivo | 2026-11-01T11:19:33 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 12.8, "falhou": false} |
| 272 | 4 | acao | programa | ao_vivo | 2026-11-01T11:19:33 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 4.7, "falhou": false} |
| 273 | 5 | acao | programa | ao_vivo | 2026-11-01T11:19:33 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 8.8, "falhou": false} |
| 274 | 6 | acao | programa | ao_vivo | 2026-11-01T11:19:33 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 9.1, "falhou": false} |
| 276 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T11:19:33 | GET /api/produtos 200 |
| 277 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T11:19:33 | conferencia_do_roteiro: confere |
| 278 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T11:19:33 | conferencia_do_roteiro: confere |
| 279 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T11:19:33 | conferencia_do_roteiro: confere |
| 280 | 11 | poda | programa | ao_vivo | 2026-11-01T11:19:33 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 282 | 12 | poda | programa | ao_vivo | 2026-11-01T11:19:33 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 283 | 13 | candidatos | programa | ao_vivo | 2026-11-01T11:19:33 | 3 de 40 verbetes entregues |
| 285 | 14 | prompt | programa | ao_vivo | 2026-11-01T11:19:33 | {"etapa": "diagnostico", "sha": "1f3b5a59ea7e611e", "prompt_sha256": "1f3b5a59ea7e", "chars": 5185, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 287 | 15 | inferencia | programa | ao_vivo | 2026-11-01T11:19:33 | diagnostico: 88,5 s |
| 288 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T11:19:33 | causa_raiz: `tipo_divergente` |
| 289 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T11:19:33 | campo: `preco` |
| 290 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T11:19:33 | impacto: `O usuário vê o preço formatado incorretamente, com um "R$" e uma vírgula, em vez de um valor numérico formatado corretamente.` |
| 291 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T11:19:33 | fonte: `[contrato-produto]` |
| 292 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T11:19:33 | fonte_citada: `contrato-produto` |
| 293 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T11:19:33 | quatro_linhas_presentes: confere |
| 294 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T11:19:33 | rotulo_no_conjunto: confere |
| 295 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T11:19:33 | fonte_existe_na_biblioteca: confere |
| 296 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T11:19:33 | fonte_estava_no_contexto: confere |
| 297 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T11:19:33 | campo_existe_no_caso: confere |
| 298 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T11:19:33 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 299 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T11:19:33 | notas_nos_verbetes_citados: informativo |
| 300 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T11:19:33 | impacto: nao_verificavel |
| 301 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T11:19:33 | fonte_formato_valido: confere |
| 302 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T11:19:33 | fonte_contem_termo_da_causa: nao_confere |
| 303 | 31 | decisao | programa | ao_vivo | 2026-11-01T11:19:33 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 303, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 282 (sinal_em_codigo), evento 280 (arvore_podada), evento 276 (corpo_http), evento 283 (verbete_entregue, campo_ausente), evento 283 (verbete_entregue, contrato-produto), evento 283 (verbete_entregue, campo_renomeado), evento 287 (resposta), evento 292 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: campo_ausente, contrato-produto, campo_renomeado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 269 a 303 da trilha; hash dos eventos deste caso: `8c777c8e5e472dc3`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
