<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-5`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/sin-5@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `resumo` · selo de probabilidade: **medio** (p = 0,99)

**IMPACTO (declarado):** `O usuário não vê o resumo dos produtos na tela, o que pode causar confusão sobre as características dos itens.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo resumo porque o sinal resumo: esperado texto|nulo, recebido None está presente na resposta HTTP e os verbetes campo_ausente, contrato-produto, entidade-produto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,01 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 217): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 36}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 0 linha(s) novas |

Trecho podado (hash `9495b7027e2ca610`):

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
    group
      heading "Picanha ao Alho" level=3
      text "Carnes"
      text "destaque: Sim"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "destaque: Não"
      button "R$ 69,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 219): regras diff_contra_contrato; antes {"chars": 1469}, depois {"chars": 23}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| resumo | texto\|nulo |  |

Trecho podado (hash `bf2c928ea082e96f`):

```text
{"resumo": "(ausente)"}
```

Interceptação (evento 212): `GET /api/produtos` status 200; corpo `b14075dd059f6770`, árvore `None`.

## 3. Contraste com a segunda causa

campo_ausente e não resposta_truncada: a escolha tem probabilidade 0,99 contra 0,01; verbete(s) na evidência: campo_ausente, contrato-produto, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 0,99 | sim |
| resposta_truncada | 0,01 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente], [contrato-produto]`; verbetes citados: `campo_ausente`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `campo_ausente`, `contrato-produto`, `entidade-produto` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `campo_ausente`, `contrato-produto`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `campo_ausente`, `contrato-produto` |
| fonte_formato_valido | `[campo_ausente], [contrato-produto]` | confere | {"ids": ["campo_ausente", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_ausente` | confere | {"termo": "campo_ausente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `resumo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids sin-5 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 205 | 1 | entrada | programa | ao_vivo | 2026-11-01T11:17:09 | caso sin-5 |
| 206 | 2 | acao | programa | ao_vivo | 2026-11-01T11:17:09 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 184.5, "falhou": false} |
| 207 | 3 | acao | programa | ao_vivo | 2026-11-01T11:17:09 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 8.2, "falhou": false} |
| 208 | 4 | acao | programa | ao_vivo | 2026-11-01T11:17:09 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.3, "falhou": false} |
| 209 | 5 | acao | programa | ao_vivo | 2026-11-01T11:17:09 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 4.1, "falhou": false} |
| 210 | 6 | acao | programa | ao_vivo | 2026-11-01T11:17:09 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 6.0, "falhou": false} |
| 212 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T11:17:09 | GET /api/produtos 200 |
| 213 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T11:17:09 | conferencia_do_roteiro: confere |
| 214 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T11:17:09 | conferencia_do_roteiro: confere |
| 215 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T11:17:09 | conferencia_do_roteiro: confere |
| 217 | 11 | poda | programa | ao_vivo | 2026-11-01T11:17:09 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 219 | 12 | poda | programa | ao_vivo | 2026-11-01T11:17:09 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 220 | 13 | candidatos | programa | ao_vivo | 2026-11-01T11:17:09 | 3 de 40 verbetes entregues |
| 222 | 14 | prompt | programa | ao_vivo | 2026-11-01T11:17:09 | {"etapa": "diagnostico", "sha": "5ee78a5c1f0a328f", "prompt_sha256": "5ee78a5c1f0a", "chars": 5255, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 224 | 15 | inferencia | programa | ao_vivo | 2026-11-01T11:17:09 | diagnostico: 86,4 s |
| 225 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T11:17:09 | causa_raiz: `campo_ausente` |
| 226 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T11:17:09 | campo: `resumo` |
| 227 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T11:17:09 | impacto: `O usuário não vê o resumo dos produtos na tela, o que pode causar confusão sobre as características dos itens.` |
| 228 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T11:17:09 | fonte: `[campo_ausente], [contrato-produto]` |
| 229 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T11:17:09 | fonte_citada: `campo_ausente` |
| 230 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T11:17:09 | fonte_citada: `contrato-produto` |
| 231 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T11:17:09 | quatro_linhas_presentes: confere |
| 232 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T11:17:09 | rotulo_no_conjunto: confere |
| 233 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T11:17:09 | fonte_existe_na_biblioteca: confere |
| 234 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T11:17:09 | fonte_existe_na_biblioteca: confere |
| 235 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T11:17:09 | fonte_estava_no_contexto: confere |
| 236 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T11:17:09 | fonte_estava_no_contexto: confere |
| 237 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T11:17:09 | campo_existe_no_caso: confere |
| 238 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T11:17:09 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 239 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T11:17:09 | notas_nos_verbetes_citados: informativo |
| 240 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T11:17:09 | impacto: nao_verificavel |
| 241 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T11:17:09 | fonte_formato_valido: confere |
| 242 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T11:17:09 | fonte_contem_termo_da_causa: confere |
| 243 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T11:17:09 | fonte_contem_termo_da_causa: nao_confere |
| 244 | 35 | decisao | programa | ao_vivo | 2026-11-01T11:17:09 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 244, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 219 (sinal_em_codigo), evento 217 (arvore_podada), evento 212 (corpo_http), evento 220 (verbete_entregue, campo_ausente), evento 220 (verbete_entregue, contrato-produto), evento 220 (verbete_entregue, entidade-produto), evento 224 (resposta), evento 229 (verbete_citado, campo_ausente), evento 230 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: campo_ausente, contrato-produto, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 205 a 244 da trilha; hash dos eventos deste caso: `ca441b25174a6312`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
