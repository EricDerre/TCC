<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Campo ausente em `GET /api/produtos`, campo `nome`

Caso `sin-22` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/sin-22`: o caso `sin-22` na corrida `fase4_ineditos`; eventos 153 a 174 da trilha `trilha_ineditos.jsonl`, hash dos eventos `d1ef7256b1088f02` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Campo ausente em `GET /api/produtos`, campo `nome`

## 3. Data, organização e autor

Observado em 06/11/2026 13:59:19 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `sin-22`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 2 (sintática: a forma da resposta não é a esperada); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 5, "resumo": "Alcatra grelhada servida na pedra quente", "tipo": "Carnes", "preco": 74.9, "imagem": "alcatra_pedra.jpg", "destaque": false}, {"id": 6, "resumo": "Corte macio grelhado na brasa", "tipo": "Carnes", "preco": 72.9, "imagem": "maminha.jpg", "destaque": false}]
```

4. Sintoma observado (texto do caso):

> Todos os cartoes da grade aparecem com o titulo '(sem nome)'. As fotos, as descricoes, os precos e os botoes 'Saiba Mais...' continuam normais.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids sin-22`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | Todos os cartoes da grade aparecem com o titulo '(sem nome)'. As fotos, as descricoes, os precos e os botoes 'Saiba Mais...' continuam normais. |

Corpo recebido, como veio no caso:

```text
[{"id": 5, "resumo": "Alcatra grelhada servida na pedra quente", "tipo": "Carnes", "preco": 74.9, "imagem": "alcatra_pedra.jpg", "destaque": false}, {"id": 6, "resumo": "Corte macio grelhado na brasa", "tipo": "Carnes", "preco": 72.9, "imagem": "maminha.jpg", "destaque": false}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 2 (sintática: a forma da resposta não é a esperada); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 2 (sintática); nível 1 (fácil). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Caso escrito: `sin-22` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/sin-22` em `trilha_ineditos.jsonl`, eventos 153 a 174, hash dos eventos `d1ef7256b1088f02`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids sin-22`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `campo_ausente` (Campo ausente). Campo: `nome`. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,94 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O título dos cartões na interface web aparece como '(sem nome)', pois o campo "nome" está ausente na resposta da API.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu campo_ausente no campo nome porque os verbetes entidade-produto, contrato-produto, campo_ausente estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,05. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 5, "resumo": "Alcatra grelhada servida na pedra quente", "tipo": "Carnes", "preco": 74.9, "imagem": "alcatra_pedra.jpg", "destaque": false}, {"id": 6, "resumo": "Corte macio grelhado na brasa", "tipo": "Carnes", "preco": 72.9, "imagem": "maminha.jpg", "destaque": false}]

SINTOMA OBSERVADO: Todos os cartoes da grade aparecem com o titulo '(sem nome)'. As fotos, as descricoes, os precos e os botoes 'Saiba Mais...' continuam normais.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> campo_ausente e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 0,94 contra 0,05; verbete(s) na evidência: entidade-produto, contrato-produto, campo_ausente

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `campo_ausente` (Campo ausente) | 0,94 | sim |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,05 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente]`; verbetes citados: `campo_ausente` (Campo ausente; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/campo_ausente.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/campo_ausente.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `contrato-produto`, `campo_ausente` |
| A linha FONTE só tem identificadores, no formato pedido | `[campo_ausente]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["campo_ausente"]} |
| O verbete citado fala da causa respondida | `campo_ausente` | confere | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids sin-22`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 153 | 1 | entrada | programa | ao_vivo | 2026-11-06T13:59:19 | caso sin-22 |
| 154 | 2 | candidatos | programa | ao_vivo | 2026-11-06T13:59:19 | 3 de 39 verbetes entregues |
| 156 | 3 | prompt | programa | ao_vivo | 2026-11-06T13:59:19 | diagnostico: 3621 caracteres; verbetes entidade-produto, contrato-produto, campo_ausente |
| 158 | 4 | inferencia | programa | ao_vivo | 2026-11-06T13:59:19 | diagnostico: 51,2 s |
| 159 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T13:59:19 | causa_raiz: `campo_ausente` |
| 160 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T13:59:19 | campo: `nome` |
| 161 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T13:59:19 | impacto: `O título dos cartões na interface web aparece como '(sem nome)', pois o campo "nome" está ausente na resposta da API.` |
| 162 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T13:59:19 | fonte: `[campo_ausente]` |
| 163 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T13:59:19 | fonte_citada: `campo_ausente` |
| 164 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T13:59:19 | quatro_linhas_presentes: confere |
| 165 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T13:59:19 | rotulo_no_conjunto: confere |
| 166 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T13:59:19 | fonte_existe_na_biblioteca: confere |
| 167 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T13:59:19 | fonte_estava_no_contexto: confere |
| 168 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T13:59:19 | campo_existe_no_caso: confere |
| 169 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T13:59:19 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 170 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T13:59:19 | notas_nos_verbetes_citados: informativo |
| 171 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T13:59:19 | impacto: nao_verificavel |
| 172 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T13:59:19 | fonte_formato_valido: confere |
| 173 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T13:59:19 | fonte_contem_termo_da_causa: confere |
| 174 | 20 | decisao | programa | ao_vivo | 2026-11-06T13:59:19 | diagnostico: escolha campo_ausente; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 174, decisão `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido.
  - Evidência: evento 154 (verbete_entregue: `entidade-produto`, `contrato-produto`, `campo_ausente`); evento 158 (resposta); evento 163 (verbete_citado: `campo_ausente`).
  - Usou: `entidade-produto`, `contrato-produto`, `campo_ausente`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 153 a 174 da trilha; hash dos eventos deste caso: `d1ef7256b1088f02`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
