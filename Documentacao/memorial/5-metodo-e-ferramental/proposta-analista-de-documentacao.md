<!-- ! Alteração de IA - Revisar: arquivo gerado por ferramentas/integrar_pesquisa_fluxo_do_agente.py a partir de 5-metodo-e-ferramental/dados/pesquisa-fluxo-do-agente/proposta-analista-de-documentacao.modelo.txt, com os números trocados pelos de medidas_do_repositorio.json. NÃO editar à mão: mude o modelo e rode o integrador (o --check compara com o regerado).
     ! Motivo: a proposta cita custos e contagens das corridas, e a regra é nenhum número digitado à mão; gerada do modelo, ela muda sozinha se uma medida mudar. -->
<!-- ! Alteração de IA - Revisar: documento novo (10/11/2026), escrito pelo Claude na sessão de pesquisa da ficha 64: a proposta de desenho para a terceira ideia do Eric, a separação entre o módulo de análise, que diagnostica e não mexe na biblioteca, e um analista de documentação, que recebe o caso já decidido por uma pessoa e só então propõe mudanças nos verbetes. Diz o que existe hoje, o que a pesquisa sustenta, o que o analista recebe, quando é chamado, o que pode propor, os filtros e os portões que valem e os que faltam, quanto custa nesta máquina, o que teria de ser medido e o que conflita com as decisões 69, 103 e 105.
     ! Motivo: o Eric disse que a ideia "requer análises profundas e pesquisas para embasar"; sem o desenho escrito, a decisão sobre implementar ficaria sem saber o custo, as medidas e os conflitos. É proposta: nada foi implementado, e nada muda no agente sem decisão dele (ficha 67). Os números vêm de `dados/pesquisa-fluxo-do-agente/medidas_do_repositorio.json`, nenhum digitado à mão. -->
<!-- ! Alteração de IA - Revisar: (10/11/2026, depois da revisão da entrega) a seção 4.2 passou a dizer o que é o gatilho da FONTE divergente e a citar, pela falha gravada na trilha, quantos casos da corrida 24 são do tipo "nenhum verbete entregue trata da causa respondida" e quantos dos diagnósticos certos que o analista de QA recusou estavam entre eles; a seção 4.4 cita quantos verbetes novos nenhum caso com gabarito leria; a seção 3 diz o que a literatura mede sobre o rótulo e sobre o curador sem treino; a seção 7 parafraseia as decisões 103 e 105 pelo texto da tabela de decisões; e o selo de confiança e o hub ganharam a explicação na primeira menção.
     ! Motivo: um revisor conferiu a proposta contra o arquivo de medidas, o código e as decisões. A frase sobre os diagnósticos certos recusados atribuía todos a uma conferência sem número medido, e o gatilho junta duas conferências (`diagnostico_ao_vivo.REGRAS_DA_FONTE_DIVERGENTE`); "nenhum caso leria" valia para quase todos os verbetes novos, não para todos; e as paráfrases das decisões 103 e 105 traziam palavras que não estão nelas. As contas que faltavam passaram a existir em `ferramentas/medidas_fluxo_do_agente.py`. -->

# Proposta de desenho: o analista de documentação (o segundo momento do modelo)

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). **Estado: proposta, não aprovada.** Nada aqui foi implementado, e o agente continua como está nas corridas 18d e 21d. A decisão é a ficha 67 das [pendências](../pendencias.md). A pesquisa que embasa cada ponto está no [levantamento do fluxo do agente](../2-pesquisa-e-literatura/levantamento-2026-11-10-fluxo-do-agente.md) (§6.16), e os números vêm das corridas já gravadas, pelo arquivo de medidas da mesma rodada.

## 1. De onde vem

Em 10/11/2026, lendo o parecer do analista de QA, o Eric propôs separar dois momentos em que o modelo é chamado (ficha 64). No primeiro, o módulo de análise faz o que o agente faz hoje (roteiro, detecção, poda, busca, diagnóstico e selo de confiança, que é a etiqueta baixo, médio ou alto que o agente dá a cada diagnóstico pela probabilidade da causa respondida) e não propõe mudança nenhuma na biblioteca. No segundo, um analista de documentação recebe o relatório pronto, com contexto próprio, e só ele propõe criar, corrigir ou limpar verbetes, guiado por filtros em código, como num time com desenvolvimento, teste e documentação.

