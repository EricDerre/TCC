<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-13`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/semt-13@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `preco` · selo de probabilidade: **alto** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê o preço formatado corretamente, mas a API retorna o preço como texto em vez de número.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo preco porque o sinal preco: esperado numero, recebido texto está presente na resposta HTTP e os verbetes campo_ausente, contrato-produto, campo_renomeado, entidade-produto estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 1 recusada(s) (teto_notas_verbete) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 1 edição(ões) para o caso semt-13. A proposta 1 (nota em [tipo_divergente]) foi recusada por a validação da Fase 3 com o código teto_notas_verbete: [tipo_divergente] ficaria com 871 caracteres de notas (teto 800).

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `tipo_divergente` | recusada: `teto_notas_verbete` | nenhum | recusada: `teto_notas_verbete` |  |

Poda de `arvore` (evento 1087): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 1089): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2096}, depois {"chars": 17}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | numero | texto |
| preco | 89.9 (referência em modo normal) | "89.9" em 14 itens |

Trecho podado (hash `b48b1bab39e02551`):

```text
{"preco": "89.9"}
```

Interceptação (evento 1083): `GET /api/produtos` status 200; corpo `c7c256cfe391ed57`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: campo_ausente, contrato-produto, campo_renomeado, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,99 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [campo_ausente]`; verbetes citados: `contrato-produto`, `campo_ausente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `campo_ausente`, `contrato-produto`, `campo_renomeado`, `entidade-produto` |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `campo_ausente`, `contrato-produto`, `campo_renomeado`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `contrato-produto`, `entidade-produto` |
| fonte_formato_valido | `[contrato-produto] [campo_ausente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto", "campo_ausente"]} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `campo_ausente` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>38 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1076 | 1 | entrada | programa | ao_vivo | 2026-11-03T22:53:08 | caso semt-13 |
| 1077 | 2 | acao | programa | ao_vivo | 2026-11-03T22:53:08 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 92.5, "url": "produtos_api.php"} |
| 1078 | 3 | acao | programa | ao_vivo | 2026-11-03T22:53:08 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 7.7, "url": null} |
| 1079 | 4 | acao | programa | ao_vivo | 2026-11-03T22:53:08 | {"acao": "conferir", "falhou": false, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 2.4, "url": null} |
| 1080 | 5 | acao | programa | ao_vivo | 2026-11-03T22:53:08 | {"acao": "conferir", "falhou": false, "passo": 4, "seletor": "#produtos-api-grid .thumbnail .btn-default", "tempo_ms": 5.3, "url": null} |
| 1081 | 6 | acao | programa | ao_vivo | 2026-11-03T22:53:08 | {"acao": "conferir", "falhou": false, "passo": 5, "seletor": "#produtos-api-status", "tempo_ms": 3.1, "url": null} |
| 1083 | 7 | interceptacao | programa | ao_vivo | 2026-11-03T22:53:08 | GET /api/produtos 200 |
| 1084 | 8 | verificacao | verificacao | ao_vivo | 2026-11-03T22:53:08 | conferencia_do_roteiro: confere |
| 1085 | 9 | verificacao | verificacao | ao_vivo | 2026-11-03T22:53:08 | conferencia_do_roteiro: confere |
| 1086 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T22:53:08 | conferencia_do_roteiro: confere |
| 1087 | 11 | poda | programa | ao_vivo | 2026-11-03T22:53:08 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 1089 | 12 | poda | programa | ao_vivo | 2026-11-03T22:53:08 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1090 | 13 | candidatos | programa | ao_vivo | 2026-11-03T22:53:08 | 3 de 40 verbetes entregues |
| 1092 | 14 | prompt | programa | ao_vivo | 2026-11-03T22:53:08 | {"chars": 5888, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "bf94a94a1daa", "sha": "bf94a94a1daa824c"} |
| 1094 | 15 | inferencia | programa | ao_vivo | 2026-11-03T22:53:08 | diagnostico: 106,3 s |
| 1095 | 16 | declaracao | modelo | ao_vivo | 2026-11-03T22:53:08 | causa_raiz: `tipo_divergente` |
| 1096 | 17 | declaracao | modelo | ao_vivo | 2026-11-03T22:53:08 | campo: `preco` |
| 1097 | 18 | declaracao | modelo | ao_vivo | 2026-11-03T22:53:08 | impacto: `O usuário vê o preço formatado corretamente, mas a API retorna o preço como texto em vez de número.` |
| 1098 | 19 | declaracao | modelo | ao_vivo | 2026-11-03T22:53:08 | fonte: `[contrato-produto] [campo_ausente]` |
| 1099 | 20 | declaracao | modelo | ao_vivo | 2026-11-03T22:53:08 | fonte_citada: `contrato-produto` |
| 1100 | 21 | declaracao | modelo | ao_vivo | 2026-11-03T22:53:08 | fonte_citada: `campo_ausente` |
| 1101 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T22:53:08 | quatro_linhas_presentes: confere |
| 1102 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T22:53:08 | rotulo_no_conjunto: confere |
| 1103 | 24 | verificacao | verificacao | ao_vivo | 2026-11-03T22:53:08 | fonte_existe_na_biblioteca: confere |
| 1104 | 25 | verificacao | verificacao | ao_vivo | 2026-11-03T22:53:08 | fonte_existe_na_biblioteca: confere |
| 1105 | 26 | verificacao | verificacao | ao_vivo | 2026-11-03T22:53:08 | fonte_estava_no_contexto: confere |
| 1106 | 27 | verificacao | verificacao | ao_vivo | 2026-11-03T22:53:08 | fonte_estava_no_contexto: confere |
| 1107 | 28 | verificacao | verificacao | ao_vivo | 2026-11-03T22:53:08 | campo_existe_no_caso: confere |
| 1108 | 29 | verificacao | verificacao | ao_vivo | 2026-11-03T22:53:08 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1109 | 30 | verificacao | verificacao | ao_vivo | 2026-11-03T22:53:08 | notas_nos_verbetes_citados: informativo |
| 1110 | 31 | verificacao | verificacao | ao_vivo | 2026-11-03T22:53:08 | impacto: nao_verificavel |
| 1111 | 32 | verificacao | verificacao | ao_vivo | 2026-11-03T22:53:08 | fonte_formato_valido: confere |
| 1112 | 33 | verificacao | verificacao | ao_vivo | 2026-11-03T22:53:08 | fonte_contem_termo_da_causa: nao_confere |
| 1113 | 34 | verificacao | verificacao | ao_vivo | 2026-11-03T22:53:08 | fonte_contem_termo_da_causa: nao_confere |
| 1114 | 35 | decisao | programa | ao_vivo | 2026-11-03T22:53:08 | diagnostico: escolha tipo_divergente; divergência não |
| 1117 | 36 | inferencia | programa | ao_vivo | 2026-11-03T22:54:58 | proposta: 108,6 s |
| 1119 | 37 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:54:58 | proposta 1: nota em [tipo_divergente]: recusada: teto_notas_verbete |
| 1120 | 38 | decisao | programa | ao_vivo | 2026-11-03T22:54:58 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 1114, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1089 (sinal_em_codigo), evento 1087 (arvore_podada), evento 1083 (corpo_http), evento 1090 (verbete_entregue, campo_ausente), evento 1090 (verbete_entregue, contrato-produto), evento 1090 (verbete_entregue, campo_renomeado), evento 1090 (verbete_entregue, entidade-produto), evento 1094 (resposta), evento 1099 (verbete_citado, contrato-produto), evento 1100 (verbete_citado, campo_ausente); divergência: não; falha: nenhuma; prov.used: campo_ausente, contrato-produto, campo_renomeado, entidade-produto (gen_ai: chat)
- evento 1120, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 1089 (sinal_em_codigo), evento 1087 (arvore_podada), evento 1083 (corpo_http), evento 1094 (resposta), evento 1117 (resposta), evento 1119 (verbete_entregue, tipo_divergente); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: campo_ausente, campo_renomeado, contrato-produto, entidade-produto, tipo_divergente

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1076 a 1120 da trilha; hash dos eventos deste caso: `218a522a0abd1a25`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
