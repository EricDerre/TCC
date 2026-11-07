<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-11`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v4/qwen2.5_7b/sin-11@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `estrutura_aninhada_divergente` · **CAMPO:** `preco` · selo de probabilidade: **medio** (p = 0,96)

**IMPACTO (declarado):** `A interface exibe um preço em formato inválido, causando confusão para o usuário.`

Justificativa (gerada por molde): O agente respondeu estrutura_aninhada_divergente no campo preco porque o sinal preco: esperado numero, recebido objeto está presente na resposta HTTP e os verbetes contrato-produto, estrutura_aninhada_divergente, entidade-produto estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 848): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `9edb71a2567f3fd5`):

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
      button "[object Object]" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "[object Object]" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "[object Object]" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 850): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2404}, depois {"chars": 42}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | numero | objeto |
| preco | 89.9 (referência em modo normal) | {"valor": 89.9, "moeda": "BRL"} em 14 itens |

Trecho podado (hash `a7ecb809577d7a2c`):

```text
{"preco": {"valor": 89.9, "moeda": "BRL"}}
```

Interceptação (evento 844): `GET /api/produtos` status 200; corpo `f148d81d95af83fe`, árvore `None`.

## 3. Contraste com a segunda causa

estrutura_aninhada_divergente e não campo_ausente: a escolha tem probabilidade 0,96 contra 0,00; verbete(s) na evidência: contrato-produto, estrutura_aninhada_divergente, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| estrutura_aninhada_divergente | 0,96 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| tipo_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| resposta_truncada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[estrutura_aninhada_divergente]`; verbetes citados: `estrutura_aninhada_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `estrutura_aninhada_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `estrutura_aninhada_divergente` | confere | contexto: `contrato-produto`, `estrutura_aninhada_divergente`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `estrutura_aninhada_divergente` | confere | verbetes: `estrutura_aninhada_divergente` |
| fonte_formato_valido | `[estrutura_aninhada_divergente]` | confere | {"ids": ["estrutura_aninhada_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `estrutura_aninhada_divergente` | confere | {"termo": "estrutura_aninhada_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-11 --k 3`

## 6. Árvore completa

<details><summary>29 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 838 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:26:19 | caso sin-11 |
| 839 | 2 | acao | programa | ao_vivo | 2026-11-06T10:26:20 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 112.6, "falhou": false} |
| 840 | 3 | acao | programa | ao_vivo | 2026-11-06T10:26:20 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 8.7, "falhou": false} |
| 841 | 4 | acao | programa | ao_vivo | 2026-11-06T10:26:20 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.4, "falhou": false} |
| 842 | 5 | acao | programa | ao_vivo | 2026-11-06T10:26:20 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 4.8, "falhou": true} |
| 844 | 6 | interceptacao | programa | ao_vivo | 2026-11-06T10:26:20 | GET /api/produtos 200 |
| 845 | 7 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | conferencia_do_roteiro: confere |
| 846 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | conferencia_do_roteiro: nao_confere |
| 848 | 9 | poda | programa | ao_vivo | 2026-11-06T10:26:20 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 850 | 10 | poda | programa | ao_vivo | 2026-11-06T10:26:20 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 851 | 11 | candidatos | programa | ao_vivo | 2026-11-06T10:26:20 | 3 de 39 verbetes entregues |
| 853 | 12 | prompt | programa | ao_vivo | 2026-11-06T10:26:20 | {"etapa": "diagnostico", "sha": "3daebe03e9899b4b", "prompt_sha256": "3daebe03e989", "chars": 3834, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 855 | 13 | inferencia | programa | ao_vivo | 2026-11-06T10:26:20 | diagnostico: 76,0 s |
| 856 | 14 | declaracao | modelo | ao_vivo | 2026-11-06T10:26:20 | causa_raiz: `estrutura_aninhada_divergente` |
| 857 | 15 | declaracao | modelo | ao_vivo | 2026-11-06T10:26:20 | campo: `preco` |
| 858 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T10:26:20 | impacto: `A interface exibe um preço em formato inválido, causando confusão para o usuário.` |
| 859 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T10:26:20 | fonte: `[estrutura_aninhada_divergente]` |
| 860 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T10:26:20 | fonte_citada: `estrutura_aninhada_divergente` |
| 861 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | quatro_linhas_presentes: confere |
| 862 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | rotulo_no_conjunto: confere |
| 863 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | fonte_existe_na_biblioteca: confere |
| 864 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | fonte_estava_no_contexto: confere |
| 865 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | campo_existe_no_caso: confere |
| 866 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 867 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | notas_nos_verbetes_citados: informativo |
| 868 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | impacto: nao_verificavel |
| 869 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | fonte_formato_valido: confere |
| 870 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | fonte_contem_termo_da_causa: confere |
| 871 | 29 | decisao | programa | ao_vivo | 2026-11-06T10:26:20 | diagnostico: escolha estrutura_aninhada_divergente; divergência não |

</details>

Nós de decisão:

- evento 871, `diagnostico`: escolha `estrutura_aninhada_divergente`; resultado rotulo_emitido; evidência: evento 850 (sinal_em_codigo), evento 848 (arvore_podada), evento 844 (corpo_http), evento 851 (verbete_entregue, contrato-produto), evento 851 (verbete_entregue, estrutura_aninhada_divergente), evento 851 (verbete_entregue, entidade-produto), evento 855 (resposta), evento 860 (verbete_citado, estrutura_aninhada_divergente); divergência: não; falha: nenhuma; prov.used: contrato-produto, estrutura_aninhada_divergente, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 838 a 871 da trilha; hash dos eventos deste caso: `9ba1c6113c6f4614`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
