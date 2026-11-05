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
sintomas: [api respondeu certo mas a tela nao, carregando parado, lista vazia com resposta cheia, botao continua habilitado apos cancelar, lista vazia, botao que nao muda, carregando..., botao inativo]
palavras_chave: [tela, estado, divergente, render, renderiza, atualiza, recarregar, filtro, ordem aleatoria, carregando, innerHTML, fetch, redirect, cancelar, cliente_cancelar.php]
causas_relacionadas: [localizador_quebrado, dado_desatualizado, corpo_vazio]
# ! Alteração por modelo qwen2.5:7b (E101, caso efe-4) - Revisar: retificação acrescentada.
# ! Alteração por modelo qwen2.5:7b (E101, caso efe-8) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5:7b (E101, caso efe-13) - Revisar: nota acrescentada.
---
## Resumo
A rede está certa — status e corpo conferem — e o usuário vê outra coisa: "Carregando" parado, lista vazia, botão que não muda.

## Sinais
- nenhum erro de console nem status de erro
- recarregar corrige: o estado não foi atualizado

## Causa
produtos_api.php só limpa "Carregando..." no then() do fetch e substitui o grid por innerHTML; na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7).

## Notas do modelo
- [E101 · efe-4 · retificação de "na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7)."] Corrigir a lógica para atualizar o estado corretamente, independentemente de ser uma coleção ou um objeto. — Motivo: Este caso mostrou que a lógica de atualização do estado da tela não está adequada, precisando ser verificada e ajustada para lidar com diferentes tipos de respostas.
- [E101 · efe-8 · nota] Adicionar nota sobre a necessidade de atualização correta do estado da tela após a resposta da API. — Motivo: Este caso mostrou que a documentação não aborda a atualização correta do estado da tela, diferentemente do tratamento do corpo da resposta.
- [E101 · efe-13 · nota] O cancelamento depende de um redirect, o que pode causar divergência na interface. — Motivo: Este caso mostrou que a dependência de redirect para cancelamento pode levar a divergência na interface, mesmo com a resposta correta da API.
