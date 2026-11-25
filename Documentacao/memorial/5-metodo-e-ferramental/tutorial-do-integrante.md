<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por `python linha_de_base_manual.py tutorial --gravar` a partir de `Programacao/AgenteCore/experimentos/tutorial_do_integrante.py` (`tutorial --check` regera e compara); não editar à mão.
     ! Motivo: é o tutorial que os três integrantes da linha de base manual da Fase 5 leem antes de começar a sessão (decisões 135 e 136). Os três têm de receber o mesmo texto, os números dele vêm das constantes do ajudante da sessão, e nenhum exemplo vem das cobaias; na página de cada sessão (`Documentacao/dashboard/sessao-integrante-N.html`) ele sai do mesmo conteúdo, com o botão no fim. -->

# Tutorial do integrante

O que você precisa saber antes de começar a sessão em que vai consertar testes à mão.

## 1. Antes de tudo: quatro combinados

Este tutorial é o único material de preparo, e é igual para os três integrantes. Leia com calma: o botão Começar fica no fim da página.

1. Até a sua sessão acabar, não abra o repositório do projeto, o painel do projeto, o README nem o documento do TCC. As respostas dos cenários estão lá, e quem já leu não pode participar.
2. Não converse sobre a sessão com os outros integrantes: nem antes da sua, nem depois, enquanto houver sessão por fazer.
3. Não use assistente de IA. O que se quer saber é quanto tempo uma pessoa leva.
4. Faça num computador, com teclado, e de uma vez só: reserve 2h10 sem interrupção.

> **Se você já leu.** Se já abriu algum desses materiais e viu a lista dos cenários ou as respostas, avise o facilitador antes de começar. Não é problema seu: ele só precisa saber.

## 2. O que é a sessão

O projeto construiu um agente que conserta testes automatizados quando eles quebram. Para saber se ele vale a pena, o projeto compara o tempo do agente com o tempo de uma pessoa fazendo o mesmo conserto à mão. Você é essa pessoa: a linha de base manual.

São 10 cenários. Em cada um, um teste automatizado de um site de teste parou ou acusou um problema, porque uma falha foi armada de propósito. Tudo isso já rodou na máquina do projeto: você recebe o registro do que aconteceu e diz o que quebrou. Mede-se quanto tempo cada cenário leva e se a resposta está certa.

O que se mede é o trabalho feito à mão, não você. O seu nome não entra em nenhum arquivo: nos registros você é o integrante 1, 2 ou 3.

| Parte da sessão | Quanto dura | O que acontece |
|---|---|---|
| Antes de começar | 10 min | este tutorial e três perguntas sobre a sua experiência |
| Treino, sem cronômetro | 15 min | um cenário de cada tipo, fora dos que valem; só aqui a página diz a resposta certa |
| Os 10 cenários | até 10 min cada | com pausa livre entre um e outro |
| Fim | 5 min | a página diz se guardou a sua sessão |

Reserve 2h10: é quanto a sessão leva se todo cenário for até o limite.

## 3. Como é um cenário

Cada cenário é uma tela desta página. Nela você recebe:

- a **ficha da falha**: a frase que o teste automático acusou;
- o **roteiro do teste**, passo a passo, com o valor de cada preenchimento;
- o **material registrado** quando o teste rodou: no cenário de contrato, a chamada à API com a resposta que chegou, o contrato esperado e a foto da tela; no de localizador, a foto da tela e o HTML da página no passo que quebrou;
- nos cenários de contrato, a **lista das 23 causas**.

Há dois tipos de cenário, e a resposta de cada um é diferente.

**Cenário de contrato**

- O site pede dados a uma API, e a resposta da API saiu do combinado.
- Você responde com **uma causa** da lista de 23 e **o campo** afetado, ou `nenhum`.
- A entrega é uma só. O tempo para na entrega, certa ou errada, e a página não diz se você acertou.

**Cenário de localizador**

- O teste procura um elemento da página por um seletor, e o seletor não acha mais o elemento. No roteiro, o passo que quebrou vem marcado.
- Você responde com **um seletor CSS novo** que ache o elemento.
- A página confere na hora. Se passar, o tempo para. Se não passar, o tempo segue e você tenta de novo.

O tempo de um cenário só começa quando você clica em **Abrir o cenário**. O limite é de 10 minutos: passou disso, a página fecha o cenário, e ele conta como não resolvido. Entre um cenário e outro a pausa é livre, e o tempo não corre.

