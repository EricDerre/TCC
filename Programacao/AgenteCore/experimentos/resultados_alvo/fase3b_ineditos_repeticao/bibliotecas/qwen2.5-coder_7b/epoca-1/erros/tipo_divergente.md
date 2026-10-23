---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: type_drift converte com str(); texto numérico ainda formata na tela, então o
# sintoma aparece em ordenação/soma. Conferido em fault_injection.py e produtos_api.php.
id: tipo_divergente
titulo: Tipo divergente
sistema: CobaiaAPI
entidade_principal: Produto
tipo: erro
status: ativo
causa_raiz: tipo_divergente
arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/routers/produtos.py]
endpoints: [GET /api/produtos, GET /api/pedidos]
sintomas: [numero como texto, booleano como Sim, destaque 1, ordenacao errada, soma errada, preco como texto, destaque como texto]
palavras_chave: [tipo, texto, string, numero, booleano, Sim, aspas, type_drift, str, virgula decimal, conversao de tipos, api, json]
causas_relacionadas: [valor_fora_do_dominio, formato_de_data_divergente, escala_ou_unidade_errada]
# ! Alteração por modelo qwen2.5-coder:7b (E1, caso semt-13) - Revisar: retificação acrescentada.
---
## Resumo
Chave certa com o tipo JSON errado: número entre aspas ("89.90"), booleano como texto ("Sim") ou número (1), inteiro como texto ("4").

## Sinais
- texto numérico com ponto ainda formata; a falha aparece ao ordenar ou somar
- "89,90" com vírgula não converte; destaque fora de true/false sai literal

## Causa
O modo type_drift aplica str() ao campo-alvo (fault_injection.py:76). A API converte DECIMAL em número e 'Sim'/'Não' em booleano (_to_dict).

## Notas do modelo
- [E1 · semt-13 · retificação de "O modo type_drift aplica str() ao campo-alvo"] Ajustar a função de conversão de tipos para garantir que os valores sejam retornados no formato correto conforme o contrato. — Motivo: A evidência deste caso mostrou que a função de conversão de tipos estava aplicando str() ao campo-alvo, o que resultava em valores incorretamente formatados. A correção desta função deve resolver o problema de exibição incorreta dos preços.
