<!-- ! Alteração de IA - Revisar: relatório novo (01/10/2026) da Fase 3-B: pontes de versão, casos inéditos, troca cruzada, o confronto com a literatura levantada, o que muda para a Fase 4 e a lista de fechamento das Fases 3 e 3-B. Segunda versão no mesmo dia, depois de uma revisão independente do texto: a variação entre corridas passou a ser contada com a mesma entrada (sem o caso de texto corrigido), a conclusão da troca cruzada ficou no que o desenho sustenta, e as atribuições da literatura foram acertadas.
     ! Motivo: o Eric pediu, com a troca cruzada rodada, a análise de todos os dados das duas últimas corridas batida com a pesquisa e a documentação, e a verificação de que os tópicos das Fases 3 e 3-B podem ser dados por concluídos antes do planejamento da Fase 4. Os resultados da 3-B estavam espalhados (roadmap §2.1 a §2.3, achado 4.37, painel) e a troca cruzada não tinha leitura nenhuma. Tabelas geradas por `analisar_fase3b.py` (blocos `tb_`, conferidos por `--check`); os números do texto foram lidos de `analise_fase3b.json` por script. -->
# Fase 3-B: testes complementares, relatório e fechamento

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md). A Fase 3 está em [fase-3-relatorio-por-modelo.md](fase-3-relatorio-por-modelo.md) e a decisão do modelo em [analise-decisoria-modelo-final.md](analise-decisoria-modelo-final.md). As tabelas deste relatório saem de `analisar_fase3b.py` (`resultados_alvo/fase3/analise_fase3b.md`) e são conferidas por `--check`.

> **Estado em 01/10/2026:** todas as corridas previstas da Fase 3-B rodaram (576 diagnósticos nas quatro corridas com modelo, nenhum erro) e estão analisadas aqui. A decisão 52 (`qwen2.5:7b` com a biblioteca L1) se mantém. Ficam duas decisões do Eric, nas fichas 17 e 18 de [pendencias.md](../pendencias.md); nenhuma impede o planejamento da Fase 4.

## 1. O que a Fase 3-B veio responder

A análise decisória (§9) fechou a Fase 3 com sete limitações declaradas. A Fase 3-B mediu as que tinham teste barato (decisão 56) e ganhou, no caminho, a sonda de correção, o experimento do recuperador e a ablação.

| Pergunta | Corrida | Resposta em uma frase |
|---|---|---|
| A medida se repete quando o Ollama muda de versão? | Pontes de 21/09 (0.34.1) e de 30/09 (0.34.4) | Quase: com a mesma entrada, de 0 a 3 casos em 36 mudam de acerto entre corridas iguais, e em 0.34.4 o Coder 7B passou do limite combinado (§3) |
| O ganho da biblioteca escrita pelo modelo aparece em casos nunca vistos? | 36 casos inéditos (28/09) | Com a L1, não; com a L3, fica 2 casos acima de L0. Somando os 72 casos, as duas ficam acima de L0 sem alcançar o efeito mínimo detectável (§4) |
| O ganho é da biblioteca ou de quem a lê? | Troca cruzada (30/09 a 01/10) | Não é da biblioteca sozinha: lida por outro modelo, ela dá 1 caso de saldo ao Coder 7B, dentro da variação entre corridas, e tira 4 do Coder 3B (§5) |
| O modelo percebe quando um erro que ele documentou foi corrigido? | Sonda de correção (28/09) | Não, com o prompt da Fase 3 (roadmap §3; decisão 58) |
| Juntar busca por palavras e busca por embedding melhora a recuperação? | Experimento do recuperador (29/09) | Não com este modelo de embedding (roadmap §2.2; decisão 61) |
| Um modelo sem ajuste por instrução faz a tarefa? | Ablação base × instruct (29/09) | O `qwen2.5:0.5b-base` não faz (0 acertos em 90), e o instruct do mesmo porte quase não acerta: o piso está no porte (roadmap §2.2; achado 4.41) |

## 2. O que rodou

<!-- tabela:tb_corridas -->
| Corrida (pasta em `resultados_alvo/`) | Modo | Modelos | Registros | Ollama nos registros | Erros | Bibliotecas lidas (hash) | Início | Fim |
|---|---|---|---|---|---|---|---|---|
| `fase3b_ponte` | ponte | qwen2.5-coder:3b, qwen2.5-coder:7b, qwen2.5:7b | 108 | 0.34.1 | 0 | L0=3196327e7fd5 | 21/09 14:24 | 21/09 18:35 |
| `fase3b_ponte_0344` | ponte | qwen2.5-coder:3b, qwen2.5-coder:7b, qwen2.5:7b | 108 | 0.34.4 | 0 | L0=3196327e7fd5 | 30/09 20:39 | 30/09 22:25 |
| `fase3b_ineditos` | ineditos | qwen2.5-coder:3b, qwen2.5:7b | 216 | 0.34.1 | 0 | L0=3196327e7fd5; L1=3394d203cab9; L1=53ccf19abeac; L3=71258b553152; L3=d9a86e383103 | 28/09 20:13 | 28/09 23:15 |
| `fase3b_cruzada_qwen` | cruzada | qwen2.5-coder:3b, qwen2.5-coder:7b | 144 | 0.34.4 | 0 | L1=3394d203cab9; L3=71258b553152 | 30/09 23:58 | 01/10 02:09 |
| `fase3b_ineditos_coder7b` | ineditos | qwen2.5-coder:7b | 108 | 0.34.4 | 0 | L0=3196327e7fd5; L1=0f0a6b7f3b37; L3=2b7c441cb9e3 | 06/10 10:26 | 06/10 12:45 |
| `fase3b_a5` | a5 | qwen2.5-coder:3b, qwen2.5:7b | 72 | 0.34.4 | 0 | L3=71258b553152; L3=d9a86e383103 | 06/10 09:23 | 06/10 10:19 |
<!-- /tabela:tb_corridas -->

Todos os registros de cada corrida saíram na mesma versão do Ollama, sem erro. As duas corridas que o roadmap tinha como opcionais rodaram em 06/10/2026 (Ollama 0.34.4): o Coder 7B nos mesmos 36 inéditos, com as versões que ele mesmo escreveu (§4.1), e a adesão cega sobre a L3 própria (§4.2). A troca cruzada leu exatamente as bibliotecas oficiais do doador (hash `3394d203cab9` na L1 e `71258b553152` na L3). Nos casos inéditos, cada modelo leu as versões que ele mesmo escreveu: o `qwen2.5-coder:3b` leu a própria L1 e a própria L3, não as do `qwen2.5:7b`. A sonda de correção, o experimento do recuperador e a ablação têm saída própria e leitura no roadmap (§3 e §2.2).

## 3. Pontes de versão: o instrumento é estável?

A ponte repete a biblioteca original (L0) nos 36 casos de avaliação, com o mesmo prompt, sempre que o Ollama muda de versão, e compara caso a caso com a Fase 3. b conta os casos que só a ponte acertou e c os que só a Fase 3 acertou. O caso `efe-3` teve o texto corrigido em 28/09 (achado 4.36): a ponte de 30/09 leu o texto novo, e por isso as tabelas trazem a conta com ele e sem ele.

<!-- tabela:tb_pontes -->
| Ponte (Ollama) | Modelo | Acerto em L0 nos 36 (IC 95%) | Acurácia balanceada | b | c | p (McNemar) | Passaram a certos | Passaram a errados | Pareável (b + c até 2) | b / c sem o caso de texto corrigido | Caso de texto corrigido entre as corridas |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.34.1 | `qwen2.5-coder:3b` | 69,4% (53,1 a 82,0) | 68,8% | 0 | 0 | 1,0000 | nenhum | nenhum | sim | 0 / 0 | nenhum |
| 0.34.1 | `qwen2.5-coder:7b` | 75,0% (58,9 a 86,2) | 80,0% | 0 | 0 | 1,0000 | nenhum | nenhum | sim | 0 / 0 | nenhum |
| 0.34.1 | `qwen2.5:7b` | 77,8% (61,9 a 88,3) | 78,8% | 1 | 1 | 1,0000 | `sin-14` | `tra-10` | sim | 1 / 1 | nenhum |
| 0.34.4 | `qwen2.5-coder:3b` | 72,2% (56,0 a 84,2) | 70,4% | 1 | 0 | 1,0000 | `tra-4` | nenhum | sim | 1 / 0 | `efe-3` |
| 0.34.4 | `qwen2.5-coder:7b` | 80,6% (65,0 a 90,2) | 82,5% | 3 | 1 | 0,6250 | `efe-3`, `semt-14`, `tra-11` | `sin-14` | **não** | 2 / 1 | `efe-3` |
| 0.34.4 | `qwen2.5:7b` | 75,0% (58,9 a 86,2) | 79,6% | 0 | 1 | 1,0000 | nenhum | `tra-4` | sim | 0 / 1 | `efe-3` |
<!-- /tabela:tb_pontes -->

