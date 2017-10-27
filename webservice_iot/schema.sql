DROP TABLE IF EXISTS users;
CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	name TEXT NOT NULL,
	username TEXT NOT NULL,
	password TEXT NOT NULL,
	access_level INTEGER NOT NULL,
	creation_date TEXT NOT NULL
);

DROP TABLE IF EXISTS devices;
CREATE TABLE devices (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	name TEXT NOT NULL,
	type INTEGER NOT NULL,
	status INTEGER NOT NULL,
	creation_date TEXT NOT NULL
);

DROP TABLE IF EXISTS devices_permissions;
CREATE TABLE devices_permissions (
	users_id INTEGER NOT NULL,
	device_id INTEGER NOT NULL,
	access_level INTEGER NOT NULL,
	FOREIGN KEY(users_id) REFERENCES users(id),
	FOREIGN KEY(device_id) REFERENCES devices(id)
);