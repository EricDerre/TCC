<!-- ! Alteração de IA - Revisar: relatório novo (01/10/2026) da Pré-Fase 4, ainda parcial: a viabilidade de rodar modelo grande lendo os pesos do disco (repositório colibri), a validação da descrição que o Gemini deu do "expert atlas", o atlas montado com os dados do projeto e o protótipo da trilha e do relatório de raciocínio. As tabelas são coladas por script (blocos `tb_viab_`, `tb_atlas_` e `tb_rac_`, conferidos por `--check`).
     ! Motivo: o Eric abriu a Pré-Fase 4 em 01/10/2026 (decisão 70) com três perguntas e pediu análise densa, com ganhos e custos, para citar na documentação formal. Sem este arquivo as respostas ficariam espalhadas entre o levantamento §6.14, o painel e os derivados em `resultados_alvo/pre_fase4/`. O que ainda falta medir ou pesquisar está dito em cada seção, para ninguém ler como conclusão o que é parcial. -->
# Pré-Fase 4: relatório (em andamento)

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). A literatura está no [levantamento da Pré-Fase 4](../2-pesquisa-e-literatura/levantamento-2026-10-01-pre-fase-4.md) (§6.14) e o plano em [roadmap.md](../roadmap.md) (§3.1). As tabelas deste relatório saem de `viabilidade_modelos_grandes.py`, `gerar_atlas.py` e `gerar_relatorio_raciocinio.py` (pasta `resultados_alvo/pre_fase4/`) e são conferidas por `--check`.

> **Estado em 01/10/2026:** das três frentes, a primeira (modelos grandes pelo disco) tem veredito; a segunda (atlas) tem a validação do texto do Gemini e o atlas com os dados do projeto, e falta o atlas de um modelo MoE de verdade (corrida 13); a terceira (raciocínio aberto) tem o protótipo sobre as corridas gravadas, e faltam a parte B da pesquisa bibliográfica e a sonda de confiança (corrida 12). Nenhuma decisão nova foi tomada: a decisão 52 (`qwen2.5:7b` com a biblioteca L1) e a decisão 69 continuam valendo.

## 1. As três perguntas

| Frente | Pergunta do Eric | Resposta até aqui | O que falta |
|---|---|---|---|
| 1. Modelos grandes pelo disco | A ideia do repositório colibri (rodar modelo muito grande em máquina fraca lendo os pesos do SSD) serve ao projeto, que é só CPU? Com que ganhos e custos? | Não como motor do agente: nesta máquina só o menor modelo do repositório roda com folga, 2 modelos grandes ficam no mínimo de RAM que o repositório declara, sem medida publicada nessa condição, e nas máquinas maiores em que há medida uma resposta levaria minutos. Aproveitam-se três ideias sem trocar de motor (seção 2.4). | A medição real com o OLMoE (corrida 13), que não muda o veredito e alimenta o atlas. |
| 2. Atlas visual | A descrição que o Gemini deu das imagens está certa? Dá para aplicar ao projeto e pôr no painel, de forma interativa? | A descrição acerta o que é MoE e o que a tela mostra, erra no que a posição dos pontos significa e na escala, e exagera nas "regiões dedicadas" (seção 3.1). O método foi aplicado ao que o projeto mede e está na aba Atlas do painel (seção 3.2). | O atlas do OLMoE lendo os nossos casos (corrida 13). |
| 3. Raciocínio aberto | Dá para deixar aberto tudo o que a IA fez, num arquivo bruto, e gerar dele um relatório para humanos? O que isso rende para lapidar a IA e conter alucinação? | O protótipo sobre as corridas gravadas existe: a trilha em três camadas, o relatório por caso e os indicadores (seção 4.1). | A parte B da pesquisa (seis tópicos), a sonda de confiança (corrida 12) e a especificação do que a Fase 4 emite. |

## 2. Modelos grandes lendo os pesos do disco (colibri)

<!-- ! Alteração de IA - Revisar: correção de 01/10/2026 (tarde) nesta seção e na linha 1 da tabela da seção 1: a RAM mínima do repositório passou a ser comparada com a memória instalada (16 GB), não com a que o Windows enxerga (15,69 GB).
     ! Motivo: a primeira versão dizia que a máquina ficava abaixo do mínimo de RAM e que só o menor modelo rodava; ela está exatamente no mínimo declarado, e dois modelos grandes cabem no disco livre. O defeito estava em `viabilidade_modelos_grandes.py` (função `cabe`) e foi achado na revisão do levantamento. O veredito para o agente não muda. -->

### 2.1 O que o repositório faz

O colibri é um motor de inferência escrito em C para modelos de mistura de especialistas (MoE). Num modelo MoE, cada camada tem muitos blocos de pesos, os especialistas, e um roteador escolhe poucos deles para cada token. O colibri mantém na RAM a parte do modelo que todo token usa e um cache de especialistas, e lê do disco, a cada token, os especialistas que o roteador escolheu e que não estão no cache. O disco entra na carga dos pesos, não na tokenização. A leitura integral do repositório, as medidas publicadas e as pesquisas em que ele se apoia estão no levantamento (§6.14.1 e §6.14.2); a literatura independente sobre inferência com os pesos fora da RAM, em §6.14.3; os modelos MoE que cabem em 16 GB, em §6.14.4.

### 2.2 A conta para esta máquina

A máquina, medida por `ferramentas/medir_disco.py`, e as medianas do agente nos 360 diagnósticos da Fase 3:

<!-- tabela:tb_viab_maquina -->
| Item | Valor | Origem |
|---|---|---|
| Processador | 12th Gen Intel(R) Core(TM) i5-1235U | `disco.json` (`maquina.cpu`) |
| RAM instalada | 16,0 GB | `disco.json` (`maquina.ram_instalada_gb`) |
| RAM que o sistema enxerga | 15,69 GB | `disco.json` (`maquina.ram_gb`) |
| RAM livre no início de uma corrida | 7,2 GB | `resultados_alvo/maquina.json` (`ram_livre_no_inicio_gb`, Fase 2-B) |
| Disco | NVMe SM2P41C3 NVMe ADATA 512GB (NVMe) | `disco.json` (`maquina.disco`) |
| Disco: tamanho e espaço livre | 474,0 GB, 218,1 GB livres | `disco.json` (`maquina.disco`) |
| Leitura do disco por fora do cache (mediana) | 3,77 GB/s | `disco.json` (`direto.gb_por_s_mediana`) |
| Leitura passando pelo cache (mediana) | 2,31 GB/s | `disco.json` (`pelo_cache.gb_por_s_mediana`) |
| Resposta mediana do `qwen2.5:7b` | 61,0 tokens em 66,7 s (360 diagnósticos) | registros oficiais da Fase 3 |
| Prompt mediano | 1285,5 tokens | registros oficiais da Fase 3 |
<!-- /tabela:tb_viab_maquina -->

