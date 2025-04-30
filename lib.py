import random
import time

def getRandCoord(used_coord,w,h):
	for i in range(1000):
		crd = [
			random.randint(0,w-1), 
			random.randint(0,h-1)
		]
		if crd not in used_coord:
			return crd
	raise Exception(f"Cannot get random coord")

def time_ms():
	return round(time.time()*1000)