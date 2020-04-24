import requests
from googletrans import Translator
import random

translator = Translator()

# Random API calls for now

def get_corona_stats(country):
    url = 'https://api.covid19api.com/total/country/' + country
    r = requests.get(url=url)

    data = r.json()

    cases = data[len(data)-1]

    confirmed = cases['Confirmed']
    recovered = cases['Recovered']
    deaths = cases['Deaths']

    return confirmed, recovered, deaths

def get_random_cat():
    url = 'https://api.thecatapi.com/v1/images/search'
    r = requests.get(url=url)

    cat_img =  r.json()[0]['url']
    return cat_img

def translate(text):
    return translator.translate(text, dest='en').text

def get_meme():
    url = 'https://api.imgflip.com/get_memes'
    r = requests.get(url=url)

    img_id = random.randint(0, len(r.json()['data']['memes']))
    return r.json()['data']['memes'][img_id]['url']

print(get_meme())
