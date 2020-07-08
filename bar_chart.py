import pandas as pd
from viz import kbest_by_threshold

df = pd.read_csv('data/cleaned_data/sef_data.csv', index_col=0)
df.fillna(0, inplace=True)

X = df.loc[:, 'hhinc_mean2000':'X.2M']
y_cr = df['CaseRate'].apply(lambda x: round(x, 2))
y_fr = df['FatalityRate']

kbest_by_threshold(X, y_cr, 0.1, 'bar','viz/case_rate_corrcoef_bar', title='Case Rate')
kbest_by_threshold(X, y_fr, 0.1, 'bar', 'viz/fatality_rate_corrcoef_bar', title='Fatality Rate')


