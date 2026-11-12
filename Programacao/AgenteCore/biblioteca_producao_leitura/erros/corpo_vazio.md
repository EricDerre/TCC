---
# ! Alteração de IA - Revisar: camada de leitura do verbete `corpo_vazio`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/corpo_vazio.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 3 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas; a nota dizia que a retirada protegia a busca ("RAG", "vetorial", "indexação semântica"), mas a camada de leitura não é buscada nem lida pelo modelo, e a busca deste projeto é por palavras; a nota retirada continua no verbete que o modelo lê; e a nota chamava as épocas de "treinamento"; neste projeto o modelo não é treinado: época é a rodada em que ele propôs acréscimos à biblioteca; a nota retirada continua no verbete que o modelo lê.
id: corpo_vazio
titulo: Corpo vazio
sistema: Ambos
entidade_principal: Infraestrutura
tipo: erro
status: ativo
causa_raiz: corpo_vazio
arquivos: [Programacao/CobaiaFront/produtos_api.php]
sintomas: [carregando indefinidamente, tela em branco sem erro, fim inesperado da entrada em corpo vazio]
palavras_chave: [vazio, sem corpo, branco, 204, espacos, nenhum byte, carregando]
causas_relacionadas: [resposta_truncada, corpo_nao_e_json, estado_da_tela_divergente]
verbete: erros/corpo_vazio.md
hash_do_verbete: 24ff40566524dc13
gerado_em: 2026-11-07
curado: sim
---

# Corpo vazio

Camada de leitura do verbete `corpo_vazio` (`biblioteca_producao/erros/corpo_vazio.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: Ambos (o site PHP e a API); entidade principal: Infraestrutura. Trata da causa `corpo_vazio` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

Status de sucesso e nenhum byte útil no corpo (vazio, só espaços, ou 204). Diferente de "[]", lista vazia, que é JSON válido.

## Como aparece na tela

- resp.json() falha em zero caracteres: "Erro ao carregar produtos" ou "Carregando..." parado.
- "[]" mostra "Nenhum produto retornado pela API.".

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `carregando indefinidamente`, `tela em branco sem erro`, `fim inesperado da entrada em corpo vazio`.

## O que conferir

Causa, como o verbete a descreve: Nenhuma rota da CobaiaAPI devolve 204 nem corpo vazio; se chega vazio, foi cortado antes de sair (servidor, proxy) ou a rota errada respondeu.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `resposta_truncada` (Resposta truncada), `corpo_nao_e_json` (Corpo não é JSON), `estado_da_tela_divergente` (Estado da tela divergente da resposta).

## Onde está no código

- Arquivos: `Programacao/CobaiaFront/produtos_api.php`.
- Rotas da API: nenhuma declarada.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `vazio`, `sem corpo`, `branco`, `204`, `espacos`, `nenhum byte`, `carregando`.

## Notas do modelo

O verbete que o modelo lê traz 2 notas do modelo. A curadoria de 10/11/2026 as retirou desta leitura; elas continuam em `biblioteca_producao/erros/corpo_vazio.md`.

## Curadoria

Leitura revisada e aprovada. Excelente conceituação da diferença entre corpo nulo e lista JSON vazia. As duas notas do modelo foram retiradas desta leitura; continuam no verbete que o modelo lê.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 3 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
