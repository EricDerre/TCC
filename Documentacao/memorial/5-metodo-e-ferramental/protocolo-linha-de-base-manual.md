<!-- ! Alteração de IA - Revisar: documento novo (04/11/2026, Fase 4, pacote P6) com o protocolo da sessão cronometrada da linha de base manual da Fase 5: os dez cenários da ficha 36, como cada um é armado, o que o integrante recebe e pode usar, quando o cronômetro começa e termina, o que conta como corrigido, a planilha, o roteiro do dia e como a comparação com o agente é feita.
     ! Motivo: o plano aprovado da Fase 4 (seção 3.9 e pacote P6) pede o protocolo escrito para a sessão com os integrantes ser marcada com antecedência (ficha 36, decisão 79); sem ele, cada integrante resolveria os cenários de um jeito, com a falha ligada à mão, e o tempo dele não seria comparável ao MTTR do agente medido no ensaio (corrida 21). -->

# Protocolo da linha de base manual (Fase 5)

<!-- ! Alteração de IA - Revisar: (16/11/2026, Fase 5, pacote F2) o protocolo passa à versão 2: o parágrafo de abertura diz a versão, a decisão e o que mudou, e as seções 4 a 8 e 10 foram reescritas (cada uma com a sua tag); as seções 1 a 3 ficam como a versão 1 as deixou, e a 9 ganhou só um aviso.
     ! Motivo: decisão 131 (ficha 73). Na versão 1 o facilitador copiava da tela para a planilha a hora de início e de fim de cada cenário, 60 horários anotados à mão só do lado das pessoas, enquanto o MTTR do agente sai do relógio da máquina; o primeiro cenário medido cronometrava a pessoa aprendendo a forma da resposta; e a lista das 23 causas ia só com os nomes. A versão 2 tem de valer antes de a primeira sessão ser marcada, para os três integrantes passarem pelo mesmo protocolo. -->
Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). Versão 3, de 16/11/2026: as três sessões passam a ser feitas por uma página publicada, uma por integrante (decisão 136), e o que vale para elas está na seção 11. Versão 2, do mesmo dia, escrita no pacote F2 da Fase 5 ([plano aprovado](../../../claude-memoria/plano-aprovado-fase-5.md), seções 4 e 8) pela ficha 73 ([pendências](../pendencias.md), decisão 131). A versão 1, de 04/11/2026, foi escrita no pacote P6 da Fase 4 ([plano aprovado](../../../claude-memoria/plano-aprovado-fase-4.md), seções 3.9 e 5) a partir das fichas 35 e 36 (decisão 79) e do projeto ABNT, seção 3.4. O catálogo dos cenários e as regras de cronômetro e de Task Success vivem no código (`Programacao/AgenteCore/experimentos/cenarios_fase4.py`); o ajudante da sessão é `Programacao/AgenteCore/experimentos/linha_de_base_manual.py`, e os testes dele, `Programacao/AgenteCore/experimentos/testar_linha_de_base.py`. Este documento diz como a sessão roda; nenhum número de resultado está aqui.

**O que mudou na versão 2.** A ferramenta grava o tempo de cada cenário num registro da sessão e preenche a planilha a partir dele; antes dos dez cenários há um treino sem cronômetro; o integrante recebe uma folha com a definição de uma linha de cada uma das 23 causas e responde três perguntas de perfil; e o que o facilitador diz durante um cenário são falas fixas. O limite continua em 10 minutos por cenário, e os pontos em que o cronômetro começa e termina são os mesmos.

**As seções 2 e 3 dizem a resposta de cada cenário: só o facilitador as lê antes da sessão.** Na sessão pela página (seção 11), o integrante recebe só o endereço da página dele, que abre com o tutorial. Na forma presencial, recebe o tutorial antes do dia (seção 4, item 9) e a folha da seção 5 no dia, e nada mais.

## 1. Para que serve

O projeto ABNT (seção 3.4) define a linha de base como os mesmos cenários resolvidos manualmente por integrantes do grupo, com o tempo cronometrado desde a apresentação da falha até a correção do teste, e diz que a comparação entre esse tempo e o MTTR do agente é o resultado central da avaliação. A ficha 36 (decisão 79) fixou três integrantes, cada um nos dez cenários, numa sessão agendada com este protocolo. A ficha 35 (decisão 79) fixou o que é "corrigido": nos cenários de contrato o agente não corrige a API, ele diagnostica, e o resultado é o diagnóstico com a causa e o campo certos; nos de localizador, o roteiro concluído sem erro com um localizador novo. O integrante é medido pela mesma régua.

A sessão não é a Fase 5 inteira: a Fase 5 junta as cinco repetições do agente nos dez cenários e a planilha desta sessão (seção 9).

## 2. Os dez cenários

O catálogo é `cenarios_fase4.CENARIOS_DO_ENSAIO`: seis cenários de contrato no catálogo de `produtos_api.php` (roteiro `api-catalogo`, chamada `GET /api/produtos`), um por modo de falha da CobaiaAPI, e quatro de localizador no front legado, um por roteiro, cada um com um modo de quebra fixo. A ficha 36, opção (a), listava `latency` entre os seis de contrato; a decisão 79 pediu trocar cenários de contrato por modos novos da ficha 28 que cobrissem mais classes, e o catálogo trocou `latency` (que repete a classe 5 do `error_500` e tem o MTTR dominado pela espera do tempo limite) por `escala_ou_unidade_errada` em `preco`, da classe 4, que nenhum dos seis cobria (`cenarios_fase4.TROCA_DA_FICHA_36`). Com a troca, os seis de contrato cobrem as cinco classes de contrato, e a classe 6 (efeito na tela) vem dos quatro de localizador.

