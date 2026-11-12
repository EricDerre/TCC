<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Campo renomeado em `GET /api/produtos/10`, campo `resumo`

Caso `sin-23` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/sin-23`: o caso `sin-23` na corrida `fase4_ineditos`; eventos 176 a 197 da trilha `trilha_ineditos.jsonl`, hash dos eventos `0354be1bfb1f8a66` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Campo renomeado em `GET /api/produtos/10`, campo `resumo`

## 3. Data, organização e autor

Observado em 06/11/2026 14:00:14 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos/10` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `sin-23`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 2 (sintática: a forma da resposta não é a esperada); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos/10`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
{"id": 10, "nome": "Refrigerante", "tipo": "Bebidas", "preco": 7.0, "imagem": "refrigerante.png", "destaque": false, "resumo_v2": "Lata 350ml, diversos sabores"}
```

4. Sintoma observado (texto do caso):

> O modal do Refrigerante abre com o titulo certo, mas o texto de descricao aparece como '(sem descrição)'.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids sin-23`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos/10` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | O modal do Refrigerante abre com o titulo certo, mas o texto de descricao aparece como '(sem descrição)'. |

Corpo recebido, como veio no caso:

```text
{"id": 10, "nome": "Refrigerante", "tipo": "Bebidas", "preco": 7.0, "imagem": "refrigerante.png", "destaque": false, "resumo_v2": "Lata 350ml, diversos sabores"}
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 2 (sintática: a forma da resposta não é a esperada); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 2 (sintática); nível 1 (fácil). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `campo_renomeado` (Campo renomeado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_renomeado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_renomeado.md`).
- Verbetes entregues pela busca e não citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Caso escrito: `sin-23` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/sin-23` em `trilha_ineditos.jsonl`, eventos 176 a 197, hash dos eventos `0354be1bfb1f8a66`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids sin-23`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `campo_renomeado` (Campo renomeado). Campo: `resumo`. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O campo resumo foi renomeado para resumo_v2, mas a interface espera resumo, resultando em uma descrição não exibida corretamente.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu campo_renomeado no campo resumo porque os verbetes contrato-produto, campo_renomeado, entidade-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos/10

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
{"id": 10, "nome": "Refrigerante", "tipo": "Bebidas", "preco": 7.0, "imagem": "refrigerante.png", "destaque": false, "resumo_v2": "Lata 350ml, diversos sabores"}

SINTOMA OBSERVADO: O modal do Refrigerante abre com o titulo certo, mas o texto de descricao aparece como '(sem descrição)'.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> campo_renomeado e não tipo_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: contrato-produto, campo_renomeado, entidade-produto

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `campo_renomeado` (Campo renomeado) | 1,00 | sim |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `chave_de_juncao_errada` (Chave de junção errada) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `dado_desatualizado` (Dado desatualizado (cache)) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[campo_renomeado]`; verbetes citados: `campo_renomeado` (Campo renomeado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_renomeado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_renomeado.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_renomeado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_renomeado` | confere | contexto: `contrato-produto`, `campo_renomeado`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `contrato-produto`, `campo_renomeado` |
| A linha FONTE só tem identificadores, no formato pedido | `[campo_renomeado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["campo_renomeado"]} |
| O verbete citado fala da causa respondida | `campo_renomeado` | confere | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `resumo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids sin-23`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 176 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:00:14 | caso sin-23 |
| 177 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:00:14 | 3 de 39 verbetes entregues |
| 179 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:00:14 | diagnostico: 3626 caracteres; verbetes contrato-produto, campo_renomeado, entidade-produto |
| 181 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:00:14 | diagnostico: 70,6 s |
| 182 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:00:14 | causa_raiz: `campo_renomeado` |
| 183 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:00:14 | campo: `resumo` |
| 184 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:00:14 | impacto: `O campo resumo foi renomeado para resumo_v2, mas a interface espera resumo, resultando em uma descrição não exibida corretamente.` |
| 185 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:00:14 | fonte: `[campo_renomeado]` |
| 186 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:00:14 | fonte_citada: `campo_renomeado` |
| 187 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:00:14 | quatro_linhas_presentes: confere |
| 188 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:00:14 | rotulo_no_conjunto: confere |
| 189 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:00:14 | fonte_existe_na_biblioteca: confere |
| 190 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:00:14 | fonte_estava_no_contexto: confere |
| 191 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:00:14 | campo_existe_no_caso: confere |
| 192 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:00:14 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 193 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:00:14 | notas_nos_verbetes_citados: informativo |
| 194 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:00:14 | impacto: nao_verificavel |
| 195 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:00:14 | fonte_formato_valido: confere |
| 196 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:00:14 | fonte_contem_termo_da_causa: confere |
| 197 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:00:14 | diagnostico: escolha campo_renomeado; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 197, decisão `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido.
  - Evidência: evento 177 (verbete_entregue: `contrato-produto`, `campo_renomeado`, `entidade-produto`); evento 181 (resposta); evento 186 (verbete_citado: `campo_renomeado`).
  - Usou: `contrato-produto`, `campo_renomeado`, `entidade-produto`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 176 a 197 da trilha; hash dos eventos deste caso: `0354be1bfb1f8a66`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
