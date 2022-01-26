import pytest

from paralympics_app import create_app, config, add_medals_data, add_noc_data, db as _db
from paralympics_app.models import User


@pytest.fixture(scope='session')
def app():
    """Create a Flask app for the testing"""
    app = create_app(config_class_name=config.TestingConfig)
    yield app


@pytest.fixture(scope='session')
def test_client(app):
    """Create a Flask test client to be used in tests"""
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope='session')
def db(app):
    """
    Return a session wide database using a Flask-SQLAlchemy database connection.
    """
    with app.app_context():
        _db.app = app
        _db.create_all()
        add_medals_data(_db)
        add_noc_data(_db)
        yield _db
        _db.drop_all()


@pytest.fixture(scope='function', autouse=True)
def session(db, app):
    """ Roll back database changes at the end of each test """
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        options = dict(bind=connection, binds={})
        sess = db.create_scoped_session(options=options)
        db.session = sess
        yield sess
        sess.remove()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope='module')
def user_data():
    """ Data to create a new user"""
    user_data = {
        'first_name': 'Alice',
        'last_name': 'Cooper',
        'password_text': 'SchoolsOut',
        'email': 'a_cooper@poison.net'
    }
    yield user_data


@pytest.fixture(scope='module')
def new_user(user_data):
    """ Create a user without a profile and add them to the database. Allow the user object to be used in tests. """
    user = User(first_name=user_data['first_name'], last_name=user_data['last_name'], email=user_data['email'],
                password_text=user_data['password_text'])
    yield user


@pytest.fixture(scope='function')
def user_with_profile():
    """ Creates a user with a profile. """
    user_data = {
        'first_name': 'Alison',
        'last_name': 'Krauss',
        'password_text': 'RaisingSand',
        'email': 'a_kraus@mymail.net'
    }
    profile_data = {
        'username': 'AK',
        'bio': 'My favourite paralympic sport is dressage.'
    }
    user = User(first_name=user_data['first_name'], last_name=user_data['last_name'], email=user_data['email'],
                password_text=user_data['password_text'])
    yield user
