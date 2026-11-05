<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-3`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/lex-3@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `corpo_vazio` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,99)

**IMPACTO (declarado):** `A tela exibe uma mensagem de erro e falta conteúdo de produtos, prejudicando a experiência do usuário.`

Justificativa (gerada por molde): O agente respondeu corpo_vazio porque o sinal esperado JSON completo e válido, recebido corpo vazio está presente na resposta HTTP e os verbetes corpo_vazio, tempo_de_resposta_excedido, resposta_truncada estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,01. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 2 recusada(s) (duplicada, id_repetido) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso lex-3. A proposta 1 (nota em [corpo_vazio]) foi recusada por a validação da Fase 3 com o código duplicada: [corpo_vazio] já tem uma nota com este texto. A proposta 2 (novo_verbete em [resposta_truncada]) foi recusada por a validação da Fase 3 com o código id_repetido: 'resposta_truncada' já é id de verbete ou nome de causa raiz.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `corpo_vazio` | recusada: `duplicada` | nenhum | recusada: `duplicada` |  |
| 2 | novo_verbete | `resposta_truncada` | recusada: `id_repetido` | nenhum | recusada: `id_repetido` |  |

Poda de `arvore` (evento 61): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 54}, depois {"linhas": 21}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 22 linha(s) da referência | 4 linha(s) novas |

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

Poda de `corpo_http` (evento 62): regras diff_contra_contrato; antes {"chars": 0}, depois {"chars": 0}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo vazio |

Trecho podado (hash `e3b0c44298fc1c14`):

```text

