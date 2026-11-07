<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-20`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v4/qwen2.5_7b/tra-20@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `chave_de_juncao_errada` · **CAMPO:** `tipo` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê categorias incorretas atribuídas aos produtos, como "Bebidas" em vez de "Carnes".`

Justificativa (gerada por molde): O agente respondeu chave_de_juncao_errada no campo tipo porque o sinal tipo: esperado "Carnes" (referência em modo normal), recebido "Bebidas" em 4 itens está presente na resposta HTTP e os verbetes chave_de_juncao_errada, entidade-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1981): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 1982): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2068}, depois {"chars": 241}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tipo | "Carnes" (referência em modo normal) | "Bebidas" em 4 itens |

Trecho podado (hash `a1a95c61af5cf648`):

```text
lista com 14 itens (referência em modo normal: 14); tipo diferente em 4 itens; por exemplo: {"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Bebidas", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}
```

Interceptação (evento 1977): `GET /api/produtos` status 200; corpo `0ef7077cc7a06cfa`, árvore `None`.

## 3. Contraste com a segunda causa

chave_de_juncao_errada e não tipo_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: chave_de_juncao_errada, entidade-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| chave_de_juncao_errada | 1,00 | sim |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[chave_de_juncao_errada]`; verbetes citados: `chave_de_juncao_errada`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `chave_de_juncao_errada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `chave_de_juncao_errada` | confere | contexto: `chave_de_juncao_errada`, `entidade-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `chave_de_juncao_errada` | confere | verbetes: `chave_de_juncao_errada`, `entidade-produto` |
| fonte_formato_valido | `[chave_de_juncao_errada]` | confere | {"ids": ["chave_de_juncao_errada"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `chave_de_juncao_errada` | confere | {"termo": "chave_de_juncao_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-20 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1971 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:04:20 | caso tra-20 |
| 1972 | 2 | acao | programa | ao_vivo | 2026-11-06T11:04:20 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 109.2, "falhou": false} |
| 1973 | 3 | acao | programa | ao_vivo | 2026-11-06T11:04:20 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 13.7, "falhou": false} |
| 1974 | 4 | acao | programa | ao_vivo | 2026-11-06T11:04:20 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.2, "falhou": false} |
| 1975 | 5 | acao | programa | ao_vivo | 2026-11-06T11:04:20 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 5.2, "falhou": false} |
| 1976 | 6 | acao | programa | ao_vivo | 2026-11-06T11:04:20 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.5, "falhou": false} |
| 1977 | 7 | interceptacao | programa | ao_vivo | 2026-11-06T11:04:20 | GET /api/produtos 200 |
| 1978 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:20 | conferencia_do_roteiro: confere |
| 1979 | 9 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:20 | conferencia_do_roteiro: confere |
| 1980 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:20 | conferencia_do_roteiro: confere |
| 1981 | 11 | poda | programa | ao_vivo | 2026-11-06T11:04:20 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1982 | 12 | poda | programa | ao_vivo | 2026-11-06T11:04:20 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1983 | 13 | candidatos | programa | ao_vivo | 2026-11-06T11:04:20 | 3 de 39 verbetes entregues |
| 1984 | 14 | prompt | programa | ao_vivo | 2026-11-06T11:04:20 | {"etapa": "diagnostico", "sha": "d13621a965e0c6be", "prompt_sha256": "d13621a965e0", "chars": 4239, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1985 | 15 | inferencia | programa | ao_vivo | 2026-11-06T11:04:20 | diagnostico: 17,9 s |
| 1986 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T11:04:20 | causa_raiz: `chave_de_juncao_errada` |
| 1987 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T11:04:20 | campo: `tipo` |
| 1988 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T11:04:20 | impacto: `O usuário vê categorias incorretas atribuídas aos produtos, como "Bebidas" em vez de "Carnes".` |
| 1989 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T11:04:20 | fonte: `[chave_de_juncao_errada]` |
| 1990 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T11:04:20 | fonte_citada: `chave_de_juncao_errada` |
| 1991 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:20 | quatro_linhas_presentes: confere |
| 1992 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:20 | rotulo_no_conjunto: confere |
| 1993 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:20 | fonte_existe_na_biblioteca: confere |
| 1994 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:20 | fonte_estava_no_contexto: confere |
| 1995 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:20 | campo_existe_no_caso: confere |
| 1996 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:20 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1997 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:20 | notas_nos_verbetes_citados: informativo |
| 1998 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:20 | impacto: nao_verificavel |
| 1999 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:20 | fonte_formato_valido: confere |
| 2000 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:20 | fonte_contem_termo_da_causa: confere |
| 2001 | 31 | decisao | programa | ao_vivo | 2026-11-06T11:04:20 | diagnostico: escolha chave_de_juncao_errada; divergência não |

</details>

Nós de decisão:

- evento 2001, `diagnostico`: escolha `chave_de_juncao_errada`; resultado rotulo_emitido; evidência: evento 1982 (sinal_em_codigo), evento 1981 (arvore_podada), evento 1977 (corpo_http), evento 1983 (verbete_entregue, chave_de_juncao_errada), evento 1983 (verbete_entregue, entidade-produto), evento 1983 (verbete_entregue, tipo_divergente), evento 1985 (resposta), evento 1990 (verbete_citado, chave_de_juncao_errada); divergência: não; falha: nenhuma; prov.used: chave_de_juncao_errada, entidade-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1971 a 2001 da trilha; hash dos eventos deste caso: `6a7740d2cbdcbc7f`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
