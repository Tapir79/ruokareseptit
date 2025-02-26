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

CREATE TABLE recipe_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    image BLOB NOT NULL,
    recipe_id INTEGER REFERENCES recipes ON DELETE CASCADE
);

-- indices to speed up queries and joins
CREATE INDEX idx_recipes_title ON recipes(title);
CREATE INDEX idx_recipes_cuisine ON recipes(cuisine_id);
CREATE INDEX idx_recipes_user ON recipes(user_id);
CREATE INDEX idx_recipe_ingredients_recipe ON recipe_ingredients(recipe_id);
CREATE INDEX idx_recipe_ingredients_ingredient ON recipe_ingredients(ingredient_id);
CREATE INDEX idx_recipe_instructions_recipe ON recipe_instructions(recipe_id);
CREATE INDEX idx_ratings_recipe ON ratings(recipe_id);
CREATE INDEX idx_recipe_images_recipe ON recipe_images(recipe_id);