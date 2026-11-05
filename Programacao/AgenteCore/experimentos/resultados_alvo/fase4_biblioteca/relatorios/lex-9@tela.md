<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-9`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/lex-9@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `corpo_nao_e_json` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê uma página de erro HTML em vez de uma lista de produtos.`

Justificativa (gerada por molde): O agente respondeu corpo_nao_e_json porque o sinal esperado JSON completo e válido, recebido corpo nao_json está presente na resposta HTTP e os verbetes corpo_nao_e_json, mensagens-de-erro-do-codigo, erro_interno_do_servidor estavam entre os entregues ao modelo. A segunda causa, corpo_vazio, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 1 recusada(s) (mensagem_nao_encontrada_no_codigo) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 1 edição(ões) para o caso lex-9. A proposta 1 (nota em [corpo_nao_e_json]) foi recusada por o filtro fonte_confiavel com o código mensagem_nao_encontrada_no_codigo: a mensagem "Página de erro HTML em vez de JSON" não está no código das cobaias nem no openapi.json.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `corpo_nao_e_json` | aceita | fonte_confiavel | recusada: `mensagem_nao_encontrada_no_codigo` | 1 |

Poda de `arvore` (evento 591): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 54}, depois {"linhas": 21}.

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

Poda de `corpo_http` (evento 592): regras diff_contra_contrato; antes {"chars": 73}, depois {"chars": 73}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | JSON completo e válido | corpo nao_json |

Trecho podado (hash `ceb0d510211b7efb`):

```text
<html><body><h1>Erro</h1><p>Falha ao montar a resposta.</p></body></html>
```

Interceptação (evento 589): `GET /api/produtos` status 200; corpo `ceb0d510211b7efb`, árvore `None`.

## 3. Contraste com a segunda causa

