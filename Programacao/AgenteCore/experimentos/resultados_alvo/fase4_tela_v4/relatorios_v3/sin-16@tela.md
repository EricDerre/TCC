<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Campo ausente em `GET /api/produtos/1 (modo field_missing, campo destaque)`, campo `destaque`

Caso `sin-16` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/sin-16@tela`: o caso `sin-16` na corrida `fase4_tela_v4`; eventos 1414 a 1453 da trilha `trilha_tela.jsonl`, hash dos eventos `9c6de28ef5afb3cf` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Campo ausente em `GET /api/produtos/1 (modo field_missing, campo destaque)`, campo `destaque`

## 3. Data, organização e autor

Observado em 06/11/2026 10:47:35 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A página `produtos_api.php` do site PHP (CobaiaFront), que chama a CobaiaAPI em `GET /api/produtos` (host localhost:8000).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Roteiro `api-detalhe` da tela, com a falha injetada `field_missing` (um campo do contrato é apagado da resposta) no campo `destaque`. Caso `sin-16`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 2 (sintática: a forma da resposta não é a esperada); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu).

## 6. Descrição para reproduzir

Passos do roteiro, na ordem em que o agente os executou (os tempos são os medidos):

1. Abrir `produtos_api.php` (0,1 s).
2. Esperar aparecer `#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger` (0,0 s).
3. Conferir `#produtos-api-grid .saiba-mais` (0,0 s).
4. Clicar em `#produtos-api-grid .saiba-mais[data-id='1']` (0,0 s).
5. Esperar aparecer `#modalDetalhe` (0,2 s).
6. Conferir `#modalDetalheTitulo` (0,0 s).
7. Conferir `#modalDetalheCorpo` (0,0 s).

A página chamou `GET /api/produtos` em localhost:8000 e recebeu status 200 (a API respondeu sem código de erro), `application/json`, 1835 caracteres, em 17,7 ms.

As 3 conferências do roteiro conferem (a tabela do bloco 7 traz cada uma).

Sintoma, como o código o descreveu para o agente:

> O campo destaque não veio na resposta. A tela mostra 14 linha(s) a menos e 14 a mais que a referência.

Trecho da resposta, como a poda em código deixou para o agente (hash `dea02287a3373e04`):

