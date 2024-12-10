# tests/test_app.py

import pytest
from src.app import create_app


@pytest.fixture
def client():
    # Create the Flask application and enable testing mode.
    app = create_app()
    app.config['TESTING'] = True

    # Create a test client for sending requests to the application.
    client = app.test_client()
    yield client


def test_home_page(client):
    # Test that the home page loads successfully.
    response = client.get('/')
    assert response.status_code == 200


def test_roles_endpoint(client):
    # Test that the roles endpoint returns a 200 status and contains "General Use".
    response = client.get('/roles')
    assert response.status_code == 200
    # Break long line into two to avoid E501 error
    assert b'General Use' in response.data


def test_ask_endpoint(client, mocker):
    # Create a mock response object for OpenAI's ChatCompletion.create
    mock_response = mocker.MagicMock()
    mock_response.choices = [{'message': {'content': 'Test response'}}]

    # Patch openai.ChatCompletion.create to return our mock_response object.
    mocker.patch(
        'openai.ChatCompletion.create',
        return_value=mock_response
    )

    # Send a POST request to the /ask endpoint with test input.
    response = client.post(
        '/ask',
        json={
            'input': 'Hello',
            'role': 'general',
            'history': []
        }
    )
    assert response.status_code == 200

    # Parse the JSON response from the server.
    data = response.get_json()
    assert 'response' in data
    # Verify that the response matches the mocked return value.
    assert data['response'] == 'Test response'
