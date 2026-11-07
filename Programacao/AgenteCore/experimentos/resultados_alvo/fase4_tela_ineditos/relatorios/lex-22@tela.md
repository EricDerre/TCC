<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-22`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/lex-22@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `corpo_nao_e_json` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,93)

**IMPACTO (declarado):** `O usuário vê uma página de erro HTML em vez de uma lista de produtos JSON, resultando em uma interface incompleta e inutilizável.`

Justificativa (gerada por molde): O agente respondeu corpo_nao_e_json porque o sinal esperado JSON completo e válido, recebido corpo nao_json está presente na resposta HTTP e os verbetes corpo_nao_e_json, erro_interno_do_servidor, mensagens-de-erro-do-codigo estavam entre os entregues ao modelo. A segunda causa, erro_interno_do_servidor, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 19): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 54}, depois {"linhas": 21}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 22 linha(s) da referência | 4 linha(s) novas |

Trecho podado (hash `a12b4b5383ead2a5`):

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
    text "Erro ao carregar produtos da CobaiaAPI: Unexpected token '<', "<html><bod"... is not valid JSON"
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

Poda de `corpo_http` (evento 20): regras diff_contra_contrato; antes {"chars": 73}, depois {"chars": 73}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| (corpo inteiro) | JSON completo e válido | corpo nao_json |

Trecho podado (hash `ceb0d510211b7efb`):

```text
<html><body><h1>Erro</h1><p>Falha ao montar a resposta.</p></body></html>
```

Interceptação (evento 16): `GET /api/produtos` status 200; corpo `ceb0d510211b7efb`, árvore `None`.

## 3. Contraste com a segunda causa

corpo_nao_e_json e não erro_interno_do_servidor: a escolha tem probabilidade 0,93 contra 0,00; verbete(s) na evidência: corpo_nao_e_json, erro_interno_do_servidor, mensagens-de-erro-do-codigo

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| corpo_nao_e_json | 0,93 | sim |
| erro_interno_do_servidor | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[corpo_nao_e_json]`; verbetes citados: `corpo_nao_e_json`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `corpo_nao_e_json` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `corpo_nao_e_json` | confere | contexto: `corpo_nao_e_json`, `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo` |
| Algum verbete do contexto trata da causa respondida | `corpo_nao_e_json` | confere | verbetes: `corpo_nao_e_json`, `erro_interno_do_servidor`, `mensagens-de-erro-do-codigo` |
| fonte_formato_valido | `[corpo_nao_e_json]` | confere | {"ids": ["corpo_nao_e_json"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `corpo_nao_e_json` | confere | {"termo": "corpo_nao_e_json"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids lex-22 --k 3`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 11 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:27:34 | caso lex-22 |
| 12 | 2 | acao | programa | ao_vivo | 2026-11-06T11:27:35 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 86.2, "falhou": false} |
| 13 | 3 | acao | programa | ao_vivo | 2026-11-06T11:27:35 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 6.9, "falhou": false} |
| 14 | 4 | acao | programa | ao_vivo | 2026-11-06T11:27:35 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.1, "falhou": true} |
| 16 | 5 | interceptacao | programa | ao_vivo | 2026-11-06T11:27:35 | GET /api/produtos 200 |
| 17 | 6 | verificacao | verificacao | ao_vivo | 2026-11-06T11:27:35 | conferencia_do_roteiro: nao_confere |
| 19 | 7 | poda | programa | ao_vivo | 2026-11-06T11:27:35 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 20 | 8 | poda | programa | ao_vivo | 2026-11-06T11:27:35 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 21 | 9 | candidatos | programa | ao_vivo | 2026-11-06T11:27:35 | 3 de 39 verbetes entregues |
| 23 | 10 | prompt | programa | ao_vivo | 2026-11-06T11:27:35 | {"etapa": "diagnostico", "sha": "c82417087d8d800c", "prompt_sha256": "c82417087d8d", "chars": 4005, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 25 | 11 | inferencia | programa | ao_vivo | 2026-11-06T11:27:35 | diagnostico: 89,8 s |
| 26 | 12 | declaracao | modelo | ao_vivo | 2026-11-06T11:27:35 | causa_raiz: `corpo_nao_e_json` |
| 27 | 13 | declaracao | modelo | ao_vivo | 2026-11-06T11:27:35 | campo: `nenhum` |
| 28 | 14 | declaracao | modelo | ao_vivo | 2026-11-06T11:27:35 | impacto: `O usuário vê uma página de erro HTML em vez de uma lista de produtos JSON, resultando em uma interface incompleta e inutilizável.` |
| 29 | 15 | declaracao | modelo | ao_vivo | 2026-11-06T11:27:35 | fonte: `[corpo_nao_e_json]` |
| 30 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T11:27:35 | fonte_citada: `corpo_nao_e_json` |
| 31 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:27:35 | quatro_linhas_presentes: confere |
| 32 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:27:35 | rotulo_no_conjunto: confere |
| 33 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:27:35 | fonte_existe_na_biblioteca: confere |
| 34 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T11:27:35 | fonte_estava_no_contexto: confere |
| 35 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T11:27:35 | campo_existe_no_caso: nao_se_aplica |
| 36 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:27:35 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 37 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:27:35 | notas_nos_verbetes_citados: informativo |
| 38 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:27:35 | impacto: nao_verificavel |
| 39 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:27:35 | fonte_formato_valido: confere |
| 40 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:27:35 | fonte_contem_termo_da_causa: confere |
| 41 | 27 | decisao | programa | ao_vivo | 2026-11-06T11:27:35 | diagnostico: escolha corpo_nao_e_json; divergência não |

</details>

Nós de decisão:

- evento 41, `diagnostico`: escolha `corpo_nao_e_json`; resultado rotulo_emitido; evidência: evento 20 (sinal_em_codigo), evento 19 (arvore_podada), evento 16 (corpo_http), evento 21 (verbete_entregue, corpo_nao_e_json), evento 21 (verbete_entregue, erro_interno_do_servidor), evento 21 (verbete_entregue, mensagens-de-erro-do-codigo), evento 25 (resposta), evento 30 (verbete_citado, corpo_nao_e_json); divergência: não; falha: nenhuma; prov.used: corpo_nao_e_json, erro_interno_do_servidor, mensagens-de-erro-do-codigo (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 11 a 41 da trilha; hash dos eventos deste caso: `98471ab1f4374fff`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
