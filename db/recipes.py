import db.db as db

AVERAGE_RATING_CONDITION = (
    "CAST(ROUND(recipes.total_rating*1.0/recipes.rating_count, 0) AS INTEGER)"
)
AVERAGE_RATING = f"{AVERAGE_RATING_CONDITION } as avg_rating"


def get_recipes():
    sql = """SELECT id, 
                    title, 
                    description,
                    user_id 
             FROM recipes 
             ORDER BY id DESC"""
    return db.query(sql)


def get_recipe(recipe_id):
    sql = f"""SELECT recipes.id, 
                    recipes.title, 
                    recipes.description,
                    recipes.user_id,
                    recipes.vegan,
                    recipes.vegetarian,
                    recipes.lactose_free,
                    recipes.gluten_free,
                    recipes.rating_count,
                    cuisines.id as cuisine_id,
                    cuisines.name as cuisine,
                    users.id as user_id,
                    users.username,
                    {AVERAGE_RATING}
             FROM recipes JOIN users ON recipes.user_id = users.id
             JOIN cuisines ON recipes.cuisine_id = cuisines.id
             WHERE recipes.id = ?"""
    result = db.query(sql, [recipe_id])
    return result[0] if result else None


def get_featured_recipe():
    sql = f"""SELECT recipes.id, 
                    recipes.title, 
                    recipes.description,
                    recipes.user_id,
                    recipes.vegan,
                    recipes.vegetarian,
                    recipes.lactose_free,
                    recipes.gluten_free,
                    recipes.rating_count,
                    cuisines.id as cuisine_id,
                    cuisines.name as cuisine,
                    users.id as user_id,
                    users.username,
                    {AVERAGE_RATING}
             FROM recipes 
             JOIN users ON recipes.user_id = users.id
             JOIN cuisines ON recipes.cuisine_id = cuisines.id
             ORDER BY avg_rating DESC, recipes.rating_count DESC
             LIMIT 1"""
    result = db.query(sql)
    return result[0] if result else None


def get_recipes_by_user(user_id, limit=10, offset=0):
    sql = f"""SELECT recipes.id,
                    recipes.title,
                    recipes.rating_count,
                    {AVERAGE_RATING}
             FROM recipes
             JOIN users ON recipes.user_id = users.id
             WHERE users.id = ?
             LIMIT ? OFFSET ?"""
    result = db.query(sql, [user_id, limit, offset])
    return result if result else []


def get_total_number_of_recipes(user_id):
    result = db.query("SELECT COUNT(*) FROM recipes WHERE user_id = ?", [user_id])
    return result[0][0] if result else 0


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


