---
# ! Alteração de IA - Revisar: camada de leitura do verbete `campo_preco_ausente`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/aprendidos/campo_preco_ausente.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 3 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: conferido em Programacao/CobaiaFront/produtos_api.php (função formatarPreco, linhas 64 a 66): sem o campo, o botão do preço mostra só "undefined", nunca "R$ undefined", e não é o botão de compra nem o de detalhes; e "frontend" estava sem o significado na primeira menção; a linha reproduz o campo arquivos do cabeçalho, que neste verbete está vazio; o arquivo apontado pelo analista é o certo, mas não está no cabeçalho, e a busca não o lê de lá; o que foi revisado é a leitura; o verbete que o modelo lê não mudou; e "frontend" estava sem o significado.
id: campo_preco_ausente
titulo: Campo preço ausente
sistema: CobaiaFront
entidade_principal: Produto
tipo: aprendido
status: ativo
sintomas: [botao com valor undefined, precos ausentes na interface]
palavras_chave: [campo ausente, preco, interface web]
causas_relacionadas: [campo_ausente]
verbete: aprendidos/campo_preco_ausente.md
hash_do_verbete: 033362ffdd5f6cfc
gerado_em: 2026-11-07
curado: sim
---

# Campo preço ausente

Camada de leitura do verbete `campo_preco_ausente` (`biblioteca_producao/aprendidos/campo_preco_ausente.md`). Tipo: aprendido (escrito pelo modelo a partir de um caso, nas Fases 3 e 4, e aceito pela validação em código e pela revisão); estado: ativo (em vigor); sistema: CobaiaFront (o site PHP); entidade principal: Produto.

## O que é

A omissão da chave `preco` no objeto da API faz com que o botão do preço, na página `produtos_api.php`, mostre o texto `undefined` no lugar do valor formatado.

## Como aparece na tela

- botao com valor undefined.
- precos ausentes na interface.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `botao com valor undefined`, `precos ausentes na interface`.

## O que conferir

O verbete não descreve a causa nem como confirmar; confira pelos sinais acima e pelos arquivos abaixo.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `campo_ausente` (Campo ausente).

## Onde está no código

- Arquivos: nenhum declarado no cabeçalho do verbete. A página que mostra o preço é `Programacao/CobaiaFront/produtos_api.php` (apontada pelo analista na curadoria e conferida no código).
- Rotas da API: nenhuma declarada.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `campo ausente`, `preco`, `interface web`.

## Notas do modelo

Nenhuma nota do modelo neste verbete.

## Curadoria

Leitura revisada e aprovada. A definição do sintoma foi refinada para detalhar a exibição do texto `undefined` na página, e o arquivo `produtos_api.php` foi apontado em "Onde está no código".

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 3 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
