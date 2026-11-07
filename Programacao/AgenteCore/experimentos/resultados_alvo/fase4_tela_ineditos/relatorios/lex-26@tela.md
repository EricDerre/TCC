<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-26`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/lex-26@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nome` · selo de probabilidade: **medio** (p = 0,95)

**IMPACTO (declarado):** `O usuário vê o nome do produto com acentos corrompidos, mostrando "PÃ£o de Alho" em vez de "Pão de Alho".`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta no campo nome porque o sinal nome: esperado "Pão de Alho" (referência em modo normal), recebido "PÃ£o de Alho" está presente na resposta HTTP e os verbetes codificacao_incorreta, entidade-produto, contrato-produto estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 284): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 197}, depois {"linhas": 48}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 2 linha(s) da referência | 8 linha(s) novas |

Trecho podado (hash `34e5f67e9bad1b77`):

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
    text "(mais 10 cartões omitidos pela poda)"
    text "Ã\x81gua Mineral"
    text "Bebidas"
    text "Garrafa 500ml, com ou sem gás"
    text "destaque: Não"
    button "R$ 6,00" class="btn btn-default disable"
    button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="8"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"
  dialog
    heading "PÃ£o de Alho" level=4
    text "Pão de alho grelhado na brasa"

```

Poda de `corpo_http` (evento 286): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 152}, depois {"chars": 247}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| nome | "Pão de Alho" (referência em modo normal) | "PÃ£o de Alho" |

Trecho podado (hash `4e9ce587e292720f`):

```text
{"id": 11, "nome": "PÃ£o de Alho", "resumo": "Pão de alho grelhado na brasa", "tipo": "Acompanhamentos", "preco": 16.9, "imagem": "paodealho.png", "destaque": false} (contra a referência em modo normal: nome "PÃ£o de Alho" em vez de "Pão de Alho")
```

Interceptação (evento 277): `GET /api/produtos` status 200; corpo `0fd45da79aa14f8a`, árvore `None`.

Interceptação (evento 279): `GET /api/produtos/11` status 200; corpo `c3fb3ef03dac9d0f`, árvore `None`.

## 3. Contraste com a segunda causa

codificacao_incorreta e não corpo_nao_e_json: a escolha tem probabilidade 0,95 contra 0,00; verbete(s) na evidência: codificacao_incorreta, entidade-produto, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 0,95 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| tipo_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[codificacao_incorreta]`; verbetes citados: `codificacao_incorreta`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `codificacao_incorreta` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `codificacao_incorreta` | confere | contexto: `codificacao_incorreta`, `entidade-produto`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | confere | verbetes: `codificacao_incorreta` |
| fonte_formato_valido | `[codificacao_incorreta]` | confere | {"ids": ["codificacao_incorreta"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `codificacao_incorreta` | confere | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids lex-26 --k 3`

## 6. Árvore completa

<details><summary>34 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 269 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:37:46 | caso lex-26 |
| 270 | 2 | acao | programa | ao_vivo | 2026-11-06T11:37:47 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 121.3, "falhou": false} |
| 271 | 3 | acao | programa | ao_vivo | 2026-11-06T11:37:47 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 7.1, "falhou": false} |
| 272 | 4 | acao | programa | ao_vivo | 2026-11-06T11:37:47 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 3.1, "falhou": false} |
| 273 | 5 | acao | programa | ao_vivo | 2026-11-06T11:37:47 | {"passo": 4, "acao": "clicar", "seletor": "#produtos-api-grid .saiba-mais[data-id='11']", "url": null, "tempo_ms": 14.4, "falhou": false} |
| 274 | 6 | acao | programa | ao_vivo | 2026-11-06T11:37:47 | {"passo": 5, "acao": "esperar", "seletor": "#modalDetalhe", "url": null, "tempo_ms": 205.4, "falhou": false} |
| 275 | 7 | acao | programa | ao_vivo | 2026-11-06T11:37:47 | {"passo": 6, "acao": "conferir", "seletor": "#modalDetalheTitulo", "url": null, "tempo_ms": 3.5, "falhou": false} |
| 276 | 8 | acao | programa | ao_vivo | 2026-11-06T11:37:47 | {"passo": 7, "acao": "conferir", "seletor": "#modalDetalheCorpo", "url": null, "tempo_ms": 4.0, "falhou": false} |
| 277 | 9 | interceptacao | programa | ao_vivo | 2026-11-06T11:37:47 | GET /api/produtos 200 |
| 279 | 10 | interceptacao | programa | ao_vivo | 2026-11-06T11:37:47 | GET /api/produtos/11 200 |
| 280 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:37:47 | conferencia_do_roteiro: confere |
| 281 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:37:47 | conferencia_do_roteiro: confere |
| 282 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:37:47 | conferencia_do_roteiro: confere |
| 284 | 14 | poda | programa | ao_vivo | 2026-11-06T11:37:47 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 286 | 15 | poda | programa | ao_vivo | 2026-11-06T11:37:47 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 287 | 16 | candidatos | programa | ao_vivo | 2026-11-06T11:37:47 | 3 de 39 verbetes entregues |
| 289 | 17 | prompt | programa | ao_vivo | 2026-11-06T11:37:47 | {"etapa": "diagnostico", "sha": "94baac48e6ddeb9b", "prompt_sha256": "94baac48e6dd", "chars": 3796, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 291 | 18 | inferencia | programa | ao_vivo | 2026-11-06T11:37:47 | diagnostico: 50,2 s |
| 292 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T11:37:47 | causa_raiz: `codificacao_incorreta` |
| 293 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T11:37:47 | campo: `nome` |
| 294 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T11:37:47 | impacto: `O usuário vê o nome do produto com acentos corrompidos, mostrando "PÃ£o de Alho" em vez de "Pão de Alho".` |
| 295 | 22 | declaracao | modelo | ao_vivo | 2026-11-06T11:37:47 | fonte: `[codificacao_incorreta]` |
| 296 | 23 | declaracao | modelo | ao_vivo | 2026-11-06T11:37:47 | fonte_citada: `codificacao_incorreta` |
| 297 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:37:47 | quatro_linhas_presentes: confere |
| 298 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:37:47 | rotulo_no_conjunto: confere |
| 299 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:37:47 | fonte_existe_na_biblioteca: confere |
| 300 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T11:37:47 | fonte_estava_no_contexto: confere |
| 301 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T11:37:47 | campo_existe_no_caso: confere |
| 302 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T11:37:47 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 303 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T11:37:47 | notas_nos_verbetes_citados: informativo |
| 304 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T11:37:47 | impacto: nao_verificavel |
| 305 | 32 | verificacao | verificacao | ao_vivo | 2026-11-06T11:37:47 | fonte_formato_valido: confere |
| 306 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T11:37:47 | fonte_contem_termo_da_causa: confere |
| 307 | 34 | decisao | programa | ao_vivo | 2026-11-06T11:37:47 | diagnostico: escolha codificacao_incorreta; divergência não |

</details>

Nós de decisão:

- evento 307, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 286 (sinal_em_codigo), evento 284 (arvore_podada), evento 279 (corpo_http), evento 287 (verbete_entregue, codificacao_incorreta), evento 287 (verbete_entregue, entidade-produto), evento 287 (verbete_entregue, contrato-produto), evento 291 (resposta), evento 296 (verbete_citado, codificacao_incorreta); divergência: não; falha: nenhuma; prov.used: codificacao_incorreta, entidade-produto, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 269 a 307 da trilha; hash dos eventos deste caso: `e475656ee5d4c04b`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
