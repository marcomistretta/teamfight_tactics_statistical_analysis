import pandas as pd

df = pd.read_csv("tree.tsv")

print(df["parent"])

print(df)