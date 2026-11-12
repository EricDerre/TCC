<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Codificação de caracteres incorreta em `GET /api/produtos`, campo `nome`

Caso `lex-4` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/lex-4@tela`: o caso `lex-4` na corrida `fase4_tela_v4`; eventos 67 a 106 da trilha `trilha_tela.jsonl`, hash dos eventos `64f887099a7f6e06` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Codificação de caracteres incorreta em `GET /api/produtos`, campo `nome`

## 3. Data, organização e autor

Observado em 06/11/2026 09:56:31 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A página `produtos_api.php` do site PHP (CobaiaFront), que chama a CobaiaAPI em `GET /api/produtos` (host localhost:8000).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Roteiro `api-catalogo` da tela, com a falha injetada `codificacao_incorreta` (os acentos vêm trocados: texto gravado em UTF-8 e lido como latin-1) no campo `nome`. Caso `lex-4`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 1 (léxica: o corpo da resposta nem dá para ler); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato).

## 6. Descrição para reproduzir

Passos do roteiro, na ordem em que o agente os executou (os tempos são os medidos):

1. Abrir `produtos_api.php` (0,1 s).
2. Esperar aparecer `#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger` (0,0 s).
3. Conferir `#produtos-api-grid .saiba-mais` (0,0 s).
4. Conferir `#produtos-api-grid .thumbnail .btn-default` (0,0 s).
5. Conferir `#produtos-api-status` (0,0 s).

A página chamou `GET /api/produtos` em localhost:8000 e recebeu status 200 (a API respondeu sem código de erro), `application/json`, 2071 caracteres, em 19,1 ms.

As 3 conferências do roteiro conferem (a tabela do bloco 7 traz cada uma).

Sintoma, como o código o descreveu para o agente:

> O campo nome veio diferente da referência em modo normal em 3 itens, por exemplo no id 8: "Ãgua Mineral" em vez de "Água Mineral". A tela mostra 6 linha(s) a menos e 6 a mais que a referência.

Trecho da resposta, como a poda em código deixou para o agente (hash `7fa7e4d45058ea88`):

```text
lista com 14 itens (referência em modo normal: 14); nome diferente em 3 itens; por exemplo: {"id": 8, "nome": "Ãgua Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}
```

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids lex-4 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| tela (árvore de acessibilidade, contra a referência em modo normal) | 1 linha(s) da referência | 7 linha(s) novas |
| corpo de `GET /api/produtos`, campo `nome` | "Água Mineral" (referência em modo normal) | "Ãgua Mineral" em 3 itens |
| conferência do roteiro `grid com 14 cartões` | 14 elementos | 14 elementos |
| conferência do roteiro `preço do primeiro cartão` | texto no padrão ^R\$ \d+,\d{2}$ | R$ 89,90 |
| conferência do roteiro `sem mensagem de erro na carga` | texto no padrão ^$ |  |

