# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 12:02:46 2021

@author: Dr. Birko-Katarina Ruzicka
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter
from collections import defaultdict


# =============================================================================
# If dataframes already exist (shortcut for if script was run before):
# =============================================================================

tos_df = pd.read_csv('tos_df_cleaned.csv', index_col=0)
tas_df = pd.read_csv('tas_df_cleaned.csv', index_col=0)
tng_df = pd.read_csv('tng_df_cleaned.csv', index_col=0)
ds9_df = pd.read_csv('ds9_df_cleaned.csv', index_col=0)
voy_df = pd.read_csv('voy_df_cleaned.csv', index_col=0)
ent_df = pd.read_csv('ent_df_cleaned.csv', index_col=0)
dis_df = pd.read_csv('dis_df_cleaned.csv', index_col=0)
pic_df = pd.read_csv('pic_df_cleaned.csv', index_col=0)
st_df = pd.read_csv('st_df_cleaned.csv', index_col=0)

# =============================================================================
# If this script is being run for the first time:
# =============================================================================

with open('improved_dataset/StarTrekDialogue.json', 'r') as read_file:
    all_series = json.load(read_file)
del(read_file)
    
tos = all_series['TOS']
tas = all_series['TAS']
tng = all_series['TNG']
ds9 = all_series['DS9']
voy = all_series['VOY']
ent = all_series['ENT']
dis = all_series['DIS']
pic = all_series['PIC']
st = []


