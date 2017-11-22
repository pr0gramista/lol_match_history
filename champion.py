import json

champion_id = input("Champion id:\n")

with open('champion.json', 'r', encoding='utf-8') as f:
    champion_data = f.read()

champion_json = json.loads(champion_data)

for champion_name in champion_json['data'].keys():
    if champion_json['data'][champion_name]['key'] == champion_id:
        print("It's {}".format(champion_name))
        break