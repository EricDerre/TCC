---
# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 101 a partir do caso tra-3 (Fase 3).
# ! Motivo: O caso mostrou que a junção entre tabelas estava incorreta, levando a categorias incorretas nos produtos, e a documentação não abordava explicitamente a necessidade de corrigir essa junção.
id: novo_verbete
titulo: Junção de tabelas incorreta
sistema: CobaiaAPI
entidade_principal: Produto
tipo: aprendido
status: ativo
arquivos: [Programacao/CobaiaAPI/app/models.py]
sintomas: [tipo_divergente, chave_de_juncao_errada]
palavras_chave: [juncao, juncao incorreta, juncao de tabelas]
causas_relacionadas: [chave_de_juncao_errada]
---
## Resumo
Corrigir a junção entre tbprodutos e tbtipos, garantindo que id_tipo_produto esteja corretamente ligado a tbtipos.id_tipo.

## Sinais
- tipo_divergente
- chave_de_juncao_errada
