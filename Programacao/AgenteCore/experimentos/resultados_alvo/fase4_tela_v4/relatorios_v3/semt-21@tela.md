<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Campo renomeado em `GET /api/produtos`, campo `nome`

Caso `semt-21` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/semt-21@tela`: o caso `semt-21` na corrida `fase4_tela_v4`; eventos 1792 a 1827 da trilha `trilha_tela.jsonl`, hash dos eventos `a8b8ede1beb4d7e9` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Campo renomeado em `GET /api/produtos`, campo `nome`

## 3. Data, organização e autor

Observado em 06/11/2026 10:59:16 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A página `produtos_api.php` do site PHP (CobaiaFront), que chama a CobaiaAPI em `GET /api/produtos` (host localhost:8000).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Roteiro `api-catalogo` da tela, com a falha injetada `valor_fora_do_dominio` (um valor vem fora do domínio permitido (número negativo, status desconhecido, booleano como texto)) no campo `nome`. Caso `semt-21`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 3 (semântica: os tipos ou os domínios dos valores não fazem sentido); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela).

## 6. Descrição para reproduzir

Passos do roteiro, na ordem em que o agente os executou (os tempos são os medidos):

1. Abrir `produtos_api.php` (0,2 s).
2. Esperar aparecer `#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger` (0,0 s).
3. Conferir `#produtos-api-grid .saiba-mais` (0,0 s).
4. Conferir `#produtos-api-grid .thumbnail .btn-default` (0,0 s).
5. Conferir `#produtos-api-status` (0,0 s).

A página chamou `GET /api/produtos` em localhost:8000 e recebeu status 200 (a API respondeu sem código de erro), `application/json`, 2222 caracteres, em 35,1 ms.

As 3 conferências do roteiro conferem (a tabela do bloco 7 traz cada uma).

Sintoma, como o código o descreveu para o agente:

> O campo nome veio diferente da referência em modo normal em 14 itens, por exemplo no id 1: "Picanha ao Alho (inválido)" em vez de "Picanha ao Alho". A tela mostra 28 linha(s) a menos e 28 a mais que a referência.

Trecho da resposta, como a poda em código deixou para o agente (hash `f1b7bc81a1c9c347`):

```text
lista com 14 itens (referência em modo normal: 14); nome diferente em 14 itens; por exemplo: {"id": 1, "nome": "Picanha ao Alho (inválido)", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids semt-21 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| tela (árvore de acessibilidade, contra a referência em modo normal) | 3 linha(s) da referência | 3 linha(s) novas |
| corpo de `GET /api/produtos`, campo `nome` | "Picanha ao Alho" (referência em modo normal) | "Picanha ao Alho (inválido)" em 14 itens |
| conferência do roteiro `grid com 14 cartões` | 14 elementos | 14 elementos |
| conferência do roteiro `preço do primeiro cartão` | texto no padrão ^R\$ \d+,\d{2}$ | R$ 89,90 |
| conferência do roteiro `sem mensagem de erro na carga` | texto no padrão ^$ |  |

A referência em modo normal desta corrida é a trilha `fase4_tela_v4/referencia/api-catalogo@normal`: é contra ela que a poda comparou a tela e o corpo.

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 3 (semântica: os tipos ou os domínios dos valores não fazem sentido); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 3 (semântica); nível 3 (difícil). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Verbetes entregues pela busca e não citados: `valor_fora_do_dominio` (Valor fora do domínio; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/valor_fora_do_dominio.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/valor_fora_do_dominio.md`); `fluxo-reserva-e-cancelamento` (Fluxo de reservar e cancelar; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/fluxo-reserva-e-cancelamento.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/fluxo-reserva-e-cancelamento.md`).
- Caso escrito: `semt-21` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/semt-21@tela` em `trilha_tela.jsonl`, eventos 1792 a 1827, hash dos eventos `a8b8ede1beb4d7e9`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/semt-21@tela.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids semt-21 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `campo_renomeado` (Campo renomeado). Campo: `nome`. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê nomes incorretos dos produtos na tela, com adição de parênteses e texto inválido.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu campo_renomeado no campo nome porque o sinal nome: esperado "Picanha ao Alho" (referência em modo normal), recebido "Picanha ao Alho (inválido)" em 14 itens está presente na resposta HTTP e os verbetes valor_fora_do_dominio, entidade-produto, fluxo-reserva-e-cancelamento estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida campo_renomeado. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

Conflito: o que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida campo_renomeado.

Falha registrada no nó: `causa_sem_verbete_que_a_trate` (origem: modelo).

## 13. Evidência

Poda de `arvore` (evento 1804), feita em código antes de montar o prompt: 193 nós antes, 39 linhas depois. Regras aplicadas: `cartoes_omitidos` 11, `decoracao_removida` 1, `headings_removidos` 1, `imagens_removidas` 16, `interativos_sem_nome_removidos` 8, `listas_achatadas` 14, `textos_sem_letra_removidos` 3.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `769513c6cbb48e95`):

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
      heading "Picanha ao Alho (inválido)" level=3
      text "Carnes"
      text "Picanha grelhada com alho laminado na brasa"
      text "destaque: Sim"
      button "R$ 89,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples (inválido)" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 84,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha (inválido)" level=3
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

