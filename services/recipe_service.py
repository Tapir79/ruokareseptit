import sqlite3
from flask import abort, redirect, render_template, request, session
import recipes
from utils.validations import validate_new_recipe_save_form, validate_new_recipe_form_instructions, validate_new_recipe_form_ingredients

def delete_temporary_session_attributes():
    if "recipe_ingredients" in session:
        del session["recipe_ingredients"]
    if "recipe_instructions" in session:
        del session["recipe_instructions"]
    if "max_instruction_id" in session:
        del session["max_instruction_id"]
    if "max_ingredient_id" in session:
        del  session["max_ingredient_id"]

def get_index():
    return render_template("index.html", recipes=recipes.get_recipes())

def search_recipe():
    query = request.args.get("query", "").strip()
    results = recipes.find_recipes(query) if query else {}
    return render_template("find_recipe.html", query=query, results=results)

def show_recipe(recipe_id):
    single_recipe = recipes.get_recipe(recipe_id)
    recipe_ingredients = recipes.get_recipe_ingredients(recipe_id)
    recipe_instructions = recipes.get_recipe_instructions(recipe_id)
    return render_template("show_recipe.html",
                           recipe=single_recipe,
                           recipe_ingredients=recipe_ingredients,
                           recipe_instructions=recipe_instructions)

def show_new_recipe():
    return render_template("new_recipe.html", errors={}, form_data={}, recipe_ingredients={}, recipe_instructions={})

def save_new_recipe(form_data, recipe_ingredients, recipe_instructions):
    """Handles the logic for saving a new recipe."""

    errors = validate_new_recipe_save_form(form_data)
    
    if errors:
        return render_template("new_recipe.html", errors=errors, form_data=form_data, 
                               recipe_ingredients=recipe_ingredients, recipe_instructions=recipe_instructions)

    title = form_data["title"]
    description = form_data["description"]
    user_id = session["user_id"]

    try:
        recipe_id = recipes.add_recipe(title, description, user_id)
        recipes.add_ingredients(recipe_id, recipe_ingredients)
        recipes.add_instructions(recipe_id, recipe_instructions)

        delete_temporary_session_attributes()

        return redirect(f"/recipe/{recipe_id}")

    except sqlite3.IntegrityError:
        print("VIRHE: reseptin tallennus epäonnistui")
        return render_template("create_recipe.html", errors={"general": "Reseptin tallennus epäonnistui"},
                               form_data=form_data, recipe_ingredients=recipe_ingredients, 
                               recipe_instructions=recipe_instructions)
    
def handle_session_instructions(form_data, recipe_ingredients, recipe_instructions):
    """Handles the logic for adding and deleting session instructions when creating a new recipe"""

    if "instruction" in request.form and form_data["instruction"] != "":
        errors = validate_new_recipe_form_instructions(form_data)
        if not errors:
            new_id = max((instr["id"] for instr in recipe_instructions), default=0) + 1
            recipe_instructions.append({"id": new_id, "instruction_name": form_data["instruction_name"]})
            session["recipe_instructions"] = recipe_instructions
        return render_template("new_recipe.html", errors=errors, form_data=form_data, recipe_ingredients=recipe_ingredients, recipe_instructions=recipe_instructions)
    
    delete_instruction_key = next((key for key in request.form.keys() if key.startswith("delete_instruction_")), None)
    if delete_instruction_key:

        instruction_id_to_remove = get_delete_instruction_id(form_data)

        if instruction_id_to_remove:
            recipe_instructions = [ins for ins in recipe_instructions if ins["id"] != instruction_id_to_remove]
            session["recipe_instructions"] = recipe_instructions
            session.modified = True

            return render_template("new_recipe.html", errors={}, form_data=form_data, recipe_ingredients=recipe_ingredients, recipe_instructions=recipe_instructions)
    
    return None


def get_delete_instruction_id(form_data):
    """Extracts the ID of an instruction marked for deletion."""
    delete_instruction_key = next((key for key in form_data.keys() if key.startswith("delete_instruction_")), None)
    if delete_instruction_key:
        instruction_id = delete_instruction_key[len("delete_instruction_"):]
        return int(instruction_id) if instruction_id.isdigit() else None
    
    return None

def handle_session_ingredients(form_data, recipe_ingredients, recipe_instructions):
    """Handles the logic for adding and deleting session ingredients when creating a new recipe"""
    if "ingredient" in request.form and form_data["ingredient"] != "":
        errors = validate_new_recipe_form_ingredients(form_data, recipe_ingredients)
        if not errors:
            new_id = max((ing["id"] for ing in recipe_ingredients), default=0) + 1
            recipe_ingredients.append({"id": new_id, "name": form_data["name"], "amount": form_data["amount"]})
            session["recipe_ingredients"] = recipe_ingredients
        return render_template("new_recipe.html", errors=errors, form_data=form_data, recipe_ingredients=recipe_ingredients, recipe_instructions=recipe_instructions)

    delete_ingredient_key = next((key for key in request.form.keys() if key.startswith("delete_ingredient_")), None)
    if delete_ingredient_key:

        ingredient_id_to_remove = delete_ingredient_key[len("delete_ingredient_"):]

        if ingredient_id_to_remove.isdigit():
            ingredient_id_to_remove = int(ingredient_id_to_remove)

            recipe_ingredients = [ing for ing in recipe_ingredients if ing["id"] != ingredient_id_to_remove]

            session["recipe_ingredients"] = recipe_ingredients
            session.modified = True

            return render_template("new_recipe.html", errors={}, form_data=form_data, recipe_ingredients=recipe_ingredients, recipe_instructions=recipe_instructions)
        
    return None
