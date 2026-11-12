<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Resposta truncada em `GET /api/produtos?pagina=1`, campo `id`

Caso `tra-4` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/tra-4@tela`: o caso `tra-4` na corrida `fase4_tela_v4`; eventos 377 a 408 da trilha `trilha_tela.jsonl`, hash dos eventos `42b70a8d35bde815` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Resposta truncada em `GET /api/produtos?pagina=1`, campo `id`

## 3. Data, organização e autor

Observado em 06/11/2026 10:08:49 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A página `produtos_api.php` do site PHP (CobaiaFront), que chama a CobaiaAPI em `GET /api/produtos` (host localhost:8000).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Roteiro `api-catalogo` da tela, com a falha injetada `contagem_inconsistente` (a lista vem sem o último item). O roteiro parou no passo 3 (conferir `#produtos-api-grid .saiba-mais`). Caso `tra-4`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 4 (tradução: o mapeamento entre as camadas está errado); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela).

## 6. Descrição para reproduzir

Passos do roteiro, na ordem em que o agente os executou (os tempos são os medidos):

1. Abrir `produtos_api.php` (0,1 s).
2. Esperar aparecer `#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger` (0,0 s).
3. Conferir `#produtos-api-grid .saiba-mais` (0,0 s): falhou aqui.

A página chamou `GET /api/produtos` em localhost:8000 e recebeu status 200 (a API respondeu sem código de erro), `application/json`, 1928 caracteres, em 18,8 ms.

A conferência do roteiro `grid com 14 cartões` não confere: esperava 14 elementos e observou 13 elementos.

Sintoma, como o código o descreveu para o agente:

> A conferência 'grid com 14 cartões' falhou: esperava 14 elementos; viu 13 elementos. A lista veio com 13 itens; a referência em modo normal tem 14: falta o id 14 ("Abacaxi na Brasa"). A tela mostra 10 linha(s) a menos que a referência.

Trecho da resposta, como a poda em código deixou para o agente (hash `9675592a8385ee52`):

