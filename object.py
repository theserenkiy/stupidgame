import dbs
import lib
import board
import time

def getObjectAtCoord(crd):
	objs = dbs.objects.c_selectMany({"x":crd[0], "y":crd[1], "shown":1})
	return objs[0] if len(objs) else None


def respawnObjects(board_id,w,h):
	resp_objects = dbs.objects.select(
		"SELECT id FROM objects WHERE board_id=? AND shown=0 AND spawntime <= ?",
		[board_id,round(time.time())]
	)
	 
	if not len(resp_objects):
		return
	
	for o in resp_objects:
		crd = lib.getRandCoord(board.getUsedCoords(board_id),w,h)
		upd = {
			"x": crd[0],
			"y": crd[1],
			"shown": 1,
			"spawntime": 0
		}
		dbs.objects.c_updateId(upd,o.id)

def setUsed(id):
	dbs.objects.c_updateId({"shown":0},id)