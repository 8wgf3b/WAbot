import requests
import os

def relation(func, args):
    address = os.environ['BIGBRO']
    r = requests.post(address, json={'func': func, 'param':args})
    return r.json()
