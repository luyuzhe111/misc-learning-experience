import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file = 'data/cleaned_data/cleaned_full_dataset.csv'

df = pd.read_csv(file)

plt.figure(figsize=(20, 10))

X = df['CountyName']
Y = df['DeathsPerThousand']

plt.bar(X, Y, width=1)
plt.xticks(rotation=90)

plt.show(aspect='auto')
