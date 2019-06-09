from pycricbuzz import Cricbuzz

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

if __name__ == '__main__':
    print(getmatches())
