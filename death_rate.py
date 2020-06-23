import pandas as pd

deaths = 'data/covid_deaths_usafacts.csv'
population = 'data/covid_county_population_usafacts.csv'

df_dth = pd.read_csv(deaths)
df_pop = pd.read_csv(population)

df_drate = df_pop.iloc[:, 0:3]
df_drate = df_drate.assign(Deaths=df_dth.iloc[:, -1],
                           Population=df_pop.iloc[:, -1],
                           DeathsPerMillion=df_dth.iloc[:, -1]/df_pop.iloc[:, -1]*1000000)

df_drate = df_drate[df_drate.countyFIPS != 0]
df_drate['DeathsPerMillion'] = df_drate['DeathsPerMillion'].fillna(0.0).astype(int)
df_drate.rename(columns={'County Name': 'CountyName'}, inplace=True)

df_drate.to_csv('data/covid_death_per_million_by_county.csv')
