import pandas as pd

df_item = pd.read_csv('format_K_CON_UN_SENSO.csv')
print(df_item.columns)

df_item['BFSword+BFSword'] = df_item['BFSword+BFSword'] + df_item['b']
df_item['BFSword+Bow'] = df_item['BFSword+Bow'] + df_item['b']
df_item['BFSword+Ap'] = df_item['BFSword+Ap'] + df_item['b']
df_item['BFSword+Tear'] = df_item['BFSword+Tear'] + df_item['b']
df_item['BFSword+ChainVest'] = df_item['a'] + df_item['b']
df_item['BFSword+NegatronCloak'] = df_item['a'] + df_item['b']
df_item['BFSword+GiantsBelt'] = df_item['a'] + df_item['b']
df_item['BFSword+Spatula'] = df_item['a'] + df_item['b']
df_item['BFSword+Gloves'] = df_item['a'] + df_item['b']

df_item['Bow+Ap'] = df_item['a'] + df_item['b']
df_item['Bow+Tear'] = df_item['a'] + df_item['b']
df_item['Bow+ChainVest'] = df_item['a'] + df_item['b']
df_item['Bow+NegatronCloak'] = df_item['a'] + df_item['b']
df_item['Bow+GiantsBelt'] = df_item['a'] + df_item['b']
df_item['Bow+Spatula"'] = df_item['a'] + df_item['b']
df_item['Bow+Gloves'] = df_item['a'] + df_item['b']

df_item['Ap+Ap'] = df_item['a'] + df_item['b']


df_item['BFSword+BFSword'] = df_item['a'] + df_item['b']
df_item['BFSword+BFSword'] = df_item['a'] + df_item['b']
df_item['BFSword+BFSword'] = df_item['a'] + df_item['b']
df_item['BFSword+BFSword'] = df_item['a'] + df_item['b']
df_item['BFSword+BFSword'] = df_item['a'] + df_item['b']
df_item['BFSword+BFSword'] = df_item['a'] + df_item['b']
df_item['BFSword+BFSword'] = df_item['a'] + df_item['b']
df_item['BFSword+BFSword'] = df_item['a'] + df_item['b']
df_item['BFSword+BFSword'] = df_item['a'] + df_item['b']
df_item['BFSword+BFSword'] = df_item['a'] + df_item['b']
df_item['BFSword+BFSword'] = df_item['a'] + df_item['b']
df_item['BFSword+BFSword'] = df_item['a'] + df_item['b']
df_item['BFSword+BFSword'] = df_item['a'] + df_item['b']
df_item['BFSword+BFSword'] = df_item['a'] + df_item['b']
df_item['BFSword+BFSword'] = df_item['a'] + df_item['b']
df_item['BFSword+BFSword'] = df_item['a'] + df_item['b']
df_item['BFSword+BFSword'] = df_item['a'] + df_item['b']
df_item['BFSword+BFSword'] = df_item['a'] + df_item['b']
df_item['BFSword+BFSword'] = df_item['a'] + df_item['b']

df_item = df_item[
    ["BFSword+BFSword", "BFSword+Bow", "BFSword+Ap", "BFSword+Tear", "BFSword+ChainVest", "BFSword+NegatronCloak",
     "BFSword+GiantsBelt", "BFSword+Spatula", "BFSword+Gloves", "Bow+Bow", "Bow+Ap", "Bow+Tear",
     "Bow+ChainVest", "Bow+NegatronCloak", "Bow+GiantsBelt", "Bow+Spatula", "Bow+Gloves", "Ap+Ap",
     "Ap+Tear", "Ap+ChainVest", "Ap+NegatronCloak", "Ap+GiantsBelt", "Ap+Spatula", "Ap+Gloves", "Tear+Tear",
     "Tear+ChainVest",
     "Tear+NegatronCloak", "Tear+GiantsBelt", "Tear+Spatula", "Tear+Gloves", "ChainVest+ChainVest",
     "ChainVest+NegatronCloak", "ChainVest+GiantsBelt", "ChainVest+Spatula", "ChainVest+Gloves",
     "NegatronCloak+NegatronCloak", "NegatronCloak+GiantsBelt", "NegatronCloak+Spatula", "NegatronCloak+Gloves",
     "GiantsBelt+GiantsBelt", "GiantsBelt+Spatula", "GiantsBelt+Gloves", "Spatula+Spatula",
     "Spatula+Gloves", "Gloves+Gloves"]]
print(df_item.columns)
print(len(df_item.columns))

df_item.rename(columns={"BFSword+BFSword": "xxx", "BFSword+Bow": "xxx", "BFSword+Ap": "xxx", "BFSword+Tear": "xxx",
                        "BFSword+ChainVest": "xxx",
                        "BFSword+NegatronCloak": "xxx", "BFSword+GiantsBelt": "xxx", "BFSword+Spatula": "xxx",
                        "BFSword+Gloves": "xxx", "Bow+Bow": "xxx",
                        "Bow+Ap": "xxx", "Bow+Tear": "xxx", "Bow+ChainVest": "xxx", "Bow+NegatronCloak": "xxx",
                        "Bow+GiantsBelt": "xxx", "Bow+Spatula": "xxx",
                        "Bow+Gloves": "xxx", "Ap+Ap": "xxx", "Ap+Tear": "xxx", "Ap+ChainVest": "xxx",
                        "Ap+NegatronCloak": "xxx", "Ap+GiantsBelt": "xxx",
                        "Ap+Spatula": "xxx", "Ap+Gloves": "xxx", "Tear+Tear": "xxx", "Tear+ChainVest": "xxx",
                        "Tear+NegatronCloak": "xxx", "Tear+GiantsBelt": "xxx",
                        "Tear+Spatula": "xxx", "Tear+Gloves": "xxx", "ChainVest+ChainVest": "xxx",
                        "ChainVest+NegatronCloak": "xxx", "ChainVest+GiantsBelt": "xxx",
                        "ChainVest+Spatula": "xxx", "ChainVest+Gloves": "xxx", "NegatronCloak+NegatronCloak": "xxx",
                        "NegatronCloak+GiantsBelt": "xxx",
                        "NegatronCloak+Spatula": "xxx", "NegatronCloak+Gloves": "xxx", "GiantsBelt+GiantsBelt": "xxx",
                        "GiantsBelt+Spatula": "xxx",
                        "GiantsBelt+Gloves": "xxx", "Spatula+Spatula": "xxx", "Spatula+Gloves": "xxx",
                        "Gloves+Gloves": "xxx"})
