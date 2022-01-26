# Fixtures for the Selenium tests only
import multiprocessing

import pytest
from selenium.webdriver import Firefox, Chrome, ChromeOptions
from selenium.webdriver.firefox.options import Options

from paralympics_app import create_app, config, add_medals_data, add_noc_data, db as _db


@pytest.fixture(scope='session')
def app():
    """Create a Flask app for the testing"""
    app = create_app(config_class_name=config.TestingConfig)
    multiprocessing.set_start_method(
        "fork")  # Needed in Python 3.8, call it once before live_server is used
    # https://github.com/pytest-dev/pytest-flask/issues/104
    with app.app_context():
        _db.app = app
        _db.create_all()
        add_medals_data(_db)
        add_noc_data(_db)
        yield app
        _db.drop_all()


@pytest.fixture(scope='class')
def firefox_driver():
    """ Selenium webdriver with options for running headless browser tests through GitHub"""
    opts = Options()
    opts.headless = True
    ffox_driver = Firefox(options=opts)
    ffox_driver.implicitly_wait(10)  # Delay to wait for the connection to be established
    yield ffox_driver
    ffox_driver.quit()


@pytest.fixture(scope='class')
def chrome_driver(request):
    """ Selenium webdriver with options to support running in GitHub actions"""
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    # options.add_argument("--window-size=1920,1080")  # use only when not in headless
    chrome_driver = Chrome(options=options)
    request.cls.driver = chrome_driver
    yield
    chrome_driver.close()
