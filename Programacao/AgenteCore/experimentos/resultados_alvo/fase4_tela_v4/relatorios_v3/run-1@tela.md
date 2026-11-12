<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Erro interno do servidor (500) em `GET /api/produtos`

Caso `run-1` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/run-1@tela`: o caso `run-1` na corrida `fase4_tela_v4`; eventos 433 a 468 da trilha `trilha_tela.jsonl`, hash dos eventos `2d965b60e454e8cb` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Erro interno do servidor (500) em `GET /api/produtos`

## 3. Data, organização e autor

Observado em 06/11/2026 10:11:24 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A página `produtos_api.php` do site PHP (CobaiaFront), que chama a CobaiaAPI em `GET /api/produtos` (host localhost:8000).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Roteiro `api-catalogo` da tela, com a falha injetada `error_500` (a CobaiaAPI responde com erro interno, status 500). O roteiro parou no passo 3 (conferir `#produtos-api-grid .saiba-mais`). Caso `run-1`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 5 (tempo e estado: o comportamento no tempo ou no estado está errado); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu).

## 6. Descrição para reproduzir

Passos do roteiro, na ordem em que o agente os executou (os tempos são os medidos):

1. Abrir `produtos_api.php` (0,1 s).
2. Esperar aparecer `#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger` (0,0 s).
3. Conferir `#produtos-api-grid .saiba-mais` (0,0 s): falhou aqui.

A página chamou `GET /api/produtos` em localhost:8000 e recebeu status 500 (a API falhou por erro interno), `application/json`, 50 caracteres, em 19,0 ms.

A conferência do roteiro `grid com 14 cartões` não confere: esperava 14 elementos e observou 0 elementos.

Sintoma, como o código o descreveu para o agente:

> A requisição respondeu HTTP 500. A conferência 'grid com 14 cartões' falhou: esperava 14 elementos; viu 0 elementos. A resposta veio como objeto em vez de lista. Os campos id, nome, resumo, tipo, preco, imagem e destaque não vieram na resposta. A resposta trouxe o campo detail, que o contrato não prevê. A tela mostra 140 linha(s) a menos e 1 a mais que a referência.

Trecho da resposta, como a poda em código deixou para o agente (hash `76e7cf76cde2ae11`):

```text
{"detail": "fault injection: error_500 em produto", "id": "(ausente)", "nome": "(ausente)", "resumo": "(ausente)", "tipo": "(ausente)", "preco": "(ausente)", "imagem": "(ausente)", "destaque": "(ausente)"}
```

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids run-1 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| tela (árvore de acessibilidade, contra a referência em modo normal) | 22 linha(s) da referência | 4 linha(s) novas |
| corpo de `GET /api/produtos` (corpo inteiro) | lista | objeto |
| corpo de `GET /api/produtos`, campo `id` | inteiro | ausente |
| corpo de `GET /api/produtos`, campo `nome` | texto | ausente |
| corpo de `GET /api/produtos`, campo `resumo` | texto\|nulo | ausente |
| corpo de `GET /api/produtos`, campo `tipo` | texto | ausente |
| corpo de `GET /api/produtos`, campo `preco` | numero | ausente |
| corpo de `GET /api/produtos`, campo `imagem` | texto\|nulo | ausente |
| corpo de `GET /api/produtos`, campo `destaque` | booleano | ausente |
| corpo de `GET /api/produtos`, campo `detail` |  | texto |
| conferência do roteiro `grid com 14 cartões` | 14 elementos | 0 elementos |

