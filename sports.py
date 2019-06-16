import requests
import os

def livescore():
    param = {os.environ['H1N']: os.environ['H1'], os.environ['H2N']: os.environ['H2']}
    address = os.environ['CRIC_ADDRESS']
    resp = requests.get(address + 'matches.php', headers = param)
    js = resp.json()
    lis = js['matchList']['matches']
    lis = list(filter(lambda x: x['status'] == 'LIVE', lis))
    if len(lis) == 0:
        return 'no live matches\n'
    s = ''
    for match in lis:
        s += match['homeTeam']['shortName'] + ' vs ' + match['awayTeam']['shortName'] + '\n'
        s += match['matchSummaryText'] + '\n'
        sid = str(match['series']['id'])
        mid = str(match['id'])
        resp = requests.get(address + 'scorecards.php?seriesid=' + sid + '&matchid=' + mid, headers = param)
        js1 = resp.json()
        sc = js1['fullScorecard']
        #s = md['teamBatting']['shortName'] + ' vs ' + md['teamBowling']['shortName'] + '\n'
        #s += md['tossMessage'] + '\n'
        for inn in sc['innings']:
            s += inn['name'] + '\n'
            s += inn['run'] + '-' + inn['wicket'] +  '(' + inn['over'] + ')\n\n'
            for bat in inn['batsmen']:
                if bat['balls'] == '':
                    continue
                s += bat['name'] + '  ' + bat['runs'] + '(' + bat['balls'] + ')  ' + bat['howOut'] + '\n'
            s += '\n'
            for ball in inn['bowlers']:
                s += ball['name'] +'  '+ ball['overs'] + '-' +ball['maidens']  + '-' +ball['runsConceded'] + '-' +ball['wickets']+'\n'
        s += '\n\n'
    return s


def rawreturn():
    url = "http://mapps.cricbuzz.com/cbzios/match/livematches"
    return requests.get(url).text

if __name__ == '__main__':
    print(1)
