import pandas as pd
import numpy as np

deaths = 'data/raw_data/covid_deaths_usafacts.csv'
population = 'data/raw_data/covid_confirmed_usafacts.csv'

df_dth = pd.read_csv(deaths)
df_pop = pd.read_csv(population)

df_drate = df_pop.iloc[:, 0:3]
df_drate = df_drate.assign(Deaths=df_dth.iloc[:, -1],
                           Population=df_pop.iloc[:, -1],
                           DeathsPerThousand=df_dth.iloc[:, -1]/df_pop.iloc[:, -1]*1000)

df_drate = df_drate[(df_drate.countyFIPS != 0) & (df_drate.countyFIPS != 1)]
df_drate = df_drate.replace([np.inf, -np.inf], np.nan)

df_drate['DeathsPerThousand'] = df_drate['DeathsPerThousand'].fillna(0.0).astype(int)
df_drate.rename(columns={'County Name': 'CountyName'}, inplace=True)

df_drate.to_csv('data/cleaned_data/covid_death_per_thousand_by_county.csv')
