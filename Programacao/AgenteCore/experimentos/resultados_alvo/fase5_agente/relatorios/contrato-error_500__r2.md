<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `contrato-error_500#2`: o que o agente fez, declarou e conferiu

Trilha `fase5_agente/qwen2.5_7b/contrato-error_500#2`; modelo `qwen2.5:7b`, Ollama 0.40.16, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `erro_interno_do_servidor` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê uma página de erro sem detalhes, enquanto a interface esperava uma lista de produtos formatada corretamente.`

Justificativa (gerada por molde): O agente respondeu erro_interno_do_servidor porque o sinal esperado lista, recebido objeto está presente na resposta HTTP e os verbetes erro_interno_do_servidor, contagem_inconsistente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 597): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 54}, depois {"linhas": 21}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 22 linha(s) da referência | 4 linha(s) novas |

Trecho podado (hash `e9b6b8fff9529555`):

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
    text "Erro ao carregar produtos da CobaiaAPI: HTTP 500"
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

Poda de `corpo_http` (evento 598): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 50}, depois {"chars": 205}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| (corpo inteiro) | lista | objeto |
| id | inteiro |  |
| nome | texto |  |
| resumo | texto\|nulo |  |
| tipo | texto |  |
| preco | numero |  |
| imagem | texto\|nulo |  |
| destaque | booleano |  |
| detail |  | texto |

Trecho podado (hash `76e7cf76cde2ae11`):

```text
{"detail": "fault injection: error_500 em produto", "id": "(ausente)", "nome": "(ausente)", "resumo": "(ausente)", "tipo": "(ausente)", "preco": "(ausente)", "imagem": "(ausente)", "destaque": "(ausente)"}
```

Interceptação (evento 595): `GET /api/produtos` status 500; corpo `24067faf5d61b7b3`, árvore `None`.

## 3. Contraste com a segunda causa

erro_interno_do_servidor e não resposta_truncada: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: erro_interno_do_servidor, contagem_inconsistente, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| erro_interno_do_servidor | 0,99 | sim |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| tipo_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[erro_interno_do_servidor] [contrato-produto]`; verbetes citados: `erro_interno_do_servidor`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `erro_interno_do_servidor` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `erro_interno_do_servidor` | confere | contexto: `erro_interno_do_servidor`, `contagem_inconsistente`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `erro_interno_do_servidor`, `contagem_inconsistente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `erro_interno_do_servidor` | confere | verbetes: `erro_interno_do_servidor` |
| fonte_formato_valido | `[erro_interno_do_servidor] [contrato-produto]` | confere | {"ids": ["erro_interno_do_servidor", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `erro_interno_do_servidor` | confere | {"termo": "erro_interno_do_servidor"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "erro_interno_do_servidor"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase5_agente_reexec --repeticoes 1`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 591 | 1 | entrada | programa | ao_vivo | 2026-11-18T19:00:51 | caso contrato-error_500#2 |
| 592 | 2 | acao | programa | ao_vivo | 2026-11-18T19:00:52 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 126.5, "falhou": false} |
| 593 | 3 | acao | programa | ao_vivo | 2026-11-18T19:00:52 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 6.3, "falhou": false} |
| 594 | 4 | acao | programa | ao_vivo | 2026-11-18T19:00:52 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 1.6, "falhou": true} |
| 595 | 5 | interceptacao | programa | ao_vivo | 2026-11-18T19:00:52 | GET /api/produtos 500 |
| 596 | 6 | verificacao | verificacao | ao_vivo | 2026-11-18T19:00:52 | conferencia_do_roteiro: nao_confere |
| 597 | 7 | poda | programa | ao_vivo | 2026-11-18T19:00:52 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 598 | 8 | poda | programa | ao_vivo | 2026-11-18T19:00:52 | corpo_http: 9 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 599 | 9 | candidatos | programa | ao_vivo | 2026-11-18T19:00:52 | 3 de 39 verbetes entregues |
| 600 | 10 | prompt | programa | ao_vivo | 2026-11-18T19:00:52 | {"etapa": "diagnostico", "sha": "3a531c262065d364", "prompt_sha256": "3a531c262065", "chars": 4228, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 602 | 11 | inferencia | programa | ao_vivo | 2026-11-18T19:00:52 | diagnostico: 17,8 s |
| 603 | 12 | declaracao | modelo | ao_vivo | 2026-11-18T19:00:52 | causa_raiz: `erro_interno_do_servidor` |
| 604 | 13 | declaracao | modelo | ao_vivo | 2026-11-18T19:00:52 | campo: `nenhum` |
| 605 | 14 | declaracao | modelo | ao_vivo | 2026-11-18T19:00:52 | impacto: `O usuário vê uma página de erro sem detalhes, enquanto a interface esperava uma lista de produtos formatada corretamente.` |
| 606 | 15 | declaracao | modelo | ao_vivo | 2026-11-18T19:00:52 | fonte: `[erro_interno_do_servidor] [contrato-produto]` |
| 607 | 16 | declaracao | modelo | ao_vivo | 2026-11-18T19:00:52 | fonte_citada: `erro_interno_do_servidor` |
| 608 | 17 | declaracao | modelo | ao_vivo | 2026-11-18T19:00:52 | fonte_citada: `contrato-produto` |
| 609 | 18 | verificacao | verificacao | ao_vivo | 2026-11-18T19:00:52 | quatro_linhas_presentes: confere |
| 610 | 19 | verificacao | verificacao | ao_vivo | 2026-11-18T19:00:52 | rotulo_no_conjunto: confere |
| 611 | 20 | verificacao | verificacao | ao_vivo | 2026-11-18T19:00:52 | fonte_existe_na_biblioteca: confere |
| 612 | 21 | verificacao | verificacao | ao_vivo | 2026-11-18T19:00:52 | fonte_existe_na_biblioteca: confere |
| 613 | 22 | verificacao | verificacao | ao_vivo | 2026-11-18T19:00:52 | fonte_estava_no_contexto: confere |
| 614 | 23 | verificacao | verificacao | ao_vivo | 2026-11-18T19:00:52 | fonte_estava_no_contexto: confere |
| 615 | 24 | verificacao | verificacao | ao_vivo | 2026-11-18T19:00:52 | campo_existe_no_caso: nao_se_aplica |
| 616 | 25 | verificacao | verificacao | ao_vivo | 2026-11-18T19:00:52 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 617 | 26 | verificacao | verificacao | ao_vivo | 2026-11-18T19:00:52 | notas_nos_verbetes_citados: informativo |
| 618 | 27 | verificacao | verificacao | ao_vivo | 2026-11-18T19:00:52 | impacto: nao_verificavel |
| 619 | 28 | verificacao | verificacao | ao_vivo | 2026-11-18T19:00:52 | fonte_formato_valido: confere |
| 620 | 29 | verificacao | verificacao | ao_vivo | 2026-11-18T19:00:52 | fonte_contem_termo_da_causa: confere |
| 621 | 30 | verificacao | verificacao | ao_vivo | 2026-11-18T19:00:52 | fonte_contem_termo_da_causa: nao_confere |
| 622 | 31 | decisao | programa | ao_vivo | 2026-11-18T19:00:52 | diagnostico: escolha erro_interno_do_servidor; divergência não |

</details>

Nós de decisão:

- evento 622, `diagnostico`: escolha `erro_interno_do_servidor`; resultado rotulo_emitido; evidência: evento 598 (sinal_em_codigo), evento 597 (arvore_podada), evento 595 (corpo_http), evento 599 (verbete_entregue, erro_interno_do_servidor), evento 599 (verbete_entregue, contagem_inconsistente), evento 599 (verbete_entregue, contrato-produto), evento 602 (resposta), evento 607 (verbete_citado, erro_interno_do_servidor), evento 608 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: erro_interno_do_servidor, contagem_inconsistente, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 591 a 622 da trilha; hash dos eventos deste caso: `60de2d8d3fffd46d`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