O que cada modelo suportado pelo repositório pede (tabela do README, conferida pela rodada 5 da pesquisa) e o que esta máquina tem. Roda com folga o modelo que cabe no disco livre e pede menos RAM do que a instalada; fica no limite o que cabe no disco livre e pede exatamente a RAM instalada, que é o mínimo declarado pelo repositório; o resto não roda:

<!-- tabela:tb_viab_familias -->
| Modelo | Parâmetros (bilhões) | Ativos por token (bilhões) | Disco pedido (GB) | RAM pedida (texto do repositório) | Cabe no disco livre | Caberia no disco vazio | RAM pedida contra a instalada | Roda nesta máquina |
|---|---|---|---|---|---|---|---|---|
| OLMoE | 7 | 1 | 7,0 | 8 GB | sim | sim | sim | sim |
| Qwen3.6-35B-A3B | 35 | 3 | 20,0 | 24 GB (needs full RAM residency) | sim | sim | **não** | **não** |
| DeepSeek V4 Flash | 284 | 13 | 167,0 | 16 GB min, 32 GB comfortable | sim | sim | no mínimo declarado | no limite |
| Qwen3.8-Flash-Next | 180 | 6 | 185,5 | 16 GB min, 24 GB comfortable at the default context | sim | sim | no mínimo declarado | no limite |
| GLM-5.3-Flash | 320 | 18 | 195,0 | 25 GB (12 GB weights at int4 + expert cache) | sim | sim | **não** | **não** |
| GLM-5.2 | 744 | 40 | 372,0 | 16 GB min, 24 GB comfortable | **não** | sim | no mínimo declarado | **não** |
| GLM-5.3 | n/a | n/a | 419,0 | 16 GB min, 24 GB comfortable | **não** | sim | no mínimo declarado | **não** |
| Inkling | 975 | 41 | 469,0 | 25 GB with the int4 dense container, ~120 GB without | **não** | sim | **não** | **não** |
| Kimi K3 | 2800 | 104 | 1600,0 | 32 GB+ | **não** | **não** | **não** | **não** |
<!-- /tabela:tb_viab_familias -->

Quanto o disco, sozinho, custaria por token do GLM-5.2. A primeira linha é medida; as de SSD SATA e de disco rígido são premissas declaradas, porque o repositório não publica medida nesses discos:

<!-- tabela:tb_viab_disco -->
| Disco | Leitura (GB/s) | Medido ou premissa | Segundos de disco por token frio | Teto de tokens por segundo | Minutos só de leitura para a resposta mediana |
|---|---|---|---|---|---|
| NVMe desta máquina, leitura por fora do cache (medido) | 3,77 | medido | 3,0 | 0,330 | 3,1 |
| SSD SATA (premissa: 0,55 GB/s, teto prático da interface) | 0,55 | premissa | 20,7 | 0,048 | 21,1 |
| disco rígido de 7.200 rpm (premissa: 0,15 GB/s em leitura sequencial) | 0,15 | premissa | 76,0 | 0,013 | 77,3 |
<!-- /tabela:tb_viab_disco -->

As medidas só com CPU que o repositório publica, aplicadas à resposta mediana do agente. Elas contam só a geração; a leitura do prompt em máquina pequena não é medida lá, então o tempo real seria maior:

<!-- tabela:tb_viab_terceiros -->
| Máquina (medida publicada no repositório) | Modelo | Tokens por segundo | Condição | Minutos só de geração para a nossa resposta mediana | Vezes o tempo total de um diagnóstico de hoje | Issue |
|---|---|---|---|---|---|---|
| Intel Core Ultra 7 270K Plus, 24 GB, WSL2, NVMe | GLM-5.2 | 0,07 | padrão; cache de especialistas com acerto de 3 a 4% | 14,5 | 13,1 | #2 |
| Intel Core Ultra 7 270K Plus, 24 GB, WSL2, NVMe | GLM-5.2 | 0,11 | com --topp 0.7, que o repositório marca como opção com perda | 9,2 | 8,3 | #2 |
| Intel i5-12600K, 32 GB, Windows 11 nativo, só CPU | GLM-5.2 | 0,08 | frio, cache limitado pela RAM a cerca de 2 especialistas por camada | 12,7 | 11,4 | #113 |
| Intel Core Ultra 9 185H, 32 GB, Windows 11 nativo | GLM-5.2 | 0,03 | frio, só CPU; a mesma máquina chega a 0,5 com o cache quente | 33,9 | 30,5 | #128 |
| Apple M3 básico, 16 GB, só CPU | OLMoE | 3,69 | frio; 4,18 com o cache quente | 0,3 | 0,2 | #949 |
<!-- /tabela:tb_viab_terceiros -->

### 2.3 Ganhos e custos

