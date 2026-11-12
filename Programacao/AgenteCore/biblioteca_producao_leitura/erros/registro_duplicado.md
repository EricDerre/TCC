---
# ! Alteração de IA - Revisar: camada de leitura do verbete `registro_duplicado`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/registro_duplicado.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
id: registro_duplicado
titulo: Registro duplicado
sistema: Ambos
entidade_principal: Pedido
tipo: erro
status: ativo
causa_raiz: registro_duplicado
arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaFront/cliente/registrar_reserva.php]
endpoints: [POST /api/pedidos, GET /api/pedidos]
tabelas: [tbpedido_reserva]
sintomas: [duas reservas identicas, dois 201 seguidos, cobranca em duplicidade]
palavras_chave: [duplicad, duplicat, repetid, reenvio, clique duplo, F5, idempot, dois registros, ids consecutivos]
causas_relacionadas: [dado_desatualizado, contagem_inconsistente]
verbete: erros/registro_duplicado.md
hash_do_verbete: b6368a8e4d912662
gerado_em: 2026-11-07
curado: sim
---

# Registro duplicado

Camada de leitura do verbete `registro_duplicado` (`biblioteca_producao/erros/registro_duplicado.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: Ambos (o site PHP e a API); entidade principal: Pedido. Trata da causa `registro_duplicado` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

A mesma escrita gravada mais de uma vez: reservas iguais com ids consecutivos, duas respostas 201 para um único gesto.

## Como aparece na tela

- registros idênticos exceto pelo id.
- dois POST com o mesmo corpo na sequência.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `duas reservas identicas`, `dois 201 seguidos`, `cobranca em duplicidade`.

## O que conferir

Causa, como o verbete a descreve: POST /api/pedidos insere sem chave de idempotência (pedidos.py:46-66): clique duplo vira duas linhas. registrar_reserva.php insere a cada POST: recarregar após reservar reenvia o formulário.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `dado_desatualizado` (Dado desatualizado (cache)), `contagem_inconsistente` (Contagem inconsistente).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/routers/pedidos.py`, `Programacao/CobaiaFront/cliente/registrar_reserva.php`.
- Rotas da API (campo `endpoints`): `POST /api/pedidos`, `GET /api/pedidos`.
- Tabelas do banco: `tbpedido_reserva`.
- Palavras que a busca usa para achar este verbete: `duplicad`, `duplicat`, `repetid`, `reenvio`, `clique duplo`, `F5`, `idempot`, `dois registros`, `ids consecutivos`.

## Notas do modelo

Nenhuma nota do modelo neste verbete.

## Curadoria

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: aprovada como estava.
