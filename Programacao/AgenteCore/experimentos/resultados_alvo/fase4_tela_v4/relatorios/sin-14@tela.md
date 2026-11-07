<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-14`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v4/qwen2.5_7b/sin-14@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_renomeado` · **CAMPO:** `imagem` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê um campo desconhecido "imagem_v2" na resposta, o que pode causar confusão e dificuldade na integração da interface com a API.`

Justificativa (gerada por molde): O agente respondeu campo_renomeado no campo imagem porque o sinal imagem: esperado imagem, recebido imagem_v2 está presente na resposta HTTP e os verbetes campo_ausente, contrato-produto, campo_renomeado estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 907): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 179}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 909): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2110}, depois {"chars": 33}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| imagem | imagem | imagem_v2 |

Trecho podado (hash `b2042fcbcc75423a`):

```text
{"imagem_v2": "picanha_alho.jpg"}
```

Interceptação (evento 903): `GET /api/produtos` status 200; corpo `58a3465f7f2815fd`, árvore `None`.

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

Linha FONTE como veio: `[campo_renomeado]`; verbetes citados: `campo_renomeado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | confere | contexto: `campo_ausente`, `contrato-produto`, `campo_renomeado` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `campo_ausente`, `contrato-produto`, `campo_renomeado` |
| fonte_formato_valido | `[campo_renomeado]` | confere | {"ids": ["campo_renomeado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_renomeado` | confere | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `imagem` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-14 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 896 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:29:01 | caso sin-14 |
| 897 | 2 | acao | programa | ao_vivo | 2026-11-06T10:29:01 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 118.3, "falhou": false} |
| 898 | 3 | acao | programa | ao_vivo | 2026-11-06T10:29:01 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 8.2, "falhou": false} |
| 899 | 4 | acao | programa | ao_vivo | 2026-11-06T10:29:01 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.0, "falhou": false} |
| 900 | 5 | acao | programa | ao_vivo | 2026-11-06T10:29:01 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 4.2, "falhou": false} |
| 901 | 6 | acao | programa | ao_vivo | 2026-11-06T10:29:01 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 2.8, "falhou": false} |
| 903 | 7 | interceptacao | programa | ao_vivo | 2026-11-06T10:29:01 | GET /api/produtos 200 |
| 904 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | conferencia_do_roteiro: confere |
| 905 | 9 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | conferencia_do_roteiro: confere |
| 906 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | conferencia_do_roteiro: confere |
| 907 | 11 | poda | programa | ao_vivo | 2026-11-06T10:29:01 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 909 | 12 | poda | programa | ao_vivo | 2026-11-06T10:29:01 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 910 | 13 | candidatos | programa | ao_vivo | 2026-11-06T10:29:01 | 3 de 39 verbetes entregues |
| 912 | 14 | prompt | programa | ao_vivo | 2026-11-06T10:29:01 | {"etapa": "diagnostico", "sha": "d2feba38440ef929", "prompt_sha256": "d2feba38440e", "chars": 3492, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 914 | 15 | inferencia | programa | ao_vivo | 2026-11-06T10:29:01 | diagnostico: 70,6 s |
| 915 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T10:29:01 | causa_raiz: `campo_renomeado` |
| 916 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T10:29:01 | campo: `imagem` |
| 917 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T10:29:01 | impacto: `O usuário vê um campo desconhecido "imagem_v2" na resposta, o que pode causar confusão e dificuldade na integração da interface com a API.` |
| 918 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T10:29:01 | fonte: `[campo_renomeado]` |
| 919 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T10:29:01 | fonte_citada: `campo_renomeado` |
| 920 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | quatro_linhas_presentes: confere |
| 921 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | rotulo_no_conjunto: confere |
| 922 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | fonte_existe_na_biblioteca: confere |
| 923 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | fonte_estava_no_contexto: confere |
| 924 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | campo_existe_no_caso: confere |
| 925 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 926 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | notas_nos_verbetes_citados: informativo |
| 927 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | impacto: nao_verificavel |
| 928 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | fonte_formato_valido: confere |
| 929 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | fonte_contem_termo_da_causa: confere |
| 930 | 31 | decisao | programa | ao_vivo | 2026-11-06T10:29:01 | diagnostico: escolha campo_renomeado; divergência não |

</details>

Nós de decisão:

- evento 930, `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido; evidência: evento 909 (sinal_em_codigo), evento 907 (arvore_podada), evento 903 (corpo_http), evento 910 (verbete_entregue, campo_ausente), evento 910 (verbete_entregue, contrato-produto), evento 910 (verbete_entregue, campo_renomeado), evento 914 (resposta), evento 919 (verbete_citado, campo_renomeado); divergência: não; falha: nenhuma; prov.used: campo_ausente, contrato-produto, campo_renomeado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 896 a 930 da trilha; hash dos eventos deste caso: `70b16354c8b50a0a`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
