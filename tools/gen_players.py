import DB 
from random import randint, choice

players = DB('players')

amount = 10

nicks = open("nicknames.txt").read().crop().split("\n")

for i in range(amount):
    pl = [
        randint(1000000,9999999),
        choice(nicks)
    ]
    print(pl)
    # players.execute("INSERT INTO players (id, name) VALUES (?,?)",pl)