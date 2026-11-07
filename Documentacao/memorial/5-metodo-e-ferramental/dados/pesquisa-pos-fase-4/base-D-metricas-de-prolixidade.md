<!-- ! Alteração de IA - Revisar: arquivo novo (07/11/2026): leitura feita por um subagente do Claude (modelo Sonnet) sobre métricas de prolixidade e objetividade para os filtros determinísticos, na rodada 6 da pesquisa (Pós-Fase 4); é um arquivo de dados que ferramentas/integrar_pesquisa_pos_fase4.py lê para montar o levantamento §6.15, e o integrador tira este comentário do texto que entra lá.
     ! Motivo: o Eric pediu em 07/11/2026 a base de pesquisa de cada ponto da Pós-Fase 4 e a validação de oito repositórios do GitHub; a leitura fica versionada como dado para o levantamento ser regerado por script e conferido pelo --check. O texto é o que o subagente escreveu, sem edição, com a marca de confiança que ele deu a cada fonte (aberta e lida; só o resumo de busca; de memória). -->
# Base D: métricas de prolixidade e objetividade (pesquisa de 7 nov. 2026)

Legenda de confiança: [ABERTA] = abri a página e li o trecho citado; [PARCIAL] = abri, mas só parte foi legível; [SECUNDÁRIA] = o número vem de um texto que cita a fonte.

## a) Legibilidade em português

### 1. Martins et al. (1996), adaptação do Flesch  [PARCIAL]

MARTINS, Teresa B. F.; GHIRALDELO, Claudete M.; NUNES, M. das Graças V.; OLIVEIRA JR., Osvaldo N. **Readability formulas applied to textbooks in Brazilian Portuguese**. São Carlos: ICMSC-USP, 1996. (Notas do ICMSC, n. 28). Disponível em: https://repositorio.usp.br/item/000906089. Acesso em: 7 nov. 2026.

- O PDF do repositório é imagem digitalizada, sem camada de texto: não consegui ler a fórmula nele. O que está confirmado é o resumo do repositório e as citações: 120 trechos de livros didáticos, quatro níveis de leitura que seguem as etapas do ensino brasileiro, e os escores de Flesch saem sistematicamente mais baixos em português do que em inglês (palavras com mais sílabas). Um texto que cita o trabalho diz que foram somados 42 pontos aos escores (206,835 + 42 = 248,835).
- Aplicação: é a única fonte primária da adaptação; a fórmula em si tem de vir de 2 (que a transcreve) e a conferência no original fica pendente de OCR.

### 2. NILC-Metrix (Leal et al., 2023)  [ABERTA]

LEAL, Sidney Evaldo et al. **NILC-Metrix: assessing the complexity of written and spoken language in Brazilian Portuguese**. Language Resources and Evaluation, v. 58, 2023. DOI 10.1007/s10579-023-09693-w. Disponível em: https://arxiv.org/abs/2201.03445. Acesso em: 7 nov. 2026.

- Reúne 200 métricas de complexidade textual para o português do Brasil (código em github.com/nilc-nlp/nilcmetrix, AGPLv3). No texto do PDF, a fórmula adaptada vem escrita assim: **Flesch = 248,835 - 1,015 x (palavras por frase) - 84,6 x (sílabas por palavra)**. Traz também o índice Brunet-like de palavras desconhecidas: 0,1579 x (% de palavras fora do Dicionário de Palavras Simples, Biderman 1998) + 0,0496 x (palavras por frase) + 3,6365.
- Aplicação: dá a fórmula do Flesch em português e uma lista pronta de métricas (comprimento de frase, sílabas, palavras raras) que o filtro pode reproduzir em Python puro; a contagem de sílabas em português precisa de regra própria (separação silábica por vogais/ditongos), a testar contra o NILC-Metrix em amostra.

### 3. Faixas do índice  [SECUNDÁRIA, duas fontes que não batem entre si]