def add_recipe(
    title,
    description,
    cuisine_id,
    user_id,
    vegan,
    vegetarian,
    lactose_free,
    gluten_free,
):
    sql = """INSERT INTO recipes (title, description, cuisine_id, user_id, vegan, vegetarian, lactose_free, gluten_free)
             VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
    db.execute(
        sql,
        [
            title,
            description,
            cuisine_id,
            user_id,
            vegan,
            vegetarian,
            lactose_free,
            gluten_free,
        ],
    )
    last_insert_id = db.last_insert_id()
    return last_insert_id


def edit_recipe(
    recipe_id,
    title,
    description,
    cuisine_id,
    user_id,
    vegan,
    vegetarian,
    lactose_free,
    gluten_free,
):
    sql = """UPDATE recipes SET title = ?, 
                                description = ?,
                                cuisine_id = ?,
                                vegan = ?,
                                vegetarian = ?,
                                lactose_free = ?,
                                gluten_free = ?
              WHERE id = ?
              AND user_id = ?"""
    db.execute(
        sql,
        [
            title,
            description,
            cuisine_id,
            vegan,
            vegetarian,
            lactose_free,
            gluten_free,
            recipe_id,
            user_id,
        ],
    )


def remove_unused_ingredients():
    sql_unused_ingredients = """DELETE FROM ingredients
                                WHERE id NOT IN
                                    (SELECT ingredient_id FROM recipe_ingredients)"""
    db.execute(sql_unused_ingredients)


def remove_recipe(recipe_id):
    sql = """DELETE FROM recipes WHERE id = ?"""
    db.execute(sql, [recipe_id])

    remove_unused_ingredients()


def get_total_search_results(
    query,
    vegan,
    vegetarian,
    lactose_free,
    gluten_free,
    avg_rating,
    cuisine,
):
    search_params, cuisine_param, conditions = build_search_query_conditions(
        query, vegan, vegetarian, lactose_free, gluten_free, avg_rating, cuisine
    )

    total_sql = """SELECT count(*) as total_results
                    FROM recipes
                    JOIN users ON recipes.user_id = users.id
                    JOIN cuisines ON recipes.cuisine_id = cuisines.id"""
    params = []
    if search_params:
        params = [f"%{ query }%", f"%{ query }%", f"%{ query }%"]
    if cuisine_param:
        params.append(cuisine)

    total_sql += conditions
    total_results = db.query(total_sql, params)
    return total_results[0]["total_results"] if total_results else 0


def find_recipes(
    query,
    vegan,
    vegetarian,
    lactose_free,
    gluten_free,
    avg_rating,
    cuisine,
    page,
    per_page,
    order_by,
):

    search_params, cuisine_param, conditions = build_search_query_conditions(
        query, vegan, vegetarian, lactose_free, gluten_free, avg_rating, cuisine
    )

    offset = (page - 1) * per_page
    sql = f"""SELECT recipes.id,
                     recipes.title,
                     recipes.description,
                     recipes.user_id,
                     recipes.vegan,
                     recipes.vegetarian,
                     recipes.lactose_free,
                     recipes.gluten_free,
                     recipes.rating_count,
                     (SELECT EXISTS (SELECT 1 FROM recipe_images
                                     WHERE recipe_id = recipes.id)) as image_exists,
                     users.username,
                     cuisines.name as cuisine,
                     cuisines.id as cuisine_id,
                     {AVERAGE_RATING}
            FROM recipes
            JOIN users ON recipes.user_id = users.id
            JOIN cuisines ON recipes.cuisine_id = cuisines.id"""
    sql += conditions

    if order_by == "avg_rating":
        order_clause = " ORDER BY avg_rating DESC"
    else:
        order_clause = " ORDER BY recipes.title ASC"

    sql += order_clause + " LIMIT ? OFFSET ?"

    params = []
    if search_params:
        params = [f"%{ query }%", f"%{ query }%", f"%{ query }%"]
    if cuisine_param:
        params.append(cuisine)
    params.append(per_page + 1)
    params.append(offset)
    return db.query(sql, params)


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
    sql = "SELECT EXISTS (SELECT 1 FROM cuisines WHERE id = ?)"
    result = db.query(sql, [cuisine_id])

    return result[0][0] == 1


def save_rating(recipe_id, comment, stars, rated_by):
    sql = """INSERT INTO ratings (comment, rated_by, stars, recipe_id)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [comment, rated_by, stars, recipe_id])
    last_insert_id = db.last_insert_id()

    # Update the recipe table with the new rating count and sum
    update_sql = """UPDATE recipes
                    SET total_rating = total_rating + ?,
                        rating_count = rating_count + 1
                    WHERE id = ?"""
    db.execute(update_sql, [stars, recipe_id])

    return last_insert_id


def get_ratings(recipe_id, limit=20, offset=0):
    query = """SELECT r.id, r.comment, r.stars, r.rated_by, r.created_at, u.username
               FROM ratings r
               JOIN users u ON r.rated_by = u.id
               WHERE r.recipe_id = ?
               ORDER BY r.created_at DESC
               LIMIT ? OFFSET ?"""
    
    result = db.query(query, (recipe_id, limit, offset))
    return result if result else []


def get_total_ratings(recipe_id):
    query = "SELECT COUNT(*) FROM ratings WHERE recipe_id = ?"
    result = db.query(query, (recipe_id,))
    return result[0][0] if result else 0


