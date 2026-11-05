<!-- ! Alteração de IA - Revisar: documento novo (04/11/2026, Fase 4, pacote P6) com o protocolo da sessão cronometrada da linha de base manual da Fase 5: os dez cenários da ficha 36, como cada um é armado, o que o integrante recebe e pode usar, quando o cronômetro começa e termina, o que conta como corrigido, a planilha, o roteiro do dia e como a comparação com o agente é feita.
     ! Motivo: o plano aprovado da Fase 4 (seção 3.9 e pacote P6) pede o protocolo escrito para a sessão com os integrantes ser marcada com antecedência (ficha 36, decisão 79); sem ele, cada integrante resolveria os cenários de um jeito, com a falha ligada à mão, e o tempo dele não seria comparável ao MTTR do agente medido no ensaio (corrida 21). -->

# Protocolo da linha de base manual (Fase 5)

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). Versão 1, de 04/11/2026, escrita no pacote P6 da Fase 4 ([plano aprovado](../../../claude-memoria/plano-aprovado-fase-4.md), seções 3.9 e 5) a partir das fichas 35 e 36 ([pendências](../pendencias.md), decisão 79) e do projeto ABNT, seção 3.4. O catálogo dos cenários e as regras de cronômetro e de Task Success vivem no código (`Programacao/AgenteCore/experimentos/cenarios_fase4.py`); o ajudante da sessão é `Programacao/AgenteCore/experimentos/linha_de_base_manual.py`. Este documento diz como a sessão roda; nenhum número de resultado está aqui.

**As seções 2 e 3 dizem a resposta de cada cenário: só o facilitador as lê antes da sessão.** O integrante recebe a seção 5 e nada mais.

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

1. **Corrida 21 feita.** A ficha da falha de cada cenário é o que a detecção do agente acusou no ensaio: o campo `motivo_deteccao` de `resultados_alvo/fase4_ensaio/cenarios.jsonl`, que o `armar` lê, e a coluna "O que a detecção acusou" da tabela `tb_f4_cenarios_por_cenario`. Sem a corrida 21, o `armar` avisa que não há ficha.
2. **Ordem e planilha.** `python linha_de_base_manual.py ordem --gravar` sorteia a ordem dos dez cenários de cada integrante com a semente 20261104 (a do integrante n usa a semente mais n), para o que um integrante aprende num cenário se espalhar entre os cenários, e grava a planilha da seção 8. A mesma semente dá sempre a mesma ordem.
3. **Ensaio do facilitador.** Rodar os dez cenários uma vez com `--cenario <nome>`, sem cronômetro, para conferir que cada um abre e que o `conferir` diz "não corrigido" sem seletor.
4. **Facilitador e integrantes.** O facilitador conduz e não resolve; quem conhece o catálogo de modos de falha (quem escreveu as seções 2 e 3) fica como facilitador, não como integrante. Os três integrantes não conversam sobre os cenários entre as sessões.
5. **Máquina.** A máquina-alvo da corrida 21, com o mesmo Chromium da venv do AgenteCore: o `armar` mostra a versão do navegador, que tem de ser a do cabeçalho da corrida 21 (a Fase 5 fixa o navegador, projeto ABNT §3.4). Um integrante por vez.
<!-- ! Alteração de IA - Revisar: (04/11/2026) item novo: a tela de login do front legado volta sozinha para a página inicial depois de 30 s, e o facilitador avisa os integrantes antes de começar.
     ! Motivo: foi o que deixou um cenário sem cura na corrida 21 (meta refresh em `admin/login.php`, roadmap §2.13). Os três cenários de localizador que passam pelo login pegariam o integrante de surpresa, e o cronômetro mediria o susto, não a correção do teste. -->
6. **Aviso aos integrantes.** A tela de login do front legado volta sozinha para a página inicial depois de 30 s (`<meta http-equiv="refresh">` em `admin/login.php`). É comportamento da aplicação, não parte da falha. O facilitador avisa antes de começar: quando isso acontecer, é só reabrir `admin/login.php` no mesmo navegador, e a quebra continua armada, porque os cookies valem para o navegador inteiro.

## 5. O que o integrante recebe e o que pode usar

**Recebe**, no começo de cada cenário:

- a ficha da falha: a frase que a detecção do agente acusou neste cenário na corrida 21 (a conferência ou o passo do roteiro que falhou, ou o que a chamada à API mostrou fora do contrato);
- o roteiro do teste, passo a passo, com o valor de cada preenchimento e, nos cenários de localizador, o passo que quebrou marcado;
- nos cenários de contrato, o contrato esperado de cada produto em `GET /api/produtos` (o mesmo bloco que o agente recebe) e a lista das 23 causas (`taxonomia.CAUSAS_RAIZ`);
- o navegador aberto no ponto em que o roteiro começa, com as ferramentas do desenvolvedor (F12): elementos, rede, console.

**Pode** navegar, inspecionar a página, ver as chamadas à API na aba de rede, abrir a API pelo navegador e consultar a documentação de seletores CSS e do Playwright.

**Não pode** abrir o código das cobaias, do agente ou o repositório (o código das cobaias mostra os modos de falha), usar assistente de IA, ver a planilha do facilitador nem falar com outro integrante durante a sessão.

**Entrega**, no contrato, uma causa da lista e o campo afetado (ou "nenhum"), por escrito, ao facilitador; no localizador, um seletor (CSS ou do Playwright) para o elemento do passo que quebrou, que o facilitador confere com o `conferir`. No localizador o integrante pode tentar de novo até o limite de tempo.

