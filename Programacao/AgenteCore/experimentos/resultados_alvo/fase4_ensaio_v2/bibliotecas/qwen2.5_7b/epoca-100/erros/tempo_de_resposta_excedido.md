---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: o modo latency é o único atraso previsto (2 s fixos); o fetch da página não
# define timeout próprio. Conferido em fault_injection.py e produtos_api.php.
id: tempo_de_resposta_excedido
titulo: Tempo de resposta excedido
sistema: Ambos
entidade_principal: Infraestrutura
tipo: erro
status: ativo
causa_raiz: tempo_de_resposta_excedido
arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php]
endpoints: [GET /api/produtos]
sintomas: [demora de segundos, timeout, conexao encerrada por tempo, carregando por muito tempo]
palavras_chave: [timeout, lento, lentidao, demora, latencia, segundos, tempo esgotado, volume, 2 s]
causas_relacionadas: [limite_de_requisicoes, erro_interno_do_servidor, corpo_vazio]
---
## Resumo
A resposta demora além do aceitável ou nunca chega: sem status (conexão encerrada) ou 200 tardio. 429 e 500 respondem rápido com um código — aqui não.

## Sinais
- 200 correto com segundos de espera: atraso no servidor ou no caminho
- sem status, "Failed to fetch": o cliente desistiu antes

## Causa
O modo latency dorme 2 s fixos (fault_injection.py:66); atrasos maiores vêm de banco, rede ou carga; o fetch da página não tem tempo limite.
