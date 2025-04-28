import map
from db import DB
import random
from random import randint
import time
import json


boards = DB('boards')
maps = DB('maps')

def createBoard(map_id):
    m = map.getMap(map_id)
    res = boards.insert({"map_id":map_id, "w":m['w'], "h":m['h']})
    # objects = boards.select('objects')


def initBoard(id, player_id):
    b = boards.selectOne("SELECT map_id,w,h,objects FROM boards WHERE id=?",[id])
    # print(f"b ========> {b}")
    if not b:
        raise Exception(f"Board {id} not found")
    # b['objects'] = generate_objects()
    # print(b['objects'])
    boards.insert({"objects": generate_objects()})
    print("weeeeeee ===>", str(boards.selectOne("SELECT * FROM boards objects")))
    m = maps.selectOne("SELECT * FROM maps WHERE id=?",[b['map_id']])




    return {"landscape": m["landscape"], "w":b["w"], "h":b["h"]}


def generate_objects():
	objects = list()
	random.seed(time.time_ns())
	obj_am = dict()
	obj_names = ["beer", "apple", "axe", "shit", "pill"]
	for el in obj_names:
		obj_am[el] = randint(7, 30)
	for el in obj_am.keys():
		for i in range(obj_am[el]):
			objects.append({"type":el, "coord":[randint(0, 100), randint(0, 100)]})
	# print(json.dumps(objects))
	return json.dumps(objects)


if __name__ == "__main__":
    createBoard(1)