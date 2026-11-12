<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Tipo divergente em `GET /api/produtos`, campo `preco`

Caso `contrato-type_drift#1` da corrida `fase4_ensaio_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ensaio_v4/qwen2.5_7b/contrato-type_drift#1`: o caso `contrato-type_drift#1` na corrida `fase4_ensaio_v4`; eventos 113 a 151 da trilha `trilha_cenarios.jsonl`, hash dos eventos `22bcc9450b8ea71d` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Tipo divergente em `GET /api/produtos`, campo `preco`

## 3. Data, organização e autor

Observado em 06/11/2026 11:17:47 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 11:13:26 a 06/11/2026 11:26:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `cenarios`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A página `produtos_api.php` do site PHP (CobaiaFront), que chama a CobaiaAPI em `GET /api/produtos` (host localhost:8000).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Roteiro `api-catalogo` da tela, com a falha injetada `type_drift` (um campo da resposta vem com outro tipo: número vira texto, e texto vira o inteiro 1) no campo `preco`. Caso `contrato-type_drift#1`, de `cenarios_fase4.py` (catálogo dos dez cenários do ensaio da Fase 5, ficha 36); classe 3 (semântica: os tipos ou os domínios dos valores não fazem sentido); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato).

## 6. Descrição para reproduzir

Passos do roteiro, na ordem em que o agente os executou (os tempos são os medidos):

1. Abrir `produtos_api.php` (0,2 s).
2. Esperar aparecer `#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger` (0,0 s).
3. Conferir `#produtos-api-grid .saiba-mais` (0,0 s).
4. Conferir `#produtos-api-grid .thumbnail .btn-default` (0,0 s).
5. Conferir `#produtos-api-status` (0,0 s).

A página chamou `GET /api/produtos` em localhost:8000 e recebeu status 200 (a API respondeu sem código de erro), `application/json`, 2096 caracteres, em 36,8 ms.

As 3 conferências do roteiro conferem (a tabela do bloco 7 traz cada uma).

Sintoma, como o código o descreveu para o agente:

> O campo preco veio como texto em vez de numero.

Trecho da resposta, como a poda em código deixou para o agente (hash `b48b1bab39e02551`):

```text
{"preco": "89.9"}
```

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| tela (árvore de acessibilidade, contra a referência em modo normal) | 0 linha(s) da referência | 0 linha(s) novas |
| corpo de `GET /api/produtos`, campo `preco` | numero | texto |
| corpo de `GET /api/produtos`, campo `preco` | 89.9 (referência em modo normal) | "89.9" em 14 itens |
| conferência do roteiro `grid com 14 cartões` | 14 elementos | 14 elementos |
| conferência do roteiro `preço do primeiro cartão` | texto no padrão ^R\$ \d+,\d{2}$ | R$ 89,90 |
| conferência do roteiro `sem mensagem de erro na carga` | texto no padrão ^$ |  |

