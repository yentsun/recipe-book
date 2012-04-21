CREATE TABLE amount_per_unit (
    "product_title" VARCHAR NOT NULL,
    "unit_title" VARCHAR NOT NULL,
    "amount" INTEGER NOT NULL
)
CREATE TABLE ingredients (
    "recipe_title" VARCHAR NOT NULL,
    "product_title" VARCHAR NOT NULL,
    "amount" INTEGER NOT NULL,
    "unit_title" VARCHAR
)
CREATE TABLE products (
	title VARCHAR NOT NULL,
	PRIMARY KEY (title)
)
CREATE TABLE recipes (
	title VARCHAR NOT NULL,
	description VARCHAR,
	PRIMARY KEY (title)
)
CREATE TABLE steps (
    "recipe_title" VARCHAR NOT NULL,
    "number" INTEGER NOT NULL,
    "time_value" INTEGER,
    "text" VARCHAR NOT NULL,
    "note" VARCHAR
)
CREATE TABLE units (
	title VARCHAR NOT NULL,
	abbr VARCHAR,
	PRIMARY KEY (title)
)
CREATE TABLE users (
	email VARCHAR(320) NOT NULL,
	hash CHAR(32) NOT NULL,
	PRIMARY KEY (email)
)
CREATE TABLE groups (
	title VARCHAR(20) NOT NULL,
	PRIMARY KEY (title)
)
CREATE TABLE user_groups (
	user_email VARCHAR(320) NOT NULL,
	group_title VARCHAR(20),
	PRIMARY KEY (user_email),
	FOREIGN KEY(user_email) REFERENCES users (email),
	FOREIGN KEY(group_title) REFERENCES groups (title)
)