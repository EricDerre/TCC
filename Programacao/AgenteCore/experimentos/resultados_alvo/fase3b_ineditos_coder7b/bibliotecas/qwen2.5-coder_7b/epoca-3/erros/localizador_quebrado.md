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
sintomas: [elemento nao encontrado, tempo esgotado procurando elemento, seletor casou dois elementos, texto do botao diferente, elementos reais de produtos_api.php, lista da api nao tem order by, roteiro nao localiza elementos, botoes desabilitados, confusao, tempo de resposta excedido, localizador quebrado, botoes de preco desabilitados]
palavras_chave: [seletor, localizador, css, xpath, id, classe, data-id, texto, ambiguo, unico, nth-child, ordem, roteiro, timeout, seletores, elementos, api, localizacao, ambiguidade, order by]
causas_relacionadas: [estado_da_tela_divergente, recurso_inexistente]
# ! Alteração por modelo qwen2.5-coder:7b (E1, caso efe-6) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5-coder:7b (E1, caso efe-9) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5-coder:7b (E1, caso efe-12) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5-coder:7b (E2, caso efe-6) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5-coder:7b (E3, caso efe-12) - Revisar: nota acrescentada.
---
## Resumo
Nenhuma requisição falhou: o roteiro não acha o elemento (seletor não casa) ou acha mais de um (ambíguo). O problema é o localizador, não o dado.

## Sinais
- "Ver mais" vs "Saiba Mais...", data-produto vs data-id: texto ou atributo inexistente
- nth-child que funciona às vezes: ordem não garantida

## Causa
Elementos reais de produtos_api.php: #produtos-api-grid, .thumbnail, button.saiba-mais[data-id], #modalDetalhe; a lista da API não tem ORDER BY (produtos.py:38).

## Notas do modelo
- [E1 · efe-6 · nota] Adicionar nota explicando que o localizador pode ser quebrado devido à ausência de ORDER BY na lista da API, o que pode causar problemas de localização de elementos. — Motivo: Esta nota ajudará a identificar que o problema está no localizador e não nos dados, explicando a causa raiz do erro.
- [E1 · efe-9 · nota] Adicionar exemplos de seletores corretos para diferentes elementos na documentação. — Motivo: A evidência deste caso mostrou que o problema estava no localizador, não no dado, e que a documentação não tinha exemplos claros de como selecionar elementos corretamente.
- [E1 · efe-12 · nota] Adicionar nota sobre seletores quebrados e ambiguidade em elementos. — Motivo: A notificação ajudará a identificar problemas de seletores quebrados e ambiguidade em elementos, facilitando a correção desses problemas.
- [E2 · efe-6 · nota] Adicionar ORDER BY na consulta SQL em produtos.py para garantir a ordem dos produtos na lista. — Motivo: A ausência de ORDER BY na lista da API pode causar problemas de localização de elementos, como o localizador quebrado, resultando em tempo de resposta excedido.
- [E3 · efe-12 · nota] Adicionar nota explicando que seletores como nth-child podem ser ambíguos e que a ausência de ORDER BY na lista da API pode causar problemas de localização de elementos. — Motivo: Esta nota ajudará a explicar a causa raiz da falha e fornecerá exemplos de seletores corretos para diferentes elementos, melhorando a documentação e evitando falhas semelhantes no futuro.
