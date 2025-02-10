import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import recipes
import users
from utils.validations import (
    user_ids_must_match,
    recipe_must_exist,
    require_login,
)
from services.recipe_service import (
    delete_temporary_session_attributes,
    get_index,
    search_recipe,
    show_recipe,
    show_new_recipe,
    save_new_recipe,
    handle_new_recipe_session_instructions,
    handle_new_recipe_session_ingredients,
    show_edit_recipe,
    get_updated_session_ingredients,
    get_updated_session_instructions,
    save_edited_recipe,
    handle_edit_recipe_session_instructions,
    handle_edit_recipe_session_ingredients,
    delete_recipe,
)

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return get_index()

@app.route("/find_recipe")
def find_recipe():
    return search_recipe()

@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    return show_recipe(recipe_id)

@app.route("/create_recipe", methods=["GET", "POST"])
def create_recipe():
    require_login(session)

    if request.method == "GET":
        delete_temporary_session_attributes()
        return show_new_recipe()

    form_data = request.form
    recipe_ingredients = session.get("recipe_ingredients", [])
    recipe_instructions = session.get("recipe_instructions", [])

    if "save" in request.form:
        return save_new_recipe(form_data, recipe_ingredients, recipe_instructions)

    instructions_response = handle_new_recipe_session_instructions(
        form_data, recipe_ingredients, recipe_instructions
    )
    if instructions_response:
        return instructions_response

    ingredients_response = handle_new_recipe_session_ingredients(
        form_data, recipe_ingredients, recipe_instructions
    )
    if ingredients_response:
        return ingredients_response

    return render_template(
        "new_recipe.html",
        errors={},
        form_data=form_data,
        recipe_ingredients=recipe_ingredients,
        recipe_instructions=recipe_instructions,
    )


@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    require_login(session)

    if request.method == "GET":
        delete_temporary_session_attributes()
        return show_edit_recipe(recipe_id)

    recipe = session["recipe"]
    form_data = request.form
    recipe_ingredients = get_updated_session_ingredients(recipe_id, form_data)
    recipe_instructions = get_updated_session_instructions(recipe_id, form_data)

    if "save" in request.form:
        return save_edited_recipe(
            recipe, form_data, recipe_ingredients, recipe_instructions, recipe_id
        )

    instructions_response = handle_edit_recipe_session_instructions(
        recipe, form_data, recipe_ingredients, recipe_instructions
    )
    if instructions_response:
        return instructions_response

    ingredients_response = handle_edit_recipe_session_ingredients(
        recipe, form_data, recipe_ingredients, recipe_instructions
    )
    if ingredients_response:
        return ingredients_response

    return render_template(
        "edit_recipe.html",
        recipe=recipe,
        errors={},
        form_data=form_data,
        recipe_ingredients=recipe_ingredients,
        recipe_instructions=recipe_instructions,
    )


@app.route("/remove_recipe/<int:recipe_id>", methods=["GET", "POST"])
def remove_recipe(recipe_id):
    require_login(session)
    return delete_recipe(recipe_id)


@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    user_recipes = users.get_user_recipes(user_id)
    if not user_recipes:
        user_recipes = {}
    if not user:
        abort(404)

    return render_template("show_user.html", user=user, user_recipes=user_recipes)


# login/logout/register app routes
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", errors={})
    if request.method == "POST":
        errors = {}
        username = request.form["username"]
        password = request.form["password"]

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


@app.route("/logout")
def logout():
    delete_temporary_session_attributes()

    if "user_id" in session:
        del session["user_id"]
        del session["username"]

    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", errors={})

    if request.method == "POST":
        errors = {}
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

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
