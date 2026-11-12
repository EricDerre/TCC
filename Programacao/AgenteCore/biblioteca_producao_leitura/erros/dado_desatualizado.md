---
# ! Alteração de IA - Revisar: camada de leitura do verbete `dado_desatualizado`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/dado_desatualizado.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
id: dado_desatualizado
titulo: Dado desatualizado (cache)
sistema: Infraestrutura
entidade_principal: Infraestrutura
tipo: erro
status: ativo
causa_raiz: dado_desatualizado
arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/database.py]
endpoints: [GET /api/pedidos, GET /api/produtos]
sintomas: [reserva nova nao aparece, cancelamento volta a ativo ao recarregar, produto novo demora a aparecer]
palavras_chave: [cache, desatualizado, velho, antigo, Age, Cache-Control, max-age, defasagem, minutos, stale]
causas_relacionadas: [estado_da_tela_divergente, registro_duplicado, contagem_inconsistente]
verbete: erros/dado_desatualizado.md
hash_do_verbete: 33d803e4d898a20e
gerado_em: 2026-11-07
curado: sim
---

# Dado desatualizado (cache)

Camada de leitura do verbete `dado_desatualizado` (`biblioteca_producao/erros/dado_desatualizado.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: Infraestrutura (servidor, banco e rede); entidade principal: Infraestrutura. Trata da causa `dado_desatualizado` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

Uma escrita confirmada (201/200) não aparece na leitura seguinte e surge minutos depois sem nova ação: a leitura veio de uma cópia antiga.

## Como aparece na tela

- cabeçalhos Age ou Cache-Control: max-age no GET.
- o painel PHP (lê o banco direto) já mostra o dado; só a API atrasa.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `reserva nova nao aparece`, `cancelamento volta a ativo ao recarregar`, `produto novo demora a aparecer`.

## O que conferir

Causa, como o verbete a descreve: A CobaiaAPI consulta o banco a cada requisição (database.py) e não envia cache; leitura defasada indica proxy ou cache do navegador entre a página e a API.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `estado_da_tela_divergente` (Estado da tela divergente da resposta), `registro_duplicado` (Registro duplicado), `contagem_inconsistente` (Contagem inconsistente).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/routers/pedidos.py`, `Programacao/CobaiaAPI/app/database.py`.
- Rotas da API (campo `endpoints`): `GET /api/pedidos`, `GET /api/produtos`.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `cache`, `desatualizado`, `velho`, `antigo`, `Age`, `Cache-Control`, `max-age`, `defasagem`, `minutos`, `stale`.

## Notas do modelo

Nenhuma nota do modelo neste verbete.

## Curadoria

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: aprovada como estava.
