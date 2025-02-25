import os
import sqlite3

# Connect to the SQLite database.
db = sqlite3.connect("database.db")

# Enable foreign keys (needed by the schema)
db.execute("PRAGMA foreign_keys = ON;")

# Loop through recipe IDs 1 to 18.
for recipe_id in range(1, 19):
    if recipe_id < 4:
        image_path = os.path.join("images", f"{recipe_id}.jpg")
    else: 
        image_path = os.path.join("images", "2.jpg")
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            image_data = f.read()
        # Insert the image as a blob. sqlite3.Binary() converts the bytes appropriately.
        db.execute(
            "INSERT INTO recipe_images (recipe_id, image) VALUES (?, ?)",
            (recipe_id, sqlite3.Binary(image_data))
        )
        print(f"Loaded image for recipe {recipe_id}.")
    else:
        print(f"Image not found for recipe {recipe_id}, skipping.")

# Commit changes and close the database.
db.commit()
db.close()
