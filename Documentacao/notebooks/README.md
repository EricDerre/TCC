[//]:=======================================================================================
# Inteligência Artificial: Uma Abordagem de Aprendizado de Máquina - 2a Edição
--------------------------------------------------------------------------------------------

### Katti Faceli; Ana C. Lorena; João Gama;  Tiago A. Almeida; André C. P. L. F. de Carvalho
[//]:=======================================================================================



## Descrição dos notebooks
-----------------------

  **Autores: Renato Moraes Silva e Pedro Reis Pires**
  -----------------------------------------------

  **Descrição geral:**
  ---------------
     Este diretório contém uma lista de notebooks em Python3 para ajudar o leitor a exercitar de maneira prática os
     conceitos apresentados no livro. 

  **Instalação de Python3:**
  ----------------------
     A primeira etapa para visualização dos notebooks é a instalação de Python3, a linguagem de programação nos quais os
     mesmos foram implementados.
     Na grande maioria das distribuições Linux e em máquinas com Mac OS X, a linguagem se encontra pré-instalada. Para
     determinadas distribuições Linux, ou para Windows, a instalação se fará necessária.
     Uma maneira bastante prática e recomendada de instalar Python e outros recursos que serão utilizados é através da 
     distribuição Anaconda, que pode ser encontrada no seguinte link: https://www.anaconda.com/products/individual#Downloads.
     É possível também instalar a linguagem através de instaladores disponibilizados em seu site oficial: 
     https://www.python.org/downloads/. 
     
  **Instalação do Jupyter Notebook:**
  -------------------------------
     Para visualizar os notebooks, é necessário a instalação do Jupyter Notebook: uma aplicação web open-source para
     implementação e execução de código de forma interativa.
     O Jupyter é instalado de forma automática junto com a instalação da distribuição Anaconda. Ainda assim, é possível 
     instalar o Jupyter Notebook através do gerenciador de pacotes PyPI (Python Package Index), usando os comando: 
     pip3 install jupyter. 
     Com o Jupyter instalado, ele pode ser aberto por meio de um terminal através do comando: jupyter notebook. Mais 
     informações sobre como instalar e usar o Jupyter, podem ser encontradas no site oficial: https://jupyter.org.

  **Instalação das bibliotecas da linguagem:**
  ----------------------------------------
     Ao longo dos 7 notebooks, serão utilizadas diversas bibliotecas de Python que não fazem parte de sua biblioteca 
     padrão. Dessa forma, é necessário instalá-las. 
     Através da instalação do Jupyter Notebook, é possível que muitas destas bibliotecas sejam instaladas em conjunto,
     Entretanto é importante verificar se elas encontram-se atualizadas, visto que muitos recursos utilizados nos notebooks
     são referentes a versões específicas (informadas nos próprios notebooks).
     Todas as bibliotecas necessárias podem ser instaladas por meio da distribuição Anaconda ou pelo PyPI. São elas:
     
     scipy: https://anaconda.org/anaconda/scipy (Anaconda) | https://pypi.org/project/scipy/ (PyPI)
     numpy: https://anaconda.org/anaconda/numpy (Anaconda) | https://pypi.org/project/numpy/ (PyPI)
     pandas: https://anaconda.org/anaconda/pandas (Anaconda) | https://pypi.org/project/pandas/ (PyPI)
     matplotlib: https://anaconda.org/conda-forge/matplotlib (Anaconda) | https://pypi.org/project/matplotlib/ (PyPI)
     seaborn: https://anaconda.org/anaconda/seaborn (Anaconda) | https://pypi.org/project/seaborn/ (PyPI)
     scikit-learn: https://anaconda.org/anaconda/scikit-learn (Anaconda) | https://pypi.org/project/scikit-learn/ (PyPI)
     nltk: https://anaconda.org/anaconda/nltk (Anaconda) | https://pypi.org/project/nltk/ (PyPI)
     wordcloud: https://anaconda.org/conda-forge/wordcloud (Anaconda) | https://pypi.org/project/wordcloud/ (PyPI)


  **Lista de Notebooks:**
  -------------------

     1 - Análise e preparação dos Dados

          - Este notebook faz referência aos conceitos apresentados nos Capítulos 2 (Análise de Dados) e 
	    3 (Pré-processamento de Dados). Ele aborda as principais etapas para análise, interpretação e 
	    preparação dos dados para os métodos de aprendizado de máquina. É abordado como fazer a eliminação 
	    de atributos irrelevantes e o tratamento de valores faltantes. Também, é mostrado como tratar valores 
	    redundantes ou inconsistentes e como fazer a normalização dos dados. Depois, é feita a detecção e 
	    remoção de outliers da base dados. Por fim, é mostrado como fazer a análise da distribuição das classes 
	    e da correlação entre os atributos. 

     2 - Métodos baseados em vizinhança - k-vizinhos mais próximos

          - Este notebook faz referência aos conceitos apresentados no 4 (Métodos baseados em vizinhança). 
        Ele aborda o algoritmo de $k$-vizinhos mais próximos (KNN), técnica de aprendizado de máquina que 
        se utiliza do conceito de distância entre amostras para predizer a classe de uma amostra nova. 
        Inicialmente, foi apresentada a técnica de normalização dos dados, de forma a se evitar problemas de escala 
        dos dados que podem afetar negativamente o KNN. Em seguida, foi implementado o classificador utilizando distância euclidiana. 
        Finalmente, foram apresentadas variações do KNN utilizando a biblioteca ```scikit-learn``, aplicando outras funções de distância, 
        seleção de classe e armazenamento dos dados.

     3 - Métodos probabilíticos

           - Este notebook se refere ao Capítulo 5 (Métodos probabilísticos).
            Ele apresenta diferentes variações do classificador naive Bayes e suas aplicações em duas bases de dados 
            distintas. Utilizamos o naive Bayes Multinomial e Bernoulli para lidar com os atributos categórico, enquanto 
            o naive Bayes Gaussiano foi aplicado em dados com atributos contínuos. Foi demonstrada a adequação de cada 
            método conforme o tipo de dado, além de avaliar o desempenho de cada classificador nas respectivas tarefas 
            de classificação, ilustrando suas características em diferentes cenários.

     4 - Regressão logística

           - Este notebook se refere ao Capítulo 5 (Métodos probabilísticos).
             Ele exlorou o comportamento da regressão logística em diferentes cenários de dados, observando como o parâmetro 
             de regularização influencia o desempenho do modelo. Inicialmente, a regressão logística foi aplicada a uma base 
             de dados linearmente separável. Depois, o método foi aplicado em dados não separáveis linearmente, utilizando atributos 
             polinomiais para transformar o espaço de entrada. Nesse cenário mais complexo, foi mostrado como o ajuste cuidadoso do parâmetro de 
             regularização tornou-se ainda mais importante, uma vez que um valor inadequado pode resultar em underfitting ou overfitting.

     5 - Árvores de Decisão

           - Este notebook se refere ao Capítulo 6 (Métodos Simbólicos).
            Ele apresenta o algoritmo de Árvores de Decisão, tradicional técnica do aprendizado de máquina que tem como 
            principal vantagem a sua explicabilidade. O método opera através da construção de uma árvore, cujos nós 
            correspondem a regras de decisão aprendidas através da análise dos dados e as folhas correspondem ao valor 
            de predição. Foi mostrado como o método pode ser aplicado através da biblioteca scikit-learn para problemas 
            de classificação e regressão.

     6 - Métodos Conexionistas

           - Este notebook se refere ao Capítulo 7 (Métodos Conexionistas).
             Ele apresenta as principais etapas do processo de classificação de dígitos numéricos usando a rede neural MLP. 
             Foi explorada uma arquitetura clássica de MLP, utilizando a função de ativação sigmoidal, uma das mais 
             tradicionais, e uma única camada intermediária. Também foram mostradas algumas configurações adicionais, como 
             o uso da função de ativação ReLU, bastante adotada nas camadas intermediárias de modelos modernos, e da função 
             softmax na camada de saída para a classificação de múltiplas classes. Também foi incluída a técnica de dropout
             e da função de otimização Adam.

     7 - Métodos de maximização das margens

           - Este notebook se refere ao Capítulo 8 (Métodos de maximização de margens).
             Ele apresenta uma análise do desempenho do método de máquinas de vetores de suporte (SVM) em diferentes contextos, 
             começando com dados separáveis linearmente  utilizando um kernel linear. Observamos o impacto da regularização no 
             limite de decisão do modelo. Em seguida, exploramos amostras não separáveis linearmente com o kernel radial, mostrando 
             como esses parâmetros afetam o limite de decisão. Por fim, realizou-se uma busca em grade na base de dados Seeds para 
             otimizar simultaneamente o kernel, custo e gamma. Essa abordagem sistemática ressaltou a importância de selecionar 
             adequadamente os hiperparâmetros para maximizar o desempenho do SVM.

     8 - Modelos Múltiplos em Classificação

           - Este notebook se refere aos Capítulos 6 (Métodos Simbólicos) e 9 (Modelos Múltiplos Preditivos).
             Ele aborda os modelos múltiplos de classificação, também conhecidos como métodos ensemble. 
             Esses modelos fazem a combinação de classificadores para obterem melhor desempenho. 
             Mais especificamente, é usado o método de floresta aleatória (RF - Random Forest) que faz a
             combinação de árvores de decisão. Os resultados desse método são comparados com o resultado de
             uma árvore de decisão.

     9 - Algoritmos e validação de Classificadores 

           - Este notebook se refere aos Capítulos 4 (Métodos Baseados em Distâncias), 5 (Métodos Probabilísticos), 
             6 (Métodos Simbólicos), 8 (Métodos de Maximização de Margens) e 10 (Avaliação de Modelos Preditivos).
             Ele aborda os conceitos de metodologia experimental e análise de desempenho. Para isso, inicialmente, 
             é empregado o método do K-vizinhos mais próximos (K-nearest neighbors - KNN) para comparar 
             o desempenho usando holdout (treino, validação e teste) e validação cruzada k-fold, com medidas de 
             acurácia,  precisão, revocação e F-medida. Adicionalmente, é implementada uma busca em grade para 
             encontrar o melhor número de vizinhos. Depois, é comparado o desempenho de vários métodos de 
             classificação.

     10 - Algoritmos e validação em Agrupamento
          
            - Este notebook se refere aos Capítulos 12 (Análise de Agrupamentos), 13 (Algoritmos de Agrupamento) 
              e 15 (Avaliação de Modelos Descritivos).
              Nele, são aplicados diferentes algoritmos de agrupamento, cada qual com sua abordagem para agrupar 
              os dados, sobre três conjuntos de dados com características diferentes. Após a execução das técnicas, 
              é realizada uma avaliação dos resultados obtidos. Dessa forma, é possível acompanhar um processo 
              simples de agrupamento de dados e análise das partições obtidas.

     11 - Métodos de agrupamento - K-médias
          
            - Este notebook se refere ao Capítulo 12 (Análise de Agrupamentos).
              Ele analisou o comportamento do K-médias em diferentes configurações de agrupamento, explorando sua capacidade 
              de ajustar os centros dos clusters e definir limites de decisão para separar dados. Ao aplicar o algoritmo em uma 
              base de dados sintética com conjuntos circulares, observou-se como o número de clusters (K) impacta diretamente a 
              qualidade do agrupamento, com valores inadequados de K levando a agrupamentos menos representativos. A análise da curva 
              de custo permitiu que ele identificasse o ponto em que o número de clusters resulta em um bom equilíbrio entre 
              simplicidade e precisão. Além disso, foi mostrada uma aplicação do K-médias para a compressão de imagens.

     12 - Modelos Múltiplos em Agrupamento

            - Este notebook se refere aos Capítulo 14 (Modelos Múltiplos Descritivos) e aos artigos Data Clustering 
              Using Evidence Accumulation (Fred & Jain, 2002) e Combining Multiple Clusterings Using Evidence 
              Accumulation (Fred & Jain, 2005).
              Nele, é ilustrada a técnica de Evidence Accumulation-based Clustering (EAC), na qual uma série
              de agrupamentos são gerados através do método de K-Médias, para depois serem combinados em um 
              agrupamento final através de um algoritmo hierárquico. É realizado um estudo da técnica sobre 
              a base de dados “spirals”, mostrando como as estruturas reais do conjunto podem ser descobertas 
              através da junção de múltiplos métodos de agrupamento.

     13 - Aplicação em Bioinformática

            - Este notebook se refere às Seções I (Preparação de Dados), II (Modelos Preditivos) e III (Modelos 
              Descritivos), além do Capítulo 19 (Sequências Biológicas).
              Nele, é realizado um experimento completo usando uma base real da área de Bioinformática. São 
              tratados dois problemas distintos, com objetivos semelhantes: classificação e agrupamento de amostras 
              de microarranjo de DNA de pacientes leucêmicos. A motivação e dados utilizados são provenientes do 
              artigo Molecular Classification of Cancer: Class Discovery and Class Prediction by Gene Expression 
              Monitoring (Golub et al., 1999). 

     14 - Aplicações em Mineração de Texto

           - Este notebook se refere ao Capítulo 23 (Categorização de Textos).
             Ele aborda o problema de classificação de textos, por meio de duas aplicações: classificação de 
             spam e detecção de notícias falsas (fake news). O método naive Bayes multinomial é usado 
             para realizar a classificação dos documentos nos dois problemas abordados. São mostradas as 
             principais etapas necessárias para a classificação de texto, incluindo o pré-processamento 
             (e.g., deixar todas as palavras com letras minúsculas, tratar URLs, emails e outros termos especiais, 
             remover stopwords e aplicar estemização), a conversão do texto em um vetor de atributos e o treinamento 
             de um método de classificação.

