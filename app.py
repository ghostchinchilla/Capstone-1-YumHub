from flask import Flask, request, render_template, redirect, flash, session, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import User, Recipe, Cuisine, Favorite,  db
import requests
import config
import bcrypt
import secrets
import string

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
app.config['SECRET_KEY'] = config.SECRET_KEY

users = {}


@app.route('/')
# Render the login form or homepage
def home_page():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')
        bio = request.form.get('bio')

        # Validate form data and ensure passwords match
        if not username or not email or not password:
            flash('Please fill in all required fields.', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'error')
            return render_template('register.html')

        # Hash the password for secure storage
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        # Check if the username is unique
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Choose another.', 'error')
            return render_template('register.html')

        # Create a new user and add to the database
        new_user = User(username=username, email=email, password=hashed_password, bio=bio)
        db.session.add(new_user)  # Add the user to the database
        db.session.commit()  # Commit the transaction

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))  # Redirect to login page

    # Render the registration form for GET requests
    return render_template('register.html')
    

# Example dictionary for users (ideally, use a database)
users = {
    'john_doe': bcrypt.hashpw(b'secure_password', bcrypt.gensalt())  # Store password as a hash
}

# Route to handle user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form.get('username')
        password = request.form.get('password')

        # Retrieve the user from the database by username
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(password.encode(), user.password):  # Check if the password matches
            session['username'] = user.username  # Set session variable
            return redirect(url_for('profile', username=user.username))  # Redirect to user profile
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return render_template('login.html')  # Return with error message

    return render_template('login.html')  # Render login form for GET requests
    

@app.route('/profile/<username>', methods=['GET', 'POST'])
def manage_profile(username):
    # Retrieve user data from the database
    user = User.query.filter_by(username=username).first()

    if not user:
        return "User not found", 404  # Handle missing user profile

    if request.method == 'POST':
        # Handle profile update
        email = request.form.get('email')
        bio = request.form.get('bio')

        # Update user information in the database
        user.email = email
        user.bio = bio
        db.session.commit()  # Commit the changes to the database

        flash('Profile updated successfully.', 'success')

    # Render the profile page
    return render_template('user_profile.html', username=username, user_profile=user)  # Pass the user profile data


    
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