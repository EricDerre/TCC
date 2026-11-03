<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-21`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/sin-21@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `tipo` · selo de probabilidade: **medio** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê o tipo do produto exibido como um objeto JSON em vez de um texto simples, o que pode causar confusão e dificuldade na interpretação dos dados.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo tipo porque o sinal tipo: esperado texto, recebido objeto está presente na resposta HTTP e os verbetes campo_ausente, colecao_no_lugar_de_objeto, contrato-produto estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,01. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1617): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `44439f441a244cf6`):

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
      text "{"valor":"Carnes","moeda":"BRL"}"
      text "Picanha grelhada com alho laminado na brasa"
      text "destaque: Sim"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "{"valor":"Carnes","moeda":"BRL"}"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "{"valor":"Carnes","moeda":"BRL"}"
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

Poda de `corpo_http` (evento 1619): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2404}, depois {"chars": 45}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tipo | texto | objeto |
| tipo | "Carnes" (referência em modo normal) | {"valor": "Carnes", "moeda": "BRL"} em 14 itens |

Trecho podado (hash `8b29b8105a557dd2`):

```text
{"tipo": {"valor": "Carnes", "moeda": "BRL"}}
```

Interceptação (evento 1612): `GET /api/produtos` status 200; corpo `8166f86042f25264`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 0,99 contra 0,01; verbete(s) na evidência: campo_ausente, colecao_no_lugar_de_objeto, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,99 | sim |
| colecao_no_lugar_de_objeto | 0,01 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [colecao_no_lugar_de_objeto]`; verbetes citados: `contrato-produto`, `colecao_no_lugar_de_objeto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `colecao_no_lugar_de_objeto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `campo_ausente`, `colecao_no_lugar_de_objeto`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `colecao_no_lugar_de_objeto` | confere | contexto: `campo_ausente`, `colecao_no_lugar_de_objeto`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[contrato-produto] [colecao_no_lugar_de_objeto]` | confere | {"ids": ["contrato-produto", "colecao_no_lugar_de_objeto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `colecao_no_lugar_de_objeto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids sin-21 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1605 | 1 | entrada | programa | ao_vivo | 2026-11-01T15:09:48 | caso sin-21 |
| 1606 | 2 | acao | programa | ao_vivo | 2026-11-01T15:09:48 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 125.7, "falhou": false} |
| 1607 | 3 | acao | programa | ao_vivo | 2026-11-01T15:09:48 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 7.3, "falhou": false} |
| 1608 | 4 | acao | programa | ao_vivo | 2026-11-01T15:09:48 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 1.8, "falhou": false} |
| 1609 | 5 | acao | programa | ao_vivo | 2026-11-01T15:09:48 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 6.2, "falhou": false} |
| 1610 | 6 | acao | programa | ao_vivo | 2026-11-01T15:09:48 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 4.4, "falhou": false} |
| 1612 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T15:09:48 | GET /api/produtos 200 |
| 1613 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T15:09:48 | conferencia_do_roteiro: confere |
| 1614 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T15:09:48 | conferencia_do_roteiro: confere |
| 1615 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T15:09:48 | conferencia_do_roteiro: confere |
| 1617 | 11 | poda | programa | ao_vivo | 2026-11-01T15:09:48 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1619 | 12 | poda | programa | ao_vivo | 2026-11-01T15:09:48 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1620 | 13 | candidatos | programa | ao_vivo | 2026-11-01T15:09:48 | 3 de 40 verbetes entregues |
| 1622 | 14 | prompt | programa | ao_vivo | 2026-11-01T15:09:48 | {"etapa": "diagnostico", "sha": "3e45e57774226b2a", "prompt_sha256": "3e45e5777422", "chars": 5853, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1624 | 15 | inferencia | programa | ao_vivo | 2026-11-01T15:09:48 | diagnostico: 104,6 s |
| 1625 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T15:09:48 | causa_raiz: `tipo_divergente` |
| 1626 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T15:09:48 | campo: `tipo` |
| 1627 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T15:09:48 | impacto: `O usuário vê o tipo do produto exibido como um objeto JSON em vez de um texto simples, o que pode causar confusão e dificuldade na interpretação dos dados.` |
| 1628 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T15:09:48 | fonte: `[contrato-produto] [colecao_no_lugar_de_objeto]` |
| 1629 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T15:09:48 | fonte_citada: `contrato-produto` |
| 1630 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T15:09:48 | fonte_citada: `colecao_no_lugar_de_objeto` |
| 1631 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T15:09:48 | quatro_linhas_presentes: confere |
| 1632 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T15:09:48 | rotulo_no_conjunto: confere |
| 1633 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T15:09:48 | fonte_existe_na_biblioteca: confere |
| 1634 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T15:09:48 | fonte_existe_na_biblioteca: confere |
| 1635 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T15:09:48 | fonte_estava_no_contexto: confere |
| 1636 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T15:09:48 | fonte_estava_no_contexto: confere |
| 1637 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T15:09:48 | campo_existe_no_caso: confere |
| 1638 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T15:09:48 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1639 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T15:09:48 | notas_nos_verbetes_citados: informativo |
| 1640 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T15:09:48 | impacto: nao_verificavel |
| 1641 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T15:09:48 | fonte_formato_valido: confere |
| 1642 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T15:09:48 | fonte_contem_termo_da_causa: nao_confere |
| 1643 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T15:09:48 | fonte_contem_termo_da_causa: nao_confere |
| 1644 | 35 | decisao | programa | ao_vivo | 2026-11-01T15:09:48 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 1644, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1619 (sinal_em_codigo), evento 1617 (arvore_podada), evento 1612 (corpo_http), evento 1620 (verbete_entregue, campo_ausente), evento 1620 (verbete_entregue, colecao_no_lugar_de_objeto), evento 1620 (verbete_entregue, contrato-produto), evento 1624 (resposta), evento 1629 (verbete_citado, contrato-produto), evento 1630 (verbete_citado, colecao_no_lugar_de_objeto); divergência: não; falha: nenhuma; prov.used: campo_ausente, colecao_no_lugar_de_objeto, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1605 a 1644 da trilha; hash dos eventos deste caso: `565861f1847bbb8f`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
