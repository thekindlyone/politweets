import pika
from elasticsearch import Elasticsearch
from sentiment import *
import json
from logwriter import *
es = Elasticsearch()
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='tweets')

logger=logWriter('consumer')
logger.write(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, tweet):
    tweet=json.loads(tweet)
    sentiment,polarity,subjectivity=get_sentiment(tweet['text'])
    if sentiment !='neutral':
        payload={  "author": tweet['username'],
                   "handle": tweet['handle'],
                   "date": tweet["timestamp"],
                   "message": tweet["text"],
                   "polarity": polarity,
                   "subjectivity": subjectivity,
                   "sentiment": sentiment}

        es.index(index="sentiment",
             doc_type="tweet",
             body=payload)

        logger.write(payload)
        logger.write('*'*20,'\n\n\n')




channel.basic_consume(callback,
                      queue='tweets',
                      no_ack=True)

channel.start_consuming()