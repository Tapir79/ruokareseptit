# Kuormitustestaus

Kuormitustestaamista varten luotu ja ladattu testidataa tietokantaan seuraavasti: 
````
python generate_load_test_data.py

sqlite3 database.db < install/load_test_data.sql
````

## Pyyntöjen aikaa mitattu seuraavasti:
````
@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response
````
- etusivun lataus 0.0s 
- haku ilman suodattimia (ilman indeksiä)
````
elapsed time: elapsed time: 6.02 s
elapsed time: 5.88  6.1 s
elapsed time: 6.02 s 
127.0.0.1 - - [25/Feb/2025 22:55:01] "GET /recipe/99999/image HTTP/1.1" 200 -
elapsed time: 6.0 s 
127.0.0.1 - - [25/Feb/2025 22:55:01] "GET /recipe/99996/image HTTP/1.1" 200 -6.09ss
127.0.0.1 - - [25/Feb/2025 22:55:01] "GET /recipe/99998/image HTTP/1.1" 200 -
127.0.0.1 - - [25/Feb/2025 22:55:01] "GET /recipe/99997/image HTTP/1.1" 200 -
127.0.0.1 - - [25/Feb/2025 22:55:01] "GET /recipe/100000/image HTTP/1.1" 200 -
````
- haku ilman suodattimia (indeksillä)
````
elapsed time: 0.0 s
127.0.0.1 - - [25/Feb/2025 23:04:58] "GET /recipe/99990/image HTTP/1.1" 200 -
elapsed time: 0.01 s
127.0.0.1 - - [25/Feb/2025 23:04:58] "GET /recipe/99989/image HTTP/1.1" 200 -
elapsed time: elapsed time:0.01 s 
elapsed time:0.01 s 0.0 
127.0.0.1 - - [25/Feb/2025 23:04:58] "GET /recipe/99988/image HTTP/1.1" 200 -
127.0.0.1 - - [25/Feb/2025 23:04:58] "GET /recipe/99987/image HTTP/1.1" 200 -
127.0.0.1 - - [25/Feb/2025 23:04:58] "GET /recipe/99986/image HTTP/1.1" 200 -
````
- haku kaikilla suodattimilla (yht. 5 AND ehtoa ja 3 OR ehtoa) 0.01s (indeksillä)

## Sovellukseen lisätyt suorituskykyparannukset: 

- loading="lazy" html image-tageihin (ei merkittävää parannusta)
- indeksin lisääminen 
- Sovelluksen etusivu lataa vain yhden kaikkein suosituimman reseptin  tähtiluokituksen ja arvosteluiden määrän perusteella
- Sovelluksen haku käyttää sivutusta, jonka vuoksi hakutulosten selaaminen on nopeaa 
- TODO: Sovelluksen kommentit on sivutettu ja niitä näytetään sivulla kerrallaan maksimissaan 10 
- TODO: Käyttäjän tiedot on sivutettu ja niitä näytetään sivulla maksimissaan 10

## Parannukset tietokantakyselyihin 

kysely lopetetaan heti ensimmäisen osuman jälkeen, kun se suoritetaan muodossa SELECT EXISTS(subquery).

````
def recipe_image_exists(recipe_id):
    sql = """SELECT EXISTS (SELECT 1 FROM recipe_images WHERE recipe_id = ?)"""
    result = db.query(sql, [recipe_id])
    return result[0][0] == 1


def cuisine_exists(cuisine_id):
    sql = "SELECT EXISTS (SELECT 1 FROM cuisines WHERE id = ?)"
    result = db.query(sql, [cuisine_id])

    return result[0][0] == 1
````

## Indeksit: 

Indeksi lisätty kenttiin, joihin kohdistuu filtteröintejä, hakuja tai liitoksia muihin tauluihin. 
Indeksi luodaan automaattisesti, jos kentässä tai kenttien yhdistelmässä on määrittely UNIQUE. Näissä tapauksissa ei tarvitse luoda ideksiä.
Lisätyt indeksit:
````
CREATE INDEX idx_recipes_title ON recipes(title);
CREATE INDEX idx_recipes_cuisine ON recipes(cuisine_id);
CREATE INDEX idx_recipes_user ON recipes(user_id);
CREATE INDEX idx_recipe_ingredients_recipe ON recipe_ingredients(recipe_id);
CREATE INDEX idx_recipe_ingredients_ingredient ON recipe_ingredients(ingredient_id);
CREATE INDEX idx_recipe_instructions_recipe ON recipe_instructions(recipe_id);
CREATE INDEX idx_ratings_recipe ON ratings(recipe_id);
CREATE INDEX idx_recipe_images_recipe ON recipe_images(recipe_id);
````