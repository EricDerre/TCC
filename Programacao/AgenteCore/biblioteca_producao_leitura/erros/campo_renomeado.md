---
# ! Alteração de IA - Revisar: camada de leitura do verbete `campo_renomeado`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/campo_renomeado.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 3 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas; a nota repetia entre aspas uma frase inteira do texto, e a repetição fazia a leitura reprovar no filtro de repetição; e a nota não dizia que o texto do modelo saiu só desta leitura e continua no verbete que o modelo lê.
id: campo_renomeado
titulo: Campo renomeado
sistema: CobaiaAPI
entidade_principal: Produto
tipo: erro
status: ativo
causa_raiz: campo_renomeado
arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaAPI/app/schemas.py]
endpoints: [GET /api/produtos, GET /api/pedidos]
sintomas: [chave desconhecida no lugar da esperada, _v2, campo com outro nome, titulo vazio, nome correto, categoria e preco corretos]
palavras_chave: [renomead, outro nome, _v2, descricao, situacao, imagem_url, field_renamed, chave inesperada, campo-renomeado, contrato, cliente]
causas_relacionadas: [campo_ausente, estrutura_aninhada_divergente]
verbete: erros/campo_renomeado.md
hash_do_verbete: 39c070b8ac1186b4
gerado_em: 2026-11-07
curado: sim
---

# Campo renomeado

Camada de leitura do verbete `campo_renomeado` (`biblioteca_producao/erros/campo_renomeado.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: CobaiaAPI (a API); entidade principal: Produto. Trata da causa `campo_renomeado` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

O valor existe sob outra chave: falta a esperada e aparece uma desconhecida com o mesmo tipo e conteúdo (preco leva a preco_v2, nome leva a descricao, status leva a situacao).

## Como aparece na tela

- o resto do objeto confere; uma chave sumiu e outra sobrou.
- vazio ou undefined só naquele campo.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `chave desconhecida no lugar da esperada`, `_v2`, `campo com outro nome`, `titulo vazio`, `nome correto`, `categoria e preco corretos`.

## O que conferir

Causa, como o verbete a descreve: O modo field_renamed troca o campo-alvo por <campo>_v2 (fault_injection.py). Fora dele: contrato mudou no servidor sem atualizar o cliente.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `campo_ausente` (Campo ausente), `estrutura_aninhada_divergente` (Estrutura aninhada divergente).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/fault_injection.py`, `Programacao/CobaiaAPI/app/schemas.py`.
- Rotas da API (campo `endpoints`): `GET /api/produtos`, `GET /api/pedidos`.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `renomead`, `outro nome`, `_v2`, `descricao`, `situacao`, `imagem_url`, `field_renamed`, `chave inesperada`, `campo-renomeado`, `contrato`, `cliente`.

## Notas do modelo

O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/erros/campo_renomeado.md`.

## Curadoria

Leitura revisada e aprovada. A redação original de "O que conferir" se mantém, pois é tecnicamente mais precisa do que a retificação que o modelo propôs. A nota do modelo foi retirada desta leitura; continua no verbete que o modelo lê.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 3 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