> **Se algo de fora atrapalhar.** No fim de cada cenário, com o tempo já parado, a página pergunta: **Alguma coisa de fora atrapalhou este cenário?** Escreva ali, na hora, só o que não é do cenário: o computador ou o navegador travou, a página não carregou, alguém interrompeu você. Não entra: cenário difícil, dúvida sobre a resposta ou tempo curto. Se nada atrapalhou, deixe em branco. O facilitador lê o aviso antes de ver os tempos e decide se aquele cenário fica fora da conta.

## 4. O que a página avisa

Não há ninguém ao lado para tirar dúvida durante um cenário. A página só mostra estes avisos:

- **Faltam dois minutos.** quando faltam 2 minutos para o limite do cenário.
- **Tempo esgotado.** quando o limite acabou. O cenário fecha sozinho.
- **Não passou. O tempo segue.** no localizador, quando o seu seletor não achou o elemento certo.
- **Passou. O tempo parou.** no localizador, quando o seu seletor achou o elemento certo.

No cenário de contrato a página só confirma que recebeu a resposta. Dúvida sobre as regras? Pergunte ao facilitador antes de clicar em Começar.

## 5. O que pode e o que não pode

**Pode:** ler o material do cenário quantas vezes quiser, usar a caixa Testar seletor e consultar a documentação de seletores CSS.

**Não pode:** abrir o repositório, o painel, o README ou o documento do TCC do projeto, usar assistente de IA nem falar com outro integrante sobre os cenários.

