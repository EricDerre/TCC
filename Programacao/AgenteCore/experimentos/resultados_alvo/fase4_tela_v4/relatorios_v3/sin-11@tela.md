<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Estrutura aninhada divergente em `GET /api/produtos`, campo `preco`

Caso `sin-11` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/sin-11@tela`: o caso `sin-11` na corrida `fase4_tela_v4`; eventos 838 a 871 da trilha `trilha_tela.jsonl`, hash dos eventos `9ba1c6113c6f4614` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Estrutura aninhada divergente em `GET /api/produtos`, campo `preco`

## 3. Data, organização e autor

Observado em 06/11/2026 10:26:19 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A página `produtos_api.php` do site PHP (CobaiaFront), que chama a CobaiaAPI em `GET /api/produtos` (host localhost:8000).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Roteiro `api-catalogo` da tela, com a falha injetada `estrutura_aninhada_divergente` (um campo vem aninhado dentro de um objeto com valor e moeda). O roteiro parou no passo 4 (conferir `#produtos-api-grid .thumbnail .btn-default`). Caso `sin-11`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 2 (sintática: a forma da resposta não é a esperada); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato).

## 6. Descrição para reproduzir

Passos do roteiro, na ordem em que o agente os executou (os tempos são os medidos):

1. Abrir `produtos_api.php` (0,1 s).
2. Esperar aparecer `#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger` (0,0 s).
3. Conferir `#produtos-api-grid .saiba-mais` (0,0 s).
4. Conferir `#produtos-api-grid .thumbnail .btn-default` (0,0 s): falhou aqui.

A página chamou `GET /api/produtos` em localhost:8000 e recebeu status 200 (a API respondeu sem código de erro), `application/json`, 2404 caracteres, em 14,6 ms.

A conferência do roteiro `preço do primeiro cartão` não confere: esperava texto no padrão ^R\$ \d+,\d{2}$ e observou [object Object].
A outra conferência do roteiro confere (a tabela do bloco 7 a traz).

Sintoma, como o código o descreveu para o agente:

> A conferência 'preço do primeiro cartão' falhou: esperava texto no padrão ^R\$ \d+,\d{2}$; viu [object Object]. O campo preco veio como objeto em vez de numero. A tela mostra 14 linha(s) a menos e 14 a mais que a referência.

Trecho da resposta, como a poda em código deixou para o agente (hash `a7ecb809577d7a2c`):

```text
{"preco": {"valor": 89.9, "moeda": "BRL"}}
```

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-11 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| tela (árvore de acessibilidade, contra a referência em modo normal) | 3 linha(s) da referência | 3 linha(s) novas |
| corpo de `GET /api/produtos`, campo `preco` | numero | objeto |
| corpo de `GET /api/produtos`, campo `preco` | 89.9 (referência em modo normal) | {"valor": 89.9, "moeda": "BRL"} em 14 itens |
| conferência do roteiro `grid com 14 cartões` | 14 elementos | 14 elementos |
| conferência do roteiro `preço do primeiro cartão` | texto no padrão ^R\$ \d+,\d{2}$ | [object Object] |

