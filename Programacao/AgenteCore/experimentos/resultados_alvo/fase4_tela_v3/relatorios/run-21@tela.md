<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-21`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/run-21@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `registro_duplicado` · **CAMPO:** `id` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: nenhum verbete entregue trata da causa respondida registro_duplicado

**IMPACTO (declarado):** `O usuário vê 10 linha(s) a mais de cartão(s) de produto, com a Picanha ao Alho duplicada.`

Justificativa (gerada por molde): O agente respondeu registro_duplicado no campo id porque o sinal itens: esperado 14 itens (referência em modo normal), recebido o id 1 ("Picanha ao Alho") aparece 2 vezes está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida registro_duplicado. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Poda de `arvore` (evento 2167): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 203}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 6 linha(s) da referência | 6 linha(s) novas |

Trecho podado (hash `d14966ad6e77a8a5`):

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
    text "(mais 12 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 2169): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2230}, depois {"chars": 301}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| itens | 14 itens (referência em modo normal) | o id 1 ("Picanha ao Alho") aparece 2 vezes |

Trecho podado (hash `7e9a03646e43dde2`):

```text
lista com 15 itens (referência em modo normal: 14); o id 1 ("Picanha ao Alho") aparece 2 vezes; por exemplo: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true} (aparece 2 vezes)
```

Interceptação (evento 2164): `GET /api/produtos` status 200; corpo `a7dbc0cbf00850f4`, árvore `None`.

## 3. Contraste com a segunda causa

registro_duplicado e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| registro_duplicado | 1,00 | sim |
| colecao_no_lugar_de_objeto | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| contagem_inconsistente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `registro_duplicado` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "registro_duplicado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids run-21 --k 3`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2159 | 1 | entrada | programa | ao_vivo | 2026-11-05T19:54:24 | caso run-21 |
| 2160 | 2 | acao | programa | ao_vivo | 2026-11-05T19:54:24 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 89.0, "falhou": false} |
| 2161 | 3 | acao | programa | ao_vivo | 2026-11-05T19:54:24 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 7.6, "falhou": false} |
| 2162 | 4 | acao | programa | ao_vivo | 2026-11-05T19:54:24 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 3.1, "falhou": true} |
| 2164 | 5 | interceptacao | programa | ao_vivo | 2026-11-05T19:54:24 | GET /api/produtos 200 |
| 2165 | 6 | verificacao | verificacao | ao_vivo | 2026-11-05T19:54:24 | conferencia_do_roteiro: nao_confere |
| 2167 | 7 | poda | programa | ao_vivo | 2026-11-05T19:54:24 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 2169 | 8 | poda | programa | ao_vivo | 2026-11-05T19:54:24 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 2170 | 9 | candidatos | programa | ao_vivo | 2026-11-05T19:54:24 | 3 de 39 verbetes entregues |
| 2172 | 10 | prompt | programa | ao_vivo | 2026-11-05T19:54:24 | {"etapa": "diagnostico", "sha": "5b3c2652c24f5f4a", "prompt_sha256": "5b3c2652c24f", "chars": 4048, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2174 | 11 | inferencia | programa | ao_vivo | 2026-11-05T19:54:24 | diagnostico: 44,8 s |
| 2175 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T19:54:24 | causa_raiz: `registro_duplicado` |
| 2176 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T19:54:24 | campo: `id` |
| 2177 | 14 | declaracao | modelo | ao_vivo | 2026-11-05T19:54:24 | impacto: `O usuário vê 10 linha(s) a mais de cartão(s) de produto, com a Picanha ao Alho duplicada.` |
| 2178 | 15 | declaracao | modelo | ao_vivo | 2026-11-05T19:54:24 | fonte: `[contrato-produto]` |
| 2179 | 16 | declaracao | modelo | ao_vivo | 2026-11-05T19:54:24 | fonte_citada: `contrato-produto` |
| 2180 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T19:54:24 | quatro_linhas_presentes: confere |
| 2181 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T19:54:24 | rotulo_no_conjunto: confere |
| 2182 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T19:54:24 | fonte_existe_na_biblioteca: confere |
| 2183 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T19:54:24 | fonte_estava_no_contexto: confere |
| 2184 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T19:54:24 | campo_existe_no_caso: confere |
| 2185 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T19:54:24 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 2186 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T19:54:24 | notas_nos_verbetes_citados: informativo |
| 2187 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T19:54:24 | impacto: nao_verificavel |
| 2188 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T19:54:24 | fonte_formato_valido: confere |
| 2189 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T19:54:24 | fonte_contem_termo_da_causa: nao_confere |
| 2190 | 27 | decisao | programa | ao_vivo | 2026-11-05T19:54:24 | diagnostico: escolha registro_duplicado; divergência sim |

</details>

Nós de decisão:

- evento 2190, `diagnostico`: escolha `registro_duplicado`; resultado rotulo_emitido; evidência: evento 2169 (sinal_em_codigo), evento 2167 (arvore_podada), evento 2164 (corpo_http), evento 2170 (verbete_entregue, entidade-produto), evento 2170 (verbete_entregue, contrato-produto), evento 2170 (verbete_entregue, estrutura_aninhada_divergente), evento 2174 (resposta), evento 2179 (verbete_citado, contrato-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2159 a 2190 da trilha; hash dos eventos deste caso: `21c53e159ba0a52a`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
