import os
from dotenv import load_dotenv
import tweepy as tw
from urllib.request import urlopen
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from .utils import Utils
 

 
class Twitter:
    

    def __init__(self,context):
       
       self.context = context
       consumer_key,consumer_secret,\
       access_token,access_token_secret = _init_env_variables()
       self.api = _api_constructor(consumer_key,consumer_secret,access_token,access_token_secret)
       
    def launch_collection_horoscope(self):
        print('Get trending topics')
        self.get_trending_topics()
        print('Get message relevants')
        self.get_message_relevant()
        print('Get horoscopo')
        self.collect_birthday()
        print(self.horoscopo_tweets) 
        print('Get collect tweets text')
        self.collect_tweets_horocopo()
        print(self.horoscopo_tweets_text)  
    
    def get_trending_topics(self):
        woeids = [23424950,753692,766273,776688,774508,754542]
        self.trends = []
        for woeid in woeids:
            trends = self.api.get_place_trends(woeid)
            for trend in trends[0]['trends']:
                tuple_trend = (trend['name'],trend['query'])
                if trend['tweet_volume'] is not None and tuple_trend not in self.trends:
                    self.trends.append(tuple_trend)
                    
    def get_message_relevant(self):
        self.comments_trending_topic = {}
        for trend in self.trends:
            tweets_by_trend = []
            tweets_in_trend = self.api.search_tweets(q=trend[1],lang='es',locale='es',result_type='mixed',count=500)
            for tweet in tweets_in_trend:
                tweets_by_trend.append((tweet.id,tweet.user.screen_name))
            self.comments_trending_topic[trend[0]] = tweets_by_trend
                
    def collect_birthday(self):
        browser = webdriver.Chrome(ChromeDriverManager().install())
        self.horoscopo_tweets = {}
        for trend in self.comments_trending_topic.keys():
            for tweet in self.comments_trending_topic[trend]:
                url = 'https://twitter.com/{0}'.format(tweet[1])
                browser.get(url)
                time.sleep(15)
                try:
                    fecha_nacimiento = browser.find_element(By.XPATH, '//*[contains(text(),"Fecha de nacimiento:")]').text
                    horoscopo = Utils.get_horoscopo(fecha_nacimiento)
                    tweets_ids = []
                    if horoscopo in self.horoscopo_tweets:
                        tweets_ids = self.horoscopo_tweets[horoscopo]
                    tweets_ids.append(tweet[0])
                    self.horoscopo_tweets[horoscopo] = tweets_ids
                except:
                    continue
        browser.quit()  
        
    def collect_tweets_horocopo(self):
        file_identificator = self.context['files'].new_fichero('tweets.txt','a')
        self.horoscopo_tweets_text = {}
        for horoscopo in self.horoscopo_tweets.keys():
            texts_tweets = []
            for tweet_id in self.horoscopo_tweets[horoscopo]:
                tweet_text = self.api.get_status(tweet_id, tweet_mode='extended')._json['full_text']
                texts_tweets.append(tweet_text)
                print("{0}-{1}".format(horoscopo,tweet_text))
                self.context['files'].action(file_identificator,"{0}-{1}\n".format(horoscopo,tweet_text.rstrip()))
            self.horoscopo_tweets_text[horoscopo] = texts_tweets
        self.context['files'].close(file_identificator)       
        
    def write_file(self):
        file_identificator = self.context['files'].new_fichero('prueba.txt','w')
        print(file_identificator)
        self.context['files'].action(file_identificator,"HOLA")
        self.context['files'].close(file_identificator)  
        
def _api_constructor(consumer_key, consumer_secret,access_token,access_token_secret):
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tw.API(auth, wait_on_rate_limit=True)


def _init_env_variables():
    load_dotenv()
    return os.getenv('consumer_key'), \
            os.getenv('consumer_secret'), \
            os.getenv('access_token'), \
            os.getenv('access_token_secret')
        