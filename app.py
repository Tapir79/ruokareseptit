from flask import Flask
from flask import render_template, request, session
import config
from utils.validations import (
    require_login,
    user_owns_the_recipe,
    recipe_must_exist,
    check_csrf,
)
from services.recipe_service import (
    delete_temporary_session_attributes,
    get_index,
    search_recipe,
    show_recipe,
    save_rating,
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
    add_new_recipe_image,
    edit_new_recipe_image,
    get_recipe_image_by_id,
)

from services.user_service import (
    get_login,
    user_login,
    user_logout,
    show_user_statistics,
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


@app.route("/recipe/<int:recipe_id>", methods=["GET", "POST"])
def recipe(recipe_id):
    if request.method == "GET":
        delete_temporary_session_attributes()
        return show_recipe(recipe_id)

    check_csrf(request, session)
    logged_in_user = session["user_id"]
    recipe = session["recipe"]
    recipe_created_by = recipe["user_id"]

    if logged_in_user != recipe_created_by:
        save_rating(recipe_id, request.form, logged_in_user)
    return show_recipe(recipe_id)

 
@app.route("/create_recipe", methods=["GET", "POST"])
def create_recipe():
    require_login(session)
    
    if request.method == "GET":
        delete_temporary_session_attributes()
        return show_new_recipe()

    check_csrf(request, session)
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

    check_csrf(request, session)
    recipe = session["recipe"]
    recipe_must_exist(recipe)

    recipe_created_by = recipe["user_id"]
    logged_in_user = session["user_id"]
    user_owns_the_recipe(logged_in_user, recipe_created_by)

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
    if request.method == "POST":
        check_csrf(request, session)
    return delete_recipe(recipe_id)

@app.route("/upload_recipe_image/<int:recipe_id>", methods=["POST"])
def upload_recipe_image(recipe_id):
    require_login(session)
    # TODO check that session user is the same user that created the recipe_id
    return add_new_recipe_image(recipe_id)

@app.route('/edit_recipe/<int:recipe_id>/image', methods=['POST'])
def edit_recipe_image(recipe_id):
    require_login(session)
    # TODO check that session user is the same user that created the recipe_id
    return edit_new_recipe_image(recipe_id)


@app.route("/recipe/<int:recipe_id>/image")
def show_recipe_image(recipe_id):
    return get_recipe_image_by_id(recipe_id)


@app.route("/user/<int:user_id>")
def show_user(user_id):
    return show_user_statistics(user_id)


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
