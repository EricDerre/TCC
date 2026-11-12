<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Chave de junção errada em `GET /api/produtos`, campo `tipo`

Caso `tra-17` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/tra-17@tela`: o caso `tra-17` na corrida `fase4_tela_v4`; eventos 1852 a 1886 da trilha `trilha_tela.jsonl`, hash dos eventos `693099892b4751f3` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Chave de junção errada em `GET /api/produtos`, campo `tipo`

## 3. Data, organização e autor

Observado em 06/11/2026 11:01:01 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A página `produtos_api.php` do site PHP (CobaiaFront), que chama a CobaiaAPI em `GET /api/produtos` (host localhost:8000).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Roteiro `api-catalogo` da tela, com a falha injetada `chave_de_juncao_errada` (o rótulo de junção (o tipo) vem trocado entre os itens da lista) no campo `tipo`. Caso `tra-17`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 4 (tradução: o mapeamento entre as camadas está errado); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu).

## 6. Descrição para reproduzir

Passos do roteiro, na ordem em que o agente os executou (os tempos são os medidos):

1. Abrir `produtos_api.php` (0,1 s).
2. Esperar aparecer `#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger` (0,0 s).
3. Conferir `#produtos-api-grid .saiba-mais` (0,0 s).
4. Conferir `#produtos-api-grid .thumbnail .btn-default` (0,0 s).
5. Conferir `#produtos-api-status` (0,0 s).

A página chamou `GET /api/produtos` em localhost:8000 e recebeu status 200 (a API respondeu sem código de erro), `application/json`, 2068 caracteres, em 18,5 ms.

As 3 conferências do roteiro conferem (a tabela do bloco 7 traz cada uma).

Sintoma, como o código o descreveu para o agente:

> O campo tipo veio diferente da referência em modo normal em 4 itens, por exemplo no id 7: "Bebidas" em vez de "Carnes".

Trecho da resposta, como a poda em código deixou para o agente (hash `a1a95c61af5cf648`):

```text
lista com 14 itens (referência em modo normal: 14); tipo diferente em 4 itens; por exemplo: {"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Bebidas", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}
```

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-17 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| tela (árvore de acessibilidade, contra a referência em modo normal) | 0 linha(s) da referência | 0 linha(s) novas |
| corpo de `GET /api/produtos`, campo `tipo` | "Carnes" (referência em modo normal) | "Bebidas" em 4 itens |
| conferência do roteiro `grid com 14 cartões` | 14 elementos | 14 elementos |
| conferência do roteiro `preço do primeiro cartão` | texto no padrão ^R\$ \d+,\d{2}$ | R$ 89,90 |
| conferência do roteiro `sem mensagem de erro na carga` | texto no padrão ^$ |  |

