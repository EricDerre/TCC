<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `fase4_cura/front-admin-login/texto_alterado/harness/r3`: o que o agente fez, declarou e conferiu

Trilha `fase4_cura/front-admin-login/texto_alterado/harness/r3`; modelo `(sem modelo: cura de seletor)`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**Cura de seletor:** aplicada: `papel_e_nome_parecido` (`role=button[name="Entrar agora"]`) · reexecução validada · mesmo elemento da referência: sim

Passo 5 do roteiro, localizador `role=button[name="Entrar"]`: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("role=button[name=\"Entrar\"]")

Da detecção à reexecução validada: 0,4 s (detecção 2026-11-01T20:04:40; validação 2026-11-01T20:04:41).

Justificativa (gerada por molde): O passo 5 (role=button[name="Entrar"]) falhou: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("role=button[name=\"Entrar\"]"). Dos 6 candidatos previstos, 4 foram gerados da árvore podada e do alvo da referência; 4 passaram as quatro verificações em código (um elemento só, visível e habilitado, mesmo papel, nome parecido acima de 0.6). O primeiro que passou, `papel_e_nome_parecido` (role=button[name="Entrar agora"]), levou o roteiro ao fim na reexecução e resolve o mesmo elemento da referência. Da detecção à reexecução validada: 0,4 s.

## 2. Evidência

Alvo registrado na corrida de referência: button "Entrar" (ocorrência 1; tag `button`; caminho `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) > button:nth-of-type(1)`; atributos {"class": " btn btn-primary", "type": "submit"}).

Candidatos na ordem fixa (limiar do nome 0.6); verificações na ordem fixa:

| Estratégia | Seletor | um elemento | visível e habilitado | mesmo papel | nome parecido | efeito na reexecução | Aplicado |
|---|---|---|---|---|---|---|---|
| `papel_e_nome` | não gerado: a árvore podada não tem button "Entrar" | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `papel_e_nome_parecido` | `role=button[name="Entrar agora"]` | confere | confere | confere | confere ("Entrar agora" contra "Entrar": similaridade 0.67 (limiar 0.6)) | confere (o roteiro chegou ao fim: 2 conferência(s) passaram em 0.281 s) | **sim** |
| `texto_contido` | `text=Entrar` | confere | confere | confere | confere ("Entrar agora" contra "Entrar": similaridade 0.67 (limiar 0.6)) | não tentado |  |
| `data_id` | não gerado: o alvo da referência não tem data-id | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `caminho_do_ancestral_com_id` | `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) > button:nth-of-type(1)` | confere | confere | confere | confere ("Entrar agora" contra "Entrar": similaridade 0.67 (limiar 0.6)) | não tentado |  |
| `posicao_entre_irmaos` | `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) >> role=button >> nth=0` | confere | confere | confere | confere ("Entrar agora" contra "Entrar": similaridade 0.67 (limiar 0.6)) | não tentado |  |

Poda de `arvore` (evento 1159): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 9}, depois {"linhas": 6}.

Trecho podado (hash `ceb745009113e60d`):

```text
document "Chuleta Quente - Login"
  text "Login"
  textbox "Login" id="login_usuario" name="login_usuario"
  text "Senha"
  textbox "Senha" id="senha_usuario" name="senha_usuario"
  button "Entrar agora" class=" btn btn-primary"

```

## 3. Contraste com a segunda causa

`papel_e_nome_parecido` (role=button[name="Entrar agora"]) e não `texto_contido` (text=Entrar): o segundo também passou as verificações estáticas, mas vem depois na ordem fixa e o primeiro já tinha levado o roteiro ao fim.

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| papel_e_nome_parecido | 5 de 5 verificações | sim |
| texto_contido | 4 de 5 verificações |  |
| caminho_do_ancestral_com_id | 4 de 5 verificações |  |
| posicao_entre_irmaos | 4 de 5 verificações |  |

## 4. FONTE declarada e conferida

Não se aplica: a cura de seletor roda sem modelo; nenhum verbete foi citado.

## 5. Linha de ação

