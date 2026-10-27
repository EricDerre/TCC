<!-- ! Alteração de IA - Revisar: em 26/10/2026 o arquivo `plano-fase-4.md` passou a ser este `plano-aprovado-fase-4.md`, com a linha de estado trocada pelo cabeçalho de aprovação (data, decisões 79 e 80 e a resposta de cada ficha); o texto do plano não foi reescrito, e o comentário original logo abaixo fica como registro de quando ele era proposta.
     ! Motivo: o Eric aprovou o plano como está e respondeu as fichas 26 a 36 uma a uma no quadro da sessão; o próprio plano (seção 5, pacote P0) manda copiá-lo para este nome com as respostas no cabeçalho, e a ficha 29 saiu diferente da recomendação, o que precisa estar visível antes do texto que assumia a recomendação. -->
<!-- ! Alteração de IA - Revisar: arquivo novo (26/10/2026) com o plano da Fase 4 (o agente na tela), escrito para a aprovação do Eric a partir do roadmap §4 e §4.5, do relatório da Pré-Fase 4 (seção 5), da especificação da trilha (versão 1), das decisões 52 a 78 e da leitura do harness e das duas cobaias; nenhum código do agente foi escrito.
     ! Motivo: a Pré-Fase 4 fechou em 26/10/2026 e o roadmap §4 era só um esqueleto; o Eric aprova o plano antes de qualquer código, e as escolhas que são dele estão nas fichas 26 a 36 de `Documentacao/memorial/pendencias.md`. Este arquivo vira `plano-aprovado-fase-4.md` só depois do sim dele; os números citados vêm dos documentos e dos JSON indicados em cada trecho (bloco ou campo), e as contagens de casos foram feitas por script sobre os bancos de casos em 26/10/2026. -->

**Aprovado pelo Eric em 26/10/2026, como está (decisão 79).** As fichas 26 a 36 de [pendencias.md](../Documentacao/memorial/pendencias.md) foram respondidas no mesmo dia, uma a uma no quadro da sessão: 26 (a), 27 (a), 28 (a), 30 (a), 31 (a), 32 (a), 33 (a), 34 (a), 35 (a) e 36 (a), todas pela recomendação; a 29 saiu pela opção (c), as duas formas de quebra de localizador (decisão 80). Onde o texto abaixo assume a recomendação da ficha 29 (quebra só pelo harness, "front intocado"), vale a decisão 80: o harness arma a quebra no navegador e o front PHP legado ganha também uma variante de quebra ligada só por parâmetro de URL ou cookie (sem ele, o front se comporta como hoje), e o relatório da fase compara as duas. O texto não é reescrito; os desvios durante a execução vão para o livro-razão e, no fechamento, para um anexo ao fim deste arquivo.

> Estado em 26/10/2026: aprovado; execução por começar pelo pacote P0 (seção 5). Livro-razão em `.superpowers/sdd/fase-4/progress.md` e restrições em `.superpowers/sdd/fase-4/constraints.md` (fora do git).

# Plano da Fase 4: o agente na tela

Data: 26/10/2026 · Máquina: i5-1235U (10 núcleos, 12 threads), 16 GB instalados (15,69 visíveis ao Windows; 4,0 GB livres com a sessão aberta em 26/10), NVMe com 218 GB livres, sem GPU utilizável, Ollama 0.40.2 (conferido em 26/10; última ponte de versão na corrida 14, em 0.40.2), Python 3.14.7, Edge 156.0.4314.42 instalado, Playwright não instalado (a venv do AgenteCore só tem o matplotlib; `%LOCALAPPDATA%\ms-playwright` não existe) · Repositório: `C:\Users\Eric.Derre\Documents\TCC` (`main`; working tree com o fechamento da Pré-Fase 4, ainda sem commit).

Notação: `RAIZ` = repositório; `EXP` = `RAIZ\Programacao\AgenteCore\experimentos`; `RA` = `EXP\resultados_alvo`; `API` = `RAIZ\Programacao\CobaiaAPI`; `FRONT` = `RAIZ\Programacao\CobaiaFront`; `DOC` = `RAIZ\Documentacao\memorial`; `FER` = `RAIZ\ferramentas`; `SDD` = `RAIZ\.superpowers\sdd\fase-4` (pasta nova, fora do git); `ESPEC` = `DOC\5-metodo-e-ferramental\especificacao-trilha-e-relatorio.md`.

## 1. Contexto

### 1.1 O que a Fase 4 entrega

A Fase 4 é a do agente na tela: o `qwen2.5:7b` com a biblioteca L1 curada deixa de ler casos escritos à mão e passa a diagnosticar o que o navegador vê. Pelo projeto ABNT (§3, terceiro e quarto objetivos específicos), ela implementa a filtragem de contexto, a interceptação de rede e a autocura de localizadores; pelo roadmap §4.1, o interceptador Playwright com poda da árvore de acessibilidade, o diagnóstico em produção, a cura de seletor com candidatos verificados em código e, pelo §4.2, o ciclo de correção na biblioteca. Pela Pré-Fase 4 (roadmap §4.5; relatório da fase, seção 5), tudo isso emite a trilha de raciocínio aberta e o relatório por caso da especificação aprovada (decisão 77).

Sai desta fase: o agente rodando ponta a ponta nas duas cobaias; a medida de quanto o diagnóstico na tela reproduz o diagnóstico em texto; a taxa de cura de seletor verificada; o ciclo de correção medido em código; a trilha e o relatório por caso avaliados contra o gabarito; e tudo o que a Fase 5 precisa para medir MTTR e Task Success (roteiros, cronômetros, restauração do banco, navegador fixo, protocolo da linha de base manual).

### 1.2 O que já está decidido (não se rediscute aqui)

| Tema | Decisão | Onde |
|---|---|---|
| Modelo e biblioteca | `qwen2.5:7b` com a L1 curada (`Programacao/AgenteCore/biblioteca_producao/`, hash `1fca10f1a6f6`), só por acréscimo validado em código; o padrão é o modelo com a biblioteca que ele mesmo escreveu | decisões 52, 69, 71, 73 |
| Busca | BM25 com sinais em código; sem busca híbrida; sem Brainiac; k = 5 é candidato a medir | decisão 61; relatório da Pré-Fase 4 §5 |
| Trilha e relatório | especificação versão 1: JSONL por corrida com cabeçalho, três camadas por nó, nó de decisão com alternativas, evidência, contraste, divergência obrigatória, probabilidade do rótulo e justificativa por molde; conferências em código; intervenção só por gatilho ou amostra; relatório em ordem fixa; nenhuma segunda chamada ao modelo para explicar, localizar erro ou julgar a trilha | decisão 77; `ESPEC` |
| Saída do modelo | sem gramática: as quatro linhas (CAUSA_RAIZ, CAMPO, IMPACTO, FONTE) conferidas em código e a probabilidade lida no token do rótulo | decisão 78 |
| Probabilidade do rótulo | triagem, não barreira: selo, gatilho de intervenção e de revisão humana; limiar pela curva risco-cobertura nos 90 casos antes da primeira corrida | corrida 12; `ESPEC` seções 6.3 e 14 |
| Ferramental das LLMs locais | mapa da decisão 55, com as ressalvas das decisões 61 e 78: poda em código, verificação por código dos rótulos e dos candidatos de seletor, cache de prefixo com prompt em ordem fixa, teto de tokens de saída, Q4_K_M, cache exato só fora de corrida medida (decisão 48) | decisão 55; `ferramental-das-llms-locais.md` §7.9 |
| Filtros da documentação autogerida | os 13 filtros que rodam em código entram; a segunda chamada ao modelo só depois de medir o custo | decisão 65; ficha 16 |
| Ciclo de correção | estado por verbete, operação "correção" que acrescenta solução sugerida e solução aplicada sem apagar, gatilho, recuperação pelo id do caso, validação em código | decisão 58; roadmap §4.2; ficha 14 |
| Navegador | o Chromium que o próprio Playwright baixa e fixa, headless | README, "Navegador recomendado para o agente" |
| Escopo da cura | diagnóstico e cura de localizador aplicada na reexecução de verificação e apresentada como sugestão; nenhum patch no código da aplicação-alvo | projeto ABNT §2.1 |
| Medição | ponte de versão antes de toda medição comparável (b + c até 2 nos 36); um modelo residente por vez; só CPU; `num_ctx` 8192; temperatura 0,1; variação entre corridas iguais de 0 a 3 casos em 36 | decisões 44, 47, 69; relatório da 3-B §3 |
| Fora | colibri como motor (decisão 75); modo thinking, raciocínio em cadeia, MCP, servidor Playwright MCP, ensembles, self-consistency, troca de modelo (decisão 55); atenção ou ativações ao vivo e segundo modelo residente (mapa da onda 2) | decisões 55 e 75; relatório da Pré-Fase 4 §5 |

