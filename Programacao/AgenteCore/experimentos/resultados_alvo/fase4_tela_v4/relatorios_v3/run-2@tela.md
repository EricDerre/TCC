<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Tempo de resposta excedido em `GET /api/produtos`

Caso `run-2` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/run-2@tela`: o caso `run-2` na corrida `fase4_tela_v4`; eventos 493 a 526 da trilha `trilha_tela.jsonl`, hash dos eventos `5b921840283ad6d7` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Tempo de resposta excedido em `GET /api/produtos`

## 3. Data, organização e autor

Observado em 06/11/2026 10:13:57 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A página `produtos_api.php` do site PHP (CobaiaFront), que chama a CobaiaAPI em `GET /api/produtos` (host localhost:8000).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Roteiro `api-catalogo` da tela, com a falha injetada `latency` (a CobaiaAPI demora de propósito antes de responder). Caso `run-2`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 5 (tempo e estado: o comportamento no tempo ou no estado está errado); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu).

## 6. Descrição para reproduzir

Passos do roteiro, na ordem em que o agente os executou (os tempos são os medidos):

1. Abrir `produtos_api.php` (0,1 s).
2. Esperar aparecer `#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger` (28,4 s).
3. Conferir `#produtos-api-grid .saiba-mais` (0,0 s).
4. Conferir `#produtos-api-grid .thumbnail .btn-default` (0,0 s).
5. Conferir `#produtos-api-status` (0,0 s).

A página chamou `GET /api/produtos` em localhost:8000 e recebeu status 200 (a API respondeu sem código de erro), `application/json`, 2068 caracteres, em 28030,7 ms.

As 3 conferências do roteiro conferem (a tabela do bloco 7 traz cada uma).

Sintoma, como o código o descreveu para o agente:

> A chamada levou 28,0 s; na referência em modo normal, 67 ms.

Trecho da resposta, como a poda em código deixou para o agente (hash `59922d051a426b7b`):

```text
lista com 14 itens, igual à referência em modo normal; primeiro item: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids run-2 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| tela (árvore de acessibilidade, contra a referência em modo normal) | 0 linha(s) da referência | 0 linha(s) novas |
| corpo de `GET /api/produtos`, campo `tempo_ms` | 67 ms (referência em modo normal) | 28031 ms |
| conferência do roteiro `grid com 14 cartões` | 14 elementos | 14 elementos |
| conferência do roteiro `preço do primeiro cartão` | texto no padrão ^R\$ \d+,\d{2}$ | R$ 89,90 |
| conferência do roteiro `sem mensagem de erro na carga` | texto no padrão ^$ |  |

A referência em modo normal desta corrida é a trilha `fase4_tela_v4/referencia/api-catalogo@normal`: é contra ela que a poda comparou a tela e o corpo.

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 5 (tempo e estado: o comportamento no tempo ou no estado está errado); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 5 (tempo e estado); nível 1 (fácil). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `tempo_de_resposta_excedido` (Tempo de resposta excedido; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/tempo_de_resposta_excedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/tempo_de_resposta_excedido.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Caso escrito: `run-2` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/run-2@tela` em `trilha_tela.jsonl`, eventos 493 a 526, hash dos eventos `5b921840283ad6d7`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/run-2@tela.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids run-2 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `tempo_de_resposta_excedido` (Tempo de resposta excedido). Campo: nenhum apontado. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário experimentou uma resposta muito lenta, o que pode levar a uma experiência ruim e potencialmente fazer com que o cliente desista da requisição.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu tempo_de_resposta_excedido no campo tempo_ms porque o sinal tempo_ms: esperado 67 ms (referência em modo normal), recebido 28031 ms está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, tempo_de_resposta_excedido estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Poda de `arvore` (evento 503), feita em código antes de montar o prompt: 193 nós antes, 39 linhas depois. Regras aplicadas: `cartoes_omitidos` 11, `decoracao_removida` 1, `headings_removidos` 1, `imagens_removidas` 16, `interativos_sem_nome_removidos` 8, `listas_achatadas` 14, `textos_sem_letra_removidos` 3.

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

Também podado em código o `corpo_http` (evento 505): de 2068 caracteres para 244 caracteres, pelas regras `diff_contra_contrato`, `diff_contra_referencia`.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tempo_ms | 67 ms (referência em modo normal) | 28031 ms |

O que sobrou desta poda (hash `59922d051a426b7b`):