def generate_dataframe(series: dict) -> pd.DataFrame:
    '''
    Takes a dictionary of episodes and converts it to a dataframe with
    additional data.
    Accepted inputs: tos, tas, tng, ds9, voy, ent
    Also accepts input 'st' to create one dataframe from all series
    '''
    
    if series not in [tos, tas, tng, ds9, voy, ent, dis, pic, st]:
        print('Series abbreviation must be one of the following:')
        print("tos, tas, tng, ds9, voy, ent, dis, pic, st")
    else:
        pass
    

    if series == tos:
        # Transform dict -> series -> dataframe:
        tos_series = pd.concat({k: pd.Series(v) for k, v in tos.items()})
        tos_df = pd.Series.to_frame(tos_series).reset_index()
        tos_df.columns = ['Episode', 'Character', 'Lines']

        # remove entries where Linecount < 10 except for main cast:
        tos_df['Linecount'] = tos_df['Lines'].str.len()
        tos_main_cast = ['KIRK', 'SPOCK', 'UHURA', 'CHEKOV', 'SULU', 'CHAPEL',
                         'COMPUTER', 'MCKOY', 'SCOTT']
        for index in tos_df.index:
            if tos_df.at[index, 'Linecount'] < 10 \
               and not tos_df.at[index, 'Character'] in tos_main_cast:
                tos_df.drop(index, axis=0, inplace=True)

        tos_df.at[2, 'Character'] = 'NUMBER ONE'
        tos_df.at[23, 'Character'] = 'NANCY CRATER'
        tos_df.at[33, 'Character'] = 'JANICE RAND'
        tos_df.at[42, 'Character'] = 'JANICE RAND'
        tos_df.at[87, 'Character'] = 'JANICE RAND'
        tos_df.at[130, 'Character'] = 'JANICE RAND'
        tos_df.at[238, 'Character'] = 'ROMULAN COMMANDER 1'
        tos_df.at[881, 'Character'] = 'ROMULAN COMMANDER 2'
        tos_df.at[523, 'Character'] = 'MARTHA LANDON'
        tos_df.at[568, 'Character'] = 'ALICE'
        tos_df.at[596, 'Character'] = 'NANCY HEDFORD'
        tos_df.at[681, 'Character'] = 'CYRANO JONES'
        tos_df.at[703, 'Character'] = 'PROVIDER ONE'
        tos_df.at[704, 'Character'] = 'PROVIDER TWO'
        tos_df.at[705, 'Character'] = 'PROVIDER THREE'
        tos_df.at[908, 'Character'] = 'STARNES'
        tos_df.at[929, 'Character'] = 'MIRANDA JONES'
        tos_df.at[1173, 'Character'] = 'JANICE LESTER'


        # Add additional columns (from manually created CSV files)
        tos_data = pd.read_csv('additional_data/tos_data.csv',
                               index_col=0, delimiter=';')
        tos_df = tos_df.merge(tos_data, left_on='Episode', right_index=True)
        
        tos_gender = pd.read_csv('additional_data/tos_gender.csv',
                                 header=None, index_col=0, squeeze=True,
                                 delimiter=';').to_dict()
        tos_df['Gender'] = tos_df['Character'].map(tos_gender)
        
        tos_df = tos_df[['Episode', 'Season', 'Year', 'Title', 'Character',
                         'Gender', 'Lines', 'Linecount']]

        tos_df.to_csv('tos_df_cleaned.csv')

        return tos_df
    
    if series == tas:
        # Transform dict -> series -> dataframe:
        tas_series = pd.concat({k: pd.Series(v) for k, v in tas.items()})
        tas_df = pd.Series.to_frame(tas_series).reset_index()
        tas_df.columns = ['Episode', 'Character', 'Lines']

        # remove entries where Linecount < 10 except for main cast:
        tas_df['Linecount'] = tas_df['Lines'].str.len()
        tas_main_cast = ['KIRK', 'SPOCK', 'UHURA', 'CHEKOV', 'SULU', 'CHAPEL',
                         'COMPUTER', 'MCKOY', 'SCOTT']
        for index in tas_df.index:
            if tas_df.at[index, 'Linecount'] < 10 \
               and not tas_df.at[index, 'Character'] in tas_main_cast:
                tas_df.drop(index, axis=0, inplace=True)

        tas_df.at[21, 'Character'] = 'SPOCK'


        # Add additional columns (from manually created CSV files)
        tas_data = pd.read_csv('additional_data/tas_data.csv',
                               index_col=0, delimiter=';')
        tas_df = tas_df.merge(tas_data, left_on='Episode', right_index=True)
        
        tas_gender = pd.read_csv('additional_data/tas_gender.csv',
                                 header=None, index_col=0, squeeze=True,
                                 delimiter=';').to_dict()
        tas_df['Gender'] = tas_df['Character'].map(tas_gender)
        
        tas_df = tas_df[['Episode', 'Season', 'Year', 'Title', 'Character',
                         'Gender', 'Lines', 'Linecount']]

        tas_df.to_csv('tas_df_cleaned.csv')

        return tas_df

    if series == tng:
        # Transform dict -> series -> dataframe:
        tng_series = pd.concat({k: pd.Series(v) for k, v in tng.items()})
        tng_df = pd.Series.to_frame(tng_series).reset_index()
        tng_df.columns = ['Episode', 'Character', 'Lines']

        # remove entries where Linecount < 10 except for main cast:
        tng_df['Linecount'] = tng_df['Lines'].str.len()
        tng_main_cast = ['PICARD', 'RIKER', 'WORF', 'DATA', 'TROI', 'CRUSHER',
                         'TASHA', 'CHIEF', "O'BRIEN", 'GUINAN', 'LAFORGE',
                         'PULASKI', 'WESLEY']
        for index in tng_df.index:
            if tng_df.at[index, 'Linecount'] < 10 \
               and not tng_df.at[index, 'Character'] in tng_main_cast:
                tng_df.drop(index, axis=0, inplace=True)

        tng_df.at[628, 'Character'] = 'KYLE RIKER'
        tng_df.at[1722, 'Character'] = 'MISS KYLE'
        tng_df.at[2058, 'Character'] = 'PICARD'
        tng_df.at[2061, 'Character'] = 'RO'
        tng_df.at[2062, 'Character'] = 'GUINAN'
        tng_df.at[2064, 'Character'] = 'KEIKO'
        tng_df.at[2085, 'Character'] = 'DATA'
        tng_df.at[2316, 'Character'] = 'RIKER'
        tng_df.at[2594, 'Character'] = 'DATA'
        tng_df.at[2634, 'Character'] = 'NECHAYEV'


        # Add additional columns (from manually created CSV files)
        tng_data = pd.read_csv('additional_data/tng_data.csv',
                               index_col=0, delimiter=';')
        tng_df = tng_df.merge(tng_data, left_on='Episode', right_index=True)
        
        tng_gender = pd.read_csv('additional_data/tng_gender.csv',
                                 header=None, index_col=0, squeeze=True,
                                 delimiter=';').to_dict()
        tng_df['Gender'] = tng_df['Character'].map(tng_gender)
        
        tng_df = tng_df[['Episode', 'Season', 'Year', 'Title', 'Character',
                         'Gender', 'Lines', 'Linecount']]

        tng_df.to_csv('tng_df_cleaned.csv')

        return tng_df

    if series == ds9:
        # Transform dict -> series -> dataframe:
        ds9_series = pd.concat({k: pd.Series(v) for k, v in ds9.items()})
        ds9_df = pd.Series.to_frame(ds9_series).reset_index()
        ds9_df.columns = ['Episode', 'Character', 'Lines']

        # remove entries where Linecount < 10 except for main cast:
        ds9_df['Linecount'] = ds9_df['Lines'].str.len()
        ds9_main_cast = ['SISKO', 'ODO', 'KIRA', 'JAKE', 'QUARK', 'DAX',
                         "O'BRIEN", 'BASHIR', 'WORF', 'EZRI']
        for index in ds9_df.index:
            if ds9_df.at[index, 'Linecount'] < 10 \
               and not ds9_df.at[index, 'Character'] in ds9_main_cast:
                ds9_df.drop(index, axis=0, inplace=True)

        ds9_df.at[260, 'Character'] = 'DAX'
        ds9_df.at[618, 'Character'] = 'GUL EVEK'
        ds9_df.at[635, 'Character'] = 'NECHAYEV'
        ds9_df.at[1740, 'Character'] = 'BASHIR'


        # Add additional columns (from manually created CSV files)
        ds9_data = pd.read_csv('additional_data/ds9_data.csv',
                               index_col=0, delimiter=';')
        ds9_df = ds9_df.merge(ds9_data, left_on='Episode', right_index=True)
        
        ds9_gender = pd.read_csv('additional_data/ds9_gender.csv',
                                 header=None, index_col=0, squeeze=True,
                                 delimiter=';').to_dict()
        ds9_df['Gender'] = ds9_df['Character'].map(ds9_gender)
        
        ds9_df = ds9_df[['Episode', 'Season', 'Year', 'Title', 'Character',
                         'Gender', 'Lines', 'Linecount']]

        ds9_df.to_csv('ds9_df_cleaned.csv')

        return ds9_df

    if series == voy:
        # Transform dict -> series -> dataframe:
        voy_series = pd.concat({k: pd.Series(v) for k, v in voy.items()})
        voy_df = pd.Series.to_frame(voy_series).reset_index()
        voy_df.columns = ['Episode', 'Character', 'Lines']

        # remove entries where Linecount < 10 except for main cast:
        voy_df['Linecount'] = voy_df['Lines'].str.len()
        voy_main_cast = ['JANEWAY', 'CHAKOTAY', 'TUVOK', 'PARIS', 'TORRES',
                         'KIM', 'EMH', 'NEELIX', 'KES', 'SEVEN', 'ICHEB',
                         'SESKA']
        for index in voy_df.index:
            if voy_df.at[index, 'Linecount'] < 10 \
               and not voy_df.at[index, 'Character'] in voy_main_cast:
                voy_df.drop(index, axis=0, inplace=True)

        voy_df.at[194, 'Character'] = 'TORRES'
        voy_df.at[499, 'Character'] = 'DANARA'
        voy_df.at[538, 'Character'] = 'JANEWAY'
        voy_df.at[539, 'Character'] = 'KIM'
        voy_df.at[540, 'Character'] = 'TORRES'
        voy_df.at[543, 'Character'] = 'EMH'
        voy_df.at[606, 'Character'] = 'DANARA'
        voy_df.at[855, 'Character'] = 'ADMIRAL E. JANEWAY'
        voy_df.at[1101, 'Character'] = 'GAUMEN'
        voy_df.at[1237, 'Character'] = 'ALPHA HIROGEN'
        voy_df.at[1238, 'Character'] = 'BETA HIROGEN'
        voy_df.at[1248, 'Character'] = 'ALPHA HIROGEN'
        voy_df.at[1339, 'Character'] = 'JANEWAY'
        voy_df.at[1342, 'Character'] = 'TUVOK'
        voy_df.at[1344, 'Character'] = 'CHAKOTAY'
        voy_df.at[1345, 'Character'] = 'EMH'
        voy_df.at[1585, 'Character'] = 'TUVOK'
        voy_df.at[1801, 'Character'] = 'TWO OF NINE'
        voy_df.at[1803, 'Character'] = 'THREE OF NINE'
        voy_df.at[1804, 'Character'] = 'FOUR OF NINE'
        voy_df.at[2377, 'Character'] = 'ALPHA HIROGEN'
        voy_df.at[2378, 'Character'] = 'BETA HIROGEN'
        voy_df.at[2388, 'Character'] = 'ALPHA HIROGEN'
        voy_df.at[2431, 'Character'] = 'TORRES'
        voy_df.at[2676, 'Character'] = 'ADMIRAL K. JANEWAY'
        voy_df = voy_df.drop(696, axis=0)  # "CROWD" is not a character
        voy_df = voy_df.drop(880, axis=0)  # "COOPERATIVE" is not a character


        # Add additional columns (from manually created CSV files)
        voy_data = pd.read_csv('additional_data/voy_data.csv',
                               index_col=0, delimiter=';')
        voy_df = voy_df.merge(voy_data, left_on='Episode', right_index=True)
        
        voy_gender = pd.read_csv('additional_data/voy_gender.csv',
                                 header=None, index_col=0, squeeze=True,
                                 delimiter=';').to_dict()
        voy_df['Gender'] = voy_df['Character'].map(voy_gender)
        
        voy_df = voy_df[['Episode', 'Season', 'Year', 'Title', 'Character',
                         'Gender', 'Lines', 'Linecount']]

        voy_df.to_csv('voy_df_cleaned.csv')

        return voy_df

    if series == ent:
        # Transform dict -> series -> dataframe:
        ent_series = pd.concat({k: pd.Series(v) for k, v in ent.items()})
        ent_df = pd.Series.to_frame(ent_series).reset_index()
        ent_df.columns = ['Episode', 'Character', 'Lines']

        # remove entries where Linecount < 10 except for main cast:
        ent_df['Linecount'] = ent_df['Lines'].str.len()
        ent_main_cast = ['ARCHER', 'DEGRA', 'HOSHI', 'PHLOX', 'REED', 'SHRAN',
                         "T'POL", 'TRAVIS', 'TUCKER']
        for index in ent_df.index:
            if ent_df.at[index, 'Linecount'] < 10 \
               and not ent_df.at[index, 'Character'] in ent_main_cast:
                ent_df.drop(index, axis=0, inplace=True)

        ent_df.at[108, 'Character'] = 'RIAAN'
        ent_df.at[742, 'Character'] = 'RIAAN'
        ent_df.at[800, 'Character'] = 'MACREADY'
        ent_df.at[900, 'Character'] = 'AMANDA COLE'
        ent_df.at[989, 'Character'] = "T'POL"


        # Add additional columns (from manually created CSV files)
        ent_data = pd.read_csv('additional_data/ent_data.csv',
                               index_col=0, delimiter=';')
        ent_df = ent_df.merge(ent_data, left_on='Episode', right_index=True)
        
        ent_gender = pd.read_csv('additional_data/ent_gender.csv',
                                 header=None, index_col=0, squeeze=True,
                                 delimiter=';').to_dict()
        ent_df['Gender'] = ent_df['Character'].map(ent_gender)
        
        ent_df = ent_df[['Episode', 'Season', 'Year', 'Title', 'Character',
                         'Gender', 'Lines', 'Linecount']]

        ent_df.to_csv('ent_df_cleaned.csv')

        return ent_df

    if series == dis:
        # Transform dict -> series -> dataframe:
        dis_series = pd.concat({k: pd.Series(v) for k, v in dis.items()})
        dis_df = pd.Series.to_frame(dis_series).reset_index()
        dis_df.columns = ['Episode', 'Character', 'Lines']

        # remove entries where Linecount < 10 except for main cast:
        dis_df.at[253, 'Character'] = 'STAMETS'
        dis_df.at[411, 'Character'] = 'NUMBER ONE'
        dis_df.at[623, 'Character'] = 'NUMBER ONE'
        dis_df.at[624, 'Character'] = 'NUMBER ONE'

        dis_df['Linecount'] = dis_df['Lines'].str.len()
        dis_main_cast = ['BURNHAM', 'SARU', 'VOQ', 'TYLER', 'STAMETS', 'TILLY',
                         'LORCA', 'CULBER', 'PIKE', 'BOOK', 'NHAN', 'ADIRA',
                         'GRAY', 'GEORGIOU', 'DETMER', 'OWOSEKUN', "L'RELL",
                         'SAREK', 'CORNWELL', 'AIRIAM', 'SPOCK']
        for index in dis_df.index:
            if dis_df.at[index, 'Linecount'] < 10 \
               and not dis_df.at[index, 'Character'] in dis_main_cast:
                dis_df.drop(index, axis=0, inplace=True)

        # Add additional columns (from manually created CSV files)
        dis_data = pd.read_csv('additional_data/dis_data.csv',
                               index_col=0, delimiter=';')
        dis_df = dis_df.merge(dis_data, left_on='Episode', right_index=True)
        
        dis_gender = pd.read_csv('additional_data/dis_gender.csv',
                                 header=None, index_col=0, squeeze=True,
                                 delimiter=';').to_dict()
        dis_df['Gender'] = dis_df['Character'].map(dis_gender)
        
        dis_df = dis_df[['Episode', 'Season', 'Year', 'Title', 'Character',
                         'Gender', 'Lines', 'Linecount']]

        dis_df.to_csv('dis_df_cleaned.csv')

        return dis_df
    
    if series == pic:
        # Transform dict -> series -> dataframe:
        pic_series = pd.concat({k: pd.Series(v) for k, v in pic.items()})
        pic_df = pd.Series.to_frame(pic_series).reset_index()
        pic_df.columns = ['Episode', 'Character', 'Lines']

        # remove entries where Linecount < 10 except for main cast:
        pic_df['Linecount'] = pic_df['Lines'].str.len()
        pic_main_cast = ['PICARD', 'AGNES', 'DAHJ', 'DATA', 'ELNOR', 'HUGH',
                         'SOJI', 'RAFFI', 'RIOS', 'NAREK', 'SEVEN', 'RIZZO']

        pic_df.at[28, 'Character'] = 'LARIS'
        pic_df.at[54, 'Character'] = 'ENOCH'
        pic_df.at[80, 'Character'] = 'EMMET'
        pic_df.at[104, 'Character'] = 'BJAYZL'
        pic_df.at[106, 'Character'] = 'BJAYZL'
        pic_df.at[148, 'Character'] = 'SOJI'

        for index in pic_df.index:
            if pic_df.at[index, 'Linecount'] < 10 \
               and not pic_df.at[index, 'Character'] in pic_main_cast:
                pic_df.drop(index, axis=0, inplace=True)

        # Add additional columns (from manually created CSV files)
        pic_data = pd.read_csv('additional_data/pic_data.csv',
                               index_col=0, delimiter=';')
        pic_df = pic_df.merge(pic_data, left_on='Episode', right_index=True)
        
        pic_gender = pd.read_csv('additional_data/pic_gender.csv',
                                 header=None, index_col=0, squeeze=True,
                                 delimiter=';').to_dict()
        pic_df['Gender'] = pic_df['Character'].map(pic_gender)
        
        pic_df = pic_df[['Episode', 'Season', 'Year', 'Title', 'Character',
                         'Gender', 'Lines', 'Linecount']]

        pic_df.to_csv('pic_df_cleaned.csv')

        return pic_df

    if series == st:  # note: all series dataframes must exist first!
        # initialize an empty DataFrame:
        st_df = pd.DataFrame()
        
        # create column 'Year' (= first aired in the US)
        st_df['Year'] = (
            list(tos_df['Year'])
            + list(tas_df['Year'])
            + list(tng_df['Year'])
            + list(ds9_df['Year'])
            + list(voy_df['Year'])
            + list(ent_df['Year'])
            + list(dis_df['Year'])
            + list(pic_df['Year']))
        years = list(np.unique(st_df['Year']))
        
        # create column 'Airdate' (= increase resolution relative to 'Year')
        airdate = []
        for y in years:
            x = list(
                np.linspace(y, y + 1, dict(st_df['Year'].value_counts())[y]))
            for e in x:
                airdate.append(e)
        st_df['Airdate'] = airdate
        
        # create column 'Episode'
        st_df['Episode'] = (
            list(tos_df['Episode'])
            + list(tas_df['Episode'])
            + list(tng_df['Episode'])
            + list(ds9_df['Episode'])
            + list(voy_df['Episode'])
            + list(ent_df['Episode'])
            + list(dis_df['Episode'])
            + list(pic_df['Episode']))
        st_df.drop_duplicates(['Episode'], keep='first', inplace=True)
        
        # create columns 'Char_male' and 'Char_female'
        char_male = defaultdict(int)
        char_female = defaultdict(int)
        for ep in list(st_df['Episode']):
            for i in tos_df.index:
                if tos_df['Episode'][i] == ep and tos_df['Gender'][i] == 'm':
                    char_male[ep] += 1
                elif tos_df['Episode'][i] == ep and tos_df['Gender'][i] == 'f':
                    char_female[ep] += 1
            for i in tas_df.index:
                if tas_df['Episode'][i] == ep and tas_df['Gender'][i] == 'm':
                    char_male[ep] += 1
                elif tas_df['Episode'][i] == ep and tas_df['Gender'][i] == 'f':
                    char_female[ep] += 1
            for i in tng_df.index:
                if tng_df['Episode'][i] == ep and tng_df['Gender'][i] == 'm':
                    char_male[ep] += 1
                elif tng_df['Episode'][i] == ep and tng_df['Gender'][i] == 'f':
                    char_female[ep] += 1
            for i in ds9_df.index:
                if ds9_df['Episode'][i] == ep and ds9_df['Gender'][i] == 'm':
                    char_male[ep] += 1
                elif ds9_df['Episode'][i] == ep and ds9_df['Gender'][i] == 'f':
                    char_female[ep] += 1
            for i in voy_df.index:
                if voy_df['Episode'][i] == ep and voy_df['Gender'][i] == 'm':
                    char_male[ep] += 1
                elif voy_df['Episode'][i] == ep and voy_df['Gender'][i] == 'f':
                    char_female[ep] += 1
            for i in ent_df.index:
                if ent_df['Episode'][i] == ep and ent_df['Gender'][i] == 'm':
                    char_male[ep] += 1
                elif ent_df['Episode'][i] == ep and ent_df['Gender'][i] == 'f':
                    char_female[ep] += 1
            for i in dis_df.index:
                if dis_df['Episode'][i] == ep and dis_df['Gender'][i] == 'm':
                    char_male[ep] += 1
                elif dis_df['Episode'][i] == ep and dis_df['Gender'][i] == 'f':
                    char_female[ep] += 1
            for i in pic_df.index:
                if pic_df['Episode'][i] == ep and pic_df['Gender'][i] == 'm':
                    char_male[ep] += 1
                elif pic_df['Episode'][i] == ep and pic_df['Gender'][i] == 'f':
                    char_female[ep] += 1
            if ep not in char_female:
                char_female[ep] = 0
        st_df['Char_male'] = st_df['Episode'].map(char_male)
        st_df['Char_female'] = st_df['Episode'].map(char_female)
        
        # create column 'Char_total'
        char_total = []
        for i in st_df.index:
            char_total.append(st_df['Char_male'][i] + st_df['Char_female'][i])
        st_df['Char_total'] = char_total
        
        # create columns 'Char_m_rel', 'Char_f_rel'
        char_m_rel, char_f_rel = [], []
        for i in st_df.index:
            char_m_rel.append(st_df['Char_male'][i] / st_df['Char_total'][i])
            char_f_rel.append(st_df['Char_female'][i] / st_df['Char_total'][i])
        st_df['Char_m_rel'] = char_m_rel
        st_df['Char_f_rel'] = char_f_rel
        
        # create columns 'Lines_male' and 'Lines_female'
        lines_male = defaultdict(int)
        lines_female = defaultdict(int)
        for ep in list(st_df['Episode']):
            for i in tos_df.index:
                if tos_df['Episode'][i] == ep and tos_df['Gender'][i] == 'm':
                    lines_male[ep] += tos_df['Linecount'][i]
                elif tos_df['Episode'][i] == ep and tos_df['Gender'][i] == 'f':
                    lines_female[ep] += tos_df['Linecount'][i]
            for i in tas_df.index:
                if tas_df['Episode'][i] == ep and tas_df['Gender'][i] == 'm':
                    lines_male[ep] += tas_df['Linecount'][i]
                elif tas_df['Episode'][i] == ep and tas_df['Gender'][i] == 'f':
                    lines_female[ep] += tas_df['Linecount'][i]
            for i in tng_df.index:
                if tng_df['Episode'][i] == ep and tng_df['Gender'][i] == 'm':
                    lines_male[ep] += tng_df['Linecount'][i]
                elif tng_df['Episode'][i] == ep and tng_df['Gender'][i] == 'f':
                    lines_female[ep] += tng_df['Linecount'][i]
            for i in ds9_df.index:
                if ds9_df['Episode'][i] == ep and ds9_df['Gender'][i] == 'm':
                    lines_male[ep] += ds9_df['Linecount'][i]
                elif ds9_df['Episode'][i] == ep and ds9_df['Gender'][i] == 'f':
                    lines_female[ep] += ds9_df['Linecount'][i]
            for i in voy_df.index:
                if voy_df['Episode'][i] == ep and voy_df['Gender'][i] == 'm':
                    lines_male[ep] += voy_df['Linecount'][i]
                elif voy_df['Episode'][i] == ep and voy_df['Gender'][i] == 'f':
                    lines_female[ep] += voy_df['Linecount'][i]
            for i in ent_df.index:
                if ent_df['Episode'][i] == ep and ent_df['Gender'][i] == 'm':
                    lines_male[ep] += ent_df['Linecount'][i]
                elif ent_df['Episode'][i] == ep and ent_df['Gender'][i] == 'f':
                    lines_female[ep] += ent_df['Linecount'][i]
            for i in dis_df.index:
                if dis_df['Episode'][i] == ep and dis_df['Gender'][i] == 'm':
                    lines_male[ep] += dis_df['Linecount'][i]
                elif dis_df['Episode'][i] == ep and dis_df['Gender'][i] == 'f':
                    lines_female[ep] += dis_df['Linecount'][i]
            for i in pic_df.index:
                if pic_df['Episode'][i] == ep and pic_df['Gender'][i] == 'm':
                    lines_male[ep] += pic_df['Linecount'][i]
                elif pic_df['Episode'][i] == ep and pic_df['Gender'][i] == 'f':
                    lines_female[ep] += pic_df['Linecount'][i]
            if ep not in lines_female:
                lines_female[ep] = 0
        
        st_df['Lines_male'] = st_df['Episode'].map(lines_male)
        st_df['Lines_female'] = st_df['Episode'].map(lines_female)
        
        # create column 'Lines_total'
        lines = []
        for i in st_df.index:
            lines.append(st_df['Lines_male'][i] + st_df['Lines_female'][i])
        st_df['Lines_total'] = lines
        
        # create columns 'Lines_m_rel', 'Lines_f_rel'
        lines_m_rel, lines_f_rel = [], []
        for i in st_df.index:
            lines_m_rel.append(st_df['Lines_male'][i]
                               / st_df['Lines_total'][i])
            lines_f_rel.append(st_df['Lines_female'][i]
                               / st_df['Lines_total'][i])
        st_df['Lines_m_rel'] = lines_m_rel
        st_df['Lines_f_rel'] = lines_f_rel
        
        st_df.to_csv('st_df_cleaned.csv')
        
        return st_df

