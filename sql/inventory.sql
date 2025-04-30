CREATE TABLE IF NOT EXISTS Inventory (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	player_id INTEGER,
	objtype STRING,
	obj_id INTEGER,
	slot_num INTEGER,
	added_time INTEGER
)