| Ideia | Ganho | Custo ou limite para este projeto | Onde está a evidência |
|---|---|---|---|
| Rodar um modelo de centenas de bilhões de parâmetros sem GPU, lendo os especialistas do NVMe | Acesso a um modelo muito maior que a RAM, com saída idêntica à do modelo inteiro nas otimizações que o repositório classifica como exatas | Nesta máquina o GLM-5.2 não cabe no disco livre, e na RAM ela fica exatamente no mínimo declarado; DeepSeek V4 Flash e Qwen3.8-Flash-Next cabem no disco livre e também ficam no mínimo de RAM, sem medida publicada numa máquina dessa classe (tabela `tb_viab_familias`). Nas máquinas maiores em que há medida, só a geração de uma resposta do tamanho das nossas leva minutos (tabela `tb_viab_terceiros`) | Seção 2.2; §6.14.1 |
| Trocar a velocidade do disco por memória | O NVMe desta máquina entrega a leitura que o método pede (tabela `tb_viab_disco`): o disco não é o gargalo | O que limita é a RAM, como o autor da medição no i5-12600K de 32 GB aponta; nesta máquina, antes disso, o espaço em disco para o modelo maior. Em SSD SATA e em disco rígido a conta piora, e a tabela de medições do repositório não tem linha com disco rígido | Seção 2.2; §6.14.1; §6.14.3 |
| Usar o modelo MoE pequeno que cabe (OLMoE) | Roda nesta máquina | Fica inteiro na RAM, então a leitura do disco não é o que o viabiliza; trocar de modelo invalida a biblioteca L1 e a comparação com as fases já medidas (decisão 69) | Mapa do levantamento (§6.14.13); §6.14.4 |
| Escolha fechada por probabilidade (o modo Brio do repositório) | Um sinal de incerteza calculado, sem trocar de motor: o diagnóstico já é uma escolha entre 23 causas, e o Ollama instalado devolve a probabilidade de cada token | Pontuar opção por opção multiplicaria a leitura do prompt; o que se mede na corrida 12 é a probabilidade do rótulo que o modelo escreveu, que não custa inferência a mais | Sonda `sondar_logprobs.py` (aba "Modelos grandes pelo disco" do painel); §6.14.1 |
| Método do atlas | Uma forma de ver o que a busca entrega e o que o modelo aproveita, sem nenhuma inferência nova | Descreve a busca e o uso do contexto, não o interior do modelo | Seção 3 |
| Disciplina de medição do repositório | Separar as otimizações que não mudam a saída das que mudam, e só aceitar ganho medido de ponta a ponta | Nenhum | Mapa do levantamento (§6.14.13) |
| Uso contínuo do SSD | Não se aplica | A descarga de pesos é carga de leitura (o estudo de descarga mede as escritas na descarga do cache KV, não nos pesos); os riscos que o repositório colibri aponta, sem medir, são a troca de memória para o disco quando a RAM acaba e o aquecimento em horas de leitura contínua | Riscos do mapa (§6.14.13); §6.14.3 |

### 2.4 Veredito

O colibri não entra como motor do agente, e o modelo decidido não muda. Com SSD NVMe, o que limita o método nesta máquina é o espaço em disco e a RAM (ela está no mínimo que o repositório declara, sem folga), não a velocidade de leitura; com SSD SATA ou disco rígido, a velocidade também barraria. Dois modelos grandes (DeepSeek V4 Flash e Qwen3.8-Flash-Next) poderiam ser tentados no limite; não há medida publicada deles numa máquina de 16 GB, e as medidas do GLM-5.2 em máquinas de 24 e 32 GB já ficam em minutos por resposta. O repositório entra na documentação formal como trabalho relacionado, com as ressalvas de que é um projeto da comunidade e de que parte das medidas vem de issues, sem revisão por pares.

Três coisas se aproveitam sem trocar de motor: a probabilidade do rótulo como sinal de incerteza (a corrida 12 mede se ela separa acerto de erro); o método do atlas, já aplicado aos dados do projeto (seção 3); e a disciplina de medição. O mapa com o veredito de cada opção avaliada, adotada, adiada ou descartada, está no levantamento (§6.14.13) e na aba "Modelos grandes pelo disco" do painel.

## 3. Atlas

### 3.1 A descrição do Gemini, conferida afirmação por afirmação

As duas imagens que o Eric enviou são da página Brain do painel web do colibri, que desenha o "expert atlas" do GLM-5.2. O texto do Gemini foi conferido contra o README do repositório (acesso em 01/10/2026) e contra a literatura levantada.

| O que o Gemini afirmou | Veredito | O que as fontes dizem | Fonte |
|---|---|---|---|
| A visualização é formalmente chamada de Expert Atlas ou Mapa de Afinidades MoE | Impreciso | "Expert atlas" é o nome que o repositório dá à ferramenta dele e ao resultado; "Brain" é o nome da página do painel. Não é um termo formal da área: a literatura trata o assunto como análise de roteamento e de especialização dos especialistas. "Mapa de Afinidades MoE" não aparece nas fontes levantadas | §6.14.1; §6.14.5 |
| É uma interface para explorar a estrutura interna do GLM-5.2, um modelo de mistura de especialistas | Correto | É a página Brain do painel do colibri, com o atlas do GLM-5.2 | README, seção "See it running"; §6.14.1 |
| Num modelo MoE um roteador envia os dados só para pequenas sub-redes, os especialistas; a tela isola o especialista 178 da camada 17 | Correto | É a definição da arquitetura, e o atlas identifica cada especialista pela camada e pelo índice | §6.14.2; §6.14.5 |
| O painel mede quais tópicos ativam com mais frequência aquele especialista (20,2% Python, 14,6% JSON, 13,3% SQL): um generalista focado em programação | Correto no essencial, com duas ressalvas | A afinidade não é a frequência crua: é a taxa de escolha em cada tópico, corrigida pela taxa de base e levada a somar 100%. E a medição usa 30 prompts (10 tópicos, 3 por tópico), com exigência de repetição em pelo menos 2 deles. Com a maior fatia perto de 20%, o próprio atlas o classifica como generalista | §6.14.5 (método do expert atlas) |
| Topologia latente (manifold 3D): os especialistas são posicionados com base em suas semelhanças semânticas | Errado | O README diz: "position is measured routing affinity, not a learned embedding". A posição vem da afinidade de roteamento medida, não de um espaço latente aprendido nem de semelhança de significado | README, seção "See it running" |
| São centenas de especialistas | Errado | São 19.456 especialistas no GLM-5.2; o painel mostra 13.260 caracterizados em dez regiões | README; §6.14.1; §6.14.5 |
| Há "regiões cerebrais" dedicadas a campos isolados, como medicina, matemática, poesia ou idiomas | Exagerado | As dez regiões são as dez categorias dos prompts usados na medição: o atlas só pode mostrar as categorias com que foi sondado. Só 7,9% dos especialistas são especialistas fortes; os demais são generalistas. E a literatura traz resultados negativos: a escolha do roteador acompanha a geometria dos estados internos, a sintaxe e a identidade do token mais do que a competência por domínio | §6.14.5 |
| O modo Live routing permite rastrear exatamente o caminho que uma requisição percorre enquanto a IA elabora a resposta | Correto quanto ao que mostra, com ressalva | O modo mostra o modelo em execução, uma célula por especialista, e cada especialista acionado num turno pisca. Mostra quais especialistas foram usados, não por que a resposta saiu como saiu: não é um registro de raciocínio | README, seção "See it running"; §6.14.5 |
| A ferramenta transforma uma matriz de números num mapa de conhecimento, do tipo que pesquisadores usam para abrir a caixa preta | Em parte | É um mapa de histogramas de roteamento, de um repositório da comunidade, sem revisão por pares. A pesquisa de interpretabilidade usa outros instrumentos (sondas lineares, autoencoders esparsos, grafos de atribuição), cada um com limites conhecidos | §6.14.5 |

