<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
# Pesquisa bibliográfica — Raciocínio em estágios para modelos pequenos

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá.

### 6.2 Raciocínio em estágios para modelos pequenos

Investigação motivada pela proposta de estruturar a análise do agente nas fases de um compilador.

**O que está bem estabelecido:**
- Chain-of-Thought **degradava** modelos pequenos no regime de 2022 — LaMDA 8B caiu de 3,2% para 1,6% em GSM8K, e o padrão se repete em toda a faixa abaixo de 10B (Wei et al., 2022). **Ressalva honesta:** eram modelos *base* de 2022; extrapolar para um Qwen2.5-3B-Instruct atual é inferência, não resultado — é justamente a lacuna que nosso experimento mede.
- O ganho de CoT concentra-se em **matemática e lógica simbólica**; fora disso é pequeno (Sprague et al., ICLR 2025).
- Há perda documentada de **até 36,3 pontos** em tarefas de classificação com exceções (Liu et al., ICML 2025) — que é a forma da nossa tarefa.
- Em pipeline de *n* estágios com confiabilidade *p*, o sucesso é *pⁿ*: com 6 estágios e p=0,85, cerca de 38%. Aritmética, não hipótese.

**O que mudou o desenho do experimento:** o trabalho PA-Tool (ACL 2026) mediu **+17 pontos no Qwen2.5-3B apenas por alinhar nomes de schema ao que o modelo viu no pré-treino**, com queda de 80% nos erros de aderência. "Análise léxica" carrega prior fortíssimo de *tokenizar código-fonte*; aplicá-lo a comparação de payload HTTP convida o modelo ao prior errado. Por isso o teste passou de dois para **três braços**: linear, estagiado com nomes de compilador, e estagiado com nomes de domínio — isolando o efeito do *nome* do efeito da *estrutura*.

**Lacuna encontrada:** não existe nenhum trabalho publicado propondo fases de compilador como andaime de prompting. A ausência não prova que a ideia é ruim, mas significa que ninguém documentou ganho com ela — e torna o resultado publicável nos dois sentidos.

**Métrica que teria passado despercebida:** *wrong-valid-schema* — resposta que parseia perfeitamente mas está semanticamente errada. O trabalho "The Constraint Tax", único no regime sub-3B, mediu validade subindo de 61,5% para 100% enquanto a acurácia caía de 19,7% para 11,0% e o erro semântico saltava para 88,9%. Medir apenas "parseou?" deixaria cego para a maior parte dos erros.

**Convergência com o achado empírico da seção 4.12:** o trabalho F-CoT mostra que o estágio de *extração* é exatamente onde modelos pequenos falham (um Qwen-3 0.6B gerou contexto estruturado válido em menos de 2% dos casos). Pré-calcular o diff em código é remover do modelo justamente esse estágio — o que havíamos descoberto medindo, antes de encontrar a literatura.
