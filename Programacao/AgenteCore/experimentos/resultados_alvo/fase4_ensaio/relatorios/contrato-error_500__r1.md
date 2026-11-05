<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `contrato-error_500#1`: o que o agente fez, declarou e conferiu

Trilha `fase4_ensaio/qwen2.5_7b/contrato-error_500#1`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `erro_interno_do_servidor` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,99) · **CONFLITO**: nenhum verbete entregue trata da causa respondida erro_interno_do_servidor

**IMPACTO (declarado):** `O usuário vê uma mensagem de erro indicando que houve um problema ao carregar os produtos da API, comprometendo a exibição correta dos itens.`

Justificativa (gerada por molde): O agente respondeu erro_interno_do_servidor porque o sinal esperado lista, recebido objeto está presente na resposta HTTP e os verbetes contrato-produto, campo_ausente, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida erro_interno_do_servidor. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Poda de `arvore` (evento 210): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 54}, depois {"linhas": 21}.

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

Poda de `corpo_http` (evento 212): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 50}, depois {"chars": 205}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | lista | objeto |
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

Interceptação (evento 207): `GET /api/produtos` status 500; corpo `24067faf5d61b7b3`, árvore `None`.

## 3. Contraste com a segunda causa

erro_interno_do_servidor e não campo_ausente: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: contrato-produto, campo_ausente, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| erro_interno_do_servidor | 0,99 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| codificacao_incorreta | 0,00 |  |
| tipo_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [campo_ausente]`; verbetes citados: `contrato-produto`, `campo_ausente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `campo_ausente`, `estrutura_aninhada_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `contrato-produto`, `campo_ausente`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `erro_interno_do_servidor` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto], [campo_ausente]` | confere | {"ids": ["contrato-produto", "campo_ausente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "erro_interno_do_servidor"} |
| fonte_contem_termo_da_causa | `campo_ausente` | **não confere** | {"termo": "erro_interno_do_servidor"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_reexec --repeticoes 1`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 202 | 1 | entrada | programa | ao_vivo | 2026-11-04T20:28:46 | caso contrato-error_500#1 |
| 203 | 2 | acao | programa | ao_vivo | 2026-11-04T20:28:46 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 122.2, "falhou": false} |
| 204 | 3 | acao | programa | ao_vivo | 2026-11-04T20:28:46 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 7.1, "falhou": false} |
| 205 | 4 | acao | programa | ao_vivo | 2026-11-04T20:28:46 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 1.6, "falhou": true} |
| 207 | 5 | interceptacao | programa | ao_vivo | 2026-11-04T20:28:46 | GET /api/produtos 500 |
| 208 | 6 | verificacao | verificacao | ao_vivo | 2026-11-04T20:28:46 | conferencia_do_roteiro: nao_confere |
| 210 | 7 | poda | programa | ao_vivo | 2026-11-04T20:28:46 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 212 | 8 | poda | programa | ao_vivo | 2026-11-04T20:28:46 | corpo_http: 9 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 213 | 9 | candidatos | programa | ao_vivo | 2026-11-04T20:28:46 | 3 de 39 verbetes entregues |
| 215 | 10 | prompt | programa | ao_vivo | 2026-11-04T20:28:46 | {"etapa": "diagnostico", "sha": "7e0aae83bdbca0f4", "prompt_sha256": "7e0aae83bdbc", "chars": 5632, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 217 | 11 | inferencia | programa | ao_vivo | 2026-11-04T20:28:46 | diagnostico: 112,6 s |
| 218 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T20:28:46 | causa_raiz: `erro_interno_do_servidor` |
| 219 | 13 | declaracao | modelo | ao_vivo | 2026-11-04T20:28:46 | campo: `nenhum` |
| 220 | 14 | declaracao | modelo | ao_vivo | 2026-11-04T20:28:46 | impacto: `O usuário vê uma mensagem de erro indicando que houve um problema ao carregar os produtos da API, comprometendo a exibição correta dos itens.` |
| 221 | 15 | declaracao | modelo | ao_vivo | 2026-11-04T20:28:46 | fonte: `[contrato-produto], [campo_ausente]` |
| 222 | 16 | declaracao | modelo | ao_vivo | 2026-11-04T20:28:46 | fonte_citada: `contrato-produto` |
| 223 | 17 | declaracao | modelo | ao_vivo | 2026-11-04T20:28:46 | fonte_citada: `campo_ausente` |
| 224 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T20:28:46 | quatro_linhas_presentes: confere |
| 225 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T20:28:46 | rotulo_no_conjunto: confere |
| 226 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T20:28:46 | fonte_existe_na_biblioteca: confere |
| 227 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T20:28:46 | fonte_existe_na_biblioteca: confere |
| 228 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T20:28:46 | fonte_estava_no_contexto: confere |
| 229 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T20:28:46 | fonte_estava_no_contexto: confere |
| 230 | 24 | verificacao | verificacao | ao_vivo | 2026-11-04T20:28:46 | campo_existe_no_caso: nao_se_aplica |
| 231 | 25 | verificacao | verificacao | ao_vivo | 2026-11-04T20:28:46 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 232 | 26 | verificacao | verificacao | ao_vivo | 2026-11-04T20:28:46 | notas_nos_verbetes_citados: informativo |
| 233 | 27 | verificacao | verificacao | ao_vivo | 2026-11-04T20:28:46 | impacto: nao_verificavel |
| 234 | 28 | verificacao | verificacao | ao_vivo | 2026-11-04T20:28:46 | fonte_formato_valido: confere |
| 235 | 29 | verificacao | verificacao | ao_vivo | 2026-11-04T20:28:46 | fonte_contem_termo_da_causa: nao_confere |
| 236 | 30 | verificacao | verificacao | ao_vivo | 2026-11-04T20:28:46 | fonte_contem_termo_da_causa: nao_confere |
| 237 | 31 | decisao | programa | ao_vivo | 2026-11-04T20:28:46 | diagnostico: escolha erro_interno_do_servidor; divergência sim |

</details>

Nós de decisão:

- evento 237, `diagnostico`: escolha `erro_interno_do_servidor`; resultado rotulo_emitido; evidência: evento 212 (sinal_em_codigo), evento 210 (arvore_podada), evento 207 (corpo_http), evento 213 (verbete_entregue, contrato-produto), evento 213 (verbete_entregue, campo_ausente), evento 213 (verbete_entregue, estrutura_aninhada_divergente), evento 217 (resposta), evento 222 (verbete_citado, contrato-produto), evento 223 (verbete_citado, campo_ausente); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: contrato-produto, campo_ausente, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 202 a 237 da trilha; hash dos eventos deste caso: `489d7e464e0b6c1b`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
