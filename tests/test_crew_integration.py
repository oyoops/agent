import pytest
from ai_web_app.crew_integration import AICrewManager
from unittest.mock import patch, MagicMock

@pytest.fixture
def ai_crew_manager():
    return AICrewManager(api_key="test_key", model_name="test_model", max_tokens=100, temperature=0.7)

@patch('ai_web_app.crew_integration.Crew')
def test_analyze_data(mock_crew, ai_crew_manager):
    mock_crew_instance = MagicMock()
    mock_crew_instance.kickoff.return_value = "Detailed analysis result"
    mock_crew.return_value = mock_crew_instance

    result = ai_crew_manager.analyze_data({"test": "data"})
    assert result == {"analysis": "Detailed analysis result"}
    mock_crew.assert_called_once()
    mock_crew_instance.kickoff.assert_called_once()

@patch('ai_web_app.crew_integration.Crew')
def test_get_recommendation(mock_crew, ai_crew_manager):
    mock_crew_instance = MagicMock()
    mock_crew_instance.kickoff.return_value = "Personalized recommendation"
    mock_crew.return_value = mock_crew_instance

    result = ai_crew_manager.get_recommendation({"user": "test"})
    assert result == {"recommendations": "Personalized recommendation"}
    mock_crew.assert_called_once()
    mock_crew_instance.kickoff.assert_called_once()

@patch('ai_web_app.crew_integration.Crew')
def test_analyze_sentiment(mock_crew, ai_crew_manager):
    mock_crew_instance = MagicMock()
    mock_crew_instance.kickoff.return_value = "Positive sentiment"
    mock_crew.return_value = mock_crew_instance

    result = ai_crew_manager.analyze_sentiment("I love this product")
    assert result == {"sentiment_analysis": "Positive sentiment"}
    mock_crew.assert_called_once()
    mock_crew_instance.kickoff.assert_called_once()

@patch('ai_web_app.crew_integration.Crew')
def test_generate_content(mock_crew, ai_crew_manager):
    mock_crew_instance = MagicMock()
    mock_crew_instance.kickoff.return_value = "Generated article content"
    mock_crew.return_value = mock_crew_instance

    result = ai_crew_manager.generate_content("AI", "article")
    assert result == {"generated_content": "Generated article content"}
    mock_crew.assert_called_once()
    mock_crew_instance.kickoff.assert_called_once()

@patch('ai_web_app.crew_integration.Crew')
def test_comprehensive_analysis(mock_crew, ai_crew_manager):
    mock_crew_instance = MagicMock()
    mock_crew_instance.kickoff.return_value = "Comprehensive analysis result"
    mock_crew.return_value = mock_crew_instance

    result = ai_crew_manager.comprehensive_analysis({"complex": "data"})
    assert result == {"comprehensive_analysis": "Comprehensive analysis result"}
    mock_crew.assert_called_once()
    mock_crew_instance.kickoff.assert_called_once()

def test_agent_initialization(ai_crew_manager):
    assert ai_crew_manager.analyst is not None
    assert ai_crew_manager.recommender is not None
    assert ai_crew_manager.sentiment_analyzer is not None
    assert ai_crew_manager.content_creator is not None

    assert ai_crew_manager.analyst.role == 'Data Analyst'
    assert ai_crew_manager.recommender.role == 'Recommendation Specialist'
    assert ai_crew_manager.sentiment_analyzer.role == 'Sentiment Analyst'
    assert ai_crew_manager.content_creator.role == 'Content Creator'

    for agent in [ai_crew_manager.analyst, ai_crew_manager.recommender, 
                  ai_crew_manager.sentiment_analyzer, ai_crew_manager.content_creator]:
        assert agent.llm_config['model'] == "test_model"
        assert agent.llm_config['temperature'] == 0.7
        assert agent.llm_config['max_tokens'] == 100