Em resumo: o texto acerta o que é um modelo MoE e o que a tela mostra, erra no que a posição dos pontos significa e na escala, e exagera ao tratar as regiões como áreas dedicadas. Para o projeto, a consequência é direta: os modelos do agente são densos, sem especialistas que um roteador escolha, então não há esse atlas para desenhar deles. O que se transfere é o método de medição.

### 3.2 O método aplicado ao que o projeto mede

O `expert_atlas` conta, para cada especialista e cada tópico, em quantos prompts independentes ele foi escolhido; divide pela quantidade de prompts do tópico; calcula a especialização como 1 menos a entropia das afinidades sobre a entropia máxima; só chama de especialista quem se repete em pelo menos dois prompts; e valida deixando um prompt de fora. No projeto, a escolha que se pode medir do mesmo jeito é a da busca: para cada caso de teste, ela põe três verbetes da biblioteca no contexto. O item é o caso, a entidade é o verbete, e as categorias são as seis classes de defeito. `gerar_atlas.py` faz essa conta para cada versão da biblioteca da corrida oficial.

<!-- tabela:tb_atlas_bibliotecas -->
| Biblioteca | Verbetes | Recuperados em algum caso | Especialistas | Generalistas | Sem repetição | Nunca recuperados |
|---|---|---|---|---|---|---|
| L1 do `qwen2.5-coder:7b` (`0f0a6b7f3b37`) | 36 | 34 | 18 | 12 | 4 | 2 |
| L3 do `qwen2.5-coder:7b` (`2b7c441cb9e3`) | 36 | 34 | 19 | 11 | 4 | 2 |
| original, L0 (`3196327e7fd5`) | 36 | 34 | 20 | 10 | 4 | 2 |
| L1 do `qwen2.5:7b` (`3394d203cab9`) | 42 | 34 | 19 | 13 | 2 | 8 |
| L1 do `qwen2.5-coder:3b` (`53ccf19abeac`) | 36 | 34 | 20 | 10 | 4 | 2 |
| L2 do `qwen2.5:7b` (`5aa8cf796035`) | 43 | 34 | 18 | 14 | 2 | 9 |
| L2 do `qwen2.5-coder:7b` (`6791ba8b281c`) | 36 | 33 | 18 | 12 | 3 | 3 |
| L3 do `qwen2.5:7b` (`71258b553152`) | 45 | 34 | 17 | 15 | 2 | 11 |
| L2 do `qwen2.5-coder:3b` (`959db34be15c`) | 36 | 34 | 20 | 10 | 4 | 2 |
| L3 do `qwen2.5-coder:3b` (`d9a86e383103`) | 37 | 34 | 20 | 10 | 4 | 3 |
<!-- /tabela:tb_atlas_bibliotecas -->

Os verbetes da biblioteca decidida, do mais recuperado para o menos:

<!-- tabela:tb_atlas_verbetes -->
| Verbete | Pasta | Casos em que entrou no contexto | Vezes em primeiro | Classe dominante | Especialização | Entropia (bits) | Rótulo | Notas do modelo |
|---|---|---|---|---|---|---|---|---|
| `entidade-produto` | negocio | 42 | 35 | sintática | 0,08 | 2,37 | generalista | 2 |
| `contrato-produto` | contratos | 38 | 1 | sintática | 0,06 | 2,43 | generalista | 3 |
| `contrato-pedido` | contratos | 23 | 17 | semântica | 0,06 | 2,44 | generalista | 0 |
| `pedido-reserva` | negocio | 14 | 0 | tradução | 0,26 | 1,92 | generalista | 3 |
| `contagem_inconsistente` | erros | 13 | 6 | runtime | 0,33 | 1,74 | generalista | 0 |
| `estado_da_tela_divergente` | erros | 13 | 1 | efeito | 0,35 | 1,67 | generalista | 3 |
| `tipo_divergente` | erros | 13 | 0 | semântica | 0,27 | 1,89 | generalista | 1 |
| `estrutura_aninhada_divergente` | erros | 12 | 0 | runtime | 0,40 | 1,55 | generalista | 2 |
| `localizador_quebrado` | erros | 9 | 7 | efeito | 0,81 | 0,50 | especialista | 1 |
| `ancora-saiba-mais` | defeitos_conhecidos | 8 | 0 | efeito | 0,79 | 0,54 | especialista | 0 |
| `corpo_nao_e_json` | erros | 7 | 5 | léxica | 0,67 | 0,86 | especialista | 2 |
| `colecao_no_lugar_de_objeto` | erros | 6 | 0 | sintática | 0,44 | 1,46 | generalista | 2 |
| `tempo_de_resposta_excedido` | erros | 6 | 2 | nenhuma | 0,26 | 1,92 | generalista | 0 |
| `campo_ausente` | erros | 5 | 0 | sintática | 0,72 | 0,72 | especialista | 1 |
| `erro_interno_do_servidor` | erros | 5 | 3 | runtime | 0,62 | 0,97 | especialista | 2 |
| `formato_de_data_divergente` | erros | 5 | 1 | semântica | 0,26 | 1,92 | generalista | 1 |
| `valor_fora_do_dominio` | erros | 5 | 0 | nenhuma | 0,41 | 1,52 | generalista | 1 |
| `corpo_vazio` | erros | 4 | 3 | léxica | 0,69 | 0,81 | especialista | 2 |
| `dado_desatualizado` | erros | 4 | 1 | runtime | 0,69 | 0,81 | especialista | 1 |
| `mensagens-de-erro-do-codigo` | erros | 4 | 0 | runtime | 0,69 | 0,81 | especialista | 0 |
| `campo_renomeado` | erros | 3 | 1 | sintática | 1,00 | 0,00 | especialista | 1 |
| `codificacao_incorreta` | erros | 3 | 1 | léxica | 0,65 | 0,92 | especialista | 0 |
| `fluxo-reserva-e-cancelamento` | negocio | 3 | 0 | nenhuma | 0,39 | 1,58 | generalista | 0 |
| `limite_de_requisicoes` | erros | 3 | 2 | runtime | 1,00 | 0,00 | especialista | 0 |
| `nulo_inesperado` | erros | 3 | 0 | semântica | 1,00 | 0,00 | especialista | 0 |
| `recurso_inexistente` | erros | 3 | 2 | runtime | 0,65 | 0,92 | especialista | 1 |
| `resposta_truncada` | erros | 3 | 0 | léxica | 1,00 | 0,00 | especialista | 2 |
| `usuario-e-login` | negocio | 3 | 1 | tradução | 0,65 | 0,92 | especialista | 0 |
| `escala_ou_unidade_errada` | erros | 2 | 0 | tradução | 1,00 | 0,00 | especialista | 2 |
| `limites-do-sistema` | negocio | 2 | 0 | efeito | 1,00 | 0,00 | especialista | 0 |
| `pagina-produtos-api` | negocio | 2 | 0 | nenhuma | 0,61 | 1,00 | especialista | 0 |
| `registro_duplicado` | erros | 2 | 1 | nenhuma | 0,61 | 1,00 | especialista | 0 |
| `chave_de_juncao_errada` | erros | 1 | 0 | semântica | 1,00 | 0,00 | sem repetição | 1 |
| `consultas-sem-checagem` | defeitos_conhecidos | 1 | 0 | efeito | 1,00 | 0,00 | sem repetição | 0 |
| `atualizacao_imediata` | aprendidos | 0 | 0 | nenhuma | n/d | n/d | nunca recuperado | 0 |
| `conversao-de-unidade` | aprendidos | 0 | 0 | nenhuma | n/d | n/d | nunca recuperado | 0 |
| `conversao-de-valor` | aprendidos | 0 | 0 | nenhuma | n/d | n/d | nunca recuperado | 0 |
| `interface-estados` | aprendidos | 0 | 0 | nenhuma | n/d | n/d | nunca recuperado | 0 |
| `interface-frontend` | aprendidos | 0 | 0 | nenhuma | n/d | n/d | nunca recuperado | 0 |
| `modos-de-injecao` | falhas_injetadas | 0 | 0 | nenhuma | n/d | n/d | nunca recuperado | 0 |
| `rotas-inexistentes` | aprendidos | 0 | 0 | nenhuma | n/d | n/d | nunca recuperado | 0 |
| `senha-sem-hash` | defeitos_conhecidos | 0 | 0 | nenhuma | n/d | n/d | nunca recuperado | 0 |
<!-- /tabela:tb_atlas_verbetes -->

