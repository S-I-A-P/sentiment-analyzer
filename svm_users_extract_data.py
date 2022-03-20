import csv

from svm_users.user_socioeconomic_data import UserSocioeconomicData
from svm_users.user_tweet_data import UserTweetData


def extract_data():
    #  key: twitter handle, value: Map of UserTweetData with key: topic
    handle_topic_map = {}
    #  key: twitter handle, value: UserSocioeconomicData
    handle_socioeconomic_data_map = {}

    with open('tweets_with_sentiment.csv', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # extract all needed data from the row
            handle = row['handle']
            topic = row['topic']
            sentiment = row['sentiment_label']
            economic_policy = float(row['economic_policy'])
            social_policy = float(row['social_policy'])
            economic_policy_rounded = float(row['economic_policy_rounded'])
            social_policy_rounded = float(row['social_policy_rounded'])

            # create topic_tweet map in handle_topic map if handle does not exist
            topic_tweet_data_map = handle_topic_map.get(handle)
            if topic_tweet_data_map is None:
                topic_tweet_data_map = {}
                handle_topic_map[handle] = topic_tweet_data_map

            # create tweet_data in topic_tweet_data map if topic does not exist
            tweet_data = topic_tweet_data_map.get(topic)
            if tweet_data is None:
                tweet_data = UserTweetData()
                topic_tweet_data_map[topic] = tweet_data

            # update tweet data
            if sentiment == 'positive':
                tweet_data.positive += 1
            elif sentiment == 'negative':
                tweet_data.negative += 1
            else:
                tweet_data.neutral += 1
            tweet_data.total += 1

            # create socioeconomic data if handle in handle_socioeconomic_data map does not exist
            socioeconomic_data = handle_socioeconomic_data_map.get(handle)
            if socioeconomic_data is None:
                socioeconomic_data = UserSocioeconomicData(economic_policy, social_policy, economic_policy_rounded,
                                                           social_policy_rounded)
                handle_socioeconomic_data_map[handle] = socioeconomic_data

        # print tweet_data results to check
        # for handle in handle_topic_map:
        #     print(handle)
        #     topic_tweet_data_map = handle_topic_map[handle]
        #     for topic in topic_tweet_data_map:
        #         print('\t' + topic)
        #         tweet_data = topic_tweet_data_map[topic]
        #         print('\t' + str(tweet_data))

        # print socioeconomic_data results to check
        # for handle in handle_socioeconomic_data_map:
        #     print(handle)
        #     socioeconomic_data = handle_socioeconomic_data_map[handle]
        #     print('\t' + str(socioeconomic_data))

        return handle_topic_map, handle_socioeconomic_data_map


extract_data()
