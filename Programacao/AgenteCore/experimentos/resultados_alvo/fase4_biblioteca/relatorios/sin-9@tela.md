<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-9`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/sin-9@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_renomeado` · **CAMPO:** `nome` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê o nome do produto como "nome_v2" em vez de "nome", o que causa confusão na exibição dos dados.`

Justificativa (gerada por molde): O agente respondeu campo_renomeado no campo nome porque o sinal nome: esperado nome, recebido nome_v2 está presente na resposta HTTP e os verbetes entidade-produto, estrutura_aninhada_divergente, contagem_inconsistente, campo_renomeado estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 2 recusada(s) (sem_evidencia_do_caso, id_repetido) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso sin-9. A proposta 1 (nota em [campo_renomeado]) foi recusada por o filtro evidencia_obrigatoria com o código sem_evidencia_do_caso: o MOTIVO não cita nenhum termo da evidência do caso (campo, status, rota, sintoma, chaves do corpo). A proposta 2 (novo_verbete em [estrutura_aninhada_divergente]) foi recusada por a validação da Fase 3 com o código id_repetido: 'estrutura_aninhada_divergente' já é id de verbete ou nome de causa raiz.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `campo_renomeado` | aceita | evidencia_obrigatoria | recusada: `sem_evidencia_do_caso` | 1 |
| 2 | novo_verbete | `estrutura_aninhada_divergente` | recusada: `id_repetido` | nenhum | recusada: `id_repetido` |  |

Poda de `arvore` (evento 752): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `a59adb210fd17df3`):

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
      heading "(sem nome)" level=3
      text "Carnes"
      text "Picanha grelhada com alho laminado na brasa"
      text "destaque: Sim"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "(sem nome)" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "(sem nome)" level=3
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

Poda de `corpo_http` (evento 754): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2110}, depois {"chars": 30}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| nome | nome | nome_v2 |

Trecho podado (hash `37a4002087f7821c`):

```text
{"nome_v2": "Picanha ao Alho"}
```

Interceptação (evento 748): `GET /api/produtos` status 200; corpo `42d1837cbc1f6390`, árvore `None`.

## 3. Contraste com a segunda causa

campo_renomeado e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, estrutura_aninhada_divergente, contagem_inconsistente, campo_renomeado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_renomeado | 1,00 | sim |
| campo_ausente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_renomeado]`; verbetes citados: `campo_renomeado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | confere | contexto: `entidade-produto`, `estrutura_aninhada_divergente`, `contagem_inconsistente`, `campo_renomeado` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `estrutura_aninhada_divergente`, `campo_renomeado` |
| fonte_formato_valido | `[campo_renomeado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["campo_renomeado"]} |
| fonte_contem_termo_da_causa | `campo_renomeado` | confere | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 741 | 1 | entrada | programa | ao_vivo | 2026-11-03T22:19:46 | caso sin-9 |
| 742 | 2 | acao | programa | ao_vivo | 2026-11-03T22:19:46 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 179.6, "url": "produtos_api.php"} |
| 743 | 3 | acao | programa | ao_vivo | 2026-11-03T22:19:46 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 5.8, "url": null} |
| 744 | 4 | acao | programa | ao_vivo | 2026-11-03T22:19:46 | {"acao": "conferir", "falhou": false, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 1.8, "url": null} |
| 745 | 5 | acao | programa | ao_vivo | 2026-11-03T22:19:46 | {"acao": "conferir", "falhou": false, "passo": 4, "seletor": "#produtos-api-grid .thumbnail .btn-default", "tempo_ms": 3.6, "url": null} |
| 746 | 6 | acao | programa | ao_vivo | 2026-11-03T22:19:46 | {"acao": "conferir", "falhou": false, "passo": 5, "seletor": "#produtos-api-status", "tempo_ms": 3.0, "url": null} |
| 748 | 7 | interceptacao | programa | ao_vivo | 2026-11-03T22:19:46 | GET /api/produtos 200 |
| 749 | 8 | verificacao | verificacao | ao_vivo | 2026-11-03T22:19:46 | conferencia_do_roteiro: confere |
| 750 | 9 | verificacao | verificacao | ao_vivo | 2026-11-03T22:19:46 | conferencia_do_roteiro: confere |
| 751 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T22:19:46 | conferencia_do_roteiro: confere |
| 752 | 11 | poda | programa | ao_vivo | 2026-11-03T22:19:46 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 754 | 12 | poda | programa | ao_vivo | 2026-11-03T22:19:46 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 755 | 13 | candidatos | programa | ao_vivo | 2026-11-03T22:19:46 | 3 de 40 verbetes entregues |
| 757 | 14 | prompt | programa | ao_vivo | 2026-11-03T22:19:46 | {"chars": 6302, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "3be3fd14db64", "sha": "3be3fd14db64bd42"} |
| 759 | 15 | inferencia | programa | ao_vivo | 2026-11-03T22:19:46 | diagnostico: 105,5 s |
| 760 | 16 | declaracao | modelo | ao_vivo | 2026-11-03T22:19:46 | causa_raiz: `campo_renomeado` |
| 761 | 17 | declaracao | modelo | ao_vivo | 2026-11-03T22:19:46 | campo: `nome` |
| 762 | 18 | declaracao | modelo | ao_vivo | 2026-11-03T22:19:46 | impacto: `O usuário vê o nome do produto como "nome_v2" em vez de "nome", o que causa confusão na exibição dos dados.` |
| 763 | 19 | declaracao | modelo | ao_vivo | 2026-11-03T22:19:46 | fonte: `[campo_renomeado]` |
| 764 | 20 | declaracao | modelo | ao_vivo | 2026-11-03T22:19:46 | fonte_citada: `campo_renomeado` |
| 765 | 21 | verificacao | verificacao | ao_vivo | 2026-11-03T22:19:46 | quatro_linhas_presentes: confere |
| 766 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T22:19:46 | rotulo_no_conjunto: confere |
| 767 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T22:19:46 | fonte_existe_na_biblioteca: confere |
| 768 | 24 | verificacao | verificacao | ao_vivo | 2026-11-03T22:19:46 | fonte_estava_no_contexto: confere |
| 769 | 25 | verificacao | verificacao | ao_vivo | 2026-11-03T22:19:46 | campo_existe_no_caso: confere |
| 770 | 26 | verificacao | verificacao | ao_vivo | 2026-11-03T22:19:46 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 771 | 27 | verificacao | verificacao | ao_vivo | 2026-11-03T22:19:46 | notas_nos_verbetes_citados: informativo |
| 772 | 28 | verificacao | verificacao | ao_vivo | 2026-11-03T22:19:46 | impacto: nao_verificavel |
| 773 | 29 | verificacao | verificacao | ao_vivo | 2026-11-03T22:19:46 | fonte_formato_valido: confere |
| 774 | 30 | verificacao | verificacao | ao_vivo | 2026-11-03T22:19:46 | fonte_contem_termo_da_causa: confere |
| 775 | 31 | decisao | programa | ao_vivo | 2026-11-03T22:19:46 | diagnostico: escolha campo_renomeado; divergência não |
| 778 | 32 | inferencia | programa | ao_vivo | 2026-11-03T22:21:36 | proposta: 138,3 s |
| 779 | 33 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:21:36 | proposta 1: nota em [campo_renomeado]: recusada: sem_evidencia_do_caso |
| 780 | 34 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:21:36 | proposta 2: novo_verbete em [estrutura_aninhada_divergente]: recusada: id_repetido |
| 781 | 35 | decisao | programa | ao_vivo | 2026-11-03T22:21:36 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 775, `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido; evidência: evento 754 (sinal_em_codigo), evento 752 (arvore_podada), evento 748 (corpo_http), evento 755 (verbete_entregue, entidade-produto), evento 755 (verbete_entregue, estrutura_aninhada_divergente), evento 755 (verbete_entregue, contagem_inconsistente), evento 755 (verbete_entregue, campo_renomeado), evento 759 (resposta), evento 764 (verbete_citado, campo_renomeado); divergência: não; falha: nenhuma; prov.used: entidade-produto, estrutura_aninhada_divergente, contagem_inconsistente, campo_renomeado (gen_ai: chat)
- evento 781, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 754 (sinal_em_codigo), evento 752 (arvore_podada), evento 748 (corpo_http), evento 759 (resposta), evento 778 (resposta), evento 779 (verbete_entregue, campo_renomeado), evento 780 (verbete_entregue, estrutura_aninhada_divergente); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: campo_renomeado, contagem_inconsistente, entidade-produto, estrutura_aninhada_divergente

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 741 a 781 da trilha; hash dos eventos deste caso: `f7d5f997286bf238`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