Sugestão (o agente não altera a aplicação): no passo 5 do roteiro, trocar o localizador `role=button[name="Entrar"]` por `role=button[name="Entrar agora"]` (estratégia `papel_e_nome_parecido`), que resolve o mesmo elemento da referência.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cura --saida fase4_cura_reexec --roteiros front-admin-login --modos texto_alterado --formas harness --repeticoes 1`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1153 | 1 | entrada | programa | ao_vivo | 2026-11-01T20:04:35 | caso None |
| 1154 | 2 | acao | programa | ao_vivo | 2026-11-01T20:04:41 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 93.2, "falhou": false, "reexecucao": 0} |
| 1155 | 3 | acao | programa | ao_vivo | 2026-11-01T20:04:41 | {"passo": 2, "acao": "esperar", "seletor": "#login_usuario", "url": null, "tempo_ms": 19.1, "falhou": false, "reexecucao": 0} |
| 1156 | 4 | acao | programa | ao_vivo | 2026-11-01T20:04:41 | {"passo": 3, "acao": "preencher", "seletor": "#login_usuario", "url": null, "tempo_ms": 14.2, "falhou": false, "reexecucao": 0} |
| 1157 | 5 | acao | programa | ao_vivo | 2026-11-01T20:04:41 | {"passo": 4, "acao": "preencher", "seletor": "#senha_usuario", "url": null, "tempo_ms": 4.5, "falhou": false, "reexecucao": 0} |
| 1158 | 6 | acao | programa | ao_vivo | 2026-11-01T20:04:41 | {"passo": 5, "acao": "clicar", "seletor": "role=button[name=\"Entrar\"]", "url": null, "tempo_ms": 5012.0, "falhou": true, "reexecucao": 0} |
| 1159 | 7 | poda | programa | ao_vivo | 2026-11-01T20:04:41 | arvore: 0 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1160 | 8 | cura | programa | ao_vivo | 2026-11-01T20:04:41 | curado: 6 candidatos, 1 reexecução(ões); aplicado papel_e_nome_parecido; MTTR 0,4 s |
| 1161 | 9 | decisao | programa | ao_vivo | 2026-11-01T20:04:41 | cura: escolha papel_e_nome_parecido; divergência sim |
| 1162 | 10 | acao | programa | ao_vivo | 2026-11-01T20:04:41 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 77.1, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome_parecido |
| 1163 | 11 | acao | programa | ao_vivo | 2026-11-01T20:04:41 | {"passo": 2, "acao": "esperar", "seletor": "#login_usuario", "url": null, "tempo_ms": 20.0, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome_parecid |
| 1164 | 12 | acao | programa | ao_vivo | 2026-11-01T20:04:41 | {"passo": 3, "acao": "preencher", "seletor": "#login_usuario", "url": null, "tempo_ms": 13.0, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome_parec |
| 1165 | 13 | acao | programa | ao_vivo | 2026-11-01T20:04:41 | {"passo": 4, "acao": "preencher", "seletor": "#senha_usuario", "url": null, "tempo_ms": 6.3, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome_pareci |
| 1166 | 14 | acao | programa | ao_vivo | 2026-11-01T20:04:41 | {"passo": 5, "acao": "clicar", "seletor": "role=button[name=\"Entrar agora\"]", "url": null, "tempo_ms": 74.8, "falhou": false, "reexecucao": 1, "candidato": "p |
| 1167 | 15 | acao | programa | ao_vivo | 2026-11-01T20:04:41 | {"passo": 6, "acao": "esperar", "seletor": "h1.breadcrumb", "url": null, "tempo_ms": 69.1, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome_parecido |
| 1168 | 16 | acao | programa | ao_vivo | 2026-11-01T20:04:41 | {"passo": 7, "acao": "conferir", "seletor": "h1.breadcrumb", "url": null, "tempo_ms": 12.3, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome_parecid |
| 1169 | 17 | acao | programa | ao_vivo | 2026-11-01T20:04:41 | {"passo": 8, "acao": "conferir", "seletor": null, "url": null, "tempo_ms": 0.0, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome_parecido", "curado" |
| 1170 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T20:04:41 | conferencia_do_roteiro: confere |
| 1171 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T20:04:41 | conferencia_do_roteiro: confere |
| 1172 | 20 | decisao | programa | ao_vivo | 2026-11-01T20:04:41 | reexecucao: escolha validada; divergência não |

</details>

Nós de decisão:

- evento 1161, `cura`: escolha `papel_e_nome_parecido`; resultado cura_aplicada; evidência: evento 1160 (candidato_de_seletor), evento 1159 (arvore_podada); divergência: sim; falha: nenhuma; prov.used: papel_e_nome_parecido, texto_contido, caminho_do_ancestral_com_id, posicao_entre_irmaos (gen_ai: execute_tool)
- evento 1172, `reexecucao`: escolha `validada`; resultado roteiro_concluido; evidência: evento 1160 (candidato_de_seletor), evento 1170 (sinal_em_codigo), evento 1171 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: papel_e_nome_parecido

Sem gabarito nem modelo: a cura de seletor é toda em código; a regra R3 separa o mesmo elemento da referência de outro que fez o roteiro passar.

## Rastro

Gerado dos eventos 1153 a 1172 da trilha; hash dos eventos deste caso: `e25136f51dc25656`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
