import json
import csv
from urllib.parse import urlencode
from urllib.request import urlopen

def safe(d, key):
    if key in d:
        return d[key]
    else:
        return "UNDEFINED"


def get_match_responses(player_id, begin_index=0):
    base = 'https://acs.leagueoflegends.com/v1/stats/player_history/EUN1/{}?'.format(player_id)
    params = urlencode({
        'begIndex': begin_index
    })
    response = json.load(urlopen(base + params), encoding='utf8')
    next_page = response['games']['gameIndexEnd']
    yield response

    while next_page > begin_index:
        params = urlencode({
                'begIndex': next_page
        })
        response = json.load(urlopen(base + params), encoding='utf8')
        begin_index = response['games']['gameIndexBegin']
        next_page = response['games']['gameIndexEnd']
        print(next_page)
        yield response

PLAYER_ID = 30317666

if __name__ == '__main__':
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow([
            "gameId",
            "platformId",
            "gameCreation",
            "gameDuration",
            "queueId",
            "mapId",
            "seasonId",
            "gameVersion",
            "gameMode",
            "gameType",
            "teamId",
            "championId",
            "spell1Id",
            "spell2Id",
            "role",
            "lane",
            "win",
            "kills",
            "deaths",
            "assists",
            "largestKillingSpree",
            "largestMultiKill",
            "killingSprees",
            "longestTimeSpentLiving",
            "doubleKills",
            "tripleKills",
            "quadraKills",
            "pentaKills",
            "unrealKills",
            "totalDamageDealt",
            "magicDamageDealt",
            "physicalDamageDealt",
            "trueDamageDealt",
            "largestCriticalStrike",
            "totalDamageDealtToChampions",
            "magicDamageDealtToChampions",
            "physicalDamageDealtToChampions",
            "trueDamageDealtToChampions",
            "totalHeal",
            "totalUnitsHealed",
            "damageSelfMitigated",
            "damageDealtToObjectives",
            "damageDealtToTurrets",
            "visionScore",
            "timeCCingOthers",
            "totalDamageTaken",
            "magicalDamageTaken",
            "physicalDamageTaken",
            "trueDamageTaken",
            "goldEarned",
            "goldSpent",
            "turretKills",
            "inhibitorKills",
            "totalMinionsKilled",
            "totalTimeCrowdControlDealt",
            "champLevel",
            "visionWardsBoughtInGame",
            "sightWardsBoughtInGame",
            "wardsPlaced",
            "wardsKilled"])

        for response in get_match_responses(PLAYER_ID):
            games = response['games']['games']
            for game in games:
                data = game["participants"][0]
                stats = data["stats"]
                timeline = data["timeline"]

                writer.writerow([
                    safe(game, "gameId"),
                    safe(game, "platformId"),
                    safe(game, "gameCreation"),
                    safe(game, "gameDuration"),
                    safe(game, "queueId"),
                    safe(game, "mapId"),
                    safe(game, "seasonId"),
                    safe(game, "gameVersion"),
                    safe(game, "gameMode"),
                    safe(game, "gameType"),
                    safe(data, "teamId"),
                    safe(data, "championId"),
                    safe(data, "spell1Id"),
                    safe(data, "spell2Id"),
                    safe(timeline, "role"),
                    safe(timeline, "lane"),
                    safe(stats, "win"),
                    safe(stats, "kills"),
                    safe(stats, "deaths"),
                    safe(stats, "assists"),
                    safe(stats, "largestKillingSpree"),
                    safe(stats, "largestMultiKill"),
                    safe(stats, "killingSprees"),
                    safe(stats, "longestTimeSpentLiving"),
                    safe(stats, "doubleKills"),
                    safe(stats, "tripleKills"),
                    safe(stats, "quadraKills"),
                    safe(stats, "pentaKills"),
                    safe(stats, "unrealKills"),
                    safe(stats, "totalDamageDealt"),
                    safe(stats, "magicDamageDealt"),
                    safe(stats, "physicalDamageDealt"),
                    safe(stats, "trueDamageDealt"),
                    safe(stats, "largestCriticalStrike"),
                    safe(stats, "totalDamageDealtToChampions"),
                    safe(stats, "magicDamageDealtToChampions"),
                    safe(stats, "physicalDamageDealtToChampions"),
                    safe(stats, "trueDamageDealtToChampions"),
                    safe(stats, "totalHeal"),
                    safe(stats, "totalUnitsHealed"),
                    safe(stats, "damageSelfMitigated"),
                    safe(stats, "damageDealtToObjectives"),
                    safe(stats, "damageDealtToTurrets"),
                    safe(stats, "visionScore"),
                    safe(stats, "timeCCingOthers"),
                    safe(stats, "totalDamageTaken"),
                    safe(stats, "magicalDamageTaken"),
                    safe(stats, "physicalDamageTaken"),
                    safe(stats, "trueDamageTaken"),
                    safe(stats, "goldEarned"),
                    safe(stats, "goldSpent"),
                    safe(stats, "turretKills"),
                    safe(stats, "inhibitorKills"),
                    safe(stats, "totalMinionsKilled"),
                    safe(stats, "totalTimeCrowdControlDealt"),
                    safe(stats, "champLevel"),
                    safe(stats, "visionWardsBoughtInGame"),
                    safe(stats, "sightWardsBoughtInGame"),
                    safe(stats, "wardsPlaced"),
                    safe(stats, "wardsKilled"),
                ])