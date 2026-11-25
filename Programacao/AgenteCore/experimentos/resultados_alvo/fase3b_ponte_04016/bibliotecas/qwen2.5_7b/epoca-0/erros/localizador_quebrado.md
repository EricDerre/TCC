---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: lista os seletores REAIS da página e a ausência de ORDER BY que torna a
# posição dos cartões instável. Conferido em produtos_api.php e produtos.py:38.
id: localizador_quebrado
titulo: Localizador (seletor) quebrado
sistema: CobaiaFront
entidade_principal: Interface
tipo: erro
status: ativo
causa_raiz: localizador_quebrado
arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/produtos_geral.php]
sintomas: [elemento nao encontrado, tempo esgotado procurando elemento, seletor casou dois elementos, texto do botao diferente]
palavras_chave: [seletor, localizador, css, xpath, id, classe, data-id, texto, ambiguo, unico, nth-child, ordem, roteiro, timeout]
causas_relacionadas: [estado_da_tela_divergente, recurso_inexistente]
---
## Resumo
Nenhuma requisição falhou: o roteiro não acha o elemento (seletor não casa) ou acha mais de um (ambíguo). O problema é o localizador, não o dado.

## Sinais
- "Ver mais" vs "Saiba Mais...", data-produto vs data-id: texto ou atributo inexistente
- nth-child que funciona às vezes: ordem não garantida

## Causa
Elementos reais de produtos_api.php: #produtos-api-grid, .thumbnail, button.saiba-mais[data-id], #modalDetalhe; a lista da API não tem ORDER BY (produtos.py:38).
