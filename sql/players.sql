CREATE TABLE IF NOT EXISTS Players (
	id STRING PRIMARY KEY,
	name TEXT,
	char INT,
	hp INT DEFAULT 100,
	maxhp INT DEFAULT 100,
	agility INT DEFAULT 20,
	base_agility INT DEFAULT 20,
	exp INT DEFAULT 0,
	damage INT DEFAULT 2,
	base_damage INT DEFAULT 2,
	defence INT DEFAULT 0,
	base_defence INT DEFAULT 0,
	is_online INT DEFAULT 0,
	board_id INT DEFAULT 0,
	x INT DEFAULT 0,
	y INT DEFAULT 0,
	xdir STRING DEFAULT 'left',
	inventory TEXT,
	wearing TEXT,
	buffs TEXT,
	respawn_timer INT UNSIGNED,
	token STRING,
	last_ping INT DEFAULT 0,
	updated INT DEFAULT 0
)


