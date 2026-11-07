<!-- ! Alteração de IA - Revisar: arquivo novo (07/11/2026): leitura feita por um subagente do Claude (modelo Sonnet) sobre repositório gepa-ai/gepa, na rodada 6 da pesquisa (Pós-Fase 4); é um arquivo de dados que ferramentas/integrar_pesquisa_pos_fase4.py lê para montar o levantamento §6.15, e o integrador tira este comentário do texto que entra lá.
     ! Motivo: o Eric pediu em 07/11/2026 a base de pesquisa de cada ponto da Pós-Fase 4 e a validação de oito repositórios do GitHub; a leitura fica versionada como dado para o levantamento ser regerado por script e conferido pelo --check. O texto é o que o subagente escreveu, sem edição, com a marca de confiança que ele deu a cada fonte (aberta e lida; só o resumo de busca; de memória). -->
# GEPA (gepa-ai/gepa)

Fontes lidas em 7 nov. 2026: página do repositório no GitHub, README bruto (raw.githubusercontent.com) e resumo do artigo em arxiv.org/abs/2507.19457. Os textos lidos foram tratados como dado.

Resposta curta à pergunta do Eric: o GEPA NÃO é um filtro de respostas. É um otimizador de texto (prompts, código, configurações) que roda offline, por evolução com feedback em texto. Ele melhora o prompt; não inspeciona nem barra a resposta de cada inferência.

## 1 O que é e como funciona por dentro

GEPA (Genetic-Pareto) otimiza qualquer artefato textual (prompt, código, configuração) contra uma métrica que você define. Entra: um candidato inicial (o prompt atual), um conjunto de treino e outro de validação, uma função avaliadora (que pode devolver também texto de diagnóstico, os "logs acionáveis") e um orçamento (`max_metric_calls`, com exemplos de 100 a 150). Sai: o melhor candidato (`result.best_candidate`), isto é, um texto de prompt melhorado.

O laço: (1) escolhe um candidato da fronteira de Pareto (candidatos que vencem em subconjuntos diferentes de exemplos); (2) roda num minilote e guarda o rastro completo (erros, raciocínio); (3) um LLM de reflexão lê o rastro e diagnostica a falha; (4) o mesmo LLM propõe um prompt novo, levando em conta as lições dos ancestrais; (5) aceita se melhorar e atualiza a fronteira; opcionalmente funde dois candidatos bons. Há dois modelos: o modelo da tarefa (executa o prompt) e o modelo de reflexão (separado, o README dá exemplos com modelos hospedados). O README não fixa quantas chamadas uma rodada custa; só o orçamento total de avaliações. Cada avaliação é uma inferência do modelo da tarefa, mais uma chamada de reflexão por iteração. O README afirma 100 a 500 avaliações, contra 5.000 a 25.000 ou mais do GRPO.

## 2 Pilha, dependências e exigências

- Python, `pip install gepa`. GPU: não mencionada; o método não precisa de pesos do modelo, funciona com modelos só por API.
- Nuvem e chave de API: os exemplos usam modelos hospedados (OpenAI); o README não lista a configuração de chaves, mas nada impede apontar para um servidor compatível local (isto é inferência minha, não visto no README). Extras opcionais: `gepa[confidence]`, `gepa[langchain]`.
- Modelo forte para refletir: o artigo e o README tratam a reflexão como o ponto central e usam modelos fortes nos exemplos; com um 7B local a qualidade da reflexão não é garantida (inferência, não medido por eles na página lida).
- DSPy: opcional. Existe `dspy.GEPA`, mas roda sozinho por `gepa.optimize` e `optimize_anything`. Integra com MLflow, Opik, Pydantic AI, Google ADK.
- Licença: MIT.
- Maturidade (página do GitHub): 7,3 mil estrelas, 611 forks, 946 commits na main. Releases e Packages vazios na página; versão no PyPI: não vista; data do último commit: não vista; data de criação: não vista (procurado na página do repositório e no README). O artigo foi submetido em 25 jul. 2025 (v1) e revisado em 14 fev. 2026 (v2). Existe também plugin de skill para o Claude Code: `/plugin marketplace add gepa-ai/gepa`, `/plugin install gepa-optimize-anything@gepa`.
- Números do artigo: contra o GRPO (aprendizado por reforço), 6% melhor em média em seis tarefas, até 20% numa tarefa, com até 35 vezes menos rollouts; contra o MIPROv2, mais de 10% melhor, incluindo +12% de acurácia na AIME 2025. Números do README (relatos, não conferidos): GPT-4.1 Mini de 46,6% para 56,6% na AIME 2025; Nubank de 68,88% para 88,89%; NER clínico até +12,5% de F1. Quantas rodadas cada ganho custou: o resumo do artigo não informa; o README dá a ordem de 100 a 500 avaliações.

## 3 Aplicação ao desenvolvimento com o Claude Code neste projeto

