<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `fase4_cura/front-admin-login/id_renomeado/harness/r4`: o que o agente fez, declarou e conferiu

Trilha `fase4_cura/front-admin-login/id_renomeado/harness/r4`; modelo `(sem modelo: cura de seletor)`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**Cura de seletor:** aplicada: `papel_e_nome` (`role=textbox[name="Login"]`) · reexecução validada · mesmo elemento da referência: sim

Passo 2 do roteiro, localizador `#login_usuario`: TimeoutError: Page.wait_for_selector: Timeout 5000ms exceeded. Call log: - waiting for locator("#login_usuario") to be visible

Da detecção à reexecução validada: 0,4 s (detecção 2026-11-01T20:02:53; validação 2026-11-01T20:02:53).

Justificativa (gerada por molde): O passo 2 (#login_usuario) falhou: TimeoutError: Page.wait_for_selector: Timeout 5000ms exceeded. Call log: - waiting for locator("#login_usuario") to be visible. Dos 6 candidatos previstos, 3 foram gerados da árvore podada e do alvo da referência; 3 passaram as quatro verificações em código (um elemento só, visível e habilitado, mesmo papel, nome parecido acima de 0.6). O primeiro que passou, `papel_e_nome` (role=textbox[name="Login"]), levou o roteiro ao fim na reexecução e resolve o mesmo elemento da referência. Da detecção à reexecução validada: 0,4 s.

## 2. Evidência

Alvo registrado na corrida de referência: textbox "Login" (ocorrência 1; tag `input`; caminho `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) > div:nth-of-type(1) > input:nth-of-type(1)`; atributos {"id": "login_usuario", "name": "login_usuario", "type": "text", "placeholder": "Digite seu login."}).

Candidatos na ordem fixa (limiar do nome 0.6); verificações na ordem fixa:

| Estratégia | Seletor | um elemento | visível e habilitado | mesmo papel | nome parecido | efeito na reexecução | Aplicado |
|---|---|---|---|---|---|---|---|
| `papel_e_nome` | `role=textbox[name="Login"]` | confere | confere | confere | confere ("Login" contra "Login": similaridade 1.00 (limiar 0.6)) | confere (o roteiro chegou ao fim: 2 conferência(s) passaram em 0.281 s) | **sim** |
| `papel_e_nome_parecido` | não gerado: nenhum textbox da árvore podada tem nome parecido com "Login" acima do limiar 0.6 (o mais próximo, "Senha", fica em 0.20) | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `texto_contido` | não gerado: o alvo da referência não tem texto visível | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `data_id` | não gerado: o alvo da referência não tem data-id | não se aplica | não se aplica | não se aplica | não se aplica | não se aplica |  |
| `caminho_do_ancestral_com_id` | `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) > div:nth-of-type(1) > input:nth-of-type(1)` | confere | confere | confere | confere ("Login" contra "Login": similaridade 1.00 (limiar 0.6)) | não tentado |  |
| `posicao_entre_irmaos` | `body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) > div:nth-of-type(1) >> role=textbox >> nth=0` | confere | confere | confere | confere ("Login" contra "Login": similaridade 1.00 (limiar 0.6)) | não tentado |  |

Poda de `arvore` (evento 790): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 7}, depois {"linhas": 6}.

Trecho podado (hash `30dd50a6666b3e83`):

```text
document "Chuleta Quente - Login"
  text "Login"
  textbox "Login" id="usuario" name="login_usuario"
  text "Senha"
  textbox "Senha" id="senha_usuario" name="senha_usuario"
  button "Entrar" class=" btn btn-primary"

```

## 3. Contraste com a segunda causa

`papel_e_nome` (role=textbox[name="Login"]) e não `caminho_do_ancestral_com_id` (body > div:nth-of-type(1) > div:nth-of-type(1) > form:nth-of-type(1) > div:nth-of-type(1) > input:nth-of-type(1)): o segundo também passou as verificações estáticas, mas vem depois na ordem fixa e o primeiro já tinha levado o roteiro ao fim.

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| papel_e_nome | 5 de 5 verificações | sim |
| caminho_do_ancestral_com_id | 4 de 5 verificações |  |
| posicao_entre_irmaos | 4 de 5 verificações |  |

## 4. FONTE declarada e conferida

Não se aplica: a cura de seletor roda sem modelo; nenhum verbete foi citado.

## 5. Linha de ação

