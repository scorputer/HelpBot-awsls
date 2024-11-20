# tests/test_app.py

import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_roles_endpoint(client):
    response = client.get('/roles')
    assert response.status_code == 200
    assert b'General Use' in response.data

def test_ask_endpoint(client, mocker):
    # Mock the OpenAI API call
    mocker.patch('openai.ChatCompletion.create', return_value={
        'choices': [{'message': {'content': 'Test response'}}]
    })

    response = client.post('/ask', json={
        'input': 'Hello',
        'role': 'general',
        'history': []
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'response' in data
    assert data['response'] == 'Test response'
