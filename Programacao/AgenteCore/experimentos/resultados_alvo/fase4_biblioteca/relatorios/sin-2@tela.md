<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-2`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/sin-2@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_renomeado` · **CAMPO:** `preco` · selo de probabilidade: **medio** (p = 0,97) · **CONFLITO**: a FONTE cita o verbete campo_renomeado, fora do contexto entregue

**IMPACTO (declarado):** `O usuário não vê os preços corretos nos cartões de produtos, e botões sem funcionalidade aparecem na página.`

Justificativa (gerada por molde): O agente respondeu campo_renomeado no campo preco porque o sinal preco: esperado preco, recebido preco_v2 está presente na resposta HTTP e os verbetes campo_ausente, contagem_inconsistente, nulo_inesperado estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,19. A FONTE cita 1 verbete(s), 1 fora do contexto entregue (campo_renomeado). O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a FONTE cita o verbete campo_renomeado, fora do contexto entregue. Este nó está marcado com a falha citacao_fora_do_contexto (origem: modelo).

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 2 recusada(s) (mensagem_nao_encontrada_no_codigo, mensagem_nao_encontrada_no_codigo) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso sin-2. A proposta 1 (nota em [campo_renomeado]) foi recusada por o filtro fonte_confiavel com o código mensagem_nao_encontrada_no_codigo: a mensagem "Corrigir a afirmação para: 'Contrato mudou no servidor sem a" não está no código das cobaias nem no openapi.json. A proposta 2 (novo_verbete em [campo_incorreto]) foi recusada por o filtro fonte_confiavel com o código mensagem_nao_encontrada_no_codigo: a mensagem "Um campo pode ser renomeado ou ausente no contrato, mas deve" não está no código das cobaias nem no openapi.json.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `campo_renomeado` | aceita | fonte_confiavel | recusada: `mensagem_nao_encontrada_no_codigo` | 1 |
| 2 | novo_verbete | `campo_incorreto` | aceita | fonte_confiavel | recusada: `mensagem_nao_encontrada_no_codigo` | 3 |

Poda de `arvore` (evento 180): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 182): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2110}, depois {"chars": 18}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | preco | preco_v2 |

Trecho podado (hash `3ca91df248763374`):

```text
{"preco_v2": 89.9}
```

Interceptação (evento 177): `GET /api/produtos` status 200; corpo `4f7726df03992678`, árvore `None`.

## 3. Contraste com a segunda causa

