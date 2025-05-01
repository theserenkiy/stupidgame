import dbs
import board 
import object
import lib
from objects_cfg import objcfg

import json
import time


INVENTORY_SLOTS = 10

def listPlayers():
	res = [dict(p) for p in dbs.players.select("SELECT * FROM players")]
	print(res)
	return res

# TODO: control speed of move — sam sdilaesh mni vpadlu
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
		ocfg = objcfg[obj["type"]]
		use_obj = 0

		if "per_slot" not in ocfg:
			ocfg["per_slot"] = 1
		
		if "limit" not in ocfg:
			ocfg["limit"] = 1

		# p = [pl["x"],pl["y"]]
		inv = getInventory(player_id)

		empty_slot = None
		found_slot = None
		objs_of_type = 0
		for i in range(INVENTORY_SLOTS):
			slot = inv[i]
			if not slot:
				inv[i] = {"type":"empty", "items":[]}
				slot = inv[i] 
			if slot["type"] == "empty" and not empty_slot:
				empty_slot = slot
			if slot["type"] != obj["type"]:
				continue
			slotlen = len(slot["items"]) if "items" in slot else 0
			objs_of_type += slotlen
			if slotlen >= ocfg["per_slot"]:
				continue
			found_slot = slot
			break

		if objs_of_type >= ocfg["limit"]:
			out["game_error"] = "Вы больше не можете поднять такой предмет"
			p = p0
		else:
			item = {
				"put_time": lib.time_ms() 
			}
			if found_slot:
				found_slot["items"].append(item)
				use_obj = 1
			elif empty_slot:
				empty_slot.update({
					"type": obj["type"],
					"items": [item]
				})
				use_obj = 1
			else:
				out["game_error"] = "Ваш рюкзак переполнен"
				p = p0
			
		if use_obj:
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
	
	upd["last_ping"] = lib.time_ms()
	if len(upd.keys()):
		dbs.players.c_updateId(upd, player_id)

	out["pos"] = p
	return out


def getInventory(player_id):
	pl = dbs.players.c_selectId(player_id,['inventory'])
	inv = json.loads(pl["inventory"] if pl["inventory"] else '[]') 

	ilen = len(inv) 
	if ilen < INVENTORY_SLOTS:
		inv += [None]*(INVENTORY_SLOTS-ilen)
	elif ilen > INVENTORY_SLOTS:
		inv = inv[0:INVENTORY_SLOTS]
	return inv

def clearInventory(id):
	dbs.players.c_updateId({"inventory":"[]"},id)

def getPlayer(id):
	return dbs.players.c_selectId(id)


if __name__ == '__main__':
	listPlayers()
	clearInventory(5146213)