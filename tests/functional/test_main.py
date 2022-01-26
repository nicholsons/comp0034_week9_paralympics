def test_index_page_valid(test_client):
    """
    GIVEN a Flask application is running
    WHEN the '/' home page is requested (GET)
    THEN check the response is valid
    """
    response = test_client.get('/')
    assert response.status_code == 200
