# import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
data = pd.read_excel("dataset.xlsx")
# print(dataframe)

def first_columns():
    POSITIVES = []
    INTENSIVE_CARE = []
    for header in data:
        # column = pd.Series(dataframe[header])
        if(header == 'SARS-Cov-2 exam result'):
            POSITIVES = data[data[header] == 'positive']
        if(header == 'Patient addmited to intensive care unit (1=yes, 0=no)'):
            INTENSIVE_CARE = data[data[header] == 1]

def write_table(name, text):
    f = open(f"./data/{name}.txt", "w")
    f.write(str(text))
    f.close()
    pass
def iqr_outlier(data : pd.Series):
    ### AMPLITUDE INTERQUARTIL | IQR = (Q3 - Q1)
    # Será usado o IQR para definir os outliers do
    # campo. Portanto é necessário remover dados 
    # faltantes e ordena-los para que seja possível
    # encontrar a amplitude interquartil do campo.

    ### Definindo os quartis
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    ### Encontrando os limites 
    lim_inferior = q1 - (1.5 * (q3 - q1))
    lim_superior = q3 + (1.5 * (q3 - q1))
    # Com os limites é possível contruir o intervalo
    # interquartil e podemos usa-lo para identificar
    # os outliers estando abaixo ou acima dele
    outlier_list = []
    length = data.size
    ### Agora é verificar os elementos estão fora intervalo 
    for i in range(length): # percorrendo todos o elemento da amostra
        is_out = False
        ### Verifica se o valor está fora da amplitude, sendo outlier
        if(data.iloc[i] < lim_inferior or data.iloc[i] > lim_superior):
            is_out = True
        outlier_list.append(is_out)
    ### Criando uma tabela 
    # Preenchendo a tabela com o valor do limites e a verificação de se 
    # o elemento da amostra se encontra fora desse intervalo
    iqr_table = pd.DataFrame({
        "[IQR] min" : pd.Series([lim_inferior] * length),
        "[IQR] max" : pd.Series([lim_superior] * length),
        "[IQR] isOutlier": pd.Series(outlier_list)
    })
    return iqr_table
def std_outlier(data : pd.Series):
    ### Definindo a media 
    media = data.mean()
    ### Encontrando os limites
    lim_inferior = media - 3 * data.std() 
    lim_superior = media + 3 * data.std()
    
    outlier_list = []
    length = data.size

    for i in range(length):
        is_out = False

        if(data.iloc[i] < lim_inferior or data.iloc[i] > lim_superior):
            is_out = True
        outlier_list.append(is_out)
    
    std_table = pd.DataFrame({
        "[STD] min" : pd.Series([lim_inferior] * length),
        "[STD] max" : pd.Series([lim_superior] * length),
        "[STD] isOutlier" : pd.Series(outlier_list)
    })
    return std_table
def small_dataframe():
    ## RECONHECENDO OUTLIERS
    # Para isso iremos tratar cada coluna do dataset 
    # como uma pd.Serie e fazer manipulações a partir
    # do seus dados e do resultado das suas operações

    ## TRATANDO OS OUTLIERS DE CADA COLUNA 
    for field in NUMERIC_FIELDS:
        ### Removendo dados faltantes 
        clean_data = data[field].dropna()
        ### Ordenando os valores sobrantes
        clean_data.sort_values(inplace=True)
        if(clean_data.isnull().all() == False):
            
            ### Reiniciando o index para novo dataframe
            clean_data.reset_index(drop=True, inplace=True)
            
            if((clean_data == 0).all() == False):
                iqr = iqr_outlier(clean_data)
                std = std_outlier(clean_data)
                values = pd.DataFrame({
                    "value" : pd.Series(clean_data)
                })
            
                table = pd.concat([values, iqr, std], axis=1)
            
                name = field.replace('/', '')
                write_table(name=name, text=table.T.to_string())

NUMERIC_FIELDS = data.select_dtypes('number').columns[6:]      

small_dataframe()