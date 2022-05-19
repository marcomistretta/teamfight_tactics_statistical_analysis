import itertools

import numpy as np
import pandas as pd


def _reformat_A(df):
    '''
    FORMATO BASE: (58+1 colonne)
    2 colonne in più del paper perchè 3 augment al posto di game mode
    NO TRAITS
    '''
    df = df[["unit1", "item1_1", "item2_1", "item3_1", "tier1", "unit2", "item1_2", "item2_2", "item3_2",
             "tier2", "unit3", "item1_3", "item2_3", "item3_3", "tier3", "unit4", "item1_4", "item2_4",
             "item3_4", "tier4", "unit5", "item1_5", "item2_5", "item3_5", "tier5", "unit6",
             "item1_6", "item2_6", "item3_6", "tier6", "unit7", "item1_7", "item2_7",
             "item3_7", "tier7", "unit8", "item1_8", "item2_8", "item3_8", "tier8", "unit9",
             "item1_9", "item2_9", "item3_9", "tier9", "unit10", "item1_10", "item2_10",
             "item3_10", "tier10", "unit11", "item1_11", "item2_11", "item3_11", "tier11",
             "aug1", "aug2", "aug3", "placement"]]

    df.to_csv('format_A.csv', index=False)
    return df


def _reformat_B(df):
    '''
    riduzione del FORMATO_A
    minimal 56+1 colonne
    tentativo fallito di UNIFICARE AUGMENT

    mappare gli augment in numeri e poi attaccarli in ordine crescente
    00
    01
    02
    03

    '''
    return df


def _reformat_C(df):
    '''
    FORMATO_A + MERGE_TRAITS come stringa numerica di 28 numeri tra 0 e 4 (59+1 colonne)
    '''
    df1 = df[["trait_1", "trait_2", "trait_3", "trait_4",
              "trait_5", "trait_6", "trait_7", "trait_8", "trait_9", "trait_10", "trait_11",
              "trait_12", "trait_13", "trait_14", "trait_15", "trait_16", "trait_17",
              "trait_18", "trait_19", "trait_20", "trait_21", "trait_22", "trait_23",
              "trait_24", "trait_25", "trait_26", "trait_27", "trait_28"]]
    list = []
    for index, row in df1.iterrows():
        str1 = ''.join(str(e) for e in row.values.flatten().tolist())
        list.append(str1)
    df = reformat_to(df, format="A", verbose=0)
    df.insert(loc=df.shape[1] - 1, column='merged_traits', value=list)

    return df


def _reformat_D(df):
    '''
    VERO PAPER FORMAT unit e merge augs as game mode
    '''
    aug_map = np.load("aug_map.npy")
    for index, aug in enumerate(aug_map):
        df.loc[df['aug1'] == aug, 'aug1'] = ("00" + str(index))[-3:]
        df.loc[df['aug2'] == aug, 'aug2'] = ("00" + str(index))[-3:]
        df.loc[df['aug3'] == aug, 'aug3'] = ("00" + str(index))[-3:]

    df1 = df[['aug1', 'aug2', 'aug3']]
    list = []
    for index, row in df1.iterrows():
        str1 = ''.join(str(e) for e in row.values.flatten().tolist())
        list.append(str1)
    df = reformat_to(df, format="A", verbose=0)
    df.insert(loc=df.shape[1] - 1, column='merged_augs', value=list)
    df = df.loc[:, ~df.columns.isin(['aug1', 'aug2', 'aug3'])]

    return df


def _reformat_E(df):
    # XXX pass else
    pass


def _reformat_V(df):
    # XXX tutto tranne match_id
    placement = df[["placement"]]
    df = df.loc[:, ~df.columns.isin(['match_id', 'placement'])]
    df.insert(loc=df.shape[1], column='placement', value=placement)

    return df


def _reformat_T(df):
    if False:
        placement = df[["placement"]]

        champ_list = df[["unit1"]].values.flatten().tolist()
        champ_list.extend(df[["unit2"]].values.flatten())
        champ_list.extend(df[["unit3"]].values.flatten())
        champ_list.extend(df[["unit4"]].values.flatten())
        champ_list.extend(df[["unit5"]].values.flatten())
        champ_list.extend(df[["unit6"]].values.flatten())
        champ_list.extend(df[["unit7"]].values.flatten())
        champ_list.extend(df[["unit8"]].values.flatten())
        champ_list.extend(df[["unit9"]].values.flatten())
        champ_list.extend(df[["unit10"]].values.flatten())
        champ_list.extend(df[["unit11"]].values.flatten())

        champ_list = list(set(champ_list))
        champ_list.remove('0')

        for champ in champ_list:
            # print(df.loc[df['unit1'] == champ, 'tier1'].values)
            # print(df.loc[df['unit2'] == champ, 'tier2'].values)

            champ_oc = np.empty((df.shape[0], 11))

            for i in range(1, 12):
                ch = df.loc[df['unit' + str(i)] == champ, 'tier' + str(i)].reindex(
                    list(range(df.index.min(), df.index.max() + 1)), fill_value=0)

                champ_oc[:, i - 1] = ch

            tier_champ = np.amax(champ_oc, axis=1)

            df.insert(loc=df.shape[1], column=champ, value=tier_champ)
            print(champ)

        # print(df.head())

        df = df[champ_list]
        df.insert(loc=df.shape[1], column='placement', value=placement)
        print(df.head())

        df.to_csv('format_T.csv', index=False)
    else:
        df = pd.read_csv('format_T.csv')

    return df


