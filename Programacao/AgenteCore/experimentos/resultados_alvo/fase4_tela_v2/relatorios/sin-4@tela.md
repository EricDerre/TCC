<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-4`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/sin-4@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `A tela exibe informações incompletas, mostrando dois elementos a menos e adicionando dois elementos não esperados.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto porque o sinal esperado objeto, recebido lista está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 154): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 197}, depois {"linhas": 41}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 2 linha(s) da referência | 1 linha(s) novas |

Trecho podado (hash `d5173f7cbffdeeca`):

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
    text "(sem descrição)"

```

Poda de `corpo_http` (evento 156): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 163}, depois {"chars": 174}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
|  | objeto | lista |

Trecho podado (hash `b78f8a85ed458c1a`):

```text
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 147): `GET /api/produtos` status 200; corpo `4b1bdd056e7a8c3b`, árvore `None`.

Interceptação (evento 149): `GET /api/produtos/1` status 200; corpo `3d81a09c6ed20335`, árvore `None`.

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não resposta_truncada: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 1,00 | sim |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

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

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids sin-4 --k 3`

## 6. Árvore completa

<details><summary>38 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 139 | 1 | entrada | programa | ao_vivo | 2026-11-01T14:12:08 | caso sin-4 |
| 140 | 2 | acao | programa | ao_vivo | 2026-11-01T14:12:09 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 165.8, "falhou": false} |
| 141 | 3 | acao | programa | ao_vivo | 2026-11-01T14:12:09 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 7.8, "falhou": false} |
| 142 | 4 | acao | programa | ao_vivo | 2026-11-01T14:12:09 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 3.6, "falhou": false} |
| 143 | 5 | acao | programa | ao_vivo | 2026-11-01T14:12:09 | {"passo": 4, "acao": "clicar", "seletor": "#produtos-api-grid .saiba-mais[data-id='1']", "url": null, "tempo_ms": 35.9, "falhou": false} |
| 144 | 6 | acao | programa | ao_vivo | 2026-11-01T14:12:09 | {"passo": 5, "acao": "esperar", "seletor": "#modalDetalhe", "url": null, "tempo_ms": 226.8, "falhou": false} |
| 145 | 7 | acao | programa | ao_vivo | 2026-11-01T14:12:09 | {"passo": 6, "acao": "conferir", "seletor": "#modalDetalheTitulo", "url": null, "tempo_ms": 5.0, "falhou": false} |
| 146 | 8 | acao | programa | ao_vivo | 2026-11-01T14:12:09 | {"passo": 7, "acao": "conferir", "seletor": "#modalDetalheCorpo", "url": null, "tempo_ms": 5.5, "falhou": false} |
| 147 | 9 | interceptacao | programa | ao_vivo | 2026-11-01T14:12:09 | GET /api/produtos 200 |
| 149 | 10 | interceptacao | programa | ao_vivo | 2026-11-01T14:12:09 | GET /api/produtos/1 200 |
| 150 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T14:12:09 | conferencia_do_roteiro: confere |
| 151 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T14:12:09 | conferencia_do_roteiro: confere |
| 152 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T14:12:09 | conferencia_do_roteiro: confere |
| 154 | 14 | poda | programa | ao_vivo | 2026-11-01T14:12:09 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 156 | 15 | poda | programa | ao_vivo | 2026-11-01T14:12:09 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 157 | 16 | candidatos | programa | ao_vivo | 2026-11-01T14:12:09 | 3 de 40 verbetes entregues |
| 159 | 17 | prompt | programa | ao_vivo | 2026-11-01T14:12:09 | {"etapa": "diagnostico", "sha": "4814aed277f9c42b", "prompt_sha256": "4814aed277f9", "chars": 5944, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 161 | 18 | inferencia | programa | ao_vivo | 2026-11-01T14:12:09 | diagnostico: 81,3 s |
| 162 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T14:12:09 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 163 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T14:12:09 | campo: `nenhum` |
| 164 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T14:12:09 | impacto: `A tela exibe informações incompletas, mostrando dois elementos a menos e adicionando dois elementos não esperados.` |
| 165 | 22 | declaracao | modelo | ao_vivo | 2026-11-01T14:12:09 | fonte: `[contrato-produto] [colecao_no_lugar_de_objeto]` |
| 166 | 23 | declaracao | modelo | ao_vivo | 2026-11-01T14:12:09 | fonte_citada: `contrato-produto` |
| 167 | 24 | declaracao | modelo | ao_vivo | 2026-11-01T14:12:09 | fonte_citada: `colecao_no_lugar_de_objeto` |
| 168 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T14:12:09 | quatro_linhas_presentes: confere |
| 169 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T14:12:09 | rotulo_no_conjunto: confere |
| 170 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T14:12:09 | fonte_existe_na_biblioteca: confere |
| 171 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T14:12:09 | fonte_existe_na_biblioteca: confere |
| 172 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T14:12:09 | fonte_estava_no_contexto: confere |
| 173 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T14:12:09 | fonte_estava_no_contexto: confere |
| 174 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T14:12:09 | campo_existe_no_caso: nao_se_aplica |
| 175 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T14:12:09 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 176 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T14:12:09 | notas_nos_verbetes_citados: informativo |
| 177 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T14:12:09 | impacto: nao_verificavel |
| 178 | 35 | verificacao | verificacao | ao_vivo | 2026-11-01T14:12:09 | fonte_formato_valido: confere |
| 179 | 36 | verificacao | verificacao | ao_vivo | 2026-11-01T14:12:09 | fonte_contem_termo_da_causa: nao_confere |
| 180 | 37 | verificacao | verificacao | ao_vivo | 2026-11-01T14:12:09 | fonte_contem_termo_da_causa: confere |
| 181 | 38 | decisao | programa | ao_vivo | 2026-11-01T14:12:09 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 181, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 156 (sinal_em_codigo), evento 154 (arvore_podada), evento 149 (corpo_http), evento 157 (verbete_entregue, entidade-produto), evento 157 (verbete_entregue, contrato-produto), evento 157 (verbete_entregue, colecao_no_lugar_de_objeto), evento 161 (resposta), evento 166 (verbete_citado, contrato-produto), evento 167 (verbete_citado, colecao_no_lugar_de_objeto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, colecao_no_lugar_de_objeto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 139 a 181 da trilha; hash dos eventos deste caso: `8d784a48a83ae000`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
