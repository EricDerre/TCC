---
# ! Alteração de IA - Revisar: camada de leitura do verbete `contrato-pedido`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/contratos/contrato-pedido.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 3 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas; a nota chamava as épocas de "treinamento"; neste projeto o modelo não é treinado: época é a rodada em que ele propôs acréscimos à biblioteca; a nota retirada continua no verbete que o modelo lê.
id: contrato-pedido
titulo: Contrato de /api/pedidos
sistema: CobaiaAPI
entidade_principal: Pedido
tipo: contrato
status: ativo
arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/schemas.py, Programacao/CobaiaFront/cliente/index.php]
endpoints: [GET /api/pedidos, POST /api/pedidos, POST /api/pedidos/{id}/cancelar]
tabelas: [tbpedido_reserva, tbusuarios]
sintomas: [data em outro formato, status desconhecido, 422 sem login, cliente nao encontrado, duas reservas iguais apos um unico post, registros com id consecutivo]
palavras_chave: [contrato, pedidos, reservas, login, cpf, id_pedido, pessoas, data_pedido, status, nome, 201, 404, 422, cancelar, post duplo, registros duplicados]
causas_relacionadas: [formato_de_data_divergente, valor_fora_do_dominio, recurso_inexistente, campo_ausente]
verbete: contratos/contrato-pedido.md
hash_do_verbete: 98b81ea8a09c0d3c
gerado_em: 2026-11-07
curado: sim
---

# Contrato de /api/pedidos

Camada de leitura do verbete `contrato-pedido` (`biblioteca_producao/contratos/contrato-pedido.md`). Tipo: contrato (o contrato de uma rota da API, campo a campo); estado: ativo (em vigor); sistema: CobaiaAPI (a API); entidade principal: Pedido.

## O que é

GET /api/pedidos?login=<cpf>; POST /api/pedidos {id_clientes, pessoas, data_pedido} leva a 201; POST /api/pedidos/{id}/cancelar. Campos: id_pedido, pessoas, data_pedido AAAA-MM-DD, status 'Em Análise'|'Cancelado', nome, cpf.

## Como aparece na tela

- data noutro formato ou como número.
- status fora dos dois valores.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `data em outro formato`, `status desconhecido`, `422 sem login`, `cliente nao encontrado`, `duas reservas iguais apos um unico post`, `registros com id consecutivo`.

## O que conferir

Causa, como o verbete a descreve: cpf vem de login_usuario (pedidos.py). Busca exata na API; o site usa LIKE '%login%' (cliente/index.php:4).

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `formato_de_data_divergente` (Formato de data divergente), `valor_fora_do_dominio` (Valor fora do domínio), `recurso_inexistente` (Recurso inexistente (404 e vizinhos)), `campo_ausente` (Campo ausente).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/routers/pedidos.py`, `Programacao/CobaiaAPI/app/schemas.py`, `Programacao/CobaiaFront/cliente/index.php`.
- Rotas da API (campo `endpoints`): `GET /api/pedidos`, `POST /api/pedidos`, `POST /api/pedidos/{id}/cancelar`.
- Tabelas do banco: `tbpedido_reserva`, `tbusuarios`.
- Palavras que a busca usa para achar este verbete: `contrato`, `pedidos`, `reservas`, `login`, `cpf`, `id_pedido`, `pessoas`, `data_pedido`, `status`, `nome`, `201`, `404`, `422`, `cancelar`, `post duplo`, `registros duplicados`.

## Notas do modelo

O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/contratos/contrato-pedido.md`.

## Curadoria

Leitura revisada e aprovada. Especificação do contrato mantida integralmente. A nota do modelo sobre registros duplicados no POST foi retirada desta leitura, porque repete o que a causa `registro_duplicado` já trata; continua no verbete que o modelo lê.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 3 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
