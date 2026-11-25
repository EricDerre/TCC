---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: quando a resposta está certa e a tela errada, a causa está no JS ou na
# ausência de atualização; descreve o que o código faz de fato. Conferido em produtos_api.php
# e reserva_cli.php.
id: estado_da_tela_divergente
titulo: Estado da tela divergente da resposta
sistema: CobaiaFront
entidade_principal: Interface
tipo: erro
status: ativo
causa_raiz: estado_da_tela_divergente
arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaFront/cliente/reserva_cli.php]
sintomas: [api respondeu certo mas a tela nao, carregando parado, lista vazia com resposta cheia, botao continua habilitado apos cancelar]
palavras_chave: [tela, estado, divergente, render, renderiza, atualiza, recarregar, filtro, ordem aleatoria, carregando, innerHTML]
causas_relacionadas: [localizador_quebrado, dado_desatualizado, corpo_vazio]
---
## Resumo
A rede está certa — status e corpo conferem — e o usuário vê outra coisa: "Carregando" parado, lista vazia, botão que não muda.

## Sinais
- nenhum erro de console nem status de erro
- recarregar corrige: o estado não foi atualizado

## Causa
produtos_api.php só limpa "Carregando..." no then() do fetch e substitui o grid por innerHTML; na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7).
