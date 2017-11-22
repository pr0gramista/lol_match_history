import json
from collections import Counter
from urllib.parse import urlencode
from urllib.request import urlopen

champions = Counter()

def get_match_history(player_id, begin_index=0):
    base = 'https://acs.leagueoflegends.com/v1/stats/player_history/EUW1/{}?'.format(player_id)
    params = urlencode({
            'begIndex': begin_index
    })
    response = urlopen(base + params).read()
    return json.loads(response, encoding='utf8')


def process_response(response):
    for game in response['games']['games']:
        champions.update([game['participants'][0]['championId']])

PLAYER_ID = 30317666

if __name__ == '__main__':
    response = get_match_history(PLAYER_ID)
    process_response(response)
    begin_index = 0
    next_page = response['games']['gameIndexEnd']

    while next_page > begin_index:
        response = get_match_history(PLAYER_ID, next_page + 1)
        process_response(response)
        begin_index = response['games']['gameIndexBegin']
        next_page = response['games']['gameIndexEnd']
        print(next_page)


    print(champions.most_common(10))