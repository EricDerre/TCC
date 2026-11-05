<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-2`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/semt-2@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `destaque` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê o campo destaque como texto em vez de um booleano, o que pode causar confusão e problemas na interface.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo destaque porque o sinal destaque: esperado booleano, recebido texto está presente na resposta HTTP e os verbetes contrato-produto, campo_ausente, valor_fora_do_dominio estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 2 recusada(s) (texto_curto, arquivo_inexistente) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso semt-2. A proposta 1 (nota em [tipo_divergente]) foi recusada por a validação da Fase 3 com o código texto_curto: TEXTO com 52 caracteres (mínimo 60). A proposta 2 (retificacao em [valor_fora_do_dominio]) foi recusada por a validação da Fase 3 com o código arquivo_inexistente: ARQUIVOS cita 'tbprodutos': não existe no repositório.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `tipo_divergente` | recusada: `texto_curto` | nenhum | recusada: `texto_curto` |  |
| 2 | retificacao | `valor_fora_do_dominio` | recusada: `arquivo_inexistente` | nenhum | recusada: `arquivo_inexistente` |  |

Poda de `arvore` (evento 274): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `c313b8b1cf5627df`):

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
      text "destaque: True"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: False"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: False"
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

Poda de `corpo_http` (evento 276): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2096}, depois {"chars": 20}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| destaque | booleano | texto |
| destaque | true (referência em modo normal) | "True" em 14 itens |

Trecho podado (hash `5ec83198df34c240`):

```text
{"destaque": "True"}
```

Interceptação (evento 269): `GET /api/produtos` status 200; corpo `733c772e1d9b42a2`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não valor_fora_do_dominio: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-produto, campo_ausente, valor_fora_do_dominio

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 1,00 | sim |
| valor_fora_do_dominio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [valor_fora_do_dominio]`; verbetes citados: `contrato-produto`, `valor_fora_do_dominio`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `valor_fora_do_dominio` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `campo_ausente`, `valor_fora_do_dominio` |
| O verbete citado estava no contexto entregue ao modelo | `valor_fora_do_dominio` | confere | contexto: `contrato-produto`, `campo_ausente`, `valor_fora_do_dominio` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `contrato-produto`, `valor_fora_do_dominio` |
| fonte_formato_valido | `[contrato-produto], [valor_fora_do_dominio]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto", "valor_fora_do_dominio"]} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `valor_fora_do_dominio` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `destaque` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>39 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 262 | 1 | entrada | programa | ao_vivo | 2026-11-03T21:28:03 | caso semt-2 |
| 263 | 2 | acao | programa | ao_vivo | 2026-11-03T21:28:03 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 102.6, "url": "produtos_api.php"} |
| 264 | 3 | acao | programa | ao_vivo | 2026-11-03T21:28:03 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 8.0, "url": null} |
| 265 | 4 | acao | programa | ao_vivo | 2026-11-03T21:28:03 | {"acao": "conferir", "falhou": false, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 2.3, "url": null} |
| 266 | 5 | acao | programa | ao_vivo | 2026-11-03T21:28:03 | {"acao": "conferir", "falhou": false, "passo": 4, "seletor": "#produtos-api-grid .thumbnail .btn-default", "tempo_ms": 4.8, "url": null} |
| 267 | 6 | acao | programa | ao_vivo | 2026-11-03T21:28:03 | {"acao": "conferir", "falhou": false, "passo": 5, "seletor": "#produtos-api-status", "tempo_ms": 3.1, "url": null} |
| 269 | 7 | interceptacao | programa | ao_vivo | 2026-11-03T21:28:03 | GET /api/produtos 200 |
| 270 | 8 | verificacao | verificacao | ao_vivo | 2026-11-03T21:28:03 | conferencia_do_roteiro: confere |
| 271 | 9 | verificacao | verificacao | ao_vivo | 2026-11-03T21:28:03 | conferencia_do_roteiro: confere |
| 272 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T21:28:03 | conferencia_do_roteiro: confere |
| 274 | 11 | poda | programa | ao_vivo | 2026-11-03T21:28:03 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 276 | 12 | poda | programa | ao_vivo | 2026-11-03T21:28:03 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 277 | 13 | candidatos | programa | ao_vivo | 2026-11-03T21:28:03 | 3 de 40 verbetes entregues |
| 279 | 14 | prompt | programa | ao_vivo | 2026-11-03T21:28:03 | {"chars": 5590, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "fdf4ad2d39a1", "sha": "fdf4ad2d39a165fe"} |
| 281 | 15 | inferencia | programa | ao_vivo | 2026-11-03T21:28:03 | diagnostico: 106,5 s |
| 282 | 16 | declaracao | modelo | ao_vivo | 2026-11-03T21:28:03 | causa_raiz: `tipo_divergente` |
| 283 | 17 | declaracao | modelo | ao_vivo | 2026-11-03T21:28:03 | campo: `destaque` |
| 284 | 18 | declaracao | modelo | ao_vivo | 2026-11-03T21:28:03 | impacto: `O usuário vê o campo destaque como texto em vez de um booleano, o que pode causar confusão e problemas na interface.` |
| 285 | 19 | declaracao | modelo | ao_vivo | 2026-11-03T21:28:03 | fonte: `[contrato-produto], [valor_fora_do_dominio]` |
| 286 | 20 | declaracao | modelo | ao_vivo | 2026-11-03T21:28:03 | fonte_citada: `contrato-produto` |
| 287 | 21 | declaracao | modelo | ao_vivo | 2026-11-03T21:28:03 | fonte_citada: `valor_fora_do_dominio` |
| 288 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T21:28:03 | quatro_linhas_presentes: confere |
| 289 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T21:28:03 | rotulo_no_conjunto: confere |
| 290 | 24 | verificacao | verificacao | ao_vivo | 2026-11-03T21:28:03 | fonte_existe_na_biblioteca: confere |
| 291 | 25 | verificacao | verificacao | ao_vivo | 2026-11-03T21:28:03 | fonte_existe_na_biblioteca: confere |
| 292 | 26 | verificacao | verificacao | ao_vivo | 2026-11-03T21:28:03 | fonte_estava_no_contexto: confere |
| 293 | 27 | verificacao | verificacao | ao_vivo | 2026-11-03T21:28:03 | fonte_estava_no_contexto: confere |
| 294 | 28 | verificacao | verificacao | ao_vivo | 2026-11-03T21:28:03 | campo_existe_no_caso: confere |
| 295 | 29 | verificacao | verificacao | ao_vivo | 2026-11-03T21:28:03 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 296 | 30 | verificacao | verificacao | ao_vivo | 2026-11-03T21:28:03 | notas_nos_verbetes_citados: informativo |
| 297 | 31 | verificacao | verificacao | ao_vivo | 2026-11-03T21:28:03 | impacto: nao_verificavel |
| 298 | 32 | verificacao | verificacao | ao_vivo | 2026-11-03T21:28:03 | fonte_formato_valido: confere |
| 299 | 33 | verificacao | verificacao | ao_vivo | 2026-11-03T21:28:03 | fonte_contem_termo_da_causa: nao_confere |
| 300 | 34 | verificacao | verificacao | ao_vivo | 2026-11-03T21:28:03 | fonte_contem_termo_da_causa: nao_confere |
| 301 | 35 | decisao | programa | ao_vivo | 2026-11-03T21:28:03 | diagnostico: escolha tipo_divergente; divergência não |
| 304 | 36 | inferencia | programa | ao_vivo | 2026-11-03T21:29:54 | proposta: 160,2 s |
| 306 | 37 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:29:54 | proposta 1: nota em [tipo_divergente]: recusada: texto_curto |
| 308 | 38 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:29:54 | proposta 2: retificacao em [valor_fora_do_dominio]: recusada: arquivo_inexistente |
| 309 | 39 | decisao | programa | ao_vivo | 2026-11-03T21:29:54 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 301, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 276 (sinal_em_codigo), evento 274 (arvore_podada), evento 269 (corpo_http), evento 277 (verbete_entregue, contrato-produto), evento 277 (verbete_entregue, campo_ausente), evento 277 (verbete_entregue, valor_fora_do_dominio), evento 281 (resposta), evento 286 (verbete_citado, contrato-produto), evento 287 (verbete_citado, valor_fora_do_dominio); divergência: não; falha: nenhuma; prov.used: contrato-produto, campo_ausente, valor_fora_do_dominio (gen_ai: chat)
- evento 309, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 276 (sinal_em_codigo), evento 274 (arvore_podada), evento 269 (corpo_http), evento 281 (resposta), evento 304 (resposta), evento 306 (verbete_entregue, tipo_divergente), evento 308 (verbete_entregue, valor_fora_do_dominio); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: campo_ausente, contrato-produto, tipo_divergente, valor_fora_do_dominio

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 262 a 309 da trilha; hash dos eventos deste caso: `b9b24f8b7892b6fe`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
