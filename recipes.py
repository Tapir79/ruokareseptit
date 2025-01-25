import db

def add_recipe(title, instructions, user_id):
    sql = """ INSERT INTO recipes (title, instructions, user_id)
                  VALUES (?, ?, ?)"""
    db.execute(sql, [title, instructions, user_id])


def get_recipes():
    sql = """ SELECT title, instructions, user_id 
                FROM recipes 
                ORDER BY id DESC """
    return db.query(sql)
