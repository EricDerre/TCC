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
palavras_chave: [seletor, localizador, css, xpath, id, classe, data-id, texto, ambiguo, unico, nth-child, ordem, roteiro, timeout, elemento, ambiguidade]
causas_relacionadas: [estado_da_tela_divergente, recurso_inexistente]
# ! Alteração por modelo qwen2.5:7b (E1, caso efe-12) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5:7b (E2, caso efe-12) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5:7b (E2, caso efe-12) - Revisar: retificação acrescentada.
---
## Resumo
Nenhuma requisição falhou: o roteiro não acha o elemento (seletor não casa) ou acha mais de um (ambíguo). O problema é o localizador, não o dado.

## Sinais
- "Ver mais" vs "Saiba Mais...", data-produto vs data-id: texto ou atributo inexistente
- nth-child que funciona às vezes: ordem não garantida

## Causa
Elementos reais de produtos_api.php: #produtos-api-grid, .thumbnail, button.saiba-mais[data-id], #modalDetalhe; a lista da API não tem ORDER BY (produtos.py:38).

## Notas do modelo
- [E1 · efe-12 · nota] Adicionado que o localizador pode ser ambíguo, encontrando mais de um elemento com o mesmo seletor. — Motivo: Este caso mostrou que o diagnóstico precisa considerar a ambiguidade no seletor, o que não estava claro na documentação original.
- [E2 · efe-12 · nota] Adicionar que o seletor pode ser ambíguo, encontrando mais de um elemento com o mesmo seletor. — Motivo: Este caso mostrou que a documentação não abrangia a possibilidade de um seletor ser ambíguo, encontrando mais de um elemento, o que pode causar erros na integração.
- [E2 · efe-12 · retificação de "o roteiro não acha o elemento (seletor não casa) ou acha mais de um (ambíguo). O problema é o localizador, não o dado."] Corrigir para "o roteiro não acha o elemento (seletor não casa) ou acha mais de um (ambíguo). O problema é o localizador, não o dado. A lista da API não tem ORDER BY (produtos.py:38)." — Motivo: Este caso mostrou que a documentação não mencionava explicitamente que a falta de ORDER BY na API pode causar ambiguidade nos seletores, o que pode levar a erros na integração.
