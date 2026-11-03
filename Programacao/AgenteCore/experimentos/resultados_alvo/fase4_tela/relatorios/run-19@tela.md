<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-19`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/run-19@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `preco` · selo de probabilidade: **baixo** (p = 0,32)

**IMPACTO (declarado):** `O usuário vê o preço formatado corretamente em R$ 89,90, mas o front-end não realiza a formatação do valor recebido, que é um número.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo preco porque o sinal arvore: esperado 0 linha(s) da referência, recebido 0 linha(s) novas está presente na tela e os verbetes entidade-produto, contrato-produto, campo_ausente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,32. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,32); trate como hipótese e confira o campo preco antes de agir.

## 2. Evidência

Poda de `arvore` (evento 2168): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 197}, depois {"linhas": 42}.

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

Poda de `corpo_http` (evento 2169): regras diff_contra_contrato; antes {"chars": 161}, depois {"chars": 174}.

Trecho podado (hash `b78f8a85ed458c1a`):

```text
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 2163): `GET /api/produtos` status 200; corpo `4b1bdd056e7a8c3b`, árvore `None`.

Interceptação (evento 2164): `GET /api/produtos/1` status 200; corpo `b5a0d0b69ce86861`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 0,32 contra 0,32; verbete(s) na evidência: entidade-produto, contrato-produto, campo_ausente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,32 | sim |
| campo_ausente | 0,32 |  |
| campo_renomeado | 0,32 |  |
| colecao_no_lugar_de_objeto | 0,24 |  |
| corpo_nao_e_json | 0,03 |  |
| corpo_vazio | 0,03 |  |
| resposta_truncada | 0,03 |  |
| formato_de_data_divergente | 0,03 |  |
| estrutura_aninhada_divergente | 0,01 |  |
| valor_fora_do_dominio | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `contrato-produto` |
| fonte_formato_valido | `[entidade-produto], [contrato-produto]` | confere | {"ids": ["entidade-produto", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids run-19 --k 3`

## 6. Árvore completa

<details><summary>38 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2155 | 1 | entrada | programa | ao_vivo | 2026-11-01T12:28:49 | caso run-19 |
| 2156 | 2 | acao | programa | ao_vivo | 2026-11-01T12:29:20 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 120.5, "falhou": false} |
| 2157 | 3 | acao | programa | ao_vivo | 2026-11-01T12:29:20 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 28045.8, "falhou": false |
| 2158 | 4 | acao | programa | ao_vivo | 2026-11-01T12:29:20 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 1.9, "falhou": false} |
| 2159 | 5 | acao | programa | ao_vivo | 2026-11-01T12:29:20 | {"passo": 4, "acao": "clicar", "seletor": "#produtos-api-grid .saiba-mais[data-id='1']", "url": null, "tempo_ms": 67.5, "falhou": false} |
| 2160 | 6 | acao | programa | ao_vivo | 2026-11-01T12:29:20 | {"passo": 5, "acao": "esperar", "seletor": "#modalDetalhe", "url": null, "tempo_ms": 2399.8, "falhou": false} |
| 2161 | 7 | acao | programa | ao_vivo | 2026-11-01T12:29:20 | {"passo": 6, "acao": "conferir", "seletor": "#modalDetalheTitulo", "url": null, "tempo_ms": 3.6, "falhou": false} |
| 2162 | 8 | acao | programa | ao_vivo | 2026-11-01T12:29:20 | {"passo": 7, "acao": "conferir", "seletor": "#modalDetalheCorpo", "url": null, "tempo_ms": 6.0, "falhou": false} |
| 2163 | 9 | interceptacao | programa | ao_vivo | 2026-11-01T12:29:20 | GET /api/produtos 200 |
| 2164 | 10 | interceptacao | programa | ao_vivo | 2026-11-01T12:29:20 | GET /api/produtos/1 200 |
| 2165 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T12:29:20 | conferencia_do_roteiro: confere |
| 2166 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T12:29:20 | conferencia_do_roteiro: confere |
| 2167 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T12:29:20 | conferencia_do_roteiro: confere |
| 2168 | 14 | poda | programa | ao_vivo | 2026-11-01T12:29:20 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 2169 | 15 | poda | programa | ao_vivo | 2026-11-01T12:29:20 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2170 | 16 | candidatos | programa | ao_vivo | 2026-11-01T12:29:20 | 3 de 40 verbetes entregues |
| 2172 | 17 | prompt | programa | ao_vivo | 2026-11-01T12:29:20 | {"etapa": "diagnostico", "sha": "8f9795fd6297682d", "prompt_sha256": "8f9795fd6297", "chars": 5387, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2174 | 18 | inferencia | programa | ao_vivo | 2026-11-01T12:29:20 | diagnostico: 81,1 s |
| 2175 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T12:29:20 | causa_raiz: `tipo_divergente` |
| 2176 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T12:29:20 | campo: `preco` |
| 2177 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T12:29:20 | impacto: `O usuário vê o preço formatado corretamente em R$ 89,90, mas o front-end não realiza a formatação do valor recebido, que é um número.` |
| 2178 | 22 | declaracao | modelo | ao_vivo | 2026-11-01T12:29:20 | fonte: `[entidade-produto], [contrato-produto]` |
| 2179 | 23 | declaracao | modelo | ao_vivo | 2026-11-01T12:29:20 | fonte_citada: `entidade-produto` |
| 2180 | 24 | declaracao | modelo | ao_vivo | 2026-11-01T12:29:20 | fonte_citada: `contrato-produto` |
| 2181 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T12:29:20 | quatro_linhas_presentes: confere |
| 2182 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T12:29:20 | rotulo_no_conjunto: confere |
| 2183 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T12:29:20 | fonte_existe_na_biblioteca: confere |
| 2184 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T12:29:20 | fonte_existe_na_biblioteca: confere |
| 2185 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T12:29:20 | fonte_estava_no_contexto: confere |
| 2186 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T12:29:20 | fonte_estava_no_contexto: confere |
| 2187 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T12:29:20 | campo_existe_no_caso: confere |
| 2188 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T12:29:20 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2189 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T12:29:20 | notas_nos_verbetes_citados: informativo |
| 2190 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T12:29:20 | impacto: nao_verificavel |
| 2191 | 35 | verificacao | verificacao | ao_vivo | 2026-11-01T12:29:20 | fonte_formato_valido: confere |
| 2192 | 36 | verificacao | verificacao | ao_vivo | 2026-11-01T12:29:20 | fonte_contem_termo_da_causa: nao_confere |
| 2193 | 37 | verificacao | verificacao | ao_vivo | 2026-11-01T12:29:20 | fonte_contem_termo_da_causa: nao_confere |
| 2194 | 38 | decisao | programa | ao_vivo | 2026-11-01T12:29:20 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 2194, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 2169 (sinal_em_codigo), evento 2168 (arvore_podada), evento 2164 (corpo_http), evento 2170 (verbete_entregue, entidade-produto), evento 2170 (verbete_entregue, contrato-produto), evento 2170 (verbete_entregue, campo_ausente), evento 2174 (resposta), evento 2179 (verbete_citado, entidade-produto), evento 2180 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, campo_ausente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2155 a 2194 da trilha; hash dos eventos deste caso: `0e57ff7dff94f922`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
