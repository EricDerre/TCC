<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-19`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/run-19@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `id` · selo de probabilidade: **baixo** (p = 0,39)

**IMPACTO (declarado):** `O usuário vê uma lista de produtos em vez de um único produto detalhado.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto no campo id porque o sinal tempo_ms: esperado 17 ms (referência em modo normal), recebido 2013 ms está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, valor_fora_do_dominio estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,41. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,39); trate como hipótese e confira o campo id antes de agir.

## 2. Evidência

Poda de `arvore` (evento 2189): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 197}, depois {"linhas": 42}.

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

Poda de `corpo_http` (evento 2190): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 161}, depois {"chars": 174}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tempo_ms | 17 ms (referência em modo normal) | 2013 ms |

Trecho podado (hash `b78f8a85ed458c1a`):

```text
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 2184): `GET /api/produtos` status 200; corpo `4b1bdd056e7a8c3b`, árvore `None`.

Interceptação (evento 2185): `GET /api/produtos/1` status 200; corpo `b5a0d0b69ce86861`, árvore `None`.

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não tipo_divergente: a escolha tem probabilidade 0,39 contra 0,41; verbete(s) na evidência: entidade-produto, contrato-produto, valor_fora_do_dominio

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,41 |  |
| colecao_no_lugar_de_objeto | 0,39 | sim |
| campo_ausente | 0,10 |  |
| campo_renomeado | 0,10 |  |
| tempo_de_resposta_excedido | 0,06 |  |
| resposta_truncada | 0,01 |  |
| estrutura_aninhada_divergente | 0,01 |  |
| formato_de_data_divergente | 0,01 |  |
| valor_fora_do_dominio | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `valor_fora_do_dominio` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids run-19 --k 3`

## 6. Árvore completa

<details><summary>34 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2176 | 1 | entrada | programa | ao_vivo | 2026-11-01T15:30:14 | caso run-19 |
| 2177 | 2 | acao | programa | ao_vivo | 2026-11-01T15:30:46 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 115.4, "falhou": false} |
| 2178 | 3 | acao | programa | ao_vivo | 2026-11-01T15:30:46 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 28513.1, "falhou": false |
| 2179 | 4 | acao | programa | ao_vivo | 2026-11-01T15:30:46 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 1.8, "falhou": false} |
| 2180 | 5 | acao | programa | ao_vivo | 2026-11-01T15:30:46 | {"passo": 4, "acao": "clicar", "seletor": "#produtos-api-grid .saiba-mais[data-id='1']", "url": null, "tempo_ms": 23.1, "falhou": false} |
| 2181 | 6 | acao | programa | ao_vivo | 2026-11-01T15:30:46 | {"passo": 5, "acao": "esperar", "seletor": "#modalDetalhe", "url": null, "tempo_ms": 2404.7, "falhou": false} |
| 2182 | 7 | acao | programa | ao_vivo | 2026-11-01T15:30:46 | {"passo": 6, "acao": "conferir", "seletor": "#modalDetalheTitulo", "url": null, "tempo_ms": 3.5, "falhou": false} |
| 2183 | 8 | acao | programa | ao_vivo | 2026-11-01T15:30:46 | {"passo": 7, "acao": "conferir", "seletor": "#modalDetalheCorpo", "url": null, "tempo_ms": 4.8, "falhou": false} |
| 2184 | 9 | interceptacao | programa | ao_vivo | 2026-11-01T15:30:46 | GET /api/produtos 200 |
| 2185 | 10 | interceptacao | programa | ao_vivo | 2026-11-01T15:30:46 | GET /api/produtos/1 200 |
| 2186 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T15:30:46 | conferencia_do_roteiro: confere |
| 2187 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T15:30:46 | conferencia_do_roteiro: confere |
| 2188 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T15:30:46 | conferencia_do_roteiro: confere |
| 2189 | 14 | poda | programa | ao_vivo | 2026-11-01T15:30:46 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 2190 | 15 | poda | programa | ao_vivo | 2026-11-01T15:30:46 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 2191 | 16 | candidatos | programa | ao_vivo | 2026-11-01T15:30:46 | 3 de 40 verbetes entregues |
| 2193 | 17 | prompt | programa | ao_vivo | 2026-11-01T15:30:46 | {"etapa": "diagnostico", "sha": "04cef37f6652a5a1", "prompt_sha256": "04cef37f6652", "chars": 5650, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2195 | 18 | inferencia | programa | ao_vivo | 2026-11-01T15:30:46 | diagnostico: 77,6 s |
| 2196 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T15:30:46 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 2197 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T15:30:46 | campo: `id` |
| 2198 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T15:30:46 | impacto: `O usuário vê uma lista de produtos em vez de um único produto detalhado.` |
| 2199 | 22 | declaracao | modelo | ao_vivo | 2026-11-01T15:30:46 | fonte: `[contrato-produto]` |
| 2200 | 23 | declaracao | modelo | ao_vivo | 2026-11-01T15:30:46 | fonte_citada: `contrato-produto` |
| 2201 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T15:30:46 | quatro_linhas_presentes: confere |
| 2202 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T15:30:46 | rotulo_no_conjunto: confere |
| 2203 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T15:30:46 | fonte_existe_na_biblioteca: confere |
| 2204 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T15:30:46 | fonte_estava_no_contexto: confere |
| 2205 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T15:30:46 | campo_existe_no_caso: confere |
| 2206 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T15:30:46 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2207 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T15:30:46 | notas_nos_verbetes_citados: informativo |
| 2208 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T15:30:46 | impacto: nao_verificavel |
| 2209 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T15:30:46 | fonte_formato_valido: confere |
| 2210 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T15:30:46 | fonte_contem_termo_da_causa: nao_confere |
| 2211 | 34 | decisao | programa | ao_vivo | 2026-11-01T15:30:46 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 2211, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 2190 (sinal_em_codigo), evento 2189 (arvore_podada), evento 2185 (corpo_http), evento 2191 (verbete_entregue, entidade-produto), evento 2191 (verbete_entregue, contrato-produto), evento 2191 (verbete_entregue, valor_fora_do_dominio), evento 2195 (resposta), evento 2200 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, valor_fora_do_dominio (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2176 a 2211 da trilha; hash dos eventos deste caso: `1a3cd2726d73fcaa`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
