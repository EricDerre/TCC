<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `contrato-malformed_json#1`: o que o agente fez, declarou e conferiu

Trilha `fase4_ensaio/qwen2.5_7b/contrato-malformed_json#1`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `resposta_truncada` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,96)

**IMPACTO (declarado):** `A interface exibe uma mensagem de erro e falta conteúdo de produtos, enquanto o usuário espera ver 14 cartões de produtos.`

Justificativa (gerada por molde): O agente respondeu resposta_truncada porque o sinal esperado JSON completo e válido, recebido corpo truncado está presente na resposta HTTP e os verbetes contagem_inconsistente, colecao_no_lugar_de_objeto, corpo_vazio estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,04. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 15): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 54}, depois {"linhas": 21}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 22 linha(s) da referência | 4 linha(s) novas |

Trecho podado (hash `c6422e71024439c5`):

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
    text "Erro ao carregar produtos da CobaiaAPI: Unterminated string in JSON at position 47 (line 1 column 48)"
    text "O melhor churrasco da Zona Leste"
    text "Av. Itaquera, 8266 - Itaquera - São Paulo - SP - CEP: 08295000  (11) 2185-9200 ✉"
    link "contato@churrasdafornalha.com.br" href="mailto:contato@churrasdafornalha.com.br?subject=Contato do Site&cc=matheuscs006@gmail.com"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 17): regras diff_contra_contrato; antes {"chars": 47}, depois {"chars": 50}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo truncado |

Trecho podado (hash `b818f94cbe080e90`):

```text
...[{"id": 1, "nome": "resposta truncada de propos
```

Interceptação (evento 12): `GET /api/produtos` status 200; corpo `8d7d3410d730489f`, árvore `None`.

## 3. Contraste com a segunda causa

resposta_truncada e não corpo_nao_e_json: a escolha tem probabilidade 0,96 contra 0,04; verbete(s) na evidência: contagem_inconsistente, colecao_no_lugar_de_objeto, corpo_vazio

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| resposta_truncada | 0,96 | sim |
| corpo_nao_e_json | 0,04 |  |
| corpo_vazio | 0,04 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[corpo_vazio], [contagem_inconsistente]`; verbetes citados: `corpo_vazio`, `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `corpo_vazio` | confere |  |
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `corpo_vazio` | confere | contexto: `contagem_inconsistente`, `colecao_no_lugar_de_objeto`, `corpo_vazio` |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `contagem_inconsistente`, `colecao_no_lugar_de_objeto`, `corpo_vazio` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | confere | verbetes: `corpo_vazio` |
| fonte_formato_valido | `[corpo_vazio], [contagem_inconsistente]` | confere | {"ids": ["corpo_vazio", "contagem_inconsistente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `corpo_vazio` | **não confere** | {"termo": "resposta_truncada"} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | **não confere** | {"termo": "resposta_truncada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_reexec --repeticoes 1`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 7 | 1 | entrada | programa | ao_vivo | 2026-11-04T20:19:50 | caso contrato-malformed_json#1 |
| 8 | 2 | acao | programa | ao_vivo | 2026-11-04T20:19:50 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 99.8, "falhou": false} |
| 9 | 3 | acao | programa | ao_vivo | 2026-11-04T20:19:50 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 5.4, "falhou": false} |
| 10 | 4 | acao | programa | ao_vivo | 2026-11-04T20:19:50 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 1.5, "falhou": true} |
| 12 | 5 | interceptacao | programa | ao_vivo | 2026-11-04T20:19:50 | GET /api/produtos 200 |
| 13 | 6 | verificacao | verificacao | ao_vivo | 2026-11-04T20:19:50 | conferencia_do_roteiro: nao_confere |
| 15 | 7 | poda | programa | ao_vivo | 2026-11-04T20:19:50 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 17 | 8 | poda | programa | ao_vivo | 2026-11-04T20:19:50 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 18 | 9 | candidatos | programa | ao_vivo | 2026-11-04T20:19:50 | 3 de 39 verbetes entregues |
| 20 | 10 | prompt | programa | ao_vivo | 2026-11-04T20:19:50 | {"etapa": "diagnostico", "sha": "e7abce593fe007f4", "prompt_sha256": "e7abce593fe0", "chars": 5424, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 22 | 11 | inferencia | programa | ao_vivo | 2026-11-04T20:19:50 | diagnostico: 118,4 s |
| 23 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T20:19:50 | causa_raiz: `resposta_truncada` |
| 24 | 13 | declaracao | modelo | ao_vivo | 2026-11-04T20:19:50 | campo: `nenhum` |
| 25 | 14 | declaracao | modelo | ao_vivo | 2026-11-04T20:19:50 | impacto: `A interface exibe uma mensagem de erro e falta conteúdo de produtos, enquanto o usuário espera ver 14 cartões de produtos.` |
| 26 | 15 | declaracao | modelo | ao_vivo | 2026-11-04T20:19:50 | fonte: `[corpo_vazio], [contagem_inconsistente]` |
| 27 | 16 | declaracao | modelo | ao_vivo | 2026-11-04T20:19:50 | fonte_citada: `corpo_vazio` |
| 28 | 17 | declaracao | modelo | ao_vivo | 2026-11-04T20:19:50 | fonte_citada: `contagem_inconsistente` |
| 29 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T20:19:50 | quatro_linhas_presentes: confere |
| 30 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T20:19:50 | rotulo_no_conjunto: confere |
| 31 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T20:19:50 | fonte_existe_na_biblioteca: confere |
| 32 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T20:19:50 | fonte_existe_na_biblioteca: confere |
| 33 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T20:19:50 | fonte_estava_no_contexto: confere |
| 34 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T20:19:50 | fonte_estava_no_contexto: confere |
| 35 | 24 | verificacao | verificacao | ao_vivo | 2026-11-04T20:19:50 | campo_existe_no_caso: nao_se_aplica |
| 36 | 25 | verificacao | verificacao | ao_vivo | 2026-11-04T20:19:50 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 37 | 26 | verificacao | verificacao | ao_vivo | 2026-11-04T20:19:50 | notas_nos_verbetes_citados: informativo |
| 38 | 27 | verificacao | verificacao | ao_vivo | 2026-11-04T20:19:50 | impacto: nao_verificavel |
| 39 | 28 | verificacao | verificacao | ao_vivo | 2026-11-04T20:19:50 | fonte_formato_valido: confere |
| 40 | 29 | verificacao | verificacao | ao_vivo | 2026-11-04T20:19:50 | fonte_contem_termo_da_causa: nao_confere |
| 41 | 30 | verificacao | verificacao | ao_vivo | 2026-11-04T20:19:50 | fonte_contem_termo_da_causa: nao_confere |
| 42 | 31 | decisao | programa | ao_vivo | 2026-11-04T20:19:50 | diagnostico: escolha resposta_truncada; divergência não |

</details>

Nós de decisão:

- evento 42, `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido; evidência: evento 17 (sinal_em_codigo), evento 15 (arvore_podada), evento 12 (corpo_http), evento 18 (verbete_entregue, contagem_inconsistente), evento 18 (verbete_entregue, colecao_no_lugar_de_objeto), evento 18 (verbete_entregue, corpo_vazio), evento 22 (resposta), evento 27 (verbete_citado, corpo_vazio), evento 28 (verbete_citado, contagem_inconsistente); divergência: não; falha: nenhuma; prov.used: contagem_inconsistente, colecao_no_lugar_de_objeto, corpo_vazio (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 7 a 42 da trilha; hash dos eventos deste caso: `79717a7b77245fc5`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