- Dissertação PUC-Rio (Maxwell, arquivo 23892_7.PDF, capítulo 6), citando Martins et al. (1996): quatro faixas. 75 a 100 muito fácil (até a 4a série do fundamental); 50 a 75 fácil (até a 8a série); 25 a 50 difícil (ensino médio ou superior); 0 a 25 muito difícil (áreas acadêmicas específicas). Atenção: essa dissertação escreve a constante como 164,835, o que destoa de 248,835 do NILC; tratar como erro de transcrição dela. Disponível em: https://www.maxwell.vrac.puc-rio.br/23892/23892_7.PDF. Acesso em: 7 nov. 2026.
- RODRIGUES; NETO. Signo, Santa Cruz do Sul, v. 36, n. 60, p. 50-60, 2011, tabela da fórmula original de Flesch (206,835), com a tradução de Goldim (2003): 90-100 muito fácil, 80-90 fácil, 70-80 razoavelmente fácil, 60-70 padrão, 50-60 razoavelmente difícil, 40-50 difícil, 0-30 muito difícil. Essa tabela é da fórmula sem os 42 pontos, então não vale para a adaptada. Disponível em: https://seer.unisc.br/index.php/signo/article/view/1421/1607. Acesso em: 7 nov. 2026.
- Aplicação: para a fórmula adaptada, a referência é a tabela de quatro faixas; relatório para analista de QA deve ficar em 50 ou mais (nível "fácil"), o que é uma escolha nossa apoiada na faixa, não um valor da fonte. Flesch mede só frase e sílaba, a própria literatura chama de superficial; serve como alarme, não como nota.

## b) Prolixidade e viés de tamanho em modelos

### 4. Zheng et al. (2023), MT-Bench e Chatbot Arena  [ABERTA]

ZHENG, Lianmin et al. **Judging LLM-as-a-judge with MT-Bench and Chatbot Arena**. arXiv:2306.05685, 2023. Disponível em: https://arxiv.org/abs/2306.05685. Acesso em: 7 nov. 2026.

- Seção 3.3, ataque da "lista repetitiva": em 23 respostas com lista numerada, os autores inseriram no início uma cópia reescrita da lista, sem informação nova. O juiz falhou (preferiu a resposta inflada) em 91,3% dos casos com Claude-v1 e com GPT-3.5, e em 8,7% com GPT-4. Juízes com mais de 80% de concordância com humanos ainda caem em texto mais longo.
- Aplicação: justifica filtro determinístico de tamanho: um modelo julgando o próprio verbete não é confiável contra enchimento; a medida precisa vir de código.

### 5. Dubois et al. (2024), AlpacaEval com controle de tamanho  [ABERTA]

DUBOIS, Yann; GALAMBOSI, Balázs; LIANG, Percy; HASHIMOTO, Tatsunori B. **Length-Controlled AlpacaEval: a simple way to debias automatic evaluators**. arXiv:2404.04475, 2024. Disponível em: https://arxiv.org/abs/2404.04475. Acesso em: 7 nov. 2026.

- Ajusta um modelo linear generalizado que prevê a preferência do juiz a partir da diferença de tamanho e de outros traços, e recalcula a preferência supondo diferença de tamanho zero. A correlação de Spearman com o Chatbot Arena sobe de 0,94 para 0,98.
- Aplicação: o tamanho é um confundidor medido em código; ao comparar verbetes, comparar a densidade (informação por palavra) e não o tamanho bruto, ou fixar o tamanho como covariável.

### 6. Zhang, Das e Zhang (2024), compensação por verbosidade  [ABERTA]

ZHANG, Yusen; DAS, Sarkar Snigdha Sarathi; ZHANG, Rui. **Verbosity does not equal veracity: demystify verbosity compensation behavior of large language models**. arXiv:2411.07858, 2024 (v2). Disponível em: https://arxiv.org/abs/2411.07858. Acesso em: 7 nov. 2026.

- Define resposta verbosa como aquela que pode ser comprimida em menos tokens com o mesmo sentido (repete a pergunta, enumera demais, hesita). Em 14 modelos e 5 bases, a frequência é de 50,40% no GPT-4; na base Qasper, respostas verbosas e concisas diferem 27,61% em desempenho; um algoritmo em cascata baixou o Mistral de 63,81% para 16,16%. Verbosas têm mais incerteza. É preprint no arXiv (a versão em evento UncertaiNLP 2025 foi só vista na busca).
- Aplicação: sustenta duas medidas por código, a frequência (parcela de textos acima de um teto) e o achado de que texto verboso anda junto com incerteza do modelo, o que casa com o nó de diagnóstico.

