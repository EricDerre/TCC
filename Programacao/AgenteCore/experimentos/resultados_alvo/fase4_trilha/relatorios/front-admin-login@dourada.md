<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `fase4_trilha/qwen2.5_7b/front-admin-login@dourada`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/front-admin-login@dourada`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `localizador_quebrado` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário não consegue avançar na página de login, ficando preso na tela de entrada de credenciais.`

Justificativa (gerada por molde): O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, tempo_de_resposta_excedido, usuario-e-login estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Alvo registrado na corrida de referência: button "Entrar" (ocorrência 1; tag `button`; caminho `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) > button:nth-of-type(1)`; atributos {"class": " btn btn-primary", "type": "submit"}).

Candidatos na ordem fixa (limiar do nome 0.6); verificações na ordem fixa:

| Estratégia | Seletor | um elemento | visível e habilitado | mesmo papel | nome parecido | efeito na reexecução | Aplicado |
|---|---|---|---|---|---|---|---|
| `papel_e_nome` | `role=button[name="Entrar"]` | confere | confere | confere | confere ("Entrar" contra "Entrar": similaridade 1.00 (limiar 0.6)) | confere (o roteiro chegou ao fim: 2 conferência(s) passaram em 0.301 s) | **sim** |
| `papel_e_nome_parecido` | não gerado: nenhum button da árvore podada tem nome parecido com "Entrar" acima do limiar 0.6 | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `texto_contido` | `text=Entrar` | confere | confere | confere | confere ("Entrar" contra "Entrar": similaridade 1.00 (limiar 0.6)) | não tentado |  |
| `data_id` | não gerado: o alvo da referência não tem data-id | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `caminho_do_ancestral_com_id` | `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) > button:nth-of-type(1)` | confere | confere | confere | confere ("Entrar" contra "Entrar": similaridade 1.00 (limiar 0.6)) | não tentado |  |
| `posicao_entre_irmaos` | `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) >> role=button >> nth=0` | confere | confere | confere | confere ("Entrar" contra "Entrar": similaridade 1.00 (limiar 0.6)) | não tentado |  |

Poda de `arvore` (evento 3881): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 9}, depois {"linhas": 6}.

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

