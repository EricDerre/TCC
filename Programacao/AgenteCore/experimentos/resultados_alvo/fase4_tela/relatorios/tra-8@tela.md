<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-8`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/tra-8@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `resposta_truncada` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,41) · **CONFLITO**: nenhum verbete entregue trata da causa respondida resposta_truncada

**IMPACTO (declarado):** `A interface web exibe menos produtos do que o esperado, causando uma experiência descontinuada para o usuário.`

Justificativa (gerada por molde): O agente respondeu resposta_truncada porque o sinal arvore: esperado 1 linha(s) da referência, recebido 1 linha(s) novas está presente na tela e os verbetes entidade-produto, colecao_no_lugar_de_objeto, contrato-produto estavam entre os entregues ao modelo. A segunda causa, contagem_inconsistente, ficou com probabilidade 0,39 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida resposta_truncada. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,41); trate como hipótese e confira o caso antes de agir.

## 2. Evidência

Poda de `arvore` (evento 1186): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 183}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 1187): regras diff_contra_contrato; antes {"chars": 1928}, depois {"chars": 174}.

Trecho podado (hash `b78f8a85ed458c1a`):

```text
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 1184): `GET /api/produtos` status 200; corpo `4f6d409f5a92ce2d`, árvore `None`.

## 3. Contraste com a segunda causa

resposta_truncada e não contagem_inconsistente: a escolha tem probabilidade 0,41 contra 0,39; verbete(s) na evidência: entidade-produto, colecao_no_lugar_de_objeto, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| resposta_truncada | 0,41 | sim |
| contagem_inconsistente | 0,39 |  |
| colecao_no_lugar_de_objeto | 0,15 |  |
| corpo_nao_e_json | 0,02 |  |
| corpo_vazio | 0,02 |  |
| estrutura_aninhada_divergente | 0,01 |  |
| formato_de_data_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| tipo_divergente | 0,00 |  |
| codificacao_incorreta | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [colecao_no_lugar_de_objeto]`; verbetes citados: `contrato-produto`, `colecao_no_lugar_de_objeto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `colecao_no_lugar_de_objeto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `colecao_no_lugar_de_objeto`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `colecao_no_lugar_de_objeto` | confere | contexto: `entidade-produto`, `colecao_no_lugar_de_objeto`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto] [colecao_no_lugar_de_objeto]` | confere | {"ids": ["contrato-produto", "colecao_no_lugar_de_objeto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "resposta_truncada"} |
| fonte_contem_termo_da_causa | `colecao_no_lugar_de_objeto` | **não confere** | {"termo": "resposta_truncada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids tra-8 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1180 | 1 | entrada | programa | ao_vivo | 2026-11-01T11:55:41 | caso tra-8 |
| 1181 | 2 | acao | programa | ao_vivo | 2026-11-01T11:55:41 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 120.2, "falhou": false} |
| 1182 | 3 | acao | programa | ao_vivo | 2026-11-01T11:55:41 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 8.8, "falhou": false} |
| 1183 | 4 | acao | programa | ao_vivo | 2026-11-01T11:55:41 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 1.8, "falhou": true} |
| 1184 | 5 | interceptacao | programa | ao_vivo | 2026-11-01T11:55:41 | GET /api/produtos 200 |
| 1185 | 6 | verificacao | verificacao | ao_vivo | 2026-11-01T11:55:41 | conferencia_do_roteiro: nao_confere |
| 1186 | 7 | poda | programa | ao_vivo | 2026-11-01T11:55:41 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1187 | 8 | poda | programa | ao_vivo | 2026-11-01T11:55:41 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1188 | 9 | candidatos | programa | ao_vivo | 2026-11-01T11:55:41 | 3 de 40 verbetes entregues |
| 1189 | 10 | prompt | programa | ao_vivo | 2026-11-01T11:55:41 | {"etapa": "diagnostico", "sha": "70fb2bccfa3bff25", "prompt_sha256": "70fb2bccfa3b", "chars": 5652, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1191 | 11 | inferencia | programa | ao_vivo | 2026-11-01T11:55:41 | diagnostico: 17,6 s |
| 1192 | 12 | declaracao | modelo | ao_vivo | 2026-11-01T11:55:41 | causa_raiz: `resposta_truncada` |
| 1193 | 13 | declaracao | modelo | ao_vivo | 2026-11-01T11:55:41 | campo: `nenhum` |
| 1194 | 14 | declaracao | modelo | ao_vivo | 2026-11-01T11:55:41 | impacto: `A interface web exibe menos produtos do que o esperado, causando uma experiência descontinuada para o usuário.` |
| 1195 | 15 | declaracao | modelo | ao_vivo | 2026-11-01T11:55:41 | fonte: `[contrato-produto] [colecao_no_lugar_de_objeto]` |
| 1196 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T11:55:41 | fonte_citada: `contrato-produto` |
| 1197 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T11:55:41 | fonte_citada: `colecao_no_lugar_de_objeto` |
| 1198 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T11:55:41 | quatro_linhas_presentes: confere |
| 1199 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T11:55:41 | rotulo_no_conjunto: confere |
| 1200 | 20 | verificacao | verificacao | ao_vivo | 2026-11-01T11:55:41 | fonte_existe_na_biblioteca: confere |
| 1201 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T11:55:41 | fonte_existe_na_biblioteca: confere |
| 1202 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T11:55:41 | fonte_estava_no_contexto: confere |
| 1203 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T11:55:41 | fonte_estava_no_contexto: confere |
| 1204 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T11:55:41 | campo_existe_no_caso: nao_se_aplica |
| 1205 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T11:55:41 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 1206 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T11:55:41 | notas_nos_verbetes_citados: informativo |
| 1207 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T11:55:41 | impacto: nao_verificavel |
| 1208 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T11:55:41 | fonte_formato_valido: confere |
| 1209 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T11:55:41 | fonte_contem_termo_da_causa: nao_confere |
| 1210 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T11:55:41 | fonte_contem_termo_da_causa: nao_confere |
| 1211 | 31 | decisao | programa | ao_vivo | 2026-11-01T11:55:41 | diagnostico: escolha resposta_truncada; divergência sim |

</details>

Nós de decisão:

- evento 1211, `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido; evidência: evento 1187 (sinal_em_codigo), evento 1186 (arvore_podada), evento 1184 (corpo_http), evento 1188 (verbete_entregue, entidade-produto), evento 1188 (verbete_entregue, colecao_no_lugar_de_objeto), evento 1188 (verbete_entregue, contrato-produto), evento 1191 (resposta), evento 1196 (verbete_citado, contrato-produto), evento 1197 (verbete_citado, colecao_no_lugar_de_objeto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, colecao_no_lugar_de_objeto, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1180 a 1211 da trilha; hash dos eventos deste caso: `5c0fa2be64a1dbcf`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