def _reformat_Z(df):
    df = pd.read_csv('export_dataframe.csv')
    df = reformat_to(df, "T", verbose=0)

    df = df[["placement", "TFT6_Camille", "TFT6_Brand", "TFT6_JarvanIV", "TFT6_Illaoi", "TFT6_Nocturne", "TFT6_Darius",
             "TFT6_Ziggs",
             "TFT6_Kassadin", "TFT6_Ezreal", "TFT6_Singed", "TFT6_Poppy", "TFT6_Twitch", "TFT6_Caitlyn", "TFT6_Zyra",
             "TFT6_Syndra", "TFT6_Sejuani", "TFT6_Quinn", "TFT6_Zilean", "TFT6_Talon", "TFT6_Swain", "TFT6_Corki",
             "TFT6_Ashe", "TFT6_Warwick", "TFT6_Lulu", "TFT6_RekSai", "TFT6_Blitzcrank", "TFT6_Vex", "TFT6_Lucian",
             "TFT6_Senna", "TFT6_Malzahar", "TFT6_Zac", "TFT6_Tryndamere", "TFT6_ChoGath", "TFT6_Leona", "TFT6_Ekko",
             "TFT6_Gnar", "TFT6_Gangplank", "TFT6_MissFortune", "TFT6_Morgana", "TFT6_Alistar", "TFT6_Renata",
             "TFT6_Seraphine", "TFT6_Ahri", "TFT6_Jhin", "TFT6_Draven", "TFT6_Braum", "TFT6_KhaZix", "TFT6b_Vi",
             "TFT6_Sivir", "TFT6_Irelia", "TFT6_Orianna", "TFT6_Veigar", "TFT6_Viktor", "TFT6_TahmKench", "TFT6_Jinx",
             "TFT6_Jayce", "TFT6_Zeri", "TFT6_Silco", "TFT6_Galio", "TFT6_Kaisa"]]

    df.loc[df['placement'] <= 4, ['placement']] = 1
    df.loc[df['placement'] > 4, ['placement']] = 0

    df.to_csv('format_unit_cost.csv', index=False)

    return df


def _reformat_I(df):
    if False:
        #
        # item_list = df[["item1_1"]].values.flatten().tolist()
        # item_list.extend(df[["item2_1"]].values.flatten())
        # item_list.extend(df[["item3_1"]].values.flatten())
        #
        # for i in range(1,12):
        #     item_list.extend(df[["item1_"+str]].values.flatten())
        #     item_list.extend(df[["item2_2"]].values.flatten())
        #     item_list.extend(df[["item3_2"]].values.flatten())
        df_item = pd.DataFrame(
            columns=['BFSword', 'Bow', 'Ap', 'Tear', 'ChainVest', 'NegatronCloak', 'GiantsBelt', 'Spatula', 'Gloves'])
        for index, row in df.iterrows():
            print(index)

            item_list = []
            for i in range(1, 12):
                item_list.append(row["item1_" + str(i)])
                item_list.append(row["item2_" + str(i)])
                item_list.append(row["item3_" + str(i)])

            item_list = [item for item in item_list if item < 100 and item != 0]
            single_item_list = [sum(map(lambda x: str(x).count(str(i)), item_list)) for i in range(1, 10)]
            df_item.loc[index] = single_item_list
        print(df_item)

        df_item.to_csv('format_I.csv', index=False)

        # df1 = df
        # df = reformat_to(format="X", verbose=0)
        # df.insert(loc=df.shape[1]-1, column=df1.columns[92:304], value=df1[92:304])
    else:
        df_item = pd.read_csv('format_I.csv')
    df1 = pd.read_csv('export_dataframe.csv')

    df1 = reformat_to(df1, "T", verbose=0)

    result = pd.concat([df_item, df1], axis=1)

    return result


def _reformat_M(df):
    if False:

        df_item = pd.DataFrame(
            columns=['BFSword', 'Bow', 'Ap', 'Tear', 'ChainVest', 'NegatronCloak', 'GiantsBelt', 'Spatula', 'Gloves'])
        for index, row in df.iterrows():
            print(index)

            item_list = []
            for i in range(1, 12):
                item_list.append(row["item1_" + str(i)])
                item_list.append(row["item2_" + str(i)])
                item_list.append(row["item3_" + str(i)])

            item_list = [item for item in item_list if item < 100 and item != 0]
            single_item_list = [sum(map(lambda x: str(x).count(str(i)), item_list)) for i in range(1, 10)]
            df_item.loc[index] = single_item_list
        print(df_item)

        df_item.to_csv('format_I.csv', index=False)

        # df1 = df
        # df = reformat_to(format="X", verbose=0)
        # df.insert(loc=df.shape[1]-1, column=df1.columns[92:304], value=df1[92:304])
    else:
        df_item = pd.read_csv('format_I.csv')
    df1 = pd.read_csv('export_dataframe.csv')

    df1 = reformat_to(df1, "T", verbose=0)

    result = pd.concat([df_item, df1], axis=1)

    return result


