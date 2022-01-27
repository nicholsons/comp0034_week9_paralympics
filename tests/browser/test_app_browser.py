from time import sleep

import pytest
from selenium.webdriver.common.by import By


@pytest.mark.usefixtures('chrome_driver', 'run_app')
class TestAppBrowser:
    """Class containing Selenium tests.
    This does not need to be a python class, it is written this way to give you an example of a test class.
    """

    def test_app_is_running(self):
        """ Check the app is running"""
        sleep(5)
        self.driver.get('http://127.0.0.1:5000/')
        assert self.driver.title == 'Home'

    def test_signup_succeeds(self, user_data):
        """
        Test that a user can create an account using the signup form if all fields are filled out correctly,
        and that they are redirected to the index page.
        """
        # Go to the home page
        self.driver.get('http://127.0.0.1:5000/')

        # Click signup menu link
        # See https://www.selenium.dev/documentation/webdriver/waits/
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.ID, "nav-signup").click()

        # Test person data
        first_name = "First"
        last_name = "Last"
        email = "email@ucl.ac.uk"
        password = "password1"
        password_repeat = "password1"

        # Fill in registration form
        self.driver.find_element(By.ID, "first_name").send_keys(first_name)
        self.driver.find_element(By.ID, "last_name").send_keys(last_name)
        self.driver.find_element(By.ID, "email").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "password_repeat").send_keys(password_repeat)
        self.driver.find_element(By.ID, "btn-signup").click()

        # Assert that browser redirects to index page
        self.driver.implicitly_wait(10)
        assert self.driver.current_url == 'http://127.0.0.1:5000/'

        # Assert success message is flashed on the index page
        message = self.driver.find_element(By.ID, "flash-messages").text
        assert f"Hello, {first_name} {last_name}. You are signed up." in message


def document_initialised(driver):
    return driver.execute_script("return initialised")