| Cenário | Tipo e classe | O que está ligado | Resposta certa |
|---|---|---|---|
| `contrato-malformed_json` | contrato, classe 1 | modo `malformed_json` na CobaiaAPI | causa `resposta_truncada`, campo nenhum |
| `contrato-field_missing` | contrato, classe 2 | modo `field_missing` em `preco` | causa `campo_ausente`, campo `preco` |
| `contrato-field_renamed` | contrato, classe 2 | modo `field_renamed` em `preco` | causa `campo_renomeado`, campo `preco` |
| `contrato-type_drift` | contrato, classe 3 | modo `type_drift` em `preco` | causa `tipo_divergente`, campo `preco` |
| `contrato-escala_ou_unidade_errada` | contrato, classe 4 | modo `escala_ou_unidade_errada` em `preco` | causa `escala_ou_unidade_errada`, campo `preco` |
| `contrato-error_500` | contrato, classe 5 | modo `error_500` | causa `erro_interno_do_servidor`, campo nenhum |
| `localizador-front-busca` | localizador, classe 6 | `id_renomeado`: o campo de busca perde o id `buscar` (vira `buscar_v2`); o roteiro procura `#buscar` | um seletor que ache o campo de busca |
| `localizador-front-admin-login` | localizador, classe 6 | `classe_trocada`: a classe `btn-primary` do botão Entrar vira `btn-entrar`; o roteiro procura `button.btn-primary` | um seletor que ache o botão Entrar |
| `localizador-front-admin-produtos` | localizador, classe 6 | `texto_alterado`: os botões passam de "EXCLUIR" a "EXCLUIR ITEM"; o roteiro procura o botão pelo nome terminado em "EXCLUIR" | um seletor que ache o botão EXCLUIR do primeiro produto |
| `localizador-front-cliente-reserva` | localizador, classe 6 | `estrutura_alterada`: o botão Reservar é envolvido num `div.acoes` e vai para o começo do formulário; o roteiro procura `#reserva_login > input[type=submit]` | um seletor que ache o botão Reservar |

A descrição de cada quebra é a da célula em `cenarios_fase4.QUEBRAS`; a causa e o campo esperados são os de `CENARIOS_DE_CONTRATO`.

## 3. Como cada cenário é armado

O facilitador não liga nada à mão: o ajudante usa as mesmas funções da corrida, para o integrante encontrar a mesma falha que o agente encontrou.

- **`armar`** restaura o banco (`restaurar_banco.restaurar`, conferindo as contagens do seed) e liga a falha. Nos cenários de contrato, `executar_fase4.ligar_modo` faz o `POST /api/admin/fault-mode` com o modo e o campo do cenário e probabilidade 1, como na corrida. Nos de localizador, `cenarios_fase4.armar_quebra` grava no navegador os cookies `quebra` e `quebra_pagina` que a variante PHP do front lê (`Programacao/CobaiaFront/quebra.php`). A corrida 21 arma a quebra pelo harness, no navegador; a corrida 19 mediu as duas formas iguais (mesma árvore de acessibilidade da página quebrada e mesmo resultado em 16 das 16 células, [roadmap §2.11](../roadmap.md), bloco `tb_f4_cura_formas`), e a variante PHP vale em todas as abas que o integrante abrir. Depois o `armar` abre o Chromium do Playwright, com janela, no endereço em que o roteiro começa, e mostra no terminal o material do integrante (seção 5). O Enter no terminal fecha o navegador e desliga a falha.
- **`conferir`** (só localizador) restaura o banco, arma a mesma quebra num navegador sem janela e roda o roteiro do agente com o seletor do integrante em todo passo que usava o localizador quebrado: é a mesma troca da reexecução da cura do agente (`cenarios_fase4.roteiro_com_seletor`) e o mesmo critério (`cenarios_fase4.task_success`, roteiro concluído sem erro). Ele diz "CORRIGIDO" ou "não corrigido" e mostra os segundos da restauração do banco, que saem do cronômetro como saem do MTTR do agente.
- **`desarmar`** volta a CobaiaAPI ao modo normal, para o caso de uma sessão parar no meio.

O cenário é chamado pela vez (`--vez <integrante> <posição>`), e o nome dele, que diz o modo de falha, não aparece na tela. `--cenario <nome>` existe para o ensaio do facilitador.

## 4. Antes do dia

<!-- ! Alteração de IA - Revisar: (16/11/2026, versão 2) o item 1 diz que a ficha é a mesma da corrida 21d; o item 3 diz que o ensaio pelo nome não grava nada e como ensaiar os comandos novos numa pasta de teste; o item 4 diz quem não serve de integrante; o item 5 pede `RESULTADOS_DIR`; os itens 7 e 8 são novos: a folha e o texto fixo que saem por comando, e o cronômetro de reserva (celular e folha de papel).
     ! Motivo: decisão 131 (ficha 73). Com o tempo gravado pela ferramenta, o ensaio do facilitador não pode deixar linhas no registro das três sessões; a folha e o texto fixo saem do código para os três integrantes receberem e ouvirem a mesma coisa; e o cronômetro de reserva é o que vale no cenário em que a ferramenta falhar (plano da Fase 5, seção 4.4). -->
1. **Corrida 21 feita.** A ficha da falha de cada cenário é o que a detecção do agente acusou no ensaio: o campo `motivo_deteccao` de `resultados_alvo/fase4_ensaio/cenarios.jsonl`, que o `armar` lê, e a coluna "O que a detecção acusou" da tabela `tb_f4_cenarios_por_cenario`. Sem a corrida 21, o `armar` avisa que não há ficha. A ficha é o mesmo texto, cenário a cenário, na corrida 21d (`resultados_alvo/fase4_ensaio_v4`), que é a leitura vigente do ensaio: o teste `teste_ficha_da_falha_continua_igual_a_da_corrida_21d` confere os dez.
2. **Ordem e planilha.** `python linha_de_base_manual.py ordem --gravar` sorteia a ordem dos dez cenários de cada integrante com a semente 20261104 (a do integrante n usa a semente mais n), para o que um integrante aprende num cenário se espalhar entre os cenários, e grava a planilha da seção 8. A mesma semente dá sempre a mesma ordem.
3. **Ensaio do facilitador.** Rodar os dez cenários uma vez com `--cenario <nome>`, sem cronômetro, para conferir que cada um abre e que o `conferir` diz "não corrigido" sem seletor. Chamado pelo nome, o ajudante não grava nada no registro da sessão. Os comandos da versão 2 (`perfil`, `treino`, `entregar`, `planilha`) são ensaiados com `--registro fase5_manual_ensaio` e, no `planilha`, com `--planilha <cópia da planilha>`; a pasta do ensaio é apagada depois. O registro de verdade, `resultados_alvo/fase5_manual/sessao.jsonl`, só recebe as três sessões. O comando `python linha_de_base_manual.py ensaio` imprime o passo a passo inteiro, com os comandos dos dez cenários e, para cada cenário de localizador, um seletor que conserta o roteiro (`linha_de_base_manual.SELETOR_DO_ENSAIO`).
4. **Facilitador e integrantes.** O facilitador conduz e não resolve; quem conhece o catálogo de modos de falha (quem escreveu as seções 2 e 3) fica como facilitador, não como integrante. Os três integrantes não conversam sobre os cenários entre as sessões. Quem já leu a lista dos dez cenários ou as causas esperadas (no painel, no README, no documento do TCC ou no repositório) não serve de integrante; se não houver substituto, participa e isso fica declarado na leitura. A pergunta é uma das três de perfil (seção 10).
5. **Máquina.** A máquina-alvo da corrida 21, com o mesmo Chromium da venv do AgenteCore: o `armar` mostra a versão do navegador, que tem de ser a do cabeçalho da corrida 21 (a Fase 5 fixa o navegador, projeto ABNT §3.4), e a grava no registro. Um integrante por vez. As janelas dos comandos precisam de `RESULTADOS_DIR=resultados_alvo`: sem ela o ajudante recusa gravar, para o registro não ir parar em outra pasta.
<!-- ! Alteração de IA - Revisar: (04/11/2026) item novo: a tela de login do front legado volta sozinha para a página inicial depois de 30 s, e o facilitador avisa os integrantes antes de começar.
     ! Motivo: foi o que deixou um cenário sem cura na corrida 21 (meta refresh em `admin/login.php`, roadmap §2.13). Os três cenários de localizador que passam pelo login pegariam o integrante de surpresa, e o cronômetro mediria o susto, não a correção do teste. -->
