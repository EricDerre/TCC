---
# ! Alteração de IA - Revisar: camada de leitura do verbete `entidade-produto`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/negocio/entidade-produto.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 2 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas; o termo continuava sem o significado na primeira menção, e os filtros de texto do pacote Q2 seguiam reprovando a leitura.
id: entidade-produto
titulo: Produto e sua categoria
sistema: Ambos
entidade_principal: Produto
tipo: funcionamento
status: ativo
arquivos: [Programacao/CobaiaAPI/app/models.py, Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/banco/seed.sql]
endpoints: [GET /api/produtos, GET /api/produtos/{id}]
tabelas: [tbprodutos, tbtipos]
sintomas: [nome da categoria no titulo do cartao, preco com grandeza estranha, preco cru, separador decimal como virgula]
palavras_chave: [produto, categoria, tipo, preco, destaque, imagem, resumo, cardapio, picanha, formatacao, decimal, separador]
causas_relacionadas: [chave_de_juncao_errada, escala_ou_unidade_errada, tipo_divergente]
verbete: negocio/entidade-produto.md
hash_do_verbete: ce4af533dfd3ceed
gerado_em: 2026-11-07
curado: sim
---

# Produto e sua categoria

Camada de leitura do verbete `entidade-produto` (`biblioteca_producao/negocio/entidade-produto.md`). Tipo: funcionamento (descreve como uma parte do sistema funciona); estado: ativo (em vigor); sistema: Ambos (o site PHP e a API); entidade principal: Produto.

## O que é

Item do cardápio em tbprodutos, ligado a uma categoria de tbtipos (Carnes, Bebidas, Acompanhamentos, Sobremesas). 14 produtos; o id 1 é Picanha ao Alho, Carnes, 89,90.

## Como aparece na tela

- título com nome de categoria: junção trocada.
- preço com grandeza estranha: conversão de valor_produto.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `nome da categoria no titulo do cartao`, `preco com grandeza estranha`, `preco cru`, `separador decimal como virgula`.

## O que conferir

Causa, como o verbete a descreve: valor_produto é DECIMAL(9,2) e destaque_produto é `ENUM('Sim','Não')`, uma lista fechada de valores permitidos; produtos.py (_to_dict) converte em número e booleano.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `chave_de_juncao_errada` (Chave de junção errada), `escala_ou_unidade_errada` (Escala ou unidade errada), `tipo_divergente` (Tipo divergente).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/models.py`, `Programacao/CobaiaAPI/app/routers/produtos.py`, `Programacao/CobaiaFront/banco/seed.sql`.
- Rotas da API (campo `endpoints`): `GET /api/produtos`, `GET /api/produtos/{id}`.
- Tabelas do banco: `tbprodutos`, `tbtipos`.
- Palavras que a busca usa para achar este verbete: `produto`, `categoria`, `tipo`, `preco`, `destaque`, `imagem`, `resumo`, `cardapio`, `picanha`, `formatacao`, `decimal`, `separador`.

## Notas do modelo

O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/negocio/entidade-produto.md`.

## Curadoria

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 2 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
