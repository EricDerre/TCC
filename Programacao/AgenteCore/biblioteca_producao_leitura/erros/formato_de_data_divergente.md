---
# ! Alteração de IA - Revisar: camada de leitura do verbete `formato_de_data_divergente`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/formato_de_data_divergente.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
id: formato_de_data_divergente
titulo: Formato de data divergente
sistema: CobaiaAPI
entidade_principal: Pedido
tipo: erro
status: ativo
causa_raiz: formato_de_data_divergente
arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/schemas.py]
endpoints: [GET /api/pedidos, POST /api/pedidos]
tabelas: [tbpedido_reserva]
sintomas: [Invalid Date, data como numero, data em formato brasileiro]
palavras_chave: [data, formato, iso, AAAA-MM-DD, dd/mm/aaaa, timestamp, epoch, Invalid Date, data_pedido]
causas_relacionadas: [escala_ou_unidade_errada, tipo_divergente]
verbete: erros/formato_de_data_divergente.md
hash_do_verbete: d64362675a1ee897
gerado_em: 2026-11-07
curado: sim
---

# Formato de data divergente

Camada de leitura do verbete `formato_de_data_divergente` (`biblioteca_producao/erros/formato_de_data_divergente.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: CobaiaAPI (a API); entidade principal: Pedido. Trata da causa `formato_de_data_divergente` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

data_pedido deve ser texto AAAA-MM-DD. Chega noutro formato (10/09/2026), como segundos (1789084800) ou com hora e fuso: e o cliente não interpreta.

## Como aparece na tela

- "Invalid Date" na listagem: formato brasileiro ou texto não reconhecido.
- número grande no lugar da data: timestamp.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `Invalid Date`, `data como numero`, `data em formato brasileiro`.

## O que conferir

Causa, como o verbete a descreve: A API devolve data_pedido.isoformat() (pedidos.py:23), sempre AAAA-MM-DD. Em escala_ou_unidade_errada a data é legível mas deslocada; aqui é ilegível.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `escala_ou_unidade_errada` (Escala ou unidade errada), `tipo_divergente` (Tipo divergente).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/routers/pedidos.py`, `Programacao/CobaiaAPI/app/schemas.py`.
- Rotas da API (campo `endpoints`): `GET /api/pedidos`, `POST /api/pedidos`.
- Tabelas do banco: `tbpedido_reserva`.
- Palavras que a busca usa para achar este verbete: `data`, `formato`, `iso`, `AAAA-MM-DD`, `dd/mm/aaaa`, `timestamp`, `epoch`, `Invalid Date`, `data_pedido`.

## Notas do modelo

Nenhuma nota do modelo neste verbete.

## Curadoria

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: aprovada como estava.
