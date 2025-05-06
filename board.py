import time 
import math 
import random 
import lib
import object
from objects_cfg import objcfg
import map

import dbs

def createBoard(map_id):
	m = map.getMap(map_id)
	id = dbs.boards.insert({"map_id":map_id, "w":m['w'], "h":m['h']})
	spawnObjects(id, m["w"], m["h"])
	print(f"Board id: {id}")

def initBoard(board_id,player_id):
	b = dbs.boards.c_selectId(board_id)
	if not b:
		raise Exception(f"Board {id} not found")
	print(b)
	m = dbs.maps.c_selectId(b['map_id'])
	
	objects = [dict(o) for o in dbs.objects.c_selectMany({'board_id': board_id, 'shown':1},['id','name','x','y'])]

	mycrd = lib.getRandCoord(getUsedCoords(board_id),b["w"],b["h"])

	dbs.players.update({
		"x": mycrd[0],
		"y": mycrd[1],
		"board_id": board_id
	},"id=?",[player_id])

	return {"landscape": m["landscape"], "w":b["w"], "h":b["h"], "objects": objects, "mycrd": mycrd}

def getBoardObjects(board_id):
	pass

def delObjects(board_id):
	dbs.objects.delete("board_id=?",[board_id])

def spawnObjects(board_id,w,h):
	
	# time.gmtime()
	cells_count = w * h
	map_factor = cells_count/10000
	objects = []
	used_coord = []
	for name in object.cfg:
		c = object.cfg[name]
		amount = round(c["permap"]*map_factor)
		# print(amount)
		oids = []
		for i in range(amount):
			crd = lib.getRandCoord(used_coord, w, h)
			obj = {
				"board_id": board_id,
				"name": name,
				"x": crd[0],
				"y": crd[1],
				"updated": 0,
				"shown": 1,
				"spawntime": 0
			}

			print(obj)
			oid = dbs.objects.c_insert(obj)
			oids.append(oid)
			used_coord.append(crd)



def getUsedCoords(board_id):
	pls = dbs.players.c_selectMany({"board_id":board_id},['x','y'])
	used_coords_0 = [[o["x"],o["y"]] for o in pls]

	objects = dbs.objects.c_selectMany({"board_id":board_id, "shown":1},['x','y','id'])
	
	return [[o["x"],o["y"]] for o in objects] + used_coords_0



		
def getBoardDim(id):
	return dbs.boards.c_selectId(id,['w','h'])

if __name__ == "__main__":
	delObjects(1)
	#createBoard(1)
	spawnObjects(1,100,100)
	# print()
	pass