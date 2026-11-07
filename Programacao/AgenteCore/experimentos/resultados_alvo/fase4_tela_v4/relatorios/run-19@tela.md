<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-19`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v4/qwen2.5_7b/run-19@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tempo_de_resposta_excedido` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,98)

**IMPACTO (declarado):** `O usuário experimentou uma resposta lenta, o que pode causar insatisfação e atrasos na experiência do usuário.`

Justificativa (gerada por molde): O agente respondeu tempo_de_resposta_excedido no campo tempo_ms porque o sinal tempo_ms: esperado 16 ms (referência em modo normal), recebido 2012 ms está presente na resposta HTTP e os verbetes tempo_de_resposta_excedido, entidade-produto, contrato-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,02. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 2091): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 197}, depois {"linhas": 42}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 0 linha(s) da referência | 0 linha(s) novas |

Trecho podado (hash `1d807eb42e97c234`):

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
  dialog
    heading "Picanha ao Alho" level=4
    text "Picanha grelhada com alho laminado na brasa"

```

Poda de `corpo_http` (evento 2092): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 161}, depois {"chars": 174}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tempo_ms | 16 ms (referência em modo normal) | 2012 ms |

Trecho podado (hash `b78f8a85ed458c1a`):

```text
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 2086): `GET /api/produtos` status 200; corpo `4b1bdd056e7a8c3b`, árvore `None`.

Interceptação (evento 2087): `GET /api/produtos/1` status 200; corpo `b5a0d0b69ce86861`, árvore `None`.

## 3. Contraste com a segunda causa

tempo_de_resposta_excedido e não tipo_divergente: a escolha tem probabilidade 0,98 contra 0,02; verbete(s) na evidência: tempo_de_resposta_excedido, entidade-produto, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tempo_de_resposta_excedido | 0,98 | sim |
| tipo_divergente | 0,02 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tempo_de_resposta_excedido]`; verbetes citados: `tempo_de_resposta_excedido`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tempo_de_resposta_excedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tempo_de_resposta_excedido` | confere | contexto: `tempo_de_resposta_excedido`, `entidade-produto`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | confere | verbetes: `tempo_de_resposta_excedido` |
| fonte_formato_valido | `[tempo_de_resposta_excedido]` | confere | {"ids": ["tempo_de_resposta_excedido"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tempo_de_resposta_excedido` | confere | {"termo": "tempo_de_resposta_excedido"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids run-19 --k 3`

## 6. Árvore completa

<details><summary>34 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2078 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:07:48 | caso run-19 |
| 2079 | 2 | acao | programa | ao_vivo | 2026-11-06T11:08:19 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 113.3, "falhou": false} |
| 2080 | 3 | acao | programa | ao_vivo | 2026-11-06T11:08:19 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 28446.9, "falhou": false |
| 2081 | 4 | acao | programa | ao_vivo | 2026-11-06T11:08:19 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.3, "falhou": false} |
| 2082 | 5 | acao | programa | ao_vivo | 2026-11-06T11:08:19 | {"passo": 4, "acao": "clicar", "seletor": "#produtos-api-grid .saiba-mais[data-id='1']", "url": null, "tempo_ms": 25.4, "falhou": false} |
| 2083 | 6 | acao | programa | ao_vivo | 2026-11-06T11:08:19 | {"passo": 5, "acao": "esperar", "seletor": "#modalDetalhe", "url": null, "tempo_ms": 2387.8, "falhou": false} |
| 2084 | 7 | acao | programa | ao_vivo | 2026-11-06T11:08:19 | {"passo": 6, "acao": "conferir", "seletor": "#modalDetalheTitulo", "url": null, "tempo_ms": 4.0, "falhou": false} |
| 2085 | 8 | acao | programa | ao_vivo | 2026-11-06T11:08:19 | {"passo": 7, "acao": "conferir", "seletor": "#modalDetalheCorpo", "url": null, "tempo_ms": 3.1, "falhou": false} |
| 2086 | 9 | interceptacao | programa | ao_vivo | 2026-11-06T11:08:19 | GET /api/produtos 200 |
| 2087 | 10 | interceptacao | programa | ao_vivo | 2026-11-06T11:08:19 | GET /api/produtos/1 200 |
| 2088 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | conferencia_do_roteiro: confere |
| 2089 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | conferencia_do_roteiro: confere |
| 2090 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | conferencia_do_roteiro: confere |
| 2091 | 14 | poda | programa | ao_vivo | 2026-11-06T11:08:19 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 2092 | 15 | poda | programa | ao_vivo | 2026-11-06T11:08:19 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 2093 | 16 | candidatos | programa | ao_vivo | 2026-11-06T11:08:19 | 3 de 39 verbetes entregues |
| 2095 | 17 | prompt | programa | ao_vivo | 2026-11-06T11:08:19 | {"etapa": "diagnostico", "sha": "ef8db820a5c980ad", "prompt_sha256": "ef8db820a5c9", "chars": 3539, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2097 | 18 | inferencia | programa | ao_vivo | 2026-11-06T11:08:19 | diagnostico: 71,2 s |
| 2098 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T11:08:19 | causa_raiz: `tempo_de_resposta_excedido` |
| 2099 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T11:08:19 | campo: `nenhum` |
| 2100 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T11:08:19 | impacto: `O usuário experimentou uma resposta lenta, o que pode causar insatisfação e atrasos na experiência do usuário.` |
| 2101 | 22 | declaracao | modelo | ao_vivo | 2026-11-06T11:08:19 | fonte: `[tempo_de_resposta_excedido]` |
| 2102 | 23 | declaracao | modelo | ao_vivo | 2026-11-06T11:08:19 | fonte_citada: `tempo_de_resposta_excedido` |
| 2103 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | quatro_linhas_presentes: confere |
| 2104 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | rotulo_no_conjunto: confere |
| 2105 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | fonte_existe_na_biblioteca: confere |
| 2106 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | fonte_estava_no_contexto: confere |
| 2107 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | campo_existe_no_caso: nao_se_aplica |
| 2108 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2109 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | notas_nos_verbetes_citados: informativo |
| 2110 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | impacto: nao_verificavel |
| 2111 | 32 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | fonte_formato_valido: confere |
| 2112 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | fonte_contem_termo_da_causa: confere |
| 2113 | 34 | decisao | programa | ao_vivo | 2026-11-06T11:08:19 | diagnostico: escolha tempo_de_resposta_excedido; divergência não |

</details>

Nós de decisão:

- evento 2113, `diagnostico`: escolha `tempo_de_resposta_excedido`; resultado rotulo_emitido; evidência: evento 2092 (sinal_em_codigo), evento 2091 (arvore_podada), evento 2087 (corpo_http), evento 2093 (verbete_entregue, tempo_de_resposta_excedido), evento 2093 (verbete_entregue, entidade-produto), evento 2093 (verbete_entregue, contrato-produto), evento 2097 (resposta), evento 2102 (verbete_citado, tempo_de_resposta_excedido); divergência: não; falha: nenhuma; prov.used: tempo_de_resposta_excedido, entidade-produto, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2078 a 2113 da trilha; hash dos eventos deste caso: `88c02123b0ed6352`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