def _reformat_K(df):
    if False:

        # item_list = df[["item1_1"]].values.flatten().tolist()
        # item_list.extend(df[["item2_1"]].values.flatten())
        # item_list.extend(df[["item3_1"]].values.flatten())
        #
        # for i in range(1,12):
        #     item_list.extend(df[["item1_"+str]].values.flatten())
        #     item_list.extend(df[["item2_2"]].values.flatten())
        #     item_list.extend(df[["item3_2"]].values.flatten())
        single_item = ['BFSword', 'Bow', 'Ap', 'Tear', 'ChainVest', 'NegatronCloak', 'GiantsBelt', 'Spatula', 'Gloves']
        #                    1       2      3   4       5               6               7               8           9
        item_dict = {}
        for key, value in zip([i for i in range(1, 10)], single_item):
            item_dict[key] = value

        inverse_item_ids = {v: k for k, v in item_dict.items()}

        composite_item = []
        composite_item_ids = []
        for element in itertools.product(*[single_item, single_item]):
            composite_item.append(str(element[0]) + '+' + str(element[1]))
            composite_item_ids.append(str(inverse_item_ids[str(element[0])]) + str(inverse_item_ids[str(element[1])]))

        df_item_complete = pd.DataFrame()

        for idx, item in enumerate(composite_item_ids):
            item_oc = np.empty((df.shape[0], 11 * 3))
            for i in range(1, 12):
                itm = df.loc[df['item1_' + str(i)] == int(item), 'item1_' + str(i)].reindex(
                    list(range(df.index.min(), df.index.max() + 1)), fill_value=0)
                for _idx, a in enumerate(itm):
                    if a != 0:
                        itm[_idx] = 1
                item_oc[:, (i - 1)] = itm

                itm = df.loc[df['item2_' + str(i)] == int(item), 'item2_' + str(i)].reindex(
                    list(range(df.index.min(), df.index.max() + 1)), fill_value=0)
                for _idx, a in enumerate(itm):
                    if a != 0:
                        itm[_idx] = 1
                item_oc[:, (i - 1) + 11] = itm

                itm = df.loc[df['item3_' + str(i)] == int(item), 'item3_' + str(i)].reindex(
                    list(range(df.index.min(), df.index.max() + 1)), fill_value=0)
                for _idx, a in enumerate(itm):
                    if a != 0:
                        itm[_idx] = 1
                item_oc[:, (i - 1) + 22] = itm

            item_oc_tot = np.sum(item_oc, axis=1)
            # print(composite_item[idx], item_oc_tot)

            df_item_complete.insert(loc=df_item_complete.shape[1], column=composite_item[idx], value=item_oc_tot)

        df_item_complete.to_csv('format_K.csv', index=False)

        # df1 = df
        # df = reformat_to(format="X", verbose=0)
        # df.insert(loc=df.shape[1]-1, column=df1.columns[92:304], value=df1[92:304])
    else:

        single_item = ['BFSword', 'Bow', 'Ap', 'Tear', 'ChainVest', 'NegatronCloak', 'GiantsBelt', 'Spatula', 'Gloves']
        #                    1       2      3   4       5               6               7               8           9
        item_dict = {}
        for key, value in zip([i for i in range(1, 10)], single_item):
            item_dict[key] = value

        inverse_item_ids = {v: k for k, v in item_dict.items()}

        composite_item = []
        composite_item_ids = []
        for element in itertools.product(*[single_item, single_item]):
            composite_item.append(str(element[0]) + '+' + str(element[1]))
            composite_item_ids.append(str(inverse_item_ids[str(element[0])]) + str(inverse_item_ids[str(element[1])]))

        composite_item_dict = {}
        for i, _ in enumerate(composite_item):
            composite_item_dict[composite_item_ids[i]] = composite_item[i]

        df_item_complete = pd.read_csv('format_K.csv')

        real_item_names = ["Tacticians Crow", "Runaans Hurricane", "Morellonomicon", "Last Whisper", "Ionic Spark",
                           "Recurve Bow", "B.F.Sword", "Warmogs Armor", "Thiefs Gloves", "Statikk Shiv",
                           "Jeweled Gauntlet", "Infinity Edge", "Evil Giantslayer", "Dragons Claw", "Bramble Vest",
                           "Blue Buff", "Archangels Staff", "Sparring Gloves", "Zephyr", "Titans Resolve",
                           "Sunfire Cape", "Spear of Shojin", "Redemption", "Rabadons Deathcap", "Hand of Justice",
                           "Guinsoos Rageblade", "Gargoyle Stoneplate", "Edge of Night", "Tear of the Goddess",
                           "Needlessly Large Rod", "ZzRot Portal", "Zekes Herald", "Shroud of Stillness", "Quicksilver",
                           "Locket of the Iron Solari", "Hextech Gunblade", "Frozen Heart", "Deathblade",
                           "Chalice of Power", "Giants Belt", "Chain Vest", "Rapid Firecannon", "Banshees Claw",
                           "Negatron Cloak", "Bloodthirster"]
        real_item_ids = [['88'], ['27', '72'], ['37', '73'], ['29', '92'], ['36', '63'], ['2'], ['1'], ['77'], ['99'],
                         ['24', '42'],
                         ['39', '93'], ['19', '91'], ['12', '21'], ['66'], ['55'], ['44'], ['34', '43'], ['9'],
                         ['67', '76'],
                         ['25', '52'], ['57', '75'], ['14', '41'], ['47', '74'], ['33'], ['49', '94'], ['23', '32'],
                         ['56', '65'],
                         ['15', '51'], ['4'], ['3'], ['27', '72'], ['17', '71'], ['59', '95'], ['69', '96'],
                         ['35', '53'], ['13', '31'],
                         ['45', '54'], ['11'], ['46', '64'], ['7'], ['5'], ['22'], ['79', '97'], ['6'],
                         [['16'], ['61']]]

        realname_item_dict = {}
        for id, key in enumerate(real_item_names):
            realname_item_dict[key] = real_item_ids[id]

        for item in real_item_names:
            if len(realname_item_dict[item]) == 2:
                df_item_complete[item] = df_item_complete[composite_item_dict[realname_item_dict[item][0]]] + \
                                         df_item_complete[composite_item_dict[realname_item_dict[item][1]]]
            else:
                try:
                    df_item_complete[item] = df_item_complete[composite_item_dict[realname_item_dict[item][0]]]
                except:
                    print(item)

        df_item_complete.drop(composite_item, axis=1, inplace=True)

    df1 = pd.read_csv('export_dataframe.csv')
    df1 = reformat_to(df1, "T", verbose=0)

    result = pd.concat([df_item_complete, df1], axis=1)
    result.to_csv('format_K_CON_UN_SENSO.csv', index=False)

    return result


