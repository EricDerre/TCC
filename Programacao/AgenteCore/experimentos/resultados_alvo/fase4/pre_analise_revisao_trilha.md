<!-- ! Alteração de IA - Revisar: novo (05/11/2026): pré-análise dos 11 relatórios da sessão de revisão da corrida 22, escrita pelo Claude a pedido do Eric, sem abrir o gabarito.
     ! Motivo: o Eric pediu uma pré-análise antes de seguir com a sessão, como fez na planilha do lote da corrida 20. Fica em arquivo separado, fora da página e do painel, porque a adesão apropriada
     (especificação da trilha, seção 12 c) só mede o relatório se o revisor decidir sem ver este parecer; os valores são julgamento do Claude, não medida de corrida. -->
# Pré-análise da revisão dos relatórios da trilha (corrida 22)

**Lida pelo Eric em 05/11/2026, depois de ele responder o relatório 1 (decisão 85).** A partir do relatório 2, a decisão dele mede o relatório mais este parecer, não o relatório sozinho. Depois, o Eric aprovou este parecer para os relatórios 2 a 11 (decisão 86).

Feita pelo Claude (Opus 5.5) em 05/11/2026, com os mesmos campos da ficha da página. Tempo até a decisão não se aplica a mim e fica de fora.

## Como foi feita

- Li os 11 relatórios como a página mostra, com o nome neutro. A árvore completa, só no primeiro; nos outros, ela repete em eventos o que as seções 1 a 5 já trazem, e o subagente que revisou os relatórios antes da publicação leu todas.
- Para os rótulos em disputa, li as definições de `tipo_divergente`, `valor_fora_do_dominio`, `registro_duplicado`, `contagem_inconsistente` e `escala_ou_unidade_errada` na biblioteca de produção, sem as linhas que citam nome de caso.
- Não abri `trilha.md`, `trilha.json`, a planilha, o banco de casos nem a sua resposta já salva. Quando este parecer foi escrito, nada aqui tinha sido conferido contra o gabarito; a conferência, feita depois, está no bloco `tb_f4_revisao_parecer` de `leitura_revisao_trilha.md`.

## A resposta que o Eric já tinha dado

Abri a resposta dele no relatório 1 só depois de escrever este parecer. Os dois aceitam e avaliam como certo; ele dá utilidade 4 e eu, 3. Divergimos em achar o erro: ele marcou sim e eu, não vi erro. Com o diagnóstico certo não há erro do agente para achar, então ele pode ter lido "erro" como o defeito do sistema. A página passou a explicar a pergunta para os relatórios seguintes.

## Limites

- **Não sou um leitor novo.** Escrevi parte do gerador destes relatórios e já vi os nomes dos casos na planilha, o que não dá para desver.
- **Sei quantos erros a amostra tem.** Isso entrou no meu julgamento: depois de achar os óbvios, fui procurar o que faltava entre os que pareciam certos, e o relatório 4 era o único com dois rótulos vizinhos em disputa.
- **Consultei a biblioteca.** Um revisor só com o relatório na mão não teria essas definições, e isso pesa no relatório 4.

## Parecer

| # | Relatório | Causa do agente | Selo | Erro localizado | Decisão | Utilidade | Avaliação | Causa que eu daria | Confiança |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `relatorio-1` | `dado_desatualizado` | alto | n.a. | aceitar | 3 | certo | a mesma | alta |
| 2 | `relatorio-2` | `erro_interno_do_servidor` | médio | n.a. | aceitar | 3 | certo | a mesma | alta |
| 3 | `relatorio-3` | `resposta_truncada` | alto | n.a. | aceitar | 4 | certo | a mesma | alta |
| 4 | `relatorio-4` | `tipo_divergente` | alto | não | recusar | 2 | errado | `valor_fora_do_dominio` | média |
| 5 | `relatorio-5` | `registro_duplicado` | baixo | sim | recusar | 4 | errado | `escala_ou_unidade_errada` | alta |
| 6 | `relatorio-6` | `estrutura_aninhada_divergente` | alto | n.a. | aceitar | 3 | certo | a mesma | alta |
| 7 | `relatorio-7` | `codificacao_incorreta` | baixo | n.a. | aceitar | 3 | certo | a mesma | alta |
| 8 | `relatorio-8` | `tempo_de_resposta_excedido` | médio | sim | recusar | 5 | errado | `localizador_quebrado` | alta |
| 9 | `relatorio-9` | `nulo_inesperado` | alto | n.a. | aceitar | 4 | certo | a mesma | alta |
| 10 | `relatorio-10` | `colecao_no_lugar_de_objeto` | baixo | sim | recusar | 3 | errado | `campo_ausente` | alta |
| 11 | `relatorio-11` | `colecao_no_lugar_de_objeto` | baixo | sim | recusar | 5 | errado | `campo_renomeado` | alta |

## Relatório por relatório

**Relatório 1, aceitar.** O POST criou o pedido 8 e o GET seguinte só traz o 7. O cabeçalho tem `Age: 240` com `max-age=300`, e o pedido aparece depois de alguns minutos: é cache velho. O relatório atrapalha um pouco: a justificativa diz que a causa vem do sinal "corpo nao_json", que só existe porque o caso está escrito em prosa, e o CONFLITO vem de a resposta mudar sem documentação, o que é esperado.

**Relatório 2, aceitar.** Status 500 com `erro interno` no corpo; não há o que disputar. A justificativa fala em "no campo id" enquanto o CAMPO declarado é `nenhum`, e as linhas de campo ausente da tabela são consequência do corpo de erro.

