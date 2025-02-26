import random
import sqlite3
import os

db = sqlite3.connect("database.db")

# Clear existing data
db.execute("DELETE FROM users")
db.execute("DELETE FROM ratings")
db.execute("DELETE FROM recipe_instructions")
db.execute("DELETE FROM recipe_ingredients")
db.execute("DELETE FROM recipes")
db.execute("DELETE FROM recipe_images")  # Clear images as well

user_count = 1000
recipe_count = 100000  # 100k recipes for load testing

# Insert users (IDs 1..1000)
for i in range(1, user_count + 1):
    username = f"user{i}"
    db.execute("INSERT INTO users (username) VALUES (?)", (username,))

# Insert recipes (all created by user 1)
for i in range(1, recipe_count + 1):
    title = f"Recipe {i}"
    description = f"This is the description for recipe {i}. Lorem ipsum dolor sit amet."
    rating = random.randint(1, 5)
    lactose_free = random.randint(0, 1)
    cuisine_id = random.randint(1, 8)  # assuming 8 cuisines exist
    db.execute(
        f"""
        INSERT INTO recipes(id, title, description, total_rating, rating_count, lactose_free, cuisine_id, user_id)
        VALUES ({i}, ?, ?, {rating}, 1, {lactose_free}, {cuisine_id}, 1)
        """,
        (title, description)
    )
    
    # Insert one ingredient (using ingredient id 1)
    amount = f"{random.randint(1,500)} g"
    db.execute(
        "INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES (?, ?, ?)",
        (amount, i, 1)
    )
    
    # Insert one instruction
    instruction = f"Step 1: Do something important for recipe {i}."
    db.execute(
        "INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES (?, ?, ?)",
        (instruction, 1, i)
    )

# For each recipe, insert 30 ratings
for recipe_id in range(1, recipe_count + 1):
    # Select 30 unique raters from user 2 to user_count
    raters = random.sample(range(2, user_count + 1), 30)
    for rated_by in raters:
        stars = random.randint(1, 5)
        comment = f"Rating for recipe {recipe_id} by user {rated_by}"
        db.execute(
            "INSERT INTO ratings(comment, stars, rated_by, recipe_id) VALUES (?, ?, ?, ?)",
            (comment, stars, rated_by, recipe_id)
        )
    if recipe_id % 1000 == 0:
        print(f"Inserted ratings for recipe {recipe_id}.")

# Insert image for every recipe using "images/2.jpg"
image_path = os.path.join("images", "2.jpg")
if os.path.exists(image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()
    for i in range(1, recipe_count + 1):
        db.execute(
            "INSERT INTO recipe_images (recipe_id, image) VALUES (?, ?)",
            (i, sqlite3.Binary(image_data))
        )
        if i % 1000 == 0:
            print(f"Uploaded image for recipe {i}.")
else:
    print(f"Image not found at {image_path}. No images were uploaded.")

db.commit()
db.close()

print("Load test data generation completed.")
