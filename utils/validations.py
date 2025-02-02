
# "some_int_number": {"type": "int", "min_value": 1, "required": True},
VALIDATION_RULES = {
    "title": {"type": "string", "max_length": 30, "min_length": 1, "required": True},
    "description": {"type": "string", "max_length": 1000, "required": True},
    "name": {"type": "string", "max_length": 30, "min_length": 1, "required": True},
    "amount": {"type": "string", "max_length": 20, "min_length": 1, "required": True},
}

from flask import abort

def validate_input(field_name, value):
    """Validates a single input field based on predefined rules."""
    rules = VALIDATION_RULES.get(field_name)

    if not rules:
        print("No validation rules for the given field:" + field_name)
        return None  

    # Required field check
    if rules.get("required") and not value:
        return f"{field_name} is required."

    try:
        if rules["type"] == "int":
            value = int(value)
    except ValueError:
        return f"{field_name} saa sisältää vain numeroita. Sen tyyppi on {rules['type']}."
    
    try: 
        if rules["type"] == "float":
            value = float(value)
    except ValueError:
        return f"{field_name} saa sisältää vain desimaaliluvun. Sen tyyppi on {rules['type']}."

    # Max length check for strings
    if rules["type"] == "string" and "max_length" in rules and len(value) > rules["max_length"]:
        return f"Kenttä {field_name} saa olla enintään {rules['max_length']} merkkiä pitkä."
    
    # Min length check for strings
    if rules["type"] == "string" and "min_length" in rules and len(value) < rules["min_length"]:
        return f"Kentän {field_name} on oltava ainakin {rules['min_length']} merkkiä pitkä."

    # Min/Max value checks 
    if "min_value" in rules and value < rules["min_value"]:
        return f"{field_name} on oltava vähintään {rules['min_value']} merkkiä pitkä."
    if "max_value" in rules and value > rules["max_value"]:
        return f"{field_name} on oltava enintään {rules['max_value']} merkkiä pitkä."

    return None 

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