# =============================================================================
# After creating dataframes: Analysis
# =============================================================================


def get_labels(dataframe):
    if 'tos_000' in list(dataframe['Episode']):
        series = 'The Original Series (TOS)'
        short = 'tos'
    elif 'tas_000' in list(dataframe['Episode']):
        series = 'The Animates Series (TAS)'
        short = 'tas'
    elif 'tng_000' in list(dataframe['Episode']):
        series = 'The Next Generation (TNG)'
        short = 'tng'
    elif 'ds9_000' in list(dataframe['Episode']):
        series = 'Deep Space Nine (DS9)'
        short = 'ds9'
    elif 'voy_000' in list(dataframe['Episode']):
        series = 'Star Trek Voyager (VOY)'
        short = 'voy'
    elif 'ent_000' in list(dataframe['Episode']):
        series = 'Star Trek Enterprise (ENT)'
        short = 'ent'
    elif 'dis_000' in list(dataframe['Episode']):
        series = 'Star Trek Discovery (DIS)'
        short = 'dis'
    elif 'pic_000' in list(dataframe['Episode']):
        series = 'Star Trek Picard (PIC)'
        short = 'pic'
    return series, short


def characters_by_gender(dataframe):
    print('Number of unique characters with speaking roles: ',
          dataframe['Character'].nunique(), '\n---')

    lines_by_char = defaultdict(np.int64)
    for i in dataframe.index:
        lines_by_char[dataframe['Character'][i]] += dataframe['Linecount'][i]
    
    print('Sum of lines spoken by everyone: ', sum(dataframe['Linecount']),
          '\n---')
    top10 = sorted(lines_by_char.items(), key=itemgetter(1), reverse=True)[:10]
    print('Most lines spoken by: \n')
    for i in top10:
        name, lines = i
        print(f'{name:{9}}: {lines: >{5}}')
    print('---')
    
    series, short = get_labels(dataframe)
    
    # Plot number of characters by gender, in total
    char_gender = {'m': [], 'f': [], 'n': []}
    for i in dataframe.index:
        if dataframe['Gender'][i] == 'm':
            char_gender['m'].append(dataframe['Character'][i])
        elif dataframe['Gender'][i] == 'f':
            char_gender['f'].append(dataframe['Character'][i])
        elif dataframe['Gender'][i] == 'n':
            char_gender['n'].append(dataframe['Character'][i])
    
    char_m = len(np.unique(char_gender['m']))
    char_f = len(np.unique(char_gender['f']))
    char_n = len(np.unique(char_gender['n']))
    
    plt.pie([char_m, char_f, char_n],
            labels=['male', 'female', 'genderneutral'],
            shadow=False, startangle=90,
            autopct='%1.0f%%',
            colors=['#0471CE', '#E52222', '#BBBBBB'])
            #colors=['#1A6384', '#5B1414', '#AD722C'])  # trekcolors
    plt.savefig(f'{short}_characters.png', dpi=150)

    # Plot number of characters by gender, per season
    seasons = list(dataframe['Season'].unique())
    char_gender_seasons = np.empty(len(seasons), dtype=dict)
    male, female, neutral = [], [], []

    for seasonnumber, season in enumerate(seasons):
        char_gender = {'m': [], 'f': [], 'n': []}
        for i in dataframe.index:
            if dataframe['Season'][i] == season:
                if dataframe['Gender'][i] == 'm':
                    char_gender['m'].append(dataframe['Character'][i])
                elif dataframe['Gender'][i] == 'f':
                    char_gender['f'].append(dataframe['Character'][i])
                elif dataframe['Gender'][i] == 'n':
                    char_gender['n'].append(dataframe['Character'][i])
        char_gender_seasons[seasonnumber] = char_gender
        male.append(len(np.unique(char_gender['m'])))
        female.append(len(np.unique(char_gender['f'])))
        neutral.append(len(np.unique(char_gender['n'])))
    
    fig, ax = plt.subplots()
    x  = np.arange(len(seasons))
    ax.bar(x - 0.2, male, 0.2, label='male', color='#0471CE')
    ax.bar(x + 0, female, 0.2, label='female', color='#E52222')
    ax.bar(x + 0.2, neutral, 0.2, label='neutral', color='#BBBBBB')
    ax.set_ylabel('Number of characters with dialogue')
    ax.set_xticks(x)
    ax.set_xticklabels(seasons)
    ax.legend()
    ax.set_title(f'Characters by gender, by season, for {series}')
    plt.savefig(f'{short}_characters_time.png', dpi=200)
    plt.show()


