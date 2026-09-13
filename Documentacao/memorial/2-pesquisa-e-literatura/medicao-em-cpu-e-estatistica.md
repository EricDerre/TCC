<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
<!-- ! Alteração de IA - Revisar: revisão de 11/09/2026 — "literatura de serving", que era uma
     citação sem fonte, virou ZHAO; LI; WU (2026) e LU et al. (2024) com a ressalva de
     hardware; o intervalo de Wilson ganhou a fonte original (WILSON, 1927) e a medição que
     desaconselha Wald com poucas centenas de casos (BOWYER; AITCHISON; IVANOVA, 2025); e foi
     acrescentada a âncora no Cap. 10 do livro-texto (FACELI et al., 2025).
     ! Motivo: esta seção é a que o relatório final cita para justificar McNemar e Wilson, e o
     intervalo de Wilson aparecia só pelo nome - sem a fonte de 1927 nem o número que explica
     por que não usar Wald com 90 casos (cobertura real de 92,5% em N=100), a escolha parecia
     preferência do autor. "Literatura de serving" tinha o mesmo problema: não é citação. -->
<!-- ! Alteração de IA - Revisar: em 12/09/2026 "esta máquina está na 0.33.2" passou a dizer em
     que momento isso valia e quais versões vieram depois (0.33.3 na 2-B; 0.34.0 na Fase 3).
     ! Motivo: o Ollama atualizou sozinho para 0.34.0 em 12/09/2026, antes da bateria da Fase 3;
     a frase no presente daria a entender que a Fase 3 roda na mesma versão da Verificação 0,
     e o relatório da Fase 3 (§11) declara a diferença de versão como fator não controlado. -->
<!-- ! Alteração de IA - Revisar: segunda passada de 12/09/2026 — em §6.5, "esta máquina estava
     na 0.33.2 quando a Verificação 0 rodou" passou a "o Ryzen estava na 0.33.2 quando o 4.21 foi
     medido", com a 2-B inteira (Verificação 0 incluída) em 0.33.3 na máquina-alvo.
     ! Motivo: a frase montava, para a máquina-alvo, a sequência 0.33.2 → 0.33.3 → 0.34.0, que
     nenhum artefato sustenta. O "0.33.2" entrou no commit 603c423 (03/09/2026), quando esta
     seção dizia "esta máquina está na 0.33.2" e a máquina de trabalho era o Ryzen — a decisão
     25, que fez do i5 a máquina-alvo, é de 07/09; o 4.21 é essa Verificação 0. Na máquina-alvo o
     `maquina.json` da 2-B registra "ollama version is 0.33.3" desde 07/09/2026 09:18, e o
     `fase2b.log` mostra a Verificação 0 rodando às 09:29 desse mesmo dia, antes da bateria. -->
# Pesquisa bibliográfica — Medição de tempo em CPU e estatística

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá.

### 6.5 Medição de tempo em CPU e estatística

- Prefill é limitado por computação e decodificação por banda de memória (SARATHI, 2023). O trabalho *Sandwich* mostra que as duas fases têm **demandas de recurso conflitantes em CPU** e que separar os planos de compilação por fase rende **2,01× de aceleração média fim a fim e até 3,40× de redução de latência**, medido em serving só-CPU sobre cinco plataformas x86/ARM (ZHAO; LI; WU, 2026) — é a justificativa mais direta para reportar as duas durações separadas em vez do tempo total. LU et al. (2024) quantificam a assimetria pelo lado da quantização: 4 bits reduzem a latência de prefill em cerca de **50%** e a de decode em **até 75%** — **[conferir]**, porque esses números foram obtidos com um único modelo (Phi-1.5) rodando na GPU de um Jetson Orin NX via llama.cpp, e não em CPU x86, o que os torna ordem de grandeza e não previsão para esta máquina. A biblioteca infla o **prefill**; por isso a bateria passou a gravar `prompt_eval_duration` e `eval_duration` separados, que o Ollama já devolvia e o harness descartava.
- **Cache de prefixo.** O llama.cpp reaproveita o KV do prefixo comum por *slot* (`cache_prompt`). No Ollama, a issue #14780 documenta que o backend de CPU do motor novo **não reaproveitava nada** na v0.17.1 (tempo crescendo linearmente por turno); correções aparecem referenciadas na v0.30.8; o Ryzen estava na **0.33.2** quando o 4.21 foi medido (Verificação 0 de 03/09/2026); na máquina-alvo a 2-B inteira, inclusive a Verificação 0 registrada no `fase2b.log` em 07/09/2026, rodou em 0.33.3, e a Fase 3 roda em 0.34.0, depois de uma atualização automática em 12/09/2026 — ver o relatório da Fase 3, §11. Não dá para assumir: `verificar_cache_prefixo.py` mede com o `prompt_eval_count` de chamadas consecutivas e é o passo zero da execução. Se o cache funciona, o prefill da biblioteca é pago uma vez por modelo; se não, são dezenas de segundos a mais por caso e o custo entra no resultado.
- **Teste estatístico.** Cada condição roda uma vez sobre os mesmos 90 casos — comparação pareada de classificadores executados uma vez. Para esse desenho, Dietterich (1998) mostra que **McNemar** é o único teste com erro tipo I aceitável; `avaliar.py` usa a versão exata (binomial) por caso, mais intervalo de **Wilson** para cada proporção (WILSON, E. B. *Probable inference, the law of succession, and statistical inference*. Journal of the American Statistical Association, v. 22, n. 158, p. 209–212, 1927). O motivo de não usar o intervalo clássico de Wald tem número: BOWYER; AITCHISON e IVANOVA (2025) medem, em simulações e reanálise de benchmarks de LLM, que o intervalo de 95% baseado no Teorema Central do Limite entrega apenas **92,5% de cobertura real com N = 100 itens**, degradando severamente em N = 30, 10 e 3, a ponto de produzir intervalos de largura zero ou fora de [0,1] — com 90 casos, Wald não é conservador, é errado. O instrumental de avaliação em si (matriz de confusão, métricas por classe, validação, viés-variância) é o do Cap. 10 de FACELI et al. (2025) *[capítulo inferido do sumário; conferir no exemplar]*. Tempo é reportado como **mediana e IQR** sobre os 90 casos, não média.