def get_user_rating(recipe_id, rated_by):
    query = """SELECT id, comment, stars
               FROM ratings
               WHERE recipe_id = ? AND rated_by = ?"""
    result = db.query(query, (recipe_id, rated_by))
    return result[0] if result else None


def update_rating(rating_id, comment, stars):

    # Get the old rating value
    query = """SELECT recipe_id, stars FROM ratings WHERE id = ?"""
    result = db.query(query, [rating_id])

    if not result:
        return None  # Rating not found

    recipe_id, old_stars = result[0]

    update_query = """UPDATE ratings
                      SET comment = ?, stars = ?
                      WHERE id = ?"""
    db.execute(update_query, (comment, stars, rating_id))
    last_insert_id = db.last_insert_id()

    # Adjust the stored rating sum
    adjust_sql = """UPDATE recipes
                    SET total_rating = total_rating - ? + ?
                    WHERE id = ?"""
    db.execute(adjust_sql, [old_stars, stars, recipe_id])

    return last_insert_id


def add_recipe_image(recipe_id, image_data):
    sql = "INSERT INTO recipe_images (recipe_id, image) VALUES (?, ?)"
    db.execute(sql, [recipe_id, image_data])


def update_recipe_image(recipe_id, image_data):
    sql = """UPDATE recipe_images
             SET image = ?
             WHERE recipe_id = ?"""
    db.execute(sql, [image_data, recipe_id])


def get_recipe_image(recipe_id):
    sql = "SELECT image FROM recipe_images WHERE recipe_id = ? LIMIT 1"
    result = db.query(sql, [recipe_id])
    return result[0]["image"] if result else None


def recipe_image_exists(recipe):
    if recipe:
        recipe_id = recipe["id"]
        sql = """SELECT EXISTS (
                        SELECT 1 FROM recipe_images
                        WHERE recipe_id = ?)"""
        result = db.query(sql, [recipe_id])
        return result[0][0] == 1
    return False


# Helper functions


def get_next_operator(is_first):
    if is_first:
        return "WHERE"
    else:
        return "AND"


def append_to_conditions(is_first, conditions: list, query_condition):

    sql_operator = get_next_operator(is_first)
    conditions.append(sql_operator)
    conditions.append(query_condition)

    if is_first:
        is_first = False
    return is_first


def build_search_query_conditions(
    query, vegan, vegetarian, lactose_free, gluten_free, avg_rating, cuisine
):
    search_params = False
    cuisine_param = False
    is_first = True
    conditions = []

    if query:
        query_condition = """(recipes.title LIKE ?
                             OR recipes.description LIKE ?
                             OR recipes.id IN (SELECT recipe_ingredients.recipe_id
                                               FROM recipe_ingredients
                                               JOIN ingredients ON ingredients.id = recipe_ingredients.ingredient_id
                                               WHERE ingredients.name LIKE ?))"""
        search_params = True
        is_first = append_to_conditions(is_first, conditions, query_condition)

    if vegan:
        query_condition = "vegan = 1"
        is_first = append_to_conditions(is_first, conditions, query_condition)

    if vegetarian:
        query_condition = "vegetarian = 1"
        is_first = append_to_conditions(is_first, conditions, query_condition)

    if lactose_free:
        query_condition = "lactose_free = 1"
        is_first = append_to_conditions(is_first, conditions, query_condition)

    if gluten_free:
        query_condition = "gluten_free = 1"
        is_first = append_to_conditions(is_first, conditions, query_condition)

    if len(avg_rating) > 0:
        avg_rating_ints = [int(rating) for rating in avg_rating]
        ratings_str = ", ".join(map(str, avg_rating_ints))
        query_condition = f"{AVERAGE_RATING_CONDITION} IN ({ratings_str})"
        is_first = append_to_conditions(is_first, conditions, query_condition)

    if cuisine:
        query_condition = "cuisines.id = ?"
        is_first = append_to_conditions(is_first, conditions, query_condition)
        cuisine_param = True

    conditions = " ".join(conditions)
    conditions = " " + conditions + " "

    return search_params, cuisine_param, conditions
