import pandas as pd
import numpy as np

deaths = 'data/raw_data/covid_deaths_usafacts.csv'
confirmed = 'data/raw_data/covid_confirmed_usafacts.csv'
population = 'data/raw_data/covid_county_population_usafacts.csv'

df_dth = pd.read_csv(deaths)
df_cfm = pd.read_csv(confirmed)
df_pop = pd.read_csv(population)

df_covid = df_cfm.iloc[:, 0:3]
df_covid = df_covid.assign(Deaths=df_dth.iloc[:, -1],
                           Confirmed=df_cfm.iloc[:, -1],
                           Population=df_pop['population'],
                           DeathsPerThousand=df_dth.iloc[:, -1] / df_cfm.iloc[:, -1] * 1000,
                           CaseRate=df_cfm.iloc[:, -1]/df_pop['population']*100,
                           FatalityRate=df_dth.iloc[:, -1]/df_cfm.iloc[:, -1]*100
                           )

df_covid = df_covid[(df_covid.countyFIPS != 0) & (df_covid.countyFIPS != 1)]

df_covid['DeathsPerThousand'] = df_covid['DeathsPerThousand'].fillna(0.0).astype(int)
df_covid.rename(columns={'County Name': 'CountyName'}, inplace=True)
df_covid = df_covid.replace([np.inf, -np.inf], np.nan)

df_covid.to_csv('data/cleaned_data/covid_data.csv')
