from db import DB 
from random import randint, choice

print(DB)

players = DB('players')

amount = 10

nicks = open("nicknames.txt").read().strip().split("\n")

for i in range(amount):
    pl = [
        randint(1000000,9999999),
        choice(nicks)
    ]
    print(pl)
    players.insert({
        "id":randint(1000000,9999999),
        "name":choice(nicks)
    })


print(dict(players.selectOne("SELECT * FROM players LIMIT 1")))