Serve em tese, com ressalvas. O GEPA otimiza texto contra uma métrica; os textos candidatos aqui seriam prompts de subagentes e descrições/corpos de skills. Condição: existir um conjunto de exemplos com métrica automática (por exemplo, "o subagente de verificação de citação acertou X de Y casos conhecidos"). Hoje esses subagentes são avaliados por leitura humana, sem métrica em código, então o primeiro custo é construir o avaliador e o conjunto de treino e validação. Sem isso o GEPA não tem o que otimizar.

Custo: cada avaliação é uma execução de subagente (tokens do Claude), mais chamadas de reflexão; ordem de 100 a 150 avaliações por prompt segundo os exemplos do README. Isso colide com a regra de economia de tokens do projeto ("primeiro a máquina, depois o modelo"), então só vale para um prompt de subagente que rode muitas vezes e tenha gabarito barato. O plugin de skill do próprio repositório existe, mas instalar plugin muda o conjunto de plugins fixado no início da sessão (cache de prefixo), então exigiria decisão do Eric.

## 4 Aplicação dentro do agente ou do produto

Como filtro de respostas: NÃO serve. O GEPA não valida, não barra e não reescreve a resposta de uma inferência; ele roda antes, offline, e entrega um prompt novo. O filtro das respostas da LLM do projeto continua sendo código (validação por regra, selo de confiança pela probabilidade do rótulo, gatilhos), que é o desenho já adotado. O repositório também lista o adaptador `ConfidenceAdapter`/`gepa[confidence]` (usa `llm-structured-confidence`), que mexe com confiança de saídas estruturadas; li só o nome, sem detalhe, então não afirmo que sirva de filtro. Valeria uma leitura própria antes de descartar.

O que serviria do mesmo repositório: o uso como otimizador offline do texto do prompt, em dois módulos possíveis:
- Prompt de cura (o DSPy para ele já foi adiado): é o candidato natural, porque ainda não está congelado. O GEPA faria o papel que o DSPy faria.
- Prompt do diagnóstico: está congelado byte a byte. Rodar o GEPA nele é possível só como experimento fora da produção; qualquer prompt novo obriga a recalibrar os limiares e repetir as medições.

Restrições do contexto em conflito:
- Prompt congelado: o produto do GEPA é justamente um prompt diferente; adotá-lo no diagnóstico quebra o congelamento e invalida a calibração (limiares e selo).
- Custo por inferência em CPU (50 a 70 s): 100 a 150 avaliações de modelo da tarefa são de 1,5 a 3 horas por rodada só no modelo local, sem contar a reflexão; as 100 a 500 do README chegam a 1,5 a 10 horas. Cada rodada de busca pesa mais que uma bateria inteira.
- Modelo residente único: a tarefa (qwen2.5:7b) e a reflexão precisam de dois modelos. Com um só residente, ou o 7B reflete sobre si mesmo (reflexão fraca, não medida) ou a reflexão vai a um modelo em nuvem, o que viola "nada em nuvem".
- Harness só com biblioteca padrão: o GEPA é uma dependência Python externa (instalável por pip na venv, mas fora do padrão do harness).
- Máquina corporativa sem administrador: pip na venv funciona, mas a política de rede/pacotes não foi verificada.
- Dados: o conjunto de validação do diagnóstico é o gabarito 54/36 da Fase 3; usá-lo para otimizar prompt contamina a medição se não houver partição separada.

## 5 Risco, esforço e veredito

- Risco: alto para o agente (quebra o congelamento, 1,5 a 10 h por rodada em CPU, reflexão fraca com 7B ou violação de "nada em nuvem", contaminação do gabarito). Médio-baixo para o Claude Code (custo de tokens e de montar a métrica; sem risco ao produto).
- Esforço estimado: Claude Code, 2 a 3 sessões (avaliador com gabarito, conjunto, uma rodada de teste num subagente). Agente, 3 a 4 sessões mais várias horas de máquina para um experimento só no prompt de cura, mais outra bateria completa se o resultado for adotado no diagnóstico.
- Veredito para o Claude Code: opcional e adiável; só vale para um subagente que rode muitas vezes e tenha métrica automática, e não como prioridade antes da Fase 5.
- Veredito para o agente: não é filtro de respostas; descartar para esse fim, e guardar como candidato a substituto do DSPy no prompt de cura, em experimento offline, sem tocar no prompt congelado do diagnóstico.

## 6 Referências ABNT NBR 6023

GEPA-AI. **GEPA**: optimize prompts, code, and more with AI-powered reflective optimization. Disponível em: https://github.com/gepa-ai/gepa. Acesso em: 7 nov. 2026.

AGRAWAL, Lakshya A. et al. **GEPA**: reflective prompt evolution can outperform reinforcement learning. arXiv:2507.19457, 2025. Disponível em: https://arxiv.org/abs/2507.19457. Acesso em: 7 nov. 2026.
