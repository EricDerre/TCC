<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-4`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/sin-4@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `id` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `A tela exibe uma lista incompleta de produtos, mostrando 2 linhas a menos e 2 a mais que a referência.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto no campo id porque o sinal esperado objeto, recebido lista está presente na resposta HTTP e os verbetes entidade-produto, colecao_no_lugar_de_objeto, contrato-produto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 142): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 197}, depois {"linhas": 41}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 2 linha(s) da referência | 1 linha(s) novas |

Trecho podado (hash `d5173f7cbffdeeca`):

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
  dialog
    text "(sem descrição)"

```

Poda de `corpo_http` (evento 144): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 163}, depois {"chars": 174}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| (corpo inteiro) | objeto | lista |

Trecho podado (hash `b78f8a85ed458c1a`):

```text
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 135): `GET /api/produtos` status 200; corpo `4b1bdd056e7a8c3b`, árvore `None`.

Interceptação (evento 137): `GET /api/produtos/1` status 200; corpo `3d81a09c6ed20335`, árvore `None`.

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não resposta_truncada: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, colecao_no_lugar_de_objeto, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 1,00 | sim |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| tipo_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[colecao_no_lugar_de_objeto]`; verbetes citados: `colecao_no_lugar_de_objeto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `colecao_no_lugar_de_objeto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `colecao_no_lugar_de_objeto` | confere | contexto: `entidade-produto`, `colecao_no_lugar_de_objeto`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `colecao_no_lugar_de_objeto`, `contrato-produto` |
| fonte_formato_valido | `[colecao_no_lugar_de_objeto]` | confere | {"ids": ["colecao_no_lugar_de_objeto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `colecao_no_lugar_de_objeto` | confere | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids sin-4 --k 3`

## 6. Árvore completa

<details><summary>34 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 127 | 1 | entrada | programa | ao_vivo | 2026-11-05T18:44:41 | caso sin-4 |
| 128 | 2 | acao | programa | ao_vivo | 2026-11-05T18:44:41 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 83.0, "falhou": false} |
| 129 | 3 | acao | programa | ao_vivo | 2026-11-05T18:44:41 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 10.2, "falhou": false} |
| 130 | 4 | acao | programa | ao_vivo | 2026-11-05T18:44:41 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.0, "falhou": false} |
| 131 | 5 | acao | programa | ao_vivo | 2026-11-05T18:44:41 | {"passo": 4, "acao": "clicar", "seletor": "#produtos-api-grid .saiba-mais[data-id='1']", "url": null, "tempo_ms": 62.6, "falhou": false} |
| 132 | 6 | acao | programa | ao_vivo | 2026-11-05T18:44:41 | {"passo": 5, "acao": "esperar", "seletor": "#modalDetalhe", "url": null, "tempo_ms": 218.3, "falhou": false} |
| 133 | 7 | acao | programa | ao_vivo | 2026-11-05T18:44:41 | {"passo": 6, "acao": "conferir", "seletor": "#modalDetalheTitulo", "url": null, "tempo_ms": 4.2, "falhou": false} |
| 134 | 8 | acao | programa | ao_vivo | 2026-11-05T18:44:41 | {"passo": 7, "acao": "conferir", "seletor": "#modalDetalheCorpo", "url": null, "tempo_ms": 3.4, "falhou": false} |
| 135 | 9 | interceptacao | programa | ao_vivo | 2026-11-05T18:44:41 | GET /api/produtos 200 |
| 137 | 10 | interceptacao | programa | ao_vivo | 2026-11-05T18:44:41 | GET /api/produtos/1 200 |
| 138 | 11 | verificacao | verificacao | ao_vivo | 2026-11-05T18:44:41 | conferencia_do_roteiro: confere |
| 139 | 12 | verificacao | verificacao | ao_vivo | 2026-11-05T18:44:41 | conferencia_do_roteiro: confere |
| 140 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T18:44:41 | conferencia_do_roteiro: confere |
| 142 | 14 | poda | programa | ao_vivo | 2026-11-05T18:44:41 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 144 | 15 | poda | programa | ao_vivo | 2026-11-05T18:44:41 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 145 | 16 | candidatos | programa | ao_vivo | 2026-11-05T18:44:41 | 3 de 39 verbetes entregues |
| 147 | 17 | prompt | programa | ao_vivo | 2026-11-05T18:44:41 | {"etapa": "diagnostico", "sha": "c26a6a730e090aa8", "prompt_sha256": "c26a6a730e09", "chars": 3953, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 149 | 18 | inferencia | programa | ao_vivo | 2026-11-05T18:44:41 | diagnostico: 71,5 s |
| 150 | 19 | declaracao | modelo | ao_vivo | 2026-11-05T18:44:41 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 151 | 20 | declaracao | modelo | ao_vivo | 2026-11-05T18:44:41 | campo: `id` |
| 152 | 21 | declaracao | modelo | ao_vivo | 2026-11-05T18:44:41 | impacto: `A tela exibe uma lista incompleta de produtos, mostrando 2 linhas a menos e 2 a mais que a referência.` |
| 153 | 22 | declaracao | modelo | ao_vivo | 2026-11-05T18:44:41 | fonte: `[colecao_no_lugar_de_objeto]` |
| 154 | 23 | declaracao | modelo | ao_vivo | 2026-11-05T18:44:41 | fonte_citada: `colecao_no_lugar_de_objeto` |
| 155 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T18:44:41 | quatro_linhas_presentes: confere |
| 156 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T18:44:41 | rotulo_no_conjunto: confere |
| 157 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T18:44:41 | fonte_existe_na_biblioteca: confere |
| 158 | 27 | verificacao | verificacao | ao_vivo | 2026-11-05T18:44:41 | fonte_estava_no_contexto: confere |
| 159 | 28 | verificacao | verificacao | ao_vivo | 2026-11-05T18:44:41 | campo_existe_no_caso: confere |
| 160 | 29 | verificacao | verificacao | ao_vivo | 2026-11-05T18:44:41 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 161 | 30 | verificacao | verificacao | ao_vivo | 2026-11-05T18:44:41 | notas_nos_verbetes_citados: informativo |
| 162 | 31 | verificacao | verificacao | ao_vivo | 2026-11-05T18:44:41 | impacto: nao_verificavel |
| 163 | 32 | verificacao | verificacao | ao_vivo | 2026-11-05T18:44:41 | fonte_formato_valido: confere |
| 164 | 33 | verificacao | verificacao | ao_vivo | 2026-11-05T18:44:41 | fonte_contem_termo_da_causa: confere |
| 165 | 34 | decisao | programa | ao_vivo | 2026-11-05T18:44:41 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 165, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 144 (sinal_em_codigo), evento 142 (arvore_podada), evento 137 (corpo_http), evento 145 (verbete_entregue, entidade-produto), evento 145 (verbete_entregue, colecao_no_lugar_de_objeto), evento 145 (verbete_entregue, contrato-produto), evento 149 (resposta), evento 154 (verbete_citado, colecao_no_lugar_de_objeto); divergência: não; falha: nenhuma; prov.used: entidade-produto, colecao_no_lugar_de_objeto, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 127 a 165 da trilha; hash dos eventos deste caso: `3ec515128d485828`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
