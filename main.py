from src.twitter import Twitter
from src.gpt import GPT
from src.utils import Utils

if __name__ == '__main__':
    context = {}
    context['files'] = Utils.Files()
    tw = Twitter(context)
    tw.launch_collection_horoscope()
    tw.write_file()
    for horoscopo in tw.horoscopo_tweets_text.keys():
        GPT.get_GPT_text(horoscopo,tw.horoscopo_tweets_text[horoscopo])