def lines_by_gender(dataframe):
    lines_by_gender = defaultdict(np.int64)
    for i in dataframe.index:
        lines_by_gender[dataframe['Gender'][i]] += dataframe['Linecount'][i]
        
    print(f"Total number of lines spoken by characters with > 10 lines: \
          \n{'Male characters:':{26}} {lines_by_gender['m']:>{5}} \
          \n{'Female characters:':{26}} {lines_by_gender['f']:>{5}} \
          \n{'Genderneutral characters:':{26}} {lines_by_gender['n']:>{5}} \
          \n---")
    
    series, short = get_labels(dataframe)
    
    # Plot number of lines by gender, overall
    plt.pie([lines_by_gender['m'], lines_by_gender['f'], lines_by_gender['n']],
            labels=['male', 'female', 'genderneutral'],
            shadow=False, startangle=90,
            colors=['#0471CE', '#E52222', '#BBBBBB'], autopct='%1.0f%%')
    plt.savefig(f'{short}_lines.png', dpi=150)

    # Plot number of lines by gender, per season
    seasons = list(dataframe['Season'].unique())
    lines_gender_seasons = np.empty(len(seasons), dtype=dict)
    male, female, neutral = [], [], []
    
    for seasonnumber, season in enumerate(seasons):
        # lines_gender = {'m': [], 'f': [], 'n': []}
        lines_gender = defaultdict(np.int64)
        for i in dataframe.index:
            if dataframe['Season'][i] == season:
                if dataframe['Gender'][i] == 'm':
                    lines_gender['m'] += dataframe['Linecount'][i]
                elif dataframe['Gender'][i] == 'f':
                    lines_gender['f'] += dataframe['Linecount'][i]
                elif dataframe['Gender'][i] == 'n':
                    lines_gender['n'] += dataframe['Linecount'][i]
        lines_gender_seasons[seasonnumber] = dict(lines_gender)
        male.append(lines_gender['m'])
        female.append(lines_gender['f'])
        neutral.append(lines_gender['n'])
    
    fig, ax = plt.subplots()
    x  = np.arange(len(seasons))
    ax.bar(x - 0.2, male, 0.2, label='male', color='#0471CE')
    ax.bar(x + 0, female, 0.2, label='female', color='#E52222')
    ax.bar(x + 0.2, neutral, 0.2, label='neutral', color='#BBBBBB')
    ax.set_ylabel('Lines spoken (normalized)')
    ax.set_xticks(x)
    ax.set_xticklabels(seasons)
    ax.legend()
    ax.set_title(f'Lines by gender, by season, for {series}')
    plt.savefig(f'{short}_lines_time.png', dpi=200)
    plt.show()


