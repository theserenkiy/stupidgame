from db import DB
from random import randint
from math import floor
import json

maps = DB('maps')

def createMap(w,h):
	map = []
	for x in range(w):
		map.append([])
		for y in range(h):
			avg = 0
			if x > 0: 
				avg += map[x-1][y]
			if y > 0:
				avg += map[x][y-1]
			if x and y:
				avg /= 2
			map[x].append((randint(-50,50)+floor(avg)+360)%360)

	# print(map)
	ins = maps.insert({"w":w,"h":h,"landscape":json.dumps(map)})
	print(ins)

def getMap(id):
	row = maps.selectOne("SELECT * FROM maps WHERE id=? LIMIT 1",[id])
	if not row:
		raise Exception("Карта не найдена")
	return row

def listMaps(fields="*"):
	rows = maps.select(f"SELECT {fields} FROM maps")
	print(rows)
		

if __name__ == "__main__":
	# createMap(100,100)
	# listMaps("id,w,h")
	print(dict(maps.selectOne("SELECT json_extract(landscape) AS ls FROM maps LIMIT 1",[])))
	
