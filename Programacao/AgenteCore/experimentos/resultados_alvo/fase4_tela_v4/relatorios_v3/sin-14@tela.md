<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Campo renomeado em `GET /api/produtos`, campo `imagem`

Caso `sin-14` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/sin-14@tela`: o caso `sin-14` na corrida `fase4_tela_v4`; eventos 896 a 930 da trilha `trilha_tela.jsonl`, hash dos eventos `70b16354c8b50a0a` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Campo renomeado em `GET /api/produtos`, campo `imagem`

## 3. Data, organização e autor

Observado em 06/11/2026 10:29:01 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A página `produtos_api.php` do site PHP (CobaiaFront), que chama a CobaiaAPI em `GET /api/produtos` (host localhost:8000).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Roteiro `api-catalogo` da tela, com a falha injetada `field_renamed` (um campo da resposta vem com o nome trocado, com o sufixo _v2) no campo `imagem`. Caso `sin-14`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 2 (sintática: a forma da resposta não é a esperada); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela).

## 6. Descrição para reproduzir

Passos do roteiro, na ordem em que o agente os executou (os tempos são os medidos):

1. Abrir `produtos_api.php` (0,1 s).
2. Esperar aparecer `#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger` (0,0 s).
3. Conferir `#produtos-api-grid .saiba-mais` (0,0 s).
4. Conferir `#produtos-api-grid .thumbnail .btn-default` (0,0 s).
5. Conferir `#produtos-api-status` (0,0 s).

A página chamou `GET /api/produtos` em localhost:8000 e recebeu status 200 (a API respondeu sem código de erro), `application/json`, 2110 caracteres, em 37,1 ms.

As 3 conferências do roteiro conferem (a tabela do bloco 7 traz cada uma).

Sintoma, como o código o descreveu para o agente:

> O campo imagem veio como imagem_v2. A tela mostra 14 linha(s) a menos que a referência.

Trecho da resposta, como a poda em código deixou para o agente (hash `b2042fcbcc75423a`):

```text
{"imagem_v2": "picanha_alho.jpg"}
```

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-14 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| tela (árvore de acessibilidade, contra a referência em modo normal) | 0 linha(s) da referência | 0 linha(s) novas |
| corpo de `GET /api/produtos`, campo `imagem` | imagem | imagem_v2 |
| conferência do roteiro `grid com 14 cartões` | 14 elementos | 14 elementos |
| conferência do roteiro `preço do primeiro cartão` | texto no padrão ^R\$ \d+,\d{2}$ | R$ 89,90 |
| conferência do roteiro `sem mensagem de erro na carga` | texto no padrão ^$ |  |