def characters_trend():
    # plot character-count, by gender, for each episode
    chars_m = np.ma.array(st_df['Char_male'])
    chars_m[80] = np.ma.masked  # break after TOS
    chars_m[102] = np.ma.masked  # break after TAS
    chars_m[707] = np.ma.masked  # break after ENT
    chars_f = np.ma.array(st_df['Char_female'])
    chars_f[80] = np.ma.masked
    chars_f[102] = np.ma.masked
    chars_f[707] = np.ma.masked
    
    # plot gender-ratio of characters, for each episode
    chars_m_rel = np.ma.array(st_df['Char_m_rel'])
    chars_m_rel[80] = np.ma.masked  # break after TOS
    chars_m_rel[102] = np.ma.masked  # break after TAS
    chars_m_rel[707] = np.ma.masked  # break after ENT
    chars_f_rel = np.ma.array(st_df['Char_f_rel'])
    chars_f_rel[80] = np.ma.masked
    chars_f_rel[102] = np.ma.masked
    chars_f_rel[707] = np.ma.masked
    
    fig, ax = plt.subplots()
    ax.plot(st_df['Airdate'], chars_m_rel, alpha=0.2, c='#0471CE')
    ax.plot(st_df['Airdate'], st_df['Char_m_rel'], 'h', markersize=1.6,
            label='male', c='#0471CE')
    ax.plot(st_df['Airdate'], chars_f_rel, alpha=0.2, c='#E52222')
    ax.plot(st_df['Airdate'], st_df['Char_f_rel'], 'h', markersize=1.6,
            label='female', c='#E52222')
    ax.legend(loc=1)
    ax.set_xlabel("Year of episode's original air date (US)")
    ax.set_ylabel('% of characters per episode')
    ax.set_title('Development of characters per gender (%) with time')
    ax.set_ylim([-0.12, max(st_df['Char_m_rel']) + 0.12])
    plt.annotate('TOS', xy=(1967, -0.09))
    plt.annotate('TAS', xy=(1973, -0.09))
    plt.annotate('TNG', xy=(1990, -0.09))
    plt.annotate('DS9', xy=(1994, -0.09))
    plt.annotate('VOY', xy=(1998, -0.09))
    plt.annotate('ENT', xy=(2003, -0.09))
    plt.annotate('DIS', xy=(2016, -0.09))
    plt.annotate('PIC', xy=(2020, -0.09))
    plt.savefig('st_character_ratio_episodes', dpi=200)
    plt.show()
    
 
