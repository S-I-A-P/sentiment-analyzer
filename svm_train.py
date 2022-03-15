from matplotlib.pyplot import plot
import numpy
from sklearn import svm
import csv
from map_function import plotCompass

TRAIN_SET_PERCENTAGE = 0.8
x_train = []
y_train_economy = []
y_train_social = []
x_test = []
y_users = []
topic_labels = {}
sentiment_labels = {}
support_vector_machine_economy = svm.SVR()
support_vector_machine_social = svm.SVR()
with open('tweets_with_sentiment.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    total_rows = 0
    total_rows = sum(1 for _ in reader)  
    total_test_data = int(total_rows * TRAIN_SET_PERCENTAGE)
    index = 0
    # Topic Part
    csvfile.seek(0)
    for row in reader:
        print(row)
        break
    itl = 0
    for row in reader:
        if row['topic'] not in topic_labels:
            topic_labels[row['topic']] = itl
            itl+=1
        else:
            continue
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
            x_train.append([topic_labels[row['topic']], sentiment_labels[row['sentiment_label']]])
            x = float(row['economic_policy'])
            y = float(row['social_policy'])
            y_train_economy.append(x)
            y_train_social.append(y)
        else:
            x_test.append([topic_labels[row['topic']], sentiment_labels[row['sentiment_label']]])
            y_users.append(row['username'])
        index+=1

print(len(x_train))
# print(x_train)
print(len(y_train_economy))
# print(y_train_economy)
print(len(y_train_social))
# print(y_train_social)
print(len(x_test))
# print(x_test)
support_vector_machine_economy.fit(x_train, y_train_economy)
support_vector_machine_social.fit(x_train, y_train_social)
print('Successfully trained 2 SVMs')
y_test_economy = support_vector_machine_economy.predict(x_test)
y_test_social = support_vector_machine_social.predict(x_test)

data = []

for i in range(len(y_test_social)):
    row = dict()
    row['username'] = y_users[i]
    row['economic_policy'] = y_test_economy[i]
    row['social_policy'] = y_test_social[i]
    data.append(row)

distinctDict = dict()

for row in data:
    if row['username'] not in distinctDict:
        distinctDict[row['username']] = []
    else:
        distinctDict[row['username']].append((row['economic_policy'], row['social_policy']))
# print(data)

finalData = []
# print(len(distinctDict.keys()))
# print(distinctDict.values())
for key in distinctDict.keys():
    row = dict()
    row['username'] = key
    
    t = tuple(map(lambda y: sum(y) / float(len(y)), zip(*distinctDict[key])))
    # print(t)
    if t == ():
        continue
    row['economic_policy'] = t[0]
    row['social_policy'] = t[1]
    # row['economic_policy'] = numpy.mean(distinctDict[key][0])
    finalData.append(row)

with open('usernames_on_compass.csv', 'w', encoding='utf8', newline='') as f:
    header = finalData[0].keys()
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(finalData)

plotCompass()
plotCompass('usernames_on_compass.csv')