<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
# Decisões tomadas

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá.

## 2. Decisões tomadas

Registradas com a autoria, porque a distinção entre o que foi decidido pelo grupo e o que foi recomendação técnica importa para a seção de metodologia.

| # | Decisão | Quem decidiu | Fundamento |
|---|---|---|---|
| 1 | **Dois alvos separados**: manter o `CobaiaFront` intocado como sistema legado e construir uma `CobaiaAPI` nova para o cenário de API JSON | Eric, entre 3 opções apresentadas | Preserva o site cedido sem risco e cria a fronteira HTTP que a pesquisa exige |
| 2 | `CobaiaAPI` em **Python + FastAPI** | Eric | Tipagem do Pydantic facilita simular quebra de contrato; alinha com o vocabulário já usado no documento |
| 3 | **Um único banco compartilhado** entre os dois alvos | Eric | Evita dado inconsistente; produz o cenário realista de duas interfaces sobre o mesmo backend |
| 4 | A aba de API é uma **página nova dentro do próprio site**, com o mesmo layout | Eric | Mantém a navegação e a aparência do sistema legado, isolando a diferença na origem dos dados |
| 5 | Credencial SMTP exposta no código **fica como está** | Eric | Ambiente de teste, sem dado real de pessoa ou empresa |
| 6 | Repositório **"hit and run"**: um instalador único cobre tudo, em Windows e Linux | Eric | Facilita o uso pelos 9 integrantes e a demonstração ao vivo na banca |
| 7 | **LLM 100% local e gratuito** (Ollama), substituindo o Google Colab + FastAPI + Ngrok do projeto original | Eric | A ferramenta precisa ser usável fora da universidade, sem custo e sem configurar nuvem |
| 8 | Escopo do Self-Healing: **diagnóstico + cura de seletor**, sem propor patch do código da aplicação | Eric, entre 3 opções | Tarefa restrita o bastante para um modelo quantizado pequeno acertar, e mensurável por MTTR e Task Success |
| 9 | Navegador do agente: **Chromium do próprio Playwright**, não Chrome/Edge do sistema | Eric (após apontar que Edge inviabiliza Linux) | Versão fixa garante reprodutibilidade das métricas; mesmo comando nos dois sistemas |
| 10 | Convenção de comentários: a marca de alteração por IA **nunca vem sozinha** — sempre com o que foi feito e o motivo | Eric | O revisor precisa entender o contexto sem reabrir a investigação |
| 11 | Nomenclatura CamelCase com prefixo húngaro é **do projeto ERP, não deste** | Eric, entre 3 opções | Evita duas convenções conflitantes no mesmo repositório; aqui vale PEP8 |
| 12 | Correções no projeto de pesquisa ABNT feitas **diretamente no arquivo**, marcadas | Eric, entre 4 opções | Mais rápido; o grupo revisa depois |
| 13 | Cada modelo constrói a **própria biblioteca**, com uma **rodada de controle** usando biblioteca de referência | Eric, entre 3 opções | Separa "biblioteca ruim" de "raciocínio ruim", que ficariam confundidos numa nota única |
| 14 | Resultados em **imagens + relatório HTML** | Eric | Imagens alimentam o documento; o relatório permite explorar os dados |
| 15 | **5 a 6 modelos** na comparação | Eric, entre 3 faixas | Equilíbrio entre abrangência e profundidade da análise por modelo |
| 16 | Manter `qwen2.5-coder:3b` apesar da licença de pesquisa | Eric | Documentar a restrição; trocar apenas o padrão de produção |
| 17 | `.gitignore` mínimo, revisto depois com base em evidência | Eric | Ver seção 4.11 |
| 18 | **GPT-2 e GPT-3 descartados** como modelos de comparação | Eric, após validação | GPT-3 nunca teve pesos liberados e os originais foram desligados em 04/01/2024; GPT-2 é base sem instrução, só inglês e fora da biblioteca oficial do Ollama — três variáveis de confusão de uma vez (ver 6.3) |
| 19 | Fase 2-B **fixa o prompt em linear** e varia só a biblioteca | Eric (plano aprovado) | Nos cinco modelos completos as três estratégias empatam; no melhor modelo linear é significativamente melhor e as em estágios frequentemente não concluem; linear é a mais barata em tokens (4.16). Cruzar 3 estratégias × condições triplicaria o custo sem responder nada novo |
| 20 | A biblioteca entra **antes** do caso no prompt | Eric (plano aprovado) | Duas razões medidas na literatura: o começo é uma das duas posições em que modelos pequenos ainda acham a informação, e prefixo idêntico é o único arranjo em que o cache de KV pode reaproveitar o prefill (6.3, 6.5) |
| 21 | Defeitos conhecidos do cobaia **documentados, com marcação separada** (`tipo: defeito_conhecido`) | Eric, entre 3 opções | Permite separar nos resultados o acerto em casos com verbete de defeito dedicado do acerto nos demais — se o ganho aparece só no primeiro grupo, o efeito é de consulta; se nos dois, é raciocínio melhor ancorado |
| 22 | **Grade completa** da Fase 2-B (~2.070 inferências, 25–60 h de CPU) | Eric, entre 3 orçamentos | É o único desenho que separa falha de recuperação de falha de raciocínio (braço "só o verbete certo") e mede adesão cega à documentação errada (braço adversarial) |
| 23 | Recuperação por **BM25 + sinais calculados em código**, em biblioteca padrão; embedding denso só como ablação offline | Recomendação técnica | Zero dependência nova preserva o "hit and run"; reranking não se paga em corpus pequeno e curado (6.3); os sinais em código levaram hit@3 de 58,9% a 78,9% (4.19) |
| 24 | Modelos das ablações A3–A5: `granite4.2:8b`, `qwen2.5-coder:3b` e `phi4-mini:3.8b` | Recomendação técnica | Melhor, padrão de produção atual e piso **não degenerado**; o `1.5b` responde o mesmo rótulo em 84% dos casos (4.17) — ablação sobre modelo que não faz a tarefa não ensina nada |
| 13' | *(revisão da 13)* a geração da biblioteca pelo próprio modelo passa a ser **Fase 3** | Eric | Na Fase 2-B os modelos só consultam a biblioteca base, para isolar "buscar, localizar e seguir" de "produzir" |


