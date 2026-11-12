<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Localizador (seletor) quebrado em `GET /api/produtos`

Caso `efe-23` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/efe-23`: o caso `efe-23` na corrida `fase4_ineditos`; eventos 764 a 785 da trilha `trilha_ineditos.jsonl`, hash dos eventos `0268d0d86d5b47fa` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Localizador (seletor) quebrado em `GET /api/produtos`

## 3. Data, organização e autor

Observado em 06/11/2026 14:29:13 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `efe-23`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 6 (efeito: o que o usuário vê na tela está errado); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 6, "nome": "Maminha", "resumo": "Corte macio grelhado na brasa", "tipo": "Carnes", "preco": 72.9, "imagem": "maminha.jpg", "destaque": false}, {"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Carnes", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}]
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
      heading "Maminha" level=3
      text "Carnes"
      button "R$ 72,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="6"
    group
      heading "Cupim" level=3
      text "Carnes"
      button "R$ 76,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="7"
```

Seletor que falhou: `h2:has-text("Cupim")`.
4. Sintoma observado (texto do caso):

> A verificacao 'o titulo do Cupim esta visivel' do roteiro falha: o seletor h2:has-text("Cupim") nao encontra nenhum elemento. O cartao do Cupim aparece normalmente na tela e GET /api/produtos respondeu 200.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids efe-23`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | A verificacao 'o titulo do Cupim esta visivel' do roteiro falha: o seletor h2:has-text("Cupim") nao encontra nenhum elemento. O cartao do Cupim aparece normalmente na tela e GET /api/produtos respondeu 200. |

Corpo recebido, como veio no caso:

```text
[{"id": 6, "nome": "Maminha", "resumo": "Corte macio grelhado na brasa", "tipo": "Carnes", "preco": 72.9, "imagem": "maminha.jpg", "destaque": false}, {"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Carnes", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 6 (efeito: o que o usuário vê na tela está errado); nível 1 (fácil: o sinal é local e explícito, como status de erro, corpo que não é JSON ou campo que sumiu).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 6 (efeito); nível 1 (fácil). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `localizador_quebrado` (Localizador (seletor) quebrado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/localizador_quebrado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/localizador_quebrado.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`).
- Caso escrito: `efe-23` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/efe-23` em `trilha_ineditos.jsonl`, eventos 764 a 785, hash dos eventos `0268d0d86d5b47fa`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids efe-23`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `localizador_quebrado` (Localizador (seletor) quebrado). Campo: nenhum apontado. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O seletor utilizado para verificar a visibilidade do título do Cupim falhou, não encontrando nenhum elemento correspondente.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu localizador_quebrado porque os verbetes entidade-produto, contrato-produto, localizador_quebrado estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 6, "nome": "Maminha", "resumo": "Corte macio grelhado na brasa", "tipo": "Carnes", "preco": 72.9, "imagem": "maminha.jpg", "destaque": false}, {"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Carnes", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}]

ÁRVORE DE ACESSIBILIDADE DA PÁGINA:
document "Churrascaria Fornalha - Produtos (API)"
  navigation
    link "PRODUTOS"
    link "PRODUTOS (API)"
  main
    heading "Produtos via API" level=2
    group
      heading "Maminha" level=3
      text "Carnes"
      button "R$ 72,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="6"
    group
      heading "Cupim" level=3
      text "Carnes"
      button "R$ 76,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="7"


SELETOR QUE FALHOU: h2:has-text("Cupim")

SINTOMA OBSERVADO: A verificacao 'o titulo do Cupim esta visivel' do roteiro falha: o seletor h2:has-text("Cupim") nao encontra nenhum elemento. O cartao do Cupim aparece normalmente na tela e GET /api/produtos respondeu 200.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> localizador_quebrado e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, localizador_quebrado

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `localizador_quebrado` (Localizador (seletor) quebrado) | 1,00 | sim |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `chave_de_juncao_errada` (Chave de junção errada) | 0,00 |  |
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado` (Localizador (seletor) quebrado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/localizador_quebrado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/localizador_quebrado.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `entidade-produto`, `contrato-produto`, `localizador_quebrado` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado` |
| A linha FONTE só tem identificadores, no formato pedido | `[localizador_quebrado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["localizador_quebrado"]} |
| O verbete citado fala da causa respondida | `localizador_quebrado` | confere | {"termo": "localizador_quebrado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids efe-23`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 764 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:29:13 | caso efe-23 |
| 765 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:29:13 | 3 de 39 verbetes entregues |
| 767 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:29:13 | diagnostico: 4497 caracteres; verbetes entidade-produto, contrato-produto, localizador_quebrado |
| 769 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:29:13 | diagnostico: 72,8 s |
| 770 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:29:13 | causa_raiz: `localizador_quebrado` |
| 771 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:29:13 | campo: `nenhum` |
| 772 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:29:13 | impacto: `O seletor utilizado para verificar a visibilidade do título do Cupim falhou, não encontrando nenhum elemento correspondente.` |
| 773 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:29:13 | fonte: `[localizador_quebrado]` |
| 774 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:29:13 | fonte_citada: `localizador_quebrado` |
| 775 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:29:13 | quatro_linhas_presentes: confere |
| 776 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:29:13 | rotulo_no_conjunto: confere |
| 777 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:29:13 | fonte_existe_na_biblioteca: confere |
| 778 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:29:13 | fonte_estava_no_contexto: confere |
| 779 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:29:13 | campo_existe_no_caso: nao_se_aplica |
| 780 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:29:13 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 781 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:29:13 | notas_nos_verbetes_citados: informativo |
| 782 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:29:13 | impacto: nao_verificavel |
| 783 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:29:13 | fonte_formato_valido: confere |
| 784 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:29:13 | fonte_contem_termo_da_causa: confere |
| 785 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:29:13 | diagnostico: escolha localizador_quebrado; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 785, decisão `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido.
  - Evidência: evento 765 (verbete_entregue: `entidade-produto`, `contrato-produto`, `localizador_quebrado`); evento 769 (resposta); evento 774 (verbete_citado: `localizador_quebrado`).
  - Usou: `entidade-produto`, `contrato-produto`, `localizador_quebrado`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 764 a 785 da trilha; hash dos eventos deste caso: `0268d0d86d5b47fa`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
