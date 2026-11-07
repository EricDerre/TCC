<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-24`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/lex-24@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `resumo` · selo de probabilidade: **medio** (p = 0,98)

**IMPACTO (declarado):** `O usuário vê o texto "Com canela e aÃ§Ãºcar" em vez de "Com canela e açúcar".`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta no campo resumo porque o sinal resumo: esperado "Com canela e açúcar" (referência em modo normal), recebido "Com canela e aÃ§Ãºcar" está presente na resposta HTTP e os verbetes codificacao_incorreta, entidade-produto, contrato-produto estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 145): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 197}, depois {"linhas": 42}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 1 linha(s) da referência | 1 linha(s) novas |

Trecho podado (hash `e54828beffaf5345`):

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
  dialog
    heading "Abacaxi na Brasa" level=4
    text "Com canela e aÃ§Ãºcar"

```

Poda de `corpo_http` (evento 147): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 141}, depois {"chars": 255}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| resumo | "Com canela e açúcar" (referência em modo normal) | "Com canela e aÃ§Ãºcar" |

Trecho podado (hash `a3cc0e2822849099`):

```text
{"id": 14, "nome": "Abacaxi na Brasa", "resumo": "Com canela e aÃ§Ãºcar", "tipo": "Sobremesas", "preco": 14.9, "imagem": "abacaxi.jpg", "destaque": false} (contra a referência em modo normal: resumo "Com canela e aÃ§Ãºcar" em vez de "Com canela e açúcar")
```

Interceptação (evento 138): `GET /api/produtos` status 200; corpo `40dfa78ee8bc48ac`, árvore `None`.

Interceptação (evento 140): `GET /api/produtos/14` status 200; corpo `25684c42e5d55085`, árvore `None`.

## 3. Contraste com a segunda causa

codificacao_incorreta e não valor_fora_do_dominio: a escolha tem probabilidade 0,98 contra 0,00; verbete(s) na evidência: codificacao_incorreta, entidade-produto, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 0,98 | sim |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[codificacao_incorreta]`; verbetes citados: `codificacao_incorreta`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `codificacao_incorreta` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `codificacao_incorreta` | confere | contexto: `codificacao_incorreta`, `entidade-produto`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | confere | verbetes: `codificacao_incorreta` |
| fonte_formato_valido | `[codificacao_incorreta]` | confere | {"ids": ["codificacao_incorreta"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `codificacao_incorreta` | confere | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `resumo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids lex-24 --k 3`

## 6. Árvore completa

<details><summary>34 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 129 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:33:02 | caso lex-24 |
| 130 | 2 | acao | programa | ao_vivo | 2026-11-06T11:33:03 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 117.4, "falhou": false} |
| 131 | 3 | acao | programa | ao_vivo | 2026-11-06T11:33:03 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 8.2, "falhou": false} |
| 132 | 4 | acao | programa | ao_vivo | 2026-11-06T11:33:03 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.8, "falhou": false} |
| 133 | 5 | acao | programa | ao_vivo | 2026-11-06T11:33:03 | {"passo": 4, "acao": "clicar", "seletor": "#produtos-api-grid .saiba-mais[data-id='14']", "url": null, "tempo_ms": 32.3, "falhou": false} |
| 134 | 6 | acao | programa | ao_vivo | 2026-11-06T11:33:03 | {"passo": 5, "acao": "esperar", "seletor": "#modalDetalhe", "url": null, "tempo_ms": 217.2, "falhou": false} |
| 135 | 7 | acao | programa | ao_vivo | 2026-11-06T11:33:03 | {"passo": 6, "acao": "conferir", "seletor": "#modalDetalheTitulo", "url": null, "tempo_ms": 4.0, "falhou": false} |
| 136 | 8 | acao | programa | ao_vivo | 2026-11-06T11:33:03 | {"passo": 7, "acao": "conferir", "seletor": "#modalDetalheCorpo", "url": null, "tempo_ms": 3.8, "falhou": false} |
| 138 | 9 | interceptacao | programa | ao_vivo | 2026-11-06T11:33:03 | GET /api/produtos 200 |
| 140 | 10 | interceptacao | programa | ao_vivo | 2026-11-06T11:33:03 | GET /api/produtos/14 200 |
| 141 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:33:03 | conferencia_do_roteiro: confere |
| 142 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:33:03 | conferencia_do_roteiro: confere |
| 143 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:33:03 | conferencia_do_roteiro: confere |
| 145 | 14 | poda | programa | ao_vivo | 2026-11-06T11:33:03 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 147 | 15 | poda | programa | ao_vivo | 2026-11-06T11:33:03 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 148 | 16 | candidatos | programa | ao_vivo | 2026-11-06T11:33:03 | 3 de 39 verbetes entregues |
| 150 | 17 | prompt | programa | ao_vivo | 2026-11-06T11:33:03 | {"etapa": "diagnostico", "sha": "786961b57461fc55", "prompt_sha256": "786961b57461", "chars": 3715, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 152 | 18 | inferencia | programa | ao_vivo | 2026-11-06T11:33:03 | diagnostico: 77,3 s |
| 153 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T11:33:03 | causa_raiz: `codificacao_incorreta` |
| 154 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T11:33:03 | campo: `resumo` |
| 155 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T11:33:03 | impacto: `O usuário vê o texto "Com canela e aÃ§Ãºcar" em vez de "Com canela e açúcar".` |
| 156 | 22 | declaracao | modelo | ao_vivo | 2026-11-06T11:33:03 | fonte: `[codificacao_incorreta]` |
| 157 | 23 | declaracao | modelo | ao_vivo | 2026-11-06T11:33:03 | fonte_citada: `codificacao_incorreta` |
| 158 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:33:03 | quatro_linhas_presentes: confere |
| 159 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:33:03 | rotulo_no_conjunto: confere |
| 160 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:33:03 | fonte_existe_na_biblioteca: confere |
| 161 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T11:33:03 | fonte_estava_no_contexto: confere |
| 162 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T11:33:03 | campo_existe_no_caso: confere |
| 163 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T11:33:03 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 164 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T11:33:03 | notas_nos_verbetes_citados: informativo |
| 165 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T11:33:03 | impacto: nao_verificavel |
| 166 | 32 | verificacao | verificacao | ao_vivo | 2026-11-06T11:33:03 | fonte_formato_valido: confere |
| 167 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T11:33:03 | fonte_contem_termo_da_causa: confere |
| 168 | 34 | decisao | programa | ao_vivo | 2026-11-06T11:33:03 | diagnostico: escolha codificacao_incorreta; divergência não |

</details>

Nós de decisão:

- evento 168, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 147 (sinal_em_codigo), evento 145 (arvore_podada), evento 140 (corpo_http), evento 148 (verbete_entregue, codificacao_incorreta), evento 148 (verbete_entregue, entidade-produto), evento 148 (verbete_entregue, contrato-produto), evento 152 (resposta), evento 157 (verbete_citado, codificacao_incorreta); divergência: não; falha: nenhuma; prov.used: codificacao_incorreta, entidade-produto, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 129 a 168 da trilha; hash dos eventos deste caso: `c06f2f7d8b1e189f`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