## 6. O cronômetro

- **Começa** quando o navegador do `armar` está aberto e o integrante tem o material da seção 5: é o equivalente da detecção, onde o MTTR do agente começa. O `armar` mostra a hora.
- **Termina, no contrato,** quando o integrante entrega a causa e o campo, com a causa dentro das 23. Acertar ou errar não muda a hora do fim, como no agente: o MTTR dele para no diagnóstico conferido em código, certo ou errado, e o Task Success é que diz se acertou (ficha 35).
- **Termina, no localizador,** quando o `conferir` diz "CORRIGIDO"; desconta-se o tempo de restauração do banco que ele mostra. Cada "não corrigido" conta uma tentativa, e o cronômetro segue.
- **Limite:** 10 minutos por cenário. Estourado o limite, o cenário fica "não corrigido", sem tempo de fim; ele conta no Task Success e fica fora da média do tempo, como as execuções do agente em que o cronômetro não chegou ao fim. O limite pode mudar antes de a sessão ser marcada; depois, vale para os três integrantes.

## 7. O que conta como corrigido (Task Success)

- **Contrato:** a causa entregue é a causa esperada do cenário (seção 2) e o campo é o esperado: `preco` nos quatro cenários com campo e nenhum nos dois sem campo. É a regra de `cenarios_fase4.task_success_contrato`, a mesma do agente.
- **Localizador:** o `conferir` disse "CORRIGIDO" dentro do limite, isto é, o roteiro do agente, com o seletor do integrante no lugar do quebrado, chegou ao fim sem erro.

## 8. A planilha

`Documentacao/memorial/5-metodo-e-ferramental/planilha-linha-de-base-manual.csv`, separada por ponto e vírgula (o Excel em português abre em colunas), com uma linha por integrante e cenário, na ordem sorteada. O `ordem --gravar` nunca escreve por cima de uma planilha com anotações: grava a planilha em branco ao lado, em `planilha-linha-de-base-manual.nova.csv`.

| Coluna | O que vai nela |
|---|---|
| `integrante`, `ordem`, `cenario`, `tipo` | preenchidas pelo sorteio; `cenario` diz o modo de falha, por isso a planilha fica com o facilitador |
| `inicio` | a hora que o `armar` mostrou (hh:mm:ss) |
| `fim` | contrato: a hora da entrega; localizador: a hora do `conferir` que disse "CORRIGIDO"; vazia se estourou o limite |
| `segundos` | do início ao fim, menos `descontar_s` |
| `descontar_s` | os segundos de restauração do banco que o `conferir` mostrou (soma, se houve mais de uma tentativa); 0 no contrato |
| `causa`, `campo` | contrato: o que o integrante entregou |
| `seletor` | localizador: o seletor que corrigiu (ou o último tentado) |
| `tentativas` | localizador: quantos `conferir` com seletor foram rodados |
| `corrigido` | `sim` ou `não`, pela seção 7 (no contrato, preenchido depois da sessão) |
| `observacoes` | o que fugiu do protocolo (dúvida, interrupção, erro do facilitador) |

## 9. Como a comparação é feita

- **Agente:** as cinco repetições dos dez cenários na Fase 5 (`rodar_fase4.ps1 -Modo cenarios -Repeticoes 5`), lidas por `avaliar_fase4.py --cenarios`: MTTR médio com intervalo de 95% por reamostragem (2000 reamostras, semente fixa) e Task Success com intervalo de Wilson de 95%, no geral, por tipo de cenário e por cenário.
- **Integrantes:** as 30 linhas da planilha, com as mesmas contas (`avaliar_fase4.bootstrap_media` e `avaliar.wilson`), no geral, por tipo e por cenário. A leitura da planilha por script entra na Fase 5, para nenhum número ser digitado à mão.
- **Comparação:** o tempo dos integrantes contra o MTTR do agente, por tipo de cenário, e o Task Success dos dois lado a lado.
- **Limitações a declarar no texto:** a falha é armada, não ocorrida; o integrante parte da ficha da detecção do agente, então a detecção em si não é medida no humano; a ordem sorteada espalha o aprendizado entre os cenários mas não o elimina; três integrantes dão três tempos por cenário.

## 10. O roteiro do dia, para o facilitador

1. Na máquina-alvo, janela 1, na raiz do repositório: `python run.py` (as cobaias no ar).
2. Janela 2, na venv do AgenteCore, na pasta `Programacao/AgenteCore/experimentos`, com `$env:RESULTADOS_DIR = "resultados_alvo"`: `python linha_de_base_manual.py ordem` confere a ordem da planilha.
3. Para cada linha do integrante, na ordem: `python linha_de_base_manual.py armar --vez <integrante> <posição>`. O integrante lê no terminal a ficha, o roteiro e, no contrato, o contrato e as causas, e trabalha no navegador que abriu; só o facilitador digita. Anotar o `inicio`.
4. Contrato: anotar a causa, o campo e a hora da entrega. Localizador: numa janela 3, `python linha_de_base_manual.py conferir --vez <integrante> <posição> --seletor "<seletor ditado>"`; com "CORRIGIDO", anotar o `fim`, o `descontar_s`, o `seletor` e as `tentativas`; com "não corrigido", somar uma tentativa e seguir. No PowerShell, um seletor com aspas duplas vai entre aspas simples: `--seletor 'input[placeholder="Buscar produtos"]'`.
5. Enter na janela 2: o navegador fecha e a falha é desligada. Próxima linha.
6. No fim, `python linha_de_base_manual.py desarmar` e Ctrl+C na janela 1.
