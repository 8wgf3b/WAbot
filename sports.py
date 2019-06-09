from utils.cricbuzz import Cricbuzz
import requests

def getmatches():
    c = Cricbuzz()
    matches = c.matches()
    message = ''
    for match in matches:
        message += match['id'] + '\n' + match['team1']['name'] + ' vs ' + match['team2']['name'] + '\n' + match['status'] + '\n\n'
    return message

def livescores(mid=None):
    c = Cricbuzz()
    matches = c.matches()
def rawreturn():
    url = "http://mapps.cricbuzz.com/cbzios/match/livematches"
    return requests.get(url).text

if __name__ == '__main__':
    print(rawreturn()[:100])
