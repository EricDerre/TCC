---
# ! Alteração de IA - Revisar: camada de leitura do verbete `recurso_inexistente`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/recurso_inexistente.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 4 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas; o termo continuava sem o significado na primeira menção, e os filtros de texto do pacote Q2 seguiam reprovando a leitura; a nota não dizia que o texto do modelo saiu só desta leitura e continua no verbete que o modelo lê; e a nota citava o termo fora de crases, o que fazia a leitura reprovar no mesmo filtro que ela dizia atender.
id: recurso_inexistente
titulo: Recurso inexistente (404 e vizinhos)
sistema: CobaiaAPI
entidade_principal: Infraestrutura
tipo: erro
status: ativo
causa_raiz: recurso_inexistente
arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/routers/admin_fault.py]
endpoints: [GET /api/produtos/{id}, GET /api/pedidos, POST /api/pedidos, POST /api/pedidos/{id}/cancelar]
sintomas: [HTTP 404, Not Found, produto nao encontrado, cliente nao encontrado, pedido nao encontrado, rota errada]
palavras_chave: [404, not found, nao encontrado, inexistente, rota, endpoint, singular, plural, 403, 422, detail, campo de busca errado]
causas_relacionadas: [erro_interno_do_servidor, localizador_quebrado]
verbete: erros/recurso_inexistente.md
hash_do_verbete: 3689832a7012c939
gerado_em: 2026-11-07
curado: sim
---

# Recurso inexistente (404 e vizinhos)

Camada de leitura do verbete `recurso_inexistente` (`biblioteca_producao/erros/recurso_inexistente.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: CobaiaAPI (a API); entidade principal: Infraestrutura. Trata da causa `recurso_inexistente` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

404: id ou rota inexistente. O detail diz qual: "produto não encontrado" (produtos.py:52), "cliente não encontrado" (pedidos.py:37,52), "pedido não encontrado" (pedidos.py:74); "Not Found" genérico é rota inexistente (ex.: /api/produto).

## Como aparece na tela

- id válido e ainda 404: campo de busca errado (login × id).
- vizinhos: 403 no admin sem a chave de acesso (o cabeçalho `X-Admin-Token`); 422 sem login.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `HTTP 404`, `Not Found`, `produto nao encontrado`, `cliente nao encontrado`, `pedido nao encontrado`, `rota errada`.

## O que conferir

Causa, como o verbete a descreve: Cada 404 com mensagem vem de db.get/filter vazio na rota.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `erro_interno_do_servidor` (Erro interno do servidor (500)), `localizador_quebrado` (Localizador (seletor) quebrado).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/routers/produtos.py`, `Programacao/CobaiaAPI/app/routers/pedidos.py`, `Programacao/CobaiaAPI/app/routers/admin_fault.py`.
- Rotas da API (campo `endpoints`): `GET /api/produtos/{id}`, `GET /api/pedidos`, `POST /api/pedidos`, `POST /api/pedidos/{id}/cancelar`.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `404`, `not found`, `nao encontrado`, `inexistente`, `rota`, `endpoint`, `singular`, `plural`, `403`, `422`, `detail`, `campo de busca errado`.

## Notas do modelo

O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/erros/recurso_inexistente.md`.

## Curadoria

Leitura revisada e aprovada. Excelente distinção entre falhas de roteamento genéricas e falhas de query no banco (Not Found vs detail específico). O nome do cabeçalho com a chave de acesso ficou entre crases, para o filtro de termos técnicos do pacote Q2. A nota do modelo, que sugeria uma adição já existente no texto, foi retirada desta leitura; continua no verbete que o modelo lê.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 4 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
