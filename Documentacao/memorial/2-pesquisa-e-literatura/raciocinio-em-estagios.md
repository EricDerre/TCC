<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
<!-- ! Alteração de IA - Revisar: revisão de 11/09/2026 — a "lacuna encontrada" passou de "não
     existe nenhum trabalho publicado" para "não localizamos, no levantamento de 2026,
     trabalho publicado que", com SPRAGUE et al. (2025) e LI et al. (2025) como respaldo;
     PA-Tool, Constraint Tax e F-CoT ganharam a identificação que consta de referencias.md; e
     foi acrescentada a âncora nos Caps. 7 e 10 do livro-texto (FACELI et al., 2025).
     ! Motivo: "não existe nenhum trabalho publicado" é afirmação sobre a totalidade da
     literatura, que uma rodada de busca não sustenta — na defesa, basta um artigo para
     derrubá-la, e o resultado do TCC não depende dela. Os três trabalhos citados só por
     apelido ("PA-Tool", "The Constraint Tax", "F-CoT") não eram localizáveis por quem lesse a
     seção sem o chat: os apelidos não aparecem nos títulos publicados. -->
<!-- ! Alteração de IA - Revisar: em 12/09/2026 a citação de LI et al. (2025) na "lacuna
     encontrada" ganhou a marca [conferir], com o motivo do verificador.
     ! Motivo: `referencias.md` e o levantamento de 11/09/2026 marcam essa fonte como de
     suporte parcial (o número que circulava era a lacuna média da Tabela 1, não o "mais de
     10 pontos" do texto do artigo), e esta seção a citava sem a marca — ficava mais forte
     aqui do que na própria lista de referências. -->
# Pesquisa bibliográfica — Raciocínio em estágios para modelos pequenos

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá.

### 6.2 Raciocínio em estágios para modelos pequenos

Investigação motivada pela proposta de estruturar a análise do agente nas fases de um compilador. O vocabulário conceitual usado aqui — o que é aprender a classificar a partir de exemplos, o que uma rede profunda faz com o que recebe e como se mede o acerto de um classificador multiclasse — vem do Cap. 7 (Métodos Conexionistas) e do Cap. 10 (Avaliação de Modelos Preditivos) de FACELI et al. (2025) *[capítulo inferido do sumário; conferir no exemplar]*.

**O que está bem estabelecido:**
- Chain-of-Thought **degradava** modelos pequenos no regime de 2022 — LaMDA 8B caiu de 3,2% para 1,6% em GSM8K, e o padrão se repete em toda a faixa abaixo de 10B (Wei et al., 2022). **Ressalva honesta:** eram modelos *base* de 2022; extrapolar para um Qwen2.5-3B-Instruct atual é inferência, não resultado — é justamente a lacuna que nosso experimento mede.
- O ganho de CoT concentra-se em **matemática e lógica simbólica**; fora disso é pequeno (Sprague et al., ICLR 2025).
- Há perda documentada de **até 36,3 pontos** em tarefas de classificação com exceções (Liu et al., ICML 2025) — que é a forma da nossa tarefa.
- Em pipeline de *n* estágios com confiabilidade *p*, o sucesso é *pⁿ*: com 6 estágios e p=0,85, cerca de 38%. Aritmética, não hipótese.

**O que mudou o desenho do experimento:** o trabalho conhecido no levantamento como PA-Tool — publicado como *Don't Adapt Small Language Models for Tools; Adapt Tool Schemas to the Models* (ACL, 2026) — mediu **+17 pontos no Qwen2.5-3B apenas por alinhar nomes de schema ao que o modelo viu no pré-treino**, com queda de 80% nos erros de aderência. "Análise léxica" carrega prior fortíssimo de *tokenizar código-fonte*; aplicá-lo a comparação de payload HTTP convida o modelo ao prior errado. Por isso o teste passou de dois para **três braços**: linear, estagiado com nomes de compilador, e estagiado com nomes de domínio — isolando o efeito do *nome* do efeito da *estrutura*.

**Lacuna encontrada:** não localizamos, no levantamento de 2026, trabalho publicado que proponha fases de compilador como andaime de prompting. A ausência não prova que a ideia é ruim nem que ninguém a tenha testado: significa que ela não apareceu nas buscas feitas — e torna o resultado publicável nos dois sentidos. O que a literatura verificada sustenta é o entorno da hipótese, não ela: o ganho de raciocínio explícito concentra-se em matemática e raciocínio simbólico, empatando com a resposta direta no MMLU (SPRAGUE et al., 2025), e cadeia de raciocínio longa **piora** modelos de até 3B, com o Qwen2.5-3B-Instruct recuperando mais de 8 pontos em MATH e AMC ao misturar cadeias curtas em vez de usar só as longas (LI et al., 2025) — **[conferir]**: o verificador do levantamento de 11/09/2026 marcou a fonte como de suporte parcial, porque a queda de 7,1 pontos que circulava para o Qwen2.5-1.5B é a lacuna média entre benchmarks da Tabela 1, enquanto o texto do artigo fala em "mais de 10 pontos" em MATH e AMC; os números devem ser citados como médias, com o modelo e o benchmark ao lado.

**Métrica que teria passado despercebida:** *wrong-valid-schema* — resposta que parseia perfeitamente mas está semanticamente errada. O trabalho *The Constraint Tax: Measuring Validity-Correctness Tradeoffs in Structured Outputs for Small Language Models* (RAY, 2026), único no regime sub-3B, mediu validade subindo de 61,5% para 100% enquanto a acurácia caía de 19,7% para 11,0% e o erro semântico saltava para 88,9%. Medir apenas "parseou?" deixaria cego para a maior parte dos erros.

**Convergência com o achado empírico da seção 4.12:** o trabalho *Focused Chain-of-Thought: Efficient LLM Reasoning via Structured Context* (2026), citado no levantamento como F-CoT, mostra que o estágio de *extração* é exatamente onde modelos pequenos falham (um Qwen-3 0.6B gerou contexto estruturado válido em menos de 2% dos casos). Pré-calcular o diff em código é remover do modelo justamente esse estágio — o que havíamos descoberto medindo, antes de encontrar a literatura.

<!-- ! Alteração de IA - Revisar: parágrafo-ponte para as subseções da rodada 2 da pesquisa (21/09/2026), acrescentado ao fim da seção.
     ! Motivo: a rodada 2 fechou as lacunas que esta seção apontava; sem o ponteiro, quem lê a seção não sabe que o levantamento cresceu (§6.9.9–6.9.17) nem que existe o mapa de decisões (§6.10). Nenhum número novo é digitado aqui: os números ficam nas subseções citadas. -->
## Complemento da rodada 2 da pesquisa (21/09/2026)

A §6.9.14 do [levantamento](levantamento-2026-09-11-fase-3.md) (decomposição em estágios e cadeia de pensamento em modelos de 1,5B a 8B) reúne a evidência verificada de que raciocínio explícito não ajuda classificação de texto em modelos pequenos e de que o desenho de manter o diff de contrato e os sinais de recuperação em código, com o modelo só como seletor de rótulo, é o que a literatura chama de planejador com resolvedor por ferramenta. O modo de falha "rótulo inventado" medido na 2-A ganha ali o nome teórico de cadeia fluente porém ilógica. As implicações entram no [mapa de decisões](mapa-de-decisoes-fase-3.md) (§6.10).