campo_renomeado e não campo_ausente: a escolha tem probabilidade 0,97 contra 0,19; verbete(s) na evidência: campo_ausente, contagem_inconsistente, nulo_inesperado, campo_renomeado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_renomeado | 0,97 | sim |
| campo_ausente | 0,19 |  |
| corpo_nao_e_json | 0,01 |  |
| corpo_vazio | 0,01 |  |
| tipo_divergente | 0,01 |  |
| nulo_inesperado | 0,01 |  |
| contagem_inconsistente | 0,01 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_renomeado] [preço ausente]`; verbetes citados: `campo_renomeado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | **não confere** | contexto: `campo_ausente`, `contagem_inconsistente`, `nulo_inesperado` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `campo_ausente` |
| fonte_formato_valido | `[campo_renomeado] [preço ausente]` | **não confere** | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["campo_renomeado"]} |
| fonte_contem_termo_da_causa | `campo_renomeado` | confere | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>33 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 171 | 1 | entrada | programa | ao_vivo | 2026-11-03T21:18:45 | caso sin-2 |
| 172 | 2 | acao | programa | ao_vivo | 2026-11-03T21:18:46 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 171.2, "url": "produtos_api.php"} |
| 173 | 3 | acao | programa | ao_vivo | 2026-11-03T21:18:46 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 7.5, "url": null} |
| 174 | 4 | acao | programa | ao_vivo | 2026-11-03T21:18:46 | {"acao": "conferir", "falhou": false, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 10.0, "url": null} |
| 175 | 5 | acao | programa | ao_vivo | 2026-11-03T21:18:46 | {"acao": "conferir", "falhou": true, "passo": 4, "seletor": "#produtos-api-grid .thumbnail .btn-default", "tempo_ms": 4.0, "url": null} |
| 177 | 6 | interceptacao | programa | ao_vivo | 2026-11-03T21:18:46 | GET /api/produtos 200 |
| 178 | 7 | verificacao | verificacao | ao_vivo | 2026-11-03T21:18:46 | conferencia_do_roteiro: confere |
| 179 | 8 | verificacao | verificacao | ao_vivo | 2026-11-03T21:18:46 | conferencia_do_roteiro: nao_confere |
| 180 | 9 | poda | programa | ao_vivo | 2026-11-03T21:18:46 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 182 | 10 | poda | programa | ao_vivo | 2026-11-03T21:18:46 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 183 | 11 | candidatos | programa | ao_vivo | 2026-11-03T21:18:46 | 3 de 40 verbetes entregues |
| 185 | 12 | prompt | programa | ao_vivo | 2026-11-03T21:18:46 | {"chars": 5322, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "bf32d8385519", "sha": "bf32d8385519c879"} |
| 187 | 13 | inferencia | programa | ao_vivo | 2026-11-03T21:18:46 | diagnostico: 95,7 s |
| 188 | 14 | declaracao | modelo | ao_vivo | 2026-11-03T21:18:46 | causa_raiz: `campo_renomeado` |
| 189 | 15 | declaracao | modelo | ao_vivo | 2026-11-03T21:18:46 | campo: `preco` |
| 190 | 16 | declaracao | modelo | ao_vivo | 2026-11-03T21:18:46 | impacto: `O usuário não vê os preços corretos nos cartões de produtos, e botões sem funcionalidade aparecem na página.` |
| 191 | 17 | declaracao | modelo | ao_vivo | 2026-11-03T21:18:46 | fonte: `[campo_renomeado] [preço ausente]` |
| 192 | 18 | declaracao | modelo | ao_vivo | 2026-11-03T21:18:46 | fonte_citada: `campo_renomeado` |
| 193 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T21:18:46 | quatro_linhas_presentes: confere |
| 194 | 20 | verificacao | verificacao | ao_vivo | 2026-11-03T21:18:46 | rotulo_no_conjunto: confere |
| 195 | 21 | verificacao | verificacao | ao_vivo | 2026-11-03T21:18:46 | fonte_existe_na_biblioteca: confere |
| 196 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T21:18:46 | fonte_estava_no_contexto: nao_confere |
| 197 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T21:18:46 | campo_existe_no_caso: confere |
| 198 | 24 | verificacao | verificacao | ao_vivo | 2026-11-03T21:18:46 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 199 | 25 | verificacao | verificacao | ao_vivo | 2026-11-03T21:18:46 | notas_nos_verbetes_citados: informativo |
| 200 | 26 | verificacao | verificacao | ao_vivo | 2026-11-03T21:18:46 | impacto: nao_verificavel |
| 201 | 27 | verificacao | verificacao | ao_vivo | 2026-11-03T21:18:46 | fonte_formato_valido: nao_confere |
| 202 | 28 | verificacao | verificacao | ao_vivo | 2026-11-03T21:18:46 | fonte_contem_termo_da_causa: confere |
| 203 | 29 | decisao | programa | ao_vivo | 2026-11-03T21:18:46 | diagnostico: escolha campo_renomeado; divergência sim |
| 206 | 30 | inferencia | programa | ao_vivo | 2026-11-03T21:20:25 | proposta: 166,8 s |
| 208 | 31 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:20:25 | proposta 1: nota em [campo_renomeado]: recusada: mensagem_nao_encontrada_no_codigo |
| 210 | 32 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T21:20:25 | proposta 2: novo_verbete em [campo_incorreto]: recusada: mensagem_nao_encontrada_no_codigo |
| 211 | 33 | decisao | programa | ao_vivo | 2026-11-03T21:20:25 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 203, `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido; evidência: evento 182 (sinal_em_codigo), evento 180 (arvore_podada), evento 177 (corpo_http), evento 183 (verbete_entregue, campo_ausente), evento 183 (verbete_entregue, contagem_inconsistente), evento 183 (verbete_entregue, nulo_inesperado), evento 187 (resposta), evento 192 (verbete_citado, campo_renomeado); divergência: sim; falha: citacao_fora_do_contexto; prov.used: campo_ausente, contagem_inconsistente, nulo_inesperado, campo_renomeado (gen_ai: chat)
- evento 211, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 182 (sinal_em_codigo), evento 180 (arvore_podada), evento 177 (corpo_http), evento 187 (resposta), evento 206 (resposta), evento 208 (verbete_entregue, campo_renomeado); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: campo_ausente, campo_renomeado, contagem_inconsistente, nulo_inesperado

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 171 a 211 da trilha; hash dos eventos deste caso: `5c49a652ea2a6187`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
