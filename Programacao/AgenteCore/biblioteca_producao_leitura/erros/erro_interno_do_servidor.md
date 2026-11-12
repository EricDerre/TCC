---
# ! Alteração de IA - Revisar: camada de leitura do verbete `erro_interno_do_servidor`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/erro_interno_do_servidor.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 3 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas; a nota chamava as épocas de "treinamento"; neste projeto o modelo não é treinado: época é a rodada em que ele propôs acréscimos à biblioteca; a nota retirada continua no verbete que o modelo lê.
id: erro_interno_do_servidor
titulo: Erro interno do servidor (500)
sistema: Ambos
entidade_principal: Infraestrutura
tipo: erro
status: ativo
causa_raiz: erro_interno_do_servidor
arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/conn/connect.php]
endpoints: [GET /api/produtos, POST /api/pedidos]
sintomas: [HTTP 500, Internal Server Error, fault injection error_500, falha intermitente]
palavras_chave: [500, erro interno, internal server error, exception, excecao, fault injection, intermitente, banco fora, falha_interna, injetor, excecao_nao_tratada]
causas_relacionadas: [corpo_nao_e_json, tempo_de_resposta_excedido, limite_de_requisicoes]
verbete: erros/erro_interno_do_servidor.md
hash_do_verbete: 12c820719addfcdc
gerado_em: 2026-11-07
curado: sim
---

# Erro interno do servidor (500)

Camada de leitura do verbete `erro_interno_do_servidor` (`biblioteca_producao/erros/erro_interno_do_servidor.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: Ambos (o site PHP e a API); entidade principal: Infraestrutura. Trata da causa `erro_interno_do_servidor` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

500 com {"detail": ...}: falha própria da API. detail "fault injection: error_500 em produto" é o injetor; "Internal Server Error" é exceção não tratada.

## Como aparece na tela

- intermitente sem padrão: injetor com probability < 1.
- em toda requisição: banco inacessível ou defeito na rota.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `HTTP 500`, `Internal Server Error`, `fault injection error_500`, `falha intermitente`.

## O que conferir

Causa, como o verbete a descreve: Rotas convertem ErrorFault em 500 (produtos.py:42). No site PHP, banco fora NÃO dá 500: imprime "Atenção ERRO" em HTML (connect.php:16).

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `corpo_nao_e_json` (Corpo não é JSON), `tempo_de_resposta_excedido` (Tempo de resposta excedido), `limite_de_requisicoes` (Limite de requisições (429)).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/routers/produtos.py`, `Programacao/CobaiaAPI/app/fault_injection.py`, `Programacao/CobaiaFront/conn/connect.php`.
- Rotas da API (campo `endpoints`): `GET /api/produtos`, `POST /api/pedidos`.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `500`, `erro interno`, `internal server error`, `exception`, `excecao`, `fault injection`, `intermitente`, `banco fora`, `falha_interna`, `injetor`, `excecao_nao_tratada`.

## Notas do modelo

O verbete que o modelo lê traz 2 notas do modelo. A curadoria de 10/11/2026 as retirou desta leitura; elas continuam em `biblioteca_producao/erros/erro_interno_do_servidor.md`.

## Curadoria

Leitura revisada e aprovada. Excelente diferenciação entre o erro 500 originado na API e o comportamento do PHP (que não emite 500). As duas notas do modelo (época 1) foram retiradas desta leitura por repetirem o que o texto já diz; continuam no verbete que o modelo lê.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 3 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