Sugestão (o agente não altera a aplicação): no passo 2 do roteiro, trocar o localizador `#login_usuario` por `role=textbox[name="Login"]` (estratégia `papel_e_nome`), que resolve o mesmo elemento da referência.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cura --saida fase4_cura_reexec --roteiros front-admin-login --modos id_renomeado --formas harness --repeticoes 1`

## 6. Árvore completa

<details><summary>17 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 787 | 1 | entrada | programa | ao_vivo | 2026-11-01T20:02:48 | caso None |
| 788 | 2 | acao | programa | ao_vivo | 2026-11-01T20:02:53 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 65.9, "falhou": false, "reexecucao": 0} |
| 789 | 3 | acao | programa | ao_vivo | 2026-11-01T20:02:53 | {"passo": 2, "acao": "esperar", "seletor": "#login_usuario", "url": null, "tempo_ms": 5018.6, "falhou": true, "reexecucao": 0} |
| 790 | 4 | poda | programa | ao_vivo | 2026-11-01T20:02:53 | arvore: 0 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 791 | 5 | cura | programa | ao_vivo | 2026-11-01T20:02:53 | curado: 6 candidatos, 1 reexecução(ões); aplicado papel_e_nome; MTTR 0,4 s |
| 792 | 6 | decisao | programa | ao_vivo | 2026-11-01T20:02:53 | cura: escolha papel_e_nome; divergência sim |
| 793 | 7 | acao | programa | ao_vivo | 2026-11-01T20:02:53 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "admin/login.php", "tempo_ms": 82.0, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curad |
| 794 | 8 | acao | programa | ao_vivo | 2026-11-01T20:02:53 | {"passo": 2, "acao": "esperar", "seletor": "role=textbox[name=\"Login\"]", "url": null, "tempo_ms": 3.2, "falhou": false, "reexecucao": 1, "candidato": "papel_e |
| 795 | 9 | acao | programa | ao_vivo | 2026-11-01T20:02:53 | {"passo": 3, "acao": "preencher", "seletor": "role=textbox[name=\"Login\"]", "url": null, "tempo_ms": 5.5, "falhou": false, "reexecucao": 1, "candidato": "papel |
| 796 | 10 | acao | programa | ao_vivo | 2026-11-01T20:02:53 | {"passo": 4, "acao": "preencher", "seletor": "#senha_usuario", "url": null, "tempo_ms": 6.8, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cur |
| 797 | 11 | acao | programa | ao_vivo | 2026-11-01T20:02:53 | {"passo": 5, "acao": "clicar", "seletor": "button[type=submit]", "url": null, "tempo_ms": 68.5, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", " |
| 798 | 12 | acao | programa | ao_vivo | 2026-11-01T20:02:53 | {"passo": 6, "acao": "esperar", "seletor": "h1.breadcrumb", "url": null, "tempo_ms": 67.7, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curad |
| 799 | 13 | acao | programa | ao_vivo | 2026-11-01T20:02:53 | {"passo": 7, "acao": "conferir", "seletor": "h1.breadcrumb", "url": null, "tempo_ms": 10.9, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "cura |
| 800 | 14 | acao | programa | ao_vivo | 2026-11-01T20:02:53 | {"passo": 8, "acao": "conferir", "seletor": null, "url": null, "tempo_ms": 0.0, "falhou": false, "reexecucao": 1, "candidato": "papel_e_nome", "curado": false} |
| 801 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T20:02:53 | conferencia_do_roteiro: confere |
| 802 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T20:02:53 | conferencia_do_roteiro: confere |
| 803 | 17 | decisao | programa | ao_vivo | 2026-11-01T20:02:53 | reexecucao: escolha validada; divergência não |

</details>

Nós de decisão:

- evento 792, `cura`: escolha `papel_e_nome`; resultado cura_aplicada; evidência: evento 791 (candidato_de_seletor), evento 790 (arvore_podada); divergência: sim; falha: nenhuma; prov.used: papel_e_nome, caminho_do_ancestral_com_id, posicao_entre_irmaos (gen_ai: execute_tool)
- evento 803, `reexecucao`: escolha `validada`; resultado roteiro_concluido; evidência: evento 791 (candidato_de_seletor), evento 801 (sinal_em_codigo), evento 802 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: papel_e_nome

Sem gabarito nem modelo: a cura de seletor é toda em código; a regra R3 separa o mesmo elemento da referência de outro que fez o roteiro passar.

## Rastro

Gerado dos eventos 787 a 803 da trilha; hash dos eventos deste caso: `3877b30c83fab5bb`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
