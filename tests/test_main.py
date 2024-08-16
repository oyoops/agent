import pytest
from ai_web_app import create_app
from unittest.mock import patch

@pytest.fixture
def app():
    app = create_app('tests/test_config.yaml')
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_route(client, app):
    response = client.get('/')
    assert response.status_code == 200
    expected_message = f"Welcome to {app.config['app']['name']}!"
    assert expected_message.encode() in response.data

@patch('ai_web_app.main.AICrewManager.analyze_data')
def test_analyze_route(mock_analyze, client):
    mock_analyze.return_value = {"analysis": "Test analysis"}
    response = client.post('/analyze', json={"data": "test data"})
    assert response.status_code == 200
    assert response.json == {"analysis": "Test analysis"}

@patch('ai_web_app.main.AICrewManager.get_recommendation')
def test_recommend_route(mock_recommend, client):
    mock_recommend.return_value = {"recommendation": "Test recommendation"}
    response = client.post('/recommend', json={"user": "test user"})
    assert response.status_code == 200
    assert response.json == {"recommendation": "Test recommendation"}

@patch('ai_web_app.main.AICrewManager.analyze_sentiment')
def test_sentiment_route(mock_sentiment, client):
    mock_sentiment.return_value = {"sentiment": "positive"}
    response = client.post('/sentiment', json={"text": "I love this product"})
    assert response.status_code == 200
    assert response.json == {"sentiment": "positive"}

def test_analyze_route_no_data(client):
    response = client.post('/analyze', json={})
    assert response.status_code == 400
    assert "No data provided" in response.json["message"]

def test_recommend_route_no_data(client):
    response = client.post('/recommend', json={})
    assert response.status_code == 400
    assert "No user data provided" in response.json["message"]

def test_sentiment_route_no_data(client):
    response = client.post('/sentiment', json={})
    assert response.status_code == 400
    assert "No text provided for sentiment analysis" in response.json["message"]

def test_disabled_features(app, client):
    # Temporarily modify the app's configuration for this test
    original_features = app.config['features'].copy()
    app.config['features'] = {
        'enable_data_analysis': False,
        'enable_recommendations': False,
        'enable_sentiment_analysis': False
    }

    try:
        response = client.post('/analyze', json={"data": "test"})
        assert response.status_code == 403
        assert "Data analysis feature is currently disabled" in response.json["message"]
        
        response = client.post('/recommend', json={"user": "test"})
        assert response.status_code == 403
        assert "Recommendations feature is currently disabled" in response.json["message"]
        
        response = client.post('/sentiment', json={"text": "test"})
        assert response.status_code == 403
        assert "Sentiment analysis feature is currently disabled" in response.json["message"]
    finally:
        # Restore the original configuration
        app.config['features'] = original_features