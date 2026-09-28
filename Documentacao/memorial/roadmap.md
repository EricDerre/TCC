<!-- ! Alteração de IA - Revisar: roadmap do projeto em 28/09/2026 — onde cada fase está, o que ainda precisa rodar (comando, duração, o que fecha), o esqueleto das Fases 4 e 5 e uma tabela para o Eric encaixar os pontos dele por fase.
     ! Motivo: o Eric pediu "um roadmap de onde estamos e o que precisamos rodar" para arquitetar o novo plano; o plano complementar de 21/09 vive fora do git e as pendências dizem o que falta, mas nenhum documento junta estado por fase, corridas pendentes e o desenho das próximas fases num lugar só. Números de custo são as estimativas da análise decisória §10 e as medianas da bateria; nenhum número novo. -->
# Roadmap — 28/09/2026

Parte do [Memorial de Desenvolvimento](../Memorial%20de%20Desenvolvimento.md). Pendências e decisões em aberto em [pendencias.md](pendencias.md) (bloco de 23/09, itens 1–13); decisões numeradas em [decisoes.md](1-decisoes-e-historico/decisoes.md); painel interativo dos resultados em [`dashboard/dashboard-fase3.html`](../dashboard/dashboard-fase3.html) (gerado por `ferramentas/gerar_dashboard.py`).

## 1. Onde estamos, por fase

| Fase | O que é | Estado em 28/09/2026 |
|---|---|---|
| 1 — Ambiente e cobaias | Instalador único, CobaiaFront (PHP legado) e CobaiaAPI (FastAPI) com 7 modos de injeção de falha, banco de 90 casos | Concluída; dois casos do banco corrigidos em 28/09 (`efe-3`, `efe-10`, achado 4.36) |
| 2-A — Prompts sem documentação | 6 modelos × estratégias de prompt, máquina de desenvolvimento (Ryzen) | Concluída (relatório em `3-resultados-e-analises/fase-2a-relatorio-por-modelo.md`) |
| 2-B — Biblioteca recuperada | 6 modelos × condições A0–A5 na máquina-alvo (i5) | Concluída (07–09/09); definiu recuperação A2 e validação em código |
| 3 — Biblioteca gerida pelo modelo | 4 modelos × 3 épocas × 90 casos (13–15/09, 58h59) | Concluída e analisada; **decisão 52: `qwen2.5:7b` com L1**; relatório, comparação, análise decisória, achados 4.29–4.35, vereditos H1–H6 |
| 3-B — Testes complementares | Ponte de versão, troca cruzada, casos inéditos, sonda de correção | Ponte feita (21/09); cruzada e inéditos **prontos para rodar** (comandos abaixo); `banco_casos_ineditos.py` escrito e conferido (Eric confere 6 casos); sonda de detecção de correção rodada em 28/09 (§3) |
| 4 — Agente na tela | Interceptador Playwright (rede + árvore de acessibilidade), poda em código, cura de seletor, biblioteca em produção com ciclo de correção | Não iniciada; ferramental já decidido (decisão 55) e requisitos novos em §4 |
| 5 — Medição de valor | MTTR e Task Success contra linha de base manual, nas duas cobaias | Não iniciada; protocolo já escrito no projeto ABNT §3.4 |
| Documentação | Memorial (5 pastas), projeto de pesquisa ABNT, TCC final | Memorial em dia (decisões até 58, achados até 4.36, dashboard); ABNT com 11 modificações propostas em `4-projeto-de-pesquisa-abnt/correcoes-aplicadas.md` §5.1; TCC final não começado |

Posição no cronograma do projeto ABNT (§5, sem datas): fim do **Mês 2** (ambiente e comparação de modelos), com o Mês 1 (revisão bibliográfica) ampliado e parte do Mês 6 (redação) adiantada pelo Memorial. Os Meses 3–5 são as Fases 4 e 5.

## 2. O que precisamos rodar (máquina), em ordem

