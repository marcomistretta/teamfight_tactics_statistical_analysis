
def merge_traits(df):
    df1 = df.iloc[:, 9:37]
    list = []
    for index, row in df1.iterrows():
        str1 = ''.join(str(e) for e in row.values.flatten().tolist())
        list.append(str1)
    df.insert(90, 'merged_traits', list)
