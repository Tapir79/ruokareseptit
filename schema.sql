CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
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