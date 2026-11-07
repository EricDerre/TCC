<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-16`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/semt-16@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `tipo` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê o tipo como um número inteiro em vez de texto, o que pode causar interpretações incorretas na interface.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo tipo porque o sinal tipo: esperado texto, recebido inteiro está presente na resposta HTTP e os verbetes tipo_divergente, contrato-produto, entidade-produto estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1623): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `fd4991ac141eed24`):

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
      text "1"
      text "Picanha grelhada com alho laminado na brasa"
      text "destaque: Sim"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "1"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "1"
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

Poda de `corpo_http` (evento 1625): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 1936}, depois {"chars": 11}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tipo | texto | inteiro |
| tipo | "Carnes" (referência em modo normal) | 1 em 14 itens |

Trecho podado (hash `7e091f5a6aa3bb8f`):

```text
{"tipo": 1}
```

Interceptação (evento 1618): `GET /api/produtos` status 200; corpo `283c10134d6edd20`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: tipo_divergente, contrato-produto, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 1,00 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| resposta_truncada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tipo_divergente]`; verbetes citados: `tipo_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `tipo_divergente`, `contrato-produto`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `tipo_divergente`, `contrato-produto`, `entidade-produto` |
| fonte_formato_valido | `[tipo_divergente]` | confere | {"ids": ["tipo_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids semt-16 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1611 | 1 | entrada | programa | ao_vivo | 2026-11-05T19:38:32 | caso semt-16 |
| 1612 | 2 | acao | programa | ao_vivo | 2026-11-05T19:38:32 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 113.2, "falhou": false} |
| 1613 | 3 | acao | programa | ao_vivo | 2026-11-05T19:38:32 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 9.2, "falhou": false} |
| 1614 | 4 | acao | programa | ao_vivo | 2026-11-05T19:38:32 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 6.5, "falhou": false} |
| 1615 | 5 | acao | programa | ao_vivo | 2026-11-05T19:38:32 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 5.8, "falhou": false} |
| 1616 | 6 | acao | programa | ao_vivo | 2026-11-05T19:38:32 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.2, "falhou": false} |
| 1618 | 7 | interceptacao | programa | ao_vivo | 2026-11-05T19:38:32 | GET /api/produtos 200 |
| 1619 | 8 | verificacao | verificacao | ao_vivo | 2026-11-05T19:38:32 | conferencia_do_roteiro: confere |
| 1620 | 9 | verificacao | verificacao | ao_vivo | 2026-11-05T19:38:32 | conferencia_do_roteiro: confere |
| 1621 | 10 | verificacao | verificacao | ao_vivo | 2026-11-05T19:38:32 | conferencia_do_roteiro: confere |
| 1623 | 11 | poda | programa | ao_vivo | 2026-11-05T19:38:32 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1625 | 12 | poda | programa | ao_vivo | 2026-11-05T19:38:32 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1626 | 13 | candidatos | programa | ao_vivo | 2026-11-05T19:38:32 | 3 de 39 verbetes entregues |
| 1628 | 14 | prompt | programa | ao_vivo | 2026-11-05T19:38:32 | {"etapa": "diagnostico", "sha": "c28cb2fff982895d", "prompt_sha256": "c28cb2fff982", "chars": 3558, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1630 | 15 | inferencia | programa | ao_vivo | 2026-11-05T19:38:32 | diagnostico: 36,0 s |
| 1631 | 16 | declaracao | modelo | ao_vivo | 2026-11-05T19:38:32 | causa_raiz: `tipo_divergente` |
| 1632 | 17 | declaracao | modelo | ao_vivo | 2026-11-05T19:38:32 | campo: `tipo` |
| 1633 | 18 | declaracao | modelo | ao_vivo | 2026-11-05T19:38:32 | impacto: `O usuário vê o tipo como um número inteiro em vez de texto, o que pode causar interpretações incorretas na interface.` |
| 1634 | 19 | declaracao | modelo | ao_vivo | 2026-11-05T19:38:32 | fonte: `[tipo_divergente]` |
| 1635 | 20 | declaracao | modelo | ao_vivo | 2026-11-05T19:38:32 | fonte_citada: `tipo_divergente` |
| 1636 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T19:38:32 | quatro_linhas_presentes: confere |
| 1637 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T19:38:32 | rotulo_no_conjunto: confere |
| 1638 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T19:38:32 | fonte_existe_na_biblioteca: confere |
| 1639 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T19:38:32 | fonte_estava_no_contexto: confere |
| 1640 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T19:38:32 | campo_existe_no_caso: confere |
| 1641 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T19:38:32 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1642 | 27 | verificacao | verificacao | ao_vivo | 2026-11-05T19:38:32 | notas_nos_verbetes_citados: informativo |
| 1643 | 28 | verificacao | verificacao | ao_vivo | 2026-11-05T19:38:32 | impacto: nao_verificavel |
| 1644 | 29 | verificacao | verificacao | ao_vivo | 2026-11-05T19:38:32 | fonte_formato_valido: confere |
| 1645 | 30 | verificacao | verificacao | ao_vivo | 2026-11-05T19:38:32 | fonte_contem_termo_da_causa: confere |
| 1646 | 31 | decisao | programa | ao_vivo | 2026-11-05T19:38:32 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 1646, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1625 (sinal_em_codigo), evento 1623 (arvore_podada), evento 1618 (corpo_http), evento 1626 (verbete_entregue, tipo_divergente), evento 1626 (verbete_entregue, contrato-produto), evento 1626 (verbete_entregue, entidade-produto), evento 1630 (resposta), evento 1635 (verbete_citado, tipo_divergente); divergência: não; falha: nenhuma; prov.used: tipo_divergente, contrato-produto, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1611 a 1646 da trilha; hash dos eventos deste caso: `1f8f8fbf177f4d33`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
