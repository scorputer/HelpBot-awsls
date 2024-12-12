# tests/test_app.py

import pytest
from src.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


def test_home_page(client):
    # Test that the home page loads successfully.
    response = client.get('/')
    assert response.status_code == 200


def test_roles_endpoint(client):
    # Test that the roles endpoint returns a 200 status code.
    # Also verify it contains "General Use".
    response = client.get('/roles')
    assert response.status_code == 200
    data = response.get_json()
    assert any(role['value'] == 'general' for role in data)

    # If you've added a CareerCoachPrompt.json file, check that it's listed
    # Replace 'CareerCoachPrompt' with any other custom prompt file name you have.
    assert any(role['value'] == 'CareerCoachPrompt' for role in data)


def test_prompt_endpoint_general(client):
    # Test the /prompt/general endpoint.
    # General should return the fallback initial_prompt by default.
    response = client.get('/prompt/general')
    assert response.status_code == 200
    data = response.get_json()
    assert 'initial_prompt' in data
    # Assuming fallback is "How can I assist you?"
    assert data['initial_prompt'] == "How can I assist you?"


def test_prompt_endpoint_career_coach(client):
    # Test the /prompt/CareerCoachPrompt endpoint if you have a
    # CareerCoachPrompt.json file with an 'initial_prompt' defined.
    response = client.get('/prompt/CareerCoachPrompt')
    # If you haven't created this prompt file, remove or adjust this test.
    assert response.status_code == 200
    data = response.get_json()
    # Check that the initial prompt matches what you defined in
    # CareerCoachPrompt.json
    assert 'initial_prompt' in data
    assert data['initial_prompt'] == (
        "Hi! What aspect of your career would you like help with today?"
    )


def test_ask_endpoint_general(client, mocker):
    # Test the /ask endpoint using the 'general' role.
    # Mock the OpenAI API call to return "Test response".
    mock_response = mocker.MagicMock()
    mock_choice = mocker.MagicMock()
    mock_choice.message = {'content': 'Test response'}
    mock_response.choices = [mock_choice]

    mocker.patch(
        'openai.ChatCompletion.create',
        return_value=mock_response
    )

    response = client.post(
        '/ask',
        json={
            'input': 'Hello',
            'role': 'general',
            'history': []
        }
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'response' in data
    assert data['response'] == 'Test response'


def test_ask_endpoint_career_coach(client, mocker):
    # Test the /ask endpoint using the 'CareerCoachPrompt' role.
    # Ensure prompts and system messages are applied correctly.
    mock_response = mocker.MagicMock()
    mock_choice = mocker.MagicMock()
    mock_choice.message = {'content': 'Career advice response'}
    mock_response.choices = [mock_choice]

    mocker.patch(
        'openai.ChatCompletion.create',
        return_value=mock_response
    )

    response = client.post(
        '/ask',
        json={
            'input': 'How can I improve my resume?',
            'role': 'CareerCoachPrompt',
            'history': []
        }
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'response' in data
    assert data['response'] == 'Career advice response'
