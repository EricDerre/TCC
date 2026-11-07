<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-9`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v4/qwen2.5_7b/run-9@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tempo_de_resposta_excedido` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário experimentou uma resposta muito lenta, o que pode levar a uma experiência ruim e potencialmente fazer com que o cliente desista da requisição.`

Justificativa (gerada por molde): O agente respondeu tempo_de_resposta_excedido no campo tempo_ms porque o sinal tempo_ms: esperado 67 ms (referência em modo normal), recebido 28023 ms está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, tempo_de_resposta_excedido estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1253): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 1254): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2068}, depois {"chars": 244}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tempo_ms | 67 ms (referência em modo normal) | 28023 ms |

Trecho podado (hash `59922d051a426b7b`):

```text
lista com 14 itens, igual à referência em modo normal; primeiro item: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 1249): `GET /api/produtos` status 200; corpo `4b1bdd056e7a8c3b`, árvore `None`.

## 3. Contraste com a segunda causa

tempo_de_resposta_excedido e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, tempo_de_resposta_excedido

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tempo_de_resposta_excedido | 1,00 | sim |
| colecao_no_lugar_de_objeto | 0,00 |  |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tempo_de_resposta_excedido]`; verbetes citados: `tempo_de_resposta_excedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tempo_de_resposta_excedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tempo_de_resposta_excedido` | confere | contexto: `entidade-produto`, `contrato-produto`, `tempo_de_resposta_excedido` |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | confere | verbetes: `tempo_de_resposta_excedido` |
| fonte_formato_valido | `[tempo_de_resposta_excedido]` | confere | {"ids": ["tempo_de_resposta_excedido"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tempo_de_resposta_excedido` | confere | {"termo": "tempo_de_resposta_excedido"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids run-9 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1243 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:40:46 | caso run-9 |
| 1244 | 2 | acao | programa | ao_vivo | 2026-11-06T10:41:15 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 91.8, "falhou": false} |
| 1245 | 3 | acao | programa | ao_vivo | 2026-11-06T10:41:15 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 28470.3, "falhou": false |
| 1246 | 4 | acao | programa | ao_vivo | 2026-11-06T10:41:15 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.5, "falhou": false} |
| 1247 | 5 | acao | programa | ao_vivo | 2026-11-06T10:41:15 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 3.7, "falhou": false} |
| 1248 | 6 | acao | programa | ao_vivo | 2026-11-06T10:41:15 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.4, "falhou": false} |
| 1249 | 7 | interceptacao | programa | ao_vivo | 2026-11-06T10:41:15 | GET /api/produtos 200 |
| 1250 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T10:41:15 | conferencia_do_roteiro: confere |
| 1251 | 9 | verificacao | verificacao | ao_vivo | 2026-11-06T10:41:15 | conferencia_do_roteiro: confere |
| 1252 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T10:41:15 | conferencia_do_roteiro: confere |
| 1253 | 11 | poda | programa | ao_vivo | 2026-11-06T10:41:15 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1254 | 12 | poda | programa | ao_vivo | 2026-11-06T10:41:15 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1255 | 13 | candidatos | programa | ao_vivo | 2026-11-06T10:41:15 | 3 de 39 verbetes entregues |
| 1256 | 14 | prompt | programa | ao_vivo | 2026-11-06T10:41:15 | {"etapa": "diagnostico", "sha": "e1f161e94e1c4411", "prompt_sha256": "e1f161e94e1c", "chars": 3580, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1257 | 15 | inferencia | programa | ao_vivo | 2026-11-06T10:41:15 | diagnostico: 55,7 s |
| 1258 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T10:41:15 | causa_raiz: `tempo_de_resposta_excedido` |
| 1259 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T10:41:15 | campo: `nenhum` |
| 1260 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T10:41:15 | impacto: `O usuário experimentou uma resposta muito lenta, o que pode levar a uma experiência ruim e potencialmente fazer com que o cliente desista da requisição.` |
| 1261 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T10:41:15 | fonte: `[tempo_de_resposta_excedido]` |
| 1262 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T10:41:15 | fonte_citada: `tempo_de_resposta_excedido` |
| 1263 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T10:41:15 | quatro_linhas_presentes: confere |
| 1264 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T10:41:15 | rotulo_no_conjunto: confere |
| 1265 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T10:41:15 | fonte_existe_na_biblioteca: confere |
| 1266 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T10:41:15 | fonte_estava_no_contexto: confere |
| 1267 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T10:41:15 | campo_existe_no_caso: nao_se_aplica |
| 1268 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T10:41:15 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1269 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T10:41:15 | notas_nos_verbetes_citados: informativo |
| 1270 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T10:41:15 | impacto: nao_verificavel |
| 1271 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T10:41:15 | fonte_formato_valido: confere |
| 1272 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T10:41:15 | fonte_contem_termo_da_causa: confere |
| 1273 | 31 | decisao | programa | ao_vivo | 2026-11-06T10:41:15 | diagnostico: escolha tempo_de_resposta_excedido; divergência não |

</details>

Nós de decisão:

- evento 1273, `diagnostico`: escolha `tempo_de_resposta_excedido`; resultado rotulo_emitido; evidência: evento 1254 (sinal_em_codigo), evento 1253 (arvore_podada), evento 1249 (corpo_http), evento 1255 (verbete_entregue, entidade-produto), evento 1255 (verbete_entregue, contrato-produto), evento 1255 (verbete_entregue, tempo_de_resposta_excedido), evento 1257 (resposta), evento 1262 (verbete_citado, tempo_de_resposta_excedido); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, tempo_de_resposta_excedido (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1243 a 1273 da trilha; hash dos eventos deste caso: `fa7bef41e7f038a5`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
