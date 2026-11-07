<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-26`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/tra-26@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `nome, resumo, preco, imagem, destaque, tipo` · selo de probabilidade: **baixo** (p = 0,70) · **CONFLITO**: o campo apontado (nome, resumo, preco, imagem, destaque, tipo) não aparece no caso

**IMPACTO (declarado):** `O usuário vê nomes, resumos, preços, imagens e destaque incorretos, o que pode levar a escolhas erradas na compra e confusão sobre os produtos.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo nome, resumo, preco, imagem, destaque, tipo porque o sinal nome: esperado "Picanha Simples" (referência em modo normal), recebido "Picanha ao Alho" em 13 itens está presente na resposta HTTP e os verbetes chave_de_juncao_errada, campo_renomeado, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,12. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): o campo apontado (nome, resumo, preco, imagem, destaque, tipo) não aparece no caso. Este nó está marcado com a falha campo_errado (origem: modelo). O agente não está seguro desta causa (probabilidade 0,70); trate como hipótese e confira o campo nome, resumo, preco, imagem, destaque, tipo antes de agir.

## 2. Evidência

Poda de `arvore` (evento 1245): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 1 linha(s) da referência | 1 linha(s) novas |

Trecho podado (hash `3f3965b2336faec3`):

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
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "R$ 69,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="4"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 1247): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2068}, depois {"chars": 414}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| nome | "Picanha Simples" (referência em modo normal) | "Picanha ao Alho" em 13 itens |
| resumo | "Corte nobre grelhado no ponto" (referência em modo normal) | "Picanha grelhada com alho laminado na brasa" em 12 itens |
| preco | 84.9 (referência em modo normal) | 89.9 em 12 itens |
| imagem | "picanha_sem.jpg" (referência em modo normal) | "picanha_alho.jpg" em 12 itens |
| destaque | false (referência em modo normal) | true em 9 itens |
| tipo | "Bebidas" (referência em modo normal) | "Carnes" em 2 itens |

Trecho podado (hash `b42e71b4fec9bba4`):

