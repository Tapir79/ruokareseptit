import db

def get_recipes():
    sql = """SELECT id, 
                    title, 
                    description,
                    user_id 
             FROM recipes 
             ORDER BY id DESC"""
    return db.query(sql)


def get_recipe(recipe_id):
    sql = """SELECT recipes.id, 
                    recipes.title, 
                    recipes.description,
                    recipes.user_id, 
                    users.username 
             FROM recipes JOIN users ON recipes.user_id = users.id
             WHERE recipes.id = ?"""
    result = db.query(sql, [recipe_id])
    return result[0] if result else None

def get_recipe_ingredients(recipe_id):
    sql = """SELECT recipes.id,
                    recipe_ingredients.amount,
                    ingredients.name,
                    ingredients.id as ingredient_id
             FROM recipes JOIN recipe_ingredients ON recipe_ingredients.recipe_id = recipes.id
             JOIN ingredients ON recipe_ingredients.ingredient_id = ingredients.id
             WHERE recipes.id = ?"""
    result = db.query(sql, [recipe_id])
    return result

def add_recipe(title, description, user_id):
    sql = """INSERT INTO recipes (title, description, user_id)
             VALUES (?, ?, ?)"""
    db.execute(sql, [title, description, user_id])
    last_insert_id = db.last_insert_id()
    return last_insert_id


def edit_recipe(recipe_id, title, description):
    sql = """UPDATE recipes SET title = ?, 
                                description = ?
                            WHERE id = ?"""
    db.execute(sql, [title, description, recipe_id])


def remove_unused_ingredients():
    sql_unused_ingredients = """DELETE FROM ingredients
                                WHERE id NOT IN
                                    (SELECT ingredient_id FROM recipe_ingredients)"""
    db.execute(sql_unused_ingredients)

def remove_recipe(recipe_id):
    sql = """DELETE FROM recipes WHERE id = ?"""
    db.execute(sql, [recipe_id])

    remove_unused_ingredients()


def find_recipes(query):
    sql = """SELECT recipes.id,
                    recipes.title,
                    recipes.description,
                    recipes.user_id,
                    users.username
             FROM recipes JOIN users ON recipes.user_id = users.id
             WHERE recipes.title LIKE ? OR recipes.description LIKE ?
             ORDER BY recipes.id DESC"""

    search_term = f"%{ query }%"
    return db.query(sql, [search_term, search_term])

def add_ingredient(recipe_id, name, amount):
    sql = """SELECT name FROM ingredients WHERE name = ?"""
    result = db.query(sql, [name])
    if result:
        ingredient_name = result[0]["name"]
        raise Exception(f"{ingredient_name} on jo lisätty")

    sql = """INSERT INTO ingredients (name) VALUES (?)"""
    db.execute(sql, [name])
    ingredient_id = db.last_insert_id()

    sql = """INSERT INTO recipe_ingredients (recipe_id, ingredient_id, amount)
             VALUES (?, ?, ?)"""
    db.execute(sql, [recipe_id, ingredient_id, amount])

def edit_ingredient(recipe_id, ingredient_id, new_amount):
    sql_update_amount = """UPDATE recipe_ingredients 
                           SET amount = ? 
                           WHERE recipe_id = ? AND ingredient_id = ?"""
    db.execute(sql_update_amount, [new_amount, recipe_id, ingredient_id])

def delete_ingredient(recipe_id, ingredient_id):
    sql_delete_recipe_ingredient = """DELETE FROM recipe_ingredients 
                                      WHERE recipe_id = ? AND ingredient_id = ?"""
    db.execute(sql_delete_recipe_ingredient, [recipe_id, ingredient_id])
    remove_unused_ingredients()

def get_recipe_instructions(recipe_id):
    sql = """SELECT instruction, step_number, recipe_id FROM recipe_instructions
             WHERE recipe_id = ?
             ORDER BY step_number ASC"""
    return db.query(sql, [recipe_id])

def add_instruction(recipe_id, instruction):
    sql = """SELECT step_number FROM recipe_instructions WHERE recipe_id = ?
             ORDER BY step_number DESC LIMIT 1"""
    result = db.query(sql, [recipe_id])

    latest_step = result[0]["step_number"] if result else 0
    step_number = latest_step + 1

    sql = """INSERT INTO recipe_instructions (instruction, step_number, recipe_id)
             VALUES (?, ?, ?)"""
    db.execute(sql, [instruction, step_number, recipe_id])