6. **Aviso aos integrantes.** A tela de login do front legado volta sozinha para a página inicial depois de 30 s (`<meta http-equiv="refresh">` em `admin/login.php`). É comportamento da aplicação, não parte da falha. O facilitador avisa antes de começar: quando isso acontecer, é só reabrir `admin/login.php` no mesmo navegador, e a quebra continua armada, porque os cookies valem para o navegador inteiro.
7. **Folha do integrante e texto do facilitador.** `python linha_de_base_manual.py folha --gravar <arquivo>` grava a folha da seção 5, para imprimir uma por integrante; `python linha_de_base_manual.py falas` mostra o texto fixo da seção 10. Os dois saem do código e não são adaptados de uma sessão para a outra.
8. **Cronômetro de reserva.** Um celular com cronômetro e uma folha de papel com quatro colunas (integrante, posição do cenário, hora de início, hora de fim) ficam com o facilitador a sessão inteira. Eles só valem no cenário em que a ferramenta falhar (seção 6).
<!-- ! Alteração de IA - Revisar: (16/11/2026, à noite, decisão 135) item novo: o tutorial que os três integrantes recebem antes da sessão; a frase do começo do documento sobre o que o integrante recebe passou a citá-lo.
     ! Motivo: o Eric pediu um tutorial para os integrantes entenderem o que fazer. É material que a pessoa lê antes de ser medida, então o protocolo tem de dizer o que ele traz, o que ele não pode trazer e que os três recebem o mesmo texto no mesmo dia; sem isso, cada um chegaria com um preparo diferente. -->
9. **Tutorial do integrante.** Os três integrantes recebem o mesmo tutorial, no mesmo dia, antes da primeira sessão. O texto está em [tutorial-do-integrante.md](tutorial-do-integrante.md), gerado por `python linha_de_base_manual.py tutorial --gravar`, e `tutorial --check` acusa se ele ficar diferente do código. Desde a decisão 136 ele é o tutorial da sessão pela página e abre a página de cada integrante (seção 11), porque os integrantes não abrem o repositório. O tutorial explica os combinados de antes da sessão (não abrir o repositório, o painel, o README nem o documento do TCC; não conversar com os outros integrantes; não usar assistente de IA), como é a sessão, os dois tipos de cenário, os avisos da página, o que pode e o que não pode, como ler o material de um cenário, o passo a passo de cada tipo e o que o botão Começar faz, e repete as 23 causas. Ele não traz nome de cenário, modo de falha, página, seletor ou texto das cobaias: os exemplos são de um sistema inventado, e o exemplo resolvido usa uma causa que não é resposta de nenhum cenário nem do treino (o teste `teste_tutorial_do_integrante_explica_a_sessao_sem_entregar_resposta` confere). Depois que o primeiro integrante o recebe, o texto não muda.

## 5. O que o integrante recebe e o que pode usar

<!-- ! Alteração de IA - Revisar: (16/11/2026, versão 2) a seção passa a entregar ao integrante uma folha que sai do comando `folha` (o bloco abaixo), com o que ele recebe, o que pode e o que não pode, como responde, o limite e a definição de uma linha de cada uma das 23 causas; diz que a biblioteca do agente não é entregue; a resposta passa a ser escrita no bloco de notas; e o treino entra antes dos dez cenários.
     ! Motivo: decisão 131 (ficha 73). Na versão 1 o integrante recebia as 23 causas só pelo nome, e o tempo mediria a pessoa adivinhando o que `chave_de_juncao_errada` quer dizer; e o primeiro cenário medido cronometrava a pessoa aprendendo a forma da resposta. As 23 definições foram escritas no pacote F2 e aceitas pelo Eric como estão em 16/11/2026 (ficha 76, decisão 134): o Apêndice A do documento do TCC, de onde o plano dizia que elas viriam, só traz os nomes das causas e a descrição das seis classes. -->
**Antes do primeiro cenário**, o integrante recebe a folha abaixo, impressa, e fica com ela a sessão inteira. O texto é o que o comando `folha` imprime (`linha_de_base_manual.folha_do_integrante`), colado aqui por `python linha_de_base_manual.py protocolo --colar`; `python linha_de_base_manual.py protocolo --check` acusa se o bloco ficar diferente do código.

<!-- tabela:tb_f5_folha_do_integrante -->
**Folha do integrante.** Fique com esta folha durante a sessão.

**O que é a sessão.** São 10 cenários de teste automatizado, cada um com uma falha armada de propósito. Em cada cenário o teste parou ou acusou um problema, e o seu trabalho é dizer o que quebrou. Mede-se o tempo de cada cenário e se a resposta está certa. O seu nome não entra em nenhum arquivo.

**O que você recebe em cada cenário:**

- a ficha da falha: a frase que o teste automático acusou;
- o roteiro do teste, passo a passo, com o valor de cada preenchimento; nos cenários de localizador, o passo que quebrou vem marcado;
- nos cenários de contrato, o contrato esperado da resposta da API e a lista das 23 causas, que está no fim desta folha;
- o navegador aberto onde o roteiro começa, com as ferramentas do desenvolvedor (F12): elementos, rede e console.

**Pode:** navegar, inspecionar a página, ver as chamadas à API na aba de rede, abrir a API pelo navegador e consultar a documentação de seletores CSS e do Playwright.

**Não pode:** abrir o código das aplicações, o código do agente ou o repositório, usar assistente de IA, ver a planilha do facilitador nem falar com outro integrante sobre os cenários.

**Como responder:**

- Cenário de contrato: uma causa da lista, escrita como está nesta folha, e o campo afetado (ou nenhum). Escreva no bloco de notas ao lado do navegador e avise o facilitador. A entrega é uma só, e o facilitador não diz se está certa.
- Cenário de localizador: um seletor, CSS ou do Playwright, que ache o elemento do passo que quebrou. Escreva no bloco de notas e avise o facilitador, que confere. Se o roteiro não passar, o tempo segue e você pode tentar de novo.