A ideia mira o ponto mais fraco que os dados mostram: o que o modelo escreve na biblioteca. Na corrida 20, das 20 edições que passaram nos filtros em código, uma pessoa julgou 2 corretas, 9 parciais e 9 erradas; a biblioteca que o modelo lê tem 26 notas dele em 20 dos 39 verbetes, 25 delas escritas como instrução.

## 2. O que existe hoje

A proposta de edição já é uma chamada separada do diagnóstico. O que ela é, passo a passo:

| Ponto | Como é hoje | Onde está |
|---|---|---|
| Quem propõe | o mesmo fluxo do diagnóstico, numa segunda inferência cujo prompt é a continuação literal do prompt do diagnóstico | `estrategias.proposta_de_edicao`, `biblioteca_fase4.propor_p5` |
| O que o modelo recebe | o prompt do diagnóstico, a resposta que ele deu, a causa certa e o campo afetado (o gabarito do caso) e o verbete dedicado a essa causa | bloco "CORREÇÃO DESTE CASO" de `estrategias._FORMATO_PROPOSTA` |
| Quando | em todo caso de aprendizado, tenha o diagnóstico acertado ou errado (54 casos na corrida 20) | `executar_fase4.py`, modo `biblioteca` |
| O que pode propor | até 2 propostas por caso: nota, retificação (acrescenta a correção de um trecho) ou verbete novo; ou a palavra NENHUMA | `_FORMATO_PROPOSTA` |
| Filtros em código | o validador da Fase 3 (30 códigos de recusa), os 13 filtros da Fase 4 e a regra dos 40% (nota em verbete muito recuperado vai para revisão humana) | `evolucao_biblioteca.validar_proposta`, `biblioteca_fase4.filtrar_proposta` |
| Portão | o lote só entra depois da reavaliação nos 36 inéditos (regra R5: os casos que passam a acertar não podem ser menos que os que passam a errar) e da revisão humana, que tira a edição julgada errada | `biblioteca_fase4.promover` |
| Onde grava | numa cópia da biblioteca, na pasta da corrida; a promoção leva o lote à biblioteca de produção | `bibliotecas/<modelo>/epoca-N`, `biblioteca_producao/` |
| Custo | 2.358 tokens lidos e 361 escritos, 158 s por caso na mediana | corrida 20 |

O que a corrida 20 mostrou desse desenho:

- De 92 propostas, os filtros aceitaram 19 e seguraram 1. O modelo se absteve em 0 dos 54 casos: ele sempre propõe alguma coisa.
- 76 das 92 propostas começam por verbo de instrução ("Adicionar nota sobre...", "Corrigir a junção..."), e 18 das 20 que passaram nos filtros também. Nenhum filtro de hoje olha a forma.
- A regra do lote aceitou o lote com 0 casos ganhos e 0 perdidos nos 36 inéditos. Ela mede o lote inteiro e não enxerga a edição ruim que não muda nenhum rótulo.
- Dos verbetes novos propostos, a revisão julgou 0 corretos, 3 parciais e 3 errados.
- O gabarito que a proposta recebe só existe nos casos de aprendizado. Em uso, ninguém diz ao agente qual era a causa certa.

## 3. O que a pesquisa sustenta e o que não sustenta

Sustenta (levantamento §6.16.6 e §6.16.7):

- **Escrever na base depois da tarefa, em segundo plano e em lote.** É o desenho dos sistemas que medem ganho, e consolidar a cada interação perde para consolidar em lote.
- **O rótulo de certo ou errado pesa.** Sem o rótulo verdadeiro, um dos sistemas medidos cai, num caso abaixo de não ter memória; em outro, que usa um juiz automático, o melhor resultado é o do juiz que acerta sempre.
- **A fusão na base em código**, por edições pequenas, e nunca por texto reescrito pelo modelo: reescrever a base inteira já a fez encolher de 18.282 para 122 tokens num passo.
- **Guardar o material bruto como evidência primária**: o relatório, a trilha e a decisão da pessoa ficam, e a base é derivada deles.
- **Portões que medem antes de aceitar**: o que passava tem de continuar passando, e a aprovação é de uma pessoa.
- **Limpar por utilidade medida**: registros nunca usados ou que atrapalham saem, e os que ficam são mais corretos.