### 1.3 O que a leitura das cobaias e do harness mostrou em 26/10/2026 (só leitura)

**Cobaias.** O front PHP legado sobe em `localhost:8080` (`php -S`, por `run.py`) e a CobaiaAPI em `localhost:8000` (uvicorn, sem `--reload`); o MariaDB fica em 3306 (`root` sem senha, schema `ti93phpdb01`), subido por `_env_common.ensure_mariadb_running`. A única página que consome a API é `FRONT\produtos_api.php`: `fetch` de `GET /api/produtos` ao carregar e de `GET /api/produtos/{id}` no clique em `button.saiba-mais[data-id]`; o resto do front lê o banco por `mysqli`. As rotas de pedido (`/api/pedidos`) não são chamadas por página nenhuma. O contrato de produto no fio é `id, nome, resumo, tipo, preco, imagem, destaque` (esquema `ProdutoOut` em `API\app\schemas.py`). A injeção de falhas tem sete modos em `API\app\fault_injection.py` (`normal`, `error_500`, `latency`, `type_drift`, `field_missing`, `field_renamed`, `malformed_json`), escolhidos pelo ambiente no boot ou por `POST /api/admin/fault-mode` com o cabeçalho `X-Admin-Token`, com `target_field` e `probability` por item. Não existe script de restauração do banco (o `install.py` só reaplica os três `.sql` de forma idempotente), nenhum roteiro E2E, nenhum código de Playwright, nenhuma captura de árvore de acessibilidade e nenhum mecanismo de quebra de localizador. Os elementos do front não têm `data-testid`; só `.saiba-mais`, `.delete` e `.cancela` têm `data-id`; cartões e tabelas só têm classes do Bootstrap. O formulário de contato (`rodape.php`) envia e-mail de verdade por SMTP; `*_excluir.php` e `cliente_cancelar.php` são GET destrutivos sem sessão; as páginas carregam jQuery e AngularJS de CDN.

**Os casos e a tela.** Contagem por script em 26/10/2026 sobre `banco_casos.py`, `banco_casos_extra.py`, `banco_casos_ineditos.py` e `RA\fase3\particao.json`: os sete modos atuais produzem 6 das 23 causas (`erro_interno_do_servidor`, `tempo_de_resposta_excedido`, `tipo_divergente`, `campo_ausente`, `campo_renomeado`, `resposta_truncada`; mapa em `base_conhecimento\falhas_injetadas\modos-de-injecao.md`). Têm uma dessas causas 11 dos 36 casos de avaliação, 9 dos 36 inéditos (20 dos 72) e 15 dos 54 de aprendizado; nenhuma causa das classes tradução e efeito (fora o `efe-3`) sai de um modo atual. É a ficha 28.

**Harness.** O que a Fase 4 reaproveita existe e tem nome: `cliente_ollama.gerar` (8 chaves, `num_gpu=0`, `num_ctx=8192`, temperatura 0,1) e o gancho `sondar_logprobs.com_logprobs` (troca `_post` e acrescenta `logprobs` e `top_logprobs` sem mudar as 37 chaves do registro); `recuperacao.Indice`, `sinais_do_caso`, `sinais_deterministicos`, `pontuar`, `recuperar` (a função `contexto` exige gabarito, então o caso ao vivo precisa de uma irmã dela); `estrategias.linear_com_biblioteca` (o prompt congelado, que já tem os blocos "ÁRVORE DE ACESSIBILIDADE DA PÁGINA" e "SELETOR QUE FALHOU" quando a entrada os traz); `avaliar.extrair`; `biblioteca.carregar/render/notas/validar`; `evolucao_biblioteca.validar_proposta` (30 códigos de rejeição), `aplicar_edicao`, `hash_biblioteca`, `fechar_snapshot` (importados; o arquivo não muda); `trilha.py` (esquema v1, `localizar_declaracoes`, `verificar` com 11 regras, das quais 8 sem gabarito) e `gerar_relatorio_raciocinio.py`; `analisar_confianca` (probabilidade conjunta, AUROC com intervalo, curva risco-cobertura); `executar_fase3b._com_modelo_descarregado`, `_preparar_copia`, `_gravar_condicoes`; `caminhos.fase3(nome)`; o molde dos `.ps1` (BOM, testes antes, espera de RAM, linha FIM com duração). Lacunas: `trilha.verificar` exige `registro["gabarito"]`; `adaptar_corrida` só remonta corridas gravadas; a origem `ao_vivo` existe no esquema e nunca foi emitida.

## 2. Princípios que valem para o plano todo