### 7. Adams et al. (2023), Chain of Density  [ABERTA]

ADAMS, Griffin et al. **From sparse to dense: GPT-4 summarization with Chain of Density prompting**. arXiv:2309.04269, 2023. Disponível em: https://arxiv.org/abs/2309.04269. Acesso em: 7 nov. 2026.

- Resumos "centrados em entidades", cada vez mais densos sem ficar mais longos; estudo de preferência humana em 100 artigos do CNN/DailyMail. A página aberta não define a densidade; no corpo do artigo ela é entidades por token, a conferir lendo o PDF.
- Aplicação: base para uma densidade calculável (entidades do domínio por palavra), com a lista fechada de nomes do projeto no lugar do reconhecedor de entidades.

## c) Linguagem simples como norma

### 8. Lei n. 15.263, de 14 de novembro de 2025  [ABERTA]

BRASIL. **Lei n. 15.263, de 14 de novembro de 2025**. Institui a Política Nacional de Linguagem Simples nos órgãos e entidades da administração pública. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15263.htm. Acesso em: 7 nov. 2026.

- Art. 4: linguagem simples é "conjunto de técnicas destinadas à transmissão clara e objetiva de informações". Art. 5: frases curtas e em ordem direta, voz ativa, evitar intercaladas, uma ideia por parágrafo, palavras comuns (jargão trocado ou explicado), nome completo antes da sigla, informação mais importante primeiro, listas e tabelas quando couber, evitar redundância, testar com o público-alvo.
- Aplicação: é a norma brasileira oficial e vale como lista de regras verificáveis em código (frase curta, sigla sem expansão, redundância); não traz número de palavras por frase, o limiar tem de vir de outra fonte.

### 9. ISO 24495-1:2023, Plain language  [PARCIAL]

ISO. **ISO 24495-1:2023: Plain language, part 1: governing principles and guidelines**. Genebra: ISO, 2023. Disponível em: https://www.iso.org/standard/78907.html (a página da ISO devolveu 403; li a ficha em https://accessible-eu-centre.ec.europa.eu/content-corner/digital-library/iso-24495-12023-plain-language-part-1-governing-principles-and-guidelines_en). Acesso em: 7 nov. 2026.

- Publicada em 1 jun. 2023, 14 páginas, comitê ISO/TC 37. Vale para textos de qualquer língua escrita, com exemplos só em inglês, e cobre também redação técnica. Os princípios e diretrizes em si estão na parte paga; a ficha não os lista, e não vi número de palavras por frase.
- Aplicação: serve de ancoragem internacional para a regra "o leitor acha, entende e usa"; não fornece limiar.

## d) Orientação para comentários e textos técnicos

### 10. Google Python Style Guide, seção 3.8.5  [ABERTA]

GOOGLE. **Google Python Style Guide**: block and inline comments. Disponível em: https://google.github.io/styleguide/pyguide.html. Acesso em: 7 nov. 2026.

- Regra: comentar as partes complicadas ("se você vai ter de explicar na revisão de código, comente agora") e "nunca descreva o código", supondo que o leitor sabe Python melhor que você, mas não sabe o que você quer fazer.
- Aplicação: é a regra de estilo do projeto em uma linha; vira filtro de "frase que só repete o que o código/campo já mostra".

### 11. Google Developer Documentation Style Guide, tom  [ABERTA]

GOOGLE. **Google developer documentation style guide: tone and content**. Disponível em: https://developers.google.com/style/tone. Acesso em: 7 nov. 2026.

- Regras: dizer a informação útil de forma direta; cortar marcadores vazios como "please note" e "at this time"; não chamar passo de "simples" ou "fácil"; palavras simples no lugar de jargão e metáfora; frases curtas; variar o início das frases.
- Aplicação: dá a lista de palavras de preenchimento e de adjetivos de enfeite (versão em português: "vale ressaltar", "neste momento", "simplesmente", "basicamente").

