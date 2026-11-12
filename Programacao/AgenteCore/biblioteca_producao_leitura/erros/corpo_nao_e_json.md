---
# ! Alteração de IA - Revisar: camada de leitura do verbete `corpo_nao_e_json`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/corpo_nao_e_json.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 4 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas; a nota dizia que a retirada protegia a busca ("RAG", "vetorial", "indexação semântica"), mas a camada de leitura não é buscada nem lida pelo modelo, e a busca deste projeto é por palavras; a nota retirada continua no verbete que o modelo lê; o termo continuava sem o significado na primeira menção, e os filtros de texto do pacote Q2 seguiam reprovando a leitura.
id: corpo_nao_e_json
titulo: Corpo não é JSON
sistema: Ambos
entidade_principal: Infraestrutura
tipo: erro
status: ativo
causa_raiz: corpo_nao_e_json
arquivos: [Programacao/CobaiaFront/conn/connect.php, Programacao/CobaiaFront/produtos_api.php]
sintomas: [token inesperado no inicio da resposta, html no lugar de json, warning do php antes do json, parse_falho, listagem_nao_carrega]
palavras_chave: [json, html, xml, parse, token inesperado, warning, fatal, gateway, proxy, atencao erro, content-type, erro de sintaxe, parse_falho]
causas_relacionadas: [resposta_truncada, corpo_vazio, erro_interno_do_servidor]
verbete: erros/corpo_nao_e_json.md
hash_do_verbete: 56b198a9fc943dcb
gerado_em: 2026-11-07
curado: sim
---

# Corpo não é JSON

Camada de leitura do verbete `corpo_nao_e_json` (`biblioteca_producao/erros/corpo_nao_e_json.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: Ambos (o site PHP e a API); entidade principal: Infraestrutura. Trata da causa `corpo_nao_e_json` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

A resposta chega (às vezes 200 e Content-Type application/json), mas o corpo é HTML, XML ou aviso em texto: o parse falha no primeiro caractere.

## Como aparece na tela

- erro no console do navegador acusando caractere inválido: `Unexpected token <`, em que token é o pedaço do texto que o leitor de JSON não esperava.
- texto legível antes ou no lugar do JSON: Warning do PHP, página de gateway, "Atenção ERRO".

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `token inesperado no inicio da resposta`, `html no lugar de json`, `warning do php antes do json`, `parse_falho`, `listagem_nao_carrega`.

## O que conferir

Causa, como o verbete a descreve: Falha de conexão no site imprime "Atenção ERRO" em HTML (connect.php:16); Warning/Fatal do PHP saem antes da saída; gateway fora devolve a própria página.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `resposta_truncada` (Resposta truncada), `corpo_vazio` (Corpo vazio), `erro_interno_do_servidor` (Erro interno do servidor (500)).

## Onde está no código

- Arquivos: `Programacao/CobaiaFront/conn/connect.php`, `Programacao/CobaiaFront/produtos_api.php`.
- Rotas da API: nenhuma declarada.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `json`, `html`, `xml`, `parse`, `token inesperado`, `warning`, `fatal`, `gateway`, `proxy`, `atencao erro`, `content-type`, `erro de sintaxe`, `parse_falho`.

## Notas do modelo

O verbete que o modelo lê traz 2 notas do modelo. A curadoria de 10/11/2026 as retirou desta leitura; elas continuam em `biblioteca_producao/erros/corpo_nao_e_json.md`.

## Curadoria

Leitura revisada e aprovada. O termo `token` foi explicado na primeira menção, para o filtro de termos técnicos do pacote Q2. As duas notas do modelo (exemplos em HTML e XML) foram retiradas desta leitura; continuam no verbete que o modelo lê.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 4 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
