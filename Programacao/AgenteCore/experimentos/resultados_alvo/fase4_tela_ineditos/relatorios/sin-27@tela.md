<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-27`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/sin-27@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_renomeado` · **CAMPO:** `imagem` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê um campo desconhecido "imagem_v2" na resposta, o que pode causar confusão e dificuldade na integração da interface com a API.`

Justificativa (gerada por molde): O agente respondeu campo_renomeado no campo imagem porque o sinal imagem: esperado imagem, recebido imagem_v2 está presente na resposta HTTP e os verbetes campo_ausente, contrato-produto, campo_renomeado estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 684): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 179}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 686): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2110}, depois {"chars": 33}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| imagem | imagem | imagem_v2 |

Trecho podado (hash `b2042fcbcc75423a`):

```text
{"imagem_v2": "picanha_alho.jpg"}
```

Interceptação (evento 680): `GET /api/produtos` status 200; corpo `58a3465f7f2815fd`, árvore `None`.

## 3. Contraste com a segunda causa

campo_renomeado e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: campo_ausente, contrato-produto, campo_renomeado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_renomeado | 1,00 | sim |
| campo_ausente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_renomeado] [contrato-produto]`; verbetes citados: `campo_renomeado`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | confere | contexto: `campo_ausente`, `contrato-produto`, `campo_renomeado` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `campo_ausente`, `contrato-produto`, `campo_renomeado` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `campo_ausente`, `contrato-produto`, `campo_renomeado` |
| fonte_formato_valido | `[campo_renomeado] [contrato-produto]` | confere | {"ids": ["campo_renomeado", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_renomeado` | confere | {"termo": "campo_renomeado"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `imagem` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids sin-27 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 673 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:51:44 | caso sin-27 |
| 674 | 2 | acao | programa | ao_vivo | 2026-11-06T11:51:44 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 119.6, "falhou": false} |
| 675 | 3 | acao | programa | ao_vivo | 2026-11-06T11:51:44 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 6.6, "falhou": false} |
| 676 | 4 | acao | programa | ao_vivo | 2026-11-06T11:51:44 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.7, "falhou": false} |
| 677 | 5 | acao | programa | ao_vivo | 2026-11-06T11:51:44 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 4.0, "falhou": false} |
| 678 | 6 | acao | programa | ao_vivo | 2026-11-06T11:51:44 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.2, "falhou": false} |
| 680 | 7 | interceptacao | programa | ao_vivo | 2026-11-06T11:51:44 | GET /api/produtos 200 |
| 681 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T11:51:44 | conferencia_do_roteiro: confere |
| 682 | 9 | verificacao | verificacao | ao_vivo | 2026-11-06T11:51:44 | conferencia_do_roteiro: confere |
| 683 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:51:44 | conferencia_do_roteiro: confere |
| 684 | 11 | poda | programa | ao_vivo | 2026-11-06T11:51:44 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 686 | 12 | poda | programa | ao_vivo | 2026-11-06T11:51:44 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 687 | 13 | candidatos | programa | ao_vivo | 2026-11-06T11:51:44 | 3 de 39 verbetes entregues |
| 689 | 14 | prompt | programa | ao_vivo | 2026-11-06T11:51:44 | {"etapa": "diagnostico", "sha": "d2feba38440ef929", "prompt_sha256": "d2feba38440e", "chars": 3492, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 691 | 15 | inferencia | programa | ao_vivo | 2026-11-06T11:51:44 | diagnostico: 57,9 s |
| 692 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T11:51:44 | causa_raiz: `campo_renomeado` |
| 693 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T11:51:44 | campo: `imagem` |
| 694 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T11:51:44 | impacto: `O usuário vê um campo desconhecido "imagem_v2" na resposta, o que pode causar confusão e dificuldade na integração da interface com a API.` |
| 695 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T11:51:44 | fonte: `[campo_renomeado] [contrato-produto]` |
| 696 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T11:51:44 | fonte_citada: `campo_renomeado` |
| 697 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T11:51:44 | fonte_citada: `contrato-produto` |
| 698 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:51:44 | quatro_linhas_presentes: confere |
| 699 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:51:44 | rotulo_no_conjunto: confere |
| 700 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:51:44 | fonte_existe_na_biblioteca: confere |
| 701 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:51:44 | fonte_existe_na_biblioteca: confere |
| 702 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:51:44 | fonte_estava_no_contexto: confere |
| 703 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T11:51:44 | fonte_estava_no_contexto: confere |
| 704 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T11:51:44 | campo_existe_no_caso: confere |
| 705 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T11:51:44 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 706 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T11:51:44 | notas_nos_verbetes_citados: informativo |
| 707 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T11:51:44 | impacto: nao_verificavel |
| 708 | 32 | verificacao | verificacao | ao_vivo | 2026-11-06T11:51:44 | fonte_formato_valido: confere |
| 709 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T11:51:44 | fonte_contem_termo_da_causa: confere |
| 710 | 34 | verificacao | verificacao | ao_vivo | 2026-11-06T11:51:44 | fonte_contem_termo_da_causa: nao_confere |
| 711 | 35 | decisao | programa | ao_vivo | 2026-11-06T11:51:44 | diagnostico: escolha campo_renomeado; divergência não |

</details>

Nós de decisão:

- evento 711, `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido; evidência: evento 686 (sinal_em_codigo), evento 684 (arvore_podada), evento 680 (corpo_http), evento 687 (verbete_entregue, campo_ausente), evento 687 (verbete_entregue, contrato-produto), evento 687 (verbete_entregue, campo_renomeado), evento 691 (resposta), evento 696 (verbete_citado, campo_renomeado), evento 697 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: campo_ausente, contrato-produto, campo_renomeado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 673 a 711 da trilha; hash dos eventos deste caso: `638d7577d35b8c4e`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