def lines_trend():
    # plot line-count, by gender, for each episode
    lines_m = np.ma.array(st_df['Lines_male'])
    lines_m[80] = np.ma.masked  # break after TOS
    lines_m[102] = np.ma.masked  # break after TAS
    lines_m[707] = np.ma.masked  # break after ENT
    lines_f = np.ma.array(st_df['Lines_female'])
    lines_f[80] = np.ma.masked
    lines_f[102] = np.ma.masked
    lines_f[707] = np.ma.masked
    
    # plot gender-ratio of lines, for each episode
    lines_m_rel = np.ma.array(st_df['Lines_m_rel'])
    lines_m_rel[80] = np.ma.masked  # break after TOS
    lines_m_rel[102] = np.ma.masked  # break after TAS
    lines_m_rel[707] = np.ma.masked  # break after ENT
    lines_f_rel = np.ma.array(st_df['Lines_f_rel'])
    lines_f_rel[80] = np.ma.masked
    lines_f_rel[102] = np.ma.masked
    lines_f_rel[707] = np.ma.masked
    
    fig, ax = plt.subplots()
    ax.plot(st_df['Airdate'], lines_m_rel, alpha=0.2, c='#0471CE')
    ax.plot(st_df['Airdate'], st_df['Lines_m_rel'], 'h', markersize=1.6,
            label='male', c='#0471CE')
    ax.plot(st_df['Airdate'], lines_f_rel, alpha=0.2, c='#E52222')
    ax.plot(st_df['Airdate'], st_df['Lines_f_rel'], 'h', markersize=1.6,
            label='female', c='#E52222')
    
    # optional trendlines:
    # m1, b1 = np.polyfit(st_df['Airdate'], st_df['Lines_m_rel'], 1)
    # m2, b2 = np.polyfit(st_df['Airdate'], st_df['Lines_f_rel'], 1)
    # ax.plot(st_df['Airdate'], m1 * st_df['Airdate'] + b1, c='black',
    #         label='trend', linewidth=1, alpha=0.2, zorder=6)
    # ax.plot(st_df['Airdate'], m2 * st_df['Airdate'] + b2, c='black',
    #         linewidth=1, alpha=0.2, zorder=7)
    
    ax.legend(loc=1)
    ax.set_xlabel("Year of episode's original air date (US)")
    ax.set_ylabel('% of lines per episode')
    ax.set_title('Development of lines per gender (%) with time')
    ax.set_ylim([-0.12, max(st_df['Lines_m_rel']) + 0.12])
    plt.annotate('TOS', xy=(1967, -0.09))
    plt.annotate('TAS', xy=(1973, -0.09))
    plt.annotate('TNG', xy=(1990, -0.09))
    plt.annotate('DS9', xy=(1994, -0.09))
    plt.annotate('VOY', xy=(1998, -0.09))
    plt.annotate('ENT', xy=(2003, -0.09))
    plt.annotate('DIS', xy=(2016, -0.09))
    plt.annotate('PIC', xy=(2020, -0.09))
    plt.savefig('st_line_ratio_episodes', dpi=200)
    plt.show()


