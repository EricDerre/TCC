<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-14`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/semt-14@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `nulo_inesperado` · **CAMPO:** `tipo` · selo de probabilidade: **medio** (p = 0,96)

**IMPACTO (declarado):** `O usuário vê campos tipo mostrando "null", o que não é esperado e causa confusão.`

Justificativa (gerada por molde): O agente respondeu nulo_inesperado no campo tipo porque o sinal tipo: esperado texto, recebido nulo está presente na resposta HTTP e os verbetes campo_ausente, nulo_inesperado, contrato-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,04. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1136): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `e7c1f4f1e98ba28c`):

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
      text "null"
      text "Picanha grelhada com alho laminado na brasa"
      text "destaque: Sim"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "null"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "null"
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

Poda de `corpo_http` (evento 1138): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 1978}, depois {"chars": 14}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tipo | texto | nulo |
| tipo | "Carnes" (referência em modo normal) | null em 14 itens |

Trecho podado (hash `0576cabdd6693e35`):

```text
{"tipo": null}
```

Interceptação (evento 1131): `GET /api/produtos` status 200; corpo `01c141f88accbf65`, árvore `None`.

## 3. Contraste com a segunda causa

nulo_inesperado e não tipo_divergente: a escolha tem probabilidade 0,96 contra 0,04; verbete(s) na evidência: campo_ausente, nulo_inesperado, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| nulo_inesperado | 0,96 | sim |
| tipo_divergente | 0,04 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[nulo_inesperado]`; verbetes citados: `nulo_inesperado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `campo_ausente`, `nulo_inesperado`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `campo_ausente`, `nulo_inesperado` |
| fonte_formato_valido | `[nulo_inesperado]` | confere | {"ids": ["nulo_inesperado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids semt-14 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1124 | 1 | entrada | programa | ao_vivo | 2026-11-01T14:52:06 | caso semt-14 |
| 1125 | 2 | acao | programa | ao_vivo | 2026-11-01T14:52:07 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 177.7, "falhou": false} |
| 1126 | 3 | acao | programa | ao_vivo | 2026-11-01T14:52:07 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 8.2, "falhou": false} |
| 1127 | 4 | acao | programa | ao_vivo | 2026-11-01T14:52:07 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 3.3, "falhou": false} |
| 1128 | 5 | acao | programa | ao_vivo | 2026-11-01T14:52:07 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 6.5, "falhou": false} |
| 1129 | 6 | acao | programa | ao_vivo | 2026-11-01T14:52:07 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 4.4, "falhou": false} |
| 1131 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T14:52:07 | GET /api/produtos 200 |
| 1132 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T14:52:07 | conferencia_do_roteiro: confere |
| 1133 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T14:52:07 | conferencia_do_roteiro: confere |
| 1134 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T14:52:07 | conferencia_do_roteiro: confere |
| 1136 | 11 | poda | programa | ao_vivo | 2026-11-01T14:52:07 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1138 | 12 | poda | programa | ao_vivo | 2026-11-01T14:52:07 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1139 | 13 | candidatos | programa | ao_vivo | 2026-11-01T14:52:07 | 3 de 40 verbetes entregues |
| 1141 | 14 | prompt | programa | ao_vivo | 2026-11-01T14:52:07 | {"etapa": "diagnostico", "sha": "81e8a9f1b5ba70c6", "prompt_sha256": "81e8a9f1b5ba", "chars": 5297, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1143 | 15 | inferencia | programa | ao_vivo | 2026-11-01T14:52:07 | diagnostico: 62,6 s |
| 1144 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T14:52:07 | causa_raiz: `nulo_inesperado` |
| 1145 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T14:52:07 | campo: `tipo` |
| 1146 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T14:52:07 | impacto: `O usuário vê campos tipo mostrando "null", o que não é esperado e causa confusão.` |
| 1147 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T14:52:07 | fonte: `[nulo_inesperado]` |
| 1148 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T14:52:07 | fonte_citada: `nulo_inesperado` |
| 1149 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T14:52:07 | quatro_linhas_presentes: confere |
| 1150 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T14:52:07 | rotulo_no_conjunto: confere |
| 1151 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T14:52:07 | fonte_existe_na_biblioteca: confere |
| 1152 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T14:52:07 | fonte_estava_no_contexto: confere |
| 1153 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T14:52:07 | campo_existe_no_caso: confere |
| 1154 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T14:52:07 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1155 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T14:52:07 | notas_nos_verbetes_citados: informativo |
| 1156 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T14:52:07 | impacto: nao_verificavel |
| 1157 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T14:52:07 | fonte_formato_valido: confere |
| 1158 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T14:52:07 | fonte_contem_termo_da_causa: confere |
| 1159 | 31 | decisao | programa | ao_vivo | 2026-11-01T14:52:07 | diagnostico: escolha nulo_inesperado; divergência não |

</details>

Nós de decisão:

- evento 1159, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 1138 (sinal_em_codigo), evento 1136 (arvore_podada), evento 1131 (corpo_http), evento 1139 (verbete_entregue, campo_ausente), evento 1139 (verbete_entregue, nulo_inesperado), evento 1139 (verbete_entregue, contrato-produto), evento 1143 (resposta), evento 1148 (verbete_citado, nulo_inesperado); divergência: não; falha: nenhuma; prov.used: campo_ausente, nulo_inesperado, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1124 a 1159 da trilha; hash dos eventos deste caso: `121874fd436b73a6`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
