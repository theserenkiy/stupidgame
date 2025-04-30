# (group, probability, respawn_sec, strength, [buf_type, buf_time])
# groups: 0: heal, 1: weapon, 2: clothes, 3: buf 
# probability - to appear on cell
# strength: (0-100) 
#   heal - 0-100 (in HPs), how many HP returns when used
#   weapon - 1-100 (in HPs), damage - enemy's HP loss per one attack
#   clothes - 1-99 (in %), HP loss defence per enemy attack
#       (i.e. if cloth k = 80 then if enemy's weapon 
#       chould decrease HP by 10 points, it will decrease by 8 only)
#   buf - 1-100 (in %), how many buf specific parameter increased during the buf
#   buf_type: 
#       0 - hp
#       1 - damage 
#       2 - other 
#   buf_time: time while the buf works, sec


objcfg = {
    "apple":{
		"type": "heal",
		"prob": 0.7,
		"resp":	60,
		"limit": 50,
        "per_slot": 5,
		"stats": {
			"heal": 20
		}
	},
	"water":{
		"type": "heal",
		"prob": 0.5,
		"resp":	60,
        "limit": 20,
        "per_slot": 3,
		"stats": {
			"heal": 15
		}
	},
    "axe": {
		"type": "weapon",
		"prob": 0.3,
		"resp":	100,
		"stats": {
			"damage": 20
		}
	},
	"sword": {
		"type": "weapon",
		"prob": 0.25,
		"resp":	100,
		"stats": {
			"damage": 25
		}
	},
    "knife": {
		"type": "weapon",
		"prob": 0.5,
		"resp":	100,
		"stats": {
			"damage": 10
		}
	},
	"hammer": {
		"type": "weapon",
		"prob": 0.5,
		"resp":	100,
		"stats": {
			"damage": 7
		}
	},
	# "helmet": {
	# 	"type": "cloth",
	# 	"prob": 0.1,
	# 	"resp":	100,
	# 	"stats": {
	# 		"defence": 20,
	# 		"hp_add": 10
	# 	}
	# },
	"shield": {
		"type": "cloth",
		"prob": 0.05,
		"resp":	100,
		"stats": {
			"defence": 60,
			"hp_add": 5
		}
	},
    # "boots": {
	# 	"type": "cloth",
	# 	"prob": 0.05,
	# 	"resp":	100,
	# 	"stats": {
	# 		"defence": 10,
	# 		"damage_add": 10, 
	# 		"hp_add": 5
	# 	}
	# },
}