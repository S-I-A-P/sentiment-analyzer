import pandas as pd
import seaborn as sb
import const
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('../tweets_with_sentiment_2.csv')
print(df.describe().to_string())


def plot(x, path):
    ax = sb.countplot(x=x, data=df)
    for p in ax.patches:
        ax.annotate('{:.1f}'.format(p.get_height()), (p.get_x() + 0.25, p.get_height() + 0.01))
    plt.savefig(path)
    plt.show()


plot('economic_policy', '../saved_plots/economic_policy_count')
plot('social_policy', '../saved_plots/social_policy_count')
plot('sentiment_label', '../saved_plots/sentiment_count')
plot('language', '../saved_plots/language_count')

sb.set(font_scale=0.8)
# sb.pairplot(df, hue="sentiment_label", diag_kind="hist", aspect=2)
for t in const.topics:
    filtered_by_topic = df[df["topic"] == t]
    sb.displot(filtered_by_topic, x='social_policy', hue='sentiment_label', height=5, aspect=1, multiple="dodge",
               kde=True)
    plt.title(t)
    plt.savefig('../saved_plots/social_policy_' + t)
    plt.show()
    sb.displot(filtered_by_topic, x='economic_policy', hue='sentiment_label', height=5, aspect=1, multiple="dodge",
               kde=True)
    plt.title(t)
    plt.savefig('../saved_plots/economic_policy_' + t)
    plt.show()