def _reformat_U(df):
    tmp = pd.read_csv('format_T.csv')
    # tmp.insert(loc=tmp.shape[1]-1, column='last_round', value=df[["last_round"]])
    # tmp.insert(loc=tmp.shape[1]-1, column='lvl', value=df[["lvl"]])
    # tmp.insert(loc=tmp.shape[1]-1, column='time_eliminated', value=df[["time_eliminated"]])
    # tmp.insert(loc=tmp.shape[1]-1, column='total_damage', value=df[["total_damage"]])

    return tmp


def _reformat_X(df):
    if False:
        df = df[["aug1", "aug2", "aug3"]]
        aug_list = df[["aug1"]].values.flatten().tolist()
        aug_list.extend(df[["aug2"]].values.flatten())
        aug_list.extend(df[["aug3"]].values.flatten())

        aug_list = list(set(aug_list))
        aug_list.remove('0')

        for aug in aug_list:
            # print(df.loc[df['unit1'] == champ, 'tier1'].values)
            # print(df.loc[df['unit2'] == champ, 'tier2'].values)

            aug_oc = np.empty((df.shape[0], 212))

            for i in range(1, 4):
                oc = df.loc[df['aug' + str(i)] == aug, 'aug' + str(i)].reindex(
                    list(range(df.index.min(), df.index.max() + 1)), fill_value=0)

                for idx, a in enumerate(oc):
                    if a != 0:
                        oc[idx] = 1
                aug_oc[:, i - 1] = oc

            tier_champ = np.amax(aug_oc, axis=1)
            df.insert(loc=df.shape[1], column=aug, value=tier_champ)

        print(df.head())
        df = df.loc[:, ~df.columns.isin(['aug1', 'aug2', 'aug3'])]

        df.to_csv('format_X.csv', index=False)

        # df1 = df
        # df = reformat_to(format="X", verbose=0)
        # df.insert(loc=df.shape[1]-1, column=df1.columns[92:304], value=df1[92:304])
    else:
        df = pd.read_csv('format_X.csv')

    df1 = pd.read_csv('export_dataframe.csv')
    df1 = reformat_to(df1, "T", verbose=0)

    result = pd.concat([df, df1], axis=1)

    return result


