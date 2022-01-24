import pytest

from paralympics_app import create_app, config
from paralympics_app.models import User


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(config_class_name=config.TestingConfig)
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def user_data():
    user_data = {
        'first_name': 'Alice',
        'last_name': 'Cooper',
        'password_text': 'SchoolsOut',
        'email': 'a_cooper@poison.net'
    }
    return user_data


@pytest.fixture(scope='module')
def new_user(user_data):
    user = User(first_name=user_data['first_name'], last_name=user_data['last_name'], email=user_data['email'],
                password_text=user_data['password_text'])
    return user
