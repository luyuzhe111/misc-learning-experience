import pandas as pd

demo = 'data/raw_data/demo.csv'
cases = 'data/raw_data/covid_confirmed_usafacts.csv'
RATE = 1000

df_demo = pd.read_csv(demo, low_memory=False)
df_cases = pd.read_csv(cases)

df_demo = df_demo[df_demo['STNAME']=='New Jersey']
df_demo.rename(columns={'Unnamed: 4': 'CTNAME'}, inplace=True)

df_cases = df_cases[df_cases['State'] == 'NJ']
df_cases.rename(columns={'6/20/20': 'CUM_CASES'}, inplace=True)
df_cases['County Name'] = df_cases['County Name'].apply(lambda x: x.split(' ')[0] if len(x.split(' ')) == 2 else
                                                        x.split(' ')[0] + ' ' + x.split(' ')[1])

demo_tar_columns = ['STNAME', 'CTNAME', 'TOT_POP', 'H_MALE', 'H_FEMALE']
cases_tar_columns = ['County Name', 'CUM_CASES']

df_demo = df_demo[demo_tar_columns]
df_cases = df_cases[cases_tar_columns]

df_hisp = df_demo.merge(df_cases, how='left', left_on='CTNAME', right_on='County Name')
df_hisp['CASE_RATE'] = df_hisp['CUM_CASES']/df_hisp['TOT_POP']*RATE
df_hisp.drop(columns=['County Name'], inplace=True)

df_hisp['CASE_RATE'] = df_hisp['CASE_RATE'].round(2)
int_columns = ['TOT_POP', 'H_MALE', 'H_FEMALE']
df_hisp[int_columns] = df_hisp[int_columns].astype(int)

df_hisp.to_csv('data/cleaned_data/hisp_data.csv')


