import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import recipes
import users
from utils.validations import user_ids_must_match, recipe_must_exist, require_login, validate_form, validate_new_recipe_form_ingredients, validate_new_recipe_form_instructions, validate_new_recipe_save_form

app = Flask(__name__)
app.secret_key = config.secret_key

def delete_temporary_session_attributes():
    if "recipe_ingredients" in session:
        del session["recipe_ingredients"]
    if "recipe_instructions" in session:
        del session["recipe_instructions"]

@app.route("/")
def index():
    all_recipes = recipes.get_recipes()
    return render_template("index.html", recipes=all_recipes)

@app.route("/find_recipe")
def find_recipe():
    query = request.args.get("query", "").strip()
    results = recipes.find_recipes(query) if query else {}
    return render_template("find_recipe.html", query=query, results=results)

@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    single_recipe = recipes.get_recipe(recipe_id)
    recipe_ingredients = recipes.get_recipe_ingredients(recipe_id)
    recipe_instructions = recipes.get_recipe_instructions(recipe_id)
    return render_template("show_recipe.html",
                           recipe=single_recipe,
                           recipe_ingredients=recipe_ingredients,
                           recipe_instructions=recipe_instructions)

@app.route("/create_recipe", methods=["GET", "POST"])
def create_recipe():
    require_login(session)

    if request.method == "GET":
        delete_temporary_session_attributes()
        return render_template("new_recipe.html", errors={}, form_data={}, recipe_ingredients={}, recipe_instructions={})

    if request.method == "POST":

        form_data = request.form
        recipe_ingredients = session.get("recipe_ingredients", [])
        recipe_instructions = session.get("recipe_instructions", [])

        if "save" in request.form:
            form_data = request.form
            errors = validate_new_recipe_save_form(form_data)

            if errors:
                return render_template("new_recipe.html", errors=errors, form_data=form_data, recipe_ingredients=recipe_ingredients, recipe_instructions=recipe_instructions)

            title = request.form["title"]
            description = request.form["description"]
            user_id = session["user_id"]
            try:
                recipe_id = recipes.add_recipe(title, description, user_id)
                recipes.add_ingredients(recipe_id, recipe_ingredients)
                recipes.add_instructions(recipe_id, recipe_instructions)
            except sqlite3.IntegrityError:
                print("VIRHE: reseptin tallennus epäonnistui")

            delete_temporary_session_attributes()
            return redirect("/recipe/" + str(recipe_id))

        if "instruction" in request.form and form_data["instruction"] != "":
            errors = validate_new_recipe_form_instructions(form_data)
            if not errors:
                recipe_instructions.append({"instruction_name": form_data["instruction_name"]})
                session["recipe_instructions"] = recipe_instructions
            return render_template("new_recipe.html", errors=errors, form_data=form_data, recipe_ingredients=recipe_ingredients, recipe_instructions=recipe_instructions)

        if "ingredient" in request.form and form_data["ingredient"] != "":
            errors = validate_new_recipe_form_ingredients(form_data, recipe_ingredients)
            if not errors:
                recipe_ingredients.append({"name": form_data["name"], "amount": form_data["amount"]})
                session["recipe_ingredients"] = recipe_ingredients
            return render_template("new_recipe.html", errors=errors, form_data=form_data, recipe_ingredients=recipe_ingredients, recipe_instructions=recipe_instructions)

        if "delete_ingredient" in request.form and form_data["delete_ingredient"] != "":
            ingredient_to_remove = request.form["delete_ingredient"]
            recipe_ingredients = [ing for ing in recipe_ingredients if ing["name"] != ingredient_to_remove]
            session["recipe_ingredients"] = recipe_ingredients
            session.modified = True  # Ensure session updates persist
            return render_template("new_recipe.html", errors={}, form_data=form_data, recipe_ingredients=recipe_ingredients, recipe_instructions=recipe_instructions)


@app.route("/add_ingredient/<int:recipe_id>", methods=["GET", "POST"])
def add_ingredient(recipe_id):
    require_login(session)
    single_recipe = recipes.get_recipe(recipe_id)
    recipe_ingredients = recipes.get_recipe_ingredients(recipe_id)
    recipe_instructions = recipes.get_recipe_instructions(recipe_id)
    recipe_must_exist(single_recipe)
    user_ids_must_match(single_recipe["user_id"], session)

    if request.method == "GET":
        return render_template("add_ingredient.html",
                               recipe=single_recipe,
                               recipe_ingredients=recipe_ingredients,
                               recipe_instructions=recipe_instructions,
                               errors={},
                               form_data={},
                               edit_disabled="disabled-link")

    if request.method == "POST":
        if "back" in request.form:
            errors = {}
            return redirect(f"/recipe/{recipe_id}")

        form_data = request.form
        errors = validate_form(request.form)

        if errors:
            return render_template("add_ingredient.html",
                                    recipe=single_recipe,
                                    recipe_ingredients=recipe_ingredients,
                                    recipe_instructions=recipe_instructions,
                                    errors=errors,
                                    form_data=form_data,
                                    edit_disabled="disabled-link")

        name = request.form["name"]
        amount = request.form["amount"]

        try:
            recipes.add_ingredient(recipe_id, name, amount)
        except Exception as e:
            errors["name"] = str(e)
            return render_template("add_ingredient.html",
                                    recipe=single_recipe,
                                    recipe_ingredients=recipe_ingredients,
                                    recipe_instructions=recipe_instructions,
                                    errors=errors,
                                    form_data=form_data,
                                    edit_disabled="disabled-link")
        return redirect(f"/recipe/{recipe_id}")

