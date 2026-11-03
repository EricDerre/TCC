<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-21`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/semt-21@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_renomeado` · **CAMPO:** `nome` · selo de probabilidade: **baixo** (p = 0,48)

**IMPACTO (declarado):** `A tela exibe "Picanha ao Alho (inválido)" em vez do nome correto "Picanha ao Alho", causando confusão para o usuário.`

Justificativa (gerada por molde): O agente respondeu campo_renomeado no campo nome porque o sinal arvore: esperado 3 linha(s) da referência, recebido 3 linha(s) novas está presente na tela e os verbetes entidade-produto, contrato-produto, mensagens-de-erro-do-codigo estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,12. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,48); trate como hipótese e confira o campo nome antes de agir.

## 2. Evidência

Poda de `arvore` (evento 1871): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 1873): regras diff_contra_contrato; antes {"chars": 2222}, depois {"chars": 185}.

Trecho podado (hash `c1a44b87a39d29b5`):

```text
{"id": 1, "nome": "Picanha ao Alho (inválido)", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 1866): `GET /api/produtos` status 200; corpo `29cb154c9a798040`, árvore `None`.

## 3. Contraste com a segunda causa

campo_renomeado e não tipo_divergente: a escolha tem probabilidade 0,48 contra 0,12; verbete(s) na evidência: entidade-produto, contrato-produto, mensagens-de-erro-do-codigo

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_renomeado | 0,48 | sim |
| tipo_divergente | 0,12 |  |
| estrutura_aninhada_divergente | 0,11 |  |
| colecao_no_lugar_de_objeto | 0,10 |  |
| campo_ausente | 0,08 |  |
| formato_de_data_divergente | 0,06 |  |
| corpo_nao_e_json | 0,05 |  |
| corpo_vazio | 0,05 |  |
| resposta_truncada | 0,04 |  |
| valor_fora_do_dominio | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| nulo_inesperado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `mensagens-de-erro-do-codigo` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids semt-21 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1859 | 1 | entrada | programa | ao_vivo | 2026-11-01T12:20:45 | caso semt-21 |
| 1860 | 2 | acao | programa | ao_vivo | 2026-11-01T12:20:45 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 177.6, "falhou": false} |
| 1861 | 3 | acao | programa | ao_vivo | 2026-11-01T12:20:45 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 9.2, "falhou": false} |
| 1862 | 4 | acao | programa | ao_vivo | 2026-11-01T12:20:45 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.4, "falhou": false} |
| 1863 | 5 | acao | programa | ao_vivo | 2026-11-01T12:20:45 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 4.2, "falhou": false} |
| 1864 | 6 | acao | programa | ao_vivo | 2026-11-01T12:20:45 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 4.8, "falhou": false} |
| 1866 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T12:20:45 | GET /api/produtos 200 |
| 1867 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T12:20:45 | conferencia_do_roteiro: confere |
| 1868 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T12:20:45 | conferencia_do_roteiro: confere |
| 1869 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T12:20:45 | conferencia_do_roteiro: confere |
| 1871 | 11 | poda | programa | ao_vivo | 2026-11-01T12:20:45 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1873 | 12 | poda | programa | ao_vivo | 2026-11-01T12:20:45 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1874 | 13 | candidatos | programa | ao_vivo | 2026-11-01T12:20:45 | 3 de 40 verbetes entregues |
| 1876 | 14 | prompt | programa | ao_vivo | 2026-11-01T12:20:45 | {"etapa": "diagnostico", "sha": "843f719e8f00ca88", "prompt_sha256": "843f719e8f00", "chars": 5610, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1878 | 15 | inferencia | programa | ao_vivo | 2026-11-01T12:20:45 | diagnostico: 87,3 s |
| 1879 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T12:20:45 | causa_raiz: `campo_renomeado` |
| 1880 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T12:20:45 | campo: `nome` |
| 1881 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T12:20:45 | impacto: `A tela exibe "Picanha ao Alho (inválido)" em vez do nome correto "Picanha ao Alho", causando confusão para o usuário.` |
| 1882 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T12:20:45 | fonte: `[contrato-produto]` |
| 1883 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T12:20:45 | fonte_citada: `contrato-produto` |
| 1884 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T12:20:45 | quatro_linhas_presentes: confere |
| 1885 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T12:20:45 | rotulo_no_conjunto: confere |
| 1886 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T12:20:45 | fonte_existe_na_biblioteca: confere |
| 1887 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T12:20:45 | fonte_estava_no_contexto: confere |
| 1888 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T12:20:45 | campo_existe_no_caso: confere |
| 1889 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T12:20:45 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1890 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T12:20:45 | notas_nos_verbetes_citados: informativo |
| 1891 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T12:20:45 | impacto: nao_verificavel |
| 1892 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T12:20:45 | fonte_formato_valido: confere |
| 1893 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T12:20:45 | fonte_contem_termo_da_causa: nao_confere |
| 1894 | 31 | decisao | programa | ao_vivo | 2026-11-01T12:20:45 | diagnostico: escolha campo_renomeado; divergência não |

</details>

Nós de decisão:

- evento 1894, `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido; evidência: evento 1873 (sinal_em_codigo), evento 1871 (arvore_podada), evento 1866 (corpo_http), evento 1874 (verbete_entregue, entidade-produto), evento 1874 (verbete_entregue, contrato-produto), evento 1874 (verbete_entregue, mensagens-de-erro-do-codigo), evento 1878 (resposta), evento 1883 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, mensagens-de-erro-do-codigo (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1859 a 1894 da trilha; hash dos eventos deste caso: `8126da84be1aacec`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
