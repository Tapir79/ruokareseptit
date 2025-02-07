
# "some_int_number": {"type": "int", "min_value": 1, "required": True},
VALIDATION_RULES = {
    "title": {"type": "string", "max_length": 30, "min_length": 1, "required": True},
    "description": {"type": "string", "max_length": 1000, "required": True},
    "name": {"type": "string", "max_length": 30, "required": True},
    "amount": {"type": "string", "max_length": 20, "required": True},
    "instruction": {"type": "string", "max_length": 150, "required": True}
}

VALIDATION_RULES_NEW_RECIPE_INGREDIENT_EDIT = {
    "name": {"type": "string", "max_length": 30, "required": True},
    "amount": {"type": "string", "max_length": 20, "required": True}
}

VALIDATION_RULES_NEW_RECIPE_INSTRUCTION_EDIT = {
    "instruction_name": {"type": "string", "max_length": 150, "required": True}
}


VALIDATION_RULES_NEW_RECIPE = {
    "title": {"type": "string", "max_length": 30, "min_length": 1, "required": True},
    "description": {"type": "string", "max_length": 1000, "required": True},
    "name": {"type": "string", "max_length": 30, "required": False},
    "amount": {"type": "string", "max_length": 20, "required": False},
    "instruction": {"type": "string", "max_length": 150, "required": False}
}

from flask import abort

def check_required(rules, value):
    if rules.get("required") and not value:
        return f"pakollinen kenttä. Anna jokin arvo."

def check_max_length(rules, value):
    if rules["type"] == "string" and "max_length" in rules and len(value) > rules["max_length"]:
        return f"Kenttä saa olla enintään {rules['max_length']} merkkiä pitkä."

def check_already_added_ingredient(value, recipe_ingredients):
    if any(ingredient["name"].lower() == value for ingredient in recipe_ingredients):
        return f"{value} on jo lisätty."


def validate_input(field_name, value):
    """Validates a single input field based on predefined rules."""
    rules = VALIDATION_RULES.get(field_name)

    if not rules:
        print(f"No validation rules for the given field: {field_name}")
        return None  

    # Required field check
    if rules.get("required") and not value:
        return f"pakollinen kenttä. Anna jokin arvo."

    try:
        if rules["type"] == "int":
            value = int(value)
    except ValueError:
        return f"saa sisältää vain numeroita. Sen tyyppi on {rules['type']}."
    
    try: 
        if rules["type"] == "float":
            value = float(value)
    except ValueError:
        return f"saa sisältää vain desimaaliluvun. Sen tyyppi on {rules['type']}."

    # Max length check for strings
    if rules["type"] == "string" and "max_length" in rules and len(value) > rules["max_length"]:
        return f"Kenttä saa olla enintään {rules['max_length']} merkkiä pitkä."

    # Min/Max value checks 
    if "min_value" in rules and value < rules["min_value"]:
        return f"Arvon on oltava vähintään {rules['min_value']} merkkiä pitkä."
    if "max_value" in rules and value > rules["max_value"]:
        return f"Arvo saa olla enintään {rules['max_value']} merkkiä pitkä."

    return None 

def validate_new_recipe_instruction_input(field_name, value, recipe_instructions=[]):

    rules = VALIDATION_RULES_NEW_RECIPE_INSTRUCTION_EDIT.get(field_name)

    if not rules:
        print(f"No validation rules for the given field: {field_name}")
        return None

    return (
        #todo check already added ingredient
        check_required(rules, value) or
        check_max_length(rules, value)
    )

def validate_new_recipe_input(field_name, value):

    rules = VALIDATION_RULES_NEW_RECIPE.get(field_name)

    if not rules:
        print(f"No validation rules for the given field: {field_name}")
        return None

    return (
        check_required(rules, value) or
        check_max_length(rules, value)
    )

def validate_new_recipe_ingredient_input(field_name, value, recipe_ingredients=[]):

    rules = VALIDATION_RULES_NEW_RECIPE_INGREDIENT_EDIT.get(field_name)

    if not rules:
        print(f"No validation rules for the given field: {field_name}")
        return None

    return (
        check_already_added_ingredient(value, recipe_ingredients) or
        check_required(rules, value) or
        check_max_length(rules, value)
    )


def user_ids_must_match(recipe_user_id, session):
    if recipe_user_id != session["user_id"]:
        abort(403)

def recipe_must_exist(recipe):
    if not recipe:
        abort(404)

def require_login(session):
    if "user_id" not in session:
        abort(403)

def validate_form(form_data):
    """Validates multiple form fields."""
    errors = {}

    for field, value in form_data.items():
        error = validate_input(field, value)
        if error:
            errors[field] = error

    return errors




def validate_new_recipe_form_ingredients(form_data, recipe_ingredients=[]):
    errors = {}

    for field, value in form_data.items():
        error = validate_new_recipe_ingredient_input(field, value, recipe_ingredients)
        if error:
            errors[field] = error

    return errors

def validate_new_recipe_form_instructions(form_data):
    errors = {}

    for field, value in form_data.items():
        error = validate_new_recipe_instruction_input(field, value)
        if error:
            errors[field] = error

    return errors

def validate_new_recipe_save_form(form_data):
    errors = {}

    for field, value in form_data.items():
        error = validate_new_recipe_input(field, value)
        if error:
            errors[field] = error

    return errors