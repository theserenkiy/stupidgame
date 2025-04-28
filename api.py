from db import DB
import map
import board
from random import randint
import random
import time
import json


boards = DB('boards')
maps = DB('maps')
players = DB('players')

def getmap(d,o):
	o["map"] = map.getMap(d['id'])

def init_board(d,o):
	o.update(board.initBoard(d['id'], d['player_id']))


def get_objects(d, o):
	objects = boards.selectOne("SELECT * FROM boards objects")
	return json.dumps(objects)



# def generate_objects(d, o):
# 	objects = list()
# 	random.seed(time.time_ns())
# 	obj_am = dict()
# 	obj_names = ["beer", "apple", "axe", "shit", "pill"]
# 	for el in obj_names:
# 		obj_am[el] = randint(7, 30)
# 	for el in obj_am.keys():
# 		for i in range(obj_am[el]):
# 			objects.append({"type":el, "coord":[randint(0, 100), randint(0, 100)]})
# 	print(json.dumps(objects))
# 	return json.dumps(objects)


if __name__ == "__main__":
	pass
	# generate_objects(0, 0)