def _reformat_od(df):
    real_item_names = ["TacticiansCrow", "RunaansHurricane", "Morellonomicon", "LastWhisper", "IonicSpark",
                       "RecurveBow", "B.F.Sword", "WarmogsArmor", "ThiefsGloves", "StatikkShiv",
                       "JeweledGauntlet", "InfinityEdge", "EvilGiantslayer", "DragonsClaw", "BrambleVest",
                       "BlueBuff", "ArchangelsStaff", "SparringGloves", "Zephyr", "TitansResolve",
                       "SunfireCape", "SpearofShojin", "Redemption", "RabadonsDeathcap", "HandofJustice",
                       "GuinsoosRageblade", "GargoyleStoneplate", "EdgeofNight", "TearoftheGoddess",
                       "NeedlesslyLargeRod", "ZzRotPortal", "ZekesHerald", "ShroudofStillness", "Quicksilver",
                       "LocketoftheIronSolari", "HextechGunblade", "FrozenHeart", "Deathblade",
                       "ChaliceofPower", "GiantsBelt", "ChainVest", "RapidFirecannon", "BansheesClaw",
                       "NegatronCloak", "Bloodthirster"]

    real_item_ids = [['88'], ['27', '72'], ['37', '73'], ['29', '92'], ['36', '63'], ['2'], ['1'], ['77'], ['99'],
                     ['24', '42'],
                     ['39', '93'], ['19', '91'], ['12', '21'], ['66'], ['55'], ['44'], ['34', '43'], ['9'],
                     ['67', '76'],
                     ['25', '52'], ['57', '75'], ['14', '41'], ['47', '74'], ['33'], ['49', '94'], ['23', '32'],
                     ['56', '65'],
                     ['15', '51'], ['4'], ['3'], ['27', '72'], ['17', '71'], ['59', '95'], ['69', '96'],
                     ['35', '53'], ['13', '31'],
                     ['45', '54'], ['11'], ['46', '64'], ['7'], ['5'], ['22'], ['79', '97'], ['6'], ['16', '61']]

    realname_item_dict = {}
    for id, key in enumerate(real_item_ids):
        for sas in key:
            realname_item_dict[sas] = real_item_names[id]

    placement = df[["placement"]]

    champ_list = df[["unit1"]].values.flatten().tolist()
    champ_list.extend(df[["unit2"]].values.flatten())
    champ_list.extend(df[["unit3"]].values.flatten())
    champ_list.extend(df[["unit4"]].values.flatten())
    champ_list.extend(df[["unit5"]].values.flatten())
    champ_list.extend(df[["unit6"]].values.flatten())
    champ_list.extend(df[["unit7"]].values.flatten())
    champ_list.extend(df[["unit8"]].values.flatten())
    champ_list.extend(df[["unit9"]].values.flatten())
    champ_list.extend(df[["unit10"]].values.flatten())
    champ_list.extend(df[["unit11"]].values.flatten())

    champ_list = list(set(champ_list))
    champ_list.remove('0')

    df_merged = pd.DataFrame.copy(df, deep=True)

    for champ in champ_list:
        # print(df.loc[df['unit1'] == champ, 'tier1'].values)
        # print(df.loc[df['unit2'] == champ, 'tier2'].values)

        champ_oc = np.empty((df.shape[0], 11))
        item1 = np.empty((df.shape[0], 11))
        item2 = np.empty((df.shape[0], 11))
        item3 = np.empty((df.shape[0], 11))

        for i in range(1, 12):
            ch = df.loc[df['unit' + str(i)] == champ, 'tier' + str(i)].reindex(
                list(range(df.index.min(), df.index.max() + 1)), fill_value=0)
            obj_1 = df.loc[df['unit' + str(i)] == champ, 'item1_' + str(i)].reindex(
                list(range(df.index.min(), df.index.max() + 1)), fill_value=0)
            obj_2 = df.loc[df['unit' + str(i)] == champ, 'item2_' + str(i)].reindex(
                list(range(df.index.min(), df.index.max() + 1)), fill_value=0)
            obj_3 = df.loc[df['unit' + str(i)] == champ, 'item3_' + str(i)].reindex(
                list(range(df.index.min(), df.index.max() + 1)), fill_value=0)

            champ_oc[:, i - 1] = ch
            item1[:, i - 1] = obj_1
            item2[:, i - 1] = obj_2
            item3[:, i - 1] = obj_3

        tier_champ = np.amax(champ_oc, axis=1)
        real_items = [np.amax(item, axis=1) for item in [item1, item2, item3]]

        suus = np.column_stack((real_items[0], real_items[1], real_items[2]))

        squarer = lambda t: realname_item_dict[str(int(t))] if str(int(t)) in realname_item_dict.keys() else ""
        vfunc = np.vectorize(squarer)
        suus = vfunc(suus)

        suus = np.sort(suus, axis=1)
        items = np.char.add(np.char.add(suus[:, 0], suus[:, 1]), suus[:, 2])

        Fix_Thief = lambda t: "ThiefsGloves" if "ThiefsGloves" in str(t) else t
        vfunc = np.vectorize(Fix_Thief)
        items = vfunc(items)

        Fix_Empty = lambda t: "0" if "" == str(t) else t
        vfunc = np.vectorize(Fix_Empty)
        items = vfunc(items)

        df.insert(loc=df.shape[1], column=champ, value=tier_champ)
        df.insert(loc=df.shape[1], column=champ + '_items', value=items)

        merged = np.char.add(tier_champ.astype(int).astype(str),
                             np.char.add(np.char.add(suus[:, 0], suus[:, 1]), suus[:, 2]))
        df_merged.insert(loc=df_merged.shape[1], column=champ, value=merged)

        print(champ)

    df.to_csv('format_od.csv', index=False)
    df_merged.to_csv('format_og.csv', index=False)

    df1 = pd.read_csv('export_dataframe.csv')
    df1 = reformat_to(df1, "T", verbose=0)

    result = pd.concat([df, df1], axis=1)
    result.to_csv('format_od_fix_sense.csv', index=False)

    result = pd.concat([df_merged, df1], axis=1)
    result.to_csv('format_og_fix_sense.csv', index=False)

    return result


