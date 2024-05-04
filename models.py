from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import bcrypt
from datetime import datetime
import config
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
db = SQLAlchemy(app)

def connect_db(app):
    db.init_app=(app)

with app.app_context():
    db.create_all()  # Create all defined tables





class User(db.Model):
    __tablename__ = 'users'  # Define the table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # Unique constraint for username
    email = db.Column(db.String(120), unique=True, nullable=False)  # Unique constraint for email
    password = db.Column(db.String(255), nullable=False)  # Hashed password storage
    bio = db.Column(db.Text, nullable=True)  # Optional field for bio
    

class Recipes(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # Define many-to-many relationship with Cuisine table
    cuisine = db.relationship('Cuisine', secondary='recipe_cuisine', backref=db.backref('recipes'))

class Cuisine(db.Model):
    __tablename__ = "cuisines"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class Favorite(db.Model):
    __tablename__ = "favorites"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usesr.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)


recipe_cuisine = db.Table(
    'recipe_cuisine',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id')),
    db.Column('cuisine_id', db.Integer, db.ForeignKey('cuisines.id'))
)


