import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.feature_selection import SelectKBest, f_regression

data = pd.read_csv('data/cleaned_data/cleaned_full_dataset.csv', index_col=0)
data.dropna(inplace=True)
X = data.iloc[:, 6:]
y = data.iloc[:, 5]

X_sub = SelectKBest(f_regression, k=20).fit(X, y)
mask = X_sub.get_support()

feat_chosen = []
for chosen, feature in zip(mask, X.columns):
    if chosen:
        feat_chosen.append(feature)

selected = data[feat_chosen]

corr = selected.corr()
mask = np.zeros_like(corr)
mask[np.triu_indices_from(mask)] = True
ax = sns.heatmap(
    corr,
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    mask=mask,
    square=True
)
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=90,
    horizontalalignment='right'
)

plt.xlabel('', fontsize=5)
plt.ylabel('', fontsize=5)

plt.tight_layout()
plt.savefig('viz/x_corrcoef_20', dpi=800)

