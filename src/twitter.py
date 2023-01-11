import os
from dotenv import load_dotenv
import tweepy as tw
from urllib.request import urlopen
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
 
class Twitter:
    
    def __init__(self):
       consumer_key,consumer_secret,\
       access_token,access_token_secret = _init_env_variables()
       self.api = _api_constructor(consumer_key,consumer_secret,access_token,access_token_secret)
    
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
            tweets_in_trend = self.api.search_tweets(q=trend[1],lang='es',locale='es',result_type='mixed',count=50)
            for tweet in tweets_in_trend:
                tweets_by_trend.append((tweet.id,tweet.user.screen_name))
            self.comments_trending_topic[trend[0]] = tweets_by_trend
                
    def collect_birthday(self):
        url = 'https://twitter.com/bizarrap'
        browser = webdriver.Chrome(ChromeDriverManager().install())
        browser.get(url)
        html = browser.page_source
        time.sleep(2)
        browser.find_element(By.XPATH, '//button[text()="Some text"]')
        print(html)
        browser.quit()  
                    
        
        
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
        