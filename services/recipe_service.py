import sqlite3
from flask import make_response, redirect, render_template, flash, request, session
import db.recipes as recipes
from utils.validations import (
    allowed_file,
    validate_recipe_save_form,
    validate_recipe_form_instructions,
    validate_recipe_form_ingredients,
    recipe_must_exist,
    user_owns_the_recipe,
    check_image,
)
import html


def delete_temporary_session_attributes():
    if "recipe_ingredients" in session:
        del session["recipe_ingredients"]
    if "recipe_instructions" in session:
        del session["recipe_instructions"]
    if "max_instruction_id" in session:
        del session["max_instruction_id"]
    if "max_ingredient_id" in session:
        del session["max_ingredient_id"]
    if "recipe" in session:
        del session["recipe"]


def get_index():
    featured_recipe = recipes.get_featured_recipe()
    image_exists = recipes.recipe_image_exists(featured_recipe)
    return render_template(
        "index.html", featured_recipe=featured_recipe, image_exists=image_exists
    )


def search_recipe():
    results = None
    query = request.args.get("query", "").strip()
    vegan = request.args.get("vegan")
    vegetarian = request.args.get("vegetarian")
    lactose_free = request.args.get("lactose_free")
    gluten_free = request.args.get("gluten_free")
    avg_rating = request.args.getlist("avg_rating")
    cuisine = request.args.get("cuisine")
    page = request.args.get("page", 1, type=int)
    per_page = 5
    cuisines = recipes.get_cuisines()
    results = recipes.find_recipes(
        query,
        vegan,
        vegetarian,
        lactose_free,
        gluten_free,
        avg_rating,
        cuisine,
        page,
        per_page,
    )

    has_more = False
    if len(results) > per_page:
        has_more = True
        results = results[:per_page]

    return render_template(
        "find_recipe.html",
        query=query,
        results=results,
        cuisines=cuisines,
        page=page,
        has_more=has_more,
        vegan=vegan,
        vegetarian=vegetarian,
        lactose_free=lactose_free,
        gluten_free=gluten_free,
        avg_rating=avg_rating,
        cuisine=cuisine,
    )


def show_recipe(recipe_id):
    single_recipe = recipes.get_recipe(recipe_id)
    recipe_must_exist(single_recipe)
    recipe_ingredients = recipes.get_recipe_ingredients(recipe_id)
    recipe_instructions = recipes.get_recipe_instructions(recipe_id)

    # Ratings pagination
    ratings_page = request.args.get("ratings_page", 1, type=int)
    ratings_per_page = 20
    offset = (ratings_page - 1) * ratings_per_page
    recipe_ratings = recipes.get_ratings(
        recipe_id, limit=ratings_per_page, offset=offset
    )
    total_ratings = recipes.get_total_ratings(recipe_id)
    total_rating_pages = (total_ratings // ratings_per_page) + (
        1 if total_ratings % ratings_per_page else 0
    )

    image_exists = recipes.recipe_image_exists(single_recipe)
    session["recipe"] = dict(single_recipe)

    rating = []
    if "user_id" in session:
        user_id = session["user_id"]
        rating = get_user_rating(recipe_id, user_id)

    return render_template(
        "show_recipe.html",
        recipe=single_recipe,
        recipe_ingredients=recipe_ingredients,
        recipe_instructions=recipe_instructions,
        recipe_ratings=recipe_ratings,
        rating=rating,
        image_exists=image_exists,
        ratings_page=ratings_page,
        total_rating_pages=total_rating_pages,
    )


def get_user_rating(recipe_id, rated_by):
    single_recipe = recipes.get_recipe(recipe_id)
    recipe_must_exist(single_recipe)
    result = recipes.get_user_rating(recipe_id, rated_by)
    if result:
        return result
    return None