<!-- tabela:tb_ruido -->
| Modelo (L0, 36 casos) | Corrida A | Corrida B | Casos que mudaram de acerto | Com a mesma entrada (sem o caso de texto corrigido) | Só B acertou | Só A acertou | Rótulos que mudaram | Quais mudaram de acerto |
|---|---|---|---|---|---|---|---|---|
| `qwen2.5:7b` | Fase 3 (0.34.0) | ponte 0.34.1 | 2 | 2 | 1 | 1 | 3 | `sin-14`, `tra-10` |
| `qwen2.5:7b` | Fase 3 (0.34.0) | ponte 0.34.4 | 1 | 1 | 0 | 1 | 3 | `tra-4` |
| `qwen2.5:7b` | ponte 0.34.1 | ponte 0.34.4 | 3 | 3 | 1 | 2 | 3 | `sin-14`, `tra-10`, `tra-4` |
| `qwen2.5-coder:7b` | Fase 3 (0.34.0) | ponte 0.34.1 | 0 | 0 | 0 | 0 | 1 | nenhum |
| `qwen2.5-coder:7b` | Fase 3 (0.34.0) | ponte 0.34.4 | 4 | 3 | 3 | 1 | 4 | `efe-3`, `semt-14`, `sin-14`, `tra-11` |
| `qwen2.5-coder:7b` | ponte 0.34.1 | ponte 0.34.4 | 4 | 3 | 3 | 1 | 4 | `efe-3`, `semt-14`, `sin-14`, `tra-11` |
| `qwen2.5-coder:3b` | Fase 3 (0.34.0) | ponte 0.34.1 | 0 | 0 | 0 | 0 | 2 | nenhum |
| `qwen2.5-coder:3b` | Fase 3 (0.34.0) | ponte 0.34.4 | 1 | 1 | 1 | 0 | 2 | `tra-4` |
| `qwen2.5-coder:3b` | ponte 0.34.1 | ponte 0.34.4 | 1 | 1 | 1 | 0 | 4 | `tra-4` |
<!-- /tabela:tb_ruido -->

Leitura:
- **Em 0.34.1 os três modelos repetiram a Fase 3** dentro do limite da decisão 47 (b + c até 2).
- **Em 0.34.4 o Coder 7B saiu do limite**: b/c 3/1, ou 2/1 sem o `efe-3`, que são três casos e continuam acima de dois. Por isso a troca cruzada é lida contra o L0 desta ponte, na mesma versão, e não contra a Fase 3.
- **Com a mesma entrada, entre duas corridas do mesmo modelo mudam de acerto de 0 a 3 casos em 36**: de 1 a 3 no `qwen2.5:7b`, de 0 a 3 no Coder 7B e de 0 a 1 no 3B, e o saldo (ganhos menos perdas) não passa de 1 caso. Contando o `efe-3`, que não é a mesma entrada, o Coder 7B chega a 4 trocas e a saldo de 2. Em rótulo respondido, que muda mais que o acerto, são de 1 a 4 casos por par de corridas. O achado 4.31 falava em 0 a 2 casos; a medida de 30/09 alarga a faixa.
- **Não dá para separar a versão do acaso**: há uma corrida por versão, com temperatura 0,1 e sem semente fixa. No `qwen2.5:7b`, os dois casos que mudaram em 0.34.1 (`sin-14` e `tra-10`) voltaram ao resultado da Fase 3 em 0.34.4, e mudou outro (`tra-4`).
- **O que isso muda na leitura de todo o resto:** uma diferença de até 3 casos trocados, ou de 1 caso de saldo, entre duas corridas únicas não é evidência sozinha. O ganho da L1 na Fase 3 (4 ganhos, 0 perdas) fica acima dessa faixa de saldo, sem alcançar significância (p = 0,125).

## 4. Casos inéditos: o ganho generaliza?

Trinta e seis casos novos, dois por combinação de classe e nível, escritos só a partir do código do sistema-cobaia e nunca vistos por modelo nenhum, diagnosticados com a biblioteca original e com as versões que cada modelo escreveu.

<!-- tabela:tb_ineditos -->
| Modelo | Biblioteca | Acerto nos 36 inéditos (IC 95%) | Acurácia balanceada | Contra L0: b / c | p (McNemar) | Rótulos que mudaram contra L0 | s por diagnóstico (mediana) |
|---|---|---|---|---|---|---|---|
| `qwen2.5-coder:3b` | L0 | 58,3% (42,2 a 72,9) | 68,1% | n/a | n/a | n/a | 38,1 |
| `qwen2.5-coder:3b` | L1 | 58,3% (42,2 a 72,9) | 68,1% | 0 / 0 | 1,0000 | 0 | 22,3 |
| `qwen2.5-coder:3b` | L3 | 58,3% (42,2 a 72,9) | 68,1% | 0 / 0 | 1,0000 | 1 | 27,8 |
| `qwen2.5-coder:7b` | L0 | 83,3% (68,1 a 92,1) | 86,2% | n/a | n/a | n/a | 74,1 |
| `qwen2.5-coder:7b` | L1 | 86,1% (71,3 a 93,9) | 90,6% | 1 / 0 | 1,0000 | 2 | 71,3 |
| `qwen2.5-coder:7b` | L3 | 75,0% (58,9 a 86,2) | 80,4% | 0 / 3 | 0,2500 | 4 | 79,5 |
| `qwen2.5:7b` | L0 | 75,0% (58,9 a 86,2) | 81,2% | n/a | n/a | n/a | 73,0 |
| `qwen2.5:7b` | L1 | 72,2% (56,0 a 84,2) | 79,0% | 0 / 1 | 1,0000 | 3 | 75,5 |
| `qwen2.5:7b` | L3 | 80,6% (65,0 a 90,2) | 87,0% | 3 / 1 | 0,6250 | 6 | 66,0 |
<!-- /tabela:tb_ineditos -->

<!-- tabela:tb_agrupado -->
| Modelo | Biblioteca | Casos (oficiais + inéditos) | Acerto com L0 | Acerto com a biblioteca | Oficiais: b / c | Inéditos: b / c | Somados: b / c | Diferença | p (McNemar) |
|---|---|---|---|---|---|---|---|---|---|
| `qwen2.5-coder:3b` | L1 | 72 | 63,9% | 65,3% | 1 / 0 | 0 / 0 | 1 / 0 | +1,4 pp | 1,0000 |
| `qwen2.5-coder:3b` | L3 | 72 | 63,9% | 65,3% | 1 / 0 | 0 / 0 | 1 / 0 | +1,4 pp | 1,0000 |
| `qwen2.5-coder:7b` | L1 | 72 | 79,2% | 80,6% | 0 / 0 | 1 / 0 | 1 / 0 | +1,4 pp | 1,0000 |
| `qwen2.5-coder:7b` | L3 | 72 | 79,2% | 76,4% | 3 / 2 | 0 / 3 | 3 / 5 | -2,8 pp | 0,7266 |
| `qwen2.5:7b` | L1 | 72 | 76,4% | 80,6% | 4 / 0 | 0 / 1 | 4 / 1 | +4,2 pp | 0,3750 |
| `qwen2.5:7b` | L3 | 72 | 76,4% | 83,3% | 3 / 0 | 3 / 1 | 6 / 1 | +6,9 pp | 0,1250 |
<!-- /tabela:tb_agrupado -->

