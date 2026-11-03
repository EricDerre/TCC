<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `fase4_cura/front-admin-login/classe_trocada/php/r1`: o que o agente fez, declarou e conferiu

Trilha `fase4_cura/front-admin-login/classe_trocada/php/r1`; modelo `(sem modelo: cura de seletor)`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**Cura de seletor:** aplicada: `papel_e_nome` (`role=button[name="Entrar"]`) · reexecução validada · mesmo elemento da referência: sim

Passo 5 do roteiro, localizador `button.btn-primary`: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("button.btn-primary")

Da detecção à reexecução validada: 0,4 s (detecção 2026-11-01T20:04:00; validação 2026-11-01T20:04:01).

Justificativa (gerada por molde): O passo 5 (button.btn-primary) falhou: TimeoutError: Page.click: Timeout 5000ms exceeded. Call log: - waiting for locator("button.btn-primary"). Dos 6 candidatos previstos, 4 foram gerados da árvore podada e do alvo da referência; 4 passaram as quatro verificações em código (um elemento só, visível e habilitado, mesmo papel, nome parecido acima de 0.6). O primeiro que passou, `papel_e_nome` (role=button[name="Entrar"]), levou o roteiro ao fim na reexecução e resolve o mesmo elemento da referência. Da detecção à reexecução validada: 0,4 s.

## 2. Evidência

Alvo registrado na corrida de referência: button "Entrar" (ocorrência 1; tag `button`; caminho `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) > button:nth-of-type(1)`; atributos {"class": " btn btn-primary", "type": "submit"}).

Candidatos na ordem fixa (limiar do nome 0.6); verificações na ordem fixa:

| Estratégia | Seletor | um elemento | visível e habilitado | mesmo papel | nome parecido | efeito na reexecução | Aplicado |
|---|---|---|---|---|---|---|---|
| `papel_e_nome` | `role=button[name="Entrar"]` | confere | confere | confere | confere ("Entrar" contra "Entrar": similaridade 1.00 (limiar 0.6)) | confere (o roteiro chegou ao fim: 2 conferência(s) passaram em 0.305 s) | **sim** |
| `papel_e_nome_parecido` | não gerado: nenhum button da árvore podada tem nome parecido com "Entrar" acima do limiar 0.6 | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `texto_contido` | `text=Entrar` | confere | confere | confere | confere ("Entrar" contra "Entrar": similaridade 1.00 (limiar 0.6)) | não tentado |  |
| `data_id` | não gerado: o alvo da referência não tem data-id | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `caminho_do_ancestral_com_id` | `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) > button:nth-of-type(1)` | confere | confere | confere | confere ("Entrar" contra "Entrar": similaridade 1.00 (limiar 0.6)) | não tentado |  |
| `posicao_entre_irmaos` | `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) >> role=button >> nth=0` | confere | confere | confere | confere ("Entrar" contra "Entrar": similaridade 1.00 (limiar 0.6)) | não tentado |  |