A referência em modo normal desta corrida é a trilha `fase4_tela_v4/referencia/api-catalogo@normal`: é contra ela que a poda comparou a tela e o corpo.

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 1 (léxica: o corpo da resposta nem dá para ler); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 1 (léxica); nível 2 (médio). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `codificacao_incorreta` (Codificação de caracteres incorreta; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/codificacao_incorreta.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/codificacao_incorreta.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Verbetes entregues pela busca e não citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Caso escrito: `lex-4` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/lex-4@tela` em `trilha_tela.jsonl`, eventos 67 a 106, hash dos eventos `64f887099a7f6e06`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/lex-4@tela.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids lex-4 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `codificacao_incorreta` (Codificação de caracteres incorreta). Campo: `nome`. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,99 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê nomes com acentos corrompidos em alguns itens do cardápio.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu codificacao_incorreta no campo nome porque o sinal nome: esperado "Água Mineral" (referência em modo normal), recebido "Ãgua Mineral" em 3 itens está presente na resposta HTTP e os verbetes codificacao_incorreta, entidade-produto, contrato-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Poda de `arvore` (evento 79), feita em código antes de montar o prompt: 193 nós antes, 45 linhas depois. Regras aplicadas: `cartoes_omitidos` 10, `decoracao_removida` 1, `headings_removidos` 1, `imagens_removidas` 16, `interativos_sem_nome_removidos` 8, `listas_achatadas` 14, `textos_sem_letra_removidos` 3.

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

Também podado em código o `corpo_http` (evento 81): de 2071 caracteres para 243 caracteres, pelas regras `diff_contra_contrato`, `diff_contra_referencia`.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| nome | "Água Mineral" (referência em modo normal) | "Ãgua Mineral" em 3 itens |

O que sobrou desta poda (hash `7fa7e4d45058ea88`):

```text
lista com 14 itens (referência em modo normal: 14); nome diferente em 3 itens; por exemplo: {"id": 8, "nome": "Ãgua Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}
```

Interceptação (evento 74): `GET /api/produtos`, status 200 (a API respondeu sem código de erro); corpo guardado com o hash `0fd45da79aa14f8a`.

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> codificacao_incorreta e não tipo_divergente: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: codificacao_incorreta, entidade-produto, contrato-produto

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `codificacao_incorreta` (Codificação de caracteres incorreta) | 0,99 | sim |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[codificacao_incorreta] [entidade-produto]`; verbetes citados: `codificacao_incorreta` (Codificação de caracteres incorreta; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/codificacao_incorreta.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/codificacao_incorreta.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `codificacao_incorreta` | confere |  |
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `codificacao_incorreta` | confere | contexto: `codificacao_incorreta`, `entidade-produto`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `codificacao_incorreta`, `entidade-produto`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | confere | verbetes: `codificacao_incorreta` |
| A linha FONTE só tem identificadores, no formato pedido | `[codificacao_incorreta] [entidade-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["codificacao_incorreta", "entidade-produto"]} |
| O verbete citado fala da causa respondida | `codificacao_incorreta` | confere | {"termo": "codificacao_incorreta"} |
| O verbete citado fala da causa respondida | `entidade-produto` | não confere | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `nome` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids lex-4 --k 3`

## 17. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 67 | 1 | entrada | programa | ao_vivo | 2026-11-06T09:56:31 | caso lex-4 |
| 68 | 2 | acao | programa | ao_vivo | 2026-11-06T09:56:31 | passo 1: abrir produtos_api.php |
| 69 | 3 | acao | programa | ao_vivo | 2026-11-06T09:56:31 | passo 2: esperar aparecer #produtos-api-grid .saiba-mais, #produtos-api-status.text-danger |
| 70 | 4 | acao | programa | ao_vivo | 2026-11-06T09:56:31 | passo 3: conferir #produtos-api-grid .saiba-mais |
| 71 | 5 | acao | programa | ao_vivo | 2026-11-06T09:56:31 | passo 4: conferir #produtos-api-grid .thumbnail .btn-default |
| 72 | 6 | acao | programa | ao_vivo | 2026-11-06T09:56:31 | passo 5: conferir #produtos-api-status |
| 74 | 7 | interceptacao | programa | ao_vivo | 2026-11-06T09:56:31 | GET /api/produtos 200 |
| 75 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T09:56:31 | conferencia_do_roteiro: confere |
| 76 | 9 | verificacao | verificacao | ao_vivo | 2026-11-06T09:56:31 | conferencia_do_roteiro: confere |
| 77 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T09:56:31 | conferencia_do_roteiro: confere |
| 79 | 11 | poda | programa | ao_vivo | 2026-11-06T09:56:31 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 81 | 12 | poda | programa | ao_vivo | 2026-11-06T09:56:31 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 82 | 13 | candidatos | programa | ao_vivo | 2026-11-06T09:56:31 | 3 de 39 verbetes entregues |
| 84 | 14 | prompt | programa | ao_vivo | 2026-11-06T09:56:31 | diagnostico: 3807 caracteres; verbetes codificacao_incorreta, entidade-produto, contrato-produto |
| 86 | 15 | inferencia | programa | ao_vivo | 2026-11-06T09:56:31 | diagnostico: 76,4 s |
| 87 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T09:56:31 | causa_raiz: `codificacao_incorreta` |
| 88 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T09:56:31 | campo: `nome` |
| 89 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T09:56:31 | impacto: `O usuário vê nomes com acentos corrompidos em alguns itens do cardápio.` |
| 90 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T09:56:31 | fonte: `[codificacao_incorreta] [entidade-produto]` |
| 91 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T09:56:31 | fonte_citada: `codificacao_incorreta` |
| 92 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T09:56:31 | fonte_citada: `entidade-produto` |
| 93 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T09:56:31 | quatro_linhas_presentes: confere |
| 94 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T09:56:31 | rotulo_no_conjunto: confere |
| 95 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T09:56:31 | fonte_existe_na_biblioteca: confere |
| 96 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T09:56:31 | fonte_existe_na_biblioteca: confere |
| 97 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T09:56:31 | fonte_estava_no_contexto: confere |
| 98 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T09:56:31 | fonte_estava_no_contexto: confere |
| 99 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T09:56:31 | campo_existe_no_caso: confere |
| 100 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T09:56:31 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 101 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T09:56:31 | notas_nos_verbetes_citados: informativo |
| 102 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T09:56:31 | impacto: nao_verificavel |
| 103 | 32 | verificacao | verificacao | ao_vivo | 2026-11-06T09:56:31 | fonte_formato_valido: confere |
| 104 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T09:56:31 | fonte_contem_termo_da_causa: confere |
| 105 | 34 | verificacao | verificacao | ao_vivo | 2026-11-06T09:56:31 | fonte_contem_termo_da_causa: nao_confere |
| 106 | 35 | decisao | programa | ao_vivo | 2026-11-06T09:56:31 | diagnostico: escolha codificacao_incorreta; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 106, decisão `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido.
  - Evidência: evento 81 (sinal_em_codigo); evento 79 (arvore_podada); evento 74 (corpo_http); evento 82 (verbete_entregue: `codificacao_incorreta`, `entidade-produto`, `contrato-produto`); evento 86 (resposta); evento 91 (verbete_citado: `codificacao_incorreta`); evento 92 (verbete_citado: `entidade-produto`).
  - Usou: `codificacao_incorreta`, `entidade-produto`, `contrato-produto`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 67 a 106 da trilha; hash dos eventos deste caso: `64f887099a7f6e06`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
