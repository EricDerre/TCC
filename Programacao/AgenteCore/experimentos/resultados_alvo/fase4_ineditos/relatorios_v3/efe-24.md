<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Localizador (seletor) quebrado em `GET /api/produtos`

Caso `efe-24` da corrida `fase4_ineditos`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ineditos/qwen2.5_7b/efe-24`: o caso `efe-24` na corrida `fase4_ineditos`; eventos 787 a 808 da trilha `trilha_ineditos.jsonl`, hash dos eventos `4fe6aac6ea9e32c2` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Localizador (seletor) quebrado em `GET /api/produtos`

## 3. Data, organização e autor

Observado em 06/11/2026 14:30:30 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 13:52:23 a 06/11/2026 14:35:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `ineditos`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A requisição `GET /api/produtos` da CobaiaAPI, lida de um caso escrito (sem navegador neste diagnóstico: o agente recebeu em texto a requisição, o status, o contrato, o corpo e o sintoma).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Esta corrida rodou sem navegador. Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Caso escrito `efe-24`, de `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27); classe 6 (efeito: o que o usuário vê na tela está errado); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato). Sem roteiro nem falha injetada: o agente leu a requisição, o status, o contrato, o corpo e o sintoma em texto.

## 6. Descrição para reproduzir

O caso entrou em texto, como foi posto no prompt (sem roteiro na tela):

1. Requisição `GET /api/produtos`, status 200 (a API respondeu sem código de erro).
2. Contrato da interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.
3. Corpo da resposta:

```text
[{"id": 5, "nome": "Alcatra na Pedra", "resumo": "Alcatra grelhada servida na pedra quente", "tipo": "Carnes", "preco": 74.9, "imagem": "alcatra_pedra.jpg", "destaque": false}, {"id": 6, "nome": "Maminha", "resumo": "Corte macio grelhado na brasa", "tipo": "Carnes", "preco": 72.9, "imagem": "maminha.jpg", "destaque": false}]
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
      heading "Alcatra na Pedra" level=3
      text "Carnes"
      button "R$ 74,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="5"
    group
      heading "Maminha" level=3
      text "Carnes"
      button "R$ 72,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="6"
```

Seletor que falhou: `.thumbnail:has-text("Alcatra na Pedra") button >> nth=0`.
4. Sintoma observado (texto do caso):

> O passo 'abrir os detalhes da Alcatra na Pedra' clica no seletor sem erro, mas o modal nao abre: o passo seguinte, que espera #modalDetalhe visivel, esgota o tempo. Depois do clique nao aparece nenhuma requisicao GET /api/produtos/5 na rede.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids efe-24`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| corpo de `GET /api/produtos` | um JSON com os campos do contrato acima | o corpo abaixo |
| o que a interface mostrou | a página com os dados da resposta | O passo 'abrir os detalhes da Alcatra na Pedra' clica no seletor sem erro, mas o modal nao abre: o passo seguinte, que espera #modalDetalhe visivel, esgota o tempo. Depois do clique nao aparece nenhuma requisicao GET /api/produtos/5 na rede. |

Corpo recebido, como veio no caso:

