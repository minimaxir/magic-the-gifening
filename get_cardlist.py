import json
import csv

file_path = "/Users/maxwoolf/Downloads/AllSets.json"
invalid_sets = ['MED', 'ME2', 'ME3', 'ME4']
MODERN_THRESH = '2003-07-28'
CURRENT_THRESH = '2014-07-28'


def encode_border(releaseDate):
    if releaseDate < MODERN_THRESH:
        return 'o'
    elif releaseDate < CURRENT_THRESH:
        return 'm'
    return 'c'


with open('cards.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'name', 'border'])
    with open(file_path, 'r') as data:
        all_sets = json.load(data)
        sets = all_sets.keys()

        for set in sets:
            border = encode_border(all_sets[set]['releaseDate'])
            cards = all_sets[set]['cards']
            for card in cards:
                if 'multiverseid' in card and set not in invalid_sets:
                    type = card.get('type')

                    if (type is not None and
                            type == "Instant" or
                            type == "Sorcery" and
                            card['layout'] == 'normal'):
                        writer.writerow(
                            [card['name'], card['multiverseid'], border])