**O tempo.** Começa quando o navegador abre. Para na entrega, no cenário de contrato, ou quando o seletor passa, no de localizador. O limite é de 10 minutos por cenário. Entre um cenário e outro a pausa é livre.

**Um aviso sobre a aplicação.** A tela de login volta sozinha para a página inicial depois de 30 segundos. Isso não é a falha: abra a tela de login de novo no mesmo navegador.

**As 23 causas** dos cenários de contrato. Escolha uma:

1. `corpo_nao_e_json`: a resposta chega, mas o corpo não é JSON: vem uma página HTML ou um texto solto
2. `corpo_vazio`: a resposta chega sem nada no corpo
3. `resposta_truncada`: o corpo começa como JSON e é cortado antes do fim
4. `codificacao_incorreta`: as letras acentuadas chegam trocadas por outros símbolos
5. `campo_ausente`: um campo que o contrato exige não vem na resposta
6. `campo_renomeado`: o valor vem, mas num campo com um nome diferente do que o contrato diz
7. `estrutura_aninhada_divergente`: o campo vem dentro de outro objeto, ou num nível diferente do que o contrato diz
8. `colecao_no_lugar_de_objeto`: vem uma lista onde o contrato pede um objeto só, ou o inverso
9. `tipo_divergente`: o campo vem com um tipo diferente do que o contrato declara
10. `valor_fora_do_dominio`: o tipo está certo, mas o valor não é um dos permitidos, como uma opção que não existe
11. `formato_de_data_divergente`: a data vem escrita num formato diferente do que o contrato pede
12. `nulo_inesperado`: um campo obrigatório vem com o valor nulo
13. `escala_ou_unidade_errada`: o número vem em outra escala ou unidade, como gramas no lugar de quilos
14. `chave_de_juncao_errada`: o registro vem ligado ao item errado de outra tabela
15. `contagem_inconsistente`: a quantidade de itens que vem não é a que deveria vir
16. `tempo_de_resposta_excedido`: a resposta chega certa, mas demora mais do que o tempo aceito
17. `limite_de_requisicoes`: o servidor recusa a chamada por excesso de requisições (status 429)
18. `dado_desatualizado`: a resposta traz um dado antigo, que já mudou no banco
19. `registro_duplicado`: o mesmo registro vem mais de uma vez na resposta
20. `erro_interno_do_servidor`: o servidor falha ao atender a chamada e responde com erro (status 500)
21. `recurso_inexistente`: o endereço ou o registro pedido não existe (status 404)
22. `localizador_quebrado`: a página mudou e o seletor que o teste usa não acha mais o elemento
23. `estado_da_tela_divergente`: a resposta da API está certa, mas a tela mostra outra coisa
<!-- /tabela:tb_f5_folha_do_integrante -->

**Em cada cenário**, o `armar` mostra no terminal:

- a ficha da falha: a frase que a detecção do agente acusou neste cenário na corrida 21 (a conferência ou o passo do roteiro que falhou, ou o que a chamada à API mostrou fora do contrato);
- o roteiro do teste, passo a passo, com o valor de cada preenchimento e, nos cenários de localizador, o passo que quebrou marcado;
- nos cenários de contrato, o contrato esperado de cada produto em `GET /api/produtos` (o mesmo bloco que o agente recebe) e a lista das 23 causas (`taxonomia.CAUSAS_RAIZ`), que a folha explica;

e abre o navegador no ponto em que o roteiro começa, com as ferramentas do desenvolvedor (F12): elementos, rede, console.

A definição de cada causa diz só o que o nome significa, sem campo, página ou forma de armar a falha (`linha_de_base_manual.DEFINICAO_DAS_CAUSAS`). A biblioteca do agente não é entregue: ela está no repositório, que o integrante não pode abrir, e é parte do agente. Essa diferença é uma limitação declarada da comparação (plano da Fase 5, seção 12, item 4).

**Pode** navegar, inspecionar a página, ver as chamadas à API na aba de rede, abrir a API pelo navegador e consultar a documentação de seletores CSS e do Playwright.

**Não pode** abrir o código das cobaias, do agente ou o repositório (o código das cobaias mostra os modos de falha), usar assistente de IA, ver a planilha do facilitador nem falar com outro integrante durante a sessão.

**Entrega**, no contrato, uma causa da lista e o campo afetado (ou "nenhum"), escritos no bloco de notas ao lado do navegador: o facilitador roda o `entregar` e copia de lá. No localizador, um seletor (CSS ou do Playwright) para o elemento do passo que quebrou, também no bloco de notas, que o facilitador copia e confere com o `conferir`. No localizador o integrante pode tentar de novo até o limite de tempo; no contrato a entrega é uma só.

**Treino.** Antes dos dez cenários há um treino sem cronômetro (comando `treino`), com duas partes que não são nenhum dos dez. A primeira é um cenário de contrato com o modo `latency` da CobaiaAPI, que saiu do catálogo pela troca da ficha 36: a resposta chega certa, com atraso, e a resposta do treino é a causa `tempo_de_resposta_excedido`, com campo nenhum. A segunda é um exercício de seletor numa página que não está nos quatro roteiros de localizador: achar o botão "Saiba Mais..." do primeiro produto em `produtos_api.php`, sem quebra armada. Só no treino o facilitador diz a resposta certa. O treino não grava início, entrega nem tentativa: fica só um evento `treino` no registro, dizendo que o integrante treinou.

## 6. O cronômetro

<!-- ! Alteração de IA - Revisar: (16/11/2026, versão 2) quem grava o tempo passa a ser a ferramenta, no registro da sessão: o `armar` grava o início, o comando novo `entregar` grava o fim do cenário de contrato no Enter do facilitador, antes de a causa e o campo serem digitados, e o `conferir` grava cada tentativa de seletor. Entram também o aviso do limite pela janela do `armar`, a vez armada duas vezes e o cronômetro de reserva. Os pontos de começo e de fim e o limite de 10 minutos são os da versão 1.
     ! Motivo: decisão 131 (ficha 73); plano da Fase 5, seção 4.4. O MTTR do agente sai do relógio da máquina, com três casas; a hora que o facilitador copiava da tela (hh:mm:ss) punha, só do lado das pessoas, o erro de leitura e de cópia e o tempo de digitar a resposta. Com o registro, o tempo das pessoas também não é digitado. -->
O tempo é gravado pela ferramenta no registro da sessão, `resultados_alvo/fase5_manual/sessao.jsonl`: uma linha por evento, só acréscimo, com a hora do relógio da máquina em milésimos. O facilitador não anota hora nenhuma na planilha. Os pontos de começo e de fim são os da versão 1, que espelham os do agente.

