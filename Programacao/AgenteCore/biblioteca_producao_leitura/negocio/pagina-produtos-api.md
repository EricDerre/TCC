---
# ! Alteração de IA - Revisar: camada de leitura do verbete `pagina-produtos-api`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/negocio/pagina-produtos-api.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
id: pagina-produtos-api
titulo: Aba "Produtos (API)", a fronteira JSON
sistema: CobaiaFront
entidade_principal: Interface
tipo: funcionamento
status: ativo
arquivos: [Programacao/CobaiaFront/produtos_api.php]
endpoints: [GET /api/produtos, GET /api/produtos/{id}]
sintomas: [carregando produtos parado, nenhum produto retornado, erro ao carregar produtos, R$ NaN, object Object]
palavras_chave: [produtos_api, fetch, cartao, card, modal, saiba mais, formatarPreco, Number, NaN, data-id, status, grid]
causas_relacionadas: [estado_da_tela_divergente, localizador_quebrado, corpo_vazio, tipo_divergente]
verbete: negocio/pagina-produtos-api.md
hash_do_verbete: acc350822a0e24e1
gerado_em: 2026-11-07
curado: sim
---

# Aba "Produtos (API)", a fronteira JSON

Camada de leitura do verbete `pagina-produtos-api` (`biblioteca_producao/negocio/pagina-produtos-api.md`). Tipo: funcionamento (descreve como uma parte do sistema funciona); estado: ativo (em vigor); sistema: CobaiaFront (o site PHP); entidade principal: Interface.

## O que é

produtos_api.php monta os cartões com fetch() em localhost:8000/api/produtos: a única fronteira JSON do cobaia; detalhe via GET /api/produtos/{id}.

## Como aparece na tela

- "Carregando..." parado: o fetch nunca resolveu.
- "Nenhum produto retornado pela API.": não é lista, ou vazia.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `carregando produtos parado`, `nenhum produto retornado`, `erro ao carregar produtos`, `R$ NaN`, `object Object`.

## O que conferir

Causa, como o verbete a descreve: formatarPreco() usa Number(): preço não numérico sai cru; tipo objeto sai via JSON.stringify; botão button.saiba-mais[data-id].

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `estado_da_tela_divergente` (Estado da tela divergente da resposta), `localizador_quebrado` (Localizador (seletor) quebrado), `corpo_vazio` (Corpo vazio), `tipo_divergente` (Tipo divergente).

## Onde está no código

- Arquivos: `Programacao/CobaiaFront/produtos_api.php`.
- Rotas da API (campo `endpoints`): `GET /api/produtos`, `GET /api/produtos/{id}`.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `produtos_api`, `fetch`, `cartao`, `card`, `modal`, `saiba mais`, `formatarPreco`, `Number`, `NaN`, `data-id`, `status`, `grid`.

## Notas do modelo

Nenhuma nota do modelo neste verbete.

## Curadoria

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: aprovada como estava.
