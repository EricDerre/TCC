<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-21`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/semt-21@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_renomeado` · **CAMPO:** `nome` · selo de probabilidade: **baixo** (p = 0,76)

**IMPACTO (declarado):** `O usuário vê nomes incorretos na interface, com a adição de "(inválido)" em todos os produtos.`

Justificativa (gerada por molde): O agente respondeu campo_renomeado no campo nome porque o sinal nome: esperado "Picanha ao Alho" (referência em modo normal), recebido "Picanha ao Alho (inválido)" em 14 itens está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, estrutura_aninhada_divergente estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,21. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,76); trate como hipótese e confira o campo nome antes de agir.

## 2. Evidência

Poda de `arvore` (evento 1813): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `769513c6cbb48e95`):

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
      heading "Picanha ao Alho (inválido)" level=3
      text "Carnes"
      text "Picanha grelhada com alho laminado na brasa"
      text "destaque: Sim"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples (inválido)" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha (inválido)" level=3
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

```

Poda de `corpo_http` (evento 1815): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2222}, depois {"chars": 278}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| nome | "Picanha ao Alho" (referência em modo normal) | "Picanha ao Alho (inválido)" em 14 itens |

Trecho podado (hash `f1b7bc81a1c9c347`):

```text
lista com 14 itens (referência em modo normal: 14); nome diferente em 14 itens; por exemplo: {"id": 1, "nome": "Picanha ao Alho (inválido)", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 1808): `GET /api/produtos` status 200; corpo `29cb154c9a798040`, árvore `None`.

## 3. Contraste com a segunda causa

campo_renomeado e não estrutura_aninhada_divergente: a escolha tem probabilidade 0,76 contra 0,21; verbete(s) na evidência: entidade-produto, contrato-produto, estrutura_aninhada_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_renomeado | 0,76 | sim |
| estrutura_aninhada_divergente | 0,21 |  |
| campo_ausente | 0,01 |  |
| tipo_divergente | 0,01 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `estrutura_aninhada_divergente` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `contrato-produto`, `estrutura_aninhada_divergente` |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids semt-21 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1801 | 1 | entrada | programa | ao_vivo | 2026-11-05T19:43:10 | caso semt-21 |
| 1802 | 2 | acao | programa | ao_vivo | 2026-11-05T19:43:10 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 105.2, "falhou": false} |
| 1803 | 3 | acao | programa | ao_vivo | 2026-11-05T19:43:10 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 8.0, "falhou": false} |
| 1804 | 4 | acao | programa | ao_vivo | 2026-11-05T19:43:10 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.5, "falhou": false} |
| 1805 | 5 | acao | programa | ao_vivo | 2026-11-05T19:43:10 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 3.6, "falhou": false} |
| 1806 | 6 | acao | programa | ao_vivo | 2026-11-05T19:43:10 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 2.9, "falhou": false} |
| 1808 | 7 | interceptacao | programa | ao_vivo | 2026-11-05T19:43:10 | GET /api/produtos 200 |
| 1809 | 8 | verificacao | verificacao | ao_vivo | 2026-11-05T19:43:10 | conferencia_do_roteiro: confere |
| 1810 | 9 | verificacao | verificacao | ao_vivo | 2026-11-05T19:43:10 | conferencia_do_roteiro: confere |
| 1811 | 10 | verificacao | verificacao | ao_vivo | 2026-11-05T19:43:10 | conferencia_do_roteiro: confere |
| 1813 | 11 | poda | programa | ao_vivo | 2026-11-05T19:43:10 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1815 | 12 | poda | programa | ao_vivo | 2026-11-05T19:43:10 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1816 | 13 | candidatos | programa | ao_vivo | 2026-11-05T19:43:10 | 3 de 39 verbetes entregues |
| 1818 | 14 | prompt | programa | ao_vivo | 2026-11-05T19:43:10 | {"etapa": "diagnostico", "sha": "d718fc1a8b4bdc32", "prompt_sha256": "d718fc1a8b4b", "chars": 4142, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1820 | 15 | inferencia | programa | ao_vivo | 2026-11-05T19:43:10 | diagnostico: 44,0 s |
| 1821 | 16 | declaracao | modelo | ao_vivo | 2026-11-05T19:43:10 | causa_raiz: `campo_renomeado` |
| 1822 | 17 | declaracao | modelo | ao_vivo | 2026-11-05T19:43:10 | campo: `nome` |
| 1823 | 18 | declaracao | modelo | ao_vivo | 2026-11-05T19:43:10 | impacto: `O usuário vê nomes incorretos na interface, com a adição de "(inválido)" em todos os produtos.` |
| 1824 | 19 | declaracao | modelo | ao_vivo | 2026-11-05T19:43:10 | fonte: `[contrato-produto]` |
| 1825 | 20 | declaracao | modelo | ao_vivo | 2026-11-05T19:43:10 | fonte_citada: `contrato-produto` |
| 1826 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T19:43:10 | quatro_linhas_presentes: confere |
| 1827 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T19:43:10 | rotulo_no_conjunto: confere |
| 1828 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T19:43:10 | fonte_existe_na_biblioteca: confere |
| 1829 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T19:43:10 | fonte_estava_no_contexto: confere |
| 1830 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T19:43:10 | campo_existe_no_caso: confere |
| 1831 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T19:43:10 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1832 | 27 | verificacao | verificacao | ao_vivo | 2026-11-05T19:43:10 | notas_nos_verbetes_citados: informativo |
| 1833 | 28 | verificacao | verificacao | ao_vivo | 2026-11-05T19:43:10 | impacto: nao_verificavel |
| 1834 | 29 | verificacao | verificacao | ao_vivo | 2026-11-05T19:43:10 | fonte_formato_valido: confere |
| 1835 | 30 | verificacao | verificacao | ao_vivo | 2026-11-05T19:43:10 | fonte_contem_termo_da_causa: nao_confere |
| 1836 | 31 | decisao | programa | ao_vivo | 2026-11-05T19:43:10 | diagnostico: escolha campo_renomeado; divergência não |

</details>

Nós de decisão:

- evento 1836, `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido; evidência: evento 1815 (sinal_em_codigo), evento 1813 (arvore_podada), evento 1808 (corpo_http), evento 1816 (verbete_entregue, entidade-produto), evento 1816 (verbete_entregue, contrato-produto), evento 1816 (verbete_entregue, estrutura_aninhada_divergente), evento 1820 (resposta), evento 1825 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, estrutura_aninhada_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1801 a 1836 da trilha; hash dos eventos deste caso: `9c02a1f55fb91e92`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
