---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: o charset é fixado em três pontos (connect.php, config.py, schema); conferido.
id: codificacao_incorreta
titulo: Codificação de caracteres incorreta
sistema: Ambos
entidade_principal: Infraestrutura
tipo: erro
status: ativo
causa_raiz: codificacao_incorreta
arquivos: [Programacao/CobaiaFront/conn/connect.php, Programacao/CobaiaAPI/app/config.py, Programacao/CobaiaFront/banco/schema_completo.sql]
sintomas: [acentos trocados por simbolos, caracteres estranhos nos nomes, texto legivel mas com acentos errados]
palavras_chave: [codificacao, encoding, utf-8, utf8, latin-1, acento, mojibake, charset, duplo, ã, Ã]
causas_relacionadas: [corpo_nao_e_json, tipo_divergente]
---
## Resumo
JSON válido e estrutura certa, mas textos com acento corrompidos: bytes latin-1 declarados utf-8, ou utf-8 convertido duas vezes ("Pão" vira "PÃ£o").

## Sinais
- só campos de texto livre afetados; números e chaves intactos
- parte dos registros certa e parte errada: conversão dupla parcial

## Causa
Banco e conexões em utf8 (connect.php:7, config.py); se corrompe, o dado foi gravado errado ou um intermediário reconverteu.