- **Começa** quando o navegador do `armar` está aberto e o integrante tem o material da seção 5: é o equivalente da detecção, onde o MTTR do agente começa. O `armar --vez` grava o evento `inicio` nesse instante e mostra a hora.
- **Termina, no contrato,** quando o integrante entrega a causa e o campo, com a causa dentro das 23. O facilitador deixa o `entregar --vez` esperando numa terceira janela e dá Enter no instante da entrega: a hora é gravada no Enter (evento `entrega`), antes de a causa e o campo serem digitados (evento `resposta`), para o tempo de digitar não entrar no cronômetro. Causa que não está na lista não para o cronômetro: o `entregar` a recusa. Se foi erro de digitação, o facilitador digita de novo; se o integrante entregou algo que não está na lista, a linha vazia desfaz a entrega e o tempo segue. Acertar ou errar não muda a hora do fim, como no agente: o MTTR dele para no diagnóstico conferido em código, certo ou errado, e o Task Success é que diz se acertou (ficha 35).
- **Termina, no localizador,** quando o `conferir` diz "CORRIGIDO". Cada `conferir --vez --seletor` grava um evento `tentativa` com o seletor, o resultado, a hora em que o roteiro terminou e os segundos de restauração do banco, que saem do cronômetro como saem do MTTR do agente. Cada "não corrigido" conta uma tentativa, e o cronômetro segue.
- **Limite:** 10 minutos por cenário (`linha_de_base_manual.LIMITE_S`). A janela do `armar` avisa quando faltam dois minutos e quando o tempo acaba, com o banco das tentativas já descontado. Estourado o limite, o cenário fica "não corrigido", sem tempo de fim; ele conta no Task Success e fica fora da média do tempo, como as execuções do agente em que o cronômetro não chegou ao fim. O limite pode mudar antes de a primeira sessão ser marcada; depois, vale para os três integrantes.
- **Vez armada duas vezes.** Se o `armar` da mesma vez rodar de novo (navegador fechado por engano, por exemplo), vale o primeiro início: o cronômetro não recomeça, o `armar` avisa na tela, e o facilitador escreve o motivo nas observações.
- **Cronômetro de reserva.** O celular e a folha de papel da seção 4 correm em paralelo: o facilitador dispara o cronômetro quando diz "O tempo está correndo." e anota no papel a hora de início e a de fim de cada cenário. Se a ferramenta falhar num cenário (comando que caiu, registro que não gravou), vale a anotação à mão: o facilitador preenche a linha da planilha com os horários do papel e escreve `anotada à mão` nas observações (seção 8).
- **O que entra no tempo sem ser trabalho do integrante.** O tempo de avisar que entregou e de o facilitador dar Enter ou colar o seletor entra no cronômetro. É uma limitação declarada, e a leitura trata como empate a diferença menor que a folga do cronômetro das pessoas (plano da Fase 5, regra L8 e seção 12, item 10).

## 7. O que conta como corrigido (Task Success)

<!-- ! Alteração de IA - Revisar: (16/11/2026, versão 2) a seção passa a dizer quem faz a conta: o `entregar` no contrato, sem mostrar o resultado na tela, e o `conferir` no localizador. A regra não mudou.
     ! Motivo: decisão 131 (ficha 73). Na versão 1 o corrigido do contrato era preenchido à mão depois da sessão, comparando a resposta com a seção 2; agora sai da mesma função que mede o agente. Ele continua fora da vista do integrante, porque saber se acertou um cenário muda o que a pessoa responde nos seguintes. -->
- **Contrato:** a causa entregue é a causa esperada do cenário (seção 2) e o campo é o esperado: `preco` nos quatro cenários com campo e nenhum nos dois sem campo. É a regra de `cenarios_fase4.task_success_contrato`, a mesma do agente. O `entregar` faz essa conta na hora (`linha_de_base_manual.resultado_da_entrega`) e a grava no registro, sem mostrar na tela: o `corrigido` do contrato só aparece na planilha, preenchida depois que o integrante sai.
- **Localizador:** o `conferir` disse "CORRIGIDO" dentro do limite, isto é, o roteiro do agente, com o seletor do integrante no lugar do quebrado, chegou ao fim sem erro. O resultado é dito na hora, porque o integrante pode tentar de novo.

## 8. A planilha

<!-- ! Alteração de IA - Revisar: (16/11/2026, versão 2) a planilha passa a ser preenchida pelo comando `planilha`, a partir do registro: a tabela diz de onde vem cada coluna, e os parágrafos novos dizem o que o comando nunca faz (trocar célula preenchida), o que é a linha anotada à mão e como se marca a linha anulada. As colunas e o arquivo são os mesmos.
     ! Motivo: decisão 131 (ficha 73); plano da Fase 5, seção 4.5. Na versão 1 o facilitador preenchia à mão o início, o fim, os segundos, o desconto, as tentativas e o corrigido de 30 linhas; cada cópia era uma chance de erro que o lado do agente não tem. A leitura da Fase 5 (`avaliar_fase5.py --manual`) confere a planilha contra o registro. -->
`Documentacao/memorial/5-metodo-e-ferramental/planilha-linha-de-base-manual.csv`, separada por ponto e vírgula (o Excel em português abre em colunas), com uma linha por integrante e cenário, na ordem sorteada. O `ordem --gravar` nunca escreve por cima de uma planilha com anotações: grava a planilha em branco ao lado, em `planilha-linha-de-base-manual.nova.csv`.

Na versão 2 o facilitador escreve só a coluna `observacoes`. As outras nove saem do registro, pelo comando `python linha_de_base_manual.py planilha`, rodado no fim da sessão, depois que o integrante sai (a planilha mostra o `corrigido` dos cenários de contrato). O comando preenche só célula vazia, e só de cenário que já acabou. Ele nunca troca uma célula preenchida: quando o registro e a planilha discordam, mostra a diferença na tela, deixa a planilha como está e sai com código 1. Com `--sem-gravar`, só mostra o que seria preenchido.

