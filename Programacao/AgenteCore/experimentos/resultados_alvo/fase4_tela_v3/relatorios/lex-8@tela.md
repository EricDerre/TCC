<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-8`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/lex-8@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `resumo` · selo de probabilidade: **medio** (p = 0,91)

**IMPACTO (declarado):** `O usuário vê um resumo com caracteres acentuados errados e uma descrição incompleta, o que pode causar confusão na apresentação dos produtos.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo resumo porque o sinal resumo: esperado "Garrafa 500ml, com ou sem gás" (referência em modo normal), recebido "Garrafa 500ml, com ou sem gÃ¡s" em 4 itens está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,06. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 680): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 682): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2073}, depois {"chars": 245}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| resumo | "Garrafa 500ml, com ou sem gás" (referência em modo normal) | "Garrafa 500ml, com ou sem gÃ¡s" em 4 itens |

Trecho podado (hash `a99e0439860e5b38`):

```text
lista com 14 itens (referência em modo normal: 14); resumo diferente em 4 itens; por exemplo: {"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gÃ¡s", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}
```

Interceptação (evento 676): `GET /api/produtos` status 200; corpo `40dfa78ee8bc48ac`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 0,91 contra 0,06; verbete(s) na evidência: entidade-produto, contrato-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,91 | sim |
| campo_ausente | 0,06 |  |
| campo_renomeado | 0,06 |  |
| colecao_no_lugar_de_objeto | 0,02 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [tipo_divergente]`; verbetes citados: `contrato-produto`, `tipo_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| fonte_formato_valido | `[contrato-produto] [tipo_divergente]` | confere | {"ids": ["contrato-produto", "tipo_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `resumo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids lex-8 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 669 | 1 | entrada | programa | ao_vivo | 2026-11-05T19:05:09 | caso lex-8 |
| 670 | 2 | acao | programa | ao_vivo | 2026-11-05T19:05:09 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 114.1, "falhou": false} |
| 671 | 3 | acao | programa | ao_vivo | 2026-11-05T19:05:09 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 8.1, "falhou": false} |
| 672 | 4 | acao | programa | ao_vivo | 2026-11-05T19:05:09 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 3.0, "falhou": false} |
| 673 | 5 | acao | programa | ao_vivo | 2026-11-05T19:05:09 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 5.2, "falhou": false} |
| 674 | 6 | acao | programa | ao_vivo | 2026-11-05T19:05:09 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.8, "falhou": false} |
| 676 | 7 | interceptacao | programa | ao_vivo | 2026-11-05T19:05:09 | GET /api/produtos 200 |
| 677 | 8 | verificacao | verificacao | ao_vivo | 2026-11-05T19:05:09 | conferencia_do_roteiro: confere |
| 678 | 9 | verificacao | verificacao | ao_vivo | 2026-11-05T19:05:09 | conferencia_do_roteiro: confere |
| 679 | 10 | verificacao | verificacao | ao_vivo | 2026-11-05T19:05:09 | conferencia_do_roteiro: confere |
| 680 | 11 | poda | programa | ao_vivo | 2026-11-05T19:05:09 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 682 | 12 | poda | programa | ao_vivo | 2026-11-05T19:05:09 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 683 | 13 | candidatos | programa | ao_vivo | 2026-11-05T19:05:09 | 3 de 39 verbetes entregues |
| 685 | 14 | prompt | programa | ao_vivo | 2026-11-05T19:05:09 | {"etapa": "diagnostico", "sha": "e18af006e0e08ce9", "prompt_sha256": "e18af006e0e0", "chars": 3895, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 687 | 15 | inferencia | programa | ao_vivo | 2026-11-05T19:05:09 | diagnostico: 46,1 s |
| 688 | 16 | declaracao | modelo | ao_vivo | 2026-11-05T19:05:09 | causa_raiz: `tipo_divergente` |
| 689 | 17 | declaracao | modelo | ao_vivo | 2026-11-05T19:05:09 | campo: `resumo` |
| 690 | 18 | declaracao | modelo | ao_vivo | 2026-11-05T19:05:09 | impacto: `O usuário vê um resumo com caracteres acentuados errados e uma descrição incompleta, o que pode causar confusão na apresentação dos produtos.` |
| 691 | 19 | declaracao | modelo | ao_vivo | 2026-11-05T19:05:09 | fonte: `[contrato-produto] [tipo_divergente]` |
| 692 | 20 | declaracao | modelo | ao_vivo | 2026-11-05T19:05:09 | fonte_citada: `contrato-produto` |
| 693 | 21 | declaracao | modelo | ao_vivo | 2026-11-05T19:05:09 | fonte_citada: `tipo_divergente` |
| 694 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T19:05:09 | quatro_linhas_presentes: confere |
| 695 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T19:05:09 | rotulo_no_conjunto: confere |
| 696 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T19:05:09 | fonte_existe_na_biblioteca: confere |
| 697 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T19:05:09 | fonte_existe_na_biblioteca: confere |
| 698 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T19:05:09 | fonte_estava_no_contexto: confere |
| 699 | 27 | verificacao | verificacao | ao_vivo | 2026-11-05T19:05:09 | fonte_estava_no_contexto: confere |
| 700 | 28 | verificacao | verificacao | ao_vivo | 2026-11-05T19:05:09 | campo_existe_no_caso: confere |
| 701 | 29 | verificacao | verificacao | ao_vivo | 2026-11-05T19:05:09 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 702 | 30 | verificacao | verificacao | ao_vivo | 2026-11-05T19:05:09 | notas_nos_verbetes_citados: informativo |
| 703 | 31 | verificacao | verificacao | ao_vivo | 2026-11-05T19:05:09 | impacto: nao_verificavel |
| 704 | 32 | verificacao | verificacao | ao_vivo | 2026-11-05T19:05:09 | fonte_formato_valido: confere |
| 705 | 33 | verificacao | verificacao | ao_vivo | 2026-11-05T19:05:09 | fonte_contem_termo_da_causa: nao_confere |
| 706 | 34 | verificacao | verificacao | ao_vivo | 2026-11-05T19:05:09 | fonte_contem_termo_da_causa: confere |
| 707 | 35 | decisao | programa | ao_vivo | 2026-11-05T19:05:09 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 707, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 682 (sinal_em_codigo), evento 680 (arvore_podada), evento 676 (corpo_http), evento 683 (verbete_entregue, entidade-produto), evento 683 (verbete_entregue, contrato-produto), evento 683 (verbete_entregue, tipo_divergente), evento 687 (resposta), evento 692 (verbete_citado, contrato-produto), evento 693 (verbete_citado, tipo_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 669 a 707 da trilha; hash dos eventos deste caso: `7982ac0ae7d24630`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