Não sustenta:

- **Que o mesmo modelo escreva melhor só por ser chamado em separado.** Nenhuma fonte compara, com o mesmo modelo, escrever no passo da tarefa contra escrever num papel separado.
- **Que um modelo de 7B sem treino seja bom redator.** Os curadores pequenos que mais rendem na literatura são treinados, por reforço ou por ajuste supervisionado; sem treino, um curador de 8B ainda fica acima de não ter memória, mas abaixo do treinado (levantamento §6.16.6). O projeto não treina modelo.

Por isso o valor do desenho abaixo está na seleção em código, no rótulo dado por uma pessoa e nos portões por edição, e não em trocar a ordem das chamadas.

## 4. O desenho proposto

### 4.1 Os dois momentos

```text
Momento 1: análise (como hoje; não propõe nada para a biblioteca)
  roteiro -> detecção -> poda -> busca -> diagnóstico -> selo -> relatório e árvore de decisão
                                                                        |
                                    uma pessoa decide sobre o relatório (aceita, recusa, informa a causa certa)
                                                                        |
Momento 2: documentação (em segundo plano, em lote; não entra no tempo até o resultado)
  seleção em código -> ficha do caso -> analista de documentação (modelo) -> filtros em código
      -> portão da busca -> portão do diagnóstico -> espera ou lote -> aprovação de uma pessoa -> promoção
```

O módulo de análise perde a proposta de edição e fica só com o diagnóstico. O analista de documentação é o mesmo modelo (`qwen2.5:7b`), com um prompt próprio, que não continua o do diagnóstico.

### 4.2 Quando o analista de documentação é chamado

Quem decide é o código, nunca o modelo. As três condições têm de valer:

1. **O relatório do caso tem a decisão de uma pessoa.** É ela que faz o papel do gabarito (a causa certa conhecida do caso). Vem do hub, a tela em que uma pessoa revisa os relatórios, prevista para depois da Fase 5 (pacote Q6 do plano da Pós-Fase 4); enquanto o hub não existe, só os casos de aprendizado, que têm gabarito, servem para medir.
2. **Há lacuna na documentação.** Ou a pessoa recusou o diagnóstico e informou a causa certa; ou aceitou, mas a conferência em código "nenhum verbete entregue trata da causa respondida" não conferiu, isto é, o modelo acertou sem a documentação dar apoio.
3. **O verbete da causa certa ainda não registra esse caso** (a auditoria por etapa, que já existe).

Diagnóstico certo e sem lacuna não chama ninguém: gravar tudo degrada a base, e o modelo não se abstém sozinho.

O agente já calcula o sinal da segunda condição. É o gatilho da FONTE divergente, que acende em dois casos: a linha FONTE da resposta cita um verbete que não estava entre os três entregues, ou nenhum dos três trata da causa respondida. Só o segundo caso é a lacuna desta seção, e a trilha grava qual dos dois ocorreu (a falha `causa_sem_verbete_que_a_trate`). Na corrida 24 o gatilho acendeu em 10 dos 36 casos, 10 deles com a falha `causa_sem_verbete_que_a_trate`: 6 acertos e 4 erros.

Pelos casos dessa corrida, as chamadas seriam, no máximo, para os 11 erros (os que a pessoa recusar informando a causa) e para esses 6 acertos. Na sessão de revisão com o analista de QA, ele recusou 10 dos 11 diagnósticos errados. Dos 5 diagnósticos certos que recusou, 5 estavam entre esses acertos: a causa estava certa e nenhum verbete entregue tratava dela. Desses 6 acertos, ele recusou 5.

As chamadas rodam em lote, quando a máquina está livre, sobre os relatórios decididos desde o lote anterior.

### 4.3 O que ele recebe

Uma **ficha do caso**, gerada por código a partir da trilha e da decisão da pessoa, com orçamento de 400 tokens:

- a requisição e o sintoma, como o diagnóstico os leu;
- a diferença medida do corpo contra o contrato e contra a referência;
- os três verbetes entregues (só o identificador e o título) e a posição em que a busca deixou o verbete da causa certa;
- a resposta do agente (causa e campo), o selo e as conferências que não conferiram;
- a decisão da pessoa: aceito ou recusado, a causa certa e o comentário, rotulado como texto de pessoa.

