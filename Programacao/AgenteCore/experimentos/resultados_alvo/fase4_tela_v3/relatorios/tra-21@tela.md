<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-21`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/tra-21@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `contagem_inconsistente` · **CAMPO:** `id` · selo de probabilidade: **baixo** (p = 0,57)

**IMPACTO (declarado):** `O usuário vê uma lista com 10 itens a menos do que esperado, pois o produto com id 14 ("Abacaxi na Brasa") não foi incluído na resposta.`

Justificativa (gerada por molde): O agente respondeu contagem_inconsistente no campo id porque o sinal itens: esperado 14 itens (referência em modo normal), recebido falta o id 14 ("Abacaxi na Brasa") está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,41 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,57); trate como hipótese e confira o campo id antes de agir.

## 2. Evidência

Poda de `arvore` (evento 2044): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 183}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 1 linha(s) da referência | 1 linha(s) novas |

Trecho podado (hash `7c54fbd0508aace9`):

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
    text "(mais 10 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 2045): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 1928}, depois {"chars": 277}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| itens | 14 itens (referência em modo normal) | falta o id 14 ("Abacaxi na Brasa") |

Trecho podado (hash `9675592a8385ee52`):

```text
lista com 13 itens (referência em modo normal: 14); falta o id 14 ("Abacaxi na Brasa"); primeiro item: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 2042): `GET /api/produtos` status 200; corpo `4f6d409f5a92ce2d`, árvore `None`.

## 3. Contraste com a segunda causa

contagem_inconsistente e não resposta_truncada: a escolha tem probabilidade 0,57 contra 0,41; verbete(s) na evidência: entidade-produto, contrato-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| contagem_inconsistente | 0,57 | sim |
| resposta_truncada | 0,41 |  |
| colecao_no_lugar_de_objeto | 0,01 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [estrutura_aninhada_divergente]`; verbetes citados: `contrato-produto`, `estrutura_aninhada_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `estrutura_aninhada_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `estrutura_aninhada_divergente` | confere | contexto: `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | confere | verbetes: `estrutura_aninhada_divergente` |
| fonte_formato_valido | `[contrato-produto], [estrutura_aninhada_divergente]` | confere | {"ids": ["contrato-produto", "estrutura_aninhada_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "contagem_inconsistente"} |
| fonte_contem_termo_da_causa | `estrutura_aninhada_divergente` | **não confere** | {"termo": "contagem_inconsistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids tra-21 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2038 | 1 | entrada | programa | ao_vivo | 2026-11-05T19:49:51 | caso tra-21 |
| 2039 | 2 | acao | programa | ao_vivo | 2026-11-05T19:49:51 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 107.2, "falhou": false} |
| 2040 | 3 | acao | programa | ao_vivo | 2026-11-05T19:49:51 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 11.7, "falhou": false} |
| 2041 | 4 | acao | programa | ao_vivo | 2026-11-05T19:49:51 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.1, "falhou": true} |
| 2042 | 5 | interceptacao | programa | ao_vivo | 2026-11-05T19:49:51 | GET /api/produtos 200 |
| 2043 | 6 | verificacao | verificacao | ao_vivo | 2026-11-05T19:49:51 | conferencia_do_roteiro: nao_confere |
| 2044 | 7 | poda | programa | ao_vivo | 2026-11-05T19:49:51 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 2045 | 8 | poda | programa | ao_vivo | 2026-11-05T19:49:51 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 2046 | 9 | candidatos | programa | ao_vivo | 2026-11-05T19:49:51 | 3 de 39 verbetes entregues |
| 2048 | 10 | prompt | programa | ao_vivo | 2026-11-05T19:49:51 | {"etapa": "diagnostico", "sha": "d1571cbf1236d817", "prompt_sha256": "d1571cbf1236", "chars": 4017, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2050 | 11 | inferencia | programa | ao_vivo | 2026-11-05T19:49:51 | diagnostico: 49,8 s |
| 2051 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T19:49:51 | causa_raiz: `contagem_inconsistente` |
| 2052 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T19:49:51 | campo: `id` |
| 2053 | 14 | declaracao | modelo | ao_vivo | 2026-11-05T19:49:51 | impacto: `O usuário vê uma lista com 10 itens a menos do que esperado, pois o produto com id 14 ("Abacaxi na Brasa") não foi incluído na resposta.` |
| 2054 | 15 | declaracao | modelo | ao_vivo | 2026-11-05T19:49:51 | fonte: `[contrato-produto], [estrutura_aninhada_divergente]` |
| 2055 | 16 | declaracao | modelo | ao_vivo | 2026-11-05T19:49:51 | fonte_citada: `contrato-produto` |
| 2056 | 17 | declaracao | modelo | ao_vivo | 2026-11-05T19:49:51 | fonte_citada: `estrutura_aninhada_divergente` |
| 2057 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T19:49:51 | quatro_linhas_presentes: confere |
| 2058 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T19:49:51 | rotulo_no_conjunto: confere |
| 2059 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T19:49:51 | fonte_existe_na_biblioteca: confere |
| 2060 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T19:49:51 | fonte_existe_na_biblioteca: confere |
| 2061 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T19:49:51 | fonte_estava_no_contexto: confere |
| 2062 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T19:49:51 | fonte_estava_no_contexto: confere |
| 2063 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T19:49:51 | campo_existe_no_caso: confere |
| 2064 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T19:49:51 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2065 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T19:49:51 | notas_nos_verbetes_citados: informativo |
| 2066 | 27 | verificacao | verificacao | ao_vivo | 2026-11-05T19:49:51 | impacto: nao_verificavel |
| 2067 | 28 | verificacao | verificacao | ao_vivo | 2026-11-05T19:49:51 | fonte_formato_valido: confere |
| 2068 | 29 | verificacao | verificacao | ao_vivo | 2026-11-05T19:49:51 | fonte_contem_termo_da_causa: nao_confere |
| 2069 | 30 | verificacao | verificacao | ao_vivo | 2026-11-05T19:49:51 | fonte_contem_termo_da_causa: nao_confere |
| 2070 | 31 | decisao | programa | ao_vivo | 2026-11-05T19:49:51 | diagnostico: escolha contagem_inconsistente; divergência não |

</details>

Nós de decisão:

- evento 2070, `diagnostico`: escolha `contagem_inconsistente`; resultado rotulo_emitido; evidência: evento 2045 (sinal_em_codigo), evento 2044 (arvore_podada), evento 2042 (corpo_http), evento 2046 (verbete_entregue, entidade-produto), evento 2046 (verbete_entregue, contrato-produto), evento 2046 (verbete_entregue, estrutura_aninhada_divergente), evento 2050 (resposta), evento 2055 (verbete_citado, contrato-produto), evento 2056 (verbete_citado, estrutura_aninhada_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2038 a 2070 da trilha; hash dos eventos deste caso: `8662386f97cf68fa`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
