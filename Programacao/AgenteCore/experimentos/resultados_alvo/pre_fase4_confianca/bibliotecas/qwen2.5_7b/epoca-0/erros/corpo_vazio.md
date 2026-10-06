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
sintomas: [carregando indefinidamente, tela em branco sem erro, fim inesperado da entrada em corpo vazio]
palavras_chave: [vazio, sem corpo, branco, 204, espacos, nenhum byte, carregando]
causas_relacionadas: [resposta_truncada, corpo_nao_e_json, estado_da_tela_divergente]
---
## Resumo
Status de sucesso e nenhum byte útil no corpo (vazio, só espaços, ou 204). Diferente de "[]", lista vazia, que é JSON válido.

## Sinais
- resp.json() falha em zero caracteres: "Erro ao carregar produtos" ou "Carregando..." parado
- "[]" mostra "Nenhum produto retornado pela API."

## Causa
Nenhuma rota da CobaiaAPI devolve 204 nem corpo vazio; se chega vazio, foi cortado antes de sair (servidor, proxy) ou a rota errada respondeu.
