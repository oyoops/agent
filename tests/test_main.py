import pytest
from ai_web_app import app
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to AI Web App" in response.data

@patch('ai_web_app.main.ai_crew_manager.analyze_data')
def test_analyze_route(mock_analyze, client):
    mock_analyze.return_value = {"analysis": "Test analysis"}
    response = client.post('/analyze', json={"data": "test data"})
    assert response.status_code == 200
    assert response.json == {"analysis": "Test analysis"}

@patch('ai_web_app.main.ai_crew_manager.get_recommendation')
def test_recommend_route(mock_recommend, client):
    mock_recommend.return_value = {"recommendation": "Test recommendation"}
    response = client.post('/recommend', json={"user": "test user"})
    assert response.status_code == 200
    assert response.json == {"recommendation": "Test recommendation"}

@patch('ai_web_app.main.ai_crew_manager.analyze_sentiment')
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