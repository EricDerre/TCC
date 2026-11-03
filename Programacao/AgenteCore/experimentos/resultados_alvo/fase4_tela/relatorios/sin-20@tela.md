<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-20`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/sin-20@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `id` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário não recebeu o identificador do produto, o que impede a localização específica de cada item.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo id porque o sinal id: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes campo_ausente, contrato-produto, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1545): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `c0722848066abd48`):

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
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="undefined"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="undefined"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "R$ 69,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="undefined"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 1547): regras diff_contra_contrato; antes {"chars": 1965}, depois {"chars": 19}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | inteiro |  |

Trecho podado (hash `8b4569439604f9f8`):

```text
{"id": "(ausente)"}
```

Interceptação (evento 1540): `GET /api/produtos` status 200; corpo `1c18c47d6e32ff35`, árvore `None`.

## 3. Contraste com a segunda causa

campo_ausente e não corpo_nao_e_json: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: campo_ausente, contrato-produto, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 1,00 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| tipo_divergente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente] [contrato-produto]`; verbetes citados: `campo_ausente`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `campo_ausente`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `campo_ausente`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `campo_ausente`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| fonte_formato_valido | `[campo_ausente] [contrato-produto]` | confere | {"ids": ["campo_ausente", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_ausente` | confere | {"termo": "campo_ausente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids sin-20 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1533 | 1 | entrada | programa | ao_vivo | 2026-11-01T12:09:06 | caso sin-20 |
| 1534 | 2 | acao | programa | ao_vivo | 2026-11-01T12:09:06 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 110.5, "falhou": false} |
| 1535 | 3 | acao | programa | ao_vivo | 2026-11-01T12:09:06 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 23.0, "falhou": false} |
| 1536 | 4 | acao | programa | ao_vivo | 2026-11-01T12:09:06 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 5.0, "falhou": false} |
| 1537 | 5 | acao | programa | ao_vivo | 2026-11-01T12:09:06 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 5.4, "falhou": false} |
| 1538 | 6 | acao | programa | ao_vivo | 2026-11-01T12:09:06 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 7.1, "falhou": false} |
| 1540 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T12:09:06 | GET /api/produtos 200 |
| 1541 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T12:09:06 | conferencia_do_roteiro: confere |
| 1542 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T12:09:06 | conferencia_do_roteiro: confere |
| 1543 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T12:09:06 | conferencia_do_roteiro: confere |
| 1545 | 11 | poda | programa | ao_vivo | 2026-11-01T12:09:06 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1547 | 12 | poda | programa | ao_vivo | 2026-11-01T12:09:06 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1548 | 13 | candidatos | programa | ao_vivo | 2026-11-01T12:09:06 | 3 de 40 verbetes entregues |
| 1550 | 14 | prompt | programa | ao_vivo | 2026-11-01T12:09:06 | {"etapa": "diagnostico", "sha": "5ee26b4c046ba568", "prompt_sha256": "5ee26b4c046b", "chars": 5293, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1552 | 15 | inferencia | programa | ao_vivo | 2026-11-01T12:09:06 | diagnostico: 91,8 s |
| 1553 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T12:09:06 | causa_raiz: `campo_ausente` |
| 1554 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T12:09:06 | campo: `id` |
| 1555 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T12:09:06 | impacto: `O usuário não recebeu o identificador do produto, o que impede a localização específica de cada item.` |
| 1556 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T12:09:06 | fonte: `[campo_ausente] [contrato-produto]` |
| 1557 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T12:09:06 | fonte_citada: `campo_ausente` |
| 1558 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T12:09:06 | fonte_citada: `contrato-produto` |
| 1559 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T12:09:06 | quatro_linhas_presentes: confere |
| 1560 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T12:09:06 | rotulo_no_conjunto: confere |
| 1561 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T12:09:06 | fonte_existe_na_biblioteca: confere |
| 1562 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T12:09:06 | fonte_existe_na_biblioteca: confere |
| 1563 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T12:09:06 | fonte_estava_no_contexto: confere |
| 1564 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T12:09:06 | fonte_estava_no_contexto: confere |
| 1565 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T12:09:06 | campo_existe_no_caso: confere |
| 1566 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T12:09:06 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1567 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T12:09:06 | notas_nos_verbetes_citados: informativo |
| 1568 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T12:09:06 | impacto: nao_verificavel |
| 1569 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T12:09:06 | fonte_formato_valido: confere |
| 1570 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T12:09:06 | fonte_contem_termo_da_causa: confere |
| 1571 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T12:09:06 | fonte_contem_termo_da_causa: nao_confere |
| 1572 | 35 | decisao | programa | ao_vivo | 2026-11-01T12:09:06 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 1572, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 1547 (sinal_em_codigo), evento 1545 (arvore_podada), evento 1540 (corpo_http), evento 1548 (verbete_entregue, campo_ausente), evento 1548 (verbete_entregue, contrato-produto), evento 1548 (verbete_entregue, colecao_no_lugar_de_objeto), evento 1552 (resposta), evento 1557 (verbete_citado, campo_ausente), evento 1558 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: campo_ausente, contrato-produto, colecao_no_lugar_de_objeto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1533 a 1572 da trilha; hash dos eventos deste caso: `3fd5320221bc5851`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
