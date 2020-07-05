import pandas as pd
from viz import corr_matrix, corrcoef_bar

df = pd.read_csv('data/raw_data/Risk_score_raw.csv')

X = df[list(df.loc[:, 'X5..male':'X.2M'])+['populationdensity']+['population']]
y = df['Risk score']

num_features = 50
out_dir = 'viz/rscore_corrcoef_mat' + str(num_features)
corr_matrix(X, y, num_features, out_dir)

out_dir = 'viz/rscore_corrcoef_bar' + str(num_features)
corrcoef_bar(X, y, num_features, out_dir)


