from flask import Flask, request, jsonify
from .crew_integration import AICrewManager
from .logging_config import logger
from dotenv import load_dotenv
import os
import yaml

def create_app(config_path='config/config.yaml'):
    # Load environment variables and configuration
    load_dotenv('openai_key.env')
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    app = Flask(__name__)
    app.config.update(config)

    ai_crew_manager = AICrewManager(
        api_key=os.getenv('OPENAI_API_KEY'),
        model_name=app.config['ai']['model_name'],
        max_tokens=app.config['ai']['max_tokens'],
        temperature=app.config['ai']['temperature']
    )

    @app.route('/analyze', methods=['POST'])
    def analyze_data():
        if not app.config['features'].get('enable_data_analysis', True):
            logger.warning("Data analysis feature is disabled")
            return jsonify({"error": "Feature Disabled", "message": "Data analysis feature is currently disabled"}), 403
        
        try:
            data = request.json
            if not data:
                raise ValueError("No data provided")
            
            logger.info(f"Analyzing data: {data}")
            result = ai_crew_manager.analyze_data(data)
            return jsonify(result)
        except ValueError as e:
            logger.error(f"Invalid data for analysis: {str(e)}")
            return jsonify({"error": "Invalid Data", "message": str(e)}), 400
        except Exception as e:
            logger.error(f"Error during data analysis: {str(e)}")
            return jsonify({"error": "Analysis Error", "message": "An error occurred during data analysis"}), 500

    @app.route('/recommend', methods=['POST'])
    def get_recommendation():
        if not app.config['features'].get('enable_recommendations', True):
            logger.warning("Recommendations feature is disabled")
            return jsonify({"error": "Feature Disabled", "message": "Recommendations feature is currently disabled"}), 403
        
        try:
            user_data = request.json
            if not user_data:
                raise ValueError("No user data provided")
            
            logger.info(f"Getting recommendation for user data: {user_data}")
            recommendation = ai_crew_manager.get_recommendation(user_data)
            return jsonify(recommendation)
        except ValueError as e:
            logger.error(f"Invalid user data for recommendation: {str(e)}")
            return jsonify({"error": "Invalid Data", "message": str(e)}), 400
        except Exception as e:
            logger.error(f"Error during recommendation: {str(e)}")
            return jsonify({"error": "Recommendation Error", "message": "An error occurred during recommendation generation"}), 500

    @app.route('/sentiment', methods=['POST'])
    def analyze_sentiment():
        if not app.config['features'].get('enable_sentiment_analysis', True):
            logger.warning("Sentiment analysis feature is disabled")
            return jsonify({"error": "Feature Disabled", "message": "Sentiment analysis feature is currently disabled"}), 403
        
        try:
            text_data = request.json.get('text')
            if not text_data:
                raise ValueError("No text provided for sentiment analysis")
            
            logger.info(f"Analyzing sentiment for text: {text_data[:50]}...")  # Log only the first 50 characters
            sentiment = ai_crew_manager.analyze_sentiment(text_data)
            return jsonify(sentiment)
        except ValueError as e:
            logger.error(f"Invalid data for sentiment analysis: {str(e)}")
            return jsonify({"error": "Invalid Data", "message": str(e)}), 400
        except Exception as e:
            logger.error(f"Error during sentiment analysis: {str(e)}")
            return jsonify({"error": "Sentiment Analysis Error", "message": "An error occurred during sentiment analysis"}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['server']['host'],
        port=app.config['server']['port'],
        debug=app.config['app']['debug']
    )