

def test_new_user(new_user):
    """
    GIVEN an User model
    WHEN new User is created
    THEN check if email, password_hash and nick are correct
    """
    assert new_user.email == 'tester1@gmail.com'
    assert new_user.password_hash == 'password123'
    assert new_user.nick == 'Tester1'


def test_new_drink(new_drink):
    """
    GIVEN a Drink model
    WHEN new Drink is created
    THEN check if name, category, technique, description and preparation are
         correct.
    """
    assert new_drink.name == 'Test Drink'
    assert new_drink.category == 'vodka'
    assert new_drink.technique == 'stir'
    assert new_drink.description == 'Test description'
    assert new_drink.preparation == 'Test preparation'


def test_new_ingredient(new_ingredient):
    """
        GIVEN an Ingredient model
        WHEN new Ingredient is created
        THEN check if ingr_name, ingr_amount and ingr_unit of ingredient are
             correct
    """
    assert new_ingredient.ingr_name == 'Test ingredient'
    assert new_ingredient.ingr_amount == 25
    assert new_ingredient.ingr_unit == 'ml'


def test_new_comment(new_comment):
    """
        GIVEN a Comment model
        WHEN new Comment is created
        THEN check if content of Comment is correct.
    """
    assert new_comment.content == 'Test comment body'