Leitura:
- **O ganho da L1 não reaparece.** Nos 36 oficiais o `qwen2.5:7b` subiu de 77,8% para 88,9% com a L1; nos inéditos vai de 75,0% para 72,2% (b/c 0/1).
- **A L3 fica acima de L0 nos dois conjuntos**: b/c 3/0 nos oficiais e 3/1 nos inéditos.
- **Com os 72 casos somados, as duas versões ficam acima de L0 e nenhuma resolve**: L1 de 76,4% para 80,6% (b/c 4/1, p = 0,375) e L3 para 83,3% (b/c 6/1, p = 0,125). O efeito mínimo detectável com 72 casos é de 13,9 pontos; o maior ganho medido é de 6,9. Para o `qwen2.5:7b`, o primeiro modelo de 7B com os 72 casos (o Coder 7B ganhou os seus em 06/10, §4.1), a hipótese H1 continua não confirmada: falta resolução, e o sinal é pequeno.
- **Entre L1 e L3 a diferença é de 2 casos em 72** (58 acertos com a L1, 60 com a L3): a L1 fica 1 caso à frente nos oficiais (32 contra 31) e a L3 fica 3 à frente nos inéditos (29 contra 26). Está dentro da faixa de variação entre corridas do §3.
- **O `qwen2.5-coder:3b` acerta o mesmo com L0, com a própria L1 e com a própria L3** (58,3% nas três; b/c 0/0), embora 13,9% dos contextos com a L1 e 47,2% com a L3 já tragam nota escrita por ele. Nos inéditos só 1 rótulo muda, com a L3, de um erro para outro; nos 36 oficiais as notas próprias mudam 3 rótulos com a L1 e 2 com a L3, com 1 acerto ganho em cada.
- Os inéditos rodaram em Ollama 0.34.1, com ponte pareável nos dois modelos. Os tempos por diagnóstico desta tabela e da tabela do §5 foram medidos com a sessão de trabalho aberta na máquina e valem como ordem de grandeza; o custo comparável é o da Fase 3 (relatório da Fase 3, §9).

<!-- ! Alteração de IA - Revisar: subseções 4.1 e 4.2 novas (06/10/2026) com as duas corridas opcionais que o Eric rodou na tarde de 06/10, depois de fechar a ficha 17 como (b); os blocos vêm de analisar_fase3b.py (--colar).
     ! Motivo: a ficha 17 dizia que as opcionais não rodariam; o Eric rodou as duas mesmo assim, e o resultado da corrida 7 toca a condição 1 do comparativo qwen × Coder para rever a decisão 52 (ficha 21). Ficam como subseções do §4 para não renumerar as seções que o painel e as fichas citam. -->
### 4.1 Corrida 7 (06/10/2026): o Coder 7B nos mesmos 36 inéditos

O `qwen2.5-coder:7b` diagnosticou os 36 inéditos com a biblioteca original e com as versões L1 e L3 que ele mesmo escreveu na Fase 3 (hash `0f0a6b7f3b37` e `2b7c441cb9e3`), em Ollama 0.34.4, 06/10 10:26 a 06/10 12:45. A tabela abaixo confronta, caso a caso, cada modelo com o `qwen2.5:7b` (que rodou os mesmos 36 em 28/09, Ollama 0.34.1), com a biblioteca de cada um; b conta os casos que só o modelo acertou e c os que só o `qwen2.5:7b` acertou. A última coluna de cada classe traz os acertos do modelo e do `qwen2.5:7b` nos 6 casos da classe.

<!-- tabela:tb_ineditos_modelos -->
| Modelo | Biblioteca (a de cada um) | Acerto nos 36 inéditos | Acerto do `qwen2.5:7b` | b (só o modelo) | c (só o doador) | Diferença | p (McNemar) | Rótulos diferentes | Nos 72 (oficiais + inéditos): b / c | p nos 72 | lexica: modelo / doador (acertos de n) | sintatica: modelo / doador (acertos de n) | semantica: modelo / doador (acertos de n) | traducao: modelo / doador (acertos de n) | runtime: modelo / doador (acertos de n) | efeito: modelo / doador (acertos de n) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `qwen2.5-coder:3b` | L0 | 58,3% | 75,0% | 1 | 7 | -16,7 pp | 0,0703 | 12 | 6 / 15 | 0,0784 | 3 / 4 (de 6) | 5 / 6 (de 6) | 3 / 5 (de 6) | 2 / 4 (de 6) | 6 / 6 (de 6) | 2 / 2 (de 6) |
| `qwen2.5-coder:3b` | L1 | 58,3% | 72,2% | 1 | 6 | -13,9 pp | 0,1250 | 12 | 3 / 14 | 0,0127 | 3 / 4 (de 6) | 5 / 6 (de 6) | 3 / 4 (de 6) | 2 / 4 (de 6) | 6 / 6 (de 6) | 2 / 2 (de 6) |
| `qwen2.5-coder:3b` | L3 | 58,3% | 80,6% | 0 | 8 | -22,2 pp | 0,0078 | 12 | 2 / 15 | 0,0023 | 3 / 6 (de 6) | 5 / 6 (de 6) | 3 / 4 (de 6) | 2 / 4 (de 6) | 6 / 6 (de 6) | 2 / 3 (de 6) |
| `qwen2.5-coder:7b` | L0 | 83,3% | 75,0% | 4 | 1 | +8,3 pp | 0,3750 | 7 | 8 / 6 | 0,7905 | 5 / 4 (de 6) | 6 / 6 (de 6) | 5 / 5 (de 6) | 4 / 4 (de 6) | 6 / 6 (de 6) | 4 / 2 (de 6) |
| `qwen2.5-coder:7b` | L1 | 86,1% | 72,2% | 6 | 1 | +13,9 pp | 0,1250 | 8 | 7 / 7 | 1,0000 | 6 / 4 (de 6) | 6 / 6 (de 6) | 5 / 4 (de 6) | 4 / 4 (de 6) | 6 / 6 (de 6) | 4 / 2 (de 6) |
| `qwen2.5-coder:7b` | L3 | 75,0% | 80,6% | 1 | 3 | -5,6 pp | 0,6250 | 6 | 3 / 8 | 0,2266 | 5 / 6 (de 6) | 6 / 6 (de 6) | 5 / 4 (de 6) | 2 / 4 (de 6) | 6 / 6 (de 6) | 3 / 3 (de 6) |
<!-- /tabela:tb_ineditos_modelos -->

Leitura:
- **Nos inéditos o Coder 7B fica à frente com L0 e com L1 e atrás com L3.** Com a biblioteca original, 83,3% contra 75,0% (b/c 4/1, p = 0,375); com a L1 de cada um, 86,1% contra 72,2% (b/c 6/1, p = 0,125); com a L3, 75,0% contra 80,6% (b/c 1/3). Nenhuma diferença chega ao efeito mínimo detectável de 19,4 pontos nos 36.
- **Nos 72 casos (36 oficiais da Fase 3 mais os 36 inéditos), com a L1 de cada um, o placar é 7/7** (p = 1,000): o que o Coder ganha nos inéditos é o que perde nos oficiais. Com L0, 8/6; com L3, 3/8.
- **Por classe, com a L1** (6 casos cada; um caso vale 16,7 pontos): o Coder ganha em lexica, semantica, efeito e empata em sintatica, traducao, runtime. É o mesmo padrão parcial das fases anteriores (léxica e efeito) com a semântica invertida.
- **A biblioteca própria do Coder 7B pouco muda nos inéditos**: contra o próprio L0, a L1 ganha 1 caso e a L3 perde 3 (bloco `tb_ineditos`); nos 72 somados, a L1 fica 1 caso acima de L0 e a L3 2 abaixo (bloco `tb_agrupado`).
- **O Coder 3B fica bem atrás do `qwen2.5:7b` nos mesmos casos**: 58,3% contra 72,2% com a L1 de cada um (b/c 1/6); nos 72, 3/14 (p = 0,0127).
- A condição 1 do comparativo qwen × Coder para rever a decisão 52 ("o Coder vencer o qwen nos casos inéditos") fica parcialmente cumprida, dentro do ruído de uma corrida por condição (de 0 a 3 casos, §3). O que fazer com isso é a ficha 21.

### 4.2 Corrida 5 (06/10/2026): adesão cega à documentação errada, com a biblioteca própria

Na condição A5 o contexto traz um verbete de erro de causa diferente da do caso e um registro de incidente fabricado que afirma essa causa errada para o sintoma; o verbete de ouro nunca está no contexto. A Fase 2-B mediu essa adesão com a biblioteca original; aqui cada modelo leu a própria L3, nos 36 casos de avaliação, em Ollama 0.34.4 (06/10 09:23 a 06/10 10:19).

<!-- tabela:tb_a5 -->
| Modelo | Biblioteca | Casos | Seguiu a causa plantada | Acertou mesmo assim | O mesmo modelo, a mesma biblioteca, em A2 (Fase 3, acerto) | Adesão cega na Fase 2-B (A5 sobre a biblioteca original) | Verbete de ouro no contexto |
|---|---|---|---|---|---|---|---|
| `qwen2.5-coder:3b` | L3 própria | 36 | 34 (94,4%) | 2 (5,6%) | 72,2% | 95,6% | 0,0% |
| `qwen2.5:7b` | L3 própria | 36 | 29 (80,6%) | 7 (19,4%) | 86,1% | não medida | 0,0% |
<!-- /tabela:tb_a5 -->