A referência em modo normal desta corrida é a trilha `fase4_tela_v4/referencia/api-catalogo@normal`: é contra ela que a poda comparou a tela e o corpo.

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 2 (sintática: a forma da resposta não é a esperada); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 2 (sintática); nível 3 (difícil). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `campo_renomeado` (Campo renomeado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_renomeado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_renomeado.md`).
- Verbetes entregues pela busca e não citados: `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Caso escrito: `sin-14` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/sin-14@tela` em `trilha_tela.jsonl`, eventos 896 a 930, hash dos eventos `70b16354c8b50a0a`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/sin-14@tela.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-14 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `campo_renomeado` (Campo renomeado). Campo: `imagem`. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê um campo desconhecido "imagem_v2" na resposta, o que pode causar confusão e dificuldade na integração da interface com a API.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu campo_renomeado no campo imagem porque o sinal imagem: esperado imagem, recebido imagem_v2 está presente na resposta HTTP e os verbetes campo_ausente, contrato-produto, campo_renomeado estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Poda de `arvore` (evento 907), feita em código antes de montar o prompt: 179 nós antes, 39 linhas depois. Regras aplicadas: `cartoes_omitidos` 11, `decoracao_removida` 1, `headings_removidos` 1, `imagens_removidas` 2, `interativos_sem_nome_removidos` 8, `listas_achatadas` 14, `textos_sem_letra_removidos` 3.

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

Também podado em código o `corpo_http` (evento 909): de 2110 caracteres para 33 caracteres, pelas regras `diff_contra_contrato`, `diff_contra_referencia`.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| imagem | imagem | imagem_v2 |

O que sobrou desta poda (hash `b2042fcbcc75423a`):

```text
{"imagem_v2": "picanha_alho.jpg"}
```

Interceptação (evento 903): `GET /api/produtos`, status 200 (a API respondeu sem código de erro); corpo guardado com o hash `58a3465f7f2815fd`.

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> campo_renomeado e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: campo_ausente, contrato-produto, campo_renomeado

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `campo_renomeado` (Campo renomeado) | 1,00 | sim |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[campo_renomeado]`; verbetes citados: `campo_renomeado` (Campo renomeado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_renomeado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_renomeado.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | confere | contexto: `campo_ausente`, `contrato-produto`, `campo_renomeado` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `campo_ausente`, `contrato-produto`, `campo_renomeado` |
| A linha FONTE só tem identificadores, no formato pedido | `[campo_renomeado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["campo_renomeado"]} |
| O verbete citado fala da causa respondida | `campo_renomeado` | confere | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `imagem` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids sin-14 --k 3`

## 17. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 896 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:29:01 | caso sin-14 |
| 897 | 2 | acao | programa | ao_vivo | 2026-11-06T10:29:01 | passo 1: abrir produtos_api.php |
| 898 | 3 | acao | programa | ao_vivo | 2026-11-06T10:29:01 | passo 2: esperar aparecer #produtos-api-grid .saiba-mais, #produtos-api-status.text-danger |
| 899 | 4 | acao | programa | ao_vivo | 2026-11-06T10:29:01 | passo 3: conferir #produtos-api-grid .saiba-mais |
| 900 | 5 | acao | programa | ao_vivo | 2026-11-06T10:29:01 | passo 4: conferir #produtos-api-grid .thumbnail .btn-default |
| 901 | 6 | acao | programa | ao_vivo | 2026-11-06T10:29:01 | passo 5: conferir #produtos-api-status |
| 903 | 7 | interceptacao | programa | ao_vivo | 2026-11-06T10:29:01 | GET /api/produtos 200 |
| 904 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | conferencia_do_roteiro: confere |
| 905 | 9 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | conferencia_do_roteiro: confere |
| 906 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | conferencia_do_roteiro: confere |
| 907 | 11 | poda | programa | ao_vivo | 2026-11-06T10:29:01 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 909 | 12 | poda | programa | ao_vivo | 2026-11-06T10:29:01 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 910 | 13 | candidatos | programa | ao_vivo | 2026-11-06T10:29:01 | 3 de 39 verbetes entregues |
| 912 | 14 | prompt | programa | ao_vivo | 2026-11-06T10:29:01 | diagnostico: 3492 caracteres; verbetes campo_ausente, contrato-produto, campo_renomeado |
| 914 | 15 | inferencia | programa | ao_vivo | 2026-11-06T10:29:01 | diagnostico: 70,6 s |
| 915 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T10:29:01 | causa_raiz: `campo_renomeado` |
| 916 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T10:29:01 | campo: `imagem` |
| 917 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T10:29:01 | impacto: `O usuário vê um campo desconhecido "imagem_v2" na resposta, o que pode causar confusão e dificuldade na integração da interface com a API.` |
| 918 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T10:29:01 | fonte: `[campo_renomeado]` |
| 919 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T10:29:01 | fonte_citada: `campo_renomeado` |
| 920 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | quatro_linhas_presentes: confere |
| 921 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | rotulo_no_conjunto: confere |
| 922 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | fonte_existe_na_biblioteca: confere |
| 923 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | fonte_estava_no_contexto: confere |
| 924 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | campo_existe_no_caso: confere |
| 925 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 926 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | notas_nos_verbetes_citados: informativo |
| 927 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | impacto: nao_verificavel |
| 928 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | fonte_formato_valido: confere |
| 929 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T10:29:01 | fonte_contem_termo_da_causa: confere |
| 930 | 31 | decisao | programa | ao_vivo | 2026-11-06T10:29:01 | diagnostico: escolha campo_renomeado; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 930, decisão `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido.
  - Evidência: evento 909 (sinal_em_codigo); evento 907 (arvore_podada); evento 903 (corpo_http); evento 910 (verbete_entregue: `campo_ausente`, `contrato-produto`, `campo_renomeado`); evento 914 (resposta); evento 919 (verbete_citado: `campo_renomeado`).
  - Usou: `campo_ausente`, `contrato-produto`, `campo_renomeado`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 896 a 930 da trilha; hash dos eventos deste caso: `70b16354c8b50a0a`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
