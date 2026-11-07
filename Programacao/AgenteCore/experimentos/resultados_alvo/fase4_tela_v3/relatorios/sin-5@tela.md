<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-5`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/sin-5@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `resumo` · selo de probabilidade: **medio** (p = 0,95)

**IMPACTO (declarado):** `O usuário vê um formulário com campos incompletos, particularmente faltando resumos para os produtos, o que pode causar confusão e dificuldade na compreensão dos itens.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo resumo porque o sinal resumo: esperado texto|nulo, recebido None está presente na resposta HTTP e os verbetes contrato-produto, campo_ausente, entidade-produto estavam entre os entregues ao modelo. A segunda causa, chave_de_juncao_errada, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 202): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 36}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 0 linha(s) novas |

Trecho podado (hash `9495b7027e2ca610`):

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
      text "destaque: Sim"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
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

Poda de `corpo_http` (evento 204): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 1469}, depois {"chars": 23}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| resumo | texto\|nulo |  |

Trecho podado (hash `bf2c928ea082e96f`):

```text
{"resumo": "(ausente)"}
```

Interceptação (evento 197): `GET /api/produtos` status 200; corpo `b14075dd059f6770`, árvore `None`.

## 3. Contraste com a segunda causa

campo_ausente e não chave_de_juncao_errada: a escolha tem probabilidade 0,95 contra 0,00; verbete(s) na evidência: contrato-produto, campo_ausente, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 0,95 | sim |
| chave_de_juncao_errada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| campo_renomeado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente]`; verbetes citados: `campo_ausente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `contrato-produto`, `campo_ausente`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `contrato-produto`, `campo_ausente` |
| fonte_formato_valido | `[campo_ausente]` | confere | {"ids": ["campo_ausente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_ausente` | confere | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `resumo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids sin-5 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 190 | 1 | entrada | programa | ao_vivo | 2026-11-05T18:46:40 | caso sin-5 |
| 191 | 2 | acao | programa | ao_vivo | 2026-11-05T18:46:40 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 166.7, "falhou": false} |
| 192 | 3 | acao | programa | ao_vivo | 2026-11-05T18:46:40 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 6.8, "falhou": false} |
| 193 | 4 | acao | programa | ao_vivo | 2026-11-05T18:46:40 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.4, "falhou": false} |
| 194 | 5 | acao | programa | ao_vivo | 2026-11-05T18:46:40 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 4.3, "falhou": false} |
| 195 | 6 | acao | programa | ao_vivo | 2026-11-05T18:46:40 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.7, "falhou": false} |
| 197 | 7 | interceptacao | programa | ao_vivo | 2026-11-05T18:46:40 | GET /api/produtos 200 |
| 198 | 8 | verificacao | verificacao | ao_vivo | 2026-11-05T18:46:40 | conferencia_do_roteiro: confere |
| 199 | 9 | verificacao | verificacao | ao_vivo | 2026-11-05T18:46:40 | conferencia_do_roteiro: confere |
| 200 | 10 | verificacao | verificacao | ao_vivo | 2026-11-05T18:46:40 | conferencia_do_roteiro: confere |
| 202 | 11 | poda | programa | ao_vivo | 2026-11-05T18:46:40 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 204 | 12 | poda | programa | ao_vivo | 2026-11-05T18:46:40 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 205 | 13 | candidatos | programa | ao_vivo | 2026-11-05T18:46:40 | 3 de 39 verbetes entregues |
| 207 | 14 | prompt | programa | ao_vivo | 2026-11-05T18:46:40 | {"etapa": "diagnostico", "sha": "1be120d8c955659b", "prompt_sha256": "1be120d8c955", "chars": 3409, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 209 | 15 | inferencia | programa | ao_vivo | 2026-11-05T18:46:40 | diagnostico: 71,5 s |
| 210 | 16 | declaracao | modelo | ao_vivo | 2026-11-05T18:46:40 | causa_raiz: `campo_ausente` |
| 211 | 17 | declaracao | modelo | ao_vivo | 2026-11-05T18:46:40 | campo: `resumo` |
| 212 | 18 | declaracao | modelo | ao_vivo | 2026-11-05T18:46:40 | impacto: `O usuário vê um formulário com campos incompletos, particularmente faltando resumos para os produtos, o que pode causar confusão e dificuldade na compreensão dos itens.` |
| 213 | 19 | declaracao | modelo | ao_vivo | 2026-11-05T18:46:40 | fonte: `[campo_ausente]` |
| 214 | 20 | declaracao | modelo | ao_vivo | 2026-11-05T18:46:40 | fonte_citada: `campo_ausente` |
| 215 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T18:46:40 | quatro_linhas_presentes: confere |
| 216 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T18:46:40 | rotulo_no_conjunto: confere |
| 217 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T18:46:40 | fonte_existe_na_biblioteca: confere |
| 218 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T18:46:40 | fonte_estava_no_contexto: confere |
| 219 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T18:46:40 | campo_existe_no_caso: confere |
| 220 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T18:46:40 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 221 | 27 | verificacao | verificacao | ao_vivo | 2026-11-05T18:46:40 | notas_nos_verbetes_citados: informativo |
| 222 | 28 | verificacao | verificacao | ao_vivo | 2026-11-05T18:46:40 | impacto: nao_verificavel |
| 223 | 29 | verificacao | verificacao | ao_vivo | 2026-11-05T18:46:40 | fonte_formato_valido: confere |
| 224 | 30 | verificacao | verificacao | ao_vivo | 2026-11-05T18:46:40 | fonte_contem_termo_da_causa: confere |
| 225 | 31 | decisao | programa | ao_vivo | 2026-11-05T18:46:40 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 225, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 204 (sinal_em_codigo), evento 202 (arvore_podada), evento 197 (corpo_http), evento 205 (verbete_entregue, contrato-produto), evento 205 (verbete_entregue, campo_ausente), evento 205 (verbete_entregue, entidade-produto), evento 209 (resposta), evento 214 (verbete_citado, campo_ausente); divergência: não; falha: nenhuma; prov.used: contrato-produto, campo_ausente, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 190 a 225 da trilha; hash dos eventos deste caso: `cfa0b8f6f032ecb7`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
