CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    cuisine_id INTEGER REFERENCES cuisines,
    user_id INTEGER REFERENCES users
);

CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE recipe_ingredients (
    id INTEGER PRIMARY KEY,
    amount TEXT NOT NULL,  -- "1 cup", "200g", "2 tsp"
    recipe_id INTEGER REFERENCES recipes ON DELETE CASCADE,
    ingredient_id INTEGER REFERENCES ingredients ON DELETE CASCADE
);

CREATE TABLE recipe_instructions (
    id INTEGER PRIMARY KEY,
    instruction TEXT NOT NULL,
    step_number INTEGER NOT NULL,
    recipe_id INTEGER REFERENCES recipes ON DELETE CASCADE
);

CREATE TABLE ratings (
    id INTEGER PRIMARY KEY,
    comment TEXT,
    stars INTEGER, -- TODO
    rated_by INTEGER REFERENCES users,
    recipe_id INTEGER REFERENCES recipes
);

CREATE TABLE cuisines (
    id INTEGER PRIMARY KEY,
    name TEXT
);

-- TODO move into separate init db file
INSERT INTO cuisines (name) VALUES 
    ('Pohjoismainen'),
    ('Eurooppalainen'),
    ('Aasialainen'),
    ('Lähi-idän keittiö'),
    ('Afrikkalainen'),
    ('Latinalaisamerikkalainen'),
    ('Pohjoisamerikkalainen'),
    ('Australialainen & Oseanialainen');