def lines_trend_glowing():

    M = np.array(st_df['Lines_m_rel'])
    F = np.array(st_df['Lines_f_rel'])
    M_smooth = gaussian_filter1d(M, sigma=3.5)
    F_smooth = gaussian_filter1d(F, sigma=3.5)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    for n in range(1, 10):
        ax.plot(st_df['Airdate'], M_smooth,
                linewidth=2 + n, alpha=0.03, color='#0477D9')
        ax.plot(st_df['Airdate'], F_smooth,
                linewidth=2 + n, alpha=0.03, color='#EB2323')
    
    ax.plot(st_df['Airdate'], M_smooth, c='#0471CE')
    ax.plot(st_df['Airdate'], F_smooth, c='#E52222')
    
    
    ax.set_title('LINES PER GENDER IN STAR TREK SERIES',
                 font='Federation', size=24, color='#FEB54C')
    #font from https://www.dafont.com/federation-classic.font
    ax.set_xlabel("episode's original air date (US)")
    ax.set_ylabel('')
    ax.set_ylim([-0.12, max(st_df['Lines_m_rel']) + 0.12])
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0 %', '20 %', '40 %', '60 %', '80 %', '100 %'])
    
    plt.annotate('male', xy=(1978, 0.89), color='#0471CE', size=14)
    plt.annotate('female', xy=(1977, 0.06), color='#E52222', size=14)
    plt.annotate('TOS', xy=(1967, -0.09), color='#FEB54C')
    plt.annotate('TAS', xy=(1973, -0.09), color='#FEB54C')
    plt.annotate('TNG', xy=(1990, -0.09), color='#FEB54C')
    plt.annotate('DS9', xy=(1994, -0.09), color='#FEB54C')
    plt.annotate('VOY', xy=(1998, -0.09), color='#FEB54C')
    plt.annotate('ENT', xy=(2003, -0.09), color='#FEB54C')
    plt.annotate('DIS', xy=(2016, -0.09), color='#FEB54C')
    plt.annotate('PIC', xy=(2020, -0.09), color='#FEB54C')
    
    # plot styling:
    plt.style.use('dark_background')
    
    for param in ['text.color', 'axes.labelcolor',
                  'xtick.color', 'ytick.color']:
        plt.rcParams[param] = '0.8'  # adjust text color
        
    for param in ['figure.facecolor', 'axes.facecolor']:
        plt.rcParams[param] = '#080A0D'  # adjust background color
    
    plt.rcParams['font.family'] = 'Verdana'  # adjust font
    
    plt.rcParams['font.size'] = 11  # adjust font size
    
    plt.savefig('st_line_ratio_episodes_glowing', dpi=200)
    plt.show()




