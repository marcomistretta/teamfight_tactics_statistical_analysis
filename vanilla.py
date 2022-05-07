import pandas as pd
dataset = pd.read_csv('export_dataframe.csv')
print(dataset.head())
dataset = dataset[:3, :].values
print(dataset)