def save_rating(recipe_id, form_data, rated_by):
    comment = html.escape(form_data["comment"])
    stars = form_data["stars"]
    existing_rating = recipes.get_user_rating(recipe_id, rated_by)

    try:
        if existing_rating:
            existing_rating_id = existing_rating["id"]
            recipes.update_rating(existing_rating_id, comment, stars)
            flash(f"Reseptin arvostelu päivitetty onnistuneesti!", "success")
        else:
            recipes.save_rating(recipe_id, comment, stars, rated_by)
            flash(f"Reseptin arvostelu lisätty onnistuneesti!", "success")
    except sqlite3.IntegrityError:
        flash(f"Reseptin arvostelun tallennus epäonnistui!", "error")
        if existing_rating:
            action = "päivitys"
        else:
            action = "tallennus"
        return render_template(
            "show_recipe.html",
            errors={"general": f"Arvostelun {action} epäonnistui"},
            form_data=form_data,
        )

    return redirect(f"/recipe/{recipe_id}")


def show_new_recipe():
    cuisines = recipes.get_cuisines()
    session["cuisines"] = [dict(cuisine) for cuisine in cuisines]
    return render_template(
        "new_recipe.html",
        errors={},
        form_data={},
        recipe_ingredients={},
        recipe_instructions={},
        cuisines=session["cuisines"],
    )


def save_new_recipe(form_data, recipe_ingredients, recipe_instructions):
    """Handles the logic for saving a new recipe."""

    errors = validate_recipe_save_form(form_data)

    if errors:
        return render_template(
            "new_recipe.html",
            errors=errors,
            form_data=form_data,
            recipe_ingredients=recipe_ingredients,
            recipe_instructions=recipe_instructions,
            cuisines=session["cuisines"],
        )

    title = html.escape(form_data["title"])
    description = html.escape(form_data["description"])
    cuisine_id = int(form_data["cuisine"])
    user_id = session["user_id"]
    cuisines = session["cuisines"]

    # Handle checkboxes: if unchecked, default to 0
    vegan = 1 if "vegan" in form_data else 0
    vegetarian = 1 if "vegetarian" in form_data else 0
    lactose_free = 1 if "lactose_free" in form_data else 0
    gluten_free = 1 if "gluten_free" in form_data else 0

    cuisine_check = recipes.cuisine_exists(cuisine_id)
    if not cuisine_check:
        print(f"VIRHE: Valittu cuisine_id={cuisine_id} ei ole olemassa!")
        return render_template(
            "new_recipe.html",
            errors={"cuisine": "Valittu ruokakulttuuri ei ole kelvollinen"},
            form_data=form_data,
            recipe_ingredients=recipe_ingredients,
            recipe_instructions=recipe_instructions,
            cuisines=cuisines,
        )

    try:
        recipe_id = recipes.add_recipe(
            title,
            description,
            cuisine_id,
            user_id,
            vegan,
            vegetarian,
            lactose_free,
            gluten_free,
        )
        recipes.add_ingredients(recipe_id, recipe_ingredients)
        recipes.add_instructions(recipe_id, recipe_instructions)

        delete_temporary_session_attributes()
        flash(f"Resepti lisätty onnistuneesti!", "success")
        return render_template("upload_image.html", recipe_id=recipe_id)

    except sqlite3.IntegrityError:
        print("VIRHE: reseptin tallennus epäonnistui")
        return render_template(
            "new_recipe.html",
            errors={"general": "Reseptin tallennus epäonnistui"},
            form_data=form_data,
            recipe_ingredients=recipe_ingredients,
            recipe_instructions=recipe_instructions,
            cuisines=session["cuisines"],
        )

    except sqlite3.DatabaseError as e:
        return render_template(
            "new_recipe.html",
            errors={"general": "Tietokantavirhe. Yritä myöhemmin uudelleen"},
            form_data=form_data,
            recipe_ingredients=recipe_ingredients,
            recipe_instructions=recipe_instructions,
            cuisines=session["cuisines"],
        )

    except Exception as e:
        return render_template(
            "new_recipe.html",
            errors={"general": "Odottamaton virhe. Yritä myöhemmin uudelleen."},
            form_data=form_data,
            recipe_ingredients=recipe_ingredients,
            recipe_instructions=recipe_instructions,
            cuisines=session["cuisines"],
        )


