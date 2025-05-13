from db import DB
import map
import board
import player
import lib
import dbs
import object
from cfg import cfg
from random import randint
import json 


def timesync(d):
	return {"time": lib.time_ms()}

def dbquery(d):
	# try:
	if not hasattr(dbs,d["table"]):
		raise Exception(f"Incorrect table {d['table']}")
	
	cur = getattr(dbs,d["table"]).execute(d["query"])
	rows = cur.fetchall()
	out = {
		"found": len(rows) 
	}

	if not out["found"]:
		return out
	
	
	out["keys"] = list(dict(rows[0]).keys())
	# print(list(dict(rows[0]).values()))
	# print(rows)
	out["rows"] = [list(dict(row).values()) for row in rows]
	return out
		
	# except Exception as e:
	# 	return {"db_error": str(e)}
	

def getmap(d):
	return {"map": map.getMap(d['id'])}

def init_game(d):
	out = board.initBoard(d['board_id'],d['player_id'])
	out["player"] = player.getPlayer(d['player_id'])
	out["objcfg"] = object.client_cfg
	out["charcfg"] = player.chars
	out["cfg"] = cfg
	return out

def move(d):
	out = {"stepnum":d["stepnum"], **player.move(d["player_id"],d["dir"])}
	return out


def heal(d):
	heal_points = 0
	heal_objs = [el for el in objcfg.keys() if objcfg[el]["type"] == "heal"]
	# inv = player.getInventory(d["player_id"])

	pl = dbs.players.c_selectId(d["player_id"], ["inventory","hp"])
	inv = json.loads(pl["inventory"] if pl["inventory"] else '[]') 
	for slot in inv:
		if slot["type"] in heal_objs:
			heal_points = objcfg[slot["type"]]["stats"]["heal"]
			del slot["items"][randint(0, len(slot["items"]) - 1)]
		
	dbs.players.c_updateId({"inventory": json.dumps(inv), "hp": pl["hp"]+heal_points}, d["player_id"])

def use_object(d):
	return player.useObject(d["player_id"],d["slotnum"])

def throw_object(d):
	return player.throwObject(d["player_id"],d["slotnum"])




