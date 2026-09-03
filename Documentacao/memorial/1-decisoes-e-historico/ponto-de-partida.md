<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
# Ponto de partida

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá.

## 1. Ponto de partida

O repositório continha apenas o commit `e854a0e` — a clonagem de um site PHP de terceiro ("Churrascaria Fornalha", cedido por um integrante do grupo para servir de cobaia). As pastas `AgenteCore` e `CobaiaAPI` existiam vazias.

**O primeiro achado condicionou todo o resto do projeto:** o `CobaiaFront` é um monolito PHP que renderiza tudo no servidor e consulta o banco diretamente via `mysqli` — **sem nenhuma chamada `fetch`/AJAX a uma API JSON**. Como o conceito central da pesquisa é *Contract Drift* na fronteira Front-to-Back, não havia fronteira alguma para o agente interceptar. Sem resolver isso, o objeto de estudo não existiria.

Também se constatou que o dump `banco/bancoatualizado.sql` estava incompleto em relação ao código: definia `tbtipos`, `tbprodutos`, `tbusuarios` e a view `vw_tbprodutos`, mas o fluxo de reservas usava `tbpedido_reserva` e `vw_tbpedidos`, inexistentes. E não havia nenhum `INSERT` — o site subia vazio e sem usuário para login.