Leitura:
- **A biblioteca própria não muda a adesão cega.** O `qwen2.5-coder:3b` segue a causa plantada em 94,4% dos casos com a própria L3, contra 95,6% na Fase 2-B com a biblioteca original; o `qwen2.5:7b`, que não tinha medida de A5 na 2-B, segue em 80,6% e acerta 19,4%, contra 86,1% com a mesma L3 na condição normal (A2).
- É o mesmo mecanismo da troca cruzada (§5) e da Fase 2-B: o modelo lê e segue o que a documentação afirma, para o bem e para o mal. Para a Fase 4, reforça que o que entra na biblioteca precisa de validação em código antes, e que uma nota errada num verbete muito recuperado vira resposta errada.
- H5 (autoenvenenamento) não muda: a adesão é à documentação errada entregue, não a notas que o modelo escreveu; com a própria L3 em A2 os dois modelos acertam como na Fase 3.

## 5. Troca cruzada: o ganho é da biblioteca ou de quem a lê?

Os dois Coder diagnosticaram os mesmos 36 casos, com o mesmo prompt e a mesma recuperação, lendo as bibliotecas L1 e L3 escritas pelo `qwen2.5:7b`. A linha de base de cada leitor é o próprio L0 na ponte de 30/09, na mesma versão do Ollama e com o mesmo texto dos casos.

<!-- tabela:tb_cruzada -->
| Quem lê | Biblioteca lida | Acerto nos 36 (IC 95%) | Acurácia balanceada | Verbete de ouro no contexto | Contexto com nota | Citou verbete anotado | Tokens de entrada (mediana) | s por diagnóstico (mediana) |
|---|---|---|---|---|---|---|---|---|
| `qwen2.5:7b` | L0, Fase 3 (Ollama 0.34.0) | 77,8% (61,9 a 88,3) | 81,2% | 86,1% | 0,0% | 0,0% | 1044 | 69,5 |
| `qwen2.5:7b` | L0, ponte (Ollama 0.34.4) | 75,0% (58,9 a 86,2) | 79,6% | 86,1% | 0,0% | 0,0% | 1044 | 68,9 |
| `qwen2.5:7b` | L1 própria, Fase 3 (Ollama 0.34.0) | 88,9% (74,7 a 95,6) | 91,7% | 83,3% | 94,4% | 66,7% | 1294 | 79,5 |
| `qwen2.5:7b` | L3 própria, Fase 3 (Ollama 0.34.0) | 86,1% (71,3 a 93,9) | 86,2% | 86,1% | 94,4% | 83,3% | 1438 | 53,9 |
| `qwen2.5-coder:7b` | L0, Fase 3 (Ollama 0.34.0) | 75,0% (58,9 a 86,2) | 80,0% | 86,1% | 0,0% | 0,0% | 1044 | 70,7 |
| `qwen2.5-coder:7b` | L0, ponte (Ollama 0.34.4) | 80,6% (65,0 a 90,2) | 82,5% | 86,1% | 0,0% | 0,0% | 1044 | 72,0 |
| `qwen2.5-coder:7b` | L1 própria, Fase 3 (Ollama 0.34.0) | 75,0% (58,9 a 86,2) | 80,0% | 86,1% | 72,2% | 55,6% | 1102 | 65,8 |
| `qwen2.5-coder:7b` | L3 própria, Fase 3 (Ollama 0.34.0) | 77,8% (61,9 a 88,3) | 84,2% | 86,1% | 100,0% | 55,6% | 1207 | 56,6 |
| `qwen2.5-coder:7b` | L1 do doador, cruzada (Ollama 0.34.4) | 83,3% (68,1 a 92,1) | 88,3% | 83,3% | 94,4% | 69,4% | 1295 | 76,6 |
| `qwen2.5-coder:7b` | L3 do doador, cruzada (Ollama 0.34.4) | 83,3% (68,1 a 92,1) | 88,3% | 86,1% | 94,4% | 77,8% | 1438 | 71,3 |
| `qwen2.5-coder:3b` | L0, Fase 3 (Ollama 0.34.0) | 69,4% (53,1 a 82,0) | 68,8% | 86,1% | 0,0% | 0,0% | 1044 | 32,2 |
| `qwen2.5-coder:3b` | L0, ponte (Ollama 0.34.4) | 72,2% (56,0 a 84,2) | 70,4% | 86,1% | 0,0% | 0,0% | 1044 | 30,9 |
| `qwen2.5-coder:3b` | L1 própria, Fase 3 (Ollama 0.34.0) | 72,2% (56,0 a 84,2) | 70,4% | 86,1% | 8,3% | 8,3% | 1046 | 17,8 |
| `qwen2.5-coder:3b` | L3 própria, Fase 3 (Ollama 0.34.0) | 72,2% (56,0 a 84,2) | 71,2% | 86,1% | 50,0% | 27,8% | 1074 | 20,9 |
| `qwen2.5-coder:3b` | L1 do doador, cruzada (Ollama 0.34.4) | 61,1% (44,9 a 75,2) | 60,4% | 83,3% | 94,4% | 52,8% | 1295 | 35,2 |
| `qwen2.5-coder:3b` | L3 do doador, cruzada (Ollama 0.34.4) | 61,1% (44,9 a 75,2) | 60,4% | 86,1% | 94,4% | 77,8% | 1438 | 29,5 |
<!-- /tabela:tb_cruzada -->

<!-- tabela:tb_cruzada_pareados -->
| Leitor com a biblioteca do doador | Comparado com | Mesma versão do Ollama | Pareável pela ponte | b (ganhos) | c (perdas) | Diferença | p (McNemar) | b / c sem o caso de texto corrigido | Rótulos que mudaram | Ganhou | Perdeu | Trocas em casos que já oscilam entre corridas de L0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `qwen2.5-coder:7b` lendo L1 | o próprio L0 na ponte (mesma versão do Ollama) | sim | sim | 3 | 2 | +2,8 pp | 1,0000 | 3 / 2 | 5 | `semt-8`, `sin-14`, `tra-10` | `semt-14`, `sin-5` | `semt-14`, `sin-14` |
| `qwen2.5-coder:7b` lendo L1 | a própria biblioteca na Fase 3 | não | não | 4 | 1 | +8,3 pp | 0,3750 | 3 / 1 | 6 | `efe-3`, `semt-8`, `tra-10`, `tra-11` | `sin-5` | n/a |
| `qwen2.5-coder:7b` lendo L1 | o doador lendo a mesma biblioteca (Fase 3) | não | não | 1 | 3 | -5,6 pp | 0,6250 | 0 / 3 | 5 | `efe-3` | `semt-14`, `tra-4`, `tra-8` | n/a |
| `qwen2.5-coder:7b` lendo L3 | o próprio L0 na ponte (mesma versão do Ollama) | sim | sim | 3 | 2 | +2,8 pp | 1,0000 | 3 / 2 | 5 | `semt-8`, `sin-14`, `tra-10` | `semt-14`, `tra-11` | `semt-14`, `sin-14`, `tra-11` |
| `qwen2.5-coder:7b` lendo L3 | a própria biblioteca na Fase 3 | não | não | 2 | 0 | +5,6 pp | 0,5000 | 2 / 0 | 2 | `sin-14`, `sin-5` | nenhum | n/a |
| `qwen2.5-coder:7b` lendo L3 | o doador lendo a mesma biblioteca (Fase 3) | não | não | 3 | 4 | -2,8 pp | 1,0000 | 3 / 4 | 7 | `efe-1`, `run-10`, `sin-14` | `semt-14`, `tra-11`, `tra-4`, `tra-8` | n/a |
| `qwen2.5-coder:3b` lendo L1 | o próprio L0 na ponte (mesma versão do Ollama) | sim | sim | 1 | 5 | -11,1 pp | 0,2188 | 1 / 5 | 8 | `semt-3` | `efe-3`, `semt-8`, `sin-11`, `sin-14`, `sin-5` | nenhum |
| `qwen2.5-coder:3b` lendo L1 | a própria biblioteca na Fase 3 | não | sim | 1 | 5 | -11,1 pp | 0,2188 | 1 / 4 | 7 | `semt-3` | `efe-3`, `semt-8`, `sin-11`, `sin-14`, `sin-5` | n/a |
| `qwen2.5-coder:3b` lendo L1 | o doador lendo a mesma biblioteca (Fase 3) | não | sim | 0 | 10 | -27,8 pp | 0,0020 | 0 / 10 | 13 | nenhum | `efe-1`, `efe-2`, `lex-1`, `lex-4`, `semt-14`, `semt-8`, `sin-11`, `sin-14`, `sin-4`, `tra-10` | n/a |
| `qwen2.5-coder:3b` lendo L3 | o próprio L0 na ponte (mesma versão do Ollama) | sim | sim | 1 | 5 | -11,1 pp | 0,2188 | 1 / 5 | 8 | `semt-3` | `efe-3`, `semt-8`, `sin-11`, `sin-14`, `sin-5` | nenhum |
| `qwen2.5-coder:3b` lendo L3 | a própria biblioteca na Fase 3 | não | sim | 1 | 5 | -11,1 pp | 0,2188 | 1 / 4 | 8 | `tra-4` | `efe-3`, `semt-8`, `sin-11`, `sin-14`, `sin-5` | n/a |
| `qwen2.5-coder:3b` lendo L3 | o doador lendo a mesma biblioteca (Fase 3) | não | sim | 1 | 10 | -25,0 pp | 0,0117 | 1 / 9 | 13 | `run-10` | `efe-2`, `efe-3`, `lex-1`, `lex-4`, `semt-14`, `semt-8`, `sin-11`, `sin-4`, `sin-5`, `tra-10` | n/a |
<!-- /tabela:tb_cruzada_pareados -->

