<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-14`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/sin-14@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `estrutura_aninhada_divergente` · **CAMPO:** `imagem` · selo de probabilidade: **medio** (p = 0,99)

**IMPACTO (declarado):** `A interface exibe um título de imagem sem exibi-la, causando uma experiência de usuário incompleta.`

Justificativa (gerada por molde): O agente respondeu estrutura_aninhada_divergente no campo imagem porque o sinal imagem: esperado imagem, recebido imagem_v2 está presente na resposta HTTP e os verbetes estrutura_aninhada_divergente, contagem_inconsistente, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,01. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 944): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 179}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 946): regras diff_contra_contrato; antes {"chars": 2110}, depois {"chars": 33}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| imagem | imagem | imagem_v2 |

Trecho podado (hash `b2042fcbcc75423a`):

```text
{"imagem_v2": "picanha_alho.jpg"}
```

Interceptação (evento 940): `GET /api/produtos` status 200; corpo `58a3465f7f2815fd`, árvore `None`.

## 3. Contraste com a segunda causa

estrutura_aninhada_divergente e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 0,99 contra 0,01; verbete(s) na evidência: estrutura_aninhada_divergente, contagem_inconsistente, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| estrutura_aninhada_divergente | 0,99 | sim |
| colecao_no_lugar_de_objeto | 0,01 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| contagem_inconsistente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| codificacao_incorreta | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[estrutura_aninhada_divergente]`; verbetes citados: `estrutura_aninhada_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `estrutura_aninhada_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `estrutura_aninhada_divergente` | confere | contexto: `estrutura_aninhada_divergente`, `contagem_inconsistente`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `estrutura_aninhada_divergente` | confere | verbetes: `estrutura_aninhada_divergente`, `contagem_inconsistente`, `colecao_no_lugar_de_objeto` |
| fonte_formato_valido | `[estrutura_aninhada_divergente]` | confere | {"ids": ["estrutura_aninhada_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `estrutura_aninhada_divergente` | confere | {"termo": "estrutura_aninhada_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `imagem` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids sin-14 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 933 | 1 | entrada | programa | ao_vivo | 2026-11-01T11:45:25 | caso sin-14 |
| 934 | 2 | acao | programa | ao_vivo | 2026-11-01T11:45:26 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 133.8, "falhou": false} |
| 935 | 3 | acao | programa | ao_vivo | 2026-11-01T11:45:26 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 5.5, "falhou": false} |
| 936 | 4 | acao | programa | ao_vivo | 2026-11-01T11:45:26 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 1.8, "falhou": false} |
| 937 | 5 | acao | programa | ao_vivo | 2026-11-01T11:45:26 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 4.0, "falhou": false} |
| 938 | 6 | acao | programa | ao_vivo | 2026-11-01T11:45:26 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.0, "falhou": false} |
| 940 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T11:45:26 | GET /api/produtos 200 |
| 941 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T11:45:26 | conferencia_do_roteiro: confere |
| 942 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T11:45:26 | conferencia_do_roteiro: confere |
| 943 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T11:45:26 | conferencia_do_roteiro: confere |
| 944 | 11 | poda | programa | ao_vivo | 2026-11-01T11:45:26 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 946 | 12 | poda | programa | ao_vivo | 2026-11-01T11:45:26 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 947 | 13 | candidatos | programa | ao_vivo | 2026-11-01T11:45:26 | 3 de 40 verbetes entregues |
| 949 | 14 | prompt | programa | ao_vivo | 2026-11-01T11:45:26 | {"etapa": "diagnostico", "sha": "e8c764796b987c9d", "prompt_sha256": "e8c764796b98", "chars": 5463, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 951 | 15 | inferencia | programa | ao_vivo | 2026-11-01T11:45:26 | diagnostico: 96,2 s |
| 952 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T11:45:26 | causa_raiz: `estrutura_aninhada_divergente` |
| 953 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T11:45:26 | campo: `imagem` |
| 954 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T11:45:26 | impacto: `A interface exibe um título de imagem sem exibi-la, causando uma experiência de usuário incompleta.` |
| 955 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T11:45:26 | fonte: `[estrutura_aninhada_divergente]` |
| 956 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T11:45:26 | fonte_citada: `estrutura_aninhada_divergente` |
| 957 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T11:45:26 | quatro_linhas_presentes: confere |
| 958 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T11:45:26 | rotulo_no_conjunto: confere |
| 959 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T11:45:26 | fonte_existe_na_biblioteca: confere |
| 960 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T11:45:26 | fonte_estava_no_contexto: confere |
| 961 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T11:45:26 | campo_existe_no_caso: confere |
| 962 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T11:45:26 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 963 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T11:45:26 | notas_nos_verbetes_citados: informativo |
| 964 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T11:45:26 | impacto: nao_verificavel |
| 965 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T11:45:26 | fonte_formato_valido: confere |
| 966 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T11:45:26 | fonte_contem_termo_da_causa: confere |
| 967 | 31 | decisao | programa | ao_vivo | 2026-11-01T11:45:26 | diagnostico: escolha estrutura_aninhada_divergente; divergência não |

</details>

Nós de decisão:

- evento 967, `diagnostico`: escolha `estrutura_aninhada_divergente`; resultado rotulo_emitido; evidência: evento 946 (sinal_em_codigo), evento 944 (arvore_podada), evento 940 (corpo_http), evento 947 (verbete_entregue, estrutura_aninhada_divergente), evento 947 (verbete_entregue, contagem_inconsistente), evento 947 (verbete_entregue, colecao_no_lugar_de_objeto), evento 951 (resposta), evento 956 (verbete_citado, estrutura_aninhada_divergente); divergência: não; falha: nenhuma; prov.used: estrutura_aninhada_divergente, contagem_inconsistente, colecao_no_lugar_de_objeto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 933 a 967 da trilha; hash dos eventos deste caso: `ee003aa43e696553`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
