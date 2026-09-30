# -*- coding: utf-8 -*- 

import numpy as np
import sklearn as skl
import scipy
from scipy.sparse import csc_matrix

# importa alguns pacotes do sckit-learn
from sklearn import model_selection 
from sklearn import linear_model # necessario para usar regressão logística
from sklearn import naive_bayes # necessario para usar o metodo naive Bayes
from sklearn import tree # necessario para usar arvores de decisao
from sklearn import svm # necessario para usar o metodo SVM
from sklearn import neighbors # necessario para usar o metodo KNN
from sklearn import model_selection # necessario para fazer validacao cruzada
from sklearn import metrics # necessario para obter o desempenho da classificacao

import pandas as pd
import re #regular expression
import os
import sys 


def relatorioDesempenho(Y_test, Y_pred, classes, imprimeRelatorio=False):
  """
  Funcao usada calcular as medidas de desempenho da classificação.
  
  Parametros
  ----------   
    
  classes: classes do problema
  
  imprimeRelatorio: variavel booleana que indica se o relatorio de desempenho
                    deve ser impresso ou nao. 
     
  Retorno
  -------
  resultados: variavel do tipo dicionario (dictionary). As chaves
              desse dicionario serao os nomes das medidas de desempenho; os valores
              para cada chave serao as medidas de desempenho calculadas na funcao.
              
              Mais especificamente, o dicionario devera conter as seguintes chaves:
              
               - acuracia: valor entre 0 e 1 
               - revocacao: um vetor contendo a revocacao obtida em relacao a cada classe
                            do problema
               - precisao: um vetor contendo a precisao obtida em relacao a cada classe
                            do problema
               - fmedida: um vetor contendo a F-medida obtida em relacao a cada classe
                            do problema
               - revocacao_macroAverage: valor entre 0 e 1
               - precisao_macroAverage: valor entre 0 e 1
               - fmedida_macroAverage: valor entre 0 e 1
               - revocacao_microAverage: valor entre 0 e 1
               - precisao_microAverage: valor entre 0 e 1
               - fmedida_microAverage: valor entre 0 e 1
  """

  # obtém a quantidade de classes
  nClasses = len(classes)

  #obtem a acuracia
  acuracia = metrics.accuracy_score(Y_test, Y_pred)
    
  # inicializa as medidas de desempenho 
  revocacao = np.zeros( len(classes) )
  precisao = np.zeros( len(classes) )
  fmedida = np.zeros( len(classes) )
    
  # calcula a medida de desempenho para cada classe individualmente
  for i in range( len(classes) ):
    
      #transforma o problema multiclasse em binário, apenas para calcular o desempenho individual da classe i
      auxY_test = np.zeros( len(Y_test) ) # inicializa o vetor de classes binárias com 0
      auxY_pred = np.zeros( len(Y_pred) ) # inicializa o vetor de classes binárias com 0
      auxY_test[Y_test==classes[i]] = 1 # onde a classe for igual a classe[i], recebe valor 1
      auxY_pred[Y_pred==classes[i]] = 1 # onde a classe for igual a classe[i], recebe valor 1
        
      revocacao[i] = metrics.recall_score(auxY_test, auxY_pred, pos_label=1) # recall
      precisao[i] = metrics.precision_score(auxY_test, auxY_pred, pos_label=1) # precision
      fmedida[i] = metrics.f1_score(auxY_test, auxY_pred, pos_label=1) # precision 
  

  revocacao_microAverage =  metrics.recall_score(Y_test, Y_pred, average='micro') # sensitividade ou recall
  precisao_microAverage = metrics.precision_score(Y_test, Y_pred, average='micro')
  fmedida_microAverage = metrics.f1_score(Y_test, Y_pred, average='micro')

  revocacao_macroAverage =  metrics.recall_score(Y_test, Y_pred, average='macro') # sensitividade ou recall
  precisao_macroAverage = metrics.precision_score(Y_test, Y_pred, average='macro')
  fmedida_macroAverage = metrics.f1_score(Y_test, Y_pred, average='macro')
  
  
  # imprimindo os resultados para cada classe
  if imprimeRelatorio:
        
      print('\n\tRevocacao   Precisao   F-medida   Classe')
      for i in range(nClasses):
        print('\t%1.3f       %1.3f      %1.3f      %s' % (revocacao[i], precisao[i], fmedida[i],classes[i] ) )
    
      print('\t------------------------------------------------');
      
      #imprime as médias
      print('\t%1.3f       %1.3f      %1.3f      Média macro' % (revocacao_macroAverage, precisao_macroAverage, fmedida_macroAverage) )
      print('\t%1.3f       %1.3f      %1.3f      Média micro\n' % (revocacao_microAverage, precisao_microAverage, fmedida_microAverage) )
    
      print('\tAcuracia: %1.3f' %acuracia)
      
  # guarda os resultados em uma estrutura tipo dicionario
  resultados = {'revocacao': revocacao, 'acuracia': acuracia, 'precisao':precisao, 'fmedida':fmedida}
  resultados.update({'revocacao_macroAverage':revocacao_macroAverage, 'precisao_macroAverage':precisao_macroAverage, 'fmedida_macroAverage':fmedida_macroAverage})
  resultados.update({'revocacao_microAverage':revocacao_microAverage, 'precisao_microAverage':precisao_microAverage, 'fmedida_microAverage':fmedida_microAverage})

  return resultados 