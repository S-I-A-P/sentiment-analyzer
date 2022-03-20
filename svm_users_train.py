from sklearn import svm

from util import approximate, calculate_avg
from const import topics
from svm_users_extract_data import extract_data

train_data_percentage = 0.8

train_data_x = []
train_data_economic_y = []
train_data_social_y = []
train_data_economic_rounded_y = []
train_data_social_rounded_y = []

test_data_x = []
test_data_economic_y = []
test_data_social_y = []
test_data_economic_rounded_y = []
test_data_social_rounded_y = []
test_users = []

# get structured data from tweets_with_sentiment.csv
handle_topic_map, handle_socioeconomic_data_map = extract_data()

train_data_limit = len(handle_socioeconomic_data_map) * train_data_percentage
print('Total data: %d' % len(handle_socioeconomic_data_map))
print('Train data limit: %d ' % train_data_limit)

# form vectors: a vector contains user's sentiment on topics (14 dimensions)
for index, handle in enumerate(handle_topic_map):
    topic_tweet_data_map = handle_topic_map[handle]
    socioeconomic_data = handle_socioeconomic_data_map[handle]
    topic_vector = []
    # get user's total sentiment on each topic (0 if no data on topic was found)
    for topic in topics:
        tweet_data = topic_tweet_data_map.get(topic)
        value = 0
        if tweet_data is not None:
            value = tweet_data.calculate_value()
        topic_vector.append(value)

    # form svm train and test vectors
    if index <= train_data_limit:
        train_data_x.append(topic_vector)
        train_data_economic_y.append(socioeconomic_data.economic_policy)
        train_data_social_y.append(socioeconomic_data.social_policy)
        train_data_economic_rounded_y.append(socioeconomic_data.economic_policy_rounded)
        train_data_social_rounded_y.append(socioeconomic_data.social_policy_rounded)
    else:
        test_users.append(handle)
        test_data_x.append(topic_vector)
        test_data_economic_y.append(socioeconomic_data.economic_policy)
        test_data_social_y.append(socioeconomic_data.social_policy)
        test_data_economic_rounded_y.append(socioeconomic_data.economic_policy_rounded)
        test_data_social_rounded_y.append(socioeconomic_data.social_policy_rounded)

# train SVMs
support_vector_machine_economy = svm.SVR(verbose=False)
support_vector_machine_social = svm.SVR(verbose=False)
support_vector_machine_economy_rounded = svm.SVR(verbose=False)
support_vector_machine_social_rounded = svm.SVR(verbose=False)

support_vector_machine_economy.fit(train_data_x, train_data_economic_y)
support_vector_machine_social.fit(train_data_x, train_data_social_y)
support_vector_machine_economy_rounded.fit(train_data_x, train_data_economic_rounded_y)
support_vector_machine_social_rounded.fit(train_data_x, train_data_social_rounded_y)

# test SVMs
results_economic = support_vector_machine_economy.predict(test_data_x)
results_social = support_vector_machine_social.predict(test_data_x)
results_economic_rounded = support_vector_machine_economy_rounded.predict(test_data_x)
results_social_rounded = support_vector_machine_social_rounded.predict(test_data_x)

# round values to -1, -0.5, 0, 0.5, 1
results_economic_rounded_rounded = approximate(results_economic_rounded)
results_social_rounded_rounded = approximate(results_social_rounded)

# print results
list_error_economic = []
list_error_social = []
list_error_economic_rounded = []
list_error_economic_rounded_rounded = []
list_error_social_rounded = []
list_error_social_rounded_rounded = []

# calculate error for each test result
for i in range(len(test_data_x)):
    print(test_users[i])

    error_economic = abs(results_economic[i] - test_data_economic_y[i])
    print('\teconomic result: %.2f, actual: %.2f, error: %.2f' % (
        results_economic[i], test_data_economic_y[i], error_economic))

    error_social = abs(results_social[i] - test_data_social_y[i])
    print('\tsocial result: %.2f, actual: %.2f, error: %.2f' % (results_social[i], test_data_social_y[i], error_social))

    error_economic_rounded = abs(results_economic_rounded[i] - test_data_economic_rounded_y[i])
    print('\teconomic rounded result: %.2f, actual: %.2f, error: %.2f' % (
        results_economic_rounded[i], test_data_economic_rounded_y[i], error_economic_rounded))
    error_economic_rounded_rounded = abs(results_economic_rounded_rounded[i] - test_data_economic_rounded_y[i])
    print('\teconomic rounded rounded result: %.2f, actual: %.2f, error: %.2f' % (
        results_economic_rounded_rounded[i], test_data_economic_rounded_y[i], error_economic_rounded_rounded))

    error_social_rounded = abs(results_social_rounded[i] - test_data_social_rounded_y[i])
    print('\tsocial rounded result: %.2f, actual: %.2f, error: %.2f' % (
        results_social_rounded[i], test_data_social_rounded_y[i], error_social_rounded))
    error_social_rounded_rounded = abs(results_social_rounded_rounded[i] - test_data_social_rounded_y[i])
    print('\tsocial rounded rounded result: %.2f, actual: %.2f, error: %.2f' % (
        results_social_rounded_rounded[i], test_data_social_rounded_y[i], error_social_rounded_rounded))

    # lists are needed for average error calculation
    list_error_economic.append(error_economic)
    list_error_social.append(error_social)
    list_error_economic_rounded.append(error_economic_rounded)
    list_error_economic_rounded_rounded.append(error_economic_rounded_rounded)
    list_error_social_rounded.append(error_social_rounded)
    list_error_social_rounded_rounded.append(error_social_rounded_rounded)

# calculate average error for results
error_economic_avg = calculate_avg(list_error_economic)
print('Average economic error %.2f' % error_economic_avg)
error_social_avg = calculate_avg(list_error_social)
print('Average social error %.2f' % error_social_avg)
error_economic_rounded_avg = calculate_avg(list_error_economic_rounded)
print('Average economic rounded error %.2f' % error_economic_rounded_avg)
error_economic_rounded_rounded_avg = calculate_avg(list_error_economic_rounded_rounded)
print('Average economic rounded rounded error %.2f' % error_economic_rounded_rounded_avg)
error_social_rounded_avg = calculate_avg(list_error_social_rounded)
print('Average social rounded error %.2f' % error_social_rounded_avg)
error_social_rounded_rounded_avg = calculate_avg(list_error_social_rounded_rounded)
print('Average social rounded rounded error %.2f' % error_social_rounded_rounded_avg)
