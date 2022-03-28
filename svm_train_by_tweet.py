from statistics import median

import numpy
import pandas as pd
from pandas import Index, DataFrame
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

topics = ('kosovo', 'albanija', 'vojska', 'crkva', 'lgbt', 'beograd', 'policija',
          'korupcija', 'evropa', 'ukrajina', 'putin', 'rusija', 'nato', 'amerika')
sentiment_dict = {'negative': -1, 'positive': 1, 'neutral': 0.5}


def get_data(data_set):
    dt = numpy.zeros((len(data_set), len(topics)), dtype=int)
    iterator = 0
    for row in data_set[
        Index(['username', 'sentiment_label', 'topic', 'economic_policy', 'social_policy', 'economic_policy_rounded',
               'social_policy_rounded'])].values:
        dt[iterator][[topics.index(row[2])]] = sentiment_dict[row[1]]
        iterator = iterator + 1
    return dt


def print_data(predictions, actual_data):
    errors = []
    for index, prediction in enumerate(predictions):
        actual = actual_data.values.item(index)
        error = abs(prediction - actual)
        errors.append(error)
        print('result: %.2f, actual: %.2f, error: %.2f' % (prediction, actual, error))
    avg_error = sum(errors) / len(errors)
    print('Avg error %.2f' % avg_error)
    print('Median error: % .2f' % median(errors))
    print('---------------------------------------------------------------------')


df = pd.read_csv('tweets_with_sentiment.csv')
train, test = train_test_split(df, test_size=0.2, random_state=35)

data = get_data(train)

support_vector_machine_social = svm.SVR(verbose=True)
support_vector_machine_economy = svm.SVR(verbose=True)

parameters = {'kernel': ('linear', 'rbf'), 'C': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
clf_social = GridSearchCV(support_vector_machine_social, parameters)
clf_social.fit(data, train['social_policy'])
clf_economy = GridSearchCV(support_vector_machine_social, parameters)
clf_economy.fit(data, train['economic_policy'])

test_data = get_data(test)

social_predictions = clf_social.predict(test_data)
economic_predictions = clf_economy.predict(test_data)

print_data(social_predictions, test['social_policy'])
print_data(economic_predictions, test['economic_policy'])
print(clf_social.best_params_)
print(clf_economy.best_params_)

#print(DataFrame(clf_social.cv_results_).to_string())
#print(DataFrame(clf_economy.cv_results_).to_string())