Também podado em código o `corpo_http` (evento 1806): de 2222 caracteres para 278 caracteres, pelas regras `diff_contra_contrato`, `diff_contra_referencia`.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| nome | "Picanha ao Alho" (referência em modo normal) | "Picanha ao Alho (inválido)" em 14 itens |

O que sobrou desta poda (hash `f1b7bc81a1c9c347`):

```text
lista com 14 itens (referência em modo normal: 14); nome diferente em 14 itens; por exemplo: {"id": 1, "nome": "Picanha ao Alho (inválido)", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 1799): `GET /api/produtos`, status 200 (a API respondeu sem código de erro); corpo guardado com o hash `29cb154c9a798040`.

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> campo_renomeado e não valor_fora_do_dominio: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: valor_fora_do_dominio, entidade-produto, fluxo-reserva-e-cancelamento

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `campo_renomeado` (Campo renomeado) | 1,00 | sim |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `chave_de_juncao_errada` (Chave de junção errada) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto]`; verbetes citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `valor_fora_do_dominio`, `entidade-produto`, `fluxo-reserva-e-cancelamento` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | não confere | nenhum verbete do contexto trata dessa causa |
| A linha FONTE só tem identificadores, no formato pedido | `[entidade-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["entidade-produto"]} |
| O verbete citado fala da causa respondida | `entidade-produto` | não confere | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `nome` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids semt-21 --k 3`

## 17. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1792 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:59:16 | caso semt-21 |
| 1793 | 2 | acao | programa | ao_vivo | 2026-11-06T10:59:16 | passo 1: abrir produtos_api.php |
| 1794 | 3 | acao | programa | ao_vivo | 2026-11-06T10:59:16 | passo 2: esperar aparecer #produtos-api-grid .saiba-mais, #produtos-api-status.text-danger |
| 1795 | 4 | acao | programa | ao_vivo | 2026-11-06T10:59:16 | passo 3: conferir #produtos-api-grid .saiba-mais |
| 1796 | 5 | acao | programa | ao_vivo | 2026-11-06T10:59:16 | passo 4: conferir #produtos-api-grid .thumbnail .btn-default |
| 1797 | 6 | acao | programa | ao_vivo | 2026-11-06T10:59:16 | passo 5: conferir #produtos-api-status |
| 1799 | 7 | interceptacao | programa | ao_vivo | 2026-11-06T10:59:16 | GET /api/produtos 200 |
| 1800 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T10:59:16 | conferencia_do_roteiro: confere |
| 1801 | 9 | verificacao | verificacao | ao_vivo | 2026-11-06T10:59:16 | conferencia_do_roteiro: confere |
| 1802 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T10:59:16 | conferencia_do_roteiro: confere |
| 1804 | 11 | poda | programa | ao_vivo | 2026-11-06T10:59:16 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 1806 | 12 | poda | programa | ao_vivo | 2026-11-06T10:59:16 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1807 | 13 | candidatos | programa | ao_vivo | 2026-11-06T10:59:16 | 3 de 39 verbetes entregues |
| 1809 | 14 | prompt | programa | ao_vivo | 2026-11-06T10:59:16 | diagnostico: 3885 caracteres; verbetes valor_fora_do_dominio, entidade-produto, fluxo-reserva-e-cancelamento |
| 1811 | 15 | inferencia | programa | ao_vivo | 2026-11-06T10:59:16 | diagnostico: 44,9 s |
| 1812 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T10:59:16 | causa_raiz: `campo_renomeado` |
| 1813 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T10:59:16 | campo: `nome` |
| 1814 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T10:59:16 | impacto: `O usuário vê nomes incorretos dos produtos na tela, com adição de parênteses e texto inválido.` |
| 1815 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T10:59:16 | fonte: `[entidade-produto]` |
| 1816 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T10:59:16 | fonte_citada: `entidade-produto` |
| 1817 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T10:59:16 | quatro_linhas_presentes: confere |
| 1818 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T10:59:16 | rotulo_no_conjunto: confere |
| 1819 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T10:59:16 | fonte_existe_na_biblioteca: confere |
| 1820 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T10:59:16 | fonte_estava_no_contexto: confere |
| 1821 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T10:59:16 | campo_existe_no_caso: confere |
| 1822 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T10:59:16 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 1823 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T10:59:16 | notas_nos_verbetes_citados: informativo |
| 1824 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T10:59:16 | impacto: nao_verificavel |
| 1825 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T10:59:16 | fonte_formato_valido: confere |
| 1826 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T10:59:16 | fonte_contem_termo_da_causa: nao_confere |
| 1827 | 31 | decisao | programa | ao_vivo | 2026-11-06T10:59:16 | diagnostico: escolha campo_renomeado; divergência entre o declarado e o medido: sim |

</details>

Nós de decisão, na ordem:

- evento 1827, decisão `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido.
  - Evidência: evento 1806 (sinal_em_codigo); evento 1804 (arvore_podada); evento 1799 (corpo_http); evento 1807 (verbete_entregue: `valor_fora_do_dominio`, `entidade-produto`, `fluxo-reserva-e-cancelamento`); evento 1811 (resposta); evento 1816 (verbete_citado: `entidade-produto`).
  - Usou: `valor_fora_do_dominio`, `entidade-produto`, `fluxo-reserva-e-cancelamento`.
  - Divergência entre o declarado e o medido: sim; falha: causa_sem_verbete_que_a_trate.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1792 a 1827 da trilha; hash dos eventos deste caso: `a8b8ede1beb4d7e9`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
