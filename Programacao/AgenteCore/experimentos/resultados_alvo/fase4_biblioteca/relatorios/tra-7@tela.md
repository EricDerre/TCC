<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-7`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/tra-7@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_renomeado` · **CAMPO:** `nome, resumo, preco, imagem, destaque, tipo` · selo de probabilidade: **medio** (p = 0,98) · **CONFLITO**: o campo apontado (nome, resumo, preco, imagem, destaque, tipo) não aparece no caso

**IMPACTO (declarado):** `O usuário vê nomes, resumos, preços, imagens e tipos incorretos nos cartões de produtos.`

Justificativa (gerada por molde): O agente respondeu campo_renomeado no campo nome, resumo, preco, imagem, destaque, tipo porque o sinal nome: esperado "Picanha Simples" (referência em modo normal), recebido "Picanha ao Alho" em 13 itens está presente na resposta HTTP e os verbetes entidade-produto, contagem_inconsistente, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,01. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): o campo apontado (nome, resumo, preco, imagem, destaque, tipo) não aparece no caso. Este nó está marcado com a falha campo_errado (origem: modelo).

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 2 recusada(s) (duplicada, id_repetido) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso tra-7. A proposta 1 (nota em [entidade-produto]) foi recusada por a validação da Fase 3 com o código duplicada: [entidade-produto] já tem uma nota com este texto. A proposta 2 (novo_verbete em [chave_de_juncao_errada]) foi recusada por a validação da Fase 3 com o código id_repetido: 'chave_de_juncao_errada' já é id de verbete ou nome de causa raiz.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `entidade-produto` | recusada: `duplicada` | nenhum | recusada: `duplicada` |  |
| 2 | novo_verbete | `chave_de_juncao_errada` | recusada: `id_repetido` | nenhum | recusada: `id_repetido` |  |

Poda de `arvore` (evento 1206): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 1 linha(s) da referência | 1 linha(s) novas |

Trecho podado (hash `3f3965b2336faec3`):

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
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "R$ 69,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="4"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 1208): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2068}, depois {"chars": 576}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| nome | "Picanha Simples" (referência em modo normal) | "Picanha ao Alho" em 13 itens |
| resumo | "Corte nobre grelhado no ponto" (referência em modo normal) | "Picanha grelhada com alho laminado na brasa" em 12 itens |
| preco | 84.9 (referência em modo normal) | 89.9 em 12 itens |
| imagem | "picanha_sem.jpg" (referência em modo normal) | "picanha_alho.jpg" em 12 itens |
| destaque | false (referência em modo normal) | true em 9 itens |
| tipo | "Bebidas" (referência em modo normal) | "Carnes" em 2 itens |

Trecho podado (hash `999b33c3291bb399`):

```text
lista com 14 itens (referência em modo normal: 14); nome diferente em 13 itens; resumo diferente em 12 itens; preco diferente em 12 itens; imagem diferente em 12 itens; destaque diferente em 9 itens; tipo diferente em 2 itens; por exemplo: {"id": 2, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}; {"id": 3, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 84.9, "imagem": "picanha_sem.jpg", "destaque": false}
```

Interceptação (evento 1201): `GET /api/produtos` status 200; corpo `ca41b82db0fe97b6`, árvore `None`.

## 3. Contraste com a segunda causa