Junto vão o verbete da causa certa, que é onde a edição entra, e o bloco de instruções com o formato da resposta.

Ficam de fora, de propósito: o relatório inteiro e a árvore inteira (são para pessoas e custam minutos de leitura, tabela abaixo); a frase de impacto e a linha FONTE como o modelo as escreveu (num dos trabalhos lidos, juntar as reflexões do próprio agente à entrada de quem extrai as lições derrubou o resultado); qualquer trecho literal do corpo HTTP (regra da especificação da trilha, seção 10); e o prompt do diagnóstico.

| O que o analista de documentação leria | Tokens lidos | Tokens escritos | Tempo por chamada |
|---|---|---|---|
| Como a proposta de hoje (continua o prompt do diagnóstico, até 2 propostas) | 2.358 | 361 | 158 s (2,6 min), medido |
| Relatório v3 inteiro, um verbete e as instruções, uma proposta | 5.921 | 204 | 275 s (4,6 min), estimado |
| Árvore de decisão, um verbete e as instruções, uma proposta | 3.299 | 204 | 174 s (2,9 min), estimado |
| Ficha curta do caso, um verbete e as instruções, uma proposta | 1.238 | 204 | 95 s (1,6 min), estimado |

A ficha curta custa cerca de 1,6 minuto por chamada; o relatório inteiro, 4,6. A entrada da ficha soma os 400 tokens do caso, 160 de um verbete e 678 das instruções de hoje, que podem encolher quando o formato tiver menos campos.

### 4.4 O que ele pode propor

Uma proposta por caso (hoje são até 2), de um destes tipos:

| Tipo | O que é | Por quê |
|---|---|---|
| `sinal_de_busca` | palavras-chave ou sintomas novos para um verbete que já existe, para a busca entregá-lo em casos como este | ataca o erro mais comum (9 dos 11 erros da corrida 24 não tinham o verbete certo entre os três) e é o único tipo cujo efeito se confere inteiro em código |
| `nota` | uma frase que afirma um fato sobre o sistema, no verbete da causa certa | é o que já existe; muda a exigência: afirmação, nunca instrução |
| `retificacao` | aponta um trecho errado de um verbete e a frase certa; o trecho antigo fica, marcado | já existe; continua sendo acréscimo |
| `nenhuma` | não há o que acrescentar | saída válida e contada |

Fica fora o verbete novo escrito pelo modelo: dos 6 verbetes novos do lote da corrida 20, a revisão julgou 0 corretos, e 5 deles nenhum caso com gabarito leria. Quando faltar verbete para uma causa, o analista sinaliza a falta e uma pessoa escreve.

Limpar não é operação do modelo (seção 4.6).

### 4.5 Os portões, na ordem

| Portão | O que confere | Existe hoje |
|---|---|---|
| 0. Seleção | as três condições da seção 4.2 | não; a auditoria por etapa existe |
| 1. Validador da Fase 3 | forma, tamanho, identificadores, duplicata, trecho citado (30 códigos) | sim |
| 2. Filtros da Fase 4 | evidência do caso, uma alegação só, fonte conferida contra o código das cobaias, redundância, proveniência, texto de origem proibida, regra dos 40% | sim |
| 3. Forma de instrução | recusa o texto que começa por verbo de instrução | não |
| 4. Filtros de texto | as oito medidas de prolixidade e objetividade do pacote Q2, com os limiares do corpus | os filtros existem; o uso nas propostas, não |
| 5. Portão da busca | com a edição aplicada numa cópia, refaz a busca de todos os casos com gabarito: recusa se o verbete da causa certa sai dos três entregues de algum caso; no `sinal_de_busca`, exige que o caso de origem passe a recebê-lo | não |
| 6. Portão do diagnóstico | refaz o diagnóstico só dos casos que leriam a edição, até um teto por edição: recusa se algum caso certo passa a errar; marca "com efeito" se o caso de origem passa a acertar | não; a regra R5 faz isso para o lote inteiro |
| 7. Espera | a edição que passou e não teve efeito medido fica fora do que o modelo lê, em `aprendidos_em_espera/`, até outro caso a motivar | a pasta existe; o estado para notas, não |
| 8. Aprovação de uma pessoa | à imagem de uma pull request: a pessoa vê a diferença no verbete, a ficha do caso e o resultado dos portões; aprova, pede mudança ou recusa; a IA só comenta | hoje é a planilha de revisão do lote; o hub é o pacote Q6 |
| 9. Promoção | o lote aprovado entra na biblioteca de produção, com a regra R5 nos inéditos e o registro em `fechamento.json`; a leitura de cada verbete que mudou fica marcada para nova curadoria | sim, salvo a marca na camada de leitura |

