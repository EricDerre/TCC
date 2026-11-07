<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-27`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/semt-27@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `contagem_inconsistente` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,98)

**IMPACTO (declarado):** `A interface exibe um número incorreto de produtos, faltando alguns e incluindo itens com IDs negativos.`

Justificativa (gerada por molde): O agente respondeu contagem_inconsistente no campo itens porque o sinal itens: esperado 14 itens (referência em modo normal), recebido faltam os ids 1 ("Picanha ao Alho"), 2 ("Picanha Simples"), 3 ("Fraldinha"), 4 ("Costelona"), 5 ("Alcatra na Pedra"), 6 ("Maminha"), 7 ("Cupim"), 8 ("Água Mineral"), 9 ("Balde de Cerveja"), 10 ("Refrigerante"), 11 ("Pão de Alho"), 12 ("Queijo Coalho"), 13 ("Hambúrguer Artesanal"), 14 ("Abacaxi na Brasa") está presente na resposta HTTP e os verbetes contagem_inconsistente, estrutura_aninhada_divergente, entidade-produto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,01 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1002): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `e24dccf249767e45`):

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
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="-2"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="-3"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "R$ 69,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="-4"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 1004): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2083}, depois {"chars": 871}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| itens | 14 itens (referência em modo normal) | faltam os ids 1 ("Picanha ao Alho"), 2 ("Picanha Simples"), 3 ("Fraldinha"), 4 ("Costelona"), 5 ("Alcatra na Pedra"), 6 ("Maminha"), 7 ("Cupim"), 8 ("Água Mineral"), 9 ("Balde de Cerveja"), 10 ("Refrigerante"), 11 ("Pão de Alho"), 12 ("Queijo Coalho"), 13 ("Hambúrguer Artesanal"), 14 ("Abacaxi na Brasa") |
| itens | 14 itens (referência em modo normal) | sobram os ids -2 ("Picanha ao Alho"), -3 ("Picanha Simples"), -4 ("Fraldinha"), -5 ("Costelona"), -6 ("Alcatra na Pedra"), -7 ("Maminha"), -8 ("Cupim"), -9 ("Água Mineral"), -10 ("Balde de Cerveja"), -11 ("Refrigerante"), -12 ("Pão de Alho"), -13 ("Queijo Coalho"), -14 ("Hambúrguer Artesanal"), -15 ("Abacaxi na Brasa") |

Trecho podado (hash `60c20051a86e36ef`):

```text
lista com 14 itens (referência em modo normal: 14); faltam os ids 1 ("Picanha ao Alho"), 2 ("Picanha Simples"), 3 ("Fraldinha"), 4 ("Costelona"), 5 ("Alcatra na Pedra"), 6 ("Maminha"), 7 ("Cupim"), 8 ("Água Mineral"), 9 ("Balde de Cerveja"), 10 ("Refrigerante"), 11 ("Pão de Alho"), 12 ("Queijo Coalho"), 13 ("Hambúrguer Artesanal"), 14 ("Abacaxi na Brasa"); sobram os ids -2 ("Picanha ao Alho"), -3 ("Picanha Simples"), -4 ("Fraldinha"), -5 ("Costelona"), -6 ("Alcatra na Pedra"), -7 ("Maminha"), -8 ("Cupim"), -9 ("Água Mineral"), -10 ("Balde de Cerveja"), -11 ("Refrigerante"), -12 ("Pão de Alho"), -13 ("Queijo Coalho"), -14 ("Hambúrguer Artesanal"), -15 ("Abacaxi na Brasa"); primeiro item: {"id": -2, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 997): `GET /api/produtos` status 200; corpo `53934a33092188b7`, árvore `None`.

## 3. Contraste com a segunda causa

