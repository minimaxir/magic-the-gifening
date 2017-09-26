from utils import *
from twython import Twython
import random
import csv

with open('cards.csv', 'r') as f:
    cards = list(csv.reader(f))

card = random.choice(cards)

create_mtg_gif(card[0], card[1], card[2])

# twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET,
#                   ACCESS_KEY, ACCESS_SECRET)

# video = open('mtg_gif.mp4', 'rb')
# response = twitter.upload_video(media=video, media_type='video/mp4')
# twitter.update_status(status='', media_ids=[response['media_id']])
