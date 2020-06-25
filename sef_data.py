import pandas as pd
import numpy as np


sef = 'data/raw_data/socioecon.csv'
com = 'data/raw_data/community.csv'

drate = 'data/cleaned_data/covid_death_per_thousand_by_county.csv'

df_sef = pd.read_csv(sef, encoding='latin-1')
df_com = pd.read_csv(com)
df_drate = pd.read_csv(drate, index_col=0)

# clean community char data
df_com = df_com[df_com['state']!=72]
df_com.drop(df_com.tail(1).index, inplace=True)

df_com[['state', 'county']] = df_com[['state', 'county']].astype(str)
df_com['county'] = df_com['county'].str.zfill(3)

df_com['countyFIPS'] = df_com['state'] + df_com['county']
df_com['countyFIPS'] = pd.to_numeric(df_com['countyFIPS'], downcast='integer')

columns_to_drop = ['state', 'county', 'cz', 'czname',
                   'popdensity2010', 'popdensity2000',
                   'poor_share1990', 'poor_share2000',
                   'frac_coll_plus2000', 'med_hhinc1990',
                   'poor_share1990', 'poor_share2000',
                   'share_black2000', 'share_white2000',
                   'share_hisp2000', 'share_asian2000',
                   'singleparent_share1990', 'singleparent_share2000']
df_com.drop(columns=columns_to_drop, inplace=True)

# clean socioeconomic data
columns_to_drop = ['cty_pop2000', 'cz', 'cz_name', 'cz_pop2000',
                   'statename', 'state_id', 'stateabbrv', 'csa',
                   'csa_name', 'cbsa', 'cbsa_name', 'intersects_msa',
                   'tax_st_diff_top20', 'pop_density']
df_sef.drop(columns=columns_to_drop, inplace=True)

# merge community char data to death rate data
df_all = df_drate.merge(df_com, how='left', left_on='countyFIPS', right_on='countyFIPS')
df_all = df_all.merge(df_sef, how='left', left_on='countyFIPS', right_on='cty').drop(columns=['cty', 'county_name'])


df_all.to_csv('data/cleaned_data/full_dataset.csv')