A referência em modo normal desta corrida é a trilha `fase4_ensaio_v4/referencia/api-catalogo@normal`: é contra ela que a poda comparou a tela e o corpo.

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 3 (semântica: os tipos ou os domínios dos valores não fazem sentido); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 3 (semântica); nível 2 (médio). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `tipo_divergente` (Tipo divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/tipo_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/tipo_divergente.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Caso escrito: `contrato-type_drift#1` em `cenarios_fase4.py` (catálogo dos dez cenários do ensaio da Fase 5, ficha 36).
- Trilha: `fase4_ensaio_v4/qwen2.5_7b/contrato-type_drift#1` em `trilha_cenarios.jsonl`, eventos 113 a 151, hash dos eventos `22bcc9450b8ea71d`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/contrato-type_drift__r1.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `tipo_divergente` (Tipo divergente). Campo: `preco`. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê o preço como um texto em vez de um número, o que pode causar problemas na exibição correta do valor.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu tipo_divergente no campo preco porque o sinal preco: esperado numero, recebido texto está presente na resposta HTTP e os verbetes contrato-produto, entidade-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Poda de `arvore` (evento 124), feita em código antes de montar o prompt: 193 nós antes, 39 linhas depois. Regras aplicadas: `cartoes_omitidos` 11, `decoracao_removida` 1, `headings_removidos` 1, `imagens_removidas` 16, `interativos_sem_nome_removidos` 8, `listas_achatadas` 14, `textos_sem_letra_removidos` 3.

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

Também podado em código o `corpo_http` (evento 126): de 2096 caracteres para 17 caracteres, pelas regras `diff_contra_contrato`, `diff_contra_referencia`.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | numero | texto |
| preco | 89.9 (referência em modo normal) | "89.9" em 14 itens |

O que sobrou desta poda (hash `b48b1bab39e02551`):

```text
{"preco": "89.9"}
```

Interceptação (evento 120): `GET /api/produtos`, status 200 (a API respondeu sem código de erro); corpo guardado com o hash `c7c256cfe391ed57`.

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> tipo_divergente e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-produto, entidade-produto, tipo_divergente

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `tipo_divergente` (Tipo divergente) | 1,00 | sim |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [tipo_divergente]`; verbetes citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `tipo_divergente` (Tipo divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/tipo_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/tipo_divergente.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `tipo_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `contrato-produto`, `entidade-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `contrato-produto`, `entidade-produto`, `tipo_divergente` |
| A linha FONTE só tem identificadores, no formato pedido | `[contrato-produto], [tipo_divergente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto", "tipo_divergente"]} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "tipo_divergente"} |
| O verbete citado fala da causa respondida | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`

## 17. Árvore completa

<details><summary>35 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 113 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:17:47 | caso contrato-type_drift#1 |
| 114 | 2 | acao | programa | ao_vivo | 2026-11-06T11:17:47 | passo 1: abrir produtos_api.php |
| 115 | 3 | acao | programa | ao_vivo | 2026-11-06T11:17:47 | passo 2: esperar aparecer #produtos-api-grid .saiba-mais, #produtos-api-status.text-danger |
| 116 | 4 | acao | programa | ao_vivo | 2026-11-06T11:17:47 | passo 3: conferir #produtos-api-grid .saiba-mais |
| 117 | 5 | acao | programa | ao_vivo | 2026-11-06T11:17:47 | passo 4: conferir #produtos-api-grid .thumbnail .btn-default |
| 118 | 6 | acao | programa | ao_vivo | 2026-11-06T11:17:47 | passo 5: conferir #produtos-api-status |
| 120 | 7 | interceptacao | programa | ao_vivo | 2026-11-06T11:17:47 | GET /api/produtos 200 |
| 121 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T11:17:47 | conferencia_do_roteiro: confere |
| 122 | 9 | verificacao | verificacao | ao_vivo | 2026-11-06T11:17:47 | conferencia_do_roteiro: confere |
| 123 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:17:47 | conferencia_do_roteiro: confere |
| 124 | 11 | poda | programa | ao_vivo | 2026-11-06T11:17:47 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 126 | 12 | poda | programa | ao_vivo | 2026-11-06T11:17:47 | corpo_http: 2 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 127 | 13 | candidatos | programa | ao_vivo | 2026-11-06T11:17:47 | 3 de 39 verbetes entregues |
| 129 | 14 | prompt | programa | ao_vivo | 2026-11-06T11:17:47 | diagnostico: 3485 caracteres; verbetes contrato-produto, entidade-produto, tipo_divergente |
| 131 | 15 | inferencia | programa | ao_vivo | 2026-11-06T11:17:47 | diagnostico: 71,4 s |
| 132 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T11:17:47 | causa_raiz: `tipo_divergente` |
| 133 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T11:17:47 | campo: `preco` |
| 134 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T11:17:47 | impacto: `O usuário vê o preço como um texto em vez de um número, o que pode causar problemas na exibição correta do valor.` |
| 135 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T11:17:47 | fonte: `[contrato-produto], [tipo_divergente]` |
| 136 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T11:17:47 | fonte_citada: `contrato-produto` |
| 137 | 21 | declaracao | modelo | ao_vivo | 2026-11-06T11:17:47 | fonte_citada: `tipo_divergente` |
| 138 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:17:47 | quatro_linhas_presentes: confere |
| 139 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:17:47 | rotulo_no_conjunto: confere |
| 140 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:17:47 | fonte_existe_na_biblioteca: confere |
| 141 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:17:47 | fonte_existe_na_biblioteca: confere |
| 142 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:17:47 | fonte_estava_no_contexto: confere |
| 143 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T11:17:47 | fonte_estava_no_contexto: confere |
| 144 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T11:17:47 | campo_existe_no_caso: confere |
| 145 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T11:17:47 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 146 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T11:17:47 | notas_nos_verbetes_citados: informativo |
| 147 | 31 | verificacao | verificacao | ao_vivo | 2026-11-06T11:17:47 | impacto: nao_verificavel |
| 148 | 32 | verificacao | verificacao | ao_vivo | 2026-11-06T11:17:47 | fonte_formato_valido: confere |
| 149 | 33 | verificacao | verificacao | ao_vivo | 2026-11-06T11:17:47 | fonte_contem_termo_da_causa: nao_confere |
| 150 | 34 | verificacao | verificacao | ao_vivo | 2026-11-06T11:17:47 | fonte_contem_termo_da_causa: confere |
| 151 | 35 | decisao | programa | ao_vivo | 2026-11-06T11:17:47 | diagnostico: escolha tipo_divergente; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 151, decisão `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido.
  - Evidência: evento 126 (sinal_em_codigo); evento 124 (arvore_podada); evento 120 (corpo_http); evento 127 (verbete_entregue: `contrato-produto`, `entidade-produto`, `tipo_divergente`); evento 131 (resposta); evento 136 (verbete_citado: `contrato-produto`); evento 137 (verbete_citado: `tipo_divergente`).
  - Usou: `contrato-produto`, `entidade-produto`, `tipo_divergente`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 113 a 151 da trilha; hash dos eventos deste caso: `22bcc9450b8ea71d`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