| Coluna | O que vai nela |
|---|---|
| `integrante`, `ordem`, `cenario`, `tipo` | preenchidas pelo sorteio; `cenario` diz o modo de falha, por isso a planilha fica com o facilitador |
| `inicio` | a hora do evento `inicio` do `armar` (hh:mm:ss; os milésimos e a data ficam no registro, e por isso um cenário não pode atravessar a meia-noite) |
| `fim` | contrato: a hora do Enter do `entregar`; localizador: a hora do `conferir` que disse "CORRIGIDO"; vazia se estourou o limite |
| `segundos` | do início ao fim, menos `descontar_s`, calculado com os milésimos do registro e escrito com vírgula decimal (o Excel em português lê o ponto como separador de milhar); por isso pode diferir em menos de 1 s da conta feita com as horas da planilha |
| `descontar_s` | a soma dos segundos de restauração do banco das tentativas, até a que corrigiu; 0 no contrato |
| `causa`, `campo` | contrato: o que o integrante entregou (`nenhum` quando não há campo); vazias se a entrega veio depois do limite |
| `seletor` | localizador: o seletor que corrigiu (ou o último tentado) |
| `tentativas` | localizador: quantos `conferir` com seletor foram rodados, até o que corrigiu |
| `corrigido` | `sim` ou `não`, pela seção 7 |
| `observacoes` | a única coluna que o facilitador escreve: o que fugiu do protocolo (dúvida, interrupção, erro do facilitador, fala fora do texto fixo) |

**Linha anotada à mão.** No cenário em que a ferramenta falhou, o facilitador preenche a linha com os horários do cronômetro de reserva e escreve `anotada à mão` nas observações (`linha_de_base_manual.MARCA_A_MAO`). O comando `planilha` não mexe nos valores dessa linha: se as observações estiverem vazias, ele põe a marca; se tiverem outro texto sem a marca, pede que o facilitador a escreva. A leitura da Fase 5 aceita essa linha sem o registro e conta à parte quantas foram.

**Linha anulada.** Só uma falha do protocolo anotada na hora anula uma medida: máquina que travou, falha armada errado, interrupção de fora (plano da Fase 5, regra L14). O facilitador começa as observações da linha com `ANULADA` e escreve o motivo (`avaliar_fase5.MARCA_ANULADA`). A leitura conta as anuladas à parte e não as substitui. Na sessão pela página (seção 11) quem escreve o aviso na hora é o integrante, e a marca é posta pelo comando `planilha`, a partir do que o facilitador decidiu na importação (decisão 137).

## 9. Como a comparação é feita

<!-- ! Alteração de IA - Revisar: (16/11/2026, versão 2) aviso no começo da seção: as regras de leitura da Fase 5 são as do plano aprovado, e os itens abaixo ficam como a versão 1 os escreveu.
     ! Motivo: a versão 1 dizia que a comparação seria por tipo de cenário, lida por `avaliar_fase4.py --cenarios`; o plano da Fase 5 (seção 5, regras L1 a L15; decisão 132) fixou o cenário como unidade e a leitura em `avaliar_fase5.py`. Sem o aviso, o protocolo e o plano diriam coisas diferentes sobre a mesma conta. -->
**Na Fase 5 valem as regras de leitura da seção 5 do [plano aprovado](../../../claude-memoria/plano-aprovado-fase-5.md)** (L1 a L15; decisão 132): o cenário é a unidade da comparação, e a planilha e o registro são lidos por `avaliar_fase5.py --manual` e `--comparar`. Os itens abaixo são os da versão 1 e ficam como registro do que se previa em 04/11/2026.

- **Agente:** as cinco repetições dos dez cenários na Fase 5 (`rodar_fase4.ps1 -Modo cenarios -Repeticoes 5`), lidas por `avaliar_fase4.py --cenarios`: MTTR médio com intervalo de 95% por reamostragem (2000 reamostras, semente fixa) e Task Success com intervalo de Wilson de 95%, no geral, por tipo de cenário e por cenário.
- **Integrantes:** as 30 linhas da planilha, com as mesmas contas (`avaliar_fase4.bootstrap_media` e `avaliar.wilson`), no geral, por tipo e por cenário. A leitura da planilha por script entra na Fase 5, para nenhum número ser digitado à mão.
- **Comparação:** o tempo dos integrantes contra o MTTR do agente, por tipo de cenário, e o Task Success dos dois lado a lado.
- **Limitações a declarar no texto:** a falha é armada, não ocorrida; o integrante parte da ficha da detecção do agente, então a detecção em si não é medida no humano; a ordem sorteada espalha o aprendizado entre os cenários mas não o elimina; três integrantes dão três tempos por cenário.

## 10. O roteiro do dia, para o facilitador

<!-- ! Alteração de IA - Revisar: (16/11/2026, versão 2) o roteiro ganha a abertura com o texto fixo e as três perguntas de perfil (comando `perfil`), o treino (comando `treino`), o `entregar` nos cenários de contrato, o cronômetro de reserva, o fecho e o comando `planilha`; o texto fixo do facilitador entra no fim, como bloco que sai do comando `falas`.
     ! Motivo: decisão 131 (ficha 73); plano da Fase 5, seção 4.3. Na versão 1 o facilitador anotava à mão o início, o fim e as tentativas e dizia o que achasse preciso; agora a ferramenta grava, e o que ele diz durante um cenário são as falas fixas, para não dar dica sem querer. O perfil explica o tempo de cada integrante sem guardar o nome, porque o repositório é público. -->
Uma sessão por integrante, com a abertura, o treino, os dez cenários e o fecho, nessa ordem (plano da Fase 5, seção 4.3).

1. Na máquina-alvo, janela 1, na raiz do repositório: `python run.py` (as cobaias no ar).
2. Janela 2, na venv do AgenteCore, na pasta `Programacao/AgenteCore/experimentos`, com `$env:RESULTADOS_DIR = "resultados_alvo"`: `python linha_de_base_manual.py ordem` confere a ordem da planilha. A janela 3, para o `entregar` e o `conferir`, é aberta do mesmo jeito.
3. **Abertura.** Entregar a folha da seção 5 e ler o texto fixo do fim desta seção. As três perguntas de perfil são gravadas com `python linha_de_base_manual.py perfil --integrante <integrante>`, em `resultados_alvo/fase5_manual/participantes.json`, sem o nome: o facilitador lê cada pergunta na tela e digita a resposta. A última pergunta do comando é uma anotação do facilitador (se o integrante escreveu ou conhece o código das cobaias) e não é feita ao integrante.
4. **Treino**, sem cronômetro: `python linha_de_base_manual.py treino contrato --integrante <integrante>` e depois `python linha_de_base_manual.py treino seletor --integrante <integrante>`. Só no treino o facilitador diz a resposta certa e explica a forma da resposta.
5. **Os dez cenários**, na ordem da planilha. Para cada linha, na janela 2: `python linha_de_base_manual.py armar --vez <integrante> <posição>`. O integrante lê no terminal a ficha, o roteiro e, no contrato, o contrato e as causas, e trabalha no navegador que abriu; só o facilitador digita. Quando a tela disser "início do cronômetro", o facilitador diz "O tempo está correndo." e dispara o cronômetro de reserva.
6. **Contrato:** na janela 3, deixar `python linha_de_base_manual.py entregar --vez <integrante> <posição>` esperando. No instante em que o integrante avisar que entregou, Enter; depois, copiar do bloco de notas a causa e o campo. **Localizador:** na janela 3, `python linha_de_base_manual.py conferir --vez <integrante> <posição> --seletor "<seletor copiado do bloco de notas>"`; com "CORRIGIDO" o cenário acabou, e com "não corrigido" o tempo segue e o integrante tenta de novo. No PowerShell, um seletor com aspas duplas vai entre aspas simples: `--seletor 'input[placeholder="Buscar produtos"]'`.
7. Enter na janela 2: o navegador fecha, a falha é desligada e o fim da janela é gravado. Anotar na folha de papel a hora de fim do cronômetro de reserva. Pausa livre, e a próxima linha.
8. **Fecho.** As duas falas do fecho; `python linha_de_base_manual.py desarmar` e Ctrl+C na janela 1. Depois que o integrante sair: `python linha_de_base_manual.py planilha` preenche a planilha, e o facilitador escreve as observações.

