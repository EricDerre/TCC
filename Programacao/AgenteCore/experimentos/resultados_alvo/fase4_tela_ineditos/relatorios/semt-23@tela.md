<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-23`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/semt-23@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `valor_fora_do_dominio` · **CAMPO:** `preco` · selo de probabilidade: **baixo** (p = 0,59)

**IMPACTO (declarado):** `O usuário vê preços negativos na interface, o que é incoerente e pode levar a confusão.`

Justificativa (gerada por molde): O agente respondeu valor_fora_do_dominio no campo preco porque o sinal preco: esperado 89.9 (referência em modo normal), recebido -90.9 em 14 itens está presente na resposta HTTP e os verbetes valor_fora_do_dominio, entidade-produto, fluxo-reserva-e-cancelamento estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,41. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,59); trate como hipótese e confira o campo preco antes de agir.

## 2. Evidência

Poda de `arvore` (evento 806): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `549519a6e88e6100`):

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
      button "R$ -90,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ -85,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "R$ -70,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Poda de `corpo_http` (evento 808): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2082}, depois {"chars": 269}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | 89.9 (referência em modo normal) | -90.9 em 14 itens |

Trecho podado (hash `27ade78311a661e6`):

```text
lista com 14 itens (referência em modo normal: 14); preco diferente em 14 itens; por exemplo: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": -90.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 802): `GET /api/produtos` status 200; corpo `6adc357553572583`, árvore `None`.

## 3. Contraste com a segunda causa

valor_fora_do_dominio e não tipo_divergente: a escolha tem probabilidade 0,59 contra 0,41; verbete(s) na evidência: valor_fora_do_dominio, entidade-produto, fluxo-reserva-e-cancelamento

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| valor_fora_do_dominio | 0,59 | sim |
| tipo_divergente | 0,41 |  |
| formato_de_data_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[valor_fora_do_dominio]`; verbetes citados: `valor_fora_do_dominio`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `valor_fora_do_dominio` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `valor_fora_do_dominio` | confere | contexto: `valor_fora_do_dominio`, `entidade-produto`, `fluxo-reserva-e-cancelamento` |
| Algum verbete do contexto trata da causa respondida | `valor_fora_do_dominio` | confere | verbetes: `valor_fora_do_dominio`, `fluxo-reserva-e-cancelamento` |
| fonte_formato_valido | `[valor_fora_do_dominio]` | confere | {"ids": ["valor_fora_do_dominio"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `valor_fora_do_dominio` | confere | {"termo": "valor_fora_do_dominio"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids semt-23 --k 3`

## 6. Árvore completa

<details><summary>29 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 796 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:56:00 | caso semt-23 |
| 797 | 2 | acao | programa | ao_vivo | 2026-11-06T11:56:00 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 116.1, "falhou": false} |
| 798 | 3 | acao | programa | ao_vivo | 2026-11-06T11:56:00 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 12.2, "falhou": false} |
| 799 | 4 | acao | programa | ao_vivo | 2026-11-06T11:56:00 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.9, "falhou": false} |
| 800 | 5 | acao | programa | ao_vivo | 2026-11-06T11:56:00 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 4.4, "falhou": true} |
| 802 | 6 | interceptacao | programa | ao_vivo | 2026-11-06T11:56:00 | GET /api/produtos 200 |
| 803 | 7 | verificacao | verificacao | ao_vivo | 2026-11-06T11:56:00 | conferencia_do_roteiro: confere |
| 804 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T11:56:00 | conferencia_do_roteiro: nao_confere |
| 806 | 9 | poda | programa | ao_vivo | 2026-11-06T11:56:00 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 808 | 10 | poda | programa | ao_vivo | 2026-11-06T11:56:00 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 809 | 11 | candidatos | programa | ao_vivo | 2026-11-06T11:56:00 | 3 de 39 verbetes entregues |
| 811 | 12 | prompt | programa | ao_vivo | 2026-11-06T11:56:00 | {"etapa": "diagnostico", "sha": "44631837beae202c", "prompt_sha256": "44631837beae", "chars": 3971, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 813 | 13 | inferencia | programa | ao_vivo | 2026-11-06T11:56:00 | diagnostico: 82,4 s |
| 814 | 14 | declaracao | modelo | ao_vivo | 2026-11-06T11:56:00 | causa_raiz: `valor_fora_do_dominio` |
| 815 | 15 | declaracao | modelo | ao_vivo | 2026-11-06T11:56:00 | campo: `preco` |
| 816 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T11:56:00 | impacto: `O usuário vê preços negativos na interface, o que é incoerente e pode levar a confusão.` |
| 817 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T11:56:00 | fonte: `[valor_fora_do_dominio]` |
| 818 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T11:56:00 | fonte_citada: `valor_fora_do_dominio` |
| 819 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:56:00 | quatro_linhas_presentes: confere |
| 820 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T11:56:00 | rotulo_no_conjunto: confere |
| 821 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T11:56:00 | fonte_existe_na_biblioteca: confere |
| 822 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:56:00 | fonte_estava_no_contexto: confere |
| 823 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:56:00 | campo_existe_no_caso: confere |
| 824 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:56:00 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 825 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:56:00 | notas_nos_verbetes_citados: informativo |
| 826 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:56:00 | impacto: nao_verificavel |
| 827 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T11:56:00 | fonte_formato_valido: confere |
| 828 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T11:56:00 | fonte_contem_termo_da_causa: confere |
| 829 | 29 | decisao | programa | ao_vivo | 2026-11-06T11:56:00 | diagnostico: escolha valor_fora_do_dominio; divergência não |

</details>

Nós de decisão:

- evento 829, `diagnostico`: escolha `valor_fora_do_dominio`; resultado rotulo_emitido; evidência: evento 808 (sinal_em_codigo), evento 806 (arvore_podada), evento 802 (corpo_http), evento 809 (verbete_entregue, valor_fora_do_dominio), evento 809 (verbete_entregue, entidade-produto), evento 809 (verbete_entregue, fluxo-reserva-e-cancelamento), evento 813 (resposta), evento 818 (verbete_citado, valor_fora_do_dominio); divergência: não; falha: nenhuma; prov.used: valor_fora_do_dominio, entidade-produto, fluxo-reserva-e-cancelamento (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 796 a 829 da trilha; hash dos eventos deste caso: `e016aed75f1dcb1a`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
