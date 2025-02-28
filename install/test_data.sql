-- Clear existing users (if any)
DELETE FROM users;

-------------------------------------------------
-- Insert 2 test users
-- guybrush/guybrush
-- elaine/elaine
-------------------------------------------------
INSERT INTO users(id, username, password_hash) VALUES
    (1, 'guybrush', 'scrypt:32768:8:1$MPut1LWmAa0itDuu$8e59b189c39a66479f815ba59e42e82fa51725f02dfc8e2083d36172dd63ead9623ed7eeac8edb80d5213200e53238ccfe0dee66bff406035b37348c8caca59e'),
    (2, 'elaine', 'scrypt:32768:8:1$sFOb3SxH2gPebwVf$18f00efff10933f37222f9b88db59321f740f783d66068937517965faea221369fe696be4ee1a8621aa5978641a616075ff2c10cee34eb761be4d5d01cc33691');

-- Clean up existing test data
DELETE FROM ratings;
DELETE FROM recipe_instructions;
DELETE FROM recipe_ingredients;
DELETE FROM ingredients;
DELETE FROM recipes;

-------------------------------------------------
-- Recipe 1: Laskiaispullat
-------------------------------------------------
INSERT INTO recipes(id, title, description, total_rating, rating_count, lactose_free, cuisine_id, user_id)
VALUES (1, 'Laskiaispullat', 'Parhaat laskiaispullat ruotsalaiseen tapaan. Voit halutessasi korvata mantelimassan mansikkahillolla.', 5, 1, 1, 1, 1);

-------------------------------------------------
-- Recipe 2: Karjalanpaisti
-------------------------------------------------
INSERT INTO recipes(id, title, description, total_rating, rating_count, lactose_free, cuisine_id, user_id)
VALUES (2, 'Karjalanpaisti', 'Perinteinen karjalainen lihapata, haudutettu miedolla lämmöllä useita tunteja, mikä tekee lihasta erityisen mureaa.', 3, 1, 0, 1, 2);

-------------------------------------------------
-- Recipe 3: Lihapullat
-------------------------------------------------
INSERT INTO recipes(id, title, description, total_rating, rating_count, lactose_free, cuisine_id, user_id)
VALUES (3, 'Lihapullat', 'Lihapullat kermakastikkeessa ruotsalaiseen tapaan. Tarjoile perunamuusin ja puolukkahillon kanssa.', 4, 1, 1, 1, 2);


-- Ingredients for Laskiaispullat
INSERT INTO ingredients(id, name) VALUES
  (1, 'laktoositon maito'),
  (2, 'kuivahiiva'),
  (3, 'taloussokeri'),
  (4, 'puolikarkea vehnäjauho'),
  (5, 'suola'),
  (6, 'kardemumma'),
  (7, 'laktoositon voi (tai margariini)'),
  (8, 'rypsi- tai auringonkukkaöljy'),
  (9, 'kananmuna'),
  (10, 'raesokeri'),
  (11, 'laktoositon vispikerma'),
  (12, 'mantelimassa');

  -- Additional ingredients for Karjalanpaisti (if not already used)
INSERT INTO ingredients(id, name) VALUES
  (13, 'naudanliha'),
  (14, 'porsaanliha'),
  (15, 'sipuli'),
  (16, 'porkkana'),
  (17, 'laakerinlehti'),
  (18, 'kokonaiset mustapippurit'),
  (19, 'vesi');

  -- Additional ingredients for Lihapullat (if not already used)
INSERT INTO ingredients(id, name) VALUES
  (20, 'valeaa paahtoleipää'),
  (21, 'nauta-porsaan jauheliha'),
  (22, 'muskottipähkinä jauheena'),
  (23, 'mustapippuri jauheena'),
  (24, 'ruokaöljy'),
  (25, 'lihaliemikuutio'),
  (26, 'ruokakerma');

-- Recipe ingredients for Laskiaispullat
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES
  ('5 dl', 1, 1),
  ('2 pussia', 1, 2),
  ('2 dl', 1, 3),
  ('n. 15 dl', 1, 4),
  ('2 tl', 1, 5),
  ('1 rkl', 1, 6),
  ('100 g', 1, 7),
  ('3/4 dl', 1, 8),
  ('1 kpl', 1, 9),
  ('1/5 dl', 1, 10),
  ('2 dl', 1, 11),
  ('1 levy', 1, 12);

  -- Recipe ingredients for Karjalanpaisti
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES
  ('500 g', 2, 13),
  ('500 g', 2, 14),
  ('2 kpl', 2, 15),
  ('3 kpl', 2, 16),
  ('2 kpl', 2, 17),
  ('5 kpl', 2, 18),
  ('1 litra', 2, 19),
  ('1 tl', 2, 5);

  -- Recipe ingredients for Lihapullat
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES
  ('1 dl', 3, 1),
  ('1 tl', 3, 3),
  ('2 viipaletta', 3, 20),
  ('1 kpl', 3, 15),
  ('600 g', 3, 21),
  ('1 kpl', 3, 9),
  ('1/4 tl', 3, 22),
  ('1/4 tl', 3, 23),
  ('3/4 tl', 3, 20),
  ('1 rkl', 3, 8),
  ('4 rkl', 3, 7),
  ('4 rkl', 3, 4),
  ('1,5 kpl', 3, 25),
  ('2 dl', 3, 19),
  ('2 dl',3, 26);