Leitura:
- **Coder 7B: 1 caso de saldo.** Vai de 80,6% para 83,3% de acerto (82,5% para 88,3% de acurácia balanceada), com 3 ganhos e 2 perdas (p = 1,0). Mesmo placar com a L1 e com a L3. Está dentro da variação entre corridas: 2 das 5 trocas com a L1 e 3 das 5 com a L3 caem em casos que já oscilam entre corridas de L0 do próprio modelo.
- **Coder 3B: 4 casos a menos.** Cai de 72,2% para 61,1% (70,4% para 60,4% de acurácia balanceada), com 1 ganho e 5 perdas (p = 0,2188); nenhuma das 6 trocas cai em caso que oscila sozinho. É o único saldo da troca cruzada fora da faixa de variação do §3, ainda sem significância. As respostas com a L1 e com a L3 são idênticas caso a caso, de modo que o Q de Cochran sobre L0, L1 e L3 (5,33, p = 0,0695) repete o mesmo contraste e não acrescenta evidência.
- **A mesma biblioteca, lida por quem a escreveu, rende mais.** Com a L1, o `qwen2.5:7b` acerta 88,9%; o Coder 7B, 83,3% (b/c 1/3 contra o doador, p = 0,625); o Coder 3B, 61,1% (b/c 0/10, p = 0,002). A diferença entre o 3B e o doador com a L1 é a única da 3-B com p abaixo de 0,05, e continua abaixo depois da correção de Holm sobre os doze pareamentos da tabela (0,002 × 12 = 0,024). Com a L3 ela é de b/c 1/10 (p = 0,0117; 1/9 sem o `efe-3`) e não se mantém depois da correção. São comparações entre modelos diferentes e entre versões do Ollama (0.34.0 e 0.34.4), com ponte pareável nos dois.
- **O arranjo "escreve o melhor, lê o mais barato" não se sustenta**: o 3B com a biblioteca do `qwen2.5:7b` acerta menos do que sem ela. "Melhor", aqui, é o modelo que mais acerta com a própria biblioteca, não o que escreve as notas mais corretas (§6).

<!-- tabela:tb_cruzada_classe -->
| Quem lê | Biblioteca lida | lexica (acertos / casos) | sintatica (acertos / casos) | semantica (acertos / casos) | traducao (acertos / casos) | runtime (acertos / casos) | efeito (acertos / casos) |
|---|---|---|---|---|---|---|---|
| `qwen2.5-coder:7b` | L0 (ponte) | 6 / 6 | 5 / 6 | 4 / 6 | 2 / 6 | 6 / 6 | 6 / 6 |
| `qwen2.5-coder:7b` | L1 do doador | 6 / 6 | 5 / 6 | 4 / 6 | 3 / 6 | 6 / 6 | 6 / 6 |
| `qwen2.5-coder:7b` | L3 do doador | 6 / 6 | 6 / 6 | 4 / 6 | 2 / 6 | 6 / 6 | 6 / 6 |
| `qwen2.5-coder:7b` | L1 própria (Fase 3) | 6 / 6 | 6 / 6 | 3 / 6 | 1 / 6 | 6 / 6 | 5 / 6 |
| `qwen2.5-coder:7b` | L3 própria (Fase 3) | 6 / 6 | 4 / 6 | 4 / 6 | 2 / 6 | 6 / 6 | 6 / 6 |
| `qwen2.5-coder:3b` | L0 (ponte) | 4 / 6 | 5 / 6 | 3 / 6 | 4 / 6 | 6 / 6 | 4 / 6 |
| `qwen2.5-coder:3b` | L1 do doador | 4 / 6 | 2 / 6 | 3 / 6 | 4 / 6 | 6 / 6 | 3 / 6 |
| `qwen2.5-coder:3b` | L3 do doador | 4 / 6 | 2 / 6 | 3 / 6 | 4 / 6 | 6 / 6 | 3 / 6 |
| `qwen2.5-coder:3b` | L1 própria (Fase 3) | 4 / 6 | 5 / 6 | 3 / 6 | 4 / 6 | 6 / 6 | 4 / 6 |
| `qwen2.5-coder:3b` | L3 própria (Fase 3) | 4 / 6 | 5 / 6 | 4 / 6 | 3 / 6 | 6 / 6 | 4 / 6 |
<!-- /tabela:tb_cruzada_classe -->

Por classe, a perda do 3B se concentra na sintática (5 acertos em 6 com L0, 2 com a biblioteca do doador) e no efeito (4 para 3); léxica, semântica, tradução e runtime ficam com o mesmo total.

<!-- tabela:tb_cruzada_rotulos -->
| Quem lê | Biblioteca lida | Rótulo mais respondido | Respostas com ele | Respostas com ele em L0 | Casos com essa causa no gabarito | Rótulos distintos | Verbetes mais citados na linha FONTE (respostas) | Verbetes mais presentes no contexto (casos) |
|---|---|---|---|---|---|---|---|---|
| `qwen2.5-coder:7b` | L1 do doador | `estrutura_aninhada_divergente` | 4 (11,1%) | 3 | 1 | 20 | `entidade-produto` (5); `localizador_quebrado` (4); `contrato-pedido` (3) | `entidade-produto` (18); `contrato-produto` (15); `contrato-pedido` (9) |
| `qwen2.5-coder:7b` | L3 do doador | `estrutura_aninhada_divergente` | 4 (11,1%) | 3 | 1 | 19 | `estrutura_aninhada_divergente` (4); `localizador_quebrado` (4); `contrato-pedido` (3) | `entidade-produto` (18); `contrato-produto` (15); `contrato-pedido` (9) |
| `qwen2.5-coder:7b` | L0 (ponte) | `campo_ausente` | 4 (11,1%) | 4 | 3 | 19 | `contrato-pedido` (4); `localizador_quebrado` (4); `entidade-produto` (3) | `entidade-produto` (19); `contrato-produto` (16); `contrato-pedido` (9) |
| `qwen2.5-coder:3b` | L1 do doador | `corpo_nao_e_json` | 7 (19,4%) | 2 | 0 | 17 | `contrato-produto` (10); `contrato-pedido` (6); `contagem_inconsistente` (4) | `entidade-produto` (18); `contrato-produto` (15); `contrato-pedido` (9) |
| `qwen2.5-coder:3b` | L3 do doador | `corpo_nao_e_json` | 7 (19,4%) | 2 | 0 | 17 | `contrato-produto` (10); `contrato-pedido` (6); `contagem_inconsistente` (3) | `entidade-produto` (18); `contrato-produto` (15); `contrato-pedido` (9) |
| `qwen2.5-coder:3b` | L0 (ponte) | `campo_ausente` | 6 (16,7%) | 6 | 3 | 18 | `contrato-produto` (6); `contrato-pedido` (5); `contagem_inconsistente` (4) | `entidade-produto` (19); `contrato-produto` (16); `contrato-pedido` (9) |
<!-- /tabela:tb_cruzada_rotulos -->

