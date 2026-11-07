<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-27`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/tra-27@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `escala_ou_unidade_errada` · **CAMPO:** `preco` · selo de probabilidade: **medio** (p = 0,94)

**IMPACTO (declarado):** `O usuário vê um preço errado, R$ 8490,00 em vez de R$ 84.90.`

Justificativa (gerada por molde): O agente respondeu escala_ou_unidade_errada no campo preco porque o sinal preco: esperado 84.9 (referência em modo normal), recebido 8490.0 está presente na resposta HTTP e os verbetes escala_ou_unidade_errada, entidade-produto, contrato-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1316): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 197}, depois {"linhas": 42}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `61d61e21f90e4a4e`):

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
  dialog
    heading "Picanha Simples" level=4
    text "Corte nobre grelhado no ponto"

```

Poda de `corpo_http` (evento 1318): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 149}, depois {"chars": 228}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | 84.9 (referência em modo normal) | 8490.0 |

Trecho podado (hash `107e913a348113a9`):

```text
{"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 8490.0, "imagem": "picanha_sem.jpg", "destaque": false} (contra a referência em modo normal: preco 8490.0 em vez de 84.9)
```

Interceptação (evento 1309): `GET /api/produtos` status 200; corpo `61ba8740c5fc1841`, árvore `None`.

Interceptação (evento 1311): `GET /api/produtos/2` status 200; corpo `b490962308b15f74`, árvore `None`.

## 3. Contraste com a segunda causa

escala_ou_unidade_errada e não tipo_divergente: a escolha tem probabilidade 0,94 contra 0,00; verbete(s) na evidência: escala_ou_unidade_errada, entidade-produto, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| escala_ou_unidade_errada | 0,94 | sim |
| tipo_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[escala_ou_unidade_errada]`; verbetes citados: `escala_ou_unidade_errada`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `escala_ou_unidade_errada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `escala_ou_unidade_errada` | confere | contexto: `escala_ou_unidade_errada`, `entidade-produto`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `escala_ou_unidade_errada` | confere | verbetes: `escala_ou_unidade_errada`, `entidade-produto` |
| fonte_formato_valido | `[escala_ou_unidade_errada]` | confere | {"ids": ["escala_ou_unidade_errada"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `escala_ou_unidade_errada` | confere | {"termo": "escala_ou_unidade_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids tra-27 --k 3`

## 6. Árvore completa

<details><summary>34 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1301 | 1 | entrada | programa | ao_vivo | 2026-11-06T12:17:07 | caso tra-27 |
| 1302 | 2 | acao | programa | ao_vivo | 2026-11-06T12:17:08 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 129.1, "falhou": false} |
| 1303 | 3 | acao | programa | ao_vivo | 2026-11-06T12:17:08 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 8.6, "falhou": false} |
| 1304 | 4 | acao | programa | ao_vivo | 2026-11-06T12:17:08 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.6, "falhou": false} |
| 1305 | 5 | acao | programa | ao_vivo | 2026-11-06T12:17:08 | {"passo": 4, "acao": "clicar", "seletor": "#produtos-api-grid .saiba-mais[data-id='2']", "url": null, "tempo_ms": 41.0, "falhou": false} |
| 1306 | 6 | acao | programa | ao_vivo | 2026-11-06T12:17:08 | {"passo": 5, "acao": "esperar", "seletor": "#modalDetalhe", "url": null, "tempo_ms": 209.8, "falhou": false} |
| 1307 | 7 | acao | programa | ao_vivo | 2026-11-06T12:17:08 | {"passo": 6, "acao": "conferir", "seletor": "#modalDetalheTitulo", "url": null, "tempo_ms": 6.6, "falhou": false} |
| 1308 | 8 | acao | programa | ao_vivo | 2026-11-06T12:17:08 | {"passo": 7, "acao": "conferir", "seletor": "#modalDetalheCorpo", "url": null, "tempo_ms": 4.4, "falhou": false} |
| 1309 | 9 | interceptacao | programa | ao_vivo | 2026-11-06T12:17:08 | GET /api/produtos 200 |
| 1311 | 10 | interceptacao | programa | ao_vivo | 2026-11-06T12:17:08 | GET /api/produtos/2 200 |
| 1312 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T12:17:08 | conferencia_do_roteiro: confere |
| 1313 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T12:17:08 | conferencia_do_roteiro: confere |
| 1314 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T12:17:08 | conferencia_do_roteiro: confere |
| 1316 | 14 | poda | programa | ao_vivo | 2026-11-06T12:17:08 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1318 | 15 | poda | programa | ao_vivo | 2026-11-06T12:17:08 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1319 | 16 | candidatos | programa | ao_vivo | 2026-11-06T12:17:08 | 3 de 39 verbetes entregues |
| 1321 | 17 | prompt | programa | ao_vivo | 2026-11-06T12:17:08 | {"etapa": "diagnostico", "sha": "0ffad8f24dd91fc1", "prompt_sha256": "0ffad8f24dd9", "chars": 4219, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1323 | 18 | inferencia | programa | ao_vivo | 2026-11-06T12:17:08 | diagnostico: 64,9 s |
| 1324 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T12:17:08 | causa_raiz: `escala_ou_unidade_errada` |
| 1325 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T12:17:08 | campo: `preco` |
| 1326 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T12:17:08 | impacto: `O usuário vê um preço errado, R$ 8490,00 em vez de R$ 84.90.` |
| 1327 | 22 | declaracao | modelo | ao_vivo | 2026-11-06T12:17:08 | fonte: `[escala_ou_unidade_errada]` |
| 1328 | 23 | declaracao | modelo | ao_vivo | 2026-11-06T12:17:08 | fonte_citada: `escala_ou_unidade_errada` |
| 1329 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T12:17:08 | quatro_linhas_presentes: confere |
| 1330 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T12:17:08 | rotulo_no_conjunto: confere |
| 1331 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T12:17:08 | fonte_existe_na_biblioteca: confere |
| 1332 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T12:17:08 | fonte_estava_no_contexto: confere |
| 1333 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T12:17:08 | campo_existe_no_caso: confere |
| 1334 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T12:17:08 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1335 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T12:17:08 | notas_nos_verbetes_citados: informativo |
| 1336 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T12:17:08 | impacto: nao_verificavel |
| 1337 | 32 | verificacao | verificacao | ao_vivo | 2026-11-06T12:17:08 | fonte_formato_valido: confere |
| 1338 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T12:17:08 | fonte_contem_termo_da_causa: confere |
| 1339 | 34 | decisao | programa | ao_vivo | 2026-11-06T12:17:08 | diagnostico: escolha escala_ou_unidade_errada; divergência não |

</details>

Nós de decisão:

- evento 1339, `diagnostico`: escolha `escala_ou_unidade_errada`; resultado rotulo_emitido; evidência: evento 1318 (sinal_em_codigo), evento 1316 (arvore_podada), evento 1311 (corpo_http), evento 1319 (verbete_entregue, escala_ou_unidade_errada), evento 1319 (verbete_entregue, entidade-produto), evento 1319 (verbete_entregue, contrato-produto), evento 1323 (resposta), evento 1328 (verbete_citado, escala_ou_unidade_errada); divergência: não; falha: nenhuma; prov.used: escala_ou_unidade_errada, entidade-produto, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1301 a 1339 da trilha; hash dos eventos deste caso: `957616e152aa94b5`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
