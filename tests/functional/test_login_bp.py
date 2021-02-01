from app import db
from app.models import User

from flask import get_flashed_messages

from flask_login import current_user

from werkzeug.security import generate_password_hash

img = 'tests/whisky_sour.jpeg'


def test_getting_login(test_app):
    """
    GIVEN testing Flask application
    WHEN '/v1/login' route send GET request
    THEN check response code and page content is correct
    """
    resp = test_app.get('/v1/login')
    assert resp.status_code == 200
    assert b'E-mail Address' in resp.data
    assert b'Password' in resp.data
    assert b'Remember Me' in resp.data
    assert b'Sign In' in resp.data


def test_login_user(test_app):
    """
    GIVEN testing Flask application and correct login data
    WHEN '/v1/login' route send POST request
    THEN check response code and page content is correct"""
    password_hash = generate_password_hash('Password123', method='SHA256')
    new_user = User(email='tester13@gmail.com', nick='Tester13',
                    password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    login_data = {'email': 'tester13@gmail.com', 'password': 'Password123'}
    r = test_app.post('/v1/login', data=login_data, follow_redirects=True)
    db.session.delete(new_user)
    db.session.commit()
    assert r.status_code == 200
    assert 'You have been logged in.' in get_flashed_messages()
    assert new_user.is_authenticated is True
    assert current_user.nick == 'Tester13'
    assert b'About the page' in r.data
