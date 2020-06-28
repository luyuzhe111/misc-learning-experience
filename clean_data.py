import pandas as pd

sef = 'data/cleaned_data/full_dataset.csv'

df = pd.read_csv(sef, index_col=0)

columns_to_drop = ['ln_wage_growth_hs_grad', 'cur_smoke_q1', 'cur_smoke_q2', 'cur_smoke_q3', 'cur_smoke_q4',
                   'bmi_obese_q1', 'bmi_obese_q2', 'bmi_obese_q3', 'bmi_obese_q4', 'exercise_any_q1',
                   'exercise_any_q2', 'exercise_any_q3', 'exercise_any_q4', 'tuition', 'gradrate_r']

df.drop(columns=columns_to_drop, inplace=True)

df.to_csv('data/cleaned_data/cleaned_full_dataset.csv')
