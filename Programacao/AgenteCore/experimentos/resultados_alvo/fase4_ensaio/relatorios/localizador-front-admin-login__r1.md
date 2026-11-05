<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `fase4_ensaio/qwen2.5_7b/localizador-front-admin-login#1`: o que o agente fez, declarou e conferiu

Trilha `fase4_ensaio/qwen2.5_7b/localizador-front-admin-login#1`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `localizador_quebrado` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário não consegue avançar na página de login, ficando preso na tela de login.`

Justificativa (gerada por molde): O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, tempo_de_resposta_excedido, usuario-e-login estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Alvo registrado na corrida de referência: button "Entrar" (ocorrência 1; tag `button`; caminho `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) > button:nth-of-type(1)`; atributos {"class": " btn btn-primary", "type": "submit"}).

Candidatos na ordem fixa (limiar do nome 0.6); verificações na ordem fixa:

| Estratégia | Seletor | um elemento | visível e habilitado | mesmo papel | nome parecido | efeito na reexecução | Aplicado |
|---|---|---|---|---|---|---|---|
| `papel_e_nome` | `role=button[name="Entrar"]` | **não confere** | não se aplica | não se aplica | não se aplica | não tentado |  |
| `papel_e_nome_parecido` | não gerado: nenhum button da árvore podada tem nome parecido com "Entrar" acima do limiar 0.6 | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `texto_contido` | `text=Entrar` | **não confere** | não se aplica | não se aplica | não se aplica | não tentado |  |
| `data_id` | não gerado: o alvo da referência não tem data-id | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `caminho_do_ancestral_com_id` | `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) > button:nth-of-type(1)` | **não confere** | não se aplica | não se aplica | não se aplica | não tentado |  |
| `posicao_entre_irmaos` | `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) >> role=button >> nth=0` | **não confere** | não se aplica | não se aplica | não se aplica | não tentado |  |

Poda de `arvore` (evento 291): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 9}, depois {"linhas": 6}.

Trecho podado (hash `b43e3d9b0f628402`):

```text
document "Chuleta Quente - Login"
  text "Login"
  textbox "Login" id="login_usuario" name="login_usuario"
  text "Senha"
  textbox "Senha" id="senha_usuario" name="senha_usuario"
  button "Entrar" class="btn btn-entrar"

