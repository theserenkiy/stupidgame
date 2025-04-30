from db import DB
import map
import board
import player
import lib

def timesync(d):
	return {"time": lib.time_ms()}

def getmap(d):
	return {"map": map.getMap(d['id'])}

def init_game(d):
	out = board.initBoard(d['board_id'],d['player_id'])
	out["player"] = player.getPlayer(d['player_id'])
	return out

def move(d):
	return {"stepnum":d["stepnum"], **player.move(d["player_id"],d["dir"])}

def generate_objects():
	pass