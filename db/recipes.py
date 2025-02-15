import db.db as db


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
                    cuisines.id as cuisine_id,
                    cuisines.name as cuisine,
                    users.id as user_id,
                    users.username,
                    (SUM(ratings.stars)/COUNT(ratings.stars)) as avg_rating
             FROM recipes JOIN users ON recipes.user_id = users.id
             JOIN cuisines ON recipes.cuisine_id = cuisines.id
             LEFT JOIN ratings ON recipes.id = ratings.recipe_id
             WHERE recipes.id = ?"""
    result = db.query(sql, [recipe_id])
    return result[0] if result else None


def get_recipes_by_user(user_id):
    sql = """SELECT recipes.id,
                    recipes.title,
                    (SUM(ratings.stars)/COUNT(ratings.stars)) as avg_rating
             FROM recipes JOIN users ON recipes.user_id = users.id
             LEFT JOIN ratings ON recipes.id = ratings.recipe_id
             WHERE users.id = ?"""
    result = db.query(sql, [user_id])
    return result if result else None


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


def add_recipe(title, description, cuisine_id, user_id):
    sql = """INSERT INTO recipes (title, description, cuisine_id, user_id)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [title, description, cuisine_id, user_id])
    last_insert_id = db.last_insert_id()
    return last_insert_id


