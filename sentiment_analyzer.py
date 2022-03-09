import csv

from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from srbai.Alati.Transliterator import transliterate_cir2lat

tokenizer = AutoTokenizer.from_pretrained("EMBEDDIA/bertic-tweetsentiment")
model = AutoModelForSequenceClassification.from_pretrained("EMBEDDIA/bertic-tweetsentiment")
pipeSr = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
pipeEn = pipeline("sentiment-analysis")

tweets = []
with open('tweet_data.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['language'] == 'en':
            sentiment = pipeEn(row['content'])[0]
        else:
            sentiment = pipeSr(transliterate_cir2lat(row['content']))[0]
        row['sentiment_label'] = sentiment['label'].lower()
        row['sentiment_score'] = sentiment['score']
        tweets.append(row)

with open('tweets_with_sentiment.csv', 'w', encoding='utf8', newline='') as f:
    header = tweets[0].keys()
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(tweets)
