import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import recipes
import users
from utils.validations import user_ids_must_match, recipe_must_exist, require_login, validate_form

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_recipes = recipes.get_recipes()
    return render_template("index.html", recipes=all_recipes)

@app.route("/find_recipe")
def find_recipe():
    query = request.args.get("query", "").strip()
    results = recipes.find_recipes(query) if query else []
    return render_template("find_recipe.html", query=query, results=results)

@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    single_recipe = recipes.get_recipe(recipe_id)
    recipe_ingredients = recipes.get_recipe_ingredients(recipe_id)
    return render_template("show_recipe.html", recipe=single_recipe, recipe_ingredients=recipe_ingredients)

@app.route("/create_recipe", methods=["GET", "POST"])
def create_recipe():
    require_login(session)
    if request.method == "GET":
        return render_template("new_recipe.html", errors=[], form_data=[])

    if request.method == "POST":
        form_data = request.form
        errors = validate_form(request.form)

        if errors:
            return render_template("new_recipe.html", errors=errors, form_data=form_data)

        title = request.form["title"]
        description = request.form["description"]
        user_id = session["user_id"]
        try:
            recipe_id = recipes.add_recipe(title, description, user_id)
        except sqlite3.IntegrityError:
            print("VIRHE: reseptin tallennus epäonnistui")
        return redirect("/recipe/" + str(recipe_id))

@app.route("/add_ingredient/<int:recipe_id>", methods=["GET", "POST"])
def add_ingredient(recipe_id):
    require_login(session)
    single_recipe = recipes.get_recipe(recipe_id)
    recipe_ingredients = recipes.get_recipe_ingredients(recipe_id)
    recipe_must_exist(single_recipe)
    user_ids_must_match(single_recipe["user_id"], session)

    if request.method == "GET":
        return render_template("add_ingredient.html", recipe=single_recipe, recipe_ingredients=recipe_ingredients, errors=[], form_data=[])

    if request.method == "POST":
        form_data = request.form
        errors = validate_form(request.form)

        if errors:
            return render_template("add_ingredient.html", recipe=single_recipe, recipe_ingredients=recipe_ingredients, errors=errors, form_data=form_data)

        name = request.form["name"]
        amount = request.form["amount"]

        try:
            recipes.add_ingredient(recipe_id, name, amount)
        except sqlite3.IntegrityError:
            print("VIRHE: reseptin muokkaus epäonnistui")
        return redirect("/recipe/" + str(recipe_id))

@app.route("/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    require_login(session)
    single_recipe = recipes.get_recipe(recipe_id)
    recipe_must_exist(single_recipe)
    user_ids_must_match(single_recipe["user_id"], session)

    if request.method == "GET":
        return render_template("edit_recipe.html", recipe=single_recipe, errors=[], form_data=[])

    if request.method == "POST":
        form_data = request.form
        errors = validate_form(request.form)

        if errors:
            return render_template("edit_recipe.html", recipe=single_recipe, errors=errors, form_data=form_data)

        title = request.form["title"]
        description = request.form["description"]

        try:
            recipes.edit_recipe(recipe_id, title, description)
        except sqlite3.IntegrityError:
            print("VIRHE: reseptin muokkaus epäonnistui")
        return redirect("/recipe/" + str(recipe_id))

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
        else:
            return redirect("/recipe/" + str(recipe_id))

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    user_recipes = users.get_user_recipes(user_id)
    if not user_recipes:
        abort(404)
    if not user:
        abort(404)
    print(user)
    return render_template("show_user.html", user=user, user_recipes=user_recipes)


# login/logout/register app routes
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            print("VIRHE: väärä tunnus tai salasana")
            return redirect("/login")


@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        print("VIRHE: salasanat eivät ole samat")
        redirect("/register")
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        print("VIRHE: tunnus on jo varattu")
        return redirect("/register")
    print("Tunnus luotu")
    return redirect("/")
