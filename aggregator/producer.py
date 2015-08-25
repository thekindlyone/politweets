from twython import TwythonStreamer
from twitter_creds import *
import httplib
from utils import *
import sys
from logwriter import *
import time

logger=logWriter('producer')

class MyStreamer(TwythonStreamer):
    def __init__(self,APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET,sqs):
        self.sqs=sqs
        TwythonStreamer.__init__(self,APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    def on_success(self, data):
        if not data.has_key("text") or not data.get("user") or not data["user"].get("screen_name"):
            return
        try:
            tags = [tag.get('text') for tag in data['entities'].get('hashtags')]
            urls = [url.get('expanded_url') for url in data['entities'].get('urls')]

            payload={
                'username':data['user']['name'],
                'handle':data['user']['screen_name'],
                'timestamp':data['created_at'],
                'retweet':data['retweeted'],
                'text':data['text'],
                'tags':tags,
                'urls':urls
            }
            if check_english(payload['text']):
                report=self.sqs.send(payload)
                logger.write(u'{} - {}...\n'.format(data['user']['screen_name'],data["text"][:30]).encode('utf-8'))
            else:
                logger.write('Skipped because Hindi',payload['text'])
            return

        except Exception as e:
            logger.write(sys.exc_info(),e)
            return

    def on_error(self, status_code, data):
        logger.write(data,status_code)
        pass
    def on_disconnect(self, data):
        time.sleep(100)
        connectAndStream(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def connectAndStream(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET):
    logger.write('Connecting')
    sqs= Q()
    stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET,sqs)
    tags = ["BJP","Narendra Modi","Modi","PM Modi","Modiji",'Aam Aadmi Party','Arvind Kejriwal','Rahul Gandhi','Mulayam Singh Yadav','Akhilesh Yadav']
    follows=["@ArvindKejriwal","@narendramodi","@BJP4India","@INCIndia","@OfficeOfRG","@AamAadmiParty","@BSP4India","@yadavakhilesh",'@laluprasadrjd','@NitishKumar']
    while True:
        try:
            stream.statuses.filter(track=tags)
            break
        except httplib.IncompleteRead as e:
            logger.write('incomplete read handled')
            time.sleep(10)
            continue

# def getTags():
#     #tag_list = ["FreeBree", "satchat","a", "python", "pycon", "django", "flask", "python3", "Python", "ipython"]
#     tag_list = 
#     # tag_list = ['#'+tag for tag in tag_list]
#     print 'tag filter',tag_list
#     return tag_list



def main():
    connectAndStream(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

main()