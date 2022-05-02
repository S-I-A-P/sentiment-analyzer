from audioop import avg
from pickle import FALSE
from statistics import mean, median, median_high
from matplotlib.pyplot import plot
import numpy
from requests import head
from sklearn import svm, random
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import csv
import random
import pandas
from xgboost import XGBRegressor, XGBRFRegressor
from map_function import plotCompass

TRAIN_SET_PERCENTAGE = 0.7
RADIUS_AROUND_REAL_POSITION = 0.4
MAX_TWEETS_PER_TOPIC = 30
MIN_LIMIT = -1
MAX_LIMIT = 1
x_train = []
y_train_economy = []
y_train_social = []
x_test = []
x_users = []
y_users = []
y_users_topic_dict = dict()
topic_labels = {}
train_set_for_plot = []
sentiment_labels = {}
result_comparison_dict = {}
tweet_topic_counter_dict = {}
tweet_topic_counter_positive_dict = {}
tweet_topic_counter_negative_dict = {}
tweet_topic_counter_neutral_dict = {}
# Igrati se sa faktorima ovde : kernel='rbf', degree=3, gamma='scale', coef0=0.0, tol=0.001, C=1.0, epsilon=0.01, shrinking=True, cache_size=500, verbose=True, max_iter=- 1 # {'linear', 'poly', 'rbf', 'sigmoid', 'precomputed'}
support_vector_machine_economy = svm.SVR(verbose=True)
support_vector_machine_social = svm.SVR(verbose=True)

# df = pandas.read_csv('tweets_with_sentiment_2.csv', header=1, names=["handle","username","timestamp","content","topic","language","economic_policy","social_policy","economic_policy_rounded","social_policy_rounded","sentiment_label","sentiment_score"])
# ds = df.sample(frac=1)
# # print(ds.to_csv())

# with open('tweets_with_sentiment_2.csv', newline='', encoding='utf-8') as r, open('tweets_with_sentiment_2_shuffled.csv', 'w', newline='', encoding='utf-8') as w:
#     # reader = csv.reader(r)
#     # header = next(r)
#     # writer = csv.writer(w)
#     # w.write(header)
#     # print(header)
#     w.write(ds.to_csv(index=False))