A validação: o atlas prevê a classe de um caso pelos verbetes da rota dele. Na corrida oficial o caso previsto fica de fora da montagem do atlas; nos casos inéditos, o atlas dos casos oficiais prevê casos que nunca entraram na conta.

<!-- tabela:tb_atlas_validacao -->
| Biblioteca | Casos | Acertos deixando um de fora | Acerto | Empates | Sem evidência | Inéditos previstos | Acerto nos inéditos | Acaso |
|---|---|---|---|---|---|---|---|---|
| L1 do `qwen2.5-coder:7b` (`0f0a6b7f3b37`) | 90 | 57 | 63,3% | 0 | 0 | n/d | n/d | 16,7% |
| L3 do `qwen2.5-coder:7b` (`2b7c441cb9e3`) | 90 | 56 | 62,2% | 1 | 0 | n/d | n/d | 16,7% |
| original, L0 (`3196327e7fd5`) | 90 | 59 | 65,6% | 1 | 0 | 23 de 36 | 63,9% | 16,7% |
| L1 do `qwen2.5:7b` (`3394d203cab9`) | 90 | 56 | 62,2% | 0 | 0 | 23 de 36 | 63,9% | 16,7% |
| L1 do `qwen2.5-coder:3b` (`53ccf19abeac`) | 90 | 59 | 65,6% | 1 | 0 | 23 de 36 | 63,9% | 16,7% |
| L2 do `qwen2.5:7b` (`5aa8cf796035`) | 90 | 56 | 62,2% | 0 | 0 | n/d | n/d | 16,7% |
| L2 do `qwen2.5-coder:7b` (`6791ba8b281c`) | 90 | 57 | 63,3% | 1 | 0 | n/d | n/d | 16,7% |
| L3 do `qwen2.5:7b` (`71258b553152`) | 90 | 56 | 62,2% | 0 | 0 | 24 de 36 | 66,7% | 16,7% |
| L2 do `qwen2.5-coder:3b` (`959db34be15c`) | 90 | 61 | 67,8% | 1 | 0 | n/d | n/d | 16,7% |
| L3 do `qwen2.5-coder:3b` (`d9a86e383103`) | 90 | 62 | 68,9% | 0 | 0 | 22 de 36 | 61,1% | 16,7% |
<!-- /tabela:tb_atlas_validacao -->

Por corrida, o acerto do modelo cruzado com a rota. O primeiro cruzamento usa o gabarito (a rota aponta a classe verdadeira do caso?) e serve para entender; o segundo não usa (a causa que o modelo respondeu é de uma classe que a rota aponta?) e é um sinal que o agente pode calcular sozinho.

