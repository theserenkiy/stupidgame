import dbs
import board 
import object
import lib

import json
import time
import random

INVENTORY_SLOTS = 10
MAX_WEARING = 5



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
		
		use_obj = 0
		objtype = obj["type"]
		inv = getInventory(player_id)

		res = inventoryAdd(inv,objtype)
		if 'game_error' in res:
			out.update(res)
			p = p0
			
		else:
			object.setUsed(obj["id"])
			out["objects_removed"] = [obj["id"]]
			# dbs.objects.unlock()
			inv.append({
				"type": obj["type"],
				"put_time": time.time() 
			})
			upd["inventory"] = inv
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


def inventoryAdd(inv,objtype):
	print("inventoryAdd",objtype)
	out = {}
	ocfg = object.cfg[objtype]
	
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
		if slot["type"] != objtype:
			continue
		slotlen = len(slot["items"]) if "items" in slot else 0
		objs_of_type += slotlen
		if slotlen >= ocfg["per_slot"]:
			continue
		found_slot = slot
		break

	if objs_of_type >= ocfg["user_limit"]:
		out["game_error"] = "Вы больше не можете поднять такой предмет"
		return out
	else:
		item = {
			"put_time": lib.time_ms() 
		}
		if found_slot:
			found_slot["items"].append(item)
			
		elif empty_slot:
			empty_slot.update({
				"type": objtype,
				"items": [item]
			})
			
		else:
			out["game_error"] = "Ваш рюкзак переполнен"
			return out
	return out


def getInventory(player_id):
	pl = dbs.players.c_selectId(player_id,['inventory'])
	
	return prepareInventory(pl["inventory"])

def prepareInventory(rawinv):
	"""Takes inventory field from db, parses it and prepares to use"""
	return prepareSlots(rawinv,INVENTORY_SLOTS)

def prepareWearing(raw):
	"""Takes wearing field from db, parses it and prepares to use"""
	return prepareSlots(raw,MAX_WEARING)

def prepareSlots(raw,amount):
	slots = json.loads(raw if raw else '[]') 

	ilen = len(slots) 
	if ilen < amount:
		slots += [None]*(amount-ilen)
	elif ilen > amount:
		slots = slots[0:amount]
	return slots


def clearInventory(id):
	dbs.players.c_updateId({"inventory":"[]", "wearing":"[]"},id)

def getPlayer(id):
	return dbs.players.c_selectId(id)

def useObject(player_id, slotnum):
	if slotnum < 0 or slotnum >= INVENTORY_SLOTS:
		raise Exception("Slot out of range")
	ret = {}
	upd = {}
	pl = dbs.players.c_selectId(player_id,["inventory","wearing","hp","maxhp","damage","defence"])
	inv = prepareInventory(pl["inventory"])
	slot = inv[slotnum]
	if slot["type"] == "empty":
		return ret
	
	objtype = slot["type"]
	cfg = object.cfg[objtype] if objtype in object.cfg else None
	if not cfg:
		raise Exception("Unknown item type")
	
	slot["items"] = slot["items"][:-1]
	if not len(slot["items"]):
		slot["type"] = "empty"
	
	ret["inventory"] = inv
	upd["inventory"] = inv

	# inventory changed. Now lets do some action!
	
	if cfg["group"] == "heal":
		if pl["hp"] == pl["maxhp"]:
			ret["msg"] = "Покушать - это хорошо. Но здоровее вам уже не стать!"
		else:
			pl["hp"] += cfg["stats"]["heal"]
			if pl["hp"] > pl["maxhp"]:
				pl["hp"] = pl["maxhp"]

	elif "wear_type" in cfg:
		wear = prepareWearing(pl["wearing"])
		
		same_type_slot = None
		empty_slot = None
		for i in range(MAX_WEARING):
			if not wear[i]:
				wear[i] = {"type":"empty"}
				
			slot = wear[i]
			if slot["type"]=="empty":
				if not empty_slot:
					empty_slot = wear[i]
				continue
				
			if slot["type"] == cfg["wear_type"]:
				same_type_slot = wear[i]
		


		if same_type_slot:
			print("same type slot")
			inventoryAdd(inv,same_type_slot["item"])
			slot = same_type_slot
			same_type_slot["item"] = objtype
		elif empty_slot:
			print("empty slot")
			slot = empty_slot
		slot["item"] = objtype
		slot["type"] = cfg["group"]

		upd["wearing"] = wear
		ret["wearing"] = wear


	dbs.players.c_updateId(upd,player_id)
	return ret

def genPlayers(amount):
	nicks = open("nicknames.txt").read().strip().split("\n")
	for i in range(amount):
		pl = [
			random.randint(1000000,9999999),
			random.choice(nicks)
		]
		print(pl)
		dbs.players.insert({
			"id":pl[0],
			"name":pl[1]
		})


if __name__ == '__main__':
	# genPlayers(10)
	# listPlayers()
	clearInventory(4962376)