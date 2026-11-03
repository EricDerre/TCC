<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `fase4_cura/front-admin-login/classe_trocada/php/r4`: o que o agente fez, declarou e conferiu

Trilha `fase4_cura/front-admin-login/classe_trocada/php/r4`; modelo `(sem modelo: cura de seletor)`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**Cura de seletor:** aplicada: `papel_e_nome` (`role=button[name="Entrar"]`) · reexecução validada · mesmo elemento da referência: sim

Passo 5 do roteiro, localizador `button.btn-primary`: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("button.btn-primary")

Da detecção à reexecução validada: 0,4 s (detecção 2026-11-01T20:04:17; validação 2026-11-01T20:04:18).

Justificativa (gerada por molde): O passo 5 (button.btn-primary) falhou: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("button.btn-primary"). Dos 6 candidatos previstos, 4 foram gerados da árvore podada e do alvo da referência; 4 passaram as quatro verificações em código (um elemento só, visível e habilitado, mesmo papel, nome parecido acima de 0.6). O primeiro que passou, `papel_e_nome` (role=button[name="Entrar"]), levou o roteiro ao fim na reexecução e resolve o mesmo elemento da referência. Da detecção à reexecução validada: 0,4 s.

## 2. Evidência

Alvo registrado na corrida de referência: button "Entrar" (ocorrência 1; tag `button`; caminho `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) > button:nth-of-type(1)`; atributos {"class": " btn btn-primary", "type": "submit"}).

Candidatos na ordem fixa (limiar do nome 0.6); verificações na ordem fixa:

| Estratégia | Seletor | um elemento | visível e habilitado | mesmo papel | nome parecido | efeito na reexecução | Aplicado |
|---|---|---|---|---|---|---|---|
| `papel_e_nome` | `role=button[name="Entrar"]` | confere | confere | confere | confere ("Entrar" contra "Entrar": similaridade 1.00 (limiar 0.6)) | confere (o roteiro chegou ao fim: 2 conferência(s) passaram em 0.296 s) | **sim** |
| `papel_e_nome_parecido` | não gerado: nenhum button da árvore podada tem nome parecido com "Entrar" acima do limiar 0.6 | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `texto_contido` | `text=Entrar` | confere | confere | confere | confere ("Entrar" contra "Entrar": similaridade 1.00 (limiar 0.6)) | não tentado |  |
| `data_id` | não gerado: o alvo da referência não tem data-id | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `caminho_do_ancestral_com_id` | `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) > button:nth-of-type(1)` | confere | confere | confere | confere ("Entrar" contra "Entrar": similaridade 1.00 (limiar 0.6)) | não tentado |  |
| `posicao_entre_irmaos` | `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) >> role=button >> nth=0` | confere | confere | confere | confere ("Entrar" contra "Entrar": similaridade 1.00 (limiar 0.6)) | não tentado |  |

Poda de `arvore` (evento 1076): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 9}, depois {"linhas": 6}.

Trecho podado (hash `b2503307a417dec0`):

```text
document "Chuleta Quente - Login"
  text "Login"
  textbox "Login" id="login_usuario" name="login_usuario"
  text "Senha"
  textbox "Senha" id="senha_usuario" name="senha_usuario"
  button "Entrar" class=" btn btn-entrar"

```

## 3. Contraste com a segunda causa

`papel_e_nome` (role=button[name="Entrar"]) e não `texto_contido` (text=Entrar): o segundo também passou as verificações estáticas, mas vem depois na ordem fixa e o primeiro já tinha levado o roteiro ao fim.

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| papel_e_nome | 5 de 5 verificações | sim |
| texto_contido | 4 de 5 verificações |  |
| caminho_do_ancestral_com_id | 4 de 5 verificações |  |
| posicao_entre_irmaos | 4 de 5 verificações |  |

## 4. FONTE declarada e conferida

Não se aplica: a cura de seletor roda sem modelo; nenhum verbete foi citado.

## 5. Linha de ação

