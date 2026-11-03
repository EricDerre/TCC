<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-9`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/semt-9@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `destaque` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê "destaque: talvez" em vez de um valor booleano, o que pode causar confusão na interpretação do destaque dos produtos.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo destaque porque o sinal destaque: esperado booleano, recebido texto está presente na resposta HTTP e os verbetes contrato-produto, campo_ausente, valor_fora_do_dominio estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1072): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `cd49b7776d4eb6ca`):

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
      text "destaque: talvez"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: talvez"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: talvez"
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

Poda de `corpo_http` (evento 1074): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2115}, depois {"chars": 22}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| destaque | booleano | texto |
| destaque | true (referência em modo normal) | "talvez" em 14 itens |

Trecho podado (hash `c65ddeac1dc2e258`):

```text
{"destaque": "talvez"}
```

Interceptação (evento 1067): `GET /api/produtos` status 200; corpo `283a95908461b884`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não valor_fora_do_dominio: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-produto, campo_ausente, valor_fora_do_dominio

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 1,00 | sim |
| valor_fora_do_dominio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| resposta_truncada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `campo_ausente`, `valor_fora_do_dominio` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `contrato-produto`, `valor_fora_do_dominio` |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `destaque` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids semt-9 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1060 | 1 | entrada | programa | ao_vivo | 2026-11-01T14:49:33 | caso semt-9 |
| 1061 | 2 | acao | programa | ao_vivo | 2026-11-01T14:49:33 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 112.9, "falhou": false} |
| 1062 | 3 | acao | programa | ao_vivo | 2026-11-01T14:49:33 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 10.7, "falhou": false} |
| 1063 | 4 | acao | programa | ao_vivo | 2026-11-01T14:49:33 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.4, "falhou": false} |
| 1064 | 5 | acao | programa | ao_vivo | 2026-11-01T14:49:33 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 9.2, "falhou": false} |
| 1065 | 6 | acao | programa | ao_vivo | 2026-11-01T14:49:33 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 10.4, "falhou": false} |
| 1067 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T14:49:33 | GET /api/produtos 200 |
| 1068 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T14:49:33 | conferencia_do_roteiro: confere |
| 1069 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T14:49:33 | conferencia_do_roteiro: confere |
| 1070 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T14:49:33 | conferencia_do_roteiro: confere |
| 1072 | 11 | poda | programa | ao_vivo | 2026-11-01T14:49:33 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1074 | 12 | poda | programa | ao_vivo | 2026-11-01T14:49:33 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1075 | 13 | candidatos | programa | ao_vivo | 2026-11-01T14:49:33 | 3 de 40 verbetes entregues |
| 1077 | 14 | prompt | programa | ao_vivo | 2026-11-01T14:49:33 | {"etapa": "diagnostico", "sha": "6c851b3e2f7db28f", "prompt_sha256": "6c851b3e2f7d", "chars": 5603, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1079 | 15 | inferencia | programa | ao_vivo | 2026-11-01T14:49:33 | diagnostico: 96,5 s |
| 1080 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T14:49:33 | causa_raiz: `tipo_divergente` |
| 1081 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T14:49:33 | campo: `destaque` |
| 1082 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T14:49:33 | impacto: `O usuário vê "destaque: talvez" em vez de um valor booleano, o que pode causar confusão na interpretação do destaque dos produtos.` |
| 1083 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T14:49:33 | fonte: `[contrato-produto]` |
| 1084 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T14:49:33 | fonte_citada: `contrato-produto` |
| 1085 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T14:49:33 | quatro_linhas_presentes: confere |
| 1086 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T14:49:33 | rotulo_no_conjunto: confere |
| 1087 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T14:49:33 | fonte_existe_na_biblioteca: confere |
| 1088 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T14:49:33 | fonte_estava_no_contexto: confere |
| 1089 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T14:49:33 | campo_existe_no_caso: confere |
| 1090 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T14:49:33 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1091 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T14:49:33 | notas_nos_verbetes_citados: informativo |
| 1092 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T14:49:33 | impacto: nao_verificavel |
| 1093 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T14:49:33 | fonte_formato_valido: confere |
| 1094 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T14:49:33 | fonte_contem_termo_da_causa: nao_confere |
| 1095 | 31 | decisao | programa | ao_vivo | 2026-11-01T14:49:33 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 1095, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1074 (sinal_em_codigo), evento 1072 (arvore_podada), evento 1067 (corpo_http), evento 1075 (verbete_entregue, contrato-produto), evento 1075 (verbete_entregue, campo_ausente), evento 1075 (verbete_entregue, valor_fora_do_dominio), evento 1079 (resposta), evento 1084 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: contrato-produto, campo_ausente, valor_fora_do_dominio (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1060 a 1095 da trilha; hash dos eventos deste caso: `c1c6266939c59572`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
