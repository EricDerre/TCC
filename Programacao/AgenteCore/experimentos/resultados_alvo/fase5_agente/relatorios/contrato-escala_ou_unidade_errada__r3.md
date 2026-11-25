<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `contrato-escala_ou_unidade_errada#3`: o que o agente fez, declarou e conferiu

Trilha `fase5_agente/qwen2.5_7b/contrato-escala_ou_unidade_errada#3`; modelo `qwen2.5:7b`, Ollama 0.40.16, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `escala_ou_unidade_errada` · **CAMPO:** `preco` · selo de probabilidade: **medio** (p = 0,98)

**IMPACTO (declarado):** `O usuário vê preços com escalas incorretas, como R$ 8990,00 em vez de R$ 89,90.`

Justificativa (gerada por molde): O agente respondeu escala_ou_unidade_errada no campo preco porque o sinal preco: esperado 89.9 (referência em modo normal), recebido 8990.0 em 14 itens está presente na resposta HTTP e os verbetes escala_ou_unidade_errada, entidade-produto, tempo_de_resposta_excedido estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 947): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 948): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2096}, depois {"chars": 270}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | 89.9 (referência em modo normal) | 8990.0 em 14 itens |

Trecho podado (hash `1cf6e56bcb7be5a1`):

```text
lista com 14 itens (referência em modo normal: 14); preco diferente em 14 itens; por exemplo: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 8990.0, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 943): `GET /api/produtos` status 200; corpo `61ba8740c5fc1841`, árvore `None`.

## 3. Contraste com a segunda causa

escala_ou_unidade_errada e não tipo_divergente: a escolha tem probabilidade 0,98 contra 0,00; verbete(s) na evidência: escala_ou_unidade_errada, entidade-produto, tempo_de_resposta_excedido

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| escala_ou_unidade_errada | 0,98 | sim |
| tipo_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[escala_ou_unidade_errada]`; verbetes citados: `escala_ou_unidade_errada`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `escala_ou_unidade_errada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `escala_ou_unidade_errada` | confere | contexto: `escala_ou_unidade_errada`, `entidade-produto`, `tempo_de_resposta_excedido` |
| Algum verbete do contexto trata da causa respondida | `escala_ou_unidade_errada` | confere | verbetes: `escala_ou_unidade_errada`, `entidade-produto` |
| fonte_formato_valido | `[escala_ou_unidade_errada]` | confere | {"ids": ["escala_ou_unidade_errada"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `escala_ou_unidade_errada` | confere | {"termo": "escala_ou_unidade_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase5_agente_reexec --repeticoes 1`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 937 | 1 | entrada | programa | ao_vivo | 2026-11-18T19:05:07 | caso contrato-escala_ou_unidade_errada#3 |
| 938 | 2 | acao | programa | ao_vivo | 2026-11-18T19:05:07 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 158.5, "falhou": false} |
| 939 | 3 | acao | programa | ao_vivo | 2026-11-18T19:05:07 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 5.9, "falhou": false} |
| 940 | 4 | acao | programa | ao_vivo | 2026-11-18T19:05:07 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.2, "falhou": false} |
| 941 | 5 | acao | programa | ao_vivo | 2026-11-18T19:05:07 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 4.0, "falhou": false} |
| 942 | 6 | acao | programa | ao_vivo | 2026-11-18T19:05:07 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.7, "falhou": false} |
| 943 | 7 | interceptacao | programa | ao_vivo | 2026-11-18T19:05:07 | GET /api/produtos 200 |
| 944 | 8 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:07 | conferencia_do_roteiro: confere |
| 945 | 9 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:07 | conferencia_do_roteiro: confere |
| 946 | 10 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:07 | conferencia_do_roteiro: confere |
| 947 | 11 | poda | programa | ao_vivo | 2026-11-18T19:05:07 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 948 | 12 | poda | programa | ao_vivo | 2026-11-18T19:05:07 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 949 | 13 | candidatos | programa | ao_vivo | 2026-11-18T19:05:07 | 3 de 39 verbetes entregues |
| 950 | 14 | prompt | programa | ao_vivo | 2026-11-18T19:05:07 | {"etapa": "diagnostico", "sha": "102f2cfb35726923", "prompt_sha256": "102f2cfb3572", "chars": 4196, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 952 | 15 | inferencia | programa | ao_vivo | 2026-11-18T19:05:07 | diagnostico: 19,1 s |
| 953 | 16 | declaracao | modelo | ao_vivo | 2026-11-18T19:05:07 | causa_raiz: `escala_ou_unidade_errada` |
| 954 | 17 | declaracao | modelo | ao_vivo | 2026-11-18T19:05:07 | campo: `preco` |
| 955 | 18 | declaracao | modelo | ao_vivo | 2026-11-18T19:05:07 | impacto: `O usuário vê preços com escalas incorretas, como R$ 8990,00 em vez de R$ 89,90.` |
| 956 | 19 | declaracao | modelo | ao_vivo | 2026-11-18T19:05:07 | fonte: `[escala_ou_unidade_errada]` |
| 957 | 20 | declaracao | modelo | ao_vivo | 2026-11-18T19:05:07 | fonte_citada: `escala_ou_unidade_errada` |
| 958 | 21 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:07 | quatro_linhas_presentes: confere |
| 959 | 22 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:07 | rotulo_no_conjunto: confere |
| 960 | 23 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:07 | fonte_existe_na_biblioteca: confere |
| 961 | 24 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:07 | fonte_estava_no_contexto: confere |
| 962 | 25 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:07 | campo_existe_no_caso: confere |
| 963 | 26 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:07 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 964 | 27 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:07 | notas_nos_verbetes_citados: informativo |
| 965 | 28 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:07 | impacto: nao_verificavel |
| 966 | 29 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:07 | fonte_formato_valido: confere |
| 967 | 30 | verificacao | verificacao | ao_vivo | 2026-11-18T19:05:07 | fonte_contem_termo_da_causa: confere |
| 968 | 31 | decisao | programa | ao_vivo | 2026-11-18T19:05:07 | diagnostico: escolha escala_ou_unidade_errada; divergência não |

</details>

Nós de decisão:

- evento 968, `diagnostico`: escolha `escala_ou_unidade_errada`; resultado rotulo_emitido; evidência: evento 948 (sinal_em_codigo), evento 947 (arvore_podada), evento 943 (corpo_http), evento 949 (verbete_entregue, escala_ou_unidade_errada), evento 949 (verbete_entregue, entidade-produto), evento 949 (verbete_entregue, tempo_de_resposta_excedido), evento 952 (resposta), evento 957 (verbete_citado, escala_ou_unidade_errada); divergência: não; falha: nenhuma; prov.used: escala_ou_unidade_errada, entidade-produto, tempo_de_resposta_excedido (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 937 a 968 da trilha; hash dos eventos deste caso: `6fa20c38b45a9ce9`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
