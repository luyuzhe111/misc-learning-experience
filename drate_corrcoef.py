import pandas as pd
from viz import corr_matrix

data = pd.read_csv('data/cleaned_data/sef_data.csv', index_col=0)
data.dropna(inplace=True)
X = data.loc[:, 'hhinc_mean2000':'X.2M']
y = data['FatalityRate']

num_features = 50
out_dir = 'viz/drate_corrcoef_mat_' + str(num_features)
corr_matrix(X, y, num_features, out_dir)

out_dir = 'viz/drate_corrcoef_bar_' + str(num_features)
corr_matrix(X, y, num_features, out_dir)


