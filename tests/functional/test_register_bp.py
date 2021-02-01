from app import db
from app.models import User

from flask import get_flashed_messages, request


img = 'tests/whisky_sour.jpeg'


def test_get_register(test_app):
    """
    GIVEN testing Flask application
    WHEN '/v1/register' route send GET request
    THEN check response code and page content is correct
    """
    resp = test_app.get('/v1/register')
    assert resp.status_code == 200
    assert b'email' in resp.data
    assert b'nick' in resp.data
    assert b'password' in resp.data
    assert b'confirm_pass' in resp.data


def test_post_register(test_app):
    """
    GIVEN testing Flask application and correct user registration data
    WHEN '/v1/register route send POST request
    THEN check response code status
    """
    user_data = {'email': 'tester1@gmail.com', 'nick': 'Tester1',
                 'password': 'Password1!', 'confirm_pass': 'Password1!',
                 'file': (open(img, 'rb'), img)}
    msg = 'Your account has been created.'
    r = test_app.post('/v1/register', data=user_data, follow_redirects=True)
    user = User.query.filter_by(email=user_data['email']).first()
    db.session.delete(user)
    db.session.commit()
    assert r.status_code == 200
    assert request.path == '/v1/login'
    assert msg in get_flashed_messages()


def test_already_registered_user(test_app):
    """
    GIVEN testing Flask application and incorrect user registration data
          including already existing user email
    WHEN '/v1/register route send POST request
    THEN check response code status, flash message and redirect address
    """
    user_data = {'email': 'tester4@gmail.com', 'nick': 'Tester4',
                 'password': 'Password1!', 'confirm_pass': 'Password1!',
                 'file': (open(img, 'rb'), img)}
    r = test_app.post('/v1/register', data=user_data, follow_redirects=True)
    error_msg = 'This email address is already registered.'
    assert r.status_code == 200
    assert request.path == '/v1/register'
    assert error_msg in get_flashed_messages()


def test_different_pass_confirmpass(test_app):
    """
    GIVEN testing Flask application and incorrect user registration data
          including different password and password confirmation
    WHEN '/v1/register route send POST request
    THEN check response code status, flash message and redirect address
    """
    user_data = {'email': 'tester10@gmail.com', 'nick': 'Tester10',
                 'password': 'Password1!', 'confirm_pass': 'Something123@',
                 'file': (open(img, 'rb'), img)}
    r = test_app.post('/v1/register', data=user_data, follow_redirects=True)
    users = User.query.filter_by(email=user_data['email']).all()
    error_msg = "Password and Confirm Password don't match."
    assert r.status_code == 200
    assert request.path == '/v1/register'
    assert len(users) == 0
    assert error_msg in get_flashed_messages()


def test_existing_nickname(test_app):
    """
    GIVEN testing Flask application and incorrect user registration data
          including already existing user nick
    WHEN '/v1/register route send POST request
    THEN check response code status, flash message and redirect address
    """
    user_data = {'email': 'tester12@gmail.com', 'nick': 'Tester4',
                 'password': 'Password1!', 'confirm_pass': 'Something123@',
                 'file': (open(img, 'rb'), img)}
    r = test_app.post('/v1/register', data=user_data, follow_redirects=True)
    users = User.query.filter_by(email=user_data['email']).all()
    error_msg = 'This nickname already exists.'
    assert r.status_code == 200
    assert request.path == '/v1/register'
    assert len(users) == 0
    assert error_msg in get_flashed_messages()