def char_trend_glowing():
    
    M = np.array(st_df['Char_m_rel'])
    F = np.array(st_df['Char_f_rel'])
    M_smooth = gaussian_filter1d(M, sigma=3.5)
    F_smooth = gaussian_filter1d(F, sigma=3.5)
    
    fig, ax = plt.subplots()
    
    for n in range(1, 10):
        ax.plot(st_df['Airdate'], M_smooth,
                linewidth=2 + n, alpha=0.03, color='#0477D9')
        ax.plot(st_df['Airdate'], F_smooth,
                linewidth=2 + n, alpha=0.03, color='#EB2323')
    
    ax.plot(st_df['Airdate'], M_smooth, c='#0471CE')
    ax.plot(st_df['Airdate'], F_smooth, c='#E52222')
    
    
    ax.set_title('CHARACTERS PER GENDER IN STAR TREK SERIES',
                 font='Federation', size=20, color='#FEB54C')
    #font from https://www.dafont.com/federation-classic.font
    ax.set_xlabel("episode's original air date (US)")
    ax.set_ylabel('')
    ax.set_ylim([-0.12, max(st_df['Lines_m_rel']) + 0.12])
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0 %', '20 %', '40 %', '60 %', '80 %', '100 %'])
    
    plt.annotate('male', xy=(1978, 0.78), color='#0471CE', size=14)
    plt.annotate('female', xy=(1977, 0.17), color='#E52222', size=14)
    plt.annotate('TOS', xy=(1967, -0.09), color='#FEB54C')
    plt.annotate('TAS', xy=(1973, -0.09), color='#FEB54C')
    plt.annotate('TNG', xy=(1990, -0.09), color='#FEB54C')
    plt.annotate('DS9', xy=(1994, -0.09), color='#FEB54C')
    plt.annotate('VOY', xy=(1998, -0.09), color='#FEB54C')
    plt.annotate('ENT', xy=(2003, -0.09), color='#FEB54C')
    plt.annotate('DIS', xy=(2016, -0.09), color='#FEB54C')
    plt.annotate('PIC', xy=(2020, -0.09), color='#FEB54C')
    plt.savefig('st_char_ratio_episodes_glowing', dpi=200)

    # plot styling:
    plt.style.use('dark_background')
    
    for param in ['text.color', 'axes.labelcolor',
                  'xtick.color', 'ytick.color']:
        plt.rcParams[param] = '0.8'  # adjust text color
        
    for param in ['figure.facecolor', 'axes.facecolor']:
        plt.rcParams[param] = '#080A0D'  # adjust background color
    
    plt.rcParams['font.family'] = 'Verdana'  # adjust font
    
    plt.rcParams['font.size'] = 11  # adjust font size
    
    plt.savefig('st_line_ratio_episodes_glowing', dpi=200)
    plt.show()




def both_glowing():
    plt.style.use('dark_background')
    
    # adjust text color
    for param in ['text.color', 'axes.labelcolor',
                  'xtick.color', 'ytick.color']:
        plt.rcParams[param] = '0.8'
        
    # adjust background color
    for param in ['figure.facecolor', 'axes.facecolor']:
        plt.rcParams[param] = '#080A0D'
    
    # adjust font
    plt.rcParams['font.family'] = 'Verdana'
        
    MC = np.array(st_df['Char_m_rel'])
    FC = np.array(st_df['Char_f_rel'])
    ML = np.array(st_df['Lines_m_rel'])
    FL = np.array(st_df['Lines_f_rel'])
    MC_smooth = gaussian_filter1d(MC, sigma=4)
    FC_smooth = gaussian_filter1d(FC, sigma=4)
    ML_smooth = gaussian_filter1d(ML, sigma=4)
    FL_smooth = gaussian_filter1d(FL, sigma=4)
    
    fig, ax = plt.subplots()
    
    for n in range(1, 10):
        ax.plot(st_df['Airdate'], MC_smooth,
                linewidth=2 + n, alpha=0.03, color='#0477D9')
        ax.plot(st_df['Airdate'], FC_smooth,
                linewidth=2 + n, alpha=0.03, color='#EB2323')
    ax.plot(st_df['Airdate'], MC_smooth, '--', c='#0471CE')
    ax.plot(st_df['Airdate'], FC_smooth, '--', c='#E52222')
    
    for n in range(1, 10):
        ax.plot(st_df['Airdate'], ML_smooth,
                linewidth=2 + n, alpha=0.03, color='#0477D9')
        ax.plot(st_df['Airdate'], FL_smooth,
                linewidth=2 + n, alpha=0.03, color='#EB2323')
    ax.plot(st_df['Airdate'], ML_smooth, c='#0471CE')
    ax.plot(st_df['Airdate'], FL_smooth, c='#E52222')
    
    ax.set_title('GENDER DISTRIBUTION IN STAR TREK SERIES',
                 font='Federation', size=20, color='#FEB54C')
    #font from https://www.dafont.com/federation-classic.font
    ax.set_xlabel("episode's original air date (US)")
    ax.set_ylabel('')
    ax.set_ylim([-0.12, max(st_df['Lines_m_rel']) + 0.12])
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0 %', '20 %', '40 %', '60 %', '80 %', '100 %'])
    
    plt.annotate('male\ncharacters', xy=(1970, 0.58), color='#0471CE', size=14)
    plt.annotate('female\ncharacters', xy=(1970, 0.30), color='#E52222', size=14)
    plt.annotate('male lines', xy=(1977, 0.89), color='#0471CE', size=14)
    plt.annotate('female lines', xy=(1977, 0.06), color='#E52222', size=14)
    plt.annotate('TOS', xy=(1967, -0.09), color='#FEB54C')
    plt.annotate('TAS', xy=(1973, -0.09), color='#FEB54C')
    plt.annotate('TNG', xy=(1990, -0.09), color='#FEB54C')
    plt.annotate('DS9', xy=(1994, -0.09), color='#FEB54C')
    plt.annotate('VOY', xy=(1998, -0.09), color='#FEB54C')
    plt.annotate('ENT', xy=(2003, -0.09), color='#FEB54C')
    plt.annotate('DIS', xy=(2016, -0.09), color='#FEB54C')
    plt.annotate('PIC', xy=(2020, -0.09), color='#FEB54C')
    plt.savefig('st_both_glowing', dpi=200)
    plt.show()
    
    
characters_by_gender(ent_df)
lines_by_gender(ent_df)

characters_trend()
lines_trend()

lines_trend_glowing()
char_trend_glowing()
both_glowing()
    
pass