contagem_inconsistente e não resposta_truncada: a escolha tem probabilidade 0,98 contra 0,01; verbete(s) na evidência: contagem_inconsistente, estrutura_aninhada_divergente, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| contagem_inconsistente | 0,98 | sim |
| resposta_truncada | 0,01 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| registro_duplicado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contagem_inconsistente]`; verbetes citados: `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `contagem_inconsistente`, `estrutura_aninhada_divergente`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | confere | verbetes: `contagem_inconsistente`, `estrutura_aninhada_divergente` |
| fonte_formato_valido | `[contagem_inconsistente]` | confere | {"ids": ["contagem_inconsistente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | confere | {"termo": "contagem_inconsistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids semt-27 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 990 | 1 | entrada | programa | ao_vivo | 2026-11-06T12:03:25 | caso semt-27 |
| 991 | 2 | acao | programa | ao_vivo | 2026-11-06T12:03:25 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 84.0, "falhou": false} |
| 992 | 3 | acao | programa | ao_vivo | 2026-11-06T12:03:25 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 7.2, "falhou": false} |
| 993 | 4 | acao | programa | ao_vivo | 2026-11-06T12:03:25 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.6, "falhou": false} |
| 994 | 5 | acao | programa | ao_vivo | 2026-11-06T12:03:25 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 5.6, "falhou": false} |
| 995 | 6 | acao | programa | ao_vivo | 2026-11-06T12:03:25 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.7, "falhou": false} |
| 997 | 7 | interceptacao | programa | ao_vivo | 2026-11-06T12:03:25 | GET /api/produtos 200 |
| 998 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T12:03:25 | conferencia_do_roteiro: confere |
| 999 | 9 | verificacao | verificacao | ao_vivo | 2026-11-06T12:03:25 | conferencia_do_roteiro: confere |
| 1000 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T12:03:25 | conferencia_do_roteiro: confere |
| 1002 | 11 | poda | programa | ao_vivo | 2026-11-06T12:03:25 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1004 | 12 | poda | programa | ao_vivo | 2026-11-06T12:03:25 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1005 | 13 | candidatos | programa | ao_vivo | 2026-11-06T12:03:25 | 3 de 39 verbetes entregues |
| 1007 | 14 | prompt | programa | ao_vivo | 2026-11-06T12:03:25 | {"etapa": "diagnostico", "sha": "b4f4b3e74998542a", "prompt_sha256": "b4f4b3e74998", "chars": 5320, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1009 | 15 | inferencia | programa | ao_vivo | 2026-11-06T12:03:25 | diagnostico: 109,9 s |
| 1010 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T12:03:25 | causa_raiz: `contagem_inconsistente` |
| 1011 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T12:03:25 | campo: `nenhum` |
| 1012 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T12:03:25 | impacto: `A interface exibe um número incorreto de produtos, faltando alguns e incluindo itens com IDs negativos.` |
| 1013 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T12:03:25 | fonte: `[contagem_inconsistente]` |
| 1014 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T12:03:25 | fonte_citada: `contagem_inconsistente` |
| 1015 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T12:03:25 | quatro_linhas_presentes: confere |
| 1016 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T12:03:25 | rotulo_no_conjunto: confere |
| 1017 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T12:03:25 | fonte_existe_na_biblioteca: confere |
| 1018 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T12:03:25 | fonte_estava_no_contexto: confere |
| 1019 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T12:03:25 | campo_existe_no_caso: nao_se_aplica |
| 1020 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T12:03:25 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1021 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T12:03:25 | notas_nos_verbetes_citados: informativo |
| 1022 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T12:03:25 | impacto: nao_verificavel |
| 1023 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T12:03:25 | fonte_formato_valido: confere |
| 1024 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T12:03:25 | fonte_contem_termo_da_causa: confere |
| 1025 | 31 | decisao | programa | ao_vivo | 2026-11-06T12:03:25 | diagnostico: escolha contagem_inconsistente; divergência não |

</details>

Nós de decisão:

- evento 1025, `diagnostico`: escolha `contagem_inconsistente`; resultado rotulo_emitido; evidência: evento 1004 (sinal_em_codigo), evento 1002 (arvore_podada), evento 997 (corpo_http), evento 1005 (verbete_entregue, contagem_inconsistente), evento 1005 (verbete_entregue, estrutura_aninhada_divergente), evento 1005 (verbete_entregue, entidade-produto), evento 1009 (resposta), evento 1014 (verbete_citado, contagem_inconsistente); divergência: não; falha: nenhuma; prov.used: contagem_inconsistente, estrutura_aninhada_divergente, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 990 a 1025 da trilha; hash dos eventos deste caso: `0d1ebc47d64c3e71`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
