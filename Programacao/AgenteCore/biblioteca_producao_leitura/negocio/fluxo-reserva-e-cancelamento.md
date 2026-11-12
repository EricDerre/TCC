---
# ! Alteração de IA - Revisar: camada de leitura do verbete `fluxo-reserva-e-cancelamento`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/negocio/fluxo-reserva-e-cancelamento.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
id: fluxo-reserva-e-cancelamento
titulo: Fluxo de reservar e cancelar
sistema: Ambos
entidade_principal: Pedido
tipo: regra
status: ativo
arquivos: [Programacao/CobaiaFront/cliente/registrar_reserva.php, Programacao/CobaiaFront/cliente/cliente_cancelar.php, Programacao/CobaiaAPI/app/routers/pedidos.py]
endpoints: [POST /api/pedidos, POST /api/pedidos/{id}/cancelar]
tabelas: [tbpedido_reserva]
sintomas: [data aceita fora da janela, reserva alheia cancelada, pessoas zero]
palavras_chave: [reservar, cancelar, data, janela, dois dias, noventa dias, pessoas, minimo, validacao, formulario]
causas_relacionadas: [valor_fora_do_dominio, dado_desatualizado, estado_da_tela_divergente]
verbete: negocio/fluxo-reserva-e-cancelamento.md
hash_do_verbete: 180eb6aef8653323
gerado_em: 2026-11-07
curado: sim
---

# Fluxo de reservar e cancelar

Camada de leitura do verbete `fluxo-reserva-e-cancelamento` (`biblioteca_producao/negocio/fluxo-reserva-e-cancelamento.md`). Tipo: regra (regra de negócio do sistema); estado: ativo (em vigor); sistema: Ambos (o site PHP e a API); entidade principal: Pedido.

## O que é

Reserva em cliente/registrar_reserva.php e cancelamento em reserva_cli.php; a API espelha em POST /api/pedidos e POST /api/pedidos/{id}/cancelar.

## Como aparece na tela

- regra de data e quantidade só no navegador.
- reserva alheia cancelada sem checagem de dono.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `data aceita fora da janela`, `reserva alheia cancelada`, `pessoas zero`.

## O que conferir

Causa, como o verbete a descreve: Data hoje+2 a hoje+90 e pessoas ≥ 1 são só min/max do HTML (registrar_reserva.php:28-35,55); cancelar grava 'Cancelado' (pedidos.py:75).

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `valor_fora_do_dominio` (Valor fora do domínio), `dado_desatualizado` (Dado desatualizado (cache)), `estado_da_tela_divergente` (Estado da tela divergente da resposta).

## Onde está no código

- Arquivos: `Programacao/CobaiaFront/cliente/registrar_reserva.php`, `Programacao/CobaiaFront/cliente/cliente_cancelar.php`, `Programacao/CobaiaAPI/app/routers/pedidos.py`.
- Rotas da API (campo `endpoints`): `POST /api/pedidos`, `POST /api/pedidos/{id}/cancelar`.
- Tabelas do banco: `tbpedido_reserva`.
- Palavras que a busca usa para achar este verbete: `reservar`, `cancelar`, `data`, `janela`, `dois dias`, `noventa dias`, `pessoas`, `minimo`, `validacao`, `formulario`.

## Notas do modelo

Nenhuma nota do modelo neste verbete.

## Curadoria

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: aprovada como estava.
