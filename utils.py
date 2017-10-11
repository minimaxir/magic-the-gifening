import requests
import time
from secrets import *
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from moviepy.video.fx.all import loop
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
        if 1.3 < ratio < 1.6:
            with open('giphy_gif.mp4', 'wb') as file:
                file.write(requests.get(gif['image_mp4_url']).content)
                return
        attempts += 1
    raise Exception('Failed to find a GIF for {}'.format(name))


def get_mtg_image(id):
    return GATHERER_URL.format(id)


def create_mtg_gif(name, id, border):
    if border == 'm':   # Modern (post-8th Ed)
        card_upper_corner = (19, 38)
        gif_width = 202 - card_upper_corner[0]
        gif_height = 172 - card_upper_corner[1]
    elif border == 'c':   # Current (post-Magic 2015)
        card_upper_corner = (17, 34)
        gif_width = 204 - card_upper_corner[0]
        gif_height = 173 - card_upper_corner[1]
    else:   # Old (pre-8th Ed)
        card_upper_corner = (25, 30)
        gif_width = 196 - card_upper_corner[0]
        gif_height = 168 - card_upper_corner[1]

    mtg_card = Image.open(BytesIO(requests.get(get_mtg_image(id)).content))
    mtg_card = ImageClip(np.asarray(mtg_card)).resize((222, 310))

    get_giphy_gif(name)
    giphy_gif = (VideoFileClip('giphy_gif.mp4',
                               target_resolution=(gif_height, gif_width))
                 .set_pos(card_upper_corner)

                 )

    if giphy_gif.duration < 2:
        giphy_gif = giphy_gif.fx(loop, n=1+int(2 // giphy_gif.duration))

    mtg_gif = CompositeVideoClip([mtg_card, giphy_gif])
    mtg_gif = mtg_gif.set_start(0).set_duration(giphy_gif.duration)
    # mtg_gif.write_gif("mtg_gif.gif")
    mtg_gif.write_videofile("mtg_gif.mp4", codec='libx264',
                            bitrate=str(np.power(10, 7)), verbose=False,
                            progress_bar=False,
                            audio=False, ffmpeg_params=['-pix_fmt', 'yuv420p'])
