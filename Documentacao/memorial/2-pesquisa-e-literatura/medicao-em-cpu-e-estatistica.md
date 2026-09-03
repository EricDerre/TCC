<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
# Pesquisa bibliográfica — Medição de tempo em CPU e estatística

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá.

### 6.5 Medição de tempo em CPU e estatística

- Prefill é limitado por computação e decodificação por banda de memória (SARATHI, 2023; literatura de *serving*). A biblioteca infla o **prefill**; por isso a bateria passou a gravar `prompt_eval_duration` e `eval_duration` separados, que o Ollama já devolvia e o harness descartava.
- **Cache de prefixo.** O llama.cpp reaproveita o KV do prefixo comum por *slot* (`cache_prompt`). No Ollama, a issue #14780 documenta que o backend de CPU do motor novo **não reaproveitava nada** na v0.17.1 (tempo crescendo linearmente por turno); correções aparecem referenciadas na v0.30.8; esta máquina está na **0.33.2**. Não dá para assumir: `verificar_cache_prefixo.py` mede com o `prompt_eval_count` de chamadas consecutivas e é o passo zero da execução. Se o cache funciona, o prefill da biblioteca é pago uma vez por modelo; se não, são dezenas de segundos a mais por caso e o custo entra no resultado.
- **Teste estatístico.** Cada condição roda uma vez sobre os mesmos 90 casos — comparação pareada de classificadores executados uma vez. Para esse desenho, Dietterich (1998) mostra que **McNemar** é o único teste com erro tipo I aceitável; `avaliar.py` usa a versão exata (binomial) por caso, mais intervalo de **Wilson** para cada proporção. Tempo é reportado como **mediana e IQR** sobre os 90 casos, não média.


