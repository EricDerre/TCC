<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `contrato-error_500#1`: o que o agente fez, declarou e conferiu

Trilha `fase4_ensaio_v3/qwen2.5_7b/contrato-error_500#1`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `erro_interno_do_servidor` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê uma página de erro sem detalhes, enquanto a interface espera uma lista de produtos com detalhes específicos.`

Justificativa (gerada por molde): O agente respondeu erro_interno_do_servidor porque o sinal esperado lista, recebido objeto está presente na resposta HTTP e os verbetes erro_interno_do_servidor, contagem_inconsistente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 202): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 54}, depois {"linhas": 21}.

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

Poda de `corpo_http` (evento 204): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 50}, depois {"chars": 205}.

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

Interceptação (evento 199): `GET /api/produtos` status 500; corpo `24067faf5d61b7b3`, árvore `None`.

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

Linha FONTE como veio: `[erro_interno_do_servidor]`; verbetes citados: `erro_interno_do_servidor`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `erro_interno_do_servidor` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `erro_interno_do_servidor` | confere | contexto: `erro_interno_do_servidor`, `contagem_inconsistente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `erro_interno_do_servidor` | confere | verbetes: `erro_interno_do_servidor` |
| fonte_formato_valido | `[erro_interno_do_servidor]` | confere | {"ids": ["erro_interno_do_servidor"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `erro_interno_do_servidor` | confere | {"termo": "erro_interno_do_servidor"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v3_reexec --repeticoes 1`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 194 | 1 | entrada | programa | ao_vivo | 2026-11-05T20:03:38 | caso contrato-error_500#1 |
| 195 | 2 | acao | programa | ao_vivo | 2026-11-05T20:03:38 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 115.9, "falhou": false} |
| 196 | 3 | acao | programa | ao_vivo | 2026-11-05T20:03:38 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 8.0, "falhou": false} |
| 197 | 4 | acao | programa | ao_vivo | 2026-11-05T20:03:38 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.8, "falhou": true} |
| 199 | 5 | interceptacao | programa | ao_vivo | 2026-11-05T20:03:38 | GET /api/produtos 500 |
| 200 | 6 | verificacao | verificacao | ao_vivo | 2026-11-05T20:03:38 | conferencia_do_roteiro: nao_confere |
| 202 | 7 | poda | programa | ao_vivo | 2026-11-05T20:03:38 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 204 | 8 | poda | programa | ao_vivo | 2026-11-05T20:03:38 | corpo_http: 9 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 205 | 9 | candidatos | programa | ao_vivo | 2026-11-05T20:03:38 | 3 de 39 verbetes entregues |
| 207 | 10 | prompt | programa | ao_vivo | 2026-11-05T20:03:38 | {"etapa": "diagnostico", "sha": "3a531c262065d364", "prompt_sha256": "3a531c262065", "chars": 4228, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 209 | 11 | inferencia | programa | ao_vivo | 2026-11-05T20:03:38 | diagnostico: 81,4 s |
| 210 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T20:03:38 | causa_raiz: `erro_interno_do_servidor` |
| 211 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T20:03:38 | campo: `nenhum` |
| 212 | 14 | declaracao | modelo | ao_vivo | 2026-11-05T20:03:38 | impacto: `O usuário vê uma página de erro sem detalhes, enquanto a interface espera uma lista de produtos com detalhes específicos.` |
| 213 | 15 | declaracao | modelo | ao_vivo | 2026-11-05T20:03:38 | fonte: `[erro_interno_do_servidor]` |
| 214 | 16 | declaracao | modelo | ao_vivo | 2026-11-05T20:03:38 | fonte_citada: `erro_interno_do_servidor` |
| 215 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T20:03:38 | quatro_linhas_presentes: confere |
| 216 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T20:03:38 | rotulo_no_conjunto: confere |
| 217 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T20:03:38 | fonte_existe_na_biblioteca: confere |
| 218 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T20:03:38 | fonte_estava_no_contexto: confere |
| 219 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T20:03:38 | campo_existe_no_caso: nao_se_aplica |
| 220 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T20:03:38 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 221 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T20:03:38 | notas_nos_verbetes_citados: informativo |
| 222 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T20:03:38 | impacto: nao_verificavel |
| 223 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T20:03:38 | fonte_formato_valido: confere |
| 224 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T20:03:38 | fonte_contem_termo_da_causa: confere |
| 225 | 27 | decisao | programa | ao_vivo | 2026-11-05T20:03:38 | diagnostico: escolha erro_interno_do_servidor; divergência não |

</details>

Nós de decisão:

- evento 225, `diagnostico`: escolha `erro_interno_do_servidor`; resultado rotulo_emitido; evidência: evento 204 (sinal_em_codigo), evento 202 (arvore_podada), evento 199 (corpo_http), evento 205 (verbete_entregue, erro_interno_do_servidor), evento 205 (verbete_entregue, contagem_inconsistente), evento 205 (verbete_entregue, contrato-produto), evento 209 (resposta), evento 214 (verbete_citado, erro_interno_do_servidor); divergência: não; falha: nenhuma; prov.used: erro_interno_do_servidor, contagem_inconsistente, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 194 a 225 da trilha; hash dos eventos deste caso: `7e16dd3350c21edd`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