<!-- tabela:tb_atlas_fatias -->
| Fatia | Casos | Acerto do modelo | Verbetes citados (distintos) | Citações fora do contexto | Rota aponta a classe: acerto | Rota não aponta: acerto | Resposta na classe da rota: acerto | Resposta fora da classe da rota: acerto |
|---|---|---|---|---|---|---|---|---|
| `fase3/granite4.2_8b/L0` | 90 | 76,7% (69) | 29 | 0 | 91,5% (54 de 59) | 48,4% (15 de 31) | 82,1% (55 de 67) | 59,1% (13 de 22) |
| `fase3/granite4.2_8b/L1` | 90 | 77,8% (70) | 31 | 1 | 91,5% (54 de 59) | 51,6% (16 de 31) | 84,6% (55 de 65) | 58,3% (14 de 24) |
| `fase3/granite4.2_8b/L2` | 90 | 74,4% (67) | 31 | 0 | 91,5% (54 de 59) | 41,9% (13 de 31) | 82,1% (55 de 67) | 50,0% (11 de 22) |
| `fase3/granite4.2_8b/L3` | 90 | 75,6% (68) | 31 | 1 | 91,5% (54 de 59) | 45,2% (14 de 31) | 83,3% (55 de 66) | 52,2% (12 de 23) |
| `fase3/qwen2.5-coder_3b/L0` | 90 | 65,6% (59) | 27 | 0 | 74,6% (44 de 59) | 48,4% (15 de 31) | 81,8% (45 de 55) | 38,2% (13 de 34) |
| `fase3/qwen2.5-coder_3b/L1` | 90 | 66,7% (60) | 27 | 1 | 74,6% (44 de 59) | 51,6% (16 de 31) | 80,4% (45 de 56) | 42,4% (14 de 33) |
| `fase3/qwen2.5-coder_3b/L2` | 90 | 66,7% (60) | 28 | 0 | 78,7% (48 de 61) | 41,4% (12 de 29) | 81,7% (49 de 60) | 34,5% (10 de 29) |
| `fase3/qwen2.5-coder_3b/L3` | 90 | 67,8% (61) | 26 | 0 | 77,4% (48 de 62) | 46,4% (13 de 28) | 84,5% (49 de 58) | 37,5% (12 de 32) |
| `fase3/qwen2.5-coder_7b/L0` | 90 | 71,1% (64) | 24 | 0 | 83,1% (49 de 59) | 48,4% (15 de 31) | 80,3% (49 de 61) | 50,0% (14 de 28) |
| `fase3/qwen2.5-coder_7b/L1` | 90 | 74,4% (67) | 25 | 0 | 86,0% (49 de 57) | 54,5% (18 de 33) | 86,0% (49 de 57) | 54,5% (18 de 33) |
| `fase3/qwen2.5-coder_7b/L2` | 90 | 73,3% (66) | 25 | 0 | 86,0% (49 de 57) | 51,5% (17 de 33) | 87,5% (49 de 56) | 48,5% (16 de 33) |
| `fase3/qwen2.5-coder_7b/L3` | 90 | 72,2% (65) | 26 | 0 | 82,1% (46 de 56) | 55,9% (19 de 34) | 85,5% (47 de 55) | 50,0% (17 de 34) |
| `fase3/qwen2.5_7b/L0` | 90 | 71,1% (64) | 29 | 1 | 81,4% (48 de 59) | 51,6% (16 de 31) | 80,0% (48 de 60) | 51,7% (15 de 29) |
| `fase3/qwen2.5_7b/L1` | 90 | 76,7% (69) | 28 | 0 | 89,3% (50 de 56) | 55,9% (19 de 34) | 82,0% (50 de 61) | 65,5% (19 de 29) |
| `fase3/qwen2.5_7b/L2` | 90 | 74,4% (67) | 28 | 0 | 87,5% (49 de 56) | 52,9% (18 de 34) | 81,7% (49 de 60) | 60,0% (18 de 30) |
| `fase3/qwen2.5_7b/L3` | 90 | 77,8% (70) | 29 | 0 | 85,7% (48 de 56) | 64,7% (22 de 34) | 80,3% (49 de 61) | 72,4% (21 de 29) |
| `fase3b_ineditos/qwen2.5-coder_3b/L0` | 36 | 58,3% (21) | 22 | 1 | 69,6% (16 de 23) | 38,5% (5 de 13) | 72,7% (16 de 22) | 35,7% (5 de 14) |
| `fase3b_ineditos/qwen2.5-coder_3b/L1` | 36 | 58,3% (21) | 23 | 2 | 69,6% (16 de 23) | 38,5% (5 de 13) | 72,7% (16 de 22) | 35,7% (5 de 14) |
| `fase3b_ineditos/qwen2.5-coder_3b/L3` | 36 | 58,3% (21) | 21 | 1 | 72,7% (16 de 22) | 35,7% (5 de 14) | 69,6% (16 de 23) | 38,5% (5 de 13) |
| `fase3b_ineditos/qwen2.5_7b/L0` | 36 | 75,0% (27) | 25 | 0 | 82,6% (19 de 23) | 61,5% (8 de 13) | 90,5% (19 de 21) | 53,3% (8 de 15) |
| `fase3b_ineditos/qwen2.5_7b/L1` | 36 | 72,2% (26) | 24 | 0 | 78,3% (18 de 23) | 61,5% (8 de 13) | 78,3% (18 de 23) | 61,5% (8 de 13) |
| `fase3b_ineditos/qwen2.5_7b/L3` | 36 | 80,6% (29) | 25 | 0 | 83,3% (20 de 24) | 75,0% (9 de 12) | 76,9% (20 de 26) | 90,0% (9 de 10) |
| `fase3b_cruzada_qwen/qwen2.5-coder_3b/L1` | 36 | 61,1% (22) | 17 | 0 | 68,2% (15 de 22) | 50,0% (7 de 14) | 88,2% (15 de 17) | 36,8% (7 de 19) |
| `fase3b_cruzada_qwen/qwen2.5-coder_3b/L3` | 36 | 61,1% (22) | 18 | 1 | 66,7% (16 de 24) | 50,0% (6 de 12) | 88,9% (16 de 18) | 33,3% (6 de 18) |
| `fase3b_cruzada_qwen/qwen2.5-coder_7b/L1` | 36 | 83,3% (30) | 21 | 0 | 90,9% (20 de 22) | 71,4% (10 de 14) | 95,5% (21 de 22) | 64,3% (9 de 14) |
| `fase3b_cruzada_qwen/qwen2.5-coder_7b/L3` | 36 | 83,3% (30) | 20 | 0 | 91,7% (22 de 24) | 66,7% (8 de 12) | 92,0% (23 de 25) | 63,6% (7 de 11) |
<!-- /tabela:tb_atlas_fatias -->

### 3.3 Leitura

