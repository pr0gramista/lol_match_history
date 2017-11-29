import json

with open('champion.json', 'r', encoding='utf-8') as f:
    champion_data = f.read()

champion_json = json.loads(champion_data)

__champions = {}

for champion_name in champion_json['data'].keys():
    __champions.update({
        int(champion_json['data'][champion_name]['key']): champion_name
    })


def get_champion_name_for_id(i):
    if i in __champions:
        return __champions[i]
    else:
        raise KeyError()


if __name__ == '__main__':
    print(get_champion_name_for_id(int(input("Champion id:\n"))))