corpo_nao_e_json e não corpo_vazio: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: corpo_nao_e_json, mensagens-de-erro-do-codigo, erro_interno_do_servidor

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| corpo_nao_e_json | 0,99 | sim |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[corpo_nao_e_json] [mensagens-de-erro-do-codigo]`; verbetes citados: `corpo_nao_e_json`, `mensagens-de-erro-do-codigo`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `corpo_nao_e_json` | confere |  |
| O verbete citado existe na biblioteca | `mensagens-de-erro-do-codigo` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `corpo_nao_e_json` | confere | contexto: `corpo_nao_e_json`, `mensagens-de-erro-do-codigo`, `erro_interno_do_servidor` |
| O verbete citado estava no contexto entregue ao modelo | `mensagens-de-erro-do-codigo` | confere | contexto: `corpo_nao_e_json`, `mensagens-de-erro-do-codigo`, `erro_interno_do_servidor` |
| Algum verbete do contexto trata da causa respondida | `corpo_nao_e_json` | confere | verbetes: `corpo_nao_e_json`, `mensagens-de-erro-do-codigo`, `erro_interno_do_servidor` |
| fonte_formato_valido | `[corpo_nao_e_json] [mensagens-de-erro-do-codigo]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["corpo_nao_e_json", "mensagens-de-erro-do-codigo"]} |
| fonte_contem_termo_da_causa | `corpo_nao_e_json` | confere | {"termo": "corpo_nao_e_json"} |
| fonte_contem_termo_da_causa | `mensagens-de-erro-do-codigo` | **não confere** | {"termo": "corpo_nao_e_json"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>34 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 585 | 1 | entrada | programa | ao_vivo | 2026-11-03T22:06:18 | caso lex-9 |
| 586 | 2 | acao | programa | ao_vivo | 2026-11-03T22:06:18 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 99.7, "url": "produtos_api.php"} |
| 587 | 3 | acao | programa | ao_vivo | 2026-11-03T22:06:18 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 5.5, "url": null} |
| 588 | 4 | acao | programa | ao_vivo | 2026-11-03T22:06:18 | {"acao": "conferir", "falhou": true, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 1.7, "url": null} |
| 589 | 5 | interceptacao | programa | ao_vivo | 2026-11-03T22:06:18 | GET /api/produtos 200 |
| 590 | 6 | verificacao | verificacao | ao_vivo | 2026-11-03T22:06:18 | conferencia_do_roteiro: nao_confere |
| 591 | 7 | poda | programa | ao_vivo | 2026-11-03T22:06:18 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 592 | 8 | poda | programa | ao_vivo | 2026-11-03T22:06:18 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 593 | 9 | candidatos | programa | ao_vivo | 2026-11-03T22:06:18 | 3 de 40 verbetes entregues |
| 594 | 10 | prompt | programa | ao_vivo | 2026-11-03T22:06:18 | {"chars": 5324, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "3f2ee60d5acc", "sha": "3f2ee60d5acc05bf"} |
| 595 | 11 | inferencia | programa | ao_vivo | 2026-11-03T22:06:18 | diagnostico: 16,9 s |
| 596 | 12 | declaracao | modelo | ao_vivo | 2026-11-03T22:06:18 | causa_raiz: `corpo_nao_e_json` |
| 597 | 13 | declaracao | modelo | ao_vivo | 2026-11-03T22:06:18 | campo: `nenhum` |
| 598 | 14 | declaracao | modelo | ao_vivo | 2026-11-03T22:06:18 | impacto: `O usuário vê uma página de erro HTML em vez de uma lista de produtos.` |
| 599 | 15 | declaracao | modelo | ao_vivo | 2026-11-03T22:06:18 | fonte: `[corpo_nao_e_json] [mensagens-de-erro-do-codigo]` |
| 600 | 16 | declaracao | modelo | ao_vivo | 2026-11-03T22:06:18 | fonte_citada: `corpo_nao_e_json` |
| 601 | 17 | declaracao | modelo | ao_vivo | 2026-11-03T22:06:18 | fonte_citada: `mensagens-de-erro-do-codigo` |
| 602 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T22:06:18 | quatro_linhas_presentes: confere |
| 603 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T22:06:18 | rotulo_no_conjunto: confere |
| 604 | 20 | verificacao | verificacao | ao_vivo | 2026-11-03T22:06:18 | fonte_existe_na_biblioteca: confere |
| 605 | 21 | verificacao | verificacao | ao_vivo | 2026-11-03T22:06:18 | fonte_existe_na_biblioteca: confere |
| 606 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T22:06:18 | fonte_estava_no_contexto: confere |
| 607 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T22:06:18 | fonte_estava_no_contexto: confere |
| 608 | 24 | verificacao | verificacao | ao_vivo | 2026-11-03T22:06:18 | campo_existe_no_caso: nao_se_aplica |
| 609 | 25 | verificacao | verificacao | ao_vivo | 2026-11-03T22:06:18 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 610 | 26 | verificacao | verificacao | ao_vivo | 2026-11-03T22:06:18 | notas_nos_verbetes_citados: informativo |
| 611 | 27 | verificacao | verificacao | ao_vivo | 2026-11-03T22:06:18 | impacto: nao_verificavel |
| 612 | 28 | verificacao | verificacao | ao_vivo | 2026-11-03T22:06:18 | fonte_formato_valido: confere |
| 613 | 29 | verificacao | verificacao | ao_vivo | 2026-11-03T22:06:18 | fonte_contem_termo_da_causa: confere |
| 614 | 30 | verificacao | verificacao | ao_vivo | 2026-11-03T22:06:18 | fonte_contem_termo_da_causa: nao_confere |
| 615 | 31 | decisao | programa | ao_vivo | 2026-11-03T22:06:18 | diagnostico: escolha corpo_nao_e_json; divergência não |
| 617 | 32 | inferencia | programa | ao_vivo | 2026-11-03T22:06:39 | proposta: 125,3 s |
| 618 | 33 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:06:39 | proposta 1: nota em [corpo_nao_e_json]: recusada: mensagem_nao_encontrada_no_codigo |
| 619 | 34 | decisao | programa | ao_vivo | 2026-11-03T22:06:39 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 615, `diagnostico`: escolha `corpo_nao_e_json`; resultado rotulo_emitido; evidência: evento 592 (sinal_em_codigo), evento 591 (arvore_podada), evento 589 (corpo_http), evento 593 (verbete_entregue, corpo_nao_e_json), evento 593 (verbete_entregue, mensagens-de-erro-do-codigo), evento 593 (verbete_entregue, erro_interno_do_servidor), evento 595 (resposta), evento 600 (verbete_citado, corpo_nao_e_json), evento 601 (verbete_citado, mensagens-de-erro-do-codigo); divergência: não; falha: nenhuma; prov.used: corpo_nao_e_json, mensagens-de-erro-do-codigo, erro_interno_do_servidor (gen_ai: chat)
- evento 619, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 592 (sinal_em_codigo), evento 591 (arvore_podada), evento 589 (corpo_http), evento 595 (resposta), evento 617 (resposta), evento 618 (verbete_entregue, corpo_nao_e_json); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: corpo_nao_e_json, erro_interno_do_servidor, mensagens-de-erro-do-codigo

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 585 a 619 da trilha; hash dos eventos deste caso: `6de2a3249b6353cc`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
