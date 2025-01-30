import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import recipes
import users

app = Flask(__name__)
app.secret_key = config.secret_key


@app.route("/")
def index():
    all_recipes = recipes.get_recipes()
    return render_template("index.html", recipes=all_recipes)

@app.route("/find_recipe")
def find_recipe():
    query = request.args.get("query")
    if query:
        results = recipes.find_recipes(query)
    else:
        query = ""
        results = []
    return render_template("find_recipe.html", query=query, results=results)


@app.route("/new_recipe")
def new_item():
    return render_template("new_recipe.html")


@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    single_recipe = recipes.get_recipe(recipe_id)
    return render_template("show_recipe.html", recipe=single_recipe)


@app.route("/edit_recipe/<int:recipe_id>")
def edit_recipe(recipe_id):
    single_recipe = recipes.get_recipe(recipe_id)
    if single_recipe["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_recipe.html", recipe=single_recipe)

@app.route("/remove_recipe/<int:recipe_id>", methods= ["GET", "POST"])
def remove_recipe(recipe_id):
    if request.method == "GET":
        single_recipe = recipes.get_recipe(recipe_id)
        return render_template("remove_recipe.html", recipe=single_recipe)

    if request.method == "POST":
        recipe_id = request.form["recipe_id"]
        if "remove" in request.form:
            try:
                recipes.remove_recipe(recipe_id)
            except sqlite3.IntegrityError:
                print("VIRHE: reseptin poistaminen epäonnistui")
            return redirect("/")
        else:
            return redirect("/recipe/" + str(recipe_id))

@app.route("/update_recipe", methods=["POST"])
def update_recipe():
    recipe_id = request.form["recipe_id"]
    title = request.form["title"]
    instructions = request.form["instructions"]

    try:
        recipes.update_recipe(recipe_id, title, instructions)
    except sqlite3.IntegrityError:
        print("VIRHE: reseptin muokkaus epäonnistui")
    return redirect("/recipe/" + str(recipe_id))


@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    title = request.form["title"]
    instructions = request.form["instructions"]
    user_id = session["user_id"]
    try:
        recipes.add_recipe(title, instructions, user_id)
    except sqlite3.IntegrityError:
        print("VIRHE: reseptin tallennus epäonnistui")
    return redirect("/")


# login/logout/register
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
    del session["user_id"]
    del session["username"]
    return redirect("/")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/create", methods=["POST"])
def create():
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
