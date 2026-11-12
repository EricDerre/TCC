---
# ! Alteração de IA - Revisar: camada de leitura do verbete `valor_fora_do_dominio`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/valor_fora_do_dominio.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 4 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas; o termo continuava sem o significado na primeira menção, e os filtros de texto do pacote Q2 seguiam reprovando a leitura; a nota dizia que a curadoria era dos 39 verbetes da biblioteca de produção; o que foi curado são as 39 leituras, e a biblioteca que o modelo lê não mudou; e a nota não dizia que o texto do modelo saiu só desta leitura e continua no verbete que o modelo lê.
id: valor_fora_do_dominio
titulo: Valor fora do domínio
sistema: Ambos
entidade_principal: Pedido
tipo: erro
status: ativo
causa_raiz: valor_fora_do_dominio
arquivos: [Programacao/CobaiaFront/banco/schema_completo.sql, Programacao/CobaiaAPI/app/models.py, Programacao/CobaiaFront/cliente/registrar_reserva.php]
endpoints: [GET /api/pedidos, GET /api/produtos]
tabelas: [tbpedido_reserva, tbprodutos]
sintomas: [status desconhecido, pessoas zero, destaque 2, reserva sem botao de cancelar, botao de cancelar some, status inesperado]
palavras_chave: [dominio, enum, permitido, conjunto, status, Pendente, Concluido, pessoas, zero, negativo, destaque, validacao]
causas_relacionadas: [tipo_divergente, formato_de_data_divergente, nulo_inesperado]
verbete: erros/valor_fora_do_dominio.md
hash_do_verbete: f3c76906d1c76ecb
gerado_em: 2026-11-07
curado: sim
---

# Valor fora do domínio

Camada de leitura do verbete `valor_fora_do_dominio` (`biblioteca_producao/erros/valor_fora_do_dominio.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: Ambos (o site PHP e a API); entidade principal: Pedido. Trata da causa `valor_fora_do_dominio` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

Tipo certo, valor fora do conjunto permitido: status diferente de 'Em Análise'/'Cancelado', destaque diferente de true/false, pessoas menor que 1.

## Como aparece na tela

- reserva nem ativa nem cancelada na tela: status inesperado.
- 0 ou negativo em pessoas: o mínimo só existe no HTML.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `status desconhecido`, `pessoas zero`, `destaque 2`, `reserva sem botao de cancelar`, `botao de cancelar some`, `status inesperado`.

## O que conferir

Causa, como o verbete a descreve: status e destaque são `ENUM` no banco, uma lista fechada de valores permitidos (schema_completo.sql:37); pessoas ≥ 1 é só min= do HTML (registrar_reserva.php:55); a API não valida o que devolve.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `tipo_divergente` (Tipo divergente), `formato_de_data_divergente` (Formato de data divergente), `nulo_inesperado` (Nulo inesperado).

## Onde está no código

- Arquivos: `Programacao/CobaiaFront/banco/schema_completo.sql`, `Programacao/CobaiaAPI/app/models.py`, `Programacao/CobaiaFront/cliente/registrar_reserva.php`.
- Rotas da API (campo `endpoints`): `GET /api/pedidos`, `GET /api/produtos`.
- Tabelas do banco: `tbpedido_reserva`, `tbprodutos`.
- Palavras que a busca usa para achar este verbete: `dominio`, `enum`, `permitido`, `conjunto`, `status`, `Pendente`, `Concluido`, `pessoas`, `zero`, `negativo`, `destaque`, `validacao`.

## Notas do modelo

O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/erros/valor_fora_do_dominio.md`.

## Curadoria

Leitura revisada e aprovada. O termo `ENUM` foi explicado na primeira menção, para o filtro de termos técnicos do pacote Q2. A nota do modelo (época 1), que pedia uma validação na API, foi retirada desta leitura por ser instrução e não descrição; continua no verbete que o modelo lê. Com este arquivo o analista encerrou a curadoria das 39 leituras.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 4 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
