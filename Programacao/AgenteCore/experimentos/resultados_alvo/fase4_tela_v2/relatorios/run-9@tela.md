<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-9`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/run-9@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tempo_de_resposta_excedido` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,98) · **CONFLITO**: nenhum verbete entregue trata da causa respondida tempo_de_resposta_excedido

**IMPACTO (declarado):** `O usuário experimentou uma resposta muito lenta, o que pode levar a uma experiência ruim e potencialmente fazer com que o sistema seja considerado lento ou ineficiente.`

Justificativa (gerada por molde): O agente respondeu tempo_de_resposta_excedido no campo tempo_ms porque o sinal tempo_ms: esperado 158 ms (referência em modo normal), recebido 28036 ms está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, contagem_inconsistente estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida tempo_de_resposta_excedido. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Poda de `arvore` (evento 1304): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 1305): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2068}, depois {"chars": 244}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tempo_ms | 158 ms (referência em modo normal) | 28036 ms |

Trecho podado (hash `59922d051a426b7b`):

```text
lista com 14 itens, igual à referência em modo normal; primeiro item: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 1300): `GET /api/produtos` status 200; corpo `4b1bdd056e7a8c3b`, árvore `None`.

## 3. Contraste com a segunda causa

tempo_de_resposta_excedido e não formato_de_data_divergente: a escolha tem probabilidade 0,98 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, contagem_inconsistente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tempo_de_resposta_excedido | 0,98 | sim |
| formato_de_data_divergente | 0,00 |  |
| contagem_inconsistente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| tipo_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [contagem_inconsistente]`; verbetes citados: `contrato-produto`, `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente` |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente` |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto], [contagem_inconsistente]` | confere | {"ids": ["contrato-produto", "contagem_inconsistente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tempo_de_resposta_excedido"} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | **não confere** | {"termo": "tempo_de_resposta_excedido"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids run-9 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1294 | 1 | entrada | programa | ao_vivo | 2026-11-01T14:57:19 | caso run-9 |
| 1295 | 2 | acao | programa | ao_vivo | 2026-11-01T14:57:47 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 116.2, "falhou": false} |
| 1296 | 3 | acao | programa | ao_vivo | 2026-11-01T14:57:47 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 28137.9, "falhou": false |
| 1297 | 4 | acao | programa | ao_vivo | 2026-11-01T14:57:47 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.3, "falhou": false} |
| 1298 | 5 | acao | programa | ao_vivo | 2026-11-01T14:57:47 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 8.7, "falhou": false} |
| 1299 | 6 | acao | programa | ao_vivo | 2026-11-01T14:57:47 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 8.1, "falhou": false} |
| 1300 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T14:57:47 | GET /api/produtos 200 |
| 1301 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T14:57:47 | conferencia_do_roteiro: confere |
| 1302 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T14:57:47 | conferencia_do_roteiro: confere |
| 1303 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T14:57:47 | conferencia_do_roteiro: confere |
| 1304 | 11 | poda | programa | ao_vivo | 2026-11-01T14:57:47 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1305 | 12 | poda | programa | ao_vivo | 2026-11-01T14:57:47 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1306 | 13 | candidatos | programa | ao_vivo | 2026-11-01T14:57:47 | 3 de 40 verbetes entregues |
| 1308 | 14 | prompt | programa | ao_vivo | 2026-11-01T14:57:47 | {"etapa": "diagnostico", "sha": "619220cc33d90d72", "prompt_sha256": "619220cc33d9", "chars": 5455, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1310 | 15 | inferencia | programa | ao_vivo | 2026-11-01T14:57:47 | diagnostico: 67,9 s |
| 1311 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T14:57:47 | causa_raiz: `tempo_de_resposta_excedido` |
| 1312 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T14:57:47 | campo: `nenhum` |
| 1313 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T14:57:47 | impacto: `O usuário experimentou uma resposta muito lenta, o que pode levar a uma experiência ruim e potencialmente fazer com que o sistema seja considerado lento ou ineficiente.` |
| 1314 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T14:57:47 | fonte: `[contrato-produto], [contagem_inconsistente]` |
| 1315 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T14:57:47 | fonte_citada: `contrato-produto` |
| 1316 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T14:57:47 | fonte_citada: `contagem_inconsistente` |
| 1317 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T14:57:47 | quatro_linhas_presentes: confere |
| 1318 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T14:57:47 | rotulo_no_conjunto: confere |
| 1319 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T14:57:47 | fonte_existe_na_biblioteca: confere |
| 1320 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T14:57:47 | fonte_existe_na_biblioteca: confere |
| 1321 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T14:57:47 | fonte_estava_no_contexto: confere |
| 1322 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T14:57:47 | fonte_estava_no_contexto: confere |
| 1323 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T14:57:47 | campo_existe_no_caso: nao_se_aplica |
| 1324 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T14:57:47 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 1325 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T14:57:47 | notas_nos_verbetes_citados: informativo |
| 1326 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T14:57:47 | impacto: nao_verificavel |
| 1327 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T14:57:47 | fonte_formato_valido: confere |
| 1328 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T14:57:47 | fonte_contem_termo_da_causa: nao_confere |
| 1329 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T14:57:47 | fonte_contem_termo_da_causa: nao_confere |
| 1330 | 35 | decisao | programa | ao_vivo | 2026-11-01T14:57:47 | diagnostico: escolha tempo_de_resposta_excedido; divergência sim |

</details>

Nós de decisão:

- evento 1330, `diagnostico`: escolha `tempo_de_resposta_excedido`; resultado rotulo_emitido; evidência: evento 1305 (sinal_em_codigo), evento 1304 (arvore_podada), evento 1300 (corpo_http), evento 1306 (verbete_entregue, entidade-produto), evento 1306 (verbete_entregue, contrato-produto), evento 1306 (verbete_entregue, contagem_inconsistente), evento 1310 (resposta), evento 1315 (verbete_citado, contrato-produto), evento 1316 (verbete_citado, contagem_inconsistente); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, contagem_inconsistente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1294 a 1330 da trilha; hash dos eventos deste caso: `de1cde8525329c1d`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