def render_new_recipe(errors, form_data, recipe_ingredients, recipe_instructions):
    """Helper function to render the new recipe page with given data."""
    return render_template(
        "new_recipe.html",
        errors=errors,
        form_data=form_data,
        recipe_ingredients=recipe_ingredients,
        recipe_instructions=recipe_instructions,
        cuisines=session["cuisines"],
    )


def handle_new_recipe_session_ingredients(
    form_data, recipe_ingredients, recipe_instructions
):
    """Handles adding and deleting session-based ingredients for a new recipe."""

    # Handle Adding a New Ingredient
    if "ingredient" in request.form and form_data["ingredient"] != "":
        errors = validate_recipe_form_ingredients(form_data, recipe_ingredients)
        if not errors:
            new_id = max((ing["id"] for ing in recipe_ingredients), default=0) + 1
            recipe_ingredients.append(
                {"id": new_id, "name": form_data["name"], "amount": form_data["amount"]}
            )
            session["recipe_ingredients"] = recipe_ingredients

        return render_new_recipe(
            errors, form_data, recipe_ingredients, recipe_instructions
        )

    # Handle Deleting an Ingredient
    ingredient_id_to_remove = get_delete_ingredient_id(form_data)
    if ingredient_id_to_remove:
        recipe_ingredients = [
            ing for ing in recipe_ingredients if ing["id"] != ingredient_id_to_remove
        ]
        session["recipe_ingredients"] = recipe_ingredients
        session.modified = True

        return render_new_recipe({}, form_data, recipe_ingredients, recipe_instructions)

    return None  # Return None if no action was taken


def handle_new_recipe_session_instructions(
    form_data, recipe_ingredients, recipe_instructions
):
    """Handles adding and deleting session-based instructions when creating a new recipe."""

    # Handle Adding a New Instruction
    if "instruction" in request.form and form_data["instruction"] != "":
        errors = validate_recipe_form_instructions(form_data)
        if not errors:
            new_id = max((instr["id"] for instr in recipe_instructions), default=0) + 1
            recipe_instructions.append(
                {"id": new_id, "instruction_name": form_data["instruction_name"]}
            )
            session["recipe_instructions"] = recipe_instructions

        return render_new_recipe(
            errors, form_data, recipe_ingredients, recipe_instructions
        )

    # Handle Deleting an Instruction
    instruction_id_to_remove = get_delete_instruction_id(form_data)
    if instruction_id_to_remove:
        recipe_instructions = [
            ins for ins in recipe_instructions if ins["id"] != instruction_id_to_remove
        ]
        session["recipe_instructions"] = recipe_instructions
        session.modified = True

        return render_new_recipe({}, form_data, recipe_ingredients, recipe_instructions)

    return None  # Return None if no action was taken


def add_new_recipe_image(recipe_id):
    single_recipe = recipes.get_recipe(recipe_id)
    recipe_must_exist(single_recipe)
    recipe_created_by = single_recipe["user_id"]
    logged_in_user = session["user_id"]
    user_owns_the_recipe(logged_in_user, recipe_created_by)

    file = request.files["image"]
    if file:
        if not file.filename.endswith(".jpg"):
            errors = {"general": " väärä tiedostomuoto."}
            return render_template(
                "upload_image.html", recipe_id=recipe_id, errors=errors
            )

        if file.filename == "":
            errors = {"general": "Tiedoston nimi ei voi olla tyhjä."}
            return render_template(
                "upload_image.html", recipe_id=recipe_id, errors=errors
            )

        if file and allowed_file(file.filename):
            image_data = file.read()  # Read the binary data
            if len(image_data) > 100 * 1024:
                errors = {"general": "Kuva on liian suuri"}
                return render_template(
                    "upload_image.html", recipe_id=recipe_id, errors=errors
                )

            try:
                recipes.add_recipe_image(recipe_id, image_data)

                flash(f"Reseptin kuva lisätty onnistuneesti!", "success")

                return redirect(f"/recipe/{recipe_id}")
            except Exception as e:
                print(f"Virhe kuvan tallennuksessa: {e}")  # Log error to console
                errors = {
                    "general": "Odottamaton virhe kuvan tallennuksessa. Yritä uudelleen."
                }
                return render_template(
                    "upload_image.html", recipe_id=recipe_id, errors=errors
                )

        errors = {"general": "Odottamaton virhe kuvan tallennuksessa. Yritä uudelleen."}
        return render_template("upload_image.html", recipe_id=recipe_id, errors=errors)

    return redirect(f"/recipe/{recipe_id}")


