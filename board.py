
import time 
import math 
import random 

from db import DB
from objects_cfg import objcfg
import map

boards = DB('boards')
maps = DB('maps')

def createBoard(map_id):
	m = map.getMap(map_id)
	res = boards.insert({"map_id":map_id, "w":m['w'], "h":m['h']})
# print(res)

def initBoard(id,player_id):
	b = boards.selectOne("SELECT * FROM boards WHERE id=?",[id])
	if not b:
		raise Exception(f"Board {id} not found")
	m = maps.selectOne("SELECT * FROM maps WHERE id=?",[b['map_id']])

	return {"landscape": m["landscape"], "w":b["w"], "h":b["h"]}

def spawnObjects(w,h):
	time.gmtime()
	cells_count = w*h
	oid = 1
	objects = []
	used_coord = []
	for t in objcfg:
		c = objcfg[t]
		amount = round(cells_count*c["prob"]*0.01)
		print(amount)
		for i in range(amount):
			crd = getRandCoord(used_coord,w,h)
			obj = (oid,t,crd,0)
			objects.append(obj)
			used_coord.append(crd)
			oid += 1
	return objects

def getRandCoord(used_coord,w,h):
	while True:
		crd = [
			random.randint(0,w-1), 
			random.randint(0,h-1)
		]
		if crd not in used_coord:
			return crd

def respawnObjects(objects,w,h):
	used_coord = [[o[2],o[3]] for o in objects]
	for o in objects:
		if o[4] < time.gmtime():
			crd = getRandCoord(used_coord,w,h)
		


if __name__ == "__main__":
	# createBoard(1)
	spawnObjects(100,100)
	# print()