Dois portões novos já podem ser vistos nos dados da corrida 20, sem modelo.

**Forma de instrução (portão 3).** Recusaria 18 das 20 edições que passaram. O filtro sozinho esvaziaria o lote: o prompt do analista tem de pedir a frase como ela vai ficar no verbete, e o filtro mede se o modelo obedeceu.

**Portão da busca (portão 5).** Aplicado a cada uma das 20 edições, sobre a biblioteca de antes do lote e os 126 casos com gabarito: 16 mudam os três verbetes de algum caso, o verbete da causa certa sai dos três 7 vezes e entra 4. Como ler: uma edição boa não tira o verbete certo de nenhum caso; a última coluna diz quantos diagnósticos o portão 6 teria de refazer.

| Caso de origem | Verbete | Operação | Casos em que os três verbetes mudam | Verbete certo entra | Verbete certo sai | Casos que leriam a edição |
|---|---|---|---|---|---|---|
| sin-1 | `campo_preco_ausente` | verbete novo | 6 | 0 | 1 | 1 |
| tra-3 | `novo_verbete` | verbete novo | 4 | 0 | 0 | 0 |
| tra-5 | `pessoas_incorretas` | verbete novo | 5 | 0 | 0 | 0 |
| run-3 | `limite_de_requisicoes` | retificação | 0 | 0 | 0 | 4 |
| run-5 | `contrato-pedido` | nota | 5 | 0 | 0 | 27 |
| efe-4 | `estado_da_tela_divergente` | retificação | 8 | 0 | 2 | 20 |
| sin-15 | `colecao_no_lugar_de_objeto` | nota | 0 | 0 | 0 | 7 |
| semt-6 | `tipo_divergente` | nota | 6 | 0 | 3 | 15 |
| semt-7 | `tipo_divergente` | retificação | 5 | 1 | 0 | 12 |
| semt-10 | `tipo_divergente` | nota | 2 | 0 | 0 | 11 |
| semt-15 | `validacao-na-api` | verbete novo | 3 | 0 | 0 | 0 |
| tra-6 | `formato_preco` | verbete novo | 4 | 0 | 1 | 0 |
| tra-14 | `contagem_inconsistente` | nota | 3 | 0 | 0 | 17 |
| run-12 | `erro_interno_do_servidor` | nota | 0 | 0 | 0 | 5 |
| efe-8 | `estado_da_tela_divergente` | nota | 4 | 1 | 0 | 13 |
| efe-8 | `atualizacao-da-tela` | verbete novo | 7 | 1 | 0 | 0 |
| efe-10 | `interface-frontend` | nota | 0 | 0 | 0 | 0 |
| efe-11 | `localizador_quebrado` | nota | 2 | 0 | 0 | 13 |
| efe-13 | `estado_da_tela_divergente` | nota | 6 | 1 | 0 | 11 |
| efe-4 | `contrato-produto` | nota | 9 | 0 | 0 | 65 |

### 4.6 Limpeza sem modelo

O modelo não percebe quando um verbete foi corrigido, então não é ele quem julga o que está velho. A limpeza é uma lista gerada por código e decidida por uma pessoa. Os sinais, todos contáveis:

- a nota ou o verbete nunca esteve entre os três entregues em nenhum caso com gabarito;
- o texto está em forma de instrução (25 das 26 notas de hoje);
- o caso que originou a edição teve o diagnóstico recusado por uma pessoa depois;
- o portão da busca mostra que a edição tira o verbete certo de algum caso.

Nada se apaga: o item vai para a espera, com a data e o motivo, e o histórico fica. O efeito de tirar de uma vez todas as notas de hoje é o que a corrida 25 mede.

### 4.7 Onde cada coisa fica

