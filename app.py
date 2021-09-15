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
    return redirect('/users')

@app.get('/users')  
def show_user_list():
    users = db.session.query(User.id, User.first_name, User.last_name).all()
    return render_template('user-listing.html', 
                                users = users)


@app.get('/users/new')
def show_new_user_form():
    return render_template('user-form.html')