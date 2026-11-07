<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-23`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/lex-23@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `corpo_vazio` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `A tela exibiu uma mensagem de erro indicando que os produtos não puderam ser carregados, e o usuário não viu nenhum produto listado, embora esperasse ver 14 elementos.`

Justificativa (gerada por molde): O agente respondeu corpo_vazio porque o sinal esperado JSON completo e válido, recebido corpo vazio está presente na resposta HTTP e os verbetes corpo_vazio, colecao_no_lugar_de_objeto, tempo_de_resposta_excedido estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 78): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 54}, depois {"linhas": 21}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 25 linha(s) da referência | 4 linha(s) novas |

Trecho podado (hash `dc4c8bca22a3d92b`):

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
    text "Erro ao carregar produtos da CobaiaAPI: Failed to execute 'json' on 'Response': Unexpected end of JSON input"
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

Poda de `corpo_http` (evento 79): regras diff_contra_contrato; antes {"chars": 0}, depois {"chars": 0}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| (corpo inteiro) | JSON completo e válido | corpo vazio |

Trecho podado (hash `e3b0c44298fc1c14`):

```text

```

Interceptação (evento 75): `GET /api/produtos` status 200; corpo `e3b0c44298fc1c14`, árvore `None`.

## 3. Contraste com a segunda causa

corpo_vazio e não corpo_nao_e_json: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: corpo_vazio, colecao_no_lugar_de_objeto, tempo_de_resposta_excedido

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| corpo_vazio | 1,00 | sim |
| corpo_nao_e_json | 0,00 |  |
| resposta_truncada | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[corpo_vazio]`; verbetes citados: `corpo_vazio`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `corpo_vazio` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `corpo_vazio` | confere | contexto: `corpo_vazio`, `colecao_no_lugar_de_objeto`, `tempo_de_resposta_excedido` |
| Algum verbete do contexto trata da causa respondida | `corpo_vazio` | confere | verbetes: `corpo_vazio`, `tempo_de_resposta_excedido` |
| fonte_formato_valido | `[corpo_vazio]` | confere | {"ids": ["corpo_vazio"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `corpo_vazio` | confere | {"termo": "corpo_vazio"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids lex-23 --k 3`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 70 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:30:17 | caso lex-23 |
| 71 | 2 | acao | programa | ao_vivo | 2026-11-06T11:30:18 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 93.5, "falhou": false} |
| 72 | 3 | acao | programa | ao_vivo | 2026-11-06T11:30:18 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 9.0, "falhou": false} |
| 73 | 4 | acao | programa | ao_vivo | 2026-11-06T11:30:18 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.6, "falhou": true} |
| 75 | 5 | interceptacao | programa | ao_vivo | 2026-11-06T11:30:18 | GET /api/produtos 200 |
| 76 | 6 | verificacao | verificacao | ao_vivo | 2026-11-06T11:30:18 | conferencia_do_roteiro: nao_confere |
| 78 | 7 | poda | programa | ao_vivo | 2026-11-06T11:30:18 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 79 | 8 | poda | programa | ao_vivo | 2026-11-06T11:30:18 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 80 | 9 | candidatos | programa | ao_vivo | 2026-11-06T11:30:18 | 3 de 39 verbetes entregues |
| 82 | 10 | prompt | programa | ao_vivo | 2026-11-06T11:30:18 | {"etapa": "diagnostico", "sha": "d85153973368b5e8", "prompt_sha256": "d85153973368", "chars": 3889, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 84 | 11 | inferencia | programa | ao_vivo | 2026-11-06T11:30:18 | diagnostico: 80,8 s |
| 85 | 12 | declaracao | modelo | ao_vivo | 2026-11-06T11:30:18 | causa_raiz: `corpo_vazio` |
| 86 | 13 | declaracao | modelo | ao_vivo | 2026-11-06T11:30:18 | campo: `nenhum` |
| 87 | 14 | declaracao | modelo | ao_vivo | 2026-11-06T11:30:18 | impacto: `A tela exibiu uma mensagem de erro indicando que os produtos não puderam ser carregados, e o usuário não viu nenhum produto listado, embora esperasse ver 14 elementos.` |
| 88 | 15 | declaracao | modelo | ao_vivo | 2026-11-06T11:30:18 | fonte: `[corpo_vazio]` |
| 89 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T11:30:18 | fonte_citada: `corpo_vazio` |
| 90 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:30:18 | quatro_linhas_presentes: confere |
| 91 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:30:18 | rotulo_no_conjunto: confere |
| 92 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:30:18 | fonte_existe_na_biblioteca: confere |
| 93 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T11:30:18 | fonte_estava_no_contexto: confere |
| 94 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T11:30:18 | campo_existe_no_caso: nao_se_aplica |
| 95 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:30:18 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 96 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:30:18 | notas_nos_verbetes_citados: informativo |
| 97 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:30:18 | impacto: nao_verificavel |
| 98 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:30:18 | fonte_formato_valido: confere |
| 99 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:30:18 | fonte_contem_termo_da_causa: confere |
| 100 | 27 | decisao | programa | ao_vivo | 2026-11-06T11:30:18 | diagnostico: escolha corpo_vazio; divergência não |

</details>

Nós de decisão:

- evento 100, `diagnostico`: escolha `corpo_vazio`; resultado rotulo_emitido; evidência: evento 79 (sinal_em_codigo), evento 78 (arvore_podada), evento 75 (corpo_http), evento 80 (verbete_entregue, corpo_vazio), evento 80 (verbete_entregue, colecao_no_lugar_de_objeto), evento 80 (verbete_entregue, tempo_de_resposta_excedido), evento 84 (resposta), evento 89 (verbete_citado, corpo_vazio); divergência: não; falha: nenhuma; prov.used: corpo_vazio, colecao_no_lugar_de_objeto, tempo_de_resposta_excedido (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 70 a 100 da trilha; hash dos eventos deste caso: `4c45629ac46f13c1`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
