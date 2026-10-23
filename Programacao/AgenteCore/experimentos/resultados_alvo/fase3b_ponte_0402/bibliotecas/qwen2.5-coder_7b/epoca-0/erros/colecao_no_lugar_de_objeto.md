---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: lista × objeto é a diferença entre as duas rotas de produto; conferido em
# produtos.py e no modal de produtos_api.php.
id: colecao_no_lugar_de_objeto
titulo: Coleção no lugar de objeto (ou o inverso)
sistema: CobaiaAPI
entidade_principal: Produto
tipo: erro
status: ativo
causa_raiz: colecao_no_lugar_de_objeto
arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/produtos_api.php]
endpoints: [GET /api/produtos, GET /api/produtos/{id}]
sintomas: [detalhe sem preencher campos, colchetes ao redor do valor, nenhum produto retornado]
palavras_chave: [lista, array, colecao, objeto, unico, recurso, colchetes, detalhe, modal]
causas_relacionadas: [estrutura_aninhada_divergente, campo_ausente]
---
## Resumo
Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (["Carnes"]).

## Sinais
- modal "Produto #1"/"(sem descrição)": p é lista
- categoria com colchetes: campo veio como lista

## Causa
GET /api/produtos devolve lista, GET /api/produtos/{id} objeto (produtos.py); a página não confere a forma antes de ler os campos.
