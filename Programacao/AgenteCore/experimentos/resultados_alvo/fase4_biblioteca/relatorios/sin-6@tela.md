<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-6`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/sin-6@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `nome` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário não vê o nome do produto na tela, o que pode causar confusão e dificuldade na identificação dos itens.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo nome porque o sinal nome: esperado texto, recebido None está presente na resposta HTTP e os verbetes campo_ausente, contrato-produto, entidade-produto estavam entre os entregues ao modelo. A segunda causa, corpo_nao_e_json, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 2 recusada(s) (palavra_chave_invalida, id_repetido) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso sin-6. A proposta 1 (nota em [campo_ausente]) foi recusada por a validação da Fase 3 com o código palavra_chave_invalida: item de lista inválido: 'botao imprime "undefined"'. A proposta 2 (novo_verbete em [campo_renomeado]) foi recusada por a validação da Fase 3 com o código id_repetido: 'campo_renomeado' já é id de verbete ou nome de causa raiz.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `campo_ausente` | recusada: `palavra_chave_invalida` | nenhum | recusada: `palavra_chave_invalida` |  |
| 2 | novo_verbete | `campo_renomeado` | recusada: `id_repetido` | nenhum | recusada: `id_repetido` |  |

Poda de `arvore` (evento 669): regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 671): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 1752}, depois {"chars": 21}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| nome | texto |  |

Trecho podado (hash `5406a4e0bdccaf7e`):

```text
{"nome": "(ausente)"}
```

Interceptação (evento 664): `GET /api/produtos` status 200; corpo `5e634a53e6e1c806`, árvore `None`.

## 3. Contraste com a segunda causa

campo_ausente e não corpo_nao_e_json: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: campo_ausente, contrato-produto, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 1,00 | sim |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| campo_renomeado | 0,00 |  |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente], [contrato-produto]`; verbetes citados: `campo_ausente`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `campo_ausente`, `contrato-produto`, `entidade-produto` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `campo_ausente`, `contrato-produto`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `campo_ausente`, `contrato-produto` |
| fonte_formato_valido | `[campo_ausente], [contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["campo_ausente", "contrato-produto"]} |
| fonte_contem_termo_da_causa | `campo_ausente` | confere | {"termo": "campo_ausente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>39 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 657 | 1 | entrada | programa | ao_vivo | 2026-11-03T22:11:27 | caso sin-6 |
| 658 | 2 | acao | programa | ao_vivo | 2026-11-03T22:11:27 | {"acao": "abrir", "falhou": false, "passo": 1, "seletor": null, "tempo_ms": 106.7, "url": "produtos_api.php"} |
| 659 | 3 | acao | programa | ao_vivo | 2026-11-03T22:11:27 | {"acao": "esperar", "falhou": false, "passo": 2, "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "tempo_ms": 12.8, "url": null} |
| 660 | 4 | acao | programa | ao_vivo | 2026-11-03T22:11:27 | {"acao": "conferir", "falhou": false, "passo": 3, "seletor": "#produtos-api-grid .saiba-mais", "tempo_ms": 2.9, "url": null} |
| 661 | 5 | acao | programa | ao_vivo | 2026-11-03T22:11:27 | {"acao": "conferir", "falhou": false, "passo": 4, "seletor": "#produtos-api-grid .thumbnail .btn-default", "tempo_ms": 3.9, "url": null} |
| 662 | 6 | acao | programa | ao_vivo | 2026-11-03T22:11:27 | {"acao": "conferir", "falhou": false, "passo": 5, "seletor": "#produtos-api-status", "tempo_ms": 4.1, "url": null} |
| 664 | 7 | interceptacao | programa | ao_vivo | 2026-11-03T22:11:27 | GET /api/produtos 200 |
| 665 | 8 | verificacao | verificacao | ao_vivo | 2026-11-03T22:11:27 | conferencia_do_roteiro: confere |
| 666 | 9 | verificacao | verificacao | ao_vivo | 2026-11-03T22:11:27 | conferencia_do_roteiro: confere |
| 667 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T22:11:27 | conferencia_do_roteiro: confere |
| 669 | 11 | poda | programa | ao_vivo | 2026-11-03T22:11:27 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 671 | 12 | poda | programa | ao_vivo | 2026-11-03T22:11:27 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 672 | 13 | candidatos | programa | ao_vivo | 2026-11-03T22:11:27 | 3 de 40 verbetes entregues |
| 674 | 14 | prompt | programa | ao_vivo | 2026-11-03T22:11:27 | {"chars": 5541, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "49c29558fb29", "sha": "49c29558fb29960d"} |
| 676 | 15 | inferencia | programa | ao_vivo | 2026-11-03T22:11:27 | diagnostico: 105,0 s |
| 677 | 16 | declaracao | modelo | ao_vivo | 2026-11-03T22:11:27 | causa_raiz: `campo_ausente` |
| 678 | 17 | declaracao | modelo | ao_vivo | 2026-11-03T22:11:27 | campo: `nome` |
| 679 | 18 | declaracao | modelo | ao_vivo | 2026-11-03T22:11:27 | impacto: `O usuário não vê o nome do produto na tela, o que pode causar confusão e dificuldade na identificação dos itens.` |
| 680 | 19 | declaracao | modelo | ao_vivo | 2026-11-03T22:11:27 | fonte: `[campo_ausente], [contrato-produto]` |
| 681 | 20 | declaracao | modelo | ao_vivo | 2026-11-03T22:11:27 | fonte_citada: `campo_ausente` |
| 682 | 21 | declaracao | modelo | ao_vivo | 2026-11-03T22:11:27 | fonte_citada: `contrato-produto` |
| 683 | 22 | verificacao | verificacao | ao_vivo | 2026-11-03T22:11:27 | quatro_linhas_presentes: confere |
| 684 | 23 | verificacao | verificacao | ao_vivo | 2026-11-03T22:11:27 | rotulo_no_conjunto: confere |
| 685 | 24 | verificacao | verificacao | ao_vivo | 2026-11-03T22:11:27 | fonte_existe_na_biblioteca: confere |
| 686 | 25 | verificacao | verificacao | ao_vivo | 2026-11-03T22:11:27 | fonte_existe_na_biblioteca: confere |
| 687 | 26 | verificacao | verificacao | ao_vivo | 2026-11-03T22:11:27 | fonte_estava_no_contexto: confere |
| 688 | 27 | verificacao | verificacao | ao_vivo | 2026-11-03T22:11:27 | fonte_estava_no_contexto: confere |
| 689 | 28 | verificacao | verificacao | ao_vivo | 2026-11-03T22:11:27 | campo_existe_no_caso: confere |
| 690 | 29 | verificacao | verificacao | ao_vivo | 2026-11-03T22:11:27 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 691 | 30 | verificacao | verificacao | ao_vivo | 2026-11-03T22:11:27 | notas_nos_verbetes_citados: informativo |
| 692 | 31 | verificacao | verificacao | ao_vivo | 2026-11-03T22:11:27 | impacto: nao_verificavel |
| 693 | 32 | verificacao | verificacao | ao_vivo | 2026-11-03T22:11:27 | fonte_formato_valido: confere |
| 694 | 33 | verificacao | verificacao | ao_vivo | 2026-11-03T22:11:27 | fonte_contem_termo_da_causa: confere |
| 695 | 34 | verificacao | verificacao | ao_vivo | 2026-11-03T22:11:27 | fonte_contem_termo_da_causa: nao_confere |
| 696 | 35 | decisao | programa | ao_vivo | 2026-11-03T22:11:27 | diagnostico: escolha campo_ausente; divergência não |
| 699 | 36 | inferencia | programa | ao_vivo | 2026-11-03T22:13:16 | proposta: 141,6 s |
| 701 | 37 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:13:16 | proposta 1: nota em [campo_ausente]: recusada: palavra_chave_invalida |
| 703 | 38 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T22:13:16 | proposta 2: novo_verbete em [campo_renomeado]: recusada: id_repetido |
| 704 | 39 | decisao | programa | ao_vivo | 2026-11-03T22:13:16 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 696, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 671 (sinal_em_codigo), evento 669 (arvore_podada), evento 664 (corpo_http), evento 672 (verbete_entregue, campo_ausente), evento 672 (verbete_entregue, contrato-produto), evento 672 (verbete_entregue, entidade-produto), evento 676 (resposta), evento 681 (verbete_citado, campo_ausente), evento 682 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: campo_ausente, contrato-produto, entidade-produto (gen_ai: chat)
- evento 704, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 671 (sinal_em_codigo), evento 669 (arvore_podada), evento 664 (corpo_http), evento 676 (resposta), evento 699 (resposta), evento 701 (verbete_entregue, campo_ausente); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: campo_ausente, contrato-produto, entidade-produto

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 657 a 704 da trilha; hash dos eventos deste caso: `69baa87b5fb8c11b`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