campo_renomeado e não estrutura_aninhada_divergente: a escolha tem probabilidade 0,98 contra 0,01; verbete(s) na evidência: entidade-produto, contagem_inconsistente, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_renomeado | 0,98 | sim |
| estrutura_aninhada_divergente | 0,01 |  |
| campo_ausente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| dado_desatualizado | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [estrutura_aninhada_divergente]`; verbetes citados: `entidade-produto`, `estrutura_aninhada_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `estrutura_aninhada_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contagem_inconsistente`, `estrutura_aninhada_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `estrutura_aninhada_divergente` | confere | contexto: `entidade-produto`, `contagem_inconsistente`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `estrutura_aninhada_divergente` |
| fonte_formato_valido | `[entidade-produto], [estrutura_aninhada_divergente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["entidade-produto", "estrutura_aninhada_divergente"]} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "campo_renomeado"} |
| fonte_contem_termo_da_causa | `estrutura_aninhada_divergente` | **não confere** | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome, resumo, preco, imagem, destaque, tipo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>39 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1194 | 1 | entrada | programa | ao_vivo | 2026-11-03T23:05:37 | caso tra-7 |
| 1195 | 2 | acao | programa | ao_vivo | 2026-11-03T23:05:37 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 115.5, "url": "produtos_api.php"} |
| 1196 | 3 | acao | programa | ao_vivo | 2026-11-03T23:05:37 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 8.5, "url": null} |
| 1197 | 4 | acao | programa | ao_vivo | 2026-11-03T23:05:37 | {"acao": "conferir", "falhou": false, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 2.9, "url": null} |
| 1198 | 5 | acao | programa | ao_vivo | 2026-11-03T23:05:37 | {"acao": "conferir", "falhou": false, "passo": 4, "seletor": "#produtos-api-grid .thumbnail .btn-default", "tempo_ms": 4.4, "url": null} |
| 1199 | 6 | acao | programa | ao_vivo | 2026-11-03T23:05:37 | {"acao": "conferir", "falhou": false, "passo": 5, "seletor": "#produtos-api-status", "tempo_ms": 3.3, "url": null} |
| 1201 | 7 | interceptacao | programa | ao_vivo | 2026-11-03T23:05:37 | GET /api/produtos 200 |
| 1202 | 8 | verificacao | verificacao | ao_vivo | 2026-11-03T23:05:37 | conferencia_do_roteiro: confere |
| 1203 | 9 | verificacao | verificacao | ao_vivo | 2026-11-03T23:05:37 | conferencia_do_roteiro: confere |
| 1204 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T23:05:37 | conferencia_do_roteiro: confere |
| 1206 | 11 | poda | programa | ao_vivo | 2026-11-03T23:05:37 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 1208 | 12 | poda | programa | ao_vivo | 2026-11-03T23:05:37 | corpo_http: 6 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1209 | 13 | candidatos | programa | ao_vivo | 2026-11-03T23:05:37 | 3 de 40 verbetes entregues |
| 1211 | 14 | prompt | programa | ao_vivo | 2026-11-03T23:05:37 | {"chars": 6646, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "975e42ced4ad", "sha": "975e42ced4ad417a"} |
| 1213 | 15 | inferencia | programa | ao_vivo | 2026-11-03T23:05:37 | diagnostico: 111,3 s |
| 1214 | 16 | declaracao | modelo | ao_vivo | 2026-11-03T23:05:37 | causa_raiz: `campo_renomeado` |
| 1215 | 17 | declaracao | modelo | ao_vivo | 2026-11-03T23:05:37 | campo: `nome, resumo, preco, imagem, destaque, tipo` |
| 1216 | 18 | declaracao | modelo | ao_vivo | 2026-11-03T23:05:37 | impacto: `O usuário vê nomes, resumos, preços, imagens e tipos incorretos nos cartões de produtos.` |
| 1217 | 19 | declaracao | modelo | ao_vivo | 2026-11-03T23:05:37 | fonte: `[entidade-produto], [estrutura_aninhada_divergente]` |
| 1218 | 20 | declaracao | modelo | ao_vivo | 2026-11-03T23:05:37 | fonte_citada: `entidade-produto` |
| 1219 | 21 | declaracao | modelo | ao_vivo | 2026-11-03T23:05:37 | fonte_citada: `estrutura_aninhada_divergente` |
| 1220 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T23:05:37 | quatro_linhas_presentes: confere |
| 1221 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T23:05:37 | rotulo_no_conjunto: confere |
| 1222 | 24 | verificacao | verificacao | ao_vivo | 2026-11-03T23:05:37 | fonte_existe_na_biblioteca: confere |
| 1223 | 25 | verificacao | verificacao | ao_vivo | 2026-11-03T23:05:37 | fonte_existe_na_biblioteca: confere |
| 1224 | 26 | verificacao | verificacao | ao_vivo | 2026-11-03T23:05:37 | fonte_estava_no_contexto: confere |
| 1225 | 27 | verificacao | verificacao | ao_vivo | 2026-11-03T23:05:37 | fonte_estava_no_contexto: confere |
| 1226 | 28 | verificacao | verificacao | ao_vivo | 2026-11-03T23:05:37 | campo_existe_no_caso: nao_confere |
| 1227 | 29 | verificacao | verificacao | ao_vivo | 2026-11-03T23:05:37 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1228 | 30 | verificacao | verificacao | ao_vivo | 2026-11-03T23:05:37 | notas_nos_verbetes_citados: informativo |
| 1229 | 31 | verificacao | verificacao | ao_vivo | 2026-11-03T23:05:37 | impacto: nao_verificavel |
| 1230 | 32 | verificacao | verificacao | ao_vivo | 2026-11-03T23:05:37 | fonte_formato_valido: confere |
| 1231 | 33 | verificacao | verificacao | ao_vivo | 2026-11-03T23:05:37 | fonte_contem_termo_da_causa: nao_confere |
| 1232 | 34 | verificacao | verificacao | ao_vivo | 2026-11-03T23:05:37 | fonte_contem_termo_da_causa: nao_confere |
| 1233 | 35 | decisao | programa | ao_vivo | 2026-11-03T23:05:37 | diagnostico: escolha campo_renomeado; divergência sim |
| 1236 | 36 | inferencia | programa | ao_vivo | 2026-11-03T23:07:32 | proposta: 186,6 s |
| 1237 | 37 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T23:07:32 | proposta 1: nota em [entidade-produto]: recusada: duplicada |
| 1238 | 38 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T23:07:32 | proposta 2: novo_verbete em [chave_de_juncao_errada]: recusada: id_repetido |
| 1239 | 39 | decisao | programa | ao_vivo | 2026-11-03T23:07:32 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 1233, `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido; evidência: evento 1208 (sinal_em_codigo), evento 1206 (arvore_podada), evento 1201 (corpo_http), evento 1209 (verbete_entregue, entidade-produto), evento 1209 (verbete_entregue, contagem_inconsistente), evento 1209 (verbete_entregue, estrutura_aninhada_divergente), evento 1213 (resposta), evento 1218 (verbete_citado, entidade-produto), evento 1219 (verbete_citado, estrutura_aninhada_divergente); divergência: sim; falha: campo_errado; prov.used: entidade-produto, contagem_inconsistente, estrutura_aninhada_divergente (gen_ai: chat)
- evento 1239, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 1208 (sinal_em_codigo), evento 1206 (arvore_podada), evento 1201 (corpo_http), evento 1213 (resposta), evento 1236 (resposta), evento 1237 (verbete_entregue, entidade-produto), evento 1238 (verbete_entregue, chave_de_juncao_errada); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: chave_de_juncao_errada, contagem_inconsistente, entidade-produto, estrutura_aninhada_divergente

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1194 a 1239 da trilha; hash dos eventos deste caso: `6c36a18bfb415631`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