def edit_new_recipe_image(recipe_id):

    single_recipe = recipes.get_recipe(recipe_id)
    recipe_must_exist(single_recipe)
    recipe_created_by = single_recipe["user_id"]
    logged_in_user = session["user_id"]
    user_owns_the_recipe(logged_in_user, recipe_created_by)

    file = request.files["image"]
    if file:
        if file.filename == "":
            errors = {"general": "Tiedoston nimi ei voi olla tyhjä."}
            return render_template(
                "show_recipe.html", recipe_id=recipe_id, errors=errors
            )

        if file and allowed_file(file.filename):
            image_data = file.read()  # Read the binary data
            if len(image_data) > 100 * 1024:
                errors = {"general": "Kuva on liian suuri"}
                return render_template(
                    "show_recipe.html", recipe_id=recipe_id, errors=errors
                )

            try:
                if recipes.recipe_image_exists(single_recipe):
                    recipes.update_recipe_image(recipe_id, image_data)

                else:
                    recipes.add_recipe_image(recipe_id, image_data)

                flash(f"Reseptin kuva päivitetty onistuneesti!", "success")
                return redirect(f"/recipe/{recipe_id}")
            except Exception as e:
                print(f"Virhe kuvan päivityksessä: {e}")  # Log error to console
                flash("Virhe kuvan päivityksessä", "error")
                errors = {
                    "general": "Odottamaton virhe kuvan päivityksessä. Yritä uudelleen."
                }
                return render_template(
                    "upload_image.html", recipe_id=recipe_id, errors=errors
                )

        errors = {"general": "Odottamaton virhe kuvan tallennuksessa. Yritä uudelleen."}
        return render_template("upload_image.html", recipe_id=recipe_id, errors=errors)

    return redirect(f"/recipe/{recipe_id}")


def get_recipe_image_by_id(recipe_id):
    image = recipes.get_recipe_image(recipe_id)
    check_image(image)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response


def show_edit_recipe(recipe_id):
    recipe = recipes.get_recipe(recipe_id)
    recipe_must_exist(recipe)
    session["recipe"] = dict(recipe)
    cuisines = recipes.get_cuisines()
    session["cuisines"] = [dict(cuisine) for cuisine in cuisines]
    recipe_ingredients = session["recipe_ingredients"] = [
        {
            "ingredient_id": ing["ingredient_id"],
            "name": ing["name"],
            "amount": ing["amount"],
        }
        for ing in recipes.get_recipe_ingredients(recipe_id)
    ]

    recipe_instructions = session["recipe_instructions"] = [
        {"id": instr["id"], "instruction_name": instr["instruction_name"]}
        for instr in recipes.get_recipe_instructions(recipe_id)
    ]

    session["max_instruction_id"] = (
        max((instr["id"] for instr in recipe_instructions), default=0) + 1
    )
    session["max_ingredient_id"] = (
        max((ing["ingredient_id"] for ing in recipe_ingredients), default=0) + 1
    )

    return render_template(
        "edit_recipe.html",
        recipe=recipe,
        errors={},
        form_data={},
        recipe_ingredients=recipe_ingredients,
        recipe_instructions=recipe_instructions,
        cuisines=session["cuisines"],
    )


def get_updated_session_ingredients(recipe_id, form_data):
    recipe_ingredients = session.get("recipe_ingredients") or [
        {
            "ingredient_id": ing["ingredient_id"],
            "name": ing["name"],
            "amount": ing["amount"],
        }
        for ing in recipes.get_recipe_ingredients(recipe_id)
    ]
    # update ingredients with form data
    for ing in recipe_ingredients:
        updated_amount = "ingredient_" + str(ing["ingredient_id"])
        if updated_amount in form_data:
            ing["amount"] = form_data[updated_amount]

    return recipe_ingredients


