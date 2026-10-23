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
sintomas: [numero como texto, booleano como Sim, destaque 1, ordenacao errada, soma errada]
palavras_chave: [tipo, texto, string, numero, booleano, Sim, aspas, type_drift, str, virgula decimal]
causas_relacionadas: [valor_fora_do_dominio, formato_de_data_divergente, escala_ou_unidade_errada]
---
## Resumo
Chave certa com o tipo JSON errado: número entre aspas ("89.90"), booleano como texto ("Sim") ou número (1), inteiro como texto ("4").

## Sinais
- texto numérico com ponto ainda formata; a falha aparece ao ordenar ou somar
- "89,90" com vírgula não converte; destaque fora de true/false sai literal

## Causa
O modo type_drift aplica str() ao campo-alvo (fault_injection.py:76). A API converte DECIMAL em número e 'Sim'/'Não' em booleano (_to_dict).
