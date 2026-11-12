---
# ! Alteração de IA - Revisar: camada de leitura do verbete `limite_de_requisicoes`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/limite_de_requisicoes.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 3 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas; a nota dizia que a retirada protegia a busca ("RAG", "vetorial", "indexação semântica"), mas a camada de leitura não é buscada nem lida pelo modelo, e a busca deste projeto é por palavras; a nota retirada continua no verbete que o modelo lê.
id: limite_de_requisicoes
titulo: Limite de requisições (429)
sistema: Infraestrutura
entidade_principal: Infraestrutura
tipo: erro
status: ativo
causa_raiz: limite_de_requisicoes
arquivos: [Programacao/CobaiaAPI/app/main.py, Programacao/CobaiaFront/produtos_api.php]
endpoints: [GET /api/produtos]
sintomas: [HTTP 429, too many requests, rate limit, para de funcionar apos varias tentativas]
palavras_chave: [429, limite, rate limit, too many requests, retry_after, cota, excesso, recarregar, status de erro, limitador de requisicoes]
causas_relacionadas: [tempo_de_resposta_excedido, erro_interno_do_servidor]
verbete: erros/limite_de_requisicoes.md
hash_do_verbete: 4f0370a818be0cf3
gerado_em: 2026-11-07
curado: sim
---

# Limite de requisições (429)

Camada de leitura do verbete `limite_de_requisicoes` (`biblioteca_producao/erros/limite_de_requisicoes.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: Infraestrutura (servidor, banco e rede); entidade principal: Infraestrutura. Trata da causa `limite_de_requisicoes` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

Status 429: o servidor ou um intermediário recusou por excesso de requisições num intervalo. Resposta rápida e com corpo: não é lentidão nem erro interno.

## Como aparece na tela

- funciona, depois falha após recarregar muitas vezes.
- "Erro ao carregar produtos da CobaiaAPI: HTTP 429"; pode vir retry_after.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `HTTP 429`, `too many requests`, `rate limit`, `para de funcionar apos varias tentativas`.

## O que conferir

Causa, como o verbete a descreve: A CobaiaAPI não tem limitador (main.py só registra CORS e routers); um 429 vem de proxy, gateway ou servidor diferente do esperado.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `tempo_de_resposta_excedido` (Tempo de resposta excedido), `erro_interno_do_servidor` (Erro interno do servidor (500)).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/main.py`, `Programacao/CobaiaFront/produtos_api.php`.
- Rotas da API (campo `endpoints`): `GET /api/produtos`.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `429`, `limite`, `rate limit`, `too many requests`, `retry_after`, `cota`, `excesso`, `recarregar`, `status de erro`, `limitador de requisicoes`.

## Notas do modelo

O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/erros/limite_de_requisicoes.md`.

## Curadoria

Leitura revisada e aprovada. Conceituação clara sobre a natureza do código HTTP 429 e sua atribuição a intermediários de infraestrutura (proxies/gateways). A nota do modelo (época 101) foi retirada desta leitura; continua no verbete que o modelo lê.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 3 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