| # | Corrida | Comando (em `Programacao/AgenteCore/experimentos`) | Inferências / tempo | Pré-requisito | O que fecha |
|---|---|---|---|---|---|
| 1 | **Troca cruzada** — L1 e L3 do `qwen2.5:7b` lidas pelos dois Coder nos 36 | `powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo cruzada -Saida fase3b_cruzada_qwen -Doador qwen2.5:7b -Versoes 1,3 -Modelos qwen2.5-coder:7b,qwen2.5-coder:3b` | 144 / ~2,5 h (uma noite; espera 6,5 GB de RAM livre) | nada | Limitação 7 (escritor × leitor); entra em `decisao_modelo.md` §6 por `--saidas-3b fase3b_ponte fase3b_cruzada_qwen`. Ressalva: `efe-3` (nos 36) mudou de texto em 28/09 — 1 caso não pareável byte a byte com a Fase 3 |
| 2 | **Casos inéditos** — 36 casos novos, `qwen2.5:7b` e 3B em L0, L1 e L3 | `powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo ineditos -Saida fase3b_ineditos -Versoes 0,1,3 -Modelos qwen2.5:7b,qwen2.5-coder:3b` | 216 / ~3 h (uma noite) | Eric confere `lex-16`, `sin-20`, `semt-18`, `tra-19`, `run-20`, `efe-20` | Limitação 2 (teste reutilizado): o ganho de L1 generaliza? Avaliação por `avaliar_fase3b.py --saida fase3b_ineditos` |
| 3 | **Regeneração combinada** de `resumo_fase3.json` com a revisão das edições | `RESULTADOS_DIR=resultados_alvo python avaliar_fase3.py --saida fase3` | 1 min, sem modelo | "pode gravar" do Eric (pendência 1 de 23/09) | `revisao_humana` deixa de vir só das planilhas; ensaio já feito numa cópia (só esse arquivo muda) |
| 4 | **Sonda de detecção de correção** (feita em 28/09) | `RESULTADOS_DIR=resultados_alvo python sonda_correcao.py --saida fase3b_correcao --modelo qwen2.5:7b --versao 1 --casos efe-3 efe-10` | 4 / ~10 min | casos corrigidos (feito) | Primeira leitura do requisito do ciclo de correção (§4.2); repetir depois de cada correção de código na Fase 4 |
| 5 | (opcional) **A5 sobre L3** nos 36 — documentação própria e adesão cega | `powershell -ExecutionPolicy Bypass -File rodar_fase3b.ps1 -Modo a5 -Saida fase3b_a5 -Modelos qwen2.5:7b,qwen2.5-coder:3b` | 72 / ~1,3 h | nada | Mais um argumento sobre H5; não muda a decisão |
| 6 | **Integração da 3-B** (P6): `decidir_modelo.py --saidas-3b …`, `gerar_tabelas_relatorio_fase3.py`, blocos do relatório §11/§12 e da análise §9/§10, handoff | sem modelo | corridas 1 e 2 | Fecha o plano complementar de 21/09 |

Fora da máquina, na mesma ordem: aprovar (ou descartar) o servidor MCP e instalar o `pyright-lsp`; remover do Ollama os modelos que não voltam (Granite, phi4-mini, os três 1.5b agora; os dois Coder depois das corridas 1 e 2); `git add -f` dos dois logs; commit do working tree.

## 3. Sonda de detecção de correção (28/09/2026)

O que foi testado: os casos `efe-3` e `efe-10` tiveram o sintoma corrigido (achado 4.36) e foram apresentados de novo ao `qwen2.5:7b`, lendo uma cópia da própria biblioteca L1 (que contém a retificação e o verbete `interface-frontend` escritos a partir do `efe-10` antigo), numa época de aprendizado só com esses dois casos. Resultado (registro em `resultados_alvo/fase3b_correcao/`: `sonda.log`, `qwen2.5_7b/diagnosticos__L1.jsonl`, `qwen2.5_7b/propostas__E2.jsonl`, `bibliotecas/qwen2.5_7b/epoca-2`, hash 1202f1be9a75):

| Caso corrigido | Diagnóstico | O que o modelo propôs | Decisão do validador |
|---|---|---|---|
| `efe-3` (cartão sem foto) | `campo_ausente`, campo `imagem` — **correto** | Retificação em `contrato-produto` repetindo a sugestão da época 1 ("preco Decimal", formatação no front) e nota em `campo_ausente` idêntica à da época 1 | Ambas rejeitadas: `teto_notas_verbete` (858 > 800 caracteres) e `duplicada` |
| `efe-10` (tela com preço antigo, API já com o novo) | `dado_desatualizado` — **errado** (gabarito `estado_da_tela_divergente`, que estava no contexto) | A mesma retificação da época 1 sobre "cancelar depende do redirect" e um verbete novo genérico `atualizacao-da-interface` ("manter a interface atualizada com a API") | Retificação rejeitada (`teto_notas_verbete`, 908 > 800); verbete novo **aceito** (forma válida, conteúdo vazio) |

Leitura: com o prompt pré-registrado da Fase 3, o modelo não percebe que a documentação que ele mesmo escreveu ficou desatualizada — repete as edições antigas e só os tetos do validador impedem a biblioteca de acumular o mesmo texto de novo; nada foi registrado como "erro + solução sugerida + solução aplicada". A recuperação por palavras não trouxe as notas ligadas ao caso (`[E1 · efe-10 · …]`), e o prompt não pede ao modelo que compare o caso novo com o que a biblioteca afirma. Consequências para o desenho da Fase 4 estão em §4.2 (decisão 58). Observação: o `efe-10` corrigido é um caso mais difícil que o antigo — a distinção entre tela não redesenhada e dado desatualizado é exatamente o que ele testa.