def get_updated_session_instructions(recipe_id, form_data):
    recipe_instructions = session.get("recipe_instructions") or [
        {"id": instr["id"], "instruction_name": instr["instruction_name"]}
        for instr in recipes.get_recipe_instructions(recipe_id)
    ]

    # update instructions with form data
    for ins in recipe_instructions:
        updated_name = "instruction_" + str(ins["id"])
        if updated_name in form_data:
            ins["instruction_name"] = form_data[updated_name]

    return recipe_instructions


def save_edited_recipe(
    recipe, form_data, recipe_ingredients, recipe_instructions, recipe_id
):
    single_recipe = recipes.get_recipe(recipe_id)
    recipe_must_exist(single_recipe)
    recipe_created_by = recipe["user_id"]
    logged_in_user = session["user_id"]

    user_owns_the_recipe(logged_in_user, recipe_created_by)

    errors = validate_recipe_save_form(form_data)

    if errors:
        return render_template(
            "edit_recipe.html",
            recipe=recipe,
            errors=errors,
            form_data=form_data,
            recipe_ingredients=recipe_ingredients,
            recipe_instructions=recipe_instructions,
            cuisines=session["cuisines"],
        )

    title = html.escape(request.form["title"])
    description = html.escape(request.form["description"])
    user_id = session["user_id"]
    cuisine_id = form_data["cuisine"]

    vegan = 1 if "vegan" in request.form else 0
    vegetarian = 1 if "vegetarian" in request.form else 0
    lactose_free = 1 if "lactose_free" in request.form else 0
    gluten_free = 1 if "gluten_free" in request.form else 0

    try:
        recipes.edit_recipe(
            recipe_id,
            title,
            description,
            cuisine_id,
            user_id,
            vegan,
            vegetarian,
            lactose_free,
            gluten_free,
        )
        recipes.add_edit_or_remove_instructions(recipe_id, recipe_instructions)
        recipes.add_edit_or_remove_ingredients(recipe_id, recipe_ingredients)
        flash(f"Resepti {recipe_id} päivitetty onnistuneesti!", "success")
        return redirect(f"/recipe/{recipe_id}")

    except sqlite3.IntegrityError:
        return render_template(
            "edit_recipe.html",
            recipe=recipe,
            errors={
                "general": "Päivitys epäonnistui. Tarkista tiedot ja yritä uudelleen."
            },
            form_data=form_data,
            recipe_ingredients=recipe_ingredients,
            recipe_instructions=recipe_instructions,
            cuisines=session["cuisines"],
        )

    except sqlite3.DatabaseError as e:
        return render_template(
            "edit_recipe.html",
            recipe=recipe,
            errors={"general": "Tietokantavirhe. Yritä myöhemmin uudelleen"},
            form_data=form_data,
            recipe_ingredients=recipe_ingredients,
            recipe_instructions=recipe_instructions,
            cuisines=session["cuisines"],
        )

    except Exception as e:
        return render_template(
            "edit_recipe.html",
            recipe=recipe,
            errors={"general": "Odottamaton virhe. Yritä myöhemmin uudelleen."},
            form_data=form_data,
            recipe_ingredients=recipe_ingredients,
            recipe_instructions=recipe_instructions,
            cuisines=session["cuisines"],
        )