A referência em modo normal desta corrida é a trilha `fase4_tela_v4/referencia/api-catalogo@normal`: é contra ela que a poda comparou a tela e o corpo.

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 4 (tradução: o mapeamento entre as camadas está errado); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 4 (tradução); nível 1 (fácil). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `chave_de_juncao_errada` (Chave de junção errada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/chave_de_juncao_errada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/chave_de_juncao_errada.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `tipo_divergente` (Tipo divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/tipo_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/tipo_divergente.md`).
- Caso escrito: `tra-17` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/tra-17@tela` em `trilha_tela.jsonl`, eventos 1852 a 1886, hash dos eventos `693099892b4751f3`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/tra-17@tela.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-17 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `chave_de_juncao_errada` (Chave de junção errada). Campo: `tipo`. Confiança: o agente está seguro desta causa (probabilidade 0,99 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê categorias incorretas atribuídas aos produtos, como "Bebidas" em vez de "Carnes".`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu chave_de_juncao_errada no campo tipo porque o sinal tipo: esperado "Carnes" (referência em modo normal), recebido "Bebidas" em 4 itens está presente na resposta HTTP e os verbetes chave_de_juncao_errada, entidade-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Poda de `arvore` (evento 1863), feita em código antes de montar o prompt: 193 nós antes, 39 linhas depois. Regras aplicadas: `cartoes_omitidos` 11, `decoracao_removida` 1, `headings_removidos` 1, `imagens_removidas` 16, `interativos_sem_nome_removidos` 8, `listas_achatadas` 14, `textos_sem_letra_removidos` 3.

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

Também podado em código o `corpo_http` (evento 1865): de 2068 caracteres para 241 caracteres, pelas regras `diff_contra_contrato`, `diff_contra_referencia`.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| tipo | "Carnes" (referência em modo normal) | "Bebidas" em 4 itens |

O que sobrou desta poda (hash `a1a95c61af5cf648`):

```text
lista com 14 itens (referência em modo normal: 14); tipo diferente em 4 itens; por exemplo: {"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Bebidas", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}
```

Interceptação (evento 1859): `GET /api/produtos`, status 200 (a API respondeu sem código de erro); corpo guardado com o hash `0ef7077cc7a06cfa`.

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> chave_de_juncao_errada e não tipo_divergente: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: chave_de_juncao_errada, entidade-produto, tipo_divergente

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `chave_de_juncao_errada` (Chave de junção errada) | 0,99 | sim |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[chave_de_juncao_errada]`; verbetes citados: `chave_de_juncao_errada` (Chave de junção errada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/chave_de_juncao_errada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/chave_de_juncao_errada.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `chave_de_juncao_errada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `chave_de_juncao_errada` | confere | contexto: `chave_de_juncao_errada`, `entidade-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `chave_de_juncao_errada` | confere | verbetes: `chave_de_juncao_errada`, `entidade-produto` |
| A linha FONTE só tem identificadores, no formato pedido | `[chave_de_juncao_errada]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["chave_de_juncao_errada"]} |
| O verbete citado fala da causa respondida | `chave_de_juncao_errada` | confere | {"termo": "chave_de_juncao_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `tipo` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-17 --k 3`

## 17. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1852 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:01:01 | caso tra-17 |
| 1853 | 2 | acao | programa | ao_vivo | 2026-11-06T11:01:01 | passo 1: abrir produtos_api.php |
| 1854 | 3 | acao | programa | ao_vivo | 2026-11-06T11:01:01 | passo 2: esperar aparecer #produtos-api-grid .saiba-mais, #produtos-api-status.text-danger |
| 1855 | 4 | acao | programa | ao_vivo | 2026-11-06T11:01:01 | passo 3: conferir #produtos-api-grid .saiba-mais |
| 1856 | 5 | acao | programa | ao_vivo | 2026-11-06T11:01:01 | passo 4: conferir #produtos-api-grid .thumbnail .btn-default |
| 1857 | 6 | acao | programa | ao_vivo | 2026-11-06T11:01:01 | passo 5: conferir #produtos-api-status |
| 1859 | 7 | interceptacao | programa | ao_vivo | 2026-11-06T11:01:01 | GET /api/produtos 200 |
| 1860 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | conferencia_do_roteiro: confere |
| 1861 | 9 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | conferencia_do_roteiro: confere |
| 1862 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | conferencia_do_roteiro: confere |
| 1863 | 11 | poda | programa | ao_vivo | 2026-11-06T11:01:01 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 1865 | 12 | poda | programa | ao_vivo | 2026-11-06T11:01:01 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1866 | 13 | candidatos | programa | ao_vivo | 2026-11-06T11:01:01 | 3 de 39 verbetes entregues |
| 1868 | 14 | prompt | programa | ao_vivo | 2026-11-06T11:01:01 | diagnostico: 4239 caracteres; verbetes chave_de_juncao_errada, entidade-produto, tipo_divergente |
| 1870 | 15 | inferencia | programa | ao_vivo | 2026-11-06T11:01:01 | diagnostico: 85,5 s |
| 1871 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T11:01:01 | causa_raiz: `chave_de_juncao_errada` |
| 1872 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T11:01:01 | campo: `tipo` |
| 1873 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T11:01:01 | impacto: `O usuário vê categorias incorretas atribuídas aos produtos, como "Bebidas" em vez de "Carnes".` |
| 1874 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T11:01:01 | fonte: `[chave_de_juncao_errada]` |
| 1875 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T11:01:01 | fonte_citada: `chave_de_juncao_errada` |
| 1876 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | quatro_linhas_presentes: confere |
| 1877 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | rotulo_no_conjunto: confere |
| 1878 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | fonte_existe_na_biblioteca: confere |
| 1879 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | fonte_estava_no_contexto: confere |
| 1880 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | campo_existe_no_caso: confere |
| 1881 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1882 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | notas_nos_verbetes_citados: informativo |
| 1883 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | impacto: nao_verificavel |
| 1884 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | fonte_formato_valido: confere |
| 1885 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T11:01:01 | fonte_contem_termo_da_causa: confere |
| 1886 | 31 | decisao | programa | ao_vivo | 2026-11-06T11:01:01 | diagnostico: escolha chave_de_juncao_errada; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 1886, decisão `diagnostico`: escolha `chave_de_juncao_errada`; resultado rotulo_emitido.
  - Evidência: evento 1865 (sinal_em_codigo); evento 1863 (arvore_podada); evento 1859 (corpo_http); evento 1866 (verbete_entregue: `chave_de_juncao_errada`, `entidade-produto`, `tipo_divergente`); evento 1870 (resposta); evento 1875 (verbete_citado: `chave_de_juncao_errada`).
  - Usou: `chave_de_juncao_errada`, `entidade-produto`, `tipo_divergente`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1852 a 1886 da trilha; hash dos eventos deste caso: `693099892b4751f3`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
