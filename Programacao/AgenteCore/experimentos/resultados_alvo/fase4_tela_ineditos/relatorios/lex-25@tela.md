<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-25`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/lex-25@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nome` · selo de probabilidade: **medio** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê nomes com acentos corrompidos em alguns itens do cardápio.`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta no campo nome porque o sinal nome: esperado "Água Mineral" (referência em modo normal), recebido "Ãgua Mineral" em 3 itens está presente na resposta HTTP e os verbetes codificacao_incorreta, entidade-produto, contrato-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 209): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 45}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 1 linha(s) da referência | 7 linha(s) novas |

Trecho podado (hash `3c6d65355ee53010`):

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
    text "Ã\x81gua Mineral"
    text "Bebidas"
    text "Garrafa 500ml, com ou sem gás"
    text "destaque: Não"
    button "R$ 6,00" class="btn btn-default disable"
    button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="8"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 211): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2071}, depois {"chars": 243}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| nome | "Água Mineral" (referência em modo normal) | "Ãgua Mineral" em 3 itens |

Trecho podado (hash `7fa7e4d45058ea88`):

```text
lista com 14 itens (referência em modo normal: 14); nome diferente em 3 itens; por exemplo: {"id": 8, "nome": "Ãgua Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}
```

Interceptação (evento 204): `GET /api/produtos` status 200; corpo `0fd45da79aa14f8a`, árvore `None`.

## 3. Contraste com a segunda causa

codificacao_incorreta e não tipo_divergente: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: codificacao_incorreta, entidade-produto, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 0,99 | sim |
| tipo_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| resposta_truncada | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[codificacao_incorreta] [entidade-produto]`; verbetes citados: `codificacao_incorreta`, `entidade-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `codificacao_incorreta` | confere |  |
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `codificacao_incorreta` | confere | contexto: `codificacao_incorreta`, `entidade-produto`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `codificacao_incorreta`, `entidade-produto`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | confere | verbetes: `codificacao_incorreta` |
| fonte_formato_valido | `[codificacao_incorreta] [entidade-produto]` | confere | {"ids": ["codificacao_incorreta", "entidade-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `codificacao_incorreta` | confere | {"termo": "codificacao_incorreta"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids lex-25 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 197 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:35:42 | caso lex-25 |
| 198 | 2 | acao | programa | ao_vivo | 2026-11-06T11:35:42 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 111.3, "falhou": false} |
| 199 | 3 | acao | programa | ao_vivo | 2026-11-06T11:35:42 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 7.6, "falhou": false} |
| 200 | 4 | acao | programa | ao_vivo | 2026-11-06T11:35:42 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.2, "falhou": false} |
| 201 | 5 | acao | programa | ao_vivo | 2026-11-06T11:35:42 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 8.4, "falhou": false} |
| 202 | 6 | acao | programa | ao_vivo | 2026-11-06T11:35:42 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 2.8, "falhou": false} |
| 204 | 7 | interceptacao | programa | ao_vivo | 2026-11-06T11:35:42 | GET /api/produtos 200 |
| 205 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T11:35:42 | conferencia_do_roteiro: confere |
| 206 | 9 | verificacao | verificacao | ao_vivo | 2026-11-06T11:35:42 | conferencia_do_roteiro: confere |
| 207 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:35:42 | conferencia_do_roteiro: confere |
| 209 | 11 | poda | programa | ao_vivo | 2026-11-06T11:35:42 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 211 | 12 | poda | programa | ao_vivo | 2026-11-06T11:35:42 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 212 | 13 | candidatos | programa | ao_vivo | 2026-11-06T11:35:42 | 3 de 39 verbetes entregues |
| 214 | 14 | prompt | programa | ao_vivo | 2026-11-06T11:35:42 | {"etapa": "diagnostico", "sha": "c927f5b54cbe7a76", "prompt_sha256": "c927f5b54cbe", "chars": 3807, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 216 | 15 | inferencia | programa | ao_vivo | 2026-11-06T11:35:42 | diagnostico: 47,8 s |
| 217 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T11:35:42 | causa_raiz: `codificacao_incorreta` |
| 218 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T11:35:42 | campo: `nome` |
| 219 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T11:35:42 | impacto: `O usuário vê nomes com acentos corrompidos em alguns itens do cardápio.` |
| 220 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T11:35:42 | fonte: `[codificacao_incorreta] [entidade-produto]` |
| 221 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T11:35:42 | fonte_citada: `codificacao_incorreta` |
| 222 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T11:35:42 | fonte_citada: `entidade-produto` |
| 223 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:35:42 | quatro_linhas_presentes: confere |
| 224 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:35:42 | rotulo_no_conjunto: confere |
| 225 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:35:42 | fonte_existe_na_biblioteca: confere |
| 226 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:35:42 | fonte_existe_na_biblioteca: confere |
| 227 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:35:42 | fonte_estava_no_contexto: confere |
| 228 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T11:35:42 | fonte_estava_no_contexto: confere |
| 229 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T11:35:42 | campo_existe_no_caso: confere |
| 230 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T11:35:42 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 231 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T11:35:42 | notas_nos_verbetes_citados: informativo |
| 232 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T11:35:42 | impacto: nao_verificavel |
| 233 | 32 | verificacao | verificacao | ao_vivo | 2026-11-06T11:35:42 | fonte_formato_valido: confere |
| 234 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T11:35:42 | fonte_contem_termo_da_causa: confere |
| 235 | 34 | verificacao | verificacao | ao_vivo | 2026-11-06T11:35:42 | fonte_contem_termo_da_causa: nao_confere |
| 236 | 35 | decisao | programa | ao_vivo | 2026-11-06T11:35:42 | diagnostico: escolha codificacao_incorreta; divergência não |

</details>

Nós de decisão:

- evento 236, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 211 (sinal_em_codigo), evento 209 (arvore_podada), evento 204 (corpo_http), evento 212 (verbete_entregue, codificacao_incorreta), evento 212 (verbete_entregue, entidade-produto), evento 212 (verbete_entregue, contrato-produto), evento 216 (resposta), evento 221 (verbete_citado, codificacao_incorreta), evento 222 (verbete_citado, entidade-produto); divergência: não; falha: nenhuma; prov.used: codificacao_incorreta, entidade-produto, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 197 a 236 da trilha; hash dos eventos deste caso: `ce66dd49deded125`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