def handle_edit_recipe_session_instructions(
    recipe, form_data, recipe_ingredients, recipe_instructions
):
    """Handles adding and deleting session-based instructions in recipe editing."""

    # Handle Adding a New Instruction
    if "instruction" in request.form and form_data["instruction"] != "":
        errors = validate_recipe_form_instructions(form_data)
        if not errors:
            new_id = session["max_instruction_id"]
            session["max_instruction_id"] = int(new_id) + 1

            recipe_instructions.append(
                {"id": new_id, "instruction_name": form_data["instruction_name"]}
            )
            session["recipe_instructions"] = recipe_instructions

        return render_edit_recipe(
            recipe, errors, form_data, recipe_ingredients, recipe_instructions
        )

    # Handle Deleting an Instruction
    instruction_id_to_remove = get_delete_instruction_id(form_data)
    if instruction_id_to_remove:
        recipe_instructions = [
            ins for ins in recipe_instructions if ins["id"] != instruction_id_to_remove
        ]
        session["recipe_instructions"] = recipe_instructions
        session.modified = True

        return render_edit_recipe(
            recipe, {}, form_data, recipe_ingredients, recipe_instructions
        )

    return None  # Return None if no action was taken


def render_edit_recipe(
    recipe, errors, form_data, recipe_ingredients, recipe_instructions
):
    """Helper function to render the edit recipe page with given data."""
    return render_template(
        "edit_recipe.html",
        recipe=recipe,
        errors=errors,
        form_data=form_data,
        recipe_ingredients=recipe_ingredients,
        recipe_instructions=recipe_instructions,
        cuisines=session["cuisines"],
    )


def handle_edit_recipe_session_ingredients(
    recipe, form_data, recipe_ingredients, recipe_instructions
):
    """Handles adding and deleting session-based ingredients in recipe editing."""

    # Handle Adding a New Ingredient
    if "ingredient" in request.form and form_data["ingredient"] != "":
        errors = validate_recipe_form_ingredients(form_data, recipe_ingredients)
        if not errors:
            new_id = session["max_ingredient_id"]
            session["max_ingredient_id"] = int(new_id) + 1

            recipe_ingredients.append(
                {
                    "ingredient_id": new_id,
                    "name": form_data["name"],
                    "amount": form_data["amount"],
                }
            )
            session["recipe_ingredients"] = recipe_ingredients

        return render_edit_recipe(
            recipe, errors, form_data, recipe_ingredients, recipe_instructions
        )

    # Handle Deleting an Ingredient
    ingredient_id_to_remove = get_delete_ingredient_id(form_data)
    if ingredient_id_to_remove:
        recipe_ingredients = [
            ing
            for ing in recipe_ingredients
            if ing["ingredient_id"] != ingredient_id_to_remove
        ]
        session["recipe_ingredients"] = recipe_ingredients
        session.modified = True

        return render_edit_recipe(
            recipe, {}, form_data, recipe_ingredients, recipe_instructions
        )

    return None  # Return None if no action was taken


def delete_recipe(recipe_id):
    single_recipe = recipes.get_recipe(recipe_id)
    recipe_must_exist(single_recipe)
    user_owns_the_recipe(session["user_id"], single_recipe["user_id"])

    if request.method == "GET":
        return render_template("remove_recipe.html", recipe=single_recipe)

    if request.method == "POST":
        if "remove" in request.form:
            try:
                recipes.remove_recipe(recipe_id)
            except sqlite3.IntegrityError:
                flash(f"Reseptin {recipe_id} poistaminen epäonnistui!", "error")

            flash(f"Resepti {recipe_id} poistettu onnistuneesti!", "success")
            return redirect("/")

        return redirect("/recipe/" + str(recipe_id))


def get_delete_ingredient_id(form_data):
    """Extracts the ID of an ingredient marked for deletion."""
    delete_ingredient_key = next(
        (key for key in form_data.keys() if key.startswith("delete_ingredient_")),
        None,
    )
    if delete_ingredient_key:
        ingredient_id = delete_ingredient_key[len("delete_ingredient_") :]
        return int(ingredient_id) if ingredient_id.isdigit() else None
    return None


def get_delete_instruction_id(form_data):
    """Extracts the ID of an instruction marked for deletion."""
    delete_instruction_key = next(
        (key for key in form_data.keys() if key.startswith("delete_instruction_")), None
    )
    if delete_instruction_key:
        instruction_id = delete_instruction_key[len("delete_instruction_") :]
        return int(instruction_id) if instruction_id.isdigit() else None

    return None
