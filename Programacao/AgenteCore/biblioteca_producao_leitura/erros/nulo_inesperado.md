---
# ! Alteração de IA - Revisar: camada de leitura do verbete `nulo_inesperado`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/nulo_inesperado.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
id: nulo_inesperado
titulo: Nulo inesperado
sistema: Ambos
entidade_principal: Pedido
tipo: erro
status: ativo
causa_raiz: nulo_inesperado
arquivos: [Programacao/CobaiaAPI/app/models.py, Programacao/CobaiaFront/banco/schema_completo.sql, Programacao/CobaiaAPI/app/routers/produtos.py]
endpoints: [GET /api/produtos, GET /api/pedidos]
tabelas: [tbprodutos, vw_tbpedidos]
sintomas: [null onde havia valor, saudacao vazia, R$ 0, 00 para produto com preco, produto some do filtro]
palavras_chave: [nulo, null, None, vazio, nullable, saudacao, Ola, left join, view]
causas_relacionadas: [campo_ausente, valor_fora_do_dominio, chave_de_juncao_errada]
verbete: erros/nulo_inesperado.md
hash_do_verbete: 89f4f70f7bd6ddf9
gerado_em: 2026-11-07
curado: sim
---

# Nulo inesperado

Camada de leitura do verbete `nulo_inesperado` (`biblioteca_producao/erros/nulo_inesperado.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: Ambos (o site PHP e a API); entidade principal: Pedido. Trata da causa `nulo_inesperado` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

A chave existe e vem null onde o contrato promete valor. Diferente de campo_ausente: a chave está lá.

## Como aparece na tela

- nome nulo: "Olá, !" na área do cliente; preco nulo: cartão sem valor.
- tipo nulo: produto some de filtros por categoria.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `null onde havia valor`, `saudacao vazia`, `R$ 0`, `00 para produto com preco`, `produto some do filtro`.

## O que conferir

Causa, como o verbete a descreve: Origens legítimas: resumo, valor_produto e imagem_produto são nullable (models.py:33-35) e vw_tbpedidos faz LEFT JOIN. tipo nulo não sai de produtos.py (p.tipo.rotulo_tipo).

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `campo_ausente` (Campo ausente), `valor_fora_do_dominio` (Valor fora do domínio), `chave_de_juncao_errada` (Chave de junção errada).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/models.py`, `Programacao/CobaiaFront/banco/schema_completo.sql`, `Programacao/CobaiaAPI/app/routers/produtos.py`.
- Rotas da API (campo `endpoints`): `GET /api/produtos`, `GET /api/pedidos`.
- Tabelas do banco: `tbprodutos`, `vw_tbpedidos`.
- Palavras que a busca usa para achar este verbete: `nulo`, `null`, `None`, `vazio`, `nullable`, `saudacao`, `Ola`, `left join`, `view`.

## Notas do modelo

Nenhuma nota do modelo neste verbete.

## Curadoria

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: aprovada como estava.
