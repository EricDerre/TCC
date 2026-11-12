<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Campo renomeado em `GET /api/produtos`, campo `preco`

Caso `contrato-field_renamed#1` da corrida `fase4_ensaio_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ensaio_v4/qwen2.5_7b/contrato-field_renamed#1`: o caso `contrato-field_renamed#1` na corrida `fase4_ensaio_v4`; eventos 79 a 111 da trilha `trilha_cenarios.jsonl`, hash dos eventos `30390002a6cb8f01` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Campo renomeado em `GET /api/produtos`, campo `preco`

## 3. Data, organização e autor

Observado em 06/11/2026 11:16:31 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 11:13:26 a 06/11/2026 11:26:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `cenarios`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A página `produtos_api.php` do site PHP (CobaiaFront), que chama a CobaiaAPI em `GET /api/produtos` (host localhost:8000).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Roteiro `api-catalogo` da tela, com a falha injetada `field_renamed` (um campo da resposta vem com o nome trocado, com o sufixo _v2) no campo `preco`. O roteiro parou no passo 4 (conferir `#produtos-api-grid .thumbnail .btn-default`). Caso `contrato-field_renamed#1`, de `cenarios_fase4.py` (catálogo dos dez cenários do ensaio da Fase 5, ficha 36); classe 2 (sintática: a forma da resposta não é a esperada); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato).

## 6. Descrição para reproduzir

Passos do roteiro, na ordem em que o agente os executou (os tempos são os medidos):

1. Abrir `produtos_api.php` (0,2 s).
2. Esperar aparecer `#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger` (0,0 s).
3. Conferir `#produtos-api-grid .saiba-mais` (0,0 s).
4. Conferir `#produtos-api-grid .thumbnail .btn-default` (0,0 s): falhou aqui.

A página chamou `GET /api/produtos` em localhost:8000 e recebeu status 200 (a API respondeu sem código de erro), `application/json`, 2110 caracteres, em 43,6 ms.

A conferência do roteiro `preço do primeiro cartão` não confere: esperava texto no padrão ^R\$ \d+,\d{2}$ e observou undefined.
A outra conferência do roteiro confere (a tabela do bloco 7 a traz).

Sintoma, como o código o descreveu para o agente:

> A conferência 'preço do primeiro cartão' falhou: esperava texto no padrão ^R\$ \d+,\d{2}$; viu undefined. O campo preco veio como preco_v2. A tela mostra 14 linha(s) a menos e 14 a mais que a referência.

Trecho da resposta, como a poda em código deixou para o agente (hash `3ca91df248763374`):

```text
{"preco_v2": 89.9}
```

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| tela (árvore de acessibilidade, contra a referência em modo normal) | 3 linha(s) da referência | 3 linha(s) novas |
| corpo de `GET /api/produtos`, campo `preco` | preco | preco_v2 |
| conferência do roteiro `grid com 14 cartões` | 14 elementos | 14 elementos |
| conferência do roteiro `preço do primeiro cartão` | texto no padrão ^R\$ \d+,\d{2}$ | undefined |

A referência em modo normal desta corrida é a trilha `fase4_ensaio_v4/referencia/api-catalogo@normal`: é contra ela que a poda comparou a tela e o corpo.

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 2 (sintática: a forma da resposta não é a esperada); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato); o roteiro parou no passo 4.

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 2 (sintática); nível 2 (médio). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `campo_renomeado` (Campo renomeado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_renomeado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_renomeado.md`).
- Verbetes entregues pela busca e não citados: `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Caso escrito: `contrato-field_renamed#1` em `cenarios_fase4.py` (catálogo dos dez cenários do ensaio da Fase 5, ficha 36).
- Trilha: `fase4_ensaio_v4/qwen2.5_7b/contrato-field_renamed#1` em `trilha_cenarios.jsonl`, eventos 79 a 111, hash dos eventos `30390002a6cb8f01`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/contrato-field_renamed__r1.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `campo_renomeado` (Campo renomeado). Campo: `preco`. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê um preço incorreto, exibido como "undefined" em vez do valor esperado.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu campo_renomeado no campo preco porque o sinal preco: esperado preco, recebido preco_v2 está presente na resposta HTTP e os verbetes campo_renomeado, campo_ausente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Poda de `arvore` (evento 88), feita em código antes de montar o prompt: 193 nós antes, 39 linhas depois. Regras aplicadas: `cartoes_omitidos` 11, `decoracao_removida` 1, `headings_removidos` 1, `imagens_removidas` 16, `interativos_sem_nome_removidos` 8, `listas_achatadas` 14, `textos_sem_letra_removidos` 3.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `714120f74ce44bb6`):

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
      button "undefined" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "undefined" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "undefined" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Também podado em código o `corpo_http` (evento 90): de 2110 caracteres para 18 caracteres, pelas regras `diff_contra_contrato`, `diff_contra_referencia`.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | preco | preco_v2 |

