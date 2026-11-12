---
# ! Alteração de IA - Revisar: camada de leitura do verbete `codificacao_incorreta`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/codificacao_incorreta.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
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
verbete: erros/codificacao_incorreta.md
hash_do_verbete: 52c73286a5157da8
gerado_em: 2026-11-07
curado: sim
---

# Codificação de caracteres incorreta

Camada de leitura do verbete `codificacao_incorreta` (`biblioteca_producao/erros/codificacao_incorreta.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: Ambos (o site PHP e a API); entidade principal: Infraestrutura. Trata da causa `codificacao_incorreta` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

JSON válido e estrutura certa, mas textos com acento corrompidos: bytes latin-1 declarados utf-8, ou utf-8 convertido duas vezes ("Pão" vira "PÃ£o").

## Como aparece na tela

- só campos de texto livre afetados; números e chaves intactos.
- parte dos registros certa e parte errada: conversão dupla parcial.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `acentos trocados por simbolos`, `caracteres estranhos nos nomes`, `texto legivel mas com acentos errados`.

## O que conferir

Causa, como o verbete a descreve: Banco e conexões em utf8 (connect.php:7, config.py); se corrompe, o dado foi gravado errado ou um intermediário reconverteu.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `corpo_nao_e_json` (Corpo não é JSON), `tipo_divergente` (Tipo divergente).

## Onde está no código

- Arquivos: `Programacao/CobaiaFront/conn/connect.php`, `Programacao/CobaiaAPI/app/config.py`, `Programacao/CobaiaFront/banco/schema_completo.sql`.
- Rotas da API: nenhuma declarada.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `codificacao`, `encoding`, `utf-8`, `utf8`, `latin-1`, `acento`, `mojibake`, `charset`, `duplo`, `ã`, `Ã`.

## Notas do modelo

Nenhuma nota do modelo neste verbete.

## Curadoria

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: aprovada como estava.
