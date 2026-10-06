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
sintomas: [token inesperado no inicio da resposta, html no lugar de json, warning do php antes do json, pagina html de erro 404, falha de parse, fatal error, memoria esgotada, resposta html, falha ao acessar de fora da rede local, resposta html em vez de json, falha em ambientes externos]
palavras_chave: [json, html, xml, parse, token inesperado, warning, fatal, gateway, proxy, atencao erro, content-type, resposta json, erro 404, erro de memoria, php, conexao, resposta html, erro de integracao, ambiente externo, erro 500]
causas_relacionadas: [resposta_truncada, corpo_vazio, erro_interno_do_servidor]
# ! Alteração por modelo qwen2.5-coder:7b (E1, caso lex-6) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5-coder:7b (E2, caso lex-12) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5-coder:7b (E2, caso lex-15) - Revisar: nota acrescentada.
# ! Alteração por modelo qwen2.5-coder:7b (E3, caso lex-15) - Revisar: nota acrescentada.
---
## Resumo
A resposta chega (às vezes 200 e Content-Type application/json), mas o corpo é HTML, XML ou aviso em texto — o parse falha no primeiro caractere.

## Sinais
- console "Unexpected token <"
- texto legível antes ou no lugar do JSON: Warning do PHP, página de gateway, "Atenção ERRO"

## Causa
Falha de conexão no site imprime "Atenção ERRO" em HTML (connect.php:16); Warning/Fatal do PHP saem antes da saída; gateway fora devolve a própria página.

## Notas do modelo
- [E1 · lex-6 · nota] Adicionar nota: A resposta deve ser um JSON válido, não uma página HTML de erro. — Motivo: A documentação atual não destaca que a resposta deve ser JSON, o que pode levar a diagnósticos incorretos quando a resposta não atende a este formato esperado.
- [E2 · lex-12 · nota] Adicionar nota: Erros de memória em PHP podem causar respostas HTML inválidas, interrompendo a exibição de dados JSON. — Motivo: O erro de memória em PHP (Fatal error: Allowed memory size exhausted) é uma causa comum de respostas HTML inválidas, o que corresponde ao sintoma observado.
- [E2 · lex-15 · nota] Adicionar nota explicando que a resposta deve ser JSON válido, não uma página HTML de erro. — Motivo: A nota ajudará a identificar rapidamente a causa da falha, que é a resposta HTML em vez de JSON, especialmente quando a resposta é 200 e o Content-Type indica JSON.
- [E3 · lex-15 · nota] Adicionar nota explicando que erros de resposta HTML podem ocorrer em ambientes externos devido a falhas no servidor ou gateway. — Motivo: Esta nota ajuda a entender que a falha não é exclusiva do ambiente local, mas também pode afetar ambientes externos, explicando a inconsistência observada.