@app.route("/add_instruction/<int:recipe_id>", methods=["GET", "POST"])
def add_instruction(recipe_id):
    require_login(session)
    single_recipe = recipes.get_recipe(recipe_id)
    recipe_ingredients = recipes.get_recipe_ingredients(recipe_id)
    recipe_instructions = recipes.get_recipe_instructions(recipe_id)
    recipe_must_exist(single_recipe)
    user_ids_must_match(single_recipe["user_id"], session)

    if request.method == "GET":
        return render_template("add_instruction.html",
                               recipe=single_recipe,
                               recipe_ingredients=recipe_ingredients,
                               recipe_instructions=recipe_instructions,
                               errors={},
                               form_data={},
                               edit_disabled="disabled-link")

    if request.method == "POST":
        if "back" in request.form:
            errors = {}
            return redirect(f"/recipe/{recipe_id}")
        else:
            form_data = request.form
            errors = validate_form(request.form)

            if errors:
                return render_template("add_instruction.html",
                                       recipe=single_recipe,
                                       recipe_ingredients=recipe_ingredients,
                                       recipe_instructions=recipe_instructions,
                                       errors=errors,
                                       form_data=form_data,
                                       edit_disabled="disabled-link")

            instruction = request.form["instruction"]

            try:
                recipes.add_instruction(recipe_id, instruction)
            except Exception as e:
                errors["instruction"] = str(e)
                return render_template("add_instruction.html",
                                       recipe=single_recipe,
                                       recipe_ingredients=recipe_ingredients,
                                       recipe_instructions=recipe_instructions,
                                       errors=errors,
                                       form_data=form_data,
                                       edit_disabled="disabled-link")
            return redirect(f"/recipe/{recipe_id}")

@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    require_login(session)
    single_recipe = recipes.get_recipe(recipe_id)
    recipe_ingredients = recipes.get_recipe_ingredients(recipe_id)
    recipe_instructions = recipes.get_recipe_instructions(recipe_id)
    recipe_must_exist(single_recipe)
    user_ids_must_match(single_recipe["user_id"], session)

    if request.method == "GET":
        return render_template("edit_recipe.html",
                               recipe=single_recipe,
                               recipe_ingredients=recipe_ingredients,
                               recipe_instructions=recipe_instructions,
                               errors=[],
                               form_data=[])

    if request.method == "POST":
        if "back" in request.form:
            errors = {}
            return redirect(f"/recipe/{recipe_id}")


        form_data = request.form
        errors = validate_form(request.form)
        if errors:
            return render_template("edit_recipe.html",
                                    recipe=single_recipe,
                                    recipe_ingredients=recipe_ingredients,
                                    recipe_instructions=recipe_instructions,
                                    errors=errors,
                                    form_data=form_data)

        title = form_data["title"]
        description = form_data["description"]

        try:
            recipes.edit_recipe(recipe_id, title, description)
            for ingredient in recipe_ingredients:
                ingredient_id = ingredient["ingredient_id"]
                new_amount = form_data[f"ingredient_amount_{ingredient_id}"]
                delete_ingredient = form_data.get(f"delete_ingredient_{ingredient_id}", False)

                if delete_ingredient:
                    recipes.delete_ingredient(recipe_id, ingredient_id)
                else:
                    recipes.edit_ingredient(recipe_id, ingredient_id, new_amount)

            for instruction in recipe_instructions:
                instruction_id = instruction["id"]
                new_instruction = form_data[f"instruction_{instruction_id}"]
                delete_instruction = form_data.get(f"delete_instruction_{instruction_id}",
                                                    False)
                if delete_instruction:
                    recipes.delete_instruction(recipe_id, instruction_id)
                else:
                    recipes.edit_instruction(recipe_id, instruction_id, new_instruction)

        except sqlite3.IntegrityError:
            print("VIRHE: reseptin muokkaus epäonnistui")

        return redirect(f"/recipe/{recipe_id}")

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
