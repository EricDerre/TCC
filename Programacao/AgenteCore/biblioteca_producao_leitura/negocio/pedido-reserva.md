---
# ! Alteração de IA - Revisar: camada de leitura do verbete `pedido-reserva`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/negocio/pedido-reserva.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
id: pedido-reserva
titulo: Reserva de mesa (pedido)
sistema: Ambos
entidade_principal: Pedido
tipo: funcionamento
status: ativo
arquivos: [Programacao/CobaiaFront/banco/schema_completo.sql, Programacao/CobaiaFront/cliente/reserva_cli.php, Programacao/CobaiaAPI/app/routers/pedidos.py]
endpoints: [GET /api/pedidos]
tabelas: [tbpedido_reserva, vw_tbpedidos, tbusuarios]
sintomas: [status com texto desconhecido, reserva de outro cliente, linha de reserva vazia]
palavras_chave: [reserva, pedido, status, em analise, cancelado, pessoas, data_pedido, id_clientes, view]
causas_relacionadas: [valor_fora_do_dominio, nulo_inesperado, chave_de_juncao_errada]
verbete: negocio/pedido-reserva.md
hash_do_verbete: a123c184d6582124
gerado_em: 2026-11-07
curado: sim
---

# Reserva de mesa (pedido)

Camada de leitura do verbete `pedido-reserva` (`biblioteca_producao/negocio/pedido-reserva.md`). Tipo: funcionamento (descreve como uma parte do sistema funciona); estado: ativo (em vigor); sistema: Ambos (o site PHP e a API); entidade principal: Pedido.

## O que é

Reserva em tbpedido_reserva: id_pedido, id_clientes (chave para tbusuarios), pessoas, data_pedido, status. Status só admite 'Em Análise' (inicial) e 'Cancelado'.

## Como aparece na tela

- status com outro texto: fora do domínio.
- linha de reserva toda vazia: cliente que ainda não reservou.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `status com texto desconhecido`, `reserva de outro cliente`, `linha de reserva vazia`.

## O que conferir

Causa, como o verbete a descreve: A leitura usa vw_tbpedidos, LEFT JOIN de tbusuarios (schema_completo.sql:57): cliente sem reserva vira linha com campos nulos, que reserva_cli.php renderiza.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `valor_fora_do_dominio` (Valor fora do domínio), `nulo_inesperado` (Nulo inesperado), `chave_de_juncao_errada` (Chave de junção errada).

## Onde está no código

- Arquivos: `Programacao/CobaiaFront/banco/schema_completo.sql`, `Programacao/CobaiaFront/cliente/reserva_cli.php`, `Programacao/CobaiaAPI/app/routers/pedidos.py`.
- Rotas da API (campo `endpoints`): `GET /api/pedidos`.
- Tabelas do banco: `tbpedido_reserva`, `vw_tbpedidos`, `tbusuarios`.
- Palavras que a busca usa para achar este verbete: `reserva`, `pedido`, `status`, `em analise`, `cancelado`, `pessoas`, `data_pedido`, `id_clientes`, `view`.

## Notas do modelo

Nenhuma nota do modelo neste verbete.

## Curadoria

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: aprovada como estava.
