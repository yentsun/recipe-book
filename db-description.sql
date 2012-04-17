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