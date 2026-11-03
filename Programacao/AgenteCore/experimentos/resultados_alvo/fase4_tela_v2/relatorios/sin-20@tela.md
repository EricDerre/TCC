<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-20`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/sin-20@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `id` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário não recebeu o identificador do produto, o que impede a identificação correta dos itens.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo id porque o sinal id: esperado inteiro, recebido None está presente na resposta HTTP e os verbetes campo_ausente, contrato-produto, campo_renomeado estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1553): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 1555): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 1965}, depois {"chars": 19}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | inteiro |  |

Trecho podado (hash `8b4569439604f9f8`):

```text
{"id": "(ausente)"}
```

Interceptação (evento 1548): `GET /api/produtos` status 200; corpo `1c18c47d6e32ff35`, árvore `None`.

## 3. Contraste com a segunda causa

campo_ausente e não corpo_nao_e_json: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: campo_ausente, contrato-produto, campo_renomeado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 1,00 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente] [contrato-produto]`; verbetes citados: `campo_ausente`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `campo_ausente`, `contrato-produto`, `campo_renomeado` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `campo_ausente`, `contrato-produto`, `campo_renomeado` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `campo_ausente`, `contrato-produto`, `campo_renomeado` |
| fonte_formato_valido | `[campo_ausente] [contrato-produto]` | confere | {"ids": ["campo_ausente", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_ausente` | confere | {"termo": "campo_ausente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids sin-20 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1541 | 1 | entrada | programa | ao_vivo | 2026-11-01T15:07:57 | caso sin-20 |
| 1542 | 2 | acao | programa | ao_vivo | 2026-11-01T15:07:57 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 210.6, "falhou": false} |
| 1543 | 3 | acao | programa | ao_vivo | 2026-11-01T15:07:57 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 8.9, "falhou": false} |
| 1544 | 4 | acao | programa | ao_vivo | 2026-11-01T15:07:57 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 3.4, "falhou": false} |
| 1545 | 5 | acao | programa | ao_vivo | 2026-11-01T15:07:57 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 6.1, "falhou": false} |
| 1546 | 6 | acao | programa | ao_vivo | 2026-11-01T15:07:57 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.2, "falhou": false} |
| 1548 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T15:07:57 | GET /api/produtos 200 |
| 1549 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T15:07:57 | conferencia_do_roteiro: confere |
| 1550 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T15:07:57 | conferencia_do_roteiro: confere |
| 1551 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T15:07:57 | conferencia_do_roteiro: confere |
| 1553 | 11 | poda | programa | ao_vivo | 2026-11-01T15:07:57 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1555 | 12 | poda | programa | ao_vivo | 2026-11-01T15:07:57 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1556 | 13 | candidatos | programa | ao_vivo | 2026-11-01T15:07:57 | 3 de 40 verbetes entregues |
| 1558 | 14 | prompt | programa | ao_vivo | 2026-11-01T15:07:57 | {"etapa": "diagnostico", "sha": "12be65989dc10b90", "prompt_sha256": "12be65989dc1", "chars": 5326, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1560 | 15 | inferencia | programa | ao_vivo | 2026-11-01T15:07:57 | diagnostico: 60,6 s |
| 1561 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T15:07:57 | causa_raiz: `campo_ausente` |
| 1562 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T15:07:57 | campo: `id` |
| 1563 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T15:07:57 | impacto: `O usuário não recebeu o identificador do produto, o que impede a identificação correta dos itens.` |
| 1564 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T15:07:57 | fonte: `[campo_ausente] [contrato-produto]` |
| 1565 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T15:07:57 | fonte_citada: `campo_ausente` |
| 1566 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T15:07:57 | fonte_citada: `contrato-produto` |
| 1567 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T15:07:57 | quatro_linhas_presentes: confere |
| 1568 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T15:07:57 | rotulo_no_conjunto: confere |
| 1569 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T15:07:57 | fonte_existe_na_biblioteca: confere |
| 1570 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T15:07:57 | fonte_existe_na_biblioteca: confere |
| 1571 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T15:07:57 | fonte_estava_no_contexto: confere |
| 1572 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T15:07:57 | fonte_estava_no_contexto: confere |
| 1573 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T15:07:57 | campo_existe_no_caso: confere |
| 1574 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T15:07:57 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1575 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T15:07:57 | notas_nos_verbetes_citados: informativo |
| 1576 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T15:07:57 | impacto: nao_verificavel |
| 1577 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T15:07:57 | fonte_formato_valido: confere |
| 1578 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T15:07:57 | fonte_contem_termo_da_causa: confere |
| 1579 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T15:07:57 | fonte_contem_termo_da_causa: nao_confere |
| 1580 | 35 | decisao | programa | ao_vivo | 2026-11-01T15:07:57 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 1580, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 1555 (sinal_em_codigo), evento 1553 (arvore_podada), evento 1548 (corpo_http), evento 1556 (verbete_entregue, campo_ausente), evento 1556 (verbete_entregue, contrato-produto), evento 1556 (verbete_entregue, campo_renomeado), evento 1560 (resposta), evento 1565 (verbete_citado, campo_ausente), evento 1566 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: campo_ausente, contrato-produto, campo_renomeado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1541 a 1580 da trilha; hash dos eventos deste caso: `1076760017fb06c1`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
