<!-- ! Alteração de IA - Revisar: arquivo novo (27/11/2026): o plano aprovado da coletânea de erros sorteados para a banca (cartão #99 do Kanban do orientador, TSK-POS4-010), com o desenho que o Eric aprovou no quadro (fichas 129 a 132, decisões 193 a 197) e os passos de implementação.
     ! Motivo: o botão do hub roda sempre os mesmos dez cenários, na mesma ordem, e o Eric quer evitar que a banca diga que as rodadas são casos fixos preparados de antemão; o desenho fica congelado aqui antes do código, como nos planos das fases, para a implementação ser conferida contra ele. -->
# Plano aprovado: a coletânea de erros sorteados para a banca

Aprovado pelo Eric em 27/11/2026, no quadro da sessão: as quatro fichas (129 a 132) pelas opções recomendadas e o desenho inteiro com "Aprovado (Recomendado)". Este texto não muda; desvio de implementação entra no anexo, no fim.

## 1. O pedido e o problema

O pedido do Eric (27/11/2026): "vamos fazer uma coletanea de erros que ocorrerão "aleatoriamente" durante as rodadas, para evitarem falar que são apenas casos pré determinados que rodam ali (uma pull de 50 erros acho que está bom - validar esse número)".

Hoje o botão "Ativar o agente e rodar os cenários" do hub (`hub.py`, `comando_direto`) chama `executar_fase4.py --modo cenarios --casos 10`, que roda `cenarios_fase4.CENARIOS_DO_ENSAIO`: os mesmos dez cenários da medida da Fase 5, sempre na mesma ordem.

## 2. O número, validado por script

Contas feitas em 27/11/2026 sobre os registros versionados (scripts de conta na pasta de rascunho da sessão; os números abaixo são a saída deles):

- **O que já existe, provado em corrida:** 41 combinações de página, modo de injeção e campo que a tela reproduziu na corrida 17 (`resultados_alvo/fase4_reproducao/reproducao.jsonl` e `fase4_reproducao_ineditos/reproducao.jsonl`), mais o `field_renamed` em `preco` da corrida 28b (`fase5_agente_b/cenarios.jsonl`, 5 de 5): 42 erros de contrato. E as 16 quebras de localizador (4 roteiros do front vezes 4 modos), curadas na corrida 19 (`fase4_cura/cura.jsonl`, 160 de 160). Total: 58 erros distintos, sem nenhum modo de injeção novo.
- **Gabarito:** nenhuma das 41 combinações tem duas causas nos casos gravados; a causa é sempre a do modo.
- **Por classe:** léxica 8, sintática 11, semântica 11, tradução 5, runtime 6, efeito 17 (16 de localizador e 1 de contrato).
- **Acerto do agente na tela, na medida:** a causa certa em 54 de 62 casos (corridas 18d e 18 dos inéditos); 4 combinações ele errou sempre.
- **O tamanho não impede repetição; o jeito de sortear impede.** Sorteando de novo a cada rodada, os 58 dão 37% de chance de repetir algum erro em duas rodadas de 5, e 87% em duas de 10; mesmo 200 erros dariam 41% em duas de 10. Embaralhando uma vez e tirando da pilha, nada se repete até a pilha acabar.
- **Tempo:** 81 s por caso nas corridas do botão (`resultados_alvo/fase4/botao_do_hub.md`); rodada de 5 em cerca de 7 min; a pilha inteira de 64 cartas em cerca de 86 min.
- **Mistura:** numa rodada de 5 tirada dos 58, há 4.582.116 rodadas possíveis, e 81% delas misturam contrato e tela.

Conclusão: 50 bastaria em tamanho, mas os 58 provados entram todos, porque cortar 8 seria escolher quem fica de fora.

## 3. O que o Eric decidiu

| Ficha | Pergunta | Resposta |
|---|---|---|
| 129 | Quantos erros e de onde | Os 58 provados, inclusive os 4 que o agente errou na medida |
| 130 | Como o sorteio funciona | Pilha embaralhada pelo número dito pela banca (sem número, a hora do clique), gravada antes do primeiro erro, refeita por comando |
| 131 | Rodadas sem erro | Sim: 6 cartas sem erro, uma por página; o certo é não acusar nada |
| 132 | O que a banca vê e quando | O erro sorteado fica escondido até o agente responder; depois, o cartão lado a lado com o que foi ligado e o que o agente disse |

## 4. O desenho

### 4.1 A coletânea (`Programacao/AgenteCore/experimentos/coletanea.py`, arquivo novo)

- **64 cartas em dados**, no mesmo formato dos cenários do ensaio (`id`, `tipo`, `cenario`, `modo`, `campo`, `causa`, `classe`, `nivel`, `forma`, `produto_id`, `requisicao`, `prova`, `medido_na_fase_5`), para o executor usar a carta como usa um cenário de hoje:
  - 42 de contrato (`tipo` "contrato"): página (`api-catalogo` ou `api-detalhe`), modo, campo, a causa certa, a classe e o nível do caso que provou, o produto (no detalhe) e a prova (corrida e caso).
  - 16 de localizador (`tipo` "localizador"): roteiro do front, modo de quebra, forma "harness", causa `localizador_quebrado`, classe 6, nível 2; prova na corrida 19.
  - 6 sem erro (`tipo` "sem_erro"): uma por página (catálogo, detalhe e os quatro roteiros do front), modo "normal", sem causa; prova na linha "referência ...: passou" do `fase4.log` das corridas 17 e 19.
- **Gabarito pela construção:** a causa é a do modo (o inverso de `cenarios_fase4.MODO_POR_CAUSA`); o campo certo é o que a API altera (o pedido, ou o padrão do modo em `CAMPO_PADRAO` da API), e nenhum nos modos que trocam a resposta ou a lista inteira (`MODOS_DE_RESPOSTA`, e `contagem_inconsistente` e `registro_duplicado` de `MODOS_DE_LISTA`). A conferência lê `CAMPO_PADRAO`, `MODOS_DE_LISTA` e `MODOS_DE_RESPOSTA` do próprio `CobaiaAPI/app/fault_injection.py`, pelo `ast`, sem importar a API.
- **Conferência em código** (`validar`): recusa carta com modo, campo, página ou roteiro que não existem, gabarito que não bate com o modo, carta repetida, e prova que não está nos registros versionados (ou que não reproduziu, não curou, ou tem outro modo, campo ou causa).
- **Os dez da medida** ficam marcados (`medido_na_fase_5`), lidos de `cenarios_fase4.CENARIOS_DO_ENSAIO`, nunca digitados.
- **Código da coletânea** (`hash_da_coletanea`): SHA-256 do conteúdo das 64 cartas; vai em cada sorteio.
- **Nome em palavras** de cada modo (`descricao`), para o cartão do hub.

### 4.2 O sorteio

- **A pilha:** cada carta recebe o SHA-256 de `"<número>|<id da carta>"`; a pilha é a ordem desses códigos. Sem o `random` do Python, para refazer em qualquer máquina e linguagem.
- **A rodada** tira as próximas 3, 5 ou 10 cartas (padrão 5) a partir de onde a pilha daquele número parou. Número novo, pilha nova. Pilha no fim: tira o que sobrou; pilha vazia: recusa e pede um número novo.
- **O número:** só algarismos, de 1 a 18; sem número, vale a hora do clique (`AAAAMMDDhhmmss`), com a origem "relógio".
- **O registro, antes de ligar o primeiro erro:** `sorteio.json` na pasta da corrida e uma linha em `resultados_alvo/hub/sorteios.jsonl` (só acréscimo, entra no git, como `commits_testados.jsonl`): quando, corrida, número, origem, código da coletânea, posição, quantas e as cartas. A posição seguinte sai desse arquivo (a última linha com o mesmo número e o mesmo código), sem outro estado guardado. Relançar a mesma pasta reaproveita o `sorteio.json` dela.
- **O comando que refaz:** `python coletanea.py --sortear --numero <N> --quantas <k> --posicao <p>`.

### 4.3 O executor (`executar_fase4.py`, modo `cenarios`)

- Opção nova `--coletanea`, com `--numero` e `--quantas`, desligada por padrão. Sem ela, os dez da medida rodam como hoje.
- Com ela: a corrida é parcial (uso do produto, não medida); as execuções são as cartas sorteadas, com nome neutro (`carta-07#1`), porque o nome do caso aparece na barra de progresso do hub (`diagnostico_ao_vivo.inferir`). O nome nunca vai ao prompt: `estrategias._dados_do_caso` usa só requisição, status, contrato, corpo, árvore, seletor, sintoma e observação.
- Contrato: o caminho dos seis de hoje (`Tela.rodar_caso` e o diagnóstico ao vivo), agora também na página do detalhe, com o produto e a requisição da carta.
- Localizador: o caminho dos quatro de hoje (`Cura.executar`).
- Sem erro: no catálogo e no detalhe, o caminho do contrato com o modo "normal"; no front, o roteiro sem quebra (`Cura.executar_sem_quebra`). O certo é não detectar; se detectar, no contrato o agente diagnostica como em qualquer detecção, e no front a corrida só grava a falha acusada.
- `registro_do_cenario`: na carta sem erro, Task Success é não ter detectado nada.
- O agente medido não muda: `diagnostico_ao_vivo`, a biblioteca de produção, o prompt e a cura ficam como estão. As condições da corrida gravam o sorteio, o código do prompt fixo e o da biblioteca.

### 4.4 O hub

- "O que rodar" ganha a terceira opção, "erros sorteados da coletânea", com dois campos: "Quantos casos" (3, 5, 10) e "Número da banca" (só algarismos; vazio, vale a hora do clique), cada um com a explicação. A coletânea roda só pelo hub aberto pelo `Cobaia.exe` (o site e a API no ar); fora dele, a página mostra o comando direto para a janela de quem roda.
- Na "Corrida ao vivo", quando a corrida é da coletânea: o número, a origem, a posição na pilha e quantas cartas faltam; a grade das 64 cartas por grupo (léxica, sintática, semântica, tradução, runtime, efeito, sem erro), com as tiradas em rodadas anteriores do mesmo número e as já reveladas acesas (as escondidas da rodada não acendem, para a grade não entregar o erro); um cartão por carta da rodada, "escondida" até a resposta, e depois lado a lado o que foi ligado (o modo em palavras, campo, página e a causa certa) e o que o agente disse, com acertou ou errou (no localizador, também se a cura fez o roteiro voltar a passar; na carta sem erro, se nada foi acusado); ao fim, a lista inteira e o comando que refaz; e a frase "mesmo agente da medida", conferida pelos códigos do prompt fixo e da biblioteca contra os da corrida 28b.
- A página não recebe o nome das cartas escondidas.

### 4.5 Testes e o que fica para o Eric

- `testar_coletanea.py` (novo), acréscimos em `testar_fase4.py` e em `testar_central.py`; sem modelo, sem cobaias, sem banco.
- A prova com o modelo: uma rodada de 5 pelo botão, aberta pelo `Cobaia.exe`, na janela do Eric (nunca de dentro do aplicativo Claude).
- Memorial: fichas 129 a 132 e decisões 193 a 197, linha no roadmap, painel regerado e republicado, aviso à sessão principal para o cartão #99.

O que não muda: os dez cenários da medida, as corridas 17 a 28b e os números do TCC.

## 5. Passos de implementação

Restrições de todos os passos: só biblioteca padrão (`.claude/rules/experimentos.md`); PEP8 em português; tag `! Alteração de IA - Revisar` com `! Motivo:` em todo trecho novo ou alterado; testes em Python puro, `teste_<nome>()`, runner que termina em `N testes ok`, escritos antes do código (vermelho pelo motivo certo); rodar com `PYTHONIOENCODING=utf-8` e o Python de `Programacao/AgenteCore/.venv`; nada commitado.

1. **`coletanea.py` e `testar_coletanea.py`.** Interfaces que os passos seguintes usam: `cartas() -> list[dict]`, `carta(id_) -> dict`, `validar(cartas_=None, raiz=EXP) -> list[str]`, `hash_da_coletanea(cartas_=None) -> str`, `ordem_da_pilha(numero, cartas_=None) -> list[str]`, `tirar(numero, posicao, quantas, cartas_=None) -> dict` (`cartas`, `posicao`, `proxima`, `total`, `acabou`), `normalizar_numero(texto) -> str` (ValueError fora da regra), `numero_do_relogio(agora=None) -> str`, `proxima_posicao(numero, registro, codigo=None) -> int`, `sortear(numero, quantas, registro, corrida, origem, quando=None) -> dict`, `gravar_sorteio(sorteio, pasta_da_corrida, registro) -> Path`, `comando_que_refaz(numero, quantas, posicao) -> str`, `descricao(carta_) -> str`, `GRUPOS`, `QUANTAS_PERMITIDAS = (3, 5, 10)`, `ARQUIVO_DO_SORTEIO = "sorteio.json"`, `ARQUIVO_DOS_SORTEIOS = "sorteios.jsonl"`, `PAGINAS_DO_CONTRATO`. Linha de comando: `--listar`, `--conferir`, `--sortear --numero --quantas --posicao`.
2. **Executor.** `executar_fase4.py`: `--coletanea`, `--numero`, `--quantas`; `celulas_da_coletanea(sorteio) -> list[dict]`; o sorteio antes de subir as cobaias, depois das conferências que encerram a corrida cedo; `Cura.executar_sem_quebra` e `Cura.emitir_sem_quebra`; `registro_do_cenario` com a carta sem erro. Testes em `testar_fase4.py`: células com nome neutro, caminho padrão igual, registro da carta sem erro, opções desligadas por padrão.
3. **Hub.** `hub.py`: `SELECOES` com "coletanea", `opcoes_da_corrida` com `quantas` e `numero`, `comando_direto` com as opções da coletânea, recusa fora do `Cobaia.exe` e com a pilha vazia; `hub_dados.coletanea_da_corrida(pasta, registro) -> dict | None`, lida por `AoVivo.ler`; `hub_pagina.py` e `hub_molde.py`: os campos, a grade e os cartões; `prova_do_botao` separando as cartas sem erro. Testes em `testar_central.py`, com a página no Chromium sem janela.
4. **Registro.** Roadmap (§2 e §4.8), anexo deste plano com os desvios, README e `DETALHES-TECNICOS.md` no que mudou no hub, painel regerado e republicado, nota na pasta de notas da sessão principal e mensagem a ela para o cartão #99.

## Anexo: desvios da implementação

<!-- ! Alteração de IA - Revisar: (27/11/2026) desvios 1 e 2, achados durante a implementação.
     ! Motivo: o plano não muda depois de aprovado; o que a implementação fez de diferente fica registrado aqui, com o porquê. -->
1. **O log da corrida fica escondido no hub enquanto uma rodada da coletânea roda** (`hub.Execucao.estado`). O plano não previa isso. O painel "Rodar os cenários" mostra o fim do log da corrida, e o log diz, no começo de cada carta, a página e o produto da referência (por exemplo, "referência api-detalhe produto 11", e só uma carta usa o produto 11) e, no fim dela, o modo ligado. Com o log na tela, a banca veria o erro antes da resposta, contra a decisão 196. Terminada a rodada, o log volta. Também saiu do log do começo da rodada o comando que refaz o sorteio: com ele, a lista poderia ser refeita antes do fim.
2. **O resumo das corridas do botão (`hub.py --botao`) conta "a falha foi detectada" só nas cartas com erro** e, na rodada da coletânea, diz o número e quantas cartas sem erro passaram sem nada acusado. O plano já previa separar as cartas sem erro; o desvio é só o jeito: as corridas dos dez cenários saem iguais, sem chave nova, e o `--check` do `botao_do_hub.json` gravado continua batendo.

O ruff não está instalado nesta máquina e não rodou nos arquivos novos.