A referência em modo normal desta corrida é a trilha `fase4_tela_v4/referencia/api-catalogo@normal`: é contra ela que a poda comparou a tela e o corpo.

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 2 (sintática: a forma da resposta não é a esperada); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato); o roteiro parou no passo 4.

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 2 (sintática); nível 2 (médio). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `estrutura_aninhada_divergente` (Estrutura aninhada divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/estrutura_aninhada_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/estrutura_aninhada_divergente.md`).
- Verbetes entregues pela busca e não citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Caso escrito: `sin-11` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/sin-11@tela` em `trilha_tela.jsonl`, eventos 838 a 871, hash dos eventos `9ba1c6113c6f4614`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/sin-11@tela.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-11 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `estrutura_aninhada_divergente` (Estrutura aninhada divergente). Campo: `preco`. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,96 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `A interface exibe um preço em formato inválido, causando confusão para o usuário.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu estrutura_aninhada_divergente no campo preco porque o sinal preco: esperado numero, recebido objeto está presente na resposta HTTP e os verbetes contrato-produto, estrutura_aninhada_divergente, entidade-produto estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Poda de `arvore` (evento 848), feita em código antes de montar o prompt: 193 nós antes, 39 linhas depois. Regras aplicadas: `cartoes_omitidos` 11, `decoracao_removida` 1, `headings_removidos` 1, `imagens_removidas` 16, `interativos_sem_nome_removidos` 8, `listas_achatadas` 14, `textos_sem_letra_removidos` 3.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `9edb71a2567f3fd5`):

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
      button "[object Object]" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "[object Object]" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "[object Object]" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Também podado em código o `corpo_http` (evento 850): de 2404 caracteres para 42 caracteres, pelas regras `diff_contra_contrato`, `diff_contra_referencia`.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | numero | objeto |
| preco | 89.9 (referência em modo normal) | {"valor": 89.9, "moeda": "BRL"} em 14 itens |

O que sobrou desta poda (hash `a7ecb809577d7a2c`):

```text
{"preco": {"valor": 89.9, "moeda": "BRL"}}
```

Interceptação (evento 844): `GET /api/produtos`, status 200 (a API respondeu sem código de erro); corpo guardado com o hash `f148d81d95af83fe`.

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> estrutura_aninhada_divergente e não campo_ausente: a escolha tem probabilidade 0,96 contra 0,00; verbete(s) na evidência: contrato-produto, estrutura_aninhada_divergente, entidade-produto

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,96 | sim |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[estrutura_aninhada_divergente]`; verbetes citados: `estrutura_aninhada_divergente` (Estrutura aninhada divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/estrutura_aninhada_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/estrutura_aninhada_divergente.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `estrutura_aninhada_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `estrutura_aninhada_divergente` | confere | contexto: `contrato-produto`, `estrutura_aninhada_divergente`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `estrutura_aninhada_divergente` | confere | verbetes: `estrutura_aninhada_divergente` |
| A linha FONTE só tem identificadores, no formato pedido | `[estrutura_aninhada_divergente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["estrutura_aninhada_divergente"]} |
| O verbete citado fala da causa respondida | `estrutura_aninhada_divergente` | confere | {"termo": "estrutura_aninhada_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-11 --k 3`

## 17. Árvore completa

<details><summary>29 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 838 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:26:19 | caso sin-11 |
| 839 | 2 | acao | programa | ao_vivo | 2026-11-06T10:26:20 | passo 1: abrir produtos_api.php |
| 840 | 3 | acao | programa | ao_vivo | 2026-11-06T10:26:20 | passo 2: esperar aparecer #produtos-api-grid .saiba-mais, #produtos-api-status.text-danger |
| 841 | 4 | acao | programa | ao_vivo | 2026-11-06T10:26:20 | passo 3: conferir #produtos-api-grid .saiba-mais |
| 842 | 5 | acao | programa | ao_vivo | 2026-11-06T10:26:20 | passo 4: conferir #produtos-api-grid .thumbnail .btn-default (falhou) |
| 844 | 6 | interceptacao | programa | ao_vivo | 2026-11-06T10:26:20 | GET /api/produtos 200 |
| 845 | 7 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | conferencia_do_roteiro: confere |
| 846 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | conferencia_do_roteiro: nao_confere |
| 848 | 9 | poda | programa | ao_vivo | 2026-11-06T10:26:20 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 850 | 10 | poda | programa | ao_vivo | 2026-11-06T10:26:20 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 851 | 11 | candidatos | programa | ao_vivo | 2026-11-06T10:26:20 | 3 de 39 verbetes entregues |
| 853 | 12 | prompt | programa | ao_vivo | 2026-11-06T10:26:20 | diagnostico: 3834 caracteres; verbetes contrato-produto, estrutura_aninhada_divergente, entidade-produto |
| 855 | 13 | inferencia | programa | ao_vivo | 2026-11-06T10:26:20 | diagnostico: 76,0 s |
| 856 | 14 | declaracao | modelo | ao_vivo | 2026-11-06T10:26:20 | causa_raiz: `estrutura_aninhada_divergente` |
| 857 | 15 | declaracao | modelo | ao_vivo | 2026-11-06T10:26:20 | campo: `preco` |
| 858 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T10:26:20 | impacto: `A interface exibe um preço em formato inválido, causando confusão para o usuário.` |
| 859 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T10:26:20 | fonte: `[estrutura_aninhada_divergente]` |
| 860 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T10:26:20 | fonte_citada: `estrutura_aninhada_divergente` |
| 861 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | quatro_linhas_presentes: confere |
| 862 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | rotulo_no_conjunto: confere |
| 863 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | fonte_existe_na_biblioteca: confere |
| 864 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | fonte_estava_no_contexto: confere |
| 865 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | campo_existe_no_caso: confere |
| 866 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 867 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | notas_nos_verbetes_citados: informativo |
| 868 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | impacto: nao_verificavel |
| 869 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | fonte_formato_valido: confere |
| 870 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T10:26:20 | fonte_contem_termo_da_causa: confere |
| 871 | 29 | decisao | programa | ao_vivo | 2026-11-06T10:26:20 | diagnostico: escolha estrutura_aninhada_divergente; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 871, decisão `diagnostico`: escolha `estrutura_aninhada_divergente`; resultado rotulo_emitido.
  - Evidência: evento 850 (sinal_em_codigo); evento 848 (arvore_podada); evento 844 (corpo_http); evento 851 (verbete_entregue: `contrato-produto`, `estrutura_aninhada_divergente`, `entidade-produto`); evento 855 (resposta); evento 860 (verbete_citado: `estrutura_aninhada_divergente`).
  - Usou: `contrato-produto`, `estrutura_aninhada_divergente`, `entidade-produto`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 838 a 871 da trilha; hash dos eventos deste caso: `9ba1c6113c6f4614`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
