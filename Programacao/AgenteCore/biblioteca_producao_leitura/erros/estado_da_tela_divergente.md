---
# ! Alteração de IA - Revisar: camada de leitura do verbete `estado_da_tela_divergente`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/estado_da_tela_divergente.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 3 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas; a nota chamava as épocas de "treinamento"; neste projeto o modelo não é treinado: época é a rodada em que ele propôs acréscimos à biblioteca; a nota retirada continua no verbete que o modelo lê.
id: estado_da_tela_divergente
titulo: Estado da tela divergente da resposta
sistema: CobaiaFront
entidade_principal: Interface
tipo: erro
status: ativo
causa_raiz: estado_da_tela_divergente
arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaFront/cliente/reserva_cli.php]
sintomas: [api respondeu certo mas a tela nao, carregando parado, lista vazia com resposta cheia, botao continua habilitado apos cancelar, carregando..., lista vazia, botao inativo]
palavras_chave: [tela, estado, divergente, render, renderiza, atualiza, recarregar, filtro, ordem aleatoria, carregando, innerHTML, fetch, redirect]
causas_relacionadas: [localizador_quebrado, dado_desatualizado, corpo_vazio]
verbete: erros/estado_da_tela_divergente.md
hash_do_verbete: a78a9187968f5cdd
gerado_em: 2026-11-07
curado: sim
---

# Estado da tela divergente da resposta

Camada de leitura do verbete `estado_da_tela_divergente` (`biblioteca_producao/erros/estado_da_tela_divergente.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: CobaiaFront (o site PHP); entidade principal: Interface. Trata da causa `estado_da_tela_divergente` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

A rede está certa: status e corpo conferem: e o usuário vê outra coisa: "Carregando" parado, lista vazia, botão que não muda.

## Como aparece na tela

- nenhum erro de console nem status de erro.
- recarregar corrige: o estado não foi atualizado.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `api respondeu certo mas a tela nao`, `carregando parado`, `lista vazia com resposta cheia`, `botao continua habilitado apos cancelar`, `carregando...`, `lista vazia`, `botao inativo`.

## O que conferir

Causa, como o verbete a descreve: produtos_api.php só limpa "Carregando..." no then() do fetch e substitui o grid por innerHTML; na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7).

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `localizador_quebrado` (Localizador (seletor) quebrado), `dado_desatualizado` (Dado desatualizado (cache)), `corpo_vazio` (Corpo vazio).

## Onde está no código

- Arquivos: `Programacao/CobaiaFront/produtos_api.php`, `Programacao/CobaiaFront/cliente/reserva_cli.php`.
- Rotas da API: nenhuma declarada.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `tela`, `estado`, `divergente`, `render`, `renderiza`, `atualiza`, `recarregar`, `filtro`, `ordem aleatoria`, `carregando`, `innerHTML`, `fetch`, `redirect`.

## Notas do modelo

O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/erros/estado_da_tela_divergente.md`.

## Curadoria

Leitura revisada e aprovada. Descrição conceitual precisa sobre falhas de atualização de interface após respostas assíncronas em rede bem-sucedidas. A nota do modelo (época 101), escrita como instrução, foi retirada desta leitura; continua no verbete que o modelo lê.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 3 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
