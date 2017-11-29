import asyncio
import concurrent.futures
import json
from collections import Counter
from urllib.parse import urlencode
from urllib.request import urlopen

champions = Counter()


def get_count_of_matches(player_id):
    base = 'https://acs.leagueoflegends.com/v1/stats/player_history/EUN1/{}?'.format(player_id)
    params = urlencode({
        'begIndex': 99999
    })
    response = urlopen(base + params).read()
    data = json.loads(response, encoding='utf8')
    return data['games']['gameIndexBegin']


def get_match_history(player_id, begin_index=0):
    base = 'https://acs.leagueoflegends.com/v1/stats/player_history/EUN1/{}?'.format(player_id)
    params = urlencode({
        'begIndex': begin_index
    })
    response = urlopen(base + params).read()
    return json.loads(response, encoding='utf8')


def process_response(response):
    for game in response['games']['games']:
        champions.update([game['participants'][0]['championId']])


PLAYER_ID = 30317666


def count_champions(page):
    print(page)
    response = get_match_history(PLAYER_ID, page)
    process_response(response)


async def count_all_champions():
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
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

    print(champions.most_common(10))
