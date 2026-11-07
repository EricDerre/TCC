---
# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (defeito conhecido).
# ! Motivo: defeito real do código cedido, mantido de propósito; a linha 34 do mesmo
# arquivo está certa e serve de contraste. Conferido em produtos_geral.php.
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
---
## Resumo
Nas listagens do site PHP, "Saiba Mais..." abre produto_detalhes.php?id_produto= vazio: a aspa que fecha o href vem antes do id (produtos_geral.php:51); o link da imagem (linha 34) está certo.

## Sinais
- Saiba Mais leva a produto sem dados
- roteiro que procura o link pelo id não o encontra

## Causa
Defeito do código original, sem correção. Na aba de API o botão é button.saiba-mais[data-id], sem esse problema.
