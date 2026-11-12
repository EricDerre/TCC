---
# ! Alteração de IA - Revisar: camada de leitura do verbete `limites-do-sistema`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/negocio/limites-do-sistema.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 3 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; o termo continuava sem o significado na primeira menção, e os filtros de texto do pacote Q2 seguiam reprovando a leitura; a nota chamava as épocas de "treinamento"; neste projeto o modelo não é treinado: época é a rodada em que ele propôs acréscimos à biblioteca; a nota retirada continua no verbete que o modelo lê.
id: limites-do-sistema
titulo: O que o sistema não faz
sistema: Ambos
entidade_principal: Infraestrutura
tipo: limite
status: ativo
arquivos: [Programacao/CobaiaFront/conn/connect.php, Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/schemas.py]
sintomas: [dado invalido gravado, falha silenciosa, contrato do docs diferente da resposta]
palavras_chave: [validacao, servidor, silencioso, checagem, hash, response_model, docs, declarado, real]
causas_relacionadas: [valor_fora_do_dominio, campo_ausente, tipo_divergente, dado_desatualizado]
verbete: negocio/limites-do-sistema.md
hash_do_verbete: b0bded596b317fa0
gerado_em: 2026-11-07
curado: sim
---

# O que o sistema não faz

Camada de leitura do verbete `limites-do-sistema` (`biblioteca_producao/negocio/limites-do-sistema.md`). Tipo: limite (o que o sistema não faz); estado: ativo (em vigor); sistema: Ambos (o site PHP e a API); entidade principal: Infraestrutura.

## O que é

Não valida data nem pessoas no servidor; não confere o retorno de $conn->query() em página nenhuma; não checa se a reserva cancelada é do cliente; não aplica hash (o resumo embaralhado da senha, que não se desfaz) na senha no login.

## Como aparece na tela

- dado inválido gravado sem mensagem.
- redireciona como se tivesse gravado e nada mudou: SQL falhou em silêncio.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `dado invalido gravado`, `falha silenciosa`, `contrato do docs diferente da resposta`.

## O que conferir

Causa, como o verbete a descreve: A API não revalida a resposta: rotas devolvem JSONResponse cru (produtos.py:1-7); o /docs mostra o esperado, não o que sai pela rede.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `valor_fora_do_dominio` (Valor fora do domínio), `campo_ausente` (Campo ausente), `tipo_divergente` (Tipo divergente), `dado_desatualizado` (Dado desatualizado (cache)).

## Onde está no código

- Arquivos: `Programacao/CobaiaFront/conn/connect.php`, `Programacao/CobaiaAPI/app/routers/produtos.py`, `Programacao/CobaiaAPI/app/schemas.py`.
- Rotas da API: nenhuma declarada.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `validacao`, `servidor`, `silencioso`, `checagem`, `hash`, `response_model`, `docs`, `declarado`, `real`.

## Notas do modelo

Nenhuma nota do modelo neste verbete.

## Curadoria

Leitura revisada e aprovada. O termo `hash` foi explicado na primeira menção, para o filtro de termos técnicos do pacote Q2. A leitura não tinha notas do modelo.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 3 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
