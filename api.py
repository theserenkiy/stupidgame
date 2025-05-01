from db import DB
import map
import board
import player
import lib
import dbs
from objects_cfg import objcfg
from random import randint
import json 




def timesync(d):
	return {"time": lib.time_ms()}

def getmap(d):
	return {"map": map.getMap(d['id'])}

def init_game(d):
	out = board.initBoard(d['board_id'],d['player_id'])
	out["player"] = player.getPlayer(d['player_id'])
	out["objcfg"] = objcfg
	return out

def move(d):
	out = {"stepnum":d["stepnum"], **player.move(d["player_id"],d["dir"])}
	# print(f"yo bitch api->move out >>>>>{out}")
	return out


def heal(d):
	heal_points = 0
	heal_objs = [el for el in objcfg.keys() if objcfg[el]["type"] == "heal"]
	# inv = player.getInventory(d["player_id"])

	pl = dbs.players.c_selectId(d["player_id"], ["inventory"])
	inv = json.loads(pl["inventory"] if pl["inventory"] else '[]') 
	for slot in inv:
		for heal in heal_objs:
			print(slot.keys())
			if slot["type"] == heal:
				heal_points = objcfg[heal]["stats"]["heal"]
				del slot["items"][randint(0, len(slot["items"]) - 1)]
	dbs.players.c_updateId(inv, d["player_id"])

	hp = dbs.players.c_selectId(d["player_id"], ["hp"])
	hp["hp"] += heal_points
	dbs.players.c_updateId(hp, d["player_id"])





