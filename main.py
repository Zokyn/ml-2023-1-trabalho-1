# import matplotlib.pyplot as plt
import pandas as pd
dataframe = pd.read_excel("dataset.xlsx")
# print(dataframe)
POSITIVES = []
REGULAR_WARD = []
SEMI_INTENSIVE = []
INTENSIVE_CARE = []

for header in dataframe:
    # column = pd.Series(dataframe[header])
    if(header == 'SARS-Cov-2 exam result'):
        POSITIVES = dataframe[dataframe['SARS-Cov-2 exam result'] == 'positive']
    if(
        header == 'Patient addmited to regular ward (1=yes, 0=no)' or
        header == 'Patient addmited to semi-intensive unit (1=yes, 0=no)' or
        header == 'Patient addmited to intensive care unit (1=yes, 0=no)'
        ):
        REGULAR_WARD = dataframe[dataframe['Patient addmited to regular ward (1=yes, 0=no)'] == 1]
        SEMI_INTENSIVE = dataframe[dataframe['Patient addmited to semi-intensive unit (1=yes, 0=no)'] == 1]
        INTENSIVE_CARE = dataframe[dataframe['Patient addmited to intensive care unit (1=yes, 0=no)'] == 1]