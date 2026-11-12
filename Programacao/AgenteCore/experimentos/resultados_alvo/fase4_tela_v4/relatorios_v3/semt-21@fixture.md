<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Campo ausente em `GET /api/produtos`, campo `nome`

Caso `semt-21` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/semt-21@fixture`: o caso `semt-21` na corrida `fase4_tela_v4`; eventos 1829 a 1850 da trilha `trilha_tela.jsonl`, hash dos eventos `b89d6b5af635bb48` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Campo ausente em `GET /api/produtos`, campo `nome`

## 3. Data, organização e autor

Observado em 06/11/2026 11:00:05 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `semt-21`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 3 (semântica: os tipos ou os domínios dos valores não fazem sentido); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 1, "nome": "", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]
```

4. Sintoma observado (texto do caso):

> O card mostra o texto literal '(sem nome)' no lugar do nome do produto; o campo nome e do tipo certo (texto), so que vazio.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids semt-21 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | O card mostra o texto literal '(sem nome)' no lugar do nome do produto; o campo nome e do tipo certo (texto), so que vazio. |

Corpo recebido, como veio no caso:

```text
[{"id": 1, "nome": "", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 3 (semântica: os tipos ou os domínios dos valores não fazem sentido); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 3 (semântica); nível 3 (difícil). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `tipo_divergente` (Tipo divergente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/tipo_divergente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/tipo_divergente.md`).
- Caso escrito: `semt-21` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/semt-21@fixture` em `trilha_tela.jsonl`, eventos 1829 a 1850, hash dos eventos `b89d6b5af635bb48`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/semt-21@fixture.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids semt-21 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `campo_ausente` (Campo ausente). Campo: `nome`. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,96 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê "(sem nome)" em vez do nome do produto.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu campo_ausente no campo nome porque os verbetes contrato-produto, entidade-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, campo_renomeado, ficou com probabilidade 0,28. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: O card mostra o texto literal '(sem nome)' no lugar do nome do produto; o campo nome e do tipo certo (texto), so que vazio.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> campo_ausente e não campo_renomeado: a escolha tem probabilidade 0,96 contra 0,28; verbete(s) na evidência: contrato-produto, entidade-produto, tipo_divergente

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `campo_ausente` (Campo ausente) | 0,96 | sim |
| `campo_renomeado` (Campo renomeado) | 0,28 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,03 |  |
| `corpo_vazio` (Corpo vazio) | 0,03 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `chave_de_juncao_errada` (Chave de junção errada) | 0,00 |  |
| `nulo_inesperado` (Nulo inesperado) | 0,00 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `contrato-produto` |
| A linha FONTE só tem identificadores, no formato pedido | `[contrato-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto"]} |
| O verbete citado fala da causa respondida | `contrato-produto` | não confere | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids semt-21 --k 3`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1829 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:00:05 | caso semt-21 |
| 1830 | 2 | candidatos | programa | ao_vivo | 2026-11-06T11:00:05 | 3 de 39 verbetes entregues |
| 1832 | 3 | prompt | programa | ao_vivo | 2026-11-06T11:00:05 | diagnostico: 3591 caracteres; verbetes contrato-produto, entidade-produto, tipo_divergente |
| 1834 | 4 | inferencia | programa | ao_vivo | 2026-11-06T11:00:05 | diagnostico: 51,5 s |
| 1835 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T11:00:05 | causa_raiz: `campo_ausente` |
| 1836 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T11:00:05 | campo: `nome` |
| 1837 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T11:00:05 | impacto: `O usuário vê "(sem nome)" em vez do nome do produto.` |
| 1838 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T11:00:05 | fonte: `[contrato-produto]` |
| 1839 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T11:00:05 | fonte_citada: `contrato-produto` |
| 1840 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:00:05 | quatro_linhas_presentes: confere |
| 1841 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:00:05 | rotulo_no_conjunto: confere |
| 1842 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:00:05 | fonte_existe_na_biblioteca: confere |
| 1843 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:00:05 | fonte_estava_no_contexto: confere |
| 1844 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T11:00:05 | campo_existe_no_caso: confere |
| 1845 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T11:00:05 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1846 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T11:00:05 | notas_nos_verbetes_citados: informativo |
| 1847 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:00:05 | impacto: nao_verificavel |
| 1848 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:00:05 | fonte_formato_valido: confere |
| 1849 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:00:05 | fonte_contem_termo_da_causa: nao_confere |
| 1850 | 20 | decisao | programa | ao_vivo | 2026-11-06T11:00:05 | diagnostico: escolha campo_ausente; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 1850, decisão `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido.
  - Evidência: evento 1830 (verbete_entregue: `contrato-produto`, `entidade-produto`, `tipo_divergente`); evento 1834 (resposta); evento 1839 (verbete_citado: `contrato-produto`).
  - Usou: `contrato-produto`, `entidade-produto`, `tipo_divergente`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1829 a 1850 da trilha; hash dos eventos deste caso: `b89d6b5af635bb48`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
