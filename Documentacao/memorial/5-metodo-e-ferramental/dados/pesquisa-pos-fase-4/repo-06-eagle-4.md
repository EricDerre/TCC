<!-- ! Alteração de IA - Revisar: arquivo novo (07/11/2026): leitura feita por um subagente do Claude (modelo Sonnet) sobre repositório eagle-hq/EAGLE-4, na rodada 6 da pesquisa (Pós-Fase 4); é um arquivo de dados que ferramentas/integrar_pesquisa_pos_fase4.py lê para montar o levantamento §6.15, e o integrador tira este comentário do texto que entra lá.
     ! Motivo: o Eric pediu em 07/11/2026 a base de pesquisa de cada ponto da Pós-Fase 4 e a validação de oito repositórios do GitHub; a leitura fica versionada como dado para o levantamento ser regerado por script e conferido pelo --check. O texto é o que o subagente escreveu, sem edição, com a marca de confiança que ele deu a cada fonte (aberta e lida; só o resumo de busca; de memória). -->
# eagle-hq/EAGLE-4 (pacote eagle-harness)

Fontes lidas: página do repositório no GitHub e README bruto (raw.githubusercontent.com). Não li docs/ nem o PDF EAGLE4_Paper.pdf (interesse MÉDIO; a página e o README bastam para o veredito).

## 1 O que é e como funciona por dentro

- É decodificação especulativa: um modelo rascunho (drafter) propõe tokens candidatos e o modelo alvo os verifica em lote; a saída final é a mesma que o alvo geraria sozinho (README: "same answers", temperatura 0).
- O pacote `eagle-harness` liga drafters EAGLE-4 a três motores de servidor: SGLang, vLLM e TokenSpeed. Ele mede custos reais no hardware instalado e ajusta o tamanho da árvore de rascunho conforme tamanho do lote, hardware e carga.
- Residente: o modelo alvo e o drafter EAGLE-4 ficam carregados juntos no mesmo servidor (download inicial de cerca de 62 GB no quick start). Os primeiros pedidos após a partida compilam kernels e calibram, por isso são mais lentos.
- Ganhos medidos (Qwen3.8-27B, temperatura 0, cliente SPEED-Bench, 4 GPUs NVIDIA B300): SGLang 3,42x com 1 requisição, 2,09x com 8, 1,39x com 64; vLLM 2,83x, 1,72x, 1,14x; TokenSpeed 3,09x, 2,02x, 1,41x. Em uma AMD MI355X com SGLang: 2,07x com 8 requisições e 1,56x com 32.
- O ganho cai conforme a concorrência sobe. Nenhuma medição em CPU, em laptop ou com modelo de 7B aparece na página.

## 2 Pilha, dependências e exigências

- GPU: sim, obrigatória. Quick start testado em uma B300 com Linux e driver CUDA 13; ROCm suportado para MI355X. Pip exige Python 3.12, CUDA toolkit e compilador C++.
- Nuvem e chave de API: não exigidos (é servidor local), mas o hardware alvo é de datacenter.
- Outro modelo residente: sim, o drafter fica junto do alvo.
- Runtime: SGLang (pin `sglang==0.5.23.dev252+eagle.9`), vLLM ou TokenSpeed; imagem Docker `ghcr.io/eagle-hq/eagle-4-sglang:0.1.3`. Não há suporte declarado a Ollama nem a llama.cpp. Tópicos do repositório: eagle, gpu, llm-inference, sglang, speculative-decoding, tokenspeed, vllm.
- Licença: Eagle 4 Source-Available License, "não OSI" (código disponível, não é open source). Uso comercial de oferta concorrente exige licença comercial; demais usos comerciais têm teto de US$ 20 milhões de receita agregada em 12 meses. Contribuições sob termos próprios da Eagle AI Corp. Para um TCC acadêmico sem receita o uso seria permitido, mas a licença é restritiva.
- Maturidade: 1,2 mil estrelas, 40 forks, 77 commits em main, 2 issues e 1 PR abertos. Releases e tags: nenhum listado. Data de criação: não vista na página. Data do último commit: não vista na página (procurei na página principal do repositório). Há CHANGELOG.md, CITATION.cff, SECURITY.md e docs/ (não lidos). Versão visível: imagem 0.1.3 e pin de SGLang em dev.

## 3 Aplicação ao desenvolvimento com o Claude Code neste projeto

- Não serve. O Claude Code consome modelos hospedados pela Anthropic; não há ponto onde um drafter local acelere a geração dele.
- Custo de instalar e manter: inviável sem GPU NVIDIA/AMD recente e Linux. Nenhum benefício para CLAUDE.md, memória, skills ou subagentes.

## 4 Aplicação dentro do agente ou do produto

O módulo candidato seria o diagnóstico com o qwen2.5:7b servido pelo Ollama. Conflitos com o contexto:

- CPU sem GPU: o repositório exige GPU (CUDA 13 ou ROCm) e os kernels são de GPU. Conflito direto e bloqueante.
- Ollama como runtime: o pacote só se integra a SGLang, vLLM e TokenSpeed. Trocar de runtime quebraria o harness, o prompt congelado byte a byte e a leitura de probabilidade por token já validada no Ollama.
- Um modelo residente por vez: o EAGLE-4 mantém alvo e drafter residentes. Mesma razão pela qual o projeto adiou a decodificação especulativa.
- 16 GB de RAM e Windows 11 sem administrador: o quick start baixa cerca de 62 GB e pressupõe Linux e Docker/compilador C++; nada disso cabe na máquina-alvo.
- Nada em nuvem e só biblioteca padrão no harness: o pacote traz pilha pesada de dependências (SGLang, PyTorch cu130, índices extras), fora do padrão do harness.
- Prompt congelado e fidelidade: a saída idêntica em temperatura 0 seria um ponto a favor, mas o ganho medido é para lotes e GPU, não para CPU com uma requisição de 7B.
- Licença source-available: exigiria revisão para qualquer redistribuição junto ao produto.

## 5 Risco, esforço e veredito

- Risco: alto de tempo perdido (hardware inexistente, runtime diferente, licença restritiva, sem releases formais).
- Esforço: não aplicável na máquina atual. Mesmo como estudo teórico, uma sessão de leitura do paper bastaria para citar como trabalho relacionado.
- Veredito Claude Code: não serve, o Claude Code roda modelos hospedados e o repositório só acelera servidores locais com GPU.
- Veredito agente: não serve, exige GPU, SGLang/vLLM e um segundo modelo residente, conflitando com CPU, 16 GB, um modelo por vez e Ollama; vale no máximo como citação de trabalho relacionado sobre decodificação especulativa adiada.

## 6 Referências ABNT NBR 6023

EAGLE-4 TEAM. **EAGLE-4**: official inference code of EAGLE-4. Disponível em: https://github.com/eagle-hq/eagle-4. Acesso em: 7 nov. 2026.

EAGLE-4 TEAM. **EAGLE-4**: one flexible drafter for all batch sizes and hardware. Preprint, 2026. Disponível em: https://github.com/eagle-hq/eagle-4 (arquivo EAGLE4_Paper.pdf). Acesso em: 7 nov. 2026.

Os artigos EAGLE, EAGLE-2 e EAGLE-3 são citados apenas por nome em CITATION.cff; o README não traz autores, títulos nem URLs, então não os referencio (procurei no README e na página principal).
