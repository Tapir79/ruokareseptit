from werkzeug.security import check_password_hash, generate_password_hash

import db

def get_user(user_id):
    sql = """SELECT users.id, users.username
             FROM users
             WHERE users.id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_user_recipes(user_id):
    sql = """SELECT recipes.id, recipes.title
             FROM users JOIN recipes ON users.id = recipes.user_id
             WHERE users.id = ?"""
    result = db.query(sql, [user_id])
    return result if result else None

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])


def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None

    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None
