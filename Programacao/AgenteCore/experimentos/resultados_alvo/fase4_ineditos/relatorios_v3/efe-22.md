<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Localizador (seletor) quebrado em `GET /api/produtos`

Caso `efe-22` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/efe-22`: o caso `efe-22` na corrida `fase4_ineditos`; eventos 741 a 762 da trilha `trilha_ineditos.jsonl`, hash dos eventos `9ab0baf477d84a4f` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Localizador (seletor) quebrado em `GET /api/produtos`

## 3. Data, organização e autor

Observado em 06/11/2026 14:27:36 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `efe-22`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 6 (efeito: o que o usuário vê na tela está errado); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]
```

Árvore de acessibilidade da página, como o caso a trouxe:

```text
document "Churrascaria Fornalha - Produtos (API)"
  navigation
    link "PRODUTOS"
    link "PRODUTOS (API)"
  main
    heading "Produtos via API" level=2
    group
      heading "Fraldinha" level=3
      text "Carnes"
      button "R$ 69,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    group
      heading "Costelona" level=3
      text "Carnes"
      button "R$ 79,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="4"
```

Seletor que falhou: `#saiba-mais-3`.
4. Sintoma observado (texto do caso):

> O passo 'abrir os detalhes da Fraldinha' do roteiro falha ao clicar em #saiba-mais-3: o Playwright espera 5 segundos e desiste sem ter encontrado nenhum elemento com esse seletor. A grade apareceu inteira, sem mensagem de erro, e GET /api/produtos respondeu 200.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids efe-22`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | O passo 'abrir os detalhes da Fraldinha' do roteiro falha ao clicar em #saiba-mais-3: o Playwright espera 5 segundos e desiste sem ter encontrado nenhum elemento com esse seletor. A grade apareceu inteira, sem mensagem de erro, e GET /api/produtos respondeu 200. |

Corpo recebido, como veio no caso:

```text
[{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 6 (efeito: o que o usuário vê na tela está errado); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 6 (efeito); nível 1 (fácil). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `localizador_quebrado` (Localizador (seletor) quebrado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/localizador_quebrado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/localizador_quebrado.md`).
- Verbetes entregues pela busca e não citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Caso escrito: `efe-22` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/efe-22` em `trilha_ineditos.jsonl`, eventos 741 a 762, hash dos eventos `9ab0baf477d84a4f`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids efe-22`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `localizador_quebrado` (Localizador (seletor) quebrado). Campo: nenhum apontado. Confiança: o agente está seguro desta causa (probabilidade 0,99 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário não consegue abrir os detalhes da Fraldinha, pois o seletor #saiba-mais-3 não encontra nenhum elemento correspondente na página.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu localizador_quebrado porque os verbetes contrato-produto, localizador_quebrado, entidade-produto estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]

ÁRVORE DE ACESSIBILIDADE DA PÁGINA:
document "Churrascaria Fornalha - Produtos (API)"
  navigation
    link "PRODUTOS"
    link "PRODUTOS (API)"
  main
    heading "Produtos via API" level=2
    group
      heading "Fraldinha" level=3
      text "Carnes"
      button "R$ 69,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    group
      heading "Costelona" level=3
      text "Carnes"
      button "R$ 79,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="4"


SELETOR QUE FALHOU: #saiba-mais-3

SINTOMA OBSERVADO: O passo 'abrir os detalhes da Fraldinha' do roteiro falha ao clicar em #saiba-mais-3: o Playwright espera 5 segundos e desiste sem ter encontrado nenhum elemento com esse seletor. A grade apareceu inteira, sem mensagem de erro, e GET /api/produtos respondeu 200.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> localizador_quebrado e não campo_ausente: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: contrato-produto, localizador_quebrado, entidade-produto

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `localizador_quebrado` (Localizador (seletor) quebrado) | 0,99 | sim |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `chave_de_juncao_errada` (Chave de junção errada) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `nulo_inesperado` (Nulo inesperado) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado` (Localizador (seletor) quebrado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/localizador_quebrado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/localizador_quebrado.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `contrato-produto`, `localizador_quebrado`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado` |
| A linha FONTE só tem identificadores, no formato pedido | `[localizador_quebrado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["localizador_quebrado"]} |
| O verbete citado fala da causa respondida | `localizador_quebrado` | confere | {"termo": "localizador_quebrado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids efe-22`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 741 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:27:36 | caso efe-22 |
| 742 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:27:36 | 3 de 39 verbetes entregues |
| 744 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:27:36 | diagnostico: 4576 caracteres; verbetes contrato-produto, localizador_quebrado, entidade-produto |
| 746 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:27:36 | diagnostico: 93,0 s |
| 747 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:27:36 | causa_raiz: `localizador_quebrado` |
| 748 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:27:36 | campo: `nenhum` |
| 749 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:27:36 | impacto: `O usuário não consegue abrir os detalhes da Fraldinha, pois o seletor #saiba-mais-3 não encontra nenhum elemento correspondente na página.` |
| 750 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:27:36 | fonte: `[localizador_quebrado]` |
| 751 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:27:36 | fonte_citada: `localizador_quebrado` |
| 752 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:27:36 | quatro_linhas_presentes: confere |
| 753 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:27:36 | rotulo_no_conjunto: confere |
| 754 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:27:36 | fonte_existe_na_biblioteca: confere |
| 755 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:27:36 | fonte_estava_no_contexto: confere |
| 756 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:27:36 | campo_existe_no_caso: nao_se_aplica |
| 757 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:27:36 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 758 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:27:36 | notas_nos_verbetes_citados: informativo |
| 759 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:27:36 | impacto: nao_verificavel |
| 760 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:27:36 | fonte_formato_valido: confere |
| 761 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:27:36 | fonte_contem_termo_da_causa: confere |
| 762 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:27:36 | diagnostico: escolha localizador_quebrado; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 762, decisão `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido.
  - Evidência: evento 742 (verbete_entregue: `contrato-produto`, `localizador_quebrado`, `entidade-produto`); evento 746 (resposta); evento 751 (verbete_citado: `localizador_quebrado`).
  - Usou: `contrato-produto`, `localizador_quebrado`, `entidade-produto`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 741 a 762 da trilha; hash dos eventos deste caso: `9ab0baf477d84a4f`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