<!-- tabela:tb_cruzada_casos -->
| Quem lê | Biblioteca do doador | Caso | Passou a | Causa do gabarito | Resposta com L0 | Resposta com a biblioteca do doador | Fonte citada com L0 | Fonte citada com a biblioteca do doador | Verbete de ouro no contexto | O doador acerta este caso com ela |
|---|---|---|---|---|---|---|---|---|---|---|
| `qwen2.5-coder:7b` | L1 | `semt-14` | errado | `nulo_inesperado` | `nulo_inesperado` | `campo_ausente` | `entidade-produto` | `contrato-produto` | sim | sim |
| `qwen2.5-coder:7b` | L1 | `semt-8` | certo | `nulo_inesperado` | `valor_fora_do_dominio` | `nulo_inesperado` | `contrato-produto` | `nulo_inesperado` | sim | sim |
| `qwen2.5-coder:7b` | L1 | `sin-14` | certo | `campo_renomeado` | `campo_ausente` | `campo_renomeado` | `contrato-produto` | `campo_renomeado` | sim | sim |
| `qwen2.5-coder:7b` | L1 | `sin-5` | errado | `campo_ausente` | `campo_ausente` | `estrutura_aninhada_divergente` | `campo_ausente` | `entidade-produto` | não | não |
| `qwen2.5-coder:7b` | L1 | `tra-10` | certo | `chave_de_juncao_errada` | `valor_fora_do_dominio` | `chave_de_juncao_errada` | `contrato-pedido` | `contrato-pedido` | não | sim |
| `qwen2.5-coder:7b` | L3 | `semt-14` | errado | `nulo_inesperado` | `nulo_inesperado` | `tipo_divergente` | `entidade-produto` | `contrato-produto` | sim | sim |
| `qwen2.5-coder:7b` | L3 | `semt-8` | certo | `nulo_inesperado` | `valor_fora_do_dominio` | `nulo_inesperado` | `contrato-produto` | `nulo_inesperado` | sim | sim |
| `qwen2.5-coder:7b` | L3 | `sin-14` | certo | `campo_renomeado` | `campo_ausente` | `campo_renomeado` | `contrato-produto` | `campo_renomeado` | sim | não |
| `qwen2.5-coder:7b` | L3 | `tra-10` | certo | `chave_de_juncao_errada` | `valor_fora_do_dominio` | `chave_de_juncao_errada` | `contrato-pedido` | `contrato-pedido` | não | sim |
| `qwen2.5-coder:7b` | L3 | `tra-11` | errado | `contagem_inconsistente` | `contagem_inconsistente` | `estrutura_aninhada_divergente` | `contagem_inconsistente` | `estrutura_aninhada_divergente` | sim | sim |
| `qwen2.5-coder:3b` | L1 | `efe-3` | errado | `campo_ausente` | `campo_ausente` | `corpo_nao_e_json` | `campo_ausente` | `contrato-produto` | sim | não |
| `qwen2.5-coder:3b` | L1 | `semt-3` | certo | `valor_fora_do_dominio` | `estado_da_tela_divergente` | `valor_fora_do_dominio` | `estado_da_tela_divergente` | `contrato-pedido` | sim | sim |
| `qwen2.5-coder:3b` | L1 | `semt-8` | errado | `nulo_inesperado` | `nulo_inesperado` | `corpo_nao_e_json` | `nulo_inesperado` | `contrato-produto` | sim | sim |
| `qwen2.5-coder:3b` | L1 | `sin-11` | errado | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | `corpo_vazio` | `estrutura_aninhada_divergente` | `entidade-produto`, `contagem_inconsistente` | sim | sim |
| `qwen2.5-coder:3b` | L1 | `sin-14` | errado | `campo_renomeado` | `campo_renomeado` | `corpo_nao_e_json` | `campo_renomeado` | `contrato-produto` | sim | sim |
| `qwen2.5-coder:3b` | L1 | `sin-5` | errado | `campo_ausente` | `campo_ausente` | `corpo_nao_e_json` | `campo_ausente` | `contrato-produto` | não | não |
| `qwen2.5-coder:3b` | L3 | `efe-3` | errado | `campo_ausente` | `campo_ausente` | `corpo_nao_e_json` | `campo_ausente` | `entidade-produto`, `contrato-produto` | sim | sim |
| `qwen2.5-coder:3b` | L3 | `semt-3` | certo | `valor_fora_do_dominio` | `estado_da_tela_divergente` | `valor_fora_do_dominio` | `estado_da_tela_divergente` | `contrato-pedido`, `valor_fora_do_dominio` | sim | sim |
| `qwen2.5-coder:3b` | L3 | `semt-8` | errado | `nulo_inesperado` | `nulo_inesperado` | `corpo_nao_e_json` | `nulo_inesperado` | `contrato-produto` | sim | sim |
| `qwen2.5-coder:3b` | L3 | `sin-11` | errado | `estrutura_aninhada_divergente` | `estrutura_aninhada_divergente` | `corpo_vazio` | `estrutura_aninhada_divergente` | nenhum | sim | sim |
| `qwen2.5-coder:3b` | L3 | `sin-14` | errado | `campo_renomeado` | `campo_renomeado` | `corpo_nao_e_json` | `campo_renomeado` | `contrato-produto` | sim | não |
| `qwen2.5-coder:3b` | L3 | `sin-5` | errado | `campo_ausente` | `campo_ausente` | `corpo_nao_e_json` | `campo_ausente` | `contrato-produto` | sim | sim |
<!-- /tabela:tb_cruzada_casos -->

O que acontece com o 3B, caso a caso:
- **Ele passa a responder `corpo_nao_e_json`.** Nenhum dos 36 casos tem essa causa no gabarito. Com L0 o 3B dá essa resposta 2 vezes; com a biblioteca do doador, 7 vezes (19,4% das respostas), e ela vira o rótulo mais frequente. O Coder 7B, com a mesma biblioteca, dá essa resposta 0 vezes.
- **A fonte que ele cita é `contrato-produto`**: 10 respostas com a biblioteca do doador, contra 6 com L0. O verbete está no contexto de 15 dos 36 casos.
- **Com a L1, em 4 das 5 perdas a resposta nova é `corpo_nao_e_json` e em 4 das 5 o verbete de ouro estava no contexto** (com a L3, nas 5). Nesses casos o erro não é de recuperação: o modelo tinha o verbete certo na frente e seguiu outro.
- **O que mudou nesse verbete:** na L1 do doador, `contrato-produto` recebeu três edições da época 1 (planilha de curadoria): uma nota, avaliada como parcial, que diz que "o contrato especifica a estrutura do JSON esperado", e duas retificações avaliadas como erradas. A ligação entre a nota e a troca de rótulo é leitura dos registros, não medida isolada.
- **Em rótulos, a biblioteca do doador muda 8 das 36 respostas do 3B**; entre corridas iguais dele mudam de 2 a 4, e as notas que ele escreveu para si mudam de 0 a 3.

Síntese. No 3B as notas do doador mudam respostas além da variação entre corridas (6 acertos e 8 rótulos, contra 0 a 1 acerto e 2 a 4 rótulos entre corridas iguais), e para pior. No Coder 7B as 5 trocas cabem na variação. Para quem as escreveu, as mesmas notas vieram junto com um ganho de 4 casos, que também não alcança significância. O que a cruzada mostra é que o ganho medido na Fase 3 não acompanha a biblioteca quando muda quem a lê. Ela não separa se esse ganho é do par (o modelo com a biblioteca que ele mesmo escreveu) ou do leitor (o `qwen2.5:7b` poderia ganhar também com a biblioteca de outro), porque a direção inversa não rodou; e os dois Coder também não ganham mais que 1 caso de saldo com a própria biblioteca (b/c 0/0 e 3/2 no 7B, 1/0 e 1/0 no 3B, com L1 e L3).

## 6. O que a literatura previa e o que saiu

Fontes do mapa de decisões ([mapa-de-decisoes-fase-3.md](../2-pesquisa-e-literatura/mapa-de-decisoes-fase-3.md), §6.10) e dos levantamentos de 11/09 (§6.9.6), de 22/09 (§6.12) e de 29/09; referências completas em [referencias.md](../2-pesquisa-e-literatura/referencias.md).

