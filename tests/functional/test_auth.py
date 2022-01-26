from flask import url_for, current_app
from flask_login import current_user

from paralympics_app.models import User


def login(client, email, password):
    """Provides login to be used in tests"""
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def logout(client):
    """Provides logout to be used in tests"""
    return client.get('/logout', follow_redirects=True)


def test_user_can_logout(new_user, test_client, app):
    """
    GIVEN a user with a valid username and password
    WHEN the user logs in and logs out successfully
    THEN their status is anonymous
    """
    response = login(test_client, email=new_user.email, password=new_user.password)
    assert response.status_code == 200
    assert current_user is False
    logout(test_client)
    assert current_user.is_anonymous is True


def test_signup_succeeds(test_client):
    """
        GIVEN A user is not registered
        WHEN they submit a valid registration form
        THEN they should be redirected to a page with a custom welcome message and there should be an
        additional record in the user table in the database
        """
    count = User.query.count()
    response = test_client.post('/signup', data=dict(
        first_name='Person',
        last_name='Two',
        email='person_2@people.com',
        password='password2',
        password_repeat='password2'
    ), follow_redirects=True)
    count2 = User.query.count()
    assert count2 - count == 1
    assert response.status_code == 200
    assert b'Person' in response.data