1. **Três camadas que nunca se misturam** (plano da Pré-Fase 4; `ESPEC` seção 4.1): o que o programa fez, o que o modelo declarou, o que o código conferiu. O relatório para humanos sai por script da trilha, sem segunda chamada a modelo. O gabarito aparece numa seção só, por último.
2. **Uma inferência por caso.** Cada chamada extra custa de 47 a 78 s nesta CPU (`ESPEC` seção 1); intervenção, atribuição por remoção e sonda de pós-racionalização só por gatilho ou na amostra fixa dos 36 casos de avaliação.
3. **O prompt do diagnóstico continua congelado byte a byte** enquanto a ficha 34 não disser o contrário: é o que mantém a Fase 4 comparável com as Fases 2-A a 3-B (projeto ABNT §3.4, "comparabilidade entre etapas"). O que muda é só o conteúdo dos blocos variáveis (caso, árvore, seletor, verbetes), que agora vem da tela.
4. **Tudo verificado em código antes de virar ação**: rótulo dentro das 23 causas, candidato de seletor que resolve para exatamente um elemento, acréscimo à biblioteca que passa pelos validadores, correção que só avança o estado e nunca apaga.
5. **O gabarito não entra no agente.** Na tela o agente não sabe a resposta; a avaliação é um passo à parte, sobre a trilha gravada. Toda regra de aceitação e todo limiar são fixados antes da corrida que os usa.
6. **Ponte de versão antes de toda medição.** O Ollama se atualiza sozinho; cada noite medida começa conferindo a versão e, se ela mudou desde a última ponte registrada, roda L0 nos 36 antes de qualquer outra coisa (decisão 47).
7. **Os arquivos congelados não mudam**: `executar_fase3.py`, `estrategias.py`, `evolucao_biblioteca.py`, `base_conhecimento\`, os registros de `RA\fase3\`, `RA\fase3b_*` e `RA\pre_fase4_confianca\`. O front PHP legado continua intocado (decisão de arquitetura registrada na memória do projeto); a CobaiaAPI é do grupo e pode ganhar modos novos (ficha 28).
8. **Primeiro a máquina, depois o modelo** (decisão 50): poda, diff, candidatos de seletor, molde de justificativa, gatilho de correção e toda avaliação rodam em código.

## 3. Arquitetura em módulos

### 3.1 O fluxo de um caso na tela

1. **Preparação**: o banco é restaurado ao seed; o modo de falha do cenário é ligado na CobaiaAPI (`POST /api/admin/fault-mode` com o token de `API\app\config.py`, `target_field` quando o modo é de campo, `probability` 1,0); a quebra de localizador do cenário, se houver, é armada (ficha 29); o Chromium do Playwright sobe headless com a versão gravada no cabeçalho da trilha (evento `corrida`).
2. **Roteiro**: o agente executa os passos do cenário (abrir página, esperar, clicar, conferir), escutando toda requisição e resposta a `localhost:8000` e capturando a árvore de acessibilidade depois de cada passo. Dependências externas das páginas (jQuery, AngularJS, slick, FontAwesome, mapa) são servidas de um arquivo HAR gravado uma vez em `EXP\fixtures_fase4\`, e qualquer outro host é bloqueado e registrado como incidente: a medição não depende da rede, e o formulário de contato nunca é enviado.
3. **Falha**: quando uma conferência do roteiro falha ou um localizador não resolve, o interceptador entrega o que capturou e a poda reduz a árvore e o corpo HTTP ao que interessa (seção 3.3). O caso ao vivo é montado no mesmo formato dos casos gravados (seção 3.4), e o momento da detecção é marcado (início do cronômetro do MTTR).
4. **Diagnóstico**: busca BM25 com sinais sobre a L1 curada, prompt congelado, uma inferência com `logprobs`, quatro linhas conferidas em código, probabilidade do rótulo, nó de decisão com alternativas, contraste, divergência, selo e justificativa por molde; gatilhos de intervenção e de revisão humana conforme as fichas 26 e 31.
5. **Cura e reexecução**: se a falha foi de localizador, os candidatos são gerados da árvore podada e verificados em código; o primeiro que passa é aplicado numa reexecução de verificação; o roteiro passando é o fim do cronômetro e o critério de Task Success. Se a falha foi de contrato, o que a reexecução valida depende da ficha 35.
6. **Biblioteca**: fora do conjunto de avaliação, o agente pode propor um acréscimo (uma inferência a mais), que passa pelos validadores da Fase 3 e pelos filtros da decisão 65, fica em espera e só entra depois da reavaliação do lote nos 36 inéditos; o ciclo de correção roda em código quando um cenário ligado a um verbete volta a passar.
7. **Relatório**: o relatório do caso sai da trilha, em ordem fixa (`ESPEC` seção 11), com o comando copiável para reexecutar o caso; o painel lê os derivados.

### 3.2 Os módulos

| Módulo | Arquivo | Novo ou reaproveitado | O que faz | Eventos da trilha |
|---|---|---|---|---|
| Navegador e roteiros | `EXP\navegador.py` | novo (Playwright, único pacote externo novo) | abre o Chromium fixo do Playwright em modo headless; roda um roteiro passo a passo; grava o trace só quando um passo falha (retain-on-failure) e o anexa como evidência do nó que falhou; registra a versão do Playwright e do navegador no cabeçalho | `corrida`, `acao`, `blob` (trace) |
| Interceptador | `EXP\interceptador.py` | novo | escuta requisições e respostas a `localhost:8000` (método, caminho, status, cabeçalhos escolhidos, tempo, corpo com hash SHA-256 gravado uma vez); captura a árvore de acessibilidade da página (snapshot ARIA do Playwright, conferido no P0 contra a versão instalada) depois de cada passo e na falha; monta em código a aresta "chamada HTTP" entre a página PHP e a rota FastAPI (`ESPEC` seção 3.3) | `interceptacao`, `blob` |
| Poda | `EXP\poda.py` | novo (funções puras) | reduz a árvore ao que o roteiro toca e ao entorno (papéis interativos, textos, estados), com contagens antes e depois e as regras aplicadas; reduz o corpo HTTP ao diff contra o contrato esperado e ao trecho em disputa (diretriz da Fase 2 em `EXP\RESULTADO_FASE2.md`: diff em código, não JSON cru); orçamento em caracteres por token (2,6, `biblioteca.CHARS_POR_TOKEN`) para o prompt caber em `num_ctx` 8192 sem o Ollama descartar o começo em silêncio | `poda`, `decisao` (poda) |
| Caso ao vivo | `EXP\caso_ao_vivo.py` | novo | monta `entrada` no formato dos casos gravados (`requisicao`, `status`, `contrato`, `corpo`, `sintoma`, `observacao`, `arvore`, `seletor_quebrado`); o contrato esperado vem do `openapi.json` da CobaiaAPI convertido para a forma textual dos fixtures (fixada no P2 lendo `banco_casos.py`); o sintoma sai de um molde em código a partir da conferência do roteiro que falhou e do diff contra a corrida de referência em modo `normal`; sem gabarito | `entrada`, `decisao` (montagem_do_prompt) |
| Recuperação | `EXP\recuperacao.py` (como está) e `contexto_ao_vivo` em `diagnostico_ao_vivo.py` | reaproveitado mais uma função nova | BM25 com sinais em código (`sinais_do_caso`, `sinais_deterministicos`, `pontuar`), k da ficha 30; a função nova repete o ramo A2 de `recuperacao.contexto` sem pedir gabarito; recuperação pelo id do caso para as notas `[E<n> · <caso> · …]` (ficha 32 e ciclo de correção) | `candidatos`, `decisao` (recuperacao) |
| Diagnóstico | `EXP\diagnostico_ao_vivo.py` | novo; reaproveita `estrategias.linear_com_biblioteca`, `cliente_ollama.gerar` com `sondar_logprobs.com_logprobs`, `avaliar.extrair`, `trilha.localizar_declaracoes`, `trilha.verificar` (passa a aceitar registro sem gabarito), `analisar_confianca.probabilidade_conjunta` | uma inferência por caso; conferências da `ESPEC` seção 5 (as 8 sem gabarito do protótipo mais `fonte_formato_valido` e `fonte_contem_termo_da_causa`); probabilidade lida no primeiro token depois de `CAUSA_RAIZ:`; selo pelos limiares da ficha 31; nó de decisão com as alternativas do `top_logprobs`, contraste e divergência; justificativa por molde (`ESPEC` seção 7); gatilhos de intervenção (`ESPEC` seção 6.1) | `prompt`, `inferencia`, `declaracao`, `verificacao`, `decisao` (diagnostico), `intervencao` |
| Cura de seletor | `EXP\cura_seletor.py` | novo, sem modelo | gera candidatos a partir da árvore podada e do alvo registrado na corrida de referência (papel e nome; texto normalizado; `data-id`; caminho a partir de ancestrais com id, como `#produtos-api-grid`; posição entre irmãos), numa ordem fixa; verifica cada um em código (resolve para exatamente um elemento, visível, mesmo papel do alvo, nome parecido acima de um limiar fixado no P4, e o efeito esperado do passo na reexecução); aplica só na reexecução de verificação; apresenta como sugestão no relatório | `cura`, `decisao` (cura), `acao`, `decisao` (reexecucao) |
| Biblioteca em produção | `EXP\biblioteca_fase4.py` | novo; reaproveita `biblioteca.*`, `evolucao_biblioteca.validar_proposta`, `aplicar_edicao`, `hash_biblioteca`, `fechar_snapshot` (importados) e `curar_biblioteca` | acréscimo validado: validador da Fase 3 mais os 13 filtros em código da decisão 65 (evidência obrigatória com TRECHO e id do caso; alegações curtas amarradas a trecho; abstenção "NENHUMA" válida; nomes de arquivo, endpoint e mensagem conferidos contra o `openapi.json` e o código; sinalizar ou retificar; peso por tipo de edição; redundância por n-gramas; proveniência por edição; auditoria de admissão e de atualização separadas; resolução determinística de conflito; métricas por rodada; revisão humana amostral); origem de cada verbete (humano, modelo, sistema sob teste); estado por verbete (`nao_corrigido`, `corrigido`) e operação "correção" que acrescenta "Solução sugerida" e "Solução aplicada" com data, sem remover texto; regra nova de admissão: nota em verbete presente em 40% ou mais dos contextos da calibração vai para revisão humana antes de entrar (o `contrato-produto` estava em 15 dos 36 contextos, achado 4.42); lote só aceito depois da reavaliação nos 36 inéditos; nenhum texto vindo de resposta HTTP entra sem validação (`ESPEC` seção 10) | `edicao_biblioteca`, `decisao` (edicao_biblioteca) |
| Trilha v2 | `EXP\trilha.py` | estendido (protótipo da Pré-Fase 4; continua lendo v1) | cabeçalho de corrida (modelo, quantização, versão do Ollama, `top_logprobs` e modo de leitura, `num_ctx`, temperatura, hash da L1, do prompt fixo e do índice BM25, versão do Playwright e do navegador, início e fim, limites declarados); tipos novos (`interceptacao`, `poda`, `decisao`, `intervencao`, `cura`, `edicao_biblioteca`, `incidente`, `revisao`); origem `ao_vivo` com `ts`; nó de decisão com os campos da `ESPEC` seção 4.2 e arestas PROV; taxonomia de falhas (`ESPEC` seção 8); diff determinístico contra a trilha de referência (`ESPEC` seção 9) | todos |
| Relatório por caso | `EXP\gerar_relatorio_raciocinio.py` | estendido | ordem fixa da `ESPEC` seção 11: veredito com selo e carimbo de conflito; evidência lado a lado (campo do contrato e trecho podado da resposta, com hash); contraste; FONTE conferida; linha de ação com o comando de reexecução; árvore completa recolhida; avaliação por último | |
| Cenários e cronômetros | `EXP\cenarios_fase4.py` | novo | catálogo dos roteiros nas duas cobaias (ficha 36), modo de falha e quebra de localizador por cenário, restauração do banco entre execuções, cronômetro do MTTR (detecção até reexecução validada) e critério de Task Success (fluxo restaurado e roteiro concluído sem erro) | `corrida`, `acao` |
| Orquestrador | `EXP\executar_fase4.py` e `EXP\rodar_fase4.ps1` | novos, no molde de `executar_fase3b.py` e `rodar_fase3b.ps1` | modos `ponte`, `calibracao`, `reproducao`, `tela`, `cura`, `biblioteca`, `cenarios`, `avaliacao_trilha`; sobe as cobaias por `run.start_services` e `wait_until_ready`; ponte de versão automática; `condicoes_fase4.json` por corrida; toda saída em `caminhos.fase3("fase4_<modo>")` | |
| Avaliação | `EXP\avaliar_fase4.py` (`--check`, `--colar`) e `EXP\fase4.py` (irmão de `pre_fase4.py`) | novos | reprodutibilidade na tela, acerto e concordância tela × texto, taxa de cura por tipo de quebra, precisão do ciclo de correção, MTTR e Task Success do ensaio, tamanho da trilha e do trace; blocos `tb_f4_*` para o relatório e o painel | |
| Restauração do banco | `RAIZ\restaurar_banco.py` | novo | recria `ti93phpdb01` a partir dos três `.sql` de `FRONT\banco\` (`DROP DATABASE IF EXISTS` e `apply_sql_files` do `install.py`), com `ensure_mariadb_running` | |
| Modos de injeção novos | `API\app\fault_injection.py` e `API\tests\test_fault_injection.py` | alterados conforme a ficha 28 | um modo por causa que a tela consegue mostrar | |
| Painel | `FER\painel_fase4.py` e o grupo novo em `painel_topicos.NAV` | novo | aba "Fase 4: o agente na tela" (pergunta, resposta, números-chave, gráficos, leitura, tabelas recolhidas, fontes) e "Cérebro ao vivo" (só o que a inferência devolve: probabilidade do rótulo, as 20 alternativas, margem, tempos, verbetes recuperados e a árvore da trilha, com o Python regravando um HTML local a cada diagnóstico) | |
| Testes | `EXP\testar_fase4.py` e `EXP\fixtures_fase4\` | novos | tráfego, árvores e HAR gravados uma vez e congelados; Ollama de mentira (`testar_fase3._ollama_de_mentira`); hash das áreas só de leitura antes e depois | |

### 3.3 Poda em código

Duas podas, as duas com contagens antes e depois no evento `poda`:

- **Árvore de acessibilidade**: ficam os nós com papel interativo (botão, link, campo, caixa de seleção), os textos dentro do alvo do passo e dos irmãos imediatos, os estados (desabilitado, expandido, selecionado) e os marcos da página (navegação, principal, diálogo); saem decoração, repetição de cartões além dos três primeiros e dos que o roteiro toca, e atributos sem valor diagnóstico. A forma de saída é a mesma de `banco_casos.ARVORE_CARTOES` (papel, nome entre aspas, indentação), para o bloco "ÁRVORE DE ACESSIBILIDADE DA PÁGINA" do prompt congelado continuar igual.
- **Corpo HTTP**: o contrato esperado (campos e tipos do `openapi.json`) é comparado em código com o corpo recebido; o que vai ao prompt é o diff (campo ausente, renomeado, tipo diferente, valor fora do domínio, corpo não JSON, truncado) mais o trecho em disputa, com o corpo inteiro gravado uma vez por hash. É a mesma diretriz que o diff pré-calculado da Fase 2 já media.

A poda é controle de latência, não só economia de tokens (decisão 55): o prefill em CPU cresce mais que linearmente com o prompt. Regra fixada antes de rodar: o prompt ao vivo não pode passar o maior prompt da calibração em mais de 10%; se passar, a poda aperta antes da próxima corrida, nunca o prompt fixo.

### 3.4 O caso ao vivo e o sintoma por molde

Os casos gravados têm um sintoma escrito à mão ("cartão sem foto", "preço aparece como undefined"). Na tela, o sintoma sai de um molde em código, a partir de três fontes: a conferência do roteiro que falhou (o que se esperava e o que se viu, em texto gerado pelo próprio passo), o diff do corpo HTTP contra o contrato e o diff da árvore podada contra a corrida de referência do mesmo cenário em modo `normal` (a "trilha dourada" da `ESPEC` seção 9). O texto resultante é curto, determinístico e nunca usa o nome do modo de falha nem a causa: só o que a tela e o fio mostraram.

O que isso permite medir (P3): o mesmo caso, lido do fixture e lido da tela, recebe o mesmo rótulo? A regra de aceitação está na seção 5 (R2).

### 3.5 Diagnóstico com a trilha v2

Por caso, o nó `diagnostico` registra: as 23 causas como alternativas com a probabilidade das que o `top_logprobs` devolveu; a escolha; a evidência (sinais em código, verbetes entregues) por `seq`; o contraste "esta e não a segunda", gerado por molde; a divergência entre o declarado e o medido (FONTE fora do contexto, causa sem verbete que a trate, campo ausente do caso); a confiança (`logprob_rotulo`, `p_rotulo`, margem para a segunda, entropia normalizada sobre as 20 alternativas, `selo`); a justificativa humanizada; e, quando disparada, a intervenção (remoção do verbete citado por marcador neutro, troca por verbete errado, inferência sem documentação), cada uma registrando a mudança de rótulo e a variação da probabilidade, com a inferência de base repetida nos casos de intervenção (risco 5 da especificação).

Leitura da probabilidade: no primeiro token do rótulo depois de `CAUSA_RAIZ:`, localizado por `trilha.localizar_declaracoes`, como `analisar_confianca.trecho_do_rotulo` já faz; a sondagem de `sondar_logprobs.py` (três chamadas) roda no começo de cada noite medida, porque o Ollama mudou de versão desde a última sondagem (0.34.4 em 01/10; 0.40.2 hoje).

### 3.6 Cura de seletor

Entrada: o passo que falhou (ação, localizador original, alvo registrado na corrida de referência: papel, nome, texto, atributos, caminho) e a árvore podada atual. Geração em código, ordem fixa de candidatos: (1) papel e nome iguais; (2) papel igual e nome parecido (texto normalizado, limiar fixado no P4 antes da corrida); (3) texto contido; (4) `data-id` igual; (5) caminho a partir do ancestral com id mais próximo; (6) posição entre irmãos do mesmo papel. Verificação em código, na ordem: resolve para exatamente um elemento; visível e habilitado; mesmo papel do alvo; nome parecido; o efeito esperado do passo acontece na reexecução (o modal abre, a tabela recarrega, a página muda). Só o primeiro candidato que passa é aplicado, e só na reexecução de verificação; o relatório mostra todos os candidatos com o resultado de cada verificação, e a cura "aplicada" é a que levou o roteiro ao fim (ABNT §2.1).

Quebra de localizador: o front não muda. A quebra é armada pelo harness no navegador (ficha 29), com modos determinísticos por cenário (renomear `id`, trocar classe, mudar o texto do botão, envolver o elemento num contêiner novo, reordenar irmãos), de modo que cada cenário quebra sempre do mesmo jeito.

### 3.7 Biblioteca em produção e ciclo de correção

A L1 curada é a biblioteca de partida e cresce só por acréscimo validado (seção 3.2, linha "Biblioteca em produção"). O ciclo de correção do roadmap §4.2 fica assim:

1. **Estado**: cada verbete de defeito ganha `status: nao_corrigido | corrigido` no frontmatter (`biblioteca.py` já lê `status` como campo obrigatório; o valor passa a ser controlado).
2. **Gatilho em código**: um verbete tem notas ligadas a casos pelo id (`[E1 · efe-10 · …]`); quando o cenário desse caso volta a passar com o modo de falha desligado (ou o caso reapresentado não produz mais o sintoma documentado), o código marca a correção, com a evidência (diff HTTP e diff da árvore entre a corrida que falhava e a que passou).
3. **Operação "correção"**: acrescenta ao verbete as seções "Solução sugerida" (o que o modelo tinha escrito, com data) e "Solução aplicada" (o que a evidência mostra, por molde em código, com data); nunca remove texto; a validação confere que o trecho apontado existe, que o estado só avança e que nada foi removido (`conferir_somente_acrescimo` continua valendo).
4. **Recuperação por id**: ao reapresentar um caso, as notas com o id dele entram no contexto sem depender da busca por palavras.
5. **Segunda chamada ao modelo**: só se a decisão 65 for revista depois de medir o custo; por padrão o texto da solução aplicada sai do molde.

O que isso mede (P5): o ciclo detecta as correções conhecidas (os modos desligados) sem marcar o que não foi corrigido, e a sonda de 28/09 repetida com recuperação por id muda o que o modelo propõe.

### 3.8 Relatório por caso e painel

O relatório segue a `ESPEC` seção 11 e marca a justificativa como "gerada por molde". O painel ganha o grupo "Fase 4" com duas abas, lidas de `RA\fase4\*.json`: a aba da fase (reprodutibilidade, acerto tela × texto, cura, ciclo de correção, MTTR e Task Success do ensaio, tamanho da trilha) e a aba "Cérebro ao vivo" (só o que a inferência devolve). O explorador de casos da Pré-Fase 4 passa a ler trilhas v2. Nada de atenção, ativações ou segundo modelo (mapa da onda 2).

### 3.9 O que a Fase 5 mede e o que a Fase 4 deixa pronto

A Fase 5 (roadmap §5; projeto ABNT §3.4) mede MTTR (detecção pelo agente até a correção validada na reexecução) e Task Success (cenários com fluxo restaurado e roteiro concluído sem erro, sobre os injetados), contra a linha de base manual cronometrada, em cerca de dez cenários com cinco repetições, nas duas cobaias, com banco restaurado entre execuções, modo de falha fixo por cenário e navegador fixo. A Fase 4 deixa pronto: o catálogo de cenários (ficha 36), `restaurar_banco.py`, o cronômetro e o critério no código (`cenarios_fase4.py`), a versão do navegador no cabeçalho, o ensaio de uma repetição por cenário (P6) e o protocolo escrito da linha de base manual (`DOC\5-metodo-e-ferramental\protocolo-linha-de-base-manual.md`: o que cada integrante vê, quando o cronômetro começa e termina, o que conta como "corrigido", a planilha).

## 4. Decisões do Eric: fichas 26 a 36

Cada uma é uma ficha em `pendencias.md`, com opções e recomendação; o plano assume a recomendação até a resposta, e o pacote que depende dela está indicado.

| Ficha | Decisão | Recomendação | Pacote |
|---|---|---|---|
| 26 | Os três sinais de revisão humana (probabilidade do rótulo; causa tratada por verbete do contexto; causa na classe que a rota aponta) como ordem de prioridade | a probabilidade manda; os dois sinais grátis só desempatam e viram aviso no relatório | P3 |
| 27 | O conjunto de avaliação: os 72 casos em texto mais quantos inéditos a mais, escritos por quem, conferidos por quem | 72 mais 36 inéditos novos (6 por classe), escritos por agente que lê só o código das cobaias e os modos da ficha 28, conferidos pelo Eric, antes da primeira corrida medida | P2 e P3 |
| 28 | Modos de injeção novos na CobaiaAPI, porque os sete atuais produzem 6 das 23 causas (20 dos 72 casos reproduzem na tela) | um modo por causa que a tela consegue mostrar, começando pelas classes sem nenhum modo (tradução e efeito) | P2 |
| 29 | Quebra de localizador armada pelo harness no navegador (front intocado) ou variante no PHP | pelo harness, com modos determinísticos por cenário | P4 |
| 30 | k da recuperação: 3 (como medido) ou 5 (hit@5 de 91,1% contra hit@3 de 80,0% nos 90, corrida 9) | medir os dois na calibração e decidir pela regra pré-registrada | P0 e P3 |
| 31 | Limiares do selo (alto, médio, baixo) e do gatilho pela curva risco-cobertura nos 90: que parcela vai para revisão humana | a parcela de 30% de menor probabilidade (na corrida 12, com a L1 curada, pega 7 dos 14 erros; 10% pega 4) | P3 |
| 32 | O lugar dos verbetes novos escritos pelo modelo, que a busca nunca entregou | ficam, ganham recuperação pelo id do caso e sinais de busca calculados em código; se continuarem sem recuperação na calibração, vão para uma pasta de espera | P5 |
| 33 | Tamanho da trilha e do trace: limites inline, trace só na falha, retenção | trace só na falha, 64 KB por blob inline, nós por diagnóstico e por cura limitados, retenção de seis meses, tudo medido na primeira corrida | P1 e P3 |
| 34 | O prompt do diagnóstico: congelado byte a byte na Fase 4 inteira, ou versão 2 com os itens adotados pela decisão 55 (few-shot fixo, forma dos rótulos) medida antes | congelado; os itens da decisão 55 viram um experimento em texto nos 90, sem entrar no agente desta fase | P0 e P3 |
| 35 | O que a cura cobre nas quebras de contrato: só o diagnóstico (MTTR até o diagnóstico conferido), ou também a adaptação da conferência do roteiro (campo renomeado, tipo) validada na reexecução | só localizador tem cura; nas quebras de contrato o resultado é o diagnóstico e o MTTR mede até ele, declarado assim na Fase 5 | P4 e P6 |
| 36 | Os cerca de dez cenários da Fase 5 e a linha de base manual (quem cronometra, quando) | 6 cenários de contrato em `produtos_api.php` (um por modo), 4 de localizador no front legado; linha de base por três integrantes, cada um nos dez cenários, numa sessão agendada | P6 |

## 5. Ordem de construção, TDD e o que cada etapa mede

Toda etapa segue o molde das fases anteriores: teste escrito e visto falhar pelo motivo certo antes do código (`testar_fase4.py`, funções `teste_<nome>()`, runner que termina em `N testes ok`, hash das áreas só de leitura no primeiro e no último teste); tag e motivo em todo trecho; nenhum número digitado à mão. Regras de aceitação fixadas antes da corrida que as usa:

- **R1 (reprodutibilidade)**: um caso "reproduz na tela" quando, com o modo e o campo do caso ligados, o roteiro falha no passo esperado e o caso ao vivo traz, no diff ou no sintoma por molde, o campo do gabarito (ou, nos casos sem campo, o status ou o sinal determinístico do gabarito). Conta em código, sem modelo.
- **R2 (a tela não piora)**: nos casos que reproduzem, o rótulo dado ao caso lido da tela e o rótulo dado ao caso lido do fixture, na mesma sessão do Ollama, diferem em no máximo 3 casos (a variação entre corridas iguais); acima disso, o molde do sintoma e a poda são revistos antes da próxima noite.
- **R3 (cura)**: uma cura só conta quando a conferência final do roteiro passa na reexecução; o relatório separa "mesmo elemento do alvo original" de "outro elemento que fez o roteiro passar".
- **R4 (ciclo de correção)**: precisão e revocação da marca `corrigido` contra o conjunto conhecido de modos desligados.
- **R5 (acréscimo)**: um lote de acréscimos entra se, na reavaliação nos 36 inéditos, o número de casos que passam a acertar for maior ou igual ao dos que passam a errar (b ≥ c); senão o lote fica em espera com o motivo.
- **R6 (ponte)**: toda noite medida começa conferindo a versão do Ollama contra `RA\fase4\pontes.json`; versão nova, L0 nos 36 antes de tudo; b + c até 2 contra a Fase 3 (decisão 47); o `.ps1` aborta se a versão mudar no meio (padrão da decisão 44).
- **R7 (limiares)**: os limiares do selo saem da curva risco-cobertura da calibração e ficam gravados em `RA\fase4\limiares.json` antes da primeira corrida na tela.
- **R8 (k)**: se a ficha 30 for (a), k = 5 entra só se acertar mais que k = 3 nos 90 por acurácia balanceada com b + c acima de 3; empate fica com k = 3, que é mais barato.

### P0. Aprovação, registro e ambiente (sessão 1; máquina por minutos)

1. Depois do sim: copiar este arquivo para `RAIZ\claude-memoria\plano-aprovado-fase-4.md` (cabeçalho com data e respostas das fichas), decisão nova em `decisoes.md` (a Fase 4 aberta, com o que cobre), roadmap §1 (Fase 4 "Em andamento") e §2 (corridas 16 a 22 desta seção, estado `aguarda`), `SDD\progress.md` e `SDD\constraints.md` (as regras da Pré-Fase 4 mais as desta fase: front intocado, hosts permitidos, formulário de contato nunca enviado).
2. Instalar o Playwright na venv do AgenteCore (`pip install playwright==<versão fixada>` e `python -m playwright install chromium`, sem administrador; `requirements.txt` atualizado com a versão e a tag). Registrar em `RA\fase4\ambiente.json` as versões do Python, do Playwright, do Chromium e do Ollama. Se a rede corporativa ou o antivírus bloquear o download do Chromium, parar, registrar como resultado e usar o canal `msedge` (Edge 156.0.4314.42) com a versão no cabeçalho de toda trilha; nunca desligar proteção.
3. Conferir com um roteiro mínimo (abrir `produtos_api.php`, esperar o grid) que a captura da árvore de acessibilidade funciona na versão instalada e gravar a primeira amostra em `EXP\fixtures_fase4\`.
4. Opcional e barato (decisão 55, threads e afinidade): varredura de `num_thread` em 6 prompts gravados; só entra se a geração ficar ao menos 20% mais rápida e os rótulos de L0 nos 36 não mudarem além de b + c = 2. Resultado registrado de qualquer forma.
- **Testes escritos antes**: `teste_ambiente_json_tem_as_quatro_versoes`, `teste_fixture_da_arvore_tem_papel_e_nome`, hash antes e depois das áreas só de leitura (`base_conhecimento`, `fase3`, `fase3b_*`, `pre_fase4_confianca`, `biblioteca_producao`).
- **Mede**: nada de resultado; só o ambiente.

### P1. Trilha v2 e relatório v2 (sessões 2 e 3; sem máquina)

- `trilha.py`: versão 2 do esquema (campo `v`), cabeçalho de corrida, limites declarados, tipos novos, nó de decisão com os campos da `ESPEC` seção 4.2, origem `ao_vivo` com `ts`, arestas `used`, `wasDerivedFrom`, `wasGeneratedBy`, taxonomia de falhas, `verificar` com gabarito opcional, `diff_contra_referencia` (primeiro nó divergente, casamento exato) e a tabela de exportação para nomes gen_ai (opcional, só nomes).
- `gerar_relatorio_raciocinio.py`: ordem fixa da seção 11; molde de justificativa (`justificativa_por_molde(no)`), com a frase fixa de incerteza abaixo do limiar; marca "gerada por molde".
- **Testes escritos antes**: um arquivo v1 lido por um leitor v2 sem perda; as três trilhas da vitrine regeradas byte a byte (`--vitrine --check` continua limpo); o molde nunca cita um verbete que não esteja na evidência do nó; o diff acha o primeiro nó divergente em trilhas sintéticas e tolera a variação declarada; todo valor declarado continua sendo trecho literal da resposta; nó sem divergência preenchida é rejeitado.
- **Mede**: nada na máquina; é o alicerce das corridas.

### P2. Interceptador, poda, caso ao vivo e cenários (sessões 3 a 5; navegador sem modelo)

- `navegador.py`, `interceptador.py`, `poda.py`, `caso_ao_vivo.py`, `cenarios_fase4.py` (os primeiros roteiros: catálogo pela API e detalhe no modal em `produtos_api.php`; busca, login do administrador, lista de produtos e reserva do cliente no front legado), `restaurar_banco.py`, o HAR das dependências externas, a lista de hosts permitidos, os modos novos da ficha 28 na CobaiaAPI com os testes de `API\tests\test_fault_injection.py`.
- Corridas de referência (modo `normal`) por cenário, gravadas como trilhas douradas.
- **Testes escritos antes** (sobre fixtures congelados, sem navegador): a poda da árvore preserva o alvo do passo e os papéis interativos e remove o resto, com as contagens certas; o diff do corpo contra o contrato acha campo ausente, renomeado, tipo diferente, corpo não JSON e truncado; o sintoma por molde é determinístico e não contém o nome do modo nem a causa; o caso ao vivo tem exatamente as chaves dos casos gravados; a aresta "chamada HTTP" liga `produtos_api.php` a `GET /api/produtos`; `restaurar_banco.py` deixa o seed (4 tipos, 14 produtos, 2 usuários, 0 reservas) a partir de um banco sujo; um teste de integração com as cobaias no ar, pulado com aviso quando as portas 8080, 8000 e 3306 não respondem; modos novos da API cobertos um a um.
- **Corrida 17 (reprodução; dia; sem modelo)**: os 72 casos de avaliação e inéditos com causa que um modo produz (20 hoje; mais com a ficha 28), cada um com o modo e o campo do caso ligados, roteiro rodado, caso ao vivo montado. `avaliar_fase4.py --reproducao` aplica a R1 e grava `RA\fase4\reproducibilidade.{json,md}` (por caso: reproduz ou não, motivo, tamanho da árvore antes e depois, do corpo, do caso ao vivo, tempo do cenário, tamanho do trace quando houve falha).
- **Mede**: quantos casos a tela reproduz, quanto custa um cenário (segundos) e quanto pesa a trilha, antes de gastar modelo.

### P3. Diagnóstico ao vivo (sessões 5 e 6; duas noites de máquina)

- `diagnostico_ao_vivo.py` (contexto sem gabarito, prompt congelado, gancho de `logprobs`, conferências, nó de decisão, selo, gatilhos), `executar_fase4.py --modo calibracao|tela`, `rodar_fase4.ps1`.
- **Noite A, corrida 16 (calibração e ponte; modo texto)**: `rodar_fase4.ps1 -Modo calibracao -Saida fase4_calibracao -K 3` (e `-K 3,5` se a ficha 30 for (a)). Ordem dentro da noite: sondagem dos `logprobs`; ponte de versão se a versão mudou (R6); L1 curada nos 90 casos com `logprobs`; `analisar_confianca.py` estendido aos 90 grava a curva risco-cobertura e `limiares.json` (R7). Antes da noite, nada da tela roda com modelo.
- **Noite B, corrida 18 (tela)**: `rodar_fase4.ps1 -Modo tela -Saida fase4_tela`: os casos que reproduzem (corrida 17) diagnosticados da tela e, na mesma sessão do Ollama, os mesmos casos lidos do fixture. `avaliar_fase4.py --tela` aplica a R2 e grava acerto, concordância, tempo por caso, distribuição da probabilidade e tamanho da trilha.
- **Testes escritos antes**: com Ollama de mentira, o registro de diagnóstico ao vivo tem as 37 chaves oficiais mais nada (o extra vai para a trilha); o prompt montado da tela é igual ao prompt montado do fixture quando `entrada` é igual (byte a byte); a probabilidade é lida no token certo em fluxos sintéticos (acento partido, `**CAUSA_RAIZ:**`, rótulo e quebra de linha no mesmo token, como em `testar_pre_fase4`); o selo segue `limiares.json`; os gatilhos disparam só nos casos previstos; a R2 é calculada contra um par sintético com b + c conhecido.
- **Mede**: acerto na tela contra o gabarito, concordância tela × texto, custo por caso ao vivo, AUROC da probabilidade nos 90 e os limiares.

### P4. Cura de seletor e reexecução (sessões 7 e 8; dia, sem modelo)

- `cura_seletor.py`, modos de quebra de localizador (ficha 29), reexecução de verificação, cronômetro do MTTR, `executar_fase4.py --modo cura`.
- **Testes escritos antes** (sobre árvores congeladas): cada estratégia de candidato gera o esperado numa árvore de exemplo; a verificação recusa candidato que resolve para dois elementos, para elemento invisível ou para outro papel; a ordem de aplicação é a fixa; o relatório lista todos os candidatos com o resultado; a quebra armada é determinística (o mesmo HTML, duas vezes, dá a mesma árvore).
- **Corrida 19 (cura; dia)**: `rodar_fase4.ps1 -Modo cura -Saida fase4_cura -Repeticoes 5`: 4 roteiros do front legado × 4 modos de quebra × 5 repetições (80 execuções, cerca de 40 min pela conta da seção 8). `avaliar_fase4.py --cura` aplica a R3 e grava taxa de cura por modo e roteiro, tempo da detecção à reexecução validada e os casos "outro elemento".
- **Mede**: a primeira medida de MTTR só do agente (sem linha de base), a taxa de cura e onde a geração em código falha.

### P5. Biblioteca em produção e ciclo de correção (sessões 8 a 10; uma noite)

- `biblioteca_fase4.py` (filtros da decisão 65, origem, estado, operação "correção", recuperação por id, revisão obrigatória, lote em espera), `executar_fase4.py --modo biblioteca`, `sonda_correcao.py` chamado de novo com a recuperação por id ligada.
- **Testes escritos antes**: cada filtro em código recusa o exemplo mínimo que o motiva e aceita o contraexemplo; a operação "correção" nunca remove bytes e só avança o estado; o gatilho marca `corrigido` só com a evidência dos dois diffs; a recuperação por id traz as notas do caso e nada mais; a regra dos 40% manda para revisão a nota do verbete mais recuperado da calibração; um lote com c > b fica em espera; nenhum texto de corpo HTTP entra em proposta sem validação.
- **Noite C, corrida 20 (biblioteca)**: `rodar_fase4.ps1 -Modo biblioteca -Saida fase4_biblioteca`: os 54 casos de aprendizado (da tela os que reproduzem, do fixture os outros) com diagnóstico e proposta; validação; reavaliação do lote nos 36 inéditos (R5); a sonda de correção repetida (efe-3, efe-10 e os casos cujo modo foi desligado); `avaliar_fase4.py --biblioteca` aplica a R4 e conta as propostas por filtro.
- **Mede**: quantas propostas cada filtro barra, se um lote melhora os inéditos, e a precisão do ciclo de correção em código; o que o modelo propõe quando recebe as notas do próprio caso.

### P6. Cenários da Fase 5, MTTR e Task Success (sessões 10 e 11; dia)

- Catálogo da ficha 36 em `cenarios_fase4.py`, `executar_fase4.py --modo cenarios --repeticoes N`, `avaliar_fase4.py --cenarios` (MTTR médio com intervalo por reamostragem, Task Success com intervalo de Wilson), `protocolo-linha-de-base-manual.md`.
- **Testes escritos antes**: o cronômetro começa na detecção e termina na reexecução validada; Task Success só conta roteiro concluído sem erro; o banco é restaurado entre repetições (hash das tabelas igual ao seed no começo de cada uma); a versão do navegador é a mesma em todas as repetições.
- **Corrida 21 (ensaio; dia)**: `rodar_fase4.ps1 -Modo cenarios -Saida fase4_ensaio -Repeticoes 1`: os dez cenários uma vez. Não é a Fase 5: serve para dimensionar a noite dela e conferir o protocolo.
- **Mede**: tempo por cenário e o que falta para a Fase 5 rodar sem ninguém ao lado.

### P7. Avaliação da própria trilha (sessão 12; uma noite, possivelmente duas)

- `executar_fase4.py --modo avaliacao_trilha`, mutações programadas (verbete trocado, contrato alterado, seletor quebrado), amostra de intervenção, sonda de pós-racionalização, `avaliar_fase4.py --trilha`.
- **Testes escritos antes**: TPR × TNR calculado contra um gabarito sintético; cada mutação altera exatamente o nó previsto na trilha de referência; a intervenção registra limite inferior quando o rótulo some do `top_logprobs` (risco 6 da especificação).
- **Noite D, corrida 22**: `rodar_fase4.ps1 -Modo avaliacao_trilha -Saida fase4_trilha`: nos 36 de avaliação, três intervenções por caso, repetição da inferência de base, sonda de pós-racionalização e três mutações. Depois, uma sessão de revisão com o Eric sobre 12 relatórios (6 certos e 6 errados, sorteados com semente fixa): tempo até a decisão, localização do erro, adesão apropriada, utilidade percebida como medida secundária (`ESPEC` seção 12).
- **Mede**: se a divergência sinalizada coincide com os erros reais, se a trilha aponta o nó mutado, a taxa de pós-racionalização da FONTE e o que o relatório vale para quem lê.

### P8. Painel, relatório da fase e documentação (sessões 12 e 13)

- `FER\painel_fase4.py` e o grupo "Fase 4" em `painel_topicos.NAV` (id só junto com a seção, porque `teste_toda_aba_do_mapa_existe_na_pagina` exige); `DOC\3-resultados-e-analises\fase-4-relatorio.md` com os blocos `tb_f4_*` colados por `fase4.py`; achados novos, decisões, fichas fechadas, roadmap §1, §2 e §4, README (tabela de scripts e estado), handoff em `claude-memoria\contexto\`, memória, livro-razão; um revisor por documento de texto; `conferir_docs.py`; painel regerado, testado e republicado no mesmo endereço.

## 6. Corridas previstas (entram no roadmap §2 depois da aprovação)

| # | Corrida | Comando (em `EXP`) | Inferências / tempo estimado | Pré-requisito | O que fecha |
|---|---|---|---|---|---|
| 16 | Calibração e ponte (texto): sondagem dos `logprobs`, L0 nos 36 se a versão mudou, L1 curada nos 90 com `logprobs`, k = 3 (e 5) | `powershell -ExecutionPolicy Bypass -File rodar_fase4.ps1 -Modo calibracao -Saida fase4_calibracao -K 3,5` | 126 a 216 / 2h13 a 4h03 | P0 a P3 escritos e testados; máquina livre | limiares do selo (ficha 31), k (ficha 30), ponte da fase |
| 17 | Reprodução na tela (sem modelo) | `powershell -ExecutionPolicy Bypass -File rodar_fase4.ps1 -Modo reproducao -Saida fase4_reproducao` | 0 / minutos por caso | P2; cobaias no ar | R1: quais casos reproduzem; custo de um cenário; tamanho da trilha e do trace |
| 18 | Diagnóstico ao vivo e o mesmo caso do fixture | `powershell -ExecutionPolicy Bypass -File rodar_fase4.ps1 -Modo tela -Saida fase4_tela` | 40 a 144 / 0h47 a 2h50 | corridas 16 e 17 | R2: acerto e concordância tela × texto |
| 19 | Cura de seletor | `powershell -ExecutionPolicy Bypass -File rodar_fase4.ps1 -Modo cura -Saida fase4_cura -Repeticoes 5` | 0 / cerca de 0h40 | P4; ficha 29 | R3: taxa de cura, MTTR do agente |
| 20 | Biblioteca em produção e ciclo de correção | `powershell -ExecutionPolicy Bypass -File rodar_fase4.ps1 -Modo biblioteca -Saida fase4_biblioteca` | 156 / cerca de 2h39 | P5; fichas 32 e 26 | R4 e R5 |
| 21 | Ensaio dos cenários da Fase 5 | `powershell -ExecutionPolicy Bypass -File rodar_fase4.ps1 -Modo cenarios -Saida fase4_ensaio -Repeticoes 1` | 10 / cerca de 0h19 | P6; fichas 35 e 36 | tempo por cenário; protocolo |
| 22 | Avaliação da trilha | `powershell -ExecutionPolicy Bypass -File rodar_fase4.ps1 -Modo avaliacao_trilha -Saida fase4_trilha` | 288 / 4h28 a 5h24 | P7 | `ESPEC` seção 12 |

Toda corrida grava `condicoes_fase4.json` (modo, versão do Ollama, do Playwright e do navegador, hash da biblioteca, do prompt fixo e do índice, k, limiares, lista de hosts permitidos) e um log com a linha FIM e a duração; saída em `caminhos.fase3("fase4_<modo>")`; nada é gravado em pasta oficial de fase anterior.

## 7. Riscos e salvaguardas (máquina corporativa, sem administrador)

| Risco | Salvaguarda |
|---|---|
| Download do Chromium pelo Playwright bloqueado pela rede corporativa ou pelo antivírus | Parar e registrar como resultado; canal `msedge` com a versão do Edge no cabeçalho de toda trilha; nunca desligar proteção do Windows; nada é instalado fora da venv e de `%LOCALAPPDATA%\ms-playwright` |
| RAM: o `qwen2.5:7b` pede 6,5 GB livres e o navegador headless soma memória (a medir na corrida 17) | Corridas com modelo só com a máquina livre (VS Code e sessão do Claude fechados) e lançadas pelo Eric, com aviso prévio e a duração estimada; o `.ps1` espera a RAM e aborta com mensagem; o navegador abre uma vez por corrida e fecha as páginas entre cenários; medir a memória do processo e registrar |
| O Ollama se atualiza sozinho no meio da fase | R6: ponte antes de toda noite medida; versão por registro; o `.ps1` aborta se mudar no meio; sondagem dos `logprobs` repetida a cada noite |
| As páginas dependem de CDN (jQuery, AngularJS, slick, FontAwesome, mapa) e a rede pode mudar ou faltar | HAR gravado uma vez e servido pelo Playwright nas corridas medidas; lista de hosts permitidos; qualquer outro host bloqueado e registrado como incidente |
| O formulário de contato envia e-mail de verdade; `*_excluir.php` e `cliente_cancelar.php` são GET destrutivos sem sessão | Nenhum roteiro envia o formulário de contato; os roteiros destrutivos rodam só com o banco restaurado antes e depois; a lista de hosts permitidos impede qualquer SMTP ou host externo |
| O sintoma por molde difere do sintoma escrito à mão e muda o rótulo | R2 mede a concordância; o relatório da fase declara a diferença; o prompt fixo não muda |
| Só 20 dos 72 casos reproduzem na tela hoje | Ficha 28 (modos novos); o que não reproduzir continua avaliado em texto, declarado como tal; a Fase 5 mede cenários, não os 72 |
| `latency` dorme 2 s por item (28 s na lista de 14 produtos) e pode parecer travamento | Tempo limite do roteiro acima disso (60 s) e o sintoma por molde com o tempo medido contra o orçamento declarado |
| Quebra de localizador armada no navegador pode não representar quebra real | Modos declarados e documentados; limitação registrada; a ficha 29 decide |
| A trilha e os traces crescem sem limite | Ficha 33: trace só na falha, blob inline limitado, nós limitados, tamanho medido e gravado no fim da corrida, retenção declarada |
| Candidato de seletor "errado" que faz o roteiro passar | R3 separa "mesmo elemento" de "outro elemento"; o relatório mostra todos os candidatos |
| Texto de resposta HTTP entrando na biblioteca (envenenamento) | Bloqueio em código (`ESPEC` seção 10) e o filtro de nomes citados contra o sistema |
| Lote de acréscimos que piora os inéditos | R5: lote em espera com o motivo; nada entra sem reavaliação |
| A linha de base manual depende de integrantes do grupo | Ficha 36; protocolo escrito no P6 para a sessão cronometrada ser marcada com antecedência |
| Limite de sessão do Claude no meio de um pacote | Um pacote por sessão, livro-razão em `SDD\progress.md`, arquivos disjuntos entre sessões paralelas; subagentes só para trabalho mecânico e um revisor por entregável |
| Número digitado à mão ou citação errada | `--check` em todo derivado; blocos colados; `conferir_docs.py`; um revisor por documento |

## 8. Custo estimado

Base: medianas da corrida 12 (`RA\pre_fase4\confianca.md`, bloco `tb_conf_acerto`): 61,1 s por diagnóstico com a L1 curada e 69,2 s com L0; especificação (seção 6.1): de 141 a 234 s por caso com as três intervenções; o tempo de navegador por cenário (20 s) e o de uma quebra de localizador com reexecução (30 s) são chutes declarados até a corrida 17 medir. Conta em `custo_fase4.py` (rascunho da sessão de 26/10; a versão versionada entra em `avaliar_fase4.py --custo` depois da aprovação).

| Bloco | Conta | Tempo de máquina |
|---|---|---|
| Noite A: ponte (36 × 69,2 s) e calibração (90 × 61,1 s); k = 5 nos 90 com prompt 20% maior, se a ficha 30 for (a) | 0h42 + 1h32 (+ 1h50) | 2h13 a 4h03 |
| Noite B: tela (20 a 72 casos × (61,1 + 20) s) e os mesmos casos do fixture (× 61,1 s) | 0h27 + 0h20 até 1h37 + 1h13 | 0h47 a 2h50 |
| Dia: cura (80 execuções × 30 s) | | 0h40 |
| Noite C: 54 × (61,1 + 61,1) s, reavaliação 36 × 61,1 s, sonda de correção 12 × 61,1 s | 1h50 + 0h37 + 0h12 | 2h39 |
| Dia: ensaio dos cenários (10 × 111 s) | | 0h19 |
| Noite D: intervenções 36 × 141 a 234 s, base 36 × 61,1 s, pós-racionalização 36 × 61,1 s, mutações 108 × 61,1 s | 1h25 a 2h20 + 0h37 + 0h37 + 1h50 | 4h28 a 5h24 |
| **Total da Fase 4** | | **11h06 a 15h55** (quatro noites e dois blocos de dia) |
| Referência, fora da fase: a Fase 5 inteira (10 cenários × 5 repetições × 111 s) | | cerca de 1h33 mais a linha de base manual |

Sessões de trabalho (Claude com o Eric por perto nas decisões): 13 sessões, uma por pacote ou meio pacote (tabela abaixo), de 2 a 4 horas de trabalho cada; do Eric, além das noites lançadas: as respostas às fichas 26 a 36 (antes do P2), a conferência dos inéditos novos (ficha 27), a sessão de revisão de 12 relatórios no P7 (cerca de 1 hora) e os commits.

| Sessão | Conteúdo | Máquina |
|---|---|---|
| S1 | P0: aprovação registrada, Playwright, ambiente, fixture da árvore | minutos |
| S2 e S3 | P1: trilha v2 e relatório v2 | nenhuma |
| S3 a S5 | P2: interceptador, poda, caso ao vivo, cenários, banco, modos novos; corrida 17 | dia, sem modelo |
| noite A | corrida 16: calibração e ponte | 2h13 a 4h03 |
| S5 e S6 | P3: diagnóstico ao vivo; leitura da corrida 16; limiares | |
| noite B | corrida 18: tela | 0h47 a 2h50 |
| S7 e S8 | P4: cura de seletor; corrida 19 | dia, 0h40 |
| S8 a S10 | P5: biblioteca em produção e ciclo de correção | |
| noite C | corrida 20: biblioteca | 2h39 |
| S10 e S11 | P6: cenários da Fase 5, cronômetros, protocolo; corrida 21 | dia, 0h19 |
| S12 | P7: avaliação da trilha; sessão de revisão com o Eric | |
| noite D | corrida 22: avaliação da trilha | 4h28 a 5h24 |
| S12 e S13 | P8: painel, relatório da fase, documentação, handoff; o Eric commita | |

## 9. Verificação fim a fim

1. `PYTHONIOENCODING=utf-8 python EXP\testar_fase3.py` (60), `testar_fase3b.py` (30), `testar_pre_fase4.py` (47) e `testar_fase4.py` (novos): todos ok, com o hash das áreas só de leitura igual antes e depois.
2. `--check` limpo em `avaliar_fase4.py`, `gerar_relatorio_raciocinio.py --vitrine`, `analisar_confianca.py` (corridas 12 e 16), `gerar_atlas.py` e nos já existentes.
3. `RA\fase3\`, `RA\fase3b_*`, `RA\pre_fase4_confianca\` e `base_conhecimento\` com hash igual; `biblioteca_producao\` com hash `1fca10f1a6f6` até o primeiro lote aceito, e a partir daí com o hash gravado no `fechamento.json` novo e a origem de cada verbete na trilha.
4. `versao_ollama`, versão do Playwright e do navegador uniformes dentro de cada corrida; o registro de diagnóstico com as 37 chaves oficiais.
5. `python FER\gerar_dashboard.py --check`, `testar_painel_textos.py`, `testar_painel_topicos.py`, capturas das abas novas nos dois temas e em largura de celular, painel republicado no mesmo endereço.
6. `python FER\conferir_docs.py`: tudo ok; `git status` lista só o previsto; o Eric commita.

## 10. Fora do escopo

Patch no código da aplicação-alvo (ABNT §2.1); troca de modelo, de motor ou de quantização (decisões 52, 55, 69, 75); segundo modelo residente (decodificação especulativa, rerank por modelo, verificador pequeno); saída restrita por gramática (decisão 78; volta só se o formato inválido custar casos, medido na trilha); Brainiac, MCP, servidor Playwright MCP, atenção ou ativações ao vivo (decisão 55; mapa da onda 2); validação em Linux (limitação declarada); Cypress (a contingência do ABNT não é acionada: o Playwright roda); o texto da Pré-Fase 4 e desta fase no projeto ABNT (ficha 25); a medição completa da Fase 5 (só o ensaio de uma repetição); mudar o front PHP legado; desligar qualquer proteção do Windows; instalar o que quer que seja com administrador.

## 11. Rastreabilidade

| O quê | Onde |
|---|---|
| Esqueleto e requisitos | `DOC\roadmap.md` §4.1 a §4.5, §5, §7 |
| O que a Pré-Fase 4 entregou | `DOC\3-resultados-e-analises\pre-fase-4-relatorio.md` §5 (decidido e candidatos), §4.2 (corrida 12), §3.3 (verbetes novos nunca recuperados) |
| Especificação da trilha | `ESPEC` (seções 3 a 14; decisões 77 e 78) |
| Decisões | `DOC\1-decisoes-e-historico\decisoes.md`, 44, 47, 48, 52, 55, 58, 61, 65, 69, 71, 73, 75, 77, 78 |
| Números citados | `RA\pre_fase4\confianca.md` (blocos `tb_conf_acerto`, `tb_conf_revisao`, `tb_conf_resumo`); `RA\recuperador\experimento_recuperador.md` (hit@3 e hit@5, decisão 61); relatório da 3-B §3 (variação entre corridas) e §7; achado 4.42 (`contrato-produto` em 15 dos 36 contextos); contagem de casos por script sobre os bancos e `RA\fase3\particao.json` (26/10/2026) |
| Harness e cobaias | leitura de 26/10/2026: `EXP\cliente_ollama.py`, `recuperacao.py`, `biblioteca.py`, `evolucao_biblioteca.py`, `executar_fase3.py`, `executar_fase3b.py`, `trilha.py`, `gerar_relatorio_raciocinio.py`, `sondar_logprobs.py`, `sonda_confianca.py`, `analisar_confianca.py`, `sonda_correcao.py`, `banco_casos*.py`, `rodar_*.ps1`; `API\app\fault_injection.py`, `routers\produtos.py`, `schemas.py`, `config.py`; `FRONT\produtos_api.php`, `menu_publico.php`, `rodape.php`, `admin\*.php`, `cliente\*.php`; `RAIZ\run.py`, `install.py`, `_env_common.py` |
| Fichas | `DOC\pendencias.md`, fichas 26 a 36 |