-- Recipe instructions for Laskiaispullat
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES
  ('Lämmitä maito kädenlämpöiseksi (noin 40 C)', 1, 1),
  ('Liuota maitoon hiiva, sokeri, suola ja kardemumma. Sekoita hyvin.', 2, 1),
  ('Lisää seokseen 10 dl jauhoja pienissä erissä koko ajan sekoittaen.', 3, 1),
  ('Sulata voi pehmeäksi.', 4, 1),
  ('Lisää sulatettu voi ja öljy seokseen.', 5, 1),
  ('Lisää loput jauhot (5 dl) pienissä erissä koko ajan sekoittaen.', 6, 1),
  ('Jätä taikina kohoamaan liinan alle.', 7, 1),
  ('Laita uuni lämpiämään 225 asteeseen.', 8, 1),
  ('Jaa kohonnut taikina 15 osaan.', 9, 1),
  ('Pyörittele taikinapalaset pyöreiksi palloiksi ja aseta ne uunipellille leivinpaperin päälle.', 10, 1),
  ('Peitä pullat liinalla ja anna kohota noin 15–20 minuuttia.', 11, 1),
  ('Riko kananmuna ja sekoita siihen noin ruokalusikallinen kylmää vettä.', 12, 1),
  ('Voitele pullat kananmunaseoksella.', 13, 1),
  ('Ripottele raesokeri pullien päälle koristeluun.', 14, 1),
  ('Paista pullia uunissa 225 asteessa noin 10–15 minuuttia tai kunnes ne ovat kullanruskeita.', 15, 1);

-- Recipe instructions for Karjalanpaisti
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES
  ('Leikkaa naudan- ja porsaanliha sopiviksi kuutioiksi.', 1, 2),
  ('Kuullota hienonnettu sipuli suuressa kattilassa.', 2, 2),
  ('Lisää liha kattilaan ja ruskista se kevyesti.', 3, 2),
  ('Lisää porkkanat, laakerinlehdet ja mustapippurit.', 4, 2),
  ('Kaada päälle vesi ja mausta suolalla.', 5, 2),
  ('Hauduta miedolla lämmöllä noin 2-3 tuntia, kunnes liha on mureaa.', 6, 2),
  ('Poista laakerinlehdet ennen tarjoilua.', 7, 2);

-- Recipe instructions for Lihapullat
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES
  ('Viipaloi leipäviipaleet pieniksi kuutioiksi.', 1, 3),
  ('Liota toinen lihaliemikuutio pienessä määrässä kuumaa vettä.', 2, 3),
  ('Lisää kulhoon leipäviipaleet, lihaliemi, maito, muskottipähkinä sekä ripaus suolaa ja teelusikallinen sokeria', 3, 3),
  ('Silppua ja kuullota sipuli pannulla.', 4, 3),
  ('Lisää sipulit leipä-lihaliemi-maitosekoitukseen', 5, 3),
  ('Muussaa sipuli-leipäseos hienoksi haarukalla.', 6, 3),
  ('Lisää joukkoon jauheliha ja sekoita käsin.', 7, 3),
  ('Pyörittele jauhelihataikinasta pieniä palloja.', 8, 3),
  ('Ruskista lihapullat pannulla voissa tai öljyssä ja nosta ne odottamaan kattilaan', 9, 3),
  ('Tehdään nyt kastike. Lisää pieneen kattilaan voi ja vehnäjauhot ja ruskista.', 10, 3),
  ('Tee puolikkaasta lihaliemikuutiosta 2 dl lihalientä ja sekoita se vähitellen voi-vehnäjauhoseokseen.', 11, 3),
  ('Kun kastike on paksua, kaada joukkoon kerma ja sekoita vielä hetki. Kastikkeen pitäisi olla hieman notkeaa, mutta ei juoksevaa.', 12, 3),
  ('Kaada kastike lihapullien päälle ja hauduta miedolla lämmöllä kattilassa kannen alla noin 20 minuuttia.', 13, 3);

-- Ratings for Laskiaispullat
INSERT INTO ratings(comment, stars, rated_by, recipe_id) VALUES
  ('Hurjan hyviä!', 5, 2, 1);

