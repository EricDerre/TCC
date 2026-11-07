<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-17`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v4/qwen2.5_7b/tra-17@tela`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `chave_de_juncao_errada` · **CAMPO:** `tipo` · selo de probabilidade: **alto** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê categorias incorretas atribuídas aos produtos, como "Bebidas" em vez de "Carnes".`

Justificativa (gerada por molde): O agente respondeu chave_de_juncao_errada no campo tipo porque o sinal tipo: esperado "Carnes" (referência em modo normal), recebido "Bebidas" em 4 itens está presente na resposta HTTP e os verbetes chave_de_juncao_errada, entidade-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1863): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 0 linha(s) da referência | 0 linha(s) novas |

Trecho podado (hash `e4870f4dbbc1b73d`):

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

```

Poda de `corpo_http` (evento 1865): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2068}, depois {"chars": 241}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tipo | "Carnes" (referência em modo normal) | "Bebidas" em 4 itens |

Trecho podado (hash `a1a95c61af5cf648`):

```text
lista com 14 itens (referência em modo normal: 14); tipo diferente em 4 itens; por exemplo: {"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Bebidas", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}
```

Interceptação (evento 1859): `GET /api/produtos` status 200; corpo `0ef7077cc7a06cfa`, árvore `None`.

## 3. Contraste com a segunda causa

chave_de_juncao_errada e não tipo_divergente: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: chave_de_juncao_errada, entidade-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| chave_de_juncao_errada | 0,99 | sim |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[chave_de_juncao_errada]`; verbetes citados: `chave_de_juncao_errada`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `chave_de_juncao_errada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `chave_de_juncao_errada` | confere | contexto: `chave_de_juncao_errada`, `entidade-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `chave_de_juncao_errada` | confere | verbetes: `chave_de_juncao_errada`, `entidade-produto` |
| fonte_formato_valido | `[chave_de_juncao_errada]` | confere | {"ids": ["chave_de_juncao_errada"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `chave_de_juncao_errada` | confere | {"termo": "chave_de_juncao_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-17 --k 3`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1852 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:01:01 | caso tra-17 |
| 1853 | 2 | acao | programa | ao_vivo | 2026-11-06T11:01:01 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 117.1, "falhou": false} |
| 1854 | 3 | acao | programa | ao_vivo | 2026-11-06T11:01:01 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 18.3, "falhou": false} |
| 1855 | 4 | acao | programa | ao_vivo | 2026-11-06T11:01:01 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 2.9, "falhou": false} |
| 1856 | 5 | acao | programa | ao_vivo | 2026-11-06T11:01:01 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 3.9, "falhou": false} |
| 1857 | 6 | acao | programa | ao_vivo | 2026-11-06T11:01:01 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 3.8, "falhou": false} |
| 1859 | 7 | interceptacao | programa | ao_vivo | 2026-11-06T11:01:01 | GET /api/produtos 200 |
| 1860 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | conferencia_do_roteiro: confere |
| 1861 | 9 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | conferencia_do_roteiro: confere |
| 1862 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | conferencia_do_roteiro: confere |
| 1863 | 11 | poda | programa | ao_vivo | 2026-11-06T11:01:01 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1865 | 12 | poda | programa | ao_vivo | 2026-11-06T11:01:01 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1866 | 13 | candidatos | programa | ao_vivo | 2026-11-06T11:01:01 | 3 de 39 verbetes entregues |
| 1868 | 14 | prompt | programa | ao_vivo | 2026-11-06T11:01:01 | {"etapa": "diagnostico", "sha": "d13621a965e0c6be", "prompt_sha256": "d13621a965e0", "chars": 4239, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1870 | 15 | inferencia | programa | ao_vivo | 2026-11-06T11:01:01 | diagnostico: 85,5 s |
| 1871 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T11:01:01 | causa_raiz: `chave_de_juncao_errada` |
| 1872 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T11:01:01 | campo: `tipo` |
| 1873 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T11:01:01 | impacto: `O usuário vê categorias incorretas atribuídas aos produtos, como "Bebidas" em vez de "Carnes".` |
| 1874 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T11:01:01 | fonte: `[chave_de_juncao_errada]` |
| 1875 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T11:01:01 | fonte_citada: `chave_de_juncao_errada` |
| 1876 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | quatro_linhas_presentes: confere |
| 1877 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | rotulo_no_conjunto: confere |
| 1878 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | fonte_existe_na_biblioteca: confere |
| 1879 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | fonte_estava_no_contexto: confere |
| 1880 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | campo_existe_no_caso: confere |
| 1881 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1882 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | notas_nos_verbetes_citados: informativo |
| 1883 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | impacto: nao_verificavel |
| 1884 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | fonte_formato_valido: confere |
| 1885 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | fonte_contem_termo_da_causa: confere |
| 1886 | 31 | decisao | programa | ao_vivo | 2026-11-06T11:01:01 | diagnostico: escolha chave_de_juncao_errada; divergência não |

</details>

Nós de decisão:

- evento 1886, `diagnostico`: escolha `chave_de_juncao_errada`; resultado rotulo_emitido; evidência: evento 1865 (sinal_em_codigo), evento 1863 (arvore_podada), evento 1859 (corpo_http), evento 1866 (verbete_entregue, chave_de_juncao_errada), evento 1866 (verbete_entregue, entidade-produto), evento 1866 (verbete_entregue, tipo_divergente), evento 1870 (resposta), evento 1875 (verbete_citado, chave_de_juncao_errada); divergência: não; falha: nenhuma; prov.used: chave_de_juncao_errada, entidade-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1852 a 1886 da trilha; hash dos eventos deste caso: `693099892b4751f3`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
