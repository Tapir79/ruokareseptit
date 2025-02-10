import sqlite3
from flask import abort, redirect, render_template, request, session
import users

def get_login():
    return render_template("login.html", errors={})


def show_user(user_id, users):
    user = users.get_user(user_id)
    user_recipes = users.get_user_recipes(user_id)
    if not user_recipes:
        user_recipes = {}
    if not user:
        abort(404)

    return render_template("show_user.html", user=user, user_recipes=user_recipes)

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
        return render_template("login.html", errors=errors)

    if user_id:
        session["user_id"] = user_id
        session["username"] = username
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
        errors["username"] = "Tunnus ei voi olla tyhjä."
    if not password1:
        errors["password1"] = "Tunnus ei voi olla tyhjä."
    if not password2:
        errors["password2"] = "Tunnus ei voi olla tyhjä."
    if password1 != password2:
        errors["password1"] = "Salasanat eivät täsmää"

    if errors:
        return render_template("register.html", errors=errors)

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        errors["username"] = "Tunnus on jo varattu."
        return render_template("register.html", errors=errors)
    print("Tunnus luotu")
    return redirect("/")
