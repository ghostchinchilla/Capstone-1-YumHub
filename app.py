from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET_KEY"


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:/// '

db = SQLAlchemy()
db.app=app
db.init_app=(app)


@app.route('/')
# welcome message and login / signup form
def home_page():
    return render_template('home.html')

@app.route('/cuisine')
# Display square example photos of cuisine categories(e.g. Italian, Asian, Mexican). 
# The photo is a link to go to all the recipes of that cuisine.

@app.route('/allergies')
# Display square example photos with common allergens (e.g. gluten, dairy, nut free).
# The photo is a link to go to all the recipes of that dietary need. 

@app.route('/allergies/recipes')
# Display recipes containing common allergens

@app.route('/recipes/<int:recipe_id>')
# Show details of a specific recipe. (title, ingredients, instructions, ingredient photos and num of favorites.)
def show_recipes(recipe_id):

 @app.route('/recipes/favorites')
 # Recipe id will have a heart icon next to it that the user can click to add to favorites list.
 def show_favorites():

  @app.route('/user')
# Display user profile
  def user_profile():
    return render_template('user_profile.html')

  @app.route('/register')
# Display form and process submission
  def register():
    return render_template('register.html')

@app.route('/login')
# Display form and process submission

@app.route('/logout')
def logout():
    return render_template('home.html')