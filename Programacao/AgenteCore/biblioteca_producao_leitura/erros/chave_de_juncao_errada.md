---
# ! Alteração de IA - Revisar: camada de leitura do verbete `chave_de_juncao_errada`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/chave_de_juncao_errada.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 3 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas; a nota dizia que a retirada protegia a busca ("RAG", "vetorial", "indexação semântica"), mas a camada de leitura não é buscada nem lida pelo modelo, e a busca deste projeto é por palavras; a nota retirada continua no verbete que o modelo lê.
id: chave_de_juncao_errada
titulo: Chave de junção errada
sistema: Ambos
entidade_principal: Pedido
tipo: erro
status: ativo
causa_raiz: chave_de_juncao_errada
arquivos: [Programacao/CobaiaAPI/app/models.py, Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaFront/cliente/index.php]
endpoints: [GET /api/produtos, GET /api/pedidos]
tabelas: [tbprodutos, tbtipos, tbusuarios, tbpedido_reserva]
sintomas: [nome de outra pessoa na reserva, categoria errada, imagem de outro produto, nome da categoria no titulo]
palavras_chave: [juncao, join, chave, id, fk, cliente errado, categoria errada, troca, admin, like, substring, registro errado, campo derivado]
causas_relacionadas: [nulo_inesperado, escala_ou_unidade_errada, valor_fora_do_dominio]
verbete: erros/chave_de_juncao_errada.md
hash_do_verbete: 4bc46561bb6c1d38
gerado_em: 2026-11-07
curado: sim
---

# Chave de junção errada

Camada de leitura do verbete `chave_de_juncao_errada` (`biblioteca_producao/erros/chave_de_juncao_errada.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: Ambos (o site PHP e a API); entidade principal: Pedido. Trata da causa `chave_de_juncao_errada` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

Tipo e formato certos, mas o valor é de OUTRO registro: categoria ou imagem alheia no produto, nome ou cpf de outro usuário na reserva.

## Como aparece na tela

- afeta campo derivado de junção (tipo, nome, cpf, imagem), não os próprios.
- o dado existe no banco, ligado ao registro errado.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `nome de outra pessoa na reserva`, `categoria errada`, `imagem de outro produto`, `nome da categoria no titulo`.

## O que conferir

Causa, como o verbete a descreve: Junções: id_tipo_produto e id_clientes (models.py). No site, cliente/index.php:4 usa LIKE '%login%': CPF substring de outro casa mais de um cliente.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `nulo_inesperado` (Nulo inesperado), `escala_ou_unidade_errada` (Escala ou unidade errada), `valor_fora_do_dominio` (Valor fora do domínio).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/models.py`, `Programacao/CobaiaAPI/app/routers/pedidos.py`, `Programacao/CobaiaFront/cliente/index.php`.
- Rotas da API (campo `endpoints`): `GET /api/produtos`, `GET /api/pedidos`.
- Tabelas do banco: `tbprodutos`, `tbtipos`, `tbusuarios`, `tbpedido_reserva`.
- Palavras que a busca usa para achar este verbete: `juncao`, `join`, `chave`, `id`, `fk`, `cliente errado`, `categoria errada`, `troca`, `admin`, `like`, `substring`, `registro errado`, `campo derivado`.

## Notas do modelo

O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/erros/chave_de_juncao_errada.md`.

## Curadoria

Leitura revisada e aprovada. A nota do modelo foi retirada desta leitura para manter o foco na descrição do defeito; continua no verbete que o modelo lê.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 3 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