## 4. Fase 4 — esqueleto do plano (para o Eric arquitetar)

### 4.1 O que a Fase 4 entrega (objetivos específicos 3 e 4 do projeto ABNT)
- **Interceptador Playwright**: captura das requisições e respostas da CobaiaAPI e da árvore de acessibilidade da página, com poda em código (decisão 55: poda da árvore, não do DOM bruto).
- **Diagnóstico em produção**: `qwen2.5:7b` com a biblioteca L1 curada, prompt congelado byte a byte, saída restrita por gramática (enum de causas), recuperação híbrida BM25 + embedding pequeno, cache exato só fora de corrida medida.
- **Cura de seletor**: candidatos gerados a partir da árvore de acessibilidade e verificados em código antes de reexecutar; a correção é aplicada na reexecução de verificação e apresentada ao desenvolvedor como sugestão (ABNT §2.1).

### 4.2 Requisito novo: ciclo de correção na biblioteca (Eric, 28/09/2026)
Quando um erro documentado pelo agente (na biblioteca, com solução sugerida) é corrigido no sistema — com a sugestão dele ou não —, o agente deve perceber a mudança e registrar na documentação que aquilo foi corrigido, **sem apagar o histórico**: o verbete passa a guardar o erro, a solução sugerida e a solução aplicada. O que isso pede ao harness da Fase 4 (arquivos novos; `evolucao_biblioteca.py` continua congelado para a Fase 3):
1. um campo de estado por verbete de defeito (`status: nao_corrigido | corrigido`) e uma operação nova de edição, "correção", que acrescenta as seções *solução sugerida* e *solução aplicada* com data, sem remover texto;
2. um gatilho: o caso reapresentado ou a inspeção do código mostra que o sintoma documentado não ocorre mais — a sonda de 28/09 mede se o modelo percebe isso sozinho com o prompt atual (§3);
3. recuperação por identificador: as notas do modelo já carregam o id do caso (`[E1 · efe-10 · …]`); ao corrigir um caso, o harness pode trazer ao contexto exatamente as notas ligadas a ele, em vez de depender da busca por palavras;
4. validação em código da correção (o trecho apontado existe; o status só avança; nada é removido) e o mesmo registro "o quê + motivo" das outras operações.

### 4.3 O que já está decidido para a Fase 4
Decisão 55 (mapa do levantamento das LLMs locais, §6.12.10 e §7.9): adotado, adiado e descartado, item a item; decisão 52 (modelo e biblioteca); pendências 2 (curadoria da cópia L1) e 11(f) (recuperador híbrido) do bloco de 23/09.

## 5. Fase 5 — o que já está escrito
Protocolo do projeto ABNT §3.4: MTTR (detecção → correção validada na reexecução) e Task Success (fluxo restaurado / cenários injetados), linha de base manual cronometrada, cerca de dez cenários com cinco repetições, banco restaurado entre execuções, navegador fixo pelo orquestrador, nas duas cobaias.

## 6. Documentação e entrega
1. Aplicar as 11 modificações do projeto ABNT que o Eric aprovar (`correcoes-aplicadas.md` §5.1) e resolver a autoria de MACIAK.
2. Remover as marcações de IA e regerar o PDF na entrega; conferir Faceli no exemplar.
3. TCC final: o Memorial é a matéria-prima (relatórios por fase, análise decisória, achados, referências); o dashboard serve às figuras e às tabelas.
4. Defesa.

## 7. Pontos do Eric a encaixar (28/09/2026)

Cada ponto novo entra numa linha desta tabela, na fase em que cabe; os já conhecidos estão listados.

| Ponto | Fase | Depende de | Esforço estimado |
|---|---|---|---|
| Curadoria da cópia L1 (30 edições restantes; 12 já marcadas erradas) | antes da 4 | pendência 2 | 1 sessão (IA) + conferência do Eric |
| Ciclo de correção na biblioteca (§4.2) | 4 | sonda de 28/09 | desenho + implementação em arquivos novos |
| Recuperador híbrido BM25 + embedding pequeno com reordenação (decisão 55) | 4 | — | 1 sessão + medição no i5 |
| Saída restrita por gramática com enum de causas (decisão 55) | 4 | medir custo no i5 | 1 sessão |
| Fichamento formal das 7 referências (pendência 11a) | documentação | decisão do Eric | — |
| Validação em Linux do instalador (pendência 11b) | documentação | decisão do Eric | — |
| Ablação base × instruct (pendência 11d) | só se a banca pedir | — | — |
