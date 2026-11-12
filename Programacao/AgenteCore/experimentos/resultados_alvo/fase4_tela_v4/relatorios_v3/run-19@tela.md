<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Tempo de resposta excedido em `GET /api/produtos/1 (clique em 'Saiba Mais...')`

Caso `run-19` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/run-19@tela`: o caso `run-19` na corrida `fase4_tela_v4`; eventos 2078 a 2113 da trilha `trilha_tela.jsonl`, hash dos eventos `88c02123b0ed6352` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Tempo de resposta excedido em `GET /api/produtos/1 (clique em 'Saiba Mais...')`

## 3. Data, organização e autor

Observado em 06/11/2026 11:07:48 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A página `produtos_api.php` do site PHP (CobaiaFront), que chama a CobaiaAPI em `GET /api/produtos` (host localhost:8000).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Roteiro `api-detalhe` da tela, com a falha injetada `latency` (a CobaiaAPI demora de propósito antes de responder). Caso `run-19`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 5 (tempo e estado: o comportamento no tempo ou no estado está errado); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato).

## 6. Descrição para reproduzir

Passos do roteiro, na ordem em que o agente os executou (os tempos são os medidos):

1. Abrir `produtos_api.php` (0,1 s).
2. Esperar aparecer `#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger` (28,4 s).
3. Conferir `#produtos-api-grid .saiba-mais` (0,0 s).
4. Clicar em `#produtos-api-grid .saiba-mais[data-id='1']` (0,0 s).
5. Esperar aparecer `#modalDetalhe` (2,4 s).
6. Conferir `#modalDetalheTitulo` (0,0 s).
7. Conferir `#modalDetalheCorpo` (0,0 s).

A página chamou `GET /api/produtos` em localhost:8000 e recebeu status 200 (a API respondeu sem código de erro), `application/json`, 2068 caracteres, em 28031,5 ms.

As 3 conferências do roteiro conferem (a tabela do bloco 7 traz cada uma).

Sintoma, como o código o descreveu para o agente:

> A chamada levou 2,0 s; na referência em modo normal, 16 ms.

Trecho da resposta, como a poda em código deixou para o agente (hash `b78f8a85ed458c1a`):

```text
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids run-19 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| tela (árvore de acessibilidade, contra a referência em modo normal) | 0 linha(s) da referência | 0 linha(s) novas |
| corpo de `GET /api/produtos/1 (clique em 'Saiba Mais...')`, campo `tempo_ms` | 16 ms (referência em modo normal) | 2012 ms |
| conferência do roteiro `grid carregado antes do detalhe` | 14 elementos | 14 elementos |
| conferência do roteiro `título do modal com o nome do produto` | texto no padrão \S | Picanha ao Alho |
| conferência do roteiro `corpo do modal com o resumo` | texto no padrão \S | Picanha grelhada com alho laminado na brasa |

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 5 (tempo e estado: o comportamento no tempo ou no estado está errado); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 5 (tempo e estado); nível 2 (médio). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `tempo_de_resposta_excedido` (Tempo de resposta excedido; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/tempo_de_resposta_excedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/tempo_de_resposta_excedido.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Caso escrito: `run-19` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/run-19@tela` em `trilha_tela.jsonl`, eventos 2078 a 2113, hash dos eventos `88c02123b0ed6352`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/run-19@tela.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids run-19 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `tempo_de_resposta_excedido` (Tempo de resposta excedido). Campo: nenhum apontado. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,98 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário experimentou uma resposta lenta, o que pode causar insatisfação e atrasos na experiência do usuário.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu tempo_de_resposta_excedido no campo tempo_ms porque o sinal tempo_ms: esperado 16 ms (referência em modo normal), recebido 2012 ms está presente na resposta HTTP e os verbetes tempo_de_resposta_excedido, entidade-produto, contrato-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,02. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Poda de `arvore` (evento 2091), feita em código antes de montar o prompt: 197 nós antes, 42 linhas depois. Regras aplicadas: `cartoes_omitidos` 11, `decoracao_removida` 1, `headings_removidos` 1, `imagens_removidas` 16, `interativos_sem_nome_removidos` 9, `listas_achatadas` 14, `textos_sem_letra_removidos` 3.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 0 linha(s) da referência | 0 linha(s) novas |

Trecho podado (hash `1d807eb42e97c234`):

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
  dialog
    heading "Picanha ao Alho" level=4
    text "Picanha grelhada com alho laminado na brasa"

```

Também podado em código o `corpo_http` (evento 2092): de 161 caracteres para 174 caracteres, pelas regras `diff_contra_contrato`, `diff_contra_referencia`.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tempo_ms | 16 ms (referência em modo normal) | 2012 ms |

O que sobrou desta poda (hash `b78f8a85ed458c1a`):

```text
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 2086): `GET /api/produtos`, status 200 (a API respondeu sem código de erro); corpo guardado com o hash `4b1bdd056e7a8c3b`.

