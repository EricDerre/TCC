<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-12`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/tra-12@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `escala_ou_unidade_errada` · **CAMPO:** `preco` · selo de probabilidade: **medio** (p = 0,94)

**IMPACTO (declarado):** `O usuário vê preços com valores errados, como R$ 8990,00 em vez de R$ 89,90.`

Justificativa (gerada por molde): O agente respondeu escala_ou_unidade_errada no campo preco porque o sinal preco: esperado 89.9 (referência em modo normal), recebido 8990.0 em 14 itens está presente na resposta HTTP e os verbetes entidade-produto, contagem_inconsistente, nulo_inesperado, escala_ou_unidade_errada estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,05. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 2 recusada(s) (duplicada, trecho_nao_encontrado) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso tra-12. A proposta 1 (nota em [escala_ou_unidade_errada]) foi recusada por a validação da Fase 3 com o código duplicada: [escala_ou_unidade_errada] já tem uma nota com este texto. A proposta 2 (retificacao em [escala_ou_unidade_errada]) foi recusada por a validação da Fase 3 com o código trecho_nao_encontrado: 'Adicionar exemplo de conversão incorreta de valor_produto DE' não aparece em [escala_ou_unidade_errada].

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `escala_ou_unidade_errada` | recusada: `duplicada` | nenhum | recusada: `duplicada` |  |
| 2 | retificacao | `escala_ou_unidade_errada` | recusada: `trecho_nao_encontrado` | nenhum | recusada: `trecho_nao_encontrado` |  |

Poda de `arvore` (evento 1285): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 1286): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2096}, depois {"chars": 434}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | 89.9 (referência em modo normal) | 8990.0 em 14 itens |

Trecho podado (hash `2f958e7c433d905b`):

```text
lista com 14 itens (referência em modo normal: 14); preco diferente em 14 itens; por exemplo: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 8990.0, "imagem": "picanha_alho.jpg", "destaque": true}; {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 8490.0, "imagem": "picanha_sem.jpg", "destaque": false}
```

Interceptação (evento 1281): `GET /api/produtos` status 200; corpo `61ba8740c5fc1841`, árvore `None`.

## 3. Contraste com a segunda causa

escala_ou_unidade_errada e não valor_fora_do_dominio: a escolha tem probabilidade 0,94 contra 0,05; verbete(s) na evidência: entidade-produto, contagem_inconsistente, nulo_inesperado, escala_ou_unidade_errada

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| escala_ou_unidade_errada | 0,94 | sim |
| valor_fora_do_dominio | 0,05 |  |
| formato_de_data_divergente | 0,01 |  |
| tipo_divergente | 0,00 |  |
| nulo_inesperado | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[escala_ou_unidade_errada]`; verbetes citados: `escala_ou_unidade_errada`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `escala_ou_unidade_errada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `escala_ou_unidade_errada` | confere | contexto: `entidade-produto`, `contagem_inconsistente`, `nulo_inesperado`, `escala_ou_unidade_errada` |
| Algum verbete do contexto trata da causa respondida | `escala_ou_unidade_errada` | confere | verbetes: `entidade-produto`, `escala_ou_unidade_errada` |
| fonte_formato_valido | `[escala_ou_unidade_errada]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["escala_ou_unidade_errada"]} |
| fonte_contem_termo_da_causa | `escala_ou_unidade_errada` | confere | {"termo": "escala_ou_unidade_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1275 | 1 | entrada | programa | ao_vivo | 2026-11-03T23:14:49 | caso tra-12 |
| 1276 | 2 | acao | programa | ao_vivo | 2026-11-03T23:14:50 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 152.9, "url": "produtos_api.php"} |
| 1277 | 3 | acao | programa | ao_vivo | 2026-11-03T23:14:50 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 7.2, "url": null} |
| 1278 | 4 | acao | programa | ao_vivo | 2026-11-03T23:14:50 | {"acao": "conferir", "falhou": false, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 2.8, "url": null} |
| 1279 | 5 | acao | programa | ao_vivo | 2026-11-03T23:14:50 | {"acao": "conferir", "falhou": false, "passo": 4, "seletor": "#produtos-api-grid .thumbnail .btn-default", "tempo_ms": 4.4, "url": null} |
| 1280 | 6 | acao | programa | ao_vivo | 2026-11-03T23:14:50 | {"acao": "conferir", "falhou": false, "passo": 5, "seletor": "#produtos-api-status", "tempo_ms": 3.5, "url": null} |
| 1281 | 7 | interceptacao | programa | ao_vivo | 2026-11-03T23:14:50 | GET /api/produtos 200 |
| 1282 | 8 | verificacao | verificacao | ao_vivo | 2026-11-03T23:14:50 | conferencia_do_roteiro: confere |
| 1283 | 9 | verificacao | verificacao | ao_vivo | 2026-11-03T23:14:50 | conferencia_do_roteiro: confere |
| 1284 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T23:14:50 | conferencia_do_roteiro: confere |
| 1285 | 11 | poda | programa | ao_vivo | 2026-11-03T23:14:50 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 1286 | 12 | poda | programa | ao_vivo | 2026-11-03T23:14:50 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1287 | 13 | candidatos | programa | ao_vivo | 2026-11-03T23:14:50 | 3 de 40 verbetes entregues |
| 1289 | 14 | prompt | programa | ao_vivo | 2026-11-03T23:14:50 | {"chars": 6696, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "cbb49b953537", "sha": "cbb49b953537a5cc"} |
| 1291 | 15 | inferencia | programa | ao_vivo | 2026-11-03T23:14:50 | diagnostico: 130,6 s |
| 1292 | 16 | declaracao | modelo | ao_vivo | 2026-11-03T23:14:50 | causa_raiz: `escala_ou_unidade_errada` |
| 1293 | 17 | declaracao | modelo | ao_vivo | 2026-11-03T23:14:50 | campo: `preco` |
| 1294 | 18 | declaracao | modelo | ao_vivo | 2026-11-03T23:14:50 | impacto: `O usuário vê preços com valores errados, como R$ 8990,00 em vez de R$ 89,90.` |
| 1295 | 19 | declaracao | modelo | ao_vivo | 2026-11-03T23:14:50 | fonte: `[escala_ou_unidade_errada]` |
| 1296 | 20 | declaracao | modelo | ao_vivo | 2026-11-03T23:14:50 | fonte_citada: `escala_ou_unidade_errada` |
| 1297 | 21 | verificacao | verificacao | ao_vivo | 2026-11-03T23:14:50 | quatro_linhas_presentes: confere |
| 1298 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T23:14:50 | rotulo_no_conjunto: confere |
| 1299 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T23:14:50 | fonte_existe_na_biblioteca: confere |
| 1300 | 24 | verificacao | verificacao | ao_vivo | 2026-11-03T23:14:50 | fonte_estava_no_contexto: confere |
| 1301 | 25 | verificacao | verificacao | ao_vivo | 2026-11-03T23:14:50 | campo_existe_no_caso: confere |
| 1302 | 26 | verificacao | verificacao | ao_vivo | 2026-11-03T23:14:50 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1303 | 27 | verificacao | verificacao | ao_vivo | 2026-11-03T23:14:50 | notas_nos_verbetes_citados: informativo |
| 1304 | 28 | verificacao | verificacao | ao_vivo | 2026-11-03T23:14:50 | impacto: nao_verificavel |
| 1305 | 29 | verificacao | verificacao | ao_vivo | 2026-11-03T23:14:50 | fonte_formato_valido: confere |
| 1306 | 30 | verificacao | verificacao | ao_vivo | 2026-11-03T23:14:50 | fonte_contem_termo_da_causa: confere |
| 1307 | 31 | decisao | programa | ao_vivo | 2026-11-03T23:14:50 | diagnostico: escolha escala_ou_unidade_errada; divergência não |
| 1310 | 32 | inferencia | programa | ao_vivo | 2026-11-03T23:17:04 | proposta: 194,6 s |
| 1311 | 33 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T23:17:04 | proposta 1: nota em [escala_ou_unidade_errada]: recusada: duplicada |
| 1313 | 34 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T23:17:04 | proposta 2: retificacao em [escala_ou_unidade_errada]: recusada: trecho_nao_encontrado |
| 1314 | 35 | decisao | programa | ao_vivo | 2026-11-03T23:17:04 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 1307, `diagnostico`: escolha `escala_ou_unidade_errada`; resultado rotulo_emitido; evidência: evento 1286 (sinal_em_codigo), evento 1285 (arvore_podada), evento 1281 (corpo_http), evento 1287 (verbete_entregue, entidade-produto), evento 1287 (verbete_entregue, contagem_inconsistente), evento 1287 (verbete_entregue, nulo_inesperado), evento 1287 (verbete_entregue, escala_ou_unidade_errada), evento 1291 (resposta), evento 1296 (verbete_citado, escala_ou_unidade_errada); divergência: não; falha: nenhuma; prov.used: entidade-produto, contagem_inconsistente, nulo_inesperado, escala_ou_unidade_errada (gen_ai: chat)
- evento 1314, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 1286 (sinal_em_codigo), evento 1285 (arvore_podada), evento 1281 (corpo_http), evento 1291 (resposta), evento 1310 (resposta), evento 1311 (verbete_entregue, escala_ou_unidade_errada), evento 1313 (verbete_entregue, escala_ou_unidade_errada); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: contagem_inconsistente, entidade-produto, escala_ou_unidade_errada, nulo_inesperado

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1275 a 1314 da trilha; hash dos eventos deste caso: `d96afa0b87659a03`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