with open('tweets_with_sentiment_2_shuffled.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    total_rows = 0
    total_rows = sum(1 for _ in reader)  
    print(total_rows)
    total_test_data = int(total_rows * TRAIN_SET_PERCENTAGE)
    print(total_test_data)
    index = 0
    # Topic Part
    csvfile.seek(0)
    for row in reader:
        # print(row)
        break
    # Ideja iza 'itl' i 'isp' brojacaa je u tome da SVM ne prihvata stringove, pa ih klasifikujem kao brojeve - nemam predstavu koliko je zaista ovo pametno
    itl = 0
    x_train_headers = []
    for row in reader:
        if row['topic'] not in topic_labels:
            topic_labels[row['topic']] = itl
            x_train_headers.append(row['topic'])
            itl+=1
        else:
            continue
    # print(x_train_headers)
    # x_train_headers.append("Sentiment")
    # Sentiment Part
    csvfile.seek(0)
    for row in reader:
        break
    isp = 0
    for row in reader:
        if row['sentiment_label'] not in sentiment_labels:
            sentiment_labels[row['sentiment_label']] = isp
            isp+=1
        else:
            continue
    # Train setting
    csvfile.seek(0)
    for row in reader:
        break
    for row in reader:
        # print(index)
        # print(row)
        if index < total_test_data:
            # Ogranicenje da jedan korisnik moze imati po MAX_TWEETS_PER_TOPIC tvita po odredjenoj temi
            if (row['username'], row['topic']) not in y_users_topic_dict:
                y_users_topic_dict[(row['username'], row['topic'])] = 1
            else:
                if y_users_topic_dict[(row['username'], row['topic'])] < MAX_TWEETS_PER_TOPIC:
                    y_users_topic_dict[(row['username'], row['topic'])] += 1
                else:
                    index+=1
                    continue
            if row['topic'] not in tweet_topic_counter_dict:
                tweet_topic_counter_dict[row['topic']] = 1
                if row['sentiment_label'] == 'positive':
                    tweet_topic_counter_positive_dict[row['topic']] = 1
                    tweet_topic_counter_negative_dict[row['topic']] = 0
                    tweet_topic_counter_neutral_dict[row['topic']] = 0
                elif row['sentiment_label'] == 'negative':
                    tweet_topic_counter_positive_dict[row['topic']] = 0
                    tweet_topic_counter_negative_dict[row['topic']] = 1
                    tweet_topic_counter_neutral_dict[row['topic']] = 0
                else:
                    tweet_topic_counter_positive_dict[row['topic']] = 0
                    tweet_topic_counter_negative_dict[row['topic']] = 0
                    tweet_topic_counter_neutral_dict[row['topic']] = 1
            else:
                tweet_topic_counter_dict[row['topic']] += 1
                if row['sentiment_label'] == 'positive':
                    tweet_topic_counter_positive_dict[row['topic']] += 1
                elif row['sentiment_label'] == 'negative':
                    tweet_topic_counter_negative_dict[row['topic']] += 1
                else:
                    tweet_topic_counter_neutral_dict[row['topic']] += 1
            x_users.append(row['username'])
            x_element = []
            for i in x_train_headers:
                if i == row['topic']:
                    x_element.append(1)
                else:
                    x_element.append(0)
            
            if row['sentiment_label'] == 'negative':
                x_element.append(-1)
            elif row['sentiment_label'] == 'neutral':
                x_element.append(0)
            else:
                x_element.append(1)
            # print(x_element)
            x_train.append(x_element)
            x = float(row['economic_policy'])
            y = float(row['social_policy'])
            y_train_economy.append(x)
            y_train_social.append(y)
        else:
            if row['username'] not in result_comparison_dict:
                result_comparison_dict[row['username']] = (float(row['economic_policy']), float(row['social_policy']))
            x_element_test = []
            for i in x_train_headers:
                if i == row['topic']:
                    x_element_test.append(1)
                else:
                    x_element_test.append(0)
            
            if row['sentiment_label'] == 'negative':
                x_element_test.append(-1)
            elif row['sentiment_label'] == 'neutral':
                x_element_test.append(0)
            else:
                x_element_test.append(1)
            x_test.append(x_element_test)
            y_users.append(row['username'])
            train_set_for_plot.append({'username': row['username'], 'economic_policy': row['economic_policy'], 'social_policy': row['social_policy']})
        index+=1

# print(result_comparison_dict.keys())
# print(len(x_train))
# print(x_train)
# print(len(y_train_economy))
# print(y_train_economy)
# print(len(y_train_social))c
# print(y_train_social)
# print(len(x_test))
# print(x_test)
for key in tweet_topic_counter_dict.keys():
    print(f"{key}: {tweet_topic_counter_dict[key]} \t => \t (  positive: {tweet_topic_counter_positive_dict[key]},\tneutral= {tweet_topic_counter_neutral_dict[key]},\tnegative= {tweet_topic_counter_negative_dict[key]}  )")
print("Total Used: ", len(x_train))
print("Total Unused due to MAX_TWEET_PARAMETER: ", total_test_data - len(x_train))

# Ideja obucavanje jeste ( x_train -> niz tvitova iz kojih je izvucena tema i sentiment tvita i to predstavlja ulaz (tema,sen); izlaz jeste kordinata po pojedinacnoj osovini, zato imamo dve SVM)
parameters = {'kernel': ('linear', 'rbf'), 'C': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
clf_social = GridSearchCV(support_vector_machine_social, parameters)
clf_social.fit(x_train, y_train_social)
clf_economic = GridSearchCV(support_vector_machine_social, parameters)
clf_economic.fit(x_train, y_train_economy)

# support_vector_machine_economy.fit(x_train, y_train_economy)
# support_vector_machine_social.fit(x_train, y_train_social)
# print('Successfully trained 2 SVMs')
y_test_economy = clf_economic.predict(x_test) # (support_vector_machine_economy.predict(x_test) - 0.5) * 2
y_test_social = clf_social.predict(x_test) # (support_vector_machine_social.predict(x_test) - 0.5) * 2

data = []

# Ideja ovoga jeste da se rezultati povezu sa korisnicima koji ih je objavio
for i in range(len(y_test_social)):
    row = dict()
    row['username'] = y_users[i]
    row['economic_policy'] = y_test_economy[i]
    row['social_policy'] = y_test_social[i]
    data.append(row)

distinctDict = dict()

# Ideja ovoga jeste da se korisnik za jednog korisnika vezu sve lokacije tvitova
for row in data:
    if row['username'] not in distinctDict:
        distinctDict[row['username']] = [(numpy.clip(row['economic_policy'], MIN_LIMIT, MAX_LIMIT), numpy.clip(row['social_policy'], MIN_LIMIT, MAX_LIMIT))]
    else:
        distinctDict[row['username']].append((numpy.clip(row['economic_policy'], MIN_LIMIT, MAX_LIMIT), numpy.clip(row['social_policy'], MIN_LIMIT, MAX_LIMIT)))

finalData = []
finalData_dict = {}
# Ideja ovoga jeste  da se iz svih polozaja tvitova odredi neka sredina: avg, mediana
for key in distinctDict.keys():
    if not distinctDict[key]:
        continue

    row = dict()
    row['username'] = key
    arr_x = []
    arr_y = []
    for coords in distinctDict[key]: 
        if coords == ():
            continue  
        arr_x.append(coords[0])
        arr_y.append(coords[1])

    final_x = median(arr_x)
    final_y = median(arr_y)

    final_t = (round(final_x,2),round(final_y,2)) 

    row['economic_policy'] = final_t[0]
    row['social_policy'] = final_t[1]

    finalData.append(row)
    finalData_dict[row['username']] = final_t

# Check results 
correct_users = []
print('------------------------------------------------------')
print('Result Comparison:')
results = []
for i, user in enumerate(finalData):
    r = {
        'username': user['username'], 
        'real_x': result_comparison_dict[user['username']][0], 
        'real_y': result_comparison_dict[user['username']][1], 
        'result_x': user['economic_policy'], 
        'result_y': user['social_policy'], 
        'hit':False
        }
    # print('#########################')
    # print(f'{i+1}) Username: ', user['username'])
    # print('Real position: ', result_comparison_dict[user['username']])
    xx = user['economic_policy']
    yy = user['social_policy']
    user_result_pos = (xx,yy) 
    rel_xx_min = numpy.clip(result_comparison_dict[user['username']][0] - RADIUS_AROUND_REAL_POSITION, MIN_LIMIT, MAX_LIMIT)
    rel_yy_min = numpy.clip(result_comparison_dict[user['username']][1] - RADIUS_AROUND_REAL_POSITION, MIN_LIMIT, MAX_LIMIT)
    rel_xx_max = numpy.clip(result_comparison_dict[user['username']][0] + RADIUS_AROUND_REAL_POSITION, MIN_LIMIT, MAX_LIMIT)
    rel_yy_max = numpy.clip(result_comparison_dict[user['username']][1] + RADIUS_AROUND_REAL_POSITION, MIN_LIMIT, MAX_LIMIT)
    min_lim = (rel_xx_min,rel_yy_min)
    max_lim = (rel_xx_max,rel_yy_max)
    # print(f'Rel allow pos: ({rel_xx_min:.2f},{rel_yy_min:.2f}) ({rel_xx_max:.2f},{rel_yy_max:.2f})')
    # print(f'Test position: {user_result_pos}')
    not_lower_than_min = user_result_pos[0] >= min_lim[0] and user_result_pos[1] >= min_lim[1]
    not_greater_than_max = user_result_pos[0] <= max_lim[0] and user_result_pos[1] <= max_lim[1]
    # print(f'Is it good: ({not_lower_than_min},{not_greater_than_max})')
    if user['username'] in result_comparison_dict:
        if not_lower_than_min and not_greater_than_max:
            correct_users.append(user['username'])
            r['hit'] = True
            # print('HIT!!!')
    results.append(r)

# Zapisivanje
with open('results2.csv', 'w', encoding='utf8', newline='') as f:
    header = results[0].keys()
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(results)

print('------------------------------------------------------')
print('Total number of test users: ', len(result_comparison_dict))
print('Total number of hits: ', len(correct_users))
print('Percantage of hits: ', len(correct_users)/len(result_comparison_dict) * 100)
print('Hit users:\n', correct_users)

with open('usernames_on_compass2.csv', 'w', encoding='utf8', newline='') as f:
    header = finalData[0].keys()
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(finalData)

with open('train_set2.csv', 'w', encoding='utf8', newline='') as f:
    header = train_set_for_plot[0].keys()
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(train_set_for_plot)

#
# plotCompass('train_set.csv')
# plotCompass('usernames_on_compass.csv')