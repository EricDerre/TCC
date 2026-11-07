<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-25`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/tra-25@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `resposta_truncada` · **CAMPO:** `id` · selo de probabilidade: **baixo** (p = 0,83) · **CONFLITO**: nenhum verbete entregue trata da causa respondida resposta_truncada

**IMPACTO (declarado):** `O usuário vê uma lista com um item a menos, refletindo a contagem inconsistente na interface.`

Justificativa (gerada por molde): O agente respondeu resposta_truncada no campo id porque o sinal itens: esperado 14 itens (referência em modo normal), recebido falta o id 14 ("Abacaxi na Brasa") está presente na resposta HTTP e os verbetes entidade-produto, contagem_inconsistente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, contagem_inconsistente, ficou com probabilidade 0,16. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida resposta_truncada. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,83); trate como hipótese e confira o campo id antes de agir.

## 2. Evidência

Poda de `arvore` (evento 1181): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 183}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 1183): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 1928}, depois {"chars": 277}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| itens | 14 itens (referência em modo normal) | falta o id 14 ("Abacaxi na Brasa") |

Trecho podado (hash `9675592a8385ee52`):

```text
lista com 13 itens (referência em modo normal: 14); falta o id 14 ("Abacaxi na Brasa"); primeiro item: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 1178): `GET /api/produtos` status 200; corpo `4f6d409f5a92ce2d`, árvore `None`.

## 3. Contraste com a segunda causa

resposta_truncada e não contagem_inconsistente: a escolha tem probabilidade 0,83 contra 0,16; verbete(s) na evidência: entidade-produto, contagem_inconsistente, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| resposta_truncada | 0,83 | sim |
| contagem_inconsistente | 0,16 |  |
| colecao_no_lugar_de_objeto | 0,01 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contagem_inconsistente]`; verbetes citados: `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `entidade-produto`, `contagem_inconsistente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contagem_inconsistente]` | confere | {"ids": ["contagem_inconsistente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | **não confere** | {"termo": "resposta_truncada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids tra-25 --k 3`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1173 | 1 | entrada | programa | ao_vivo | 2026-11-06T12:12:07 | caso tra-25 |
| 1174 | 2 | acao | programa | ao_vivo | 2026-11-06T12:12:07 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 91.3, "falhou": false} |
| 1175 | 3 | acao | programa | ao_vivo | 2026-11-06T12:12:07 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 7.5, "falhou": false} |
| 1176 | 4 | acao | programa | ao_vivo | 2026-11-06T12:12:07 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 1.8, "falhou": true} |
| 1178 | 5 | interceptacao | programa | ao_vivo | 2026-11-06T12:12:07 | GET /api/produtos 200 |
| 1179 | 6 | verificacao | verificacao | ao_vivo | 2026-11-06T12:12:07 | conferencia_do_roteiro: nao_confere |
| 1181 | 7 | poda | programa | ao_vivo | 2026-11-06T12:12:07 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1183 | 8 | poda | programa | ao_vivo | 2026-11-06T12:12:07 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1184 | 9 | candidatos | programa | ao_vivo | 2026-11-06T12:12:07 | 3 de 39 verbetes entregues |
| 1186 | 10 | prompt | programa | ao_vivo | 2026-11-06T12:12:07 | {"etapa": "diagnostico", "sha": "d44bd58b206399e2", "prompt_sha256": "d44bd58b2063", "chars": 3913, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1188 | 11 | inferencia | programa | ao_vivo | 2026-11-06T12:12:07 | diagnostico: 67,4 s |
| 1189 | 12 | declaracao | modelo | ao_vivo | 2026-11-06T12:12:07 | causa_raiz: `resposta_truncada` |
| 1190 | 13 | declaracao | modelo | ao_vivo | 2026-11-06T12:12:07 | campo: `id` |
| 1191 | 14 | declaracao | modelo | ao_vivo | 2026-11-06T12:12:07 | impacto: `O usuário vê uma lista com um item a menos, refletindo a contagem inconsistente na interface.` |
| 1192 | 15 | declaracao | modelo | ao_vivo | 2026-11-06T12:12:07 | fonte: `[contagem_inconsistente]` |
| 1193 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T12:12:07 | fonte_citada: `contagem_inconsistente` |
| 1194 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T12:12:07 | quatro_linhas_presentes: confere |
| 1195 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T12:12:07 | rotulo_no_conjunto: confere |
| 1196 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T12:12:07 | fonte_existe_na_biblioteca: confere |
| 1197 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T12:12:07 | fonte_estava_no_contexto: confere |
| 1198 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T12:12:07 | campo_existe_no_caso: confere |
| 1199 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T12:12:07 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 1200 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T12:12:07 | notas_nos_verbetes_citados: informativo |
| 1201 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T12:12:07 | impacto: nao_verificavel |
| 1202 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T12:12:07 | fonte_formato_valido: confere |
| 1203 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T12:12:07 | fonte_contem_termo_da_causa: nao_confere |
| 1204 | 27 | decisao | programa | ao_vivo | 2026-11-06T12:12:07 | diagnostico: escolha resposta_truncada; divergência sim |

</details>

Nós de decisão:

- evento 1204, `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido; evidência: evento 1183 (sinal_em_codigo), evento 1181 (arvore_podada), evento 1178 (corpo_http), evento 1184 (verbete_entregue, entidade-produto), evento 1184 (verbete_entregue, contagem_inconsistente), evento 1184 (verbete_entregue, contrato-produto), evento 1188 (resposta), evento 1193 (verbete_citado, contagem_inconsistente); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contagem_inconsistente, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1173 a 1204 da trilha; hash dos eventos deste caso: `622fdbb9c7de7118`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