Poda de `arvore` (evento 1016): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 9}, depois {"linhas": 6}.

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
| 1009 | 1 | entrada | programa | ao_vivo | 2026-11-01T20:03:55 | caso None |
| 1010 | 2 | acao | programa | ao_vivo | 2026-11-01T20:04:01 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 61.9, "falhou": false, "reexecucao": 0} |
| 1011 | 3 | acao | programa | ao_vivo | 2026-11-01T20:04:01 | {"passo": 2, "acao": "esperar", "seletor": "#login_usuario", "url": null, "tempo_ms": 31.4, "falhou": false, "reexecucao": 0} |
| 1012 | 4 | acao | programa | ao_vivo | 2026-11-01T20:04:01 | {"passo": 3, "acao": "preencher", "seletor": "#login_usuario", "url": null, "tempo_ms": 15.2, "falhou": false, "reexecucao": 0} |
| 1013 | 5 | acao | programa | ao_vivo | 2026-11-01T20:04:01 | {"passo": 4, "acao": "preencher", "seletor": "#senha_usuario", "url": null, "tempo_ms": 5.6, "falhou": false, "reexecucao": 0} |
| 1014 | 6 | acao | programa | ao_vivo | 2026-11-01T20:04:01 | {"passo": 5, "acao": "clicar", "seletor": "button.btn-primary", "url": null, "tempo_ms": 5011.2, "falhou": true, "reexecucao": 0} |
| 1016 | 7 | poda | programa | ao_vivo | 2026-11-01T20:04:01 | arvore: 0 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1017 | 8 | cura | programa | ao_vivo | 2026-11-01T20:04:01 | curado: 6 candidatos, 1 reexecução(ões); aplicado papel_e_nome; MTTR 0,4 s |
| 1018 | 9 | decisao | programa | ao_vivo | 2026-11-01T20:04:01 | cura: escolha papel_e_nome; divergência sim |
| 1019 | 10 | acao | programa | ao_vivo | 2026-11-01T20:04:01 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 94.1, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curad |
| 1020 | 11 | acao | programa | ao_vivo | 2026-11-01T20:04:01 | {"passo": 2, "acao": "esperar", "seletor": "#login_usuario", "url": null, "tempo_ms": 19.9, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cura |
| 1021 | 12 | acao | programa | ao_vivo | 2026-11-01T20:04:01 | {"passo": 3, "acao": "preencher", "seletor": "#login_usuario", "url": null, "tempo_ms": 15.1, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cu |
| 1022 | 13 | acao | programa | ao_vivo | 2026-11-01T20:04:01 | {"passo": 4, "acao": "preencher", "seletor": "#senha_usuario", "url": null, "tempo_ms": 5.5, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cur |
| 1023 | 14 | acao | programa | ao_vivo | 2026-11-01T20:04:01 | {"passo": 5, "acao": "clicar", "seletor": "role=button[name=\"Entrar\"]", "url": null, "tempo_ms": 81.9, "falhou": false, "reexecucao": 1, "candidato": "papel_e |
| 1024 | 15 | acao | programa | ao_vivo | 2026-11-01T20:04:01 | {"passo": 6, "acao": "esperar", "seletor": "h1.breadcrumb", "url": null, "tempo_ms": 67.4, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curad |
| 1025 | 16 | acao | programa | ao_vivo | 2026-11-01T20:04:01 | {"passo": 7, "acao": "conferir", "seletor": "h1.breadcrumb", "url": null, "tempo_ms": 12.0, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cura |
| 1026 | 17 | acao | programa | ao_vivo | 2026-11-01T20:04:01 | {"passo": 8, "acao": "conferir", "seletor": null, "url": null, "tempo_ms": 0.0, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado": false} |
| 1027 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T20:04:01 | conferencia_do_roteiro: confere |
| 1028 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T20:04:01 | conferencia_do_roteiro: confere |
| 1029 | 20 | decisao | programa | ao_vivo | 2026-11-01T20:04:01 | reexecucao: escolha validada; divergência não |

</details>

Nós de decisão:

- evento 1018, `cura`: escolha `papel_e_nome`; resultado cura_aplicada; evidência: evento 1017 (candidato_de_seletor), evento 1016 (arvore_podada); divergência: sim; falha: nenhuma; prov.used: papel_e_nome, texto_contido, caminho_do_ancestral_com_id, posicao_entre_irmaos (gen_ai: execute_tool)
- evento 1029, `reexecucao`: escolha `validada`; resultado roteiro_concluido; evidência: evento 1017 (candidato_de_seletor), evento 1027 (sinal_em_codigo), evento 1028 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: papel_e_nome

Sem gabarito nem modelo: a cura de seletor é toda em código; a regra R3 separa o mesmo elemento da referência de outro que fez o roteiro passar.

## Rastro

Gerado dos eventos 1009 a 1029 da trilha; hash dos eventos deste caso: `55bcb2344f9dd45a`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
