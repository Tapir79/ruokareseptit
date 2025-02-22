
-- test data
DELETE FROM recipes;
INSERT INTO recipes(id, title, description, total_rating, rating_count, cuisine_id, user_id)
VALUES (1,'Lihapullat','Parhaat lihapullat ruotsalaiseen tapaan.', 5, 1, 1, 1);

DELETE FROM ingredients;
INSERT INTO ingredients(id, name) VALUES(1, 'jauheliha');
INSERT INTO ingredients(id, name) VALUES(2, 'jauho');
INSERT INTO ingredients(id, name) VALUES(3, 'vehnäpaahtoleipä');
INSERT INTO ingredients(id, name) VALUES(4, 'sipuli');
INSERT INTO ingredients(id, name) VALUES(5, 'kananmuna');
INSERT INTO ingredients(id, name) VALUES(6, 'maito');
INSERT INTO ingredients(id, name) VALUES(7, 'lihaliemikuutio');
INSERT INTO ingredients(id, name) VALUES(8, 'muskottipähkinä');
INSERT INTO ingredients(id, name) VALUES(9, 'mustapippuri');
INSERT INTO ingredients(id, name) VALUES(10, 'suola');

DELETE FROM recipe_ingredients;
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES('400 g',1,1);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES('1 rkl',1,2);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES('1-2 kpl',1,3);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES('1 kpl',1,4);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES('1 kpl',1,5);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES('1 dl',1,6);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES('1 kpl',1,7);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES('hyppysellinen',1,8);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES('ripaus',1,9);
INSERT INTO recipe_ingredients(amount, recipe_id, ingredient_id) VALUES('ripaus',1,10);

DELETE FROM recipe_instructions;
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES('kuutioi leipä ja raasta sipuli',1,1);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES('lisää mausteet, leipäkuutiot ja sipuliraaste maitoon ja liota',2,1);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES('liota lihaliemikuutio pienessä määrässä kuumaa vettä ja lisää seokseen',3,1);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES('lisää joukkoon jauheliha ja kananmuna ja sekoita seos hyvin',4,1);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES('pyoritä seoksesta pieniä lihapullia',5,1);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES('ruskista pullat pannussa',6,1);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES('jätä pullat miedolle lämmölle pannuun kannen alle hautumaan',7,1);
INSERT INTO recipe_instructions(instruction, step_number, recipe_id) VALUES('Tarjoile perunamuusin, kermakastikkeen ja puolukkahillon kanssa',7,1);

DELETE FROM ratings;
INSERT INTO ratings(comment, stars, rated_by, recipe_id) VALUES('Huisin hyviä!', 5, 2, 1);

