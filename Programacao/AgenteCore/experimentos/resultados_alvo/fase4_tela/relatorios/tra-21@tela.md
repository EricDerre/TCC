<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-21`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/tra-21@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,89)

**IMPACTO (declarado):** `A interface web exibe 10 produtos a menos do que o esperado, pois a resposta da API está no formato de uma lista de objetos em vez de um único objeto.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto porque o sinal arvore: esperado 1 linha(s) da referência, recebido 1 linha(s) novas está presente na tela e os verbetes entidade-produto, contrato-produto, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,05 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 2108): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 183}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 1 linha(s) da referência | 1 linha(s) novas |

Trecho podado (hash `7c54fbd0508aace9`):

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
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 2109): regras diff_contra_contrato; antes {"chars": 1928}, depois {"chars": 174}.

Trecho podado (hash `b78f8a85ed458c1a`):

```text
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 2106): `GET /api/produtos` status 200; corpo `4f6d409f5a92ce2d`, árvore `None`.

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não resposta_truncada: a escolha tem probabilidade 0,89 contra 0,05; verbete(s) na evidência: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,89 | sim |
| resposta_truncada | 0,05 |  |
| contagem_inconsistente | 0,05 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[colecao_no_lugar_de_objeto]`; verbetes citados: `colecao_no_lugar_de_objeto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `colecao_no_lugar_de_objeto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `colecao_no_lugar_de_objeto` | confere | contexto: `entidade-produto`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto`, `colecao_no_lugar_de_objeto` |
| fonte_formato_valido | `[colecao_no_lugar_de_objeto]` | confere | {"ids": ["colecao_no_lugar_de_objeto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `colecao_no_lugar_de_objeto` | confere | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids tra-21 --k 3`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2102 | 1 | entrada | programa | ao_vivo | 2026-11-01T12:27:06 | caso tra-21 |
| 2103 | 2 | acao | programa | ao_vivo | 2026-11-01T12:27:06 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 170.9, "falhou": false} |
| 2104 | 3 | acao | programa | ao_vivo | 2026-11-01T12:27:06 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 10.7, "falhou": false} |
| 2105 | 4 | acao | programa | ao_vivo | 2026-11-01T12:27:06 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 1.7, "falhou": true} |
| 2106 | 5 | interceptacao | programa | ao_vivo | 2026-11-01T12:27:06 | GET /api/produtos 200 |
| 2107 | 6 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:06 | conferencia_do_roteiro: nao_confere |
| 2108 | 7 | poda | programa | ao_vivo | 2026-11-01T12:27:06 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 2109 | 8 | poda | programa | ao_vivo | 2026-11-01T12:27:06 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 2110 | 9 | candidatos | programa | ao_vivo | 2026-11-01T12:27:06 | 3 de 40 verbetes entregues |
| 2112 | 10 | prompt | programa | ao_vivo | 2026-11-01T12:27:06 | {"etapa": "diagnostico", "sha": "155f43c8062e1b09", "prompt_sha256": "155f43c8062e", "chars": 5643, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2114 | 11 | inferencia | programa | ao_vivo | 2026-11-01T12:27:06 | diagnostico: 45,1 s |
| 2115 | 12 | declaracao | modelo | ao_vivo | 2026-11-01T12:27:06 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 2116 | 13 | declaracao | modelo | ao_vivo | 2026-11-01T12:27:06 | campo: `nenhum` |
| 2117 | 14 | declaracao | modelo | ao_vivo | 2026-11-01T12:27:06 | impacto: `A interface web exibe 10 produtos a menos do que o esperado, pois a resposta da API está no formato de uma lista de objetos em vez de um único objeto.` |
| 2118 | 15 | declaracao | modelo | ao_vivo | 2026-11-01T12:27:06 | fonte: `[colecao_no_lugar_de_objeto]` |
| 2119 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T12:27:06 | fonte_citada: `colecao_no_lugar_de_objeto` |
| 2120 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:06 | quatro_linhas_presentes: confere |
| 2121 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:06 | rotulo_no_conjunto: confere |
| 2122 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:06 | fonte_existe_na_biblioteca: confere |
| 2123 | 20 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:06 | fonte_estava_no_contexto: confere |
| 2124 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:06 | campo_existe_no_caso: nao_se_aplica |
| 2125 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:06 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2126 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:06 | notas_nos_verbetes_citados: informativo |
| 2127 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:06 | impacto: nao_verificavel |
| 2128 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:06 | fonte_formato_valido: confere |
| 2129 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T12:27:06 | fonte_contem_termo_da_causa: confere |
| 2130 | 27 | decisao | programa | ao_vivo | 2026-11-01T12:27:06 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 2130, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 2109 (sinal_em_codigo), evento 2108 (arvore_podada), evento 2106 (corpo_http), evento 2110 (verbete_entregue, entidade-produto), evento 2110 (verbete_entregue, contrato-produto), evento 2110 (verbete_entregue, colecao_no_lugar_de_objeto), evento 2114 (resposta), evento 2119 (verbete_citado, colecao_no_lugar_de_objeto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2102 a 2130 da trilha; hash dos eventos deste caso: `92efa4057a6a8a74`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