A documentação que você pode consultar: [seletores CSS, na MDN](https://developer.mozilla.org/pt-BR/docs/Web/CSS/CSS_selectors).

## 6. Como ler o material de um cenário

- **A chamada à API** o que o site pediu e o que a API respondeu: o código de status, quanto tempo levou e o corpo da resposta, como chegou.
- **O contrato** a lista dos campos que a resposta tem de trazer, com o tipo de cada um.
- **A foto da tela** como a página do site estava quando o teste parou ou terminou.
- **O HTML da página** no cenário de localizador, o HTML da página no passo que quebrou, uma linha por elemento, com o `id`, as classes e os outros atributos de cada um. Use a busca do navegador (Ctrl+F) para achar um texto.
- **A caixa Testar seletor** diz quantos elementos do HTML o seu seletor acha e mostra o primeiro. Testar não conta como tentativa: só o botão Entregar conta.

## 7. Cenário de contrato, passo a passo

Um contrato é a lista dos campos que a resposta de uma API tem de trazer: o nome de cada campo e o tipo dele. A página mostra o contrato e a resposta que chegou. O trabalho é achar onde as duas diferem.

1. Leia a ficha da falha. Ela diz o que o teste automático viu de errado, e é a melhor pista de onde olhar.
2. Olhe o código de status e o tempo da chamada. 200 quer dizer que a API respondeu sem erro; os que começam com 4 ou 5 são erro.
3. Olhe o corpo da resposta e compare com o contrato, campo a campo.
4. Procure na lista das 23 causas a linha que descreve o que você achou.
5. Escolha a causa e escreva o campo onde o problema está. Se o problema é da resposta inteira, e não de um campo, o campo é `nenhum`.

Na comparação, estas seis perguntas cobrem tudo o que pode estar errado:

- O corpo da resposta é sequer legível?
- A forma da resposta bate com a esperada?
- Os tipos e os domínios fazem sentido?
- O mapeamento entre as camadas está correto?
- O comportamento no tempo e no estado está correto?
- O que o usuário de fato vê está correto?

> **Um exemplo, de outro sistema.** Uma agenda de consultas, que não tem nada a ver com a sessão. Serve só para mostrar o jeito de comparar e de responder.

O contrato de cada consulta, como ele aparece na página:

```text
id: inteiro | paciente: texto | data: texto, no formato AAAA-MM-DD | confirmada: booleano
```

A resposta que chegou:

```text
[{"id": 7, "paciente": "Ana Lima", "data": "19/11/2026", "confirmada": true}]
```

O status é 200 e o corpo é JSON inteiro. Os quatro campos vieram, com os nomes do contrato. O que difere é o campo `data`: o contrato pede ano, mês e dia, e a resposta trouxe dia, mês e ano. Na lista, a linha que descreve isso é a de `formato_de_data_divergente`: a data vem escrita num formato diferente do que o contrato pede.

O que você responde:

```text
causa: formato_de_data_divergente
campo: data
```

## 8. Cenário de localizador, passo a passo

Um teste automatizado acha cada elemento da página por um seletor: um texto curto que descreve o elemento. Quando a página muda, o seletor antigo pode não achar mais nada, e o teste para. No roteiro, o passo que quebrou vem marcado, com o seletor que deixou de funcionar.

1. Leia o roteiro até o passo marcado. Ele diz o que o teste ia fazer ali: clicar, preencher ou esperar um elemento.
2. Olhe a foto da tela e ache o elemento que o passo usa.
3. Ache esse elemento no HTML da página e veja o que o identifica.
4. Escreva um seletor CSS novo.
5. Use a caixa Testar seletor. O melhor é o seletor achar um elemento só: o que você quer.
6. Clique em Entregar.

Há vários jeitos de escrever um seletor CSS. Os exemplos são de um formulário de cadastro inventado.

| O que identifica o elemento | Seletor | Como se lê |
|---|---|---|
| o `id` | `#salvar` | o elemento com o id salvar |
| uma classe | `button.confirmar` | o botão com a classe confirmar |
| um atributo | `input[name=email]` | o campo com o atributo name igual a email |
| um pedaço de um atributo | `a[href*="ajuda"]` | o link cujo endereço contém ajuda |
| o lugar na página | `#cadastro > button` | o botão que é filho direto do elemento com o id cadastro |
| a posição entre iguais | `table tr:nth-child(2) td:first-child` | a primeira célula da segunda linha da tabela |

O que quer dizer passar: o primeiro elemento que o seu seletor acha no HTML tem de ser o elemento do passo que quebrou. Depois da sessão, o projeto roda o teste de verdade com o seletor que passou, e é esse resultado que vale.

## 9. As 23 causas

É a mesma lista que aparece nos cenários de contrato. Lá você escolhe uma delas.

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

## 10. Perguntas comuns

- **Vou saber se acertei?** No cenário de localizador, sim, na hora. No de contrato, não: saber se acertou um cenário mudaria o que você responde nos seguintes.
- **E se eu não souber a resposta?** No contrato, a entrega é uma só e o tempo para nela, certa ou errada; sem entrega até o limite, o cenário conta como não resolvido. No localizador, você pode tentar quantas vezes couberem no limite. Nos dois há o botão Encerrar sem resposta.
- **Posso parar no meio?** Entre um cenário e outro, sim: a página guarda onde você parou. Com um cenário aberto, não: o tempo continua correndo mesmo com a página fechada.
- **E se o computador travar ou alguém me interromper?** Siga como der: o tempo do cenário não para. No fim dele, escreva o que houve na caixa do aviso, antes de abrir o próximo. Se a página fechou, abra o mesmo endereço no mesmo navegador: ela volta de onde parou.
- **O que fica gravado sobre mim?** As respostas às três perguntas do começo, o tempo e a resposta de cada cenário, o que você escrever na caixa do aviso e o tipo de navegador, pelo número do integrante. O nome, não.
- **Posso contar para os outros como foi?** Só depois que as três sessões acabarem.

## 11. Palavras que aparecem na sessão

- **API** o serviço que entrega os dados ao site. O site chama a API e mostra na tela o que ela responde.
- **JSON** o formato de texto em que a API responde, com chaves, colchetes e pares de nome e valor.
- **Contrato** o combinado sobre a resposta da API: os campos que vêm e o tipo de cada um.
- **Campo** cada par de nome e valor da resposta, como `data` no exemplo.
- **Código de status** o número com que a API diz como a chamada terminou: 200 é sem erro, 4xx e 5xx são erro.
- **Seletor** o texto que diz ao teste qual elemento da página usar.
- **Roteiro** a lista dos passos que o teste automatizado executa, na ordem.
- **Ficha da falha** a frase em que o teste automático diz o que viu de errado.

## 12. O botão Começar

Tudo o que precisava rodar já rodou antes, na máquina do projeto: em cada cenário a falha foi armada, o teste automatizado foi executado, e o que ele e o navegador registraram está guardado nesta página. Você não instala nada e não precisa de nenhum outro programa aberto.

Quando você clica em Começar, a página faz, nesta ordem:

1. Confere se consegue guardar a sua sessão. Se não conseguir, ela avisa, e no fim mostra um código da sessão para você copiar e mandar ao facilitador.
2. Faz as três perguntas sobre a sua experiência.
3. Abre o treino, sem cronômetro: um cenário de contrato e um exercício de seletor, com a resposta certa dita no fim de cada um.
4. Mostra os 10 cenários, um por vez, na ordem sorteada para você. Cada um espera o seu clique em **Abrir o cenário**, e é nesse clique que o tempo dele começa.
5. No fim, diz se a sessão ficou guardada e mostra o código da sessão.

A página guarda cada resposta na hora. Se ela fechar ou a internet cair entre um cenário e outro, abra o mesmo endereço de novo, no mesmo navegador: ela volta de onde você parou.

> **Antes de clicar.** Depois do Começar não há pausa dentro de um cenário. Confira que você tem o tempo reservado e tire com o facilitador as dúvidas sobre as regras.

(Na página da sessão, o botão **Começar** fica aqui.)