A referência em modo normal desta corrida é a trilha `fase4_tela_v4/referencia/api-catalogo@normal`: é contra ela que a poda comparou a tela e o corpo.

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 5 (tempo e estado: o comportamento no tempo ou no estado está errado); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu); o roteiro parou no passo 3.

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 5 (tempo e estado); nível 1 (fácil). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `erro_interno_do_servidor` (Erro interno do servidor (500); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/erro_interno_do_servidor.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/erro_interno_do_servidor.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Verbetes entregues pela busca e não citados: `contagem_inconsistente` (Contagem inconsistente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/contagem_inconsistente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/contagem_inconsistente.md`).
- Caso escrito: `run-1` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/run-1@tela` em `trilha_tela.jsonl`, eventos 433 a 468, hash dos eventos `2d965b60e454e8cb`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/run-1@tela.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids run-1 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `erro_interno_do_servidor` (Erro interno do servidor (500)). Campo: nenhum apontado. Confiança: o agente está seguro desta causa (probabilidade 0,99 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê uma página de erro sem detalhes, enquanto a interface esperava uma lista de produtos formatada corretamente.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu erro_interno_do_servidor porque o sinal esperado lista, recebido objeto está presente na resposta HTTP e os verbetes erro_interno_do_servidor, contagem_inconsistente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Poda de `arvore` (evento 441), feita em código antes de montar o prompt: 54 nós antes, 21 linhas depois. Regras aplicadas: `cartoes_omitidos` 0, `decoracao_removida` 1, `headings_removidos` 1, `imagens_removidas` 2, `interativos_sem_nome_removidos` 8, `listas_achatadas` 14, `textos_sem_letra_removidos` 3.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 22 linha(s) da referência | 4 linha(s) novas |

Trecho podado (hash `e9b6b8fff9529555`):

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
    text "Erro ao carregar produtos da CobaiaAPI: HTTP 500"
    text "O melhor churrasco da Zona Leste"
    text "Av. Itaquera, 8266 - Itaquera - São Paulo - SP - CEP: 08295000  (11) 2185-9200 ✉"
    link "contato@churrasdafornalha.com.br" href="mailto:contato@churrasdafornalha.com.br?subject=Contato do Site&cc=matheuscs006@gmail.com"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Também podado em código o `corpo_http` (evento 443): de 50 caracteres para 205 caracteres, pelas regras `diff_contra_contrato`, `diff_contra_referencia`.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| (corpo inteiro) | lista | objeto |
| id | inteiro |  |
| nome | texto |  |
| resumo | texto\|nulo |  |
| tipo | texto |  |
| preco | numero |  |
| imagem | texto\|nulo |  |
| destaque | booleano |  |
| detail |  | texto |

O que sobrou desta poda (hash `76e7cf76cde2ae11`):

```text
{"detail": "fault injection: error_500 em produto", "id": "(ausente)", "nome": "(ausente)", "resumo": "(ausente)", "tipo": "(ausente)", "preco": "(ausente)", "imagem": "(ausente)", "destaque": "(ausente)"}
```

Interceptação (evento 438): `GET /api/produtos`, status 500 (a API falhou por erro interno); corpo guardado com o hash `24067faf5d61b7b3`.

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> erro_interno_do_servidor e não resposta_truncada: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: erro_interno_do_servidor, contagem_inconsistente, contrato-produto

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `erro_interno_do_servidor` (Erro interno do servidor (500)) | 0,99 | sim |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[erro_interno_do_servidor] [contrato-produto]`; verbetes citados: `erro_interno_do_servidor` (Erro interno do servidor (500); leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/erro_interno_do_servidor.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/erro_interno_do_servidor.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `erro_interno_do_servidor` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `erro_interno_do_servidor` | confere | contexto: `erro_interno_do_servidor`, `contagem_inconsistente`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `erro_interno_do_servidor`, `contagem_inconsistente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `erro_interno_do_servidor` | confere | verbetes: `erro_interno_do_servidor` |
| A linha FONTE só tem identificadores, no formato pedido | `[erro_interno_do_servidor] [contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["erro_interno_do_servidor", "contrato-produto"]} |
| O verbete citado fala da causa respondida | `erro_interno_do_servidor` | confere | {"termo": "erro_interno_do_servidor"} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "erro_interno_do_servidor"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira a resposta em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids run-1 --k 3`

## 17. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 433 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:11:24 | caso run-1 |
| 434 | 2 | acao | programa | ao_vivo | 2026-11-06T10:11:25 | passo 1: abrir produtos_api.php |
| 435 | 3 | acao | programa | ao_vivo | 2026-11-06T10:11:25 | passo 2: esperar aparecer #produtos-api-grid .saiba-mais, #produtos-api-status.text-danger |
| 436 | 4 | acao | programa | ao_vivo | 2026-11-06T10:11:25 | passo 3: conferir #produtos-api-grid .saiba-mais (falhou) |
| 438 | 5 | interceptacao | programa | ao_vivo | 2026-11-06T10:11:25 | GET /api/produtos 500 |
| 439 | 6 | verificacao | verificacao | ao_vivo | 2026-11-06T10:11:25 | conferencia_do_roteiro: nao_confere |
| 441 | 7 | poda | programa | ao_vivo | 2026-11-06T10:11:25 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 443 | 8 | poda | programa | ao_vivo | 2026-11-06T10:11:25 | corpo_http: 9 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 444 | 9 | candidatos | programa | ao_vivo | 2026-11-06T10:11:25 | 3 de 39 verbetes entregues |
| 446 | 10 | prompt | programa | ao_vivo | 2026-11-06T10:11:25 | diagnostico: 4228 caracteres; verbetes erro_interno_do_servidor, contagem_inconsistente, contrato-produto |
| 448 | 11 | inferencia | programa | ao_vivo | 2026-11-06T10:11:25 | diagnostico: 83,9 s |
| 449 | 12 | declaracao | modelo | ao_vivo | 2026-11-06T10:11:25 | causa_raiz: `erro_interno_do_servidor` |
| 450 | 13 | declaracao | modelo | ao_vivo | 2026-11-06T10:11:25 | campo: `nenhum` |
| 451 | 14 | declaracao | modelo | ao_vivo | 2026-11-06T10:11:25 | impacto: `O usuário vê uma página de erro sem detalhes, enquanto a interface esperava uma lista de produtos formatada corretamente.` |
| 452 | 15 | declaracao | modelo | ao_vivo | 2026-11-06T10:11:25 | fonte: `[erro_interno_do_servidor] [contrato-produto]` |
| 453 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T10:11:25 | fonte_citada: `erro_interno_do_servidor` |
| 454 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T10:11:25 | fonte_citada: `contrato-produto` |
| 455 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T10:11:25 | quatro_linhas_presentes: confere |
| 456 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T10:11:25 | rotulo_no_conjunto: confere |
| 457 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T10:11:25 | fonte_existe_na_biblioteca: confere |
| 458 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T10:11:25 | fonte_existe_na_biblioteca: confere |
| 459 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T10:11:25 | fonte_estava_no_contexto: confere |
| 460 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T10:11:25 | fonte_estava_no_contexto: confere |
| 461 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T10:11:25 | campo_existe_no_caso: nao_se_aplica |
| 462 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T10:11:25 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 463 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T10:11:25 | notas_nos_verbetes_citados: informativo |
| 464 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T10:11:25 | impacto: nao_verificavel |
| 465 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T10:11:25 | fonte_formato_valido: confere |
| 466 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T10:11:25 | fonte_contem_termo_da_causa: confere |
| 467 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T10:11:25 | fonte_contem_termo_da_causa: nao_confere |
| 468 | 31 | decisao | programa | ao_vivo | 2026-11-06T10:11:25 | diagnostico: escolha erro_interno_do_servidor; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 468, decisão `diagnostico`: escolha `erro_interno_do_servidor`; resultado rotulo_emitido.
  - Evidência: evento 443 (sinal_em_codigo); evento 441 (arvore_podada); evento 438 (corpo_http); evento 444 (verbete_entregue: `erro_interno_do_servidor`, `contagem_inconsistente`, `contrato-produto`); evento 448 (resposta); evento 453 (verbete_citado: `erro_interno_do_servidor`); evento 454 (verbete_citado: `contrato-produto`).
  - Usou: `erro_interno_do_servidor`, `contagem_inconsistente`, `contrato-produto`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 433 a 468 da trilha; hash dos eventos deste caso: `2d965b60e454e8cb`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
