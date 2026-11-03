<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-16`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/semt-16@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `tipo` · selo de probabilidade: **medio** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê o tipo como um número inteiro em vez de um texto, o que pode causar confusão na exibição dos produtos.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo tipo porque o sinal tipo: esperado texto, recebido inteiro está presente na resposta HTTP e os verbetes campo_ausente, contrato-produto, entidade-produto estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,01. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1681): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `fd4991ac141eed24`):

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
      text "1"
      text "Picanha grelhada com alho laminado na brasa"
      text "destaque: Sim"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "1"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "1"
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

Poda de `corpo_http` (evento 1683): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 1936}, depois {"chars": 11}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tipo | texto | inteiro |
| tipo | "Carnes" (referência em modo normal) | 1 em 14 itens |

Trecho podado (hash `7e091f5a6aa3bb8f`):

```text
{"tipo": 1}
```

Interceptação (evento 1676): `GET /api/produtos` status 200; corpo `283c10134d6edd20`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 0,99 contra 0,01; verbete(s) na evidência: campo_ausente, contrato-produto, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,99 | sim |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [entidade-produto]`; verbetes citados: `contrato-produto`, `entidade-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `campo_ausente`, `contrato-produto`, `entidade-produto` |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `campo_ausente`, `contrato-produto`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `contrato-produto`, `entidade-produto` |
| fonte_formato_valido | `[contrato-produto] [entidade-produto]` | confere | {"ids": ["contrato-produto", "entidade-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids semt-16 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1669 | 1 | entrada | programa | ao_vivo | 2026-11-01T15:12:54 | caso semt-16 |
| 1670 | 2 | acao | programa | ao_vivo | 2026-11-01T15:12:54 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 97.1, "falhou": false} |
| 1671 | 3 | acao | programa | ao_vivo | 2026-11-01T15:12:54 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 15.9, "falhou": false} |
| 1672 | 4 | acao | programa | ao_vivo | 2026-11-01T15:12:54 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 12.1, "falhou": false} |
| 1673 | 5 | acao | programa | ao_vivo | 2026-11-01T15:12:54 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 5.4, "falhou": false} |
| 1674 | 6 | acao | programa | ao_vivo | 2026-11-01T15:12:54 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.7, "falhou": false} |
| 1676 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T15:12:54 | GET /api/produtos 200 |
| 1677 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T15:12:54 | conferencia_do_roteiro: confere |
| 1678 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T15:12:54 | conferencia_do_roteiro: confere |
| 1679 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T15:12:54 | conferencia_do_roteiro: confere |
| 1681 | 11 | poda | programa | ao_vivo | 2026-11-01T15:12:54 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1683 | 12 | poda | programa | ao_vivo | 2026-11-01T15:12:54 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1684 | 13 | candidatos | programa | ao_vivo | 2026-11-01T15:12:54 | 3 de 40 verbetes entregues |
| 1686 | 14 | prompt | programa | ao_vivo | 2026-11-01T15:12:54 | {"etapa": "diagnostico", "sha": "8fdae2354beb61c4", "prompt_sha256": "8fdae2354beb", "chars": 5427, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1688 | 15 | inferencia | programa | ao_vivo | 2026-11-01T15:12:54 | diagnostico: 65,8 s |
| 1689 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T15:12:54 | causa_raiz: `tipo_divergente` |
| 1690 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T15:12:54 | campo: `tipo` |
| 1691 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T15:12:54 | impacto: `O usuário vê o tipo como um número inteiro em vez de um texto, o que pode causar confusão na exibição dos produtos.` |
| 1692 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T15:12:54 | fonte: `[contrato-produto] [entidade-produto]` |
| 1693 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T15:12:54 | fonte_citada: `contrato-produto` |
| 1694 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T15:12:54 | fonte_citada: `entidade-produto` |
| 1695 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T15:12:54 | quatro_linhas_presentes: confere |
| 1696 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T15:12:54 | rotulo_no_conjunto: confere |
| 1697 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T15:12:54 | fonte_existe_na_biblioteca: confere |
| 1698 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T15:12:54 | fonte_existe_na_biblioteca: confere |
| 1699 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T15:12:54 | fonte_estava_no_contexto: confere |
| 1700 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T15:12:54 | fonte_estava_no_contexto: confere |
| 1701 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T15:12:54 | campo_existe_no_caso: confere |
| 1702 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T15:12:54 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1703 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T15:12:54 | notas_nos_verbetes_citados: informativo |
| 1704 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T15:12:54 | impacto: nao_verificavel |
| 1705 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T15:12:54 | fonte_formato_valido: confere |
| 1706 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T15:12:54 | fonte_contem_termo_da_causa: nao_confere |
| 1707 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T15:12:54 | fonte_contem_termo_da_causa: nao_confere |
| 1708 | 35 | decisao | programa | ao_vivo | 2026-11-01T15:12:54 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 1708, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1683 (sinal_em_codigo), evento 1681 (arvore_podada), evento 1676 (corpo_http), evento 1684 (verbete_entregue, campo_ausente), evento 1684 (verbete_entregue, contrato-produto), evento 1684 (verbete_entregue, entidade-produto), evento 1688 (resposta), evento 1693 (verbete_citado, contrato-produto), evento 1694 (verbete_citado, entidade-produto); divergência: não; falha: nenhuma; prov.used: campo_ausente, contrato-produto, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1669 a 1708 da trilha; hash dos eventos deste caso: `65727d072567b0a6`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
