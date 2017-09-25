from utils import *
from twython import Twython
from random import randint
import csv

with open('cards.csv', 'r') as f:
    cards = list(csv.reader(f))

card = cards[randint(0, len(cards)-1)]

create_mtg_gif(card[0], card[1])

twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET,
                  ACCESS_KEY, ACCESS_SECRET)

video = open('mtg_gif.mp4', 'rb')
response = twitter.upload_video(media=video, media_type='video/mp4')
twitter.update_status(status='', media_ids=[response['media_id']])
