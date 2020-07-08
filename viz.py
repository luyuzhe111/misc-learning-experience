import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.feature_selection import SelectKBest, f_regression
from scipy.stats.stats import pearsonr
import plotly.express as px


def corr_matrix(X, y, num_fts, out_dir):
    feat_chosen = select_features(X, y, k=num_fts)
    selected = X[feat_chosen]

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
    plt.savefig(out_dir, dpi=800)
    plt.show()
    plt.clf()


def pearson_r(X, y, num_fts, out_dir):
    feat_chosen = select_features(X, y, k=num_fts)
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
    plt.title(str(num_fts) + ' Best Features')
    plt.savefig(out_dir, dpi=800)
    plt.show()
    plt.clf()


def kbest_by_threshold_bar(X, y, threshold, out_dir, title='None'):
    feat_chosen = select_features(X, y, k='all')
    out_list = []
    for feature in feat_chosen:
        corr_tuple = np.corrcoef(X[feature], y)
        if abs(corr_tuple[0][1]) > abs(threshold):
            out_list.append([feature, round(corr_tuple[0][1], 2)])

    corr_df = pd.DataFrame(out_list, columns=['Features', 'Correlation'])

    fig = px.bar(corr_df, x='Features', y='Correlation',
                 hover_data=['Features', 'Correlation'],
                 labels={'Features': 'Socioeconomic Factors'})
    fig.update_layout(
        title={
            'text': title,
             'x': 0.5,
        }
    )

    fig.show()

    # ax = plt.gca()
    # ax.axhline(linewidth=2, color='lightblue')
    # # xticks = (range(len(corr_df['Features'])))
    # # new_xticks = [i*2 for i in xticks]
    # # plt.bar(new_xticks, corr_df['Correlation'], align='center', width=0.6)
    # # plt.xticks(new_xticks, corr_df['Features'], rotation=90)
    # plt.bar(corr_df['Features'], corr_df['Correlation'], align='center', width=0.6, color='lightsteelblue')
    # plt.xticks(rotation=90)
    # plt.yticks(np.arange(round(min(corr_df['Correlation']), 1)-0.1,
    #                      round(max(corr_df['Correlation']), 1) + 0.1, 0.05))
    # plt.tight_layout()
    # plt.title('Best Features')
    # plt.savefig(out_dir, dpi=800, bbox_inches='tight')
    # plt.show()
    # plt.clf()


def corrcoef_bar(X, y, num_fts, out_dir):
    feat_chosen = select_features(X, y, k=num_fts)
    out_list = []
    for feature in feat_chosen:
        corr_tuple = np.corrcoef(X[feature], y)
        out_list.append([feature, corr_tuple[0][1]])

    corr_df = pd.DataFrame(out_list, columns=['Features', 'Correlation'])

    plt.bar(corr_df['Features'], corr_df['Correlation'], width=0.1)
    ax = plt.gca()
    ax.axhline(linewidth=1, color='r')
    plt.xticks(rotation=90)
    # plt.yticks(np.arange(-0.25, 0.25, 0.05))
    plt.tight_layout()
    plt.title(str(num_fts) + ' Best Features')
    plt.savefig(out_dir, dpi=800)
    plt.show()
    plt.clf()


def select_features(X, y, k='all'):
    X_sub = SelectKBest(f_regression, k=k).fit(X, y)
    mask = X_sub.get_support()

    feat_chosen = []
    for chosen, feature in zip(mask, X.columns):
        if chosen:
            feat_chosen.append(feature)
    return feat_chosen
