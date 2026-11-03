<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-17`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/tra-17@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,86)

**IMPACTO (declarado):** `A interface exibe uma lista de produtos em vez de um único produto, causando confusão no usuário.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto porque o sinal arvore: esperado 0 linha(s) da referência, recebido 0 linha(s) novas está presente na tela e os verbetes entidade-produto, contrato-produto, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,04 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1930): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 1931): regras diff_contra_contrato; antes {"chars": 2068}, depois {"chars": 174}.

Trecho podado (hash `b78f8a85ed458c1a`):

```text
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 1926): `GET /api/produtos` status 200; corpo `0ef7077cc7a06cfa`, árvore `None`.

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não resposta_truncada: a escolha tem probabilidade 0,86 contra 0,04; verbete(s) na evidência: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,86 | sim |
| resposta_truncada | 0,04 |  |
| corpo_nao_e_json | 0,04 |  |
| corpo_vazio | 0,04 |  |
| tipo_divergente | 0,03 |  |
| formato_de_data_divergente | 0,02 |  |
| estrutura_aninhada_divergente | 0,01 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [colecao_no_lugar_de_objeto]`; verbetes citados: `contrato-produto`, `colecao_no_lugar_de_objeto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `colecao_no_lugar_de_objeto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| O verbete citado estava no contexto entregue ao modelo | `colecao_no_lugar_de_objeto` | confere | contexto: `entidade-produto`, `contrato-produto`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto`, `colecao_no_lugar_de_objeto` |
| fonte_formato_valido | `[contrato-produto] [colecao_no_lugar_de_objeto]` | confere | {"ids": ["contrato-produto", "colecao_no_lugar_de_objeto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |
| fonte_contem_termo_da_causa | `colecao_no_lugar_de_objeto` | confere | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids tra-17 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1919 | 1 | entrada | programa | ao_vivo | 2026-11-01T12:23:06 | caso tra-17 |
| 1920 | 2 | acao | programa | ao_vivo | 2026-11-01T12:23:06 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 92.1, "falhou": false} |
| 1921 | 3 | acao | programa | ao_vivo | 2026-11-01T12:23:06 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 9.1, "falhou": false} |
| 1922 | 4 | acao | programa | ao_vivo | 2026-11-01T12:23:06 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 3.0, "falhou": false} |
| 1923 | 5 | acao | programa | ao_vivo | 2026-11-01T12:23:06 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 3.8, "falhou": false} |
| 1924 | 6 | acao | programa | ao_vivo | 2026-11-01T12:23:06 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 6.4, "falhou": false} |
| 1926 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T12:23:06 | GET /api/produtos 200 |
| 1927 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T12:23:06 | conferencia_do_roteiro: confere |
| 1928 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T12:23:06 | conferencia_do_roteiro: confere |
| 1929 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T12:23:06 | conferencia_do_roteiro: confere |
| 1930 | 11 | poda | programa | ao_vivo | 2026-11-01T12:23:06 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1931 | 12 | poda | programa | ao_vivo | 2026-11-01T12:23:06 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1932 | 13 | candidatos | programa | ao_vivo | 2026-11-01T12:23:06 | 3 de 40 verbetes entregues |
| 1933 | 14 | prompt | programa | ao_vivo | 2026-11-01T12:23:06 | {"etapa": "diagnostico", "sha": "64332b968215cf4b", "prompt_sha256": "64332b968215", "chars": 5509, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1935 | 15 | inferencia | programa | ao_vivo | 2026-11-01T12:23:06 | diagnostico: 35,6 s |
| 1936 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T12:23:06 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 1937 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T12:23:06 | campo: `nenhum` |
| 1938 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T12:23:06 | impacto: `A interface exibe uma lista de produtos em vez de um único produto, causando confusão no usuário.` |
| 1939 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T12:23:06 | fonte: `[contrato-produto] [colecao_no_lugar_de_objeto]` |
| 1940 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T12:23:06 | fonte_citada: `contrato-produto` |
| 1941 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T12:23:06 | fonte_citada: `colecao_no_lugar_de_objeto` |
| 1942 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T12:23:06 | quatro_linhas_presentes: confere |
| 1943 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T12:23:06 | rotulo_no_conjunto: confere |
| 1944 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T12:23:06 | fonte_existe_na_biblioteca: confere |
| 1945 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T12:23:06 | fonte_existe_na_biblioteca: confere |
| 1946 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T12:23:06 | fonte_estava_no_contexto: confere |
| 1947 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T12:23:06 | fonte_estava_no_contexto: confere |
| 1948 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T12:23:06 | campo_existe_no_caso: nao_se_aplica |
| 1949 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T12:23:06 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1950 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T12:23:06 | notas_nos_verbetes_citados: informativo |
| 1951 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T12:23:06 | impacto: nao_verificavel |
| 1952 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T12:23:06 | fonte_formato_valido: confere |
| 1953 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T12:23:06 | fonte_contem_termo_da_causa: nao_confere |
| 1954 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T12:23:06 | fonte_contem_termo_da_causa: confere |
| 1955 | 35 | decisao | programa | ao_vivo | 2026-11-01T12:23:06 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 1955, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 1931 (sinal_em_codigo), evento 1930 (arvore_podada), evento 1926 (corpo_http), evento 1932 (verbete_entregue, entidade-produto), evento 1932 (verbete_entregue, contrato-produto), evento 1932 (verbete_entregue, colecao_no_lugar_de_objeto), evento 1935 (resposta), evento 1940 (verbete_citado, contrato-produto), evento 1941 (verbete_citado, colecao_no_lugar_de_objeto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1919 a 1955 da trilha; hash dos eventos deste caso: `5de1463d2dd581a6`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
