def test_index_page_valid(test_client):
    """
    GIVEN a Flask application is running
    WHEN the '/' home page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200


def test_dashboard_not_allowed_when_user_not_logged_in(test_client):
    """
    GIVEN A user is not logged
    WHEN they access the dashboard menu option
    THEN they should be redirected to the login page
    """
    response = test_client.get('/dashboard/', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data

'''
TODO: Fix this test!
def test_dashboard_allowed_when_user_is_logged_in(test_client, login_default_user):
    """
    GIVEN A user is logged in
    WHEN they access the dashboard menu option
    THEN they should go to the dashboard which contains the words 'Paralympic History'
    """
    response = test_client.get('/dashboard/')
    assert response.status_code == 200
    assert b'Paralympic History' in response.data
'''