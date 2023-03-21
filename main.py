# import matplotlib.pyplot as plt
import pandas as pd
dataframe = pd.read_excel("dataset.xlsx")
# print(dataframe)

POSITIVES = []
INTENSIVE_CARE = []
for header in dataframe:
    # column = pd.Series(dataframe[header])
    if(header == 'SARS-Cov-2 exam result'):
        POSITIVES = dataframe[dataframe[header] == 'positive']
    if(header == 'Patient addmited to intensive care unit (1=yes, 0=no)'):
        INTENSIVE_CARE = dataframe[dataframe[header] == 1]

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
for field in NUMERIC_FIELDS:
    name = field
    data = dataframe[field].dropna()

    table = pd.DataFrame({
        "value" : pd.Series(data.reset_index(drop=True)),
        "max" : pd.Series([data.max()]*data.shape[0]),
        "min" : pd.Series([data.min()]*data.shape[0])
    })
    f = open(f"./data/{name}.txt", "w")
    f.write(str(table.T.to_string()))
    f.close()