1. **A busca separa as classes bem acima do acaso, e isso se repete fora da amostra.** Só pelos três verbetes entregues, o atlas acerta a classe do caso em bem mais da metade dos casos oficiais, contra um acaso de um sexto, e a taxa se mantém nos casos inéditos (tabela `tb_atlas_validacao`). Parte disso está embutida no desenho da biblioteca, que tem um verbete de erro por causa.
2. **Os verbetes que o modelo escreveu não são entregues pela busca.** Na tabela `tb_atlas_verbetes`, todos os verbetes da pasta `aprendidos` aparecem com zero casos. O mesmo vale para as outras bibliotecas e para os casos inéditos e da troca cruzada (tabela `tb_atlas_bibliotecas`, coluna dos nunca recuperados, que cresce junto com os verbetes novos). O ganho medido com a biblioteca do modelo vem das notas que ele acrescentou a verbetes que já existiam.
3. **O acerto do modelo acompanha a rota.** Em todas as corridas da tabela `tb_atlas_fatias`, o modelo acerta mais quando a rota aponta a classe do caso do que quando não aponta. A busca funciona como teto do diagnóstico, o que a análise da Fase 3 já indicava por outro caminho.
4. **Há um sinal calculável sem gabarito.** Quando a causa respondida é de uma classe que a rota aponta, o acerto é maior do que quando é de outra classe, em quase todas as corridas (tabela `tb_atlas_fatias`, duas últimas colunas). A diferença é grande nos modelos menores e menor no modelo decidido, e numa das corridas de casos inéditos ela se inverte, com poucos casos. É candidato a regra de "peça revisão humana" na Fase 4, a decidir junto com a probabilidade do rótulo (corrida 12).
5. **O que o desenho não diz.** A posição de cada verbete no mapa é a média das âncoras das classes ponderada pela afinidade medida. Não é semelhança de significado, e o atlas não descreve o interior do modelo.

A aba Atlas do painel traz o mapa interativo, o detalhe de cada verbete, a rota de cada caso e as trocas entre causas.

## 4. Raciocínio aberto

### 4.1 Trilha e relatório: o protótipo sobre as corridas gravadas

O desenho separa três camadas que nunca se misturam: o que o programa fez (fato), o que o modelo declarou (alegação, sempre como trecho literal da resposta) e o que o código conferiu de cada declaração. A trilha é o arquivo bruto, uma linha JSON por evento (`trilha.py`); o relatório para humanos sai por script só da trilha, sem segunda chamada a modelo, e mostra a resposta certa numa seção só (`gerar_relatorio_raciocinio.py`). O protótipo remonta a trilha de corridas já gravadas, sem rodar modelo, e diz até onde o prompt remontado está provado.

<!-- tabela:tb_rac_corridas -->
| Trilha (corrida, modelo, biblioteca) | Diagnósticos | Sem raciocínio antes das quatro linhas | Prompt inteiro provado | Só a documentação provada | Não comprovado | Acerto quando algum verbete do contexto trata da causa respondida | Acerto quando nenhum trata |
|---|---|---|---|---|---|---|---|
| `fase3`, `qwen2.5:7b`, L1 | 90 | 90 | 54 | 36 | 0 | 78,3% (65 de 83) | 57,1% (4 de 7) |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | 36 | 36 | 0 | 36 | 0 | 71,9% (23 de 32) | 75,0% (3 de 4) |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | 36 | 36 | 0 | 36 | 0 | 77,8% (21 de 27) | 11,1% (1 de 9) |
<!-- /tabela:tb_rac_corridas -->

O que o código confere sem usar o gabarito, por corrida:

<!-- tabela:tb_rac_conferencias -->
| Trilha | Conferência (sem usar o gabarito) | Confere | Não confere | Não se aplica | Não verificável ou informativo |
|---|---|---|---|---|---|
| `fase3`, `qwen2.5:7b`, L1 | A resposta tem as quatro linhas pedidas | 90 | 0 | 0 | 0 |
| `fase3`, `qwen2.5:7b`, L1 | A causa está entre as permitidas | 89 | 1 | 0 | 0 |
| `fase3`, `qwen2.5:7b`, L1 | O verbete citado existe na biblioteca | 117 | 0 | 0 | 0 |
| `fase3`, `qwen2.5:7b`, L1 | O verbete citado estava no contexto entregue ao modelo | 117 | 0 | 0 | 0 |
| `fase3`, `qwen2.5:7b`, L1 | O campo apontado aparece no caso | 53 | 0 | 37 | 0 |
| `fase3`, `qwen2.5:7b`, L1 | Algum verbete do contexto trata da causa respondida | 83 | 7 | 0 | 0 |
| `fase3`, `qwen2.5:7b`, L1 | Notas escritas pelo modelo nos verbetes citados | 0 | 0 | 0 | 90 |
| `fase3`, `qwen2.5:7b`, L1 | Frase de impacto | 0 | 0 | 0 | 90 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | A resposta tem as quatro linhas pedidas | 36 | 0 | 0 | 0 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | A causa está entre as permitidas | 36 | 0 | 0 | 0 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | O verbete citado existe na biblioteca | 43 | 0 | 0 | 0 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | O verbete citado estava no contexto entregue ao modelo | 43 | 0 | 0 | 0 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | O campo apontado aparece no caso | 23 | 0 | 13 | 0 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | Algum verbete do contexto trata da causa respondida | 32 | 4 | 0 | 0 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | Notas escritas pelo modelo nos verbetes citados | 0 | 0 | 0 | 36 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | Frase de impacto | 0 | 0 | 0 | 36 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | A resposta tem as quatro linhas pedidas | 36 | 0 | 0 | 0 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | A causa está entre as permitidas | 36 | 0 | 0 | 0 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | O verbete citado existe na biblioteca | 36 | 0 | 2 | 0 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | O verbete citado estava no contexto entregue ao modelo | 36 | 0 | 2 | 0 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | O campo apontado aparece no caso | 19 | 2 | 15 | 0 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | Algum verbete do contexto trata da causa respondida | 27 | 9 | 0 | 0 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | Notas escritas pelo modelo nos verbetes citados | 0 | 0 | 2 | 34 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | Frase de impacto | 0 | 0 | 0 | 36 |
<!-- /tabela:tb_rac_conferencias -->

E a avaliação contra o gabarito, com o cruzamento que interessa à Fase 4: o acerto quando algum verbete do contexto trata da causa respondida e quando nenhum trata.

<!-- tabela:tb_rac_avaliacao -->
| Trilha | Pergunta (com o gabarito) | Confere | Não confere |
|---|---|---|---|
| `fase3`, `qwen2.5:7b`, L1 | A causa respondida é a esperada | 69 | 21 |
| `fase3`, `qwen2.5:7b`, L1 | O campo respondido é o esperado | 67 | 23 |
| `fase3`, `qwen2.5:7b`, L1 | O verbete da causa esperada estava no contexto | 70 | 20 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | A causa respondida é a esperada | 26 | 10 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | O campo respondido é o esperado | 31 | 5 |
| `fase3b_ineditos`, `qwen2.5:7b`, L1 | O verbete da causa esperada estava no contexto | 24 | 12 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | A causa respondida é a esperada | 22 | 14 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | O campo respondido é o esperado | 25 | 11 |
| `fase3b_cruzada_qwen`, `qwen2.5-coder:3b`, L1 do `qwen2.5:7b` | O verbete da causa esperada estava no contexto | 30 | 6 |
<!-- /tabela:tb_rac_avaliacao -->

