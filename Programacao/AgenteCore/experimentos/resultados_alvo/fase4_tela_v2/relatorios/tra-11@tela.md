<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-11`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/tra-11@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `contagem_inconsistente` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê uma lista com um item a menos do que o esperado, o que pode causar confusão na exibição dos produtos.`

Justificativa (gerada por molde): O agente respondeu contagem_inconsistente no campo itens porque o sinal itens: esperado 14 itens (referência em modo normal), recebido falta o id 14 ("Abacaxi na Brasa") está presente na resposta HTTP e os verbetes contagem_inconsistente, entidade-produto, contrato-produto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1247): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 183}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 1 linha(s) da referência | 1 linha(s) novas |

Trecho podado (hash `7c54fbd0508aace9`):

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
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 1248): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 1928}, depois {"chars": 277}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| itens | 14 itens (referência em modo normal) | falta o id 14 ("Abacaxi na Brasa") |

Trecho podado (hash `9675592a8385ee52`):

```text
lista com 13 itens (referência em modo normal: 14); falta o id 14 ("Abacaxi na Brasa"); primeiro item: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 1245): `GET /api/produtos` status 200; corpo `4f6d409f5a92ce2d`, árvore `None`.

## 3. Contraste com a segunda causa

contagem_inconsistente e não resposta_truncada: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: contagem_inconsistente, entidade-produto, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| contagem_inconsistente | 0,99 | sim |
| resposta_truncada | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contagem_inconsistente]`; verbetes citados: `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `contagem_inconsistente`, `entidade-produto`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | confere | verbetes: `contagem_inconsistente` |
| fonte_formato_valido | `[contagem_inconsistente]` | confere | {"ids": ["contagem_inconsistente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | confere | {"termo": "contagem_inconsistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids tra-11 --k 3`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1241 | 1 | entrada | programa | ao_vivo | 2026-11-01T14:55:21 | caso tra-11 |
| 1242 | 2 | acao | programa | ao_vivo | 2026-11-01T14:55:21 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 107.6, "falhou": false} |
| 1243 | 3 | acao | programa | ao_vivo | 2026-11-01T14:55:21 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 15.1, "falhou": false} |
| 1244 | 4 | acao | programa | ao_vivo | 2026-11-01T14:55:21 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 3.8, "falhou": true} |
| 1245 | 5 | interceptacao | programa | ao_vivo | 2026-11-01T14:55:21 | GET /api/produtos 200 |
| 1246 | 6 | verificacao | verificacao | ao_vivo | 2026-11-01T14:55:21 | conferencia_do_roteiro: nao_confere |
| 1247 | 7 | poda | programa | ao_vivo | 2026-11-01T14:55:21 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1248 | 8 | poda | programa | ao_vivo | 2026-11-01T14:55:21 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1249 | 9 | candidatos | programa | ao_vivo | 2026-11-01T14:55:21 | 3 de 40 verbetes entregues |
| 1251 | 10 | prompt | programa | ao_vivo | 2026-11-01T14:55:21 | {"etapa": "diagnostico", "sha": "f8ebacb93bd8a42a", "prompt_sha256": "f8ebacb93bd8", "chars": 5711, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1253 | 11 | inferencia | programa | ao_vivo | 2026-11-01T14:55:21 | diagnostico: 75,3 s |
| 1254 | 12 | declaracao | modelo | ao_vivo | 2026-11-01T14:55:21 | causa_raiz: `contagem_inconsistente` |
| 1255 | 13 | declaracao | modelo | ao_vivo | 2026-11-01T14:55:21 | campo: `nenhum` |
| 1256 | 14 | declaracao | modelo | ao_vivo | 2026-11-01T14:55:21 | impacto: `O usuário vê uma lista com um item a menos do que o esperado, o que pode causar confusão na exibição dos produtos.` |
| 1257 | 15 | declaracao | modelo | ao_vivo | 2026-11-01T14:55:21 | fonte: `[contagem_inconsistente]` |
| 1258 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T14:55:21 | fonte_citada: `contagem_inconsistente` |
| 1259 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T14:55:21 | quatro_linhas_presentes: confere |
| 1260 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T14:55:21 | rotulo_no_conjunto: confere |
| 1261 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T14:55:21 | fonte_existe_na_biblioteca: confere |
| 1262 | 20 | verificacao | verificacao | ao_vivo | 2026-11-01T14:55:21 | fonte_estava_no_contexto: confere |
| 1263 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T14:55:21 | campo_existe_no_caso: nao_se_aplica |
| 1264 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T14:55:21 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1265 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T14:55:21 | notas_nos_verbetes_citados: informativo |
| 1266 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T14:55:21 | impacto: nao_verificavel |
| 1267 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T14:55:21 | fonte_formato_valido: confere |
| 1268 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T14:55:21 | fonte_contem_termo_da_causa: confere |
| 1269 | 27 | decisao | programa | ao_vivo | 2026-11-01T14:55:21 | diagnostico: escolha contagem_inconsistente; divergência não |

</details>

Nós de decisão:

- evento 1269, `diagnostico`: escolha `contagem_inconsistente`; resultado rotulo_emitido; evidência: evento 1248 (sinal_em_codigo), evento 1247 (arvore_podada), evento 1245 (corpo_http), evento 1249 (verbete_entregue, contagem_inconsistente), evento 1249 (verbete_entregue, entidade-produto), evento 1249 (verbete_entregue, contrato-produto), evento 1253 (resposta), evento 1258 (verbete_citado, contagem_inconsistente); divergência: não; falha: nenhuma; prov.used: contagem_inconsistente, entidade-produto, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1241 a 1269 da trilha; hash dos eventos deste caso: `ad3c87b638219977`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
