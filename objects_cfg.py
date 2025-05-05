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

spritemap = {
	"sprite1": (
		"bat_spiked",	"helmet_blueyellow",	"helmet_grayyellow",	"helmet_horned",	"shield_bluewhite",	"shield_redwhite",
		"sword_big",	"helmet_grayred",		"helmet_graygray",		"sword_triangle",	"sword_pirate",		"knife_kitchen",
		"green_gras",	"food_mushroom_unknown","food_water_bottle",			"knife_scythe",		"knife_pig",		"knife_cleaver",
		"food_chocolate","food_hotdog",			"armor_metal",			"food_beer",		"helmet_metal",		"armor_bullet1",
		"knife_cardboard","skull",				"shit",					"food_apple",		"shield_yellow",	"armor_bullet2",
		"knife_long",	"bat_golf",				"axe_red",				"shield_wooden",	"axe_big",			""
	)
}


objcfg = {
	"food":{
		"group": "heal",
		"class_permap": 200,	# total objects of class per map 100x100
		"user_limit": 50,		# max items of one item user can hold in inventory
		"per_slot":	5,			# max items per slot
		"resp": 100,			# respawn seconds
		"heal": 20,			# hp add when used
		"delay": 5000		# delay after use, before you can heal next time, ms
	},

	"axe":{
		"group": "weapon",
		"resp": 100,
		"class_permap": 30,
		"damage": 20,
		"speed": 5,		# strikes per 10 seconds
		"desc": "Топор. Не самое быстрое и не самое меткое оружие"
	},

	"bat":{
		"group": "weapon",
		"resp": 70,
		"class_permap": 50,
		"damage": 5,
		"speed": 7
	},

	"sword": {
		"group": "weapon",
		"class_permap": 20,
		"resp":	100,
		"damage": 15,
		"speed": 8,
		"desc": "Меч. Позволяет почувствовать себя рыцарем. И заодно - эстетично искромсать противника"
	},

	"knife": {
		"group": "weapon",
		"class_permap": 70,
		"resp":	60,
		"damage": 7,
		"speed": 10,
		"desc": "Ножик. Лучший аргумент в вашу пользу в кулачном бою"
	},

	"helmet": {
		"group": "cloth",
		"wear_on": "head",
		"class_permap": 50,
		"resp":	60,
		"defense": 7,
		"desc": "Шлем. Защищает черепную полость от побоев"
	},

    "food_apple":{
		"desc": "Натуральное яблочко с бабушкиной грядки, без ГМО и красителей, выращено с любовью",
	},
	"food_water":{
		"desc": "Вода из экологически чистых горных родников, повышает иммунитет, дарит заряд бодрости",
		"heal": 0.66
	},
    "axe_red": {
		"desc": "Топорик вообще-то для рубки дров. Но и пару дурных черепов при его помощи расшибить - не проблема"
	},
	"axe_big": {
		"desc": "Топор, специально спроектированный инженерами для усмирения граждан",
		"damage": 1.5
	},
	"bat_spiked": {
		"desc": "Дубина с шипами, убить не убьёт, но покалечит",
		"damage": 1.5	
	},
	"bat_golf": {
		"desc": "Клюшка для гольфа. Удобно махать, может легко надавать по мордасам недоброжелательному гражданину"
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