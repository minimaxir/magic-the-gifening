import requests
import time
from secrets import *

GIPHY_API_URL = "https://api.giphy.com/v1/gifs/random?api_key={}&tag={}"
GATHERER_URL = "http://gatherer.wizards.com/Handlers/Image.ashx" \
                    "?multiverseid={}&type=card"


def get_gif(name, GIPHY_API_KEY=GIPHY_API_KEY, max_attempts=10):
    attempts = 0
    while attempts < max_attempts:
        r = requests.get(GIPHY_API_URL.format(GIPHY_API_KEY, name))
        gif = r.json()['data']
        ratio = int(gif['image_width']) / int(gif['image_height'])
        # return gif['image_mp4_url']
        # print(ratio)
        if 1.2 < ratio < 1.6:
            return gif['image_mp4_url']
        attempts += 1
        time.sleep(1)


def get_mtg_image(id):
    return GATHERER_URL.format(id)
