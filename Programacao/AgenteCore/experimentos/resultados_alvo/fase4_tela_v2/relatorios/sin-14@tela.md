<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-14`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/sin-14@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_renomeado` · **CAMPO:** `imagem` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: a FONTE cita o verbete campo_renomeado, fora do contexto entregue

**IMPACTO (declarado):** `O usuário vê cartões de produtos sem imagens, causando uma experiência visual incompleta.`

Justificativa (gerada por molde): O agente respondeu campo_renomeado no campo imagem porque o sinal imagem: esperado imagem, recebido imagem_v2 está presente na resposta HTTP e os verbetes contagem_inconsistente, estrutura_aninhada_divergente, tempo_de_resposta_excedido estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), 1 fora do contexto entregue (campo_renomeado). O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a FONTE cita o verbete campo_renomeado, fora do contexto entregue. Este nó está marcado com a falha citacao_fora_do_contexto (origem: modelo).

## 2. Evidência

Poda de `arvore` (evento 952): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 179}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 0 linha(s) da referência | 0 linha(s) novas |

Trecho podado (hash `e4870f4dbbc1b73d`):

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
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 954): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2110}, depois {"chars": 33}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| imagem | imagem | imagem_v2 |

Trecho podado (hash `b2042fcbcc75423a`):

```text
{"imagem_v2": "picanha_alho.jpg"}
```

Interceptação (evento 948): `GET /api/produtos` status 200; corpo `58a3465f7f2815fd`, árvore `None`.

## 3. Contraste com a segunda causa

campo_renomeado e não estrutura_aninhada_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contagem_inconsistente, estrutura_aninhada_divergente, tempo_de_resposta_excedido, campo_renomeado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_renomeado | 1,00 | sim |
| estrutura_aninhada_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_renomeado]`; verbetes citados: `campo_renomeado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | **não confere** | contexto: `contagem_inconsistente`, `estrutura_aninhada_divergente`, `tempo_de_resposta_excedido` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `estrutura_aninhada_divergente` |
| fonte_formato_valido | `[campo_renomeado]` | confere | {"ids": ["campo_renomeado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_renomeado` | confere | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `imagem` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids sin-14 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 941 | 1 | entrada | programa | ao_vivo | 2026-11-01T14:44:20 | caso sin-14 |
| 942 | 2 | acao | programa | ao_vivo | 2026-11-01T14:44:20 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 127.6, "falhou": false} |
| 943 | 3 | acao | programa | ao_vivo | 2026-11-01T14:44:20 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 6.7, "falhou": false} |
| 944 | 4 | acao | programa | ao_vivo | 2026-11-01T14:44:20 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 1.8, "falhou": false} |
| 945 | 5 | acao | programa | ao_vivo | 2026-11-01T14:44:20 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 5.1, "falhou": false} |
| 946 | 6 | acao | programa | ao_vivo | 2026-11-01T14:44:20 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 4.6, "falhou": false} |
| 948 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T14:44:20 | GET /api/produtos 200 |
| 949 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T14:44:20 | conferencia_do_roteiro: confere |
| 950 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T14:44:20 | conferencia_do_roteiro: confere |
| 951 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T14:44:20 | conferencia_do_roteiro: confere |
| 952 | 11 | poda | programa | ao_vivo | 2026-11-01T14:44:20 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 954 | 12 | poda | programa | ao_vivo | 2026-11-01T14:44:20 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 955 | 13 | candidatos | programa | ao_vivo | 2026-11-01T14:44:20 | 3 de 40 verbetes entregues |
| 957 | 14 | prompt | programa | ao_vivo | 2026-11-01T14:44:20 | {"etapa": "diagnostico", "sha": "4d5cc62ce127d7e7", "prompt_sha256": "4d5cc62ce127", "chars": 5328, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 959 | 15 | inferencia | programa | ao_vivo | 2026-11-01T14:44:20 | diagnostico: 90,5 s |
| 960 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T14:44:20 | causa_raiz: `campo_renomeado` |
| 961 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T14:44:20 | campo: `imagem` |
| 962 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T14:44:20 | impacto: `O usuário vê cartões de produtos sem imagens, causando uma experiência visual incompleta.` |
| 963 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T14:44:20 | fonte: `[campo_renomeado]` |
| 964 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T14:44:20 | fonte_citada: `campo_renomeado` |
| 965 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T14:44:20 | quatro_linhas_presentes: confere |
| 966 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T14:44:20 | rotulo_no_conjunto: confere |
| 967 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T14:44:20 | fonte_existe_na_biblioteca: confere |
| 968 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T14:44:20 | fonte_estava_no_contexto: nao_confere |
| 969 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T14:44:20 | campo_existe_no_caso: confere |
| 970 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T14:44:20 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 971 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T14:44:20 | notas_nos_verbetes_citados: informativo |
| 972 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T14:44:20 | impacto: nao_verificavel |
| 973 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T14:44:20 | fonte_formato_valido: confere |
| 974 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T14:44:20 | fonte_contem_termo_da_causa: confere |
| 975 | 31 | decisao | programa | ao_vivo | 2026-11-01T14:44:20 | diagnostico: escolha campo_renomeado; divergência sim |

</details>

Nós de decisão:

- evento 975, `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido; evidência: evento 954 (sinal_em_codigo), evento 952 (arvore_podada), evento 948 (corpo_http), evento 955 (verbete_entregue, contagem_inconsistente), evento 955 (verbete_entregue, estrutura_aninhada_divergente), evento 955 (verbete_entregue, tempo_de_resposta_excedido), evento 959 (resposta), evento 964 (verbete_citado, campo_renomeado); divergência: sim; falha: citacao_fora_do_contexto; prov.used: contagem_inconsistente, estrutura_aninhada_divergente, tempo_de_resposta_excedido, campo_renomeado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 941 a 975 da trilha; hash dos eventos deste caso: `4d7dbc65af3c64eb`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
