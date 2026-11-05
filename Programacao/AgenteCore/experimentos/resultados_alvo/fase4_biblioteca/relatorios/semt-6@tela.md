<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-6`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/semt-6@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `contagem_inconsistente` · **CAMPO:** `id` · selo de probabilidade: **medio** (p = 0,86)

**IMPACTO (declarado):** `O usuário vê um produto com um id inválido, o que pode causar confusão e problemas na navegação entre os itens.`

Justificativa (gerada por molde): O agente respondeu contagem_inconsistente no campo id porque o sinal id: esperado inteiro, recebido texto está presente na resposta HTTP e os verbetes entidade-produto, campo_ausente, contagem_inconsistente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,10. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 1 edição(ões) aplicada(s) ([tipo_divergente]), 0 para revisão humana, 1 recusada(s) (palavra_chave_invalida).

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso semt-6. A proposta 1 (nota em [tipo_divergente], peso 1) passou pela validação da Fase 3 e pelos filtros e entrou no lote. A proposta 2 (retificacao em [contagem_inconsistente]) foi recusada por a validação da Fase 3 com o código palavra_chave_invalida: item de lista inválido: 'total e lista vem de consultas diferentes'.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `tipo_divergente` | aceita | nenhum | **aplicada** | 1 |
| 2 | retificacao | `contagem_inconsistente` | recusada: `palavra_chave_invalida` | nenhum | recusada: `palavra_chave_invalida` |  |

Poda de `arvore` (evento 904): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 906): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2096}, depois {"chars": 11}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | inteiro | texto |
| itens | 14 itens (referência em modo normal) | faltam os ids 1 ("Picanha ao Alho"), 2 ("Picanha Simples"), 3 ("Fraldinha"), 4 ("Costelona"), 5 ("Alcatra na Pedra"), 6 ("Maminha"), 7 ("Cupim"), 8 ("Água Mineral"), 9 ("Balde de Cerveja"), 10 ("Refrigerante"), 11 ("Pão de Alho"), 12 ("Queijo Coalho"), 13 ("Hambúrguer Artesanal"), 14 ("Abacaxi na Brasa") |
| itens | 14 itens (referência em modo normal) | sobram os ids 1 ("Picanha ao Alho"), 2 ("Picanha Simples"), 3 ("Fraldinha"), 4 ("Costelona"), 5 ("Alcatra na Pedra"), 6 ("Maminha"), 7 ("Cupim"), 8 ("Água Mineral"), 9 ("Balde de Cerveja"), 10 ("Refrigerante"), 11 ("Pão de Alho"), 12 ("Queijo Coalho"), 13 ("Hambúrguer Artesanal"), 14 ("Abacaxi na Brasa") |

Trecho podado (hash `51fedabde565f471`):

```text
{"id": "1"}
```

Interceptação (evento 900): `GET /api/produtos` status 200; corpo `0547c845702b985e`, árvore `None`.

## 3. Contraste com a segunda causa

contagem_inconsistente e não campo_ausente: a escolha tem probabilidade 0,86 contra 0,10; verbete(s) na evidência: entidade-produto, campo_ausente, contagem_inconsistente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| contagem_inconsistente | 0,86 | sim |
| campo_ausente | 0,10 |  |
| campo_renomeado | 0,10 |  |
| corpo_nao_e_json | 0,02 |  |
| corpo_vazio | 0,02 |  |
| resposta_truncada | 0,01 |  |
| tipo_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente] [contagem_inconsistente]`; verbetes citados: `campo_ausente`, `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `entidade-produto`, `campo_ausente`, `contagem_inconsistente` |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `entidade-produto`, `campo_ausente`, `contagem_inconsistente` |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | confere | verbetes: `contagem_inconsistente` |
| fonte_formato_valido | `[campo_ausente] [contagem_inconsistente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["campo_ausente", "contagem_inconsistente"]} |
| fonte_contem_termo_da_causa | `campo_ausente` | **não confere** | {"termo": "contagem_inconsistente"} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | confere | {"termo": "contagem_inconsistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>39 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 893 | 1 | entrada | programa | ao_vivo | 2026-11-03T22:35:41 | caso semt-6 |
| 894 | 2 | acao | programa | ao_vivo | 2026-11-03T22:35:41 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 179.6, "url": "produtos_api.php"} |
| 895 | 3 | acao | programa | ao_vivo | 2026-11-03T22:35:41 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 6.2, "url": null} |
| 896 | 4 | acao | programa | ao_vivo | 2026-11-03T22:35:41 | {"acao": "conferir", "falhou": false, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 1.9, "url": null} |
| 897 | 5 | acao | programa | ao_vivo | 2026-11-03T22:35:41 | {"acao": "conferir", "falhou": false, "passo": 4, "seletor": "#produtos-api-grid .thumbnail .btn-default", "tempo_ms": 4.0, "url": null} |
| 898 | 6 | acao | programa | ao_vivo | 2026-11-03T22:35:41 | {"acao": "conferir", "falhou": false, "passo": 5, "seletor": "#produtos-api-status", "tempo_ms": 2.8, "url": null} |
| 900 | 7 | interceptacao | programa | ao_vivo | 2026-11-03T22:35:41 | GET /api/produtos 200 |
| 901 | 8 | verificacao | verificacao | ao_vivo | 2026-11-03T22:35:41 | conferencia_do_roteiro: confere |
| 902 | 9 | verificacao | verificacao | ao_vivo | 2026-11-03T22:35:41 | conferencia_do_roteiro: confere |
| 903 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T22:35:41 | conferencia_do_roteiro: confere |
| 904 | 11 | poda | programa | ao_vivo | 2026-11-03T22:35:41 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 906 | 12 | poda | programa | ao_vivo | 2026-11-03T22:35:41 | corpo_http: 3 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 907 | 13 | candidatos | programa | ao_vivo | 2026-11-03T22:35:41 | 3 de 40 verbetes entregues |
| 909 | 14 | prompt | programa | ao_vivo | 2026-11-03T22:35:41 | {"chars": 5776, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "577ab9aa120a", "sha": "577ab9aa120ac77e"} |
| 911 | 15 | inferencia | programa | ao_vivo | 2026-11-03T22:35:41 | diagnostico: 103,0 s |
| 912 | 16 | declaracao | modelo | ao_vivo | 2026-11-03T22:35:41 | causa_raiz: `contagem_inconsistente` |
| 913 | 17 | declaracao | modelo | ao_vivo | 2026-11-03T22:35:41 | campo: `id` |
| 914 | 18 | declaracao | modelo | ao_vivo | 2026-11-03T22:35:41 | impacto: `O usuário vê um produto com um id inválido, o que pode causar confusão e problemas na navegação entre os itens.` |
| 915 | 19 | declaracao | modelo | ao_vivo | 2026-11-03T22:35:41 | fonte: `[campo_ausente] [contagem_inconsistente]` |
| 916 | 20 | declaracao | modelo | ao_vivo | 2026-11-03T22:35:41 | fonte_citada: `campo_ausente` |
| 917 | 21 | declaracao | modelo | ao_vivo | 2026-11-03T22:35:41 | fonte_citada: `contagem_inconsistente` |
| 918 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T22:35:41 | quatro_linhas_presentes: confere |
| 919 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T22:35:41 | rotulo_no_conjunto: confere |
| 920 | 24 | verificacao | verificacao | ao_vivo | 2026-11-03T22:35:41 | fonte_existe_na_biblioteca: confere |
| 921 | 25 | verificacao | verificacao | ao_vivo | 2026-11-03T22:35:41 | fonte_existe_na_biblioteca: confere |
| 922 | 26 | verificacao | verificacao | ao_vivo | 2026-11-03T22:35:41 | fonte_estava_no_contexto: confere |
| 923 | 27 | verificacao | verificacao | ao_vivo | 2026-11-03T22:35:41 | fonte_estava_no_contexto: confere |
| 924 | 28 | verificacao | verificacao | ao_vivo | 2026-11-03T22:35:41 | campo_existe_no_caso: confere |
| 925 | 29 | verificacao | verificacao | ao_vivo | 2026-11-03T22:35:41 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 926 | 30 | verificacao | verificacao | ao_vivo | 2026-11-03T22:35:41 | notas_nos_verbetes_citados: informativo |
| 927 | 31 | verificacao | verificacao | ao_vivo | 2026-11-03T22:35:41 | impacto: nao_verificavel |
| 928 | 32 | verificacao | verificacao | ao_vivo | 2026-11-03T22:35:41 | fonte_formato_valido: confere |
| 929 | 33 | verificacao | verificacao | ao_vivo | 2026-11-03T22:35:41 | fonte_contem_termo_da_causa: nao_confere |
| 930 | 34 | verificacao | verificacao | ao_vivo | 2026-11-03T22:35:41 | fonte_contem_termo_da_causa: confere |
| 931 | 35 | decisao | programa | ao_vivo | 2026-11-03T22:35:41 | diagnostico: escolha contagem_inconsistente; divergência não |
| 934 | 36 | inferencia | programa | ao_vivo | 2026-11-03T22:37:28 | proposta: 154,9 s |
| 936 | 37 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:37:28 | proposta 1: nota em [tipo_divergente]: aplicada |
| 938 | 38 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:37:28 | proposta 2: retificacao em [contagem_inconsistente]: recusada: palavra_chave_invalida |
| 939 | 39 | decisao | programa | ao_vivo | 2026-11-03T22:37:28 | edicao_biblioteca: escolha proposta_1; divergência sim |

</details>

Nós de decisão:

- evento 931, `diagnostico`: escolha `contagem_inconsistente`; resultado rotulo_emitido; evidência: evento 906 (sinal_em_codigo), evento 904 (arvore_podada), evento 900 (corpo_http), evento 907 (verbete_entregue, entidade-produto), evento 907 (verbete_entregue, campo_ausente), evento 907 (verbete_entregue, contagem_inconsistente), evento 911 (resposta), evento 916 (verbete_citado, campo_ausente), evento 917 (verbete_citado, contagem_inconsistente); divergência: não; falha: nenhuma; prov.used: entidade-produto, campo_ausente, contagem_inconsistente (gen_ai: chat)
- evento 939, `edicao_biblioteca`: escolha `proposta_1`; resultado lote; evidência: evento 906 (sinal_em_codigo), evento 904 (arvore_podada), evento 900 (corpo_http), evento 911 (resposta), evento 934 (resposta), evento 936 (verbete_entregue, tipo_divergente), evento 938 (verbete_entregue, contagem_inconsistente); divergência: sim; falha: nenhuma; prov.used: campo_ausente, contagem_inconsistente, entidade-produto, tipo_divergente

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 893 a 939 da trilha; hash dos eventos deste caso: `052faa6d80cb9f82`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
