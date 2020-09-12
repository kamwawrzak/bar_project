from flask import current_app as app
from flask import render_template

from flask_login import login_required


@app.route('/')
def index():
    return render_template('base.html', title='Home')


@app.route('/v1/register')
def registration():
    return render_template('register.html', title='Registration')


@app.route('/v1/login')
def login():
    return render_template('login.html', title='Login')


@login_required
@app.route('/v1/add_drink')
def add_drink():
    return render_template('add_drink.html', title='Add Drink')


@app.route('/v1/drinks')
def display_drinks():
    return render_template('display_drinks.html', title='Drinks')
