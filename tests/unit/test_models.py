from paralympics_app.models import User


def test_user_table_empty():
    """
    GIVEN a newly created test_client
    WHEN the User table is queried
    THEN it should return zero rows
    """
    rows = User.query.count()
    assert rows == 0


def test_user_table_has_one_row(db, new_user):
    """
        GIVEN a newly created test_client
        WHEN a new user is inserted in the User table
        THEN it should return one row
        """
    db.session.add(new_user)
    db.session.commit()
    rows = User.query.count()
    assert rows == 1


def test_new_user_details_correct(new_user, test_client):
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
    user = User(first_name=user_data['first_name'], last_name=user_data['last_name'], email=user_data['email'],
                password_text=user_data['password_text'])
    assert user.first_name == 'Meat'
    assert user.last_name == 'Loaf'
    assert user.email == 'meat@bat.org'
    assert user.password != 'BatOutOfHell'
