<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-20`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/tra-20@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `tipo` · selo de probabilidade: **baixo** (p = 0,56)

**IMPACTO (declarado):** `O usuário vê produtos classificados incorretamente, como bebidas ao invés de carnes.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo tipo porque o sinal tipo: esperado "Carnes" (referência em modo normal), recebido "Bebidas" em 4 itens está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,39. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,56); trate como hipótese e confira o campo tipo antes de agir.

## 2. Evidência

Poda de `arvore` (evento 1993): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 1994): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2068}, depois {"chars": 241}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tipo | "Carnes" (referência em modo normal) | "Bebidas" em 4 itens |

Trecho podado (hash `a1a95c61af5cf648`):

```text
lista com 14 itens (referência em modo normal: 14); tipo diferente em 4 itens; por exemplo: {"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Bebidas", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}
```

Interceptação (evento 1989): `GET /api/produtos` status 200; corpo `0ef7077cc7a06cfa`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não estrutura_aninhada_divergente: a escolha tem probabilidade 0,56 contra 0,39; verbete(s) na evidência: entidade-produto, contrato-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,56 | sim |
| estrutura_aninhada_divergente | 0,39 |  |
| campo_ausente | 0,04 |  |
| campo_renomeado | 0,04 |  |
| colecao_no_lugar_de_objeto | 0,01 |  |
| chave_de_juncao_errada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `contrato-produto` |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids tra-20 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1983 | 1 | entrada | programa | ao_vivo | 2026-11-05T19:47:55 | caso tra-20 |
| 1984 | 2 | acao | programa | ao_vivo | 2026-11-05T19:47:56 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 110.2, "falhou": false} |
| 1985 | 3 | acao | programa | ao_vivo | 2026-11-05T19:47:56 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 8.2, "falhou": false} |
| 1986 | 4 | acao | programa | ao_vivo | 2026-11-05T19:47:56 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.8, "falhou": false} |
| 1987 | 5 | acao | programa | ao_vivo | 2026-11-05T19:47:56 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 5.7, "falhou": false} |
| 1988 | 6 | acao | programa | ao_vivo | 2026-11-05T19:47:56 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.6, "falhou": false} |
| 1989 | 7 | interceptacao | programa | ao_vivo | 2026-11-05T19:47:56 | GET /api/produtos 200 |
| 1990 | 8 | verificacao | verificacao | ao_vivo | 2026-11-05T19:47:56 | conferencia_do_roteiro: confere |
| 1991 | 9 | verificacao | verificacao | ao_vivo | 2026-11-05T19:47:56 | conferencia_do_roteiro: confere |
| 1992 | 10 | verificacao | verificacao | ao_vivo | 2026-11-05T19:47:56 | conferencia_do_roteiro: confere |
| 1993 | 11 | poda | programa | ao_vivo | 2026-11-05T19:47:56 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1994 | 12 | poda | programa | ao_vivo | 2026-11-05T19:47:56 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1995 | 13 | candidatos | programa | ao_vivo | 2026-11-05T19:47:56 | 3 de 39 verbetes entregues |
| 1996 | 14 | prompt | programa | ao_vivo | 2026-11-05T19:47:56 | {"etapa": "diagnostico", "sha": "b95a3f525739aaab", "prompt_sha256": "b95a3f525739", "chars": 3865, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1997 | 15 | inferencia | programa | ao_vivo | 2026-11-05T19:47:56 | diagnostico: 37,5 s |
| 1998 | 16 | declaracao | modelo | ao_vivo | 2026-11-05T19:47:56 | causa_raiz: `tipo_divergente` |
| 1999 | 17 | declaracao | modelo | ao_vivo | 2026-11-05T19:47:56 | campo: `tipo` |
| 2000 | 18 | declaracao | modelo | ao_vivo | 2026-11-05T19:47:56 | impacto: `O usuário vê produtos classificados incorretamente, como bebidas ao invés de carnes.` |
| 2001 | 19 | declaracao | modelo | ao_vivo | 2026-11-05T19:47:56 | fonte: `[contrato-produto]` |
| 2002 | 20 | declaracao | modelo | ao_vivo | 2026-11-05T19:47:56 | fonte_citada: `contrato-produto` |
| 2003 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T19:47:56 | quatro_linhas_presentes: confere |
| 2004 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T19:47:56 | rotulo_no_conjunto: confere |
| 2005 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T19:47:56 | fonte_existe_na_biblioteca: confere |
| 2006 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T19:47:56 | fonte_estava_no_contexto: confere |
| 2007 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T19:47:56 | campo_existe_no_caso: confere |
| 2008 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T19:47:56 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2009 | 27 | verificacao | verificacao | ao_vivo | 2026-11-05T19:47:56 | notas_nos_verbetes_citados: informativo |
| 2010 | 28 | verificacao | verificacao | ao_vivo | 2026-11-05T19:47:56 | impacto: nao_verificavel |
| 2011 | 29 | verificacao | verificacao | ao_vivo | 2026-11-05T19:47:56 | fonte_formato_valido: confere |
| 2012 | 30 | verificacao | verificacao | ao_vivo | 2026-11-05T19:47:56 | fonte_contem_termo_da_causa: nao_confere |
| 2013 | 31 | decisao | programa | ao_vivo | 2026-11-05T19:47:56 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 2013, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1994 (sinal_em_codigo), evento 1993 (arvore_podada), evento 1989 (corpo_http), evento 1995 (verbete_entregue, entidade-produto), evento 1995 (verbete_entregue, contrato-produto), evento 1995 (verbete_entregue, estrutura_aninhada_divergente), evento 1997 (resposta), evento 2002 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1983 a 2013 da trilha; hash dos eventos deste caso: `96323936cfe16e9c`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