```text
lista com 14 itens (referência em modo normal: 14); nome diferente em 13 itens; resumo diferente em 12 itens; preco diferente em 12 itens; imagem diferente em 12 itens; destaque diferente em 9 itens; tipo diferente em 2 itens; por exemplo: {"id": 2, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 1240): `GET /api/produtos` status 200; corpo `ca41b82db0fe97b6`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não valor_fora_do_dominio: a escolha tem probabilidade 0,70 contra 0,12; verbete(s) na evidência: chave_de_juncao_errada, campo_renomeado, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,70 | sim |
| valor_fora_do_dominio | 0,12 |  |
| campo_ausente | 0,09 |  |
| campo_renomeado | 0,09 |  |
| chave_de_juncao_errada | 0,05 |  |
| dado_desatualizado | 0,03 |  |
| resposta_truncada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| registro_duplicado | 0,00 |  |
| nulo_inesperado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tipo_divergente], [campo_renomeado]`; verbetes citados: `tipo_divergente`, `campo_renomeado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `chave_de_juncao_errada`, `campo_renomeado`, `tipo_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | confere | contexto: `chave_de_juncao_errada`, `campo_renomeado`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `tipo_divergente` |
| fonte_formato_valido | `[tipo_divergente], [campo_renomeado]` | confere | {"ids": ["tipo_divergente", "campo_renomeado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `campo_renomeado` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome, resumo, preco, imagem, destaque, tipo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids tra-26 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1233 | 1 | entrada | programa | ao_vivo | 2026-11-06T12:14:23 | caso tra-26 |
| 1234 | 2 | acao | programa | ao_vivo | 2026-11-06T12:14:23 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 106.8, "falhou": false} |
| 1235 | 3 | acao | programa | ao_vivo | 2026-11-06T12:14:23 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 6.7, "falhou": false} |
| 1236 | 4 | acao | programa | ao_vivo | 2026-11-06T12:14:23 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.1, "falhou": false} |
| 1237 | 5 | acao | programa | ao_vivo | 2026-11-06T12:14:23 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 4.4, "falhou": false} |
| 1238 | 6 | acao | programa | ao_vivo | 2026-11-06T12:14:23 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.1, "falhou": false} |
| 1240 | 7 | interceptacao | programa | ao_vivo | 2026-11-06T12:14:23 | GET /api/produtos 200 |
| 1241 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T12:14:23 | conferencia_do_roteiro: confere |
| 1242 | 9 | verificacao | verificacao | ao_vivo | 2026-11-06T12:14:23 | conferencia_do_roteiro: confere |
| 1243 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T12:14:23 | conferencia_do_roteiro: confere |
| 1245 | 11 | poda | programa | ao_vivo | 2026-11-06T12:14:23 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1247 | 12 | poda | programa | ao_vivo | 2026-11-06T12:14:23 | corpo_http: 6 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1248 | 13 | candidatos | programa | ao_vivo | 2026-11-06T12:14:23 | 3 de 39 verbetes entregues |
| 1250 | 14 | prompt | programa | ao_vivo | 2026-11-06T12:14:23 | {"etapa": "diagnostico", "sha": "d1403841eb045205", "prompt_sha256": "d1403841eb04", "chars": 5268, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1252 | 15 | inferencia | programa | ao_vivo | 2026-11-06T12:14:23 | diagnostico: 91,3 s |
| 1253 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T12:14:23 | causa_raiz: `tipo_divergente` |
| 1254 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T12:14:23 | campo: `nome, resumo, preco, imagem, destaque, tipo` |
| 1255 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T12:14:23 | impacto: `O usuário vê nomes, resumos, preços, imagens e destaque incorretos, o que pode levar a escolhas erradas na compra e confusão sobre os produtos.` |
| 1256 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T12:14:23 | fonte: `[tipo_divergente], [campo_renomeado]` |
| 1257 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T12:14:23 | fonte_citada: `tipo_divergente` |
| 1258 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T12:14:23 | fonte_citada: `campo_renomeado` |
| 1259 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T12:14:23 | quatro_linhas_presentes: confere |
| 1260 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T12:14:23 | rotulo_no_conjunto: confere |
| 1261 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T12:14:23 | fonte_existe_na_biblioteca: confere |
| 1262 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T12:14:23 | fonte_existe_na_biblioteca: confere |
| 1263 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T12:14:23 | fonte_estava_no_contexto: confere |
| 1264 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T12:14:23 | fonte_estava_no_contexto: confere |
| 1265 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T12:14:23 | campo_existe_no_caso: nao_confere |
| 1266 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T12:14:23 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1267 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T12:14:23 | notas_nos_verbetes_citados: informativo |
| 1268 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T12:14:23 | impacto: nao_verificavel |
| 1269 | 32 | verificacao | verificacao | ao_vivo | 2026-11-06T12:14:23 | fonte_formato_valido: confere |
| 1270 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T12:14:23 | fonte_contem_termo_da_causa: confere |
| 1271 | 34 | verificacao | verificacao | ao_vivo | 2026-11-06T12:14:23 | fonte_contem_termo_da_causa: nao_confere |
| 1272 | 35 | decisao | programa | ao_vivo | 2026-11-06T12:14:23 | diagnostico: escolha tipo_divergente; divergência sim |

</details>

Nós de decisão:

- evento 1272, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1247 (sinal_em_codigo), evento 1245 (arvore_podada), evento 1240 (corpo_http), evento 1248 (verbete_entregue, chave_de_juncao_errada), evento 1248 (verbete_entregue, campo_renomeado), evento 1248 (verbete_entregue, tipo_divergente), evento 1252 (resposta), evento 1257 (verbete_citado, tipo_divergente), evento 1258 (verbete_citado, campo_renomeado); divergência: sim; falha: campo_errado; prov.used: chave_de_juncao_errada, campo_renomeado, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1233 a 1272 da trilha; hash dos eventos deste caso: `64d8d7f7078238c9`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
