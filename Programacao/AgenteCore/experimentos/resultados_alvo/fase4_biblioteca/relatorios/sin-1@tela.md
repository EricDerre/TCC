<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-1`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/sin-1@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `preco` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário não vê os preços dos produtos na tela, resultando em botões sem informações relevantes.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo preco porque o sinal preco: esperado numero, recebido None está presente na resposta HTTP e os verbetes campo_ausente, contrato-produto, campo_renomeado estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 1 edição(ões) aplicada(s) ([campo_preco_ausente]), 0 para revisão humana, 1 recusada(s) (texto_nao_atomico).

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso sin-1. A proposta 1 (nota em [campo_ausente]) foi recusada por o filtro atomicidade com o código texto_nao_atomico: o TEXTO enumera itens; uma alegação por proposta. A proposta 2 (novo_verbete em [campo_preco_ausente], peso 3) passou pela validação da Fase 3 e pelos filtros e entrou no lote.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `campo_ausente` | aceita | atomicidade | recusada: `texto_nao_atomico` | 1 |
| 2 | novo_verbete | `campo_preco_ausente` | aceita | nenhum | **aplicada** | 3 |

Poda de `arvore` (evento 134): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `714120f74ce44bb6`):

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
      button "undefined" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "undefined" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "undefined" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 136): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 1888}, depois {"chars": 22}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | numero |  |

Trecho podado (hash `eba906ccfeea5e6e`):

```text
{"preco": "(ausente)"}
```

Interceptação (evento 130): `GET /api/produtos` status 200; corpo `560029372ed43f7a`, árvore `None`.

## 3. Contraste com a segunda causa

campo_ausente e não corpo_nao_e_json: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: campo_ausente, contrato-produto, campo_renomeado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 1,00 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| tipo_divergente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente] [contrato-produto]`; verbetes citados: `campo_ausente`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `campo_ausente`, `contrato-produto`, `campo_renomeado` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `campo_ausente`, `contrato-produto`, `campo_renomeado` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `campo_ausente`, `contrato-produto`, `campo_renomeado` |
| fonte_formato_valido | `[campo_ausente] [contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["campo_ausente", "contrato-produto"]} |
| fonte_contem_termo_da_causa | `campo_ausente` | confere | {"termo": "campo_ausente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>37 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 124 | 1 | entrada | programa | ao_vivo | 2026-11-03T21:14:24 | caso sin-1 |
| 125 | 2 | acao | programa | ao_vivo | 2026-11-03T21:14:24 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 86.1, "url": "produtos_api.php"} |
| 126 | 3 | acao | programa | ao_vivo | 2026-11-03T21:14:24 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 8.4, "url": null} |
| 127 | 4 | acao | programa | ao_vivo | 2026-11-03T21:14:24 | {"acao": "conferir", "falhou": false, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 2.2, "url": null} |
| 128 | 5 | acao | programa | ao_vivo | 2026-11-03T21:14:24 | {"acao": "conferir", "falhou": true, "passo": 4, "seletor": "#produtos-api-grid .thumbnail .btn-default", "tempo_ms": 4.8, "url": null} |
| 130 | 6 | interceptacao | programa | ao_vivo | 2026-11-03T21:14:24 | GET /api/produtos 200 |
| 131 | 7 | verificacao | verificacao | ao_vivo | 2026-11-03T21:14:24 | conferencia_do_roteiro: confere |
| 132 | 8 | verificacao | verificacao | ao_vivo | 2026-11-03T21:14:24 | conferencia_do_roteiro: nao_confere |
| 134 | 9 | poda | programa | ao_vivo | 2026-11-03T21:14:24 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 136 | 10 | poda | programa | ao_vivo | 2026-11-03T21:14:24 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 137 | 11 | candidatos | programa | ao_vivo | 2026-11-03T21:14:24 | 3 de 40 verbetes entregues |
| 139 | 12 | prompt | programa | ao_vivo | 2026-11-03T21:14:24 | {"chars": 5664, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "8e4adbcad635", "sha": "8e4adbcad635912b"} |
| 141 | 13 | inferencia | programa | ao_vivo | 2026-11-03T21:14:24 | diagnostico: 105,7 s |
| 142 | 14 | declaracao | modelo | ao_vivo | 2026-11-03T21:14:24 | causa_raiz: `campo_ausente` |
| 143 | 15 | declaracao | modelo | ao_vivo | 2026-11-03T21:14:24 | campo: `preco` |
| 144 | 16 | declaracao | modelo | ao_vivo | 2026-11-03T21:14:24 | impacto: `O usuário não vê os preços dos produtos na tela, resultando em botões sem informações relevantes.` |
| 145 | 17 | declaracao | modelo | ao_vivo | 2026-11-03T21:14:24 | fonte: `[campo_ausente] [contrato-produto]` |
| 146 | 18 | declaracao | modelo | ao_vivo | 2026-11-03T21:14:24 | fonte_citada: `campo_ausente` |
| 147 | 19 | declaracao | modelo | ao_vivo | 2026-11-03T21:14:24 | fonte_citada: `contrato-produto` |
| 148 | 20 | verificacao | verificacao | ao_vivo | 2026-11-03T21:14:24 | quatro_linhas_presentes: confere |
| 149 | 21 | verificacao | verificacao | ao_vivo | 2026-11-03T21:14:24 | rotulo_no_conjunto: confere |
| 150 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T21:14:24 | fonte_existe_na_biblioteca: confere |
| 151 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T21:14:24 | fonte_existe_na_biblioteca: confere |
| 152 | 24 | verificacao | verificacao | ao_vivo | 2026-11-03T21:14:24 | fonte_estava_no_contexto: confere |
| 153 | 25 | verificacao | verificacao | ao_vivo | 2026-11-03T21:14:24 | fonte_estava_no_contexto: confere |
| 154 | 26 | verificacao | verificacao | ao_vivo | 2026-11-03T21:14:24 | campo_existe_no_caso: confere |
| 155 | 27 | verificacao | verificacao | ao_vivo | 2026-11-03T21:14:24 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 156 | 28 | verificacao | verificacao | ao_vivo | 2026-11-03T21:14:24 | notas_nos_verbetes_citados: informativo |
| 157 | 29 | verificacao | verificacao | ao_vivo | 2026-11-03T21:14:24 | impacto: nao_verificavel |
| 158 | 30 | verificacao | verificacao | ao_vivo | 2026-11-03T21:14:24 | fonte_formato_valido: confere |
| 159 | 31 | verificacao | verificacao | ao_vivo | 2026-11-03T21:14:24 | fonte_contem_termo_da_causa: confere |
| 160 | 32 | verificacao | verificacao | ao_vivo | 2026-11-03T21:14:24 | fonte_contem_termo_da_causa: nao_confere |
| 161 | 33 | decisao | programa | ao_vivo | 2026-11-03T21:14:24 | diagnostico: escolha campo_ausente; divergência não |
| 164 | 34 | inferencia | programa | ao_vivo | 2026-11-03T21:16:14 | proposta: 146,0 s |
| 166 | 35 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:16:14 | proposta 1: nota em [campo_ausente]: recusada: texto_nao_atomico |
| 168 | 36 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:16:14 | proposta 2: novo_verbete em [campo_preco_ausente]: aplicada |
| 169 | 37 | decisao | programa | ao_vivo | 2026-11-03T21:16:14 | edicao_biblioteca: escolha proposta_2; divergência sim |

</details>

Nós de decisão:

- evento 161, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 136 (sinal_em_codigo), evento 134 (arvore_podada), evento 130 (corpo_http), evento 137 (verbete_entregue, campo_ausente), evento 137 (verbete_entregue, contrato-produto), evento 137 (verbete_entregue, campo_renomeado), evento 141 (resposta), evento 146 (verbete_citado, campo_ausente), evento 147 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: campo_ausente, contrato-produto, campo_renomeado (gen_ai: chat)
- evento 169, `edicao_biblioteca`: escolha `proposta_2`; resultado lote; evidência: evento 136 (sinal_em_codigo), evento 134 (arvore_podada), evento 130 (corpo_http), evento 141 (resposta), evento 164 (resposta), evento 166 (verbete_entregue, campo_ausente); divergência: sim; falha: nenhuma; prov.used: campo_ausente, campo_renomeado, contrato-produto

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 124 a 169 da trilha; hash dos eventos deste caso: `77e54044d05281ad`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
