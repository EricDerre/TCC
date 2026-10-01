<!-- ! Alteração de IA - Revisar: guia novo (30/09/2026) para a leitura dirigida do livro-texto (FACELI et al., 3. ed., 2025) na plataforma Minha Biblioteca: o que pode ser feito com o e-book, o roteiro de capítulos por uso no TCC, o modelo de ficha com página e o fluxo de integração das citações no Memorial e no projeto ABNT.
     ! Motivo: o Eric tem acesso legítimo ao e-book e pediu para "varrer todas as informações do livro" para citações e conhecimento; o caminho correto (e o único legal) é a leitura com anotações e citações curtas com página, não a cópia do livro. O roteiro parte do mapa de capítulos que a pesquisa da Fase 3 já fez (§6.10.4). -->
# Guia de leitura do livro-texto (Faceli et al., 3. ed., 2025)

**Obra:** FACELI, K.; LORENA, A. C.; GAMA, J.; ALMEIDA, T. A.; CARVALHO, A. C. P. L. F. *Inteligência Artificial: uma abordagem de aprendizado de máquina*. 3. ed. Rio de Janeiro: LTC, 2025. E-book ISBN 978-85-216-3921-3, acessado pela Minha Biblioteca (assinatura do Eric); exemplar físico com o Eric desde 30/09/2026.

## 1. O que pode ser feito com o e-book

- **Pode:** ler; marcar e anotar dentro da plataforma; copiar trechos curtos para citação (a plataforma limita a cópia e acrescenta a referência sozinha); exportar as **próprias** notas e destaques; escrever fichamento com as ideias em palavras nossas, sempre com o número da página.
- **Não pode:** baixar ou copiar o livro inteiro, contornar a proteção da plataforma, ou versionar trechos longos no repositório. A Lei 9.610/1998 permite a citação de passagens para estudo e crítica, com autor, obra e página; é exatamente o que o TCC precisa.
- **O que entra no repositório:** este guia, a ficha de leitura (notas nossas e citações curtas com página) e as citações incorporadas ao Memorial e ao projeto ABNT. Nada do texto integral.

## 2. Roteiro de capítulos, por uso no TCC

Os números de capítulo vêm do sumário da 3. ed. usado no mapa de decisões (§6.10.4); quem ler confere no e-book e corrige aqui se algum número mudou.

| Ordem | Capítulo | O que procurar | Onde entra no TCC |
|---|---|---|---|
| 1 | **Cap. 10, Avaliação de modelos preditivos** | Partição treino/teste e holdout; matriz de confusão; acurácia, precisão, revocação, F1 e as médias macro e micro em multiclasse; acurácia balanceada, se aparecer; intervalos de confiança; testes para comparar classificadores (McNemar, t pareado, Wilcoxon); o alerta contra decidir por um único número | Decisão 36 (regra pré-registrada: acurácia balanceada nos 36) e decisão 52; relatório da Fase 3 §2 a §5; análise decisória; ABNT §3.4 (critérios) e §2.2 |
| 2 | **Cap. 4, Métodos baseados em distâncias** | Aprendizado baseado em instâncias, k-NN, medidas de similaridade e o custo de buscar vizinhos; o papel da representação | Recuperador BM25 como busca por vizinhos entre verbetes (§6.3 do Memorial); decisão 61 (híbrido descartado) |
| 3 | **Cap. 19, Textos** | Pré-processamento de texto, saco de palavras, TF-IDF, representações vetoriais (embeddings), classificação de texto | Experimento do recuperador (por que os sinais em código vencem o embedding neste corpus); classe "tradução"; tokenização (§6.7) |
| 4 | **Cap. 7, Métodos conexionistas** e **Parte V, Tendências e perspectivas** | Redes profundas, representação aprendida, transformadores, ajuste fino e o que a 3. ed. diz sobre modelos de linguagem | Referencial teórico do TCC final (ficha 10, item 10); ABNT §2.2; contexto dos modelos locais (§6.1) |
| 5 | **Cap. 16, Dados dinâmicos** e **Cap. 3, Pré-processamento de dados** | Fluxos de dados, deriva de conceito, atualização incremental; limpeza, seleção e redução de dados | A biblioteca gerida pelo modelo como fluxo com deriva (§6.6); curadoria da L1 e filtros da Fase 4 (decisão 65) |
| 6 | **Cap. 1, Introdução** | Definições de aprendizado de máquina, tipos de aprendizado, viés indutivo, o ciclo de um projeto de AM | Vocabulário do texto final em português; abertura do capítulo teórico |
| 7 | **Cap. 15, Avaliação de modelos descritivos** | Índices de validação de agrupamentos | Só se a análise agrupar erros por classe de defeito; leitura opcional |

