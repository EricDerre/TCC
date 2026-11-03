<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-4`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/lex-4@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nome` · selo de probabilidade: **medio** (p = 0,89) · **CONFLITO**: nenhum verbete entregue trata da causa respondida codificacao_incorreta

**IMPACTO (declarado):** `O usuário vê nomes com caracteres codificados incorretamente na tela, como "Ãgua Mineral" em vez de "Água Mineral".`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta no campo nome porque o sinal nome: esperado "Água Mineral" (referência em modo normal), recebido "Ãgua Mineral" em 3 itens está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, contagem_inconsistente estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,03 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Poda de `arvore` (evento 87): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 45}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 1 linha(s) da referência | 7 linha(s) novas |

Trecho podado (hash `3c6d65355ee53010`):

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
    text "Ã\x81gua Mineral"
    text "Bebidas"
    text "Garrafa 500ml, com ou sem gás"
    text "destaque: Não"
    button "R$ 6,00" class="btn btn-default disable"
    button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="8"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 89): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2071}, depois {"chars": 410}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| nome | "Água Mineral" (referência em modo normal) | "Ãgua Mineral" em 3 itens |

Trecho podado (hash `ad8faa3b1aebfc8f`):

```text
lista com 14 itens (referência em modo normal: 14); nome diferente em 3 itens; por exemplo: {"id": 8, "nome": "Ãgua Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}; {"id": 11, "nome": "PÃ£o de Alho", "resumo": "Pão de alho grelhado na brasa", "tipo": "Acompanhamentos", "preco": 16.9, "imagem": "paodealho.png", "destaque": false}
```

Interceptação (evento 82): `GET /api/produtos` status 200; corpo `0fd45da79aa14f8a`, árvore `None`.

## 3. Contraste com a segunda causa

codificacao_incorreta e não formato_de_data_divergente: a escolha tem probabilidade 0,89 contra 0,03; verbete(s) na evidência: entidade-produto, contrato-produto, contagem_inconsistente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 0,89 | sim |
| formato_de_data_divergente | 0,03 |  |
| campo_ausente | 0,02 |  |
| campo_renomeado | 0,02 |  |
| valor_fora_do_dominio | 0,02 |  |
| tipo_divergente | 0,02 |  |
| resposta_truncada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| contagem_inconsistente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| nulo_inesperado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[entidade-produto], [contrato-produto]` | confere | {"ids": ["entidade-produto", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "codificacao_incorreta"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids lex-4 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 75 | 1 | entrada | programa | ao_vivo | 2026-11-01T14:09:53 | caso lex-4 |
| 76 | 2 | acao | programa | ao_vivo | 2026-11-01T14:09:53 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 115.0, "falhou": false} |
| 77 | 3 | acao | programa | ao_vivo | 2026-11-01T14:09:53 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 7.6, "falhou": false} |
| 78 | 4 | acao | programa | ao_vivo | 2026-11-01T14:09:53 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.5, "falhou": false} |
| 79 | 5 | acao | programa | ao_vivo | 2026-11-01T14:09:53 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 6.8, "falhou": false} |
| 80 | 6 | acao | programa | ao_vivo | 2026-11-01T14:09:53 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.3, "falhou": false} |
| 82 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T14:09:53 | GET /api/produtos 200 |
| 83 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T14:09:53 | conferencia_do_roteiro: confere |
| 84 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T14:09:53 | conferencia_do_roteiro: confere |
| 85 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T14:09:53 | conferencia_do_roteiro: confere |
| 87 | 11 | poda | programa | ao_vivo | 2026-11-01T14:09:53 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 89 | 12 | poda | programa | ao_vivo | 2026-11-01T14:09:53 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 90 | 13 | candidatos | programa | ao_vivo | 2026-11-01T14:09:53 | 3 de 40 verbetes entregues |
| 92 | 14 | prompt | programa | ao_vivo | 2026-11-01T14:09:53 | {"etapa": "diagnostico", "sha": "b1a6bb02272e3b74", "prompt_sha256": "b1a6bb02272e", "chars": 6253, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 94 | 15 | inferencia | programa | ao_vivo | 2026-11-01T14:09:53 | diagnostico: 86,8 s |
| 95 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T14:09:53 | causa_raiz: `codificacao_incorreta` |
| 96 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T14:09:53 | campo: `nome` |
| 97 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T14:09:53 | impacto: `O usuário vê nomes com caracteres codificados incorretamente na tela, como "Ãgua Mineral" em vez de "Água Mineral".` |
| 98 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T14:09:53 | fonte: `[entidade-produto], [contrato-produto]` |
| 99 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T14:09:53 | fonte_citada: `entidade-produto` |
| 100 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T14:09:53 | fonte_citada: `contrato-produto` |
| 101 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T14:09:53 | quatro_linhas_presentes: confere |
| 102 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T14:09:53 | rotulo_no_conjunto: confere |
| 103 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T14:09:53 | fonte_existe_na_biblioteca: confere |
| 104 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T14:09:53 | fonte_existe_na_biblioteca: confere |
| 105 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T14:09:53 | fonte_estava_no_contexto: confere |
| 106 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T14:09:53 | fonte_estava_no_contexto: confere |
| 107 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T14:09:53 | campo_existe_no_caso: confere |
| 108 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T14:09:53 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 109 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T14:09:53 | notas_nos_verbetes_citados: informativo |
| 110 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T14:09:53 | impacto: nao_verificavel |
| 111 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T14:09:53 | fonte_formato_valido: confere |
| 112 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T14:09:53 | fonte_contem_termo_da_causa: nao_confere |
| 113 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T14:09:53 | fonte_contem_termo_da_causa: nao_confere |
| 114 | 35 | decisao | programa | ao_vivo | 2026-11-01T14:09:53 | diagnostico: escolha codificacao_incorreta; divergência sim |

</details>

Nós de decisão:

- evento 114, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 89 (sinal_em_codigo), evento 87 (arvore_podada), evento 82 (corpo_http), evento 90 (verbete_entregue, entidade-produto), evento 90 (verbete_entregue, contrato-produto), evento 90 (verbete_entregue, contagem_inconsistente), evento 94 (resposta), evento 99 (verbete_citado, entidade-produto), evento 100 (verbete_citado, contrato-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, contagem_inconsistente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 75 a 114 da trilha; hash dos eventos deste caso: `5aabe3d7ddb1f0ef`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
