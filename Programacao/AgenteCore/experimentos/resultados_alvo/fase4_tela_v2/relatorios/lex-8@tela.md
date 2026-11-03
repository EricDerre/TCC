<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-8`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/lex-8@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `formato_de_data_divergente` · **CAMPO:** `nenhum` · selo de probabilidade: **baixo** (p = 0,22) · **CONFLITO**: nenhum verbete entregue trata da causa respondida formato_de_data_divergente

**IMPACTO (declarado):** `A interface exibe preços com acentos faltando, causando uma leitura incorreta dos preços.`

Justificativa (gerada por molde): O agente respondeu formato_de_data_divergente no campo resumo porque o sinal resumo: esperado "Garrafa 500ml, com ou sem gás" (referência em modo normal), recebido "Garrafa 500ml, com ou sem gÃ¡s" em 4 itens está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, contagem_inconsistente estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,14. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida formato_de_data_divergente. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,22); trate como hipótese e confira o campo resumo antes de agir.

## 2. Evidência

Poda de `arvore` (evento 707): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 709): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2073}, depois {"chars": 412}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| resumo | "Garrafa 500ml, com ou sem gás" (referência em modo normal) | "Garrafa 500ml, com ou sem gÃ¡s" em 4 itens |

Trecho podado (hash `274a6c69751a98f7`):

```text
lista com 14 itens (referência em modo normal: 14); resumo diferente em 4 itens; por exemplo: {"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gÃ¡s", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}; {"id": 11, "nome": "Pão de Alho", "resumo": "PÃ£o de alho grelhado na brasa", "tipo": "Acompanhamentos", "preco": 16.9, "imagem": "paodealho.png", "destaque": false}
```

Interceptação (evento 703): `GET /api/produtos` status 200; corpo `40dfa78ee8bc48ac`, árvore `None`.

## 3. Contraste com a segunda causa

formato_de_data_divergente e não estrutura_aninhada_divergente: a escolha tem probabilidade 0,22 contra 0,14; verbete(s) na evidência: entidade-produto, contrato-produto, contagem_inconsistente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| formato_de_data_divergente | 0,22 | sim |
| estrutura_aninhada_divergente | 0,14 |  |
| contagem_inconsistente | 0,13 |  |
| colecao_no_lugar_de_objeto | 0,12 |  |
| campo_ausente | 0,10 |  |
| campo_renomeado | 0,10 |  |
| tipo_divergente | 0,07 |  |
| valor_fora_do_dominio | 0,06 |  |
| resposta_truncada | 0,05 |  |
| corpo_nao_e_json | 0,05 |  |
| corpo_vazio | 0,05 |  |
| codificacao_incorreta | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente` |
| Algum verbete do contexto trata da causa respondida | `formato_de_data_divergente` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[entidade-produto], [contrato-produto]` | confere | {"ids": ["entidade-produto", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "formato_de_data_divergente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "formato_de_data_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids lex-8 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 696 | 1 | entrada | programa | ao_vivo | 2026-11-01T14:35:06 | caso lex-8 |
| 697 | 2 | acao | programa | ao_vivo | 2026-11-01T14:35:06 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 195.8, "falhou": false} |
| 698 | 3 | acao | programa | ao_vivo | 2026-11-01T14:35:06 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 9.2, "falhou": false} |
| 699 | 4 | acao | programa | ao_vivo | 2026-11-01T14:35:06 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 3.1, "falhou": false} |
| 700 | 5 | acao | programa | ao_vivo | 2026-11-01T14:35:06 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 7.2, "falhou": false} |
| 701 | 6 | acao | programa | ao_vivo | 2026-11-01T14:35:06 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 6.5, "falhou": false} |
| 703 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T14:35:06 | GET /api/produtos 200 |
| 704 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T14:35:06 | conferencia_do_roteiro: confere |
| 705 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T14:35:06 | conferencia_do_roteiro: confere |
| 706 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T14:35:06 | conferencia_do_roteiro: confere |
| 707 | 11 | poda | programa | ao_vivo | 2026-11-01T14:35:06 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 709 | 12 | poda | programa | ao_vivo | 2026-11-01T14:35:06 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 710 | 13 | candidatos | programa | ao_vivo | 2026-11-01T14:35:06 | 3 de 40 verbetes entregues |
| 712 | 14 | prompt | programa | ao_vivo | 2026-11-01T14:35:06 | {"etapa": "diagnostico", "sha": "c81b6a0264c76ce5", "prompt_sha256": "c81b6a0264c7", "chars": 6104, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 714 | 15 | inferencia | programa | ao_vivo | 2026-11-01T14:35:06 | diagnostico: 78,9 s |
| 715 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T14:35:06 | causa_raiz: `formato_de_data_divergente` |
| 716 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T14:35:06 | campo: `nenhum` |
| 717 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T14:35:06 | impacto: `A interface exibe preços com acentos faltando, causando uma leitura incorreta dos preços.` |
| 718 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T14:35:06 | fonte: `[entidade-produto], [contrato-produto]` |
| 719 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T14:35:06 | fonte_citada: `entidade-produto` |
| 720 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T14:35:06 | fonte_citada: `contrato-produto` |
| 721 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T14:35:06 | quatro_linhas_presentes: confere |
| 722 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T14:35:06 | rotulo_no_conjunto: confere |
| 723 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T14:35:06 | fonte_existe_na_biblioteca: confere |
| 724 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T14:35:06 | fonte_existe_na_biblioteca: confere |
| 725 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T14:35:06 | fonte_estava_no_contexto: confere |
| 726 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T14:35:06 | fonte_estava_no_contexto: confere |
| 727 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T14:35:06 | campo_existe_no_caso: nao_se_aplica |
| 728 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T14:35:06 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 729 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T14:35:06 | notas_nos_verbetes_citados: informativo |
| 730 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T14:35:06 | impacto: nao_verificavel |
| 731 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T14:35:06 | fonte_formato_valido: confere |
| 732 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T14:35:06 | fonte_contem_termo_da_causa: nao_confere |
| 733 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T14:35:06 | fonte_contem_termo_da_causa: nao_confere |
| 734 | 35 | decisao | programa | ao_vivo | 2026-11-01T14:35:06 | diagnostico: escolha formato_de_data_divergente; divergência sim |

</details>

Nós de decisão:

- evento 734, `diagnostico`: escolha `formato_de_data_divergente`; resultado rotulo_emitido; evidência: evento 709 (sinal_em_codigo), evento 707 (arvore_podada), evento 703 (corpo_http), evento 710 (verbete_entregue, entidade-produto), evento 710 (verbete_entregue, contrato-produto), evento 710 (verbete_entregue, contagem_inconsistente), evento 714 (resposta), evento 719 (verbete_citado, entidade-produto), evento 720 (verbete_citado, contrato-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, contagem_inconsistente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 696 a 734 da trilha; hash dos eventos deste caso: `809e0588545eb9dc`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
