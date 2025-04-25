from db import DB
import map
import board

maps = DB('maps')
players = DB('players')

def getmap(d,o):
	o["map"] = map.getMap(d['id'])

def init_board(d,o):
	o.update(board.initBoard(d['id']))


def generate_objects():
	pass