O texto abaixo é o que o comando `falas` imprime (`linha_de_base_manual.texto_do_facilitador`), colado aqui por `protocolo --colar`.

<!-- tabela:tb_f5_texto_do_facilitador -->
**Texto fixo do facilitador.** Leia em voz alta, como está escrito. O que for dito além deste texto vai para a coluna `observacoes` da planilha.

**Abertura**, antes do treino:

1. "Esta sessão mede duas coisas em 10 cenários de teste com uma falha: quanto tempo leva para resolver cada um e se a resposta está certa. O que se mede é o trabalho feito à mão, não você: o seu nome não entra em nenhum arquivo."
2. "Em cada cenário você recebe a ficha da falha, que é a frase que o teste automático acusou, o roteiro do teste passo a passo e o navegador aberto onde o roteiro começa, com as ferramentas do desenvolvedor, na tecla F12. A sua folha diz tudo isto por escrito."
3. "Há dois tipos de cenário. No de contrato, a resposta é uma causa da lista de 23 da sua folha e o campo afetado, ou nenhum. No de localizador, a resposta é um seletor, CSS ou do Playwright, que ache o elemento do passo que quebrou. Escreva a resposta no bloco de notas ao lado e me avise."
4. "Você pode navegar, inspecionar a página, ver as chamadas na aba de rede, abrir a API pelo navegador e consultar a documentação de seletores. Não pode abrir o código das aplicações, o código do agente nem o repositório, usar assistente de IA, ver a minha planilha nem falar com os outros integrantes sobre os cenários."
5. "O tempo começa quando o navegador abre. No cenário de contrato ele para quando você entrega; a entrega é uma só, e eu não digo se está certa. No de localizador eu confiro o seletor: se o roteiro passar, o tempo para; se não passar, o tempo segue e você pode tentar de novo. O limite é de 10 minutos por cenário, e entre um cenário e outro a pausa é livre."
6. "Um aviso sobre a aplicação: a tela de login volta sozinha para a página inicial depois de 30 segundos. Isso não é a falha. Se acontecer, abra a tela de login de novo no mesmo navegador."
7. "Durante um cenário eu não respondo perguntas sobre ele e só digo as frases combinadas."
8. "Antes de começar, três perguntas."
   - "Quanto tempo de prática você tem com teste de software ou com programação para a web?"
   - "Você já usou as ferramentas do desenvolvedor do navegador (a tecla F12)?"
   - "Você já leu a lista dos 10 cenários ou as causas esperadas no painel, no README, no documento do TCC ou no repositório?"

As respostas são gravadas com o comando `perfil`, sem o nome. Quem responde que já leu a lista dos cenários não serve de integrante; se não houver substituto, participa e isso fica declarado na leitura.

**Treino**, sem cronômetro:

9. "Agora um treino, sem cronômetro, para você conhecer o material e a forma da resposta: um cenário de contrato e um exercício de seletor que não estão entre os que valem. Só no treino eu digo a resposta certa."

**Durante um cenário**, as únicas falas:

- "O tempo está correndo." Quando o navegador abre.
- "Faltam dois minutos." Quando a janela do `armar` avisar.
- "Pode entregar quando quiser." Se o integrante perguntar se já pode entregar.
- "A causa precisa ser uma das 23 da lista, escrita como está na folha." Quando o `entregar` recusar a causa.
- "Não passou. O tempo segue." Quando o `conferir` disser "não corrigido".
- "Passou. O tempo parou." Quando o `conferir` disser "CORRIGIDO".
- "Tempo esgotado." Quando a janela do `armar` avisar que os 10 minutos acabaram.

O cronômetro de reserva, no celular, é disparado na primeira fala e parado na entrega ou no seletor que passou; os dois horários vão para a folha de papel, com o número do integrante e a posição do cenário.

**Fecho**:

- "Acabou. Obrigado."
- "Por favor, não comente os cenários nem as respostas com os outros integrantes até as sessões deles acabarem."
<!-- /tabela:tb_f5_texto_do_facilitador -->

## 11. A sessão pela página publicada (versão 3)

<!-- ! Alteração de IA - Revisar: seção nova (16/11/2026, decisão 136): a sessão da linha de base manual feita por uma página publicada, uma por integrante: o que roda antes nesta máquina, o que a página leva, como a sessão corre, onde ela fica guardada, como vem para o registro e o que muda na medida.
     ! Motivo: o Eric decidiu que os integrantes fazem a sessão por um endereço, sem instalar nada, com tudo o que precisa rodar já rodado aqui e só o diagnóstico por conta deles. Uma página publicada não alcança as cobaias nem o navegador desta máquina, e abrir a máquina para a internet exporia um site inseguro de propósito num notebook corporativo; por isso a falha é armada e o teste é executado antes, e a página leva o registro. Sem esta seção o protocolo descreveria só a forma presencial, que virou reserva. -->
Desde a decisão 136, as três sessões são feitas por uma página publicada (um artefato do claude.ai por integrante), sem ninguém instalar nada e sem facilitador ao lado. As seções 4 a 8 e 10 descrevem a forma presencial da versão 2, que fica como reserva, com os comandos dela testados. Para as sessões vale esta seção; onde ela não diz nada, valem as seções 6 e 7: onde o cronômetro começa e termina, o limite de 10 minutos e o que conta como corrigido.

