import requests
import time
from secrets import *
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from io import BytesIO
from PIL import Image
import numpy as np

GIPHY_API_URL = "https://api.giphy.com/v1/gifs/random?api_key={}&tag={}"
GATHERER_URL = "http://gatherer.wizards.com/Handlers/Image.ashx" \
    "?multiverseid={}&type=card"


def get_giphy_gif(name, GIPHY_API_KEY=GIPHY_API_KEY, max_attempts=10):
    attempts = 0
    while attempts < max_attempts:
        r = requests.get(GIPHY_API_URL.format(GIPHY_API_KEY, name))
        gif = r.json()['data']
        ratio = int(gif['image_width']) / int(gif['image_height'])
        # return gif['image_mp4_url']
        # print(ratio)
        if 1.3 < ratio < 1.6:
            with open('giphy_gif.mp4', 'wb') as file:
                file.write(requests.get(gif['image_mp4_url']).content)
                return
        attempts += 1
        # time.sleep(1)


def get_mtg_image(id):
    return GATHERER_URL.format(id)


def create_mtg_gif(name, id):
    card_upper_corner = (17, 35)
    gif_width = 205 - card_upper_corner[0]
    gif_height = 173 - card_upper_corner[1]

    mtg_card = Image.open(BytesIO(requests.get(get_mtg_image(id)).content))
    mtg_card = ImageClip(np.asarray(mtg_card)).resize((222, 310))

    get_giphy_gif(name)
    giphy_gif = (VideoFileClip('giphy_gif.mp4',
                               target_resolution=(gif_height, gif_width))
                 .set_pos(card_upper_corner)

                 )

    mtg_gif = CompositeVideoClip([mtg_card, giphy_gif])
    mtg_gif = mtg_gif.set_start(0).set_duration(giphy_gif.duration)
    # mtg_gif.write_gif("mtg_gif.gif")
    mtg_gif.write_videofile("mtg_gif.mp4", codec='libx264', bitrate="50000000",
                            audio=False, ffmpeg_params=['-pix_fmt', 'yuv420p'])
