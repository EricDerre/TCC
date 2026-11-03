<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-21`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/sin-21@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `tipo` · selo de probabilidade: **medio** (p = 0,98) · **CONFLITO**: a FONTE cita o verbete tipo_divergente, fora do contexto entregue

**IMPACTO (declarado):** `O usuário vê o tipo do produto exibido como um objeto JSON em vez de um texto simples, o que pode causar confusão.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo tipo porque o sinal tipo: esperado texto, recebido objeto está presente na resposta HTTP e os verbetes campo_ausente, colecao_no_lugar_de_objeto, contrato-produto estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,01. A FONTE cita 2 verbete(s), 1 fora do contexto entregue (tipo_divergente). O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a FONTE cita o verbete tipo_divergente, fora do contexto entregue. Este nó está marcado com a falha citacao_fora_do_contexto (origem: modelo).

## 2. Evidência

Poda de `arvore` (evento 1609): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `44439f441a244cf6`):

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
      text "{"valor":"Carnes","moeda":"BRL"}"
      text "Picanha grelhada com alho laminado na brasa"
      text "destaque: Sim"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "{"valor":"Carnes","moeda":"BRL"}"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "{"valor":"Carnes","moeda":"BRL"}"
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

Poda de `corpo_http` (evento 1611): regras diff_contra_contrato; antes {"chars": 2404}, depois {"chars": 45}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tipo | texto | objeto |

Trecho podado (hash `8b29b8105a557dd2`):

```text
{"tipo": {"valor": "Carnes", "moeda": "BRL"}}
```

Interceptação (evento 1604): `GET /api/produtos` status 200; corpo `8166f86042f25264`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 0,98 contra 0,01; verbete(s) na evidência: campo_ausente, colecao_no_lugar_de_objeto, contrato-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,98 | sim |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [tipo_divergente]`; verbetes citados: `contrato-produto`, `tipo_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `campo_ausente`, `colecao_no_lugar_de_objeto`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | **não confere** | contexto: `campo_ausente`, `colecao_no_lugar_de_objeto`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[contrato-produto] [tipo_divergente]` | confere | {"ids": ["contrato-produto", "tipo_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids sin-21 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1597 | 1 | entrada | programa | ao_vivo | 2026-11-01T12:11:29 | caso sin-21 |
| 1598 | 2 | acao | programa | ao_vivo | 2026-11-01T12:11:29 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 107.1, "falhou": false} |
| 1599 | 3 | acao | programa | ao_vivo | 2026-11-01T12:11:29 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 17.9, "falhou": false} |
| 1600 | 4 | acao | programa | ao_vivo | 2026-11-01T12:11:29 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 3.7, "falhou": false} |
| 1601 | 5 | acao | programa | ao_vivo | 2026-11-01T12:11:29 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 8.4, "falhou": false} |
| 1602 | 6 | acao | programa | ao_vivo | 2026-11-01T12:11:29 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 4.0, "falhou": false} |
| 1604 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T12:11:29 | GET /api/produtos 200 |
| 1605 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T12:11:29 | conferencia_do_roteiro: confere |
| 1606 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T12:11:29 | conferencia_do_roteiro: confere |
| 1607 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T12:11:29 | conferencia_do_roteiro: confere |
| 1609 | 11 | poda | programa | ao_vivo | 2026-11-01T12:11:29 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1611 | 12 | poda | programa | ao_vivo | 2026-11-01T12:11:29 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1612 | 13 | candidatos | programa | ao_vivo | 2026-11-01T12:11:29 | 3 de 40 verbetes entregues |
| 1614 | 14 | prompt | programa | ao_vivo | 2026-11-01T12:11:29 | {"etapa": "diagnostico", "sha": "a1c2bedf8fdf9253", "prompt_sha256": "a1c2bedf8fdf", "chars": 5722, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1616 | 15 | inferencia | programa | ao_vivo | 2026-11-01T12:11:29 | diagnostico: 101,3 s |
| 1617 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T12:11:29 | causa_raiz: `tipo_divergente` |
| 1618 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T12:11:29 | campo: `tipo` |
| 1619 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T12:11:29 | impacto: `O usuário vê o tipo do produto exibido como um objeto JSON em vez de um texto simples, o que pode causar confusão.` |
| 1620 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T12:11:29 | fonte: `[contrato-produto] [tipo_divergente]` |
| 1621 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T12:11:29 | fonte_citada: `contrato-produto` |
| 1622 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T12:11:29 | fonte_citada: `tipo_divergente` |
| 1623 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T12:11:29 | quatro_linhas_presentes: confere |
| 1624 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T12:11:29 | rotulo_no_conjunto: confere |
| 1625 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T12:11:29 | fonte_existe_na_biblioteca: confere |
| 1626 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T12:11:29 | fonte_existe_na_biblioteca: confere |
| 1627 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T12:11:29 | fonte_estava_no_contexto: confere |
| 1628 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T12:11:29 | fonte_estava_no_contexto: nao_confere |
| 1629 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T12:11:29 | campo_existe_no_caso: confere |
| 1630 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T12:11:29 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1631 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T12:11:29 | notas_nos_verbetes_citados: informativo |
| 1632 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T12:11:29 | impacto: nao_verificavel |
| 1633 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T12:11:29 | fonte_formato_valido: confere |
| 1634 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T12:11:29 | fonte_contem_termo_da_causa: nao_confere |
| 1635 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T12:11:29 | fonte_contem_termo_da_causa: confere |
| 1636 | 35 | decisao | programa | ao_vivo | 2026-11-01T12:11:29 | diagnostico: escolha tipo_divergente; divergência sim |

</details>

Nós de decisão:

- evento 1636, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1611 (sinal_em_codigo), evento 1609 (arvore_podada), evento 1604 (corpo_http), evento 1612 (verbete_entregue, campo_ausente), evento 1612 (verbete_entregue, colecao_no_lugar_de_objeto), evento 1612 (verbete_entregue, contrato-produto), evento 1616 (resposta), evento 1621 (verbete_citado, contrato-produto), evento 1622 (verbete_citado, tipo_divergente); divergência: sim; falha: citacao_fora_do_contexto; prov.used: campo_ausente, colecao_no_lugar_de_objeto, contrato-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1597 a 1636 da trilha; hash dos eventos deste caso: `78e4f19a4b528ecc`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
