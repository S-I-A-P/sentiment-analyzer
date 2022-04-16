import pandas as pd
import seaborn as sb
import const
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('../tweets_with_sentiment_2.csv')
print(df.describe().to_string())

sb.countplot(x='economic_policy', data=df)
plt.show()
sb.countplot(x='social_policy', data=df)
plt.show()
sb.countplot(x='sentiment_label', data=df)
plt.show()
sb.countplot(x='language', data=df)
plt.show()
sb.set(font_scale=0.8)
sb.pairplot(df, hue="sentiment_label", diag_kind="hist", aspect=2)
for t in const.topics:
    filtered_by_topic = df[df["topic"]==t]
    sb.displot(filtered_by_topic, x='economic_policy', hue='sentiment_label', height=5, aspect=1, multiple="dodge", kde=True)

    plt.title(t)
    plt.show()