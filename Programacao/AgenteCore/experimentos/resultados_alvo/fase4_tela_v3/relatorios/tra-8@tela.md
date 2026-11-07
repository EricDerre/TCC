<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-8`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/tra-8@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `resposta_truncada` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,55) · **CONFLITO**: nenhum verbete entregue trata da causa respondida resposta_truncada

**IMPACTO (declarado):** `A interface exibiu 10 cartões a menos do que o esperado, pois a API retornou uma lista com 13 itens em vez dos 14 previstos.`

Justificativa (gerada por molde): O agente respondeu resposta_truncada no campo itens porque o sinal itens: esperado 14 itens (referência em modo normal), recebido falta o id 14 ("Abacaxi na Brasa") está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, contagem_inconsistente estavam entre os entregues ao modelo. A segunda causa, contagem_inconsistente, ficou com probabilidade 0,43. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida resposta_truncada. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,55); trate como hipótese e confira o campo itens antes de agir.

## 2. Evidência

Poda de `arvore` (evento 1150): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 183}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 1 linha(s) da referência | 1 linha(s) novas |

Trecho podado (hash `7c54fbd0508aace9`):

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
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "R$ 69,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 10 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 1151): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 1928}, depois {"chars": 277}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| itens | 14 itens (referência em modo normal) | falta o id 14 ("Abacaxi na Brasa") |

Trecho podado (hash `9675592a8385ee52`):

```text
lista com 13 itens (referência em modo normal: 14); falta o id 14 ("Abacaxi na Brasa"); primeiro item: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 1148): `GET /api/produtos` status 200; corpo `4f6d409f5a92ce2d`, árvore `None`.

## 3. Contraste com a segunda causa

resposta_truncada e não contagem_inconsistente: a escolha tem probabilidade 0,55 contra 0,43; verbete(s) na evidência: entidade-produto, contrato-produto, contagem_inconsistente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| resposta_truncada | 0,55 | sim |
| contagem_inconsistente | 0,43 |  |
| colecao_no_lugar_de_objeto | 0,02 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contagem_inconsistente]`; verbetes citados: `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contagem_inconsistente]` | confere | {"ids": ["contagem_inconsistente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | **não confere** | {"termo": "resposta_truncada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids tra-8 --k 3`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1144 | 1 | entrada | programa | ao_vivo | 2026-11-05T19:22:04 | caso tra-8 |
| 1145 | 2 | acao | programa | ao_vivo | 2026-11-05T19:22:05 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 97.8, "falhou": false} |
| 1146 | 3 | acao | programa | ao_vivo | 2026-11-05T19:22:05 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 8.5, "falhou": false} |
| 1147 | 4 | acao | programa | ao_vivo | 2026-11-05T19:22:05 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.4, "falhou": true} |
| 1148 | 5 | interceptacao | programa | ao_vivo | 2026-11-05T19:22:05 | GET /api/produtos 200 |
| 1149 | 6 | verificacao | verificacao | ao_vivo | 2026-11-05T19:22:05 | conferencia_do_roteiro: nao_confere |
| 1150 | 7 | poda | programa | ao_vivo | 2026-11-05T19:22:05 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1151 | 8 | poda | programa | ao_vivo | 2026-11-05T19:22:05 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1152 | 9 | candidatos | programa | ao_vivo | 2026-11-05T19:22:05 | 3 de 39 verbetes entregues |
| 1153 | 10 | prompt | programa | ao_vivo | 2026-11-05T19:22:05 | {"etapa": "diagnostico", "sha": "408015577d788815", "prompt_sha256": "408015577d78", "chars": 3922, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1154 | 11 | inferencia | programa | ao_vivo | 2026-11-05T19:22:05 | diagnostico: 63,1 s |
| 1155 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T19:22:05 | causa_raiz: `resposta_truncada` |
| 1156 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T19:22:05 | campo: `nenhum` |
| 1157 | 14 | declaracao | modelo | ao_vivo | 2026-11-05T19:22:05 | impacto: `A interface exibiu 10 cartões a menos do que o esperado, pois a API retornou uma lista com 13 itens em vez dos 14 previstos.` |
| 1158 | 15 | declaracao | modelo | ao_vivo | 2026-11-05T19:22:05 | fonte: `[contagem_inconsistente]` |
| 1159 | 16 | declaracao | modelo | ao_vivo | 2026-11-05T19:22:05 | fonte_citada: `contagem_inconsistente` |
| 1160 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T19:22:05 | quatro_linhas_presentes: confere |
| 1161 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T19:22:05 | rotulo_no_conjunto: confere |
| 1162 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T19:22:05 | fonte_existe_na_biblioteca: confere |
| 1163 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T19:22:05 | fonte_estava_no_contexto: confere |
| 1164 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T19:22:05 | campo_existe_no_caso: nao_se_aplica |
| 1165 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T19:22:05 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 1166 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T19:22:05 | notas_nos_verbetes_citados: informativo |
| 1167 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T19:22:05 | impacto: nao_verificavel |
| 1168 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T19:22:05 | fonte_formato_valido: confere |
| 1169 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T19:22:05 | fonte_contem_termo_da_causa: nao_confere |
| 1170 | 27 | decisao | programa | ao_vivo | 2026-11-05T19:22:05 | diagnostico: escolha resposta_truncada; divergência sim |

</details>

Nós de decisão:

- evento 1170, `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido; evidência: evento 1151 (sinal_em_codigo), evento 1150 (arvore_podada), evento 1148 (corpo_http), evento 1152 (verbete_entregue, entidade-produto), evento 1152 (verbete_entregue, contrato-produto), evento 1152 (verbete_entregue, contagem_inconsistente), evento 1154 (resposta), evento 1159 (verbete_citado, contagem_inconsistente); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, contagem_inconsistente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1144 a 1170 da trilha; hash dos eventos deste caso: `12a9ee882fae10cc`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
