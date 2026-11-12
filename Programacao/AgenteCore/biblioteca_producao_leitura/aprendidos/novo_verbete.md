---
# ! Alteração de IA - Revisar: camada de leitura do verbete `novo_verbete`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/aprendidos/novo_verbete.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 2 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: uma frase colada no fim do item dizia que o cabeçalho traz os sintomas "entidade trocada, dados relacionados nulos, cruzamento indevido"; o cabeçalho do verbete traz `tipo_divergente` e `chave_de_juncao_errada`, como diz a linha logo abaixo, que ficou, e é isso que a busca lê; a nota chamava as épocas de "treinamento"; o texto veio de uma proposta do modelo aceita na biblioteca, e os nomes listados são causas da mesma taxonomia, não de outra; o que foi revisado é a leitura; o verbete que o modelo lê não mudou.
id: novo_verbete
titulo: Junção de tabelas incorreta
sistema: CobaiaAPI
entidade_principal: Produto
tipo: aprendido
status: ativo
arquivos: [Programacao/CobaiaAPI/app/models.py]
sintomas: [tipo_divergente, chave_de_juncao_errada]
palavras_chave: [juncao, juncao incorreta, juncao de tabelas]
causas_relacionadas: [chave_de_juncao_errada]
verbete: aprendidos/novo_verbete.md
hash_do_verbete: c156dcf9871176be
gerado_em: 2026-11-07
curado: sim
---

# Junção de tabelas incorreta

Camada de leitura do verbete `novo_verbete` (`biblioteca_producao/aprendidos/novo_verbete.md`). Tipo: aprendido (escrito pelo modelo a partir de um caso, nas Fases 3 e 4, e aceito pela validação em código e pela revisão); estado: ativo (em vigor); sistema: CobaiaAPI (a API); entidade principal: Produto.

## O que é

A instrução de junção (JOIN) ou o mapeamento ORM vincula colunas incorretas entre tabelas (ex: falha ao ligar id_tipo_produto), resultando em associações indevidas de dados.

## Como aparece na tela

- atributos da entidade relacionada aparecem trocados ou vazios na interface.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `tipo_divergente`, `chave_de_juncao_errada`.

## O que conferir

O verbete não descreve a causa nem como confirmar; confira pelos sinais acima e pelos arquivos abaixo.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `chave_de_juncao_errada` (Chave de junção errada).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/models.py`.
- Rotas da API: nenhuma declarada.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `juncao`, `juncao incorreta`, `juncao de tabelas`.

## Notas do modelo

Nenhuma nota do modelo neste verbete.

## Curadoria

Leitura revisada. O texto original, escrito pelo modelo na época 101 a partir do caso `tra-3`, era uma instrução ("Corrigir a junção") e listava nomes de causas da taxonomia no lugar de sintomas da tela. O conteúdo foi reescrito para um formato descritivo. Nota: Este verbete é um artefato redundante que sobrepõe a causa original chave_de_juncao_errada.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 2 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
