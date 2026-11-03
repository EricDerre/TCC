<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-16`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/semt-16@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `tipo` · selo de probabilidade: **medio** (p = 0,98)

**IMPACTO (declarado):** `O usuário vê o tipo como um número inteiro em vez de uma string, o que pode causar interpretações incorretas na interface.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo tipo porque o sinal tipo: esperado texto, recebido inteiro está presente na resposta HTTP e os verbetes campo_ausente, contrato-produto, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,01. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1673): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 1675): regras diff_contra_contrato; antes {"chars": 1936}, depois {"chars": 11}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tipo | texto | inteiro |

Trecho podado (hash `7e091f5a6aa3bb8f`):

```text
{"tipo": 1}
```

Interceptação (evento 1668): `GET /api/produtos` status 200; corpo `283c10134d6edd20`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 0,98 contra 0,01; verbete(s) na evidência: campo_ausente, contrato-produto, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,98 | sim |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| resposta_truncada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `campo_ausente`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids semt-16 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1661 | 1 | entrada | programa | ao_vivo | 2026-11-01T12:14:32 | caso semt-16 |
| 1662 | 2 | acao | programa | ao_vivo | 2026-11-01T12:14:32 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 129.5, "falhou": false} |
| 1663 | 3 | acao | programa | ao_vivo | 2026-11-01T12:14:32 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 9.9, "falhou": false} |
| 1664 | 4 | acao | programa | ao_vivo | 2026-11-01T12:14:32 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 13.5, "falhou": false} |
| 1665 | 5 | acao | programa | ao_vivo | 2026-11-01T12:14:32 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 9.5, "falhou": false} |
| 1666 | 6 | acao | programa | ao_vivo | 2026-11-01T12:14:32 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 5.4, "falhou": false} |
| 1668 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T12:14:32 | GET /api/produtos 200 |
| 1669 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T12:14:32 | conferencia_do_roteiro: confere |
| 1670 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T12:14:32 | conferencia_do_roteiro: confere |
| 1671 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T12:14:32 | conferencia_do_roteiro: confere |
| 1673 | 11 | poda | programa | ao_vivo | 2026-11-01T12:14:32 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1675 | 12 | poda | programa | ao_vivo | 2026-11-01T12:14:32 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1676 | 13 | candidatos | programa | ao_vivo | 2026-11-01T12:14:32 | 3 de 40 verbetes entregues |
| 1678 | 14 | prompt | programa | ao_vivo | 2026-11-01T12:14:32 | {"etapa": "diagnostico", "sha": "f225a56db41dfab0", "prompt_sha256": "f225a56db41d", "chars": 5479, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1680 | 15 | inferencia | programa | ao_vivo | 2026-11-01T12:14:32 | diagnostico: 64,1 s |
| 1681 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T12:14:32 | causa_raiz: `tipo_divergente` |
| 1682 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T12:14:32 | campo: `tipo` |
| 1683 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T12:14:32 | impacto: `O usuário vê o tipo como um número inteiro em vez de uma string, o que pode causar interpretações incorretas na interface.` |
| 1684 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T12:14:32 | fonte: `[contrato-produto]` |
| 1685 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T12:14:32 | fonte_citada: `contrato-produto` |
| 1686 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T12:14:32 | quatro_linhas_presentes: confere |
| 1687 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T12:14:32 | rotulo_no_conjunto: confere |
| 1688 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T12:14:32 | fonte_existe_na_biblioteca: confere |
| 1689 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T12:14:32 | fonte_estava_no_contexto: confere |
| 1690 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T12:14:32 | campo_existe_no_caso: confere |
| 1691 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T12:14:32 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1692 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T12:14:32 | notas_nos_verbetes_citados: informativo |
| 1693 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T12:14:32 | impacto: nao_verificavel |
| 1694 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T12:14:32 | fonte_formato_valido: confere |
| 1695 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T12:14:32 | fonte_contem_termo_da_causa: nao_confere |
| 1696 | 31 | decisao | programa | ao_vivo | 2026-11-01T12:14:32 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 1696, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1675 (sinal_em_codigo), evento 1673 (arvore_podada), evento 1668 (corpo_http), evento 1676 (verbete_entregue, campo_ausente), evento 1676 (verbete_entregue, contrato-produto), evento 1676 (verbete_entregue, colecao_no_lugar_de_objeto), evento 1680 (resposta), evento 1685 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: campo_ausente, contrato-produto, colecao_no_lugar_de_objeto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1661 a 1696 da trilha; hash dos eventos deste caso: `c5d2c68dd893a4fc`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
