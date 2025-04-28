CREATE TABLE IF NOT EXISTS Players (
	id STRING PRIMARY KEY,
	name TEXT,
	hp INT DEFAULT 100,
	exp INT DEFAULT 0,
	is_online INT DEFAULT 0,
	board_id INT DEFAULT 0,
	x INT DEFAULT 0,
	y INT DEFAULT 0,
	inventory TEXT,
	buffs TEXT,
	respawn_timer INT UNSIGNED,
	token STRING,
	last_ping INT DEFAULT 0
)


