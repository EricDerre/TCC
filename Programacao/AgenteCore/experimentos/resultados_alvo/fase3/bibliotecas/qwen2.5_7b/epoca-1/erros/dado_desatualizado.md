---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: a API lê o banco a cada requisição e não envia cabeçalhos de cache; a
# defasagem entre painel PHP e API é o sinal de cache intermediário. Conferido.
id: dado_desatualizado
titulo: Dado desatualizado (cache)
sistema: Infraestrutura
entidade_principal: Infraestrutura
tipo: erro
status: ativo
causa_raiz: dado_desatualizado
arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/database.py]
endpoints: [GET /api/pedidos, GET /api/produtos]
sintomas: [reserva nova nao aparece, cancelamento volta a ativo ao recarregar, produto novo demora a aparecer, status inconsistente, reserva cancelada aparecendo como ativa]
palavras_chave: [cache, desatualizado, velho, antigo, Age, Cache-Control, max-age, defasagem, minutos, stale, api, get, php]
causas_relacionadas: [estado_da_tela_divergente, registro_duplicado, contagem_inconsistente]
# ! Alteração por modelo qwen2.5:7b (E1, caso run-11) - Revisar: retificação acrescentada.
---
## Resumo
Uma escrita confirmada (201/200) não aparece na leitura seguinte e surge minutos depois sem nova ação — a leitura veio de uma cópia antiga.

## Sinais
- cabeçalhos Age ou Cache-Control: max-age no GET
- o painel PHP (lê o banco direto) já mostra o dado; só a API atrasa

## Causa
A CobaiaAPI consulta o banco a cada requisição (database.py) e não envia cache; leitura defasada indica proxy ou cache do navegador entre a página e a API.

## Notas do modelo
- [E1 · run-11 · retificação de "Sinais: cabeçalhos Age ou Cache-Control: max-age no GET; o painel PHP (lê o banco direto) já mostra o dado; só a API atrasa."] Adicionar "A leitura defasada indica que a API está lendo dados antigos do banco, enquanto o painel PHP atualiza em tempo real." — Motivo: Este texto destaca a causa raiz do problema, mostrando que a desatualização dos dados é devido à API ler dados antigos do banco, enquanto o painel PHP atualiza em tempo real, o que não foi evidente no caso original.
