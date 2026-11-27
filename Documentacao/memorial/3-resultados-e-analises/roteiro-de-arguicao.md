<!-- ! Alteração de IA - Revisar: arquivo novo (27/11/2026): roteiro de arguição para a banca, com as seis perguntas que uma segunda revisão de fora previu e a resposta curta que o documento do TCC sustenta, com a seção de cada uma.
     ! Motivo: decisão 190: o Eric pediu o roteiro ao lado do relatório da Pós-Fase 4, para o grupo se preparar; as respostas saem só do documento, e as do parecer de fora não foram usadas. -->

# Roteiro de arguição para a banca

Este roteiro serve para o grupo ensaiar as seis perguntas que uma revisão de fora previu para a defesa. Cada resposta é curta e sai só do documento do TCC; a seção indicada em cada pergunta é onde o leitor confere o que foi dito, e onde estão os números e as limitações com o texto completo.

## 1. Por que o agente chama o modelo antes de curar o localizador, se a cura em código é tão rápida?

**Resposta curta:** a cura de seletor feita só em código resolveu as 160 quebras armadas, com mediana de 0,639 s. O agente completo, porém, chama o modelo para diagnosticar antes de curar, e por isso o tempo nos cenários de localizador é de outra ordem de grandeza: 67,6 s de mediana nos quatro cenários de localizador da corrida 21d e 74,0 s na média dos dez cenários. O documento diz que o tempo do agente é o tempo do modelo, e que a maior parte dele é a leitura do prompt. Nos quatro cenários de localizador da Fase 5 o agente levou de 39,0 a 65,4 s em média. O caminho rápido, que tente a cura em código antes de chamar o modelo, está declarado como trabalho futuro, e a lentidão na quebra de localizador está entre as limitações principais.

**Onde está no documento:** 6.7.1 (onde o tempo vai), 6.9 (Discussão, terceira parte e quadro das relações), 7 (limitações e trabalhos futuros), Apêndice D (as duas contas, mediana e média).

## 2. A biblioteca escrita pelo próprio modelo fracassou?

**Resposta curta:** o ganho dela não se sustentou. Na Fase 3, das 63 edições revisadas, 23 eram corretas, 17 parciais e 23 erradas, e 21 das corretas repetiam o verbete original. A primeira versão da biblioteca do qwen2.5:7b fez 32 certos nos 36 casos de avaliação e 26 nos 36 inéditos, abaixo dos 27 da biblioteca original. Na corrida 25, sem as notas do modelo, o agente acertou 54 de 72 casos contra 56 com a biblioteca inteira (p = 0,6875), e o tempo do meio por caso caiu de 66,35 para 57,63 s. O que moveu o acerto na tela foi a busca passar a usar o que o caso mede contra a tela normal: o verbete certo chegou ao modelo em 36 dos 37 casos, e não em 21, e o acerto foi de 27 para 32. O documento diz que o limite da biblioteca editada pelo modelo foi medido, e a Conclusão atribui o acerto à busca, e não à escrita do modelo.

**Onde está no documento:** 6.4.1, 6.5.1, 6.7.1, 6.7.2, 6.7.5, 6.9 (Discussão e quadro das relações), 7 (Conclusão, quarto objetivo).

## 3. Como defender a comparação com as pessoas, sendo só três estudantes do próprio grupo?

**Resposta curta:** o documento não afirma superioridade sobre analistas de teste: a linha de base são três estudantes do grupo no começo da prática, e com gente mais experiente o tempo das pessoas tende a ser outro. O resultado central é o do tempo: o agente reparou mais rápido nos 10 cenários, com MTTR médio de 66,3 s contra 219,7 s (teste dos sinais, p = 0,0020), e a regra que diz quando um lado foi mais rápido foi fixada antes de qualquer medida. O Task Success foi de 49 de 50 execuções do agente contra 14 de 30 tentativas das pessoas, resultado que depende da sessão de um integrante e é lido com essa ressalva: sem essa sessão, o Task Success fica sem veredito, e o do tempo continua. O documento também diz que a pessoa lê o registro capturado antes, e não o site no ar, e que a entrega errada e rápida entra no tempo médio dela como tempo curto, o que favorece as pessoas.