**Relatório 3, aceitar.** O JSON acaba no meio de um texto, e o sintoma só aparece com lista grande. Aqui o sinal em código é real e aponta para a causa. A frase de impacto diz que aparecem os dois primeiros itens, o que ninguém conferiu, mas isso não muda a causa.

**Relatório 4, recusar, com confiança média.** O corpo traz `"destaque": 2` e o contrato pede booleano. A biblioteca separa os dois casos: `tipo_divergente` lista "destaque 1" entre os sintomas e `valor_fora_do_dominio` lista "destaque 2" e diz "destaque diferente de true/false". Pela biblioteca, a causa é a segunda. A dúvida é legítima, porque um número no lugar de booleano também é tipo errado ao pé da letra, e a própria poda classifica assim. O verbete `valor_fora_do_dominio` não veio na busca. **Este é o achado mais importante da pré-análise:** selo alto, sem CONFLITO, todas as conferências certas e a segunda causa com probabilidade zero. Quem lê só o relatório aceita.

**Relatório 5, recusar.** Há um único registro, com `pessoas` 8 onde o POST mandou 4. `registro_duplicado` pede dois registros iguais com ids consecutivos, e não há dois. `escala_ou_unidade_errada` lista "dobro de pessoas" e "quantidade dobrada". O verbete certo não veio na busca e nem aparece entre as alternativas. Aqui o relatório funciona: selo baixo, `causa_sem_verbete_que_a_trate`, três intervenções mudam a resposta e a conferência diz que nenhum verbete trata da causa. Ele avisa do erro, mas não diz qual é a causa certa.

**Relatório 6, aceitar.** O corpo vem como `{"data": {"itens": [...]}}` e o contrato pede lista na raiz. O CONFLITO vem de tirar ou trocar o próprio verbete da causa, o que mostra que ele foi usado, não que a resposta está errada.

**Relatório 7, aceitar.** A observação diz que o cabeçalho declara utf-8 e os bytes estão em latin-1. O selo baixo é falso alarme: sem verbete e sem documentação o modelo fica mais seguro, não menos.

**Relatório 8, recusar.** Nenhuma requisição falhou, o seletor `button.btn-detalhes` não existe na árvore e o botão real é "Saiba Mais...". O tempo esgotado é efeito de não achar o elemento, não a causa. O verbete certo foi entregue; o modelo seguiu as palavras do sintoma. É o melhor caso do relatório: a seção 3 põe `localizador_quebrado` em segundo lugar e a remoção e a troca caem nele.

**Relatório 9, aceitar.** `nome` veio nulo, o contrato pede texto e a saudação sai vazia. A tabela do contrato mostra isso em uma linha. O CONFLITO é falso alarme, de novo porque a resposta muda sem documentação.

**Relatório 10, recusar.** A lista tem dois itens e o segundo não tem `resumo`, o que explica alguns cartões com descrição e outros sem. O verbete do contrato diz que `GET /api/produtos` devolve lista, então `colecao_no_lugar_de_objeto` não faz sentido. O relatório só ajuda a duvidar, com selo baixo e CONFLITO. Ele ainda tranquiliza no lugar errado: a poda diz "sem diferença" porque `poda.diff_contrato` compara só o primeiro item da lista.

**Relatório 11, recusar.** O corpo traz `imagem_url` no lugar de `imagem`. A poda diz `imagem:renomeado`, a tabela mostra a troca e o verbete `campo_renomeado` foi entregue. Mesmo assim o modelo respondeu `colecao_no_lugar_de_objeto`, com probabilidade 0,30. A própria justificativa se contradiz, e a recusa sai em segundos.

## O que se repete

- **Onde o erro começa.** Nos relatórios 4, 5 e 10, a busca não trouxe o verbete da causa certa, e o relatório mostra o que veio, nunca o que faltou. Nos relatórios 8 e 11, o verbete veio e o erro é do modelo.
- **O CONFLITO separa pouco.** Pelo meu julgamento ele acerta nos relatórios 5, 8, 10 e 11, dá falso alarme nos relatórios 1, 6 e 9 e não aparece no relatório 4. Os falsos alarmes vêm todos de a documentação pesar, o que alimenta a ficha 39.
- **Justificativa por molde.** Ela cita sinal falso nos relatórios 1 e 5 e um campo que não é o declarado no relatório 2. Quem lê isso perde confiança no resto.
- **Linha de ação.** É praticamente a mesma frase nos 11 e não ajuda em nenhum.
- **O que decide.** As seções 1 e 2 bastam quase sempre, a seção 3 decide no relatório 8, a tabela de conferências da seção 4 só importa no relatório 5 e a árvore completa não decide nenhum.

Meus cinco recusados são compatíveis com as contagens agregadas de `tb_f4_trilha_sinais`, de erros pegos pela divergência e pelo selo baixo. Isso é só coerência, não conferência contra o gabarito.

## Achados para depois da sessão

Nenhum foi mudado durante a sessão, porque isso misturaria versões. Os defeitos 1 e 3 foram consertados depois dela (decisão 89).

1. **A poda só compara o primeiro item de uma lista** (`amostra = dado[0]` em `poda.diff_contrato`). Um defeito em outro item sai como "sem diferença".
2. **O relatório não avisa quando a causa certa ficou fora das alternativas**, como nos relatórios 4 e 5.
3. **A biblioteca e a poda discordavam em `destaque: 2`:** a biblioteca chama de valor fora do domínio, a poda chamava de tipo diferente, e a justificativa do relatório citava esse sinal. **Correção:** eu tinha escrito aqui que esse sinal empurrava o modelo para o rótulo errado. Isso estava errado: nos casos de texto, o prompt leva o corpo inteiro, e o resultado da poda não chega ao modelo.