**O que roda antes, nesta máquina.** Com as cobaias no ar e sem modelo, `python linha_de_base_manual.py material` roda cada um dos dez cenários e o treino, com a falha armada pelas mesmas funções das sessões presenciais (`executar_fase4.ligar_modo` no contrato; os cookies da variante PHP no localizador), e guarda em `resultados_alvo/fase5_material/material.json` o que o teste e o navegador registraram: nos cenários de contrato, a chamada à API (status, tempo e corpo) e a foto da tela; nos de localizador, a foto da tela, o HTML da página no passo que quebrou e a posição do elemento do passo. A ficha da falha continua sendo a da corrida 21. O comando não regrava o material sem `--regravar`, e um teste confere que o navegador e o banco são os da corrida 21d. Depois, `python linha_de_base_manual.py paginas --gravar` monta as três páginas, `Documentacao/dashboard/sessao-integrante-1.html`, `-2` e `-3`, e `paginas --check` acusa se elas ficarem diferentes do código e do material.

**O que a página leva.** O tutorial ([tutorial-do-integrante.md](tutorial-do-integrante.md)), com o botão Começar no fim, e os dez cenários pela posição na ordem sorteada daquele integrante. Ela não leva o nome do cenário, o modo de falha nem a resposta esperada: só o treino traz a resposta, porque a página a diz no fim dele. Cada página é só do seu integrante.

**Como a sessão corre.** Depois do Começar, a página faz as três perguntas de perfil, abre o treino sem cronômetro (o cenário de contrato do treino e o exercício de seletor) e mostra os dez cenários, um por vez. O tempo de um cenário começa no clique em "Abrir o cenário". No contrato a pessoa escolhe uma causa na lista das 23 e escreve o campo, a entrega é uma só, e a página não diz se está certa. No localizador a resposta é um seletor CSS: a caixa Testar seletor diz quantos elementos ele acha, sem contar tentativa, e o botão Entregar confere contra a fotografia do HTML, passando quando o primeiro elemento que o seletor acha é o elemento do passo. A página avisa quando faltam dois minutos, fecha o cenário no limite e tem o botão Encerrar sem resposta. Os avisos são as mesmas frases das falas fixas. Com o cenário fechado e o tempo parado, a página pergunta se alguma coisa de fora atrapalhou (parágrafo da regra L14, abaixo).

**Onde a sessão fica guardada.** Em três lugares: no navegador da pessoa, para ela voltar de onde parou; no banco do artefato (documento `sessoes/integrante-N`), quando a pessoa pode gravar nele; e no código da sessão, que a página mostra no fim para a pessoa copiar e mandar ao facilitador. Pelo que a plataforma documenta, o banco só aceita gravação do dono da página e de quem foi convidado por e-mail como editor, com a página sem link público; quem só tem o link não grava. Por isso a página nunca depende do banco para seguir, e o código da sessão existe para nenhuma sessão se perder.

**Como a sessão vem para cá.** O Claude lê o documento do banco do artefato, ou o facilitador salva num arquivo o código que a pessoa mandou, e roda, com as cobaias no ar, `python linha_de_base_manual.py importar --arquivo <arquivo> --conhece-o-codigo sim|nao`. Se o integrante deixou aviso de que algo de fora atrapalhou, o comando pede antes a decisão do `--anular` (parágrafo da regra L14, abaixo). O comando confere a sessão inteira antes de gravar, acha o cenário de cada posição pelo sorteio, refaz o corrigido do contrato pela regra do agente e roda o roteiro de verdade com o seletor que passou na página: é esse resultado que vale. O registro sai em `resultados_alvo/fase5_manual/sessao.jsonl`, no formato dos comandos presenciais, e o perfil em `participantes.json`, com a anotação do facilitador sobre o código das cobaias. Depois, `python linha_de_base_manual.py planilha` preenche a planilha, como na seção 8. Cada integrante entra uma vez só.

<!-- ! Alteração de IA - Revisar: parágrafo novo (17/11/2026, ficha 77, decisão 137): como o integrante avisa, na sessão pela página, de uma falha do protocolo, e como o facilitador decide a anulação da linha na importação.
     ! Motivo: a regra L14 do plano só anula a medida de um cenário por falha do protocolo anotada na hora, e a seção 8 só dizia quem anota na forma presencial (o facilitador, com `ANULADA` nas observações). Na sessão pela página não há ninguém ao lado: sem este parágrafo, o cenário em que o computador travou entraria na conta como demora da pessoa, ou seria tirado depois de o tempo ter sido visto. A decisão fica na importação, que não mostra tempo nenhum, para valer o "antes de qualquer número ser lido" da regra. -->
**Quando algo de fora atrapalha um cenário (regra L14, decisão 137).** Na forma presencial quem anota a falha do protocolo é o facilitador (seção 8). Na sessão pela página quem anota é a própria pessoa: no fim de cada cenário, com o tempo já parado e antes de abrir o próximo, a página pergunta "Alguma coisa de fora atrapalhou este cenário?", com uma caixa de texto que pode ficar vazia. Conta o que não é do cenário: o computador ou o navegador travou, a página não carregou, alguém interrompeu. Não conta cenário difícil, dúvida sobre a resposta nem tempo curto. O tutorial diz isso antes da sessão. O aviso é gravado com a hora no registro da sessão. Na importação, o comando `importar` mostra cada aviso (a posição do cenário e o texto, sem tempo nenhum) e não grava nada enquanto o facilitador não disser, só pelo motivo escrito, quais avisos são falha do protocolo: `--anular` com as posições separadas por vírgula anula as linhas dessas posições, e `--anular nenhum` mantém todas. A decisão vai para o registro com a hora em que foi tomada, e o comando `planilha` escreve o aviso nas observações da linha: `ANULADA: aviso do integrante: ...` quando a linha foi anulada, e `aviso do integrante (linha mantida): ...` quando não foi. Posição sem aviso escrito na hora não pode ser anulada. O tempo e a resposta do cenário anulado continuam no registro; a leitura conta a linha à parte e não a substitui.

**Como compartilhar.** Cada página é compartilhada só com o seu integrante, e os três recebem o endereço no mesmo dia. Para a página guardar a sessão sozinha, o integrante é convidado por e-mail como editor e entra logado; sem isso a sessão segue igual, e ele manda o código no fim.

**O que muda na medida, a declarar na leitura.** A pessoa lê o registro do que aconteceu, em vez de investigar o site no ar com as ferramentas do navegador. Não há facilitador ao lado: não abrir o repositório, não usar assistente de IA e não conversar com os outros passam a ser um combinado, e a falha do protocolo é anotada pela própria pessoa, sem ninguém para conferir se a interrupção aconteceu. O navegador, o aparelho e o relógio são os de cada um. O seletor é só CSS, e a página o confere contra uma fotografia do HTML; o que vale é o roteiro de verdade, rodado na importação, e um seletor que passe na página e não passe nele deixa o cenário como não corrigido, sem nova tentativa. As sessões deixam de ser presenciais, como a decisão 130 previa.
