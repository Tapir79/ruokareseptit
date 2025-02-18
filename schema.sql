CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    total_rating INTEGER DEFAULT 0,
    rating_count INTEGER DEFAULT 0,
    vegan INTEGER DEFAULT 0, -- Boolean stored as 0 (FALSE) or 1 (TRUE)
    vegetarian INTEGER DEFAULT 0, -- Boolean stored as 0 (FALSE) or 1 (TRUE)
    lactose_free INTEGER DEFAULT 0, -- Boolean stored as 0 (FALSE) or 1 (TRUE)
    gluten_free INTEGER DEFAULT 0, -- Boolean stored as 0 (FALSE) or 1 (TRUE)
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
    recipe_id INTEGER REFERENCES recipes ON DELETE CASCADE,
    created_at TEXT DEFAULT (DATETIME('now')),
    UNIQUE (rated_by, recipe_id)
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
