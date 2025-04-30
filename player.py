import dbs
import board 
import object
import json
import time
from objects_cfg import objcfg

INVENTORY_CAPACITY = 10

def listPlayers():
	res = [dict(p) for p in dbs.players.select("SELECT * FROM players")]
	print(res)
	return res

# TODO: control speed of move
def move(player_id,dir):
	out = {}
	upd = {}
	pl = dbs.players.c_selectId(player_id,['x','y','board_id'])
	brd = board.getBoardDim(pl["board_id"])

	p0 = [pl["x"], pl["y"]] 
	p = [pl["x"]+dir[0], pl["y"]+dir[1]]
	if p[0] < 0:
		p[0] = 0
	if p[0] >= brd["w"]:
		p[0] = brd["w"]-1
	if p[1] < 0:
		p[1] = 0
	if p[1] >= brd["h"]:
		p[1] = brd["h"]-1
	
	# dbs.objects.lock()
	obj = object.getObjectAtCoord(p)
	if obj:
		print(obj)
		# p = [pl["x"],pl["y"]]
		pl_ = dbs.players.c_selectId(player_id,['inventory'])
		inv = json.loads(pl_["inventory"] if pl_["inventory"] else '[]') 
		if len(inv) >= INVENTORY_CAPACITY:
			out["game_error"] = "Ваш рюкзак переполнен"
			p = p0
		else:
			cfg = objcfg[obj["type"]]
			lim = cfg["limit"] if "limit" in cfg else 1
			count = len([o for o in inv if o["type"]==obj["type"]])
			if count >= lim:
				out["game_error"] = "Вы больше не можете поднять такой предмет"
				p = p0
			else:
				object.setUsed(obj["id"])
				out["objects_removed"] = [obj["id"]]
				# dbs.objects.unlock()
				inv.append({
					"type": obj["type"],
					"put_time": time.time() 
				})
				upd["inventory"] = json.dumps(inv)
				out["inventory"] = inv
		
		# dbs.objects.unlock()
	
	# dbs.objects.unlock()
	if p != p0:
		upd.update({"x":p[0],"y":p[1]})
	
	if len(upd.keys()):
		dbs.players.c_updateId(upd,player_id)

	out["pos"] = p
	return out

def clearInventory(id):
	dbs.players.c_updateId({"inventory":"[]"},id)

def getPlayer(id):
	return dbs.players.c_selectId(id)


if __name__ == '__main__':
	listPlayers()
	clearInventory(5146213)