<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-1`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/semt-1@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `preco` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê o preço formatado incorretamente, com vírgulas em vez de pontos e como texto ao invés de número.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo preco porque o sinal preco: esperado numero, recebido texto está presente na resposta HTTP e os verbetes campo_ausente, contrato-produto, campo_renomeado estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 281): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 283): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2096}, depois {"chars": 17}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | numero | texto |
| preco | 89.9 (referência em modo normal) | "89.9" em 14 itens |

Trecho podado (hash `b48b1bab39e02551`):

```text
{"preco": "89.9"}
```

Interceptação (evento 277): `GET /api/produtos` status 200; corpo `c7c256cfe391ed57`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: campo_ausente, contrato-produto, campo_renomeado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 1,00 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| resposta_truncada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [campo_ausente]`; verbetes citados: `contrato-produto`, `campo_ausente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `campo_ausente`, `contrato-produto`, `campo_renomeado` |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `campo_ausente`, `contrato-produto`, `campo_renomeado` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[contrato-produto] [campo_ausente]` | confere | {"ids": ["contrato-produto", "campo_ausente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `campo_ausente` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids semt-1 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 270 | 1 | entrada | programa | ao_vivo | 2026-11-01T14:17:03 | caso semt-1 |
| 271 | 2 | acao | programa | ao_vivo | 2026-11-01T14:17:04 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 192.9, "falhou": false} |
| 272 | 3 | acao | programa | ao_vivo | 2026-11-01T14:17:04 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 9.6, "falhou": false} |
| 273 | 4 | acao | programa | ao_vivo | 2026-11-01T14:17:04 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 4.8, "falhou": false} |
| 274 | 5 | acao | programa | ao_vivo | 2026-11-01T14:17:04 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 4.4, "falhou": false} |
| 275 | 6 | acao | programa | ao_vivo | 2026-11-01T14:17:04 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 4.9, "falhou": false} |
| 277 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T14:17:04 | GET /api/produtos 200 |
| 278 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T14:17:04 | conferencia_do_roteiro: confere |
| 279 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T14:17:04 | conferencia_do_roteiro: confere |
| 280 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T14:17:04 | conferencia_do_roteiro: confere |
| 281 | 11 | poda | programa | ao_vivo | 2026-11-01T14:17:04 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 283 | 12 | poda | programa | ao_vivo | 2026-11-01T14:17:04 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 284 | 13 | candidatos | programa | ao_vivo | 2026-11-01T14:17:04 | 3 de 40 verbetes entregues |
| 286 | 14 | prompt | programa | ao_vivo | 2026-11-01T14:17:04 | {"etapa": "diagnostico", "sha": "82cb40efb8df7e1a", "prompt_sha256": "82cb40efb8df", "chars": 5316, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 288 | 15 | inferencia | programa | ao_vivo | 2026-11-01T14:17:04 | diagnostico: 90,5 s |
| 289 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T14:17:04 | causa_raiz: `tipo_divergente` |
| 290 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T14:17:04 | campo: `preco` |
| 291 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T14:17:04 | impacto: `O usuário vê o preço formatado incorretamente, com vírgulas em vez de pontos e como texto ao invés de número.` |
| 292 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T14:17:04 | fonte: `[contrato-produto] [campo_ausente]` |
| 293 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T14:17:04 | fonte_citada: `contrato-produto` |
| 294 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T14:17:04 | fonte_citada: `campo_ausente` |
| 295 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T14:17:04 | quatro_linhas_presentes: confere |
| 296 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T14:17:04 | rotulo_no_conjunto: confere |
| 297 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T14:17:04 | fonte_existe_na_biblioteca: confere |
| 298 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T14:17:04 | fonte_existe_na_biblioteca: confere |
| 299 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T14:17:04 | fonte_estava_no_contexto: confere |
| 300 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T14:17:04 | fonte_estava_no_contexto: confere |
| 301 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T14:17:04 | campo_existe_no_caso: confere |
| 302 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T14:17:04 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 303 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T14:17:04 | notas_nos_verbetes_citados: informativo |
| 304 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T14:17:04 | impacto: nao_verificavel |
| 305 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T14:17:04 | fonte_formato_valido: confere |
| 306 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T14:17:04 | fonte_contem_termo_da_causa: nao_confere |
| 307 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T14:17:04 | fonte_contem_termo_da_causa: nao_confere |
| 308 | 35 | decisao | programa | ao_vivo | 2026-11-01T14:17:04 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 308, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 283 (sinal_em_codigo), evento 281 (arvore_podada), evento 277 (corpo_http), evento 284 (verbete_entregue, campo_ausente), evento 284 (verbete_entregue, contrato-produto), evento 284 (verbete_entregue, campo_renomeado), evento 288 (resposta), evento 293 (verbete_citado, contrato-produto), evento 294 (verbete_citado, campo_ausente); divergência: não; falha: nenhuma; prov.used: campo_ausente, contrato-produto, campo_renomeado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 270 a 308 da trilha; hash dos eventos deste caso: `24968572c6f7e09e`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
