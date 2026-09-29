---
# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5-coder:3b na época 3 a partir do caso efe-13 (Fase 3).
# ! Motivo: O novo verbete explica que o problema ocorre quando o then() limpa "Carregando..." e substitui o grid por innerHTML, o que pode causar a tela de mostrar conteúdo anterior.
id: estado_da_tela_divergente-correto
titulo: Estado da tela divergente corrigido
sistema: Ambos
entidade_principal: Interface
tipo: aprendido
status: ativo
arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaFront/cliente/cliente_cancelar.php]
sintomas: [tela mostra conteudo anterior, recarregar nao corrige]
palavras_chave: [tela divergente, fetch, innerhtml]
causas_relacionadas: [estado_da_tela_divergente]
---
## Resumo
Corrigido o erro na limpeza do "Carregando..." no then() do fetch.

## Sinais
- tela mostra conteudo anterior
- recarregar nao corrige