```text
{"destaque": "(ausente)"}
```

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-16 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| tela (árvore de acessibilidade, contra a referência em modo normal) | 3 linha(s) da referência | 3 linha(s) novas |
| corpo de `GET /api/produtos/1 (modo field_missing, campo destaque)`, campo `destaque` | booleano | ausente |
| conferência do roteiro `grid carregado antes do detalhe` | 14 elementos | 14 elementos |
| conferência do roteiro `título do modal com o nome do produto` | texto no padrão \S | Picanha ao Alho |
| conferência do roteiro `corpo do modal com o resumo` | texto no padrão \S | Picanha grelhada com alho laminado na brasa |

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 2 (sintática: a forma da resposta não é a esperada); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 2 (sintática); nível 1 (fácil). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Caso escrito: `sin-16` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/sin-16@tela` em `trilha_tela.jsonl`, eventos 1414 a 1453, hash dos eventos `9c6de28ef5afb3cf`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/sin-16@tela.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-16 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `campo_ausente` (Campo ausente). Campo: `destaque`. Confiança: o agente está seguro desta causa (probabilidade 0,99 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O campo destaque não foi incluído na resposta, resultando em uma exibição incompleta da página com 14 linhas a menos.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu campo_ausente no campo destaque porque o sinal destaque: esperado booleano, recebido None está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, campo_ausente estavam entre os entregues ao modelo. A segunda causa, campo_renomeado, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Poda de `arvore` (evento 1430), feita em código antes de montar o prompt: 197 nós antes, 42 linhas depois. Regras aplicadas: `cartoes_omitidos` 11, `decoracao_removida` 1, `headings_removidos` 1, `imagens_removidas` 16, `interativos_sem_nome_removidos` 9, `listas_achatadas` 14, `textos_sem_letra_removidos` 3.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `f90df6f477ad3eb8`):

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
      text "destaque: undefined"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: undefined"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: undefined"
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

Também podado em código o `corpo_http` (evento 1432): de 145 caracteres para 25 caracteres, pelas regras `diff_contra_contrato`, `diff_contra_referencia`.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| destaque | booleano |  |

O que sobrou desta poda (hash `dea02287a3373e04`):

```text
{"destaque": "(ausente)"}
```

Interceptação (evento 1423): `GET /api/produtos`, status 200 (a API respondeu sem código de erro); corpo guardado com o hash `67aa0b74224df738`.

Interceptação (evento 1425): `GET /api/produtos/1`, status 200; corpo guardado com o hash `b11d0160488d8cdf`.

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> campo_ausente e não campo_renomeado: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, campo_ausente

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `campo_ausente` (Campo ausente) | 0,99 | sim |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `chave_de_juncao_errada` (Chave de junção errada) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente]`; verbetes citados: `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `contrato-produto`, `campo_ausente` |
| A linha FONTE só tem identificadores, no formato pedido | `[campo_ausente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["campo_ausente"]} |
| O verbete citado fala da causa respondida | `campo_ausente` | confere | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `destaque` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-16 --k 3`

## 17. Árvore completa

<details><summary>34 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1414 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:47:35 | caso sin-16 |
| 1415 | 2 | acao | programa | ao_vivo | 2026-11-06T10:47:35 | passo 1: abrir produtos_api.php |
| 1416 | 3 | acao | programa | ao_vivo | 2026-11-06T10:47:35 | passo 2: esperar aparecer #produtos-api-grid .saiba-mais, #produtos-api-status.text-danger |
| 1417 | 4 | acao | programa | ao_vivo | 2026-11-06T10:47:35 | passo 3: conferir #produtos-api-grid .saiba-mais |
| 1418 | 5 | acao | programa | ao_vivo | 2026-11-06T10:47:35 | passo 4: clicar em #produtos-api-grid .saiba-mais[data-id='1'] |
| 1419 | 6 | acao | programa | ao_vivo | 2026-11-06T10:47:35 | passo 5: esperar aparecer #modalDetalhe |
| 1420 | 7 | acao | programa | ao_vivo | 2026-11-06T10:47:35 | passo 6: conferir #modalDetalheTitulo |
| 1421 | 8 | acao | programa | ao_vivo | 2026-11-06T10:47:35 | passo 7: conferir #modalDetalheCorpo |
| 1423 | 9 | interceptacao | programa | ao_vivo | 2026-11-06T10:47:35 | GET /api/produtos 200 |
| 1425 | 10 | interceptacao | programa | ao_vivo | 2026-11-06T10:47:35 | GET /api/produtos/1 200 |
| 1426 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T10:47:35 | conferencia_do_roteiro: confere |
| 1427 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T10:47:35 | conferencia_do_roteiro: confere |
| 1428 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T10:47:35 | conferencia_do_roteiro: confere |
| 1430 | 14 | poda | programa | ao_vivo | 2026-11-06T10:47:35 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 1432 | 15 | poda | programa | ao_vivo | 2026-11-06T10:47:35 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1433 | 16 | candidatos | programa | ao_vivo | 2026-11-06T10:47:35 | 3 de 39 verbetes entregues |
| 1435 | 17 | prompt | programa | ao_vivo | 2026-11-06T10:47:35 | diagnostico: 3485 caracteres; verbetes entidade-produto, contrato-produto, campo_ausente |
| 1437 | 18 | inferencia | programa | ao_vivo | 2026-11-06T10:47:35 | diagnostico: 52,8 s |
| 1438 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T10:47:35 | causa_raiz: `campo_ausente` |
| 1439 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T10:47:35 | campo: `destaque` |
| 1440 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T10:47:35 | impacto: `O campo destaque não foi incluído na resposta, resultando em uma exibição incompleta da página com 14 linhas a menos.` |
| 1441 | 22 | declaracao | modelo | ao_vivo | 2026-11-06T10:47:35 | fonte: `[campo_ausente]` |
| 1442 | 23 | declaracao | modelo | ao_vivo | 2026-11-06T10:47:35 | fonte_citada: `campo_ausente` |
| 1443 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T10:47:35 | quatro_linhas_presentes: confere |
| 1444 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T10:47:35 | rotulo_no_conjunto: confere |
| 1445 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T10:47:35 | fonte_existe_na_biblioteca: confere |
| 1446 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T10:47:35 | fonte_estava_no_contexto: confere |
| 1447 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T10:47:35 | campo_existe_no_caso: confere |
| 1448 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T10:47:35 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1449 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T10:47:35 | notas_nos_verbetes_citados: informativo |
| 1450 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T10:47:35 | impacto: nao_verificavel |
| 1451 | 32 | verificacao | verificacao | ao_vivo | 2026-11-06T10:47:35 | fonte_formato_valido: confere |
| 1452 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T10:47:35 | fonte_contem_termo_da_causa: confere |
| 1453 | 34 | decisao | programa | ao_vivo | 2026-11-06T10:47:35 | diagnostico: escolha campo_ausente; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 1453, decisão `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido.
  - Evidência: evento 1432 (sinal_em_codigo); evento 1430 (arvore_podada); evento 1425 (corpo_http); evento 1433 (verbete_entregue: `entidade-produto`, `contrato-produto`, `campo_ausente`); evento 1437 (resposta); evento 1442 (verbete_citado: `campo_ausente`).
  - Usou: `entidade-produto`, `contrato-produto`, `campo_ausente`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1414 a 1453 da trilha; hash dos eventos deste caso: `9c6de28ef5afb3cf`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
