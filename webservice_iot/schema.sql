DROP TABLE IF EXISTS users;
CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	name TEXT NOT NULL,
	username TEXT NOT NULL,
	password TEXT NOT NULL,
	access INTEGER NOT NULL
);

DROP TABLE IF EXISTS devices;
CREATE TABLE devices (
	id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	name TEXT NOT NULL,
	type INTEGER NOT NULL,
	creation_date TEXT NOT NULL
);