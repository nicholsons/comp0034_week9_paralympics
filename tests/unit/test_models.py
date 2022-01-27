from paralympics_app.models import User


def test_new_user_details_correct():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the first_name, last_name, email, and password fields are defined correctly
    """
    user = User(first_name='Meat', last_name='Loaf', email='meat@bat.org', password_text='BatOutOfHell')

    assert user.first_name == 'Meat'
    assert user.last_name == 'Loaf'
    assert user.email == 'meat@bat.org'
    assert user.password != 'BatOutOfHell'