| Lugar | O que guarda | Muda quando |
|---|---|---|
| `biblioteca_producao/` | o que o modelo lê | só por lote promovido |
| `aprendidos_em_espera/` | propostas sem efeito medido e itens arquivados | a cada lote |
| pasta do lote, na corrida | as propostas, os portões de cada uma e a aprovação | a cada lote |
| `biblioteca_producao_leitura/` | a camada de leitura para pessoas | pede nova curadoria do verbete que mudou |
| trilha da execução | eventos `edicao_biblioteca` com a origem, os portões e a aprovação | a cada proposta |

## 5. Quanto custa nesta máquina

Uma chamada do analista com a ficha curta custa cerca de 95 s, contra 158 s da proposta de hoje. Ela roda em segundo plano e não entra no tempo até o resultado do diagnóstico. Os portões:

| Portão | Custo nesta máquina |
|---|---|
| Filtros em código e portão da busca | segundos, sem modelo |
| Portão do diagnóstico em todos os casos que leriam cada edição (lote da corrida 20) | 221 diagnósticos, 4,2 horas |
| Reavaliação do lote nos 36 inéditos, como a regra R5 fez | 36 diagnósticos, 39 minutos |
| Os 72 casos (os oficiais de avaliação e os inéditos), como a corrida 25 | 72 diagnósticos, 82 minutos |

O portão do diagnóstico é o caro: um verbete que a busca entrega muito, como `contrato-produto`, seria lido por 65 dos 126 casos; a mediana é de 9 casos por edição. Daí o teto por edição: acima dele, a edição só é medida no lote, e a regra dos 40% já manda esse tipo de verbete para a revisão de uma pessoa.

O custo que não foi medido é o da pessoa: o tempo de revisão por edição não aparece em nenhuma corrida nem em nenhuma fonte lida.

## 6. O que teria de ser medido, e com quais corridas

| Medida | O que responde | Modelo | Custo |
|---|---|---|---|
| M1. Os portões 3, 4 e 5 aplicados às 92 propostas da corrida 20, contra a revisão humana | quantas edições erradas e parciais cada portão recusaria, e quantas corretas perderia | não | minutos, sem máquina de inferência (o portão 5 já está na seção 4.5) |
| M2. O analista com a ficha curta nos 54 casos de aprendizado da corrida 20, com o gabarito no lugar da decisão da pessoa, e a mesma revisão humana, às cegas | se a entrada própria e uma proposta por caso mudam a parcela correta, a abstenção e a forma do texto; é a comparação que a literatura não tem (mesmo modelo, mesmos casos) | sim | 54 inferências, cerca de 86 minutos, mais a revisão humana |
| M3. O portão do diagnóstico nas edições que passarem na M2 | quantas edições têm efeito medido e quantas vão para a espera | sim | depende de quantas passam; o teto por edição limita |
| M4. Se um lote for promovido: os 72 casos de novo, pareados com as corridas 22 e 24 | se a biblioteca nova muda o diagnóstico (decisão 69) | sim | 82 minutos, mais a ponte de versão do Ollama |
| M5. Com o hub: a decisão da pessoa como rótulo, no lugar do gabarito | quantas edições a pessoa aprova e quanto tempo gasta por edição | sim | depende do pacote Q6 |

O que recalibrar. O selo de confiança foi calibrado na corrida 16, com a biblioteca de antes do lote da corrida 20, e seguiu valendo depois da promoção porque a regra R5 não mostrou mudança. A mesma regra serve aqui: se a M4 mostrar mudança fora do ruído, repetem-se a calibração (os 90 casos, cerca de 83 minutos) e as corridas da tela e dos cenários (18d e 21d) antes de qualquer número novo valer. O prompt do diagnóstico não muda em nenhuma dessas medidas.

## 7. O que conflita com as decisões 69, 103 e 105

**Decisão 69** (o padrão é o modelo com a biblioteca que ele mesmo escreveu; trocar o modelo que lê exige medir de novo). A proposta mantém o mesmo modelo como analista, de modo que o par não muda. Mas todo lote promovido muda a biblioteca que o modelo lê, e pela 69 isso pede medir de novo: é a medida M4. Se um dia o analista for outro modelo, o par muda e a medida é a inteira.