```

Interceptação (evento 58): `GET /api/produtos` status 200; corpo `e3b0c44298fc1c14`, árvore `None`.

## 3. Contraste com a segunda causa

corpo_vazio e não resposta_truncada: a escolha tem probabilidade 0,99 contra 0,01; verbete(s) na evidência: corpo_vazio, tempo_de_resposta_excedido, resposta_truncada

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| corpo_vazio | 0,99 | sim |
| resposta_truncada | 0,01 |  |
| corpo_nao_e_json | 0,00 |  |
| tempo_de_resposta_excedido | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[corpo_vazio]`; verbetes citados: `corpo_vazio`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `corpo_vazio` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `corpo_vazio` | confere | contexto: `corpo_vazio`, `tempo_de_resposta_excedido`, `resposta_truncada` |
| Algum verbete do contexto trata da causa respondida | `corpo_vazio` | confere | verbetes: `corpo_vazio`, `tempo_de_resposta_excedido`, `resposta_truncada` |
| fonte_formato_valido | `[corpo_vazio]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["corpo_vazio"]} |
| fonte_contem_termo_da_causa | `corpo_vazio` | confere | {"termo": "corpo_vazio"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 53 | 1 | entrada | programa | ao_vivo | 2026-11-03T21:05:22 | caso lex-3 |
| 54 | 2 | acao | programa | ao_vivo | 2026-11-03T21:05:22 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 170.4, "url": "produtos_api.php"} |
| 55 | 3 | acao | programa | ao_vivo | 2026-11-03T21:05:22 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 6.7, "url": null} |
| 56 | 4 | acao | programa | ao_vivo | 2026-11-03T21:05:22 | {"acao": "conferir", "falhou": true, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 1.7, "url": null} |
| 58 | 5 | interceptacao | programa | ao_vivo | 2026-11-03T21:05:22 | GET /api/produtos 200 |
| 59 | 6 | verificacao | verificacao | ao_vivo | 2026-11-03T21:05:22 | conferencia_do_roteiro: nao_confere |
| 61 | 7 | poda | programa | ao_vivo | 2026-11-03T21:05:22 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 62 | 8 | poda | programa | ao_vivo | 2026-11-03T21:05:22 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 63 | 9 | candidatos | programa | ao_vivo | 2026-11-03T21:05:22 | 3 de 40 verbetes entregues |
| 65 | 10 | prompt | programa | ao_vivo | 2026-11-03T21:05:22 | {"chars": 5095, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "758a8717b9ce", "sha": "758a8717b9ceecf7"} |
| 67 | 11 | inferencia | programa | ao_vivo | 2026-11-03T21:05:22 | diagnostico: 95,5 s |
| 68 | 12 | declaracao | modelo | ao_vivo | 2026-11-03T21:05:22 | causa_raiz: `corpo_vazio` |
| 69 | 13 | declaracao | modelo | ao_vivo | 2026-11-03T21:05:22 | campo: `nenhum` |
| 70 | 14 | declaracao | modelo | ao_vivo | 2026-11-03T21:05:22 | impacto: `A tela exibe uma mensagem de erro e falta conteúdo de produtos, prejudicando a experiência do usuário.` |
| 71 | 15 | declaracao | modelo | ao_vivo | 2026-11-03T21:05:22 | fonte: `[corpo_vazio]` |
| 72 | 16 | declaracao | modelo | ao_vivo | 2026-11-03T21:05:22 | fonte_citada: `corpo_vazio` |
| 73 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T21:05:22 | quatro_linhas_presentes: confere |
| 74 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T21:05:22 | rotulo_no_conjunto: confere |
| 75 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T21:05:22 | fonte_existe_na_biblioteca: confere |
| 76 | 20 | verificacao | verificacao | ao_vivo | 2026-11-03T21:05:22 | fonte_estava_no_contexto: confere |
| 77 | 21 | verificacao | verificacao | ao_vivo | 2026-11-03T21:05:22 | campo_existe_no_caso: nao_se_aplica |
| 78 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T21:05:22 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 79 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T21:05:22 | notas_nos_verbetes_citados: informativo |
| 80 | 24 | verificacao | verificacao | ao_vivo | 2026-11-03T21:05:22 | impacto: nao_verificavel |
| 81 | 25 | verificacao | verificacao | ao_vivo | 2026-11-03T21:05:22 | fonte_formato_valido: confere |
| 82 | 26 | verificacao | verificacao | ao_vivo | 2026-11-03T21:05:22 | fonte_contem_termo_da_causa: confere |
| 83 | 27 | decisao | programa | ao_vivo | 2026-11-03T21:05:22 | diagnostico: escolha corpo_vazio; divergência não |
| 86 | 28 | inferencia | programa | ao_vivo | 2026-11-03T21:07:02 | proposta: 185,9 s |
| 88 | 29 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:07:02 | proposta 1: nota em [corpo_vazio]: recusada: duplicada |
| 90 | 30 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:07:02 | proposta 2: novo_verbete em [resposta_truncada]: recusada: id_repetido |
| 91 | 31 | decisao | programa | ao_vivo | 2026-11-03T21:07:02 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 83, `diagnostico`: escolha `corpo_vazio`; resultado rotulo_emitido; evidência: evento 62 (sinal_em_codigo), evento 61 (arvore_podada), evento 58 (corpo_http), evento 63 (verbete_entregue, corpo_vazio), evento 63 (verbete_entregue, tempo_de_resposta_excedido), evento 63 (verbete_entregue, resposta_truncada), evento 67 (resposta), evento 72 (verbete_citado, corpo_vazio); divergência: não; falha: nenhuma; prov.used: corpo_vazio, tempo_de_resposta_excedido, resposta_truncada (gen_ai: chat)
- evento 91, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 62 (sinal_em_codigo), evento 61 (arvore_podada), evento 58 (corpo_http), evento 67 (resposta), evento 86 (resposta), evento 88 (verbete_entregue, corpo_vazio), evento 90 (verbete_entregue, resposta_truncada); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: corpo_vazio, resposta_truncada, tempo_de_resposta_excedido

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 53 a 91 da trilha; hash dos eventos deste caso: `349fa62236b4571f`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
