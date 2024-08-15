import pytest
from ai_web_app import AICrewManager
from unittest.mock import patch, MagicMock

@pytest.fixture
def ai_crew_manager():
    return AICrewManager(api_key="test_key", model_name="test_model", max_tokens=100, temperature=0.7)

@patch('ai_web_app.crew_integration.Crew')
def test_analyze_data(mock_crew, ai_crew_manager):
    mock_crew_instance = MagicMock()
    mock_crew_instance.kickoff.return_value = {"analysis": "Test analysis"}
    mock_crew.return_value = mock_crew_instance

    result = ai_crew_manager.analyze_data({"test": "data"})
    assert result == {"analysis": "Test analysis"}
    mock_crew.assert_called_once()
    mock_crew_instance.kickoff.assert_called_once()

@patch('ai_web_app.crew_integration.Crew')
def test_get_recommendation(mock_crew, ai_crew_manager):
    mock_crew_instance = MagicMock()
    mock_crew_instance.kickoff.return_value = {"recommendation": "Test recommendation"}
    mock_crew.return_value = mock_crew_instance

    result = ai_crew_manager.get_recommendation({"user": "test"})
    assert result == {"recommendation": "Test recommendation"}
    mock_crew.assert_called_once()
    mock_crew_instance.kickoff.assert_called_once()

@patch('ai_web_app.crew_integration.Crew')
def test_analyze_sentiment(mock_crew, ai_crew_manager):
    mock_crew_instance = MagicMock()
    mock_crew_instance.kickoff.return_value = {"sentiment": "positive"}
    mock_crew.return_value = mock_crew_instance

    result = ai_crew_manager.analyze_sentiment("I love this product")
    assert result == {"sentiment": "positive"}
    mock_crew.assert_called_once()
    mock_crew_instance.kickoff.assert_called_once()

def test_agent_initialization(ai_crew_manager):
    assert ai_crew_manager.analyst is not None
    assert ai_crew_manager.recommender is not None
    assert ai_crew_manager.sentiment_analyzer is not None

    assert ai_crew_manager.analyst.role == 'Data Analyst'
    assert ai_crew_manager.recommender.role == 'Recommendation Specialist'
    assert ai_crew_manager.sentiment_analyzer.role == 'Sentiment Analyst'

    assert ai_crew_manager.llm_config['model'] == "test_model"
    assert ai_crew_manager.llm_config['temperature'] == 0.7