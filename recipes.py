import db


def add_recipe(title, instructions, user_id):
    sql = """INSERT INTO recipes (title, instructions, user_id)
            VALUES (?, ?, ?) """
    db.execute(sql, [title, instructions, user_id])


def get_recipes():
    sql = """SELECT id, title, instructions, user_id 
            FROM recipes 
            ORDER BY id DESC"""
    return db.query(sql)


def get_recipe(recipe_id):
    sql = """SELECT  recipes.id, recipes.title, recipes.instructions, users.username 
            FROM recipes JOIN users ON recipes.user_id = users.id
            WHERE recipes.id = ?"""
    return db.query(sql, [recipe_id])[0]
