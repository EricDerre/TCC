---
# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
# ! Motivo: um verbete por rótulo do conjunto fechado, com o ponto real do código que
# produz o sintoma neste sistema; conferido em connect.php e produtos_api.php.
id: corpo_nao_e_json
titulo: Corpo não é JSON
sistema: Ambos
entidade_principal: Infraestrutura
tipo: erro
status: ativo
causa_raiz: corpo_nao_e_json
arquivos: [Programacao/CobaiaFront/conn/connect.php, Programacao/CobaiaFront/produtos_api.php]
sintomas: [token inesperado no inicio da resposta, html no lugar de json, warning do php antes do json, resposta html, texto legivel antes do json, xml ou aviso em texto]
palavras_chave: [json, html, xml, parse, token inesperado, warning, fatal, gateway, proxy, atencao erro, content-type, parse falha, primeiro caractere]
causas_relacionadas: [resposta_truncada, corpo_vazio, erro_interno_do_servidor]
# ! Alteração por modelo qwen2.5-coder:3b (E1, caso lex-2) - Revisar: retificação acrescentada.
# ! Alteração por modelo qwen2.5-coder:3b (E1, caso lex-12) - Revisar: retificação acrescentada.
---
## Resumo
A resposta chega (às vezes 200 e Content-Type application/json), mas o corpo é HTML, XML ou aviso em texto — o parse falha no primeiro caractere.

## Sinais
- console "Unexpected token <"
- texto legível antes ou no lugar do JSON: Warning do PHP, página de gateway, "Atenção ERRO"

## Causa
Falha de conexão no site imprime "Atenção ERRO" em HTML (connect.php:16); Warning/Fatal do PHP saem antes da saída; gateway fora devolve a própria página.

## Notas do modelo
- [E1 · lex-2 · retificação de "o parse falha no primeiro caractere"] Corrige a descrição para especificar que o parse falha no primeiro caractere. — Motivo: O caso atual mostra que o erro ocorre no primeiro caractere, mas a descrição anterior não menciona isso. Esta correção ajuda a evitar confusão com outros tipos de erros de parse.
- [E1 · lex-12 · retificação de "o parse falha no primeiro caractere"] Ajuste o trecho para "o parse falha no primeiro caractere da resposta". — Motivo: Este trecho melhor descreve o erro específico que pode ocorrer na análise da resposta, ajudando a evitar confusões futuras.
