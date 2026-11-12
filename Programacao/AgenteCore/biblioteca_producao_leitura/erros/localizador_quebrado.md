---
# ! Alteração de IA - Revisar: camada de leitura do verbete `localizador_quebrado`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/localizador_quebrado.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 3 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas; a nota dizia que a retirada protegia a busca ("RAG", "vetorial", "indexação semântica"), mas a camada de leitura não é buscada nem lida pelo modelo, e a busca deste projeto é por palavras; a nota retirada continua no verbete que o modelo lê.
id: localizador_quebrado
titulo: Localizador (seletor) quebrado
sistema: CobaiaFront
entidade_principal: Interface
tipo: erro
status: ativo
causa_raiz: localizador_quebrado
arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/produtos_geral.php]
sintomas: [elemento nao encontrado, tempo esgotado procurando elemento, seletor casou dois elementos, texto do botao diferente]
palavras_chave: [seletor, localizador, css, xpath, id, classe, data-id, texto, ambiguo, unico, nth-child, ordem, roteiro, timeout, elemento, ambiguidade, order by, consulta]
causas_relacionadas: [estado_da_tela_divergente, recurso_inexistente]
verbete: erros/localizador_quebrado.md
hash_do_verbete: e952850a7b7899c2
gerado_em: 2026-11-07
curado: sim
---

# Localizador (seletor) quebrado

Camada de leitura do verbete `localizador_quebrado` (`biblioteca_producao/erros/localizador_quebrado.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: CobaiaFront (o site PHP); entidade principal: Interface. Trata da causa `localizador_quebrado` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

Nenhuma requisição falhou: o roteiro não acha o elemento (seletor não casa) ou acha mais de um (ambíguo). O problema é o localizador, não o dado.

## Como aparece na tela

- "Ver mais" vs "Saiba Mais...", data-produto vs data-id: texto ou atributo inexistente.
- nth-child que funciona às vezes: ordem não garantida.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `elemento nao encontrado`, `tempo esgotado procurando elemento`, `seletor casou dois elementos`, `texto do botao diferente`.

## O que conferir

Causa, como o verbete a descreve: Elementos reais de produtos_api.php: #produtos-api-grid, .thumbnail, button.saiba-mais[data-id], #modalDetalhe; a lista da API não tem ORDER BY (produtos.py:38).

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `estado_da_tela_divergente` (Estado da tela divergente da resposta), `recurso_inexistente` (Recurso inexistente (404 e vizinhos)).

## Onde está no código

- Arquivos: `Programacao/CobaiaFront/produtos_api.php`, `Programacao/CobaiaAPI/app/routers/produtos.py`, `Programacao/CobaiaFront/produtos_geral.php`.
- Rotas da API: nenhuma declarada.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `seletor`, `localizador`, `css`, `xpath`, `id`, `classe`, `data-id`, `texto`, `ambiguo`, `unico`, `nth-child`, `ordem`, `roteiro`, `timeout`, `elemento`, `ambiguidade`, `order by`, `consulta`.

## Notas do modelo

O verbete que o modelo lê traz 2 notas do modelo. A curadoria de 10/11/2026 as retirou desta leitura; elas continuam em `biblioteca_producao/erros/localizador_quebrado.md`.

## Curadoria

Leitura revisada e aprovada. Conceituação clara sobre falhas de seleção no DOM e instabilidade por ordenação não determinística. As duas notas do modelo (épocas 1 e 101) foram retiradas desta leitura; continuam no verbete que o modelo lê.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 3 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
