<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-17`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/semt-17@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `id` · selo de probabilidade: **medio** (p = 0,88)

**IMPACTO (declarado):** `O usuário vê um campo id nulo, o que pode causar problemas na identificação dos produtos.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo id porque o sinal id: esperado inteiro, recebido nulo está presente na resposta HTTP e os verbetes campo_ausente, contrato-produto, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,11 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1737): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 1739): regras diff_contra_contrato; antes {"chars": 2105}, depois {"chars": 12}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | inteiro | nulo |

Trecho podado (hash `735c36862ca0cbf9`):

```text
{"id": null}
```

Interceptação (evento 1732): `GET /api/produtos` status 200; corpo `a33ec7dcc3457d74`, árvore `None`.

## 3. Contraste com a segunda causa

campo_ausente e não corpo_nao_e_json: a escolha tem probabilidade 0,88 contra 0,11; verbete(s) na evidência: campo_ausente, contrato-produto, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 0,88 | sim |
| corpo_nao_e_json | 0,11 |  |
| corpo_vazio | 0,11 |  |
| resposta_truncada | 0,00 |  |
| tipo_divergente | 0,00 |  |
| nulo_inesperado | 0,00 |  |
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

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids semt-17 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1725 | 1 | entrada | programa | ao_vivo | 2026-11-01T12:16:32 | caso semt-17 |
| 1726 | 2 | acao | programa | ao_vivo | 2026-11-01T12:16:33 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 191.8, "falhou": false} |
| 1727 | 3 | acao | programa | ao_vivo | 2026-11-01T12:16:33 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 8.4, "falhou": false} |
| 1728 | 4 | acao | programa | ao_vivo | 2026-11-01T12:16:33 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.3, "falhou": false} |
| 1729 | 5 | acao | programa | ao_vivo | 2026-11-01T12:16:33 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 4.3, "falhou": false} |
| 1730 | 6 | acao | programa | ao_vivo | 2026-11-01T12:16:33 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 4.3, "falhou": false} |
| 1732 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T12:16:33 | GET /api/produtos 200 |
| 1733 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T12:16:33 | conferencia_do_roteiro: confere |
| 1734 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T12:16:33 | conferencia_do_roteiro: confere |
| 1735 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T12:16:33 | conferencia_do_roteiro: confere |
| 1737 | 11 | poda | programa | ao_vivo | 2026-11-01T12:16:33 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1739 | 12 | poda | programa | ao_vivo | 2026-11-01T12:16:33 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1740 | 13 | candidatos | programa | ao_vivo | 2026-11-01T12:16:33 | 3 de 40 verbetes entregues |
| 1742 | 14 | prompt | programa | ao_vivo | 2026-11-01T12:16:33 | {"etapa": "diagnostico", "sha": "4785af085e65a4aa", "prompt_sha256": "4785af085e65", "chars": 5260, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1744 | 15 | inferencia | programa | ao_vivo | 2026-11-01T12:16:33 | diagnostico: 59,4 s |
| 1745 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T12:16:33 | causa_raiz: `campo_ausente` |
| 1746 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T12:16:33 | campo: `id` |
| 1747 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T12:16:33 | impacto: `O usuário vê um campo id nulo, o que pode causar problemas na identificação dos produtos.` |
| 1748 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T12:16:33 | fonte: `[campo_ausente] [contrato-produto]` |
| 1749 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T12:16:33 | fonte_citada: `campo_ausente` |
| 1750 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T12:16:33 | fonte_citada: `contrato-produto` |
| 1751 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T12:16:33 | quatro_linhas_presentes: confere |
| 1752 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T12:16:33 | rotulo_no_conjunto: confere |
| 1753 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T12:16:33 | fonte_existe_na_biblioteca: confere |
| 1754 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T12:16:33 | fonte_existe_na_biblioteca: confere |
| 1755 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T12:16:33 | fonte_estava_no_contexto: confere |
| 1756 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T12:16:33 | fonte_estava_no_contexto: confere |
| 1757 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T12:16:33 | campo_existe_no_caso: confere |
| 1758 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T12:16:33 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1759 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T12:16:33 | notas_nos_verbetes_citados: informativo |
| 1760 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T12:16:33 | impacto: nao_verificavel |
| 1761 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T12:16:33 | fonte_formato_valido: confere |
| 1762 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T12:16:33 | fonte_contem_termo_da_causa: confere |
| 1763 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T12:16:33 | fonte_contem_termo_da_causa: nao_confere |
| 1764 | 35 | decisao | programa | ao_vivo | 2026-11-01T12:16:33 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 1764, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 1739 (sinal_em_codigo), evento 1737 (arvore_podada), evento 1732 (corpo_http), evento 1740 (verbete_entregue, campo_ausente), evento 1740 (verbete_entregue, contrato-produto), evento 1740 (verbete_entregue, colecao_no_lugar_de_objeto), evento 1744 (resposta), evento 1749 (verbete_citado, campo_ausente), evento 1750 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: campo_ausente, contrato-produto, colecao_no_lugar_de_objeto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1725 a 1764 da trilha; hash dos eventos deste caso: `9392e01f2c4a85db`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
