<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-11`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/sin-11@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `preco` · selo de probabilidade: **baixo** (p = 0,74)

**IMPACTO (declarado):** `O usuário vê botões sem texto em vez de preços formatados corretamente.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo preco porque o sinal preco: esperado numero, recebido objeto está presente na resposta HTTP e os verbetes campo_ausente, estrutura_aninhada_divergente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,17. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,74); trate como hipótese e confira o campo preco antes de agir.

## 2. Evidência

Poda de `arvore` (evento 889): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 891): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2404}, depois {"chars": 42}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | numero | objeto |
| preco | 89.9 (referência em modo normal) | {"valor": 89.9, "moeda": "BRL"} em 14 itens |

Trecho podado (hash `a7ecb809577d7a2c`):

```text
{"preco": {"valor": 89.9, "moeda": "BRL"}}
```

Interceptação (evento 885): `GET /api/produtos` status 200; corpo `f148d81d95af83fe`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 0,74 contra 0,17; verbete(s) na evidência: campo_ausente, estrutura_aninhada_divergente, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,74 | sim |
| campo_ausente | 0,17 |  |
| campo_renomeado | 0,17 |  |
| estrutura_aninhada_divergente | 0,07 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente] [contrato-produto]`; verbetes citados: `campo_ausente`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `campo_ausente`, `estrutura_aninhada_divergente`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `campo_ausente`, `estrutura_aninhada_divergente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[campo_ausente] [contrato-produto]` | confere | {"ids": ["campo_ausente", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_ausente` | **não confere** | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids sin-11 --k 3`

## 6. Árvore completa

<details><summary>33 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 879 | 1 | entrada | programa | ao_vivo | 2026-11-01T14:41:26 | caso sin-11 |
| 880 | 2 | acao | programa | ao_vivo | 2026-11-01T14:41:27 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 128.6, "falhou": false} |
| 881 | 3 | acao | programa | ao_vivo | 2026-11-01T14:41:27 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 12.5, "falhou": false} |
| 882 | 4 | acao | programa | ao_vivo | 2026-11-01T14:41:27 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 3.1, "falhou": false} |
| 883 | 5 | acao | programa | ao_vivo | 2026-11-01T14:41:27 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 7.8, "falhou": true} |
| 885 | 6 | interceptacao | programa | ao_vivo | 2026-11-01T14:41:27 | GET /api/produtos 200 |
| 886 | 7 | verificacao | verificacao | ao_vivo | 2026-11-01T14:41:27 | conferencia_do_roteiro: confere |
| 887 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T14:41:27 | conferencia_do_roteiro: nao_confere |
| 889 | 9 | poda | programa | ao_vivo | 2026-11-01T14:41:27 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 891 | 10 | poda | programa | ao_vivo | 2026-11-01T14:41:27 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 892 | 11 | candidatos | programa | ao_vivo | 2026-11-01T14:41:27 | 3 de 40 verbetes entregues |
| 894 | 12 | prompt | programa | ao_vivo | 2026-11-01T14:41:27 | {"etapa": "diagnostico", "sha": "9131238266968d36", "prompt_sha256": "913123826696", "chars": 5802, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 896 | 13 | inferencia | programa | ao_vivo | 2026-11-01T14:41:27 | diagnostico: 96,7 s |
| 897 | 14 | declaracao | modelo | ao_vivo | 2026-11-01T14:41:27 | causa_raiz: `tipo_divergente` |
| 898 | 15 | declaracao | modelo | ao_vivo | 2026-11-01T14:41:27 | campo: `preco` |
| 899 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T14:41:27 | impacto: `O usuário vê botões sem texto em vez de preços formatados corretamente.` |
| 900 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T14:41:27 | fonte: `[campo_ausente] [contrato-produto]` |
| 901 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T14:41:27 | fonte_citada: `campo_ausente` |
| 902 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T14:41:27 | fonte_citada: `contrato-produto` |
| 903 | 20 | verificacao | verificacao | ao_vivo | 2026-11-01T14:41:27 | quatro_linhas_presentes: confere |
| 904 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T14:41:27 | rotulo_no_conjunto: confere |
| 905 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T14:41:27 | fonte_existe_na_biblioteca: confere |
| 906 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T14:41:27 | fonte_existe_na_biblioteca: confere |
| 907 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T14:41:27 | fonte_estava_no_contexto: confere |
| 908 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T14:41:27 | fonte_estava_no_contexto: confere |
| 909 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T14:41:27 | campo_existe_no_caso: confere |
| 910 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T14:41:27 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 911 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T14:41:27 | notas_nos_verbetes_citados: informativo |
| 912 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T14:41:27 | impacto: nao_verificavel |
| 913 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T14:41:27 | fonte_formato_valido: confere |
| 914 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T14:41:27 | fonte_contem_termo_da_causa: nao_confere |
| 915 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T14:41:27 | fonte_contem_termo_da_causa: nao_confere |
| 916 | 33 | decisao | programa | ao_vivo | 2026-11-01T14:41:27 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 916, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 891 (sinal_em_codigo), evento 889 (arvore_podada), evento 885 (corpo_http), evento 892 (verbete_entregue, campo_ausente), evento 892 (verbete_entregue, estrutura_aninhada_divergente), evento 892 (verbete_entregue, contrato-produto), evento 896 (resposta), evento 901 (verbete_citado, campo_ausente), evento 902 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: campo_ausente, estrutura_aninhada_divergente, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 879 a 916 da trilha; hash dos eventos deste caso: `e26088bed747afe9`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
