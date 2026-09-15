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
sintomas: [token inesperado no inicio da resposta, html no lugar de json, warning do php antes do json, parse_falho, listagem_nao_carrega, pagina de erro html em vez de json, aviso antes do json, parse falho no primeiro caractere]
palavras_chave: [json, html, xml, parse, token inesperado, warning, fatal, gateway, proxy, atencao erro, content-type, erro de sintaxe, parse_falho, aviso, parse falho]
causas_relacionadas: [resposta_truncada, corpo_vazio, erro_interno_do_servidor]
# ! Alteração por modelo qwen2.5:7b (E1, caso lex-2) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5:7b (E1, caso lex-9) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5:7b (E2, caso lex-2) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5:7b (E2, caso lex-2) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5:7b (E3, caso lex-6) - Revisar: nota acrescentada.
---
## Resumo
A resposta chega (às vezes 200 e Content-Type application/json), mas o corpo é HTML, XML ou aviso em texto — o parse falha no primeiro caractere.

## Sinais
- console "Unexpected token <"
- texto legível antes ou no lugar do JSON: Warning do PHP, página de gateway, "Atenção ERRO"

## Causa
Falha de conexão no site imprime "Atenção ERRO" em HTML (connect.php:16); Warning/Fatal do PHP saem antes da saída; gateway fora devolve a própria página.

## Notas do modelo
- [E1 · lex-2 · nota] Adicionar um exemplo de sintoma específico, como "Página de erro HTML em vez de JSON", para melhorar a identificação de casos onde o corpo da resposta não é JSON. — Motivo: Este exemplo mostra que a documentação não abrange casos onde o erro é causado por uma página de erro HTML em vez de JSON, o que pode ser um sintoma comum de problemas de conexão ou falhas do servidor.
- [E1 · lex-9 · nota] Adicionar um exemplo de sintoma para clarificar que XML também pode causar parse falho. — Motivo: Este caso mostrou que XML também pode causar parse falho, mas a documentação não destaca isso.
- [E2 · lex-2 · nota] Adicionar que sintomas podem incluir avisos antes do JSON e parse falhos no primeiro caractere. — Motivo: Este caso mostrou que avisos HTML podem preceder o JSON, causando parse falhos, e que sintomas específicos como esses devem ser documentados.
- [E2 · lex-2 · nota] Adicionar exemplos específicos de sintomas, como "Página de erro HTML em vez de JSON" e "aviso antes do JSON", para melhor identificação de casos onde o corpo da resposta não é JSON. — Motivo: Este caso mostrou que precisamos de exemplos mais detalhados de sintomas para diagnóstico preciso, como avisos antes do JSON e parse falhos no primeiro caractere.
- [E3 · lex-6 · nota] Adicionar que parse falhos podem ocorrer com qualquer tipo de corpo não JSON, não apenas HTML. — Motivo: Este caso mostrou que o parse falho pode ocorrer com respostas HTML, não apenas JSON, precisando ser explicitado na documentação.
