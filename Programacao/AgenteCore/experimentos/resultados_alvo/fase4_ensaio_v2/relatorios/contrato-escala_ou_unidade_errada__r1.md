<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `contrato-escala_ou_unidade_errada#1`: o que o agente fez, declarou e conferiu

Trilha `fase4_ensaio_v2/qwen2.5_7b/contrato-escala_ou_unidade_errada#1`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `escala_ou_unidade_errada` · **CAMPO:** `preco` · selo de probabilidade: **baixo** (p = 0,69)

**IMPACTO (declarado):** `O usuário vê preços com uma escala errada, mostrando R$ 8990,00 em vez de R$ 89,90.`

Justificativa (gerada por molde): O agente respondeu escala_ou_unidade_errada no campo preco porque o sinal preco: esperado 89.9 (referência em modo normal), recebido 8990.0 em 14 itens está presente na resposta HTTP e os verbetes entidade-produto, contagem_inconsistente, nulo_inesperado estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,15. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,69); trate como hipótese e confira o campo preco antes de agir.

## 2. Evidência

Poda de `arvore` (evento 173): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 175): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2096}, depois {"chars": 434}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | 89.9 (referência em modo normal) | 8990.0 em 14 itens |

Trecho podado (hash `2f958e7c433d905b`):

```text
lista com 14 itens (referência em modo normal: 14); preco diferente em 14 itens; por exemplo: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 8990.0, "imagem": "picanha_alho.jpg", "destaque": true}; {"id": 2, "nome": "Picanha Simples", "resumo": "Corte nobre grelhado no ponto", "tipo": "Carnes", "preco": 8490.0, "imagem": "picanha_sem.jpg", "destaque": false}
```

Interceptação (evento 168): `GET /api/produtos` status 200; corpo `61ba8740c5fc1841`, árvore `None`.

## 3. Contraste com a segunda causa

escala_ou_unidade_errada e não valor_fora_do_dominio: a escolha tem probabilidade 0,69 contra 0,15; verbete(s) na evidência: entidade-produto, contagem_inconsistente, nulo_inesperado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| escala_ou_unidade_errada | 0,69 | sim |
| valor_fora_do_dominio | 0,15 |  |
| formato_de_data_divergente | 0,08 |  |
| tipo_divergente | 0,07 |  |
| nulo_inesperado | 0,01 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |

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

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v2_reexec --repeticoes 1`

## 6. Árvore completa

<details><summary>30 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 161 | 1 | entrada | programa | ao_vivo | 2026-11-04T21:39:31 | caso contrato-escala_ou_unidade_errada#1 |
| 162 | 2 | acao | programa | ao_vivo | 2026-11-04T21:39:31 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 114.6, "falhou": false} |
| 163 | 3 | acao | programa | ao_vivo | 2026-11-04T21:39:31 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 12.5, "falhou": false} |
| 164 | 4 | acao | programa | ao_vivo | 2026-11-04T21:39:31 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.8, "falhou": false} |
| 165 | 5 | acao | programa | ao_vivo | 2026-11-04T21:39:31 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 14.0, "falhou": false} |
| 166 | 6 | acao | programa | ao_vivo | 2026-11-04T21:39:31 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 5.9, "falhou": false} |
| 168 | 7 | interceptacao | programa | ao_vivo | 2026-11-04T21:39:31 | GET /api/produtos 200 |
| 169 | 8 | verificacao | verificacao | ao_vivo | 2026-11-04T21:39:31 | conferencia_do_roteiro: confere |
| 170 | 9 | verificacao | verificacao | ao_vivo | 2026-11-04T21:39:31 | conferencia_do_roteiro: confere |
| 171 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T21:39:31 | conferencia_do_roteiro: confere |
| 173 | 11 | poda | programa | ao_vivo | 2026-11-04T21:39:31 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 175 | 12 | poda | programa | ao_vivo | 2026-11-04T21:39:31 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 176 | 13 | candidatos | programa | ao_vivo | 2026-11-04T21:39:31 | 3 de 39 verbetes entregues |
| 178 | 14 | prompt | programa | ao_vivo | 2026-11-04T21:39:31 | {"etapa": "diagnostico", "sha": "75bee05e41f69750", "prompt_sha256": "75bee05e41f6", "chars": 5925, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 180 | 15 | inferencia | programa | ao_vivo | 2026-11-04T21:39:31 | diagnostico: 133,4 s |
| 181 | 16 | declaracao | modelo | ao_vivo | 2026-11-04T21:39:31 | causa_raiz: `escala_ou_unidade_errada` |
| 182 | 17 | declaracao | modelo | ao_vivo | 2026-11-04T21:39:31 | campo: `preco` |
| 183 | 18 | declaracao | modelo | ao_vivo | 2026-11-04T21:39:31 | impacto: `O usuário vê preços com uma escala errada, mostrando R$ 8990,00 em vez de R$ 89,90.` |
| 184 | 19 | declaracao | modelo | ao_vivo | 2026-11-04T21:39:31 | fonte: `[sinais: preço com grandeza estranha]` |
| 185 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T21:39:31 | quatro_linhas_presentes: confere |
| 186 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T21:39:31 | rotulo_no_conjunto: confere |
| 187 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T21:39:31 | fonte_existe_na_biblioteca: nao_se_aplica |
| 188 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T21:39:31 | fonte_estava_no_contexto: nao_se_aplica |
| 189 | 24 | verificacao | verificacao | ao_vivo | 2026-11-04T21:39:31 | campo_existe_no_caso: confere |
| 190 | 25 | verificacao | verificacao | ao_vivo | 2026-11-04T21:39:31 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 191 | 26 | verificacao | verificacao | ao_vivo | 2026-11-04T21:39:31 | notas_nos_verbetes_citados: nao_se_aplica |
| 192 | 27 | verificacao | verificacao | ao_vivo | 2026-11-04T21:39:31 | impacto: nao_verificavel |
| 193 | 28 | verificacao | verificacao | ao_vivo | 2026-11-04T21:39:31 | fonte_formato_valido: nao_se_aplica |
| 194 | 29 | verificacao | verificacao | ao_vivo | 2026-11-04T21:39:31 | fonte_contem_termo_da_causa: nao_se_aplica |
| 195 | 30 | decisao | programa | ao_vivo | 2026-11-04T21:39:31 | diagnostico: escolha escala_ou_unidade_errada; divergência não |

</details>

Nós de decisão:

- evento 195, `diagnostico`: escolha `escala_ou_unidade_errada`; resultado rotulo_emitido; evidência: evento 175 (sinal_em_codigo), evento 173 (arvore_podada), evento 168 (corpo_http), evento 176 (verbete_entregue, entidade-produto), evento 176 (verbete_entregue, contagem_inconsistente), evento 176 (verbete_entregue, nulo_inesperado), evento 180 (resposta); divergência: não; falha: nenhuma; prov.used: entidade-produto, contagem_inconsistente, nulo_inesperado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 161 a 195 da trilha; hash dos eventos deste caso: `878ff48d38739ff3`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
