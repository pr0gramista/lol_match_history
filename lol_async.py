import asyncio
import concurrent.futures
import csv
import json
import time
from collections import Counter
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

import champion

champions = Counter()


def get_count_of_matches(player_id):
    base = 'https://acs.leagueoflegends.com/v1/stats/player_history/EUN1/{}?'.format(player_id)
    params = urlencode({
        'begIndex': 99999
    })
    try:
        response = urlopen(base + params).read()
        data = json.loads(response, encoding='utf8')
        return data['games']['gameIndexBegin']
    except HTTPError as e:
        if e.code == 429:
            time.sleep(0.1)
            return get_count_of_matches(player_id)



def get_match_history(player_id, begin_index=0):
    base = 'https://acs.leagueoflegends.com/v1/stats/player_history/EUN1/{}?'.format(player_id)
    params = urlencode({
        'begIndex': begin_index
    })
    try:
        response = urlopen(base + params).read()
        return json.loads(response, encoding='utf8')
    except HTTPError as e:
        if e.code == 429:
            time.sleep(0.1)
            return get_match_history(player_id, begin_index=begin_index)


def process_response(response):
    for game in response['games']['games']:
        champions.update([game['participants'][0]['championId']])


PLAYER_ID = 30317666


def count_champions(page):
    print(page)
    response = get_match_history(PLAYER_ID, page)
    process_response(response)


async def count_all_champions():
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(executor, count_champions, page)
            for page in range(0, count_of_matches, 10)
        ]
        await asyncio.wait(futures)


if __name__ == '__main__':
    count_of_matches = get_count_of_matches(PLAYER_ID)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(count_all_champions())

    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        for champ in champions.most_common():
            print("{}: {}".format(champion.get_champion_name_for_id(champ[0]), champ[1]))
            writer.writerow([champ[0], champ[1], champion.get_champion_name_for_id(champ[0])])
