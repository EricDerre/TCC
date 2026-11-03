<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-21`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/tra-21@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `contagem_inconsistente` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,96)

**IMPACTO (declarado):** `O usuário vê uma lista com um produto a menos, o que pode causar confusão sobre o conteúdo disponível.`

Justificativa (gerada por molde): O agente respondeu contagem_inconsistente no campo itens porque o sinal itens: esperado 14 itens (referência em modo normal), recebido falta o id 14 ("Abacaxi na Brasa") está presente na resposta HTTP e os verbetes entidade-produto, contagem_inconsistente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,02 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 2129): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 183}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 2130): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 1928}, depois {"chars": 277}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| itens | 14 itens (referência em modo normal) | falta o id 14 ("Abacaxi na Brasa") |

Trecho podado (hash `9675592a8385ee52`):

```text
lista com 13 itens (referência em modo normal: 14); falta o id 14 ("Abacaxi na Brasa"); primeiro item: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 2127): `GET /api/produtos` status 200; corpo `4f6d409f5a92ce2d`, árvore `None`.

## 3. Contraste com a segunda causa

contagem_inconsistente e não resposta_truncada: a escolha tem probabilidade 0,96 contra 0,02; verbete(s) na evidência: entidade-produto, contagem_inconsistente, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| contagem_inconsistente | 0,96 | sim |
| resposta_truncada | 0,02 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contagem_inconsistente]`; verbetes citados: `contagem_inconsistente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `entidade-produto`, `contagem_inconsistente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `contagem_inconsistente` | confere | verbetes: `contagem_inconsistente` |
| fonte_formato_valido | `[contagem_inconsistente]` | confere | {"ids": ["contagem_inconsistente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contagem_inconsistente` | confere | {"termo": "contagem_inconsistente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids tra-21 --k 3`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2123 | 1 | entrada | programa | ao_vivo | 2026-11-01T15:27:52 | caso tra-21 |
| 2124 | 2 | acao | programa | ao_vivo | 2026-11-01T15:27:52 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 106.8, "falhou": false} |
| 2125 | 3 | acao | programa | ao_vivo | 2026-11-01T15:27:52 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 6.6, "falhou": false} |
| 2126 | 4 | acao | programa | ao_vivo | 2026-11-01T15:27:52 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.3, "falhou": true} |
| 2127 | 5 | interceptacao | programa | ao_vivo | 2026-11-01T15:27:52 | GET /api/produtos 200 |
| 2128 | 6 | verificacao | verificacao | ao_vivo | 2026-11-01T15:27:52 | conferencia_do_roteiro: nao_confere |
| 2129 | 7 | poda | programa | ao_vivo | 2026-11-01T15:27:52 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 2130 | 8 | poda | programa | ao_vivo | 2026-11-01T15:27:52 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 2131 | 9 | candidatos | programa | ao_vivo | 2026-11-01T15:27:52 | 3 de 40 verbetes entregues |
| 2133 | 10 | prompt | programa | ao_vivo | 2026-11-01T15:27:52 | {"etapa": "diagnostico", "sha": "f7330460404cc9a0", "prompt_sha256": "f7330460404c", "chars": 5702, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2135 | 11 | inferencia | programa | ao_vivo | 2026-11-01T15:27:52 | diagnostico: 92,4 s |
| 2136 | 12 | declaracao | modelo | ao_vivo | 2026-11-01T15:27:52 | causa_raiz: `contagem_inconsistente` |
| 2137 | 13 | declaracao | modelo | ao_vivo | 2026-11-01T15:27:52 | campo: `nenhum` |
| 2138 | 14 | declaracao | modelo | ao_vivo | 2026-11-01T15:27:52 | impacto: `O usuário vê uma lista com um produto a menos, o que pode causar confusão sobre o conteúdo disponível.` |
| 2139 | 15 | declaracao | modelo | ao_vivo | 2026-11-01T15:27:52 | fonte: `[contagem_inconsistente]` |
| 2140 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T15:27:52 | fonte_citada: `contagem_inconsistente` |
| 2141 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T15:27:52 | quatro_linhas_presentes: confere |
| 2142 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T15:27:52 | rotulo_no_conjunto: confere |
| 2143 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T15:27:52 | fonte_existe_na_biblioteca: confere |
| 2144 | 20 | verificacao | verificacao | ao_vivo | 2026-11-01T15:27:52 | fonte_estava_no_contexto: confere |
| 2145 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T15:27:52 | campo_existe_no_caso: nao_se_aplica |
| 2146 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T15:27:52 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2147 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T15:27:52 | notas_nos_verbetes_citados: informativo |
| 2148 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T15:27:52 | impacto: nao_verificavel |
| 2149 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T15:27:52 | fonte_formato_valido: confere |
| 2150 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T15:27:52 | fonte_contem_termo_da_causa: confere |
| 2151 | 27 | decisao | programa | ao_vivo | 2026-11-01T15:27:52 | diagnostico: escolha contagem_inconsistente; divergência não |

</details>

Nós de decisão:

- evento 2151, `diagnostico`: escolha `contagem_inconsistente`; resultado rotulo_emitido; evidência: evento 2130 (sinal_em_codigo), evento 2129 (arvore_podada), evento 2127 (corpo_http), evento 2131 (verbete_entregue, entidade-produto), evento 2131 (verbete_entregue, contagem_inconsistente), evento 2131 (verbete_entregue, contrato-produto), evento 2135 (resposta), evento 2140 (verbete_citado, contagem_inconsistente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contagem_inconsistente, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2123 a 2151 da trilha; hash dos eventos deste caso: `f33df80ee7b039f4`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
