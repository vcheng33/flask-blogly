"""Blogly application."""

from flask import Flask, request, render_template, session, flash, redirect
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "somethingImportant"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.get('/')
def redirect_users_page():
    """Redirects to the users page"""
    return redirect('/users')

@app.get('/users')  
def show_user_list():
    """gets user list and renders user-listing.html"""
    users = db.session.query(User.id, User.first_name, User.last_name).all()
    return render_template('user-listing.html', 
                                users = users)

@app.get('/users/new')
def show_new_user_form():
    """Renders the user-add-form.html"""
    return render_template('user-add-form.html')

@app.post('/users/new')
def save_new_user():
    """ Takes the inputs from the new user form and add it to the database."""

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def show_user_details(user_id):
    """ Shows details about the user """

    user = User.query.get(user_id)
    posts = user.posts
    # breakpoint()

    return render_template('user-details.html', user=user, posts=posts)

@app.get('/users/<int:user_id>/edit')
def show_user_edit_page(user_id):
    # user_edit_form
    """ Shows details about the user """

    user = User.query.get(user_id)
    # breakpoint()

    return render_template('user-edit-form.html', user=user)

@app.post('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Gets the user information from the database and then 
    updates the db with user information from the new user form"""
    user = User.query.get(user_id)

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url']

    user.first_name=first_name
    user.last_name=last_name
    user.image_url=image_url
    
    db.session.commit()

    return redirect('/users')

@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Gets user information and deletes the user from the db."""
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()
    
    return redirect('/users')

