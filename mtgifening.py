#!/usr/bin/python3

from utils import *
from twython import Twython
import random
import csv
from datetime import datetime

with open('cards.csv', 'r') as f:
    cards = list(csv.reader(f))


while True:
    try:
        card = random.choice(cards)
        create_mtg_gif(card[0], card[1], card[2])

        twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET,
                          ACCESS_KEY, ACCESS_SECRET)

        video = open('mtg_gif.mp4', 'rb')
        response = twitter.upload_video(media=video, media_type='video/mp4')
        twitter.update_status(status='', media_ids=[response['media_id']])
        print("Posted {} at {}!".format(card[0], str(datetime.now())))
        quit()

    except Exception as e:
        print(e)
