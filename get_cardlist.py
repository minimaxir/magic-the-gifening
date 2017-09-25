import json
import csv

file_path = "/Users/maxwoolf/Downloads/AllSets.json"

with open('cards.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'name'])
    with open(file_path, 'r') as data:
        all_sets = json.load(data)
        sets = all_sets.keys()

        for set in sets:
            cards = all_sets[set]['cards']
            for card in cards:
                if 'multiverseid' in card:
                    type = card.get('type')
                    if (type is not None and
                            type == "Instant" or
                            type == "Sorcery" and
                            card['layout'] == 'normal'):
                        writer.writerow([card['name'], card['multiverseid']])
