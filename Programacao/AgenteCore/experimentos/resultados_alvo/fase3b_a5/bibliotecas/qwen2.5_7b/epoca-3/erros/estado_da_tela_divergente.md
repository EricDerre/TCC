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
sintomas: [api respondeu certo mas a tela nao, carregando parado, lista vazia com resposta cheia, botao continua habilitado apos cancelar, lista vazia, botao que nao muda]
palavras_chave: [tela, estado, divergente, render, renderiza, atualiza, recarregar, filtro, ordem aleatoria, carregando, innerHTML, cancelar, redirect]
causas_relacionadas: [localizador_quebrado, dado_desatualizado, corpo_vazio]
# ! Alteração por modelo qwen2.5:7b (E1, caso efe-4) - Revisar: retificação acrescentada.
# ! Alteração por modelo qwen2.5:7b (E1, caso efe-8) - Revisar: retificação acrescentada.
# ! Alteração por modelo qwen2.5:7b (E1, caso efe-10) - Revisar: retificação acrescentada.
---
## Resumo
A rede está certa — status e corpo conferem — e o usuário vê outra coisa: "Carregando" parado, lista vazia, botão que não muda.

## Sinais
- nenhum erro de console nem status de erro
- recarregar corrige: o estado não foi atualizado

## Causa
produtos_api.php só limpa "Carregando..." no then() do fetch e substitui o grid por innerHTML; na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7).

## Notas do modelo
- [E1 · efe-4 · retificação de "na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7)."] Corrigir a lógica de cancelamento para não depender de redirect, garantindo a atualização do estado da tela. — Motivo: Este caso mostrou que a lógica de atualização da interface não está sincronizada com a resposta da API, evidenciando a necessidade de uma revisão na implementação do cancelamento.
- [E1 · efe-8 · retificação de "na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7)."] Corrigir a implementação do cancelamento para que não dependa apenas do redirect, mas também limpe o estado da tela corretamente. — Motivo: Esta retificação mostra que a implementação atual está incompleta e que o cancelamento deve ser tratado de forma mais robusta, o que pode ajudar a prevenir erros semelhantes no futuro.
- [E1 · efe-10 · retificação de "na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7)."] Corrigir a lógica de cancelamento para não depender do redirect, garantindo que a interface seja atualizada corretamente. — Motivo: Este caso mostrou que a lógica de atualização da interface pode estar incorreta, mesmo com dados corretos na rede. A documentação sobre o estado da tela divergente não foi explicita sobre a necessidade de atualização do DOM.
