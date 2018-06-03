
# coding: utf-8

#  ![conjuntodedados.jpg](conjuntodedados.jpg)
#  
#  Análise de Gastos públicos dos deputados da CLDF  [Trabalho de Data Science]
# -----------------------------------------
# #### @author: Luiz Eduardo 
# ### [Linkedin](www.linkedin.com/in/isweluiz)
# #### Professor: Sergio Côrtes
# ------------------
# Descrição: A transparência no trabalho dos governantes e das instituições e empresas públicas é obrigatória no Brasil. A Lei de Acesso à Informação - LAI, de 2011, garante o direito de solicitar e receber informações de órgãos públicos, de forma gratuita, para qualquer cidadão ou entidade. Esse acesso livre à informação permite que todos os cidadãos tenham a mesma capacidade de fiscalizar, monitorar, conhecer e discutir os gastos, as ações e as decisões das entidades.
# 
# 
# 
# > ### Índice
# > Limpeza de Dados (Data Cleaning)
# 
# > Análise dos Dados (Data Analysis)
# 
# > Visualização dos Dados (Data Visualization)
# 
# > Conclusão
# 
# 
# > ### Escopo da análise
# 
# > Extração dos dados da CLDF no link [Dados Abertos CLDF](dosabertos.cl.df.gov.br) 
# 
# > Anális dos dados (data analysis)
# 
# > Qual deputado que mais gastou? Em qual periódo do ano ele(a) mais gastou?
# 
# > Qual deputado que menos gastou neste período?
# 
# >Quais forncedores receberam os maiores valores?

# In[23]:


#Importando bibiliotecas
import matplotlib.pyplot as plt # Bibilioteca util para criar gráficos
import pandas as pd # Bibilioteca para auxiliar a importar e maniular nossos dataframes
import numpy as np # Bibilioteca útil para realizar operações matemáticas
import seaborn as sns # Bibilioteca utilizada para dar um toque especial nos gráficos
import math

#import chardet   #Trabalha com leitura de arquivos, acredito que n será necessário utiliza=lá
plt.style.use('ggplot') #Customização de gráficos , informações em https://matplotlib.org/users/style_sheets.html
#print(plt.style.available)


# In[79]:

verba2016 = pd.read_excel(r'C:\Users\p188432\Downloads\Data science\Python-master\Gastos públicos dos deputados\02 - Dados Preparadps\verba_indenizatoria_2016.xlsx')
#verba2017
verba2017 = pd.read_excel(r'C:\Users\p188432\Downloads\Data science\Python-master\Gastos públicos dos deputados\02 - Dados Preparadps\verba_indenizatoria_2017.xlsx')
verba2016.head  #Visualizando as primeiras colunas e linhas do nosso dataframe
verba.head

# In[80]:

list(verba.columns) #Lista das colunas que possuimos em nosso dataframe
verba2017.iloc[10]

# In[18]:
#Listando o nome de cada Deputado contido na coluna nome
quantos =  verba2017['Nome'].unique()
list(quantos)


# In[81]:
#Contagem de linhas em cada coluna
verba.count() 

# In[16]:
#Contador de linhas e colunas
print('O arquivo \"verba" ' ' possui ' + str(verba.shape[0]) + ' linhas e ' +str(verba.shape[1]) + ' colunas') 

# In[19]:

#verificando o tipo de dados que estamos trabalhando
verba.dtypes

# In[20]:
#Indormação de todas as colunas númericas para vermos se há algum valor indevido
verba.describe() 

# In[21]:
# Retirando colunas que não iremos utilizar
#verba.drop(['' ], axis = 1, inplace = True)

# In[84]:


verba.columns


# In[83]:


#Alterando o nome de algumas colunas
verba.columns = ['Gabinete', 'Deputado', 'CPF', 'Fornecedor', 'CNPJ (ou CPF)',
       'Data', 'Mês', 'Nº Documento', 'Valor']


# In[85]:


#Removendo linhas cuja o campo das colunas estão vazios
verba = verba.dropna(subset=  ['Valor'], axis=0) 
verba = verba.dropna(subset= ['Deputado'], axis=0)


# In[86]:


#Criando uma coluna 
verba['Contador'] = 0


# In[87]:


print(verba['Valor'].head(5))


# In[88]:


#Vai armazenar cada político e seu respectivo gasto
despesas_deputado = {}
nome_deputado = verba['Deputado'].unique()
list(nome_deputado)


# In[89]:


#Efetuando o agrupamento das despesas dos deputados e somando.
for i in nome_deputado: 
    i_nome = verba[verba['Deputado'] == i]
    total_gastos = i_nome['Valor'].sum()
    despesas_deputado[i] = total_gastos
    gastos_por_deputados = pd.DataFrame.from_dict(despesas_deputado, orient='index') 
    gastos_por_deputados.columns = ['VALOR'] #Adicionando um nome a coluna númerica
gastos_por_deputados.head(10)


# In[90]:


#Ordenando os valores do dataframe
gastos_por_deputados = gastos_por_deputados.sort_values(by = 'VALOR', ascending=False) 
gastos_por_deputados.plot(kind='barh' , color='green', grid =True, alpha=0.8) 
plt.title('Gastos por Deputado') #Titulo para o gráfico
plt.xlabel('Valor gasto em 2017') # Legenda para o eixo x
#plt.ylabel('Deputado') #Legenda para o eixo y
plt.show()


# > ### Notamos que o Deputado Chico Vigilante foi o deputado que teve maiores gastos púbicos no ano de 2017
# > #### Agora devemos reponder as seguintes perguntas;
# 
# > Quais foram os seus fornecedores?
# 
# > Quais fornecedores receberam os maiores valores?
# 
# > Qual o periódo do ano ele mais gastou?

# In[91]:


#Conta a quantidade de linhas do arquivo, quantidade de regitros de contas lançados pelo deputado
maior_gasto = verba[verba['Deputado'] == 'Deputado Chico Vigilante'].reset_index()
maior_gasto.shape[0] 


# In[92]:


maior_gasto.head()


# In[93]:


#Função que retorna um Dataframe com os valores agrupados no ano gastos pelo deputado
def gastos_fornecedor(deputado_):
    nome_deputado = verba[verba['Deputado'] == deputado_ ]
    nome_deputado = nome_deputado.groupby('Fornecedor')[['Deputado', 'Valor']].sum()
    return nome_deputado


# In[55]:


#Aplicando a função nos itens do Deputado Chico Vigilante
#Essa função pode ser aplicada para todos os deputados da lista
chico_vigilante = gastos_fornecedor('Deputado Chico Vigilante')
chico_vigilante = chico_vigilante.sort_values(by = 'Valor' , ascending = False)
chico_vigilante.head(15).plot(kind='barh', color= 'green', grid= True, title='Deputado Chico Vigilante')
plt.xlabel('Despesas') # Legenda para o eixo x
plt.show()


# .
# 

# In[94]:


#Qual foi o gasto mensal do Deputado Chico Vigilante?
#mensal_deputado = verba['Fornecedor']
mensal_deputado = verba.groupby('Mês')['Valor'].sum()
mensal_deputado.plot(title = 'Gastos por mês dos Deputados' , color = 'green', grid = True)
plt.ylabel('Gasto em R$')
plt.xlabel('Mês')
plt.show()


# In[100]:


#Percebemos que o mês 7 foi o menor gasto do ano, pegando valor total gasto no mês 7
mes = verba[verba['Mês'] == 5]['Valor'].sum()
verba.groupby('Mês')['Valor'].sum()

