import pandas as pd

sef = 'data/raw_data/socioecon.csv'
com = 'data/raw_data/community.csv'
covid = 'data/cleaned_data/covid_data.csv'
rscore = 'data/raw_data/Risk_score_raw.csv'

df_sef = pd.read_csv(sef, encoding='latin-1')
df_com = pd.read_csv(com)
df_covid = pd.read_csv(covid, index_col=0)
df_rscore = pd.read_csv(rscore, index_col=0)

# clean community char data
df_com = df_com[df_com['state'] != 72]
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
                   'tax_st_diff_top20', 'pop_d_2000_1980', 'lf_d_2000_1980', 'tuition', 'gradrate_r']
df_sef.drop(columns=columns_to_drop, inplace=True)

# merge community char data to covid data
df_all = df_covid.merge(df_com, how='left', left_on='countyFIPS', right_on='countyFIPS')
df_all = df_all.merge(df_sef, how='left', left_on='countyFIPS', right_on='cty').drop(columns=['cty', 'county_name'])


# merge risk score data
df_all = df_all.merge(df_rscore, how='left', left_on='countyFIPS', right_on='countyfips')

df_all.drop(columns=['county.fips', 'value', 'region', 'stateFIPS', 'populationdensity',
                     'job_density_2013', 'State_y', 'population', 'countyfips',
                     'Statename', 'state.fips', 'share_white2010', 'share_black2010',
                     'share_hisp2010', 'poor_share2010', 'foreign_share2010', 'cs_frac_black'], inplace=True)
df_all = df_all[list(df_all.loc[:, 'countyFIPS':'FatalityRate']) + ['Risk score'] +
                list(df_all.loc[:, 'hhinc_mean2000':'X.2M'])]

df_all.to_csv('data/cleaned_data/sef_data.csv', index=0)
