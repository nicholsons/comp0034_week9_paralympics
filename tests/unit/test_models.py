from paralympics_app.models import User


def test_new_user_details_correct():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the first_name, last_name, email, and password fields are defined correctly
    """
    user_data = {
        'first_name': 'Meat',
        'last_name': 'Loaf',
        'password_text': 'BatOutOfHell',
        'email': 'meat@bat.org'
    }

    user = User(first_name='Meat', last_name='Loaf', email='meat@bat.org', password_text='BatOutOfHell')

    assert user.first_name == 'Meat'
    assert user.last_name == 'Loaf'
    assert user.email == 'meat@bat.org'
    assert user.password != 'BatOutOfHell'


def test_user_table_has_one_more_row(db, new_user):
    """
        GIVEN the app database
        WHEN a new user is inserted in the User table
        THEN the row count should increase by one
        """
    row_count_1 = User.query.count()
    db.session.add(new_user)
    db.session.commit()
    row_count_2 = User.query.count()
    assert row_count_2 - row_count_1 == 1