O que sobrou desta poda (hash `3ca91df248763374`):

```text
{"preco_v2": 89.9}
```

Interceptação (evento 85): `GET /api/produtos`, status 200 (a API respondeu sem código de erro); corpo guardado com o hash `4f7726df03992678`.

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> campo_renomeado e não tipo_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: campo_renomeado, campo_ausente, contrato-produto

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `campo_renomeado` (Campo renomeado) | 1,00 | sim |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[campo_renomeado]`; verbetes citados: `campo_renomeado` (Campo renomeado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_renomeado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_renomeado.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | confere | contexto: `campo_renomeado`, `campo_ausente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `campo_renomeado`, `campo_ausente`, `contrato-produto` |
| A linha FONTE só tem identificadores, no formato pedido | `[campo_renomeado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["campo_renomeado"]} |
| O verbete citado fala da causa respondida | `campo_renomeado` | confere | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`

## 17. Árvore completa

<details><summary>29 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 79 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:16:31 | caso contrato-field_renamed#1 |
| 80 | 2 | acao | programa | ao_vivo | 2026-11-06T11:16:32 | passo 1: abrir produtos_api.php |
| 81 | 3 | acao | programa | ao_vivo | 2026-11-06T11:16:32 | passo 2: esperar aparecer #produtos-api-grid .saiba-mais, #produtos-api-status.text-danger |
| 82 | 4 | acao | programa | ao_vivo | 2026-11-06T11:16:32 | passo 3: conferir #produtos-api-grid .saiba-mais |
| 83 | 5 | acao | programa | ao_vivo | 2026-11-06T11:16:32 | passo 4: conferir #produtos-api-grid .thumbnail .btn-default (falhou) |
| 85 | 6 | interceptacao | programa | ao_vivo | 2026-11-06T11:16:32 | GET /api/produtos 200 |
| 86 | 7 | verificacao | verificacao | ao_vivo | 2026-11-06T11:16:32 | conferencia_do_roteiro: confere |
| 87 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T11:16:32 | conferencia_do_roteiro: nao_confere |
| 88 | 9 | poda | programa | ao_vivo | 2026-11-06T11:16:32 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 90 | 10 | poda | programa | ao_vivo | 2026-11-06T11:16:32 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 91 | 11 | candidatos | programa | ao_vivo | 2026-11-06T11:16:32 | 3 de 39 verbetes entregues |
| 93 | 12 | prompt | programa | ao_vivo | 2026-11-06T11:16:32 | diagnostico: 3650 caracteres; verbetes campo_renomeado, campo_ausente, contrato-produto |
| 95 | 13 | inferencia | programa | ao_vivo | 2026-11-06T11:16:32 | diagnostico: 71,0 s |
| 96 | 14 | declaracao | modelo | ao_vivo | 2026-11-06T11:16:32 | causa_raiz: `campo_renomeado` |
| 97 | 15 | declaracao | modelo | ao_vivo | 2026-11-06T11:16:32 | campo: `preco` |
| 98 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T11:16:32 | impacto: `O usuário vê um preço incorreto, exibido como "undefined" em vez do valor esperado.` |
| 99 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T11:16:32 | fonte: `[campo_renomeado]` |
| 100 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T11:16:32 | fonte_citada: `campo_renomeado` |
| 101 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:16:32 | quatro_linhas_presentes: confere |
| 102 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T11:16:32 | rotulo_no_conjunto: confere |
| 103 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T11:16:32 | fonte_existe_na_biblioteca: confere |
| 104 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:16:32 | fonte_estava_no_contexto: confere |
| 105 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:16:32 | campo_existe_no_caso: confere |
| 106 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:16:32 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 107 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:16:32 | notas_nos_verbetes_citados: informativo |
| 108 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:16:32 | impacto: nao_verificavel |
| 109 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T11:16:32 | fonte_formato_valido: confere |
| 110 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T11:16:32 | fonte_contem_termo_da_causa: confere |
| 111 | 29 | decisao | programa | ao_vivo | 2026-11-06T11:16:32 | diagnostico: escolha campo_renomeado; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 111, decisão `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido.
  - Evidência: evento 90 (sinal_em_codigo); evento 88 (arvore_podada); evento 85 (corpo_http); evento 91 (verbete_entregue: `campo_renomeado`, `campo_ausente`, `contrato-produto`); evento 95 (resposta); evento 100 (verbete_citado: `campo_renomeado`).
  - Usou: `campo_renomeado`, `campo_ausente`, `contrato-produto`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 79 a 111 da trilha; hash dos eventos deste caso: `30390002a6cb8f01`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
