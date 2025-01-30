import db

def get_recipes():
    sql = """SELECT id, 
                    title, 
                    instructions, 
                    user_id 
             FROM recipes 
             ORDER BY id DESC"""
    return db.query(sql)


def get_recipe(recipe_id):
    sql = """SELECT recipes.id, 
                    recipes.title, 
                    recipes.instructions, 
                    recipes.user_id, 
                    users.username 
             FROM recipes JOIN users ON recipes.user_id = users.id
             WHERE recipes.id = ?"""
    result = db.query(sql, [recipe_id])

    if result:
        return result[0]
    else:
        return None


def add_recipe(title, instructions, user_id):
    sql = """INSERT INTO recipes (title, instructions, user_id)
             VALUES (?, ?, ?)"""
    db.execute(sql, [title, instructions, user_id])


def edit_recipe(recipe_id, title, instructions):
    sql = """UPDATE recipes SET title = ?, 
                                instructions = ?
                            WHERE id = ?"""
    db.execute(sql, [title, instructions, recipe_id])

def remove_recipe(recipe_id):
    sql = """DELETE FROM recipes WHERE id = ?"""
    db.execute(sql, [recipe_id])

def find_recipes(query):
    sql = """SELECT recipes.id,
                    recipes.title,
                    recipes.instructions,
                    recipes.user_id,
                    users.username
             FROM recipes JOIN users ON recipes.user_id = users.id
             WHERE recipes.title LIKE ? OR recipes.instructions LIKE ?
             ORDER BY recipes.id DESC"""

    search_term = f"%{ query }%"
    return db.query(sql, [search_term, search_term])
