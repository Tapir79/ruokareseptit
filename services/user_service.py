import secrets
import sqlite3
from flask import abort, redirect, render_template, request, session
import db.users as users
import db.recipes as recipes

def get_login():
    return render_template("login.html", errors={})

def show_user_statistics(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)

    page = request.args.get("page", 1, type=int)  # Default to page 1
    per_page = 10  # Number of recipes per page
    offset = (page - 1) * per_page

    user_recipes = recipes.get_recipes_by_user(user_id, limit=per_page, offset=offset)
    total_recipes = recipes.get_total_number_of_recipes(user_id)
    total_pages = (total_recipes // per_page) + (1 if total_recipes % per_page else 0)

    return render_template("show_user.html", user=user, user_recipes=user_recipes, total_recipes=total_recipes, page=page, total_pages=total_pages)

def user_login(form_data):
    errors = {}
    username = form_data["username"]
    password = form_data["password"]

    if not username:
        errors["username"] = "Tunnus ei voi olla tyhjä."
    if not password:
        errors["password"] = "Salasana ei voi olla tyhjä."

    user_id, error_message = users.check_login(username, password)
    if error_message:
        errors["username"] = error_message

    if errors:
        return render_template("login.html", errors=errors, username=username)

    if user_id:
        session["user_id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")

    return redirect("/login")

def user_logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]

    return redirect("/")

def get_user_registration():
    return render_template("register.html", errors={})

def register_user(form_data):
    errors = {}
    username = form_data["username"]
    password1 = form_data["password1"]
    password2 = form_data["password2"]

    if not username:
        errors["username"] = "Käyttäjätunnus vaaditaan."
    if not password1 and password2:
        errors["password1"] = "Salasana vaaditaan."
    if password1 != password2:
        errors["password1"] = "Salasanat eivät täsmää"

    if errors:
        return render_template("register.html", errors=errors, username=username)

    try:
        user_id = users.create_user(username, password1)
        session["user_id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")
        
    except sqlite3.IntegrityError:
        errors["username"] = "Tunnus on jo varattu."
        return render_template("register.html", errors=errors, username=username)
    
