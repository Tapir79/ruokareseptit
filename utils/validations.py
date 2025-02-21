from flask import abort

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

VALIDATION_RULES_NEW_RECIPE_INGREDIENT_EDIT = {
    "name": {"type": "string", "max_length": 30, "required": True},
    "amount": {"type": "string", "max_length": 20, "required": True}
}

VALIDATION_RULES_NEW_RECIPE_INSTRUCTION_EDIT = {
    "instruction_name": {"type": "string", "max_length": 150, "required": True}
}

VALIDATION_RULES_NEW_RECIPE = {
    "title": {"type": "string", "max_length": 30, "min_length": 1, "required": True},
    "description": {"type": "string", "max_length": 300, "required": True},
    "cuisine":{"type": "int", "required": True}
}

def check_type(rules, value):
    expected_type = rules.get("type")
    if expected_type == "string" and not isinstance(value, str):
        return "Arvon on oltava tekstiä."
    if expected_type == "int":
        try:
            int(value)  # Try converting to int
        except ValueError:
            return "Arvon on oltava kokonaisluku."


def check_required(rules, value):
    if rules.get("required") and not value:
        return f"pakollinen kenttä. Anna jokin arvo."

def check_max_length(rules, value):
    if rules["type"] == "string" and "max_length" in rules and len(value) > rules["max_length"]:
        return f"Kenttä saa olla enintään {rules['max_length']} merkkiä pitkä."

def check_already_added_ingredient(value, recipe_ingredients):
    if any(ingredient["name"].lower() == value for ingredient in recipe_ingredients):
        return f"{value} on jo lisätty."


def validate_recipe_instruction_input(field_name, value):

    rules = VALIDATION_RULES_NEW_RECIPE_INSTRUCTION_EDIT.get(field_name)

    if not rules:
        print(f"No validation rules for the given field: {field_name}")
        return None

    return (
        check_required(rules, value) or
        check_max_length(rules, value) or
        check_type(rules, value)
    )

def validate_recipe_input(field_name, value):

    rules = VALIDATION_RULES_NEW_RECIPE.get(field_name)

    if not rules:
        print(f"No validation rules for the given field: {field_name}")
        return None

    return (
        check_required(rules, value) or
        check_max_length(rules, value) or
        check_type(rules, value)
    )

def validate_recipe_ingredient_input(field_name, value, recipe_ingredients=[]):

    rules = VALIDATION_RULES_NEW_RECIPE_INGREDIENT_EDIT.get(field_name)

    if not rules:
        print(f"No validation rules for the given field: {field_name}")
        return None

    return (
        check_already_added_ingredient(value, recipe_ingredients) or
        check_required(rules, value) or
        check_max_length(rules, value) or
        check_type(rules, value)
    )

def validate_recipe_form_ingredients(form_data, recipe_ingredients=[]):
    errors = {}

    for field, value in form_data.items():
        error = validate_recipe_ingredient_input(field, value, recipe_ingredients)
        if error:
            errors[field] = error

    return errors

def validate_recipe_form_instructions(form_data):
    errors = {}

    for field, value in form_data.items():
        error = validate_recipe_instruction_input(field, value)
        if error:
            errors[field] = error

    return errors

def validate_recipe_save_form(form_data):
    errors = {}
    for field, value in form_data.items():
        error = validate_recipe_input(field, value)
        if error:
            errors[field] = error

    return errors


def user_ids_must_match(recipe_user_id, session):
    if recipe_user_id != session["user_id"]:
        abort(403)

def recipe_must_exist(recipe):
    if not recipe:
        abort(404)

def require_login(session):
    if "user_id" not in session:
        abort(403)

def user_owns_the_recipe(logged_in_user, recipe_created_by):
    if logged_in_user != recipe_created_by:
        abort(403)

def check_csrf(request, session):
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

def check_image(image):
    if not image:
        abort(404)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS