<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-8`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/semt-8@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `nulo_inesperado` · **CAMPO:** `preco` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê um preço nulo na interface, o que pode causar confusão e desinformação.`

Justificativa (gerada por molde): O agente respondeu nulo_inesperado no campo preco porque o sinal preco: esperado numero, recebido nulo está presente na resposta HTTP e os verbetes nulo_inesperado, contrato-produto, entidade-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 972): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `95567b9d021da4fd`):

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
      button "R$ 0,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 0,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "R$ 0,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 974): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2070}, depois {"chars": 15}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | numero | nulo |
| preco | 89.9 (referência em modo normal) | null em 14 itens |

Trecho podado (hash `d2144c0056fc65c7`):

```text
{"preco": null}
```

Interceptação (evento 967): `GET /api/produtos` status 200; corpo `8d871a2a7b69d75c`, árvore `None`.

## 3. Contraste com a segunda causa

nulo_inesperado e não tipo_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: nulo_inesperado, contrato-produto, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| nulo_inesperado | 1,00 | sim |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
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

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids semt-8 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 960 | 1 | entrada | programa | ao_vivo | 2026-11-05T19:16:06 | caso semt-8 |
| 961 | 2 | acao | programa | ao_vivo | 2026-11-05T19:16:06 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 108.5, "falhou": false} |
| 962 | 3 | acao | programa | ao_vivo | 2026-11-05T19:16:06 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 7.2, "falhou": false} |
| 963 | 4 | acao | programa | ao_vivo | 2026-11-05T19:16:06 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.5, "falhou": false} |
| 964 | 5 | acao | programa | ao_vivo | 2026-11-05T19:16:06 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 4.5, "falhou": false} |
| 965 | 6 | acao | programa | ao_vivo | 2026-11-05T19:16:06 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.6, "falhou": false} |
| 967 | 7 | interceptacao | programa | ao_vivo | 2026-11-05T19:16:06 | GET /api/produtos 200 |
| 968 | 8 | verificacao | verificacao | ao_vivo | 2026-11-05T19:16:06 | conferencia_do_roteiro: confere |
| 969 | 9 | verificacao | verificacao | ao_vivo | 2026-11-05T19:16:06 | conferencia_do_roteiro: confere |
| 970 | 10 | verificacao | verificacao | ao_vivo | 2026-11-05T19:16:06 | conferencia_do_roteiro: confere |
| 972 | 11 | poda | programa | ao_vivo | 2026-11-05T19:16:06 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 974 | 12 | poda | programa | ao_vivo | 2026-11-05T19:16:06 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 975 | 13 | candidatos | programa | ao_vivo | 2026-11-05T19:16:06 | 3 de 39 verbetes entregues |
| 977 | 14 | prompt | programa | ao_vivo | 2026-11-05T19:16:06 | {"etapa": "diagnostico", "sha": "8c493f39d1299d33", "prompt_sha256": "8c493f39d129", "chars": 3389, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 979 | 15 | inferencia | programa | ao_vivo | 2026-11-05T19:16:06 | diagnostico: 67,1 s |
| 980 | 16 | declaracao | modelo | ao_vivo | 2026-11-05T19:16:06 | causa_raiz: `nulo_inesperado` |
| 981 | 17 | declaracao | modelo | ao_vivo | 2026-11-05T19:16:06 | campo: `preco` |
| 982 | 18 | declaracao | modelo | ao_vivo | 2026-11-05T19:16:06 | impacto: `O usuário vê um preço nulo na interface, o que pode causar confusão e desinformação.` |
| 983 | 19 | declaracao | modelo | ao_vivo | 2026-11-05T19:16:06 | fonte: `[nulo_inesperado]` |
| 984 | 20 | declaracao | modelo | ao_vivo | 2026-11-05T19:16:06 | fonte_citada: `nulo_inesperado` |
| 985 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T19:16:06 | quatro_linhas_presentes: confere |
| 986 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T19:16:06 | rotulo_no_conjunto: confere |
| 987 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T19:16:06 | fonte_existe_na_biblioteca: confere |
| 988 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T19:16:06 | fonte_estava_no_contexto: confere |
| 989 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T19:16:06 | campo_existe_no_caso: confere |
| 990 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T19:16:06 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 991 | 27 | verificacao | verificacao | ao_vivo | 2026-11-05T19:16:06 | notas_nos_verbetes_citados: informativo |
| 992 | 28 | verificacao | verificacao | ao_vivo | 2026-11-05T19:16:06 | impacto: nao_verificavel |
| 993 | 29 | verificacao | verificacao | ao_vivo | 2026-11-05T19:16:06 | fonte_formato_valido: confere |
| 994 | 30 | verificacao | verificacao | ao_vivo | 2026-11-05T19:16:06 | fonte_contem_termo_da_causa: confere |
| 995 | 31 | decisao | programa | ao_vivo | 2026-11-05T19:16:06 | diagnostico: escolha nulo_inesperado; divergência não |

</details>

Nós de decisão:

- evento 995, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 974 (sinal_em_codigo), evento 972 (arvore_podada), evento 967 (corpo_http), evento 975 (verbete_entregue, nulo_inesperado), evento 975 (verbete_entregue, contrato-produto), evento 975 (verbete_entregue, entidade-produto), evento 979 (resposta), evento 984 (verbete_citado, nulo_inesperado); divergência: não; falha: nenhuma; prov.used: nulo_inesperado, contrato-produto, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 960 a 995 da trilha; hash dos eventos deste caso: `87a31e00c382f0bd`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
