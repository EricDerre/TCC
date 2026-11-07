<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-24`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/semt-24@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `destaque` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê o campo destaque como texto em vez de booleano, resultando em uma exibição incorreta na interface web.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo destaque porque o sinal destaque: esperado booleano, recebido texto está presente na resposta HTTP e os verbetes tipo_divergente, contrato-produto, entidade-produto estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 870): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `c313b8b1cf5627df`):

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
      text "destaque: True"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: False"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: False"
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

Poda de `corpo_http` (evento 872): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2096}, depois {"chars": 20}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| destaque | booleano | texto |
| destaque | true (referência em modo normal) | "True" em 14 itens |

Trecho podado (hash `5ec83198df34c240`):

```text
{"destaque": "True"}
```

Interceptação (evento 865): `GET /api/produtos` status 200; corpo `733c772e1d9b42a2`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: tipo_divergente, contrato-produto, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 1,00 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tipo_divergente] [contrato-produto]`; verbetes citados: `tipo_divergente`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `tipo_divergente`, `contrato-produto`, `entidade-produto` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `tipo_divergente`, `contrato-produto`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `tipo_divergente`, `contrato-produto`, `entidade-produto` |
| fonte_formato_valido | `[tipo_divergente] [contrato-produto]` | confere | {"ids": ["tipo_divergente", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `destaque` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids semt-24 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 858 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:58:30 | caso semt-24 |
| 859 | 2 | acao | programa | ao_vivo | 2026-11-06T11:58:30 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 110.0, "falhou": false} |
| 860 | 3 | acao | programa | ao_vivo | 2026-11-06T11:58:30 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 23.5, "falhou": false} |
| 861 | 4 | acao | programa | ao_vivo | 2026-11-06T11:58:30 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.6, "falhou": false} |
| 862 | 5 | acao | programa | ao_vivo | 2026-11-06T11:58:30 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 3.7, "falhou": false} |
| 863 | 6 | acao | programa | ao_vivo | 2026-11-06T11:58:30 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.2, "falhou": false} |
| 865 | 7 | interceptacao | programa | ao_vivo | 2026-11-06T11:58:30 | GET /api/produtos 200 |
| 866 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T11:58:30 | conferencia_do_roteiro: confere |
| 867 | 9 | verificacao | verificacao | ao_vivo | 2026-11-06T11:58:30 | conferencia_do_roteiro: confere |
| 868 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:58:30 | conferencia_do_roteiro: confere |
| 870 | 11 | poda | programa | ao_vivo | 2026-11-06T11:58:30 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 872 | 12 | poda | programa | ao_vivo | 2026-11-06T11:58:30 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 873 | 13 | candidatos | programa | ao_vivo | 2026-11-06T11:58:30 | 3 de 39 verbetes entregues |
| 875 | 14 | prompt | programa | ao_vivo | 2026-11-06T11:58:30 | {"etapa": "diagnostico", "sha": "71f4d41efc9ada11", "prompt_sha256": "71f4d41efc9a", "chars": 3614, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 877 | 15 | inferencia | programa | ao_vivo | 2026-11-06T11:58:30 | diagnostico: 73,7 s |
| 878 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T11:58:30 | causa_raiz: `tipo_divergente` |
| 879 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T11:58:30 | campo: `destaque` |
| 880 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T11:58:30 | impacto: `O usuário vê o campo destaque como texto em vez de booleano, resultando em uma exibição incorreta na interface web.` |
| 881 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T11:58:30 | fonte: `[tipo_divergente] [contrato-produto]` |
| 882 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T11:58:30 | fonte_citada: `tipo_divergente` |
| 883 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T11:58:30 | fonte_citada: `contrato-produto` |
| 884 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:58:30 | quatro_linhas_presentes: confere |
| 885 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:58:30 | rotulo_no_conjunto: confere |
| 886 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:58:30 | fonte_existe_na_biblioteca: confere |
| 887 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:58:30 | fonte_existe_na_biblioteca: confere |
| 888 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:58:30 | fonte_estava_no_contexto: confere |
| 889 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T11:58:30 | fonte_estava_no_contexto: confere |
| 890 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T11:58:30 | campo_existe_no_caso: confere |
| 891 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T11:58:30 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 892 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T11:58:30 | notas_nos_verbetes_citados: informativo |
| 893 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T11:58:30 | impacto: nao_verificavel |
| 894 | 32 | verificacao | verificacao | ao_vivo | 2026-11-06T11:58:30 | fonte_formato_valido: confere |
| 895 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T11:58:30 | fonte_contem_termo_da_causa: confere |
| 896 | 34 | verificacao | verificacao | ao_vivo | 2026-11-06T11:58:30 | fonte_contem_termo_da_causa: nao_confere |
| 897 | 35 | decisao | programa | ao_vivo | 2026-11-06T11:58:30 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 897, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 872 (sinal_em_codigo), evento 870 (arvore_podada), evento 865 (corpo_http), evento 873 (verbete_entregue, tipo_divergente), evento 873 (verbete_entregue, contrato-produto), evento 873 (verbete_entregue, entidade-produto), evento 877 (resposta), evento 882 (verbete_citado, tipo_divergente), evento 883 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: tipo_divergente, contrato-produto, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 858 a 897 da trilha; hash dos eventos deste caso: `2974154b13afce31`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
