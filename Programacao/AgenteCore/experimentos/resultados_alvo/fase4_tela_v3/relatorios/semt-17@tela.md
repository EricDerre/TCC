<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-17`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/semt-17@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `nulo_inesperado` · **CAMPO:** `id` · selo de probabilidade: **medio** (p = 0,97)

**IMPACTO (declarado):** `O usuário vê um botão com um identificador nulo, o que pode levar a erros na interação com a interface.`

Justificativa (gerada por molde): O agente respondeu nulo_inesperado no campo id porque o sinal id: esperado inteiro, recebido nulo está presente na resposta HTTP e os verbetes nulo_inesperado, contrato-produto, entidade-produto estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1683): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `ec5e87aaa55e738e`):

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
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="null"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="null"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "R$ 69,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="null"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 1685): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2105}, depois {"chars": 12}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | inteiro | nulo |
| id | 1 (referência em modo normal) | null em 14 itens |

Trecho podado (hash `735c36862ca0cbf9`):

```text
{"id": null}
```

Interceptação (evento 1678): `GET /api/produtos` status 200; corpo `a33ec7dcc3457d74`, árvore `None`.

## 3. Contraste com a segunda causa

nulo_inesperado e não campo_ausente: a escolha tem probabilidade 0,97 contra 0,00; verbete(s) na evidência: nulo_inesperado, contrato-produto, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| nulo_inesperado | 0,97 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| tipo_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[nulo_inesperado]`; verbetes citados: `nulo_inesperado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `nulo_inesperado`, `contrato-produto`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `nulo_inesperado` |
| fonte_formato_valido | `[nulo_inesperado]` | confere | {"ids": ["nulo_inesperado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids semt-17 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1671 | 1 | entrada | programa | ao_vivo | 2026-11-05T19:39:51 | caso semt-17 |
| 1672 | 2 | acao | programa | ao_vivo | 2026-11-05T19:39:51 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 150.4, "falhou": false} |
| 1673 | 3 | acao | programa | ao_vivo | 2026-11-05T19:39:51 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 5.7, "falhou": false} |
| 1674 | 4 | acao | programa | ao_vivo | 2026-11-05T19:39:51 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 1.9, "falhou": false} |
| 1675 | 5 | acao | programa | ao_vivo | 2026-11-05T19:39:51 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 3.9, "falhou": false} |
| 1676 | 6 | acao | programa | ao_vivo | 2026-11-05T19:39:51 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.6, "falhou": false} |
| 1678 | 7 | interceptacao | programa | ao_vivo | 2026-11-05T19:39:51 | GET /api/produtos 200 |
| 1679 | 8 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:51 | conferencia_do_roteiro: confere |
| 1680 | 9 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:51 | conferencia_do_roteiro: confere |
| 1681 | 10 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:51 | conferencia_do_roteiro: confere |
| 1683 | 11 | poda | programa | ao_vivo | 2026-11-05T19:39:51 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1685 | 12 | poda | programa | ao_vivo | 2026-11-05T19:39:51 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1686 | 13 | candidatos | programa | ao_vivo | 2026-11-05T19:39:51 | 3 de 39 verbetes entregues |
| 1688 | 14 | prompt | programa | ao_vivo | 2026-11-05T19:39:51 | {"etapa": "diagnostico", "sha": "2b5cdccbbb023c1b", "prompt_sha256": "2b5cdccbbb02", "chars": 3347, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1690 | 15 | inferencia | programa | ao_vivo | 2026-11-05T19:39:51 | diagnostico: 35,2 s |
| 1691 | 16 | declaracao | modelo | ao_vivo | 2026-11-05T19:39:51 | causa_raiz: `nulo_inesperado` |
| 1692 | 17 | declaracao | modelo | ao_vivo | 2026-11-05T19:39:51 | campo: `id` |
| 1693 | 18 | declaracao | modelo | ao_vivo | 2026-11-05T19:39:51 | impacto: `O usuário vê um botão com um identificador nulo, o que pode levar a erros na interação com a interface.` |
| 1694 | 19 | declaracao | modelo | ao_vivo | 2026-11-05T19:39:51 | fonte: `[nulo_inesperado]` |
| 1695 | 20 | declaracao | modelo | ao_vivo | 2026-11-05T19:39:51 | fonte_citada: `nulo_inesperado` |
| 1696 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:51 | quatro_linhas_presentes: confere |
| 1697 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:51 | rotulo_no_conjunto: confere |
| 1698 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:51 | fonte_existe_na_biblioteca: confere |
| 1699 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:51 | fonte_estava_no_contexto: confere |
| 1700 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:51 | campo_existe_no_caso: confere |
| 1701 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:51 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1702 | 27 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:51 | notas_nos_verbetes_citados: informativo |
| 1703 | 28 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:51 | impacto: nao_verificavel |
| 1704 | 29 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:51 | fonte_formato_valido: confere |
| 1705 | 30 | verificacao | verificacao | ao_vivo | 2026-11-05T19:39:51 | fonte_contem_termo_da_causa: confere |
| 1706 | 31 | decisao | programa | ao_vivo | 2026-11-05T19:39:51 | diagnostico: escolha nulo_inesperado; divergência não |

</details>

Nós de decisão:

- evento 1706, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 1685 (sinal_em_codigo), evento 1683 (arvore_podada), evento 1678 (corpo_http), evento 1686 (verbete_entregue, nulo_inesperado), evento 1686 (verbete_entregue, contrato-produto), evento 1686 (verbete_entregue, entidade-produto), evento 1690 (resposta), evento 1695 (verbete_citado, nulo_inesperado); divergência: não; falha: nenhuma; prov.used: nulo_inesperado, contrato-produto, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1671 a 1706 da trilha; hash dos eventos deste caso: `ce402450ec5fab22`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