Interceptação (evento 2087): `GET /api/produtos/1`, status 200; corpo guardado com o hash `b5a0d0b69ce86861`.

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> tempo_de_resposta_excedido e não tipo_divergente: a escolha tem probabilidade 0,98 contra 0,02; verbete(s) na evidência: tempo_de_resposta_excedido, entidade-produto, contrato-produto

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `tempo_de_resposta_excedido` (Tempo de resposta excedido) | 0,98 | sim |
| `tipo_divergente` (Tipo divergente) | 0,02 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[tempo_de_resposta_excedido]`; verbetes citados: `tempo_de_resposta_excedido` (Tempo de resposta excedido; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/tempo_de_resposta_excedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/tempo_de_resposta_excedido.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tempo_de_resposta_excedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tempo_de_resposta_excedido` | confere | contexto: `tempo_de_resposta_excedido`, `entidade-produto`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | confere | verbetes: `tempo_de_resposta_excedido` |
| A linha FONTE só tem identificadores, no formato pedido | `[tempo_de_resposta_excedido]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["tempo_de_resposta_excedido"]} |
| O verbete citado fala da causa respondida | `tempo_de_resposta_excedido` | confere | {"termo": "tempo_de_resposta_excedido"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira a resposta em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids run-19 --k 3`

## 17. Árvore completa

<details><summary>34 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2078 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:07:48 | caso run-19 |
| 2079 | 2 | acao | programa | ao_vivo | 2026-11-06T11:08:19 | passo 1: abrir produtos_api.php |
| 2080 | 3 | acao | programa | ao_vivo | 2026-11-06T11:08:19 | passo 2: esperar aparecer #produtos-api-grid .saiba-mais, #produtos-api-status.text-danger |
| 2081 | 4 | acao | programa | ao_vivo | 2026-11-06T11:08:19 | passo 3: conferir #produtos-api-grid .saiba-mais |
| 2082 | 5 | acao | programa | ao_vivo | 2026-11-06T11:08:19 | passo 4: clicar em #produtos-api-grid .saiba-mais[data-id='1'] |
| 2083 | 6 | acao | programa | ao_vivo | 2026-11-06T11:08:19 | passo 5: esperar aparecer #modalDetalhe |
| 2084 | 7 | acao | programa | ao_vivo | 2026-11-06T11:08:19 | passo 6: conferir #modalDetalheTitulo |
| 2085 | 8 | acao | programa | ao_vivo | 2026-11-06T11:08:19 | passo 7: conferir #modalDetalheCorpo |
| 2086 | 9 | interceptacao | programa | ao_vivo | 2026-11-06T11:08:19 | GET /api/produtos 200 |
| 2087 | 10 | interceptacao | programa | ao_vivo | 2026-11-06T11:08:19 | GET /api/produtos/1 200 |
| 2088 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | conferencia_do_roteiro: confere |
| 2089 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | conferencia_do_roteiro: confere |
| 2090 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | conferencia_do_roteiro: confere |
| 2091 | 14 | poda | programa | ao_vivo | 2026-11-06T11:08:19 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 2092 | 15 | poda | programa | ao_vivo | 2026-11-06T11:08:19 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 2093 | 16 | candidatos | programa | ao_vivo | 2026-11-06T11:08:19 | 3 de 39 verbetes entregues |
| 2095 | 17 | prompt | programa | ao_vivo | 2026-11-06T11:08:19 | diagnostico: 3539 caracteres; verbetes tempo_de_resposta_excedido, entidade-produto, contrato-produto |
| 2097 | 18 | inferencia | programa | ao_vivo | 2026-11-06T11:08:19 | diagnostico: 71,2 s |
| 2098 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T11:08:19 | causa_raiz: `tempo_de_resposta_excedido` |
| 2099 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T11:08:19 | campo: `nenhum` |
| 2100 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T11:08:19 | impacto: `O usuário experimentou uma resposta lenta, o que pode causar insatisfação e atrasos na experiência do usuário.` |
| 2101 | 22 | declaracao | modelo | ao_vivo | 2026-11-06T11:08:19 | fonte: `[tempo_de_resposta_excedido]` |
| 2102 | 23 | declaracao | modelo | ao_vivo | 2026-11-06T11:08:19 | fonte_citada: `tempo_de_resposta_excedido` |
| 2103 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | quatro_linhas_presentes: confere |
| 2104 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | rotulo_no_conjunto: confere |
| 2105 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | fonte_existe_na_biblioteca: confere |
| 2106 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | fonte_estava_no_contexto: confere |
| 2107 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | campo_existe_no_caso: nao_se_aplica |
| 2108 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2109 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | notas_nos_verbetes_citados: informativo |
| 2110 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | impacto: nao_verificavel |
| 2111 | 32 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | fonte_formato_valido: confere |
| 2112 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T11:08:19 | fonte_contem_termo_da_causa: confere |
| 2113 | 34 | decisao | programa | ao_vivo | 2026-11-06T11:08:19 | diagnostico: escolha tempo_de_resposta_excedido; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 2113, decisão `diagnostico`: escolha `tempo_de_resposta_excedido`; resultado rotulo_emitido.
  - Evidência: evento 2092 (sinal_em_codigo); evento 2091 (arvore_podada); evento 2087 (corpo_http); evento 2093 (verbete_entregue: `tempo_de_resposta_excedido`, `entidade-produto`, `contrato-produto`); evento 2097 (resposta); evento 2102 (verbete_citado: `tempo_de_resposta_excedido`).
  - Usou: `tempo_de_resposta_excedido`, `entidade-produto`, `contrato-produto`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2078 a 2113 da trilha; hash dos eventos deste caso: `88c02123b0ed6352`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
