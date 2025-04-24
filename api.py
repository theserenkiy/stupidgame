from db import DB
import map
import board

maps = DB('maps')
players = DB('players')

def getmap(d,o):
    map.getMap(d.id)
    
    

    