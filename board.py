
import time 
import math 
import random 

from db import DB
from objects_cfg import objcfg
import map

players_db = DB("players")
boards_db = DB('boards')
maps_db = DB('maps')
objects_db = DB("objects")

def createBoard(map_id):
	m = map.getMap(map_id)
	id = boards_db.insert({"map_id":map_id, "w":m['w'], "h":m['h']})
	spawnObjects(id, m["w"], m["h"])
	print(f"Board id: {id}")

def initBoard(board_id,player_id):
	b = boards_db.selectOne("SELECT * FROM boards WHERE id=?",[board_id])
	if not b:
		raise Exception(f"Board {id} not found")
	print(b)
	m = maps_db.selectOne("SELECT * FROM maps WHERE id=?",[b['map_id']])
	
	objects = [dict(o) for o in objects_db.select("SELECT id,type,x,y FROM objects WHERE board_id=? AND shown=1",[board_id])]

	mycrd = getRandCoord(getUsedCoords(board_id),b["w"],b["h"])

	players_db.update({
		"x": mycrd[0],
		"y": mycrd[1],
		"board_id": board_id
	},"id=?",[player_id])

	return {"landscape": m["landscape"], "w":b["w"], "h":b["h"], "objects": objects, "mycrd": mycrd}

def getBoardObjects(board_id):
	pass


def spawnObjects(board_id,w,h):
	
	# time.gmtime()
	cells_count = w * h
	objects = []
	used_coord = []
	for t in objcfg:
		c = objcfg[t]
		amount = round(cells_count * c["prob"] * 0.003)
		# print(amount)
		oids = []
		for i in range(amount):
			crd = getRandCoord(used_coord, w, h)
			obj = {
				"board_id": board_id,
				"type": t,
				"x": crd[0],
				"y": crd[1],
				"updated": 0,
				"shown": 1,
				"spawntime": 0
			}

			print(obj)
			oid = objects_db.insert(obj)
			oids.append(oid)
			used_coord.append(crd)


def getRandCoord(used_coord,w,h):
	while True:
		crd = [
			random.randint(0,w-1), 
			random.randint(0,h-1)
		]
		if crd not in used_coord:
			return crd


def getUsedCoords(board_id):
	pls = players_db.select("SELECT x,y FROM players WHERE board_id=?",[board_id])
	used_coords_0 = [[o["x"],o["y"]] for o in pls]

	objects = objects_db.select(
		"SELECT x,y,id FROM objects WHERE board_id=? AND shown=1",
		[board_id]
	)
	
	return [[o["x"],o["y"]] for o in objects] + used_coords_0


def respawnObjects(board_id):
	resp_objects = objects_db.select(
		"SELECT id FROM objects WHERE board_id=? AND shown=0 AND spawntime <= ?",
		[board_id,time.gmtime()]
	)
	
	if not len(resp_objects):
		return
	
	for o in resp_objects:
		crd = getRandCoord(getUsedCoords(board_id),w,h)
		upd = {
			"x": crd[0],
			"y": crd[1],
			"shown": 1,
			"spawntime": 0
		}
		objects_db.execute(upd,"id=?",[o.id])
		


if __name__ == "__main__":
	#createBoard(1)
	# spawnObjects(100,100)
	# print()
	pass