<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-2`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/run-2@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tempo_de_resposta_excedido` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,98) · **CONFLITO**: nenhum verbete entregue trata da causa respondida tempo_de_resposta_excedido

**IMPACTO (declarado):** `O usuário experimentou uma resposta muito lenta, o que pode levar a uma experiência ruim e potencialmente interromper a interação com a interface.`

Justificativa (gerada por molde): O agente respondeu tempo_de_resposta_excedido no campo tempo_ms porque o sinal tempo_ms: esperado 158 ms (referência em modo normal), recebido 28033 ms está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, contagem_inconsistente estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida tempo_de_resposta_excedido. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Poda de `arvore` (evento 522): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 0 linha(s) da referência | 0 linha(s) novas |

Trecho podado (hash `e4870f4dbbc1b73d`):

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
      text "Picanha grelhada com alho laminado na brasa"
      text "destaque: Sim"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
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

Poda de `corpo_http` (evento 524): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2068}, depois {"chars": 244}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tempo_ms | 158 ms (referência em modo normal) | 28033 ms |

Trecho podado (hash `59922d051a426b7b`):

```text
lista com 14 itens, igual à referência em modo normal; primeiro item: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 518): `GET /api/produtos` status 200; corpo `4b1bdd056e7a8c3b`, árvore `None`.

## 3. Contraste com a segunda causa

tempo_de_resposta_excedido e não formato_de_data_divergente: a escolha tem probabilidade 0,98 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, contagem_inconsistente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tempo_de_resposta_excedido | 0,98 | sim |
| formato_de_data_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| resposta_truncada | 0,00 |  |
| contagem_inconsistente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [contagem_inconsistente]`; verbetes citados: `contrato-produto`, `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente` |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente` |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto], [contagem_inconsistente]` | confere | {"ids": ["contrato-produto", "contagem_inconsistente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tempo_de_resposta_excedido"} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | **não confere** | {"termo": "tempo_de_resposta_excedido"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids run-2 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 512 | 1 | entrada | programa | ao_vivo | 2026-11-01T14:28:12 | caso run-2 |
| 513 | 2 | acao | programa | ao_vivo | 2026-11-01T14:28:40 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 114.7, "falhou": false} |
| 514 | 3 | acao | programa | ao_vivo | 2026-11-01T14:28:40 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 28150.9, "falhou": false |
| 515 | 4 | acao | programa | ao_vivo | 2026-11-01T14:28:40 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 3.6, "falhou": false} |
| 516 | 5 | acao | programa | ao_vivo | 2026-11-01T14:28:40 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 6.0, "falhou": false} |
| 517 | 6 | acao | programa | ao_vivo | 2026-11-01T14:28:40 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.6, "falhou": false} |
| 518 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T14:28:40 | GET /api/produtos 200 |
| 519 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T14:28:40 | conferencia_do_roteiro: confere |
| 520 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T14:28:40 | conferencia_do_roteiro: confere |
| 521 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T14:28:40 | conferencia_do_roteiro: confere |
| 522 | 11 | poda | programa | ao_vivo | 2026-11-01T14:28:40 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 524 | 12 | poda | programa | ao_vivo | 2026-11-01T14:28:40 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 525 | 13 | candidatos | programa | ao_vivo | 2026-11-01T14:28:40 | 3 de 40 verbetes entregues |
| 527 | 14 | prompt | programa | ao_vivo | 2026-11-01T14:28:40 | {"etapa": "diagnostico", "sha": "0772cf4821e5141b", "prompt_sha256": "0772cf4821e5", "chars": 5455, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 529 | 15 | inferencia | programa | ao_vivo | 2026-11-01T14:28:40 | diagnostico: 66,1 s |
| 530 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T14:28:40 | causa_raiz: `tempo_de_resposta_excedido` |
| 531 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T14:28:40 | campo: `nenhum` |
| 532 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T14:28:40 | impacto: `O usuário experimentou uma resposta muito lenta, o que pode levar a uma experiência ruim e potencialmente interromper a interação com a interface.` |
| 533 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T14:28:40 | fonte: `[contrato-produto], [contagem_inconsistente]` |
| 534 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T14:28:40 | fonte_citada: `contrato-produto` |
| 535 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T14:28:40 | fonte_citada: `contagem_inconsistente` |
| 536 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T14:28:40 | quatro_linhas_presentes: confere |
| 537 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T14:28:40 | rotulo_no_conjunto: confere |
| 538 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T14:28:40 | fonte_existe_na_biblioteca: confere |
| 539 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T14:28:40 | fonte_existe_na_biblioteca: confere |
| 540 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T14:28:40 | fonte_estava_no_contexto: confere |
| 541 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T14:28:40 | fonte_estava_no_contexto: confere |
| 542 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T14:28:40 | campo_existe_no_caso: nao_se_aplica |
| 543 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T14:28:40 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 544 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T14:28:40 | notas_nos_verbetes_citados: informativo |
| 545 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T14:28:40 | impacto: nao_verificavel |
| 546 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T14:28:40 | fonte_formato_valido: confere |
| 547 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T14:28:40 | fonte_contem_termo_da_causa: nao_confere |
| 548 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T14:28:40 | fonte_contem_termo_da_causa: nao_confere |
| 549 | 35 | decisao | programa | ao_vivo | 2026-11-01T14:28:40 | diagnostico: escolha tempo_de_resposta_excedido; divergência sim |

</details>

Nós de decisão:

- evento 549, `diagnostico`: escolha `tempo_de_resposta_excedido`; resultado rotulo_emitido; evidência: evento 524 (sinal_em_codigo), evento 522 (arvore_podada), evento 518 (corpo_http), evento 525 (verbete_entregue, entidade-produto), evento 525 (verbete_entregue, contrato-produto), evento 525 (verbete_entregue, contagem_inconsistente), evento 529 (resposta), evento 534 (verbete_citado, contrato-produto), evento 535 (verbete_citado, contagem_inconsistente); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, contagem_inconsistente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 512 a 549 da trilha; hash dos eventos deste caso: `7ae3672fd4a0d040`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
