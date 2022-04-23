import numpy as np
import pandas as pd

dataset = pd.read_csv('export_dataframe.csv')

xd1 = dataset[["aug1"]].drop_duplicates().values.tolist()
xd2 = dataset[["aug2"]].drop_duplicates().values.tolist()
xd3 = dataset[["aug3"]].drop_duplicates().values.tolist()
xd1.extend(xd2)
xd1.extend(xd3)


def unique(list1):
    npArray1 = np.array(list1)
    uniqueNpArray1 = np.unique(npArray1)
    return uniqueNpArray1.tolist()

ylist = sorted(unique(xd1))
# XXX non ancora implementato
print(ylist, len(ylist))

np.save("aug_map", ylist)