import os
from dotenv import load_dotenv
import openai
import wandb

class GPT():
    
    @staticmethod
    def get_GPT_text(horoscopo,list_tweets):
        load_dotenv()
        openai.api_key = os.getenv('api_key_gt')
        gpt_prompt = "Analizando los comentarios mas relevante de twitter se ha clasificado cada uno de ellos con su horoscopo. ",\
                    "Siendo para el horoscopo {0} estos tweets: ".format(horoscopo)

        for i,text in enumerate(list_tweets):
            gpt_prompt+= '{0}."{1}" \n'.format(i,text)

        gpt_prompt += "Con la información de estos tweets.Necesito un conocer el horoscopo del día de hoy, y escribirlo en un tweet. \nEl tweet es:"



        response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=gpt_prompt,
        temperature=0.5,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )


        text = response['choices'][0]['text']
        print(text)
        