-- Ratings for Karjalanpaisti
INSERT INTO ratings(comment, stars, rated_by, recipe_id) VALUES
  ('Ihan ok resepti!', 3, 1, 2);

-- Ratings for Lihapullat
INSERT INTO ratings(comment, stars, rated_by, recipe_id) VALUES
  ('Parempia kuin Ikean lihapullat!', 4, 1, 3);

-------------------------------------------
-- Lorem ipsum data for testing pagination
-------------------------------------------

-- Recipe 4: Lorem Ipsum Recipe 4 (No tag, Pattern 0)
INSERT INTO recipes(id, title, description, total_rating, rating_count, lactose_free, vegan, vegetarian, gluten_free, cuisine_id, user_id)
VALUES (4, 'Lorem Ipsum Recipe 4', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 1, 1, 0, 0, 0, 0, 2, 1);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES ('100 g', 4, 1);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES ('Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 1, 4);
INSERT INTO ratings(comment, stars, rated_by, recipe_id) VALUES ('Lorem ipsum comment.', 1, 1, 4);

-- Recipe 5: Lorem Ipsum Recipe 5 (Laktoositon, Pattern 1)
INSERT INTO recipes(id, title, description, total_rating, rating_count, lactose_free, vegan, vegetarian, gluten_free, cuisine_id, user_id)
VALUES (5, 'Lorem Ipsum Recipe 5', 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 2, 1, 1, 0, 0, 0, 3, 2);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES ('150 g', 5, 2);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES ('Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 1, 5);
INSERT INTO ratings(comment, stars, rated_by, recipe_id) VALUES ('Consectetur adipiscing elit.', 2, 2, 5);

-- Recipe 6: Lorem Ipsum Recipe 6 (Vegan, Pattern 2)
INSERT INTO recipes(id, title, description, total_rating, rating_count, lactose_free, vegan, vegetarian, gluten_free, cuisine_id, user_id)
VALUES (6, 'Lorem Ipsum Recipe 6', 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', 3, 1, 0, 1, 0, 0, 4, 1);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES ('200 g', 6, 3);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES ('Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', 1, 6);
INSERT INTO ratings(comment, stars, rated_by, recipe_id) VALUES ('Duis aute irure dolor in reprehenderit.', 3, 1, 6);

-- Recipe 7: Lorem Ipsum Recipe 7 (Kasvis, Pattern 3)
INSERT INTO recipes(id, title, description, total_rating, rating_count, lactose_free, vegan, vegetarian, gluten_free, cuisine_id, user_id)
VALUES (7, 'Lorem Ipsum Recipe 7', 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', 4, 1, 0, 0, 1, 0, 5, 2);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES ('120 g', 7, 1);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES ('Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', 1, 7);
INSERT INTO ratings(comment, stars, rated_by, recipe_id) VALUES ('Excepteur sint occaecat cupidatat non proident.', 4, 2, 7);

-- Recipe 8: Lorem Ipsum Recipe 8 (Gluteeniton, Pattern 4)
INSERT INTO recipes(id, title, description, total_rating, rating_count, lactose_free, vegan, vegetarian, gluten_free, cuisine_id, user_id)
VALUES (8, 'Lorem Ipsum Recipe 8', 'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 1, 1, 0, 0, 0, 1, 6, 1);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES ('130 g', 8, 2);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES ('Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 1, 8);
INSERT INTO ratings(comment, stars, rated_by, recipe_id) VALUES ('Lorem ipsum dolor sit amet.', 1, 1, 8);

-- Recipe 9: Lorem Ipsum Recipe 9 (No tag, Pattern 0)
INSERT INTO recipes(id, title, description, total_rating, rating_count, lactose_free, vegan, vegetarian, gluten_free, cuisine_id, user_id)
VALUES (9, 'Lorem Ipsum Recipe 9', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor.', 2, 1, 0, 0, 0, 0, 7, 2);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES ('140 g', 9, 3);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor.', 1, 9);
INSERT INTO ratings(comment, stars, rated_by, recipe_id) VALUES ('Ut enim ad minim veniam.', 2, 2, 9);

-- Recipe 10: Lorem Ipsum Recipe 10 (Laktoositon, Pattern 1)
INSERT INTO recipes(id, title, description, total_rating, rating_count, lactose_free, vegan, vegetarian, gluten_free, cuisine_id, user_id)
VALUES (10, 'Lorem Ipsum Recipe 10', 'Quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', 3, 1, 1, 0, 0, 0, 8, 1);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES ('110 g', 10, 1);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES ('Quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', 1, 10);
INSERT INTO ratings(comment, stars, rated_by, recipe_id) VALUES ('Sed do eiusmod tempor incididunt.', 3, 1, 10);

-- Recipe 11: Lorem Ipsum Recipe 11 (Vegan, Pattern 2)
INSERT INTO recipes(id, title, description, total_rating, rating_count, lactose_free, vegan, vegetarian, gluten_free, cuisine_id, user_id)
VALUES (11, 'Lorem Ipsum Recipe 11', 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', 4, 1, 0, 1, 0, 0, 1, 2);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES ('115 g', 11, 2);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES ('Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', 1, 11);
INSERT INTO ratings(comment, stars, rated_by, recipe_id) VALUES ('Excepteur sint occaecat cupidatat.', 4, 2, 11);

-- Recipe 12: Lorem Ipsum Recipe 12 (Kasvis, Pattern 3)
INSERT INTO recipes(id, title, description, total_rating, rating_count, lactose_free, vegan, vegetarian, gluten_free, cuisine_id, user_id)
VALUES (12, 'Lorem Ipsum Recipe 12', 'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 1, 1, 0, 0, 1, 0, 2, 1);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES ('125 g', 12, 3);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES ('Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 1, 12);
INSERT INTO ratings(comment, stars, rated_by, recipe_id) VALUES ('Lorem ipsum dolor sit amet, consectetur adipiscing elit.', 1, 1, 12);

-- Recipe 13: Lorem Ipsum Recipe 13 (Gluteeniton, Pattern 4)
INSERT INTO recipes(id, title, description, total_rating, rating_count, lactose_free, vegan, vegetarian, gluten_free, cuisine_id, user_id)
VALUES (13, 'Lorem Ipsum Recipe 13', 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 2, 1, 0, 0, 0, 1, 3, 2);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES ('135 g', 13, 1);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES ('Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 1, 13);
INSERT INTO ratings(comment, stars, rated_by, recipe_id) VALUES ('Ut enim ad minim veniam, quis nostrud exercitation.', 2, 2, 13);

-- Recipe 14: Lorem Ipsum Recipe 14 (No tag, Pattern 0)
INSERT INTO recipes(id, title, description, total_rating, rating_count, lactose_free, vegan, vegetarian, gluten_free, cuisine_id, user_id)
VALUES (14, 'Lorem Ipsum Recipe 14', 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', 3, 1, 0, 0, 0, 0, 4, 1);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES ('145 g', 14, 2);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES ('Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', 1, 14);
INSERT INTO ratings(comment, stars, rated_by, recipe_id) VALUES ('Duis aute irure dolor in reprehenderit.', 3, 1, 14);

-- Recipe 15: Lorem Ipsum Recipe 15 (Laktoositon, Pattern 1)
INSERT INTO recipes(id, title, description, total_rating, rating_count, lactose_free, vegan, vegetarian, gluten_free, cuisine_id, user_id)
VALUES (15, 'Lorem Ipsum Recipe 15', 'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', 4, 1, 1, 0, 0, 0, 5, 2);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES ('155 g', 15, 3);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES ('Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', 1, 15);
INSERT INTO ratings(comment, stars, rated_by, recipe_id) VALUES ('Excepteur sint occaecat cupidatat non proident.', 4, 2, 15);

-- Recipe 16: Lorem Ipsum Recipe 16 (Vegan, Pattern 2)
INSERT INTO recipes(id, title, description, total_rating, rating_count, lactose_free, vegan, vegetarian, gluten_free, cuisine_id, user_id)
VALUES (16, 'Lorem Ipsum Recipe 16', 'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 1, 1, 0, 1, 0, 0, 6, 1);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES ('160 g', 16, 1);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES ('Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', 1, 16);
INSERT INTO ratings(comment, stars, rated_by, recipe_id) VALUES ('Lorem ipsum dolor sit amet.', 1, 1, 16);

-- Recipe 17: Lorem Ipsum Recipe 17 (Kasvis, Pattern 3)
INSERT INTO recipes(id, title, description, total_rating, rating_count, lactose_free, vegan, vegetarian, gluten_free, cuisine_id, user_id)
VALUES (17, 'Lorem Ipsum Recipe 17', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor.', 2, 1, 0, 0, 1, 0, 7, 2);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES ('165 g', 17, 2);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES ('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor.', 1, 17);
INSERT INTO ratings(comment, stars, rated_by, recipe_id) VALUES ('Ut enim ad minim veniam.', 2, 2, 17);

-- Recipe 18: Lorem Ipsum Recipe 18 (Gluteeniton, Pattern 4)
INSERT INTO recipes(id, title, description, total_rating, rating_count, lactose_free, vegan, vegetarian, gluten_free, cuisine_id, user_id)
VALUES (18, 'Lorem Ipsum Recipe 18', 'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 3, 1, 0, 0, 0, 1, 8, 1);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES ('170 g', 18, 3);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES ('Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.', 1, 18);
INSERT INTO ratings(comment, stars, rated_by, recipe_id) VALUES ('Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', 3, 1, 18);