Duas leituras já são seguras. Nenhum diagnóstico das corridas remontadas traz raciocínio escrito antes das quatro linhas da resposta (tabela `tb_rac_corridas`), nem do `qwen2.5:7b` nem do `qwen2.5-coder:3b`: o que há para abrir é o que o programa fez e o que o código confere, não uma cadeia de raciocínio do modelo. E a conferência "a causa respondida é tratada por algum verbete do contexto" separa acerto de erro sem precisar do gabarito na corrida oficial do `qwen2.5:7b` e, com muito mais força, no `qwen2.5-coder:3b` da troca cruzada; nos casos inéditos do `qwen2.5:7b` ela não separa, com só 4 casos no grupo sem verbete (tabela `tb_rac_corridas`, duas últimas colunas).

### 4.2 Sonda de confiança (corrida 12, pendente)

O Ollama instalado devolve a probabilidade de cada token que o modelo escreve, medida antes da temperatura (sonda `sondar_logprobs.py`). A corrida 12 grava essa probabilidade para o rótulo de cada um dos 72 casos que nenhuma biblioteca viu, e a análise dirá se ela separa acerto de erro melhor do que os dois sinais calculáveis sem gabarito que já existem (seções 3.3 e 4.1). A corrida depende de uma noite combinada com o Eric.

### 4.3 Literatura (parte B da rodada 5, pendente)

Seis tópicos: se o raciocínio escrito é o que decidiu a resposta, formatos de trilha e exigências de registro, relatório de raciocínio para quem desenvolve, atribuição ao contexto, probabilidade do rótulo como sinal e uso das trilhas para melhorar o sistema. Entram como §6.14.6 a §6.14.11 do levantamento, e a especificação do que a Fase 4 emite em cada passo é fechada depois deles.

## 5. O que já se pode levar para o plano da Fase 4 (provisório)

- Emitir a trilha em três camadas a cada diagnóstico, no formato já usado pelo protótipo, e gerar dela o relatório por caso.
- Fazer em código, a cada diagnóstico, as conferências que não dependem do gabarito (tabela `tb_rac_conferencias`).
- Avaliar, como regras de "peça revisão humana", os sinais calculáveis sem gabarito: a causa respondida ser tratada por um verbete do contexto, a causa respondida ser de uma classe que a rota aponta e, depois da corrida 12, a probabilidade do rótulo.
- Rever o lugar dos verbetes novos escritos pelo modelo: como a busca não os entrega, eles só aumentam a biblioteca.

Nada disto é decisão: são candidatos, a decidir no plano da Fase 4 com a parte B da pesquisa e a corrida 12 em mãos.

## 6. Limitações

- A conta de viabilidade usa as medidas que o repositório publica, feitas em máquinas de terceiros e com outro modelo; a medição nesta máquina é a da corrida 13, e só com o modelo pequeno.
- O atlas descreve a busca e o uso do contexto. Parte da afinidade vem do desenho da biblioteca, e os cruzamentos por corrida têm poucos casos nas corridas de 36.
- As trilhas das corridas gravadas são remontadas: o prompt não foi gravado na época, e o relatório diz até onde a remontagem está provada. Nas corridas novas o hash do prompt enviado fica gravado.
- A parte B da pesquisa ainda não rodou; o que este relatório diz sobre o raciocínio aberto vem dos dados do projeto, não da literatura.
<!-- ! Alteração de IA - Revisar: (05/10/2026) limitação nova e linha de rastreabilidade sobre a revisão das sínteses da parte A; duas células da tabela 2.3 refeitas.
     ! Motivo: seis revisores conferiram as sínteses contra as afirmações verificadas e apontaram 104 trechos (quase todos frase mais forte que a fonte); as correções entraram por script, declaradas no levantamento (§6.14.12), e as duas células repetiam frases corrigidas ("o limite é a RAM"; escritas do cache KV lidas como se fossem dos pesos). -->
- As sínteses da parte A passaram por revisão contra as afirmações verificadas (um revisor por tópico e um para o mapa): 104 apontamentos, quase todos frase mais forte que a fonte, viraram 156 correções declaradas no levantamento (§6.14.12, com o trecho antigo, o novo e o motivo de cada uma). O texto corrigido continua sendo texto de agente sobre fontes verificadas por agente; o que a revisão não cobre é a leitura das fontes em si.

## 7. Rastreabilidade

| O quê | Onde |
|---|---|
| Conta de viabilidade | `resultados_alvo/pre_fase4/viabilidade_modelos_grandes.json` e `.md` (`viabilidade_modelos_grandes.py`); disco em `disco.json` (`ferramentas/medir_disco.py`) |
| Amostra de probabilidades por token | `resultados_alvo/pre_fase4/logprobs_amostra__*.json` (`sondar_logprobs.py`) |
| Atlas | `resultados_alvo/pre_fase4/atlas.json` e `atlas.md` (`gerar_atlas.py`); aba Atlas do painel (`ferramentas/painel_atlas.py`) |
| Trilhas e relatórios de caso | `resultados_alvo/pre_fase4/trilhas/`, `relatorios/` e `indicadores_raciocinio.json` (`trilha.py`, `gerar_relatorio_raciocinio.py`) |
| Literatura | [levantamento da Pré-Fase 4](../2-pesquisa-e-literatura/levantamento-2026-10-01-pre-fase-4.md) (§6.14) e [referencias.md](../2-pesquisa-e-literatura/referencias.md) |
| Correções da revisão das sínteses | `ferramentas/correcoes_pesquisa_pre_fase4.py` (156 trechos, aplicados por `integrar_pesquisa_pre_fase4.py` e listados no fim do §6.14.12); os relatórios dos revisores ficam em `.superpowers/sdd/pre-fase-4/pesquisa/revisao/` (fora do git) |
| Testes | `testar_pre_fase4.py` e `ferramentas/testar_integrar_pesquisa_pre_fase4.py`, `ferramentas/testar_painel_topicos.py` |
| Decisão e plano | decisão 70; `claude-memoria/plano-aprovado-pre-fase-4.md`; roadmap §3.1 |