| O que a literatura dizia | Fonte | O que a 3-B mediu | Leitura |
|---|---|---|---|
| Agentes nem sempre usam a experiência que escreveram: corromper ou trocar a memória por enchimento quase não muda o resultado | ZHAO, W. et al., 2026 (mapa, linha 17) | Trocar a biblioteca original pela do doador muda 6 acertos no 3B (de 0 a 1 entre corridas iguais) e 5 no Coder 7B (de 0 a 3 entre corridas iguais) | No 3B as notas são lidas e seguidas, para pior; no Coder 7B a troca cabe na variação entre corridas. A ablação do artigo (verbete corrompido, irrelevante, de enchimento) não foi rodada |
| O ganho da memória escrita pelo próprio modelo depende da competência de quem escreve, não de quem lê; modelos menores ganham pouco | SUZGUN et al., 2025 (mapa, linha 10; levantamento de 11/09, §6.9.6) | O 3B ganhou 1 caso com a própria biblioteca na Fase 3 e perdeu 4 de saldo com a biblioteca do modelo que mais acerta | Confirma a parte dos modelos menores. A perda com a biblioteca alheia aponta para o lado de quem lê, que a fonte não cobre; e o doador é o que mais acerta, não o que escreve as notas mais corretas (31,0% de edições corretas na revisão, contra 40,0% do 3B e 41,7% do Coder 7B) |
| Contexto recuperado com ruído derruba respostas que o modelo acertava sem ele, mais nos modelos menores | PANDEY, 2026 (linha 24) | O 3B perde 5 dos 26 casos que acertava com L0; o Coder 7B, 2 dos 29 | Mesmo sentido, tamanho bem menor que o relatado (quedas de dezenas de pontos) |
| Modelos adotam o conteúdo recuperado mesmo contra o que sabiam (mais de 60% dos casos); e, com memória, a maior parte dos erros acontece depois de a memória correta ter sido recuperada (61 a 62%) | WU; WU; ZOU, 2024 (linha 15); XIANG et al., 2026 (linha 16) | Em 4 das 5 perdas do 3B com a L1 o verbete de ouro estava no contexto | Falha de uso, não de recuperação; bate com a adesão cega de 95,6% do 3B a documentação errada na Fase 2-B |
| O desempenho de um formato de prompt se correlaciona fracamente entre modelos, e os melhores formatos não se transferem nem entre modelos da mesma família | SCLAR et al., 2024 (a correlação fraca); VORONOV et al., 2024 (a mesma família); levantamento de 22/09, §6.12 | A biblioteca do `qwen2.5:7b`, lida por dois modelos da mesma família Qwen2.5, não reproduz o ganho | Analogia, não previsão: as duas fontes tratam de formato de prompt, não de conteúdo de memória |
| Lições em linguagem natural se transferem entre tarefas (FEVER de 63% para 70% com lições aprendidas no HotpotQA); nessa medida as lições foram adaptadas por um modelo mais forte (GPT-4) e lidas por um mais fraco (GPT-3.5) | ZHAO, A. et al., 2024 (levantamento de 11/09, §6.9.6; afirmação parcial por causa dessa troca de modelo) | Com a tarefa igual e modelos locais de 3B e 7B lendo a biblioteca de outro, o ganho não foi detectado | É o precedente mais próximo de "um escreve, outro lê", e lá houve ganho; o porte dos modelos e o arranjo (adaptação, não escrita) impedem a comparação direta |
| Temperatura baixa não garante repetição; exige versão registrada e ponte | HE et al., 2025; BALTES et al., 2025 (linha 21) | Com a mesma entrada, de 0 a 3 casos em 36 mudam entre corridas iguais | Confirma; o achado 4.31 fica corrigido pelo 4.43 |
| Teste reutilizado infla o resultado; confirmar em casos inéditos | ZHU et al., 2025; KAPOOR et al., 2024 (riscos do mapa) | O ganho da L1 não reaparece nos inéditos | A ressalva era pertinente; a limitação 2 da análise decisória passa a ter medida |
| Amostra pequena não resolve; declarar o efeito mínimo antes do p | KOTAWALA, 2026; CARD et al., 2020 (linhas 5 e 6) | Com 72 casos o efeito mínimo cai para 13,9 pontos; o maior ganho é de 6,9 | Dobrar a amostra não bastou; o resultado segue direcional |
| A automelhoria sobe e depois regride; reportar o melhor ponto e o último | LIN, 2026 (linha 8) | Nos inéditos a L3 fica acima da L1 | O pico em L1 é dos 36 oficiais; em casos novos a ordem se inverte, dentro da variação |

**Lacuna declarada.** Nenhuma fonte das quatro rodadas mede diretamente uma biblioteca escrita por um modelo local pequeno e lida por outro. O precedente mais próximo é o ExpeL, na tabela acima, em modelos de API e com ganho. A troca cruzada fica como medida própria do trabalho, e o tema entra como candidato a uma busca dirigida se a banca pedir.

## 7. O que muda e o que não muda

- **A decisão 52 não muda.** Ela saiu da regra fixada antes da bateria, sobre a Fase 3 oficial. O Coder 7B, lendo a L1 do `qwen2.5:7b`, não alcança o `qwen2.5:7b` (83,3% contra 88,9%); era uma das duas condições que o comparativo qwen × Coder (§9) listava para rever a escolha. A outra, o Coder 7B nos casos inéditos, rodou em 06/10/2026 (§4.1): o Coder fica à frente nos 36 inéditos com L0 e L1 (saldo de 3 e 5 casos, p = 0,375 e 0,125) e atrás com L3; nos 72 casos com L1 o placar é 7/7. A condição fica parcialmente cumprida, dentro do ruído, e a revisão da decisão 52 é a ficha 21.
- **O padrão do agente é o modelo com a biblioteca que ele mesmo escreveu, e não a biblioteca como peça independente** (decisão 69). O ganho medido não acompanhou a biblioteca quando mudou quem a lê; trocar o modelo que lê exige medir de novo.
- **A biblioteca de partida da Fase 4 continua sendo a L1 curada** (decisão 60). O achado 4.37 deixou essa conta para a integração: com 72 casos, a L3 fica 2 casos à frente da L1, dentro da variação; a L1 já tem curadoria, hash conferido e cópia de produção, e a L3 exigiria revisar as edições das épocas 2 e 3. Não há evidência para trocar.
- **A cópia curada foi medida em 06/10/2026** (corrida 12, `resultados_alvo/pre_fase4_confianca/`, Ollama 0.34.4; relatório da Pré-Fase 4 §4.2, bloco `tb_conf_acerto`): com 23 das 40 edições (hash `1fca10f1a6f6`), o `qwen2.5:7b` acerta 80,6% nos 72 casos, contra 81,9% com a L1 inteira na mesma corrida (b/c 1/2, p = 1,00) e 73,6% com a biblioteca original (b/c 5/0); nos 36 inéditos fica 1 caso acima da L1. Custa menos por diagnóstico (61,1 s contra 70,5 s de mediana; 1132 contra 1315 tokens de prompt). A ficha 18 fecha e a L1 curada segue como ponto de partida da Fase 4 (decisão 71).
- **Para o plano da Fase 4**, quatro pontos saem daqui: (1) ponte de versão antes de toda medição, porque o Ollama se atualiza sozinho nesta máquina; (2) uma corrida por condição não basta para diferenças de até 3 casos, e os 72 casos (36 oficiais e 36 inéditos) passam a ser o conjunto de avaliação disponível; (3) nota anexada a verbete que aparece em quase metade dos contextos, como `contrato-produto`, alcança quase metade dos diagnósticos e pede revisão humana antes de entrar; (4) a medição da cópia curada como linha de base.

## 8. Limitações que ficam

1. Um doador e dois leitores, todos da família Qwen2.5; só as versões L1 e L3; 36 casos; uma corrida por condição. A direção inversa (o `qwen2.5:7b` lendo a biblioteca de outro modelo) não rodou, então a cruzada não separa o que é do par do que é do leitor.
2. O ganho do doador com a própria L1 (4 ganhos, 0 perdas) também não é significativo; toda a leitura é direcional.
3. Os pareamentos da cruzada contra a Fase 3 misturam versões do Ollama (0.34.0 e 0.34.4); para o Coder 7B eles não são pareáveis, e a leitura usa só a ponte.
4. Os inéditos rodaram em 0.34.1 e a cruzada em 0.34.4; as duas corridas não são comparadas entre si.
5. O caso `efe-3` mudou de texto em 28/09 e está nos 36; as comparações que cruzam essa data trazem a conta com ele e sem ele.
6. Os 36 casos inéditos e 30 das 40 avaliações da curadoria foram escritos por IA e conferidos contra o código; em 06/10/2026 o Eric conferiu os 6 casos de amostra e a planilha inteira (ficha 17) e não mudou nenhuma linha.
7. O mecanismo do 3B (§5) é leitura dos registros; não houve corrida que isolasse a nota de `contrato-produto`.
8. Os tempos por diagnóstico das corridas da 3-B foram medidos com a sessão de trabalho aberta e valem como ordem de grandeza; o custo por versão segue com a ressalva da análise decisória (limitação 4).
9. O Granite ficou fora de toda a 3-B por falta de memória (decisão 52).
10. As corridas de 06/10/2026 (§4.1, §4.2) têm uma corrida por condição; o `qwen2.5:7b` não tinha medida de A5 na Fase 2-B, então a comparação "biblioteca original contra própria" na adesão cega só existe para o 3B; e o Coder 7B nos inéditos rodou em outra versão do Ollama (0.34.4) que o `qwen2.5:7b` nos mesmos casos (0.34.1), com a ponte de 30/09 dizendo que o Coder 7B passou do limite de pareamento.