Sugestão (o agente não altera a aplicação): no passo 5 do roteiro, trocar o localizador `button.btn-primary` por `role=button[name="Entrar"]` (estratégia `papel_e_nome`), que resolve o mesmo elemento da referência.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cura --saida fase4_cura_reexec --roteiros front-admin-login --modos classe_trocada --formas php --repeticoes 1`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1070 | 1 | entrada | programa | ao_vivo | 2026-11-01T20:04:12 | caso None |
| 1071 | 2 | acao | programa | ao_vivo | 2026-11-01T20:04:18 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 94.1, "falhou": false, "reexecucao": 0} |
| 1072 | 3 | acao | programa | ao_vivo | 2026-11-01T20:04:18 | {"passo": 2, "acao": "esperar", "seletor": "#login_usuario", "url": null, "tempo_ms": 19.8, "falhou": false, "reexecucao": 0} |
| 1073 | 4 | acao | programa | ao_vivo | 2026-11-01T20:04:18 | {"passo": 3, "acao": "preencher", "seletor": "#login_usuario", "url": null, "tempo_ms": 13.9, "falhou": false, "reexecucao": 0} |
| 1074 | 5 | acao | programa | ao_vivo | 2026-11-01T20:04:18 | {"passo": 4, "acao": "preencher", "seletor": "#senha_usuario", "url": null, "tempo_ms": 5.3, "falhou": false, "reexecucao": 0} |
| 1075 | 6 | acao | programa | ao_vivo | 2026-11-01T20:04:18 | {"passo": 5, "acao": "clicar", "seletor": "button.btn-primary", "url": null, "tempo_ms": 5006.5, "falhou": true, "reexecucao": 0} |
| 1076 | 7 | poda | programa | ao_vivo | 2026-11-01T20:04:18 | arvore: 0 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1077 | 8 | cura | programa | ao_vivo | 2026-11-01T20:04:18 | curado: 6 candidatos, 1 reexecução(ões); aplicado papel_e_nome; MTTR 0,4 s |
| 1078 | 9 | decisao | programa | ao_vivo | 2026-11-01T20:04:18 | cura: escolha papel_e_nome; divergência sim |
| 1079 | 10 | acao | programa | ao_vivo | 2026-11-01T20:04:18 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 92.3, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curad |
| 1080 | 11 | acao | programa | ao_vivo | 2026-11-01T20:04:18 | {"passo": 2, "acao": "esperar", "seletor": "#login_usuario", "url": null, "tempo_ms": 20.5, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cura |
| 1081 | 12 | acao | programa | ao_vivo | 2026-11-01T20:04:18 | {"passo": 3, "acao": "preencher", "seletor": "#login_usuario", "url": null, "tempo_ms": 14.8, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cu |
| 1082 | 13 | acao | programa | ao_vivo | 2026-11-01T20:04:18 | {"passo": 4, "acao": "preencher", "seletor": "#senha_usuario", "url": null, "tempo_ms": 4.5, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cur |
| 1083 | 14 | acao | programa | ao_vivo | 2026-11-01T20:04:18 | {"passo": 5, "acao": "clicar", "seletor": "role=button[name=\"Entrar\"]", "url": null, "tempo_ms": 73.7, "falhou": false, "reexecucao": 1, "candidato": "papel_e |
| 1084 | 15 | acao | programa | ao_vivo | 2026-11-01T20:04:18 | {"passo": 6, "acao": "esperar", "seletor": "h1.breadcrumb", "url": null, "tempo_ms": 68.6, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curad |
| 1085 | 16 | acao | programa | ao_vivo | 2026-11-01T20:04:18 | {"passo": 7, "acao": "conferir", "seletor": "h1.breadcrumb", "url": null, "tempo_ms": 12.3, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cura |
| 1086 | 17 | acao | programa | ao_vivo | 2026-11-01T20:04:18 | {"passo": 8, "acao": "conferir", "seletor": null, "url": null, "tempo_ms": 0.0, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado": false} |
| 1087 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T20:04:18 | conferencia_do_roteiro: confere |
| 1088 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T20:04:18 | conferencia_do_roteiro: confere |
| 1089 | 20 | decisao | programa | ao_vivo | 2026-11-01T20:04:18 | reexecucao: escolha validada; divergência não |

</details>

Nós de decisão:

- evento 1078, `cura`: escolha `papel_e_nome`; resultado cura_aplicada; evidência: evento 1077 (candidato_de_seletor), evento 1076 (arvore_podada); divergência: sim; falha: nenhuma; prov.used: papel_e_nome, texto_contido, caminho_do_ancestral_com_id, posicao_entre_irmaos (gen_ai: execute_tool)
- evento 1089, `reexecucao`: escolha `validada`; resultado roteiro_concluido; evidência: evento 1077 (candidato_de_seletor), evento 1087 (sinal_em_codigo), evento 1088 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: papel_e_nome

Sem gabarito nem modelo: a cura de seletor é toda em código; a regra R3 separa o mesmo elemento da referência de outro que fez o roteiro passar.

## Rastro

Gerado dos eventos 1070 a 1089 da trilha; hash dos eventos deste caso: `d042c325b9af6753`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
