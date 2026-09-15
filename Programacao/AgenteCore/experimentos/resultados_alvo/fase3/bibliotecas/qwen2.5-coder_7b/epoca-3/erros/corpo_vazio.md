---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: separa "sem corpo" de "lista vazia", que a página trata de forma diferente;
# conferido em produtos_api.php.
id: corpo_vazio
titulo: Corpo vazio
sistema: Ambos
entidade_principal: Infraestrutura
tipo: erro
status: ativo
causa_raiz: corpo_vazio
arquivos: [Programacao/CobaiaFront/produtos_api.php]
sintomas: [carregando indefinidamente, tela em branco sem erro, fim inesperado da entrada em corpo vazio, tabela de reservas vazia, erro de carregamento, pagina de carregamento indefinido, dados nao retornados]
palavras_chave: [vazio, sem corpo, branco, 204, espacos, nenhum byte, carregando, resposta vazia, erro de integracao, erro interno, rota errada]
causas_relacionadas: [resposta_truncada, corpo_nao_e_json, estado_da_tela_divergente]
# ! Alteração por modelo qwen2.5-coder:7b (E1, caso lex-13) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5-coder:7b (E3, caso lex-3) - Revisar: nota acrescentada.
---
## Resumo
Status de sucesso e nenhum byte útil no corpo (vazio, só espaços, ou 204). Diferente de "[]", lista vazia, que é JSON válido.

## Sinais
- resp.json() falha em zero caracteres: "Erro ao carregar produtos" ou "Carregando..." parado
- "[]" mostra "Nenhum produto retornado pela API."

## Causa
Nenhuma rota da CobaiaAPI devolve 204 nem corpo vazio; se chega vazio, foi cortado antes de sair (servidor, proxy) ou a rota errada respondeu.

## Notas do modelo
- [E1 · lex-13 · nota] Adicionar nota: "Ocorre quando a API retorna uma resposta vazia, que pode ser devido a um erro interno ou a uma rota errada." — Motivo: Esta nota ajuda a identificar a causa raiz do problema, que é um corpo vazio, e fornece contexto sobre onde pode ocorrer.
- [E3 · lex-3 · nota] Adicionar nota explicando que o corpo vazio pode ser causado por erros internos ou rotas incorretas. — Motivo: Esta nota ajuda a identificar rapidamente a causa do problema, facilitando o diagnóstico em casos sem corpo JSON válido.
