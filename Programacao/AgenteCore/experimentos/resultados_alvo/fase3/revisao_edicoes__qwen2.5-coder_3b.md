<!-- ! Alteração de IA - Revisar: planilha de revisão humana das edições que o modelo fez na biblioteca, GERADA por avaliar_fase3.py --gerar-revisao.
     ! Motivo: o harness só consegue medir se a edição é VÁLIDA (formato, tetos, não copiou o caso); se o que foi escrito é verdade sobre o cobaia, só conferindo
     contra o código. Esta planilha existe para esse julgamento e NÃO é sobrescrita: uma nova execução da avaliação encontra o arquivo e o deixa como está. -->
<!-- ! Alteração de IA - Revisar: colunas Avaliação e Comentário preenchidas pelo Claude em 22/09/2026 (primeira passada,
     a pedido do Eric), conferindo cada texto contra o código do cobaia (produtos.py, pedidos.py, fault_injection.py, database.py,
     produtos_api.php, schema_completo.sql, seed.sql), o caso citado (banco_casos*.py) e o verbete original em base_conhecimento/.
     ! Motivo: o Eric pediu que a revisão fosse adiantada pela IA para a análise decisória não ficar com o critério "qualidade das
     edições" em branco; os vereditos são provisórios até ele revisar. Critério aplicado: Correta = verdadeiro sobre o sistema e
     pertinente ao diagnóstico ("redundante" no comentário marca texto que o verbete já dizia); Parcial = vago, recomendação sem fato
     novo, ou verdade fora de lugar; Errada = afirma algo que o código não faz ou atribui a causa a outro componente. -->


# Revisão das edições aceitas — qwen2.5-coder:3b

Amostra determinística de 10 edição(ões) aceita(s), até 10 por época, com ao menos uma de cada operação usada na época.

Como preencher: abra o verbete citado na cópia do modelo (`bibliotecas/qwen2.5-coder_3b/epoca-<Época>/`), leia o texto acrescentado e confira contra o código do cobaia (`Programacao/Cobaia/`). Escreva na coluna **Avaliação** um de:

- `Correta` — o que está escrito é verdade sobre o sistema e ajuda no diagnóstico;
- `Parcial` — é verdade em parte, ou é vago demais para ajudar;
- `Errada` — afirma algo que o código não faz.

Deixe a coluna em branco no que não revisar: a avaliação conta em branco (e qualquer outro valor) como `sem_avaliacao`.

| # | Época | Caso | Verbete | Operação | Texto | Motivo | Avaliação | Comentário |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | lex-2 | corpo_nao_e_json | retificacao | Corrige a descrição para especificar que o parse falha no primeiro caractere. | O caso atual mostra que o erro ocorre no primeiro caractere, mas a descrição anterior não menciona isso. Esta correção ajuda a evitar confusão com outros tipos de erros de parse. | Correta | Redundante: o Resumo do verbete já dizia que o parse falha no primeiro caractere. |
| 2 | 1 | lex-12 | corpo_nao_e_json | retificacao | Ajuste o trecho para "o parse falha no primeiro caractere da resposta". | Este trecho melhor descreve o erro específico que pode ocorrer na análise da resposta, ajudando a evitar confusões futuras. | Correta | Redundante: mesmo conteúdo da linha 1, de novo. |
| 3 | 1 | sin-9 | campo_renomeado | retificacao | Corrigido o campo_renomeado para preencher o contrato esperado. | O campo_renomeado estava causando inconsistências no contrato esperado, tornando o diagnóstico mais preciso para casos futuros. | Parcial | Frase sem conteúdo verificável; não descreve o sistema nem o caso. |
| 4 | 1 | run-11 | dado_desatualizado | retificacao | A API não envia cache, o que pode levar a leituras defasadas. | A evidência deste caso é a descrição da leitura defasada, que mostra que a API não está enviando cache, causando a carga de dados não atualizada. | Errada | Inverte o diagnóstico: a CobaiaAPI lê o banco a cada requisição e não envia cabeçalhos de cache (database.py, pedidos.py); a defasagem vem de proxy ou cache do navegador, não da ausência de cache na API. |
| 5 | 2 | run-14 | dado_desatualizado | retificacao | A CobaiaAPI não envia cache, o que pode levar a leituras defasadas. | A documentação não especifica que a API deve enviar cache, o que pode levar a leituras defasadas. | Errada | Mesma afirmação da linha 4 no caso run-14; a ausência de cache na API não causa leitura defasada. |
| 6 | 2 | lex-13 | contrato-pedido | retificacao | Corrigido o contrato para aceitar apenas 'Em Análise' e 'Cancelado' como status. | O erro estava ocorrendo porque o contrato não especificava os valores permitidos para o status, e o sistema estava retornando 'Em Análise' e 'Cancelado' como valores válidos. A correção agora especifica que apenas esses valores são aceitos. | Correta | Redundante e fora de lugar: o contrato já dizia status 'Em Análise' ou 'Cancelado' (ENUM em schema_completo.sql); lex-13 é corpo vazio, sem relação com status. |
| 7 | 2 | lex-14 | resposta_truncada | retificacao | Corrigir o parsing JSON para lidar com erros de truncamento. | O erro de truncamento pode ser causado por problemas de comunicação, então melhorar o parsing JSON ajuda a evitar erros futuros. | Parcial | Recomendação de mexer no parse; não descreve o sistema nem ajuda a distinguir truncamento (malformed_json em produtos.py, proxy, conexão cortada). |
| 8 | 3 | sin-3 | estrutura_aninhada_divergente | retificacao | Adicione um novo campo "tipo" no contrato de /api/produtos para especificar que o campo deve ser um texto. | O contrato atual não especifica que o campo "tipo" deve ser um texto, o que pode levar a erros de integração futuros. | Errada | O contrato-produto já declara tipo como texto e o campo existe; sin-3 é o tipo vindo como objeto, não campo faltante. |
| 9 | 3 | tra-2 | contrato-pedido | retificacao | O contrato de pedidos permite apenas 'Em Análise' e 'Cancelado' como status. | O trecho "status fora dos dois valores" foi retificado para "status fora do domínio", que é mais preciso e clara. A evidência deste caso é a correção no contrato de pedidos, que agora especifica os valores permitidos para o status. | Correta | Redundante e fora de lugar: já estava no contrato; tra-2 é chave de junção errada (nome do Administrador), sem relação com o domínio de status. |
| 10 | 3 | efe-13 | estado_da_tela_divergente-correto | novo_verbete | Corrigido o erro na limpeza do "Carregando..." no then() do fetch. | O novo verbete explica que o problema ocorre quando o then() limpa "Carregando..." e substitui o grid por innerHTML, o que pode causar a tela de mostrar conteúdo anterior. | Errada | Verbete novo afirma 'corrigido o erro na limpeza do Carregando'; nenhuma correção existe em produtos_api.php. O mecanismo real (cada resposta substitui o grid inteiro e a mais antiga pode chegar por último) ficou só no motivo. |
