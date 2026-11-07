<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-26`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/semt-26@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `nulo_inesperado` · **CAMPO:** `resumo` · selo de probabilidade: **medio** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê um produto sem descrição, enquanto a referência mostra a descrição completa.`

Justificativa (gerada por molde): O agente respondeu nulo_inesperado no campo resumo porque o sinal resumo: esperado "Queijo coalho grelhado com mel" (referência em modo normal), recebido null está presente na resposta HTTP e os verbetes contrato-produto, entidade-produto, nulo_inesperado estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 942): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 197}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 4 linha(s) da referência | 1 linha(s) novas |

Trecho podado (hash `6476ae0aa98a0937`):

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
      text "destaque: Sim"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
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
    heading "Queijo Coalho" level=4
    text "(sem descrição)"

```

Poda de `corpo_http` (evento 944): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 122}, depois {"chars": 228}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| resumo | "Queijo coalho grelhado com mel" (referência em modo normal) | null |

Trecho podado (hash `453aed492dfa9ae5`):

```text
{"id": 12, "nome": "Queijo Coalho", "resumo": null, "tipo": "Acompanhamentos", "preco": 22.9, "imagem": "queijo.png", "destaque": true} (contra a referência em modo normal: resumo null em vez de "Queijo coalho grelhado com mel")
```

Interceptação (evento 935): `GET /api/produtos` status 200; corpo `e76e0faee9ddea73`, árvore `None`.

Interceptação (evento 937): `GET /api/produtos/12` status 200; corpo `01404db46334dbb5`, árvore `None`.

## 3. Contraste com a segunda causa

nulo_inesperado e não campo_ausente: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: contrato-produto, entidade-produto, nulo_inesperado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| nulo_inesperado | 0,99 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| tipo_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[nulo_inesperado]`; verbetes citados: `nulo_inesperado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `contrato-produto`, `entidade-produto`, `nulo_inesperado` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `nulo_inesperado` |
| fonte_formato_valido | `[nulo_inesperado]` | confere | {"ids": ["nulo_inesperado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `resumo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids semt-26 --k 3`

## 6. Árvore completa

<details><summary>34 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 926 | 1 | entrada | programa | ao_vivo | 2026-11-06T12:01:18 | caso semt-26 |
| 927 | 2 | acao | programa | ao_vivo | 2026-11-06T12:01:19 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 88.2, "falhou": false} |
| 928 | 3 | acao | programa | ao_vivo | 2026-11-06T12:01:19 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 10.0, "falhou": false} |
| 929 | 4 | acao | programa | ao_vivo | 2026-11-06T12:01:19 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.6, "falhou": false} |
| 930 | 5 | acao | programa | ao_vivo | 2026-11-06T12:01:19 | {"passo": 4, "acao": "clicar", "seletor": "#produtos-api-grid .saiba-mais[data-id='12']", "url": null, "tempo_ms": 22.8, "falhou": false} |
| 931 | 6 | acao | programa | ao_vivo | 2026-11-06T12:01:19 | {"passo": 5, "acao": "esperar", "seletor": "#modalDetalhe", "url": null, "tempo_ms": 217.8, "falhou": false} |
| 932 | 7 | acao | programa | ao_vivo | 2026-11-06T12:01:19 | {"passo": 6, "acao": "conferir", "seletor": "#modalDetalheTitulo", "url": null, "tempo_ms": 3.6, "falhou": false} |
| 933 | 8 | acao | programa | ao_vivo | 2026-11-06T12:01:19 | {"passo": 7, "acao": "conferir", "seletor": "#modalDetalheCorpo", "url": null, "tempo_ms": 3.3, "falhou": false} |
| 935 | 9 | interceptacao | programa | ao_vivo | 2026-11-06T12:01:19 | GET /api/produtos 200 |
| 937 | 10 | interceptacao | programa | ao_vivo | 2026-11-06T12:01:19 | GET /api/produtos/12 200 |
| 938 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T12:01:19 | conferencia_do_roteiro: confere |
| 939 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T12:01:19 | conferencia_do_roteiro: confere |
| 940 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T12:01:19 | conferencia_do_roteiro: confere |
| 942 | 14 | poda | programa | ao_vivo | 2026-11-06T12:01:19 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 944 | 15 | poda | programa | ao_vivo | 2026-11-06T12:01:19 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 945 | 16 | candidatos | programa | ao_vivo | 2026-11-06T12:01:19 | 3 de 39 verbetes entregues |
| 947 | 17 | prompt | programa | ao_vivo | 2026-11-06T12:01:19 | {"etapa": "diagnostico", "sha": "57f6e4790accd846", "prompt_sha256": "57f6e4790acc", "chars": 3642, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 949 | 18 | inferencia | programa | ao_vivo | 2026-11-06T12:01:19 | diagnostico: 53,0 s |
| 950 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T12:01:19 | causa_raiz: `nulo_inesperado` |
| 951 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T12:01:19 | campo: `resumo` |
| 952 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T12:01:19 | impacto: `O usuário vê um produto sem descrição, enquanto a referência mostra a descrição completa.` |
| 953 | 22 | declaracao | modelo | ao_vivo | 2026-11-06T12:01:19 | fonte: `[nulo_inesperado]` |
| 954 | 23 | declaracao | modelo | ao_vivo | 2026-11-06T12:01:19 | fonte_citada: `nulo_inesperado` |
| 955 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T12:01:19 | quatro_linhas_presentes: confere |
| 956 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T12:01:19 | rotulo_no_conjunto: confere |
| 957 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T12:01:19 | fonte_existe_na_biblioteca: confere |
| 958 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T12:01:19 | fonte_estava_no_contexto: confere |
| 959 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T12:01:19 | campo_existe_no_caso: confere |
| 960 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T12:01:19 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 961 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T12:01:19 | notas_nos_verbetes_citados: informativo |
| 962 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T12:01:19 | impacto: nao_verificavel |
| 963 | 32 | verificacao | verificacao | ao_vivo | 2026-11-06T12:01:19 | fonte_formato_valido: confere |
| 964 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T12:01:19 | fonte_contem_termo_da_causa: confere |
| 965 | 34 | decisao | programa | ao_vivo | 2026-11-06T12:01:19 | diagnostico: escolha nulo_inesperado; divergência não |

</details>

Nós de decisão:

- evento 965, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 944 (sinal_em_codigo), evento 942 (arvore_podada), evento 937 (corpo_http), evento 945 (verbete_entregue, contrato-produto), evento 945 (verbete_entregue, entidade-produto), evento 945 (verbete_entregue, nulo_inesperado), evento 949 (resposta), evento 954 (verbete_citado, nulo_inesperado); divergência: não; falha: nenhuma; prov.used: contrato-produto, entidade-produto, nulo_inesperado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 926 a 965 da trilha; hash dos eventos deste caso: `6aa549418242f3ec`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
