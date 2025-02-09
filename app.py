import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import recipes
import users
from utils.validations import user_ids_must_match, recipe_must_exist, require_login, validate_form, validate_new_recipe_form_ingredients, validate_new_recipe_form_instructions, validate_new_recipe_save_form
from services.recipe_service import delete_temporary_session_attributes, get_index, search_recipe, show_recipe, show_new_recipe, save_new_recipe, handle_session_instructions, handle_session_ingredients

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

    if request.method == "POST":

        form_data = request.form
        recipe_ingredients = session.get("recipe_ingredients", [])
        recipe_instructions = session.get("recipe_instructions", [])

        if "save" in request.form:
            return save_new_recipe(form_data, recipe_ingredients, recipe_instructions)

        instructions_response = handle_session_instructions(form_data, recipe_ingredients, recipe_instructions)
        if instructions_response:
            return instructions_response

        ingredients_response = handle_session_ingredients(form_data, recipe_ingredients, recipe_instructions)
        if ingredients_response:
            return ingredients_response

        return render_template("new_recipe.html", errors={}, form_data=form_data, recipe_ingredients=recipe_ingredients, recipe_instructions=recipe_instructions)

@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    require_login(session)

    recipe = recipes.get_recipe(recipe_id)
    recipe_must_exist(recipe)

    if request.method == "GET":
        delete_temporary_session_attributes()

        recipe_ingredients = session["recipe_ingredients"] = [
            {"ingredient_id": ing["ingredient_id"], "name": ing["name"], "amount": ing["amount"]}
            for ing in recipes.get_recipe_ingredients(recipe_id)]

        recipe_instructions = session["recipe_instructions"] = [
            {"id": instr["id"], "instruction_name": instr["instruction_name"]}
            for instr in recipes.get_recipe_instructions(recipe_id)]

        session["max_instruction_id"] = max((instr["id"] for instr in recipe_instructions), default=0) + 1
        session["max_ingredient_id"] = max((ing["ingredient_id"] for ing in recipe_ingredients), default=0) + 1

        return render_template("edit_recipe.html", recipe=recipe, errors={}, form_data={}, recipe_ingredients=recipe_ingredients, recipe_instructions=recipe_instructions)

    form_data = request.form
    # Load existing ingredients and instructions
    recipe_ingredients = session.get("recipe_ingredients") or [
        {"ingredient_id": ing["ingredient_id"], "name": ing["name"], "amount": ing["amount"]}
        for ing in recipes.get_recipe_ingredients(recipe_id)]

    recipe_instructions = session.get("recipe_instructions") or [
        {"id": instr["id"], "instruction_name": instr["instruction_name"]}
        for instr in recipes.get_recipe_instructions(recipe_id)]

    # update instructions with form data
    for ins in recipe_instructions:
        updated_name =  "instruction_" + str(ins["id"])
        if updated_name in form_data:
            ins["instruction_name"] = form_data[updated_name]

    # update ingredients with form data
    for ing in recipe_ingredients:
        updated_amount = "ingredient_" + str(ing["ingredient_id"])
        if updated_amount in form_data:
            ing["amount"] = form_data[updated_amount]

    # Handle recipe update
    if "save" in request.form:
        errors = validate_new_recipe_save_form(form_data)
        if errors:
            return render_template("edit_recipe.html", recipe=recipe, errors=errors, form_data=form_data, recipe_ingredients=recipe_ingredients, recipe_instructions=recipe_instructions)

        title = request.form["title"]
        description = request.form["description"]
        user_id = session["user_id"]

        try:
            recipes.edit_recipe(recipe_id, title, description, user_id)
            recipes.add_edit_or_remove_instructions(recipe_id, recipe_instructions)
            recipes.edit_or_remove_ingredients(recipe_id, recipe_ingredients)
        except sqlite3.IntegrityError:
            print("VIRHE: reseptin päivitys epäonnistui")

        return redirect(f"/recipe/{recipe_id}")

    if "instruction" in request.form and form_data["instruction"] != "":
        errors = validate_new_recipe_form_instructions(form_data)
        if not errors:
            new_id = session["max_instruction_id"]
            session["max_instruction_id"] = int(new_id) + 1
            recipe_instructions.append({"id": new_id, "instruction_name": form_data["instruction_name"]})
            session["recipe_instructions"] = recipe_instructions
        return render_template("edit_recipe.html", recipe=recipe, errors=errors, form_data=form_data, recipe_ingredients=recipe_ingredients, recipe_instructions=recipe_instructions)

    delete_instruction_key = next((key for key in request.form.keys() if key.startswith("delete_instruction_")), None)
    if delete_instruction_key:
        instruction_id_to_remove = delete_instruction_key[len("delete_instruction_"):]

        if instruction_id_to_remove.isdigit():
            instruction_id_to_remove = int(instruction_id_to_remove)
            recipe_instructions = [ins for ins in recipe_instructions if ins["id"] != instruction_id_to_remove]
            session["recipe_instructions"] = recipe_instructions
            session.modified = True
            return render_template("edit_recipe.html", recipe=recipe, errors={}, form_data=form_data, recipe_ingredients=recipe_ingredients, recipe_instructions=recipe_instructions)

    if "ingredient" in request.form and form_data["ingredient"] != "":
        errors = validate_new_recipe_form_ingredients(form_data, recipe_ingredients)
        if not errors:
            new_id = session["max_ingredient_id"]
            session["max_ingredient_id"] = int(new_id) + 1
            recipe_ingredients.append({"ingredient_id": new_id, "name": form_data["name"], "amount": form_data["amount"]})
            session["recipe_ingredients"] = recipe_ingredients
        return render_template("edit_recipe.html", recipe=recipe, errors=errors, form_data=form_data, recipe_ingredients=recipe_ingredients, recipe_instructions=recipe_instructions)

    delete_ingredient_key = next((key for key in request.form.keys() if key.startswith("delete_ingredient_")), None)
    if delete_ingredient_key:

        ingredient_id_to_remove = delete_ingredient_key[len("delete_ingredient_"):]

        if ingredient_id_to_remove.isdigit():
            ingredient_id_to_remove = int(ingredient_id_to_remove)
            recipe_ingredients = [ing for ing in recipe_ingredients if ing["ingredient_id"] != ingredient_id_to_remove]
            session["recipe_ingredients"] = recipe_ingredients
            session.modified = True
            return render_template("edit_recipe.html", recipe=recipe, errors={}, form_data=form_data, recipe_ingredients=recipe_ingredients, recipe_instructions=recipe_instructions)

    return render_template("edit_recipe.html", recipe=recipe, errors={}, form_data=form_data, recipe_ingredients=recipe_ingredients, recipe_instructions=recipe_instructions)


@app.route("/remove_recipe/<int:recipe_id>", methods= ["GET", "POST"])
def remove_recipe(recipe_id):
    require_login(session)
    single_recipe = recipes.get_recipe(recipe_id)
    recipe_must_exist(single_recipe)
    user_ids_must_match(single_recipe["user_id"], session)

    if request.method == "GET":
        return render_template("remove_recipe.html", recipe=single_recipe)

    if request.method == "POST":
        if "remove" in request.form:
            try:
                recipes.remove_recipe(recipe_id)
            except sqlite3.IntegrityError:
                print("VIRHE: reseptin poistaminen epäonnistui")
            return redirect("/")

        return redirect("/recipe/" + str(recipe_id))

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
