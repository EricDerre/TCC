<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-8`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/semt-8@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `nulo_inesperado` · **CAMPO:** `preco` · selo de probabilidade: **medio** (p = 0,96)

**IMPACTO (declarado):** `O usuário vê preços nulos nos botões de detalhes, o que pode levar a confusão sobre os preços reais dos produtos.`

Justificativa (gerada por molde): O agente respondeu nulo_inesperado no campo preco porque o sinal preco: esperado numero, recebido nulo está presente na resposta HTTP e os verbetes campo_ausente, nulo_inesperado, contrato-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,01. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1004): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `95567b9d021da4fd`):

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
      button "R$ 0,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 0,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "R$ 0,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 1006): regras diff_contra_contrato; antes {"chars": 2070}, depois {"chars": 15}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | numero | nulo |

Trecho podado (hash `d2144c0056fc65c7`):

```text
{"preco": null}
```

Interceptação (evento 999): `GET /api/produtos` status 200; corpo `8d871a2a7b69d75c`, árvore `None`.

## 3. Contraste com a segunda causa

nulo_inesperado e não tipo_divergente: a escolha tem probabilidade 0,96 contra 0,01; verbete(s) na evidência: campo_ausente, nulo_inesperado, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| nulo_inesperado | 0,96 | sim |
| tipo_divergente | 0,01 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| corpo_nao_e_json | 0,01 |  |
| corpo_vazio | 0,01 |  |
| valor_fora_do_dominio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[nulo_inesperado]`; verbetes citados: `nulo_inesperado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `campo_ausente`, `nulo_inesperado`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `campo_ausente`, `nulo_inesperado` |
| fonte_formato_valido | `[nulo_inesperado]` | confere | {"ids": ["nulo_inesperado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids semt-8 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 992 | 1 | entrada | programa | ao_vivo | 2026-11-01T11:48:00 | caso semt-8 |
| 993 | 2 | acao | programa | ao_vivo | 2026-11-01T11:48:01 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 114.8, "falhou": false} |
| 994 | 3 | acao | programa | ao_vivo | 2026-11-01T11:48:01 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 9.9, "falhou": false} |
| 995 | 4 | acao | programa | ao_vivo | 2026-11-01T11:48:01 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 4.0, "falhou": false} |
| 996 | 5 | acao | programa | ao_vivo | 2026-11-01T11:48:01 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 7.5, "falhou": false} |
| 997 | 6 | acao | programa | ao_vivo | 2026-11-01T11:48:01 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 5.7, "falhou": false} |
| 999 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T11:48:01 | GET /api/produtos 200 |
| 1000 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T11:48:01 | conferencia_do_roteiro: confere |
| 1001 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T11:48:01 | conferencia_do_roteiro: confere |
| 1002 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T11:48:01 | conferencia_do_roteiro: confere |
| 1004 | 11 | poda | programa | ao_vivo | 2026-11-01T11:48:01 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1006 | 12 | poda | programa | ao_vivo | 2026-11-01T11:48:01 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1007 | 13 | candidatos | programa | ao_vivo | 2026-11-01T11:48:01 | 3 de 40 verbetes entregues |
| 1009 | 14 | prompt | programa | ao_vivo | 2026-11-01T11:48:01 | {"etapa": "diagnostico", "sha": "8c6e2d2144192a76", "prompt_sha256": "8c6e2d214419", "chars": 5186, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1011 | 15 | inferencia | programa | ao_vivo | 2026-11-01T11:48:01 | diagnostico: 93,1 s |
| 1012 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T11:48:01 | causa_raiz: `nulo_inesperado` |
| 1013 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T11:48:01 | campo: `preco` |
| 1014 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T11:48:01 | impacto: `O usuário vê preços nulos nos botões de detalhes, o que pode levar a confusão sobre os preços reais dos produtos.` |
| 1015 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T11:48:01 | fonte: `[nulo_inesperado]` |
| 1016 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T11:48:01 | fonte_citada: `nulo_inesperado` |
| 1017 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T11:48:01 | quatro_linhas_presentes: confere |
| 1018 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T11:48:01 | rotulo_no_conjunto: confere |
| 1019 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T11:48:01 | fonte_existe_na_biblioteca: confere |
| 1020 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T11:48:01 | fonte_estava_no_contexto: confere |
| 1021 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T11:48:01 | campo_existe_no_caso: confere |
| 1022 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T11:48:01 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1023 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T11:48:01 | notas_nos_verbetes_citados: informativo |
| 1024 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T11:48:01 | impacto: nao_verificavel |
| 1025 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T11:48:01 | fonte_formato_valido: confere |
| 1026 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T11:48:01 | fonte_contem_termo_da_causa: confere |
| 1027 | 31 | decisao | programa | ao_vivo | 2026-11-01T11:48:01 | diagnostico: escolha nulo_inesperado; divergência não |

</details>

Nós de decisão:

- evento 1027, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 1006 (sinal_em_codigo), evento 1004 (arvore_podada), evento 999 (corpo_http), evento 1007 (verbete_entregue, campo_ausente), evento 1007 (verbete_entregue, nulo_inesperado), evento 1007 (verbete_entregue, contrato-produto), evento 1011 (resposta), evento 1016 (verbete_citado, nulo_inesperado); divergência: não; falha: nenhuma; prov.used: campo_ausente, nulo_inesperado, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 992 a 1027 da trilha; hash dos eventos deste caso: `a86d89925b743008`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
