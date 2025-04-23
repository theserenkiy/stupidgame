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

	print(map)
	maps.execute('INSERT INTO maps (landscape) VALUES (?)',[json.dumps(map)])


def listMaps():
	print(maps.execute('SELECT * FROM maps'))


createMap(10,10)
listMaps()