**Onde está no documento:** 6.8 e 6.8.1 (resultado e sessões), 6.9 (limitações da medida da Fase 5), 7 (quinto objetivo, expectativa do projeto de pesquisa e trabalhos futuros).

## 4. Como saber que o agente não está ajustado ao vocabulário da taxonomia e das aplicações do grupo?

**Resposta curta:** não dá para afirmar que não está, e o documento declara isso: as falhas são injetadas, não ocorridas, em duas aplicações sob controle do grupo, uma delas cedida por um integrante. A evidência em contrário são os casos inéditos, escritos só a partir do código do sistema: na corrida 18e o agente acertou 22 dos 25 que reproduzem na tela, e na corrida 24 acertou 25 dos 36 inéditos, com a ressalva de que são casos diferentes dos de avaliação. Quando o verbete certo chega ao modelo, são 18 de 20; quando não chega, 7 de 16, e a classe de tradução é a mais fraca, com 1 de 6. O documento também diz que os 36 inéditos foram escritos por IA e conferidos contra o código, que a regra R1 rodou mais larga que o texto do plano, e que as medidas valem para uma máquina e uma versão da biblioteca.

**Onde está no documento:** 5.3 (aplicações-alvo e injeção de falhas), 4.1.13 (representatividade da falha injetada), 6.5.1, 6.7.1, 6.7.2 (corrida 24), 6.7.4 (as regras da fase), 6.9 e 7 (limitações principais).

## 5. O agente serve para uma esteira de integração contínua, com cerca de um minuto por falha?

**Resposta curta:** o documento não mediu o agente dentro de uma esteira de integração contínua e diz isso como limitação. Cada falha custa ao agente cerca de um minuto de modelo em CPU, uma de cada vez (66,3 s de MTTR médio na corrida 28b), de modo que uma suíte com dezenas de falhas levaria dezenas de minutos. A maior parte desse tempo é a leitura do prompt: mediana de 83,1% do tempo do diagnóstico nos dez cenários da corrida 21b. Como trabalho futuro, o documento propõe agrupar as falhas de uma mesma rodada da esteira para chamar o modelo uma vez por causa provável, e não uma vez por falha. A seleção de cenários pelo Git também está descrita, e o documento diz que a seleção por arquivo não vê uma falha vinda de uma resposta ruim do modelo, e por isso a rodada completa volta em prazo fixo.

**Onde está no documento:** 6.7.1 (onde o tempo vai), 6.7.6 (hub de revisão e seleção pelo Git), 6.9 (limitações que atravessam as fases), 7 (limitações e trabalhos futuros).

## 6. Por que não prender a saída do modelo por gramática, se uma execução falhou por falta da linha FONTE?

**Resposta curta:** a gramática de saída (GBNF) ficou adiada na Pré-Fase 4, porque exigia outro motor e uma medição prévia, e a probabilidade lida no primeiro token do rótulo da causa é o sinal de triagem do agente, com AUROC de 0,78 na sonda de confiança; o prompt ficou congelado desde as Fases 2-A e 2-B, por causa da sensibilidade ao formato. A única execução sem Task Success na Fase 5 foi uma resposta sem a linha FONTE: o rótulo saiu certo, mas o diagnóstico não foi conferido em código e o cronômetro não fechou; nas outras quatro repetições do cenário, passou. O documento já lista isso como trabalho futuro: a saída presa às quatro linhas por uma gramática, com nova tentativa quando uma linha falta, e com a conferência de que a gramática não muda a probabilidade que o selo de confiança usa.

**Onde está no documento:** 4.1.9 (a probabilidade do rótulo), 5.5 (diagnóstico ao vivo e a leitura do primeiro token), 4.2.4 (o que a literatura descartou, tabela dos adiados), 6.6.1, 6.8.1 (a execução sem a linha FONTE), 7 (trabalhos futuros).
