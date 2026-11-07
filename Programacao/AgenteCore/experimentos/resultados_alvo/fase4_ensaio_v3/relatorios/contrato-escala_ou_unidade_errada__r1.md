<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `contrato-escala_ou_unidade_errada#1`: o que o agente fez, declarou e conferiu

Trilha `fase4_ensaio_v3/qwen2.5_7b/contrato-escala_ou_unidade_errada#1`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `escala_ou_unidade_errada` · **CAMPO:** `preco` · selo de probabilidade: **baixo** (p = 0,52)

**IMPACTO (declarado):** `O usuário vê preços com uma escala errada, exibidos como R$ 8990,00 em vez de R$ 89,90.`

Justificativa (gerada por molde): O agente respondeu escala_ou_unidade_errada no campo preco porque o sinal preco: esperado 89.9 (referência em modo normal), recebido 8990.0 em 14 itens está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,27 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,52); trate como hipótese e confira o campo preco antes de agir.

## 2. Evidência

Poda de `arvore` (evento 165): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `b68e52486de88711`):

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
      button "R$ 8990,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 8490,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "R$ 6990,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 167): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2096}, depois {"chars": 270}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | 89.9 (referência em modo normal) | 8990.0 em 14 itens |

Trecho podado (hash `1cf6e56bcb7be5a1`):

```text
lista com 14 itens (referência em modo normal: 14); preco diferente em 14 itens; por exemplo: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 8990.0, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 160): `GET /api/produtos` status 200; corpo `61ba8740c5fc1841`, árvore `None`.

## 3. Contraste com a segunda causa

escala_ou_unidade_errada e não valor_fora_do_dominio: a escolha tem probabilidade 0,52 contra 0,27; verbete(s) na evidência: entidade-produto, contrato-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| escala_ou_unidade_errada | 0,52 | sim |
| valor_fora_do_dominio | 0,27 |  |
| tipo_divergente | 0,14 |  |
| formato_de_data_divergente | 0,03 |  |
| colecao_no_lugar_de_objeto | 0,02 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `escala_ou_unidade_errada` | confere | verbetes: `entidade-produto` |
| fonte_formato_valido | `[entidade-produto], [contrato-produto]` | confere | {"ids": ["entidade-produto", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "escala_ou_unidade_errada"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "escala_ou_unidade_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v3_reexec --repeticoes 1`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 153 | 1 | entrada | programa | ao_vivo | 2026-11-05T20:02:06 | caso contrato-escala_ou_unidade_errada#1 |
| 154 | 2 | acao | programa | ao_vivo | 2026-11-05T20:02:06 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 97.8, "falhou": false} |
| 155 | 3 | acao | programa | ao_vivo | 2026-11-05T20:02:06 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 9.8, "falhou": false} |
| 156 | 4 | acao | programa | ao_vivo | 2026-11-05T20:02:06 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 1.9, "falhou": false} |
| 157 | 5 | acao | programa | ao_vivo | 2026-11-05T20:02:06 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 3.8, "falhou": false} |
| 158 | 6 | acao | programa | ao_vivo | 2026-11-05T20:02:06 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 4.2, "falhou": false} |
| 160 | 7 | interceptacao | programa | ao_vivo | 2026-11-05T20:02:06 | GET /api/produtos 200 |
| 161 | 8 | verificacao | verificacao | ao_vivo | 2026-11-05T20:02:06 | conferencia_do_roteiro: confere |
| 162 | 9 | verificacao | verificacao | ao_vivo | 2026-11-05T20:02:06 | conferencia_do_roteiro: confere |
| 163 | 10 | verificacao | verificacao | ao_vivo | 2026-11-05T20:02:06 | conferencia_do_roteiro: confere |
| 165 | 11 | poda | programa | ao_vivo | 2026-11-05T20:02:06 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 167 | 12 | poda | programa | ao_vivo | 2026-11-05T20:02:06 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 168 | 13 | candidatos | programa | ao_vivo | 2026-11-05T20:02:06 | 3 de 39 verbetes entregues |
| 170 | 14 | prompt | programa | ao_vivo | 2026-11-05T20:02:06 | {"etapa": "diagnostico", "sha": "b534319be9a34e24", "prompt_sha256": "b534319be9a3", "chars": 4127, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 172 | 15 | inferencia | programa | ao_vivo | 2026-11-05T20:02:06 | diagnostico: 87,5 s |
| 173 | 16 | declaracao | modelo | ao_vivo | 2026-11-05T20:02:06 | causa_raiz: `escala_ou_unidade_errada` |
| 174 | 17 | declaracao | modelo | ao_vivo | 2026-11-05T20:02:06 | campo: `preco` |
| 175 | 18 | declaracao | modelo | ao_vivo | 2026-11-05T20:02:06 | impacto: `O usuário vê preços com uma escala errada, exibidos como R$ 8990,00 em vez de R$ 89,90.` |
| 176 | 19 | declaracao | modelo | ao_vivo | 2026-11-05T20:02:06 | fonte: `[entidade-produto], [contrato-produto]` |
| 177 | 20 | declaracao | modelo | ao_vivo | 2026-11-05T20:02:06 | fonte_citada: `entidade-produto` |
| 178 | 21 | declaracao | modelo | ao_vivo | 2026-11-05T20:02:06 | fonte_citada: `contrato-produto` |
| 179 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T20:02:06 | quatro_linhas_presentes: confere |
| 180 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T20:02:06 | rotulo_no_conjunto: confere |
| 181 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T20:02:06 | fonte_existe_na_biblioteca: confere |
| 182 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T20:02:06 | fonte_existe_na_biblioteca: confere |
| 183 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T20:02:06 | fonte_estava_no_contexto: confere |
| 184 | 27 | verificacao | verificacao | ao_vivo | 2026-11-05T20:02:06 | fonte_estava_no_contexto: confere |
| 185 | 28 | verificacao | verificacao | ao_vivo | 2026-11-05T20:02:06 | campo_existe_no_caso: confere |
| 186 | 29 | verificacao | verificacao | ao_vivo | 2026-11-05T20:02:06 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 187 | 30 | verificacao | verificacao | ao_vivo | 2026-11-05T20:02:06 | notas_nos_verbetes_citados: informativo |
| 188 | 31 | verificacao | verificacao | ao_vivo | 2026-11-05T20:02:06 | impacto: nao_verificavel |
| 189 | 32 | verificacao | verificacao | ao_vivo | 2026-11-05T20:02:06 | fonte_formato_valido: confere |
| 190 | 33 | verificacao | verificacao | ao_vivo | 2026-11-05T20:02:06 | fonte_contem_termo_da_causa: nao_confere |
| 191 | 34 | verificacao | verificacao | ao_vivo | 2026-11-05T20:02:06 | fonte_contem_termo_da_causa: nao_confere |
| 192 | 35 | decisao | programa | ao_vivo | 2026-11-05T20:02:06 | diagnostico: escolha escala_ou_unidade_errada; divergência não |

</details>

Nós de decisão:

- evento 192, `diagnostico`: escolha `escala_ou_unidade_errada`; resultado rotulo_emitido; evidência: evento 167 (sinal_em_codigo), evento 165 (arvore_podada), evento 160 (corpo_http), evento 168 (verbete_entregue, entidade-produto), evento 168 (verbete_entregue, contrato-produto), evento 168 (verbete_entregue, estrutura_aninhada_divergente), evento 172 (resposta), evento 177 (verbete_citado, entidade-produto), evento 178 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 153 a 192 da trilha; hash dos eventos deste caso: `eaec45e2e4fad8c1`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
