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

NUMERIC_FIELDS = [
    'Hematocrit',
    'Hemoglobin',
    'Platelets',
    'Mean platelet volume ',
    'Red blood Cells',
    'Lymphocytes',
    'Mean corpuscular hemoglobin concentration\xa0(MCHC)',
    'Leukocytes',
    'Basophils',
    'Mean corpuscular hemoglobin (MCH)',
    'Eosinophils',
    'Mean corpuscular volume (MCV)',
    'Monocytes',
    'Red blood cell distribution width (RDW)',
    'Serum Glucose'
]      
def write_table(name, text):
    f = open(f"./data/{name}.txt", "w")
    f.write(str(text))
    f.close()
pass
def iqr_outlier(data : pd.Series):
    ### Definindo os quartis
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    ### Encontrando os limites 
    lim_inferior = q1 + (1.5 * (q3 - q1))
    lim_superior = q3 + (1.5 * (q3 - q1))

    is_outlier = []
    
    length = data.size
    for i in range(length):
        result = False
        ### Verifica se o valor está fora da amplitude, sendo outlier
        if(data.iloc[i] < lim_inferior, data.iloc[i] > lim_superior):
            result = True
        is_outlier.append(result)

    iqr_table = pd.DataFrame({
        "[IQR] min" : pd.Series([lim_inferior] * length),
        "[IQR] max" : pd.Series([lim_superior] * length),
        "[IQR] isOutlier": pd.Series(is_outlier)
    })
    return iqr_table
def small_dataframe():
    ## RECONHECENDO OUTLIERS
    # Para isso iremos tratar cada coluna do dataset 
    # como uma pd.Serie e fazer manipulações a partir
    # do seus dados e do resultado das suas operações

    ## TRATANDO OS OUTLIERS DE CADA COLUNA 
    ### AMPLITUDE INTERQUARTIL | IQR = (Q3 - Q1)
    # Será usado o IQR para definir os outliers do
    # campo. Portanto é necessário remover dados 
    # faltantes e ordena-los para que seja possível
    # encontrar a amplitude interquartil do campo.
    
    for field in NUMERIC_FIELDS:
        ### Removendo dados faltantes 
        clean_data = data[field].dropna()
        ### Ordenando os valores sobrantes
        clean_data.sort_values(inplace=True)
        ### Reiniciando o index para novo dataframe
        clean_data.reset_index(drop=True, inplace=True)
        ### Pegando o comprimento dos dados
        n = clean_data.shape[0] # n = length
        
        iqr = iqr_outlier(clean_data)
        values = pd.DataFrame({
            "value" : pd.Series(clean_data)
        })

        table = pd.concat([values, iqr], axis=1)
        write_table(name=field, text=table.T.to_string())

small_dataframe()