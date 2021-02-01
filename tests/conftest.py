from app import create_app, db
from app.models import Comment, Drink, Ingredient, User

import pytest


@pytest.fixture()
def test_app():
    app = create_app()
    with app.test_client() as test_app:
        with app.app_context():
            yield test_app


@pytest.fixture()
def new_user():
    user = User(email='tester1@gmail.com',
                password_hash='password123',
                nick='Tester1')
    return user


@pytest.fixture()
def new_drink():
    drink = Drink(name='Test Drink',
                  category='vodka',
                  technique='stir',
                  description='Test description',
                  preparation='Test preparation')
    return drink


@pytest.fixture()
def new_ingredient():
    ingredient = Ingredient(ingr_name='Test ingredient',
                            ingr_amount=25,
                            ingr_unit='ml')
    return ingredient


@pytest.fixture()
def new_comment():
    comment = Comment(content='Test comment body')
    return comment


@pytest.fixture()
def delete_test_user(email):
    user = User.query.filter_by(email=email).first()
    db.session.delete(user)
    db.session.commit()
