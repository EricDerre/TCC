<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `contrato-field_renamed#4`: o que o agente fez, declarou e conferiu

Trilha `fase5_agente/qwen2.5_7b/contrato-field_renamed#4`; modelo `qwen2.5:7b`, Ollama 0.40.16, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_renomeado` · **CAMPO:** `preco` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê um preço incorreto, exibido como "undefined" em vez do valor esperado.`

Justificativa (gerada por molde): O agente respondeu campo_renomeado no campo preco porque o sinal preco: esperado preco, recebido preco_v2 está presente na resposta HTTP e os verbetes campo_renomeado, campo_ausente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1251): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `714120f74ce44bb6`):

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
      button "undefined" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "undefined" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "undefined" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 1252): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2110}, depois {"chars": 18}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | preco | preco_v2 |

Trecho podado (hash `3ca91df248763374`):

```text
{"preco_v2": 89.9}
```

Interceptação (evento 1248): `GET /api/produtos` status 200; corpo `4f7726df03992678`, árvore `None`.

## 3. Contraste com a segunda causa

campo_renomeado e não tipo_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: campo_renomeado, campo_ausente, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_renomeado | 1,00 | sim |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_renomeado]`; verbetes citados: `campo_renomeado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | confere | contexto: `campo_renomeado`, `campo_ausente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `campo_renomeado`, `campo_ausente`, `contrato-produto` |
| fonte_formato_valido | `[campo_renomeado]` | confere | {"ids": ["campo_renomeado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_renomeado` | confere | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase5_agente_reexec --repeticoes 1`

## 6. Árvore completa

<details><summary>29 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1243 | 1 | entrada | programa | ao_vivo | 2026-11-18T19:09:01 | caso contrato-field_renamed#4 |
| 1244 | 2 | acao | programa | ao_vivo | 2026-11-18T19:09:02 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 143.9, "falhou": false} |
| 1245 | 3 | acao | programa | ao_vivo | 2026-11-18T19:09:02 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 6.4, "falhou": false} |
| 1246 | 4 | acao | programa | ao_vivo | 2026-11-18T19:09:02 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.5, "falhou": false} |
| 1247 | 5 | acao | programa | ao_vivo | 2026-11-18T19:09:02 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 4.2, "falhou": true} |
| 1248 | 6 | interceptacao | programa | ao_vivo | 2026-11-18T19:09:02 | GET /api/produtos 200 |
| 1249 | 7 | verificacao | verificacao | ao_vivo | 2026-11-18T19:09:02 | conferencia_do_roteiro: confere |
| 1250 | 8 | verificacao | verificacao | ao_vivo | 2026-11-18T19:09:02 | conferencia_do_roteiro: nao_confere |
| 1251 | 9 | poda | programa | ao_vivo | 2026-11-18T19:09:02 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1252 | 10 | poda | programa | ao_vivo | 2026-11-18T19:09:02 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1253 | 11 | candidatos | programa | ao_vivo | 2026-11-18T19:09:02 | 3 de 39 verbetes entregues |
| 1254 | 12 | prompt | programa | ao_vivo | 2026-11-18T19:09:02 | {"etapa": "diagnostico", "sha": "d938cc6ebd4b79c4", "prompt_sha256": "d938cc6ebd4b", "chars": 3650, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1255 | 13 | inferencia | programa | ao_vivo | 2026-11-18T19:09:02 | diagnostico: 14,3 s |
| 1256 | 14 | declaracao | modelo | ao_vivo | 2026-11-18T19:09:02 | causa_raiz: `campo_renomeado` |
| 1257 | 15 | declaracao | modelo | ao_vivo | 2026-11-18T19:09:02 | campo: `preco` |
| 1258 | 16 | declaracao | modelo | ao_vivo | 2026-11-18T19:09:02 | impacto: `O usuário vê um preço incorreto, exibido como "undefined" em vez do valor esperado.` |
| 1259 | 17 | declaracao | modelo | ao_vivo | 2026-11-18T19:09:02 | fonte: `[campo_renomeado]` |
| 1260 | 18 | declaracao | modelo | ao_vivo | 2026-11-18T19:09:02 | fonte_citada: `campo_renomeado` |
| 1261 | 19 | verificacao | verificacao | ao_vivo | 2026-11-18T19:09:02 | quatro_linhas_presentes: confere |
| 1262 | 20 | verificacao | verificacao | ao_vivo | 2026-11-18T19:09:02 | rotulo_no_conjunto: confere |
| 1263 | 21 | verificacao | verificacao | ao_vivo | 2026-11-18T19:09:02 | fonte_existe_na_biblioteca: confere |
| 1264 | 22 | verificacao | verificacao | ao_vivo | 2026-11-18T19:09:02 | fonte_estava_no_contexto: confere |
| 1265 | 23 | verificacao | verificacao | ao_vivo | 2026-11-18T19:09:02 | campo_existe_no_caso: confere |
| 1266 | 24 | verificacao | verificacao | ao_vivo | 2026-11-18T19:09:02 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1267 | 25 | verificacao | verificacao | ao_vivo | 2026-11-18T19:09:02 | notas_nos_verbetes_citados: informativo |
| 1268 | 26 | verificacao | verificacao | ao_vivo | 2026-11-18T19:09:02 | impacto: nao_verificavel |
| 1269 | 27 | verificacao | verificacao | ao_vivo | 2026-11-18T19:09:02 | fonte_formato_valido: confere |
| 1270 | 28 | verificacao | verificacao | ao_vivo | 2026-11-18T19:09:02 | fonte_contem_termo_da_causa: confere |
| 1271 | 29 | decisao | programa | ao_vivo | 2026-11-18T19:09:02 | diagnostico: escolha campo_renomeado; divergência não |

</details>

Nós de decisão:

- evento 1271, `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido; evidência: evento 1252 (sinal_em_codigo), evento 1251 (arvore_podada), evento 1248 (corpo_http), evento 1253 (verbete_entregue, campo_renomeado), evento 1253 (verbete_entregue, campo_ausente), evento 1253 (verbete_entregue, contrato-produto), evento 1255 (resposta), evento 1260 (verbete_citado, campo_renomeado); divergência: não; falha: nenhuma; prov.used: campo_renomeado, campo_ausente, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1243 a 1271 da trilha; hash dos eventos deste caso: `6647c18db5794b4d`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
