from json import load, dump
from json.decoder import JSONDecodeError
from time import sleep

def sort():
    try:
        json_data = load(open('data.json', 'r'))

        f = open('bannedusers.txt', 'r')
        bannedusers = f.readlines()
        bannedusers = [banneduser.replace('\n', '') for banneduser in bannedusers]
   
        bannable = []
        
        for user in json_data:
            if user['reportable'] and user['name'] not in bannedusers:
                bannable.append(user)

        dump(bannable, open('bannable.json', 'w'), indent=4)
        f.close()

        return bannable
    except FileNotFoundError:
        print('\'bannedusers.txt\' Not found')