```text
lista com 14 itens, igual à referência em modo normal; primeiro item: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 499): `GET /api/produtos`, status 200 (a API respondeu sem código de erro); corpo guardado com o hash `4b1bdd056e7a8c3b`.

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> tempo_de_resposta_excedido e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, tempo_de_resposta_excedido

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `tempo_de_resposta_excedido` (Tempo de resposta excedido) | 1,00 | sim |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[tempo_de_resposta_excedido]`; verbetes citados: `tempo_de_resposta_excedido` (Tempo de resposta excedido; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/tempo_de_resposta_excedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/tempo_de_resposta_excedido.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tempo_de_resposta_excedido` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tempo_de_resposta_excedido` | confere | contexto: `entidade-produto`, `contrato-produto`, `tempo_de_resposta_excedido` |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | confere | verbetes: `tempo_de_resposta_excedido` |
| A linha FONTE só tem identificadores, no formato pedido | `[tempo_de_resposta_excedido]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["tempo_de_resposta_excedido"]} |
| O verbete citado fala da causa respondida | `tempo_de_resposta_excedido` | confere | {"termo": "tempo_de_resposta_excedido"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira a resposta em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids run-2 --k 3`

## 17. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 493 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:13:57 | caso run-2 |
| 494 | 2 | acao | programa | ao_vivo | 2026-11-06T10:14:26 | passo 1: abrir produtos_api.php |
| 495 | 3 | acao | programa | ao_vivo | 2026-11-06T10:14:26 | passo 2: esperar aparecer #produtos-api-grid .saiba-mais, #produtos-api-status.text-danger |
| 496 | 4 | acao | programa | ao_vivo | 2026-11-06T10:14:26 | passo 3: conferir #produtos-api-grid .saiba-mais |
| 497 | 5 | acao | programa | ao_vivo | 2026-11-06T10:14:26 | passo 4: conferir #produtos-api-grid .thumbnail .btn-default |
| 498 | 6 | acao | programa | ao_vivo | 2026-11-06T10:14:26 | passo 5: conferir #produtos-api-status |
| 499 | 7 | interceptacao | programa | ao_vivo | 2026-11-06T10:14:26 | GET /api/produtos 200 |
| 500 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T10:14:26 | conferencia_do_roteiro: confere |
| 501 | 9 | verificacao | verificacao | ao_vivo | 2026-11-06T10:14:26 | conferencia_do_roteiro: confere |
| 502 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T10:14:26 | conferencia_do_roteiro: confere |
| 503 | 11 | poda | programa | ao_vivo | 2026-11-06T10:14:26 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 505 | 12 | poda | programa | ao_vivo | 2026-11-06T10:14:26 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 506 | 13 | candidatos | programa | ao_vivo | 2026-11-06T10:14:26 | 3 de 39 verbetes entregues |
| 508 | 14 | prompt | programa | ao_vivo | 2026-11-06T10:14:26 | diagnostico: 3580 caracteres; verbetes entidade-produto, contrato-produto, tempo_de_resposta_excedido |
| 510 | 15 | inferencia | programa | ao_vivo | 2026-11-06T10:14:26 | diagnostico: 54,5 s |
| 511 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T10:14:26 | causa_raiz: `tempo_de_resposta_excedido` |
| 512 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T10:14:26 | campo: `nenhum` |
| 513 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T10:14:26 | impacto: `O usuário experimentou uma resposta muito lenta, o que pode levar a uma experiência ruim e potencialmente fazer com que o cliente desista da requisição.` |
| 514 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T10:14:26 | fonte: `[tempo_de_resposta_excedido]` |
| 515 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T10:14:26 | fonte_citada: `tempo_de_resposta_excedido` |
| 516 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T10:14:26 | quatro_linhas_presentes: confere |
| 517 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T10:14:26 | rotulo_no_conjunto: confere |
| 518 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T10:14:26 | fonte_existe_na_biblioteca: confere |
| 519 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T10:14:26 | fonte_estava_no_contexto: confere |
| 520 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T10:14:26 | campo_existe_no_caso: nao_se_aplica |
| 521 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T10:14:26 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 522 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T10:14:26 | notas_nos_verbetes_citados: informativo |
| 523 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T10:14:26 | impacto: nao_verificavel |
| 524 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T10:14:26 | fonte_formato_valido: confere |
| 525 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T10:14:26 | fonte_contem_termo_da_causa: confere |
| 526 | 31 | decisao | programa | ao_vivo | 2026-11-06T10:14:26 | diagnostico: escolha tempo_de_resposta_excedido; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 526, decisão `diagnostico`: escolha `tempo_de_resposta_excedido`; resultado rotulo_emitido.
  - Evidência: evento 505 (sinal_em_codigo); evento 503 (arvore_podada); evento 499 (corpo_http); evento 506 (verbete_entregue: `entidade-produto`, `contrato-produto`, `tempo_de_resposta_excedido`); evento 510 (resposta); evento 515 (verbete_citado: `tempo_de_resposta_excedido`).
  - Usou: `entidade-produto`, `contrato-produto`, `tempo_de_resposta_excedido`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 493 a 526 da trilha; hash dos eventos deste caso: `5b921840283ad6d7`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
