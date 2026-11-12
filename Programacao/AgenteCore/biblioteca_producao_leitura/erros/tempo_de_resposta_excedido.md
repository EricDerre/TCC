---
# ! Alteração de IA - Revisar: camada de leitura do verbete `tempo_de_resposta_excedido`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/tempo_de_resposta_excedido.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
id: tempo_de_resposta_excedido
titulo: Tempo de resposta excedido
sistema: Ambos
entidade_principal: Infraestrutura
tipo: erro
status: ativo
causa_raiz: tempo_de_resposta_excedido
arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php]
endpoints: [GET /api/produtos]
sintomas: [demora de segundos, timeout, conexao encerrada por tempo, carregando por muito tempo]
palavras_chave: [timeout, lento, lentidao, demora, latencia, segundos, tempo esgotado, volume, 2 s]
causas_relacionadas: [limite_de_requisicoes, erro_interno_do_servidor, corpo_vazio]
verbete: erros/tempo_de_resposta_excedido.md
hash_do_verbete: 7b241e8b6a2713da
gerado_em: 2026-11-07
curado: sim
---

# Tempo de resposta excedido

Camada de leitura do verbete `tempo_de_resposta_excedido` (`biblioteca_producao/erros/tempo_de_resposta_excedido.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: Ambos (o site PHP e a API); entidade principal: Infraestrutura. Trata da causa `tempo_de_resposta_excedido` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

A resposta demora além do aceitável ou nunca chega: sem status (conexão encerrada) ou 200 tardio. 429 e 500 respondem rápido com um código: aqui não.

## Como aparece na tela

- 200 correto com segundos de espera: atraso no servidor ou no caminho.
- sem status, "Failed to fetch": o cliente desistiu antes.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `demora de segundos`, `timeout`, `conexao encerrada por tempo`, `carregando por muito tempo`.

## O que conferir

Causa, como o verbete a descreve: O modo latency dorme 2 s fixos (fault_injection.py:66); atrasos maiores vêm de banco, rede ou carga; o fetch da página não tem tempo limite.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `limite_de_requisicoes` (Limite de requisições (429)), `erro_interno_do_servidor` (Erro interno do servidor (500)), `corpo_vazio` (Corpo vazio).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/fault_injection.py`, `Programacao/CobaiaFront/produtos_api.php`.
- Rotas da API (campo `endpoints`): `GET /api/produtos`.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `timeout`, `lento`, `lentidao`, `demora`, `latencia`, `segundos`, `tempo esgotado`, `volume`, `2 s`.

## Notas do modelo

Nenhuma nota do modelo neste verbete.

## Curadoria

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: aprovada como estava.