## 9. Fechamento das Fases 3 e 3-B

<!-- ! Alteração de IA - Revisar: (06/10/2026) linhas 6, 13, 18, 19 e 25 da tabela e a frase final da seção refeitas com as respostas do Eric às fichas 17 e 18; a limitação 6 do §8 também.
     ! Motivo: o Eric fechou a ficha 17 como (b), conferindo os 6 casos e a planilha sem mudar nada, e a 18 como (a), medindo a cópia curada na corrida 12 de 06/10; o texto dizia que as conferências esperavam por ele e que as duas corridas opcionais aguardavam decisão. -->

Todos os tópicos obrigatórios estão concluídos. A tabela diz o estado de cada um, a evidência e o que fica para depois.

| # | Tópico | Fase | Estado | Evidência | O que fica |
|---|---|---|---|---|---|
| 1 | Bateria oficial: 4 modelos, 3 épocas, 90 casos | 3 | Concluído | `resultados_alvo/fase3/`; relatório da Fase 3 §1 | Nada |
| 2 | Relatório por modelo, comparação entre fases e análise decisória | 3 | Concluído | Três documentos em `3-resultados-e-analises/`, tabelas por script com `--check` | Nada |
| 3 | Hipóteses H1 a H6 com veredito | 3 | Concluído | Achado 4.29; relatório da Fase 3 §2 | Os vereditos não mudam; para o `qwen2.5:7b`, H1 segue não confirmada com 72 casos (§4) |
| 4 | Decisão do modelo e da biblioteca | 3 | Concluído | Decisão 52; `decisao_modelo.md`; análise decisória §8 | Mantida depois da 3-B (§7); o que vai para a produção é a cópia curada, com as ressalvas do tópico 6 |
| 5 | Revisão das 63 edições aceitas | 3 | Concluído com ressalva | Relatório da Fase 3 §7; resumo regravado em 29/09 | Um revisor só, IA conferida contra o código, aceita pelo Eric em 23/09 |
| 6 | Curadoria da L1 e cópia de produção | 3 | Concluído com ressalva | `biblioteca_producao/` (hash `1fca10f1a6f6`); achado 4.40 | A cópia curada foi medida na corrida 12 de 06/10/2026 (ficha 18): rende como a L1 inteira (80,6% contra 81,9% nos 72; decisão 71); a planilha de 40 linhas foi conferida pelo Eric em 06/10 (ficha 17), sem mudança |
| 7 | Comparativo qwen × Coder | 3 | Concluído | `comparativo-qwen25-7b-vs-coder-7b.md`; achado 4.38 | A medida que falta nele é a corrida opcional do tópico 19 |
| 8 | Instalador com o modelo escolhido | 3 | Concluído | `install.py` baixa o `qwen2.5:7b` desde 23/09 | Nada |
| 9 | Pesquisa bibliográfica: quatro rodadas, mapa de decisões e mapa de filtros | 3 | Concluído | Levantamentos §6.9 a §6.13; `referencias.md` | Lacuna declarada: biblioteca escrita por um modelo local e lida por outro (§6) |
| 10 | Ponte de versão em Ollama 0.34.1 | 3-B | Concluído | §3 | O Granite ficou sem ponte, por falta de memória (decisão 52) |
| 11 | Ponte de versão em Ollama 0.34.4 | 3-B | Concluído com ressalva | §3; relatório da Fase 3 §11 | Coder 7B fora do limite; ponte nova a cada versão do Ollama |
| 12 | Correção dos casos `efe-3` e `efe-10` no banco | 3-B | Concluído com ressalva | Achado 4.36; decisão 58; ficha 13 | O `efe-3` está nos 36: as comparações com a Fase 3 trazem a conta com ele e sem ele |
| 13 | Casos inéditos | 3-B | Concluído | §4; achados 4.37 e 4.44 | Os 6 casos de amostra foram conferidos pelo Eric em 06/10/2026 (ficha 17), sem mudança |
| 14 | Troca cruzada | 3-B | Concluído | §5; achado 4.42 | A direção inversa não rodou (§8, limitação 1) |
| 15 | Sonda de detecção de correção | 3-B | Concluído | Roadmap §3; decisão 58 | O ciclo de correção é requisito da Fase 4 |
| 16 | Experimento do recuperador | 3-B | Concluído | Roadmap §2.2; decisão 61; achado 4.39 | Medir k = 5 na Fase 4 |
| 17 | Ablação base × instruct | 3-B | Concluído | Roadmap §2.2; achado 4.41 | Nada |
| 18 | Adesão cega sobre a L3 (corrida 5) | 3-B | Concluído | §4.2; análise decisória §10, item (c) | Rodou em 06/10/2026: a biblioteca própria não muda a adesão cega |
| 19 | Coder 7B nos 36 inéditos (corrida 7) | 3-B | Concluído | §4.1; comparativo qwen × Coder §9 | Rodou em 06/10/2026: o Coder fica à frente nos inéditos com L0 e L1, dentro do ruído; a decisão 52 é a ficha 21 |
| 20 | Granite com teto de texto maior | 3-B | Não rodado (inviável) | Decisão 52 (memória insuficiente); análise decisória §10, item (d) | A leitura "barrado pelo formato, não incapaz" (achado 4.30) continua hipótese não medida |
| 21 | Réplicas com temperatura alta | 3-B | Descartado | Plano complementar, item (e) | A variação entre corridas foi medida pelas pontes (achado 4.43) |
| 22 | Integração da 3-B na documentação e no painel | 3-B | Concluído | Este relatório; `decisao_modelo.md` §6; painel do projeto | Nada |
| 23 | Ferramental do Claude Code e das LLMs locais | Método | Concluído | `5-metodo-e-ferramental/` | Repetir a medição de tokens ao fim da Fase 4 |
| 24 | Projeto de pesquisa ABNT, modificações 1 a 8 | Documentação | Concluído | `correcoes-aplicadas.md` §5.2 | Item 10 e o PDF final sem as marcações, na entrega |
| 25 | Pendências em ficha (1 a 16) | Gestão | Concluído | `pendencias.md` | Fichas 17 e 18 abertas em 01/10 e fechadas em 06/10/2026 |

As fichas 17 e 18 foram respondidas em 06/10/2026, e as duas corridas opcionais rodaram no mesmo dia (§4.1 e §4.2). O que ainda depende só do Eric para o encerramento formal: a ficha 21 (o que fazer com a decisão 52 depois do Coder 7B nos inéditos), tirar os dois Coder do Ollama (nenhuma corrida restante os usa) e o commit.

## 10. Rastreabilidade

| Número | Onde nasce | Como conferir |
|---|---|---|
| Pontes, variação entre corridas, inéditos somados, troca cruzada | `resultados_alvo/fase3/analise_fase3b.json` e `.md` | `RESULTADOS_DIR=resultados_alvo python analisar_fase3b.py --check` (confere também os blocos deste relatório) |
| Pareamento de cada saída da 3-B contra a mesma versão na Fase 3 | `decisao_modelo.md` §6 | `python decidir_modelo.py --saida fase3 --saidas-3b fase3b_ponte fase3b_ponte_0344 fase3b_cruzada_qwen --check` |
| Avaliação de cada corrida | `resultados_alvo/<saida>/resumo_fase3.json` | `python avaliar_fase3b.py --saida <saida>` |
| Edições de `contrato-produto` e cópia curada | `resultados_alvo/fase3/curadoria_L1__qwen2.5_7b.md`; `biblioteca_producao/curadoria.json` | `python curar_biblioteca.py --listar` |
| Testes do script de análise | `testar_fase3b.py` (seção 9) | `python testar_fase3b.py` |