```text
lista com 13 itens (referência em modo normal: 14); falta o id 14 ("Abacaxi na Brasa"); primeiro item: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-4 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| tela (árvore de acessibilidade, contra a referência em modo normal) | 1 linha(s) da referência | 1 linha(s) novas |
| corpo de `GET /api/produtos?pagina=1`, campo `itens` | 14 itens (referência em modo normal) | falta o id 14 ("Abacaxi na Brasa") |
| conferência do roteiro `grid com 14 cartões` | 14 elementos | 13 elementos |

A referência em modo normal desta corrida é a trilha `fase4_tela_v4/referencia/api-catalogo@normal`: é contra ela que a poda comparou a tela e o corpo.

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 4 (tradução: o mapeamento entre as camadas está errado); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela); o roteiro parou no passo 3.

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 4 (tradução); nível 3 (difícil). Confiança do agente: o agente não está seguro desta causa; trate como hipótese e confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contagem_inconsistente` (Contagem inconsistente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/contagem_inconsistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/contagem_inconsistente.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Caso escrito: `tra-4` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/tra-4@tela` em `trilha_tela.jsonl`, eventos 377 a 408, hash dos eventos `42b70a8d35bde815`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/tra-4@tela.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-4 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `resposta_truncada` (Resposta truncada). Campo: `id`. Confiança: o agente não está seguro desta causa; trate como hipótese e confira antes de agir (probabilidade 0,51 no rótulo; selo `baixo` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê uma lista com um item a menos, resultando em uma exibição incompleta dos produtos.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu resposta_truncada no campo id porque o sinal itens: esperado 14 itens (referência em modo normal), recebido falta o id 14 ("Abacaxi na Brasa") está presente na resposta HTTP e os verbetes entidade-produto, contagem_inconsistente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, contagem_inconsistente, ficou com probabilidade 0,46. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida resposta_truncada. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,51); trate como hipótese e confira o campo id antes de agir.

Conflito: o que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida resposta_truncada.

Falha registrada no nó: `causa_sem_verbete_que_a_trate` (origem: modelo).

## 13. Evidência

Poda de `arvore` (evento 385), feita em código antes de montar o prompt: 183 nós antes, 39 linhas depois. Regras aplicadas: `cartoes_omitidos` 10, `decoracao_removida` 1, `headings_removidos` 1, `imagens_removidas` 15, `interativos_sem_nome_removidos` 8, `listas_achatadas` 14, `textos_sem_letra_removidos` 3.

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

Também podado em código o `corpo_http` (evento 387): de 1928 caracteres para 277 caracteres, pelas regras `diff_contra_contrato`, `diff_contra_referencia`.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| itens | 14 itens (referência em modo normal) | falta o id 14 ("Abacaxi na Brasa") |

O que sobrou desta poda (hash `9675592a8385ee52`):

```text
lista com 13 itens (referência em modo normal: 14); falta o id 14 ("Abacaxi na Brasa"); primeiro item: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 382): `GET /api/produtos`, status 200 (a API respondeu sem código de erro); corpo guardado com o hash `4f6d409f5a92ce2d`.

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> resposta_truncada e não contagem_inconsistente: a escolha tem probabilidade 0,51 contra 0,46; verbete(s) na evidência: entidade-produto, contagem_inconsistente, contrato-produto

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `resposta_truncada` (Resposta truncada) | 0,51 | sim |
| `contagem_inconsistente` (Contagem inconsistente) | 0,46 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,02 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `codificacao_incorreta` (Codificação de caracteres incorreta) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[contagem_inconsistente]`; verbetes citados: `contagem_inconsistente` (Contagem inconsistente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/contagem_inconsistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/contagem_inconsistente.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contagem_inconsistente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contagem_inconsistente` | confere | contexto: `entidade-produto`, `contagem_inconsistente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `resposta_truncada` | não confere | nenhum verbete do contexto trata dessa causa |
| A linha FONTE só tem identificadores, no formato pedido | `[contagem_inconsistente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contagem_inconsistente"]} |
| O verbete citado fala da causa respondida | `contagem_inconsistente` | não confere | {"termo": "resposta_truncada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `id` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-4 --k 3`

## 17. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 377 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:08:49 | caso tra-4 |
| 378 | 2 | acao | programa | ao_vivo | 2026-11-06T10:08:50 | passo 1: abrir produtos_api.php |
| 379 | 3 | acao | programa | ao_vivo | 2026-11-06T10:08:50 | passo 2: esperar aparecer #produtos-api-grid .saiba-mais, #produtos-api-status.text-danger |
| 380 | 4 | acao | programa | ao_vivo | 2026-11-06T10:08:50 | passo 3: conferir #produtos-api-grid .saiba-mais (falhou) |
| 382 | 5 | interceptacao | programa | ao_vivo | 2026-11-06T10:08:50 | GET /api/produtos 200 |
| 383 | 6 | verificacao | verificacao | ao_vivo | 2026-11-06T10:08:50 | conferencia_do_roteiro: nao_confere |
| 385 | 7 | poda | programa | ao_vivo | 2026-11-06T10:08:50 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 387 | 8 | poda | programa | ao_vivo | 2026-11-06T10:08:50 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 388 | 9 | candidatos | programa | ao_vivo | 2026-11-06T10:08:50 | 3 de 39 verbetes entregues |
| 390 | 10 | prompt | programa | ao_vivo | 2026-11-06T10:08:50 | diagnostico: 3922 caracteres; verbetes entidade-produto, contagem_inconsistente, contrato-produto |
| 392 | 11 | inferencia | programa | ao_vivo | 2026-11-06T10:08:50 | diagnostico: 68,7 s |
| 393 | 12 | declaracao | modelo | ao_vivo | 2026-11-06T10:08:50 | causa_raiz: `resposta_truncada` |
| 394 | 13 | declaracao | modelo | ao_vivo | 2026-11-06T10:08:50 | campo: `id` |
| 395 | 14 | declaracao | modelo | ao_vivo | 2026-11-06T10:08:50 | impacto: `O usuário vê uma lista com um item a menos, resultando em uma exibição incompleta dos produtos.` |
| 396 | 15 | declaracao | modelo | ao_vivo | 2026-11-06T10:08:50 | fonte: `[contagem_inconsistente]` |
| 397 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T10:08:50 | fonte_citada: `contagem_inconsistente` |
| 398 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T10:08:50 | quatro_linhas_presentes: confere |
| 399 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T10:08:50 | rotulo_no_conjunto: confere |
| 400 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T10:08:50 | fonte_existe_na_biblioteca: confere |
| 401 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T10:08:50 | fonte_estava_no_contexto: confere |
| 402 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T10:08:50 | campo_existe_no_caso: confere |
| 403 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T10:08:50 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 404 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T10:08:50 | notas_nos_verbetes_citados: informativo |
| 405 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T10:08:50 | impacto: nao_verificavel |
| 406 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T10:08:50 | fonte_formato_valido: confere |
| 407 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T10:08:50 | fonte_contem_termo_da_causa: nao_confere |
| 408 | 27 | decisao | programa | ao_vivo | 2026-11-06T10:08:50 | diagnostico: escolha resposta_truncada; divergência entre o declarado e o medido: sim |

</details>

Nós de decisão, na ordem:

- evento 408, decisão `diagnostico`: escolha `resposta_truncada`; resultado rotulo_emitido.
  - Evidência: evento 387 (sinal_em_codigo); evento 385 (arvore_podada); evento 382 (corpo_http); evento 388 (verbete_entregue: `entidade-produto`, `contagem_inconsistente`, `contrato-produto`); evento 392 (resposta); evento 397 (verbete_citado: `contagem_inconsistente`).
  - Usou: `entidade-produto`, `contagem_inconsistente`, `contrato-produto`.
  - Divergência entre o declarado e o medido: sim; falha: causa_sem_verbete_que_a_trate.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 377 a 408 da trilha; hash dos eventos deste caso: `42b70a8d35bde815`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