**Decisão 103** (os verbetes da biblioteca de produção não mudam; o que o relatório, o hub e a revisão humana mostram à pessoa sai de uma camada de leitura fora dela). Criar, corrigir ou limpar verbetes é o contrário de "não mudam". A proposta só convive com a 103 enquanto nada é promovido, com as propostas e os itens arquivados fora da produção. Promover um lote, ou arquivar uma nota de hoje, pede decisão nova que diga como a 103 passa a valer. E cada verbete que mudar invalida a leitura curada dele (`biblioteca_leitura.py --check` acusa o verbete que mudou depois da leitura), o que custa nova curadoria por uma pessoa.

**Decisão 105** (o plano da Pós-Fase 4 aprovado como está: os pacotes Q1 a Q5 antes da Fase 5 e o hub, pacote Q6, depois dela; nenhuma corrida repetida, prompt e biblioteca intactos. O texto do plano que ela aprova traz ainda a regra de nenhuma segunda chamada ao modelo: filtros, árvore e relatório são código). Implementar os dois momentos antes da Fase 5 é desvio do plano e obriga a repetir corridas. E a decisão da pessoa, de que o desenho depende, vem do hub, que o plano pôs depois da Fase 5 (decisão 101). A proposta cabe no plano se ficar como desenho agora e implementação junto do pacote Q6. A chamada do analista não é chamada nova no agente: a proposta de edição já consta da especificação da trilha (seção 4.4, uma inferência, quando houver); o que muda é a entrada, o momento e os portões.

Outras regras que a proposta toca: a biblioteca só cresce por acréscimo (decisões 30 e 33; especificação da trilha, seção 10), e mandar um item para a espera não apaga nada, mas tira texto do que o modelo lê, o que é mudança de regra a decidir; os filtros em código entram e a segunda chamada só depois de medir o custo (decisão 65), atendida pelas medidas da seção 5; o prompt do diagnóstico congelado (decisões 79 e 91), que a proposta não toca, porque o analista tem prompt próprio.

## 8. O que a proposta não resolve

- **A qualidade do que um modelo de 7B escreve.** Os portões reduzem o que entra; não melhoram o que é escrito. A expectativa realista é de poucas edições por lote, quase todas `sinal_de_busca`.
- **A decisão da pessoa pode estar errada.** Na sessão de revisão, a decisão foi apropriada em 30 de 36 relatórios. Por isso a chamada só vale quando a pessoa informa a causa, e o lote ainda passa pelos casos com gabarito.
- **O portão da busca só enxerga os casos que existem.** Uma edição pode atrapalhar um caso que ainda não foi escrito.
- **Mais um prompt para congelar e medir.** O prompt do analista vira peça medida, como o do diagnóstico.

## 9. O que fica para o Eric

A ficha 67: aprovar ou não esta proposta como base de desenho, e quando. A recomendação é aprovar como base para depois da Fase 5, junto do hub, e fazer antes disso só a medida M1, que não gasta modelo. Se a corrida 25 mostrar que as notas de hoje atrapalham o diagnóstico, a limpeza delas vira decisão própria, antes ou depois da Fase 5.

## 10. Rastreabilidade

Pesquisa: levantamento §6.16.6 (o papel separado), §6.16.7 (degradação e portões), §6.16.9 (as medidas do repositório) e §6.16.10 (o veredito da ideia 3); antes dela, §6.9.6, §6.13.3, §6.13.7, §6.13.10 e §6.15.1. Código lido, sem alteração: `estrategias.py` (`_FORMATO_PROPOSTA`, `proposta_de_edicao`), `biblioteca_fase4.py` (`propor_p5`, `filtrar_proposta`, `promover`, `mover_para_espera`), `evolucao_biblioteca.py`, `experimento_sem_notas.py`, `diagnostico_ao_vivo.py`. Dados: `resultados_alvo/fase4/biblioteca.json`, `fase4_biblioteca/lote.json`, `revisao_do_lote.md` e `propostas__E101.jsonl` (corrida 20), `ineditos.json` (corrida 24), `sem_notas_previa.json` (prévia da corrida 25), `leitura_revisao_v3.json`, `taxas_progresso.json`; tudo por `ferramentas/medidas_fluxo_do_agente.py`. Decisões 30, 33, 65, 69, 79, 91, 93, 101, 103, 105 e 116; especificação da trilha, seções 4.4 e 10; ficha 64.
