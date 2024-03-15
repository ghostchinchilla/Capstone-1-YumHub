from flask import Flask, request, render_template, redirect, flash, session, url_for, jsonify
import requests

# from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# generating secret_key

import secrets
import string

def generate_secret_key(length=24):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(length))
    return secret_key

# Generate a secret key of length 24
secret_key = generate_secret_key()
print("Generated Secret Key:", secret_key)

app.config['SECRET_KEY'] = secret_key

# !!!!!!!!!!!!!!!  append &apikey=1 to the end of your API requests

#struggling with connecting to postgresql so actually start a database

# ??????? app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///YumHub ' ????????

db = SQLAlchemy()
db.app=app
# db.init_app(app)

# BASE_URL = ('www.themealdb.com/api/json/v1/1/categories.php')
# resp = requests.get(BASE_URL)
# data = resp.json()

users = {}


@app.route('/')
# welcome message and login / signup form
def home_page():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle form submission
        username = request.form['username']
        password = request.form['password']
        # Additional form fields can be accessed similarly

        # Perform validation (e.g., check if username is available, password meets criteria)
        if username in users:
            error = 'Username already exists. Please choose a different one.'
            return render_template('register.html', error=error)

        # Create new user account
        users[username] = {'password': password}
        # Additional user data can be stored in the users dictionary

        # Redirect to login page after successful registration
        return redirect(url_for('login'))
    else:
        # Render registration form for GET requests
        return render_template('register.html', error=None)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/profile', methods=['POST'])
def create_user_profile():
    username = request.form.get['username']
    email = request.form.get['email']
    password = request.form.get['password']
    bio = request.form.get['bio']

    # Validate form data (e.g., check for required fields, validate email format, etc.)
    if not username or not email or not password:
        # Handle missing required fields
        error = 'Please fill in all required fields.'
        return redirect(url_for('register', error=error))  # Redirect to registration page with error message

    # Store the user profile (assuming user_profiles is a dictionary)
    users[username] = {'email': email, 'password': password, 'bio': bio}

    # Redirect to the user's profile page
    return redirect(url_for('profile', username=username))


@app.route('/profile/<username>')
def profile(username):
    user_profile = users.get(username)
    if user_profile:
        return render_template('profile.html', user=user_profile)
    else:
        # Assuming you have an error template to display user not found message
        return render_template('error.html', message="User not found")

if __name__ == '__main__':
    app.run(debug=True)
    



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            # Authentication successful, redirect to a different page
            return redirect(url_for('profile', username=username))
        else:
            # Authentication failed, show error message
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)
    else:
        # Render the login form for GET requests
        return render_template('login.html', error=None)


    
@app.route('/logout')
def logout():
  # Clear the session to log out the user
    session.clear()
    # Redirect to the home page or any other desired page after logging out
    return redirect(url_for('login'))


@app.route('/cuisines')
def show_cuisines():
   # Make a request to TheMealDB API to get categories
    response = requests.get('https://www.themealdb.com/api/json/v1/1/categories.php?apikey=1')
    data = response.json()
    categories = data['categories']
    
    # Render template with categories data
    return render_template('cuisines.html', categories=categories)

if __name__ == '__main__':
    app.run(debug=True)

    @app.route('/cuisines/<cuisine_name>')
    def cuisine_recipes(cuisine_name):
    # Make a request to TheMealDB API to get recipes for the specified cuisine
     response = requests.get(f'https://www.themealdb.com/api/json/v1/1/filter.php?c={cuisine_name}&apikey=1')
     data = response.json()
     recipes = data['meals']
    
    # Render template with recipes data
     return render_template('cuisine_recipes.html', cuisine=cuisine_name, recipes=recipes)



@app.route('/recipes/<int:recipe_id>')
def recipe_details(recipe_id):
    # Make a request to TheMealDB API to get details of the recipe with the given ID
    response = requests.get(f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={recipe_id}&apikey=1')
    data = response.json()
    
    # Extract relevant information from the API response
    recipe = data['meals'][0]  # Assuming the API returns a single recipe for the given ID
    
    # Pass the recipe details to the HTML template for rendering
    return render_template('recipe_details.html', recipe=recipe)

@app.route('/favorites')
def show_favorites():
   return render_template('/favorites.html')