```text
[{"id": 5, "nome": "Alcatra na Pedra", "resumo": "Alcatra grelhada servida na pedra quente", "tipo": "Carnes", "preco": 74.9, "imagem": "alcatra_pedra.jpg", "destaque": false}, {"id": 6, "nome": "Maminha", "resumo": "Corte macio grelhado na brasa", "tipo": "Carnes", "preco": 72.9, "imagem": "maminha.jpg", "destaque": false}]
```

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 6 (efeito: o que o usuário vê na tela está errado); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 6 (efeito); nível 2 (médio). Confiança do agente: o agente está seguro desta causa.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `localizador_quebrado` (Localizador (seletor) quebrado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/localizador_quebrado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/localizador_quebrado.md`).
- Verbetes entregues pela busca e não citados: `contrato-produto` (Contrato de /api/produtos; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/contratos/contrato-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/contratos/contrato-produto.md`); `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`).
- Caso escrito: `efe-24` em `banco_casos_ineditos_fase4.py` (os 36 inéditos da ficha 27).
- Trilha: `fase4_ineditos/qwen2.5_7b/efe-24` em `trilha_ineditos.jsonl`, eventos 787 a 808, hash dos eventos `4fe6aac6ea9e32c2`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids efe-24`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `localizador_quebrado` (Localizador (seletor) quebrado). Campo: nenhum apontado. Confiança: o agente está seguro desta causa (probabilidade 1,00 no rótulo; selo `alto` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário não consegue abrir os detalhes do produto Alcatra na Pedra, pois o modal não aparece após o clique.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu localizador_quebrado porque os verbetes localizador_quebrado, contrato-produto, entidade-produto estavam entre os entregues ao modelo. A segunda causa, estrutura_aninhada_divergente, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 5, "nome": "Alcatra na Pedra", "resumo": "Alcatra grelhada servida na pedra quente", "tipo": "Carnes", "preco": 74.9, "imagem": "alcatra_pedra.jpg", "destaque": false}, {"id": 6, "nome": "Maminha", "resumo": "Corte macio grelhado na brasa", "tipo": "Carnes", "preco": 72.9, "imagem": "maminha.jpg", "destaque": false}]

ÁRVORE DE ACESSIBILIDADE DA PÁGINA:
document "Churrascaria Fornalha - Produtos (API)"
  navigation
    link "PRODUTOS"
    link "PRODUTOS (API)"
  main
    heading "Produtos via API" level=2
    group
      heading "Alcatra na Pedra" level=3
      text "Carnes"
      button "R$ 74,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="5"
    group
      heading "Maminha" level=3
      text "Carnes"
      button "R$ 72,90"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="6"


SELETOR QUE FALHOU: .thumbnail:has-text("Alcatra na Pedra") button >> nth=0

SINTOMA OBSERVADO: O passo 'abrir os detalhes da Alcatra na Pedra' clica no seletor sem erro, mas o modal nao abre: o passo seguinte, que espera #modalDetalhe visivel, esgota o tempo. Depois do clique nao aparece nenhuma requisicao GET /api/produtos/5 na rede.
```

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> localizador_quebrado e não estrutura_aninhada_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: localizador_quebrado, contrato-produto, entidade-produto

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `localizador_quebrado` (Localizador (seletor) quebrado) | 1,00 | sim |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `resposta_truncada` (Resposta truncada) | 0,00 |  |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `nulo_inesperado` (Nulo inesperado) | 0,00 |  |
| `corpo_nao_e_json` (Corpo não é JSON) | 0,00 |  |
| `corpo_vazio` (Corpo vazio) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `estado_da_tela_divergente` (Estado da tela divergente da resposta) | 0,00 |  |
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `tempo_de_resposta_excedido` (Tempo de resposta excedido) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[localizador_quebrado]`; verbetes citados: `localizador_quebrado` (Localizador (seletor) quebrado; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/localizador_quebrado.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/localizador_quebrado.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `localizador_quebrado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `localizador_quebrado` | confere | contexto: `localizador_quebrado`, `contrato-produto`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `localizador_quebrado` | confere | verbetes: `localizador_quebrado` |
| A linha FONTE só tem identificadores, no formato pedido | `[localizador_quebrado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["localizador_quebrado"]} |
| O verbete citado fala da causa respondida | `localizador_quebrado` | confere | {"termo": "localizador_quebrado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo ineditos --saida fase4_ineditos_reexec --ids efe-24`

## 17. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 787 | 1 | entrada | programa | ao_vivo | 2026-11-06T14:30:30 | caso efe-24 |
| 788 | 2 | candidatos | programa | ao_vivo | 2026-11-06T14:30:30 | 3 de 39 verbetes entregues |
| 790 | 3 | prompt | programa | ao_vivo | 2026-11-06T14:30:30 | diagnostico: 4604 caracteres; verbetes localizador_quebrado, contrato-produto, entidade-produto |
| 792 | 4 | inferencia | programa | ao_vivo | 2026-11-06T14:30:30 | diagnostico: 92,2 s |
| 793 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T14:30:30 | causa_raiz: `localizador_quebrado` |
| 794 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T14:30:30 | campo: `nenhum` |
| 795 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T14:30:30 | impacto: `O usuário não consegue abrir os detalhes do produto Alcatra na Pedra, pois o modal não aparece após o clique.` |
| 796 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T14:30:30 | fonte: `[localizador_quebrado]` |
| 797 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T14:30:30 | fonte_citada: `localizador_quebrado` |
| 798 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T14:30:30 | quatro_linhas_presentes: confere |
| 799 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T14:30:30 | rotulo_no_conjunto: confere |
| 800 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T14:30:30 | fonte_existe_na_biblioteca: confere |
| 801 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T14:30:30 | fonte_estava_no_contexto: confere |
| 802 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T14:30:30 | campo_existe_no_caso: nao_se_aplica |
| 803 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T14:30:30 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 804 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T14:30:30 | notas_nos_verbetes_citados: informativo |
| 805 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T14:30:30 | impacto: nao_verificavel |
| 806 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T14:30:30 | fonte_formato_valido: confere |
| 807 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T14:30:30 | fonte_contem_termo_da_causa: confere |
| 808 | 20 | decisao | programa | ao_vivo | 2026-11-06T14:30:30 | diagnostico: escolha localizador_quebrado; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 808, decisão `diagnostico`: escolha `localizador_quebrado`; resultado rotulo_emitido.
  - Evidência: evento 788 (verbete_entregue: `localizador_quebrado`, `contrato-produto`, `entidade-produto`); evento 792 (resposta); evento 797 (verbete_citado: `localizador_quebrado`).
  - Usou: `localizador_quebrado`, `contrato-produto`, `entidade-produto`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 787 a 808 da trilha; hash dos eventos deste caso: `4fe6aac6ea9e32c2`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