O que o livro **não** cobre, e continua vindo dos artigos do levantamento: agentes com modelos de linguagem, recuperação para geração (RAG), testes de software com self-healing, deriva de contrato. O livro é a espinha teórica de aprendizado de máquina e de avaliação, não a fonte das afirmações específicas do projeto.

## 3. Modelo de ficha (uma por trecho)

```
Capítulo e seção: 10.3 (exemplo)
Página(s): 000
Citação curta (até três linhas, entre aspas, exatamente como no livro):
Em palavras nossas (o que o trecho diz e por que importa):
Onde entra: decisão 36 / relatório Fase 3 §4 / ABNT §3.4 (escolher)
Forma da citação no texto: (FACELI et al., 2025, p. 000)
```

A ficha consolidada fica em `fichamento-faceli-3ed.md`, nesta pasta, uma seção por capítulo, na ordem do roteiro.

## 4. Fluxo

1. **Ler e marcar na plataforma** (Eric, ou o integrante que ficar com o capítulo): destacar os trechos e anotar a página; a ferramenta de notas da plataforma guarda tudo.
2. **Exportar as notas** (função de exportar ou imprimir o caderno de notas e destaques, se a plataforma oferecer; senão, copiar os destaques curtos para a ficha à mão). O que se exporta são as nossas anotações, não o livro.
3. **Consolidar** (Claude): converter as notas na ficha por capítulo, conferir a forma ABNT de cada citação, e integrar: citações com página no Memorial (relatório da Fase 3, análise decisória, §6.x) e no projeto ABNT (§2.2, §3.4), referência já existente na lista.
4. **Registrar**: linha no índice do Memorial, decisão numerada se algum critério do TCC mudar por causa da leitura, e a aba Pesquisa do painel passa a citar a ficha.

**Divisão sugerida entre os sete integrantes:** capítulos 10 e 4 com o Eric (são os que sustentam a decisão do modelo); um capítulo do roteiro para cada um dos demais, com a ficha preenchida no modelo acima. Uma semana de leitura cobre o roteiro inteiro.

## 5. O que o livro acrescenta ao trabalho

- **Base normativa para o desenho de avaliação.** A partição 54/36, a acurácia balanceada, o McNemar pareado e o bootstrap deixam de ser escolhas nossas e passam a ser o instrumental recomendado pelo livro-texto da área, citado com página. É o que a banca vai reconhecer primeiro.
- **Vocabulário em português.** Termos como acurácia balanceada, validação, deriva de conceito, aprendizado baseado em instâncias e representação vetorial ganham a forma consagrada no livro; o texto final fica uniforme.
- **Enquadramento teórico da biblioteca gerida pelo modelo.** O capítulo de dados dinâmicos dá o nome do fenômeno que a Fase 3 mediu (deriva) e justifica a curadoria e os filtros da Fase 4.
- **Justificativa do recuperador.** Os capítulos de distâncias e de textos explicam por que a busca lexical com sinais extraídos por código vence o embedding num corpus pequeno e técnico, o que hoje está registrado só como medida (decisão 61).
- **Referencial do TCC final.** O capítulo conexionista e a parte de tendências dão o pano de fundo dos modelos de linguagem em português, com autores brasileiros de referência (Prêmio Jabuti), o que fecha o item 10 da ficha 10.
- **Material de demonstração.** Os notebooks de apoio (na máquina, fora do git) servem para ilustrar matriz de confusão e validação na defesa, se for útil.