Sugestão (o agente não altera a aplicação): no passo 5 do roteiro, trocar o localizador `button.btn-primary` por `role=button[name="Entrar"]` (estratégia `papel_e_nome`), que resolve o mesmo elemento da referência.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --casos 0`

## 6. Árvore completa

<details><summary>39 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3874 | 1 | entrada | programa | ao_vivo | 2026-11-05T02:33:30 | caso None |
| 3875 | 2 | acao | programa | ao_vivo | 2026-11-05T02:33:35 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 86.8, "falhou": false, "reexecucao": 0} |
| 3876 | 3 | acao | programa | ao_vivo | 2026-11-05T02:33:35 | {"passo": 2, "acao": "esperar", "seletor": "#login_usuario", "url": null, "tempo_ms": 25.2, "falhou": false, "reexecucao": 0} |
| 3877 | 4 | acao | programa | ao_vivo | 2026-11-05T02:33:35 | {"passo": 3, "acao": "preencher", "seletor": "#login_usuario", "url": null, "tempo_ms": 15.8, "falhou": false, "reexecucao": 0} |
| 3878 | 5 | acao | programa | ao_vivo | 2026-11-05T02:33:35 | {"passo": 4, "acao": "preencher", "seletor": "#senha_usuario", "url": null, "tempo_ms": 8.5, "falhou": false, "reexecucao": 0} |
| 3879 | 6 | acao | programa | ao_vivo | 2026-11-05T02:33:35 | {"passo": 5, "acao": "clicar", "seletor": "button.btn-primary", "url": null, "tempo_ms": 5008.0, "falhou": true, "reexecucao": 0} |
| 3881 | 7 | poda | programa | ao_vivo | 2026-11-05T02:33:35 | arvore: 0 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 3882 | 8 | candidatos | programa | ao_vivo | 2026-11-05T02:33:35 | 3 de 39 verbetes entregues |
| 3884 | 9 | prompt | programa | ao_vivo | 2026-11-05T02:33:35 | {"etapa": "diagnostico", "sha": "e5815b844eec5145", "prompt_sha256": "e5815b844eec", "chars": 3911, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 3886 | 10 | inferencia | programa | ao_vivo | 2026-11-05T02:33:35 | diagnostico: 55,2 s |
| 3887 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T02:33:35 | causa_raiz: `localizador_quebrado` |
| 3888 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T02:33:35 | campo: `nenhum` |
| 3889 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T02:33:35 | impacto: `O usuário não consegue avançar na página de login, ficando preso na tela de entrada de credenciais.` |
| 3890 | 14 | declaracao | modelo | ao_vivo | 2026-11-05T02:33:35 | fonte: `[localizador_quebrado]` |
| 3891 | 15 | declaracao | modelo | ao_vivo | 2026-11-05T02:33:35 | fonte_citada: `localizador_quebrado` |
| 3892 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T02:33:35 | quatro_linhas_presentes: confere |
| 3893 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T02:33:35 | rotulo_no_conjunto: confere |
| 3894 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T02:33:35 | fonte_existe_na_biblioteca: confere |
| 3895 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T02:33:35 | fonte_estava_no_contexto: confere |
| 3896 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T02:33:35 | campo_existe_no_caso: nao_se_aplica |
| 3897 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T02:33:35 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 3898 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T02:33:35 | notas_nos_verbetes_citados: informativo |
| 3899 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T02:33:35 | impacto: nao_verificavel |
| 3900 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T02:33:35 | fonte_formato_valido: confere |
| 3901 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T02:33:35 | fonte_contem_termo_da_causa: confere |
| 3902 | 26 | decisao | programa | ao_vivo | 2026-11-05T02:33:35 | diagnostico: escolha localizador_quebrado; divergência não |
| 3903 | 27 | cura | programa | ao_vivo | 2026-11-05T02:34:33 | curado: 6 candidatos, 1 reexecução(ões); aplicado papel_e_nome; MTTR 57,9 s |
| 3904 | 28 | decisao | programa | ao_vivo | 2026-11-05T02:34:33 | cura: escolha papel_e_nome; divergência sim |
| 3905 | 29 | acao | programa | ao_vivo | 2026-11-05T02:34:33 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 72.1, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curad |
| 3906 | 30 | acao | programa | ao_vivo | 2026-11-05T02:34:33 | {"passo": 2, "acao": "esperar", "seletor": "#login_usuario", "url": null, "tempo_ms": 27.8, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cura |
| 3907 | 31 | acao | programa | ao_vivo | 2026-11-05T02:34:33 | {"passo": 3, "acao": "preencher", "seletor": "#login_usuario", "url": null, "tempo_ms": 16.7, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cu |
| 3908 | 32 | acao | programa | ao_vivo | 2026-11-05T02:34:33 | {"passo": 4, "acao": "preencher", "seletor": "#senha_usuario", "url": null, "tempo_ms": 7.2, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cur |
| 3909 | 33 | acao | programa | ao_vivo | 2026-11-05T02:34:33 | {"passo": 5, "acao": "clicar", "seletor": "role=button[name=\"Entrar\"]", "url": null, "tempo_ms": 74.5, "falhou": false, "reexecucao": 1, "candidato": "papel_e |
| 3910 | 34 | acao | programa | ao_vivo | 2026-11-05T02:34:33 | {"passo": 6, "acao": "esperar", "seletor": "h1.breadcrumb", "url": null, "tempo_ms": 76.8, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curad |
| 3911 | 35 | acao | programa | ao_vivo | 2026-11-05T02:34:33 | {"passo": 7, "acao": "conferir", "seletor": "h1.breadcrumb", "url": null, "tempo_ms": 13.8, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cura |
| 3912 | 36 | acao | programa | ao_vivo | 2026-11-05T02:34:33 | {"passo": 8, "acao": "conferir", "seletor": null, "url": null, "tempo_ms": 0.0, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado": false} |
| 3913 | 37 | verificacao | verificacao | ao_vivo | 2026-11-05T02:34:33 | conferencia_do_roteiro: confere |
| 3914 | 38 | verificacao | verificacao | ao_vivo | 2026-11-05T02:34:33 | conferencia_do_roteiro: confere |
| 3915 | 39 | decisao | programa | ao_vivo | 2026-11-05T02:34:33 | reexecucao: escolha validada; divergência não |

</details>

Nós de decisão:

- evento 3902, `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido; evidência: evento 3881 (arvore_podada), evento 3882 (verbete_entregue, localizador_quebrado), evento 3882 (verbete_entregue, tempo_de_resposta_excedido), evento 3882 (verbete_entregue, usuario-e-login), evento 3886 (resposta), evento 3891 (verbete_citado, localizador_quebrado); divergência: não; falha: nenhuma; prov.used: localizador_quebrado, tempo_de_resposta_excedido, usuario-e-login (gen_ai: chat)
- evento 3904, `cura`: escolha `papel_e_nome`; resultado cura_aplicada; evidência: evento 3903 (candidato_de_seletor), evento 3881 (arvore_podada); divergência: sim; falha: nenhuma; prov.used: papel_e_nome, texto_contido, caminho_do_ancestral_com_id, posicao_entre_irmaos (gen_ai: execute_tool)
- evento 3915, `reexecucao`: escolha `validada`; resultado roteiro_concluido; evidência: evento 3903 (candidato_de_seletor), evento 3913 (sinal_em_codigo), evento 3914 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: papel_e_nome

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3874 a 3915 da trilha; hash dos eventos deste caso: `27f51fa55a5b7dc5`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
