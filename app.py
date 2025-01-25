import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
import config
import recipes
import users

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_recipes = recipes.get_recipes()
    return render_template("index.html", recipes=all_recipes)

@app.route("/login", methods=["GET","POST"])
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

@app.route("/new_recipe")
def new_item():
    return render_template("new_recipe.html")
