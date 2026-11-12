---
# ! Alteração de IA - Revisar: camada de leitura do verbete `ancora-saiba-mais`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/defeitos_conhecidos/ancora-saiba-mais.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
id: ancora-saiba-mais
titulo: Link "Saiba Mais..." abre produto vazio
sistema: CobaiaFront
entidade_principal: Interface
tipo: defeito_conhecido
status: nao_corrigido
arquivos: [Programacao/CobaiaFront/produtos_geral.php, Programacao/CobaiaFront/produto_detalhes.php]
sintomas: [saiba mais abre produto vazio, id_produto vazio na url, link nao encontrado pelo roteiro]
palavras_chave: [saiba mais, ancora, href, aspas, id_produto, produtos_geral, detalhe, link]
causas_relacionadas: [localizador_quebrado, recurso_inexistente, estado_da_tela_divergente]
verbete: defeitos_conhecidos/ancora-saiba-mais.md
hash_do_verbete: b956d35354be4d20
gerado_em: 2026-11-07
curado: sim
---

# Link "Saiba Mais..." abre produto vazio

Camada de leitura do verbete `ancora-saiba-mais` (`biblioteca_producao/defeitos_conhecidos/ancora-saiba-mais.md`). Tipo: defeito_conhecido (um defeito real do código cedido, mantido de propósito); estado: nao_corrigido (defeito sem correção no código cedido); sistema: CobaiaFront (o site PHP); entidade principal: Interface.

## O que é

Nas listagens do site PHP, "Saiba Mais..." abre produto_detalhes.php?id_produto= vazio: a aspa que fecha o href vem antes do id (produtos_geral.php:51); o link da imagem (linha 34) está certo.

## Como aparece na tela

- Saiba Mais leva a produto sem dados.
- roteiro que procura o link pelo id não o encontra.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `saiba mais abre produto vazio`, `id_produto vazio na url`, `link nao encontrado pelo roteiro`.

## O que conferir

Causa, como o verbete a descreve: Defeito do código original, sem correção. Na aba de API o botão é button.saiba-mais[data-id], sem esse problema.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `localizador_quebrado` (Localizador (seletor) quebrado), `recurso_inexistente` (Recurso inexistente (404 e vizinhos)), `estado_da_tela_divergente` (Estado da tela divergente da resposta).

## Onde está no código

- Arquivos: `Programacao/CobaiaFront/produtos_geral.php`, `Programacao/CobaiaFront/produto_detalhes.php`.
- Rotas da API: nenhuma declarada.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `saiba mais`, `ancora`, `href`, `aspas`, `id_produto`, `produtos_geral`, `detalhe`, `link`.

## Notas do modelo

Nenhuma nota do modelo neste verbete.

## Curadoria

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: aprovada como estava.
