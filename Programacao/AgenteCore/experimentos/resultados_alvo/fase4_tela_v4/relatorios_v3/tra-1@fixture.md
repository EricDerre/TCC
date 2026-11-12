<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Escala ou unidade errada em `GET /api/produtos`, campo `preco`

Caso `tra-1` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/tra-1@fixture`: o caso `tra-1` na corrida `fase4_tela_v4`; eventos 354 a 375 da trilha `trilha_tela.jsonl`, hash dos eventos `d1a0cc4fb48146cc` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Escala ou unidade errada em `GET /api/produtos`, campo `preco`

## 3. Data, organização e autor

Observado em 06/11/2026 10:07:22 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `tra-1`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 4 (tradução: o mapeamento entre as camadas está errado); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 8990, "imagem": "picanha_alho.jpg", "destaque": true}]
```

4. Sintoma observado (texto do caso):

> Os precos aparecem cem vezes maiores: 'R$ 8.990,00' para a picanha.

5. Observação adicional (texto do caso):

> No banco, tbprodutos.valor_produto do id 1 vale 89.90.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-1 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | Os precos aparecem cem vezes maiores: 'R$ 8.990,00' para a picanha. |

Corpo recebido, como veio no caso:

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 8990, "imagem": "picanha_alho.jpg", "destaque": true}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 4 (tradução: o mapeamento entre as camadas está errado); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 4 (tradução); nível 2 (médio). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `escala_ou_unidade_errada` (Escala ou unidade errada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/escala_ou_unidade_errada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/escala_ou_unidade_errada.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Caso escrito: `tra-1` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/tra-1@fixture` em `trilha_tela.jsonl`, eventos 354 a 375, hash dos eventos `d1a0cc4fb48146cc`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/tra-1@fixture.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-1 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `escala_ou_unidade_errada` (Escala ou unidade errada). Campo: `preco`. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê preços cem vezes maiores do que o esperado, como 'R$ 8.990,00' para a picanha.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu escala_ou_unidade_errada no campo preco porque os verbetes entidade-produto, escala_ou_unidade_errada, contrato-produto estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 8990, "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: Os precos aparecem cem vezes maiores: 'R$ 8.990,00' para a picanha.

OBSERVAÇÃO ADICIONAL: No banco, tbprodutos.valor_produto do id 1 vale 89.90.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> escala_ou_unidade_errada e não valor_fora_do_dominio: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, escala_ou_unidade_errada, contrato-produto

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 1,00 | sim |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `estado_da_tela_divergente` (Estado da tela divergente da resposta) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[escala_ou_unidade_errada]`; verbetes citados: `escala_ou_unidade_errada` (Escala ou unidade errada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/escala_ou_unidade_errada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/escala_ou_unidade_errada.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `escala_ou_unidade_errada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `escala_ou_unidade_errada` | confere | contexto: `entidade-produto`, `escala_ou_unidade_errada`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `escala_ou_unidade_errada` | confere | verbetes: `entidade-produto`, `escala_ou_unidade_errada` |
| A linha FONTE só tem identificadores, no formato pedido | `[escala_ou_unidade_errada]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["escala_ou_unidade_errada"]} |
| O verbete citado fala da causa respondida | `escala_ou_unidade_errada` | confere | {"termo": "escala_ou_unidade_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-1 --k 3`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 354 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:07:22 | caso tra-1 |
| 355 | 2 | candidatos | programa | ao_vivo | 2026-11-06T10:07:22 | 3 de 39 verbetes entregues |
| 357 | 3 | prompt | programa | ao_vivo | 2026-11-06T10:07:22 | diagnostico: 3896 caracteres; verbetes entidade-produto, escala_ou_unidade_errada, contrato-produto |
| 359 | 4 | inferencia | programa | ao_vivo | 2026-11-06T10:07:22 | diagnostico: 83,5 s |
| 360 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T10:07:22 | causa_raiz: `escala_ou_unidade_errada` |
| 361 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T10:07:22 | campo: `preco` |
| 362 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T10:07:22 | impacto: `O usuário vê preços cem vezes maiores do que o esperado, como 'R$ 8.990,00' para a picanha.` |
| 363 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T10:07:22 | fonte: `[escala_ou_unidade_errada]` |
| 364 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T10:07:22 | fonte_citada: `escala_ou_unidade_errada` |
| 365 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T10:07:22 | quatro_linhas_presentes: confere |
| 366 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T10:07:22 | rotulo_no_conjunto: confere |
| 367 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T10:07:22 | fonte_existe_na_biblioteca: confere |
| 368 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T10:07:22 | fonte_estava_no_contexto: confere |
| 369 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T10:07:22 | campo_existe_no_caso: confere |
| 370 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T10:07:22 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 371 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T10:07:22 | notas_nos_verbetes_citados: informativo |
| 372 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T10:07:22 | impacto: nao_verificavel |
| 373 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T10:07:22 | fonte_formato_valido: confere |
| 374 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T10:07:22 | fonte_contem_termo_da_causa: confere |
| 375 | 20 | decisao | programa | ao_vivo | 2026-11-06T10:07:22 | diagnostico: escolha escala_ou_unidade_errada; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 375, decisão `diagnostico`: escolha `escala_ou_unidade_errada`; resultado rotulo_emitido.
  - Evidência: evento 355 (verbete_entregue: `entidade-produto`, `escala_ou_unidade_errada`, `contrato-produto`); evento 359 (resposta); evento 364 (verbete_citado: `escala_ou_unidade_errada`).
  - Usou: `entidade-produto`, `escala_ou_unidade_errada`, `contrato-produto`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 354 a 375 da trilha; hash dos eventos deste caso: `d1a0cc4fb48146cc`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
