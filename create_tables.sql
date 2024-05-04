
-- Connect to the newly created database
\c yumhub_db

-- Create the 'users' table
DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    bio TEXT
);

-- Insert initial data into 'users'
INSERT INTO users (username, email, password, bio)
VALUES ('Username1', 'Email1', 'Password1', 'Bio')
ON CONFLICT (username) DO NOTHING;
-- Create the 'cuisines' table

DROP TABLE IF EXISTS cuisines;
CREATE TABLE IF NOT EXISTS cuisines (
    cuisine_id SERIAL PRIMARY KEY,
    cuisine_name TEXT NOT NULL
);

-- Insert initial data into 'cuisines'INSERT INTO cuisines (cuisine_id, cuisine_name)
INSERT INTO cuisines (cuisine_id, cuisine_name)
VALUES (1, 'Cuisine Name')
ON CONFLICT (cuisine_id) DO NOTHING; 

-- Create the 'recipes' table with corrected foreign key references
DROP TABLE IF EXISTS recipes;
CREATE TABLE IF NOT EXISTS recipes (
    recipe_id SERIAL PRIMARY KEY,
    recipe_title VARCHAR(50) NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    cuisine_id INT,
    FOREIGN KEY (cuisine_id) REFERENCES cuisines(cuisine_id)
);

-- Insert initial data into 'recipes'
INSERT INTO recipes (recipe_title, ingredients, instructions, user_id, cuisine_id)
VALUES ('Recipe Title', 'Ingredients', 'Instructions', 1, 1);  

-- Create the 'favorites' table with correct foreign key references
DROP TABLE IF EXISTS favorites;
CREATE TABLE IF NOT EXISTS favorites (
    favorite_id SERIAL PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    recipe_id INT,
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)  
);

-- Insert initial data into 'favorites'
INSERT INTO favorites (user_id, recipe_id)
VALUES (1, 1)
ON CONFLICT (user_id, recipe_id) DO NOTHING;



CREATE TABLE IF NOT EXISTS recipe_cuisine (
    recipe_id INT, 
    cuisine_id INT, 
    PRIMARY KEY (recipe_id, cuisine_id),  -- Composite primary key
    FOREIGN KEY (recipe_id) REFERENCES recipes(id),  # Foreign key to 'recipes'
    FOREIGN KEY (cuisine_id) REFERENCES cuisines(id)  # Foreign key to 'cuisines'
);

INSERT INTO recipe_cuisine (recipe_id, cuisine_id)
VALUES
   (1, 1), 
   (2, 2)
   ON CONFLICT (recipe_id, cuisine_id) DO NOTHING;