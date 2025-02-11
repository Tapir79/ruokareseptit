from flask import Flask
from flask import render_template, request, session
import config
from utils.validations import (
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

from services.user_service import (
    get_login,
    user_login,
    user_logout,
    show_user,
    get_user_registration,
    register_user,
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
    cuisines = session["cuisines"]

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
        cuisines=cuisines,
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
    cuisines = session["cuisines"]

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
        cuisines=cuisines,
    )


@app.route("/remove_recipe/<int:recipe_id>", methods=["GET", "POST"])
def remove_recipe(recipe_id):
    require_login(session)
    return delete_recipe(recipe_id)


@app.route("/user/<int:user_id>")
def show_user(user_id):
    return show_user(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return get_login()
    if request.method == "POST":
        return user_login(request.form)


@app.route("/logout")
def logout():
    delete_temporary_session_attributes()
    return user_logout()


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return get_user_registration()

    if request.method == "POST":
        return register_user(request.form)
