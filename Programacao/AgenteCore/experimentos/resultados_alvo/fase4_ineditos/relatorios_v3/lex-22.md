<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Corpo não é JSON em `GET /api/produtos`

Caso `lex-22` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/lex-22`: o caso `lex-22` na corrida `fase4_ineditos`; eventos 3 a 24 da trilha `trilha_ineditos.jsonl`, hash dos eventos `f63b07f1c84b3e79` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Corpo não é JSON em `GET /api/produtos`

## 3. Data, organização e autor

Observado em 06/11/2026 13:52:34 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `lex-22`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 1 (léxica: o corpo da resposta nem dá para ler); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
<html><body><h1>Erro</h1><p>Falha ao montar a resposta.</p></body></html>
```

4. Sintoma observado (texto do caso):

> A pagina Produtos (API) abre sem nenhum cartao. A linha de status acima da grade fica vermelha e mostra 'Erro ao carregar produtos da CobaiaAPI:' seguido de uma mensagem do navegador que cita o caractere inesperado '<' e diz que o texto nao e JSON valido. O status HTTP da resposta e 200.

5. Observação adicional (texto do caso):

> O Content-Type da resposta e text/html, nao application/json.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids lex-22`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | A pagina Produtos (API) abre sem nenhum cartao. A linha de status acima da grade fica vermelha e mostra 'Erro ao carregar produtos da CobaiaAPI:' seguido de uma mensagem do navegador que cita o caractere inesperado '<' e diz que o texto nao e JSON valido. O status HTTP da resposta e 200. |

Corpo recebido, como veio no caso:

```text
<html><body><h1>Erro</h1><p>Falha ao montar a resposta.</p></body></html>
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 1 (léxica: o corpo da resposta nem dá para ler); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 1 (léxica); nível 1 (fácil). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `corpo_nao_e_json` (Corpo não é JSON; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/corpo_nao_e_json.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/corpo_nao_e_json.md`).
- Verbetes entregues pela busca e não citados: `mensagens-de-erro-do-codigo` (Índice de mensagens literais do código; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/mensagens-de-erro-do-codigo.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/mensagens-de-erro-do-codigo.md`); `corpo_vazio` (Corpo vazio; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/corpo_vazio.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/corpo_vazio.md`).
- Caso escrito: `lex-22` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/lex-22` em `trilha_ineditos.jsonl`, eventos 3 a 24, hash dos eventos `f63b07f1c84b3e79`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids lex-22`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `corpo_nao_e_json` (Corpo não é JSON). Campo: nenhum apontado. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,92 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `A página Produtos exibe uma mensagem de erro e não carrega nenhum cartão de produto.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu corpo_nao_e_json porque os verbetes corpo_nao_e_json, mensagens-de-erro-do-codigo, corpo_vazio estavam entre os entregues ao modelo. A segunda causa, corpo_vazio, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
<html><body><h1>Erro</h1><p>Falha ao montar a resposta.</p></body></html>

SINTOMA OBSERVADO: A pagina Produtos (API) abre sem nenhum cartao. A linha de status acima da grade fica vermelha e mostra 'Erro ao carregar produtos da CobaiaAPI:' seguido de uma mensagem do navegador que cita o caractere inesperado '<' e diz que o texto nao e JSON valido. O status HTTP da resposta e 200.

OBSERVAÇÃO ADICIONAL: O Content-Type da resposta e text/html, nao application/json.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> corpo_nao_e_json e não corpo_vazio: a escolha tem probabilidade 0,92 contra 0,00; verbete(s) na evidência: corpo_nao_e_json, mensagens-de-erro-do-codigo, corpo_vazio

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `corpo_nao_e_json` (Corpo não é JSON) | 0,92 | sim |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[corpo_nao_e_json]`; verbetes citados: `corpo_nao_e_json` (Corpo não é JSON; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/corpo_nao_e_json.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/corpo_nao_e_json.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `corpo_nao_e_json` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `corpo_nao_e_json` | confere | contexto: `corpo_nao_e_json`, `mensagens-de-erro-do-codigo`, `corpo_vazio` |
| Algum verbete do contexto trata da causa respondida | `corpo_nao_e_json` | confere | verbetes: `corpo_nao_e_json`, `mensagens-de-erro-do-codigo`, `corpo_vazio` |
| A linha FONTE só tem identificadores, no formato pedido | `[corpo_nao_e_json]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["corpo_nao_e_json"]} |
| O verbete citado fala da causa respondida | `corpo_nao_e_json` | confere | {"termo": "corpo_nao_e_json"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids lex-22`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3 | 1 | entrada | programa | ao_vivo | 2026-11-06T13:52:34 | caso lex-22 |
| 4 | 2 | candidatos | programa | ao_vivo | 2026-11-06T13:52:34 | 3 de 39 verbetes entregues |
| 6 | 3 | prompt | programa | ao_vivo | 2026-11-06T13:52:34 | diagnostico: 3820 caracteres; verbetes corpo_nao_e_json, mensagens-de-erro-do-codigo, corpo_vazio |
| 8 | 4 | inferencia | programa | ao_vivo | 2026-11-06T13:52:34 | diagnostico: 70,8 s |
| 9 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T13:52:34 | causa_raiz: `corpo_nao_e_json` |
| 10 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T13:52:34 | campo: `nenhum` |
| 11 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T13:52:34 | impacto: `A página Produtos exibe uma mensagem de erro e não carrega nenhum cartão de produto.` |
| 12 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T13:52:34 | fonte: `[corpo_nao_e_json]` |
| 13 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T13:52:34 | fonte_citada: `corpo_nao_e_json` |
| 14 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T13:52:34 | quatro_linhas_presentes: confere |
| 15 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T13:52:34 | rotulo_no_conjunto: confere |
| 16 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T13:52:34 | fonte_existe_na_biblioteca: confere |
| 17 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T13:52:34 | fonte_estava_no_contexto: confere |
| 18 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T13:52:34 | campo_existe_no_caso: nao_se_aplica |
| 19 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T13:52:34 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 20 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T13:52:34 | notas_nos_verbetes_citados: informativo |
| 21 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T13:52:34 | impacto: nao_verificavel |
| 22 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T13:52:34 | fonte_formato_valido: confere |
| 23 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T13:52:34 | fonte_contem_termo_da_causa: confere |
| 24 | 20 | decisao | programa | ao_vivo | 2026-11-06T13:52:34 | diagnostico: escolha corpo_nao_e_json; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 24, decisão `diagnostico`: escolha `corpo_nao_e_json`; resultado rotulo_emitido.
  - Evidência: evento 4 (verbete_entregue: `corpo_nao_e_json`, `mensagens-de-erro-do-codigo`, `corpo_vazio`); evento 8 (resposta); evento 13 (verbete_citado: `corpo_nao_e_json`).
  - Usou: `corpo_nao_e_json`, `mensagens-de-erro-do-codigo`, `corpo_vazio`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3 a 24 da trilha; hash dos eventos deste caso: `f63b07f1c84b3e79`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
