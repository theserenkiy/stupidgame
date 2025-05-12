import dbs
import lib
import board
import time
from objects_cfg import spritemap, objcfg
import json

cfg = {}
client_cfg = {}

def getObjectAtCoord(crd):
	objs = dbs.objects.c_selectMany({"x":crd[0], "y":crd[1], "shown":1})
	return objs[0] if len(objs) else None




def setUsed(id):
	dbs.objects.c_updateId({"shown":0},id)

def compileCfg():
	try:
		item_sprites = {}
		for sname in spritemap:
			spr = spritemap[sname]
			imw = int(spr["w"]/spr["nx"])
			imh = int(spr["h"]/spr["ny"])
			
			for i in range(len(spr["map"])):
				name = spr["map"][i]
				if not name:
					continue
				if name in item_sprites:
					dupsprite = item_sprites[name]["sprite"]
					raise Exception(f"Duplicate image for item {name}: sprites {dupsprite} and {sname}")
				item_sprites[name] = {
					"sprite": sname,
					"x": int(i%spr["nx"]),
					"y": int(i/spr["nx"]),
					"w": imw,
					"h": imh
				}

		itemlist = item_sprites.keys()
		
		ocls = [v.split("_") for v in [k for k in objcfg.keys() if k not in itemlist]+list(itemlist)]
		ocls.sort(key=lambda v: len(v))
		# print(ocls)

		for c in ocls:
			cname = "_".join(c)
			cls = objcfg[cname] if cname in objcfg else {}

			scname = None
			if len(c) > 1:
				for i in range(len(c)-1):
					scname = "_".join(c[:-(i+1)])
					if scname in objcfg:
						break
			if scname:
				if scname not in objcfg:
					raise Exception(f"Cannot find super '{scname}' for {cname}")
				super = objcfg[scname]
				
				for k in cls:
					if isinstance(cls[k], float):
						if k not in super:
							raise Exception(f"Class {scname} has no field {k} for subclass {cname}")
						cls[k] *= super[k]
				
				for k in super:
					if k not in cls:
						cls[k] = super[k]
					elif isinstance(cls[k], float):
						cls[k] = round(cls[k]*super[k])
			
			if cls["group"]=="weapon":
				cls["wear_type"] = "weapon"

			if "permap" not in cls:
				raise Exception(f"Missing class_permap for {cname}")
			
			if "per_slot" not in cls:
				cls["per_slot"] = 1

			if "user_limit" not in cls:
				cls["user_limit"] = 1

			if "desc" not in cls:
				cls["desc"] = ""
			
			if cname in item_sprites:
				cls["icon"] = item_sprites[cname]
				cfg[cname] = cls
				client_cfg[cname] = cls
				if "wear_type" not in cls:
					client_cfg[cname]["wear_type"] = ""
			
		print(json.dumps(client_cfg,ensure_ascii=False))	

	except Exception as e:
		raise Exception("CompileCfg error: "+str(e))



if __name__ == "__main__":
	compileCfg()

	
