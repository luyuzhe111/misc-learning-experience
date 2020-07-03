import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, f_regression
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt

dataset = pd.read_csv('data/cleaned_data/cleaned_full_dataset.csv', index_col=0)
dataset.dropna(inplace=True)
X = dataset.iloc[:, 6:]
y = dataset.iloc[:, 5]

X_sub = SelectKBest(f_regression, k=20).fit(X, y)
mask = X_sub.get_support()

feat_chosen = []
for chosen, feature in zip(mask, X.columns):
    if chosen:
        feat_chosen.append(feature)

out_list = []
for feature in feat_chosen:
    corr_tuple = pearsonr(X[feature], y)
    out_list.append([feature, corr_tuple[0], corr_tuple[1]])

corr_df = pd.DataFrame(out_list, columns=['Features', 'Correlation', 'P-value'])

fig, ax = plt.subplots()
ax.bar(corr_df['Features'], corr_df['Correlation'], width=0.1)
ax.axhline(linewidth=1, color='r')
plt.xticks(corr_df['Features'], rotation=90)
plt.tight_layout()
plt.title('20 Best Features')
# fig.autofmt_xdate()
plt.savefig('viz/correlation', dpi=800)
plt.show()