def _reformat_og(df):
    real_item_names = ["TacticiansCrow", "RunaansHurricane", "Morellonomicon", "LastWhisper", "IonicSpark",
                       "RecurveBow", "B.F.Sword", "WarmogsArmor", "ThiefsGloves", "StatikkShiv",
                       "JeweledGauntlet", "InfinityEdge", "EvilGiantslayer", "DragonsClaw", "BrambleVest",
                       "BlueBuff", "ArchangelsStaff", "SparringGloves", "Zephyr", "TitansResolve",
                       "SunfireCape", "SpearofShojin", "Redemption", "RabadonsDeathcap", "HandofJustice",
                       "GuinsoosRageblade", "GargoyleStoneplate", "EdgeofNight", "TearoftheGoddess",
                       "NeedlesslyLargeRod", "ZzRotPortal", "ZekesHerald", "ShroudofStillness", "Quicksilver",
                       "LocketoftheIronSolari", "HextechGunblade", "FrozenHeart", "Deathblade",
                       "ChaliceofPower", "GiantsBelt", "ChainVest", "RapidFirecannon", "BansheesClaw",
                       "NegatronCloak", "Bloodthirster"]

    real_item_ids = [['88'], ['27', '72'], ['37', '73'], ['29', '92'], ['36', '63'], ['2'], ['1'], ['77'], ['99'],
                     ['24', '42'],
                     ['39', '93'], ['19', '91'], ['12', '21'], ['66'], ['55'], ['44'], ['34', '43'], ['9'],
                     ['67', '76'],
                     ['25', '52'], ['57', '75'], ['14', '41'], ['47', '74'], ['33'], ['49', '94'], ['23', '32'],
                     ['56', '65'],
                     ['15', '51'], ['4'], ['3'], ['27', '72'], ['17', '71'], ['59', '95'], ['69', '96'],
                     ['35', '53'], ['13', '31'],
                     ['45', '54'], ['11'], ['46', '64'], ['7'], ['5'], ['22'], ['79', '97'], ['6'], ['16''61']]

    item_type_dict = {"TacticiansCrow": "Utility",
                      "RunaansHurricane": "AttackDamage",
                      "Morellonomicon": "Utility",
                      "LastWhisper": "AttackDamage",
                      "IonicSpark": "Tank",
                      "WarmogsArmor": "Tank",
                      "ThiefsGloves": "Utility",
                      "StatikkShiv": "AbilityPower",
                      "JeweledGauntlet": "AbilityPower",
                      "InfinityEdge": "AttackDamage",
                      "EvilGiantslayer": "AttackDamage",
                      "DragonsClaw": "Tank",
                      "BrambleVest": "Tank",
                      "BlueBuff": "AbilityPower",
                      "ArchangelsStaff": "AbilityPower",
                      "Zephyr": "Utility",
                      "TitansResolve": "Tank",
                      "SunfireCape": "Tank",
                      "SpearofShojin": "AbilityPower",
                      "Redemption": "Tank",
                      "RabadonsDeathcap": "AbilityPower",
                      "HandofJustice": "Utility",
                      "GuinsoosRageblade": "AttackDamage",
                      "GargoyleStoneplate": "Tank",
                      "EdgeofNight": "Utility",
                      "ZzRotPortal": "Utility",
                      "ZekesHerald": "Support",
                      "ShroudofStillness": "Utility",
                      "Quicksilver": "Utility",
                      "LocketoftheIronSolari": "Support",
                      "HextechGunblade": "AbilityPower",
                      "FrozenHeart": "Utility",
                      "Deathblade": "AttackDamage",
                      "ChaliceofPower": "Support",
                      "RapidFirecannon": "AttackDamage",
                      "BansheesClaw": "Support",
                      "Bloodthirster": "AttackDamage"}

    support_mask = {"": 0,
                    "TacticiansCrow": 0,
                    "RunaansHurricane": 0,
                    "Morellonomicon": 0,
                    "LastWhisper": 0,
                    "IonicSpark": 0,
                    "WarmogsArmor": 0,
                    "ThiefsGloves": 0,
                    "StatikkShiv": 0,
                    "JeweledGauntlet": 0,
                    "InfinityEdge": 0,
                    "EvilGiantslayer": 0,
                    "DragonsClaw": 0,
                    "BrambleVest": 0,
                    "BlueBuff": 0,
                    "ArchangelsStaff": 0,
                    "Zephyr": 0,
                    "TitansResolve": 0,
                    "SunfireCape": 0,
                    "SpearofShojin": 0,
                    "Redemption": 0,
                    "RabadonsDeathcap": 0,
                    "HandofJustice": 0,
                    "GuinsoosRageblade": 0,
                    "GargoyleStoneplate": 0,
                    "EdgeofNight": 0,
                    "ZzRotPortal": 0,
                    "ZekesHerald": 1,
                    "ShroudofStillness": 0,
                    "Quicksilver": 0,
                    "LocketoftheIronSolari": 1,
                    "HextechGunblade": 0,
                    "FrozenHeart": 0,
                    "Deathblade": 0,
                    "ChaliceofPower": 1,
                    "RapidFirecannon": 0,
                    "BansheesClaw": 1,
                    "Bloodthirster": 0}

    utility_mask = {"TacticiansCrow": 1,
                    "RunaansHurricane": 0,
                    "Morellonomicon": 1,
                    "LastWhisper": 0,
                    "IonicSpark": 0,
                    "WarmogsArmor": 0,
                    "ThiefsGloves": 1,
                    "StatikkShiv": 0,
                    "JeweledGauntlet": 0,
                    "InfinityEdge": 0,
                    "EvilGiantslayer": 0,
                    "DragonsClaw": 0,
                    "BrambleVest": 0,
                    "BlueBuff": 0,
                    "ArchangelsStaff": 0,
                    "Zephyr": 1,
                    "TitansResolve": 0,
                    "SunfireCape": 0,
                    "SpearofShojin": 0,
                    "Redemption": 0,
                    "RabadonsDeathcap": 0,
                    "HandofJustice": 1,
                    "GuinsoosRageblade": 0,
                    "GargoyleStoneplate": 0,
                    "EdgeofNight": 1,
                    "ZzRotPortal": 1,
                    "ZekesHerald": 0,
                    "ShroudofStillness": 1,
                    "Quicksilver": 1,
                    "LocketoftheIronSolari": 0,
                    "HextechGunblade": 0,
                    "FrozenHeart": 1,
                    "Deathblade": 0,
                    "ChaliceofPower": 0,
                    "RapidFirecannon": 0,
                    "BansheesClaw": 0,
                    "Bloodthirster": 0}

    ad_mask = {"TacticiansCrow": 0,
               "RunaansHurricane": 1,
               "Morellonomicon": 0,
               "LastWhisper": 1,
               "IonicSpark": 0,
               "WarmogsArmor": 0,
               "ThiefsGloves": 0,
               "StatikkShiv": 0,
               "JeweledGauntlet": 0,
               "InfinityEdge": 1,
               "EvilGiantslayer": 1,
               "DragonsClaw": 0,
               "BrambleVest": 0,
               "BlueBuff": 0,
               "ArchangelsStaff": 0,
               "Zephyr": 0,
               "TitansResolve": 0,
               "SunfireCape": 0,
               "SpearofShojin": 0,
               "Redemption": 0,
               "RabadonsDeathcap": 0,
               "HandofJustice": 0,
               "GuinsoosRageblade": 1,
               "GargoyleStoneplate": 0,
               "EdgeofNight": 0,
               "ZzRotPortal": 0,
               "ZekesHerald": 0,
               "ShroudofStillness": 0,
               "Quicksilver": 0,
               "LocketoftheIronSolari": 0,
               "HextechGunblade": 0,
               "FrozenHeart": 0,
               "Deathblade": 1,
               "ChaliceofPower": 0,
               "RapidFirecannon": 1,
               "BansheesClaw": 0,
               "Bloodthirster": 1}

    ap_mask = {"TacticiansCrow": 0,
               "RunaansHurricane": 0,
               "Morellonomicon": 0,
               "LastWhisper": 0,
               "IonicSpark": 0,
               "WarmogsArmor": 0,
               "ThiefsGloves": 0,
               "StatikkShiv": 1,
               "JeweledGauntlet": 1,
               "InfinityEdge": 0,
               "EvilGiantslayer": 0,
               "DragonsClaw": 0,
               "BrambleVest": 0,
               "BlueBuff": 1,
               "ArchangelsStaff": 1,
               "Zephyr": 0,
               "TitansResolve": 0,
               "SunfireCape": 0,
               "SpearofShojin": 1,
               "Redemption": 0,
               "RabadonsDeathcap": 1,
               "HandofJustice": 0,
               "GuinsoosRageblade": 0,
               "GargoyleStoneplate": 0,
               "EdgeofNight": 0,
               "ZzRotPortal": 0,
               "ZekesHerald": 0,
               "ShroudofStillness": 0,
               "Quicksilver": 0,
               "LocketoftheIronSolari": 0,
               "HextechGunblade": 1,
               "FrozenHeart": 0,
               "Deathblade": 0,
               "ChaliceofPower": 0,
               "RapidFirecannon": 0,
               "BansheesClaw": 0,
               "Bloodthirster": 0}

    tank_mask = {"TacticiansCrow": 0,
                 "RunaansHurricane": 0,
                 "Morellonomicon": 0,
                 "LastWhisper": 0,
                 "IonicSpark": 1,
                 "WarmogsArmor": 1,
                 "ThiefsGloves": 0,
                 "StatikkShiv": 0,
                 "JeweledGauntlet": 0,
                 "InfinityEdge": 0,
                 "EvilGiantslayer": 0,
                 "DragonsClaw": 1,
                 "BrambleVest": 1,
                 "BlueBuff": 0,
                 "ArchangelsStaff": 0,
                 "Zephyr": 0,
                 "TitansResolve": 1,
                 "SunfireCape": 1,
                 "SpearofShojin": 0,
                 "Redemption": 1,
                 "RabadonsDeathcap": 0,
                 "HandofJustice": 0,
                 "GuinsoosRageblade": 0,
                 "GargoyleStoneplate": 1,
                 "EdgeofNight": 0,
                 "ZzRotPortal": 0,
                 "ZekesHerald": 0,
                 "ShroudofStillness": 0,
                 "Quicksilver": 0,
                 "LocketoftheIronSolari": 0,
                 "HextechGunblade": 0,
                 "FrozenHeart": 0,
                 "Deathblade": 0,
                 "ChaliceofPower": 0,
                 "RapidFirecannon": 0,
                 "BansheesClaw": 0,
                 "Bloodthirster": 0}

    realname_item_dict = {}
    for id, key in enumerate(real_item_ids):
        for sas in key:
            realname_item_dict[sas] = real_item_names[id]

    placement = df[["placement"]]

    champ_list = df[["unit1"]].values.flatten().tolist()
    champ_list.extend(df[["unit2"]].values.flatten())
    champ_list.extend(df[["unit3"]].values.flatten())
    champ_list.extend(df[["unit4"]].values.flatten())
    champ_list.extend(df[["unit5"]].values.flatten())
    champ_list.extend(df[["unit6"]].values.flatten())
    champ_list.extend(df[["unit7"]].values.flatten())
    champ_list.extend(df[["unit8"]].values.flatten())
    champ_list.extend(df[["unit9"]].values.flatten())
    champ_list.extend(df[["unit10"]].values.flatten())
    champ_list.extend(df[["unit11"]].values.flatten())

    champ_list = list(set(champ_list))
    champ_list.remove('0')

    for champ in champ_list:
        # print(df.loc[df['unit1'] == champ, 'tier1'].values)
        # print(df.loc[df['unit2'] == champ, 'tier2'].values)

        champ_oc = np.empty((df.shape[0], 11))
        item1 = np.empty((df.shape[0], 11))
        item2 = np.empty((df.shape[0], 11))
        item3 = np.empty((df.shape[0], 11))

        for i in range(1, 12):
            ch = df.loc[df['unit' + str(i)] == champ, 'tier' + str(i)].reindex(
                list(range(df.index.min(), df.index.max() + 1)), fill_value=0)
            obj_1 = df.loc[df['unit' + str(i)] == champ, 'item1_' + str(i)].reindex(
                list(range(df.index.min(), df.index.max() + 1)), fill_value=0)
            obj_2 = df.loc[df['unit' + str(i)] == champ, 'item2_' + str(i)].reindex(
                list(range(df.index.min(), df.index.max() + 1)), fill_value=0)
            obj_3 = df.loc[df['unit' + str(i)] == champ, 'item3_' + str(i)].reindex(
                list(range(df.index.min(), df.index.max() + 1)), fill_value=0)

            champ_oc[:, i - 1] = ch
            item1[:, i - 1] = obj_1
            item2[:, i - 1] = obj_2
            item3[:, i - 1] = obj_3

        tier_champ = np.amax(champ_oc, axis=1)
        real_items = [np.amax(item, axis=1) for item in [item1, item2, item3]]

        suus = np.column_stack((real_items[0], real_items[1], real_items[2]))

        squarer = lambda t: realname_item_dict[str(int(t))] if str(int(t)) in realname_item_dict.keys() else ""
        vfunc = np.vectorize(squarer)
        suus = vfunc(suus)

        support_lambda = lambda t: support_mask[str(t)] if str(t) in support_mask.keys() else 0
        vfunc = np.vectorize(support_lambda)
        support_item = np.sum(vfunc(suus), axis=1)

        tank_lambda = lambda t: tank_mask[str(t)] if str(t) in tank_mask.keys() else 0
        vfunc = np.vectorize(tank_lambda)
        tank_item = np.sum(vfunc(suus), axis=1)

        utility_lambda = lambda t: utility_mask[str(t)] if str(t) in utility_mask.keys() else 0
        vfunc = np.vectorize(utility_lambda)
        utility_item = np.sum(vfunc(suus), axis=1)

        ap_lambda = lambda t: ap_mask[str(t)] if str(t) in ap_mask.keys() else 0
        vfunc = np.vectorize(ap_lambda)
        ap_item = np.sum(vfunc(suus), axis=1)

        ad_lambda = lambda t: ad_mask[str(t)] if str(t) in ad_mask.keys() else 0
        vfunc = np.vectorize(ad_lambda)
        ad_item = np.sum(vfunc(suus), axis=1)

        df.insert(loc=df.shape[1], column=champ, value=tier_champ)
        df.insert(loc=df.shape[1], column=champ + '_Support', value=support_item)
        df.insert(loc=df.shape[1], column=champ + '_Tank', value=tank_item)
        df.insert(loc=df.shape[1], column=champ + '_AttackDamage', value=ad_item)
        df.insert(loc=df.shape[1], column=champ + '_AbilityPower', value=ap_item)
        df.insert(loc=df.shape[1], column=champ + '_Utility', value=utility_item)

        print(champ)

    df.to_csv('format_og.csv', index=False)

    df1 = pd.read_csv('export_dataframe.csv')
    df1 = reformat_to(df1, "T", verbose=0)

    result = pd.concat([df, df1], axis=1)
    result.to_csv('format_og_fix_sense.csv', index=False)

    return result


