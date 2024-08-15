import pytest
from ai_web_app import create_app
from unittest.mock import patch

@pytest.fixture
def app():
    return create_app('tests/test_config.yaml')

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to AI Web App" in response.data

# ... (other tests remain the same)

@patch('ai_web_app.main.config')
def test_disabled_features(mock_config, client):
    mock_config['features'] = {
        'enable_data_analysis': False,
        'enable_recommendations': False,
        'enable_sentiment_analysis': False
    }
    
    response = client.post('/analyze', json={"data": "test"})
    assert response.status_code == 403
    assert "Data analysis feature is currently disabled" in response.json["message"]
    
    response = client.post('/recommend', json={"user": "test"})
    assert response.status_code == 403
    assert "Recommendations feature is currently disabled" in response.json["message"]
    
    response = client.post('/sentiment', json={"text": "test"})
    assert response.status_code == 403
    assert "Sentiment analysis feature is currently disabled" in response.json["message"]