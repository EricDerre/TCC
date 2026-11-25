<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `contrato-malformed_json#1`: o que o agente fez, declarou e conferiu

Trilha `fase5_sondagem_frio_20261118_212709/qwen2.5_7b/contrato-malformed_json#1`; modelo `qwen2.5:7b`, Ollama 0.40.16, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `resposta_truncada` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `A interface exibiu uma tela incompleta, com 140 linhas a menos e 1 linha a mais que a referência esperada, devido à resposta da API sendo cortada.`

Justificativa (gerada por molde): O agente respondeu resposta_truncada porque o sinal esperado JSON completo e válido, recebido corpo truncado está presente na resposta HTTP e os verbetes resposta_truncada, contagem_inconsistente, entidade-produto estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 15): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 54}, depois {"linhas": 21}.

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
| (corpo inteiro) | JSON completo e válido | corpo truncado |

Trecho podado (hash `b818f94cbe080e90`):

```text
...[{"id": 1, "nome": "resposta truncada de propos
```

Interceptação (evento 12): `GET /api/produtos` status 200; corpo `8d7d3410d730489f`, árvore `None`.

## 3. Contraste com a segunda causa

resposta_truncada e não corpo_nao_e_json: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: resposta_truncada, contagem_inconsistente, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| resposta_truncada | 1,00 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[resposta_truncada]`; verbetes citados: `resposta_truncada`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `resposta_truncada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `resposta_truncada` | confere | contexto: `resposta_truncada`, `contagem_inconsistente`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | confere | verbetes: `resposta_truncada` |
| fonte_formato_valido | `[resposta_truncada]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["resposta_truncada"]} |
| fonte_contem_termo_da_causa | `resposta_truncada` | confere | {"termo": "resposta_truncada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase5_sondagem_frio_20261118_212709_reexec --repeticoes 1`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 7 | 1 | entrada | programa | ao_vivo | 2026-11-18T21:28:15 | caso contrato-malformed_json#1 |
| 8 | 2 | acao | programa | ao_vivo | 2026-11-18T21:28:16 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 90.2, "url": "produtos_api.php"} |
| 9 | 3 | acao | programa | ao_vivo | 2026-11-18T21:28:16 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 7.3, "url": null} |
| 10 | 4 | acao | programa | ao_vivo | 2026-11-18T21:28:16 | {"acao": "conferir", "falhou": true, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 1.5, "url": null} |
| 12 | 5 | interceptacao | programa | ao_vivo | 2026-11-18T21:28:16 | GET /api/produtos 200 |
| 13 | 6 | verificacao | verificacao | ao_vivo | 2026-11-18T21:28:16 | conferencia_do_roteiro: nao_confere |
| 15 | 7 | poda | programa | ao_vivo | 2026-11-18T21:28:16 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 17 | 8 | poda | programa | ao_vivo | 2026-11-18T21:28:16 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 18 | 9 | candidatos | programa | ao_vivo | 2026-11-18T21:28:16 | 3 de 39 verbetes entregues |
| 20 | 10 | prompt | programa | ao_vivo | 2026-11-18T21:28:16 | {"chars": 3938, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "23f9d2879369", "sha": "23f9d28793694e85"} |
| 22 | 11 | inferencia | programa | ao_vivo | 2026-11-18T21:28:16 | diagnostico: 75,8 s |
| 23 | 12 | declaracao | modelo | ao_vivo | 2026-11-18T21:28:16 | causa_raiz: `resposta_truncada` |
| 24 | 13 | declaracao | modelo | ao_vivo | 2026-11-18T21:28:16 | campo: `nenhum` |
| 25 | 14 | declaracao | modelo | ao_vivo | 2026-11-18T21:28:16 | impacto: `A interface exibiu uma tela incompleta, com 140 linhas a menos e 1 linha a mais que a referência esperada, devido à resposta da API sendo cortada.` |
| 26 | 15 | declaracao | modelo | ao_vivo | 2026-11-18T21:28:16 | fonte: `[resposta_truncada]` |
| 27 | 16 | declaracao | modelo | ao_vivo | 2026-11-18T21:28:16 | fonte_citada: `resposta_truncada` |
| 28 | 17 | verificacao | verificacao | ao_vivo | 2026-11-18T21:28:16 | quatro_linhas_presentes: confere |
| 29 | 18 | verificacao | verificacao | ao_vivo | 2026-11-18T21:28:16 | rotulo_no_conjunto: confere |
| 30 | 19 | verificacao | verificacao | ao_vivo | 2026-11-18T21:28:16 | fonte_existe_na_biblioteca: confere |
| 31 | 20 | verificacao | verificacao | ao_vivo | 2026-11-18T21:28:16 | fonte_estava_no_contexto: confere |
| 32 | 21 | verificacao | verificacao | ao_vivo | 2026-11-18T21:28:16 | campo_existe_no_caso: nao_se_aplica |
| 33 | 22 | verificacao | verificacao | ao_vivo | 2026-11-18T21:28:16 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 34 | 23 | verificacao | verificacao | ao_vivo | 2026-11-18T21:28:16 | notas_nos_verbetes_citados: informativo |
| 35 | 24 | verificacao | verificacao | ao_vivo | 2026-11-18T21:28:16 | impacto: nao_verificavel |
| 36 | 25 | verificacao | verificacao | ao_vivo | 2026-11-18T21:28:16 | fonte_formato_valido: confere |
| 37 | 26 | verificacao | verificacao | ao_vivo | 2026-11-18T21:28:16 | fonte_contem_termo_da_causa: confere |
| 38 | 27 | decisao | programa | ao_vivo | 2026-11-18T21:28:16 | diagnostico: escolha resposta_truncada; divergência não |

</details>

Nós de decisão:

- evento 38, `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido; evidência: evento 17 (sinal_em_codigo), evento 15 (arvore_podada), evento 12 (corpo_http), evento 18 (verbete_entregue, resposta_truncada), evento 18 (verbete_entregue, contagem_inconsistente), evento 18 (verbete_entregue, entidade-produto), evento 22 (resposta), evento 27 (verbete_citado, resposta_truncada); divergência: não; falha: nenhuma; prov.used: resposta_truncada, contagem_inconsistente, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 7 a 38 da trilha; hash dos eventos deste caso: `3ca910dfc58288f7`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
