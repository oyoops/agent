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

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to AI Web App" in response.data

@patch('ai_web_app.main.AICrewManager.analyze_data')
def test_analyze_route(mock_analyze, client):
    mock_analyze.return_value = {"analysis": "Test analysis"}
    response = client.post('/analyze', json={"data": "test data"}, headers={"Authorization": "Bearer secret-token-1"})
    assert response.status_code == 200
    assert response.json == {"analysis": "Test analysis"}

@patch('ai_web_app.main.AICrewManager.get_recommendation')
def test_recommend_route(mock_recommend, client):
    mock_recommend.return_value = {"recommendations": "Test recommendation"}
    response = client.post('/recommend', json={"user": "test user"}, headers={"Authorization": "Bearer secret-token-1"})
    assert response.status_code == 200
    assert response.json == {"recommendations": "Test recommendation"}

@patch('ai_web_app.main.AICrewManager.analyze_sentiment')
def test_sentiment_route(mock_sentiment, client):
    mock_sentiment.return_value = {"sentiment_analysis": "positive"}
    response = client.post('/sentiment', json={"text": "I love this product"}, headers={"Authorization": "Bearer secret-token-1"})
    assert response.status_code == 200
    assert response.json == {"sentiment_analysis": "positive"}

@patch('ai_web_app.main.AICrewManager.generate_content')
def test_generate_content_route(mock_generate, client):
    mock_generate.return_value = {"generated_content": "Test article"}
    response = client.post('/generate-content', json={"topic": "AI", "content_type": "article"}, headers={"Authorization": "Bearer secret-token-1"})
    assert response.status_code == 200
    assert response.json == {"generated_content": "Test article"}

@patch('ai_web_app.main.AICrewManager.comprehensive_analysis')
def test_comprehensive_analysis_route(mock_analysis, client):
    mock_analysis.return_value = {"comprehensive_analysis": "Detailed insights"}
    response = client.post('/comprehensive-analysis', json={"data": "complex data"}, headers={"Authorization": "Bearer secret-token-1"})
    assert response.status_code == 200
    assert response.json == {"comprehensive_analysis": "Detailed insights"}

def test_analyze_route_no_data(client):
    response = client.post('/analyze', json={}, headers={"Authorization": "Bearer secret-token-1"})
    assert response.status_code == 400
    assert "No data provided" in response.json["message"]

def test_recommend_route_no_data(client):
    response = client.post('/recommend', json={}, headers={"Authorization": "Bearer secret-token-1"})
    assert response.status_code == 400
    assert "No user data provided" in response.json["message"]

def test_sentiment_route_no_data(client):
    response = client.post('/sentiment', json={}, headers={"Authorization": "Bearer secret-token-1"})
    assert response.status_code == 400
    assert "No text provided for sentiment analysis" in response.json["message"]

def test_generate_content_route_no_data(client):
    response = client.post('/generate-content', json={}, headers={"Authorization": "Bearer secret-token-1"})
    assert response.status_code == 400
    assert "Topic and content type must be provided" in response.json["message"]

def test_comprehensive_analysis_route_no_data(client):
    response = client.post('/comprehensive-analysis', json={}, headers={"Authorization": "Bearer secret-token-1"})
    assert response.status_code == 400
    assert "No data provided for analysis" in response.json["message"]

def test_unauthorized_access(client):
    response = client.post('/analyze', json={"data": "test"})
    assert response.status_code == 401
    assert "Missing token" in response.json["error"]

    response = client.post('/analyze', json={"data": "test"}, headers={"Authorization": "Bearer invalid-token"})
    assert response.status_code == 401
    assert "Invalid token" in response.json["error"]

def test_disabled_features(app, client):
    with app.app_context():
        app.config['features'] = {
            'enable_data_analysis': False,
            'enable_recommendations': False,
            'enable_sentiment_analysis': False,
            'enable_content_generation': False,
            'enable_comprehensive_analysis': False
        }
        
        endpoints = ['/analyze', '/recommend', '/sentiment', '/generate-content', '/comprehensive-analysis']
        for endpoint in endpoints:
            response = client.post(endpoint, json={"data": "test"}, headers={"Authorization": "Bearer secret-token-1"})
            assert response.status_code == 403
            assert "is currently disabled" in response.json["message"]