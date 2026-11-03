<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-11`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/lex-11@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nome` · selo de probabilidade: **medio** (p = 0,91) · **CONFLITO**: nenhum verbete entregue trata da causa respondida codificacao_incorreta

**IMPACTO (declarado):** `O usuário vê nomes com caracteres codificados incorretamente, como "Ãgua Mineral" em vez de "Água Mineral".`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta no campo nome porque o sinal nome: esperado "Água Mineral" (referência em modo normal), recebido "Ãgua Mineral" em 3 itens está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, contagem_inconsistente estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,03 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Poda de `arvore` (evento 828): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 45}.

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

Poda de `corpo_http` (evento 829): regras diff_contra_contrato, diff_contra_referencia; antes {"chars": 2071}, depois {"chars": 410}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| nome | "Água Mineral" (referência em modo normal) | "Ãgua Mineral" em 3 itens |

Trecho podado (hash `ad8faa3b1aebfc8f`):

```text
lista com 14 itens (referência em modo normal: 14); nome diferente em 3 itens; por exemplo: {"id": 8, "nome": "Ãgua Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}; {"id": 11, "nome": "PÃ£o de Alho", "resumo": "Pão de alho grelhado na brasa", "tipo": "Acompanhamentos", "preco": 16.9, "imagem": "paodealho.png", "destaque": false}
```

Interceptação (evento 824): `GET /api/produtos` status 200; corpo `0fd45da79aa14f8a`, árvore `None`.

## 3. Contraste com a segunda causa

codificacao_incorreta e não formato_de_data_divergente: a escolha tem probabilidade 0,91 contra 0,03; verbete(s) na evidência: entidade-produto, contrato-produto, contagem_inconsistente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 0,91 | sim |
| formato_de_data_divergente | 0,03 |  |
| campo_ausente | 0,02 |  |
| campo_renomeado | 0,02 |  |
| tipo_divergente | 0,02 |  |
| valor_fora_do_dominio | 0,01 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| contagem_inconsistente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| nulo_inesperado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `contagem_inconsistente` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[entidade-produto], [contrato-produto]` | confere | {"ids": ["entidade-produto", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "codificacao_incorreta"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids lex-11 --k 3`

## 6. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 818 | 1 | entrada | programa | ao_vivo | 2026-11-01T14:38:59 | caso lex-11 |
| 819 | 2 | acao | programa | ao_vivo | 2026-11-01T14:38:59 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 165.9, "falhou": false} |
| 820 | 3 | acao | programa | ao_vivo | 2026-11-01T14:38:59 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 8.7, "falhou": false} |
| 821 | 4 | acao | programa | ao_vivo | 2026-11-01T14:38:59 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 3.1, "falhou": false} |
| 822 | 5 | acao | programa | ao_vivo | 2026-11-01T14:38:59 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 3.9, "falhou": false} |
| 823 | 6 | acao | programa | ao_vivo | 2026-11-01T14:38:59 | {"passo": 5, "acao": "conferir", "seletor": "#produtos-api-status", "url": null, "tempo_ms": 2.9, "falhou": false} |
| 824 | 7 | interceptacao | programa | ao_vivo | 2026-11-01T14:38:59 | GET /api/produtos 200 |
| 825 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T14:38:59 | conferencia_do_roteiro: confere |
| 826 | 9 | verificacao | verificacao | ao_vivo | 2026-11-01T14:38:59 | conferencia_do_roteiro: confere |
| 827 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T14:38:59 | conferencia_do_roteiro: confere |
| 828 | 11 | poda | programa | ao_vivo | 2026-11-01T14:38:59 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 829 | 12 | poda | programa | ao_vivo | 2026-11-01T14:38:59 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 830 | 13 | candidatos | programa | ao_vivo | 2026-11-01T14:38:59 | 3 de 40 verbetes entregues |
| 832 | 14 | prompt | programa | ao_vivo | 2026-11-01T14:38:59 | {"etapa": "diagnostico", "sha": "df93d1ed7f273607", "prompt_sha256": "df93d1ed7f27", "chars": 6253, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 834 | 15 | inferencia | programa | ao_vivo | 2026-11-01T14:38:59 | diagnostico: 82,5 s |
| 835 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T14:38:59 | causa_raiz: `codificacao_incorreta` |
| 836 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T14:38:59 | campo: `nome` |
| 837 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T14:38:59 | impacto: `O usuário vê nomes com caracteres codificados incorretamente, como "Ãgua Mineral" em vez de "Água Mineral".` |
| 838 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T14:38:59 | fonte: `[entidade-produto], [contrato-produto]` |
| 839 | 20 | declaracao | modelo | ao_vivo | 2026-11-01T14:38:59 | fonte_citada: `entidade-produto` |
| 840 | 21 | declaracao | modelo | ao_vivo | 2026-11-01T14:38:59 | fonte_citada: `contrato-produto` |
| 841 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T14:38:59 | quatro_linhas_presentes: confere |
| 842 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T14:38:59 | rotulo_no_conjunto: confere |
| 843 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T14:38:59 | fonte_existe_na_biblioteca: confere |
| 844 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T14:38:59 | fonte_existe_na_biblioteca: confere |
| 845 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T14:38:59 | fonte_estava_no_contexto: confere |
| 846 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T14:38:59 | fonte_estava_no_contexto: confere |
| 847 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T14:38:59 | campo_existe_no_caso: confere |
| 848 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T14:38:59 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 849 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T14:38:59 | notas_nos_verbetes_citados: informativo |
| 850 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T14:38:59 | impacto: nao_verificavel |
| 851 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T14:38:59 | fonte_formato_valido: confere |
| 852 | 33 | verificacao | verificacao | ao_vivo | 2026-11-01T14:38:59 | fonte_contem_termo_da_causa: nao_confere |
| 853 | 34 | verificacao | verificacao | ao_vivo | 2026-11-01T14:38:59 | fonte_contem_termo_da_causa: nao_confere |
| 854 | 35 | decisao | programa | ao_vivo | 2026-11-01T14:38:59 | diagnostico: escolha codificacao_incorreta; divergência sim |

</details>

Nós de decisão:

- evento 854, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 829 (sinal_em_codigo), evento 828 (arvore_podada), evento 824 (corpo_http), evento 830 (verbete_entregue, entidade-produto), evento 830 (verbete_entregue, contrato-produto), evento 830 (verbete_entregue, contagem_inconsistente), evento 834 (resposta), evento 839 (verbete_citado, entidade-produto), evento 840 (verbete_citado, contrato-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: entidade-produto, contrato-produto, contagem_inconsistente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 818 a 854 da trilha; hash dos eventos deste caso: `7f1a315fcecdd60a`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