def reformat_to(df, format="A", verbose=0, two_class=False):
    if verbose == 1:
        print(df.columns.values)
        print("df:\n", df.head())  # first x-row
        print(df.shape)

    if format == "A":
        df = _reformat_A(df)
    elif format == "B":
        df = _reformat_B(df)
    elif format == "C":
        df = _reformat_C(df)
    elif format == "D":
        df = _reformat_D(df)
    elif format == "V":
        df = _reformat_V(df)
    elif format == "I":
        df = _reformat_I(df)
    elif format == "T":
        df = _reformat_T(df)
    elif format == "U":
        df = _reformat_U(df)
    elif format == "X":
        df = _reformat_X(df)
    elif format == "K":
        df = _reformat_K(df)
    elif format == "Z":
        df = _reformat_Z(df)
    elif format == "od":
        df = _reformat_od(df)
    elif format == "og":
        df = _reformat_og(df)
    else:
        df = _reformat_E(df)

    if two_class:
        df.loc[df['placement'] <= 4, ['placement']] = 1
        df.loc[df['placement'] > 4, ['placement']] = 0

    if verbose:
        print("\n\n\n ************************** START reformat", str(format), "**************************")
        print(df.columns.values)
        print("df:\n", df.head())  # first x-row
        print(df.shape)
    return df


if __name__ == "__main__":
    dataset = pd.read_csv('export_dataframe.csv')

    # dataset = reformat_to(dataset, "A", verbose=1)
    #
    # ## dataset = reformat_to(dataset, "B", verbose=1)
    #
    # dataset = reformat_to(dataset, "C", verbose=1)
    #
    # dataset = reformat_to(dataset, "D", verbose=1)
    #
    # dataset = reformat_to(dataset, "T", verbose=1)

    dataset = reformat_to(dataset, "og", verbose=1, two_class=True)