## e) Métricas calculáveis sem modelo e de onde sai cada uma

| Métrica | Como calcular | Fonte |
|---|---|---|
| Palavras por frase (média e máximo) | contar palavras / frases | NILC-Metrix (2); Lei 15.263 art. 5 (frases curtas); Google tom (11) |
| Flesch adaptado | 248,835 - 1,015 x palavras/frase - 84,6 x sílabas/palavra | NILC-Metrix (2), Martins (1) |
| Taxa de compressão | palavras do texto / palavras do resumo que o conteúdo pede (ex.: número de campos que mudaram) | definição de verboso como "comprimível" em Zhang (6); a escolha do denominador é nossa |
| Razão de preenchimento | palavras da lista fechada de enchimento / palavras | Google tom (11); Zhang (6): repete pergunta, hesita |
| Repetição interna | trechos repetidos (n-gramas de 3 palavras que reaparecem) / total | ataque da lista repetitiva em Zheng (4) |
| Densidade | termos do domínio da lista fechada (campos, tabelas, códigos) / palavras | Adams (7), adaptado a lista fechada |
| Jargão por lista fechada | termos da lista do projeto sem expansão na primeira menção / termos | Lei 15.263 art. 5 (jargão trocado ou explicado, sigla com nome completo) |
| Tamanho absoluto em palavras | contagem; usar como covariável, não como nota | Dubois (5), Zheng (4) |

## O que isso fixa para o desenho

Entram nos filtros, nesta ordem de confiança: (1) palavras por frase, com teto de 20 de média e 30 no máximo por frase (o teto vem do nosso corpus de comentários bons, medido por script, e não de uma fonte: nem a Lei 15.263 nem o ISO dão número; só a regra "frases curtas" está na lei); (2) Flesch adaptado de 50 ou mais, que é a fronteira entre "fácil" e "difícil" na tabela de quatro faixas de Martins citada pela dissertação da PUC-Rio, usado só como alarme porque a literatura chama o índice de superficial e as duas fontes secundárias divergem na constante; (3) razão de preenchimento por lista fechada, com a lista tirada das regras do guia do Google (11) e traduzida; limiar a calibrar como o percentil 95 do corpus de referência; (4) repetição interna, justificada pelo ataque da lista repetitiva (4), onde juízes caíram em 91,3% dos casos, e pelo conceito de verbosidade como "comprimível" (6); (5) taxa de compressão contra o resumo que o conteúdo pede, onde o denominador (campos que mudaram, rótulo, uma frase de causa) é decisão de desenho; (6) jargão e sigla sem expansão por lista fechada (Lei 15.263 art. 5). Como o tamanho infla a nota de qualquer juiz-modelo (4, 5), o tamanho em palavras entra nas tabelas como covariável e nunca como critério de aprovação; comparações entre verbetes usam densidade, não tamanho. A regra "nunca descreva o código" (10) vira a verificação de que a frase cita um fato do caso (campo, tabela, valor) e não repete o rótulo.

## O que não achei

Não li a fórmula direto no original de Martins et al. (1996): o PDF é imagem sem texto, a fórmula veio do NILC-Metrix (2) e as faixas, de uma dissertação, que escreve a constante errada. Não achei nenhuma fonte primária com limiar numérico de palavras por frase para português (a Lei 15.263 e o ISO 24495-1 só dão a regra qualitativa; os princípios do ISO estão na parte paga). Não achei limiar publicado de razão de preenchimento nem de taxa de compressão: o que existe é a definição de verbosidade de Zhang (6), então esses dois limiares são calibração nossa e devem ser declarados assim. Não encontrei métrica de densidade de informação validada para o português; a de Adams (7) é para inglês e a definição exata no artigo não foi confirmada pela página do resumo. Não achei padrão ABNT de linguagem simples (só a lei federal e o ISO). Não confirmei o guia oficial de comentários para a regra de tamanho de docstring além da seção 3.8.5.
