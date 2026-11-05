<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-6`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/tra-6@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `escala_ou_unidade_errada` · **CAMPO:** `preco` · selo de probabilidade: **baixo** (p = 0,77)

**IMPACTO (declarado):** `O usuário vê preços com a escala errada, mostrando R$ 8990,00 em vez de R$ 89,90.`

Justificativa (gerada por molde): O agente respondeu escala_ou_unidade_errada no campo preco porque o sinal preco: esperado 89.9 (referência em modo normal), recebido 8990.0 em 14 itens está presente na resposta HTTP e os verbetes entidade-produto, contagem_inconsistente, nulo_inesperado estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,10. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,77); trate como hipótese e confira o campo preco antes de agir.

**Biblioteca:** 1 edição(ões) aplicada(s) ([formato_preco]), 0 para revisão humana, 1 recusada(s) (duplicada).

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso tra-6. A proposta 1 (nota em [escala_ou_unidade_errada]) foi recusada por a validação da Fase 3 com o código duplicada: [escala_ou_unidade_errada] já tem uma nota com este texto. A proposta 2 (novo_verbete em [formato_preco], peso 3) passou pela validação da Fase 3 e pelos filtros e entrou no lote.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `escala_ou_unidade_errada` | recusada: `duplicada` | nenhum | recusada: `duplicada` |  |
| 2 | novo_verbete | `formato_preco` | aceita | nenhum | **aplicada** | 3 |

Poda de `arvore` (evento 1164): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `b68e52486de88711`):

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
      button "R$ 8990,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 8490,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "R$ 6990,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 1166): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2096}, depois {"chars": 434}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | 89.9 (referência em modo normal) | 8990.0 em 14 itens |

Trecho podado (hash `2f958e7c433d905b`):

```text
lista com 14 itens (referência em modo normal: 14); preco diferente em 14 itens; por exemplo: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 8990.0, "imagem": "picanha_alho.jpg", "destaque": true}; {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 8490.0, "imagem": "picanha_sem.jpg", "destaque": false}
```

Interceptação (evento 1159): `GET /api/produtos` status 200; corpo `61ba8740c5fc1841`, árvore `None`.

## 3. Contraste com a segunda causa

escala_ou_unidade_errada e não tipo_divergente: a escolha tem probabilidade 0,77 contra 0,10; verbete(s) na evidência: entidade-produto, contagem_inconsistente, nulo_inesperado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| escala_ou_unidade_errada | 0,77 | sim |
| tipo_divergente | 0,10 |  |
| formato_de_data_divergente | 0,07 |  |
| valor_fora_do_dominio | 0,06 |  |
| nulo_inesperado | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| contagem_inconsistente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[sinais: preço com grandeza estranha]`; verbetes citados: nenhum.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca |  | não se aplica | nenhum verbete citado na linha FONTE |
| O verbete citado estava no contexto entregue ao modelo |  | não se aplica | nenhum verbete citado na linha FONTE |
| Algum verbete do contexto trata da causa respondida | `escala_ou_unidade_errada` | confere | verbetes: `entidade-produto` |
| fonte_formato_valido | `[sinais: preço com grandeza estranha]` | não se aplica | nenhum verbete citado na linha FONTE |
| fonte_contem_termo_da_causa |  | não se aplica | sem causa ou sem verbete citado |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>34 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1152 | 1 | entrada | programa | ao_vivo | 2026-11-03T23:00:42 | caso tra-6 |
| 1153 | 2 | acao | programa | ao_vivo | 2026-11-03T23:00:42 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 174.7, "url": "produtos_api.php"} |
| 1154 | 3 | acao | programa | ao_vivo | 2026-11-03T23:00:42 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 10.0, "url": null} |
| 1155 | 4 | acao | programa | ao_vivo | 2026-11-03T23:00:42 | {"acao": "conferir", "falhou": false, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 2.1, "url": null} |
| 1156 | 5 | acao | programa | ao_vivo | 2026-11-03T23:00:42 | {"acao": "conferir", "falhou": false, "passo": 4, "seletor": "#produtos-api-grid .thumbnail .btn-default", "tempo_ms": 4.5, "url": null} |
| 1157 | 6 | acao | programa | ao_vivo | 2026-11-03T23:00:42 | {"acao": "conferir", "falhou": false, "passo": 5, "seletor": "#produtos-api-status", "tempo_ms": 2.7, "url": null} |
| 1159 | 7 | interceptacao | programa | ao_vivo | 2026-11-03T23:00:42 | GET /api/produtos 200 |
| 1160 | 8 | verificacao | verificacao | ao_vivo | 2026-11-03T23:00:42 | conferencia_do_roteiro: confere |
| 1161 | 9 | verificacao | verificacao | ao_vivo | 2026-11-03T23:00:42 | conferencia_do_roteiro: confere |
| 1162 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T23:00:42 | conferencia_do_roteiro: confere |
| 1164 | 11 | poda | programa | ao_vivo | 2026-11-03T23:00:42 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 1166 | 12 | poda | programa | ao_vivo | 2026-11-03T23:00:42 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1167 | 13 | candidatos | programa | ao_vivo | 2026-11-03T23:00:42 | 3 de 40 verbetes entregues |
| 1169 | 14 | prompt | programa | ao_vivo | 2026-11-03T23:00:42 | {"chars": 5792, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "1ad40b1e2a5c", "sha": "1ad40b1e2a5c6fbe"} |
| 1171 | 15 | inferencia | programa | ao_vivo | 2026-11-03T23:00:42 | diagnostico: 116,0 s |
| 1172 | 16 | declaracao | modelo | ao_vivo | 2026-11-03T23:00:42 | causa_raiz: `escala_ou_unidade_errada` |
| 1173 | 17 | declaracao | modelo | ao_vivo | 2026-11-03T23:00:42 | campo: `preco` |
| 1174 | 18 | declaracao | modelo | ao_vivo | 2026-11-03T23:00:42 | impacto: `O usuário vê preços com a escala errada, mostrando R$ 8990,00 em vez de R$ 89,90.` |
| 1175 | 19 | declaracao | modelo | ao_vivo | 2026-11-03T23:00:42 | fonte: `[sinais: preço com grandeza estranha]` |
| 1176 | 20 | verificacao | verificacao | ao_vivo | 2026-11-03T23:00:42 | quatro_linhas_presentes: confere |
| 1177 | 21 | verificacao | verificacao | ao_vivo | 2026-11-03T23:00:42 | rotulo_no_conjunto: confere |
| 1178 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T23:00:42 | fonte_existe_na_biblioteca: nao_se_aplica |
| 1179 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T23:00:42 | fonte_estava_no_contexto: nao_se_aplica |
| 1180 | 24 | verificacao | verificacao | ao_vivo | 2026-11-03T23:00:42 | campo_existe_no_caso: confere |
| 1181 | 25 | verificacao | verificacao | ao_vivo | 2026-11-03T23:00:42 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1182 | 26 | verificacao | verificacao | ao_vivo | 2026-11-03T23:00:42 | notas_nos_verbetes_citados: nao_se_aplica |
| 1183 | 27 | verificacao | verificacao | ao_vivo | 2026-11-03T23:00:42 | impacto: nao_verificavel |
| 1184 | 28 | verificacao | verificacao | ao_vivo | 2026-11-03T23:00:42 | fonte_formato_valido: nao_se_aplica |
| 1185 | 29 | verificacao | verificacao | ao_vivo | 2026-11-03T23:00:42 | fonte_contem_termo_da_causa: nao_se_aplica |
| 1186 | 30 | decisao | programa | ao_vivo | 2026-11-03T23:00:42 | diagnostico: escolha escala_ou_unidade_errada; divergência não |
| 1189 | 31 | inferencia | programa | ao_vivo | 2026-11-03T23:02:42 | proposta: 169,8 s |
| 1190 | 32 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T23:02:42 | proposta 1: nota em [escala_ou_unidade_errada]: recusada: duplicada |
| 1191 | 33 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T23:02:42 | proposta 2: novo_verbete em [formato_preco]: aplicada |
| 1192 | 34 | decisao | programa | ao_vivo | 2026-11-03T23:02:42 | edicao_biblioteca: escolha proposta_2; divergência sim |

</details>

Nós de decisão:

- evento 1186, `diagnostico`: escolha `escala_ou_unidade_errada`; resultado rotulo_emitido; evidência: evento 1166 (sinal_em_codigo), evento 1164 (arvore_podada), evento 1159 (corpo_http), evento 1167 (verbete_entregue, entidade-produto), evento 1167 (verbete_entregue, contagem_inconsistente), evento 1167 (verbete_entregue, nulo_inesperado), evento 1171 (resposta); divergência: não; falha: nenhuma; prov.used: entidade-produto, contagem_inconsistente, nulo_inesperado (gen_ai: chat)
- evento 1192, `edicao_biblioteca`: escolha `proposta_2`; resultado lote; evidência: evento 1166 (sinal_em_codigo), evento 1164 (arvore_podada), evento 1159 (corpo_http), evento 1171 (resposta), evento 1189 (resposta), evento 1190 (verbete_entregue, escala_ou_unidade_errada); divergência: sim; falha: nenhuma; prov.used: contagem_inconsistente, entidade-produto, escala_ou_unidade_errada, nulo_inesperado

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1152 a 1192 da trilha; hash dos eventos deste caso: `1ca369b3471765da`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