```

## 3. Contraste com a segunda causa

localizador_quebrado e não tempo_de_resposta_excedido: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: localizador_quebrado, tempo_de_resposta_excedido, usuario-e-login

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| localizador_quebrado | 1,00 | sim |
| tempo_de_resposta_excedido | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `tempo_de_resposta_excedido`, `usuario-e-login` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado` |
| fonte_formato_valido | `[localizador_quebrado]` | confere | {"ids": ["localizador_quebrado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `localizador_quebrado` | confere | {"termo": "localizador_quebrado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_reexec --repeticoes 1`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 284 | 1 | entrada | programa | ao_vivo | 2026-11-04T20:32:38 | caso None |
| 285 | 2 | acao | programa | ao_vivo | 2026-11-04T20:32:43 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 106.0, "falhou": false, "reexecucao": 0} |
| 286 | 3 | acao | programa | ao_vivo | 2026-11-04T20:32:43 | {"passo": 2, "acao": "esperar", "seletor": "#login_usuario", "url": null, "tempo_ms": 25.3, "falhou": false, "reexecucao": 0} |
| 287 | 4 | acao | programa | ao_vivo | 2026-11-04T20:32:43 | {"passo": 3, "acao": "preencher", "seletor": "#login_usuario", "url": null, "tempo_ms": 17.9, "falhou": false, "reexecucao": 0} |
| 288 | 5 | acao | programa | ao_vivo | 2026-11-04T20:32:43 | {"passo": 4, "acao": "preencher", "seletor": "#senha_usuario", "url": null, "tempo_ms": 7.4, "falhou": false, "reexecucao": 0} |
| 289 | 6 | acao | programa | ao_vivo | 2026-11-04T20:32:43 | {"passo": 5, "acao": "clicar", "seletor": "button.btn-primary", "url": null, "tempo_ms": 5013.4, "falhou": true, "reexecucao": 0} |
| 291 | 7 | poda | programa | ao_vivo | 2026-11-04T20:32:43 | arvore: 0 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 292 | 8 | candidatos | programa | ao_vivo | 2026-11-04T20:32:43 | 3 de 39 verbetes entregues |
| 294 | 9 | prompt | programa | ao_vivo | 2026-11-04T20:32:43 | {"etapa": "diagnostico", "sha": "e5815b844eec5145", "prompt_sha256": "e5815b844eec", "chars": 3911, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 296 | 10 | inferencia | programa | ao_vivo | 2026-11-04T20:32:43 | diagnostico: 55,4 s |
| 297 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T20:32:43 | causa_raiz: `localizador_quebrado` |
| 298 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T20:32:43 | campo: `nenhum` |
| 299 | 13 | declaracao | modelo | ao_vivo | 2026-11-04T20:32:43 | impacto: `O usuário não consegue avançar na página de login, ficando preso na tela de login.` |
| 300 | 14 | declaracao | modelo | ao_vivo | 2026-11-04T20:32:43 | fonte: `[localizador_quebrado]` |
| 301 | 15 | declaracao | modelo | ao_vivo | 2026-11-04T20:32:43 | fonte_citada: `localizador_quebrado` |
| 302 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T20:32:43 | quatro_linhas_presentes: confere |
| 303 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T20:32:43 | rotulo_no_conjunto: confere |
| 304 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T20:32:43 | fonte_existe_na_biblioteca: confere |
| 305 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T20:32:43 | fonte_estava_no_contexto: confere |
| 306 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T20:32:43 | campo_existe_no_caso: nao_se_aplica |
| 307 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T20:32:43 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 308 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T20:32:43 | notas_nos_verbetes_citados: informativo |
| 309 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T20:32:43 | impacto: nao_verificavel |
| 310 | 24 | verificacao | verificacao | ao_vivo | 2026-11-04T20:32:43 | fonte_formato_valido: confere |
| 311 | 25 | verificacao | verificacao | ao_vivo | 2026-11-04T20:32:43 | fonte_contem_termo_da_causa: confere |
| 312 | 26 | decisao | programa | ao_vivo | 2026-11-04T20:32:43 | diagnostico: escolha localizador_quebrado; divergência não |
| 313 | 27 | cura | programa | ao_vivo | 2026-11-04T20:33:41 | não curado: 6 candidatos, 0 reexecução(ões) |
| 314 | 28 | decisao | programa | ao_vivo | 2026-11-04T20:33:41 | cura: escolha nenhuma; divergência sim |
| 315 | 29 | decisao | programa | ao_vivo | 2026-11-04T20:33:41 | reexecucao: escolha falhou; divergência sim |
| 316 | 30 | incidente | programa | ao_vivo | 2026-11-04T20:33:41 | {"tipo": "cdn_fora_do_har", "url": "https://code.jquery.com/jquery-2.2.0.min-js", "host": "code.jquery.com", "decisao": "har", "tipo_recurso": "script", "quando |
| 317 | 31 | incidente | programa | ao_vivo | 2026-11-04T20:33:41 | {"tipo": "cdn_fora_do_har", "url": "https://cdn.jsdelivr.net/npm/slick/slick.min.js", "host": "cdn.jsdelivr.net", "decisao": "har", "tipo_recurso": "script", "q |

</details>

Nós de decisão:

- evento 312, `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido; evidência: evento 291 (arvore_podada), evento 292 (verbete_entregue, localizador_quebrado), evento 292 (verbete_entregue, tempo_de_resposta_excedido), evento 292 (verbete_entregue, usuario-e-login), evento 296 (resposta), evento 301 (verbete_citado, localizador_quebrado); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, tempo_de_resposta_excedido, usuario-e-login (gen_ai: chat)
- evento 314, `cura`: escolha `nenhuma`; resultado sem_cura; evidência: evento 313 (candidato_de_seletor), evento 291 (arvore_podada); divergência: sim; falha: candidato_invalido; prov.used: papel_e_nome, texto_contido, caminho_do_ancestral_com_id, posicao_entre_irmaos (gen_ai: execute_tool)
- evento 315, `reexecucao`: escolha `falhou`; resultado sem_candidato; evidência: evento 313 (candidato_de_seletor); divergência: sim; falha: candidato_invalido; prov.used: nenhum

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 284 a 317 da trilha; hash dos eventos deste caso: `aa4c3d13e61695a8`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