def edit_recipe(recipe_id, title, description, cuisine_id, user_id):
    sql = """UPDATE recipes SET title = ?, 
                                description = ?,
                                cuisine_id = ?
                            WHERE id = ?
                            AND user_id = ?"""
    db.execute(sql, [title, description, cuisine_id, recipe_id, user_id])


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
                    users.username,
                    cuisines.name,
                    (SUM(ratings.stars)/COUNT(ratings.stars)) as avg_rating
             FROM recipes JOIN users ON recipes.user_id = users.id
             JOIN cuisines ON recipes.cuisine_id = cuisines.id
             LEFT JOIN ratings ON recipes.id = ratings.recipe_id
             WHERE (recipes.title LIKE ?
             OR recipes.description LIKE ?
             OR recipes.id IN (SELECT recipe_ingredients.recipe_id
                              FROM recipe_ingredients
                              JOIN ingredients
                              ON ingredients.id = recipe_ingredients.ingredient_id
                              WHERE ingredients.name LIKE ?))
             GROUP BY recipes.id,
                    recipes.title,
                    recipes.description,
                    recipes.user_id,
                    users.username,
                    cuisines.name
             ORDER BY recipes.id DESC"""

    search_term = f"%{ query }%"
    return db.query(sql, [search_term, search_term, search_term])


def add_ingredients(recipe_id, recipe_ingredients):
    for ingredient in recipe_ingredients:
        add_ingredient(recipe_id, ingredient["name"], ingredient["amount"])


def add_ingredient(recipe_id, name, amount):
    # Check if the ingredient exists in the 'ingredients' table
    sql_ingredient_exists = """SELECT id FROM ingredients WHERE name = ?"""
    result = db.query(sql_ingredient_exists, [name])

    if result:
        ingredient_id = result[0]["id"]  # Pick existing ingredient ID
    else:
        # Insert new ingredient if it does not exist
        sql_insert_ingredient = """INSERT INTO ingredients (name) VALUES (?)"""
        db.execute(sql_insert_ingredient, [name])
        ingredient_id = db.last_insert_id()

    # Check if the ingredient is already linked to the recipe
    sql_recipe_ingredient_exists = """SELECT 1 FROM recipe_ingredients
                                      WHERE recipe_id = ? AND ingredient_id = ?"""
    result = db.query(sql_recipe_ingredient_exists, [recipe_id, ingredient_id])

    if not result:
        # If ingredient is NOT in the recipe, insert it
        sql_insert_recipe_ingredient = """INSERT INTO recipe_ingredients (recipe_id, ingredient_id, amount)
                                          VALUES (?, ?, ?)"""
        db.execute(sql_insert_recipe_ingredient, [recipe_id, ingredient_id, amount])
        print(f"Ainesosa '{name}' lisätty reseptiin ID {recipe_id}.")
    else:
        print(
            f"Ainesosa '{name}' on jo lisätty reseptiin ID {recipe_id}."
        )  # Do nothing if already added


def edit_ingredient(recipe_id, ingredient_id, new_amount):
    sql_update_amount = """UPDATE recipe_ingredients
                           SET amount = ?
                           WHERE recipe_id = ?
                           AND ingredient_id = ?"""
    db.execute(sql_update_amount, [new_amount, recipe_id, ingredient_id])


def delete_ingredient(recipe_id, ingredient_id):
    sql_delete_recipe_ingredient = """DELETE FROM recipe_ingredients
                                      WHERE recipe_id = ?
                                      AND ingredient_id = ?"""
    db.execute(sql_delete_recipe_ingredient, [recipe_id, ingredient_id])
    remove_unused_ingredients()


def get_recipe_instructions(recipe_id):
    sql = """SELECT id, instruction as instruction_name, step_number, recipe_id FROM recipe_instructions
             WHERE recipe_id = ?
             ORDER BY step_number ASC"""
    return db.query(sql, [recipe_id])


def add_instructions(recipe_id, recipe_instructions):
    for instruction in recipe_instructions:
        add_instruction(recipe_id, instruction["instruction_name"])


def add_instruction(recipe_id, instruction):
    sql = """SELECT step_number FROM recipe_instructions WHERE recipe_id = ?
             ORDER BY step_number DESC LIMIT 1"""
    result = db.query(sql, [recipe_id])

    latest_step = result[0]["step_number"] if result else 0
    step_number = latest_step + 1

    sql = """INSERT INTO recipe_instructions (instruction, step_number, recipe_id)
             VALUES (?, ?, ?)"""
    db.execute(sql, [instruction, step_number, recipe_id])


def edit_instruction(recipe_id, instruction_id, new_instruction):
    sql_update_instruction = """UPDATE recipe_instructions
                           SET instruction = ?
                           WHERE recipe_id = ? AND id = ?"""
    db.execute(sql_update_instruction, [new_instruction, recipe_id, instruction_id])


def delete_instruction(recipe_id, instruction_id):
    sql_delete_instruction = """DELETE FROM recipe_instructions
                                      WHERE recipe_id = ? AND id = ?"""
    db.execute(sql_delete_instruction, [recipe_id, instruction_id])


def add_edit_or_remove_ingredients(recipe_id, recipe_ingredients):
    db_ingredients = get_recipe_ingredients(recipe_id)
    db_ingredients_dict = {ing["ingredient_id"]: ing for ing in db_ingredients}
    new_ingredients = []
    edited_ingredients = []
    for ing in recipe_ingredients:
        if ing.get("ingredient_id") not in db_ingredients_dict:
            new_ingredients.append(ing)
        else:
            edited_ingredients.append(ing)

    input_ingredient_ids = {ing["ingredient_id"] for ing in recipe_ingredients}
    deleted_ingredients = [
        ing
        for ing in db_ingredients
        if ing["ingredient_id"] not in input_ingredient_ids
    ]

    for ingredient in deleted_ingredients:
        delete_ingredient(recipe_id, ingredient["ingredient_id"])
    for ingredient in edited_ingredients:
        edit_ingredient(recipe_id, ingredient["ingredient_id"], ingredient["amount"])
    for ingredient in new_ingredients:
        add_ingredient(recipe_id, ingredient["name"], ingredient["amount"])


def add_edit_or_remove_instructions(recipe_id, recipe_instructions):
    db_instructions = get_recipe_instructions(recipe_id)
    db_instructions_dict = {instr["id"]: instr for instr in db_instructions}
    new_instructions = []
    edited_instructions = []
    for instr in recipe_instructions:
        if instr.get("id") not in db_instructions_dict:
            new_instructions.append(instr)
        else:
            edited_instructions.append(instr)

    input_instruction_ids = {
        instr["id"] for instr in recipe_instructions if "id" in instr
    }
    deleted_instructions = [
        instr for instr in db_instructions if instr["id"] not in input_instruction_ids
    ]

    for instruction in deleted_instructions:
        delete_instruction(recipe_id, instruction["id"])
    for instruction in edited_instructions:
        print(instruction["id"], instruction["instruction_name"])
        edit_instruction(recipe_id, instruction["id"], instruction["instruction_name"])
    for instruction in new_instructions:
        add_instruction(recipe_id, instruction["instruction_name"])


def get_cuisines():
    """Fetch all cuisines from the database."""
    return db.query("SELECT id, name FROM cuisines")


def cuisine_exists(cuisine_id):
    return db.query("SELECT id FROM cuisines WHERE id = ?", [str(cuisine_id)])


def save_rating(recipe_id, comment, rated_by):
    sql = """INSERT INTO ratings (comment, rated_by, recipe_id)
             VALUES (?, ?, ?)"""
    db.execute(sql, [comment, rated_by, recipe_id])
    last_insert_id = db.last_insert_id()
    return last_insert_id


def get_ratings(recipe_id):
    sql = """SELECT
             ratings.comment,
             ratings.stars,
             ratings.rated_by,
             ratings.recipe_id,
             ratings.created_at,
             users.username
             FROM ratings
             JOIN users ON ratings.rated_by = users.id
             WHERE recipe_id = ?
             ORDER BY created_at DESC"""
    return db.query(sql, [recipe_id])


def get_user_rating(recipe_id, rated_by):
    query = """SELECT id, comment, stars
               FROM ratings
               WHERE recipe_id = ? AND rated_by = ?"""
    result = db.query(query, (recipe_id, rated_by))
    return result[0] if result else None


def update_rating(rating_id, comment, stars):
    query = """UPDATE ratings
               SET comment = ?,
                   stars = ?
               WHERE id = ?"""
    db.execute(query, (comment, stars, rating_id))
    last_insert_id = db.last_insert_id()
    return last_insert_id
