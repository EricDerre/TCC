<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-9`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/semt-9@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `destaque` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê "destaque: talvez" em vez de um booleano, o que pode causar interpretações incorretas na interface.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo destaque porque o sinal destaque: esperado booleano, recebido texto está presente na resposta HTTP e os verbetes contrato-produto, campo_ausente, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1064): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 1066): regras diff_contra_contrato; antes {"chars": 2115}, depois {"chars": 22}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| destaque | booleano | texto |

Trecho podado (hash `c65ddeac1dc2e258`):

```text
{"destaque": "talvez"}
```

Interceptação (evento 1059): `GET /api/produtos` status 200; corpo `283a95908461b884`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-produto, campo_ausente, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 1,00 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tipo_divergente]`; verbetes citados: `tipo_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `contrato-produto`, `campo_ausente`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `contrato-produto`, `tipo_divergente` |
| fonte_formato_valido | `[tipo_divergente]` | confere | {"ids": ["tipo_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `destaque` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids semt-9 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1052 | 1 | entrada | programa | ao_vivo | 2026-11-01T11:50:46 | caso semt-9 |
| 1053 | 2 | acao | programa | ao_vivo | 2026-11-01T11:50:46 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 141.6, "falhou": false} |
| 1054 | 3 | acao | programa | ao_vivo | 2026-11-01T11:50:46 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 12.8, "falhou": false} |
| 1055 | 4 | acao | programa | ao_vivo | 2026-11-01T11:50:46 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 3.5, "falhou": false} |
| 1056 | 5 | acao | programa | ao_vivo | 2026-11-01T11:50:46 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 10.5, "falhou": false} |
| 1057 | 6 | acao | programa | ao_vivo | 2026-11-01T11:50:46 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 5.5, "falhou": false} |
| 1059 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T11:50:46 | GET /api/produtos 200 |
| 1060 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T11:50:46 | conferencia_do_roteiro: confere |
| 1061 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T11:50:46 | conferencia_do_roteiro: confere |
| 1062 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T11:50:46 | conferencia_do_roteiro: confere |
| 1064 | 11 | poda | programa | ao_vivo | 2026-11-01T11:50:46 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1066 | 12 | poda | programa | ao_vivo | 2026-11-01T11:50:46 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1067 | 13 | candidatos | programa | ao_vivo | 2026-11-01T11:50:46 | 3 de 40 verbetes entregues |
| 1069 | 14 | prompt | programa | ao_vivo | 2026-11-01T11:50:46 | {"etapa": "diagnostico", "sha": "ceccc673f396dca0", "prompt_sha256": "ceccc673f396", "chars": 5331, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1071 | 15 | inferencia | programa | ao_vivo | 2026-11-01T11:50:46 | diagnostico: 93,7 s |
| 1072 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T11:50:46 | causa_raiz: `tipo_divergente` |
| 1073 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T11:50:46 | campo: `destaque` |
| 1074 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T11:50:46 | impacto: `O usuário vê "destaque: talvez" em vez de um booleano, o que pode causar interpretações incorretas na interface.` |
| 1075 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T11:50:46 | fonte: `[tipo_divergente]` |
| 1076 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T11:50:46 | fonte_citada: `tipo_divergente` |
| 1077 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T11:50:46 | quatro_linhas_presentes: confere |
| 1078 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T11:50:46 | rotulo_no_conjunto: confere |
| 1079 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T11:50:46 | fonte_existe_na_biblioteca: confere |
| 1080 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T11:50:46 | fonte_estava_no_contexto: confere |
| 1081 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T11:50:46 | campo_existe_no_caso: confere |
| 1082 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T11:50:46 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1083 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T11:50:46 | notas_nos_verbetes_citados: informativo |
| 1084 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T11:50:46 | impacto: nao_verificavel |
| 1085 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T11:50:46 | fonte_formato_valido: confere |
| 1086 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T11:50:46 | fonte_contem_termo_da_causa: confere |
| 1087 | 31 | decisao | programa | ao_vivo | 2026-11-01T11:50:46 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 1087, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1066 (sinal_em_codigo), evento 1064 (arvore_podada), evento 1059 (corpo_http), evento 1067 (verbete_entregue, contrato-produto), evento 1067 (verbete_entregue, campo_ausente), evento 1067 (verbete_entregue, tipo_divergente), evento 1071 (resposta), evento 1076 (verbete_citado, tipo_divergente); divergência: não; falha: nenhuma; prov.used: contrato-produto, campo_ausente, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1052 a 1087 da trilha; hash dos eventos deste caso: `dc6c01a37a4aafeb`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
