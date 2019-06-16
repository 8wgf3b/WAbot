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
        sid = str(match['series']['id'])
        mid = str(match['id'])
        resp = requests.get(address + 'matchdetail.php?seriesid=' + sid + '&matchid=' + mid, headers = param)
        js1 = resp.json()
        md = js1['matchDetail']
        s = md['teamBatting']['shortName'] + ' vs ' + md['teamBowling']['shortName'] + '\n'
        s += md['tossMessage'] + '\n'
        for i in md['innings']:
            s += i['shortName'] + ': ' + str(i['runs']) + '-' + str(i['wickets']) + ' (' + str(i['overs']) +')\n'
        a = set()
        for cb in md['currentBatters']:
            if cb['name'] not in a:
                a.add(cb['name'])
            else:
                continue
            if cb['isFacing']  == True:
                cb['name'] += '*'
            s += cb['name'] + ': ' + cb['runs'] + ' (' + cb['ballsFaced'] + ') ' + 'SR: ' + cb['strikeRate'] + '\n'

        s += '\n\n'
    return s


def rawreturn():
    url = "http://mapps.cricbuzz.com/cbzios/match/livematches"
    return requests.get(url).text

if __name__ == '__main__':
    print(1)
