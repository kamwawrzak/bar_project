from flask import current_app as app
from flask import render_template


@app.route('/')
def index():
    return render_template('base.html', title='Home')


@app.route('/v1/register')
def registration():
    return render_template('register.html', title='Registration')


@app.route('/v1/login')
def login():
    return render_template('login.html', title='Login')
