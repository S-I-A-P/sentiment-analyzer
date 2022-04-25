from sklearn.ensemble import RandomForestClassifier
import numpy
import pandas as pd
from pandas import Index
from sklearn.model_selection import train_test_split
import seaborn as sm
from sklearn.metrics import confusion_matrix
from sklearn import tree
import matplotlib.pyplot as plt

topics = ('kosovo', 'albanija', 'vojska', 'crkva', 'lgbt', 'beograd', 'policija',
          'korupcija', 'evropa', 'ukrajina', 'putin', 'rusija', 'nato', 'amerika')
sentiment_dict = {'negative': -1, 'positive': 1, 'neutral': 0.5}
NUMBER_OF_ESTIMATORS = 10

def get_data(data_set):
    dt = numpy.zeros((len(data_set), len(topics)), dtype=int)
    iterator = 0
    for row in data_set[
        Index(['username', 'sentiment_label', 'topic', 'economic_policy', 'social_policy', 'economic_policy_rounded',
               'social_policy_rounded'])].values:
        dt[iterator][[topics.index(row[2])]] = sentiment_dict[row[1]]
        iterator = iterator + 1
    return dt


df = pd.read_csv('tweets_with_sentiment.csv')
train, test = train_test_split(df, test_size=0.2, random_state=35)

model = RandomForestClassifier(n_estimators=NUMBER_OF_ESTIMATORS)
train['social_policy_rounded'] = train['social_policy_rounded'] * 10
test['social_policy_rounded'] = test['social_policy_rounded'] * 10
test_data = get_data(test)
data = get_data(train)
model.fit(data, train['social_policy_rounded'])
print(model.score(test_data, test['social_policy_rounded']))
predicted = model.predict(test_data)
cm = confusion_matrix(test['social_policy_rounded'], predicted)
sm.heatmap(cm, annot=True)
plt.xlabel("predicted")
plt.ylabel("truth")
plt.show()

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(15, 15), dpi=500)
for index in range(0, NUMBER_OF_ESTIMATORS):
    tree.plot_tree(model.estimators_[0],
                   feature_names=topics,
                   class_names=['-1', '-0.5', '0', '0.5', '1'],
                   filled=True);
    fig.savefig('estimator_individual_trees/rf_individualtree' + str(index) + '.png')
