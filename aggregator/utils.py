#!/usr/bin/env python
from __future__ import division
import pika
import json
from textblob import TextBlob
from fuzzywuzzy import fuzz
# import language_check
import enchant
import re

class Q():
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='tweets')

    def send(self,body):
        data=json.dumps(body)
        self.channel.basic_publish(exchange='',
                              routing_key='tweets',
                              body=data)
        
    def close(self):
        self.connection.close()
        # print 'conn closed'


def get_sentiment(tweet_body):
    tweet = TextBlob(tweet_body)
    if tweet.sentiment.polarity < 0:
        sentiment = "negative"
    elif tweet.sentiment.polarity == 0:
        sentiment = "neutral"
    else:
        sentiment = "positive"

    return sentiment,tweet.sentiment.polarity,tweet.sentiment.subjectivity

# tool = language_check.LanguageTool('en-US')
# def get_accuracy(tweet_body):
#     detect(tweet_body)
#     corrected=language_check.correct(text.decode('utf-8'))
#     accuracy=fuzz.ratio(tweet_body,corrected)
#     return accuracy


d=enchant.Dict("en_US")
def check_english(text):
    text=' '.join([word for word in text.split() if not word.startswith('@')])
    text = re.sub(r"(?:\@|https?\://)\S+", "", text)
    if (sum([1 for char in text if ord(char)<=128])/len(text))*100 > 70:
        words=[text.split()[0]]+[w for w in text.split()[1:] if (w.islower() or w=='I')and w.isalpha()]
        eng_prob=(sum([1 for word in words if d.check(word)])/len(words))*100 
        # print text,eng_prob
        return eng_prob > 50
    else:
        return False

